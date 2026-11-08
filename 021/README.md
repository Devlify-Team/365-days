# Day 21 — ML model versioning with DVC

**Month:** Month 1: Foundations & GitHub Basics · **Topic:** ML Ops · **Primary:** DVC · **Alternatives:** MLflow, Weights & Biases (W&B) · **Slug:** `ml-model-versioning-with-dvc`

## Purpose

This compact exercise tracks a reproducible model-training stage separately from Git-managed code and pipeline metadata. `src/train.py` fits a straight line to the deliberately toy CSV `data/toy-training.csv` and writes `models/model.json`; the sample is illustrative, not real data or a production model.

## Run the pipeline

DVC is initialized locally inside this numbered folder with `no_scm = True`, so it does not reinitialize or nest the outer repository. From the repository root:

```bash
cd 021
uv tool install dvc
# Or install DVC in a dedicated Python environment: python -m pip install dvc

dvc repro
dvc status
cat models/model.json
```

This workspace was validated with DVC 3.67.1: `dvc repro` ran the `train` stage and produced a slope of 2 and intercept of 1; `dvc status` reported that the pipeline was up to date. The three standard-library trainer tests also passed.

`dvc.yaml` declares the stage command, source-script and CSV dependencies, and model output. The tracked `dvc.lock` records the dependency/output hashes for the reproduced run. DVC keeps the generated model in its local cache and working tree; `.gitignore` excludes the model, cache, and transient state from Git. The tiny CSV, code, pipeline definition, lockfile, and DVC configuration are in Git.

See DVC’s [getting-started guide for data versioning](https://dvc.org/doc/start/data-management/data-versioning) and its [pipeline definition guide](https://dvc.org/doc/user-guide/pipelines/defining-pipelines) for how `dvc.yaml`, `dvc.lock`, dependencies, and outputs work.

## What to commit

From the outer repository root, commit the pipeline and its source inputs/metadata—not the generated model or DVC cache:

```bash
git add 021/README.md 021/.gitignore 021/.dvcignore 021/.dvc/config \
  021/dvc.yaml 021/dvc.lock 021/data/toy-training.csv \
  021/src/train.py 021/tests/test_train.py
git commit -m "Add Day 021 DVC model-versioning example"
```

## Share artifacts with a team

This project has no shared DVC remote configured. Another checkout can recreate the model from the committed toy data and stage with `dvc repro`. For larger or shared artifacts, configure a team-approved remote, then push cached outputs; collaborators can pull them after obtaining the Git metadata:

```bash
dvc remote add -d <name> <url>
dvc push
# In another checkout:
dvc pull
```

DVC supports multiple storage backends; choose one approved by your team. Keep credentials in local DVC configuration or a secret manager, never in committed files. See the official [remote storage guide](https://dvc.org/doc/user-guide/data-management/remote-storage).

## Files

```text
021/
├── .dvc/config                 # no_scm = True; no remote configured
├── .dvcignore
├── .gitignore
├── README.md
├── data/toy-training.csv
├── dvc.lock                    # generated and tracked
├── dvc.yaml
├── models/model.json           # generated locally; ignored by Git
├── src/train.py
└── tests/test_train.py
```
