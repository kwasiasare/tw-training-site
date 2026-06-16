---
course: kwasi-GenAI
title: RAG vs fine-tuning
month: 2
monthTitle: Retrieval-Augmented Generation (RAG)
lesson: 6
summary: 'A decision framework for RAG versus fine-tuning: RAG is usually cheaper, updatable, and auditable,
  while fine-tuning earns its place for behaviour and style, not fresh facts.'
objectives:
- Distinguish what RAG changes (knowledge) from what fine-tuning changes (behaviour)
- 'List three reasons RAG is the default: cheaper, updatable, auditable'
- Identify the cases where fine-tuning is genuinely warranted
- Explain why fine-tuning is a poor way to add fresh or frequently-changing facts
- Apply a simple decision framework to a real scenario
- Recognise that RAG and fine-tuning can be combined, not either/or
video: g2-l06-rag-vs-finetuning.mp4
quiz:
- q: What does RAG primarily change about a model's output?
  options:
  - Its tone and format
  - The knowledge it can draw on, by supplying facts at query time
  - Its underlying weights
  - Its token limit
  answer: 1
  why: RAG injects relevant facts into the prompt at run time; it gives the model new knowledge without
    altering the model itself.
- q: What does fine-tuning primarily change?
  options:
  - The facts the model knows today
  - The model's behaviour, style, and format by adjusting its weights on examples
  - The vector database
  - The embedding model
  answer: 1
  why: Fine-tuning trains on examples to shape how the model responds — tone, structure, task-specific
    behaviour — rather than to add fresh, changing facts.
- q: Which is the strongest reason RAG is usually the default over fine-tuning?
  options:
  - It needs no embeddings
  - It is cheaper to build, easy to update, and auditable via citations
  - It makes the model bigger
  - It removes the need for a model
  answer: 1
  why: RAG avoids training cost, updates by changing documents not weights, and lets you trace every answer
    to a source.
- q: Why is fine-tuning a poor choice for adding frequently-changing facts?
  options:
  - It is too cheap
  - Each fact change needs retraining, and the model can't cite its source
  - It updates instantly
  - It stores facts in a database
  answer: 1
  why: Baking facts into weights means re-training to update them and gives no traceable source, whereas
    RAG just swaps a document.
- q: In one sentence, give a case where fine-tuning is genuinely warranted.
  answer: When you need consistent, specialised behaviour or output format that prompting can't reliably
    achieve, on a stable task with many examples.
  why: Fine-tuning shines for durable behaviour and style at scale, not for supplying current information.
- q: 'True or false: RAG and fine-tuning are mutually exclusive. Explain.'
  answer: False — you can fine-tune a model for behaviour and still use RAG to supply current facts; they
    address different problems.
  why: 'They are complementary: tune for how it answers, retrieve for what it knows.'
resources:
- label: Anthropic docs — Fine-tuning Claude on Amazon Bedrock
  url: https://docs.anthropic.com/en/docs/build-with-claude/fine-tuning
- label: AWS — When to use RAG vs fine-tuning
  url: https://aws.amazon.com/blogs/machine-learning/customize-foundation-models-with-rag-fine-tuning-or-both/
- label: Anthropic — Retrieval Augmented Generation overview
  url: https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation
- label: OpenAI docs — When to fine-tune
  url: https://platform.openai.com/docs/guides/fine-tuning
- label: Microsoft Learn — RAG vs fine-tuning
  url: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide
---

## Two different problems

Newcomers treat RAG and fine-tuning as rivals for the same job. They aren't. They change different things:

- **RAG** changes **what the model knows** — it supplies relevant facts at query time, in the prompt. The model's weights never change.
- **Fine-tuning** changes **how the model behaves** — you adjust its weights by training on examples, shaping tone, format, and task-specific behaviour.

A clean way to remember it: **RAG is for knowledge, fine-tuning is for behaviour.** If your problem is "the model doesn't *know* our policies / products / tickets," that's a knowledge problem — reach for RAG. If your problem is "the model doesn't *respond* in our specific style / structure / classification scheme," that's a behaviour problem — fine-tuning may help.

## Why RAG is the default

For the vast majority of "the model needs our information" problems, start with RAG. Three reasons:

1. **Cheaper.** No training run, no GPU bill, no ML pipeline. You build an index and call an API — engineering you already know.
2. **Updatable.** Knowledge changed? Edit, add, or delete a document and re-embed it. The next query sees the new fact *immediately*. No retraining, no redeploy of the model.
3. **Auditable.** Because the facts live in retrievable chunks, every answer can carry a **citation** back to its source (lesson 7). For a security- and compliance-minded engineer this is huge: you can show *why* the system said what it said.

Those three — cheap, updatable, auditable — are exactly the properties you want in production systems, and they're precisely where fine-tuning struggles.

## Why fine-tuning is the wrong tool for fresh facts

Baking facts into weights has two fatal flaws for changing information. First, **updating means retraining**: a price change or a new policy requires a fresh fine-tune, which is slow and costly. Second, **there's no source**: a fine-tuned fact is dissolved into the weights, so the model can't cite where it came from, and you can't easily tell whether it's current or hallucinated. Fine-tuning also risks **stale facts** and is more prone to confidently stating outdated information.

## When fine-tuning is genuinely warranted

Fine-tuning earns its place when the problem is **durable behaviour**, not current facts:

- A **consistent output format or style** that prompting can't reliably enforce at scale.
- A **specialised, narrow task** done at high volume where you want shorter prompts and lower latency (the behaviour is baked in, so you stop spending tokens explaining it).
- **Domain tone or classification schemes** with many high-quality labelled examples and a stable target.

Note the pattern: a **stable task**, **lots of examples**, and a need for **behaviour** rather than **knowledge**. With Claude, fine-tuning is available through platforms like **Amazon Bedrock**, fitting the cloud workflow you already run.

## They combine

This isn't either/or. A mature system can **fine-tune for behaviour and use RAG for facts**: a model tuned to your house style and structure, retrieving current information to answer from. Tune *how* it answers; retrieve *what* it answers about.

## A simple decision framework

Ask, in order: **(1) Is this a knowledge gap?** Use RAG. **(2) Can a better prompt fix it?** Try that before anything heavier. **(3) Is it a stable behaviour/format need with many examples and high volume?** Consider fine-tuning. **(4) Both?** Combine them. Reach for fine-tuning last, deliberately — not as the first lever.

## Your task

Write a one-paragraph recommendation for each of these: (a) a chatbot answering questions over a frequently-updated internal wiki; (b) a service that must always reply as strict JSON in a fixed schema at very high volume. State RAG, fine-tuning, or both, and justify it using the framework.
