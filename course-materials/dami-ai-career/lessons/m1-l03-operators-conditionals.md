---
course: dami-ai-career
title: Operators & conditionals
month: 1
monthTitle: Python Foundations + Git
lesson: 3
summary: Combine values with arithmetic, comparison and logical operators, then let your code make decisions
  with if, elif and else.
objectives:
- Use arithmetic operators including floor division, modulo and exponent
- Compare values with ==, !=, <, >, <= and >=
- Combine conditions with the logical operators and, or and not
- Write decision logic using if, elif and else
- Understand truthy and falsy values in Python
- Avoid the classic mistake of using = instead of ==
- Read and reason about nested and chained conditions
video: m1-l03-operators-conditionals.mp4
quiz:
- q: What does the expression 17 % 5 evaluate to?
  options:
  - '3'
  - '3.4'
  - '2'
  - '12'
  answer: 2
  why: The modulo operator % gives the remainder of division. 17 divided by 5 is 3 remainder 2, so 17
    % 5 is 2.
- q: Which operator checks whether two values are equal?
  options:
  - '='
  - ==
  - =>
  - '!='
  answer: 1
  why: A single = assigns a value to a variable; the double == is the comparison operator that tests for
    equality and returns True or False.
- q: What is the value of (5 > 3) and (2 > 4)?
  options:
  - 'True'
  - 'False'
  - '5'
  - An error
  answer: 1
  why: 5 > 3 is True but 2 > 4 is False. The 'and' operator needs both sides True, so the whole expression
    is False.
- q: In an if/elif/else chain, how many of the blocks actually run?
  answer: At most one — Python runs the first block whose condition is True, then skips the rest.
  why: Python checks each condition top to bottom and executes only the first matching branch; else runs
    only if none matched.
- q: Name two values that are considered falsy in Python.
  answer: 'Any two of: 0, 0.0, an empty string, an empty list, an empty dict, or None.'
  why: Falsy values evaluate to False in a boolean context, so an if on them runs the else branch.
- q: What does 7 // 2 give, and why does it differ from 7 / 2?
  answer: 7 // 2 gives 3 (floor division, the whole-number part); 7 / 2 gives 3.5 (true division).
  why: // discards the fractional part and returns the floor, while / always returns a float result.
resources:
- label: Python docs — More Control Flow Tools (if statements)
  url: https://docs.python.org/3/tutorial/controlflow.html#if-statements
- label: Python docs — Operators and Expressions reference
  url: https://docs.python.org/3/reference/expressions.html
- label: Real Python — Conditional Statements in Python
  url: https://realpython.com/python-conditional-statements/
- label: 'Python Crash Course (Eric Matthes) — Chapter 5: If Statements'
---

## Operators: doing things with values

An **operator** is a symbol that combines values to produce a new value. You already know the arithmetic ones from maths, but Python adds a couple worth memorising.

```python
print(7 + 2)    # 9   addition
print(7 - 2)    # 5   subtraction
print(7 * 2)    # 14  multiplication
print(7 / 2)    # 3.5 true division (always a float)
print(7 // 2)   # 3   floor division (whole part)
print(7 % 2)    # 1   modulo (the remainder)
print(7 ** 2)   # 49  exponent (7 squared)
```

The two that surprise newcomers are `//` and `%`. Floor division `//` throws away the fraction; modulo `%` keeps only the remainder. Together they answer *how many whole times, and what is left over*.

## Comparison operators

Comparison operators ask a yes/no question and return a **boolean** — `True` or `False`.

```python
print(5 == 5)   # True   equal to
print(5 != 3)   # True   not equal to
print(5 > 3)    # True   greater than
print(5 <= 4)   # False  less than or equal
```

The biggest beginner trap lives here: `=` **assigns** a value, while `==` **compares**. Using one where you meant the other is a bug you will meet many times.

## Logical operators: and, or, not

Real decisions combine several conditions. Python uses readable words instead of symbols.

- `and` — True only if **both** sides are True
- `or` — True if **at least one** side is True
- `not` — flips True to False and back

```python
age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("Welcome in")
```

## Conditionals: making decisions

A conditional runs a block of code **only when** a condition is True. The keyword is `if`, followed by a condition and a colon; the indented lines run when the condition holds.

Use `elif` (else-if) for extra cases and `else` as the catch-all. Python checks each condition top to bottom and runs **only the first** that is True.

```python
score = 72
if score >= 70:
    print("Distinction")
elif score >= 50:
    print("Pass")
else:
    print("Resit")
```

## Truthy and falsy

An `if` does not need a comparison — it just needs something **truthy**. In Python, `0`, `0.0`, `""` (empty string), empty lists/dicts and `None` are **falsy**; almost everything else is **truthy**.

```python
name = ""
if name:
    print("Got a name")
else:
    print("Name is empty")   # this runs
```

## Your task

Write a small script that reads a number and prints whether it is **negative, zero, or positive**, and separately whether it is **even or odd** using `%`.
