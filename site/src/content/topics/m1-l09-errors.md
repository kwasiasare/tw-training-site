---
title: Errors & exception handling
month: 1
monthTitle: Python Foundations + Git
lesson: 9
summary: Read tracebacks, catch exceptions with try/except, and write code that fails clearly instead
  of crashing silently.
objectives:
- Tell the difference between syntax errors and runtime exceptions
- Read a Python traceback from the bottom up
- Catch errors with try and except blocks
- Catch specific exception types instead of everything
- Use else and finally for cleanup and follow-up code
- Raise your own exceptions to signal bad input
- Decide when to handle an error and when to let it crash
video: m1-l09-errors.mp4
quiz:
- q: Which statement starts a block that handles errors in Python?
  options:
  - catch
  - try
  - handle
  - rescue
  answer: 1
  why: Python uses try to mark code that might fail, with an except block to handle the error.
- q: When reading a traceback, which line tells you what actually went wrong?
  options:
  - The first line
  - The last line
  - The middle line
  - Any line with a file path
  answer: 1
  why: 'Read tracebacks bottom-up: the final line names the exception type and message.'
- q: Why is catching a specific exception better than a bare 'except:'?
  answer: A bare except hides unexpected bugs and catches things you did not mean to, like KeyboardInterrupt;
    naming the type only handles what you expect.
  why: Catching too broadly swallows real problems and makes debugging much harder.
- q: What does the 'finally' block do?
  options:
  - Runs only if no error occurred
  - Runs only if an error occurred
  - Runs no matter what, error or not
  - Runs before the try block
  answer: 2
  why: finally always runs, making it ideal for cleanup like closing files or connections.
- q: Which keyword do you use to trigger an exception yourself?
  answer: raise
  why: raise lets you signal an error, for example raise ValueError("age must be positive").
- q: True or false — a syntax error can be caught with try/except.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Syntax errors stop the code from running at all, so try/except never gets a chance to run.
resources:
- label: Python docs — Errors and Exceptions (official tutorial 8)
  url: https://docs.python.org/3/tutorial/errors.html
- label: Python docs — Built-in Exceptions
  url: https://docs.python.org/3/library/exceptions.html
- label: 'Real Python — Python Exceptions: An Introduction'
  url: https://realpython.com/python-exceptions/
- label: 'Python Crash Course (Eric Matthes) — Chapter 10: Files and Exceptions'
---

## Two kinds of errors

Python has two broad kinds of errors. A **syntax error** means the code is not valid Python — a missing colon or a stray bracket — and the program will not even start. A **runtime exception** happens while the program is running: the syntax is fine, but something goes wrong, like dividing by zero or opening a file that does not exist.

You cannot catch a syntax error with `try`/`except` because the code never runs. You *can* catch exceptions, and that is what this lesson is about.

## Reading a traceback

When an exception is not handled, Python prints a **traceback** and stops. Read it from the **bottom up**: the last line names the exception type and message; the lines above show the path of calls that led there.

```python
def divide(a, b):
    return a / b

divide(10, 0)
# ZeroDivisionError: division by zero
```

The final line, `ZeroDivisionError: division by zero`, tells you exactly what happened.

## try / except

Wrap risky code in a `try` block. If an exception happens, control jumps to the matching `except` block instead of crashing.

```python
try:
    age = int(input("Age: "))
    print(100 / age)
except ValueError:
    print("Please type a whole number.")
except ZeroDivisionError:
    print("Age cannot be zero.")
```

Catch **specific** exception types. A bare `except:` swallows everything — including bugs you did not anticipate — and makes problems invisible.

## else and finally

An `else` block runs only if the `try` succeeded with no exception. A `finally` block runs **no matter what**, which is perfect for cleanup.

```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("No such file.")
else:
    print(f.read())
    f.close()
finally:
    print("Done attempting to read.")
```

## Raising your own exceptions

Use `raise` to signal that something is wrong — for example, invalid input to your own function. This fails loudly and early, which is far better than returning a wrong answer.

```python
def set_age(age):
    if age < 0:
        raise ValueError("age must be positive")
    return age
```

## When NOT to catch

Do not catch an error just to hide it. If you cannot sensibly recover, let the program crash with its clear traceback — a silent failure is worse than a loud one. Catch errors only where you can do something useful: retry, use a default, or show the user a helpful message.

## Your task

Take a script that asks the user for a number and make it robust: keep asking until they give valid input, using `try`/`except`.
