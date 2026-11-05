"""Offline tests for reviewer-note structure; no project code is analyzed."""

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_review import inspect_review, main


COMPLETE = """## Decision
Request changes

## Findings
### Finding: Empty input crashes
**Impact:** An empty list raises an exception for a valid request.
**Suggested action:** Add a guard and a test for the empty case.

## Evidence inspected
Reviewed `paging.py` and the focused unit tests. Did not run integration tests.

## Unreviewed scope
I did not assess deployment or performance behavior.
"""

NO_FINDINGS = """## Decision
Approve

## Findings
No findings.

## Evidence inspected
Read every changed line and ran the unit tests.

## Unreviewed scope
None known.
"""


class ReviewNoteTests(unittest.TestCase):
    def test_complete_finding_note_passes(self):
        self.assertEqual(inspect_review(COMPLETE), [])

    def test_no_findings_is_an_allowed_explicit_outcome(self):
        self.assertEqual(inspect_review(NO_FINDINGS), [])

    def test_template_is_flagged_until_filled(self):
        template = Path(__file__).resolve().parents[1] / "review-note-template.md"
        findings = inspect_review(template.read_text(encoding="utf-8"))
        self.assertGreaterEqual(sum("placeholder" in item for item in findings), 4)

    def test_invalid_decision_and_incomplete_finding_are_reported(self):
        body = COMPLETE.replace("Request changes", "Maybe")
        body = body.replace("**Suggested action:** Add a guard and a test for the empty case.", "Suggested action missing.")
        findings = inspect_review(body)
        self.assertTrue(any("Decision must be" in item for item in findings))
        self.assertTrue(any("Suggested action line" in item for item in findings))

    def test_missing_and_duplicate_sections_are_reported(self):
        findings = inspect_review(NO_FINDINGS.replace("## Unreviewed scope\nNone known.\n", "") + "\n## Decision\nComment\n")
        self.assertTrue(any("Missing required section" in item for item in findings))
        self.assertTrue(any("duplicate section" in item for item in findings))

    def test_cli_exit_codes_and_scope_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.md"
            path.write_text(NO_FINDINGS, encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(main([str(path)]), 0)
            self.assertIn("does not verify code correctness", stdout.getvalue())
            path.write_text("## Decision\nTODO\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(path)]), 1)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(Path(directory) / "missing.md")]), 2)


if __name__ == "__main__":
    unittest.main()
