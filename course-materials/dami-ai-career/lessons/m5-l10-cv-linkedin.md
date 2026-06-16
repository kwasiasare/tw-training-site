---
course: dami-ai-career
title: CV & LinkedIn for AI roles
month: 5
monthTitle: Polish, Deploy, Go Public
lesson: 10
summary: Turn your projects and maths background into a sharp, keyword-aware CV and LinkedIn profile that
  passes screens and lands AI interviews.
objectives:
- Structure a one-page CV that an AI recruiter and ATS can both read
- Translate your maths degree and support internship into relevant strengths
- Write impact bullets using the action-plus-metric formula
- Tailor keywords to a job description without keyword stuffing
- Optimise a LinkedIn headline, About section, and Featured projects
- Link a clean GitHub and portfolio that back up every claim
- Avoid the common mistakes that get early-career CVs rejected
video: m5-l10-cv-linkedin.mp4
quiz:
- q: What does ATS stand for, and why does it matter for your CV?
  answer: Applicant Tracking System — software that parses and ranks CVs before a human sees them, so
    layout and keywords must be machine-readable.
  why: Many AI-role applications are filtered by an ATS first; a fancy multi-column or image-based CV
    can be parsed into garbage and rejected automatically.
- q: Which bullet is strongest on an AI CV?
  options:
  - Worked on a machine learning project
  - Built a churn model in Python with scikit-learn, reaching 0.89 ROC-AUC on held-out data
  - Responsible for data and modelling tasks
  - Interested in AI and passionate about data
  answer: 1
  why: It names the action, the tools, and a concrete metric — recruiters and hiring managers can instantly
    judge the impact.
- q: Where should your most important keywords and projects appear?
  options:
  - Only in a skills list at the bottom
  - Near the top, in the summary and first project
  - Hidden in white text for the ATS
  - In the cover letter only
  answer: 1
  why: Recruiters skim top-down for seconds; the top third of the CV must carry your headline skills and
    best project, and hidden white text is a trick that gets you blacklisted.
- q: True or false — you should send the same CV to every AI job.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Tailor the summary, skills order, and project emphasis to each job description so the relevant
    keywords and strengths surface first.
- q: Name two things a strong LinkedIn headline for an aspiring AI engineer should do.
  answer: State the target role or direction (e.g. Aspiring ML Engineer) and signal concrete skills or
    evidence (Python, building NLP projects) rather than just a job title.
  why: The headline is searchable and is the first thing recruiters see; a specific, skill-rich headline
    appears in more searches and reads as credible.
- q: Why should every claim on your CV map to something a recruiter can verify?
  answer: Because interviewers probe your CV; a GitHub repo, demo link, or metric you can explain proves
    the claim and protects you from being caught out.
  why: Unverifiable buzzwords invite tough questions; linked, explainable evidence turns claims into a
    credible, interview-winning story.
resources:
- label: Google Technical Writing & resume guidance — Tech Resume Inside Out (Gergely Orosz)
  url: https://thetechresume.com/
- label: LinkedIn Help — Optimise your profile for search and recruiters
  url: https://www.linkedin.com/help/linkedin
- label: Harvard Extension School — Resume and Cover Letter Guide
  url: https://www.extension.harvard.edu/resources/career-resources/
- label: GitHub Docs — About your profile README
---

## Why your CV is a data pipeline

Think of an application like a pipeline. Your CV is the input, an **ATS** (Applicant Tracking System) often parses it first, a recruiter skims it for seconds, and only then does a hiring manager read it carefully. If any stage chokes, you never reach an interview. Your job is to make every stage flow.

As a maths graduate moving into AI, you have a real edge: rigour, probability, linear algebra, and proof-level thinking. The CV's job is to make that edge **obvious and relevant** to an AI role.

## Structure that survives an ATS

Keep it **one page**, single column, plain fonts, real text (never an image of text). A clean order works best:

1. **Name + contact + links** (GitHub, LinkedIn, portfolio).
2. **Summary** — two lines: who you are, your direction, your strongest evidence.
3. **Skills** — grouped: languages, ML/data, tools.
4. **Projects** — your strongest first, with metrics.
5. **Experience** — your L1 support internship, framed for impact.
6. **Education** — your maths degree.

Avoid tables, text boxes, and multi-column layouts — many parsers scramble them.

## Impact bullets: action + tool + metric

Weak bullets describe duties. Strong bullets describe **impact**. Use the formula: *action verb -> what you built -> with which tools -> measurable result*.

```text
Weak:   Worked on a machine learning model for customer data.
Strong: Built a churn classifier in Python (scikit-learn);
        reached 0.89 ROC-AUC and shipped it behind a FastAPI endpoint.
```

Numbers can be model metrics, dataset size, latency, users, or time saved. Even a personal project metric beats a vague verb.

## Tailoring keywords without faking

Read the job description and mirror its real language. If it says "NLP" and "PyTorch", use those exact terms **where they are true**. A quick way to spot overlap is to count which of your skills appear in the posting.

```python
job_desc = open("job.txt").read().lower()
my_skills = ["python", "pytorch", "sql", "nlp", "fastapi", "docker"]
matches = [s for s in my_skills if s in job_desc]
missing = [s for s in my_skills if s not in job_desc]
print("emphasise:", matches)
print("deprioritise:", missing)
```

Lead with the matched skills. Never claim a skill you cannot defend in an interview.

## LinkedIn that recruiters can find

LinkedIn is a search engine. Three fields do the heavy lifting:

- **Headline**: name your target plus concrete skills, e.g. *Aspiring ML Engineer | Python, scikit-learn, NLP | Maths graduate*.
- **About**: a short story — maths foundation, the pivot into AI, two project highlights, what you're looking for.
- **Featured**: pin your best project repo, a demo, or a write-up so claims are clickable.

Fill the Skills section with the exact terms recruiters search, and ask a mentor or peer for one endorsement on each top skill.

## Make every claim verifiable

Interviewers probe what's on the page. Every project should map to a **GitHub repo with a clear README**, ideally a live demo or notebook. Your profile README and pinned repos are part of your CV now.

```bash
git clone https://github.com/you/churn-api
cd churn-api
open README.md   # screenshots, metrics, how to run
```

## Your task

Rewrite your CV to one page with three metric-driven project bullets, then update your LinkedIn headline and Featured section to match.
