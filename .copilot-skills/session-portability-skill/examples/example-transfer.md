# Example: Session Portability

## Scenario 1: Transfer a Local Session to a Codespace

### User Request

> "Transfer my current session to my Codespace"

### Agent Response

The agent gathers context from the current session and generates a handoff prompt:

```
I'll prepare a handoff prompt so you can continue this work in your Codespace.

1. Gathering session context...
   Branch: feature/add-auth-middleware
   Repo: github/my-app
   Last commit: a1b2c3d (Add JWT validation middleware)

2. Reading session plan...
   Found plan.md with 3 completed and 2 remaining tasks.

3. Checking for uncommitted changes...
   Modified: src/middleware/auth.ts, src/routes/api.ts

4. ⚠️  Security note: Please review the handoff prompt below before sharing
   it outside your own environments. It may contain file paths or task
   descriptions that reference internal systems.

5. Generating handoff prompt...

---

# Session Handoff

## Repository & Branch
- **Repo:** github/my-app
- **Branch:** feature/add-auth-middleware
- **Last commit:** a1b2c3d Add JWT validation middleware

## What Was Being Worked On
Adding JWT-based authentication middleware to the API routes. The middleware
validates tokens, extracts user claims, and attaches them to the request context.

## Current Progress

### Completed
- Created JWT validation middleware in `src/middleware/auth.ts`
- Added token refresh endpoint in `src/routes/auth.ts`
- Wrote unit tests for token validation

### In Progress
- Integrating middleware with existing API routes (`src/routes/api.ts`)
  — need to add `requireAuth()` to protected endpoints

### Not Started
- End-to-end tests for auth flow

## Uncommitted Changes
 src/middleware/auth.ts | 12 ++++++------
 src/routes/api.ts      |  8 ++++++++
 2 files changed, 14 insertions(+), 6 deletions(-)

## Key Files
- `src/middleware/auth.ts` — JWT validation middleware
- `src/routes/auth.ts` — Token refresh endpoint
- `src/routes/api.ts` — API routes (being updated)
- `tests/middleware/auth.test.ts` — Unit tests

## Next Steps
1. Finish adding `requireAuth()` to protected endpoints in `src/routes/api.ts`
2. Write end-to-end tests for the full auth flow
3. Update API documentation

## Notes
- Using `jsonwebtoken` library for JWT operations
- Token expiry is set to 1 hour, refresh tokens to 7 days
- Decision: chose middleware pattern over decorator pattern for Express compatibility

---

6. ✅ Handoff prompt ready!

To continue in your Codespace:

   a. Push your branch:
      $ git add -A && git commit -m "WIP: auth middleware integration"
      $ git push origin feature/add-auth-middleware

   b. Open your Codespace and run:
      $ cd /workspaces/my-app
      $ git checkout feature/add-auth-middleware
      $ git pull origin feature/add-auth-middleware
      $ copilot

   c. Paste the handoff prompt above into the new session.

   💡 Tip: Use /share to create a gist backup of this conversation first.
```

### Outcome

The user pushes their branch, opens the Codespace, starts a new `copilot` session, and pastes the handoff prompt. The new session has full context of what was done and what remains.

---

## Scenario 2: Conversation Backup with `/share`

### User Request

> "I want a full backup of this conversation before switching to my Codespace"

### Agent Response

```
Good idea! Here's how to create a full conversation backup:

1. Use /share to create a gist of this conversation.
   This captures the complete conversation history as a reference.

2. ⚠️  Note: /share creates a secret (unlisted) gist. Anyone with the URL
   can view it. Review the conversation for sensitive content first.

3. After creating the gist, I'll also generate a handoff prompt for you.
   The handoff prompt is a concise summary — the gist is the full record.

You can include the gist URL in the handoff prompt so the agent in the
new session can reference it if needed.
```

### Outcome

The user gets both a full conversation backup (via gist) and a concise handoff prompt for the new session.

---

## Scenario 3: Handoff with Uncommitted Changes

### User Request

> "Transfer my session to Codespace — I have uncommitted changes I don't want to lose"

### Agent Response

```
I see you have uncommitted changes. Let's make sure nothing is lost.

1. Checking uncommitted changes...
   Modified: src/api/handler.go (not staged)
   New file: src/api/handler_test.go (not staged)

2. Options for preserving your changes:

   Option A — Commit as WIP (recommended):
      $ git add -A
      $ git commit -m "WIP: API handler implementation"
      $ git push origin feature/api-handler

   Option B — Create a patch file and share via gist:
      $ git diff > /tmp/session-changes.patch
      $ gh gist create /tmp/session-changes.patch
      Apply in the Codespace by streaming the patch content to git:
      $ gh gist view <gist-id> --raw | git apply

3. I'll include the uncommitted changes in the handoff prompt so the new
   session knows about them regardless of which option you choose.

Which option would you prefer?
```

### Outcome

The user's uncommitted changes are preserved through either a WIP commit or a patch file, and the handoff prompt documents what was changed.
