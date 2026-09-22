# Q4 — Calculate variance (0.5 marks)

## Problem

`q-calculate-variance.json` holds 1000 measurements. Report the **sample variance**
(N−1 denominator), rounded to 2 decimal places.

## How it is actually graded

```text
data       = 1000 integers, seeded from your email
expected   = sampleVariance(data).toFixed(2)      // simple-statistics, N-1
check      = |parseFloat(yourAnswer) - parseFloat(expected)| > 0.05  ->  reject
```

Tolerance is **±0.05**, which is the whole story (see traps).

## Solution

```text
128.70
```

## Verification

Three independent computations agree exactly:

```text
n            = 1000          (matches the stated count)
range        = 51 .. 91
mean         = 70.654

statistics.variance(data)        = 128.69898298298298      (N-1)
exact Fraction arithmetic (N-1)  = 32142571/249750 = 128.69898298298298
grader's JS  sampleVariance(...) = 128.69898298298298  -> toFixed(2) = "128.70"

|128.70 - 128.7| = 0  ≤  0.05   ✅
```

## Traps

| Trap | Detail |
|---|---|
| **Bessel's correction is the entire question** | Population variance gives `128.57`. That is **0.130** away from the expected value — well outside the ±0.05 tolerance, so it is rejected. |
| **Which function to call** | ✅ `statistics.variance()`, `VAR.S()`, `np.var(x, ddof=1)` · ❌ `statistics.pvariance()`, `VAR.P()`, `np.var(x)` (defaults to `ddof=0`). |
| **Rounding, not truncation** | Report 2 dp. The tolerance is generous enough that 2 dp always lands, but only if the right estimator was used. |

```text
sample variance     s² = Σ(xᵢ − x̄)² / (n − 1)      ← unbiased, this question
population variance σ² = Σ(xᵢ − μ)²  / n
```
