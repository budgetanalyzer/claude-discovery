"""
Quality analysis and peer potential scoring.

Analyzes repos to distinguish production implementations from tutorials.
Scores repos on a 1-10 scale for "peer potential".
"""

from datetime import datetime, timezone
from github import Github, GithubException
from src.config import Config
from src.prefilter import load_search_config


def check_ci_cd(repo):
    """Check if repository has CI/CD configuration."""
    ci_cd_indicators = [
        '.github/workflows',
        '.circleci',
        'circle.yml',
        '.gitlab-ci.yml',
        'Jenkinsfile',
        '.travis.yml'
    ]

    try:
        contents = repo.get_contents("")
        filenames = [item.name for item in contents if item.type == "dir"] + \
                   [item.name for item in contents if item.type == "file"]

        for indicator in ci_cd_indicators:
            if indicator in filenames:
                return True, indicator
    except:
        pass

    return False, None


def check_tests(repo):
    """Check if repository has test directories/files."""
    test_indicators = [
        'test',
        'tests',
        '__tests__',
        'spec',
        'specs'
    ]

    try:
        contents = repo.get_contents("")
        dirnames = [item.name.lower() for item in contents if item.type == "dir"]

        for indicator in test_indicators:
            if indicator in dirnames:
                return True, indicator
    except:
        pass

    return False, None


def check_docker_kubernetes(repo):
    """Check for Docker and Kubernetes configurations."""
    docker_k8s_indicators = {
        'Dockerfile': 'docker',
        'docker-compose.yml': 'docker',
        'docker-compose.yaml': 'docker',
        'Tiltfile': 'kubernetes',
        'kubernetes': 'kubernetes',
        'k8s': 'kubernetes',
        'helm': 'kubernetes',
        '.devcontainer': 'devcontainer'
    }

    found = {'docker': False, 'kubernetes': False, 'devcontainer': False}
    details = []

    try:
        contents = repo.get_contents("")
        items = {item.name: item.type for item in contents}

        for indicator, category in docker_k8s_indicators.items():
            if indicator in items:
                found[category] = True
                details.append(indicator)
    except:
        pass

    return found, details


def check_related_repos(github_client, owner):
    """Check if owner has multiple related repositories (microservices pattern)."""
    try:
        user = github_client.get_user(owner)
        repos = list(user.get_repos())

        # Look for patterns suggesting microservices architecture
        service_patterns = ['-service', '_service', 'service-', '-api', '-gateway', '-common']
        related_repos = []

        for repo in repos:
            repo_name_lower = repo.name.lower()
            for pattern in service_patterns:
                if pattern in repo_name_lower:
                    related_repos.append(repo.name)
                    break

        return len(related_repos), related_repos[:5]  # Return count and sample

    except:
        return 0, []


