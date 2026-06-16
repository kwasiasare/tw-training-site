---
course: kwasi-GenAI
title: Reranking retrieved results
month: 2
monthTitle: Retrieval-Augmented Generation (RAG)
lesson: 5
summary: 'Improve relevance with a second pass: retrieve a generous candidate set with fast vector search,
  then rerank it with a cross-encoder so the truly best chunks rise to the top.'
objectives:
- Explain why first-pass vector search alone often misranks results
- Contrast a bi-encoder (vector search) with a cross-encoder (reranker)
- Describe the retrieve-then-rerank two-stage pattern
- Choose a candidate size and final top-n for reranking
- Call a reranker API and reorder chunks by relevance score
- Weigh reranking's latency and cost against its accuracy gains
video: g2-l05-reranking.mp4
quiz:
- q: Why is first-pass vector search not always enough?
  options:
  - It is too slow
  - Embeddings are computed independently, so the closest vectors aren't always the most relevant to the
    exact query
  - It cannot store metadata
  - It only works in English
  answer: 1
  why: A bi-encoder embeds query and document separately and approximately, so nuance and exact intent
    can be lost; the nearest vectors aren't always the best answers.
- q: How does a cross-encoder reranker differ from vector search?
  options:
  - It is the same thing
  - It reads the query and a document together and scores their relevance directly
  - It only counts shared keywords
  - It embeds faster
  answer: 1
  why: A cross-encoder takes the query and each candidate as a pair and judges relevance jointly, which
    is more accurate but too slow to run over the whole corpus.
- q: What is the standard two-stage retrieval pattern?
  options:
  - Rerank everything, then embed
  - Retrieve many candidates fast with vectors, then rerank the few best with a cross-encoder
  - Fine-tune, then retrieve
  - Query the model twice
  answer: 1
  why: Vector search cheaply narrows millions to a few dozen candidates; the expensive cross-encoder then
    reorders just those, giving accuracy at acceptable cost.
- q: Why not run the cross-encoder over the entire corpus directly?
  options:
  - It would be more accurate but is far too slow and expensive at scale
  - It is less accurate
  - It cannot read text
  - It needs no query
  answer: 0
  why: A cross-encoder must process each query-document pair, which is O(n) of expensive model calls —
    impractical over millions, hence the cheap first pass.
- q: In one sentence, what's a reasonable candidate count to send to the reranker?
  answer: Retrieve around 20-50 candidates from vector search, then rerank down to the top 3-5 for the
    prompt.
  why: A generous first pass maximises the chance the true answer is in the set; the reranker then keeps
    only the best few to control prompt size.
- q: What is the main cost of adding a reranker, and how do you justify it?
  answer: Extra latency and per-query cost; justified when retrieval quality directly drives answer accuracy
    and the gain outweighs the added milliseconds and spend.
  why: Reranking adds a model call per query, so you adopt it when the relevance improvement is worth
    the latency and cost on your workload.
resources:
- label: Cohere — Rerank documentation
  url: https://docs.cohere.com/docs/rerank-overview
- label: Pinecone — Rerankers and two-stage retrieval
  url: https://www.pinecone.io/learn/series/rag/rerankers/
- label: Sentence-Transformers — Cross-Encoders
  url: https://www.sbert.net/examples/applications/cross-encoder/README.html
- label: Azure AI Search — semantic ranking
  url: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview
- label: Hugging Face — MTEB reranking benchmarks
  url: https://huggingface.co/spaces/mteb/leaderboard
---

## The problem with a single pass

Your pipeline works: embed the query, pull the top-k, prompt the model. But you'll notice something — the *right* chunk is often retrieved, just not at rank 1. It might sit at position 6, below chunks that are merely *near* in vector space but don't actually answer the question. If you only feed the model the top 3, you miss it.

Why does this happen? Vector search uses a **bi-encoder**: it embeds the query and each document **separately and in advance**, then compares vectors. That's what makes it fast enough for millions of items — but the model never sees the query and document *together*. Subtle intent, negation, and exact-match nuance get smoothed away. The nearest vectors are a great *shortlist*, not a perfect *ranking*.

## Cross-encoders: read both together

A **cross-encoder** (a **reranker**) fixes the ranking. It takes the query and one candidate document **as a pair**, reads them jointly, and outputs a single relevance score. Because it attends to both texts at once, it judges "does this actually answer the question?" far more accurately than comparing two pre-computed vectors.

The catch: a cross-encoder must run once **per candidate**, so it's `O(n)` of expensive model calls. You could never run it over a million chunks per query. So you don't.

## The two-stage pattern

The industry-standard solution combines the strengths of both:

1. **Retrieve (bi-encoder, cheap):** vector search narrows millions of chunks down to a generous candidate set — say the top **20–50**.
2. **Rerank (cross-encoder, accurate):** the reranker scores just those candidates against the query and reorders them. You keep the final **top 3–5** for the prompt.

```python
# Stage 1: fast, generous recall
candidates = collection.query(vector=q_vec, top_k=40)

# Stage 2: accurate reordering
ranked = reranker.rerank(
    query=user_question,
    documents=[c.text for c in candidates],
    top_n=5,
)
context = assemble([candidates[r.index] for r in ranked])
```

A wide first pass maximises the chance the true answer is *somewhere* in the candidate set; the reranker's job is then just to float it to the top. This single change is often the biggest quality win in a RAG system.

## Picking the numbers

- **Candidate count (k):** 20–50 is a sweet spot. Higher recall, but more reranker work.
- **Final top-n:** 3–5 chunks into the prompt, same precision/recall thinking as before.

Managed rerankers (e.g. **Cohere Rerank**) are a single API call; **Azure AI Search** offers built-in **semantic ranking** in the cloud you already run; or you can self-host a sentence-transformers cross-encoder. Any of them slots in as stage two.

## What it costs you

Reranking adds **latency** (one extra model call) and **per-query cost**. That's the whole trade. Adopt it when retrieval quality directly drives answer accuracy — which, for most serious RAG, it does. Measure: compare answers with and without the reranker on real questions. If the right chunk now reliably reaches the model, the few extra milliseconds are easily worth it. If you're latency-bound, rerank a smaller candidate set or use a faster reranker.

## Your task

Take the `answer(question)` function from last lesson. Widen the first-pass retrieval to top-k = 30, add a reranker as stage two, and keep the top 5. Pick a question where the old top-3 missed the answer and confirm the reranked top-5 now includes the correct chunk.
