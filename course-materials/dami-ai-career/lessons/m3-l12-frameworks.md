---
title: 'Frameworks: LangChain / LlamaIndex'
month: 3
monthTitle: LLM Application Skills
lesson: 12
summary: Use LangChain and LlamaIndex to wire LLMs, prompts, and your own documents into real applications
  faster.
objectives:
- Explain what an LLM framework is and the problem it solves
- Compare LangChain (general orchestration) and LlamaIndex (data/RAG focus)
- Build a simple prompt-to-model chain with LCEL
- Load documents, index them, and query with LlamaIndex
- Understand retrieval-augmented generation (RAG) at a high level
- Know when a framework helps and when raw SDK calls are simpler
video: m3-l12-frameworks.mp4
quiz:
- q: What is the main job of a framework like LangChain?
  options:
  - To train new language models
  - To orchestrate LLMs, prompts, tools, and data into apps
  - To replace Python entirely
  - To store your API keys securely
  answer: 1
  why: LangChain provides reusable building blocks to wire prompts, models, retrievers, and tools together
    — it does not train models.
- q: Which framework is most focused on connecting your own documents to an LLM (RAG)?
  options:
  - LangChain
  - LlamaIndex
  - NumPy
  - Flask
  answer: 1
  why: LlamaIndex specialises in loading, indexing, and retrieving over your data, though LangChain can
    do RAG too.
- q: In a RAG pipeline, why do we retrieve documents before calling the model?
  answer: To give the model relevant, up-to-date context it was not trained on, reducing hallucinations.
  why: Retrieval injects your specific facts into the prompt so the answer is grounded in real source
    material.
- q: What does LCEL stand for and what is it for?
  answer: LangChain Expression Language — a declarative way to compose components into chains using the
    pipe operator.
  why: LCEL lets you connect prompt, model, and output parser with a clean, streamable, composable syntax.
- q: When might you skip a framework and call the SDK directly?
  options:
  - For a single, simple model call with no retrieval or tools
  - When you need many chained steps
  - When building a large RAG system
  - When connecting many data sources
  answer: 0
  why: For one-off simple calls a framework adds overhead; the raw Anthropic SDK is clearer and has fewer
    moving parts.
- q: True or false — frameworks store your API key for you so you do not need environment variables.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. You still keep secrets like ANTHROPIC_API_KEY in environment variables; the framework just
    reads them.
resources:
- label: LangChain Documentation (official)
  url: https://python.langchain.com/
- label: LlamaIndex Documentation (official)
  url: https://docs.llamaindex.ai/
- label: Anthropic Claude — Messages API docs
  url: https://docs.anthropic.com/en/api/messages
- label: LangChain — Anthropic integration (langchain-anthropic)
  url: https://python.langchain.com/docs/integrations/chat/anthropic/
---

## Why frameworks?

By now you can call a language model directly with the Anthropic SDK. That works well for a single request. But real applications need more: a prompt template here, a model call there, your own documents pulled in, maybe a tool the model can use. Wiring all that by hand gets messy fast.

A **framework** gives you reusable building blocks for these jobs so you write less plumbing and focus on your logic. The two best known in the LLM world are **LangChain** and **LlamaIndex**.

## LangChain vs LlamaIndex

Think of them as overlapping but with different centres of gravity.

- **LangChain** — broad orchestration. Prompts, models, output parsers, tools, agents, memory. Good when your app has several steps chained together.
- **LlamaIndex** — data-first. Loading documents, splitting them, indexing, and retrieving the right chunks. Built for **RAG** (retrieval-augmented generation).

They are not rivals you must choose between forever — many projects use both. Start with the one that matches your main need.

## A simple LangChain chain (LCEL)

**LCEL** (LangChain Expression Language) composes components with the pipe `|` operator: a prompt feeds a model, the model feeds a parser.

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Explain {topic} in one sentence.")
model = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1024)
chain = prompt | model | StrOutputParser()

print(chain.invoke({"topic": "eigenvalues"}))
```

The key reads from the `ANTHROPIC_API_KEY` environment variable — never hard-code it.

## RAG with LlamaIndex

RAG means: **retrieve** relevant text, then **generate** an answer grounded in it. This lets the model answer questions about *your* documents — things it was never trained on.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

docs = SimpleDirectoryReader("my_notes").load_data()
index = VectorStoreIndex.from_documents(docs)
engine = index.as_query_engine()

print(engine.query("What did my notes say about gradient descent?"))
```

Under the hood it splits your files into chunks, embeds them as vectors, finds the closest chunks to your question, and passes them to the model as context.

## When NOT to use a framework

Frameworks add layers. For a single, simple model call with no retrieval and no tools, the raw Anthropic SDK is clearer:

```python
from anthropic import Anthropic

client = Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarise photosynthesis."}],
)
print(msg.content[0].text)
```

Reach for a framework when you have multiple steps, retrieval over data, tools, or agents.

## Your task

Pick a folder of your own notes or PDFs and build a tiny RAG app with LlamaIndex that answers a question about them. Keep your API key in an environment variable.
