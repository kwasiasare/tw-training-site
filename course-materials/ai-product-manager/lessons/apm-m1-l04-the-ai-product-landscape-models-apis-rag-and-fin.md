---
course: ai-product-manager
title: 'The AI Product Landscape: Models, APIs, RAG, and Fine-Tuning'
month: 1
monthTitle: AI Literacy and LLM Foundations for PMs
lesson: 4
summary: 'This lesson gives AI PMs a practical map of the AI product landscape: foundation models, hosted
  APIs, retrieval-augmented generation (RAG), and fine-tuning. You''ll learn the trade-offs of each approach
  across cost, latency, accuracy, control, and maintenance, and practice choosing the right pattern for
  a given use case in a structured comparison brief.'
objectives:
- Distinguish foundation models, hosted model APIs, RAG, and fine-tuning, and explain what problem each
  solves
- Compare build-vs-buy options across cost, latency, data control, accuracy, and maintenance trade-offs
- Match common use cases (e.g. Q&A over docs, brand voice, domain knowledge) to the appropriate architectural
  pattern
- Identify when RAG, fine-tuning, or both are needed versus prompt engineering alone
- Draft a one-page comparison brief that justifies an architecture recommendation to stakeholders
video: apm-m1-l04-the-ai-product-landscape-models-apis-rag-and-fin.mp4
quiz:
- q: A support team wants a chatbot to answer questions using their constantly-updated help center articles,
    with citations. Which approach fits best?
  options:
  - Fine-tune a model on the help articles
  - Hosted API with RAG over the help center
  - Self-host an open model with no retrieval
  - Prompt engineering alone with no data access
  answer: 1
  why: The knowledge is proprietary and frequently changing and needs citations — RAG retrieves current
    content at query time without retraining, unlike fine-tuning which goes stale and can't cite sources.
- q: What does fine-tuning do best?
  options:
  - Teach the model new, frequently-changing facts
  - Shape consistent tone, format, or narrow-task behavior
  - Eliminate the need for any evaluation
  - Reduce vendor dependency to zero
  answer: 1
  why: Fine-tuning changes behavior — style, format, narrow tasks. It's unreliable for teaching facts
    (use RAG) and doesn't remove the need for evaluation.
- q: Which approach generally offers the fastest time to ship for an MVP?
  options:
  - Self-hosted open-source model
  - Fine-tuned model from scratch
  - Hosted API with prompt engineering
  - Building your own foundation model
  answer: 2
  why: Calling a hosted API with prompt engineering requires no infrastructure or training and can produce
    a working product in days.
- q: When is self-hosting an open model most justified?
  options:
  - When you want the fastest possible MVP
  - When data residency, privacy, regulation, or high-volume economics require it
  - Whenever you need the model to cite sources
  - Only when prompt engineering fails
  answer: 1
  why: Self-hosting trades higher operational cost for maximum control — justified by privacy, regulatory,
    residency, or large-scale cost reasons, not speed.
- q: In one or two sentences, explain the 'knowledge vs behavior' rule for choosing between RAG and fine-tuning.
  answer: Use RAG when the model needs to know new or changing facts, since it retrieves your data at
    query time; use fine-tuning when the model needs to behave a certain way, such as tone, format, or
    a narrow task. They solve different problems and are often combined.
  why: 'This captures the core heuristic: RAG injects knowledge, fine-tuning shapes behavior, and prompt
    engineering should be tried first for light steering.'
- q: Name two 'hidden' costs an AI PM should include in a comparison brief beyond per-token price.
  answer: Evaluation pipelines, monitoring, ongoing maintenance/retraining, infrastructure/ops, and vendor
    risk are all valid examples.
  why: Total cost of ownership includes evals, monitoring, retraining stale fine-tunes or RAG indexes,
    and infrastructure — ignoring these leads to bad build-vs-buy decisions.
resources:
- label: 'OpenAI: Best practices and when to fine-tune vs use RAG'
  url: https://platform.openai.com/docs/guides/optimizing-llm-accuracy
- label: 'Anthropic: Retrieval-augmented generation guide'
  url: https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation
- label: 'AWS: Build vs buy for generative AI (Bedrock overview)'
  url: https://aws.amazon.com/bedrock/
- label: 'a16z: Emerging Architectures for LLM Applications'
  url: https://a16z.com/emerging-architectures-for-llm-applications/
---

## Why this matters

As an AI PM, one of your earliest and most consequential decisions is *how* you'll deliver intelligence: which model, hosted or self-managed, and which architectural pattern wraps around it. Get this wrong and you over-spend, under-deliver on accuracy, or build something you can't maintain. This lesson gives you a decision framework, not deep ML theory.

## The four building blocks

### 1. Foundation models
Large pre-trained models (GPT-4, Claude, Gemini, Llama, Mistral) trained on broad data. They are the raw engine. You rarely train one yourself — that costs millions. Your choice is which one to *use* and *how*.

### 2. Hosted model APIs (buy)
You call a provider's model over an API (OpenAI, Anthropic, Google, Bedrock). You pay per token. Fast to ship, no infra, always-improving models, but you give up some data control and depend on a vendor.

### 3. RAG (Retrieval-Augmented Generation)
You keep your own knowledge in a vector database (or search index), retrieve relevant chunks at query time, and inject them into the prompt. The model 'reads' your data without being retrained. Best for **fresh, proprietary, or frequently-changing knowledge** and when you need citations.

### 4. Fine-tuning
You further train a base model on your examples so it internalizes a **style, format, or narrow task**. Good for consistent tone, structured outputs, or classification at scale. It does *not* reliably teach new facts and must be redone when data changes.

## The mental model: knowledge vs behavior

- Need the model to **know new facts**? → RAG (or tools/APIs).
- Need the model to **behave a certain way** (tone, format, task)? → Fine-tuning.
- Need just a little steering? → **Prompt engineering** first — it's free and instant.
- These combine: many production systems use a hosted API + RAG + light prompt engineering, and add fine-tuning only when justified.

## Build vs buy spectrum

| Approach | Time to ship | Cost profile | Data control | Best for |
|---|---|---|---|---|
| Hosted API + prompting | Days | Per-token, low upfront | Lower (vendor) | MVPs, general tasks |
| Hosted API + RAG | Weeks | Per-token + infra for retrieval | Medium | Q&A over your docs |
| Fine-tuned hosted model | Weeks–months | Training + serving cost | Medium | Consistent style/format/task |
| Self-hosted open model | Months | High infra + ops | Highest | Privacy, scale economics, regulation |

## Decision heuristics

1. **Start cheap and fast.** Try prompt engineering on a hosted API before anything else.
2. **Add RAG when answers depend on your data** or need to be current and cited.
3. **Fine-tune for behavior, not knowledge** — and only after prompting plateaus.
4. **Self-host when** data residency, privacy, regulatory, or high-volume cost reasons demand it.
5. **Watch total cost of ownership:** eval pipelines, monitoring, retraining, and vendor risk, not just per-token price.

## The comparison brief (your deliverable)

A one-pager that, for a specific use case, lists: the problem and success metric, 2–3 candidate approaches, a trade-off table (cost, latency, accuracy, data control, maintenance), risks, and a recommendation with rationale. This is the artifact you'll bring to engineering and leadership.

## Common pitfalls

- Jumping to fine-tuning to 'teach facts' — usually the wrong tool; use RAG.
- Ignoring evaluation: you can't compare approaches without a test set and metrics.
- Underestimating maintenance: RAG indexes go stale; fine-tunes need re-training; vendors change models.
- Optimizing per-token cost while ignoring engineering and ops cost.
