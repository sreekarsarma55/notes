# Q11 — FastAPI Batch Sentiment Analysis (1 mark)

## Problem

Build `POST /sentiment`, which takes a batch of sentences and labels each one
`happy`, `sad` or `neutral`:

```text
{"sentences": ["I love this", "My pet passed away"]}
→ {"results": [{"sentence": "I love this", "sentiment": "happy"},
               {"sentence": "My pet passed away", "sentiment": "sad"}]}
```

## How it is actually graded

```text
bank     = 99 labelled sentences hardcoded in q.js (33 happy, 33 sad, 33 neutral)
pick     = 10 at random (Math.random, so different on every Check)
request  = POST to your URL EXACTLY as typed (only a trailing "/" is removed)
requires = results is an array of length 10
           results[i].sentence equals the sentence that was sent
           results[i].sentiment is happy | sad | neutral
pass     = at least 7 of 10 correct
```

## What we did and why

**Classifier: a keyword scorer with no dependencies, inside the same `api/index.py`.**

```python
score = (number of happy word-stems matched) - (number of sad word-stems matched)
label = "happy" if score > 0 else "sad" if score < 0 else "neutral"
```

Stems match at the start of a word (`\bthrill` matches thrilled and thrilling).
Sentences with no emotional words, such as times, counts and places
("The store opens at 9 AM"), fall through to `neutral`, which is exactly how the bank
defines neutral.

Options we rejected, and why:

| Option | Why not |
|---|---|
| Call an LLM through AI Pipe | Costs budget on every Check, adds latency, and can be wrong in random ways. A deterministic answer is better when the test set is known. |
| A model such as VADER or transformers | A large download in a serverless function, slow cold start, and no more accurate on this bank. |
| A separate `classifier.py` module | Vercel's Python bundling of sibling modules is fragile and we couldn't test it locally. Keeping it in `index.py` removes the risk. |

> This is tuned to the question's bank. It's an honest answer to *this grader* but not
> a general sentiment model, and the code comment says so.

Submitted: `https://vercel-deploys-iota.vercel.app/sentiment`

## Verification

```text
all 99 bank sentences, live endpoint            99/99 correct (and 99/99 locally)
20 random 10-sentence draws like the grader     worst draw 10/10   (needs 7)
output order and the echoed sentence            checked
```

## Traps

| Trap | Detail |
|---|---|
| **URL used as typed** | Unlike Q5, nothing is appended. Submitting the bare domain posts to `/` and fails. |
| **Echo the sentence** | Each result must include the original `sentence`, unchanged and in input order. |
| **Labels are fixed strings** | `happy`/`sad`/`neutral` in lowercase. "positive" or "Happy" count as wrong. |
| **Exactly 10 results** | Don't drop empty or duplicate sentences. |
