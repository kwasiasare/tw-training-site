---
course: ai-app-developer-2026
title: Build a Prompt-Driven Text Assistant
month: 1
monthTitle: Python and LLM Foundations
lesson: 4
summary: Build a small command-line text assistant in Python that uses engineered prompts and structured
  (JSON) outputs to summarize and transform user-supplied text. You'll learn to call an LLM API, design
  reliable prompts, parse structured responses, and ship a usable CLI.
objectives:
- Set up a Python project that calls an LLM API securely using environment variables
- Write engineered prompts with clear roles, instructions, and constraints
- Request and parse structured JSON outputs from an LLM for reliable downstream use
- Build a CLI that accepts text and a task (summarize, rewrite, extract) and prints results
- Handle common failure modes like malformed JSON, rate limits, and empty input
video: aad-m1-l04-build-a-prompt-driven-text-assistant.mp4
quiz:
- q: Why do we ask the model to return JSON instead of free-form text?
  options:
  - JSON uses fewer tokens always
  - Structured output is predictable and easy to parse programmatically
  - The API only supports JSON
  - JSON prevents the model from hallucinating entirely
  answer: 1
  why: Requesting JSON matching a defined schema makes the model's output predictable and parseable, turning
    it into a reliable component your code can consume.
- q: What is the main purpose of wrapping user text in delimiters like triple quotes?
  options:
  - To make the output prettier
  - To reduce token cost
  - To separate data from instructions and reduce prompt injection risk
  - To force the model to summarize
  answer: 2
  why: Delimiters signal that the enclosed text is content to be processed, not instructions to follow,
    which helps guard against prompt injection.
- q: Which setting in the API call helps make outputs more consistent and deterministic?
  options:
  - A high temperature like 1.5
  - A low temperature like 0.3
  - Setting max_tokens to 1
  - Using more messages
  answer: 1
  why: Lower temperature reduces randomness, producing more consistent and repeatable outputs—useful for
    structured tasks.
- q: Where should the API key be stored in this project?
  options:
  - Hard-coded in the Python file
  - In a .env file that is gitignored
  - In the prompt text
  - In the CLI arguments
  answer: 1
  why: Secrets belong in a .env file loaded at runtime and excluded from version control via .gitignore,
    never hard-coded or committed.
- q: Name one failure mode the CLI should handle and briefly how.
  answer: 'Malformed JSON: wrap json.loads in a try/except and optionally retry; or empty input: validate
    before calling the API; or rate limits: catch the API exception with backoff.'
  why: Robust apps handle malformed JSON, empty input, rate limits, and prompt injection so they degrade
    gracefully instead of crashing.
- q: What are the three parts of an engineered prompt described in this lesson?
  answer: System role (behavior/persona), instruction (the task with constraints), and the delimited user
    input.
  why: These three parts give the model clear behavior, a clear task, and clearly-marked data to work
    on.
resources:
- label: OpenAI API Reference — Chat Completions
  url: https://platform.openai.com/docs/api-reference/chat
- label: OpenAI Prompt Engineering Guide
  url: https://platform.openai.com/docs/guides/prompt-engineering
- label: Python argparse documentation
  url: https://docs.python.org/3/library/argparse.html
- label: python-dotenv on PyPI
  url: https://pypi.org/project/python-dotenv/
---

## What You're Building

A small CLI tool, `assist`, that takes a chunk of text and a task—**summarize**, **rewrite**, or **extract key points**—and returns a clean, structured result. The app demonstrates the core loop of every LLM-powered application: take user input, wrap it in an engineered prompt, call the model, parse the response, and present it.

## Project Setup

Create a virtual environment and install dependencies.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install openai python-dotenv
```

Store your API key in a `.env` file and never commit it:

```
OPENAI_API_KEY=sk-...
```

Add `.env` to your `.gitignore`.

## Anatomy of an Engineered Prompt

A good prompt has three parts:

1. **System role** — sets behavior and persona ("You are a precise text assistant").
2. **Instruction** — what to do, with explicit constraints (length, tone, format).
3. **Input** — the user's text, clearly delimited so the model can't confuse instructions with content.

Delimiters matter. Wrap user text in triple quotes or tags so injected instructions inside the text are treated as data, not commands.

## Requesting Structured Output

Free-form text is hard to use programmatically. Instead, ask the model to return **JSON** matching a schema you define. This makes the output predictable and parseable.

```python
import json, os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

