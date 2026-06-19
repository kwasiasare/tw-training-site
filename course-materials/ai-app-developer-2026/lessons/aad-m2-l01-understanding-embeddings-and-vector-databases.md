---
course: ai-app-developer-2026
title: Understanding Embeddings and Vector Databases
month: 2
monthTitle: Building RAG Applications with Vector Databases
lesson: 1
summary: Learn how text embeddings turn language into vectors that capture meaning, and how vector databases
  like Chroma and Pinecone store and search those vectors for fast semantic retrieval. This lesson builds
  the foundation for RAG (Retrieval-Augmented Generation) applications.
objectives:
- Explain what text embeddings are and why they enable semantic search
- Generate embeddings using an embedding model (e.g., OpenAI or sentence-transformers)
- Describe how vector databases index and search vectors using similarity metrics
- Store and query embeddings in Chroma and understand the Pinecone equivalent
- Choose appropriate distance metrics and chunking strategies for retrieval quality
video: aad-m2-l01-understanding-embeddings-and-vector-databases.mp4
quiz:
- q: What is a text embedding?
  options:
  - A compressed zip file of text
  - A numeric vector representing the meaning of text
  - A keyword index of a document
  - An encrypted version of the text
  answer: 1
  why: An embedding is a vector of floats that captures semantic meaning, allowing similar texts to be
    close in vector space.
- q: Which similarity metric is most commonly used for text embeddings?
  options:
  - Cosine similarity
  - Hamming distance
  - Jaccard index
  - Levenshtein distance
  answer: 0
  why: Cosine similarity measures the angle between vectors and is the standard choice for most text embedding
    models.
- q: Why must you use the same embedding model for indexing and querying?
  options:
  - To save API costs
  - Because vectors from different models live in different spaces and aren't comparable
  - Because databases only support one model
  - To keep dimensions under 512
  answer: 1
  why: Different models produce vectors in incompatible spaces, so mixing them yields meaningless similarity
    scores.
- q: What does a vector database use to avoid comparing a query against every stored vector?
  options:
  - A SQL JOIN
  - An approximate nearest neighbor (ANN) index like HNSW
  - A full-text keyword index
  - A relational primary key
  answer: 1
  why: ANN indexes such as HNSW let the database find close matches quickly without an exhaustive scan.
- q: In one sentence, why do we chunk documents before embedding them?
  answer: Chunking splits long documents into smaller pieces so retrieval is precise and chunks fit within
    the model's context, while overlap preserves meaning across boundaries.
  why: Chunking balances retrieval precision with retaining enough context, and overlap avoids cutting
    ideas mid-sentence.
- q: What is the key difference between Chroma and Pinecone in how embeddings are handled?
  answer: Chroma can generate embeddings for you and runs locally, while Pinecone is a managed cloud service
    that requires you to supply the vectors yourself.
  why: Chroma is convenient for local prototyping with optional built-in embedding; Pinecone scales in
    the cloud but expects pre-computed vectors.
resources:
- label: Chroma documentation
  url: https://docs.trychroma.com/
- label: Pinecone documentation
  url: https://docs.pinecone.io/
- label: OpenAI Embeddings guide
  url: https://platform.openai.com/docs/guides/embeddings
- label: Sentence-Transformers documentation
  url: https://www.sbert.net/
---

## What Are Embeddings?

An **embedding** is a numeric vector (a list of floating-point numbers) that represents the *meaning* of a piece of text. An embedding model maps text into a high-dimensional space (commonly 384, 768, or 1536 dimensions) where semantically similar texts land close together.

For example, "How do I reset my password?" and "I forgot my login credentials" produce vectors that are near each other, even though they share few words. This is the core idea behind **semantic search**: we match by meaning rather than by exact keywords.

## How Similarity Is Measured

Vector databases compare vectors using a **distance/similarity metric**:

- **Cosine similarity** — measures the angle between vectors; most common for text embeddings. Ranges from -1 to 1 (higher = more similar).
- **Dot product** — useful when vectors are normalized.
- **Euclidean (L2) distance** — straight-line distance; lower = more similar.

Most text embedding models are tuned for cosine similarity. Pick the metric your model recommends.

## Generating Embeddings

You can generate embeddings with a hosted API or a local model.

```python
# Hosted: OpenAI
from openai import OpenAI
client = OpenAI()
resp = client.embeddings.create(
    model="text-embedding-3-small",
    input="How do I reset my password?"
)
vector = resp.data[0].embedding  # list of 1536 floats
```

```python
# Local: sentence-transformers
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dims
vector = model.encode("How do I reset my password?")
```

Key practical points: embeddings from different models are **not** comparable, so use the same model for indexing and querying. Costs and latency differ between hosted and local options.

## What Is a Vector Database?

A **vector database** stores embeddings alongside metadata and supports fast **approximate nearest neighbor (ANN)** search. Instead of comparing your query against every stored vector (slow at scale), it uses an index (e.g., HNSW) to find the closest matches in milliseconds.

Popular options:
- **Chroma** — open-source, easy to run locally, great for prototyping.
- **Pinecone** — fully managed cloud service, scales to billions of vectors.
- Others: Weaviate, Qdrant, Milvus, pgvector.

## Chunking Documents

Before embedding long documents, split them into **chunks** (e.g., 200–500 tokens with some overlap). Each chunk is embedded and stored separately. Good chunking balances:
- Chunks small enough to be precise and fit in context
- Chunks large enough to retain meaning
- Overlap to avoid cutting ideas mid-sentence

## Storing and Querying in Chroma

```python
import chromadb
client = chromadb.Client()
collection = client.create_collection("docs")

# Add documents (Chroma can embed for you, or pass your own vectors)
collection.add(
    documents=["Reset your password from Settings.", "Contact billing for refunds."],
    ids=["doc1", "doc2"],
    metadatas=[{"topic": "auth"}, {"topic": "billing"}]
)

# Semantic query
results = collection.query(
    query_texts=["I forgot my login"],
    n_results=2
)
print(results["documents"])
```

## The Pinecone Equivalent

```python
from pinecone import Pinecone
pc = Pinecone(api_key="...")
index = pc.Index("docs")

# Upsert vectors you generated yourself
index.upsert(vectors=[
    {"id": "doc1", "values": vector1, "metadata": {"text": "Reset your password..."}}
])

# Query with a query vector
index.query(vector=query_vector, top_k=2, include_metadata=True)
```

Note: Pinecone expects you to supply the vectors, so you run the embedding model yourself. Chroma can optionally handle embedding for you.

## How This Fits Into RAG

In a RAG pipeline: (1) embed and store your knowledge base, (2) embed the user's question, (3) retrieve the top-k most similar chunks, (4) inject them into the LLM prompt as context. The vector database is the **retrieval** engine that grounds the model in your data.
