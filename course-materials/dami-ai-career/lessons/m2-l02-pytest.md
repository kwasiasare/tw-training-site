---
course: dami-ai-career
title: Automated testing with pytest
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 2
summary: Write small automated checks that prove your code works and catch bugs the moment they appear.
objectives:
- Explain why automated tests give you confidence to change code
- Install pytest and run it from the command line
- Write test functions named test_ that use plain assert
- Read pytest output to find which test failed and why
- Test edge cases and check that code raises the right exceptions
- Use parametrize to run one test over many inputs
- Organise tests in a tests/ folder next to your code
video: m2-l02-pytest.mp4
quiz:
- q: How does pytest decide which functions are tests?
  options:
  - They are decorated with @test
  - Their names start with test_
  - They are in a class called Test
  - They return True
  answer: 1
  why: By default pytest collects functions whose names start with test_ in files named test_*.py or *_test.py.
- q: What keyword do you use inside a pytest test to check a condition?
  options:
  - expect
  - assert
  - check
  - verify
  answer: 1
  why: pytest uses Python's plain assert statement and rewrites it to show a helpful message when it fails.
- q: What does a green dot (.) mean in pytest's output?
  options:
  - A test was skipped
  - A test passed
  - A test failed
  - A test errored
  answer: 1
  why: Each dot is one passing test; F marks a failure and E marks an error during setup.
- q: Why write automated tests instead of just running the program by hand?
  answer: Tests run instantly and repeatedly, so they catch bugs the moment code changes and give you
    confidence to refactor.
  why: Manual checking is slow, forgettable, and easy to skip; automated tests run the same checks every
    time in seconds.
- q: Which pytest feature runs the same test logic over many input/expected pairs?
  options:
  - '@pytest.fixture'
  - '@pytest.mark.parametrize'
  - '@pytest.mark.skip'
  - '@pytest.raises'
  answer: 1
  why: '@pytest.mark.parametrize feeds a list of cases into one test function, reporting each case separately.'
- q: How do you assert that a function raises a ValueError for bad input?
  answer: 'Use a with pytest.raises(ValueError): block and call the function inside it.'
  why: pytest.raises is a context manager that passes only if the expected exception is raised inside
    the block.
resources:
- label: pytest — official documentation (Get Started)
  url: https://docs.pytest.org/en/stable/getting-started.html
- label: Real Python — Effective Python Testing With pytest
  url: https://realpython.com/pytest-python-testing/
- label: Python docs — unittest.assert reference (background on assertions)
  url: https://docs.python.org/3/library/unittest.html
- label: Python Testing with pytest (Brian Okken) — book
---

## Why automated tests?

A **test** is code that checks your other code does what you expect. Instead of running your program by hand and eyeballing the output, you write small functions that say "given this input, the answer should be that" — and a tool runs them all in seconds.

For a maths graduate this is just **proof by example, automated**. You state what should be true, and the machine verifies it every single time you change anything. The real payoff is confidence: with tests you can refactor or add features without fear of silently breaking old behaviour.

## Installing and running pytest

`pytest` is the most popular testing tool in Python. Install it with pip, then run it from your project folder. It automatically finds your tests.

```bash
pip install pytest
pytest
```

pytest discovers files named `test_*.py`, and inside them, functions whose names start with `test_`.

## Your first test

A test is an ordinary function. Inside it you use Python's plain `assert` keyword: if the condition is true the test passes; if not, it fails. Put the function under test in one file and the test in another.

```python
# math_utils.py
def add(a, b):
    return a + b

# test_math_utils.py
from math_utils import add

def test_add_positives():
    assert add(2, 3) == 5

def test_add_negatives():
    assert add(-1, -1) == -2
```

Run `pytest` and you'll see a dot for each pass. A failure prints the line, the expected value, and the actual value — pytest rewrites your `assert` to show both sides.

## Edge cases and exceptions

Good tests cover the boring cases *and* the tricky ones: empty input, zero, negatives, and inputs that should be rejected. To check that bad input raises an error, use `pytest.raises`.

```python
import pytest
from math_utils import divide

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

The test passes only if the expected exception is raised inside the `with` block.

## Many cases at once: parametrize

When you want the same check over several inputs, don't copy-paste. `@pytest.mark.parametrize` feeds a list of cases into one test, and each case is reported separately.

```python
import pytest
from math_utils import add

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## Your task

Create a `tests/` folder, pick a function you wrote earlier, and write at least **three tests** for it: one normal case, one edge case, and one that checks an error is raised. Run `pytest` until it is all green.
