---
course: ml-engineer
title: Monitoring, Drift, and Retraining in Production
month: 6
monthTitle: Cloud Deployment, Scaling, and Monitoring
lesson: 3
summary: 'Deployed models decay silently as the world shifts, and offline test metrics cannot warn you.
  This capstone mini-project lesson teaches you to implement production monitoring concretely: detect
  data and concept drift with Evidently and a dependency-light statistical check, track performance once
  labels arrive, and define automated retraining triggers.'
objectives:
- Explain why offline metrics are insufficient and how deployed models decay silently
- Distinguish data drift from concept drift with concrete examples and the right detection strategy
- Implement a runnable Evidently drift report comparing a reference window to a current window
- Build a dependency-light drift check using scipy.stats.ks_2samp and reason about PSI
- Monitor model performance once labels arrive and place NannyML, Prometheus, and Grafana correctly
- Define documented retraining triggers and ship a monitoring mini-project for the capstone model
video: mle-m6-l03-monitoring-drift-and-retraining-in-production.mp4
quiz:
- q: Which scenario is an example of concept drift rather than data drift?
  options:
  - The mean of an input feature gradually shifts upward over time
  - A new category appears in a categorical input feature
  - The number of incoming prediction requests doubles overnight
  - Fraud tactics evolve so the same transaction features now imply a different label
  answer: 3
  why: 'Concept drift means the relationship P(y|X) changes: identical inputs now map to a different target.
    Shifting feature means or new categories are data drift in P(X); request volume is an operational
    change.'
- q: What does an Evidently DataDriftPreset report primarily compare?
  options:
  - Training time against inference latency
  - A reference data window against a current data window, feature by feature
  - Model weights before and after retraining
  - Predicted labels against confirmed ground-truth labels
  answer: 1
  why: DataDriftPreset contrasts a trusted reference window with a recent current window per feature,
    surfacing distribution shifts. It does not require ground-truth labels.
- q: Why is scipy.stats.ks_2samp useful as a dependency-light drift check?
  options:
  - It automatically retrains the model when drift is detected
  - It measures classification accuracy without any labels
  - It tests whether reference and current samples come from the same distribution, returning a statistic
    and p-value
  - It guarantees the input feature is normally distributed
  answer: 2
  why: The two-sample Kolmogorov-Smirnov test compares two empirical distributions and returns a statistic
    and p-value; a small p-value flags that the current window has drifted from the reference.
- q: Once ground-truth labels arrive in production, what is the most direct way to confirm the model has
    degraded?
  options:
  - Recompute the same offline evaluation metrics (F1, AUC) on the newly labeled production window and
    compare to the deploy baseline
  - Count the number of API requests per second
  - Re-run the project's unit tests
  - Increase the model's learning rate
  answer: 0
  why: With real labels you can recompute the exact metrics used at evaluation time over a recent window
    and compare against the logged baseline, directly measuring true performance decay.
- q: What problem does a tool like NannyML specifically address?
  options:
  - Containerizing the trained model for deployment
  - Estimating model performance before ground-truth labels are available
  - Serving predictions to clients over HTTP
  - Visualizing CPU and memory usage of the server
  answer: 1
  why: NannyML focuses on estimating production model performance when labels are delayed or absent, complementing
    drift detection until true labels arrive.
- q: Name one concrete condition you would encode as an automated retraining trigger.
  answer: A drift metric crossing a threshold (e.g., share of drifted features above 30% for N consecutive
    windows) or a monitored performance metric dropping below a floor (e.g., F1 falling 5 points under
    the baseline). A scheduled cadence gated by a holdout comparison is also acceptable.
  why: 'Good triggers are explicit and measurable: a drift threshold, a performance floor, or a scheduled
    retrain gated on beating the incumbent, all of which avoid retraining on noise.'
resources:
- label: Evidently AI Documentation
  url: https://docs.evidentlyai.com/
- label: NannyML Documentation
  url: https://nannyml.readthedocs.io/en/stable/
- label: 'Evidently: Data Drift vs Concept Drift'
  url: https://www.evidentlyai.com/ml-in-production/concept-drift
- label: 'Prometheus: Getting Started with Metrics & Grafana'
  url: https://prometheus.io/docs/prometheus/latest/getting_started/
---

## Why Monitoring Matters

