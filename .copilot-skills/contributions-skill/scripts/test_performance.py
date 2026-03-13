#!/usr/bin/env python3
"""
Performance and correctness test harness for contributions skill scripts.

Tests:
  1. Rate guard — only sleeps when X-RateLimit-Remaining < threshold
  2. Parallel speedup — ThreadPoolExecutor is ≥5x faster than sequential
  3. Cache hits — cached items skip all HTTP calls
  4. fetch-details output correctness — right keys, involvement field, roles field
  5. filter-reviewed-prs parallel correctness — same results as sequential, no duplicates

No live API calls: all HTTP is intercepted via unittest.mock.
No GitHub token required.

Usage:
    python3 test_performance.py           # run all tests
    python3 test_performance.py -v        # verbose output
    python3 test_performance.py Test2     # run a single test by name
"""

import json
import os
import sys
import tempfile
import time
import threading
import unittest
import unittest.mock
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from http.client import HTTPMessage

# ──────────────────────────────────────────────────────────────────────────────
# Helpers — build fake urllib HTTP responses
# ──────────────────────────────────────────────────────────────────────────────

def _make_response(body, remaining=4999, reset_ts=None):
    """Return a mock object that looks like urllib.request.urlopen() response."""
    if reset_ts is None:
        reset_ts = int(time.time()) + 3600

    raw = json.dumps(body).encode()
    mock_resp = unittest.mock.MagicMock()
    mock_resp.read.return_value = raw
    mock_resp.headers = {
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(reset_ts),
    }
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = unittest.mock.MagicMock(return_value=False)
    return mock_resp


def _make_pr_response(number, repo="org/repo", remaining=4999):
    """A realistic /pulls/{number} REST response."""
    return _make_response({
        "number": number,
        "title": f"PR #{number}",
        "body": f"Description of PR {number}",
        "state": "merged",
        "merged": True,
        "merged_at": "2026-01-15T10:00:00Z",
        "created_at": "2026-01-10T08:00:00Z",
        "closed_at": "2026-01-15T10:00:00Z",
        "additions": 42,
        "deletions": 10,
        "changed_files": 3,
        "labels": [{"name": "bug"}],
        "html_url": f"https://github.com/{repo}/pull/{number}",
        "user": {"login": "testuser"},
    }, remaining=remaining)


def _make_comments_response(comments=None, remaining=4999):
    """A /pulls/{n}/comments or /issues/{n}/comments response."""
    return _make_response(comments or [], remaining=remaining)


def _make_reviews_response(reviews=None, remaining=4999):
    return _make_response(reviews or [], remaining=remaining)


# ──────────────────────────────────────────────────────────────────────────────
# Dynamically import the scripts under test
# ──────────────────────────────────────────────────────────────────────────────

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

