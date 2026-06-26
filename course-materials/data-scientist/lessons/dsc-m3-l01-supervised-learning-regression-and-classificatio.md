---
course: data-scientist
title: 'Supervised Learning: Regression and Classification'
month: 3
monthTitle: Machine Learning in Practice
lesson: 1
summary: Learn to train, evaluate, and interpret supervised learning models with scikit-learn. This lesson
  covers linear regression for continuous outcomes and logistic regression for classification, including
  the full workflow from train/test split to metric selection and coefficient interpretation.
objectives:
- Distinguish regression from classification problems and choose the right model for each
- Train linear and logistic regression models using scikit-learn's consistent API
- Evaluate models with appropriate metrics (RMSE, R2, accuracy, precision, recall, ROC-AUC)
- Interpret model coefficients to explain predictions to stakeholders
- Apply train/test splitting and feature scaling to avoid data leakage and overfitting
- Diagnose common pitfalls like imbalanced classes and the accuracy trap
video: dsc-m3-l01-supervised-learning-regression-and-classificatio.mp4
quiz:
- q: Which model would you choose to predict whether a customer will churn (yes/no)?
  options:
  - Linear regression
  - Logistic regression
  - RMSE
  - StandardScaler
  answer: 1
  why: Churn is a binary categorical outcome, so it's a classification task. Logistic regression outputs
    class probabilities, making it the right choice.
- q: Why is accuracy a poor metric when 97% of transactions are legitimate and 3% are fraud?
  options:
  - Accuracy can't be computed on imbalanced data
  - A model predicting 'legitimate' always scores 97% but catches no fraud
  - Accuracy only works for regression
  - Accuracy requires scaled features
  answer: 1
  why: With heavy imbalance, a trivial model that always predicts the majority class gets high accuracy
    while completely failing at the actual goal. Precision, recall, and ROC-AUC are more informative.
- q: What is the main reason to split data into train and test sets BEFORE scaling?
  options:
  - It makes training faster
  - To prevent test-set information from leaking into training
  - Scaling only works on training data
  - To reduce the number of features
  answer: 1
  why: Fitting a scaler on all data lets test statistics influence training, leaking information and producing
    overly optimistic, dishonest performance estimates.
- q: In linear regression, what does a coefficient of 2.5 for a feature mean?
  options:
  - The feature explains 2.5% of variance
  - The target increases by 2.5 units per one-unit increase in that feature, holding others constant
  - The probability of the class is 2.5
  - The model has 2.5 errors
  answer: 1
  why: A linear regression coefficient is the expected change in the target for a one-unit increase in
    that feature, with all other features held fixed.
- q: Name the scikit-learn method that returns predicted class probabilities (rather than hard labels)
    for a classifier.
  answer: predict_proba
  why: predict_proba returns the probability for each class, which you can threshold yourself or feed
    into metrics like ROC-AUC, whereas predict returns hard labels.
- q: Which metric should you prioritize if missing a positive case (a false negative) is very costly,
    such as failing to detect a disease?
  options:
  - Precision
  - Recall
  - R-squared
  - Intercept
  answer: 1
  why: Recall measures the fraction of actual positives the model catches. When false negatives are costly,
    maximizing recall ensures fewer positive cases are missed.
resources:
- label: scikit-learn Supervised Learning User Guide
  url: https://scikit-learn.org/stable/supervised_learning.html
- label: 'scikit-learn Model Evaluation: Metrics'
  url: https://scikit-learn.org/stable/modules/model_evaluation.html
- label: scikit-learn Pipelines and Preprocessing
  url: https://scikit-learn.org/stable/modules/compose.html
- label: 'Google ML Crash Course: Logistic Regression'
  url: https://developers.google.com/machine-learning/crash-course/logistic-regression
---

## What Is Supervised Learning?

Supervised learning trains a model on labeled examples so it can predict labels for new, unseen data. Each row has input **features** (X) and a known **target** (y). The two core flavors are:

- **Regression** predicts a continuous number (e.g., house price, demand, temperature).
- **Classification** predicts a discrete category (e.g., spam vs. not spam, churn vs. retain).

The model learns a mapping `f(X) -> y` by minimizing error on the training data, then we measure how well it generalizes on held-out data.

## The scikit-learn Workflow

Every estimator in scikit-learn follows the same pattern, which makes swapping models trivial:

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)      # learn parameters
preds = model.predict(X_test)    # generate predictions
```

Always split **before** any fitting or scaling so that information from the test set never leaks into training.

## Linear Regression

Linear regression fits a line (or hyperplane) of the form:

```
y = b0 + b1*x1 + b2*x2 + ... + bn*xn
```

The coefficients (`b1...bn`) tell you the expected change in `y` for a one-unit increase in a feature, holding others constant. The intercept `b0` is the predicted value when all features are zero.

**Key evaluation metrics:**

- **RMSE** (Root Mean Squared Error): average prediction error in the target's units; penalizes large errors heavily.
- **MAE** (Mean Absolute Error): average absolute error; more robust to outliers.
- **R²**: proportion of variance explained (0 to 1; higher is better).

```python
from sklearn.metrics import root_mean_squared_error, mean_squared_error, r2_score
import numpy as np

rmse = root_mean_squared_error(y_test, preds)   # sklearn >= 1.4
# equivalent: np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)
```

## Logistic Regression

Despite its name, logistic regression is a **classification** algorithm. It passes a linear combination of features through the **sigmoid function** to output a probability between 0 and 1:

```
p = 1 / (1 + e^-(b0 + b1*x1 + ...))
```

We convert probability to a class using a threshold (default 0.5). Coefficients relate to the **log-odds**: exponentiating a coefficient gives the **odds ratio** for that feature.

```python
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
probs = clf.predict_proba(X_test)[:, 1]
labels = clf.predict(X_test)
```

## Classification Metrics

Accuracy alone is misleading on imbalanced data (the **accuracy trap**). If 95% of emails are not spam, a model that always predicts "not spam" scores 95% but is useless. Use:

- **Precision**: of predicted positives, how many were correct? (TP / (TP+FP))
- **Recall**: of actual positives, how many did we catch? (TP / (TP+FN))
- **F1**: harmonic mean of precision and recall.
- **ROC-AUC**: ranking quality across all thresholds.

```python
from sklearn.metrics import classification_report, roc_auc_score
print(classification_report(y_test, labels))
print(roc_auc_score(y_test, probs))
```

## Feature Scaling and Preprocessing

Linear and logistic models benefit from **standardized** features (mean 0, std 1), especially when using regularization. Use a `Pipeline` to bundle scaling with the model so scaling fits only on training folds:

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
pipe.fit(X_train, y_train)
```

## Interpreting and Communicating Results

A major advantage of linear models is **interpretability**. After scaling, coefficient magnitude indicates relative importance; sign indicates direction. Note that standardized-coefficient magnitude reflects relative importance *only* under low multicollinearity — with correlated features, prefer permutation importance or SHAP. Always translate findings into business language: "Each additional support ticket increases churn odds by 30%." This is what separates a data scientist from a black-box button-pusher.

## Common Pitfalls

- **Data leakage**: fitting scalers/encoders on the full dataset before splitting.
- **Overfitting**: great train scores, poor test scores; add regularization (`C` parameter) or simplify.
- **Ignoring class imbalance**: use `class_weight='balanced'`, resampling, or threshold tuning.
- **Reading too much into correlated features**: collinearity makes individual coefficients unstable.
