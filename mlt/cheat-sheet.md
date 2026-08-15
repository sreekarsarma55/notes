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

## Linear Regression (Week 5)

```text
setup:         X is d × n (columns = points), y ∈ ℝⁿ, w ∈ ℝᵈ
prediction:    ŷ = w^T x        all at once: ŷ = X^T w
loss:          f(w) = ‖X^T w − y‖²
gradient:      ∇f = 2X(X^T w − y)

normal equations:
    X X^T w = X y
    w* = (X X^T)⁻¹ X y          (X X^T is d × d)
    singular → infinitely many solutions, use pseudo-inverse

geometric:     least squares = orthogonal projection of y
               onto span of the rows of X
               residual ⟂ subspace  ⇒  X(X^T w − y) = 0

gradient descent:
    w^(t+1) = w^(t) − η · 2X(X^T w^(t) − y)
    convex ⇒ GLOBAL optimum  (contrast: K-means / EM = local)
    η too large → diverges ; too small → slow
    cost: closed form O(d³)  vs  GD O(nd) per step

kernel regression:
    w = Xα ,  K = X^T X  (n × n)
    α = K⁻¹ y
    ŷ(x) = Σᵢ αᵢ K(xᵢ, x)
    d ↔ n trade-off, same as PCA vs Kernel PCA

probabilistic view:
    yᵢ = w^T xᵢ + εᵢ ,  εᵢ ~ N(0, σ²)
    ⇒ MLE ≡ least squares   (why squared error is used)
```

---

## Ridge & Lasso (Week 6)

```text
goodness of the MLE:
    w_ML is UNBIASED:  E[w_ML] = w
    MSE(w_ML) = σ² · tr((X X^T)⁻¹) = σ² Σᵢ 1/λᵢ
    small λᵢ  ⇒  MSE explodes  (collinear features, d ≳ n)
    achieves Cramér-Rao bound ⇒ best UNBIASED
    but a BIASED estimator can have lower MSE  → ridge

cross-validation:
    K-fold: train on K−1 folds, validate on the held-out fold, average
    LOOCV = K = n
    used to CHOOSE λ  (never pick λ by training error)

Bayesian view:
    prior w ~ N(0, γ² I),  likelihood y|w ~ N(X^T w, σ² I)
    MAP  ⇒  minimize ‖X^T w − y‖² + (σ²/γ²)‖w‖²
    ⇒ RIDGE with  λ = σ²/γ²

ridge (ℓ2):
    minimize ‖X^T w − y‖² + λ‖w‖²
    w_ridge = (X X^T + λI)⁻¹ X y
    eigenvalues become λᵢ + λ > 0  ⇒  ALWAYS invertible, unique
                                      (works even when d > n)
    λ → 0 ⇒ w_ML ;  λ → ∞ ⇒ 0

ridge vs least squares (eigenbasis, X X^T = Q Λ Q^T):
    w_ridge = Q (Λ + λI)⁻¹ Λ Q^T w_ML
    per coordinate:   βᵢ = [λᵢ / (λᵢ + λ)] · αᵢ
    small λᵢ → shrunk MOST (exactly the noisy directions)
    MSE(λ) = Σᵢ [ σ²λᵢ/(λᵢ+λ)²  +  λ²αᵢ²/(λᵢ+λ)² ]
                  └variance┘        └─bias²─┘
    THEOREM: ∃ λ > 0 with MSE(w_ridge) < MSE(w_ML)

lasso (ℓ1):
    minimize ‖X^T w − y‖² + λ‖w‖₁
    NO closed form (|w| not differentiable at 0) → iterative
    orthonormal case (X X^T = I), soft-thresholding:
        (w_lasso)ᵢ = sign((w_ML)ᵢ) · max(|(w_ML)ᵢ| − λ/2, 0)
        (w_ridge)ᵢ = (w_ML)ᵢ / (1 + λ)
    SPARSE: coefficients become exactly 0 → feature selection
    why: ℓ1 ball is a DIAMOND, corners sit on the axes
    lasso ⇔ Laplace prior ;  ridge ⇔ Gaussian prior
```

| | Ridge (ℓ2) | Lasso (ℓ1) |
|--|-----------|------------|
| closed form | ✅ | ❌ |
| sparsity | ❌ | ✅ |
| prior | Gaussian | Laplace |
| shape | circle | diamond |

---

## Classification: KNN & Trees (Week 7)

