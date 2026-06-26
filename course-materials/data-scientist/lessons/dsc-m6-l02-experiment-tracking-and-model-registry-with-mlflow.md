---
course: data-scientist
title: Experiment Tracking and Model Registry with MLflow
month: 6
monthTitle: Productionization and MLOps
lesson: 2
summary: Learn to make machine learning reproducible and production-ready with MLflow. This lesson covers
  tracking runs (params, metrics, artifacts, and the model itself), comparing runs in the MLflow UI, and
  using the Model Registry to version and promote models with aliases. You will finish by loading a registered
  model back for serving, connecting tracking to deployment.
objectives:
- Explain why experiment tracking is essential for reproducibility and comparing model runs
- Log parameters, metrics, and artifacts for a run using the MLflow tracking API
- Log a trained scikit-learn model with mlflow.sklearn using the MLflow 3.x name= argument
- Compare and rank runs visually in the MLflow UI to select the best model
- Register a model and manage versions, promoting them with aliases such as champion
- Load a registered model back by alias to serve predictions in production
video: dsc-m6-l02-experiment-tracking-and-model-registry-with-mlflow.mp4
quiz:
- q: What is the primary value of experiment tracking with MLflow?
  options:
  - It automatically increases model accuracy
  - It records params, metrics, and artifacts so runs are reproducible and comparable
  - It removes the need for any version control system
  - It only works with deep learning frameworks
  answer: 1
  why: Tracking captures the inputs (params), outputs (metrics), and artifacts of every run, so you can
    reproduce a result months later and answer 'which parameters gave that score?' by comparing runs instead
    of guessing.
- q: In MLflow 3.x, which keyword argument names the saved model when calling mlflow.sklearn.log_model()?
  options:
  - path=
  - model_name=
  - artifact_path=
  - name=
  answer: 3
  why: MLflow 3.x uses name= to identify the logged model (e.g., name="model"). The older 2.x API used
    artifact_path=, which is why pinning the version matters when reading code or docs.
- q: Which MLflow call records numeric performance values such as f1 and roc_auc for a run?
  options:
  - mlflow.log_metrics()
  - mlflow.log_params()
  - mlflow.log_artifacts()
  - mlflow.sklearn.log_model()
  answer: 0
  why: log_metrics() stores numeric scores. log_params() stores hyperparameters like C and max_iter, log_artifacts()
    stores output files like plots, and log_model() stores the serialized model.
- q: What is the modern, recommended way to mark a registered model version as the one production should
    use?
  options:
  - Delete all older versions so only one remains
  - Rename the experiment to 'production'
  - Assign an alias like 'champion' to a version with set_registered_model_alias
  - Retrain the model from scratch each deployment
  answer: 2
  why: Aliases (e.g., champion) are the modern promotion mechanism; you point an alias at a specific version
    with MlflowClient().set_registered_model_alias(). Stage transitions (Staging/Production) are the older,
    now-discouraged API.
- q: Which URI loads the registered model version currently carrying the 'champion' alias?
  options:
  - models:/churn-model/champion
  - models:/churn-model@champion
  - runs:/churn-model@champion
  - model://churn-model:champion
  answer: 1
  why: 'The alias syntax uses an @ between the model name and the alias: models:/churn-model@champion.
    The slash form (models:/name/version) is for a numeric version, and runs:/ refers to a run artifact,
    not a registered model.'
- q: Name the MLflow function, typically used as a context manager with 'with', that opens a new tracked
    run.
  answer: mlflow.start_run
  why: mlflow.start_run() begins a run; used as 'with mlflow.start_run():' it ensures the run is properly
    closed and that all params, metrics, and the model are logged under that single run.
resources:
- label: MLflow Tracking Documentation
  url: https://mlflow.org/docs/latest/ml/tracking/
- label: MLflow Model Registry Documentation
  url: https://mlflow.org/docs/latest/ml/model-registry/
- label: mlflow.sklearn Python API Reference
  url: https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html
- label: 'ML Experiment Tracking: What It Is and Why It Matters'
  url: https://neptune.ai/blog/ml-experiment-tracking
---

## Why Tracking Matters

Every data scientist has lived this nightmare: a model scored beautifully last Tuesday, but nobody recorded the exact features, hyperparameters, or random seed that produced it. **Experiment tracking** ends the guesswork. A tracking tool records the inputs and outputs of every training run so results are **reproducible** and **comparable**.

