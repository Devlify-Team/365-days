import unittest
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PROJECT_ROOT / "docs"


def navigation_pages(items):
    """Yield the page paths recursively from MkDocs' navigation data."""
    for item in items:
        if isinstance(item, str):
            yield item
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    yield value
                elif isinstance(value, list):
                    yield from navigation_pages(value)


class DocumentationSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = yaml.safe_load((PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8"))

    def test_site_has_a_name_and_navigation(self):
        self.assertTrue(self.config.get("site_name"))
        self.assertTrue(self.config.get("nav"))

    def test_every_navigation_target_exists(self):
        pages = list(navigation_pages(self.config["nav"]))
        self.assertTrue(pages)
        for page in pages:
            with self.subTest(page=page):
                self.assertTrue((DOCS_ROOT / page).is_file())

    def test_every_navigation_target_is_unique(self):
        pages = list(navigation_pages(self.config["nav"]))
        self.assertEqual(len(pages), len(set(pages)))

    def test_homepage_has_a_single_top_level_heading(self):
        text = (DOCS_ROOT / "index.md").read_text(encoding="utf-8")
        headings = [line for line in text.splitlines() if line.startswith("# ")]
        self.assertEqual(len(headings), 1)


if __name__ == "__main__":
    unittest.main()
