---
course: ai-app-developer-2026
title: Building Your AI Developer Portfolio
month: 5
monthTitle: Capstone & Career Launch
lesson: 2
summary: 'Hiring for AI application roles is portfolio-first: a reviewer decides in under a minute whether
  you can build, based on what they can see and click. This lesson turns two or three of your course apps
  — the RAG document Q&A chatbot, the autonomous research agent, and your production capstone — into hireable
  artifacts. For each project you will produce a clean public GitHub repo, a README that answers what/how/try-it,
  an architecture diagram, a live demo link, a short demo video, and a one-page design doc. Then you will
  frame all of them as a single narrative: ''I design, evaluate, and ship LLM-powered applications.''
  The output is a portfolio that converts a profile view into an interview.'
objectives:
- Select and package 2-3 course apps as self-contained case studies with consistent artifacts
- Write a README that answers what it does, how it is built, and how to try it in under a minute
- Produce a clear architecture diagram and a one-page design doc per project (problem, design, trade-offs,
  results)
- Publish a live demo link and a 60-90 second demo video for each project
- 'Make repos clean and credible: no secrets, an .env.example, a license, and meaningful commits'
- Frame all projects as one narrative that positions you for AI developer roles
video: aad-m5-l02-building-your-ai-developer-portfolio.mp4
quiz:
- q: A reviewer lands on your project README. What must it answer fastest?
  options:
  - What the app does, how it is built, and how to try it right now
  - Your full commit history and every dependency version
  - Your personal biography and career goals
  - A list of every prompt you experimented with
  answer: 0
  why: Portfolio reviewing is fast. A README that immediately answers what it does, how it is built, and
    'can I try it now' (a live link) lets a busy reviewer confirm capability in under a minute, which
    is what converts a click into an interview.
- q: What is the single most damaging thing to leave in a public portfolio repo?
  options:
  - A detailed architecture diagram
  - A committed API key or .env file with real secrets
  - A long, thorough README
  - An MIT license file
  answer: 1
  why: A leaked API key is a security incident and an instant credibility killer for an AI developer —
    it suggests you do not understand secret handling. Use environment variables and ship an .env.example
    with placeholders; the other items are positives.
- q: How should two or three projects relate to each other in a portfolio?
  options:
  - As unrelated one-offs with no connecting theme
  - As identical clones of the same tutorial
  - As one narrative — increasing depth across RAG, agents, and a shipped production app
  - Hidden until an interviewer specifically asks
  answer: 2
  why: A coherent story is more persuasive than scattered demos. Framing the RAG chatbot, the agent, and
    the production capstone as increasing depth — 'I design, evaluate, and ship LLM apps' — tells a hiring
    manager one clear thing about what you can do.
- q: Why include a one-page design doc per project, beyond the README?
  options:
  - To pad the repo with more files
  - 'To show engineering judgment: the problem, the design, the trade-offs you weighed, and measurable
    results'
  - Because READMEs cannot contain images
  - To replace the need for any code
  answer: 1
  why: A design doc demonstrates judgment, not just output. Stating the problem, the design, the alternatives
    you rejected and why, and quantified results is the clearest signal that you think like an engineer
    rather than a tutorial-follower.
- q: What makes a demo video effective for an AI app portfolio?
  options:
  - A 20-minute screen recording of you writing all the code
  - A voiceover with no visible application
  - A static screenshot with no motion
  - A 60-90 second clip showing the app doing its one job end to end, including a real result or citation
  answer: 3
  why: Reviewers watch short, focused clips. A 60-90 second video that shows the app performing its core
    job end to end — a question answered with a citation, a report generated — proves it actually works,
    which screenshots and long recordings do not.
- q: In three to five sentences, write the one-narrative positioning statement for a portfolio built on
    the RAG chatbot, the research agent, and the production capstone.
  answer: 'I am an AI application developer who designs, evaluates, and ships LLM-powered apps. My portfolio
    shows increasing depth: a RAG document Q&A chatbot that answers with citations grounded in a real
    corpus, an autonomous research agent that plans, calls web tools, and returns a structured cited report,
    and a production capstone deployed to a public URL with an evaluation suite, observability, rate limiting,
    and cost controls. Across all three I work the full path from prompt and retrieval design through
    tool calling to deployment and evaluation, with quantified results like faithfulness scores and latency.
    Each project links a clean GitHub repo, an architecture diagram, a live demo, and a short video. Together
    they say one thing: I can build and operate real AI applications, not just prototypes.'
  why: A strong statement opens with a positioning line, proves it with the three projects framed as increasing
    depth, names concrete skills (retrieval, tool calling, deployment, evaluation) and quantified results,
    and points to evidence — exactly the narrative that earns a screen.
resources:
- label: Make a README — structure and template for project READMEs
  url: https://www.makeareadme.com/
- label: 'GitHub Docs: About READMEs'
  url: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- label: diagrams.net (draw.io) — free architecture diagramming
  url: https://www.drawio.com/
- label: 'LinkedIn Help: Add and edit the Featured section'
  url: https://www.linkedin.com/help/linkedin/answer/a522537
---

## Why Portfolio-First Hiring Changes Your Job

For AI application roles in 2026, hiring is **portfolio-first**. There is no single mandatory certification, and a degree is rarely the deciding factor. What decides is whether a reviewer — a recruiter, then an engineer — can look at what you have built and believe you can do the work. That decision happens fast, often in under a minute, and it happens by **clicking**: opening a repo, skimming a README, watching a short video, trying a live link. Your job in this lesson is to make those artifacts so clear and credible that the click ends in 'let's talk.'

You already have the raw material. Across this course you built a RAG document Q&A chatbot, an autonomous research agent, and — in the previous lesson — a production capstone. This lesson turns **two or three** of them into polished, hireable artifacts and ties them into one story.

