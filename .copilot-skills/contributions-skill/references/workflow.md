# Workflow Reference

This skill follows a staged workflow so data collection and synthesis stay predictable.

## Phase 1 - Search

- Search authored PRs
- Search review-requested PRs
- Search authored / assigned / mentioned issues
- Deduplicate by `repo + number`

## Phase 2 - Review Filtering

Use `scripts/filter-reviewed-prs.py` to keep only meaningful review activity:

- changes requested
- substantial review comments
- inline review comments
- meaningful issue comments on a PR

Boilerplate approvals such as `LGTM` should not count as meaningful review work on their own.

## Phase 3 - GitHub Discussions

Use `scripts/search-discussion-kudos.py` to collect:

- discussions that mention the user
- comments that contain kudos-like language or emoji
- discussions authored by the user

## Phase 4 - Slack (Optional)

This packaged skill does not bundle automated Slack tooling. If a target environment already has approved Slack tooling, it can optionally gather:

- participated threads
- mentions by others
- kudos-like Slack messages

Slack should be treated as optional data, not a hard dependency.

## Phase 5 - Detail Enrichment

Use `scripts/fetch-details.py` to fetch:

- PR body, merge status, labels, changed files, additions, deletions
- the user's own inline review comments
- issue body and comments

The script caches individual items under `phase5/cache/` so interrupted runs can resume efficiently.

## Phase 6 - Narrative Synthesis

The final write-up should emphasize:

- impact and outcomes
- scope and ownership
- technical leadership in reviews
- recognition and collaboration

Avoid producing a summary that is only counts and raw metrics.
