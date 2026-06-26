---
course: ml-engineer
title: Testing and CI/CD for ML Systems
month: 6
monthTitle: Cloud Deployment, Scaling, and Monitoring
lesson: 2
summary: 'Learn to test machine learning systems the way employers expect: unit tests for pipeline code,
  API tests for your serving layer, data and schema validation, and model-quality gates. Then wire it
  all into a GitHub Actions CI/CD pipeline that runs your tests on every change and deploys automatically
  when you merge to main.'
objectives:
- Explain why ML systems need code tests plus data tests and model tests
- Write deterministic unit tests for pipeline and feature-engineering functions with pytest
- Test a FastAPI prediction service using TestClient and assert status codes and response schema
- Validate incoming data for ranges, nulls, and types using Great Expectations or pandera
- Add a model-quality gate that fails the build when an evaluation metric drops below a threshold
- Build a GitHub Actions workflow that installs dependencies, runs pytest, and deploys on merge to main
video: mle-m6-l02-testing-and-ci-cd-for-ml-systems.mp4
quiz:
- q: Compared with a traditional software project, what extra categories of tests does an ML system require?
  options:
  - Only slower integration tests
  - Data tests and model tests, on top of code tests
  - Manual tests only, since ML cannot be automated
  - Just more unit tests for the same code
  answer: 1
  why: ML systems fail not only from buggy code but from bad data and degraded models, so you add data-validation
    tests and model-quality tests in addition to ordinary code unit tests.
- q: When unit-testing a feature-engineering function with pytest, what property makes the test reliable?
  options:
  - It calls a live production database
  - It trains a full model first
  - It depends on the current system clock
  - 'It is deterministic: the same input always gives the same expected output'
  answer: 3
  why: Good unit tests are deterministic. You feed a known input and assert an exact expected output,
    so the test passes or fails for a clear reason rather than flaking on randomness or external state.
- q: How do you test a FastAPI prediction endpoint inside pytest without running a live server?
  options:
  - Wrap the app in fastapi.testclient.TestClient and call it in-process
  - Deploy to production and curl it
  - Open the browser at /docs manually
  - Disable validation and skip the endpoint
  answer: 0
  why: TestClient from fastapi.testclient drives the ASGI app in-process, letting you POST a request and
    assert on the status code and JSON body without binding a network port or starting uvicorn.
- q: What is the purpose of a data-validation test using a tool like Great Expectations or pandera?
  options:
  - To make training run faster
  - To replace the need for unit tests
  - To catch bad input early by asserting ranges, nulls, and types before it reaches the model
  - To automatically label the dataset
  answer: 2
  why: Data-validation tools declare a schema or set of expectations (value ranges, non-null columns,
    expected dtypes) and fail loudly when data violates them, catching corruption before it silently degrades
    predictions.
- q: In a CI pipeline, what should a model-quality gate do when the evaluation metric falls below the
    agreed threshold?
  options:
  - Fail the build so the regression is not merged or deployed
  - Silently log a warning and continue
  - Automatically lower the threshold to pass
  - Delete the test so the pipeline goes green
  answer: 0
  why: 'A quality gate is an assertion: if accuracy (or another metric) drops below the threshold the
    test fails, the CI run goes red, and the regression is blocked from merging or deploying.'
- q: Why is it important to gate the deploy job on the branch (for example, only run it when the ref is
    refs/heads/main)?
  answer: So that tests run on every push and pull request for fast feedback, but deployment only happens
    for trusted, reviewed code merged into the main branch rather than on every feature branch or PR.
  why: Running tests broadly gives early feedback on all branches, while restricting deploys to main ensures
    only reviewed, merged code reaches production, preventing accidental deployments from feature branches.
resources:
- label: pytest Official Documentation
  url: https://docs.pytest.org/en/stable/
- label: 'GitHub Actions: Building and Testing Python'
  url: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python
- label: 'Made With ML: Testing Machine Learning Systems'
  url: https://madewithml.com/courses/mlops/testing/
- label: 'pandera: Data Validation for DataFrames'
  url: https://pandera.readthedocs.io/en/stable/
---

## Why ML Systems Need Testing and CI/CD

