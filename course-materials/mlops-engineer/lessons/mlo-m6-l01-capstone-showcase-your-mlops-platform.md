---
course: mlops-engineer
title: 'Capstone Showcase: Package Your MLOps Platform as Portfolio Evidence'
month: 6
monthTitle: Capstone & Career Launch
lesson: 1
summary: 'You already built two capstones in this course: an end-to-end production MLOps system in Module
  4 and a production LLM serving system in Module 5. This lesson does not build a third system — it shows
  you how to package those two into one coherent, portfolio-grade showcase. You will produce the evidence
  a hiring manager actually evaluates: clean architecture diagrams, public GitHub repos with one-command
  setup, a short demo video, a written design doc per system, and quantified results tied to SLOs. You
  will also score your work against a ''portfolio-grade'' rubric so you know it is ready before you ship
  it.'
objectives:
- Frame your Module 4 and Module 5 capstones as one portfolio narrative instead of two disconnected labs
- 'Produce the four evidence artifacts per system: architecture diagram, GitHub repo, demo video, and
  design doc'
- Write quantified results that tie back to the SLOs you defined (latency, throughput, cost, MTTR, deploy
  frequency)
- Make each repo reproducible with a one-command setup and a README a reviewer can follow in minutes
- Explain your design decisions as trade-offs and rejected alternatives, the clearest signal of engineering
  judgment
- Score your showcase against a portfolio-grade rubric and close gaps before you publish it
video: mlo-m6-l01-capstone-showcase-your-mlops-platform.mp4
quiz:
- q: This module's first lesson is a showcase, not a build. Why package the existing Module 4 and Module
    5 capstones rather than start a third project?
  options:
  - Because three projects are always worse than two
  - Because the two existing capstones already demonstrate end-to-end ownership across classic ML and
    LLM serving; the hireable work is turning them into evidence (diagrams, repos, demos, design docs,
    quantified results), not building more
  - Because hiring managers never look at GitHub repos
  - Because a third project would be easier than documenting the first two
  answer: 1
  why: The capstones already prove capability; what converts effort into offers is presentation and the
    ability to defend the work. Packaging the two systems into diagrams, repos, demos, design docs, and
    quantified results is higher-leverage than adding an undocumented third build.
- q: Which set of four artifacts best turns one capstone into a persuasive portfolio case study?
  options:
  - A folder of screenshots with no narrative
  - A clean architecture diagram, a public GitHub repo with one-command setup, a 3-5 minute demo video,
    and a one-page design doc with trade-offs and quantified results
  - Only the certification badge
  - A long list of every command you ran during the build
  answer: 1
  why: Hiring managers buy outcomes and judgment. A diagram shows the design at a glance, the repo proves
    it is real and reproducible, the demo proves it runs, and the design doc explains why you chose this
    design over alternatives and what it achieved.
- q: What single property most separates a portfolio-grade MLOps repo from an average one?
  options:
  - The largest possible number of files
  - A private repo only you can see
  - Reproducibility — a reviewer can clone it and bring the system up with one command, exactly as taught
    in both capstones
  - Using the newest possible framework versions
  answer: 2
  why: Both course capstones stress that reproducibility (one-command setup) is what separates a great
    project from an average one. It demonstrates the system is genuinely engineered and operable, not
    a notebook that only runs on your laptop.
- q: How should you state results so they are credible to a hiring manager?
  options:
  - Claim the system is 'fast and scalable' with no numbers
  - 'Tie outcomes to the SLOs you defined: p95 latency or TTFT/TPOT met, tokens/sec throughput, cost-per-1k-tokens
    before vs. after optimization, deploy frequency, and rollback/MTTR'
  - Report only that the code compiles
  - List the tools used without any measured impact
  answer: 1
  why: Quantified results tied to explicit SLOs (latency, throughput, cost, deploy frequency, MTTR) make
    claims verifiable and demonstrate you operate to targets — the same SLO discipline both capstones
    required.
