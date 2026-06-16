---
course: dami-ai-career
title: Take-home assignments strategy
month: 6
monthTitle: Apply & Interview
lesson: 8
summary: Plan, scope, and deliver take-home coding challenges that read clearly, run cleanly, and show
  how you actually think.
objectives:
- Read the brief carefully and clarify scope before writing any code
- Time-box the work and prioritise a working end-to-end solution
- Structure the repo so a reviewer can run it in minutes
- Write a README that explains decisions, trade-offs, and how to run
- Add a few meaningful tests instead of chasing full coverage
- Document assumptions and what you would do with more time
- Avoid common red flags that get strong candidates rejected
video: m6-l08-take-homes.mp4
quiz:
- q: What is the single most important thing a reviewer wants from your take-home?
  options:
  - Maximum lines of code
  - Code that runs and solves the core problem clearly
  - Every possible edge case handled
  - A custom framework you built
  answer: 1
  why: Reviewers first check that it runs and solves the stated problem cleanly. Clarity beats cleverness
    and volume.
- q: You have a strict time-box but cannot finish every feature. What should you do?
  options:
  - Submit nothing until it is perfect
  - Deliver a working core and note remaining work in the README
  - Hand in broken half-features for each requirement
  - Ask for a deadline extension every time
  answer: 1
  why: A working end-to-end slice plus an honest 'what I'd do with more time' section is far stronger
    than several half-finished features.
- q: Why should you write a README even for a small take-home?
  options:
  - To pad the submission
  - So the reviewer can run it and understand your decisions quickly
  - Because READMEs are legally required
  - To hide weak code
  answer: 1
  why: The README is the first thing a reviewer reads. Clear setup steps and stated trade-offs make their
    job easy and signal seniority.
- q: A brief is ambiguous about an input format. What is the best response?
  answer: State a reasonable assumption explicitly in the README (and ask the recruiter if there's time),
    then build to it.
  why: Reviewers want to see judgement. Documenting an explicit, reasonable assumption is better than
    guessing silently or stalling.
- q: Name two things to check before you submit, beyond 'the code works'.
  answer: That it runs from a clean clone (fresh setup), and that no secrets or API keys are committed.
  why: A clean-clone run and removing secrets are classic last-mile checks. A repo that fails on a fresh
    machine reads as careless.
- q: Should you aim for 100% test coverage on a take-home?
  options:
  - Yes, always
  - No — a few meaningful tests on core logic are enough
  answer: 1
  why: Time is limited. A handful of well-chosen tests on the important paths shows discipline; chasing
    total coverage usually wastes the time-box.
resources:
- label: GitHub Docs — About READMEs
  url: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- label: pytest — official documentation
  url: https://docs.pytest.org/
- label: The Pragmatic Programmer (Hunt & Thomas) — on clarity and trade-offs
- label: Anthropic — Claude Messages API docs
  url: https://docs.anthropic.com/en/api/messages
---

## What reviewers actually grade

A take-home is not a puzzle to win — it's a small sample of how you'd work on the team. Reviewers spend ten to twenty minutes per submission, so they look for the same things every time: does it **run**, does it **solve the stated problem**, and can they **follow your reasoning**.

Clarity beats cleverness. A simple, readable solution that runs from a clean clone will out-score a brilliant but tangled one. Most rejections come from repos that don't run, ignore the brief, or hide good work behind no explanation.

## Scope before you code

Read the brief twice. List the **must-haves** versus the **nice-to-haves**. If anything is ambiguous, write down a reasonable assumption (and email the recruiter if there's time). Then time-box: decide up front how many hours this gets, and aim for a working end-to-end slice first.

A common trap is starting four features and finishing none. Finish one path completely, then widen.

## Structure the repo for the reviewer

Make it runnable in minutes. Pin dependencies, give one obvious entry point, and put setup steps at the top of the README.

```bash
git clone <your-repo> && cd <your-repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py --input data/sample.csv
```

Keep secrets out of the repo. Read keys from environment variables, never commit them, and add a `.env.example` showing what's needed.

## A small, honest test suite

You don't need full coverage — you need to show you can test the parts that matter. Pick the core logic and the trickiest edge case.

```python
from analyse import top_tag

def test_top_tag_picks_most_common():
    rows = [{"tag": "a"}, {"tag": "b"}, {"tag": "a"}]
    assert top_tag(rows) == "a"

def test_top_tag_empty_returns_none():
    assert top_tag([]) is None
```

Run them with `pytest -q` and make sure they pass on a clean checkout.

## If the task involves an LLM

Some modern take-homes ask you to call a model. Keep it simple, keep the key in an environment variable, and use the current Claude Messages API — not any deprecated completions endpoint.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from env

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarise this ticket in one line."}],
)
print(msg.content[0].text)
```

Note in the README which model you chose and why, and handle the case where the key is missing so the grader gets a clear error, not a crash.

## Final checklist and your task

Before you submit: clone fresh and run it, check no secrets are committed, proofread the README, and write a short 'with more time I would...' section. Then ship it on time.

Your task: take any small script from this course, wrap it in a clean repo with a README, one entry point, and two tests, exactly as if it were a take-home.
