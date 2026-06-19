---
course: ml-engineer
title: 'Capstone: End-to-End ML System'
month: 4
monthTitle: 'Production ML: Pipelines, Evaluation, and Capstone'
lesson: 4
summary: A capstone lesson guiding learners to design, build, and present a complete end-to-end ML system
  spanning data ingestion, pipeline, training, evaluation, deployment, and monitoring as a portfolio project.
objectives:
- Scope a realistic ML problem and define success metrics tied to a business or user outcome
- Build a reproducible pipeline from raw data through feature engineering, training, and evaluation
- Deploy a trained model behind an inference API with versioning and basic monitoring
- Evaluate the system rigorously, including offline metrics, error analysis, and slice-based fairness
  checks
- Document and present the project clearly for a portfolio and technical interviews
video: mle-m4-l04-capstone-end-to-end-ml-system.mp4
quiz:
- q: Why should you save the entire fitted pipeline (preprocessing + model) rather than just the model?
  options:
  - It makes the file smaller
  - It ensures serving applies identical transformations as training, avoiding train/serve skew
  - It improves model accuracy automatically
  - It removes the need for input validation
  answer: 1
  why: Saving preprocessing and model together guarantees the exact same feature transformations run at
    inference time, preventing train/serve skew.
- q: Which practice best prevents data leakage in a temporal prediction problem?
  options:
  - Shuffling all rows before splitting
  - Splitting by time so training precedes the validation/test period
  - Using accuracy instead of F1
  - Scaling features after splitting
  answer: 1
  why: For time-dependent data, splitting chronologically prevents the model from seeing future information
    during training, which would leak into evaluation.
- q: What is the purpose of slice-based evaluation?
  options:
  - To reduce model training time
  - To detect underperformance on specific subgroups hidden by aggregate metrics
  - To replace the need for a test set
  - To increase the dataset size
  answer: 1
  why: Aggregate metrics can hide poor performance on subgroups; slice-based evaluation surfaces these
    hidden weaknesses.
- q: Why establish a trivial baseline before modeling?
  options:
  - To meet a deadline
  - To know the minimum performance any real model must beat
  - To avoid using cross-validation
  - Because it is the final deliverable
  answer: 1
  why: A baseline (e.g., majority class or mean predictor) defines the floor of acceptable performance
    and contextualizes your model's value.
- q: Name one signal you would monitor in production to know when a deployed model may need retraining.
  answer: 'Data or prediction drift (also acceptable: rising error rate, stale input data, latency spikes)'
  why: Drift in incoming data or output distributions indicates the model's assumptions may no longer
    hold, signaling a retrain.
- q: In one phrase, what should a /predict API response include besides the prediction for traceability?
  answer: The model version
  why: Returning the model version lets you trace which model produced a given prediction, essential for
    debugging and audits.
resources:
- label: MLflow Documentation
  url: https://mlflow.org/docs/latest/index.html
- label: FastAPI Documentation
  url: https://fastapi.tiangolo.com/
- label: 'Google: Model Cards for Model Reporting'
  url: https://modelcards.withgoogle.com/about
- label: scikit-learn Pipeline Guide
  url: https://scikit-learn.org/stable/modules/compose.html
---

## Capstone Overview

This capstone ties together everything from the bootcamp into one shippable project. The goal is not a Kaggle-style notebook, but a **system**: data flows in, a model is trained and evaluated, and predictions are served behind an API with monitoring. Treat it as the centerpiece of your portfolio.

## 1. Scope and Problem Framing

Start by choosing a problem you can defend.

- **Define the task**: classification, regression, ranking, or forecasting.
- **Pick the metric that matters**: don't default to accuracy. Use F1, AUC, RMSE, or a business KPI (e.g., cost of false positives).
- **Set a baseline**: a trivial model (majority class, mean predictor, simple heuristic) you must beat.
- **State constraints**: latency budget, data freshness, interpretability requirements.

Write a one-page project brief before writing code.

## 2. Data Pipeline

A pipeline must be **reproducible** and **idempotent**.

- **Ingestion**: pull raw data from a source (CSV, API, database). Store an immutable raw copy.
- **Validation**: schema checks, null rates, range checks. Fail loudly on bad data.
- **Transformation**: feature engineering encapsulated in a `Pipeline`/`ColumnTransformer` so the same logic runs in training and serving.
- **Splitting**: respect time order for temporal data; avoid leakage from target-derived features.

Version both data and code (e.g., DVC + Git) so any run is repeatable.

## 3. Training and Experiment Tracking

- Use an experiment tracker (MLflow, Weights & Biases) to log params, metrics, and artifacts.
- Tune hyperparameters with cross-validation; never tune on the test set.
- Save the **fitted pipeline** (preprocessing + model) as a single artifact so serving matches training exactly.

## 4. Evaluation

Go beyond a single number.

- **Offline metrics** on a held-out test set vs. the baseline.
- **Error analysis**: inspect the worst predictions; look for patterns.
- **Slice-based evaluation**: report metrics per subgroup to catch hidden underperformance.
- **Calibration** (for classifiers) and **confidence intervals** where feasible.

## 5. Deployment

- Wrap the saved pipeline in an inference service (FastAPI) with a `/predict` endpoint.
- Validate inputs with a schema (Pydantic). Return predictions plus a model version.
- Containerize with Docker for reproducible deploys.
- Add **monitoring**: log inputs/outputs, track latency, and watch for data/prediction drift.

## 6. Documentation and Presentation

- A clear README: problem, data, approach, results, how to run.
- A model card summarizing intended use, metrics, and limitations.
- A short demo (video or live) and an architecture diagram.

The deliverable is a story: problem → data → model → results → deployment → what you'd do next.
