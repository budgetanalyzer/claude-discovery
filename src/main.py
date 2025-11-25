"""
Main entry point for claude-discovery.

Orchestrates the discovery workflow:
1. Pre-filter by topics
2. Search for discovery patterns
3. Extract contacts
4. Analyze quality
5. Generate reports
"""

import sys
from src.config import Config
from src.prefilter import prefilter_by_topics
from src.search import search_for_discovery_patterns
from src.extract import extract_contacts
from src.analyze import analyze_quality
from src.generate import generate_reports


def main(tier=1):
    """Run the complete discovery workflow.

    Args:
        tier: Which topic tier to search (1=primary, 2=fallback, 3=expansion)
    """
    try:
        # Validate configuration
        print("Validating configuration...")
        Config.validate()
        print(f"✓ Configuration valid")
        print(f"  GitHub token: {'*' * 20}")
        print()

        # Stage 1: Topic pre-filtering
        print("Stage 1: Pre-filtering by topics...")
        print(f"  Searching with tier {tier}...")
        candidates = prefilter_by_topics(tier=tier)
        print(f"✓ Found {len(candidates)} candidate repositories")
        print()
        
        # Stage 2: Content search
        print("Stage 2: Searching for discovery patterns...")
        discoveries = search_for_discovery_patterns(candidates)
        print(f"✓ Found {len(discoveries)} repos with discovery patterns")
        print()
        
        # Stage 3: Contact extraction
        print("Stage 3: Extracting contact information...")
        for discovery in discoveries:
            discovery['contacts'] = extract_contacts(discovery)
        contact_count = sum(len(d.get('contacts', [])) for d in discoveries)
        print(f"✓ Extracted {contact_count} contacts")
        print()
        
        # Stage 4: Quality analysis
        print("Stage 4: Analyzing quality...")
        for discovery in discoveries:
            discovery['quality'] = analyze_quality(discovery)
        high_quality = [d for d in discoveries if d['quality']['score'] >= Config.QUALITY_THRESHOLD]
        print(f"✓ Analyzed {len(discoveries)} repos")
        print(f"  {len(high_quality)} repos scored >= {Config.QUALITY_THRESHOLD}")
        print()
        
        # Stage 5: Generate reports
        print("Stage 5: Generating reports...")
        metadata = {
            'tier': tier,
            'total_candidates': len(candidates)
        }
        report_paths = generate_reports(discoveries, metadata=metadata)
        print(f"✓ Reports generated:")
        print(f"  JSON: {report_paths['json']}")
        print(f"  Markdown: {report_paths['markdown']}")
        print()
        
        print("Discovery complete!")
        print(f"Found {len(high_quality)} high-quality peers.")
        
        return 0
        
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1
    except NotImplementedError as e:
        print(f"Not implemented: {e}", file=sys.stderr)
        print("\nThis is expected during development.")
        print("See docs/PLAN.md for implementation timeline.")
        return 2
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 3


if __name__ == '__main__':
    # Parse command line arguments
    tier = 1  # Default to tier 1
    if len(sys.argv) > 1:
        try:
            tier = int(sys.argv[1])
            if tier < 1 or tier > 3:
                print(f"Error: Invalid tier {tier}. Must be 1, 2, or 3.", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print(f"Error: Invalid tier argument '{sys.argv[1]}'. Must be an integer.", file=sys.stderr)
            sys.exit(1)

    sys.exit(main(tier=tier))
