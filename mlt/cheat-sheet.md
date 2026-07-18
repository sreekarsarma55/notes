# ⚡ MLT Quiz 1 — Cheat Sheet

One-page recall for Weeks 1–4. Read this last, right before the exam.

---

## PCA (Week 1)
```
center:        x_i <- x_i - mu
covariance:    C = (1/n) X X^T            (d x d, symmetric, PSD)
components:    eigenvectors of C
variance:      = eigenvalue lambda
proj / proxy:  z = w^T x
var explained: (l_1+...+l_k)/(l_1+...+l_d)
recon error:   l_(k+1)+...+l_d            (sum of dropped eigenvalues)
compression:   ratio = n*d / [k(n+d)]
```
- data on a line → 2nd eigenvalue = 0
- PCs orthogonal ⇒ uncorrelated; unique up to sign; unsupervised

## Kernel PCA (Week 2)
```
kernel:        K(x,y) = phi(x)^T phi(y)      (never compute phi)
poly:          (x^T y + c)^p     RBF: exp(-||x-y||^2 / 2 sigma^2)
kernel matrix: n x n  (NOT d x d) ; must be centered
valid kernel:  symmetric AND positive semi-definite (Mercer)
poly dim:      inhomog C(d+p, p) ; homog C(d+p-1, p)
cost:          O(n^3), depends on n not d  (RBF = infinite dims)
```

## K-means (Week 3)
```
objective:     J = sum_k sum_{x in C_k} ||x - mu_k||^2
Lloyd:         assign to nearest centroid -> update centroid = mean -> repeat
converges:     YES, but to a LOCAL min (depends on init)
clusters:      spherical/convex; fails on rings/moons/unequal sizes
boundary:      perpendicular bisector (straight line)
k-means++:     P(pick x) = D(x)^2 / sum D(.)^2   (D = dist to nearest chosen)
choose K:      elbow method (J always drops with K; J=0 at K=n)
```

## Estimation / EM (Week 4)
```
MLE:           maximise l(theta) = sum_i log P(x_i|theta)
  coin:        p_hat = h/n
  Gaussian:    mu = mean ; sigma^2 = (1/n) sum (x-mu)^2  (biased)
Bayesian:      posterior ∝ likelihood * prior
  Beta-Bern:   Beta(a,b) prior + h ones,t zeros -> Beta(a+h, b+t)
  Beta mean:   a/(a+b)
GMM:           P(x) = sum_k pi_k N(x|mu_k,Sigma_k) ; soft, elliptical
E-step:        r_ik = pi_k N_ik / sum_j pi_j N_ij      (sum_k r_ik = 1)
M-step:        mu_k, Sigma_k weighted by r ; pi_k = N_k/n  (N_k = sum_i r_ik)
EM:            increases log-lik each step -> LOCAL max
Jensen:        convex f(E[X])<=E[f(X)] ; log is concave -> lower bound
```

---

## 🔢 Numbers worth remembering from practice
| Setup | Result |
|-------|--------|
| Compression ratio ≥ 1.4, n=1000, d=10 | k = 7 (`10000/1010k`) |
| min of var-ratio θ over 5 PCs | 1/5 = 0.2 |
| Beta(10,5)→Beta(30,45), zeros | 40 |
| MLE of `theta x^(theta-1)`, x=1/e^i (i=1..4) | 0.4 |
| poly kernel d=2, p=2 dim | 6 |

## ⏱️ 60-second priority order
1. **k-means++** `D(x)^2` probability (shows up 3×)
2. **PCA** variance = eigenvalue; line → 2nd eigenvalue 0
3. **MLE** coin `h/n`, Gaussian mean/var
4. **EM** E-step responsibilities, soft vs hard
5. **Kernels** valid? (symmetric+PSD), feature dim, n×n matrix
