# claude-discovery - AI-Native Discovery Tool

## Project Overview

A discovery tool for finding GitHub repositories that use discovery patterns in their documentation. This project is itself an example of the pattern it seeks: documentation that helps AI agents understand the codebase through exploration.

**Purpose**: Find peer architects who independently adopted discovery-based documentation for AI-native development.

**Not about**: Evangelism, user acquisition, or building a community. About finding the "five people on the planet" working on this.

## Development Environment

**This is an AI-native project.** Designed for AI agents to understand and extend.

**Discovery**:
```bash
# View project structure
tree -L 2 -I '__pycache__|*.pyc'

# List all Python modules
find src -name "*.py" -type f

# Check if environment is configured
test -f .env && echo "Configured" || echo "Need to copy .env.example"

# View dependencies
cat requirements.txt

# Check for TODO/FIXME markers
grep -r "TODO\|FIXME" src/ --include="*.py"
```

**Prerequisites**:
- Python 3.10+
- GitHub Personal Access Token
- Git (for version control)

**First-time setup**:
```bash
# Copy environment template
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN

# Install dependencies
pip install -r requirements.txt

# Run discovery
python -m src.main
```

## Architecture

**Pattern**: Single-purpose Python application with modular components

**Discovery**:
```bash
# View module structure
ls -la src/

# Check which modules are implemented
for file in src/*.py; do 
  echo "=== $file ===" 
  head -n 10 "$file" | grep -E "^(def|class)" || echo "Not implemented yet"
done

# View configuration structure
cat config/search_queries.yaml 2>/dev/null || echo "Config not yet created"
```

**Components**:
- `src/prefilter.py` - Topic-based GitHub search (reduces millions of repos to ~50 candidates)
- `src/search.py` - Content search for discovery patterns in pre-filtered repos
- `src/extract.py` - Contact information extraction (public data only)
- `src/analyze.py` - Quality scoring for "peer potential"
- `src/generate.py` - Report generation (discoveries.json, DISCOVERIES.md)
- `src/config.py` - Configuration management

**Data Flow**:
```
Topic Filter → Content Search → Contact Extract → Quality Analyze → Generate Reports
(prefilter)    (search)         (extract)        (analyze)       (generate)
```

## Discovery Patterns This Tool Looks For

The meta-pattern: We're searching for repos that use these same discovery techniques.

**Example patterns** (what we search for in other repos):
```markdown
## Service Architecture
**Discovery**:
\```bash
kubectl get pods -n namespace
docker ps
tilt get uiresources
\```

## Technology Stack
**Discovery**:
\```bash
grep -r "spring-boot" pom.xml
find . -name "package.json" -exec cat {} \;
\```

## Codebase Structure
**Discovery**:
\```bash
tree -L 2
find src -type f -name "*.java" | wc -l
\```
```

**Why these patterns matter**:
- Shows production thinking (real commands, not abstract descriptions)
- Enables AI agents to understand the codebase autonomously
- Indicates the architect "gets" AI-native development

## How The Search Works

