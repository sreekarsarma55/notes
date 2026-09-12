# ⚡ MLT Quiz 2 — Cheat Sheet (Weeks 5–8)

Scope: **supervised learning** — regression (5–6) and classification (7–8).
Read this last, right before the exam. Full-course version: [`cheat-sheet.md`](cheat-sheet.md).

```text
Week 5  Linear regression      → normal equations, geometry, GD, kernel, MLE view
Week 6  Regularization         → is least squares good? → ridge, lasso, CV
Week 7  Classification         → 0-1 loss, KNN, decision trees, gen vs disc
Week 8  Naive Bayes            → the generative classifier (boundary is LINEAR)
```

Notation used throughout Weeks 5–6: `X` is **d × n** (columns = data points), `y ∈ ℝⁿ`, `w ∈ ℝᵈ`.

---

## Week 5 — Linear Regression

```text
predict:   ŷ = w^T x          all at once:  ŷ = X^T w
loss:      f(w) = ‖X^T w − y‖²
gradient:  ∇f = 2X(X^T w − y)

NORMAL EQUATIONS
    X X^T w = X y
    w* = (X X^T)⁻¹ X y             (X X^T is d × d)
    singular ⇒ infinitely many solutions → use pseudo-inverse

GEOMETRIC VIEW
    least squares = orthogonal PROJECTION of y onto span(rows of X)
    residual ⟂ subspace  ⇒  X(X^T w − y) = 0   ⇒  same normal equations

GRADIENT DESCENT
    w ← w − η · 2X(X^T w − y)
    CONVEX ⇒ GLOBAL optimum      (contrast K-means / EM = local only)
    η too large → diverges ;  too small → slow
    cost: closed form O(d³)  vs  GD O(nd) per step

KERNEL REGRESSION
    w = Xα ,  K = X^T X   (n × n)
    α = K⁻¹ y
    ŷ(x) = Σᵢ αᵢ K(xᵢ, x)
    d ↔ n trade-off, same as PCA vs Kernel PCA

PROBABILISTIC VIEW
    yᵢ = w^T xᵢ + εᵢ ,  εᵢ ~ N(0, σ²)
    ⇒ MLE ≡ least squares      ← this is WHY squared error is used
```

---

## Week 6 — Ridge & Lasso

```text
GOODNESS OF THE MLE
    w_ML is UNBIASED:  E[w_ML] = w
    MSE(w_ML) = σ² · tr((X X^T)⁻¹) = σ² Σᵢ 1/λᵢ     λᵢ = eigenvalues of X X^T
    one small λᵢ ⇒ MSE EXPLODES  (collinear features, d ≳ n)
    achieves Cramér-Rao ⇒ best UNBIASED estimator
    but a BIASED estimator can beat it in MSE  → ridge

CROSS-VALIDATION
    K-fold: train on K−1 folds, validate on the held-out one, average
    LOOCV = K = n
    used to CHOOSE λ  —  NEVER pick λ by training error (always prefers λ=0)

BAYESIAN VIEW
    prior w ~ N(0, γ²I),  likelihood y|w ~ N(X^T w, σ²I)
    MAP ⇒ minimize ‖X^T w − y‖² + (σ²/γ²)‖w‖²
    ⇒ RIDGE with  λ = σ²/γ²

RIDGE (ℓ2)
    minimize ‖X^T w − y‖² + λ‖w‖²
    w_ridge = (X X^T + λI)⁻¹ X y
    eigenvalues become λᵢ + λ > 0 ⇒ ALWAYS invertible & unique (even if d > n)
    λ → 0 ⇒ w_ML ;   λ → ∞ ⇒ 0

SHRINKAGE (eigenbasis, X X^T = Q Λ Q^T)
    w_ridge = Q (Λ + λI)⁻¹ Λ Q^T w_ML
    per coordinate:   βᵢ = [λᵢ / (λᵢ + λ)] · αᵢ        ∈ (0, 1)
    SMALL λᵢ shrink MOST  ← exactly the noisy directions that blew up the MSE
    MSE(λ) = Σᵢ [ σ²λᵢ/(λᵢ+λ)²  +  λ²αᵢ²/(λᵢ+λ)² ]
                  └variance┘        └─bias²─┘
    THEOREM: ∃ λ > 0 with MSE(w_ridge) < MSE(w_ML)

LASSO (ℓ1)
    minimize ‖X^T w − y‖² + λ‖w‖₁
    NO closed form (|w| not differentiable at 0) → iterative
    orthonormal case (X X^T = I):
        lasso:  (w_lasso)ᵢ = sign((w_ML)ᵢ) · max(|(w_ML)ᵢ| − λ/2, 0)   ← soft-threshold
        ridge:  (w_ridge)ᵢ = (w_ML)ᵢ / (1 + λ)
    SPARSE: coefficients become exactly 0 ⇒ feature selection
    why: the ℓ1 ball is a DIAMOND, its corners lie ON THE AXES
```

---

## Week 7 — Classification, KNN & Trees

