---
course: agentic-ai-engineer
title: Building Your Agentic AI Portfolio
month: 5
monthTitle: Capstone & Career Launch
lesson: 2
summary: 'One capstone proves you can ship; a small portfolio proves it was not a fluke. This lesson helps
  you assemble two to three focused agentic projects that span the breadth employers look for: a tool-using
  agent, a RAG agent, and a multi-agent orchestration paired with an MCP server you built. For each you
  will produce the same package — a clean repo, an architecture diagram, a short demo, a design doc, and
  eval results — and tie them together under one coherent story. Because agentic AI is a portfolio-led
  role with no dominant certification, this collection of working systems is the credential that actually
  moves hiring decisions.'
objectives:
- Plan a portfolio of 2-3 complementary agentic projects that show range without overlapping
- Build a tool-using agent, a RAG agent, and a multi-agent orchestration with an MCP server
- 'Produce a consistent package per project: repo, diagram, demo, design doc, and eval results'
- Write READMEs that lead with the problem, architecture, and quantified outcomes
- Frame all projects under one narrative that signals an agentic AI engineer
- 'Avoid common portfolio anti-patterns: tutorial clones, no evaluation, and dead demos'
video: age-m5-l02-building-your-agentic-ai-portfolio.mp4
quiz:
- q: Why build a small portfolio of distinct projects instead of one large monolithic app?
  options:
  - More repos always rank higher in search
  - Distinct projects show range — tool use, retrieval, orchestration — and prove your first success was
    repeatable
  - A monolith cannot be deployed
  - Employers only count the number of files
  answer: 1
  why: Two or three focused projects demonstrate breadth across the core agentic skills and show that
    you can repeat a good outcome. A single monolith hides which skills are yours and looks like one lucky
    build.
- q: What is the strongest reason to include an MCP server you built in your portfolio?
  options:
  - It is the only way to call an LLM
  - It shows you can expose tools and data to agents through an open, interoperable standard — a current,
    in-demand skill
  - It removes the need for any evaluation
  - It makes your agent run without any model
  answer: 1
  why: The Model Context Protocol is an open standard for connecting agents to tools and data sources.
    Building an MCP server demonstrates a modern integration skill employers are actively hiring for and
    shows you understand interoperable tool exposure, not just one framework's plugins.
- q: Which set of projects best demonstrates agentic breadth?
  options:
  - Three near-identical chatbots over different documents
  - A tool-using agent, a RAG agent, and a multi-agent orchestration with an MCP server
  - Three Jupyter notebooks with no runnable entry point
  - One project copied from a tutorial, three times
  answer: 1
  why: A tool-using agent, a RAG agent, and a multi-agent orchestration plus an MCP server cover the core
    competencies — function calling, retrieval grounding, coordination, and interoperable tool exposure
    — without redundancy. The other options show one skill or none.
- q: What should every project README lead with?
  options:
  - A long list of every library version installed
  - The problem it solves, the architecture, and quantified outcomes — with setup and limitations following
  - An apology that it is just a learning project
  - The author's full life story
  answer: 1
  why: Reviewers skim. Leading with the problem, the architecture, and measurable outcomes lets someone
    grasp the value in seconds, then drill into setup and limitations. Burying the point under dependency
    lists or apologies wastes the attention you have.
- q: Which is a portfolio anti-pattern to avoid?
  options:
  - A README with an architecture diagram and eval numbers
  - A short demo video showing the agent working end to end
  - An unmodified tutorial clone with no evaluation and a demo link that no longer works
  - A design doc that states trade-offs and limitations
  answer: 2
  why: Tutorial clones show no original thinking, missing evaluation means you cannot prove the system
    works, and a dead demo link erodes trust instantly. The other choices are exactly the signals that
    make a portfolio credible.
- q: In two to four sentences, describe the single narrative you would use to tie a tool-using agent,
    a RAG agent, and a multi-agent + MCP project into one coherent portfolio.
  answer: 'I would frame all three as one story: I design, evaluate, and ship LLM agents that take real
    actions, ground their answers in trusted data, and coordinate to solve multi-step tasks. The tool-using
    agent shows safe function calling and action-taking, the RAG agent shows retrieval grounding with
    citations and faithfulness evaluation, and the multi-agent project with an MCP server shows orchestration
    and interoperable tool exposure. Each repo carries the same package — diagram, demo, design doc, and
    eval results — so the collection reads as one engineer''s consistent practice rather than three unrelated
    experiments. That single line on my profile turns three projects into a clear claim about what I build.'
  why: A strong answer states one positioning line, maps each project to a distinct competency (action-taking,
    grounding, orchestration/interoperability), and notes the consistent packaging that makes the set
    read as one coherent body of work.
resources:
- label: Model Context Protocol (MCP) — build a server
  url: https://modelcontextprotocol.io
- label: LangGraph documentation (multi-agent orchestration)
  url: https://langchain-ai.github.io/langgraph/
- label: LangChain RAG tutorial
  url: https://python.langchain.com/docs/tutorials/rag/
- label: GitHub Pages (host portfolio pages and demos)
  url: https://pages.github.com/
---

## Why a Portfolio, Not Just a Capstone

Your capstone proves you can ship one sophisticated system. A small portfolio proves that success was deliberate and repeatable, and it shows **range** — the breadth of agentic skills a team actually needs. This matters more in agentic AI than in most fields, because the role is **emerging and portfolio-led**: there is no single dominant certification a recruiter screens for. Instead, hiring managers look at what you have built and whether you can defend it. Two or three focused, well-packaged projects are the credential that moves a hiring decision.

