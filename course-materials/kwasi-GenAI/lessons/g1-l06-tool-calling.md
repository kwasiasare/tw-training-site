---
course: kwasi-GenAI
title: Tool (function) calling
month: 1
monthTitle: LLM Foundations & API Fluency
lesson: 6
summary: Give a model the ability to call your code. Define a tool with a JSON schema, handle the tool_use
  request, execute the function, and return a tool_result so the model can finish its answer.
objectives:
- Define a tool with a name, description, and input schema
- Recognise a tool_use block and a stop_reason of tool_use
- Execute the requested tool with the model's supplied input
- Return a tool_result block tied to the matching tool_use id
- Loop the conversation until the model produces a final answer
- Explain why tool calling is the foundation of agents
video: g1-l06-tool-calling.mp4
quiz:
- q: What does a tool definition contain?
  options:
  - Only a name
  - A name, a description, and an input_schema (JSON schema)
  - The function's source code
  - A URL to call
  answer: 1
  why: A tool is declared with a name, a description that tells the model when to use it, and an input_schema
    describing the parameters — the model never sees your code.
- q: When the model wants to use a tool, what signals it?
  options:
  - The response is empty
  - stop_reason is 'tool_use' and the content includes a tool_use block
  - The temperature changes
  - You receive an error
  answer: 1
  why: The model returns stop_reason 'tool_use' along with one or more tool_use blocks naming the tool
    and the input it wants you to run.
- q: Who actually executes the tool?
  options:
  - Anthropic's servers
  - Your code — you run the function and return the result
  - The model, internally
  - A separate billing service
  answer: 1
  why: For user-defined tools, the model only requests the call; your application executes the function
    and sends the result back.
- q: How must a tool_result be linked to the request?
  options:
  - By timestamp
  - By the tool_use_id matching the originating tool_use block
  - By tool name only
  - It does not need linking
  answer: 1
  why: Each tool_result carries the tool_use_id of the tool_use block it answers, so the model knows which
    call the result belongs to.
- q: In one sentence, describe the tool-use loop.
  answer: The model asks for a tool, you execute it and send back a tool_result, then you call the model
    again, repeating until stop_reason is end_turn and the model gives its final answer.
  why: Tool calling is an iterative loop of request, execute, return, and re-call until the model is done.
- q: Why is tool calling the foundation of agents?
  answer: Because it lets the model take real actions and pull in real data through your code, turning
    a text generator into something that can do work in the world.
  why: Agents are tool-using loops; mastering the raw tool_use to tool_result cycle is the core skill
    every agent framework builds on.
resources:
- label: Anthropic — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Anthropic — Implement tool use
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
- label: Anthropic — Handling stop reasons
  url: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- label: Anthropic — Python SDK tool examples
  url: https://github.com/anthropics/anthropic-sdk-python
---

## Letting the model call your code

In lesson two you saw that models are weak at math and stuck behind a knowledge cutoff. **Tool calling** is the cure. You give the model a set of functions it may ask you to run — a calculator, a database lookup, a weather API — and when it needs one, it requests the call. *You* run the function and hand back the result, and the model uses it to finish its answer.

The critical detail: the model never executes anything itself. It only asks. Your code stays in control of what actually runs — which, for a security-minded engineer, is exactly the right boundary. This is the raw mechanism every agent framework is built on, so learn it here, directly.

## Defining a tool

A tool is a JSON object with three parts: a `name`, a `description` (the model reads this to decide *when* to use the tool — be clear and specific), and an `input_schema` describing the parameters as JSON schema.

```python
tools = [{
    "name": "get_weather",
    "description": "Get the current weather for a city. Use when the user asks about weather.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "City name"}},
        "required": ["city"],
    },
}]
```

Notice there is no code here — just a contract. The model decides whether and how to call it.

## The tool_use → tool_result loop

You pass `tools` with your request. If the model decides to use one, the response comes back with `stop_reason: "tool_use"` and a `tool_use` block naming the tool, an `id`, and the `input` it wants.

```python
messages = [{"role": "user", "content": "What's the weather in Paris?"}]
response = client.messages.create(
    model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages,
)

if response.stop_reason == "tool_use":
    # 1. Append the assistant's turn (it contains the tool_use block)
    messages.append({"role": "assistant", "content": response.content})
    for block in response.content:
        if block.type == "tool_use":
            # 2. Execute the tool yourself
            result = get_weather(**block.input)   # your real function
            # 3. Return a tool_result tied to the tool_use id
            messages.append({"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            }]})
    # 4. Call the model again so it can use the result
    response = client.messages.create(
        model="claude-opus-4-8", max_tokens=1024, tools=tools, messages=messages,
    )
```

Three rules make this work: append the assistant's `tool_use` content to history, match each `tool_result` to its `tool_use_id`, and then **call the model again**. You repeat the cycle until `stop_reason` is `end_turn` — that is the model's final answer.

## The loop is the whole idea

That request → execute → return → re-call cycle *is* an agent. Wrap it in a `while` loop and the model can chain several tools to complete a task: look up an order, check inventory, then summarise. Each pass, you stay in control — you can log, validate, or require human approval before running anything dangerous. (Your CI/CD instinct for human-in-the-loop approvals maps perfectly onto gating a risky tool call.) The SDKs offer a "tool runner" that automates the loop, but you should understand the manual version first so the automation is never a black box.

## Why it changes everything

With tool calling, a model stops being a text generator and starts being something that can *act*: do exact math, fetch fresh data, hit your internal APIs. Every mitigation from lesson two — grounding, recency, calculation — is delivered through this one mechanism. It is the single most important pattern in the course, and the deliverable you build next puts it to work.

## Your task

Define one simple tool (for example an `add` calculator or a fake `lookup_status` function), send a prompt that should trigger it, detect the `tool_use` block, execute your function, return a `tool_result` with the matching id, and call the model again to get the final answer.
