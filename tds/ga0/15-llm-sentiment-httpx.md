# Q15 — LLM Sentiment Analysis (1 mark)

## Problem

Write Python that uses `httpx` to send a seeded piece of meaningless text to OpenAI's
chat completions API with `gpt-4o-mini`. The system message asks for the sentiment
as `GOOD`, `BAD` or `NEUTRAL`. Use a dummy API key; the code is never run against
OpenAI.

## How it is actually graded

Your code runs **in the browser in Pyodide**, with `httpx` swapped for a fake that
records the call:

```text
sys.modules["httpx"] = MockHttpx()      # post() records method, url, json=, headers=
exec(your code)

checks, in order:
  method == POST
  url ends with /v1/chat/completions
  headers has "Authorization"
  body passed as json=  (NOT data= or content=)
  json.model == "gpt-4o-mini"
  exactly 2 messages: [system, user]
  system content contains GOOD, BAD and NEUTRAL
  user content .trim() == the seeded text exactly
```

## What we did and why

[`solutions/q15-httpx-sentiment.py`](solutions/q15-httpx-sentiment.py):

```python
import httpx
TEXT = "5Zj3G 4HTa9 9F4FxQ jThMKFwixCXZJoWXN JVVst1C5N4Lpg"   # seeded for this email
response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": "Bearer dummy-api-key"},
    json={"model": "gpt-4o-mini", "messages": [
        {"role": "system", "content": "Analyze the sentiment ... exactly one of: GOOD, BAD, or NEUTRAL."},
        {"role": "user", "content": TEXT}]},
)
response.raise_for_status()
print(response.json()["choices"][0]["message"]["content"])
```

| Choice | Why |
|---|---|
| Module-level `httpx.post(...)` | The fake only replaces the module-level `post`. `httpx.Client()` doesn't exist on the fake. |
| `json=` keyword | The fake's signature is `post(url, json=None, headers=None, **kw)`. `data=` lands in `**kw` and the body looks empty. |
| No `async` / `asyncio.run` | Pyodide runs the code once at the top level; a coroutine that's never awaited sends nothing. |
| Copy the seeded text exactly | It's compared after `.trim()` only. One wrong character fails it. |
| `raise_for_status()` | Good practice; the fake supports it. |

## Verification

```text
rebuilt the grader's MockHttpx in local Python and ran the answer   all checks pass
seeded text regenerated from seedrandom(email#q-llm-sentiment-analysis)   matches the page
quiz                                                                 green
```

## Traps

| Trap | Detail |
|---|---|
| **`httpx.Client` / `AsyncClient`** | Not on the fake, so you get an AttributeError. |
| **Real API key** | Never needed. Don't paste a real token into a graded text box. |
| **Base URL** | Any host works if the path ends in `/v1/chat/completions`. |
| **Extra messages** | A third message (e.g. a few-shot example) fails the 2-message check. |
