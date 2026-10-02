# Q10 — Write a FastAPI server to serve data (3 marks)

## Problem

You're given `q-fastapi.csv` (2000 rows of `studentId,class`). Serve it at `GET /api`:

```text
GET /api                     → {"students": [all rows]}
GET /api?class=1A&class=1B   → {"students": [only rows in 1A or 1B]}
```

Submit the public URL of the endpoint.

## How it is actually graded

```text
classes  = 4 classes picked with Math.random   ← NOT seeded: different on every Check
request  = fetch(`${yourURL}?class=A&class=B&class=C&class=D`)   (URL as you typed it)
expected = CSV rows whose class is one of the 4, IN CSV FILE ORDER
check    = deep strict equality of body.students against expected
           every key, every value, every type, every position
```

## What we did and why

The endpoint lives in the shared [`vercel-deploys`](https://github.com/sreekarsarma55/vercel-deploys)
app. These are the choices that matter for this grader:

```python
@lru_cache(maxsize=1)
def load_students():
    with open(DATA_DIR / "q-fastapi.csv", newline="", encoding="utf-8") as f:
        return [{"studentId": int(r["studentId"]), "class": r["class"]}
                for r in csv.DictReader(f)]

@app.get("/api")
async def students(class_: Optional[List[str]] = Query(None, alias="class")):
    rows = load_students()
    if class_:
        wanted = set(class_)
        rows = [r for r in rows if r["class"] in wanted]   # keeps CSV order
    return {"students": rows}
```

| Choice | Why |
|---|---|
| `List[str] = Query(alias="class")` | `?class=` is repeated, so FastAPI needs a list to collect every value. `class` is a Python keyword, hence the alias. |
| Filter by **looping over the CSV** | The order has to match the file. Looping over the requested classes would group the rows by class instead. |
| `int(studentId)` | The grader builds its expected rows with numbers, and deep equality treats `"1"` and `1` as different. |
| CSV bundled with `includeFiles: api/data/**` | Vercel's Python builder only ships imported code. Without this the data file is missing at runtime. |
| `lru_cache` | Parse the CSV once per warm instance, not once per request. |
| CORS `allow_origins=["*"]` | The grader calls from the quiz page in your browser. |

Submitted: `https://vercel-deploys-iota.vercel.app/api`

## Verification

```text
local: grader's comparison, 200 random 4-class picks (of 311 classes)   200/200 equal
live:  same comparison over HTTP against the Vercel URL                 passed
quiz:  green on Check
CI:    smoke test asserts 2000 rows and that a single-class filter works
```

## Traps

| Trap | Detail |
|---|---|
| **Order is graded** | Output must be in CSV order, not grouped by class. |
| **Types are graded** | `studentId` must be a number. `csv` reads everything as strings. |
| **Random on every Check** | You can't fit your answer to one test. The endpoint has to be correct for any 4 classes. |
| **URL is used as typed** | Submit the URL that ends in `/api`; nothing is appended. |
| **Data file not deployed** | Without `includeFiles` it works locally and returns 500 on Vercel. |
