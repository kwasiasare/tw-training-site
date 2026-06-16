---
course: dami-ai-career
title: Evaluation harnesses
month: 4
monthTitle: Portfolio Projects
lesson: 3
summary: Build a repeatable test rig that scores your AI app against a fixed dataset so you can measure
  quality, not guess.
objectives:
- Explain what an evaluation harness is and why vibes are not enough
- Build a small labelled dataset of inputs and expected outputs
- 'Write metrics: exact match, contains, and an LLM-as-judge score'
- Loop over cases, call the model, and aggregate a pass rate
- Pin the model and keep settings deterministic for fair comparison
- Track results over time so you can catch regressions
- Wire the harness into a simple CI check
video: m4-l03-eval-harness.mp4
quiz:
- q: What is the main purpose of an evaluation harness?
  options:
  - To deploy the model to production
  - To measure model output quality against a fixed dataset
  - To fine-tune the model weights
  - To reduce the API bill
  answer: 1
  why: An eval harness runs your app over a known set of cases and scores the outputs, turning 'it feels
    better' into a number you can track.
- q: Why is a single fixed dataset important for fair comparison?
  answer: It keeps the inputs and expected answers constant, so any change in score comes from your code
    or prompt, not from different test data.
  why: If the dataset moves, you can't tell whether a score change is a real improvement or just easier
    examples.
- q: Which metric is best when answers are free-form text and exact match is too strict?
  options:
  - Exact string match
  - LLM-as-judge
  - File size
  - Token count
  answer: 1
  why: LLM-as-judge uses a separate model call to grade an answer against a rubric, handling wording differences
    that break exact match.
- q: Why pin the model ID (e.g. claude-sonnet-4-6) in your harness?
  answer: So results are comparable over time; an unpinned or changing model could shift scores for reasons
    unrelated to your code.
  why: 'Reproducibility: pinning the model isolates your changes as the cause of any score movement.'
- q: What does a regression mean in the context of an eval harness?
  options:
  - A new feature shipped
  - The pass rate dropped after a change
  - The model got faster
  - A test was added
  answer: 1
  why: A regression is when a change lowers your score versus the last run — exactly what the harness
    exists to catch.
- q: Why run the eval harness in CI (continuous integration)?
  answer: To automatically catch quality drops on every commit or pull request before they reach users.
  why: 'CI makes the eval a gate: if the pass rate falls below a threshold, the build fails and you investigate
    before merging.'
resources:
- label: Anthropic docs — Test and evaluate your prompts
  url: https://platform.claude.com/docs/en/test-and-evaluate/eval-tool
- label: Anthropic Cookbook (GitHub) — evaluation examples
  url: https://github.com/anthropics/anthropic-cookbook
- label: Hugging Face Evaluate — metrics library
  url: https://huggingface.co/docs/evaluate
- label: pytest documentation — for wiring evals into CI
  url: https://docs.pytest.org/
---

## Why you need an eval harness

When you tweak a prompt and the output looks nicer, how do you *know* it actually got better? You don't — unless you measure it. An **evaluation harness** is a small program that runs your AI app over a fixed set of test cases and scores the results. It turns "this feels better" into a number you can compare run to run.

As a maths graduate this should feel natural: you're defining a function from (input, expected) pairs to a score, then aggregating.

## The three ingredients

Every harness has three parts:

1. A **dataset** — a list of inputs paired with expected answers (or a rubric).
2. A **metric** — a function that scores one model output against the expected answer.
3. A **runner** — a loop that calls the model for each case, scores it, and aggregates.

Keep the dataset small and fixed at first (10-30 cases). A frozen dataset is what makes results comparable.

## A minimal dataset

Store cases as plain data so they're easy to read and extend:

```python
cases = [
    {"input": "What is 2 + 2?", "expected": "4"},
    {"input": "Capital of France?", "expected": "Paris"},
    {"input": "Is 7 prime?", "expected": "yes"},
]
```

## Calling the model and scoring

Pin the model so re-runs are comparable. We use the Anthropic Claude Messages API:

```python
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

def run_case(prompt: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()

def contains_score(output: str, expected: str) -> int:
    return 1 if expected.lower() in output.lower() else 0

passed = 0
for case in cases:
    out = run_case(case["input"])
    passed += contains_score(out, case["expected"])

print(f"Pass rate: {passed}/{len(cases)}")
```

## LLM-as-judge for free-form answers

Exact match breaks on essays, summaries, and explanations. For those, ask a second model call to grade the answer against a short rubric, returning a number you can average. Keep the judge prompt strict and ask for just a score so it's easy to parse.

## Wiring it into CI

Turn the harness into a test that fails when quality drops, then run it on every pull request:

```bash
# fail the build if the eval pass rate is below threshold
pytest tests/test_eval.py -q
```

Now a prompt change that quietly makes things worse gets caught before it ships.

## Your task

Build a 10-case dataset for a small task you care about, write a `contains` metric, and print a pass rate.
