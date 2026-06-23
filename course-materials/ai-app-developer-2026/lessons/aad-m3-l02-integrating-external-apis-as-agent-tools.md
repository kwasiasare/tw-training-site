---
course: ai-app-developer-2026
title: Integrating External APIs as Agent Tools
month: 3
monthTitle: Agents, Tools, and APIs
lesson: 2
summary: Learn how to wrap external APIs—web search, calculators, and third-party services—as callable
  tools your LLM agent can invoke dynamically. You'll define tool schemas, implement handlers, handle
  errors and authentication securely, and orchestrate the tool-calling loop.
objectives:
- Explain how tool/function calling enables an LLM agent to invoke external code
- Define clear tool schemas (name, description, JSON parameters) that guide model selection
- Wrap a web search, calculator, and a third-party REST API as agent tools
- 'Implement the tool-calling loop: parse model output, execute, and return results'
- Apply security and reliability best practices including auth, timeouts, validation, and error handling
video: aad-m3-l02-integrating-external-apis-as-agent-tools.mp4
quiz:
- q: What is the single most important factor influencing whether the model picks the correct tool?
  options:
  - The tool's name length
  - The clarity of the tool's description
  - The number of parameters
  - The order tools appear in the list
  answer: 1
  why: The model reads each tool's natural-language description to decide when and whether to use it,
    so clear, specific descriptions are the primary driver of correct tool selection.
- q: Why should you avoid using raw eval() in a calculator tool?
  options:
  - It is slower than AST parsing
  - It can execute arbitrary, malicious code from model-generated strings
  - It cannot handle decimals
  - It is deprecated in Python 3
  answer: 1
  why: Model-generated input is untrusted; raw eval() can run arbitrary code, creating a serious security
    vulnerability. Parsing a restricted AST limits execution to safe arithmetic.
- q: In the tool-calling loop, what role is used for the message containing a tool's execution result?
  options:
  - user
  - system
  - tool
  - assistant
  answer: 2
  why: Tool results are appended as messages with the 'tool' role (linked by tool_call_id) so the model
    can read the output and continue reasoning.
- q: Why should you cap the number of iterations in the orchestration loop?
  options:
  - To reduce the model's accuracy
  - To prevent runaway or infinite tool-calling
  - To force the model to answer in one call
  - To save disk space
  answer: 1
  why: A confused agent could request tools indefinitely; an iteration cap prevents runaway loops that
    waste cost and time.
- q: Name one best practice for handling API keys when wrapping external APIs as tools.
  answer: Store them in environment variables instead of in code or the prompt
  why: Keeping secrets in environment variables (not hard-coded or embedded in prompts) prevents accidental
    exposure and keeps credentials out of logs and version control.
- q: What are the three core components of a tool schema?
  answer: name, description, and parameters (JSON Schema)
  why: Every tool definition needs a unique name, a description telling the model what it does and when
    to use it, and a parameters JSON Schema describing the arguments.
resources:
- label: OpenAI Function/Tool Calling Guide
  url: https://platform.openai.com/docs/guides/function-calling
- label: Anthropic Tool Use Documentation
  url: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- label: Tavily Search API (LLM-friendly web search)
  url: https://docs.tavily.com/
- label: JSON Schema Reference
  url: https://json-schema.org/learn/getting-started-step-by-step
---

## Why Tools Matter

An LLM on its own is a text predictor frozen at its training cutoff. It can't look up today's news, run exact arithmetic reliably, or query your company's database. **Tools** close this gap by letting the model call external functions and APIs at runtime. The agent decides *when* to call a tool, *which* tool, and *with what arguments*—then incorporates the result into its reasoning.

## How Tool Calling Works

Modern LLM APIs (OpenAI, Anthropic, etc.) support structured tool/function calling:

1. You send the user message **plus a list of tool definitions** (schemas).
2. The model responds either with a normal answer **or** a structured request to call a tool, including arguments as JSON.
3. Your code executes the tool and sends the result back to the model.
4. The model uses the result to produce a final answer—or calls another tool.

