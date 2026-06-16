---
course: dami-ai-career
title: Environment & secrets in production
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 4
summary: Keep API keys out of your code and load them safely from the environment in development and in
  production.
objectives:
- Explain why secrets must never be hard-coded or committed to Git
- Store keys as environment variables and read them with os.environ / os.getenv
- Use a .env file in development and keep it out of Git with .gitignore
- Load .env files locally with python-dotenv without breaking production
- Set environment variables on a real host (Railway, Render, GitHub Actions)
- Fail fast and clearly when a required secret is missing
- Apply this to a real call to the Anthropic Claude API
video: m5-l04-secrets-prod.mp4
quiz:
- q: Why should an API key never be written directly into your Python source code?
  answer: Because the code is shared and committed to Git, so anyone with the repo (or the public GitHub
    page) can read and abuse the key.
  why: Secrets in source get pushed to remote, leaked in history, and copied between machines — a key
    in code is a key for everyone.
- q: Which function safely reads an environment variable and returns None instead of crashing if it is
    missing?
  options:
  - os.environ['KEY']
  - os.getenv('KEY')
  - os.read('KEY')
  - env.get('KEY')
  answer: 1
  why: os.getenv returns None when the variable is unset; os.environ['KEY'] raises a KeyError.
- q: What is the main job of a .env file?
  options:
  - It encrypts your secrets
  - It stores local config and secrets that are loaded into the environment, and is kept out of Git
  - It replaces requirements.txt
  - It is uploaded to production automatically
  answer: 1
  why: A .env file holds local key-value secrets; python-dotenv loads them into the environment and you
    add it to .gitignore so it is never committed.
- q: True or false — you should commit your .env file so teammates get the same keys.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Commit a .env.example with blank or fake values; never commit the real .env.
- q: In production on a host like Railway or Render, where do your secrets come from?
  options:
  - A committed .env file
  - The host's environment variable / secrets settings
  - Hard-coded constants
  - A public config file
  answer: 1
  why: You set them in the host's dashboard or secrets manager; the running app reads them the same way
    it reads any environment variable.
- q: What should your code do at startup if a required secret like ANTHROPIC_API_KEY is missing?
  answer: Stop immediately with a clear error message saying which variable is missing, rather than continuing
    and failing later with a confusing error.
  why: Failing fast at startup turns a mysterious mid-run crash into an obvious, fixable configuration
    message.
resources:
- label: The Twelve-Factor App — Config (store config in the environment)
  url: https://12factor.net/config
- label: python-dotenv documentation
  url: https://saurabh-kumar.com/python-dotenv/
- label: Python docs — os.environ and os.getenv
  url: https://docs.python.org/3/library/os.html#os.environ
- label: Anthropic API — getting started and authentication
  url: https://docs.claude.com/en/api/getting-started
---

## Why secrets don't belong in code

A **secret** is anything that grants access: an API key, a database password, a token. The single most common beginner mistake — and a costly one — is writing the secret straight into your Python file.

The problem is that your code travels. You commit it to Git, push it to GitHub, copy it between machines. A key written as `api_key = "sk-ant-..."` is now in your commit history forever, and if the repo is public, bots will find and abuse it within minutes.

The rule: **configuration that changes between machines, and anything secret, lives in the environment — not in the code.**

## Reading from the environment

An **environment variable** is a named value the operating system hands to your program. Python reads them through the `os` module. Use `os.getenv` so a missing value returns `None` instead of crashing.

```python
import os

api_key = os.getenv("ANTHROPIC_API_KEY")
print(api_key is not None)   # True if the variable is set
```

Your code now contains no secret — only the *name* of where to find one. The same code runs on your laptop and in production; only the environment differs.

## The .env file for local development

Typing `export ANTHROPIC_API_KEY=...` every time is tedious. In development we keep secrets in a `.env` file — plain `KEY=value` lines — and load them with the **python-dotenv** library.

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()                       # reads .env into the environment
api_key = os.getenv("ANTHROPIC_API_KEY")
```

Your `.env` file looks like this:

```bash
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
```

**Critical:** add `.env` to your `.gitignore` so it is never committed. Commit a `.env.example` with blank values so teammates know which variables to set.

## Secrets in production

In production there is no `.env` file. Instead, the host provides the variables — and `load_dotenv()` simply does nothing when no `.env` exists, so the same code works in both places.

- **Railway / Render**: add variables in the project's Variables / Environment settings.
- **GitHub Actions**: store them as repository Secrets and expose them as `env:`.

```yaml
# .github/workflows/run.yml
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python main.py
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Fail fast when a secret is missing

Don't let a missing key turn into a confusing crash three steps later. Check at startup and stop with a clear message.

```python
import os

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY is not set. Add it to your .env file.")
```

## Putting it together with the Claude API

The Anthropic SDK reads `ANTHROPIC_API_KEY` from the environment automatically — you don't even pass it in. That is the whole point: secret in the environment, never in the code.

```python
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()   # picks up ANTHROPIC_API_KEY from the environment

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
)
print(msg.content[0].text)
```

## Your task

Take one of your earlier scripts that calls the Claude API, move the key into a `.env` file, add `.env` to `.gitignore`, and confirm it still runs.
