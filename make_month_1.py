# -*- coding: utf-8 -*-
"""Builds the Month 1 study pack: Python Foundations + Git.
Run from this folder:  python make_month_1.py
"""
from doc_helpers import (
    new_doc, title_block, h1, h2, h3, para, lead, bullet, numbered,
    code_block, callout, table_from_rows, quiz, page_break,
    NAVY, ACCENT, GREY, GREEN, AMBER, RED,
)

doc = new_doc()

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
title_block(
    doc,
    "Month 1 - Python Foundations + Git",
    "From a maths brain to a coding brain: the bedrock of every AI job",
    "Maths Graduate to AI Job - 6-Month Programme  |  ~30+ hrs/week  |  Beginner-friendly, rigorous",
)

para(doc,
     "Welcome to Month 1. You already think rigorously thanks to your maths degree - that is a "
     "genuine advantage, because programming is just formalising precise instructions for a machine. "
     "What you have not yet built is fluency: the muscle memory of writing, running, and debugging code "
     "every single day. This month builds that fluency from absolute first principles and finishes with "
     "the three tools every working AI engineer touches daily: the terminal, Python, and Git. Read the "
     "notes, type out (do not copy-paste) every code example, take the quizzes honestly, and finish the "
     "project. Typing the examples by hand is non-negotiable - it is how the syntax moves from your eyes "
     "into your fingers.")

# ---------------------------------------------------------------------------
# Learning objectives
# ---------------------------------------------------------------------------
h1(doc, "Learning objectives")
para(doc, "By the end of Month 1 you will be able to:")
for t in [
    "Explain what happens when Python runs a script, and set up a working development environment from scratch.",
    "Use Python's core data types (int, float, str, bool) and manipulate strings confidently.",
    "Write correct conditional logic with comparison and boolean operators.",
    "Choose the right built-in collection (list, tuple, dict, set) for a problem and use it well.",
    "Write loops (for/while) and control them with break, continue, and comprehensions.",
    "Define functions and modules with clear parameters, return values, and docstrings.",
    "Model real-world things with classes, including __init__ and inheritance.",
    "Read and write files, and serialise data to and from JSON.",
    "Handle errors gracefully with try/except and raise your own exceptions.",
    "Isolate project dependencies with virtual environments and install packages with pip.",
    "Track your work with Git and publish a clean repository to GitHub.",
    "Call a public web API with requests and query a SQLite database with sqlite3.",
]:
    bullet(doc, t)

page_break(doc)

# ===========================================================================
# Helper to keep topic sections consistent
# ===========================================================================

# ---------------------------------------------------------------------------
# Topic 1: How Python runs & your setup
# ---------------------------------------------------------------------------
h1(doc, "1. How Python runs & your setup")

para(doc,
     "A computer's CPU only understands machine code - raw binary instructions. Python is a high-level "
     "language, so something must translate your readable text into something the machine can act on. "
     "That something is the Python interpreter, usually the reference implementation called CPython. "
     "When you run a script, CPython first compiles your source text into an intermediate form called "
     "bytecode (you may see .pyc files appear in a __pycache__ folder - that is cached bytecode). A "
     "component called the Python Virtual Machine (PVM) then executes that bytecode one instruction at "
     "a time. This is why Python is often called an 'interpreted' language: there is no separate compile "
     "step you run by hand, and you get errors at run time rather than before.")

para(doc,
     "There are two ways to run Python. The interactive interpreter (the REPL - Read, Eval, Print, Loop) "
     "starts when you type 'python' with no file: you type one line, press Enter, and see the result "
     "immediately. It is perfect for quick experiments. The second way is a script: you save your code "
     "in a file ending in .py and run 'python myfile.py', which executes the whole file top to bottom.")

para(doc,
     "Your setup for this course: install Python from python.org (version 3.11 or newer). On Windows, "
     "tick 'Add Python to PATH' during installation so the 'python' command works in any terminal. "
     "Install Visual Studio Code as your editor, add Microsoft's official Python extension, and learn to "
     "open a terminal inside VS Code (Ctrl+`). The terminal is where you run scripts, install packages, "
     "and use Git - get comfortable living in it.")

lead(doc, "Key terms:",
     "interpreter (translates and runs your code), bytecode (compiled intermediate form), REPL "
     "(interactive prompt), PATH (the list of folders your shell searches for commands), IDE/editor "
     "(VS Code).")

code_block(doc,
"""# hello.py  -  your first script
# Run it from a terminal with:  python hello.py

print("Hello, AI career!")          # print() writes text to the screen

# A comment starts with #. Python ignores it. Comments explain WHY, not WHAT.

name = "Dami"                        # store a value in a variable
print("Set up complete,", name)     # commas in print add a space between items

# Check your version from inside Python:
import sys
print("Running Python", sys.version)
""")

para(doc,
     "Save that as hello.py and run 'python hello.py'. If you see the greeting and your version printed, "
     "your environment works. If instead you see \"'python' is not recognized\", Python is not on your "
     "PATH - reinstall and tick the PATH box, or use 'py' on Windows.")

callout(doc, "Common mistakes",
        "Running code by clicking 'Run' in an editor without understanding it also works from the "
        "terminal - learn the terminal way, because servers have no GUI. Forgetting to add Python to "
        "PATH. Confusing the REPL (no file) with running a script. Saving a file as hello.py.txt by "
        "accident (turn on file-extension visibility). Editing one file but running another.")

quiz(doc, [
    {'q': "What does the Python interpreter (CPython) produce before the PVM executes your program?",
     'options': ["Machine code directly", "Bytecode", "Assembly", "An .exe file"],
     'answer': "B) Bytecode",
     'why': "CPython compiles source to bytecode, which the Python Virtual Machine then executes."},
    {'q': "REPL stands for which of the following?",
     'options': ["Run, Edit, Print, Load", "Read, Eval, Print, Loop",
                 "Read, Execute, Process, Log", "Recursive Evaluation Programming Language"],
     'answer': "B) Read, Eval, Print, Loop",
     'why': "It reads a line, evaluates it, prints the result, and loops for the next line."},
    {'q': "What is the PATH environment variable used for?",
     'answer': "It is the list of folders the shell searches to find an executable when you type a command like 'python'.",
     'why': "If Python's folder is not on PATH, the shell cannot find the command."},
    {'q': "True or False: a .py file must be compiled by you manually before it can run.",
     'options': ["True", "False"],
     'answer': "B) False",
     'why': "The interpreter compiles to bytecode automatically each time; there is no separate manual compile step."},
    {'q': "Which character begins a comment in Python, and what is a comment for?",
     'answer': "The # character. Comments are ignored by Python and exist to explain intent to humans.",
     'why': "Good comments explain WHY code does something, not restate WHAT it obviously does."},
    {'q': "You type 'python' with no filename and get a '>>>' prompt. What are you using?",
     'answer': "The interactive interpreter / REPL.",
     'why': "The >>> prompt is the REPL waiting for one expression or statement at a time."},
], title="Quiz - Topic 1")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 2: Variables, data types & strings
# ---------------------------------------------------------------------------
h1(doc, "2. Variables, data types & strings")

para(doc,
     "A variable is a name that refers to a value. In Python a variable is not a labelled box that holds "
     "data; it is a label attached to an object that lives in memory. When you write x = 5, Python creates "
     "an integer object 5 and binds the name x to it. Assigning y = x makes y point at the same object, "
     "not a copy. This 'names point at objects' model matters later for mutable types like lists.")

para(doc,
     "Python is dynamically typed: you do not declare a type, and a name can be rebound to a different "
     "type later. But every value still has a definite type. The core built-in types you start with are: "
     "int (whole numbers, unlimited size), float (decimal numbers, stored in binary so they have tiny "
     "rounding errors), str (text), and bool (True or False, which is technically a subtype of int where "
     "True == 1). Use type(value) to inspect a type and isinstance(value, int) to test one.")

