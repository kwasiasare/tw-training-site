---
course: dami-ai-career
title: Writing technical blog posts
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 8
summary: Turn your projects into clear technical blog posts that show your thinking and help you get noticed
  by employers.
objectives:
- Understand why technical writing boosts your AI job search
- Choose a focused topic and a single takeaway for a post
- 'Structure a post: hook, problem, solution, results, lessons'
- Write reproducible code blocks readers can actually run
- Add diagrams, results, and honest caveats to build trust
- Publish on a free platform and share it the right way
video: m5-l08-blogging.mp4
quiz:
- q: What is the main career benefit of blogging for an aspiring AI engineer?
  options:
  - It replaces having a CV
  - It shows your thinking and creates a public portfolio
  - It guarantees a job offer
  - It earns advertising money quickly
  answer: 1
  why: A blog demonstrates how you reason and communicate — recruiters and engineers can see your work,
    which a CV alone cannot show.
- q: What should every post have exactly one of?
  options:
  - A code block
  - A clear single takeaway
  - An external link
  - A funny GIF
  answer: 1
  why: Focusing each post on one main idea keeps it readable and memorable; readers should know what they
    learned in one sentence.
- q: Why should code blocks in a post be runnable and self-contained?
  answer: So readers can copy, paste, and reproduce your results without guessing missing imports or setup
    — reproducibility builds trust.
  why: Broken or partial snippets frustrate readers and make you look careless; complete examples prove
    the post actually works.
- q: Where should API keys appear in any code you publish?
  options:
  - Hard-coded in the snippet
  - In an environment variable, never in the text
  - In the post title
  - In a screenshot
  answer: 1
  why: Never paste secrets. Read them from environment variables like ANTHROPIC_API_KEY so you don't leak
    credentials to the public.
- q: Name one good free platform for publishing a technical blog post.
  answer: Dev.to, Hashnode, Medium, or GitHub Pages are all common free choices.
  why: These give you a public URL, a built-in audience, and simple Markdown editing without managing
    servers.
- q: What makes a post more trustworthy and honest?
  options:
  - Hiding what went wrong
  - Including caveats, limitations, and failed attempts
  - Only showing perfect results
  - Avoiding numbers
  answer: 1
  why: Sharing limitations and what didn't work signals real engineering maturity and helps readers avoid
    the same pitfalls.
resources:
- label: Dev.to — free developer blogging community
  url: https://dev.to
- label: Hashnode — developer blogging platform
  url: https://hashnode.com
- label: GitHub Pages — host a blog from a repo
  url: https://pages.github.com
- label: Google Technical Writing Courses (free)
  url: https://developers.google.com/tech-writing
---

## Why blog at all?

You've built projects this course — a model, an A P I, a deployed app. A **technical blog post** turns that hidden work into something recruiters, engineers, and your future self can read. It shows not just *what* you built but *how you think*, which a CV alone never reveals.

Writing also sharpens your own understanding. If you can explain a confusion matrix clearly to a stranger, you truly understand it.

## Pick one idea

A strong post has **one takeaway**. Not "everything I learned about machine learning" — instead "how I cut my model's false positives in half." Narrow beats broad. Write the single sentence a reader should remember *before* you write anything else.

## A reliable structure

Most good technical posts follow the same shape:

1. **Hook** — a relatable problem in two sentences.
2. **Context** — what you were building and why.
3. **Solution** — the key steps, with code.
4. **Results** — numbers, screenshots, before/after.
5. **Lessons** — what you'd do differently.

## Make code reproducible

Readers will copy your code. Make it **complete**: real imports, no hidden setup, secrets in environment variables. Show a small, runnable example rather than your whole repo.

```python
import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from env

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarise this post in one sentence."}],
)
print(msg.content[0].text)
```

Keep your key out of the text. Set it once in your shell:

```bash
export ANTHROPIC_API_KEY="your-key-here"
python summarise.py
```

## Publish and share

Use a free platform — **Dev.to**, **Hashnode**, **Medium**, or **GitHub Pages**. Write in Markdown, add a clear title, and pick honest tags. Then share the link where engineers gather: LinkedIn, relevant Discord or Slack groups, and your network. One good post, shared well, beats ten posts no one reads.

## Your task

Pick one project from this course and **write a 600-word post** with one takeaway, one runnable code block, and one honest lesson. Publish it and share the U R L.
