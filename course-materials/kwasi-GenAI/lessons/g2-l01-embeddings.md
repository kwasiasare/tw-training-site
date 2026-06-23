---
course: kwasi-GenAI
title: Embeddings & cosine similarity
month: 2
monthTitle: Retrieval-Augmented Generation (RAG)
lesson: 1
summary: Understand what a vector embedding actually represents, how cosine similarity measures meaning,
  and how to choose an embedding model for your RAG system.
objectives:
- Explain what a vector embedding represents and why similar meaning lands near in space
- Describe how cosine similarity scores two embeddings between -1 and 1
- Generate an embedding from text using an embeddings API
- Compare candidate embedding models on dimension, cost, context, and domain fit
- Explain why query and document must use the same embedding model
- Connect embeddings to the retrieval step you will build later in the module
video: g2-l01-embeddings.mp4
quiz:
- q: What does a single text embedding actually represent?
  options:
  - The exact characters of the text, compressed
  - A list of numbers positioning the text's meaning in a vector space
  - A summary sentence of the text
  - A hash used to detect duplicates
  answer: 1
  why: An embedding is a fixed-length vector of floats that places text in a high-dimensional space so
    that similar meanings sit close together.
- q: Cosine similarity between two embeddings measures…
  options:
  - The number of shared words
  - The angle between the two vectors, ignoring their length
  - The file size difference
  - How many tokens each text has
  answer: 1
  why: Cosine similarity compares the direction (angle) of two vectors, so it captures semantic closeness
    regardless of vector magnitude.
- q: Why must you embed the query and the documents with the SAME model?
  options:
  - To save money on API calls
  - So both land in the same vector space and distances are meaningful
  - Because models refuse mixed input
  - It is only a style preference
  answer: 1
  why: Different models produce vectors in different, incompatible spaces; comparing across them gives
    meaningless distances.
- q: A cosine similarity of 1.0 between two text vectors means…
  options:
  - The texts are unrelated
  - The vectors point in exactly the same direction (maximally similar)
  - An error occurred
  - The texts are opposites
  answer: 1
  why: Cosine ranges from -1 to 1; 1.0 means identical direction and therefore maximal semantic similarity
    in that model's space.
- q: In one sentence, why do we use embeddings instead of keyword matching for retrieval?
  answer: Embeddings capture meaning, so a query can match relevant passages even when they share no exact
    keywords.
  why: Keyword search misses paraphrases and synonyms; embeddings let 'cancel my plan' match a passage
    about 'ending a subscription'.
- q: Name two practical factors to weigh when choosing an embedding model.
  answer: 'Vector dimension and cost (others: max input length, domain/language fit, on-prem vs API).'
  why: Higher dimensions and longer context cost more storage and money; domain fit affects retrieval
    quality, so you trade these against each other.
resources:
- label: Voyage AI — Embeddings (Anthropic's recommended partner)
  url: https://docs.voyageai.com/docs/embeddings
- label: OpenAI docs — Embeddings guide
  url: https://platform.openai.com/docs/guides/embeddings
- label: Amazon Bedrock — Titan Text Embeddings
  url: https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html
- label: Hugging Face — Massive Text Embedding Benchmark (MTEB) leaderboard
  url: https://huggingface.co/spaces/mteb/leaderboard
- label: Pinecone — What are vector embeddings?
  url: https://www.pinecone.io/learn/vector-embeddings/
---

## The problem embeddings solve

You already know keyword search. It is exact: the words must match. But a user who types "how do I cancel my plan" should still find a passage titled "ending a subscription" — same meaning, zero shared keywords. **Embeddings** are how we let a computer match on *meaning* instead of *spelling*.

An embedding is a list of numbers — a **vector** — that an embedding model produces for a piece of text. You can picture each vector as a point in a huge multi-dimensional space. The model is trained so that texts with similar meaning land near each other, and unrelated texts land far apart. "Cancel my plan" and "end my subscription" end up as neighbours; "how to bake bread" sits across the room.

## What the numbers mean

A typical embedding has a fixed **dimension** — say 1024 or 1536 floats. You never read those numbers by hand; no single dimension means "formality" or "topic". What matters is the *geometry*: relative positions encode relationships the model learned from huge amounts of text.

The key property is this: **same model, same space.** If you embed your documents with one model and your query with another, their vectors live in different, incompatible spaces and the distances are nonsense. Pick one embedding model and use it for everything in a given index.

## Cosine similarity: measuring closeness

To ask "how similar are these two texts?" you compare their vectors. The standard measure is **cosine similarity** — the cosine of the angle between the two vectors. It ranges from `-1` (opposite) through `0` (unrelated) to `1` (same direction, maximally similar). It ignores vector length and looks only at direction, which is exactly what we want for meaning.

```python
import numpy as np

def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

# higher score = more semantically similar
print(cosine(vec_query, vec_passage))
```

In practice your vector database computes this for you across millions of vectors. You just need to know: bigger cosine score means "closer in meaning".

## Getting an embedding from an API

You call an embeddings endpoint with text and get a vector back. Anthropic does not offer its own embeddings API — it recommends a dedicated provider, **Voyage AI**, for this step. The pattern is identical across providers, whether you use Voyage AI, an OpenAI-compatible endpoint, **Amazon Bedrock Titan** / **Azure OpenAI** in the cloud you already run, or an open model you host yourself (such as **BGE** or **E5**).

```python
# Pseudocode — provider-agnostic
vec = embeddings.create(model="<embedding-model>", input="end my subscription")
# vec is e.g. 1024 floats; store it next to the original text
```

Note the embedding model is **separate** from your chat model (`claude-opus-4-8`). Embedding models are smaller, cheaper, and tuned for retrieval, not conversation.

## Choosing an embedding model

There is no single best model — you trade off four things:

- **Dimension** — more dimensions can capture more nuance but cost more storage and slower search.
- **Cost & throughput** — you may embed millions of chunks; price per token matters.
- **Max input length** — must comfortably fit your chunk size (next lesson).
- **Domain & language fit** — a model strong on legal English may be weak on code or German.

A sensible default: start with a reputable general model, measure retrieval quality on *your* questions, and only change if results are weak. Benchmarks like **MTEB** are a starting signal, not gospel — your corpus is the real test.

## Your task

Pick an embeddings API you can access (Bedrock Titan, Azure OpenAI, or another). Embed three short sentences: two that mean the same thing and one unrelated. Compute cosine similarity for all three pairs and confirm the two related sentences score highest.
