# 📗 Week 2 — Kernel PCA

## 1. What's wrong with plain PCA?

**Problem A — PCA is linear.** It only finds straight-line directions. If the data has a curved structure (e.g. two concentric circles, or a parabola), no straight line captures it.

![Concentric rings: not linearly separable in 2D, separable after a feature map](images/kernel_pca.png)

The rings on the left cannot be separated by any straight line, so PCA is helpless. But after mapping each point to the feature `x1^2 + x2^2` (its squared radius), the two classes become **linearly separable** (right panel).

**Problem B — time complexity.** Plain PCA builds a `d x d` covariance matrix and eigen-decomposes it in `O(d^3)`. When `d` is huge, this is infeasible.

## 2. Feature transformation

Escape plan: map the data to a higher-dimensional space where it *becomes* linearly structured, then do ordinary PCA there.

```
phi :  R^d  ->  R^D   (D usually much larger)
x   |->  phi(x)
```

Example (concentric circles → 3D):
```
phi(x) = ( x1^2 , x2^2 , sqrt(2) x1 x2 )
```
The radius information becomes a coordinate axis, so a flat plane can separate the rings.

## 3. The kernel trick

**The catch:** the feature space can be enormous or even infinite-dimensional, so computing `phi(x)` explicitly is impossible/expensive.

**The rescue:** PCA only ever needs **inner products** `phi(x_i)^T phi(x_j)`. A **kernel function** gives that directly, without computing `phi`:

```
K(x_i, x_j) = phi(x_i)^T phi(x_j)
```

Verify with the example above:
```
phi(a)^T phi(b) = a1^2 b1^2 + a2^2 b2^2 + 2 a1a2 b1b2 = (a1 b1 + a2 b2)^2 = (a^T b)^2
```
So `K(a,b) = (a^T b)^2` computed in the *original* space gives the same result — no trip to 3D needed. **That is the kernel trick.**

## 4. Common kernels

| Kernel | Formula | Notes |
|--------|---------|-------|
| Linear | `K = x^T y` | = plain PCA |
| Polynomial | `K = (x^T y + c)^p` | degree `p`, constant `c >= 0` |
| RBF / Gaussian | `K = exp(-||x - y||^2 / (2 sigma^2))` | **infinite-dimensional** feature space |

**Polynomial kernel feature-space dimension** (input dimension `d`):
```
inhomogeneous (x^T y + c)^p  ->  dim = C(d + p, p)      (all monomials of degree <= p)
homogeneous   (x^T y)^p      ->  dim = C(d + p - 1, p)  (monomials of degree exactly p)
```
Example: parabola data, `d = 2`, `p = 2`, inhomogeneous → `C(4,2) = 6` features `{1, x1, x2, x1^2, x2^2, x1 x2}`.

## 5. The Kernel PCA procedure

1. Build the **kernel matrix** `K` of size **n x n** (n = number of points), `K[i][j] = K(x_i, x_j)`.
2. **Center the kernel matrix** (we can't center `phi(x)` directly, so we center K instead):
   ```
   K' = K - 1n K - K 1n + 1n K 1n      (1n = n x n matrix of 1/n)
   ```
3. Eigen-decompose `K'` to get the components in feature space.

## 6. Complexity punchline

| | Plain PCA | Kernel PCA |
|--|-----------|------------|
| Matrix | covariance, **d x d** | kernel, **n x n** |
| Cost | O(d^3) | O(n^3) |
| Best when | n large, d small | **d large (even infinite)**, n manageable |

Kernel PCA's cost depends on **n**, not on `d` or the feature-space dimension `D` — this is why RBF (infinite D) is still tractable.

## 7. Valid kernels — Mercer's condition

For `K` to correspond to some valid `phi` (a genuine inner product), the kernel matrix must be:
```
1. Symmetric:              K(x, y) = K(y, x)
2. Positive semi-definite: all eigenvalues of K >= 0
```
This is **Mercer's theorem**. If a proposed kernel is **not symmetric**, it is immediately invalid (e.g. a function with an `x1^3 x2` term but no matching `x1 x2^3` term).

## 8. Worked example — RBF kernel value

Points `a = (1,0)`, `b = (0,1)`, `sigma^2 = 1`:
```
||a - b||^2 = 1 + 1 = 2
K(a,b) = exp(-2 / 2) = exp(-1) ~= 0.368
```
Sanity check: `a = b` → `||.||^2 = 0` → `K = 1` (max similarity). RBF acts like a similarity score in `[0, 1]`.

## 9. Common exam traps

| Question | Answer |
|----------|--------|
| Size of the kernel matrix? | **n x n** (points), not d x d. |
| Do we compute phi(x)? | **No** — only `K(x, y)`. |
| Which kernel = infinite dims? | **RBF / Gaussian.** |
| Requirement for a valid kernel? | **Symmetric + PSD** (Mercer). |
| Do we skip centering? | **No** — center the *kernel matrix*. |
| When beats plain PCA? | Non-linear data, or huge `d`. |
