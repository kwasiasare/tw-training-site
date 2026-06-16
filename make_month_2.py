# -*- coding: utf-8 -*-
"""Generate the Month 2 study pack: Data, SQL & Web APIs.

Run from the same directory so the `doc_helpers` import resolves:
    python make_month_2.py
"""
from doc_helpers import (
    new_doc, title_block, h1, h2, h3, para, lead, bullet, numbered,
    code_block, callout, table_from_rows, quiz, page_break,
    NAVY, ACCENT, GREY, GREEN, AMBER, RED,
)

OUT = "Month_2_Data_SQL_APIs_Study_Pack.docx"


def build():
    doc = new_doc()

    # ----------------------------------------------------------------- TITLE
    title_block(
        doc,
        "Month 2 - Data, SQL & Web APIs",
        "Maths Graduate to AI Engineer - 6-Month Programme",
        "Study Pack | ~30 hrs/week | Prerequisite: Month 1 (Python basics + Git)",
    )

    # ------------------------------------------------------- LEARNING OBJECTIVES
    h1(doc, "Learning objectives")
    para(doc,
         "By the end of Month 2 you will move from 'I can write a Python loop' to "
         "'I can take raw data, clean it, analyse it, store it, and serve it over the "
         "web'. This is the toolkit every entry-level data/ML engineer is expected to "
         "have. Concretely, you should be able to:")
    for b in [
        "Write idiomatic, expressive Python using comprehensions, generators, lambdas, "
        "*args/**kwargs and basic decorators.",
        "Write and run automated tests with pytest, including fixtures and parametrisation.",
        "Use NumPy to replace slow Python loops with fast vectorised array operations.",
        "Load, clean, reshape, group and join real datasets with Pandas.",
        "Produce clear charts with matplotlib to communicate findings.",
        "Write SQL that filters, joins, aggregates and uses subqueries and indexes.",
        "Design a small relational schema with sensible keys and normalisation.",
        "Explain HTTP/REST: methods, status codes, headers, auth and pagination.",
        "Build a working REST API with FastAPI and Pydantic models.",
        "Connect the maths you already know (vectors, dot products, probability) to the "
        "NumPy code that ML is built on.",
    ]:
        bullet(doc, b)

    page_break(doc)

    # ============================================================= TOPIC 1
    section_advanced_python(doc)
    page_break(doc)
    section_pytest(doc)
    page_break(doc)
    section_numpy(doc)
    page_break(doc)
    section_pandas(doc)
    page_break(doc)
    section_matplotlib(doc)
    page_break(doc)
    section_sql(doc)
    page_break(doc)
    section_data_modelling(doc)
    page_break(doc)
    section_http_rest(doc)
    page_break(doc)
    section_fastapi(doc)
    page_break(doc)
    section_maths_bridge(doc)
    page_break(doc)

    # ----------------------------------------------------------------- EXERCISES
    exercises(doc)
    page_break(doc)

    # ----------------------------------------------------------------- PROJECT
    project_brief(doc)
    page_break(doc)

    # ----------------------------------------------------------------- RESOURCES
    resources(doc)

    doc.save(OUT)
    print("Saved", OUT)


# ===================================================================== SECTIONS

def section_advanced_python(doc):
    h1(doc, "1. Advanced Python")
    para(doc,
         "In Month 1 you learned the building blocks: variables, loops, conditionals, "
         "functions and lists. This section teaches the constructs that make Python code "
         "shorter, faster and more 'Pythonic'. None of these add new power in a theoretical "
         "sense - a for-loop can do everything - but they make intent clearer and code "
         "easier to read, which matters enormously on a real team.")

    h2(doc, "Comprehensions")
    para(doc,
         "A list comprehension builds a list in a single expression. Read it as 'the "
         "expression, for each item, optionally if a condition holds'. It replaces the "
         "common pattern of creating an empty list and appending in a loop. There are also "
         "set comprehensions {..} and dict comprehensions {k: v for ..}.")
    code_block(doc,
               "# Old style\n"
               "squares = []\n"
               "for n in range(10):\n"
               "    if n % 2 == 0:\n"
               "        squares.append(n * n)\n\n"
               "# Comprehension (same result)\n"
               "squares = [n * n for n in range(10) if n % 2 == 0]\n\n"
               "# Dict comprehension: word -> length\n"
               "words = ['cat', 'tiger', 'ox']\n"
               "lengths = {w: len(w) for w in words}\n"
               "print(squares)   # [0, 4, 16, 36, 64]\n"
               "print(lengths)   # {'cat': 3, 'tiger': 5, 'ox': 2}")

    h2(doc, "Generators")
    para(doc,
         "A generator produces values one at a time, on demand, instead of building the "
         "whole list in memory. You create one with a function that uses 'yield', or with a "
         "generator expression (round brackets instead of square). Generators are lazy: they "
         "are perfect for large or infinite sequences and for streaming data because they "
         "never hold everything in memory at once.")
    code_block(doc,
               "def first_n_squares(n):\n"
               "    for i in range(n):\n"
               "        yield i * i        # 'yield' pauses and returns one value\n\n"
               "gen = first_n_squares(5)\n"
               "print(next(gen))           # 0\n"
               "print(list(gen))           # [1, 4, 9, 16]  (continues where it left off)\n\n"
               "# Generator expression: sum without building a list in memory\n"
               "total = sum(i * i for i in range(1_000_000))\n"
               "print(total)")

    h2(doc, "Lambdas")
    para(doc,
         "A lambda is a tiny anonymous (unnamed) function written inline. It is limited to a "
         "single expression. Lambdas are most useful as the 'key' argument to sorted(), max(), "
         "min() and similar functions, where you need a small throwaway function.")
    code_block(doc,
               "people = [('Ada', 36), ('Alan', 41), ('Grace', 28)]\n\n"
               "# Sort by age (the second element of each tuple)\n"
               "by_age = sorted(people, key=lambda person: person[1])\n"
               "print(by_age)   # [('Grace', 28), ('Ada', 36), ('Alan', 41)]\n\n"
               "add = lambda a, b: a + b   # works, but a def is clearer for named funcs\n"
               "print(add(2, 3))           # 5")

    h2(doc, "*args and **kwargs")
    para(doc,
         "These let a function accept any number of positional or keyword arguments. Inside "
         "the function, *args is a tuple of the extra positional arguments and **kwargs is a "
         "dict of the extra keyword arguments. The names 'args' and 'kwargs' are convention; "
         "the * and ** are what matter. You can also use * and ** to 'unpack' a list or dict "
         "into a call.")
    code_block(doc,
               "def describe(label, *args, **kwargs):\n"
               "    print('label:', label)\n"
               "    print('extra positionals:', args)\n"
               "    print('extra keywords:', kwargs)\n\n"
               "describe('demo', 1, 2, 3, colour='red', size=10)\n"
               "# label: demo\n"
               "# extra positionals: (1, 2, 3)\n"
               "# extra keywords: {'colour': 'red', 'size': 10}\n\n"
               "nums = [4, 9, 16]\n"
               "print(max(*nums))   # unpacks to max(4, 9, 16) -> 16")

    h2(doc, "Decorators (intro)")
    para(doc,
         "A decorator is a function that wraps another function to add behaviour, without "
         "changing the wrapped function's own code. Because functions are first-class objects "
         "in Python (you can pass them around like any value), a decorator simply takes a "
         "function and returns a new function. The @name syntax above a def is just sugar for "
         "'func = name(func)'. You will meet decorators constantly: @pytest.fixture, "
         "@app.get in FastAPI, @property, and many more.")
    code_block(doc,
               "import functools\n"
               "import time\n\n"
               "def timed(func):\n"
               "    @functools.wraps(func)            # preserves func's name/docstring\n"
               "    def wrapper(*args, **kwargs):\n"
               "        start = time.perf_counter()\n"
               "        result = func(*args, **kwargs)\n"
               "        elapsed = time.perf_counter() - start\n"
               "        print(f'{func.__name__} took {elapsed:.4f}s')\n"
               "        return result\n"
               "    return wrapper\n\n"
               "@timed                                # same as: slow = timed(slow)\n"
               "def slow(n):\n"
               "    return sum(range(n))\n\n"
               "slow(1_000_000)   # prints: slow took 0.01xx s")

    callout(doc, "Common mistakes",
            "Don't mutate a list while iterating over it. Comprehensions that are too long "
            "become unreadable - prefer a loop past two clauses. A generator is exhausted "
            "after one full pass: looping over it twice yields nothing the second time. "
            "Avoid assigning a lambda to a name (use def instead). Forgetting functools.wraps "
            "in a decorator hides the original function's name, which breaks debugging and "
            "some frameworks.")

    quiz(doc, [
        {"q": "Which builds a list of the even numbers 0-8?",
         "options": ["[n for n in range(9) if n % 2 == 0]",
                     "[n for n in range(9) if n % 2 == 1]",
                     "(n for n in range(9) if n % 2 == 0)",
                     "{n for n in range(9) if n % 2 == 0}"],
         "answer": "A",
         "why": "Option C is a generator (not a list) and D is a set; B keeps odds."},
        {"q": "What is the key difference between a list and a generator?",
         "answer": "A list stores all its items in memory at once; a generator produces "
                   "items lazily, one at a time, on demand.",
         "why": "This makes generators memory-efficient for large or infinite streams."},
        {"q": "After calling next(g) once on a generator of 3 values, how many remain?",
         "options": ["3", "2", "0", "Error"],
         "answer": "B", "why": "Each next() consumes one value; two remain."},
        {"q": "In 'def f(*args, **kwargs)', what type is kwargs inside the function?",
         "options": ["list", "tuple", "dict", "set"],
         "answer": "C", "why": "*args collects extra positionals into a tuple; **kwargs "
                                "collects extra keyword args into a dict."},
        {"q": "What does the @ decorator syntax 'desugar' to? Given '@d' above 'def f(): ...'",
         "answer": "f = d(f)",
         "why": "The decorator d is called with f and the result is rebound to the name f."},
        {"q": "Why use functools.wraps inside a decorator?",
         "answer": "It copies the wrapped function's name, docstring and metadata onto the "
                   "wrapper, so debugging and introspection still work.",
         "why": "Without it, every decorated function would appear to be named 'wrapper'."},
        {"q": "Best use of a lambda?",
         "options": ["Defining a 50-line function", "As the key= argument to sorted()",
                     "Replacing all def statements", "Importing a module"],
         "answer": "B", "why": "Lambdas shine as small inline throwaway functions, "
                                "e.g. sort keys."},
    ], title="Quiz - Advanced Python")


