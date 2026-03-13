# GitHub Sub-Issues and Issue Types Reference Notes

## Hard Limits

- Maximum direct sub-issues per parent: **100**
- Maximum nesting depth: **8**
- Maximum issue types per organization: **25**
- Only **one type per issue**

Always validate these limits before creating parent/child links.

## Issue Types

### Default Types

Organizations include three default types: **Task**, **Bug**, and **Feature**. These can be edited, disabled, or deleted by org admins.

**Epic** is commonly added as a custom type to represent large initiatives that contain multiple Features and Tasks.

> **Important:** Issue types are an **organization-only feature**. Personal (user-owned) repositories do not support issue types. When working in a personal repo, use labels for classification instead.

### Type Hierarchy Pattern

```text
Epic          → Large initiative spanning multiple workstreams
├── Feature   → User-facing capability or significant enhancement
│   ├── Task  → Discrete implementation work
│   └── Bug   → Defect discovered during planning or execution
└── Task      → Infrastructure or internal work
```

### Querying Available Types

```bash
# List all issue types for an organization
gh api /orgs/{org}/issue-types
```

## Recommended API Workflow

1. **Discover types** — `gh api /orgs/{org}/issue-types`
2. **Create issues with type** (REST API):
   ```bash
   gh api repos/{owner}/{repo}/issues \
     --method POST \
     -f title="..." \
     -f body="$(cat /tmp/issue.md)" \
     -f type="Task"
   ```
3. **Set or update type on existing issues** (REST API):
   ```bash
   gh api repos/{owner}/{repo}/issues/{number} \
     --method PATCH \
     -f type="Epic"
   ```
4. **Fetch issue node IDs** — `gh issue view N --json id,number,url`
5. **Link issues as parent/child** via GraphQL:
   ```bash
   gh api graphql -f query='mutation($parent:ID!,$child:ID!){
     addSubIssue(input:{issueId:$parent,subIssueId:$child}){ issue{ id } }
   }' -F parent=... -F child=...
   ```
6. **Re-query and verify** resulting hierarchy shape

## Validation Checklist

- [ ] No parent has >100 direct children
- [ ] No branch exceeds depth 8
- [ ] Every issue has exactly one type assigned
- [ ] Type matches the nature of the work (Epic for initiatives, Feature for user-facing, Task for implementation, Bug for defects)
- [ ] All labels used exist in the repository (or were created after user approval)
- [ ] Labels are applied consistently across related issues
- [ ] No labels duplicate what the issue type already conveys
- [ ] Each issue has clear acceptance criteria
- [ ] Execution order is defined and dependency-safe
- [ ] API responses were checked for errors before proceeding

## Split Strategies When Limits Are Exceeded

- Introduce intermediate Epic or Feature parent issues for large fan-out
- Re-group by milestone, layer, or domain to reduce direct children
- Keep leaves actionable; avoid oversized child issues

## Issue Type CLI / API Notes

- `gh issue create` does **not** support a `--type` flag as of this writing — use the REST API instead
- `gh issue create` **does** support `--label` for applying labels at creation time
- The REST API accepts a `type` string field on both POST (create) and PATCH (update) for issues
- The REST API accepts a `labels` array field on both POST and PATCH for issues
- Organization-level endpoints exist to manage type definitions: `GET/POST/PATCH/DELETE /orgs/{org}/issue-types`
- Issue types are visible in project views and can be used for filtering (`type:Bug`, `type:Task`, etc.)
- Labels can be listed with `gh label list`, created with `gh label create`, and filtered in search (`label:area/auth`)
