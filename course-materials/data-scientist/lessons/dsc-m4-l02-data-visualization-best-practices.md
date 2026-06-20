---
course: data-scientist
title: Data Visualization Best Practices
month: 4
monthTitle: Experimentation, Visualization, and Capstone
lesson: 2
summary: Learn to create clear, honest, and compelling data visualizations using matplotlib and seaborn,
  choosing the right chart for the question while avoiding common pitfalls that mislead viewers.
objectives:
- Select the appropriate chart type for a given data structure and analytical question
- Apply core design principles—clarity, honesty, and minimal clutter—to every chart
- Build effective visualizations using matplotlib and seaborn with proper labels, scales, and color
- Identify and correct common misleading practices like truncated axes and overplotting
- Design accessible visuals using colorblind-safe palettes and clear annotation
video: dsc-m4-l02-data-visualization-best-practices.mp4
quiz:
- q: Why should bar charts generally start their y-axis at zero?
  options:
  - To save space on the page
  - Because seaborn requires it
  - Because a truncated axis exaggerates differences between bars
  - Because zero is always the data minimum
  answer: 2
  why: Truncating the baseline visually inflates small differences between bars, misleading the viewer
    about the magnitude of the comparison.
- q: Which chart type is most appropriate for showing the relationship between two continuous variables?
  options:
  - Pie chart
  - Scatter plot
  - Stacked bar chart
  - Box plot
  answer: 1
  why: A scatter plot maps two continuous variables onto x and y axes, making relationships and correlations
    visible.
- q: What is a good technique for dealing with overplotting in a dense scatter plot?
  options:
  - Add more gridlines
  - Use transparency (alpha), sampling, or a hexbin plot
  - Switch to a pie chart
  - Remove the axis labels
  answer: 1
  why: Transparency, sampling, or density-based plots like hexbin reveal underlying structure that solid
    overlapping points would hide.
- q: Roughly what fraction of men have red-green color vision deficiency, motivating colorblind-safe palettes?
  options:
  - About 8%
  - About 50%
  - Less than 0.1%
  - About 25%
  answer: 0
  why: Around 8% of men have red-green color deficiency, so using colorblind-safe palettes and not relying
    on color alone improves accessibility.
- q: In one sentence, explain the relationship between matplotlib and seaborn.
  answer: Seaborn is a higher-level library built on top of matplotlib that provides attractive statistical
    chart defaults, while matplotlib gives low-level control for fine-tuning.
  why: Seaborn wraps matplotlib to simplify common statistical plots, but you can still access matplotlib
    objects to customize details.
- q: Name one thing a chart title should do beyond labeling the variables.
  answer: State the key insight or takeaway from the chart.
  why: An effective title communicates the message (e.g., 'Average bill is highest on weekends') rather
    than a generic description, guiding the viewer to the conclusion.
resources:
- label: seaborn official tutorial
  url: https://seaborn.pydata.org/tutorial.html
- label: matplotlib Pyplot tutorial
  url: https://matplotlib.org/stable/tutorials/pyplot.html
- label: Fundamentals of Data Visualization (Claus Wilke, free online)
  url: https://clauswilke.com/dataviz/
- label: Choosing color palettes in seaborn
  url: https://seaborn.pydata.org/tutorial/color_palettes.html
---

## Why Visualization Matters

A chart is an argument made visible. As a data scientist, your analysis is only as valuable as your ability to communicate it. A good visualization reveals patterns instantly; a bad one hides them or—worse—misleads stakeholders into wrong decisions.

The goal is always **clarity and honesty**. Every design choice should help the viewer understand the data faithfully, not impress them with decoration.

## Choosing the Right Chart

Match the chart to the question and data type:

- **Comparison across categories** → bar chart
- **Trend over time** → line chart
- **Distribution of one variable** → histogram, KDE, box plot
- **Relationship between two variables** → scatter plot
- **Part-to-whole** → stacked bar (avoid pie charts for more than 2-3 slices)
- **Correlation matrix** → heatmap

Ask: *What single message should the viewer take away?* Then pick the form that delivers it most directly.

## Core Design Principles

1. **Maximize the data-ink ratio** (Tufte): remove gridlines, borders, and 3D effects that carry no information.
2. **Label everything**: title, axis labels with units, and a legend when needed.
3. **Start bar charts at zero**: truncated y-axes exaggerate differences. Line charts can use non-zero baselines when showing relative change, but disclose it.
4. **Order intentionally**: sort categorical bars by value, not alphabetically, unless order is meaningful.
5. **Use color purposefully**: color should encode data or highlight, not decorate.

## matplotlib vs seaborn

- **matplotlib** is the low-level foundation—full control over every element.
- **seaborn** is built on matplotlib and provides attractive statistical defaults with less code.

A common workflow: use seaborn to draw the chart quickly, then drop to matplotlib to fine-tune labels, limits, and annotations.

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(7,4))
sns.barplot(data=tips, x="day", y="total_bill", ax=ax, errorbar="sd")
ax.set_ylabel("Average total bill ($)")
ax.set_xlabel("Day of week")
ax.set_title("Average bill is highest on weekends")
plt.tight_layout()
```

Notice the title states the *insight*, not just "Bill by Day".

## Avoiding Misleading Charts

- **Truncated axes**: starting a bar chart's y-axis above zero inflates small differences.
- **Dual y-axes**: easily imply false correlation; use with caution.
- **Overplotting**: dense scatter plots hide structure—use transparency (`alpha`), sampling, or hexbin/2D density.
- **Misleading aggregation**: a single average can hide bimodal distributions; show the spread.
- **Wrong scale**: skewed data may need a log scale—label it clearly.

## Color and Accessibility

- Use **colorblind-safe palettes** (`sns.color_palette("colorblind")`); ~8% of men have red-green color deficiency.
- Sequential palettes for ordered/continuous data, diverging for data with a meaningful midpoint, qualitative for categories.
- Don't rely on color alone—add labels, patterns, or direct annotation.
- Ensure sufficient contrast and readable font sizes for the final medium.

## A Practical Checklist

Before sharing any chart, ask:
1. Does the title state the takeaway?
2. Are axes labeled with units?
3. Is the baseline honest (zero for bars)?
4. Is the chart type right for the question?
5. Is it readable in grayscale / for colorblind viewers?
6. Have I removed all non-informative clutter?
