---
course: dami-ai-career
title: System-design-lite for LLM apps
month: 6
monthTitle: Apply & Interview
lesson: 6
summary: 'Sketch a clean, interview-ready architecture for an LLM app: API layer, retrieval, model calls,
  caching, and guardrails.'
objectives:
- Describe the standard request path of an LLM application end to end
- Place a retrieval (RAG) layer correctly and know when you actually need one
- Reason about latency, cost, and which model size fits each job
- Apply prompt caching, batching, and streaming to control cost and speed
- 'Add guardrails: validation, retries, timeouts, and rate limiting'
- Draw a simple architecture diagram you can defend in an interview
video: m6-l06-system-design.mp4
quiz:
- q: In a typical LLM app, where does the model API call sit?
  options:
  - In the user's browser, calling the model directly
  - Behind your own backend service that holds the API key
  - Inside the database query layer
  - In the CDN edge cache only
  answer: 1
  why: Your backend holds the secret key and orchestrates the call; the browser never talks to the model
    API directly, so keys stay safe.
- q: What problem does a retrieval (RAG) layer primarily solve?
  options:
  - It makes the model train faster
  - It gives the model relevant, up-to-date context it wasn't trained on
  - It replaces the need for a database
  - It encrypts the prompt
  answer: 1
  why: RAG fetches relevant documents and injects them into the prompt, grounding answers in your own
    or current data instead of the model's frozen training.
- q: Which choice most directly reduces repeated cost when many requests share the same long preamble?
  options:
  - Switching to a bigger model
  - Prompt caching of the shared prefix
  - Lowering max_tokens to 1
  - Removing the system prompt
  answer: 1
  why: Prompt caching reuses the already-processed shared prefix at roughly a tenth of the cost, so the
    fixed context isn't re-billed on every call.
- q: Name one guardrail that protects an LLM endpoint from a slow or stuck model call.
  answer: A timeout (plus retries with backoff) so a hung request fails fast instead of blocking.
  why: Timeouts bound how long you wait; paired with bounded retries they keep one slow call from holding
    resources or hanging the user.
- q: Why pick a smaller model like Haiku for some steps in a pipeline?
  answer: It is cheaper and faster, which is fine for simple, high-volume sub-tasks like classification
    or routing.
  why: Right-sizing the model per step saves cost and latency; reserve the largest model for the genuinely
    hard reasoning.
- q: True or false — for a long response you should stream tokens rather than wait for the whole reply.
  options:
  - 'True'
  - 'False'
  answer: 0
  why: Streaming shows progress immediately and avoids HTTP timeouts on long generations, improving both
    UX and reliability.
resources:
- label: Anthropic docs — Building with Claude (Messages API overview)
  url: https://docs.anthropic.com/en/api/messages
- label: Anthropic docs — Prompt caching
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- label: Designing Data-Intensive Applications (Martin Kleppmann) — for system-design fundamentals
- label: Anthropic docs — Reduce latency and streaming
  url: https://docs.anthropic.com/en/docs/build-with-claude/streaming
---

## What is system-design-lite?

A full systems-design interview can feel huge. For LLM apps you only need a **lite** version: a clear picture of how a request flows from the user, through your backend, to the model and back. As a maths graduate you already think in terms of inputs, transformations, and outputs — an architecture diagram is just that, drawn with boxes and arrows.

The goal is to draw a diagram you can **defend**: explain each box, why it exists, and what happens if it fails.

## The standard request path

Every LLM app shares a backbone:

1. **Client** (web or mobile) sends a request to your **backend**.
2. The backend optionally **retrieves** relevant context (a database or vector search).
3. It builds a prompt and calls the **model API**. Your secret key lives here, never in the browser.
4. The reply is validated, maybe **streamed** back to the client, and logged.

```python
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

def answer(question: str, context: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="Answer using only the provided context.",
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQ: {question}"}],
    )
    return msg.content[0].text
```

## Adding retrieval (RAG)

When the model needs facts it was never trained on — your docs, recent data — add a **retrieval** layer. You search a store for the most relevant chunks and paste them into the prompt. This *grounds* answers and cuts hallucination.

Don't add RAG by reflex: if the answer fits in a short, stable prompt, skip it. Retrieval adds a database, an index, and more things that can break.

## Cost, latency, and right-sizing

Three levers keep an LLM app affordable and fast:

- **Model size** — use a small, cheap model (Haiku) for routing or classification; reserve a larger one (Opus) for hard reasoning.
- **Prompt caching** — cache the shared prefix so a long system prompt isn't re-billed every call.
- **Streaming and batching** — stream long replies for snappy UX; batch non-urgent jobs for a discount.

## Guardrails: making it robust

A design that only works on the happy path fails the interview. Add:

- **Timeouts and bounded retries** so a stuck call fails fast.
- **Input validation and output checks** (e.g. require valid JSON).
- **Rate limiting** to protect your endpoint and your bill.

```bash
# A tiny health check you can run against your own backend
curl -s --max-time 10 -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is our refund policy?"}'
```

## Your task

Pick one LLM app idea and **draw its architecture** on paper: client, backend, retrieval (if needed), model call, and guardrails. Write one sentence under each box explaining why it's there.
