# 📕 Week 4 — Estimation: MLE, Bayesian, GMM, EM

## 1. The big picture

You assume data came from a distribution with unknown **parameters**; estimation finds the best parameter values from the data.

- **MLE (Maximum Likelihood):** parameter is a fixed unknown; pick the value that makes the data most probable.
- **Bayesian:** parameter is *random*; start with a prior belief, update with data.

Then scale up to **mixtures** (GMM) and the algorithm that fits them (**EM**).

## 2. Maximum Likelihood Estimation (MLE)

Likelihood for iid data:
```
L(theta) = prod_i  P(x_i | theta)
```
Log-likelihood (turns product into sum; same maximiser since log is increasing):
```
l(theta) = sum_i  log P(x_i | theta)
```
**Recipe:** write `l(theta)`, differentiate, set `= 0`, solve.

**Results to memorise:**
```
Bernoulli / coin:  p_hat = (#successes) / (#trials)
Gaussian:          mu_hat = sample mean
                   sigma^2_hat = (1/n) sum (x_i - mu_hat)^2   (BIASED, uses 1/n)
```

**Worked (coin):** 7 heads in 10. `l(p) = 7 log p + 3 log(1-p)`. Set `7/p - 3/(1-p) = 0` → `p_hat = 0.7`.

**Worked (custom density):** `f(x;theta) = theta x^(theta-1)` on `[0,1]`, observations `x_i = 1/e^i` for `i=1..4`.
```
l = 4 log theta + (theta - 1) * sum log x_i,   sum log x_i = -(1+2+3+4) = -10
dl/dtheta = 4/theta - 10 = 0  ->  theta_hat = 0.4
```

## 3. Bayesian estimation

Treat `theta` as random with a prior `P(theta)`; update via Bayes' rule:
```
P(theta | X) = P(X | theta) P(theta) / P(X)
posterior  proportional_to  likelihood * prior
```

### Conjugate priors — Beta / Bernoulli

The **Beta** distribution is the **conjugate prior** for the Bernoulli parameter `p`: if the prior is Beta, the posterior is also Beta — just add the counts.
```
prior      Beta(alpha, beta)
observe    h ones (successes), t zeros (failures)
posterior  Beta(alpha + h,  beta + t)
```
- Mean of `Beta(alpha, beta) = alpha / (alpha + beta)` (Bayesian point estimate of p).
- To recover counts: `h = alpha_post - alpha_prior`, `t = beta_post - beta_prior`.

**Worked:** prior `Beta(10,5)`, posterior `Beta(30,45)` → `#ones = 20`, `#zeros = 40`.

### MLE vs Bayesian

| | MLE | Bayesian |
|--|-----|----------|
| theta is | fixed unknown | random variable |
| prior | no | **yes** |
| output | single value | full distribution |
| lots of data | — | **converges to MLE** |

## 4. Gaussian Mixture Models (GMM)

Data modelled as a mixture of `K` Gaussians:
```
P(x) = sum_{k=1..K}  pi_k * N(x | mu_k, Sigma_k),   sum pi_k = 1,  pi_k >= 0
```
- `pi_k` = mixing coefficient (prior probability of cluster k).
- Generative story: pick cluster k with prob `pi_k`, then draw from that Gaussian.

**GMM vs K-means:**

| | K-means | GMM (EM) |
|--|---------|----------|
| assignment | hard (0/1) | **soft** (probabilities) |
| cluster shape | spherical | **elliptical** (any Sigma) |
| relationship | special case of GMM | general |

**Why direct MLE fails for GMM:** the log-likelihood has `log(sum_k ...)` with a hidden variable (which Gaussian produced each point), so you can't just set the derivative to zero. Hence EM.

## 5. Convex functions & Jensen's inequality

- **Convex** `f`: chord lies above the curve; `f'' >= 0` (e.g. `x^2`, `e^x`). **Concave** = opposite (e.g. `log`).
- **Jensen's inequality:**
  ```
  convex:   f(E[X]) <= E[f(X)]
  concave:  f(E[X]) >= E[f(X)]
  ```
- Since `log` is **concave**, Jensen gives a **lower bound** on the GMM log-likelihood; EM repeatedly maximises that bound.

## 6. The EM algorithm

**E-step — responsibilities** (soft assignment: probability cluster k generated point i):
```
              pi_k * N(x_i | mu_k, Sigma_k)
r_ik  =  --------------------------------------
          sum_j  pi_j * N(x_i | mu_j, Sigma_j)
```
Note: `sum_k r_ik = 1` for each point (responsibilities over clusters sum to 1).

**M-step — update parameters** (let `N_k = sum_i r_ik`):
```
mu_k    = (1/N_k) sum_i r_ik x_i                          (weighted mean)
Sigma_k = (1/N_k) sum_i r_ik (x_i - mu_k)(x_i - mu_k)^T   (weighted covariance)
pi_k    = N_k / n                                         (fraction of responsibility)
```

**Loop** E → M until the log-likelihood converges.

**Convergence:** EM increases (or keeps equal) the log-likelihood every iteration → converges to a **local maximum** (depends on init, like K-means).

**Worked (E-step):** two clusters, `pi_1 = pi_2 = 0.5`, densities `N_1 = 0.20`, `N_2 = 0.05` at point x.
```
num1 = 0.5 * 0.20 = 0.10,  num2 = 0.5 * 0.05 = 0.025,  denom = 0.125
r_1 = 0.10 / 0.125 = 0.8,   r_2 = 0.025 / 0.125 = 0.2   (sum = 1 check)
```

**Worked (pi_k after M-step):** responsibilities for cluster k across 5 points `{0.9,0.8,0.7,0.6,0.5}`:
```
pi_k = (0.9+0.8+0.7+0.6+0.5) / 5 = 3.5 / 5 = 0.7
```

## 7. EM notation cheat (from mock Q7)

With `lambda_k^i` denoting the responsibility of cluster k for point i:
```
TRUE:   pi_k = P(z_i = k)                 (mixing coefficient = prior)
TRUE:   lambda_k^i = P(z_i = k | x_i)     (responsibility = posterior)
FALSE:  sum_i lambda_k^i = 1              (responsibilities sum to 1 over k, not i)
FALSE:  lambda_k^i = f(x_i | z_i = k)     (that's the likelihood, not responsibility)
```

## 8. Common exam traps

| Question | Answer |
|----------|--------|
| MLE variance of Gaussian biased? | **Yes** (1/n version). |
| MLE of a coin? | observed proportion `h/n`. |
| Beta posterior from Beta prior? | add counts: `Beta(a+ones, b+zeros)`. |
| K-means vs GMM? | hard/spherical vs **soft/elliptical**. |
| E-step computes? | **responsibilities**. |
| EM finds global max? | **No — local**. |
| log convex or concave? | **concave** (Jensen → lower bound). |
