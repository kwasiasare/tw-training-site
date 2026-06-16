---
title: Variables, data types & strings
month: 1
monthTitle: Python Foundations + Git
lesson: 2
summary: Store values in variables, recognise Python's core data types, and work confidently with text
  using strings.
objectives:
- Create variables and assign values with the equals sign
- 'Name the four core data types: int, float, str and bool'
- Use type() to inspect what kind of value you have
- Convert between types with int(), float() and str()
- Build and format text using f-strings
- Use common string methods like upper, lower and strip
- Index and slice strings to pull out characters
video: m1-l02-variables-types-strings.mp4
quiz:
- q: What does the line  age = 30  do?
  options:
  - Compares age to 30
  - Creates a variable named age holding the value 30
  - Prints 30
  - Defines a function
  answer: 1
  why: 'A single equals sign is assignment: it stores the value 30 in a variable called age. Double equals
    (==) is comparison.'
- q: What type does Python give the value  3.0 ?
  options:
  - int
  - float
  - str
  - bool
  answer: 1
  why: Any number written with a decimal point is a float (floating-point number), even if the fractional
    part is zero.
- q: What is printed by  print(type("5")) ?
  options:
  - <class 'int'>
  - <class 'float'>
  - <class 'str'>
  - '5'
  answer: 2
  why: The quotes make "5" a string, not a number. type() reports <class 'str'>.
- q: Write the expression that converts the string "42" into the integer 42.
  answer: int("42")
  why: int() parses a string of digits into a whole number. float("42") would give 42.0 instead.
- q: Given  name = "Dami" , write an f-string that produces the text  Hello, Dami!
  answer: f"Hello, {name}!"
  why: Prefix the string with f and wrap the variable in curly braces; Python inserts its value where
    the braces are.
- q: What does  "  hi  ".strip()  return?
  options:
  - '"hi"'
  - '"  hi  "'
  - '"HI"'
  - '"h i"'
  answer: 0
  why: strip() removes whitespace from both ends of a string, leaving "hi" with no surrounding spaces.
resources:
- label: Python docs — An Informal Introduction (Numbers & Strings)
  url: https://docs.python.org/3/tutorial/introduction.html
- label: Python docs — Text Sequence Type (str methods)
  url: https://docs.python.org/3/library/stdtypes.html#string-methods
- label: Python Crash Course (Eric Matthes) — Chapters 2 & 3
- label: Real Python — Python f-Strings
  url: https://realpython.com/python-f-strings/
---

## What is a variable?

A **variable** is a name that points to a value stored in memory. You create one with a single equals sign: the name on the left, the value on the right.

```python
age = 30
name = "Dami"
print(name, "is", age)
```

Think of `=` as *assignment*, not the mathematical equals you know. It means "store this value under this name". Double equals `==` is the one that asks "are these equal?".

## The core data types

Every value in Python has a **type**. The four you'll use constantly are:

- `int` — whole numbers, like `30`
- `float` — numbers with a decimal point, like `3.14`
- `str` — text (a *string*), in quotes, like `"Dami"`
- `bool` — `True` or `False`

Use `type()` to check any value:

```python
print(type(30))       # <class 'int'>
print(type(3.14))     # <class 'float'>
print(type("Dami"))   # <class 'str'>
print(type(True))     # <class 'bool'>
```

## Converting between types

Types don't always mix. Adding the string `"5"` to the number `5` is an error. You **convert** with `int()`, `float()` and `str()`.

```python
x = "5"
n = int(x)         # the number 5
print(n + 10)      # 15
print("Total: " + str(n + 10))   # Total: 15
```

This matters a lot later: data read from files, web forms, or a database often arrives as text and must be converted before you can do maths with it.

## Working with strings

Strings are sequences of characters. The cleanest way to build text from variables is an **f-string** — put an `f` before the quote and wrap variables in curly braces.

```python
name = "Dami"
age = 30
print(f"{name} is {age} years old")
```

Strings come with handy **methods**. A method is a function attached to a value, called with a dot:

```python
title = "  Data Science  "
print(title.strip())        # "Data Science"
print(title.strip().upper())# "DATA SCIENCE"
print(len("Dami"))          # 4
```

## Indexing and slicing

Each character has a position, starting at **0**. Use square brackets to grab one character, or a range to grab a *slice*.

```python
word = "Python"
print(word[0])    # P
print(word[-1])   # n (last)
print(word[0:3])  # Pyt
```

## Your task

Ask the user for their name and birth year with `input()`, convert the year to an `int`, work out their age, and print a friendly message using an f-string.
