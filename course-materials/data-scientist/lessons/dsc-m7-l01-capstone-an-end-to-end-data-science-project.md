---
course: data-scientist
title: 'Capstone: An End-to-End Data Science Project'
month: 7
monthTitle: Capstone & Career Launch
lesson: 1
summary: 'This is the culminating project that ties together everything from the first six modules into
  one portfolio-grade case study. You will take a single business problem all the way from framing and
  data wrangling, through EDA, modeling, and honest evaluation, to a quantified business-impact statement
  and a deployment or serving note that proves the work could run in production. Unlike the Module 4 mini-capstone,
  this project is judged against an explicit rubric and is expected to use the tools you added later:
  MLflow for experiment tracking, and a FastAPI or Streamlit serving artifact so a reviewer can actually
  interact with the model. The deliverable is the single strongest piece of evidence in your portfolio,
  a project that demonstrates judgment, rigor, and the ability to connect a model to a decision.'
objectives:
- Frame an ambiguous business problem into a measurable question with a primary metric, guardrails, and
  a baseline
- 'Run the full workflow end to end: wrangling, EDA, leakage-safe splitting, modeling, and validation'
- Quantify business impact in money or decisions, not just model accuracy
- Track experiments with MLflow so every result is reproducible and comparable
- 'Add a deployment or serving note: a FastAPI endpoint or Streamlit demo a reviewer can run'
- Self-assess the project against an explicit hiring-grade rubric before publishing it
video: dsc-m7-l01-capstone-an-end-to-end-data-science-project.mp4
quiz:
- q: How does this career-launch capstone differ most from a typical course exercise or the earlier mini-capstone?
  options:
  - It requires the highest possible model accuracy and nothing else
  - It is judged end to end on framing, rigor, quantified business impact, and a runnable serving artifact,
    not just a model score
  - It forbids using any library you learned earlier in the course
  - It must be completed without writing a README
  answer: 1
  why: 'A hiring-grade capstone is evaluated as a complete case study: a clearly framed problem, a leakage-safe
    and reproducible workflow, an honest evaluation, a business-impact statement, and a serving artifact
    a reviewer can interact with. Accuracy alone is never the bar.'
- q: Why should a strong capstone include a business-impact statement expressed in money or decisions?
  options:
  - Because hiring managers only read the first sentence
  - Because impact framed as dollars saved, conversions gained, or hours avoided proves you connect a
    model to a decision, which is the core of the job
  - Because it lets you skip reporting model metrics
  - Because business impact is required to import scikit-learn
  answer: 1
  why: Data scientists are paid to change decisions, not to maximize AUC in a vacuum. Translating a metric
    gain into an estimated dollar or operational impact (with stated assumptions) is exactly the judgment
    that separates a hireable project from a Kaggle leaderboard entry.
- q: What is the role of MLflow in this capstone?
  options:
  - To track parameters, metrics, and artifacts so every experiment is logged, comparable, and reproducible
  - To replace cross-validation entirely
  - To deploy the model to Kubernetes automatically
  - To clean the raw data before modeling
  answer: 0
  why: MLflow Tracking records each run's parameters, metrics, and artifacts, so you can compare your
    baseline against later models and a reviewer can reproduce the winning run. It is the evidence layer
    that makes 'my best model scored X' verifiable rather than a claim.
- q: Why add a deployment or serving note (a FastAPI endpoint or Streamlit demo) rather than stopping
    at a notebook?
  options:
  - Because notebooks cannot train models
  - Because a serving artifact is required to compute an ROC-AUC
  - Because a model behind an interface proves the work could reach production and lets a reviewer actually
    use it
  - Because it removes the need to evaluate the model
  answer: 2
  why: A notebook proves you can analyze; a small FastAPI endpoint or a Streamlit app proves the model
    can leave the notebook and serve a prediction someone can click. It is the single artifact that most
    distinguishes a production-minded data scientist from a coursework finisher.
- q: Which practice best protects your capstone's reported metrics from being misleadingly optimistic?
  options:
  - Tuning hyperparameters directly on the test set
  - Imputing missing values using the full dataset before splitting
  - Selecting features by their correlation with the target on all rows at once
  - Splitting into train, validation, and test before any leakage-prone transformation, and touching test
    only once at the end
  answer: 3
  why: Fitting imputers, scalers, encoders, or feature selectors on data that includes validation or test
    rows leaks information and inflates scores. Splitting first and reserving the test set for a single
    final evaluation keeps your reported numbers honest.
