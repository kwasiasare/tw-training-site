---
course: data-scientist
title: Orchestrating the ML Lifecycle (Capstone)
month: 6
monthTitle: Productionization and MLOps
lesson: 4
summary: 'This capstone ties the module together by treating MLOps as a continuous loop: data, train,
  track, serve, monitor, and retrain. You''ll learn why orchestration matters, build a minimal pipeline
  as a DAG, add CI/CD that tests and deploys on merge, then complete a mini-project that productionizes
  your Module 3 predictive model end to end.'
objectives:
- Describe the MLOps lifecycle as a continuous loop connecting serving, tracking, and monitoring
- Explain why orchestration is needed to schedule and automate pipeline steps
- Model a pipeline as a Directed Acyclic Graph (DAG) using a modern orchestrator API
- Build a minimal, readable Airflow TaskFlow or Prefect pipeline that retrains and re-deploys
- Set up a CI/CD workflow that runs pytest and deploys on merge with GitHub Actions
- 'Productionize an existing model end to end: serve, track, monitor for drift, and schedule retraining'
video: dsc-m6-l04-orchestration-and-the-mlops-lifecycle.mp4
quiz:
- q: Which statement best describes the MLOps lifecycle?
  options:
  - 'A continuous loop: data, train, track, serve, monitor, then retrain'
  - A one-time linear process that ends the moment the model is deployed
  - Only the model-training step in isolation
  - A technique for avoiding version control
  answer: 0
  why: MLOps is a loop, not a one-shot deployment. Data flows into training, runs are tracked, the model
    is served, production is monitored, and drift or new data triggers retraining, closing the loop.
- q: What is the primary purpose of an orchestrator such as Apache Airflow or Prefect?
  options:
  - To replace your machine learning model with a rules engine
  - To automatically label your training data
  - To schedule and automate the steps of a pipeline expressed as a DAG
  - To store model artifacts and nothing else
  answer: 2
  why: An orchestrator schedules, runs, retries, and monitors the dependent steps of a workflow. Those
    steps are expressed as a DAG so the engine knows the order and dependencies.
- q: In a CI/CD pipeline for ML, what should run automatically on every push or pull request?
  options:
  - A full retrain on the entire production dataset
  - Automated tests such as pytest against the code and the pipeline
  - A manual code review with no automation
  - Deletion of the held-out test set
  answer: 1
  why: CI runs your automated tests on every change so broken code or a broken pipeline is caught before
    merge. Heavy retraining and deployment are separate, often gated steps.
- q: What does a DAG (Directed Acyclic Graph) guarantee about a pipeline?
  options:
  - That every task always runs at the same time in parallel
  - That tasks may form cycles and loop back on themselves
  - That no task will ever fail at runtime
  - That tasks run in a defined order with no circular dependencies
  answer: 3
  why: 'A DAG is directed and acyclic: edges define dependencies and order, and the absence of cycles
    means a task can never depend on itself, directly or transitively.'
- q: Why add a scheduled drift check as a step in the lifecycle?
  options:
  - To make model training run faster
  - To replace the need for a held-out test set
  - To detect when incoming data diverges from training data and trigger retraining
  - To reduce the number of input features automatically
  answer: 2
  why: Data drift degrades a deployed model silently. A scheduled drift check (Lesson 3) flags divergence
    between live and training data so the pipeline can alert or retrain before performance collapses.
- q: Name the experiment-tracking tool from Lesson 2 you would use to log parameters, metrics, and model
    artifacts during each automated training run.
  answer: MLflow
  why: MLflow records parameters, metrics, and artifacts per run and provides a model registry, so every
    orchestrated retrain is reproducible and comparable to past runs.
resources:
- label: 'Apache Airflow: TaskFlow API tutorial'
  url: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html
- label: 'GitHub Actions: Building and testing Python (CI)'
  url: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python
- label: 'Google Cloud: MLOps — Continuous delivery and automation pipelines in ML'
  url: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- label: 'ml-ops.org: MLOps Principles'
  url: https://ml-ops.org/content/mlops-principles
---

## The MLOps Lifecycle Is a Loop

Everything in this module clicks together when you stop seeing deployment as the finish line and start seeing it as one stop on a **continuous loop**:

```
data -> train -> track -> serve -> monitor -> retrain -> (back to data)
```

