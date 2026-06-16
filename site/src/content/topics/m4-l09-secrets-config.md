---
title: Secrets & configuration management
month: 4
monthTitle: Portfolio Projects
lesson: 9
summary: Keep API keys out of your code, load settings from the environment, and never commit a secret
  to Git again.
objectives:
- Explain why secrets must never live in source code or Git history
- Separate configuration from code using environment variables
- Load secrets safely with a .env file and python-dotenv
- Protect secrets with .gitignore and an .env.example template
- Call the Anthropic Claude API using a key read from the environment
- Know how secrets are injected in CI/CD and cloud deployments
- Respond correctly when a secret leaks
video: m4-l09-secrets-config.mp4
quiz:
- q: Where should an API key like ANTHROPIC_API_KEY live?
  options:
  - Hard-coded in your Python file
  - In an environment variable, loaded at runtime
  - In the README so teammates can find it
  - Committed to Git in a config.py
  answer: 1
  why: Secrets belong in the environment (or a secret manager), never in source code. Code reads them
    at runtime via os.environ.
- q: Why must the .env file be added to .gitignore?
  answer: So it is never committed to Git, keeping real secrets out of the repository and its history.
  why: Once a secret is pushed to a shared or public repo it is considered compromised, even after deletion,
    because it stays in history.
- q: What is the purpose of an .env.example file?
  options:
  - It stores the real production keys
  - It is a committed template listing variable names with no real values
  - It replaces .gitignore
  - It encrypts your secrets
  answer: 1
  why: .env.example is committed and documents which variables are needed, using placeholder values so
    teammates know what to set.
- q: True or false — deleting a leaked key from a file and committing the fix makes the repo safe.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. The key remains in Git history. You must rotate (revoke and regenerate) the key, not just
    delete it.
- q: In Python, how do you read an environment variable named ANTHROPIC_API_KEY?
  answer: os.environ["ANTHROPIC_API_KEY"] or os.getenv("ANTHROPIC_API_KEY").
  why: The os module exposes the environment; getenv returns None (or a default) if the variable is missing
    instead of raising.
- q: How are secrets provided to a deployed app or a CI/CD pipeline?
  options:
  - You commit the .env file to the deploy branch
  - Through the platform's secret store or repository secrets, injected as env vars
  - You email them to the server
  - You paste them into the build log
  answer: 1
  why: Platforms like GitHub Actions and cloud hosts provide encrypted secret stores that are injected
    as environment variables at run time.
resources:
- label: python-dotenv — read .env files into environment variables
  url: https://pypi.org/project/python-dotenv/
- label: The Twelve-Factor App — Config (store config in the environment)
  url: https://12factor.net/config
- label: GitHub Docs — Using secrets in GitHub Actions
  url: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions
- label: Anthropic — API keys and authentication
  url: https://docs.anthropic.com/en/api/getting-started
---

## Why secrets must leave your code

A **secret** is any value that grants access: an API key, a database password, a token. The golden rule is simple — secrets never belong in source code. If you hard-code a key, anyone who reads your repo can use it, and once it is pushed to Git it lives in the **history** forever, even after you delete the line.

This matters for your portfolio. Public GitHub repos are scanned constantly by bots, and a leaked Anthropic or cloud key can be abused within minutes, running up a bill on your account.

## Configuration belongs in the environment

The fix is to separate **configuration** from **code**. Your code stays the same everywhere; only the settings change between your laptop, a teammate's machine, and production. The standard place to put those settings is **environment variables** — named values the operating system hands to your program at run time.

```python
import os

api_key = os.environ["ANTHROPIC_API_KEY"]   # raises if missing
debug = os.getenv("DEBUG", "false")          # default if missing
```

Use `os.environ[...]` when the value is required, and `os.getenv(name, default)` when it is optional.

## The .env file for local development

Typing `export VAR=...` every session is tedious, so locally we keep settings in a **.env** file and load them with **python-dotenv**. The `.env` file is for your machine only — it must never be committed.

```bash
# .env  (NEVER commit this file)
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
DEBUG=true
```

```python
from dotenv import load_dotenv
import os

load_dotenv()                                # reads .env into the environment
key = os.environ["ANTHROPIC_API_KEY"]
```

## Protect it with .gitignore and a template

Two files keep you safe. Add `.env` to **.gitignore** so Git ignores it, and commit an **.env.example** with the variable *names* but fake values, so teammates know what to set.

```bash
# .gitignore
.env
.env.*
!.env.example
```

The `.env.example` is committed; the real `.env` is not.

## Using a secret with the Claude API

The Anthropic client reads `ANTHROPIC_API_KEY` from the environment automatically — you never pass the key in code.

```python
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()                         # picks up ANTHROPIC_API_KEY
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)
print(msg.content[0].text)
```

## Secrets in CI/CD and the cloud

Your `.env` never leaves your laptop, so how does a deployed app get its keys? Through the platform's encrypted **secret store**. In GitHub Actions you add **repository secrets** and reference them in the workflow; the host injects them as environment variables at run time.

```yaml
# .github/workflows/ci.yml
steps:
  - run: python app.py
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

If a key ever leaks, **rotate** it — revoke the old one and generate a new one. Deleting the file is not enough.
