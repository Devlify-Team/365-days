# Day 007: Write a Comprehensive README

This workbook entry teaches you to turn a project’s purpose, setup, usage, and support path into a clear, maintainable GitHub README.

## Overview

Day 007 belongs to **Month 1: Foundations & GitHub Basics** in the 365 Days workbook. The primary learning resource is GitHub’s README guidance, with MkDocs as an alternate documentation landing-page reference. The practical outcome is a README that helps a new reader decide whether a project is relevant, install or configure it, run a first example, test it, and find help without guessing.

A strong README is product documentation at the repository entrance. It should answer, in the order a reader needs: what the project does, who it is for, why its features matter, how to get started, how to use it, how to verify it, what its limitations are, and where to ask for help. Keep deeper architecture and long-form guides elsewhere; link to them from the README when they exist.

### Workbook metadata

- **Day:** 007
- **Theme:** Documentation
- **Month:** 1 — Foundations & GitHub Basics
- **Primary resource:** [GitHub’s README guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- **Alternate resource:** [MkDocs](https://www.mkdocs.org/)
- **Suggested repository name:** `write-a-comprehensive-readme`
- **Repository scope:** This exercise stays inside the current single repository; it does not create a separate repository.

## Learning goals

By the end of this exercise, you should be able to:

1. Explain a project’s value and intended audience in plain language.
2. Organize a README around a predictable reader journey rather than a list of implementation details.
3. Write copyable, tested setup and usage commands.
4. Use local relative links that continue to work when the repository is cloned or viewed on another branch.
5. State support boundaries and limitations honestly.
6. Run a lightweight audit while understanding that automation does not replace proofreading, accessibility review, or security testing.

## Getting started

### Requirements

- Python 3.9 or newer
- Python standard library only; no third-party dependencies are required
- A shell and a local checkout of this repository

Change into the Day 007 directory from the repository root:

```bash
cd 007
```

The exercise files are linked here for convenient inspection:

- [README audit CLI](readme_audit.py)
- [README template](README_TEMPLATE.md)
- [Greeting example README](examples/greeting/README.md)
- [Greeting example code](examples/greeting/hello.py)
- [Day 007 tests](tests/)

### Suggested workflow

1. Read the [official GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).
2. Inspect the [greeting example README](examples/greeting/README.md) and its [Python program](examples/greeting/hello.py).
3. Copy the structure from [README_TEMPLATE.md](README_TEMPLATE.md) into a real project README, replacing every explicit placeholder.
4. Run the audit against the customized README.
5. Follow every setup and usage command in a clean environment or fresh checkout, then revise any ambiguous step.

## Usage

The sample program prints a greeting and accepts an optional name. From the repository root, run the exact example command:

```bash
python3 007/examples/greeting/hello.py --name John
```

The expected output is:

```text
Hello, John!
```

To audit the sample README from the repository root:

```bash
python3 -B 007/readme_audit.py 007/examples/greeting/README.md
```

The audit checks for a clear `#` title, a nonempty description after the title, the expected overview/setup/usage/testing/help sections (including documented aliases), balanced fenced code blocks, existing local relative links, and unfinished placeholder markers. A clean result is useful evidence that the document has the required shape; it is not proof that every claim or command is correct.

### What to include in a project README

Use this outline as a practical default:

1. **Title and one-sentence description:** Identify the project and its outcome immediately.
2. **Overview:** Explain what it does, why it is useful, and who should use it. Add a short feature list only when each feature has a reason to exist.
3. **Getting started:** State prerequisites, installation or setup, configuration, and the smallest successful path.
4. **Usage and examples:** Provide copyable commands, realistic inputs, expected outputs, and links to more examples.
5. **Testing:** Tell readers how to run the relevant checks and what a successful run means.
6. **Help, support, or contact:** Identify the issue tracker, discussion channel, maintainer route, or a clear way to report a reproducible problem.
7. **Limitations:** Describe unsupported environments, known constraints, destructive actions, or behavior that may surprise users.
8. **Contribution and license:** Add these when the project has an established process and permissions. A license section is optional if rights have not yet been decided; do not imply permissions that have not been granted.

## Testing

Run the Day 007 unittest suite from the repository root:

```bash
python3 -B -m unittest discover -s 007/tests -p 'test_*.py' -v
```

The example’s focused audit command is:

```bash
python3 -B 007/readme_audit.py 007/examples/greeting/README.md
```

The template intentionally contains explicit placeholders and is not expected to pass as a finished project README. Running the following command should report multiple findings, including unfinished placeholders and the missing one-sentence description. Fill in and verify the template before expecting it to pass:

```bash
python3 -B 007/readme_audit.py 007/README_TEMPLATE.md
```

Customize the template first; audit the resulting project README rather than treating the unfinished template as production documentation. The audit is intentionally lightweight: it does not replace human proofreading, accessibility testing, security testing, command execution in a clean environment, link checks for remote URLs, or review of technical accuracy.

## Help / Support

For this workbook exercise, start with the [GitHub README documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), compare the [alternate MkDocs landing page](https://www.mkdocs.org/), and inspect the linked [sample README](examples/greeting/README.md). If a local command or test fails, verify that you are at the repository root, that Python 3.9+ is available, and that the expected Day 007 files are present. Report a reproducible issue through the repository’s established issue or discussion channel when one is configured.

## Practical customized README checklist

Before calling a README finished, confirm that:

- The title and first paragraph say what the project does without unexplained jargon.
- The audience and the reason each important feature matters are clear.
- Prerequisites, installation, configuration, and first-run steps are copyable and have been tested.
- Examples show realistic commands and expected results.
- Testing instructions identify the command and the meaningful success signal.
- Help, limitations, and support boundaries are honest and easy to find.
- Local links use repository-relative paths and resolve after cloning.
- Code fences are balanced, language labels are useful, and prose is readable with a keyboard and screen reader.
- Badges are optional and included only when they are maintained and useful; stale badges reduce trust.
- A license is not asserted until the project’s rights and chosen license are decided.

## Source notes

GitHub describes a README as a place to explain why a project is useful, what it does, how to get started, where to get help, and who maintains or contributes to it. GitHub also recommends relative links for files within a repository because they work across clones and branches. The primary source for this exercise is [About the repository README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes). [MkDocs](https://www.mkdocs.org/) is included as an alternate documentation-site perspective, not as a required dependency.
