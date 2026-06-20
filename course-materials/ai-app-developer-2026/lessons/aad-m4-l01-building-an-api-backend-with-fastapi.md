---
course: ai-app-developer-2026
title: Building an API Backend with FastAPI
month: 4
monthTitle: Deployment and Capstone Project
lesson: 1
summary: Learn to expose your LLM-powered application as a production-ready REST API using FastAPI. This
  lesson covers input validation with Pydantic, streaming token-by-token responses with Server-Sent Events,
  structured error handling, and patterns for keeping API keys secure and requests resilient.
objectives:
- Scaffold a FastAPI application and define typed request/response models with Pydantic
- Validate and sanitize user input before passing it to an LLM
- Implement streaming responses so tokens reach clients incrementally
- Add robust error handling with appropriate HTTP status codes and structured error payloads
- Apply security and reliability practices such as API key management, timeouts, and CORS
video: aad-m4-l01-building-an-api-backend-with-fastapi.mp4
quiz:
- q: What HTTP status code does FastAPI return by default when a request fails Pydantic validation?
  options:
  - '400'
  - '422'
  - '500'
  - '404'
  answer: 1
  why: FastAPI returns 422 Unprocessable Entity with detailed field errors when request data violates
    the Pydantic model constraints.
- q: Which media type should a streaming SSE endpoint set on its StreamingResponse?
  options:
  - application/json
  - text/plain
  - text/event-stream
  - multipart/form-data
  answer: 2
  why: 'Server-Sent Events use the text/event-stream media type, and each message is prefixed with ''data:
    ''.'
- q: Why is async support particularly valuable for an LLM API backend?
  options:
  - It makes the model produce better answers
  - Most latency is I/O waiting on the provider, so async frees workers to handle other requests
  - It reduces token costs
  - It encrypts requests automatically
  answer: 1
  why: LLM calls are I/O-bound; async lets a worker handle other requests while awaiting the provider
    response, improving throughput.
- q: Which status code best represents an upstream model provider timing out?
  options:
  - '200'
  - '404'
  - '504'
  - '301'
  answer: 2
  why: 504 Gateway Timeout signals that an upstream service (the model provider) did not respond in time.
- q: Name one practice for keeping API keys secure in a FastAPI deployment.
  answer: Load them from environment variables instead of hardcoding them in source.
  why: Storing secrets in environment variables (or a secrets manager) keeps them out of source control
    and out of client responses.
- q: What is the purpose of declaring a response_model on an endpoint?
  answer: It validates and documents the response shape, ensuring clients receive a consistent, typed
    payload.
  why: response_model lets FastAPI serialize, validate, and auto-document the output, filtering out unexpected
    fields.
resources:
- label: FastAPI Official Documentation
  url: https://fastapi.tiangolo.com/
- label: 'FastAPI: Custom Response & StreamingResponse'
  url: https://fastapi.tiangolo.com/advanced/custom-response/
- label: Pydantic Field Validation Docs
  url: https://docs.pydantic.dev/latest/concepts/fields/
- label: Uvicorn Deployment Guide
  url: https://www.uvicorn.org/deployment/
---

## Why FastAPI for AI Apps

FastAPI is the de-facto choice for shipping Python-based AI services. It gives you:

- **Type-driven validation** via Pydantic — fewer bad requests reach your model.
- **Async support** — essential when most of your latency is waiting on an LLM provider.
- **Auto-generated docs** at `/docs` (Swagger) and `/redoc`.
- **Native streaming** through `StreamingResponse`, which pairs perfectly with token streaming from LLMs.

## Project Scaffold

Install the essentials:

```bash
pip install fastapi uvicorn[standard] pydantic openai
```

A minimal app:

```python
from fastapi import FastAPI

app = FastAPI(title="AI Chat API")

@app.get("/health")
def health():
    return {"status": "ok"}
```

Run it with `uvicorn main:app --reload`.

## Input Validation with Pydantic

Never trust raw input. Define a request model that enforces constraints:

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1, le=4096)

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int
```

If a client sends an empty prompt or a temperature of 5, FastAPI returns a `422` with a clear message — before any expensive model call.

## A Basic Chat Endpoint

```python
from openai import OpenAI
client = OpenAI()

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": req.prompt}],
        temperature=req.temperature,
        max_tokens=req.max_tokens,
    )
    choice = completion.choices[0].message.content
    return ChatResponse(reply=choice, tokens_used=completion.usage.total_tokens)
```

## Streaming Responses

Users expect ChatGPT-style streaming. Use `StreamingResponse` with a generator that yields chunks as they arrive. Server-Sent Events (SSE) is a simple, browser-friendly format.

```python
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    def event_generator():
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": req.prompt}],
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield f"data: {delta}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

Key points: set `media_type="text/event-stream"`, prefix lines with `data: `, and signal completion with a sentinel like `[DONE]`.

## Error Handling

Wrap provider calls and translate failures into meaningful HTTP responses. Avoid leaking stack traces or API keys.

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal_error", "detail": "Something went wrong."})

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        ...
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Upstream model timed out")
    except Exception:
        raise HTTPException(status_code=502, detail="Model provider error")
```

Use the right status codes: `422` validation, `429` rate limited, `502/504` upstream issues, `500` for unexpected bugs.

## Security and Reliability

- **Secrets**: load API keys from environment variables (e.g. `os.environ["OPENAI_API_KEY"]`), never hardcode.
- **CORS**: add `CORSMiddleware` and restrict `allow_origins` to your known frontends.
- **Timeouts**: set client timeouts so a hanging provider doesn't pin your workers.
- **Rate limiting**: protect against abuse and runaway costs (e.g. `slowapi`).
- **Auth**: require an API key header or JWT for non-public endpoints.

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

## Deployment Notes

Run in production with multiple workers behind a process manager: `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4` or use Gunicorn with Uvicorn workers. Containerize with Docker, set env vars, and add a `/health` probe for orchestration.