para(doc,
     "Strings are sequences of characters written in single or double quotes. They are immutable - you "
     "cannot change a character in place; you build a new string instead. You index with [], slice with "
     "[start:stop:step], and use many built-in methods such as .upper(), .lower(), .strip(), .split(), "
     "and .replace(). Modern Python formats strings with f-strings: put an f before the quote and write "
     "expressions inside {curly braces}. This is the clearest, fastest way to build text.")

code_block(doc,
'''# --- types ---
age = 27                     # int
height = 1.78                # float
name = "Dami"                # str
is_learning = True           # bool

print(type(age), type(height), type(name), type(is_learning))
# <class 'int'> <class 'float'> <class 'str'> <class 'bool'>

# --- converting between types (casting) ---
year_text = "2026"
year = int(year_text)        # str -> int
print(year + 1)              # 2027
print(str(year) + "!")       # int -> str so we can join text

# --- string methods & slicing ---
phrase = "  Machine Learning  "
print(phrase.strip())            # "Machine Learning"  (trim whitespace)
print(phrase.strip().upper())    # "MACHINE LEARNING"
print("a,b,c".split(","))        # ['a', 'b', 'c']
print(phrase[2:9])               # slice: "Machine"

# --- f-strings: the modern way to build text ---
score = 0.8734
print(f"{name} scored {score:.1%}")     # Dami scored 87.3%
print(f"Next year you'll be {age + 1}") # expressions work inside braces

# --- floats are not exact ---
print(0.1 + 0.2)                 # 0.30000000000000004  (binary rounding)
print(round(0.1 + 0.2, 2))       # 0.3
''')

callout(doc, "Common mistakes",
        "Using = (assignment) when you mean == (comparison). Trying to add a string and an int ('age: ' "
        "+ 27 raises TypeError - cast with str() or use an f-string). Expecting 0.1 + 0.2 to equal 0.3 "
        "exactly. Trying to mutate a string in place (s[0] = 'X' fails). Forgetting that .strip() returns "
        "a NEW string and does not change the original.")

quiz(doc, [
    {'q': "What does type(True) return, and why might True == 1 be True?",
     'answer': "<class 'bool'>; bool is a subtype of int where True behaves as 1 and False as 0.",
     'why': "Booleans are integers under the hood, so True == 1 and False == 0."},
    {'q': "Which expression correctly joins the name variable with the number 27 into one string?",
     'options': ['"Age: " + 27', 'f"Age: {27}"', '"Age: ".27', "27 + \"Age\""],
     'answer': 'B) f"Age: {27}"',
     'why': "You cannot add a str and an int; an f-string (or str(27)) converts the number to text."},
    {'q': "What is printed by: print('  hi  '.strip().upper()) ?",
     'answer': "HI",
     'why': ".strip() removes the surrounding spaces, then .upper() capitalises the letters."},
    {'q': "True or False: strings in Python are mutable (you can change a character in place).",
     'options': ["True", "False"],
     'answer': "B) False",
     'why': "Strings are immutable; methods like .replace() return a brand new string."},
    {'q': "What does 'a,b,c'.split(',') return?",
     'options': ["'abc'", "['a', 'b', 'c']", "('a','b','c')", "{'a','b','c'}"],
     'answer': "B) ['a', 'b', 'c']",
     'why': ".split(',') breaks the string at each comma and returns a list of the pieces."},
    {'q': "Why does print(0.1 + 0.2) not show exactly 0.3?",
     'answer': "Floats are stored in binary, and 0.1 and 0.2 have no exact binary representation, so a tiny rounding error appears.",
     'why': "Use round() or the decimal module when exactness matters (e.g. money)."},
    {'q': "Given x = 'hello', what is x[1:4]?",
     'options': ["'hell'", "'ell'", "'ello'", "'hel'"],
     'answer': "B) 'ell'",
     'why': "Slicing is start-inclusive, stop-exclusive: indices 1, 2, 3 -> 'e','l','l'."},
], title="Quiz - Topic 2")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 3: Operators & conditionals
# ---------------------------------------------------------------------------
h1(doc, "3. Operators & conditionals")

para(doc,
     "Operators are symbols that combine values. Arithmetic operators include + - * / (true division, "
     "always returns a float), // (floor division, discards the remainder), % (modulo, the remainder), "
     "and ** (exponentiation). Comparison operators ( == != < <= > >= ) compare two values and return a "
     "bool. Boolean operators (and, or, not) combine truth values. Note the difference between == "
     "(equal value) and 'is' (the same object in memory) - use == for values, 'is' only for None.")

para(doc,
     "Conditionals let a program choose a path. The structure is if / elif / else. Python uses "
     "indentation - not braces - to group the body of each branch, so consistent indentation (4 spaces) "
     "is part of the syntax, not a style choice. The condition is any expression Python can judge as "
     "truthy or falsy. Falsy values include False, 0, 0.0, '' (empty string), [] (empty list), {} "
     "(empty dict), and None; almost everything else is truthy. This lets you write 'if items:' to mean "
     "'if the list is not empty'.")

para(doc,
     "Two important shortcuts: 'and' and 'or' short-circuit - 'a and b' stops and returns a if a is "
     "falsy, never evaluating b. And the ternary expression 'x if condition else y' chooses a value "
     "inline. Chained comparisons like 0 <= x < 100 work exactly as in maths.")

code_block(doc,
'''score = 73

# arithmetic
print(17 // 5)    # 3   (floor division)
print(17 % 5)     # 2   (remainder - great for "is it even?")
print(2 ** 10)    # 1024 (exponentiation)

# if / elif / else  -  indentation defines the blocks
if score >= 70:
    grade = "Distinction"
elif score >= 50:
    grade = "Pass"
else:
    grade = "Resit"
print(grade)                       # Distinction

# boolean logic and chained comparison (just like maths)
is_valid = 0 <= score <= 100
print(is_valid and score >= 50)    # True

# truthiness: empty collections are falsy
items = []
if not items:
    print("the list is empty")     # this prints

# ternary expression
status = "even" if score % 2 == 0 else "odd"
print(status)                      # odd

# == vs is
a = [1, 2]
b = [1, 2]
print(a == b)      # True  (same value)
print(a is b)      # False (different objects in memory)
''')

callout(doc, "Common mistakes",
        "Using = instead of == in a condition (Python catches this, but it is the classic beginner slip). "
        "Mixing tabs and spaces for indentation - pick spaces and never mix (this causes IndentationError). "
        "Using 'is' to compare values instead of == (only use 'is' with None). Forgetting the colon at the "
        "end of an if/elif/else line. Writing 'if score = 70' instead of '=='.")

quiz(doc, [
    {'q': "What does 17 % 5 evaluate to?",
     'options': ["3", "2", "3.4", "12"],
     'answer': "B) 2",
     'why': "% is modulo, the remainder of 17 divided by 5 (5*3=15, remainder 2)."},
    {'q': "Which of these values is TRUTHY?",
     'options': ["0", "''", "[]", "'0'"],
     'answer': "D) '0'",
     'why': "A non-empty string is truthy, even if its content is the character zero. 0, '', and [] are falsy."},
    {'q': "When should you use 'is' rather than '=='?",
     'answer': "Use 'is' only to test identity, in practice 'x is None'; use '==' to compare values.",
     'why': "'is' checks whether two names point at the same object; '==' checks equal value."},
    {'q': "What does the expression \"even\" if n % 2 == 0 else \"odd\" do?",
     'answer': "It is a ternary expression that evaluates to 'even' when n is even, otherwise 'odd'.",
     'why': "Form: value_if_true if condition else value_if_false."},
    {'q': "Python groups the body of an if-statement using what?",
     'options': ["Curly braces { }", "Parentheses ( )", "Indentation", "The 'end' keyword"],
     'answer': "C) Indentation",
     'why': "Python uses indentation (conventionally 4 spaces) to define blocks - it is syntax, not style."},
    {'q': "What is the value of 0 <= 5 < 3 ?",
     'options': ["True", "False", "Error", "0"],
     'answer': "B) False",
     'why': "Chained: 0 <= 5 is True but 5 < 3 is False, so the whole chain is False."},
], title="Quiz - Topic 3")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 4: Lists, tuples, dictionaries & sets
# ---------------------------------------------------------------------------
h1(doc, "4. Lists, tuples, dictionaries & sets")

