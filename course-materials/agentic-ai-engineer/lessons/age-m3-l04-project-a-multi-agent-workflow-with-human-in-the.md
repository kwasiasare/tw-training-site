---
course: agentic-ai-engineer
title: 'Project: A Multi-Agent Workflow with Human-in-the-Loop Checkpoints'
month: 3
monthTitle: Multi-Agent Orchestration with LangGraph
lesson: 4
summary: Build a production-style multi-agent workflow in LangGraph where a supervisor routes work to
  specialist agents, pauses at human approval gates before high-risk actions, and recovers gracefully
  from errors. You'll wire up shared state, conditional routing, interrupts with checkpointers, and resumable
  execution.
objectives:
- Design a supervised multi-agent topology with a router/supervisor and specialist worker agents in LangGraph
- Model shared graph state and conditional edges to coordinate a multi-step business task
- Implement human-in-the-loop approval gates using interrupts and a persistent checkpointer
- Add error-recovery patterns (retries, fallbacks, and escalation to a human) for robust execution
- Resume a paused graph from a saved checkpoint and feed in human decisions
- Evaluate when to use human checkpoints versus full autonomy in production
video: age-m3-l04-project-a-multi-agent-workflow-with-human-in-the.mp4
quiz:
- q: What two LangGraph features together enable human-in-the-loop checkpoints?
  options:
  - LLM routing and tool calling
  - A checkpointer and an interrupt (e.g., interrupt_before)
  - Streaming and async nodes
  - Subgraphs and reducers
  answer: 1
  why: A checkpointer persists state per thread_id so the run can be paused and resumed, and interrupt_before/after
    halts execution to return control for human review.
- q: Why is `Annotated[list, operator.add]` used for the errors field in state?
  options:
  - It encrypts the error messages
  - It limits the list to one item
  - It acts as a reducer so concurrent node writes append instead of overwrite
  - It converts errors to strings automatically
  answer: 2
  why: Reducers tell LangGraph how to merge state updates; operator.add appends lists so multiple nodes
    can record errors without clobbering each other.
- q: After a graph pauses at an interrupt, how do you resume it with a human decision?
  options:
  - Restart the whole graph from scratch
  - Call update_state with the decision, then invoke with None and the same config
  - Delete the checkpoint and rebuild the graph
  - Call get_state repeatedly until it continues
  answer: 1
  why: You write the human's decision into state via update_state, then invoke with None on the same thread_id
    config so execution continues from the saved checkpoint.
- q: Which actions are the best candidates for a human approval gate?
  options:
  - Every single node for maximum safety
  - Read-only data retrieval steps
  - Irreversible or high-risk actions like issuing a refund
  - LLM routing decisions
  answer: 2
  why: Gating should target irreversible or high-risk actions; over-gating reversible or low-risk steps
    destroys throughput without adding meaningful safety.
- q: Why should MemorySaver be replaced in production?
  options:
  - It is slower than all alternatives
  - It does not support interrupts
  - Its state is in-memory and lost on restart, so use a durable saver like SqliteSaver or PostgresSaver
  - It cannot store TypedDict state
  answer: 2
  why: MemorySaver keeps state in memory, which is lost on process restart; durable checkpointers persist
    state so long-running, human-gated workflows survive restarts.
- q: In one sentence, what is the role of the supervisor in this architecture?
  answer: The supervisor inspects the shared state and decides which specialist agent runs next, looping
    until the task is complete.
  why: 'The supervisor pattern centralizes routing: each worker returns to the supervisor, which reads
    state and chooses the next node or ends the run.'
resources:
- label: LangGraph Human-in-the-Loop docs
  url: https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
- label: LangGraph Persistence & Checkpointers
  url: https://langchain-ai.github.io/langgraph/concepts/persistence/
- label: LangGraph Multi-Agent (Supervisor) tutorial
  url: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/
- label: LangGraph StateGraph & Reducers API reference
  url: https://langchain-ai.github.io/langgraph/reference/graphs/
---

## Project Overview

In this project you'll build a **supervised team of agents** that processes a multi-step business task: drafting and sending a customer refund decision. The workflow includes specialist agents, **approval gates** where a human must sign off before irreversible actions, and **error recovery** so transient failures don't crash the run.

The scenario: a customer submits a refund request. The system must (1) gather order data, (2) analyze policy eligibility, (3) draft a customer email, (4) **pause for human approval** before issuing the refund, then (5) execute and confirm.

## The Architecture

We use a **supervisor pattern**: a central supervisor node inspects the shared state and routes to the right worker. Workers are specialist agents:

