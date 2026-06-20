---
course: ml-engineer
title: Statistics and Probability for Data-Driven Decisions
month: 1
monthTitle: 'Foundations: Python and Math for ML'
lesson: 3
summary: This lesson equips you with the core statistical and probabilistic tools Machine Learning Engineers
  use to validate patterns in data. You'll work with common probability distributions, run hypothesis
  tests, and compute confidence intervals to turn raw observations into defensible, data-driven decisions.
objectives:
- Identify and apply common probability distributions (normal, binomial, Bernoulli) to model real data
- Distinguish between population parameters and sample statistics, and explain sampling variability
- Construct and interpret confidence intervals for means and proportions
- Formulate null and alternative hypotheses and run t-tests and proportion tests
- Interpret p-values, significance levels, and the risks of Type I/II errors correctly
- Translate statistical results into practical ML decisions (e.g., model comparison, A/B tests)
video: mle-m1-l03-statistics-and-probability-for-data-driven-decis.mp4
quiz:
- q: What does the Central Limit Theorem tell us?
  options:
  - All data is normally distributed
  - Sample means approach a normal distribution as n grows
  - Larger samples always have larger variance
  - The population mean equals the sample mean exactly
  answer: 1
  why: The CLT states that the distribution of sample means tends toward normal as sample size increases,
    regardless of the underlying population distribution.
- q: 'A p-value of 0.03 with \u03b1 = 0.05 means:'
  options:
  - The null hypothesis is definitely false
  - We reject the null hypothesis at the 5% level
  - There is a 3% chance the alternative is true
  - The effect is practically large
  answer: 1
  why: Since 0.03 < 0.05, we reject the null. The p-value is the probability of data this extreme under
    the null, not the probability the hypothesis is true, and says nothing about effect size.
- q: Which formula gives the standard error of the mean?
  options:
  - s \u00d7 sqrt(n)
  - s / n
  - s / sqrt(n)
  - sqrt(s) / n
  answer: 2
  why: The standard error of the mean is the sample standard deviation divided by the square root of the
    sample size, so it shrinks as n grows.
- q: What type of error is a false positive?
  options:
  - Type I error
  - Type II error
  - Sampling error
  - Measurement error
  answer: 0
  why: A Type I error is rejecting a true null hypothesis, i.e., a false positive, and its rate is controlled
    by the significance level \u03b1.
- q: In one sentence, explain the correct interpretation of a 95% confidence interval.
  answer: If we repeated the sampling procedure many times, about 95% of the constructed intervals would
    contain the true population parameter.
  why: The 95% refers to the long-run reliability of the procedure, not the probability that a single
    specific interval contains the true value.
- q: Why should you report effect size alongside a p-value?
  answer: Because statistical significance does not imply practical importance; effect size shows how
    large and meaningful the difference actually is.
  why: With large samples even tiny, unimportant differences can be statistically significant, so effect
    size is needed to judge real-world relevance.
resources:
- label: SciPy stats module documentation
  url: https://docs.scipy.org/doc/scipy/reference/stats.html
- label: 'Seeing Theory: Visual Introduction to Probability and Statistics'
  url: https://seeing-theory.brown.edu/
- label: 'StatQuest: Statistics Fundamentals (YouTube playlist)'
  url: https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9
- label: Think Stats by Allen B. Downey (free book)
  url: https://greenteapress.com/wp/think-stats-2e/
---

## Why Statistics Matters for ML Engineers

Machine Learning is applied statistics at scale. Before trusting a model or a metric improvement, you must know whether a pattern is *real* or just noise. This lesson gives you the practical toolkit: distributions to model uncertainty, confidence intervals to quantify it, and hypothesis tests to validate claims.

## Probability Distributions

A distribution describes how likely each value of a random variable is.

- **Bernoulli**: single yes/no trial with success probability `p` (e.g., did a user click?).
- **Binomial**: number of successes in `n` independent Bernoulli trials.
- **Normal (Gaussian)**: bell-shaped, defined by mean `\u03bc` and standard deviation `\u03c3`. Many averages converge to it.

The **Central Limit Theorem (CLT)** is foundational: the distribution of sample means approaches a normal distribution as sample size grows, regardless of the underlying distribution. This is why normal-based methods work so widely.

```python
import numpy as np
from scipy import stats

# Sample means become normal (CLT)
data = np.random.exponential(scale=2.0, size=10000)
sample_means = [np.mean(np.random.choice(data, 50)) for _ in range(1000)]
print(np.mean(sample_means), np.std(sample_means))
```

## Population vs Sample

We rarely measure the whole **population**; we work with a **sample**. Sample statistics (mean `x\u0304`, std `s`) estimate population parameters (`\u03bc`, `\u03c3`). Because samples vary, every estimate carries uncertainty called the **standard error**:

`SE = s / sqrt(n)`

Larger samples shrink the standard error, making estimates more precise.

## Confidence Intervals

A **95% confidence interval (CI)** is a range that would contain the true parameter in 95% of repeated samples. For a mean:

`CI = x\u0304 \u00b1 t* \u00d7 SE`

```python
import numpy as np
from scipy import stats

sample = np.array([12, 15, 14, 10, 13, 16, 11, 14])
mean = sample.mean()
se = stats.sem(sample)
ci = stats.t.interval(0.95, len(sample)-1, loc=mean, scale=se)
print(f"Mean={mean:.2f}, 95% CI={ci}")
```

Interpretation tip: the CI describes the *procedure's* reliability, not the probability that this specific interval holds the truth.

## Hypothesis Testing

A hypothesis test asks: is an observed effect likely under the assumption of *no effect*?

1. **Null hypothesis (H\u2080)**: no effect / no difference.
2. **Alternative hypothesis (H\u2081)**: there is an effect.
3. Choose a **significance level** `\u03b1` (commonly 0.05).
4. Compute a **test statistic** and its **p-value**.
5. If p-value < `\u03b1`, reject H\u2080.

The **p-value** is the probability of observing data at least as extreme as ours, *assuming H\u2080 is true*. A small p-value means the data is surprising under the null.

```python
from scipy import stats

# Two-sample t-test: did model B beat model A on accuracy?
model_a = [0.81, 0.79, 0.82, 0.80, 0.78]
model_b = [0.84, 0.85, 0.83, 0.86, 0.82]
t_stat, p = stats.ttest_ind(model_b, model_a)
print(f"t={t_stat:.3f}, p={p:.4f}")
```

## Errors and Pitfalls

- **Type I error (false positive)**: rejecting a true null. Controlled by `\u03b1`.
- **Type II error (false negative)**: failing to reject a false null. Related to **statistical power**.
- **p-hacking**: testing many things until something looks significant. Pre-register hypotheses and correct for multiple comparisons.
- Statistical significance \u2260 practical significance. Always check **effect size**.

## Applying This in ML

- Compare models with proper tests rather than a single accuracy number.
- Run A/B tests with proportion tests to validate feature launches.
- Report metrics with confidence intervals, not just point estimates.
- Use distributions to detect data drift and anomalies in production.
