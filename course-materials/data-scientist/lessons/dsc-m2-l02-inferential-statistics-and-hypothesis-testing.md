---
course: data-scientist
title: Inferential Statistics and Hypothesis Testing
month: 2
monthTitle: Statistics and SQL for Analysis
lesson: 2
summary: 'This lesson teaches the core tools of inferential statistics for data scientists: confidence
  intervals for estimating population parameters, t-tests for comparing means, and chi-square tests for
  categorical relationships. You will learn how to frame hypotheses, interpret p-values, choose the right
  test, and avoid common pitfalls when drawing conclusions from samples.'
objectives:
- Distinguish between descriptive and inferential statistics and explain the role of sampling.
- Construct and interpret confidence intervals for means and proportions.
- Formulate null and alternative hypotheses and interpret p-values and significance levels.
- Select and apply the appropriate t-test (one-sample, two-sample, paired) for comparing means.
- Apply chi-square tests of independence and goodness-of-fit to categorical data.
- Recognize common errors such as p-hacking, Type I/II errors, and misinterpreting significance.
video: dsc-m2-l02-inferential-statistics-and-hypothesis-testing.mp4
quiz:
- q: What does a 95% confidence interval actually mean?
  options:
  - There is a 95% probability the true parameter is in this specific interval
  - If we repeated sampling many times, about 95% of such intervals would contain the true parameter
  - 95% of the data falls within the interval
  - The sample mean is correct 95% of the time
  answer: 1
  why: 'A confidence level refers to the long-run procedure: 95% of intervals built this way capture the
    true parameter. It is not a probability statement about one fixed interval.'
- q: Which test is most appropriate for comparing the mean conversion time before and after a UI change
    measured on the same users?
  options:
  - Two-sample independent t-test
  - Chi-square test of independence
  - Paired t-test
  - One-sample z-test
  answer: 2
  why: Measurements are taken on the same subjects before and after, so observations are paired, calling
    for a paired t-test.
- q: 'A p-value of 0.03 with α = 0.05 means:'
  options:
  - There is a 3% chance the null hypothesis is true
  - We reject the null hypothesis
  - The effect is large and important
  - We accept the null hypothesis
  answer: 1
  why: Since p (0.03) ≤ α (0.05), we reject the null. The p-value is not the probability the null is true,
    and significance says nothing about effect magnitude.
- q: You want to know if device type (mobile/desktop) is related to whether a user converts (yes/no).
    Which test fits?
  options:
  - Paired t-test
  - Chi-square test of independence
  - One-sample t-test
  - Confidence interval for a mean
  answer: 1
  why: Both variables are categorical and we are testing for a relationship between them, which is exactly
    what a chi-square test of independence does.
- q: In your own words, what is a Type I error?
  answer: Rejecting a null hypothesis that is actually true — a false positive, occurring with probability
    alpha.
  why: A Type I error is concluding there is an effect when none truly exists; its rate is set by the
    significance level α.
- q: Why should you report effect sizes and confidence intervals in addition to p-values?
  answer: Because statistical significance does not imply practical importance; effect sizes and CIs convey
    the magnitude and precision of the effect, not just whether it is non-zero.
  why: A tiny, unimportant effect can be statistically significant with a large sample, so p-values alone
    can mislead about real-world relevance.
resources:
- label: SciPy Statistical Functions Documentation
  url: https://docs.scipy.org/doc/scipy/reference/stats.html
- label: 'StatQuest: Hypothesis Testing and P-values (YouTube)'
  url: https://www.youtube.com/c/joshstarmer
- label: 'Seeing Theory: Visual Introduction to Probability and Statistics'
  url: https://seeing-theory.brown.edu/
- label: Practical Statistics for Data Scientists (O'Reilly)
  url: https://www.oreilly.com/library/view/practical-statistics-for/9781492072935/
---

## From Sample to Population

Inferential statistics lets us draw conclusions about a **population** using a **sample**. Because we rarely measure everyone, we quantify uncertainty rather than claim exact truth. Two pillars support this: **estimation** (confidence intervals) and **hypothesis testing** (t-tests, chi-square, etc.).

Key idea: sample statistics vary from sample to sample. The **sampling distribution** describes that variation, and its spread is the **standard error (SE)**.

## Confidence Intervals

A confidence interval (CI) gives a range of plausible values for a population parameter.

For a mean: `CI = x̄ ± t* × (s / √n)`

- `x̄` = sample mean, `s` = sample standard deviation, `n` = sample size.
- `t*` = critical value from the t-distribution for your confidence level and `df = n - 1`.

**Interpretation:** A 95% CI means that if we repeated the sampling process many times, about 95% of the intervals would contain the true parameter. It does **not** mean there is a 95% probability the true value lies in this one interval.

Wider intervals = more uncertainty. CIs shrink with larger `n` and smaller variability.

## Hypothesis Testing Framework

1. **State hypotheses.** Null `H0` (no effect / no difference) vs. alternative `H1`.
2. **Choose significance level `α`** (commonly 0.05) — your tolerance for a false positive.
3. **Compute a test statistic** and its **p-value**.
4. **Decide:** if `p ≤ α`, reject `H0`; otherwise fail to reject `H0`.

**P-value:** the probability of observing data as extreme or more extreme than what we saw, *assuming H0 is true*. A small p-value means the data are surprising under H0.

**Errors:**
- **Type I (false positive):** rejecting a true H0. Probability = `α`.
- **Type II (false negative):** failing to reject a false H0. Probability = `β`. Power = `1 - β`.

## T-Tests: Comparing Means

Use t-tests when comparing means and the population standard deviation is unknown.

- **One-sample t-test:** is the sample mean different from a known value?
- **Two-sample (independent) t-test:** do two groups have different means? (e.g., A/B test)
- **Paired t-test:** compare two measurements on the same subjects (before/after).

Assumptions: roughly normal data (or large n via CLT), independent observations, and reasonably comparable variances (use Welch's t-test if variances differ).

```python
from scipy import stats
# Two-sample (Welch's) t-test
t, p = stats.ttest_ind(group_a, group_b, equal_var=False)
print(f"t={t:.3f}, p={p:.4f}")
```

## Chi-Square Tests: Categorical Data

- **Goodness-of-fit:** does one categorical variable match an expected distribution?
- **Test of independence:** are two categorical variables related? (built on a contingency table)

The statistic compares observed vs. expected counts: `χ² = Σ (O - E)² / E`.

```python
import pandas as pd
from scipy.stats import chi2_contingency
table = pd.crosstab(df['device'], df['converted'])
chi2, p, dof, expected = chi2_contingency(table)
print(f"chi2={chi2:.3f}, p={p:.4f}")
```

Assumption: expected counts should generally be ≥ 5 in each cell.

## Practical Cautions

- **Statistical significance ≠ practical significance.** Report effect sizes (e.g., Cohen's d) and CIs, not just p-values.
- **Multiple comparisons** inflate false positives — correct with Bonferroni or FDR methods.
- **Avoid p-hacking:** decide tests and sample size before peeking at data.
- Always check assumptions and visualize your data first.