def section_pytest(doc):
    h1(doc, "2. Automated testing with pytest")
    para(doc,
         "Testing is the habit that separates hobby code from professional code. An automated "
         "test is just a function that calls your code and asserts the result is what you "
         "expect. When you change code later, you re-run the tests and instantly know if you "
         "broke something. pytest is the de-facto standard test runner for Python: it is "
         "simple, uses plain 'assert', and finds your tests automatically.")
    para(doc,
         "Convention: put tests in files named test_*.py, with functions named test_*. Run "
         "everything by typing 'pytest' in the terminal. pytest discovers and runs them, then "
         "prints a green dot per pass and a detailed traceback per failure.")

    h2(doc, "A first test")
    code_block(doc,
               "# file: calculator.py\n"
               "def add(a, b):\n"
               "    return a + b\n\n"
               "def divide(a, b):\n"
               "    if b == 0:\n"
               "        raise ValueError('cannot divide by zero')\n"
               "    return a / b")
    code_block(doc,
               "# file: test_calculator.py\n"
               "import pytest\n"
               "from calculator import add, divide\n\n"
               "def test_add():\n"
               "    assert add(2, 3) == 5\n"
               "    assert add(-1, 1) == 0\n\n"
               "def test_divide_normal():\n"
               "    assert divide(10, 2) == 5\n\n"
               "def test_divide_by_zero_raises():\n"
               "    with pytest.raises(ValueError):\n"
               "        divide(1, 0)\n\n"
               "# Run from the terminal:  pytest -v")

    h2(doc, "Parametrisation - many cases, one test")
    para(doc,
         "Instead of copying a test for each input, @pytest.mark.parametrize feeds it a table "
         "of inputs and expected outputs. pytest runs the function once per row and reports "
         "each separately.")
    code_block(doc,
               "import pytest\n"
               "from calculator import add\n\n"
               "@pytest.mark.parametrize('a, b, expected', [\n"
               "    (2, 3, 5),\n"
               "    (0, 0, 0),\n"
               "    (-1, -1, -2),\n"
               "    (100, 1, 101),\n"
               "])\n"
               "def test_add_many(a, b, expected):\n"
               "    assert add(a, b) == expected")

    h2(doc, "Fixtures - reusable setup")
    para(doc,
         "A fixture is reusable setup code (a sample object, a temp file, a database "
         "connection). You declare it with @pytest.fixture and 'request' it by naming it as a "
         "test argument; pytest supplies it automatically.")
    code_block(doc,
               "import pytest\n\n"
               "@pytest.fixture\n"
               "def sample_users():\n"
               "    return [{'name': 'Ada'}, {'name': 'Alan'}]\n\n"
               "def test_user_count(sample_users):\n"
               "    assert len(sample_users) == 2\n\n"
               "def test_first_user(sample_users):\n"
               "    assert sample_users[0]['name'] == 'Ada'")

    callout(doc, "Common mistakes",
            "Test files or functions not named test_* are silently skipped - nothing runs and "
            "you think you're green. Tests that depend on each other's order are fragile; each "
            "test should stand alone. Using '==' to compare floats fails on rounding - use "
            "pytest.approx(). Asserting nothing (forgetting 'assert') makes a test that can "
            "never fail. Catching an exception with try/except instead of pytest.raises hides "
            "whether it was actually raised.")

    quiz(doc, [
        {"q": "What file/function naming does pytest discover by default?",
         "options": ["main_*.py / run_*", "test_*.py / test_*",
                     "spec_*.py / it_*", "any name works"],
         "answer": "B", "why": "pytest auto-discovers test_*.py (or *_test.py) files and "
                                "test_* functions."},
        {"q": "Which construct asserts that a call raises a specific exception?",
         "options": ["assert raises(ValueError)", "with pytest.raises(ValueError):",
                     "expect(ValueError)", "try: ... except: pass"],
         "answer": "B", "why": "pytest.raises is a context manager that passes only if the "
                                "expected exception is raised inside the block."},
        {"q": "What does @pytest.mark.parametrize do?",
         "answer": "Runs the same test function multiple times with different argument sets, "
                   "reporting each case separately.",
         "why": "It removes copy-paste duplication across similar test cases."},
        {"q": "How does a test receive a fixture's value?",
         "answer": "By naming the fixture as a parameter of the test function; pytest injects "
                   "it automatically.",
         "why": "This is dependency injection - pytest matches the parameter name to a fixture."},
        {"q": "Why prefer pytest.approx() when comparing floats?",
         "answer": "Floating-point arithmetic has tiny rounding errors, so exact == often "
                   "fails; approx() compares within a small tolerance.",
         "why": "e.g. 0.1 + 0.2 == 0.3 is False in floating point."},
        {"q": "A test function contains no 'assert'. Will pytest ever mark it failed (assuming "
              "no exception)?",
         "options": ["Yes, always", "No - with nothing to assert it passes", "Only with -v",
                     "It errors"],
         "answer": "B", "why": "A test passes if it runs without raising; without an assert "
                                "there is nothing to fail it - a silent false sense of safety."},
    ], title="Quiz - pytest")