MLflow is the de facto open-source standard. This lesson uses **MLflow 3.x** (install with `pip install "mlflow>=3,<4"`). The core abstractions are:

- An **experiment** groups related runs (e.g., all attempts at a churn model).
- A **run** is a single execution: its params, metrics, artifacts, and model.

With tracking in place, "which params gave that score?" becomes a query, not a memory test.

## Logging a Run

You wrap training in `mlflow.start_run()` and log three kinds of information: **parameters** (the knobs you set), **metrics** (the scores you measured), and **artifacts** (any output files such as plots or reports).

```python
import mlflow
from sklearn.linear_model import LogisticRegression

mlflow.set_experiment("churn-model")

with mlflow.start_run():
    model = LogisticRegression(C=1.0, max_iter=1000)
    model.fit(X_train, y_train)

    mlflow.log_params({"C": 1.0, "max_iter": 1000})
    mlflow.log_metrics({"f1": 0.82, "roc_auc": 0.90})
    mlflow.log_artifact("confusion_matrix.png")
```

Each `with` block is one run. Re-run the script with different settings and MLflow keeps a tidy history of every attempt.

## Logging the Model Itself

Params and metrics describe a run, but you also want the **trained model** saved so it can be reloaded later. The `mlflow.sklearn` flavor serializes the estimator along with its environment.

```python
with mlflow.start_run():
    # ... log_params / log_metrics ...
    mlflow.sklearn.log_model(model, name="model")  # MLflow 3.x (2.x used artifact_path=)
```

**Version note:** MLflow 3.x uses `name=` to identify the logged model. MLflow 2.x used `artifact_path=` instead, so older tutorials will show `mlflow.sklearn.log_model(model, artifact_path="model")`. The behavior is the same; only the keyword changed. Pinning your MLflow version keeps the API unambiguous.

## Comparing Runs in the MLflow UI

Start the UI locally with:

```bash
mlflow ui
```

Then open `http://localhost:5000`. Select your experiment and you will see a table of runs, one row each, with columns for every param and metric. From here you can:

- **Sort** by a metric (e.g., highest `roc_auc`) to find the best run instantly.
- **Select several runs** and click *Compare* to see side-by-side params and metric charts.
- **Drill into** any run to view its artifacts and logged model.

This visual comparison replaces spreadsheets full of copy-pasted numbers and makes model selection an evidence-based decision.

## The Model Registry

Tracking answers "what did I try?" The **Model Registry** answers "what is in production?" It is a centralized store of named models, each with numbered **versions** and a lifecycle.

The simplest path is to register a model at log time with `registered_model_name`:

```python
with mlflow.start_run():
    # ... log params and metrics first ...
    mlflow.sklearn.log_model(
        model,
        name="model",
        registered_model_name="churn-model",
    )
```

You can also register an existing run's model after the fact:

```python
result = mlflow.register_model(
    "runs:/<run_id>/model", "churn-model")
```

The first registration creates **Version 1**; each subsequent one increments to Version 2, 3, and so on. Nothing is overwritten, so you can always roll back.

## Promoting with Aliases

How do you say "this version is the one production should serve"? The **modern** approach is **aliases**: human-readable pointers like `champion` or `challenger` that you attach to a specific version.

```python
from mlflow import MlflowClient

client = MlflowClient()
client.set_registered_model_alias(
    name="churn-model", alias="champion", version=3)
```

When a better model arrives, repoint `champion` to the new version. Consumers reference the alias, never a hard-coded number.

**Version note:** older MLflow used **stage transitions** (`Staging`, `Production`) via `transition_model_version_stage`. Stages are now deprecated in favor of aliases, which are more flexible because you can define as many as you need.

## Loading a Registered Model for Serving

This closes the loop with the deployment workflow from the previous lesson. Instead of shipping a pickle file by hand, your serving code pulls the current champion straight from the registry by alias:

```python
import mlflow.sklearn

model = mlflow.sklearn.load_model(
    "models:/churn-model@champion")
predictions = model.predict(X_new)
```

The URI `models:/churn-model@champion` resolves the alias to whatever version is current, so promoting a new model needs **no code change** in the service. You could also load a fixed version with `models:/churn-model/3` when you need strict pinning. This alias-based loading is the bridge from experimentation to reliable, reproducible production serving.
