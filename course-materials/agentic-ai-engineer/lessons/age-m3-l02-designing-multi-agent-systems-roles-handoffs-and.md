---
course: agentic-ai-engineer
title: 'Designing Multi-Agent Systems: Roles, Handoffs, and Communication'
month: 3
monthTitle: Multi-Agent Orchestration with LangGraph
lesson: 2
summary: Learn to architect multi-agent systems where specialized LLM agents collaborate through message
  passing, delegation, and shared state. This lesson covers role design, handoff patterns, communication
  protocols, and how to implement them in LangGraph.
objectives:
- Define specialized agent roles with clear responsibilities and boundaries
- Compare orchestration topologies (supervisor, network, hierarchical) and choose appropriately
- Implement agent handoffs and delegation using LangGraph commands and routing
- Design shared state and message-passing schemas that prevent context bloat and confusion
- Apply guardrails to control loops, termination, and error recovery in multi-agent flows
video: age-m3-l02-designing-multi-agent-systems-roles-handoffs-and.mp4
quiz:
- q: Which orchestration topology is recommended as the default starting point?
  options:
  - Network (peer-to-peer)
  - Supervisor (central router)
  - Hierarchical teams
  - Single mega-agent
  answer: 1
  why: The supervisor topology centralizes routing decisions, making the system easiest to reason about
    and debug. You only graduate to hierarchical when the supervisor prompt becomes overloaded.
- q: In LangGraph, what does the `goto` field of a `Command` specify?
  options:
  - The tool to call next
  - The next node/agent to run
  - The maximum recursion limit
  - The summary of the previous step
  answer: 1
  why: '`goto` names the next node to execute, transferring control; the `update` field writes data into
    shared state.'
- q: What is a primary risk when agents forward all their internal messages to each other?
  options:
  - Context bloat that wastes tokens and confuses models
  - Loss of the recursion limit
  - Tools becoming unavailable
  - State keys being deleted
  answer: 0
  why: Forwarding every message inflates context, raising cost and confusing the next agent. Pass summaries
    or structured payloads and use separate state channels instead.
- q: Which mechanisms help prevent infinite loops in a multi-agent graph? (select the best answer)
  options:
  - Adding more tools to each agent
  - Setting a recursion_limit and an explicit END termination path
  - Using a larger model
  - Removing the supervisor
  answer: 1
  why: A recursion_limit caps total steps and an explicit END path lets the supervisor terminate, together
    preventing runaway loops.
- q: In one or two sentences, explain the difference between delegation and a handoff.
  answer: Delegation assigns a sub-task and expects a result to be returned to the caller, while a handoff
    transfers control (and possibly ownership of the conversation) to another agent, which may not return.
  why: Delegation is request/response for a sub-task; a handoff passes control onward, so the originating
    agent may not regain control.
- q: What is a strong signal that an agent's role is too broad and should be split?
  answer: When its prompt keeps adding 'and also handle this' clauses, indicating multiple distinct responsibilities.
  why: A focused role has a single-sentence mandate; needing 'and also' instructions means it covers multiple
    jobs that belong in separate specialized agents.
resources:
- label: LangGraph Multi-Agent Concepts Documentation
  url: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
- label: LangGraph Supervisor Tutorial
  url: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/
- label: LangGraph Command and Handoffs How-To
  url: https://langchain-ai.github.io/langgraph/how-tos/command/
- label: 'LangSmith: Tracing and Evaluating Agents'
  url: https://docs.smith.langchain.com/
---

## Why Multi-Agent Systems?

A single LLM agent with one giant prompt and 30 tools quickly becomes unreliable: it forgets instructions, picks wrong tools, and produces inconsistent output. Splitting work across **specialized agents** improves accuracy, makes prompts shorter and testable, and lets teams own components independently.

Use multiple agents when:
- The task spans distinct skills (research vs. writing vs. code review).
- You need isolation of tools/permissions per role.
- You want parallelism or independent scaling/evaluation.

Avoid them when a single agent or a simple tool call works — orchestration adds latency, cost, and failure modes.

## Designing Roles

Treat each agent like a focused team member. A good role definition includes:
- **Mandate**: one clear job ("You research factual questions and return cited sources").
- **Tools**: only what the role needs (least privilege).
- **Inputs/Outputs**: a contract — what it receives and the shape it returns.
- **Boundaries**: when to hand off rather than guess.

Keep roles narrow. If a prompt needs "and also...", that's a signal to split.

## Orchestration Topologies

- **Supervisor (router)**: a central agent decides which worker handles the next step. Easiest to reason about and debug. Best default.
- **Network (peer-to-peer)**: any agent can hand off to any other. Flexible but harder to control; risk of loops.
- **Hierarchical**: supervisors of supervisors — teams of agents. Scales to complex workflows but adds depth and latency.

Start with a supervisor; graduate to hierarchical only when the supervisor prompt gets overloaded.

## Handoffs and Delegation

A **handoff** transfers control (and optionally a payload) from one agent to another. In LangGraph, agents return a `Command` that updates shared state and names the next node via `goto`.

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from typing import Literal

def supervisor(state: MessagesState) -> Command[Literal["researcher", "writer", "__end__"]]:
    decision = route(state["messages"])  # LLM picks next role
    if decision == "done":
        return Command(goto=END)
    return Command(goto=decision)

def researcher(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = do_research(state["messages"])
    return Command(goto="supervisor", update={"messages": [result]})
```

Delegation differs from handoff: in delegation the caller expects a result back (sub-task), while a handoff may transfer ownership entirely.

## Communication: Shared State vs. Messages

Two patterns to move information:
- **Shared state**: a typed object (e.g., `MessagesState` plus custom keys) all agents read/write. Great for accumulated artifacts.
- **Message passing**: agents append messages to a list; the next agent reads recent context.

Guard against **context bloat**: don't forward every internal message between agents. Pass summaries or structured handoff payloads. Consider separate state channels (e.g., `research_notes`, `draft`) instead of one giant transcript.

```python
from typing import Annotated, TypedDict
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list, add]
    research_notes: str
    draft: str
    next_agent: str
```

## Control, Loops, and Termination

Multi-agent systems can loop forever. Always add:
- A **step/iteration counter** with a max via `graph.invoke(..., {"recursion_limit": 25})`.
- Explicit **termination conditions** (supervisor returns `END`).
- **Error handling** so a failing worker reports back instead of crashing the graph.

## Practical Checklist

1. Write each agent's mandate in one sentence.
2. Define the state schema and which keys each agent touches.
3. Choose a topology (default: supervisor).
4. Implement handoffs with `Command(goto=..., update=...)`.
5. Add recursion limits and termination logic.
6. Trace and evaluate each agent independently (e.g., with LangSmith).
