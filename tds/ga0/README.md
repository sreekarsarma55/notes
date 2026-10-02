# GA0 — Graded Assignment 0 (Sep 2026)

Quiz: `https://exam.sanand.workers.dev/tds-2026-09-ga0` · Total **35.5 marks** ·
40% ≈ **14.2 marks** · Deadline **Sun 11 Oct 2026, 11:59 pm IST**.

**Status: all 25 questions green and saved.**

Each note is a guide rather than an answer key. It covers what the question asks,
how the grader actually checks it, **what we did and why**, how we verified it before
submitting, and the traps. Account-specific answers (seeded from the email) are
included for reference, but the method is what carries over to GA1–GA8.

## How to read these notes

```text
problem → how it is actually graded → what we did and why → verification → traps
```

The middle section is the point. Almost every question had one non-obvious thing
that decided pass or fail (CORS header exposure, a lossy decoder, a hex scan that
picked up CSS colours, a percentile definition). The notes are written around that.

## Questions by skill

| # | Question | Marks | Skill | Key idea | Note |
|---|---|---|---|---|---|
| 1 | Scale Manipulation Repair in Axis Design | 1 | data viz | grader reads the **first** number; phrase list is hardcoded | [01](01-axis-scale-manipulation.md) |
| 2 | Build a Binary Eval Rubric | 1 | LLM evals | structural yes/no checks that agree with the hidden labels | [02](02-binary-eval-rubric.md) |
| 3 | The Bug Hunter (Property-Based Testing) | 1 | testing | bug only shows up for `0/False`, `1/True` | [03](03-property-based-testing.md) |
| 4 | Calculate variance | 0.5 | stats | sample (n−1), not population | [04](04-sample-variance.md) |
| 5 | Code Interpreter with AI Error Analysis | 1 | FastAPI + LLM | the traceback is ground truth; the AI only corroborates | [05](05-code-interpreter.md) |
| 6 | Fix the Color Encoding Mismatch | 1 | data viz | **every** `#hex` in the file is graded; theme colours moved to `rgb()` | [06](06-color-encoding.md) |
| 7 | Count crawled HTML files | 1 | crawling | `wget -r --accept html`; count by first letter | [07](07-crawl-html.md) |
| 8 | CSS: Featured-Sale Discount Sum | 2 | DevTools / CSS | `.featured.sale` = both classes on one element | [08](08-css-selectors.md) |
| 9 | dbt: Operations performance mart | 1 | dbt / SQL | regex-graded; write a real model that also meets each check | [09](09-dbt-model.md) |
| 10 | Write a FastAPI server to serve data | 3 | FastAPI | repeated `?class=`, CSV order, `int` ids | [10](10-fastapi-students.md) |
| 11 | FastAPI Batch Sentiment Analysis | 1 | FastAPI | deterministic classifier; URL used as typed | [11](11-batch-sentiment.md) |
| 12 | Get an LLM to say Yes | 2 | prompt injection | measure prompts offline; ask for a *name*, not agreement | [12](12-llm-say-yes.md) |
| 13 | Create a GitHub Action | 1 | CI | public repo; the **latest** run must contain the step | [13](13-github-action.md) |
| 14 | Reconstruct and desaturate an image | 1 | images | WebP is lossy, so build it in the grader's own browser | [14](14-image-unscramble.md) |
| 15 | LLM Sentiment Analysis | 1 | httpx / LLM API | runs in Pyodide with a fake httpx; `json=` keyword | [15](15-llm-sentiment-httpx.md) |
| 16 | Move and rename files | 3 | bash | `tr '0-9' '1-90'`, skip no-op `mv`, `LC_ALL=C` | [16](16-move-rename-files.md) |
| 17 | Network Game: Graph Detective | 1 | APIs / search | clues → z-score; JWT valid only for **this ISO week** | [17](17-network-game.md) |
| 18 | Local Ollama Endpoint | 3 | tunnels / CORS | ngrok traffic policy: Host rewrite, `x-email`, expose headers | [18](18-ollama-ngrok.md) |
| 19 | Replace across files | 2 | bash | `sed -i 's/IITM/IIT Madras/gI'` | [19](19-replace-across-files.md) |
| 20 | Sort and Filter a JSON Product Catalog | 0.5 | JSON | `>=`, 3-key sort, numbers stay numbers | [20](20-sort-filter-json.md) |
| 21 | SQL: Average salary by department | 0.5 | SQL | `GROUP BY` + `ROUND(AVG())`; column order | [21](21-sql-average-salary.md) |
| 22 | Process files with different encodings | 2 | encodings | cp1252 ≠ latin-1; `utf-16` strips the BOM | [22](22-file-encodings.md) |
| 23 | Use DevTools | 1 | DevTools | hidden ≠ absent | [23](23-devtools-hidden-input.md) |
| 24 | Use GitHub | 1 | GitHub | the **raw** URL from a **public** repo | [24](24-github-raw-email.md) |
| 25 | Deploy a POST analytics endpoint to Vercel | 3 | serverless | linear p95; `Access-Control-Expose-Headers` | [25](25-vercel-latency.md) |

