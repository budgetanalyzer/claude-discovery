# Opt-In and Opt-Out Policy

## Philosophy

Claude Discovery respects privacy and repository ownership. All information in the registry is sourced from publicly available repositories, but we recognize that not all maintainers may want to be listed.

## Privacy Principles

1. **Public Information Only**: We only index publicly available repository data
2. **Respect Requests**: We promptly honor all opt-out requests
3. **No Tracking**: We don't track repository activity beyond initial discovery
4. **Consent-First**: Repository owners can request inclusion or exclusion at any time
5. **Transparency**: Our discovery methodology and criteria are fully documented

## How to Opt Out

If you'd like your repository removed from the discovery registry:

1. **Open an Issue**: [Submit an opt-out request](https://github.com/budgetanalyzer/claude-discovery/issues/new?template=opt-in-out.md)
2. **Provide Repository URL**: Include the full GitHub URL of your repository
3. **No Explanation Required**: We respect your privacy - no need to explain why

Your repository will be removed from the registry within 48 hours.

## How to Opt In

If you'd like your repository included in the discovery registry:

1. **Check Criteria**: Ensure your repository uses discovery patterns in documentation
2. **Open an Issue**: [Submit an opt-in request](https://github.com/budgetanalyzer/claude-discovery/issues/new?template=opt-in-out.md)
3. **Provide Context**: Describe what discovery patterns you use
4. **Consent**: Confirm you're okay with publicly available contact info being displayed

We'll review your request and add your repository if it meets the criteria.

## Discovery Criteria

Repositories are included if they:

1. **Use discovery patterns** in root-level markdown files (README.md, CONTRIBUTING.md, etc.)
2. **Contain exploration commands** like `grep`, `kubectl`, `docker`, `find`, `git log`
3. **Show production thinking** (not just tutorials or generic documentation)
4. **Have quality signals** (tests, CI/CD, multiple contributors, etc.)

## What Information Is Displayed

For included repositories, we display:

- Repository name, owner, and URL
- Star count and primary language
- Discovery patterns found
- Links to files containing discovery patterns
- Publicly stated contact information (from SECURITY.md, package.json, etc.)
- Quality score based on production indicators

## Managing Opt-Out Requests (Maintainers)

For claude-discovery maintainers, use the `opt_manager.py` tool:

```bash
# Add repository to opt-out list
python src/opt_manager.py add owner repo "User request via issue #123"

# Remove repository from opt-out list (opt back in)
python src/opt_manager.py remove owner repo

# Check if repository is opted out
python src/opt_manager.py check owner repo

# List all opted-out repositories
python src/opt_manager.py list

# Filter discoveries.json to exclude opted-out repos
python src/opt_manager.py filter
```

## Automated Filtering

The discovery and site generation scripts automatically respect the opt-out list:

1. `opt-out.json` maintains the list of excluded repositories
2. `opt_manager.py filter` removes opted-out repos from `discoveries.json`
3. `site_generator.py` generates the site from the filtered discoveries
4. GitHub Actions can automate this workflow

## Questions?

If you have questions about opt-in/opt-out or privacy:

- Open an issue: https://github.com/budgetanalyzer/claude-discovery/issues
- Start a discussion: https://github.com/budgetanalyzer/claude-discovery/discussions

We're committed to respecting repository owners' preferences and maintaining a privacy-first approach.
