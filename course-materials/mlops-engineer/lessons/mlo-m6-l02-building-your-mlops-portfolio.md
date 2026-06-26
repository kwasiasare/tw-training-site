---
course: mlops-engineer
title: Building Your MLOps Portfolio
month: 6
monthTitle: Capstone & Career Launch
lesson: 2
summary: 'A portfolio is not a dump of repositories — it is a small set of curated artifacts that each
  prove a specific MLOps competency. In this lesson you turn two or three platform artifacts into hireable
  portfolio pieces: a deploy/CI-CD pipeline, an LLMOps serving stack (vLLM behind KServe), and an infrastructure-as-code
  repo. For each, you will define the competency it proves, structure the repo so a reviewer can verify
  it in minutes, write a results-and-trade-offs README, and add a short demo. You will learn to prioritize
  depth over breadth and to make every piece reproducible, because a reviewer who can run it believes
  it.'
objectives:
- Select two or three artifacts that each prove a distinct, in-demand MLOps competency
- Structure a portfolio repo so a reviewer can understand and verify it within minutes
- Write a README that leads with the problem, architecture, results, and trade-offs
- Extract a CI/CD pipeline, an LLMOps serving stack, and an IaC repo as standalone portfolio pieces
- Make every piece reproducible with pinned dependencies, seed data, and one-command setup
- Prioritize depth over breadth and avoid the common portfolio anti-patterns
video: mlo-m6-l02-building-your-mlops-portfolio.mp4
quiz:
- q: What is the goal of an MLOps portfolio piece, as opposed to just a code repository?
  options:
  - To contain as many files and frameworks as possible
  - To prove a specific, in-demand competency with evidence a reviewer can verify quickly — a clear problem,
    architecture, reproducible code, and quantified results
  - To stay private so competitors cannot copy it
  - To showcase the longest commit history
  answer: 1
  why: A portfolio piece is an argument that you can do a specific part of the job. It needs a stated
    problem, a legible architecture, reproducible code, and measurable results — not volume of files.
    Each piece should map to a competency a job description asks for.
- q: Which three artifacts best cover the core competencies an MLOps hiring manager screens for?
  options:
  - Three copies of the same model-training notebook
  - A deploy/CI-CD pipeline, an LLMOps serving stack (vLLM + KServe), and an infrastructure-as-code repo
  - A spreadsheet, a slide deck, and a blog post with no code
  - Three unfinished side projects
  answer: 1
  why: These three map to automation (CI/CD), GPU model serving (LLMOps), and reproducible infrastructure
    (IaC) — the highest-signal competencies for an MLOps role, and each is extractable from the systems
    you already built.
- q: Why prioritize depth over breadth when choosing portfolio pieces?
  options:
  - Because more pieces always rank higher in search
  - Because reviewers prefer empty repos
  - Because two or three deep, reproducible, well-documented pieces demonstrate real ownership, whereas
    many shallow repos signal tutorials never finished
  - Because breadth is illegal on GitHub
  answer: 2
  why: Reviewers can tell the difference between a deep, operable system and a pile of half-finished tutorials.
    A few polished, reproducible pieces with results and trade-offs prove ownership; breadth without depth
    dilutes the signal.
- q: What should the top of a portfolio repo README contain?
  options:
  - A wall of installation logs
  - The problem it solves, an architecture diagram, how to run it, the quantified results, and the trade-offs
    you made
  - Only a license file
  - A list of every library version with no explanation
  answer: 1
  why: A reviewer skims. Leading with the problem, a diagram, run instructions, quantified results, and
    trade-offs lets them verify capability in minutes — the structure that converts a repo view into an
    interview.
- q: For an IaC portfolio piece, which detail most signals production maturity?
  options:
  - Hardcoding credentials directly in the .tf files so it 'just works'
  - A single 2000-line file with every resource
  - Provisioning by clicking through the cloud console and screenshotting it
  - Remote state, no committed secrets, modular reusable code, and a documented plan/apply/destroy workflow
  answer: 3
  why: Remote state, secret hygiene, modular code, and a clean plan/apply/destroy lifecycle show you treat
    infrastructure as reviewable, reproducible, and safe — exactly the maturity an MLOps team needs.
