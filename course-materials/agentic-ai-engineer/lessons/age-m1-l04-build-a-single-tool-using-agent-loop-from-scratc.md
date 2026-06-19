---
course: agentic-ai-engineer
title: Build a Single Tool-Using Agent Loop from Scratch
month: 1
monthTitle: LLM Foundations and Tool-Using Agents
lesson: 4
summary: Learn to build a complete observe-think-act agent loop from scratch, where an LLM selects tools,
  executes them, observes results, and iterates until a task is solved—without relying on heavyweight
  frameworks.
objectives:
- Explain the observe-think-act loop and how it enables iterative problem solving in LLM agents
- Design a tool interface (name, description, JSON schema, callable) that an LLM can reliably invoke
- Implement a control loop that parses model output, dispatches tool calls, and feeds observations back
  into context
- Add termination conditions, step limits, and error handling to keep the loop safe and bounded
- Trace and debug a running agent by inspecting the prompt, tool calls, and observations at each step
video: age-m1-l04-build-a-single-tool-using-agent-loop-from-scratc.mp4
quiz:
- q: In the observe-think-act loop, what does the 'observe' step do?
  options:
  - It asks the model to generate its final answer
  - It captures the tool's output and adds it back to the conversation
  - It validates the JSON schema of the tool parameters
  - It increments the step counter to enforce limits
  answer: 1
  why: Observe means capturing the result of the executed tool and feeding it back into the model's context
    so it can decide the next step.
- q: Which tool field most directly determines whether the model chooses the right tool?
  options:
  - The name
  - The description
  - The return type
  - The step limit
  answer: 1
  why: The description acts like a mini-prompt telling the model when the tool should be used; vague descriptions
    lead to wrong or missed tool selection.
- q: Why is max_steps important in an agent loop?
  options:
  - It improves the quality of the model's reasoning
  - It prevents the loop from running forever if the model gets stuck
  - It is required by all LLM APIs
  - It removes the need for error handling
  answer: 1
  why: A hard step cap bounds the loop so a confused or looping model can't run indefinitely, controlling
    cost and risk.
- q: What is the recommended way to handle a tool that raises an exception during execution?
  options:
  - Crash the program so the developer notices
  - Silently ignore it and continue
  - Catch it and feed the error back as an observation so the model can recover
  - Retry the same call forever until it succeeds
  answer: 2
  why: Returning the error as an observation lets the model adjust its approach instead of crashing the
    whole agent.
- q: Name the pattern that interleaves reasoning traces with tool actions in an agent loop.
  answer: ReAct
  why: ReAct (Reasoning + Acting) describes interleaving the model's reasoning with tool actions and observations,
    which is exactly what the observe-think-act loop implements.
- q: In a text-protocol loop, what must your code do every iteration after the model replies?
  answer: Parse the reply to decide whether it's a tool call or a final answer (and then dispatch the
    tool or return).
  why: With a text protocol there's no structured field, so you parse the model's JSON output to distinguish
    a tool call from a final answer and act accordingly.
resources:
- label: 'ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)'
  url: https://arxiv.org/abs/2210.03629
- label: OpenAI Function/Tool Calling Guide
  url: https://platform.openai.com/docs/guides/function-calling
- label: Anthropic Tool Use Documentation
  url: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- label: LangChain Agents Conceptual Guide (for comparison with what frameworks hide)
  url: https://python.langchain.com/docs/concepts/agents/
---

## Why Build the Loop Yourself?

Frameworks like LangChain or the OpenAI Agents SDK hide a surprisingly small core: a loop that lets a language model *think*, *choose a tool*, *act*, and *observe the result*—repeating until the task is done. Building this loop from scratch makes you a far better agentic engineer because you understand exactly what the model sees, where failures happen, and how to control cost and safety.

## The Observe-Think-Act Loop

At its heart, an agent is a `while` loop around an LLM call:

1. **Think** – The model reads the task plus the history so far and decides what to do next.
2. **Act** – If the model requests a tool, we execute that tool with the model's arguments.
3. **Observe** – We capture the tool's output and append it to the conversation.
4. **Repeat** – The model now sees the observation and decides the next step.
5. **Finish** – When the model produces a final answer instead of a tool call, we exit.

This mirrors the **ReAct** pattern (Reasoning + Acting): interleaving reasoning traces with tool actions so the model can ground its decisions in real-world feedback.

## Anatomy of a Tool

A tool needs four things so the model can use it reliably:

- **name** – a short identifier (`search_web`, `calculator`).
- **description** – tells the model *when* to use it. This is the most important field; write it like a prompt.
- **parameters schema** – a JSON Schema describing the arguments. This lets you validate inputs.
- **callable** – the actual Python function that runs the work.

```python
tools = {
    "calculator": {
        "description": "Evaluate a math expression. Input: {\"expression\": \"2+2\"}",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]},
        "fn": lambda args: str(eval(args["expression"], {"__builtins__": {}}))
    }
}
```

## How the Model Signals a Tool Call

There are two common mechanisms:

- **Native function/tool calling** – Modern APIs return a structured `tool_calls` field. Preferred: no fragile parsing.
- **Text-protocol (prompted) calling** – You instruct the model to emit JSON like `{"action": "calculator", "action_input": {...}}` and you parse it. Useful for models without native support.

Either way, your loop must distinguish *"the model wants to call a tool"* from *"the model is giving a final answer."*

## A Minimal Loop (Text Protocol)

```python
import json

SYSTEM = '''You are an agent. To use a tool, respond with ONLY:
{"action": "<tool_name>", "action_input": {...}}
When you have the answer, respond with:
{"action": "final", "action_input": "<answer>"}
Available tools: calculator(expression).'''

def run_agent(task, llm, tools, max_steps=6):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": task}]
    for step in range(max_steps):
        reply = llm(messages)                 # call your model
        messages.append({"role": "assistant", "content": reply})
        try:
            call = json.loads(reply)
        except json.JSONDecodeError:
            return "Error: model did not return valid JSON"
        if call["action"] == "final":
            return call["action_input"]
        tool = tools.get(call["action"])
        if not tool:
            obs = f"Error: unknown tool {call['action']}"
        else:
            try:
                obs = tool["fn"](call["action_input"])
            except Exception as e:
                obs = f"Tool error: {e}"
        messages.append({"role": "user", "content": f"Observation: {obs}"})
    return "Stopped: reached max steps"
```

## Termination, Limits, and Safety

A production loop must never run forever or do something dangerous:

- **Step limit** (`max_steps`) – a hard cap so a confused model can't loop infinitely.
- **Final-answer detection** – an explicit `final` action is more reliable than guessing.
- **Tool error handling** – feed errors back as observations so the model can recover, rather than crashing.
- **Input validation** – validate arguments against the JSON schema before executing.
- **Sandboxing** – never `eval` untrusted input in production; use safe evaluators and least-privilege tools.

## Debugging the Loop

The single best habit: **log every step**—the messages sent, the raw model reply, the parsed tool call, and the observation. Most agent bugs are really *prompt* bugs (the model mis-formats output) or *tool* bugs (bad arguments). Seeing the full trace turns mysterious failures into obvious ones.

## Recap

You now have the irreducible core of an agent: a bounded loop that lets a model reason, call tools, observe results, and converge on an answer. Everything more advanced—multi-agent systems, planners, memory—builds on this exact pattern.
