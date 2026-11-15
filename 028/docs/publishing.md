# Publishing

MkDocs builds this source into a static `site/` directory. The files can be hosted by a static site provider, but this starter does not select a provider or publish automatically.

## Before publishing

- [ ] Replace the sample content, title, and navigation with project-specific documentation.
- [ ] Run `python -m mkdocs build --strict` and resolve all warnings.
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Review the rendered pages, links, code examples, and mobile layout.
- [ ] Confirm the selected host's base path, domain, and access settings.
- [ ] Add deployment credentials only through the host's approved secret store; never put them in source files.

The generated output is a build artifact. Keep the Markdown source and `mkdocs.yml` under version control; do not commit `site/` unless the chosen host explicitly requires it.
