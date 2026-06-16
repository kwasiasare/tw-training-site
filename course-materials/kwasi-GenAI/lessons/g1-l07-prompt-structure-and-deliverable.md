---
course: kwasi-GenAI
title: Prompt structure & the deliverable
month: 1
monthTitle: LLM Foundations & API Fluency
lesson: 7
summary: 'Use the system and user roles deliberately and add few-shot examples to steer behaviour, then
  assemble everything from Module 1 into the deliverable: a tool-using API client that returns structured
  data.'
objectives:
- Use the system role for durable rules and the user role for the task
- Add few-shot examples to demonstrate the format and behaviour you want
- Explain why examples often beat longer instructions
- Combine tool use and structured output in one client
- Build a CLI / script that calls a model, uses a tool, and returns parseable data
- Connect every Module 1 concept into one working deliverable
video: g1-l07-prompt-structure-and-deliverable.mp4
quiz:
- q: What belongs in the system prompt versus the user message?
  options:
  - Everything goes in the user message
  - System holds durable rules and persona; the user message holds the specific task or input
  - System holds the task; user holds the rules
  - They are interchangeable
  answer: 1
  why: The system prompt sets stable behaviour and constraints for the whole exchange, while each user
    message carries the specific request or data.
- q: What is few-shot prompting?
  options:
  - Sending the request several times
  - Including a few example input/output pairs in the prompt to demonstrate the desired behaviour
  - Using a smaller model
  - Lowering max_tokens
  answer: 1
  why: Few-shot prompting shows the model worked examples of the format and behaviour you want, which
    it then imitates.
- q: Why do examples often beat longer instructions?
  options:
  - They use fewer tokens always
  - A concrete demonstration of the desired output is clearer to the model than abstract description
  - Instructions are ignored
  - Examples disable hallucination
  answer: 1
  why: Showing the exact shape and tone you want is usually less ambiguous than describing it in prose,
    so the model matches it more reliably.
- q: The Module 1 deliverable combines which two features most directly?
  options:
  - Streaming and caching
  - Tool use and structured output
  - Vision and batching
  - Fine-tuning and embeddings
  answer: 1
  why: The deliverable is a tool-using client that returns structured data, so it puts the tool_use loop
    and JSON-schema output together.
- q: In one sentence, what is the Module 1 deliverable?
  answer: A CLI or script that calls a model with a tool defined, runs the tool_use to tool_result loop,
    and returns reliable structured data the rest of a program can consume.
  why: It is the capstone that ties together the raw API, roles, tools, and structured output into one
    working client.
- q: Why build the deliverable on the raw API rather than a framework?
  answer: So you understand every step of the loop yourself — the request, the tool call, the result,
    the structured output — which makes any framework you adopt later transparent instead of magic.
  why: Mastering the raw mechanism first means later abstractions are something you can reason about and
    debug, not a black box.
resources:
- label: Anthropic — System prompts / Use system prompts
  url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/system-prompts
- label: Anthropic — Use examples (multishot prompting)
  url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting
- label: Anthropic — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Anthropic — Structured outputs
  url: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
---

## Two roles, used on purpose

You met the `system` prompt and the `user` role in lesson three. Now use them deliberately. The **system prompt** holds what is *durable*: who the assistant is, the rules it must follow, the format it should default to, the context that applies to every turn. The **user message** holds what is *specific*: this question, this document, this record to extract. Keeping the split clean makes behaviour predictable — and, as you learned, keeps the cacheable prefix stable.

A good system prompt is concrete: "You are an extraction service. Answer only from the provided text. If a field is missing, return null. Never invent values." That single block governs every request that follows.

## Few-shot prompting

The fastest way to get the behaviour and format you want is often not more instructions — it is **examples**. Few-shot prompting means including a few input/output pairs in the prompt that demonstrate exactly what you want.

```python
system = "You classify support tickets as: billing, technical, or other."
messages = [
    {"role": "user", "content": "My invoice is wrong."},
    {"role": "assistant", "content": "billing"},
    {"role": "user", "content": "The app crashes on launch."},
    {"role": "assistant", "content": "technical"},
    {"role": "user", "content": "How do I reset my password?"},   # real input
]
```

The model sees the pattern and continues it. A concrete demonstration of the desired output is usually clearer than any abstract description, which is why examples often beat longer prose. Use them whenever format or edge-case handling matters.

## Building the deliverable

Now assemble Module 1 into one thing: **a tool-using API client that returns structured data.** It is a small CLI or script that takes a question, lets the model call a tool to get real information, and returns a clean, parseable object — combining the raw Messages API, roles, the tool-use loop, and structured output.

```python
import anthropic, json

client = anthropic.Anthropic()
MODEL = "claude-opus-4-8"

def lookup_order(order_id: str) -> str:
    # your real data source; stubbed here
    return json.dumps({"order_id": order_id, "status": "shipped", "eta_days": 2})

tools = [{
    "name": "lookup_order",
    "description": "Look up an order's status by id.",
    "input_schema": {"type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"]},
}]

def ask(question: str) -> dict:
    messages = [{"role": "user", "content": question}]
    while True:
        resp = client.messages.create(
            model=MODEL, max_tokens=1024, tools=tools, messages=messages,
            system="You are an order assistant. Use tools for real data.",
        )
        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            for b in resp.content:
                if b.type == "tool_use":
                    out = lookup_order(**b.input)
                    messages.append({"role": "user", "content": [{
                        "type": "tool_result", "tool_use_id": b.id, "content": out}]})
            continue
        # final turn: ask for structured output
        return resp
```

That loop is the heart of it: the model calls `lookup_order`, you run it, return the result, and the model finishes. To make the *final* answer machine-readable, add an `output_config` JSON schema (from lesson five) so the client hands back a typed record — status, ETA, a summary — instead of prose. Wire it to `argparse` or `sys.argv` and you have a real CLI.

## Why this is the right capstone

Everything you have learned shows up here. Tokens and the context window set the budget. The failure modes justify the tool. Roles and few-shot examples steer behaviour. The tool-use loop fetches real data. Structured output makes the result safe to consume. And you built it on the **raw API** — so when you adopt a framework later, or deploy the same patterns on Bedrock or Azure, none of it is a black box.

## Your task

Build the deliverable: a CLI or script that takes a question as an argument, defines at least one tool, runs the full tool_use to tool_result loop, and returns structured JSON output the caller can parse. Test it on a question that forces the tool to be used.
