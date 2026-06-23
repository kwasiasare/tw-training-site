---
course: agentic-ai-engineer
title: Defining and Wiring Tools with Function Calling
month: 1
monthTitle: LLM Foundations and Tool-Using Agents
lesson: 3
summary: Learn how to define tool schemas and wire external functions to an LLM using function calling,
  so the model can autonomously decide when and how to invoke tools like search, calculators, and API
  calls.
objectives:
- Explain how LLM function calling works and the request/response loop between model and tools
- Write valid JSON Schema definitions for tools, including parameters, types, and required fields
- Implement and register Python functions for search, calculation, and API calls
- Build the agent loop that parses tool calls, executes functions, and returns results to the model
- Apply best practices for tool descriptions, validation, and error handling in production
video: age-m1-l03-defining-and-wiring-tools-with-function-calling.mp4
quiz:
- q: In function calling, who actually executes the tool's code?
  options:
  - The LLM runs the code internally
  - Your application code executes it
  - The API provider's servers run it automatically
  - No code is executed; it's simulated
  answer: 1
  why: The model only proposes a structured tool call as JSON. Your application is responsible for executing
    the function, which keeps you in control for safety.
- q: Which field in a tool schema most influences whether the model selects the correct tool?
  options:
  - name
  - description
  - required
  - type
  answer: 1
  why: The description tells the model when and why to use the tool, so a clear, specific description
    is the biggest driver of correct tool selection.
- q: What format do function-call arguments arrive in from the model?
  options:
  - A Python dictionary
  - A JSON-encoded string that must be parsed
  - An XML document
  - A list of positional values
  answer: 1
  why: Arguments come as a JSON string (e.g. in call.function.arguments), so you must json.loads them
    into a dict before calling the function.
- q: Why should you set a maximum iteration count on the agent loop?
  options:
  - To reduce token cost only
  - To prevent infinite or runaway tool-calling loops
  - Because the API requires it
  - To improve description quality
  answer: 1
  why: Without a cap, a model could keep requesting tools indefinitely; a max iteration count is a safety
    guard against runaway loops.
- q: When a tool fails, what is the recommended way to handle it so the agent can recover?
  answer: Return a clear error message as the tool result string so the model can read it and retry or
    adjust, instead of crashing the program.
  why: Returning a descriptive error as the tool result lets the model reason about the failure and choose
    an alternative path.
- q: What two messages must be appended to the conversation for each tool call before re-invoking the
    model?
  answer: The assistant's tool-call message and a matching tool-role message containing the result with
    the same tool_call_id.
  why: Both are required to maintain valid conversation structure; omitting the assistant message is a
    common bug.
resources:
- label: OpenAI Function Calling Guide
  url: https://platform.openai.com/docs/guides/function-calling
- label: JSON Schema Official Documentation
  url: https://json-schema.org/learn/getting-started-step-by-step
- label: Anthropic Tool Use Documentation
  url: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- label: LangChain Tools Concepts
  url: https://python.langchain.com/docs/concepts/tools/
---

## Why Function Calling Matters

Large language models are excellent at reasoning over text but cannot natively fetch live data, do reliable arithmetic, or take real actions. **Function calling** (also called tool calling) bridges that gap: you describe a set of functions to the model, and the model can choose to emit a structured request to invoke one of them. Your code executes the function and feeds the result back, letting the model continue its reasoning with fresh, grounded information.

Crucially, the model never runs your code. It only *proposes* a call as structured JSON. Your application is always in control of execution, which is the foundation of safe, production-ready agents.

## The Function Calling Loop

1. **Define tools** as schemas (name, description, parameters).
2. **Send** the user message plus the tool definitions to the model.
3. The model responds either with a normal text answer **or** with one or more `tool_calls` containing a function name and JSON arguments.
4. **Execute** the requested function(s) in your code.
5. **Append** the tool result to the conversation and call the model again.
6. The model uses the result to produce a final answer (or request another tool).

