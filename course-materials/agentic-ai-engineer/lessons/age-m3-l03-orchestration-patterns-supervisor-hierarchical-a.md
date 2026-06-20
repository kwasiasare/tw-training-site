---
course: agentic-ai-engineer
title: 'Orchestration Patterns: Supervisor, Hierarchical, and Parallel Agents'
month: 3
monthTitle: Multi-Agent Orchestration with LangGraph
lesson: 3
summary: Learn to implement the three foundational multi-agent coordination topologies in LangGraph—supervisor
  routing, hierarchical teams, and parallel fan-out/fan-in—so you can route tasks intelligently, compose
  nested agent teams, and run independent work concurrently while safely merging results.
objectives:
- Distinguish the supervisor, hierarchical, and parallel orchestration patterns and when each is appropriate
- Implement a supervisor agent in LangGraph that routes tasks to specialized workers using conditional
  edges
- Compose nested teams into a hierarchical graph using subgraphs and shared state
- Run agents concurrently with fan-out edges and merge their outputs safely using reducer-based state
- Apply state-management and error-handling practices that keep multi-agent systems production-ready
video: age-m3-l03-orchestration-patterns-supervisor-hierarchical-a.mp4
quiz:
- q: In the supervisor pattern, what determines which worker node runs next?
  options:
  - A fixed sequential edge order
  - The supervisor's routing decision via conditional edges
  - Random selection by the runtime
  - Whichever worker has the lowest latency
  answer: 1
  why: The supervisor node returns a routing decision (e.g., the 'next' field), and add_conditional_edges
    maps that value to the target node, enabling dynamic LLM-driven routing.
- q: Why must channels written by parallel branches use a reducer like operator.add?
  options:
  - To make the graph compile faster
  - To avoid conflicting concurrent writes to the same state key
  - To enable checkpointing
  - To bypass the recursion limit
  answer: 1
  why: When multiple nodes run in the same superstep and write the same key, LangGraph needs a reducer
    to merge the updates; without one it raises a conflict error.
- q: How is a hierarchical orchestration implemented in LangGraph?
  options:
  - By increasing the recursion_limit
  - By using a compiled team graph as a node (subgraph) inside a parent graph
  - By disabling reducers
  - By calling the LLM with more tokens
  answer: 1
  why: A compiled graph can be added as a node in another graph, so each team becomes a subgraph governed
    by a top-level supervisor.
- q: What is the purpose of the Send API?
  options:
  - To checkpoint state to disk
  - To dynamically spawn a variable number of parallel node invocations at runtime
  - To stop infinite supervisor loops
  - To convert messages into embeddings
  answer: 1
  why: Send lets a node return a list of invocations (each with its own payload) so LangGraph runs N copies
    of a worker concurrently—dynamic fan-out for map-style work.
- q: In a fan-out/fan-in design, when does the aggregator node execute?
  options:
  - As soon as the first branch completes
  - Only after all incoming branches complete
  - Before the branches run
  - Once per branch, repeatedly
  answer: 1
  why: 'The aggregator acts as a synchronization barrier: it runs a single time after every incoming parallel
    branch has finished.'
- q: Name one safeguard you should add to prevent a supervisor from looping forever.
  answer: Set a recursion_limit (or track a step counter to force FINISH).
  why: Supervisor loops can run indefinitely if the LLM never returns FINISH; a recursion limit or explicit
    step counter stops runaway execution.
resources:
- label: LangGraph Multi-Agent Concepts (official docs)
  url: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
- label: 'LangGraph Tutorial: Hierarchical Agent Teams'
  url: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/
- label: 'LangGraph How-to: Map-Reduce with the Send API'
  url: https://langchain-ai.github.io/langgraph/how-tos/map-reduce/
- label: LangGraph State, Reducers, and Channels Reference
  url: https://langchain-ai.github.io/langgraph/concepts/low_level/
---

## Why Orchestration Patterns Matter

A single LLM agent works for simple tasks, but real workloads need multiple specialized agents that coordinate. LangGraph models this as a **stateful graph**: nodes are agents (or functions), edges define control flow, and a shared **state** object carries data between nodes. The way you wire nodes and edges *is* your orchestration pattern.

Three patterns cover the vast majority of production designs:

