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
p95 (nearest-rank)   sorted(x)[ceil(0.95 × n) − 1]
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

## uv

```bash
uv run script.py                      # run with inline PEP 723 deps
uv run --with fastapi --with uvicorn python app.py
uv venv && uv pip install -r requirements.txt
uvx <tool>                            # run a tool without installing
```

## Bash one-liners that keep recurring

```bash
# flatten nested dirs into one folder
find . -type f -exec mv -n {} target/ \;

# shift every digit by one (1→2, 9→0) in filenames
for f in *; do mv "$f" "$(echo "$f" | tr '0123456789' '1234567890')"; done

# stable, locale-independent hash of a folder's contents
grep . * | LC_ALL=C sort | sha256sum

# case-insensitive replace, preserving line endings
sed -i 's/IITM/IIT Madras/gI' *

# recursive mirror of a site, HTML only
wget --recursive --level=3 --no-parent --convert-links \
     --adjust-extension --accept html,htm --directory-prefix=./out URL
```

## Encodings

```python
pd.read_csv("data1.csv", encoding="cp1252")     # Windows-1252
pd.read_csv("data2.csv", encoding="utf-8")
pd.read_csv("data3.txt", encoding="utf-16", sep="\t")
```

UTF-16 files carry a BOM; use `utf-16` (not `utf-16le`) to let Python read it.

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
vercel.json         {"builds":[{"src":"api/index.py","use":"@vercel/python"}],
                     "routes":[{"src":"/(.*)","dest":"api/index.py"}]}
```

Deploying a subfolder: set **Root Directory** in project settings. Deploying a
non-default branch: set **Production Branch**, or use the branch's preview URL.
No filesystem writes, no `subprocess`, no `pip install` at runtime.
