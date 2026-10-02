# Q24 — Use GitHub (1 mark)

## Problem

Create a **public** repo, commit an `email.json` containing
`{"email": "<your email>"}`, and submit its **raw** URL.

## How it is actually graded

```text
1. URL hostname includes raw.githubusercontent.com
2. fetch(url).json()                 (from your browser, no auth)
3. body.email === your email
```

## What we did and why

We put `email.json` in the root of
[`vercel-deploys`](https://github.com/sreekarsarma55/vercel-deploys), the same public
repo used for Q5/Q10/Q11/Q13/Q25, so there's only one repo to keep public.

```text
https://raw.githubusercontent.com/sreekarsarma55/vercel-deploys/main/email.json
→ {"email": "23f3002028@ds.study.iitm.ac.in"}
```

Why the **raw** URL: the normal `github.com/.../blob/...` URL returns an HTML page.
`raw.githubusercontent.com` returns the file itself, which `.json()` can parse.

## Verification

```text
curl the raw URL      returns the exact JSON
replayed the grader   pass, once the repo was public (it was private at first)
```

## Traps

| Trap | Detail |
|---|---|
| **Private repo** | A raw URL from a private repo returns 404 without a token. |
| **The `blob` URL** | That's an HTML page, so the JSON parse fails. |
| **Key name or typos in the email** | It must be exactly `"email"` with the email exactly as it appears on the quiz page. |
| **Raw CDN caching** | Raw URLs can be cached for a few minutes. After editing, wait before pressing Check. |