This is a loop, not a single round trip. The agent may chain several tool calls.

## Anatomy of a Tool Definition

A tool schema has three critical parts:

- **name** — a short, unique identifier (e.g. `web_search`).
- **description** — natural-language explanation of *what it does and when to use it*. This is what the model reads to decide. Write it carefully.
- **parameters** — a JSON Schema describing the arguments, their types, and which are required.

The OpenAI Chat Completions API wraps each tool as `{"type": "function", "function": {...}}`, with the `name`, `description`, and `parameters` nested inside `function`:

```json
{
  "type": "function",
  "function": {
    "name": "web_search",
    "description": "Search the web for current information. Use when the user asks about recent events or facts you don't know.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {"type": "string", "description": "The search query"}
      },
      "required": ["query"]
    }
  }
}
```

## Wrapping Three Common Tools

### 1. Calculator
LLMs are unreliable at exact math. Delegate to code:

```python
def calculator(expression: str) -> str:
    import ast, operator as op
    # Safe eval: only allow arithmetic nodes
    allowed = {ast.Add: op.add, ast.Sub: op.sub,
               ast.Mult: op.mul, ast.Div: op.truediv,
               ast.Pow: op.pow, ast.USub: op.neg}
    # Cap exponentiation: even a "safe" AST evaluator must bound Pow, or a
    # model-generated expression like 9**9**9 will hang/OOM the process (DoS).
    MAX_EXP = 100
    def ev(node):
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, ast.BinOp):
            left, right = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Pow) and (abs(right) > MAX_EXP or abs(left) > 1e6):
                raise ValueError("exponent or base too large")
            return allowed[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp): return allowed[type(node.op)](ev(node.operand))
        raise ValueError("unsupported")
    return str(ev(ast.parse(expression, mode='eval').body))
```
Never use raw `eval()` on model-generated strings.

### 2. Web Search
Call a search provider (Tavily, Bing, SerpAPI) and return concise results:

```python
import requests, os

def web_search(query: str) -> str:
    resp = requests.post(
        "https://api.tavily.com/search",
        json={"api_key": os.environ["TAVILY_API_KEY"], "query": query, "max_results": 3},
        timeout=10,
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])
    return "\n".join(f"{r['title']}: {r['content'][:200]}" for r in results)
```

### 3. Third-Party REST API (e.g. weather)
Wrap any REST endpoint the same way—translate model arguments into an HTTP request and the response into a clean string.

## The Orchestration Loop

```python
from openai import OpenAI
import json

client = OpenAI()
tools = [...]  # your schemas
handlers = {"calculator": calculator, "web_search": web_search}

def run_agent(user_msg: str, max_iters: int = 5):
    messages = [{"role": "user", "content": user_msg}]
    for _ in range(max_iters):  # cap iterations to avoid runaway tool-calling
        resp = client.chat.completions.create(
            model="gpt-4o", messages=messages, tools=tools)
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content  # final answer
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = handlers[call.function.name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })
    return "Stopped: reached the maximum number of tool-calling iterations."
```

Always cap the loop (e.g. max 5 iterations) to avoid infinite tool-calling.

## Security & Reliability Best Practices

- **Validate arguments** against the schema before executing—models can hallucinate malformed input.
- **Store API keys in environment variables**, never in code or the prompt.
- **Set timeouts** on every network call and handle failures gracefully; return an error string the model can reason about.
- **Limit scope**: give each tool the minimum permissions it needs (read-only where possible).
- **Sanitize outputs** before passing back—truncate large payloads to control token cost.
- **Add a loop guard** to prevent runaway tool-calling.
- **Log tool calls** for debugging and auditing.

## Writing Good Tool Descriptions

The model's tool choice quality depends almost entirely on your descriptions. Be specific about *when* to use the tool and what each parameter means. Vague descriptions cause wrong or missed tool calls.
