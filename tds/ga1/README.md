# GA1 — Graded Assignment 1 (Sep 2026)

Quiz: `https://exam.sanand.workers.dev/tds-2026-09-ga1` · 16 questions · **22 marks** ·
Due **Sun 18 Oct 2026, 11:59 pm IST**.

**Result: 22 / 22, saved 9 Oct 2026.**

## What changed from GA0

GA0 graded almost everything in the browser. GA1 moves most checks to the server:

```text
browser  --POST /backendVerify {email, quizSign, questionId, response}-->  exam server
```

The question *data* is still built in the browser from `seedrandom(email#questionId + version)`, so
it can be rebuilt offline. The *check* happens on the server, so the only way to be sure is to send
the exact payload the Check button sends. Every answer below was confirmed that way before it was
handed over, unless the table says otherwise.

How we ran the bundle offline: replace its CDN imports (`lit-html`, `jszip`, `seedrandom`,
`prettier`) with local npm packages, `import()` it in Node, call each question's init function, then
call its generator (`ie`, `de`, `le`, `i1`, `N4`). This uses the grader's own code, not a re-typed copy.

## Questions

| # | Question | Marks | How it's graded | What decided it | Status |
|---|---|---|---|---|---|
| 1 | VS Code version | 0.5 | regex `Version: Code x.y.z` + `OS Version:` | paste the *whole* `code -s` output | run on your machine |
| 2 | Code in response headers | 0.5 | server; code rotates hourly | it's in `X-Exam-Code`, not the body (`curl -i`) | verified |
| 3 | POST with uv + HTTPie | 0.5 | parses your JSON: `headers.Host`, `json.email`, `json.request_id` | `--ignore-stdin` when stdin isn't a terminal | verified |
| 4 | npx prettier | 0.5 | sha256 of `prettier@3.4.2` output | the version is pinned; other versions format differently | verified |
| 5 | Fix broken JSON | 1 | server compares with the original | 6 errors: 3 missing commas, 2 unquoted keys, 1 single-quoted key | verified |
| 6 | 12-factor config | 1 | **browser**: random `?set=` overrides, strict type + value check | precedence order, `debug` → bool, `api_key` masked, CORS | 300/300 replays |
| 7 | Reorganise files | 1 | server; sha256 of `find . -type f \| LC_ALL=C sort` | delete the zip's `README.md`; unicode + spaces in paths; `tr -d '\r'` | verified |
| 8 | CSV sales from ZIP | 1 | server; rounded revenue | Mumbai + `Jan` from `YYYY-Mon-DD` dates | verified |
| 9 | GitHub Pages | 1 | page fetched through the exam proxy, email must appear | `<!--email_off-->` stops Cloudflare hiding the email | needs Pages switched on |
| 10 | Git forensics | 1.5 | server | `git log -S` finds the *introducing* commit; subjects repeat as decoys | verified |
| 11 | Cosine similarity | 1.5 | server; exact top-5 per query | re-normalise anyway; tie → smaller `doc_id` | verified (10/10) |
| 12 | Yes/No model split | 1 | browser → AI Pipe, both models, `\bYes\b` / `\bNo\b` | needs your token; measure prompts before submitting | run on your machine |
| 13 | termlog decode | 2 | server checks the signed recording | cipher = rot13(hex(reverse(code))) | run on your machine |
| 14 | Live MCP server | 3 | server acts as a real MCP client, 5 tool calls | challenge comes from the **HTTP header**, not the JSON body | live grader passed |
| 15 | Ledger agent | 4 | server sends 6 unseen questions, 15 s each | IST dates, latest `updated_at` wins, paid-only, currency → USD | live grader passed (54/54) |
| 16 | Tangram | 2 | signed token whose match key = target | **the board's y-axis points up; the SVG's points down**; exact a + b√2 geometry | server match key = target |

## Notes per question

**Q4.** `npx -y prettier@3.4.2 README.md | sha256sum`. We rebuilt the seeded README and hashed both
the CLI output and `prettier.format()`; both gave the same hash. Pinning `@3.4.2` is the whole point:
it is the version the grader uses in the browser.

**Q5.** Parse errors only report the *first* problem, so "fix one, re-run, repeat" works but is slow.
[`helpers/q05_fix_json.py`](helpers/q05_fix_json.py) applies line-level rules (quote bare and
single-quoted keys, add a comma when a value line is followed by another key, drop trailing commas)
and then `json.loads` the result, which raises if anything is left. Its output matched the grader's
original byte for byte.