para(doc,
     "Real programs juggle collections of values, and Python gives you four core containers, each suited "
     "to a different job. A list is an ordered, mutable sequence written with [] - your everyday "
     "workhorse for a changing collection. A tuple is an ordered but immutable sequence written with () "
     "- use it for fixed groupings (a coordinate, a row) where you do not want anything changed. A "
     "dictionary maps keys to values with {key: value} - the right choice whenever you look things up by "
     "name rather than position; lookups are extremely fast. A set is an unordered collection of unique "
     "values - perfect for membership tests and removing duplicates.")

para(doc,
     "Mutability is the key idea. Because lists, dicts, and sets are mutable, methods like .append() "
     "change them in place and return None - a common surprise. Because two names can point at the same "
     "list, changing it through one name is visible through the other. Tuples being immutable makes them "
     "safe to use as dictionary keys; lists cannot be keys. Choosing the right container is half of "
     "writing clean Python.")

code_block(doc,
'''# LIST - ordered, mutable
scores = [70, 55, 90]
scores.append(48)          # add to end -> [70, 55, 90, 48]
scores.sort()              # in place -> [48, 55, 70, 90]
print(scores[0], scores[-1])   # 48 90  (negative index counts from the end)
print(len(scores))             # 4

# TUPLE - ordered, immutable (good for fixed records)
point = (51.5, -0.12)          # latitude, longitude for London
lat, lon = point               # unpacking
print(lat, lon)                # 51.5 -0.12

# DICTIONARY - lookup by key
student = {"name": "Dami", "score": 73}
print(student["name"])             # Dami
student["passed"] = student["score"] >= 50   # add a new key
print(student.get("grade", "N/A")) # safe lookup with default
for key, value in student.items(): # iterate key/value pairs
    print(key, "->", value)

# SET - unique values, fast membership
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)             # {1, 2, 3}
print(3 in unique)             # True (very fast)
print(len(unique))            # 3

# list comprehension - build a list concisely
squares = [n * n for n in range(5)]   # [0, 1, 4, 9, 16]
print(squares)
''')

callout(doc, "Common mistakes",
        "Expecting scores = scores.sort() to work - .sort() returns None and sorts in place; use "
        "sorted(scores) if you want a new list. Using a list where a dict would be clearer (scanning a "
        "list for an item is slow; dict lookup is instant). Accessing a missing dict key with [] (raises "
        "KeyError) instead of .get(). Forgetting that two variables can point at the SAME list, so "
        "editing one edits 'both'. Trying to put a list inside a set (lists are unhashable).")

quiz(doc, [
    {'q': "Which collection should you use to look values up by a name/label rather than by position?",
     'options': ["list", "tuple", "dictionary", "set"],
     'answer': "C) dictionary",
     'why': "Dicts map keys to values and give fast lookup by key."},
    {'q': "What does scores.append(5) return?",
     'options': ["The new list", "5", "None", "The length"],
     'answer': "C) None",
     'why': ".append() mutates the list in place and returns None - assigning its result loses your data."},
    {'q': "Which type is immutable and can therefore be used as a dictionary key?",
     'options': ["list", "tuple", "set", "dict"],
     'answer': "B) tuple",
     'why': "Tuples are immutable and hashable, so they can be dict keys; lists cannot."},
    {'q': "What is the result of set([1, 1, 2, 3, 3])?",
     'answer': "{1, 2, 3}",
     'why': "A set keeps only unique values, removing duplicates."},
    {'q': "How do you safely read dict key 'grade' that might not exist, defaulting to 'N/A'?",
     'answer': "student.get('grade', 'N/A')",
     'why': "Indexing with [] raises KeyError if the key is missing; .get(key, default) does not."},
    {'q': "What does [n*2 for n in range(3)] produce?",
     'options': ["[0, 2, 4]", "[2, 4, 6]", "[0, 1, 2]", "[1, 2, 3]"],
     'answer': "A) [0, 2, 4]",
     'why': "range(3) yields 0,1,2; doubling each gives 0,2,4."},
    {'q': "True or False: indexing scores[-1] gives the last element.",
     'options': ["True", "False"],
     'answer': "A) True",
     'why': "Negative indices count from the end; -1 is the last item."},
], title="Quiz - Topic 4")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 5: Loops
# ---------------------------------------------------------------------------
h1(doc, "5. Loops")

para(doc,
     "A loop repeats a block of code. The for-loop iterates over the items of any iterable - a list, "
     "string, range, dictionary, or file - giving you each item in turn. Use it when you know what you "
     "are iterating over. The range(start, stop, step) function produces a sequence of integers (stop is "
     "exclusive) and is the standard way to loop a fixed number of times. The while-loop repeats as long "
     "as a condition stays true; use it when you do not know in advance how many iterations you need, "
     "such as 'keep asking until the user types quit'.")

para(doc,
     "Two control statements steer loops: break exits the loop immediately, and continue skips to the "
     "next iteration. The often-useful enumerate() gives you both the index and the item, and zip() walks "
     "two sequences in lockstep. A for-loop can have an else clause that runs only if the loop finished "
     "without hitting break - handy for search-and-report patterns. Beware the infinite loop: a while "
     "whose condition never becomes false will run forever, so make sure something inside changes the "
     "condition.")

code_block(doc,
'''# for over a list
for name in ["Ada", "Alan", "Grace"]:
    print("Hello", name)

# range: loop a fixed number of times (stop is exclusive)
total = 0
for i in range(1, 6):          # 1, 2, 3, 4, 5
    total += i
print("sum 1..5 =", total)     # 15

# enumerate gives index + item
for index, name in enumerate(["Ada", "Alan"], start=1):
    print(index, name)         # 1 Ada / 2 Alan

# zip walks two lists together
names  = ["Ada", "Alan"]
scores = [91, 88]
for n, s in zip(names, scores):
    print(f"{n}: {s}")

# while: repeat until a condition changes
countdown = 3
while countdown > 0:
    print(countdown)
    countdown -= 1             # MUST change the condition or it loops forever
print("Lift off!")

# break and continue
for n in range(10):
    if n == 5:
        break                  # stop entirely at 5
    if n % 2 == 0:
        continue               # skip even numbers
    print(n)                   # prints 1, 3
''')

callout(doc, "Common mistakes",
        "Forgetting to change the variable a while-loop depends on -> infinite loop (Ctrl+C to stop it). "
        "Off-by-one errors with range: range(1, 5) is 1,2,3,4 - the stop value is excluded. Modifying a "
        "list while looping over it (delete from a copy, or build a new list instead). Using a while-loop "
        "where a for-loop over a known sequence is clearer. Confusing break (leave the loop) with continue "
        "(skip to next iteration).")

quiz(doc, [
    {'q': "How many numbers does range(1, 5) produce, and which ones?",
     'answer': "Four numbers: 1, 2, 3, 4. The stop value 5 is excluded.",
     'why': "range is start-inclusive and stop-exclusive."},
    {'q': "Which statement immediately exits a loop entirely?",
     'options': ["continue", "break", "pass", "return"],
     'answer': "B) break",
     'why': "break leaves the loop; continue only skips to the next iteration."},
    {'q': "When is a while-loop more appropriate than a for-loop?",
     'answer': "When you do not know in advance how many iterations are needed - e.g. repeat until the user types 'quit'.",
     'why': "for-loops suit iterating a known sequence; while-loops suit condition-driven repetition."},
    {'q': "What does enumerate(['a','b'], start=1) yield on each iteration?",
     'options': ["'a', 'b'", "(1,'a') then (2,'b')", "(0,'a') then (1,'b')", "1, 2"],
     'answer': "B) (1,'a') then (2,'b')",
     'why': "enumerate pairs each item with an index, beginning at the given start."},
    {'q': "What causes an infinite while-loop?",
     'answer': "The loop's condition never becomes false because nothing inside the loop changes it.",
     'why': "Always update the variable the condition depends on."},
    {'q': "What does this print:  for n in range(4):\\n    if n==2: continue\\n    print(n)",
     'options': ["0 1 2 3", "0 1 3", "0 1", "1 2 3"],
     'answer': "B) 0 1 3",
     'why': "continue skips the print only when n is 2, so 2 is omitted."},
], title="Quiz - Topic 5")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 6: Functions & modules
# ---------------------------------------------------------------------------
h1(doc, "6. Functions & modules")

