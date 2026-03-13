# TheHub Docs Search Skill

Search and retrieve documentation from GitHub's internal knowledge base (github/thehub).

## When to Use This Skill

- Finding engineering practices or development guides
- Looking up security policies and compliance standards
- Searching for deployment or operational procedures
- Finding team guides and onboarding materials
- Discovering service documentation
- Looking up incident response procedures
- HR, IT, or administrative procedures

## Prerequisites

This skill uses the GitHub MCP Server tools (`search_code`, `get_file_contents`) as its primary search method. For faster, offline access, clone `github/thehub` locally.

### Local Clone (Recommended)

Clone `github/thehub` for faster searches and offline access. The skill discovers the clone at runtime:

1. `THEHUB_LOCAL_PATH` environment variable (if set)
2. Sibling directory of the current repo (e.g. `../thehub`)
3. Falls back to MCP tools if no local clone is found

Optionally set the environment variable:

```bash
export THEHUB_LOCAL_PATH="$HOME/code/github/thehub"
```

## Installation

### Using gh-hubber-skills (Recommended)

```bash
gh extension install github/gh-hubber-skills
gh hubber-skills install thehub-docs-search-skill
```

### Manual Installation

**Personal skills** (available across all your projects):
```bash
cp -r thehub-docs-search-skill ~/.copilot/skills/
```

**Project-specific skills**:
```bash
cp -r thehub-docs-search-skill /path/to/your/repo/.github/skills/
```

## Usage

This skill activates when you ask Copilot to:
- "Search thehub for [topic]"
- "Find docs on [topic]"
- "What's the policy on [topic]?"
- "How do I [action]?" (for GitHub-internal processes)
- "Find the engineering guide for [topic]"
- "Search internal docs about [topic]"

## Features

- **Local-first access**: Prefers reading from a local clone for speed and offline use; falls back to MCP tools automatically
- **MCP-native**: Uses `search_code` and `get_file_contents` from the GitHub MCP Server, avoiding fragile shell pipelines
- **Compact**: ~120 lines of focused instructions that the agent can parse quickly without consuming excessive context
- **Directory-aware**: Understands the thehub docs structure for targeted searches
- **Metadata extraction**: Parses Jekyll frontmatter (title, owner_team, owner_slack)
- **Direct links**: Always provides thehub.github.com URLs

## Limitations

- **Read-only**: Cannot create or modify thehub docs
- **Access required**: Must have Hubber access to github/thehub
- **Search scope**: Only searches the github/thehub repository

## Support

- **Skill issues**: Open an issue in github/agent-skills
- **thehub access**: Contact #github-help on Slack
- **Documentation questions**: Use the owner_slack channel from the doc metadata
