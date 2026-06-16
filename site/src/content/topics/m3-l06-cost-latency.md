---
title: Cost, latency & token management
month: 3
monthTitle: LLM Application Skills
lesson: 6
summary: Measure tokens, pick the right model, cache shared context, and stream responses so your LLM
  apps stay fast and affordable.
objectives:
- Explain how tokens drive both the cost and the latency of an LLM request
- Count tokens before sending a request and estimate the cost
- Choose between Opus, Sonnet, and Haiku based on the job
- Cut input cost with prompt caching for repeated context
- Reduce perceived latency by streaming responses
- Cap output cost with sensible max_tokens and the right effort level
video: m3-l06-cost-latency.mp4
quiz:
- q: What is the unit you are billed on for an LLM API call?
  options:
  - Requests
  - Tokens
  - Characters
  - Seconds
  answer: 1
  why: You pay per input and output token; tokens are chunks of text roughly three-quarters of a word
    each, and output tokens usually cost more than input.
- q: Input tokens and output tokens are priced the same.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Output tokens are typically several times more expensive than input tokens, so capping output
    length matters a lot for cost.
- q: Which tool gives an accurate token count for a Claude prompt before you send it?
  options:
  - tiktoken
  - len(text)
  - client.messages.count_tokens
  - A guess of words times 1.3
  answer: 2
  why: tiktoken is OpenAI's tokenizer and undercounts Claude. Use the count_tokens endpoint, which is
    model-specific and exact.
- q: You send the same 50KB document as context on hundreds of requests. What single technique most reduces
    your input cost?
  answer: Prompt caching (cache_control on the shared prefix)
  why: Cached prefix tokens are read at roughly one-tenth of the normal input price, so repeated large
    context becomes far cheaper after the first request.
- q: Streaming makes a long response cost less money.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Streaming does not change token cost; it lowers PERCEIVED latency by showing tokens as they
    arrive instead of waiting for the whole reply.
- q: Name one way to put a hard ceiling on the cost of a single response.
  answer: Set a sensible max_tokens (and/or lower the effort level)
  why: max_tokens caps how many output tokens can be generated, bounding the most expensive part of the
    bill; effort tunes how much the model thinks.
resources:
- label: Anthropic docs - Token counting
  url: https://platform.claude.com/docs/en/build-with-claude/token-counting
- label: Anthropic docs - Prompt caching
  url: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- label: Anthropic docs - Streaming Messages
  url: https://platform.claude.com/docs/en/build-with-claude/streaming
- label: Anthropic pricing
  url: https://platform.claude.com/docs/en/about-claude/pricing
---

## Why cost and latency matter

When you call an LLM you pay per **token** and you wait for tokens to come back. Tokens are small chunks of text — roughly three-quarters of a word each. Two kinds matter: **input tokens** (your prompt) and **output tokens** (the reply). Output tokens usually cost several times more than input tokens.

As a maths graduate, think of the bill as a simple sum: `input_tokens * input_price + output_tokens * output_price`. Latency tracks the same quantities — more output tokens means a longer wait.

## Count tokens before you send

Don't guess token counts, and don't use `tiktoken` — that's OpenAI's tokenizer and it undercounts Claude. Use the model-specific `count_tokens` endpoint to measure exactly, then multiply by the price.

```python
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

result = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": open("report.txt").read()}],
)

print(result.input_tokens)
# Sonnet input is $3 per million tokens:
print(f"Input cost: ${result.input_tokens * 3 / 1_000_000:.4f}")
```

## Pick the right model

You rarely need the most powerful model for every job. Match the model to the task:

- **Haiku** (`claude-haiku-4-5`) — fast and cheap; great for classification and simple extraction.
- **Sonnet** (`claude-sonnet-4-6`) — the everyday balance of speed and intelligence.
- **Opus** (`claude-opus-4-8`) — most capable; use it for hard reasoning and long agentic work.

A classifier on Haiku can be many times cheaper than the same task on Opus, with no loss of quality for that job.

## Cache repeated context

If many requests share a big chunk of context — a document, a long system prompt, a set of examples — cache it. A cached prefix is read at roughly one-tenth of the normal input price.

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": large_document_text,  # the shared, stable part
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": "Summarise the key points."}],
)

print(response.usage.cache_read_input_tokens)  # served cheaply from cache
print(response.usage.input_tokens)             # uncached, full price
```

Caching is a **prefix match**: keep stable content first and put the changing question last, or the cache won't hit.

## Stream to cut perceived latency

Streaming doesn't change the bill, but it makes your app *feel* fast — the user sees words appear instead of staring at a spinner.

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain gradient descent simply."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Cap the output

The most expensive part of a request is the output. Set a sensible `max_tokens` so a runaway reply can't blow your budget, and use a lower **effort** level when you don't need deep reasoning. Your task: take one of your earlier scripts, run `count_tokens` on a typical prompt, and work out its cost per thousand calls.
