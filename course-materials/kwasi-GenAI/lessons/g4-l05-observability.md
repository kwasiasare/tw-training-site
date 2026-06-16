---
course: kwasi-GenAI
title: Observability & tracing
month: 4
monthTitle: Production Engineering
lesson: 5
summary: 'See inside your LLM app in production: log prompts, outputs, cost, and latency, trace multi-step
  chains and agents, and use tools like LangSmith and Langfuse to debug what users actually hit.'
objectives:
- Explain why LLM apps need observability beyond ordinary application logs
- 'Capture the right fields per call: prompt, output, tokens, cost, latency, model'
- Trace a multi-step chain or agent run as a tree of spans
- Use a platform like LangSmith or Langfuse to inspect and debug runs
- Attach user feedback and eval scores to traces for continuous improvement
- Build dashboards and alerts on cost, latency, and error-rate
video: g4-l05-observability.mp4
quiz:
- q: Why are ordinary application logs not enough for an LLM app?
  options:
  - They're too fast
  - You also need the actual prompts, outputs, token usage, and cost to debug quality and spend
  - Logs are illegal for AI
  - LLMs don't produce logs
  answer: 1
  why: Debugging an LLM feature means seeing the exact prompt, the model's output, and the cost/latency
    — fields ordinary request logs don't capture.
- q: What is a trace in the context of an LLM agent or chain?
  options:
  - A single API key
  - A tree of spans showing each step — retrieval, model calls, tool calls — in one run
  - The model's training history
  - A type of prompt
  answer: 1
  why: A trace records a whole run as nested spans, so you can see each retrieval, model call, and tool
    call and where time or errors went.
- q: Which fields should you log on every model call for observability?
  options:
  - Only the final answer
  - Prompt, output, model, input/output tokens, cost, and latency
  - Just the latency
  - Only errors
  answer: 1
  why: Capturing prompt, output, model, token usage, cost, and latency lets you debug quality, track spend,
    and spot regressions per call.
- q: What do LangSmith and Langfuse primarily provide?
  options:
  - A new LLM model
  - Tracing, logging, and evaluation dashboards for LLM apps
  - A faster network
  - A vector database only
  answer: 1
  why: Both are LLM observability platforms that capture traces, log prompts/outputs/cost/latency, and
    support evaluation and feedback on real runs.
- q: In one sentence, why attach user feedback and eval scores to traces?
  answer: Linking feedback and scores to the exact run lets you find the prompts and inputs that produced
    bad answers and feed them back into your golden dataset and fixes.
  why: Connecting outcomes to the precise trace closes the loop between production behaviour and the evals
    you use to improve the system.
- q: In one sentence, what's a sensible privacy precaution when logging prompts and outputs?
  answer: Redact or avoid logging sensitive data like PII or secrets, control access to the logs, and
    follow retention rules, because prompts and outputs often contain user data.
  why: Prompts and outputs frequently carry personal or confidential data, so observability must respect
    the same data-protection discipline as any other system.
resources:
- label: LangSmith — Observability and tracing docs
  url: https://docs.smith.langchain.com/observability
- label: Langfuse — Tracing for LLM applications
  url: https://langfuse.com/docs/tracing
- label: OpenTelemetry — GenAI semantic conventions
  url: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- label: Anthropic — Token counting (usage in responses)
  url: https://docs.anthropic.com/en/docs/build-with-claude/token-counting
- label: Microsoft Learn — Monitor generative AI applications
  url: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/monitor-applications
---

## You can't fix what you can't see

A user says "the assistant gave me a wrong answer yesterday." In a normal service you'd pull the logs and reconstruct the request. In an LLM app, ordinary logs fail you: they show the HTTP request and a 200, but not the **prompt** that was assembled, the **output** the model returned, which **model** ran, how many **tokens** it cost, or how long it took. **Observability** for LLM apps means capturing all of that, so production behaviour is debuggable instead of a mystery. This is the same instinct behind your existing metrics, logs, and traces — extended to the things that make GenAI different.

## What to log on every call

For each model call, capture a structured record:

```python
record = {
    "ts": now(), "model": "claude-sonnet-4-6",
    "system": system_prompt, "input": user_msg,
    "output": msg.content[0].text,
    "input_tokens": msg.usage.input_tokens,
    "output_tokens": msg.usage.output_tokens,
    "cost": cost(msg.usage), "latency_ms": elapsed,
    "request_id": req_id, "user_id": uid,
}
```

The usage field on the response gives you exact token counts (the basis for cost from lesson 3) and your timer gives latency (lesson 4). A `request_id` lets you tie a complaint to the precise run. Be deliberate about privacy: prompts and outputs often contain PII or secrets, so redact sensitive fields, lock down access, and set retention — the same data-protection discipline you already apply elsewhere.

## Tracing multi-step runs

Real apps aren't one call. A RAG request does retrieval, then a model call; an agent loops through tool calls and model calls. A flat log can't show that shape. A **trace** records the whole run as a tree of **spans** — one span per step, nested under a parent — so you can see retrieval took 40ms, the model call took 1.2s, and the second tool call is where it failed.

```python
with trace("rag_request") as run:
    with run.span("retrieve") as s:
        chunks = retriever.search(q); s.log(k=len(chunks))
    with run.span("generate"):
        answer = llm(q, chunks)
```

If you've read distributed traces in a microservice stack, this is the same mental model — a parent request fanning into child spans, with timing and metadata on each.

## LangSmith and Langfuse

You don't have to build the viewer yourself. **LangSmith** and **Langfuse** are observability platforms purpose-built for LLM apps. They capture traces, log prompts, outputs, tokens, cost, and latency, and give you a UI to inspect any run step by step. Langfuse is open-source and self-hostable — attractive if data residency matters, which it often does for a security-minded engineer. Both integrate with a few lines of code and follow the emerging **OpenTelemetry GenAI** conventions, so this isn't a walled garden.

## Close the loop with feedback and evals

Observability becomes a flywheel when you attach outcomes to traces. Record a thumbs-up/down, or run last-module's **LLM-as-judge** over production samples and store the score on the trace. Now you can filter to "runs the judge scored low," read the exact prompt and context that produced them, and feed those cases straight back into your **golden dataset**. Production failures become tomorrow's regression tests.

## Dashboards and alerts

Finally, aggregate. Build dashboards for cost per day, p50/p95 latency, error rate, and token usage per feature, and set alerts: spend spiking, latency breaching a threshold, error rate climbing. This is exactly the SRE discipline you already have — you're just pointing it at tokens, cost, and answer quality instead of CPU and disk.

## Your task

Wrap your RAG or agent call so every model call logs a structured record with prompt, output, model, tokens, cost, and latency. Add simple span timing around retrieval and generation so you can see where the time goes. Then either integrate Langfuse (or LangSmith) or write the records to a JSONL file and build one summary that reports average cost, p95 latency, and error rate. Identify one slow or expensive step from the data.
