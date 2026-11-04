"""Offline tests for Markdown structure; no remote PR is created."""

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_pr_body import inspect_body, main


COMPLETE = """## Summary\nAdds a focused example.\n\n## Motivation\nThe issue asks for clearer guidance.\n\n## Changes\nUpdated the guide and checked links.\n\n## Validation\n`python -m unittest` passed.\n\n## Risks and limitations\nNo runtime code changed; links still require periodic review.\n\n## Review focus\nPlease check the workflow and scope.\n"""


class PullRequestBodyTests(unittest.TestCase):
    def test_complete_body_passes(self):
        self.assertEqual(inspect_body(COMPLETE), [])

    def test_template_placeholders_are_reported(self):
        path = Path(__file__).resolve().parents[1] / "pull-request-body-template.md"
        findings = inspect_body(path.read_text(encoding="utf-8"))
        self.assertEqual(sum("placeholder" in item for item in findings), 6)

    def test_missing_and_empty_sections_are_reported(self):
        findings = inspect_body("## Summary\nA change.\n## Validation\n\n")
        self.assertTrue(any("empty" in item.lower() for item in findings))
        self.assertTrue(any("Missing required section" in item for item in findings))

    def test_duplicate_section_is_reported(self):
        findings = inspect_body(COMPLETE + "\n## Summary\nRepeated.\n")
        self.assertTrue(any("duplicate section" in item for item in findings))

    def test_top_level_title_does_not_fill_summary(self):
        body = COMPLETE.replace("## Summary\nAdds a focused example.", "## Summary\n# PR title")
        findings = inspect_body(body)
        self.assertTrue(any("Section '## Summary' is empty." == item for item in findings))

    def test_cli_exit_codes_for_valid_and_unreadable_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "body.md"
            path.write_text(COMPLETE, encoding="utf-8")
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(main([str(path)]), 0)
            self.assertIn("does not verify tests", stdout.getvalue())
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(Path(directory) / "missing.md")]), 2)


if __name__ == "__main__":
    unittest.main()
