---
course: mlops-engineer
title: Tracking Experiments and Models with MLflow
month: 2
monthTitle: Experiment Tracking, Pipelines & Model Deployment
lesson: 1
summary: Learn how to use MLflow Tracking to log parameters, metrics, and artifacts so your machine learning
  experiments become reproducible, comparable, and ready for production handoff. This lesson covers MLflow's
  core concepts, the tracking API, the Model Registry, and practical patterns for organizing runs and
  experiments.
objectives:
- Explain MLflow's core components (Tracking, Models, Registry) and the relationship between experiments
  and runs
- Instrument training code to log parameters, metrics, artifacts, and models using the MLflow Python API
- Use autologging to capture framework-specific details with minimal code
- Compare and reproduce experiments via the MLflow UI and stored run metadata
- Register, version, and stage models using the MLflow Model Registry
video: mlo-m2-l01-tracking-experiments-and-models-with-mlflow.mp4
quiz:
- q: What is the difference between an MLflow experiment and a run?
  options:
  - They are synonyms with no difference
  - An experiment is a single training execution; a run groups many experiments
  - An experiment is a named grouping of runs; a run is one execution of training code
  - A run stores parameters while an experiment stores metrics
  answer: 2
  why: An experiment is a named container (e.g., per project) that groups multiple runs, and each run
    is a single execution of your training code with its own params, metrics, and artifacts.
- q: Which MLflow call lets you record a numeric result that changes over training epochs as a time series?
  options:
  - mlflow.log_param with step
  - mlflow.log_metric with a step argument
  - mlflow.log_artifact
  - mlflow.set_tag
  answer: 1
  why: log_metric accepts a step argument, allowing the same metric to be logged repeatedly to form a
    time series; parameters are logged only once.
- q: What does mlflow.autolog() primarily provide?
  options:
  - Automatic deployment to production
  - Automatic capture of params, metrics, and the model for supported frameworks
  - Automatic dataset versioning and hashing
  - Automatic git commit logging
  answer: 1
  why: Autolog automatically captures parameters, metrics, and the model for supported libraries like
    scikit-learn and PyTorch with minimal code.
- q: Why is logging the model with a framework flavor (e.g., mlflow.sklearn.log_model) important?
  options:
  - It compresses the model to save space
  - It enables the model to be reloaded and served later
  - It prevents the model from being overwritten
  - It encrypts the model artifact
  answer: 1
  why: Logging via a flavor stores the model in a standardized, framework-aware format so MLflow can reload
    and serve it, including capturing its environment dependencies.
- q: Name two things (besides parameters and metrics) you should log to make a run fully reproducible.
  answer: The git commit SHA and the dataset version or hash (also environment/requirements).
  why: Reproducibility requires knowing the exact code (git SHA), the exact data (dataset version/hash),
    and the environment, in addition to params and metrics.
- q: In the Model Registry, what is the purpose of stages or aliases like 'Production' or '@champion'?
  answer: They mark which model version is active for a given environment/use so serving systems can load
    it by stage/alias instead of a specific run ID.
  why: Stages and aliases decouple deployment from specific runs, letting serving layers reference models:/name/Production
    and promote versions without code changes.
resources:
- label: MLflow Tracking Documentation
  url: https://mlflow.org/docs/latest/tracking.html
- label: MLflow Model Registry Guide
  url: https://mlflow.org/docs/latest/model-registry.html
- label: MLflow Python API Reference
  url: https://mlflow.org/docs/latest/python_api/mlflow.html
- label: MLflow Autologging Documentation
  url: https://mlflow.org/docs/latest/tracking/autolog.html
---

## Why Experiment Tracking Matters

Machine learning is inherently experimental. You try different hyperparameters, features, and architectures, and each change produces a result. Without a system to record what you did and what happened, you lose the ability to answer basic questions: *Which run produced the best model? What learning rate did I use? Can I reproduce that result next week?*

**MLflow Tracking** solves this by recording the inputs (parameters), outputs (metrics), and outputs/files (artifacts) of each model run in a structured, queryable store.

## Core Concepts

- **Experiment**: A named grouping of runs, usually corresponding to one project or task (e.g., `churn-prediction`).
- **Run**: A single execution of your training code. Each run has a unique ID and stores params, metrics, tags, and artifacts.
- **Parameters**: Inputs/config you set, like `learning_rate` or `n_estimators`. Logged once per run.
- **Metrics**: Numeric results you measure, like `accuracy` or `loss`. Can be logged repeatedly (e.g., per epoch) to form a time series.
- **Artifacts**: Output files — models, plots, data samples, confusion matrices.
- **Tracking Server / Backend Store**: Where data is stored. Locally it defaults to a `mlruns/` directory; in production you point to a tracking server backed by a database and artifact store (e.g., S3).

## The Tracking API

The typical pattern uses a context manager so the run closes cleanly:

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

mlflow.set_tracking_uri("http://localhost:5000")  # or local path
mlflow.set_experiment("churn-prediction")

with mlflow.start_run(run_name="rf-baseline"):
    params = {"n_estimators": 200, "max_depth": 8}
    mlflow.log_params(params)

    model = RandomForestClassifier(**params).fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    mlflow.log_metric("accuracy", acc)
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.sklearn.log_model(model, artifact_path="model")
```

Key calls:
- `mlflow.log_param` / `log_params` — record configuration.
- `mlflow.log_metric` / `log_metrics` — record results; pass `step=` for time series.
- `mlflow.log_artifact` / `log_artifacts` — store files or directories.
- `mlflow.<flavor>.log_model` — store the model in a framework-specific *flavor* so it can be reloaded and served.

## Autologging

For supported libraries (scikit-learn, PyTorch, TensorFlow, XGBoost, LightGBM), a single call captures params, metrics, and the model automatically:

```python
mlflow.autolog()  # or mlflow.sklearn.autolog()
```

Autolog is great for getting started fast, but combine it with explicit `log_*` calls for custom metrics or business-specific artifacts.

## Comparing and Reproducing Runs

Launch the UI with `mlflow ui` (default port 5000). You can:
- Sort and filter runs by metric.
- Select multiple runs to compare params/metrics side by side.
- Inspect logged artifacts and download models.

For reproducibility, also log the **git commit**, **dataset version/hash**, and **environment** (MLflow captures a `conda.yaml`/`requirements.txt` with logged models). Use tags like `mlflow.set_tag("git_sha", sha)` to make runs traceable.

## The Model Registry

The Model Registry is a centralized store for managing the lifecycle of models:

```python
mlflow.register_model(
    model_uri="runs:/<run_id>/model",
    name="churn-classifier"
)
```

It provides:
- **Versioning** — each registration increments a version number.
- **Stages/aliases** — mark versions as `Staging`, `Production`, or use aliases like `@champion`.
- **Lineage** — links a registered version back to the run that produced it.

This bridges experimentation and deployment: your serving layer can load `models:/churn-classifier/Production` without knowing which exact run it came from.

## Practical Tips

- Use a remote tracking server in teams so everyone logs to the same place.
- Name runs and use consistent experiment names.
- Log enough to reproduce, but avoid logging huge raw datasets as artifacts — log a hash or pointer instead.
- Set `MLFLOW_TRACKING_URI` as an environment variable in CI/CD pipelines.
