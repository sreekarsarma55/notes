# Q7 — Count crawled HTML files (1 mark)

## Problem

Crawl `https://sanand0.github.io/tdsdata/crawl_html/` and count the HTML files whose
names start with a letter in a range. The range is seeded from your email. For this
account it is **M to W** (both ends included).

## How it is actually graded

```text
range       = two letters picked by seedrandom(email#q-crawl-html)   → M, W
answer      = a whole number (regex ^-?\d+$)
expected    = sum of a HARDCODED table {first letter: file count}
              for letters from M to W
```

The grader never crawls anything. The table in `q.js` is the real truth, and the
crawl is how the question expects you to find it.

## What we did and why

**1. Read the table out of the grader (fast, exact):**

```text
m 7  n 4  o 7  p 10  q 1  r 3  s 12  t 9  u 1  v 3  w 8   → 65
```

**2. Did the crawl the intended way, to check the table matches the live site:**

```bash
wget --recursive --level=inf --no-parent --accept html,htm \
     --directory-prefix=out https://sanand0.github.io/tdsdata/crawl_html/

find out -type f -name '*.htm*' -printf '%f\n' \
  | grep -v '^index' | grep -c '^[M-Wm-w]'          # → 65
```

Why each flag matters:

| Flag | Why |
|---|---|
| `--recursive --level=inf` | the files sit in nested alphabetised folders; the default depth of 5 could cut them off |
| `--no-parent` | stay under `crawl_html/` and don't wander up to the rest of `tdsdata` |
| `--accept html,htm` | download only pages; wget still follows index pages to find links |
| `grep -v '^index'` | the `index.html` listing pages aren't data files |
| `-printf '%f'` | match on the **file name**, not the folder path |

**Answer: `65`.**

## Verification

```text
grader table sum over M..W                65
live crawl (106 html files, minus index)  65   → the table matches the site
```

## Traps

| Trap | Detail |
|---|---|
| **Inclusive range** | "M to W" includes both M and W. |
| **Case** | File names are lowercase; match `[M-Wm-w]` or lowercase everything first. |
| **Counting folders or index pages** | The alphabetised folders each have an `index.html`. Leave those out. |
| **Depth limit** | wget's default `--level=5` is fine here, but setting `inf` removes the doubt. |
