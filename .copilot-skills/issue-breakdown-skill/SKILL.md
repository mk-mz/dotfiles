---
name: issue-breakdown
description: This skill should be used when the user asks to "break this issue down", "split this work into tasks", "create sub-issues", "plan a sub-issue hierarchy", or needs large GitHub issues decomposed into actionable, limit-safe sub-issues.
---

# Issue Breakdown - Plan and Build Sub-Issue Trees

Decompose large work items into implementable GitHub issues and sub-issues using **issue types** (Epic, Task, Bug, Feature, etc.) with clear hierarchy, ordering, and acceptance criteria.

## When to Use This Skill

- A single issue is too large to execute safely
- Work requires explicit sequencing or dependency mapping
- User wants GitHub-native tracking through sub-issues
- The task needs a hierarchy while respecting platform limits
- Work should be categorized with issue types for filtering, reporting, and project views
- Issues need consistent labeling for cross-cutting concerns (priority, area, team, etc.)

## Issue Types

GitHub issue types provide structured classification at the organization level. Always assign an appropriate type to every issue created during a breakdown.

> **Note:** Issue types are only available in **organization repositories**. Personal (user-owned) repositories do not support issue types. If working in a personal repo, skip the type assignment steps and rely on labels for classification instead.

### Common Types

| Type | When to Use | Default? |
|------|-------------|----------|
| **Task** | A discrete, actionable unit of work. Most leaf-level sub-issues should be Tasks. | ✅ Yes |
| **Bug** | A defect, regression, or unexpected behavior discovered during planning or execution. | ✅ Yes |
| **Feature** | New user-facing capability or significant enhancement. Use when a sub-issue delivers something a user can interact with. | ✅ Yes |
| **Epic** | Large initiative spanning multiple workstreams. Use as the top-level parent that groups related Tasks, Bugs, and Features. | ❌ Custom — must be created by an org admin |

### Type Selection Rules

1. **Top-level parent** → Epic (unless the parent is itself a child of a larger Epic, in which case use Feature or Task).
2. **Workstream groupings** (L1 children of an Epic) → Feature if they deliver user-facing value; Task if they are internal/infrastructure.
3. **Leaf-level work items** → Task for implementation work, Bug for defect fixes.
4. **Mixed trees** are expected — an Epic can contain Features, Tasks, and Bugs as children at any level.
5. If the organization has **custom types** (e.g., Research, Documentation, Security), prefer those when they match the work more precisely than the defaults.
6. Only **one type per issue** — do not combine types. Use labels for secondary classification.

### Discovering Available Types

Before creating issues, check what types are available in the target organization:

```bash
# List issue types for the organization
gh api /orgs/{org}/issue-types
```

If custom types exist, incorporate them into the breakdown where appropriate.

## Labels

Labels provide secondary classification that complements issue types. While a type defines *what kind* of work an issue is, labels capture cross-cutting concerns like priority, area, team ownership, and status.

### Label Strategy

1. **Prefer existing labels.** Before assigning labels, always fetch the repository's current labels:

```bash
# List all labels in the repo
gh label list --json name,description --limit 200
```

2. **Match by intent, not exact name.** If the repo has `priority/high` instead of `P1`, use the existing convention.
3. **Ask before creating new labels.** If a useful label doesn't exist, propose it to the user and only create it after confirmation:

```bash
# Create a new label (only after user approval)
gh label create "area/auth" --description "Authentication and authorization" --color "0075ca"
```

4. **Apply labels consistently** across all issues in a breakdown. If the parent Epic gets `area/auth`, all children in that workstream should too.

### Common Label Categories

| Category | Examples | When to Apply |
|----------|----------|---------------|
| **Area/Component** | `area/auth`, `area/api`, `frontend` | Group by code area or domain |
| **Priority** | `priority/high`, `P1`, `urgent` | When the user specifies or implies priority |
| **Team** | `team/platform`, `team/security` | When ownership is clear |
| **Size/Effort** | `size/S`, `size/M`, `size/L` | When estimating scope |
| **Status** | `blocked`, `needs-design`, `ready` | When workflow state matters |
| **Tracking** | `epic/checkout-migration`, `sprint-42` | When linking to a broader initiative |