```text
BINARY CLASSIFICATION
    y ∈ {0,1},  h : ℝᵈ → {0,1}
    0-1 loss:  error(h) = (1/n) Σᵢ 𝟙(h(xᵢ) ≠ yᵢ)
    NON-convex + NON-differentiable ⇒ NO gradient descent  ← shapes the whole week
    number of classifiers on d binary features = 2^(2ᵈ)
    Bayes optimal: h*(x) = argmax_y P(y|x) ;  Bayes error = irreducible floor

KNN
    training: store the data  (LAZY, non-parametric)
    predict:  k nearest points → MAJORITY vote
    cost:  train O(1),  PREDICT O(nd) per query,  storage O(nd)
    k = 1   → training error 0, jagged, HIGH variance, OVERFITS
    large k → smooth, high bias, low variance ;  k = n → majority class
    choose k by CV (use ODD k for binary to avoid ties)
    k = 1 boundary = Voronoi cells ⇒ PIECEWISE LINEAR
    MUST normalise features (Euclidean distance is scale-sensitive)
    curse of dimensionality: (d_max − d_min)/d_min → 0 as d → ∞
    Cover-Hart: 1-NN error ≤ 2 × Bayes error as n → ∞

DECISION TREES
    predict = walk root → leaf, O(depth) ;  boundaries AXIS-PARALLEL rectangles
    entropy:  H(p) = −p log₂p − (1−p) log₂(1−p)
              H = 0 when pure ;  H = 1 bit at p = 0.5 (maximum)
    Gini:     1 − Σ_c p_c²  =  2p(1−p)  for binary
    information gain:
        IG = H(parent) − Σ_children (|Dᵥ|/|D|) · H(Dᵥ)
        pick the split with MAX IG ;  IG ≥ 0 always
    numeric feature: candidate thresholds = midpoints of sorted values
    GREEDY (ID3/CART) ⇒ NOT globally optimal ; the optimal tree is NP-hard
    overfits: full tree ⇒ 0 training error
    fixes: max depth, min samples/leaf, min gain, PRUNING (all tuned by CV)

GENERATIVE vs DISCRIMINATIVE
    generative:      model P(x|y) and P(y), classify by argmax_y P(x|y)P(y)
                     CAN generate new data  —  Naive Bayes, GMM, LDA
    discriminative:  model P(y|x) or h(x) directly, CANNOT generate
                     —  logistic regression, SVM, trees, KNN
```

---

## Week 8 — Naive Bayes

```text
FULL generative model (binary x):  2(2ᵈ − 1) + 1 parameters   ← EXPONENTIAL
NAIVE BAYES assumption — conditional independence GIVEN y:
    P(x|y) = Π_j P(xⱼ|y)
    (NOT independence overall — only WITHIN each class)
    parameters = 2d + 1                                       ← LINEAR

MLE — just counting, no optimization:
    p̂ = n₁/n ,   p̂ⱼ¹ = #(y=1 & xⱼ=1)/n₁ ,   p̂ⱼ⁰ = #(y=0 & xⱼ=1)/n₀

predict:  argmax_y  P(y) · Π_j P(xⱼ|y)
    binary feature:  P(xⱼ|y) = (pⱼ^y)^{xⱼ} (1 − pⱼ^y)^{1−xⱼ}

PITFALLS
    zero probability: scores are a PRODUCT ⇒ ONE zero annihilates everything
        Laplace (add-one):  p̂ⱼ^y = (count + 1)/(n_y + 2)
        general (K values): (count + α)/(n_y + α·K)
    independence usually FALSE ⇒ only DIAGONAL covariance (axis-aligned)
        probabilities miscalibrated, but the ARGMAX is often still right
    underflow ⇒ work in log space:  log P(y) + Σ_j log P(xⱼ|y)

DECISION FUNCTION IS LINEAR
    log[P(y=1|x)/P(y=0|x)] = w₀ + Σ_j wⱼ xⱼ

              pⱼ¹ (1 − pⱼ⁰)
    wⱼ = log ───────────────         ← log-odds ratio;  = 0 when pⱼ¹ = pⱼ⁰
              pⱼ⁰ (1 − pⱼ¹)

    w₀ = log[p/(1−p)] + Σ_j log[(1 − pⱼ¹)/(1 − pⱼ⁰)]
    predict y = 1  ⇔  w^T x + w₀ > 0

GAUSSIAN NAIVE BAYES (continuous x)
    P(xⱼ|y) = N(xⱼ ; μⱼ^y, (σⱼ^y)²)  ⇒ DIAGONAL covariance
    μ̂ⱼ^y, (σ̂ⱼ^y)² = mean/variance of feature j within class y
    shared variances (σⱼ¹ = σⱼ⁰) → xⱼ² CANCELS  → LINEAR boundary
                                    wⱼ = (μⱼ¹ − μⱼ⁰)/σⱼ²
    per-class variances            → xⱼ² SURVIVES → QUADRATIC boundary
    (mirrors LDA vs QDA)
```

---

## 🔗 Cross-cutting tables (Q2 loves these)

### Shape of the decision boundary

