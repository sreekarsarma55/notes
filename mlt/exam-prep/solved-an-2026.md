# ✅ Solved — MLT End Term, AN T1 2026

Answers checked against the paper's own marking **and**
recomputed numerically (21/21 assertions pass).
Source: `../pyq/MLT_ET_AN_T1_2026.pdf`.

This paper shares questions with FN T1 2026 — its Q17
and Q18 are identical to FN's Q2 and Q4.

---

## Q2 · 3 mk · SA — Naive Bayes free parameters

Binary classification, **five binary features**, a
generative model satisfying **class-conditional
independence**. How many free parameters?

```text
class-conditional independence = NAIVE BAYES

prior P(y=1)                ->  1   (P(y=0) follows)
P(xj = 1 | y=1), j = 1..5   ->  5
P(xj = 1 | y=0), j = 1..5   ->  5
                                --
                     2d + 1  =  11
```

### ✅ Answer: **11**

> Contrast: a **full** generative model (no independence
> assumption) would need `2(2⁵ − 1) + 1 = 63`. That gap
> is the whole point of Naive Bayes.

---

## Q3 · 3 mk · SA — neural network parameters

Input **10** · two hidden layers of **30** · output 1.
**"Ignore the biases."**

```text
10*30 = 300
30*30 = 900
30*1  =  30
-----------
total = 1230
```

### ✅ Answer: **1230**

> With biases it would be **1291** (`+30+30+1`).

---

## Q4 · 3 mk · SA — Bayesian point estimate

Dataset of 20 points, **15 ones and 5 zeros**, Bernoulli
parameter `p`, prior **`Beta(3, 2)`**. Point estimate =
expected value of the posterior.

```text
h = 15 ones, t = 5 zeros
posterior = Beta(3 + 15, 2 + 5) = Beta(18, 7)
mean = 18 / (18 + 7) = 18/25 = 0.72
```

### ✅ Answer: **0.72** (accepted 0.71 – 0.73)

> Same archetype as FN 2026 Q8 — that one had prior
> `Beta(10,40)` with 60 heads/40 tails, giving
> `Beta(70,80)` and mean `0.467`.

---

## Q5 · 3 mk · MCQ — bagging

A bag is `n` points sampled uniformly **with
replacement** from `n` points. Probability a given point
is **not** in the bag?

```text
each of the n draws misses the point with prob (1 - 1/n)
draws are independent
   -> P(not in bag) = (1 - 1/n)^n  ->  1/e = 0.368
```

### ✅ Answer: **`(1 − 1/n)ⁿ`**

> So ≈63.2% of distinct points appear in a bag, and the
> ≈36.8% left out form the out-of-bag (OOB) set.

---

## Q6 · 3 mk · MCQ — choosing a classifier from a figure

Red and green points shown. Pick the most appropriate
classifier.

```text
clean straight-line gap        -> hard-margin linear SVM
slight overlap / a few strays  -> SOFT-margin linear SVM
curved or ring-shaped groups   -> kernel (non-linear) SVM
```

> If any point sits on the wrong side, hard margin is
> **infeasible** — so overlap always means soft margin
> or a kernel.

---

## Q9 · 3 mk · MSQ — polynomial kernel

For `K(x,y) = (xᵀy)^p`:

```text
TRUE   p even  ->  K >= 0 for all x, y
                   (an even power is never negative)
TRUE   x, y orthogonal  ->  xᵀy = 0  ->  K = 0
FALSE  "K can never be zero"
       (it IS zero for orthogonal vectors)
```

---

## Q10 · 3 mk · MSQ — identify the two losses

The graph plots loss against `u = (wᵀx)y`.

```text
GREEN  straight line reaching exactly 0 at u = 1
       -> HINGE loss    max(0, 1-u)

RED    smooth curve, decays but never touches 0
       -> LOGISTIC loss  log(1 + e^-u)
```

### ✅ Answers: **Logistic loss** and **Hinge loss**

> Not squared loss (that U-turns upward after `u = 1`),
> and not 0-1 loss (that is a step at `u = 0`).

---

## Q11 · 3 mk · MSQ — PCA properties

`C` = covariance of a centered dataset, `n` points in
`ℝᵈ`, `X` the **d × n** data matrix, `wᵢ` the i-th
principal component.

```text
TRUE   wᵢᵀ C wᵢ is the variance along wᵢ
       (it equals the eigenvalue lambda_i)

TRUE   wᵢᵀ wⱼ = 0 for i != j
       (principal components are orthogonal)

FALSE  C = (1/n) Xᵀ X
       X is d x n, so Xᵀ X is n x n.
       The covariance must be d x d: C = (1/n) X Xᵀ

FALSE  wᵢᵀ C wᵢ > 0 for each i with 1 <= i <= n
       two errors: the index should run to d, not n;
       and the variance can be 0 (a zero eigenvalue,
       e.g. rank-deficient data)
```

---

## Q12 · 4 mk · SA — decision tree region area

Trace the path to the **only** leaf predicting `0`:

```text
x1 <= 1     YES
x1 <= -1    NO    ->  -1 < x1 <= 1     width 2
x2 <= 3     YES
x2 <= -2    NO    ->  -2 < x2 <= 3     width 5

area = 2 * 5 = 10
```

### ✅ Answer: **10**

> Every other leaf outputs 1, so `S` is this single
> rectangle. Verified by brute force on a fine grid.

---

## Q13 · 4 mk · SA — logistic regression probability

Given `w` and a test point, `P(y=1|x)` is expressed with
`e` in it; solve for the unknown.

```text
P(y=1|x) = sigma(wᵀx) = 1 / (1 + e^(-wᵀx))

so compute wᵀx first, then match the required form
```

---

## Q17 · 4 mk · MCQ — same as FN 2026 Q2

Perceptron, logistic and SVM all output `w*`.
See [`solved-fn-2026.md`](solved-fn-2026.md) Q2.

## Q18 · 4 mk · MSQ — same as FN 2026 Q4

Multicollinearity: LR may be non-unique, lasso can zero
weights, ridge never does.
See [`most-likely-questions.md`](most-likely-questions.md) §4.
