# Issue Breakdown Skill Tests

Tests that the skill enforces platform limits, assigns types, and respects label governance.

---

## Test: Enforces Sub-Issue Limits

**Prompt:**
```
I need to break down this epic into about 150 tasks. Can you create sub-issues for all of them under the parent issue?
```

**Expected Behavior:**
The response should flag that 150 direct children exceeds the 100 sub-issue limit.
It should propose a rebalancing strategy (e.g., grouping into intermediate Feature or Task parents).
It should NOT silently create 150 sub-issues or ignore the limit.

---

## Test: Assigns Issue Types to Every Issue

**Prompt:**
```
Break down this issue into sub-issues:

We need to migrate the checkout service to the new auth SDK. This involves updating the SDK config, adding token validation, updating API schemas, and writing integration tests.
```

**Expected Behavior:**
Every issue in the proposed breakdown should have an explicit type assigned (Epic, Feature, Task, Bug, or a custom type).
The top-level parent should be typed as Epic (or Feature if it's a child of a larger initiative).
Leaf-level work items should be typed as Task.
The response should NOT create any issue without a type.

---

## Test: Asks Before Creating Labels

**Prompt:**
```
Break this work into sub-issues and label them with priority and area tags.
```

**Expected Behavior:**
The response should first check existing repository labels (via `gh label list` or equivalent).
If the requested labels don't exist, it should propose new labels and ask for confirmation before creating them.
It should NOT create new labels without user approval.
It should prefer matching existing label conventions (e.g., use `priority/high` if that's what the repo uses, not `P1`).
