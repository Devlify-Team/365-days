"""Unit tests for the standard-library README quality checker."""

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from readme_audit import audit_text, main


GOOD = """# Sample project
A short description for someone seeing the project for the first time.

## Overview
It prints a greeting.

## Getting Started
Run it with Python.

## Usage
```sh
python3 hello.py
```

## Testing
Run the test command.

## Help
Ask the maintainer.
"""


class ReadmeAuditTests(unittest.TestCase):
    def test_complete_readme_passes(self):
        self.assertEqual(audit_text(GOOD), [])

    def test_reports_missing_sections(self):
        findings = audit_text("# Tiny\nOne line.\n")
        self.assertTrue(any("Overview" in item for item in findings))
        self.assertTrue(any("Getting Started" in item for item in findings))
        self.assertTrue(any("Usage" in item for item in findings))

    def test_reports_description_and_unclosed_fence(self):
        text = "# Title\n## Overview\n```python\nprint('hi')\n"
        findings = audit_text(text)
        self.assertTrue(any("description" in item.lower() for item in findings))
        self.assertTrue(any("code block" in item for item in findings))

    def test_reports_explicit_unfinished_marker_outside_code(self):
        findings = audit_text(GOOD + "\n[[TODO]]\n")
        self.assertTrue(any("unfinished marker" in item for item in findings))

    def test_reports_readme_template_placeholders(self):
        findings = audit_text(GOOD + "\n[PROJECT_NAME]\n[Explain the audience.]\n")
        self.assertGreaterEqual(sum("unfinished marker" in item for item in findings), 2)

    def test_ignores_markers_and_fake_links_inside_code(self):
        text = GOOD + "\n```text\n[[TODO]] [example](missing.txt)\n```\n"
        self.assertEqual(audit_text(text), [])

    def test_checks_local_links_but_allows_urls_and_anchors(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "guide.md").write_text("Guide", encoding="utf-8")
            text = GOOD + "\n[Guide](guide.md) [Missing](absent.md) " \
                   "[Heading](#usage) [Web](https://example.test)\n"
            findings = audit_text(text, directory)
            local_errors = [item for item in findings if "local link target" in item]
            self.assertEqual(len(local_errors), 1)
            self.assertIn("absent.md", local_errors[0])

    def test_cli_exit_codes_and_file_error(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(GOOD, encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([str(readme)]), 0)
            self.assertIn("passed", output.getvalue())
            readme.write_text("# incomplete\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(readme)]), 1)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(Path(directory) / "missing.md")]), 2)


if __name__ == "__main__":
    unittest.main()
