---
course: dami-ai-career
title: FastAPI for AI apps
month: 4
monthTitle: Portfolio Projects
lesson: 6
summary: Wrap your AI logic in a FastAPI web service so other apps can call your model over HTTP.
objectives:
- Understand what a web API is and why AI apps need one
- Build a FastAPI app with a POST endpoint
- Validate request and response data with Pydantic models
- Call the Anthropic Claude Messages API from an endpoint
- Keep your API key safe in an environment variable
- Run the server locally with uvicorn and test it
- Read auto-generated docs at the /docs page
video: m4-l06-fastapi-ai.mp4
quiz:
- q: What does an API let you do?
  options:
  - Style a web page
  - Let one program call another over HTTP
  - Train a neural network
  - Store files on disk
  answer: 1
  why: An A P I (Application Programming Interface) lets programs talk to each other — here, a client
    sends a request and your server returns a response over HTTP.
- q: Which decorator defines a POST endpoint in FastAPI?
  options:
  - '@app.get'
  - '@app.post'
  - '@app.route'
  - '@app.send'
  answer: 1
  why: '@app.post("/path") registers a function to handle POST requests, which is the right verb for sending
    data like a prompt.'
- q: What is Pydantic used for in FastAPI?
  options:
  - Running the server
  - Validating and parsing request and response data
  - Sending emails
  - Drawing charts
  answer: 1
  why: A Pydantic BaseModel declares the shape of your data; FastAPI uses it to validate incoming JSON
    and document the schema automatically.
- q: Where should your ANTHROPIC_API_KEY live?
  answer: In an environment variable, not hard-coded in the source.
  why: Hard-coding secrets risks leaking them in Git. The Anthropic client reads ANTHROPIC_API_KEY from
    the environment by default.
- q: What command runs a FastAPI app named app in main.py during development?
  answer: uvicorn main:app --reload
  why: Uvicorn is the A S G I server; main:app points to the app object in main.py, and --reload restarts
    on code changes.
- q: What URL shows FastAPI's auto-generated interactive docs?
  options:
  - /api
  - /docs
  - /help
  - /swagger.json
  answer: 1
  why: FastAPI serves interactive Swagger U I at /docs out of the box, generated from your Pydantic models
    and endpoints.
resources:
- label: FastAPI — official documentation
  url: https://fastapi.tiangolo.com/
- label: FastAPI Tutorial — First Steps
  url: https://fastapi.tiangolo.com/tutorial/first-steps/
- label: Anthropic API — Messages reference
  url: https://docs.anthropic.com/en/api/messages
- label: Pydantic — official documentation
  url: https://docs.pydantic.dev/
---

## Why AI apps need an API

You have working A I logic — a function that takes a prompt and returns a Claude response. But a function only runs inside one Python process. To let a website, a mobile app, or a teammate use it, you expose it as a **web API**: a server that listens for HTTP requests and returns answers.

**FastAPI** is a modern Python framework that makes this fast to build, automatically validates your data, and generates interactive docs for free.

## Your first endpoint

An **endpoint** is a URL plus an HTTP verb that runs a function. For sending data like a prompt we use **POST**. The `@app.post` decorator wires a path to a handler.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

Run it locally with uvicorn, the A S G I server:

```bash
pip install fastapi uvicorn anthropic
uvicorn main:app --reload
```

## Validating data with Pydantic

Never trust raw input. A **Pydantic** `BaseModel` declares exactly what fields you expect and their types. FastAPI parses the incoming JSON into that model, rejects bad requests with a clear error, and documents the schema automatically.

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    reply: str
```

## Calling Claude from an endpoint

Inside the handler, create an Anthropic client and call the **Messages API**. The client reads `ANTHROPIC_API_KEY` from the environment — keep keys out of your code.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": req.prompt}],
    )
    return ChatResponse(reply=msg.content[0].text)
```

## Testing and docs

With the server running, open `http://127.0.0.1:8000/docs`. FastAPI generates an interactive Swagger page from your models — you can send a real request from the browser. Set your key first:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## Your task

Build a small FastAPI service with a `/chat` POST endpoint that calls Claude, validate the request with a Pydantic model, and test it from the `/docs` page.
