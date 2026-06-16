---
course: dami-ai-career
title: Application architecture
month: 4
monthTitle: Portfolio Projects
lesson: 5
summary: Design how the pieces of an AI app fit together — frontend, backend, model API, and data — so
  it stays clean and scalable.
objectives:
- Explain what application architecture is and why it matters for portfolio projects
- 'Identify the core layers: frontend, backend, model/API, and data store'
- Separate concerns so each layer has one clear responsibility
- Understand the request flow from user click to model response and back
- Keep secrets like API keys out of the frontend and in environment variables
- Choose between monolith and simple service split for a small project
- Draw a clear architecture diagram to include in your portfolio
video: m4-l05-architecture.mp4
quiz:
- q: In a typical AI web app, where should your ANTHROPIC_API_KEY live?
  options:
  - In the frontend JavaScript
  - In the backend, read from an environment variable
  - Hard-coded in the HTML
  - In the GitHub README
  answer: 1
  why: The key must stay server-side in an env var. If it is in the frontend, anyone can read it from
    the browser and steal it.
- q: What is the main benefit of 'separation of concerns'?
  options:
  - It makes the app run faster
  - Each part has one job, so it is easier to change and test
  - It removes the need for a database
  - It hides the code from users
  answer: 1
  why: When each layer does one thing, you can change or fix one part without breaking the others, and
    you can test them independently.
- q: Which layer is responsible for calling the Claude Messages API and shaping the prompt?
  options:
  - The frontend
  - The backend
  - The database
  - The browser cache
  answer: 1
  why: The backend holds the secret key and business logic, so it calls the model API. The frontend just
    sends user input and shows results.
- q: In one sentence, what is application architecture?
  answer: The high-level design of how an application's parts (frontend, backend, model, data) are split
    up and connected.
  why: Architecture is the shape of the system — which components exist and how they talk — not the line-by-line
    code inside them.
- q: Why might you start a small portfolio project as a monolith rather than many microservices?
  answer: A monolith is simpler to build, deploy, and reason about; microservices add overhead you rarely
    need at small scale.
  why: For a one-person portfolio project, a single deployable app is easier and faster; you split into
    services only when there is a real reason.
- q: What does the backend act as between the user and the model API?
  answer: A trusted middle layer (a proxy/gateway) that holds secrets, validates input, and forwards requests.
  why: The backend shields the API key, controls what gets sent, and lets you add logging, limits, and
    error handling in one place.
resources:
- label: Mozilla MDN — Client-Server overview
  url: https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview
- label: The Twelve-Factor App (config in the environment)
  url: https://12factor.net/config
- label: Anthropic — Messages API reference
  url: https://docs.anthropic.com/en/api/messages
- label: Martin Fowler — MonolithFirst
  url: https://martinfowler.com/bliki/MonolithFirst.html
---

## What is application architecture?

**Application architecture** is the high-level design of how the parts of your app fit together. Not the line-by-line code — the *shape*. Which components exist, what each one does, and how they talk to each other.

For a portfolio AI app, getting this right means a recruiter can read your diagram and instantly understand your thinking. That clarity is worth as much as the code itself.

## The core layers

Most AI web apps have four layers:

- **Frontend** — what the user sees and clicks (the browser).
- **Backend** — your server code; holds secrets and business logic.
- **Model / API** — the Claude Messages API that does the A I work.
- **Data store** — a database or files where you keep state.

The golden rule is **separation of concerns**: each layer has *one* job. That makes the system easy to change, test, and explain.

## The request flow

Follow a single click through the system. The user types a question and presses send. The frontend sends that text to your backend. The backend validates it, attaches the secret key, and calls the model. The model replies, the backend cleans it up, and the frontend shows it.

The frontend never talks to the model directly. The backend is a **trusted middle layer**.

```python
# backend: app.py (Flask)
import os
from flask import Flask, request, jsonify
from anthropic import Anthropic

app = Flask(__name__)
client = Anthropic()  # reads ANTHROPIC_API_KEY from env

@app.post("/ask")
def ask():
    user_text = request.json["question"]
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": user_text}],
    )
    return jsonify({"answer": msg.content[0].text})
```

## Keep secrets out of the frontend

Your `ANTHROPIC_API_KEY` is like a password. If it sits in browser code, anyone can open dev tools and steal it. Keep it on the **server**, loaded from an environment variable — never committed to Git.

```bash
# set the key in your shell or a .env file (gitignored)
export ANTHROPIC_API_KEY="sk-ant-..."

# .gitignore
.env
```

## Monolith vs services

For a small portfolio project, start with a **monolith** — one deployable app containing frontend and backend. It is simpler to build, deploy, and reason about. Split into separate services only when there is a real reason: different scaling needs, separate teams, or independent deploys. Do not add microservices just to look advanced.

## Your task

Draw the architecture diagram for one of your projects: boxes for each layer, arrows for the request flow, and a note on where the secret key lives. Add it to your README.
