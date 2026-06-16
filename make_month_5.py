# -*- coding: utf-8 -*-
"""Month 5 Study Pack: Polish, Deploy, Go Public."""
import os
from doc_helpers import (new_doc, title_block, h1, h2, h3, para, lead, bullet,
                         numbered, code_block, callout, table_from_rows, quiz,
                         page_break, NAVY, ACCENT, GREY, GREEN, AMBER, RED)

OUT = os.path.dirname(os.path.abspath(__file__))
doc = new_doc()

# ----------------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------------
title_block(doc,
    'Month 5 - Polish, Deploy, Go Public',
    'Study Pack: ship your Month 4 projects, make them credible, and put your name on them',
    'Maths graduate + L1 support -> AI Application Developer  |  ~30+ hrs/week  |  Months 1-4 complete')

# ----------------------------------------------------------------------------
# Learning objectives
# ----------------------------------------------------------------------------
h1(doc, 'Learning objectives')
para(doc, 'By the end of Month 5 you will have turned the projects you built in Month 4 from '
          '"runs on my laptop" into "anyone can click a link and try it". You move from being a '
          'person who can build to a person who can ship and be seen. Concretely, you will be able to:')
bullet(doc, 'Choose the right deployment platform (Render, Railway, Hugging Face Spaces, or Azure) for a given project and explain the trade-offs.')
bullet(doc, 'Write a working Dockerfile for a Python web app and understand the difference between an image and a container.')
bullet(doc, 'Build a CI/CD pipeline in GitHub Actions that runs your tests on every push and deploys on merge to main.')
bullet(doc, 'Manage configuration and secrets safely in production using environment variables and secret managers, and never commit a key again.')
bullet(doc, 'Add structured logging and basic observability so you can answer "what happened and why" when something breaks.')
bullet(doc, 'Evaluate and monitor an LLM app in production: log prompts/outputs, capture user feedback, and watch for drift.')
bullet(doc, 'Reduce cost and latency with caching, model selection, batching, and prompt trimming.')
bullet(doc, 'Write a technical blog post and a portfolio README that make a hiring manager want to talk to you.')
bullet(doc, 'Rewrite your CV and LinkedIn around the narrative "maths graduate + support engineer building AI applications".')
bullet(doc, 'Publish your work publicly: a live demo, a containerised repo, a portfolio site, and 2-3 posts.')

callout(doc, 'Mindset', 'A deployed, documented, slightly-imperfect project beats a perfect one nobody '
        'can see. This month is about visibility and credibility, not new algorithms.')
page_break(doc)

# ============================================================================
# TOPIC 1 - Deployment platforms
# ============================================================================
h1(doc, '1. Deployment platforms: Render, Railway, Hugging Face Spaces, Azure')

para(doc, 'A web app on your laptop is only reachable from your laptop. "Deploying" means putting your '
          'code on a computer that is always on, connected to the internet, and reachable at a URL. From '
          'first principles, every platform has to do the same handful of jobs: take your code, install '
          'its dependencies, start your process, give it a public address (and HTTPS), keep it running, '
          'and restart it if it crashes. The platforms below differ mainly in how much of that they do '
          'for you, how much they cost, and what kind of app they are optimised for.')

para(doc, 'There are two broad models. A "Platform as a Service" (PaaS) like Render or Railway takes your '
          'Git repo, detects that it is a Python app, builds it, and runs it - you mostly just push code. '
          'An "Infrastructure as a Service" / cloud platform like Azure gives you more primitives '
          '(app services, container apps, virtual machines, managed databases, networking) and more '
          'control, at the cost of more setup. Hugging Face Spaces is a special case: it is purpose-built '
          'for hosting ML demos (Gradio, Streamlit, or Docker) and is the fastest way to get a model demo '
          'in front of people.')

h3(doc, 'When to use each')
para(doc, 'Render - a clean, modern Heroku replacement. Connect a GitHub repo, it auto-deploys on push. '
          'Great for FastAPI/Flask backends and Streamlit apps. Has a free tier (which sleeps after '
          'inactivity), managed Postgres, background workers, and cron jobs. Good default for "I built a '
          'web API or app and want a real URL".')
para(doc, 'Railway - similar developer experience to Render, very fast to set up, generous starter usage, '
          'nice for hooking up a database and a service together. Good when you want minimal config and a '
          'quick live link. Pricing is usage-based, so watch a busy app.')
para(doc, 'Hugging Face Spaces - the home turf for ML/LLM demos. Pick Gradio or Streamlit and you get a '
          'shareable demo with almost no DevOps. It is where AI people look, so a Space doubles as '
          'portfolio visibility. Free CPU tier; paid GPU tiers if you host your own model. Use it for '
          'the public-facing demo of an LLM project.')
para(doc, 'Azure - you already have some familiarity, and it is what many UK employers use. Azure App '
          'Service or Azure Container Apps will host a FastAPI app or a Docker container with proper '
          'custom domains, scaling, Key Vault for secrets, and Application Insights for monitoring. Use '
          'Azure when you want to demonstrate "enterprise-credible" cloud skills, or when a project needs '
          'managed identity, private networking, or to sit next to other Azure resources. It is more '
          'setup than Render/Railway, but naming Azure on your CV resonates with support-to-cloud hiring.')

callout(doc, 'Rule of thumb', 'LLM demo for people to play with -> Hugging Face Spaces. A real backend '
        'API or full app -> Render or Railway. Show employer-grade cloud skills -> Azure Container Apps '
        'or App Service. You do not need all four; deploy at least one project on a PaaS and one on Azure.', color=GREEN)

h3(doc, 'A minimal Render service config (render.yaml)')
code_block(doc,
'''# render.yaml - infrastructure-as-code for Render
# Commit this at the repo root; Render reads it on deploy.
services:
  - type: web
    name: ticket-assistant
    runtime: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
      - key: OPENAI_API_KEY
        sync: false          # set this in the Render dashboard, NOT in the file
    healthCheckPath: /healthz''')

para(doc, 'Two details matter on every PaaS. First, you must bind to the host 0.0.0.0 and the port the '
          'platform gives you (here the $PORT environment variable), not localhost:8000 - the platform '
          'decides the port. Second, secrets like API keys are set in the dashboard or as "sync: false" '
          'env vars, never written into the committed file.')

callout(doc, 'Common mistakes', 'Hard-coding host="127.0.0.1" or a fixed port so the platform cannot '
        'route traffic. Forgetting requirements.txt so the build has nothing to install. Putting secrets '
        'in render.yaml or app code. Assuming a free tier is always-on - free Render/Spaces instances '
        'sleep and cold-start, so add a health check and warn demo viewers it may take ~30s to wake.', color=RED)

