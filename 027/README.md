# Build a project README gallery

- **Day:** 027
- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Showcase
- **Primary GitHub:** `readme-gallery`
- **Alternative:** Personal website
- **Slug:** `build-a-project-readme-gallery`

This small Python tool builds a browsable Markdown gallery from a manifest of project README files. It extracts each README's title and opening summary, groups the entries by category, and writes local links that work when the repository is cloned. Three sample README files are included; replace them and the manifest with your own projects.

## Build and test

From this folder, run:

```bash
python3 scripts/build_gallery.py
python3 -m unittest discover -s tests -v
```

The first command regenerates `README_GALLERY.md`. Review the output and commit it when ready. The generator uses only the Python standard library, rejects duplicate project IDs and missing or out-of-folder README paths, and will not overwrite a source README. It does not publish a website or contact external services.

## Customize it

Edit `projects.json` to add each project's unique slug, category, and path to its README. Write the README with one top-level title and a concise opening paragraph; the gallery uses those as the card title and preview. The paths stay local, so readers can open a project's README in GitHub or in a clone.

GitHub describes a README as a first stop for explaining what a project does and how to get started, and recommends relative links for files in a repository. See [About the repository README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) for details.
