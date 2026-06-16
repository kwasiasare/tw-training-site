---
course: kwasi-GenAI
title: State and memory across steps
month: 3
monthTitle: Agents & Orchestration
lesson: 6
summary: 'Manage what an agent remembers: the short-term scratchpad inside one run versus longer-term
  memory that persists across runs, and how state actually flows between turns.'
objectives:
- Explain why the Messages API is stateless and what that implies for memory
- Distinguish the short-term scratchpad from longer-term persistent memory
- Describe how state is passed between turns by re-sending the message history
- Use the memory tool or an external store to persist facts across sessions
- Decide what belongs in the transcript, in a memory file, or in a database
- Keep memory lean so it helps rather than causing context bloat
video: g3-l06-state-memory.mp4
quiz:
- q: Because the Messages API is stateless, how does an agent 'remember' earlier steps within one run?
  options:
  - The server stores the session for you
  - You re-send the full message history on every call
  - The model has built-in long-term memory
  - Memory is automatic once you set a flag
  answer: 1
  why: The API holds no session; the conversation persists only because your code re-sends the accumulated
    messages list each turn.
- q: What is the short-term scratchpad?
  options:
  - A database of user profiles
  - The growing message history (and thinking) within a single run that holds the agent's working state
  - A cache of model weights
  - The system prompt
  answer: 1
  why: The scratchpad is the in-run working memory — the accumulating messages and reasoning that carry
    state from one step to the next within a single task.
- q: What distinguishes longer-term memory from the scratchpad?
  options:
  - It is faster
  - It persists across separate runs or sessions, stored outside the transcript
  - It uses a different model
  - It cannot be edited
  answer: 1
  why: Longer-term memory survives beyond one run — saved to a file or store — so a later session can
    recall facts the scratchpad would have lost.
- q: In one sentence, how does the memory tool let an agent persist information?
  answer: Claude reads and writes files in a memory directory that you back with storage, so notes survive
    across sessions.
  why: The memory tool exposes file operations on a /memories directory; your backend stores them, giving
    the agent durable cross-session memory.
- q: Why should you NOT pour everything into long-term memory?
  answer: Memory that is loaded into context still costs tokens and can bury the relevant signal, so unbounded
    memory just recreates context bloat.
  why: Memory is only useful if it is selective; storing and re-loading everything reintroduces the cost
    and noise problems of bloat.
- q: Where should a user's durable preference (e.g. preferred language) live?
  answer: In longer-term persistent memory — a memory file or database keyed to the user — not only in
    the current run's scratchpad.
  why: A durable preference must survive across sessions, so it belongs in persistent storage, not the
    transient in-run transcript.
resources:
- label: Claude Docs — Memory tool
  url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- label: Claude Docs — Context editing
  url: https://platform.claude.com/docs/en/build-with-claude/context-editing
- label: Claude Docs — Compaction
  url: https://platform.claude.com/docs/en/build-with-claude/compaction
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
---

## The API has no memory — you do

Start from the fact that surprised everyone in the failure-modes lesson: the Messages API is **stateless**. The server does not remember your conversation. Send the same single message twice and you get two independent answers — there's no session on the other end. So when an agent appears to "remember" what it did three steps ago, that's not the API; it's *your code* re-sending the accumulated history. Memory is something you build, not something you switch on.

There are two layers of it, and keeping them separate is the whole lesson.

## Short-term: the scratchpad

The **scratchpad** is the agent's working memory *within a single run*: the growing `messages` list — user turns, assistant turns, tool calls, tool results — plus the model's thinking. As the loop turns, each step's output becomes context for the next. That's how the agent "knows" it already looked up the customer id two iterations ago: the id is sitting in the transcript you keep re-sending.

```python
messages = [{"role": "user", "content": task}]
# Each loop iteration APPENDS to messages, then re-sends the whole list:
#   messages.append(assistant_turn)      # what Claude said / called
#   messages.append(tool_results_turn)   # what the tools returned
# The accumulated list IS the short-term memory.
```

The scratchpad is automatic and powerful — but it's also exactly what causes context bloat. It lives and dies with the run; when the run ends, the scratchpad is gone.

## Longer-term: persistent memory

Some facts must outlive a single run: a user's preferred language, a project's coding standard, what an overnight agent learned yesterday. That's **longer-term memory** — state stored *outside* the transcript so a future session can recall it.

Anthropic provides a **memory tool** for this: Claude can `view`, `create`, `str_replace`, and `delete` files in a `/memories` directory, and *you* implement the storage backend (a folder, an object store, a database). The agent jots a note now and reads it back in a future session. You can equally roll your own: a function tool that writes to a database keyed by user id. Either way the principle is identical — durable facts live in storage you control, and the agent loads only what's relevant into context when it needs it.

```python
# The memory tool surfaces file ops to the model; your backend stores them.
response = client.messages.create(
    model="claude-opus-4-8", max_tokens=1024,
    messages=[{"role": "user", "content": "Remember my stack is Python and Terraform."}],
    tools=[{"type": "memory_20250818", "name": "memory"}],
)
```

## Passing state between turns and sessions

Put the two layers together and the data flow is clear. **Within a run**, state passes between turns by appending to `messages` and re-sending. **Across runs**, state passes by writing to persistent memory at the end of one session and reading it back at the start of the next. A long-running agent does both: it works in the scratchpad, and periodically *promotes* a durable learning into long-term memory so it isn't lost when the scratchpad is pruned or the run ends.

For a DevOps engineer, the analogy is tidy: the scratchpad is the ephemeral state inside a single pipeline run; long-term memory is the artifact store or state file that the next run reads.

## Keep memory lean

Memory only helps if it's **selective**. Anything loaded into context still costs tokens and still competes for the model's attention — so dumping everything into long-term memory just recreates context bloat one session later. Store the durable, reusable facts; let the scratchpad handle the transient ones; and combine memory with the context editing and compaction from last lesson so the working window stays focused. Good memory is a small set of high-value notes, not a transcript dump.

## Your task

For your weather agent, list three pieces of state and classify each: scratchpad (in-run only), or long-term memory (persists across sessions). Then write one sentence describing exactly when the agent would *write* a fact to long-term memory and when it would *read* it back.
