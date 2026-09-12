# ✅ Solved — MLT End Term, FN T1 2026

Every answer here was checked against the paper's own
marked answer **and** recomputed numerically (23/23
assertions pass). Source: `../pyq/MLT_ET_FN_T1_2026.pdf`.

The FN and AN 2026 papers **share questions** (their Q2
and Q4 are identical), so the bank is reused.

---

## Q2 · 4 mk · MCQ — perceptron vs logistic vs SVM

`x₁ = (1,0)` positive, `x₂ = (−1,0)` negative.
One iteration of perceptron and of logistic gradient
ascent (`η = 1`) from `w⁰ = (0,0)`; SVM trained normally.
Which classifier outputs the max-margin `w*`?

**SVM**

```text
constraints:  y(wᵀx) >= 1
  x1: w1 >= 1
  x2: -(-w1) = w1 >= 1      (same constraint)
minimise ½||w||²  ->  w = (1, 0)
margin width 2/||w|| = 2
```

**Perceptron** (rule: predict +1 when `wᵀx >= 0`)

```text
x1: wᵀx = 0 >= 0 -> +1, correct    -> no update
x2: wᵀx = 0 >= 0 -> +1, but y = -1 -> update
    w = (0,0) + (-1)(-1,0) = (1, 0)
```

**Logistic** — full-batch, `y ∈ {0,1}`, `σ(0) = 0.5`

```text
gradient = Σ (yᵢ - sigma(wᵀxᵢ)) xᵢ   evaluated at w = 0
  point 1: (1 - 0.5)(1, 0)  = (0.5, 0)
  point 2: (0 - 0.5)(-1, 0) = (0.5, 0)
  sum = (1, 0)
w = (0,0) + 1*(1,0) = (1, 0)
```

### ✅ Answer: **All three classifiers output `w*`**

> ⚠️ **Subtlety worth knowing.** "One iteration of
> gradient ascent" means **full batch** — compute the
> gradient over *all* points at `w = 0`, then take one
> step. If you instead update after each point
> (stochastic), you get `(0.8775, 0)` — a different
> vector but the **same direction**, so the same
> classifier. Scaling `w` never changes predictions.

---

## Q6 · 4 mk · SA — SVM prediction from the multipliers

```text
D = { ((1,2), +1), ((2,2), +1),
      ((2,-1), -1), ((1,-2), -1) }
alpha = (2, 0, 3, 0)
x_test = (1, 1)
```

```text
w* = Σ alpha_i y_i x_i
   = 2(+1)(1,2) + 0 + 3(-1)(2,-1) + 0
   = (2,4) - (6,-3)
   = (-4, 7)

w*ᵀ x_test = -4(1) + 7(1) = 3 > 0
```

### ✅ Answer: **1** (i.e. `+1`)

> Only `x₁` and `x₃` are support vectors. There is **no
> bias** in the given formula, which is why
> `Σαᵢyᵢ = 2 − 3 = −1 ≠ 0` here — that constraint only
> applies when a bias term exists. Don't "correct" it.

---

## Q7 · 4 mk · SA — logistic with a 0.7 threshold

Scores `wᵀx`: `−1.2, 0.0, 2.5, 0.4, 0.8`.
Predict `+1` when `P(y=+1|x) >= 0.7`.

```text
sigma(z) >= 0.7  <=>  z >= ln(0.7/0.3) = 0.847

-1.2 -> sigma = 0.231   no
 0.0 -> sigma = 0.500   no
 2.5 -> sigma = 0.924   YES
 0.4 -> sigma = 0.599   no
 0.8 -> sigma = 0.690   NO   <- the trap
```

### ✅ Answer: **1**

> `0.8` feels like it should pass, but `σ(0.8) = 0.690`,
> just under `0.7`. Always convert the threshold to a
> score cut-off first.

---

## Q8 · 4 mk · SA — Beta posterior mean

100 flips, 60 heads. Prior `Beta(10, 40)`.

```text
heads h = 60, tails t = 40
posterior = Beta(10 + 60, 40 + 40) = Beta(70, 80)
mean = 70 / (70 + 80) = 70/150 = 0.4667
```

### ✅ Answer: **0.467** (accepted 0.44 – 0.49)

---

## Q9 & Q10 · 2 mk each · SA — reading a soft-margin figure

One figure, 14 points, two questions. Use the
complementary-slackness table.

| Position | `ξᵢ` | `αᵢ` | count |
|---|---|---|---|
| strictly outside margin | `0` | `= 0` | **6** |
| exactly on the margin | `0` | `0 ≤ αᵢ ≤ C` | 3 |
| inside / violating | `> 0` | `= C` | **5** |

### ✅ Q9 "non-zero slack" = **5**
### ✅ Q10 "definitely `αᵢ = 0`" = **6**

> These are *different rows*. `ξᵢ > 0` ⇔ `αᵢ = C` (row 3),
> while `αᵢ = 0` is row 1. A point exactly on the margin
> is in neither answer.

---

## Q11 & Q12 · 2 mk each — KNN with K = 3

Points: `(1,1)+`, `(2,1)+`, `(2,2)−`, `(5,1)−`,
`(5,4)−`, `(5,5)−`. Test point `(4,1)`.

```text
distance to (4,1):
  (5,1)  1.000   -1
  (2,1)  2.000   +1
  (2,2)  2.236   -1
  (1,1)  3.000   +1
  (5,4)  3.162   -1
  (5,5)  4.123   -1

K = 3  ->  labels {-1, +1, -1}  ->  two vs one
```

### ✅ Q11 Answer: **−1**
### ✅ Q12: "the nearest neighbours are dominated by negative class points"

---

## Q13 · 3 mk · MCQ — comparing two trees

Compare information gain:

```text
IG = H(parent) - Σ (|Dv|/|D|) H(Dv)
H(p) = -p log2 p - (1-p) log2 (1-p)
```

A **pure split** (each child all one class) gives
`H(children) = 0`, so `IG = H(parent)` — the maximum
possible. Whichever tree splits more purely wins.

---

## Q14 · 3 mk · MCQ — bagging vs boosting

### ✅ Answer: **Bagging reduces variance, Boosting reduces bias**

---

## Q15 · 3 mk · MCQ — hard-margin boundary

The boundary is the perpendicular bisector of the two
points, so it passes through their midpoint with `w`
along the line joining them.

### ✅ Answer: **`−x − y = 0`** (i.e. `x + y = 0`)

---

## Q16 · 3 mk · MCQ — PCA keeping all 5 components

### ✅ Answer: **PCA has NOT reduced the dimensionality, because all principal components are retained**

> Keeping every component is just a rotation into an
> uncorrelated basis. Reduction only happens when you
> **drop** components.

---

## Q17 · 3 mk · SA — neural network parameters

Input 5 · three hidden layers of 10 · output 1.
**"Ignore the biases."**

```text
5*10  = 50
10*10 = 100
10*10 = 100
10*1  = 10
------------
total = 260
```

### ✅ Answer: **260**

> With biases it would be **291** (`+10+10+10+1`). The
> paper says to ignore them — this instruction appeared
> in **both** 2026 papers, so expect it again.

---

## Other questions in this paper

```text
Q3  MSQ  which w vectors separate the classes
         -> test sign(wᵀx) against each label
Q4  MSQ  one feature = exact linear combination
         (multicollinearity) -> see archetype 13
Q5  MSQ  perceptron with two valid w's
         -> the result depends on initialisation and
            the ORDER points are presented
```