Almost every machine learning engineer job description asks for "clean, versioned, tested code" and experience with **CI/CD**. The reason is simple: an ML system is software, and software that is not tested breaks in production. But ML adds two failure modes that traditional apps do not have. Your code can be correct while the **data** that flows through it is corrupt, or while the **model** has silently degraded. So an ML test suite has three layers: code tests, data tests, and model tests.

**CI/CD** stands for Continuous Integration and Continuous Delivery. CI runs your test suite automatically on every change so bugs are caught in minutes, not after release. CD automatically ships code that passes the tests. Together they turn "it worked on my laptop" into a repeatable, trustworthy pipeline.

## Unit-Testing Pipeline Functions with pytest

`pytest` is the standard Python testing framework. A test is just a function whose name starts with `test_`, containing `assert` statements. The golden rule is to make tests **deterministic**: feed a known input and assert an exact expected output.

```python
# features.py
def normalize(values):
    lo, hi = min(values), max(values)
    return [(v - lo) / (hi - lo) for v in values]

# test_features.py
from features import normalize

def test_normalize_scales_to_unit_range():
    out = normalize([0, 5, 10])
    assert out == [0.0, 0.5, 1.0]

def test_normalize_handles_negatives():
    out = normalize([-10, 0, 10])
    assert out[0] == 0.0 and out[-1] == 1.0
```

Run the whole suite with `pytest -q`. Test the deterministic transforms and feature logic that your pipeline depends on; that is where subtle bugs hide.

## Testing the Prediction API

Your serving layer is code too, so test it. FastAPI ships a `TestClient` (built on httpx) that drives your app **in-process** with no running server. You assert both the HTTP status code and the response schema.

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_returns_valid_schema():
    payload = {"sepal_length": 5.1, "sepal_width": 3.5,
               "petal_length": 1.4, "petal_width": 0.2}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "prediction" in body
    assert isinstance(body["prediction"], int)

def test_predict_rejects_bad_input():
    resp = client.post("/predict", json={"sepal_length": "oops"})
    assert resp.status_code == 422
```

The second test confirms that invalid input is rejected with a 422, exactly the contract Pydantic enforces.

## Data and Schema Validation Tests

Models are only as good as their inputs. A data-validation test asserts that incoming data has the right **ranges, nullability, and types** before it reaches the model. Tools like **pandera** and **Great Expectations** let you declare these expectations as a schema.

```python
import pandera as pa
from pandera import Column, Check

schema = pa.DataFrameSchema({
    "age": Column(int, Check.in_range(0, 120)),
    "income": Column(float, Check.greater_than(0), nullable=False),
    "country": Column(str, nullable=False),
})

def test_input_data_matches_schema(sample_df):
    schema.validate(sample_df)  # raises SchemaError if data is invalid
```

If a new batch contains negative ages or null incomes, validation fails fast with a clear error instead of producing garbage predictions.

## Model-Quality Gates

A model-quality gate is a test that **fails the build** when an evaluation metric drops below an agreed threshold. It protects you from merging a model that looks fine but quietly lost accuracy.

```python
from sklearn.metrics import accuracy_score
import joblib

MIN_ACCURACY = 0.85

def test_model_meets_accuracy_threshold():
    model = joblib.load("model.pkl")
    X_test, y_test = load_holdout()
    acc = accuracy_score(y_test, model.predict(X_test))
    assert acc >= MIN_ACCURACY, f"accuracy {acc:.3f} below {MIN_ACCURACY}"
```

Because it is an ordinary `assert`, the gate runs in the same `pytest` command as everything else, and a regression turns CI red.

## The CI/CD Pipeline with GitHub Actions

GitHub Actions runs your tests in the cloud on every push and pull request. A workflow is a YAML file in `.github/workflows/`. Below, the **test** job installs dependencies and runs pytest; the **deploy** job runs only after tests pass and only on the `main` branch.

```yaml
name: ML CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -q

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

The `needs: test` line makes deploy wait for green tests, and the `if` condition restricts deployment to merges into `main`. Pull requests get full test feedback but never deploy.

## Key Takeaways

Test ML systems in three layers: code, data, and model. Keep unit tests deterministic, drive your API with `TestClient`, validate data with pandera or Great Expectations, and gate merges on a model-quality assertion. Let GitHub Actions run it all and deploy only reviewed code on `main`. That is what "clean, versioned, tested code" looks like.
