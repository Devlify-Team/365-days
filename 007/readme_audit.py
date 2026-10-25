#!/usr/bin/env python3
"""Check a README's basic structure, fenced code, placeholders and local links."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

REQUIRED_SECTIONS = {
    "overview": ("overview", "what it does", "purpose", "project description"),
    "getting started": ("getting started", "installation", "setup"),
    "usage": ("usage", "examples", "quick example"),
    "testing": ("testing", "tests", "test"),
    "help": ("help", "support", "contact", "troubleshooting"),
}
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
LINK = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")
PLACEHOLDER = re.compile(
    r"\[\[[^\]]+\]\]|\[(?:[A-Z][A-Z0-9_, /:-]*|"
    r"(?:Explain|Describe|State|Replace|Add|Provide|Choose|List|Install|Run|"
    r"Contact|Write|Set|Configure|Your)\b[^\]]*)\]"
)


def audit_text(text, base_dir="."):
    """Return actionable findings for README text; an empty list means it passes."""
    base = Path(base_dir)
    findings = []
    visible = []
    headings = []
    links = []
    fence_char = None
    fence_length = 0

    for number, line in enumerate(text.splitlines(), 1):
        fence = FENCE.match(line)
        if fence:
            token = fence.group(1)
            char, length = token[0], len(token)
            if fence_char is None:
                fence_char, fence_length = char, length
            elif char == fence_char and length >= fence_length and not line.strip()[length:].strip():
                fence_char, fence_length = None, 0
            visible.append("")
            continue
        if fence_char is not None:
            visible.append("")
            continue
        visible.append(line)
        placeholder = PLACEHOLDER.search(line)
        if placeholder:
            findings.append(f"Line {number}: replace unfinished marker {placeholder.group(0)}.")
        for match in LINK.finditer(line):
            destination = match.group(1).strip("<>")
            links.append((number, destination))
        heading = HEADING.match(line)
        if heading:
            headings.append((number, len(heading.group(1)), heading.group(2).strip()))

    if fence_char is not None:
        findings.append("A fenced code block is not closed.")

    first_content = next((line.strip() for line in visible if line.strip()), "")
    if not re.match(r"^#\s+\S", first_content):
        findings.append("Start with one clear level-one project title (# Project Name).")
    elif headings and headings[0][1] != 1:
        findings.append("The first Markdown heading should be a level-one title.")

    if headings and len(headings[0]) >= 3:
        first_heading_index = next((i for i, line in enumerate(visible)
                                    if HEADING.match(line)), -1)
        title_description = ""
        if first_heading_index >= 0:
            for line in visible[first_heading_index + 1:]:
                if HEADING.match(line):
                    break
                if line.strip() and not line.lstrip().startswith(("[", "![", "<")):
                    title_description = line.strip()
                    break
        if not title_description:
            findings.append("Add a short plain-language description after the title.")

    normalized = [re.sub(r"[^a-z0-9 ]", "", h.lower()).strip() for _, _, h in headings]
    for section, aliases in REQUIRED_SECTIONS.items():
        if not any(any(h == alias or h.startswith(alias + " ") for alias in aliases)
                   for h in normalized):
            findings.append(f"Add a {section.title()} section (or a clear equivalent heading).")

    for number, destination in links:
        parsed = urlsplit(destination)
        if parsed.scheme or destination.startswith("//") or destination.startswith("#"):
            continue
        local = parsed.path
        if not local:
            continue
        target = (base / local).resolve()
        if not target.exists():
            findings.append(f"Line {number}: local link target does not exist: {local}")

    return findings


def audit_file(path):
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"Cannot read {path}: {error}") from error
    return audit_text(text, path.resolve().parent)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", type=Path, help="README.md to check")
    args = parser.parse_args(argv)
    try:
        findings = audit_file(args.readme)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if findings:
        print(f"README audit: {len(findings)} finding(s).")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"README audit passed: {args.readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