para(doc,
     "A function is a named, reusable block of code that takes inputs (parameters), does work, and "
     "usually returns a result. Functions are how you avoid repetition and break a big problem into "
     "small, testable pieces - the single most important habit for writing maintainable code. You define "
     "one with def, list parameters in parentheses, and use return to hand a value back to the caller. A "
     "function with no return statement returns None.")

para(doc,
     "Parameters can have default values (def greet(name='friend')), and callers can pass arguments by "
     "position or by keyword (greet(name='Dami')). *args collects extra positional arguments into a tuple "
     "and **kwargs collects extra keyword arguments into a dict - you will see these constantly in "
     "libraries. Variables created inside a function are local: they exist only during the call and do "
     "not leak out (this is 'scope'). Always write a docstring - a triple-quoted string just under the "
     "def - to explain what the function does; tools and teammates rely on it.")

para(doc,
     "A module is just a .py file. When your code grows, you split it into modules and import what you "
     "need: import math then math.sqrt(9), or from math import sqrt. Python ships with a large standard "
     "library (math, random, datetime, json, os, and more) so you rarely start from zero. The common "
     "guard if __name__ == '__main__': lets a file act as both an importable module and a runnable "
     "script - code under it runs only when the file is executed directly, not when imported.")

code_block(doc,
'''def average(numbers):
    """Return the arithmetic mean of a non-empty list of numbers."""
    return sum(numbers) / len(numbers)

print(average([70, 80, 90]))     # 80.0

# default parameters + keyword arguments
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Dami"))                       # Hello, Dami!
print(greet("Dami", greeting="Welcome"))   # Welcome, Dami!

# *args and **kwargs
def describe(*args, **kwargs):
    print("positional:", args)     # a tuple
    print("keyword:", kwargs)      # a dict

describe(1, 2, role="student", year=1)

# using the standard library (modules)
import random
from math import sqrt
print(sqrt(144))                   # 12.0
print(random.choice(["A", "B", "C"]))   # a random pick

# the main guard
def main():
    print("This runs only when the file is executed directly.")

if __name__ == "__main__":
    main()
''')

callout(doc, "Common mistakes",
        "Forgetting to return a value (the function then returns None and your caller gets nothing). "
        "Confusing printing with returning - print() shows text but does not give the value back for "
        "reuse. Using a mutable default argument like def f(items=[]) - the SAME list is shared across "
        "calls; use None and create a fresh list inside. Defining a variable inside a function and "
        "expecting to use it outside (scope). Naming your file the same as a standard module (e.g. "
        "random.py) so your import breaks.")

quiz(doc, [
    {'q': "What does a function return if it has no return statement?",
     'options': ["0", "An empty string", "None", "An error"],
     'answer': "C) None",
     'why': "Functions without an explicit return implicitly return None."},
    {'q': "What is the difference between printing a value and returning it?",
     'answer': "print() displays text on screen; return hands the value back to the caller so it can be stored or reused.",
     'why': "You cannot do total = print(x); print returns None. Use return for data flow."},
    {'q': "Why is def add(items=[]) a dangerous default?",
     'answer': "The same list object is reused across every call, so data accumulates unexpectedly. Use items=None and create a new list inside.",
     'why': "Default arguments are evaluated once at definition time, not per call."},
    {'q': "What does **kwargs collect inside a function?",
     'options': ["Extra positional args as a tuple", "Extra keyword args as a dict",
                 "All args as a list", "Nothing"],
     'answer': "B) Extra keyword args as a dict",
     'why': "*args gathers extra positional args (tuple); **kwargs gathers extra keyword args (dict)."},
    {'q': "What does if __name__ == '__main__': achieve?",
     'answer': "Code under it runs only when the file is executed directly, not when the file is imported as a module.",
     'why': "This lets a file be both a reusable module and a runnable script."},
    {'q': "Write a one-line function header (def ...) for a function 'square' taking one parameter n.",
     'answer': "def square(n):",
     'why': "def, the name, parentheses with the parameter, and a colon."},
], title="Quiz - Topic 6")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 7: Object-oriented programming
# ---------------------------------------------------------------------------
h1(doc, "7. Object-oriented programming (classes, __init__, inheritance)")

para(doc,
     "Object-oriented programming (OOP) lets you bundle data and the behaviour that acts on it into a "
     "single unit called an object. A class is the blueprint; an object (or instance) is a concrete thing "
     "built from that blueprint. If a dictionary is a loose bag of related values, a class is a strict, "
     "named template that also carries methods - functions that belong to the object. This matters in AI "
     "work because libraries like scikit-learn and PyTorch are deeply object-oriented: you create a model "
     "object and call model.fit(...) and model.predict(...).")

para(doc,
     "The special method __init__ is the initialiser (constructor): Python calls it automatically when "
     "you create an instance, and it sets up the object's initial attributes. The first parameter of "
     "every method is self, which refers to the particular instance the method is called on - it is how "
     "an object reads and writes its own data. Attributes are the variables stored on self; methods are "
     "functions defined inside the class. Another useful special method, __repr__, defines how the object "
     "prints, which makes debugging far easier.")

para(doc,
     "Inheritance lets one class build on another. A subclass (child) inherits the attributes and methods "
     "of its parent and can add new ones or override existing ones. You call the parent's initialiser with "
     "super().__init__(...). This models 'is-a' relationships: a Student is a Person, so Student(Person) "
     "reuses Person's code and extends it. Inheritance done well removes duplication; overused, it tangles "
     "code - prefer it only for genuine is-a relationships.")

code_block(doc,
'''class Person:
    def __init__(self, name, age):
        self.name = name          # attribute stored on the instance
        self.age = age

    def greet(self):              # a method; self is the instance
        return f"Hi, I'm {self.name}, aged {self.age}."

    def __repr__(self):           # how the object prints
        return f"Person({self.name!r}, {self.age})"

p = Person("Dami", 27)
print(p.greet())                  # Hi, I'm Dami, aged 27.
print(p)                          # Person('Dami', 27)

# Inheritance: Student IS A Person
class Student(Person):
    def __init__(self, name, age, course):
        super().__init__(name, age)   # reuse Person's setup
        self.course = course

    def greet(self):                  # override the parent's method
        base = super().greet()
        return f"{base} I study {self.course}."

s = Student("Ada", 22, "AI")
print(s.greet())                  # Hi, I'm Ada, aged 22. I study AI.
print(isinstance(s, Person))      # True - a Student is a Person
''')

callout(doc, "Common mistakes",
        "Forgetting self as the first parameter of a method, or forgetting to write self.x to store an "
        "attribute. Confusing the class (blueprint) with an instance (a built object). Forgetting to call "
        "super().__init__() in a subclass, so parent attributes never get set. Defining attributes at "
        "class level and being surprised they are shared by all instances. Reaching for inheritance when "
        "the relationship is not really 'is-a'.")

quiz(doc, [
    {'q': "What is the difference between a class and an instance?",
     'answer': "A class is the blueprint/template; an instance (object) is a concrete thing created from that class.",
     'why': "One class can produce many independent instances."},
    {'q': "What does the __init__ method do?",
     'options': ["Deletes the object", "Initialises a new instance's attributes",
                 "Prints the object", "Imports modules"],
     'answer': "B) Initialises a new instance's attributes",
     'why': "__init__ is the constructor, run automatically when you create an instance."},
    {'q': "What does the parameter 'self' refer to inside a method?",
     'answer': "The particular instance the method is being called on, used to access that object's own attributes and methods.",
     'why': "self distinguishes one instance's data from another's."},
    {'q': "How do you call a parent class's initialiser from a subclass?",
     'options': ["parent.init()", "super().__init__(...)", "Person.new()", "self.__init__()"],
     'answer': "B) super().__init__(...)",
     'why': "super() gives access to the parent class so you can reuse its setup."},
    {'q': "If Student(Person), what does isinstance(student_obj, Person) return?",
     'options': ["True", "False", "Error", "None"],
     'answer': "A) True",
     'why': "A subclass instance is also an instance of its parent class."},
    {'q': "What is the purpose of defining __repr__?",
     'answer': "It controls how the object is displayed when printed or inspected, which aids debugging.",
     'why': "Without it, you see an unhelpful default like <Person object at 0x...>."},
], title="Quiz - Topic 7")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 8: Files & JSON
# ---------------------------------------------------------------------------
h1(doc, "8. Files & JSON")

