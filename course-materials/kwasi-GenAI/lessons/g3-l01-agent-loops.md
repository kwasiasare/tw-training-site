---
course: kwasi-GenAI
title: 'The agent loop: plan, act, observe, repeat'
month: 3
monthTitle: Agents & Orchestration
lesson: 1
summary: 'Understand what turns a single model call into an agent: a loop that plans, calls tools, observes
  results, and repeats until the task is done.'
objectives:
- Explain the difference between a single model call and an agent loop
- Describe the plan, act, observe, repeat cycle and what drives each step
- Identify the role of tools and the stop_reason field in continuing or ending the loop
- Trace a simple agentic loop in the Messages API by hand
- Decide when a task genuinely needs an agent versus a single call or a fixed workflow
- Recognise why bounding the loop matters before you ever run one
video: g3-l01-agent-loops.mp4
quiz:
- q: What is the core thing that makes an agent different from a single model call?
  options:
  - It uses a bigger model
  - 'It runs a loop: it acts, observes the result, and decides the next action'
  - It always streams its output
  - It never uses tools
  answer: 1
  why: An agent is defined by the loop — the model chooses an action, sees the result, and feeds that
    back to choose the next action, repeating until the task is complete.
- q: In the Messages API, which stop_reason tells your loop that Claude wants to call a tool?
  options:
  - end_turn
  - max_tokens
  - tool_use
  - stop_sequence
  answer: 2
  why: When stop_reason is tool_use, Claude has emitted a tool_use block; you execute the tool and feed
    the result back as a tool_result to continue the loop.
- q: After you run a tool, how do you return its output to Claude?
  options:
  - As a new system prompt
  - As a user message containing a tool_result block with the matching tool_use_id
  - By editing the assistant message in place
  - You don't — Claude already knows
  answer: 1
  why: Tool output goes back as a user-role message containing a tool_result block whose tool_use_id matches
    the tool_use block Claude emitted.
- q: In one sentence, what are the four phases of the classic agent loop?
  answer: Plan the next step, act by calling a tool, observe the tool's result, then repeat until the
    task is finished.
  why: Plan, act, observe, repeat is the heartbeat of every agent; the model reasons, takes an action,
    reads the outcome, and loops.
- q: Name one reason you should bound an agent loop with a maximum number of iterations.
  answer: Without a cap, a confused agent can loop forever — repeating the same failing tool call — burning
    tokens and money with no progress.
  why: Bounding iterations is the simplest safety rail against runaway loops, which we cover in depth
    later in the module.
- q: When should you NOT reach for an agent?
  answer: When the task is a single, well-specified step like classification or extraction — a single
    model call is cheaper, faster, and easier to reason about.
  why: Agents add cost, latency, and unpredictability; only use one when the task is genuinely multi-step
    and hard to fully specify in advance.
resources:
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
- label: Claude Docs — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Claude Docs — Handling stop reasons
  url: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- label: Claude Docs — Agents and tools
  url: https://platform.claude.com/docs/en/agents-and-tools/overview
---

## A single call versus a loop

Everything you built in the first two modules was a **single call**: you sent a prompt, Claude sent back an answer, done. That one round trip is perfect for classification, summarisation, extraction, and retrieval-augmented question answering. The model reasons over what you gave it and replies once.

An **agent** is different in exactly one way that matters: it runs a **loop**. The model doesn't just answer — it decides on an *action*, your code runs that action, the result comes back, and the model decides the *next* action based on what it just saw. It keeps going until the task is finished. That feedback cycle is the whole idea.

## Plan, act, observe, repeat

The loop has four phases, and they map cleanly onto things you already know from operations work:

- **Plan** — the model reasons about the goal and picks the next step. This is like deciding which command to run next in a debugging session.
- **Act** — the model emits a **tool call** (a `tool_use` block). Your harness executes it: a shell command, an API request, a database query.
- **Observe** — your code feeds the tool's output back to the model as a `tool_result`. Now the model can see what happened.
- **Repeat** — the model plans again with that new information, and the cycle continues until it has what it needs.

Think of it as a `while` loop where the model is the condition and the body.

## What drives the loop: stop_reason

The engine that turns this from theory into code is the `stop_reason` field on every Messages API response. When Claude wants to use a tool, it stops with `stop_reason` set to **`tool_use`**. When it's finished and ready to answer the user, it stops with **`end_turn`**. Your loop is simply: *keep going while the stop reason is tool_use*.

```python
import anthropic

client = anthropic.Anthropic()
messages = [{"role": "user", "content": "What is 23 times 47, then add 9?"}]

while True:
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=tools,            # your tool definitions
        messages=messages,
    )
    if response.stop_reason != "tool_use":
        break                  # end_turn: Claude is done

    # Append Claude's turn, run each tool, feed results back
    messages.append({"role": "assistant", "content": response.content})
    results = []
    for block in response.content:
        if block.type == "tool_use":
            output = run_tool(block.name, block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output,
            })
    messages.append({"role": "user", "content": results})
```

That's an agent. There is no magic — just a loop, a list of tools, and a stop condition. The SDK even ships a tool runner that hides this loop for you, but you should understand the manual version first, because the manual loop is where you put approval gates, logging, and safety bounds.

## Anthropic's Messages API in one breath

Everything goes through `messages.create`. Roles are `user` and `assistant`, with an optional top-level `system` prompt. Content is a list of **blocks**: text, `tool_use` (Claude asking to call a tool), and `tool_result` (you returning the answer). The default model in your examples should be the most capable one, **`claude-opus-4-8`**; reach for `claude-sonnet-4-6` when you want speed at scale. The same loop pattern runs unchanged on Amazon Bedrock and the cloud platforms you already operate in.

## When NOT to build an agent

Agents are powerful and also slower, costlier, and less predictable than a single call. Before you reach for one, ask: is the task genuinely multi-step and hard to specify up front? Can errors be caught and recovered? If the answer is "it's really just one extraction step," use a single call. If it's "turn this vague request into a finished result by exploring," that's agent territory.

## Your task

Write out, in plain English on paper, the plan-act-observe-repeat trace for an agent that answers "What's the current weather in the city where our main office is?" given two tools: `get_office_location()` and `get_weather(city)`. List each loop iteration, the tool called, and the `stop_reason` you'd expect.
