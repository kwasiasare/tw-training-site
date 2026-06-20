---
course: data-scientist
title: 'Capstone: Full Data Science Project and Portfolio'
month: 4
monthTitle: Experimentation, Visualization, and Capstone
lesson: 4
summary: A practical capstone lesson guiding you through delivering an end-to-end data science project—from
  problem framing and data wrangling to modeling, experimentation, and a polished stakeholder presentation—packaged
  for your portfolio.
objectives:
- Frame a business problem into a measurable data science question with clear success metrics
- 'Execute an end-to-end workflow: data wrangling, EDA, modeling, and validation'
- Design and interpret an experiment (A/B test or offline evaluation) to validate impact
- Communicate results through a stakeholder-ready presentation and reproducible repository
- Assemble the project into a portfolio artifact that demonstrates hiring-relevant skills
video: dsc-m4-l04-capstone-full-data-science-project-and-portfolio.mp4
quiz:
- q: Why should you define your primary and guardrail metrics before exploring the data?
  options:
  - To make the dataset smaller
  - To prevent metric-shopping and keep evaluation honest
  - Because it is required by scikit-learn
  - To avoid writing a README
  answer: 1
  why: Defining metrics up front anchors success criteria to the business goal and prevents choosing whichever
    metric happens to look best after the fact.
- q: What is the main purpose of establishing a baseline model?
  options:
  - To deploy it directly to production
  - To set a performance floor that more complex models must beat
  - To replace cross-validation
  - To avoid doing EDA
  answer: 1
  why: A baseline provides a reference point; complex models are only justified if they outperform it
    on validation data.
- q: Which practice helps prevent data leakage?
  options:
  - Splitting into train/validation/test before leakage-prone transformations
  - Imputing missing values using the full dataset including test
  - Using the target variable to create features
  - Tuning on the test set
  answer: 0
  why: Splitting before transformations ensures information from validation/test sets does not influence
    training, preventing leakage.
- q: When presenting to stakeholders, what should you lead with?
  options:
  - The detailed model architecture
  - The recommendation and expected impact
  - A list of hyperparameters
  - The raw confusion matrix
  answer: 1
  why: Stakeholders care about decisions and impact first; methodology details come later and only as
    needed.
- q: In one short phrase, name the structure recommended for a stakeholder presentation narrative.
  answer: Context, Approach, Findings, Recommendation, Next Steps
  why: This flow moves the audience from situation to action, leading with what matters and ending with
    concrete next steps.
- q: What single quality makes a portfolio repository trustworthy to a reviewer?
  answer: Reproducibility
  why: If a reviewer can clone the repo and run it end to end, it demonstrates rigor and credibility beyond
    just the results shown.
resources:
- label: 'Cookiecutter Data Science: standardized project structure'
  url: https://drivendata.github.io/cookiecutter-data-science/
- label: 'Google: Rules of Machine Learning (best practices)'
  url: https://developers.google.com/machine-learning/guides/rules-of-ml
- label: Trustworthy Online Controlled Experiments (A/B testing guide)
  url: https://experimentguide.com/
- label: How to Write a Good Data Science README
  url: https://github.com/banesullivan/README
---

## Why a Capstone Matters

A capstone is the single most persuasive artifact in a data scientist's portfolio. It proves you can take an ambiguous problem all the way to a decision-ready insight. Unlike coursework, a capstone is judged on completeness, clarity, and impact—not just model accuracy.

## Step 1: Frame the Problem

Start with the stakeholder, not the data. Write a one-paragraph problem statement that answers:

- **Who** is the decision-maker and what decision do they need to make?
- **What** is the measurable outcome (e.g., reduce churn by 5%, improve forecast MAPE)?
- **What** does success look like, and what is the baseline?

Define a primary metric and one or two guardrail metrics before touching the data. This prevents metric-shopping later.

## Step 2: Data Wrangling

Real data is messy. Document every cleaning decision in code and comments so the pipeline is reproducible.

- Profile the data: shapes, types, missingness, duplicates, ranges.
- Handle missing values deliberately (impute, drop, or flag) and justify the choice.
- Engineer features tied to domain logic, not just statistical convenience.
- Create a clean train/validation/test split **before** any leakage-prone transformations.

## Step 3: Exploratory Data Analysis

EDA builds intuition and surfaces risks. Use visualizations to communicate, not decorate.

- Univariate distributions and outlier checks.
- Relationships between candidate features and the target.
- Document 3-5 concrete insights that shape your modeling choices.

## Step 4: Modeling

- Establish a **baseline** (mean prediction, logistic regression, or a simple heuristic).
- Iterate to more complex models only if they beat the baseline on validation.
- Tune hyperparameters with cross-validation; avoid touching the test set until the end.
- Evaluate with metrics aligned to the business goal (e.g., precision/recall, AUC, RMSE) and inspect errors.

## Step 5: Experimentation

Validate that your model or intervention actually moves the metric.

- For online settings, design an **A/B test**: define hypothesis, randomization unit, sample size, and significance level.
- For offline settings, use a held-out test set or backtesting and report confidence intervals.
- Be explicit about assumptions and threats to validity (selection bias, leakage, seasonality).

## Step 6: Communicate to Stakeholders

Translate technical work into a decision narrative:

- Lead with the recommendation and expected impact, not the methodology.
- Use a structure: Context → Approach → Findings → Recommendation → Next Steps.
- Quantify uncertainty honestly; stakeholders trust calibrated confidence.

## Step 7: Package for Portfolio

- A clean GitHub repo with a clear README, requirements file, and runnable notebooks/scripts.
- A short write-up or blog post summarizing the problem and impact.
- A slide deck or recorded walkthrough for non-technical audiences.
- Reproducibility: anyone should be able to clone and run your project.

## Common Pitfalls

- Skipping the baseline and over-engineering models.
- Data leakage from improper splitting or target-derived features.
- Presenting accuracy without business context.
- A repo that no one can reproduce.
