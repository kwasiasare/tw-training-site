---
course: ml-engineer
title: Feature Engineering and Selection Techniques
month: 2
monthTitle: Core Machine Learning Algorithms
lesson: 3
summary: Engineer, encode, scale, and select features to measurably boost model performance on tabular
  data.
objectives:
- Differentiate feature engineering, encoding, scaling, and selection and explain why each matters
- Apply categorical encoding strategies (one-hot, ordinal, target encoding) without leaking information
- Scale and transform numeric features appropriately for the chosen model family
- Engineer informative features from dates, text, and interactions
- Use filter, wrapper, and embedded methods to select a compact, high-signal feature set
- Build leak-free preprocessing pipelines with scikit-learn for reproducible production workflows
video: mle-m2-l03-feature-engineering-and-selection-techniques.mp4
quiz:
- q: Which scaling situation is LEAST necessary?
  options:
  - Training an SVM with an RBF kernel
  - Running PCA on numeric features
  - Fitting a gradient-boosted tree model
  - Training a neural network
  answer: 2
  why: Tree-based models such as gradient boosting are scale-invariant because they split on thresholds,
    so scaling provides little to no benefit.
- q: Why must target (mean) encoding be fit inside cross-validation folds?
  options:
  - To make it run faster
  - To avoid leaking the target into the features
  - To reduce the number of categories
  - To make the encoding one-hot compatible
  answer: 1
  why: Computing category means using the same rows you train on leaks target information, inflating validation
    scores; fitting within folds prevents this.
- q: Which is an example of an embedded feature selection method?
  options:
  - Pearson correlation ranking
  - Recursive Feature Elimination
  - Lasso (L1) coefficient shrinkage
  - Variance threshold
  answer: 2
  why: Lasso performs selection during model training by driving uninformative coefficients to zero, which
    is the definition of an embedded method.
- q: When is one-hot encoding a poor choice?
  options:
  - Low-cardinality nominal features
  - High-cardinality categorical features
  - Binary yes/no features
  - Features with three categories
  answer: 1
  why: One-hot encoding creates one column per category, so high-cardinality features cause an explosion
    in dimensionality.
- q: In one sentence, what is data leakage in feature engineering?
  answer: Data leakage is when information from outside the training fold (especially the target or test
    data) influences feature creation, producing overly optimistic and unreliable performance estimates.
  why: Leakage typically comes from fitting transformers on all data or using future/target information,
    which inflates offline metrics but fails in production.
- q: Name one reason to prefer fewer, well-selected features.
  answer: Fewer strong features reduce overfitting, speed up training, and improve interpretability.
  why: Compact feature sets generalize better and are easier to maintain and explain in production.
resources:
- label: 'scikit-learn: Preprocessing data'
  url: https://scikit-learn.org/stable/modules/preprocessing.html
- label: 'scikit-learn: Feature selection'
  url: https://scikit-learn.org/stable/modules/feature_selection.html
- label: category_encoders library documentation
  url: https://contrib.scikit-learn.org/category_encoders/
- label: Feature Engineering for Machine Learning (O'Reilly)
  url: https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/
---

## Why Feature Engineering Matters

Models learn patterns from features, not raw data. On tabular problems, thoughtful feature engineering often beats fancier algorithms. The goal is to expose signal in a form the model can use, while keeping the pipeline reproducible and leak-free.

Key idea: **Garbage in, garbage out.** A linear model with great features can outperform a deep net fed raw columns.

## The Workflow

1. **Understand** the data (types, distributions, missingness, target relationship).
2. **Clean** (impute, handle outliers, fix types).
3. **Encode** categoricals into numbers.
4. **Scale/transform** numerics.
5. **Create** new features (interactions, ratios, date parts, aggregations).
6. **Select** the most useful features.
7. **Validate** with cross-validation, watching for leakage.

## Encoding Categorical Variables

- **One-hot encoding**: one binary column per category. Good for low-cardinality nominal features. Explodes dimensionality for high cardinality.
- **Ordinal encoding**: map categories to integers. Only valid when there is a real order (e.g. low/medium/high).
- **Target (mean) encoding**: replace category with the mean target value. Powerful for high cardinality, but **must be fit inside cross-validation folds** or it leaks the target. Add smoothing to stabilize rare categories.
- **Frequency/count encoding**: replace category with its occurrence count — cheap and surprisingly useful for tree models.

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_enc = ohe.fit_transform(X[['city']])
```

## Scaling and Transforming Numerics

- **StandardScaler**: zero mean, unit variance. Default for linear models, SVMs, neural nets, PCA.
- **MinMaxScaler**: squashes to [0,1]. Useful when bounded ranges matter.
- **RobustScaler**: uses median/IQR — resilient to outliers.
- **Log / Box-Cox / Yeo-Johnson**: reduce skew, stabilize variance.

Tree-based models (random forests, gradient boosting) are **scale-invariant**, so scaling rarely helps them. Distance- and gradient-based models need it.

## Creating New Features

- **Date/time**: extract year, month, day-of-week, hour, is_weekend, days-since-event.
- **Interactions & ratios**: price_per_sqft, debt_to_income, product of two drivers.
- **Aggregations**: group-by stats (mean spend per customer).
- **Binning**: convert continuous to categorical to capture nonlinearity for linear models.
- **Text**: length, counts, TF-IDF for bag-of-words signal.

## Feature Selection Techniques

- **Filter methods**: rank features independently of the model — correlation, mutual information, chi-square, variance threshold. Fast, model-agnostic.
- **Wrapper methods**: search feature subsets using model performance — Recursive Feature Elimination (RFE), forward/backward selection. Accurate but expensive.
- **Embedded methods**: selection happens during training — L1 (Lasso) zeroes coefficients; tree feature importances; permutation importance. Good balance of cost and quality.

Fewer, stronger features reduce overfitting, speed up training, and improve interpretability.

## Avoiding Data Leakage

Leakage = information from outside the training fold (especially the target or test data) sneaking into features. Common causes: scaling/encoding fit on the full dataset, target encoding without folds, or features computed using future information.

**Fix:** fit all transformers on training data only, inside a `Pipeline`, and evaluate with cross-validation.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

pre = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
])
pipe = Pipeline([('pre', pre), ('clf', RandomForestClassifier())])
pipe.fit(X_train, y_train)  # all preprocessing learned from train only
```

## Practical Tips

- Always measure: compare CV scores before and after each change.
- Start simple; add complexity only if it pays off.
- Document every transformation so production matches training.
- Watch cardinality, missingness, and skew as red flags.