- **Data**: fresh data arrives from your warehouse or stream.
- **Train**: you fit the model (Module 3).
- **Track**: you log params, metrics, and artifacts with **MLflow** (Lesson 2).
- **Serve**: you expose predictions behind **FastAPI + Docker** (Lesson 1).
- **Monitor**: you watch for **data drift** and performance decay (Lesson 3).
- **Retrain**: drift or a schedule triggers a new run, and the loop closes.

The job of MLOps is to make this loop **automated, reproducible, and observable** instead of a sequence of manual notebook runs.

## Why Orchestration?

The steps above have **dependencies**: you cannot serve a model you have not trained, and you should not retrain before validating new data. Running them by hand does not scale and is not reproducible.

An **orchestrator** (Apache Airflow, Prefect, Dagster) lets you declare the steps and dependencies once, then **schedule** them, **retry** failures, **backfill** history, and **alert** on errors. You express the workflow as a **DAG** — a Directed Acyclic Graph — where each node is a task and each edge is a dependency. "Acyclic" means no task can loop back onto itself, so the engine can always compute a valid run order.

## A Minimal Pipeline as a DAG

Modern Airflow uses the **TaskFlow API** (`@dag` / `@task` decorators), which is far cleaner than the legacy operator style. Each `@task` function becomes a node; calling one with another's return value creates the dependency edge.

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(schedule='@daily', start_date=datetime(2026, 1, 1), catchup=False)
def churn_pipeline():
    @task
    def extract() -> str:
        # pull fresh data, return a path/URI
        return 'data/churn_latest.parquet'

    @task
    def check_drift(path: str) -> bool:
        # compare live vs training distribution (Lesson 3)
        return True  # drift detected

    @task
    def train_and_track(path: str) -> str:
        # fit model, log to MLflow, return run/model URI
        return 'models:/churn/Staging'

    @task
    def deploy(model_uri: str):
        # promote + redeploy the FastAPI service (Lesson 1)
        print(f'Deploying {model_uri}')

    p = extract()
    if_drift = check_drift(p)
    model = train_and_track(p)
    deploy(model)

churn_pipeline()
```

The graph reads top to bottom: extract feeds drift-check and training; training feeds deploy. Airflow schedules it daily and retries any failed task.

## CI/CD for ML

Orchestration automates the *runtime* loop; **CI/CD** automates *shipping the code* behind it. On every push or pull request, **Continuous Integration** runs your tests so a broken pipeline never reaches production. On merge, **Continuous Delivery** deploys.

Here is a minimal, valid GitHub Actions workflow that runs `pytest`, then deploys only on the main branch:

```yaml
name: ml-ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -q
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh
```

Tests should cover your code **and** your pipeline: schema checks, a tiny end-to-end run on sample data, and a check that the model meets a minimum metric threshold before promotion.

## Putting It All Together

The full lifecycle: code lives in Git; **CI** tests every change; on merge, **CD** ships the pipeline and serving image; the **orchestrator** runs the DAG on schedule; each run **trains** and **tracks** to MLflow; the best model is **served** via FastAPI; **monitoring** watches drift; and drift or the schedule **retrains**. Humans stay in the loop only for approvals and incidents.

## Mini-Project Brief: Productionize Your Module 3 Model

Take the predictive model from the **Module 3 mini-project (dsc-m3-l04)** and productionize it end to end using everything in this module. Keep it small but complete.

1. **Serve it** — wrap the saved pipeline in a **FastAPI** app with a `/predict` endpoint and containerize it with a **Dockerfile** (Lesson 1).
2. **Track training** — refactor training into a script that logs params, metrics, and the model artifact to **MLflow** and registers it (Lesson 2).
3. **Add a drift check** — write a function that compares a recent data batch against the training distribution and returns a drift flag (Lesson 3).
4. **Wire a pipeline** — connect extract -> drift-check -> train+track -> deploy as an Airflow TaskFlow (or Prefect) DAG on a daily schedule.
5. **Write a runbook** — a one-page Markdown doc: how to deploy, how to roll back, what the alerts mean, and who to page.

## Deliverables

- `app/main.py` (FastAPI) + `Dockerfile` that serves the model.
- `train.py` that logs a run to MLflow and registers the model.
- `monitoring/drift.py` with a drift-detection function and threshold.
- `pipeline.py` defining the scheduled DAG (TaskFlow `@dag`/`@task` or Prefect `@flow`/`@task`).
- `.github/workflows/ml-ci.yml` running `pytest` on push and deploying on merge.
- `tests/` with at least one pipeline test and one API test.
- `RUNBOOK.md` covering deploy, rollback, alerts, and on-call.
