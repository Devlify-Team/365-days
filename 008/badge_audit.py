#!/usr/bin/env python3
"""Check README badge image markup without fetching remote images."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

IMAGE = re.compile(r"!\[([^\]]*)\]\((<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
PLACEHOLDER = re.compile(r"(?:<\s*(?:owner|repo|workflow)[^>]*>|\b(?:YOUR_OWNER|YOUR_REPO|OWNER|REPO)\b)", re.IGNORECASE)
BADGE_HOSTS = {"img.shields.io", "shields.io", "badgen.net", "www.badgen.net"}


def strip_fenced_code(text):
    """Replace fenced-code contents with blank lines before scanning Markdown."""
    output = []
    fence_char = None
    fence_length = 0
    for line in text.splitlines():
        match = FENCE.match(line)
        if match:
            token = match.group(1)
            char, length = token[0], len(token)
            if fence_char is None:
                fence_char, fence_length = char, length
            elif char == fence_char and length >= fence_length and not line.strip()[length:].strip():
                fence_char, fence_length = None, 0
            output.append("")
        elif fence_char is None:
            output.append(line)
        else:
            output.append("")
    return "\n".join(output)


def audit_text(text):
    """Return the detected badge count and actionable markup findings."""
    findings = []
    badges = 0
    visible = strip_fenced_code(text)
    for number, line in enumerate(visible.splitlines(), 1):
        for image in IMAGE.finditer(line):
            alt = image.group(1).strip()
            destination = image.group(2).strip("<>")
            parsed = urlsplit(destination)
            hostname = (parsed.hostname or "").lower()
            is_badge = hostname in BADGE_HOSTS or (
                hostname == "github.com" and "/actions/workflows/" in parsed.path
                and parsed.path.endswith("/badge.svg")
            )
            if not is_badge:
                continue
            badges += 1
            if not alt:
                findings.append(f"Line {number}: badge image has empty alt text.")
            elif alt.lower() in {"badge", "image", "status"}:
                findings.append(f"Line {number}: badge alt text is too generic; describe its meaning.")
            if parsed.scheme.lower() not in {"http", "https"} or not hostname:
                findings.append(f"Line {number}: badge URL must use an absolute HTTP or HTTPS URL.")
            if PLACEHOLDER.search(destination):
                findings.append(f"Line {number}: badge URL still contains an owner/repository placeholder.")
    return badges, findings


def audit_file(path):
    path = Path(path)
    try:
        return audit_text(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        raise ValueError(f"Cannot read {path}: {error}") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", type=Path, help="Markdown README to inspect")
    args = parser.parse_args(argv)
    try:
        badges, findings = audit_file(args.readme)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if findings:
        print(f"Badge audit: {badges} badge(s), {len(findings)} finding(s).")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"Badge audit passed: {badges} badge(s) in {args.readme}.")
    print("Remote badge rendering and the truth of badge claims were not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
