---
course: kwasi-GenAI
title: Vector databases
month: 2
monthTitle: Retrieval-Augmented Generation (RAG)
lesson: 3
summary: 'Store and search embeddings at scale: start with pgvector or Chroma, understand index, upsert,
  and query, then know when a managed option like Pinecone earns its cost.'
objectives:
- Explain what a vector database does that a normal database cannot do well
- 'Describe the three core operations: build an index, upsert vectors, and query'
- Stand up a local vector store with pgvector or Chroma
- Explain why approximate nearest-neighbour search trades a little recall for huge speed
- Store metadata alongside vectors and filter on it at query time
- Decide when a managed vector database like Pinecone is worth the cost
video: g2-l03-vector-databases.mp4
quiz:
- q: What is the core job of a vector database?
  options:
  - Store images only
  - Store embeddings and find the nearest vectors to a query vector fast
  - Replace your relational database entirely
  - Compress text losslessly
  answer: 1
  why: A vector database indexes embeddings so it can return the most similar vectors to a query vector
    quickly, even across millions of items.
- q: What does 'upsert' mean in a vector database?
  options:
  - Delete all vectors
  - Insert new vectors or update existing ones by id
  - Sort the vectors alphabetically
  - Export to CSV
  answer: 1
  why: Upsert inserts a vector (with its id and metadata) or updates it if that id already exists, which
    keeps your index in sync as documents change.
- q: Why do production vector databases use approximate nearest-neighbour (ANN) search?
  options:
  - It is more accurate than exact search
  - Exact search over millions of vectors is too slow; ANN trades tiny recall loss for big speed
  - It uses less disk
  - It avoids needing embeddings
  answer: 1
  why: Comparing a query against every vector exactly is O(n) and too slow at scale; ANN indexes return
    almost-best matches in milliseconds.
- q: Why store metadata (like source, date, tenant) alongside each vector?
  options:
  - It is required by JSON
  - So you can filter results, cite sources, and enforce access control at query time
  - To make vectors larger
  - It speeds up embedding
  answer: 1
  why: Metadata lets you filter (e.g. only this customer's docs), return citations, and apply security
    boundaries during retrieval.
- q: In one sentence, when is a managed vector DB like Pinecone worth choosing over pgvector?
  answer: When scale, uptime, or operational load outgrow what you want to run yourself, and you'd rather
    pay for a hosted, autoscaling service.
  why: pgvector and Chroma are great to start; managed services pay off at large scale or when you don't
    want to operate the index.
- q: Why is pgvector often a great first choice for a team already running Postgres?
  answer: It adds vector search to the database they already operate, so vectors live next to relational
    data with no new system to run.
  why: Reusing existing Postgres skills and infrastructure removes operational overhead and keeps metadata
    and vectors in one place.
resources:
- label: pgvector — open-source vector similarity search for Postgres
  url: https://github.com/pgvector/pgvector
- label: Chroma — open-source embedding database docs
  url: https://docs.trychroma.com/
- label: Pinecone — Vector database documentation
  url: https://docs.pinecone.io/guides/get-started/overview
- label: Azure AI Search — vector search overview
  url: https://learn.microsoft.com/en-us/azure/search/vector-search-overview
- label: Pinecone — What is a vector database?
  url: https://www.pinecone.io/learn/vector-database/
---

## Why a normal database isn't enough

You now have thousands of chunks, each with an embedding. At query time you embed the user's question and need the *most similar* chunks. A relational `WHERE` clause can't do that — there's no index for "closest in 1024-dimensional space". A **vector database** is built exactly for this: it stores embeddings and answers "give me the k vectors nearest to this one" in milliseconds, even across millions of items.

If you come from a DevOps background, the mental model is familiar: it's a specialised index, much like a search engine's inverted index, but for geometry instead of keywords.

## The three operations you actually use

Every vector store, from a local library to a managed cloud service, exposes the same three operations:

1. **Index** — define a collection/table that holds vectors of a fixed dimension, choosing a distance metric (usually cosine).
2. **Upsert** — insert a vector with an `id` and a bag of `metadata`, or update it if that id already exists. Re-embed a changed document and upsert it; the index stays current.
3. **Query** — embed the question, send that vector, and get back the top-k most similar vectors with their metadata and scores.

```python
# Pattern is the same everywhere
collection.upsert(id="doc1#chunk3", vector=vec, metadata={"source": "handbook.pdf", "page": 12})
hits = collection.query(vector=query_vec, top_k=5, where={"source": "handbook.pdf"})
```

## Start local: pgvector or Chroma

Don't reach for a managed service on day one. Two excellent starting points:

- **pgvector** adds a `vector` column type and similarity operators to **PostgreSQL**. If your team already runs Postgres — and most cloud teams do — this is ideal: vectors live next to your relational data and metadata, with no new system to operate.
- **Chroma** is a lightweight, open-source embedding database that runs in-process or as a small server. It's perfect for prototypes and local development.

```sql
-- pgvector
CREATE EXTENSION vector;
CREATE TABLE chunks (id text PRIMARY KEY, body text, embedding vector(1024));
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
SELECT id, body FROM chunks ORDER BY embedding <=> :query_vec LIMIT 5;
```

That `<=>` is the cosine-distance operator, and the **HNSW** index is what makes the search fast.

## Approximate nearest neighbour: fast on purpose

Comparing a query against every stored vector (exact search) is `O(n)` — fine for a thousand chunks, hopeless for ten million. So vector databases build an **ANN** index (commonly **HNSW**, a navigable graph). ANN returns *almost* the best matches, trading a sliver of recall for enormous speed. You can tune that trade-off; for RAG, near-perfect recall in single-digit milliseconds is exactly the deal you want.

## Metadata is not optional

Always store metadata with each vector: source file, page, document id, date, tenant/customer, access level. It pays off three ways. You **filter** ("only this customer's documents"). You **cite** (return the source so the user can verify — lesson 7). And you enforce **security boundaries** at query time, which as a security-minded engineer you will care about: never let one tenant retrieve another's chunks.

## When to go managed (Pinecone & friends)

Managed services like **Pinecone**, or **Azure AI Search** vector search in the cloud you already run, handle sharding, replication, autoscaling, and uptime for you. They earn their cost when your corpus or traffic outgrows a single Postgres box, when you need high availability without operating it yourself, or when you want hybrid (keyword + vector) search out of the box. The migration path is gentle: the same upsert/query shape works everywhere, so start local and move when the numbers justify it.

## Your task

Stand up a local vector store with Chroma or pgvector. Upsert the chunks you produced last lesson, each with `source` metadata. Run one query, print the top-5 chunks with their similarity scores, then re-run it filtered to a single source file.
