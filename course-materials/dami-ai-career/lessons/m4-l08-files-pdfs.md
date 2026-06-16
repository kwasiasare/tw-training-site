---
course: dami-ai-career
title: Working with files & PDFs
month: 4
monthTitle: Portfolio Projects
lesson: 8
summary: Read, write and parse files — text, CSV and PDFs — then feed extracted text to Claude for summaries
  and extraction.
objectives:
- Open, read and write files safely with the with statement
- Choose the right mode and encoding for text files
- Work with paths cleanly using pathlib
- Read and write CSV data with the csv and pandas libraries
- Extract text from PDFs using pypdf
- Send extracted document text to Claude for summarisation and extraction
- Handle missing files and bad input gracefully
video: m4-l08-files-pdfs.mp4
quiz:
- q: Why prefer the with statement when opening a file?
  options:
  - It runs faster
  - It closes the file automatically, even on error
  - It encrypts the file
  - It is required by Python
  answer: 1
  why: 'with open(...) as f: guarantees the file is closed when the block ends, even if an exception is
    raised.'
- q: Which file mode opens a file for writing and erases existing content?
  options:
  - '"r"'
  - '"a"'
  - '"w"'
  - '"x"'
  answer: 2
  why: '"w" truncates (empties) the file before writing. Use "a" to append, "r" to read.'
- q: What encoding should you almost always specify when reading text files?
  answer: utf-8
  why: Passing encoding="utf-8" avoids garbled characters and platform-dependent defaults across Windows,
    macOS and Linux.
- q: Which library reliably extracts text from a PDF in Python?
  options:
  - pandas
  - pypdf
  - requests
  - json
  answer: 1
  why: pypdf reads PDF pages and exposes extract_text(); pandas is for tables, requests for HTTP, json
    for JSON.
- q: After extracting messy PDF text, how do you get a clean summary with Claude?
  answer: Pass the extracted text inside the content of a messages.create call to the Claude Messages
    API.
  why: You send the raw text as the user message content and ask Claude to summarise or extract fields;
    keep the API key in an env var.
- q: True or false — pypdf's extract_text always returns perfectly clean, structured text.
  options:
  - 'True'
  - 'False'
  answer: 1
  why: False. Scanned or complex-layout PDFs often need cleaning, and image-only PDFs need OCR before
    any text is available.
resources:
- label: Python docs — Reading and Writing Files (tutorial 7.2)
  url: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
- label: pypdf documentation
  url: https://pypdf.readthedocs.io/en/stable/
- label: pathlib — Object-oriented filesystem paths
  url: https://docs.python.org/3/library/pathlib.html
- label: Anthropic — Messages API reference
  url: https://docs.anthropic.com/en/api/messages
---

## Why files matter for your portfolio

Real projects live on data, and that data sits in **files**: text logs, CSV exports, JSON config, and a lot of **PDFs** — invoices, reports, contracts. A portfolio project that ingests a folder of documents and produces a clean summary looks far more impressive than another toy notebook.

In this lesson you'll read and write files safely, parse CSVs, pull text out of PDFs, and hand that text to Claude to summarise or extract structured fields.

## Opening files the safe way

Always use the `with` statement. It closes the file automatically when the block ends — even if an error is thrown. Specify the **mode** (`r` read, `w` write, `a` append) and the **encoding**.

```python
# Read a whole text file
with open("notes.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Write a new file (overwrites!)
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
```

## Paths and CSVs

Use `pathlib` for paths so your code works on Windows, macOS and Linux. For tabular data, `pandas` reads and writes CSV in one line.

```python
from pathlib import Path
import pandas as pd

data_dir = Path("data")
df = pd.read_csv(data_dir / "sales.csv")
print(df.head())
df.to_csv(data_dir / "clean.csv", index=False)
```

## Extracting text from PDFs

Install `pypdf`, loop over the pages, and call `extract_text()`. Note that PDFs are messy — text can arrive out of order, and scanned (image-only) PDFs return nothing until you run OCR.

```python
from pypdf import PdfReader

reader = PdfReader("report.pdf")
pages = [page.extract_text() or "" for page in reader.pages]
full_text = "\n".join(pages)
```

## Sending document text to Claude

Once you have the text, let an **A I** model do the reading. Send the extracted text as the message content and ask Claude to summarise or pull out fields. Keep your key in the `ANTHROPIC_API_KEY` environment variable.

```python
from anthropic import Anthropic

client = Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user",
               "content": "Summarise this report in 5 bullets:\n\n" + full_text}],
)
print(msg.content[0].text)
```

## Your task

Build a small script that reads every PDF in a `docs/` folder, extracts the text, and writes a one-paragraph Claude summary of each into a CSV.
