---
course: mlops-engineer
title: Managing Model Versions with the MLflow Model Registry
month: 2
monthTitle: Experiment Tracking, Pipelines & Model Deployment
lesson: 2
summary: Learn how to use the MLflow Model Registry to register model versions, manage their lifecycle
  through stages, and promote models from development to production with governance and traceability.
objectives:
- Explain the purpose of the MLflow Model Registry and how it differs from experiment tracking
- Register a logged model and create new versions programmatically and via the UI
- Transition model versions through lifecycle stages (None, Staging, Production, Archived)
- Apply governance practices like aliases, tags, descriptions, and approval workflows
- Load and serve a specific registered model version or stage in downstream applications
video: mlo-m2-l02-managing-model-versions-with-the-mlflow-model-re.mp4
quiz:
- q: What is the key difference between a model version and an alias in the MLflow Model Registry?
  options:
  - Versions are mutable pointers; aliases are immutable snapshots
  - Versions are immutable snapshots; aliases are mutable pointers to a version
  - They are identical concepts with different names
  - Aliases can only be set in the UI, versions only via API
  answer: 1
  why: Each registered version is an immutable numbered snapshot, while an alias like @champion is a mutable
    pointer you can reassign to any version, enabling promotion without code changes.
- q: Which model URI loads the version currently pointed to by the 'champion' alias?
  options:
  - models:/fraud-detector/champion
  - models:/fraud-detector@champion
  - runs:/champion/model
  - models:/champion/fraud-detector
  answer: 1
  why: 'The alias syntax uses an @ sign: models:/<name>@<alias>. A slash with a name refers to a stage
    or version number, not an alias.'
- q: Why should production services reference models by name+alias rather than by run ID?
  options:
  - Run IDs are not supported by MLflow
  - It decouples deployment from training so you can promote/rollback by reassigning the alias
  - It makes models train faster
  - Aliases encrypt the model artifacts
  answer: 1
  why: Referencing by name+alias decouples the serving layer from any specific training run; you promote
    or roll back simply by reassigning the alias, with no change to serving code.
- q: What does the MLflow Model Registry add on top of experiment tracking?
  options:
  - A way to log metrics during training
  - A governed system of record for which model version is in which lifecycle stage
  - Automatic hyperparameter tuning
  - A replacement for data versioning
  answer: 1
  why: Experiment tracking records runs; the registry provides versioning, lifecycle stages/aliases, and
    governance metadata to manage which model is deployed.
- q: Name the parameter you pass to log_model to automatically register the model under a name.
  answer: registered_model_name
  why: Passing registered_model_name to mlflow.<flavor>.log_model registers the logged model and creates
    a new version in one step.
- q: List the four legacy lifecycle stages available for a model version.
  answer: None, Staging, Production, Archived
  why: These are the legacy stage labels; aliases are the modern recommended alternative in MLflow 2.9+.
resources:
- label: MLflow Model Registry Documentation
  url: https://mlflow.org/docs/latest/model-registry.html
- label: MLflow Deploy a model version / model URIs guide
  url: https://mlflow.org/docs/latest/models.html
- label: MLflow Model Registry aliases & tags reference
  url: https://mlflow.org/docs/latest/model-registry.html#using-registered-model-aliases
- label: MlflowClient API reference
  url: https://mlflow.org/docs/latest/python_api/mlflow.client.html
---

## Why a Model Registry?

Experiment tracking captures *runs* — parameters, metrics, and artifacts produced during training. But once you have a good model, you need a system of record to answer questions like: *Which model is in production right now? Who approved it? Can I roll back?* The **MLflow Model Registry** is a centralized store that manages the full lifecycle of your models.

The Registry sits on top of tracked runs. You log a model during a run, then **register** it to give it a named, versioned identity that survives independently of the experiment.

## Core Concepts

- **Registered Model**: a named entity (e.g. `fraud-detector`) that groups all versions.
- **Model Version**: an immutable, numbered snapshot (v1, v2, ...) created each time you register a model under a name.
- **Stage** (legacy): `None`, `Staging`, `Production`, `Archived` — lifecycle labels for a version.
- **Alias** (modern): a mutable named pointer like `@champion` or `@challenger` that you attach to a specific version. Aliases are the recommended replacement for stages in MLflow 2.9+.
- **Tags & Description**: free-form metadata for governance (e.g. `validation_status=passed`, owner, ticket links).

## Registering a Model

You can register at log time or after the fact:

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier

with mlflow.start_run() as run:
    model = RandomForestClassifier().fit(X_train, y_train)
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="fraud-detector"  # registers automatically
    )
```

Or register an existing run's artifact:

```python
result = mlflow.register_model(
    model_uri=f"runs:/{run.info.run_id}/model",
    name="fraud-detector"
)
print(result.version)  # e.g. 3
```

## Managing the Lifecycle

Use the `MlflowClient` to drive transitions and metadata:

```python
from mlflow.tracking import MlflowClient
client = MlflowClient()

# Add governance metadata
client.update_model_version(
    name="fraud-detector", version=3,
    description="RF, AUC 0.94, validated on Q2 holdout"
)
client.set_model_version_tag("fraud-detector", "3", "validation_status", "passed")
```

### Aliases (recommended)

```python
# Point the 'champion' alias at version 3
client.set_registered_model_alias("fraud-detector", "champion", 3)

# Later, promote a challenger
client.set_registered_model_alias("fraud-detector", "challenger", 4)
```

### Stage transitions (legacy API)

```python
client.transition_model_version_stage(
    name="fraud-detector", version=3, stage="Production",
    archive_existing_versions=True
)
```

## Loading Models for Inference

Downstream services reference models by name + alias/version, not by run ID — this decouples deployment from training:

```python
# By alias (modern)
model = mlflow.pyfunc.load_model("models:/fraud-detector@champion")

# By version
model = mlflow.pyfunc.load_model("models:/fraud-detector/3")

# By stage (legacy)
model = mlflow.pyfunc.load_model("models:/fraud-detector/Production")
```

Because aliases are mutable pointers, you can promote a new version by reassigning `@champion` — the serving layer picks it up without code changes.

## Governance & Promotion Workflow

A typical governed flow:

1. Data scientist trains and registers a candidate (v4).
2. CI runs automated validation; tags v4 `validation_status=passed`.
3. A reviewer inspects metrics and description, then assigns `@challenger`.
4. After A/B or shadow testing, an approver reassigns `@champion` to v4 and archives the old version.
5. Audit trail is preserved: every version, who changed it, and when.

Protect the registry with **access controls** (in MLflow on Databricks or behind a gateway) so only authorized roles can promote to production. Combine with **webhooks** or CI triggers to automate downstream redeployment when an alias changes.

## Key Takeaways

- The Registry is your single source of truth for *which model is where*.
- Versions are immutable; aliases/stages are mutable pointers.
- Prefer aliases + tags over legacy stages going forward.
- Reference models by name+alias in production to decouple serving from training.