- **Supervisor** — one coordinator decides who acts next.
- **Hierarchical** — supervisors of supervisors; teams nested inside teams.
- **Parallel** — multiple agents run concurrently, then results are merged.

## State Is the Backbone

Every LangGraph app defines a typed state. Channels can have **reducers** that control how updates merge—critical once agents run in parallel.

```python
from typing import Annotated, TypedDict
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]  # appends across nodes
    next: str                                # supervisor routing decision
    results: Annotated[list, operator.add]   # parallel workers append here
```

Without a reducer, two parallel nodes writing the same key cause a conflict error. With `operator.add`, their lists are concatenated automatically.

## Pattern 1: Supervisor

A supervisor agent inspects the state and chooses the next worker, or decides the task is done. Workers report back to the supervisor, creating a hub-and-spoke loop.

```python
from langgraph.graph import StateGraph, START, END

def supervisor(state: AgentState):
    # An LLM call returns one of: "researcher", "coder", or "FINISH"
    decision = route_with_llm(state["messages"])
    return {"next": decision}

def researcher(state): ...
def coder(state): ...

graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("coder", coder)

graph.add_edge(START, "supervisor")
# Conditional edge maps the routing decision to a node
graph.add_conditional_edges(
    "supervisor",
    lambda s: s["next"],
    {"researcher": "researcher", "coder": "coder", "FINISH": END},
)
graph.add_edge("researcher", "supervisor")
graph.add_edge("coder", "supervisor")
app = graph.compile()
```

**Use when** tasks need dynamic, LLM-driven routing and a clear point of accountability. Watch out for infinite loops—add a step counter or `recursion_limit`.

## Pattern 2: Hierarchical

When the number of workers grows, a single supervisor becomes a bottleneck and its prompt gets unwieldy. Split workers into **teams**, each with its own sub-supervisor, then add a **top-level supervisor** that routes between teams.

In LangGraph, a compiled graph can be used as a node inside another graph (a **subgraph**). The research team and the writing team are each their own supervisor graph; the top graph routes between them.

```python
research_team = build_research_graph().compile()
writing_team = build_writing_graph().compile()

top = StateGraph(AgentState)
top.add_node("research_team", research_team)
top.add_node("writing_team", writing_team)
top.add_node("top_supervisor", top_supervisor)
# top_supervisor routes between the two team subgraphs
```

**Use when** you have many specialists, distinct domains, or want to reuse a team across projects. Keep state schemas compatible across levels (or transform at the boundary).

## Pattern 3: Parallel (Fan-Out / Fan-In)

When subtasks are independent, run them concurrently to cut latency. From one node, add edges to several nodes; LangGraph executes them in the same **superstep**. A downstream **aggregator** node fans them back in.

```python
graph.add_edge("dispatch", "search_web")
graph.add_edge("dispatch", "search_docs")
graph.add_edge("dispatch", "search_db")
# All three run concurrently, each appends to results (reducer required)
graph.add_edge("search_web", "aggregate")
graph.add_edge("search_docs", "aggregate")
graph.add_edge("search_db", "aggregate")
```

The `aggregate` node only runs once **all** its incoming branches complete (a synchronization barrier). Because the workers write to a reducer channel (`results` with `operator.add`), their outputs merge without conflict.

For dynamic fan-out (unknown number of branches at build time), use the **Send** API to spawn N parallel invocations of the same node.

```python
from langgraph.constants import Send

def dispatch(state):
    return [Send("worker", {"task": t}) for t in state["tasks"]]
```

## Choosing and Combining Patterns

These patterns compose. A common production shape is a **hierarchical supervisor** whose teams internally **fan out** work in parallel. Start simple (single supervisor), measure latency and accuracy, then introduce hierarchy or parallelism only where it pays off.

## Production Considerations

- **Loop guards**: set `recursion_limit` and track step counts to prevent runaway supervisors.
- **State reducers**: always use reducers for any channel written by parallel branches.
- **Checkpointing**: attach a checkpointer for durability, retries, and human-in-the-loop pauses.
- **Observability**: trace each node (e.g., LangSmith) to debug routing decisions.
- **Cost/latency**: parallelism reduces wall-clock time but increases concurrent token spend—budget accordingly.
