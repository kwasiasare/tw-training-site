---
course: kwasi-GenAI
title: Guardrails & output validation
month: 4
monthTitle: Production Engineering
lesson: 6
summary: Stop treating model output as trusted. Validate it against a schema, run allow/deny checks, and
  refuse or repair bad output before it reaches a user or a downstream system.
objectives:
- Explain why LLM output must be validated like any untrusted input
- Enforce structure with JSON schema validation and tool-use / structured outputs
- Apply allow/deny checks for content, topics, and forbidden actions
- Repair malformed output by re-prompting, and refuse when repair fails
- Place guardrails on both the input and the output side of a call
- 'Fail safe: choose safe defaults and clear refusals over wrong answers'
video: g4-l06-guardrails.mp4
quiz:
- q: Why should you treat LLM output as untrusted?
  options:
  - The model is malicious
  - It can be malformed, off-policy, or wrong, and it may flow into downstream systems
  - Output is always encrypted
  - The API requires it
  answer: 1
  why: Model output is probabilistic and can break schemas, violate policy, or be incorrect — and if it
    feeds a database, API, or UI, that's a real risk surface.
- q: What is the most reliable way to get structured output you can parse?
  options:
  - Hope the model returns JSON
  - Use tool-use / structured outputs or validate against a schema and repair on failure
  - Ask once and trust it
  - Lower the temperature only
  answer: 1
  why: Constraining output via tool-use/structured outputs and validating against a schema (then repairing)
    is far more reliable than hoping for clean JSON.
- q: What is an allow/deny check?
  options:
  - A login system
  - A rule that permits only approved content/actions or blocks forbidden ones
  - A rate limiter
  - A caching layer
  answer: 1
  why: Allow/deny checks gate output by policy — allowing only approved topics or actions, or blocking
    forbidden terms, links, or operations.
- q: When schema validation fails, what is a good first response?
  options:
  - Crash the app
  - Re-prompt the model to repair the output, and refuse if it still fails
  - Return the broken output anyway
  - Ignore the error
  answer: 1
  why: Re-prompting with the validation error often fixes malformed output; if repair fails, refuse safely
    rather than passing broken data downstream.
- q: In one sentence, why place guardrails on the input side too, not just the output?
  answer: Checking the input lets you block disallowed requests, strip injected instructions, and enforce
    limits before spending a call, complementing the output checks that catch bad results.
  why: Input guardrails stop bad or abusive requests early and cheaply, while output guardrails catch
    what the model still gets wrong.
- q: In one sentence, what does 'fail safe' mean for an LLM feature?
  answer: When output can't be validated or repaired, return a safe default or a clear refusal rather
    than a wrong or unsafe answer.
  why: A predictable safe failure protects users and downstream systems far better than confidently shipping
    an invalid or harmful result.
resources:
- label: Anthropic — Increase output consistency (structured output)
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/increase-consistency
- label: Anthropic — Tool use (forcing structured calls)
  url: https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
- label: Pydantic — Models and validation
  url: https://docs.pydantic.dev/latest/concepts/models/
- label: Guardrails AI — Validators and output guards
  url: https://www.guardrailsai.com/docs
- label: 'OWASP — LLM05: Improper Output Handling'
  url: https://genai.owasp.org/llmrisk/llm05-improper-output-handling/
---

## Model output is untrusted input

Here's the security reflex you already have, applied to GenAI: **never trust output you didn't validate.** A model's answer is probabilistic. It can return broken JSON, invent a field, drift off policy, propose an unsafe action, or simply be wrong. The danger isn't the text on its own — it's where the text *goes*: into a database, an API call, a shell command, a financial transaction, a rendered web page. OWASP names this **Improper Output Handling**, and treating model output as trusted is exactly the kind of mistake you'd never make with user form input.

## Enforce structure with a schema

If your code parses the output, you must guarantee its shape. Hoping the model returns clean JSON is not a strategy. Two reliable techniques: constrain generation with **tool-use / structured outputs**, and **validate** the result against a schema before using it.

```python
from pydantic import BaseModel, ValidationError

class Ticket(BaseModel):
    category: str
    priority: int      # 1-5
    summary: str

def parse(raw: str) -> Ticket | None:
    try:
        return Ticket.model_validate_json(raw)
    except ValidationError:
        return None
```

A Pydantic model is your contract. If the output doesn't fit — missing field, wrong type, priority out of range — validation fails loudly instead of corrupting data downstream. This is the same input-validation rigour you'd put on any API boundary.

## Allow / deny checks

Structure isn't enough; you also gate **content and actions**. An **allow-list** permits only approved values — a category from a fixed set, a URL from an approved domain, a tool from a whitelist. A **deny-list** blocks forbidden things — leaked secrets, profanity, competitor mentions, dangerous shell commands. For an agent that can act, the highest-value check is on the *action*: this tool call, with these arguments, is it permitted? That's least-privilege, the principle you already enforce on IAM roles, applied to tool use.

## Repair, then refuse

When a check fails, you have a ladder of responses. First, **repair**: hand the validation error back to the model and ask it to fix the output. Re-prompting with the specific problem fixes malformed output surprisingly often.

```python
def robust(raw):
    t = parse(raw)
    if t:
        return t
    fixed = llm(f"Your output failed validation. Return ONLY valid JSON matching the schema. Was: {raw}")
    return parse(fixed)          # may still be None
```

If repair still fails, **refuse**. Return a safe default or a clear message — "I couldn't produce a valid answer" — and never pass broken or off-policy output downstream. A predictable safe failure beats a confident wrong one every time.

## Guard both sides

Guardrails belong on the **input** as well as the output. On the way in, block disallowed requests, enforce length limits, and strip or quarantine instructions hidden in user content (the seed of prompt injection — next lesson). On the way out, run the schema and allow/deny checks. Input guards are cheap and stop bad requests before you spend a call; output guards catch what the model still gets wrong. Libraries like **Guardrails AI** package common validators, and the major clouds offer managed guardrail layers — but the pattern matters more than any one tool.

## Fail safe by default

The governing principle is **fail safe**. When in doubt, choose the safe default, the conservative action, the honest refusal. A user can recover from "I'm not sure, let me get a human"; they cannot recover from a wrong wire transfer or a deleted record. You already build systems that degrade gracefully — bring that instinct here.

## Your task

Define a Pydantic schema for a structured output your app produces. Add a validation step, an allow-list check on at least one field, and a repair-then-refuse path. Feed it three deliberately broken outputs (bad JSON, an out-of-range value, a denied value) and confirm each is repaired or safely refused — never passed through.
