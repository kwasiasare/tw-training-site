---
course: data-scientist
title: 'Mini-Project: SQL-Driven Statistical Analysis'
month: 2
monthTitle: Statistics and SQL for Analysis
lesson: 4
summary: In this hands-on mini-project you combine SQL data extraction with statistical hypothesis testing
  to investigate a real business question end-to-end. You'll frame a hypothesis, write SQL to pull a clean
  analysis-ready dataset, validate assumptions, run an appropriate statistical test in Python, and document
  your findings in a reproducible report.
objectives:
- Translate a business question into a testable statistical hypothesis with clear null and alternative
  statements
- Write SQL queries that extract, aggregate, and clean an analysis-ready dataset
- Select and run an appropriate statistical test (t-test, chi-square, or proportion test) based on data
  type and assumptions
- Interpret p-values, effect sizes, and confidence intervals in plain business language
- Document the full workflow in a reproducible, peer-readable analysis report
video: dsc-m2-l04-mini-project-sql-driven-statistical-analysis.mp4
quiz:
- q: What should you decide before extracting or looking at any data?
  options:
  - The exact p-value you want
  - The significance level (alpha) and hypotheses
  - The color scheme of your charts
  - Which database engine to use
  answer: 1
  why: Fixing alpha and stating H0/H1 before analysis prevents p-hacking and keeps the test valid.
- q: Order value is strongly right-skewed with a few extreme outliers. Which is the most appropriate response?
  options:
  - Ignore it; the t-test always works
  - Consider a log transform or a non-parametric test like Mann-Whitney U
  - Delete all orders above the mean
  - Switch to a chi-square test
  answer: 1
  why: Skewed continuous data can violate t-test assumptions; a transform or non-parametric test is more
    robust, while chi-square is for categorical data.
- q: Why must you report an effect size in addition to the p-value?
  options:
  - P-values are always wrong
  - Effect size measures practical importance, which significance alone does not
  - It is required by SQL
  - Effect size replaces the hypothesis
  answer: 1
  why: A result can be statistically significant yet practically trivial, especially with large samples;
    effect size quantifies the magnitude.
- q: Which test fits comparing the conversion RATE (a proportion) between two variants?
  options:
  - Welch's t-test
  - Two-proportion z-test or chi-square test
  - Pearson correlation
  - Linear regression of order_id
  answer: 1
  why: Conversion rate is a categorical/proportion outcome, so a two-proportion z-test or chi-square test
    is appropriate.
- q: In one sentence, why should you verify your SQL joins before running statistics?
  answer: Because a join that fans out rows duplicates observations, inflating sample size and biasing
    means and test results.
  why: Duplicated rows break the assumption of one independent observation per unit and distort every
    downstream statistic.
- q: Name one piece of information, besides the p-value, that a complete analysis report should include.
  answer: Effect size, confidence interval, the SQL used, assumption checks, or stated limitations (any
    one).
  why: A defensible report documents the full workflow and the magnitude/uncertainty of the result, not
    just whether p < alpha.
resources:
- label: 'SciPy stats: statistical tests reference'
  url: https://docs.scipy.org/doc/scipy/reference/stats.html
- label: pandas read_sql documentation
  url: https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html
- label: Mode SQL Tutorial (intermediate to advanced)
  url: https://mode.com/sql-tutorial/
- label: 'StatQuest: Hypothesis Testing and p-values (video series)'
  url: https://www.youtube.com/c/joshstarmer
---

## Overview

This mini-project ties together the two pillars of analytical work: **getting the right data** (SQL) and **drawing defensible conclusions from it** (statistics). Real data science rarely starts with a tidy CSV. You query a database, shape the data, then test a hypothesis and communicate the result.

We'll use a running example: *Does a new checkout flow (variant B) increase the average order value compared to the old flow (variant A)?*

## Step 1 — Frame the Hypothesis

Before touching data, write down:

