---
course: agentic-ai-engineer
title: Short-Term and Long-Term Memory for Agents
month: 2
monthTitle: Reasoning, Memory, and Retrieval
lesson: 2
summary: Agents need memory to be useful beyond a single turn. This lesson teaches you to build short-term
  conversational buffers that keep dialogue coherent within a session, and long-term, vector-backed memory
  that lets an agent recall facts across sessions. You'll learn windowing and summarization strategies
  to control context-window cost, how to embed and retrieve relevant memories, and how to combine both
  layers in a production agent.
objectives:
- Distinguish short-term (working) memory from long-term (persistent) memory and explain when each is
  needed
- Implement a conversational buffer with windowing and summarization to manage token budgets
- Build vector-backed long-term memory using embeddings and a vector store for semantic recall
- Design a write/read policy that decides what to persist and how to retrieve it at query time
- Combine short-term and long-term memory into a single agent loop with relevance and recency filtering
- 'Identify production concerns: cost, privacy, staleness, and memory eviction'
video: age-m2-l02-short-term-and-long-term-memory-for-agents.mp4
quiz:
- q: What is the main reason an LLM agent needs explicit memory management?
  options:
  - LLMs forget their training data over time
  - Each API call is stateless and only sees what's in the prompt
  - Vector databases require it
  - Embeddings expire after each session
  answer: 1
  why: LLM calls are stateless; the model only knows what's in the current prompt, so the agent must feed
    prior context back in explicitly.
- q: Which short-term memory strategy best balances bounded token cost with preserving older context?
  options:
  - Replaying the full history every turn
  - Buffer window only (last N turns)
  - Hybrid summary plus window
  - Storing everything in a vector database
  answer: 2
  why: The summary-plus-window hybrid compresses old turns into a running summary while keeping recent
    turns verbatim, bounding cost without fully losing older context.
- q: In the embed-and-retrieve pattern for long-term memory, what happens at read time?
  options:
  - Every stored memory is added to the prompt
  - The query is embedded and a similarity search returns top-k memories
  - The summary is regenerated from scratch
  - The model fine-tunes on stored memories
  answer: 1
  why: At read time you embed the current query and run a similarity search, injecting only the top-k
    most relevant memories into the prompt.
- q: Why should you avoid writing every conversation message into long-term memory?
  options:
  - Vector stores cannot hold conversational text
  - It pollutes retrieval with low-value filler, hurting relevance
  - Embeddings only work on facts
  - It violates the context window limit
  answer: 1
  why: Storing filler degrades retrieval quality; a write policy that extracts only durable facts keeps
    long-term recall relevant.
- q: Name two factors beyond raw semantic relevance that should influence which long-term memories are
    retrieved.
  answer: Recency and importance
  why: A combined score weights relevance, recency (prefer newer facts), and importance (salience), e.g.
    score = α·relevance + β·recency + γ·importance.
- q: Give one production concern specific to storing user memories and a way to address it.
  answer: 'Privacy/PII—use per-user namespaces, support deletion, and encrypt sensitive data (other valid
    answers: cost capping, staleness via timestamps, eviction by age/importance).'
  why: Memory often holds personal data, so namespacing, deletion support, and encryption address privacy
    and compliance; cost, staleness, and eviction are other valid concerns.
resources:
- label: LangChain Memory documentation
  url: https://python.langchain.com/docs/how_to/chatbots_memory/
- label: 'Generative Agents: Interactive Simulacra of Human Behavior (memory retrieval scoring)'
  url: https://arxiv.org/abs/2304.03442
- label: Qdrant vector database documentation
  url: https://qdrant.tech/documentation/
- label: 'MemGPT: Towards LLMs as Operating Systems (long-term memory paging)'
  url: https://arxiv.org/abs/2310.08560
---

## Why Agents Need Memory

A raw LLM is stateless: each API call only knows what's in the prompt. To behave like an assistant that 'remembers,' an agent must explicitly feed prior context back into the model. We split this into two layers:

