#!/usr/bin/env python3
"""Check whether a pull request body gives reviewers the required context."""

import argparse
from pathlib import Path
import re
import sys

REQUIRED = (
    "Summary",
    "Motivation",
    "Changes",
    "Validation",
    "Risks and limitations",
    "Review focus",
)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|FILL\s+IN|PLACEHOLDER)\b", re.IGNORECASE)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def inspect_body(markdown):
    """Return actionable findings for missing, duplicate, empty or unfinished sections."""
    sections = {}
    current = None
    findings = []
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        match = HEADING.match(line)
        if match:
            level = len(match.group(1))
            if level == 1:
                current = None
                continue
            if level > 2:
                if current is not None:
                    sections[current].append(line)
                continue
            name = match.group(2).strip().rstrip("#").strip()
            current = name.casefold()
            if current in sections:
                findings.append(f"Line {line_number}: duplicate section '## {name}'.")
            else:
                sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)

    for title in REQUIRED:
        key = title.casefold()
        if key not in sections:
            findings.append(f"Missing required section: '## {title}'.")
            continue
        text = HTML_COMMENT.sub("", "\n".join(sections[key])).strip()
        if not text:
            findings.append(f"Section '## {title}' is empty.")
        elif PLACEHOLDER.search(text):
            findings.append(f"Section '## {title}' still contains a placeholder.")
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("body", type=Path, help="Markdown file containing the proposed PR description")
    args = parser.parse_args(argv)
    try:
        content = args.body.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Could not read pull request body: {error}", file=sys.stderr)
        return 2
    findings = inspect_body(content)
    if findings:
        print(f"Draft needs work: {len(findings)} finding(s).", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print("Draft contains all required reviewer-context sections and no section placeholders.")
    print("This check does not verify tests, approvals, repository rules, or merge eligibility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
