# Deployment Guide

## GitHub Pages Deployment

### Prerequisites

1. Repository on GitHub
2. Generated static site in `site/` directory
3. GitHub Pages enabled in repository settings

### Step 1: Generate the Site

```bash
# Generate static site from discoveries
python3 src/site_generator.py
```

This creates the `site/` directory with:
- `index.html` - Main discovery registry
- `patterns.html` - Pattern library
- `about.html` - About page
- `discoveries-data.js` - Data for client-side search
- `style.css`, `search.js` - Assets

### Step 2: Enable GitHub Pages

1. Go to repository Settings > Pages
2. Source: Deploy from a branch
3. Branch: `main` (or your default branch)
4. Folder: `/site`
5. Click Save

### Step 3: Configure Custom Domain (Optional)

If you have a custom domain:

1. Add `CNAME` file to `site/` directory:
   ```bash
   echo "discovery.yourdomain.com" > site/CNAME
   ```

2. Configure DNS:
   - Add CNAME record: `discovery` → `yourusername.github.io`

3. In GitHub Pages settings:
   - Custom domain: `discovery.yourdomain.com`
   - Enforce HTTPS: ✓

### Step 4: Verify Deployment

1. Wait 1-2 minutes for deployment
2. Visit: `https://yourusername.github.io/claude-discovery/`
3. Test search functionality
4. Check all pages load correctly

## GitHub Discussions Setup

### Enable Discussions

1. Go to repository Settings > General
2. Features section
3. Check "Discussions"
4. Click "Set up discussions"

GitHub will create a default welcome discussion.

### Configure Discussion Categories

The discussion templates in `.github/DISCUSSION_TEMPLATE/` will automatically appear when creating new discussions:

- **Pattern Sharing** - Share discovery patterns found in documentation
- **Architecture Discussion** - Discuss AI-native architecture approaches

You can also create custom categories:

1. Go to Discussions tab
2. Click "New discussion"
3. Manage categories → Edit
4. Add categories like:
   - **General** - Open-ended discussions
   - **Show and tell** - Share your implementations
   - **Q&A** - Questions about discovery patterns
   - **Ideas** - Proposals for new features

### Pin Important Discussions

Pin key discussions to the top:

1. Create "Welcome" discussion explaining the purpose
2. Create "How to contribute patterns" guide
3. Pin both discussions

## Automation with GitHub Actions

### Auto-regenerate Site on New Discoveries

Create `.github/workflows/regenerate-site.yml`:

```yaml
name: Regenerate Site

on:
  push:
    paths:
      - 'discoveries.json'
      - 'opt-out.json'
  workflow_dispatch:

jobs:
  regenerate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Filter opted-out repositories
        run: python3 src/opt_manager.py filter

      - name: Generate site
        run: python3 src/site_generator.py

      - name: Commit updated site
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add site/
          git diff --quiet && git diff --staged --quiet || git commit -m "Auto-regenerate site from discoveries"

      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.ref }}
```

### Auto-run Discovery Weekly

Create `.github/workflows/weekly-discovery.yml`:

```yaml
name: Weekly Discovery

on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight
  workflow_dispatch:

jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run discovery
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python3 -m src.main

      - name: Filter opted-out repositories
        run: python3 src/opt_manager.py filter

      - name: Generate site
        run: python3 src/site_generator.py

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: "Weekly discovery run"
          title: "Weekly Discovery Results"
          body: "Automated weekly discovery run. Review new discoveries before merging."
          branch: weekly-discovery
```

## Maintenance

### Weekly Tasks

1. Review new opt-in/opt-out requests
2. Manually review new discoveries for quality
3. Update pattern library with new patterns
4. Respond to discussions

### Monthly Tasks

1. Audit opted-out repositories (ensure they're respected)
2. Review and improve quality scoring algorithm
3. Analyze which patterns are most common
4. Update documentation based on learnings

### Quarterly Tasks

1. Reach out to high-quality discoveries (score 8+)
2. Write blog post or update about findings
3. Refactor and improve codebase
4. Update discovery criteria based on ecosystem evolution

## Monitoring

### Track Metrics

- Total discoveries over time
- High-quality peer count
- Opt-out rate (should be low)
- Discussion activity
- Site traffic (via GitHub Insights)

### Health Checks

```bash
# Verify opt-out filtering works
python3 src/opt_manager.py list
python3 src/opt_manager.py filter

# Regenerate site and check for errors
python3 src/site_generator.py

# Validate discoveries data
python3 -c "import json; json.load(open('discoveries.json'))"
```

## Troubleshooting

### Site Not Updating

1. Check GitHub Actions logs
2. Verify `site/` directory has latest files
3. Force-push to trigger rebuild:
   ```bash
   git commit --allow-empty -m "Trigger Pages rebuild"
   git push
   ```

### Discussions Not Showing Templates

1. Ensure `.github/DISCUSSION_TEMPLATE/` exists
2. Templates must be `.yml` format
3. Check for YAML syntax errors
4. May take 5-10 minutes to appear after push

### Opt-Out Not Working

1. Check `opt-out.json` contains repository
2. Run `python3 src/opt_manager.py filter`
3. Regenerate site: `python3 src/site_generator.py`
4. Commit and push changes

## Security

### API Tokens

- Never commit `.env` file
- Use GitHub Actions secrets for tokens
- Rotate tokens periodically
- Use fine-grained tokens with minimal permissions

### Privacy

- Always respect opt-out requests promptly
- Only display publicly available information
- Don't scrape private repositories
- Honor `robots.txt` if doing additional scraping

## Support

Questions about deployment? Open a discussion or issue on GitHub.
