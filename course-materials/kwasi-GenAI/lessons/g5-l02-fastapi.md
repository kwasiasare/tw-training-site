---
course: kwasi-GenAI
title: Expose your GenAI work as an API with FastAPI
month: 5
monthTitle: Python for Production Apps
lesson: 2
summary: 'Turn your GenAI scripts into a real web service with FastAPI: define endpoints, type your request
  and response with Pydantic models, and run it with uvicorn.'
objectives:
- Explain why exposing GenAI work as an HTTP API matters for production
- Create a FastAPI app with GET and POST endpoints
- Type request and response bodies with Pydantic models for automatic validation
- Run the app locally with uvicorn and explore the auto-generated docs
- Call a Claude model from inside an endpoint and return a structured response
- Use async endpoints so the server handles many requests concurrently
video: g5-l02-fastapi.mp4
quiz:
- q: What does FastAPI give you automatically when you type your endpoints with Pydantic models?
  options:
  - A database
  - Request validation, JSON serialisation, and interactive API docs
  - A trained model
  - A Dockerfile
  answer: 1
  why: FastAPI uses the Pydantic types on your function to validate incoming JSON, serialise responses,
    and generate interactive OpenAPI docs at /docs — all for free.
- q: Which tool runs a FastAPI app?
  options:
  - pip
  - uvicorn, an ASGI server
  - git
  - venv
  answer: 1
  why: FastAPI is an ASGI framework, so you run it with an ASGI server such as uvicorn, e.g. uvicorn main:app
    --reload.
- q: Why declare a request body as a Pydantic model rather than reading raw JSON?
  options:
  - It is faster to type
  - FastAPI then validates and parses the body for you and rejects bad input with a clear 422 error
  - It encrypts the request
  - It is required to return JSON
  answer: 1
  why: Typing the body as a Pydantic model means FastAPI parses and validates it automatically, returning
    a helpful 422 error if the client sends the wrong shape.
- q: What is the benefit of making an endpoint that calls an LLM an async def endpoint?
  options:
  - It makes the model smarter
  - The server can handle other requests while this one waits on the model, improving throughput
  - It removes the need for uvicorn
  - It caches responses
  answer: 1
  why: An LLM call is I/O-bound; an async endpoint lets the event loop serve other requests during the
    wait instead of blocking a worker.
- q: In one sentence, what does the @app.post("/path") decorator do?
  answer: It registers the function below it as the handler for HTTP POST requests to that URL path on
    your FastAPI app.
  why: The decorator wires a URL and HTTP method to your Python function so FastAPI routes matching requests
    to it.
- q: Where can you try your API in the browser without writing a client?
  answer: At the auto-generated interactive docs, served by default at /docs (Swagger UI), or /redoc.
  why: FastAPI builds an OpenAPI schema from your types and serves Swagger UI at /docs so you can call
    endpoints from the browser.
resources:
- label: FastAPI — Official documentation
  url: https://fastapi.tiangolo.com/
- label: 'FastAPI — Tutorial: First Steps & Request Body'
  url: https://fastapi.tiangolo.com/tutorial/body/
- label: Uvicorn — ASGI web server
  url: https://www.uvicorn.org/
- label: Anthropic — Messages API reference
  url: https://docs.anthropic.com/en/api/messages
- label: FastAPI — Concurrency and async / await
  url: https://fastapi.tiangolo.com/async/
---

## From script to service

A script that summarises a document is useful to you. A **service** that summarises a document is useful to everyone — your colleagues, a web app, another microservice, a CI/CD job. The difference is an **API**: an HTTP endpoint others can call over the network. As a cloud engineer you already deploy and secure services; now you'll build one that wraps your GenAI work.

**FastAPI** is the standard modern way to do this in Python. It's fast, it's typed, and it turns your Pydantic models into automatic validation and documentation. Let's build one.

## Your first endpoint

Install it and write a tiny app.

```bash
pip install "fastapi[standard]" uvicorn
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

The `@app.get("/health")` decorator registers the function as the handler for `GET /health`. Returning a dict is enough — FastAPI serialises it to JSON for you.

## Typed requests and responses

Real endpoints accept input. Declare the shape with a **Pydantic model** and FastAPI validates it automatically: the right fields, the right types, or a clear `422` error back to the caller.

```python
from pydantic import BaseModel

class SummariseRequest(BaseModel):
    text: str
    max_words: int = 50

class SummariseResponse(BaseModel):
    summary: str

@app.post("/summarise", response_model=SummariseResponse)
def summarise(req: SummariseRequest):
    ...
```

By typing `req: SummariseRequest`, FastAPI parses and validates the JSON body. By setting `response_model`, it validates and documents what you send back. You get correctness and documentation for free.

## Running it with uvicorn

FastAPI is an **ASGI** app, so you run it with an ASGI server — **uvicorn**.

```bash
uvicorn main:app --reload
```

Here `main` is the file and `app` is the FastAPI object. `--reload` restarts on code changes during development. Now open `http://127.0.0.1:8000/docs` — FastAPI built interactive **Swagger UI** from your types, so you can call your endpoints from the browser with no client code.

## Calling Claude from an endpoint

Now wire in the model. Because an LLM call waits on the network, make the endpoint **async** so the server can serve other requests during the wait.

```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

@app.post("/summarise", response_model=SummariseResponse)
async def summarise(req: SummariseRequest):
    msg = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=f"Summarise in at most {req.max_words} words.",
        messages=[{"role": "user", "content": req.text}],
    )
    return SummariseResponse(summary=msg.content[0].text)
```

Notice the system prompt is a **top-level** field and the user text is a message — that's the Anthropic Messages API shape. The same service pattern fronts a model on Amazon Bedrock or Azure equally well.

## Why this is production-shaped

You now have a typed, documented, async HTTP service. From here it's familiar cloud territory: put it behind a gateway, add an API key dependency, log requests, and containerise it (next lessons). You've turned a notebook experiment into something deployable.

## Your task

Build a FastAPI app with a `POST /summarise` endpoint that takes `text` and `max_words`, calls a Claude model asynchronously, and returns a typed `SummariseResponse`. Run it with uvicorn and test it from the `/docs` page.