def section_numpy(doc):
    h1(doc, "3. NumPy arrays & vectorised operations")
    para(doc,
         "NumPy is the foundation of the entire Python data/ML stack - Pandas, scikit-learn, "
         "PyTorch and TensorFlow all build on its array. The core object is the ndarray: a "
         "fixed-size, same-type, N-dimensional grid of numbers stored in a compact block of "
         "memory. Because the data is contiguous and typed, NumPy can run operations in "
         "optimised C code over the whole array at once - this is called vectorisation, and it "
         "is often 10-100x faster than a Python loop.")
    para(doc,
         "Mentally, a 1-D array is a vector, a 2-D array is a matrix, and higher dimensions are "
         "tensors. As a maths grad this should feel natural - NumPy is essentially linear "
         "algebra with a programming interface.")

    h2(doc, "Creating and operating on arrays")
    code_block(doc,
               "import numpy as np\n\n"
               "a = np.array([1, 2, 3, 4])\n"
               "b = np.array([10, 20, 30, 40])\n\n"
               "print(a + b)        # [11 22 33 44]  - elementwise, no loop\n"
               "print(a * 2)        # [2 4 6 8]      - broadcasting a scalar\n"
               "print(a.dot(b))     # 300            - dot product\n"
               "print(a.mean())     # 2.5\n"
               "print(a.shape)      # (4,)\n\n"
               "m = np.arange(6).reshape(2, 3)   # 2x3 matrix [[0 1 2] [3 4 5]]\n"
               "print(m.sum(axis=0))             # column sums [3 5 7]\n"
               "print(m.sum(axis=1))             # row sums    [3 12]")

    h2(doc, "Vectorisation vs a Python loop")
    para(doc,
         "The same calculation - here, squaring a million numbers - is far faster as a single "
         "array expression than as an element-by-element Python loop, because the loop runs in "
         "the C layer rather than the Python interpreter.")
    code_block(doc,
               "import numpy as np\n\n"
               "data = np.arange(1_000_000)\n\n"
               "# Vectorised: one expression, runs in C\n"
               "squared = data ** 2\n\n"
               "# Boolean masking: select without a loop\n"
               "big = data[data > 999_000]\n"
               "print(big[:5])          # [999001 999002 999003 999004 999005]\n"
               "print(squared.mean())   # average of the squares")

    h2(doc, "Broadcasting")
    para(doc,
         "Broadcasting is NumPy's rule for combining arrays of different shapes. The smaller "
         "array is 'stretched' across the larger one without copying data. A scalar broadcasts "
         "to every element; a (3,) row vector broadcasts across every row of a (2,3) matrix.")
    code_block(doc,
               "import numpy as np\n\n"
               "prices = np.array([[100.0], [200.0], [300.0]])  # shape (3,1)\n"
               "rates = np.array([1.0, 1.1, 1.2])               # shape (3,)\n"
               "print(prices * rates)   # (3,3): each price scaled by each rate")

    callout(doc, "Common mistakes",
            "NumPy arrays are a single fixed dtype: putting a string into an int array silently "
            "converts everything. Slices are views, not copies - editing a slice edits the "
            "original; use .copy() if you need independence. Don't loop element by element 'to "
            "be safe' - that throws away NumPy's whole point. Shape mismatches that don't follow "
            "broadcasting rules raise a ValueError. Integer arrays truncate division results "
            "(use float).")

    quiz(doc, [
        {"q": "What does 'vectorisation' mean in NumPy?",
         "answer": "Performing an operation on a whole array at once in fast compiled C code, "
                   "instead of looping element by element in Python.",
         "why": "It is both faster and more concise than an explicit Python loop."},
        {"q": "Given a = np.array([1,2,3]), what is a * 3?",
         "options": ["[1,2,3,1,2,3,1,2,3]", "[3,6,9]", "9", "error"],
         "answer": "B", "why": "A scalar broadcasts and multiplies each element; list "
                                "repetition (the first option) is Python-list behaviour."},
        {"q": "m.sum(axis=0) on a 2-D array sums along which direction?",
         "options": ["Each row", "Each column (down the rows)", "Everything", "The diagonal"],
         "answer": "B", "why": "axis=0 collapses the row axis, giving one value per column."},
        {"q": "Is a basic NumPy slice a copy or a view of the original array?",
         "answer": "A view - it shares memory, so modifying the slice modifies the original.",
         "why": "Use .copy() when you need an independent array."},
        {"q": "np.array([1,2,3]).dot(np.array([4,5,6])) equals?",
         "options": ["[4,10,18]", "32", "15", "error"],
         "answer": "B", "why": "Dot product: 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32."},
        {"q": "What is broadcasting?",
         "answer": "NumPy's rule for automatically expanding a smaller array's shape to match a "
                   "larger one in an operation, without copying data.",
         "why": "It lets a scalar or row vector combine with a matrix elementwise."},
    ], title="Quiz - NumPy")


def section_pandas(doc):
    h1(doc, "4. Pandas - loading, cleaning, transforming")
    para(doc,
         "Pandas is the workhorse for tabular data in Python - think of it as a programmable "
         "spreadsheet. Its two core objects are the Series (a single labelled column) and the "
         "DataFrame (a table of columns sharing one index). Real datasets are messy: missing "
         "values, wrong types, duplicates, inconsistent text. Pandas gives you tools to load, "
         "clean, reshape, group and join that data, and it sits on top of NumPy so it inherits "
         "vectorised speed.")

    h2(doc, "Loading and inspecting")
    code_block(doc,
               "import pandas as pd\n\n"
               "df = pd.read_csv('sales.csv')\n\n"
               "df.head()        # first 5 rows\n"
               "df.shape         # (rows, columns)\n"
               "df.info()        # column names, dtypes, non-null counts\n"
               "df.describe()    # summary stats for numeric columns\n"
               "df['region'].value_counts()   # frequency of each region")

    h2(doc, "Cleaning")
    para(doc,
         "Cleaning typically means handling missing values (drop or fill), fixing data types, "
         "removing duplicates and standardising text. Always inspect before and after.")
    code_block(doc,
               "import pandas as pd\n\n"
               "df = pd.read_csv('sales.csv')\n\n"
               "df = df.drop_duplicates()                      # remove exact duplicate rows\n"
               "df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # bad -> NaN\n"
               "df['amount'] = df['amount'].fillna(0)          # fill missing with 0\n"
               "df['region'] = df['region'].str.strip().str.title()  # tidy text\n"
               "df = df.dropna(subset=['date'])                # drop rows missing a date\n"
               "df['date'] = pd.to_datetime(df['date'])        # parse to datetime")

    h2(doc, "Selecting, filtering, new columns")
    code_block(doc,
               "# Boolean filtering\n"
               "north = df[df['region'] == 'North']\n"
               "big = df[(df['amount'] > 1000) & (df['region'] == 'North')]\n\n"
               "# .loc selects by label, .iloc by integer position\n"
               "first_amount = df.loc[0, 'amount']\n"
               "first_row = df.iloc[0]\n\n"
               "# Create a derived column\n"
               "df['amount_with_tax'] = df['amount'] * 1.2")

    h2(doc, "groupby - split, apply, combine")
    para(doc,
         "groupby is the most important analytical tool in Pandas. It splits the data into "
         "groups by a key, applies an aggregation to each group, and combines the results into "
         "a new table. This is the same idea as SQL's GROUP BY.")
    code_block(doc,
               "# Total and average sales per region\n"
               "summary = df.groupby('region')['amount'].agg(['sum', 'mean', 'count'])\n"
               "print(summary)\n\n"
               "# Multiple grouping keys\n"
               "by_region_month = df.groupby(['region', df['date'].dt.month])['amount'].sum()")

    h2(doc, "merge / join")
    para(doc,
         "merge combines two DataFrames on a shared key column, exactly like a SQL join. The "
         "'how' argument controls which rows survive: inner (only matches), left (all rows from "
         "the left table), right, or outer (everything).")
    code_block(doc,
               "import pandas as pd\n\n"
               "orders = pd.DataFrame({'customer_id': [1, 2, 3],\n"
               "                       'amount': [100, 250, 90]})\n"
               "customers = pd.DataFrame({'customer_id': [1, 2, 4],\n"
               "                          'name': ['Ada', 'Alan', 'Grace']})\n\n"
               "merged = orders.merge(customers, on='customer_id', how='left')\n"
               "print(merged)\n"
               "# customer 3 has no name (NaN); customer 4 (no order) is excluded in a left join")

    callout(doc, "Common mistakes",
            "'Chained assignment' like df[df.x > 0]['y'] = 1 may not change the DataFrame and "
            "triggers SettingWithCopyWarning - use .loc instead. NaN != NaN, so use .isna() not "
            "== to find missing values. Forgetting that most Pandas methods return a NEW object "
            "and don't modify in place (reassign or pass inplace=True). Combining filters with "
            "Python 'and'/'or' fails - use & and | with parentheses around each condition. Inner "
            "joins silently drop unmatched rows; check your row count before and after.")

    quiz(doc, [
        {"q": "What are the two core Pandas data structures?",
         "options": ["List and Dict", "Series and DataFrame", "Array and Matrix",
                     "Row and Column"],
         "answer": "B", "why": "A Series is one labelled column; a DataFrame is a table of "
                                "Series sharing an index."},
        {"q": "Which join keeps ALL rows from the left table, matching where possible?",
         "options": ["inner", "left", "right", "cross"],
         "answer": "B", "why": "A left join keeps every left row, filling unmatched right "
                                "columns with NaN."},
        {"q": "What does df.groupby('region')['amount'].sum() return?",
         "answer": "The total of 'amount' for each distinct value of 'region' (split-apply-"
                   "combine).",
         "why": "groupby splits by the key, sum aggregates each group, results are combined."},
        {"q": "How do you correctly filter rows where amount>1000 AND region=='North'?",
         "options": ["df[df.amount>1000 and df.region=='North']",
                     "df[(df.amount>1000) & (df.region=='North')]",
                     "df.filter(amount>1000, region='North')",
                     "df[df.amount>1000][region=='North']"],
         "answer": "B", "why": "Pandas needs vectorised & with parentheses; Python 'and' "
                                "raises on arrays."},
        {"q": "Why use .isna() instead of == NaN to find missing values?",
         "answer": "Because NaN is not equal to anything, including itself, so == NaN is "
                   "always False; .isna() detects them correctly.",
         "why": "This is IEEE floating-point NaN semantics."},
        {"q": "Difference between .loc and .iloc?",
         "answer": ".loc selects by label/name; .iloc selects by integer position.",
         "why": "df.loc[0,'amount'] uses labels; df.iloc[0,2] uses positions."},
        {"q": "Do most Pandas methods modify the DataFrame in place by default?",
         "options": ["Yes", "No - they return a new object", "Only numeric ones", "Random"],
         "answer": "B", "why": "Most return a new object; you must reassign or pass "
                                "inplace=True (where supported)."},
    ], title="Quiz - Pandas")


