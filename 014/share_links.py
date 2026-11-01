#!/usr/bin/env python3
"""Build sharing URLs for a notebook already stored in a public GitHub repo."""

import argparse
import re
from urllib.parse import quote, urlencode


def _validate(repo, path, ref):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repo):
        raise ValueError("Repository must be owner/name using GitHub-style names")
    if not path or "\\" in path or path.startswith("/") or "?" in path or "#" in path:
        raise ValueError("Notebook path must be a relative POSIX path without query or fragment")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts) or not path.lower().endswith(".ipynb"):
        raise ValueError("Path must identify a .ipynb file inside the repository")
    if not ref or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", ref) or ".." in ref or "//" in ref or ref.endswith("/"):
        raise ValueError("Ref must be a branch, tag or commit-style name")
    if any(part in (".", "..") for part in ref.split("/")):
        raise ValueError("Ref cannot contain dot path components")


def build_links(repo, path, ref="main"):
    """Return GitHub, NBViewer and Binder URLs; performs no network operation."""
    _validate(repo, path, ref)
    owner, name = repo.split("/", 1)
    encoded_ref = quote(ref, safe="")
    encoded_path = quote(path, safe="/")
    github = f"https://github.com/{owner}/{name}/blob/{encoded_ref}/{encoded_path}"
    nbviewer = f"https://nbviewer.org/github/{owner}/{name}/blob/{encoded_ref}/{encoded_path}"
    binder_path = "/" + path
    binder = f"https://mybinder.org/v2/gh/{owner}/{name}/{encoded_ref}?{urlencode({'filepath': binder_path})}"
    return {"GitHub": github, "NBViewer": nbviewer, "Binder": binder}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Public GitHub repository in owner/name form")
    parser.add_argument("--path", required=True, help="Path to a committed .ipynb file relative to the repository root")
    parser.add_argument("--ref", default="main", help="Branch, tag or commit (default: main)")
    args = parser.parse_args(argv)
    try:
        links = build_links(args.repo, args.path, args.ref)
    except ValueError as error:
        parser.error(str(error))
    for service, link in links.items():
        print(f"{service}: {link}")
    print("\nThis only formats URLs. The notebook must already be committed to a repository the viewer can access.")
    print("Use public, permission-cleared notebooks; the tool does not publish, test or launch anything.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
