---
course: data-scientist
title: Prompt Engineering for Data Tasks
month: 5
monthTitle: Generative AI and LLM Foundations for Data Scientists
lesson: 2
summary: Learn to treat a prompt as a data-processing component you can build, measure, and improve. This
  lesson shows how to write structured prompts for classification and extraction over a pandas DataFrame,
  then evaluate them with scikit-learn metrics exactly like you would a trained model. You will also add
  guardrails for label sets and parse failures and reason about the cost and latency of batch prompting.
objectives:
- Decompose a good data prompt into role, task, explicit constraints, a fixed output format, and a fixed
  label set
- Classify a text column in a DataFrame with few-shot prompting and a cheap, fast model
- Extract messy text into structured JSON and parse it safely without eval
- Build a small labeled eval set and measure accuracy, precision, recall, and F1 with scikit-learn
- Iterate on a prompt using the same eval loop you use to iterate on a model
- Add guardrails for fixed label sets, an unknown option, parse failures, and batch cost
video: dsc-m5-l02-prompt-engineering-for-data-tasks.mp4
quiz:
- q: Which set of elements best describes the anatomy of a reliable data-task prompt?
  options:
  - A friendly greeting, a long backstory, and an open-ended question
  - The highest possible temperature and a very large max_tokens
  - A clear role/task, explicit constraints, a fixed output format, and a fixed label set
  - A single example and a request to be creative
  answer: 2
  why: Reliable data prompts pin down the role and task, state constraints, force a fixed output format,
    and restrict outputs to a known label set so results are parseable and comparable across rows.
- q: Why should you evaluate a classification prompt on a small LABELED set before running it over the
    whole DataFrame?
  options:
  - Because it lets you measure accuracy and F1 and iterate on the prompt the same way you iterate on
    a model
  - Because the API refuses unlabeled data
  - Because labeled data makes the model run faster
  - Because evaluation is only possible on the training split
  answer: 0
  why: 'A labeled eval set turns prompt iteration into the familiar measure-then-improve loop: you compute
    accuracy, precision, recall, and F1 on known answers and keep the prompt version that scores best.'
- q: Which scikit-learn function gives you per-class precision, recall, and F1 in a single readable summary?
  options:
  - train_test_split
  - StandardScaler
  - predict_proba
  - classification_report
  answer: 3
  why: classification_report(y_true, y_pred) prints per-class precision, recall, F1, and support, which
    is exactly what you want when comparing prompt versions against true labels.
- q: What is the safest way to turn a model's JSON-looking string output into a Python object?
  options:
  - Call eval() on the string
  - Use json.loads() inside a try/except and handle parse failures
  - Trust the string and index into it directly
  - Concatenate it into another prompt
  answer: 1
  why: Never eval() model output. Parse with json.loads() wrapped in try/except so malformed responses
    are caught and routed to a fallback (such as 'unknown') instead of crashing the pipeline.
- q: For bulk classification of thousands of rows where each call is a simple label, which model choice
    is most appropriate as a default?
  options:
  - A date-suffixed pinned model ID for reproducibility
  - claude-opus-4-8 for every single row regardless of difficulty
  - claude-haiku-4-5 for cheap, fast bulk work, escalating only hard cases to claude-opus-4-8
  - The most expensive model available, to be safe
  answer: 2
  why: 'Match the model to the job: claude-haiku-4-5 is cheap and fast for high-volume simple labels,
    and you reserve claude-opus-4-8 for the genuinely hard or ambiguous cases. Avoid hard-pinning date-suffixed
    IDs.'
- q: Explain why guardrails like a fixed label set and an explicit 'unknown'/'other' option improve a
    classification prompt, and how they connect to the Module 3 confusion matrix.
  answer: A fixed label set constrains the model to outputs you can map to known classes, so every prediction
    lines up with a column or row of the confusion matrix instead of producing free-text you cannot score.
    An explicit 'unknown' or 'other' option gives the model a safe place to put genuinely ambiguous rows
    rather than guessing a wrong concrete label, which keeps false positives and false negatives honest.
    Together they make predicted-vs-true comparison clean, so accuracy, precision, recall, and F1 computed
    from the confusion matrix reflect real performance rather than parsing noise.
  why: Guardrails align the model's output space with the evaluation's label space. That is what makes
    a confusion matrix and the metrics derived from it (accuracy, precision, recall, F1) trustworthy.
resources:
- label: 'Anthropic: Prompt Engineering Overview'
  url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- label: 'Anthropic: Multishot (Few-Shot) Prompting'
  url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- label: 'Anthropic: Increase Output Consistency (Structured / JSON Output)'
  url: https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-consistency
