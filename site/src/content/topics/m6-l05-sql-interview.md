---
title: SQL interview practice
month: 6
monthTitle: Apply & Interview
lesson: 5
summary: Practise the SQL patterns interviewers love — joins, aggregation, grouping, and window functions
  — and explain your query out loud.
objectives:
- Read a question, identify the tables, and plan the query before typing
- Choose the right join (INNER vs LEFT) for the question asked
- Aggregate with GROUP BY and filter groups using HAVING
- Solve top-N-per-group problems with window functions
- Know the logical order SQL actually runs clauses in
- Explain your query out loud the way an interviewer expects
video: m6-l05-sql-interview.mp4
quiz:
- q: Which join keeps every row from the left table even when there is no match on the right?
  options:
  - INNER JOIN
  - LEFT JOIN
  - CROSS JOIN
  - FULL JOIN
  answer: 1
  why: LEFT JOIN returns all left-table rows; columns from the right table are NULL where no match exists.
- q: WHERE filters individual rows. Which clause filters groups after aggregation?
  options:
  - GROUP BY
  - ORDER BY
  - HAVING
  - DISTINCT
  answer: 2
  why: HAVING runs after GROUP BY, so it can filter on aggregates like COUNT(*) > 5; WHERE cannot.
- q: 'In what order does SQL logically evaluate these clauses: SELECT, FROM, WHERE, GROUP BY?'
  answer: FROM, then WHERE, then GROUP BY, then SELECT (SELECT runs near the end).
  why: Because SELECT runs late, column aliases defined there are not visible to WHERE or GROUP BY in
    most engines.
- q: You need the 2nd highest salary per department. Which tool fits best?
  options:
  - A simple GROUP BY
  - A window function like RANK() OVER (PARTITION BY ...)
  - DISTINCT
  - ORDER BY alone
  answer: 1
  why: Window functions rank rows within each partition without collapsing them, which is exactly what
    top-N-per-group needs.
- q: Why can COUNT(column) return a smaller number than COUNT(*) on the same table?
  answer: COUNT(*) counts all rows; COUNT(column) ignores rows where that column is NULL.
  why: Knowing NULL handling shows the interviewer you think about data quality, not just syntax.
- q: True or false — an INNER JOIN can return fewer rows than either input table.
  options:
  - 'True'
  - 'False'
  answer: 0
  why: True. Unmatched rows from both sides are dropped, so the result can be smaller than both inputs.
resources:
- label: Mode SQL Tutorial (free, interactive, beginner to advanced)
  url: https://mode.com/sql-tutorial/
- label: PostgreSQL Tutorial — Window Functions
  url: https://www.postgresqltutorial.com/postgresql-window-function/
- label: LeetCode — Database problem set (interview practice)
  url: https://leetcode.com/problemset/database/
- label: SQLZoo — practice exercises with a live database
  url: https://sqlzoo.net/
---

## Why SQL still wins interviews

Almost every data and A I role touches data that lives in a relational database, so **SQL** comes up in interviews far more than people expect. The good news: the question patterns repeat. Master a handful of them and you can solve most live screens calmly.

This lesson is about *practice*, not memorising syntax. The skill interviewers grade is: can you read a vague question, picture the tables, and turn it into a correct query while talking through your reasoning?

## Start by reading the data, not writing code

Before you type, identify the **tables**, their **keys**, and which one is the "main" table the answer is about. Restate the question in plain English: *for each customer, count their orders*. That sentence already tells you the join and the GROUP BY.

```sql
-- For each customer, how many orders have they placed?
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
ORDER BY order_count DESC;
```

Notice the **LEFT JOIN**: a customer with zero orders still appears, with a count of 0. An INNER JOIN would silently hide them — a classic interview trap.

## Joins, GROUP BY, and HAVING

- **INNER JOIN** keeps only matching rows from both sides.
- **LEFT JOIN** keeps every left row, filling NULLs where the right has no match.
- **GROUP BY** collapses rows into groups so you can aggregate (COUNT, SUM, AVG).
- **HAVING** filters those groups *after* aggregation; **WHERE** filters rows *before*.

```sql
-- Customers who have spent more than 1000 in total
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING SUM(o.amount) > 1000;
```

## The logical order of execution

SQL does not run top to bottom. The logical order is roughly: **FROM** -> **WHERE** -> **GROUP BY** -> **HAVING** -> **SELECT** -> **ORDER BY** -> **LIMIT**. Because SELECT runs late, an alias you create there usually cannot be used in WHERE. Saying this in an interview signals real understanding.

## Window functions for top-N-per-group

When a question says "per group" and "top N" or "second highest", reach for a **window function**. Unlike GROUP BY, it ranks rows *without* collapsing them.

```sql
-- Top earner per department
SELECT name, department, salary
FROM (
  SELECT name, department, salary,
         RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
  FROM employees
) ranked
WHERE rnk = 1;
```

## Practice plan before your screen

Do a few easy and medium database problems on LeetCode or SQLZoo each day. **Speak your plan out loud** before typing, watch for NULLs, and always sanity-check row counts. Calm, narrated reasoning beats a silently typed perfect query.
