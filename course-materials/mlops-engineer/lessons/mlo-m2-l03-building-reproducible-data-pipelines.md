---
course: mlops-engineer
title: Building Reproducible Data Pipelines
month: 2
monthTitle: Experiment Tracking, Pipelines & Model Deployment
lesson: 3
summary: Learn to build automated, reproducible data pipelines that ingest, validate, transform, and version
  data for reliable model training. Covers DAG orchestration, data versioning with DVC, schema validation,
  and CI-style automation.
objectives:
- Explain why reproducibility matters in data pipelines and what factors break it
- Design a modular ingestion-to-transformation pipeline using DAG-based orchestration
- Version datasets and pipeline outputs using tools like DVC and content hashing
- Add data validation and schema checks to catch quality issues before training
- Parameterize and automate pipeline runs so they execute identically across environments
video: mlo-m2-l03-building-reproducible-data-pipelines.mp4
quiz:
- q: What does it mean for a pipeline stage to be idempotent?
  options:
  - It runs faster on each subsequent execution
  - Running it twice with the same input yields the same output
  - It automatically parallelizes across machines
  - It deletes its inputs after running
  answer: 1
  why: Idempotency means repeated execution with identical inputs produces identical results, which is
    essential for safe retries and reproducibility.
- q: Why use DVC instead of committing large data files directly to Git?
  options:
  - Git cannot store binary files at all
  - DVC stores data in remote storage and keeps lightweight hashed pointers in Git
  - DVC encrypts all data automatically
  - Git deletes large files after each commit
  answer: 1
  why: DVC keeps a small pointer with a content hash in Git while the actual data lives in remote object
    storage, giving versioning without bloating the repo.
- q: Which of these most directly threatens pipeline reproducibility?
  options:
  - Using a fixed random seed
  - Storing raw data immutably
  - Pulling from a mutable source table that changes over time
  - Declaring stages in a DAG
  answer: 2
  why: A mutable source that changes underneath you means the same code can produce different datasets,
    breaking reproducibility.
- q: What is the main purpose of adding data validation (e.g., Pandera or Great Expectations) to a pipeline?
  options:
  - To speed up data transformation
  - To fail fast on schema/quality issues before they corrupt training
  - To compress data for storage
  - To replace the need for version control
  answer: 1
  why: Validation enforces expectations on types, ranges, and nulls so bad data is caught at the boundary
    rather than silently degrading the model.
- q: Name one practice that helps make a train/test split deterministic across runs.
  answer: Setting a fixed random seed
  why: Fixing the random seed ensures sampling and splitting produce the same partitions every run, a
    key part of determinism.
- q: In a DVC pipeline, what does running 'dvc repro' do when only one stage's dependencies have changed?
  answer: It re-runs only the changed stage (and downstream stages), reusing cached outputs for the rest
  why: DVC tracks dependencies and caches outputs, so it re-executes only the affected stages, saving
    time while keeping results consistent.
resources:
- label: DVC Documentation — Data Pipelines
  url: https://dvc.org/doc/start/data-pipelines
- label: Great Expectations Documentation
  url: https://docs.greatexpectations.io/
- label: 'Pandera: Statistical Data Validation'
  url: https://pandera.readthedocs.io/
- label: Prefect Orchestration Docs
  url: https://docs.prefect.io/
---

## Why Reproducible Data Pipelines

A model is only as trustworthy as the data that produced it. If you cannot recreate the exact dataset used for a training run, you cannot reliably debug regressions, audit results, or roll back. **Reproducibility** means that given the same inputs, code, and configuration, the pipeline produces the same output every time.

Common reproducibility killers:

- Mutable data sources (a table that changes underneath you)
- Uncontrolled randomness (no fixed seeds)
- Hidden manual steps (someone edits a CSV by hand)
- Untracked code or config changes
- Environment drift (different library versions)

## Anatomy of a Data Pipeline

A typical pipeline is a directed acyclic graph (DAG) of stages:

1. **Ingestion** — pull raw data from sources (databases, APIs, object storage) into a raw landing zone. Keep raw data immutable.
2. **Validation** — check schema, types, ranges, and nulls before processing.
3. **Transformation / Feature engineering** — clean, join, aggregate, and encode.
4. **Splitting** — produce train/validation/test sets deterministically.
5. **Versioning & registration** — record the output dataset with a content hash and metadata.

Each stage should be **idempotent**: running it twice with the same input yields the same result.

## Orchestration with DAGs

Tools like Airflow, Prefect, Dagster, or DVC pipelines let you declare stages and their dependencies. The orchestrator runs stages in order, caches outputs, and re-runs only what changed.

```yaml
# dvc.yaml — declarative pipeline stages
stages:
  ingest:
    cmd: python src/ingest.py --date ${date}
    deps:
      - src/ingest.py
    outs:
      - data/raw/events.parquet
  validate:
    cmd: python src/validate.py
    deps:
      - src/validate.py
      - data/raw/events.parquet
  transform:
    cmd: python src/transform.py
    deps:
      - src/transform.py
      - data/raw/events.parquet
    outs:
      - data/processed/features.parquet
```

With `dvc repro`, only stages whose dependencies changed are re-executed.

## Data Versioning

Git handles code but not large data. **DVC** (Data Version Control) stores data in remote object storage and tracks lightweight pointers (`.dvc` files) in Git. The pointer holds a content hash, so checking out a commit restores the exact dataset.

```bash
dvc add data/raw/events.parquet   # creates events.parquet.dvc with md5 hash
git add data/raw/events.parquet.dvc .gitignore
dvc push                          # upload data to remote (S3, GCS, etc.)
```

Now a teammate runs `git checkout <commit> && dvc pull` to get the identical data. Tie a dataset version to each model training run for full lineage.

## Data Validation

Validate early to fail fast. Libraries like Great Expectations or Pandera express expectations as code.

```python
import pandera as pa
from pandera import Column, Check

schema = pa.DataFrameSchema({
    "user_id": Column(int, nullable=False),
    "amount": Column(float, Check.ge(0)),
    "country": Column(str, Check.isin(["US", "UK", "DE"])),
})

validated = schema.validate(df)  # raises on violation
```

Validation guards against silent data drift, malformed inputs, and schema breaks that would otherwise corrupt training.

## Parameterization and Determinism

Drive behavior with a config file, not hard-coded values, so runs are explicit and repeatable.

```yaml
# params.yaml
seed: 42
split:
  test_size: 0.2
filters:
  min_date: '2024-01-01'
```

Always set random seeds for sampling and splitting, pin library versions in a lockfile, and avoid wall-clock-dependent logic. Record the config, code commit, and data hash together as the run's fingerprint.

## Putting It Together

A production-grade reproducible pipeline:

- Stores raw data immutably and versions every artifact
- Declares stages as a cached DAG
- Validates data at boundaries
- Is parameterized and seeded
- Records lineage linking data, code, and config to each model

This foundation makes downstream training, deployment, and auditing dramatically more reliable.
