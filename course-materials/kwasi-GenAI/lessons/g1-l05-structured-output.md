---
course: kwasi-GenAI
title: Structured / JSON output
month: 1
monthTitle: LLM Foundations & API Fluency
lesson: 5
summary: Get reliable, parseable JSON out of a model using JSON-schema structured output, and understand
  why parsing prose with regex is fragile and breaks in production.
objectives:
- Explain why parsing free-form prose for data is fragile
- Request structured output by supplying a JSON schema
- Use the SDK parse helper to validate output against a schema
- Describe the difference between JSON output and strict tool use
- Choose structured output when a downstream system needs reliable data
- Handle the cases where structured output can still fail
video: g1-l05-structured-output.mp4
quiz:
- q: Why is parsing model prose with regex fragile?
  options:
  - Regex is slow
  - The model can phrase the same data many ways, so any parser eventually breaks on a new phrasing
  - JSON is not supported by models
  - Regex cannot read numbers
  answer: 1
  why: Natural language has endless valid phrasings; a regex tuned to today's output silently breaks the
    moment the model words things differently.
- q: How do you ask the Messages API for guaranteed-shape JSON?
  options:
  - Set temperature to 0
  - Provide a JSON schema via output_config.format
  - Add 'return JSON' as a stop sequence
  - Use a GET request
  answer: 1
  why: Structured output is requested through output_config.format with a json_schema, which constrains
    the response to match the schema.
- q: What does the SDK parse helper (e.g. messages.parse) give you?
  options:
  - Faster responses
  - A validated, typed object parsed from the model's output against your schema
  - Free tokens
  - Automatic streaming
  answer: 1
  why: The parse helper validates the response against your schema (e.g. a Pydantic model) and returns
    a typed object, removing manual JSON handling.
- q: How does 'strict tool use' relate to structured output?
  options:
  - They are unrelated
  - Both constrain shape — strict tools validate a tool's input parameters against its schema
  - Strict tools disable JSON
  - Strict tools are only for streaming
  answer: 1
  why: 'Structured output constrains the response body; strict tool use (strict: true) constrains a tool
    call''s input parameters — both are schema enforcement on the same endpoint.'
- q: In one sentence, when should you prefer structured output over prose?
  answer: Whenever a downstream system — a database, an API, a UI, another service — must consume the
    result programmatically and needs a reliable, predictable shape.
  why: Machine consumers need stable fields and types, which prose cannot guarantee but a JSON schema
    can.
- q: Name one situation where structured output can still fail.
  answer: When the model refuses for safety (stop_reason 'refusal') or hits max_tokens mid-object, the
    output may be incomplete or not match the schema, so you still validate and handle errors.
  why: Schema constraints shape the output but do not override a refusal or a truncated response, so defensive
    handling is still required.
resources:
- label: Anthropic — Structured outputs
  url: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- label: Anthropic — Tool use overview (strict)
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: JSON Schema — Getting started
  url: https://json-schema.org/learn/getting-started-step-by-step
- label: Anthropic — Increase output consistency
  url: https://platform.claude.com/docs/en/build-with-claude/define-success
---

## The problem with prose

A model loves to talk. Ask for someone's email and plan and it might say: "Sure! Jane Doe can be reached at jane@co.com and she's on the Enterprise plan." Lovely for a human. A nightmare for code. To extract the fields you would write a regex — and that regex breaks the instant the model phrases things differently next time: "Jane (jane@co.com) — Enterprise tier." Same data, new wording, broken parser.

This is the central lesson: **never build a production pipeline on parsing free-form prose.** Natural language has infinite valid phrasings, and your parser only handles the ones you have seen. You need the model to return data in a shape you define.

## Structured output: define the shape

The fix is **structured output**. You hand the API a **JSON schema** describing exactly the fields and types you want, and the response is constrained to match it. Instead of hoping for JSON, you require it.

```python
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user",
               "content": "Extract: Jane Doe (jane@co.com) wants Enterprise."}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name":  {"type": "string"},
                    "email": {"type": "string"},
                    "plan":  {"type": "string"},
                },
                "required": ["name", "email", "plan"],
                "additionalProperties": False,
            },
        }
    },
)
```

The first content block is now reliable JSON you can `json.loads()` with confidence.

## The parse helper

Even better, the SDK can validate *and* type the result for you. In Python you define a Pydantic model and call `messages.parse`:

```python
from pydantic import BaseModel

class Contact(BaseModel):
    name: str
    email: str
    plan: str

response = client.messages.parse(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    output_format=Contact,
)
contact = response.parsed_output   # a validated Contact instance
print(contact.email)
```

No manual JSON handling, no regex, and an immediate type error if something is off. TypeScript does the same with a Zod schema.

## Structured output vs strict tool use

These are two flavours of the same idea — schema enforcement on the one Messages endpoint. **Structured output** (`output_config.format`) constrains the model's *response body*. **Strict tool use** (`strict: true` on a tool) constrains the *input parameters* of a tool the model calls. You will use the second in the next lesson. Both guarantee shape; they just apply it in different places.

## It is reliable, not magic

Structured output dramatically increases reliability, but it does not override everything. If the model **refuses** for safety (`stop_reason: "refusal"`) or the output is **cut off** by `max_tokens` mid-object, you can still get an incomplete or non-conforming result. So you keep validating and handle those cases — the same defensive posture you already apply to any external input. The first request with a new schema is also slightly slower while the schema compiles; later calls hit a cache.

## Why this matters for you

Every integration you build will hand model output to something else — a database, an API, a dashboard. Structured output is the contract that makes those handoffs safe. It turns a chatty model into a dependable component in a pipeline, which is exactly what an Applied GenAI Engineer ships.

## Your task

Define a small JSON schema (or Pydantic / Zod model) for a data record relevant to your work, then make a request that extracts that record from a sentence of prose. Parse the result and print one field, and note what would have broken if you had used a regex instead.