- q: When you frame both capstones as one narrative, what is the strongest unifying story?
  options:
  - '''I followed two tutorials end to end'''
  - '''I design, deploy, monitor, and operate ML systems in production — for both classic models and LLMs
    — with CI/CD, IaC, and SLO-driven reliability'''
  - '''I know many tools'''
  - '''I prefer Kubernetes to Docker Compose'''
  answer: 1
  why: A single positioning line that spans classic ML and LLM serving, anchored in deployment, monitoring,
    CI/CD, IaC, and SLOs, tells a hiring manager exactly what an MLOps engineer does — and your two capstones
    are the proof.
- q: In two to four sentences, outline what you would put in the one-page design doc for your Module 4
    MLOps capstone so it reads as engineering judgment rather than a task list.
  answer: 'I would open with the business problem and the success criteria, the ML metric thresholds and
    the latency/throughput SLOs, then show the five-plane architecture (data, training pipeline with a
    promotion gate, containerized serving, CI/CD, and monitoring with drift). I would state the measurable
    results against those SLOs (for example p95 under 200ms, drift alerting wired to retraining) and then
    the key trade-offs: why I chose canary over big-bang deploys, why a promotion gate, and what I would
    improve next. Closing with the rejected alternative for each major decision is what signals senior
    judgment. That arc — problem, architecture, results, trade-offs — is what separates an engineer from
    a button-clicker.'
  why: A strong design doc follows a problem-to-trade-offs arc, ties results to the SLOs defined at scoping,
    and names the alternatives rejected, which is exactly the judgment hiring managers probe for.
resources:
- label: 'Google Cloud — MLOps: Continuous delivery and automation pipelines in ML (maturity levels)'
  url: https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- label: MLflow Documentation — Tracking & Model Registry
  url: https://mlflow.org/docs/latest/index.html
- label: KServe — Generative Inference (LLM serving)
  url: https://kserve.github.io/website/docs/model-serving/generative-inference/multi-node
- label: vLLM Documentation
  url: https://docs.vllm.ai/en/latest/
---

## A Showcase, Not a Third Build

You have already done the hard part. In the Module 4 capstone you built an end-to-end production MLOps system — data and training pipelines, a containerized serving API, CI/CD, infrastructure as code, and monitoring with drift detection. In the Module 5 capstone you built a production LLM serving system — vLLM behind an OpenAI-compatible API, quantized and scaled on Kubernetes with KServe, observed with token- and cost-aware telemetry, gated by an evaluation suite, and operated inside a cost budget. This lesson does **not** ask you to build a third system. It asks you to turn those two into one polished, portfolio-grade showcase that gets you interviews.

The difference between a learner and a hire is rarely capability — it is presentation and the ability to defend the work. Most strong candidates lose not because the engineering is weak but because no one can see it, or because the artifacts that recruiters do see say nothing. Your job here is to convert two real systems into evidence a hiring manager can evaluate in minutes.

## One Narrative Across Two Systems

Do not present two unrelated labs. Frame them as a single story with a clear through-line: *I design, deploy, monitor, and operate machine learning systems in production — for both classic models and large language models.* The Module 4 system proves you own the classic ML lifecycle: pipelines, a model promotion gate, CI/CD, IaC, and drift monitoring. The Module 5 system proves you extend that same discipline to GPU-served LLMs: efficient serving, quantization, autoscaling, evaluation gates, guardrails, and cost control. Together they say the one thing an MLOps hiring manager wants to hear — you can take a model from a checkpoint to a reliable, observable, cost-bounded endpoint, and keep it healthy after deployment.

Write a short portfolio landing page (even a pinned README on your GitHub profile) that introduces both systems under that single sentence, then links each one. This is the frame everything else hangs on.

## Four Artifacts Per System

Treat each capstone as a self-contained case study with exactly four artifacts. Resist the urge to add more; depth and clarity beat volume.

