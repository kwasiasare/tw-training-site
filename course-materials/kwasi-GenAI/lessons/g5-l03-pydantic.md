---
course: kwasi-GenAI
title: Validate data with Pydantic
month: 5
monthTitle: Python for Production Apps
lesson: 3
summary: Use Pydantic to define typed data models that validate inputs and outputs, then pair those models
  with structured LLM output so the model returns data your code can trust.
objectives:
- Define a Pydantic BaseModel with typed and optional fields
- Explain how Pydantic validates and coerces data, raising clear errors on bad input
- Add custom rules with field constraints and validators
- Validate untrusted LLM output against a model before using it
- Generate a JSON Schema from a model to drive structured LLM output
- Use a tool / structured-output call so Claude returns data matching your schema
video: g5-l03-pydantic.mp4
quiz:
- q: What happens when you pass data that doesn't match a Pydantic model's types?
  options:
  - It is silently ignored
  - Pydantic raises a ValidationError describing exactly which fields are wrong
  - The program continues with None values
  - It converts everything to strings
  answer: 1
  why: Pydantic validates on construction and raises a ValidationError listing each field that failed
    and why, so bad data is caught at the boundary.
- q: Why is Pydantic especially valuable for LLM outputs?
  options:
  - It makes the model cheaper
  - LLM output is untrusted text, and Pydantic checks it has the exact shape and types your code expects
    before you use it
  - It speeds up token generation
  - It stores the output in a database
  answer: 1
  why: A model can return malformed or unexpected JSON; validating it against a Pydantic model guarantees
    the data is the right shape before downstream code touches it.
- q: How does Pydantic help you get structured output from Claude in the first place?
  options:
  - It rewrites the prompt
  - model_json_schema() produces a JSON Schema you can hand to the model as a tool / output schema
  - It fine-tunes the model
  - It caches responses
  answer: 1
  why: Pydantic can emit a JSON Schema from your model, which you pass as the tool input schema so the
    model is constrained to return data in that exact shape.
- q: 'What does a field default like ''priority: int = 1'' mean in a Pydantic model?'
  options:
  - The field is forbidden
  - The field is optional and becomes 1 if the caller omits it
  - The field must always equal 1
  - The field is a string
  answer: 1
  why: Giving a field a default value makes it optional; if the input omits it, Pydantic fills in the
    default.
- q: In one sentence, what is the difference between parsing and validating that Pydantic does at once?
  answer: Parsing turns raw input like a JSON dict into typed Python objects, and validating checks those
    values obey your declared types and constraints — Pydantic does both when you construct the model.
  why: Pydantic coerces and checks in a single step, so a successfully constructed model is guaranteed
    to be well-formed.
- q: How do you validate a Python dict against a Pydantic model named Ticket?
  answer: Call Ticket.model_validate(data), which returns a validated Ticket instance or raises a ValidationError.
  why: model_validate parses and validates an existing dict (or JSON via model_validate_json), giving
    you a trusted, typed object.
resources:
- label: Pydantic — Official documentation
  url: https://docs.pydantic.dev/latest/
- label: Pydantic — Models and validation
  url: https://docs.pydantic.dev/latest/concepts/models/
- label: Pydantic — JSON Schema
  url: https://docs.pydantic.dev/latest/concepts/json_schema/
- label: Anthropic — Tool use (structured output)
  url: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- label: Anthropic — Increase output consistency with JSON
  url: https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
---

## The data boundary problem

Every production app has a boundary where untrusted data comes in: a user's request, a file, a third-party API — and now, a language model's reply. Inside your app you want **trusted, typed** data. Outside, anything goes. **Pydantic** is the tool that guards that boundary. You declare the shape you expect, and Pydantic parses, coerces, and validates incoming data into clean Python objects — or tells you precisely what was wrong.

For a GenAI engineer this is doubly important, because LLM output is *text the model chose to produce*. It might be perfect JSON, or it might be slightly off. Pydantic lets you refuse to trust it until it's verified.

## Defining a model

A Pydantic model is a class that inherits from `BaseModel` with typed fields.

```python
from pydantic import BaseModel

class Ticket(BaseModel):
    id: int
    title: str
    priority: int = 1          # default makes it optional
    tags: list[str] = []
```

Construct it and Pydantic validates: `Ticket(id="7", title="Login bug")` succeeds and **coerces** `"7"` to the integer `7`. Pass `id="abc"` and it raises a `ValidationError` naming the field and the problem. Parsing and validating happen in one step, so a constructed model is guaranteed well-formed.

## Validating existing data

When the data already exists as a dict or JSON string — like an LLM's reply — use the validate methods.

```python
Ticket.model_validate(some_dict)          # from a dict
Ticket.model_validate_json(raw_json_str)  # from a JSON string
```

Both return a typed `Ticket` or raise `ValidationError`. This is your safety gate.

## Constraints and custom rules

Go beyond types with constraints and validators.

```python
from pydantic import BaseModel, Field, field_validator

class Ticket(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    priority: int = Field(ge=1, le=5)

    @field_validator("title")
    @classmethod
    def no_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title cannot be blank")
        return v
```

Now `priority` must be between 1 and 5, and a blank title is rejected. The rules live with the data, not scattered through your code.

## Pairing with structured LLM output

Here's where it clicks for GenAI. Pydantic can emit a **JSON Schema** from your model, and Claude's **tool use** lets you give the model an input schema it must match. So your Pydantic model becomes the contract on *both* ends.

```python
import anthropic
from anthropic import Anthropic

client = Anthropic()
schema = Ticket.model_json_schema()

resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    tools=[{"name": "emit_ticket",
            "description": "Return the parsed ticket",
            "input_schema": schema}],
    tool_choice={"type": "tool", "name": "emit_ticket"},
    messages=[{"role": "user", "content": raw_email}],
)

tool_use = next(b for b in resp.content if b.type == "tool_use")
ticket = Ticket.model_validate(tool_use.input)   # trusted!
```

Forcing `tool_choice` to your tool makes Claude return arguments shaped like your schema, and `model_validate` confirms it before you trust it. The same pattern works on Amazon Bedrock and Azure. **Generate** the schema from Pydantic, **validate** the reply with Pydantic — one model, both directions.

## Your task

Define a Pydantic `Ticket` model with `id`, `title`, a `priority` between 1 and 5, and `tags`. Ask Claude to parse a messy support email into that shape using its JSON Schema as a tool, then validate the reply with `model_validate` and print the typed object.
