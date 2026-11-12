import tempfile
import unittest
from pathlib import Path

from scripts.check_markdown import check_markdown


class CheckMarkdownTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "target.md").write_text("# Target\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_markdown(self, content):
        path = self.root / "sample.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_accepts_heading_balanced_fence_and_existing_local_link(self):
        path = self.write_markdown(
            "# Guide\n\n[Target](target.md)\n\n```bash\necho ok\n```\n"
        )
        self.assertEqual(check_markdown(path), [])

    def test_reports_missing_heading_and_unclosed_fence(self):
        path = self.write_markdown("No heading here\n\n```python\nprint('x')\n")
        errors = check_markdown(path)
        self.assertTrue(any("exactly one top-level heading" in error for error in errors))
        self.assertTrue(any("unclosed fenced code block" in error for error in errors))

    def test_reports_missing_local_link_target(self):
        path = self.write_markdown("# Guide\n\n[Missing](missing.md)\n")
        errors = check_markdown(path)
        self.assertTrue(any("local link target does not exist" in error for error in errors))

    def test_ignores_external_links(self):
        path = self.write_markdown("# Guide\n\n[Website](https://example.com)\n")
        self.assertEqual(check_markdown(path), [])


if __name__ == "__main__":
    unittest.main()
