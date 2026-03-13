# Jargon Translation Skill

Translate GitHub-internal jargon, acronyms, and terminology using the [github/glossary](https://github.com/github/glossary) repository.

## When to Use This Skill

- Encountering unfamiliar GitHub acronyms or internal terms (e.g., PRU, CAPI, dialtone)
- Onboarding and need quick definitions
- Reading docs or Slack threads full of jargon
- Want to understand domain-specific terms (Actions, Copilot, Codespaces, etc.)

## Prerequisites

- [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated
- Access to the `github/glossary` repository

## Installation

### Personal Skills
```bash
cp -r jargon-translation-skill ~/.copilot/skills/
```

### Project Skills
```bash
cp -r jargon-translation-skill /path/to/repo/.github/skills/
```

## Usage

This skill activates when you ask Copilot to:
- "What does PRU mean?"
- "Define dialtone"
- "Translate this jargon: CAPI, AOAI, CCA"
- "What's the glossary definition of agent?"
- "Look up this acronym: IET"

The skill will:
1. Search the `github/glossary` repo for the term
2. Return the definition with source link
3. Check domain-specific glossaries if relevant (Copilot, Actions, etc.)

## Features

- **Multi-glossary search** - Searches main glossary and all domain-specific subdirectories
- **Batch lookups** - Translate multiple terms at once
- **Context-aware** - Suggests the most relevant glossary based on conversation context
- **Source links** - Always provides links back to the glossary repo

## Examples

See [`examples/basic-usage.md`](./examples/basic-usage.md) for detailed usage scenarios.

---

**Note:** This skill requires access to the private `github/glossary` repository.
