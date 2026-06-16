---
course: dami-ai-career
title: Portfolio site + README craft
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 9
summary: Build a clean portfolio site and write READMEs that make recruiters understand and trust your
  projects in seconds.
objectives:
- Understand what a hiring manager actually looks for in a portfolio
- Structure a README that explains what, why, and how
- Add setup, usage, and demo sections people can follow
- Publish a simple portfolio site with GitHub Pages
- Pin and order your best repositories on GitHub
- Write project descriptions that lead with impact, not tech
- Avoid the common mistakes that get portfolios ignored
video: m5-l09-portfolio.mp4
quiz:
- q: What is the single most important section a README should open with?
  options:
  - Your full git history
  - A one-line description of what the project does
  - A list of every dependency version
  - Your personal biography
  answer: 1
  why: A reader decides in seconds whether to keep reading. A clear one-liner answering 'what is this?'
    earns that time.
- q: Which file name does GitHub automatically render on a repository's front page?
  options:
  - readme.txt
  - ABOUT.md
  - README.md
  - index.html
  answer: 2
  why: GitHub looks for README.md (Markdown) in the repo root and renders it as the landing page.
- q: GitHub Pages can host a static site directly from which of these?
  options:
  - A running Python server
  - A branch or /docs folder in your repo
  - A paid database
  - An external FTP server
  answer: 1
  why: GitHub Pages serves static files from a chosen branch or the /docs folder — no server needed, and
    it is free.
- q: Why should a project description lead with impact rather than the tech stack?
  answer: Because recruiters and managers care first about what the project does and the problem it solves;
    the tech stack matters but is secondary.
  why: Impact tells them why the work matters; the stack is easy to skim later. Leading with 'built a
    churn predictor that flags at-risk users' beats 'used pandas and scikit-learn'.
- q: What does pinning a repository on your GitHub profile do?
  answer: It places that repository at the top of your profile so visitors see your best work first instead
    of your most recent commit.
  why: You can pin up to six repos. Use them to curate, since visitors rarely scroll past the top of your
    profile.
- q: Name two things a good 'Usage' section in a README should include.
  answer: A copy-pasteable command to run the project and an example of the expected input and output.
  why: People want to try it fast. A runnable command plus a sample result removes guesswork and proves
    the project works.
resources:
- label: GitHub Pages — official documentation
  url: https://docs.github.com/en/pages
- label: Make a README — guide to writing good READMEs
  url: https://www.makeareadme.com/
- label: Awesome README — curated examples and templates
  url: https://github.com/matiassingers/awesome-readme
- label: Shields.io — README badges for build, license, and more
  url: https://shields.io/
---

## Why a portfolio matters

Your CV says you can do the work. Your **portfolio proves it**. For someone moving from a maths degree and an L1 support role into A I, a portfolio is the bridge — it turns 'I studied this' into 'here is something I built that runs'.

A hiring manager spends seconds, not minutes, on each candidate. Your job is to make those seconds count: clear projects, clear writing, no friction.

## What goes in the portfolio

Quality beats quantity. Three or four **finished, well-documented** projects beat twenty half-built ones. For each project show the problem, your approach, the result, and how to run it.

Curate ruthlessly. Pin your best work on GitHub so visitors see it first. Delete or archive the noise.

## Anatomy of a great README

The README is the front door of every project. Open with a one-line description, then expand. A reliable structure:

```markdown
# Project Title

One sentence: what it does and who it helps.

## Features
- Bullet the key things it does

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py --input data.csv
```

## Results
A chart, a metric, or a short demo.
```

Lead with **impact**, not tech. 'Predicts customer churn with 87% accuracy' beats 'uses scikit-learn'.

## Publishing with GitHub Pages

GitHub Pages hosts a static site for free, straight from your repo. Put an `index.html` in a `/docs` folder (or a `gh-pages` branch), enable Pages in repo settings, and you have a live U R L.

```bash
mkdir docs
echo '<h1>Dami — A I Portfolio</h1>' > docs/index.html
git add docs/index.html
git commit -m "Add portfolio landing page"
git push
```

Then go to Settings, Pages, choose the branch and `/docs` folder, and save.

## Make it easy to read

Use headings, short paragraphs, and code blocks people can copy. Add badges for build status or license. Include a screenshot or a GIF — a picture of your project running is worth a thousand words.

## Your task

Pick your strongest project, rewrite its README with the structure above, pin it on GitHub, and publish a one-page portfolio with GitHub Pages.
