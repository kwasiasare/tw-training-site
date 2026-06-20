---
course: ai-app-developer-2026
title: 'Project: Document Q&A Chatbot'
month: 2
monthTitle: Building RAG Applications with Vector Databases
lesson: 4
summary: A hands-on project lesson where you build a complete RAG-powered Document Q&A chatbot that ingests
  PDFs, retrieves relevant chunks from a vector database, and answers questions with cited sources.
objectives:
- Build an end-to-end ingestion pipeline that loads, chunks, and embeds PDF documents into a vector database
- Implement a retrieval function that returns the most relevant chunks for a user query
- Construct a grounded prompt that instructs the LLM to answer only from retrieved context and cite sources
- Assemble a chat loop that maintains context and returns answers with inline source citations
- Evaluate and debug common RAG failure modes like hallucination, poor retrieval, and chunking issues
video: aad-m2-l04-project-document-q-a-chatbot.mp4
quiz:
- q: Why do we store metadata like filename and page number with each chunk?
  options:
  - To make embeddings more accurate
  - To enable source citations in the final answer
  - To reduce the size of the vector database
  - To speed up similarity search
  answer: 1
  why: Metadata travels with the chunk through retrieval so the answer can cite exactly which file and
    page it came from.
- q: What is the single most effective prompt technique to reduce hallucination in RAG?
  options:
  - Increasing temperature
  - Instructing the model to answer only from the provided context and admit when it doesn't know
  - Using a larger model
  - Retrieving more chunks
  answer: 1
  why: Grounding the model with an explicit instruction to use only the supplied context — and to say
    'I don't know' otherwise — is the primary defense against hallucination.
- q: Why should you persist the vector database to disk after ingestion?
  options:
  - To improve answer quality
  - Because embedding is slow and costly, so you avoid re-doing it on every run
  - Because the LLM requires it
  - To enable multi-turn chat memory
  answer: 1
  why: Embedding all chunks is the expensive, time-consuming step; persisting lets you reuse the vectors
    without re-embedding.
- q: What problem does chunk overlap solve?
  options:
  - It reduces token costs
  - It prevents losing context that spans a chunk boundary
  - It improves embedding model accuracy globally
  - It removes duplicate documents
  answer: 1
  why: Overlap ensures information that straddles two chunks isn't cut off and lost, preserving context
    for retrieval.
- q: In one sentence, why must the same embedding model be used during ingestion and at query time?
  answer: Because query and document vectors must live in the same vector space for similarity search
    to be meaningful; different models produce incomparable embeddings.
  why: Similarity is only meaningful when both the stored chunk vectors and the query vector are produced
    by the same model in the same vector space.
- q: What is a good strategy for handling vague follow-up questions like 'What about its price?' in a
    chat loop?
  answer: Rewrite the follow-up into a standalone question using conversation history before performing
    retrieval.
  why: Vector search needs an explicit query; rewriting resolves pronouns and references so retrieval
    finds the right chunks.
resources:
- label: LangChain RAG Tutorial (official docs)
  url: https://python.langchain.com/docs/tutorials/rag/
- label: Chroma Vector Database Documentation
  url: https://docs.trychroma.com/
- label: OpenAI Embeddings Guide
  url: https://platform.openai.com/docs/guides/embeddings
- label: Streamlit – Build a chat UI
  url: https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
---

## Project Overview

In this project you build a **Document Q&A chatbot** using Retrieval-Augmented Generation (RAG). The bot answers questions over a custom set of PDFs and shows the **source** for every answer, so users can verify claims. This ties together everything from the module: embeddings, vector search, prompt construction, and the LLM call.

The architecture has two phases:

1. **Ingestion (offline):** Load PDFs → split into chunks → embed each chunk → store vectors + metadata in a vector DB.
2. **Query (online):** Embed the user question → search the vector DB for top-k chunks → build a grounded prompt → call the LLM → return the answer with citations.

## Step 1: Ingest and Chunk PDFs

Use a loader (e.g. `pypdf` or LangChain's `PyPDFLoader`) to extract text page by page. Keep page numbers and file names as **metadata** — you need these for citations later.

Split text into overlapping chunks. A `RecursiveCharacterTextSplitter` with `chunk_size=1000` and `chunk_overlap=150` is a sane default. Overlap prevents losing context that straddles a chunk boundary.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(pages)
```

## Step 2: Embed and Store

Each chunk is converted to a vector with an embedding model (e.g. `text-embedding-3-small`). Store the vector along with the original text and metadata in a vector store such as **Chroma**, **FAISS**, or **Pinecone**.

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
vectordb = Chroma.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"), persist_directory="./db")
```

Persist the DB so you don't re-embed on every run — embedding is the slow, costly part.

## Step 3: Retrieve Relevant Context

At query time, embed the question and run a similarity search for the top-k chunks (start with k=4). Each returned chunk carries its source metadata.

```python
retriever = vectordb.as_retriever(search_kwargs={"k": 4})
docs = retriever.invoke(user_question)
```

## Step 4: Build a Grounded Prompt

The key to reducing hallucination is **instructing the model to answer only from the provided context** and to say "I don't know" when the context is insufficient. Include source labels so the model can cite them.

```python
context = "\n\n".join(f"[{d.metadata['source']} p.{d.metadata['page']}] {d.page_content}" for d in docs)
prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.
Cite sources in brackets like [file.pdf p.3].

Context:
{context}

Question: {user_question}"""
```

## Step 5: Generate and Cite

Send the prompt to the chat model with a low temperature (0–0.2) for factual consistency. Display the answer plus the list of source documents that were retrieved.

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
answer = llm.invoke(prompt).content
```

## Step 6: Chat Loop and Memory

Wrap it in a loop. For multi-turn chat, prepend recent conversation history to the question, or use a query-rewriting step to make follow-up questions standalone before retrieval ("What about its price?" → "What about the price of Product X?").

## Debugging Common RAG Failures

- **Hallucination:** Tighten the prompt; lower temperature; confirm context is actually being injected.
- **Bad retrieval:** Try smaller chunks, more overlap, increase k, or check the embedding model matches between ingest and query.
- **Wrong citations:** Verify metadata is preserved through chunking.
- **Truncated context:** Watch the context window; cap k or chunk size.

## Stretch Goals

Add a relevance threshold to drop weak matches, a reranker for better ordering, streaming responses, and a simple web UI with Streamlit or Gradio.
