---
course: agentic-ai-engineer
title: 'Introduction to LangGraph: State, Nodes, and Edges'
month: 3
monthTitle: Multi-Agent Orchestration with LangGraph
lesson: 1
summary: LangGraph models agent workflows as explicit stateful graphs, giving you fine-grained control,
  persistence, and observability that simple chains and ReAct loops lack. This lesson teaches the three
  core primitives—State, Nodes, and Edges—and how to compile and run a graph.
objectives:
- Explain why graph-based orchestration improves control, persistence, and observability over linear chains
- Define a typed graph State using TypedDict and reducer annotations
- Implement nodes as pure functions that read state and return partial updates
- Wire normal and conditional edges, including START and END, to control flow
- Compile and invoke a StateGraph, and add a checkpointer for persistence
video: age-m3-l01-introduction-to-langgraph-state-nodes-and-edges.mp4
quiz:
- q: What is the purpose of a reducer in a LangGraph state field?
  options:
  - It validates the LLM output before it is stored
  - It defines how a node's update is merged into existing state
  - It compiles the graph into a runnable
  - It schedules which node runs next
  answer: 1
  why: A reducer (set via Annotated[type, fn]) tells LangGraph how to merge an update with the current
    value—e.g. operator.add appends to a list instead of overwriting it.
- q: What should a node function return?
  options:
  - The entire new state object
  - A boolean indicating success
  - A partial state update containing only changed keys
  - The name of the next node to run
  answer: 2
  why: Nodes return a partial dict of just the keys they change; LangGraph merges it into state using
    the reducers.
- q: Which construct lets the graph choose its next node based on the current state?
  options:
  - A normal edge
  - A conditional edge
  - A checkpointer
  - The END sentinel
  answer: 1
  why: add_conditional_edges runs a router function that inspects state and returns the name of the next
    node, enabling branching.
- q: What does adding a checkpointer at compile time provide?
  options:
  - Faster LLM inference
  - Automatic prompt optimization
  - 'Persistence: state snapshots that enable resume and human-in-the-loop'
  - Type validation of the state schema
  answer: 2
  why: A checkpointer snapshots state after each step; with a thread_id this gives durable, resumable
    execution and human-in-the-loop pauses.
- q: In one sentence, what happens to a state field that has no reducer when a node returns a new value
    for it?
  answer: The new value overwrites (replaces) the existing value.
  why: Without a reducer, the default behavior is replacement rather than merging or appending.
- q: Name the two special sentinels used to mark a graph's entry and exit points.
  answer: START and END
  why: START marks where execution begins and END marks where it terminates; edges connect these to your
    nodes.
resources:
- label: LangGraph Documentation
  url: https://langchain-ai.github.io/langgraph/
- label: LangGraph Low-Level Concepts (State, Nodes, Edges)
  url: https://langchain-ai.github.io/langgraph/concepts/low_level/
- label: LangGraph Persistence & Checkpointers Guide
  url: https://langchain-ai.github.io/langgraph/concepts/persistence/
- label: LangGraph Quickstart Tutorial
  url: https://langchain-ai.github.io/langgraph/tutorials/introduction/
---

## Why LangGraph?

Most first agents are built as linear chains or a single ReAct loop. These work for demos but break down in production: you cannot easily branch, retry, loop, pause for human input, or inspect what happened. LangGraph reframes an agent as a **stateful graph**—a set of nodes (units of work) connected by edges (control flow) that all read from and write to a shared **state** object.

This buys you three things:

- **Control** — explicit branching, loops, and routing instead of hoping the LLM does the right thing.
- **Persistence** — checkpointers snapshot state after every step, enabling resume, time-travel, and human-in-the-loop.
- **Observability** — every transition is a discrete, inspectable event you can trace and debug.

## The State

State is the single source of truth that flows through the graph. You declare its shape with a `TypedDict` (or Pydantic model).

```python
from typing import Annotated, TypedDict
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list, add]   # reducer: append, don't overwrite
    step_count: int                  # default behavior: overwrite
```

Each key can have a **reducer** via `Annotated[type, reducer_fn]`. A reducer decides how a node's update is merged into existing state. Without a reducer, the new value **replaces** the old one; with `add` (or `operator.add`), lists are concatenated—essential for accumulating message history.

## Nodes

A node is just a function (sync or async) that takes the current state and returns a **partial** state update—a dict containing only the keys it wants to change.

```python
def call_model(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response], "step_count": state["step_count"] + 1}
```

Nodes should be small and ideally side-effect-aware. They never mutate state in place; they return updates that LangGraph merges using the reducers.

## Edges

Edges define how control moves between nodes.

- **Normal edge**: always go from A to B — `graph.add_edge("a", "b")`.
- **Conditional edge**: a routing function inspects state and returns the name of the next node — `graph.add_conditional_edges("a", router_fn)`.
- **START / END**: special sentinels marking entry and exit points.

```python
from langgraph.graph import StateGraph, START, END

def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

builder = StateGraph(AgentState)
builder.add_node("model", call_model)
builder.add_node("tools", call_tools)
builder.add_edge(START, "model")
builder.add_conditional_edges("model", should_continue)
builder.add_edge("tools", "model")   # loop back
graph = builder.compile()
```

## Compiling and Running

Calling `.compile()` validates the graph and returns a runnable. Invoke it with an initial state:

```python
result = graph.invoke({"messages": [user_msg], "step_count": 0})
```

You can also `.stream()` to observe each node's output as it executes.

## Persistence with Checkpointers

Pass a checkpointer at compile time to snapshot state after every step. With a `thread_id`, you get durable, resumable conversations and human-in-the-loop pauses.

```python
from langgraph.checkpoint.memory import MemorySaver

graph = builder.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "user-123"}}
graph.invoke({"messages": [user_msg], "step_count": 0}, config)
```

In production swap `MemorySaver` for a SQLite or Postgres saver so state survives restarts.

## Mental Model

Think of LangGraph as a state machine for agents: state is the data, nodes are the work, edges are the rules, and the checkpointer is the memory. Master these four and you can build loops, retries, and multi-agent systems with confidence.