- **Architecture diagram.** One clean diagram per system in a consistent visual style. For Module 4, draw the five planes — data and feature layer, training pipeline (ingest, validate, train, evaluate, register), containerized serving, CI/CD, and monitoring — and show the artifacts that connect them: data versions, model versions in the registry, and image tags. For Module 5, draw the serving runtime (vLLM), the optimization layer (quantized checkpoint), the scaling plane (KServe with scale-to-zero and tensor parallelism), the observability and evaluation plane, and the governance/cost plane. The diagram is the first thing anyone looks at, so make it legible.
- **GitHub repo.** A public repo per system (or a monorepo with two clearly separated folders). Include the real artifacts: Dockerfiles, the FastAPI service, the training pipeline with the promotion gate, the Terraform/IaC, the GitHub Actions workflows, the Kubernetes/KServe manifests, the Prometheus/Grafana config and dashboard JSON, the drift job, and — for Module 5 — the vLLM serve command, the KServe `InferenceService`, and the RAGAS/LLM-as-judge eval suite. Each repo needs a README that states the problem, shows the architecture, and explains how to deploy and how to test.
- **Demo video.** Three to five minutes per system showing it working end to end: a deploy running through CI/CD, a prediction or a streamed LLM completion, the Grafana dashboard updating, an alert firing, the eval gate blocking a bad change. Recruiters and engineers watch these; a working demo is worth more than any description.
- **Design doc.** One page per system: the business problem, the design and why, the trade-offs and limitations, and the measurable results. This is the artifact that separates an engineer from a button-clicker, because it shows judgment rather than clicks.

## Quantify the Results Against Your SLOs

Both capstones made you define SLOs up front — use them now as the spine of your results. Replace vague claims ("fast and scalable") with measured outcomes tied to those targets:

- **Module 4 (classic ML):** p95 latency vs. the target (e.g., p95 < 200ms), throughput in requests/sec, the ML metric the model hit, deploy frequency enabled by CI/CD, rollback time / MTTR from your canary or blue-green strategy, and drift caught before it degraded predictions.
- **Module 5 (LLM serving):** p95 **TTFT** and **TPOT** against their SLOs, tokens/sec throughput, **cost-per-1k-tokens before vs. after** quantization and batching (the single most persuasive number for an LLM system), GPU utilization, scale-to-zero savings during idle, and the eval score that gated promotion.

Even in a lab you can measure all of these. Numbers make claims credible; a before/after cost reduction or a stated MTTR signals that you operate to targets, not just that you can wire components together.

## Make It Reproducible

The single highest-impact property of an MLOps portfolio is reproducibility, and both capstones already emphasized it. A reviewer should be able to clone the repo and bring the system up with **one command** — `make up`, `docker compose up`, a `terraform apply` plus a documented bootstrap, or a `skaffold`/`kubectl apply` path with seed data. Pin dependencies, never commit secrets (use a secrets manager or `.env.example`), and document the exact versions of MLflow, vLLM, KServe, and the cloud provider you used. A clean, runnable repo with a one-command setup is what moves a capstone from "good" to "memorable."

## Explain Decisions as Trade-offs

When a reviewer or interviewer asks "why did you build it this way?", never answer with a feature list — name the alternative you rejected and why. *I used a canary rollout instead of a big-bang deploy so a bad model rolls back in seconds without downtime. I added a model-metric promotion gate so a worse model can't reach production. I set KServe `minReplicas: 0` to avoid paying for idle GPUs, accepting a cold start as the trade-off. I quantized the LLM to AWQ/FP8 to roughly halve cost, but only after the eval suite confirmed quality held.* Considering alternatives is the clearest signal of seniority, and your design docs should already capture each one.

## The Portfolio-Grade Rubric

Before you publish, score each system against this checklist — anything missing is a gap to close:

1. **Clarity** — a diagram and one-paragraph problem statement a non-expert understands in 60 seconds.
2. **Reproducibility** — one-command setup, pinned deps, no secrets, documented versions.
3. **Completeness** — all five planes present and connected (serving, pipeline/optimization, CI/CD or scaling, monitoring/eval, governance/cost).
4. **Quantified results** — outcomes tied to the SLOs you defined, with at least one before/after number.
5. **Judgment** — a design doc that names trade-offs and rejected alternatives.
6. **Proof it runs** — a 3-5 minute demo video and dashboard screenshots.

When both capstones clear all six, you have a showcase, not a pile of code. That package — two systems, eight artifacts, one narrative, and quantified results — is the foundation for the resume, portfolio pieces, and job search in the rest of this module.

## The Deliverable

By the end of this lesson you should have a portfolio landing page that frames both capstones under one positioning line; for each system a clean architecture diagram, a public reproducible GitHub repo, a 3-5 minute demo video, and a one-page design doc; quantified results tied to your SLOs; and a rubric pass confirming every gap is closed. You are not building more — you are making what you already built impossible to ignore.
