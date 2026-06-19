---
course: ai-app-developer-2026
title: Building Multi-Step and Multi-Agent Workflows
month: 3
monthTitle: Agents, Tools, and APIs
lesson: 3
summary: Learn to orchestrate LLM agents that delegate subtasks, share memory, and recover from errors
  across multi-step workflows. This lesson covers orchestration patterns (sequential, router, supervisor,
  and parallel fan-out), state and memory passing, tool delegation, and resilient error handling so you
  can ship reliable multi-agent applications.
objectives:
- Describe common multi-agent orchestration patterns and when to use each
- Design a workflow that decomposes a goal into delegated subtasks across specialized agents
- Manage shared state and memory so agents pass context without losing information
- Implement error handling, retries, and fallbacks that keep workflows resilient
- Add guardrails like step limits and validation to prevent runaway agent loops
video: aad-m3-l03-building-multi-step-and-multi-agent-workflows.mp4
quiz:
- q: Which orchestration pattern uses a coordinator agent that dynamically decides which worker to call
    next and loops until the goal is met?
  options:
  - Sequential pipeline
  - Router
  - Supervisor
  - Parallel fan-out
  answer: 2
  why: The supervisor (orchestrator) pattern uses a coordinator that dynamically chooses the next worker
    and loops, making it the most flexible but also requiring guardrails like step limits.
- q: Why should you pass each agent only the slice of state it needs rather than the full history?
  options:
  - It is required by all LLM APIs
  - It reduces token cost and prevents confusion
  - It makes agents stateful
  - It removes the need for error handling
  answer: 1
  why: Sending only the relevant slice of state lowers token usage and keeps each agent focused, reducing
    the chance of confusion from irrelevant context.
- q: Which guardrail most directly prevents a supervisor agent from looping forever and burning tokens?
  options:
  - Vector store retrieval
  - Step/loop limits
  - Parallel fan-out
  - Long-term memory
  answer: 1
  why: Capping the number of iterations with step or loop limits stops a dynamic supervisor agent from
    running indefinitely.
- q: What is the recommended format for handoffs between agents so the next agent can parse the result
    reliably?
  answer: Structured output such as JSON
  why: Returning structured, parseable output like JSON makes delegation reliable, letting the receiving
    agent consume defined inputs like a function call.
- q: 'True or false: Long-term memory is typically stored in a vector store or database and retrieved
    only when relevant.'
  options:
  - 'True'
  - 'False'
  answer: 0
  why: Long-term memory persists across sessions and is commonly kept in a vector store or database, with
    relevant items retrieved on demand rather than always included.
resources:
- label: LangGraph documentation — building stateful multi-agent workflows
  url: https://langchain-ai.github.io/langgraph/
- label: OpenAI Agents / function calling guide
  url: https://platform.openai.com/docs/guides/function-calling
- label: 'Anthropic: Building effective agents'
  url: https://www.anthropic.com/research/building-effective-agents
---

## Why Multi-Step and Multi-Agent Workflows

A single prompt-and-response call works for simple tasks, but real applications often need many steps: gather data, reason, call tools, validate, and produce output. When one agent tries to do everything, prompts grow bloated and reliability drops. **Multi-agent workflows** split the work across specialized agents, each with a focused role, smaller prompt, and limited tool set.

Think of it like a software team: a planner breaks down the goal, workers execute pieces, and a reviewer checks the result.

## Core Orchestration Patterns

- **Sequential (pipeline):** Output of agent A feeds agent B feeds agent C. Best for linear processes like *research → draft → edit*.
- **Router:** A classifier agent inspects the request and routes it to the right specialist (billing vs. tech support). Cheap and predictable.
- **Supervisor / orchestrator:** A coordinator agent dynamically decides which worker to call next and loops until the goal is met. Most flexible, but needs guardrails.
- **Parallel fan-out / fan-in:** Run several agents at once (e.g., summarize 5 documents), then aggregate results. Faster for independent subtasks.

Start with the simplest pattern that solves the problem. Sequential and router workflows are easier to debug than fully autonomous supervisors.

## State and Memory

Agents are stateless by default, so the orchestrator must carry context between steps. Two kinds of memory matter:

- **Short-term (working) memory:** The shared state object passed through the workflow — the task, intermediate results, and scratchpad. Keep it structured (a dict or typed object), not just a growing transcript.
- **Long-term memory:** Persisted knowledge across sessions, often stored in a vector store or database and retrieved when relevant.

Don't pass the entire history to every agent. Give each agent only the slice of state it needs. This reduces token cost and prevents confusion.

```python
state = {
    "goal": "Write a market summary for product X",
    "research": None,
    "draft": None,
    "errors": [],
}

def run_pipeline(state):
    state["research"] = research_agent(state["goal"])
    state["draft"] = writer_agent(state["goal"], state["research"])
    return editor_agent(state["draft"])
```

## Delegation and Tools

Delegation means one agent hands a subtask to another agent or a tool. Practical rules:

- Give each agent a **clear role description** and only the tools it needs.
- Define handoffs explicitly — return structured output (JSON) so the next agent can parse it reliably.
- Treat sub-agents like function calls: defined inputs, defined outputs.

## Error Handling and Resilience

Multi-step workflows multiply failure points. Plan for them:

- **Retries with backoff** for transient API/tool errors.
- **Validation** of each agent's output before passing it on (schema checks, JSON parsing). Re-prompt the agent if output is malformed.
- **Fallbacks:** if a specialist fails, route to a default handler or return a graceful message.
- **Step / loop limits:** cap iterations so a supervisor agent can't loop forever and burn tokens.
- **Logging and tracing:** record every agent call, input, and output so you can debug and observe cost.

```python
def safe_call(agent, *args, retries=2):
    for attempt in range(retries + 1):
        try:
            out = agent(*args)
            if validate(out):
                return out
        except Exception as e:
            log(f"attempt {attempt} failed: {e}")
    return fallback_response()
```

## Putting It Together

A robust workflow combines a pattern (e.g., supervisor), structured shared state, explicit handoffs, validation, and guardrails. Build incrementally: get a sequential version working, add validation, then introduce dynamic routing only if needed. Always instrument with logging so you can see what each agent did.
