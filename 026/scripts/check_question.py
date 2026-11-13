"""Check whether a discussion question draft includes useful context."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = ("Goal", "Context", "What I tried", "Question")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
PLACEHOLDER = re.compile(r"\[(?:describe|include|list|ask|write|replace|add|explain|remove)[^\]]*\]|\b(?:TODO|TBD)\b", re.IGNORECASE)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def check_draft(text: str) -> list[str]:
    """Return missing or unfilled question sections; never score the content."""
    problems: list[str] = []
    headings = list(HEADING.finditer(text))
    if not any(match.group(1) == "#" for match in headings):
        problems.append("Add a descriptive level-one title.")

    sections: dict[str, str] = {}
    for index, match in enumerate(headings):
        if match.group(1) != "##":
            continue
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        sections[match.group(2).strip().casefold()] = COMMENT.sub("", text[start:end]).strip()

    for required in REQUIRED:
        body = sections.get(required.casefold())
        if body is None:
            problems.append(f"Add a '## {required}' section.")
        elif not body:
            problems.append(f"Add content under '## {required}'.")
        elif PLACEHOLDER.search(body):
            problems.append(f"Replace the placeholder under '## {required}'.")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Markdown file containing a draft question")
    args = parser.parse_args()
    try:
        text = args.draft.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Cannot read {args.draft}: {error}", file=sys.stderr)
        return 2

    problems = check_draft(text)
    if problems:
        print("\n".join(f"- {problem}" for problem in problems), file=sys.stderr)
        return 1
    print("Question draft has the required sections and no recognized placeholders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