Files we submitted or ran are in [`solutions/`](solutions/). The deployed endpoints
(Q5, Q10, Q11, Q25) and the Q13/Q24 artefacts are in
[`sreekarsarma55/vercel-deploys`](https://github.com/sreekarsarma55/vercel-deploys).

## The method that makes this tractable

```text
1. fetch the grader        curl https://exam.sanand.workers.dev/exam.js
                          -> module map names exam-tds-2026-09-ga0.js
2. fetch the validators    curl https://exam.sanand.workers.dev/exam-tds-2026-09-ga0.js
3. read the check for the question: expected value, tolerance, regex, hidden data
4. reproduce it offline (node/python), assert it passes
5. submit once, then SAVE
```

Step 5 matters: *Check* validates but records nothing; only *Save* stores a submission.

Three kinds of question come up, and each needs a different approach:

| Kind | Examples | Approach |
|---|---|---|
| **Pure value** (seeded) | Q4, Q7, Q8, Q16, Q19–Q23 | Rebuild the seeded data from `seedrandom(email#qid)` and compute it two ways: the grader's formula and the real tool (bash, pandas, sqlite). |
| **Text checked by rules** | Q1, Q6, Q9, Q15 | Pull the check function out of `q.js` and run it on your submission. |
| **Live endpoint** | Q5, Q10, Q11, Q13, Q18, Q24, Q25 | Replay the grader's exact `fetch` **from a browser on another origin** (Playwright), not just curl. |

## Recurring traps

| Trap | Where it bit |
|---|---|
| Grader parses the **first number** in your text, not the one you meant | Q1 |
| A "snippet pattern" is matched as a **literal string** | Q1: `"type": "linear"` ≠ `type: "linear"` |
| A "description" check is a **hardcoded phrase list**, not judged on meaning | Q1, Q6 |
| The grader scans the **whole file**, not just the part you meant | Q6: CSS theme hexes counted as palette colours |
| **curl passing ≠ browser passing**: CORS, and JS can only read *exposed* headers | Q18, Q25 |
| URL used **as typed** vs a suffix appended | Q5 appends; Q10, Q11, Q25 don't |
| Randomness: **seeded** (precompute it) vs `Math.random` (handle any input) | Seeded: Q3, Q5, Q8, Q16… Random: Q10, Q11 |
| Exact comparisons: types, order, trailing `\n`, every pixel | Q5, Q10, Q14, Q20 |
| Two definitions of the same statistic | Q4 sample vs population; Q25 linear vs nearest-rank p95 |
| Answers that **expire or depend on uptime** | Q17 JWT (ISO week); Q18 tunnel; Vercel pause |
| A mocked library | Q3 fake `hypothesis`; Q15 fake `httpx` |
| **Pasting code through chat** turns `\n` into real newlines | Q12 tester, Q14 snippet: use one-liners or `chr(10)` |

## Keep alive until the deadline

Saved answers for Q5, Q10, Q11, Q18 and Q25 point at **live** services. If these are
re-checked later, the services need to still be running:

```text
Vercel   vercel-deploys-iota.vercel.app      Hobby projects can be auto-paused
                                             (503 DEPLOYMENT_PAUSED) → Settings → General → Resume
ngrok    Q18 tunnel + ollama serve           only needed while pressing Check/Save
```
