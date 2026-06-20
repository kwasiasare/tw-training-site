---
course: agentic-ai-engineer
title: 'Capstone: Design, Build, and Deploy a Production Multi-Agent Application'
month: 4
monthTitle: Evaluation, Deployment, and Capstone
lesson: 4
summary: In this capstone you bring together everything from the course to design, build, and deploy a
  production-grade multi-agent application. You will scope a real problem, architect an orchestration
  layer over specialized agents, wire in RAG and memory, add an evaluation harness with guardrails and
  observability, and ship a live HTTP endpoint plus a thin UI for your portfolio.
objectives:
- Scope a realistic multi-agent use case and translate it into an architecture with clear agent roles,
  tools, and orchestration patterns.
- Implement a coordinated system combining an orchestrator, RAG retrieval, and short- plus long-term memory.
- Build an automated evaluation harness with offline test sets, online tracing, and guardrails before
  deployment.
- Deploy a containerized, authenticated, observable endpoint with cost and latency controls.
- Document and demo the system as a portfolio-ready artifact with reproducible setup and metrics.
video: age-m4-l04-capstone-design-build-and-deploy-a-production-mu.mp4
quiz:
- q: Which orchestration pattern is the safest default for a capstone because it's predictable and debuggable?
  options:
  - Peer-to-peer network hand-off
  - Supervisor / orchestrator-worker
  - Fully autonomous swarm
  - Single monolithic prompt
  answer: 1
  why: The supervisor/orchestrator-worker pattern delegates subtasks to specialists with clear control
    flow, making it predictable and easy to debug—ideal for a capstone.
- q: Why should RAG answers always include source citations in this project?
  options:
  - To increase token usage
  - To make answers longer
  - To enable faithfulness evaluation
  - To bypass authentication
  answer: 2
  why: Citations let you measure whether the answer is grounded in retrieved sources (faithfulness), a
    key evaluation metric.
- q: What is the primary purpose of a CI regression gate on the eval set?
  options:
  - To speed up inference
  - To block deployments when quality scores drop below thresholds
  - To reduce embedding dimensions
  - To rotate API keys
  answer: 1
  why: The regression gate runs the offline eval set in CI and prevents shipping changes that degrade
    quality below your defined thresholds.
- q: Which control most directly prevents runaway cost from an agent stuck in a loop?
  options:
  - Larger context window
  - Max-step and token/timeout budgets
  - More vector DB shards
  - A bigger model
  answer: 1
  why: Hard limits on steps, tokens, and timeouts stop loops before they consume excessive budget.
- q: Name one thing your portfolio README should include to make the project reproducible.
  answer: A one-command setup/run instruction (and the live URL, architecture, and eval results)
  why: Reproducibility—like a single command to run locally and one to deploy—lets others verify your
    system works, which is essential for a portfolio piece.
- q: In two or three words, what distinguishes short-term from long-term memory in this system?
  answer: Session scratchpad vs persisted facts
  why: Short-term memory is the in-session conversation/scratchpad; long-term memory is a persisted store
    of user facts and prior results, often summarized to stay bounded.
resources:
- label: 'LangGraph: building multi-agent orchestration'
  url: https://langchain-ai.github.io/langgraph/
- label: 'Langfuse: open-source LLM observability and evaluation'
  url: https://langfuse.com/docs
- label: FastAPI deployment guide
  url: https://fastapi.tiangolo.com/deployment/
- label: OpenAI guide on evaluating and productionizing agents
  url: https://platform.openai.com/docs/guides/evals
---

## Capstone Overview

This is the integrative project for the course. You will ship an **end-to-end agentic system** that a hiring manager can run, inspect, and trust. The deliverable is not a notebook demo—it is a deployed, evaluated, observable service.

Minimum viable scope:
- A clearly defined task that genuinely benefits from **multiple cooperating agents** (e.g., a research assistant that plans, retrieves, drafts, and critiques).
- An **orchestration layer** that routes work between agents and tools.
- **RAG** over a real document corpus.
- **Memory** (session-scoped + persistent).
- An **evaluation harness** with pass/fail gates.
- A **deployed endpoint** plus minimal UI or API docs.

## Step 1 — Scope and Architecture

Start from the user outcome, not the framework. Write a one-paragraph problem statement and 3-5 concrete user stories. Then decide the orchestration pattern:

- **Supervisor / orchestrator-worker**: a planner agent delegates subtasks to specialists. Best default for capstones—predictable and debuggable.
- **Sequential pipeline**: fixed stages (retrieve → draft → critique → finalize). Simple and cheap.
- **Network / hand-off**: agents pass control peer-to-peer. Powerful but harder to evaluate.

Define each agent's **role, allowed tools, and stop conditions**. Keep the number of agents small (2-4). More agents = more failure surface.

## Step 2 — RAG and Memory

**RAG**: chunk your corpus (start ~500-1000 tokens with overlap), embed, store in a vector DB, and retrieve top-k with a reranking or metadata filter. Always cite sources in the answer so you can evaluate faithfulness.

**Memory**:
- *Short-term*: the conversation/scratchpad within a session.
- *Long-term*: a persisted store (vector or key-value) for user facts and prior results. Write a summarization step so memory does not grow unbounded.

## Step 3 — Evaluation Harness

Do not ship on vibes. Build evaluation **before** deployment.

- **Offline eval set**: 20-50 curated inputs with expected behaviors. Score with deterministic checks plus an LLM-as-judge rubric (helpfulness, faithfulness, format).
- **Component metrics**: retrieval recall@k, tool-call success rate, hallucination rate, task completion.
- **Online tracing**: log every step (prompts, tool calls, tokens, latency, cost) with a tool like LangSmith/Langfuse/OpenTelemetry.
- **Regression gate**: a CI step that runs the eval set and blocks deploy if scores drop below threshold.

## Step 4 — Guardrails and Reliability

- Input/output validation (schemas, content filters, PII handling).
- **Loop and budget limits**: max steps, max tokens, timeouts to prevent runaway cost.
- Retries with backoff and graceful fallbacks (e.g., return best partial answer).
- Idempotency and structured tool outputs.

## Step 5 — Deployment

- Wrap the app in a web framework (FastAPI) exposing a `/chat` or `/run` endpoint.
- **Containerize** with Docker; pin dependencies.
- Add **auth** (API key/JWT) and rate limiting.
- Deploy to a managed host (Render, Fly.io, Cloud Run, etc.). Inject secrets via environment, never commit keys.
- Add a healthcheck and basic dashboards (latency p95, cost/request, error rate).

## Step 6 — Portfolio Packaging

- README: problem, architecture diagram, setup, eval results, live URL.
- A short Loom/GIF demo.
- Reproducible: one command to run locally, one to deploy.
- Note known limitations and next steps—shows engineering maturity.

## Common Pitfalls

- Over-engineering with too many agents.
- No evaluation, so you can't prove it works.
- Unbounded loops draining budget.
- Leaking secrets or skipping auth on a public endpoint.
- RAG with no citations, making faithfulness unmeasurable.
