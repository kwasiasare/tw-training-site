---
course: mlops-engineer
title: Monitoring Model Performance and Detecting Drift
month: 4
monthTitle: Cloud Deployment, Monitoring & Capstone
lesson: 2
summary: This lesson teaches MLOps engineers how to instrument a deployed model with Prometheus and Grafana
  to track operational health (latency, errors, throughput) and model-specific signals like data and concept
  drift. You'll learn what metrics to expose, how to scrape and visualize them, how to detect drift statistically,
  and how to wire alerts that trigger retraining or rollback.
objectives:
- Distinguish operational metrics (latency, errors, throughput) from model-quality and drift metrics
- Instrument a model service to expose Prometheus metrics using a client library
- Configure Prometheus scraping and build Grafana dashboards for real-time monitoring
- Detect data drift and concept drift using statistical tests like PSI and KS
- Define alerting rules and an action plan (retrain, rollback, page) when thresholds are breached
video: mlo-m4-l02-monitoring-model-performance-and-detecting-drift.mp4
quiz:
- q: Which Prometheus metric type would you use to expose a continuously updated PSI drift score that
    can rise and fall?
  options:
  - Counter
  - Gauge
  - Histogram
  - Summary
  answer: 1
  why: A Gauge represents a value that can go up and down, which fits a drift score. Counters only increase;
    histograms bucket distributions of observations.
- q: What does a PSI value of 0.30 typically indicate?
  options:
  - The distribution is stable
  - Moderate drift, monitor only
  - Significant drift worth acting on
  - Insufficient data to compute
  answer: 2
  why: By common rule of thumb, PSI above 0.25 signals significant population shift that warrants investigation
    or retraining.
- q: Why is concept drift harder to detect in real time than data drift?
  options:
  - It requires ground-truth labels, which are often delayed
  - Prometheus cannot store the metric
  - It only affects categorical features
  - It is the same as latency drift
  answer: 0
  why: Concept drift is a change in the input-to-output relationship, which can only be measured once
    true labels arrive — and labels often lag predictions by hours or days.
- q: Which PromQL function computes p95 latency from a histogram metric?
  options:
  - rate()
  - avg_over_time()
  - histogram_quantile()
  - increase()
  answer: 2
  why: histogram_quantile() computes a quantile (e.g. 0.95) from histogram bucket data, typically combined
    with rate() over the _bucket series.
- q: 'Short answer: Name the metric label you should always attach to prediction metrics so you can compare
    deployments.'
  answer: model_version
  why: Labeling metrics with the model version lets you compare latency, errors, and drift across different
    deployed model versions.
- q: 'Short answer: What is the term for monitoring the shift in a model''s output score distribution
    before labels are available?'
  answer: prediction drift
  why: Prediction drift tracks changes in the output distribution and serves as an early warning that
    doesn't require ground-truth labels.
resources:
- label: Prometheus Documentation
  url: https://prometheus.io/docs/introduction/overview/
- label: Grafana Dashboards & Alerting Docs
  url: https://grafana.com/docs/grafana/latest/
- label: 'Evidently AI: Open-source ML monitoring & drift detection'
  url: https://docs.evidentlyai.com/
- label: prometheus_client Python library
  url: https://github.com/prometheus/client_python
---

## Why Monitor a Deployed Model?

A model that scored 0.92 AUC in training can silently degrade in production. The world changes (data drift), relationships shift (concept drift), and infrastructure fails (latency spikes, errors). Monitoring closes the loop between deployment and the next training cycle.

Think of monitoring in two layers:

- **Operational / service health**: latency, error rate, request throughput, resource usage. These tell you if the *service* is healthy.
- **Model / data health**: prediction distribution, input feature distributions, and (when labels arrive) accuracy. These tell you if the *model* is still correct.

## The Prometheus + Grafana Stack

