"""Tests for static Shields/Badgen and GitHub workflow badge markup."""

import contextlib
import io
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from badge_audit import audit_text, main


class BadgeAuditTests(unittest.TestCase):
    def test_descriptive_static_badges_pass(self):
        text = """[![Documentation: Markdown](https://img.shields.io/badge/docs-Markdown-blue)](https://example.org/docs)
![Runtime dependencies: none](https://badgen.net/badge/dependencies/none/green)
"""
        count, findings = audit_text(text)
        self.assertEqual(count, 2)
        self.assertEqual(findings, [])

    def test_real_github_actions_badge_is_detected(self):
        count, findings = audit_text(
            "![Latest workflow result](https://github.com/team/project/actions/workflows/ci.yml/badge.svg?branch=main)"
        )
        self.assertEqual(count, 1)
        self.assertEqual(findings, [])

    def test_empty_and_generic_alt_text_are_reported(self):
        count, findings = audit_text(
            "![ ](https://img.shields.io/badge/docs-Markdown-blue)\n"
            "![Badge](https://img.shields.io/badge/coverage-95%25-green)\n"
        )
        self.assertEqual(count, 2)
        self.assertEqual(len(findings), 2)
        self.assertTrue(any("empty alt" in item for item in findings))
        self.assertTrue(any("generic" in item for item in findings))

    def test_repository_placeholders_are_reported(self):
        count, findings = audit_text(
            "![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)"
        )
        self.assertEqual(count, 1)
        self.assertTrue(any("placeholder" in item for item in findings))

    def test_example_images_in_fenced_code_are_ignored(self):
        count, findings = audit_text(
            "```markdown\n![Badge](https://img.shields.io/badge/a-b-blue)\n```\n"
            "![Diagram](https://example.org/diagram.png)"
        )
        self.assertEqual((count, findings), (0, []))

    def test_missing_file_and_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text("![Docs](https://img.shields.io/badge/docs-Markdown-blue)\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([str(path)]), 0)
            self.assertIn("1 badge(s)", output.getvalue())
            path.write_text("![ ](https://img.shields.io/badge/docs-Markdown-blue)\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(path)]), 1)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(Path(directory) / "missing.md")]), 2)


if __name__ == "__main__":
    unittest.main()
