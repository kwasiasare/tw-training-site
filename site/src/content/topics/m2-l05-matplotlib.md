---
title: Data visualisation with matplotlib
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 5
summary: Turn numbers into clear charts with matplotlib — line, scatter, bar and histogram plots you can
  label, style and save.
objectives:
- Create a figure and axes with plt.subplots and understand the object model
- Draw line, scatter, bar and histogram plots from lists or arrays
- Label axes, add a title and a legend so a chart explains itself
- Plot pandas Series and DataFrame columns directly
- Control style, colour, markers and figure size
- Save a chart to a file with savefig for reports and notebooks
video: m2-l05-matplotlib.mp4
quiz:
- q: Which call creates a figure and a single axes you can draw on?
  options:
  - plt.draw()
  - plt.subplots()
  - plt.canvas()
  - plt.axis()
  answer: 1
  why: fig, ax = plt.subplots() returns a Figure and an Axes; you call methods like ax.plot on the axes.
- q: Which plot type best shows the distribution of a single numeric column?
  options:
  - Line plot
  - Scatter plot
  - Histogram
  - Pie chart
  answer: 2
  why: A histogram buckets values into bins and shows how frequently each range occurs — ideal for one
    variable's distribution.
- q: What is the standard import alias for matplotlib's plotting interface?
  options:
  - import matplotlib as mpl
  - import matplotlib.pyplot as plt
  - import pyplot as plt
  - from matplotlib import plot as plt
  answer: 1
  why: import matplotlib.pyplot as plt is the universal convention; plt gives you the plotting functions.
- q: Which method shows a label that explains each line in the chart, using the label= text you passed
    to plot?
  answer: ax.legend()
  why: After giving each plot a label=, calling ax.legend() draws the key (legend) that maps colours to
    labels.
- q: Which method writes the current chart to a PNG file?
  answer: fig.savefig (or plt.savefig)
  why: fig.savefig("chart.png") saves the figure to disk; do it before plt.show() in scripts so the figure
    still exists.
- q: Why is the 'object-oriented' style (fig, ax) preferred over the pyplot state machine?
  answer: It is explicit about which axes you are drawing on, so it scales to multiple subplots and is
    easier to read.
  why: The state-machine style (plt.plot, plt.title) hides which axes is 'current'; fig, ax makes every
    call unambiguous.
resources:
- label: Matplotlib — Pyplot tutorial (official)
  url: https://matplotlib.org/stable/tutorials/pyplot.html
- label: Matplotlib — Quick start guide
  url: https://matplotlib.org/stable/users/explain/quick_start.html
- label: Real Python — Python Plotting With Matplotlib
  url: https://realpython.com/python-matplotlib-guide/
- label: 'Python Data Science Handbook (Jake VanderPlas) — Chapter 4: Visualization with Matplotlib'
---

## Why visualise data?

Numbers in a table hide their shape. A **chart** lets you see a trend, an outlier, or a distribution in a single glance. As a maths graduate you already think in functions and distributions — matplotlib lets you *draw* them.

**matplotlib** is the foundational plotting library in Python. pandas, seaborn and many others build on top of it, so learning it pays off everywhere.

## The figure and axes model

Every chart lives on a **Figure** (the whole canvas) which holds one or more **Axes** (a single plot with its x and y). The clean, modern way is to create both at once, then call methods on the axes.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax.set_xlabel("x")
ax.set_ylabel("x squared")
ax.set_title("A simple line")
plt.show()
```

Prefer this `fig, ax` style over bare `plt.plot(...)`. It is explicit about *which* plot you are drawing on, which matters the moment you have more than one.

## The common plot types

Four plots cover most early needs:

- `ax.plot(x, y)` — a **line**, good for trends over time.
- `ax.scatter(x, y)` — **points**, good for relationships between two variables.
- `ax.bar(labels, values)` — **bars**, good for comparing categories.
- `ax.hist(values, bins=20)` — a **histogram**, good for one variable's distribution.

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar"]
sales = [120, 150, 130]

fig, ax = plt.subplots()
ax.bar(months, sales, color="steelblue")
ax.set_title("Sales by month")
ax.set_ylabel("Units")
plt.show()
```

## Labelling and legends

An unlabelled chart is a puzzle. Always add axis labels and a title. When you draw several series, give each a `label=` and call `ax.legend()` to show the key.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 2, 3], label="linear")
ax.plot([1, 2, 3], [1, 4, 9], label="quadratic")
ax.legend()
plt.show()
```

## Plotting with pandas

In practice your data lives in a **DataFrame**. pandas wraps matplotlib, so `df.plot()` works, but you can also pass columns straight to an axes for full control.

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({"day": [1, 2, 3], "temp": [14, 16, 15]})
fig, ax = plt.subplots()
ax.plot(df["day"], df["temp"], marker="o")
ax.set_xlabel("Day")
ax.set_ylabel("Temp (C)")
plt.show()
```

## Saving your work

In a notebook a chart just appears. In a script, call `fig.savefig` to write a file — do this **before** `plt.show()` so the figure still exists.

```python
fig.savefig("temperature.png", dpi=150, bbox_inches="tight")
```

## Your task

Load a small CSV with pandas and make **two** charts from it — one line or scatter, one bar or histogram — fully labelled, and save each as a PNG.
