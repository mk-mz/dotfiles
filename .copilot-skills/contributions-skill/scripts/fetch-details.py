#!/usr/bin/env python3
"""
Fetch detailed content for all PRs and issues.

Uses urllib.request directly to bypass shell hook output interception.
Fetches PR details (body, additions, deletions, labels, merge status,
and the user's own inline review comments) and issue details (body,
all comments up to COMMENT_CAP per issue).

Supports checkpoint/resume: items already written to per-item cache
files in <output-dir>/cache/ are skipped on re-runs.

Supports partial runs via --skip-authored / --skip-reviewed / --skip-issues
flags so Agent A1 and Agent A2 can each fetch only their subset.
"""

import argparse
import json
import os
import sys
import time
import threading
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Constants ─────────────────────────────────────────────────────────────────
COMMENT_CAP = 200       # max issue comments to fetch (paginated)
MAX_RETRIES = 3         # max attempts on rate-limit or transient errors
MAX_WORKERS = 10        # concurrent HTTP workers
RATE_LIMIT_SAFETY = 100 # sleep only when remaining drops below this

# ── Thread-safe rate-limit state ──────────────────────────────────────────────
_rate_lock = threading.Lock()
_rate_remaining = None
_rate_reset_ts = None


def _rate_guard(remaining, reset_ts):
    """Sleep only if we're close to exhausting the rate limit.

    Called after each successful API response with the headers from that
    response. Does nothing when remaining is healthy (≥ RATE_LIMIT_SAFETY).
    """
    if remaining is None:
        return
    if remaining < RATE_LIMIT_SAFETY:
        wait = max(int(reset_ts) - int(time.time()) + 1, 1)
        print(f"  Rate guard: {remaining} remaining, sleeping {wait}s", file=sys.stderr)
        time.sleep(wait)


