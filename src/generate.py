"""
Discovery report generation.

Generates both machine-readable (JSON) and human-readable (Markdown) reports.
"""

import json
from datetime import datetime
from collections import Counter
from src.config import Config


def generate_json_report(discoveries, output_path=None, metadata=None):
    """
    Generate machine-readable JSON report.

    Args:
        discoveries: List of discovery results
        output_path: Optional path override (defaults to Config.DISCOVERIES_JSON)
        metadata: Optional metadata dict to include

    Returns:
        Path to generated file
    """
    if output_path is None:
        output_path = Config.DISCOVERIES_JSON

    # Calculate statistics
    total_discoveries = len(discoveries)
    high_quality = [d for d in discoveries if d.get('quality', {}).get('score', 0) >= 7]
    medium_quality = [d for d in discoveries if 5 <= d.get('quality', {}).get('score', 0) < 7]

    # Build report structure
    report = {
        'metadata': {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'version': '1.0',
            'total_discoveries': total_discoveries,
            'high_quality_count': len(high_quality),
            'medium_quality_count': len(medium_quality),
            **(metadata or {})
        },
        'discoveries': []
    }

    # Sort discoveries by quality score (descending)
    sorted_discoveries = sorted(
        discoveries,
        key=lambda d: d.get('quality', {}).get('score', 0),
        reverse=True
    )

    # Add each discovery
    for discovery in sorted_discoveries:
        report['discoveries'].append({
            'repository': {
                'owner': discovery.get('owner'),
                'name': discovery.get('repo'),
                'url': discovery.get('url'),
                'stars': discovery.get('stars'),
                'language': discovery.get('language'),
                'topics': discovery.get('topics', []),
                'last_push': discovery.get('last_push')
            },
            'discovery': {
                'markdown_file': discovery.get('markdown_file'),
                'file_url': discovery.get('file_url'),
                'patterns_found': discovery.get('patterns_found', []),
                'pattern_score': discovery.get('pattern_score', 0)
            },
            'contacts': discovery.get('contacts', []),
            'quality': discovery.get('quality', {})
        })

    # Write JSON file
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    return str(output_path)