The goal is not volume. Three near-identical chatbots add nothing. You want a small set of **complementary** projects, each demonstrating a distinct core competency, each held to the same quality bar you set in your capstone.

## The Three-Project Spread

Aim for two to three projects that together cover the agentic skill map without overlap.

### 1. A tool-using agent
A single agent that takes real actions through **function calling** — querying an API, running code, writing to a system. This project shows you understand the agent loop: the model proposes a tool call, your code executes it, the result returns to the model, and the loop continues until a stop condition. Emphasize **safe tool design**: validated arguments, structured outputs, bounded steps, and graceful handling of tool errors. A good example is an agent that turns natural-language requests into validated API calls and confirms the result.

### 2. A RAG agent
An agent grounded in a real document corpus. This is where you show **retrieval** done well: sensible chunking, embeddings, top-k retrieval with metadata filters or reranking, and — non-negotiable — **citations** in every answer so faithfulness is measurable. The differentiator from a basic RAG demo is evaluation: report retrieval recall, faithfulness, and answer quality on a small test set. A RAG agent over a domain you understand (a product's docs, a research area) reads as genuinely useful.

### 3. A multi-agent orchestration with an MCP server
Your most ambitious piece (this can be your capstone, repackaged). A **LangGraph** orchestration of specialized agents, plus an **MCP server you built** to expose a tool or data source. The Model Context Protocol is an open, interoperable standard for connecting agents to tools and data, and building a server signals a modern, in-demand integration skill rather than lock-in to one framework's plugin format. Show the coordination topology, the agents' contracts, and how the MCP server is consumed. A nice touch is to make the same MCP server usable from more than one client, which proves the value of building to a shared standard rather than a one-off integration.

If you only have time for two projects, drop one and keep the RAG agent and the multi-agent-plus-MCP piece, since together they still demonstrate grounding, orchestration, and interoperability. Quality per project always beats quantity: a reviewer who opens one polished, evaluated repo is more persuaded than by five thin ones.

Together these three cover **action-taking, grounding, orchestration, and interoperability** — exactly the competencies a job description for an agentic role lists.

## One Consistent Package Per Project

Consistency is itself a signal of professionalism. Give every project the same five artifacts:

- **A clean repo.** Readable code, pinned dependencies, secrets via environment variables, and a sensible structure. The repo is the thing reviewers actually open.
- **An architecture diagram.** One clear diagram of the agent loop, the RAG pipeline, or the orchestration graph. It is the first thing anyone looks at.
- **A short demo.** Two to four minutes (a Loom or GIF) showing the system working end to end. Recruiters and engineers watch these; a dead or missing demo is a wasted opportunity.
- **A design doc.** One page: the problem, the design and why, the trade-offs and alternatives you rejected, and known limitations. This is what separates an engineer from a tutorial follower.
- **Eval results.** Even a small harness with a handful of metrics — task success rate, tool-call accuracy, faithfulness, latency, cost — turns claims into evidence. Almost no junior portfolio has this, so it sets you apart immediately.

## Write READMEs That Respect Attention

Reviewers skim in seconds. Lead the README with the **problem**, the **architecture diagram**, and the **quantified outcomes**, then follow with setup, usage, and limitations. A reader should understand what the project does and that it works before they scroll. Replace "this was a learning project" with a confident statement of what it does and what you measured. Numbers carry credibility: "answers grounded with citations at 91% faithfulness on a 30-question eval set" says more than a paragraph of adjectives.

Pin your best repositories on your GitHub profile and write a profile README that frames the collection. You can also publish a simple portfolio page (GitHub Pages works well) that links each project's repo, diagram, and demo under one story.

## Tie It Together With One Story

Do not present three unrelated experiments. Frame the whole collection with a single positioning line, for example: *I design, evaluate, and ship LLM agents that take real actions, ground their answers in trusted data, and coordinate to solve multi-step tasks.* Then each project becomes a proof point for part of that claim — the tool-using agent for action-taking, the RAG agent for grounding, the multi-agent and MCP project for orchestration and interoperability. Because every repo carries the same package, the set reads as one engineer's consistent practice. That coherence is what turns a list of links into a credential.

## How a Reviewer Will Read It

It helps to picture the thirty seconds a reviewer actually spends. They land on your profile or resume, click one repo, and skim the README top to bottom. In that window they are asking three silent questions: *Does this person understand a real problem? Did they build something that works? Can they prove it?* A clean diagram answers the first, a runnable repo and demo answer the second, and your eval numbers answer the third. If any of those is missing, the reviewer fills the gap with doubt and moves on. This is why the **consistent package matters more than any single clever feature**: the package is engineered to answer all three questions fast, for every project, so a skim turns into a screen rather than a bounce. Optimize your portfolio for that skim, not for the one reviewer in fifty who reads every line.

## Anti-Patterns to Avoid

- **Tutorial clones.** An unmodified copy of a popular walkthrough shows no original thinking. If you start from a tutorial, change the problem, add evaluation, and make it yours.
- **No evaluation.** Without metrics you cannot prove anything works, and you forfeit your biggest differentiator.
- **Dead demos.** A broken deploy link or a video that 404s erodes trust instantly. Check your links, and prefer a stable recording over a fragile live URL.
- **Secret leaks.** Never commit API keys. A leaked key in git history is both a security failure and a credibility hit.
- **Over-scoping.** Three polished small projects beat one sprawling unfinished one. Ship, evaluate, document, then move on.

## The Deliverable

By the end of this lesson you should have a plan for two to three complementary projects, at least one already packaged to the full standard, and a profile that frames them under a single story. That collection — working systems, evaluated and documented — is the portfolio that, in a role with no dominant certification, does the job a certificate would: it proves you can do the work.