- q: In two to four sentences, describe how you would extract your Module 5 LLM serving work into a standalone
    portfolio piece that proves the 'GPU model serving' competency.
  answer: 'I would create a focused repo whose README states the use case and the latency and cost SLOs,
    then shows the architecture: a quantized open model served by vLLM behind an OpenAI-compatible API,
    deployed as a KServe InferenceService with scale-to-zero and request-based autoscaling. I would include
    the vLLM serve command, the InferenceService manifest, the Prometheus/Grafana dashboard for TTFT,
    TPOT, throughput, and cost-per-1k-tokens, and a short load-test script with a one-command setup. The
    results section would report p95 TTFT and TPOT against target and the cost-per-1k-tokens before and
    after quantization and batching, and the trade-offs section would explain the cold-start cost of scale-to-zero
    and the accuracy check that justified quantization. A three-minute demo would show a streamed completion
    and the dashboard updating under load.'
  why: A strong answer scopes one competency, structures the repo around SLOs and architecture, includes
    runnable artifacts and dashboards, and reports quantified before/after results with trade-offs — proving
    GPU serving capability a reviewer can verify.
resources:
- label: GitHub Actions Documentation
  url: https://docs.github.com/en/actions
- label: Terraform Documentation — Infrastructure as Code
  url: https://developer.hashicorp.com/terraform/docs
- label: Made With ML — MLOps Course (project structure & best practices)
  url: https://madewithml.com/
- label: Awesome MLOps — curated tools and references
  url: https://github.com/visenger/awesome-mlops
---

## What a Portfolio Actually Is

A portfolio is not your entire GitHub account. It is a small, curated set of artifacts, each of which proves one specific competency a hiring manager screens for. The previous lesson packaged your two full capstones; this lesson zooms in and extracts **standalone portfolio pieces** from them — each a focused repo that a reviewer can open, understand, and verify in minutes. The mental model is simple: for every competency on a job description, you want exactly one piece that demonstrates it convincingly.

MLOps hiring managers consistently screen for three things: can you **automate** the path to production (CI/CD), can you **serve models reliably and efficiently** (especially GPU/LLM serving in 2026), and can you make **infrastructure reproducible** (IaC). Conveniently, you already built all three inside your Module 4 and Module 5 capstones. Your task now is to lift them out, sharpen them, and present each as its own argument.

## Choose Two or Three Pieces (Depth Over Breadth)

Resist the urge to publish ten repos. Two or three deep, reproducible, well-documented pieces beat a dozen shallow ones every time, because a reviewer can instantly tell the difference between an operable system and a half-finished tutorial. Pick pieces that cover distinct competencies rather than three variations of the same thing:

1. **A deploy / CI-CD pipeline** — proves automation and safe delivery.
2. **An LLMOps serving stack** — proves modern, GPU-aware model serving.
3. **An infrastructure-as-code repo** — proves reproducible, reviewable infrastructure.

Three is plenty. If you only have time to polish two, choose the CI/CD pipeline and the LLMOps stack, because GPU model serving and automation are the highest-signal competencies for MLOps roles in 2026.

## Piece 1 — The Deploy / CI-CD Pipeline

Extract the CI/CD work from your Module 4 capstone into a focused repo. The story it tells: *I automate testing, building, and safe deployment of an ML service.* Structure it so the workflow file is the centerpiece.

- **What to include:** a `.github/workflows` pipeline that lints, runs unit and integration tests, builds and pushes a container image tagged by commit SHA, and deploys with a **canary or blue-green** rollout; the model **promotion gate** that blocks a worse model; and a rollback path.
- **README leads with:** the problem (manual deploys are slow and risky), a diagram of the pipeline stages, how to trigger it, and the results — *deploy frequency enabled, rollback/MTTR, and the regression class the promotion gate prevents.*
- **Make it real:** wire it to a tiny sample model and a throwaway environment so the Actions runs are green and visible in the repo's Actions tab. A reviewer who sees passing CI believes the rest.

Key trade-offs to document: canary vs. blue-green vs. recreate; gating on a metric threshold vs. manual approval; and why secrets live in the secrets manager, never the repo.

## Piece 2 — The LLMOps Serving Stack

