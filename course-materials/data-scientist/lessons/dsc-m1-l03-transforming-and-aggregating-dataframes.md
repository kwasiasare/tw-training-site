---
course: data-scientist
title: Transforming and Aggregating DataFrames
month: 1
monthTitle: Python and Data Wrangling Foundations
lesson: 3
summary: Learn to transform and aggregate pandas DataFrames using filtering, grouping, joining, and reshaping
  so you can summarize raw data into business-ready insights.
objectives:
- Filter and select DataFrame rows and columns using boolean masks and query expressions
- Aggregate data with groupby and named aggregations to compute summary statistics
- Combine datasets using merge and join operations with the appropriate join type
- Reshape data between wide and long formats using pivot_table, melt, and stack/unstack
- Chain transformations into readable pipelines that answer concrete business questions
video: dsc-m1-l03-transforming-and-aggregating-dataframes.mp4
quiz:
- q: Which expression correctly filters for rows where country is 'US' AND revenue exceeds 1000?
  options:
  - df[df['country']=='US' & df['revenue']>1000]
  - df[(df['country']=='US') & (df['revenue']>1000)]
  - df[df['country']=='US' and df['revenue']>1000]
  - df.filter('country==US', 'revenue>1000')
  answer: 1
  why: Each condition must be wrapped in parentheses and combined with & (not the keyword 'and') because
    of operator precedence and elementwise evaluation.
- q: What does named aggregation like total=('revenue','sum') primarily give you?
  options:
  - Faster computation than .sum()
  - Automatic joining of tables
  - Clean, predictable output column names
  - Conversion from wide to long format
  answer: 2
  why: Named aggregation lets you specify the output column name along with the source column and function,
    producing readable, predictable results.
- q: You merge orders with customers using how='left'. After the merge you have more rows than the original
    orders table. What is the most likely cause?
  options:
  - The join type should have been inner
  - Duplicate keys in customers caused a many-to-many match
  - melt was applied automatically
  - reset_index added extra rows
  answer: 1
  why: A left join keeps all left rows, but if the right table has duplicate keys each match multiplies
    rows, increasing the count. Checking counts and using validate= catches this.
- q: Which function converts wide-format data back into long/tidy format?
  options:
  - pivot_table
  - melt
  - groupby
  - merge
  answer: 1
  why: melt unpivots columns into rows, producing long/tidy data that plotting and modeling tools prefer.
- q: In one sentence, describe the 'split-apply-combine' pattern used by groupby.
  answer: Data is split into groups by key, a function is applied to each group, and the results are combined
    into one summary table.
  why: This three-step pattern is the conceptual foundation of groupby aggregation in pandas.
- q: Which join type keeps ALL rows from both DataFrames, filling missing matches with NaN?
  options:
  - inner
  - left
  - right
  - outer
  answer: 3
  why: An outer join returns the union of keys from both tables, inserting NaN where one side has no match.
resources:
- label: 'pandas Group By: split-apply-combine (official docs)'
  url: https://pandas.pydata.org/docs/user_guide/groupby.html
- label: pandas Merge, join, concatenate (official docs)
  url: https://pandas.pydata.org/docs/user_guide/merging.html
- label: pandas Reshaping and pivot tables (official docs)
  url: https://pandas.pydata.org/docs/user_guide/reshaping.html
- label: Tidy Data by Hadley Wickham
  url: https://vita.had.co.nz/papers/tidy-data.pdf
---

## Why Transformation and Aggregation Matter

Raw data rarely answers business questions directly. A data scientist's daily work is reshaping messy tables into clean summaries: *average revenue per region*, *churn rate per cohort*, *top products per month*. Pandas gives you a small set of composable verbs—filter, group, join, reshape—that cover the vast majority of these tasks.

## Filtering and Selecting

Use boolean masks to keep the rows you care about:

```python
high_value = df[df["revenue"] > 1000]
recent_us = df[(df["country"] == "US") & (df["year"] >= 2023)]
```

Combine conditions with `&` (and), `|` (or), `~` (not), and wrap each condition in parentheses. For readability, `df.query("revenue > 1000 and country == 'US'")` is often cleaner. Select columns with `df[["a", "b"]]` or `df.loc[:, ["a", "b"]]`.

## Grouping and Aggregating

`groupby` splits the data into groups, applies a function, and combines the results—the *split-apply-combine* pattern.

```python
summary = (
    df.groupby("region")
      .agg(
          total_revenue=("revenue", "sum"),
          avg_order=("revenue", "mean"),
          orders=("order_id", "count"),
      )
      .reset_index()
)
```

Named aggregation (`new_col=("source_col", "func")`) produces clean, predictable column names. You can group by multiple keys: `df.groupby(["region", "year"])`. Use `.reset_index()` to turn group keys back into regular columns.

## Joining DataFrames

Use `merge` to combine tables on shared keys—similar to SQL joins:

```python
orders.merge(customers, on="customer_id", how="left")
```

Join types:
- **inner**: only matching keys in both tables
- **left**: all rows from the left table, matched where possible
- **right**: all rows from the right table
- **outer**: all rows from both, filling gaps with NaN

Always check row counts before and after a join—unexpected growth usually means duplicate keys causing a many-to-many explosion. Use `validate="one_to_many"` to enforce assumptions.

## Reshaping: Wide vs Long

Long (tidy) format has one observation per row; wide format spreads a variable across columns.

```python
# long -> wide
pivot = df.pivot_table(index="region", columns="year",
                       values="revenue", aggfunc="sum")

# wide -> long
long = pivot.reset_index().melt(id_vars="region",
                                var_name="year", value_name="revenue")
```

`pivot_table` aggregates duplicates automatically; `pivot` does not. Use `melt` to unpivot for plotting or modeling, which generally prefer long/tidy data.

## Putting It Together

A typical pipeline filters, joins reference data, groups, and reshapes—often chained with method calls. Keep steps small, name intermediate results when debugging, and validate row counts at each stage. This workflow turns raw transactional data into the summary tables that drive dashboards and decisions.