quiz(doc, [
    {'q': 'You built a Gradio demo of your RAG app and want AI recruiters to try it with zero DevOps. Best platform?',
     'options': ['A bare virtual machine you SSH into', 'Hugging Face Spaces', 'A Kubernetes cluster', 'Your laptop with ngrok'],
     'answer': 'B - Hugging Face Spaces', 'why': 'Spaces is purpose-built for Gradio/Streamlit ML demos and is where the AI community already looks.'},
    {'q': 'On a PaaS, why must you bind your server to host 0.0.0.0 and to $PORT?',
     'answer': 'Short answer: the platform routes external traffic to your container on a port it assigns (exposed as $PORT) and across all interfaces; binding to 127.0.0.1 or a fixed port means the router cannot reach your process.',
     'why': 'localhost is only reachable from inside the container; the platform picks the port.'},
    {'q': 'True or False: it is fine to put your OPENAI_API_KEY directly in render.yaml because the repo is private.',
     'answer': 'False', 'why': 'Private repos get cloned, forked, made public, or leaked. Keys belong in dashboard secrets / env vars, never in committed files.'},
    {'q': 'Which platform would you choose to demonstrate enterprise-credible cloud skills with Key Vault and managed identity?',
     'options': ['Railway', 'Hugging Face Spaces', 'Azure (App Service / Container Apps)', 'GitHub Pages'],
     'answer': 'C - Azure', 'why': 'Azure offers Key Vault, managed identity, App Insights and is common in UK enterprise; it signals cloud maturity.'},
    {'q': 'Your free-tier app takes 30 seconds to respond the first time someone visits after a quiet period. Why?',
     'answer': 'Short answer: cold start - free tiers spin the instance down when idle and must boot it back up on the next request.',
     'why': 'Free Render/Spaces dynos sleep to save resources; the first request pays the wake-up cost.'},
    {'q': 'Which is the single best "default" choice for hosting a FastAPI backend with a managed Postgres database, with auto-deploy on git push?',
     'options': ['GitHub Pages', 'Render', 'A static S3 bucket', 'Hugging Face Spaces'],
     'answer': 'B - Render', 'why': 'Render auto-deploys from GitHub, runs web services + workers, and offers managed Postgres. Pages/S3 are static only; Spaces is for ML demos.'},
], title='Topic 1 Quiz - Deployment platforms')
page_break(doc)

# ============================================================================
# TOPIC 2 - Docker basics
# ============================================================================
h1(doc, '2. Docker basics: images, containers, and a Python Dockerfile')

para(doc, 'The oldest problem in software is "it works on my machine". Docker solves it by packaging your '
          'app together with everything it needs to run - the exact Python version, the libraries, the '
          'system packages, the files - into a single portable unit. From first principles, Docker uses '
          'features of the Linux kernel to give a process its own isolated view of the filesystem, '
          'network, and process tree, so it behaves the same on your laptop, a colleague\'s machine, and '
          'a cloud server.')

para(doc, 'Two words you must keep straight. An image is a read-only, layered blueprint: a snapshot of a '
          'filesystem plus the command to run. A container is a running (or stopped) instance of an '
          'image - the live process. The analogy: an image is like a class, a container is like an object '
          'created from it; or an image is a recipe and a container is the cooked meal. You build an image '
          'once and can run many containers from it.')

para(doc, 'A Dockerfile is the plain-text recipe for building an image. Each instruction (FROM, COPY, RUN, '
          'CMD) creates a cached layer. Docker caches layers and only rebuilds from the first one that '
          'changed, which is why we copy and install requirements.txt before copying the rest of the code: '
          'your dependencies rarely change, so that expensive layer stays cached while you iterate on code.')

h3(doc, 'A simple, correct Dockerfile for a Python (FastAPI) app')
code_block(doc,
'''# Dockerfile - builds an image for a FastAPI app
FROM python:3.11-slim

# Don't write .pyc files; flush stdout/stderr immediately (good for logs)
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy deps first so this layer is cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code
COPY . .

# Run as a non-root user (security best practice)
RUN useradd --create-home appuser
USER appuser

# Document the port the app listens on
EXPOSE 8000

# Start the server, binding to all interfaces
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]''')

para(doc, 'You would also add a .dockerignore file so junk does not bloat the image or leak in:')
code_block(doc,
'''# .dockerignore
__pycache__/
*.pyc
.venv/
.env
.git/
tests/
*.md''')

h3(doc, 'The everyday commands')
code_block(doc,
'''# Build an image and tag it
docker build -t ticket-assistant:latest .

# Run a container from that image, mapping host port 8000 -> container 8000,
# and passing an env file with secrets (never baked into the image)
docker run -p 8000:8000 --env-file .env ticket-assistant:latest

# See running containers / images
docker ps
docker images

# Stop and remove
docker stop <container_id>''')

callout(doc, 'Common mistakes', 'Copying all code before installing deps, so every code change busts the '
        'pip cache and rebuilds are slow. Baking secrets or a .env into the image with COPY . . (they '
        'live in the layers forever - use --env-file or runtime secrets, and a .dockerignore). Using a '
        'full "python:3.11" base when "slim" is far smaller. Forgetting --host 0.0.0.0 so the app is '
        'unreachable from outside the container. Running as root by default.', color=RED)

quiz(doc, [
    {'q': 'What is the difference between a Docker image and a Docker container?',
     'answer': 'Short answer: an image is the read-only, layered blueprint (filesystem snapshot + start command); a container is a running/stopped instance created from an image. One image, many containers.',
     'why': 'Image = class/recipe; container = object/cooked meal.'},
    {'q': 'Why do we COPY requirements.txt and run pip install BEFORE copying the rest of the code?',
     'options': ['It is alphabetical', 'To use Docker layer caching so deps are not reinstalled on every code change', 'pip requires it', 'To make the image bigger'],
     'answer': 'B - layer caching', 'why': 'Dependencies change rarely; isolating them in an earlier layer keeps that slow layer cached while code iterates.'},
    {'q': 'True or False: putting your .env in the image via "COPY . ." is a safe way to ship secrets.',
     'answer': 'False', 'why': 'Anything copied into a layer is recoverable from the image forever. Use --env-file at run time or a secret manager, and .dockerignore the .env.'},
    {'q': 'Which base image is the better default for a small Python web service?',
     'options': ['python:3.11', 'python:3.11-slim', 'ubuntu:latest then install python', 'scratch'],
     'answer': 'B - python:3.11-slim', 'why': 'slim is much smaller than the full image but still has pip; ubuntu/scratch need extra setup.'},
    {'q': 'What does "docker run -p 8000:8000" do?',
     'answer': 'Short answer: maps host port 8000 to container port 8000 so traffic to localhost:8000 on the host reaches the app listening inside the container.',
     'why': 'The left number is the host port, the right is the container port.'},
    {'q': 'Why run the container as a non-root user (USER appuser)?',
     'answer': 'Short answer: defence in depth - if the app is compromised, a non-root process limits what an attacker can do inside (and on the host).',
     'why': 'Least privilege; many platforms also block or warn on root containers.'},
    {'q': 'What is the purpose of a .dockerignore file?',
     'options': ['It lists images to delete', 'It excludes files (e.g. .git, .env, .venv) from the build context', 'It is required by Kubernetes', 'It sets environment variables'],
     'answer': 'B', 'why': 'It keeps the image small and prevents secrets/junk from being copied into layers.'},
], title='Topic 2 Quiz - Docker basics')
page_break(doc)

# ============================================================================
# TOPIC 3 - CI/CD with GitHub Actions
# ============================================================================
h1(doc, '3. CI/CD intro with GitHub Actions')

para(doc, 'CI/CD stands for Continuous Integration and Continuous Deployment (or Delivery). Continuous '
          'Integration means: every time anyone pushes code, an automated system checks it out, installs '
          'it, and runs the tests and linters - so you find breakage in minutes, not after release. '
          'Continuous Deployment means: when those checks pass on the main branch, the system '
          'automatically ships the new version. The point is to remove the manual, error-prone steps '
          'between "I wrote code" and "it is live and verified".')

