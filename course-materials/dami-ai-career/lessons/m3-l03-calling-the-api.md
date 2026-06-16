---
title: Calling the LLM API
month: 3
monthTitle: LLM Application Skills
lesson: 3
summary: Send your first request to Claude from Python, structure messages, read the response, and keep
  your API key safe.
objectives:
- Install the Anthropic SDK and create a client
- Keep your API key in an environment variable, never in code
- Send a message with the messages.create method
- Pick a model id and set max_tokens sensibly
- Read text out of the response content blocks
- Add a system prompt to steer Claude's behaviour
- Handle common errors like rate limits and bad requests
video: m3-l03-calling-the-api.mp4
quiz:
- q: Where should your Anthropic API key live?
  options:
  - Hard-coded in the script
  - In an environment variable like ANTHROPIC_API_KEY
  - In a public GitHub repo
  - In the messages list
  answer: 1
  why: Keys are secrets. Store them in the ANTHROPIC_API_KEY environment variable so the SDK reads them
    automatically and they never end up in your code or git history.
- q: Which method sends a request to Claude in the Anthropic Python SDK?
  options:
  - client.complete()
  - client.chat()
  - client.messages.create()
  - client.send()
  answer: 2
  why: The current Messages API uses client.messages.create(). The old completions API is deprecated and
    should not be used.
- q: What does the response.content field hold?
  options:
  - A single string
  - A list of content blocks
  - A status code
  - The API key
  answer: 1
  why: content is a list of blocks (TextBlock, ThinkingBlock, and so on). Check each block's type and
    read .text on text blocks.
- q: Name the two required parameters on messages.create() besides messages.
  answer: model and max_tokens
  why: Every request must specify which model to call and a max_tokens ceiling on the output length.
- q: What is a system prompt used for?
  answer: To set Claude's role, tone, and rules before the conversation
  why: The system parameter gives Claude persistent instructions that shape every reply, separate from
    the user's message.
- q: If you send too many requests too quickly, which error do you get?
  options:
  - AuthenticationError
  - RateLimitError
  - NotFoundError
  - BadRequestError
  answer: 1
  why: A 429 raises RateLimitError. The SDK retries automatically with backoff, and you can read the retry-after
    header to wait.
resources:
- label: Anthropic API — Messages reference
  url: https://docs.claude.com/en/api/messages
- label: Anthropic Python SDK on GitHub
  url: https://github.com/anthropics/anthropic-sdk-python
- label: Anthropic Quickstart guide
  url: https://docs.claude.com/en/docs/get-started
- label: Anthropic Console (get an API key)
  url: https://console.anthropic.com
---

## What is an LLM API call?

So far you have used Claude through a chat window. An **API** lets your *code* talk to Claude instead. You send a request describing the conversation, and Claude sends back a response your program can read and act on.

Think of it like a function from your maths days: messages go in, a reply comes out. The difference is the function lives on Anthropic's servers, and you call it over the internet.

## Setup and your API key

First install the official SDK, then store your key as an environment variable. **Never** paste your key into your code or commit it to git.

```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."   # macOS / Linux
```

On Windows PowerShell you would use `$env:ANTHROPIC_API_KEY = "sk-ant-..."`. The SDK reads this variable automatically.

## Your first request

Create a client, then call `client.messages.create()`. You must pass a `model`, a `max_tokens` ceiling, and a list of `messages`.

```python
from anthropic import Anthropic

client = Anthropic()   # reads ANTHROPIC_API_KEY from the environment

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain a derivative in one sentence."}
    ],
)
```

## Reading the response

The reply is not a plain string. `msg.content` is a **list of blocks**. For a simple text answer, read `.text` off the first text block.

```python
for block in msg.content:
    if block.type == "text":
        print(block.text)

print(msg.usage.input_tokens, msg.usage.output_tokens)
```

`msg.usage` tells you how many tokens you spent, which maps directly to cost.

## System prompts and roles

A **system prompt** sets Claude's role and rules for the whole conversation. Each entry in `messages` has a `role` (`user` or `assistant`) and `content`. The API is stateless, so you resend the full history each turn.

```python
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a patient maths tutor. Keep answers short.",
    messages=[{"role": "user", "content": "What is a gradient?"}],
)
```

## Handling errors

Networks fail and limits get hit. Wrap calls in `try / except` and catch the typed exceptions the SDK gives you.

```python
import anthropic

try:
    msg = client.messages.create(model="claude-sonnet-4-6", max_tokens=256,
                                 messages=[{"role": "user", "content": "Hi"}])
except anthropic.RateLimitError:
    print("Slow down — too many requests.")
except anthropic.AuthenticationError:
    print("Check your API key.")
```

## Your task

Write a short script that asks Claude one question, prints the answer, and prints the token usage. Try adding a system prompt and see how the answer changes.
