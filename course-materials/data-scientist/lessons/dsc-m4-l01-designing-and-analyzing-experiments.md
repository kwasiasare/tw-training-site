---
course: data-scientist
title: Designing and Analyzing Experiments
month: 4
monthTitle: Experimentation, Visualization, and Capstone
lesson: 1
summary: 'Learn to design rigorous A/B experiments end-to-end: forming hypotheses, choosing primary metrics,
  computing required sample size and power, running tests cleanly, and analyzing results to drive trustworthy
  product decisions.'
objectives:
- Formulate a testable hypothesis and select primary, secondary, and guardrail metrics for an experiment
- Calculate the required sample size given baseline rate, minimum detectable effect, significance level,
  and power
- Run an A/B test correctly while avoiding peeking, sample ratio mismatch, and other common pitfalls
- Analyze experiment results using appropriate statistical tests and interpret p-values, confidence intervals,
  and effect sizes
- Translate statistical findings into clear, actionable business recommendations
video: dsc-m4-l01-designing-and-analyzing-experiments.mp4
quiz:
- q: Why is random assignment central to A/B testing?
  options:
  - It guarantees equal group sizes
  - It balances confounding variables so differences can be attributed to the treatment
  - It eliminates the need for a sample size calculation
  - It makes the test one-sided
  answer: 1
  why: Random assignment distributes confounders evenly across groups in expectation, which is what enables
    a causal interpretation of any observed difference.
- q: If you halve the minimum detectable effect (MDE) you want to detect, roughly what happens to the
    required sample size?
  options:
  - It halves
  - It stays the same
  - It doubles
  - It quadruples
  answer: 3
  why: Sample size scales with 1/MDE^2, so halving the MDE multiplies the required sample size by about
    four.
- q: Which practice inflates the false positive (Type I error) rate?
  options:
  - Running the test for a full week
  - Repeatedly checking results and stopping as soon as p < 0.05
  - Randomizing at the user level
  - Reporting a confidence interval
  answer: 1
  why: Optional stopping (peeking) gives many chances to cross the significance threshold by chance, inflating
    the false positive rate beyond the nominal alpha.
- q: What does a 95% confidence interval for the treatment effect that excludes 0 tell you?
  options:
  - The result is not significant
  - The effect is practically important
  - The result is statistically significant at alpha = 0.05
  - The sample size was too small
  answer: 2
  why: A 95% CI excluding zero corresponds to rejecting the null at the 0.05 level — statistical significance,
    though not necessarily practical significance.
- q: In one sentence, what is the difference between a primary (OEC) metric and a guardrail metric?
  answer: The primary/OEC metric is the single outcome the decision is based on, while guardrail metrics
    are metrics that must not be harmed by the change.
  why: The OEC drives the ship decision; guardrails ensure the change doesn't degrade critical health
    metrics like latency or churn.
- q: Name one statistical test appropriate for comparing conversion rates between two groups.
  answer: Two-proportion z-test (or chi-square test).
  why: Conversion rate is a proportion, so a two-proportion z-test or a chi-square test of independence
    is appropriate.
resources:
- label: Trustworthy Online Controlled Experiments (Kohavi, Tang, Xu)
  url: https://experimentguide.com/
- label: 'statsmodels: Statistics for power and proportions'
  url: https://www.statsmodels.org/stable/stats.html
- label: Evan Miller's Sample Size and A/B Test Calculators
  url: https://www.evanmiller.org/ab-testing/
- label: Udacity / Google A/B Testing course notes
  url: https://www.udacity.com/course/ab-testing--ud257
---

## Why Experiments Matter

Observational data tells you what *correlates*; controlled experiments tell you what *causes*. A/B testing (randomized controlled trials in a product context) is the gold standard for measuring the causal impact of a change because random assignment balances confounders across groups.

As a data scientist you will be asked: *"Did this new feature actually move the needle?"* A well-designed experiment answers that with quantified confidence.

## The Experiment Lifecycle

