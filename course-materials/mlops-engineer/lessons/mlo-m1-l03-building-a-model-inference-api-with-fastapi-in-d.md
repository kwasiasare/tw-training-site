---
course: mlops-engineer
title: Building a Model Inference API with FastAPI in Docker
month: 1
monthTitle: Containerization & Foundations for ML Workloads
lesson: 3
summary: Learn to wrap a trained ML model in a production-ready REST API using FastAPI, validate requests
  with Pydantic, and package the whole service in a Docker container for reproducible, portable deployment.
objectives:
- Build a FastAPI inference service that loads a model at startup and serves predictions over HTTP
- Define request and response schemas with Pydantic for input validation and clear contracts
- Implement health and readiness endpoints for production monitoring
- Write an efficient, layer-cached Dockerfile to package the API and its dependencies
- Run, test, and debug the containerized service locally with proper port mapping and environment configuration
video: mlo-m1-l03-building-a-model-inference-api-with-fastapi-in-d.mp4
quiz:
- q: Where should you load the serialized model in a FastAPI inference service?
  options:
  - Inside the /predict request handler on every call
  - Once at application startup using lifespan or a startup event
  - In a background thread after the first request
  - In the Dockerfile during image build
  answer: 1
  why: Loading once at startup keeps the model in memory and avoids the heavy deserialization cost on
    every request, drastically reducing latency.
- q: What happens when a client sends a payload that fails Pydantic validation?
  options:
  - The server crashes with a 500 error
  - Inference runs on default values
  - FastAPI returns a 422 response before the handler runs
  - The request is silently ignored
  answer: 2
  why: Pydantic validation runs before your route logic; invalid input automatically yields a 422 Unprocessable
    Entity response, protecting the model from bad data.
- q: Why copy requirements.txt and install dependencies before copying the source code in a Dockerfile?
  options:
  - It is required by the Docker syntax
  - To leverage layer caching so code changes don't reinstall dependencies
  - To reduce the number of EXPOSE statements
  - Because pip cannot find the file otherwise
  answer: 1
  why: Docker caches layers; installing dependencies in an earlier layer means changing only source code
    reuses the cached dependency layer, speeding up rebuilds.
- q: Why must the Uvicorn server bind to 0.0.0.0 instead of 127.0.0.1 inside a container?
  options:
  - 0.0.0.0 is faster than 127.0.0.1
  - 127.0.0.1 only accepts connections from inside the container, making it unreachable from the host
  - 0.0.0.0 encrypts traffic automatically
  - It is required for Pydantic to work
  answer: 1
  why: Binding to 127.0.0.1 limits the listener to the container's own loopback; 0.0.0.0 listens on all
    interfaces so the mapped host port can reach the service.
- q: In one sentence, explain the difference between a /health (liveness) and a /ready (readiness) endpoint.
  answer: Health/liveness reports that the process is alive and running, while readiness reports that
    the service is fully initialized (e.g. model loaded) and able to accept traffic.
  why: Orchestrators restart containers that fail liveness but only remove from load balancing those that
    fail readiness, so the two probes serve distinct purposes.
resources:
- label: FastAPI Official Documentation
  url: https://fastapi.tiangolo.com/
- label: Docker Best Practices for Building Images
  url: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- label: Uvicorn Deployment Guide
  url: https://www.uvicorn.org/deployment/
- label: Pydantic Models and Validation
  url: https://docs.pydantic.dev/latest/concepts/models/
---

## Why Serve Models Behind an API?

A trained model file (e.g. `model.pkl`) is useless on its own in production. Consumers need a stable, language-agnostic way to send features and get predictions back. A **REST API** provides that contract, and a **Docker container** makes the runtime reproducible across laptops, CI, and clusters.

FastAPI is the de-facto choice for ML inference services because it is fast (ASGI/Starlette), gives you automatic OpenAPI docs, and uses **Pydantic** for type-checked request validation with almost no boilerplate.

## Project Structure

```
inference-api/
  app/
    main.py        # FastAPI app + routes
    schemas.py     # Pydantic request/response models
    model.py       # model loading + predict logic
  model.pkl        # serialized artifact
  requirements.txt
  Dockerfile
```

## Loading the Model Once

Load the model **at application startup**, not per request. Deserializing on every call destroys latency. Use FastAPI's `lifespan` (or `@app.on_event("startup")`) to load once into module/global state.

```python
# model.py
import joblib

class ModelService:
    def __init__(self):
        self.model = None
    def load(self, path: str):
        self.model = joblib.load(path)
    def predict(self, features):
        return self.model.predict([features])[0]

service = ModelService()
```

## Defining the Contract with Pydantic

```python
# schemas.py
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    sepal_length: float = Field(..., gt=0)
    sepal_width: float = Field(..., gt=0)
    petal_length: float = Field(..., gt=0)
    petal_width: float = Field(..., gt=0)

class PredictResponse(BaseModel):
    prediction: int
    model_version: str
```

Pydantic rejects malformed payloads automatically with a `422` response, so you never run inference on garbage input.

## The FastAPI App

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .model import service
from .schemas import PredictRequest, PredictResponse
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    service.load(os.getenv("MODEL_PATH", "model.pkl"))
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"ready": service.model is not None}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    features = [req.sepal_length, req.sepal_width, req.petal_length, req.petal_width]
    pred = service.predict(features)
    return PredictResponse(prediction=int(pred), model_version="1.0.0")
```

**Health vs Ready:** `/health` (liveness) says the process is alive; `/ready` (readiness) says the model is loaded and the service can accept traffic. Orchestrators like Kubernetes use these distinctly.

## Writing an Efficient Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy deps first so this layer caches when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY model.pkl .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key practices:
- Use a **slim** base image to reduce size and attack surface.
- Copy `requirements.txt` and install **before** copying source, so dependency layers stay cached.
- `--no-cache-dir` keeps the image lean.
- Bind to `0.0.0.0` (not `127.0.0.1`) so the container accepts external connections.

## Build, Run, and Test

```bash
docker build -t inference-api:1.0.0 .
docker run -p 8000:8000 inference-api:1.0.0

# test
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

Visit `http://localhost:8000/docs` for interactive Swagger UI generated automatically.

## Production Notes

- Run multiple workers via Gunicorn + Uvicorn workers for CPU-bound inference, or scale horizontally with more container replicas.
- Keep the model artifact out of source control; pull it from object storage or a model registry at build/startup.
- Log request IDs and latency; expose metrics (e.g. Prometheus) for monitoring.
- Pin dependency versions in `requirements.txt` for reproducible builds.