- **Prometheus** is a pull-based time-series database. Your service exposes a `/metrics` HTTP endpoint; Prometheus *scrapes* it on an interval (e.g. every 15s).
- **Grafana** queries Prometheus (using PromQL) and renders dashboards and alerts.
- **Alertmanager** routes Prometheus alerts to Slack, PagerDuty, email, etc.

Metric types you'll use:

- **Counter**: monotonically increasing (e.g. `predictions_total`, `errors_total`).
- **Gauge**: value that goes up and down (e.g. `drift_psi_score`, `inflight_requests`).
- **Histogram**: distribution buckets (e.g. `request_latency_seconds`), enables percentiles via `histogram_quantile`.

## Instrumenting the Service

Use the `prometheus_client` library in Python to expose metrics:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

PRED_COUNT = Counter('predictions_total', 'Total predictions', ['model_version'])
ERROR_COUNT = Counter('prediction_errors_total', 'Failed predictions')
LATENCY = Histogram('prediction_latency_seconds', 'Inference latency',
                    buckets=[.01, .05, .1, .25, .5, 1, 2.5])
DRIFT_PSI = Gauge('feature_drift_psi', 'PSI score', ['feature'])

def predict(features):
    PRED_COUNT.labels(model_version='v3').inc()
    with LATENCY.time():
        try:
            return model.predict(features)
        except Exception:
            ERROR_COUNT.inc()
            raise

start_http_server(8000)  # exposes /metrics on :8000
```

## Prometheus Scrape Config

```yaml
scrape_configs:
  - job_name: 'model-service'
    scrape_interval: 15s
    static_configs:
      - targets: ['model-service:8000']
```

## Useful PromQL Queries

```promql
# p95 latency over 5m
histogram_quantile(0.95, sum(rate(prediction_latency_seconds_bucket[5m])) by (le))

# error rate
sum(rate(prediction_errors_total[5m])) / sum(rate(predictions_total[5m]))

# request throughput
sum(rate(predictions_total[1m]))
```

## Detecting Drift

Drift detection compares a **reference** distribution (training or a known-good window) against the **current** production window.

- **Data / covariate drift**: input feature distributions change. Common tests:
  - **PSI (Population Stability Index)**: bin both distributions, sum `(curr% - ref%) * ln(curr%/ref%)`. Rule of thumb: `<0.1` stable, `0.1–0.25` moderate, `>0.25` significant drift.
  - **KS test** for continuous features, **Chi-square** for categorical.
- **Prediction drift**: the output score distribution shifts even before labels arrive — an early warning.
- **Concept drift**: the input→output relationship changes. Requires ground-truth labels, so you can only measure it once labels land (sometimes days later). Track rolling accuracy/AUC as labels arrive.

Compute drift in a batch job or sidecar, then publish the score as a Gauge so Prometheus can scrape and alert on it.

```python
import numpy as np
def psi(ref, cur, bins=10):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    r = np.histogram(ref, edges)[0] / len(ref) + 1e-6
    c = np.histogram(cur, edges)[0] / len(cur) + 1e-6
    return np.sum((c - r) * np.log(c / r))
```

## Alerting and Acting on Signals

Define alert rules in Prometheus:

```yaml
groups:
  - name: model-alerts
    rules:
      - alert: HighLatencyP95
        expr: histogram_quantile(0.95, sum(rate(prediction_latency_seconds_bucket[5m])) by (le)) > 0.5
        for: 5m
        labels: { severity: warning }
      - alert: FeatureDriftHigh
        expr: feature_drift_psi > 0.25
        for: 10m
        labels: { severity: critical }
```

Map each alert to an action: high latency → scale up / investigate infra; high error rate → rollback to previous model version; high drift → trigger a retraining pipeline and notify the team. Avoid alert fatigue by using `for:` durations and sensible thresholds.

## Best Practices

- Always log the **model version** as a label so you can compare deployments.
- Keep a **reference dataset** versioned alongside the model for drift baselines.
- Monitor **prediction drift** for early warning since labels are often delayed.
- Dashboards should show service health and model health side by side.
- Test your alerts — a silent alerting pipeline is worse than none.
