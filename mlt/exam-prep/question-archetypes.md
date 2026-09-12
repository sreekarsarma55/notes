# 🔁 The 15 Recurring Question Types

Extracted from 7 past end-term papers. Roughly **70% of
the paper** is these patterns. Each entry: the method,
then the trap.

---

## 1. SVM — recover `w` from the multipliers ⭐

**Given** the `αᵢ` and the dataset, predict a test label.

```text
w* = Σᵢ αᵢ yᵢ xᵢ
ŷ  = sign( w*ᵀ x_test )
```

Only terms with `αᵢ > 0` contribute (support vectors).

**Trap:** if the question's formula has **no `b`**, ignore
bias entirely — and then `Σαᵢyᵢ = 0` need *not* hold.
Don't "fix" the data because of it.

---

## 2. SVM — count points from a margin figure ⭐⭐

Two questions are often asked off one figure. The
complementary-slackness table *is* the answer key.

| Position of point | `ξᵢ` | `αᵢ` |
|---|---|---|
| strictly OUTSIDE margin, `yf(x) > 1` | `0` | **`= 0`** |
| exactly ON margin, `yf(x) = 1` | `0` | `0 ≤ αᵢ ≤ C` |
| INSIDE / violating, `yf(x) < 1` | **`> 0`** | **`= C`** |

```text
"non-zero slack"        -> count row 3
"definitely alpha = 0"  -> count row 1
"misclassified"         -> xi > 1 (past the boundary)
```

**Trap:** `ξᵢ > 0` and `αᵢ = 0` count *different* rows.
2026 asked both about the same figure (answers 5 and 6).

---

## 3. SVM — boundary from two points

The max-margin boundary is the **perpendicular bisector**
of the segment joining the two points.

```text
(1,0) positive and (-1,0) negative
-> boundary x1 = 0,  w proportional to (1,0)
-> margin width 2/||w||
```

---

## 4. Perceptron vs logistic vs SVM, one iteration ⭐

Appeared in **both** 2026 papers.

```text
Perceptron   mistake if y(wᵀx) <= 0
             w <- w + y x

Logistic     gradient ASCENT on log-likelihood
             w <- w + eta * Σ (yᵢ - sigma(wᵀxᵢ)) xᵢ
             uses y in {0,1};  sigma(0) = 0.5

SVM          min ½||w||²  s.t.  y(wᵀx) >= 1
```

On symmetric data all three give the same `w`.

**Trap:** logistic needs `y ∈ {0,1}`, the others
`y ∈ {−1,+1}`. Mixing them corrupts everything after.

---

## 5. Logistic + threshold → count points ⭐

**Convert the probability threshold into a score
cut-off. Never eyeball it.**

```text
sigma(z) >= t   <=>   z >= ln( t / (1-t) )

t = 0.5  ->  z >= 0
t = 0.7  ->  z >= 0.847
t = 0.8  ->  z >= 1.386
t = 0.9  ->  z >= 2.197
```

**Trap (2026):** with `t = 0.7`, a score of `0.8` looks
big enough but `σ(0.8) = 0.690 < 0.7`, so it is **not**
class +1. Only `z = 2.5` qualified. Answer was 1.

---

## 6. Beta posterior mean

```text
prior Beta(a, b)  +  h heads, t tails
   -> posterior Beta(a + h, b + t)
   -> mean = a / (a + b)   using the NEW a, b
```

```text
Beta(10,40) + 60 heads/40 tails
   -> Beta(70, 80)
   -> mean = 70/150 = 0.467
```

**Trap:** 100 flips with 60 heads means `t = 40`, not
100. And the mean uses the *posterior* parameters.

---

## 7. KNN from a plot

```text
1. compute SQUARED distances (skip the sqrt,
   the ranking is the same)
2. take the K smallest
3. majority vote
```

A follow-up MCQ usually just restates it: "neighbours
are dominated by class X".

**Trap:** count carefully — a point that looks far in
one axis can be nearer overall. Use odd `K`, and if the
vote ties the answer is "Tie".

---

## 8. Decision trees