para(doc,
     "Programs need to remember data between runs, and the simplest way is to read and write files. "
     "Python opens a file with open(path, mode). Common modes are 'r' (read), 'w' (write, which "
     "overwrites), and 'a' (append). Always open files using a 'with' block: with open(...) as f - this "
     "context manager guarantees the file is closed properly even if an error occurs, which prevents data "
     "loss and resource leaks. Text files deal in str; you read with f.read() or iterate line by line, and "
     "write with f.write(). Add encoding='utf-8' to handle any characters reliably across systems.")

para(doc,
     "JSON (JavaScript Object Notation) is the universal text format for structured data, used by almost "
     "every web API. It maps cleanly onto Python types: a JSON object becomes a dict, an array becomes a "
     "list, and strings/numbers/true/false/null become str/int or float/bool/None. The json module gives "
     "you four key functions. json.dumps(obj) serialises a Python object to a JSON string and json.loads(s) "
     "parses a JSON string back into Python objects. The file variants json.dump(obj, f) and json.load(f) "
     "do the same straight to and from an open file. This is exactly how the project will save your to-do "
     "list and read the API's weather response.")

code_block(doc,
'''import json

# --- writing and reading a TEXT file (note the 'with' block) ---
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("line one\\n")
    f.write("line two\\n")

with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:                  # iterate line by line
        print(line.strip())

# --- JSON <-> Python ---
todo = {"tasks": ["learn loops", "build project"], "done": 0}

# Python object -> JSON string
text = json.dumps(todo, indent=2)
print(text)

# JSON string -> Python object
back = json.loads(text)
print(back["tasks"][0])             # learn loops

# Save / load straight to a file
with open("todo.json", "w", encoding="utf-8") as f:
    json.dump(todo, f, indent=2)

with open("todo.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["done"])               # 0
''')

callout(doc, "Common mistakes",
        "Opening with 'w' when you meant 'a' - 'w' wipes the file. Forgetting the 'with' block and "
        "leaving files open. Confusing json.dumps/loads (work with strings) with json.dump/load (work "
        "with file objects) - the 's' stands for string. Forgetting that JSON keys are always strings. "
        "Trying to json.dump a non-serialisable object (e.g. a set or a custom class) without converting "
        "it first. Omitting encoding='utf-8' and hitting odd character errors.")

quiz(doc, [
    {'q': "Which file mode OVERWRITES the file if it already exists?",
     'options': ["'r'", "'a'", "'w'", "'x'"],
     'answer': "C) 'w'",
     'why': "'w' truncates/overwrites; 'a' appends; 'r' only reads."},
    {'q': "Why should you open files using a 'with' block?",
     'answer': "The context manager automatically closes the file even if an error occurs, preventing leaks and data loss.",
     'why': "It removes the need to remember f.close()."},
    {'q': "What is the difference between json.dumps and json.dump?",
     'answer': "dumps returns a JSON string; dump writes JSON directly to an open file object. The 's' = string.",
     'why': "Same pairing for loads (from string) vs load (from file)."},
    {'q': "A JSON object parsed by json.loads becomes which Python type?",
     'options': ["list", "tuple", "dict", "set"],
     'answer': "C) dict",
     'why': "JSON objects map to Python dicts; JSON arrays map to lists."},
    {'q': "JSON keys must always be of what type?",
     'answer': "Strings.",
     'why': "Even numeric-looking keys are strings in JSON."},
    {'q': "What does json.loads('[1, 2, 3]') return in Python?",
     'options': ["'[1, 2, 3]'", "[1, 2, 3]", "(1, 2, 3)", "{1, 2, 3}"],
     'answer': "B) [1, 2, 3]",
     'why': "A JSON array deserialises into a Python list."},
], title="Quiz - Topic 8")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 9: Errors & exception handling
# ---------------------------------------------------------------------------
h1(doc, "9. Errors & exception handling")

para(doc,
     "Errors are normal. There are two broad kinds. Syntax errors mean Python cannot even parse your "
     "code (a missing colon or bracket) and nothing runs until you fix them. Exceptions happen at run "
     "time when something goes wrong during execution - dividing by zero (ZeroDivisionError), accessing a "
     "missing dict key (KeyError), converting bad text to a number (ValueError), or calling a method that "
     "does not exist (AttributeError). When an exception is raised and nothing handles it, the program "
     "stops and prints a traceback - read tracebacks from the bottom up: the last line names the error.")

para(doc,
     "You handle exceptions with try/except. Put the risky code in try; if an exception of the type you "
     "name in except occurs, control jumps there instead of crashing. Catch specific exceptions, not a "
     "bare 'except:', so you do not accidentally hide bugs. An optional else runs if no exception occurred, "
     "and finally always runs (used for cleanup). You can also raise your own exceptions with raise to "
     "signal that a caller misused your function. Good error handling makes the difference between a "
     "program that crashes on the first odd input and one a real user can trust - your dashboard project "
     "must not die just because the network blips.")

code_block(doc,
'''# A traceback you would see if unhandled:
# Traceback (most recent call last):
#   File "x.py", line 1, in <module>
#     int("not a number")
# ValueError: invalid literal for int() with base 10: 'not a number'

# try / except - catch a SPECIFIC error
def parse_age(text):
    try:
        age = int(text)
    except ValueError:
        print(f"'{text}' is not a whole number; using 0.")
        age = 0
    return age

print(parse_age("27"))     # 27
print(parse_age("oops"))   # message, then 0

# multiple excepts + else + finally
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero.")
        return None
    else:
        print("Division succeeded.")   # runs only if no error
        return result
    finally:
        print("done attempting division.")  # always runs

safe_divide(10, 2)
safe_divide(10, 0)

# raising your own exception
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    return balance - amount
''')

callout(doc, "Common mistakes",
        "Using a bare 'except:' that swallows every error (including Ctrl+C and real bugs) - always catch "
        "specific types. Putting too much code inside one try block so you cannot tell what failed. "
        "Catching an exception and silently doing nothing ('pass'), hiding the problem. Reading a "
        "traceback top-down instead of bottom-up. Confusing a syntax error (won't run at all) with a "
        "runtime exception (runs until it hits the bad line).")

quiz(doc, [
    {'q': "What is the difference between a syntax error and an exception?",
     'answer': "A syntax error stops the code from running at all; an exception occurs at run time during execution and can be caught.",
     'why': "Syntax errors are detected before execution; exceptions are raised while the program runs."},
    {'q': "Which error is raised by int('abc')?",
     'options': ["KeyError", "ValueError", "TypeError", "ZeroDivisionError"],
     'answer': "B) ValueError",
     'why': "'abc' is the wrong value for int conversion, so ValueError is raised."},
    {'q': "Why should you avoid a bare 'except:' clause?",
     'answer': "It catches every exception, including ones you did not anticipate and even keyboard interrupts, hiding real bugs.",
     'why': "Catch specific exception types so genuine problems still surface."},
    {'q': "Which block always runs whether or not an exception occurred?",
     'options': ["try", "except", "else", "finally"],
     'answer': "D) finally",
     'why': "finally runs regardless - it is used for cleanup."},
    {'q': "You read a traceback in which direction to find the actual error?",
     'answer': "Bottom up - the last line names the exception type and message.",
     'why': "The lines above show the call chain leading to it."},
    {'q': "How do you deliberately signal an error from your own function?",
     'options': ["throw", "raise", "error", "panic"],
     'answer': "B) raise",
     'why': "Python uses the raise keyword, e.g. raise ValueError('...')."},
], title="Quiz - Topic 9")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 10: Virtual environments & pip
# ---------------------------------------------------------------------------
h1(doc, "10. Virtual environments & pip")