para(doc, 'GitHub Actions is GitHub\'s built-in CI/CD. You describe a workflow in a YAML file under '
          '.github/workflows/. A workflow has triggers (on: push, pull_request), one or more jobs, and '
          'each job runs steps on a fresh virtual machine ("runner"). Steps either run shell commands or '
          'use pre-built "actions" (reusable building blocks, e.g. actions/checkout to clone your repo). '
          'This fits your support background perfectly: it is automation and reproducibility, the same '
          'instincts as a good runbook.')

h3(doc, 'A basic test + deploy workflow')
code_block(doc,
'''# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest ruff

      - name: Lint
        run: ruff check .

      - name: Run tests
        run: pytest -q

  deploy:
    # Only deploy after tests pass, and only on main
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render deploy
        run: curl -fsS -X POST "$RENDER_DEPLOY_HOOK"
        env:
          RENDER_DEPLOY_HOOK: ${{ secrets.RENDER_DEPLOY_HOOK }}''')

para(doc, 'Read the structure: the test job runs on every push and PR. The deploy job declares '
          '"needs: test", so it only starts if tests passed, and "if: github.ref == refs/heads/main" so '
          'it only runs on the main branch - not on PRs or the dev branch. The deploy uses a secret '
          '(secrets.RENDER_DEPLOY_HOOK) injected by GitHub, so the URL is never in the code. Many '
          'platforms (Render, Railway, Azure) provide a deploy hook URL or a dedicated deploy action.')

callout(doc, 'Common mistakes', 'Putting the workflow file anywhere other than .github/workflows/ (it '
        'must be exactly there). Hard-coding tokens instead of using ${{ secrets.NAME }}. Letting deploy '
        'run without "needs: test", so broken code ships. Running deploy on every branch instead of '
        'gating with an "if" on main. Forgetting to install pytest/ruff so the steps fail with command '
        'not found. YAML indentation errors - it is whitespace-sensitive.', color=RED)

quiz(doc, [
    {'q': 'What do the "CI" and "CD" in CI/CD stand for, in one line each?',
     'answer': 'CI = Continuous Integration: auto-run tests/linters on every push. CD = Continuous Deployment/Delivery: auto-ship the version once checks pass.',
     'why': 'CI catches breakage early; CD removes manual release steps.'},
    {'q': 'Where must a GitHub Actions workflow file live?',
     'options': ['Repo root', '.github/workflows/', 'workflows/', 'src/ci/'],
     'answer': 'B - .github/workflows/', 'why': 'GitHub only discovers workflow YAML files in that exact directory.'},
    {'q': 'In the workflow, what does "needs: test" on the deploy job guarantee?',
     'answer': 'Short answer: the deploy job will not start unless the test job completed successfully, so broken code is not deployed.',
     'why': 'It creates a dependency/ordering and a pass-gate between jobs.'},
    {'q': 'How should a deploy token be provided to a workflow step?',
     'options': ['Hard-coded in the YAML', 'In a public README', 'Via ${{ secrets.NAME }} configured in repo settings', 'As a commit message'],
     'answer': 'C - via secrets', 'why': 'GitHub Encrypted Secrets inject values at run time and keep them out of source control and logs.'},
    {'q': 'True or False: actions/checkout@v4 is needed because the runner starts as a clean machine without your code.',
     'answer': 'True', 'why': 'Each job runs on a fresh runner; checkout clones your repository onto it.'},
    {'q': 'Why add "if: github.ref == \'refs/heads/main\'" to the deploy job?',
     'answer': 'Short answer: so deployment only happens for the main branch, not for pull requests or feature/dev branches.',
     'why': 'You want to test everywhere but ship only from your release branch.'},
    {'q': 'A YAML workflow fails to even start with a parse error. Most likely cause?',
     'options': ['Too many tests', 'Incorrect indentation/whitespace in the YAML', 'The repo is private', 'Python is too new'],
     'answer': 'B - indentation', 'why': 'YAML is whitespace-sensitive; mixing tabs/spaces or wrong nesting breaks parsing.'},
], title='Topic 3 Quiz - CI/CD with GitHub Actions')
page_break(doc)

# ============================================================================
# TOPIC 4 - Environment & secrets in production
# ============================================================================
h1(doc, '4. Environment & secrets in production')

para(doc, 'Configuration is everything that changes between where your app runs: the database URL, the API '
          'keys, feature flags, the log level. The foundational principle (from the "Twelve-Factor App") '
          'is: keep configuration in the environment, not in the code. Code is the same everywhere; '
          'configuration differs between your laptop, a test server, and production. Mixing them means '
          'you cannot move code between environments without editing it, and it is how secrets end up in '
          'Git history.')

para(doc, 'A secret is configuration that is also sensitive: API keys, database passwords, tokens. The '
          'cardinal rule is never commit a secret to version control. Git remembers everything; once a '
          'key is pushed, treat it as compromised even after you delete it, because it lives in history '
          'and in anyone\'s clone. Locally you keep secrets in a .env file that is listed in .gitignore. '
          'In production you provide them as environment variables or, better, through a secret manager '
          'like Azure Key Vault, AWS Secrets Manager, or the platform\'s built-in secrets store.')

h3(doc, 'Loading config safely in Python')
code_block(doc,
'''# config.py - read configuration from the environment, fail loudly if missing
import os
from dotenv import load_dotenv   # python-dotenv

load_dotenv()  # loads a local .env in dev; no-op in prod where vars are set already

class Settings:
    def __init__(self):
        # Required secret - crash early with a clear message if absent
        self.openai_api_key = self._require("OPENAI_API_KEY")
        # Optional with a sensible default
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.environment = os.getenv("ENVIRONMENT", "development")

    @staticmethod
    def _require(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Missing required env var: {name}")
        return value

settings = Settings()''')

para(doc, 'And the two files that make this safe in a repo:')
code_block(doc,
'''# .gitignore  ->  make sure real secrets never get committed
.env
*.env
.venv/

# .env.example  ->  COMMIT THIS (no real values) so others know what to set
OPENAI_API_KEY=
LOG_LEVEL=INFO
ENVIRONMENT=development''')

para(doc, 'In Azure, instead of plain env vars you can store the key in Key Vault and let the app read it '
          'via a managed identity - so no human ever handles the secret and there is nothing to leak. '
          'That is the kind of detail that signals real production maturity in an interview.')

callout(doc, 'Common mistakes', 'Committing a real .env (add it to .gitignore on day one). Printing or '
        'logging secrets - they end up in log files and CI output. Reusing the same key across dev and '
        'prod. Not rotating a key after it leaks (deleting the commit is not enough - the key is already '
        'exposed; revoke and reissue it). Forgetting a .env.example so teammates cannot reproduce config.', color=RED)

quiz(doc, [
    {'q': 'State the core twelve-factor rule about configuration.',
     'answer': 'Short answer: store configuration in the environment, not in the code, so the same code runs unchanged across dev/test/prod.',
     'why': 'Config differs per environment; code should not.'},
    {'q': 'You accidentally pushed an API key to GitHub, then deleted it in the next commit. Is the key safe?',
     'options': ['Yes, deleting the commit removes it', 'No - it is in history/clones and must be revoked and reissued', 'Yes if the repo is private', 'Only if no one starred the repo'],
     'answer': 'B - revoke and reissue', 'why': 'Git history retains the key and clones/forks may have it; the only safe fix is to rotate the key at the provider.'},
    {'q': 'Which file should be committed, and which must NOT be?',
     'answer': 'Commit .env.example (placeholder keys, no real values). Never commit .env (real secrets); add it to .gitignore.',
     'why': '.env.example documents required config; .env holds the actual secrets.'},
    {'q': 'In production on Azure, what is a stronger pattern than plain environment variables for secrets?',
     'options': ['A text file on the server', 'Azure Key Vault accessed via managed identity', 'Hard-coding in config.py', 'A public Gist'],
     'answer': 'B - Key Vault + managed identity', 'why': 'Secrets are centralised, access-controlled, auditable, and no human handles the raw value.'},
    {'q': 'True or False: it is fine to log the value of OPENAI_API_KEY at startup to confirm it loaded.',
     'answer': 'False', 'why': 'Logs are stored, shipped, and viewed widely; log only that a key is present/absent, never the value.'},
    {'q': 'Why does the example config raise an error if a required env var is missing, rather than using None?',
     'answer': 'Short answer: fail fast with a clear message at startup instead of a confusing crash deep in a request later.',
     'why': 'Loud, early failure is easier to diagnose than a silent missing key.'},
], title='Topic 4 Quiz - Environment & secrets')
page_break(doc)

