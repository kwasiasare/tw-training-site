---
course: kwasi-GenAI
title: 'Orchestration frameworks: accelerators, not crutches'
month: 3
monthTitle: Agents & Orchestration
lesson: 3
summary: See what LangChain and LlamaIndex give you and what they hide, so you can use a framework as
  an accelerator while still understanding the agent loop underneath.
objectives:
- List what orchestration frameworks like LangChain and LlamaIndex provide out of the box
- Explain what those frameworks abstract away and why that can hide bugs
- Map a framework agent back to the raw plan-act-observe loop underneath
- Decide when a framework earns its weight versus when raw SDK calls are clearer
- Avoid lock-in by keeping prompts, tools, and model choice under your control
- Debug a framework agent by inspecting the underlying API calls
video: g3-l03-orchestration-frameworks.mp4
quiz:
- q: What is the healthiest mental model for an orchestration framework?
  options:
  - A replacement for understanding the API
  - An accelerator that wraps the same loop you could write yourself
  - A required dependency for any agent
  - A model provider
  answer: 1
  why: Frameworks wrap the same plan-act-observe loop and the same Messages API; they accelerate you but
    don't replace understanding what's underneath.
- q: Which of these is something frameworks most usefully provide?
  options:
  - A faster model
  - 'Ready-made integrations: loaders, vector store adapters, tool wrappers, memory'
  - Lower token prices
  - Guaranteed correctness
  answer: 1
  why: Their real value is glue code — document loaders, retrievers, tool and memory abstractions — so
    you don't reinvent integrations.
- q: Why can a framework's abstraction hide bugs?
  options:
  - It encrypts your prompts
  - It can build the actual prompt and tool schema for you, so you may not see what's really sent to the
    model
  - It changes the model silently every call
  - It disables tools
  answer: 1
  why: When the framework assembles the prompt, the tool schema, and the loop, the exact bytes sent to
    the API are out of sight — so a bad prompt or wrong model is hard to spot.
- q: In one sentence, what should you always be able to do with a framework agent?
  answer: Map it back to the raw plan-act-observe loop and inspect the actual API request it sends.
  why: Keeping the underlying loop and request visible is how you debug, control cost, and avoid being
    trapped by the abstraction.
- q: Name one practical way to avoid framework lock-in.
  answer: Keep your prompts, tool definitions, and model choice as your own values that you pass in, rather
    than burying them inside framework defaults.
  why: Owning the prompt, tools, and model id means you can drop down to raw SDK calls or swap frameworks
    without rewriting your logic.
- q: When does reaching for a framework clearly NOT earn its weight?
  answer: For a simple single-call task or a short, fixed two-step loop, where the framework adds dependencies
    and indirection without saving real work.
  why: Frameworks pay off on integration-heavy apps; for a single call or a tiny loop, raw SDK code is
    shorter and clearer.
resources:
- label: LangChain — Documentation
  url: https://python.langchain.com/docs/introduction/
- label: LlamaIndex — Documentation
  url: https://docs.llamaindex.ai/en/stable/
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
- label: Claude Docs — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
---

## The honest framing

**LangChain** and **LlamaIndex** are orchestration frameworks: libraries that sit on top of the model API and hand you ready-made pieces for building agents and RAG apps. They are genuinely useful. They are also frequently misused as a substitute for understanding the loop you learned in Lesson 1. The goal of this lesson is to let you use one as an **accelerator** without it becoming a **crutch**.

The rule of thumb: a framework should never do anything you couldn't, in principle, write yourself with `messages.create`. When it does something you don't understand, that's a signal to look underneath, not to look away.

## What they give you

The real value is **glue code** you'd otherwise write by hand:

- **Loaders and connectors** — read PDFs, web pages, Notion, S3, databases into a common document shape.
- **Retrieval plumbing** — chunking, embedding, vector store adapters, and retrievers wired together (LlamaIndex is especially strong here).
- **Tool abstractions** — wrap a Python function as a tool the model can call, with the schema generated for you.
- **Memory and state** — buffers and stores for carrying conversation history across turns.
- **Prebuilt agents and chains** — a ReAct-style loop or a retrieval chain you can instantiate in a few lines.

For an integration-heavy application — many data sources, a vector store, conversation memory — this saves real, tedious work. That's the accelerator.

## What they hide

The same abstraction that saves typing also **hides the wire**. When the framework assembles your prompt, builds the tool JSON schema, runs the loop, and parses the response, the *exact bytes sent to the model* are out of your direct view. That matters because, as you saw in the RAG module, the prompt is the product. A framework default prompt that's vaguely worded, a tool description the model can't act on, or a silently chosen cheaper model can all degrade your app — and you won't see why, because the loop is behind a curtain.

The other thing they hide is the **loop itself**. A prebuilt agent is still plan-act-observe-repeat underneath — but if you've never written that loop, a runaway or a wrong tool selection looks like framework magic going wrong rather than a bounded, debuggable cycle.

## Mapping the framework back to the loop

Whenever you use a prebuilt agent, hold this picture in your head: the framework is calling `messages.create`, reading `stop_reason`, running the `tool_use` blocks, and feeding `tool_result` back — exactly the loop from Lesson 1. The skill is being able to drop down and **see the real request**. Every serious framework lets you turn on verbose or callback logging that prints the actual prompt and tool calls. Use it. If you can't see the request, you can't debug the agent.

```python
# Conceptual: a framework agent is still this loop underneath
# 1. messages.create(model=..., tools=..., messages=...)
# 2. if stop_reason == "tool_use": run tools, append tool_result
# 3. else: done
```

## Staying in control

Two habits keep a framework an accelerator rather than a trap. **First, own your inputs.** Pass in your own prompt text, your own tool definitions, and your own model id (`claude-opus-4-8` by default, `claude-sonnet-4-6` for scale) rather than relying on framework defaults you haven't read. **Second, keep an escape hatch.** Structure your code so the business logic — what the tools do, what the prompt says — lives in your code, and the framework is just wiring. Then you can swap the framework, or drop to raw SDK calls, without a rewrite. On Amazon Bedrock or Azure these same frameworks point at the cloud-hosted model with a different client, so owning your inputs keeps you portable across clouds too.

## When to skip the framework

For a single-call task or a short fixed loop, a framework is overhead: more dependencies, more indirection, more surface area for version churn. Write the raw loop. Reach for the framework when the *integration* burden is real — multiple loaders, a vector store, memory — and the glue code would otherwise be yours to maintain.

## Your task

Take the two-tool agent you traced in Lesson 1. In notes, describe how a LangChain or LlamaIndex agent would represent it — which framework piece wraps the tools, where the loop lives, and exactly where you would turn on logging to see the real `messages.create` request it sends.
