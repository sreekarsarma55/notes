# Q5 — Code Interpreter with AI Error Analysis (1 mark)

## Problem

Deploy a FastAPI endpoint `POST /code-interpreter` that executes submitted Python and
returns:

```json
{ "error": [3], "result": "Traceback ..." }
```

`error` is the list of line numbers where execution failed (empty when it succeeds),
`result` is the exact stdout or the traceback. CORS must be enabled.

Answer submitted to the quiz = **the public URL**.

## How it is actually graded

```text
bank        = 60 cases embedded in the validator (30 clean, 30 with errors)
selection   = seeded shuffle from your email -> 3 cases, deterministic
POST        = {"code": ...} to  <yourURL>/code-interpreter   (suffix auto-appended)
requires    = res.ok, content-type includes application/json,
              Array.isArray(body.error), typeof body.result === "string"

clean case  ->  body.error.length === 0
            AND body.result === expectedOutput      (EXACT string, trailing \n included)
error case  ->  sorted(body.error) === sorted(expectedLines)
            AND body.result contains "Traceback" or "Error"

pass        = all 3 cases pass
```

**The 3 cases for `23f3002028@ds.study.iitm.ac.in` are ids 8, 34, 2 — all clean:**

| id | code | expected `result` |
|---|---|---|
| 8 | `numbers = [x**2 for x in range(5)]` / `print(numbers)` | `"[0, 1, 4, 9, 16]\n"` |
| 34 | `result = list(range(0, 10, 3))` / `print(result)` | `"[0, 3, 6, 9]\n"` |
| 2 | `numbers = [1,2,3,4,5]` / `total = sum(numbers)` / `print(f'Sum: {total}')` | `"Sum: 15\n"` |

So no AI call is ever made for this account — **zero AI Pipe spend**.

## Solution

[`apps/code-interpreter/`](apps/code-interpreter/) — a single FastAPI app:

- `execute_python_code()` compiles with filename `<code>`, runs `exec` with **one**
  namespace dict for globals *and* locals, and captures stdout via `redirect_stdout`.
- On failure it trims its own `exec` frame from the traceback so the output matches
  what a real interpreter prints.
- `error_lines_from_traceback()` returns `[exc.lineno]` for `SyntaxError`, otherwise the
  **deepest** traceback frame belonging to `<code>`.
- `analyze_error_with_ai()` runs *only* on failure, via AI Pipe with a strict
  `json_schema` response format and a Pydantic `ErrorAnalysis` model. Its answer is
  reported as `ai_error_lines` / `ai_agreed` while the traceback stays authoritative.

### Why the AI is grounded rather than trusted

Case 15 is the argument:

```text
1 | def divide(a, b):
2 |     return a / b          <- raises ZeroDivisionError
3 |
4 | result = divide(10, 0)    <- the call site
5 | print(result)
expected error lines: [2]
```

An LLM asked "which line failed?" very often answers `4`. The expected answer is the
deepest frame, `2`. Grounding on the real traceback is exactly the fix for the
hallucinated-line-number problem the question itself raises.

## Verification

```text
all 60 bank cases (30 clean + 30 error)     60/60 pass, zero AI calls
the 3 graded cases over real HTTP           exact match on result, error == []
content-type                                application/json
CORS preflight (OPTIONS)                    200, access-control-allow-origin: *
error case 15 (deepest-frame rule)          expected [2], got [2]
documented Example 1                        error [], result "15\n"
documented Example 2                        error [3], traceback text matches the docs
```

## Deployment runbook

See [`apps/code-interpreter/README.md`](apps/code-interpreter/README.md). Short version:
import the repo at `vercel.com/new`, set **Root Directory** to
`tds/ga0/apps/code-interpreter`, set the production branch to `tds`, deploy, then submit
`https://<project>.vercel.app/code-interpreter`.

## Traps

| Trap | Detail |
|---|---|
| **Exact string comparison** | `result` must equal `"Sum: 15\n"` — the trailing newline from `print` included. Stripping whitespace fails the case. |
| **Two dicts break comprehensions** | `exec(code, globals_d, locals_d)` makes a comprehension look its free variables up in globals only, raising `NameError`. Pass one dict for both. |
| **Deepest frame, not the call site** | The expected line is where the exception was raised. |
| **`SyntaxError` has no frame** | It is raised by `compile`, so walk `exc.lineno` instead of the traceback. |
| **CORS is graded implicitly** | The grader runs in a browser page, so a missing preflight response shows up as "Cannot reach endpoint". |
| **Your own frames leak** | `traceback.format_exc()` includes the harness's `exec` line; drop `tb_next` once for clean output. |
