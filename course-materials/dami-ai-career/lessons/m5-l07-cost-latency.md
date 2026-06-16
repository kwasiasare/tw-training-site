---
course: dami-ai-career
title: Cost & latency optimisation
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 7
summary: Cut the cost and response time of your LLM app by choosing the right model, caching context,
  and streaming output.
objectives:
- Understand how token pricing turns inputs and outputs into money
- Measure cost with token counting before you send a request
- Pick the right model for each task to balance cost and quality
- Use prompt caching to slash the cost of repeated context
- Reduce latency with streaming and smaller, focused prompts
- Use the Batches API for non-urgent, high-volume jobs
- Build the habit of measuring before optimising
video: m5-l07-cost-latency.mp4
quiz:
- q: In the Claude API, you pay separately for input tokens and output tokens. Which is usually more expensive
    per token?
  options:
  - Input tokens
  - Output tokens
  - They cost the same
  - Neither — billing is per request
  answer: 1
  why: Output tokens cost more per token than input tokens (e.g. Sonnet 4.6 is $3 input vs $15 output
    per million), so keeping responses short saves the most money.
- q: What is the main benefit of prompt caching when you reuse a large document across many requests?
  options:
  - It makes the model smarter
  - Cached tokens are served at roughly 10% of the normal input price
  - It removes the need for an API key
  - It increases the context window
  answer: 1
  why: Cache reads cost about a tenth of the normal input price, so reusing a cached prefix can cut input
    costs by up to ninety percent.
- q: Which technique most directly improves the *perceived* latency of a chat app — the time before the
    user sees anything?
  options:
  - Using a bigger model
  - Streaming the response token by token
  - Adding more tools
  - Raising max_tokens
  answer: 1
  why: Streaming shows tokens as they are generated, so the user sees output almost immediately instead
    of waiting for the full response.
- q: Why should you count tokens with the API before sending a large request, rather than estimating with
    a generic tokenizer?
  answer: Token counts are model-specific; generic tokenizers like tiktoken undercount Claude tokens,
    so using messages.count_tokens gives an accurate cost estimate.
  why: The count_tokens endpoint uses Claude's own tokenizer, so your cost estimate matches what you will
    actually be billed.
- q: You have 50,000 product reviews to classify overnight, and the results are not needed immediately.
    Which approach is most cost-effective?
  answer: Use the Batches API, which processes requests asynchronously at 50% of the standard price.
  why: Batch processing trades immediacy for a 50% discount, ideal for large, non-latency-sensitive jobs.
- q: True or false — the fastest way to cut cost is always to switch to the cheapest model.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. A cheap model that gives wrong answers may need retries or human fixes; match the model
    to the task and measure before deciding.
resources:
- label: Anthropic docs — Pricing
  url: https://platform.claude.com/docs/en/pricing
- label: Anthropic docs — Prompt caching
  url: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- label: Anthropic docs — Token counting
  url: https://platform.claude.com/docs/en/build-with-claude/token-counting
- label: Anthropic docs — Batch processing
  url: https://platform.claude.com/docs/en/build-with-claude/batch-processing
---

## Why cost and latency matter

Once your app works, two numbers decide whether it survives in production: how much each request **costs** and how long users **wait**. A demo that calls the most expensive model on every keystroke is fine for a weekend project, but it will burn your budget and frustrate users at scale.

The good news: a handful of techniques can cut both dramatically — often by an order of magnitude — without rewriting your logic.

## How token pricing works

The API bills per **token** (roughly three-quarters of a word). You pay separately for the **input** (your prompt) and the **output** (the model's reply), and output is several times more expensive per token. For example, Claude Sonnet 4.6 is $3 per million input tokens and $15 per million output tokens.

So the two biggest levers are: send less input, and ask for shorter output.

## Measure before you optimise

Never guess at cost — count. The `count_tokens` endpoint uses Claude's own tokenizer, so the number matches your bill. Do not use generic tokenizers like tiktoken; they undercount Claude tokens.

```python
from anthropic import Anthropic

client = Anthropic()
resp = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": open("report.md").read()}],
)
print(resp.input_tokens)
# Estimated input cost = input_tokens * 3 / 1_000_000  (dollars)
```

## Choose the right model

Not every task needs your smartest model. Use a tiered approach: a small, fast model for simple work and a larger one only where quality really matters.

```python
from anthropic import Anthropic

client = Anthropic()

# Cheap and fast — good for simple classification
resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=10,
    messages=[{"role": "user", "content": "Classify as positive or negative: Loved it!"}],
)
print(resp.content[0].text)
```

Keep your key in an environment variable (`ANTHROPIC_API_KEY`); never hard-code it.

## Cache repeated context

If many requests share a big chunk of text — a long document, a system prompt, few-shot examples — cache it. The first request writes the cache; later requests read it at roughly a tenth of the input price.

```python
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": large_document_text,
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": "Summarise the key points"}],
)
print(resp.usage.cache_read_input_tokens)  # tokens served cheaply from cache
```

Caching is a **prefix match**: keep stable content first and volatile content (timestamps, IDs) last, or you will silently invalidate the cache.

## Reduce latency

Latency is about how fast users *feel* your app, not just total compute. Two habits help most:

- **Stream** the response so users see text immediately instead of waiting for the whole reply.
- **Trim** the prompt — shorter input and a sensible `max_tokens` both speed things up.

For large, non-urgent jobs (overnight classification, bulk summaries), use the **Batches API**: it runs asynchronously at 50% of the standard price.

## Your task

Take one feature of your app, run `count_tokens` on a real request, then try one optimisation — a smaller model, caching, or streaming — and compare the before and after.
