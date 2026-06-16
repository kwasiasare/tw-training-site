---
course: dami-ai-career
title: Intro to APIs with the requests library
month: 1
monthTitle: Python Foundations + Git
lesson: 12
summary: Talk to web services from Python — send HTTP requests, read JSON responses, and handle errors
  with the requests library.
objectives:
- Explain what an API is and why programs use them to share data
- Send a GET request to a real API with requests.get
- Read the status code and check whether a request succeeded
- Parse a JSON response into a Python dictionary with .json()
- Pass query parameters and headers to customise a request
- Handle errors with raise_for_status and try / except
- Keep API keys out of your code using environment variables
video: m1-l12-apis-requests.mp4
quiz:
- q: What does API stand for?
  options:
  - Automated Program Input
  - Application Programming Interface
  - Applied Protocol Identifier
  - Advanced Python Integration
  answer: 1
  why: An API — Application Programming Interface — is a defined way for one program to request data or
    actions from another.
- q: Which HTTP status code means the request succeeded?
  options:
  - '200'
  - '404'
  - '500'
  - '301'
  answer: 0
  why: 200 means OK. 404 means not found, and 500 means a server error.
- q: Which requests method turns a JSON response body into a Python dictionary?
  options:
  - .text
  - .json()
  - .content
  - .parse()
  answer: 1
  why: response.json() decodes the JSON body into Python dicts and lists. .text gives the raw string.
- q: What does response.raise_for_status() do?
  answer: It raises an exception if the response status code indicates an error (4xx or 5xx), so failures
    aren't silently ignored.
  why: Without it, a failed request still returns a response object and your code may carry on with bad
    data.
- q: Why should you store an API key in an environment variable instead of writing it in your code?
  answer: So the secret key is not committed to git or shared publicly; it keeps credentials out of source
    control.
  why: Hard-coded keys leak when code is pushed to a repo; environment variables keep secrets separate
    from code.
- q: In requests.get(url, params={...}), what does the params argument do?
  options:
  - Sets the request body
  - Adds query string parameters to the URL
  - Sets authentication headers
  - Chooses the HTTP method
  answer: 1
  why: params builds the query string, e.g. ?q=python&limit=5, and handles encoding for you.
resources:
- label: requests — official documentation (Quickstart)
  url: https://requests.readthedocs.io/en/latest/user/quickstart/
- label: MDN — An overview of HTTP
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
- label: Real Python — Python's requests Library (Guide)
  url: https://realpython.com/python-requests/
- label: JSONPlaceholder — free fake REST API for testing
  url: https://jsonplaceholder.typicode.com/
---

## What is an API?

An **API** (Application Programming Interface) is a defined way for one program to ask another program for data or actions. When you check the weather in an app, that app sends a request to a weather service's API and gets data back. For an A I engineer, APIs are how you pull in data, call models, and connect systems.

Most web APIs work over **HTTP**, the same protocol your browser uses. You send a **request** to a URL; the server sends back a **response**.

## Installing and importing requests

The `requests` library is the friendliest way to make HTTP calls in Python. Install it once with pip.

```bash
pip install requests
```

Then import it in your script.

```python
import requests
```

## Your first GET request

A **GET** request asks a server for data. We call `requests.get` with a URL and get back a **response object**. The `status_code` tells us how it went — `200` means success.

```python
import requests

url = "https://jsonplaceholder.typicode.com/todos/1"
response = requests.get(url)

print(response.status_code)   # 200
print(response.json())        # {'userId': 1, 'id': 1, ...}
```

## Reading JSON responses

Most APIs reply in **JSON**, a text format of keys and values. Calling `.json()` converts it into a Python **dictionary** you can index like any other dict.

```python
data = response.json()
print(data["title"])        # the to-do's title
print(data["completed"])    # True or False
```

## Parameters, headers, and errors

Many APIs accept **query parameters** to filter results, and **headers** for things like authentication. Always check for errors: `raise_for_status()` throws if the request failed, and a `try`/`except` keeps your program from crashing.

```python
import requests

params = {"userId": 1}
try:
    r = requests.get("https://jsonplaceholder.typicode.com/todos", params=params, timeout=5)
    r.raise_for_status()
    todos = r.json()
    print(len(todos), "to-dos found")
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
```

## Keeping API keys safe

Paid APIs give you a secret **API key**. Never write it directly in your code — if you push to git, the key leaks. Store it in an **environment variable** and read it with `os.environ`.

```python
import os
import requests

api_key = os.environ["MY_API_KEY"]
headers = {"Authorization": "Bearer " + api_key}
r = requests.get("https://api.example.com/data", headers=headers)
```

## Your task

Pick a free public API (such as JSONPlaceholder), send a GET request, check the status code, and print one field from the JSON response.
