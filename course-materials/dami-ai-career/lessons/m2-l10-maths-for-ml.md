---
course: dami-ai-career
title: Maths-for-ML bridge
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 10
summary: 'Connect the maths you already know to the four pillars machine learning actually uses: vectors,
  matrices, derivatives, and probability.'
objectives:
- Represent data as vectors and matrices with NumPy
- Compute dot products and understand them as similarity and weighted sums
- Use matrix multiplication to apply a model to many rows at once
- Explain gradients and how gradient descent minimises a loss
- Read probability notation and apply Bayes' rule to a simple problem
- Recognise the four maths pillars inside a real ML training loop
video: m2-l10-maths-for-ml.mp4
quiz:
- q: What does the dot product of two vectors give you?
  options:
  - Another vector
  - A single number (scalar)
  - A matrix
  - A probability
  answer: 1
  why: The dot product sums the element-wise products, producing one scalar — a weighted sum used everywhere
    in ML.
- q: In gradient descent, which direction do you step to reduce the loss?
  options:
  - Along the gradient
  - Opposite the gradient
  - Perpendicular to the gradient
  - A random direction
  answer: 1
  why: The gradient points uphill (steepest increase), so we step in the negative gradient direction to
    go downhill toward a minimum.
- q: For NumPy arrays A (shape 3x2) and B (shape 2x4), what is the shape of A @ B?
  options:
  - 3x4
  - 2x2
  - 3x2
  - It errors
  answer: 0
  why: Matrix multiplication requires inner dimensions to match (2 and 2); the result takes the outer
    dimensions, giving 3x4.
- q: What is a gradient, in one sentence?
  answer: The vector of partial derivatives of a function — it points in the direction of steepest increase.
  why: Each component is the slope with respect to one variable; together they say which way the function
    rises fastest.
- q: State Bayes' rule and what it lets you do.
  answer: P(A|B) = P(B|A) * P(A) / P(B); it flips a conditional probability so you can update a belief
    given new evidence.
  why: It is the backbone of probabilistic ML — turning P(evidence|cause) into P(cause|evidence).
- q: Why do we use matrices instead of looping over rows one at a time?
  options:
  - Matrices are more accurate
  - Vectorised matrix maths is far faster and clearer
  - Loops are not allowed in Python
  - Matrices use less memory always
  answer: 1
  why: Libraries like NumPy run matrix operations in fast compiled code, processing every row at once
    — vectorisation beats Python loops for speed and readability.
resources:
- label: 3Blue1Brown — Essence of Linear Algebra (video series)
  url: https://www.3blue1brown.com/topics/linear-algebra
- label: NumPy — The Absolute Basics for Beginners
  url: https://numpy.org/doc/stable/user/absolute_beginners.html
- label: Mathematics for Machine Learning (Deisenroth, Faisal, Ong) — free PDF
  url: https://mml-book.github.io/
- label: 3Blue1Brown — Gradient descent, how neural networks learn
  url: https://www.youtube.com/watch?v=IHZwWFHWa-w
---

## Why this lesson?

You already have the hard part — a maths degree. The goal here is **translation**, not new theory: matching the four pieces of maths that machine learning leans on to the language ML practitioners use. Those four pillars are **vectors**, **matrices**, **derivatives (gradients)**, and **probability**.

We'll do all of it in code with NumPy, because in ML you rarely compute by hand — you describe the maths and let the library run it fast.

## Vectors: data as arrows

A **vector** is just an ordered list of numbers. One data point — say a house with size, bedrooms, and age — becomes a vector `[120, 3, 10]`. The **dot product** multiplies matching entries and sums them into a single number.

```python
import numpy as np

x = np.array([120, 3, 10])      # features
w = np.array([0.5, 20, -1.0])   # weights
prediction = x @ w              # dot product -> scalar
print(prediction)               # 110.0
```

That dot product is a **weighted sum** — the core operation inside almost every model. It also measures similarity: aligned vectors give a large value.

## Matrices: many rows at once

Stack many data vectors as rows and you get a **matrix**. **Matrix multiplication** applies the same weights to every row in one go — this is *vectorisation*, and it is far faster than a Python loop.

```python
import numpy as np

X = np.array([[120, 3, 10],     # 3 houses
              [80,  2, 25],
              [150, 4, 2]])
w = np.array([0.5, 20, -1.0])
predictions = X @ w             # one prediction per row
print(predictions)              # [110.  70. 133.]
```

Remember the shape rule: `(m x n) @ (n x p) = (m x p)`. The inner dimensions must match.

## Derivatives: how models learn

Training means **minimising a loss** — a number measuring how wrong the model is. The **gradient** is the vector of partial derivatives of the loss with respect to each weight; it points uphill. So we step the *other* way. That loop is **gradient descent**:

```python
w = w - learning_rate * gradient
```

Repeat thousands of times and the weights settle where the loss is small. Every "learning" algorithm you'll meet is some flavour of this idea.

## Probability: reasoning under uncertainty

ML outputs are rarely certain — they're **probabilities**. You'll read `P(A|B)` as "probability of A given B". The key tool is **Bayes' rule**, which flips a conditional so you can update a belief when new evidence arrives:

`P(A|B) = P(B|A) * P(A) / P(B)`

This underpins spam filters, classifiers, and anything that reasons from evidence to cause.

## Your task

Using NumPy, build a 4x3 feature matrix and a length-3 weight vector, then compute all four predictions with a single `@`. Confirm by hand that one row matches.
