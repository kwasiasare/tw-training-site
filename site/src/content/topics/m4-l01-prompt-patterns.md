---
title: Prompt-engineering patterns
month: 4
monthTitle: Portfolio Projects
lesson: 1
summary: Reusable patterns - roles, few-shot, structured output and chaining - that make a language model's
  answers reliable enough to ship.
objectives:
- Write a clear instruction with a role, task, and constraints
- Use a system prompt to set persistent behaviour
- Steer output with few-shot examples
- Force machine-readable answers with structured output
- Split hard problems into a chain of smaller prompts
- Call the Claude Messages API in Python with a model id and max_tokens
- Evaluate a prompt and iterate instead of guessing
video: m4-l01-prompt-patterns.mp4
quiz:
- q: What is the role of a system prompt?
  options:
  - It stores the API key
  - It sets persistent behaviour and persona for the whole conversation
  - It is the user's first question
  - It limits how many tokens you are billed for
  answer: 1
  why: The system prompt frames who the model is and how it should behave across every turn, separate
    from the per-message user content.
- q: What is few-shot prompting?
  options:
  - Asking the same question several times
  - Giving a few worked input-output examples so the model copies the pattern
  - Using fewer tokens to save money
  - Calling the model with a tiny max_tokens
  answer: 1
  why: Few-shot means including a handful of example pairs in the prompt so the model infers the format
    and style you want.
- q: Why ask the model for JSON output instead of free text?
  options:
  - JSON is cheaper per token
  - JSON can be parsed reliably by your code without fragile string-matching
  - The model thinks harder in JSON
  - It is the only format the API accepts
  answer: 1
  why: Structured output (e.g. JSON) lets your program read fields directly, instead of guessing meaning
    from prose that varies each run.
- q: In one sentence, what is prompt chaining and when would you use it?
  answer: Splitting a task into a sequence of prompts where each step's output feeds the next; use it
    when one prompt is doing too much or accuracy drops.
  why: Chaining keeps each step simple and checkable - extract, then summarise, then format - which is
    far more reliable than one giant prompt.
- q: Name one reason you should keep your API key in an environment variable, not in your code.
  answer: So the secret is never committed to Git or shared, keeping it out of your portfolio repo and
    version history.
  why: Hard-coded keys leak when you push to GitHub; reading ANTHROPIC_API_KEY from the environment keeps
    the secret private.
- q: What does the temperature-free, deterministic-leaning approach of giving explicit constraints buy
    you?
  options:
  - Faster responses
  - More predictable, on-spec answers that are easier to test
  - A larger context window
  - Free tokens
  answer: 1
  why: Explicit constraints (length, format, what to avoid) narrow the model's choices, so outputs vary
    less and are easier to evaluate.
resources:
- label: Anthropic - Prompt engineering overview
  url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview
- label: Anthropic - Use examples (multishot prompting)
  url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- label: Anthropic - Chain complex prompts
  url: https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts
- label: Anthropic Cookbook (GitHub) - runnable prompt recipes
  url: https://github.com/anthropics/anthropic-cookbook
---

## Why prompt patterns?

A **prompt** is the text you send to a language model. Beginners type a question and hope. Engineers use **patterns** - reusable shapes that turn a vague request into a reliable, testable instruction. For your portfolio projects this is the difference between a demo that works once and a feature that works every time.

Think of it like a function signature: a good prompt states the **role**, the **task**, the **inputs**, and the **constraints** on the output.

## Pattern 1: role, task, constraints

Don't just say *"summarise this"*. Say who the model is, what to do, and what the answer must look like.

```text
You are a careful financial analyst.
Summarise the email below in exactly 3 bullet points.
Do not invent numbers. If a figure is missing, write "not stated".
```

The role sets tone, the task is the verb, and the constraints (3 bullets, no invented numbers) make the output predictable - and therefore testable.

## Pattern 2: system prompt + few-shot

The **system prompt** sets persistent behaviour for the whole conversation. **Few-shot** prompting adds a few worked examples so the model copies the pattern. Here is a minimal Claude Messages API call in Python:

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You label support tickets. Reply with one word: billing, bug, or other.",
    messages=[
        {"role": "user", "content": "My card was charged twice."},
        {"role": "assistant", "content": "billing"},
        {"role": "user", "content": "The app crashes on login."},
    ],
)
print(msg.content[0].text)  # -> bug
```

The earlier user/assistant pair is the single example that teaches the format.

## Pattern 3: structured output

When your code needs to *read* the answer, ask for JSON and parse it - never string-match prose.

```python
import json
from anthropic import Anthropic

client = Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    messages=[{"role": "user", "content":
        'Extract name and city as JSON keys "name" and "city": '
        '"Ada Lovelace lives in London."'}],
)
data = json.loads(msg.content[0].text)
print(data["city"])  # -> London
```

## Pattern 4: prompt chaining

If one prompt is doing too much, break it into steps where each output feeds the next: **extract -> summarise -> format**. Each step is simple, so each step is easy to check and fix. This is the single biggest reliability win in real projects.

## Your task

Take one feature in your portfolio project and rewrite its prompt using **role, task, constraints** plus one **few-shot example**. Keep your key in `ANTHROPIC_API_KEY`.
