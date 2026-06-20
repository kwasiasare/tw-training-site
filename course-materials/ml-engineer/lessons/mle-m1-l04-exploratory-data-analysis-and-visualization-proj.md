---
course: ml-engineer
title: Exploratory Data Analysis and Visualization Project
month: 1
monthTitle: 'Foundations: Python and Math for ML'
lesson: 4
summary: 'A hands-on EDA project lesson: learn a repeatable workflow to load, clean, and explore a messy
  dataset, then communicate actionable insights with Matplotlib and Seaborn visualizations packaged into
  an EDA report.'
objectives:
- Structure a repeatable EDA workflow from raw data to insight report
- Diagnose and handle missing values, duplicates, outliers, and dtype issues
- Choose appropriate univariate, bivariate, and multivariate visualizations
- Use Matplotlib and Seaborn effectively for clear, labeled charts
- Translate visual findings into actionable, business-relevant insights
- Assemble a reproducible EDA report in a Jupyter notebook
video: mle-m1-l04-exploratory-data-analysis-and-visualization-proj.mp4
quiz:
- q: Which pandas method is best for quickly spotting columns stored with the wrong data type?
  options:
  - df.describe()
  - df.info()
  - df.head()
  - df.shape
  answer: 1
  why: df.info() lists each column's dtype and non-null count, making wrong dtypes (like numbers stored
    as objects) immediately visible.
- q: You find values of 999 in an 'age' column. What is the most appropriate first action?
  options:
  - Immediately delete all rows containing 999
  - Treat 999 as a likely missing-value placeholder and investigate
  - Scale the column to fix it
  - Ignore it since describe() handles outliers
  answer: 1
  why: 999 is a classic placeholder for missing data. You should investigate and treat it as missing rather
    than as a real age, and document the decision.
- q: Which visualization is most appropriate for comparing a numeric variable across several categories?
  options:
  - Correlation heatmap
  - Grouped boxplot or violin plot
  - Single histogram
  - Scatter plot of two numerics
  answer: 1
  why: Grouped boxplots or violin plots show the distribution of a numeric variable within each category,
    ideal for numeric-vs-categorical comparison.
- q: What makes an EDA finding 'actionable' rather than just descriptive?
  options:
  - It uses the most colorful chart available
  - It restates a summary statistic
  - It is specific, supported by a chart, and implies a decision or next step
  - It includes as many variables as possible
  answer: 2
  why: Actionable insights are specific, backed by evidence (a chart), and point toward a concrete decision
    or next step, rather than merely restating numbers.
- q: Name one essential element every chart in your EDA report should have to be self-explanatory.
  answer: A clear title (or labeled axes with units / a legend)
  why: Self-explanatory charts need clear titles, axis labels with units, readable ticks, and legends
    where appropriate so a reader understands them without extra text.
- q: In one short phrase, what is the final deliverable of this EDA project?
  answer: A reproducible EDA report with actionable insights
  why: The project deliverable is a reproducible notebook that cleans a messy dataset and ends with 3-5
    chart-supported, actionable insights plus data-quality caveats.
resources:
- label: Seaborn official tutorial
  url: https://seaborn.pydata.org/tutorial.html
- label: pandas Getting Started & Data Cleaning guide
  url: https://pandas.pydata.org/docs/getting_started/index.html
- label: Matplotlib Pyplot tutorial
  url: https://matplotlib.org/stable/tutorials/pyplot.html
- label: 'Kaggle: Data Cleaning course'
  url: https://www.kaggle.com/learn/data-cleaning
---

## Why EDA Matters

Exploratory Data Analysis (EDA) is the first real contact a Machine Learning Engineer has with data. Before building any model, you must understand the data's shape, quality, distributions, and relationships. Good EDA prevents garbage-in/garbage-out, surfaces data quality problems early, and generates hypotheses worth modeling.

The goal of this project is to produce an **EDA report** — a clean, narrated Jupyter notebook that takes a messy dataset and ends with 3-5 actionable insights backed by visualizations.

## A Repeatable EDA Workflow

1. **Understand the context** — What does each column mean? What is the target/question?
2. **Load and inspect** — shape, `head()`, `dtypes`, `info()`, `describe()`.
3. **Assess data quality** — missing values, duplicates, impossible values, inconsistent categories.
4. **Clean** — fix dtypes, parse dates, standardize categories, handle missing data.
5. **Univariate analysis** — distribution of each variable.
6. **Bivariate / multivariate analysis** — relationships, correlations, group comparisons.
7. **Synthesize insights** — write down what you found and what it implies.

## Loading and First Look

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')

df = pd.read_csv('sales.csv')
print(df.shape)
df.info()
df.describe(include='all')
```

Use `df.info()` to spot wrong dtypes (e.g., numbers stored as objects) and `df.describe()` to catch suspicious min/max values (a negative age, a price of 0).

## Assessing Data Quality

```python
# Missing values
df.isna().sum().sort_values(ascending=False)
(df.isna().mean() * 100).round(1)  # percent missing

# Duplicates
df.duplicated().sum()

# Inconsistent categories
df['country'].value_counts(dropna=False)
```

Common messiness: `'USA'`, `'usa'`, `'United States'` all meaning the same thing; whitespace; mixed case; placeholder values like `-1` or `999`.

## Cleaning Strategies

- **Dtypes:** `pd.to_numeric(..., errors='coerce')`, `pd.to_datetime(...)`.
- **Standardize text:** `df['country'].str.strip().str.lower().replace(mapping)`.
- **Missing data:** decide per column — drop, impute (median for skewed numerics, mode for categoricals), or flag with an indicator column. Document your choice.
- **Outliers:** investigate before deleting. Use the IQR rule or domain knowledge; an outlier may be the most interesting signal.

```python
q1, q3 = df['price'].quantile([0.25, 0.75])
iqr = q3 - q1
mask = df['price'].between(q1 - 1.5*iqr, q3 + 1.5*iqr)
```

## Univariate Visualization

- **Numeric:** histogram (`sns.histplot`), boxplot (`sns.boxplot`), KDE.
- **Categorical:** count plot (`sns.countplot`), bar chart.

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(df['price'], kde=True, ax=axes[0])
axes[0].set_title('Price distribution')
sns.boxplot(x=df['price'], ax=axes[1])
axes[1].set_title('Price spread')
plt.tight_layout()
```

## Bivariate and Multivariate Visualization

- **Numeric vs numeric:** scatter (`sns.scatterplot`), correlation heatmap.
- **Numeric vs categorical:** boxplot/violin grouped by category.
- **Categorical vs categorical:** grouped bar charts, crosstab heatmaps.

```python
corr = df.select_dtypes('number').corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)

sns.scatterplot(data=df, x='ad_spend', y='revenue', hue='region')
```

Use `hue`, `size`, and `sns.FacetGrid`/`sns.pairplot` to add dimensions, but avoid overcrowding a single chart.

## Making Charts Communicate

Every chart should be self-explanatory: a clear title, labeled axes with units, readable tick labels, and a legend when needed. Prefer a few sharp charts over many noisy ones. Use color intentionally — not decoratively.

## Synthesizing Insights

End your report with a short "Key Findings" section. Each insight should be: (1) specific, (2) supported by a chart, and (3) actionable. Example: "Revenue per ad dollar is 2x higher in the North region; consider reallocating budget." Avoid restating obvious statistics without interpretation.

## Deliverable Checklist

- Reproducible notebook (runs top to bottom).
- Documented cleaning decisions.
- Labeled, purposeful visualizations.
- 3-5 written, actionable insights.
- A short data-quality caveats section.
