---
course: mlops-engineer
title: 'Capstone: Build an End-to-End Production MLOps System'
month: 4
monthTitle: Cloud Deployment, Monitoring & Capstone
lesson: 4
summary: 'This capstone lesson guides you through architecting and building a complete, production-grade
  MLOps system that ties together every skill from the course: containerization, automated training and
  inference pipelines, CI/CD, cloud infrastructure, and live monitoring. You''ll plan the architecture,
  implement each layer, and produce a portfolio-ready project that demonstrates end-to-end ownership of
  a deployed ML service.'
objectives:
- Design a reference architecture that connects data, training, serving, CI/CD, and monitoring components
- Containerize a model service and reproducibly orchestrate training and inference pipelines
- Provision cloud infrastructure as code and deploy a model behind a versioned, scalable endpoint
- Implement CI/CD that automates testing, building, and deployment with safe rollout strategies
- Instrument the system with monitoring for latency, errors, and data/model drift, with alerting
- Package the project for a portfolio with clear documentation and reproducibility
video: mlo-m4-l04-capstone-build-an-end-to-end-production-mlops-sy.mp4
quiz:
- q: What is the primary purpose of a model promotion gate in the training pipeline?
  options:
  - To speed up training
  - To only register a new model if it outperforms the current production model
  - To reduce Docker image size
  - To rotate cloud secrets
  answer: 1
  why: The gate compares new model metrics against the production baseline and blocks registration if
    the new model is worse, preventing regressions from reaching production.
- q: Which deployment strategy lets you roll back a bad model release without downtime?
  options:
  - Recreate/big-bang deploy
  - Blue-green or canary deployment
  - Manual SSH copy
  - Deleting the old container first
  answer: 1
  why: Blue-green and canary strategies keep a known-good version available, so traffic can shift back
    instantly if the new release misbehaves.
- q: Why is monitoring only infrastructure metrics (CPU, latency) insufficient for ML systems?
  options:
  - Infra metrics are always wrong
  - It misses data and model-quality issues like drift that degrade predictions silently
  - Latency cannot be measured in containers
  - Prometheus does not support ML
  answer: 1
  why: Models can keep responding quickly while their predictions degrade due to data or concept drift;
    you need data/model-quality monitoring to catch this.
- q: What practice makes infrastructure reproducible and reviewable in the capstone?
  options:
  - Clicking through the cloud console manually
  - Infrastructure as Code (e.g., Terraform)
  - Storing config only in your head
  - Hardcoding resources in the app
  answer: 1
  why: Infrastructure as Code defines resources declaratively in version control, making provisioning
    reproducible, reviewable, and auditable.
- q: Name one statistical method you can use to detect feature data drift between live traffic and the
    training reference.
  answer: PSI (Population Stability Index) or a KS test
  why: Both PSI and the Kolmogorov-Smirnov test compare distributions of incoming features against the
    training reference to flag drift.
- q: In one sentence, what single quality most distinguishes a strong MLOps capstone in a portfolio?
  answer: Reproducibility — a reviewer can set it up and run the whole system with minimal effort (e.g.,
    one command).
  why: Reproducibility demonstrates that the system is truly engineered and operable, not just a one-off
    notebook that works only on your machine.
resources:
- label: MLflow Documentation — Model Registry & Tracking
  url: https://mlflow.org/docs/latest/index.html
- label: Evidently AI — Data & Model Drift Monitoring
  url: https://docs.evidentlyai.com/
- label: Terraform Documentation — Infrastructure as Code
  url: https://developer.hashicorp.com/terraform/docs
- label: 'Google Cloud — MLOps: Continuous delivery and automation pipelines in ML'
  url: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
---

## Capstone Overview

This is the integration lesson where the individual pieces you've learned — Docker, pipelines, CI/CD, cloud infra, and monitoring — come together into a single deployed system. The goal is not to learn a new tool but to demonstrate **end-to-end ownership**: from raw data to a monitored, production endpoint that can be retrained and redeployed automatically.

Treat this as a portfolio project. Hiring managers want to see that you can connect components, make sound trade-offs, and operate a system after deployment — not just train a model in a notebook.

## Reference Architecture

A typical end-to-end system has five planes:

1. **Data & Feature layer** — versioned datasets (DVC or object storage), optional feature store.
2. **Training pipeline** — orchestrated steps (ingest → validate → train → evaluate → register) producing a versioned model in a registry (e.g., MLflow).
3. **Serving layer** — a containerized inference API (FastAPI + Docker) behind a scalable runtime (Kubernetes, ECS, or a managed endpoint).
4. **CI/CD** — Git-triggered pipelines that test, build images, push to a registry, and deploy with controlled rollout.
5. **Monitoring & observability** — metrics (Prometheus/Grafana), logging, and drift detection feeding alerts and retraining triggers.

The planes connect through artifacts: data versions, model versions in the registry, and container image tags. Each handoff should be reproducible and traceable.

## Step 1 — Scope and Success Criteria

Pick a realistic problem (e.g., churn prediction, image classification, demand forecasting). Define:

- Business metric and ML metric (e.g., F1, RMSE) with target thresholds.
- Latency and throughput SLOs for the endpoint (e.g., p95 < 200ms).
- A clear definition of "production-ready": automated tests pass, model registered, endpoint live, dashboards show traffic, alerts configured.

## Step 2 — Containerize the Service

Wrap inference in a FastAPI app, load the model from the registry, and define a `/predict` and `/health` endpoint. Build a slim image with a multi-stage Dockerfile and pin dependencies.

```dockerfile
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Step 3 — Build the Training Pipeline

Orchestrate the steps so a single command (or trigger) reproduces a model. Validate inputs, train, evaluate against thresholds, and **only register** the model if it beats the current production version.

```python
if new_metrics["f1"] > prod_metrics["f1"]:
    mlflow.register_model(model_uri, "churn-model")
else:
    raise ValueError("Model did not beat production baseline")
```

## Step 4 — Infrastructure as Code

Provision cloud resources with Terraform (or equivalent): the container registry, compute (EKS/ECS/Cloud Run), networking, and IAM roles. Keep state in remote backend and never hardcode secrets — use a secrets manager.

## Step 5 — CI/CD Pipeline

Use GitHub Actions (or GitLab CI). On push: run lint + unit + integration tests, build and push the image, then deploy. Use a **canary or blue-green** strategy so a bad model can be rolled back without downtime.

```yaml
jobs:
  test-build-deploy:
    steps:
      - run: pytest
      - run: docker build -t $REGISTRY/model:$SHA .
      - run: docker push $REGISTRY/model:$SHA
      - run: kubectl set image deploy/model model=$REGISTRY/model:$SHA
```

## Step 6 — Monitoring & Drift

Instrument the service to expose Prometheus metrics (request count, latency histogram, error rate). Add a drift job that compares incoming feature distributions to the training reference (e.g., PSI or KS test with Evidently). Wire alerts: high latency, error spikes, or drift above threshold should notify the team and optionally trigger retraining.

## Step 7 — Document for Your Portfolio

A strong README includes: architecture diagram, how to run locally, how CI/CD deploys, screenshots of dashboards, and a section on trade-offs and what you'd improve. Reproducibility (one-command setup) is what separates a great capstone from an average one.

## Common Pitfalls

- Skipping the model gate, so worse models get promoted.
- No rollback plan — deploys become risky.
- Monitoring only infra metrics and ignoring data/model quality.
- Secrets committed to the repo.
- A project that runs only on your laptop and can't be reproduced.