def section_matplotlib(doc):
    h1(doc, "5. Data visualisation with matplotlib")
    para(doc,
         "A chart communicates a pattern faster than a table of numbers. matplotlib is the "
         "foundational plotting library in Python; Pandas plotting and Seaborn are built on it. "
         "The mental model: a Figure is the whole canvas, and it contains one or more Axes (an "
         "individual plot with its x/y axes). You draw onto an Axes, label it, then show or save.")

    h2(doc, "A line chart and a bar chart")
    code_block(doc,
               "import matplotlib.pyplot as plt\n\n"
               "months = ['Jan', 'Feb', 'Mar', 'Apr']\n"
               "sales = [120, 135, 100, 160]\n\n"
               "fig, ax = plt.subplots(figsize=(7, 4))\n"
               "ax.plot(months, sales, marker='o', label='2025')\n"
               "ax.set_title('Monthly sales')\n"
               "ax.set_xlabel('Month')\n"
               "ax.set_ylabel('Sales (k)')\n"
               "ax.legend()\n"
               "ax.grid(True, alpha=0.3)\n"
               "fig.savefig('sales_line.png', dpi=150, bbox_inches='tight')\n"
               "plt.show()")
    code_block(doc,
               "import matplotlib.pyplot as plt\n\n"
               "regions = ['North', 'South', 'East', 'West']\n"
               "totals = [4200, 3100, 2800, 3900]\n\n"
               "fig, ax = plt.subplots()\n"
               "ax.bar(regions, totals, color='steelblue')\n"
               "ax.set_title('Total sales by region')\n"
               "ax.set_ylabel('Total sales')\n"
               "plt.tight_layout()\n"
               "plt.show()")

    h2(doc, "Histograms and subplots")
    para(doc,
         "A histogram shows the distribution of one numeric variable by binning values. "
         "plt.subplots(rows, cols) creates a grid of Axes so you can compare charts side by side.")
    code_block(doc,
               "import matplotlib.pyplot as plt\n"
               "import numpy as np\n\n"
               "data = np.random.default_rng(0).normal(loc=50, scale=10, size=1000)\n\n"
               "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))\n"
               "ax1.hist(data, bins=30, color='seagreen')\n"
               "ax1.set_title('Histogram')\n"
               "ax2.boxplot(data)\n"
               "ax2.set_title('Box plot')\n"
               "plt.tight_layout()\n"
               "plt.show()")

    callout(doc, "Common mistakes",
            "Forgetting plt.show() (interactive) or savefig() (script) means nothing appears. "
            "Always label axes and add a title - an unlabelled chart is useless. Calling plot "
            "repeatedly without a new Figure stacks everything on one Axes. Choosing the wrong "
            "chart type (pie charts for many categories, line charts for unordered categories) "
            "misleads. Saving before show() is fine, but show() can clear the figure on some "
            "backends, so savefig() first if scripting.")

    quiz(doc, [
        {"q": "In matplotlib's model, what is the relationship between a Figure and an Axes?",
         "answer": "A Figure is the whole canvas; it contains one or more Axes, each an "
                   "individual plot with its own x and y axes.",
         "why": "You draw data onto an Axes, not directly onto the Figure."},
        {"q": "Which chart best shows the distribution of a single numeric variable?",
         "options": ["Line chart", "Pie chart", "Histogram", "Scatter of one variable"],
         "answer": "C", "why": "A histogram bins values to reveal their distribution/spread."},
        {"q": "What does plt.subplots(1, 2) return and create?",
         "answer": "A Figure and a row of two Axes (it returns the figure and an array/tuple "
                   "of the two Axes objects).",
         "why": "It lets you place two plots side by side for comparison."},
        {"q": "In a script (no interactive window), how do you persist a chart to disk?",
         "options": ["plt.show()", "fig.savefig('name.png')", "print(fig)", "ax.draw()"],
         "answer": "B", "why": "savefig writes the figure to an image file; show() only opens a "
                                "window."},
        {"q": "Why label axes and add a title on every chart?",
         "answer": "So a reader can understand what is being measured and in what units; an "
                   "unlabelled chart cannot be interpreted.",
         "why": "Communication is the whole point of a visualisation."},
    ], title="Quiz - matplotlib")


