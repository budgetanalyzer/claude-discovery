#!/usr/bin/env python3
"""
Generate static GitHub Pages site from discoveries.json
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import Counter


def load_discoveries():
    """Load discoveries from JSON file"""
    with open('discoveries.json', 'r') as f:
        return json.load(f)


def calculate_stats(data):
    """Calculate statistics from discoveries"""
    discoveries = data['discoveries']

    total = len(discoveries)
    high_quality = sum(1 for d in discoveries if d['quality']['score'] >= 7)
    medium_quality = sum(1 for d in discoveries if 5 <= d['quality']['score'] < 7)
    low_quality = sum(1 for d in discoveries if d['quality']['score'] < 5)

    # Count unique languages
    languages = set(
        d['repository']['language']
        for d in discoveries
        if d['repository']['language']
    )

    # Count patterns
    pattern_counter = Counter()
    for d in discoveries:
        for pattern in d['discovery']['patterns_found']:
            pattern_counter[pattern] += 1

    return {
        'total': total,
        'high_quality': high_quality,
        'medium_quality': medium_quality,
        'low_quality': low_quality,
        'language_count': len(languages),
        'patterns': pattern_counter
    }


def generate_discoveries_data_js(discoveries):
    """Generate JavaScript data file for client-side rendering"""
    # Convert discoveries to simplified format for JS
    js_data = []
    for d in discoveries:
        js_data.append({
            'repository': {
                'owner': d['repository']['owner'],
                'name': d['repository']['name'],
                'url': d['repository']['url'],
                'stars': d['repository']['stars'],
                'language': d['repository']['language'],
            },
            'discovery': {
                'markdown_file': d['discovery']['markdown_file'],
                'file_url': d['discovery']['file_url'],
                'patterns_found': d['discovery']['patterns_found'],
            },
            'quality': {
                'score': d['quality']['score'],
                'reasoning': d['quality']['reasoning'],
            },
            'contacts': d.get('contacts', [])[:3]  # Limit to first 3 contacts
        })

    js_content = f"// Auto-generated from discoveries.json\n"
    js_content += f"// Generated: {datetime.utcnow().isoformat()}Z\n\n"
    js_content += f"const discoveries = {json.dumps(js_data, indent=2)};\n"

    return js_content


def generate_pattern_library_content(pattern_counter, discoveries):
    """Generate HTML content for pattern library"""
    content = []

    # Group patterns by category
    docker_patterns = [p for p in pattern_counter if 'docker' in p.lower()]
    kubectl_patterns = [p for p in pattern_counter if 'kubectl' in p.lower()]
    git_patterns = [p for p in pattern_counter if 'git' in p.lower()]
    other_patterns = [
        p for p in pattern_counter
        if p not in docker_patterns + kubectl_patterns + git_patterns
    ]

    def render_pattern_section(title, description, patterns, icon):
        if not patterns:
            return ""

        # Find repos using these patterns
        repos_using = {}
        for pattern in patterns:
            repos_using[pattern] = []
            for d in discoveries:
                if pattern in d['discovery']['patterns_found']:
                    repo_name = f"{d['repository']['owner']}/{d['repository']['name']}"
                    repo_url = d['repository']['url']
                    repos_using[pattern].append((repo_name, repo_url))

        section = f"""
        <section class="pattern-section">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
            <div class="pattern-examples">
        """

        for pattern in sorted(patterns, key=lambda p: pattern_counter[p], reverse=True):
            count = pattern_counter[pattern]
            section += f"""
                <div>
                    <code class="pattern-code">{pattern}</code>
                    <div class="repos-using">
                        <strong>Used in {count} repositories</strong>
                        <div class="repo-list">
            """
            for repo_name, repo_url in sorted(repos_using[pattern])[:5]:  # Limit to 5
                section += f'<a href="{repo_url}" class="repo-badge">{repo_name}</a>'

            if len(repos_using[pattern]) > 5:
                section += f'<span class="repo-badge" style="background: var(--secondary-color)">+{len(repos_using[pattern]) - 5} more</span>'

            section += """
                        </div>
                    </div>
                </div>
            """

        section += """
            </div>
        </section>
        """
        return section

    # Generate sections
    content.append(render_pattern_section(
        "Docker Discovery Patterns",
        "Commands for exploring Docker containers, images, and logs",
        docker_patterns,
        "🐳"
    ))

    content.append(render_pattern_section(
        "Kubernetes Discovery Patterns",
        "Commands for exploring Kubernetes clusters, pods, and services",
        kubectl_patterns,
        "☸️"
    ))

    content.append(render_pattern_section(
        "Git Discovery Patterns",
        "Commands for exploring repository history and structure",
        git_patterns,
        "📚"
    ))

    content.append(render_pattern_section(
        "Other Discovery Patterns",
        "Additional exploration patterns found in repositories",
        other_patterns,
        "🔍"
    ))

    return '\n'.join(content)


def generate_site():
    """Generate complete static site"""
    print("Loading discoveries...")
    data = load_discoveries()
    discoveries = data['discoveries']

    print("Calculating statistics...")
    stats = calculate_stats(data)

    print(f"Found {stats['total']} discoveries:")
    print(f"  - High quality: {stats['high_quality']}")
    print(f"  - Medium quality: {stats['medium_quality']}")
    print(f"  - Low quality: {stats['low_quality']}")
    print(f"  - Languages: {stats['language_count']}")

    # Create site directory
    site_dir = Path('site')
    site_dir.mkdir(exist_ok=True)

    # Generate discoveries data JS
    print("Generating discoveries-data.js...")
    discoveries_js = generate_discoveries_data_js(discoveries)
    (site_dir / 'discoveries-data.js').write_text(discoveries_js)

    # Copy static files
    print("Copying static files...")
    templates_dir = Path('templates')
    shutil.copy(templates_dir / 'style.css', site_dir / 'style.css')
    shutil.copy(templates_dir / 'search.js', site_dir / 'search.js')

    # Generate index.html
    print("Generating index.html...")
    index_template = (templates_dir / 'index.html').read_text()
    index_html = index_template.replace('{{ total_count }}', str(stats['total']))
    index_html = index_html.replace('{{ high_quality_count }}', str(stats['high_quality']))
    index_html = index_html.replace('{{ language_count }}', str(stats['language_count']))
    index_html = index_html.replace('{{ last_updated }}', datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'))
    (site_dir / 'index.html').write_text(index_html)

    # Generate patterns.html
    print("Generating patterns.html...")
    pattern_content = generate_pattern_library_content(stats['patterns'], discoveries)
    patterns_template = (templates_dir / 'patterns.html').read_text()
    patterns_html = patterns_template.replace('{{ patterns_content }}', pattern_content)
    patterns_html = patterns_html.replace('{{ last_updated }}', datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'))
    (site_dir / 'patterns.html').write_text(patterns_html)

    # Copy about.html
    print("Generating about.html...")
    shutil.copy(templates_dir / 'about.html', site_dir / 'about.html')

    print(f"\n✓ Static site generated in {site_dir}/")
    print(f"  - index.html (main registry)")
    print(f"  - patterns.html (pattern library)")
    print(f"  - about.html (vision and principles)")
    print(f"  - discoveries-data.js (data for search)")
    print(f"  - style.css, search.js (assets)")
    print(f"\nTo preview locally:")
    print(f"  cd site && python3 -m http.server 8000")
    print(f"  Open http://localhost:8000")


if __name__ == '__main__':
    generate_site()
