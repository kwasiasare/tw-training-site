---
course: dami-ai-career
title: Chunking strategies
month: 3
monthTitle: LLM Application Skills
lesson: 9
summary: Split long documents into retrievable pieces that fit a model's context and return clean, relevant
  answers in a RAG pipeline.
objectives:
- Explain why chunking is needed for retrieval and long documents
- Compare fixed-size, recursive, and semantic chunking strategies
- Choose a sensible chunk size and overlap for a use case
- Implement character and token-based chunking in Python
- Preserve structure and attach metadata to each chunk
- Evaluate chunking quality by inspecting retrieved results
video: m3-l09-chunking.mp4
quiz:
- q: Why do we chunk documents before putting them in a retrieval system?
  options:
  - To make the text larger
  - To fit context limits and improve retrieval relevance
  - Because models cannot read English
  - To delete unimportant words
  answer: 1
  why: Chunks keep each retrieved piece focused and small enough to fit the context window, so search
    returns relevant passages instead of whole documents.
- q: What is the main purpose of chunk overlap?
  options:
  - To save storage space
  - To speed up the model
  - To avoid cutting a key idea exactly at a boundary
  - To encrypt the text
  answer: 2
  why: Overlap repeats a little text between neighbouring chunks so a sentence or idea split across a
    boundary still appears whole in at least one chunk.
- q: Which strategy splits on natural separators like paragraphs, then sentences, falling back to characters
    only if needed?
  options:
  - Fixed-size chunking
  - Recursive chunking
  - Random chunking
  - No chunking
  answer: 1
  why: Recursive chunking tries a priority list of separators (paragraph, line, sentence, word) so splits
    land on natural boundaries before resorting to raw character cuts.
- q: 'True or false: chunk size should always be measured in characters, never tokens.'
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Because models bill and limit by tokens, sizing chunks in tokens is often more reliable;
    characters are a convenient approximation only.
- q: Name one useful piece of metadata to store alongside each chunk and say why.
  answer: The source document name or page number, so retrieved answers can cite where they came from.
  why: Metadata such as source, title, page, or section lets you trace, filter, and cite chunks, which
    is essential for trustworthy RAG answers.
- q: In one sentence, what is a reasonable default starting point for chunk size and overlap?
  answer: Around 500 to 1000 tokens per chunk with roughly 10 to 20 percent overlap, then tune by inspecting
    results.
  why: These defaults balance enough context per chunk against retrieval precision; you adjust based on
    document type and observed answer quality.
resources:
- label: LangChain docs — Text Splitters (RecursiveCharacterTextSplitter)
  url: https://python.langchain.com/docs/concepts/text_splitters/
- label: Pinecone — Chunking Strategies for LLM Applications
  url: https://www.pinecone.io/learn/chunking-strategies/
- label: Anthropic docs — Token counting (size chunks by tokens)
  url: https://platform.claude.com/docs/en/build-with-claude/token-counting
- label: Anthropic Cookbook — Retrieval Augmented Generation
  url: https://github.com/anthropics/anthropic-cookbook
---

## Why chunking?

A language model can only read so much text at once, and a retrieval system works best when each stored piece is small and focused. **Chunking** is the act of splitting a long document into smaller pieces, called **chunks**, before you embed and store them.

If you store an entire 50-page PDF as one item, a search for one fact returns all 50 pages, most of it irrelevant. If you split it into paragraph-sized chunks, search returns just the passages that matter. Good chunking is often the single biggest lever on the quality of a Retrieval-Augmented Generation (RAG) system.

## The trade-off: size vs precision

Chunk size is a balance. **Large chunks** carry more surrounding context but dilute relevance and may overflow limits. **Small chunks** are precise but can lose the context needed to answer.

A common starting point is roughly **500 to 1000 tokens** per chunk. Size in **tokens**, not characters, because models limit and bill by tokens. A rough rule of thumb is one token per four characters of English, but count properly when it matters.

## Overlap

If you cut strictly every N tokens, you will sometimes slice a sentence or idea in half. **Overlap** repeats a small slice of text between neighbouring chunks so the idea survives in at least one chunk. A typical overlap is 10 to 20 percent of the chunk size.

```python
def chunk_text(text, size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap   # step back to create overlap
    return chunks

doc = open("report.txt", encoding="utf-8").read()
print(len(chunk_text(doc)))
```

This is **fixed-size** chunking: simple and fast, but blind to structure.

## Smarter strategies

**Recursive chunking** splits on a priority list of separators — paragraphs first, then lines, then sentences, then words — so cuts land on natural boundaries. **Semantic chunking** groups sentences by meaning, keeping related ideas together. Recursive is the practical default for most text.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""],
)
chunks = splitter.split_text(doc)
print(len(chunks), "chunks")
```

## Metadata matters

Each chunk should travel with **metadata**: the source file, a title, a page or section number. This lets you cite where an answer came from and filter retrieval. Without it, a correct answer is hard to trust.

## Sizing by tokens with Claude

When the downstream model is Claude, count tokens with the Anthropic SDK so chunks fit your budget exactly. Keep your A P I key in the `ANTHROPIC_API_KEY` environment variable.

```python
from anthropic import Anthropic

client = Anthropic()
for i, ch in enumerate(chunks):
    n = client.messages.count_tokens(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": ch}],
    ).input_tokens
    print(f"chunk {i}: {n} tokens")
```

## Your task

Take a long text file, chunk it three ways — fixed-size, recursive, and recursive with metadata — and inspect the boundaries of the first few chunks for each.
