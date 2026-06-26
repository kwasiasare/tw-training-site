---
course: ml-engineer
title: 'Capstone: An End-to-End ML System as Portfolio Evidence'
month: 7
monthTitle: Capstone & Career Launch
lesson: 1
summary: Earlier in the course you learned to build a pipeline, evaluate rigorously, serve a model, and
  monitor it in production. This capstone turns those skills into one flagship portfolio project that
  proves you can ship an ML system, not just train a notebook model. You will scope a defensible problem,
  build the full loop from data to monitoring, and hold the work to an explicit rubric and a clear definition
  of done. The deliverable is a public, reproducible repository with an architecture diagram, a model
  card, a live or recorded demo, and a written design doc that explains your decisions and trade-offs.
  This is the single project a hiring manager will look at first, so we engineer it to be unmistakably
  hireable.
objectives:
- Scope an end-to-end ML problem with a metric tied to a real user or business outcome and a baseline
  you must beat
- 'Build the full system loop: data ingestion, reproducible pipeline, training, evaluation, serving, and
  monitoring'
- Apply an explicit capstone rubric and a written definition of done to judge whether the project is portfolio-ready
- 'Produce the four core artifacts: a clean repo with README, an architecture diagram, a model card, and
  a demo'
- Quantify results against the baseline and report latency, throughput, and cost alongside model metrics
- Write a design doc that defends your decisions and names the alternatives you rejected
video: mle-m7-l01-capstone-an-end-to-end-ml-system.mp4
quiz:
- q: What distinguishes a portfolio-grade capstone from a strong Kaggle-style notebook?
  options:
  - The capstone uses a larger dataset and more model parameters
  - The capstone avoids using any pre-built libraries
  - The capstone is a deployed, reproducible system with data ingestion, serving, and monitoring, not
    just a trained model in a notebook
  - The capstone reports only accuracy instead of multiple metrics
  answer: 2
  why: A notebook proves you can train a model; a capstone proves you can ship a system. Hiring managers
    for ML Engineer roles look for the full loop from data to a served, monitored endpoint, packaged so
    someone else can run it. That systems-level evidence is what separates an engineer from a hobbyist.
- q: Why should your capstone define a baseline before any modeling?
  options:
  - Baselines are required by scikit-learn before training
  - A trivial baseline (majority class, mean, or simple heuristic) sets the floor your model must beat
    and makes your results interpretable
  - Baselines remove the need for a test set
  - Baselines guarantee the model will generalize
  answer: 1
  why: Without a baseline, an F1 of 0.82 means nothing. A trivial predictor or simple heuristic defines
    the minimum any real model must exceed and turns your headline metric into a credible, contextualized
    claim a reviewer can trust.
- q: Which set of numbers makes a capstone result most credible to an ML hiring manager?
  options:
  - The model metric versus the baseline, plus serving latency, throughput, and an estimated cost per
    1,000 predictions
  - Only the final validation accuracy
  - The number of lines of code written
  - The number of epochs trained and the GPU brand used
  answer: 0
  why: ML Engineers are judged on systems, not just model quality. Reporting the metric lift over baseline
    together with p95 latency, throughput, and a cost estimate demonstrates that you think about production
    trade-offs, which is exactly the judgment the role requires.
- q: What belongs in the 'definition of done' for a portfolio capstone?
  options:
  - The model achieves 100% accuracy on the training set
  - The model is the largest architecture you could fit in memory
  - The notebook runs once on your laptop without errors
  - A reproducible repo, a metric that beats the baseline, a served endpoint with input validation and
    versioning, basic monitoring, and the four documentation artifacts
  answer: 3
  why: Done is an explicit bar, not a feeling. It means another person can clone and run the project,
    the model beats the baseline, the endpoint validates inputs and returns a model version, monitoring
    is wired up, and the diagram, README, model card, and demo all exist.
