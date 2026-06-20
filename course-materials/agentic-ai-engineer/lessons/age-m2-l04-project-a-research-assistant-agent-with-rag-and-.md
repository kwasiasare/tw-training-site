---
course: agentic-ai-engineer
title: 'Project: A Research Assistant Agent with RAG and Memory'
month: 2
monthTitle: Reasoning, Memory, and Retrieval
lesson: 4
summary: Build a production-minded research assistant agent that plans queries, retrieves from a document
  corpus with RAG, maintains short- and long-term memory, and answers with cited sources.
objectives:
- Design an agent architecture that combines a planner, RAG retriever, and memory layers
- Implement document ingestion, chunking, and embedding into a vector store
- Build a retrieval pipeline that returns relevant passages with source metadata for citations
- Add short-term (conversation) and long-term (persistent) memory to the agent
- Compose the components into an answer-synthesis loop that grounds responses and cites sources
- Evaluate the assistant for faithfulness, citation accuracy, and retrieval quality
video: age-m2-l04-project-a-research-assistant-agent-with-rag-and-.mp4
quiz:
- q: Why must chunk metadata (title, source_url, chunk_index) be stored alongside embeddings?
  options:
  - It improves embedding quality
  - It is required to produce verifiable citations
  - It reduces vector storage size
  - It speeds up the embedding model
  answer: 1
  why: Citations require knowing which document and location a retrieved passage came from, which is exactly
    what the stored metadata provides.
- q: What is the main purpose of instructing the synthesizer to 'say you don't know' when sources lack
    the answer?
  options:
  - To shorten responses
  - To reduce hallucination by preventing ungrounded claims
  - To save tokens
  - To skip the retrieval step
  answer: 1
  why: Telling the model to refuse when the context doesn't support an answer is a key technique for keeping
    responses grounded and reducing fabrication.
- q: Which memory type lets the agent resolve a follow-up like 'what about its limitations?'
  options:
  - Long-term persistent memory
  - Short-term conversational memory
  - The vector index
  - The reranker
  answer: 1
  why: Short-term conversational memory holds the recent dialogue, enabling the planner to rewrite ambiguous
    follow-ups into standalone questions.
- q: Why is chunk overlap used during ingestion?
  options:
  - To increase the number of vectors for billing
  - So context isn't cut off mid-thought at chunk boundaries
  - To make embeddings deterministic
  - To avoid storing metadata
  answer: 1
  why: Overlap preserves continuity across chunk boundaries so a relevant idea split between two chunks
    is still retrievable in full.
- q: Name one metric you would track to evaluate the research assistant's groundedness.
  answer: Faithfulness (or citation accuracy / retrieval recall)
  why: Faithfulness measures whether each claim is supported by a cited passage; citation accuracy and
    retrieval recall are also valid groundedness-related metrics.
- q: Why should facts recalled from long-term memory be re-grounded against the corpus before being cited?
  answer: To ensure attribution is accurate and the cited source actually supports the claim
  why: Memory may store paraphrased or stale facts; re-grounding against the corpus ensures the citation
    points to a real, current source that supports the statement.
resources:
- label: 'RAGAS: Evaluation framework for RAG pipelines'
  url: https://docs.ragas.io/
- label: LangChain RAG documentation
  url: https://python.langchain.com/docs/tutorials/rag/
- label: Chroma vector database docs
  url: https://docs.trychroma.com/
- label: OpenAI Embeddings guide
  url: https://platform.openai.com/docs/guides/embeddings
---

## Overview

In this capstone project you assemble the pieces from earlier lessons—planning, memory, and retrieval—into a single **research assistant agent**. The agent answers questions over a document corpus and backs every claim with citations to source passages.

The goal is not a toy demo but a pattern you can ship: clear ingestion, deterministic retrieval, grounded generation, and verifiable citations.

## Architecture

The agent has four cooperating components:

