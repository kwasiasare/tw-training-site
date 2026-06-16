---
title: Building UIs with Streamlit
month: 4
monthTitle: Portfolio Projects
lesson: 7
summary: Turn your Python scripts into shareable web apps with Streamlit — no HTML, CSS, or JavaScript
  required.
objectives:
- Understand what Streamlit is and why it suits data and AI portfolios
- Install Streamlit and run an app with streamlit run
- Display text, data, and charts with st.write, st.dataframe, and st.line_chart
- Collect user input using widgets like st.text_input, st.slider, and st.button
- Understand Streamlit's rerun model and use st.session_state to keep state
- Wire a Claude API call into an interactive app with secrets kept safe
- Cache slow work with st.cache_data so the app stays fast
video: m4-l07-streamlit.mp4
quiz:
- q: How do you start a Streamlit app from the terminal?
  options:
  - python app.py
  - streamlit run app.py
  - streamlit start app.py
  - run streamlit app.py
  answer: 1
  why: Streamlit apps launch with the command streamlit run app.py, which opens the app in your browser.
- q: What happens every time a user interacts with a widget in Streamlit?
  options:
  - Only that widget updates
  - Nothing until you click Submit
  - The whole script reruns top to bottom
  - The page reloads from the server cache
  answer: 2
  why: Streamlit reruns the entire script on every interaction — this simple model is why st.session_state
    and caching matter.
- q: Which object keeps values alive across reruns?
  options:
  - st.cache_data
  - st.session_state
  - st.global
  - st.memory
  answer: 1
  why: st.session_state is a dictionary-like store that persists across reruns for a single user session.
- q: Why should you put your Anthropic API key in .streamlit/secrets.toml or an environment variable instead
    of in the code?
  answer: So the secret key is never hard-coded or pushed to GitHub, keeping it private and out of version
    control.
  why: Hard-coded keys leak when you share or commit code; secrets files and env vars keep credentials
    separate and gitignored.
- q: What does st.cache_data do?
  answer: It stores the result of an expensive function so repeated runs with the same inputs return instantly
    instead of recomputing.
  why: Because the script reruns on every interaction, caching avoids repeating slow work like loading
    data or calling an API.
- q: Which function would you use to show a pandas DataFrame as an interactive table?
  options:
  - st.text
  - st.dataframe
  - st.print
  - st.table_view
  answer: 1
  why: st.dataframe renders a scrollable, sortable interactive table; st.table renders a simpler static
    one.
resources:
- label: Streamlit — Get started (official docs)
  url: https://docs.streamlit.io/get-started
- label: Streamlit API reference
  url: https://docs.streamlit.io/develop/api-reference
- label: Streamlit Community Cloud — deploy your app for free
  url: https://streamlit.io/cloud
- label: Anthropic — Python SDK and Messages API
  url: https://docs.anthropic.com/en/api/messages
---

## Why Streamlit?

You have written scripts and notebooks that do clever things — but a recruiter cannot run a `.py` file. **Streamlit** turns a plain Python script into a web app you can share with a link. No HTML, CSS, or JavaScript needed: you write Python, Streamlit draws the page.

For an AI portfolio this is gold. A working, clickable app that calls a model is far more persuasive than a screenshot.

## Install and run

Streamlit installs with pip. You launch an app with the `streamlit run` command — not plain `python`.

```bash
pip install streamlit
streamlit run app.py
```

This opens your app in the browser, usually at http://localhost:8501, and reloads automatically when you save the file.

## Display and input

Every widget is a function. `st.write` shows almost anything; `st.dataframe` shows a table; input widgets return the user's value.

```python
import streamlit as st

st.title("My first app")
name = st.text_input("Your name")
if st.button("Greet"):
    st.write(f"Hello, {name}!")
```

## The rerun model

Here is the one idea that confuses everyone: **every interaction reruns the whole script from top to bottom**. A button click, a slider drag — the entire file runs again. To remember values between runs, use `st.session_state`, a dictionary that survives reruns.

```python
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("Add one"):
    st.session_state.count += 1
st.write("Count:", st.session_state.count)
```

## Calling Claude from your app

Keep your key in an environment variable (`ANTHROPIC_API_KEY`) or `.streamlit/secrets.toml` — never in the code. Because the script reruns often, wrap slow or paid work carefully and only call the model on a button press.

```python
import streamlit as st
from anthropic import Anthropic

client = Anthropic()
prompt = st.text_area("Ask Claude")
if st.button("Send"):
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    st.write(msg.content[0].text)
```

## Cache the slow parts

Loading a big CSV or computing a chart on every rerun is wasteful. Decorate the function with `@st.cache_data` and Streamlit reuses the result when inputs do not change.

```python
@st.cache_data
def load_data(path):
    return pd.read_csv(path)
```

## Your task

Take a script from an earlier lesson and **wrap it in a Streamlit app** with at least one input widget and one output. Bonus: deploy it free on Streamlit Community Cloud.
