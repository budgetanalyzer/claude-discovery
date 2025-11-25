#!/usr/bin/env python3
"""
Manage opt-in and opt-out requests for the discovery registry
"""

import json
from datetime import datetime
from pathlib import Path


class OptOutManager:
    def __init__(self, opt_out_file='opt-out.json'):
        self.opt_out_file = Path(opt_out_file)
        self.data = self._load()

    def _load(self):
        """Load opt-out data"""
        if self.opt_out_file.exists():
            with open(self.opt_out_file, 'r') as f:
                return json.load(f)
        return {
            'opt_out_repositories': [],
            'last_updated': None,
            'notes': 'Repositories that have requested exclusion'
        }

    def _save(self):
        """Save opt-out data"""
        self.data['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        with open(self.opt_out_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_opt_out(self, owner, repo, reason=None):
        """Add a repository to the opt-out list"""
        repo_id = f"{owner}/{repo}"

        # Check if already opted out
        for entry in self.data['opt_out_repositories']:
            if entry['repository'] == repo_id:
                print(f"Repository {repo_id} is already opted out")
                return False

        entry = {
            'repository': repo_id,
            'opted_out_at': datetime.utcnow().isoformat() + 'Z',
            'reason': reason
        }

        self.data['opt_out_repositories'].append(entry)
        self._save()
        print(f"✓ Added {repo_id} to opt-out list")
        return True

    def remove_opt_out(self, owner, repo):
        """Remove a repository from the opt-out list (opt back in)"""
        repo_id = f"{owner}/{repo}"

        original_count = len(self.data['opt_out_repositories'])
        self.data['opt_out_repositories'] = [
            entry for entry in self.data['opt_out_repositories']
            if entry['repository'] != repo_id
        ]

        if len(self.data['opt_out_repositories']) < original_count:
            self._save()
            print(f"✓ Removed {repo_id} from opt-out list (opted back in)")
            return True
        else:
            print(f"Repository {repo_id} was not in the opt-out list")
            return False

    def is_opted_out(self, owner, repo):
        """Check if a repository is opted out"""
        repo_id = f"{owner}/{repo}"
        return any(
            entry['repository'] == repo_id
            for entry in self.data['opt_out_repositories']
        )

    def list_opted_out(self):
        """List all opted-out repositories"""
        return [entry['repository'] for entry in self.data['opt_out_repositories']]

    def filter_discoveries(self, discoveries_file='discoveries.json', output_file='discoveries.json'):
        """Filter discoveries to remove opted-out repositories"""
        with open(discoveries_file, 'r') as f:
            data = json.load(f)

        original_count = len(data['discoveries'])

        # Filter out opted-out repositories
        data['discoveries'] = [
            d for d in data['discoveries']
            if not self.is_opted_out(d['repository']['owner'], d['repository']['name'])
        ]

        filtered_count = original_count - len(data['discoveries'])

        if filtered_count > 0:
            # Save filtered discoveries
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Filtered {filtered_count} opted-out repositories")
            print(f"  Remaining discoveries: {len(data['discoveries'])}")
        else:
            print("No opted-out repositories found in discoveries")


def main():
    """CLI for managing opt-in/opt-out"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python opt_manager.py add <owner> <repo> [reason]")
        print("  python opt_manager.py remove <owner> <repo>")
        print("  python opt_manager.py list")
        print("  python opt_manager.py filter")
        print("  python opt_manager.py check <owner> <repo>")
        sys.exit(1)

    manager = OptOutManager()
    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 4:
            print("Error: Missing owner and repo")
            sys.exit(1)
        owner = sys.argv[2]
        repo = sys.argv[3]
        reason = sys.argv[4] if len(sys.argv) > 4 else None
        manager.add_opt_out(owner, repo, reason)

    elif command == 'remove':
        if len(sys.argv) < 4:
            print("Error: Missing owner and repo")
            sys.exit(1)
        owner = sys.argv[2]
        repo = sys.argv[3]
        manager.remove_opt_out(owner, repo)

    elif command == 'list':
        opted_out = manager.list_opted_out()
        if opted_out:
            print(f"Opted-out repositories ({len(opted_out)}):")
            for repo in opted_out:
                print(f"  - {repo}")
        else:
            print("No repositories have opted out")

    elif command == 'filter':
        manager.filter_discoveries()

    elif command == 'check':
        if len(sys.argv) < 4:
            print("Error: Missing owner and repo")
            sys.exit(1)
        owner = sys.argv[2]
        repo = sys.argv[3]
        if manager.is_opted_out(owner, repo):
            print(f"{owner}/{repo} is OPTED OUT")
        else:
            print(f"{owner}/{repo} is NOT opted out")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
