---
course: ai-app-developer-2026
title: Chunking, Indexing, and Retrieval Strategies
month: 2
monthTitle: Building RAG Applications with Vector Databases
lesson: 2
summary: Learn how to split documents into effective chunks, index them in a vector database, and tune
  retrieval so your RAG app returns the most relevant context for each query. Covers chunking strategies,
  embeddings, indexing parameters, and retrieval techniques like top-k, hybrid search, metadata filtering,
  and re-ranking.
objectives:
- Choose an appropriate chunking strategy (size, overlap, structure-aware) for a given document type
- Explain how embeddings and vector indexes (HNSW, IVF) affect retrieval quality and speed
- Configure retrieval parameters such as top-k, similarity metric, and metadata filters
- Apply hybrid search and re-ranking to improve relevance over pure vector similarity
- Diagnose and fix common retrieval failures using evaluation metrics
video: aad-m2-l02-chunking-indexing-and-retrieval-strategies.mp4
quiz:
- q: Why add overlap between chunks?
  options:
  - To reduce the total number of vectors stored
  - To preserve context that would otherwise be cut at chunk boundaries
  - To make embeddings faster to compute
  - To force the LLM to read more text
  answer: 1
  why: Overlap repeats some tokens from the previous chunk so meaning spanning a boundary isn't lost,
    improving retrieval of split-up context.
- q: What is the main benefit of hybrid search over pure vector search?
  options:
  - It removes the need for an embedding model
  - It catches exact terms, names, and codes that embeddings often miss
  - It always returns fewer results
  - It eliminates the need for chunking
  answer: 1
  why: Hybrid search combines dense vector similarity with sparse keyword/BM25 matching, so exact tokens
    like product codes or acronyms are reliably retrieved.
- q: Which is a correct way to use a re-ranker in retrieval?
  options:
  - Retrieve top-1 then re-rank that single result
  - Retrieve a large candidate set (e.g., 20-50), re-rank, keep the best few
  - Skip vector search entirely and only re-rank
  - Re-rank before embedding the documents
  answer: 1
  why: Re-ranking works by pulling a broad candidate set with fast ANN search, then scoring query-passage
    pairs with a cross-encoder to keep the most relevant few.
- q: You change your chunk size from 800 to 400 tokens. What else must you do?
  options:
  - Nothing; the index updates automatically
  - Re-embed and re-index all chunks
  - Switch similarity metric to Euclidean
  - Increase top-k to 100
  answer: 1
  why: New chunk boundaries produce different text, so all chunks must be re-embedded and the index rebuilt
    to reflect the new chunks.
- q: Name one retrieval metric you would track to evaluate whether the correct passage is being retrieved.
  answer: Recall@k
  why: Recall@k (or hit rate) measures whether the expected source chunk appears in the top k retrieved
    results, directly evaluating retrieval correctness.
- q: Why must you use the same embedding model for both documents and queries?
  answer: So query and document vectors live in the same vector space and are comparable
  why: Different models produce incompatible vector spaces; similarity scores between them are meaningless,
    breaking retrieval.
resources:
- label: 'LangChain: Text Splitters documentation'
  url: https://python.langchain.com/docs/concepts/text_splitters/
- label: 'Pinecone Learn: Chunking and Retrieval Strategies'
  url: https://www.pinecone.io/learn/chunking-strategies/
- label: HNSW ANN index explained (Pinecone)
  url: https://www.pinecone.io/learn/series/faiss/hnsw/
- label: 'Ragas: Evaluation framework for RAG pipelines'
  url: https://docs.ragas.io/
---

## Why Chunking and Retrieval Matter

A Retrieval-Augmented Generation (RAG) app is only as good as the context it feeds the LLM. If retrieval returns irrelevant or fragmented passages, the model hallucinates or answers vaguely. Two levers control retrieval quality: **how you split documents (chunking)** and **how you search the index (retrieval strategy)**.

The pipeline is: `documents -> chunks -> embeddings -> vector index -> query -> retrieve -> (re-rank) -> context -> LLM`.

## Chunking Strategies

Chunking splits long documents into passages small enough to embed and fit in the prompt, but large enough to carry meaning.

- **Fixed-size chunking**: split by a token/character count (e.g., 512 tokens). Simple and fast, but can cut sentences mid-thought.
- **Overlap**: include the last N tokens of the previous chunk (e.g., 10-20% overlap) so context isn't lost at boundaries.
- **Recursive/structure-aware chunking**: split on natural separators in order — paragraphs, then sentences, then words. Keeps semantic units intact.
- **Document-structure chunking**: respect Markdown headings, HTML tags, code blocks, or PDF sections so each chunk maps to a logical unit.
- **Semantic chunking**: group sentences by embedding similarity, breaking when topic shifts.

### Rules of thumb

- Start with **~300-800 tokens** per chunk and **10-15% overlap**.
- Smaller chunks = more precise retrieval but more fragments and higher index cost.
- Larger chunks = more context per hit but more noise and risk of diluting the embedding.
- Attach **metadata** (source, title, section, page, date) to every chunk for filtering and citations.

## Embeddings and Indexing

Each chunk is converted to a vector by an embedding model (e.g., `text-embedding-3-small`). Choose an embedding model that matches your domain and language, and **use the same model for queries and documents**.

Vector databases store these vectors in an **Approximate Nearest Neighbor (ANN)** index for fast search:

- **HNSW** (graph-based): great recall/latency balance; tune `M` (connections) and `ef_search` (search breadth).
- **IVF** (cluster-based): partitions vectors into lists; tune `nprobe` (lists searched).
- **Flat / brute force**: exact but slow; fine for small datasets.

Similarity is measured with **cosine**, **dot product**, or **Euclidean** distance — pick what your embedding model was trained for (usually cosine).

## Retrieval Strategies

- **Top-k retrieval**: return the k most similar chunks. Typical k = 3-8. Too low misses context; too high adds noise and cost.
- **Metadata filtering**: restrict search by source, date, or user permissions before/while searching.
- **Hybrid search**: combine dense (vector) and sparse (keyword/BM25) retrieval to catch exact terms, names, and acronyms that embeddings miss.
- **Re-ranking**: retrieve a larger candidate set (e.g., 20-50), then use a cross-encoder re-ranker to score query-passage pairs and keep the best few.
- **Query transformations**: rewrite, expand, or split the user query (multi-query, HyDE) to improve recall.
- **MMR (Maximal Marginal Relevance)**: balances relevance with diversity to avoid near-duplicate chunks.

## Putting It Together (Example)

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600, chunk_overlap=80,
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_documents(docs)

# index chunks with metadata, then retrieve
results = vector_store.similarity_search(
    query, k=20, filter={"source": "handbook"}
)
top = reranker.rerank(query, results)[:5]
```

## Evaluating and Tuning

Don't guess — measure. Build a small set of question/expected-source pairs and track:

- **Recall@k / Hit rate**: did the right chunk appear in the top k?
- **Context precision**: how much retrieved text is actually relevant?
- **Faithfulness/answer quality**: does the final answer rely on retrieved context?

Tune one variable at a time: chunk size, overlap, k, hybrid weighting, re-ranking. Re-embed when you change chunking or the embedding model.

## Common Pitfalls

- Mismatched query/document embedding models.
- Chunks too large (noisy embeddings) or too small (lost context).
- No metadata, so no filtering or citations.
- Relying on pure vector search for exact-match queries (IDs, codes) — add keyword/hybrid.
- Forgetting to re-index after changing chunking parameters.
