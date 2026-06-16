---
course: kwasi-GenAI
title: Chunking strategies
month: 2
monthTitle: Retrieval-Augmented Generation (RAG)
lesson: 2
summary: Learn why naive fixed-size chunking breaks retrieval, and how overlap plus structure-aware and
  semantic chunking keep each chunk meaningful and self-contained.
objectives:
- Explain why documents must be split into chunks before embedding
- Describe how naive fixed-size chunking severs sentences and meaning
- Apply overlap to preserve context across chunk boundaries
- Use structure-aware splitting that respects headings, paragraphs, and code
- Explain the idea behind semantic chunking and when it helps
- Choose a starting chunk size and overlap and justify the trade-offs
video: g2-l02-chunking.mp4
quiz:
- q: Why do we split documents into chunks before embedding them?
  options:
  - To make the files smaller on disk
  - So each retrievable unit fits the embedding model and represents one focused idea
  - Because APIs reject any text over 10 words
  - To remove duplicate words
  answer: 1
  why: Chunks must fit the embedding model's input limit and be focused enough that one chunk answers
    one question; whole documents are too broad to retrieve precisely.
- q: What is the main failure of naive fixed-size character chunking?
  options:
  - It is too slow
  - It cuts sentences and ideas mid-thought, producing meaningless fragments
  - It uses too much disk
  - It only works in English
  answer: 1
  why: Splitting strictly every N characters ignores sentence and paragraph boundaries, so a chunk can
    start mid-sentence and lose the meaning needed to retrieve it.
- q: What does chunk overlap achieve?
  options:
  - It compresses the text
  - It repeats a slice of text between adjacent chunks so context isn't lost at boundaries
  - It deletes redundant chunks
  - It encrypts the chunks
  answer: 1
  why: Overlap carries the end of one chunk into the start of the next, so a fact split across a boundary
    still appears whole in at least one chunk.
- q: Structure-aware chunking means…
  options:
  - Splitting only by character count
  - Splitting along headings, paragraphs, lists, and code blocks the document already has
  - Randomly shuffling chunks
  - Removing all formatting first
  answer: 1
  why: Respecting the document's own structure keeps each chunk a coherent unit, like a whole section
    or paragraph, which embeds and retrieves far better.
- q: In one sentence, why can a chunk that is too large hurt retrieval?
  answer: A large chunk mixes several topics, so its embedding is a blurry average that matches no single
    query well and wastes context budget.
  why: One vector must represent the whole chunk; if it covers many ideas, it sits between them all and
    matches none precisely, and it also crowds the prompt.
- q: Name a sensible starting point for chunk size and overlap, and say why you'd tune it.
  answer: Around 500-1000 tokens with 10-20% overlap, then tune based on whether retrieval returns complete,
    on-topic answers for your real questions.
  why: These defaults balance focus and context; the right values depend on your documents and queries,
    so you measure and adjust.
resources:
- label: Pinecone — Chunking strategies for LLM applications
  url: https://www.pinecone.io/learn/chunking-strategies/
- label: LangChain docs — Text splitters
  url: https://python.langchain.com/docs/concepts/text_splitters/
- label: Anthropic — Contextual Retrieval
  url: https://www.anthropic.com/news/contextual-retrieval
- label: Unstructured — Chunking for RAG
  url: https://docs.unstructured.io/open-source/core-functionality/chunking
- label: Weaviate — An overview of chunking strategies
  url: https://weaviate.io/blog/chunking-strategies-for-rag
---

## Why we chunk at all

In the last lesson you turned text into embeddings. But you rarely embed a whole document. A 40-page PDF becomes one vector that means "a bit of everything" — too blurry to match any specific question, and probably too long for the embedding model anyway. So before embedding, we **chunk**: split each document into smaller pieces, embed each piece, and store them. At query time we retrieve the few *chunks* most relevant to the question.

The goal of a good chunk is simple: **one chunk should be a focused, self-contained idea** — big enough to be meaningful, small enough that its single embedding really represents it.

## Why naive fixed-size chunking fails

The tempting first approach is to cut every N characters: "give me 1000-character chunks". This breaks badly. Character 1000 lands wherever it lands — mid-sentence, mid-word, halfway through a table. You get fragments like `...the refund policy applies only if` with the rest stranded in the next chunk. That fragment embeds to something vague, and the actual answer is now split across two chunks, so neither retrieves cleanly.

```python
# Naive — DON'T ship this
def bad_chunks(text, size=1000):
    return [text[i:i+size] for i in range(0, len(text), size)]
# cuts sentences, tables, and code mid-thought
```

Fixed-size *by token count* is a little better than by character, but it still ignores meaning and structure.

## Fix one: overlap

The cheapest improvement is **overlap**. Carry the last slice of each chunk into the start of the next — say a 10–20% overlap. Now a fact that straddles a boundary appears whole in at least one chunk. Overlap costs a little extra storage and some duplication, but it dramatically reduces "the answer was cut in half" failures.

```python
def overlap_chunks(text, size=800, overlap=120):
    step = size - overlap
    return [text[i:i+size] for i in range(0, len(text), step)]
```

## Fix two: respect the document's structure

Documents already tell you where the natural seams are: headings, paragraphs, list items, code blocks, table rows. **Structure-aware** (or recursive) splitting prefers to break on those boundaries first, and only falls back to a hard size limit if a section is still too big. The result: each chunk tends to be a whole paragraph or a whole subsection — a coherent unit.

This matters enormously for the technical docs you'll work with. You never want to split a code block down the middle, or separate a heading from the paragraph it introduces. Splitters like LangChain's recursive splitter, or layout-aware tools like Unstructured, do this for you across Markdown, HTML, and PDF.

## Fix three: semantic chunking

The most advanced approach is **semantic chunking**: walk through the document sentence by sentence and start a new chunk only when the topic *shifts* — detected by a drop in embedding similarity between consecutive sentences. This keeps each chunk topically tight, at the cost of extra computation. Use it when documents are dense and unstructured. A related, very effective technique is Anthropic's **Contextual Retrieval**, which prepends a short, model-generated description of where each chunk sits in the document before embedding it, so the chunk carries its own context.

## Picking a starting point

Don't agonise. A reasonable default for prose is roughly **500–1000 tokens per chunk with 10–20% overlap**, using a structure-aware splitter. Then *measure*: ask your real questions and check whether the retrieved chunks contain complete, on-topic answers. If answers feel truncated, increase size or overlap; if chunks feel unfocused and noisy, shrink them.

## Your task

Take one real document (a PDF or Markdown file you care about). Chunk it two ways: naive fixed-size, and structure-aware with overlap. Print three chunks from each and compare — note how the naive chunks cut ideas in half while the structure-aware chunks stay coherent.
