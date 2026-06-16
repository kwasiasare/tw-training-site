---
course: dami-ai-career
title: Retrieval-Augmented Generation (RAG)
month: 3
monthTitle: LLM Application Skills
lesson: 10
summary: Ground an LLM in your own documents by retrieving relevant chunks and feeding them into the prompt
  as context.
objectives:
- Explain why RAG reduces hallucinations and keeps answers up to date
- 'Describe the RAG pipeline: chunk, embed, store, retrieve, generate'
- Turn text into embedding vectors and store them in a vector database
- Retrieve the most relevant chunks using cosine similarity
- Build a prompt that grounds Claude in the retrieved context
- Cite sources and recognise common RAG failure modes
video: m3-l10-rag.mp4
quiz:
- q: What problem does RAG primarily solve?
  options:
  - It makes the model train faster
  - It grounds answers in external, up-to-date documents the model never memorised
  - It removes the need for a prompt
  - It compresses the model
  answer: 1
  why: RAG retrieves relevant text from your own data and adds it to the prompt, so the model answers
    from facts instead of guessing from memory.
- q: In the RAG pipeline, what is an embedding?
  options:
  - A copy of the user's question
  - A numeric vector that captures the meaning of a piece of text
  - A database index name
  - The model's final answer
  answer: 1
  why: An embedding is a list of numbers (a vector) where texts with similar meaning sit close together,
    enabling semantic search.
- q: Which metric is commonly used to measure how similar two embedding vectors are?
  options:
  - Mean squared error
  - Cosine similarity
  - Accuracy
  - Perplexity
  answer: 1
  why: Cosine similarity measures the angle between two vectors; values near 1 mean the texts are semantically
    close.
- q: Why do we split documents into smaller chunks before embedding?
  answer: So each vector captures a focused idea and retrieval returns precise, relevant passages that
    fit in the prompt, rather than whole documents.
  why: Chunking keeps embeddings meaningful and lets you pass only the relevant pieces into the limited
    context window.
- q: What should you do in the prompt to reduce the chance the model invents facts not in the retrieved
    context?
  answer: Instruct it to answer only from the provided context and to say 'I don't know' when the context
    lacks the answer.
  why: Grounding instructions plus retrieved context keep the model honest and let it admit gaps instead
    of hallucinating.
- q: 'True or false: RAG requires retraining or fine-tuning the language model.'
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. RAG adds knowledge at inference time through the prompt, so you can update your data without
    touching the model.
resources:
- label: Anthropic docs — Embeddings & retrieval with Claude
  url: https://docs.claude.com/en/docs/build-with-claude/embeddings
- label: Anthropic docs — Contextual Retrieval (improving RAG accuracy)
  url: https://www.anthropic.com/news/contextual-retrieval
- label: Pinecone — Retrieval-Augmented Generation learning guide
  url: https://www.pinecone.io/learn/retrieval-augmented-generation/
- label: The original RAG paper (Lewis et al., 2020)
  url: https://arxiv.org/abs/2005.11401
---

## Why RAG?

A language model only knows what it learned during training. Ask it about your company handbook, last week's news, or a private PDF and it will either refuse or, worse, **hallucinate** a confident wrong answer.

**Retrieval-Augmented Generation (RAG)** fixes this. Instead of retraining the model, we *retrieve* the most relevant pieces of your own text and paste them into the prompt as context. The model then answers from facts you supplied. As a maths graduate this is a familiar idea: an open-book exam beats a closed-book one.

## The RAG pipeline

RAG has two phases. **Indexing** (done once, offline):

1. **Chunk** — split documents into small passages.
2. **Embed** — turn each chunk into a vector (a list of numbers capturing meaning).
3. **Store** — save the vectors in a vector database.

**Querying** (every question):

4. **Embed the question** with the same model.
5. **Retrieve** the chunks whose vectors are closest to the question.
6. **Generate** — give those chunks plus the question to the LLM.

## Embeddings and similarity

An **embedding** maps text to a point in high-dimensional space so that similar meanings sit near each other. We measure closeness with **cosine similarity** — the cosine of the angle between two vectors. A value near 1 means very similar; near 0 means unrelated.

```python
import numpy as np

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Retrieve top-k chunks for a query embedding
def top_k(query_vec, chunk_vecs, k=3):
    scores = [cosine_similarity(query_vec, c) for c in chunk_vecs]
    return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
```

## Grounding the generation with Claude

Once you have the top chunks, build a prompt that tells the model to answer **only** from that context. Keep your API key in an environment variable, never in code.

```python
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

def answer(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = (
        f"Use ONLY the context to answer. If the answer is not there, "
        f"say 'I don't know'.\n\nContext:\n{context}\n\nQuestion: {question}"
    )
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
```

## Failure modes and good habits

RAG is powerful but not magic. Watch for: **bad chunking** (passages too big or split mid-idea), **retrieval misses** (the right chunk never surfaces), and **ignored context** (the model answers from memory anyway). Improve results by tuning chunk size, retrieving a few extra chunks, asking the model to **cite** which chunk it used, and instructing it to admit when it doesn't know.

## Your task

Take three short text files, chunk and embed them, store the vectors, and build a tiny question-answering loop that retrieves the top chunks and grounds Claude in them.
