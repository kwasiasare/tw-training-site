---
course: dami-ai-career
title: 'Advanced Python: comprehensions, generators, decorators'
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 1
summary: Write concise comprehensions, memory-efficient generators, and reusable decorators to make your
  Python cleaner, faster, and more Pythonic.
objectives:
- Build lists, dicts and sets with comprehensions
- Add filtering conditions inside a comprehension
- Write generator functions using yield
- Explain why generators save memory with large data
- Understand that functions are first-class objects
- Write and apply a basic decorator with @
- 'Choose the right tool: comprehension, generator, or loop'
video: m2-l01-advanced-python.mp4
quiz:
- q: What does the comprehension [x*x for x in range(4)] produce?
  options:
  - '[1, 4, 9, 16]'
  - '[0, 1, 4, 9]'
  - '[0, 1, 2, 3]'
  - '[1, 2, 3, 4]'
  answer: 1
  why: range(4) gives 0,1,2,3, and squaring each gives 0, 1, 4, 9.
- q: Which keyword turns a function into a generator?
  options:
  - return
  - async
  - yield
  - gen
  answer: 2
  why: yield produces a value and pauses the function, resuming where it left off on the next request.
- q: What is the main advantage of a generator over building a full list?
  options:
  - It runs on multiple cores
  - It uses far less memory
  - It sorts results automatically
  - It is always more accurate
  answer: 1
  why: A generator yields one item at a time instead of holding every item in memory, so it scales to
    huge or infinite sequences.
- q: In Python, what does it mean that functions are first-class objects?
  answer: Functions can be assigned to variables, passed as arguments, and returned from other functions,
    just like any other value.
  why: This is exactly what makes decorators possible — a decorator is a function that takes a function
    and returns a new one.
- q: What does the @ symbol do above a function definition?
  answer: It applies a decorator — it wraps the function below it with the named decorator function.
  why: '@timer above def work() is shorthand for work = timer(work).'
- q: 'Rewrite this loop as a list comprehension: result = []; for n in nums: if n > 0: result.append(n)'
  answer: '[n for n in nums if n > 0]'
  why: The expression comes first, then the for clause, then the optional if filter.
resources:
- label: Python docs — List, Dict and Set Comprehensions (tutorial 5)
  url: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
- label: Python docs — Generators (tutorial 9.9)
  url: https://docs.python.org/3/tutorial/classes.html#generators
- label: Real Python — Primer on Python Decorators
  url: https://realpython.com/primer-on-python-decorators/
- label: Fluent Python (Luciano Ramalho) — Chapters on iterables and decorators
---

## Comprehensions: build collections in one line

A **comprehension** is a compact way to build a list, dictionary, or set from an existing iterable. Instead of creating an empty list and appending in a loop, you describe the whole result in one expression.

```python
# the long way
squares = []
for x in range(5):
    squares.append(x * x)

# the comprehension
squares = [x * x for x in range(5)]   # [0, 1, 4, 9, 16]
```

You can add an `if` to filter, and the same pattern works for dicts and sets.

```python
evens = [n for n in range(10) if n % 2 == 0]   # [0, 2, 4, 6, 8]
lengths = {w: len(w) for w in ["hi", "world"]}  # {'hi': 2, 'world': 5}
unique = {c for c in "banana"}                  # {'b', 'a', 'n'}
```

## Generators: one item at a time

A comprehension builds the whole collection in memory. A **generator** produces values lazily — one at a time, only when asked. You write one with a function that uses `yield` instead of `return`.

```python
def count_up_to(limit):
    n = 1
    while n <= limit:
        yield n
        n += 1

for value in count_up_to(3):
    print(value)   # 1, then 2, then 3
```

Each call to `yield` hands back a value and **pauses** the function; it resumes from that exact spot next time. This means a generator can describe a sequence too big to fit in memory — even an infinite one.

## Why generators save memory

If you build a list of ten million squares, all ten million live in memory at once. A generator holds only the current value and a little state, so memory stays flat no matter how long the sequence is. Use a **generator expression** — just round brackets instead of square — when you only iterate once.

```python
total = sum(x * x for x in range(10_000_000))   # tiny memory footprint
```

## Functions are first-class objects

In Python a function is just a value. You can store it in a variable, pass it to another function, or return it from one. This is the foundation decorators are built on.

```python
def shout(text):
    return text.upper()

say = shout          # store the function itself
print(say("hi"))     # HI
```

## Decorators: wrap behaviour around a function

A **decorator** is a function that takes a function and returns a new one with extra behaviour added — logging, timing, access checks — without changing the original code. The `@name` syntax above a definition applies it.

```python
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_add(a, b):
    return a + b

slow_add(2, 3)   # prints timing, returns 5
```

## Your task

Take a `for` loop from an earlier lesson and rewrite it as a comprehension. Then write one generator function and one simple decorator that prints a message before and after the wrapped function runs.
