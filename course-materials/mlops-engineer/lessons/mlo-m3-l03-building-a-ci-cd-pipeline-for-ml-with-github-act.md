---
course: mlops-engineer
title: Building a CI/CD Pipeline for ML with GitHub Actions
month: 3
monthTitle: Orchestration, CI/CD & Infrastructure as Code
lesson: 3
summary: Learn how to design and implement a CI/CD pipeline for machine learning using GitHub Actions.
  You'll automate testing, container image building, and model deployment so every code change is validated
  and shipped reliably.
objectives:
- Explain how CI/CD principles apply to ML systems and how they differ from traditional software CI/CD
- Author GitHub Actions workflows using triggers, jobs, steps, and the runner environment
- Automate ML-specific testing including unit tests, data validation, and model performance checks
- Build and push container images to a registry as part of the pipeline
- Deploy models automatically to a target environment using secrets and environment gates
- Apply best practices for caching, matrix builds, and secure credential management
video: mlo-m3-l03-building-a-ci-cd-pipeline-for-ml-with-github-act.mp4
quiz:
- q: What is the primary purpose of the 'needs' keyword in a GitHub Actions workflow?
  options:
  - To install dependencies before a job
  - To enforce execution order and dependencies between jobs
  - To store secrets securely
  - To trigger the workflow on a schedule
  answer: 1
  why: '''needs'' makes one job wait for another to complete successfully, enforcing order like test →
    build → deploy.'
- q: Which addition makes an ML CI/CD pipeline different from a traditional software pipeline?
  options:
  - Running unit tests
  - A model evaluation/metrics gate before deployment
  - Using a Docker image
  - Logging into a registry
  answer: 1
  why: ML pipelines add data validation and a model metrics gate so accuracy regressions block deployment,
    beyond ordinary unit tests.
- q: Why is it recommended to tag container images with the commit SHA?
  options:
  - It makes images smaller
  - It provides traceability linking each deployment to an exact commit
  - It speeds up the build
  - It encrypts the image
  answer: 1
  why: Tagging with the SHA ties every deployed image to the precise code that produced it, enabling traceability
    and rollback.
- q: How should sensitive registry or cloud credentials be provided to a workflow?
  options:
  - Hardcoded in the YAML file
  - In a public README
  - Via encrypted GitHub Secrets using ${{ secrets.NAME }}
  - Printed to the build logs
  answer: 2
  why: Secrets are stored encrypted and referenced with the secrets expression; GitHub masks them in logs.
    Hardcoding is insecure.
- q: In one sentence, why should large model weight files generally not be committed directly to Git in
    an ML CI/CD setup?
  answer: Git is not designed for large binary files; bloated history slows clones and CI, so weights
    belong in artifact storage, DVC, or a model registry.
  why: Git history grows permanently with large binaries, hurting performance; dedicated artifact/model
    storage is the right tool.
- q: 'What does the workflow condition `if: github.ref == ''refs/heads/main''` accomplish on a build job?'
  answer: It restricts the job to run only when the workflow runs on the main branch, preventing builds/deploys
    from feature branches.
  why: The ref check ensures the build-and-push step executes only for the main branch, avoiding accidental
    deployments from other branches.
resources:
- label: GitHub Actions documentation
  url: https://docs.github.com/en/actions
- label: docker/build-push-action
  url: https://github.com/docker/build-push-action
- label: Using environments for deployment
  url: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
- label: 'CML: Continuous Machine Learning'
  url: https://cml.dev/
---

## Why CI/CD for ML?

Continuous Integration (CI) and Continuous Delivery/Deployment (CD) automate the path from a code change to a running service. For ML, this matters even more because your system has three moving parts: **code, data, and model artifacts**. A bug can hide in any of them.

A well-built ML CI/CD pipeline gives you:

- **Fast feedback** — tests run automatically on every push or pull request.
- **Reproducibility** — the same steps run the same way every time, not on someone's laptop.
- **Safety** — image building and deployment only happen after checks pass.
- **Traceability** — every deployed model maps back to a commit.

## How ML CI/CD differs from traditional CI/CD

| Concern | Traditional software | ML systems |
|---|---|---|
| What changes | Code | Code + data + model weights |
| Tests | Unit/integration | Plus data validation & model metrics |
| Build artifact | Binary/image | Image + model artifact |
| Failure modes | Logic bugs | Data drift, accuracy regression |

ML pipelines often add a **model evaluation gate**: even if the code passes, deployment is blocked if accuracy drops below a threshold.

## GitHub Actions core concepts

- **Workflow**: a YAML file in `.github/workflows/` that defines automation.
- **Event/trigger**: what starts the workflow (`push`, `pull_request`, `schedule`, `workflow_dispatch`).
- **Job**: a group of steps that run on the same runner; jobs run in parallel by default unless you add `needs`.
- **Step**: a single command (`run`) or reusable action (`uses`).
- **Runner**: the VM (e.g., `ubuntu-latest`) that executes the job.
- **Secrets**: encrypted values (registry passwords, cloud keys) accessed via `${{ secrets.NAME }}`.

## A typical ML pipeline structure

1. **Test job** — install deps, run linting, unit tests, data validation, and a lightweight model check.
2. **Build job** (`needs: test`) — build a Docker image containing the serving code and model, then push to a container registry.
3. **Deploy job** (`needs: build`) — pull the image and roll it out to a target environment, often gated by a protected GitHub Environment.

## Example workflow

```yaml
name: ml-cicd
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: pytest tests/ --maxfail=1
      - run: python scripts/validate_data.py
      - run: python scripts/check_model_metrics.py --min-accuracy 0.85

  build-and-push:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./deploy.sh ghcr.io/${{ github.repository }}:${{ github.sha }}
        env:
          CLOUD_TOKEN: ${{ secrets.CLOUD_TOKEN }}
```

## Key practices

- **Pin actions** to a major version (`@v4`) and pin base images for reproducibility.
- **Cache dependencies** (`cache: 'pip'`) to speed up runs.
- **Tag images with the commit SHA** so every deployment is traceable.
- **Use `needs`** to enforce order: don't build a broken model, don't deploy an unbuilt image.
- **Gate deployment** with GitHub Environments that require approvals or branch restrictions.
- **Never hardcode secrets** — always use `${{ secrets.* }}`; GitHub masks them in logs.
- **Add a model metrics gate** so accuracy regressions fail the build like any other test.

## Common pitfalls

- Storing large model files directly in Git — use artifact storage, DVC, or a model registry instead.
- Running expensive training in CI on every commit — separate training pipelines from serving CI/CD.
- Forgetting `if:` conditions, causing deploys from feature branches.
- Letting tests pass while metrics silently degrade — always include an evaluation check.
