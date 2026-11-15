# Writing pages

## Add a page

Create a Markdown file in `docs/`, give it one clear level-one heading, and write for a specific reader task. Put prerequisites before steps, use descriptive headings, and keep code examples short enough to copy and verify.

## Add it to navigation

Edit the `nav` section in `mkdocs.yml`. The label is what readers see in the site menu; the path is relative to the `docs/` directory. For example:

```yaml
nav:
  - Home: index.md
  - New guide: new-guide.md
```

Create `docs/new-guide.md` before running the build. The navigation tests check that each configured page exists.

## Link to related pages

Use relative Markdown links such as `[Getting started](getting-started.md)`. Keep link text descriptive so readers know where a link leads. Preview the built site and check that links work in the final navigation context.