def section_sql(doc):
    h1(doc, "6. SQL in depth")
    para(doc,
         "SQL (Structured Query Language) is how you talk to relational databases, and it is "
         "one of the most durable, in-demand skills in tech. Data lives in tables (rows and "
         "columns); SQL is a declarative language - you describe WHAT you want, and the "
         "database engine figures out HOW to fetch it efficiently. Almost every data and ML "
         "role expects solid SQL.")

    h2(doc, "SELECT, WHERE, ORDER BY, LIMIT")
    para(doc,
         "SELECT chooses columns; FROM names the table; WHERE filters rows; ORDER BY sorts; "
         "LIMIT caps the row count. Logical order of evaluation: FROM -> WHERE -> GROUP BY -> "
         "HAVING -> SELECT -> ORDER BY -> LIMIT.")
    code_block(doc,
               "SELECT name, region, amount\n"
               "FROM   orders\n"
               "WHERE  amount > 1000\n"
               "  AND  region = 'North'\n"
               "ORDER BY amount DESC\n"
               "LIMIT 10;")

    h2(doc, "Aggregations and GROUP BY")
    para(doc,
         "Aggregate functions (COUNT, SUM, AVG, MIN, MAX) collapse many rows into one value. "
         "GROUP BY produces one aggregated row per group. WHERE filters rows BEFORE grouping; "
         "HAVING filters groups AFTER aggregation.")
    code_block(doc,
               "SELECT   region,\n"
               "         COUNT(*)      AS num_orders,\n"
               "         SUM(amount)   AS total,\n"
               "         AVG(amount)   AS avg_amount\n"
               "FROM     orders\n"
               "WHERE    amount > 0\n"
               "GROUP BY region\n"
               "HAVING   SUM(amount) > 5000\n"
               "ORDER BY total DESC;")

    h2(doc, "JOINs")
    para(doc,
         "A JOIN combines rows from two tables using a related column. INNER JOIN keeps only "
         "matching pairs. LEFT JOIN keeps every row from the left table, with NULLs where the "
         "right has no match. This is the relational counterpart of Pandas merge.")
    code_block(doc,
               "SELECT c.name, o.amount\n"
               "FROM   customers AS c\n"
               "JOIN   orders    AS o ON o.customer_id = c.id   -- INNER by default\n"
               "WHERE  o.amount > 100;\n\n"
               "-- Keep customers even if they have no orders:\n"
               "SELECT c.name, o.amount\n"
               "FROM   customers AS c\n"
               "LEFT JOIN orders AS o ON o.customer_id = c.id;")

    h2(doc, "Subqueries")
    para(doc,
         "A subquery is a query nested inside another. Use it to filter against a computed set "
         "or value - here, customers whose order beat the overall average.")
    code_block(doc,
               "SELECT name, amount\n"
               "FROM   orders\n"
               "WHERE  amount > (SELECT AVG(amount) FROM orders)\n"
               "ORDER BY amount DESC;")

    h2(doc, "Indexes")
    para(doc,
         "An index is a sorted lookup structure (typically a B-tree) the database keeps on one "
         "or more columns. It lets the engine find matching rows without scanning the whole "
         "table - like the index at the back of a book. Indexes hugely speed up WHERE and JOIN "
         "on the indexed columns, but they cost extra storage and slow down writes, because "
         "every insert/update must also update the index. Index the columns you filter and join "
         "on; don't index everything.")
    code_block(doc,
               "CREATE INDEX idx_orders_customer ON orders (customer_id);\n"
               "CREATE INDEX idx_orders_region   ON orders (region);")

    callout(doc, "Common mistakes",
            "Comparing to NULL with = never matches - use IS NULL / IS NOT NULL. Putting an "
            "aggregate condition in WHERE instead of HAVING is an error - WHERE runs before "
            "grouping. Selecting columns not in GROUP BY (and not aggregated) is invalid in "
            "standard SQL. A missing JOIN condition produces a cartesian product (every row "
            "times every row). SELECT * in production code is fragile and slow - name your "
            "columns.")

    quiz(doc, [
        {"q": "Which clause filters GROUPS after aggregation?",
         "options": ["WHERE", "HAVING", "ORDER BY", "LIMIT"],
         "answer": "B", "why": "WHERE filters rows before grouping; HAVING filters the "
                                "aggregated groups afterwards."},
        {"q": "What does a LEFT JOIN return that an INNER JOIN does not?",
         "answer": "All rows from the left table even when there is no matching right row "
                   "(right columns become NULL).",
         "why": "INNER keeps only matched pairs; LEFT preserves unmatched left rows."},
        {"q": "How do you correctly test for a NULL value?",
         "options": ["x = NULL", "x == NULL", "x IS NULL", "x EQUALS NULL"],
         "answer": "C", "why": "NULL is unknown, so = NULL is never true; IS NULL is the "
                                "correct test."},
        {"q": "Name the trade-off of adding an index.",
         "answer": "Faster reads/lookups on the indexed columns, but extra storage and slower "
                   "inserts/updates because the index must be maintained.",
         "why": "Indexes speed reads at the cost of write performance and disk space."},
        {"q": "Write a query for the total amount per region (table orders, columns region, "
              "amount). Short answer.",
         "answer": "SELECT region, SUM(amount) FROM orders GROUP BY region;",
         "why": "SUM is the aggregate; GROUP BY region gives one row per region."},
        {"q": "What happens if you JOIN two tables but forget the ON condition?",
         "options": ["Syntax error always", "A cartesian product (every row paired with every "
                     "row)", "Returns nothing", "Returns only the left table"],
         "answer": "B", "why": "Without a join predicate you get the cross product - usually a "
                                "bug and a huge result set."},
        {"q": "In logical evaluation order, does SELECT run before or after WHERE?",
         "options": ["Before", "After", "Same time", "Never"],
         "answer": "B", "why": "Order is FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> "
                                "ORDER BY, so SELECT runs after WHERE."},
    ], title="Quiz - SQL")


def section_data_modelling(doc):
    h1(doc, "7. Relational data modelling")
    para(doc,
         "Before you write SQL you must decide how to structure the tables. Good data modelling "
         "stores each fact once, in the right place, so the data stays consistent as it grows. "
         "The relational model organises data into tables (relations) of rows and columns, "
         "linked by keys.")

    h2(doc, "Keys")
    para(doc,
         "A primary key uniquely identifies each row in a table (e.g. customer id). A foreign "
         "key is a column in one table that references the primary key of another, creating a "
         "relationship - and the database can enforce it (you cannot insert an order for a "
         "customer that doesn't exist). A natural key is a real-world unique value (an email); "
         "a surrogate key is an artificial id (an auto-incrementing integer), usually preferred "
         "because it never changes.")
    code_block(doc,
               "CREATE TABLE customers (\n"
               "    id    INTEGER PRIMARY KEY,\n"
               "    name  TEXT NOT NULL,\n"
               "    email TEXT UNIQUE\n"
               ");\n\n"
               "CREATE TABLE orders (\n"
               "    id          INTEGER PRIMARY KEY,\n"
               "    customer_id INTEGER NOT NULL,\n"
               "    amount      REAL NOT NULL,\n"
               "    FOREIGN KEY (customer_id) REFERENCES customers (id)\n"
               ");")

    h2(doc, "Normalisation basics")
    para(doc,
         "Normalisation is the process of splitting data into related tables to remove "
         "redundancy and avoid update anomalies (where the same fact stored in many places "
         "drifts out of sync). The first three normal forms, informally:")
    bullet(doc, "1NF: each cell holds a single atomic value; no repeating groups or lists in a "
                "cell.")
    bullet(doc, "2NF: it is in 1NF and every non-key column depends on the WHOLE primary key "
                "(matters for composite keys).")
    bullet(doc, "3NF: it is in 2NF and no non-key column depends on another non-key column (no "
                "transitive dependencies).")
    para(doc,
         "Practical rule of thumb: if you find yourself repeating the same text (a customer's "
         "name on every order row), pull it into its own table and reference it by id. The "
         "trade-off: highly normalised data needs more joins to read. Analytics systems often "
         "deliberately DENORMALISE for read speed - but transactional systems normalise for "
         "correctness.")

    h2(doc, "Relationships")
    para(doc,
         "One-to-many is the most common (one customer has many orders): the 'many' side holds "
         "the foreign key. Many-to-many (students and courses) is modelled with a third "
         "'junction' table holding two foreign keys.")

    callout(doc, "Common mistakes",
            "Storing comma-separated lists in one cell (breaks 1NF and makes querying painful). "
            "Repeating descriptive data across rows instead of referencing a lookup table. No "
            "primary key, so rows can't be uniquely identified or safely updated. Foreign keys "
            "with no constraint, allowing orphaned records. Over-normalising a small read-heavy "
            "reporting table when a flat structure would be simpler.")

    quiz(doc, [
        {"q": "What is a primary key?",
         "answer": "A column (or set of columns) that uniquely identifies each row in a table.",
         "why": "No two rows may share the same primary key value, and it cannot be NULL."},
        {"q": "What does a foreign key do?",
         "options": ["Encrypts a column", "References the primary key of another table to link "
                     "them", "Sorts the table", "Creates an index automatically"],
         "answer": "B", "why": "A foreign key enforces a relationship: its value must exist as a "
                                "primary key in the referenced table."},
        {"q": "Why normalise data?",
         "answer": "To remove redundancy so each fact is stored once, preventing inconsistencies "
                   "and update anomalies.",
         "why": "Duplicated data can drift out of sync when only some copies are updated."},
        {"q": "Which violates 1NF?",
         "options": ["One value per cell", "A column storing 'red,green,blue' in one cell",
                     "A primary key", "A foreign key"],
         "answer": "B", "why": "1NF requires atomic single values; a comma-separated list is a "
                                "repeating group."},
        {"q": "How do you model a many-to-many relationship (students <-> courses)?",
         "answer": "With a third junction/bridge table holding a foreign key to each side "
                   "(student_id, course_id).",
         "why": "Each enrolment is one row, allowing any student in any number of courses."},
        {"q": "Surrogate vs natural key - which is usually preferred and why?",
         "answer": "A surrogate key (an artificial auto-increment id) is usually preferred "
                   "because it is stable and never changes, unlike natural values such as an "
                   "email.",
         "why": "Natural keys can change (people change emails), breaking references."},
    ], title="Quiz - Data modelling")


