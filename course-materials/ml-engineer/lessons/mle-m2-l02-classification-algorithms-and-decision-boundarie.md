---
course: ml-engineer
title: Classification Algorithms and Decision Boundaries
month: 2
monthTitle: Core Machine Learning Algorithms
lesson: 2
summary: This lesson teaches you how to train and compare three foundational classifiers—logistic regression,
  decision trees, and support vector machines—on a real classification problem. You'll learn what a decision
  boundary is, how each algorithm carves up feature space, and how to interpret model outputs, evaluate
  performance, and choose the right tool for the job.
objectives:
- Explain what a decision boundary is and how it differs across logistic regression, decision trees, and
  SVMs
- Train logistic regression, decision tree, and SVM classifiers using scikit-learn
- Interpret model coefficients, feature importances, and support vectors to understand predictions
- Evaluate and compare classifiers using accuracy, precision, recall, F1, and confusion matrices
- Diagnose underfitting vs. overfitting and tune key hyperparameters for each algorithm
video: mle-m2-l02-classification-algorithms-and-decision-boundarie.mp4
quiz:
- q: Which statement best describes the decision boundary of logistic regression?
  options:
  - A set of axis-aligned rectangles
  - A straight hyperplane where w·x + b = 0
  - A smooth curve defined by support vectors
  - A random partition of feature space
  answer: 1
  why: Logistic regression is a linear classifier; its boundary is the hyperplane where the linear combination
    w·x + b equals zero.
- q: Why is feature scaling important for SVMs and logistic regression but not strictly for decision trees?
  options:
  - Trees train faster when unscaled
  - Distance- and magnitude-based methods are sensitive to feature scale, while tree splits compare values
    within a single feature
  - Scaling changes the class labels
  - SVMs ignore feature values entirely
  answer: 1
  why: SVMs (margins/distances) and logistic regression (coefficient magnitudes) are sensitive to differing
    feature scales, whereas a tree splits on one feature at a time so monotonic scaling doesn't change
    splits.
- q: In a cancer-detection model, which metric is usually the highest priority and why?
  options:
  - Precision, because false alarms are most costly
  - Recall, because missing a malignant case (false negative) is dangerous
  - Accuracy, because classes are balanced
  - Training speed, because data is small
  answer: 1
  why: Missing a malignant tumor (a false negative) can be life-threatening, so recall—catching as many
    true positives as possible—is typically prioritized.
- q: Which hyperparameter most directly controls overfitting in a decision tree?
  options:
  - gamma
  - kernel
  - max_depth
  - learning_rate
  answer: 2
  why: Limiting max_depth (along with min_samples_leaf) restricts how complex the tree can grow, reducing
    overfitting.
- q: 'Short answer: What are the points called that lie closest to an SVM''s decision boundary and define
    its margin?'
  answer: support vectors
  why: The maximum-margin hyperplane is determined by the closest training points, which are called support
    vectors.
- q: 'Short answer: Name the scikit-learn hyperparameter that controls regularization strength in both
    LogisticRegression and SVC (it is the inverse of regularization strength).'
  answer: C
  why: In both LogisticRegression and SVC, C is the inverse regularization parameter—smaller C means stronger
    regularization.
resources:
- label: 'scikit-learn: Supervised Learning – Classification'
  url: https://scikit-learn.org/stable/supervised_learning.html
- label: 'scikit-learn: Plot classifier decision boundaries (Classifier comparison)'
  url: https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
- label: 'scikit-learn: SVM kernels and parameters guide'
  url: https://scikit-learn.org/stable/modules/svm.html
- label: Breast Cancer Wisconsin dataset documentation
  url: https://scikit-learn.org/stable/datasets/toy_dataset.html#breast-cancer-dataset
---

## Overview

Classification is the task of assigning inputs to one of several discrete categories. In this lesson we solve a binary classification problem (predicting whether a tumor is malignant or benign using the Breast Cancer Wisconsin dataset) with three classic algorithms and compare how each separates the classes.

The central idea uniting them is the **decision boundary**: the surface in feature space where the model switches from predicting one class to another. Different algorithms produce different boundary shapes, which directly affects bias, variance, and interpretability.

## The Three Algorithms

### Logistic Regression
Despite the name, logistic regression is a **linear classifier**. It models the probability of the positive class with the sigmoid of a linear combination of features:

```
p(y=1 | x) = 1 / (1 + e^-(w·x + b))
```

- The decision boundary is a **straight line** (hyperplane in higher dimensions) where `w·x + b = 0`.
- Coefficients `w` are interpretable: a positive weight pushes the prediction toward the positive class.
- Regularization (`C` in scikit-learn, the inverse of regularization strength) controls overfitting.

### Decision Trees
A decision tree splits the data with a sequence of **axis-aligned** if/else rules, producing a boundary made of rectangular regions.

- Highly interpretable—you can read the rules directly.
- Handles non-linear relationships and mixed feature types without scaling.
- Prone to **overfitting**; control with `max_depth`, `min_samples_leaf`, and pruning.
- Feature importances tell you which features drive the splits.

### Support Vector Machines (SVM)
An SVM finds the hyperplane that **maximizes the margin** between classes. The points closest to the boundary are the **support vectors**.

- With a linear kernel the boundary is a line; with an **RBF kernel** it becomes smoothly curved.
- Key hyperparameters: `C` (margin softness vs. misclassification) and `gamma` (RBF kernel reach).
- Requires **feature scaling** to work well.

## A Practical Workflow

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

scaler = StandardScaler().fit(X_train)
X_train_s, X_test_s = scaler.transform(X_train), scaler.transform(X_test)

models = {
    'logreg': LogisticRegression(max_iter=5000, C=1.0),
    'tree':   DecisionTreeClassifier(max_depth=4, random_state=42),
    'svm':    SVC(kernel='rbf', C=1.0, gamma='scale'),
}

for name, model in models.items():
    # tree doesn't need scaling, but scaled input is harmless
    model.fit(X_train_s, y_train)
    preds = model.predict(X_test_s)
    print(name)
    print(confusion_matrix(y_test, preds))
    print(classification_report(y_test, preds))
```

## Interpreting Results

- **Confusion matrix**: rows are true labels, columns are predictions. In medical contexts, false negatives (missing a malignant tumor) are far costlier than false positives.
- **Precision** = TP / (TP + FP): of predicted positives, how many were correct.
- **Recall** = TP / (TP + FN): of actual positives, how many we caught. Often the priority in healthcare.
- **F1** balances precision and recall.
- Prefer **stratified** splits and cross-validation so class proportions stay consistent.

## Choosing the Right Model

| Need | Best fit |
|------|----------|
| Interpretable rules | Decision tree |
| Probability estimates + linear signal | Logistic regression |
| Complex non-linear boundary, medium data | SVM (RBF) |
| Fast training on huge data | Logistic regression |

Always scale features for logistic regression and SVMs, tune hyperparameters with cross-validation, and judge models on the metric that matches your business cost.
