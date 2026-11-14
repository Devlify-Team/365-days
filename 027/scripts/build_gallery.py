"""Generate a categorized Markdown gallery from local project READMEs."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
TITLE = re.compile(r"^#\s+(.+?)\s*#*\s*$")


def readme_preview(path: Path) -> tuple[str, str]:
    """Read the first H1 and following prose paragraph from a README."""
    lines = path.read_text(encoding="utf-8").splitlines()
    title = None
    paragraph: list[str] = []
    after_title = False
    for line in lines:
        if title is None:
            match = TITLE.match(line)
            if match:
                title = match.group(1).strip()
                after_title = True
            continue
        if after_title:
            if not line.strip():
                if paragraph:
                    break
                continue
            if line.startswith("#") or line.startswith(("- ", "* ", "> ", "```")):
                continue
            paragraph.append(line.strip())
    if not title:
        raise ValueError(f"{path}: expected a level-one README title")
    summary = " ".join(paragraph).strip()
    if not summary:
        raise ValueError(f"{path}: expected an opening summary paragraph")
    return title, summary


def load_projects(manifest_path: Path) -> list[dict[str, str]]:
    """Load project entries and ensure all source READMEs stay in the project."""
    manifest_path = manifest_path.resolve()
    root = manifest_path.parent
    try:
        entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read manifest {manifest_path}: {error}") from error
    if not isinstance(entries, list) or not entries:
        raise ValueError("manifest must be a non-empty JSON array")

    projects: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for number, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"entry {number} must be a JSON object")
        slug, category, readme = (entry.get(key) for key in ("id", "category", "readme"))
        if not all(isinstance(value, str) and value.strip() for value in (slug, category, readme)):
            raise ValueError(f"entry {number} needs non-empty id, category, and readme fields")
        if not SLUG.fullmatch(slug):
            raise ValueError(f"entry {number} has an invalid id: {slug}")
        if slug in seen_ids:
            raise ValueError(f"duplicate project id: {slug}")
        seen_ids.add(slug)

        source = (root / readme).resolve()
        if source != root and root not in source.parents:
            raise ValueError(f"README path must stay inside the manifest folder: {readme}")
        if not source.is_file():
            raise ValueError(f"README file does not exist: {readme}")
        title, summary = readme_preview(source)
        projects.append({"id": slug, "category": category.strip(), "readme": str(source), "title": title, "summary": summary})
    return projects


def generate_gallery(manifest_path: Path, output_path: Path | None = None) -> Path:
    """Write the README gallery and return its path."""
    manifest_path = manifest_path.resolve()
    root = manifest_path.parent
    output_path = (output_path or (root / "README_GALLERY.md")).resolve()
    projects = load_projects(manifest_path)
    source_paths = {Path(project["readme"]).resolve() for project in projects}
    if output_path in source_paths:
        raise ValueError("gallery output cannot overwrite a source README")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for project in projects:
        grouped[project["category"]].append(project)

    lines = [
        "# Project README Gallery",
        "",
        "A browsable collection of project README previews. Edit `projects.json` and rebuild with `python3 scripts/build_gallery.py`.",
    ]
    for category in sorted(grouped, key=str.casefold):
        lines.extend(["", f"## {category}"])
        for project in sorted(grouped[category], key=lambda item: item["title"].casefold()):
            relative = Path(os.path.relpath(project["readme"], output_path.parent))
            link = quote(relative.as_posix(), safe="/._-")
            title = project["title"].replace("[", "\\[").replace("]", "\\]")
            summary = project["summary"].replace("|", "\\|")
            lines.extend(["", f"### [{title}]({link})", "", summary])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parents[1] / "projects.json")
    parser.add_argument("--output", type=Path, help="Output Markdown file (default: README_GALLERY.md beside manifest)")
    args = parser.parse_args()
    try:
        output = generate_gallery(args.manifest, args.output)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
