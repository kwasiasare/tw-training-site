---
title: Putting it together
month: 4
monthTitle: Portfolio Projects
lesson: 10
summary: Combine everything you've learned into one polished, end-to-end portfolio project that proves
  you can ship real AI work.
objectives:
- Scope a focused project that tells a clear story to recruiters
- Wire data, an LLM call, and an interface into one working app
- Keep API keys and secrets out of your code with environment variables
- Write a README that lets anyone run your project in minutes
- Add basic tests and error handling so the demo doesn't break
- Deploy or record a demo so the project is easy to view
- Present the project with results, trade-offs, and next steps
video: m4-l10-putting-together.mp4
quiz:
- q: What is the best way to store your ANTHROPIC_API_KEY in a portfolio project?
  options:
  - Paste it directly in the code
  - In an environment variable, read with os.environ
  - In the README so reviewers can use it
  - In a public config.json committed to GitHub
  answer: 1
  why: Secrets belong in environment variables (or a .env file that is git-ignored), never hard-coded
    or committed where others can see them.
- q: Which file makes a portfolio project easy for a stranger to run?
  options:
  - LICENSE
  - requirements.txt
  - README.md
  - All of these help, but the README is the entry point
  answer: 3
  why: A clear README explains what the project does and how to run it; requirements.txt and LICENSE support
    it, but the README is what a recruiter reads first.
- q: Why scope a portfolio project narrowly rather than building something huge?
  options:
  - Big projects are always better
  - A finished, focused project beats an impressive unfinished one
  - Recruiters dislike ambition
  - Narrow projects need no testing
  answer: 1
  why: One small project you actually finished and can demo cleanly is far more convincing than a sprawling
    one that doesn't run.
- q: Name one thing your README should always include so someone can run your project.
  answer: Setup/install and run instructions (e.g. install dependencies, set the API key, run the command).
  why: Without clear setup and run steps, even great code is useless to a reviewer who can't get it started.
- q: In one phrase, what should the final slide of a project presentation cover?
  answer: Results, trade-offs you made, and what you would do next.
  why: Closing with results and honest next steps shows engineering judgement, which is what employers
    are really assessing.
- q: What does pinning versions in requirements.txt (e.g. anthropic==0.39.0) protect against?
  options:
  - Slower installs
  - A future package update silently breaking your app
  - Larger repo size
  - Needing a virtual environment
  answer: 1
  why: 'Pinned versions make the project reproducible: it installs the same dependencies today and months
    from now, so it keeps working.'
resources:
- label: Anthropic Claude Messages API documentation
  url: https://docs.anthropic.com/en/api/messages
- label: GitHub Docs — About READMEs
  url: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- label: Streamlit — Get started building data apps
  url: https://docs.streamlit.io/get-started
- label: The Twelve-Factor App — Config (store config in the environment)
  url: https://12factor.net/config
---

## The goal: one project that proves it

After four months you can write Python, use Git, query data, and call an LLM. This lesson is about **putting it together** into a single portfolio project a recruiter can open, understand, and run.

The aim is not size — it's a **finished, focused** project that tells a clear story: *here is a real problem, here is how I used AI to solve it, here is the result.*

## Scope it small, ship it whole

Pick one narrow problem. A good shape is: take some **input**, send it to **Claude**, return a useful **output**, wrapped in a small interface.

Examples that work well: a CV-to-cover-letter helper, a support-ticket classifier, a notes summariser. Each is small enough to finish and clear enough to explain.

Write down, in one sentence, what done looks like. Then build to that and stop.

## The core: data in, Claude in the middle, result out

Here is the heart of almost every project — a clean call to the Claude Messages API. Keep your key in an environment variable, never in the code.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

def summarise(text: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Summarise in 3 bullets:\n{text}"}],
    )
    return msg.content[0].text
```

## Make it runnable by a stranger

A project a reviewer can't run might as well not exist. Pin your dependencies and set the key from the shell.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # Windows: set ANTHROPIC_API_KEY=...
streamlit run app.py
```

Your `requirements.txt` should pin versions, for example `anthropic==0.39.0` and `streamlit==1.39.0`, so it installs the same way every time.

## Polish: README, tests, and a demo

Three things turn code into a portfolio piece:

- **README** — one-line description, a screenshot, setup steps, and how to run it.
- **A test or two** — even one `assert` that your function returns text proves you think about correctness.
- **A demo** — deploy it or record a 60-second screen capture, and link it at the top of the README.

Add simple error handling so a missing key or empty input shows a friendly message instead of a stack trace.

## Present it like an engineer

When you talk about the project, cover three things: **the result**, the **trade-offs** you made (why this model, why this scope), and **what you'd do next**. That honesty is exactly the judgement employers are hiring for.

## Your task

Ship one end-to-end project this week: scope it in a sentence, build the data-to-Claude-to-output core, write the README, and record a short demo.
