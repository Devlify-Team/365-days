# Why these folders exist

This small Python example uses three top-level areas so responsibilities are easy to find:

- `src/structure_demo/` contains the importable example package. The `src` layout makes the source location explicit and, when the repository root is on Python's import path, helps avoid importing the package directly from its working tree by accident.
- `tests/` contains checks for the public greeting function and command-line behavior. Tests are not mixed into runtime code.
- `docs/` holds supporting design and usage notes that would make the main README too long.

The root `README.md` introduces the example and gives run commands; `.gitignore` keeps generated caches, virtual environments, and local environment files out of ordinary version control. These are conventions, not universal requirements: choose language-appropriate names and add directories only when the project has content for them. This learning sample runs directly from source with Python's standard library; it does not include a package installer, release workflow, or external dependencies.
