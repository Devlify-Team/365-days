"""Offline unit tests for the side-effect-free notebook link builder."""

import contextlib
import io
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from share_links import build_links, main


class ShareLinksTests(unittest.TestCase):
    def test_builds_github_nbviewer_and_binder_links(self):
        links = build_links("my-team/notebooks", "reports/quick-start.ipynb")
        self.assertEqual(links["GitHub"], "https://github.com/my-team/notebooks/blob/main/reports/quick-start.ipynb")
        self.assertEqual(links["NBViewer"], "https://nbviewer.org/github/my-team/notebooks/blob/main/reports/quick-start.ipynb")
        parts = urlsplit(links["Binder"])
        self.assertEqual(parts.netloc, "mybinder.org")
        self.assertEqual(parts.path, "/v2/gh/my-team/notebooks/main")
        self.assertEqual(parse_qs(parts.query)["filepath"], ["/reports/quick-start.ipynb"])

    def test_encodes_spaces_and_branch_paths(self):
        links = build_links("team/repo", "notebooks/month one.ipynb", "feature/share-demo")
        self.assertIn("feature%2Fshare-demo", links["GitHub"])
        self.assertIn("month%20one.ipynb", links["GitHub"])
        self.assertEqual(parse_qs(urlsplit(links["Binder"]).query)["filepath"], ["/notebooks/month one.ipynb"])

    def test_rejects_malformed_repos_paths_and_refs(self):
        cases = [
            ("owner/repo?x=1", "n.ipynb", "main"),
            ("owner/repo", "../secret.ipynb", "main"),
            ("owner/repo", "/n.ipynb", "main"),
            ("owner/repo", "docs/readme.md", "main"),
            ("owner/repo", "docs\\file.ipynb", "main"),
            ("owner/repo", "n.ipynb", "../main"),
        ]
        for repo, path, ref in cases:
            with self.subTest(repo=repo, path=path, ref=ref), self.assertRaises(ValueError):
                build_links(repo, path, ref)

    def test_cli_prints_all_three_links_without_publishing(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["--repo", "org/repo", "--path", "demo.ipynb"])
        self.assertEqual(result, 0)
        self.assertIn("GitHub: https://github.com/org/repo/blob/main/demo.ipynb", output.getvalue())
        self.assertIn("NBViewer:", output.getvalue())
        self.assertIn("Binder:", output.getvalue())
        self.assertIn("does not publish", output.getvalue())


if __name__ == "__main__":
    unittest.main()
