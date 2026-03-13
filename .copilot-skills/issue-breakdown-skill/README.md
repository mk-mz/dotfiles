# Issue Breakdown

Break large GitHub issues into clear, actionable sub-issues using **issue types** (Epic, Task, Bug, Feature) with dependency order, scope boundaries, and hierarchy limits.

## When to Use This Skill

- Splitting a broad issue into implementation-ready, properly typed tasks
- Creating Epic → Feature → Task hierarchies for multi-step projects
- Using GitHub sub-issues and issue types for structured tracking
- Enforcing sub-issue hierarchy limits before creating links

## Installation

### Using gh-hubber-skills CLI (Recommended)

```bash
gh hubber-skills install issue-breakdown-skill
gh hubber-skills install issue-breakdown-skill --project
```

### Manual Installation

**Personal skills**:
```bash
cp -r issue-breakdown-skill ~/.copilot/skills/
```

**Project skills**:
```bash
cp -r issue-breakdown-skill /path/to/repo/.github/skills/
```

## Usage

This skill activates when you ask Copilot to:
- "break this issue into sub-issues"
- "split this work into actionable tasks"
- "create an epic with sub-issues"
- "plan this issue as GitHub sub-issues with types"

The skill will:
1. Discover available issue types and existing labels in the repository
2. Analyze scope and identify decomposition axes
3. Build a typed hierarchy (Epic → Feature/Task → Task/Bug) with appropriate labels
4. Validate GitHub limits (max 100 direct sub-issues, max depth 8)
5. Create issues with the correct type and labels, proposing new labels only with user approval

## Features

- **Issue-type-aware planning** — assigns Epic, Task, Bug, Feature (or custom types) to every issue
- **Smart labeling** — uses existing repo labels, proposes new ones only with user approval
- **Typed hierarchy trees** — Epics group Features and Tasks; Bugs are tracked where discovered
- **Actionable issue drafting** with acceptance criteria and test notes
- **Limit-aware decomposition** for GitHub sub-issue constraints
- **REST + GraphQL execution** — creates typed issues via REST API, links via GraphQL
- **Custom type discovery** — queries the org for available types before creating issues
- **Clarifying questions** when scope or split strategy is ambiguous

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Repository write access for creating and linking issues
- Sub-issues feature available in the target repository
- Issue types configured in the organization (defaults: Task, Bug, Feature; Epic may need to be added)
- **Note:** Issue types are not available in personal repositories — only organization repos support them

## Examples

- See [`examples/basic-usage.md`](./examples/basic-usage.md) for an end-to-end breakdown workflow.
- See [`references/github-sub-issues.md`](./references/github-sub-issues.md) for API and limit notes.
