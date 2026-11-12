"""Check basic Markdown structure and local links without third-party tools."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^#\s+\S")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def check_markdown(path: Path | str) -> list[str]:
    """Return structural Markdown errors for one file, if any."""
    source = Path(path)
    try:
        lines = source.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return [f"{source}: cannot read file: {error}"]

    errors: list[str] = []
    heading_count = 0
    open_fence: tuple[str, int, int] | None = None
    links: list[tuple[int, str]] = []

    for line_number, line in enumerate(lines, start=1):
        fence_match = FENCE.match(line)
        if open_fence is None:
            if fence_match:
                marker = fence_match.group(1)
                open_fence = (marker[0], len(marker), line_number)
                continue
            if HEADING.match(line):
                heading_count += 1
            links.extend((line_number, match.group(1).strip()) for match in LINK.finditer(line))
        elif fence_match:
            marker = fence_match.group(1)
            if marker[0] == open_fence[0] and len(marker) >= open_fence[1]:
                open_fence = None

    if heading_count != 1:
        errors.append(f"{source}: expected exactly one top-level heading, found {heading_count}")
    if open_fence is not None:
        errors.append(f"{source}:{open_fence[2]}: unclosed fenced code block")

    for line_number, destination in links:
        if destination.startswith("<") and ">" in destination:
            destination = destination[1:destination.index(">")]
        parsed = urlsplit(destination)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (source.parent / unquote(parsed.path)).resolve()
        if not target.exists():
            errors.append(f"{source}:{line_number}: local link target does not exist: {parsed.path}")

    return errors


def markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        else:
            print(f"{path}: not a Markdown file or directory", file=sys.stderr)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Markdown files or folders")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    inputs = args.paths or [project_root / "docs"]
    files = markdown_files(inputs)
    if not files:
        print("No Markdown files found", file=sys.stderr)
        return 1

    errors = [error for path in files for error in check_markdown(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(files)} Markdown file(s); no structural issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
