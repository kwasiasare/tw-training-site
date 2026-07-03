---
course: ai-app-developer-2026
title: Calling Your First LLM API
month: 1
monthTitle: Python and LLM Foundations
lesson: 2
summary: Learn to make your first programmatic call to an LLM provider's API. You'll set up authentication
  securely, send a chat request, parse the response, stream tokens as they arrive, and handle rate limits
  and errors gracefully.
objectives:
- Configure API keys securely using environment variables and avoid hard-coding secrets
- Make a basic chat completion request to an LLM API and parse the response
- Implement token streaming to display output incrementally
- Handle common errors and rate limits with retries and backoff
- Understand request parameters like model, temperature, and max tokens
video: aad-m1-l02-calling-your-first-llm-api.mp4
quiz:
- q: What is the safest way to provide your API key to your application?
  options:
  - Hard-code it directly in the source file
  - Store it in an environment variable or .env file that is git-ignored
  - Paste it into a public README for the team
  - Send it as a query parameter in the URL
  answer: 1
  why: Keys should never be in source code or public files. Environment variables or a git-ignored .env
    file (and a secrets manager in production) keep them out of version control.
- q: What does setting stream=True accomplish?
  options:
  - It makes the model more accurate
  - It returns the response incrementally as chunks/deltas
  - It disables rate limiting
  - It reduces token cost to zero
  answer: 1
  why: Streaming returns the response in small delta chunks as they're generated, improving perceived
    responsiveness, but does not change accuracy, cost, or rate limits.
- q: Which HTTP status code typically indicates you've hit a rate limit?
  options:
  - '200'
  - '404'
  - '429'
  - '500'
  answer: 2
  why: A 429 Too Many Requests response signals you've exceeded the provider's rate limit; the recommended
    response is to retry with exponential backoff.
- q: Which parameter most directly controls the maximum length and cost of a response?
  options:
  - temperature
  - model
  - max_tokens
  - stream
  answer: 2
  why: max_tokens caps how many tokens the model can generate, directly limiting response length and the
    associated cost.
- q: In one short phrase, name the retry strategy recommended for handling 429 rate-limit errors.
  answer: exponential backoff
  why: Exponential backoff increases the wait time after each failed attempt (e.g., 1s, 2s, 4s), reducing
    pressure on the API and improving the chance of success.
- q: Which field in the response object should you log to monitor token consumption and cost?
  answer: usage
  why: The usage field reports prompt_tokens, completion_tokens, and total_tokens, which you log to track
    spending.
resources:
- label: OpenAI API Reference – Chat Completions
  url: https://platform.openai.com/docs/api-reference/chat
- label: OpenAI Python SDK (GitHub)
  url: https://github.com/openai/openai-python
- label: python-dotenv documentation
  url: https://pypi.org/project/python-dotenv/
- label: OpenAI Rate Limits Guide
  url: https://platform.openai.com/docs/guides/rate-limits
---

## Overview

Calling an LLM API is the foundational skill for building AI applications. At its core, you send a structured request (your prompt plus parameters) over HTTPS and receive a generated response. This lesson uses the OpenAI Python SDK as the example, but the same concepts apply to Anthropic, Google, and most providers.

## Setting Up Your Environment

Install the SDK and a dotenv helper:

```bash
pip install openai python-dotenv
```

**Never hard-code API keys.** Store them in environment variables or a `.env` file that is git-ignored.

```
# .env
OPENAI_API_KEY=sk-...
```

```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]
```

Add `.env` to `.gitignore` so secrets never reach version control. In production, use a secrets manager (AWS Secrets Manager, Vault, or platform env vars).

## Your First Call

```python
from openai import OpenAI
import os

client = OpenAI()  # reads OPENAI_API_KEY from env automatically
# Read the model name from an env var so your code survives model churn
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Explain what an API is in one sentence."}
    ],
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].message.content)
```

### Key Request Parameters

- **model**: which model to use (affects cost, speed, quality)
- **messages**: the conversation history; roles are `system`, `user`, `assistant`
- **temperature**: 0 = deterministic, higher = more creative (0.0–2.0)
- **max_tokens**: cap on response length

### Choosing a Model

Every provider ships models in tiers. **Frontier** models give the best reasoning quality; **mini/nano** tiers trade some quality for much lower latency and cost. Choose by weighing three factors: **task difficulty, latency, and cost**. Drafting, classification, and extraction usually run fine on a mini-tier model; complex reasoning or agent work may justify a frontier model.

Model names evolve quickly — new versions ship and old ones are deprecated — so don't memorize names from a course or blog post. Check the provider's live model documentation ([OpenAI models page](https://platform.openai.com/docs/models), [Anthropic models docs](https://docs.anthropic.com/en/docs/about-claude/models/overview)) before choosing.

To keep your code working through model churn, read the model name from an environment variable with a sensible default:

```python
import os
# Swap models via env var without touching code
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
```

Any snippet in this course that hard-codes a model name can (and in production, should) use this pattern.

### Reading the Response

The response object contains `choices` (usually one), each with a `message`. It also includes a `usage` field reporting `prompt_tokens`, `completion_tokens`, and `total_tokens` — essential for tracking cost.

```python
print(response.usage.total_tokens)
```

## Streaming Responses

For a responsive UX, stream tokens as they are generated instead of waiting for the full response.

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a haiku about code."}],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

Each chunk carries a small `delta`. You concatenate deltas to build the full message.

## Same Call with Claude

The same request looks nearly identical with Anthropic's SDK (`pip install anthropic`). Two differences to note: the **system prompt is a top-level parameter** (not a message role), and **`max_tokens` is required**.

```python
from anthropic import Anthropic
import os

client = Anthropic()  # reads ANTHROPIC_API_KEY from env automatically

response = client.messages.create(
    model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5"),
    max_tokens=200,  # required on the Anthropic API
    system="You are a concise assistant.",
    messages=[{"role": "user", "content": "Explain what an API is in one sentence."}],
)
print(response.content[0].text)
```

The response shape differs slightly too: content is a list of blocks, so you read `response.content[0].text`, and token usage is reported as `response.usage.input_tokens` and `output_tokens`. Everything else — env-var keys, streaming, retries with backoff — follows the same patterns you just learned.

## Handling Errors and Rate Limits

Network calls fail. Providers enforce rate limits (requests/tokens per minute) and return `429 Too Many Requests`. Use retries with exponential backoff.

```python
import time
from openai import RateLimitError, APIError

def call_with_retry(client, **kwargs):
    for attempt in range(5):
        try:
            return client.chat.completions.create(**kwargs)
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except APIError as e:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("Max retries exceeded")
```

The SDK also has built-in retries (`max_retries` on the client). Add timeouts to avoid hanging requests.

## Cost and Safety Tips

- Set `max_tokens` to control runaway costs.
- Log `usage` to monitor spend.
- Validate and sanitize user input before sending.
- Use the cheapest model that meets quality needs.
- Rotate keys if they are ever exposed.

## Summary

You now know how to authenticate securely, send a chat request, parse responses, stream output, and handle rate limits. These primitives underpin every LLM-powered feature you'll build.
