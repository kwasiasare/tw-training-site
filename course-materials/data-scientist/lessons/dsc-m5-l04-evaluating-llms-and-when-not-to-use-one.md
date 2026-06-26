---
course: data-scientist
title: Evaluating LLMs and When NOT to Use One
month: 5
monthTitle: Generative AI and LLM Foundations for Data Scientists
lesson: 4
summary: 'Ship LLM features the way you ship any model: with a labeled eval set and real metrics, not
  vibes. This capstone lesson teaches you to build an evaluation harness with scikit-learn, recognize
  and mitigate hallucination, and apply a clear decision framework for when classical ML beats an LLM.
  You finish by building both an LLM classifier and a classical baseline, evaluating them on the same
  holdout, and recommending which to ship.'
objectives:
- Build an evaluation harness for an LLM feature using a labeled holdout set
- Score LLM outputs with scikit-learn metrics (accuracy, precision, recall, F1) reused from Module 3
- Explain why hallucination happens and apply grounding, citations, and abstention to reduce it
- Apply a decision framework that chooses classical ML over an LLM for structured tabular prediction
- Compare cost, latency, determinism, and privacy tradeoffs between LLM and classical approaches
- Deliver a mini-project comparing an LLM classifier and a TF-IDF baseline with a written recommendation
video: dsc-m5-l04-evaluating-llms-and-when-not-to-use-one.mp4
quiz:
- q: Why must you build a labeled eval set before shipping an LLM-powered classification feature?
  options:
  - LLMs cannot be evaluated with scikit-learn
  - Eval sets make the LLM run faster at inference time
  - Without ground-truth labels you cannot measure accuracy, precision, recall, or F1 — only guess
  - The Anthropic API requires an eval set to return a response
  answer: 2
  why: Evaluation is non-negotiable. A labeled holdout gives you ground truth to compare predictions against,
    so you can compute real metrics instead of trusting that the output 'looks right'. You would never
    ship a classical model without test metrics; an LLM feature is no different.
