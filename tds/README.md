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
| [`cheat-sheet.md`](cheat-sheet.md) | Command/API recall: `uv`, bash, git, FastAPI, CORS, Vercel, AI Pipe |
| [`ga0/`](ga0/) | Graded Assignment 0: a guide per question (how it's graded, what we did and why) |
| [`ga1/`](ga1/) | Graded Assignment 1 (22/22): grader map, what we did and why, helper scripts |
| [`ga0/solutions/`](ga0/solutions/) | Files we submitted or ran (HTML, SQL, scripts, ngrok policy) |
| [vercel-deploys](https://github.com/sreekarsarma55/vercel-deploys) | Separate repo: the FastAPI app behind every endpoint question (Q5, Q10, Q11, Q25) |

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

## 📈 Status

GA0: **all 25 questions green and saved** (of 35.5 marks). See [`ga0/README.md`](ga0/README.md) for the
question-by-skill table, the method and the recurring traps.

---

_Part of [sreekarsarma55/notes](https://github.com/sreekarsarma55/notes). Subject branch: `tds`._
