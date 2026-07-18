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

**Q1 — Kernel → feature map.** `(x^T y)^2 = x1^2 y1^2 + 2 x1x2 y1y2 + x2^2 y2^2` ⇒ `phi = [x1^2, sqrt2 x1x2, x2^2]`. → **D**

**Q2 — Valid kernel?** `k(a,b)` has term `a^3 b`, `k(b,a)` has `a b^3` ⇒ not symmetric ⇒ **not valid**. → **B (No)**

**Q3 — Scalar proxy.** `w^T x = (1/2)(1) + (sqrt3/2)(2) = (1 + 2 sqrt3)/2`. → **B**

**Q4 — Assign x3.** Centroids: C1{x1,x6}=(0,1.5), C2{x2,x5}=(0,0), C3{x4,x7}=(0,-1.5). x3=(0,0) is closest to C2. → **B (2)**

**Q5 — Which init splits +/- marks?** Marks {6,3,-5,-4,2,-3,5,-2}.
- I1 (f8 alone): centroids -2 and 4/7 ⇒ after one step positives{6,3,2,5} vs negatives ⇒ clean → **I1: Yes**
- I2 (f1 alone): centroids 6 and -4/7 ⇒ f5=2 lands with negatives ⇒ not clean → **I2: No** → **C**

**Q6 — One K-means step.** Init (0,0),(3,0). C1={x1..x5}, C2={x6..x9}. Obj = 4 + 3 = **7**. New centroids `mu1=(0,0)`, `mu2=(13/4,0)=(3.25,0)`. → **D**

**Q7 — EM statements.** `lambda_k^i = P(z_i=k|x_i)`. A `pi_k=P(z_i=k)` ✔; C ✔; B `sum_i=1` ✘ (sums over k); D likelihood ✘. → **A and C**

**Q8 — min variance ratio.** `theta = l_1/(l_1+...+l_5)`, minimised when all equal ⇒ `1/5`. → **0.2**

**Q9 — compression ratio.** `10000/(1010 k) >= 1.4` ⇒ `k <= 7.07` ⇒ **7** (k=8 gives 1.24 < 1.4).

**Q10 — kernel PCA dim.** Parabola ⇒ degree-2 poly kernel, d=2 ⇒ `C(4,2)` = **6**.

**Q11 — Beta counts.** `Beta(10,5)→Beta(30,45)`: ones=20, zeros=**40**.

**Q12 — pi_k after M-step.** `(0.9+0.8+0.7+0.6+0.5)/5 = 3.5/5` = **0.7**.

**Q13 — centered?** Mean = (0,0). → **A (Yes)**

**Q14 — unit representatives.** Line direction `(1,3)`, `||.||=sqrt10`. Unit vectors `±(1,3)/sqrt10`. → **A and B** (C, D not unit norm)

**Q15 — variance PC1.** `C = (1/4)[[10,30],[30,90]]`, eigenvalues 25 and 0 ⇒ **25**.

**Q16 — variance PC2.** Data on a line ⇒ **0**.

**Q17 — log-likelihood.** `sum_i [log theta + (theta-1) log x_i]`. → **C**

**Q18 — MLE theta.** `4/theta + sum log x_i = 0`, `sum log x_i = -10` ⇒ `theta = 4/10` = **0.4**.

**Q19–21 — k-means++.** Given x2=(2,0) first (prob 1/5), `D^2` to x2: x1=8, x3=4, x4=8, x5=16, sum=36.
- **Q19** x2→x1: `(1/5)(8/36)` = **0.044**
- **Q20** x2→x3: `(1/5)(4/36)` = **0.022**
- **Q21** x2→x5: `(1/5)(16/36)` = **0.089**

---

## 🔥 Pattern frequency (what to prioritise)

| Topic | Questions | Weight |
|-------|-----------|--------|
| Kernels (valid? map? dim?) | Q1, Q2, Q10 | high |
| PCA (variance, projection, centering, compression) | Q3, Q8, Q9, Q13, Q15, Q16 | very high |
| K-means (assign/update, objective, Lloyd) | Q4, Q5, Q6 | high |
| k-means++ (`D^2` probability) | Q19, Q20, Q21 | high |
| EM/GMM (responsibilities, pi_k, notation) | Q7, Q12 | medium |
| MLE / Bayesian (log-lik, Beta-Bernoulli) | Q11, Q17, Q18 | medium |

**Takeaway:** PCA numerics and the k-means++ `D(x)^2` formula together account for ~40% of the paper. Nail those first.
