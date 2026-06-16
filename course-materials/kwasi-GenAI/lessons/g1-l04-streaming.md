---
course: kwasi-GenAI
title: Streaming responses
month: 1
monthTitle: LLM Foundations & API Fluency
lesson: 4
summary: 'Stream a model''s response as it is generated using server-sent events: consume token deltas
  as they arrive, and learn when streaming improves responsiveness and prevents timeouts.'
objectives:
- Explain what server-sent events are and how a streamed response arrives
- Consume incremental text deltas with the SDK streaming helper
- Reassemble the full message from a stream when you need it
- Decide when streaming is worth it and when it is not
- Use streaming to avoid HTTP timeouts on long or large outputs
- Identify the key stream event types in order
video: g1-l04-streaming.mp4
quiz:
- q: What does streaming change about how you receive a response?
  options:
  - The model thinks harder
  - The response arrives incrementally as a series of events instead of one final blob
  - It removes the token limit
  - It encrypts the output
  answer: 1
  why: Streaming delivers the response piece by piece via server-sent events, so you can display or process
    tokens as they are generated rather than waiting for the whole thing.
- q: Which delivery mechanism does the Messages API use to stream?
  options:
  - WebSockets
  - Server-sent events (SSE) over HTTP
  - FTP
  - gRPC only
  answer: 1
  why: Streamed responses are delivered as server-sent events — a one-way HTTP stream of event/data lines.
- q: Which event type carries the incremental text as it is generated?
  options:
  - message_start
  - content_block_delta
  - message_stop
  - ping
  answer: 1
  why: content_block_delta events carry the token deltas (text_delta); message_start and message_stop
    bookend the stream.
- q: 'A strong practical reason to stream a large output is to:'
  options:
  - Reduce token cost
  - Avoid HTTP request timeouts on long generations
  - Disable the context window
  - Force the model to use tools
  answer: 1
  why: Long non-streaming requests can exceed HTTP idle timeouts; streaming keeps data flowing so the
    connection stays alive and you get a responsive UI.
- q: In one sentence, when is streaming NOT worth the extra complexity?
  answer: When the output is short and you only need the final result for a backend step — for example
    a quick classification — a single non-streaming call is simpler.
  why: Streaming pays off for user-facing latency and long outputs; for short machine-to-machine results
    it just adds handling code for no benefit.
- q: After consuming a stream, how do you get the complete assembled message?
  answer: Use the SDK helper such as get_final_message() (Python) or finalMessage() (TypeScript), which
    accumulates the deltas into the full Message object.
  why: The streaming helpers track state for you, so you get the final message with usage and stop_reason
    without manually stitching deltas.
resources:
- label: Anthropic — Streaming messages
  url: https://platform.claude.com/docs/en/build-with-claude/streaming
- label: MDN — Using server-sent events
  url: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
- label: Anthropic — Messages API reference
  url: https://platform.claude.com/docs/en/api/messages
- label: Anthropic — Python SDK streaming examples
  url: https://github.com/anthropics/anthropic-sdk-python
---

## Why streaming exists

When you call the API normally, you wait for the model to finish, then receive the whole response at once. For a long answer that can mean staring at a blank screen for many seconds. **Streaming** changes the delivery: the response arrives incrementally, token by token, as it is generated. The user sees words appear in real time, exactly like a chat UI.

There is also a hard engineering reason. Very long generations can exceed an HTTP request's idle timeout — the connection sits silent while the model works, and a proxy or the SDK gives up. Streaming keeps data flowing, so the connection stays alive. In fact the SDKs will refuse a non-streaming request whose `max_tokens` is large enough to risk a timeout. For big outputs, streaming is not optional.

## Server-sent events

Streaming is delivered as **server-sent events (SSE)** — a simple one-way stream over a single HTTP response. The server writes a sequence of `event:` and `data:` lines, and your client reads them as they arrive. It is plain HTTP, not WebSockets, so it works through ordinary proxies and load balancers you already run.

```text
event: message_start
data: {"type":"message_start", ...}

event: content_block_delta
data: {"type":"content_block_delta","delta":{"type":"text_delta","text":"Hello"}}

event: message_stop
data: {"type":"message_stop"}
```

The key events, in order: `message_start` (metadata), one or more `content_block_start` / `content_block_delta` / `content_block_stop` sequences (the actual content), `message_delta` (carries the final `stop_reason` and usage), and `message_stop` at the very end.

## Consuming token deltas

The SDK gives you a streaming helper so you rarely parse raw SSE yourself. The simplest pattern iterates over text as it arrives:

```python
with client.messages.stream(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short poem about CI/CD."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

Each chunk is a **delta** — a small piece of new text. You `flush` so it appears immediately. That loop is the whole user-facing magic of a chat interface.

## Getting the final message

Often you want to stream for responsiveness *and* still have the complete object — full text, `stop_reason`, token usage — when it is done. The helpers accumulate that for you:

```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()
    print("\nTokens:", final.usage.output_tokens)
```

In TypeScript the equivalent is `stream.finalMessage()`. You get the live experience and the structured result without stitching deltas by hand.

## When to stream — and when not to

Stream when latency is **visible to a human** (chat, assistants, anything interactive) or when the output is **long enough to risk a timeout**. Skip streaming when you just need a short final result for a backend step — a one-word classification, a small extraction — where a single non-streaming call is simpler to write and read.

For your DevOps instincts: streaming is the difference between a CLI tool that feels alive and one that appears to hang. It is also your timeout insurance for any large generation.

## Your task

Write a small script that streams a response to a multi-paragraph prompt and prints the text as it arrives. Then call `get_final_message()` (or `finalMessage()`) and print the output token count and `stop_reason`.