```text
binary classification:
    y ∈ {0,1},  learn h : ℝᵈ → {0,1}
    0-1 loss:  error(h) = (1/n) Σᵢ 𝟙(h(xᵢ) ≠ yᵢ)
    NON-convex + NON-differentiable ⇒ NO gradient descent
    number of classifiers on d binary features = 2^(2ᵈ)
    Bayes optimal:  h*(x) = argmax_y P(y | x)   (Bayes error = irreducible floor)

KNN:
    training: store the data (LAZY learner, non-parametric)
    predict:  k nearest points → MAJORITY vote
    cost:  train O(1),  PREDICT O(nd) per query,  storage O(nd)
    k = 1  → training error 0, jagged, HIGH variance, overfits
    large k → smooth, high bias, low variance ;  k = n → majority class
    choose k by cross-validation (use ODD k for binary)
    k = 1 boundary = Voronoi cells → PIECEWISE LINEAR
    MUST normalise features (Euclidean distance is scale-sensitive)
    curse of dimensionality: (d_max − d_min)/d_min → 0 as d → ∞
    Cover-Hart: 1-NN error ≤ 2 × Bayes error as n → ∞

decision trees:
    internal node = test on one feature, leaf = label
    predict = walk root → leaf, O(depth) ; boundaries AXIS-PARALLEL
    entropy:  H(p) = −p log₂p − (1−p) log₂(1−p)
              H = 0 pure ;  H = 1 bit at p = 0.5 (max)
    Gini:     1 − Σ_c p_c²  =  2p(1−p)  for binary
    information gain:
        IG = H(parent) − Σ_children (|Dᵥ|/|D|) · H(Dᵥ)
        pick the split with MAX IG ;  IG ≥ 0 always
    numeric feature: candidate thresholds = midpoints of sorted values
    GREEDY (ID3/CART) → not globally optimal ; optimal tree is NP-hard
    overfits: full tree → 0 training error
    fixes: max depth, min samples/leaf, min gain, PRUNING (tune by CV)

generative vs discriminative:
    generative:      model P(x|y) and P(y), classify by Bayes
                     h(x) = argmax_y P(x|y) P(y)
                     CAN generate new data
                     e.g. Naive Bayes, GMM, LDA
    discriminative:  model P(y|x) or h(x) directly, CANNOT generate
                     e.g. logistic regression, SVM, trees, KNN
```

| | Generative | Discriminative |
|--|-----------|----------------|
| models | `P(x\|y)`, `P(y)` | `P(y\|x)` |
| generate data | ✅ | ❌ |
| assumptions | stronger | weaker |
| better with | small data | large data |

---

## Naive Bayes (Week 8)

```text
full generative model (binary x ∈ {0,1}ᵈ):
    P(x|y) needs 2ᵈ − 1 parameters PER CLASS
    total = 2(2ᵈ − 1) + 1        ← EXPONENTIAL, infeasible
    MLE by counting ⇒ almost every x gets probability exactly 0

chain rule (no assumption yet, still exponential):
    P(x|y) = P(x₁|y) · P(x₂|x₁,y) · ... · P(x_d|x₁..x_{d−1},y)

NAIVE BAYES assumption — conditional independence GIVEN y:
    P(x|y) = Π_j P(xⱼ|y)
    (NOT independence overall — only within each class)
    total parameters = 2d + 1     ← LINEAR

MLE (just counting, no optimization):
    p̂    = n₁ / n
    p̂ⱼ¹  = #(y=1 and xⱼ=1) / n₁
    p̂ⱼ⁰  = #(y=0 and xⱼ=1) / n₀

predict:  argmax_y  P(y) · Π_j P(xⱼ|y)
    binary feature:  P(xⱼ|y) = (pⱼ^y)^{xⱼ} (1 − pⱼ^y)^{1−xⱼ}

PITFALLS:
    zero probability: scores are a PRODUCT ⇒ one 0 annihilates everything
      Laplace (add-one):  p̂ⱼ^y = (count + 1)/(n_y + 2)
      general (K values): (count + α)/(n_y + α·K)
    independence usually FALSE ⇒ diagonal covariance only (axis-aligned)
      probabilities miscalibrated, but the ARGMAX is often still right
    underflow ⇒ work in log space:
      log score(y) = log P(y) + Σ_j log P(xⱼ|y)

DECISION FUNCTION IS LINEAR (binary features):
    log[P(y=1|x)/P(y=0|x)] = w₀ + Σ_j wⱼ xⱼ

              pⱼ¹ (1 − pⱼ⁰)
    wⱼ = log ───────────────      ← log-odds ratio;  = 0 when pⱼ¹ = pⱼ⁰
              pⱼ⁰ (1 − pⱼ¹)

    w₀ = log[p/(1−p)] + Σ_j log[(1 − pⱼ¹)/(1 − pⱼ⁰)]

    predict y = 1  ⇔  w^T x + w₀ > 0

GAUSSIAN NAIVE BAYES (continuous x):
    P(xⱼ|y) = N(xⱼ ; μⱼ^y, (σⱼ^y)²)   ⇒ DIAGONAL covariance
    μ̂ⱼ^y, (σ̂ⱼ^y)² = mean/variance of feature j within class y
    shared variances (σⱼ¹ = σⱼ⁰)  → xⱼ² CANCELS → LINEAR boundary
                                     wⱼ = (μⱼ¹ − μⱼ⁰)/σⱼ²
    per-class variances            → xⱼ² SURVIVES → QUADRATIC boundary
    (mirrors LDA vs QDA)
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