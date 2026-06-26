---
course: data-scientist
title: Serving Models with FastAPI and Docker
month: 6
monthTitle: Productionization and MLOps
lesson: 1
summary: A saved model file is not a product until something can call it. This lesson turns a trained
  joblib model into a production-grade prediction service using FastAPI, loading the model once at startup
  with the lifespan pattern, validating requests and responses with Pydantic v2, and packaging everything
  in a lean, non-root Docker image. You'll also learn how worker-based concurrency interacts with model
  memory.
objectives:
- Explain why a serialized model must be wrapped in an API before it can deliver value
- Build a minimal FastAPI prediction endpoint that returns typed JSON
- Load the model once at startup using the lifespan pattern instead of an import-time global
- Define Pydantic v2 request and response schemas that include a model_version field for traceability
- Containerize the service with a slim base image, a non-root user, and deterministic dependencies
- Reason about uvicorn/gunicorn worker concurrency and its per-worker model memory cost
video: dsc-m6-l01-serving-models-with-fastapi-and-docker.mp4
quiz:
- q: Why does training and saving a model with joblib.dump() not, on its own, constitute a deployed product?
  options:
  - joblib files are too large to store in production
  - The model loses accuracy when serialized to disk
  - Nothing can call the model until you expose it behind an interface such as an API
  - Pydantic cannot read joblib files
  answer: 2
  why: A .joblib file is just bytes on disk. Other systems and users can only get predictions once you
    wrap the model in a callable interface, most commonly an HTTP API, which is exactly what FastAPI provides.
- q: What is the main advantage of loading the model in a FastAPI lifespan handler rather than as a global
    at module import time?
  options:
  - The model is loaded exactly once when the app starts and is cleanly tied to the app's lifecycle
  - The model is reloaded on every incoming request for freshness
  - It lets you avoid using Pydantic schemas entirely
  - It encrypts the model file automatically
  answer: 0
  why: The lifespan async context manager runs setup code before the app serves traffic and teardown after,
    loading the model once into app.state and binding it to the application lifecycle, which is cleaner
    and more testable than an import-time global side effect.
- q: Why should the Pydantic response model include a model_version field?
  options:
  - It makes predictions run faster
  - It is required for FastAPI to return JSON
  - It replaces the need for logging
  - It gives every prediction traceability, so you can tell which model version produced a given result
  answer: 3
  why: 'Returning the model_version with each prediction provides traceability and auditability: when
    results are investigated later, you can map a response back to the exact model that produced it, which
    is essential for debugging and governance.'
- q: Which Dockerfile choice best follows production best practice for a model service?
  options:
  - Run the container as root so it can write anywhere
  - Use a slim base image, create and switch to a non-root user, and install pinned deps with --no-cache-dir
  - Install dependencies without a requirements file to stay flexible
  - Use the full python image and run pip install with no version pins
  answer: 1
  why: A slim base reduces image size and attack surface, a non-root user limits blast radius if the container
    is compromised, and pinned dependencies installed with --no-cache-dir give deterministic, lean builds.
- q: If you run uvicorn with 4 workers serving a 500 MB model, roughly how much memory do the loaded models
    consume in total?
  options:
  - About 500 MB, because workers share one copy of the model
  - About 125 MB, because the model is split across workers
  - About 2 GB, because each of the 4 workers holds its own copy of the model
  - Zero, because the model lives only on disk
  answer: 2
  why: Each worker is a separate process with its own memory space and loads its own copy of the model
    via the lifespan handler. Four workers each holding a 500 MB model use roughly 2 GB combined, so you
    must size worker count against model footprint and host RAM.
- q: In two or three sentences, explain why feeding model input through a Pydantic request schema is safer
    than reading raw values straight from the request body, and give one concrete failure it prevents.
  answer: A Pydantic schema validates and coerces incoming data against declared types and constraints
    before your prediction code ever runs, so malformed or missing fields are rejected with a clear 422
    error instead of crashing deep in the model call. It documents the exact contract callers must follow
    and centralizes validation in one place. A concrete failure it prevents is passing a string or null
    where the model expects a numeric feature, which would otherwise raise an opaque error inside scikit-learn
    or produce a garbage prediction.
  why: Pydantic enforces the input contract at the edge of the service, converting validation into predictable,
    well-typed errors and protecting the model from receiving inputs of the wrong type, shape, or range.
resources:
- label: FastAPI Documentation
  url: https://fastapi.tiangolo.com/
