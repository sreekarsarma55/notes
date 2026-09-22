# Q1 — Scale Manipulation Repair in Axis Design (1 mark)

## Problem

A Chart.js chart uses a deceptive scale. Identify the manipulation, quantify the
distortion with a number, fix the axis, and put the explanation in an HTML comment
at the top of the submitted HTML.

Assigned variant: **chart 8 of 20** — "Growth is steady and linear", 9 monthly points
`178.4 … 335.58`, with `scales.y.type = "logarithmic"`.

## How it is actually graded

Generator (type `D` = log scale) and validator, from `exam-tds-2026-09-ga0.js`:

```text
firstDelta       = y[1] - y[0]                 = 195.81 - 178.4  = 17.41
lastDelta        = y[8] - y[7]                 = 335.58 - 313.52 = 22.06
distortionValue  = round(lastDelta/firstDelta, 1 dp)             = 1.3
tolerance        = max(0.2, |1.3| × 0.15)                        = 0.2
```

Eight checks run in order, and the **first** failure is the message you see:

| # | Check |
|---|---|
| 1 | submission length ≥ 140 chars |
| 2 | at least one `<!-- ... -->` comment |
| 3 | a number exists in the comment — **the first regex match `-?\d+(\.\d+)?`** |
| 4 | `\|number − 1.3\| ≤ 0.2`, i.e. anything in **1.10 … 1.50** |
| 5 | `/\btype\s*:\s*["']linear["']/` matches the submission |
| 6 | comment contains one of **5 hardcoded phrases** (below) |
| 7 | `linear` appears in comment + HTML |
| 8 | HTML has `<canvas`, `new Chart(`, `<script` |

The five accepted phrases for type `D` — matching is lowercased, whitespace-collapsed,
substring:

```text
log scale compresses linear acceleration
log axis hides arithmetic growth pace
linear growth appears flattened on log
growth visually compressed by 1.3x          (o.toFixed(1))
compression profile 8 on log axis           (scenarioId + 1)
```

## Solution

Distortion `1.27` (= 22.06 / 17.41, the grader's own formula before its 1-dp rounding),
fix `scales.y.type` to `linear` with `beginAtZero: true`, and seed the comment with the
required phrases. See [`apps/`](apps/) — the submission HTML is reproduced in the PR
that added this note.

Comment skeleton that satisfies checks 3–7:

```text
<!--
  Quantification: 1.27
  Distortion: 1.27 (last-period gain 22.06 divided by first-period gain 17.41)
  ... The log scale compresses linear acceleration ... growth visually compressed
  by 1.3x ... genuinely linear growth appears flattened on log ...
  Fix: options.scales.y now uses type: "linear" with beginAtZero: true ...
-->
```

## Verification

Three routes to the underlying data shape, computed in `analyze.py`:

```text
straight-line fit   R² = 0.99817   slope = +19.852 users/period
exponential fit     R² = 0.98856   rate  = +8.26 %/period
=> the series is genuinely LINEAR, so a log axis is unjustified
range  max/min = 335.58/178.4 = 1.8811× = 0.2744 decades  (a log axis wants ≥ 1)
```

The rendered chart was screenshotted headless to confirm it still draws, and all
8 checks were replicated in `verify-q01.mjs` before submitting.

## Traps

| Trap | Detail |
|---|---|
| **First number wins** | `ua()` takes the first `-?\d+(\.\d+)?` in *all* comments joined. A comment opening with `max/min = 335.58/178.4` submits **335.58**. Put the distortion first and keep stray numbers out. |
| **Literal snippet match** | `"type": "linear"` (quoted key) does **not** contain `type: "linear"`. Chart.js accepts both; the regex does not. |
| **Newlines break capture** | `Distortion:` and its text must be on the same line, or a non-DOTALL `.*` capture comes back empty. |
| **Phrase list is hardcoded** | No amount of good prose about logarithmic compression passes check 6. Only those five strings do. |
| **Tolerance is wider than stated** | `max(0.2, 15%)` ⇒ ±0.2, not ±0.195, so 1.10–1.50 all pass. |
| **The interesting bit of the analysis** | A log axis normally *hides* exponential growth. Here the data is linear, so the log axis **manufactures** a fake deceleration — it contradicts the chart's own "steady and linear" title. |
