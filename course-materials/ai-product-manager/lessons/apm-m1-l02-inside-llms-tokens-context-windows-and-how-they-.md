---
course: ai-product-manager
title: 'Inside LLMs: Tokens, Context Windows, and How They Generate Text'
month: 1
monthTitle: AI Literacy and LLM Foundations for PMs
lesson: 2
summary: A practical introduction to how large language models actually work—tokens, context windows,
  and next-token prediction—so PMs can make sound product decisions and explain LLMs clearly to non-technical
  teammates. You'll finish by drafting a one-page LLM explainer.
objectives:
- Explain what tokens are and how they affect cost, latency, and product limits
- Describe context windows and reason about what fits in a single prompt
- Explain how LLMs generate text via next-token prediction and sampling parameters
- Connect model mechanics (temperature, context limits, tokenization) to concrete product trade-offs
- Produce a one-page LLM explainer that demystifies LLMs for non-technical stakeholders
video: apm-m1-l02-inside-llms-tokens-context-windows-and-how-they-.mp4
quiz:
- q: Approximately how many tokens does an English word average?
  options:
  - About 0.1 tokens
  - About 0.75 tokens
  - About 4 tokens
  - About 10 tokens
  answer: 1
  why: An English word averages roughly 0.75 tokens (a token is ~4 characters), so token counts are usually
    a bit higher than word counts.
- q: What does the context window represent?
  options:
  - The total tokens a model was trained on
  - The maximum tokens the model can consider in one request, input plus output
  - The number of users who can chat at once
  - The model's long-term memory across all conversations
  answer: 1
  why: The context window is the maximum tokens (prompt + generated output) the model can attend to in
    a single request; it is not persistent memory across calls.
- q: Why can the same prompt produce different answers?
  options:
  - The model edits its training data each time
  - Text generation samples from a probability distribution over next tokens
  - Tokens change size between requests
  - The context window resets randomly
  answer: 1
  why: Generation is probabilistic—the model samples the next token from a distribution—so outputs can
    vary, especially at higher temperature.
- q: A teammate wants to 'just paste our entire 200-page manual into every prompt' so the model always
    knows everything. What's the best PM response?
  options:
  - Great idea, do it for every call
  - That likely exceeds the context window and raises cost/latency; use retrieval to include only relevant
    parts
  - Increase the temperature instead
  - Tokens don't apply to documents
  answer: 1
  why: Large documents often exceed the context window and inflate cost and latency; retrieval (RAG) pulls
    only relevant chunks, which is more efficient and effective.
- q: In one sentence, explain why LLMs hallucinate.
  answer: Because they generate text by predicting statistically likely next tokens rather than looking
    up verified facts, they can produce plausible-sounding but false content.
  why: 'Hallucination stems from the next-token prediction mechanism: the model optimizes for plausibility,
    not truth, so confident errors occur.'
- q: Which temperature setting is most appropriate for a structured data-extraction task that must be
    consistent?
  options:
  - A high temperature near 1.0+
  - A temperature near 0
  - Temperature has no effect on consistency
  - The maximum possible temperature
  answer: 1
  why: A low temperature (near 0) makes output more deterministic and repeatable, which is ideal for extraction
    and other tasks that require consistency.
resources:
- label: OpenAI Tokenizer (visualize how text splits into tokens)
  url: https://platform.openai.com/tokenizer
- label: 'OpenAI Guide: Prompt engineering and generation parameters'
  url: https://platform.openai.com/docs/guides/prompt-engineering
- label: 'Anthropic: Introduction to context windows and prompting'
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- label: What Is ChatGPT Doing... and Why Does It Work? (Stephen Wolfram)
  url: https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/
---

## Why PMs Need to Understand LLM Mechanics

As an AI PM you don't need to train models, but you do need a working mental model of how LLMs operate. The three concepts that drive most product decisions—cost, latency, quality, and reliability—are **tokens**, **context windows**, and **next-token generation**. Understanding these lets you scope features realistically, estimate costs, and translate engineering reality to business stakeholders.

## Tokens: The Unit of Everything

LLMs don't read words or characters—they read **tokens**. A token is a chunk of text, roughly 4 characters or about 0.75 words in English. "Tokenization" is the process of splitting input text into these chunks using a learned vocabulary.

- Common words are often one token (`apple`). Rare words split into several (`tokenization` → `token` + `ization`).
- Whitespace and punctuation count. Code, JSON, and non-English text often use more tokens per word.
- **Both input and output are billed in tokens.** A 500-word prompt plus a 500-word answer is roughly 1,300 tokens.

**Why it matters for product:** pricing is per-token, so prompt design directly affects unit economics. Latency also scales with output tokens—long responses feel slow because the model generates one token at a time.

## Context Windows: The Model's Working Memory

The **context window** is the maximum number of tokens the model can consider at once—input prompt plus generated output combined. Models range from a few thousand tokens to hundreds of thousands or more.

- Anything outside the window is invisible to the model. The model has **no memory** between separate API calls unless you re-send the relevant text.
- "Memory" in chat apps is an illusion: the app re-sends prior conversation each turn until it no longer fits, then truncates or summarizes.
- Bigger windows cost more and can be slower; relevant context beats maximum context.

**Why it matters for product:** features like "summarize this 100-page doc" or "remember my preferences" require deliberate engineering—chunking, retrieval (RAG), or summarization—not just a bigger prompt.

## How LLMs Generate Text: Next-Token Prediction

At its core, an LLM is a very sophisticated autocomplete. Given a sequence of tokens, it predicts a **probability distribution over the next token**, picks one, appends it, and repeats. That's it.

- There is no database lookup and no guaranteed truth—just statistical prediction learned from training data. This is why models **hallucinate** plausible-sounding but false content.
- **Temperature** controls randomness: low (≈0) is more deterministic and focused; high (≈1+) is more creative and varied.
- **Top-p / top-k** limit which candidate tokens are considered, another lever on creativity vs. consistency.
- Output is generated sequentially (streaming), which is why you see text appear word by word.

**Why it matters for product:** because output is probabilistic, the same prompt can give different answers. Plan for variability with evaluations, guardrails, and human review where stakes are high.

## Connecting Mechanics to Product Decisions

| Concept | Product lever | Trade-off |
|---|---|---|
| Tokens | Prompt length, output length | Cost & latency vs. richness |
| Context window | How much you can include | More context vs. cost/speed |
| Temperature | Determinism | Consistency vs. creativity |
| Next-token prediction | Reliability | Flexibility vs. hallucination risk |

## Your Deliverable: The One-Page Explainer

Create a single page for non-technical teammates that covers: (1) what a token is and why it affects cost, (2) what the context window is and why the model 'forgets,' (3) that the model predicts text and can be confidently wrong, and (4) three implications for our product. Use plain language and one concrete analogy per concept. Keep it skimmable—headers, short bullets, no jargon without a definition.
