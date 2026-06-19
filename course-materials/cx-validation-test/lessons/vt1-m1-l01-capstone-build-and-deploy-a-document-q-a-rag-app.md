---
course: cx-validation-test
title: 'Capstone: Build and Deploy a Document Q&A RAG App with Python and an LLM'
month: 1
monthTitle: Building a RAG-Powered LLM Application in Python
lesson: 1
summary: In this capstone lesson you build a complete Document Q&A application in Python that ingests
  files, chunks and embeds them into a vector store, retrieves relevant context, and uses an LLM with
  retrieval-augmented generation to answer questions with citations. You then wrap it in a simple web
  UI and deploy it as a portfolio-ready project.
objectives:
- Design the end-to-end architecture of a RAG document Q&A application (ingest, embed, store, retrieve,
  generate).
- Implement a Python ingestion pipeline that loads, chunks, and embeds documents into a vector store.
- Build a retrieval + prompt-augmentation layer that grounds LLM answers in retrieved context and returns
  citations.
- Wrap the app in a minimal web UI (Streamlit) and handle configuration, secrets, and errors.
- Deploy the application to a hosting platform and document it as a portfolio project.
- Evaluate answer quality and apply practical improvements like chunk tuning and reranking.
video: vt1-m1-l01-capstone-build-and-deploy-a-document-q-a-rag-app.mp4
quiz:
- q: In a RAG pipeline, what is the correct order of the indexing phase?
  options:
  - Embed question -> retrieve -> generate
  - Load -> chunk -> embed -> store in vector DB
  - Store -> retrieve -> chunk -> embed
  - Generate -> embed -> store -> load
  answer: 1
  why: The offline indexing phase loads documents, splits them into chunks, embeds each chunk into a vector,
    and stores those vectors in a vector database. Retrieval and generation happen later at query time.
- q: Why set the LLM temperature to 0 for a factual document Q&A app?
  options:
  - It makes the model faster
  - It produces more deterministic, grounded answers
  - It increases creativity for better summaries
  - It reduces the embedding cost
  answer: 1
  why: Temperature 0 minimizes randomness, giving deterministic answers that stick closely to the retrieved
    context — ideal for factual Q&A where you want consistency and minimal hallucination.
- q: What is the main purpose of keeping metadata (like filename and page) on each chunk?
  options:
  - To compress the vectors
  - To enable source citations in the answer
  - To speed up embedding
  - To avoid using a vector store
  answer: 1
  why: Metadata travels with each chunk so that when chunks are retrieved you can show which document
    and page the answer came from, providing trustworthy citations.
- q: Which practice helps prevent the LLM from hallucinating answers not in your documents?
  options:
  - Using a larger chunk size
  - Instructing the prompt to answer only from context and otherwise say 'I don't know'
  - Disabling the vector store
  - Raising the temperature
  answer: 1
  why: A strict prompt that limits the model to the provided context and allows it to admit when the answer
    isn't present is the primary guardrail against hallucination in RAG.
- q: Name one reason RAG is often preferred over fine-tuning for a document Q&A app.
  answer: Knowledge stays fresh by re-indexing (no retraining), it grounds answers to reduce hallucination,
    and it is cheaper than training.
  why: RAG lets you update knowledge simply by re-indexing documents, grounds answers in real retrieved
    text, and avoids the cost and complexity of training a model.
- q: Why should you persist (save) the vector index to disk in your capstone app?
  answer: To avoid re-embedding documents on every run, saving time and API cost.
  why: Embedding is the expensive step; saving the FAISS index lets you load it instantly instead of recomputing
    embeddings each time the app starts.
resources:
- label: LangChain RAG / Q&A documentation
  url: https://python.langchain.com/docs/tutorials/rag/
- label: FAISS vector store (Facebook AI Similarity Search)
  url: https://github.com/facebookresearch/faiss
- label: Streamlit deployment docs (Community Cloud)
  url: https://docs.streamlit.io/deploy/streamlit-community-cloud
- label: OpenAI Embeddings guide
  url: https://platform.openai.com/docs/guides/embeddings
---

## What You're Building