# ============================================================================
# TOPIC 5 - Observability & logging
# ============================================================================
h1(doc, '5. Observability & logging')

para(doc, 'When your app runs on a server you cannot see, logs are your eyes. Observability is the broader '
          'idea: can you understand what your system is doing, and why, from the outputs it emits? It '
          'rests on three pillars - logs (discrete events), metrics (numbers over time, e.g. requests '
          'per second, error rate, p95 latency), and traces (the path of one request across components). '
          'For your stage, getting logging right is 80% of the value.')

para(doc, 'The key upgrade from beginner logging is structured logging. Instead of free-text "User did a '
          'thing", you emit machine-readable records (usually JSON) with consistent fields: a timestamp, '
          'a level, a message, a request id, and any relevant context. Structured logs can be searched, '
          'filtered, and aggregated ("show me all ERROR logs for request abc-123" or "count errors per '
          'endpoint"). Always include a correlation/request id so you can follow a single user action '
          'across many log lines. And never use print() in production - use the logging module so you '
          'control levels and destinations.')

h3(doc, 'Structured logging + request middleware in FastAPI')
code_block(doc,
'''import logging, json, time, uuid
from fastapi import FastAPI, Request

# --- configure a JSON formatter ---
class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if hasattr(record, "request_id"):
            payload["request_id"] = record.request_id
        return json.dumps(payload)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
log = logging.getLogger("app")

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()
    try:
        response = await call_next(request)
    except Exception:
        log.exception("unhandled error", extra={"request_id": request_id})
        raise
    duration_ms = round((time.time() - start) * 1000, 1)
    log.info(
        f"{request.method} {request.url.path} -> {response.status_code} "
        f"in {duration_ms}ms",
        extra={"request_id": request_id},
    )
    response.headers["X-Request-ID"] = request_id
    return response''')

para(doc, 'This logs one structured line per request with method, path, status, latency, and a request id '
          'that is also returned in a response header - so when a user reports an error you can ask for '
          'their X-Request-ID and find exactly their logs. Use levels deliberately: DEBUG for development '
          'detail, INFO for normal events, WARNING for recoverable oddities, ERROR for failures you need '
          'to act on. In the cloud, ship these logs to a platform (Azure Application Insights, or the '
          'platform\'s log stream) so you can search them.')

callout(doc, 'Common mistakes', 'Using print() instead of logging, so you cannot set levels or route '
        'output. Logging unstructured free text that you cannot search or aggregate. Logging secrets or '
        'full user PII/prompts without thought. No request id, so you cannot correlate the lines of one '
        'request. Logging so much at DEBUG in prod that real signals drown (and costs rise). Swallowing '
        'exceptions silently instead of log.exception().', color=RED)

quiz(doc, [
    {'q': 'Name the three pillars of observability.',
     'answer': 'Logs (discrete events), metrics (numbers over time like error rate/latency), and traces (the path of one request across components).',
     'why': 'Together they let you answer what happened, how much/how often, and where.'},
    {'q': 'What is the main advantage of structured (JSON) logs over free-text logs?',
     'options': ['They are shorter', 'They can be searched, filtered, and aggregated by field', 'They are required by Python', 'They use less disk always'],
     'answer': 'B', 'why': 'Consistent fields let log tools query e.g. all ERRORs for one request_id or count errors per endpoint.'},
    {'q': 'Why attach a request_id / correlation id to every log line of a request?',
     'answer': 'Short answer: so you can follow a single user action across many log lines and components, and match a user-reported error to its exact logs.',
     'why': 'It correlates otherwise-scattered events into one story.'},
    {'q': 'Which logging level is appropriate for "a failure I need to act on"?',
     'options': ['DEBUG', 'INFO', 'WARNING', 'ERROR'],
     'answer': 'D - ERROR', 'why': 'ERROR signals a real failure; WARNING is a recoverable oddity, INFO/DEBUG are normal/diagnostic.'},
    {'q': 'True or False: print() is fine for production logging.',
     'answer': 'False', 'why': 'print() gives no levels, no structure, and no control over destinations; use the logging module.'},
    {'q': 'A user reports an error. Your middleware returns an X-Request-ID header. How does that help you?',
     'answer': 'Short answer: ask the user for that ID, then search your structured logs for that request_id to see exactly what happened on their request.',
     'why': 'It turns a vague report into a precise lookup.'},
], title='Topic 5 Quiz - Observability & logging')
page_break(doc)

# ============================================================================
# TOPIC 6 - Production evaluation & monitoring of LLM apps
# ============================================================================
h1(doc, '6. Production evaluation & monitoring of LLM apps')

para(doc, 'LLM apps fail differently from normal software. The code can be perfect while the output is '
          'wrong, unhelpful, off-brand, or hallucinated - and the same input can give different outputs. '
          'So you cannot rely on unit tests alone; you must evaluate the quality of generations and watch '
          'them over time. The loop is: log what went in and out, define what "good" means, measure it, '
          'and capture human feedback to keep improving.')

para(doc, 'Log the right things for every LLM call: the prompt (or a reference to it), the model and '
          'parameters (temperature, version), the output, token counts and cost, latency, and which '
          'retrieved documents were used (for RAG). Be deliberate about privacy - prompts can contain '
          'user data, so redact or hash PII and follow your data policy. These logs let you debug bad '
          'answers, reproduce issues, and build evaluation sets from real traffic.')

para(doc, 'Evaluation has two modes. Offline: a fixed test set of inputs with expected qualities, scored '
          'by exact/semantic match, by rules, or by an "LLM-as-judge" that rates outputs against a '
          'rubric - run this in CI so a prompt change cannot silently regress quality. Online: measure '
          'live behaviour - thumbs up/down feedback, escalation/override rates (very natural from your '
          'support background), latency and cost. Drift is the slow degradation when reality moves away '
          'from what you built for: user questions shift, an upstream model is updated, or your retrieved '
          'documents go stale. You detect drift by tracking metrics over time (feedback score, '
          'refusal/hallucination rate, retrieval relevance) and alerting when they move.')

h3(doc, 'Logging an LLM call and capturing feedback')
code_block(doc,
'''import time, uuid, logging
log = logging.getLogger("llm")

def answer_question(client, question: str, model="gpt-4o-mini"):
    trace_id = str(uuid.uuid4())
    start = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        temperature=0,
    )
    out = resp.choices[0].message.content
    log.info("llm_call", extra={"data": {
        "trace_id": trace_id,
        "model": model,
        "prompt_chars": len(question),     # store length, redact raw PII per policy
        "completion_tokens": resp.usage.completion_tokens,
        "prompt_tokens": resp.usage.prompt_tokens,
        "latency_ms": round((time.time() - start) * 1000, 1),
    }})
    return {"trace_id": trace_id, "answer": out}

def record_feedback(trace_id: str, helpful: bool, comment: str = ""):
    # store to DB/analytics; ties user feedback back to the exact generation
    log.info("llm_feedback", extra={"data": {
        "trace_id": trace_id, "helpful": helpful, "comment": comment,
    }})''')

