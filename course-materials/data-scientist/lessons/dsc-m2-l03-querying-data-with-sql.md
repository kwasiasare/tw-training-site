---
course: data-scientist
title: Querying Data with SQL
month: 2
monthTitle: Statistics and SQL for Analysis
lesson: 3
summary: Learn to extract and analyze data from relational databases using SQL. This lesson covers filtering
  and aggregations, the major join types, subqueries and CTEs, and window functions for advanced analytics
  tasks data scientists face daily.
objectives:
- Write SELECT queries that filter, group, and aggregate data to answer analytical questions
- Combine tables correctly using INNER, LEFT, RIGHT, and FULL joins
- Use subqueries and common table expressions (CTEs) to structure complex logic
- Apply window functions for running totals, rankings, and period-over-period comparisons
- Understand SQL logical execution order to debug queries and avoid common mistakes
video: dsc-m2-l03-querying-data-with-sql.mp4
quiz:
- q: Which clause filters rows AFTER aggregation has occurred?
  options:
  - WHERE
  - HAVING
  - GROUP BY
  - ORDER BY
  answer: 1
  why: WHERE filters rows before grouping, while HAVING filters the aggregated results after GROUP BY
    runs.
- q: You want to keep all customers even those with no orders. Which join should you use (customers on
    the left)?
  options:
  - INNER JOIN
  - LEFT JOIN
  - CROSS JOIN
  - Self join
  answer: 1
  why: A LEFT JOIN returns all rows from the left table (customers) and fills NULLs where there is no
    matching order.
- q: What distinguishes a window function from a GROUP BY aggregation?
  options:
  - Window functions are faster always
  - Window functions collapse rows into one
  - Window functions compute across rows without collapsing them
  - Window functions cannot use ORDER BY
  answer: 2
  why: Window functions perform calculations over a set of related rows while preserving each individual
    row, unlike GROUP BY which collapses rows into summaries.
- q: In SQL's logical execution order, which clause is evaluated first?
  options:
  - SELECT
  - FROM
  - WHERE
  - ORDER BY
  answer: 1
  why: SQL logically begins with FROM to identify the source data, then applies WHERE, GROUP BY, HAVING,
    SELECT, and finally ORDER BY.
- q: Name the keyword used to define a Common Table Expression (CTE).
  answer: WITH
  why: CTEs are introduced with the WITH keyword, which names a reusable, readable result set used in
    the main query.
- q: Which window function would you use to compare each row's value to the previous row within a partition?
  answer: LAG
  why: LAG accesses a value from a prior row in the ordered window, ideal for period-over-period comparisons.
    LEAD does the same for the next row.
resources:
- label: Mode SQL Tutorial (Intermediate & Advanced)
  url: https://mode.com/sql-tutorial/
- label: PostgreSQL Window Functions Documentation
  url: https://www.postgresql.org/docs/current/tutorial-window.html
- label: SQLBolt Interactive SQL Lessons
  url: https://sqlbolt.com/
- label: Select Star SQL (free interactive book)
  url: https://selectstarsql.com/
---

## Why SQL for Data Scientists

Most real-world data lives in relational databases. Before you can model or visualize anything in Python, you need to pull the right data. SQL (Structured Query Language) is the universal tool for querying relational data, and fluency in it separates productive data scientists from those who wait on engineering teams.

## The Core Query Structure

A basic query follows a familiar pattern:

```sql
SELECT column_a, column_b
FROM table_name
WHERE condition
GROUP BY column_a
HAVING aggregate_condition
ORDER BY column_b
LIMIT 100;
```

**Logical execution order** differs from the written order. SQL evaluates clauses roughly as: `FROM` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `ORDER BY` -> `LIMIT`. This is why you cannot reference a `SELECT` alias inside a `WHERE` clause, but you can in `ORDER BY`.

## Aggregations

Aggregate functions collapse many rows into a summary value: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. Pair them with `GROUP BY` to compute per-group summaries.

```sql
SELECT category, COUNT(*) AS num_orders, AVG(amount) AS avg_amount
FROM orders
GROUP BY category
HAVING COUNT(*) > 10;
```

Use `WHERE` to filter rows *before* aggregation and `HAVING` to filter *after* aggregation.

## Joins

Joins combine rows from multiple tables based on a related key.

- **INNER JOIN**: only rows with matches in both tables.
- **LEFT JOIN**: all rows from the left table, NULLs where no match on the right.
- **RIGHT JOIN**: all rows from the right table.
- **FULL OUTER JOIN**: all rows from both, matched where possible.

```sql
SELECT c.customer_name, o.order_id, o.amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

A LEFT JOIN is your friend when you want to keep all customers even those without orders (great for spotting churn or gaps).

## Subqueries and CTEs

A **subquery** is a query nested inside another. A **CTE** (Common Table Expression) using `WITH` makes complex logic readable and reusable.

```sql
WITH high_value AS (
    SELECT customer_id, SUM(amount) AS total
    FROM orders
    GROUP BY customer_id
    HAVING SUM(amount) > 1000
)
SELECT c.customer_name, h.total
FROM high_value h
JOIN customers c ON c.customer_id = h.customer_id;
```

Prefer CTEs over deeply nested subqueries for readability and easier debugging.

## Window Functions

Window functions perform calculations across a set of rows related to the current row **without collapsing them** like `GROUP BY` does. The `OVER()` clause defines the window.

```sql
SELECT
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_seq,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount
FROM orders;
```

Common window functions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, and aggregate functions with `OVER`. `PARTITION BY` resets the window per group; `ORDER BY` inside `OVER` defines ordering for running/ranking calculations.

## Practical Tips

- Always inspect a sample with `LIMIT` before running heavy aggregations.
- Be explicit with table aliases when joining.
- Watch for fan-out: joining one-to-many can inflate aggregate counts.
- NULLs do not match in joins or equality; handle them deliberately.
