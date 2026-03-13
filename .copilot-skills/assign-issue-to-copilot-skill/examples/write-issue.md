# Example: Write a Copilot-Ready Issue

Create an issue that Copilot can understand and implement effectively.

## Scenario

You want Copilot to implement rate limiting for an API endpoint, but you need to write the issue first. The issue should be detailed enough for Copilot to complete the work autonomously.

## User Request

> "Write an issue for Copilot to add rate limiting to the /api/users endpoint"

## Agent Response: Creating the Issue

````bash
# Creating a well-structured issue for Copilot

gh issue create \
  --title "Add rate limiting to /api/users endpoint" \
  --body "$(cat <<'EOF'
## Problem

The `/api/users` endpoint currently has no rate limiting, which could lead to:
- API abuse and DoS attacks
- Performance degradation under high load
- Excessive resource consumption

## Proposed Solution

Implement rate limiting using the existing `express-rate-limit` middleware that's already configured in the project.

**Configuration:**
- Limit: 100 requests per minute per IP address
- Window: 60 seconds (sliding window)
- Response: 429 Too Many Requests with Retry-After header
- Storage: Use existing Redis instance for distributed rate limiting

## Files to Modify

- `src/api/routes/users.js` - Apply rate limiter middleware to the endpoint
- `src/middleware/rateLimiter.js` - Add configuration for users endpoint (if needed)
- `tests/api/users.test.js` - Add rate limiting tests
- `docs/api.md` - Document the rate limit

## Acceptance Criteria

- [ ] Rate limiter applied to `GET /api/users` endpoint
- [ ] Rate limiter applied to `POST /api/users` endpoint  
- [ ] Returns 429 status code when limit exceeded
- [ ] Includes `Retry-After` header in 429 responses
- [ ] Uses Redis for distributed rate limiting (multi-instance support)
- [ ] All existing tests still pass
- [ ] New tests added for rate limiting behavior

## Test Cases to Add

```javascript
describe('Rate Limiting', () => {
  it('should allow requests under the limit', async () => {
    // Make 50 requests - all should succeed
  });
  
  it('should return 429 when limit exceeded', async () => {
    // Make 101 requests - last one should fail with 429
  });
  
  it('should include Retry-After header in 429 response', async () => {
    // Verify header is present and has correct value
  });
  
  it('should reset limit after window expires', async () => {
    // Verify limit resets after 60 seconds
  });
});
```

## Implementation Notes

- The project already has `express-rate-limit` installed (v6.7.0)
- Redis connection is configured in `src/config/redis.js`
- Other endpoints use rate limiting - see `src/api/routes/auth.js` for reference
- Follow the same pattern as the auth endpoints for consistency

## Related Documentation

- Express Rate Limit docs: https://github.com/express-rate-limit/express-rate-limit
- Redis Rate Limiter: https://github.com/express-rate-limit/rate-limit-redis
- Internal rate limiting standards: /docs/rate-limiting-standards.md

## Testing

Run these commands after implementation:

```bash
# Run tests
npm test -- users.test.js

# Test manually with curl
for i in {1..101}; do
  curl -i http://localhost:3000/api/users
done

# Should see 429 on request 101
```

## Success Criteria

Implementation is complete when:
1. All automated tests pass
2. Manual testing confirms 429 responses after 100 requests
3. Retry-After header is present
4. Documentation is updated
5. Code review approved
EOF
)" \
  --label "enhancement,ready-for-copilot"
````

## Created Issue

```
✅ Created issue #456
https://github.com/owner/repo/issues/456

Title: Add rate limiting to /api/users endpoint
Labels: enhancement, ready-for-copilot
State: OPEN

The issue includes:
✅ Clear problem statement
✅ Specific solution approach
✅ Exact file paths to modify
✅ Detailed acceptance criteria
✅ Test cases to implement
✅ Implementation notes with context
✅ Links to relevant documentation
✅ Manual testing instructions

This issue is ready for Copilot to pick up!

Next step: Assign Copilot to this issue?
```

## Assign Copilot

**User Response:**
> "Yes, assign Copilot"

**Agent Response:**
```bash
gh issue edit 456 --add-assignee @copilot
```

```
🤖 Assigning Copilot to issue #456...

✅ Copilot assigned!

Expected timeline:
• 0-2 min: Copilot analyzes the issue
• 2-10 min: Implementation and testing
• 10+ min: PR opened

I'll monitor progress and notify you when the PR is ready.
```

## Alternative: Simpler Issue (Smaller Change)

For smaller changes, a simpler issue format works well:

````bash
gh issue create \
  --title "Fix typo in user.js documentation" \
  --body "$(cat <<'EOF'
## Problem
There's a typo in `src/models/user.js` line 45: "recieve" should be "receive"

## Solution
Change line 45 from:
```javascript
// recieve user data from database
```