def section_http_rest(doc):
    h1(doc, "8. HTTP & REST deep dive")
    para(doc,
         "The web runs on HTTP, a request/response protocol: a client sends a request to a "
         "server, the server sends back a response. REST is a popular style for designing web "
         "APIs around 'resources' (things like users or orders) identified by URLs, manipulated "
         "with standard HTTP methods. Understanding HTTP is essential both for calling other "
         "people's APIs and for building your own.")

    h2(doc, "Methods (verbs)")
    table_from_rows(doc,
                    ["Method", "Purpose", "Idempotent?"],
                    [["GET", "Read a resource; no side effects", "Yes"],
                     ["POST", "Create a new resource / submit data", "No"],
                     ["PUT", "Replace a resource entirely", "Yes"],
                     ["PATCH", "Partially update a resource", "No (usually)"],
                     ["DELETE", "Remove a resource", "Yes"]])
    para(doc,
         "Idempotent means making the same request many times has the same effect as making it "
         "once (GET, PUT, DELETE). POST is not idempotent - posting twice usually creates two "
         "records.")

    h2(doc, "Status codes")
    table_from_rows(doc,
                    ["Range", "Meaning", "Examples"],
                    [["2xx", "Success", "200 OK, 201 Created, 204 No Content"],
                     ["3xx", "Redirection", "301 Moved, 304 Not Modified"],
                     ["4xx", "Client error (your fault)", "400 Bad Request, 401 Unauthorised, "
                      "403 Forbidden, 404 Not Found, 429 Too Many Requests"],
                     ["5xx", "Server error (their fault)", "500 Internal Error, 503 Unavailable"]])

    h2(doc, "Headers, body and auth")
    para(doc,
         "Headers carry metadata: Content-Type (e.g. application/json) describes the body's "
         "format; Authorization carries credentials; Accept states what the client wants back. "
         "The body carries the actual data (often JSON). Common auth schemes: an API key in a "
         "header, a Bearer token ('Authorization: Bearer <token>', used by OAuth2/JWT), or "
         "HTTP Basic. Always send credentials over HTTPS so they are encrypted in transit.")

    h2(doc, "Calling an API in Python")
    code_block(doc,
               "import requests\n\n"
               "resp = requests.get(\n"
               "    'https://api.example.com/orders',\n"
               "    headers={'Authorization': 'Bearer YOUR_TOKEN'},\n"
               "    params={'region': 'North', 'page': 1},\n"
               "    timeout=10,\n"
               ")\n"
               "resp.raise_for_status()      # raise on 4xx/5xx\n"
               "data = resp.json()           # parse JSON body into a dict/list\n"
               "print(resp.status_code)      # 200\n"
               "print(data)")

    h2(doc, "Pagination")
    para(doc,
         "APIs rarely return millions of rows at once; they paginate. Common schemes: "
         "offset/limit (?page=2&per_page=50), or cursor-based (the response includes a 'next' "
         "token or URL you follow). You loop, fetching pages until there are none left.")
    code_block(doc,
               "import requests\n\n"
               "results, page = [], 1\n"
               "while True:\n"
               "    r = requests.get('https://api.example.com/orders',\n"
               "                     params={'page': page, 'per_page': 100}, timeout=10)\n"
               "    r.raise_for_status()\n"
               "    batch = r.json()\n"
               "    if not batch:            # empty page -> we're done\n"
               "        break\n"
               "    results.extend(batch)\n"
               "    page += 1\n"
               "print('total fetched:', len(results))")

    callout(doc, "Common mistakes",
            "Treating a 200 status as 'data is correct' - check the body too. Forgetting to "
            "handle 4xx/5xx (always call raise_for_status() or check status_code). Hard-coding "
            "secrets/tokens in source instead of environment variables. No timeout, so a hung "
            "server freezes your program forever. Ignoring pagination and assuming the first "
            "page is all the data. Sending credentials over plain HTTP.")

    quiz(doc, [
        {"q": "Which HTTP method is the conventional choice for READING data with no side "
              "effects?",
         "options": ["POST", "GET", "DELETE", "PUT"],
         "answer": "B", "why": "GET retrieves a resource and should not change server state."},
        {"q": "What does a 404 status code mean?",
         "options": ["Server crashed", "Success", "Resource not found (client error)",
                     "Unauthorised"],
         "answer": "C", "why": "404 is a 4xx client error meaning the requested resource "
                                "doesn't exist."},
        {"q": "What does 'idempotent' mean for an HTTP method?",
         "answer": "Making the same request multiple times has the same effect as making it "
                   "once.",
         "why": "GET, PUT and DELETE are idempotent; POST generally is not."},
        {"q": "Which header tells the server the request body is JSON?",
         "options": ["Accept: text/html", "Content-Type: application/json",
                     "Authorization: Bearer", "Host:"],
         "answer": "B", "why": "Content-Type describes the format of the body being sent."},
        {"q": "A 500-range status code indicates whose problem?",
         "options": ["The client's", "The server's", "The network only", "Nobody's"],
         "answer": "B", "why": "5xx codes are server-side errors; 4xx codes are client-side."},
        {"q": "Why must an API client handle pagination?",
         "answer": "Because the server returns results in limited pages, so you must loop and "
                   "fetch subsequent pages to get the full dataset.",
         "why": "Assuming page one is everything silently loses data."},
        {"q": "Where should API tokens/secrets be stored?",
         "options": ["Hard-coded in the script", "In environment variables / a secret store",
                     "In a public repo", "In the URL query string"],
         "answer": "B", "why": "Secrets belong in environment variables or a secrets manager, "
                                "never committed to source control."},
    ], title="Quiz - HTTP & REST")


