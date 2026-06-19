---
course: ml-engineer
title: 'Python for ML: NumPy, Pandas, and Clean Code'
month: 1
monthTitle: 'Foundations: Python and Math for ML'
lesson: 1
summary: A hands-on lesson that builds your core data-wrangling toolkit using NumPy and Pandas. You'll
  learn to create and manipulate arrays, load and clean real-world tabular data, explore datasets, and
  write clean, maintainable Python that scales into production ML pipelines.
objectives:
- Create, index, and perform vectorized operations on NumPy arrays instead of slow Python loops
- Load tabular data into Pandas DataFrames and inspect its structure, types, and summary statistics
- Clean messy data by handling missing values, fixing dtypes, and removing duplicates
- Explore and transform data using filtering, grouping, and aggregation
- Apply clean-code practices (clear names, small functions, vectorization) to data-wrangling scripts
video: mle-m1-l01-python-for-ml-numpy-pandas-and-clean-code.mp4
quiz:
- q: Why are vectorized NumPy operations generally preferred over Python for-loops for numeric work?
  options:
  - They use more memory but are easier to read
  - They run in optimized C and are faster and clearer
  - They automatically handle missing values
  - They only work on integers
  answer: 1
  why: Vectorized operations apply to the whole array at once in optimized C code, making them both faster
    than Python loops and more readable.
- q: Which Pandas method gives you column data types and a count of non-null values?
  options:
  - df.describe()
  - df.head()
  - df.info()
  - df.shape
  answer: 2
  why: df.info() reports each column's dtype along with non-null counts, while describe() gives numeric
    summary stats and head() shows sample rows.
- q: What is the difference between df.loc and df.iloc?
  options:
  - loc selects by label, iloc selects by integer position
  - loc is faster than iloc
  - iloc only works on columns
  - There is no difference
  answer: 0
  why: loc indexes by row/column labels, whereas iloc indexes by integer positions.
- q: Which approach avoids the SettingWithCopyWarning when assigning to a subset of rows?
  options:
  - df[df.a > 1]['b'] = 0
  - Using a for-loop with iterrows
  - Using df.loc[df.a > 1, 'b'] = 0
  - Converting to a NumPy array first
  answer: 2
  why: Chained indexing can operate on a copy; using a single .loc call with both row and column selectors
    ensures the assignment targets the original DataFrame.
- q: In one short phrase, name the Pandas pattern used to compute survival rate per passenger class.
  answer: split-apply-combine (groupby)
  why: 'groupby implements split-apply-combine: data is split into groups, an aggregation is applied,
    and results are combined.'
- q: Name one reason filling missing ages with the median is often preferred over the mean.
  answer: The median is robust to outliers
  why: Outliers skew the mean but have little effect on the median, making median imputation more stable
    for skewed numeric columns.
resources:
- label: 'NumPy: The Absolute Basics for Beginners'
  url: https://numpy.org/doc/stable/user/absolute_beginners.html
- label: 'Pandas: 10 Minutes to Pandas'
  url: https://pandas.pydata.org/docs/user_guide/10min.html
- label: 'Pandas User Guide: Working with Missing Data'
  url: https://pandas.pydata.org/docs/user_guide/missing_data.html
- label: PEP 8 – Style Guide for Python Code
  url: https://peps.python.org/pep-0008/
---

## Why NumPy and Pandas?

Machine learning starts with data, and the vast majority of an ML engineer's early work is loading, cleaning, and exploring that data. Two libraries form the backbone of this work in Python:

- **NumPy** provides the `ndarray`, a fast, memory-efficient n-dimensional array that powers nearly every numeric library in Python (including Pandas, scikit-learn, and PyTorch).
- **Pandas** provides the `DataFrame`, a labeled, table-like structure ideal for real-world, heterogeneous datasets.

Understanding both — and when to use which — is foundational for every downstream ML task.

## NumPy: Vectorized Numeric Computing

A NumPy array stores elements of a single type in contiguous memory, which makes operations dramatically faster than Python lists.

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.arange(0, 8, 2)      # [0 2 4 6]
z = np.zeros((2, 3))         # 2x3 matrix of zeros

# Vectorized math: no loops needed
print(a * 2)                 # [2 4 6 8]
print(a + b)                 # elementwise add
print(a.mean(), a.sum())
```

### Vectorization beats loops

Instead of writing a `for` loop to process each element, apply operations to the whole array at once. This is faster (executed in optimized C) and clearer.

```python
# Slow, un-Pythonic
result = [x ** 2 for x in range(1000)]

# Fast, vectorized
result = np.arange(1000) ** 2
```

### Indexing, slicing, and boolean masks

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
m[0, 1]        # 2
m[:, 0]        # first column -> [1 4]
m[m > 3]       # boolean mask -> [4 5 6]
```

Broadcasting lets arrays of different shapes combine automatically, e.g. adding a row vector to every row of a matrix.

## Pandas: Working with Real Data

A `DataFrame` is a collection of columns (each a `Series`) sharing an index. Load data from CSV and inspect it immediately:

```python
import pandas as pd

df = pd.read_csv('titanic.csv')
df.head()          # first 5 rows
df.shape           # (rows, columns)
df.info()          # dtypes and non-null counts
df.describe()      # summary stats for numeric columns
df['age'].value_counts()
```

### Selecting data

- `df['age']` selects one column (a Series).
- `df[['age', 'fare']]` selects multiple columns.
- `df.loc[row_label, col_label]` selects by label.
- `df.iloc[row_pos, col_pos]` selects by integer position.
- Boolean filtering: `df[df['age'] > 30]`.

## Cleaning Messy Data

Real datasets are rarely clean. Common steps:

```python
# 1. Detect missing values
df.isnull().sum()

# 2. Fill or drop them
df['age'] = df['age'].fillna(df['age'].median())
df = df.dropna(subset=['embarked'])

# 3. Fix dtypes
df['survived'] = df['survived'].astype('int')

# 4. Remove duplicates
df = df.drop_duplicates()

# 5. Standardize text
df['sex'] = df['sex'].str.strip().str.lower()
```

Choose imputation strategies thoughtfully — median is robust to outliers, while dropping rows loses data. Document your decisions.

## Exploring with Group-By and Aggregation

The split-apply-combine pattern answers analytical questions quickly:

```python
# Survival rate by passenger class
df.groupby('pclass')['survived'].mean()

# Multiple aggregations
df.groupby('sex').agg(
    avg_age=('age', 'mean'),
    count=('survived', 'size'),
)
```

## Clean Code for Data Work

Data scripts rot fast. Keep them maintainable:

- **Prefer vectorized operations** over `iterrows()` loops — they're faster and clearer.
- **Avoid chained assignment** like `df[df.a > 1]['b'] = 0`; use `.loc` instead to prevent `SettingWithCopyWarning`.
- **Use descriptive names**: `passengers_df`, not `d2`.
- **Wrap reusable logic in small functions** with a single responsibility.
- **Avoid mutating in place silently**; return new DataFrames or be explicit.

```python
def clean_passengers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['age'] = df['age'].fillna(df['age'].median())
    df['sex'] = df['sex'].str.strip().str.lower()
    return df.drop_duplicates()
```

A clean cleaning function is testable, reusable, and the first step toward a production pipeline.

## Key Takeaways

- NumPy gives you fast vectorized numeric arrays; Pandas gives you labeled tabular data.
- Inspect before you transform: `head`, `info`, `describe`.
- Handle missing data, dtypes, and duplicates deliberately.
- Use group-by for fast exploration, and write clean, function-based code.
