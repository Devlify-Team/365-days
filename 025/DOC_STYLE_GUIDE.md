# Documentation style guide

Use the target project's own style guide when one exists. These checks are a lightweight fallback, not a universal grammar rulebook.

## Write for a reader's task

Name the audience and the outcome. Put prerequisites before steps, use one action per numbered step, and explain the expected result when it helps the reader know they succeeded. Prefer familiar words and active voice; define necessary technical terms.

## Make pages easy to scan

Use a specific title and descriptive headings in a logical order. Keep paragraphs focused. Use numbered lists for sequences and bullets for options. Avoid headings that merely say “Overview” when a more informative phrase fits.

## Keep examples safe and usable

Use fenced code blocks with a language label. Show copyable commands without shell prompts. Clearly mark values readers must replace, and never include real credentials, personal data, or destructive commands without explaining the impact. Test commands when possible.

## Check links and accessibility

Use link text that describes its destination rather than “click here.” Prefer relative paths for links to files in the same repository. Add useful alternative text to informative images; do not put essential instructions only in an image. Ensure tables and screenshots remain understandable on small screens.

## Verify before asking for review

Check facts against the current product or source code, run the repository's checks, inspect the rendered preview, and review your diff. The local checker in this project catches only a few structural issues; it cannot replace this human review.
