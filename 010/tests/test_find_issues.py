"""Offline tests for the read-only issue search helper."""

import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import find_issues


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


class FinderTests(unittest.TestCase):
    def test_default_query_is_open_issue_and_label(self):
        self.assertEqual(find_issues.make_query(), 'is:issue is:open label:"good first issue"')

    def test_language_and_repo_filters(self):
        query = find_issues.make_query("C++", "octo-cat/project_2")
        self.assertEqual(query, 'is:issue is:open label:"good first issue" language:C++ repo:octo-cat/project_2')

    def test_rejects_invalid_qualifiers_and_limits(self):
        with self.assertRaises(ValueError):
            find_issues.make_query("Python repo:someone/else")
        with self.assertRaises(ValueError):
            find_issues.make_query(repository="not-a-repository")
        for invalid in (0, 21, True, "5"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                find_issues.search_issues(limit=invalid, opener=lambda *a, **k: None)

    def test_search_builds_encoded_read_only_request(self):
        observed = {}
        result = {"total_count": 1, "items": [{"title": "Docs typo", "number": 8}]}

        def opener(request, timeout):
            observed["url"] = request.full_url
            observed["method"] = request.get_method()
            observed["headers"] = request.headers
            observed["timeout"] = timeout
            return FakeResponse(result)

        total, items = find_issues.search_issues("Python", "org/repo", 3, opener)
        query = parse_qs(urlsplit(observed["url"]).query)
        self.assertEqual(total, 1)
        self.assertEqual(items[0]["title"], "Docs typo")
        self.assertIn('label:"good first issue"', query["q"][0])
        self.assertIn("language:Python", query["q"][0])
        self.assertIn("repo:org/repo", query["q"][0])
        self.assertEqual(query["per_page"], ["3"])
        self.assertEqual(observed["method"], "GET")
        self.assertEqual(observed["timeout"], 15)
        self.assertNotIn("Authorization", observed["headers"])

    def test_format_displays_source_link_update_and_labels(self):
        text = find_issues.format_issue({
            "title": "Fix docs\nwording",
            "number": 12,
            "html_url": "https://github.com/org/repo/issues/12",
            "repository_url": "https://api.github.com/repos/org/repo",
            "updated_at": "2026-10-28T04:00:00Z",
            "labels": [{"name": "good first issue"}],
        })
        self.assertIn("org/repo #12: Fix docs wording", text)
        self.assertIn("https://github.com/org/repo/issues/12", text)
        self.assertIn("good first issue", text)

    def test_cli_output_is_clear_and_never_assigns(self):
        fake = (2, [{"title": "Docs", "number": 4, "html_url": "https://github.com/x/y/issues/4"}])
        output = io.StringIO()
        with patch("find_issues.search_issues", return_value=fake):
            with patch("sys.stdout", output):
                self.assertEqual(find_issues.main(["--language", "Python", "--limit", "1"]), 0)
        self.assertIn("showing 1", output.getvalue())
        self.assertIn("read-only", output.getvalue())
        self.assertNotIn("assign me", output.getvalue().lower())

    def test_cli_surfaces_rate_limit_errors(self):
        output = io.StringIO()
        with patch("find_issues.search_issues", side_effect=ValueError("rate limit reached")):
            with patch("sys.stderr", output):
                self.assertEqual(find_issues.main([]), 1)
        self.assertIn("rate limit reached", output.getvalue())


if __name__ == "__main__":
    unittest.main()
