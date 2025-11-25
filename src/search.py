"""
Content search for discovery patterns in pre-filtered repositories.

Fetches root-level markdown files and searches for discovery command patterns.
"""

import re
from github import Github, GithubException, RateLimitExceededException
from src.config import Config
from src.prefilter import load_search_config, check_rate_limit


def search_for_discovery_patterns(candidate_repos):
    """
    Search pre-filtered repos for discovery patterns.

    Args:
        candidate_repos: List of {owner, repo, url, ...} from prefilter

    Returns:
        List of repos with discovery patterns: [{repo_info, markdown_file, pattern_score}]
    """
    # Load pattern configuration
    config = load_search_config()
    patterns_config = config.get('discovery_patterns', [])
    target_files = config.get('target_files', ['README.md', 'CLAUDE.md'])

    # Build regex patterns with weights
    patterns = {}
    for pattern_def in patterns_config:
        pattern = pattern_def.get('pattern')
        weight = pattern_def.get('weight', 1)
        patterns[pattern] = weight

    print(f"  Loaded {len(patterns)} discovery patterns")
    print(f"  Target files: {', '.join(target_files)}")
    print()

    # Initialize GitHub client
    github_client = Github(Config.GITHUB_TOKEN)

    # Check initial rate limit
    check_rate_limit(github_client)
    print()

    discoveries = []
    total_repos = len(candidate_repos)

    for idx, candidate in enumerate(candidate_repos, 1):
        owner = candidate['owner']
        repo_name = candidate['repo']
        default_branch = candidate.get('default_branch', 'main')

        print(f"  [{idx}/{total_repos}] Searching {owner}/{repo_name}...")

        try:
            # Get repository object
            repo = github_client.get_repo(f"{owner}/{repo_name}")

            # Try each target markdown file
            best_match = None
            best_score = 0

            for target_file in target_files:
                try:
                    # Fetch file content
                    file_content = repo.get_contents(target_file, ref=default_branch)

                    if file_content.size > 500000:  # Skip files > 500KB
                        print(f"    ⚠ {target_file} too large ({file_content.size} bytes), skipping")
                        continue

                    # Decode content
                    content = file_content.decoded_content.decode('utf-8', errors='ignore')

                    # Search for patterns
                    patterns_found = []
                    score = 0

                    for pattern, weight in patterns.items():
                        # Search for pattern (case insensitive)
                        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                        if matches:
                            patterns_found.append(pattern)
                            # Score based on weight * number of occurrences (cap at 3x weight)
                            pattern_score = min(weight * len(matches), weight * 3)
                            score += pattern_score

                    if score > 0:
                        print(f"    ✓ {target_file}: {len(patterns_found)} patterns, score {score}")

                        if score > best_score:
                            best_score = score
                            best_match = {
                                'markdown_file': target_file,
                                'file_url': file_content.html_url,
                                'patterns_found': patterns_found,
                                'pattern_score': score,
                                'file_content_preview': content[:500]
                            }

                except GithubException as e:
                    if e.status == 404:
                        # File doesn't exist, continue to next file
                        continue
                    else:
                        print(f"    ⚠ Error fetching {target_file}: {e}")
                        continue

            # If we found patterns, add to discoveries
            if best_match:
                discovery = {
                    **candidate,  # Include all candidate info
                    **best_match  # Add discovery-specific fields
                }
                discoveries.append(discovery)
                print(f"    → Added to discoveries (best match: {best_match['markdown_file']})")
            else:
                print(f"    ✗ No discovery patterns found")

        except RateLimitExceededException as e:
            print(f"  ⚠ Rate limit exceeded at repo {idx}/{total_repos}")
            check_rate_limit(github_client)
            print("  Consider running again later or with fewer candidates")
            break

        except Exception as e:
            print(f"    ✗ Error processing repo: {e}")
            continue

    # Final summary
    print()
    print(f"  Processed {min(idx, total_repos)} repositories")
    print(f"  Found patterns in {len(discoveries)} repositories")
    print()

    # Check final rate limit
    check_rate_limit(github_client)

    return discoveries


if __name__ == '__main__':
    # Test the search with mock data
    print("Testing discovery pattern search...")
    print()

    # Mock candidate (Budget Analyzer orchestration repo for testing)
    mock_candidates = [
        {
            'owner': 'budgetanalyzer',
            'repo': 'orchestration',
            'url': 'https://github.com/budgetanalyzer/orchestration',
            'stars': 0,
            'topics': ['ai-assisted-development'],
            'last_push': '2024-11-25T00:00:00Z',
            'language': 'Shell',
            'description': 'Orchestration for Budget Analyzer',
            'default_branch': 'main'
        }
    ]

    try:
        results = search_for_discovery_patterns(mock_candidates)
        print()
        print(f"✓ Found {len(results)} repos with discovery patterns")
        print()

        if results:
            print("Results:")
            for discovery in results:
                print(f"  - {discovery['owner']}/{discovery['repo']}")
                print(f"    File: {discovery['markdown_file']}")
                print(f"    Score: {discovery['pattern_score']}")
                print(f"    Patterns: {', '.join(discovery['patterns_found'][:5])}")

    except Exception as e:
        print(f"✗ Error: {e}")
