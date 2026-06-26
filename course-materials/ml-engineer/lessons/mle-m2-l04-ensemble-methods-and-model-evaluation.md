---
course: ml-engineer
title: Ensemble Methods and Model Evaluation
month: 2
monthTitle: Core Machine Learning Algorithms
lesson: 4
summary: This lesson teaches how ensemble methods—random forests and gradient boosting—combine many weak
  learners into strong predictive models, and how to rigorously evaluate them using cross-validation and
  metrics like ROC-AUC. You will learn the bias-variance intuition behind bagging and boosting, key hyperparameters,
  and a practical workflow to optimize a classifier.
objectives:
- Explain the difference between bagging (random forests) and boosting (gradient boosting) and when to
  use each.
- Train random forest and gradient boosting classifiers in scikit-learn with sensible hyperparameters.
- Use k-fold and stratified cross-validation to obtain reliable performance estimates.
- Select and interpret evaluation metrics including accuracy, precision, recall, F1, and ROC-AUC.
- Tune hyperparameters with grid/randomized search to optimize a model without overfitting.
- Interpret feature importance to understand model behavior.
video: mle-m2-l04-ensemble-methods-and-model-evaluation.mp4
quiz:
- q: What is the primary effect of bagging (as in random forests)?
  options:
  - Reduces bias by focusing on errors sequentially
  - Reduces variance by averaging decorrelated models
  - Increases interpretability of a single tree
  - Eliminates the need for cross-validation
  answer: 1
  why: Bagging trains many models on bootstrap samples and averages them, which mainly reduces variance.
    Boosting is the one that reduces bias sequentially.
- q: In gradient boosting, what does a lower learning_rate generally require?
  options:
  - Fewer trees and faster training
  - More trees (n_estimators) to reach good performance
  - A larger max_depth per tree
  - Removing cross-validation
  answer: 1
  why: A smaller learning rate shrinks each tree's contribution, so you typically need more boosting rounds,
    but it often generalizes better.
- q: Why use StratifiedKFold instead of plain KFold for classification?
  options:
  - It trains faster
  - It preserves class proportions in each fold
  - It removes the need for a test set
  - It automatically tunes hyperparameters
  answer: 1
  why: Stratified folds keep the class distribution consistent across folds, giving more reliable estimates,
    especially with imbalanced data.
- q: Which metric is threshold-independent and measures ranking quality?
  options:
  - Accuracy
  - Recall
  - ROC-AUC
  - Precision
  answer: 2
  why: ROC-AUC measures the probability that a random positive is ranked above a random negative, independent
    of any decision threshold.
- q: In one sentence, why can accuracy be misleading on imbalanced datasets?
  answer: Because a model can achieve high accuracy by always predicting the majority class while completely
    failing to identify the rare positive cases.
  why: With class imbalance, the majority class dominates accuracy, so metrics like precision, recall,
    F1, or PR-AUC give a truer picture.
- q: Name the key reason you should not tune hyperparameters on your final test set.
  answer: Tuning on the test set leaks information and produces an optimistic, biased performance estimate
    that won't generalize.
  why: The test set must remain untouched to give an unbiased estimate; tuning on it causes overfitting
    to that set.
resources:
- label: 'scikit-learn: Ensemble methods user guide'
  url: https://scikit-learn.org/stable/modules/ensemble.html
- label: 'scikit-learn: Cross-validation guide'
  url: https://scikit-learn.org/stable/modules/cross_validation.html
- label: 'scikit-learn: Model evaluation metrics'
  url: https://scikit-learn.org/stable/modules/model_evaluation.html
- label: XGBoost documentation
  url: https://xgboost.readthedocs.io/
---

## Why Ensembles?

A single decision tree is easy to interpret but tends to overfit (high variance) or underfit (high bias). **Ensemble methods** combine many models so that their errors partially cancel out, producing predictions that are more accurate and robust than any individual model.

Two dominant families exist:

