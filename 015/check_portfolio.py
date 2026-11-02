#!/usr/bin/env python3
"""Validate a portfolio manifest; never reads or analyzes project datasets."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_TEXT = ("title", "summary", "data_source", "data_rights", "limitations")
ENTRY_KEYS = frozenset(("slug", "title", "summary", "repository_url", "data_source",
                        "data_rights", "limitations", "reviewed_for_publication"))


def validate_portfolio(document):
    """Return (entry_count, findings) for the publication manifest."""
    findings = []
    if not isinstance(document, dict):
        return 0, ["Manifest must be a JSON object."]
    projects = document.get("projects")
    if not isinstance(projects, list):
        return 0, ["Manifest must contain a projects list."]

    seen_slugs = set()
    for index, project in enumerate(projects, start=1):
        where = f"Project {index}"
        if not isinstance(project, dict):
            findings.append(f"{where} must be an object.")
            continue
        extra_keys = set(project) - ENTRY_KEYS
        if extra_keys:
            findings.append(f"{where} has unexpected key(s): {', '.join(sorted(extra_keys))}.")
        slug = project.get("slug")
        if not isinstance(slug, str) or not SLUG.fullmatch(slug):
            findings.append(f"{where} needs a lowercase hyphenated slug.")
        elif slug in seen_slugs:
            findings.append(f"{where} repeats slug {slug!r}.")
        else:
            seen_slugs.add(slug)

        for field in REQUIRED_TEXT:
            value = project.get(field)
            if not isinstance(value, str) or not value.strip():
                findings.append(f"{where} needs non-empty {field!r} text.")

        repository_url = project.get("repository_url")
        if not isinstance(repository_url, str) or not repository_url.strip():
            findings.append(f"{where} needs a repository_url.")
        else:
            try:
                parsed = urlsplit(repository_url)
                valid_url = (parsed.scheme == "https" and bool(parsed.hostname)
                             and not parsed.username and not parsed.password)
            except ValueError:
                valid_url = False
            if not valid_url:
                findings.append(f"{where} repository_url must be a public-safe HTTPS URL without embedded credentials.")
        if project.get("reviewed_for_publication") is not True:
            findings.append(f"{where} must pass publication review before it is listed.")
    return len(projects), findings


def load_manifest(path):
    """Read and validate the manifest's JSON, returning its projects and findings."""
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return 0, [f"Could not read manifest: {error}"]
    except json.JSONDecodeError as error:
        return 0, [f"Invalid JSON: {error}"]
    return validate_portfolio(document)


def main(argv=None):
    default_path = Path(__file__).parent / "site" / "projects.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path, default=default_path,
                        help="portfolio JSON file (default: site/projects.json)")
    args = parser.parse_args(argv)
    count, findings = load_manifest(args.manifest)
    if findings:
        print(f"Portfolio check failed: {len(findings)} finding(s).", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    if count == 0:
        print("Portfolio manifest is valid and empty. Add a real, reviewed case study when ready.")
    else:
        print(f"Portfolio manifest is valid: {count} reviewed case study/case studies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
