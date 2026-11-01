# Day 14 · Month 1: Foundations & GitHub Basics

## Topic: Notebooks

**Workbook mapping:** Day 14 · Project: Share notebooks on GitHub · Primary: GitHub `notebook-sharing` · Alternatives: NBViewer and Binder · Slug: `share-notebooks-on-github`.

## What this project does

`share_links.py` is a dependency-free, read-only command-line tool that formats links for a notebook that is **already committed** to a GitHub repository. Given a repository in `owner/name` form, a relative `.ipynb` path, and a branch, tag, or commit-like ref, it prints links for:

- **GitHub**, using a `blob` URL that displays the committed notebook. GitHub documents viewing non-code files, including rendered notebooks, in its [Working with non-code files documentation](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).
- **NBViewer**, a notebook rendering/viewing service for files hosted elsewhere. [NBViewer](https://nbviewer.org/) is not a file host and does not receive an upload from this tool.
- **Binder**, which launches a remote interactive environment from the repository. Binder’s [documentation](https://mybinder.readthedocs.io/en/latest/) explains the repository-based environment model and reproducibility requirements; its [sample repository launch example](https://mybinder.readthedocs.io/en/latest/examples/sample_repos.html) shows the `?filepath=/path/to/notebook.ipynb` URL format.

The builder URL-encodes branch/ref and notebook-path components where required, validates the inputs, and makes **zero network calls**. It uploads nothing, publishes nothing, and does not test, verify, or launch any generated link. The command’s output is only a set of formatted URLs.

## Before sharing

1. First commit the notebook to an appropriate repository. GitHub, NBViewer, and Binder cannot display a notebook that has not been committed at a location they can access.
2. From the repository root, inspect the working tree with `git status` and review the notebook itself.
3. Remove or protect credentials, tokens, private data or results, personal information, and anything you do not have permission to redistribute. Check that dependencies and supporting files are suitable for the intended audience.
4. Decide whether the repository should be public. The generated links only work for viewers with the requisite access. NBViewer and Binder generally require a public repository for the usual sharing flow. Once sensitive content is pushed to a public repository, public exposure may be irreversible without removing it from repository history; removing the current file alone may not remove historical copies.
5. For Binder, make the environment reproducible where needed—for example with `requirements.txt`, `environment.yml`, or another supported setup. Binder builds can take time, and a successful link depends on the repository’s environment being buildable.

GitHub’s rendered notebook view is static: rich JavaScript interactions are not interactive on GitHub. Use Binder when viewers need a remote interactive environment, and remember that Binder executes code in that environment, so notebooks should be reviewed accordingly.

## Usage

Run the link builder from the repository root (the script is in directory `014`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B 014/share_links.py \
  --repo OWNER/REPO \
  --path notebooks/example.ipynb \
  --ref main
```

Example output has one URL for each service:

```text
GitHub: https://github.com/OWNER/REPO/blob/main/notebooks/example.ipynb
NBViewer: https://nbviewer.org/github/OWNER/REPO/blob/main/notebooks/example.ipynb
Binder: https://mybinder.org/v2/gh/OWNER/REPO/main?filepath=%2Fnotebooks%2Fexample.ipynb

This only formats URLs. The notebook must already be committed to a repository the viewer can access.
Use public, permission-cleared notebooks; the tool does not publish, test or launch anything.
```

Arguments:

- `--repo` is required and must be a GitHub-style `owner/name` value.
- `--path` is required and must be a relative POSIX path ending in `.ipynb`; it cannot contain `..`, an absolute prefix, backslashes, query text, or a fragment.
- `--ref` is optional and defaults to `main`. It may identify a branch, tag, or commit-style ref.

The generated URL is not proof that the notebook is reachable. Open or distribute links only after checking repository visibility and access through the appropriate service; this script itself does not perform that check.

## Tests

The tests are dependency-free built-in `unittest` tests and parse URLs locally; they do not contact GitHub, NBViewer, or Binder:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s 014/tests -p 'test_*.py' -v
```

The current suite contains 4 tests covering link construction, URL encoding, invalid repositories/paths/refs, and CLI output without publishing.

## Files

- `014/share_links.py` — dependency-free, read-only CLI that validates inputs and formats GitHub, NBViewer, and Binder notebook links.
- `014/tests/test_share_links.py` — local `unittest` coverage for URL parsing, validation, encoding, and non-publishing CLI behavior.
- `014/.gitignore` — ignores Python bytecode and common test caches.
- `014/README.md` — this usage and safe-sharing guide.

No sharing or posting action occurs here: the user remains responsible for committing the notebook, checking its contents and permissions, choosing repository visibility, and deciding whether or where to distribute the resulting links.
