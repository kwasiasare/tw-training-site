---
course: kwasi-GenAI
title: Async & concurrency for many model calls
month: 5
monthTitle: Python for Production Apps
lesson: 1
summary: Learn async and await in Python so your code can wait on many LLM calls at once instead of one
  at a time, using asyncio.gather to fan out dozens of requests concurrently.
objectives:
- Explain why LLM calls are I/O-bound and how that makes concurrency a huge win
- Define an async function and call it with await
- Use asyncio.gather to run many model calls concurrently and collect all results
- Use the AsyncAnthropic client to make non-blocking Messages API calls
- Bound concurrency with a semaphore so you respect rate limits
- Recognise when to reach for threads or processes instead of asyncio
video: g5-l01-async-concurrency.mp4
quiz:
- q: Why does concurrency help so much when making many LLM calls?
  options:
  - LLM calls are CPU-bound, so more cores finish faster
  - 'LLM calls are I/O-bound: most of the time is spent waiting on the network, so you can wait on many
    at once'
  - It reduces the number of tokens billed
  - It makes each individual response shorter
  answer: 1
  why: An LLM call spends almost all its time waiting for the model's response over the network, so while
    one waits another can start — that overlap is where concurrency pays off.
- q: What does asyncio.gather do?
  options:
  - Runs coroutines one after another in order
  - Schedules many coroutines to run concurrently and returns all their results together
  - Converts a function into a thread
  - Caches the results of a coroutine
  answer: 1
  why: asyncio.gather takes multiple awaitables, runs them concurrently on the event loop, and returns
    a list of their results once all have finished.
- q: What keyword pauses a coroutine until an awaitable result is ready?
  options:
  - yield
  - await
  - return
  - async
  answer: 1
  why: await suspends the coroutine and hands control back to the event loop until the awaited operation
    completes, letting other coroutines run meanwhile.
- q: Why bound concurrency with an asyncio.Semaphore when calling an LLM API?
  options:
  - It makes responses arrive in order
  - It limits how many requests are in flight at once so you stay under the provider's rate limits
  - It encrypts the requests
  - It is required for await to work
  answer: 1
  why: Firing thousands of requests at once will trip rate limits; a semaphore caps the number of simultaneous
    in-flight calls to a safe ceiling.
- q: In one sentence, what is the difference between async I/O and threads for this work?
  answer: Async I/O uses a single thread and an event loop to interleave many waiting operations, which
    is ideal for I/O-bound work like network calls, whereas threads or processes are better for CPU-bound
    work.
  why: asyncio shines when the bottleneck is waiting on the network; CPU-heavy work needs real parallelism
    from threads or processes.
- q: What does an async function return when you call it without awaiting it?
  answer: A coroutine object that has not run yet; you must await it or pass it to something like asyncio.gather
    to actually execute it.
  why: Calling an async function only creates a coroutine — the event loop runs it when you await it or
    schedule it as a task.
resources:
- label: 'Python docs — asyncio: Asynchronous I/O'
  url: https://docs.python.org/3/library/asyncio.html
- label: Python docs — Coroutines and Tasks (gather, semaphore)
  url: https://docs.python.org/3/library/asyncio-task.html
- label: Anthropic — Client SDKs (AsyncAnthropic)
  url: https://docs.anthropic.com/en/api/client-sdks
- label: 'Real Python — Async IO in Python: A Complete Walkthrough'
  url: https://realpython.com/async-io-python/
- label: Anthropic — Rate limits
  url: https://docs.anthropic.com/en/api/rate-limits
---

## Why concurrency matters for LLM work

Most of your automation so far probably ran one step, then the next, then the next. That is fine when each step is quick. But an LLM call is different: you send a request and then **wait** — often a second or several — for the model to think and stream back tokens. The work isn't your CPU; it's the network and the model far away. We call this **I/O-bound** work.

Now imagine you need to summarise 200 documents, or classify a backlog of 5,000 support tickets. Done one at a time, you pay the full wait for every single call and the total time is brutal. The insight is simple: while one call is waiting, your program could start another. That overlap is **concurrency**, and for many LLM calls it can turn an hour into a minute.

## async and await in one breath

Python's tool for this is `asyncio`. You mark a function `async def`, which makes it a **coroutine**. Inside it, wherever you'd normally block waiting on something, you write `await`. The `await` keyword suspends that coroutine and hands control back to an **event loop**, which is free to run other coroutines while the first one waits.

```python
import asyncio

async def greet(name):
    await asyncio.sleep(1)   # pretend this is a network call
    return f"Hello, {name}"

async def main():
    print(await greet("Kwasi"))

asyncio.run(main())
```

Calling `greet("Kwasi")` on its own does **not** run it — it returns a coroutine object. It only runs when you `await` it, or hand it to the event loop. `asyncio.run(main())` starts the loop and runs your top-level coroutine.

## Fanning out with asyncio.gather

The payoff is `asyncio.gather`. Give it many coroutines and it runs them **concurrently**, returning all results once they finish.

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def classify(ticket):
    msg = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{"role": "user", "content": f"Label this ticket: {ticket}"}],
    )
    return msg.content[0].text

async def main(tickets):
    results = await asyncio.gather(*(classify(t) for t in tickets))
    return results

asyncio.run(main(my_tickets))
```

Note `AsyncAnthropic` and `await client.messages.create(...)`: the SDK gives you a non-blocking client so the call cooperates with the event loop. The same idea applies on Amazon Bedrock or Azure with their async clients.

## Respecting rate limits with a semaphore

Fanning out 5,000 calls at once will trip the provider's **rate limits** and get you HTTP 429s. Bound the concurrency with an `asyncio.Semaphore` so only, say, 10 calls are in flight at a time.

```python
sem = asyncio.Semaphore(10)

async def classify(ticket):
    async with sem:
        msg = await client.messages.create(...)
        return msg.content[0].text
```

The `async with sem` acquires a slot before the call and releases it after, capping in-flight work at a safe ceiling — much like limiting parallel jobs in a CI/CD pipeline.

## When asyncio is the wrong tool

asyncio is for **I/O-bound** work — waiting on networks, disks, APIs. If your bottleneck is heavy computation (CPU-bound), a single event loop won't help; reach for `concurrent.futures` with threads or, for true parallelism, processes. For calling LLMs, though, async is almost always exactly right.

## Your task

Write an async script that takes a list of 20 short prompts, calls a Claude model for each one concurrently with `asyncio.gather`, bounds concurrency to 5 with a semaphore, and prints all the answers. Time it against a plain sequential loop and note the difference.
