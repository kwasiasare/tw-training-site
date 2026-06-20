---
course: data-scientist
title: 'Mini-Project: Exploratory Data Analysis Report'
month: 1
monthTitle: Python and Data Wrangling Foundations
lesson: 4
summary: In this capstone mini-project, you build an end-to-end exploratory data analysis (EDA) notebook
  on a public dataset. You will profile the data, clean it, engineer simple features, visualize distributions
  and relationships, and write up actionable initial insights in a reproducible report.
objectives:
- Load a public dataset and produce a structured data profile (shape, dtypes, missingness, summary stats)
- 'Apply systematic cleaning steps: handle missing values, fix dtypes, and remove duplicates and obvious
  errors'
- Create univariate, bivariate, and correlation visualizations to surface patterns
- Identify and document outliers and data-quality issues with clear rationale
- Translate findings into a concise, reproducible EDA report with insights and next steps
video: dsc-m1-l04-mini-project-exploratory-data-analysis-report.mp4
quiz:
- q: What is the primary purpose of the profiling step in EDA?
  options:
  - To train a predictive model
  - To build a mental model of the data's structure and quality before changing it
  - To delete all missing values
  - To deploy the notebook to production
  answer: 1
  why: Profiling (shape, dtypes, missingness, summary stats) builds your understanding of the data before
    any cleaning or modeling decisions.
- q: Which approach to missing values is recommended?
  options:
  - Always fill every column with zero
  - Always drop any row with a missing value
  - 'Decide per column: drop, impute, or flag, based on context'
  - Ignore missing values entirely
  answer: 2
  why: Missing-value handling should be column-specific and reasoned, since blanket strategies like zero-filling
    or dropping all rows can distort the data or lose information.
- q: Why should you be cautious about imputing missing values before a train/test split?
  options:
  - It makes plots harder to read
  - It causes data leakage that inflates later model performance
  - It changes the column dtypes
  - It always removes outliers
  answer: 1
  why: Imputing using statistics computed over the whole dataset leaks information from the test set into
    training, giving overly optimistic results.
- q: According to the IQR rule, an outlier is a value beyond which thresholds?
  options:
  - Mean plus or minus one standard deviation
  - Q1 minus 1.5*IQR and Q3 plus 1.5*IQR
  - The minimum and maximum values
  - Median plus or minus the mode
  answer: 1
  why: The standard IQR rule flags values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR as potential outliers.
- q: Name one element that should appear in the provenance header of your EDA notebook.
  answer: The data source (and/or download date and license)
  why: Recording the source, date, and license makes the analysis reproducible and trustworthy.
- q: In one short phrase, what should each 'Key Finding' be backed by?
  answer: A number or a plot
  why: Findings should be evidence-based — each tied to a specific statistic or visualization rather than
    vague impressions.
resources:
- label: pandas Getting Started & User Guide
  url: https://pandas.pydata.org/docs/user_guide/index.html
- label: ydata-profiling (automated EDA reports)
  url: https://docs.profiling.ydata.ai/
- label: seaborn Statistical Visualization Tutorial
  url: https://seaborn.pydata.org/tutorial.html
- label: Kaggle Datasets (public data for practice)
  url: https://www.kaggle.com/datasets
---

## What This Mini-Project Delivers

You will produce a single Jupyter notebook that takes a raw public dataset and ends with a short written set of insights. Think of it as the artifact you would hand to a stakeholder or attach to a portfolio. A good EDA report answers three questions: *What is in this data? Can I trust it? What is interesting or actionable?*

Pick a dataset with at least a few thousand rows and a mix of numeric and categorical columns. Good options include the Titanic dataset, the Ames Housing dataset, or any CSV from Kaggle or a government open-data portal.

## Step 1 — Set Up and Load

Start with a clean, reproducible header.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 50)
df = pd.read_csv('data/dataset.csv')
df.head()
```

Record the data source, download date, and license at the top of the notebook in a markdown cell. Reproducibility starts with provenance.

## Step 2 — Profile the Data

Profiling builds your mental model before you touch anything.

```python
print(df.shape)
df.info()
df.describe(include='all').T
df.isna().mean().sort_values(ascending=False)
df.duplicated().sum()
```

For each column note: its type, its meaning, the percentage missing, cardinality (for categoricals), and the range or distribution (for numerics). Tools like `ydata-profiling` (formerly pandas-profiling) can automate this, but do it manually at least once so you understand what the automated report shows.

## Step 3 — Clean Systematically

Don't clean randomly. Work column by column and log every decision.

- **Dtypes:** convert dates with `pd.to_datetime`, cast categoricals, fix numbers stored as strings.
- **Duplicates:** `df = df.drop_duplicates()` after confirming they are true duplicates.
- **Missing values:** decide per column — drop, impute with median/mode, or flag with an indicator column. Never blindly fill everything with zero.
- **Errors and impossible values:** negative ages, future dates, values outside a known domain.

```python
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['age'] = df['age'].clip(lower=0, upper=120)
df['city'] = df['city'].str.strip().str.title()
median_fare = df['fare'].median()
df['fare'] = df['fare'].fillna(median_fare)
```

## Step 4 — Visualize Distributions and Relationships

Use three layers of plots:

- **Univariate:** histograms and boxplots for numerics, bar charts for categoricals.
- **Bivariate:** scatter plots, grouped boxplots, and crosstabs against your target or key variable.
- **Multivariate:** a correlation heatmap for numeric features.

```python
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(df['age'], kde=True, ax=ax[0])
sns.boxplot(x='survived', y='fare', data=df, ax=ax[1])
plt.tight_layout()

corr = df.select_dtypes('number').corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
```

Use the IQR rule (`Q1 - 1.5*IQR`, `Q3 + 1.5*IQR`) to flag outliers, but investigate before deleting — outliers are sometimes the most interesting rows.

## Step 5 — Write the Insights

Close the notebook with a markdown section titled **Key Findings**. Each finding should be one sentence backed by a number or plot, for example: *"Passengers in first class survived at 63% vs 24% in third class, suggesting class is a strong predictor."* Add a **Data Quality Notes** list and a **Next Steps** list (modeling ideas, additional data to collect).

## Common Pitfalls

- Imputing before splitting data (causes leakage in later modeling).
- Dropping rows with any missing value, losing most of your data.
- Reporting correlation as causation.
- Charts with no titles or axis labels — always label.

## Deliverable Checklist

1. Provenance header with source and date.
2. Profiling section.
3. Documented cleaning steps.
4. At least 5 labeled visualizations.
5. Key Findings, Data Quality Notes, and Next Steps.