SYSTEM = "You are a precise text assistant. Always reply with valid JSON only."

def run_task(task: str, text: str) -> dict:
    instruction = {
        "summarize": "Summarize the text in 2-3 sentences.",
        "rewrite": "Rewrite the text to be clear and professional.",
        "extract": "Extract the 3-5 most important points as a list.",
    }[task]

    prompt = (
        f"{instruction}\n"
        f"Return JSON with keys: 'task', 'result' (string or list), 'word_count' (int).\n"
        f"Text:\n\"\"\"{text}\"\"\""
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    return json.loads(resp.choices[0].message.content)
```

Note `response_format={"type": "json_object"}`, which instructs the API to return valid JSON, and a low `temperature` for consistency. This is **JSON mode**, the original mechanism — keep it in mind as the baseline, then upgrade to Structured Outputs below.

### Structured Outputs: The Modern Default

JSON mode (`json_object`) is the legacy baseline: it guarantees syntactically valid JSON, but the model can still return the wrong keys or types. **Structured Outputs** goes further — you pass a JSON Schema with `"strict": true`, and the API **guarantees the response conforms to that schema**:

```python
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "assist_result",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "result": {"type": "string"},
                    "word_count": {"type": "integer"},
                },
                "required": ["task", "result", "word_count"],
                "additionalProperties": False,
            },
        },
    },
    temperature=0.3,
)
```

The SDK also offers a convenience helper: define the schema as a Pydantic model and let `.parse()` handle the schema plumbing and validation for you:

```python
from pydantic import BaseModel

class AssistResult(BaseModel):
    task: str
    result: str
    word_count: int

completion = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt},
    ],
    response_format=AssistResult,
)
out = completion.choices[0].message.parsed  # a validated AssistResult instance
```

Use Structured Outputs whenever downstream code depends on the shape; fall back to JSON mode only for models or providers that don't support strict schemas.

### The Responses API

OpenAI's current primary interface is the **Responses API** — `client.responses.create(model=..., input=...)` — which unifies chat, tool use, and structured outputs under one endpoint (read the reply from `response.output_text`). Chat Completions remains fully supported, and this course uses it because it's the request shape the widest range of providers and libraries are compatible with. Everything you learn here — messages, structured output, temperature — transfers directly.

## Building the CLI

Use Python's built-in `argparse` to accept a task and text (from an argument or stdin).

```python
import argparse, sys

def main():
    parser = argparse.ArgumentParser(description="Prompt-driven text assistant")
    parser.add_argument("task", choices=["summarize", "rewrite", "extract"])
    parser.add_argument("--text", help="Input text; if omitted, read stdin")
    args = parser.parse_args()

    text = args.text or sys.stdin.read()
    if not text.strip():
        print("Error: no input text provided.", file=sys.stderr)
        sys.exit(1)

    try:
        out = run_task(args.task, text)
    except json.JSONDecodeError:
        print("Error: model returned malformed JSON.", file=sys.stderr)
        sys.exit(2)

    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
```

Run it:

```bash
echo "Long article text here..." | python assist.py summarize
python assist.py extract --text "Meeting notes..."
```

## Handling Failure Modes

Real apps fail gracefully:

- **Malformed JSON** — wrap `json.loads` in try/except and optionally retry once.
- **Empty input** — validate before calling the API to save tokens.
- **Rate limits / network errors** — catch API exceptions and show a friendly message; add retries with backoff for production.
- **Prompt injection** — delimit user text and keep instructions in the system message.

## Key Takeaways

Every LLM app is the same loop: shape the input with a prompt, constrain the output format, parse it, and handle errors. Structured JSON output turns an unpredictable model into a reliable component you can build on.
