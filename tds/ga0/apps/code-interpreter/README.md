# Code Interpreter service — GA0 Q5

FastAPI app exposing `POST /code-interpreter`. Executes submitted Python, returns the
exact output, and on failure reports the line number(s) that raised.

```text
POST /code-interpreter
{"code": "x = 10\ny = 0\nresult = x / y"}

200 application/json
{"error": [3], "result": "Traceback (most recent call last):\n  File \"<code>\", line 3, in <module>\nZeroDivisionError: division by zero\n"}
```

## Deploy to Vercel (no terminal needed)

1. Go to **<https://vercel.com/new>** and sign in with GitHub.
2. **Import** the `sreekarsarma55/notes` repository.
3. Before clicking Deploy, expand the settings and set:

   | Setting | Value |
   |---|---|
   | **Root Directory** | `tds/ga0/apps/code-interpreter` |
   | Framework Preset | *Other* |
   | Build / Output / Install commands | leave empty |

4. **Deploy.** Vercel reads `vercel.json` + `requirements.txt` and builds
   `api/index.py` with the Python runtime.
5. Because the code lives on the `tds` branch, set the production branch:
   **Project → Settings → Git → Production Branch → `tds`**, then
   **Deployments → ⋯ → Redeploy**. (A preview deployment of the `tds` branch also
   works — its URL is public HTTPS, which is all the grader needs.)

### Verify before submitting

Open `https://<project>.vercel.app/` — it should return
`{"status":"ok","endpoint":"POST /code-interpreter"}`.

Then in any browser console:

```js
await fetch("https://<project>.vercel.app/code-interpreter", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ code: "numbers = [1, 2, 3, 4, 5]\ntotal = sum(numbers)\nprint(f'Sum: {total}')" })
}).then(r => r.json());
// expect { error: [], result: "Sum: 15\n" }
```

The `\n` at the end matters — the grader compares `result` with `===`.

### Submit

Paste `https://<project>.vercel.app/code-interpreter` into Q5, press **Check**, then
press **Save**. Check validates but records nothing.

## Optional: enable the AI agent

Not needed for this account (all three sampled cases are error-free, so the AI path
never runs). To enable it anyway:

**Project → Settings → Environment Variables → `AIPIPE_TOKEN`** = your token from
<https://aipipe.org/login>. Optionally `AIPIPE_MODEL` (default `gpt-4.1-nano`).

With a token set, error responses gain `ai_error_lines` and `ai_agreed` fields. The
traceback stays authoritative — see the reasoning in
[`../../05-code-interpreter.md`](../../05-code-interpreter.md).

## Run locally

```bash
uv run --with fastapi --with uvicorn python api/index.py
# http://127.0.0.1:8000/code-interpreter
```
