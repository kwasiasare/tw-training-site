---
course: data-scientist
title: Embeddings and Retrieval-Augmented Generation (RAG)
month: 5
monthTitle: Generative AI and LLM Foundations for Data Scientists
lesson: 3
summary: Learn how text embeddings turn documents into dense vectors where semantic similarity becomes
  geometric closeness, and how to use them to build retrieval-augmented generation (RAG) systems. This
  lesson walks from generating embeddings with Voyage AI, through semantic search with cosine similarity,
  to grounding an LLM's answers in retrieved context so it responds from your data rather than its training
  memory.
objectives:
- Explain what text embeddings are and why semantic similarity maps to geometric closeness
- Generate document and query embeddings using the Voyage AI client
- Implement semantic search with cosine similarity using only numpy
- Build a minimal RAG pipeline that retrieves top-k chunks and grounds an LLM answer in them
- Choose when to scale from in-memory search to a vector database like Chroma or pgvector
- Evaluate when RAG helps, when retrieval quality limits it, and how the pattern stays provider-agnostic
video: dsc-m5-l03-embeddings-and-retrieval-augmented-generation.mp4
quiz:
- q: What does a text embedding actually represent?
  options:
  - A compressed copy of the original text that can be decoded back to words
  - A hash that is identical only for identical strings
  - A dense vector of numbers positioning the text in a space where similar meanings sit close together
  - The model's final answer to a question about the text
  answer: 2
  why: An embedding is a dense numeric vector. Semantically similar texts land near each other geometrically,
    which is exactly what makes vector-based semantic search work. It is not a reversible compression
    or a hash.
- q: Which provider does this lesson use for embeddings, and why not Anthropic?
  options:
  - Voyage AI, because Anthropic offers no embeddings API and recommends Voyage
  - Anthropic, via its dedicated embeddings endpoint
  - Anthropic, by asking Claude to output a vector
  - Any LLM, since every chat model also returns embeddings
  answer: 0
  why: Anthropic does not provide an embeddings API; it officially recommends Voyage AI. You call vo.embed(...)
    with VOYAGE_API_KEY. Chat models like Claude generate text, not embedding vectors.
- q: In semantic search, why is cosine similarity a natural choice for comparing two embedding vectors?
  options:
  - It counts how many words two texts share
  - It only works after the vectors are sorted
  - It requires the vectors to be integers
  - It measures the angle between vectors, so it captures directional (semantic) similarity regardless
    of magnitude
  answer: 3
  why: 'Cosine similarity is the normalized dot product: it measures the angle between vectors, capturing
    how aligned their directions are independent of length. That aligns with how embedding models encode
    meaning as direction.'
- q: In a RAG pipeline, what is the role of the retrieved top-k chunks?
  options:
  - They are used to fine-tune the model's weights at request time
  - They are inserted into the prompt as context so the model answers grounded in them
  - They replace the user's question entirely
  - They are discarded after retrieval and only the scores are sent to the model
  answer: 1
  why: RAG retrieves the most relevant chunks and places them in the prompt as context. The model is then
    instructed to answer using that context, which grounds the response in your data and reduces hallucination.
    No weights are updated.
- q: When should you move from in-memory numpy cosine search to a vector database such as Chroma or pgvector?
  options:
  - As soon as you have more than one document
  - Only when you switch embedding providers
  - When the corpus grows large enough that scanning every vector per query becomes too slow or memory-heavy
  - Never, because numpy always outperforms a vector database
  answer: 2
  why: A brute-force numpy scan is fine for small corpora but recomputes similarity against every vector
    each query. Vector databases add indexing, persistence, and approximate nearest-neighbor search that
    scale to large corpora.
- q: 'Open-ended: Describe the limits of RAG. Why is retrieval quality often called the ceiling of a RAG
    system, and name two things you could change to raise that ceiling.'
  why: RAG end-to-end quality is capped by what retrieval finds — the generator cannot use information
    it never receives.
  answer: 'Retrieval quality is the ceiling because the LLM can only ground its answer in the chunks retrieval
    actually surfaces — if the relevant chunk is never retrieved, no amount of model capability recovers
    it. Two things you could change to raise that ceiling: improve the chunking strategy and use a stronger
    or domain-tuned embedding model (other options: query rewriting, re-ranking or increasing top-k, and
    improving corpus coverage/freshness).'
resources:
- label: Voyage AI — Text Embeddings Documentation
  url: https://docs.voyageai.com/docs/embeddings
