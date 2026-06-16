---
course: dami-ai-career
title: Intro to SQL with SQLite
month: 1
monthTitle: Python Foundations + Git
lesson: 13
summary: Store data in tables and ask questions of it using SQL, all with SQLite — a database that needs
  no server.
objectives:
- Explain what a relational database and a table are
- Create a SQLite database file and a table with typed columns
- Insert rows and read them back with SELECT
- Filter, sort, and limit results with WHERE, ORDER BY, and LIMIT
- Summarise data with COUNT, AVG, and GROUP BY
- Run SQL from the sqlite3 shell and from Python's sqlite3 module
video: m1-l13-sql-sqlite.mp4
quiz:
- q: What does SQL stand for?
  options:
  - Simple Query Language
  - Structured Query Language
  - Sequential Query Logic
  - System Quality Layer
  answer: 1
  why: SQL is Structured Query Language — the standard language for talking to relational databases.
- q: Why is SQLite called 'serverless'?
  answer: The whole database is a single file on disk, read and written directly by your program — there
    is no separate database server process to install or run.
  why: Unlike Postgres or MySQL, SQLite needs no server; the library reads and writes one .db file directly.
- q: Which clause filters which rows a SELECT returns?
  options:
  - ORDER BY
  - GROUP BY
  - WHERE
  - LIMIT
  answer: 2
  why: WHERE keeps only the rows whose condition is true; ORDER BY sorts, GROUP BY aggregates, LIMIT caps
    the count.
- q: What does SELECT * FROM students; return?
  options:
  - Only the first row
  - Every column of every row in students
  - The number of rows
  - An error
  answer: 1
  why: The asterisk means all columns, and with no WHERE clause it returns all rows in the table.
- q: Which SQL keyword adds new rows to a table?
  answer: INSERT (INSERT INTO ... VALUES ...)
  why: INSERT INTO table (columns) VALUES (...) adds rows; SELECT reads, UPDATE changes, DELETE removes.
- q: What does GROUP BY do in a query?
  answer: It collapses rows that share a value into groups so aggregate functions like COUNT or AVG are
    computed per group.
  why: GROUP BY course with AVG(score) gives one average score for each course rather than one over all
    rows.
resources:
- label: SQLite — official documentation
  url: https://www.sqlite.org/docs.html
- label: Python docs — sqlite3 module
  url: https://docs.python.org/3/library/sqlite3.html
- label: SQLBolt — interactive SQL lessons
  url: https://sqlbolt.com/
- label: Mode — SQL Tutorial
  url: https://mode.com/sql-tutorial/
---

## What is a database?

A **relational database** stores data in **tables**: rows and columns, like a spreadsheet but with strict rules. Each column has a name and a **type** (text, integer, real). Each row is one record.

**SQL** — Structured Query Language — is how we talk to that data: create tables, add rows, and ask questions. It is declarative: you say *what* you want, not *how* to fetch it.

## Why SQLite?

**SQLite** is a tiny database where the entire database is a single file on disk. There is no server to install or start — your program opens the file directly. It already ships with Python, so you have it right now.

It is perfect for learning, small apps, and analysis. The same SQL you learn here works in Postgres and MySQL later.

## Creating a table and adding rows

You define columns and their types with `CREATE TABLE`, then add rows with `INSERT`.

```sql
CREATE TABLE students (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    course  TEXT,
    score   REAL
);

INSERT INTO students (name, course, score)
VALUES ('Dami', 'Maths', 91.5),
       ('Ada',  'Stats', 88.0);
```

## Asking questions with SELECT

`SELECT` reads data. `WHERE` filters rows, `ORDER BY` sorts them, and `LIMIT` caps how many come back.

```sql
SELECT name, score FROM students
WHERE score > 80
ORDER BY score DESC
LIMIT 5;
```

## Summarising with aggregates

Aggregate functions collapse many rows into one number. With `GROUP BY` you get one result *per group*.

```sql
SELECT course, COUNT(*) AS n, AVG(score) AS avg_score
FROM students
GROUP BY course;
```

## Running SQL from Python

Python's built-in `sqlite3` module lets you run the same SQL from code and pull results back as Python tuples.

```python
import sqlite3

conn = sqlite3.connect('school.db')
cur = conn.cursor()
cur.execute('SELECT name, score FROM students WHERE score > ?', (80,))
print(cur.fetchall())
conn.commit()
conn.close()
```

## Your task

Create `school.db`, add a `students` table with five rows, then write one query that returns the average score per course.
