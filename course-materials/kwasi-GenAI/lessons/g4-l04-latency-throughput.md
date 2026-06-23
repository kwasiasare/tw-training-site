---
course: kwasi-GenAI
title: Latency & throughput
month: 4
monthTitle: Production Engineering
lesson: 4
summary: 'Make LLM features feel fast and scale well: stream for perceived latency, cap max_tokens, and
  use batching and concurrency to raise throughput without melting your rate limits.'
objectives:
- Distinguish time-to-first-token, total latency, and throughput
- Use streaming to slash perceived latency without changing real compute
- Cap max_tokens and shorten output to cut total generation time
- Raise throughput with async concurrency while respecting rate limits
- Use batch processing for high-volume, non-interactive workloads
- Choose the right model size for the latency budget of a feature
video: g4-l04-latency-throughput.mp4
quiz:
- q: Why does streaming improve perceived latency even though total compute is unchanged?
  options:
  - It uses a faster model
  - The user sees the first words almost immediately instead of waiting for the whole answer
  - It skips output tokens
  - It caches the response
  answer: 1
  why: Streaming sends tokens as they're generated, so the user reads from the first token rather than
    staring at a spinner until the full answer is done.
- q: What most directly reduces total generation time for a single request?
  options:
  - Raising temperature
  - Generating fewer output tokens (lower max_tokens, concise answers)
  - Adding more context
  - Disabling streaming
  answer: 1
  why: Output is generated token by token, so fewer output tokens means less time — capping max_tokens
    and asking for brevity directly cuts latency.
- q: What is throughput, as opposed to latency?
  options:
  - The time for one request to finish
  - How many requests you can complete per unit of time
  - The cost per token
  - The size of the model
  answer: 1
  why: Latency is how long one request takes; throughput is how many requests you can process per second
    or minute across the system.
- q: Why must concurrency respect the provider's rate limits?
  options:
  - It doesn't matter
  - Firing too many simultaneous requests triggers 429 errors and backoff, hurting throughput
  - Concurrency is banned by the API
  - Rate limits only apply to streaming
  answer: 1
  why: Exceeding the requests-per-minute or tokens-per-minute limit returns 429 errors, so you cap concurrency
    and back off to keep real throughput high.
- q: In one sentence, when is the Batch API a better fit than live concurrent calls?
  answer: For large volumes of non-interactive work that can tolerate delay — like nightly evals or bulk
    classification — batch processing handles them at lower cost and without managing live rate limits.
  why: Batch trades immediacy for cheaper, simpler high-volume throughput, which suits offline jobs where
    nobody is waiting on a screen.
- q: In one sentence, how does model choice affect latency?
  answer: Smaller, faster models like Haiku respond with lower latency than larger models, so for latency-sensitive
    features you pick the smallest model that still meets your quality bar.
  why: Model size trades capability for speed, so matching the model to the latency budget is a core tuning
    lever.
resources:
- label: Anthropic — Reducing latency
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/reduce-latency
- label: Anthropic — Streaming Messages
  url: https://docs.anthropic.com/en/docs/build-with-claude/streaming
- label: Anthropic — Message Batches API
  url: https://docs.anthropic.com/en/docs/build-with-claude/batch-processing
- label: Anthropic — Rate limits
  url: https://docs.anthropic.com/en/api/rate-limits
- label: AWS — Run inference with Amazon Bedrock batch jobs
  url: https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html
---

## Three numbers, not one

"Make it faster" hides three different goals. **Time-to-first-token** is how long until the user sees *anything*. **Total latency** is how long until the full answer is done. **Throughput** is how many requests your system completes per unit of time. They're tuned with different levers, and confusing them leads to optimising the wrong thing. As an engineer who has watched p95 dashboards, this framing will feel familiar — it's tail latency versus requests-per-second, applied to token generation.

## Streaming: win the perception game

An LLM generates its answer one token at a time. Without streaming, you wait for the entire answer, then show it — the user stares at a spinner. With **streaming**, you send each token as it's produced, so the first words appear almost instantly. The real compute is identical; the *felt* speed is transformed. For any chat or interactive surface, streaming is the highest-leverage latency win you can make.

```python
with client.messages.stream(
    model="claude-sonnet-4-6", max_tokens=512,
    messages=[{"role": "user", "content": q}]) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Cap the output

Because the answer is generated token by token, **total latency scales with output length**. The longest part of most requests is the model writing a long answer. Two moves cut it: set a sensible `max_tokens` ceiling so a runaway response can't drag on, and instruct the model to be concise. This is the same lever that saved money last lesson — shorter output is both cheaper and faster. Don't over-cap, though; truncating a needed answer is a worse failure than a slightly slower one.

## Throughput: concurrency with limits

Latency is about one request; throughput is about many. Processing a queue serially wastes time, because most of each request is spent waiting on the network and the model. **Async concurrency** fires many requests in flight at once.

```python
import asyncio

async def worker(sem, q):
    async with sem:                 # cap concurrency
        return await aclient.messages.create(
            model="claude-haiku-4-5", max_tokens=256,
            messages=[{"role": "user", "content": q}])

async def run(questions, limit=8):
    sem = asyncio.Semaphore(limit)
    return await asyncio.gather(*[worker(sem, q) for q in questions])
```

The semaphore is the important part. Providers enforce **rate limits** — requests-per-minute and tokens-per-minute. Fire too many at once and you get 429 errors and forced backoff, which *lowers* real throughput. Cap concurrency below your limit and add exponential backoff on 429s. This is ordinary backpressure, the same discipline you'd apply to any downstream service.

## Batch for the big, patient jobs

Some workloads aren't interactive at all: re-running your eval suite, classifying a million records, generating embeddings overnight. Nobody is watching a screen, so immediacy doesn't matter. The **Batch API** is built for this — submit a large set of requests, collect results when they're ready, at lower cost and without you hand-managing rate limits. Amazon Bedrock offers the same batch-inference pattern. Use live concurrency when a human waits; use batch when only a deadline does.

## Pick the right model

Finally, model size *is* a latency lever. A smaller model like Haiku (`claude-haiku-4-5`) returns faster than a larger one. For a latency-sensitive feature, choose the smallest model that still clears your quality bar — and lean on the routing idea from last lesson to keep heavy models for the requests that truly need them.

## Your task

Take an interactive prompt and add streaming so the first token appears immediately; note how much better it *feels* even with identical compute. Then write an async batch runner that processes a list of twenty prompts with a concurrency semaphore and exponential backoff on 429s. Measure total latency for one request and total wall-clock for the twenty, and write down which lever helped which number.
