#!/usr/bin/env python3
"""Find open GitHub issues carrying the `good first issue` label.

The search is read-only and unauthenticated. Results are leads to review, not
recommendations; this tool never assigns issues or submits comments.
"""

import argparse
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.github.com/search/issues"
USER_AGENT = "365-days-day010-good-first-issue-finder"


def make_query(language=None, repository=None):
    """Build a constrained GitHub Search query from optional qualifiers."""
    parts = ['is:issue', 'is:open', 'label:"good first issue"']
    if language:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9+#_.-]*", language):
            raise ValueError("Language must be a single language name, such as Python or C++")
        parts.append(f"language:{language}")
    if repository:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repository):
            raise ValueError("Repository must use the owner/name format")
        parts.append(f"repo:{repository}")
    return " ".join(parts)


def search_issues(language=None, repository=None, limit=5, opener=urlopen):
    """Return (total_count, items) from GitHub's public Search Issues API."""
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("Limit must be an integer from 1 to 20")
    query = make_query(language, repository)
    url = API + "?" + urlencode({
        "q": query,
        "per_page": limit,
        "sort": "updated",
        "order": "desc",
    })
    request = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
    })
    try:
        with opener(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        if error.code == 403 or error.code == 429:
            raise ValueError("GitHub Search API rate limit or access limit reached; wait before trying again") from error
        raise ValueError(f"GitHub Search API returned HTTP {error.code}") from error
    except URLError as error:
        raise ValueError(f"Could not reach GitHub Search API: {error.reason}") from error
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("GitHub Search API returned an unreadable response") from error
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError("GitHub Search API response did not include an issue list")
    return int(payload.get("total_count", 0)), payload["items"]


def format_issue(issue):
    """Format one result without implying that its label guarantees suitability."""
    url = issue.get("html_url", "(no web link returned)")
    title = issue.get("title", "(untitled issue)").replace("\n", " ").strip()
    number = issue.get("number", "?")
    repo_url = issue.get("repository_url", "")
    repository = "/".join(repo_url.rstrip("/").split("/")[-2:]) if repo_url else "unknown repository"
    updated = issue.get("updated_at")
    lines = [f"- {repository} #{number}: {title}", f"  {url}"]
    if updated:
        lines.append(f"  Updated: {updated}")
    labels = [label.get("name", "") for label in issue.get("labels", []) if label.get("name")]
    if labels:
        lines.append("  Labels: " + ", ".join(labels))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", help="Limit to a GitHub language, such as Python or C++")
    parser.add_argument("--repo", help="Limit to one repository in owner/name form")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results to display (1-20; default: 5)")
    args = parser.parse_args(argv)
    try:
        total, items = search_issues(args.language, args.repo, args.limit)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"GitHub returned {total} open issue(s) matching this label; showing {len(items)}.")
    if items:
        print("\n".join(format_issue(item) for item in items))
    else:
        print("No current matches. Try another language or browse the linked directories in the README.")
    print("\nReview each issue and its project guidance yourself; labels do not guarantee beginner fit.")
    print("This tool is read-only. It does not assign issues, comment, or create pull requests.")
    print("Unauthenticated GitHub issue-search requests are rate-limited.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
