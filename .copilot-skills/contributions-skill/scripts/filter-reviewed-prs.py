#!/usr/bin/env python3
"""
Filter review-requested PRs to find genuinely reviewed ones.

Checks each PR for meaningful review activity (reviews, inline comments,
issue comments) and discards automated approvals and boilerplate.

Uses urllib.request directly to bypass shell hook output interception.
Fetches reviews and inline comments in parallel using ThreadPoolExecutor.
"""

import argparse
import json
import os
import sys
import time
import threading
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Constants ─────────────────────────────────────────────────────────────────
MAX_RETRIES = 3
MAX_WORKERS = 10
RATE_LIMIT_SAFETY = 100

# ── Thread-safe rate-limit state ──────────────────────────────────────────────
_rate_lock = threading.Lock()
_rate_remaining = None
_rate_reset_ts = None

_print_lock = threading.Lock()

BOILERPLATE = {
    "", "lgtm", "👍", "approved", "looks good", "lgtm!", "👍🏻",
    "looks good to me", "looks good!", ":+1:", ":thumbsup:",
}


def _rate_guard(remaining, reset_ts):
    """Sleep only if we're close to exhausting the rate limit."""
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


def is_meaningful_body(body):
    """Check if a review/comment body is meaningful (not boilerplate)."""
    if not body:
        return False
    cleaned = body.strip().lower()
    if cleaned in BOILERPLATE:
        return False
    if len(cleaned) < 10:
        return False
    return True


def check_pr(pr, username, token):
    """Check a single PR for genuine review activity.
    Returns (keep: bool, reason: str, details: dict)
    """
    repo = pr["repository"]["nameWithOwner"]
    number = pr["number"]

    # Fetch reviews and inline comments once each, shared across all decision paths
    reviews, _, _ = github_api(f"repos/{repo}/pulls/{number}/reviews", token)
    if reviews == "RATE_LIMITED":
        return None, "RATE_LIMITED", {}

    inline, _, _ = github_api(f"repos/{repo}/pulls/{number}/comments", token)
    if inline == "RATE_LIMITED":
        return None, "RATE_LIMITED", {}

    user_inline = [
        c for c in (inline or [])
        if c.get("user", {}).get("login", "").lower() == username.lower()
    ]

    # ── Check formal reviews ──────────────────────────────────────────────────
    user_reviews = []
    if reviews:
        user_reviews = [r for r in reviews if r.get("user", {}).get("login", "").lower() == username.lower()]

    if user_reviews:
        for review in user_reviews:
            state = review.get("state", "")
            body = review.get("body", "")

            if state == "CHANGES_REQUESTED":
                return True, "requested_changes", {"review_state": state, "body_preview": body[:200]}

            if state == "COMMENTED" and is_meaningful_body(body):
                return True, "meaningful_review_comment", {"review_state": state, "body_preview": body[:200]}

            if state == "APPROVED" and is_meaningful_body(body):
                return True, "approved_with_comment", {"review_state": state, "body_preview": body[:200]}

        # Had reviews but all boilerplate — fall through to inline comments

    # ── Inline review comments (shared fetch, checked for both paths) ─────────
    if user_inline:
        return True, "inline_review_comments", {
            "count": len(user_inline),
            "preview": user_inline[0].get("body", "")[:200]
        }

    # ── If formal reviews were all boilerplate, stop here ────────────────────
    if user_reviews:
        return False, "automated_approval_only", {
            "review_states": [r["state"] for r in user_reviews],
            "bodies": [r.get("body", "")[:50] for r in user_reviews]
        }

    # ── No formal reviews at all — check issue-level comments ────────────────
    issue_comments, _, _ = github_api(f"repos/{repo}/issues/{number}/comments", token)
    if issue_comments == "RATE_LIMITED":
        return None, "RATE_LIMITED", {}
    user_issue_comments = [
        c for c in (issue_comments or [])
        if c.get("user", {}).get("login", "").lower() == username.lower()
    ]

    if user_issue_comments:
        meaningful = [c for c in user_issue_comments if is_meaningful_body(c.get("body", ""))]
        if meaningful:
            return True, "issue_comment", {
                "count": len(meaningful),
                "preview": meaningful[0].get("body", "")[:200]
            }

    return False, "no_activity", {}


