---
course: dami-ai-career
title: Vector databases with Chroma
month: 3
monthTitle: LLM Application Skills
lesson: 8
summary: Store text as embeddings in Chroma and retrieve the most relevant chunks by meaning to ground
  your LLM answers.
objectives:
- Explain what an embedding is and why similar meanings sit close together
- Describe what a vector database stores and why you need one
- Create a Chroma collection and add documents with metadata
- Run a similarity query and read back the nearest results
- Understand cosine distance and how results are ranked
- Use retrieved chunks as context for a Claude prompt (RAG basics)
- Persist a Chroma collection to disk and reload it
video: m3-l08-vector-dbs.mp4
quiz:
- q: What does an embedding represent?
  options:
  - A compressed image of the text
  - A list of numbers capturing the text's meaning
  - The exact word count of the text
  - A unique database ID for the text
  answer: 1
  why: An embedding is a vector — a list of floating-point numbers — where similar meanings produce nearby
    vectors.
- q: Why use a vector database instead of a normal SQL database for semantic search?
  answer: A vector database indexes embeddings so it can find the nearest vectors by meaning quickly;
    SQL matches exact values or keywords, not meaning.
  why: Semantic search needs nearest-neighbour lookups over high-dimensional vectors, which SQL is not
    built to do efficiently.
- q: In Chroma, what do you get back from collection.query()?
  options:
  - Only the raw embedding vectors
  - The single most similar document
  - The nearest documents, their metadata, distances, and ids
  - A yes or no match flag
  answer: 2
  why: query() returns the top-k nearest documents along with their ids, metadatas, and distances so you
    can rank and use them.
- q: 'With cosine distance, which is more similar to the query: a result with distance 0.12 or one with
    distance 0.83?'
  options:
  - '0.83'
  - '0.12'
  - They are equally similar
  - You cannot tell from distance
  answer: 1
  why: Smaller distance means closer in vector space, so 0.12 is more similar than 0.83.
- q: In retrieval-augmented generation (RAG), what is the vector database's job?
  answer: To retrieve the most relevant chunks of your own data so they can be added to the prompt as
    context for the LLM.
  why: The model itself does the reasoning; Chroma supplies the relevant facts to ground the answer and
    reduce hallucination.
- q: True or false — Chroma can store a vector together with the original text and metadata.
  options:
  - 'True'
  - 'False'
  answer: 0
  why: Each Chroma record holds the embedding, the source document text, an id, and optional metadata
    like source or page.
resources:
- label: Chroma — Official documentation
  url: https://docs.trychroma.com/
- label: Chroma — Getting Started guide
  url: https://docs.trychroma.com/getting-started
- label: Pinecone — What is a vector database? (concept primer)
  url: https://www.pinecone.io/learn/vector-database/
- label: Anthropic docs — Embeddings & RAG overview
  url: https://docs.claude.com/en/docs/build-with-claude/embeddings
---

## Why a vector database?

LLMs are powerful, but they don't know about *your* documents — your notes, your company's policies, your PDFs. To answer questions about your data, you first need to **find the relevant pieces**, then hand them to the model.

Keyword search ("find the word *refund*") misses anything phrased differently. **Semantic search** finds text by *meaning*, so "money back" matches "refund". A **vector database** like Chroma is built exactly for this.

## Embeddings: meaning as numbers

An **embedding** is a list of numbers (a vector) that captures the meaning of a piece of text. A model turns each chunk of text into, say, 384 or 1536 numbers. Texts with similar meaning produce vectors that sit **close together** in that high-dimensional space.

As a maths graduate this is friendly territory: each document is a point in R^n, and "similar" means "a small distance apart".

## Your first Chroma collection

Install Chroma, then create a **collection** — a named bucket of documents. By default Chroma will embed the text for you.

```bash
pip install chromadb
```

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="notes")

collection.add(
    documents=[
        "Refunds are processed within 14 days.",
        "Our office is open Monday to Friday.",
        "Cats are excellent at sitting on keyboards.",
    ],
    metadatas=[{"topic": "billing"}, {"topic": "hours"}, {"topic": "misc"}],
    ids=["doc1", "doc2", "doc3"],
)
```

## Querying by meaning

Now ask a question. Chroma embeds your query, finds the nearest document vectors, and returns them ranked by **distance** (smaller = more similar).

```python
results = collection.query(
    query_texts=["How do I get my money back?"],
    n_results=2,
)

for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(round(dist, 3), doc)
```

The refund note comes back first, even though the words "money back" never appear in it.

## From retrieval to an answer (RAG)

**Retrieval-augmented generation** = retrieve the relevant chunks, then put them in the prompt. Chroma finds the facts; Claude does the reasoning.

```python
import chromadb
from anthropic import Anthropic

col = chromadb.Client().get_collection("notes")
hits = col.query(query_texts=["refund policy?"], n_results=2)
context = "\n".join(hits["documents"][0])

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user",
               "content": f"Use this context:\n{context}\n\nQuestion: What is the refund window?"}],
)
print(msg.content[0].text)
```

## Persisting your data

The in-memory client forgets everything on exit. Use a **persistent client** to save the collection to disk and reload it next time.

```python
client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection("notes")
```

## Your task

Take a handful of your own notes, load them into a persistent Chroma collection, and query it with three questions phrased differently from the text.