## Pick Two or Three, Not Everything

More projects is not better. Choose the **two or three strongest** that together show range:

- **The RAG document Q&A chatbot** — demonstrates embeddings, chunking, retrieval, and grounded, cited answers.
- **The autonomous research agent** — demonstrates tool calling, an agent loop, and structured output.
- **The production capstone** — demonstrates deployment, evaluation, observability, and cost control.

This trio is deliberate: it shows increasing depth from retrieval, to agency, to shipping and operating. Three excellent case studies beat seven half-finished ones. If one project is weak, cut it rather than dilute the set.

## The Anatomy of a Hireable Case Study

Treat every project as a self-contained case study with the **same five artifacts**, in a consistent style so the set looks intentional:

### 1. A clean GitHub repo

Public, well-organized, and credible at a glance:

- A logical structure (`/backend`, `/frontend`, `/evals`, `/docs`).
- **No secrets** — ever. Keys live in environment variables; ship an `.env.example` with placeholders and scan your history so a key never slipped in.
- A `LICENSE` (MIT is a fine default) and a `.gitignore` that excludes `.env` and build artifacts.
- **Meaningful commits.** A history of small, descriptive commits reads as a real engineer; one giant 'initial commit' of everything does not.
- Pin the repo on your GitHub profile.

### 2. A README that answers what / how / try-it

The README is the highest-traffic file you will ever write. Structure it so the answers are immediate:

- **One-line pitch** at the very top: *'A RAG assistant that answers questions about [corpus] with cited sources.'*
- **Live demo link** near the top — the 'can I try it now' answer.
- **Screenshot or GIF** so the reader sees it without running anything.
- **Architecture** — the diagram plus a few sentences.
- **Tech stack** — Python, FastAPI, the model provider, the vector DB.
- **Evaluation results** — your faithfulness/pass-rate number; almost no one else includes this, so it stands out.
- **Setup** — clone, install, `.env.example`, run.
- **Known limitations** — naming them signals maturity, not weakness.

### 3. An architecture diagram

One clean diagram per project, in a consistent visual style across all three (use **diagrams.net/draw.io** or Excalidraw). Show the request flow: browser → API → retrieval → agent/tool loop → model → streamed response. A diagram is the fastest way for a reviewer to understand your system, and it is the first image most people look at.

### 4. A live demo link

A clickable, working URL is the most persuasive artifact you have, because it removes all doubt. Deploy the frontend (Vercel/Netlify) and backend (Render/Railway/Fly), keep keys server-side, and **verify the link in an incognito window**. If hosting a full backend is impractical for a project, a hosted Streamlit or Hugging Face Space is an acceptable fallback — but a live link beats a screenshot every time.

### 5. A short demo video

Record **60-90 seconds** (Loom or a GIF) showing the app doing its one job end to end: a question typed, a streamed answer with a citation appearing, or a research report generated. Reviewers watch these; they are proof of life that screenshots cannot give. Link it at the top of the README and in your LinkedIn Featured section.

## The One-Page Design Doc

Beyond the README, write a **one-page design doc** per project — this is the artifact that separates an engineer from a tutorial-follower. Four short sections:

1. **Problem** — who is the user and what job does this do?
2. **Design** — the architecture and the key decisions (which vector DB, which chunking strategy, which model, why streaming).
3. **Trade-offs** — the alternatives you rejected and **why**. 'I used pgvector over Pinecone because the corpus is small and I wanted one fewer managed service.' This is the single clearest signal of judgment.
4. **Results** — quantified: faithfulness score, retrieval precision, latency, cost per query, before/after a change you made.

A reviewer who reads this knows you make deliberate decisions and measure their impact — which is exactly what the interview will probe.

## Common Portfolio Mistakes

A few mistakes quietly sink otherwise capable candidates. **Tutorial clones** — three projects that are obviously the same walkthrough everyone else followed — say nothing about you; add a real twist (your own corpus, a new tool, a different evaluation) so each is distinctly yours. **Broken live links** are worse than no link, because a dead demo signals you do not maintain your work; check them before every application. **A wall of unexplained code** with no README forces the reviewer to do your job, and they will simply move on. **Vague results** ('improved accuracy') carry none of the weight of a number ('raised faithfulness from 0.74 to 0.91'). And **inconsistent presentation** — one repo polished, the next a mess — undercuts the whole set, because reviewers judge you by the weakest artifact they happen to open. Treat all three projects to the same standard, or cut the one you cannot bring up to it.

## Tie It Together: One Narrative

Do not present three disconnected demos. Frame them as **one story** about who you are: *'I design, evaluate, and ship LLM-powered applications.'* The chatbot shows you can ground a model in real data; the agent shows you can give a model tools and structure; the capstone shows you can deploy, evaluate, and operate it. Write a short portfolio landing page — even a `README.md` on your GitHub profile — that introduces all three under that single line and links each repo, diagram, demo, and video.

That narrative is what you will carry into the next two lessons: your **resume** (Lesson 3) turns these case studies into quantified bullets, and your **LinkedIn profile** (Lesson 4) puts the same story and the same Featured links in front of recruiters.

## Portfolio Checklist

- [ ] 2-3 strong projects chosen; weak ones cut
- [ ] Each repo public, clean, structured, with a LICENSE and no secrets
- [ ] Meaningful commit history; `.env.example` present
- [ ] README answers what / how / try-it, with a live link and evals
- [ ] One consistent-style architecture diagram per project
- [ ] Working live demo link verified in incognito
- [ ] 60-90s demo video per project
- [ ] One-page design doc (problem, design, trade-offs, results) each
- [ ] A profile landing page framing all three as one narrative
