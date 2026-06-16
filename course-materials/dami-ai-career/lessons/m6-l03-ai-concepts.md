---
course: dami-ai-career
title: AI/LLM concept interview questions
month: 6
monthTitle: Apply & Interview
lesson: 3
summary: Answer common AI and large language model interview questions clearly, covering tokens, embeddings,
  prompting, RAG, fine-tuning, and evaluation.
objectives:
- Explain what a large language model is and how next-token prediction works
- Describe tokens, context windows, and why they matter for cost and limits
- Contrast prompting, retrieval-augmented generation, and fine-tuning
- Explain embeddings and how similarity search powers RAG
- Define hallucination and name practical ways to reduce it
- Discuss temperature, system prompts, and how to evaluate model outputs
- Make a calibrated Claude Messages API call and read the response
video: m6-l03-ai-concepts.mp4
quiz:
- q: What is an LLM fundamentally trained to do?
  options:
  - Look answers up in a database
  - Predict the next token given the previous ones
  - Run Python code internally
  - Search the live internet
  answer: 1
  why: 'An LLM is a next-token predictor: given prior tokens it outputs a probability distribution over
    the next token, sampled repeatedly.'
- q: What is a token?
  answer: A token is a chunk of text (often a word piece or few characters) that the model reads and generates
    one at a time.
  why: Models work in tokens, not characters or whole words; roughly 3-4 characters of English per token,
    which drives context limits and cost.
- q: Which technique gives a model fresh, private knowledge WITHOUT retraining weights?
  options:
  - Fine-tuning
  - Retrieval-augmented generation (RAG)
  - Increasing temperature
  - Quantisation
  answer: 1
  why: RAG retrieves relevant documents at query time and adds them to the prompt, so the model answers
    from current data without changing its weights.
- q: What does raising the temperature do to model output?
  options:
  - Makes it faster
  - Makes it more random and varied
  - Makes it always factual
  - Reduces token cost
  answer: 1
  why: Higher temperature flattens the probability distribution, increasing randomness and creativity;
    lower temperature makes output more focused and deterministic.
- q: What is a hallucination in an LLM, and name one way to reduce it?
  answer: A confident but false or fabricated answer; reduce it with RAG, asking for citations, lower
    temperature, or telling the model to say 'I don't know'.
  why: LLMs generate plausible text, not verified facts; grounding the model in retrieved sources and
    allowing uncertainty cuts fabrication.
- q: What is an embedding used for in a RAG system?
  answer: A vector representing text meaning, so similar texts sit close together and you can find relevant
    documents by similarity search.
  why: Embeddings turn text into numbers; nearest-neighbour search over those vectors retrieves the most
    relevant chunks to feed the model.
resources:
- label: Anthropic — Claude Messages API documentation
  url: https://docs.anthropic.com/en/api/messages
- label: Anthropic — Prompt engineering overview
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- label: Jay Alammar — The Illustrated Transformer
  url: https://jalammar.github.io/illustrated-transformer/
- label: OpenAI — What are embeddings (guide)
  url: https://platform.openai.com/docs/guides/embeddings
---

## What interviewers are really testing

In an A I or L L M concept interview, nobody expects you to have trained a model from scratch. They want to know you understand **what these systems are**, **where they break**, and **how to use them responsibly**. Clear, honest explanations beat buzzwords every time.

As a maths graduate you have an edge: probability, vectors, and linear algebra are exactly the language under the hood.

## What is an LLM?

A **large language model** is a neural network trained on huge amounts of text to do one deceptively simple thing: **predict the next token**. Given the tokens so far, it outputs a probability distribution over the next token, picks one, appends it, and repeats. Everything else — answering questions, writing code, summarising — emerges from that loop.

A **token** is a chunk of text, usually a word piece. The **context window** is how many tokens the model can see at once. Both cost and limits are measured in tokens.

## Prompting vs RAG vs fine-tuning

Three ways to make a model do what you want:

- **Prompting** — change the instructions you send. Fastest, cheapest, no training.
- **Retrieval-augmented generation (RAG)** — fetch relevant documents and paste them into the prompt so the model answers from your data.
- **Fine-tuning** — retrain the weights on examples to change style or behaviour. Most expensive; use last.

Rule of thumb: try prompting, then RAG, then fine-tuning.

## Embeddings and similarity search

RAG depends on **embeddings**: a model turns text into a vector of numbers so that texts with similar meaning sit close together. To find relevant context you embed the question and search for the nearest document vectors.

```python
import numpy as np

def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))

# 1.0 means identical direction; near 0 means unrelated
print(cosine([1, 0, 1], [1, 0, 1]))   # 1.0
```

## Calling a model: the Claude Messages API

When asked to show code, use the **Anthropic Claude Messages API**. Keep your key in an environment variable, never in code.

```python
from anthropic import Anthropic

client = Anthropic()   # reads ANTHROPIC_API_KEY from env

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    temperature=0.2,
    messages=[{"role": "user", "content": "Explain tokens in one sentence."}],
)

print(msg.content[0].text)
```

Lower `temperature` for factual tasks, higher for creative ones. Model ids you should know: `claude-opus-4-8` (most capable), `claude-sonnet-4-6` (balanced), `claude-haiku-4-5` (fast and cheap).

## Hallucinations and evaluation

A **hallucination** is a confident but false answer. The model generates plausible text, not verified truth. Reduce it by grounding the model in retrieved sources (RAG), asking for citations, lowering temperature, and explicitly allowing it to say *"I don't know"*.

To **evaluate** outputs, build a small test set of inputs with expected answers, then score with exact-match, human review, or an L L M-as-judge. Always measure before and after a change.

## Your task

Write a one-paragraph answer, out loud, to each of these: *What is a token? What is RAG? What is a hallucination and how do you reduce it?* Record yourself and tighten until each is under thirty seconds.
