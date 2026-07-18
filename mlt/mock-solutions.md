# 📝 Mock Test — 21 Worked Solutions

Full solutions to the Quiz-1 mock. Each shows the method, not just the answer.

## Quick answer key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | D | 8 | 0.2 | 15 | 25 |
| 2 | B (No) | 9 | 7 | 16 | 0 |
| 3 | B | 10 | 6 | 17 | C |
| 4 | B (2) | 11 | 40 | 18 | 0.4 |
| 5 | C | 12 | 0.7 | 19 | 0.044 |
| 6 | D | 13 | A (Yes) | 20 | 0.022 |
| 7 | A and C | 14 | A and B | 21 | 0.089 |

---

## Solutions

**Q1 — Kernel → feature map.** `(x^T y)² = x₁²y₁² + 2 x₁x₂ y₁y₂ + x₂²y₂²` ⇒ `φ = [x₁², √2 x₁x₂, x₂²]`. → **D**

**Q2 — Valid kernel?** `k(a,b)` has term `a³b`, `k(b,a)` has `ab³` ⇒ not symmetric ⇒ **not valid**. → **B (No)**

**Q3 — Scalar proxy.** `w^T x = (1/2)(1) + (√3/2)(2) = (1 + 2√3)/2`. → **B**

**Q4 — Assign x₃.** Centroids: C1{x₁,x₆}=(0, 1.5), C2{x₂,x₅}=(0, 0), C3{x₄,x₇}=(0, −1.5). x₃=(0,0) is closest to C2. → **B (2)**

**Q5 — Which init splits +/− marks?** Marks {6, 3, −5, −4, 2, −3, 5, −2}.
- I₁ (f₈ alone): centroids −2 and 4/7 ⇒ after one step positives {6,3,2,5} vs negatives ⇒ clean → **I₁: Yes**
- I₂ (f₁ alone): centroids 6 and −4/7 ⇒ f₅=2 lands with negatives ⇒ not clean → **I₂: No** → **C**

**Q6 — One K-means step.** Init (0,0), (3,0). C1={x₁..x₅}, C2={x₆..x₉}. Obj = 4 + 3 = **7**. New centroids `μ₁ = (0,0)`, `μ₂ = (13/4, 0) = (3.25, 0)`. → **D**

**Q7 — EM statements.** `λ_k^i = P(z_i=k | xᵢ)`. A `π_k = P(z_i=k)` ✔; C ✔; B `Σᵢ = 1` ✘ (sums over k); D likelihood ✘. → **A and C**

**Q8 — min variance ratio.** `θ = λ₁/(λ₁+...+λ₅)`, minimised when all equal ⇒ `1/5`. → **0.2**

**Q9 — compression ratio.** `10000/(1010 k) ≥ 1.4` ⇒ `k ≤ 7.07` ⇒ **7** (k=8 gives 1.24 < 1.4).

**Q10 — kernel PCA dim.** Parabola ⇒ degree-2 poly kernel, d=2 ⇒ `C(4, 2)` = **6**.

**Q11 — Beta counts.** `Beta(10,5) → Beta(30,45)`: ones = 20, zeros = **40**.

**Q12 — π_k after M-step.** `(0.9 + 0.8 + 0.7 + 0.6 + 0.5)/5 = 3.5/5` = **0.7**.

**Q13 — centered?** Mean = (0, 0). → **A (Yes)**

**Q14 — unit representatives.** Line direction `(1, 3)`, `‖·‖ = √10`. Unit vectors `±(1, 3)/√10`. → **A and B** (C, D not unit norm)

**Q15 — variance PC1.** `C = (1/4)[[10,30],[30,90]]`, eigenvalues 25 and 0 ⇒ **25**.

**Q16 — variance PC2.** Data on a line ⇒ **0**.

**Q17 — log-likelihood.** `Σᵢ [log θ + (θ − 1) log xᵢ]`. → **C**

**Q18 — MLE θ.** `4/θ + Σ log xᵢ = 0`, `Σ log xᵢ = −10` ⇒ `θ = 4/10` = **0.4**.

**Q19–21 — k-means++.** Given x₂=(2,0) first (prob 1/5), `D²` to x₂: x₁=8, x₃=4, x₄=8, x₅=16, sum=36.
- **Q19** x₂ → x₁: `(1/5)(8/36)` = **0.044**
- **Q20** x₂ → x₃: `(1/5)(4/36)` = **0.022**
- **Q21** x₂ → x₅: `(1/5)(16/36)` = **0.089**

---

## 🔥 Pattern frequency (what to prioritise)

| Topic | Questions | Weight |
|-------|-----------|--------|
| Kernels (valid? map? dim?) | Q1, Q2, Q10 | high |
| PCA (variance, projection, centering, compression) | Q3, Q8, Q9, Q13, Q15, Q16 | very high |
| K-means (assign/update, objective, Lloyd) | Q4, Q5, Q6 | high |
| k-means++ (`D²` probability) | Q19, Q20, Q21 | high |
| EM/GMM (responsibilities, π_k, notation) | Q7, Q12 | medium |
| MLE / Bayesian (log-lik, Beta-Bernoulli) | Q11, Q17, Q18 | medium |

**Takeaway:** PCA numerics and the k-means++ `D(x)²` formula together account for ~40% of the paper. Nail those first.