Extract your Module 5 serving work into a repo that proves **GPU-aware LLM serving**, the competency in highest demand in 2026. The story: *I serve open LLMs efficiently and operate them to latency and cost SLOs.*

- **What to include:** the **vLLM** serve command (with quantization and KV-cache settings), the **KServe** `InferenceService` manifest with `minReplicas: 0` for scale-to-zero and request-based autoscaling, the Prometheus scrape config and a Grafana dashboard covering **TTFT, TPOT, tokens/sec, GPU/KV-cache utilization, and cost-per-1k-tokens**, and a small load-test script (e.g., locust or a token-rate harness).
- **README leads with:** the use case, the latency SLOs (p95 TTFT, p95 TPOT) and the cost budget, the architecture diagram, one-command setup, and results — *p95 TTFT/TPOT against target and cost-per-1k-tokens before vs. after quantization and continuous batching.*
- **Trade-offs to document:** the cold-start cost of scale-to-zero; the accuracy check (an eval pass) that justified quantization; and tensor parallelism if the model exceeded one GPU.

If you lack a GPU to run it live, document the exact instance type and costs, include the dashboards and a recorded demo, and make the manifests apply cleanly so the engineering is verifiable even without a live endpoint.

## Piece 3 — The Infrastructure-as-Code Repo

Extract the Terraform from your Module 4 capstone into a clean IaC repo. The story: *I provision cloud infrastructure declaratively, reproducibly, and safely.*

- **What to include:** modular Terraform for the container registry, compute (EKS/GKE/ECS or a managed endpoint), networking, and IAM; a **remote state** backend; variables and environments; and a documented `plan` / `apply` / `destroy` workflow. Optionally, a CI job that runs `terraform plan` on pull requests.
- **README leads with:** what it provisions, a diagram of the resources, how to run it end to end, and the cost to stand it up and tear it down.
- **Maturity signals:** no committed secrets, modular reusable code instead of one giant file, remote state, and a clean destroy path so a reviewer can run it without leaving orphaned cloud spend.

This piece is small but disproportionately persuasive: it shows you treat infrastructure as code that is reviewed and versioned, not as console clicks no one can reproduce.

## Structure Every Repo the Same Way

Consistency makes you look like an engineer who ships. Use the same skeleton for each piece:

```
repo/
  README.md          # problem, architecture diagram, run, results, trade-offs
  architecture.png   # one clean diagram
  src/ or manifests/ # the actual code/config
  tests/             # something a reviewer can run
  Makefile           # `make up`, `make test`, `make down`
  .env.example       # documents config; never real secrets
  demo/              # link or short recording
```

The README is the highest-leverage file. A reviewer skims, so lead with the **problem**, then the **architecture diagram**, then **how to run it** (one command), then the **quantified results**, then the **trade-offs and what you'd improve**. Everything below that is reference.

## Make It Reproducible

Reproducibility is the property that makes a reviewer *believe* a piece. For each repo: pin dependency versions, ship seed data or a tiny sample model so nothing external is required, provide a one-command bring-up, document the exact tool versions, and confirm a clean teardown. Never commit secrets — use `.env.example` and a secrets manager. A piece a reviewer can run in five minutes is worth more than a far more ambitious one they cannot.

## Avoid the Anti-Patterns

- **Tutorial graveyard.** Ten unfinished repos signal abandonment, not skill. Curate to two or three.
- **No README, or a README that's just install logs.** Lead with problem, architecture, results.
- **No results.** "It works" is not a result; "p95 TTFT 420ms, cost-per-1k-tokens cut 58% via quantization + batching" is.
- **Secrets in the repo.** An instant credibility (and security) failure.
- **Runs only on your laptop.** If a reviewer can't reproduce it, it doesn't count.
- **Breadth over depth.** One deep, operable piece outperforms five shallow ones.

## The Deliverable

By the end of this lesson you should have two or three standalone portfolio repos — a CI/CD pipeline, an LLMOps serving stack, and an IaC repo — each with a consistent structure, a results-and-trade-offs README, a one-command setup, a short demo, and clean reproducibility. Pin them on your GitHub profile under the portfolio landing page from Lesson 1. These are the concrete pieces your resume bullets and LinkedIn profile will point to in the next two lessons.