def generate_markdown_report(discoveries, output_path=None, metadata=None):
    """
    Generate human-readable Markdown report.

    Args:
        discoveries: List of discovery results
        output_path: Optional path override (defaults to Config.DISCOVERIES_MD)
        metadata: Optional metadata dict to include

    Returns:
        Path to generated file
    """
    if output_path is None:
        output_path = Config.DISCOVERIES_MD

    # Calculate statistics
    total_discoveries = len(discoveries)
    high_quality = [d for d in discoveries if d.get('quality', {}).get('score', 0) >= 7]
    medium_quality = [d for d in discoveries if 5 <= d.get('quality', {}).get('score', 0) < 7]
    low_quality = [d for d in discoveries if d.get('quality', {}).get('score', 0) < 5]

    # Sort discoveries by quality score (descending)
    sorted_discoveries = sorted(
        discoveries,
        key=lambda d: d.get('quality', {}).get('score', 0),
        reverse=True
    )

    # Count pattern frequencies
    all_patterns = []
    for d in discoveries:
        all_patterns.extend(d.get('patterns_found', []))
    pattern_counts = Counter(all_patterns)

    # Build markdown
    lines = []
    lines.append("# Discovery Report")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    lines.append("")

    # Summary section
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total discoveries:** {total_discoveries}")
    lines.append(f"- **High-quality peers (score ≥ 7):** {len(high_quality)}")
    lines.append(f"- **Medium-quality (score 5-6):** {len(medium_quality)}")
    lines.append(f"- **Lower quality (score < 5):** {len(low_quality)}")
    lines.append("")

    if metadata:
        lines.append("### Search Parameters")
        lines.append("")
        for key, value in metadata.items():
            lines.append(f"- **{key}:** {value}")
        lines.append("")

    # High quality discoveries
    if high_quality:
        lines.append("## High-Quality Peers (Score ≥ 7)")
        lines.append("")
        lines.append("| Repository | Stars | Score | Patterns | Language | Contact | Last Push |")
        lines.append("|------------|-------|-------|----------|----------|---------|-----------|")

        for d in high_quality:
            repo_link = f"[{d['owner']}/{d['repo']}]({d['url']})"
            stars = d.get('stars', 0)
            score = d.get('quality', {}).get('score', 0)
            pattern_count = len(d.get('patterns_found', []))
            language = d.get('language', 'N/A')

            # Get first contact
            contacts = d.get('contacts', [])
            if contacts:
                first_contact = contacts[0]
                if first_contact['type'] == 'email':
                    contact_str = first_contact['value']
                else:
                    contact_str = f"@{first_contact['value']}"
            else:
                contact_str = "N/A"

            last_push = d.get('last_push', 'Unknown')
            if last_push and last_push != 'Unknown':
                last_push = last_push[:10]  # Just the date

            lines.append(f"| {repo_link} | {stars} | {score} | {pattern_count} | {language} | {contact_str} | {last_push} |")

        lines.append("")

        # Details for high-quality repos
        lines.append("### Details")
        lines.append("")
        for d in high_quality:
            lines.append(f"#### [{d['owner']}/{d['repo']}]({d['url']})")
            lines.append("")
            lines.append(f"**Quality Score:** {d.get('quality', {}).get('score', 0)}/10")
            lines.append("")
            lines.append(f"**Reasoning:** {d.get('quality', {}).get('reasoning', 'N/A')}")
            lines.append("")
            lines.append(f"**Discovery File:** [{d.get('markdown_file')}]({d.get('file_url')})")
            lines.append("")
            patterns = d.get('patterns_found', [])
            if patterns:
                lines.append(f"**Patterns Found:** {', '.join(patterns[:10])}")
                lines.append("")
            lines.append("---")
            lines.append("")

    # Medium quality discoveries
    if medium_quality:
        lines.append("## Medium-Quality (Score 5-6)")
        lines.append("")
        lines.append("| Repository | Stars | Score | Patterns | Contact |")
        lines.append("|------------|-------|-------|----------|---------|")

        for d in medium_quality:
            repo_link = f"[{d['owner']}/{d['repo']}]({d['url']})"
            stars = d.get('stars', 0)
            score = d.get('quality', {}).get('score', 0)
            pattern_count = len(d.get('patterns_found', []))

            contacts = d.get('contacts', [])
            contact_str = contacts[0]['value'] if contacts else "N/A"

            lines.append(f"| {repo_link} | {stars} | {score} | {pattern_count} | {contact_str} |")

        lines.append("")

    # Low quality (just list)
    if low_quality:
        lines.append("## Lower Quality (Score < 5)")
        lines.append("")
        for d in low_quality:
            repo_link = f"[{d['owner']}/{d['repo']}]({d['url']})"
            score = d.get('quality', {}).get('score', 0)
            lines.append(f"- {repo_link} (score: {score})")
        lines.append("")

    # Pattern analysis
    if pattern_counts:
        lines.append("## Pattern Analysis")
        lines.append("")
        lines.append("Most common discovery patterns:")
        lines.append("")
        for pattern, count in pattern_counts.most_common(10):
            lines.append(f"- `{pattern}`: {count} repos")
        lines.append("")

    # Next steps
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. Review high-quality peers manually")
    lines.append("2. Check for false positives in pattern matching")
    lines.append("3. Draft outreach message for top candidates")
    lines.append("4. Initiate contact with 1-3 high-potential peers")
    lines.append("")

    # Write markdown file
    content = '\n'.join(lines)
    with open(output_path, 'w') as f:
        f.write(content)

    return str(output_path)


def generate_reports(discoveries, metadata=None):
    """
    Generate both JSON and Markdown reports.

    Args:
        discoveries: List of discovery results
        metadata: Optional metadata dict to include in reports

    Returns:
        {'json': json_path, 'markdown': md_path}
    """
    json_path = generate_json_report(discoveries, metadata=metadata)
    md_path = generate_markdown_report(discoveries, metadata=metadata)

    return {
        'json': json_path,
        'markdown': md_path
    }


if __name__ == '__main__':
    # Test report generation
    print("Testing report generation...")
    print()

    # Mock discoveries
    mock_discoveries = [
        {
            'owner': 'budgetanalyzer',
            'repo': 'orchestration',
            'url': 'https://github.com/budgetanalyzer/orchestration',
            'stars': 5,
            'language': 'Shell',
            'topics': ['ai-assisted-development', 'kubernetes'],
            'last_push': '2024-11-25T00:00:00Z',
            'markdown_file': 'CLAUDE.md',
            'file_url': 'https://github.com/budgetanalyzer/orchestration/blob/main/CLAUDE.md',
            'patterns_found': ['kubectl', 'tree -', 'grep -r', 'tilt'],
            'pattern_score': 15,
            'contacts': [
                {'type': 'github', 'value': 'budgetanalyzer', 'source_file': 'repository_owner', 'confidence': 'low'}
            ],
            'quality': {
                'score': 8,
                'signals_found': ['has_ci_cd', 'has_kubernetes', 'high_discovery_depth'],
                'reasoning': 'High-quality peer: K8s configs, rich discovery patterns'
            }
        }
    ]

    try:
        metadata = {'tier': 1, 'total_candidates': 10}
        paths = generate_reports(mock_discoveries, metadata=metadata)

        print(f"✓ Reports generated successfully")
        print()
        print(f"JSON report: {paths['json']}")
        print(f"Markdown report: {paths['markdown']}")

    except Exception as e:
        print(f"✗ Error: {e}")
