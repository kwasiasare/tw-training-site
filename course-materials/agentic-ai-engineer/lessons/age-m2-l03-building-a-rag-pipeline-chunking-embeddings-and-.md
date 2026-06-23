---
course: agentic-ai-engineer
title: 'Building a RAG Pipeline: Chunking, Embeddings, and Retrieval'
month: 2
monthTitle: Reasoning, Memory, and Retrieval
lesson: 3
summary: Learn to build a retrieval-augmented generation (RAG) pipeline that grounds LLM agent responses
  in your own documents. We cover document chunking strategies, generating embeddings, storing vectors,
  and retrieving relevant context to inject into prompts—turning a general LLM into a knowledgeable, citation-backed
  assistant.
objectives:
- Explain why RAG is needed and how it reduces hallucination by grounding responses in source documents
- Choose and apply appropriate chunking strategies that balance context size and retrieval precision
- Generate embeddings and store them in a vector database for semantic search
- Implement a retrieval step that selects relevant chunks and assembles a grounded prompt
- Evaluate retrieval quality and apply improvements like metadata filtering and re-ranking
video: age-m2-l03-building-a-rag-pipeline-chunking-embeddings-and-.mp4
quiz:
- q: What is the primary purpose of RAG in an LLM agent?
  options:
  - To make the model train faster
  - To ground responses in external documents and reduce hallucination
  - To compress the model's weights
  - To replace the need for prompts
  answer: 1
  why: RAG retrieves relevant external text and injects it into the prompt so the model answers from real
    sources, reducing hallucination and adding up-to-date, domain knowledge.
- q: Why add overlap between consecutive chunks?
  options:
  - To reduce storage costs
  - So meaning split across a chunk boundary isn't lost
  - To make embeddings faster
  - To avoid using metadata
  answer: 1
  why: Overlap ensures a sentence or idea spanning a boundary appears in both chunks, preserving context
    for retrieval.
- q: What happens if you use different embedding models for ingestion and querying?
  options:
  - Nothing, they're interchangeable
  - Retrieval breaks because vectors aren't comparable
  - It speeds up search
  - It improves accuracy
  answer: 1
  why: Different models produce vectors in different spaces, so similarity comparisons become meaningless
    and retrieval quality collapses. Always use the same model for both.
- q: Which technique combines keyword search with vector search to catch exact terms like product codes?
  options:
  - Re-ranking
  - Hybrid search
  - Chunking
  - Query rewriting
  answer: 1
  why: Hybrid search merges keyword (e.g., BM25) and semantic vector retrieval, capturing both exact matches
    and semantic similarity.
- q: Name one metric you would use to evaluate the retrieval step of a RAG system.
  answer: recall@k (or precision@k)
  why: Recall@k measures whether the correct chunks appear in the top-k retrieved results; precision@k
    measures how many retrieved chunks are relevant. Both assess retrieval quality.
- q: Why should the prompt instruct the model to say 'I don't know' when the answer isn't in the context?
  answer: To prevent hallucination when retrieval fails or context is insufficient
  why: Explicit grounding and an abstain instruction make the model rely on provided context and avoid
    fabricating answers when the needed information wasn't retrieved.
resources:
- label: LangChain RAG / Retrieval documentation
  url: https://python.langchain.com/docs/concepts/rag/
- label: OpenAI Embeddings guide
  url: https://platform.openai.com/docs/guides/embeddings
- label: Chroma vector database docs
  url: https://docs.trychroma.com/
- label: 'RAGAS: evaluation framework for RAG pipelines'
  url: https://docs.ragas.io/
---

## Why RAG?

Large language models are trained on a fixed snapshot of public data. They don't know your company's internal docs, your latest product specs, or anything that changed after training. When asked about unfamiliar topics they often **hallucinate**—producing confident but wrong answers.

**Retrieval-Augmented Generation (RAG)** solves this by fetching relevant text from your own knowledge base at query time and injecting it into the prompt. The model then answers *from the provided context* rather than from memory. This gives you:

- Up-to-date, domain-specific answers without retraining
- Citations and traceability (you know which document a fact came from)
- Lower cost than fine-tuning, and easy content updates

## The RAG Pipeline at a Glance

A RAG system has two phases:

1. **Ingestion (offline):** load documents → chunk → embed → store vectors
2. **Query (online):** embed the question → retrieve top-k chunks → build prompt → generate answer

## Step 1: Chunking

You cannot embed an entire 50-page PDF as one vector—you'd lose precision and exceed context limits. Instead, split documents into **chunks**.

Key decisions:

- **Chunk size:** Too large and retrieval pulls in irrelevant text and wastes tokens; too small and you lose coherent meaning. A common starting point is **300–800 tokens**.
- **Overlap:** Add **10–20% overlap** between consecutive chunks so a sentence split across a boundary isn't lost.
- **Strategy:** Prefer **semantic/structural splitting** (by paragraph, heading, or sentence) over naive character counts. Respect document structure—don't cut mid-sentence when avoidable.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# from_tiktoken_encoder makes chunk_size/chunk_overlap count TOKENS, not
# characters—so these numbers match the 300–800 token guidance above.
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500,        # tokens (within the 300–800 range)
    chunk_overlap=75,      # tokens (~15% overlap)
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_text(document_text)
```

Attach **metadata** to each chunk (source filename, page, section, date). You'll use it for filtering and citations.

## Step 2: Embeddings

An **embedding** is a dense vector that captures semantic meaning. Texts with similar meaning map to nearby vectors. We embed each chunk once at ingestion and embed the query at search time, then compare with **cosine similarity**.

```python
from openai import OpenAI
client = OpenAI()

def embed(texts):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [d.embedding for d in resp.data]
```

Tips:

- Use the **same embedding model** for ingestion and querying.
- Batch embedding calls to cut cost and latency.
- Pick a model sized to your needs—smaller models are cheaper and often good enough.

## Step 3: Vector Store

A **vector database** indexes embeddings for fast approximate nearest-neighbor (ANN) search. Options include Chroma, FAISS, Pinecone, Weaviate, and pgvector.

```python
import chromadb
client = chromadb.Client()
col = client.create_collection("docs")

col.add(
    ids=[f"c{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embed(chunks),
    metadatas=[{"source": "handbook.pdf", "page": 3}] * len(chunks)
)
```

## Step 4: Retrieval and Prompt Assembly

At query time, embed the question and retrieve the top-k most similar chunks. Then build a prompt that instructs the model to answer **only** from the context.

```python
q_emb = embed([question])[0]
results = col.query(query_embeddings=[q_emb], n_results=4)
context = "\n\n".join(results["documents"][0])

prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}"""
```

This grounding instruction is critical: it tells the model to abstain rather than hallucinate when context is insufficient.

## Improving Retrieval Quality

- **Metadata filtering:** restrict search to a date range, department, or document type.
- **Re-ranking:** use a cross-encoder to re-score the top-k candidates for higher precision.
- **Hybrid search:** combine keyword (BM25) with vector search to catch exact terms like product codes.
- **Query rewriting:** expand or rephrase vague queries before retrieval.

## Evaluating RAG

Don't ship blind. Measure:

- **Retrieval metrics:** recall@k, precision@k—did the right chunk get retrieved?
- **Answer metrics:** faithfulness (is the answer supported by context?) and answer relevance.
- Build a small golden set of question/answer pairs and test changes against it.

## Common Pitfalls

- Mismatched embedding models between ingestion and query.
- Chunks too big (noisy) or too small (fragmented).
- No grounding instruction—model ignores context and hallucinates.
- Forgetting to store metadata, so you can't cite or filter.
