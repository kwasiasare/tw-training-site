---
course: kwasi-GenAI
title: Citation, grounding & the RAG deliverable
month: 2
monthTitle: Retrieval-Augmented Generation (RAG)
lesson: 7
summary: Make answers trustworthy by grounding them in retrieved context and citing sources, then assemble
  everything from the module into a working RAG system over a real document corpus.
objectives:
- Define grounding and explain why it reduces hallucination
- Instruct the model to cite the source of each claim and to refuse when context is missing
- Carry chunk ids and metadata through the pipeline so citations are verifiable
- Assemble the full ingest-and-query RAG system from the module's pieces
- Evaluate the system on real questions, including ones it should refuse
- 'Ship the Module 2 deliverable: a RAG system over a real corpus, with citations'
video: g2-l07-citation-grounding-and-deliverable.mp4
quiz:
- q: What does it mean to 'ground' an answer?
  options:
  - Make it shorter
  - Base every claim on the retrieved context rather than the model's memory
  - Translate it
  - Run it through a reranker
  answer: 1
  why: Grounding means the answer is built from the supplied context, so claims are tied to retrieved
    sources rather than the model's parametric guesswork.
- q: How do you get reliable citations from the model?
  options:
  - Hope it adds them
  - Pass each chunk with an id and instruct the model to cite that id for each claim
  - Fine-tune for citations
  - Use a bigger model only
  answer: 1
  why: Carrying a stable id with each chunk and instructing the model to reference it lets every claim
    point back to a verifiable source.
- q: What should a well-grounded system do when the context lacks the answer?
  options:
  - Guess confidently
  - Say it doesn't have the information instead of inventing one
  - Return random chunks
  - Crash
  answer: 1
  why: Refusing when the context is insufficient is the heart of grounding; an honest non-answer beats
    a fabricated one.
- q: Why are verifiable citations especially valuable to a security/compliance engineer?
  options:
  - They look nice
  - They let you audit and prove why the system gave an answer
  - They speed up retrieval
  - They reduce token cost
  answer: 1
  why: Citations create an audit trail, so you can show the source behind every claim — essential for
    trust, compliance, and debugging.
- q: In one sentence, why might an answer still be wrong even though it cites a source?
  answer: The cited chunk could be retrieved but irrelevant or misread, so you must check the citation
    actually supports the claim.
  why: Citation links a claim to a source, but only verifying the source confirms the claim; reranking
    and evaluation reduce, not eliminate, this risk.
- q: List the end-to-end stages of the RAG system you build as the deliverable.
  answer: Ingest (load, chunk, embed, upsert), then query (embed question, search, rerank, assemble cited
    context, prompt Claude, return grounded answer with citations).
  why: 'The deliverable joins every module lesson: chunking, embeddings, vector DB, retrieval, reranking,
    and grounded, cited generation.'
resources:
- label: Anthropic docs — Citations
  url: https://docs.anthropic.com/en/docs/build-with-claude/citations
- label: Anthropic docs — Reduce hallucinations
  url: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- label: Anthropic docs — Messages API reference
  url: https://docs.anthropic.com/en/api/messages
- label: Anthropic — Contextual Retrieval
  url: https://www.anthropic.com/news/contextual-retrieval
- label: AWS — Retrieval Augmented Generation (RAG)
  url: https://aws.amazon.com/what-is/retrieval-augmented-generation/
---

## Grounding: the answer must come from the context

A RAG system that retrieves the right chunks can still hallucinate if the model falls back on its own memory. **Grounding** is the discipline of forcing every claim to come from the **retrieved context**, not the model's parametric guesswork. You enforce it with the system prompt: answer *only* from the provided context, and if the answer isn't there, **say so**. That single instruction, plus good retrieval, is what turns a chatty model into a trustworthy assistant.

Grounding and refusal are two sides of one coin. The willingness to say "I don't have that information" is not a weakness — it's the feature. As an operations engineer you already prize systems that fail loudly and honestly over ones that guess.

## Citations: make every claim checkable

Grounding tells the model *where* to look; **citations** let *you* verify it looked there. Carry a stable **id** (and source/page metadata) with every chunk all the way through the pipeline, then instruct the model to cite the id behind each claim. Now each sentence points back to a retrievable source the user can open.

```python
system = (
    "Answer ONLY from the <doc> blocks. After each claim, cite its id like [doc-id]. "
    "If the context does not contain the answer, say you don't have that information."
)
```

The Claude API also offers a built-in **Citations** feature that returns structured references to the exact passages used — worth adopting for production. Either way, remember: a citation links a claim to a source, but only *checking* the source confirms the claim. Reranking and evaluation reduce bad citations; they don't abolish the need to verify.

## The Module 2 deliverable: a working RAG system

Everything you've built now assembles into one system over a **real document corpus** (your team's docs, a product manual, a set of policies — anything you can legally use). It has two halves.

### Ingest (run once, re-run when docs change)

```python
# 1. LOAD your corpus (PDFs, Markdown, HTML)
docs = load_corpus("./corpus")

# 2. CHUNK structure-aware, with overlap  (lesson 2)
chunks = structure_aware_chunks(docs, size=800, overlap=120)

# 3. EMBED each chunk  (lesson 1)
vectors = [embeddings.create(model=EMBED_MODEL, input=c.text) for c in chunks]

# 4. UPSERT into the vector store with metadata  (lesson 3)
for c, v in zip(chunks, vectors):
    store.upsert(id=c.id, vector=v, metadata={"source": c.source, "page": c.page})
```

### Query (per question)

```python
import anthropic
client = anthropic.Anthropic()

def answer(question: str) -> str:
    q = embeddings.create(model=EMBED_MODEL, input=question)        # embed  (l4)
    candidates = store.query(vector=q, top_k=30)                    # search (l3)
    top = reranker.rerank(question, candidates, top_n=5)            # rerank (l5)
    context = "\n".join(
        f'<doc id="{c.id}" source="{c.source}">\n{c.text}\n</doc>' for c in top
    )                                                              # assemble (l4)
    resp = client.messages.create(                                 # ground + cite (l7)
        model="claude-opus-4-8",
        max_tokens=1024,
        system=(
            "Answer ONLY from the <doc> blocks. Cite each claim's id like [id]. "
            "If the answer isn't in the context, say you don't have that information."
        ),
        messages=[{"role": "user",
                   "content": f"<context>\n{context}\n</context>\n\nQuestion: {question}"}],
    )
    return resp.content[0].text
```

That's the whole module in two code blocks. The same pattern runs on **Amazon Bedrock** or **Azure** with their Claude endpoints — only the client setup changes.

## Evaluate before you call it done

Don't ship on vibes. Write a small set of test questions: several the corpus **can** answer (check the answer is correct *and* cites the right source) and a few it **cannot** (check the system refuses instead of inventing). This tiny eval set is your regression guard — re-run it whenever you change chunk size, top-k, the reranker, or the prompt. It's the same instinct as a CI test suite, applied to an AI system.

## Your task — Module 2 deliverable

Build and ship the full system over a real corpus you choose. Ingest it, then answer at least five questions: show correct, **cited** answers for in-corpus questions and an honest refusal for an out-of-corpus question. Keep your eval questions in the repo. This RAG system is your Module 2 deliverable and a strong portfolio piece — you can demo it in interviews.