**Two-stage approach** (necessary due to GitHub's massive scale):

**Stage 1: Topic Pre-Filtering**
```bash
# Simulated search (what the code does)
# topic:ai-native archived:false stars:>=50
# → ~50 candidate repos (99% reduction)

# View topic filter configuration
cat config/search_queries.yaml

# Check prefilter module
head -n 50 src/prefilter.py
```

**Stage 2: Content Search**
```bash
# Search only the pre-filtered candidates
# Fetch: README.md, CONTRIBUTING.md, DEVELOPMENT.md, ARCHITECTURE.md, CLAUDE.md
# Filter: Keep only files with discovery command patterns

# View search patterns
grep -A 5 "DISCOVERY_PATTERNS" src/search.py
```

**Quality Scoring**:
```bash
# View scoring criteria
grep -A 10 "def analyze_quality" src/analyze.py

# Check what signals we look for
grep -r "Production evidence\|Maturity markers" src/analyze.py
```

## Technology Stack

**Language**: Python 3.10+
- Simple, excellent for scripting and GitHub API interaction
- No over-engineering (this is a discovery tool, not a production service)

**Dependencies**:
```bash
# View all dependencies
cat requirements.txt

# Check dependency versions
pip list | grep -E "PyGithub|requests|python-dotenv"
```

**Key libraries**:
- `PyGithub` - GitHub API wrapper
- `requests` - HTTP client
- `python-dotenv` - Environment variable management
- `pytest` - Testing (Phase 2)

## Development Workflow

**Running the discovery**:
```bash
# Full discovery run
python -m src.main

# Run specific component (when implemented)
python -m src.prefilter    # Topic filtering only
python -m src.search       # Content search only
python -m src.analyze      # Analyze existing discoveries

# View results
cat discoveries.json | python -m json.tool | head -n 50
cat DISCOVERIES.md | head -n 100
```

**Testing** (Phase 2):
```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/test_extract.py -v

# Check test coverage
pytest --cov=src tests/
```

**Debugging**:
```bash
# Check for Python errors
python -m py_compile src/*.py

# View recent changes
git log --oneline -10

# Check what's committed vs working directory
git status
```

## Configuration

**Discovery**:
```bash
# View environment variables
cat .env.example

# Check if token is configured (doesn't show the token)
grep -q "GITHUB_TOKEN" .env && echo "Token configured" || echo "Need token"

# View search query configuration
cat config/search_queries.yaml
```

**Key settings**:
- `GITHUB_TOKEN` - Personal access token (required)
- `config/search_queries.yaml` - Topic filters, quality thresholds
- `.gitignore` - Ensures .env never gets committed

## Results & Output

**Discovery**:
```bash
# View discoveries (after running search)
cat DISCOVERIES.md

# Count how many repos found
jq 'length' discoveries.json

# View high-scoring repos only
jq '[.[] | select(.score >= 7)]' discoveries.json

# Extract contact emails
jq '.[].contacts[]?.email' discoveries.json | sort -u

# Group by programming language
jq 'group_by(.language) | map({language: .[0].language, count: length})' discoveries.json
```

## Project Status

**Discovery**:
```bash
# Check what's implemented
ls -la src/*.py | awk '{print $NF}' | while read f; do 
  lines=$(wc -l < "$f")
  echo "$f: $lines lines"
done

# View current phase from plan
grep -A 5 "## Phase 1" docs/PLAN.md | head -n 10

# Check recent progress
git log --oneline --since="1 week ago"
```

**Current phase**: Week 1 - Foundation  
**Next phase**: Week 2 - Core Search (prefilter.py, search.py)

## Best Practices

**For AI agents working on this project**:

1. **Stay simple** - This is a discovery tool, not a production service
2. **Respect rate limits** - GitHub API has 5000 req/hour (authenticated)
3. **Privacy first** - Only public information, respect robots.txt
4. **Pattern over filename** - Search for discovery commands, not specific filenames
5. **Quality over quantity** - Finding 5 peers > cataloging 500 repos

## Notes for Claude Code

**Meta-observation**: This CLAUDE.md exemplifies the pattern we're searching for:
- Discovery commands throughout (`tree`, `grep`, `find`, `jq`, `git`)
- Enables autonomous understanding of the codebase
- Shows real commands for real exploration
- Pattern-based, not prescriptive

**When extending this project**:
- Add discovery commands to any new documentation
- Keep the two-stage search strategy (topic → content)
- Maintain simplicity (resist over-engineering)
- Test the hypothesis: Do discovery patterns help you understand this codebase faster?

**Path portability**: This repo works anywhere, not just `/workspace/claude-discovery/`. All paths should be relative or use dynamic resolution.

**Dogfooding**: This repo should be discoverable by its own search tool. After implementing search, run it and verify that `claude-discovery` itself appears in results.

## See Also

- [README.md](README.md) - Public-facing vision statement
- [docs/PLAN.md](docs/PLAN.md) - Detailed implementation plan
- [docs/PATTERNS.md](docs/PATTERNS.md) - Observed architectural patterns (generated)
- [docs/FINDINGS.md](docs/FINDINGS.md) - Qualitative observations (generated)

---

**This is a living document.** As we implement search and find peers, we'll update based on what we learn.

**Status**: Foundation phase  
**Author**: Human architect + AI collaborator  
**Date**: 2025-01-24