- label: 'scikit-learn: Classification Metrics (accuracy, precision, recall, F1)'
  url: https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics
---

## Why a Prompt Is a Data Component

In earlier modules you trained models that map inputs to outputs. A prompt does the same thing: it maps a row of text to a label or a structured record, except you write the mapping in natural language instead of fitting parameters. So a prompt can be **built, measured, versioned, and improved** with the same discipline you apply to a model. The biggest mistake is to write one prompt, eyeball a few outputs, and ship it. Instead, define the task crisply, run it on a labeled sample, and score it.

## Anatomy of a Good Data Prompt

A reliable data prompt has four parts:

- **Role and task**: tell the model what it is and exactly what to do.
- **Explicit constraints**: what to include, what to ignore, edge cases.
- **A fixed output format**: one label, or strict JSON. No prose.
- **A fixed label set**: the allowed answers, plus an escape hatch.

```python
from anthropic import Anthropic
client = Anthropic()

def classify(text, labels):
    msg = client.messages.create(
        model="claude-haiku-4-5", max_tokens=10,
        system=f"Classify into exactly one of: {labels}. Reply with only the label.",
        messages=[{"role": "user", "content": text}],
    )
    return msg.content[0].text.strip()
```

The `system` prompt fixes the task and format; the user turn carries the row. `max_tokens=10` keeps it cheap because a label is short.

## Few-Shot Classification Over a DataFrame

Real work means a whole column, not one string. Add a few labeled examples to steer the model, then map over the column with a cheap model.

```python
import pandas as pd

LABELS = ["billing", "bug", "feature_request", "other"]
df = pd.DataFrame({"ticket": ["App crashes on login",
                               "Charge me yearly instead"]})

df["pred"] = df["ticket"].apply(lambda t: classify(t, LABELS))
```

For thousands of rows, batch with `claude-haiku-4-5` for speed and cost, and reserve `claude-opus-4-8` for the rows your eval flags as ambiguous. Don't hard-pin a date-suffixed model ID; pick the model that fits the difficulty.

## Extraction to Structured JSON

Classification picks one label; extraction pulls many fields from messy text. Ask for strict JSON and parse it safely.

```python
import json

def extract(text):
    msg = client.messages.create(
        model="claude-haiku-4-5", max_tokens=200,
        system=("Extract fields as JSON with keys "
                "company, amount, due_date. Use null if missing. "
                "Output only JSON."),
        messages=[{"role": "user", "content": text}],
    )
    raw = msg.content[0].text
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"company": None, "amount": None, "due_date": None}
```

Never call `eval()` on model output. For hard guarantees, use tool use or structured outputs so the response is schema-validated, not hand-parsed.

## Evaluate a Prompt Like a Model

This is the heart of the lesson. Build a small **labeled** eval set, run the prompt, and measure it with scikit-learn, connecting back to Module 3 metrics.

```python
from sklearn.metrics import (accuracy_score, f1_score,
                             classification_report)

eval_df = pd.DataFrame({
    "text": ["App crashes", "Refund please", "Add dark mode"],
    "true": ["bug", "billing", "feature_request"],
})
eval_df["pred"] = eval_df["text"].apply(lambda t: classify(t, LABELS))

print(accuracy_score(eval_df["true"], eval_df["pred"]))
print(f1_score(eval_df["true"], eval_df["pred"], average="macro"))
print(classification_report(eval_df["true"], eval_df["pred"]))
```

Accuracy, precision, recall, F1, and the confusion matrix mean exactly what they did for a classifier. Iterating on a prompt is the same loop as iterating on a model: change the wording, re-run, keep the higher-scoring version.

## Guardrails for Reliable Pipelines

Production prompts fail in predictable ways:

- **Constrain to a fixed label set** so outputs map cleanly to your classes and confusion matrix.
- **Give an explicit `unknown`/`other` option** so the model parks ambiguous rows instead of guessing wrong.
- **Handle parse failures** with `try/except` and a fallback label, so one bad response never crashes a batch.

```python
def safe_label(text, labels):
    out = classify(text, labels).lower()
    return out if out in labels else "other"
```

## Cost and Latency of Batch Prompting

Each row is an API call, so cost and latency scale with the data. Use `claude-haiku-4-5` for the bulk, keep `max_tokens` tight for labels, and escalate only flagged rows to `claude-opus-4-8`. Where supported, batch processing trades latency for a lower per-call price on large, non-interactive jobs.
