---
title: Files & JSON
month: 1
monthTitle: Python Foundations + Git
lesson: 8
summary: Read and write text files safely, then load and save structured data with JSON — the format that
  powers APIs and AI tools.
objectives:
- Open, read, and write text files using Python
- Use the with statement so files always close safely
- 'Choose the right file mode: read, write, and append'
- Understand what JSON is and why it powers APIs
- Convert between Python objects and JSON strings
- Load JSON from a file and save Python data back to JSON
video: m1-l08-files-json.mp4
quiz:
- q: What does the with statement give you when opening a file?
  options:
  - Faster reading
  - It closes the file automatically when the block ends
  - It encrypts the file
  - It converts the file to JSON
  answer: 1
  why: 'with open(...) as f: guarantees the file is closed even if an error happens, so you never leak
    open file handles.'
- q: Which file mode overwrites an existing file from scratch?
  options:
  - '"r"'
  - '"a"'
  - '"w"'
  - '"x"'
  answer: 2
  why: '"w" (write) truncates the file to empty before writing. "a" appends to the end; "r" only reads.'
- q: Which Python function turns a Python object into a JSON string?
  options:
  - json.load
  - json.dumps
  - json.parse
  - json.read
  answer: 1
  why: json.dumps serialises (dumps) an object to a string. json.loads does the reverse. The s stands
    for string.
- q: What Python type does a JSON object become when you load it?
  answer: A dictionary (dict)
  why: A JSON object with key/value pairs maps directly to a Python dict; a JSON array becomes a list.
- q: Why must you specify encoding="utf-8" when opening files?
  answer: So accented and non-English characters are read and written correctly across systems.
  why: Without an explicit encoding Python uses the OS default, which can corrupt characters like é or
    — on Windows.
- q: What is the difference between json.dumps and json.dump?
  answer: dumps returns a JSON string; dump writes JSON straight to an open file.
  why: Same for load (reads from a file) versus loads (parses a string). The s means string.
resources:
- label: Python docs — Reading and Writing Files (tutorial 7.2)
  url: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
- label: Python docs — json module
  url: https://docs.python.org/3/library/json.html
- label: Real Python — Working With JSON Data in Python
  url: https://realpython.com/python-json/
- label: 'Python Crash Course (Eric Matthes) — Chapter 10: Files and Exceptions'
---

## Why files and JSON matter

So far your programs forget everything when they stop. **Files** let your data survive — you save results, read inputs, and keep logs. And **JSON** is the standard way to store and exchange *structured* data: nearly every web API, config file, and AI tool speaks JSON.

As a maths graduate moving toward AI work, you'll meet JSON constantly — it's how you'll send prompts to models and read their replies.

## Reading and writing text files

Use `open()` with a **mode**, and always wrap it in a `with` block so the file closes automatically — even if something goes wrong.

```python
# Write a file (overwrites it)
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Hello, file!\n")
    f.write("Second line.\n")

# Read it back
with open("notes.txt", "r", encoding="utf-8") as f:
    text = f.read()
print(text)
```

## File modes

The mode string controls what you can do:

- `"r"` — read (the default); errors if the file is missing.
- `"w"` — write; **erases** the file first.
- `"a"` — append; adds to the end, keeping what's there.

Always pass `encoding="utf-8"` so accented characters never get mangled.

## What is JSON?

**JSON** (JavaScript Object Notation) is plain text that looks a lot like a Python dictionary: keys in quotes, values, and square brackets for lists. It's human-readable and understood by every language.

A JSON **object** becomes a Python **dict**; a JSON **array** becomes a **list**.

## Working with JSON in Python

The built-in `json` module converts between Python objects and JSON. Remember the **s = string** rule: `dumps`/`loads` use strings, `dump`/`load` use files.

```python
import json

user = {"name": "Dami", "skills": ["python", "git"], "hours": 30}

# Save to a file
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(user, f, indent=2)

# Load it back into a Python dict
with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data["name"])        # Dami
print(data["skills"][0])   # python
```

## Your task

Save a small dictionary about yourself to a `profile.json` file, then write a second script that loads it and prints a friendly summary.
