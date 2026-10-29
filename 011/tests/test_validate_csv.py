"""Offline tests for the scaffold's streaming CSV schema check."""

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ds_template.validate_csv import main, validate_csv


class ValidateCsvTests(unittest.TestCase):
    def write_csv(self, directory, content):
        path = Path(directory) / "fixture.csv"
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_csv_counts_data_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "id,value\n1,alpha\n2,beta\n")
            self.assertEqual(validate_csv(path, ["id", "value"]), (2, []))

    def test_accepts_bom_and_skips_blank_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "\ufeffid,value\n\n1,alpha\n")
            self.assertEqual(validate_csv(path, ["id", "value"]), (1, []))

    def test_reports_missing_duplicate_and_blank_headers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "id,id,\n1,alpha,\n")
            rows, findings = validate_csv(path, ["id", "value"])
            self.assertEqual(rows, 1)
            self.assertTrue(any("blank column" in item for item in findings))
            self.assertTrue(any("Duplicate" in item for item in findings))
            self.assertTrue(any("Missing required" in item for item in findings))

    def test_reports_malformed_row_width(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "id,value\n1,alpha\n2\n")
            rows, findings = validate_csv(path, ["id", "value"])
            self.assertEqual(rows, 2)
            self.assertTrue(any("expected 2 fields, found 1" in item for item in findings))

    def test_reports_malformed_csv_quoting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, 'id,value\n1,"unterminated\n')
            rows, findings = validate_csv(path, ["id", "value"])
            self.assertEqual(rows, 0)
            self.assertTrue(any("CSV parse error" in item for item in findings))

    def test_reports_empty_file_and_rejects_invalid_requirements(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "")
            self.assertEqual(validate_csv(path, ["id"]), (0, ["CSV is empty; expected a header row."]))
            for required in ([], ["   "], ["id", "id"]):
                with self.subTest(required=required), self.assertRaises(ValueError):
                    validate_csv(path, required)
            with self.assertRaises(ValueError):
                validate_csv(Path(directory) / "missing.csv", ["id"])

    def test_cli_reports_success_and_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, "id,value\n1,alpha\n")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([str(path), "--required-columns", "id,value"]), 0)
            self.assertIn("1 data row(s)", output.getvalue())
            path.write_text("id\n1\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(path), "--required-columns", "id,value"]), 1)


if __name__ == "__main__":
    unittest.main()
