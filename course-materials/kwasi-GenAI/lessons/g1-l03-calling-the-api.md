---
course: kwasi-GenAI
title: Calling the API directly
month: 1
monthTitle: LLM Foundations & API Fluency
lesson: 3
summary: 'Make your first raw call to the Anthropic Messages API: understand messages, the user and assistant
  roles, the top-level system prompt, and content blocks — the shape every later feature builds on.'
objectives:
- Send a basic request to the Anthropic Messages API
- Explain the roles user and assistant and how turns alternate
- Use the top-level system parameter to set behaviour
- Describe content blocks and why content is a list, not a string
- 'Read the key fields of a response: content, stop_reason, and usage'
- Recognise the same request shape on Amazon Bedrock and Azure
video: g1-l03-calling-the-api.mp4
quiz:
- q: Which endpoint do Anthropic requests go through?
  options:
  - POST /v1/chat
  - POST /v1/messages
  - GET /v1/generate
  - POST /v1/completions
  answer: 1
  why: The Messages API is the single endpoint (POST /v1/messages); tools and structured output are features
    of it, not separate APIs.
- q: Where does the system prompt go in a Messages request?
  options:
  - As the first message with role 'system'
  - In a top-level 'system' parameter, separate from messages
  - Inside the user message text
  - It is not supported
  answer: 1
  why: Anthropic takes the system prompt as a top-level 'system' field, distinct from the messages array
    of user and assistant turns.
- q: What two roles make up a normal messages array?
  options:
  - admin and guest
  - user and assistant
  - system and tool
  - client and server
  answer: 1
  why: Conversation turns alternate between role 'user' (you) and role 'assistant' (the model); the system
    prompt is separate.
- q: Why is a message's content often a list of blocks rather than a plain string?
  options:
  - To save bandwidth
  - So one turn can hold mixed parts — text, images, tool_use, tool_result
  - Because strings are deprecated
  - To force JSON output
  answer: 1
  why: Content blocks let a single message carry multiple typed parts, which is what makes images, tool
    calls, and tool results possible in the same turn.
- q: In one sentence, what does the response 'stop_reason' field tell you?
  answer: It tells you why the model stopped generating — for example end_turn when it finished, max_tokens
    when it hit the output cap, or tool_use when it wants you to run a tool.
  why: Branching on stop_reason is how your code knows whether the turn is complete or needs follow-up
    action.
- q: Name one cloud where you can call Claude with these same Messages-API patterns.
  answer: Amazon Bedrock (or Azure / Microsoft Foundry) — the request shape is the same, only the client
    setup and model-id prefix change.
  why: The Messages API shape carries across clouds you already operate, so the skills here transfer directly
    to Bedrock and Azure deployments.
resources:
- label: Anthropic — Messages API reference
  url: https://platform.claude.com/docs/en/api/messages
- label: Anthropic — Get started / first request
  url: https://platform.claude.com/docs/en/get-started
- label: Anthropic — Claude on Amazon Bedrock
  url: https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock
- label: Anthropic — Python SDK (anthropic-sdk-python)
  url: https://github.com/anthropics/anthropic-sdk-python
---

## Start at the raw API, not a framework

It is tempting to reach straight for a high-level framework. Don't — not yet. Frameworks hide exactly the request shape you most need to understand. If you learn the **raw Messages API** first, every framework, agent loop, and abstraction you meet later becomes obvious, because you will recognise what it is generating underneath. This is the same reason you learned HTTP before learning a web framework.

Everything Anthropic does goes through one endpoint: `POST /v1/messages`. Tools, streaming, and structured output are all *features of this single endpoint*, not separate APIs. Master its shape and you have mastered the surface.

## The anatomy of a request

A request has a few core parts: the `model`, a `max_tokens` cap, an optional top-level `system` prompt, and a `messages` array.

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    system="You are a concise assistant for DevOps engineers.",
    messages=[
        {"role": "user", "content": "In one line, what is idempotency?"}
    ],
)
print(response.content[0].text)
```

Notice what is *not* here: no separate "prompt" string, no template engine. Just a model, a system instruction, and a conversation.

## Roles: user and assistant

The `messages` array is the conversation. Each entry has a `role` — either `user` (you) or `assistant` (the model) — and turns alternate. The first message must be `user`. To continue a conversation, you append the assistant's previous reply and your next `user` message, then send the whole history again. The API is **stateless**: it remembers nothing between calls, so you always send the full conversation.

The **system** prompt is deliberately *not* a role inside the array. It is a top-level `system` parameter that sets persona, rules, and context for the whole exchange. Keeping it separate makes its authority clear and its placement cache-friendly.

## Content blocks

Look closely at `content`. For a simple text turn you can pass a plain string, but under the hood content is a **list of typed blocks**. That is why `response.content[0].text` indexes into a list.

```python
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe this diagram."},
        # an image block could go here too
    ],
}]
```

Blocks are the reason one message can mix text with an image, or carry a `tool_use` request, or return a `tool_result`. Every advanced feature in this module is just a new block type. Learn the container now and the features slot in later.

## Reading the response

The response object carries `content` (the list of output blocks), `stop_reason` (why it stopped — `end_turn`, `max_tokens`, `tool_use`, `refusal`), and `usage` (input and output token counts — your cost meter). Always check `stop_reason` before assuming a turn is complete; in later lessons it is how you detect a tool call.

## The same shape, in your clouds

Here is the payoff for your background: this exact request shape runs on **Amazon Bedrock** and **Azure / Microsoft Foundry** too. The client setup and the model-id string change (Bedrock prefixes ids, for example `anthropic.claude-opus-4-8`), but `messages`, `system`, roles, and content blocks are identical. Learn it once here on the first-party API; deploy it wherever you already operate.

## Your task

Using the Anthropic Python SDK, send a single Messages request with a one-sentence `system` prompt of your choice and one `user` message. Print `response.content[0].text`, then also print `response.stop_reason` and `response.usage` and note what each tells you.
