---
course: kwasi-GenAI
title: Packaging & dependencies for deploy
month: 5
monthTitle: Python for Production Apps
lesson: 4
summary: 'Make your GenAI app deployable: declare metadata and dependencies in pyproject.toml, pin versions
  for reproducible builds, isolate with a virtualenv, and containerise it for the cloud.'
objectives:
- Describe a Python project with a pyproject.toml file
- Explain why pinning dependency versions makes builds reproducible
- Separate loose requirements from a fully pinned lock for deployment
- Use a virtual environment to isolate a project's dependencies
- Write a Dockerfile that containerises a FastAPI GenAI service
- Keep secrets like API keys out of the image and pass them at runtime
video: g5-l04-packaging.mp4
quiz:
- q: What is the modern, standard file for declaring a Python project's metadata and dependencies?
  options:
  - setup.cfg
  - pyproject.toml
  - requirements.lock
  - package.json
  answer: 1
  why: pyproject.toml is the standardised project file (PEP 621) where you declare name, version, dependencies,
    and build configuration.
- q: Why pin exact dependency versions for a deployable app?
  options:
  - It makes the app run faster
  - It makes builds reproducible — the same versions install today and in six months, avoiding 'works
    on my machine' drift
  - It reduces the number of dependencies
  - It is required by Python to import packages
  answer: 1
  why: Pinning exact versions means every build installs the identical dependency set, so a build that
    passes today still behaves the same later and in production.
- q: Why should an API key never be baked into a Docker image?
  options:
  - Images can't store text
  - Anyone who pulls the image can read the secret, and it ends up in image layers and registries
  - It makes the image larger
  - Keys expire when containerised
  answer: 1
  why: Secrets baked into an image are readable by anyone with the image and persist in layer history;
    pass them at runtime via environment variables or a secrets manager instead.
- q: What does a virtual environment give a project at deploy time?
  options:
  - A faster CPU
  - An isolated set of dependencies so the project's packages don't clash with anything else on the host
  - Automatic scaling
  - A public URL
  answer: 1
  why: A virtualenv isolates the project's installed packages so versions never collide with the system
    Python or other projects.
- q: In one sentence, why use a pinned lock file in addition to your pyproject dependencies?
  answer: pyproject lists the direct dependencies you want, while a lock file records the exact resolved
    versions of every package including transitive ones, so deployments are byte-for-byte reproducible.
  why: Direct requirements can resolve to different transitive versions over time; a lock freezes the
    entire resolved tree for reproducible installs.
- q: What is the purpose of copying and installing dependencies before copying your app code in a Dockerfile?
  answer: It lets Docker cache the dependency layer, so rebuilds after a code change skip reinstalling
    unchanged dependencies and are much faster.
  why: Docker caches layers in order; putting rarely-changing dependency installs first means code edits
    don't bust the dependency cache.
resources:
- label: Python Packaging — Writing your pyproject.toml
  url: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- label: uv — An extremely fast Python package & project manager
  url: https://docs.astral.sh/uv/
- label: pip — Requirements files & reproducible installs
  url: https://pip.pypa.io/en/stable/reference/requirements-file-format/
- label: Docker — Best practices for writing Dockerfiles
  url: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- label: Docker — Build secrets (don't bake them in)
  url: https://docs.docker.com/build/building/secrets/
---

## From 'runs on my laptop' to 'runs in the cloud'

You've built an async, typed FastAPI service that calls Claude. The last gap is the one every engineer knows: making it run *reliably somewhere other than your laptop*. That means declaring what your project is and what it needs, freezing those needs so they don't drift, and wrapping it in a container the cloud can run. None of this is GenAI-specific — it's the production discipline that turns a prototype into a deployable artifact.

## Describe the project: pyproject.toml

The standard project file is **`pyproject.toml`**. It declares your app's name, version, and dependencies in one place.

```toml
[project]
name = "summariser-api"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115",
    "uvicorn>=0.30",
    "anthropic>=0.40",
    "pydantic>=2.7",
]
```

This replaces the older scattered `setup.py`/`setup.cfg`. Modern tools like **uv** or **pip** read it directly. `dependencies` lists what you *want*; the exact versions get resolved at install time.

## Pin for reproducible builds

Loose ranges like `>=0.115` are fine for development, but a deployment must be **reproducible**: the same versions today, in six months, and in production. So you also produce a **lock** — a fully pinned list of every package, including the transitive ones you never named.

```bash
# with uv
uv lock
uv export --no-dev > requirements.txt   # fully pinned

# or with pip-tools / pip freeze
pip freeze > requirements.txt
```

Now `requirements.txt` pins `fastapi==0.115.6`, `anthropic==0.42.0`, and everything underneath. This kills 'works on my machine': the build that passes CI installs the *exact* same tree in production.

## Isolate with a virtual environment

Every build still runs inside a **virtual environment** so the project's packages never clash with the host or another project.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The container does the same thing in a clean base image — isolation by construction.

## Containerise it

A **Dockerfile** is the recipe to build a runnable image. Order matters: install dependencies *before* copying your code so Docker can cache that layer and rebuilds stay fast.

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# 1. Deps first — cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Then the app code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run it:

```bash
docker build -t summariser-api .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY summariser-api
```

## Never bake in secrets

Notice the API key is passed at **runtime** with `-e`, not written into the image. A secret baked into an image is readable by anyone who pulls it and lingers in layer history and registries. In the cloud you'd inject it from a secrets manager — AWS Secrets Manager, Azure Key Vault — exactly as you already do for other services. The SDK reads `ANTHROPIC_API_KEY` from the environment automatically.

## Your task

Write a `pyproject.toml` for your summariser service, produce a fully pinned `requirements.txt`, and write a Dockerfile that installs dependencies before copying code. Build the image, run it passing `ANTHROPIC_API_KEY` at runtime, and confirm the `/docs` page loads from the container.