- q: In two to four sentences, outline the business-impact paragraph you would write for a churn-prediction
    capstone, including the assumptions you would state.
  answer: 'I would translate the model''s recall and precision into retained customers: for example, at
    a 0.45 threshold the model flags 1,000 at-risk customers per month at 30 percent precision, so a retention
    offer that saves 20 percent of true churners preserves roughly 60 accounts a month. At an average
    annual contract value of 1,200 dollars, that is about 72,000 dollars of retained revenue per year,
    before the cost of the offers. I would state the assumptions explicitly: the precision and recall
    hold on fresh data, the offer''s save rate is an estimate from a small pilot, and the contract value
    is an average rather than a guarantee. Finally I would note that a small A/B test should confirm the
    save rate before claiming the full figure.'
  why: A strong answer converts model metrics into an operational and dollar outcome, shows the arithmetic,
    and is explicit about every assumption (precision holds out of sample, the save rate is estimated,
    the value is an average) plus the experiment that would validate it. That is calibrated, defensible
    impact rather than a hand-wave.
resources:
- label: 'Cookiecutter Data Science: a standardized, reproducible project structure'
  url: https://cookiecutter-data-science.drivendata.org/
- label: 'Google: Rules of Machine Learning (engineering best practices)'
  url: https://developers.google.com/machine-learning/guides/rules-of-ml
- label: MLflow Tracking documentation (log params, metrics, and artifacts)
  url: https://mlflow.org/docs/latest/tracking.html
- label: Streamlit documentation (build an interactive model demo)
  url: https://docs.streamlit.io/
---

## The Project That Gets You Hired

Everything in this course has been building toward one artifact: a complete, end-to-end data science project you can put your name on. The Module 4 mini-capstone taught the workflow; this lesson raises the bar. Now you have MLflow, you have a serving stack from Module 6, and you may have a GenAI component from Module 5. The career-launch capstone is judged the way a hiring manager judges a take-home: not on a single accuracy number, but on whether you framed a real problem, worked rigorously, quantified the impact in business terms, and showed the model could actually run. This is the project a reviewer clicks through in five minutes and decides whether to invite you to an interview.

## Step 1: Frame the Problem Around a Decision

Start with the decision-maker, not the dataset. Write a one-paragraph problem statement that names **who** decides, **what** they decide, the **measurable outcome**, and the **baseline** that outcome stands against. Choose a single **primary metric** tied to the goal (recall for fraud, RMSE for a forecast, ROC-AUC for ranking) and one or two **guardrail metrics** so a win on the primary does not quietly break something else. Define all of this before you explore the data; committing to metrics up front is the single best defense against metric-shopping later.

Pick a problem with a believable business story. "Predict which trial users will convert so sales can prioritize outreach" beats "classify the iris dataset" every time, because the former has a decision attached and the latter does not.

## Step 2: Wrangle and Explore Honestly

Real data is messy, and your handling of that mess is part of what is being assessed. Profile shapes, types, missingness, duplicates, and ranges. Make deliberate, documented decisions about missing values and outliers, and justify each one in a comment or markdown cell. Then **split into train, validation, and test before any leakage-prone transformation**, fit imputers, scalers, and encoders on the training fold only, and reserve the test set for a single final evaluation.

Use EDA to communicate, not to decorate. Produce a handful of figures that each make a point: a distribution that explains a modeling choice, a relationship that motivates a feature, a class imbalance that justifies your metric. Write down three to five concrete insights that directly shape the modeling that follows.

## Step 3: Model From a Baseline, Track With MLflow

Always begin with a **baseline**, a mean prediction, a logistic regression, or a simple rule, so every later model has a floor to beat. Add complexity only when it measurably wins on validation. Tune with cross-validation and keep the test set untouched.

This is where MLflow earns its place. Wrap each experiment in a run and log the parameters, the metrics, and the trained model as an artifact:

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

