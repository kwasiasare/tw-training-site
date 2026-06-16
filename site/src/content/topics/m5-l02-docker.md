---
title: Docker basics
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 2
summary: Package your AI app and all its dependencies into a portable container that runs the same on
  any machine.
objectives:
- Explain what a container is and why "works on my machine" stops being a problem
- Tell the difference between an image and a container
- Write a simple Dockerfile for a Python AI app
- Build an image and run it as a container with docker build and docker run
- Pass secrets like ANTHROPIC_API_KEY in safely with environment variables
- Map ports so you can reach a running app from your browser
- Use .dockerignore and a requirements.txt for clean, reproducible builds
video: m5-l02-docker.mp4
quiz:
- q: What is the difference between a Docker image and a container?
  answer: An image is the read-only blueprint (built once); a container is a running instance of that
    image.
  why: 'Like a class versus an object: you build one image, then run many containers from it.'
- q: Which command builds an image from a Dockerfile in the current folder and tags it 'myapp'?
  options:
  - docker run -t myapp .
  - docker build -t myapp .
  - docker create myapp
  - docker image myapp .
  answer: 1
  why: docker build reads the Dockerfile, -t myapp names the image, and the dot is the build context (current
    folder).
- q: Why should you NOT hard-code your ANTHROPIC_API_KEY inside the Dockerfile?
  answer: Anyone with the image could read the key; pass it at runtime with -e or --env-file instead.
  why: Image layers are inspectable, so baked-in secrets leak. Inject them at run time and keep them in
    env vars.
- q: In 'docker run -p 8000:80 myapp', what does 8000:80 mean?
  options:
  - Run 8000 copies on port 80
  - Host port 8000 maps to container port 80
  - Container port 8000 maps to host port 80
  - Limit memory to 8000 megabytes
  answer: 1
  why: The format is host:container — traffic to localhost:8000 is forwarded to port 80 inside the container.
- q: What is the purpose of a .dockerignore file?
  answer: It lists files and folders to exclude from the build context, so secrets and junk like .env
    or venv are not copied in.
  why: Smaller, cleaner builds and no accidental leaking of local files or credentials into the image.
- q: True or false — a container automatically keeps all its files after you delete and re-run it.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Containers are ephemeral; data written inside is lost unless you use a volume or bind mount
    to persist it.
resources:
- label: Docker — Get Started (official guide)
  url: https://docs.docker.com/get-started/
- label: Dockerfile reference (official docs)
  url: https://docs.docker.com/reference/dockerfile/
- label: Docker — Best practices for writing Dockerfiles
  url: https://docs.docker.com/build/building/best-practices/
- label: Play with Docker — free in-browser lab
  url: https://labs.play-with-docker.com/
---

## Why Docker?

You have built an A I app that runs on your laptop. But "it works on my machine" is not a deployment plan. The server might have a different Python version, missing libraries, or different settings. **Docker** solves this by packaging your code *and* everything it needs — Python, libraries, files — into a single portable unit called a **container** that runs the same everywhere.

Think of a container as a sealed lunchbox: whatever you put in stays exactly as packed, no matter whose fridge it ends up in.

## Images vs containers

This is the one distinction to nail. An **image** is the read-only blueprint — built once, stored on disk. A **container** is a running instance of that image. One image, many containers, like a class and its objects in code.

```bash
docker build -t myapp .     # build the image (blueprint)
docker run myapp            # start a container from it
docker ps                   # list running containers
```

## Writing a Dockerfile

A **Dockerfile** is a recipe: each line is a step Docker runs to build your image. Start from an official base image, copy your code in, install dependencies, then say how to start.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Copying `requirements.txt` *before* the rest of your code lets Docker cache the slow `pip install` step, so rebuilds are fast when only your code changes.

## Secrets and the Anthropic API

Never bake an API key into the image — anyone who pulls it can read the layers. Keep keys in **environment variables** and pass them in at run time. Your code reads the key from the environment; Docker hands it over with `-e` or `--env-file`.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from inside a container!"}],
)
print(msg.content[0].text)
```

Then run it without ever writing the key into a file the image keeps:

```bash
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY myapp
```

## Ports and persistence

If your app serves a web page or A P I, you must **map a port** so your browser can reach inside the container. The format is `host:container`. Also remember containers are **ephemeral**: files written inside vanish when the container is removed, unless you mount a **volume**.

```bash
docker run -p 8000:80 myapp        # localhost:8000 -> port 80 inside
docker run -v $(pwd)/data:/app/data myapp
```

## Your task

Take the A I app you built earlier and write a Dockerfile for it. Add a `.dockerignore` (exclude `.env`, `venv`, `__pycache__`), build the image, and run it — passing your `ANTHROPIC_API_KEY` as an environment variable.