You will ship a **Document Q&A app**: users upload PDFs or text files, ask natural-language questions, and get answers grounded in *their* documents with source citations. This is the canonical RAG (Retrieval-Augmented Generation) pattern and an excellent portfolio piece because it touches data engineering, embeddings, LLM prompting, and deployment.

## The RAG Architecture

RAG has two phases:

1. **Indexing (offline):** load documents -> split into chunks -> embed chunks -> store vectors.
2. **Query (online):** embed the question -> retrieve top-k similar chunks -> build a prompt with that context -> call the LLM -> return the answer + sources.

```
Docs -> Loader -> Chunker -> Embeddings -> Vector Store
                                              |
Question -> Embed -> Similarity Search -------+--> Context
                                              |
                          Prompt(Context+Q) -> LLM -> Answer + Citations
```

Why RAG instead of fine-tuning? It keeps knowledge **fresh and editable** (just re-index), reduces hallucination by grounding answers in real text, and is far cheaper than training.

## Project Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install langchain langchain-openai langchain-community \
            faiss-cpu pypdf streamlit python-dotenv tiktoken
```

Store secrets in a `.env` file (never commit it):

```
OPENAI_API_KEY=sk-...
```

```python
from dotenv import load_dotenv
load_dotenv()  # reads .env into environment
```

## Step 1 — Ingestion and Chunking

Documents are too large to fit in a prompt, so we split them. **Chunk size** and **overlap** are the most important knobs: too large and retrieval is imprecise; too small and you lose context. A good starting point is ~800–1000 characters with 100–150 overlap.

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

docs = PyPDFLoader("manual.pdf").load()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=150
)
chunks = splitter.split_documents(docs)
```

Each chunk keeps `metadata` (source filename, page) — essential for citations later.

## Step 2 — Embeddings and Vector Store

An **embedding** turns text into a vector so semantic similarity becomes geometric distance. We store these in a vector index (FAISS runs locally, great for a capstone).

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = FAISS.from_documents(chunks, embeddings)
store.save_local("index")  # persist so you don't re-embed every run
```

## Step 3 — Retrieval and Generation

At query time, retrieve the most relevant chunks and stuff them into the prompt. Use a strict prompt that tells the model to answer **only** from context and to say "I don't know" otherwise — this is your main anti-hallucination guardrail.

```python
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    """Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}
Answer:""")

retriever = store.as_retriever(search_kwargs={"k": 4})
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)
result = qa.invoke({"query": "What is the warranty period?"})
print(result["result"])
for d in result["source_documents"]:
    print(d.metadata)
```

Set `temperature=0` for factual Q&A to keep answers deterministic and grounded.

## Step 4 — The Web UI (Streamlit)

```python
import streamlit as st

st.title("📄 Document Q&A")
file = st.file_uploader("Upload a PDF", type="pdf")
question = st.text_input("Ask a question")
if file and question:
    # build/load index, run qa chain
    answer = qa.invoke({"query": question})
    st.write(answer["result"])
    st.caption("Sources: " + ", ".join(
        {d.metadata['source'] for d in answer['source_documents']}))
```

Cache the index with `@st.cache_resource` so you don't re-embed on every interaction.

## Step 5 — Deploy

Options for a free/cheap portfolio deploy:

- **Streamlit Community Cloud** — push to GitHub, connect repo, add `OPENAI_API_KEY` as a secret. Easiest.
- **Hugging Face Spaces** — supports Streamlit/Gradio apps.
- **Docker + a VM/Render** — most control.

Add a `requirements.txt`, a `README.md` with screenshots and architecture diagram, and **never** commit your API key. Use the platform's secrets manager.

## Evaluating and Improving

- **Tune chunking:** experiment with size/overlap and re-test on sample questions.
- **Increase k or add reranking:** retrieve more candidates, then rerank for precision.
- **Add metadata filters** (e.g., by document or date).
- **Track quality:** keep a small set of question/expected-answer pairs and spot-check after changes.
- **Manage cost:** cache embeddings, use smaller embedding/LLM models, and limit context length.

## Common Pitfalls

- Re-embedding on every run (persist the index!).
- Chunks too large to retrieve precisely.
- No "I don't know" guardrail -> hallucinations.
- Leaking API keys in the repo.
- Forgetting to surface citations, which kills user trust.
