# Day 13 — Jupyter notebook best practices

- **Month:** 1 — Foundations & GitHub Basics
- **Category:** Notebooks
- **Primary listed in the tracker:** GitHub `jupyter-guide`
- **Alternative:** [Google Colab](https://colab.research.google.com/)
- **Slug:** `jupyter-notebook-best-practices`

## What this lesson contains

This lesson is a practical guide to making Jupyter notebooks clear, repeatable, reviewable, and safe to share. The teaching notebook is [`jupyter_best_practices.ipynb`](./jupyter_best_practices.ipynb). It contains no dataset and performs no analysis; its code cells are intentionally unexecuted, with `execution_count` set to `null` and saved outputs cleared.

The notebook follows a deliberate order:

1. Start with a question, audience, and purpose.
2. Record data provenance, ownership, access date, licensing, sensitive fields, and permissions before loading real data.
3. Make execution order explicit and account for hidden kernel state.
4. Keep inputs and assumptions visible.
5. Work in small, testable steps.
6. Explain results, evidence, and limitations.
7. Review the notebook before committing or sharing.

Read each Markdown explanation before its related code. A notebook is a narrative, not just a script: explain what each step does and why. Keep cells small, name variables clearly, and separate data cleaning, analysis, and presentation. Move reusable functions into tested Python modules instead of copying large blocks between cells. Avoid hardcoded absolute paths, undocumented current-directory assumptions, and secrets in notebooks or source control. Use project-relative paths and keep credentials outside the notebook.

## Execution order and clean state

A Jupyter kernel retains variables and imports between cell runs. Running cells out of order can therefore produce results that depend on hidden state rather than on the visible notebook order. Before sharing or relying on results, **restart the kernel, then use Run All from the top**. This verifies that the saved order is sufficient and exposes missing setup steps. See the official [Jupyter documentation](https://docs.jupyter.org/en/latest/) and [Running Code](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Running%20Code.html) guide for the execution model and controls.

When a real project needs packages, include the expected Python version and installation instructions (for example, a requirements file or a short setup note) rather than assuming that a reader has the same environment. Record relevant library versions when they affect reproducibility. Document the source and permitted use of every real input before loading it; do not treat this starter notebook as evidence that any real dataset was tested.

Outputs should be intentional. Keep a useful result when it helps the reader understand the lesson or supports a documented conclusion, but remove debugging output, accidental displays, large tables, and other unneeded outputs before committing. Review the Git diff and inspect the complete notebook for secrets, private paths, personal information, data that cannot be redistributed, and license restrictions. Consider both privacy and licensing when sharing.

## Google Colab sharing

Google Colab can share the notebook’s contents—text, code, saved output, and comments—according to the sharing permission selected by the owner. Sharing does not share the runtime machine, its files, or its installed libraries, so a recipient may need to recreate the environment and obtain authorized inputs. Set permissions deliberately and do not assume that a shared notebook includes your runtime state. See the official [Google Colab FAQ](https://research.google.com/colaboratory/intl/en-GB/faq.html) for current details.

## Lightweight audit

[`notebook_audit.py`](./notebook_audit.py) is a dependency-free JSON shape and clean-execution checker. It checks the basics needed here: notebook format version 4, an integer minor version, top-level and cell metadata objects, recognized cell types, text sources, non-empty unique cell IDs, and— for code cells—`execution_count: null` plus an empty `outputs` list. It also reports invalid JSON and unreadable files.

This is intentionally **not** a full `nbformat` schema validator. For the complete format definition and stricter validation expectations, consult the official [nbformat format description](https://nbformat.readthedocs.io/en/latest/format_description.html). Passing this audit does not prove that code is correct, that a runtime is reproducible, that data permissions are valid, or that an analysis is scientifically sound.

Run these commands from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B 013/notebook_audit.py 013/jupyter_best_practices.ipynb
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s 013/tests -p 'test_*.py' -v
```

The tests in [`tests/test_notebook_audit.py`](./tests/test_notebook_audit.py) are offline standard-library tests using temporary structural fixtures. They cover clean notebooks, saved outputs and execution counts, duplicate IDs and unknown cell types, malformed structure, and invalid JSON. They do not load a dataset or perform notebook analysis.

## Before committing or sharing

- Confirm the question, audience, and notebook order are understandable.
- Restart the kernel and run all cells from a fresh state when validating an executed notebook.
- Document provenance, permissions, privacy, and licensing before using real data.
- Provide environment versions and install instructions when they matter.
- Remove unneeded outputs and debugging material.
- Review the Git diff and the notebook contents for secrets, private paths, and restricted material.
- Check the intended sharing permission, especially in Colab.
- Run the lightweight audit and the offline tests.

The directory’s [`.gitignore`](./.gitignore) excludes Python bytecode, cache directories, and Jupyter checkpoint files. No dataset is included with this lesson.