to:
```javascript
// receive user data from database
```

## Acceptance Criteria
- [ ] Typo fixed in `src/models/user.js` line 45
- [ ] No other changes needed

## Files to Modify
- `src/models/user.js` (line 45)
EOF
)" \
  --assignee @copilot
````

```
✅ Created and assigned issue #457
https://github.com/owner/repo/issues/457

This simple issue should be completed by Copilot in 1-2 minutes.
```

## Template Comparison

### ✅ Good Issue (Detailed Feature)

```markdown
## Problem
[Clear description with impact/motivation]

## Proposed Solution  
[Specific approach with configuration details]

## Files to Modify
- `exact/path/to/file.js` - [what to change]

## Acceptance Criteria
- [ ] [Specific requirement]
- [ ] All tests pass
- [ ] Tests added

## Test Cases
[Specific test descriptions or code]

## Implementation Notes
[Context, existing patterns, gotchas]

## Related Documentation
[Links to relevant docs]
```

### ❌ Bad Issue (Too Vague)

```markdown
## Problem
The API needs rate limiting

## Solution
Add rate limiting

## Acceptance Criteria
- [ ] Rate limiting works
```

**Why it's bad:**
- No specific endpoint mentioned
- No configuration details
- No file paths
- No test expectations
- No context about existing patterns

## Issue Quality Checklist

Before assigning to Copilot, verify:

**Required Elements:**
- [ ] Clear, specific title
- [ ] Problem statement with motivation
- [ ] Proposed solution or approach
- [ ] Specific file paths (when applicable)
- [ ] Acceptance criteria (checkbox list)
- [ ] Testing requirements

**Recommended Elements:**
- [ ] Implementation notes and context
- [ ] Links to related documentation
- [ ] Example code or test cases
- [ ] References to similar patterns in codebase
- [ ] Manual testing instructions

**Optional but Helpful:**
- [ ] Screenshots or diagrams
- [ ] Performance considerations
- [ ] Security considerations
- [ ] Backward compatibility notes

## Best Practices for Different Issue Types

### Bug Fix Issue

```markdown
## Problem
Login fails with error "Invalid token" when user has special characters in username.

## Steps to Reproduce
1. Create user with username `user@test.com`
2. Attempt to login
3. See error: "Invalid token"

## Expected Behavior
Login should succeed regardless of special characters in username.

## Root Cause
Token generation in `src/auth/tokenGenerator.js` doesn't properly encode special characters.

## Proposed Fix
Use `encodeURIComponent()` when generating tokens in `src/auth/tokenGenerator.js` line 34.

## Files to Modify
- `src/auth/tokenGenerator.js` (line 34)
- `tests/auth/tokenGenerator.test.js` (add test case)

## Acceptance Criteria
- [ ] Login succeeds with special characters in username
- [ ] Test added for usernames with @, +, ., and other special chars
- [ ] All existing auth tests pass
```

### Documentation Issue

```markdown
## Problem
The API documentation for `/api/users` endpoint is missing request/response examples.

## Proposed Solution
Add comprehensive examples to `docs/api/users.md` showing:
- List users request/response
- Create user request/response
- Error responses (400, 404, 500)

## Files to Modify
- `docs/api/users.md` (add examples section)

## Acceptance Criteria
- [ ] Examples added for all endpoints
- [ ] Shows request format (headers, body)
- [ ] Shows response format (status, headers, body)
- [ ] Includes error examples

## Example Format
Follow the format used in `docs/api/auth.md` for consistency.
```

### Refactoring Issue

```markdown
## Problem
The `UserController.js` has grown to 800 lines and handles too many responsibilities, making it hard to maintain.

## Proposed Solution
Extract user validation logic into a separate `UserValidator.js` class.

## Files to Create
- `src/validators/UserValidator.js` - New validator class

## Files to Modify
- `src/controllers/UserController.js` - Remove validation, use UserValidator
- `tests/controllers/UserController.test.js` - Update to use validator
- `tests/validators/UserValidator.test.js` - New test file

## Acceptance Criteria
- [ ] UserValidator class created with all validation methods
- [ ] UserController uses UserValidator for all validations
- [ ] All existing tests pass
- [ ] New tests for UserValidator
- [ ] No change in API behavior (internal refactor only)

## Validation Methods to Extract
- `validateEmail()`
- `validatePassword()`
- `validateUsername()`
- `validateAge()`

See lines 234-456 in UserController.js
```

## Notes

- **Issue Length:** Detailed issues (100-300 lines) work best for complex features
- **Simple Changes:** Brief issues (20-50 lines) are fine for typos, small fixes
- **Code Examples:** Including code snippets helps Copilot understand expectations
- **Links:** Reference existing code patterns in the same repo
- **Tests:** Always specify what tests to add - this ensures quality
