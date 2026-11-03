#!/usr/bin/env python3
"""Check showcase entries and their local project README targets."""

import argparse
import json
from pathlib import Path
import re
import sys

FIELDS = {"number", "title", "topic", "description", "readme"}
NUMBER = re.compile(r"^\d{3}$")


def validate_manifest(document, repository_root):
    """Return project count and validation messages for a manifest."""
    findings = []
    if not isinstance(document, dict) or not isinstance(document.get("projects"), list):
        return 0, ["Manifest must be an object containing a projects list."]
    root = Path(repository_root).resolve()
    site_dir = root / "016" / "site"
    seen = set()
    projects = document["projects"]
    for index, project in enumerate(projects, start=1):
        where = f"Project entry {index}"
        if not isinstance(project, dict):
            findings.append(f"{where} must be an object.")
            continue
        if set(project) != FIELDS:
            missing = sorted(FIELDS - set(project))
            extra = sorted(set(project) - FIELDS)
            if missing:
                findings.append(f"{where} is missing: {', '.join(missing)}.")
            if extra:
                findings.append(f"{where} has unexpected keys: {', '.join(extra)}.")
        number = project.get("number")
        if not isinstance(number, str) or not NUMBER.fullmatch(number):
            findings.append(f"{where} needs a three-digit zero-padded project number.")
        elif number in seen:
            findings.append(f"{where} repeats project number {number}.")
        else:
            seen.add(number)
        for field in ("title", "topic", "description"):
            value = project.get(field)
            if not isinstance(value, str) or not value.strip():
                findings.append(f"{where} needs non-empty {field!r} text.")
        expected = f"../../{number}/README.md" if isinstance(number, str) else None
        if project.get("readme") != expected:
            findings.append(f"{where} README path must point to that numbered folder's README.")
        else:
            target = (site_dir / project["readme"]).resolve()
            if not target.is_relative_to(root):
                findings.append(f"{where} README path escapes the repository.")
            elif not target.is_file():
                findings.append(f"{where} README target does not exist: {project['readme']}.")
    return len(projects), findings


def load_manifest(path, repository_root):
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return 0, [f"Could not read manifest: {error}"]
    except json.JSONDecodeError as error:
        return 0, [f"Invalid JSON: {error}"]
    return validate_manifest(document, repository_root)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path, default=Path(__file__).parent / "site" / "projects.json")
    args = parser.parse_args(argv)
    count, findings = load_manifest(args.manifest, Path(__file__).parent.parent)
    if findings:
        print(f"Showcase check failed: {len(findings)} finding(s).", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print(f"Showcase is valid: {count} projects link to existing README files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
