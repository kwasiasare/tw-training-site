---
course: dami-ai-career
title: Embeddings & semantic similarity
month: 3
monthTitle: LLM Application Skills
lesson: 7
summary: Turn text into vectors so a computer can measure meaning, then use distance to find what is semantically
  similar.
objectives:
- Explain what a text embedding is and why it is a vector
- Describe how similar meanings map to nearby vectors
- Compute cosine similarity between two embeddings
- Generate embeddings with a real embeddings API
- Build a tiny semantic search over a list of documents
- Know when to use embeddings versus keyword search
- Recognise embeddings as the foundation of RAG
video: m3-l07-embeddings.mp4
quiz:
- q: What is a text embedding?
  options:
  - A compressed copy of the text
  - A list of numbers (a vector) representing the meaning of the text
  - A summary written by the model
  - The raw token IDs of the text
  answer: 1
  why: An embedding is a fixed-length vector of numbers; texts with similar meaning get vectors that point
    in similar directions.
- q: Two sentences with similar meaning will have embeddings that are...
  options:
  - Far apart / pointing in different directions
  - Identical
  - Close together / pointing in a similar direction
  - Always the same length string
  answer: 2
  why: 'Semantic similarity shows up as geometric closeness: similar meaning means a small angle between
    the vectors.'
- q: Which measure is most commonly used to compare two embeddings?
  options:
  - Cosine similarity
  - String length
  - Edit distance
  - Alphabetical order
  answer: 0
  why: Cosine similarity measures the angle between two vectors, ignoring their magnitude, so it captures
    direction (meaning).
- q: Cosine similarity returns 1.0 for two vectors. What does that tell you?
  answer: They point in exactly the same direction, so the texts are maximally similar in meaning.
  why: Cosine similarity ranges from -1 to 1; 1 means identical direction, 0 means unrelated, and negative
    means opposite direction.
- q: Why would you choose embeddings over plain keyword search?
  answer: Embeddings match on meaning, so they find relevant results even when the exact words differ
    (e.g. 'car' vs 'automobile').
  why: Keyword search needs matching words; embeddings capture semantic meaning, handling synonyms and
    paraphrases.
- q: Embeddings are the first step in which common LLM pattern?
  options:
  - Fine-tuning
  - RAG (Retrieval-Augmented Generation)
  - Tokenisation
  - Quantisation
  answer: 1
  why: RAG embeds your documents, retrieves the most similar ones to a question, and feeds them to the
    model as context.
resources:
- label: Anthropic docs — Embeddings (how to use them with Claude)
  url: https://docs.anthropic.com/en/docs/build-with-claude/embeddings
- label: Cohere — Introduction to Text Embeddings
  url: https://docs.cohere.com/docs/embeddings
- label: scikit-learn — cosine_similarity reference
  url: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
- label: 3Blue1Brown — Vectors, the basics (YouTube)
---

## What is an embedding?

An **embedding** is a list of numbers — a **vector** — that represents the *meaning* of a piece of text. A model reads your sentence and outputs something like `[0.12, -0.04, 0.88, ...]`, often with hundreds or a thousand dimensions.

As a maths graduate you already have the intuition: a vector is just a point in space. The whole trick of embeddings is that **texts with similar meaning land near each other** in that space, and unrelated texts land far apart.

## Meaning becomes geometry

Once text is a vector, *similarity becomes distance*. "How is the weather?" and "What's it like outside?" use almost no shared words, but their embeddings point in nearly the same direction.

This is powerful because it turns a fuzzy language question ("do these mean the same thing?") into a concrete maths question ("how close are these two vectors?").

## Cosine similarity

The most common way to compare two embeddings is **cosine similarity** — the cosine of the angle between them. It ignores how long the vectors are and only cares about *direction*.

- `1.0` -> same direction (very similar meaning)
- `0.0` -> perpendicular (unrelated)
- `-1.0` -> opposite direction

```python
import numpy as np

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(cosine_similarity([1, 0, 1], [1, 0, 1]))   # 1.0
print(cosine_similarity([1, 0, 0], [0, 1, 0]))   # 0.0
```

## Generating real embeddings

You rarely build embeddings by hand — you call an embeddings API. Install a provider's client, set your API key as an environment variable, and ask for a vector per text.

```bash
pip install voyageai
export VOYAGE_API_KEY="your-key-here"
```

```python
import voyageai

vo = voyageai.Client()   # reads VOYAGE_API_KEY from the environment

docs = ["How do I reset my password?", "What is your refund policy?"]
result = vo.embed(docs, model="voyage-3", input_type="document")
vectors = result.embeddings   # one vector per document
print(len(vectors), len(vectors[0]))   # 2 vectors, each ~1024 numbers
```

## A tiny semantic search

Put it together: embed your documents once, embed the user's question, then rank documents by cosine similarity. The top match is your most relevant document — even if it shares no words with the question.

```python
query = "I forgot my login details"
q_vec = vo.embed([query], model="voyage-3", input_type="query").embeddings[0]

scores = [cosine_similarity(q_vec, d) for d in vectors]
best = docs[scores.index(max(scores))]
print(best)   # 'How do I reset my password?'
```

## Why this matters

Embeddings are the foundation of **RAG** (Retrieval-Augmented Generation): embed your knowledge base, retrieve the chunks most similar to a question, then hand those chunks to Claude as context. Master embeddings now and the next lessons on vector databases and RAG will click into place.

## Your task

Embed five short sentences of your own, compute the cosine similarity of every pair, and confirm that the pairs *you* think are similar score highest.
