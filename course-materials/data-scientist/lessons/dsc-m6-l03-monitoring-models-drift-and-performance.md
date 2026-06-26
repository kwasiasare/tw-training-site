---
course: data-scientist
title: 'Monitoring Models in Production: Drift and Performance'
month: 6
monthTitle: Productionization and MLOps
lesson: 3
summary: A model that scored well offline can silently decay once it meets the real world. This lesson
  teaches you to detect data drift and concept drift statistically, build a concrete drift report with
  Evidently, track live performance with the same scikit-learn metrics from Module 3, and wire up alerts
  and retraining triggers so problems surface before they hurt the business.
objectives:
- Explain why production models decay and why offline metrics are not enough
- Define and distinguish data drift from concept drift with concrete examples
- Detect drift statistically using the KS test and the Population Stability Index
- Build a reference-vs-current drift report with Evidently and read its output
- Monitor live performance by recomputing Module 3 metrics as labels arrive
- Design alerting thresholds and retraining triggers that respond to drift
video: dsc-m6-l03-monitoring-models-drift-and-performance.mp4
quiz:
- q: A spam classifier's input email distribution looks unchanged, but spammers have invented new tactics
    so the SAME features now imply 'spam' less often. What is this called?
  options:
  - Data drift
  - Sampling bias
  - Label leakage
  - Concept drift
  answer: 3
  why: Concept drift is a change in the relationship between features and the target P(y|X). The inputs
    look stable but the meaning of those inputs has shifted, so the learned mapping is now wrong.
- q: Which statistical test is a natural choice for detecting drift in a single CONTINUOUS feature by
    comparing a reference window to a current window?
  options:
  - Two-sample Kolmogorov-Smirnov (KS) test
  - Pearson correlation
  - Linear regression t-test
  - One-way ANOVA on the target
  answer: 0
  why: scipy.stats.ks_2samp compares two empirical distributions of a continuous variable and returns
    a statistic and p-value, making it a dependency-light way to flag distribution shift in one feature.
- q: Why is monitoring input drift valuable even BEFORE ground-truth labels arrive?
  options:
  - Drift metrics replace the need for labels permanently
  - Input distributions never change in production
  - Labels are often delayed, so drift is an early proxy warning that performance MAY be degrading
  - Drift only matters for regression models
  answer: 2
  why: Ground truth often lags by days or weeks. Input and prediction drift can be measured immediately,
    giving an early signal to investigate before delayed labels confirm a performance drop.
- q: 'A Population Stability Index (PSI) of 0.30 between the reference and current distribution of a feature
    most likely indicates:'
  options:
  - A significant, actionable population shift worth investigating
  - No meaningful change; ignore it
  - A data type error in the column
  - Perfect stability between the two windows
  answer: 0
  why: By common rule of thumb, PSI below 0.1 is stable, 0.1-0.2 is moderate, and above 0.2-0.25 signals
    a major shift. A PSI of 0.30 is a strong signal to investigate.
- q: Which tool can ESTIMATE a model's performance in production WITHOUT immediately available ground-truth
    labels?
  options:
  - matplotlib
  - NannyML
  - StandardScaler
  - train_test_split
  answer: 1
  why: NannyML provides performance-estimation algorithms (such as CBPE for classification) that estimate
    metrics like ROC-AUC from model confidence and drift before labels arrive, complementing label-based
    monitoring.
- q: Describe a sensible alerting and retraining policy for a model whose input drift report fires but
    whose labels have not yet arrived. What checks would you run and what would trigger an actual retrain?
  answer: open
  why: 'A strong answer: first confirm the drift is real and not a pipeline bug (schema change, nulls,
    unit change); quantify it (which features, how large the PSI/KS shift); estimate performance impact
    with a label-free method like NannyML; alert the owning team rather than auto-retraining on a single
    noisy signal; and trigger a retrain only when a sustained threshold is crossed or, once labels arrive,
    when a live metric (e.g., ROC-AUC or recall) drops below an agreed SLO, retraining on fresh representative
    data and validating before promotion.'
resources:
- label: Evidently AI Documentation
  url: https://docs.evidentlyai.com/
- label: NannyML Documentation
  url: https://nannyml.readthedocs.io/en/stable/
- label: 'Evidently: Data Drift vs Concept Drift (ML Monitoring guide)'
  url: https://www.evidentlyai.com/ml-in-production/data-drift
- label: 'scikit-learn Model Evaluation: Metrics'
  url: https://scikit-learn.org/stable/modules/model_evaluation.html
---

## Why Models Decay in Production

A model is a snapshot of the world at training time, but the world keeps moving. Customer behavior shifts, competitors launch products, fraudsters change tactics, an upstream team renames a column. None of these events touch your code, yet each can quietly erode accuracy. This is **model decay**, and it is the default outcome, not the exception.

