---
course: kwasi-GenAI
title: 'Portfolio and interview: your background is the edge'
month: 6
monthTitle: Capstone & Career
lesson: 3
summary: Build a portfolio that lands interviews and prepare to win them — positioning your cloud and
  security background as a real differentiator, telling the project story well, and handling the common
  applied GenAI interview topics.
objectives:
- Position a cloud, DevOps, and security background as a differentiator in applied GenAI
- Structure a portfolio around one deployable flagship project plus clear write-ups
- Tell a project story using a problem, approach, decisions, results structure
- Answer common applied GenAI interview questions on RAG, agents, evals, and safety
- Connect prompt injection, secrets, and human-in-the-loop to security fundamentals you know
- Prepare honest answers about trade-offs, failures, and what you'd do next
video: g6-l03-portfolio-and-interview.mp4
quiz:
- q: What is the single strongest differentiator a cloud/security engineer brings to applied GenAI?
  options:
  - Knowing more prompts than anyone
  - Being able to secure and deploy what others can only prototype
  - Having the fastest typing speed
  - Memorising model parameter counts
  answer: 1
  why: Most applied AI engineers can prototype but cannot secure or deploy to production — that operational
    and security competence is exactly what teams are missing.
- q: How should a portfolio be structured to land interviews?
  options:
  - Twenty half-finished notebooks
  - One deployable flagship project with a clear write-up, plus supporting pieces
  - Only a list of certifications
  - A single screenshot with no code
  answer: 1
  why: One polished, deployed flagship that a reviewer can run and read beats a pile of unfinished experiments;
    depth and a clear story win.
- q: Which structure helps you tell a project story clearly in an interview?
  options:
  - Random facts in any order
  - Problem, approach, key decisions, results
  - Only the final result with no context
  - A list of every library you imported
  answer: 1
  why: Problem -> approach -> decisions -> results gives the interviewer context, reasoning, and evidence
    in a logical arc they can follow.
- q: Name one applied GenAI interview topic that maps directly onto security fundamentals you already
    know.
  answer: Prompt injection — it is untrusted input crossing a trust boundary, the same threat model as
    injection attacks, handled with input validation, least privilege for tools, and human approval on
    risky actions.
  why: Prompt injection is a classic trust-boundary problem, so your existing security instincts transfer
    directly and impress interviewers.
- q: Why is it good to discuss a project's trade-offs and failures in an interview?
  answer: It shows engineering maturity and honesty — interviewers trust someone who understands the limits
    of their system more than someone who claims it is perfect.
  why: Naming trade-offs and what you'd improve signals real understanding and self-awareness, which senior
    interviewers actively look for.
- q: When asked 'how do you know your RAG system is good?', what is the strongest answer?
  options:
  - It feels right
  - I built an eval set with expected answers and measure retrieval and answer quality, plus guardrails
    on output
  - I never tested it
  - The model is large so it must be good
  answer: 1
  why: Pointing to an eval set with measurable retrieval and answer-quality metrics, plus output guardrails,
    proves you treat quality as something you measure, not vibes.
resources:
- label: Anthropic — Building effective agents
  url: https://www.anthropic.com/research/building-effective-agents
- label: Anthropic docs — Reduce prompt injection / strengthen guardrails
  url: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks
- label: OWASP — Top 10 for Large Language Model Applications
  url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- label: Anthropic docs — Define success criteria & evaluations
  url: https://platform.claude.com/docs/en/test-and-evaluate/define-success
- label: GitHub Docs — About READMEs (project write-ups)
  url: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
---

## Your background is not a gap — it's the edge

It is easy to walk into applied GenAI feeling like the newcomer who must catch up to the data scientists. Flip that. **Most applied AI engineers cannot secure or deploy what they prototype — you can.** That sentence is your entire positioning. Teams are drowning in clever prototypes that nobody can ship safely. You arrive already knowing CI/CD, secrets management, identity, networking, monitoring, and threat modelling. You don't need to out-prompt anyone. You need to be the person who turns a notebook into a production service that doesn't leak keys or get jailbroken.

Say it plainly in your CV, your README, and your interviews: *I bring cloud and security engineering to GenAI — I can ship and secure what others can only demo.*

## A portfolio that lands interviews

Depth beats breadth. A reviewer would rather run **one deployable flagship project** than skim twenty half-finished notebooks. Your capstone is that flagship: a tool-using, retrieving, planning, guarded system you actually deployed.

Structure the portfolio like this:

- **The flagship**, deployed and runnable, with a clear `README`.
- **A write-up** that explains the problem, the architecture, the key decisions, and the results — written for a busy reader.
- **Supporting pieces** (the earlier phase deliverables) as smaller, linked examples.

The README is doing real work. Open with one sentence on what the system does, then a diagram, then how to run it, then what you'd improve. Make the security and deployment story visible: "secrets in Key Vault, input/output guardrails, human approval on irreversible tool calls, eval suite in CI."

## Telling the project story

In interviews you'll be asked to "walk me through a project." Use a simple arc: **Problem → Approach → Key decisions → Results.**

- **Problem:** what real need did it serve? Keep it concrete.
- **Approach:** the architecture — agent orchestrating RAG and tools, wrapped by guardrails and evals.
- **Key decisions:** why RAG over fine-tuning, why a typed tool contract, why a human gate on certain actions. This is where you show judgement.
- **Results:** what your eval set measured, and what you'd improve next.

The decisions and results sections are where senior interviewers decide whether you understand your own system. Always name a trade-off — "retrieval was fast but sometimes missed context, so I added a re-ranking step" — because honesty about limits reads as maturity.

## Common interview topics

Expect questions across four areas, all of which you can connect to things you know.

**RAG.** How does retrieval work? How do you chunk and embed? How do you know it's good? Strong answer: an eval set with expected answers, measuring retrieval hit-rate and answer quality.

**Agents.** When is an agent the right tool versus a simple workflow? How do you stop runaway loops? Strong answer: agents for open-ended, multi-step tasks; cap iterations; gate irreversible actions.

**Evals and quality.** "How do you know it works?" Never answer "it feels right." Point to a measurable eval set and output guardrails.

**Safety and security — your home turf.** **Prompt injection** is untrusted input crossing a trust boundary — the same threat model as any injection attack. You handle it with input validation, **least privilege** for tools, output filtering, and **human-in-the-loop** approval on risky actions. Secrets never live in prompts or code; they live in a managed vault. When you frame LLM safety in classic security terms — trust boundaries, least privilege, defence in depth — you sound like someone who has done this before, because you have.

When discussing models, use current Claude — `claude-opus-4-8` via the Messages API — and note it runs on Amazon Bedrock and Azure (Microsoft Foundry), so deployment fits the clouds you operate.

## Honest answers win

The best interview answers admit limits. "What would you do differently?" is a gift — answer it with a real improvement. "Where does it break?" shows you've stress-tested your own work. Confident honesty beats polished overclaiming every time, especially with experienced interviewers.

## Your task

Write the README and one-page write-up for your capstone using the Problem → Approach → Key decisions → Results structure, and make the security-and-deployment story explicit. Then draft and rehearse out loud three answers: one on how you know your system works, one on how you'd handle prompt injection, and one on a trade-off you made and what you'd improve next.
