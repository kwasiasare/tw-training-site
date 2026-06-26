---
course: ml-engineer
title: Retrieval-Augmented Generation and Vector Databases
month: 5
monthTitle: 'LLM Engineering: Transformers, RAG, and Fine-Tuning'
lesson: 3
summary: 'Retrieval-augmented generation (RAG) grounds a language model in your own data by retrieving
  relevant passages and injecting them into the prompt, fixing hallucination and stale-knowledge problems.
  In this lesson you build the full pipeline as an ML engineer: embed text with open-source sentence-transformers,
  store and search vectors with a vector database, retrieve the top-k passages, and generate a grounded
  answer.'
objectives:
- Explain why LLMs hallucinate and how injecting retrieved context grounds their answers
- Describe how embeddings turn semantic similarity into a vector distance computation
- Generate sentence embeddings locally with the sentence-transformers library
- Use a vector database for approximate nearest-neighbor search and persistence instead of a brute-force
  scan
- 'Assemble an end-to-end RAG pipeline: chunk, embed, store, retrieve top-k, prompt, generate'
- Evaluate and improve retrieval quality through chunking, top-k tuning, and re-ranking
video: mle-m5-l03-retrieval-augmented-generation-and-vector-databases.mp4
quiz:
- q: Why are large language models prone to producing confident but incorrect answers about niche or recent
    facts?
  options:
  - They cannot process text longer than a single sentence
  - Their weights are updated live with every user query
  - They always refuse to answer factual questions
  - Their knowledge is frozen at training time and they have no access to your private or up-to-date data
  answer: 3
  why: An LLM only knows what was in its training data up to its cutoff. It cannot see your private documents
    or anything newer, so when asked outside that knowledge it may produce a fluent but fabricated answer.
    RAG fixes this by retrieving relevant context and placing it in the prompt.
- q: What property of embedding vectors makes them useful for retrieval?
  options:
  - They compress any text into exactly eight bytes
  - Semantically similar texts map to nearby vectors, so similarity becomes a distance computation
  - They are unique cryptographic hashes of the input
  - They can only be compared with exact string matching
  answer: 1
  why: Embeddings place text in a high-dimensional space where meaning corresponds to geometry. Passages
    about the same topic land close together, so finding relevant text reduces to a nearest-neighbor (distance
    or cosine) search rather than keyword matching.
- q: In the sentence-transformers snippet, why pass normalize_embeddings=True when encoding?
  options:
  - It translates the input text to English first
  - It removes stop words before encoding
  - It scales each vector to unit length, so cosine similarity reduces to a simple dot product
  - It is mandatory or the model will fail to load
  answer: 2
  why: Normalizing to unit length means the dot product of two vectors equals their cosine similarity.
    This makes similarity scoring cheaper and is what many vector indexes expect, so it keeps retrieval
    consistent and fast.
- q: What does a vector database primarily add over a brute-force NumPy cosine scan?
  options:
  - Approximate nearest-neighbor indexing plus persistence, so search stays fast as the corpus grows
  - A guarantee that the LLM will never hallucinate
  - Automatic training of the embedding model for you
  - Removal of the need to chunk documents
  answer: 0
  why: A brute-force scan compares the query against every stored vector, which is O(N) and slow at scale.
    Vector databases build an approximate nearest-neighbor (ANN) index for sub-linear search and persist
    the vectors and metadata so you do not re-embed on every restart.
- q: In a RAG system, why is retrieval quality often described as the ceiling on overall answer quality?
  options:
  - Because the generator ignores any retrieved context
  - If the correct passage is never retrieved, the generator has no grounded evidence to base its answer
    on
  - Because a larger embedding model always removes the need for retrieval
  - Because top-k must always be set to exactly one
  answer: 1
  why: Generation can only use what retrieval surfaces. If the relevant chunk is missing from the top-k,
    even the best LLM must fall back on its parametric memory and may hallucinate. Improving chunking,
    top-k, and re-ranking raises that ceiling.
- q: In one or two words, name the first pipeline stage that splits long documents into smaller passages
    before they are embedded.
  answer: chunking
  why: Chunking breaks documents into passage-sized units so each embedding captures a focused piece of
    meaning and retrieved context fits within the prompt. Chunk size and overlap are key levers for retrieval
    quality.
resources:
- label: Sentence Transformers (SBERT) Documentation
  url: https://www.sbert.net/
- label: 'Chroma Vector Database: Getting Started'
  url: https://docs.trychroma.com/docs/overview/getting-started