- **Bagging (Bootstrap Aggregating):** Train many models in parallel on bootstrap samples and average their predictions. This mainly reduces **variance**. Random forests are the classic example.
- **Boosting:** Train models sequentially, where each new model focuses on the errors of the previous ones. This mainly reduces **bias**. Gradient boosting (and XGBoost/LightGBM) are the leading examples.

## Random Forests

A random forest builds many decision trees, each on a bootstrap sample of the data, and at each split considers only a random subset of features. This **decorrelates** the trees so averaging them yields a large variance reduction.

Key hyperparameters:

- `n_estimators`: number of trees (more is usually better but slower; diminishing returns).
- `max_depth`: limits tree depth to control overfitting.
- `max_features`: number of features considered per split (e.g. `sqrt` for classification).
- `min_samples_leaf`: minimum samples per leaf, a smoothing/regularization knob.

Random forests are robust, need little tuning, handle mixed feature types, and provide feature importances out of the box.

## Gradient Boosting

Gradient boosting fits trees sequentially. Each tree is trained on the **residual errors** (gradients of the loss) of the current ensemble, gradually improving the fit. Because it minimizes bias aggressively, it can overfit if not regularized.

Key hyperparameters:

- `learning_rate`: shrinks each tree's contribution; lower values need more trees but generalize better.
- `n_estimators`: number of boosting rounds.
- `max_depth`: usually small (3-6) for boosting (weak learners).
- `subsample`: fraction of rows sampled per tree (stochastic gradient boosting).

**`HistGradientBoostingClassifier` is the modern scikit-learn boosting default** — a histogram-based implementation that natively handles missing values (NaNs) and categorical features and is far faster than the legacy `GradientBoostingClassifier` on large datasets. **XGBoost**, **LightGBM**, and **CatBoost** are popular external libraries built on similar ideas, with extra regularization and tuning options widely used in production and competitions.

```python
from sklearn.ensemble import HistGradientBoostingClassifier

clf = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1)
clf.fit(X_train, y_train)
```

## Cross-Validation

A single train/test split gives a noisy performance estimate. **k-fold cross-validation** splits data into k folds, trains on k-1 and validates on the remaining fold, rotating k times and averaging the scores. For classification, use **StratifiedKFold** to preserve class proportions in each fold.

Cross-validation is also the basis for hyperparameter search: never tune on your final test set. Use a nested or held-out test set for the final unbiased estimate.

## Evaluation Metrics

Choose metrics that match the business goal, especially with imbalanced classes:

- **Accuracy:** fraction correct; misleading when classes are imbalanced.
- **Precision:** of predicted positives, how many are truly positive (TP / (TP+FP)).
- **Recall (sensitivity):** of actual positives, how many were caught (TP / (TP+FN)).
- **F1:** harmonic mean of precision and recall.
- **ROC-AUC:** area under the ROC curve; probability the model ranks a random positive above a random negative. Threshold-independent and great for ranking quality.
- **PR-AUC:** more informative than ROC-AUC under severe class imbalance.

## Practical Workflow

1. Establish a baseline (e.g. a single tree or logistic regression).
2. Train a random forest and a gradient boosting model.
3. Evaluate with stratified cross-validation using ROC-AUC plus precision/recall.
4. Tune hyperparameters with `RandomizedSearchCV` (faster than full grid).
5. Inspect feature importances for sanity and insight.
6. Report final performance on a held-out test set.

```python
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

rf = RandomForestClassifier(n_estimators=300, max_features='sqrt', random_state=42)
rf_auc = cross_val_score(rf, X, y, cv=cv, scoring='roc_auc')
print('RF ROC-AUC:', rf_auc.mean())

# HistGradientBoosting is the modern, histogram-based sklearn default (fast, handles NaNs)
hgb = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, max_depth=3, random_state=42)
hgb_auc = cross_val_score(hgb, X, y, cv=cv, scoring='roc_auc')
print('HGB ROC-AUC:', hgb_auc.mean())
```

## Key Takeaways

- Bagging reduces variance; boosting reduces bias.
- Random forests are robust defaults; gradient boosting often wins accuracy with careful tuning.
- Always validate with cross-validation and pick metrics suited to your problem and class balance.
