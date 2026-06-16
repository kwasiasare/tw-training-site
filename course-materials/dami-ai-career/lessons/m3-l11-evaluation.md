---
course: dami-ai-career
title: Evaluating LLM apps
month: 3
monthTitle: LLM Application Skills
lesson: 11
summary: Measure whether your LLM app actually works — build test sets, define metrics, and grade outputs
  with code and with an LLM judge.
objectives:
- Explain why LLM apps need evaluation, not just spot-checking
- Build a small, representative evaluation dataset with inputs and expected outputs
- 'Choose metrics that fit the task: exact match, similarity, or rubric scores'
- Write code-based (deterministic) checks for structured outputs
- Use an LLM-as-judge to grade open-ended responses against a rubric
- Track results over time so you can catch regressions before users do
video: m3-l11-evaluation.mp4
quiz:
- q: Why is spot-checking a few prompts by hand a poor way to evaluate an LLM app?
  answer: It isn't repeatable or representative — small manual checks miss edge cases, can't catch regressions
    when you change the prompt or model, and don't give you a number you can track over time.
  why: Evaluation needs a fixed dataset and a metric so results are comparable across changes.
- q: Which metric is the right fit for grading a classifier that must output exactly 'positive', 'negative',
    or 'neutral'?
  options:
  - LLM-as-judge with a rubric
  - Exact match (accuracy)
  - Cosine similarity of embeddings
  - Average response length
  answer: 1
  why: A fixed label set has one correct answer per item, so exact match against the expected label is
    simplest and most reliable.
- q: What is 'LLM-as-judge'?
  options:
  - Letting the model pick its own training data
  - Using a second LLM call to grade an output against a rubric
  - A benchmark published by Anthropic
  - A tool that auto-fixes failing tests
  answer: 1
  why: For open-ended answers there's no single correct string, so you prompt a model to score the output
    against explicit criteria.
- q: When you change your prompt and your eval accuracy drops from 0.92 to 0.78, what has happened?
  options:
  - The model got smarter
  - A regression — the change made the app worse on your test set
  - The dataset is too large
  - Nothing measurable
  answer: 1
  why: A drop on a fixed test set is a regression; catching it before shipping is the whole point of evals.
- q: Give one reason to prefer a code-based check over an LLM judge when both could work.
  answer: Code-based checks are deterministic, free, and instant — so for structured or exact-match outputs
    they're cheaper and more reliable than spending a model call to judge.
  why: Use the LLM judge only where there's no programmatic ground truth, like tone or open-ended quality.
- q: Why should your evaluation dataset be kept separate from the examples you use to design the prompt?
  answer: So you measure generalisation, not memorisation — if you tune the prompt on the same examples
    you grade on, a high score may just mean you overfit to those cases.
  why: A held-out test set gives an honest estimate of how the app behaves on unseen inputs.
resources:
- label: Anthropic docs — Define your success criteria and create strong empirical evaluations
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/define-success
- label: Anthropic Cookbook — building evals and using an LLM as a judge
  url: https://github.com/anthropics/anthropic-cookbook
- label: Hugging Face — Evaluating LLMs guide
  url: https://huggingface.co/learn/cookbook/en/llm_judge
- label: Your project repo — an evals/ folder with a dataset.jsonl and a run_evals.py script
---

## Why evaluate at all?

When you build an ordinary program, you write tests: given an input, you assert the exact output. LLM apps are harder — the same prompt can give slightly different wording each time, and "correct" is often a matter of degree. But that does **not** mean you skip measuring. It means you measure deliberately.

Without evaluation you are flying blind. You tweak a prompt, it *feels* better, you ship it — and you've quietly broken three other cases. An **evaluation** (an "eval") turns "feels better" into a number you can compare.

## The three ingredients of an eval

Every eval has the same shape:

1. A **dataset** — a list of inputs paired with what a good answer looks like.
2. A **task** — the function that runs your app on each input.
3. A **metric** — a rule that scores each output, giving you one number overall.

Keep the dataset small but representative: 20–50 hand-picked cases that cover the easy path *and* the tricky edges. And hold it back — don't tune your prompt on the very examples you grade on, or you're just memorising.

## Picking a metric

Match the metric to the task:

- **Exact match** — for fixed outputs like classification labels. Did the model output exactly `positive`?
- **Similarity** — for short factual answers where wording varies; compare against the expected answer.
- **Rubric score** — for open-ended text (a summary, an email). Here there is no single right string, so you grade against explicit criteria.

## Code-based checks

Whenever there's a programmatic ground truth, check it with code — it's free, instant, and deterministic. Here we grade a sentiment classifier built on the Claude Messages API.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

dataset = [
    {"text": "I love this!", "label": "positive"},
    {"text": "This is terrible.", "label": "negative"},
    {"text": "It arrived on Tuesday.", "label": "neutral"},
]

def classify(text):
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user",
                   "content": f"Reply with one word — positive, negative, or neutral:\n{text}"}],
    )
    return msg.content[0].text.strip().lower()

correct = sum(classify(row["text"]) == row["label"] for row in dataset)
print(f"Accuracy: {correct / len(dataset):.2f}")
```

## LLM-as-judge

For open-ended outputs there's no string to match, so you ask a *second* model call to grade the answer against a rubric. Use a clear rubric and force a numeric score so you can average it.

```python
def judge(question, answer):
    rubric = (
        "Score 1-5 how accurate and helpful the answer is. "
        "Reply with ONLY the integer."
    )
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=5,
        messages=[{"role": "user",
                   "content": f"{rubric}\n\nQ: {question}\nA: {answer}"}],
    )
    return int(msg.content[0].text.strip())

score = judge("What is the capital of France?", "Paris is the capital of France.")
print(f"Judge score: {score}/5")
```

## Track it over time

Save each run's score next to the prompt and model you used. The moment a change drops the number, you've caught a **regression** before your users did. That single habit — a held-out dataset, a metric, a recorded score — is what separates a hobby prompt from a production LLM app.

## Your task

Build a tiny `evals/` folder for one of your own prompts: a `dataset.jsonl` with 10 cases, and a script that prints one accuracy or average-score number.
