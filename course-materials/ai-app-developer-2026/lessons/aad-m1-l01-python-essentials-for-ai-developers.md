---
course: ai-app-developer-2026
title: Python Essentials for AI Developers
month: 1
monthTitle: Python and LLM Foundations
lesson: 1
summary: Set up a modern Python environment and master the core patterns—virtual environments, typing,
  async I/O, and structured data handling—that you'll rely on in every LLM-powered project.
objectives:
- Set up an isolated Python project environment with virtual environments and dependency management
- Use type hints and Pydantic models to validate and structure LLM inputs and outputs
- Write async functions to make concurrent API calls efficiently
- Handle JSON and structured data cleanly when working with LLM responses
- Apply error handling and retry patterns for unreliable network calls
video: aad-m1-l01-python-essentials-for-ai-developers.mp4
quiz:
- q: Why should you use a virtual environment for each Python project?
  options:
  - To make Python run faster
  - To isolate dependencies so they don't collide between projects
  - To automatically encrypt your API keys
  - To enable async functions
  answer: 1
  why: Virtual environments isolate each project's dependencies, preventing version conflicts between
    projects.
- q: What is the primary benefit of using Pydantic with LLM output?
  options:
  - It makes API calls faster
  - It validates and coerces text into typed Python objects, catching malformed data
  - It replaces the need for try/except
  - It stores your API keys securely
  answer: 1
  why: Pydantic validates LLM output against a defined schema, coercing it into typed objects and raising
    clear errors on bad data.
- q: Why is async particularly well-suited for LLM API calls?
  options:
  - LLM calls are CPU-bound and need multiple cores
  - LLM calls are I/O-bound, so concurrency reduces total waiting time
  - Async makes the model more accurate
  - Async encrypts the network traffic
  answer: 1
  why: LLM calls spend most time waiting on the network (I/O-bound), so running them concurrently with
    asyncio dramatically cuts total wait time.
- q: Which function runs multiple coroutines concurrently and waits for all of them?
  options:
  - asyncio.sleep
  - asyncio.gather
  - json.loads
  - time.wait
  answer: 1
  why: asyncio.gather schedules multiple coroutines to run concurrently and returns when all have completed.
- q: What technique is used to space out retries after failed network calls, and what is its name?
  answer: Exponential backoff
  why: Exponential backoff waits progressively longer (e.g., 2**attempt seconds) between retries to avoid
    hammering a failing service.
- q: Which dict method safely returns a default when a key may be missing from LLM output?
  answer: dict.get
  why: dict.get(key, default) returns the default instead of raising a KeyError when the key is absent,
    which is common with unpredictable LLM responses.
resources:
- label: Python asyncio official documentation
  url: https://docs.python.org/3/library/asyncio.html
- label: Pydantic documentation
  url: https://docs.pydantic.dev/latest/
- label: Python venv and virtual environments guide
  url: https://docs.python.org/3/library/venv.html
- label: 'httpx: a next-generation HTTP client'
  url: https://www.python-httpx.org/
---

## Why Python for AI Developers

Python is the lingua franca of AI. Nearly every LLM provider ships a Python SDK first, and the ecosystem (Pydantic, httpx, asyncio, FastAPI) is built around the patterns you'll use to ship real apps. This lesson focuses on the practical subset of Python you actually need—not the whole language.

## Setting Up Your Environment

Never install packages globally. Each project gets its own isolated environment so dependencies don't collide.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install openai pydantic httpx python-dotenv

# Freeze for reproducibility
pip freeze > requirements.txt
```

Store secrets like API keys in a `.env` file (never commit it) and load them with `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]
```

## Type Hints: Your First Line of Defense

Type hints make code self-documenting and let editors catch bugs before runtime. They're essential when passing structured data to and from LLMs.

```python
from typing import Optional

def summarize(text: str, max_words: int = 100) -> str:
    ...

def find_user(user_id: int) -> Optional[dict]:
    ...
```

## Pydantic: Validate LLM Output

LLMs return text—often JSON-shaped text that may be malformed. Pydantic models validate and coerce that data into typed Python objects, raising clear errors when something is wrong.

```python
from pydantic import BaseModel

class Recipe(BaseModel):
    title: str
    servings: int
    ingredients: list[str]

# Parse model output safely
raw = '{"title": "Soup", "servings": 4, "ingredients": ["water", "salt"]}'
recipe = Recipe.model_validate_json(raw)
print(recipe.servings)  # 4, as an int
```

Many modern LLM SDKs accept a Pydantic model directly to enforce structured outputs.

## Async: Talk to APIs Concurrently

LLM calls are I/O-bound—you spend most time waiting on the network. `asyncio` lets you fire many requests concurrently instead of one at a time, dramatically speeding up batch work.

```python
import asyncio
import httpx

async def fetch(client: httpx.AsyncClient, prompt: str) -> str:
    resp = await client.post("https://api.example.com/v1/chat",
                             json={"prompt": prompt})
    return resp.json()["text"]

async def main(prompts: list[str]) -> list[str]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, p) for p in prompts]
        return await asyncio.gather(*tasks)

results = asyncio.run(main(["hi", "hello", "hey"]))
```

Key rules: use `async def` to define coroutines, `await` to call them, and `asyncio.gather` to run many concurrently. Never block an event loop with synchronous sleeps or heavy CPU work.

## Handling JSON and Structured Data

You'll constantly convert between JSON and Python objects. The `json` module handles the basics; Pydantic handles validation.

```python
import json

data = json.loads('{"key": "value"}')   # str -> dict
text = json.dumps(data)                  # dict -> str
```

Use `dict.get(key, default)` to avoid `KeyError` when a field might be missing—common with LLM output.

## Error Handling and Retries

Network calls fail. Wrap API calls in try/except and retry transient errors with backoff.

```python
import asyncio

async def call_with_retry(fn, retries: int = 3):
    for attempt in range(retries):
        try:
            return await fn()
        except Exception as e:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # exponential backoff
```

## Putting It Together

A typical AI app flow: load config from `.env`, define Pydantic models for your data, make async calls to the LLM, validate the response, and handle errors gracefully. Master these patterns and the rest of the course will feel natural.
