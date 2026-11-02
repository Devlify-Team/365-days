# Day 15 · Month 1 Foundations & GitHub Basics

## Topic

Projects

## Build a data analysis portfolio

This is a **starter** for a data analysis portfolio. The primary GitHub project is `data-portfolio`; a personal website is an alternative. Slug: `build-a-data-analysis-portfolio`.

The starter page is a static local preview. It does not contain a real portfolio, fake entries, fake results, or a dataset. Add only real, completed analyses that you have permission to share.

## Project tree

```text
015/
├── site/
│   ├── index.html
│   ├── styles.css
│   ├── portfolio.js
│   └── projects.json
├── case-study-template.md
├── check_portfolio.py
├── tests/
│   └── test_check_portfolio.py
└── .gitignore
```

- `site/index.html`, `site/styles.css`, and `site/portfolio.js` make up the dependency-free static page.
- `site/projects.json` starts with an empty `projects` list. The page fetches this local file and displays an honest no-projects message until you add reviewed case studies.
- The JavaScript safely inserts user content with `textContent`, requires HTTPS repository links, and requires the publication review flag.
- `case-study-template.md` provides the structure for defensible case studies.
- `check_portfolio.py` validates portfolio metadata with the Python standard library only. It does not read or analyze datasets.
- `tests/test_check_portfolio.py` uses metadata-only fixtures and makes no claims about real data.
- `.gitignore` helps keep local and generated files out of the repository.

## Required case-study metadata

Each project object must contain exactly these keys:

```text
slug
title
summary
repository_url
data_source
data_rights
limitations
reviewed_for_publication
```

The machine-readable schema is exactly:

```json
{
  "slug": "lowercase-hyphenated-slug",
  "title": "Project title",
  "summary": "Short summary",
  "repository_url": "https://github.com/your-account/your-repository",
  "data_source": "Where the data came from",
  "data_rights": "License and permission details",
  "limitations": "Known limitations",
  "reviewed_for_publication": true
}
```

`slug` must be lowercase and hyphenated. `repository_url` must use HTTPS and must not contain embedded credentials. Set `reviewed_for_publication` to `true` only after checking the repository, source, outputs, sharing permissions, and publication risks.

Do not invent an analysis, result, dataset, source, license, or permission. Document the real source, license or permission basis, and limitations. Never include private data, credentials, tokens, or other secrets. Verify the repository source and outputs before publishing. A portfolio may be hosted separately by you; this folder provides only a local static preview and has no deployment workflow or hosted site.

## Commands

Run these from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B 015/check_portfolio.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s 015/tests -p 'test_*.py' -v
```

The empty `projects` list passes the checker. The tests validate metadata-only behavior, including the starter state; they do not read or analyze a dataset.

To preview the static page locally:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory 015/site
```

Then open <http://127.0.0.1:8000>. The page is intended for local preview only. It has no external images, fonts, assets, or dependencies.

## Adding a case study

Start with `case-study-template.md`. Add a project only when the analysis is complete and defensible, you can share the data or describe its permitted use, and the repository source and outputs have been verified. Record what the data is, where it came from, the applicable rights or permissions, the method and results you can support, and the limitations. Keep the metadata honest and leave the list empty when there is no suitable completed project yet.
