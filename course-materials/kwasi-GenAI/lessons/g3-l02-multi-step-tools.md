---
course: kwasi-GenAI
title: Multi-step and parallel tool use
month: 3
monthTitle: Agents & Orchestration
lesson: 2
summary: Chain tool calls so each step feeds the next, and run independent tools concurrently so the agent
  finishes faster and cheaper.
objectives:
- Distinguish sequential (chained) tool use from parallel (concurrent) tool use
- Explain why Claude can emit several tool_use blocks in one turn
- Return multiple tool_result blocks correctly in a single user message
- Execute independent tools concurrently in your harness to cut latency
- Use disable_parallel_tool_use when a step must run alone
- Recognise programmatic tool calling as a way to compose many calls efficiently
video: g3-l02-multi-step-tools.mp4
quiz:
- q: When are two tool calls safe to run in parallel?
  options:
  - Always — parallelism is free
  - When neither depends on the other's result and neither has a conflicting side effect
  - Only when they call the same tool
  - Never — tools must run one at a time
  answer: 1
  why: Independent, read-only tool calls can run concurrently; calls where one needs the other's output,
    or that conflict on side effects, must be sequenced.
- q: Claude returns two tool_use blocks in a single response. How should you reply?
  options:
  - Send two separate user messages, one per result
  - Send one user message containing two tool_result blocks
  - Ignore the second and answer the first
  - Re-prompt Claude to pick one tool
  answer: 1
  why: All tool results for one assistant turn go back together in a single user message, each as its
    own tool_result block with the matching tool_use_id.
- q: What does a chained (sequential) tool flow look like?
  options:
  - Two unrelated lookups at once
  - Tool A's output becomes the input to tool B in the next loop iteration
  - One tool called repeatedly with the same input
  - A single call with no tools
  answer: 1
  why: Chaining means the result of one tool feeds the next step — for example, look up an order id, then
    use that id to fetch the order's line items.
- q: In one sentence, what is the main benefit of running independent tools concurrently?
  answer: It cuts wall-clock latency, because three two-second lookups finish in about two seconds instead
    of six.
  why: Parallel execution overlaps the waiting time of independent calls, so total latency is roughly
    the slowest call rather than the sum.
- q: What request option forces Claude to use at most one tool per turn?
  answer: Setting disable_parallel_tool_use to true inside tool_choice forces at most one tool call per
    response.
  why: disable_parallel_tool_use is the lever for steps that must run alone, such as a write that other
    steps depend on.
- q: Why does the matching tool_use_id matter when returning several results?
  answer: Each tool_result must carry the id of the tool_use block it answers so Claude can pair each
    result with the right call.
  why: Without the matching id, Claude cannot tell which result belongs to which of the several calls
    it made.
resources:
- label: Claude Docs — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Claude Docs — Implement tool use
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
- label: Claude Docs — Programmatic tool calling
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
---

## Two shapes of multi-tool work

Last lesson the loop called one tool at a time. Real tasks need two richer shapes:

- **Sequential / chained** — the output of one tool is the *input* to the next. "Find the customer id for this email, then look up that customer's open orders." Step two literally cannot start until step one returns. These run across loop iterations, one after another.
- **Parallel / concurrent** — several tools that don't depend on each other. "Get the weather in London, Paris, and Tokyo." None needs another's answer, so they can all run at the same time.

Knowing which shape you're in is the whole skill. Chaining is about *order*; parallelism is about *independence*.

## Chaining: results feed the next step

Chaining falls out of the loop naturally. Claude calls `get_customer_id(email)`, you return the id, and on the next iteration Claude uses that id to call `get_open_orders(customer_id)`. Each `tool_result` you feed back becomes context the model reasons over to choose the next call. You don't orchestrate the chain by hand — the model does, as long as your tools are well described.

```python
# Iteration 1: Claude calls get_customer_id("sam@co.com") -> "cust_88"
# Iteration 2: Claude calls get_open_orders("cust_88") -> [...]
# Iteration 3: Claude writes the answer. stop_reason == "end_turn"
```

## Parallel: one turn, several tool_use blocks

Here's the part people miss: in a **single** assistant turn, Claude can emit **several** `tool_use` blocks at once when it sees the calls are independent. Your job is to run them all and return **one** user message containing **all** the results — each as its own `tool_result` with the matching `tool_use_id`.

```python
import concurrent.futures as cf

tool_uses = [b for b in response.content if b.type == "tool_use"]

# Run independent tools concurrently
with cf.ThreadPoolExecutor() as pool:
    futures = {pool.submit(run_tool, b.name, b.input): b for b in tool_uses}
    results = []
    for fut in cf.as_completed(futures):
        block = futures[fut]
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,   # matching id is mandatory
            "content": fut.result(),
        })

messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": results})   # all results, one message
```

The win is **latency**. Three independent two-second lookups run serially take six seconds; run concurrently they take about two. For a DevOps engineer this is the same instinct as firing off independent health checks in parallel rather than looping over them.

## When to force serial execution

Parallelism is only safe when the calls are truly independent and free of conflicting side effects. A parallel-safe `read` is fine; two writes to the same record are not. When a step must run alone — say a write whose result later steps depend on — set `disable_parallel_tool_use` to `true` inside `tool_choice`, and Claude will emit at most one tool call per turn.

```python
tool_choice = {"type": "auto", "disable_parallel_tool_use": True}
```

## Composing many calls: programmatic tool calling

When a task needs *many* chained calls, each round trip pushes its intermediate result into Claude's context — tokens you pay for and rarely need again. **Programmatic tool calling** lets Claude write a small script that calls your tools as functions; the script runs in a sandbox, processes results with normal loops and filters, and only the final answer returns to the model. Reach for it when you have lots of sequential calls or large intermediate results you want filtered before they hit the context window.

## Your task

Take a task with three independent lookups (e.g. weather in three cities) and one chained pair (find a user's home city, then its weather). On paper, mark which calls go in parallel and which must be sequenced, and write the single user message of `tool_result` blocks you'd return for the parallel batch.