The trap is trusting your **offline metrics**. A 0.92 ROC-AUC on a held-out test set tells you how the model did on data that looks like the past; it says nothing about next month. Production monitoring closes that gap by continuously asking two questions: *has the incoming data changed?* and *is the model still right?*

## Data Drift vs. Concept Drift

These two terms are constantly confused, so define them precisely.

- **Data drift** (covariate shift): the distribution of the **inputs** `P(X)` changes. Example: your loan model was trained mostly on applicants aged 30-45, but a new marketing campaign brings in mostly 18-25 year-olds. The features look different from what the model saw in training.
- **Concept drift**: the **relationship** between inputs and target `P(y | X)` changes. The inputs may look identical, but their meaning has shifted. Example: a spam filter's emails look statistically the same, but spammers invent new tricks, so the same words now imply spam far less reliably. The learned mapping is simply wrong now.

Why it matters: data drift is detectable **without labels** because you only need the inputs. Concept drift usually requires **ground truth** to confirm, because you must observe that the same `X` now yields a different `y`. In practice you monitor input drift as an early warning and performance metrics as confirmation.

## Detecting Drift Statistically

Drift detection compares a **reference window** (often the training or a known-good period) against a **current window** (recent production data), feature by feature.

For a single continuous feature, the two-sample **Kolmogorov-Smirnov (KS) test** compares the two empirical distributions and needs nothing beyond SciPy:

```python
from scipy.stats import ks_2samp

stat, p_value = ks_2samp(ref_df["income"], cur_df["income"])
if p_value < 0.05:
    print(f"Drift suspected in 'income' (KS={stat:.3f}, p={p_value:.4f})")
```

The **Population Stability Index (PSI)** is the classic credit-risk metric. It bins a feature and sums `(cur% - ref%) * ln(cur% / ref%)` across bins. Rule of thumb: **< 0.1 stable, 0.1-0.2 moderate, > 0.2 significant shift**. Both KS and PSI are dependency-light and easy to run on a schedule.

## A Concrete Drift Report with Evidently

Hand-rolling a test per column does not scale to hundreds of features. **Evidently** automates this: you pass a reference and a current dataframe, and a preset picks an appropriate test per column and renders an HTML report.

```python
from evidently import Report
from evidently.presets import DataDriftPreset

report = Report(metrics=[DataDriftPreset()])
result = report.run(reference_data=ref_df, current_data=cur_df)
result.save_html("drift.html")
```

The report shows, per feature, the test used, the drift score, and whether drift was detected, plus an overall dataset drift share. Note that **Evidently's API has evolved across versions** (the modern 0.4+/0.6+ pattern uses `Report` with presets); always check the current docs at https://docs.evidentlyai.com/ for the exact imports your installed version expects.

An important complement is **NannyML**, which can **estimate performance without labels** using algorithms like CBPE, giving an estimated ROC-AUC before ground truth lands. Use Evidently for drift and NannyML for label-free performance estimation to cover the gap while labels are delayed.

## Monitoring Live Performance Once Labels Arrive

Drift is a leading indicator; the lagging, ground-truth indicator is **actual performance**. When labels finally arrive (a user churns, a loan defaults, a ticket is resolved), recompute the **exact same scikit-learn metrics from Module 3** over rolling windows so the numbers are comparable to your offline baseline.

```python
from sklearn.metrics import roc_auc_score, recall_score, classification_report

# y_true: labels that just arrived; probs/labels: stored predictions
window_auc = roc_auc_score(y_true, probs)
window_recall = recall_score(y_true, labels)
print(classification_report(y_true, labels))

if window_auc < 0.80:            # agreed SLO threshold
    raise_alert("ROC-AUC below SLO", window_auc)
```

Log these per window into a time series and plot the trend. A slow downward slope in recall or ROC-AUC is decay in action, and it lets you connect a performance drop back to the drift you already flagged.

## Alerting and Retraining Triggers

Detection is useless without a response policy. Build a tiered playbook:

1. **Validate first.** Rule out a pipeline bug: a schema change, a flood of nulls, or a unit change (dollars to cents) often masquerades as drift.
2. **Alert, don't auto-fire.** A single noisy window should notify the owning team, not trigger a retrain. Require a **sustained** breach (drift share above threshold for N consecutive windows).
3. **Retrain on real evidence.** Trigger retraining when a live metric falls below its **SLO** (e.g., recall < 0.80) or when sustained, confirmed drift coincides with a falling label-free performance estimate.
4. **Retrain safely.** Train on fresh, representative data, validate against the current production model, promote only if it wins, and keep the old model for rollback.

Never wire `eval()` or arbitrary code execution into an alerting pipeline; keep triggers as explicit, reviewable thresholds. Monitoring is a control loop: detect, confirm, decide, act, and verify the fix held.

A complete stack has three layers: **input drift** (Evidently/PSI/KS, available immediately), **estimated performance** (NannyML, available before labels), and **measured performance** (Module 3 sklearn metrics, available once labels land). Wire each into dashboards and alerts, and your models stop decaying in silence.
