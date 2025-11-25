"""
Topic-based pre-filtering for GitHub repository search.

Reduces search space from millions of repos to ~50-200 candidates
by using GitHub Search API with topic and metadata filters.
"""

import time
import yaml
from pathlib import Path
from github import Github, RateLimitExceededException
from src.config import Config


def load_search_config():
    """Load search queries configuration from YAML."""
    config_path = Config.CONFIG_DIR / 'search_queries.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def build_search_query(tier_config, filters):
    """
    Build GitHub search query string from tier config and filters.

    Args:
        tier_config: Tier configuration dict with topics
        filters: Common filters dict (archived, fork, stars, etc.)

    Returns:
        Query string for GitHub search API
    """
    query_parts = []

    # Add topics (OR condition for multiple topics in same tier)
    topics = tier_config.get('topics', [])
    if len(topics) == 1:
        query_parts.append(f"topic:{topics[0]}")
    elif len(topics) > 1:
        # Multiple topics: treat as OR (find repos with ANY of these topics)
        topic_query = ' OR '.join([f"topic:{t}" for t in topics])
        query_parts.append(f"({topic_query})")

    # Add common filters
    if filters.get('archived') is False:
        query_parts.append("archived:false")

    if filters.get('fork') is False:
        query_parts.append("fork:false")

    if 'min_stars' in filters:
        query_parts.append(f"stars:>={filters['min_stars']}")

    if 'pushed_after' in filters:
        query_parts.append(f"pushed:>{filters['pushed_after']}")

    if 'min_size_kb' in filters:
        query_parts.append(f"size:>={filters['min_size_kb']}")

    if 'min_topics' in filters:
        query_parts.append(f"topics:>={filters['min_topics']}")

    return ' '.join(query_parts)


def check_rate_limit(github_client):
    """Check and display rate limit status."""
    rate_limit = github_client.get_rate_limit()
    search_remaining = rate_limit.search.remaining
    search_limit = rate_limit.search.limit
    core_remaining = rate_limit.core.remaining
    core_limit = rate_limit.core.limit

    print(f"  Rate limits - Search: {search_remaining}/{search_limit}, "
          f"Core: {core_remaining}/{core_limit}")

    return rate_limit


def prefilter_by_topics(tier=1):
    """
    Pre-filter repositories using GitHub topic search.

    Args:
        tier: Which tier to search (1=primary, 2=fallback, 3=expansion)

    Returns:
        List of candidate repositories: [{owner, repo, url, stars, topics, last_push}]
    """
    # Load configuration
    config = load_search_config()
    tiers = config.get('tiers', [])
    filters = config.get('filters', {})

    # Validate tier
    if tier < 1 or tier > len(tiers):
        raise ValueError(f"Invalid tier {tier}. Must be 1-{len(tiers)}")

    # Get tier config (tiers are 1-indexed, list is 0-indexed)
    tier_config = tiers[tier - 1]
    tier_name = tier_config.get('name', f'tier-{tier}')
    topics = tier_config.get('topics', [])

    print(f"  Tier {tier}: {tier_name}")
    print(f"  Description: {tier_config.get('description', 'N/A')}")
    print(f"  Expected results: {tier_config.get('expected_results', 'unknown')}")
    print(f"  Topics: {', '.join(topics)}")
    print()

    # Initialize GitHub client
    github_client = Github(Config.GITHUB_TOKEN)

    # Check initial rate limit
    check_rate_limit(github_client)
    print()

    # Execute searches for each topic separately (GitHub doesn't support OR for topics)
    all_candidates = {}  # Use dict to deduplicate by repo full name

    for topic_idx, topic in enumerate(topics, 1):
        # Build query for this specific topic
        topic_config = {'topics': [topic]}
        query = build_search_query(topic_config, filters)

        print(f"  [{topic_idx}/{len(topics)}] Searching topic '{topic}'...")
        print(f"  Query: {query}")

        try:
            repositories = github_client.search_repositories(query=query)
            total_count = repositories.totalCount
            print(f"  Total matches: {total_count}")

            # Fetch results (respecting pagination)
            fetched = 0
            for idx, repo in enumerate(repositories, 1):
                full_name = f"{repo.owner.login}/{repo.name}"

                # Skip if already seen from another topic
                if full_name in all_candidates:
                    continue

                candidate = {
                    'owner': repo.owner.login,
                    'repo': repo.name,
                    'url': repo.html_url,
                    'stars': repo.stargazers_count,
                    'topics': repo.get_topics(),
                    'last_push': repo.pushed_at.isoformat() if repo.pushed_at else None,
                    'language': repo.language,
                    'description': repo.description,
                    'default_branch': repo.default_branch
                }
                all_candidates[full_name] = candidate
                fetched += 1

                # Progress indicator every 10 repos
                if fetched % 10 == 0:
                    print(f"  Fetched {fetched} new repositories...")

                # Safety limit per topic to avoid excessive API calls
                if fetched >= Config.DEFAULT_MAX_RESULTS // len(topics):
                    print(f"  Reached limit for this topic")
                    break

            print(f"  Retrieved {fetched} new repositories from this topic")
            print()

        except RateLimitExceededException as e:
            print(f"  ⚠ Rate limit exceeded: {e}")
            rate_limit = check_rate_limit(github_client)
            reset_time = rate_limit.search.reset
            print(f"  Rate limit resets at: {reset_time}")
            raise

        except Exception as e:
            print(f"  ✗ Search failed for topic '{topic}': {e}")
            print(f"  Continuing with remaining topics...")
            print()

    candidates = list(all_candidates.values())
    print(f"  Total unique repositories across all topics: {len(candidates)}")

    # Check final rate limit
    print()
    check_rate_limit(github_client)

    return candidates


if __name__ == '__main__':
    # Test the prefilter
    print("Testing topic pre-filter...")
    print()
    try:
        results = prefilter_by_topics(tier=1)
        print()
        print(f"✓ Found {len(results)} candidate repositories")
        print()

        if results:
            print("Sample results:")
            for i, repo in enumerate(results[:5], 1):
                print(f"  {i}. {repo['owner']}/{repo['repo']} - {repo['stars']} stars")
                print(f"     Topics: {', '.join(repo['topics'][:5])}")

    except NotImplementedError as e:
        print(f"✗ Not implemented yet: {e}")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
