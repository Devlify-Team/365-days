"""Standard-library tests for notebook structure and clean-output checks."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notebook_audit import audit_document, audit_path


def notebook(cells=None):
    return {
        "cells": cells if cells is not None else [
            {"cell_type": "markdown", "id": "intro", "metadata": {}, "source": "Title"},
            {"cell_type": "code", "id": "setup", "metadata": {}, "execution_count": None, "outputs": [], "source": "print('ready')"},
        ],
        "metadata": {"kernelspec": {"name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


class NotebookAuditTests(unittest.TestCase):
    def test_clean_notebook_passes(self):
        count, findings = audit_document(notebook())
        self.assertEqual(count, 2)
        self.assertEqual(findings, [])

    def test_saved_outputs_and_execution_counts_fail(self):
        doc = notebook()
        doc["cells"][1]["execution_count"] = 2
        doc["cells"][1]["outputs"] = [{"output_type": "stream", "name": "stdout", "text": "private"}]
        _, findings = audit_document(doc)
        self.assertTrue(any("execution count" in item for item in findings))
        self.assertTrue(any("saved outputs" in item for item in findings))

    def test_code_cell_must_explicitly_set_null_execution_count(self):
        doc = notebook()
        del doc["cells"][1]["execution_count"]
        _, findings = audit_document(doc)
        self.assertTrue(any("execution count" in item for item in findings))

    def test_unknown_cell_type_and_duplicate_id_fail(self):
        doc = notebook([
            {"cell_type": "unknown", "id": "x", "metadata": {}, "source": ""},
            {"cell_type": "markdown", "id": "x", "metadata": {}, "source": ""},
        ])
        _, findings = audit_document(doc)
        self.assertTrue(any("unknown type" in item for item in findings))
        self.assertTrue(any("repeats cell id" in item for item in findings))

    def test_malformed_top_level_and_source_fail(self):
        doc = notebook()
        doc["cells"][0]["source"] = 7
        doc["metadata"] = []
        _, findings = audit_document(doc)
        self.assertTrue(any("source" in item for item in findings))
        self.assertTrue(any("metadata" in item for item in findings))

    def test_audit_path_reads_a_notebook_and_reports_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            good = Path(directory) / "good.ipynb"
            good.write_text(json.dumps(notebook()), encoding="utf-8")
            self.assertEqual(audit_path(good), (2, []))
            bad = Path(directory) / "bad.ipynb"
            bad.write_text("{not json", encoding="utf-8")
            _, findings = audit_path(bad)
            self.assertTrue(any("Invalid notebook JSON" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