- q: Why save the entire fitted pipeline (preprocessing plus model) as one artifact for the capstone?
  options:
  - It reduces the model file size
  - It guarantees serving applies identical transformations to training, preventing train/serve skew
  - It allows skipping input validation at serving time
  - It automatically improves the model's accuracy
  answer: 1
  why: If preprocessing is re-implemented separately at serving time, subtle differences create train/serve
    skew and silent errors. Persisting the fitted preprocessing and model together ensures the exact same
    feature transformations run in production as in training.
- q: In two to four sentences, describe how you would present your capstone's results so they read as
    credible engineering rather than a lucky score.
  answer: I would open with the problem and the metric that matters, then state my result next to the
    baseline so the lift is visible, for example F1 0.84 against a 0.61 majority-class baseline. I would
    add the production numbers, p95 latency around 90 milliseconds, roughly 200 requests per second per
    replica, and an estimated cost per thousand predictions, so the reviewer sees I thought about serving,
    not just accuracy. Then I would show a slice-based breakdown and a short error analysis to prove I
    understand where the model fails. Finally I would point to the reproducible repo and demo so every
    claim can be verified.
  why: A credible presentation pairs the headline metric with a baseline, adds production trade-offs (latency,
    throughput, cost), surfaces weaknesses through slices and error analysis, and links to reproducible
    evidence, which together signal engineering judgment rather than a single lucky number.
resources:
- label: 'Google: Model Cards for Model Reporting'
  url: https://modelcards.withgoogle.com/about
- label: MLflow Documentation
  url: https://mlflow.org/docs/latest/index.html
- label: 'scikit-learn: Pipelines and composite estimators'
  url: https://scikit-learn.org/stable/modules/compose.html
- label: 'Evidently: Open-source ML monitoring'
  url: https://docs.evidentlyai.com/
---

## The One Project That Gets You Hired

By now you have built pipelines, evaluated models rigorously, deployed an inference API, and wired up monitoring. This capstone is where those pieces become a single, presentable system that a hiring manager will open first. The earlier Module 4 capstone taught you the *mechanics* of building the loop; this lesson is about producing **portfolio evidence**: a flagship project so clearly engineered that it argues, on its own, that you can do the job. The difference between a learner and a hire is rarely raw modeling skill. It is the ability to ship a system end to end and explain why you built it that way.

## Scope a Problem You Can Defend

Start with a one-page brief, written before any code.

- **Pick a task with a real outcome.** Classification, regression, ranking, forecasting, or a retrieval/LLM task from Module 5. Choose data you can legally use and a problem you can explain to a non-expert in two sentences.
- **Choose the metric that matters.** Do not default to accuracy. Use F1, AUC, RMSE, recall at a fixed precision, or a business KPI such as the cost of a false positive. Tie it to the decision the model informs.
- **Set a baseline.** A majority-class predictor, a mean, or a simple heuristic. This is the floor your model must beat, and it makes every later number interpretable.
- **State constraints.** Latency budget, data freshness, interpretability, and a rough cost ceiling. Constraints are what make the project read like real engineering.

A capstone that picks a sharp, modest problem and nails the full loop beats an ambitious project that only half-works.

## Build the Full Loop

The capstone must demonstrate the complete system, not a single stage.

1. **Data ingestion.** Pull from a source (CSV, API, or database) and store an immutable raw copy. Validate schema, null rates, and ranges, and fail loudly on bad data.
2. **Reproducible pipeline.** Encapsulate all feature engineering in a `Pipeline` or `ColumnTransformer` so the same logic runs in training and serving. Respect time order in splits to avoid leakage.
3. **Training with tracking.** Log parameters, metrics, and artifacts with MLflow or Weights & Biases. Tune with cross-validation; never touch the test set until the end. Save the **fitted pipeline** as one artifact.
4. **Rigorous evaluation.** Compare against the baseline on held-out data, run error analysis on the worst predictions, and report **slice-based** metrics to catch hidden underperformance.
5. **Serving.** Wrap the saved pipeline behind a FastAPI `/predict` endpoint (or a serving runtime such as KServe, Triton, or Ray Serve for a Module 6 flavor). Validate inputs with a Pydantic schema and return the prediction plus a **model version**. Containerize with Docker.
6. **Monitoring.** Log inputs, outputs, and latency, and watch for data and prediction drift with a tool like Evidently or NannyML. Decide in advance what triggers a retrain.

