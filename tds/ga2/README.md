# GA2 — Graded Assignment 2 (Sep 2026)

Quiz: `https://exam.sanand.workers.dev/tds-2026-09-ga2` · 15 questions · **25.5 marks** ·
Due **Sun 18 Oct 2026, 11:59 pm IST**.

GA2 is almost entirely *deployment* work: 10 of the 15 questions are graded by calling a URL you
host. Nine of those now live in one FastAPI app
([vercel-deploys](https://github.com/sreekarsarma55/vercel-deploys)), one is a Docker Compose
stack, and the rest are terminal recordings or prompts.

## How GA2 is graded

```text
backendVerify   Q1 Q2 Q3 Q4 Q6 Q8 Q10 Q13 Q14 Q15   exam server probes your URL
browser         Q5 Q7 Q9 Q11 Q12                     validator fetches from the quiz page
```

Both kinds can be rehearsed before submitting:

* **Server-graded**: POST the same payload the Check button sends to `/backendVerify`. It returns
  the real verdict and records nothing (only Save stores a score). A `cloudflared` quick tunnel in
  front of a locally running app is enough to get a verdict in seconds.
* **Browser-graded**: the validator lives in `exam-tds-2026-09-ga2.js`. Copy its logic and run it
  against the app locally — hundreds of times, with the same randomisation it uses.

**Save rechecks every live endpoint.** The page says so: *"Save rechecks your answers, including
live servers."* So a deployment that is down at Save time scores zero even if Check was green.

## Questions

| # | Question | Marks | What decided it | Status |
|---|---|---|---|---|
| 1 | HTTPBin terminal lab (termlog) | 2 | seven `capture` wrappers with the right curl flags | commands verified |
| 2 | Differentiate model intelligence | 2 | a question whose *wrong* answer is YES; nano trips, mini doesn't | tester written |
| 3 | CORS-aware metrics API | 1.5 | only the assigned origin may get ACAO; evil origin gets none | real grader ✅ |
| 4 | OAuth/OIDC token verification | 2 | RS256 signature + iss + aud + exp, all four | real grader ✅ |
| 5 | 12-factor config precedence | 1 | **identical to GA1 Q6** — same question id and seed | already deployed ✅ |
| 6 | Compose + Redis behind a tunnel | 2 | Redis `INCR`, independent keys, real `PING` in `/healthz` | real grader ✅ |
| 7 | POST analytics endpoint | 1.5 | 401 without the key; revenue counts positive amounts only | 100 replays ✅ |
| 8 | Observability: metrics, health, logs | 1.5 | counter must really advance; logs must mention `/work` | real grader ✅ |
| 9 | Local LLM through a tunnel | 1 | browser-graded, so CORS and the Host header both matter | self-test script |
| 10 | Local LLM structured output | 2 | rules beat an LLM: deterministic, and 422 (never 500) on junk | real grader ✅ ×6 |
| 11 | Idempotency + pagination + rate limit | 2 | same key → same id; ids 1..45 exactly once; 429 + `Retry-After` | replays ✅ |
| 12 | Middleware stack | 1.5 | echo an inbound `X-Request-ID` in body *and* header | replays ✅ |
| 13 | Recover a fragmented LLM stream | 1.5 | decode hex → bytes → NDJSON; never per-chunk JSON | real grader ✅ |
| 14 | Docker build cache misses | 1.5 | `COPY` hashes content, not mtime; `.dockerignore` kills case D | real grader ✅ |
| 15 | Custom Ollama model (termlog) | 2 | exact SYSTEM text and four PARAMETER values | commands verified |

## Notes per question

**Q1.** The `capture` helper wraps each command's output in `HTTPBIN_BEGIN/END <tag> <TASK>`
markers, so nothing extra may be printed inside a capture. The flag choices that matter:
`-d` with `-X PUT` sends `application/x-www-form-urlencoded` (task FORM), `-d` with an explicit
`Content-Type: application/json` keeps `10` a number and `true` a boolean (task POST),
`-sSL -G --data-urlencode` both encodes the `url` parameter and follows the redirect (REDIRECT),
`-c jar.txt` then `-b jar.txt` splits cookie *setting* from the captured cookie *read* (COOKIES),
and `-o /dev/null -w '%{http_code}'` prints the status and nothing else (STATUS). All seven were
run for real before being handed over: [`helpers/q01_httpbin.sh`](helpers/q01_httpbin.sh).

**Q2.** The backend sends one user message to `gpt-5-nano` and `gpt-5-mini`, three times, with
minimal reasoning effort, and accepts only a bare `YES`/`NO` (case and one trailing `.`/`!`
ignored; a quoted answer or any explanation fails). Two of three trials must split.
[`helpers/q02_split.py`](helpers/q02_split.py) replays that contract against AI Pipe directly so
candidates can be ranked without burning the exam's three-attempts-per-minute budget. The
candidates in [`q02_prompts.txt`](helpers/q02_prompts.txt) are all questions whose *incorrect*
answer is YES (is 91 prime, does `0.1 + 0.2 == 0.3`, does the Moon have a permanently dark side),
on the theory that the smaller model is likelier to take the bait.

**Q3.** The grader sends a preflight from the assigned origin (expects ACAO), a preflight from a
random origin (expects **no** ACAO), then a `GET /stats`. A blanket `CORSMiddleware(allow_origins=["*"])`
fails the second probe, so the app now computes CORS per path: wildcard everywhere the GA0/GA1
graders need it, and a single assigned origin for `/stats` and `/ping`.

**Q4.** Verified with pure-Python RSA PKCS#1 v1.5 — parse the SPKI DER for `(n, e)`, compute
`sig^e mod n`, and compare against `00 01 FF… 00 || DigestInfo || SHA-256`. That keeps PyJWT and
`cryptography` out of the serverless bundle. Testing needed tokens, and the sandbox has no
`openssl`, so a throwaway RSA key minted them with `cryptography`: valid, expired, wrong-audience,
wrong-issuer, tampered-payload and `alg: none` — the last one guards against algorithm confusion.

**Q5.** Nothing to do. GA2 reuses the question id `q-config-precedence-server`, and the seed is
`id#email#version`, so the assigned layers are byte-for-byte the GA1 ones. The deployed
`/effective-config` answered it unchanged.

**Q6.** `redis.asyncio` + `INCR`, with `/healthz` actually calling `PING`. Compose publishes only
the API; Redis stays on the internal network. Files:
[`helpers/q06-compose/`](helpers/q06-compose/). Verified by running the same `app.py` against a
real `redis:7-alpine` container behind a tunnel.

**Q8.** The counter has to be *live*. Incrementing it in middleware means `/metrics` itself counts,
so the increase is always at least the number of `/work` calls. `/logs/tail` returns the last N
entries with `level`, `ts`, `path` and `request_id`, which also gives the grader its `/work` match.

**Q9.** Two traps, both from the browser: Ollama rejects an unknown `Host` (DNS-rebinding
protection), so the tunnel must rewrite it — `cloudflared --http-host-header localhost:11434`; and
free ngrok shows browsers an interstitial page, and unlike GA0 Q18 this grader does *not* send
`ngrok-skip-browser-warning`, so ngrok free will fail here. [`helpers/q09_selftest.sh`](helpers/q09_selftest.sh)
replays the echo test, the arithmetic test and the preflight.

**Q10.** The question says to wrap a local LLM, but the grader only checks four extracted fields on
randomised invoices. Regex rules are deterministic, instant, and need no model, so that is what is
deployed; it passed six independent runs. Empty or malformed input returns 422, which the grader
explicitly tests (a 500 fails).

**Q11.** The cursor is just an opaque offset. Created orders get string ids (`ord-…`) so they never
pollute the 1..45 catalog the pagination scan walks. Rate limiting is a sliding window keyed on
`(path bucket, X-Client-Id)`, so the grader's pagination client cannot exhaust the flood client's
budget.

**Q13.** The chunks are hex-encoded *bytes*, deliberately split mid-UTF-8 (`café` straddles a
boundary). Decode all the hex, join the bytes, then split on newlines — anything that parses each
chunk as JSON fails. Stop at the first `done: true` (keeping its text) or at an `error` record
(keeping earlier text, `complete: false`), and drop the trailing unterminated record.

**Q14.** Case C is the interesting one: BuildKit hashes file *content* for `COPY`, so `touch`
alone is a cache hit. Case D changes a file excluded by `.dockerignore`, so it is not even in the
build context. Case E edits the `RUN` command itself, which invalidates L4 and everything after it.

**Q15.** `ollama show --modelfile` must echo the exact SYSTEM line and each assigned PARAMETER
once. Inherited extras are fine. Use `SYSTEM """…"""` so the text survives verbatim, and keep the
base model's chat template.

## Keep alive until the deadline

```text
Vercel app   Q3 Q4 Q5 Q7 Q8 Q10 Q11 Q12 Q13 Q14   must not be paused
Compose+tunnel   Q6                                 docker compose up + cloudflared
Ollama+tunnel    Q9                                  ollama serve + cloudflared
```

Q1, Q2 and Q15 are one-shot (a recording, a prompt, a recording), so once they are green they stay
green.
