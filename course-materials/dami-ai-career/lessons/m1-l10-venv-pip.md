---
course: dami-ai-career
title: Virtual environments & pip
month: 1
monthTitle: Python Foundations + Git
lesson: 10
summary: Create isolated Python environments and install packages with pip so each project keeps its own
  dependencies without conflicts.
objectives:
- Explain why each project needs its own isolated environment
- Create a virtual environment with the venv module
- Activate and deactivate an environment on Windows, macOS, and Linux
- Install, upgrade, and remove packages with pip
- Pin dependencies in a requirements.txt file and reinstall from it
- Avoid committing your venv folder to Git with .gitignore
video: m1-l10-venv-pip.mp4
quiz:
- q: Why use a virtual environment for each project?
  options:
  - To make Python run faster
  - To isolate each project's packages and versions
  - To compress your code
  - To replace Git
  answer: 1
  why: A virtual environment keeps each project's dependencies separate, so different versions never clash.
- q: Which command creates a new virtual environment in a folder called venv?
  options:
  - pip install venv
  - python -m venv venv
  - python venv new
  - venv create venv
  answer: 1
  why: python -m venv venv runs the built-in venv module and creates the environment in a folder named
    venv.
- q: What does pip freeze do?
  options:
  - Stops pip from running
  - Lists installed packages with exact versions
  - Deletes all packages
  - Updates Python itself
  answer: 1
  why: pip freeze prints every installed package and its exact version, which you redirect into requirements.txt.
- q: Write the pip command that installs every package listed in requirements.txt.
  answer: pip install -r requirements.txt
  why: The -r flag tells pip to read a requirements file and install each pinned package from it.
- q: After activating a venv, what command leaves it and returns to the system Python?
  answer: deactivate
  why: Typing deactivate exits the active environment in any shell, restoring your normal Python.
- q: True or false — you should commit your venv folder to Git so teammates get the same packages.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. The venv is large and machine-specific; share requirements.txt instead and add venv to .gitignore.
resources:
- label: 'Python docs — venv: Creation of virtual environments'
  url: https://docs.python.org/3/library/venv.html
- label: pip documentation — User Guide
  url: https://pip.pypa.io/en/stable/user_guide/
- label: Python Packaging — Installing packages with pip and venv
  url: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- label: 'Real Python — Python Virtual Environments: A Primer'
  url: https://realpython.com/python-virtual-environments-a-primer/
---

## The dependency problem

Real projects rely on **third-party packages** — code other people wrote, like `numpy` or `pandas`. The trouble is versions. Project A might need `pandas` version 1, while Project B needs version 2. If you install everything into one global Python, those versions fight, and upgrading for one project silently breaks another.

As a maths graduate think of it like keeping each experiment's variables separate so results don't contaminate each other.

## What a virtual environment is

A **virtual environment** (venv) is a private copy of Python with its own package folder, living inside your project. Packages you install there stay there. Python ships with a `venv` module, so you need nothing extra.

```bash
cd my_project
python -m venv venv
```

This creates a `venv` folder. It is *not* your code — never commit it to Git.

## Activating and deactivating

You must **activate** the environment so your terminal uses its Python. The command differs by operating system.

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

# leave the environment
deactivate
```

Once active, your prompt shows `(venv)`. Now `python` and `pip` point inside the environment.

## Installing packages with pip

`pip` is Python's package installer. With the venv active, anything you install lands inside it.

```bash
pip install pandas
pip install numpy==1.26.4   # a specific version
pip list                    # see what's installed
pip uninstall pandas
```

## Sharing with requirements.txt

To let a teammate (or future you) recreate the exact setup, freeze your packages into a file and commit *that* file.

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

Add a `.gitignore` line containing `venv/` so the heavy environment folder is never committed.

## Your task

Create a fresh project folder, make a venv, activate it, install `requests`, and save a `requirements.txt`.