If you completed Module 5 or 6, lean into them: an LLM/RAG capstone with a vector database and an evaluation harness, or a model served on Kubernetes with autoscaling, both make strong, current portfolio pieces for 2026.

## The Capstone Rubric

Hold the work to an explicit rubric. Score each row honestly out of the weight shown.

- **Problem framing (15).** Clear task, metric tied to an outcome, baseline, and constraints.
- **Data and pipeline (20).** Immutable raw data, validation, leakage-safe splits, reproducible transforms.
- **Modeling and evaluation (20).** Beats the baseline; error analysis and slice metrics present.
- **Serving (20).** Versioned, input-validated endpoint; containerized; latency and throughput measured.
- **Monitoring (10).** Drift and latency tracked; a stated retraining trigger.
- **Documentation (15).** README, architecture diagram, model card, and a design doc with trade-offs.

A project below roughly 80 out of 100 is not yet portfolio-ready. The rubric is not bureaucracy; it is the same checklist a reviewer applies, so applying it first removes their easy reasons to pass.

## The Definition of Done

"Done" is a hard bar, not a feeling. Your capstone is done when:

- Another person can **clone the repo and reproduce** your results from the README, with pinned dependencies and a seed.
- The model **beats the baseline** by a margin you report next to it.
- The **endpoint validates inputs**, returns a model version, and is containerized.
- **Monitoring** is wired up and you can name the retraining trigger.
- The **four artifacts exist**: README, architecture diagram, model card, and a demo.

Until all five are true, the project is in progress, not in your portfolio.

## Quantify Like an Engineer

ML Engineers are judged on systems, so report system numbers next to model numbers. Pair your headline metric with the baseline ("F1 0.84 versus a 0.61 majority-class baseline"), then add **p95 latency**, **throughput** (requests per second per replica), and an **estimated cost per 1,000 predictions**. Even in a personal project these are measurable, and they signal that you think about production, not just leaderboard score. A slice table and a short error analysis prove you understand where the model fails, the single clearest sign of maturity.

## Common Capstone Pitfalls

Most capstones fail in predictable ways, and avoiding them is half the battle. Watch for these:

- **Leakage that inflates the score.** Computing scalers, target encodings, or feature selection on the full dataset before splitting leaks the test set into training. Fit every transform inside the pipeline on the training fold only.
- **A model with no baseline.** A 0.91 AUC sounds great until you learn the majority-class baseline is 0.90. Always report the lift.
- **Train/serve skew.** Re-implementing preprocessing in the API instead of serving the saved fitted pipeline. Serve the exact artifact you trained.
- **An endpoint that never proves it works.** No load test, no latency numbers, no example request in the README. Include a runnable `curl` example and a small load test.
- **Scope creep.** Trying to build five models and shipping none. A narrow problem solved completely beats a broad one half-built.
- **A repo a stranger cannot run.** Unpinned dependencies, missing data instructions, no seed. If a reviewer cannot reproduce your headline number in ten minutes, the project is not done.

Run this checklist before you call the capstone finished; each item is something a reviewer will probe. A useful test is to hand the repo to a peer with no context and ask them to reproduce your headline number using only the README. If they get stuck, you have found exactly the gap an interviewer would find, and fixing it now costs minutes instead of an offer.

## Package It as Four Artifacts

Every reviewer wants the same four things:

- **A clean public repo** with a README that states the problem, architecture, how to deploy, how to test, and the results.
- **An architecture diagram** showing the loop from data to monitoring in one glance.
- **A model card** summarizing intended use, training data, metrics, slices, and limitations.
- **A demo**, three to five minutes, showing the endpoint serving a real request and the monitoring updating.

Add a short **design doc** that defends your choices by naming the alternative you rejected: "I served with FastAPI rather than a managed endpoint because the project is cost-sensitive and low-traffic, and I can show the Dockerfile and load test." That single habit, explaining the road not taken, is what makes the work read as senior. This polished package is the launch pad for the resume, portfolio, and job-search lessons that follow.
