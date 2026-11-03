# Day 16 — Create a project showcase

**Workbook mapping:** Month 1 · Projects · Primary GitHub concept: `project-showcase` · Alternative: GitHub Pages · Slug: `create-a-project-showcase`.

This is an accessible, static project gallery built from the repository's first 15 completed projects. It does not invent metrics or results. The cards link to existing project READMEs.

## Files

- `site/index.html`, `site/styles.css`, and `site/showcase.js` build a responsive filterable gallery with search and topic filters.
- `site/projects.json` lists projects 001–015 and relative README paths. Text is added through DOM text nodes rather than HTML strings.
- `check_showcase.py` validates the manifest fields, unique zero-padded numbers, and that every card points to an existing README under this repository.
- `tests/test_check_showcase.py` tests real links and invalid metadata offline.

## Preview

From the repository root, start a local-only server:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/016/site/>. The page uses only local files, with no external fonts, images, services, or dependencies.

## Validate

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B 016/check_showcase.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s 016/tests -p 'test_*.py' -v
```

The validator checks that every displayed project is backed by a real README in its numbered folder. When adding future projects to the showcase, update `site/projects.json` with the title, topic, concise description, and README link; rerun the validator and tests.

## Hosting

The files in `site/` can be deployed to a static host after reviewing the links. This project intentionally adds no GitHub Pages workflow: the repository already has a site publisher for another exercise, and a second workflow could replace its published site. The local preview does not deploy or publish anything.