with mlflow.start_run(run_name="rf_v1"):
    model = RandomForestClassifier(n_estimators=300, max_depth=8)
    model.fit(X_train, y_train)
    auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
    mlflow.log_param("max_depth", 8)
    mlflow.log_metric("val_auc", auc)
    mlflow.sklearn.log_model(model, "model")
```

Now your claim "my best model scored 0.89 AUC" is backed by a logged, comparable, reproducible run instead of a number in a slide. A reviewer can see the baseline, the iterations, and exactly which run won.

## Step 4: Evaluate, Then Translate to Business Impact

Report the primary and guardrail metrics on the held-out test set, with a confidence interval or at least a sense of variance. Inspect your errors: a confusion matrix, the worst mispredictions, a calibration check. Then do the step most candidates skip, **translate the metric into a decision**.

If a churn model lifts recall from 40% to 65% at acceptable precision, estimate how many customers that saves per month and what that is worth at average contract value, stating every assumption. If a demand forecast cuts RMSE by 15%, estimate the inventory or staffing dollars that error reduction frees up. Impact framed in money, conversions, or hours is what proves you connect models to outcomes. Be calibrated: name the assumptions and the experiment (often a small A/B test) that would confirm the figure.

## Step 5: Add a Deployment or Serving Note

A notebook proves analysis; a serving artifact proves the work can leave the notebook. You do not need a full production system, you need evidence. The lightest credible option is a **Streamlit** app that loads the saved model and returns a prediction from user input. A more engineering-flavored option is a small **FastAPI** endpoint that accepts a JSON record and returns a score, optionally containerized with Docker as you learned in Module 6.

```python
from fastapi import FastAPI
import mlflow.sklearn

app = FastAPI()
model = mlflow.sklearn.load_model("models:/churn/Production")

@app.post("/predict")
def predict(features: dict):
    score = model.predict_proba([list(features.values())])[0, 1]
    return {"churn_probability": round(float(score), 4)}
```

Write a short serving note in the README: how to run it, an example request and response, and what you would add for real production (input validation, monitoring, the drift checks from Module 6). That paragraph signals production awareness even in a lab-scale project.

## Step 6: Score Yourself Against the Rubric

Before you publish, grade your own project against the rubric below. Each row is something a reviewer notices:

- **Problem framing (15%)** — a clear decision, primary metric, guardrails, and baseline.
- **Data and EDA (15%)** — documented cleaning, leakage-safe splitting, insightful figures.
- **Modeling (20%)** — baseline first, justified complexity, sound validation, MLflow-tracked runs.
- **Evaluation (15%)** — honest test-set metrics with error analysis and uncertainty.
- **Business impact (15%)** — quantified in money or decisions, assumptions stated.
- **Serving (10%)** — a runnable FastAPI or Streamlit artifact with a serving note.
- **Reproducibility and communication (10%)** — a clean repo, a clear README, code anyone can clone and run.

If any row is weak, fix it before you move on to building your portfolio. A project that scores well on this rubric is the strongest single piece of evidence you will own.

## An Optional GenAI Extension

If your Module 5 work fits the problem, a small GenAI layer can lift the capstone from strong to memorable, as long as it serves the decision rather than decorating it. Two patterns work well. First, an **LLM-assisted feature step**: use a model to turn free text (support tickets, product reviews, call notes) into structured features your classifier can consume, then verify that those derived features actually improve the metric on validation. Second, a **retrieval layer**: ground a short natural-language explanation of each prediction in the customer's own records, so a stakeholder can read why the model flagged an account. Keep it honest. Evaluate the LLM component the way Module 5 taught, ask whether it helps and where it fails, and never let a language model fabricate the numbers your stakeholders will act on. Used judiciously, a GenAI extension shows range, classical rigor paired with modern tooling, inside a single coherent project rather than as a bolted-on gimmick.

## Common Pitfalls

- A high accuracy with no business story, the reviewer cannot tell why the work matters.
- Leakage from fitting transformers before splitting, which makes every metric untrustworthy.
- Skipping the serving artifact, leaving the project feeling academic.
- An unreproducible repo, no requirements file, hard-coded paths, no instructions.

Avoid these and you have not just finished a course exercise, you have built the centerpiece of a portfolio that argues you are ready for the role.
