---
course: ai-product-manager
title: 'Capabilities vs. Limits: Hallucinations, Bias, and Cost Realities'
month: 1
monthTitle: AI Literacy and LLM Foundations for PMs
lesson: 3
summary: A practical lesson helping aspiring AI Product Managers map LLM strengths and weaknesses—covering
  hallucinations, bias, and cost realities—then translate that understanding into a concrete risk-and-mitigation
  document for a sample product idea.
objectives:
- Distinguish tasks where LLMs reliably excel from those where they systematically fail
- Explain why hallucinations occur and identify product patterns that reduce their impact
- Recognize sources of bias in LLM outputs and the product-level mitigations available
- Estimate and reason about the cost drivers (tokens, model tier, volume) of an LLM feature
- Produce a risk-and-mitigation note for a sample AI product idea
video: apm-m1-l03-capabilities-vs-limits-hallucinations-bias-and-c.mp4
quiz:
- q: Which task is an LLM most reliably suited for?
  options:
  - Recalling exact statistics from memory
  - Summarizing a document you provide
  - Performing precise multi-step arithmetic
  - Guaranteeing the same answer every time
  answer: 1
  why: LLMs excel at transforming or synthesizing text you hand them; summarization over provided context
    is a strong fit, while exact recall, math, and determinism are weak points.
- q: What is the primary cause of hallucinations in LLMs?
  options:
  - The model runs out of memory
  - The model optimizes for plausible text rather than truth
  - Insufficient compute at inference
  - Users typing poorly worded prompts
  answer: 1
  why: LLMs generate the most likely next tokens, with no built-in mechanism for verifying truth or signaling
    uncertainty, so they can produce confident but false output.
- q: Which is the most effective product-level mitigation for hallucinations?
  options:
  - Increasing the output token limit
  - Grounding responses in retrieved sources with citations
  - Using a larger frontier model only
  - Removing the system prompt
  answer: 1
  why: Retrieval-augmented generation grounds answers in real sources and lets you cite them, directly
    reducing fabricated facts; bigger models alone do not eliminate hallucination.
- q: Which factor does NOT directly increase per-request LLM cost?
  options:
  - Longer input context
  - More output tokens
  - Choosing a higher model tier
  - Caching repeated system prompts
  answer: 3
  why: Caching reduces cost by reusing work; input length, output length, and model tier all increase
    cost per request.
- q: In one sentence, name two ways bias can show up in LLM outputs.
  answer: Bias can appear as stereotyped content skewed by gender, race, or geography, and as uneven response
    quality across different languages or user groups.
  why: Bias stems from patterns in training data and manifests both as skewed content and as inconsistent
    quality across populations, which is why segment testing matters.
- q: What should an AI PM produce before writing detailed PRD requirements for an LLM feature?
  answer: A risk and mitigation note covering the task, capability fit, top failure modes, mitigations,
    an eval plan, and a cost estimate.
  why: This one-pager aligns engineering, design, and legal on what 'good' and 'risky' mean, grounding
    the roadmap in realistic capabilities before committing requirements.
resources:
- label: 'OpenAI Documentation: Prompt engineering and best practices'
  url: https://platform.openai.com/docs/guides/prompt-engineering
- label: 'Anthropic: Reducing hallucinations and using retrieval'
  url: https://docs.anthropic.com/en/docs/build-with-claude/reduce-hallucinations
- label: Google People + AI Guidebook (designing for AI errors and trust)
  url: https://pair.withgoogle.com/guidebook/
- label: OpenAI Pricing (token-based cost reference)
  url: https://openai.com/api/pricing/
---

## Why This Matters

As an AI PM, your edge is judgment: knowing what large language models (LLMs) can and cannot do *before* you commit a roadmap. Overpromising leads to broken trust; underusing leads to missed opportunity. This lesson gives you a mental model for capabilities, the three biggest failure modes (hallucination, bias, cost), and a lightweight artifact you can ship to your team.

## What LLMs Do Well

LLMs are strong at language transformation tasks where fluency matters more than ground truth, and where a human can verify output cheaply:

- **Summarization & rewriting** — condensing, changing tone, translating.
- **Drafting** — first-pass emails, code, marketing copy.
- **Extraction & classification** — pulling fields from text, tagging sentiment.
- **Synthesis over provided context** — answering from documents you give it (retrieval-augmented).

The common thread: the model is *manipulating text it was handed* or producing a draft a human reviews. Risk stays low.

## Where LLMs Fail

- **Factual recall without sources** — models predict plausible tokens, not truth.
- **Precise math and counting** — unreliable without tools.
- **Fresh or private knowledge** — training cutoff and no access to your data unless you supply it.
- **Long-horizon reasoning & strict logic** — degrades over multi-step chains.
- **Determinism** — the same prompt can yield different answers.

## Hallucinations

A hallucination is a confident, fluent output that is false or fabricated. It happens because the model optimizes for *likely* text, not *correct* text. There is no built-in 'I don't know.'

**Product mitigations:**
- Ground responses in retrieved sources (RAG) and cite them.
- Constrain scope: narrow tasks hallucinate less than open-ended ones.
- Add verification layers (rules, second model, human review) for high-stakes outputs.
- Design UI that signals uncertainty and makes correction easy.
- Measure: track a hallucination rate on a labeled eval set.

## Bias

LLMs learn patterns from internet-scale data, including societal biases. Outputs can skew by gender, race, geography, or reinforce stereotypes. Bias also appears as uneven quality across languages or user groups.

**Product mitigations:**
- Define fairness requirements for your use case early.
- Test across representative user segments and edge cases.
- Use system prompts and guardrails to set tone and refuse harmful asks.
- Keep a human in the loop for consequential decisions (hiring, lending, moderation).
- Document known limitations to users.

## Cost Realities

LLM cost is driven by **tokens** (roughly 0.75 words per token), split into input (prompt + context) and output tokens, multiplied by **price per token** for the chosen model tier and your **request volume**.

Key levers:
- **Model tier**: a frontier model can cost 10–30x a small one. Match model to task difficulty.
- **Context size**: long RAG contexts and chat history inflate input tokens every call.
- **Output length**: cap max tokens; ask for concise answers.
- **Caching & batching**: reuse results; cache system prompts.
- **Latency vs. cost vs. quality** is a triangle — you usually pick two.

A rough unit-economics check: `cost per request = (input_tokens + output_tokens) / 1000 * price_per_1k`. Multiply by expected requests per user per month to sanity-check margins.

## The Artifact: A Risk & Mitigation Note

For any AI feature, write a one-pager with: the task, why an LLM fits, top 3 failure modes, mitigations, an eval plan, and a cost estimate. Below is a template you'll fill in for a sample idea (e.g., an AI assistant that drafts customer-support replies from a help-center knowledge base).

| Section | Content |
|---|---|
| Task | Draft support replies grounded in help docs |
| Capability fit | Summarization + synthesis over provided context — strong fit |
| Hallucination risk | May invent policies; mitigate with RAG + citations + agent review |
| Bias risk | Tone may vary by customer name/locale; test segments, fix system prompt |
| Cost | ~1.5k input + 0.3k output tokens/reply; pick mid-tier model; cap output |
| Eval plan | 100 labeled tickets, track accuracy, hallucination rate, agent edit rate |

Ship this note before writing a single PRD requirement. It aligns engineering, design, and legal on what 'good' and 'risky' mean.
