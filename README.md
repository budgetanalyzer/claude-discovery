# claude-discovery: Finding Peers in AI-Native Architecture

> "I want to meet someone who is good enough to understand what I built."

## What Is This?

A discovery tool for finding GitHub repositories that use **discovery patterns** in their documentation - a signal that the architect independently figured out AI-native development practices.

This isn't about evangelism or user acquisition. It's about finding the "five people on the planet" working on AI-native architecture patterns and starting conversations.

## The Pattern We're Looking For

We're searching for a specific architectural approach:

- **Discovery commands over static lists** - Documentation that teaches through exploration (`kubectl get pods`, `tree -L 2`, `grep -r "pattern"`)
- **Pattern recognition** - If someone independently adopted discovery-based documentation, they "get it"
- **Production thinking** - Commands that help you understand real systems, not tutorials
- **Filename agnostic** - Whether it's README.md, CONTRIBUTING.md, or CLAUDE.md doesn't matter

Example discovery pattern:
```markdown
## Service Architecture

**Discovery**:
\```bash
# List all running resources
tilt get uiresources

# View pod status
kubectl get pods -n budget-analyzer
\```
```

If a root markdown file contains commands like these, that architect is thinking about AI-native development.

## How It Works

**Two-Stage Discovery:**

1. **Topic Pre-Filtering** - Use GitHub Search API to find candidate repos by topics
   - Primary: `topic:ai-assisted-development`
   - Fallback: `topic:devcontainer topic:kubernetes`
   - Reduces search space from millions to ~50 repos

2. **Content Search** - Scan pre-filtered repos for discovery patterns
   - Fetch root-level markdown files
   - Look for discovery command patterns (grep, kubectl, docker, tree, etc.)
   - Score based on pattern depth and quality

**Analysis:**
- Extract contact information (public data only)
- Score "peer potential" based on production signals
- Generate registry of discoveries

## Quick Start

### Running Discovery

```bash
# Clone the repository
git clone https://github.com/budgetanalyzer/claude-discovery.git
cd claude-discovery

# Set up environment
cp .env.example .env
# Edit .env and add your GitHub Personal Access Token

# Install dependencies
pip install -r requirements.txt

# Run discovery
python -m src.main

# View results
cat DISCOVERIES.md          # Human-readable findings
cat discoveries.json        # Machine-readable data
```

### Viewing the Registry

