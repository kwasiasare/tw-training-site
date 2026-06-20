---
course: data-scientist
title: Model Evaluation and Validation
month: 3
monthTitle: Machine Learning in Practice
lesson: 2
summary: Learn to measure model performance honestly using train-test splits, cross-validation, and the
  right metrics so you can detect and prevent overfitting before deploying to production.
objectives:
- Explain why a held-out test set is essential and how data leakage undermines evaluation
- Apply train-test splits and k-fold cross-validation correctly in scikit-learn
- Select appropriate metrics (accuracy, precision, recall, F1, ROC-AUC) for a given problem
- Interpret ROC and precision-recall curves to compare classifiers
- Diagnose overfitting vs underfitting using train/validation performance gaps
- Use stratification and pipelines to avoid common validation mistakes
video: dsc-m3-l02-model-evaluation-and-validation.mp4
quiz:
- q: Why is stratification important when splitting data for classification?
  options:
  - It speeds up model training
  - It preserves the class proportions in each split
  - It removes outliers automatically
  - It scales the features
  answer: 1
  why: Stratification keeps the same class balance in train and test sets, which is especially important
    for imbalanced datasets so each split is representative.
- q: 'A model scores 0.98 on training data but 0.71 on the validation set. This indicates:'
  options:
  - Underfitting
  - Overfitting
  - Perfect generalization
  - Data leakage from test to train
  answer: 1
  why: A large gap between high training performance and lower validation performance is the classic signature
    of overfitting.
- q: Which metric is most misleading on a heavily imbalanced dataset?
  options:
  - Recall
  - Precision
  - Accuracy
  - ROC-AUC
  answer: 2
  why: Accuracy can be very high simply by predicting the majority class, hiding poor performance on the
    minority class.
- q: What does an ROC-AUC of 0.5 mean?
  options:
  - Perfect classifier
  - Random guessing
  - High precision
  - Severe overfitting
  answer: 1
  why: An AUC of 0.5 means the model performs no better than random chance at ranking positives above
    negatives.
- q: In one sentence, why should preprocessing be inside a cross-validation pipeline?
  answer: So that transformations like scaling are fit only on training folds, preventing data leakage
    and giving honest performance estimates.
  why: Fitting preprocessing on the full dataset lets information from validation folds leak into training,
    inflating scores.
- q: Name a situation where recall should be prioritized over precision.
  answer: Fraud or disease detection, where missing a true positive is far costlier than a false alarm.
  why: When false negatives carry high cost, maximizing recall ensures more true positives are caught
    even at the expense of some false positives.
resources:
- label: 'scikit-learn: Cross-validation guide'
  url: https://scikit-learn.org/stable/modules/cross_validation.html
- label: 'scikit-learn: Model evaluation metrics'
  url: https://scikit-learn.org/stable/modules/model_evaluation.html
- label: 'Google ML Crash Course: Classification (ROC & AUC)'
  url: https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc
---

## Why Evaluation Matters

A model that scores 99% on the data it was trained on may be useless on new data. The whole point of machine learning is **generalization** — performing well on data the model has never seen. Honest evaluation is how we estimate that future performance before committing to production.

## Train-Test Split

The simplest approach: hold out a portion of data (commonly 20-30%) that the model never sees during training. We train on the rest and evaluate on the held-out test set.

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
```

- `random_state` makes the split reproducible.
- `stratify=y` preserves class proportions — critical for imbalanced data.

**Never** let test data influence training, feature scaling, or feature selection. That is **data leakage** and produces overly optimistic scores.

## Cross-Validation

A single split can be lucky or unlucky. **K-fold cross-validation** splits data into k parts, trains on k-1 and validates on the remaining fold, rotating through all folds and averaging the results.

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
print(scores.mean(), scores.std())
```

- Use **StratifiedKFold** for classification to keep class balance per fold.
- More folds = lower bias, higher variance and cost. 5 or 10 are typical.
- For time-series, use `TimeSeriesSplit` — never shuffle temporal data.

## Choosing Metrics

**Accuracy** = correct predictions / total. It is misleading when classes are imbalanced (99% accuracy by always predicting the majority class).

For classification, use the **confusion matrix** to derive:

- **Precision** = TP / (TP + FP) — of predicted positives, how many were right.
- **Recall (sensitivity)** = TP / (TP + FN) — of actual positives, how many we caught.
- **F1** = harmonic mean of precision and recall.

The choice depends on cost: fraud detection prioritizes recall; spam filtering may prioritize precision.

## ROC-AUC

The **ROC curve** plots true positive rate vs false positive rate across all classification thresholds. The **AUC** (area under the curve) summarizes it in one number:

- 0.5 = random guessing, 1.0 = perfect.
- AUC is threshold-independent and robust to class proportion shifts.
- For heavily imbalanced data, the **precision-recall curve (PR-AUC)** is often more informative.

```python
from sklearn.metrics import roc_auc_score, roc_curve
y_proba = model.predict_proba(X_test)[:, 1]
print(roc_auc_score(y_test, y_proba))
```

## Diagnosing Over/Underfitting

- **Overfitting**: high training score, much lower validation score. Fix with more data, regularization, simpler models, or fewer features.
- **Underfitting**: low scores on both. Fix with more complex models or better features.
- A **validation curve** or **learning curve** visualizes these gaps.

## Pipelines Prevent Leakage

Wrap preprocessing and the model in a `Pipeline` so transformations are fit only on training folds during cross-validation.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
pipe = make_pipeline(StandardScaler(), model)
cross_val_score(pipe, X, y, cv=5, scoring='roc_auc')
```

This ensures the scaler never sees validation data, giving trustworthy estimates.