para(doc,
     "Real projects depend on third-party packages, and different projects often need different - "
     "sometimes conflicting - versions of the same package. If you install everything globally, project A "
     "upgrading a library can silently break project B. A virtual environment solves this: it is an "
     "isolated, per-project copy of Python with its own packages folder. Activate it and 'pip install' "
     "puts packages only there; deactivate and your system Python is untouched. Every professional Python "
     "project uses one - it is not optional.")

para(doc,
     "Python ships with the venv module. You create an environment once per project, activate it whenever "
     "you work, and install dependencies into it. pip is Python's package installer; it downloads packages "
     "from PyPI, the Python Package Index. The convention is to record your project's dependencies in a "
     "requirements.txt file (pip freeze > requirements.txt) so anyone - including future you - can "
     "recreate the exact environment with pip install -r requirements.txt. Always add the environment "
     "folder (e.g. .venv/) to your .gitignore; you commit requirements.txt, never the installed packages.")

code_block(doc,
'''# These are TERMINAL commands, not Python code.

# 1) create a virtual environment named .venv (do this once per project)
python -m venv .venv

# 2) activate it
#    Windows (PowerShell):
.venv\\Scripts\\Activate.ps1
#    macOS / Linux:
source .venv/bin/activate
# your prompt now shows (.venv)

# 3) install packages INTO the environment
pip install requests

# 4) see what is installed / freeze it for sharing
pip list
pip freeze > requirements.txt

# 5) on another machine, recreate everything:
pip install -r requirements.txt

# 6) leave the environment when done
deactivate
''')

callout(doc, "Common mistakes",
        "Forgetting to activate the environment, then wondering why 'import requests' fails (you installed "
        "into the wrong Python). Committing the .venv folder to Git instead of requirements.txt - add "
        ".venv/ to .gitignore. Mixing 'pip' from one Python with 'python' from another; use 'python -m pip "
        "install ...' to be sure they match. Installing packages globally and creating version conflicts. "
        "Forgetting to re-run pip freeze after adding a new dependency.")

quiz(doc, [
    {'q': "What problem does a virtual environment solve?",
     'answer': "It isolates each project's packages so different projects can use different/conflicting versions without breaking each other or the system Python.",
     'why': "Global installs cause cross-project version conflicts."},
    {'q': "Which command creates a virtual environment called .venv?",
     'options': ["pip new .venv", "python -m venv .venv", "venv create .venv", "python venv .venv"],
     'answer': "B) python -m venv .venv",
     'why': "venv is a standard-library module run with python -m venv <folder>."},
    {'q': "What is PyPI?",
     'answer': "The Python Package Index - the public repository pip downloads packages from.",
     'why': "pip install fetches packages from PyPI by default."},
    {'q': "Which file records your project's dependencies for others to reinstall?",
     'options': ["packages.json", "requirements.txt", "setup.cfg", "deps.lock"],
     'answer': "B) requirements.txt",
     'why': "Created with pip freeze > requirements.txt and reused with pip install -r requirements.txt."},
    {'q': "Should you commit the .venv folder to Git? Why or why not?",
     'answer': "No - it is large and machine-specific. Commit requirements.txt instead and add .venv/ to .gitignore.",
     'why': "The environment can be recreated from requirements.txt."},
    {'q': "Your 'import requests' fails right after pip install succeeded. What is the most likely cause?",
     'answer': "You did not activate the virtual environment (or installed into a different Python than you are running).",
     'why': "Activation ensures pip and python refer to the same isolated environment."},
], title="Quiz - Topic 10")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 11: Git & GitHub fundamentals
# ---------------------------------------------------------------------------
h1(doc, "11. Git & GitHub fundamentals")

para(doc,
     "Git is a version control system: it records snapshots of your project over time so you can see what "
     "changed, undo mistakes, and collaborate without overwriting each other's work. It is the single most "
     "important professional tool after the language itself - every engineering job assumes you know it. "
     "GitHub is a website that hosts Git repositories online; Git is the tool, GitHub is one place to store "
     "and share repositories. Do not conflate them.")

para(doc,
     "Git has three areas. The working directory is your actual files. The staging area (index) is where "
     "you assemble the next snapshot with git add. A commit permanently records the staged snapshot with "
     "a message, via git commit. So the everyday cycle is: edit files, git add the changes you want, git "
     "commit them with a clear message, and git push to upload to GitHub. git status shows where things "
     "stand and git log shows history. A .gitignore file lists paths Git should never track - things like "
     ".venv/, secret keys, and __pycache__/.")

para(doc,
     "Branches let you work on a feature without disturbing the main line; you create a branch, commit on "
     "it, then merge it back (often through a Pull Request on GitHub, where changes can be reviewed before "
     "joining main). For this course you will follow a dev -> test -> approve -> main flow: do your work, "
     "commit clear messages, push, and only merge to your main branch once it works. Write commit messages "
     "in the imperative mood ('Add weather fetcher', not 'added stuff') and commit small, logical chunks "
     "rather than one giant dump.")

code_block(doc,
'''# TERMINAL commands.

# one-time identity setup
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"

# start tracking a project
git init                      # create a repo in the current folder
git status                    # what is changed/untracked?

# the core cycle
git add dashboard.py          # stage one file (or: git add .  for all)
git commit -m "Add weather fetcher"   # record a snapshot

# connect to GitHub and upload (create the empty repo on GitHub first)
git remote add origin https://github.com/you/personal-dashboard.git
git branch -M main
git push -u origin main       # push and set upstream

# day-to-day after that
git pull                      # get others' changes first
git add .
git commit -m "Persist todos to SQLite"
git push

# branching for a new feature
git switch -c add-quotes      # create + switch to a branch
# ...edit, add, commit...
git push -u origin add-quotes # then open a Pull Request on GitHub
''')

callout(doc, "Common mistakes",
        "Committing secrets (API keys, passwords) or the .venv folder - use .gitignore and environment "
        "variables. Vague commit messages like 'fix' or 'stuff'. Forgetting to git add before commit, so "
        "your change is not actually saved in the snapshot. Confusing Git (the tool) with GitHub (the "
        "host). Pushing directly to main without testing. Never running git status/git log, so you lose "
        "track of state. Committing huge unrelated changes in one commit.")

quiz(doc, [
    {'q': "What is the difference between Git and GitHub?",
     'answer': "Git is the version-control tool that runs locally; GitHub is a website that hosts Git repositories online.",
     'why': "You can use Git with no GitHub at all; GitHub is one hosting option."},
    {'q': "Put the core cycle in order: commit, add, edit.",
     'answer': "edit -> add (stage) -> commit (record snapshot).",
     'why': "git add stages changes; git commit records the staged snapshot."},
    {'q': "What does the staging area (index) hold?",
     'options': ["The remote copy", "Changes assembled for the next commit",
                 "Deleted files only", "Your commit history"],
     'answer': "B) Changes assembled for the next commit",
     'why': "git add moves changes into staging; git commit turns staged changes into a snapshot."},
    {'q': "What belongs in a .gitignore file?",
     'answer': "Paths Git should not track, such as .venv/, __pycache__/, secret keys, and large generated files.",
     'why': "It keeps secrets and machine-specific clutter out of the repository."},
    {'q': "Which command uploads your committed local changes to GitHub?",
     'options': ["git add", "git commit", "git push", "git status"],
     'answer': "C) git push",
     'why': "push sends commits from your local repo to the remote (origin)."},
    {'q': "Why are branches useful?",
     'answer': "They let you develop a feature in isolation without disturbing the main line, then merge it back when ready (often via a Pull Request).",
     'why': "This keeps main stable and enables review before merging."},
    {'q': "Good commit messages are written in which mood, with an example?",
     'answer': "Imperative mood, e.g. 'Add weather fetcher' rather than 'added stuff'.",
     'why': "Imperative messages read as instructions and match Git's own conventions."},
], title="Quiz - Topic 11")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 12: Intro to APIs with requests
# ---------------------------------------------------------------------------
h1(doc, "12. Intro to APIs with the requests library")

