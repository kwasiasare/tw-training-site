---
course: ai-app-developer-2026
title: Introduction to LLM Agents and Tool Use
month: 3
monthTitle: Agents, Tools, and APIs
lesson: 1
summary: 'This lesson introduces LLM agents: systems that use a language model to reason, plan, and call
  external tools to complete multi-step tasks autonomously. You''ll learn the agent loop, how tool calling
  works, common agent patterns like ReAct, and practical considerations for building reliable agents.'
objectives:
- Explain what an LLM agent is and how it differs from a single LLM prompt
- Describe the agent reasoning loop (observe, think, act) and the ReAct pattern
- Define tools and write tool schemas the model can call
- Trace how an agent selects and invokes a tool, then incorporates results
- Identify common failure modes and guardrails for reliable agents
video: aad-m3-l01-introduction-to-llm-agents-and-tool-use.mp4
quiz:
- q: What best distinguishes an LLM agent from a single LLM prompt?
  options:
  - The agent uses a larger model
  - The agent runs the LLM in a loop that reasons, acts via tools, and repeats
  - The agent never produces text
  - The agent does not need any prompt
  answer: 1
  why: An agent wraps the model in an iterative loop that lets it choose actions, call tools, observe
    results, and continue until the goal is met—unlike a single one-shot prompt.
- q: In tool calling, who actually executes the tool/function?
  options:
  - The LLM runs the code internally
  - Your application code executes it and returns the result
  - The JSON schema executes itself
  - The user manually runs every call
  answer: 1
  why: The model only proposes a structured tool call with arguments; your application runs the function
    and feeds the result back. This separation is key for control and safety.
- q: What does the ReAct pattern interleave?
  options:
  - Requests and Acknowledgements
  - Reasoning (thoughts) and Acting (tool calls)
  - Retrieval and Caching
  - Rendering and Compiling
  answer: 1
  why: 'ReAct stands for Reasoning + Acting: the model alternates between reasoning thoughts and taking
    actions like tool calls, using observations to inform the next step.'
- q: Which is a sensible guardrail against runaway agent loops?
  options:
  - Remove all tools
  - Set a maximum number of iterations
  - Always trust tool outputs blindly
  - Disable logging
  answer: 1
  why: A max-iteration limit stops the agent from looping forever. Other guardrails include input validation,
    human approval, timeouts, and tracing.
- q: In one short sentence, why are clear tool names and descriptions important?
  answer: The model uses the names and descriptions to decide which tool to call, so clear ones lead to
    better tool selection.
  why: The agent selects tools based on their metadata; vague descriptions cause wrong or missed tool
    choices.
- q: Name one capability a tool can give an LLM that the model lacks on its own.
  answer: Access to live/real-time data (e.g., current weather or prices), reliable math, database queries,
    or taking actions like sending email.
  why: Tools fill gaps such as the knowledge cutoff, unreliable arithmetic, and inability to act in the
    real world.
resources:
- label: OpenAI Function Calling / Tools Guide
  url: https://platform.openai.com/docs/guides/function-calling
- label: 'ReAct: Synergizing Reasoning and Acting in Language Models (paper)'
  url: https://arxiv.org/abs/2210.03629
- label: LangChain Agents Documentation
  url: https://python.langchain.com/docs/concepts/agents/
- label: 'Anthropic: Building Effective Agents'
  url: https://www.anthropic.com/research/building-effective-agents
---

## What Is an LLM Agent?

A plain LLM call takes a prompt and returns text in one shot. An **agent** wraps the LLM in a loop that lets it *reason about a goal, decide on actions, call external tools, observe the results, and repeat* until the task is done.

The key shift: the model is no longer just generating an answer—it is **driving a process**. It chooses what to do next based on what it has learned so far.

## Why Agents?

LLMs alone are limited: they have a knowledge cutoff, can't do reliable math, can't fetch live data, and can't take real-world actions. **Tools** close these gaps.

- Need today's weather? Call a weather API.
- Need exact arithmetic? Call a calculator.
- Need company data? Query a database or search documents.
- Need to send an email or create a ticket? Call that service.

The agent decides *when* and *how* to use each tool.

## The Agent Loop

Most agents follow a cycle:

1. **Observe** – read the goal and any new information (tool outputs).
2. **Think** – reason about the next step (often hidden "scratchpad" text).
3. **Act** – either call a tool or produce a final answer.
4. **Repeat** until the model decides it is finished.

This is the basis of the **ReAct** pattern (Reasoning + Acting), where the model interleaves thoughts and actions.

```
Thought: I need the current price of BTC.
Action: get_price(symbol="BTC")
Observation: 64200
Thought: Now I can answer.
Final Answer: Bitcoin is about $64,200.
```

## How Tool Calling Works

Modern LLM APIs support **function/tool calling**. You give the model a list of tools, each described by a JSON schema (name, description, parameters). The model responds with a structured request to call a tool and the arguments it chose. Your code executes the function and feeds the result back.

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {"type": "string", "description": "City name"}
    },
    "required": ["city"]
  }
}
```

The model does **not** run the code—your application does. The model only proposes the call. This separation is critical for safety and control.

## A Minimal Agent in Pseudocode

```python
messages = [{"role": "user", "content": goal}]
while True:
    resp = llm.chat(messages, tools=tools)
    if resp.tool_call:
        result = run_tool(resp.tool_call.name, resp.tool_call.args)
        messages.append(resp.message)
        messages.append({"role": "tool", "content": result})
    else:
        return resp.content  # final answer
```

Notice the loop keeps appending the model's actions and the tool outputs to the conversation so the model has full context each turn.

## Designing Good Tools

- **Clear names and descriptions** – the model picks tools based on these.
- **Tight parameter schemas** – fewer, well-typed arguments reduce errors.
- **Small, composable tools** beat one giant do-everything tool.
- **Return concise, structured results** – trim noise so the model isn't overwhelmed.

## Failure Modes and Guardrails

Agents can loop forever, hallucinate tool arguments, or call tools with bad data. Practical safeguards:

- **Max-iteration limit** to stop runaway loops.
- **Input validation** before executing tool calls.
- **Human-in-the-loop approval** for risky actions (payments, deletes).
- **Timeouts and error handling** so a failed tool returns a usable message.
- **Logging/tracing** every thought, action, and observation for debugging.

## Putting It Together

An effective agent = a capable model + well-described tools + a controlled loop + guardrails. Start simple (one or two tools, a strict iteration cap), observe traces, then expand. In later lessons you'll connect real APIs and frameworks to build production agents.
