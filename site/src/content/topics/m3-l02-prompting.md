---
title: Prompting & system prompts
month: 3
monthTitle: LLM Application Skills
lesson: 2
summary: Learn to write clear prompts and system prompts that steer a large language model toward reliable,
  well-shaped answers.
objectives:
- Explain the difference between a system prompt and a user message
- Write a system prompt that sets role, rules, and output format
- Structure user prompts with context, task, and constraints
- Use few-shot examples to demonstrate the behaviour you want
- Call the Claude Messages API with a system prompt in Python
- Recognise common prompting mistakes and how to fix them
video: m3-l02-prompting.mp4
quiz:
- q: What is a system prompt?
  options:
  - The user's question
  - Standing instructions that set the model's role and rules for the whole conversation
  - An error message from the API
  - The model's hidden weights
  answer: 1
  why: The system prompt is persistent guidance — role, tone, and rules — that applies across every turn,
    separate from each user message.
- q: In the Anthropic Messages API, where does the system prompt go?
  options:
  - Inside the messages list as a user turn
  - In a separate top-level system parameter
  - In the model name
  - In the max_tokens field
  answer: 1
  why: Claude takes the system prompt as its own top-level system= parameter, kept distinct from the messages
    list of user and assistant turns.
- q: What is 'few-shot' prompting?
  options:
  - Asking the model many separate questions
  - Giving the model a few worked examples of input and desired output
  - Limiting the model to a few tokens
  - Running the model a few times and voting
  answer: 1
  why: Few-shot prompting shows the model two or three examples of the input-to-output behaviour you want,
    which steers its responses far better than a description alone.
- q: Why ask the model to return a specific format such as JSON?
  answer: So your program can reliably parse the output instead of guessing where each piece of information
    is.
  why: A specified, structured format makes the response machine-readable, which is essential when the
    model's output feeds into the rest of your code.
- q: Name one common prompting mistake and how to fix it.
  answer: Being vague — fix it by stating the exact task, the context, and the desired output format and
    length.
  why: Vague prompts force the model to guess your intent; specific instructions about task, context,
    and format give consistent, usable answers.
- q: True or false — putting your rules in the system prompt and your question in the user message keeps
    instructions consistent across a multi-turn chat.
  options:
  - 'True'
  - 'False'
  answer: 0
  why: True. The system prompt persists across every turn, so the model keeps following those rules even
    as the user messages change.
resources:
- label: Anthropic — Prompt engineering overview
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- label: Anthropic — System prompts guide
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts
- label: Anthropic — Use examples (multishot prompting)
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- label: Anthropic Prompt Library — ready-made example prompts
  url: https://docs.anthropic.com/en/resources/prompt-library/library
---

## What is a prompt?

A **prompt** is the text you send to a large language model to get a response. The quality of that response depends heavily on how you ask. As a maths graduate, think of it like specifying a problem precisely: the clearer the statement, the better the solution.

There are two kinds of instruction you give Claude:

- The **system prompt** — standing rules that set the model's role, tone, and output format for the whole conversation.
- The **user message** — the actual question or task for this turn.

## System prompts: setting the rules

The system prompt is where you tell the model *who it is* and *how to behave* across every turn. Put the role, the constraints, and the required output format here. It stays in effect even as the user messages change.

In the Anthropic Messages API the system prompt is a separate top-level parameter — it is not just another message in the list.

```python
from anthropic import Anthropic

client = Anthropic()

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a concise maths tutor. Answer in at most three sentences.",
    messages=[
        {"role": "user", "content": "What is a derivative?"}
    ],
)
print(msg.content[0].text)
```

## Structuring the user message

A strong user prompt usually has three parts: **context** (background the model needs), **task** (what to do), and **constraints** (format, length, tone). Spelling these out removes guesswork.

Vague: *"Tell me about this data."*

Specific: *"Here is a CSV of monthly sales. Summarise the three biggest trends in bullet points, one sentence each."*

## Few-shot examples

Often the fastest way to get the behaviour you want is to *show* it. Giving the model two or three examples of input and the desired output is called **few-shot** (or multishot) prompting, and it steers the model far more reliably than description alone.

```python
system = (
    "Classify each review as POSITIVE or NEGATIVE.\n"
    "Review: 'Loved it, fast and clean.' -> POSITIVE\n"
    "Review: 'Slow and rude staff.' -> NEGATIVE"
)

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=20,
    system=system,
    messages=[{"role": "user", "content": "Review: 'Average meal, nothing special.'"}],
)
print(msg.content[0].text)
```

## Asking for a parseable format

When the model's output feeds into your own code, ask for a structured format such as JSON so you can parse it reliably instead of guessing. Keep your API key in an environment variable (`ANTHROPIC_API_KEY`) and never hard-code it.

## Common mistakes

- Being **vague** — fix by stating task, context, and format.
- **Mixing rules into every user message** — put persistent rules in the system prompt instead.
- **No output format** — specify it when code will read the result.
- **Over-stuffing** — too many instructions compete; keep it focused.

## Your task

Write a system prompt and one user message that make Claude act as a friendly explainer of a topic from your degree, and return its answer as three short bullet points.