- **Retriever** — fetches order and customer history.
- **PolicyAnalyst** — decides eligibility against refund rules.
- **Drafter** — writes the customer-facing message.
- **Executor** — issues the refund (the irreversible action, gated by a human).

The supervisor reads state, picks the next worker, and the graph loops back to the supervisor after each worker finishes until the task is `done`.

## Shared State

All agents read and write a single typed state object. Keep it explicit:

```python
from typing import TypedDict, Literal, Annotated
import operator

class RefundState(TypedDict):
    request: str
    order: dict | None
    eligibility: str | None        # "approved" | "denied" | "unclear"
    draft_email: str | None
    human_decision: str | None     # "approve" | "reject" | "edit"
    status: str                    # routing signal
    errors: Annotated[list, operator.add]
    next: str
```

Using `Annotated[list, operator.add]` lets multiple nodes append to `errors` without clobbering each other — this is how LangGraph reducers merge concurrent writes.

## Building the Supervisor

The supervisor is a function (or small LLM call) that returns the name of the next node. Keep routing deterministic where you can — LLM routing is powerful but harder to test.

```python
def supervisor(state: RefundState) -> dict:
    if state.get("order") is None:
        return {"next": "retriever"}
    if state.get("eligibility") is None:
        return {"next": "policy_analyst"}
    if state.get("draft_email") is None:
        return {"next": "drafter"}
    if state.get("human_decision") is None:
        return {"next": "approval_gate"}
    if state["human_decision"] == "approve":
        return {"next": "executor"}
    return {"next": "END"}
```

## Wiring the Graph

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

builder = StateGraph(RefundState)
builder.add_node("supervisor", supervisor)
builder.add_node("retriever", retriever)
builder.add_node("policy_analyst", policy_analyst)
builder.add_node("drafter", drafter)
builder.add_node("approval_gate", approval_gate)
builder.add_node("executor", executor)

builder.set_entry_point("supervisor")

def route(state): return state["next"] if state["next"] != "END" else END

builder.add_conditional_edges("supervisor", route)
for worker in ["retriever", "policy_analyst", "drafter", "executor"]:
    builder.add_edge(worker, "supervisor")

# Compile with a checkpointer and an interrupt BEFORE the gate
graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["approval_gate"],
)
```

## Human-in-the-Loop Checkpoints

Two things make HITL work in LangGraph:

1. **A checkpointer** (e.g., `MemorySaver`, or `SqliteSaver`/`PostgresSaver` in production) that persists state after every step, keyed by a `thread_id`.
2. **An interrupt** — `interrupt_before=["approval_gate"]` halts execution *before* the node runs, returning control to your application.

Run until the interrupt:

```python
config = {"configurable": {"thread_id": "refund-123"}}
result = graph.invoke({"request": "...", "status": "new", "errors": []}, config)
# Execution pauses; inspect the draft
state = graph.get_state(config)
print(state.values["draft_email"])
```

A human reviews the draft and eligibility. To resume, update the state with their decision and invoke with `None`:

```python
graph.update_state(config, {"human_decision": "approve"})
final = graph.invoke(None, config)   # continues from the checkpoint
```

If the human edits the draft, write both the edit and the decision before resuming. The graph picks up exactly where it paused — no recomputation of earlier steps.

## Error Recovery

Production agents fail: APIs time out, the LLM returns malformed JSON, a tool 500s. Layer your defenses:

- **Retries with backoff** inside a node for transient errors.
- **Fallbacks**: if `policy_analyst` is unsure, route to a human instead of guessing.
- **Escalation**: append to `state['errors']`; the supervisor can route to an `approval_gate` or a `human_escalation` node when errors accumulate.

```python
def policy_analyst(state):
    try:
        result = call_llm_policy(state["order"])
        return {"eligibility": result}
    except Exception as e:
        return {"eligibility": "unclear", "errors": [str(e)]}
```

Because the checkpointer saves state after each node, a crash mid-run can be resumed from the last good checkpoint rather than restarted.

## Putting It Together — Run Loop

A real app exposes two endpoints: **start** (invoke fresh) and **resume** (after human input). Store `thread_id` so the human's later approval maps back to the right paused run. The same pattern scales to long-running tasks that wait hours or days for a human.

## Production Tips

- Use a durable checkpointer (`SqliteSaver`/`PostgresSaver`), not `MemorySaver`, so state survives restarts.
- Gate only **irreversible or high-risk** actions — over-gating destroys throughput.
- Log every state transition for auditability.
- Make routing testable: prefer deterministic supervisor logic, reserve LLM routing for genuinely ambiguous decisions.