- label: 'pgvector: Open-Source Vector Similarity Search for Postgres'
  url: https://github.com/pgvector/pgvector
- label: 'Faiss: A Library for Efficient Similarity Search (Meta AI)'
  url: https://github.com/facebookresearch/faiss
---

## Overview

Large language models are fluent but forgetful: their knowledge is frozen at training time, and they have never seen your internal wiki, your codebase, or yesterday's incident report. **Retrieval-augmented generation (RAG)** closes this gap. Instead of fine-tuning the model, you retrieve the most relevant passages from your own data at query time and place them directly in the prompt, so the model answers from evidence rather than guessing.

## 1. The Grounding Problem

Ask a vanilla LLM a question about a private document and it will often produce a confident, plausible, and wrong answer. This is **hallucination**, and it stems from two limits: the model's knowledge is stale (bounded by its training cutoff) and incomplete (it never saw your data). RAG addresses both by injecting fresh, relevant context:

```python
prompt = f"""Answer using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{retrieved_text}

Question: {question}"""
```

The model still does the reasoning and phrasing, but the facts come from text you retrieved and trust.

## 2. Embeddings: Meaning as Vectors

To retrieve by *meaning* rather than exact keywords, we convert text into **embeddings**: dense vectors where semantically similar texts land close together. Two paraphrases of the same idea map to nearby points even with no shared words, so retrieval becomes a nearest-neighbor search. Closeness is usually measured with **cosine similarity**:

```python
import numpy as np

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

If the vectors are already unit-length (normalized), cosine similarity is just the dot product.

## 3. Building Embeddings with sentence-transformers

As an ML engineer you often want embeddings you can run and version yourself. The open-source **sentence-transformers** library does exactly this, running locally with no external API:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")  # open-source, runs locally
vecs = model.encode(
    ["How do I reset my password?", "Steps to recover account access"],
    normalize_embeddings=True,
)
print(vecs.shape)  # (2, 384)
```

The two sentences above share almost no words yet produce highly similar vectors. The pattern is provider-agnostic: managed services such as Voyage AI expose the same `encode`-then-store interface behind an API if you prefer not to self-host. Pick a model for your domain and stay consistent: queries and documents must be embedded with the *same* model.

## 4. Vector Databases: Indexing and Persistence

A brute-force cosine scan over every stored vector works for a few thousand passages but is O(N) per query and forgets everything on restart. A **vector database** adds two things: an **approximate nearest-neighbor (ANN)** index for sub-linear search as the corpus grows, and **persistence** of vectors plus metadata. Chroma gives a minimal local example:

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("docs")

collection.add(
    ids=["d1", "d2"],
    documents=["Reset your password from Settings.", "Our refund window is 30 days."],
    embeddings=model.encode(
        ["Reset your password from Settings.", "Our refund window is 30 days."],
        normalize_embeddings=True,
    ).tolist(),
)

hits = collection.query(
    query_embeddings=model.encode(["forgot my login"], normalize_embeddings=True).tolist(),
    n_results=2,
)
```

FAISS (a raw ANN index) and pgvector (vectors inside Postgres) are popular alternatives with the same shape: add vectors, query for the nearest.

## 5. The End-to-End RAG Pipeline

The full flow is six stages: **chunk** documents into passages, **embed** each chunk, **store** the vectors, **retrieve** the top-k nearest to the query, **inject** them into the prompt, and **generate**:

```python
import anthropic

hits = collection.query(
    query_embeddings=model.encode([question], normalize_embeddings=True).tolist(),
    n_results=4,
)
context = "\n\n".join(hits["documents"][0])

client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user",
               "content": f"Context:\n{context}\n\nQuestion: {question}"}],
)
print(resp.content[0].text)
```

The generator can be any LLM: an open model served from HuggingFace, or an API. Retrieval is the part you own.

## 6. Evaluating and Improving RAG

Retrieval quality is the **ceiling** on answer quality: if the right passage never reaches the prompt, no generator can ground on it. Evaluate retrieval directly with metrics like recall@k (is the gold passage in the top-k?) before blaming the model. The main levers are **chunking** (size and overlap, so a passage holds one coherent idea), **top-k** (too low misses evidence, too high adds noise and cost), and **re-ranking** (retrieve a wide candidate set, then re-score with a stronger cross-encoder and keep the best few).

## Key Takeaways

RAG grounds an LLM in your data without retraining it. Embed with a consistent model, store in a vector database for fast persistent search, retrieve the top-k, and let the model generate from that evidence. When answers are weak, fix retrieval first.
