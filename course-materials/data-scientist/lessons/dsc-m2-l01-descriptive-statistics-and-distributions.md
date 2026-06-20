---
course: data-scientist
title: Descriptive Statistics and Distributions
month: 2
monthTitle: Statistics and SQL for Analysis
lesson: 1
summary: A practical introduction to descriptive statistics and probability distributions for data scientists.
  You'll learn to compute and interpret measures of central tendency and spread, recognize common distributions,
  and use these tools to quantitatively characterize real datasets in Python.
objectives:
- 'Compute and interpret measures of central tendency: mean, median, and mode'
- Quantify spread using variance, standard deviation, range, IQR, and percentiles
- Identify and describe skewness and the effect of outliers on summary statistics
- Recognize common distributions (normal, uniform, binomial, Poisson, log-normal) and their use cases
- Apply pandas and NumPy to generate descriptive summaries of real datasets
- Interpret the empirical rule and use distribution shape to guide analysis decisions
video: dsc-m2-l01-descriptive-statistics-and-distributions.mp4
quiz:
- q: Which measure of central tendency is most robust to outliers?
  options:
  - Mean
  - Median
  - Range
  - Variance
  answer: 1
  why: The median is the middle value and is unaffected by extreme values, unlike the mean which gets
    pulled toward outliers.
- q: For an approximately normal distribution, roughly what percentage of data falls within two standard
    deviations of the mean?
  options:
  - 50%
  - 68%
  - 95%
  - 99.7%
  answer: 2
  why: The empirical rule states about 95% of data lies within two standard deviations of the mean.
- q: 'If a dataset''s mean is much larger than its median, the distribution is most likely:'
  options:
  - Left-skewed
  - Symmetric
  - Right-skewed
  - Uniform
  answer: 2
  why: When the mean exceeds the median, a long right tail pulls the mean upward, indicating right (positive)
    skew.
- q: Which distribution best models the number of customer arrivals at a store per hour?
  options:
  - Normal
  - Poisson
  - Uniform
  - Log-normal
  answer: 1
  why: The Poisson distribution models counts of events occurring in a fixed interval of time or space.
- q: Why does sample variance divide by n−1 instead of n?
  answer: Dividing by n−1 (Bessel's correction) corrects for bias, giving an unbiased estimate of the
    population variance since the sample mean is used in the calculation.
  why: Using the sample mean underestimates spread, so dividing by n−1 instead of n compensates and yields
    an unbiased estimator.
- q: Using the 1.5×IQR rule, write the upper threshold above which a value is flagged as an outlier (in
    terms of Q1, Q3, and IQR).
  answer: Q3 + 1.5 * IQR
  why: Values above Q3 plus 1.5 times the interquartile range are considered potential outliers.
resources:
- label: pandas DataFrame.describe() documentation
  url: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html
- label: SciPy stats module (distributions and descriptive stats)
  url: https://docs.scipy.org/doc/scipy/reference/stats.html
- label: 'Khan Academy: Summarizing quantitative data'
  url: https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data
- label: Seaborn distribution plots tutorial
  url: https://seaborn.pydata.org/tutorial/distributions.html
---

## Why Descriptive Statistics Matter

Before building models, a data scientist must understand the data. Descriptive statistics summarize a dataset's key features with a few numbers, letting you spot errors, outliers, and patterns quickly. They answer: *Where is the center? How spread out is it? What shape does it take?*

## Central Tendency

Three common measures of the 'center' of data:

- **Mean** — the arithmetic average. Sensitive to outliers. `sum(x) / n`.
- **Median** — the middle value when sorted. Robust to outliers; better for skewed data like income.
- **Mode** — the most frequent value. Useful for categorical data.

When mean ≈ median, the distribution is roughly symmetric. When mean > median, it's right-skewed (long right tail); when mean < median, it's left-skewed.

## Measures of Spread

Central tendency alone is misleading — two datasets can share a mean but differ wildly in variability.

- **Range** = max − min. Simple but very sensitive to extremes.
- **Variance** = average squared deviation from the mean. Note: sample variance divides by `n-1` (Bessel's correction) for an unbiased estimate.
- **Standard deviation** = square root of variance; in the same units as the data.
- **IQR (Interquartile Range)** = Q3 − Q1, the middle 50% of data. Robust to outliers and used for box plots.
- **Percentiles/Quantiles** describe relative position (e.g., the 90th percentile).

A common outlier rule: values below `Q1 - 1.5*IQR` or above `Q3 + 1.5*IQR` are flagged.

## Shape: Skewness and Kurtosis

- **Skewness** measures asymmetry. Positive = right tail longer; negative = left tail longer.
- **Kurtosis** measures tail heaviness. High kurtosis means more extreme outliers than a normal distribution.

## Common Distributions

| Distribution | Type | Typical use |
|---|---|---|
| **Normal (Gaussian)** | Continuous | Heights, measurement errors; foundation for many tests |
| **Uniform** | Continuous/Discrete | Equal probability outcomes; random sampling |
| **Binomial** | Discrete | Count of successes in n trials (conversions, clicks) |
| **Poisson** | Discrete | Counts of events in a fixed interval (arrivals per hour) |
| **Log-normal** | Continuous | Right-skewed positive data (income, prices) |

### The Empirical Rule (Normal Distribution)

For an approximately normal distribution:
- ~68% of data lies within 1 standard deviation of the mean
- ~95% within 2 standard deviations
- ~99.7% within 3 standard deviations

This rule helps you sanity-check spread and identify how unusual a value is (via z-scores: `z = (x - mean) / std`).

## Doing It in Python

```python
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')

# Quick summary of all numeric columns
print(df.describe())

# Individual statistics
col = df['salary']
print('mean:', col.mean())
print('median:', col.median())
print('std:', col.std())        # sample std (ddof=1 by default in pandas)
print('IQR:', col.quantile(0.75) - col.quantile(0.25))
print('skew:', col.skew())
```

Note: pandas `.std()` uses `ddof=1` (sample) by default, while NumPy `np.std()` uses `ddof=0` (population) — be explicit to avoid subtle bugs.

## Practical Workflow

1. Run `df.describe()` and `df.info()` first.
2. Plot histograms and box plots to see shape and outliers.
3. Choose mean vs. median based on skew.
4. Use IQR or z-scores to flag outliers before modeling.
5. Match the data's shape to a candidate distribution to inform downstream methods.
