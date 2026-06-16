---
course: dami-ai-career
title: NumPy & vectorised operations
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 3
summary: Use NumPy arrays to do fast, whole-array maths without writing loops — the foundation under pandas
  and every AI library.
objectives:
- Create NumPy arrays from lists and with helpers like arange and zeros
- Explain why vectorised array operations are faster than Python loops
- Use element-wise arithmetic, broadcasting, and built-in maths functions
- Inspect arrays with shape, dtype, and ndim
- Index and slice 1D and 2D arrays, including boolean masks
- Aggregate arrays with sum, mean, and axis-based reductions
video: m2-l03-numpy.mp4
quiz:
- q: What does 'vectorised' mean in NumPy?
  options:
  - Drawing graphs as vectors
  - Applying an operation to a whole array at once, with no explicit Python loop
  - Converting an array into a Python list
  - Running code on the GPU
  answer: 1
  why: Vectorised operations run the loop in fast, compiled C code under the hood, so you write a + b
    instead of a for-loop.
- q: Why is a NumPy array usually faster than a Python list for numeric work?
  answer: It stores one fixed numeric type in a contiguous block of memory and runs operations in compiled
    C, avoiding per-element Python overhead.
  why: A Python list holds boxed objects scattered in memory; a NumPy array is a tight, typed buffer the
    CPU can stream through quickly.
- q: Given a = np.array([1, 2, 3]), what is a * 2?
  options:
  - '[1, 2, 3, 1, 2, 3]'
  - '[2, 4, 6]'
  - An error
  - '[1, 4, 9]'
  answer: 1
  why: Multiplication is element-wise on arrays. Unlike a Python list (where * repeats it), a NumPy array
    doubles each element.
- q: What attribute tells you the dimensions of an array, e.g. (3, 4)?
  answer: shape
  why: a.shape returns a tuple giving the size along each axis; (3, 4) means 3 rows and 4 columns.
- q: What does broadcasting let you do?
  options:
  - Send arrays over a network
  - Combine arrays of different but compatible shapes without copying data
  - Print arrays nicely
  - Convert dtypes automatically
  answer: 1
  why: Broadcasting stretches a smaller array across a larger one (e.g. adding a scalar or a row to a
    matrix) without making real copies.
- q: For a 2D array a, what does a.sum(axis=0) compute?
  answer: The sum down each column (collapsing the rows).
  why: axis=0 reduces along rows, leaving one value per column; axis=1 would sum across columns, giving
    one value per row.
resources:
- label: NumPy — the absolute basics for beginners
  url: https://numpy.org/doc/stable/user/absolute_beginners.html
- label: NumPy Quickstart tutorial
  url: https://numpy.org/doc/stable/user/quickstart.html
- label: 'Python Data Science Handbook (Jake VanderPlas) — Chapter 2: Introduction to NumPy'
  url: https://jakevdp.github.io/PythonDataScienceHandbook/
- label: 'Real Python — NumPy Tutorial: Your First Steps Into Data Science'
  url: https://realpython.com/numpy-tutorial/
---

## Why NumPy?

**NumPy** (Numerical Python) is the core array library for scientific computing in Python. Almost everything in data science and AI — pandas, scikit-learn, PyTorch — is built on top of it.

A plain Python list can hold anything, but that flexibility is slow for numbers. NumPy's array (the `ndarray`) stores one fixed type in a contiguous block of memory, so the CPU can stream through it and run operations in compiled C. The result: cleaner code that is often 10 to 100 times faster.

```bash
pip install numpy
```

## Creating arrays

The convention is `import numpy as np`. You can build arrays from lists, or with helpers.

```python
import numpy as np

a = np.array([1, 2, 3, 4])
zeros = np.zeros(5)            # [0. 0. 0. 0. 0.]
range_ = np.arange(0, 10, 2)  # [0 2 4 6 8]
grid = np.array([[1, 2, 3],
                 [4, 5, 6]])  # a 2x3 matrix

print(grid.shape)   # (2, 3)
print(grid.dtype)   # int64
print(grid.ndim)    # 2
```

`shape` is the size along each axis, `dtype` is the element type, and `ndim` is the number of dimensions.

## Vectorised operations

The big idea: apply an operation to a **whole array at once**, with no explicit loop. This is called **vectorisation**.

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

print(a + b)        # [11 22 33]
print(a * 2)        # [2 4 6]
print(np.sqrt(a))   # [1.  1.41 1.73]
```

Compare that to writing a `for` loop to add two lists element by element — vectorised code is shorter, clearer, and far faster.

## Broadcasting

**Broadcasting** lets NumPy combine arrays of different but compatible shapes. A scalar, or a row, is automatically stretched to fit — without actually copying the data.

```python
grid = np.array([[1, 2, 3],
                 [4, 5, 6]])
row = np.array([10, 20, 30])

print(grid + row)
# [[11 22 33]
#  [14 25 36]]
```

## Indexing, slicing & masks

Indexing works like lists, but extends to multiple dimensions and to **boolean masks** — a powerful way to filter.

```python
a = np.array([5, 12, 7, 20, 3])

print(a[1])          # 12
print(a[1:4])        # [12  7 20]
print(a[a > 10])     # [12 20]  (boolean mask)
```

## Aggregations

Reductions like `sum` and `mean` collapse an array to a summary. With 2D arrays, `axis` chooses the direction.

```python
grid = np.array([[1, 2, 3],
                 [4, 5, 6]])

print(grid.sum())          # 21  (everything)
print(grid.sum(axis=0))    # [5 7 9]  (down columns)
print(grid.mean(axis=1))   # [2. 5.]  (across rows)
```

## Your task

Create an array of 10 numbers, then **without any loop** compute their mean, find all values above the mean using a boolean mask, and square them.
