#!/usr/bin/env python3
"""Check reviewer-note structure; does not inspect code or submit a review."""

import argparse
from pathlib import Path
import re
import sys

REQUIRED = ("Decision", "Findings", "Evidence inspected", "Unreviewed scope")
OPTIONAL = ("Positive notes",)
H2 = re.compile(r"^##\s+(.+?)\s*#*\s*$")
H3 = re.compile(r"^###\s+(.+?)\s*#*\s*$")
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|FILL\s+IN|PLACEHOLDER)\b", re.IGNORECASE)
DECISIONS = {"approve", "comment", "request changes"}


def parse_sections(markdown):
    sections = {}
    current = None
    findings = []
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        match = H2.match(line)
        if match:
            title = match.group(1).strip().rstrip("#").strip()
            current = title.casefold()
            if current in sections:
                findings.append(f"Line {line_number}: duplicate section '## {title}'.")
            else:
                sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return sections, findings


def inspect_review(markdown):
    """Return actionable findings when a reviewer note is incomplete."""
    sections, findings = parse_sections(markdown)
    normalized = {}
    for title in REQUIRED:
        key = title.casefold()
        if key not in sections:
            findings.append(f"Missing required section: '## {title}'.")
            continue
        text = "\n".join(sections[key]).strip()
        normalized[key] = text
        if not text:
            findings.append(f"Section '## {title}' is empty.")
        elif PLACEHOLDER.search(text):
            findings.append(f"Section '## {title}' still contains a placeholder.")
    for title in OPTIONAL:
        text = "\n".join(sections.get(title.casefold(), [])).strip()
        if text and PLACEHOLDER.search(text):
            findings.append(f"Optional section '## {title}' still contains a placeholder.")

    decision = normalized.get("decision", "").strip().casefold()
    if decision and decision not in DECISIONS:
        findings.append("Decision must be Approve, Comment, or Request changes.")

    notes = normalized.get("findings", "").strip()
    if notes and notes.casefold() != "no findings.":
        blocks = []
        current_block = None
        for line in notes.splitlines():
            match = H3.match(line)
            if match:
                current_block = {"title": match.group(1), "lines": []}
                blocks.append(current_block)
            elif current_block is not None:
                current_block["lines"].append(line)
        if not blocks:
            findings.append("Findings must say 'No findings.' or use a '### Finding: ...' block.")
        for block in blocks:
            body = "\n".join(block["lines"])
            if not re.search(r"(?im)^\s*\*\*Impact:?\*\*\s*:?\s*", body):
                findings.append(f"Finding {block['title']!r} needs an Impact line.")
            if not re.search(r"(?im)^\s*\*\*Suggested action:?\*\*\s*:?\s*", body):
                findings.append(f"Finding {block['title']!r} needs a Suggested action line.")
            if PLACEHOLDER.search(body):
                findings.append(f"Finding {block['title']!r} still contains a placeholder.")
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path, help="Markdown reviewer-note file")
    args = parser.parse_args(argv)
    try:
        markdown = args.review.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Could not read review note: {error}", file=sys.stderr)
        return 2
    findings = inspect_review(markdown)
    if findings:
        print(f"Review note needs work: {len(findings)} finding(s).", file=sys.stderr)
        for item in findings:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("Review note structure is complete.")
    print("This check does not verify code correctness, evidence, approvals, or merge eligibility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
