#!/usr/bin/env python3
"""Lightweight structural and clean-output check for an .ipynb JSON file."""

import argparse
import json
from pathlib import Path
import sys

CELL_TYPES = {"markdown", "code", "raw"}


def audit_document(document):
    """Return (cell_count, findings) for basic structure and clean-output rules."""
    findings = []
    if not isinstance(document, dict):
        return 0, ["Notebook root must be a JSON object."]
    if document.get("nbformat") != 4:
        findings.append("Expected notebook format version 4.")
    if type(document.get("nbformat_minor")) is not int:
        findings.append("Missing or invalid notebook format minor version.")
    if not isinstance(document.get("metadata"), dict):
        findings.append("Notebook metadata must be an object.")
    cells = document.get("cells")
    if not isinstance(cells, list):
        return 0, findings + ["Notebook cells must be a list."]

    identifiers = set()
    for index, cell in enumerate(cells):
        where = f"Cell {index + 1}"
        if not isinstance(cell, dict):
            findings.append(f"{where} must be an object.")
            continue
        cell_type = cell.get("cell_type")
        if cell_type not in CELL_TYPES:
            findings.append(f"{where} has unknown type {cell_type!r}.")
        if not isinstance(cell.get("metadata"), dict):
            findings.append(f"{where} metadata must be an object.")
        source = cell.get("source")
        if not (isinstance(source, str) or (isinstance(source, list) and all(isinstance(line, str) for line in source))):
            findings.append(f"{where} source must be text or a list of text lines.")
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not cell_id:
            findings.append(f"{where} needs a non-empty cell id.")
        elif cell_id in identifiers:
            findings.append(f"{where} repeats cell id {cell_id!r}.")
        else:
            identifiers.add(cell_id)
        if cell_type == "code":
            if "execution_count" not in cell or cell["execution_count"] is not None:
                findings.append(f"{where} has an execution count; clear it before committing.")
            if cell.get("outputs") != []:
                findings.append(f"{where} has saved outputs; clear them before committing.")
    return len(cells), findings


def audit_path(path):
    """Load a notebook as UTF-8 JSON and apply the lightweight audit."""
    path = Path(path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return 0, [f"Could not read notebook: {error}"]
    except json.JSONDecodeError as error:
        return 0, [f"Invalid notebook JSON: {error}"]
    return audit_document(document)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path, help="Notebook JSON (.ipynb) to check")
    args = parser.parse_args(argv)
    cells, findings = audit_path(args.notebook)
    if findings:
        print(f"Notebook audit failed: {len(findings)} finding(s).", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print(f"Notebook audit passed: {cells} cells; code execution counts are clear; no saved outputs.")
    print("This is a lightweight check, not the full nbformat schema validator.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
