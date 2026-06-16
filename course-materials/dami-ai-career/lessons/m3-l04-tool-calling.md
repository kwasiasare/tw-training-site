---
course: dami-ai-career
title: Tool / function calling
month: 3
monthTitle: LLM Application Skills
lesson: 4
summary: Give an LLM typed tools it can call, run them in your code, and feed the results back to finish
  the task.
objectives:
- Explain why tool calling lets an LLM act, not just talk
- Define a tool with a name, description, and JSON Schema input
- Pass tools to the Claude Messages API and read a tool_use block
- Execute the requested tool in your own code and return a tool_result
- Loop on the stop_reason until Claude finishes (the agentic loop)
- Handle tool errors and force a specific tool with tool_choice
video: m3-l04-tool-calling.mp4
quiz:
- q: In tool calling, who actually runs the tool's code?
  options:
  - The LLM, internally
  - Your application code
  - Anthropic's servers, always
  - The JSON Schema
  answer: 1
  why: For user-defined tools the model only requests the call; your code executes it and returns the
    result. (Server-side tools like web search are the exception.)
- q: What field tells you Claude wants to call a tool instead of finishing?
  options:
  - end_turn
  - max_tokens
  - tool_use
  - refusal
  answer: 2
  why: When response.stop_reason is "tool_use", the content contains a tool_use block you must execute
    and respond to.
- q: What does a tool definition need at minimum?
  answer: A name, a description, and an input_schema (JSON Schema describing the inputs).
  why: Claude reads the description and schema to decide when to call the tool and how to shape the arguments.
- q: When you send a tool result back, what must it reference?
  options:
  - The tool's name
  - The matching tool_use_id
  - The model id
  - The system prompt
  answer: 1
  why: Each tool_result must carry the same tool_use_id as the tool_use block, so Claude pairs the answer
    with its request.
- q: How do you signal that a tool call failed?
  answer: Return the tool_result with is_error set to true and an informative message.
  why: Claude sees the error and can retry differently or ask for clarification instead of assuming success.
- q: Why parse tool inputs with json.loads rather than string matching?
  options:
  - It is faster
  - Escaping can vary, so only a real JSON parse is reliable
  - It avoids API calls
  - string matching is not allowed
  answer: 1
  why: Models may escape Unicode or slashes differently in the input field; parse the JSON instead of
    matching raw text.
resources:
- label: Anthropic docs - Tool use (function calling) overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Anthropic docs - Implement tool use
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
- label: JSON Schema - Understanding JSON Schema (official guide)
  url: https://json-schema.org/understanding-json-schema
- label: Anthropic Python SDK (GitHub)
  url: https://github.com/anthropics/anthropic-sdk-python
---

## Why tool calling?

An LLM on its own can only produce text. It cannot look up today's weather, query your database, or send an email. **Tool calling** (also called **function calling**) closes that gap: you describe some functions to the model, and when it needs one, it asks you to run it and tell it the result.

Think of it like a function in maths. You hand the model a signature - a name and the shape of its inputs - and it decides *when* to call it and *with what arguments*. Your code computes the output and hands it back.

## How the conversation flows

The key idea: **the model never runs your code**. It only *requests* a call. The loop is:

1. You send a message plus a list of tools.
2. Claude replies. If `stop_reason` is `"tool_use"`, the reply contains a `tool_use` block with a tool name and JSON inputs.
3. Your code runs that tool and sends back a `tool_result` with the matching `tool_use_id`.
4. Claude reads the result and either answers or calls another tool. You repeat until `stop_reason` is `"end_turn"`.

## Defining a tool

A tool is a **name**, a **description**, and an **input_schema** written as JSON Schema. The description matters a lot - Claude uses it to decide when the tool applies, so say *when* to call it, not just what it does.

```python
weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather for a city. Call this whenever the user asks about weather.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. London"}
        },
        "required": ["city"],
    },
}
```

## The agentic loop

Here is the full round trip with the Claude Messages API. We keep looping until Claude stops asking for tools.

```python
import json
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

def get_weather(city):
    return f"18 degrees and cloudy in {city}"

messages = [{"role": "user", "content": "What's the weather in London?"}]

while True:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=[weather_tool],
        messages=messages,
    )
    if resp.stop_reason != "tool_use":
        break
    messages.append({"role": "assistant", "content": resp.content})
    results = []
    for block in resp.content:
        if block.type == "tool_use":
            out = get_weather(**block.input)  # block.input is already parsed JSON
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": out,
            })
    messages.append({"role": "user", "content": results})

print(next(b.text for b in resp.content if b.type == "text"))
```

## Errors and forcing a tool

If a tool fails, do not crash - return the result with `is_error` set to `true` and a clear message, so Claude can adapt. And if you need to *guarantee* a specific tool gets used, set `tool_choice`.

```python
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=[weather_tool],
    tool_choice={"type": "tool", "name": "get_weather"},
    messages=[{"role": "user", "content": "London weather?"}],
)
```

## Your task

Write a tool called `calculate` that takes a maths expression and returns the answer, wire it into the loop above, and ask Claude a word problem that forces it to call your tool.
