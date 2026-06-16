---
course: dami-ai-career
title: Loops
month: 1
monthTitle: Python Foundations + Git
lesson: 5
summary: Repeat work automatically — walk through collections with for loops and keep going until a condition
  changes with while loops.
objectives:
- Use a for loop to walk through every item in a collection
- Generate sequences of numbers with range()
- Use a while loop to repeat until a condition becomes false
- Control loops with break and continue
- Avoid infinite loops by always changing the condition
- Build up results by looping with an accumulator variable
video: m1-l05-loops.mp4
quiz:
- q: Which loop should you use when you know the collection you want to walk through?
  options:
  - while loop
  - for loop
  - if statement
  - break loop
  answer: 1
  why: A for loop is built for iterating over a known collection or sequence, visiting each item once.
- q: What does range(2, 8) produce?
  options:
  - 2 to 8 including 8
  - 2, 3, 4, 5, 6, 7
  - 8 numbers starting at 2
  - 2 and 8 only
  answer: 1
  why: range(start, stop) includes start but stops BEFORE stop, so you get 2, 3, 4, 5, 6, 7.
- q: What is the difference between break and continue?
  answer: break exits the loop entirely; continue skips the rest of the current iteration and moves to
    the next one.
  why: break stops looping altogether, while continue only abandons the current pass and carries on with
    the next item.
- q: What usually causes an infinite loop in a while loop?
  options:
  - Using range()
  - Forgetting to change the condition variable
  - Using a for loop instead
  - Indenting the body
  answer: 1
  why: If the condition never becomes false because nothing inside the loop updates it, the loop runs
    forever.
- q: True or false — a for loop in Python can iterate directly over the characters of a string.
  options:
  - 'True'
  - 'False'
  answer: 0
  why: True. Strings are sequences, so 'for ch in word' visits each character one at a time.
- q: What is an accumulator in a loop?
  answer: A variable defined before the loop that you build up (add to or append to) on each pass to collect
    a running result.
  why: For example, total = 0 before the loop, then total = total + n inside it sums every value.
resources:
- label: Python docs — The for statement & range (official tutorial 4)
  url: https://docs.python.org/3/tutorial/controlflow.html#for-statements
- label: 'Python Crash Course (Eric Matthes) — Chapter 4: Working with Lists & Chapter 7: while loops'
- label: Real Python — Python for Loops (Definite Iteration)
  url: https://realpython.com/python-for-loop/
- label: Real Python — Python while Loops (Indefinite Iteration)
  url: https://realpython.com/python-while-loop/
---

## Why loops?

Computers are brilliant at doing the same thing over and over without getting bored. A **loop** is how you tell Python to repeat a block of code. Without loops you would copy and paste the same lines once per item — unthinkable when you have a thousand items.

As a maths graduate, think of it like a summation sign. *Σ from i=1 to n* says "do this for every i". A loop is that idea made executable.

## The for loop

A **for loop** walks through every item in a collection — a list, a string, a range — and runs its body once per item. The indented block is the body.

```python
names = ["Dami", "Ada", "Sam"]
for name in names:
    print("Hello, " + name)
```

Each time round, `name` holds the next item. The loop ends automatically when the collection is exhausted.

## Counting with range()

When you want numbers rather than an existing list, use `range`. Note that `range(start, stop)` **stops before** `stop`.

```python
for i in range(1, 6):
    print(i)        # prints 1 2 3 4 5
```

A classic use is an **accumulator** — a variable you build up on each pass.

```python
total = 0
for n in range(1, 101):
    total = total + n
print(total)        # 5050
```

## The while loop

A **while loop** repeats *as long as* a condition stays true. Use it when you don't know in advance how many times to loop.

```python
count = 5
while count > 0:
    print(count)
    count = count - 1   # MUST change the condition
print("Lift off!")
```

The golden rule: something inside the loop must eventually make the condition false, or you get an **infinite loop**.

## break and continue

`break` exits the loop immediately. `continue` skips the rest of the current pass and jumps to the next item.

```python
for n in range(1, 10):
    if n == 5:
        break       # stop completely at 5
    if n % 2 == 0:
        continue    # skip even numbers
    print(n)        # prints 1 3
```

## Your task

Write a loop that prints the **times table** for a number of your choice (e.g. 1 through 12), then add a `while` loop that keeps asking until the user types "quit".