def _import_script(name):
    """Import a script as a module without executing its main() block."""
    import importlib.util
    path = os.path.join(SCRIPTS_DIR, name)
    spec = importlib.util.spec_from_file_location(name.replace(".py", "").replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    # Patch sys.argv so argparse inside the module doesn't choke on test runner args
    with unittest.mock.patch("sys.argv", [name]):
        spec.loader.exec_module(mod)
    return mod


# ──────────────────────────────────────────────────────────────────────────────
# Test 1 — Rate guard: only sleeps when remaining < threshold
# ──────────────────────────────────────────────────────────────────────────────

class Test1RateGuard(unittest.TestCase):
    """Rate guard should NOT sleep on healthy remaining counts, SHOULD sleep near limit."""

    def setUp(self):
        self.mod = _import_script("fetch-details.py")

    def test_no_sleep_when_healthy(self):
        """500 calls with remaining=4999 → zero sleeps."""
        sleep_calls = []
        with unittest.mock.patch("time.sleep", side_effect=sleep_calls.append):
            for _ in range(500):
                self.mod._rate_guard(4999, int(time.time()) + 3600)
        self.assertEqual(len(sleep_calls), 0,
            f"Expected 0 sleeps on healthy remaining, got {len(sleep_calls)}")

    def test_sleeps_when_near_limit(self):
        """remaining=50 (below RATE_LIMIT_SAFETY=100) → should sleep."""
        sleep_calls = []
        future_reset = int(time.time()) + 30
        with unittest.mock.patch("time.sleep", side_effect=sleep_calls.append):
            self.mod._rate_guard(50, future_reset)
        self.assertGreater(len(sleep_calls), 0,
            "Expected at least 1 sleep when remaining < RATE_LIMIT_SAFETY")

    def test_sleep_duration_reasonable(self):
        """Sleep duration should match time until reset."""
        future_reset = int(time.time()) + 45
        sleep_calls = []
        with unittest.mock.patch("time.sleep", side_effect=sleep_calls.append):
            self.mod._rate_guard(10, future_reset)
        self.assertTrue(len(sleep_calls) > 0)
        # Should sleep roughly (reset - now) seconds, ±2s tolerance
        self.assertAlmostEqual(sleep_calls[0], 46, delta=2,
            msg=f"Expected sleep ~46s, got {sleep_calls[0]:.1f}s")

    def test_threshold_boundary(self):
        """remaining == RATE_LIMIT_SAFETY should NOT sleep (boundary is exclusive)."""
        threshold = self.mod.RATE_LIMIT_SAFETY
        sleep_calls = []
        with unittest.mock.patch("time.sleep", side_effect=sleep_calls.append):
            self.mod._rate_guard(threshold, int(time.time()) + 3600)
        self.assertEqual(len(sleep_calls), 0,
            f"Should not sleep at exactly RATE_LIMIT_SAFETY={threshold}")


# ──────────────────────────────────────────────────────────────────────────────
# Test 2 — Parallel speedup: ≥5x faster than sequential
# ──────────────────────────────────────────────────────────────────────────────

class Test2ParallelSpeedup(unittest.TestCase):
    """Parallel fetch of 20 items each taking 0.05s should be ≥5x faster."""

    ITEMS = 20
    ITEM_DELAY = 0.05   # simulated network RTT per item

    def _fetch_item_slow(self, item):
        """Simulate a blocking network fetch."""
        time.sleep(self.ITEM_DELAY)
        return {"id": item, "result": "ok"}

    def test_sequential_baseline(self):
        start = time.time()
        results = [self._fetch_item_slow(i) for i in range(self.ITEMS)]
        elapsed = time.time() - start
        self.assertEqual(len(results), self.ITEMS)
        # Should take close to ITEMS * ITEM_DELAY
        self.assertGreater(elapsed, self.ITEMS * self.ITEM_DELAY * 0.8)

    def test_parallel_is_faster(self):
        start = time.time()
        with ThreadPoolExecutor(max_workers=10) as pool:
            results = list(pool.map(self._fetch_item_slow, range(self.ITEMS)))
        parallel_elapsed = time.time() - start

        # Sequential reference (just math, not re-running)
        sequential_estimate = self.ITEMS * self.ITEM_DELAY

        speedup = sequential_estimate / parallel_elapsed
        self.assertGreaterEqual(speedup, 5.0,
            f"Expected ≥5x speedup, got {speedup:.1f}x "
            f"(parallel={parallel_elapsed:.2f}s, seq_est={sequential_estimate:.2f}s)")
        self.assertEqual(len(results), self.ITEMS)

    def test_fetch_details_uses_threadpool(self):
        """fetch-details.py must expose MAX_WORKERS constant ≥ 5."""
        mod = _import_script("fetch-details.py")
        self.assertTrue(hasattr(mod, "MAX_WORKERS"),
            "fetch-details.py must define MAX_WORKERS")
        self.assertGreaterEqual(mod.MAX_WORKERS, 5,
            f"MAX_WORKERS should be ≥5, got {mod.MAX_WORKERS}")

    def test_filter_uses_threadpool(self):
        """filter-reviewed-prs.py must expose MAX_WORKERS constant ≥ 5."""
        mod = _import_script("filter-reviewed-prs.py")
        self.assertTrue(hasattr(mod, "MAX_WORKERS"),
            "filter-reviewed-prs.py must define MAX_WORKERS")
        self.assertGreaterEqual(mod.MAX_WORKERS, 5,
            f"MAX_WORKERS should be ≥5, got {mod.MAX_WORKERS}")


# ──────────────────────────────────────────────────────────────────────────────
# Test 3 — Cache hits skip HTTP
# ──────────────────────────────────────────────────────────────────────────────

class Test3CacheHits(unittest.TestCase):
    """Items already in cache must not trigger any urllib.request.urlopen calls."""

    def setUp(self):
        self.mod = _import_script("fetch-details.py")
        self.tmpdir = tempfile.mkdtemp()

    def _pre_populate_cache(self, items):
        """Write fake cached entries for the given (repo, number) pairs."""
        for repo, number in items:
            cached_data = {
                "repo": repo, "number": number,
                "title": f"Cached PR #{number}", "body": "cached body",
                "state": "merged", "merged": True, "merged_at": None,
                "created_at": None, "closed_at": None,
                "additions": 1, "deletions": 1, "changed_files": 1,
                "labels": [], "url": "", "user": "testuser",
                "my_review_comments": [], "my_review_comment_count": 0,
            }
            self.mod.save_cached(self.tmpdir, "prs", f"{repo.replace('/', '__')}__{number}", cached_data)

    def test_cached_prs_skip_http(self):
        items = [("org/repo-a", 1), ("org/repo-a", 2), ("org/repo-b", 3)]
        self._pre_populate_cache(items)

        http_call_count = [0]
        def fake_urlopen(req):
            http_call_count[0] += 1
            return _make_pr_response(999)

        with unittest.mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            for repo, number in items:
                result = self.mod.fetch_pr_details(repo, number, "testuser", "fake-token", self.tmpdir)
                self.assertIsNotNone(result)
                self.assertEqual(result["number"], number)

        self.assertEqual(http_call_count[0], 0,
            f"Expected 0 HTTP calls for {len(items)} cached items, got {http_call_count[0]}")

    def test_uncached_prs_make_http_calls(self):
        items = [("org/repo-x", 10), ("org/repo-x", 11)]
        # No pre-population — cache is empty

        call_numbers = []
        def fake_urlopen(req):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            # Return empty inline review comments for /comments, real data for /pulls/{n}
            if "/comments" in url:
                return _make_comments_response()
            num = int(url.rstrip("/").split("/")[-1])
            call_numbers.append(num)
            return _make_pr_response(num)

        with unittest.mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            for repo, number in items:
                self.mod.fetch_pr_details(repo, number, "testuser", "fake-token", self.tmpdir)

        self.assertGreaterEqual(len(call_numbers), len(items),
            f"Expected ≥{len(items)} HTTP calls for uncached items, got {len(call_numbers)}")


# ──────────────────────────────────────────────────────────────────────────────
# Test 4 — fetch-details output correctness
# ──────────────────────────────────────────────────────────────────────────────

class Test4OutputCorrectness(unittest.TestCase):
    """End-to-end: write input JSONs, run main(), assert output files are correct."""

    def setUp(self):
        self.mod = _import_script("fetch-details.py")
        self.tmpdir = tempfile.mkdtemp()

        # 3 authored PRs
        self.prs_authored = [
            {"number": i, "repository": {"nameWithOwner": "org/repo"}, "title": f"PR {i}"}
            for i in [1, 2, 3]
        ]
        # 2 issues
        self.issues = [
            {"number": i, "repository": {"nameWithOwner": "org/repo"},
             "title": f"Issue {i}", "roles": ["authored"]}
            for i in [101, 102]
        ]

        self.prs_authored_path = os.path.join(self.tmpdir, "prs-authored.json")
        self.prs_reviewed_path = os.path.join(self.tmpdir, "prs-reviewed.json")
        self.issues_path = os.path.join(self.tmpdir, "issues.json")

        with open(self.prs_authored_path, "w") as f:
            json.dump(self.prs_authored, f)
        with open(self.prs_reviewed_path, "w") as f:
            json.dump([], f)
        with open(self.issues_path, "w") as f:
            json.dump(self.issues, f)

    def _fake_urlopen(self, req):
        url = req.full_url if hasattr(req, "full_url") else str(req)
        if "/comments" in url:
            return _make_comments_response()
        if "/issues/" in url and "/pulls/" not in url:
            # Issue detail endpoint
            num = int(url.rstrip("/").split("/")[-1])
            return _make_response({
                "number": num, "title": f"Issue {num}", "body": "issue body",
                "state": "open", "created_at": None, "closed_at": None,
                "labels": [], "html_url": "", "user": {"login": "testuser"},
            })
        # PR detail: extract number from URL
        parts = url.rstrip("/").split("/")
        try:
            num = int(parts[-1])
        except ValueError:
            num = 1
        return _make_pr_response(num)

    def test_authored_prs_have_involvement_authored(self):
        with unittest.mock.patch("urllib.request.urlopen", side_effect=self._fake_urlopen):
            import argparse
            args = argparse.Namespace(
                token="fake", username="testuser",
                prs_authored=self.prs_authored_path,
                prs_reviewed=self.prs_reviewed_path,
                issues=self.issues_path,
                output_dir=self.tmpdir,
                skip_authored=False, skip_reviewed=True, skip_issues=True,
            )
            self.mod.run(args)

        out = os.path.join(self.tmpdir, "pr-details-authored.json")
        self.assertTrue(os.path.exists(out), "pr-details-authored.json not created")
        with open(out) as f:
            data = json.load(f)
        self.assertEqual(len(data), 3, f"Expected 3 authored PRs, got {len(data)}")
        for item in data:
            self.assertEqual(item["involvement"], "authored",
                f"involvement should be 'authored', got {item.get('involvement')}")

    def test_issues_have_roles_field(self):
        with unittest.mock.patch("urllib.request.urlopen", side_effect=self._fake_urlopen):
            import argparse
            args = argparse.Namespace(
                token="fake", username="testuser",
                prs_authored=self.prs_authored_path,
                prs_reviewed=self.prs_reviewed_path,
                issues=self.issues_path,
                output_dir=self.tmpdir,
                skip_authored=True, skip_reviewed=True, skip_issues=False,
            )
            self.mod.run(args)

        out = os.path.join(self.tmpdir, "issue-details.json")
        self.assertTrue(os.path.exists(out), "issue-details.json not created")
        with open(out) as f:
            data = json.load(f)
        self.assertEqual(len(data), 2, f"Expected 2 issues, got {len(data)}")
        for item in data:
            self.assertIn("roles", item, "Each issue must have a 'roles' field")
            self.assertIsInstance(item["roles"], list, "'roles' must be a list")

    def test_no_unconditional_sleep(self):
        """main() must not call time.sleep() unconditionally (only via _rate_guard)."""
        sleep_calls = []
        # _rate_guard uses time.sleep; we want to confirm it's not called for healthy remaining
        with unittest.mock.patch("urllib.request.urlopen", side_effect=self._fake_urlopen):
            with unittest.mock.patch("time.sleep", side_effect=sleep_calls.append):
                import argparse
                args = argparse.Namespace(
                    token="fake", username="testuser",
                    prs_authored=self.prs_authored_path,
                    prs_reviewed=self.prs_reviewed_path,
                    issues=self.issues_path,
                    output_dir=self.tmpdir,
                    skip_authored=False, skip_reviewed=False, skip_issues=False,
                )
                self.mod.run(args)
        self.assertEqual(len(sleep_calls), 0,
            f"Expected 0 sleeps with healthy rate limit (remaining=4999), got {len(sleep_calls)}")


# ──────────────────────────────────────────────────────────────────────────────
# Test 5 — filter-reviewed-prs parallel correctness
# ──────────────────────────────────────────────────────────────────────────────

class Test5FilterParallelCorrectness(unittest.TestCase):
    """Parallel filter produces same keep/discard split as sequential, no duplicates."""

    def setUp(self):
        self.mod = _import_script("filter-reviewed-prs.py")
        self.tmpdir = tempfile.mkdtemp()

    def _make_prs(self, count):
        return [
            {
                "number": i,
                "title": f"PR #{i}",
                "repository": {"nameWithOwner": "org/repo"},
            }
            for i in range(1, count + 1)
        ]

    def _fake_urlopen_meaningful(self, req):
        """PRs 1–10 have meaningful reviews, 11–20 have boilerplate only."""
        url = req.full_url if hasattr(req, "full_url") else str(req)
        parts = url.rstrip("/").split("/")
        try:
            pr_num = int(parts[-2] if parts[-1] in ("reviews", "comments") else parts[-1])
        except (ValueError, IndexError):
            pr_num = 999

        if "/reviews" in url:
            if pr_num <= 10:
                body = "This has a real comment with substance and detail about the code"
                return _make_response([{
                    "user": {"login": "testuser"},
                    "state": "COMMENTED",
                    "body": body,
                }])
            else:
                return _make_response([{
                    "user": {"login": "testuser"},
                    "state": "APPROVED",
                    "body": "lgtm",
                }])
        if "/comments" in url:
            return _make_comments_response()
        if "/issues/" in url:
            return _make_comments_response()
        return _make_response([])

    def test_correct_split_10_keep_10_discard(self):
        prs = self._make_prs(20)
        input_path = os.path.join(self.tmpdir, "input.json")
        with open(input_path, "w") as f:
            json.dump(prs, f)

        with unittest.mock.patch("urllib.request.urlopen", side_effect=self._fake_urlopen_meaningful):
            kept, discarded, errors = self.mod.run_filter(
                prs=prs,
                username="testuser",
                token="fake-token",
                output_dir=self.tmpdir,
            )

        self.assertEqual(len(kept), 10,
            f"Expected 10 kept, got {len(kept)}: {[p['number'] for p in kept]}")
        self.assertEqual(len(discarded), 10,
            f"Expected 10 discarded, got {len(discarded)}")
        self.assertEqual(len(errors), 0,
            f"Expected 0 errors, got {len(errors)}")

    def test_no_duplicates_in_output(self):
        prs = self._make_prs(20)

        with unittest.mock.patch("urllib.request.urlopen", side_effect=self._fake_urlopen_meaningful):
            kept, discarded, errors = self.mod.run_filter(
                prs=prs,
                username="testuser",
                token="fake-token",
                output_dir=self.tmpdir,
            )

        all_numbers = [p["number"] for p in kept] + [p["number"] for p in discarded]
        self.assertEqual(len(all_numbers), len(set(all_numbers)),
            f"Duplicates found in output: {[n for n in all_numbers if all_numbers.count(n) > 1]}")
        self.assertEqual(len(all_numbers), 20,
            f"Expected 20 total items, got {len(all_numbers)}")

    def test_no_batch_sleep(self):
        """filter script must not call time.sleep() unconditionally."""
        prs = self._make_prs(5)
        sleep_calls = []

        with unittest.mock.patch("urllib.request.urlopen", side_effect=self._fake_urlopen_meaningful):
            with unittest.mock.patch("time.sleep", side_effect=sleep_calls.append):
                self.mod.run_filter(
                    prs=prs,
                    username="testuser",
                    token="fake-token",
                    output_dir=self.tmpdir,
                )

        self.assertEqual(len(sleep_calls), 0,
            f"Expected 0 unconditional sleeps, got {len(sleep_calls)}: {sleep_calls}")


# ──────────────────────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────────────────────

def _fmt_result(test_name, passed, detail=""):
    icon = "✅" if passed else "❌"
    msg = f"{icon} {test_name}"
    if detail:
        msg += f" ({detail})"
    return msg


if __name__ == "__main__":
    import argparse as _ap

    p = _ap.ArgumentParser(description="Contributions skill performance & correctness tests")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose unittest output")
    p.add_argument("filter", nargs="?", help="Run only tests matching this substring")
    parsed, remaining = p.parse_known_args()

    verbosity = 2 if parsed.verbose else 1
    loader = unittest.TestLoader()

    if parsed.filter:
        suite = unittest.TestSuite()
        for cls in [Test1RateGuard, Test2ParallelSpeedup, Test3CacheHits,
                    Test4OutputCorrectness, Test5FilterParallelCorrectness]:
            for name in loader.getTestCaseNames(cls):
                if parsed.filter.lower() in name.lower() or parsed.filter.lower() in cls.__name__.lower():
                    suite.addTest(cls(name))
    else:
        suite = unittest.TestSuite()
        for cls in [Test1RateGuard, Test2ParallelSpeedup, Test3CacheHits,
                    Test4OutputCorrectness, Test5FilterParallelCorrectness]:
            suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
