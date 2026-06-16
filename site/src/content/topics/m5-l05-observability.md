---
title: Observability & logging
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 5
summary: Make your app explain itself in production using structured logs, request IDs, metrics, and traces
  so you can find problems fast.
objectives:
- 'Understand the three pillars of observability: logs, metrics, and traces'
- Use Python's logging module with levels instead of print statements
- Write structured (JSON) logs so machines can search and filter them
- Attach request IDs and context to follow one request across your code
- Track latency, token usage, and errors for LLM API calls
- Avoid logging secrets and other sensitive data
- Know when to reach for a tool like Sentry or a metrics dashboard
video: m5-l05-observability.mp4
quiz:
- q: Which Python module is the standard, built-in way to record what your program is doing?
  options:
  - print
  - logging
  - tracing
  - console
  answer: 1
  why: The logging module ships with Python and gives you levels, formatting, and configurable destinations
    that print cannot.
- q: 'Put these log levels in order from least to most severe: ERROR, DEBUG, INFO, WARNING.'
  answer: DEBUG, INFO, WARNING, ERROR
  why: DEBUG is the most detailed and least severe; ERROR signals something genuinely went wrong. CRITICAL
    sits above ERROR.
- q: Why are structured (JSON) logs better than plain text logs for a deployed app?
  options:
  - They use less disk space
  - Machines can search, filter, and aggregate the fields
  - They are encrypted by default
  - They run faster
  answer: 1
  why: Each log becomes key-value data, so tools can query by request_id, level, or latency instead of
    grepping raw strings.
- q: What is the purpose of attaching a request ID to every log line for a single request?
  answer: It lets you trace one request's whole journey through your code, even when many requests run
    at once.
  why: A shared correlation ID ties scattered log lines together so you can follow exactly what happened
    for one user's call.
- q: Which of these should you NEVER write into a log?
  options:
  - The HTTP status code
  - The response latency in milliseconds
  - A user's API key or password
  - The model name you called
  answer: 2
  why: Logs are often stored and shared widely; secrets and credentials must never be written to them.
- q: For an LLM-powered endpoint, name two numbers worth logging on every call.
  answer: Latency and token usage (input and output tokens); error rate is also valuable.
  why: Latency and tokens drive your cost and user experience, so tracking them per call lets you spot
    slow or expensive requests.
resources:
- label: Python docs — Logging HOWTO (official tutorial)
  url: https://docs.python.org/3/howto/logging.html
- label: Python docs — logging module reference
  url: https://docs.python.org/3/library/logging.html
- label: Sentry — Python error monitoring (Getting Started)
  url: https://docs.sentry.io/platforms/python/
- label: Google SRE Book — Monitoring Distributed Systems (free online)
  url: https://sre.google/sre-book/monitoring-distributed-systems/
---

## Why observability?

On your laptop you can watch your program run. In production you cannot — it runs on a server somewhere, serving real users, and the first sign of trouble is often an angry message. **Observability** is the practice of making your app explain itself: emitting enough signal that you can answer *what happened?* and *why?* without redeploying.

It rests on three pillars: **logs** (a timestamped record of events), **metrics** (numbers over time, like requests per minute), and **traces** (the path of one request through your system).

## Logging properly: stop using print

`print()` is fine while you write code, but it has no levels, no timestamps, and no easy way to switch off. Python's built-in `logging` module fixes all of that.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger(__name__)

log.info("Server started")
log.warning("Cache miss for user %s", user_id)
log.error("Payment failed", exc_info=True)
```

**Levels** let you control noise: DEBUG, INFO, WARNING, ERROR, CRITICAL. In production you might show INFO and above; while debugging you drop to DEBUG.

## Structured logs

Plain-text logs are readable by humans but painful for machines. **Structured logging** emits each line as JSON, so a log platform can filter by any field.

```python
import json, logging, time

def log_event(**fields):
    fields["ts"] = time.time()
    print(json.dumps(fields))

log_event(level="INFO", event="llm_call", model="claude-sonnet-4-6",
          latency_ms=842, input_tokens=120, output_tokens=210)
```

Now you can ask your tooling "show me every `llm_call` slower than 2000ms" instead of grepping raw text.

## Request IDs: following one request

When many requests run at once, their log lines interleave. Attach a **request ID** (a correlation ID) to every line for a request, and you can follow that one request end to end.

```python
import uuid, logging

log = logging.getLogger(__name__)

def handle(request):
    request_id = str(uuid.uuid4())
    log.info("received", extra={"request_id": request_id})
    # ... do work, passing request_id everywhere ...
    log.info("completed", extra={"request_id": request_id})
```

## Observability for LLM calls

LLM endpoints have their own signals worth tracking: **latency**, **token usage** (which drives cost), and **errors**. Wrap each Claude call and log the outcome.

```python
import time, logging
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from env
log = logging.getLogger(__name__)

start = time.perf_counter()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarise this ticket."}],
)
latency_ms = round((time.perf_counter() - start) * 1000)
log.info("llm_call ok latency_ms=%s in=%s out=%s",
         latency_ms, msg.usage.input_tokens, msg.usage.output_tokens)
```

## Don't log secrets, and reach for tools

Logs get stored, copied, and shared — so **never** write API keys, passwords, tokens, or full user data into them. Redact or omit them.

Once your logs are structured, dedicated tools earn their keep: **Sentry** captures and groups exceptions with full stack traces; a metrics dashboard charts latency and error rates over time. Start with good logs, then layer tools on top.

## Your task

Take one endpoint from your project and add structured logging with a request ID, plus latency and token logging on any LLM call.
