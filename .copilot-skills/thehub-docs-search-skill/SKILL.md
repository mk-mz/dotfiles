---
name: thehub-docs-search
description: Use when searching GitHub internal documentation, company policies, engineering processes, HR guides, or any "how does GitHub do X" questions. Triggers on TheHub, internal docs, GitHub process, company policy.
---

# Searching GitHub Internal Documentation (TheHub)

GitHub's internal documentation lives in the `github/thehub` repository (5,000+ docs). Use GitHub MCP server tools to search and retrieve content. Prefer a local clone when available.

## When to Use

- Questions about GitHub company processes, policies, or guides
- "How do I do X at GitHub?" questions (expenses, travel, name changes, etc.)
- Engineering fundamentals, incident response, security policies
- HR, IT, or administrative procedures
- Any question that would be answered by internal documentation

## Local Clone Detection

Before using API calls, check if `github/thehub` is cloned locally. A local clone is faster, works offline, and avoids rate limits.

Check in order:
1. `THEHUB_LOCAL_PATH` environment variable
2. Sibling directory `../thehub`
3. Fall back to MCP tools (`search_code`, `get_file_contents`) if no local clone

```bash
if [ -n "${THEHUB_LOCAL_PATH:-}" ] && [ -d "$THEHUB_LOCAL_PATH/docs" ]; then
    THEHUB_ROOT="$THEHUB_LOCAL_PATH"
elif [ -d "../thehub/docs" ]; then
    THEHUB_ROOT="../thehub"
fi
```

When `THEHUB_ROOT` is set, prefer `grep -ri "TERM" "$THEHUB_ROOT/docs" --include='*.md' -l` and `cat` over API calls.

## Directory Structure

Representative areas (not exhaustive):

| Directory | Content | Subdirectories |
|-----------|---------|----------------|
| `docs/epd/engineering/` | Engineering practices, deployment, services | `deployment/`, `testing/`, `monitoring/`, `architecture/`, `tools/`, `fundamentals/`, `incident-response/`, `how-we-work/` |
| `docs/epd/product/` | Product development, design | `design/`, `pm-guides/`, `research/`, `processes/` |
| `docs/epd/data/` | Data engineering, analytics | `pipelines/`, `privacy/`, `analytics/`, `governance/` |
| `docs/security/` | Security policies, compliance, operations | `policies/`, `operations/`, `standards/` |
| `docs/guides/` | General guides (onboarding, tools, workflows) | `onboarding/`, `tools/`, `workflows/` |
| `docs/teams/` | Team-specific docs and runbooks | `[team-name]/` with `processes/`, `runbooks/`, `architecture/` |
| `docs/products/` | Product/service documentation | `[product-name]/` with `architecture/`, `operations/`, `api/` |
| `docs/news/` | Announcements, updates | `all-hands/`, `updates/`, `launches/` |
| `docs/hr/` | HR/People docs | |
| `docs/it/` | IT docs | |
| `docs/support/` | Support docs | |
| `docs/learning/` | Learning resources | |

## How to Search

**Step 1: Use `search_code` to find relevant files**
```
search_code query:"expense repo:github/thehub path:docs/"
```

**Step 2: Use `get_file_contents` to read specific docs**
```
get_file_contents owner:github repo:thehub path:docs/guides/expenses/index.md
```

**Search by directory when the topic maps to a known area:**
```
search_code query:"deployment repo:github/thehub path:docs/epd/engineering/"
```

## Frontmatter & Metadata

TheHub docs use Jekyll with YAML frontmatter. When reading a doc, extract and present:
- `title` -- document title
- `owner_team` -- team responsible for the doc
- `owner_slack` -- Slack channel for questions

## URL Mapping

File paths map to thehub URLs by dropping the `.md` extension:
```
docs/epd/engineering/deployment.md -> https://thehub.github.com/docs/epd/engineering/deployment
```
Always include the thehub.github.com link when presenting results.

## Presenting Results

Use this format when presenting docs to the user:

```
[Title from frontmatter]
https://thehub.github.com/docs/path/to/doc
Owner: [owner_team] ([owner_slack])

Key sections:
- [Section 1]
- [Section 2]

Summary: [2-3 sentence summary of the most relevant content]
```

Suggest related docs and contact channels when available.

## Example Searches

| Question | Search Strategy |
|----------|-----------------|
| Expense reports | `search_code` query:"expense repo:github/thehub path:docs/guides/" |
| Incident response | `search_code` query:"incident response repo:github/thehub path:docs/epd/engineering/" |
| Security policies | `search_code` query:"[topic] repo:github/thehub path:docs/security/" |
| Service tier requirements | `search_code` query:"service tier repo:github/thehub path:docs/epd/" |
| Deployment guides | `search_code` query:"deployment repo:github/thehub path:docs/epd/engineering/" |
| Team runbooks | Browse `docs/teams/[team-name]/runbooks/` |

## Error Handling

| Situation | Action |
|-----------|--------|
| No results found | Try broader terms, different keywords, or browse the directory structure |
| Cannot access github/thehub | User may lack Hubber access. Suggest contacting #github-help |
| Rate limit warnings | Use local clone, wait, or use more specific searches |
| Doc not found at path | Doc may have moved or been renamed. Search by content instead |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Guessing answers about GitHub processes | Always search thehub first |
| Searching public docs.github.com | Internal docs are in github/thehub repo |
| Not including thehub.github.com links | Always provide the URL so the user can read the full doc |
| Dumping full doc content without summary | Extract key sections and summarize |
