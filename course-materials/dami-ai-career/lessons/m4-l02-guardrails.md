---
course: dami-ai-career
title: Guardrails & hallucination control
month: 4
monthTitle: Portfolio Projects
lesson: 2
summary: Keep your AI app safe and honest by validating inputs and outputs, grounding answers in retrieved
  facts, and saying "I don't know".
objectives:
- Explain what a hallucination is and why LLMs produce them
- Add input guardrails to block prompt injection and off-topic requests
- Add output guardrails that validate structure and content before use
- Ground answers in retrieved context and cite sources
- Force structured JSON output and validate it with a schema
- Let the model abstain and say 'I don't know' when unsure
- Log refusals and failures so you can measure and improve
video: m4-l02-guardrails.mp4
quiz:
- q: What is an LLM 'hallucination'?
  options:
  - A network timeout
  - Confident, fluent output that is factually wrong or made up
  - A request that gets blocked
  - Output that is too short
  answer: 1
  why: A hallucination is plausible-sounding text the model invented; it is not grounded in any real source
    and may be completely false.
- q: Why does grounding (RAG) reduce hallucinations?
  options:
  - It makes the model bigger
  - It gives the model real source text to answer from
  - It lowers the temperature
  - It hides the system prompt
  answer: 1
  why: By retrieving relevant documents and putting them in the prompt, the model answers from supplied
    facts instead of guessing from memory.
- q: What is the safest behaviour when the context does not contain the answer?
  options:
  - Guess the most likely answer
  - Return an empty string
  - Say 'I don't know' or that the answer isn't in the sources
  - Repeat the question
  answer: 2
  why: 'Abstaining is correct: a confident wrong answer is far more dangerous than admitting the information
    is missing.'
- q: Name one input guardrail you can add before sending a user's message to the model.
  answer: Detect and block prompt injection / off-topic / disallowed requests (e.g. with a classifier,
    allowlist, or moderation check).
  why: Input guardrails stop malicious or out-of-scope requests reaching the model, reducing both abuse
    and wasted cost.
- q: Why validate the model's output against a JSON schema before using it?
  answer: The model can return malformed or unexpected JSON; validating catches it so your app doesn't
    crash or act on bad data.
  why: 'Treat model output as untrusted input: parse, validate the shape and values, and reject anything
    that fails before it reaches downstream code.'
- q: Which setting most directly makes answers more repeatable and less random?
  options:
  - A higher temperature
  - A lower temperature
  - More max_tokens
  - A longer system prompt
  answer: 1
  why: Lower temperature makes sampling more deterministic, which is useful for factual, structured, or
    guardrailed tasks.
resources:
- label: Anthropic — Reduce hallucinations (prompt engineering guide)
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/reduce-hallucinations
- label: Anthropic — Increase output consistency (JSON & structure)
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/increase-consistency
- label: OWASP Top 10 for LLM Applications
  url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- label: Pydantic — Models & validation (official docs)
  url: https://docs.pydantic.dev/latest/concepts/models/
---

## What is a hallucination?

A **hallucination** is when a language model produces output that sounds confident and fluent but is factually wrong or completely made up. Large language models predict the next likely token from patterns in their training data — they have no built-in sense of truth. So when they don't know something, they often *guess* in a way that reads exactly like a correct answer.

For a portfolio project this matters enormously. A demo that invents a fake legal clause, a wrong dosage, or a non-existent function call looks impressive until someone checks it. **Guardrails** are the controls you put around the model to catch problems before they reach the user.

## Input guardrails

The first line of defence is checking the request *before* it reaches the model. This blocks **prompt injection** (a user trying to override your instructions), off-topic requests, and obvious abuse — and saves you the API cost of a doomed call.

```python
BANNED = ["ignore previous", "reveal your prompt", "system prompt"]

def check_input(text: str) -> bool:
    low = text.lower()
    if any(phrase in low for phrase in BANNED):
        return False        # block it
    if len(text) > 4000:
        return False        # too long / suspicious
    return True
```

Keyword lists are crude; in production you'd use a small classifier or a moderation model. But the idea is the same: **untrusted input is validated first.**

## Grounding: answer from sources

The single most effective way to cut hallucinations is **grounding** — retrieve real documents and tell the model to answer *only* from them. This is the core of Retrieval-Augmented Generation (RAG). Crucially, you also give the model permission to abstain.

```python
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

SYSTEM = (
    "Answer using ONLY the provided context. "
    "If the answer is not in the context, reply exactly: "
    "'I don't know based on the provided sources.' Cite the source id."
)

def ask(question: str, context: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0,
        system=SYSTEM,
        messages=[{"role": "user",
                   "content": f"Context:\n{context}\n\nQuestion: {question}"}],
    )
    return msg.content[0].text
```

Setting `temperature=0` makes answers more deterministic, and the system prompt makes "I don't know" an acceptable, expected output.

## Output guardrails & structured output

Treat the model's reply as **untrusted output**. Ask for JSON, then *validate* it with a schema before any downstream code uses it. If validation fails, you can reject, retry, or fall back — never act on unverified data.

```python
from pydantic import BaseModel, ValidationError
import json

class Answer(BaseModel):
    answer: str
    confidence: float
    source_id: str

def validate(raw: str) -> Answer | None:
    try:
        return Answer(**json.loads(raw))
    except (ValidationError, json.JSONDecodeError):
        return None   # malformed -> reject and retry
```

## Logging, evaluation & the abstain rule

Guardrails are only useful if you **measure** them. Log every blocked input, every failed validation, and every "I don't know". Those logs become your evaluation set: you can count how often the model abstains correctly versus hallucinates.

A simple rule sums it up: **a confident wrong answer is worse than an honest "I don't know".** Reward abstention. Your task: add input checks, grounding, and JSON validation to one of your portfolio apps, and log every refusal.
