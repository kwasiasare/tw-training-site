---
course: data-scientist
title: Building Your Data Science Portfolio
month: 7
monthTitle: Capstone & Career Launch
lesson: 2
summary: 'One capstone is good; a small, deliberate portfolio of two or three projects is what convinces
  a hiring manager. This lesson shows how to assemble a coherent portfolio with a clear narrative: a flagship
  end-to-end project, a focused analysis or experiment, and at least one GenAI or LLM project from Module
  5, each backed by a clean GitHub repo, a reproducible notebook, a live demo where possible, and a short
  write-up. You will learn how to structure repos and READMEs so a reviewer can verify your work in seconds,
  how to use Streamlit and Streamlit Community Cloud to make models interactive, and how to build a credible
  GitHub and Kaggle presence. The goal is a portfolio that reads as evidence, not as a list of tutorials
  you followed.'
objectives:
- Choose two to three projects that together tell a coherent data science story
- Structure each project as a clean GitHub repo with a reproducible notebook and a strong README
- Publish at least one interactive demo using Streamlit or Streamlit Community Cloud
- Include one GenAI or LLM project (for example a minimal RAG app) from Module 5
- Write a concise project write-up that leads with the problem and the impact
- Build a credible GitHub and Kaggle presence that recruiters can find and trust
video: dsc-m7-l02-building-your-data-science-portfolio.mp4
quiz:
- q: What makes a data science portfolio genuinely persuasive rather than just a list of projects?
  options:
  - The largest possible number of half-finished notebooks
  - A small set of complete projects with a clear narrative, reproducible repos, and demonstrable results
    a reviewer can verify
  - Only a certification badge with no projects
  - Forking popular repos without changing them
  answer: 1
  why: Hiring managers value depth and verifiability over volume. Two or three complete, reproducible
    projects with a clear story and results someone can run prove capability far better than a long list
    of shallow or copied notebooks.
- q: Why should at least one portfolio project be a GenAI or LLM project, such as a minimal RAG application?
  options:
  - Because LLMs have made classical machine learning obsolete
  - Because 2026 data science roles increasingly expect familiarity with LLM APIs, embeddings, and retrieval,
    and a small RAG project demonstrates that range
  - Because GenAI projects require no evaluation
  - Because it lets you avoid showing any SQL or statistics
  answer: 1
  why: By 2026 most data science teams touch LLMs somewhere in their stack. A focused project that calls
    an LLM API, builds embeddings, and grounds answers in retrieved context shows you can work with the
    modern toolset, while your other projects still prove classical rigor.
- q: What is the single most important quality of a portfolio GitHub repository?
  options:
  - That it contains thousands of commits
  - That the README is written in a rare language
  - That a reviewer can clone it and reproduce the result by following the README
  - That the notebooks have no comments so they look clean
  answer: 2
  why: Reproducibility is the trust signal. A repo with a clear README, a requirements or environment
    file, and code that runs end to end demonstrates rigor; one that cannot be reproduced undermines even
    impressive-looking results.
- q: Why publish an interactive demo with a tool like Streamlit instead of only sharing a notebook?
  options:
  - Because notebooks cannot contain charts
  - Because a hosted, clickable demo lets a non-technical reviewer experience the model in seconds without
    setting up Python
  - Because Streamlit trains models faster than scikit-learn
  - Because demos remove the need for a README
  answer: 1
  why: A live Streamlit app (for example on Streamlit Community Cloud) turns a static notebook into something
    a recruiter or hiring manager can actually use from a browser, which dramatically increases the odds
    they engage with your work.
- q: How should a project write-up be structured to be most effective?
  options:
  - Lead with the problem and the impact, then summarize approach, results, and limitations
  - Open with a full dump of every hyperparameter you tried
  - Start with your life story and end with the dataset license
  - Only include the final accuracy number with no context
  answer: 0
  why: A reader decides in the first lines whether to keep going. Leading with the business problem and
    the quantified impact, then briefly covering approach, results, and honest limitations, respects the
    reader's time and frames the work as outcome-driven.
