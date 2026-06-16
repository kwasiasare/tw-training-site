---
title: Relational data modelling
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 7
summary: Design tables, keys and relationships so your data is consistent, non-redundant, and easy to
  query.
objectives:
- Explain what a relational model is in terms of tables, rows and columns
- Choose sensible primary keys and use foreign keys to link tables
- Model one-to-many and many-to-many relationships
- Apply normalisation up to third normal form to remove redundancy
- Sketch a simple entity relationship diagram for a problem
- Write CREATE TABLE statements that enforce keys and constraints
video: m2-l07-data-modelling.mp4
quiz:
- q: What is a primary key?
  options:
  - A column that can repeat freely
  - A column (or set) that uniquely identifies each row
  - A link to another table
  - The first column in a table
  answer: 1
  why: A primary key uniquely identifies each row and cannot be null or duplicated.
- q: What does a foreign key do?
  options:
  - Encrypts a column
  - Speeds up queries automatically
  - Points to a primary key in another table to link them
  - Stores foreign currency values
  answer: 2
  why: A foreign key holds a value that must match a primary key elsewhere, enforcing a valid relationship.
- q: How do you model a many-to-many relationship between students and courses?
  answer: With a junction (join) table holding a foreign key to each side, e.g. enrolments(student_id,
    course_id).
  why: Each enrolment row links one student to one course, so one student can have many courses and vice
    versa.
- q: Which problem does normalisation mainly solve?
  options:
  - Slow networks
  - Data redundancy and update anomalies
  - Weak passwords
  - Large file sizes
  answer: 1
  why: Normalisation splits data so each fact lives in one place, preventing redundancy and inconsistent
    updates.
- q: In an orders and customers design, which table holds the customer_id foreign key for a one-to-many
    relationship?
  answer: The orders (many) table holds customer_id pointing to customers; one customer has many orders.
  why: The foreign key always lives on the many side, referencing the one side's primary key.
- q: What is first normal form (1NF) at a basic level?
  options:
  - Every table has a foreign key
  - Each cell holds a single atomic value, no repeating groups
  - Tables are sorted alphabetically
  - Every column is indexed
  answer: 1
  why: '1NF requires atomic values: no lists or repeating groups stuffed into one cell.'
resources:
- label: PostgreSQL docs — Data Definition (CREATE TABLE, constraints)
  url: https://www.postgresql.org/docs/current/ddl.html
- label: SQLite — official tutorial and SQL reference
  url: https://www.sqlite.org/lang.html
- label: Database Design (Wikibooks) — normalisation chapters
- label: Mode SQL Tutorial — relational concepts
  url: https://mode.com/sql-tutorial/
---

## Why model data?

A **relational database** stores data in **tables** — rows and columns, like a spreadsheet, but with rules. Good *data modelling* is deciding which tables you need, what each column means, and how the tables connect. Get this right and your queries stay simple and your data stays consistent. Get it wrong and you'll fight duplicate, contradictory data forever.

As a maths graduate, think of a table as a **set of tuples** (rows) over a fixed schema (columns) — the relational model is literally built on set theory.

## Keys: primary and foreign

Every table needs a **primary key**: a column (or combination) that uniquely identifies each row and is never null. A **foreign key** is a column that stores the primary key value of *another* table, creating a link.

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    total NUMERIC
);
```

Here `orders.customer_id` is a foreign key into `customers`. The database will reject an order whose `customer_id` doesn't exist.

## Relationships

There are three shapes you'll meet constantly:

- **One-to-one** — rare; often just merge into one table.
- **One-to-many** — one customer has many orders. The foreign key lives on the *many* side (`orders`).
- **Many-to-many** — students take many courses, courses have many students. You need a **junction table**.

```sql
CREATE TABLE enrolments (
    student_id INTEGER REFERENCES students(id),
    course_id  INTEGER REFERENCES courses(id),
    PRIMARY KEY (student_id, course_id)
);
```

Each row of `enrolments` links one student to one course; together they express the many-to-many relationship.

## Normalisation

**Normalisation** is the process of organising tables so each fact is stored in exactly one place. The first three normal forms are enough for almost all work:

- **1NF** — each cell is a single atomic value (no comma-separated lists).
- **2NF** — every non-key column depends on the *whole* primary key.
- **3NF** — non-key columns depend on the key *and nothing but the key* (no column depending on another non-key column).

The payoff is fewer **update anomalies**: change a customer's email in one row, not fifty.

## Entity relationship diagrams

Before writing SQL, sketch an **ER diagram**: boxes for entities (Customer, Order), lines for relationships, and crow's-foot marks for "one" and "many". This is your blueprint — cheap to redraw, expensive to refactor later.

## Your task

Pick a small domain you know — a library, a gym, a music playlist. Identify the **entities**, give each a primary key, decide the relationships, and write the `CREATE TABLE` statements. Make sure every many-to-many uses a junction table.
