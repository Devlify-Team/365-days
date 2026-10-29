"""Check a CSV header and row shape without loading the file into memory."""

import argparse
import csv
from pathlib import Path
import sys


def validate_csv(path, required_columns):
    """Return (data_rows_checked, findings) for a CSV with a header row."""
    required = [column.strip() for column in required_columns if column.strip()]
    if not required:
        raise ValueError("Provide at least one required column name")
    if len(set(required)) != len(required):
        raise ValueError("Required column names must be unique")

    path = Path(path)
    findings = []
    try:
        handle = path.open("r", newline="", encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"Cannot open CSV file: {error}") from error

    try:
        with handle:
            reader = csv.reader(handle, strict=True)
            try:
                header = next(reader)
            except StopIteration:
                return 0, ["CSV is empty; expected a header row."]
            except csv.Error as error:
                return 0, [f"CSV parse error near line {reader.line_num}: {error}"]
            if not header:
                return 0, ["CSV header row is empty."]
            if any(not name.strip() for name in header):
                findings.append("CSV header contains a blank column name.")
            duplicates = sorted({name for name in header if header.count(name) > 1})
            if duplicates:
                findings.append("Duplicate header columns: " + ", ".join(duplicates))
            missing = [name for name in required if name not in header]
            if missing:
                findings.append("Missing required columns: " + ", ".join(missing))
            rows_checked = 0
            try:
                for row in reader:
                    if not row:
                        continue
                    line_number = reader.line_num
                    rows_checked += 1
                    if len(row) != len(header):
                        findings.append(
                            f"Line {line_number}: expected {len(header)} fields, found {len(row)}."
                        )
                        break
            except csv.Error as error:
                findings.append(f"CSV parse error near line {reader.line_num}: {error}")
    except UnicodeError as error:
        raise ValueError(f"CSV is not valid UTF-8 text: {error}") from error
    return rows_checked, findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV file to inspect (must include a header row)")
    parser.add_argument("--required-columns", required=True, help="Comma-separated header columns required by your task")
    args = parser.parse_args(argv)
    try:
        required = args.required_columns.split(",")
        rows, findings = validate_csv(args.csv_file, required)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if findings:
        print(f"CSV check: {len(findings)} finding(s); {rows} data row(s) inspected.")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"CSV check passed: {rows} data row(s); required columns are present.")
    print("This schema check is not a full data-quality or analytical validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
