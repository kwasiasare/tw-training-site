---
title: Job-search strategy & role targeting
month: 6
monthTitle: Apply & Interview
lesson: 1
summary: 'Plan a focused job search: pick the right AI roles, read job descriptions critically, and build
  a pipeline you can track.'
objectives:
- Distinguish ML engineer, data scientist, AI engineer and applied AI roles
- Map your maths and L1 support background onto realistic entry points
- Decode a job description to separate must-haves from nice-to-haves
- Target roles by seniority, sector and tech stack instead of applying blindly
- Build a simple application tracker and a weekly outreach routine
- Tailor your CV keywords to each job using a repeatable process
video: m6-l01-job-search.mp4
quiz:
- q: You have a maths degree, L1 support experience and six months of Python and ML projects. Which role
    is usually the most realistic first target?
  options:
  - Senior ML research scientist
  - Junior or entry-level AI / data role
  - Head of data
  - Principal engineer
  answer: 1
  why: Entry-level and junior roles match a career-changer with projects but no commercial ML experience;
    senior and principal roles expect years of production work.
- q: In a job description, what does the 'requirements' versus 'nice to have' split tell you?
  answer: Requirements are the must-haves you should largely meet; nice-to-haves are bonus skills, so
    you can apply if you meet most requirements and a few extras.
  why: Treating every bullet as mandatory makes you self-reject. Most candidates are hired without ticking
    every nice-to-have.
- q: Roughly what overlap with the stated requirements is a sensible threshold for applying to an entry-level
    role?
  options:
  - 100 percent
  - About 60 to 70 percent
  - Exactly 50 percent
  - Only apply at 90 percent or more
  answer: 1
  why: Around 60 to 70 percent overlap is a healthy signal; insisting on 100 percent means you apply far
    too little and miss roles you could grow into.
- q: Why tailor CV keywords to each specific job description?
  answer: Many employers use applicant tracking systems and keyword screens, so matching the language
    of the JD helps your CV pass filters and shows relevance.
  why: An A T S and a busy recruiter both scan for the exact skills named in the posting; mirroring that
    language increases your hit rate.
- q: Which is the better weekly habit for a 30-hour-a-week job seeker?
  options:
  - Send 50 generic applications in one burst
  - A steady routine of fewer, tailored applications plus outreach
  - Wait for recruiters to find you
  - Only apply when you feel fully qualified
  answer: 1
  why: A consistent pipeline of tailored applications and direct outreach converts far better than mass
    generic spraying or passive waiting.
- q: What is the main purpose of an application tracker?
  answer: To record every role, its status and next action so you follow up on time, spot what is working
    and avoid duplicate or forgotten applications.
  why: A tracker turns a chaotic search into a measurable pipeline you can review and improve each week.
resources:
- label: LinkedIn Jobs — search and set role alerts
  url: https://www.linkedin.com/jobs/
- label: UK Government — National Careers Service job profiles
  url: https://nationalcareers.service.gov.uk/
- label: Levels.fyi — compare tech and AI role titles and pay
  url: https://www.levels.fyi/
- label: Cracking the Coding Interview (Gayle Laakmann McDowell) — Behavioural and process chapters
---

## Why strategy beats volume

A job search without a strategy means sending hundreds of generic applications and hearing nothing back. With only about thirty hours a week, you cannot out-spam the market — but you can out-target it. The goal of this lesson is a **focused pipeline**: the right roles, the right framing of your background, and a routine you can sustain.

You are a career-changer: a maths degree, an L1 support internship, and a growing portfolio of coding and machine-learning projects. That is a real, hireable profile — the job is to point it at the roles where it lands.

## Know the role landscape

AI job titles are messy and overlap. A few common buckets:

- **Data Scientist** — statistics, experiments, modelling, communicating insight.
- **Machine Learning Engineer** — building, training and shipping models in production.
- **AI / Applied AI Engineer** — wiring large language models and APIs into products.
- **Data / Analytics Engineer** — pipelines, SQL and the data plumbing underneath.

Your maths gives you an edge on the statistics-heavy roles; your support background gives you an edge anywhere that values communication and debugging under pressure. Target **junior** or **entry-level** versions first.

## Decode the job description

Most beginners self-reject by treating every bullet as mandatory. Read each posting in three passes: the **must-haves** (the requirements), the **nice-to-haves**, and the **signals** (sector, stack, team size). A useful rule of thumb: if you meet roughly sixty to seventy percent of the requirements, apply.

You can even score the overlap programmatically to keep yourself honest:

```python
jd_keywords = {"python", "sql", "pandas", "machine learning", "git", "aws"}
my_skills   = {"python", "sql", "pandas", "machine learning", "git"}

overlap = my_skills & jd_keywords
score = len(overlap) / len(jd_keywords)
print(f"Match: {score:.0%}  Missing: {jd_keywords - my_skills}")
# Match: 83%  Missing: {'aws'}
```

If you are at sixty percent or more, apply and name the one or two gaps as things you are actively learning.

## Build a trackable pipeline

Treat applications like a dataset. Capture every role, its status and the next action so nothing falls through the cracks. A spreadsheet works, but a tiny script keeps it consistent:

```bash
# one CSV per week; columns you actually review
echo "company,role,date_applied,status,next_action,follow_up_date" > applications.csv
echo "Acme,Junior Data Scientist,2026-06-15,applied,follow up,2026-06-22" >> applications.csv
cat applications.csv
```

Each week, review the tracker: which sources and which framings get replies? Double down on what works and drop what does not.

## A sustainable weekly routine

With thirty hours, protect a fixed rhythm: a block for **finding and tailoring** applications, a block for **outreach** (messaging people at target companies), and a block for **interview prep and projects**. Aim for a small number of well-tailored applications plus a few genuine messages each week, not a one-off burst of generic ones. Consistency compounds.
