# 🚨 Most Likely Questions — read this first

**Five question types appeared in BOTH 2026 papers**
(FN T1 2026 and AN T1 2026). Two were *word-for-word
identical*. That is ~17 of 50 marks from five patterns.

If you learn nothing else, learn these.

---

## 1. Beta posterior mean ⭐⭐⭐

Appeared in **both** papers with different numbers.

```text
prior Beta(a, b)  +  h ones, t zeros
   -> posterior Beta(a + h, b + t)
   -> point estimate = mean = a / (a + b)
      using the NEW a and b
```

**FN 2026:** 100 flips, 60 heads, prior `Beta(10,40)`

```text
h = 60, t = 40
posterior Beta(70, 80)
mean = 70/150 = 0.467
```

**AN 2026:** 20 points, 15 ones, prior `Beta(3,2)`

```text
h = 15, t = 5
posterior Beta(18, 7)
mean = 18/25 = 0.72
```

**Traps**
- 100 flips with 60 heads means `t = 40`, not 100.
- 20 points with 15 ones means `t = 5`.
- The mean uses the **posterior** parameters, not the
  prior.

---

## 2. Neural network parameter count ⭐⭐⭐

Appeared in **both** papers, both times saying
**"Ignore the biases."**

```text
per layer n_in -> n_out
   ignoring biases: n_in * n_out
   with biases:     n_in * n_out + n_out
```

**FN 2026:** `5 -> 10 -> 10 -> 10 -> 1`

```text
5*10 + 10*10 + 10*10 + 10*1
= 50 + 100 + 100 + 10  =  260
(with biases it would be 291)
```

**AN 2026:** `10 -> 30 -> 30 -> 1`

```text
10*30 + 30*30 + 30*1
= 300 + 900 + 30  =  1230
(with biases it would be 1291)
```

**Trap:** read the instruction. Both papers said ignore
biases, but do not assume — check every time.

---

## 3. Perceptron vs logistic vs SVM ⭐⭐⭐

**Identical question in both papers** (FN Q2, AN Q17).

`x₁ = (1,0)` positive, `x₂ = (−1,0)` negative. One
iteration of perceptron and of logistic gradient ascent
(`η = 1`) from `w⁰ = (0,0)`. SVM trained normally.

```text
SVM         w1 >= 1 from both constraints
            minimise ½||w||²  ->  w = (1, 0)

Perceptron  x1: wᵀx = 0 >= 0 -> +1, correct, no update
            x2: wᵀx = 0 >= 0 -> +1 but y = -1, update
                w = (0,0) + (-1)(-1,0) = (1, 0)

Logistic    FULL-BATCH, y in {0,1}, sigma(0) = 0.5
            (1-0.5)(1,0) + (0-0.5)(-1,0) = (1, 0)
            w = (0,0) + 1*(1,0) = (1, 0)
```

### Answer: all three output `w*`

**Traps**
- Logistic uses `y ∈ {0,1}`; the others `y ∈ {−1,+1}`.
- "One iteration of gradient ascent" = **full batch**.
  Updating point-by-point gives `(0.8775, 0)` — a
  different vector, same direction, same classifier.

---

## 4. Multicollinearity MSQ ⭐⭐⭐

**Identical question in both papers** (FN Q4, AN Q18).
One feature is an exact linear combination of others.

```text
TRUE   unregularised LR training MSE <= ridge's
       (ridge only adds a constraint, so it cannot
        fit the training data better)

TRUE   the LR solution may NOT be unique
       (X Xᵀ is singular -> infinitely many solutions)

TRUE   lasso CAN force weights exactly to zero

FALSE  "ridge will always set at least one coefficient
        exactly to zero"   <- ridge NEVER does this
```

---

## 5. Bagging vs boosting ⭐⭐

```text
Bagging reduces VARIANCE.  Boosting reduces BIAS.
```

And the bootstrap probability:

```text
P(a given point NOT in the bag) = (1 - 1/n)^n -> 1/e
   so ~63.2% of distinct points are included
   the ~36.8% left out = OUT-OF-BAG set
```

---

# Also very likely (in one 2026 paper each)

## 6. Naive Bayes free parameters

```text
binary class, d binary features,
class-conditional independence (= Naive Bayes)

   prior P(y=1)              ->  1
   P(xj=1 | y=1), j=1..d     ->  d
   P(xj=1 | y=0), j=1..d     ->  d
                                ------
                         total =  2d + 1
```

`d = 5` gives **11**. (A *full* generative model would
need `2(2^d − 1) + 1 = 63`.)

## 7. SVM figure — count the points

| Position | `ξᵢ` | `αᵢ` |
|---|---|---|
| outside margin, `yf(x) > 1` | `0` | **`= 0`** |
| on the margin, `yf(x) = 1` | `0` | `0 ≤ αᵢ ≤ C` |
| inside/violating, `yf(x) < 1` | **`> 0`** | **`= C`** |

FN 2026 asked both ends off one figure: "non-zero slack"
= 5, "definitely `αᵢ = 0`" = 6.

## 8. SVM prediction from the multipliers

```text
w* = Σ alpha_i y_i x_i        yhat = sign(w*ᵀ x_test)
```

Only `αᵢ > 0` contribute. If the given formula has no
`b`, ignore bias (then `Σαᵢyᵢ = 0` need not hold).

## 9. Logistic threshold → count

```text
sigma(z) >= t   <=>   z >= ln( t/(1-t) )

t=0.5 -> 0      t=0.7 -> 0.847
t=0.8 -> 1.386  t=0.9 -> 2.197
```

FN 2026 trap: `z = 0.8` gives `σ = 0.690 < 0.7`, so it is
**not** class +1.

## 10. Decision tree region area

Trace the path to the leaf with the asked label, collect
the interval on each feature, multiply the widths.

AN 2026: the only `0` leaf needs
`x₁ ≤ 1`, `x₁ > −1`, `x₂ ≤ 3`, `x₂ > −2`

```text
area = (1 - (-1)) * (3 - (-2)) = 2 * 5 = 10
```

## 11. PCA MSQ

```text
TRUE   wᵢᵀ C wᵢ is the variance along wᵢ (= eigenvalue)
TRUE   wᵢᵀ wⱼ = 0 for i != j  (orthogonal)
FALSE  C = (1/n) Xᵀ X     <- X is d x n, so this is
                             n x n. Correct: (1/n) X Xᵀ
FALSE  wᵢᵀ C wᵢ > 0 for all i   <- variance can be 0
                                   (zero eigenvalue)
```

Also: keeping **all** components means PCA has **not**
reduced the dimensionality.

## 12. Identify losses from a graph

```text
hinge        straight line, hits EXACTLY 0 at z = 1
logistic     smooth curve, NEVER reaches 0
0-1          a step at z = 0
exponential  explodes fastest as z -> -inf
squared      U-shape, RISES again after z = 1
```

AN 2026 showed a straight line to 0 at `u=1` (hinge) and
a smooth curve never touching 0 (logistic).