- **Short-term memory (working memory):** the current conversation, held for the duration of a session. Cheap to access, lives in the context window.
- **Long-term memory (persistent memory):** facts, preferences, and past interactions stored outside the model—typically in a vector database—and retrieved on demand across sessions.

## Short-Term Memory

The simplest form is a **buffer**: append every user and assistant message to a list and replay it each turn. This breaks down because context windows and cost are finite. Three common strategies:

1. **Buffer window** — keep only the last *N* turns. Simple, predictable token cost, but loses older context.
2. **Token-budget buffer** — keep as many recent messages as fit under a token cap.
3. **Summary memory** — periodically compress older turns into a running summary, then keep recent turns verbatim. Preserves gist while bounding tokens.

A hybrid—**summary + window**—is the production default: a rolling summary of old turns plus the last few raw turns.

```python
class SummaryWindowMemory:
    def __init__(self, llm, window=6):
        self.llm = llm
        self.window = window
        self.summary = ""
        self.recent = []

    def add(self, role, content):
        self.recent.append({"role": role, "content": content})
        if len(self.recent) > self.window:
            old = self.recent[:-self.window]
            self.recent = self.recent[-self.window:]
            self.summary = self.llm.summarize(self.summary, old)

    def context(self):
        msgs = []
        if self.summary:
            msgs.append({"role": "system", "content": f"Summary so far: {self.summary}"})
        return msgs + self.recent
```

## Long-Term Memory with Vectors

Long-term memory persists beyond the session. The standard pattern is **embed-and-retrieve**:

1. **Write:** when something worth remembering occurs (a stated preference, a fact, a resolved task), embed the text and store the vector plus metadata in a vector store.
2. **Read:** at each turn, embed the current query, run a similarity search, and inject the top-k relevant memories into the prompt.

```python
def remember(store, embed, text, meta):
    vec = embed(text)
    store.upsert(id=uuid(), vector=vec, payload={"text": text, **meta})

def recall(store, embed, query, k=4):
    hits = store.search(embed(query), top_k=k)
    return [h.payload["text"] for h in hits]
```

### What to store
Don't dump every message into long-term memory—it pollutes retrieval. Use a **write policy**: store distilled facts, user preferences, decisions, and entities, not filler. Often you run a small extraction step ("Does this turn contain a durable fact? If so, summarize it.").

### Retrieval quality
- **Relevance:** cosine similarity over embeddings.
- **Recency:** bias toward newer memories with a time-decay score.
- **Importance:** optionally score and weight salient memories (the approach used in generative-agent research).

A common combined score: `score = α·relevance + β·recency + γ·importance`.

## Combining Both Layers

The agent loop on each turn:

1. Take the user input.
2. **Recall** top-k long-term memories relevant to the input.
3. Build the prompt: system instructions + retrieved memories + short-term context (summary + recent turns) + user input.
4. Call the LLM, return the answer.
5. **Write** new durable facts to long-term memory and append the turn to short-term memory.

```python
def agent_turn(user_input):
    memories = recall(store, embed, user_input, k=4)
    prompt = build_prompt(system, memories, stm.context(), user_input)
    answer = llm.chat(prompt)
    stm.add("user", user_input)
    stm.add("assistant", answer)
    facts = extract_facts(user_input, answer)
    for f in facts:
        remember(store, embed, f, {"ts": now(), "user": user_id})
    return answer
```

## Production Concerns

- **Token/cost control:** retrieval and summarization both add tokens—measure and cap them.
- **Privacy & compliance:** memory may hold PII. Support per-user namespaces, deletion (right-to-be-forgotten), and encryption.
- **Staleness & conflicts:** preferences change. Store timestamps, prefer recent, and consider updating rather than appending.
- **Eviction:** cap memory size; evict by age or low importance to keep retrieval sharp.
- **Namespacing:** isolate memories per user/tenant to prevent leakage across users.
