---
course: ml-engineer
title: Regression Models from Scratch and with Scikit-Learn
month: 2
monthTitle: Core Machine Learning Algorithms
lesson: 1
summary: Learn how linear regression works under the hood by implementing it from scratch with gradient
  descent and the normal equation, then build and compare linear, Ridge, and Lasso models with Scikit-Learn
  on a housing dataset. You will evaluate models with proper metrics, understand the bias-variance tradeoff,
  and use regularization to control overfitting.
objectives:
- Derive and implement linear regression from scratch using the normal equation and gradient descent
- Explain the mean squared error cost function and how gradient descent minimizes it
- Train linear, Ridge, and Lasso regression models with Scikit-Learn on a housing dataset
- Evaluate regression performance using MAE, RMSE, and R-squared with proper train/test splits
- Apply feature scaling and regularization to reduce overfitting and improve generalization
- Interpret model coefficients and select an appropriate regression model for a given problem
video: mle-m2-l01-regression-models-from-scratch-and-with-scikit-l.mp4
quiz:
- q: Why is mean squared error a convenient cost function for linear regression?
  options:
  - It is non-differentiable, forcing discrete solutions
  - It is convex, so gradient descent finds a single global minimum
  - It ignores large errors entirely
  - It only works with categorical targets
  answer: 1
  why: MSE is convex for linear models, meaning there is one global minimum, so optimization reliably
    converges to the best weights.
- q: What is the main drawback of the normal equation compared to gradient descent?
  options:
  - It cannot find the optimal weights
  - It requires a learning rate
  - Inverting XᵀX becomes computationally expensive with many features
  - It only works on scaled data
  answer: 2
  why: The normal equation requires inverting XᵀX, which scales roughly as O(n³) in the number of features,
    making it slow for high-dimensional data.
- q: Which regularization technique can drive some coefficients to exactly zero, performing feature selection?
  options:
  - Ridge (L2)
  - Lasso (L1)
  - Standard linear regression
  - Normal equation
  answer: 1
  why: Lasso uses an L1 penalty whose geometry pushes some coefficients to exactly zero, effectively selecting
    a subset of features.
- q: Why should feature scaling and the model be wrapped in a Scikit-Learn Pipeline?
  options:
  - To make training slower but more accurate
  - To prevent data leakage by fitting the scaler only on training data
  - Because models cannot accept raw NumPy arrays
  - To avoid needing a test set
  answer: 1
  why: A Pipeline ensures the scaler is fit only on training folds and reapplied to validation/test data,
    preventing information from leaking and giving honest evaluation.
- q: In one sentence, what does the R-squared metric tell you about a regression model?
  answer: It tells you the fraction of the variance in the target that the model explains, where 1.0 is
    perfect and 0 means no better than predicting the mean.
  why: R² measures explained variance, providing a scale-free sense of fit quality relative to a baseline
    that always predicts the mean.
- q: What effect does increasing the regularization strength α have on the bias-variance tradeoff?
  answer: Increasing α shrinks coefficients more, raising bias but lowering variance, which can reduce
    overfitting up to a point.
  why: Stronger regularization constrains the model, increasing bias and decreasing variance—the core
    mechanism for controlling overfitting.
resources:
- label: Scikit-Learn Linear Models User Guide
  url: https://scikit-learn.org/stable/modules/linear_model.html
- label: 'Hands-On Machine Learning (Géron) Ch. 4: Training Models'
  url: https://github.com/ageron/handson-ml3
- label: Scikit-Learn Regression Metrics Reference
  url: https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics
- label: California Housing Dataset Documentation
  url: https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset
---

## Overview

Regression predicts a **continuous** target (e.g., house price) from input features. In this lesson we build linear regression twice: once by hand to understand the math, and once with Scikit-Learn to see production-ready tooling. We then add regularization (Ridge and Lasso) to combat overfitting.

## The Linear Regression Model

We assume the target is a weighted sum of features plus a bias:

```
ŷ = w0 + w1*x1 + w2*x2 + ... + wn*xn = Xw
```

where `X` includes a column of 1s for the bias term `w0`. The goal is to find weights `w` that minimize prediction error.

## The Cost Function: Mean Squared Error

We measure error with **MSE**:

```
MSE(w) = (1/m) * Σ (ŷ_i - y_i)^2
```

MSE is convex for linear models, so there is a single global minimum. We can reach it two ways.

### 1. The Normal Equation (closed form)

```
w = (XᵀX)⁻¹ Xᵀ y
```

This gives the exact optimal weights in one step. It is great for small/medium feature sets but costs roughly O(n³) to invert `XᵀX`, so it becomes slow when there are many features.

### 2. Gradient Descent (iterative)

Update weights in the direction that reduces cost:

```
gradient = (2/m) * Xᵀ (Xw - y)
w := w - learning_rate * gradient
```

Gradient descent scales to large datasets and many features but requires choosing a learning rate and **feature scaling** (so all features contribute on a comparable scale).

## From-Scratch Implementation

```python
import numpy as np

class LinearRegressionGD:
    def __init__(self, lr=0.01, n_iters=1000):
        self.lr, self.n_iters = lr, n_iters
    def fit(self, X, y):
        m, n = X.shape
        Xb = np.c_[np.ones(m), X]      # add bias column
        self.w = np.zeros(n + 1)
        for _ in range(self.n_iters):
            grad = (2/m) * Xb.T @ (Xb @ self.w - y)
            self.w -= self.lr * grad
        return self
    def predict(self, X):
        return np.c_[np.ones(X.shape[0]), X] @ self.w
```

Always scale features before gradient descent: `X = (X - X.mean()) / X.std()`.

## Regularization

With many or correlated features the model can **overfit**: it memorizes training noise and generalizes poorly. Regularization penalizes large weights.

- **Ridge (L2):** adds `α * Σ wj²`. Shrinks coefficients smoothly, keeps all features. Good default.
- **Lasso (L1):** adds `α * Σ |wj|`. Drives some coefficients to exactly zero, performing feature selection.
- **ElasticNet:** a mix of L1 and L2.

The hyperparameter `α` controls strength: larger `α` = more shrinkage = more bias, less variance.

## With Scikit-Learn

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

X, y = fetch_california_housing(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

for name, model in [('Linear', LinearRegression()),
                    ('Ridge', Ridge(alpha=1.0)),
                    ('Lasso', Lasso(alpha=0.1))]:
    pipe = make_pipeline(StandardScaler(), model)
    pipe.fit(X_tr, y_tr)
    pred = pipe.predict(X_te)
    rmse = np.sqrt(mean_squared_error(y_te, pred))
    print(name, 'RMSE', round(rmse,3), 'R2', round(r2_score(y_te, pred),3))
```

Use a `Pipeline` so scaling is fit only on training data and reapplied consistently—this prevents data leakage.

## Evaluation Metrics

- **MAE** — average absolute error, same units as target, robust to outliers.
- **RMSE** — square root of MSE, penalizes large errors more, same units as target.
- **R²** — fraction of variance explained (1.0 is perfect, 0 means no better than predicting the mean).

Always evaluate on a held-out **test set** and use cross-validation to tune `α`.

## Key Takeaways

Linear regression is the foundation of ML regression. The normal equation gives exact solutions for small problems; gradient descent scales. Regularization (Ridge/Lasso) is essential for generalization, and proper scaling plus pipelines keep your evaluation honest.