def analyze_quality(repo_info):
    """
    Analyze repository quality and calculate peer potential score.

    Args:
        repo_info: Repository information from search results

    Returns:
        {
            score: int (1-10),
            signals_found: [list of quality signals],
            signal_details: {dict of detailed signals},
            reasoning: str (explanation of score)
        }
    """
    owner = repo_info['owner']
    repo_name = repo_info['repo']
    pattern_score = repo_info.get('pattern_score', 0)

    # Initialize GitHub client
    github_client = Github(Config.GITHUB_TOKEN)

    # Initialize scoring
    score = 0
    signals_found = []
    signal_details = {}
    reasoning_parts = []

    try:
        repo = github_client.get_repo(f"{owner}/{repo_name}")

        # 1. Production Evidence (max 5 points)
        has_ci, ci_detail = check_ci_cd(repo)
        if has_ci:
            score += 2
            signals_found.append('has_ci_cd')
            signal_details['ci_cd'] = ci_detail
            reasoning_parts.append(f"CI/CD via {ci_detail}")

        has_tests, test_detail = check_tests(repo)
        if has_tests:
            score += 2
            signals_found.append('has_tests')
            signal_details['tests'] = test_detail
            reasoning_parts.append(f"tests in {test_detail}/")

        docker_k8s, dk_details = check_docker_kubernetes(repo)
        if docker_k8s['docker']:
            score += 1
            signals_found.append('has_docker')
            signal_details['docker'] = True

        if docker_k8s['kubernetes']:
            score += 2
            signals_found.append('has_kubernetes')
            signal_details['kubernetes'] = dk_details
            reasoning_parts.append(f"K8s configs: {', '.join(dk_details[:3])}")

        if docker_k8s['devcontainer']:
            score += 1
            signals_found.append('has_devcontainer')
            signal_details['devcontainer'] = True
            reasoning_parts.append("devcontainer setup")

        # 2. Discovery Pattern Depth (max 3 points)
        # Normalize pattern score to 0-3 range
        normalized_pattern = min(pattern_score / 10, 3)
        score += normalized_pattern

        if pattern_score > 10:
            signals_found.append('high_discovery_depth')
            reasoning_parts.append(f"rich discovery patterns (score: {pattern_score})")
        elif pattern_score > 5:
            signals_found.append('medium_discovery_depth')

        signal_details['pattern_score'] = pattern_score

        # 3. Activity Signals (max 2 points)
        last_push = repo.pushed_at
        if last_push:
            days_since_push = (datetime.now(timezone.utc) - last_push).days
            signal_details['days_since_push'] = days_since_push

            if days_since_push < 30:
                score += 1
                signals_found.append('recent_commits')
                reasoning_parts.append(f"active ({days_since_push}d ago)")

        try:
            contributors = repo.get_contributors()
            contributor_count = contributors.totalCount

            if contributor_count > 1:
                score += 1
                signals_found.append('multiple_contributors')
                signal_details['contributors'] = contributor_count
                reasoning_parts.append(f"{contributor_count} contributors")
        except:
            pass

        # 4. Related Repos (max 3 points)
        related_count, related_sample = check_related_repos(github_client, owner)
        if related_count > 0:
            related_points = min(related_count, 3)
            score += related_points
            signals_found.append('multiple_repos')
            signal_details['related_repos'] = related_sample
            reasoning_parts.append(f"{related_count} related repos")

        # Cap at 10
        final_score = min(int(score), 10)

        # Build reasoning
        if reasoning_parts:
            reasoning = "; ".join(reasoning_parts)
        else:
            reasoning = "Minimal production signals detected"

        # Add overall assessment
        if final_score >= 7:
            reasoning = f"High-quality peer: {reasoning}"
        elif final_score >= 5:
            reasoning = f"Medium-quality: {reasoning}"
        else:
            reasoning = f"Low production signals: {reasoning}"

        return {
            'score': final_score,
            'signals_found': signals_found,
            'signal_details': signal_details,
            'reasoning': reasoning
        }

    except Exception as e:
        # Fallback scoring based on pattern score alone
        fallback_score = min(int(pattern_score / 2), 5)
        return {
            'score': fallback_score,
            'signals_found': ['pattern_only'],
            'signal_details': {'pattern_score': pattern_score, 'error': str(e)},
            'reasoning': f"Limited analysis (error: {str(e)[:50]}), scored on patterns only"
        }


if __name__ == '__main__':
    # Test quality analysis
    print("Testing quality analysis...")
    print()

    # Mock repo info (Budget Analyzer for testing)
    mock_repo = {
        'owner': 'budgetanalyzer',
        'repo': 'orchestration',
        'url': 'https://github.com/budgetanalyzer/orchestration',
        'pattern_score': 15,
        'patterns_found': ['kubectl', 'tree -', 'grep -r', 'tilt']
    }

    try:
        quality = analyze_quality(mock_repo)
        print(f"✓ Quality analysis complete")
        print()
        print(f"Score: {quality['score']}/10")
        print(f"Signals: {', '.join(quality['signals_found'])}")
        print(f"Reasoning: {quality['reasoning']}")
        print()
        print("Details:")
        for key, value in quality['signal_details'].items():
            print(f"  {key}: {value}")

    except Exception as e:
        print(f"✗ Error: {e}")
