---
course: ml-engineer
title: Building Reproducible Data Pipelines
month: 4
monthTitle: 'Production ML: Pipelines, Evaluation, and Capstone'
lesson: 1
summary: Learn to construct automated, versioned data pipelines that reliably ingest, transform, validate,
  and serve data into training workflows—making your ML systems reproducible from raw source to trained
  model.
objectives:
- Explain why reproducibility matters in production ML and identify the components that must be versioned
- Design a modular pipeline with ingestion, transformation, validation, and serving stages
- Apply data and code versioning using tools like DVC and Git to make runs reproducible
- Implement data validation and schema checks to catch issues before training
- Orchestrate pipeline steps with a DAG-based tool and parameterize runs via configuration
- Connect pipeline outputs to training workflows with deterministic, traceable artifacts
video: mle-m4-l01-building-reproducible-data-pipelines.mp4
quiz:
- q: What does it mean for a pipeline stage to be idempotent?
  options:
  - It runs faster each time it executes
  - Running it multiple times with the same inputs yields the same output
  - It automatically retries on failure
  - It encrypts its output data
  answer: 1
  why: Idempotency means repeated execution on identical inputs produces identical outputs, which is essential
    for reproducibility and safe re-runs.
- q: In DVC, what is stored in Git versus remote storage?
  options:
  - Both data and code go to Git
  - Lightweight pointer files go to Git; actual data goes to remote storage
  - Data goes to Git; pointers go to remote storage
  - Everything is stored only in remote storage
  answer: 1
  why: DVC commits small .dvc pointer files to Git while pushing the large actual data files to remote
    object storage like S3 or GCS.
- q: Why should random seeds be set and recorded in a data pipeline?
  options:
  - To make the pipeline run faster
  - To make stochastic steps like splitting reproducible
  - To encrypt the dataset
  - To reduce memory usage
  answer: 1
  why: Recording seeds ensures stochastic operations such as train/test splits produce the same results
    across runs, preserving reproducibility.
- q: What is the purpose of data validation before transformation/training?
  options:
  - To compress the data
  - To fail fast and catch schema or quality issues before training on bad data
  - To version the data automatically
  - To speed up model inference
  answer: 1
  why: Validation enforces expectations on schema, types, and ranges so the pipeline stops loudly instead
    of silently training on corrupt data.
- q: Name one thing (besides code) that must be versioned to achieve full reproducibility.
  answer: Data (or configuration/parameters, or the environment/dependencies)
  why: Reproducibility requires versioning code, data, configuration, and environment together—any of
    data, config, or environment is a valid answer.
- q: Why does DVC only re-run stages whose dependencies or parameters changed?
  answer: It uses caching to skip unchanged stages, saving time while keeping outputs reproducible and
    traceable.
  why: DVC tracks deps, params, and outs per stage, so it recomputes only what changed, combining efficient
    caching with deterministic reproducibility.
resources:
- label: DVC Documentation — Data Version Control
  url: https://dvc.org/doc
- label: Great Expectations — Data Validation
  url: https://docs.greatexpectations.io
- label: Pandera — Statistical Data Validation for pandas
  url: https://pandera.readthedocs.io
- label: MLflow — Tracking and Lineage
  url: https://mlflow.org/docs/latest/index.html
---

## Why Reproducible Data Pipelines Matter

In production ML, a model is only as trustworthy as the data that produced it. If you cannot recreate the exact dataset, transformations, and parameters that generated a model, you cannot debug regressions, satisfy audits, or safely retrain. **Reproducibility** means that given the same inputs and code, you get the same outputs—every time.

A reproducible pipeline versions four things together:

- **Code** (transformation logic) via Git
- **Data** (raw and processed) via a data versioning tool
- **Configuration** (parameters, paths, hyperparameters) via config files
- **Environment** (dependencies) via lockfiles or containers

## Anatomy of a Data Pipeline

A typical pipeline is a directed acyclic graph (DAG) of stages:

1. **Ingestion** — pull raw data from sources (databases, APIs, object storage). Capture a snapshot or a queryable version.
2. **Validation** — check schema, types, ranges, null rates, and distribution drift before proceeding.
3. **Transformation** — clean, join, engineer features. Keep this deterministic (avoid `now()`, unseeded randomness).
4. **Splitting** — produce train/validation/test sets with fixed seeds and stable keys.
5. **Serving** — write versioned artifacts (feature tables, TFRecords, parquet) that training consumes.

Each stage should be **idempotent**: running it twice with the same inputs yields the same output.

## Versioning Data with DVC

[DVC](https://dvc.org) tracks large data files alongside Git. It stores lightweight `.dvc` pointer files in Git and pushes the actual data to remote storage (S3, GCS, etc.).

```bash
# Track a raw dataset
dvc add data/raw/transactions.csv
git add data/raw/transactions.csv.dvc .gitignore
git commit -m "Add raw transactions v1"

# Push data to remote
dvc remote add -d storage s3://my-bucket/dvcstore
dvc push
```

Now a teammate runs `git checkout <commit> && dvc pull` to retrieve the *exact* data tied to that code version.

## Defining Pipeline Stages

DVC pipelines (or tools like Airflow, Prefect, Kubeflow) let you declare stages with explicit dependencies and outputs. With DVC's `dvc.yaml`:

```yaml
stages:
  transform:
    cmd: python src/transform.py
    deps:
      - src/transform.py
      - data/raw/transactions.csv
    params:
      - transform.fillna_strategy
    outs:
      - data/processed/features.parquet
  split:
    cmd: python src/split.py
    deps:
      - data/processed/features.parquet
    params:
      - split.test_size
      - split.seed
    outs:
      - data/splits/
```

Run the whole graph with `dvc repro`. DVC re-executes only stages whose dependencies or params changed—this gives caching plus reproducibility.

## Parameterizing with Configuration

Keep all tunable values in a `params.yaml` rather than hardcoding them. This makes runs explicit and diffable.

```yaml
transform:
  fillna_strategy: median
split:
  test_size: 0.2
  seed: 42
```

Changing `seed` or `test_size` produces a new, tracked pipeline run. Always set and record random seeds.

## Data Validation

Validate data before it flows downstream. Libraries like Great Expectations or Pandera define expectations:

```python
import pandera as pa
from pandera import Column, Check

schema = pa.DataFrameSchema({
    "amount": Column(float, Check.greater_than(0)),
    "customer_id": Column(int, nullable=False),
    "category": Column(str, Check.isin(["a", "b", "c"])),
})

validated = schema.validate(df)  # raises on violation
```

Fail fast: a broken schema should stop the pipeline rather than silently train on garbage.

## Connecting to Training

Training reads versioned artifacts and records which data version it used (the Git commit / DVC hash). Log this into your experiment tracker (MLflow, W&B) so every model links back to its exact dataset. This closes the loop: model → params → data → raw source.

## Best Practices

- Make every stage **deterministic and idempotent**.
- Never mutate raw data in place; treat it as immutable.
- Store config separate from code; record seeds.
- Validate early and fail loudly.
- Tie model artifacts to data + code versions for full lineage.