| Method | Boundary |
|---|---|
| Linear regression / linear classifier | hyperplane |
| Kernel regression | non-linear curve |
| 1-NN | **piecewise linear** (Voronoi cells) |
| Decision tree | **axis-parallel** rectangles |
| Naive Bayes, binary features | **LINEAR** |
| Gaussian NB, **shared** variances | **LINEAR** |
| Gaussian NB, **per-class** variances | **QUADRATIC** |

### Closed form or iterative?

| Method | Solution |
|---|---|
| Least squares | ✅ `(X X^T)⁻¹ X y` |
| Ridge | ✅ `(X X^T + λI)⁻¹ X y` |
| Kernel regression | ✅ `K⁻¹ y` |
| Naive Bayes | ✅ counting |
| **Lasso** | ❌ iterative only |
| Decision tree | ❌ greedy recursion |
| KNN | — no training at all |

### Global or local optimum?

| Method | Optimum |
|---|---|
| Least squares / ridge / lasso | **GLOBAL** (convex) |
| Decision tree | greedy — not optimal (NP-hard) |
| K-means / EM *(Weeks 3–4)* | **LOCAL** only |

### Cost — does it scale with `d` or `n`?

| Method | Cost |
|---|---|
| Least squares / ridge | `O(d³)` — inverts a `d × d` matrix |
| Kernel regression | `O(n³)` — inverts an `n × n` matrix |
| Gradient descent | `O(nd)` per step |
| KNN | `O(nd)` **per query** |
| Naive Bayes | `O(nd)` train, `O(d)` predict |

### Every prior/assumption → what it produces

| Assumption | Result |
|---|---|
| Gaussian **noise on `y`** | squared-error loss (Week 5) |
| Gaussian **prior on `w`** | **ridge** (ℓ2), `λ = σ²/γ²` |
| Laplace **prior on `w`** | **lasso** (ℓ1) |
| Conditional independence of features | **Naive Bayes** |
| Shared class variances | linear boundary |

### Every hyperparameter is chosen the same way

```text
λ (ridge / lasso) ,  k (KNN) ,  tree depth / min samples ,  α (smoothing)
                        ↓
              CROSS-VALIDATION      (never training error)
```

---

## 🔢 Numbers worth remembering

| Setup | Result |
|---|---|
| `X = [1 2 3]`, `y = (1,2,2)` | `w_ML = 11/14 = 0.7857` |
| same, ridge `λ = 2` | `w = 11/16 = 0.6875` |
| eigenvalues `(4, 0.1)`, `σ² = 1` | `MSE(w_ML) = 10.25` (the 0.1 causes 97.6%) |
| shrink factors at `λ = 0.9` | `4/4.9 = 0.816` and `0.1/1.0 = 0.100` |
| lasso, `w_ML = (3, −0.4, 0.1)`, `λ = 1` | `(2.5, 0, 0)` — sparse |
| ridge, same `λ = 1` | `(1.5, −0.2, 0.05)` — all nonzero |
| `H(3/4)` | `0.811` bits |
| parent `4+/4−`, split `(3+,1−)&(1+,3−)` | `IG = 0.189` |
| parent `4+/4−`, split `(4+,0−)&(0+,4−)` | `IG = 1.000` (max) |
| NB params, `d = 10` | `2,047` full vs `21` naive |
| NB params, `d = 30` | `2,147,483,647` vs `61` |
| NB weights (smoothed example) | `w₁ = log 12 = 2.485`, `w₂ = log 1.5 = 0.405`, `w₀ = −1.139` |
| `P(y=1)=0.3, P(x\|y=1)=0.8` vs `0.7, 0.2` | joints `0.24` vs `0.14` → `y=1`, posterior `0.632` |

---

## ⏱️ 60-second priority order

1. **Normal equations** `(X X^T)⁻¹ X y` and **ridge** `(X X^T + λI)⁻¹ X y`
2. **Ridge shrinkage factor** `λᵢ/(λᵢ + λ)` — small `λᵢ` shrinks most
3. **Naive Bayes is LINEAR**; Gaussian NB: shared variance → linear, per-class → quadratic
4. **Entropy / information gain** computation, `H(0.5) = 1` bit
5. **KNN**: `k` voting, `O(nd)` at test time, curse of dimensionality
6. **Lasso** soft-threshold `λ/2` and *why* the diamond gives sparsity
7. **`MSE(w_ML) = σ² Σ 1/λᵢ`** — the reason regularization exists

---

## ⚠️ Fastest traps to lose marks on

```text
✗ forgetting the data must be CENTERED before PCA-style computations
✗ saying lasso has a closed form                     (it does NOT)
✗ saying ridge gives sparsity                        (it does NOT — never exactly 0)
✗ saying X X^T + λI might be singular                (never, for λ > 0)
✗ mixing up d × d (ridge) and n × n (kernel) matrices
✗ claiming NB assumes features are independent       (only GIVEN y)
✗ forgetting ONE zero kills the whole NB product
✗ saying gradient descent on 0-1 loss                (non-differentiable)
✗ thinking a tree can make a diagonal cut            (axis-parallel only)
✗ picking λ or k by TRAINING error                   (use cross-validation)
✗ forgetting to normalise features for KNN
```
