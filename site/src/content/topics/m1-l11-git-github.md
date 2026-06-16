---
title: Git & GitHub fundamentals
month: 1
monthTitle: Python Foundations + Git
lesson: 11
summary: Track changes to your code with Git and back it up, share it, and collaborate online using GitHub.
objectives:
- Explain what Git and GitHub are and how they differ
- Initialise a repository and record snapshots with add and commit
- Inspect history and status with log and status
- Connect a local repo to GitHub and push your work
- Use branches to work safely without breaking main
- Ignore files you should never commit with a .gitignore
video: m1-l11-git-github.mp4
quiz:
- q: What is the difference between Git and GitHub?
  answer: Git is the version-control tool on your computer; GitHub is an online service that hosts Git
    repositories.
  why: Git runs locally and tracks changes; GitHub stores a copy in the cloud for backup and collaboration.
    You can use Git without GitHub.
- q: Which command records a snapshot of your staged changes?
  options:
  - git save
  - git commit
  - git push
  - git stage
  answer: 1
  why: git commit takes everything you have staged with git add and saves it as a permanent snapshot in
    the history, with a message.
- q: What does git add do?
  options:
  - Uploads files to GitHub
  - Creates a new repository
  - Moves changes into the staging area
  - Deletes a file
  answer: 2
  why: git add stages changes — it tells Git which edits you want included in your next commit. It does
    not upload or commit anything by itself.
- q: What is a .gitignore file for?
  answer: It lists files and folders that Git should not track, such as secrets, virtual environments,
    and large data files.
  why: Keeping things like passwords, .env files, and venv out of your repo avoids leaking secrets and
    bloating the history.
- q: Why use a branch instead of committing straight to main?
  options:
  - Branches run faster
  - It lets you work on a change in isolation
  - It deletes the main branch
  - GitHub requires it
  answer: 1
  why: A branch is a separate line of work, so you can experiment freely. If it works you merge it into
    main; if not, you discard it — main stays safe.
- q: 'In what order do these three steps normally happen: commit, add, push?'
  answer: add, then commit, then push.
  why: You stage changes with add, snapshot them with commit, then send those commits to GitHub with push.
resources:
- label: Pro Git book (free, official) — Chapters 1-3
  url: https://git-scm.com/book/en/v2
- label: GitHub Docs — Get started with Git and GitHub
  url: https://docs.github.com/en/get-started
- label: Atlassian — Git Tutorials and cheat sheet
  url: https://www.atlassian.com/git/tutorials
- label: Oh My Git! — a free game for learning Git
  url: https://ohmygit.org/
---

## Why version control?

Imagine saving files as `report_final.py`, then `report_final_v2.py`, then `report_final_REALLY_final.py`. It quickly becomes chaos. **Version control** solves this: it records snapshots of your project over time so you can see what changed, when, and why — and roll back if you break something.

**Git** is the most popular version-control tool. It runs on your own computer. **GitHub** is a website that stores copies of your Git repositories online, so your work is backed up and you can share it with others or with your future employer.

## Your first repository

A **repository** (or *repo*) is a folder that Git is watching. You create one with `git init`. After that, Git tracks every change you choose to record.

```bash
git init
git add hello.py
git commit -m "Add hello.py"
```

There are three stages: your **working directory** (your files), the **staging area** (changes you've marked with `add`), and the **repository** (snapshots saved with `commit`).

## Checking status and history

Two commands you'll run constantly: `git status` shows what's changed and what's staged, and `git log` shows the history of commits.

```bash
git status
git log --oneline
```

Every commit needs a clear message. Write it in the present tense, describing what the change does — for example, `Fix off-by-one error in loop`.

## Connecting to GitHub

Create an empty repo on GitHub, then link your local one to it and push. **Push** sends your commits up; **pull** brings new commits down.

```bash
git remote add origin https://github.com/you/project.git
git branch -M main
git push -u origin main
```

## Branches

A **branch** is a separate line of work. You can build a feature on a branch without touching `main`. When it works, you **merge** it back.

```bash
git switch -c add-login
# ...make changes, add, commit...
git switch main
git merge add-login
```

## Ignore the things you should never commit

Create a file called `.gitignore` listing things Git should skip — secrets, your virtual environment, and data files.

```bash
.env
venv/
__pycache__/
*.csv
```

## Your task

Put one of your Python scripts under Git, push it to a new GitHub repo, and add a `.gitignore`.
