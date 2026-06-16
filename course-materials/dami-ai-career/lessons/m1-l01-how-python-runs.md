---
title: How Python runs & your setup
month: 1
monthTitle: Python Foundations + Git
lesson: 1
summary: Understand what happens when you run Python, then install it cleanly and run your first script
  from the terminal.
objectives:
- Explain what an interpreter does when it runs your code
- Tell the difference between source code, bytecode, and the Python runtime
- Install Python and confirm the version from the terminal
- 'Run code two ways: the interactive REPL and a saved .py file'
- Use a virtual environment to keep project dependencies isolated
- Read and understand a basic traceback when something breaks
video: m1-l01-how-python-runs.mp4
quiz:
- q: What does the Python interpreter do with your source code?
  options:
  - Translates it once into a standalone .exe
  - Reads and executes it line by line at run time
  - Sends it to the GPU
  - Stores it in a database
  answer: 1
  why: 'Python is interpreted: the interpreter reads your code, compiles it to bytecode, and executes
    it when you run the program — no separate build step into a standalone binary.'
- q: Which command shows the Python version installed on your machine?
  options:
  - python --run
  - python --version
  - python --check
  - python install
  answer: 1
  why: python --version (or python -V) prints the interpreter version, which confirms Python is installed
    and on your PATH.
- q: What is the main reason to use a virtual environment per project?
  options:
  - It makes code run faster
  - It isolates each project's packages so versions don't clash
  - It is required to write any Python
  - It encrypts your code
  answer: 1
  why: A virtual environment keeps each project's dependencies separate, so installing a package for one
    project never breaks another.
- q: Name the file extension used for a saved Python script.
  answer: .py
  why: Python source files end in .py, and you run them with python yourfile.py.
- q: In one sentence, what is the REPL and when would you use it?
  answer: The REPL is the interactive Python prompt where you type one line and see the result instantly;
    use it to experiment and test small ideas.
  why: REPL stands for Read-Eval-Print Loop — perfect for quick checks, but real programs live in saved
    .py files.
- q: When a program crashes, what does the traceback's last line usually tell you?
  answer: The type of error and a short message, such as NameError or ZeroDivisionError, describing what
    went wrong.
  why: 'Read tracebacks from the bottom up: the final line names the error and reason, and the lines above
    show where it happened.'
resources:
- label: Python.org — Download the latest Python
  url: https://www.python.org/downloads/
- label: 'Python docs — The Python Tutorial: Using the Interpreter'
  url: https://docs.python.org/3/tutorial/interpreter.html
- label: 'Python docs — venv: Creating virtual environments'
  url: https://docs.python.org/3/library/venv.html
- label: 'Real Python — Python Virtual Environments: A Primer'
  url: https://realpython.com/python-virtual-environments-a-primer/
---

## What actually happens when you "run" Python

When you run a program, your code has to become instructions the computer can execute. With some languages you **compile** the whole program ahead of time into a standalone file. Python is different: it is **interpreted**. The Python **interpreter** reads your source code, quietly compiles it to an intermediate form called **bytecode**, and then executes that bytecode line by line.

The practical upshot: there is no separate build step. You write a file, you run it, you see the result. That fast feedback loop is one reason Python is so beginner-friendly.

## Source code, bytecode, and the runtime

Think of three layers. Your **source code** is the `.py` text file you write. The interpreter turns it into **bytecode** (you may notice a `__pycache__` folder appear). The **Python runtime** — often called CPython — is the program that actually runs that bytecode on your operating system.

You never write bytecode by hand. Knowing it exists just helps the whole thing stop feeling like magic.

## Installing Python and checking it works

Download the latest Python from python.org and install it. The single most important check is that your terminal can find it.

```bash
python --version
# Python 3.12.4
```

If that prints a version number, Python is installed and on your **PATH**. On some systems you type `python3` instead of `python`.

## Two ways to run code

The first way is the **REPL** — the interactive prompt. Type `python`, and you get a `>>>` prompt where each line runs instantly. Great for experiments.

```python
>>> 2 + 2
4
>>> print("Hello")
Hello
```

The second way is a **saved script**. Put your code in a file and run the file. This is how real programs are written.

```bash
# hello.py contains:  print("Hello, world!")
python hello.py
# Hello, world!
```

## Virtual environments: one clean box per project

Different projects often need different package versions. A **virtual environment** is an isolated copy of Python for a single project, so installing something for one project never breaks another.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

Once activated, anything you install with `pip` lives only inside that project. Get into the habit now — every serious project you build will use one.

## Reading errors without panic

When code breaks, Python prints a **traceback**. Read it from the **bottom up**: the last line names the error type and message. Errors are normal and they are information, not failure.

## Your task

Install Python, confirm the version in your terminal, create a virtual environment, then write and run a `hello.py` file that prints your name.
