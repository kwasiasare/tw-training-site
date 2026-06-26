---
course: data-scientist
title: Feature Engineering and Tree-Based Models
month: 3
monthTitle: Machine Learning in Practice
lesson: 3
summary: Learn how to engineer predictive features and build tree-based models (random forests and gradient
  boosting) to lift model performance on real-world tabular data.
objectives:
- Explain why feature engineering often matters more than model choice for tabular data
- Create and transform features including encodings, interactions, and date/aggregate features
- Distinguish how random forests and gradient boosting machines work and when to use each
- Train, tune, and evaluate tree-based models with scikit-learn and gradient boosting libraries
- Interpret feature importance and avoid common pitfalls like data leakage
video: dsc-m3-l03-feature-engineering-and-tree-based-models.mp4
quiz:
- q: For tabular data, which generally has the biggest impact on model performance?
  options:
  - The deep learning architecture
  - The quality of engineered features
  - The programming language used
  - The number of CPU cores
  answer: 1
  why: For structured/tabular data, well-engineered features typically matter more than the specific algorithm
    chosen.
- q: How does a random forest reduce overfitting compared to a single decision tree?
  options:
  - By building trees sequentially to fix errors
  - By averaging many trees trained on bootstrap samples and random feature subsets
  - By using a very high learning rate
  - By removing all categorical features
  answer: 1
  why: Random forests use bagging — averaging many decorrelated trees reduces variance and overfitting.
- q: Which statement about gradient boosting is correct?
  options:
  - Trees are built independently in parallel
  - Each new tree corrects the errors of the previous ensemble
  - It is insensitive to hyperparameters
  - It cannot be used for classification
  answer: 1
  why: Gradient boosting builds trees sequentially, each one fitting the residual errors of the current
    ensemble.
- q: Which practice helps prevent data leakage?
  options:
  - Fitting encoders on the full dataset before splitting
  - Using target encoding without cross-validation
  - Fitting transformations inside a pipeline on the training fold only
  - Including post-outcome features
  answer: 2
  why: Fitting transformations only on the training fold (via a pipeline) ensures no test/future information
    leaks into training.
- q: Name one feature engineering technique appropriate for a high-cardinality categorical column.
  answer: Target/mean encoding (computed with cross-validation)
  why: High-cardinality columns are too wide for one-hot encoding; target encoding with cross-folds is
    compact and avoids leakage.
- q: In gradient boosting, what combination typically generalizes better at the cost of training time?
  answer: A lower learning rate with more trees (plus early stopping)
  why: Smaller learning rates require more trees but produce smoother, better-generalizing models; early
    stopping prevents overfitting.
resources:
- label: 'scikit-learn: Ensemble methods documentation'
  url: https://scikit-learn.org/stable/modules/ensemble.html
- label: LightGBM documentation
  url: https://lightgbm.readthedocs.io/
- label: 'SHAP: explaining model predictions'
  url: https://shap.readthedocs.io/
- label: 'Kaggle: Feature Engineering course'
  url: https://www.kaggle.com/learn/feature-engineering
---

## Why Feature Engineering Matters

For structured/tabular data, the quality of your features usually determines model performance more than the choice of algorithm. Feature engineering is the process of using domain knowledge and data transformations to create inputs that make patterns easier for models to learn.

Good features:
- Encode domain knowledge (e.g., `price_per_sqft` instead of raw price and area)
- Reduce noise and expose signal
- Handle missing values and outliers sensibly

## Common Feature Engineering Techniques

**Categorical encoding**
- One-hot encoding for low-cardinality categories
- Target/mean encoding for high-cardinality (with cross-fold to avoid leakage)
- Ordinal encoding when categories have natural order

Rather than hand-rolling the cross-fold target encoding, reach for the built-in `sklearn.preprocessing.TargetEncoder`, which handles the cross-fold internally. As a modern alternative, `HistGradientBoostingClassifier(categorical_features=...)` consumes categoricals natively, so you can often skip explicit encoding altogether.

**Numeric transformations**
- Scaling (less critical for trees, important for linear/NN models)
- Log transforms for skewed distributions
- Binning continuous values

**Interaction & ratio features**
- Combine columns: `income / household_size`, `clicks * recency`

**Date/time features**
- Extract day-of-week, month, hour, is_weekend, time-since-event

**Aggregation features**
- Group-by statistics: customer's average purchase, rolling means

## Tree-Based Models

Tree-based models split the feature space into regions using if/else rules. A single decision tree is interpretable but tends to overfit. Ensembles fix this.

**Random Forest (bagging)**
- Trains many deep trees on bootstrap samples with random feature subsets
- Averages predictions to reduce variance
- Robust, little tuning, parallelizable

**Gradient Boosting (boosting)**
- Builds trees sequentially, each correcting the previous errors
- Often the highest accuracy on tabular data
- Libraries: XGBoost, LightGBM, CatBoost, and sklearn's `HistGradientBoostingClassifier`
- More sensitive to hyperparameters (learning rate, tree depth, number of estimators)

## Key Hyperparameters

| Model | Key knobs |
|-------|-----------|
| Random Forest | `n_estimators`, `max_depth`, `max_features`, `min_samples_leaf` |
| Gradient Boosting | `learning_rate`, `n_estimators`, `max_depth`, `subsample` |

Lower learning rate + more trees usually generalizes better but trains slower. Use early stopping with a validation set.

## Avoiding Data Leakage

Leakage happens when information unavailable at prediction time sneaks into training. Common causes:
- Fitting scalers/encoders on the full dataset before splitting
- Target encoding without cross-validation
- Including future or post-outcome features

Always fit transformations inside a pipeline on the training fold only.

## Evaluation & Interpretation

- Use proper validation (k-fold or time-based splits)
- Choose metrics aligned with the business (AUC, F1, RMSE)
- Inspect feature importance and SHAP values to explain predictions
- Compare against a simple baseline before celebrating

## Practical Workflow

1. Build a baseline model on raw features
2. Engineer features iteratively, validating each change
3. Try random forest, then gradient boosting
4. Tune hyperparameters with cross-validation
5. Interpret and validate for leakage before deploying