**Information gain**

```text
IG = H(parent) - Σ_children (|Dv|/|D|) * H(Dv)

H(p) = -p log2(p) - (1-p) log2(1-p)
H(0) = H(1) = 0        (pure)
H(0.5) = 1 bit         (maximum)
H(0.75) = 0.811
```

A **pure split gives IG = H(parent)**, the maximum, and
beats any impure split. `IG >= 0` always.

**Region area:** the tree makes axis-parallel
rectangles. Add the areas of the boxes with the asked
label.

---

## 9. Bagging vs boosting (near-guaranteed 3 mk)

> **Bagging reduces VARIANCE. Boosting reduces BIAS.**

| | Bagging | Boosting |
|---|---|---|
| training | parallel | sequential |
| base model | deep trees | stumps |
| reduces | variance | bias |
| aggregation | equal vote | weighted `α_t` |
| example | Random Forest | AdaBoost |

AdaBoost weight:

```text
alpha_t = 0.5 * ln( (1 - eps_t) / eps_t )

eps = 0.2 -> 0.693      eps = 0.5 -> 0
eps = 0.3 -> 0.424      eps -> 0  -> infinity
```

---

## 10. Bootstrap probability

```text
P(a given point NOT in the bag) = (1 - 1/n)^n
                               -> 1/e = 0.368

so about 63.2% of distinct points are included,
and the ~36.8% left out are the OUT-OF-BAG set
```

---

## 11. PCA conceptual (in every paper)

```text
variance along a PC   = its eigenvalue
total variance        = trace = sum of eigenvalues
fraction explained    = (l1+...+lk)/(l1+...+ld)
projection            = wᵀx
data lies on a line   -> 2nd eigenvalue = 0
```

**Trap (2026):** keeping **all** components means PCA has
**NOT** reduced dimensionality — it only rotated /
de-correlated the data.

---

## 12. Neural network parameter count ⚠️

```text
per layer n_in -> n_out
   with biases:     n_in*n_out + n_out
   ignoring biases: n_in*n_out
```

```text
5 -> 10 -> 10 -> 10 -> 1, IGNORING biases
   5*10 + 10*10 + 10*10 + 10*1
   = 50 + 100 + 100 + 10 = 260
```

**Trap:** 2026 said **"ignore the biases"** in both
papers. With biases the same net is 291. Read the line.

---

## 13. Multicollinearity MSQ ⭐

One feature is an exact linear combination of others.

```text
TRUE   unregularised LR training MSE <= ridge's
TRUE   the LR solution may NOT be unique (XXᵀ singular)
TRUE   lasso CAN force weights exactly to zero
FALSE  ridge sets a coefficient exactly to zero  <- never
```

Appeared in **both** 2026 papers.

---

## 14. Polynomial kernel MSQ

For `K(x,y) = (xᵀy)^p`:

```text
p even              -> K >= 0 for all x, y
x, y orthogonal     -> K = 0
"K can never be 0"  -> FALSE
```

---

## 15. Identify losses from a graph

Let `z = y(wᵀx)` be the margin.

```text
hinge        max(0, 1-z)   hits exactly 0 at z = 1
logistic     log(1+e^-z)   smooth, never touches 0
0-1          step at z = 0
exponential  e^-z          explodes fastest as z -> -inf
squared      (1-z)^2       U-shape, RISES again after z=1
```

**Trap:** only hinge and exponential are true upper
bounds on 0-1 loss. Natural-log logistic is not
(`log 2 = 0.693 < 1` at `z = 0`); it is only an upper
bound in base 2. Perceptron loss `max(0,-z)` is 0 at
`z = 0`, so also not a bound.

---

## Quick numeric recall

```text
ln 2 = 0.693      ln 3 = 1.099      ln 4 = 1.386
1/e = 0.368       1 - 1/e = 0.632
sigma(0) = 0.5    sigma(0.8) = 0.690
sigma(1) = 0.731  sigma(2.5) = 0.924
H(0.5) = 1        H(0.75) = 0.811
ln(7/3) = 0.847
```