- q: In two to four sentences, describe the three-project portfolio you would assemble and the single
    story they should tell together.
  answer: 'I would lead with a flagship end-to-end project, for example a churn-prediction model with
    EDA, a tracked modeling workflow, a quantified revenue-retention impact, and a Streamlit demo. Second,
    a focused analysis or experiment, such as an A/B test write-up or a SQL-driven cohort analysis, to
    show statistical and querying depth. Third, a GenAI project from Module 5, a minimal RAG app that
    answers questions over a document set, to show I can work with LLM APIs and embeddings. Together they
    should say one thing: I can take a business question from data to a decision, validate it statistically,
    and work with both classical and modern tooling. Each links to a clean repo and, where possible, a
    live demo.'
  why: A strong answer names three complementary projects (end-to-end ML, statistical depth, and modern
    GenAI), ties them to a single positioning narrative, and points at reproducible evidence. That breadth-with-a-throughline
    is exactly what reassures a hiring manager that the candidate is well-rounded, not a one-trick portfolio.
resources:
- label: 'GitHub: managing your profile README (build a portfolio landing page)'
  url: https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
- label: 'Streamlit Community Cloud: deploy and share apps for free'
  url: https://streamlit.io/cloud
- label: 'Kaggle: competitions, datasets, and public notebooks'
  url: https://www.kaggle.com/
- label: 'Cookiecutter Data Science: a standardized, reproducible project structure'
  url: https://cookiecutter-data-science.drivendata.org/
---

## Why a Portfolio Beats a Resume Bullet

A resume claims; a portfolio proves. When a hiring manager can click into a clean repo, read a crisp write-up, and run a live demo, the question shifts from "can this person do the work?" to "when can they start?" The goal of this lesson is not to produce a pile of notebooks. It is to assemble two or three deliberate projects that, together, tell one coherent story about the kind of data scientist you are. Depth and verifiability beat volume every time, three complete, reproducible projects outperform a dozen abandoned tutorials.

## Choose Two to Three Projects With a Throughline

The strongest portfolios are curated, not accumulated. A reliable structure is:

- **A flagship end-to-end project.** This is your Module 7 capstone: a real business problem taken from framing through modeling to quantified impact and a serving demo. It anchors the portfolio and demonstrates the full workflow.
- **A focused analysis or experiment.** Something narrower that shows statistical and querying depth, an A/B test write-up with a clear hypothesis and confidence intervals, or a SQL-driven cohort analysis answering a sharp business question. This proves you are not only a model-fitter but an analyst who reasons with data.
- **A GenAI or LLM project.** At least one project from Module 5: a minimal retrieval-augmented generation app that answers questions over a document set using embeddings, or an LLM-assisted data task. In 2026, most data teams touch LLMs somewhere, and this project shows you can work with the modern toolset while your other work proves classical rigor.

The throughline matters more than the count. The three projects should let you say one sentence: *I take a business question from raw data to a validated decision, and I work fluently with both classical ML and modern GenAI tooling.* Curate so every project supports that sentence.

## Structure Each Repo So It Can Be Trusted

Reproducibility is the trust signal that separates a portfolio from a screenshot gallery. Give each project a clean GitHub repo with a predictable structure (the Cookiecutter Data Science layout is a good default):

- A top-level **README** that leads with the problem and the result.
- A `requirements.txt` or environment file so the project installs cleanly.
- A `data/` folder (or a script/link to fetch data you cannot commit) and a `notebooks/` or `src/` folder.
- One **runnable notebook or script** that reproduces the headline result end to end.
- Saved artifacts where relevant, a trained model, the MLflow run, the figures used in the write-up.

The acid test: a stranger clones the repo, follows the README, and reproduces your headline number. If they cannot, the project is a claim, not evidence. Pin your best repositories on your GitHub profile and use a **profile README** as a portfolio landing page that links all three projects under one short positioning statement.

## Make at Least One Project Interactive