A model that scored well offline can silently decay the moment it meets live traffic. The world shifts: user behavior changes, upstream data sources change schema, and last quarter's patterns stop holding. Offline metrics on a frozen test set tell you nothing about *today's* inputs. Production monitoring closes that loop -- it watches the data flowing in and the predictions flowing out, and warns you before a quiet decay becomes a costly outage. Earlier lessons *described* drift; this one makes you **implement** it.

## Data Drift vs Concept Drift

These two are often confused but have different fixes.

- **Data drift (covariate shift)**: the distribution of the inputs P(X) changes while the input-to-output relationship stays the same. Example: a credit model trained mostly on urban applicants starts receiving rural ones, so the feature distributions move.
- **Concept drift**: the relationship P(y|X) itself changes -- the same inputs now imply a different label. Example: fraud tactics evolve, so transaction patterns once benign are now fraudulent.

Data drift you can detect *without labels* by comparing feature distributions. Concept drift usually needs labels (or a proxy) because the inputs can look unchanged while accuracy quietly collapses.

## Implementing a Drift Report with Evidently

Evidently compares a **reference** window (a trusted baseline, often your training or last-good period) against a **current** window (recent production data).

```python
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

ref_df = pd.read_parquet("reference.parquet")  # baseline window
cur_df = pd.read_parquet("current.parquet")    # recent production window

report = Report(metrics=[DataDriftPreset()])
result = report.run(reference_data=ref_df, current_data=cur_df)
result.save_html("drift.html")
```

Open `drift.html` for a per-feature breakdown and an overall drift share. Note: the Evidently API evolves across versions (0.4 vs 0.6+), so always check the current docs for the exact import paths and method names.

## A Dependency-Light Check: KS Test and PSI

You do not always need a framework. For a single numeric feature, the two-sample Kolmogorov-Smirnov test asks "do these two samples come from the same distribution?"

```python
from scipy.stats import ks_2samp

stat, p_value = ks_2samp(ref_df["amount"], cur_df["amount"])
drifted = p_value < 0.05
print(f"KS stat={stat:.3f} p={p_value:.4f} drifted={drifted}")
```

A small p-value flags drift. For a single bounded score, the **Population Stability Index (PSI)** bins both windows and sums (cur%-ref%)*ln(cur%/ref%); a common rule of thumb is PSI < 0.1 stable, 0.1-0.25 moderate, > 0.25 significant. These make cheap, alert-friendly per-feature checks.

## Performance Monitoring Once Labels Arrive

Drift is a *leading* indicator; the ground truth is actual performance. When labels eventually land (a refund is confirmed, a click happens), recompute the **same metrics** from your evaluation lesson over a sliding window:

```python
from sklearn.metrics import f1_score, roc_auc_score

f1 = f1_score(y_true_window, y_pred_window)
auc = roc_auc_score(y_true_window, y_score_window)
```

Compare against the baseline you logged at deploy time. When labels are delayed or absent, **NannyML** estimates model performance *before* labels arrive using methods like confidence-based performance estimation. Separately, track **operational** metrics -- latency, throughput, error rate -- by exposing counters to **Prometheus** and dashboarding them in **Grafana**. Data quality, model quality, and operational health are three distinct layers.

## Defining Retraining Triggers

Decide *in advance* what conditions force a retrain, and write them down:

- **Drift trigger**: share of drifted features exceeds a threshold (e.g., > 30%) for N consecutive windows.
- **Performance trigger**: a monitored metric drops below a floor (e.g., F1 falls 5 points under baseline).
- **Cadence + gate**: retrain on a schedule, but only ship if the new model beats the incumbent on a holdout.

Avoid retraining on every blip -- noise causes thrash. Always validate the retrained model against the current one before promotion.

## Mini-Project: Add Monitoring to Your Capstone

Take the model from your Module 4 capstone and make it observable.

**Brief**: Build `monitor.py` that loads your saved pipeline, reads a reference window and a new production window, and produces (1) an Evidently drift report and (2) a performance check, then prints a clear retrain / no-retrain decision based on a documented rule.

**Deliverables**:
1. `monitor.py` generating `drift.html` via `DataDriftPreset` on reference vs current windows.
2. A dependency-light `ks_2samp` check on at least one key feature as a fallback.
3. A performance section recomputing your capstone metric on a labeled window vs the deploy baseline.
4. A `RETRAINING.md` documenting your exact trigger (drift % and/or metric drop) and the validation gate before promotion.
5. A short README note on how often the monitor runs and who gets alerted.

This is the missing piece that turns a trained model into a maintained system.
