---
course: data-scientist
title: 'Mini-Project: End-to-End Predictive Model'
month: 3
monthTitle: Machine Learning in Practice
lesson: 4
summary: 'In this hands-on mini-project, you build a complete machine learning pipeline from raw data
  to a tuned, evaluated, and documented model. You''ll practice the full workflow data scientists use
  in production: framing the problem, cleaning and splitting data, engineering features, training baselines,
  tuning hyperparameters with cross-validation, evaluating against business-relevant metrics, and documenting
  your results for stakeholders.'
objectives:
- Frame a predictive problem and select an evaluation metric aligned with the business goal
- Construct a leak-free preprocessing and modeling pipeline using scikit-learn
- Establish a baseline model and iteratively improve it with feature engineering and hyperparameter tuning
- Evaluate models with cross-validation and an untouched test set using appropriate metrics
- Document model performance, assumptions, and limitations in a reproducible report
video: dsc-m3-l04-mini-project-end-to-end-predictive-model.mp4
quiz:
- q: Why should you split your data into train and test sets before doing exploratory data analysis?
  options:
  - To make the code run faster
  - To prevent information from the test set leaking into modeling decisions
  - Because scikit-learn requires it
  - To reduce the dataset size
  answer: 1
  why: Exploring or fitting on the full dataset lets test-set information influence your choices, leaking
    information and inflating performance estimates. Splitting first keeps the test set an honest final
    check.
- q: On an imbalanced churn dataset where you act on the top-ranked customers, which metric is most appropriate?
  options:
  - Accuracy
  - R-squared
  - ROC-AUC / precision@k
  - Mean squared error
  answer: 2
  why: With class imbalance and a ranking-based action, accuracy is misleading. ROC-AUC and precision@k
    reflect how well the model ranks and identifies the at-risk customers you actually target.
- q: What is the main benefit of wrapping preprocessing inside a scikit-learn Pipeline before cross-validation?
  options:
  - It automatically tunes hyperparameters
  - It guarantees a higher accuracy
  - Transformers are fit only on each training fold, preventing leakage
  - It removes the need for a test set
  answer: 2
  why: A Pipeline ensures imputers, scalers, and encoders are fit within each CV training fold, so statistics
    from validation folds never leak into training, giving unbiased estimates.
- q: Why establish a simple baseline model before building complex ones?
  options:
  - Baselines always outperform complex models
  - It provides a reference point to judge whether added complexity improves results
  - It is required for cross-validation
  - Baselines do not need hyperparameter tuning
  answer: 1
  why: A baseline gives context. If a complex model can't beat a dummy or logistic regression, the added
    complexity isn't justified.
- q: Name one essential item you should include in a model card to make results reproducible.
  answer: 'Pinned dependencies / random seeds / saved pipeline (any of: data source, metrics, limitations,
    seeds)'
  why: Reproducibility requires documenting things like the data source, the metric, pinned dependency
    versions, fixed random seeds, and the saved fitted pipeline so others can recreate your results.
- q: What mistake does tuning hyperparameters using the test set cause?
  answer: It causes data leakage and an overly optimistic, unreliable performance estimate
  why: Using the test set during tuning means it no longer provides an unbiased estimate; the reported
    performance will be inflated and won't reflect real-world results.
resources:
- label: 'scikit-learn: Pipelines and composite estimators'
  url: https://scikit-learn.org/stable/modules/compose.html
- label: 'scikit-learn: Cross-validation and hyperparameter tuning'
  url: https://scikit-learn.org/stable/modules/grid_search.html
- label: 'Google: Model Cards for responsible reporting'
  url: https://modelcards.withgoogle.com/about
- label: 'scikit-learn: Common pitfalls and data leakage'
  url: https://scikit-learn.org/stable/common_pitfalls.html
---

## Project Overview

This mini-project takes you through a complete supervised learning workflow. The goal is not just a high score but a **reproducible, leak-free, well-documented pipeline** you could hand to a colleague or deploy.

We'll use a tabular classification example (predicting customer churn), but the workflow applies equally to regression.

## Step 1 — Frame the Problem

Before writing code, answer:

- **What are we predicting?** Binary churn (yes/no) in the next 30 days.
- **Why does it matter?** Retention team wants a ranked list of at-risk customers to target.
- **What metric matters?** Because we rank customers and act on the top ones, **ROC-AUC** and **precision@k** matter more than raw accuracy (the classes are imbalanced).

> A clear problem statement determines your metric, your train/test strategy, and what "good enough" means.

## Step 2 — Split First, Then Explore

Split the data **before** any analysis to avoid leakage. Use a stratified split to preserve class balance.

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)
```

Do all EDA on the training set only. The test set is a one-time final check.

## Step 3 — Build a Leak-Free Pipeline

Wrap preprocessing and the model in a single `Pipeline`. Fit transformers (imputers, scalers, encoders) **inside** cross-validation folds so test-fold statistics never leak into training.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

num = ['tenure', 'monthly_charges']
cat = ['contract', 'payment_method']

pre = ColumnTransformer([
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')),
                      ('sc', StandardScaler())]), num),
    ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                      ('oh', OneHotEncoder(handle_unknown='ignore'))]), cat),
])

clf = Pipeline([('pre', pre),
                ('model', RandomForestClassifier(random_state=42))])
```

## Step 4 — Baseline First

Always establish a simple baseline (e.g., `DummyClassifier`, logistic regression) before complex models. It tells you whether sophistication is buying you anything.

```python
from sklearn.model_selection import cross_val_score
import numpy as np
scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='roc_auc')
print(f'CV AUC: {scores.mean():.3f} +/- {scores.std():.3f}')
```

## Step 5 — Tune Hyperparameters

Use cross-validation inside the search. `RandomizedSearchCV` is usually more efficient than exhaustive grid search.

```python
from sklearn.model_selection import RandomizedSearchCV
param_dist = {
    'model__n_estimators': [200, 400, 600],
    'model__max_depth': [None, 8, 16, 24],
    'model__min_samples_leaf': [1, 2, 4],
}
search = RandomizedSearchCV(clf, param_dist, n_iter=20, cv=5,
                            scoring='roc_auc', random_state=42, n_jobs=-1)
search.fit(X_train, y_train)
print(search.best_params_, search.best_score_)
```

## Step 6 — Final Evaluation

Evaluate the **best** model once on the held-out test set. Report multiple metrics and a confusion matrix.

```python
from sklearn.metrics import roc_auc_score, classification_report
best = search.best_estimator_
proba = best.predict_proba(X_test)[:, 1]
print('Test AUC:', roc_auc_score(y_test, proba))
print(classification_report(y_test, best.predict(X_test)))
```

Inspect feature importances or SHAP values to explain drivers of churn.

## Step 7 — Document & Reproduce

Write a short model card:

- **Problem & metric**
- **Data**: source, date, size, known biases
- **Approach**: pipeline steps, model, tuning
- **Results**: CV vs test metrics, confusion matrix
- **Limitations**: assumptions, where it may fail, monitoring plan

Pin dependencies (`requirements.txt`), set random seeds, and save the fitted pipeline with `joblib.dump` so results are reproducible.

## Common Pitfalls

- Fitting scalers/encoders on the full dataset (data leakage)
- Tuning on the test set
- Reporting accuracy on imbalanced data
- Forgetting to set `random_state`
- No baseline to compare against