para(doc,
     "An API (Application Programming Interface) is a defined way for one program to ask another program "
     "for data or actions. A web API is reached over HTTP: your code sends a request to a URL (an "
     "endpoint) and the server sends back a response, almost always as JSON. This is how your dashboard "
     "will get live weather. The most common HTTP methods are GET (fetch data) and POST (send data). "
     "Every response carries a status code: 200 means OK, 404 means not found, 401 means unauthorised "
     "(usually a bad or missing API key), and 500 means a server error. Always check the status code "
     "before trusting the body.")

para(doc,
     "requests is the de-facto Python library for HTTP - clean and beginner-friendly. You call "
     "requests.get(url, params=...) where params is a dict of query-string values (the library encodes "
     "them onto the URL for you). The returned response object exposes resp.status_code, resp.text (raw "
     "text), and resp.json() (parsed into Python dict/list). Many APIs need an API key for authentication "
     "- you sign up, receive a key, and pass it as a parameter or header. Critically, never hard-code a "
     "key in your committed code; read it from an environment variable so it stays out of Git. Wrap "
     "network calls in try/except because networks fail.")

code_block(doc,
'''import requests   # pip install requests first (inside your venv)

def get_weather(city, api_key):
    """Return (temp_c, description) for a city, or None on failure."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()          # raise if status is 4xx/5xx
    except requests.RequestException as e:
        print("Network/API error:", e)
        return None

    data = resp.json()                   # parse JSON -> Python dict
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return temp, desc

# Read the key from the environment - never hard-code secrets.
import os
key = os.environ.get("OWM_API_KEY", "")
result = get_weather("London", key)
if result:
    temp, desc = result
    print(f"London: {temp} C, {desc}")
''')

para(doc,
     "Two reliable APIs that need NO key are great for first experiments: an open quotes API and the "
     "free Open-Meteo weather API. Start with a keyless API to prove the request/response loop works, "
     "then graduate to one that needs a key.")

callout(doc, "Common mistakes",
        "Hard-coding an API key in code that you then push to GitHub (rotate it immediately if you do). "
        "Not checking resp.status_code / not calling raise_for_status(), then crashing on an error body. "
        "Calling resp.json() on a non-JSON or error response. Building the query string by hand instead "
        "of passing params=. Forgetting a timeout so the program hangs forever. Not wrapping the call in "
        "try/except for network failures.")

quiz(doc, [
    {'q': "What does an HTTP status code of 200 mean?",
     'options': ["Not found", "OK / success", "Unauthorised", "Server error"],
     'answer': "B) OK / success",
     'why': "200 means the request succeeded; 404 not found, 401 unauthorised, 500 server error."},
    {'q': "Which requests method fetches data from an endpoint?",
     'options': ["requests.post", "requests.get", "requests.send", "requests.fetch"],
     'answer': "B) requests.get",
     'why': "GET retrieves data; POST sends data to the server."},
    {'q': "What does resp.json() return?",
     'answer': "The response body parsed from JSON into Python objects (typically a dict or list).",
     'why': "It saves you calling json.loads(resp.text) yourself."},
    {'q': "Why should an API key be read from an environment variable instead of written in code?",
     'answer': "So the secret is never committed to Git/GitHub where others could see and abuse it.",
     'why': "Hard-coded secrets in a public repo are a common, serious security mistake."},
    {'q': "What is the purpose of passing params={...} to requests.get?",
     'answer': "requests encodes the dict into the URL query string for you, correctly and safely.",
     'why': "Manual string-building is error-prone (encoding, escaping)."},
    {'q': "A 401 status usually indicates what?",
     'options': ["The server crashed", "The URL is wrong", "A bad or missing API key", "Success"],
     'answer': "C) A bad or missing API key",
     'why': "401 Unauthorised typically means authentication (your key) failed."},
], title="Quiz - Topic 12")

page_break(doc)

# ---------------------------------------------------------------------------
# Topic 13: Intro to SQL with SQLite
# ---------------------------------------------------------------------------
h1(doc, "13. Intro to SQL with SQLite (sqlite3 module)")

para(doc,
     "A database stores structured data so it survives between runs and can be queried efficiently. A "
     "relational database organises data into tables of rows and columns, and SQL (Structured Query "
     "Language) is the language you use to define and query them. SQLite is a tiny, serverless relational "
     "database: the entire database is a single file on disk, with no server to install or configure. It "
     "is built right into Python through the sqlite3 module, which makes it the perfect place to learn SQL "
     "and to persist your dashboard's to-do list.")

para(doc,
     "The four core SQL operations are often called CRUD: CREATE/INSERT (add rows), SELECT (read rows), "
     "UPDATE (change rows), and DELETE (remove rows). You first CREATE TABLE to define columns and their "
     "types, then INSERT rows, SELECT them back with optional WHERE filters and ORDER BY sorting, UPDATE "
     "or DELETE by condition. In Python you connect to the file, get a cursor, execute SQL on it, and "
     "commit() to save changes. The single most important safety rule: never build SQL by gluing strings "
     "with user input - use parameter placeholders (?) and pass values as a tuple. This prevents SQL "
     "injection, a classic and dangerous bug.")

code_block(doc,
'''import sqlite3

# connect (creates the file if it does not exist)
conn = sqlite3.connect("dashboard.db")
cur = conn.cursor()

# CREATE a table (IF NOT EXISTS makes it safe to re-run)
cur.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        task  TEXT NOT NULL,
        done  INTEGER NOT NULL DEFAULT 0
    )
""")

# INSERT - ALWAYS use ? placeholders, never string formatting
cur.execute("INSERT INTO todos (task) VALUES (?)", ("Learn SQL",))
cur.execute("INSERT INTO todos (task) VALUES (?)", ("Build dashboard",))
conn.commit()                       # save the changes

# SELECT - read rows back
cur.execute("SELECT id, task, done FROM todos ORDER BY id")
for row in cur.fetchall():
    print(row)                      # (1, 'Learn SQL', 0) ...

# UPDATE - mark a task done by id
cur.execute("UPDATE todos SET done = 1 WHERE id = ?", (1,))
conn.commit()

# DELETE - remove a task
cur.execute("DELETE FROM todos WHERE id = ?", (2,))
conn.commit()

# count remaining open tasks
cur.execute("SELECT COUNT(*) FROM todos WHERE done = 0")
print("open tasks:", cur.fetchone()[0])

conn.close()                        # always close when done
''')

callout(doc, "Common mistakes",
        "Building SQL with f-strings or + and user input -> SQL injection; always use ? placeholders and "
        "a tuple of values (note the trailing comma in a one-element tuple: (\"x\",)). Forgetting "
        "conn.commit(), so your INSERT/UPDATE/DELETE is lost when the program ends. Forgetting WHERE on "
        "an UPDATE or DELETE and changing every row. Not closing the connection. Confusing fetchone() "
        "(one row) with fetchall() (all rows).")

quiz(doc, [
    {'q': "What does the acronym CRUD stand for in databases?",
     'answer': "Create, Read, Update, Delete (in SQL: INSERT, SELECT, UPDATE, DELETE).",
     'why': "These are the four fundamental data operations."},
    {'q': "Why is SQLite convenient for learning and small projects?",
     'options': ["It needs a dedicated server", "It is a single file and built into Python",
                 "It only runs on Linux", "It cannot use SQL"],
     'answer': "B) It is a single file and built into Python",
     'why': "sqlite3 is serverless, file-based, and ships with Python's standard library."},
    {'q': "Which SQL statement reads rows from a table?",
     'options': ["INSERT", "SELECT", "UPDATE", "DELETE"],
     'answer': "B) SELECT",
     'why': "SELECT retrieves rows, optionally filtered with WHERE."},
    {'q': "Why must you use ? placeholders instead of string-formatting values into SQL?",
     'answer': "To prevent SQL injection; placeholders safely escape values so malicious input cannot alter the query.",
     'why': "String-built SQL with user input is the classic injection vulnerability."},
    {'q': "What happens if you INSERT rows but never call conn.commit()?",
     'answer': "The changes are not saved and are lost when the connection closes.",
     'why': "commit() finalises the transaction to disk."},
    {'q': "What is the difference between cur.fetchone() and cur.fetchall()?",
     'answer': "fetchone() returns a single row (or None); fetchall() returns a list of all remaining rows.",
     'why': "Choose based on whether you expect one row or many."},
    {'q': "What risk comes from an UPDATE or DELETE statement with no WHERE clause?",
     'answer': "It affects every row in the table.",
     'why': "Always scope destructive statements with a WHERE condition."},
], title="Quiz - Topic 13")

