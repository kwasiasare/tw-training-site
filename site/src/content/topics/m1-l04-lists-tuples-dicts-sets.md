---
title: Lists, tuples, dictionaries & sets
month: 1
monthTitle: Python Foundations + Git
lesson: 4
summary: Meet Python's four core collections — store many values, look them up by key, and choose the
  right structure for each job.
objectives:
- Create and index lists, and change them in place
- Use tuples for fixed, unchangeable groups of values
- Store and retrieve data by key with dictionaries
- Use sets to hold unique values and do membership tests fast
- Choose the right collection for a given problem
- Loop over each collection cleanly
video: m1-l04-lists-tuples-dicts-sets.mp4
quiz:
- q: Which collection is ordered and changeable (mutable)?
  options:
  - tuple
  - list
  - set
  - frozenset
  answer: 1
  why: A list is ordered and mutable — you can change, add, and remove items after creating it.
- q: What is the main difference between a list and a tuple?
  answer: A list is mutable (can be changed); a tuple is immutable (fixed once created).
  why: Use a tuple when the group of values should never change, such as a coordinate (x, y).
- q: How do you get the value for the key "name" from a dictionary called user?
  options:
  - user("name")
  - user["name"]
  - user.name
  - user{"name"}
  answer: 1
  why: 'Dictionaries are accessed with square brackets and the key: user["name"].'
- q: What happens when you add a duplicate value to a set?
  options:
  - It raises an error
  - It is ignored — sets keep only unique values
  - It is added twice
  - It overwrites the whole set
  answer: 1
  why: Sets store only unique values, so adding a duplicate simply has no effect.
- q: What does len(my_list) return?
  answer: The number of items in the list.
  why: len() works on any collection and gives you its size — handy for loops and checks.
- q: Which collection should you use to count unique visitors to a website?
  answer: A set — it automatically removes duplicates so only distinct visitors remain.
  why: Sets discard repeats, so the size of the set equals the number of unique values.
resources:
- label: Python docs — Data Structures (official tutorial 5)
  url: https://docs.python.org/3/tutorial/datastructures.html
- label: Python Crash Course (Eric Matthes) — Chapters 3, 4 & 6
- label: Real Python — Lists and Tuples in Python
  url: https://realpython.com/python-lists-tuples/
- label: Real Python — Dictionaries in Python
  url: https://realpython.com/python-dicts/
---

## Why collections?

So far you have stored one value per variable. Real data comes in groups: a list of marks, a row of coordinates, a record of a person, a set of tags. Python gives you four core **collections** to hold groups of values, and choosing the right one makes your code clearer and faster.

The four are: **list**, **tuple**, **dictionary**, and **set**.

## Lists — ordered and changeable

A **list** keeps items in order and lets you change them. Write it with square brackets. You reach an item by its **index**, counting from zero.

```python
scores = [70, 85, 90]
print(scores[0])      # 70 (first item)
scores.append(60)     # add to the end
scores[1] = 88        # change an item
print(len(scores))    # 4
```

## Tuples — fixed and unchangeable

A **tuple** looks like a list but uses round brackets and cannot be changed after it is made — it is **immutable**. Use it for groups that should stay fixed, like an (x, y) point.

```python
point = (3, 4)
x, y = point          # unpack into two variables
print(x, y)           # 3 4
# point[0] = 9        # would raise an error
```

## Dictionaries — look up by key

A **dictionary** stores **key-value** pairs. Instead of a numeric index, you look things up by a meaningful key. Write it with curly braces and colons.

```python
user = {"name": "Dami", "age": 25}
print(user["name"])       # Dami
user["age"] = 26          # update a value
user["city"] = "Lagos"    # add a new pair
for key, value in user.items():
    print(key, "->", value)
```

## Sets — unique values only

A **set** holds only **unique** values and has no order. It is perfect for removing duplicates and for fast membership tests.

```python
tags = {"python", "git", "python"}
print(tags)               # {'python', 'git'} — duplicate gone
tags.add("sql")
print("git" in tags)      # True
```

## Choosing the right one

Use a **list** for an ordered, changeable sequence. Use a **tuple** for a fixed group. Use a **dictionary** to label data with keys. Use a **set** for uniqueness and fast lookups.

## Your task

Build a small contacts program: keep each contact as a **dictionary**, store all contacts in a **list**, and use a **set** to track which cities appear.
