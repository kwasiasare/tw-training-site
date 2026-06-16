---
course: dami-ai-career
title: Functions & modules
month: 1
monthTitle: Python Foundations + Git
lesson: 6
summary: Write reusable, named blocks of code — pass them inputs, get results back, and organise your
  work into modules.
objectives:
- Define and call your own functions with the def keyword
- Pass information in with parameters and arguments
- Return results and understand the difference between print and return
- Use default and keyword arguments to make functions flexible
- Understand variable scope (local vs global)
- Reuse code across files with modules and import
video: m1-l06-functions.mp4
quiz:
- q: What keyword defines a function in Python?
  options:
  - function
  - def
  - func
  - define
  answer: 1
  why: def (short for define) starts a function definition, followed by the name, parentheses, and a colon.
- q: What is the difference between a parameter and an argument?
  answer: A parameter is the name in the function definition; an argument is the actual value you pass
    when calling.
  why: def greet(name) — name is a parameter; greet("Dami") — "Dami" is the argument.
- q: What does a function return if it has no return statement?
  options:
  - '0'
  - An error
  - None
  - An empty string
  answer: 2
  why: A function with no explicit return automatically returns the special value None.
- q: True or false — a variable created inside a function can be used after the function finishes.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Such variables are local and disappear once the function returns.
resources:
- label: Python docs — Defining Functions (official tutorial 4.7)
  url: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- label: 'Python Crash Course (Eric Matthes) — Chapter 8: Functions'
- label: Real Python — Defining Your Own Python Function
  url: https://realpython.com/defining-your-own-python-function/
---

## Why functions?

A **function** is a reusable, named block of code. You write a piece of logic once, give it a name, and run it whenever you need it. Without functions you would copy and paste the same lines everywhere — and a bug means fixing every copy.

As a maths graduate this feels natural: a function takes an **input**, does something, and produces an **output** — like *f(x) = x²*.

## Defining and calling a function

Use `def`, a name, parentheses, and a colon. The indented block is the **body**. Defining does not run it — you **call** it with its name and parentheses.

```python
def greet():
    print("Hello, world!")

greet()   # call it
```

## Parameters and arguments

The names inside the parentheses are **parameters**; the values you pass are **arguments**.

```python
def greet(name):
    print("Hello, " + name + "!")

greet("Dami")
```

## Returning values

`return` hands a value back. Note: `print` only shows text; `return` gives back a value you can store.

```python
def add(a, b):
    return a + b

total = add(3, 4)   # 7
```

## Scope and modules

Variables made inside a function are **local** and vanish when it ends. A **module** is a Python file of functions you `import` elsewhere — and the standard library gives you thousands for free.

```python
import math
print(math.sqrt(16))   # 4.0
```

## Your task

Take one of your earlier scripts and **rewrite it using functions**.