page_break(doc)

# ---------------------------------------------------------------------------
# Exercises
# ---------------------------------------------------------------------------
h1(doc, "Exercises")
para(doc,
     "Do these in order; each builds the skills the project needs. Type everything by hand, run it, and "
     "commit each finished exercise to a Git repo named month1-exercises.")

numbered(doc, "Warm-up I/O: ask the user for their name and birth year with input(), then print a sentence "
              "telling them how old they turn this year. Handle non-numeric input gracefully with try/except.")
numbered(doc, "FizzBuzz: print the numbers 1 to 100, but print 'Fizz' for multiples of 3, 'Buzz' for "
              "multiples of 5, and 'FizzBuzz' for multiples of both. Use the modulo operator.")
numbered(doc, "Grade calculator: write a function grade(score) that returns 'A','B','C', or 'F' using "
              "if/elif/else, then loop over a list of scores and build a dict mapping each score to its grade.")
numbered(doc, "Word counter: read a text file, count how many times each word appears (case-insensitive) "
              "using a dictionary, and print the five most common words. Use .lower() and .split().")
numbered(doc, "Contact book class: design a Contact class (name, email, phone) with a __repr__, and an "
              "AddressBook class that stores many contacts in a list with add(), find(name), and all() methods.")
numbered(doc, "JSON note app: a command-line loop that lets the user add, list, and delete notes, persisting "
              "them to notes.json so they survive between runs. Use json.load/json.dump and handle a missing file.")
numbered(doc, "Keyless API call: using requests, fetch a random quote from a free no-key quotes API, parse "
              "the JSON, and print the quote and author. Wrap it in try/except and check the status code.")
numbered(doc, "SQLite to-do CLI: build a small command-line to-do app backed by SQLite with add, list, "
              "complete, and delete commands. Use ? placeholders and commit after every change.")

page_break(doc)

# ---------------------------------------------------------------------------
# Project brief
# ---------------------------------------------------------------------------
h1(doc, "Project brief - Command-line Personal Dashboard")

lead(doc, "Goal:",
     "Build a single command-line Python program that, when run, greets the user, fetches and displays "
     "today's weather for a chosen city from a public API, shows a random motivational quote, and lets "
     "the user manage a persistent to-do list. It ties together every Month 1 skill into one real, "
     "useful tool, and ships as a clean, documented GitHub repository.")

lead(doc, "Functional requirements:", "")
bullet(doc, "On start, print a friendly greeting that includes today's date (use the datetime module).")
bullet(doc, "Fetch current weather for a city (default city configurable) from a public API using requests; "
            "display temperature and a short description. Handle network/API errors without crashing.")
bullet(doc, "Display a random quote, either from a keyless quotes API or from a local list/JSON of quotes "
            "as a fallback when offline.")
bullet(doc, "Provide a to-do list with add, list, complete, and delete actions, persisted with SQLite "
            "(sqlite3) - or JSON if you prefer - so tasks survive between runs.")
bullet(doc, "Use a menu loop so the user can perform several actions before quitting; validate input and "
            "handle bad choices gracefully.")
bullet(doc, "Read any API key from an environment variable, never hard-coded. Organise the code into "
            "functions (and at least one class), with docstrings.")

lead(doc, "Technical requirements:", "")
bullet(doc, "Use a virtual environment; record dependencies in requirements.txt.")
bullet(doc, "Track the whole project with Git and publish to GitHub with a clear commit history.")
bullet(doc, "Include a .gitignore (ignore .venv/, __pycache__/, the .db file, and any secrets).")
bullet(doc, "Include a README.md explaining what it does, how to set up the venv, how to set the API key, "
            "and how to run it.")

lead(doc, "Milestones:", "")
numbered(doc, "Prove the API call works: a throwaway script that hits the weather (or quotes) API and "
              "prints the raw JSON. Confirm the request/response loop end-to-end.")
numbered(doc, "Parse and display: extract just the fields you need (temperature, description, quote text) "
              "and print them cleanly, with try/except around the network call.")
numbered(doc, "Persistent to-do list: create the SQLite table and implement add/list/complete/delete with "
              "? placeholders and commits; verify tasks survive restarts.")
numbered(doc, "Assemble the dashboard: combine greeting, weather, quote, and a menu loop into one program; "
              "refactor into functions and a class; move the API key to an environment variable.")
numbered(doc, "Harden and polish: handle offline mode (quote fallback, friendly weather error), validate "
              "all user input, add docstrings and comments.")
numbered(doc, "Clean, documented GitHub repo: write the README, add requirements.txt and .gitignore, make "
              "tidy commits, and push the final version to GitHub.")

lead(doc, "Grading rubric:", "")
table_from_rows(
    doc,
    ["Criterion", "Weight", "What 'excellent' looks like"],
    [
        ["Functionality", "30%", "All features work: weather, quote, and a persistent to-do list, run reliably from the menu."],
        ["Code quality & structure", "20%", "Clear functions and at least one class, sensible names, docstrings, no copy-paste repetition."],
        ["Error handling", "15%", "Network failures, bad input, and missing files are handled gracefully; the app never crashes on normal misuse."],
        ["Persistence (SQLite/JSON)", "10%", "To-do data is stored correctly with parameterised queries and survives restarts."],
        ["Git & GitHub hygiene", "15%", "Meaningful commit history, .gitignore present, no secrets or .venv committed, repo is public and clean."],
        ["Documentation (README)", "10%", "README clearly explains setup (venv, API key), usage, and features; requirements.txt included."],
    ],
)
para(doc,
     "Stretch goals (optional): cache the last weather result to show when offline; add a 'days until a "
     "goal' countdown; let the user pick the city at runtime; add simple coloured terminal output.",
     italic=True, color=GREY)

page_break(doc)

# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------
h1(doc, "Resources")
para(doc, "Free or low-cost, well-known resources. Search the names; do not trust any URL you have not verified.")

bullet(doc, "Python official documentation and the official Python Tutorial (docs.python.org) - the "
            "authoritative reference; the tutorial is surprisingly readable for beginners.")
bullet(doc, "Automate the Boring Stuff with Python by Al Sweigart - free to read online; an excellent, "
            "practical beginner book aimed at exactly your starting point.")
bullet(doc, "Real Python - high-quality tutorials on functions, OOP, virtual environments, requests, and "
            "SQLite; many articles are free.")
bullet(doc, "freeCodeCamp - free long-form Python and SQL courses on YouTube and their website, with "
            "hands-on projects.")
bullet(doc, "The Pro Git book by Scott Chacon and Ben Straub - free online; the definitive, clear guide to "
            "Git, plus GitHub's own free 'GitHub Skills' interactive courses.")
bullet(doc, "W3Schools and SQLBolt - quick, interactive references for Python syntax and for practising "
            "SQL queries in the browser.")
bullet(doc, "Requests library documentation - the official 'Requests: HTTP for Humans' docs; short and "
            "example-driven for learning web APIs.")
bullet(doc, "Exercism (Python track) and Codewars - free graded coding exercises ('katas') to drill "
            "syntax and problem-solving with feedback.")

para(doc, "")
para(doc,
     "Study tip: spend at least half your ~30 hours each week writing and running code, not just reading. "
     "Type every example, break it on purpose, read the traceback, and fix it. Commit something to GitHub "
     "every single day - small, consistent reps beat occasional marathons.",
     italic=True, color=ACCENT)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
OUT = "Month_1_Python_Foundations_Study_Pack.docx"
doc.save(OUT)
print("Saved:", OUT)