### Label Rules

1. Only apply labels that **already exist** in the repository unless the user approves creating new ones.
2. When proposing new labels, include a name, description, and color suggestion.
3. Batch label proposals — present all new labels at once rather than asking one at a time.
4. Do not duplicate what issue types already convey (e.g., don't add a `bug` label to a Bug-typed issue).

## Core Constraints (Always Enforce)

1. **Maximum direct sub-issues per parent: 100**
2. **Maximum hierarchy depth: 8 levels**
3. **Every issue must have a type assigned.**
4. Validate limits **before** creating or linking issues.
5. If limits are exceeded, propose and apply a split strategy (for example, additional parent buckets).

## Process

### Step 1: Clarify Scope and Decomposition Axes

Collect:
- desired outcome
- in/out of scope
- constraints (risk, rollout, testing)
- preferred grouping strategy (by layer, feature area, milestone, or dependency chain)
- relevant issue types available in the organization (query with `gh api /orgs/{org}/issue-types`)
- existing repository labels (query with `gh label list`)

If the split is ambiguous, ask targeted questions before generating issues.

### Step 2: Build a Typed Task Tree Draft

Create a draft hierarchy, assigning a type and labels to every node:

```text
Epic #parent: "Migrate checkout service to new auth SDK" [area/auth, priority/high]
├── Feature #A: "SDK integration layer" [area/auth]
│   ├── Task #A1: "Bootstrap SDK configuration" [area/auth]
│   ├── Task #A2: "Token validation middleware" [area/auth]
│   └── Bug #A3: "Fix legacy token edge case" [area/auth]
├── Feature #B: "API contract updates" [area/api, area/auth]
│   ├── Task #B1: "Update endpoint schemas" [area/api]
│   └── Task #B2: "Input validation hardening" [area/api]
└── Task #C: "Integration tests and rollout guardrails" [area/auth]
```

Each leaf issue must include:
- concrete objective
- completion criteria
- validation/test expectation
- assigned issue type
- relevant labels (from existing repo labels)

### Step 3: Validate Limit Safety

Run checks on the draft:
- direct children count for each parent <= 100
- depth for every node <= 8
- every node has exactly one issue type assigned
- all labels used in the draft exist in the repository (if not, batch-propose new labels to the user)

If invalid:
1. stop issue creation
2. explain exactly which node violates limits
3. propose a rebalance plan
4. continue only after user confirmation (or after auto-rebalance if user already requested autonomous execution)

### Step 4: Draft Issue Bodies

Use this template for each child issue:

```markdown
## Goal
[What this issue delivers]

## Scope
- In: [...]
- Out: [...]

## Acceptance Criteria
- [ ] ...
- [ ] ...

## Dependencies
- Parent: #[parent]
- Blocks: #[optional]

## Validation
[How to verify completion]
```

### Step 5: Create and Link Issues via GitHub APIs

Preferred flow:

1. **Create any approved new labels** before creating issues:

```bash
# Create new labels (only after user confirmation)
gh label create "area/auth" --description "Authentication and authorization" --color "0075ca"
```

2. **Create issues with type and labels** using the REST API (the `gh issue create` CLI does not yet support the `--type` flag):

```bash
# Create an issue with a type and labels via REST API
gh api repos/{owner}/{repo}/issues \
  --method POST \
  -f title="SDK bootstrap and configuration" \
  -f body="$(cat /tmp/issue.md)" \
  -f type="Task" \
  -f 'labels[][name]=area/auth' \
  -f 'labels[][name]=priority/high'
```

Alternatively, use `gh issue create` with `--label` for issues that don't need a type set at creation time, or set the type in a follow-up PATCH:

```bash
gh issue create --title "..." --body-file /tmp/issue.md --label "area/auth" --label "priority/high"
```

3. **Set or update the type on an existing issue** via REST API:

```bash
# Update an existing issue's type
gh api repos/{owner}/{repo}/issues/{number} \
  --method PATCH \
  -f type="Epic"
```

4. **Fetch node IDs** for sub-issue linking:

```bash
gh issue view 123 --json id,number,title,url
```

5. **Link parent/child relations** through GraphQL sub-issue mutations:

```bash
gh api graphql -f query='mutation($parent:ID!,$child:ID!){ addSubIssue(input:{issueId:$parent,subIssueId:$child}){ issue{ id } } }' -F parent=... -F child=...
```

### Step 6: Return a Structured Plan Summary

Always return:
- tree overview with **types**, depth, and child counts
- created issue numbers/URLs
- unresolved questions or blocked nodes
- next execution order

## Output Format

```text
Issue Breakdown Plan
Parent: #123 (Epic) [area/auth, priority/high]

Hierarchy:
- L1 #124 [Feature] Auth foundation (children: 3) [area/auth]
  - L2 #126 [Task] Bootstrap SDK config [area/auth]
  - L2 #127 [Task] Token validation middleware [area/auth]
  - L2 #128 [Bug] Fix legacy token edge case [area/auth]
- L1 #125 [Feature] API hardening (children: 2) [area/api]
  - L2 #130 [Task] Rate limits [area/api]
  - L2 #131 [Task] Input validation [area/api]
- L1 #129 [Task] Integration tests & rollout [area/auth]

Labels:
- Existing: area/auth, area/api, priority/high ✅
- Created: (none)

Limit Checks:
- Max direct children: PASS (largest=3, limit=100)
- Max depth: PASS (actual=2, limit=8)
- Type coverage: PASS (all issues typed)

Execution Order:
1) #126, #127
2) #128
3) #130, #131
4) #129
```

## Error Handling

### Limit Violation
- **Symptom:** Planned tree exceeds 100 direct children or depth > 8
- **Action:** Halt linking, report offending node, propose rebalance structure

### Missing Permissions
- **Symptom:** `gh api` returns permission/authorization errors
- **Action:** Surface exact command failure and required permissions; do not silently skip

### API/Schema Mismatch
- **Symptom:** GraphQL mutation for sub-issues is rejected, or `type` field is not accepted on REST create
- **Action:** Show response payload, fall back to draft-only output, and ask user whether to continue with manual linking/typing

### Issue Type Not Found
- **Symptom:** REST API rejects the `type` value (e.g., custom type not configured in the organization)
- **Action:** List available types with `gh api /orgs/{org}/issue-types`, suggest the closest match, and ask user to confirm

## Boundaries

**Will:**
- Break large issues into actionable, **typed** sub-issues
- Assign appropriate issue types (Epic, Task, Bug, Feature, or custom) to every issue
- Apply existing repository labels for cross-cutting concerns (area, priority, team, etc.)
- Propose new labels when needed and **ask before creating them**
- Enforce GitHub hierarchy limits
- Ask focused clarification questions when needed
- Use GitHub APIs/CLI to create, type, label, and link issues when authorized

**Will Not:**
- Create issues without an assigned type
- Create new labels without user approval
- Create invalid hierarchies that violate platform limits
- Invent dependencies without stating assumptions
- Hide API failures or proceed with partial silent failure

## Quick Reference

```bash
# List available issue types for the org
gh api /orgs/{org}/issue-types

# List existing labels in the repo
gh label list --json name,description --limit 200

# Create a new label (only after user approval)
gh label create "area/auth" --description "Authentication and authorization" --color "0075ca"

# Create an issue with a type and labels (REST API)
gh api repos/{owner}/{repo}/issues \
  --method POST \
  -f title="..." \
  -f body="$(cat /tmp/issue.md)" \
  -f type="Task" \
  -f 'labels[][name]=area/auth'

# Or use gh issue create with labels (type set separately)
gh issue create --title "..." --body-file /tmp/issue.md --label "area/auth" --label "priority/high"

# Set type on an existing issue
gh api repos/{owner}/{repo}/issues/{number} \
  --method PATCH \
  -f type="Epic"

# Read issue ID and metadata
gh issue view 123 --json id,number,title,url

# Link parent/child (sub-issue)
gh api graphql -f query='mutation($parent:ID!,$child:ID!){ addSubIssue(input:{issueId:$parent,subIssueId:$child}){ issue{ id } } }' -F parent=... -F child=...
```
