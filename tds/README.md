# Tools in Data Science (TDS)

Notes, solved assignments and runnable artifacts for **TDS, Sep 2026 term** (IITM BS Diploma).

TDS is not a maths course, so these notes deliberately depart from the
*intuition → formulas → worked example* shape used on the `mlt` branch. A TDS
question is a **tool + a grader**, so every note here follows:

> problem → how it is actually graded → solution → verification → traps

That shape exists because of the single most useful thing learned in this course:
**the grader is a program, and conforming to its contract is part of the answer.**

## 🗂️ Contents

| File | What's in it |
|---|---|
| [`00-course-overview.md`](00-course-overview.md) | Course structure, grading split, weekly topics, strategy |
| [`cheat-sheet.md`](cheat-sheet.md) | Command/API recall: `uv`, bash, git, FastAPI, CORS, Vercel, AI Pipe, ngrok, JWT, dbt |
| [`ga0/`](ga0/) | Graded Assignment 0: a guide per question (how it's graded, what we did and why) |
| [`ga0/solutions/`](ga0/solutions/) | GA0 files we submitted or ran (HTML, SQL, scripts, ngrok policy) |
| [`ga1/`](ga1/) | Graded Assignment 1: grader map, what decided each question, and why |
| [`ga1/helpers/`](ga1/helpers/) | GA1 scripts: JSON repair, file reorganise, cosine ranking, two-model prompt tester, tangram solver |
| [vercel-deploys](https://github.com/sreekarsarma55/vercel-deploys) | Separate repo: the FastAPI app behind every live-endpoint question (GA0 Q5/Q10/Q11/Q25, GA1 Q6/Q14/Q15) |

## ⚠️ How TDS grading actually works

The GA quizzes are served from `https://exam.sanand.workers.dev/<quiz-id>`. The page
loads `exam.js`, which lazily imports a per-quiz module (`exam-<quiz-id>.js`)
containing **every question's validator, expected value and hidden test data**.

Consequences worth internalising:

1. Most questions are graded **client-side** by a JavaScript function, not by a human
   and not by an LLM. It checks regexes, tolerances and exact strings.
2. Several questions are **seeded from your email**, so the assigned variant and the
   sampled test cases are deterministic — the same every time you press Check.
3. The assignment explicitly permits this: *"It's hackable. Hacking is allowed."*
   Reading the validator is therefore the intended difficulty, not a workaround.

The productive loop is: **read the validator → reproduce it offline → verify → submit once.**

**From GA1 on, most checks moved to the server.** The browser still *builds* each question's data
from the seed, but sends your answer to `POST /backendVerify` for the verdict. That endpoint returns
the same result as the Check button (it records nothing; only Save does), so the loop becomes:
**rebuild the data offline → compute → confirm with the exact payload Check sends → Save.**
Live-endpoint questions (MCP server, ledger agent, config service) are re-graded on every Check,
so the deployment must stay up until the deadline.

## 📈 Status

| Assignment | Score | Notes |
|---|---|---|
| GA0 | all 25 questions green and saved (35.5 marks) | [`ga0/README.md`](ga0/README.md): question-by-skill table, method, recurring traps |
| GA1 | **22 / 22**, saved 9 Oct 2026 (due 18 Oct) | [`ga1/README.md`](ga1/README.md): what changed (server-side grading), per-question notes |

Hardest lessons so far: browsers hide non-safelisted headers from JS (GA0 Q18/Q25), lossy WebP
decodes differ per tool (GA0 Q14), and a mirrored y-axis made a tangram fit look right to within
1 px but never match exactly (GA1 Q16).

---

_Part of [sreekarsarma55/notes](https://github.com/sreekarsarma55/notes). Subject branch: `tds`._