para(doc, 'The trace_id is the thread that ties a generation to the feedback a user later gives on it. '
          'Aggregate "helpful" over time and per model/prompt version, and you have a live quality '
          'dashboard and an A/B mechanism for prompt changes.')

callout(doc, 'Common mistakes', 'Shipping prompt changes with no eval set, so quality silently regresses. '
        'Logging raw user prompts containing PII with no redaction. Tracking only uptime, not output '
        'quality (the app is "up" but answering badly). No feedback capture, so you have no ground truth. '
        'Ignoring an upstream model version change that shifts behaviour. Using temperature > 0 for '
        'evals you want to be reproducible.', color=RED)

quiz(doc, [
    {'q': 'Why are unit tests alone insufficient for an LLM app?',
     'answer': 'Short answer: the code can be correct while the generated output is wrong/hallucinated/off-brand, and outputs are non-deterministic - so you must evaluate output quality, not just code paths.',
     'why': 'LLM failure modes are in the content, not the control flow.'},
    {'q': 'What is "LLM-as-judge" evaluation?',
     'options': ['Letting users vote', 'Using an LLM to score outputs against a rubric', 'A courtroom simulator', 'A linter for prompts'],
     'answer': 'B', 'why': 'A model rates candidate outputs by a defined rubric, useful for scaling offline eval beyond exact match.'},
    {'q': 'Define "drift" for an LLM app and give one cause.',
     'answer': 'Short answer: drift is the gradual degradation of quality as conditions change vs. what you built for - e.g. user questions shift, the upstream model is updated, or retrieved documents go stale.',
     'why': 'The world moves; static prompts/data fall out of sync.'},
    {'q': 'What is the role of the trace_id in the logging example?',
     'answer': 'Short answer: it links a specific generation to the feedback a user later gives, so you can attribute quality and build eval sets from real traffic.',
     'why': 'It connects request, output, cost, and feedback into one record.'},
    {'q': 'Offline vs online evaluation - one line each.',
     'answer': 'Offline = score a fixed test set (often in CI) before shipping. Online = measure live behaviour (feedback, escalation/override rate, latency, cost) in production.',
     'why': 'Offline catches regressions pre-release; online watches real users.'},
    {'q': 'True or False: monitoring that the app has 99.9% uptime is enough to know it works well.',
     'answer': 'False', 'why': 'An LLM app can be fully "up" while giving poor or wrong answers; you must also monitor output quality and feedback.'},
    {'q': 'Why set temperature=0 for outputs you want to evaluate reproducibly?',
     'options': ['It is faster', 'It makes outputs deterministic/comparable across runs', 'It is cheaper', 'It improves grammar'],
     'answer': 'B', 'why': 'Lower/zero temperature reduces randomness so the same input yields stable output for fair comparison.'},
], title='Topic 6 Quiz - LLM evaluation & monitoring')
page_break(doc)

# ============================================================================
# TOPIC 7 - Cost & latency optimisation
# ============================================================================
h1(doc, '7. Cost & latency optimisation')

para(doc, 'LLM apps cost money per token and take real time per call, and both scale with usage. Two '
          'metrics drive everything: cost (priced per input + output token, so longer prompts and longer '
          'answers cost more) and latency (how long a user waits, dominated by the model size and the '
          'number of output tokens generated). Optimising is about getting acceptable quality for the '
          'least tokens, the smallest adequate model, and the fewest redundant calls.')

para(doc, 'Levers, roughly in order of bang-for-effort:')
bullet(doc, 'Caching - if the same input recurs, store and reuse the answer instead of paying for it again. Cache exact prompts, or semantically (embed the query and reuse a near-identical prior answer). Huge win for FAQ-style traffic.')
bullet(doc, 'Model selection - use the smallest/cheapest model that meets quality. Route easy requests to a small fast model and only escalate hard ones to a large model ("model cascading").')
bullet(doc, 'Prompt trimming - shorter system prompts and tighter context cut input tokens directly. For RAG, retrieve fewer, better chunks rather than stuffing everything in.')
bullet(doc, 'Limiting output - set max_tokens and ask for concise answers; output tokens are often the bigger latency cost because they are generated one at a time.')
bullet(doc, 'Batching - when you have many independent items (e.g. classifying 1000 tickets overnight), batch them; some providers offer cheaper asynchronous batch endpoints for non-urgent work.')
bullet(doc, 'Streaming - stream tokens to the user so perceived latency drops even if total time is unchanged.')

h3(doc, 'A simple cache wrapper around an LLM call')
code_block(doc,
'''import hashlib, json, functools

_cache = {}   # in real life: Redis or a database, not a dict

def cache_key(model: str, messages: list) -> str:
    blob = json.dumps({"model": model, "messages": messages}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()

def cached_completion(client, model, messages, max_tokens=300):
    key = cache_key(model, messages)
    if key in _cache:
        return _cache[key]          # cache hit: zero tokens, near-zero latency
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,      # cap output to control cost & latency
        temperature=0,              # deterministic -> safe to cache
    )
    answer = resp.choices[0].message.content
    _cache[key] = answer
    return answer''')

para(doc, 'Note temperature=0: caching only makes sense when the same input should give the same output. '
          'And max_tokens caps the most expensive, slowest part - generation. Measure before and after '
          '(tokens and latency from your Topic 6 logs) so you can prove the savings - and quote that '
          'number in your blog post and interviews.')

callout(doc, 'Common mistakes', 'Defaulting to the biggest model for everything. Stuffing huge context '
        '"just in case" when retrieval of a few good chunks is cheaper and often better. No max_tokens, '
        'so answers and bills run long. Caching non-deterministic (temperature > 0) calls and serving '
        'stale/odd results. Optimising latency you never measured - profile first. Over-caching dynamic '
        'data so users see outdated answers.', color=RED)

quiz(doc, [
    {'q': 'LLM API cost is charged per what?',
     'options': ['Per request only', 'Per input + output token', 'Per minute', 'Per user'],
     'answer': 'B - per token (input + output)', 'why': 'Longer prompts and longer completions both increase cost; trimming both saves money.'},
    {'q': 'What is "model cascading" / routing?',
     'answer': 'Short answer: send easy requests to a small cheap model and only escalate hard ones to a larger model, balancing cost and quality.',
     'why': 'Most traffic is easy; you pay for the big model only when needed.'},
    {'q': 'Why is caching with temperature=0 sensible but caching with temperature=1.0 risky?',
     'answer': 'Short answer: at temperature 0 the same input is meant to give the same output, so reusing it is correct; at high temperature outputs vary by design, so a cached one may be wrong/stale for that intent.',
     'why': 'Caching assumes a stable input->output mapping.'},
    {'q': 'Which typically dominates per-request latency?',
     'options': ['Reading the prompt', 'Generating output tokens one at a time', 'Network DNS', 'Logging'],
     'answer': 'B - output token generation', 'why': 'Tokens are produced sequentially, so longer answers take proportionally longer; capping max_tokens helps.'},
    {'q': 'Give one technique that lowers PERCEIVED latency without reducing total compute time.',
     'answer': 'Streaming the response token-by-token so the user starts reading immediately.',
     'why': 'Time-to-first-token drops even though total time is similar.'},
    {'q': 'You must classify 50,000 tickets overnight, no rush. What is the cost-smart approach?',
     'options': ['Call the largest model synchronously one at a time', 'Use batching / async batch endpoints with a small model', 'Do it by hand', 'Increase temperature'],
     'answer': 'B - batch with a small model', 'why': 'Non-urgent bulk work suits cheaper batch endpoints and the smallest adequate model.'},
    {'q': 'True or False: you should optimise latency by intuition before measuring it.',
     'answer': 'False', 'why': 'Measure first (your structured logs give tokens and latency); optimise the real bottleneck, not a guessed one.'},
], title='Topic 7 Quiz - Cost & latency')
page_break(doc)

