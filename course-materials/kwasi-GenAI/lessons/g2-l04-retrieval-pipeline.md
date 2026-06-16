---
course: kwasi-GenAI
title: The retrieval pipeline
month: 2
monthTitle: Retrieval-Augmented Generation (RAG)
lesson: 4
summary: 'Wire the full RAG flow end to end: take a query, embed it, run similarity search, assemble retrieved
  chunks into context, and prompt the model — with sensible top-k and context handling.'
objectives:
- 'Trace the five stages of a RAG query: embed, search, assemble, prompt, answer'
- Choose a top-k value and explain the precision/recall trade-off
- Assemble retrieved chunks into a clean, bounded context block
- Write a system prompt that grounds the model in the retrieved context
- Send retrieved context to Claude using the Messages API
- Spot and handle the case where retrieval returns nothing relevant
video: g2-l04-retrieval-pipeline.mp4
quiz:
- q: What are the stages of a basic RAG query, in order?
  options:
  - Prompt, embed, search, answer
  - Embed query, similarity search, assemble context, prompt model, answer
  - Search, fine-tune, embed, answer
  - Answer, then retrieve to check
  answer: 1
  why: RAG embeds the user's query, runs similarity search for relevant chunks, assembles them into context,
    puts that in the prompt, and the model answers from it.
- q: What does top-k control in retrieval?
  options:
  - The model's temperature
  - How many of the most similar chunks you retrieve
  - The embedding dimension
  - The number of tokens in the answer
  answer: 1
  why: top-k is the number of nearest chunks returned; too small may miss the answer, too large floods
    the prompt with noise.
- q: Why not just set top-k very high to be safe?
  options:
  - It costs nothing
  - Too many chunks add noise, cost tokens, and can dilute or distract the model
  - The database forbids it
  - It improves embeddings
  answer: 1
  why: Extra low-relevance chunks waste context budget and can bury the real answer, hurting both quality
    and cost.
- q: Where do the retrieved chunks go in a Claude Messages API call?
  options:
  - Into the model weights
  - Into the prompt as context, with a system prompt instructing the model to use it
  - Into the embedding model
  - Nowhere — Claude fetches them itself
  answer: 1
  why: Retrieved text is placed in the prompt (often the user turn) with a system prompt telling Claude
    to answer only from that provided context.
- q: In one sentence, what should your system do when retrieval returns nothing relevant?
  answer: Detect the low scores or empty result and have the model say it doesn't know, rather than inventing
    an answer.
  why: Grounding means no context, no claim; surfacing 'I don't have that information' beats a confident
    hallucination.
- q: Why separate and clearly delimit each retrieved chunk in the context block?
  answer: So the model can tell sources apart and you can attach citations to specific chunks later.
  why: Clear delimiters and ids per chunk make grounding and citation reliable, which lesson 7 builds
    on.
resources:
- label: Anthropic docs — Messages API reference
  url: https://docs.anthropic.com/en/api/messages
- label: 'Anthropic — Prompt engineering: use XML tags'
  url: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- label: LangChain — Build a Retrieval Augmented Generation (RAG) app
  url: https://python.langchain.com/docs/tutorials/rag/
- label: Anthropic — Contextual Retrieval
  url: https://www.anthropic.com/news/contextual-retrieval
- label: AWS — Retrieval Augmented Generation (RAG) explained
  url: https://aws.amazon.com/what-is/retrieval-augmented-generation/
---

## The whole flow on one page

Everything in the last three lessons now clicks together. A RAG query has five stages:

1. **Embed the query** — turn the user's question into a vector with the *same* embedding model you used for the documents.
2. **Similarity search** — ask the vector database for the top-k nearest chunks.
3. **Assemble context** — stitch those chunks into one clean, bounded block of text.
4. **Prompt the model** — put the context and the question into a Claude Messages API call, with a system prompt that says "answer only from this context".
5. **Answer** — the model responds, grounded in what you retrieved.

That's it. RAG is not a model; it's this pipeline wrapped around a model.

## Stage 1-2: embed and search

```python
q_vec = embeddings.create(model=EMBED_MODEL, input=user_question)
hits = collection.query(vector=q_vec, top_k=5)  # nearest chunks + scores
```

Reuse the exact embedding model from your ingestion step — same model, same space, or the distances mean nothing (lesson 1).

## Choosing top-k

**top-k** is how many chunks you pull back. It's a precision/recall dial:

- Too **small** (k=1–2) and you may miss the chunk that holds the answer.
- Too **large** (k=20) and you flood the prompt with weakly-related text — more tokens, more cost, and the real answer can get buried in noise.

A good starting band is **k = 3 to 8**. Start at 5, then adjust based on whether answers are complete (raise k) or unfocused (lower k). Later you'll add **reranking** (next lesson) so you can retrieve a generous k and then keep only the best few.

## Stage 3: assemble the context

Don't just concatenate raw text. Give each chunk a clear boundary and an id so the model — and later your citation code — can tell them apart. Claude responds very well to **XML-style tags**:

```python
context = "\n".join(
    f'<doc id="{h.id}" source="{h.metadata["source"]}">\n{h.text}\n</doc>'
    for h in hits
)
```

Keep the block within a sensible token budget. If your chunks are large or k is high, you may trim or summarise — but never silently drop the chunk that actually answers the question.

## Stage 4: prompt the model

Now the Messages API call. The **system** prompt sets the rules; the **user** turn carries the context and question.

```python
import anthropic
client = anthropic.Anthropic()

resp = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    system=(
        "You are a support assistant. Answer ONLY using the context in <doc> tags. "
        "If the answer is not in the context, say you don't have that information. "
        "Cite the source id for each claim."
    ),
    messages=[{
        "role": "user",
        "content": f"<context>\n{context}\n</context>\n\nQuestion: {user_question}",
    }],
)
print(resp.content[0].text)
```

The same shape runs on **Amazon Bedrock** and **Azure** with their respective Claude endpoints — only the client construction changes.

## When retrieval finds nothing

Grounding has a sharp edge: **no context, no claim.** If the top scores are all low, or the database returns nothing, don't send a half-empty prompt and hope. Detect it and let the model say "I don't have that information." A truthful "I don't know" beats a confident hallucination every time — exactly the reliability mindset you bring from operations.

## Your task

Using the vector store from last lesson, write a single function `answer(question)` that does all five stages and returns Claude's grounded response. Test it with a question your corpus *can* answer and one it *cannot*, and confirm the second returns an honest "I don't have that information."
