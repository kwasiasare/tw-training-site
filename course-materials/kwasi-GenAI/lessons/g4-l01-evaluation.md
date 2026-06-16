---
course: kwasi-GenAI
title: 'Evaluation: golden datasets & LLM-as-judge'
month: 4
monthTitle: Production Engineering
lesson: 1
summary: Learn how to measure whether an LLM feature actually works using golden datasets, LLM-as-judge
  scoring, and regression tests that catch quality drops before users do.
objectives:
- Explain why LLM outputs need evaluation that goes beyond unit tests
- Build a golden dataset of inputs paired with reference answers and grading criteria
- Score free-form outputs with an LLM-as-judge and a clear rubric
- Choose between exact-match, similarity, and judge-based metrics for a task
- Wire evaluations into CI so a prompt change runs the suite like a regression test
- Read an eval report and decide whether a change ships or rolls back
video: g4-l01-evaluation.mp4
quiz:
- q: Why can't you test most LLM features with ordinary equality assertions?
  options:
  - LLMs never make mistakes
  - Outputs are free-form text that can be correct in many different wordings
  - Python can't compare strings
  - Assertions are deprecated
  answer: 1
  why: Generative outputs vary in wording while still being correct, so strict equality gives false failures;
    you need similarity or judge-based scoring.
- q: What is a golden dataset?
  options:
  - A paid dataset from a vendor
  - A curated set of representative inputs with reference answers and grading criteria
  - The model's training data
  - A backup of production logs
  answer: 1
  why: A golden dataset is your hand-curated set of test cases — inputs plus what a good answer looks
    like — that you grade every change against.
- q: In LLM-as-judge, what most improves the reliability of the scores?
  options:
  - Using the cheapest model
  - A precise rubric with explicit criteria and a scale
  - Asking for a one-word answer only
  - Running it once
  answer: 1
  why: A clear rubric with defined criteria and a numeric or categorical scale makes judge scores consistent
    and reproducible.
- q: Where should an LLM evaluation suite run to act as a regression test?
  options:
  - Only on the developer's laptop, manually
  - In CI on every prompt or model change
  - Never — it's too slow
  - Only after users complain
  answer: 1
  why: Running the eval suite in CI on each change turns quality into a gate, catching regressions the
    way unit tests catch broken code.
- q: In one sentence, when is exact-match scoring appropriate instead of an LLM judge?
  answer: When the task has one canonical answer — like a classification label, a JSON field, or an extracted
    value — exact-match or schema checks are cheaper and more reliable than a judge.
  why: Deterministic tasks have a single correct output, so a direct comparison is both faster and more
    trustworthy than a model-based judge.
- q: In one sentence, why should you pin a fixed eval set rather than always testing on fresh random samples?
  answer: A fixed golden set lets you compare scores across changes on equal footing, so a difference
    reflects your change rather than different test cases.
  why: Holding the test set constant isolates the effect of your change, which is the whole point of a
    regression test.
resources:
- label: Anthropic — Develop your tests and evals
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests
- label: Anthropic — Using the Evaluation tool
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool
- label: OpenAI Cookbook — Getting started with evals
  url: https://cookbook.openai.com/examples/evaluation/getting_started_with_openai_evals
- label: 'Hugging Face — A guide to evaluation: LLM-as-a-judge'
  url: https://huggingface.co/learn/cookbook/en/llm_judge
- label: Microsoft Learn — Evaluation of generative AI applications
  url: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai
---

## Why "it looked good" is not a test

You already trust unit tests in CI/CD: a function returns a value, you assert it equals the expected value, green means safe to merge. LLM features break that comfort. The output is free-form text, and a good answer can be phrased a hundred ways. Assert that the model returns exactly one string and you'll get false failures every run. Skip testing entirely and you ship quietly worse answers with every prompt tweak. **Evaluation** is how we bring engineering discipline back: a repeatable way to measure output quality so a change is a decision backed by numbers, not a vibe.

## The golden dataset

The foundation is a **golden dataset** — a curated set of representative inputs, each paired with what a good answer looks like and the criteria for judging it. Twenty to a hundred carefully chosen cases beat thousands of random ones. Cover the common path, the tricky edge cases, and the failure modes you've already seen in production.

```python
golden = [
  {"input": "Refund policy for opened software?",
   "reference": "No refunds once the licence key is revealed.",
   "must_include": ["licence key", "no refund"]},
  {"input": "Can I expense a taxi?",
   "reference": "Taxis are reimbursable up to 40 dollars with a receipt.",
   "must_include": ["receipt", "40"]},
]
```

Pin this set and treat it like a fixture. Holding the test cases constant is what makes a score difference mean *your change*, not different questions.

## Pick the right metric

Not every task needs a clever metric. Match the metric to the task:

- **Exact match / schema check** — for classification labels, extracted fields, or JSON. One canonical answer, so compare directly.
- **Keyword or substring checks** — cheap guardrails like "the answer must mention the receipt requirement".
- **Similarity** — embedding cosine similarity for "close enough in meaning".
- **LLM-as-judge** — for open-ended quality (helpfulness, faithfulness, tone) where only judgement works.

## LLM-as-judge

For free-form answers, use a capable model as a grader. The trick is a **precise rubric**: explicit criteria and a fixed scale, so scores are consistent.

```python
from anthropic import Anthropic
client = Anthropic()

JUDGE = """You are grading a support answer. Score 1-5 on:
- faithfulness: only uses facts from the reference
- completeness: covers the key points
Return JSON: {\"score\": int, \"reason\": str}."""

def judge(question, reference, answer):
    msg = client.messages.create(
        model="claude-opus-4-8", max_tokens=300,
        system=JUDGE,
        messages=[{"role": "user",
            "content": f"Q: {question}\nReference: {reference}\nAnswer: {answer}"}])
    return msg.content[0].text
```

Use a strong model as judge (here Opus, `claude-opus-4-8`), ask for a reason as well as a score so failures are debuggable, and spot-check the judge against your own ratings now and then. The same pattern runs on Amazon Bedrock or Azure — the rubric is what matters, not the cloud.

## Make it a regression test

Now connect it to the discipline you already have. Run the eval suite in CI on every prompt or model change. Compute an aggregate (mean judge score, percentage passing keyword checks) and set a threshold. If a change drops below it, the build fails — exactly like a broken unit test. You catch the quiet quality regression *before* it reaches users, and you have a number to justify shipping or rolling back.

## Your task

Write a golden dataset of ten input/reference pairs for a feature you care about. Implement two scorers: a keyword check and an LLM-as-judge with a 1-to-5 rubric. Run both against your current prompt, record the scores, then change one line of the prompt and re-run. Confirm the numbers move — and that you can now say which prompt is better with evidence.
