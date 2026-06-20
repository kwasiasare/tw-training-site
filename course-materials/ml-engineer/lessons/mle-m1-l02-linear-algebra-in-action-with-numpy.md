---
course: ml-engineer
title: Linear Algebra in Action with NumPy
month: 1
monthTitle: 'Foundations: Python and Math for ML'
lesson: 2
summary: Learn how to represent and manipulate vectors and matrices with NumPy, compute dot products and
  norms, perform matrix multiplication, and apply decompositions like eigendecomposition and SVD that
  underpin core ML algorithms.
objectives:
- Create and manipulate vectors and matrices using NumPy arrays
- Compute dot products, norms, and cosine similarity to measure vector relationships
- Perform matrix multiplication, transposition, and inversion correctly
- Apply broadcasting to write efficient, vectorized linear algebra code
- Use eigendecomposition and SVD to understand dimensionality reduction techniques like PCA
- Connect linear algebra operations to real ML tasks such as linear regression
video: mle-m1-l02-linear-algebra-in-action-with-numpy.mp4
quiz:
- q: Which operator performs matrix multiplication in NumPy?
  options:
  - '*'
  - '@'
  - +
  - '%'
  answer: 1
  why: The @ operator performs matrix multiplication, while * does element-wise multiplication.
- q: What does np.linalg.norm(v) compute for a vector v?
  options:
  - The sum of its elements
  - Its length (magnitude)
  - Its transpose
  - Its inverse
  answer: 1
  why: The norm computes the magnitude or length of a vector, e.g., the Euclidean norm sqrt(sum of squares).
- q: For A @ B with A of shape (m, n), what shape must B have?
  options:
  - (m, n)
  - (n, p)
  - (p, n)
  - (m, m)
  answer: 1
  why: 'The inner dimensions must match: A is (m, n), so B must be (n, p), giving a result of shape (m,
    p).'
- q: Why prefer np.linalg.solve(A, b) over computing np.linalg.inv(A) @ b?
  options:
  - It returns a different answer
  - It is more numerically stable and efficient
  - It works only on square matrices
  - It computes eigenvalues too
  answer: 1
  why: Solving the system directly is more numerically stable and faster than explicitly forming the inverse.
- q: Which decomposition factors any matrix into U S Vᵀ and underpins PCA and recommender systems?
  answer: SVD (Singular Value Decomposition)
  why: SVD factors any matrix A into U, S, and Vᵀ; its top singular values capture the most variance,
    enabling dimensionality reduction.
- q: In one short phrase, what does broadcasting let you do in NumPy?
  answer: Operate on arrays of different shapes without explicit loops
  why: Broadcasting automatically stretches smaller arrays to compatible shapes, enabling efficient vectorized
    operations like subtracting a mean vector from every row.
resources:
- label: NumPy Linear Algebra documentation (numpy.linalg)
  url: https://numpy.org/doc/stable/reference/routines.linalg.html
- label: '3Blue1Brown: Essence of Linear Algebra (video series)'
  url: https://www.3blue1brown.com/topics/linear-algebra
- label: NumPy Broadcasting guide
  url: https://numpy.org/doc/stable/user/basics.broadcasting.html
- label: Mathematics for Machine Learning (free book)
  url: https://mml-book.github.io/
---

## Why Linear Algebra Matters for ML

Nearly every machine learning model is built on linear algebra. Data is stored as vectors and matrices, model parameters are vectors, and training involves matrix operations. NumPy gives us fast, vectorized tools to do this math efficiently in Python.

## Vectors and Matrices

A **vector** is a 1-D array of numbers; a **matrix** is a 2-D array. In NumPy both are `ndarray` objects.

```python
import numpy as np
v = np.array([1, 2, 3])          # shape (3,)
M = np.array([[1, 2], [3, 4]])    # shape (2, 2)
print(v.shape, M.shape)
```

The `.shape` attribute is your best friend—most bugs are shape mismatches.

## Dot Products and Norms

The **dot product** sums element-wise products and measures alignment between vectors:

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.dot(a, b))   # 32
print(a @ b)          # 32 (preferred operator)
```

The **norm** (length/magnitude) of a vector:

```python
np.linalg.norm(a)     # sqrt(1+4+9) = 3.742
```

**Cosine similarity** measures the angle between vectors (used in recommendations and NLP):

```python
cos = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

## Matrix Multiplication

Matrix multiplication combines rows and columns. For `A @ B`, the inner dimensions must match: `(m, n) @ (n, p) -> (m, p)`.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)          # matrix product
print(A * B)          # element-wise (NOT the same!)
print(A.T)            # transpose
```

This is exactly how a neural network layer computes `outputs = inputs @ weights + bias`.

## Broadcasting

Broadcasting lets NumPy operate on arrays of different shapes without explicit loops, by stretching smaller arrays.

```python
X = np.array([[1, 2, 3], [4, 5, 6]])
mean = X.mean(axis=0)        # shape (3,)
X_centered = X - mean        # broadcasts row-wise
```

This is the foundation of feature normalization.

## Solving Linear Systems

Linear regression's closed-form solution uses matrix inversion. Prefer `np.linalg.solve` over computing the inverse directly for stability.

```python
# Solve Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = np.linalg.solve(A, b)    # [2., 3.]
```

## Matrix Decompositions

Decompositions break a matrix into useful factors.

**Eigendecomposition** finds vectors that only get scaled (not rotated) by a matrix. It powers PCA on covariance matrices.

```python
values, vectors = np.linalg.eig(A)
```

**Singular Value Decomposition (SVD)** factors any matrix `A = U S Vᵀ`. It underpins PCA, recommender systems, and data compression.

```python
U, S, Vt = np.linalg.svd(X)
```

The largest singular values capture the most variance—keeping only the top ones gives dimensionality reduction.

## Putting It Together: Linear Regression

```python
# Normal equation: w = (XᵀX)^-1 Xᵀ y
Xt = X.T
w = np.linalg.solve(Xt @ X, Xt @ y)
```

This single line trains a linear regression model—pure linear algebra.

## Key Takeaways

- Always check shapes; use `@` for matrix multiply, `*` for element-wise.
- Use `np.linalg.solve` instead of explicit inverses.
- SVD and eigendecomposition are the math behind PCA and many ML methods.
