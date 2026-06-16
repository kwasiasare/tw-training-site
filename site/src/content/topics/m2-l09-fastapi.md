---
title: Building REST APIs with FastAPI
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 9
summary: Expose your Python logic to the world by building fast, typed, auto-documented web APIs with
  the FastAPI framework.
objectives:
- Explain what a REST API is and how HTTP methods map to actions
- Create a FastAPI app and run it with the Uvicorn server
- Define GET and POST endpoints with path and query parameters
- Validate request bodies using Pydantic models
- Return correct status codes and JSON responses
- Use the auto-generated interactive docs to test your API
video: m2-l09-fastapi.mp4
quiz:
- q: In REST, which HTTP method is conventionally used to create a new resource?
  options:
  - GET
  - POST
  - DELETE
  - HEAD
  answer: 1
  why: POST sends data to the server to create a new resource. GET retrieves, PUT/PATCH update, and DELETE
    removes.
- q: What is the main job of a Pydantic model in FastAPI?
  options:
  - Connect to the database
  - Validate and parse incoming request data
  - Start the web server
  - Render HTML pages
  answer: 1
  why: Pydantic models declare the expected shape and types; FastAPI uses them to validate, parse, and
    document the request body automatically.
- q: Which HTTP status code means 'created successfully'?
  options:
  - '200'
  - '201'
  - '404'
  - '500'
  answer: 1
  why: 201 Created signals a new resource was made. 200 is generic OK, 404 is not found, and 500 is a
    server error.
- q: What command runs a FastAPI app where the FastAPI instance is named 'app' in a file called main.py?
  answer: uvicorn main:app --reload
  why: Uvicorn is the ASGI server. 'main:app' points to the app object in main.py, and --reload restarts
    on code changes during development.
- q: By default, at which URL path can you find FastAPI's interactive Swagger documentation?
  answer: /docs
  why: FastAPI auto-generates interactive Swagger UI at /docs and an alternative ReDoc page at /redoc
    from your code and type hints.
- q: True or false — FastAPI uses standard Python type hints to validate and convert request data.
  options:
  - 'True'
  - 'False'
  answer: 0
  why: True. FastAPI reads your type hints to validate input, convert types, and build documentation,
    which is a big reason it is so concise.
resources:
- label: FastAPI official documentation
  url: https://fastapi.tiangolo.com/
- label: FastAPI tutorial — User Guide (First Steps)
  url: https://fastapi.tiangolo.com/tutorial/first-steps/
- label: Pydantic documentation
  url: https://docs.pydantic.dev/latest/
- label: MDN — An overview of HTTP
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
---

## What is a REST API?

An **API** (Application Programming Interface) is a way for programs to talk to each other. A **REST API** does this over HTTP — the same protocol your browser uses. A client sends a **request** to a URL using a **method** (GET, POST, PUT, DELETE), and the server sends back a **response**, usually as JSON.

The methods map to actions: **GET** reads data, **POST** creates, **PUT/PATCH** update, and **DELETE** removes. This lets the maths logic you have been writing become a service other apps — and AI products — can call.

## FastAPI and your first endpoint

**FastAPI** is a modern Python framework for building APIs. It is fast, uses ordinary type hints, and generates interactive docs for free. Install it together with the **Uvicorn** server.

```bash
pip install "fastapi[standard]" uvicorn
```

A route is just a function with a decorator that says which method and path it answers.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, API!"}
```

## Running the server

Uvicorn serves your app. The `--reload` flag restarts it whenever you save a file.

```bash
uvicorn main:app --reload
```

Now visit `http://127.0.0.1:8000` for the response and `http://127.0.0.1:8000/docs` for the interactive Swagger documentation, where you can try every endpoint in the browser.

## Path and query parameters

Values inside the URL path become **path parameters**; type hints convert and validate them. Extra options after a `?` are **query parameters**.

```python
@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

Here FastAPI guarantees `item_id` is an integer — send text and it returns a clear 422 error automatically.

## Request bodies with Pydantic

To accept structured data, declare a **Pydantic model**. FastAPI validates the incoming JSON against it, parses it, and documents it for you.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items", status_code=201)
def create_item(item: Item):
    return {"created": item.name, "price": item.price}
```

Notice `status_code=201` — we return the correct "created" code rather than a plain 200.

## Your task

Build a small **books API**: a Pydantic `Book` model, a GET endpoint to list books, and a POST endpoint to add one. Test it all from the `/docs` page.