def _check_one_task(args):
    pr, username, token = args
    keep, reason, details = check_pr(pr, username, token)
    return pr, keep, reason, details


def run_filter(prs, username, token, output_dir):
    """Core filter logic, extracted for testability.

    Returns (kept, discarded, errors) lists.
    Writes prs-genuinely-reviewed.json, prs-discarded.json to output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    total = len(prs)

    kept = []
    discarded = []
    errors = []
    counter = [0]

    tasks = [(pr, username, token) for pr in prs]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(_check_one_task, t): t[0] for t in tasks}
        for future in as_completed(futures):
            pr, keep, reason, details = future.result()
            repo = pr["repository"]["nameWithOwner"]
            number = pr["number"]
            title = pr["title"][:60]

            counter[0] += 1
            i = counter[0]

            if keep is None and reason == "RATE_LIMITED":
                # One final retry after a brief wait
                time.sleep(60)
                keep, reason, details = check_pr(pr, username, token)
                if keep is None:
                    errors.append({"pr": pr, "error": "rate_limited_twice"})
                    with _print_lock:
                        print(f"  [{i}/{total}] STILL RATE LIMITED: {repo}#{number}")
                    continue

            if keep:
                pr["review_reason"] = reason
                pr["review_details"] = details
                kept.append(pr)
                with _print_lock:
                    print(f"  [{i}/{total}] KEEP ({reason}): {repo}#{number} - {title}")
            else:
                pr["discard_reason"] = reason
                pr["discard_details"] = details
                discarded.append(pr)
                if i % 50 == 0:
                    with _print_lock:
                        print(f"  [{i}/{total}] skip ({reason}): {repo}#{number} - {title}")

            if i % 50 == 0:
                with _print_lock:
                    print(f"  --- Progress: {i}/{total} | Kept: {len(kept)} | Discarded: {len(discarded)} ---")

    # Save results
    with open(f"{output_dir}/prs-genuinely-reviewed.json", "w") as f:
        json.dump(kept, f, indent=2)
    with open(f"{output_dir}/prs-discarded.json", "w") as f:
        json.dump(discarded, f, indent=2)
    if errors:
        with open(f"{output_dir}/prs-errors.json", "w") as f:
            json.dump(errors, f, indent=2)

    return kept, discarded, errors


def main():
    parser = argparse.ArgumentParser(description="Filter review-requested PRs for genuine reviews")
    parser.add_argument("--token", help="GitHub auth token (defaults to GH_TOKEN env var)")
    parser.add_argument("--username", required=True, help="GitHub username")
    parser.add_argument("--input", required=True, help="Path to prs-reviewed-only.json")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()
    args.token = args.token or os.environ.get("GH_TOKEN")
    if not args.token:
        parser.error("GitHub auth token required via --token or GH_TOKEN environment variable")

    with open(args.input) as f:
        prs = json.load(f)
    total = len(prs)
    print(f"Processing {total} PRs (workers={MAX_WORKERS})...")

    kept, discarded, errors = run_filter(prs, args.username, args.token, args.output_dir)

    # Summary
    print(f"\n{'='*60}")
    print("FILTER RESULTS")
    print(f"{'='*60}")
    print(f"Total processed: {total}")
    print(f"Genuinely reviewed (kept): {len(kept)}")
    print(f"Discarded: {len(discarded)}")
    print(f"Errors: {len(errors)}")

    if kept:
        reasons = Counter(p["review_reason"] for p in kept)
        repos = Counter(p["repository"]["nameWithOwner"] for p in kept)
        print(f"\nKept by reason: {dict(reasons)}")
        print(f"\nKept by repo:")
        for repo, count in repos.most_common():
            print(f"  {count:3d}  {repo}")


if __name__ == "__main__":
    main()