- **Null hypothesis (H0):** There is no difference in mean order value between variants A and B.
- **Alternative (H1):** Variant B has a different (or higher) mean order value than A.
- **Significance level (alpha):** Typically 0.05.
- **Metric and unit of analysis:** Order value per completed order.

A clear hypothesis prevents "p-hacking" — fishing through data until something looks significant.

## Step 2 — Extract Data with SQL

Pull only what you need, at the correct grain. Filter out test accounts, refunds, and incomplete orders.

```sql
SELECT
    o.order_id,
    e.variant,
    o.order_value
FROM orders o
JOIN experiment_assignment e
    ON o.user_id = e.user_id
WHERE o.status = 'completed'
  AND o.created_at >= '2024-01-01'
  AND e.experiment = 'checkout_v2'
  AND o.is_test = FALSE;
```

Good extraction habits:

- **Filter at the source** — smaller, cleaner data downstream.
- **Keep the grain explicit** — one row per order here.
- **Avoid silent duplication** — verify joins don't fan out rows.

You can also compute group summaries directly in SQL as a sanity check:

```sql
SELECT
    variant,
    COUNT(*)        AS n_orders,
    AVG(order_value) AS mean_value,
    STDDEV(order_value) AS sd_value
FROM ... -- same query as above wrapped
GROUP BY variant;
```

## Step 3 — Validate Assumptions

Before running a test, check that its assumptions hold:

- **Sample size** — enough observations per group (rule of thumb >30 for CLT to help).
- **Distribution** — order value is often right-skewed; consider a log transform or a non-parametric test (Mann-Whitney U).
- **Independence** — one observation per user, or account for repeat customers.
- **Outliers** — a single huge order can dominate a mean; inspect with a boxplot.

## Step 4 — Run the Statistical Test

For comparing two group means, use an independent two-sample t-test (Welch's version does not assume equal variances).

```python
import pandas as pd
from scipy import stats

df = pd.read_sql(query, conn)
a = df.loc[df.variant == 'A', 'order_value']
b = df.loc[df.variant == 'B', 'order_value']

t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)
print(f't = {t_stat:.3f}, p = {p_value:.4f}')
```

Report an **effect size** too — statistical significance is not practical significance:

```python
import numpy as np

# Simple pooled SD: an approximation valid for roughly equal sample sizes
pooled_sd = np.sqrt((a.var() + b.var()) / 2)
cohens_d = (b.mean() - a.mean()) / pooled_sd
print(f"Cohen's d = {cohens_d:.3f}")

# More accurate for unequal n: the df-weighted pooled SD
# n1, n2 = len(a), len(b)
# pooled_sd = np.sqrt(((n1-1)*a.var(ddof=1) + (n2-1)*b.var(ddof=1)) / (n1+n2-2))
```

The simple `pooled_sd` above is an approximation that holds when the two groups are similar in size; for unequal samples, use the degrees-of-freedom-weighted pooled SD shown in the comment (with `var(ddof=1)`).

For categorical outcomes (e.g., conversion rate), use a **chi-square test** or a **two-proportion z-test** instead.

## Step 5 — Interpret and Document

Translate numbers into a decision:

- If `p < alpha`, reject H0: the difference is unlikely due to chance.
- Always pair the p-value with the **effect size** and a **confidence interval** for the difference in means.
- State limitations: time window, confounders, novelty effects.

A good report contains: the question, the hypothesis, the SQL used, assumption checks, the test and result, the effect size, and a one-line recommendation.

## Common Pitfalls

- Reading significance as importance — a tiny, useless lift can be "significant" with huge samples.
- Ignoring multiple comparisons — testing many metrics inflates false positives.
- Forgetting to deduplicate users before treating orders as independent.
- Letting outliers or skew silently break the t-test's assumptions.

## Deliverable

Produce a short notebook or markdown report investigating one hypothesis on a dataset of your choice, including the SQL, the test, the effect size, and a plain-language conclusion.
