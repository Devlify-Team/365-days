"""Generate a curated portfolio page from verified local project links."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def load_portfolio(manifest_path: Path) -> dict[str, object]:
    """Load portfolio metadata and validate each local project target."""
    manifest_path = manifest_path.resolve()
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read portfolio data: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("portfolio data must be a JSON object")

    title = _text(data.get("title"), "title")
    repository = _text(data.get("repository"), "repository")
    if not REPOSITORY.fullmatch(repository):
        raise ValueError("repository must use the OWNER/REPOSITORY format")
    summary = _text(data.get("summary"), "summary")
    projects = data.get("projects")
    if not isinstance(projects, list) or not projects:
        raise ValueError("projects must be a non-empty list")

    repo_root = manifest_path.parent.parent.resolve()
    seen_paths: set[str] = set()
    normalized: list[dict[str, str]] = []
    for number, item in enumerate(projects, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"project {number} must be a JSON object")
        project = {
            key: _text(item.get(key), f"project {number} {key}")
            for key in ("title", "focus", "description", "path")
        }
        if project["path"] in seen_paths:
            raise ValueError(f"duplicate project path: {project['path']}")
        seen_paths.add(project["path"])
        target = (manifest_path.parent / project["path"]).resolve()
        if target == repo_root or repo_root not in target.parents:
            raise ValueError(f"project path must stay inside this repository: {project['path']}")
        if not target.exists():
            raise ValueError(f"project target does not exist: {project['path']}")
        normalized.append(project)

    return {
        "title": title,
        "repository": repository,
        "summary": summary,
        "projects": normalized,
    }


def _escape_link_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def render_portfolio(data: dict[str, object]) -> str:
    """Render validated data as a readable GitHub-flavored Markdown page."""
    repository = str(data["repository"])
    lines = [
        f"# {_escape_link_text(str(data['title']))}",
        "",
        f"**Repository:** [`{repository}`](https://github.com/{repository})",
        "",
        str(data["summary"]).replace("|", "\\|"),
        "",
        "## Selected projects",
    ]
    for project in data["projects"]:
        title = _escape_link_text(project["title"])
        link = quote(project["path"], safe="/._-")
        lines.extend(
            [
                "",
                f"### [{title}]({link})",
                "",
                f"**Focus:** {project['focus']}",
                "",
                project["description"].replace("|", "\\|"),
            ]
        )
    lines.extend(
        [
            "",
            "## Explore the full challenge",
            "",
            "Browse the [365 Days project index](../README.md) for the complete collection.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_portfolio(manifest_path: Path, output_path: Path | None = None) -> Path:
    """Validate input and write the generated portfolio file."""
    manifest_path = manifest_path.resolve()
    output_path = (output_path or (manifest_path.parent / "PORTFOLIO.md")).resolve()
    if output_path == manifest_path:
        raise ValueError("output cannot overwrite portfolio.json")
    data = load_portfolio(manifest_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_portfolio(data), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "portfolio.json",
        help="Portfolio JSON manifest",
    )
    parser.add_argument("--output", type=Path, help="Output Markdown file")
    args = parser.parse_args()
    try:
        result = build_portfolio(args.input, args.output)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Generated {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
