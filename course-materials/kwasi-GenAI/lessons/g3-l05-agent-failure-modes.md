---
course: kwasi-GenAI
title: 'Agent failure modes: loops, wrong tools, context bloat'
month: 3
monthTitle: Agents & Orchestration
lesson: 5
summary: Learn the three classic ways agents go wrong — runaway loops, wrong tool selection, and context
  bloat — and the concrete guardrails that detect and bound each one.
objectives:
- Identify the three common agent failure modes and what each looks like in practice
- Bound a loop with iteration caps, token budgets, and stagnation detection
- Improve tool selection with clearer descriptions, enums, and fewer tools
- Detect and prevent context bloat as tool results accumulate over many turns
- Add logging that surfaces each failure mode before it costs you
- Connect agent guardrails to the CI/CD and monitoring habits you already use
video: g3-l05-agent-failure-modes.mp4
quiz:
- q: What is a runaway loop?
  options:
  - A tool that returns too slowly
  - An agent that keeps calling tools without making progress, often repeating the same failing call
  - A model that refuses to answer
  - A network timeout
  answer: 1
  why: A runaway loop is an agent stuck cycling — repeating actions or oscillating — without converging
    on the goal, burning tokens the whole time.
- q: Which guardrail most directly bounds a runaway loop?
  options:
  - A bigger model
  - A maximum iteration count, plus a token budget and stagnation detection
  - Disabling all tools
  - A longer system prompt
  answer: 1
  why: Hard caps on iterations and tokens, combined with detecting repeated identical calls, stop a runaway
    before it spirals.
- q: What most often causes wrong tool selection?
  options:
  - The model is broken
  - Vague or overlapping tool descriptions, or too many tools to choose from
  - The temperature setting
  - Using the Messages API
  answer: 1
  why: Claude picks tools from their descriptions; vague, overlapping, or too-numerous tools make the
    right choice ambiguous.
- q: In one sentence, what is context bloat and why does it hurt?
  answer: It is the steady growth of the conversation as tool results pile up, which raises cost and latency
    and can crowd out the information that matters.
  why: Every turn re-sends the whole history; unbounded growth means you pay for and reason over stale
    tool output you no longer need.
- q: Name one technique to control context bloat in a long-running agent.
  answer: Use context editing or compaction to prune or summarise old tool results and thinking, keeping
    the transcript lean.
  why: Context editing clears stale content and compaction summarises it, so the working context stays
    focused without losing structure.
- q: How does an iteration cap on an agent mirror something from CI/CD?
  answer: It is the same as a job timeout in a pipeline — a hard ceiling that kills a run that has stopped
    making progress so it can't hang forever.
  why: Bounding an agent loop is the same operational instinct as setting timeouts and retry limits on
    pipeline jobs.
resources:
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
- label: Claude Docs — Handling stop reasons
  url: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- label: Claude Docs — Context editing
  url: https://platform.claude.com/docs/en/build-with-claude/context-editing
- label: Claude Docs — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
---

## Agents fail in predictable ways

The good news about agent failures is that they are *boring* — there are a handful of them and they recur. Once you can name the three big ones, you can build the guardrail for each before you ship. This is exactly the posture you already take with infrastructure: you don't hope a job won't hang, you set a timeout.

The three to know: **runaway loops**, **wrong tool selection**, and **context bloat**.

## Failure 1: runaway loops

A **runaway loop** is an agent that keeps acting without making progress. The classic signature is the same tool call, with the same input, returning the same error, over and over — the model trying the locked door repeatedly. Sometimes it oscillates between two tools instead.

Three guardrails, all cheap:

- **Iteration cap** — hard-limit the number of times around the loop (e.g. 10). When you hit it, stop and surface what happened. This is a job timeout.
- **Token budget** — track cumulative tokens and abort past a ceiling. Money guard.
- **Stagnation detection** — if the last N tool calls are identical, or the same error repeats, break out. Progress guard.

```python
MAX_ITERS, seen = 10, []
for i in range(MAX_ITERS):
    response = client.messages.create(
        model="claude-opus-4-8", max_tokens=1024,
        tools=tools, messages=messages)
    if response.stop_reason != "tool_use":
        break
    calls = [(b.name, str(b.input)) for b in response.content if b.type == "tool_use"]
    if calls and calls == seen[-1:]:          # same call as last time
        raise RuntimeError("stagnation: repeating tool call")
    seen.append(calls)
    # ... run tools, append results ...
else:
    raise RuntimeError("hit iteration cap")
```

## Failure 2: wrong tool selection

Claude chooses tools from their **descriptions**. If two tools overlap (`search` and `lookup`), if a description is vague ("gets data"), or if there are simply too many tools, the model's choice becomes a coin flip. The fixes are all about clarity:

- **Write prescriptive descriptions** — say *when* to call the tool, not just what it does: "Call this when the user asks about current order status."
- **Use enums** for fixed-value parameters so the model can't invent an invalid argument.
- **Trim the tool set** — fewer, sharper tools beat a sprawling menu. If you have a large library, tool search loads only the relevant schemas per request.
- **Force a tool** when you know which one is needed: `tool_choice` set to that specific tool.

Wrong tool selection is usually a prompt-and-schema problem, not a model problem.

## Failure 3: context bloat

The Messages API is **stateless** — every turn re-sends the entire conversation. In a long agent run, each tool result is appended and re-sent forever, so the context grows without bound. The costs are real: higher token spend, higher latency, and — worst — the *signal-to-noise ratio drops*, so the information that matters gets buried under stale tool output.

Detect it by watching `usage` on each response; if input tokens climb every turn, you're bloating. Control it with:

- **Context editing** — automatically clear old tool results and thinking blocks once they're no longer relevant.
- **Compaction** — summarise earlier context into a compact block as you approach the window limit.
- **Prompt caching** — cache the stable prefix so the unchanging part is cheap to re-send (a cost guard, not a size guard).

## Make failures visible

None of these guardrails help if you can't see the failure coming. Log, on every iteration: the iteration number, the tool calls made, cumulative tokens from `usage`, and the `stop_reason`. That single log line turns a mysterious runaway into an obvious one — the same way good pipeline logs turn a hung build into a five-second diagnosis.

## Your task

Take your Lesson 1 weather agent and write, in pseudocode, the three guards: an iteration cap, a stagnation check that breaks on a repeated identical tool call, and a per-iteration log line showing iteration number, tool calls, cumulative tokens, and stop_reason.
