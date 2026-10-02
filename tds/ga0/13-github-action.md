# Q13 — Create a GitHub Action (1 mark)

## Problem

Create a GitHub Actions workflow in one of your repos with a step whose **name**
contains your email, run it, and submit the repo URL.

## How it is actually graded

```text
GET api.github.com/repos/{user}/{repo}/actions/runs   (no auth, from your browser)
runs[0]           = the MOST RECENT run, of any workflow
GET runs[0].jobs_url
pass = some step in some job has a name that includes your email
```

Two things follow: the repo has to be **public** (an anonymous API call sees nothing
in a private repo), and the latest run has to be one that includes the step.

## What we did and why

Rather than adding a throwaway "hello world" workflow, we added a **real smoke test**
to [`vercel-deploys`](https://github.com/sreekarsarma55/vercel-deploys) and gave one of
its steps the email as its name:

```yaml
name: Smoke test
on:
  push:
    branches: [main]
  workflow_dispatch:          # lets you re-run it by hand to make it the latest run
jobs:
  smoke-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 23f3002028@ds.study.iitm.ac.in      # ← what the grader looks for
        run: echo "TDS GA0 Q13"
      - uses: astral-sh/setup-uv@v5
      - name: Import the app and exercise every endpoint
        run: uv run --with fastapi --with httpx python - <<'EOF'
             # FastAPI TestClient hits /, /code-interpreter, /api, /api/latency
             EOF
```

Why this design:

- **It runs on every push to `main`**, so the most recent run is always this
  workflow. A second workflow would compete to be `runs[0]`.
- **It's useful beyond the grade**: every deploy is checked before you trust the
  live URL.
- `workflow_dispatch` lets you trigger it by hand if another run ends up as the
  latest.

Submitted: `https://github.com/sreekarsarma55/vercel-deploys`

## Verification

```text
replayed the grader's two API calls with curl   step name found in runs[0]
```

The first attempt failed because the repo was **private**. Making it public fixed it.

## Traps

| Trap | Detail |
|---|---|
| **Private repo** | The grader's request has no auth, so it sees no runs. |
| **"Most recent run" means any workflow** | A later run from a different workflow (Dependabot, Pages) hides yours. Re-run yours last. |
| **Step name, not job name** | It searches `steps[].name`. |
| **The run must exist** | Committing the YAML isn't enough if nothing triggers it. Push to the branch it watches. |
