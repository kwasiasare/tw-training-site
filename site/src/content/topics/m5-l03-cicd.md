---
title: CI/CD with GitHub Actions
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 3
summary: Automate testing and deployment of your code on every push using GitHub Actions workflows defined
  in YAML.
objectives:
- Explain what CI and CD mean and why they matter
- Create a workflow file under .github/workflows
- Understand triggers, jobs, and steps in a workflow
- Run your tests automatically on every push and pull request
- Cache dependencies and use a matrix to test multiple versions
- Store secrets safely and use them in a deploy step
video: m5-l03-cicd.mp4
quiz:
- q: What does CI stand for?
  options:
  - Code Inspection
  - Continuous Integration
  - Compiled Instructions
  - Container Image
  answer: 1
  why: 'CI is Continuous Integration: every change is automatically merged, built, and tested so problems
    surface early.'
- q: Where must a GitHub Actions workflow file live in your repository?
  options:
  - In the repo root
  - In .github/workflows/
  - In a folder named actions/
  - Anywhere, as long as it ends in .yml
  answer: 1
  why: GitHub only runs workflow files placed inside the .github/workflows/ directory.
- q: Which event would you use to run tests when someone opens a pull request?
  options:
  - push
  - pull_request
  - schedule
  - workflow_dispatch
  answer: 1
  why: The pull_request event triggers the workflow when a PR is opened, updated, or reopened.
- q: In one sentence, why should you never paste an API key directly into a workflow file?
  answer: Because the file is committed to the repo and visible to anyone with access; secrets must be
    stored in encrypted GitHub Secrets and read from the environment.
  why: Hard-coded keys leak the moment the code is shared or made public. Use repository or environment
    secrets instead.
- q: What is the difference between a job and a step?
  answer: A job is a group of steps that run together on one runner; a step is a single command or action
    inside a job.
  why: Jobs run in parallel by default on separate runners, while steps inside a job run in order on the
    same machine.
- q: What does CD usually add on top of CI?
  options:
  - Deleting old branches
  - Continuous Delivery or Deployment
  - Code formatting only
  - Database backups
  answer: 1
  why: CD extends CI by automatically delivering or deploying the build to staging or production once
    tests pass.
resources:
- label: GitHub Actions — official documentation
  url: https://docs.github.com/en/actions
- label: GitHub Actions — Workflow syntax reference
  url: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- label: GitHub Docs — Using secrets in GitHub Actions
  url: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions
- label: Martin Fowler — Continuous Integration (article)
  url: https://martinfowler.com/articles/continuousIntegration.html
---

## What is CI/CD?

**CI** stands for *Continuous Integration*: every time you push code, it is automatically built and tested so bugs show up within minutes instead of weeks. **CD** stands for *Continuous Delivery* (or *Deployment*): once the tests pass, your code is automatically delivered to staging or shipped to production.

Together, C I C D turns "it works on my machine" into "it provably works, every time, for everyone". GitHub Actions is GitHub's built-in tool for this — free for public repos and generous for private ones.

## Anatomy of a workflow

A workflow is a YAML file in `.github/workflows/`. It has three core ideas:

- **Triggers** (`on:`) — what events run it, e.g. a push or a pull request.
- **Jobs** — groups of work that run on a fresh virtual machine (a *runner*).
- **Steps** — the individual commands or reusable *actions* inside a job.

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
```

## Running your tests automatically

The workflow above checks out your code, installs Python, installs your dependencies, then runs `pytest`. If any test fails, the job goes red and GitHub blocks the merge. This is the single highest-value thing CI does for you.

You can speed things up by **caching** dependencies and test many versions at once with a **matrix**:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements.txt
      - run: pytest
```

## Secrets and deployment (CD)

Never paste an API key into a workflow file — it lives in your repo for anyone to read. Instead store it under **Settings → Secrets and variables → Actions**, then read it from the environment.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarise the test report."}],
)
print(msg.content[0].text)
```

In the workflow, you expose the secret like this so the script can read it:

```yaml
      - name: Smoke test the model
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python smoke_test.py
```

## Your task

Add a `.github/workflows/ci.yml` to one of your projects that installs dependencies and runs your tests on every push. Confirm it goes green on GitHub.
