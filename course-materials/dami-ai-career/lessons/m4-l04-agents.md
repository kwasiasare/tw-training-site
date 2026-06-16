---
course: dami-ai-career
title: Agents & multi-step workflows
month: 4
monthTitle: Portfolio Projects
lesson: 4
summary: Build agents that loop — calling tools, reading results, and deciding the next step until a multi-step
  task is done.
objectives:
- Explain what an LLM agent is and how it differs from a single prompt
- Define tools the model can call, with names, descriptions, and input schemas
- 'Run the agentic loop: call, read tool_use, execute, feed results back'
- Use the Anthropic tool runner to handle the loop for you
- Decide when a simple workflow beats a full agent
- 'Add guardrails: step limits, error handling, and human approval for risky actions'
video: m4-l04-agents.mp4
quiz:
- q: What makes an agent different from a single LLM call?
  options:
  - It uses a bigger model
  - It loops — calling tools and deciding the next step until done
  - It always streams output
  - It never makes mistakes
  answer: 1
  why: 'An agent runs a loop: the model picks an action (often a tool), you run it, feed the result back,
    and it decides what to do next.'
- q: When Claude wants to call a tool, what is the stop_reason on the response?
  options:
  - end_turn
  - max_tokens
  - tool_use
  - refusal
  answer: 2
  why: stop_reason becomes "tool_use". You execute the tool, return a tool_result, and call the API again
    to continue.
- q: In a tool definition, what does input_schema describe?
  options:
  - The model's system prompt
  - The JSON shape of the arguments the tool expects
  - The order tools run in
  - The API key
  answer: 1
  why: input_schema is JSON Schema describing the tool's parameters, so the model knows exactly what arguments
    to supply.
- q: Why prefer a fixed workflow over an open-ended agent when you can?
  answer: A workflow is more predictable, cheaper, faster, and easier to debug; reach for an agent only
    when the path can't be fully specified in advance.
  why: Agents add cost and latency and are harder to reason about. Use the simplest tier that solves the
    task.
- q: Name one guardrail you should add to an agentic loop.
  answer: A maximum step (iteration) limit, error handling on tool calls, or human approval before irreversible
    actions.
  why: Without limits an agent can loop forever or take harmful actions; bounds and approval gates keep
    it safe.
resources:
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/engineering/building-effective-agents
- label: Anthropic docs — Tool use overview
  url: https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
- label: Anthropic Python SDK (anthropic) on GitHub
  url: https://github.com/anthropics/anthropic-sdk-python
- label: Anthropic Quickstarts — agent examples
  url: https://github.com/anthropics/anthropic-quickstarts
---

## What is an agent?

Up to now you've sent one prompt and read one reply. An **agent** does more: it runs a **loop**. The model decides on an action — usually calling a **tool** — you run that action, hand the result back, and the model decides what to do next. It keeps going until the task is finished.

Think of it like long division. You don't solve it in one step; you repeat *estimate, multiply, subtract, bring down* until there's nothing left. An agent repeats *think, act, observe* the same way.

## Tools: giving the model hands

A **tool** is a function the model is allowed to call. You describe it with a name, a plain-English description, and an `input_schema` (JSON Schema) for its arguments. The model never runs your code — it just *asks* to, and your program does the running.

```python
tools = [{
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
    }
}]
```

## The agentic loop

When the model wants a tool, the response comes back with `stop_reason == "tool_use"`. You execute the tool, append a `tool_result`, and call the API again. Repeat until `stop_reason == "end_turn"`.

```python
from anthropic import Anthropic
client = Anthropic()
messages = [{"role": "user", "content": "Weather in Lagos?"}]
while True:
    resp = client.messages.create(model="claude-sonnet-4-6",
        max_tokens=1024, tools=tools, messages=messages)
    if resp.stop_reason != "tool_use":
        break
    messages.append({"role": "assistant", "content": resp.content})
    results = []
    for b in resp.content:
        if b.type == "tool_use":
            out = run_tool(b.name, b.input)   # your code
            results.append({"type": "tool_result",
                "tool_use_id": b.id, "content": out})
    messages.append({"role": "user", "content": results})
```

## Let the SDK run the loop

Writing that loop by hand is good for understanding. In practice the SDK's **tool runner** does it for you — you define tools as typed functions and iterate the results.

## Workflow vs agent

Not everything needs an agent. If you can write the steps down in advance — *extract, then summarise, then email* — that's a **workflow**, and a workflow is cheaper, faster, and far easier to debug. Reach for a full agent only when the path genuinely can't be planned ahead.

## Guardrails

An unbounded loop can spin forever or do something irreversible. Always add a **step limit**, handle tool errors gracefully, and require **human approval** before risky actions like sending money or deleting data.

## Your task

Build a tiny two-tool agent (e.g. a calculator and a search stub) and watch the loop call them in turn.