# ============================================================================
# TOPIC 8 - Writing technical blog posts that get you hired
# ============================================================================
h1(doc, '8. Writing technical blog posts that get you hired')

para(doc, 'A blog post is a portfolio asset that works while you sleep. For a career-changer it does '
          'three jobs at once: it proves you can build, it proves you can communicate (the skill that '
          'separates good engineers from great ones, and exactly what your support background already '
          'shows), and it gives recruiters something to find when they Google you. You do not need to be '
          'an expert; you need to teach the thing you just learned, clearly, with evidence.')

para(doc, 'A reliable structure for a "build" post:')
numbered(doc, 'Hook / problem - the concrete problem in one or two sentences. "Support agents waste minutes triaging tickets. I built an assistant that drafts a category and a reply."')
numbered(doc, 'Context - who you are and why you cared (the support-to-AI angle makes it memorable).')
numbered(doc, 'What you built - a short demo: a GIF, a screenshot, and a live link near the top so skimmers see value immediately.')
numbered(doc, 'How it works - architecture in a simple diagram, the key decisions, and one or two code snippets (not the whole repo).')
numbered(doc, 'The hard part - one real problem you hit and how you solved it. This is what proves you actually built it.')
numbered(doc, 'Results / what you learned - numbers if you have them (latency, cost, accuracy), and honest limitations.')
numbered(doc, 'Call to action - links to the live demo, the repo, and your LinkedIn.')

para(doc, 'What to show vs. tell: show a demo, real numbers, and a small diagram; do not paste hundreds of '
          'lines of code or narrate every commit. Be honest about limitations - it reads as senior, not '
          'weak. Title for search and skimmers: "I built an AI support-ticket assistant - here is the '
          'architecture and what I learned" beats "My project". Publish on a platform with reach (your '
          'own site, Dev.to, Medium, or a LinkedIn article) and cross-post a short version as a LinkedIn '
          'post linking to the full piece.')

h3(doc, 'A reusable post skeleton (Markdown)')
code_block(doc,
'''# I built an AI support-ticket assistant (and what it taught me about RAG)

**TL;DR:** [one line]. Live demo: <link> - Code: <github link>

![demo](demo.gif)

## The problem
[2-3 sentences on the real pain]

## What I built
[short paragraph + a screenshot] - try it: <link>

## How it works
[simple architecture diagram]
```python
# one small, illustrative snippet
```

## The hard part
[the bug/decision and how you solved it]

## Results & limitations
- Latency: ~X ms p95   - Cost: ~$Y / 1k requests
- What it does NOT do yet: ...

## Want the details?
Code, live demo, and my LinkedIn: <links>''')

callout(doc, 'Common mistakes', 'Burying the demo link at the bottom (put it near the top). Pasting the '
        'whole codebase instead of one telling snippet. A vague title nobody searches for. No screenshot/'
        'GIF - readers want to see it. Pretending it is flawless (limitations build trust). Writing for '
        'experts instead of teaching the next learner. Never publishing because it "is not ready" - ship it.', color=RED)

quiz(doc, [
    {'q': 'Name the three jobs a technical blog post does for a career-changer.',
     'answer': 'It proves you can build, proves you can communicate, and gives recruiters something to find when they search your name.',
     'why': 'Build + communicate + discoverability.'},
    {'q': 'Where should the live demo link and a screenshot/GIF go in the post?',
     'options': ['At the very bottom', 'Near the top so skimmers see value immediately', 'Only in the repo', 'Hidden behind a sign-up'],
     'answer': 'B - near the top', 'why': 'Most readers skim; lead with proof and a clickable demo.'},
    {'q': 'Why include a "the hard part" section about a problem you hit?',
     'answer': 'Short answer: it proves you genuinely built the thing and shows real problem-solving, which is more convincing than a flawless walkthrough.',
     'why': 'Specific struggle signals authenticity and depth.'},
    {'q': 'True or False: admitting limitations makes you look weak and should be left out.',
     'answer': 'False', 'why': 'Honest limitations read as senior and build trust; hiding them looks naive.'},
    {'q': 'Which title is better for getting found and read?',
     'options': ['"My Project"', '"Update 3"', '"I built an AI support-ticket assistant - architecture and lessons"', '"Untitled"'],
     'answer': 'C', 'why': 'It is searchable, specific, and tells a skimmer the value and content.'},
    {'q': 'How much code should a "build" post contain?',
     'answer': 'Short answer: one or two short, illustrative snippets - not the whole repo; link to the full code on GitHub.',
     'why': 'Snippets illustrate; the repo holds the rest.'},
], title='Topic 8 Quiz - Technical blog posts')
page_break(doc)

# ============================================================================
# TOPIC 9 - Portfolio site + README craft
# ============================================================================
h1(doc, '9. Portfolio site + README craft')

para(doc, 'Your portfolio site and your repo READMEs are the landing pages of your career. A recruiter '
          'spends seconds deciding whether to keep reading, so both must communicate value fast: what is '
          'this, what does it do, can I see it working, and is this person credible. The README is often '
          'the very first thing an engineer opens when they click your GitHub link - a great project with '
          'a bad README looks abandoned.')

para(doc, 'A strong portfolio site is simple: a one-line positioning statement ("Maths graduate and '
          'support engineer building AI applications"), three or four flagship projects each with a '
          'screenshot, a one-sentence value statement, a live demo link and a repo link, plus a short '
          'about section and clear contact/LinkedIn. You do not need a fancy framework - a static site '
          '(plain HTML, or a template) hosted free on GitHub Pages or Netlify is enough. Substance over '
          'styling.')

para(doc, 'A strong README, top to bottom: a one-line description and a banner screenshot/GIF; a live '
          'demo link; the problem it solves and key features; a short "how it works"/architecture note; '
          'a quickstart (how to run it locally in a few commands); the tech stack; and limitations / '
          'roadmap. Show, do not just tell: a screenshot or GIF at the top is worth a thousand words.')

h3(doc, 'A README skeleton (Markdown)')
code_block(doc,
'''# Support-Ticket Assistant

> Drafts a category and a suggested reply for incoming support tickets, using RAG over your knowledge base.

**Live demo:** https://ticket-assistant.example.dev  -  **Stack:** FastAPI - OpenAI - Docker

![demo](docs/demo.gif)

## Why
Support agents spend minutes triaging each ticket. This drafts a first response in seconds.

## Features
- Auto-categorises tickets and drafts a reply
- Cites the knowledge-base passages it used
- Thumbs up/down feedback logged for evaluation

## Architecture
User -> FastAPI -> retrieval (embeddings) -> LLM -> response (+ logging/feedback)

## Run it locally
```bash
git clone https://github.com/you/ticket-assistant
cp .env.example .env        # add your OPENAI_API_KEY
docker build -t ticket-assistant . && docker run -p 8000:8000 --env-file .env ticket-assistant
```

## Limitations / roadmap
- English only for now  -  [ ] add multi-language  -  [ ] human-in-the-loop review''')

