---
course: ai-app-developer-2026
title: Monitoring, Cost Control, and Evaluation
month: 4
monthTitle: Deployment and Capstone Project
lesson: 3
summary: Learn to keep a deployed LLM app reliable and affordable by adding structured logging, token-cost
  tracking, and automated evaluation tests. This lesson covers what to instrument, how to estimate and
  cap spend, and how to build a lightweight eval harness so quality doesn't silently regress.
objectives:
- Instrument an LLM app with structured logging that captures prompts, responses, latency, and token usage
- Calculate and track token costs per request, per user, and per feature to forecast and control spend
- Apply cost-control techniques like caching, model routing, max-token limits, and budget alerts
- Build an automated evaluation suite using golden datasets and LLM-as-judge to catch quality regressions
- Define key monitoring metrics and set up alerts that flag reliability and cost problems in production
video: aad-m4-l03-monitoring-cost-control-and-evaluation.mp4
quiz:
- q: Why is structured (JSON) logging preferred over plain-text logging for LLM apps?
  options:
  - It uses less disk space
  - It can be queried and aggregated to compute metrics
  - It automatically redacts PII
  - It is required by all LLM providers
  answer: 1
  why: Structured logs let you filter, group, and aggregate fields like tokens, latency, and cost — essential
    for building dashboards and metrics. Plain text is hard to query reliably.
- q: Which technique most directly prevents a single request from generating an unexpectedly huge (and
    expensive) response?
  options:
  - Caching prompts
  - Setting max_tokens on the completion
  - Adding a request_id
  - Using LLM-as-judge
  answer: 1
  why: max_tokens caps the length of the generated output, directly bounding the most variable and often
    costliest part of a call.
- q: What is the main purpose of a golden dataset in an evaluation harness?
  options:
  - To store production logs for billing
  - To provide curated inputs with expected outputs/criteria for repeatable scoring
  - To cache responses for cost savings
  - To redact sensitive data before logging
  answer: 1
  why: A golden dataset is a curated, representative set of inputs with acceptance criteria, used to score
    the app consistently and catch regressions over time.
- q: Which is a valid concern when using LLM-as-judge for evaluation?
  options:
  - It cannot score text outputs
  - It always costs more than human review
  - It may be biased and should be validated against human labels
  - It only works with deterministic outputs
  answer: 2
  why: LLM judges can carry biases (e.g., favoring verbose answers), so you should validate their scores
    against human-labeled examples before relying on them.
- q: Name two dimensions you should aggregate token cost by to find expensive features and forecast spend.
  answer: Per feature and per user (also per request and per day)
  why: Aggregating cost by feature reveals which parts of the app are expensive, while per-user (and per-day)
    aggregation supports forecasting, billing insight, and abuse detection.
- q: Give one example of a deterministic scorer you could use in an eval suite.
  answer: Exact match, regex match, JSON-schema validity, or contains-keyword check
  why: Deterministic scorers give fast, reproducible pass/fail signals without needing another model,
    ideal for structured or constrained outputs.
resources:
- label: Langfuse — open-source LLM observability and evals
  url: https://langfuse.com/docs
- label: OpenAI Evals framework
  url: https://github.com/openai/evals
- label: Helicone — LLM logging and cost monitoring
  url: https://docs.helicone.ai/
- label: OpenAI pricing and token usage docs
  url: https://platform.openai.com/docs/guides/production-best-practices
---

## Why Monitoring, Cost, and Evaluation Matter

Shipping an LLM app is the start, not the finish. Unlike traditional software, LLM apps fail *silently*: outputs can degrade in quality, costs can spike with usage, and a model or prompt change can break behavior without throwing an error. Three disciplines keep a deployed app healthy:

- **Monitoring** — know what's happening right now (latency, errors, traffic, token use).
- **Cost control** — keep spend predictable and bounded.
- **Evaluation** — verify output quality stays acceptable over time.

## Logging: What to Capture

Use **structured logging** (JSON), not plain text, so you can query and aggregate later. For every LLM call, log:

- A `request_id` (trace ID) to correlate multi-step flows
- `timestamp`, `user_id` (or hashed), and `feature` name
- `model`, `prompt_tokens`, `completion_tokens`, `total_tokens`
- `latency_ms` and `status` (success/error/timeout)
- The prompt and response (redact PII; consider truncation or sampling)

```python
import json, time, logging
logger = logging.getLogger("llm")

def log_call(request_id, model, usage, latency_ms, status):
    logger.info(json.dumps({
        "request_id": request_id,
        "model": model,
        "prompt_tokens": usage["prompt_tokens"],
        "completion_tokens": usage["completion_tokens"],
        "latency_ms": latency_ms,
        "status": status,
    }))
```

**Privacy note:** prompts and responses may contain sensitive data. Redact or hash PII, set retention limits, and follow your data policy.

## Token-Cost Tracking

Providers bill per token, usually at different rates for input vs. output. Compute cost per call from the usage object:

```python
PRICES = {  # USD per 1K tokens (example rates)
    "gpt-4o-mini": {"in": 0.00015, "out": 0.0006},
}

def cost(model, usage):
    p = PRICES[model]
    return (usage["prompt_tokens"]/1000)*p["in"] + \
           (usage["completion_tokens"]/1000)*p["out"]
```

Aggregate cost **per request, per user, per feature, and per day**. This tells you which features are expensive and lets you forecast monthly spend. Tag every call so you can slice the data later.

## Cost-Control Techniques

- **Cap output** with `max_tokens` — runaway completions are a common cost leak.
- **Cache** repeated or similar prompts (exact-match or semantic cache) to skip calls entirely.
- **Model routing** — send easy requests to a cheap/small model, escalate only hard ones.
- **Trim context** — don't stuff the whole history; retrieve and include only what's needed.
- **Set budgets and alerts** — daily/monthly spend thresholds that page you before the bill does.
- **Rate-limit per user** to prevent abuse and cost spikes.

## Evaluation: Catching Quality Regressions

Manual spot-checks don't scale. Build a repeatable **eval harness**:

1. **Golden dataset** — a curated set of representative inputs with expected outputs or acceptance criteria.
2. **Scorers** — choose metrics that fit the task:
   - Deterministic: exact match, regex, JSON-schema validity, contains-keyword.
   - **LLM-as-judge**: a model scores correctness, relevance, or tone against a rubric (cheaper to scale, but validate the judge).
   - Human review for a sampled subset.
3. **Run on every change** — new prompt, new model, new retrieval config. Treat it like a test suite in CI.

```python
def evaluate(cases, run_app):
    passed = 0
    for c in cases:
        out = run_app(c["input"])
        if c["check"](out):
            passed += 1
    return passed / len(cases)
```

Track the **pass rate over time** and gate deployments on a minimum threshold.

## Putting It Together in Production

- Emit structured logs → ship to a dashboard (Grafana, Datadog, or a hosted LLM observability tool like Langfuse/Helicone).
- Define **SLOs**: e.g., p95 latency < 3s, error rate < 1%, daily cost < $X.
- Alert on threshold breaches and on **eval pass-rate drops**.
- Review dashboards regularly; close the loop by feeding production failures back into your golden dataset.
