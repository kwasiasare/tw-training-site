---
course: dami-ai-career
title: HTTP & REST deep dive
month: 2
monthTitle: Data, SQL & Web APIs
lesson: 8
summary: Learn how HTTP requests, methods, status codes, and REST conventions let your code talk to web
  APIs.
objectives:
- Explain the request/response cycle behind every web API call
- Use the core HTTP methods GET, POST, PUT, PATCH, and DELETE correctly
- Read status codes and headers to tell success from failure
- Describe what makes an API RESTful, including resources and statelessness
- Send authenticated requests with headers and an API key or token
- Call a real JSON API from Python using the requests library
video: m2-l08-http-rest.mp4
quiz:
- q: Which HTTP method should you use to fetch data without changing anything on the server?
  options:
  - POST
  - GET
  - DELETE
  - PUT
  answer: 1
  why: GET retrieves a resource and is safe and read-only — it should never modify server state.
- q: What does a 404 status code mean?
  options:
  - Server error
  - Success
  - Not Found
  - Unauthorized
  answer: 2
  why: 404 is in the 4xx client-error family and means the requested resource does not exist at that URL.
- q: Which status code family means the request succeeded?
  options:
  - 1xx
  - 2xx
  - 4xx
  - 5xx
  answer: 1
  why: 2xx codes (like 200 OK and 201 Created) signal success; 4xx is client error and 5xx is server error.
- q: Name one property that makes an API RESTful.
  answer: 'Statelessness — each request carries all the information needed and the server stores no client
    session between requests (also acceptable: resource-based URLs, standard HTTP methods).'
  why: REST treats data as resources addressed by URLs, uses standard HTTP methods, and is stateless so
    requests are independent.
- q: What is the difference between PUT and PATCH?
  answer: PUT replaces the entire resource with the data you send; PATCH updates only the specific fields
    you include.
  why: Use PUT for a full replacement and PATCH for a partial update of an existing resource.
- q: Where do you usually put an API key or token when calling a protected endpoint?
  options:
  - In the URL path
  - In a request header
  - In the status code
  - In the method name
  answer: 1
  why: 'Credentials normally travel in a header such as Authorization: Bearer <token>, not in the visible
    path.'
resources:
- label: MDN Web Docs — HTTP overview
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
- label: MDN Web Docs — HTTP response status codes
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- label: Python requests — Quickstart
  url: https://requests.readthedocs.io/en/latest/user/quickstart/
- label: REST API Tutorial — What is REST?
  url: https://restfulapi.net/
---

## The request/response cycle

Every time your code talks to a web API, it follows the same pattern: a **client** sends a **request** to a **server**, and the server sends back a **response**. This is the heart of HTTP — the HyperText Transfer Protocol.

A request has four parts: a **method** (the verb), a **URL** (which resource), **headers** (metadata), and an optional **body** (data you send). A response comes back with a **status code**, headers, and usually a body — often JSON.

## HTTP methods (the verbs)

The method tells the server what you want to do with a resource.

- **GET** — read a resource. Safe and read-only.
- **POST** — create a new resource.
- **PUT** — replace an existing resource entirely.
- **PATCH** — update part of a resource.
- **DELETE** — remove a resource.

GET should never change anything. POST, PUT, PATCH, and DELETE are the ones that modify state.

## Status codes

The server replies with a three-digit code grouped into families:

- **2xx** — success (200 OK, 201 Created).
- **3xx** — redirection.
- **4xx** — client error — *you* sent something wrong (400 Bad Request, 401 Unauthorized, 404 Not Found).
- **5xx** — server error — the server broke (500 Internal Server Error).

Always check the status code before trusting the body.

## What makes an API RESTful

**REST** is a set of conventions, not a technology. A RESTful API treats your data as **resources**, each with its own URL — for example `/users/42`. You act on those resources using the standard HTTP methods, and the API is **stateless**: every request carries everything the server needs, so the server keeps no memory of you between calls.

This is why REST scales well and feels predictable: `GET /users/42` always means the same thing.

## Calling an API from Python

The `requests` library makes HTTP calls simple. Install it first:

```bash
pip install requests
```

Then send a GET request and read the JSON response:

```python
import requests

r = requests.get("https://api.github.com/users/octocat")
print(r.status_code)        # 200
data = r.json()             # parse JSON into a dict
print(data["name"])         # The Octocat
```

To send data and authenticate, use a method with a body and an Authorization header:

```python
import requests

headers = {"Authorization": "Bearer YOUR_TOKEN"}
payload = {"title": "Hello", "body": "My first API call"}
r = requests.post("https://api.example.com/posts",
                  json=payload, headers=headers)
print(r.status_code)        # 201 if created
```

## Your task

Use `requests` to call a free public API (try the GitHub users endpoint), print the status code, and pull two fields out of the JSON response.
