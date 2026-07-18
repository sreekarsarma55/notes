# ⚡ MLT Quiz 1 — Cheat Sheet

One-page recall for Weeks 1–4. Read this last, right before the exam.

---

## PCA (Week 1)

```text
center:        x_i <- x_i - mu
covariance:    C = (1/n) X X^T            (d × d, symmetric, PSD)
components:    eigenvectors of C
variance:      = eigenvalue λ
proj / proxy:  z = w^T x
var explained: (λ₁ + ... + λₖ) / (λ₁ + ... + λ_d)
recon error:   λₖ₊₁ + ... + λ_d           (sum of dropped eigenvalues)
compression:   ratio = (n × d) / [k(n + d)]
```

- Data on a line → 2nd eigenvalue = 0
- PCs are orthogonal → uncorrelated
- Principal components are unique up to sign
- PCA is unsupervised

---

## Kernel PCA (Week 2)

```text
kernel:        K(x,y) = φ(x)^T φ(y)      (never compute φ)
poly:          (x^T y + c)^p
RBF:           exp(-||x-y||² / 2σ²)

kernel matrix: n × n (NOT d × d); must be centered
valid kernel:  symmetric AND positive semi-definite (Mercer)
poly dim:      inhomogeneous: C(d+p, p)
               homogeneous:   C(d+p-1, p)
cost:          O(n³), depends on n not d
RBF:           infinite-dimensional feature space
```

---

## K-means (Week 3)

```text
objective:     J = Σ_k Σ_{x∈C_k} ||x - μ_k||²
Lloyd:         assign → update centroid = mean → repeat
converges:     YES, but to a LOCAL minimum
clusters:      spherical / convex
fails on:      rings, moons, unequal cluster sizes
boundary:      perpendicular bisector (straight line)
k-means++:     P(pick x) = D(x)² / Σ D(.)²
choose K:      elbow method
               J always decreases with K
               J = 0 when K = n
```

---

## Estimation / EM (Week 4)

```text
MLE:           maximize ℓ(θ) = Σ_i log P(x_i | θ)

Coin:
    p̂ = h / n

Gaussian:
    μ = mean
    σ² = (1/n) Σ(x - μ)²      (biased estimator)

Bayesian:
    posterior ∝ likelihood × prior

Beta-Bernoulli:
    Beta(a,b) + h ones, t zeros
    → Beta(a+h, b+t)

Beta mean:
    a / (a+b)

GMM:
    P(x) = Σ_k π_k N(x | μ_k, Σ_k)
    soft, elliptical clusters

E-step:
    r_ik = π_k N_ik / Σ_j π_j N_ij
    Σ_k r_ik = 1

M-step:
    μ_k, Σ_k weighted by r
    π_k = N_k / n
    N_k = Σ_i r_ik

EM:
    increases log-likelihood every iteration
    converges to a LOCAL maximum

Jensen:
    convex:  f(E[X]) ≤ E[f(X)]
    log is concave → used to derive EM lower bound
```

---

## 🔢 Numbers Worth Remembering

| Setup | Result |
|-------|--------|
| Compression ratio ≥ 1.4, n = 1000, d = 10 | k = 7 (`10000 / (1010k)`) |
| Minimum variance ratio over 5 PCs | 1/5 = 0.2 |
| Beta(10,5) → Beta(30,45), number of zeros | 40 |
| MLE of `θx^(θ−1)`, x = 1/e^i (i = 1..4) | θ = 0.4 |
| Polynomial kernel, d = 2, p = 2 | Feature dimension = 6 |

---

## ⏱️ 60-Second Priority Order

1. **K-means++:** `D(x)²` sampling probability
2. **PCA:** variance = eigenvalue; data on a line → 2nd eigenvalue = 0
3. **MLE:** coin → `h/n`; Gaussian → mean & variance
4. **EM:** E-step responsibilities; soft vs. hard clustering
5. **Kernel methods:** valid kernel = symmetric + PSD; feature dimension; kernel matrix is `n × n`