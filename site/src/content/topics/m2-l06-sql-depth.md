---
title: 'SQL in depth: joins, GROUP BY, subqueries'
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 6
summary: Combine tables with joins, summarise rows with GROUP BY, and answer harder questions using nested
  subqueries.
objectives:
- Combine rows from two tables with INNER JOIN using a key
- Keep unmatched rows with LEFT JOIN and spot the NULLs
- Summarise rows into groups with GROUP BY and aggregate functions
- Filter groups with HAVING and understand how it differs from WHERE
- Answer harder questions by nesting a subquery inside a query
- Read a query in the order the database actually runs it
video: m2-l06-sql-depth.mp4
quiz:
- q: Which join keeps every row from the left table even when there is no match on the right?
  options:
  - INNER JOIN
  - LEFT JOIN
  - CROSS JOIN
  - FULL JOIN
  answer: 1
  why: LEFT JOIN returns all left-table rows; unmatched right-side columns come back as NULL.
- q: You want to filter on the result of COUNT(*) per group. Which clause do you use?
  options:
  - WHERE
  - GROUP BY
  - HAVING
  - ORDER BY
  answer: 2
  why: WHERE filters individual rows before grouping; HAVING filters whole groups after aggregation.
- q: What does GROUP BY do?
  options:
  - Sorts rows alphabetically
  - Removes duplicate rows
  - Collapses rows that share a value into one row per group
  - Joins two tables
  answer: 2
  why: GROUP BY buckets rows by the column(s) you name, so aggregates like SUM and COUNT run per bucket.
- q: In SQL, what is a subquery?
  answer: A query nested inside another query, whose result feeds the outer query.
  why: Subqueries can sit in WHERE, FROM, or SELECT and let you compute a value to compare or join against.
- q: Write the aggregate function that counts the number of rows in each group.
  answer: COUNT(*)
  why: COUNT(*) counts all rows per group; COUNT(column) counts only non-NULL values in that column.
- q: WHERE and HAVING run at different times. Which runs first?
  options:
  - HAVING runs first
  - WHERE runs first
  - They run at the same time
  - It depends on ORDER BY
  answer: 1
  why: WHERE filters rows before grouping; only then does GROUP BY form groups and HAVING filter them.
resources:
- label: SQLBolt — interactive SQL lessons (joins, aggregates, subqueries)
  url: https://sqlbolt.com/
- label: Mode SQL Tutorial — Joins and Aggregate Functions
  url: https://mode.com/sql-tutorial/
- label: PostgreSQL docs — Joined Tables and GROUP BY
  url: https://www.postgresql.org/docs/current/queries-table-expressions.html
- label: SQLite docs — Query Language (SELECT)
  url: https://www.sqlite.org/lang_select.html
---

## Why go deeper than SELECT?

A single table rarely holds the whole story. Customers live in one table, their orders in another. To answer real questions — *how much did each customer spend?* — you must **combine** tables and **summarise** rows. That is what joins, GROUP BY, and subqueries give you.

As a maths graduate, think of a table as a relation: a set of tuples. A **join** is like an intersection over a shared key, and **GROUP BY** is partitioning a set into equivalence classes, then applying a function to each class.

## Joins: combining tables on a key

A join matches rows from two tables using a shared column, usually an id. An **INNER JOIN** keeps only rows that match in both tables. A **LEFT JOIN** keeps every row from the left table and fills missing right-side values with `NULL`.

```sql
-- Every order with its customer's name
SELECT o.id, c.name, o.amount
FROM orders AS o
INNER JOIN customers AS c
  ON o.customer_id = c.id;

-- Customers WITH or WITHOUT orders
SELECT c.name, o.id
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.id;
```

Use table **aliases** (`o`, `c`) to keep queries short, and always say which table a column comes from when names could clash.

## GROUP BY and aggregates

**GROUP BY** collapses rows that share a value into one row per group. You then apply an **aggregate function** — `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` — to each group.

```sql
-- Total and average spend per customer
SELECT customer_id,
       COUNT(*)    AS num_orders,
       SUM(amount) AS total_spent,
       AVG(amount) AS avg_order
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 100
ORDER BY total_spent DESC;
```

Every column in `SELECT` must either be inside an aggregate or listed in `GROUP BY`.

## WHERE vs HAVING

This trips up everyone. **WHERE** filters individual rows *before* grouping. **HAVING** filters whole groups *after* aggregation. If you need `COUNT(*) > 3`, that condition belongs in `HAVING`, because the count does not exist until groups are formed.

## Subqueries: a query inside a query

A **subquery** is a SELECT nested inside another statement. Its result feeds the outer query. Use one to compare against a computed value, or to build a temporary table to join against.

```sql
-- Customers who spent more than the average customer
SELECT name
FROM customers
WHERE id IN (
  SELECT customer_id
  FROM orders
  GROUP BY customer_id
  HAVING SUM(amount) > (SELECT AVG(amount) FROM orders)
);
```

## How SQL actually runs

SQL is not read top to bottom. The engine runs roughly: `FROM` and joins, then `WHERE`, then `GROUP BY`, then `HAVING`, then `SELECT`, then `ORDER BY`, then `LIMIT`. Knowing this order explains why you cannot use a `SELECT` alias in `WHERE`, but can in `ORDER BY`.

## Your task

Take a two-table dataset (orders and customers, or any pair you have). Write one query with a `LEFT JOIN`, one with `GROUP BY` plus `HAVING`, and one that uses a subquery. Explain in a sentence what each answers.