callout(doc, 'Common mistakes', 'A README that is just the default framework boilerplate. No screenshot '
        'and no live link (the two things people want most). No quickstart, so nobody can run it. Listing '
        'twenty half-finished repos instead of three polished ones. Dead demo links (test them - a 404 is '
        'worse than no link). A portfolio site that is all style and no substance, or that never ships '
        'because you are perfecting the CSS.', color=RED)

quiz(doc, [
    {'q': 'Why is the README often more important than the code for a first impression?',
     'answer': 'Short answer: it is the first thing a visitor opens; it decides whether they keep reading, and a great project with a poor README looks abandoned.',
     'why': 'It is the project landing page.'},
    {'q': 'What are the two things visitors most want at the top of a README/portfolio?',
     'options': ['A licence and a changelog', 'A screenshot/GIF and a live demo link', 'The full test suite', 'Your CV as a PDF'],
     'answer': 'B - screenshot/GIF + live demo', 'why': 'Visual proof and a clickable demo communicate value in seconds.'},
    {'q': 'How many projects should a portfolio feature, and at what quality?',
     'answer': 'Short answer: three or four polished, deployed, documented projects beat twenty half-finished ones.',
     'why': 'Curation signals judgment; quantity of junk signals the opposite.'},
    {'q': 'What does a "quickstart" section in a README let someone do?',
     'answer': 'Short answer: clone and run the project locally in a few commands, so they can actually try it.',
     'why': 'Lowers friction to evaluate your work.'},
    {'q': 'True or False: you need a complex JavaScript framework to have a credible portfolio site.',
     'answer': 'False', 'why': 'A simple static site (GitHub Pages/Netlify) with clear content and live demos is plenty; substance over styling.'},
    {'q': 'Why must you test every demo link before sharing your portfolio?',
     'answer': 'Short answer: a dead/404 link is worse than no link - it signals carelessness on the exact thing you are showcasing.',
     'why': 'Broken proof undermines credibility.'},
], title='Topic 9 Quiz - Portfolio & README')
page_break(doc)

# ============================================================================
# TOPIC 10 - CV & LinkedIn + personal branding
# ============================================================================
h1(doc, '10. CV & LinkedIn for AI roles + personal branding')

para(doc, 'Your CV and LinkedIn are not autobiographies; they are arguments that you can do an AI '
          'application developer job. The strongest asset a career-changer has is a coherent narrative, '
          'and yours is unusually good: "maths graduate + support engineer now building and deploying AI '
          'applications". Maths gives you the quantitative credibility employers want for AI; support '
          'gives you something most junior devs lack - real users, real incidents, communication, '
          'debugging under pressure, and empathy for the people who use software. The job of every line '
          'is to connect that past to this future.')

para(doc, 'The support-to-AI narrative, made explicit: in support you debugged systems you did not write, '
          'triaged and prioritised under pressure, communicated complex issues to non-technical users, '
          'and saw exactly where software frustrates people. Those are the instincts behind good '
          'observability, good evaluation, and useful AI tools. Frame your projects as solving the '
          'problems you saw in support - the ticket assistant is the perfect bridge.')

h3(doc, 'CV that lands AI interviews')
bullet(doc, 'Top "headline" + 2-3 line summary stating the narrative and your target role.')
bullet(doc, 'Projects section ABOVE or alongside experience - your deployed AI projects are your strongest evidence; each with what it does, the stack, a metric, and a live link.')
bullet(doc, 'Achievement bullets, not duties: lead with a verb and quantify ("Reduced average ticket-triage time by drafting categorised replies with a RAG assistant; deployed on Azure with CI/CD").')
bullet(doc, 'A focused skills section: Python, FastAPI, LLM APIs, RAG, Docker, GitHub Actions, Azure, SQL - the things this month and Month 1-4 gave you.')
bullet(doc, 'Reframe support experience toward transferable engineering skills; keep it tight, one to two pages.')

h3(doc, 'LinkedIn that gets you found')
bullet(doc, 'Headline with keywords recruiters search: "AI Application Developer | Python, LLMs, RAG | ex-Support Engineer | Maths Graduate".')
bullet(doc, 'About section telling the narrative in the first person, ending with what you are looking for and links to your portfolio.')
bullet(doc, 'Featured section pinning your live demos, blog posts, and portfolio site.')
bullet(doc, 'Post your work (your Month 5 blog posts) - being visible and consistent is how recruiters find you; engagement compounds.')
bullet(doc, 'Set "Open to work" for the target roles, and connect with people in AI/ML and the companies you want.')

h3(doc, 'A LinkedIn headline + summary skeleton')
code_block(doc,
'''Headline:
AI Application Developer | Python, LLMs, RAG, Docker, Azure |
Maths Graduate & ex-Support Engineer | Building & shipping AI tools

About:
I'm a maths graduate and former support engineer who now builds and
deploys AI applications. Support taught me how software really fails and
how to fix it under pressure; maths gives me the quantitative grounding
for ML. I recently built and deployed [project] - a RAG assistant that
[value], live at [link]. I'm looking for a junior AI / LLM application
developer role. Portfolio: [link]  -  Writing: [blog link]''')

callout(doc, 'Common mistakes', 'A generic "hardworking team player" summary with no narrative or '
        'keywords. Listing job duties instead of quantified achievements. Hiding deployed projects at the '
        'bottom or omitting live links. Apologising for being a career-changer instead of selling the '
        'support+maths edge. An empty Featured section and never posting, so no recruiter ever finds you. '
        'A CV that runs past two pages.', color=RED)

quiz(doc, [
    {'q': 'In one line, what is the career-change narrative this course builds toward?',
     'answer': 'Maths graduate + support engineer now building and deploying AI applications - quantitative credibility plus real-user, real-incident experience.',
     'why': 'It links the past (maths + support) to the target role coherently.'},
    {'q': 'Name two transferable skills from support that are genuinely valuable in AI engineering.',
     'answer': 'Any two of: debugging unfamiliar systems, triage/prioritisation under pressure, communicating complex issues to non-technical users, empathy for real users, incident handling - all of which underpin observability, evaluation, and useful tools.',
     'why': 'Support is real engineering-adjacent experience, not a gap.'},
    {'q': 'Why put a Projects section high on the CV for a career-changer?',
     'options': ['To fill space', 'Deployed projects are the strongest evidence you can do the job', 'It is alphabetical', 'Recruiters ignore experience'],
     'answer': 'B', 'why': 'For someone without prior dev titles, working deployed projects are the most convincing proof.'},
    {'q': 'Rewrite this as an achievement bullet: "Responsible for handling support tickets."',
     'answer': 'Example: "Triaged and resolved ~N support tickets/week, communicating fixes to non-technical users; later automated first-draft replies with a deployed RAG assistant, cutting triage time."',
     'why': 'Lead with a verb, quantify, and connect to the AI narrative.'},
    {'q': 'What belongs in a LinkedIn headline to get found by recruiters?',
     'options': ['A motivational quote', 'Keywords for the role and stack (AI, Python, LLMs, RAG)', 'Your full address', 'Nothing - leave it blank'],
     'answer': 'B - role + stack keywords', 'why': 'Recruiters search by keyword; the headline is heavily weighted.'},
    {'q': 'True or False: a career-changer should downplay the support background to look like a "pure" developer.',
     'answer': 'False', 'why': 'The support+maths combination is a differentiator; sell it as an edge, do not hide it.'},
    {'q': 'What should the LinkedIn Featured section contain?',
     'answer': 'Short answer: pinned live demos, your blog/LinkedIn posts, and your portfolio site - your best proof, one click away.',
     'why': 'It surfaces evidence at the top of your profile.'},
], title='Topic 10 Quiz - CV, LinkedIn & branding')
page_break(doc)

