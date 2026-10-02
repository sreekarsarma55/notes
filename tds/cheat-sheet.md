# TDS cheat sheet

Condensed recall for the tools GA0 and the ROE keep asking about.

## Reading a quiz grader

```bash
curl -s https://exam.sanand.workers.dev/exam.js -o exam.js          # module map
curl -s https://exam.sanand.workers.dev/exam-<quiz-id>.js -o q.js   # validators + data
grep -o "exam-[a-z0-9-]*\.js" exam.js | sort -u                    # find the quiz module
```

Per-question validators live in `q.js` as `answer` functions. Useful greps: the
question id (`q-...`), `throw new Error`, `tolerance`, `expected`.

## Statistics

```text
sample variance      s² = Σ(xᵢ − x̄)² / (n − 1)     statistics.variance / VAR.S / ddof=1
population variance  σ² = Σ(xᵢ − μ)²  / n           statistics.pvariance / VAR.P / ddof=0
Pearson r            r  = Σ(aᵢ−ā)(bᵢ−b̄) / √(Σ(aᵢ−ā)² Σ(bᵢ−b̄)²)
p95 (linear)         r=(n−1)·0.95; x₍⌊r⌋₎ + (r−⌊r⌋)(x₍⌊r⌋+1₎ − x₍⌊r⌋₎)   numpy default · GA0 Q25
p95 (nearest-rank)   sorted(x)[ceil(0.95 × n) − 1]                     differs by up to 7 ms on Q25 data
```

## Chart.js axis manipulations

| Manipulation | Config tell | Fix |
|---|---|---|
| truncated axis | `y.min` non-zero / no `beginAtZero` | `beginAtZero: true` |
| incorrect log scale | `y.type: "logarithmic"`, range < 1 decade | `type: "linear"` |
| inverted axis | `y.reverse: true` | `reverse: false` |
| dual-axis trick | two datasets with `yAxisID: y` / `y1`, independent min/max | share one scale, or plot % change |

On a log axis, pixels-per-unit falls off as `1/y`: equal **ratios** get equal distance,
equal **amounts** do not.

## Colour scheme choice

```text
sequential   ordered low→high, single-hue ramp     L* monotonic
categorical  unordered groups                     pairwise CIEDE2000 ≥ 30
diverging    meaningful midpoint (e.g. 0)         mid L* ≥ 80, both ends L* ≤ 65
avoid        rainbow/jet (hue span > 270°)
```

## FastAPI + CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
```

Browser-based graders send an `OPTIONS` preflight first; without CORS the failure looks
like "cannot reach endpoint". Note: `allow_origins=["*"]` cannot be combined with
`allow_credentials=True`.

If the grader **reads a response header in JavaScript** (`res.headers.get(...)`), also
add `expose_headers=["*"]`. Cross-origin JS can only read the safelisted headers
(Content-Type, Cache-Control, Content-Language, Content-Length, Expires,
Last-Modified, Pragma). `Access-Control-Allow-Origin` and custom headers like
`X-Email` read as `null` otherwise (GA0 Q18, Q25).

## uv

```bash
uv run script.py                      # run with inline PEP 723 deps
uv run --with fastapi --with uvicorn python app.py
uv venv && uv pip install -r requirements.txt
uvx <tool>                            # run a tool without installing
```

## Bash one-liners that keep recurring

```bash
# flatten nested dirs into one folder (skip files already moved)
mkdir flat && find . -mindepth 2 -type f -not -path './flat/*' -exec mv -n {} flat/ \;

# shift every digit by one (1→2, 9→0); skip names with no digit (mv a a is an error)
for f in *; do n=$(echo "$f" | tr '0-9' '1-90'); [ "$f" = "$n" ] || mv "$f" "$n"; done

# stable, locale-independent hash of a folder's contents
grep . * | LC_ALL=C sort | sha256sum