**Live Site:** [https://budgetanalyzer.github.io/claude-discovery](https://budgetanalyzer.github.io/claude-discovery) *(once deployed)*

**Local Preview:**
```bash
# Generate static site from discoveries
python3 src/site_generator.py

# Serve locally
cd site && python3 -m http.server 8000

# Open http://localhost:8000
```

The registry site includes:
- **Searchable discovery registry** - Filter by quality, language, patterns
- **Pattern library** - Common discovery patterns with examples
- **About page** - Philosophy and principles

### Managing Opt-In/Opt-Out

```bash
# Add repository to opt-out list
python3 src/opt_manager.py add owner repo "User request"

# Remove from opt-out (opt back in)
python3 src/opt_manager.py remove owner repo

# Check opt-out status
python3 src/opt_manager.py check owner repo

# Filter discoveries and regenerate site
python3 src/opt_manager.py filter
python3 src/site_generator.py
```

See [docs/OPT-IN-OUT.md](docs/OPT-IN-OUT.md) for complete opt-in/opt-out policy.

## Prerequisites

- Python 3.10+
- GitHub Personal Access Token (with `repo` scope for private search, `public_repo` for public only)

## Configuration

Create a `.env` file with your GitHub token:

```bash
GITHUB_TOKEN=ghp_your_token_here
```

Optional configuration in `config/search_queries.yaml`:
- Topic tiers and filters
- Quality scoring weights
- Contact extraction patterns

## What We're Looking For

**High-potential peers have:**
- Production implementations (not tutorials)
- Multiple related repositories (microservices pattern)
- CI/CD and deployment configurations
- Thoughtful documentation with discovery patterns
- Recent commits and active development

**We're NOT looking for:**
- Repositories that just renamed README to CLAUDE.md
- Static documentation without discovery commands
- Abandoned or tutorial-only projects
- Mass-adoption or ecosystem building

## Philosophical Principles

### Discovery, Not Evangelism
We're finding people who already figured it out independently, not convincing people to adopt a convention.

### Quality Over Quantity
Finding 5 peer architects > cataloging 500 repos with renamed READMEs.

### Privacy-Respecting
Only index public information. Respect robots.txt. Provide opt-out mechanisms.

### AI-Native Architecture
This tool itself exemplifies the patterns:
- Discoverable (has its own CLAUDE.md)
- Pattern-based documentation
- Simple, bounded context
- Runnable without complex setup

## Topic Standardization

We're establishing `ai-assisted-development` as a GitHub topic:
- Repositories built FOR and WITH AI as collaborative partner
- Discovery patterns in documentation
- Production-grade implementations
- Containerized development environments for AI agents

**Dogfooding:** Budget Analyzer repositories use this topic, making them discoverable by this tool.

## Project Status

**Current Phase:** Phase 3 Complete - Connection Layer

**Phase 1 - MVP Discovery Engine:** ✓ Complete
- [x] Topic-based pre-filtering
- [x] Content search for discovery patterns
- [x] Contact extraction
- [x] Quality scoring
- [x] Report generation (JSON + Markdown)
- [x] 24 repositories discovered, 3 high-quality peers identified

**Phase 2 - Pattern Recognition:** ✓ Complete
- [x] Pattern detection and categorization
- [x] Quality signal analysis
- [x] Findings documentation

**Phase 3 - Connection Layer:** ✓ Complete
- [x] GitHub Pages static site with searchable registry
- [x] Pattern library showcasing discovered patterns
- [x] GitHub Discussions templates for pattern sharing
- [x] Opt-in/opt-out mechanism with privacy-first approach
- [x] Automated site generation from discoveries

**Next Steps:**
- Enable GitHub Pages and Discussions (requires manual GitHub UI steps)
- Conduct outreach to high-quality peers (score 8+)
- Document conversations and learnings
- Iterate on discovery criteria based on feedback

See [docs/PLAN.md](docs/PLAN.md) for detailed roadmap and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment instructions.

## Why This Will Work

**Hypothesis:** There are architects independently discovering that microservices, pattern-based documentation, and discovery commands enable AI-native development.

**Evidence:** You found it. Others will too.

**Network Effect:** Discovery → Connection → Learning → Ecosystem

## Get Involved

### Opt-In or Opt-Out

**Want to be included in the registry?** [Submit an opt-in request](https://github.com/budgetanalyzer/claude-discovery/issues/new?template=opt-in-out.md)

**Want to be excluded?** [Submit an opt-out request](https://github.com/budgetanalyzer/claude-discovery/issues/new?template=opt-in-out.md) - no explanation needed, we respect your privacy.

See [docs/OPT-IN-OUT.md](docs/OPT-IN-OUT.md) for our complete privacy policy.

### Join the Conversation

**GitHub Discussions** *(once enabled)*:
- Share discovery patterns you've found
- Discuss AI-native architecture approaches
- Connect with peer architects
- Learn from others' implementations

### Contributing

This is a discovery project, not a community project (yet). If you've independently adopted discovery patterns in your documentation, we'd love to hear from you.

For now:
1. Star the repo if the pattern resonates
2. Add `ai-assisted-development` topic to your repos if you're doing this
3. [Share your discoveries](https://github.com/budgetanalyzer/claude-discovery/discussions)
4. Open an issue for bugs or feature requests

## License

MIT License - See LICENSE file for details

## Meta

This project uses discovery patterns in its own documentation. Point your AI at `github.com/budgetanalyzer/claude-discovery` and see how it works.

**Status:** Alpha - Building the discovery engine  
**Author:** Human architect + AI collaborator  
**Date:** 2025-01-24

---

> "This is how movements start: not with manifestos, but with people independently discovering truth and finding each other."
