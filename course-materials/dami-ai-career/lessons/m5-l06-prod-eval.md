---
course: dami-ai-career
title: Production evaluation & monitoring
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 6
summary: Measure whether your deployed AI app is actually good, then watch it in production so you catch
  problems before users do.
objectives:
- Explain why offline evaluation and live monitoring are both needed
- Build a small labelled eval set and run it automatically
- 'Choose sensible metrics: accuracy, latency, cost, and quality'
- Use an LLM-as-judge to score open-ended outputs
- Log every request and response for later inspection
- Track latency, error rate, and token cost in production
- Set alerts and watch for drift so quality does not silently rot
video: m5-l06-prod-eval.mp4
quiz:
- q: What is the difference between offline evaluation and production monitoring?
  answer: Offline evaluation runs your system against a fixed test set before deploying; monitoring watches
    real live traffic after deploying.
  why: Evaluation answers 'is it good enough to ship?'; monitoring answers 'is it still good now that
    real users are hitting it?'.
- q: Why might you use an LLM as a judge instead of exact string matching?
  options:
  - It is always cheaper
  - Open-ended answers can be correct in many wordings, so exact match fails
  - It removes the need for any test set
  - It guarantees 100% accuracy
  answer: 1
  why: For free-text outputs there is no single right string, so a judge model can score correctness,
    relevance, or tone where exact match would wrongly fail valid answers.
- q: Which of these is NOT a metric you would typically monitor in production?
  options:
  - p95 latency
  - Error rate
  - Number of lines of code in the repo
  - Cost per request
  answer: 2
  why: Latency, error rate, and cost are live operational signals; lines of code is a static repo property,
    not something you watch in production.
- q: What does 'drift' mean in a deployed AI system?
  answer: When real-world inputs or model behaviour gradually change so that quality degrades even though
    the code has not changed.
  why: User questions evolve and models or data shift over time; drift is why a system that passed evals
    at launch can quietly get worse later.
- q: Why is p95 latency often more useful than average latency?
  options:
  - It is easier to compute
  - It hides slow requests
  - It shows the experience of your slowest 5% of users, who feel the pain
  - Averages cannot be logged
  answer: 2
  why: An average can look fine while a tail of very slow requests ruins the experience for some users;
    p95 surfaces that tail.
- q: Name one thing you should log for every request to support later debugging.
  answer: The input prompt, the model output, latency, token usage, and a timestamp (any one of these
    is acceptable).
  why: Structured logs let you reproduce failures, spot regressions, and trace cost and latency back to
    specific requests.
resources:
- label: Anthropic docs — Reducing latency
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/reduce-latency
- label: Anthropic docs — Create strong empirical evaluations
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests
- label: Google — ML Test Score / Rules of Machine Learning
- label: Hugging Face Evaluate library
  url: https://huggingface.co/docs/evaluate
---

## Why evaluation and monitoring matter

You have built an AI feature, wired in the Claude Messages API, and deployed it. But how do you *know* it works — and keeps working? Two practices answer this.

**Offline evaluation** runs your system against a fixed test set *before* you ship. It answers: is this good enough to release?

**Production monitoring** watches real live traffic *after* you ship. It answers: is it still good now that real users are hitting it?

A system can pass every eval at launch and still degrade later as user questions change or the world moves on. You need both.

## Build an eval set

An eval set is a small collection of representative inputs with expected outputs (or grading rules). Even 20–50 hand-picked cases catch a surprising number of regressions. Run them automatically so every change is checked.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

cases = [
    {"input": "What is 2 + 2?", "expected": "4"},
    {"input": "Capital of France?", "expected": "Paris"},
]

def answer(question: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}],
    )
    return msg.content[0].text.strip()

passed = sum(c["expected"] in answer(c["input"]) for c in cases)
print(f"{passed}/{len(cases)} passed")
```

## Pick the right metrics

Different questions need different numbers. Track a handful:

- **Accuracy / quality** — did the answer meet the expected result or rubric?
- **Latency** — how long did it take? Watch **p95**, not just the average, so the slow tail does not hide.
- **Cost** — tokens in plus tokens out, times the price per token.
- **Error rate** — fraction of requests that failed or were refused.

For open-ended answers there is no single correct string, so exact matching fails. Use an **LLM-as-judge**: ask a model to score the output against a rubric.

```python
def judge(question: str, response: str) -> int:
    prompt = (
        f"Question: {question}\n"
        f"Answer: {response}\n"
        "Score the answer 1-5 for correctness. Reply with only the number."
    )
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8,
        messages=[{"role": "user", "content": prompt}],
    )
    return int(msg.content[0].text.strip())
```

## Log and monitor in production

What you do not measure, you cannot fix. Log every request as structured data — input, output, latency, token usage, and a timestamp — so you can reproduce failures and trace cost back to specific calls.

```python
import json, time

start = time.perf_counter()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": question}],
)
log = {
    "ts": time.time(),
    "latency_s": round(time.perf_counter() - start, 3),
    "input_tokens": msg.usage.input_tokens,
    "output_tokens": msg.usage.output_tokens,
}
print(json.dumps(log))
```

Feed these logs into a dashboard, set **alerts** when latency or error rate cross a threshold, and re-run your eval set on a sample of real traffic to catch **drift** early.

## Your task

Add request logging to one of your deployed features and write a 10-case eval set you can run with a single command.
