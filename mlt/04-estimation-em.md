# 📕 Week 4 — Estimation: MLE, Bayesian, GMM, EM

## 1. The big picture

You assume data came from a distribution with unknown **parameters**; estimation finds the best parameter values from the data.

- **MLE (Maximum Likelihood):** parameter is a fixed unknown; pick the value that makes the data most probable.
- **Bayesian:** parameter is *random*; start with a prior belief, update with data.

Then scale up to **mixtures** (GMM) and the algorithm that fits them (**EM**).

## 2. Maximum Likelihood Estimation (MLE)

Likelihood for iid data:

```text
L(θ) = Πᵢ P(xᵢ | θ)
```

Log-likelihood (turns product into sum; same maximiser since log is increasing):

```text
ℓ(θ) = Σᵢ log P(xᵢ | θ)
```

**Recipe:** write `ℓ(θ)`, differentiate, set `= 0`, solve.

**Results to memorise:**

```text
Bernoulli / coin:  p̂ = (#successes) / (#trials)
Gaussian:          μ̂ = sample mean
                   σ̂² = (1/n) Σ (xᵢ − μ̂)²   (BIASED, uses 1/n)
```

**Worked (coin):** 7 heads in 10. `ℓ(p) = 7 log p + 3 log(1 − p)`. Set `7/p − 3/(1 − p) = 0` → `p̂ = 0.7`.

**Worked (custom density):** `f(x; θ) = θ x^(θ−1)` on `[0, 1]`, observations `xᵢ = 1/eⁱ` for `i = 1..4`.

```text
ℓ = 4 log θ + (θ − 1) · Σ log xᵢ,   Σ log xᵢ = −(1+2+3+4) = −10
dℓ/dθ = 4/θ − 10 = 0   →   θ̂ = 0.4
```

## 3. Bayesian estimation

Treat `θ` as random with a prior `P(θ)`; update via Bayes' rule:

```text
P(θ | X) = P(X | θ) P(θ) / P(X)
posterior  ∝  likelihood × prior
```

### Conjugate priors — Beta / Bernoulli

The **Beta** distribution is the **conjugate prior** for the Bernoulli parameter `p`: if the prior is Beta, the posterior is also Beta — just add the counts.

```text
prior      Beta(α, β)
observe    h ones (successes), t zeros (failures)
posterior  Beta(α + h,  β + t)
```

- Mean of `Beta(α, β) = α / (α + β)` (Bayesian point estimate of p).
- To recover counts: `h = α_post − α_prior`, `t = β_post − β_prior`.

**Worked:** prior `Beta(10, 5)`, posterior `Beta(30, 45)` → `#ones = 20`, `#zeros = 40`.

### MLE vs Bayesian

| | MLE | Bayesian |
|--|-----|----------|
| θ is | fixed unknown | random variable |
| prior | no | **yes** |
| output | single value | full distribution |
| lots of data | — | **converges to MLE** |

## 4. Gaussian Mixture Models (GMM)

Data modelled as a mixture of `K` Gaussians:

```text
P(x) = Σ_k  π_k · N(x | μ_k, Σ_k),   Σ π_k = 1,  π_k ≥ 0
```

- `π_k` = mixing coefficient (prior probability of cluster k).
- Generative story: pick cluster k with prob `π_k`, then draw from that Gaussian.

**GMM vs K-means:**

| | K-means | GMM (EM) |
|--|---------|----------|
| assignment | hard (0/1) | **soft** (probabilities) |
| cluster shape | spherical | **elliptical** (any Σ) |
| relationship | special case of GMM | general |

**Why direct MLE fails for GMM:** the log-likelihood has `log(Σ_k ...)` with a hidden variable (which Gaussian produced each point), so you can't just set the derivative to zero. Hence EM.

## 5. Convex functions & Jensen's inequality

- **Convex** `f`: chord lies above the curve; `f″ ≥ 0` (e.g. `x²`, `eˣ`). **Concave** = opposite (e.g. `log`).
- **Jensen's inequality:**

```text
convex:   f(E[X]) ≤ E[f(X)]
concave:  f(E[X]) ≥ E[f(X)]
```

- Since `log` is **concave**, Jensen gives a **lower bound** on the GMM log-likelihood; EM repeatedly maximises that bound.

## 6. The EM algorithm

**E-step — responsibilities** (soft assignment: probability cluster k generated point i):

```text
              π_k · N(xᵢ | μ_k, Σ_k)
r_ik  =  ──────────────────────────────
          Σ_j  π_j · N(xᵢ | μ_j, Σ_j)
```

Note: `Σ_k r_ik = 1` for each point (responsibilities over clusters sum to 1).

**M-step — update parameters** (let `N_k = Σᵢ r_ik`):

```text
μ_k    = (1/N_k) Σᵢ r_ik xᵢ                       (weighted mean)
Σ_k    = (1/N_k) Σᵢ r_ik (xᵢ − μ_k)(xᵢ − μ_k)^T   (weighted covariance)
π_k    = N_k / n                                  (fraction of responsibility)
```

**Loop** E → M until the log-likelihood converges.

**Convergence:** EM increases (or keeps equal) the log-likelihood every iteration → converges to a **local maximum** (depends on init, like K-means).

**Worked (E-step):** two clusters, `π₁ = π₂ = 0.5`, densities `N₁ = 0.20`, `N₂ = 0.05` at point x.

```text
num₁ = 0.5 × 0.20 = 0.10,  num₂ = 0.5 × 0.05 = 0.025,  denom = 0.125
r₁ = 0.10 / 0.125 = 0.8,   r₂ = 0.025 / 0.125 = 0.2    (sum = 1 ✓)
```

**Worked (π_k after M-step):** responsibilities for cluster k across 5 points `{0.9, 0.8, 0.7, 0.6, 0.5}`:

```text
π_k = (0.9 + 0.8 + 0.7 + 0.6 + 0.5) / 5 = 3.5 / 5 = 0.7
```

## 7. EM notation cheat (from mock Q7)

With `λ_k^i` denoting the responsibility of cluster k for point i:

```text
TRUE:   π_k = P(z_i = k)                (mixing coefficient = prior)
TRUE:   λ_k^i = P(z_i = k | xᵢ)         (responsibility = posterior)
FALSE:  Σᵢ λ_k^i = 1                    (responsibilities sum to 1 over k, not i)
FALSE:  λ_k^i = f(xᵢ | z_i = k)         (that's the likelihood, not responsibility)
```

## 8. Common exam traps

| Question | Answer |
|----------|--------|
| MLE variance of Gaussian biased? | **Yes** (1/n version). |
| MLE of a coin? | observed proportion `h/n`. |
| Beta posterior from Beta prior? | add counts: `Beta(α + ones, β + zeros)`. |
| K-means vs GMM? | hard/spherical vs **soft/elliptical**. |
| E-step computes? | **responsibilities**. |
| EM finds global max? | **No — local**. |
| log convex or concave? | **concave** (Jensen → lower bound). |
