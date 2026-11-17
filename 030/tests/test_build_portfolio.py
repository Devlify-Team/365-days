import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_portfolio import build_portfolio, load_portfolio


class BuildPortfolioTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.project_dir = self.root / "030"
        self.project_dir.mkdir()
        self.target = self.root / "001"
        self.target.mkdir()
        self.manifest = self.project_dir / "portfolio.json"
        self.data = {
            "title": "Demo portfolio",
            "repository": "team/sample-projects",
            "summary": "A verified portfolio summary.",
            "projects": [
                {
                    "title": "Example project",
                    "focus": "Testing",
                    "description": "A concise, evidence-based project description.",
                    "path": "../001/",
                }
            ],
        }
        self.write_manifest()

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_manifest(self):
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")

    def test_builds_markdown_with_local_project_and_repository_links(self):
        output = build_portfolio(self.manifest)
        content = output.read_text(encoding="utf-8")
        self.assertIn("# Demo portfolio", content)
        self.assertIn("https://github.com/team/sample-projects", content)
        self.assertIn("### [Example project](../001/)", content)
        self.assertIn("A concise, evidence-based project description.", content)

    def test_rejects_duplicate_project_paths(self):
        self.data["projects"].append(dict(self.data["projects"][0]))
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "duplicate project path"):
            load_portfolio(self.manifest)

    def test_rejects_missing_project_target(self):
        self.data["projects"][0]["path"] = "../missing/"
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "does not exist"):
            load_portfolio(self.manifest)

    def test_rejects_project_path_outside_repository(self):
        self.data["projects"][0]["path"] = "../../outside/"
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "inside this repository"):
            load_portfolio(self.manifest)

    def test_rejects_invalid_repository_identifier(self):
        self.data["repository"] = "not-a-repository-url"
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "OWNER/REPOSITORY"):
            load_portfolio(self.manifest)

    def test_does_not_overwrite_manifest(self):
        with self.assertRaisesRegex(ValueError, "cannot overwrite"):
            build_portfolio(self.manifest, self.manifest)


if __name__ == "__main__":
    unittest.main()