def section_fastapi(doc):
    h1(doc, "9. Building REST APIs with FastAPI")
    para(doc,
         "FastAPI is a modern Python framework for building web APIs quickly. Its key ideas: "
         "you declare routes with decorators (@app.get, @app.post); you describe request and "
         "response data with Pydantic models (Python classes with type hints); and FastAPI uses "
         "those types to validate input automatically, serialise output to JSON, and generate "
         "interactive documentation for free at /docs.")

    h2(doc, "A minimal app")
    code_block(doc,
               "# file: main.py\n"
               "from fastapi import FastAPI\n\n"
               "app = FastAPI()\n\n"
               "@app.get('/')\n"
               "def read_root():\n"
               "    return {'message': 'Hello, API'}\n\n"
               "@app.get('/health')\n"
               "def health():\n"
               "    return {'status': 'ok'}\n\n"
               "# Run it:  uvicorn main:app --reload\n"
               "# Then open http://127.0.0.1:8000/docs for interactive docs")

    h2(doc, "Path and query parameters")
    para(doc,
         "Function parameters whose names appear in the path become path parameters; the rest "
         "become query parameters. Type hints make FastAPI validate and convert them "
         "automatically (a non-integer id yields a clean 422 error).")
    code_block(doc,
               "from fastapi import FastAPI\n\n"
               "app = FastAPI()\n\n"
               "@app.get('/orders/{order_id}')\n"
               "def get_order(order_id: int, currency: str = 'GBP'):\n"
               "    # order_id from the path, currency from ?currency=...\n"
               "    return {'order_id': order_id, 'currency': currency}")

    h2(doc, "Request/response models with Pydantic")
    para(doc,
         "A Pydantic model declares the shape of your data with typed fields. Used as a "
         "function parameter, it validates and parses the incoming JSON body; used as "
         "response_model, it shapes and documents the output. Invalid input is rejected "
         "automatically with a 422 and a helpful error message - you write no validation code.")
    code_block(doc,
               "from fastapi import FastAPI\n"
               "from pydantic import BaseModel, Field\n\n"
               "app = FastAPI()\n\n"
               "class OrderIn(BaseModel):\n"
               "    customer: str\n"
               "    amount: float = Field(gt=0)        # must be > 0\n"
               "    region: str\n\n"
               "class OrderOut(BaseModel):\n"
               "    id: int\n"
               "    customer: str\n"
               "    amount_with_tax: float\n\n"
               "_db = []\n\n"
               "@app.post('/orders', response_model=OrderOut, status_code=201)\n"
               "def create_order(order: OrderIn):\n"
               "    new_id = len(_db) + 1\n"
               "    record = OrderOut(id=new_id, customer=order.customer,\n"
               "                      amount_with_tax=round(order.amount * 1.2, 2))\n"
               "    _db.append(record)\n"
               "    return record")

    callout(doc, "Common mistakes",
            "Forgetting type hints, so FastAPI can't validate or document the endpoint. "
            "Returning a non-serialisable object (return Pydantic models or dicts, not raw DB "
            "rows). Confusing path parameters (in the URL path) with query parameters "
            "(after ?). Doing slow blocking work in an endpoint without async. Not setting the "
            "right status_code (e.g. 201 for create). Putting business logic, validation and DB "
            "access all in the route function instead of separate modules.")

    quiz(doc, [
        {"q": "How do you declare a GET endpoint at /items in FastAPI?",
         "options": ["@app.route('/items')", "@app.get('/items')", "def get_items(): pass",
                     "@get('/items')"],
         "answer": "B", "why": "FastAPI uses method-specific decorators like @app.get and "
                                "@app.post."},
        {"q": "What is the role of a Pydantic model in FastAPI?",
         "answer": "It declares the typed shape of request/response data; FastAPI uses it to "
                   "validate input, serialise output to JSON, and generate docs.",
         "why": "You get automatic validation and documentation from the type hints alone."},
        {"q": "In @app.get('/orders/{order_id}') with def get(order_id: int), what is "
              "order_id?",
         "options": ["A query parameter", "A path parameter", "A header", "The request body"],
         "answer": "B", "why": "Its name appears in the URL path, so it is a path parameter."},
        {"q": "What status code does FastAPI return for a request body that fails validation?",
         "options": ["200", "404", "422", "500"],
         "answer": "C", "why": "FastAPI/Pydantic return 422 Unprocessable Entity with details "
                                "on what was invalid."},
        {"q": "What URL serves the auto-generated interactive docs by default?",
         "answer": "/docs (Swagger UI); /redoc is also provided.",
         "why": "FastAPI builds an OpenAPI schema and a UI from your routes and models."},
        {"q": "Which command runs a FastAPI app named 'app' in main.py with auto-reload?",
         "options": ["python main.py", "uvicorn main:app --reload", "fastapi run",
                     "flask run"],
         "answer": "B", "why": "uvicorn is the ASGI server; main:app points to the app object, "
                                "--reload restarts on code changes during development."},
    ], title="Quiz - FastAPI")


def section_maths_bridge(doc):
    h1(doc, "10. Maths-for-ML bridge")
    para(doc,
         "You already have the mathematics - this section connects it to code, because ML is "
         "linear algebra, calculus and probability executed at scale by NumPy and friends. We "
         "go fast on the theory and focus on the NumPy translation.")

    h2(doc, "Vectors and the dot product")
    para(doc,
         "A vector is an ordered list of numbers - in code, a 1-D NumPy array. The dot product "
         "a . b = sum of a_i * b_i is everywhere in ML: it is the core of a neuron's weighted "
         "sum, of similarity measures, and of matrix multiplication. Geometrically a . b = "
         "|a| |b| cos(theta), so it also measures alignment between vectors.")
    code_block(doc,
               "import numpy as np\n\n"
               "a = np.array([1.0, 2.0, 3.0])\n"
               "b = np.array([4.0, 5.0, 6.0])\n\n"
               "print(np.dot(a, b))        # 32.0  = 1*4 + 2*5 + 3*6\n"
               "print(a @ b)               # 32.0  - @ is the matmul/dot operator\n\n"
               "# Vector norm (length) and cosine similarity\n"
               "norm_a = np.linalg.norm(a)\n"
               "cos_sim = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))\n"
               "print(round(cos_sim, 4))   # ~0.9746  (vectors point in a similar direction)")

    h2(doc, "Matrices and matrix multiplication")
    para(doc,
         "A matrix is a 2-D array. Matrix multiplication combines two matrices where the inner "
         "dimensions match: (m x n) @ (n x p) = (m x p). A linear model's prediction over a "
         "whole dataset is one matrix multiply X @ w - this is why vectorised linear algebra is "
         "the heart of ML performance.")
    code_block(doc,
               "import numpy as np\n\n"
               "X = np.array([[1.0, 2.0],\n"
               "              [3.0, 4.0],\n"
               "              [5.0, 6.0]])     # 3 samples, 2 features  (3x2)\n"
               "w = np.array([0.5, -1.0])      # weights                (2,)\n\n"
               "predictions = X @ w            # (3x2)@(2,) -> (3,)\n"
               "print(predictions)            # [-1.5 -2.5 -3.5]\n\n"
               "print(X.T.shape)              # transpose: (2, 3)\n"
               "print((X.T @ X).shape)        # (2, 2) - appears in least squares")

    h2(doc, "Probability refresher in code")
    para(doc,
         "Probability underlies classification, loss functions and evaluation. Two ideas you'll "
         "use constantly: expectation (the mean), and turning scores into probabilities with the "
         "softmax/sigmoid functions. Here we sample, estimate, and apply softmax.")
    code_block(doc,
               "import numpy as np\n\n"
               "rng = np.random.default_rng(42)\n\n"
               "# Estimate E[X] of a fair die by simulation (should approach 3.5)\n"
               "rolls = rng.integers(1, 7, size=100_000)\n"
               "print(rolls.mean())          # ~3.5\n\n"
               "# Softmax: turn raw scores into a probability distribution\n"
               "def softmax(z):\n"
               "    z = z - z.max()          # numerical stability\n"
               "    e = np.exp(z)\n"
               "    return e / e.sum()\n\n"
               "scores = np.array([2.0, 1.0, 0.1])\n"
               "probs = softmax(scores)\n"
               "print(probs.round(3))        # e.g. [0.659 0.242 0.099]\n"
               "print(probs.sum())           # 1.0 - it's a valid distribution")

    callout(doc, "Common mistakes",
            "Confusing elementwise multiplication a * b with the dot product a @ b - they are "
            "different operations. Matrix-multiply shapes must align on the inner dimension "
            "(n must match) or NumPy raises a ValueError. Forgetting to subtract the max in "
            "softmax causes overflow (exp of large numbers). Treating probabilities that don't "
            "sum to 1 as a distribution. Mixing up a row vector and a column vector when shapes "
            "are (n,) vs (n,1).")

    quiz(doc, [
        {"q": "Compute the dot product of [1,2,3] and [4,5,6].",
         "answer": "32",
         "why": "1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32."},
        {"q": "In NumPy, what does the @ operator do between two arrays?",
         "options": ["Elementwise multiply", "Matrix multiplication / dot product",
                     "Concatenation", "Comparison"],
         "answer": "B", "why": "@ is matrix multiplication; for two 1-D arrays it gives the dot "
                                "product."},
        {"q": "For matrix multiply (m x n) @ (n x p), what must hold and what is the result "
              "shape?",
         "answer": "The inner dimensions must match (both n); the result is (m x p).",
         "why": "Each output entry is a dot product of a row of the first and a column of the "
                "second."},
        {"q": "What is the expected value of one roll of a fair six-sided die?",
         "options": ["3", "3.5", "6", "1"],
         "answer": "B", "why": "(1+2+3+4+5+6)/6 = 21/6 = 3.5."},
        {"q": "What does the softmax function produce from a vector of scores?",
         "answer": "A vector of non-negative values that sum to 1 - a probability distribution.",
         "why": "It exponentiates and normalises, turning scores into class probabilities."},
        {"q": "Why subtract the max before exponentiating in softmax?",
         "answer": "For numerical stability - it prevents exp() from overflowing on large "
                   "inputs, without changing the result.",
         "why": "Subtracting a constant cancels in the normalisation."},
        {"q": "Geometrically, a.b = |a||b|cos(theta). If two unit vectors are orthogonal, "
              "their dot product is?",
         "options": ["1", "0", "-1", "Undefined"],
         "answer": "B", "why": "cos(90 degrees) = 0, so orthogonal vectors have dot product 0."},
    ], title="Quiz - Maths-for-ML bridge")