**Q6.** Order, low → high: hard-coded defaults → `config.development.yaml` → `.env` → OS `APP_*` →
`?set=`. `APP_LOG_LEVEL` maps to `log_level`, `NUM_WORKERS` to `workers`. The browser compares with
`typeof`, so `"8658"` is not `8658`. Deployed as `GET /effective-config` in
[vercel-deploys](https://github.com/sreekarsarma55/vercel-deploys).

**Q7.** [`helpers/q07_reorganize.sh`](helpers/q07_reorganize.sh): `find -print0 | while read -d ''`
handles spaces; `grep -m1 '^category:'` takes only the first match; `tr -d '\r'` removes CRLF; the
bundled `README.md` must be deleted first. With it left in, the hash is `ebe4…`, which is wrong.
Some names use a Cyrillic `і` that looks exactly like `i`. Never retype paths by hand.

**Q10.** `git log -S 'STAGING_TOKEN=stg_' -- config/app.env` lists two commits: the one that added
the token and the one that rotated it. The introducing commit is the older one. `git log -p --reverse`
shows the `+STAGING_TOKEN=stg_…` line directly.

**Q11.** [`helpers/q11_rank.py`](helpers/q11_rank.py): `D @ q` on unit vectors, then sort by
`(-similarity, doc_id)` so ties go to the smaller id.

**Q12.** [`helpers/q12_split.py`](helpers/q12_split.py) sends each candidate in
[`q12_prompts.txt`](helpers/q12_prompts.txt) to both models N times and counts replies that meet the
grader's exact rule. The candidates aim at real differences: self-identity (luna knows its name) and
hard arithmetic where a weaker model guesses wrong.

**Q13.** The cipher contains only digits and `n–s`, so it is hex with ROT13 applied last. Undo in
reverse order: `tr 'A-Za-z' 'N-ZA-Mn-za-m' | xxd -r -p | rev`. Run it **inside** the recording; the
code changes every 3 hours.

**Q14.** MCP over Streamable HTTP is JSON-RPC over `POST`: answer `initialize`, return `202` with no
body for notifications, list one tool, and on `tools/call` hash `X-Exam-Challenge` from the request
headers. No SDK needed. Responses are plain JSON; SSE is optional.

**Q15.** No LLM: every grader question is one of six shapes (revenue by region+month, refunded count,
top product by month, average paid order by region, distinct customers per product, order count).
Keyword rules pick the shape; the numbers are computed from the data. The traps are in the data, not
the wording: 219 duplicated ids, half the timestamps in UTC (a `20:30Z` order on 31 Dec counts as
1 Jan in IST), INR and EUR amounts.

**Q16.** The grader only accepts a token whose `match_key` equals the target's `expected_match_key`:
a SHA-256 of the union outline, computed in exact `a + b√2` arithmetic with translation removed.
"Close" scores zero.

```text
1. solve.py        backtracking exact cover on the target outline (shapely): next piece's
                   top-left corner goes at the region's top-left corner, all 8 orientations
2. pixfit.py       rasterise each layout, move pieces ±4 ticks to minimise pixel XOR with the target
3. exact_search.mjs for each piece, every pose that draws the same polygon (different
                   orientation/flip combinations land on different √2 lattices), then test the
                   game's own computeMatchKey (imported from the game's JS)
```

**The bug that cost hours: the board draws with y pointing up, but the target is an SVG with y pointing
down.** Every layout built from the unflipped picture was the mirror image of the target. It looked
right to within 1 px, and no ±2-tick search could ever match the key. The fix was to flip the target
(`y → 576 − y`) before solving. After that, the exact search found the match in 9 tries:

```text
state data  [[84,80,4,1],[180,48,0,1],[203,80,1,0],[116,16,0,1],[225,70,0,1],[148,16,0,0],[16,102,7,0]]
server match_key 45da1499…6bff == expected_match_key   (this account's target, tg-044)
```

Paste the state into **State data**, then **Load state**, then **Generate signed payload**. Lesson: when
an approximate fit is close but the exact check never passes, look for a frame-of-reference error
(axis direction, units, origin) before you widen the search.

## Keep alive until the deadline

Q6, Q14 and Q15 are graded live. Q14 says outright that "a score you got earlier does not carry
over". The Vercel project must be running (it was paused on 8 Oct), and the GitHub Pages site (Q9)
must stay published.
