#!/usr/bin/env python3
"""
Search GitHub Discussions for mentions and detect kudos/recognition,
and capture discussions authored by the user.

Uses urllib.request directly to bypass shell hook output interception.
Searches via GraphQL API and applies keyword + emoji pattern matching.
Paginates through all results using cursor-based pagination.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

KUDOS_KEYWORDS = [
    "thanks", "thank you", "great work", "awesome", "kudos", "shoutout",
    "shout out", "props", "appreciate", "well done", "nice work", "stellar",
    "amazing", "fantastic", "excellent", "helped", "saved us", "went above",
    "above and beyond", "unblocked", "huge help", "lifesaver", "hero",
    "incredible", "outstanding", "superb", "brilliant", "grateful",
    "big thanks", "thank", "great job", "nice job", "good job",
]

KUDOS_EMOJI = ["🎉", "🙏", "👏", "🏆", "⭐", "💪", "🙌", "❤️", "💯", "🔥", "👍", "🥇"]

PAGE_SIZE = 100  # GraphQL max per page


def graphql(query, token, retries_remaining=1):
    """Execute a GraphQL query and return parsed JSON. Raises on error."""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        if "errors" in result:
            print(f"  GraphQL errors: {result['errors']}", file=sys.stderr)
        return result
    except urllib.error.HTTPError as e:
        if e.code == 403:
            reset = e.headers.get("X-RateLimit-Reset", "")
            if reset:
                wait = int(reset) - int(time.time()) + 1
                wait = max(wait, 60)
                print(f"  GraphQL rate limited. Waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)
                if retries_remaining > 0:
                    return graphql(query, token, retries_remaining=retries_remaining - 1)
                print("  GraphQL rate limited after retry, giving up.", file=sys.stderr)
                return None
            print(f"  GraphQL HTTP 403 (no reset header)", file=sys.stderr)
            return None
        elif e.code == 401:
            print(f"  GraphQL HTTP 401: bad token or insufficient scopes", file=sys.stderr)
            return None
        else:
            body = e.read().decode(errors="replace")
            print(f"  GraphQL HTTP {e.code}: {e.reason} — {body[:200]}", file=sys.stderr)
            return None
    except urllib.error.URLError as e:
        print(f"  GraphQL network error: {e.reason}", file=sys.stderr)
        return None


def fetch_all_discussions(query_str, token):
    """Fetch all discussions matching query_str using cursor pagination."""
    discussions = []
    cursor = None
    page = 1

    while True:
        after_clause = f', after: "{cursor}"' if cursor else ""
        gql = f"""
        {{
          search(query: "{query_str}", type: DISCUSSION, first: {PAGE_SIZE}{after_clause}) {{
            discussionCount
            pageInfo {{
              hasNextPage
              endCursor
            }}
            nodes {{
              ... on Discussion {{
                id
                title
                url
                createdAt
                body
                repository {{ nameWithOwner }}
                author {{ login }}
                comments(first: 100) {{
                  totalCount
                  nodes {{
                    author {{ login }}
                    body
                    createdAt
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        result = graphql(gql, token)
        if not result or "data" not in result:
            print(f"  Failed to fetch discussions page {page}, stopping.", file=sys.stderr)
            break

        search = result["data"]["search"]
        total = search["discussionCount"]
        nodes = search["nodes"]
        page_info = search["pageInfo"]

        discussions.extend(nodes)
        print(f"  Page {page}: fetched {len(nodes)} discussions (total reported: {total}, accumulated: {len(discussions)})")

        if not page_info["hasNextPage"]:
            break

        cursor = page_info["endCursor"]
        page += 1
        time.sleep(1)  # be polite between pages

    return discussions


def has_kudos(text, target_user):
    """Check if text contains kudos directed at target_user."""
    if not text:
        return False, []

    text_lower = text.lower()
    target_lower = target_user.lower()

    user_mentioned = (
        f"@{target_lower}" in text_lower or
        target_lower in text_lower
    )

    if not user_mentioned:
        return False, []

    signals = []

    for kw in KUDOS_KEYWORDS:
        if kw in text_lower:
            signals.append(f"keyword:{kw}")

    for emoji in KUDOS_EMOJI:
        if emoji in text:
            signals.append(f"emoji:{emoji}")

    if signals:
        return True, signals

    return False, []


def process_discussions_for_kudos(discussions, username):
    """Scan discussions and comments for kudos directed at username."""
    all_kudos = []
    all_discussions = []

    for disc in discussions:
        title = disc["title"]
        url = disc["url"]
        repo = disc["repository"]["nameWithOwner"]
        author = disc["author"]["login"] if disc.get("author") else "unknown"
        body = disc.get("body", "")
        comments = disc.get("comments", {}).get("nodes", [])
        comment_count = disc.get("comments", {}).get("totalCount", 0)

        print(f"\n  [{repo}] {title[:70]}")
        print(f"    Author: {author} | Comments: {comment_count}")

        disc_data = {
            "id": disc["id"],
            "title": title,
            "url": url,
            "repo": repo,
            "author": author,
            "createdAt": disc["createdAt"],
            "body": body,
            "commentCount": comment_count,
            "comments": comments,
            "kudos": []
        }

        # Check body for kudos (skip self-authored)
        if author.lower() != username.lower():
            is_kudos, signals = has_kudos(body, username)
            if is_kudos:
                lines = body.split("\n")
                relevant_lines = [l for l in lines if username.lower() in l.lower()]
                quote = relevant_lines[0].strip() if relevant_lines else body[:200]

                kudos_entry = {
                    "source": "discussion_body",
                    "who": author,
                    "quote": quote[:500],
                    "signals": signals,
                    "url": url,
                    "title": title,
                    "repo": repo,
                    "date": disc["createdAt"]
                }
                disc_data["kudos"].append(kudos_entry)
                all_kudos.append(kudos_entry)
                print(f"    KUDOS in body from {author}: {signals}")

        # Check comments for kudos
        for comment in comments:
            comment_author = comment.get("author", {})
            if isinstance(comment_author, dict):
                comment_login = comment_author.get("login", "unknown")
            else:
                comment_login = "unknown"

            if comment_login.lower() == username.lower():
                continue

            comment_body = comment.get("body", "")
            is_kudos, signals = has_kudos(comment_body, username)

            if is_kudos:
                lines = comment_body.split("\n")
                relevant_lines = [l for l in lines if username.lower() in l.lower()]
                quote = relevant_lines[0].strip() if relevant_lines else comment_body[:200]

                kudos_entry = {
                    "source": "comment",
                    "who": comment_login,
                    "quote": quote[:500],
                    "signals": signals,
                    "url": url,
                    "title": title,
                    "repo": repo,
                    "date": comment.get("createdAt", "")
                }
                disc_data["kudos"].append(kudos_entry)
                all_kudos.append(kudos_entry)
                print(f"    KUDOS in comment from {comment_login}: {signals}")

        all_discussions.append(disc_data)

    return all_discussions, all_kudos


def main():
    parser = argparse.ArgumentParser(description="Search GitHub Discussions for kudos/recognition and authored discussions")
    parser.add_argument("--token", help="GitHub auth token (defaults to GH_TOKEN env var)")
    parser.add_argument("--username", required=True, help="GitHub username to search for")
    parser.add_argument("--org", required=True, help="GitHub org to search within")
    parser.add_argument("--start-date", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()
    args.token = args.token or os.environ.get("GH_TOKEN")
    if not args.token:
        parser.error("GitHub auth token required via --token or GH_TOKEN environment variable")

    os.makedirs(args.output_dir, exist_ok=True)

    # ── Phase A: Discussions mentioning the user (kudos search) ─────────────
    print("Fetching discussions that mention the user (kudos search)...")
    mention_query = f'org:{args.org} {args.username} created:{args.start_date}..{args.end_date}'
    mention_discussions = fetch_all_discussions(mention_query, args.token)
    print(f"Total mention discussions fetched: {len(mention_discussions)}")

    all_discussions, all_kudos = process_discussions_for_kudos(mention_discussions, args.username)

    # ── Phase B: Discussions authored by the user ────────────────────────────
    print("\nFetching discussions authored by the user...")
    authored_query = f'org:{args.org} author:{args.username} created:{args.start_date}..{args.end_date}'
    authored_raw = fetch_all_discussions(authored_query, args.token)
    print(f"Total authored discussions fetched: {len(authored_raw)}")

    authored_discussions = []
    for disc in authored_raw:
        author = disc["author"]["login"] if disc.get("author") else "unknown"
        comments = disc.get("comments", {}).get("nodes", [])
        comment_count = disc.get("comments", {}).get("totalCount", 0)
        authored_discussions.append({
            "id": disc["id"],
            "title": disc["title"],
            "url": disc["url"],
            "repo": disc["repository"]["nameWithOwner"],
            "author": author,
            "createdAt": disc["createdAt"],
            "body": disc.get("body", ""),
            "commentCount": comment_count,
        })
        print(f"  [{disc['repository']['nameWithOwner']}] {disc['title'][:70]} ({comment_count} comments)")

    # ── Save results ─────────────────────────────────────────────────────────
    with open(f"{args.output_dir}/discussions-full.json", "w") as f:
        json.dump(all_discussions, f, indent=2)

    with open(f"{args.output_dir}/kudos-found.json", "w") as f:
        json.dump(all_kudos, f, indent=2)

    with open(f"{args.output_dir}/discussions-authored.json", "w") as f:
        json.dump(authored_discussions, f, indent=2)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("DISCUSSION RESULTS")
    print(f"{'='*60}")
    print(f"Mention discussions analyzed: {len(all_discussions)}")
    print(f"Kudos entries found:          {len(all_kudos)}")
    print(f"Discussions authored:         {len(authored_discussions)}")

    if all_kudos:
        print(f"\nKudos details:")
        for k in all_kudos:
            print(f"  - From: {k['who']} in [{k['repo']}] \"{k['title'][:50]}\"")
            print(f"    Signals: {', '.join(k['signals'])}")
            print(f"    Quote: {k['quote'][:150]}")
            print()


if __name__ == "__main__":
    main()
