"""
Contact information extraction from discovered repositories.

Extracts public contact information (emails, GitHub usernames) from repos.
Privacy-respecting: Only uses public information.
"""

import re
from github import Github, GithubException
from src.config import Config


# Bot accounts to filter out
BOT_ACCOUNTS = {
    'dependabot', 'dependabot[bot]', 'renovate', 'renovate[bot]',
    'github-actions', 'github-actions[bot]', 'greenkeeper',
    'snyk-bot', 'codecov', 'imgbot', 'allcontributors'
}

# Example/dummy emails to ignore
IGNORE_EMAIL_PATTERNS = [
    r'.*@example\.com',
    r'.*@example\.org',
    r'.*@test\.com',
    r'no-?reply@.*',
    r'noreply@.*',
    r'.*dependabot.*',
    r'.*renovate.*',
    r'.*github-actions.*'
]


def is_valid_email(email):
    """Check if email appears to be valid and not a bot/example."""
    if not email:
        return False

    # Check against ignore patterns
    for pattern in IGNORE_EMAIL_PATTERNS:
        if re.match(pattern, email, re.IGNORECASE):
            return False

    # Basic email format check
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return re.match(email_pattern, email) is not None


def is_valid_username(username):
    """Check if GitHub username is valid and not a bot."""
    if not username:
        return False

    username_lower = username.lower()
    return username_lower not in BOT_ACCOUNTS


def extract_emails_from_text(text):
    """Extract email addresses from text."""
    if not text:
        return []

    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)

    # Filter and deduplicate
    valid_emails = set()
    for email in matches:
        if is_valid_email(email):
            valid_emails.add(email.lower())

    return list(valid_emails)


def extract_usernames_from_text(text):
    """Extract GitHub @mentions from text."""
    if not text:
        return []

    # GitHub mention pattern: @username
    mention_pattern = r'@([a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?)'
    matches = re.findall(mention_pattern, text)

    # Filter and deduplicate
    valid_usernames = set()
    for username in matches:
        if is_valid_username(username):
            valid_usernames.add(username)

    return list(valid_usernames)


def extract_contacts(repo_info):
    """
    Extract contact information from a repository.

    Args:
        repo_info: Repository information from search results

    Returns:
        List of contacts: [{type, value, source_file, confidence}]
    """
    contacts = []
    owner = repo_info['owner']
    repo_name = repo_info['repo']
    default_branch = repo_info.get('default_branch', 'main')

    # Initialize GitHub client
    github_client = Github(Config.GITHUB_TOKEN)

    try:
        repo = github_client.get_repo(f"{owner}/{repo_name}")

        # Files to check for contacts (in priority order)
        contact_files = [
            ('SECURITY.md', 'high'),
            ('CODE_OF_CONDUCT.md', 'high'),
            ('package.json', 'medium'),
            ('pyproject.toml', 'medium'),
            ('pom.xml', 'medium'),
            (repo_info.get('markdown_file', 'README.md'), 'low')
        ]

        seen_contacts = set()  # Deduplicate

        for filename, confidence in contact_files:
            try:
                file_content = repo.get_contents(filename, ref=default_branch)

                # Skip large files
                if file_content.size > 100000:  # 100KB limit for contact extraction
                    continue

                content = file_content.decoded_content.decode('utf-8', errors='ignore')

                # Extract emails
                emails = extract_emails_from_text(content)
                for email in emails:
                    if email not in seen_contacts:
                        contacts.append({
                            'type': 'email',
                            'value': email,
                            'source_file': filename,
                            'confidence': confidence
                        })
                        seen_contacts.add(email)

                # Extract GitHub usernames (only from markdown files)
                if filename.endswith('.md'):
                    usernames = extract_usernames_from_text(content)
                    for username in usernames:
                        username_key = f"@{username}"
                        if username_key not in seen_contacts:
                            contacts.append({
                                'type': 'github',
                                'value': username,
                                'source_file': filename,
                                'confidence': confidence
                            })
                            seen_contacts.add(username_key)

            except GithubException as e:
                if e.status == 404:
                    # File doesn't exist, continue
                    continue
                else:
                    # Other error, log and continue
                    continue

        # Fallback: Add repository owner as contact if no other contacts found
        if not contacts:
            owner_key = f"@{owner}"
            if owner_key not in seen_contacts:
                contacts.append({
                    'type': 'github',
                    'value': owner,
                    'source_file': 'repository_owner',
                    'confidence': 'low'
                })

    except Exception as e:
        # If all else fails, return owner as fallback
        contacts = [{
            'type': 'github',
            'value': owner,
            'source_file': 'repository_owner',
            'confidence': 'low'
        }]

    return contacts


if __name__ == '__main__':
    # Test extraction
    print("Testing contact extraction...")
    print()

    # Mock repo info (Budget Analyzer for testing)
    mock_repo = {
        'owner': 'budgetanalyzer',
        'repo': 'orchestration',
        'url': 'https://github.com/budgetanalyzer/orchestration',
        'default_branch': 'main',
        'markdown_file': 'CLAUDE.md'
    }

    try:
        contacts = extract_contacts(mock_repo)
        print(f"✓ Extracted {len(contacts)} contacts")
        print()

        if contacts:
            print("Contacts found:")
            for contact in contacts:
                print(f"  - {contact['type']}: {contact['value']}")
                print(f"    Source: {contact['source_file']} (confidence: {contact['confidence']})")

    except Exception as e:
        print(f"✗ Error: {e}")
