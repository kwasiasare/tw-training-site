---
course: ml-engineer
title: Deploying Models as APIs
month: 4
monthTitle: 'Production ML: Pipelines, Evaluation, and Capstone'
lesson: 3
summary: Learn how to take a trained machine learning model and serve it behind a production-ready REST
  API using FastAPI, then package it into a Docker container for reliable, portable deployment.
objectives:
- Explain why models are served behind APIs and the trade-offs of online vs. batch inference
- Load a serialized model and build prediction endpoints with FastAPI and Pydantic request validation
- Add health checks, input/output schemas, and basic error handling to a serving API
- Containerize the API with Docker, including dependency pinning and a clean entrypoint
- Test the API locally and reason about scaling, latency, and monitoring concerns in production
video: mle-m4-l03-deploying-models-as-apis.mp4
quiz:
- q: Why should a model be loaded once at application startup rather than inside the prediction endpoint?
  options:
  - It reduces the Docker image size
  - It avoids paying the load cost on every request, improving latency
  - It is required by Pydantic validation
  - It prevents the model from being versioned
  answer: 1
  why: Loading the model per request adds significant latency and wastes resources. Loading once at startup
    means every request reuses the in-memory model.
- q: What HTTP status code does FastAPI automatically return when an incoming request fails Pydantic validation?
  options:
  - '200'
  - '404'
  - '422'
  - '500'
  answer: 2
  why: FastAPI uses 422 Unprocessable Entity for validation errors when the request body doesn't match
    the declared Pydantic schema.
- q: In the Dockerfile, why is requirements.txt copied and installed before copying the rest of the application
    code?
  options:
  - To hide the source code from the image
  - To leverage Docker layer caching so dependencies aren't reinstalled on every code change
  - Because pip cannot run after COPY .
  - To reduce the number of API workers
  answer: 1
  why: Copying and installing requirements first lets Docker cache that layer; when only app code changes,
    the expensive dependency install is skipped.
- q: Which characteristic should a serving API have to scale horizontally behind a load balancer?
  options:
  - It should store session state in memory
  - It should be stateless
  - It should load the model per request
  - It should disable health checks
  answer: 1
  why: Stateless services can be replicated freely since any instance can handle any request, enabling
    horizontal scaling.
- q: What is the purpose of a /health endpoint in a deployed API?
  answer: It lets orchestrators or load balancers check that the service is alive and ready to receive
    traffic.
  why: Health checks allow infrastructure like Kubernetes or load balancers to detect unhealthy instances
    and route traffic only to healthy ones.
- q: Name one production concern, other than health checks, that you should address when serving a model
    as an API.
  answer: 'Monitoring latency and prediction drift (also acceptable: concurrency/multiple workers, model
    versioning, passing secrets via environment variables).'
  why: Production serving requires monitoring, scaling via workers, versioning, and secure secret handling
    beyond just basic functionality.
resources:
- label: FastAPI Official Documentation
  url: https://fastapi.tiangolo.com/
- label: Docker Get Started Guide
  url: https://docs.docker.com/get-started/
- label: Uvicorn Deployment Docs
  url: https://www.uvicorn.org/deployment/
- label: Pydantic Documentation
  url: https://docs.pydantic.dev/
---

## Why Serve Models as APIs?

A trained model saved as a file (e.g., `model.pkl`) is useless to other systems until it is reachable. Wrapping it in a **REST API** lets web apps, mobile clients, and other services request predictions over HTTP without knowing anything about Python or your model internals.

**Online (real-time) inference** answers one request at a time with low latency — ideal for fraud checks or recommendations. **Batch inference** scores large datasets on a schedule and is cheaper per prediction but not interactive. This lesson focuses on online serving.

## Choosing FastAPI

FastAPI is a modern Python web framework that is fast, async-capable, and gives you:

- Automatic request validation via **Pydantic** models
- Auto-generated interactive docs at `/docs` (Swagger UI)
- Type hints that double as documentation and validation

## Anatomy of a Serving API

A minimal but solid serving service has:

1. **Model loading at startup** — load once, reuse across requests (never reload per request).
2. **A request schema** — validates incoming JSON so bad input fails fast with a clear 422 error.
3. **A prediction endpoint** — transforms input, calls `model.predict`, returns JSON.
4. **A health endpoint** — lets orchestrators (Kubernetes, load balancers) know the service is alive.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from pydantic import BaseModel, ConfigDict
import joblib

MODEL_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model once at startup into app.state, not at import time.
    app.state.model = joblib.load("model.joblib")
    yield


app = FastAPI(title="Iris Classifier", lifespan=lifespan)

class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class IrisResponse(BaseModel):
    # Allow the model_version field (Pydantic v2 protects the "model_" prefix).
    model_config = ConfigDict(protected_namespaces=())
    prediction: int
    label: str
    model_version: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=IrisResponse)
def predict(req: IrisRequest, request: Request):
    model = request.app.state.model
    features = [[req.sepal_length, req.sepal_width,
                 req.petal_length, req.petal_width]]
    pred = int(model.predict(features)[0])
    return IrisResponse(prediction=pred, label=str(pred),
                        model_version=MODEL_VERSION)
```

Run it locally with:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` to try requests interactively.

## Error Handling and Validation

Pydantic automatically rejects malformed payloads with HTTP 422. For domain errors (e.g., model failure), raise `HTTPException`:

```python
from fastapi import HTTPException

try:
    pred = model.predict(features)
except Exception:
    raise HTTPException(status_code=500, detail="Inference failed")
```

Never let raw stack traces leak to clients — return clean status codes and messages.

## Containerizing with Docker

Containers package your code, dependencies, and runtime into a single portable image so it runs identically on your laptop, CI, and the cloud.

Pin dependencies in `requirements.txt`:

```
fastapi>=0.115,<0.116
uvicorn[standard]>=0.34,<0.35
gunicorn>=23.0,<24.0
scikit-learn>=1.6,<1.7
joblib>=1.4,<1.5
```

These are compatible-release ranges; regenerate and pin exact versions into a lockfile (e.g. `pip freeze > requirements.lock` or `pip-compile`) so production builds stay reproducible.

A clean `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", "--bind", "0.0.0.0:8000"]
```

Build and run:

```bash
docker build -t iris-api .
docker run -p 8000:8000 iris-api
```

**Tips:** use a `slim` base image to keep size down, copy `requirements.txt` first so dependency layers cache, and never bake secrets into the image — pass them as environment variables.

## Production Concerns

- **Concurrency:** run multiple workers to handle parallel requests — in production use Gunicorn with Uvicorn workers (e.g., `gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 4`), matching the Dockerfile `CMD`. The bare `uvicorn` command above is fine for local development. N workers each hold their own copy of the model in memory — size workers against model footprint and host RAM.
- **Latency:** keep models warm, batch where possible, and avoid heavy per-request I/O.
- **Monitoring:** log request counts, latency, and prediction distributions to detect drift.
- **Versioning:** include a model version in responses so you can trace which model produced a prediction.
- **Statelessness:** keep the API stateless so it scales horizontally behind a load balancer.
