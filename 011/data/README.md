# Data folders

No dataset is bundled with this template. Put authorized input files in `raw/`, keep originals unchanged, and document the source, acquisition date, license, and any access restrictions before use. Do not commit private, personal, licensed, or otherwise restricted data; the local `.gitignore` excludes data files while retaining these starter folders.

Use `interim/` for clearly described intermediate transformations and `processed/` for final analysis-ready outputs. Rebuild these from the original source when practical, rather than editing raw data in place. Keep code that reads, validates, or transforms data under `src/`, with tests for assumptions. `external/` is a reminder to document data received from third parties and its use conditions.

Folder names are conventions, not guarantees of correctness, privacy, permission, or reproducibility. Confirm that you are authorized to access, process, and store any real dataset before adding it to a project.
