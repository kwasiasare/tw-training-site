---
course: data-scientist
title: Python Essentials for Data Work
month: 1
monthTitle: Python and Data Wrangling Foundations
lesson: 1
summary: 'A hands-on introduction to the Python skills data scientists use daily: setting up a reliable
  environment, mastering core syntax and data structures, and writing reusable functions through small,
  data-focused exercises.'
objectives:
- Set up a reproducible Python environment using virtual environments and a notebook or IDE
- Use Python's core data types and structures (lists, tuples, dicts, sets) to represent tabular and record
  data
- Apply control flow and comprehensions to filter, transform, and aggregate small datasets
- Write clean, reusable functions with parameters, return values, and docstrings
- Handle common edge cases and errors gracefully when wrangling messy data
video: dsc-m1-l01-python-essentials-for-data-work.mp4
quiz:
- q: Which data structure best represents a single row of named fields?
  options:
  - list
  - tuple
  - dict
  - set
  answer: 2
  why: A dictionary maps field names (keys) to values, which is exactly how a row with named columns is
    represented.
- q: What does dict.get("key", 0) return if the key is missing?
  options:
  - It raises a KeyError
  - It returns None
  - It returns 0
  - It returns an empty string
  answer: 2
  why: The second argument to .get() is the default returned when the key is absent, so it returns 0 instead
    of raising an error.
- q: Which comprehension correctly filters rows where revenue exceeds 1000?
  options:
  - '[r for r in table if r["revenue"] > 1000]'
  - '[r > 1000 for r in table]'
  - '{r: 1000 for r in table}'
  - '[r for r in table > 1000]'
  answer: 0
  why: The condition belongs in an if clause after the loop expression, keeping only rows whose revenue
    exceeds 1000.
- q: Why should you use a virtual environment for a data project?
  options:
  - It makes Python run faster
  - It isolates project dependencies for reproducibility
  - It is required to import pandas
  - It automatically writes your code
  answer: 1
  why: Virtual environments isolate package versions per project so the environment can be reproduced
    reliably by others.
- q: In one short phrase, what is the purpose of wrapping a float() conversion in a try/except block?
  answer: To handle invalid or missing values gracefully instead of crashing
  why: float() raises ValueError or TypeError on bad input; try/except lets you return a safe default
    and keep the program running.
- q: What command writes your installed packages and versions to a file for sharing?
  answer: pip freeze > requirements.txt
  why: pip freeze lists installed packages with pinned versions, and redirecting it to requirements.txt
    records them for reproducible setups.
resources:
- label: Python Official Tutorial — Data Structures
  url: https://docs.python.org/3/tutorial/datastructures.html
- label: 'Real Python: Python Virtual Environments Primer'
  url: https://realpython.com/python-virtual-environments-a-primer/
- label: Python Docs — Errors and Exceptions
  url: https://docs.python.org/3/tutorial/errors.html
- label: JupyterLab Documentation
  url: https://jupyterlab.readthedocs.io/
---

## Why Python for Data Work

Python is the lingua franca of data science because it is readable, has a massive ecosystem (pandas, NumPy, scikit-learn), and scales from quick exploration to production pipelines. Before reaching for libraries, you need fluency in the language itself: the data structures and functions you'll use thousands of times.

## Setting Up Your Environment

Reproducibility starts with isolation. Never install packages globally for project work.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install core tools and pin them
pip install jupyterlab pandas numpy
pip freeze > requirements.txt
```

Use JupyterLab or VS Code for interactive exploration. Commit your `requirements.txt` so teammates can rebuild the exact environment.

**Modern tooling:** Many teams now use `uv`, a fast drop-in for venv and pip (e.g. `uv venv`, `uv pip install pandas`). It's also common to declare your *direct* dependencies in a `pyproject.toml` and keep a separate locked file for the exact, fully-pinned versions.

## Core Data Types

- **int / float** — numeric values for measurements and counts
- **str** — text, labels, categorical values
- **bool** — `True`/`False`, often the result of comparisons
- **None** — the absence of a value (think missing data)

```python
revenue = 1999.50      # float
customers = 42         # int
region = "EMEA"        # str
is_active = True        # bool
churn_date = None       # missing value
```

## Data Structures You'll Use Constantly

| Structure | Syntax | Use case |
|-----------|--------|----------|
| list | `[1, 2, 3]` | ordered, mutable sequence (a column) |
| tuple | `(lat, lon)` | fixed, immutable record |
| dict | `{"id": 1}` | key-value records (a row) |
| set | `{"a", "b"}` | unique values, fast membership |

```python
# A row as a dict
row = {"id": 7, "region": "EMEA", "revenue": 1999.5}

# A table as a list of dicts
table = [
    {"id": 7, "region": "EMEA", "revenue": 1999.5},
    {"id": 8, "region": "APAC", "revenue": 850.0},
]

regions = {r["region"] for r in table}  # set -> {'EMEA', 'APAC'}
```

## Control Flow and Comprehensions

Comprehensions are the Pythonic way to filter and transform data in one readable line.

```python
# Filter rows with revenue over 1000
high_value = [r for r in table if r["revenue"] > 1000]

# Transform into a list of just regions
region_list = [r["region"] for r in table]

# Build a lookup dict {id: revenue}
lookup = {r["id"]: r["revenue"] for r in table}
```

Use a regular loop when logic is complex or has side effects; use a comprehension when you're building a new collection.

## Writing Functions

Functions make code reusable and testable. Always add a docstring and handle the empty case.

```python
def average_revenue(rows):
    """Return the mean revenue across rows, or 0.0 if empty."""
    if not rows:
        return 0.0
    total = sum(r["revenue"] for r in rows)
    return total / len(rows)

average_revenue(table)  # -> 1424.75
```

## Handling Messy Data

Real data has gaps. Use `.get()` for safe dictionary access and `try/except` for risky conversions.

```python
def to_float(value, default=0.0):
    """Convert value to float, returning default on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

revenue = row.get("revenue", 0.0)   # no KeyError if missing
clean = to_float("1,200".replace(",", ""))
```

## Practice Exercise

Given a list of order dicts, write a function that returns total revenue per region as a dict. This combines iteration, dictionary updates, and `.get()` — the foundation of group-by logic you'll later do with pandas.
