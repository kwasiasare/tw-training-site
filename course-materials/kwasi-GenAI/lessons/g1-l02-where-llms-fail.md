---
course: kwasi-GenAI
title: Where LLMs fail
month: 1
monthTitle: LLM Foundations & API Fluency
lesson: 2
summary: Learn the predictable failure modes of LLMs — hallucination, knowledge cutoff, and weak arithmetic
  and multi-step logic — why each one happens, and the engineering patterns that mitigate them.
objectives:
- Define hallucination and explain why next-token prediction produces it
- Explain knowledge cutoff and why models are stale on recent facts
- Describe why raw LLMs are unreliable at arithmetic and long multi-step logic
- Match each failure mode to a concrete mitigation pattern
- Decide when to add retrieval, tools, or verification to a system
- Treat model output as untrusted input that needs validation
video: g1-l02-where-llms-fail.mp4
quiz:
- q: Why do LLMs hallucinate?
  options:
  - They are connected to a faulty database
  - They generate the most plausible-sounding next tokens, which can be confidently wrong
  - They run out of memory
  - They always copy their training data verbatim
  answer: 1
  why: A model optimises for fluent, plausible continuations, not truth, so it can produce confident statements
    that have no grounding in fact.
- q: What is a knowledge cutoff?
  options:
  - A rate limit on requests
  - The date after which the model has no built-in knowledge of events
  - The maximum output length
  - A billing threshold
  answer: 1
  why: A model only knows what was in its training data up to a cutoff date, so it is unaware of anything
    that happened afterwards unless you supply it.
- q: Why are raw LLMs weak at multi-digit arithmetic?
  options:
  - Arithmetic is banned by the API
  - They predict digit tokens by pattern rather than truly calculating
  - The numbers are too large for the context window
  - They round everything to the nearest hundred
  answer: 1
  why: The model pattern-matches its way through digits instead of executing an exact algorithm, so long
    calculations drift off the correct answer.
- q: Which pattern best mitigates a knowledge-cutoff problem for current events?
  options:
  - Raise the temperature
  - Give the model fresh data via retrieval or a web/search tool
  - Ask the same question twice
  - Shorten the prompt
  answer: 1
  why: Supplying current information in the prompt — through retrieval-augmented generation or a search
    tool — fills the gap the training cutoff leaves.
- q: In one sentence, what is the safest mindset toward LLM output in a production pipeline?
  answer: Treat the model's output as untrusted, unverified input that must be validated, grounded, or
    checked before you act on it.
  why: Like any external input, model output can be wrong or malformed, so guardrails and validation belong
    around it.
- q: Name one reliable way to make an LLM do exact arithmetic.
  answer: Give it a calculator or code-execution tool and have it call that instead of computing the answer
    in its head.
  why: Offloading the calculation to deterministic code removes the model's pattern-matching error entirely.
resources:
- label: Anthropic — Reduce hallucinations
  url: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- label: Anthropic — Tool use overview
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- label: Anthropic — Models overview (knowledge cutoffs)
  url: https://platform.claude.com/docs/en/about-claude/models/overview
- label: Anthropic — Increase output consistency
  url: https://platform.claude.com/docs/en/build-with-claude/define-success
---

## Failures are predictable, not random

In the last lesson you saw that an LLM only predicts the next most-plausible token. That single mechanism explains its strengths *and* its three classic failure modes. Once you can name each one and explain why it happens, you can engineer around it. None of this means the models are bad — it means you treat them like any component with known limits.

## Hallucination

A **hallucination** is a confident statement that is simply not true: a fake citation, an invented API method, a plausible-but-wrong fact. It happens because the model optimises for *plausibility*, not truth. If the most fluent continuation of your prompt is a made-up function name, the model will happily produce it — with the same calm tone it uses for correct answers.

The danger is the confidence. There is no built-in "I don't know" unless the prompt and training encourage it. Mitigations:

- **Ground the model** in real source text (retrieval-augmented generation), and ask it to answer *only* from that text and cite it.
- **Give it permission to say "I don't know"** explicitly in the system prompt.
- **Verify** anything load-bearing — links, numbers, names — with a second check.

## Knowledge cutoff and recency

A model is trained on data up to a **cutoff date**. After that date it knows nothing — not last week's release, not today's prices, not the incident you are debugging right now. Ask about a recent event and it will either admit ignorance or, worse, hallucinate a plausible-sounding answer.

This is not a bug you can prompt away; the information is genuinely absent. The fix is to **bring the data to the model**: retrieve relevant documents and put them in the context window, or give the model a **web search / fetch tool** so it can pull current information itself. As a cloud engineer you already think this way — you wouldn't expect a cached value to reflect a change that happened after it was cached.

## Weak arithmetic and multi-step logic

LLMs are surprisingly shaky at exact arithmetic and long chains of reasoning. Multiply two large numbers and a raw model often produces something *close* but wrong. The reason is the same prediction loop: it pattern-matches digit tokens rather than executing an exact algorithm, and small errors compound across many steps.

The mitigations are pragmatic:

- **Offload the calculation** to a tool — a calculator or a code-execution sandbox — and have the model call it. Deterministic code gives an exact answer every time.
- **Encourage step-by-step reasoning** for logic problems so the model breaks a hard task into smaller, checkable pieces.
- **Verify the result** when correctness matters.

```text
Bad:  "What is 48273 * 1956?"  -> model guesses a close-but-wrong number
Good: model calls a calculator tool -> exact result, every time
```

## The unifying mindset

Notice the pattern across all three: the fix is rarely "prompt harder." It is to **add structure around the model** — grounding for hallucination, fresh data for recency, tools for math and logic — and to treat every output as untrusted input that earns trust only after validation. This is exactly the security-and-reliability instinct you already have. Modules 2 and beyond build directly on these mitigations.

## Your task

Write down a real question from your own work for each failure mode — one that would trigger a hallucination, one blocked by knowledge cutoff, and one requiring exact arithmetic — and note the single mitigation you would reach for in each case.
