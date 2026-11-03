"""Local tests for showcase metadata and project README paths."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_showcase import load_manifest, validate_manifest


def project(number="001", **updates):
    entry = {
        "number": number,
        "title": "Example project",
        "topic": "Testing",
        "description": "Metadata-only test fixture.",
        "readme": f"../../{number}/README.md",
    }
    entry.update(updates)
    return entry


class ShowcaseTests(unittest.TestCase):
    def test_real_showcase_manifest_links_to_all_existing_projects(self):
        root = Path(__file__).resolve().parents[2]
        count, findings = load_manifest(Path(__file__).resolve().parents[1] / "site" / "projects.json", root)
        self.assertEqual(count, 15)
        self.assertEqual(findings, [])

    def test_duplicate_numbers_and_extra_fields_fail(self):
        root = Path(__file__).resolve().parents[2]
        _, findings = validate_manifest({"projects": [project(), project(extra="bad")]}, root)
        self.assertTrue(any("repeats project number" in item for item in findings))
        self.assertTrue(any("unexpected keys" in item for item in findings))

    def test_unpadded_numbers_and_wrong_readme_path_fail(self):
        root = Path(__file__).resolve().parents[2]
        _, findings = validate_manifest({"projects": [project(number="1", readme="../../001/README.md")]}, root)
        self.assertTrue(any("three-digit" in item for item in findings))
        self.assertTrue(any("README path" in item for item in findings))

    def test_missing_target_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "016" / "site").mkdir(parents=True)
            _, findings = validate_manifest({"projects": [project("007")]}, root)
            self.assertTrue(any("does not exist" in item for item in findings))

    def test_loader_reports_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text("{broken", encoding="utf-8")
            _, findings = load_manifest(path, directory)
            self.assertTrue(any("Invalid JSON" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
