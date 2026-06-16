---
course: dami-ai-career
title: Python coding interview practice
month: 6
monthTitle: Apply & Interview
lesson: 4
summary: Practise solving coding problems out loud — clarify, plan, code clean Python, test edge cases,
  and talk through trade-offs like an engineer.
objectives:
- Follow a repeatable problem-solving framework under interview pressure
- Clarify the problem and state assumptions before writing code
- Reason about time and space complexity using Big-O notation
- 'Pick the right built-in data structure: list, dict, set, deque'
- Write clean, readable Python and test edge cases out loud
- Recover gracefully when you get stuck or hit a bug
video: m6-l04-python-interview.mp4
quiz:
- q: What is the average time complexity of looking up a key in a Python dict?
  options:
  - O(n)
  - O(log n)
  - O(1)
  - O(n log n)
  answer: 2
  why: Dicts are hash maps, so average key lookup is constant time O(1) — a core reason to reach for them
    in interviews.
- q: Which data structure gives O(1) membership tests and removes duplicates?
  options:
  - list
  - set
  - tuple
  - str
  answer: 1
  why: A set stores unique hashable items and supports O(1) average 'in' checks, unlike a list which is
    O(n).
- q: Before writing any code in an interview, what should you do first?
  options:
  - Start typing the brute-force solution
  - Clarify the problem and ask about inputs and edge cases
  - Announce the optimal Big-O
  - Stay silent until you have the full answer
  answer: 1
  why: Clarifying inputs, output, constraints and edge cases shows engineering judgement and prevents
    solving the wrong problem.
- q: In one sentence, what is Big-O notation used for?
  answer: It describes how an algorithm's running time or memory grows as the input size grows.
  why: Big-O focuses on growth rate for large inputs, ignoring constants, so you can compare approaches.
- q: Name one edge case worth checking on a function that processes a list of numbers.
  answer: 'An empty list (also valid: a single element, negatives, duplicates, or very large input).'
  why: Empty and single-element inputs are the classic cases that break naive code and impress interviewers
    when handled.
- q: If you get stuck mid-problem, what is the best move?
  options:
  - Go silent and keep typing
  - Erase everything and restart
  - Talk through your thinking and state a simpler brute-force first
  - Ask the interviewer for the answer
  answer: 2
  why: Interviewers score your communication and process; a working brute-force you can explain beats
    silent perfection you never reach.
resources:
- label: NeetCode — curated coding interview problems and patterns
  url: https://neetcode.io/
- label: LeetCode — practice problems by topic and difficulty
  url: https://leetcode.com/
- label: Python docs — Data Structures (list, dict, set, deque)
  url: https://docs.python.org/3/tutorial/datastructures.html
- label: Cracking the Coding Interview (Gayle Laakmann McDowell)
---

## What a coding interview really tests

A coding interview is **not** a test of whether you've memorised the answer. It tests how you *think*: can you understand a problem, break it down, write clean code, and communicate while you do it? As a maths graduate you already have the strongest muscle — structured problem solving. Now you add a spoken process and fluent Python.

The single biggest mistake beginners make is going silent and typing. Interviewers can't read your mind. **Narrate everything.**

## A framework you can repeat

Use the same five steps on every problem so nerves don't derail you:

1. **Clarify** — restate the problem, ask about input types, size, and edge cases.
2. **Examples** — work a small example by hand to confirm understanding.
3. **Plan** — describe an approach in plain English before coding; mention the Big-O.
4. **Code** — write clean Python, talking as you go.
5. **Test** — run through edge cases out loud: empty input, one element, duplicates.

It is completely fine to start with a brute-force solution, say so, then improve it.

## Big-O in one minute

**Big-O** describes how running time grows as input size *n* grows. You compare approaches by their growth, ignoring constants.

- `O(1)` — constant, e.g. a dict lookup.
- `O(n)` — one pass through the data.
- `O(n log n)` — typical sorting.
- `O(n^2)` — nested loops over the same data; usually a red flag you can improve.

## Know your data structures

Most interview wins come from picking the right built-in. A **dict** or **set** turns an O(n^2) scan into an O(n) pass.

```python
# Two-sum: find indices of two numbers adding to target.
def two_sum(nums, target):
    seen = {}                      # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:           # O(1) lookup
            return [seen[need], i]
        seen[x] = i
    return []                      # no pair found

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

The naive version checks every pair in O(n^2); the dict version is a single O(n) pass.

## Test edge cases out loud

After coding, walk through inputs that break naive code. State each one and check your code handles it.

```python
assert two_sum([], 5) == []          # empty list
assert two_sum([3], 3) == []         # single element
assert two_sum([3, 3], 6) == [0, 1]  # duplicates
print("all checks pass")
```

## Practise deliberately

Don't grind hundreds of random problems. Pick a pattern — hash maps, two pointers, sliding window, binary search — and do three or four problems on it until it feels automatic. Solve them *out loud*, even alone, and time yourself. The goal is fluency under pressure, not coverage.
