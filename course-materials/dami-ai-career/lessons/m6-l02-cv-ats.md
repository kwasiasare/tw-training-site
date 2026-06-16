---
course: dami-ai-career
title: Tailoring CVs & ATS basics
month: 6
monthTitle: Apply & Interview
lesson: 2
summary: Tailor your CV to each role and get past the Applicant Tracking System by mirroring keywords
  and using clean, parseable formatting.
objectives:
- Understand what an Applicant Tracking System (ATS) does and why it matters
- Read a job description and extract the keywords that matter
- Tailor your CV to each role without lying or stuffing
- Use a clean, single-column, parseable CV layout
- Write achievement bullets using the action-metric-result formula
- Position a maths background and L1 support internship for AI roles
- Avoid common formatting traps that break ATS parsing
video: m6-l02-cv-ats.mp4
quiz:
- q: What does an ATS primarily do with your CV?
  options:
  - Reads it like a human recruiter
  - Parses it into structured fields and scores it against the job
  - Auto-rejects anyone without a PhD
  - Posts it publicly online
  answer: 1
  why: An ATS parses your CV into fields (skills, experience, education) and ranks it against the job's
    keywords before a human ever sees it.
- q: Which CV format is safest for ATS parsing?
  options:
  - A two-column PDF with text boxes
  - An image-based PDF
  - A simple single-column document with standard headings
  - A scanned printout
  answer: 2
  why: Single-column text with standard headings (Experience, Education, Skills) parses cleanly; columns,
    text boxes, and images often scramble or get dropped.
- q: What is the best source for the keywords you should put in your CV?
  options:
  - A generic keyword list online
  - The specific job description you are applying to
  - Your favourite buzzwords
  - The company's stock price
  answer: 1
  why: Each job description names the exact skills and tools the employer screens for; mirror that role's
    language rather than a generic list.
- q: Why is keyword stuffing (repeating terms unnaturally) a bad idea?
  answer: It reads as spam to humans, can be flagged, and does not demonstrate real evidence of the skill.
  why: Modern ATS and recruiters look for context and evidence; cramming keywords without achievements
    fails the human review even if it passes parsing.
- q: Give one strong way to phrase a CV achievement bullet.
  answer: Use action verb + what you did + measurable result, e.g. 'Automated weekly ticket report with
    Python, cutting manual work by 3 hours.'
  why: The action-metric-result formula turns vague duties into evidence and naturally includes role keywords.
- q: How many distinct CV versions should you ideally keep?
  options:
  - One CV for every job
  - A master CV plus a tailored version per role
  - A new CV written from scratch each time
  - None — use LinkedIn only
  answer: 1
  why: Keep one master CV with everything, then cut and reorder it into a tailored version for each role
    — fast and consistent.
resources:
- label: Harvard FAS Resume & Cover Letter Guide (PDF)
  url: https://careerservices.fas.harvard.edu/resources/bullet-point-resume-template/
- label: Jobscan — How ATS works and CV keyword matching
  url: https://www.jobscan.co/applicant-tracking-systems
- label: Google reStructured CV / Google XYZ formula (Laszlo Bock)
- label: The Markdown Resume — plain-text, ATS-friendly templates
  url: https://github.com/there4/markdown-resume
---

## What an ATS actually is

An **Applicant Tracking System (ATS)** is software employers use to collect, parse, and rank job applications. When you upload a CV, the ATS does not read it like a person — it tries to extract structured fields (your name, jobs, dates, skills, education) and then scores how well those fields match the job description.

If your CV is hard to parse, key information gets lost or jumbled before a human ever sees it. So step one is simply: **be parseable**.

## Mirror the job description

Every job description is a free answer key. It tells you the exact tools, skills, and phrases the employer screens for. Your job is to **mirror that language honestly** — if you genuinely have the skill, use the same word the employer used (say "Python" not just "scripting", "SQL" not just "databases").

A quick trick: paste the job description into a script and pull out the most frequent meaningful words.

```python
import re
from collections import Counter

jd = open("job_description.txt", encoding="utf-8").read().lower()
words = re.findall(r"[a-z][a-z+#.]+", jd)
stop = {"and", "the", "with", "you", "for", "our", "to", "of", "in", "a"}
common = [w for w in words if w not in stop and len(w) > 2]

for word, n in Counter(common).most_common(20):
    print(f"{n:>3}  {word}")
```

Then make sure the genuine matches appear in your CV — ideally in a **Skills** section and again as **evidence** inside an achievement bullet.

## Keep the format clean

Fancy layouts break ATS parsing. Two-column designs, text boxes, tables, images, and headers/footers often get scrambled or dropped. Use a **single-column** layout, standard section headings, and a normal font.

Write your CV in a plain format you control, like Markdown, then export to PDF:

```bash
# Convert a clean markdown CV to PDF with pandoc
pandoc cv.md -o cv.pdf --pdf-engine=xelatex
```

Use standard headings the ATS expects: **Experience**, **Education**, **Skills**, **Projects**. Save the file with your name, e.g. `Dami-Adeyemi-CV.pdf`.

## Write achievement bullets, not duties

Don't list what you were *responsible for* — show what you *achieved*. Use the formula **action verb + what you did + measurable result**.

- Weak: "Responsible for handling support tickets."
- Strong: "Resolved 40+ L1 support tickets per week, automating the weekly report in Python and saving 3 hours."

The strong version naturally includes keywords (Python, support) and gives evidence a number proves.

## Position your maths + support story

You are not "just" a maths graduate with a support internship — that's a strong, in-demand combination. Maths signals **statistics, linear algebra, and rigour**; L1 support signals **debugging, communication, and working under pressure**. Frame projects (your course work) as a **Projects** section so a thin work history still shows real, applied AI skills.

## Your task

Take one real job advert, extract its keywords, and produce a **tailored** single-column CV with at least three achievement bullets in the action-metric-result format.
