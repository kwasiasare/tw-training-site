---
title: Streaming & structured output
month: 3
monthTitle: LLM Application Skills
lesson: 5
summary: Stream model responses token-by-token for snappy apps, and force JSON output that matches a schema
  so your code can trust it.
objectives:
- Explain why streaming makes LLM apps feel faster and avoids timeouts
- Stream a Claude response and print tokens as they arrive
- Get the full message after a stream with get_final_message()
- Force the model to return JSON that matches a schema
- Validate structured output into a Pydantic model with messages.parse()
- Avoid fragile string-parsing by trusting schema-guaranteed JSON
- Choose between streaming and a single blocking call for a given task
video: m3-l05-streaming-structured.mp4
quiz:
- q: What is the main user-facing benefit of streaming a model response?
  options:
  - It uses fewer tokens
  - Text appears progressively instead of after a long pause
  - It removes the need for an API key
  - It guarantees valid JSON
  answer: 1
  why: Streaming delivers tokens as they are generated, so the user sees output immediately rather than
    waiting for the whole response.
- q: In the Anthropic Python SDK, which call gives you the complete message after streaming finishes?
  options:
  - stream.collect()
  - stream.get_final_message()
  - stream.finish()
  - stream.result()
  answer: 1
  why: get_final_message() returns the fully accumulated Message after the stream completes, including
    usage and stop_reason.
- q: Which approach is recommended to force the model to return JSON that fits a schema?
  options:
  - A prefilled assistant turn
  - output_config with a json_schema format, or messages.parse()
  - Asking nicely in the prompt only
  - Lowering max_tokens
  answer: 1
  why: output_config.format with a json_schema constrains the response shape; messages.parse() additionally
    validates it into a typed object.
- q: Name the SDK method that streams AND validates the response into a Pydantic model is NOT one call.
    What method validates a non-streamed response into a Pydantic model?
  answer: messages.parse
  why: client.messages.parse(...) with output_format=YourModel returns response.parsed_output as a validated
    instance of your Pydantic class.
- q: Why should you parse tool or JSON output with json.loads rather than matching the raw string?
  answer: Because the model may escape characters (Unicode or slashes) differently, so raw string matching
    is fragile; parsing handles escaping correctly.
  why: JSON escaping can vary between responses; json.loads() decodes it reliably while substring checks
    can silently miss.
- q: 'True or false: streaming is recommended whenever a request may produce long output or use a high
    max_tokens.'
  options:
  - 'True'
  - 'False'
  answer: 0
  why: Long or large-output requests risk HTTP timeouts on a single blocking call; streaming keeps the
    connection active and avoids the cap surprise.
resources:
- label: Anthropic docs — Streaming Messages
  url: https://platform.claude.com/docs/en/build-with-claude/streaming
- label: Anthropic docs — Structured outputs
  url: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- label: Pydantic documentation — Models
  url: https://docs.pydantic.dev/latest/concepts/models/
- label: Anthropic Python SDK (GitHub)
  url: https://github.com/anthropics/anthropic-sdk-python
---

## Two skills your apps need

By now you can call Claude and get a reply. Two refinements make your apps feel professional and stay reliable:

1. **Streaming** — show text as it is generated, instead of freezing while the whole answer is produced.
2. **Structured output** — force the reply into a fixed JSON shape your code can trust, instead of fishing values out of free-form prose.

As a maths graduate, think of structured output as constraining the *codomain* of the model: you specify the exact shape the answer must take.

## Why streaming?

A model generates one token at a time. A normal `messages.create()` call waits for **all** of them, then hands you the finished message. For a long answer that is a multi-second silent pause — and for very long outputs the request can even hit an HTTP timeout.

Streaming delivers each chunk the moment it is ready. The user reads along as the model writes, exactly like a chat app. Default to streaming for anything with long input, long output, or a high `max_tokens`.

## Streaming with the SDK

Use `client.messages.stream(...)` as a context manager and iterate `text_stream`:

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain gradient descent in 3 sentences."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

    final = stream.get_final_message()

print("\n\nTokens out:", final.usage.output_tokens)
```

`flush=True` shows each chunk immediately. After the loop, `get_final_message()` gives you the whole assembled message — usage, stop reason, everything — so you get streaming *and* the convenience of a complete result.

## Why structured output?

Imagine asking the model to extract a customer's name, email, and whether they want a demo. If it replies in a paragraph, your code has to parse English — brittle and error-prone. Instead, you can **constrain the response to a JSON schema**, so every reply is valid JSON with exactly the fields you asked for.

The cleanest way in Python is `client.messages.parse()` with a Pydantic model. The SDK validates the response for you and hands back a typed object.

```python
from pydantic import BaseModel
from anthropic import Anthropic

client = Anthropic()

class Contact(BaseModel):
    name: str
    email: str
    wants_demo: bool

response = client.messages.parse(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Jane Doe (jane@co.com) asked us to book her a demo next week.",
    }],
    output_format=Contact,
)

contact = response.parsed_output   # a validated Contact instance
print(contact.name, contact.email, contact.wants_demo)
```

No brittle string parsing: `contact.wants_demo` is a real Python `bool`.

## A note on parsing

When you do read JSON yourself — from a raw schema response or a tool call — always use `json.loads()`. Models can escape characters differently between responses, so matching the raw text is fragile. Parse it properly and let the JSON decoder do the work.

## Your task

Take one of your earlier scripts and (1) switch it to streaming, then (2) make it return a small Pydantic model with two or three fields.
