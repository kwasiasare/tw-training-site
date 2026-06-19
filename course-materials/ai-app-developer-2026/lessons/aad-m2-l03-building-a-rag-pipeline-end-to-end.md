---
course: ai-app-developer-2026
title: Building a RAG Pipeline End to End
month: 2
monthTitle: Building RAG Applications with Vector Databases
lesson: 3
summary: Learn to build a complete Retrieval-Augmented Generation (RAG) pipeline that grounds LLM answers
  in your own documents, from ingestion and chunking through embedding, vector search, prompt assembly,
  and generation.
objectives:
- Explain the components of a RAG pipeline and why retrieval grounds LLM responses
- Ingest, chunk, and embed documents into a vector database
- Implement semantic retrieval of relevant context for a user query
- Assemble grounded prompts and generate answers with citations
- Evaluate and improve RAG quality and reduce hallucinations
video: aad-m2-l03-building-a-rag-pipeline-end-to-end.mp4
quiz:
- q: Why must you use the same embedding model for documents and queries?
  options:
  - To save on API costs
  - So vectors live in the same space and similarity is meaningful
  - Because vector databases require it
  - To make chunks the same size
  answer: 1
  why: Embeddings from different models occupy different vector spaces, so cosine similarity between them
    is meaningless. The same model ensures query and document vectors are comparable.
- q: What is the main purpose of adding overlap between chunks?
  options:
  - To increase the number of vectors stored
  - To prevent ideas spanning chunk boundaries from being lost
  - To reduce embedding costs
  - To improve LLM generation speed
  answer: 1
  why: Overlap ensures that a concept split across a chunk boundary still appears intact in at least one
    chunk, preserving its meaning for retrieval.
- q: Which instruction most helps reduce hallucinations in a RAG prompt?
  options:
  - Ask the model to be creative
  - Tell it to answer only from the provided context and say 'I don't know' otherwise
  - Increase the temperature setting
  - Remove all metadata from context
  answer: 1
  why: Explicitly constraining the model to the provided context and permitting an 'I don't know' response
    prevents it from fabricating answers from general training knowledge.
- q: In the indexing phase, what is the correct order of steps?
  options:
  - Embed, load, store, chunk
  - Load, chunk, embed, store
  - Chunk, store, load, embed
  - Retrieve, embed, generate, store
  answer: 1
  why: During offline indexing you load documents, chunk them into pieces, embed each chunk into a vector,
    then store those vectors with metadata in the vector database.
- q: Name one metric used to evaluate the retrieval (not generation) quality of a RAG system.
  answer: recall@k
  why: Retrieval quality is measured by metrics like recall@k or hit rate, which check whether the correct
    relevant chunks appear in the top-k results.
- q: What does the 'augment' step in RAG refer to?
  options:
  - Increasing the size of the training dataset
  - Injecting retrieved context into the prompt before generation
  - Adding more documents to the vector store
  - Fine-tuning the embedding model
  answer: 1
  why: Augmentation means enriching the prompt with the retrieved relevant context so the LLM generates
    an answer grounded in that information.
resources:
- label: LangChain RAG documentation
  url: https://python.langchain.com/docs/tutorials/rag/
- label: Chroma vector database docs
  url: https://docs.trychroma.com/
- label: 'RAGAS: RAG evaluation framework'
  url: https://docs.ragas.io/
- label: OpenAI embeddings guide
  url: https://platform.openai.com/docs/guides/embeddings
---

## What Is RAG and Why Use It

Retrieval-Augmented Generation (RAG) combines a retrieval system with a generative LLM. Instead of relying only on the model's frozen training knowledge, you fetch relevant snippets from your own knowledge base at query time and inject them into the prompt. This lets the model answer questions about private, recent, or domain-specific data while reducing hallucinations and enabling citations.

RAG is cheaper and faster than fine-tuning for keeping knowledge fresh: you just update the document store, no retraining needed.

## The End-to-End Pipeline

A RAG pipeline has two phases:

**Indexing (offline):**
1. **Load** documents (PDFs, web pages, markdown, databases).
2. **Chunk** text into manageable pieces (e.g., 300–800 tokens with overlap).
3. **Embed** each chunk into a vector using an embedding model.
4. **Store** vectors + metadata in a vector database (Pinecone, Chroma, Weaviate, pgvector).

**Querying (online):**
1. **Embed** the user query with the same embedding model.
2. **Retrieve** the top-k most similar chunks via vector similarity search.
3. **Augment** the prompt with retrieved context.
4. **Generate** an answer with the LLM, grounded in that context.

## Chunking Strategy

Chunking matters more than people expect. Chunks that are too large dilute relevance and waste context window; too small lose meaning.

- Start with ~500 tokens and 10–20% overlap so ideas spanning boundaries aren't lost.
- Split on semantic boundaries (paragraphs, headings) when possible.
- Attach metadata: source, title, page, section. This powers citations and filtering.

## Embeddings and the Vector Store

An embedding model maps text to a dense vector where semantic similarity equals geometric closeness (cosine similarity). Use the **same model** for documents and queries.

```python
from openai import OpenAI
import chromadb

client = OpenAI()
db = chromadb.PersistentClient(path="./store")
collection = db.get_or_create_collection("docs")

def embed(texts):
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in resp.data]

# Index chunks
collection.add(
    ids=[f"c{i}" for i in range(len(chunks))],
    embeddings=embed(chunks),
    documents=chunks,
    metadatas=[{"source": s} for s in sources],
)
```

## Retrieval and Prompt Assembly

At query time, embed the question, search for top-k chunks, then build a prompt that instructs the model to answer **only** from the provided context.

```python
def answer(question, k=4):
    q_emb = embed([question])[0]
    hits = collection.query(query_embeddings=[q_emb], n_results=k)
    context = "\n\n".join(hits["documents"][0])
    prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
```

## Reducing Hallucinations and Citing Sources

- Explicitly instruct the model to say "I don't know" when context is insufficient.
- Include source metadata in context so the model can cite it.
- Return the retrieved chunks alongside the answer for transparency.

## Evaluating RAG Quality

Measure two things separately:

- **Retrieval quality:** are the right chunks returned? Use recall@k, hit rate.
- **Generation quality:** is the answer faithful to the context (faithfulness) and does it address the question (relevance)?

Tools like RAGAS automate faithfulness and relevance scoring. Iterate on chunk size, k, embedding model, and prompt wording based on measured failures.

## Common Pitfalls

- Using different embedding models for index and query.
- Forgetting overlap, splitting sentences mid-idea.
- Stuffing too many chunks and exceeding context limits.
- Not handling the "no relevant docs" case.
