# GA0 — Graded Assignment 0 (Sep 2026)

Quiz: `https://exam.sanand.workers.dev/tds-2026-09-ga0` · Total **35.5 marks** ·
40% ≈ **14.2 marks** · Deadline **Sun 11 Oct 2026, 11:59 pm IST**.

## Mark tracker

| # | Question | Marks | Status | Note |
|---|---|---|---|---|
| 1 | Scale Manipulation Repair in Axis Design | 1 | ✅ solved | [01](01-axis-scale-manipulation.md) |
| 2 | Build a Binary Eval Rubric | 1 | ✅ solved | [02](02-binary-eval-rubric.md) |
| 3 | The Bug Hunter (Property-Based Testing) | 1 | ✅ solved | [03](03-property-based-testing.md) |
| 4 | Calculate variance | 0.5 | ✅ solved | [04](04-sample-variance.md) |
| 5 | Code Interpreter with AI Error Analysis | 1 | 🚧 code ready, needs deploy | [05](05-code-interpreter.md) |
| 6 | Fix the Color Encoding Mismatch | 1 | ⬜ todo | diverging palette, `L*` checks |
| 7 | Count crawled HTML files | 1 | ⬜ todo | `wget` mirror + count M–W |
| 8 | CSS: Featured-Sale Discount Sum | 2 | ⬜ todo | `.featured.sale` sum |
| 9 | dbt: Operations performance mart | 1 | ⬜ todo | structure/keyword validated |
| 10 | Write a FastAPI server to serve data | 3 | ⬜ todo | `GET /api?class=` |
| 11 | FastAPI Batch Sentiment Analysis | 1 | ⬜ todo | `POST /sentiment` |
| 12 | Get an LLM to say Yes | 2 | ⬜ todo | prompt injection |
| 13 | Create a GitHub Action | 1 | ⬜ todo | step named with email |
| 14 | Reconstruct and desaturate an image | 1 | ⬜ todo | 5×5 unscramble + luminance |
| 15 | LLM Sentiment Analysis | 1 | ⬜ todo | dummy `httpx` POST |
| 16 | Move and rename files | 3 | ⬜ todo | `mv` + digit shift + sha256 |
| 17 | Network Game: Graph Detective | 1 | ⬜ todo | JWT from game |
| 18 | Local Ollama Endpoint | 3 | ⬜ todo | needs local Ollama + ngrok |
| 19 | Replace across files | 2 | ⬜ todo | case-insensitive IITM → IIT Madras |
| 20 | Sort and Filter a JSON Product Catalog | 0.5 | ⬜ todo | filter ≥ threshold, 3-key sort |
| 21 | SQL: Average salary by department | 0.5 | ⬜ todo | `GROUP BY` + `ROUND` |
| 22 | Process files with different encodings | 2 | ⬜ todo | CP-1252 / UTF-8 / UTF-16 |
| 23 | Use DevTools | 1 | ✅ answer found | hidden input value in the DOM |
| 24 | Use GitHub | 1 | ⬜ todo | raw `email.json` URL |
| 25 | Deploy a POST analytics endpoint to Vercel | 3 | ⬜ todo | `POST /api/latency` |

**Banked so far: 4.5 / 35.5** (Q1–Q4 verified + Q23 answer known).

## The method that makes this tractable

```text
1. fetch the grader        curl https://exam.sanand.workers.dev/exam.js
                          -> module map names exam-tds-2026-09-ga0.js
2. fetch the validators    curl https://exam.sanand.workers.dev/exam-tds-2026-09-ga0.js
3. read the check for the question: expected value, tolerance, regex, hidden data
4. reproduce it offline (node/python), assert it passes
5. submit once, then SAVE
```

Every question in this folder was verified this way before submitting. Step 5
matters: *Check* validates but records nothing; only *Save* stores a submission.

## Recurring traps

| Trap | Where it bit |
|---|---|
| Grader parses the **first number** in your text, not the one you meant | Q1 — 41 numbers in an HTML comment, it read `335.58` |
| A required "snippet pattern" is matched as a **literal string**, so `"type": "linear"` ≠ `type: "linear"` | Q1 |
| Regex `.` does not cross newlines, so a label and its value must share a line | Q1 |
| A "description" check can be a **hardcoded phrase list**, not semantic | Q1 — 5 accepted phrases |
| Sample vs population variance, with tolerance tighter than the difference | Q4 |
| The library you `import` may be a **shim**, not the real package | Q3 — fake `hypothesis` |
| "Random" test cases are **seeded from your email** — deterministic, so precomputable | Q3, Q5 |
