---
course: agentic-ai-engineer
title: Deploying Agents as APIs with Persistence and Scaling
month: 4
monthTitle: Evaluation, Deployment, and Capstone
lesson: 3
summary: Learn to package an agent graph behind a production FastAPI service with persistent conversation
  state, streaming token responses, and containerized deployment that scales horizontally.
objectives:
- Expose an agent graph through FastAPI endpoints with request validation and structured responses
- Implement persistent agent state using a checkpointer backed by a database for cross-request continuity
- Stream agent responses to clients using Server-Sent Events or chunked HTTP
- Containerize the service with Docker and configure it for horizontal scaling and health checks
- 'Apply production concerns: configuration, concurrency, observability, and graceful shutdown'
video: age-m4-l03-deploying-agents-as-apis-with-persistence-and-sc.mp4
quiz:
- q: Why should conversation state be stored in a shared database checkpointer rather than in process
    memory?
  options:
  - It makes the agent respond faster
  - So any replica can resume any conversation and state survives restarts
  - Because FastAPI cannot hold variables in memory
  - To reduce the number of tokens sent to the LLM
  answer: 1
  why: A shared, durable checkpointer keyed by thread_id lets stateless replicas resume any conversation
    and preserves state across restarts — essential for horizontal scaling.
- q: Which FastAPI mechanism is used to stream token-by-token agent output to clients?
  options:
  - StreamingResponse with Server-Sent Events
  - A blocking synchronous return
  - Pydantic response_model only
  - Module-level global variables
  answer: 0
  why: StreamingResponse paired with an async generator yielding SSE events streams chunks as the agent
    produces them, lowering perceived latency.
- q: Why are async endpoints (async def with ainvoke/astream) preferred for agent APIs?
  options:
  - They use less memory than sync code always
  - LLM calls are I/O-bound, so async lets one worker handle many concurrent requests
  - They guarantee the LLM returns faster
  - They remove the need for a load balancer
  answer: 1
  why: Agent requests spend most time waiting on I/O-bound LLM calls; async concurrency lets a single
    worker serve many requests while waiting.
- q: What identifies which conversation a request belongs to in the persisted state?
  options:
  - The Docker container ID
  - The thread_id in the run config
  - The Uvicorn worker number
  - The client's IP address
  answer: 1
  why: The thread_id passed in the configurable run config is the key the checkpointer uses to load and
    save that conversation's state.
- q: Name two endpoints you should add so an orchestrator (like Kubernetes) can probe the service.
  answer: /health and /ready
  why: Liveness (/health) and readiness (/ready) probes let the orchestrator know when to restart or route
    traffic to a replica.
- q: In one sentence, why must application workers stay stateless when scaling horizontally?
  answer: Because requests can hit any replica, so conversation state must live in shared storage rather
    than in any single worker's memory.
  why: Load balancers distribute requests across replicas; if state were in process memory, a follow-up
    request hitting a different replica would lose context.
resources:
- label: FastAPI documentation
  url: https://fastapi.tiangolo.com/
- label: LangGraph persistence & checkpointers
  url: https://langchain-ai.github.io/langgraph/concepts/persistence/
- label: Uvicorn deployment guide
  url: https://www.uvicorn.org/deployment/
- label: Docker Python best practices
  url: https://docs.docker.com/language/python/
---

## Why APIs for Agents

An agent that only runs in a notebook is a prototype. To serve real users you need a network-accessible service that handles concurrent requests, remembers conversations, streams output, and recovers from restarts. FastAPI is the de-facto Python choice: it is async-native, fast, and gives automatic OpenAPI docs.

## Wrapping the Agent Graph

Assume you built an agent as a compiled graph (e.g. a LangGraph `app` or any callable that takes input + config and returns output). The service layer should:

- Accept a validated request (Pydantic model)
- Attach a `thread_id` / session identifier to the run config
- Invoke the graph asynchronously
- Return a structured response

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    thread_id: str
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    result = await agent.ainvoke({"messages": [("user", req.message)]}, config)
    return ChatResponse(thread_id=req.thread_id, reply=result["messages"][-1].content)
```

Use `async def` and the async invocation methods (`ainvoke`, `astream`) so a single worker can handle many concurrent requests while waiting on LLM I/O.

## Persistence: Remembering State Across Requests

Each HTTP request is stateless, but conversations are not. A **checkpointer** persists the graph state keyed by `thread_id`. In-memory checkpointers lose everything on restart and don't work across multiple replicas, so for production use a shared database.

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

checkpointer = AsyncPostgresSaver.from_conn_string(DB_URL)
agent = graph.compile(checkpointer=checkpointer)
```

Key points:

- The `thread_id` is the conversation key — generate it client-side or server-side and return it.
- A shared store (Postgres, Redis) lets any replica resume any conversation — essential for horizontal scaling.
- Set TTLs or archival policies so state doesn't grow unbounded.

## Streaming Responses

Users expect token-by-token output. Stream with Server-Sent Events (SSE) using FastAPI's `StreamingResponse`.

```python
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    async def gen():
        async for chunk in agent.astream(
            {"messages": [("user", req.message)]}, config, stream_mode="messages"
        ):
            yield f"data: {chunk_to_text(chunk)}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```

Streaming reduces perceived latency and lets you cancel long runs early.

## Containerization

Package the app in Docker for reproducible deploys.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

For production you often front Uvicorn with Gunicorn workers or run multiple Uvicorn processes behind a load balancer.

## Scaling Horizontally

Because state lives in the shared checkpointer (not in process memory), you can run **stateless replicas** behind a load balancer. Guidelines:

- Keep workers stateless; never cache conversation state in a module-level dict.
- Size concurrency for I/O-bound LLM calls — many async tasks per worker.
- Add `/health` and `/ready` endpoints for orchestrator probes.
- Handle graceful shutdown so in-flight streams finish before the pod dies.
- Externalize secrets and config via environment variables.

## Observability

Log request IDs and `thread_id`, emit latency and token-usage metrics, and trace agent steps. Without tracing, debugging multi-step agent failures in production is nearly impossible.
