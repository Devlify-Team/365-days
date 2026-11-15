# Create a project documentation site

- **Day:** 028
- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Showcase
- **Primary GitHub:** `docs-site`
- **Alternative:** ReadTheDocs
- **Slug:** `create-project-documentation-site`

A small, ready-to-preview documentation site built with MkDocs. It includes a landing page, setup instructions, page-authoring guidance, a publishing checklist, a built-in search, and tests that keep the navigation linked to real source pages.

## Preview and build

From this folder, create an environment and install the pinned direct dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

Open the local address printed by MkDocs to preview edits. To validate the site and run its structural tests:

```bash
python -m mkdocs build --strict
python -m unittest discover -s tests -v
```

The generated `site/` folder is ignored by Git. It contains static files that you can host on a static site provider; deployment is intentionally not configured, so you can choose a destination and add its workflow later.

## Customize it

Edit `mkdocs.yml` to change the title, theme, and navigation. Add Markdown files under `docs/` and add them to the navigation so readers can find them. Replace the sample site content with documentation for your own project.

The structure follows the official [MkDocs getting-started guide](https://www.mkdocs.org/getting-started/), which uses a configuration file and a `docs/` source directory. GitHub's [README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) also explains how README files help visitors get started; this project keeps the longer user documentation in the site.
