---
course: mlops-engineer
title: Containerizing a Machine Learning Model with Docker
month: 1
monthTitle: Containerization & Foundations for ML Workloads
lesson: 2
summary: Learn to package a trained ML model and its dependencies into a reproducible, portable Docker
  image. This lesson walks through writing a production-ready Dockerfile, building and tagging images,
  optimizing with layer caching and multi-stage builds, and running an inference service inside a container.
objectives:
- Explain why containerization solves reproducibility and portability problems for ML workloads
- Write a Dockerfile that packages a trained model, code, and pinned dependencies
- Build, tag, and run a container image that serves model predictions
- Apply layer-caching and multi-stage build techniques to shrink image size and speed up builds
- Follow security and reproducibility best practices (pinned versions, slim base images, non-root user)
video: mlo-m1-l02-containerizing-a-machine-learning-model-with-doc.mp4
quiz:
- q: Why should you copy requirements.txt and run pip install before copying your application code in
    a Dockerfile?
  options:
  - It reduces the final image size automatically
  - It lets Docker cache the dependency layer so code changes don't trigger reinstalls
  - It is required syntax for all Dockerfiles
  - It encrypts the dependencies
  answer: 1
  why: Dependencies change less often than code. Installing them in an earlier layer means the cached
    pip install is reused when only application code changes, speeding up rebuilds.
- q: What is the main purpose of a multi-stage Docker build for ML images?
  options:
  - To run multiple models at once
  - To build wheels/artifacts in one stage and ship only the runtime in a smaller final image
  - To allow editing the model after build
  - To skip pinning dependency versions
  answer: 1
  why: Multi-stage builds let you use heavy build tools (compilers, wheel builders) in an intermediate
    stage and copy only the needed artifacts into a clean, slim final image.
- q: Which practice improves container security?
  options:
  - Running the process as root
  - Baking secrets directly into the image
  - Running as a non-root user and injecting secrets at runtime
  - Using the largest possible base image
  answer: 2
  why: Running as a non-root user limits the blast radius of a compromise, and injecting secrets at runtime
    keeps them out of the immutable image layers.
- q: What does a .dockerignore file do?
  options:
  - Lists which Python packages to install
  - Excludes files (like .git, data, venv) from the build context
  - Defines the container's start command
  - Sets environment variables at runtime
  answer: 1
  why: A .dockerignore excludes unnecessary or sensitive files from the build context, keeping builds
    fast and preventing accidental leaks.
- q: Name one reason it can be better to pull a large model from object storage at container startup rather
    than baking it into the image. (short answer)
  answer: Baking a large model bloats the image, slows pulls/deploys, and forces a rebuild for every model
    update; pulling at runtime keeps images small and lets you swap model versions without rebuilding.
  why: Large artifacts inside images increase size and rebuild frequency; externalizing them decouples
    model versioning from image builds and keeps images lean.
- q: What is the benefit of tagging an image with both a semantic version and the git SHA?
  answer: It provides human-readable versioning plus exact traceability back to the source commit that
    produced the image, aiding reproducibility and debugging.
  why: Semantic versions communicate intent while the git SHA pins the exact code state, giving full auditability
    of what is running in production.
resources:
- label: Docker official Dockerfile best practices
  url: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- label: Docker multi-stage builds guide
  url: https://docs.docker.com/build/building/multi-stage/
- label: FastAPI in containers documentation
  url: https://fastapi.tiangolo.com/deployment/docker/
- label: Google distroless base images
  url: https://github.com/GoogleContainerTools/distroless
---

## Why Containerize an ML Model?

A trained model is useless in production if it only runs on the data scientist's laptop. Containerization bundles your model artifact, inference code, system libraries, and pinned Python dependencies into a single immutable **image** that runs identically on any machine with a container runtime.

Key benefits for MLOps:

- **Reproducibility** — the exact same environment everywhere, eliminating "works on my machine".
- **Portability** — the same image runs on a laptop, CI runner, or Kubernetes cluster.
- **Isolation** — dependencies don't conflict with the host or other services.
- **Scalability** — images are the unit of deployment for orchestrators like Kubernetes.

## Anatomy of an ML Container

A typical inference container includes:

1. A **base image** (e.g. `python:3.11-slim`).
2. **System dependencies** (e.g. `libgomp1` for some ML libs).
3. **Python dependencies** from a pinned `requirements.txt`.
4. The **model artifact** (e.g. `model.pkl`, `model.joblib`, or an ONNX file).
5. **Inference code** — usually an API server such as FastAPI or Flask.

## Writing the Dockerfile

```dockerfile
# 1. Pin the base image for reproducibility
FROM python:3.11-slim

# 2. Set a working directory
WORKDIR /app

# 3. Install Python deps first to leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy code and the trained model artifact
COPY app/ ./app/
COPY model.joblib .

# 5. Run as a non-root user for security
RUN useradd --create-home appuser
USER appuser

# 6. Document the port and define the start command
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Why this order matters
Docker builds images in **layers** and caches each one. Because dependencies change far less often than your code, copying and installing `requirements.txt` *before* copying source code means a code change only rebuilds the cheap final layers — not the expensive `pip install`.

## A Minimal Inference App

```python
# app/main.py
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

model = joblib.load("model.joblib")
app = FastAPI()

class Features(BaseModel):
    values: list[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(f: Features):
    pred = model.predict([f.values])
    return {"prediction": pred.tolist()}
```

## Building and Running

```bash
# Build and tag the image (semantic + git-sha tags are good practice)
docker build -t my-model:1.0.0 .

# Run it, mapping container port 8000 to host 8000
docker run -p 8000:8000 my-model:1.0.0

# Test the endpoint
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"values": [5.1, 3.5, 1.4, 0.2]}'
```

## Optimizing the Image

### Use a `.dockerignore`
Exclude virtual envs, data, notebooks, and `.git` to keep the build context small and avoid leaking secrets.

```
.git
__pycache__/
*.ipynb
data/
venv/
```

### Multi-stage builds
When you need build tools (compilers, wheels) but don't want them in the final image, use a builder stage and copy only the artifacts forward.

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY app/ ./app/
COPY model.joblib .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Best Practices Checklist

- **Pin everything**: base image tag and every dependency version.
- **Use slim or distroless** base images to reduce attack surface and size.
- **Run as non-root**.
- **Add a HEALTHCHECK** or expose a `/health` endpoint for orchestrators.
- **Tag with both a semantic version and the git SHA** for traceability.
- **Don't bake secrets** into the image; inject them at runtime via env vars or secret managers.
- **Decide on model storage**: small models can be baked in; large models are often pulled from object storage / a registry at startup.
