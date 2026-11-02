"""Offline metadata-only tests; no datasets or analysis results are included."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_portfolio import load_manifest, validate_portfolio


def entry(**updates):
    value = {
        "slug": "sample-review",
        "title": "Example case study",
        "summary": "Metadata-only test fixture.",
        "repository_url": "https://github.com/example/project",
        "data_source": "Public test fixture only; no dataset is read.",
        "data_rights": "Rights checked for this metadata fixture.",
        "limitations": "This tests the manifest structure only.",
        "reviewed_for_publication": True,
    }
    value.update(updates)
    return value


class PortfolioManifestTests(unittest.TestCase):
    def test_empty_portfolio_is_valid_without_fabricated_projects(self):
        count, findings = validate_portfolio({"projects": []})
        self.assertEqual(count, 0)
        self.assertEqual(findings, [])

    def test_complete_reviewed_case_study_metadata_passes(self):
        count, findings = validate_portfolio({"projects": [entry()]})
        self.assertEqual(count, 1)
        self.assertEqual(findings, [])

    def test_unreviewed_project_and_http_url_fail(self):
        count, findings = validate_portfolio({"projects": [entry(reviewed_for_publication=False,
                                                                  repository_url="http://example.org/project")]})
        self.assertEqual(count, 1)
        self.assertTrue(any("publication review" in item for item in findings))
        self.assertTrue(any("HTTPS URL" in item for item in findings))

    def test_extra_fields_and_malformed_https_url_fail(self):
        _, findings = validate_portfolio({"projects": [entry(extra_field="unexpected",
                                                               repository_url="https://[invalid")]})
        self.assertTrue(any("unexpected key" in item for item in findings))
        self.assertTrue(any("HTTPS URL" in item for item in findings))

    def test_required_disclosures_slug_and_duplicate_are_checked(self):
        first = entry(data_rights="", slug="Not-A-Slug")
        second = entry()
        third = entry()
        _, findings = validate_portfolio({"projects": [first, second, third]})
        self.assertTrue(any("data_rights" in item for item in findings))
        self.assertTrue(any("lowercase hyphenated slug" in item for item in findings))
        self.assertTrue(any("repeats slug" in item for item in findings))

    def test_manifest_loader_parses_json_and_reports_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps({"projects": []}), encoding="utf-8")
            self.assertEqual(load_manifest(path), (0, []))
            path.write_text("{invalid", encoding="utf-8")
            _, findings = load_manifest(path)
            self.assertTrue(any("Invalid JSON" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