- q: A model confidently states a plausible-sounding but factually false citation. What is this called,
    and which technique most directly reduces it?
  options:
  - Hallucination; ground the model in retrieved source text (RAG) and ask it to cite or say 'I don't
    know'
  - Overfitting; add more training epochs
  - Data leakage; split the data before scaling
  - Class imbalance; use class_weight='balanced'
  answer: 0
  why: Hallucination is fluent, confident output unsupported by fact. Grounding the model on retrieved
    documents (RAG), instructing it to cite sources, and explicitly permitting abstention ('say you don't
    know') are the most direct mitigations because they constrain generation to available evidence.
- q: You need to predict a numeric customer lifetime value from 40 tabular features, with 200,000 labeled
    rows. Which tool is the better default and why?
  options:
  - An LLM, because it is the most advanced technology available
  - Neither — this problem cannot be modeled
  - An LLM, because tabular data is unstructured text
  - Classical ML (e.g. gradient boosting / regression), because it is cheaper, faster, deterministic,
    and interpretable on structured data with ample labels
  answer: 3
  why: Structured tabular prediction with plenty of labels is the textbook case for classical ML. It is
    cheaper per prediction, lower latency, deterministic, interpretable, and typically more accurate than
    prompting an LLM. Reaching for an LLM here adds cost and non-determinism for no benefit.
- q: When using an LLM as a judge to grade other LLM outputs, what is the main caution?
  options:
  - The judge model is always more accurate than human labels
  - LLM-as-judge can carry systematic bias and inconsistency, so validate it against a sample of human
    labels before trusting it
  - LLM-as-judge cannot produce a numeric score
  - You must use the same model as both the judge and the model under test
  answer: 1
  why: An LLM judge is convenient for scoring open-ended outputs, but it can be biased (e.g. favoring
    verbose or same-family answers) and inconsistent. Always calibrate it against a human-labeled sample
    before relying on it, and prefer exact metrics where you have ground-truth labels.
- q: Which set of tradeoffs correctly describes an LLM API call relative to a local logistic-regression
    prediction?
  options:
  - Cheaper, lower latency, fully deterministic, keeps data local
  - Free, instant, deterministic, and private by default
  - More expensive per call, higher latency, non-deterministic, and may send sensitive data to a third
    party
  - Identical on every dimension
  answer: 2
  why: An LLM call typically costs money per token, adds network and inference latency, is non-deterministic
    across runs, and may transmit data off-premises. A local classical model is essentially free per call,
    fast, deterministic, and keeps data in your environment. These tradeoffs drive the build-vs-LLM decision.
- q: In two or three sentences, describe a real task at your organization (or a realistic one) where an
    LLM is the RIGHT tool, and explain which specific properties of the task justify it over classical
    ML.
  answer: A strong answer names an unstructured-text or generation task — e.g. summarizing free-form support
    tickets, drafting replies, extracting structured fields from messy contracts, or few-shot classification
    with very few labels — and ties the choice to properties like unstructured input, low/no labeled data,
    need for flexible reasoning or natural-language output, or rapid prototyping without a training pipeline.
  why: 'The point is to articulate the decision framework from the other side: LLMs earn their cost on
    unstructured text, generation, low-label or few-shot settings, and flexible reasoning, where building
    a classical model would be slow or impossible. Tying the justification to concrete task properties
    shows real understanding rather than defaulting to the trendiest tool.'
resources:
- label: 'Anthropic: Define your success criteria and create strong empirical evaluations'
  url: https://platform.claude.com/docs/en/test-and-evaluate/define-success
- label: 'Anthropic: Reduce hallucinations'
  url: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- label: 'scikit-learn: Metrics and scoring (classification metrics)'
  url: https://scikit-learn.org/stable/modules/model_evaluation.html
- label: 'EU AI Act: high-level summary (Future of Life Institute)'
  url: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
---

## Why Evaluation Is Non-Negotiable

You would never ship a churn model without a confusion matrix and a held-out test set. An LLM feature deserves the same discipline. The danger is that LLM output is fluent and *looks* correct, which makes 'it seems to work' feel like evidence. It isn't: a demo that impresses on five hand-picked prompts can fail on 30% of real traffic, and only an evaluation will tell you.

The mental shift: treat the prompt + model as **a classifier (or generator) you must measure**. Define what 'correct' means, collect labeled examples, run the system, and score it — the same workflow as Module 3, only the model changed.

## Building an Eval Harness

Start with a small **labeled eval set**: 50-500 examples with known answers (`y_true`). Run the LLM, parse each prediction defensively, and score with metrics you already know.

```python
from anthropic import Anthropic
from sklearn.metrics import accuracy_score, f1_score, classification_report

client = Anthropic()
LABELS = ["billing", "technical", "account", "other"]

def classify(text):
    msg = client.messages.create(
        model="claude-haiku-4-5",  # cheap model for high-volume eval runs
        max_tokens=10,
        system=f"Classify the ticket into one of: {LABELS}. Reply with only the label.",
        messages=[{"role": "user", "content": text}],
    )
    out = msg.content[0].text.strip().lower()
    return out if out in LABELS else "other"  # never eval() model output

y_pred = [classify(t) for t in X_eval]
print(accuracy_score(y_eval, y_pred))
print(f1_score(y_eval, y_pred, average='macro'))
print(classification_report(y_eval, y_pred))
```

Use `claude-haiku-4-5` for cheap eval loops; reserve `claude-opus-4-8` for genuinely hard tasks. **Never `eval()` raw model output** — parse against a known label set.

For open-ended outputs (summaries, drafts) with no single right answer, an **LLM-as-judge** can score quality. But judges carry systematic bias (favoring verbose or same-family answers) and can be inconsistent — calibrate against a human-labeled sample before trusting them.

## Hallucination

A **hallucination** is fluent, confident output unsupported by fact — an invented citation, a fabricated API. It happens because an LLM predicts likely-sounding tokens with no built-in sense of what it doesn't know. Mitigations, by impact:

- **Grounding / RAG** (from l03): retrieve real source text and answer *only* from it.
- **Ask for citations**: require the model to point to the supporting passage.
- **Permit abstention**: allow 'I don't know' so the model isn't forced to guess.
- **Verify programmatically**: check claimed URLs, numbers, and IDs against a source of truth.

## The Decision Framework: LLM vs Classical ML

The most important point in the module: **for structured tabular prediction with plenty of labels, an LLM is usually the wrong tool.**

| Signal | Classical ML | LLM |
|---|---|---|
| Input shape | Structured / tabular | Unstructured text |
| Labeled data | Plenty | Little / none (few-shot) |
| Task | Fixed prediction | Generation, reasoning |
| Cost per call | Near zero | Per-token \$ |
| Latency | Milliseconds | Hundreds of ms+ |
| Determinism | Deterministic | Non-deterministic |
| Interpretability | High (coefficients) | Low |

A gradient-boosted tree on 40 features and 200k rows is cheaper, faster, more accurate, and explainable. An LLM shines only where a classical model is impractical: messy free text, generation, and low-label settings.

## Cost, Latency, Determinism, Privacy

Four tradeoffs to make explicit in any design doc:

- **Cost**: LLM calls cost money per token; a local model is near-free per prediction.
- **Latency**: network + inference adds hundreds of ms; classical inference is sub-millisecond.
- **Determinism**: the same prompt can yield different answers; a fitted model is reproducible.
- **Privacy**: an API call may send data off-premises — check regulations (e.g. the EU AI Act) before routing personal data to a third party.

## Mini-Project Brief: LLM vs Baseline Showdown

**Goal.** Take a text-classification dataset (e.g. the 20 Newsgroups subset, or your own labeled tickets/reviews). Build **two** classifiers, evaluate both on the *same* labeled holdout with the *same* metrics, and recommend which to ship.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# Classical baseline (connects back to earlier modules)
baseline = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
baseline.fit(X_train, y_train)
base_pred = baseline.predict(X_test)

llm_pred = [classify(t) for t in X_test]  # reuse the harness above
```

**Deliverables:**

1. A prompt-based LLM classifier and a TF-IDF + logistic-regression baseline.
2. Both evaluated on one holdout with `accuracy_score`, `f1_score`, and `classification_report`.
3. A results table comparing metrics **and** cost/latency for each approach.
4. A short written recommendation: which would you ship, and why — citing the decision framework and the measured tradeoffs.

The honest answer is often 'the baseline,' and being able to defend that is the skill this module teaches.
