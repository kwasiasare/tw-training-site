---
course: mlops-engineer
title: Multi-Container Apps with Docker Compose
month: 1
monthTitle: Containerization & Foundations for ML Workloads
lesson: 4
summary: Learn to use Docker Compose to define and run a multi-container ML application locally, orchestrating
  your model API alongside a database, cache, and supporting services with a single declarative file.
objectives:
- Explain what Docker Compose is and when to use it over plain Docker commands
- Write a docker-compose.yml file defining multiple services for an ML stack
- Configure networking, volumes, environment variables, and dependencies between services
- Use healthchecks and depends_on to control startup ordering for a model API and its database
- Manage the Compose lifecycle with up, down, logs, and build commands
- Apply best practices for local development and parity with production environments
video: mlo-m1-l04-multi-container-apps-with-docker-compose.mp4
quiz:
- q: Inside a Compose network, how should the API service connect to a database service named 'db'?
  options:
  - Using localhost:5432
  - Using the hostname 'db'
  - Using the container's IP address hardcoded
  - Using 0.0.0.0:5432
  answer: 1
  why: Compose registers each service under its service name as a DNS hostname, so the API reaches the
    database at host 'db'. localhost would refer to the API container itself.
- q: What does 'depends_on' alone guarantee by default?
  options:
  - The dependency is fully ready to accept connections
  - Only that the dependency container has started
  - That data volumes are mounted
  - That the dependency passes its healthcheck
  answer: 1
  why: 'By default depends_on only waits for the container to start, not for the service to be ready.
    You need a healthcheck with condition: service_healthy for true readiness.'
- q: Which mechanism persists database data across container removal?
  options:
  - The container's writable layer
  - A named volume
  - An environment variable
  - The ports mapping
  answer: 1
  why: Named volumes (e.g., pgdata) persist data independently of the container lifecycle, unlike the
    ephemeral container filesystem.
- q: Which command stops and removes containers, networks, AND named volumes?
  options:
  - docker compose stop
  - docker compose down
  - docker compose down -v
  - docker compose rm
  answer: 2
  why: docker compose down removes containers and networks; adding -v also removes named volumes, deleting
    persisted data.
- q: Why should you pin image versions like postgres:16 instead of postgres:latest?
  answer: To ensure reproducibility — :latest can change unexpectedly, breaking your environment, whereas
    a pinned version gives consistent, predictable builds across machines and over time.
  why: Reproducibility is a core MLOps concern; pinned versions prevent silent breakage when an image
    is updated upstream.
- q: What is the purpose of a docker-compose.override.yml file?
  answer: It adds or overrides settings (like bind mounts, hot-reload commands, or debug ports) for local
    development without modifying the base compose file used for CI/staging, supporting environment parity.
  why: Override files let you keep a clean shared base config while customizing behavior per environment.
resources:
- label: Docker Compose official documentation
  url: https://docs.docker.com/compose/
- label: Compose file specification reference
  url: https://docs.docker.com/reference/compose-file/
- label: Control startup and shutdown order in Compose
  url: https://docs.docker.com/compose/how-tos/startup-order/
- label: Manage data in Docker (volumes)
  url: https://docs.docker.com/storage/volumes/
---

## Why Docker Compose?

When you deploy an ML model, the API rarely runs alone. It usually needs a database to store predictions or features, a cache like Redis for fast lookups, and maybe a message queue or a feature store. Running each container manually with long `docker run` commands is error-prone and hard to reproduce.

**Docker Compose** lets you define an entire multi-container application in a single declarative YAML file (`docker-compose.yml`). One command — `docker compose up` — builds, networks, and starts everything together. This gives you reproducible local environments that closely mirror production.

## Anatomy of a docker-compose.yml

A Compose file describes **services** (containers), **networks**, and **volumes**.

```yaml
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://ml:secret@db:5432/predictions
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=ml
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=predictions
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ml"]
      interval: 5s
      retries: 5
volumes:
  pgdata:
```

Key points:
- `build:` builds from a Dockerfile; `image:` pulls a prebuilt image.
- `ports:` maps host:container so you can reach the API at `localhost:8000`.
- `environment:` injects config — never hardcode secrets in your image.

## Service-to-Service Networking

Compose automatically creates a default network and registers each service under its **service name** as a DNS hostname. Your API connects to the database using the host `db`, not `localhost`. This is one of the most common beginner mistakes — inside the network, `localhost` refers to the container itself, not a peer service.

## Controlling Startup Order with Healthchecks

`depends_on` controls *startup order*, but by default it only waits until the container starts — not until the service is *ready*. A Postgres container may be running but not yet accepting connections. Combine `depends_on` with `condition: service_healthy` and a `healthcheck` so your API only starts after the database can actually serve queries.

## Persisting Data with Volumes

Containers are ephemeral. If you store your database data inside the container filesystem, it disappears when the container is removed. **Named volumes** (like `pgdata`) persist data across restarts. **Bind mounts** map a host directory into the container — useful for live-reloading code or mounting model artifacts during development.

## The Compose Lifecycle

- `docker compose up -d` — build (if needed) and start all services in the background.
- `docker compose logs -f api` — follow logs from one service.
- `docker compose ps` — list running services.
- `docker compose down` — stop and remove containers and networks (add `-v` to also remove volumes).
- `docker compose build` — rebuild images after code changes.
- `docker compose up --build` — rebuild and restart in one step.

## Configuration & Environment Management

Use a `.env` file for variables Compose interpolates into the YAML, and `env_file:` to inject runtime variables into a container. Keep secrets out of version control. For environment parity, use Compose **override files** (`docker-compose.override.yml` for local dev) so you can add bind mounts and debug ports locally without changing the base file used for CI or staging.

## Best Practices for ML Workloads

- Pin image versions (`postgres:16`, not `postgres:latest`) for reproducibility.
- Keep heavy model artifacts in volumes or object storage, not baked into images when iterating.
- Define resource awareness — Compose is for local/dev; production typically moves to Kubernetes.
- Use healthchecks on the model API itself so dependent services know when it's ready.
