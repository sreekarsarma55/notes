# 🧪 Patterns from the two solved practice papers

Additional question types beyond the official papers.
Source: `../et-practice/`.

---

## 1. Valid covariance matrix? (symmetric + PSD)

> Which of these are valid covariance matrices for
> centered datasets in `ℝ³`?

```text
C1 = [1 0 0        C2 = [4 0 0       C3 = [5 0 0
      4 3 0              0 3 0             0 0 0
      1 9 2]             0 0 2]            0 0 0]

C4 = [1 0 1
      0 1 0
      1 0 0]
```

**Test, in this order:**

```text
1. SYMMETRIC?  (fastest disqualifier)
2. PSD?        all eigenvalues >= 0
```

```text
C1  not symmetric              -> INVALID
C2  symmetric, eig 4,3,2 > 0   -> valid
C3  symmetric, eig 5,0,0 >= 0  -> valid  (zeros are OK!)
C4  symmetric BUT eig = 1, (1±sqrt5)/2
    and (1-sqrt5)/2 = -0.618 < 0
                                -> INVALID
```

### ✅ Answer: `C₂` and `C₃`

**Key points**
- A **zero** eigenvalue is fine — that is just a
  degenerate/rank-deficient dataset (variance 0 along
  that direction).
- A **negative** eigenvalue is impossible, because
  variance along a direction cannot be negative.
- Same test as **Mercer's condition** for a valid
  kernel: symmetric + PSD.

---

## 2. Expected accuracy of a random classifier

> `k` classes, balanced data. A dummy classifier picks a
> class uniformly at random. Expected accuracy?

```text
P(correct on one point) = 1/k
by linearity of expectation, expected accuracy = 1/k

k = 2  -> 0.5      k = 10 -> 0.1
```

Use it as a sanity floor: any model at `1/k` accuracy has
learnt nothing.

---

## 3. Neural network on flipped / shuffled inputs

> Train a net on images, then turn every image upside
> down (train and test) and retrain from scratch.
> Performance?

### ✅ Same performance as before

**Why:** we only use **fully connected** layers. Every
input neuron connects to every neuron in the first
hidden layer, so the *ordering* of input neurons is
irrelevant — permuting inputs just permutes weights.
The network relearns equally well.

> This would NOT hold for a convolutional network, which
> assumes spatial locality. Our course only covers fully
> connected layers.

---

## 4. Compute the hinge loss of a dataset

> Given `w`, find the total hinge loss for a
> soft-margin linear SVM.

```text
for each point:  loss_i = max(0, 1 - y_i (wᵀ x_i))
total = sum of loss_i
```

```text
y(wᵀx) = 1.5  -> max(0, -0.5) = 0
y(wᵀx) = 1.0  -> max(0,  0  ) = 0
y(wᵀx) = 0.4  -> max(0,  0.6) = 0.6
y(wᵀx) = -2   -> max(0,  3  ) = 3
```

**Trap:** points with `y(wᵀx) >= 1` contribute **exactly
0**, not a small amount. Only points inside or across
the margin add anything.

---

## 5. Probability a random point is classified +1

> A point is drawn uniformly from a square/region. What
> is the probability it is predicted class +1?

```text
It is a GEOMETRY question:

P(+1) = area where wᵀx + b > 0  /  total area
```

Draw the boundary line, work out which part of the
square lies on the positive side, divide by the total
area.

---

## 6. Range of the weight-vector angle

> `w` makes an angle `θ` with the positive `x₁` axis. For
> what range of `θ` are both given points class 1?

```text
w = (cos θ, sin θ)
need wᵀx > 0 for each point x

wᵀx > 0  <=>  the angle between w and x is < 90 degrees
```

Convert each condition into an inequality on `θ`, then
intersect the ranges.

---

## 7. Modified loss functions — derive the gradient

> A per-point constant `cᵢ` is attached to each term of
> the squared-error loss. What is the gradient?

```text
standard      f(w) = Σ (wᵀxᵢ - yᵢ)²
              grad = 2 Σ (wᵀxᵢ - yᵢ) xᵢ

weighted      f(w) = Σ cᵢ (wᵀxᵢ - yᵢ)²
              grad = 2 Σ cᵢ (wᵀxᵢ - yᵢ) xᵢ
```

The weight `cᵢ` simply rides along inside the sum.
Setting the gradient to zero gives a weighted version of
the normal equations.

---

## 8. Modified logistic threshold → boundary equation

> Prediction uses a threshold `t` instead of 0.5. What is
> the decision boundary?

```text
predict 1 when sigma(wᵀx) >= t
   <=>  wᵀx >= ln( t/(1-t) )

so the boundary is  wᵀx = ln( t/(1-t) )
```

At `t = 0.5` this reduces to `wᵀx = 0`, the usual case.