1. **Planner** — decomposes a user question into one or more retrieval queries and decides whether memory or fresh retrieval is needed.
2. **Retriever (RAG)** — embeds queries, searches a vector store, and returns ranked chunks with source metadata.
3. **Memory** — short-term conversational buffer plus long-term persistent store of facts and prior findings.
4. **Synthesizer** — an LLM call that composes a grounded answer from retrieved context and inserts inline citations.

```
User Q -> Planner -> {Memory lookup, Retrieval} -> Context -> Synthesizer -> Answer + Citations
```

## Step 1: Ingestion and Indexing

Before the agent can answer anything, build the corpus index.

- **Load** documents (PDF, Markdown, HTML).
- **Chunk** text into ~500-800 token passages with ~10-15% overlap so context isn't cut mid-thought.
- **Embed** each chunk with an embedding model.
- **Store** vectors plus metadata: `doc_id`, `title`, `source_url`, `chunk_index`.

```python
from chromadb import Client
from openai import OpenAI

client = OpenAI()
db = Client()
collection = db.create_collection("research_corpus")

def embed(text):
    return client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding

for chunk in chunks:
    collection.add(
        ids=[chunk.id],
        embeddings=[embed(chunk.text)],
        documents=[chunk.text],
        metadatas=[{"title": chunk.title, "source_url": chunk.url, "chunk_index": chunk.idx}],
    )
```

Metadata is what makes citations possible—store it carefully.

## Step 2: Retrieval with Citations

Retrieval returns both the passage text and the metadata needed to cite it.

```python
def retrieve(query, k=5):
    results = collection.query(query_embeddings=[embed(query)], n_results=k)
    passages = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        passages.append({"text": doc, "title": meta["title"], "url": meta["source_url"]})
    return passages
```

Consider a **reranking** step (cross-encoder) for higher precision, and dedupe near-identical chunks.

## Step 3: Memory Layers

- **Short-term memory**: the running conversation, kept in a buffer or summarized when it grows. Lets the agent resolve follow-ups like "what about its limitations?"
- **Long-term memory**: facts the agent has confirmed or summaries of past sessions, persisted in a store (often the same vector DB in a separate collection). Retrieved by relevance like any other source.

Keep memory and corpus retrieval separate so you can attribute answers correctly: a fact recalled from memory should be re-grounded against the corpus before being cited as a source.

## Step 4: The Planner Loop

The planner decides the strategy. A simple but effective pattern:

1. Rewrite the user question into standalone form using conversation history.
2. Generate 1-3 search queries (multi-query expansion improves recall).
3. Retrieve for each, merge and dedupe passages.
4. If retrieved context is weak (low scores), reformulate or ask a clarifying question.

## Step 5: Grounded Synthesis with Citations

Prompt the synthesizer to answer **only** from provided context and to cite using numbered references.

```python
SYSTEM = '''Answer using ONLY the numbered sources below.
Cite claims inline as [n]. If the sources do not contain the answer,
say you don't know. Do not invent citations.'''

def synthesize(question, passages):
    context = "\n".join(f"[{i+1}] {p['text']} (Source: {p['title']})"
                        for i, p in enumerate(passages))
    msg = f"Sources:\n{context}\n\nQuestion: {question}"
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"system","content":SYSTEM},
                  {"role":"user","content":msg}],
    ).choices[0].message.content
```

The "say you don't know" instruction is critical for reducing hallucination.

## Step 6: Evaluation

Measure what matters before shipping:

- **Faithfulness / groundedness**: is every claim supported by a cited passage?
- **Citation accuracy**: do the cited sources actually contain the claim?
- **Retrieval recall**: does the top-k contain the gold passage?
- **Answer relevance**: does it address the question?

Use a small labeled question set and an LLM-as-judge or frameworks like RAGAS. Track these metrics as you change chunking, k, or models.

## Production Considerations

- Cache embeddings and frequent queries.
- Log retrieved passages with each answer for auditability.
- Set a confidence threshold to fall back to "I don't know."
- Re-index when the corpus changes; version your index.
