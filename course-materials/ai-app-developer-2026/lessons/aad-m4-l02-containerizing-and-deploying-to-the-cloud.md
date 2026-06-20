---
course: ai-app-developer-2026
title: Containerizing and Deploying to the Cloud
month: 4
monthTitle: Deployment and Capstone Project
lesson: 2
summary: Learn to package an LLM-powered application into a Docker container and deploy it to a cloud
  platform, handling environment configuration and secrets securely along the way.
objectives:
- Write an efficient, production-ready Dockerfile for an LLM-powered app
- Manage environment variables and secrets without baking them into images
- Build, run, and test containers locally before deployment
- Deploy a containerized app to a managed cloud platform
- Apply security and cost best practices for production LLM apps
video: aad-m4-l02-containerizing-and-deploying-to-the-cloud.mp4
quiz:
- q: Why should you copy requirements.txt and install dependencies before copying the rest of your source
    code in a Dockerfile?
  options:
  - It makes the final image larger but more secure
  - It allows Docker to cache the dependency layer so code changes don't trigger reinstalls
  - It is required syntax for Python images
  - It encrypts the dependencies
  answer: 1
  why: Docker caches layers; installing dependencies before copying code means changing your source doesn't
    invalidate the (slow) dependency-install layer, speeding rebuilds.
- q: Which is the WORST way to handle an API key in a container?
  options:
  - Inject it via the cloud platform's secret manager at runtime
  - Pass it with docker run --env-file .env locally
  - Bake it into an image layer or pass it as a build ARG
  - Read it from os.environ at runtime
  answer: 2
  why: Secrets baked into image layers or passed as ARG persist in the image history and can be extracted,
    even if 'removed' later.
- q: Why is running the container as a non-root user recommended?
  options:
  - It makes the image build faster
  - It reduces the security blast radius if the app is compromised
  - It is required by all cloud platforms
  - It enables layer caching
  answer: 1
  why: Running as non-root limits what an attacker can do if they exploit the application, improving container
    security.
- q: What is the purpose of a /health endpoint in a deployed container?
  options:
  - To store secrets
  - To let the cloud platform verify the app is alive and ready
  - To increase request timeout
  - To cache LLM responses
  answer: 1
  why: Platforms use health checks to determine if a container instance is healthy and route traffic accordingly.
- q: Name one reason LLM apps often need higher request timeouts in production than typical web apps.
  answer: LLM model inference/API calls are slow and can take many seconds, so default short timeouts
    would cut off responses.
  why: LLM completions can take several seconds or more, so request timeouts must be raised to avoid prematurely
    terminating valid requests.
- q: What file should you add to keep secrets and clutter out of the Docker build context?
  answer: .dockerignore
  why: A .dockerignore excludes files like .env, .git, and __pycache__ from the build context, keeping
    images clean and secrets out.
resources:
- label: Docker official documentation
  url: https://docs.docker.com/
- label: Dockerfile best practices
  url: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- label: Google Cloud Run — Deploy a container
  url: https://cloud.google.com/run/docs/deploying
- label: 'Twelve-Factor App: Config & Backing Services'
  url: https://12factor.net/config
---

## Why Containerize?

Containers package your application code, runtime, and dependencies into a single portable artifact. For LLM-powered apps this matters because you often have specific Python versions, native libraries, and pinned SDK versions that must behave identically in development and production.

Benefits:
- **Reproducibility** — "works on my machine" disappears.
- **Portability** — run the same image locally, in CI, and in any cloud.
- **Isolation** — dependencies don't collide with the host.
- **Scalability** — cloud platforms scale container replicas easily.

## Anatomy of a Good Dockerfile

A minimal FastAPI LLM app Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run as non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key practices:
- Use a **slim** base image to reduce size and attack surface.
- Copy `requirements.txt` and install **before** copying source so the dependency layer is cached.
- Use `--no-cache-dir` to keep image small.
- Run as a **non-root user** for security.
- Add a `.dockerignore` (exclude `.git`, `.env`, `__pycache__`, `venv`).

## Environment Configuration

Never hardcode config. Read it from environment variables:

```python
import os
API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("MODEL", "gpt-4o-mini")
```

Locally you can use a `.env` file (loaded with `python-dotenv`), but **never commit it** and **never COPY it into the image**. The `.env` is for local dev only.

## Secrets Management

Secrets (API keys, DB passwords) must never be:
- Committed to source control
- Baked into image layers (they persist even if deleted later)
- Passed via `ARG` (visible in image history)

Instead:
- **Local:** pass `--env-file .env` to `docker run`.
- **Cloud:** use the platform's secret manager (e.g., Cloud Run secrets, AWS Secrets Manager, Azure Key Vault, or platform env-var settings injected at runtime).

## Build, Run, and Test Locally

```bash
# Build
docker build -t my-llm-app:latest .

# Run with secrets from a file
docker run -p 8000:8000 --env-file .env my-llm-app:latest

# Test
curl http://localhost:8000/health
```

Always verify the container works locally before pushing to the cloud — it's the fastest feedback loop.

## Deploying to the Cloud

The general flow for a managed container platform (Google Cloud Run as the example):

```bash
# Tag and push to a registry
docker tag my-llm-app gcr.io/my-project/my-llm-app
docker push gcr.io/my-project/my-llm-app

# Deploy
gcloud run deploy my-llm-app \
  --image gcr.io/my-project/my-llm-app \
  --set-secrets OPENAI_API_KEY=openai-key:latest \
  --region us-central1 \
  --allow-unauthenticated
```

Most platforms (Render, Railway, Fly.io, AWS App Runner) follow the same pattern: push image → configure env/secrets → deploy → get a URL.

## Production Considerations

- **Health checks** — expose a `/health` endpoint so the platform knows the app is alive.
- **Scaling & timeouts** — LLM calls are slow; raise request timeouts and set sensible concurrency.
- **Cost control** — set max instances; scale to zero when idle.
- **Observability** — log requests, latencies, and token usage.
- **Image scanning** — scan images for vulnerabilities in CI.
