---
title: 'Pandas: clean, transform, group, merge'
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 4
summary: Use pandas DataFrames to load messy data, clean it, transform columns, group and aggregate, then
  merge tables together.
objectives:
- Load data into a DataFrame and inspect it with head, info and describe
- Select rows and columns using loc and iloc
- Clean missing values with dropna and fillna
- Transform columns with vectorised operations and assign
- Summarise data with groupby and aggregation
- Combine tables with merge on a shared key
- Save a cleaned DataFrame back to CSV
video: m2-l04-pandas.mp4
quiz:
- q: What is the primary 2D data structure in pandas?
  options:
  - Series
  - DataFrame
  - Array
  - Table
  answer: 1
  why: A DataFrame is the table-like 2D structure with rows and labelled columns; a Series is a single
    column.
- q: Which method selects rows and columns by their labels?
  options:
  - iloc
  - loc
  - at_index
  - select
  answer: 1
  why: loc selects by label; iloc selects by integer position. df.loc[2, 'age'] uses labels.
- q: What does df.groupby('city')['sales'].sum() return?
  answer: A Series of total sales for each city, indexed by city.
  why: groupby splits rows by city, then sum aggregates the sales column within each group into one value
    per city.
- q: Which call fills missing values with 0 instead of deleting rows?
  options:
  - df.dropna(0)
  - df.fillna(0)
  - df.isna(0)
  - df.replace(0)
  answer: 1
  why: fillna(0) replaces NaN with 0 and keeps every row; dropna would remove rows containing missing
    values.
- q: In df.merge(other, on='id', how='left'), what does how='left' do?
  answer: It keeps every row from the left DataFrame and attaches matching rows from the right, filling
    NaN where there is no match.
  why: A left join preserves all left-side rows; unmatched right-side columns become NaN, like a SQL LEFT
    JOIN.
- q: Why are pandas vectorised operations like df['a'] * 2 preferred over a Python for-loop?
  answer: They run in fast compiled C code over the whole column at once, so they are much faster and
    shorter than looping row by row.
  why: Vectorisation avoids slow per-row Python overhead and is the idiomatic, performant way to transform
    columns.
resources:
- label: pandas — Getting started tutorials (official docs)
  url: https://pandas.pydata.org/docs/getting_started/index.html
- label: 10 Minutes to pandas (official quickstart)
  url: https://pandas.pydata.org/docs/user_guide/10min.html
- label: Python for Data Analysis, 3rd ed. (Wes McKinney, creator of pandas)
  url: https://wesmckinney.com/book/
- label: Kaggle — Pandas course (free, hands-on)
  url: https://www.kaggle.com/learn/pandas
---

## What is pandas?

**pandas** is the standard Python library for working with tabular data — the kind you find in spreadsheets, CSV files and SQL tables. Its core object is the **DataFrame**: rows and labelled columns, like a sheet in Excel but programmable.

As a maths graduate, think of a DataFrame as a matrix where every column has a name and can hold a different type. Most real data science work is *getting the data into shape* before any modelling happens.

```python
import pandas as pd

df = pd.read_csv("sales.csv")
print(df.head())     # first 5 rows
print(df.info())     # columns, types, missing counts
print(df.describe()) # summary stats for numeric columns
```

## Selecting data

Use `loc` to select by **label** and `iloc` to select by **integer position**. You can filter rows with a boolean condition, which is how you ask questions of your data.

```python
df["price"]              # one column (a Series)
df.loc[0, "price"]       # row label 0, column 'price'
df.iloc[0, 2]            # first row, third column
df[df["price"] > 100]    # rows where price exceeds 100
```

## Cleaning missing data

Real data is messy. Missing values show up as **NaN**. You either drop them or fill them — the right choice depends on the column.

```python
df.isna().sum()             # count missing per column
df = df.dropna(subset=["price"])   # drop rows missing price
df["city"] = df["city"].fillna("unknown")
```

## Transforming columns

Do maths on whole columns at once — this is **vectorisation**, and it is far faster and clearer than a Python loop. Use `assign` or direct assignment to add new columns.

```python
df["total"] = df["price"] * df["quantity"]
df["price_gbp"] = df["price"].round(2)
df["name"] = df["name"].str.strip().str.title()
```

## Grouping and aggregating

`groupby` follows a **split–apply–combine** pattern: split rows into groups, apply a function to each group, combine the results. This is how you turn raw rows into insight.

```python
df.groupby("city")["total"].sum()
df.groupby("city").agg(
    revenue=("total", "sum"),
    orders=("total", "count"),
)
```

## Merging tables

Data often lives across several tables. `merge` joins them on a shared **key**, exactly like a SQL join. `how` controls which rows are kept: inner, left, right or outer.

```python
orders = pd.read_csv("orders.csv")
customers = pd.read_csv("customers.csv")
joined = orders.merge(customers, on="customer_id", how="left")
joined.to_csv("orders_clean.csv", index=False)
```

## Your task

Take a CSV with missing values, **clean it, add one new column, group by a category, and merge in a second table**.
