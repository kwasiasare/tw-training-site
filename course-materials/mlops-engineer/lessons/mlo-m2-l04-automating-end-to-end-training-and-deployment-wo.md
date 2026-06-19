---
course: mlops-engineer
title: Automating End-to-End Training and Deployment Workflows
month: 2
monthTitle: Experiment Tracking, Pipelines & Model Deployment
lesson: 4
summary: This lesson shows how to connect data preparation, model training, evaluation, and MLflow registration
  into a single automated, reproducible workflow that produces a deployable model artifact. You'll learn
  the building blocks of an end-to-end pipeline, how to orchestrate them, gate promotion on quality, and
  trigger deployment.
objectives:
- Describe the stages of an end-to-end training-to-deployment pipeline and how they connect
- Build a modular pipeline that runs data prep, training, evaluation, and MLflow registration as one workflow
- Use MLflow tracking and the Model Registry to version, stage, and promote models
- Implement quality gates that conditionally register and promote models based on evaluation metrics
- Trigger deployment automatically from a registered model using CI/CD or orchestration tools
video: mlo-m2-l04-automating-end-to-end-training-and-deployment-wo.mp4
quiz:
- q: What is the primary reason to register a model in the MLflow Model Registry only after a quality
    gate passes?
  options:
  - To save storage space on the tracking server
  - To prevent underperforming models from being promoted and deployed
  - Because registration is required before training
  - To reduce the number of experiment runs
  answer: 1
  why: The quality gate ensures only models meeting metric and quality criteria are registered and eligible
    for promotion, preventing bad models from reaching production.
- q: Why should pipeline stages pass artifacts through a shared store or run IDs rather than in-memory
    objects?
  options:
  - It makes the code shorter
  - It keeps stages decoupled, restartable, and orchestrator-friendly
  - In-memory objects are always faster
  - MLflow forbids in-memory data
  answer: 1
  why: Using a shared store/run IDs decouples stages so each can run independently, be retried, and be
    scheduled by an orchestrator across separate processes or machines.
- q: Which MLflow Registry behavior preserves a rollback path when promoting a new Production model?
  options:
  - Deleting all older versions
  - Archiving existing versions instead of deleting them
  - Disabling the tracking server
  - Re-running training from scratch
  answer: 1
  why: Using archive_existing_versions=True moves the old Production model to Archived rather than deleting
    it, so you can roll back if the new version misbehaves.
- q: Which tools are commonly used to orchestrate a scheduled end-to-end retraining DAG?
  options:
  - Airflow, Prefect, or Dagster
  - Only Jupyter notebooks
  - A spreadsheet
  - Manual SSH scripts
  answer: 0
  why: Airflow, Prefect, and Dagster are workflow orchestrators designed to define and schedule DAGs of
    dependent tasks, ideal for retraining pipelines.
- q: In one sentence, name two checks (beyond accuracy) a quality gate might enforce before promoting
    a model.
  answer: 'Examples: fairness/bias checks, inference latency, model size, or comparison against the current
    production model''s metrics.'
  why: Gates should consider operational and ethical criteria—like fairness, latency, and size—not just
    predictive accuracy, to ensure the model is truly production-ready.
- q: What does referencing a model by the URI 'models:/churn-model/Production' allow a deployment job
    to do?
  answer: It lets the deployment always fetch the current Production-stage version of the model without
    hard-coding a specific version number.
  why: Stage-based URIs decouple deployment from specific version numbers, so promotions automatically
    point serving to the right model and enable clean rollbacks.
resources:
- label: MLflow Model Registry Documentation
  url: https://mlflow.org/docs/latest/model-registry.html
- label: MLflow Tracking Documentation
  url: https://mlflow.org/docs/latest/tracking.html
- label: Apache Airflow Concepts (DAGs & Tasks)
  url: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html
- label: KServe Model Serving Documentation
  url: https://kserve.github.io/website/
---

## Why Automate End-to-End Workflows

Manual hand-offs between data scientists and engineers cause drift, broken reproducibility, and slow releases. An automated workflow links every stage—data ingestion, feature processing, training, evaluation, registration, and deployment—so a single trigger produces a versioned, deployable model with full lineage.

Goals of automation:

- **Reproducibility**: same code + same data + same params = same model.
- **Traceability**: every model maps to a run, dataset version, and metrics.
- **Speed & safety**: quality gates prevent bad models from reaching production.

## Anatomy of the Pipeline

A typical end-to-end workflow has these stages:

1. **Data prep** — pull raw data, validate schema, build features, output a versioned dataset.
2. **Train** — fit the model, log params/metrics/artifacts to MLflow.
3. **Evaluate** — compute metrics on a held-out set; compare against a baseline or current production model.
4. **Register** — if the model passes the gate, register it in the MLflow Model Registry.
5. **Promote & deploy** — transition the model to Staging/Production and trigger a deployment.

Keep each stage **modular** (a function or script with clear inputs/outputs) so it can be tested, reused, and orchestrated independently.

## Wiring It Together with MLflow

MLflow tracking captures runs; the Model Registry manages versions and stages.

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("churn-prediction")

def train_and_register(X_train, y_train, X_val, y_val, params, threshold=0.80):
    with mlflow.start_run() as run:
        mlflow.log_params(params)
        model = RandomForestClassifier(**params).fit(X_train, y_train)
        f1 = f1_score(y_val, model.predict(X_val))
        mlflow.log_metric("val_f1", f1)
        mlflow.sklearn.log_model(model, artifact_path="model")

        # Quality gate
        if f1 >= threshold:
            uri = f"runs:/{run.info.run_id}/model"
            mlflow.register_model(uri, "churn-model")
        return f1
```

## Quality Gates and Promotion

Never auto-deploy unconditionally. Use a gate that compares the candidate to the current Production model:

```python
from mlflow.tracking import MlflowClient
client = MlflowClient()

def promote_if_better(name, candidate_version, metric, prod_metric):
    if metric > prod_metric:
        client.transition_model_version_stage(
            name=name, version=candidate_version,
            stage="Production", archive_existing_versions=True)
```

Gate criteria can include accuracy/F1 thresholds, fairness checks, latency, and model size. Failing the gate should stop the pipeline and alert the team.

## Orchestration

Chain stages with an orchestrator so they run on a schedule or trigger:

- **Airflow / Prefect / Dagster** — define a DAG of tasks; good for scheduled retraining.
- **GitHub Actions / GitLab CI** — trigger on code push or via webhook when a model is registered.
- **MLflow Recipes / Kubeflow Pipelines** — ML-native pipeline definitions.

Pass artifacts between stages via a shared store (object storage, dataset version IDs, or MLflow run IDs) rather than in-memory objects.

## Triggering Deployment

Once a model reaches `Production`, trigger deployment by:

1. **Registry webhook / event** → CI job builds a serving container referencing the model URI `models:/churn-model/Production`.
2. **Deploy** to a serving target (KServe, SageMaker, a FastAPI container) using a rolling or canary strategy.
3. **Smoke test** the live endpoint, then route traffic.

## Best Practices

- Parameterize everything (config files, not hard-coded values).
- Make stages **idempotent** and restartable.
- Log data and code versions alongside the model for full lineage.
- Keep a rollback path: previous Production version stays archived, not deleted.
- Monitor post-deploy and feed signals back to trigger retraining.
