# Getting started

## Requirements

Install Python 3.10 or newer. The project pins MkDocs in `requirements.txt` so you can rebuild the same starter with a known direct dependency.

## Create an environment

From the `028` project folder, create and activate a virtual environment, then install the requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Preview locally

Run `python -m mkdocs serve` from the folder containing `mkdocs.yml`. Open the local URL printed by the command. The development server watches the source files and rebuilds the preview after edits.

To check a production-style build without starting the server, run `python -m mkdocs build --strict`. Fix warnings before publishing.