A notebook asks the reviewer to set up Python; a hosted demo asks them only to click. **Streamlit** turns a model into a small web app in a few dozen lines, and **Streamlit Community Cloud** hosts it for free straight from your GitHub repo:

```python
import streamlit as st
import joblib

model = joblib.load("model.pkl")
st.title("Churn Risk Estimator")
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly = st.number_input("Monthly charges", 0.0, 200.0, 70.0)

if st.button("Predict"):
    prob = model.predict_proba([[tenure, monthly]])[0, 1]
    st.metric("Churn probability", f"{prob:.0%}")
```

Link the live URL prominently in the README and on your LinkedIn Featured section. A recruiter who can move a slider and watch a prediction change is far more likely to engage than one staring at a static cell. For projects that do not suit a model demo, a clear interactive dashboard (Plotly or a Streamlit page over your analysis) serves the same purpose.

## Write a Short, Outcome-First Write-Up

Each project deserves a one-page write-up, in the README, as a blog post, or both. Structure it for a reader who decides in the first few lines whether to continue:

1. **Problem and impact first.** What decision did this inform, and what was the quantified result?
2. **Approach, briefly.** The data, the key modeling or analysis choices, and why.
3. **Results.** The headline metrics, a figure or two, and what they mean.
4. **Limitations and next steps.** Honest caveats and what you would do with more time.

Leading with impact, not methodology, signals that you understand data science exists to change decisions. Honest limitations build more trust than inflated claims, reviewers have seen enough over-promising portfolios to value candor.

## Build a Credible GitHub and Kaggle Presence

Your profiles are part of the portfolio. On **GitHub**, keep contribution activity visible, write meaningful commit messages, and ensure your pinned repos are your best work, not abandoned experiments. A profile README that frames your focus and links your three projects turns your profile into a one-screen pitch.

**Kaggle** is the most recognized public proving ground for data scientists. You do not need a competition medal to benefit: publish a clean, well-narrated notebook on a public dataset, or enter a beginner-friendly competition to show you can work an end-to-end pipeline under a public benchmark. A polished Kaggle notebook doubles as a portfolio piece and demonstrates you can communicate analysis to a wide audience. Together, an active GitHub and a thoughtful Kaggle presence make you findable and credible before you ever send an application.

## A Concrete Example Portfolio

To make this tangible, here is a three-project set that would impress for an entry-level data scientist. Project one, **Telco Churn Prediction**: a full pipeline on a public churn dataset, gradient boosting at ROC-AUC 0.89, MLflow-tracked runs, a Streamlit demo where a reviewer adjusts tenure and monthly charges to watch the risk score update, and a README that estimates retained revenue. Project two, **Pricing A/B Test Analysis**: a clean notebook that states a hypothesis, computes the required sample size, runs a two-proportion test, reports a 4.2% conversion lift with a confidence interval, and discusses threats to validity, proof that you reason statistically, not just fit models. Project three, **Docs Q&A with RAG**: a minimal retrieval-augmented app that embeds a documentation set, retrieves the top chunks, and grounds an LLM answer, with a short evaluation of where retrieval helps and where it fails. Three projects, three distinct skills, one story, data to decision, validated, with modern tooling. Notice each is scoped to finish in days, not months; depth and polish beat sprawling ambition that never ships.

## Common Pitfalls

- **Quantity over quality.** Ten shallow notebooks read worse than three complete projects.
- **Tutorials in disguise.** A re-run of a famous tutorial with no original framing or data adds nothing; change the question, the data, or the analysis.
- **Dead repos.** A repo that will not install or run actively damages credibility.
- **No narrative.** Projects with no write-up force the reviewer to reverse-engineer your intent, and most will not bother.

Curate ruthlessly, make it reproducible, lead with impact, and link it everywhere. Revisit the portfolio every few weeks: retire your weakest piece as you build something stronger, refresh a README, and keep the live demos running, because a broken demo link is worse than no link at all. A portfolio maintained this way keeps working for you long after you publish it, and it does the selling so your application does not have to.
