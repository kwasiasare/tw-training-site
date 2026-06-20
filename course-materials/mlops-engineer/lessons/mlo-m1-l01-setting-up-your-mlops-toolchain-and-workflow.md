---
course: mlops-engineer
title: Setting Up Your MLOps Toolchain and Workflow
month: 1
monthTitle: Containerization & Foundations for ML Workloads
lesson: 1
summary: Set up a reproducible local MLOps development environment by installing and configuring Git,
  Python with virtual environments, Docker, and supporting tools, then wire them together into a coherent
  day-to-day workflow.
objectives:
- Install and verify Git, Python, and Docker on a local workstation
- Create isolated, reproducible Python environments using venv and pip/requirements files
- Configure Git with a sensible .gitignore and commit workflow for ML projects
- Build and run a minimal Docker container for an ML workload
- Describe how the core tools map to stages of the MLOps lifecycle and combine into a daily workflow
video: mlo-m1-l01-setting-up-your-mlops-toolchain-and-workflow.mp4
quiz:
- q: Why should you copy requirements.txt into the Docker image before copying the rest of your code?
  options:
  - It reduces the final image size
  - It lets Docker cache the dependency-install layer so rebuilds are faster
  - It is required by the Dockerfile syntax
  - It prevents secrets from leaking into the image
  answer: 1
  why: Docker caches layers; copying requirements first means the expensive pip install layer is only
    rebuilt when dependencies change, not on every code edit.
- q: What is the recommended way to handle large datasets and model weights in an ML project?
  options:
  - Commit them directly to Git
  - Exclude them via .gitignore and track them with DVC or object storage
  - Store them inside the Docker image
  - Email them between teammates
  answer: 1
  why: Git is poor at large binaries. You gitignore them and use tools like DVC or object storage, tracking
    only lightweight pointers/metadata in Git.
- q: Why create a per-project Python virtual environment instead of installing packages globally?
  options:
  - It makes Python run faster
  - It isolates and pins dependencies for reproducibility per project
  - It is the only way to use pip
  - It automatically deploys your model
  answer: 1
  why: A venv isolates each project's dependencies and versions, preventing conflicts and enabling reproducible
    installs from a frozen requirements file.
- q: Which command confirms that the Docker daemon is actually working after installation?
  options:
  - docker --version
  - docker run hello-world
  - docker build .
  - git --version
  answer: 1
  why: docker --version only prints the client version; docker run hello-world pulls and runs a container,
    proving the daemon and runtime work end to end.
- q: In one short phrase, what is the central MLOps theme that connects venvs, requirements files, and
    Docker?
  answer: reproducibility
  why: All three tools exist to make environments and runs reproducible across machines and team members,
    which is the core goal of MLOps foundations.
- q: Name one tool you would use to track ML experiments (metrics, parameters, runs).
  answer: MLflow
  why: MLflow (or Weights & Biases) is commonly used to track experiment parameters, metrics, and artifacts
    across runs.
resources:
- label: Docker — Get Started / official docs
  url: https://docs.docker.com/get-started/
- label: Python venv documentation
  url: https://docs.python.org/3/library/venv.html
- label: Pro Git book (free online)
  url: https://git-scm.com/book/en/v2
- label: DVC — Data Version Control docs
  url: https://dvc.org/doc
---

## Why a Standard Toolchain Matters

MLOps lives at the intersection of data science, software engineering, and operations. Before you can train, version, deploy, or monitor models, you need a reliable, reproducible local environment. A consistent toolchain reduces the classic *"it works on my machine"* problem and gives every engineer the same baseline.

The four foundations we configure in this lesson are:

- **Git** — version control for code, configuration, and pipeline definitions.
- **Python** — the dominant language for ML, managed with isolated environments.
- **Docker** — containerization so workloads run identically anywhere.
- **Supporting CLI tools** — package managers, a code editor, and ML utilities.

## Installing and Verifying the Core Tools

Start by confirming each tool is present and on a supported version. Run these in a terminal:

```bash
git --version       # expect 2.30+
python3 --version   # expect 3.10+
docker --version    # expect 20.10+
docker run hello-world  # confirms the Docker daemon works
```

If any command fails, install via your platform: `apt`/`brew` for Git and Python, and Docker Desktop (macOS/Windows) or Docker Engine (Linux). On Linux, add your user to the `docker` group so you don't need `sudo`.

## Configuring Git for ML Projects

Set your identity once, globally, then create a project-scoped `.gitignore` so you never commit large or secret artifacts:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

A good ML `.gitignore` excludes virtual environments, data, model binaries, and caches:

```gitignore
.venv/
__pycache__/
*.pyc
data/
models/
*.ckpt
.env
.ipynb_checkpoints/
```

Large datasets and model weights should **not** live in Git directly — use tools like DVC or object storage and track only pointers/metadata.

## Isolated Python Environments

Never install project dependencies into the system Python. Create a per-project virtual environment so dependency versions are pinned and reproducible:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install scikit-learn pandas
pip freeze > requirements.txt
```

Commit `requirements.txt` (or a lockfile from tools like `pip-tools`, Poetry, or `uv`) so teammates and CI install the exact same versions. Reproducibility is the central theme of MLOps.

## A Minimal Dockerized ML Workload

Docker packages your code *and* its environment into an image that runs the same on a laptop, CI runner, or cluster. A simple `Dockerfile` for a Python ML app:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "train.py"]
```

Build and run it:

```bash
docker build -t my-ml-app:dev .
docker run --rm my-ml-app:dev
```

Key practices: copy `requirements.txt` *before* the rest of the code so Docker caches the dependency layer; use slim base images; and never bake secrets into the image (pass them at runtime with `--env` or mounted files).

## How the Tools Fit the MLOps Lifecycle

| Stage | Primary tools |
|-------|---------------|
| Develop / experiment | Python, venv, Git, editor (VS Code) |
| Version data & models | DVC, object storage |
| Package & ship | Docker |
| Automate | Git + CI/CD |
| Track experiments | MLflow / Weights & Biases |

Your daily loop becomes: branch in Git → develop in an activated venv → test → build a Docker image → push and let CI validate it. Mastering this local foundation makes every later MLOps concept — pipelines, registries, deployment — far easier.

## Recap

You now have a verified, reproducible workstation: Git for versioning, a virtual environment for isolated dependencies, and Docker for portable execution. These are the non-negotiable foundations for everything that follows in the course.