# ============================================================================
# EXERCISES
# ============================================================================
h1(doc, 'Exercises')
para(doc, 'Do these in order; each builds toward the project. Commit your work to GitHub as you go.')
numbered(doc, 'Deploy one Month 4 project to a PaaS (Render or Railway) or Hugging Face Spaces and get a public URL. Add a health-check endpoint and confirm it returns 200. Note the cold-start time.')
numbered(doc, 'Write a Dockerfile and .dockerignore for one project. Build the image, run the container locally with --env-file, and confirm the app works at localhost. Record the image size and try shrinking it (slim base, layer order).')
numbered(doc, 'Add a GitHub Actions workflow (.github/workflows/ci.yml) that installs deps, lints with ruff, and runs pytest on every push. Make a deliberately failing test to prove the pipeline catches it, then fix it.')
numbered(doc, 'Extend the workflow to deploy on merge to main using a deploy hook stored as a GitHub secret. Confirm a push to main updates the live site and a push to dev does not deploy.')
numbered(doc, 'Add structured JSON logging and a request-id middleware to one app. Trigger an error and find that single request in the logs using its request id.')
numbered(doc, 'Add LLM call logging (model, tokens, latency, trace_id) and a thumbs up/down feedback endpoint to your LLM app. Generate 10 sample calls and produce a tiny summary of average latency and feedback.')
numbered(doc, 'Add a cache and a max_tokens cap to your LLM app. Measure tokens and latency before and after on a repeated query, and write down the saving.')
numbered(doc, 'Write one technical blog post and rewrite your CV + LinkedIn headline/summary using the skeletons. Get one person to read each and give feedback.')
page_break(doc)

# ============================================================================
# PROJECT BRIEF
# ============================================================================
h1(doc, 'Project brief: Make your Month 4 projects public and credible')

lead(doc, 'Goal:', 'Take the projects you built in Month 4 and turn them into public, credible, '
        'employer-ready assets. By the end you have at least one live demo link, a containerised repo '
        'with CI/CD, a simple portfolio site, 2-3 published posts, and a rewritten CV and LinkedIn - all '
        'tied together by the "maths graduate + support engineer building AI applications" narrative.')

h3(doc, 'Requirements')
bullet(doc, 'At least one Month 4 project deployed live with a working public demo link (Render, Railway, Hugging Face Spaces, or Azure).')
bullet(doc, 'One project containerised with a working Dockerfile and .dockerignore (image builds and runs).')
bullet(doc, 'A GitHub Actions workflow that runs tests/lint on every push and deploys on merge to main, using secrets (no committed keys).')
bullet(doc, 'Structured logging with request ids in at least one app, plus LLM call logging and feedback capture in the LLM app.')
bullet(doc, 'At least one measured cost/latency optimisation (caching or model selection or prompt trimming) with before/after numbers.')
bullet(doc, 'A simple portfolio site (GitHub Pages or Netlify) featuring 3-4 projects with screenshots, value statements, and live/repo links.')
bullet(doc, 'Polished READMEs for the featured repos (screenshot/GIF, live link, quickstart, architecture, limitations).')
bullet(doc, '2-3 technical blog/LinkedIn posts published, each with a demo link and a code/architecture insight.')
bullet(doc, 'Rewritten CV (<=2 pages, projects-forward, quantified) and LinkedIn (keyword headline, narrative About, Featured pinned).')

h3(doc, 'Milestones (4 weeks)')
table_from_rows(doc,
    ['Week', 'Focus', 'Deliverable'],
    [
        ['Week 1', 'Deploy + Docker', 'One project live with a public demo link; one project containerised and running locally.'],
        ['Week 2', 'CI/CD + secrets + logging', 'GitHub Actions test+deploy pipeline green; secrets in place (no committed keys); structured logging + request ids added.'],
        ['Week 3', 'LLM eval + cost/latency + portfolio', 'LLM call logging + feedback live; one measured optimisation with before/after numbers; portfolio site published with 3-4 projects and polished READMEs.'],
        ['Week 4', 'Write + brand', '2-3 posts published; CV and LinkedIn rewritten around the narrative; all live links tested and working.'],
    ])

h3(doc, 'Grading rubric')
table_from_rows(doc,
    ['Criterion', 'Weight', 'Excellent (full marks) looks like'],
    [
        ['Live deployment', '20%', 'At least one project live at a stable URL; health check passes; handles cold start gracefully.'],
        ['Docker & CI/CD', '20%', 'Clean Dockerfile (slim base, cached layers, non-root, .dockerignore); Actions pipeline runs tests+lint and gates deploy on main with secrets.'],
        ['Secrets & logging', '15%', 'No secrets in repo or history; .env.example present; structured logs with request ids; LLM logging + feedback.'],
        ['Evaluation & optimisation', '15%', 'Feedback captured; at least one cost/latency optimisation with credible before/after numbers.'],
        ['Portfolio & READMEs', '15%', 'Clean site, 3-4 curated projects, screenshots, working live/repo links; READMEs with demo + quickstart + limitations.'],
        ['Writing & branding', '15%', '2-3 strong posts; CV and LinkedIn coherent, quantified, narrative-driven, keyword-rich; all links work.'],
    ])

callout(doc, 'Definition of done', 'A stranger can find you on LinkedIn, read a post, click a live demo, '
        'browse a clean README, and understand in two minutes that you are a maths-graduate support '
        'engineer who builds and ships AI applications - with the links to prove it.', color=GREEN)
page_break(doc)

# ============================================================================
# RESOURCES
# ============================================================================
h1(doc, 'Resources')
para(doc, 'All real and free (or with free tiers). Prefer official docs - they stay current.')
bullet(doc, 'Docker - official "Get Started" guide: https://docs.docker.com/get-started/')
bullet(doc, 'GitHub Actions documentation (workflows, secrets, quickstart): https://docs.github.com/en/actions')
bullet(doc, 'Render documentation (deploy from Git, render.yaml, env vars): https://render.com/docs')
bullet(doc, 'Railway documentation: https://docs.railway.app/')
bullet(doc, 'Hugging Face Spaces documentation (Gradio/Streamlit/Docker demos): https://huggingface.co/docs/hub/spaces')
bullet(doc, 'Azure Container Apps documentation: https://learn.microsoft.com/en-us/azure/container-apps/')
bullet(doc, 'The Twelve-Factor App (config, logs, dependencies - the principles behind this month): https://12factor.net/')
bullet(doc, 'Python logging HOWTO (levels, handlers, formatters): https://docs.python.org/3/howto/logging.html')
bullet(doc, 'OpenAI production best practices (rate limits, latency, cost): https://platform.openai.com/docs/guides/production-best-practices')

# ----------------------------------------------------------------------------
out_path = os.path.join(OUT, 'Month_5_Deploy_and_Brand_Study_Pack.docx')
doc.save(out_path)
print('Saved:', out_path)
