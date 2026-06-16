---
course: dami-ai-career
title: Deployment platforms
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 1
summary: Take your AI app off your laptop and put it on the internet, choosing the right hosting platform
  for the job.
objectives:
- Explain what deployment means and why localhost is not enough
- Tell apart static hosts, app platforms (PaaS), and serverless functions
- 'Match a platform to a project: Streamlit, FastAPI, or a static front end'
- Configure environment variables and secrets safely on a host
- Pin dependencies with requirements.txt for reproducible deploys
- Read build logs and diagnose a failed deployment
video: m5-l01-deploy-platforms.mp4
quiz:
- q: Why can't you just send a friend your localhost URL to use your app?
  answer: localhost (127.0.0.1) only refers to the machine the request comes from, so it points at their
    computer, not yours; the app must be hosted on a public server with a real domain.
  why: localhost always resolves to the local machine, so a public, reachable host is required for others
    to access your app.
- q: Which platform type runs your code only when a request arrives and scales to zero when idle?
  options:
  - Static host
  - Platform-as-a-Service (PaaS)
  - Serverless functions
  - A dedicated virtual machine
  answer: 2
  why: Serverless functions spin up on demand per request and cost nothing while idle, but have cold starts
    and time limits.
- q: Where should your ANTHROPIC_API_KEY live when deployed?
  options:
  - Hard-coded in app.py
  - In a committed .env file
  - In the platform's secrets / environment variables settings
  - In the README so teammates can find it
  answer: 2
  why: Secrets belong in the host's environment-variable settings, never in code or version control where
    they can leak.
- q: What is the main job of requirements.txt during deployment?
  options:
  - It runs your tests
  - It lists the Python packages the host must install
  - It stores your API keys
  - It defines the app's routes
  answer: 1
  why: The host reads requirements.txt to pip install the exact packages your app needs, making the build
    reproducible.
- q: Name one trade-off of serverless functions compared with an always-on PaaS app.
  answer: 'Cold starts: the first request after idle is slow while the function boots; there are also
    execution time limits unsuited to long-running tasks.'
  why: Serverless saves money at idle but adds latency on cold starts and caps how long a single request
    can run.
- q: A static host like Netlify or GitHub Pages can run your Python FastAPI backend.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Static hosts only serve pre-built files (HTML, CSS, JS); running Python server code needs
    a PaaS or serverless platform.
resources:
- label: Streamlit Community Cloud — Deploy an app
  url: https://docs.streamlit.io/deploy/streamlit-community-cloud
- label: Render — Deploy a FastAPI app (docs)
  url: https://render.com/docs/deploy-fastapi
- label: Hugging Face Spaces — Documentation
  url: https://huggingface.co/docs/hub/spaces
- label: The Twelve-Factor App — III. Config (env vars)
  url: https://12factor.net/config
---

## What deployment really means

**Deployment** is moving your app from your laptop to a server that anyone on the internet can reach. While you build, you run things on `localhost` — address `127.0.0.1` — which always means *this machine*. Send that link to a friend and it points at *their* computer, not yours.

To go public you need a **host**: a machine (or managed service) that is always on, has a public address, and runs your code. Your job is to package the app, tell the host how to start it, and hand over your secrets safely.

## Three kinds of platform

Not every app needs the same host. The three families you'll meet:

- **Static hosts** (Netlify, GitHub Pages, Cloudflare Pages) — serve pre-built files only: HTML, CSS, JavaScript. No Python runs. Great for a portfolio site or a React front end.
- **Platform-as-a-Service / PaaS** (Render, Railway, Fly.io, Streamlit Cloud, Hugging Face Spaces) — you give it code, it builds and runs a long-lived process. Perfect for a FastAPI or Streamlit AI app.
- **Serverless functions** (Vercel Functions, AWS Lambda) — your code runs only when a request arrives, then scales to zero. Cheap at idle, but **cold starts** add latency and there are time limits.

## Pinning dependencies

The host is a fresh machine — none of your packages are installed. A `requirements.txt` lists exactly what to install so the build is reproducible.

```bash
pip freeze > requirements.txt
cat requirements.txt
# anthropic==0.39.0
# fastapi==0.115.0
# uvicorn==0.32.0
```

## Secrets and environment variables

Never hard-code an API key, and never commit a `.env` file. Read keys from the environment, and set the real values in the platform's secrets panel.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Say hello in one line."}],
)
print(msg.content[0].text)
```

## Picking a platform

For this course, **Streamlit Community Cloud** and **Hugging Face Spaces** are the fastest free routes to a live AI demo — connect a GitHub repo and they build it for you. Reach for **Render** when you need a plain FastAPI backend with a public URL. Use a static host only for a front end with no Python.

## Your task

Pick one app you've built. Write its `requirements.txt`, move every secret to an environment variable, push to GitHub, and deploy it to Streamlit Cloud or Hugging Face Spaces. Share the live link.
