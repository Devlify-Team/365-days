import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_gallery import generate_gallery, load_projects


class BuildGalleryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.readme = self.root / "sample" / "README.md"
        self.readme.parent.mkdir()
        self.readme.write_text(
            "# Sample Project\n\nA useful first paragraph for the gallery.\n\n## Details\n\nMore text.\n",
            encoding="utf-8",
        )
        self.manifest = self.root / "projects.json"
        self.write_manifest([{"id": "sample-project", "category": "Tools", "readme": "sample/README.md"}])

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_manifest(self, entries):
        self.manifest.write_text(json.dumps(entries), encoding="utf-8")

    def test_generates_title_summary_and_relative_link(self):
        output = generate_gallery(self.manifest)
        text = output.read_text(encoding="utf-8")
        self.assertIn("## Tools", text)
        self.assertIn("### [Sample Project](sample/README.md)", text)
        self.assertIn("A useful first paragraph for the gallery.", text)

    def test_duplicate_ids_are_rejected(self):
        entry = {"id": "sample-project", "category": "Tools", "readme": "sample/README.md"}
        self.write_manifest([entry, entry])
        with self.assertRaisesRegex(ValueError, "duplicate project id"):
            load_projects(self.manifest)

    def test_paths_cannot_escape_manifest_directory(self):
        self.write_manifest([{"id": "outside", "category": "Tools", "readme": "../outside.md"}])
        with self.assertRaisesRegex(ValueError, "must stay inside"):
            load_projects(self.manifest)

    def test_output_cannot_replace_source_readme(self):
        with self.assertRaisesRegex(ValueError, "cannot overwrite"):
            generate_gallery(self.manifest, self.readme)

    def test_readme_requires_title_and_summary(self):
        self.readme.write_text("Just text\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "level-one README title"):
            load_projects(self.manifest)


if __name__ == "__main__":
    unittest.main()
