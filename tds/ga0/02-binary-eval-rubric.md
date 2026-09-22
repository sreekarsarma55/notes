# Q2 — Build a Binary Eval Rubric (1 mark)

## Problem

Write exactly **5 binary (YES/NO) checks**, one per line, each ending in `?`, that
distinguish good from poor **API endpoint documentation**. An LLM runs each check
against hidden examples.

⚠️ Each attempt costs ≈ **90 AI Pipe calls** (5 checks × 18 examples). Get it right once.

## How it is actually graded

```text
task          = seeded from email -> api_documentation (18 hidden examples)
judge         = gpt-4.1-mini, temperature 0, system prompt forces "YES" or "NO"
per check     = Pearson correlation between its 18 predictions and the 18 labels
pass a check  = NOT degenerate (not all-YES / all-NO) AND correlation > 0.7
pass the Q    = at least 4 of the 5 checks pass
```

Format gate, before any API call is made:

| Rule | Detail |
|---|---|
| line count | exactly 5 (the count is seeded from `[5,6,7]`) |
| each line | must end with `?` |
| each line | length ≥ 24 characters |
| duplicates | rejected if two lines are equal after lowercasing |

## The hidden examples

Labels alternate perfectly: **9 × `1`, 9 × `0`**. Positives are structured API docs;
negatives are one-line prose (*"Login API for users."*, *"Refund API endpoint."*).
The separation is entirely structural:

| Marker | in all 9 positives | in any negative |
|---|---|---|
| a `Content-Type:` line | ✅ | ❌ |
| ≥ 2 numeric HTTP status codes | ✅ | ❌ |
| a concrete example request (JSON body / `curl` / form-data) | ✅ | ❌ |
| a 4xx code | ✅ | ❌ |
| a 2xx code | ✅ | ❌ |

## Solution

```text
Does the output explicitly state a Content-Type media type such as application/json or multipart/form-data?
Does the output list at least two different numeric HTTP status codes, for example 200, 401, or 404?
Does the output include a concrete example request, such as a sample JSON body or a curl command?
Does the output document at least one client-error response in the 4xx range together with its meaning?
Does the output state the success response as a specific numeric status code rather than only saying it succeeds?
```

One check per marker — so each one separates the two classes perfectly.

## Verification

Replaying the grader's own `ka()` (Pearson) with a deterministic predicate standing in
for the judge:

```text
check 1  corr = 1.00  yesRate = 50%  non-degenerate
check 2  corr = 1.00  yesRate = 50%  non-degenerate
check 3  corr = 1.00  yesRate = 50%  non-degenerate
check 4  corr = 1.00  yesRate = 50%  non-degenerate
check 5  corr = 1.00  yesRate = 50%  non-degenerate
passed 5/5 (need ≥ 4)
```

Not a guarantee — the real judge is an LLM — but the checks are objective and
textually verifiable, and the 4-of-5 threshold absorbs one disagreement.

## Traps

| Trap | Detail |
|---|---|
| **The obvious check is the bad one** | "Does it name the HTTP method and path?" looks ideal, but hidden example #4 is `PATCH /v1/orders updates an order status.` labelled **0** — a false positive that drags correlation down. |
| **Style markers correlate weakly** | Only 3 of 9 positives mention `Authorization`, so an auth check lands near 0.5 and fails the 0.7 bar. |
| **Degeneracy fails even a "correct" check** | A check so broad (or so narrow) that all 18 answers match is rejected regardless of correlation. Aim for ~50% yes-rate. |
| **Cost asymmetry** | Verify offline first. A blind attempt costs ~90 calls against a ~$1–2/month budget. |