def github_api(endpoint, token, max_retries=MAX_RETRIES):
    """Call GitHub REST API and return (parsed_json, remaining, reset_ts).

    Returns (None, None, None) on unrecoverable error.
    Returns ("RATE_LIMITED", None, None) when all retries exhausted on 403.
    """
    global _rate_remaining, _rate_reset_ts
    url = f"https://api.github.com/{endpoint}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                remaining = resp.headers.get("X-RateLimit-Remaining")
                reset_ts = resp.headers.get("X-RateLimit-Reset")
            remaining = int(remaining) if remaining else None
            reset_ts = int(reset_ts) if reset_ts else int(time.time()) + 3600
            # Update shared state
            with _rate_lock:
                _rate_remaining = remaining
                _rate_reset_ts = reset_ts
            _rate_guard(remaining, reset_ts)
            return data, remaining, reset_ts
        except urllib.error.HTTPError as e:
            if e.code == 403:
                reset = e.headers.get("X-RateLimit-Reset", "")
                if reset:
                    wait = int(reset) - int(time.time()) + 1
                    wait = max(wait, 60)
                else:
                    wait = 60 * attempt
                if attempt < max_retries:
                    print(f"  Rate limited (attempt {attempt}/{max_retries}). Waiting {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                    continue
                else:
                    print(f"  Rate limited after {max_retries} attempts for {endpoint}. Giving up.", file=sys.stderr)
                    return "RATE_LIMITED", None, None
            elif e.code == 404:
                return None, None, None
            else:
                print(f"  HTTP {e.code} for {endpoint}: {e.reason}", file=sys.stderr)
                return None, None, None
        except urllib.error.URLError as e:
            print(f"  Network error for {endpoint}: {e.reason}", file=sys.stderr)
            if attempt < max_retries:
                time.sleep(5 * attempt)
                continue
            return None, None, None
    return None, None, None


def fetch_all_issue_comments(repo, number, token, cap=COMMENT_CAP):
    """Fetch issue comments across pages up to cap."""
    comments = []
    page = 1
    per_page = min(100, cap)

    while len(comments) < cap:
        data, _, _ = github_api(
            f"repos/{repo}/issues/{number}/comments?per_page={per_page}&page={page}",
            token
        )
        if not data:
            break
        for c in data:
            comments.append({
                "author": c.get("user", {}).get("login", ""),
                "body": c.get("body", "")[:500],
                "created_at": c.get("created_at", ""),
            })
        if len(data) < per_page:
            break
        page += 1

    return comments[:cap]


def fetch_user_review_comments(repo, number, username, token):
    """Fetch inline review comments left by username on a PR."""
    data, _, _ = github_api(f"repos/{repo}/pulls/{number}/comments?per_page=100", token)
    if not data:
        return []
    return [
        {
            "body": c.get("body", "")[:500],
            "path": c.get("path", ""),
            "created_at": c.get("created_at", ""),
        }
        for c in data
        if c.get("user", {}).get("login", "").lower() == username.lower()
    ]


def cache_path(output_dir, kind, key):
    """Path for a per-item cache file."""
    cache_dir = os.path.join(output_dir, "cache", kind)
    os.makedirs(cache_dir, exist_ok=True)
    safe_key = key.replace("/", "__")
    return os.path.join(cache_dir, f"{safe_key}.json")


def load_cached(output_dir, kind, key):
    path = cache_path(output_dir, kind, key)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def save_cached(output_dir, kind, key, data):
    path = cache_path(output_dir, kind, key)
    with open(path, "w") as f:
        json.dump(data, f)


def fetch_pr_details(repo, number, username, token, output_dir):
    """Fetch detailed PR info, using cache if available."""
    cache_key = f"{repo.replace('/', '__')}__{number}"
    cached = load_cached(output_dir, "prs", cache_key)
    if cached:
        return cached

    data, _, _ = github_api(f"repos/{repo}/pulls/{number}", token)
    if not data or data == "RATE_LIMITED":
        return None

    review_comments = fetch_user_review_comments(repo, number, username, token)

    result = {
        "repo": repo,
        "number": number,
        "title": data.get("title", ""),
        "body": data.get("body", "") or "",
        "state": data.get("state", ""),
        "merged": data.get("merged", False),
        "merged_at": data.get("merged_at"),
        "created_at": data.get("created_at"),
        "closed_at": data.get("closed_at"),
        "additions": data.get("additions", 0),
        "deletions": data.get("deletions", 0),
        "changed_files": data.get("changed_files", 0),
        "labels": [l["name"] for l in data.get("labels", [])],
        "url": data.get("html_url", ""),
        "user": data.get("user", {}).get("login", ""),
        "my_review_comments": review_comments,
        "my_review_comment_count": len(review_comments),
    }
    save_cached(output_dir, "prs", cache_key, result)
    return result


def fetch_issue_details(repo, number, token, output_dir):
    """Fetch detailed issue info with all comments, using cache if available."""
    cache_key = f"{repo.replace('/', '__')}__{number}"
    cached = load_cached(output_dir, "issues", cache_key)
    if cached:
        return cached

    data, _, _ = github_api(f"repos/{repo}/issues/{number}", token)
    if not data or data == "RATE_LIMITED":
        return None

    comments = fetch_all_issue_comments(repo, number, token)

    result = {
        "repo": repo,
        "number": number,
        "title": data.get("title", ""),
        "body": data.get("body", "") or "",
        "state": data.get("state", ""),
        "created_at": data.get("created_at"),
        "closed_at": data.get("closed_at"),
        "labels": [l["name"] for l in data.get("labels", [])],
        "url": data.get("html_url", ""),
        "user": data.get("user", {}).get("login", ""),
        "comments": comments,
        "comment_count": len(comments),
    }
    save_cached(output_dir, "issues", cache_key, result)
    return result


# ── Thread-safe progress counter ──────────────────────────────────────────────
class _Progress:
    def __init__(self, total, label):
        self._lock = threading.Lock()
        self._count = 0
        self._total = total
        self._label = label

    def increment(self, repo, number):
        with self._lock:
            self._count += 1
            sys.stdout.write(f"\r  [{self._count}/{self._total}] {self._label}: {repo}#{number}    ")
            sys.stdout.flush()

    def done(self):
        print()  # newline after \r progress


# ── Parallel fetch helpers ─────────────────────────────────────────────────────
def _fetch_authored_pr_task(args):
    pr, username, token, output_dir, progress = args
    repo = pr["repository"]["nameWithOwner"]
    number = pr["number"]
    detail = fetch_pr_details(repo, number, username, token, output_dir)
    progress.increment(repo, number)
    if detail:
        detail["involvement"] = "authored"
    return detail


def _fetch_reviewed_pr_task(args):
    pr, username, token, output_dir, progress = args
    repo = pr["repository"]["nameWithOwner"]
    number = pr["number"]
    detail = fetch_pr_details(repo, number, username, token, output_dir)
    progress.increment(repo, number)
    if detail:
        detail["involvement"] = "reviewed"
        detail["review_reason"] = pr.get("review_reason", "")
        detail["review_details"] = pr.get("review_details", {})
    return detail


def _fetch_issue_task(args):
    issue, token, output_dir, progress = args
    repo = issue["repository"]["nameWithOwner"]
    number = issue["number"]
    detail = fetch_issue_details(repo, number, token, output_dir)
    progress.increment(repo, number)
    if detail:
        # "roles" is written by Phase 1 deduplication as a list
        detail["roles"] = issue.get("roles", [])
    return detail


def run(args):
    """Core logic, extracted for testability. args is an argparse.Namespace."""
    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.prs_authored) as f:
        prs_authored = json.load(f)
    with open(args.prs_reviewed) as f:
        prs_reviewed = json.load(f)
    with open(args.issues) as f:
        issues = json.load(f)

    skip_authored = getattr(args, "skip_authored", False)
    skip_reviewed = getattr(args, "skip_reviewed", False)
    skip_issues = getattr(args, "skip_issues", False)

    pr_details_authored = []
    pr_details_reviewed = []
    issue_details = []

    # ── Authored PRs ──────────────────────────────────────────────────────────
    if not skip_authored and prs_authored:
        print(f"\n--- Fetching {len(prs_authored)} authored PR details (workers={MAX_WORKERS}) ---")
        progress = _Progress(len(prs_authored), "authored")
        tasks = [(pr, args.username, args.token, args.output_dir, progress) for pr in prs_authored]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            pr_details_authored = [d for d in pool.map(_fetch_authored_pr_task, tasks) if d]
        progress.done()

    # ── Reviewed PRs ─────────────────────────────────────────────────────────
    if not skip_reviewed and prs_reviewed:
        print(f"\n--- Fetching {len(prs_reviewed)} reviewed PR details (workers={MAX_WORKERS}) ---")
        progress = _Progress(len(prs_reviewed), "reviewed")
        tasks = [(pr, args.username, args.token, args.output_dir, progress) for pr in prs_reviewed]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            pr_details_reviewed = [d for d in pool.map(_fetch_reviewed_pr_task, tasks) if d]
        progress.done()

    # ── Issues ────────────────────────────────────────────────────────────────
    if not skip_issues and issues:
        print(f"\n--- Fetching {len(issues)} issue details (workers={MAX_WORKERS}) ---")
        progress = _Progress(len(issues), "issues")
        tasks = [(issue, args.token, args.output_dir, progress) for issue in issues]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            issue_details = [d for d in pool.map(_fetch_issue_task, tasks) if d]
        progress.done()

    # ── Save results ──────────────────────────────────────────────────────────
    # Write separate files so A1/A2 agents can run concurrently without conflict.
    # The approval gate merges pr-details-authored.json + pr-details-reviewed.json
    # into pr-details.json before Phase 6.
    if not skip_authored:
        with open(f"{args.output_dir}/pr-details-authored.json", "w") as f:
            json.dump(pr_details_authored, f, indent=2)
    if not skip_reviewed:
        with open(f"{args.output_dir}/pr-details-reviewed.json", "w") as f:
            json.dump(pr_details_reviewed, f, indent=2)
    if not skip_issues:
        with open(f"{args.output_dir}/issue-details.json", "w") as f:
            json.dump(issue_details, f, indent=2)

    # ── Stats ─────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("DETAIL FETCH RESULTS")
    print(f"{'='*60}")

    if not skip_authored:
        merged = [p for p in pr_details_authored if p.get("merged")]
        total_additions = sum(p.get("additions", 0) for p in pr_details_authored)
        total_deletions = sum(p.get("deletions", 0) for p in pr_details_authored)
        total_files = sum(p.get("changed_files", 0) for p in pr_details_authored)
        print(f"Authored PRs: {len(pr_details_authored)} ({len(merged)} merged)")
        print(f"  Lines added: {total_additions:,}")
        print(f"  Lines deleted: {total_deletions:,}")
        print(f"  Files changed: {total_files:,}")

    if not skip_reviewed:
        total_review_comments = sum(p.get("my_review_comment_count", 0) for p in pr_details_reviewed)
        print(f"Reviewed PRs: {len(pr_details_reviewed)}")
        print(f"  Inline review comments left: {total_review_comments:,}")

    if not skip_issues:
        open_issues = [i for i in issue_details if i.get("state") == "open"]
        closed_issues = [i for i in issue_details if i.get("state") == "closed"]
        print(f"Issues: {len(issue_details)} ({len(open_issues)} open, {len(closed_issues)} closed)")

    # Top repos by lines changed (authored only)
    if not skip_authored and pr_details_authored:
        repo_lines = defaultdict(lambda: {"added": 0, "deleted": 0})
        for p in pr_details_authored:
            repo_lines[p["repo"]]["added"] += p.get("additions", 0)
            repo_lines[p["repo"]]["deleted"] += p.get("deletions", 0)
        print(f"\nLines changed by repo (authored PRs):")
        for repo, lines in sorted(repo_lines.items(),
                                   key=lambda x: x[1]["added"] + x[1]["deleted"],
                                   reverse=True)[:10]:
            print(f"  {repo}: +{lines['added']:,} / -{lines['deleted']:,}")

    print(f"\nOutput saved to {args.output_dir}/")

    return pr_details_authored, pr_details_reviewed, issue_details


def main():
    parser = argparse.ArgumentParser(description="Fetch detailed content for PRs and issues")
    parser.add_argument("--token", help="GitHub auth token (defaults to GH_TOKEN env var)")
    parser.add_argument("--username", required=True, help="GitHub username (used to filter review comments)")
    parser.add_argument("--prs-authored", required=True, help="Path to prs-authored.json")
    parser.add_argument("--prs-reviewed", required=True, help="Path to prs-genuinely-reviewed.json")
    parser.add_argument("--issues", required=True, help="Path to issues-all-deduped.json")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--skip-authored", action="store_true",
                        help="Skip authored PRs (Agent A2 mode: only reviewed PRs)")
    parser.add_argument("--skip-reviewed", action="store_true",
                        help="Skip reviewed PRs (Agent A1 mode: only authored PRs + issues)")
    parser.add_argument("--skip-issues", action="store_true",
                        help="Skip issues (Agent A2 mode: only reviewed PRs)")
    args = parser.parse_args()
    args.token = args.token or os.environ.get("GH_TOKEN")
    if not args.token:
        parser.error("GitHub auth token required via --token or GH_TOKEN environment variable")
    run(args)


if __name__ == "__main__":
    main()
