---
course: data-scientist
title: Loading and Cleaning Data with Pandas
month: 1
monthTitle: Python and Data Wrangling Foundations
lesson: 2
summary: Learn to import data from common file formats, inspect its structure and quality, and systematically
  clean messy real-world datasets using pandas—handling missing values, fixing inconsistent formats, and
  preparing data for analysis.
objectives:
- Load data from CSV, Excel, and other formats into pandas DataFrames with appropriate parameters
- Inspect a dataset's structure, types, and quality using core pandas methods
- Detect and handle missing values using strategies like dropping and imputation
- Standardize inconsistent text, dates, and numeric formats
- Remove duplicates and apply type conversions to produce analysis-ready data
video: dsc-m1-l02-loading-and-cleaning-data-with-pandas.mp4
quiz:
- q: Which parameter in read_csv lets you treat strings like '-' and 'n/a' as missing values during loading?
  options:
  - parse_dates
  - na_values
  - usecols
  - dtype
  answer: 1
  why: na_values accepts a list of additional strings that pandas should interpret as NaN when reading
    the file.
- q: What does errors='coerce' do in pd.to_numeric or pd.to_datetime?
  options:
  - Raises an error and stops execution on bad values
  - Drops rows with bad values
  - Converts unparseable values to NaN/NaT
  - Ignores the conversion entirely
  answer: 2
  why: With errors='coerce', values that cannot be parsed become NaN (or NaT for dates), letting you handle
    them deliberately afterward.
- q: Which method gives you the count of missing values in each column?
  options:
  - df.info()
  - df.describe()
  - df.isna().sum()
  - df.value_counts()
  answer: 2
  why: df.isna() returns a boolean DataFrame of missing values, and .sum() totals them per column.
- q: For a numeric column with a skewed distribution, which is generally the best imputation value?
  options:
  - The mean
  - The median
  - Zero
  - The maximum
  answer: 1
  why: The median is robust to skew and outliers, making it a safer central value for skewed numeric data
    than the mean.
- q: Write the pandas method call (with no arguments) that removes exact duplicate rows from a DataFrame
    named df.
  answer: df.drop_duplicates()
  why: drop_duplicates() with no arguments removes rows that are exact duplicates across all columns,
    keeping the first occurrence by default.
- q: Which method would you use first to see column data types and non-null counts in one summary?
  options:
  - df.head()
  - df.info()
  - df.shape
  - df.describe()
  answer: 1
  why: df.info() displays each column's data type along with its non-null count, quickly revealing type
    and missingness issues.
resources:
- label: pandas IO tools (reading and writing data) documentation
  url: https://pandas.pydata.org/docs/user_guide/io.html
- label: pandas Working with missing data guide
  url: https://pandas.pydata.org/docs/user_guide/missing_data.html
- label: pandas Cookbook (practical recipes)
  url: https://pandas.pydata.org/docs/user_guide/cookbook.html
- label: 'Real Python: Cleaning Data With pandas'
  url: https://realpython.com/python-data-cleaning-numpy-pandas/
---

## Why Data Cleaning Matters

Real-world data is messy: missing values, inconsistent capitalization, mixed date formats, stray whitespace, and duplicate rows are the norm, not the exception. Data scientists routinely spend the majority of a project on loading and cleaning data before any modeling begins. Pandas is the workhorse library for this work in Python.

## Loading Data

Pandas can read many formats. The most common is CSV:

```python
import pandas as pd

df = pd.read_csv('sales.csv')
```

Useful parameters:

- `sep` — delimiter (e.g. `';'` or `'\t'`)
- `na_values` — extra strings to treat as missing (e.g. `['NA', '-', 'unknown']`)
- `parse_dates` — columns to parse as datetimes
- `dtype` — force column types
- `usecols` — load only needed columns

```python
df = pd.read_csv('sales.csv', na_values=['-', 'n/a'], parse_dates=['order_date'])
```

Other readers: `pd.read_excel()`, `pd.read_json()`, `pd.read_parquet()`, `pd.read_sql()`.

## Inspecting the Data

Always look before you clean:

```python
df.head()        # first rows
df.shape         # (rows, columns)
df.info()        # dtypes and non-null counts
df.describe()    # summary stats for numeric columns
df.isna().sum()  # missing values per column
df['city'].value_counts()  # category frequencies
```

`info()` and `isna().sum()` are your fastest signals of data-quality problems.

## Handling Missing Values

First understand *why* values are missing, then choose a strategy:

- **Drop**: `df.dropna()` removes rows; `df.dropna(axis=1)` removes columns. Use `subset=` and `thresh=` for control.
- **Impute**: fill with a sensible value.

```python
df['age'] = df['age'].fillna(df['age'].median())
df['category'] = df['category'].fillna('unknown')
```

Use the median for skewed numerics, the mean for symmetric data, and the mode or a placeholder for categories. Avoid dropping data carelessly—you may lose valuable signal.

## Fixing Inconsistent Formats

Text is a common offender:

```python
df['city'] = df['city'].str.strip().str.lower()
df['city'] = df['city'].replace({'ny': 'new york', 'nyc': 'new york'})
```

Convert types explicitly:

```python
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
```

Using `errors='coerce'` turns unparseable values into `NaN`/`NaT` so you can handle them deliberately.

## Removing Duplicates

```python
df.duplicated().sum()      # how many duplicate rows
df = df.drop_duplicates()  # remove exact duplicates
df = df.drop_duplicates(subset=['customer_id'], keep='last')
```

## A Practical Cleaning Workflow

1. Load with the right parameters.
2. Inspect shape, types, and missingness.
3. Standardize column names: `df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')`.
4. Fix data types.
5. Handle missing values.
6. Standardize text/categories.
7. Remove duplicates.
8. Validate the result with another `info()`/`describe()`.

Keep cleaning steps in a reproducible script or notebook so the same raw data always produces the same clean output.
