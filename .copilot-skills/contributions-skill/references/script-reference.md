# Script Reference

## `scripts/fetch-details.py`

Purpose:

- Enrich PR and issue search results with detailed metadata
- Cache per-item fetches for resumable runs

Key outputs:

- `pr-details-authored.json`
- `pr-details-reviewed.json`
- `issue-details.json`

Important flags:

- `--skip-authored`
- `--skip-reviewed`
- `--skip-issues`
- `--username` to filter review comments to the current user

## `scripts/filter-reviewed-prs.py`

Purpose:

- Reduce review-requested PRs to the subset with meaningful human review activity

Key outputs:

- `prs-genuinely-reviewed.json`
- `prs-discarded.json`
- `prs-errors.json` when retries still fail

Signals counted as meaningful:

- `CHANGES_REQUESTED`
- non-boilerplate `COMMENTED`
- inline comments
- substantial issue comments on the PR

## `scripts/search-discussion-kudos.py`

Purpose:

- Search GitHub Discussions via GraphQL
- Detect kudos using keywords and emoji
- Collect authored discussions separately

Key outputs:

- `discussions-full.json`
- `kudos-found.json`
- `discussions-authored.json`

## Slack follow-up

This repo package intentionally does not bundle automated Slack tooling.

If a target environment already has approved Slack tooling, keep these rules:

- use a separate Slack workspace/domain value instead of assuming it matches the GitHub org
- use the Slack display name separately from the GitHub handle when self-filtering matters
- treat Slack as optional enrichment, not a hard requirement

## `scripts/test_performance.py`

Purpose:

- Validate rate-limit behavior
- Check concurrency assumptions
- Verify cache hits skip network calls
- Validate output shapes without live API calls

Run:

```bash
python3 scripts/test_performance.py
python3 scripts/test_performance.py -v
```