This loop may run several times for multi-step tasks.

## Anatomy of a Tool Schema

A tool is described with JSON Schema. Key fields:

- `name`: a short, unique, snake_case identifier.
- `description`: tells the model *when* and *why* to use the tool. This is the single most important field for good tool selection.
- `parameters`: a JSON Schema object with `properties`, `type`, and `required`.

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the current weather for a city. Use when the user asks about temperature or conditions.",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {"type": "string", "description": "City name, e.g. 'Paris'"},
        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
      },
      "required": ["city"]
    }
  }
}
```

## Wiring Functions in Python

Keep a registry mapping tool names to the actual Python callables.

Tool arguments here are **model-generated**, which means they are untrusted. A tempting shortcut is `eval(expression, {"__builtins__": {}}, {})`, but **restricting `__builtins__` is not a sandbox**: well-documented bypasses recover dangerous callables by walking Python's object graph (e.g. via `().__class__.__base__.__subclasses__()`), so a crafted expression can still read files or run commands. This is exactly the rule the Best Practices section states — *never `eval` untrusted input*. The safe approach for arithmetic is to parse the expression with `ast` and walk the tree, allowing **only** a whitelist of arithmetic nodes. For richer, code-running tools, use a real sandbox (E2B, Modal, or a locked-down container) instead of `eval`.

```python
import ast
import json
import operator

# Only these binary/unary operators are permitted.
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        # Pow (**) is intentionally excluded to avoid compute DoS (e.g. 9**9**9).
        return _BIN_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

def calculator(expression: str) -> str:
    # Safe arithmetic evaluation: parse + whitelist, never eval().
    tree = ast.parse(expression, mode="eval")
    return str(_safe_eval(tree))

def web_search(query: str) -> str:
    # Call your real search API here
    return f"Top results for {query}..."

TOOLS = {"calculator": calculator, "web_search": web_search}
```

The parser accepts numbers, `+ - * / // %`, unary `+/-`, and parentheses, and raises a clear `ValueError` on anything else (function calls, attribute access, names, or `**`). Because the grammar contains no way to reach an object or builtin, there is nothing to bypass.

## The Agent Loop in Code

```python
from openai import OpenAI
client = OpenAI()

messages = [{"role": "user", "content": "What is 1234 * 5678?"}]

while True:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tool_schemas,
    )
    msg = resp.choices[0].message
    messages.append(msg)

    if not msg.tool_calls:
        print(msg.content)  # final answer
        break

    for call in msg.tool_calls:
        fn = TOOLS[call.function.name]
        args = json.loads(call.function.arguments)
        result = fn(**args)
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": str(result),
        })
```

Note that you must append both the assistant's tool-call message **and** a matching `tool` message (with the same `tool_call_id`) for each call before re-invoking the model.

## Best Practices

- **Write descriptions for the model, not humans.** State exactly when to use the tool and what each parameter means.
- **Validate arguments** before executing. The model can hallucinate or omit fields; never trust JSON blindly.
- **Handle errors gracefully.** Return a clear error string as the tool result so the model can recover or retry rather than crashing.
- **Keep tools small and focused.** One job per tool yields better selection accuracy.
- **Limit the number of tools** per request (typically under ~20) to avoid confusing the model.
- **Never `eval` untrusted input** — tool arguments are model-generated and untrusted. Restricting `__builtins__` does *not* make `eval` safe (the object graph leaks dangerous callables). Parse arithmetic with an `ast` whitelist; for arbitrary code use a real sandbox (E2B, Modal, locked-down container).
- **Set a max iteration count** on the loop to prevent infinite tool-calling loops.

## Common Pitfalls

- Forgetting to append the assistant message before the tool result, breaking the conversation structure.
- Vague descriptions causing the model to pick the wrong tool or none at all.
- Not parsing `arguments` (they arrive as a JSON *string*, not a dict).
- Returning non-string tool results — always serialize.