# ===================================================================== EXERCISES

def exercises(doc):
    h1(doc, "Exercises")
    para(doc,
         "Work through these in order; each builds on the last and increases in difficulty. "
         "Commit your solution to Git after each one, write at least one pytest test where it "
         "makes sense, and keep your code in a tidy repo.")
    numbered(doc,
             "Warm-up (Advanced Python): Given a list of integers, use a single comprehension "
             "to build a list of the squares of only the even numbers. Then rewrite it as a "
             "generator expression and sum it.")
    numbered(doc,
             "Decorator + tests: Write a decorator @retry that re-runs a function up to 3 times "
             "if it raises an exception, then succeeds or re-raises. Write pytest tests proving "
             "it retries and eventually gives up.")
    numbered(doc,
             "NumPy: Without using a Python loop, create a 5x5 multiplication table as a NumPy "
             "array using broadcasting, then compute its row sums and column means.")
    numbered(doc,
             "Pandas cleaning: Load a messy CSV (missing values, stray whitespace, mixed-case "
             "categories, a numeric column stored as text). Clean every issue and print before/"
             "after row counts and dtypes.")
    numbered(doc,
             "Pandas analysis + chart: From the cleaned data, use groupby to find the top 5 "
             "categories by total value, then plot them as a labelled bar chart saved to PNG.")
    numbered(doc,
             "SQL: Load the same data into SQLite. Write queries for (a) total per category, "
             "(b) the categories above the overall average, using a subquery, and (c) a JOIN "
             "across two related tables. Add an index and describe what it speeds up.")
    numbered(doc,
             "Data modelling: Design a 3-table schema (e.g. customers, orders, products with a "
             "junction table) in 3NF. Draw the relationships, write the CREATE TABLE statements "
             "with primary and foreign keys, and justify each key.")
    numbered(doc,
             "FastAPI: Build a small API with GET /categories (list) and GET "
             "/categories/{name}/total (one aggregate), backed by your cleaned data. Use a "
             "Pydantic response model, return correct status codes, and test it with the /docs "
             "page and one pytest test using FastAPI's TestClient.")


# ===================================================================== PROJECT

def project_brief(doc):
    h1(doc, "Project brief - Insights API")
    lead(doc, "Goal:",
         "Take a real-ish CSV dataset, clean and analyse it with Pandas to produce genuine "
         "insights and a chart, then expose those results as JSON through a FastAPI service. "
         "This mirrors a real entry-level data/backend task end to end.")

    h2(doc, "Part A - Data analysis")
    bullet(doc, "Choose a real-ish public CSV (e.g. a Kaggle dataset, a government open-data "
                "CSV, or the classic Titanic / NYC taxi / retail sales sets).")
    bullet(doc, "Load it with Pandas; document its shape, columns and dtypes.")
    bullet(doc, "Clean it: handle missing values, fix types, remove duplicates, standardise "
                "text. Record every cleaning step.")
    bullet(doc, "Compute at least three non-trivial insights using groupby and at least one "
                "merge/join (split the data into two tables if needed).")
    bullet(doc, "Produce at least two labelled matplotlib charts saved as PNG.")

    h2(doc, "Part B - FastAPI service")
    bullet(doc, "Expose the cleaned/aggregated results through a FastAPI app.")
    bullet(doc, "Provide at least: GET /summary (overall stats), GET /groups (the groupby "
                "results), and GET /groups/{key} (one group's detail).")
    bullet(doc, "Use Pydantic response models, correct status codes, and a 404 for unknown "
                "keys.")
    bullet(doc, "Include the interactive /docs and at least three pytest tests using "
                "TestClient.")

    h2(doc, "Requirements checklist")
    bullet(doc, "Clean, modular code: separate data-loading/cleaning, analysis and API layers.")
    bullet(doc, "A README explaining the dataset, how to run the analysis, and how to start the "
                "API.")
    bullet(doc, "Everything in Git with meaningful commits; a requirements.txt or equivalent.")
    bullet(doc, "Tests pass with a single 'pytest' command.")

    h2(doc, "Milestones")
    table_from_rows(doc,
                    ["Week", "Milestone", "Deliverable"],
                    [["1", "Data acquired & cleaned",
                      "Notebook/script that loads and cleans the CSV; documented steps"],
                     ["2", "Analysis & charts",
                      "groupby + join insights and 2+ saved PNG charts"],
                     ["3", "API built",
                      "FastAPI app with the three endpoints and Pydantic models"],
                     ["4", "Tested & documented",
                      "pytest suite passing, README, tidy Git history, final demo"]])

    h2(doc, "Grading rubric")
    table_from_rows(doc,
                    ["Criterion", "Weight", "What 'excellent' looks like"],
                    [["Data cleaning", "20%",
                      "All issues handled correctly; steps documented and justified"],
                     ["Analysis & insight", "20%",
                      "3+ correct, meaningful insights using groupby and a join"],
                     ["Visualisation", "10%",
                      "Clear, fully labelled, well-chosen charts saved to file"],
                     ["API design", "20%",
                      "Sensible REST routes, Pydantic models, correct status codes incl. 404"],
                     ["Testing", "15%",
                      "Meaningful pytest tests (incl. TestClient) all passing"],
                     ["Code quality & Git", "10%",
                      "Modular, readable code; clean commits; clear README"],
                     ["Stretch", "5%",
                      "Pagination, SQLite storage, env-var config, or deployment"]])

    callout(doc, "Stretch goals",
            "Store the cleaned data in SQLite and have the API query it with SQL. Add pagination "
            "to /groups. Read configuration from environment variables. Add an /docs link in the "
            "README and deploy the API somewhere free.", color=GREEN)


# ===================================================================== RESOURCES

def resources(doc):
    h1(doc, "Resources")
    para(doc, "All free or low-cost and widely respected. Search the names; avoid paywalled "
              "courses where a free official doc exists.")
    lead(doc, "Automate the Boring Stuff with Python (Al Sweigart):",
         "Free online book; excellent for consolidating practical Python.")
    lead(doc, "Official Python tutorial (docs.python.org):",
         "The authoritative reference for comprehensions, generators and decorators.")
    lead(doc, "pytest official documentation:",
         "Clear guides on fixtures, parametrisation and assertions.")
    lead(doc, "NumPy 'Absolute Beginners' guide (official docs):",
         "The best free introduction to arrays, vectorisation and broadcasting.")
    lead(doc, "pandas official documentation - '10 minutes to pandas' and the User Guide:",
         "Concise, accurate, example-driven.")
    lead(doc, "Kaggle Learn (free micro-courses):",
         "Short hands-on courses on Pandas, data visualisation and SQL with real datasets.")
    lead(doc, "SQLBolt and Mode Analytics SQL Tutorial:",
         "Free interactive SQL lessons from SELECT through joins and aggregations.")
    lead(doc, "FastAPI official documentation:",
         "Outstanding, beginner-friendly tutorial that takes you from hello-world to "
         "production patterns.")
    lead(doc, "3Blue1Brown 'Essence of Linear Algebra' (YouTube):",
         "Free video series that builds visual intuition for vectors and matrices.")


if __name__ == "__main__":
    build()
