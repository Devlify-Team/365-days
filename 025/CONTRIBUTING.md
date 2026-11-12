# Contributing documentation

Good documentation fixes are specific, accurate, and easy to review. These steps are a starting point; always follow the target repository's own rules first.

## 1. Find a useful change

Read the project's `README.md`, `CONTRIBUTING.md`, and code of conduct. Search existing issues and discussions so you do not duplicate work. For a broad rewrite, unclear requirement, or unclaimed issue, ask maintainers before investing time. Respect issue labels and any areas the project does not accept contributions to.

## 2. Make one focused edit

Choose a clear reader and the task they need to complete. Fix one concrete gap, such as an outdated command, missing prerequisite, confusing sentence, or broken local link. Keep the change within the project's scope. Use the [documentation style guide](DOC_STYLE_GUIDE.md) for a quick review.

## 3. Work on a branch

For a repository where you have write access, use a topic branch. For a project where you do not, fork it and clone your fork before creating the branch.

```bash
git checkout -b DOCS-CHANGE
```

Edit the smallest relevant set of files. Preserve the project's terminology and formatting, and avoid unrelated cleanup.

## 4. Check and preview

Run the project's documented checks. In this learning lab, run:

```bash
python3 scripts/check_markdown.py docs/
python3 -m unittest discover -s tests -v
```

Read the rendered Markdown preview, test command examples when practical, and confirm the instructions match the current product or code. A passing lint check cannot verify facts, accessibility, or the rendering behavior of every platform.

## 5. Open a clear pull request

Use `templates/pull-request-template.md` as a prompt. Describe the reader problem and the change, list what you checked, and link any related issue. Keep the title specific. Review your own diff and preview before requesting review; respond to maintainer feedback on the same pull request.

For a larger proposal, open an issue first when the maintainers request it. Do not claim work on another contributor's issue unless the project has invited help or its rules allow it.
