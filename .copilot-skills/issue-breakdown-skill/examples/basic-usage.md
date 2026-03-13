# Example: Break a Platform Migration Issue into Typed Sub-Issues

## Scenario

A parent issue tracks "Migrate checkout service to new auth SDK."  
The work is too large for one PR and needs GitHub sub-issues with proper issue types and dependency order.

## User Request

> "Break issue #450 into sub-issues and create the hierarchy."

## Agent Response (Abbreviated)

```text
I'll check the available issue types for your org, then decompose #450 by workstream
(SDK integration, API updates, rollout/test) and assign appropriate types to each issue.
```

### 1) Discover available types

```bash
gh api /orgs/acme-corp/issue-types
# Returns: Epic, Task, Bug, Feature (defaults)
```

### 2) Proposed typed hierarchy

> **Note:** Issue numbers below (e.g., #451) are illustrative — actual numbers are assigned by GitHub at creation time.

```text
Epic #450: Migrate checkout service to new auth SDK [area/auth, priority/high]
├── Feature: SDK integration layer [area/auth]
│   ├── Task: Bootstrap SDK configuration [area/auth]
│   ├── Task: Token validation middleware migration [area/auth]
│   └── Bug: Fix legacy token refresh edge case [area/auth]
├── Feature: Auth-related endpoint contract updates [area/api, area/auth]
│   ├── Task: Update endpoint schemas [area/api]
│   └── Task: Input validation hardening [area/api]
└── Task: Integration tests and rollout guardrails [area/auth, testing]
```

### 3) Limit checks

- Direct children on #450: 3 (<= 100) ✅
- Max depth: 2 (<= 8) ✅
- Type coverage: all issues typed ✅
- Labels: `area/auth`, `area/api` exist ✅; `testing` not found — proposed to user ✅

### 4) Execution order

1. SDK bootstrap (Task)
2. Token middleware migration (Task)
3. Legacy token bug fix (Bug — can parallel with step 2)
4. Endpoint schema + validation updates (Tasks)
5. Integration tests & rollout (Task — last)

### 5) Commands used

```bash
# Check existing labels
gh label list --json name,description --limit 200
# Found: area/auth, area/api, priority/high
# Not found: testing — user approved creation

# Create approved new label
gh label create "testing" --description "Test-related work" --color "bfd4f2"

# Set the parent issue to Epic type
gh api repos/acme-corp/checkout-svc/issues/450 \
  --method PATCH -f type="Epic"

# Create typed and labeled child issues via REST API
# (capture the returned issue number from each response for linking)
gh api repos/acme-corp/checkout-svc/issues \
  --method POST \
  -f title="SDK integration layer" \
  -f body="$(cat /tmp/sdk-integration.md)" \
  -f type="Feature" \
  -f 'labels[][name]=area/auth'

gh api repos/acme-corp/checkout-svc/issues \
  --method POST \
  -f title="Bootstrap SDK configuration" \
  -f body="$(cat /tmp/sdk-bootstrap.md)" \
  -f type="Task" \
  -f 'labels[][name]=area/auth'

gh api repos/acme-corp/checkout-svc/issues \
  --method POST \
  -f title="Fix legacy token refresh edge case" \
  -f body="$(cat /tmp/token-bug.md)" \
  -f type="Bug" \
  -f 'labels[][name]=area/auth'

# Fetch node IDs for sub-issue linking (use the issue numbers returned by the POST responses above)
gh issue view 450 --json id,number,title,url
gh issue view <created-issue-number> --json id,number,title,url

# Link parent/child via GraphQL
gh api graphql -f query='mutation($parent:ID!,$child:ID!){
  addSubIssue(input:{issueId:$parent,subIssueId:$child}){ issue{ id } }
}' -F parent=<parent-node-id> -F child=<child-node-id>
```

## Outcome

The large issue is transformed into a limit-safe, **typed and labeled** sub-issue plan:
- **Epic** at the top for the overall initiative
- **Features** for user-facing workstreams
- **Tasks** for implementation work
- **Bug** for the discovered defect
- **Labels** applied consistently from existing repo labels, with one new label (`testing`) created after user approval

Each issue has concrete acceptance criteria, a clear type, relevant labels, and defined dependency order.