- label: Chroma — Getting Started (open-source vector database)
  url: https://docs.trychroma.com/docs/overview/getting-started
- label: pgvector — Open-source vector similarity search for Postgres
  url: https://github.com/pgvector/pgvector
- label: Anthropic — Contextual Retrieval (RAG) guide
  url: https://docs.claude.com/en/docs/build-with-claude/contextual-retrieval
---

## What Embeddings Are

An **embedding** turns a piece of text into a **dense vector** of floating-point numbers, often hundreds or thousands of dimensions. The key property: the model is trained so that texts with similar *meaning* land close together in this space, while unrelated texts land far apart. Semantic similarity becomes **geometric closeness**.

That is what makes embeddings useful. Instead of matching keywords, you ask "which document is most like this query?" and answer with arithmetic. "How do I reset my password?" and "I forgot my login credentials" share almost no words, yet their embeddings sit near each other because they mean nearly the same thing.

## Generating Embeddings

A crucial accuracy point: **Anthropic does not offer an embeddings API.** For embeddings, Anthropic officially recommends **Voyage AI**. Newer Voyage models may exist, so check the docs.

```python
import voyageai

vo = voyageai.Client()  # reads VOYAGE_API_KEY

result = vo.embed(documents, model="voyage-3.5",
                  input_type="document")
vectors = result.embeddings  # list[list[float]]
```

Use `input_type="document"` for your corpus and `input_type="query"` for a user's search query. The pattern is **provider-agnostic** — open-source models such as **BGE** or **E5** produce comparable vectors, and the retrieval logic does not change.

## Semantic Search with Cosine Similarity

Once text is vectors, finding the closest matches is just math. **Cosine similarity** measures the angle between two vectors — the normalized dot product — so it captures directional (semantic) alignment regardless of magnitude. Pure numpy is enough:

```python
import numpy as np

def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))

def top_k(query_vec, doc_vecs, k=3):
    scores = [cosine(query_vec, d) for d in doc_vecs]
    ranked = sorted(enumerate(scores),
                    key=lambda x: x[1], reverse=True)
    return ranked[:k]  # [(index, score), ...]
```

Embed the query with `input_type="query"`, score it against the stored vectors, and take the highest few. This dependency-light approach is perfect for learning and small corpora.

## From Search to RAG

**Retrieval-Augmented Generation** joins that search step to a language model: **retrieve** the top-k relevant chunks, **augment** the prompt by inserting them as context, and **generate** an answer grounded in them.

```python
from anthropic import Anthropic

client = Anthropic()
q = vo.embed([question], model="voyage-3.5",
             input_type="query").embeddings[0]
context = "\n".join(docs[i] for i, _ in top_k(q, vectors))

msg = client.messages.create(
    model="claude-opus-4-8", max_tokens=1024,
    system=("Answer ONLY using the provided context. "
            "If it's not there, say you don't know."),
    messages=[{"role": "user",
               "content": f"Context:\n{context}\n\nQuestion: {question}"}])
answer = msg.content[0].text
```

We use the stable Anthropic Messages API for generation. The system instruction is doing real work: it tells the model to stay inside the retrieved context and admit ignorance rather than invent an answer. Default to Claude, but learn model selection for your latency and cost needs. Never `eval()` model output.

## Scaling Up with Vector Databases

The numpy scan recomputes cosine similarity against *every* vector each query — fine for hundreds of chunks, but it breaks down as the corpus grows. A **vector database** adds persistence, indexing, and approximate nearest-neighbor search so queries stay fast at scale.

```python
import chromadb

collection = chromadb.Client().create_collection("docs")
collection.add(ids=ids, embeddings=vectors,
               documents=documents)
hits = collection.query(query_embeddings=[q], n_results=3)
```

**Chroma** is a lightweight place to start; **pgvector** keeps vectors right inside Postgres alongside your relational data. The retrieval interface changes, but the RAG pattern is identical.

## When RAG Helps — and Its Limits

RAG shines when you need answers **grounded in your own data**: private knowledge bases, fresh information past the model's training cutoff, or domains where hallucination is costly. By forcing the model to answer from retrieved context, you make responses traceable and far more trustworthy.

But RAG has a ceiling: **retrieval quality.** If the relevant chunk is never retrieved, no model can recover it. Raising that ceiling means better chunking, a stronger embedding model, query rewriting, re-ranking, and good corpus coverage. Build the retrieval well, and the generation takes care of itself.