# case-insensitive replace, preserving line endings (GNU sed; on macOS: perl -pi -e 's/iitm/IIT Madras/gi' *)
sed -i 's/IITM/IIT Madras/gI' *

# recursive mirror of a site, HTML only, then count files by first letter
wget --recursive --level=inf --no-parent --accept html,htm --directory-prefix=./out URL
find out -type f -name '*.htm*' -printf '%f\n' | grep -v '^index' | grep -c '^[M-Wm-w]'
```

## Encodings

```python
pd.read_csv("data1.csv", encoding="cp1252")     # Windows-1252
pd.read_csv("data2.csv", encoding="utf-8")
pd.read_csv("data3.txt", encoding="utf-16", sep="\t")
```

UTF-16 files carry a BOM; use `utf-16` (not `utf-16le`) so Python reads the BOM and
removes it. Use `cp1252`, not `latin-1`, for Windows files: both read without an error,
but only cp1252 maps 0x80–0x9F to `€ † ‚ ž …`. `file data*` tells you the encoding.

## AI Pipe

```bash
curl https://aipipe.org/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AIPIPE_TOKEN" \
  -d '{"model":"gpt-4.1-nano","messages":[{"role":"user","content":"hi"}]}'
```

Base URL swaps for `OPENAI_BASE_URL`; token swaps for `OPENAI_API_KEY`. Budget is
**$1–2 per calendar month** — prefer deterministic solutions.

Structured output (forces a schema, prevents free-form drift):

```json
"response_format": {"type": "json_schema", "json_schema": {
  "name": "out", "strict": true,
  "schema": {"type": "object",
             "properties": {"error_lines": {"type": "array", "items": {"type": "integer"}}},
             "required": ["error_lines"], "additionalProperties": false}}}
```

## Python tracebacks

```python
compile(code, "<code>", "exec")            # name frames so you can filter them
exec(compiled, ns, ns)                     # ONE dict, or comprehensions break
except SyntaxError as e: e.lineno          # no frame exists for a syntax error
tb = exc.__traceback__                     # walk tb_next; DEEPEST frame raised
```

## Vercel

```text
api/index.py        + `app` ASGI object
requirements.txt    runtime deps
vercel.json         {"builds":[{"src":"api/index.py","use":"@vercel/python",
                                "config":{"includeFiles":"api/data/**"}}],
                     "routes":[{"src":"/(.*)","dest":"api/index.py"}]}
```

- Put the app at the **repo root** and deploy from `main` (as `vercel-deploys` does).
  Root Directory and Production Branch settings can be wrong without any visible error.
- Data files must be declared in `includeFiles`. Only imported code is bundled.
- No filesystem writes, no `subprocess`, no `pip install` at runtime.
- `503 DEPLOYMENT_PAUSED` means the project is paused (by you or by a Hobby usage
  limit). Go to Project → Settings → General → **Resume Project**. No redeploy needed.

## ngrok

```bash
ngrok http 11434 --traffic-policy-file policy.yml   # NOT the deprecated --response-header-add
```

```yaml
on_http_request:
  - actions: [{type: add-headers, config: {headers: {host: "localhost:11434"}}}]
on_http_response:
  - actions: [{type: add-headers, config: {headers: {x-email: "you@example.com",
               access-control-expose-headers: "*"}}}]
```

Browsers get an ngrok warning page unless they send `ngrok-skip-browser-warning`.

## JWTs

```python
h, p, s = token.split(".")                 # base64url, no padding
json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))   # read the claims
```

Check `exp`, `sub` and any time-window claims (`week_id` = ISO week) **before** you rely
on a token. `date +%G-W%V` prints the current ISO week.

## dbt

```sql
{{ config(materialized='table') }}
with src as (select ... from {{ ref('stg_x') }} where ts::date >= current_date - 30)
select date_trunc('day', ts)::date as d, coalesce(sum(v), 0) as total
from src group by 1 order by 1
```

`ref()` builds the dependency graph. Intermediate models use CTEs; marts aggregate
and order.
