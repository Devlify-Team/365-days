# 006 — Repository structure best practices

- **Workbook:** `365_Days_GitHub_Challenge_Tracker.xlsx`, `All Projects`, Day 6
- **Month:** Month 1 — Foundations & GitHub Basics
- **Topic:** Repo Management
- **Primary:** GitHub repository structure
- **Alternative:** Cookiecutter templates
- **Suggested repository:** `repository-structure-best-practices`; delivered as `006/` inside `Devlify-Team/365-days`.

This project demonstrates a small, conventional Python package layout inside the already-selected `365-days` repository. The purpose of this README is to explain this Day 6 project and provide a quick way to inspect and run it.

## Structure

```text
006/
├── README.md
├── .gitignore
├── docs/
│   └── structure-notes.md
├── src/
│   └── structure_demo/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
├── tests/
│   └── test_structure_demo.py
```

The `src` layout keeps importable package code separate from the repository root. This helps prevent tests or local commands from accidentally importing a package directly from the checkout rather than from the intended source directory. The package uses only the Python standard library; no external packages are required.

A small project should not gain directories merely for the sake of a template. Add directories when the project actually needs them, such as documentation, examples, or additional tooling. Keep names consistent and descriptive, and place package code, tests, documentation, and configuration where contributors can find them predictably. The root README should explain the project, how to run it, and any important conventions.

## Run the example

From the repository root:

```bash
PYTHONPATH=006/src python3 -m structure_demo --name John
```

If `--name` is omitted, the program uses `world` as the default:

```bash
PYTHONPATH=006/src python3 -m structure_demo
```

## Run the tests

From the repository root:

```bash
PYTHONPATH=006/src python3 -B -m unittest discover -s 006/tests -p 'test_*.py' -v
```

The test suite uses `unittest` from the standard library. No installation step is needed.

## Repository practices covered

- Keep one coherent `365-days` repository for these daily exercises; do not create nested Git repositories or proliferate new repositories for this day.
- Use a clear source layout, with package code under `src/` and tests under `tests/`.
- Put supporting notes in `docs/` when they help, and add project metadata/build configuration only when the project needs it.
- Use `.gitignore` for generated caches, virtual environments, build output, and local secrets. It should not be treated as a substitute for careful handling of sensitive data.
- Prefer consistent naming and a useful root README over unnecessary folders or boilerplate.
- Language-specific conventions may differ in a real project; adapt the layout to the language and ecosystem rather than applying this Python example mechanically.
- A license, security policy, branch protection, CI workflow, or other repository setting may be appropriate for a real project, but this exercise does not claim that any of them is enabled.

## Cookiecutter, optionally

Cookiecutter templates can provide reusable scaffolding for teams that repeatedly start similar projects. They are optional here, not a requirement: this exercise is intentionally small enough to create and understand directly. A template should preserve the project’s conventions rather than adding unused files or directories.

## Manual checklist

- [ ] The package lives under `006/src/structure_demo/`.
- [ ] Tests live under `006/tests/` and follow the `test_*.py` naming pattern.
- [ ] Supporting layout notes live under `006/docs/`.
- [ ] `.gitignore` covers Python caches, virtual environments, and local `.env` files.
- [ ] `006/README.md` explains this project and includes runnable commands.
- [ ] The example runs with `--name John` and defaults to `world` without that option.
- [ ] The tests pass using the documented standard-library command.
- [ ] No nested Git repository or new repository was created for Day 6.

## Official references

- [GitHub repository best practices](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)

## Delivery note

The package and CLI run from the repository root using `PYTHONPATH=006/src`; all five standard-library tests passed. No nested repository or external dependency was added.
