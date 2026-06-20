---
course: ai-app-developer-2026
title: 'Capstone: Ship a Full-Stack AI Application'
month: 4
monthTitle: Deployment and Capstone Project
lesson: 4
summary: In this capstone lesson you'll combine everything you've learned—RAG pipelines, agents, and APIs—into
  a single deployed, portfolio-ready AI application. You'll architect the system, build a backend and
  frontend, deploy to a public URL, add observability and cost controls, and write documentation that
  makes your project demo-ready for recruiters and users.
objectives:
- Architect a full-stack AI application that integrates RAG, agent workflows, and external APIs into a
  coherent system
- Build and connect a backend (API + LLM logic) and a frontend (chat/UI) with streaming responses
- Deploy the application to a public cloud platform with environment-based secrets and a working demo
  URL
- Add observability, evaluation, and cost/rate-limit safeguards for production reliability
- Write portfolio-quality documentation including architecture diagrams, setup steps, and a demo walkthrough
video: aad-m4-l04-capstone-ship-a-full-stack-ai-application.mp4
quiz:
- q: Where should your LLM provider API keys live in a deployed full-stack AI app?
  options:
  - In the frontend JavaScript bundle
  - In a public environment file in the repo
  - Server-side as environment variables
  - Hardcoded in the React component
  answer: 2
  why: Keys must stay server-side as environment variables so the browser never exposes them and they
    aren't committed to the repository.
- q: What is the best scoping strategy for a capstone project?
  options:
  - Add as many features and tools as possible
  - One clear user, one job-to-be-done, one or two tools
  - Build a general-purpose assistant that does everything
  - Skip retrieval to save time
  answer: 1
  why: Tight scope—one user, one job, minimal tools—lets you finish something polished, which is more
    impressive than an unfinished ambitious app.
- q: Which technique makes a chat UI feel fast and modern during model responses?
  options:
  - Showing a static loading spinner until the full answer returns
  - Streaming tokens via Server-Sent Events
  - Polling the database every 10 seconds
  - Disabling the input until done
  answer: 1
  why: Streaming tokens as they're generated (e.g., via SSE) gives immediate visible feedback and the
    perception of speed.
- q: Which of these is NOT a production safeguard you should add before shipping?
  options:
  - Rate limiting per user or IP
  - Cost caps on max tokens
  - Committing API keys to the repo for convenience
  - Logging latency and token usage
  answer: 2
  why: Committing API keys is a security risk and the opposite of a safeguard; rate limiting, cost caps,
    and observability are all proper safeguards.
- q: Name one thing your capstone README must include to be portfolio-ready.
  answer: 'A live demo link (also acceptable: architecture diagram, setup steps, environment variables,
    or a demo video)'
  why: Portfolio-ready documentation needs a live demo link, an architecture diagram, the tech stack,
    setup steps with env vars, and ideally a short demo video—any of these is a valid answer.
- q: Why should you test your deployed app in an incognito window with no local state?
  answer: To confirm it works for a new user/stranger without relying on cached data, local secrets, or
    local setup
  why: An incognito test simulates a first-time visitor, ensuring the public demo truly works independently
    of your local environment.
resources:
- label: Vercel Deployment Documentation
  url: https://vercel.com/docs
- label: FastAPI Streaming Responses Guide
  url: https://fastapi.tiangolo.com/advanced/custom-response/
- label: LangSmith Observability for LLM Apps
  url: https://docs.smith.langchain.com/
- label: How to Write a Great Project README
  url: https://www.makeareadme.com/
---

## Capstone Overview

This is where the course comes together. You will ship a **full-stack AI application** that someone can click a link and use. The goal is not just to make it work locally, but to produce a **portfolio-ready** project: deployed, documented, and demonstrating the core skills of an AI Application Developer—RAG, agents, and API integration.

A strong capstone answers three questions for a viewer in under 60 seconds: *What does it do? How is it built? Can I try it right now?*

## Choosing a Scoped Project

Pick a project narrow enough to finish but rich enough to show depth. Good patterns:

- **Documentation assistant** — RAG over a docs corpus + an agent that can run code examples.
- **Research copilot** — agent that searches the web (API), summarizes, and cites sources stored via RAG.
- **Support triage bot** — classifies tickets, retrieves relevant KB articles, and drafts replies.

Scope rule: one clear user, one clear job-to-be-done, one or two agent tools. Resist feature creep.

## Reference Architecture

A clean separation of concerns keeps the app deployable and debuggable:

- **Frontend**: a chat or form UI (Next.js, React, or Streamlit) that streams responses.
- **Backend API**: FastAPI/Express endpoint that orchestrates the LLM, RAG retrieval, and agent tools.
- **Vector store**: managed (Pinecone, Supabase pgvector, Chroma Cloud) for retrieval.
- **LLM provider**: OpenAI/Anthropic/etc., accessed with a server-side key.
- **Agent layer**: tool-calling loop that decides when to retrieve, call APIs, or answer directly.

Keep all secrets server-side. The browser never sees your API keys.

## Backend: Orchestration

Your backend exposes a single `/chat` endpoint that:

1. Accepts a user message and conversation history.
2. Runs retrieval against the vector store when relevant.
3. Passes tools + context to the model in a tool-calling loop.
4. Streams tokens back to the client (Server-Sent Events).

Keep prompt templates, tool definitions, and retrieval logic in separate modules so they are testable.

## Frontend: The Demo Surface

The UI is what recruiters see first. Prioritize:

- Streaming output (feels fast and modern).
- Visible citations/sources from RAG to build trust.
- A clear empty state with example prompts.
- Graceful error handling when the API or model fails.

## Deployment

Deploy frontend and backend to a public platform:

- **Vercel/Netlify** for the frontend.
- **Render, Railway, Fly.io, or a serverless function** for the backend.
- Store secrets as **environment variables**, never in the repo.
- Add a **health-check** route and confirm CORS allows your frontend origin.

Tag a release and verify the public URL works in an incognito window with no local state.

## Production Safeguards

Before you call it done:

- **Rate limiting** per IP/user to prevent runaway cost.
- **Cost caps**: cap max tokens, use a cheaper model for routing.
- **Observability**: log prompts, latency, token usage (LangSmith, Helicone, or simple logging).
- **Evaluation**: a small test set of questions with expected behaviors you can re-run.
- **Guardrails**: input validation and a fallback message when retrieval returns nothing.

## Documentation and Demo

Your README should include: a one-line description, a live demo link, an architecture diagram, the tech stack, local setup steps, environment variables, and known limitations. Record a 60–90 second demo video (GIF or Loom). This documentation is often what gets you the interview.

## Shipping Checklist

- [ ] Public demo URL works without local setup
- [ ] RAG retrieves and cites sources
- [ ] At least one agent tool functions end-to-end
- [ ] Secrets are server-side env vars
- [ ] Rate limiting + cost cap in place
- [ ] README with diagram + demo video
- [ ] Repo is public and clean