- label: FastAPI Lifespan Events
  url: https://fastapi.tiangolo.com/advanced/events/
- label: 'Docker: Build best practices'
  url: https://docs.docker.com/build/building/best-practices/
- label: Pydantic Models Documentation
  url: https://docs.pydantic.dev/latest/concepts/models/
---

## Why Serving Matters

You spent weeks engineering features, tuning hyperparameters, and validating metrics. At the end you ran `joblib.dump(model, "model.joblib")` and got a file. That file is **not a product**. It is a frozen function sitting on disk that nobody and nothing can call. Value is only created when another system, a web app, a batch job, a mobile client, can send inputs and receive predictions.

The standard way to expose a model is an **HTTP API**: a small web service that loads the model, accepts JSON requests, runs `model.predict`, and returns JSON. This decouples the model from its consumers. Front-end teams don't need Python or your training environment; they just call an endpoint. **FastAPI** is the modern framework of choice because it is fast, async-friendly, and generates validation and interactive docs automatically.

## A Minimal FastAPI Prediction Service

A prediction service has three jobs: receive a request, run inference, return a response. Here is the skeleton:

```python
from fastapi import FastAPI

app = FastAPI(title="Churn Model API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(features: list[float]):
    # placeholder - we will add the model and schemas next
    return {"prediction": 0}
```

A `/health` endpoint is essential: orchestrators like Kubernetes use it to know the container is alive. But this skeleton has two problems: where does the model come from, and how do we trust the input?

## Load the Model with the Lifespan Pattern

A tempting but wrong approach is to load the model as a module-level global: `model = joblib.load(...)` at the top of the file. This runs as an import side effect, which makes testing awkward, breaks if the file is missing at import, and ties loading to import order rather than the app's actual lifecycle.

The correct, modern pattern is **lifespan**. FastAPI runs an async context manager once at startup and once at shutdown. Load the model into `app.state` so every request can reach it:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("model.joblib")
    yield
    # optional cleanup after yield

app = FastAPI(lifespan=lifespan)
```

The model loads **once**, before any traffic is served, and lives for the life of the process. Inside a handler you read it from `request.app.state.model`. This is explicit, testable, and lifecycle-aware.

## Typed Requests and Responses with Pydantic

Never trust raw input. **Pydantic v2** models declare the exact contract: which fields, which types, which constraints. Malformed requests are rejected automatically with a clear `422` before your model code runs. Crucially, the response includes a **`model_version`** field so every prediction is traceable back to the model that produced it.

```python
from pydantic import BaseModel, Field
from fastapi import Request

class PredictRequest(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(ge=0)
    support_tickets: int = Field(ge=0)

class PredictResponse(BaseModel):
    churn_probability: float
    model_version: str

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest, request: Request):
    model = request.app.state.model
    x = [[payload.tenure_months, payload.monthly_charges, payload.support_tickets]]
    proba = float(model.predict_proba(x)[0, 1])
    return PredictResponse(churn_probability=proba, model_version="1.4.0")
```

FastAPI uses these schemas to validate input, serialize output, and auto-generate OpenAPI docs at `/docs`.

## Containerize with Docker

The service must run identically on your laptop and in production. Docker packages the code, dependencies, and model into one immutable image. Follow these best practices: a **slim base image** to stay small, **pinned dependencies** for reproducibility, and a **non-root user** to limit damage if the container is breached.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and own the app files
RUN useradd --create-home appuser
COPY --chown=appuser:appuser . .
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Pin versions in `requirements.txt` (for example `fastapi==0.115.*`, `uvicorn[standard]`, `scikit-learn`, `joblib`) so a rebuild months later produces the same image. Copying `requirements.txt` before the rest of the code lets Docker cache the dependency layer and rebuild quickly when only code changes.

## Concurrency: Workers and the Memory Caveat

A single uvicorn process handles requests on one event loop, but CPU-bound `predict` calls can saturate it. To use multiple CPU cores you run **multiple workers**, often via gunicorn with uvicorn workers or `uvicorn --workers N`:

```python
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

Here is the caveat every MLOps engineer must internalize: **each worker is a separate OS process with its own memory, and each runs the lifespan handler independently, so each loads its own full copy of the model.** Four workers and a 500 MB model means roughly 2 GB of RAM just for models. Size your worker count against the model footprint and the host's available memory, not just CPU count. For large models, prefer fewer workers and horizontal scaling across containers.