1. **Hypothesis** — a specific, falsifiable statement.
2. **Metrics** — what you measure.
3. **Design** — randomization unit, sample size, duration.
4. **Run** — collect data, monitor health.
5. **Analyze** — apply statistical tests.
6. **Decide** — ship, iterate, or abandon.

## 1. Hypotheses

State a clear hypothesis: *"Changing the checkout button from gray to green will increase the purchase conversion rate."*

- **Null hypothesis (H0):** there is no difference between control and treatment.
- **Alternative hypothesis (H1):** there is a difference (two-sided) or a directional difference (one-sided).

Most teams use **two-sided** tests because they protect against the change being harmful.

## 2. Choosing Metrics

- **Primary metric (OEC):** the single metric the decision hinges on, e.g., conversion rate. Pick *one*.
- **Secondary metrics:** supporting evidence, e.g., revenue per user.
- **Guardrail metrics:** must-not-harm metrics, e.g., page load time, churn, refund rate.

Good metrics are **sensitive** (move when the feature works) and **aligned** with long-term business value. Beware vanity metrics.

## 3. Sample Size and Power

Four quantities are linked; fix three and solve for the fourth:

- **Significance level (alpha):** false positive rate, typically 0.05.
- **Power (1 - beta):** chance of detecting a true effect, typically 0.80.
- **Minimum Detectable Effect (MDE):** the smallest effect worth detecting.
- **Sample size (n).**

For a comparison of two proportions, a useful approximation for n *per group* is:

```
n = 16 * p * (1 - p) / (MDE)^2
```

where `p` is the baseline rate and `MDE` is the absolute difference you want to detect. The constant 16 bundles alpha=0.05 and power=0.80.

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

baseline = 0.10        # current conversion rate
mde_abs  = 0.02        # detect a 2 percentage-point lift
effect = proportion_effectsize(baseline + mde_abs, baseline)

analysis = NormalIndPower()
n = analysis.solve_power(effect_size=effect, alpha=0.05,
                         power=0.80, alternative='two-sided')
print(f"Need ~{n:.0f} users per group")
```

Smaller MDEs require dramatically larger samples (n scales with 1/MDE^2). Decide MDE based on business value, not statistical convenience.

## 4. Running the Test

- **Randomization unit:** usually the user, not the session, to avoid contamination and correlated observations.
- **Run for full business cycles** (often at least one week) to capture weekday/weekend effects.
- **Don't peek:** repeatedly checking and stopping when significant inflates false positives. Fix duration in advance or use sequential/Bayesian methods designed for continuous monitoring.
- **Check Sample Ratio Mismatch (SRM):** if you expected 50/50 but got 48/52, a chi-square test on counts may reveal a broken assignment system — invalidating the experiment.

## 5. Analyzing Results

Match the test to the metric type:

- **Proportions** (conversion): two-proportion z-test or chi-square test.
- **Continuous means** (revenue, time): two-sample t-test (Welch's by default).

```python
from statsmodels.stats.proportion import proportions_ztest

conversions = [1200, 1320]   # control, treatment successes
samples     = [10000, 10000] # users per group
stat, pval = proportions_ztest(conversions, samples)
print(f"z={stat:.3f}, p={pval:.4f}")
```

Report more than a p-value:

- **Effect size:** the lift (e.g., +1.2 pp, a 10% relative increase).
- **Confidence interval:** the plausible range for the true effect. If the 95% CI excludes 0, the result is significant at alpha=0.05.
- **Practical significance:** is the effect big enough to matter, given cost?

## Common Pitfalls

- **Peeking / optional stopping** inflates Type I error.
- **Multiple comparisons:** testing many metrics increases false positives — correct with Bonferroni or control false discovery rate.
- **Simpson's paradox:** aggregated results can reverse within segments; segment carefully.
- **Novelty / primacy effects:** users react to *change* itself; run long enough.
- **Confusing statistical with practical significance.**

## 6. Making the Decision

Combine the primary metric result, guardrails, and business cost. A statistically significant but tiny lift may not justify engineering and maintenance cost. Document the decision and the evidence so the org can learn.
