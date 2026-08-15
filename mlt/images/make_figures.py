"""
Generates the diagrams used in the MLT notes.
Run:  python3 make_figures.py
Outputs PNGs into the same directory.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
OUT = __import__("os").path.dirname(__import__("os").path.abspath(__file__))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------------------
# 1. PCA: the "cigar" cloud with principal component directions
# ---------------------------------------------------------------------------
def fig_pca():
    n = 300
    # correlated gaussian -> tilted ellipse ("cigar")
    base = rng.normal(size=(n, 2)) * np.array([3.0, 0.8])
    theta = np.deg2rad(35)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    X = base @ R.T
    X = X - X.mean(axis=0)                      # center

    C = (X.T @ X) / n                           # covariance
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(X[:, 0], X[:, 1], s=12, alpha=0.45, color="#3b7dd8")
    for i, col, lbl in [(0, "#d1495b", "PC1 (max variance)"),
                         (1, "#2a9d8f", "PC2")]:
        v = vecs[:, i] * np.sqrt(vals[i]) * 2.5
        ax.annotate("", xy=v, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=3))
        ax.text(v[0]*1.08, v[1]*1.08, lbl, color=col,
                fontsize=11, fontweight="bold")
    ax.axhline(0, color="grey", lw=.6); ax.axvline(0, color="grey", lw=.6)
    ax.set_aspect("equal")
    ax.set_title(f"PCA: components = eigenvectors of covariance\n"
                 f"variance PC1={vals[0]:.1f}  PC2={vals[1]:.1f}")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    save(fig, "pca_variance.png")


# ---------------------------------------------------------------------------
# 2. Kernel PCA: non-linear (concentric circles) that plain PCA cannot separate
# ---------------------------------------------------------------------------
def fig_kernel_pca():
    n = 200
    def ring(r, spread):
        ang = rng.uniform(0, 2*np.pi, n)
        rad = r + rng.normal(0, spread, n)
        return np.c_[rad*np.cos(ang), rad*np.sin(ang)]
    inner = ring(1.0, 0.12)
    outer = ring(3.0, 0.15)

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    ax = axes[0]
    ax.scatter(inner[:, 0], inner[:, 1], s=12, color="#d1495b", label="class A")
    ax.scatter(outer[:, 0], outer[:, 1], s=12, color="#3b7dd8", label="class B")
    ax.set_aspect("equal"); ax.legend(loc="upper right")
    ax.set_title("Original 2D space\nno straight line separates the rings\n(plain PCA fails)")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")

    # feature: radius^2 = x1^2 + x2^2  (what an RBF / poly kernel captures)
    ax = axes[1]
    fi = (inner**2).sum(axis=1)
    fo = (outer**2).sum(axis=1)
    ax.scatter(np.zeros(n)+0.0, fi, s=12, color="#d1495b")
    ax.scatter(np.zeros(n)+0.0, fo, s=12, color="#3b7dd8")
    thr = (fi.max()+fo.min())/2
    ax.axhline(thr, color="black", ls="--", lw=1.5, label="linear boundary")
    ax.set_xlim(-1, 1); ax.set_xticks([])
    ax.set_ylabel(r"feature  $\phi(x)=x_1^2+x_2^2$")
    ax.legend(loc="upper right")
    ax.set_title("After feature map (kernel trick)\nnow linearly separable")
    save(fig, "kernel_pca.png")


# ---------------------------------------------------------------------------
# 3. K-means: two blobs, centroids, and the linear (perpendicular-bisector) boundary
# ---------------------------------------------------------------------------
def fig_kmeans():
    n = 120
    A = rng.normal([-2, 0], 0.7, size=(n, 2))
    B = rng.normal([2.5, 1.5], 0.7, size=(n, 2))
    cA, cB = A.mean(0), B.mean(0)

    fig, ax = plt.subplots(figsize=(6.2, 5))
    ax.scatter(A[:, 0], A[:, 1], s=14, color="#3b7dd8", alpha=.6)
    ax.scatter(B[:, 0], B[:, 1], s=14, color="#e9a13b", alpha=.6)
    ax.scatter(*cA, marker="X", s=220, color="#12457a", edgecolor="white",
               linewidth=1.5, label="centroid $\\mu_1$", zorder=5)
    ax.scatter(*cB, marker="X", s=220, color="#9c5a00", edgecolor="white",
               linewidth=1.5, label="centroid $\\mu_2$", zorder=5)

    # perpendicular bisector of the two centroids = decision boundary (a line)
    mid = (cA + cB) / 2
    d = cB - cA
    perp = np.array([-d[1], d[0]])
    t = np.linspace(-4, 4, 2)
    line = mid[None, :] + t[:, None] * perp
    ax.plot(line[:, 0], line[:, 1], "k--", lw=1.6,
            label="boundary (perp. bisector)")
    ax.set_aspect("equal"); ax.legend(loc="lower right", fontsize=9)
    ax.set_title("K-means: assign to nearest centroid\nboundary is a straight line -> spherical clusters")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    save(fig, "kmeans_clusters.png")


# ---------------------------------------------------------------------------
# 4. Elbow method for choosing K
# ---------------------------------------------------------------------------
def fig_elbow():
    K = np.arange(1, 9)
    # synthetic monotically-decreasing distortion with a clear elbow at K=3
    J = np.array([100, 42, 18, 15, 13, 11.5, 10.5, 10.0])
    fig, ax = plt.subplots(figsize=(6, 4.3))
    ax.plot(K, J, "-o", color="#3b7dd8", lw=2)
    ax.scatter([3], [J[2]], s=180, facecolor="none",
               edgecolor="#d1495b", linewidth=2.5, zorder=5)
    ax.annotate("elbow -> choose K here", xy=(3, J[2]), xytext=(4.2, 55),
                color="#d1495b", fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#d1495b"))
    ax.set_xlabel("number of clusters  K")
    ax.set_ylabel("objective  J  (within-cluster distortion)")
    ax.set_title("Elbow method: J always decreases with K\npick the 'elbow' where gains flatten")
    ax.grid(alpha=.3)
    save(fig, "elbow_method.png")


# ---------------------------------------------------------------------------
# 5. Linear regression: fitted line and the residuals being squared
# ---------------------------------------------------------------------------
def fig_linear_regression():
    x = np.array([1, 2, 3, 4, 5, 6, 7], dtype=float)
    y = np.array([1.2, 2.3, 2.1, 3.6, 4.2, 4.1, 5.4])

    # least squares with intercept
    A = np.c_[np.ones_like(x), x]
    coef = np.linalg.lstsq(A, y, rcond=None)[0]
    pred = A @ coef

    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    # residual segments first so points sit on top
    for xi, yi, pi in zip(x, y, pred):
        ax.plot([xi, xi], [yi, pi], color="#d1495b", lw=1.8, zorder=2)
    ax.plot(x, pred, color="#3b7dd8", lw=2.4,
            label=r"fit  $\hat{y} = w^T x$", zorder=3)
    ax.scatter(x, y, s=55, color="#12457a", zorder=4, label="data $(x_i, y_i)$")
    ax.plot([], [], color="#d1495b", lw=1.8,
            label=r"residual  $w^T x_i - y_i$")

    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Linear regression minimises the SUM of SQUARED residuals\n"
                 r"$f(w)=\sum_i (w^T x_i - y_i)^2 = \|X^T w - y\|^2$")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=.3)
    save(fig, "linear_regression_fit.png")


# ---------------------------------------------------------------------------
# 6. Geometric interpretation: least squares = orthogonal projection
# ---------------------------------------------------------------------------
def fig_projection():
    # subspace = span of a single feature-row, drawn as a line through origin
    u = np.array([1.0, 0.45]); u = u / np.linalg.norm(u)
    y = np.array([1.6, 2.3])
    proj = (y @ u) * u                     # orthogonal projection of y

    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    t = np.linspace(-0.4, 3.2, 2)
    line = t[:, None] * u
    ax.plot(line[:, 0], line[:, 1], color="#2a9d8f", lw=2.2,
            label=r"subspace $\{X^T w\}$ = span of feature-rows")

    ax.annotate("", xy=y, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#12457a", lw=2.6))
    ax.text(y[0]+.06, y[1]+.05, r"$y$", color="#12457a",
            fontsize=14, fontweight="bold")

    ax.annotate("", xy=proj, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#3b7dd8", lw=2.6))
    ax.text(proj[0]+.05, proj[1]-.22, r"$\hat{y}=X^T w^*$", color="#3b7dd8",
            fontsize=13, fontweight="bold")

    ax.plot([y[0], proj[0]], [y[1], proj[1]], "--", color="#d1495b", lw=2.2)
    mid = (y + proj) / 2
    ax.text(mid[0]+.09, mid[1], "residual\n(perpendicular)", color="#d1495b",
            fontsize=10, fontweight="bold", va="center")

    # right-angle marker at the projection point
    n = np.array([-u[1], u[0]])
    s = 0.17
    corner = proj + n*s + u*s
    ax.plot([proj[0]+u[0]*s, corner[0]], [proj[1]+u[1]*s, corner[1]],
            color="#d1495b", lw=1.3)
    ax.plot([proj[0]+n[0]*s, corner[0]], [proj[1]+n[1]*s, corner[1]],
            color="#d1495b", lw=1.3)

    ax.set_xlim(-0.4, 3.2); ax.set_ylim(-0.4, 2.8)
    ax.set_aspect("equal")
    ax.axhline(0, color="grey", lw=.6); ax.axvline(0, color="grey", lw=.6)
    ax.legend(loc="lower right", fontsize=9)
    ax.set_title("Least squares = orthogonal projection of $y$\n"
                 r"residual $\perp$ subspace  $\Rightarrow$  $X(X^T w - y)=0$")
    save(fig, "regression_projection.png")


# ---------------------------------------------------------------------------
# 7. Gradient descent on the (convex) squared-error surface
# ---------------------------------------------------------------------------
def fig_gradient_descent():
    # 2-parameter least squares problem -> elliptical convex contours.
    # The x-feature is centered so the problem is well conditioned and the
    # descent path visibly reaches the optimum.
    X = np.array([[1.0,  1.0, 1.0, 1.0],
                  [-1.5, -0.5, 0.5, 1.5]])        # d=2, n=4
    yv = np.array([1.0, 1.9, 3.2, 3.9])

    def loss(w):
        r = X.T @ w - yv
        return r @ r

    w_star = np.linalg.lstsq(X.T, yv, rcond=None)[0]

    g1 = np.linspace(w_star[0]-3.2, w_star[0]+3.2, 260)
    g2 = np.linspace(w_star[1]-2.0, w_star[1]+2.0, 260)
    G1, G2 = np.meshgrid(g1, g2)
    Z = np.empty_like(G1)
    for i in range(G1.shape[0]):
        for j in range(G1.shape[1]):
            Z[i, j] = loss(np.array([G1[i, j], G2[i, j]]))

    # run gradient descent
    w = np.array([w_star[0]-2.8, w_star[1]+1.7])
    eta = 0.06
    path = [w.copy()]
    for _ in range(22):
        grad = 2 * X @ (X.T @ w - yv)
        w = w - eta * grad
        path.append(w.copy())
    path = np.array(path)

    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    cs = ax.contour(G1, G2, Z, levels=np.geomspace(Z.min()+.05, Z.max(), 14),
                    cmap="Blues_r", linewidths=1.0)
    ax.plot(path[:, 0], path[:, 1], "-o", color="#d1495b", ms=4.2, lw=1.7,
            label="gradient descent path")
    ax.scatter(*w_star, marker="*", s=340, color="#f4a300",
               edgecolor="#7a5200", linewidth=1.0, zorder=6,
               label="global optimum $w^*$")
    ax.scatter(*path[0], s=70, color="#12457a", zorder=6, label="start $w^0$")
    ax.set_xlabel("$w_1$"); ax.set_ylabel("$w_2$")
    ax.set_title("Squared error is CONVEX -> single global minimum\n"
                 r"$w^{(t+1)} = w^{(t)} - \eta\,\cdot 2X(X^T w^{(t)} - y)$")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "gradient_descent.png")


# ---------------------------------------------------------------------------
# 8. Kernel regression vs linear regression on non-linear data
# ---------------------------------------------------------------------------
def fig_kernel_regression():
    n = 40
    x = np.linspace(0, 1, n)
    y_true = np.sin(2*np.pi*x)
    y = y_true + rng.normal(0, 0.18, n)

    # plain linear regression (with intercept)
    A = np.c_[np.ones_like(x), x]
    lin = A @ np.linalg.lstsq(A, y, rcond=None)[0]

    # kernel regression with an RBF kernel:  alpha = (K + lam I)^-1 y
    sigma, lam = 0.12, 1e-2
    def rbf(a, b):
        return np.exp(-(a[:, None] - b[None, :])**2 / (2*sigma**2))
    K = rbf(x, x)
    alpha = np.linalg.solve(K + lam*np.eye(n), y)

    grid = np.linspace(0, 1, 300)
    kern_pred = rbf(grid, x) @ alpha        # yhat(x) = sum_i alpha_i K(x_i, x)

    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    ax.scatter(x, y, s=34, color="#12457a", alpha=.75, label="data", zorder=3)
    ax.plot(x, lin, color="#d1495b", lw=2.2, ls="--",
            label="linear regression (underfits)")
    ax.plot(grid, kern_pred, color="#2a9d8f", lw=2.6,
            label=r"kernel regression  $\sum_i \alpha_i K(x_i, x)$")
    ax.plot(x, y_true, color="grey", lw=1.2, alpha=.7, label="true function")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Kernel regression captures non-linear structure\n"
                 r"$\alpha = K^{-1} y$   (K is $n \times n$)")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.grid(alpha=.3)
    save(fig, "kernel_regression.png")


# ---------------------------------------------------------------------------
# 9. K-fold cross-validation schematic
# ---------------------------------------------------------------------------
def fig_cross_validation():
    K = 5
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for row in range(K):
        for col in range(K):
            is_val = (col == row)
            ax.add_patch(plt.Rectangle(
                (col, K - 1 - row), 1, 0.8,
                facecolor="#e9a13b" if is_val else "#cfe0f5",
                edgecolor="white", linewidth=2))
            if is_val:
                ax.text(col + .5, K - 1 - row + .4, "val", ha="center",
                        va="center", fontsize=9, fontweight="bold",
                        color="#5c3a00")
            else:
                ax.text(col + .5, K - 1 - row + .4, "train", ha="center",
                        va="center", fontsize=8.5, color="#24486f")
        ax.text(-0.18, K - 1 - row + .4, f"split {row+1}", ha="right",
                va="center", fontsize=9.5)

    ax.set_xlim(-1.5, K + .1); ax.set_ylim(-0.35, K)
    ax.axis("off")
    ax.set_title("5-fold cross-validation: every fold is the validation set exactly once\n"
                 "CV error = average of the K validation errors  →  used to choose λ",
                 fontsize=11)
    save(fig, "cross_validation.png")


# ---------------------------------------------------------------------------
# 10. Ridge MSE vs lambda: bias-variance trade-off beating the MLE
# ---------------------------------------------------------------------------
def fig_ridge_mse():
    # eigenvalues of X X^T -- one direction is badly determined
    eig = np.array([4.0, 0.1])
    alpha = np.array([1.0, 1.0])          # true w in the eigenbasis
    sigma2 = 1.0

    lam = np.linspace(0, 6, 600)
    var = np.array([np.sum(sigma2*eig / (eig + L)**2) for L in lam])
    bias2 = np.array([np.sum(L**2 * alpha**2 / (eig + L)**2) for L in lam])
    mse = var + bias2

    mle_mse = sigma2 * np.sum(1.0/eig)
    best = int(np.argmin(mse))

    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    ax.plot(lam, var, color="#3b7dd8", lw=2, ls="--", label="variance")
    ax.plot(lam, bias2, color="#e9a13b", lw=2, ls="--", label="bias$^2$")
    ax.plot(lam, mse, color="#d1495b", lw=2.8, label="MSE = bias$^2$ + variance")
    ax.axhline(mle_mse, color="grey", lw=1.6, ls=":",
               label=f"MSE of least squares = {mle_mse:.2f}")
    ax.scatter([lam[best]], [mse[best]], marker="*", s=340, color="#f4a300",
               edgecolor="#7a5200", linewidth=1.0, zorder=6,
               label=f"best λ ≈ {lam[best]:.2f}")

    ax.set_xlabel("regularization strength  λ")
    ax.set_ylabel("error")
    ax.set_ylim(0, mle_mse*1.15)
    ax.set_title("Ridge trades a little bias for a large drop in variance\n"
                 "there is always some λ > 0 that beats least squares",
                 fontsize=11)
    ax.legend(loc="upper right", fontsize=8.5)
    ax.grid(alpha=.3)
    save(fig, "ridge_mse_lambda.png")


# ---------------------------------------------------------------------------
# 11. Why L1 gives sparsity: diamond corners vs round circle
# ---------------------------------------------------------------------------
def fig_l1_l2_geometry():
    # quadratic loss  (w - c)^T A (w - c)
    c = np.array([2.3, 0.85])
    A = np.array([[1.0, 0.28], [0.28, 0.75]])

    def loss(W1, W2):
        D1, D2 = W1 - c[0], W2 - c[1]
        return (A[0, 0]*D1**2 + 2*A[0, 1]*D1*D2 + A[1, 1]*D2**2)

    t = 1.15                                  # budget
    g = np.linspace(-1.2, 3.4, 420)
    h = np.linspace(-1.6, 2.3, 420)
    G, H = np.meshgrid(g, h)
    Z = loss(G, H)

    # numerically find the constrained optimum on each boundary
    th = np.linspace(0, 2*np.pi, 4000)
    circ = np.c_[t*np.cos(th), t*np.sin(th)]
    s = np.linspace(-1, 1, 4000)
    dia = np.concatenate([np.c_[s*t, (1-np.abs(s))*t],
                          np.c_[s*t, -(1-np.abs(s))*t]])
    best_c = circ[np.argmin(loss(circ[:, 0], circ[:, 1]))]
    best_d = dia[np.argmin(loss(dia[:, 0], dia[:, 1]))]

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.0))
    for ax, region, sol, name, extra in [
            (axes[0], dia, best_d, "Lasso  ($\\ell_1$): diamond",
             "corner on the axis  →  $w_2 = 0$  (SPARSE)"),
            (axes[1], circ, best_c, "Ridge  ($\\ell_2$): circle",
             "smooth touch point  →  both weights nonzero")]:
        ax.contour(G, H, Z, levels=np.linspace(0.06, 6.5, 11),
                   cmap="Blues_r", linewidths=.9)
        ax.contour(G, H, Z, levels=[loss(*sol)], colors="#3b7dd8",
                   linewidths=2.4)
        if name.startswith("Lasso"):
            poly = np.array([[t, 0], [0, t], [-t, 0], [0, -t]])
        else:
            poly = circ
        ax.add_patch(plt.Polygon(poly, closed=True, facecolor="#2a9d8f",
                                 alpha=.22, edgecolor="#2a9d8f", lw=2.4))
        ax.scatter(*c, marker="+", s=170, color="#12457a", linewidth=2.4,
                   zorder=6)
        ax.text(c[0]+.1, c[1]+.12, r"$w_{ML}$", color="#12457a",
                fontsize=12, fontweight="bold")
        ax.scatter(*sol, s=110, color="#d1495b", zorder=7, edgecolor="white",
                   linewidth=1.2)
        ax.text(sol[0]+.14, sol[1]-.30, "solution", color="#d1495b",
                fontsize=10.5, fontweight="bold")
        ax.axhline(0, color="grey", lw=.7); ax.axvline(0, color="grey", lw=.7)
        ax.set_aspect("equal")
        ax.set_xlim(-1.2, 3.4); ax.set_ylim(-1.6, 2.3)
        ax.set_xlabel("$w_1$"); ax.set_ylabel("$w_2$")
        ax.set_title(f"{name}\n{extra}", fontsize=10.5)
    fig.suptitle("Same loss contours, different constraint shape", fontsize=12)
    save(fig, "l1_l2_geometry.png")


# ---------------------------------------------------------------------------
# 12. Coefficient paths: ridge shrinks smoothly, lasso zeroes out
# ---------------------------------------------------------------------------
def fig_coefficient_paths():
    # design with correlated + irrelevant features
    n, d = 60, 6
    Xr = rng.normal(size=(n, d))
    Xr[:, 1] = Xr[:, 0]*0.85 + rng.normal(0, .35, n)     # correlated pair
    w_true = np.array([2.4, 0.0, -1.6, 0.0, 0.0, 0.9])
    yv = Xr @ w_true + rng.normal(0, .6, n)

    lams = np.geomspace(1e-2, 1e3, 90)

    ridge = np.array([
        np.linalg.solve(Xr.T @ Xr + L*np.eye(d), Xr.T @ yv) for L in lams])

    def lasso_cd(A, b, lam, iters=600):
        """coordinate descent for 0.5||Aw-b||^2 + lam*||w||_1"""
        w = np.zeros(A.shape[1])
        norms = (A**2).sum(axis=0)
        for _ in range(iters):
            for j in range(A.shape[1]):
                if norms[j] == 0:
                    continue
                r = b - A @ w + A[:, j]*w[j]
                z = A[:, j] @ r
                w[j] = np.sign(z)*max(abs(z) - lam, 0.0)/norms[j]
        return w

    lasso = np.array([lasso_cd(Xr, yv, L) for L in lams])

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.6), sharey=True)
    colors = plt.cm.tab10(np.arange(d))
    for ax, path, name, note in [
            (axes[0], ridge, "Ridge ($\\ell_2$)",
             "coefficients shrink smoothly, never reach 0"),
            (axes[1], lasso, "Lasso ($\\ell_1$)",
             "coefficients hit EXACTLY 0 one by one")]:
        for j in range(d):
            ax.plot(lams, path[:, j], color=colors[j], lw=2,
                    label=f"$w_{j+1}$")
        ax.set_xscale("log")
        ax.axhline(0, color="black", lw=1.1, ls=":")
        ax.set_xlabel("λ  (log scale)")
        ax.set_title(f"{name}\n{note}", fontsize=10.5)
        ax.grid(alpha=.3)
    axes[0].set_ylabel("coefficient value")
    axes[1].legend(fontsize=8, ncol=2, loc="upper right")
    fig.suptitle("Coefficient paths as regularization increases", fontsize=12)
    save(fig, "ridge_lasso_paths.png")


# ---------------------------------------------------------------------------
# 13. KNN decision boundary: small k (jagged) vs large k (smooth)
# ---------------------------------------------------------------------------
def _knn_predict(train_X, train_y, query, k):
    """Majority vote over the k nearest neighbours (ties -> class 1)."""
    d2 = ((query[:, None, :] - train_X[None, :, :])**2).sum(axis=2)
    idx = np.argsort(d2, axis=1)[:, :k]
    votes = train_y[idx].sum(axis=1)
    return (votes > k/2).astype(int)


def fig_knn_boundary():
    n = 60
    A = rng.normal([-1.1, -0.6], 0.95, size=(n, 2))
    B = rng.normal([1.3, 0.9], 0.95, size=(n, 2))
    Xd = np.vstack([A, B])
    yd = np.r_[np.zeros(n, int), np.ones(n, int)]

    # a little LABEL NOISE (realistic) -- this is what k=1 overfits to,
    # producing isolated islands, while a larger k averages it away.
    flip = rng.choice(len(yd), size=9, replace=False)
    yd = yd.copy()
    yd[flip] = 1 - yd[flip]
    A, B = Xd[yd == 0], Xd[yd == 1]

    g = np.linspace(-4.2, 4.6, 240)
    h = np.linspace(-3.8, 4.4, 240)
    G, H = np.meshgrid(g, h)
    grid = np.c_[G.ravel(), H.ravel()]

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.9))
    for ax, k, note in [
            (axes[0], 1, "islands around every noisy point\ntraining error = 0, HIGH variance -> OVERFITS"),
            (axes[1], 25, "noise averaged away, smooth boundary\nhigher bias, LOW variance")]:
        Z = _knn_predict(Xd, yd, grid, k).reshape(G.shape)
        ax.contourf(G, H, Z, levels=[-.5, .5, 1.5],
                    colors=["#cfe0f5", "#f8ddb0"], alpha=.85)
        ax.contour(G, H, Z, levels=[.5], colors="#d1495b", linewidths=2.0)
        ax.scatter(A[:, 0], A[:, 1], s=26, color="#12457a",
                   edgecolor="white", linewidth=.6, label="class 0")
        ax.scatter(B[:, 0], B[:, 1], s=26, color="#c07800", marker="s",
                   edgecolor="white", linewidth=.6, label="class 1")
        ax.set_title(f"k = {k}\n{note}", fontsize=10.5)
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
        ax.set_xlim(g[0], g[-1]); ax.set_ylim(h[0], h[-1])
    axes[0].legend(loc="lower right", fontsize=8.5, framealpha=.95)
    fig.suptitle("k controls the bias-variance trade-off in KNN", fontsize=12)
    save(fig, "knn_decision_boundary.png")


# ---------------------------------------------------------------------------
# 14. Curse of dimensionality: distances concentrate as d grows
# ---------------------------------------------------------------------------
def fig_curse_of_dimensionality():
    n = 500

    def dists(d, seed):
        r = np.random.default_rng(seed)
        P = r.random((n, d))
        q = r.random(d)
        return np.sqrt(((P - q)**2).sum(axis=1))

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.5))

    # ---- left: the distance DISTRIBUTION collapses to a spike ----
    ax = axes[0]
    for d, c, lbl in [(2, "#3b7dd8", "d = 2"), (10, "#2a9d8f", "d = 10"),
                      (500, "#d1495b", "d = 500")]:
        dd = dists(d, 11)
        dd = dd / dd.mean()                    # normalise so scales compare
        ax.hist(dd, bins=45, density=True, alpha=.55, color=c, label=lbl)
    ax.axvline(1.0, color="grey", lw=.9, ls=":")
    ax.set_xlabel("distance to the query  (divided by the mean distance)")
    ax.set_ylabel("density")
    ax.set_xlim(0, 2.1)
    ax.set_title("Distances CONCENTRATE around their mean\n"
                 "in high d every point is about equally far away",
                 fontsize=10.5)
    ax.legend(fontsize=9)

    # ---- right: the relative gap decays to 0 ----
    ax = axes[1]
    dims = np.unique(np.geomspace(2, 2000, 30).astype(int))
    trials = 40
    gap = []
    for d in dims:
        v = [(lambda x: (x.max() - x.min())/x.min())(dists(d, 1000 + d*97 + t))
             for t in range(trials)]
        gap.append(np.median(v))               # median: robust to outliers

    ax.plot(dims, gap, "-o", color="#3b7dd8", lw=2, ms=4.5)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("number of dimensions  d  (log scale)")
    ax.set_ylabel(r"$(d_{max} - d_{min})\,/\,d_{min}$")
    ax.set_title("The relative gap between nearest and farthest\n"
                 r"shrinks toward 0  $\Rightarrow$  'nearest' loses meaning",
                 fontsize=10.5)
    ax.grid(alpha=.3, which="both")
    save(fig, "curse_of_dimensionality.png")


# ---------------------------------------------------------------------------
# 15. Impurity measures: entropy and Gini vs class proportion
# ---------------------------------------------------------------------------
def fig_entropy_curve():
    p = np.linspace(1e-9, 1 - 1e-9, 600)
    H = -p*np.log2(p) - (1-p)*np.log2(1-p)
    gini = 2*p*(1-p)

    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ax.plot(p, H, color="#3b7dd8", lw=2.6, label=r"entropy  $H(p)$  (bits)")
    ax.plot(p, gini, color="#2a9d8f", lw=2.4, ls="--",
            label=r"Gini  $2p(1-p)$")
    ax.axvline(.5, color="grey", lw=.9, ls=":")
    ax.scatter([.5], [1.0], s=110, color="#d1495b", zorder=6)
    ax.annotate("maximally mixed\n$p=0.5$, $H=1$ bit", xy=(.5, 1.0),
                xytext=(.60, .72), color="#d1495b", fontsize=9.5,
                fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#d1495b"))
    for x0, lbl in [(0.0, "pure\n$H=0$"), (1.0, "pure\n$H=0$")]:
        ax.annotate(lbl, xy=(x0, 0), xytext=(x0 + (.06 if x0 == 0 else -.14), .18),
                    color="#12457a", fontsize=9.5, fontweight="bold",
                    arrowprops=dict(arrowstyle="-|>", color="#12457a"))
    ax.set_xlabel("fraction of positives in the node,  $p$")
    ax.set_ylabel("impurity")
    ax.set_ylim(0, 1.12)
    ax.set_title("Impurity is highest for a 50/50 node, zero for a pure node\n"
                 "splits are chosen to reduce it the most (information gain)",
                 fontsize=11)
    ax.legend(loc="lower center", fontsize=9)
    ax.grid(alpha=.3)
    save(fig, "entropy_curve.png")


# ---------------------------------------------------------------------------
# 16. Decision tree: axis-parallel partition and the matching tree
# ---------------------------------------------------------------------------
def fig_decision_tree_partition():
    # explicit tree so the partition and the diagram agree exactly:
    #   root:  x1 <= 5
    #     yes:  x2 <= 3  ->  +   else  -
    #     no :  x2 <= 6  ->  -   else  +
    regions = [((0, 5), (0, 3), "+"), ((0, 5), (3, 10), "\u2212"),
               ((5, 10), (0, 6), "\u2212"), ((5, 10), (6, 10), "+")]
    col = {"+": "#cfe0f5", "\u2212": "#f8ddb0"}

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.0),
                             gridspec_kw={"width_ratios": [1, 1.12]})

    # ---- left: feature space ----
    ax = axes[0]
    for (x0, x1), (y0, y1), lab in regions:
        ax.add_patch(plt.Rectangle((x0, y0), x1-x0, y1-y0,
                                   facecolor=col[lab], edgecolor="none"))
        ax.text((x0+x1)/2, (y0+y1)/2, lab, ha="center", va="center",
                fontsize=22, fontweight="bold",
                color="#12457a" if lab == "+" else "#8a5300")
    # sample points consistent with the regions
    for (x0, x1), (y0, y1), lab in regions:
        pts = np.c_[rng.uniform(x0+.4, x1-.4, 9), rng.uniform(y0+.4, y1-.4, 9)]
        ax.scatter(pts[:, 0], pts[:, 1], s=22,
                   color="#12457a" if lab == "+" else "#c07800",
                   marker="o" if lab == "+" else "s",
                   edgecolor="white", linewidth=.6, zorder=4)
    ax.plot([5, 5], [0, 10], color="#d1495b", lw=2.6)
    ax.plot([0, 5], [3, 3], color="#d1495b", lw=2.6)
    ax.plot([5, 10], [6, 6], color="#d1495b", lw=2.6)
    ax.text(5.15, 9.5, "$x_1=5$", color="#d1495b", fontsize=11, fontweight="bold")
    ax.text(.2, 3.2, "$x_2=3$", color="#d1495b", fontsize=11, fontweight="bold")
    ax.text(9.8, 6.2, "$x_2=6$", color="#d1495b", fontsize=11,
            fontweight="bold", ha="right")
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_title("Every split is AXIS-PARALLEL\n-> the space becomes rectangles",
                 fontsize=10.5)

    # ---- right: the tree ----
    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(-0.2, 10.2); ax.set_ylim(0.8, 10)

    def node(x, y, txt, kind, fs=11):
        face = {"test": "#e8eef7", "+": "#cfe0f5", "\u2212": "#f8ddb0"}[kind]
        edge = {"test": "#3b7dd8", "+": "#12457a", "\u2212": "#c07800"}[kind]
        ax.add_patch(plt.Rectangle((x-1.15, y-.52), 2.3, 1.04,
                                   facecolor=face, edgecolor=edge,
                                   linewidth=1.8, zorder=3,
                                   joinstyle="round"))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs,
                fontweight="bold", zorder=4,
                color=edge if kind != "test" else "#12457a")

    def edge(x0, y0, x1, y1, lab, dx):
        ax.plot([x0, x1], [y0-.52, y1+.52], color="#7f8fa6", lw=1.6, zorder=2)
        ax.text((x0+x1)/2 + dx, (y0+y1)/2, lab, fontsize=9.5,
                color="#4a5a6a", fontweight="bold", ha="center")

    M = "\u2212"
    node(5, 8.8, "$x_1 \\leq 5$ ?", "test")
    node(2.4, 5.6, "$x_2 \\leq 3$ ?", "test")
    node(7.6, 5.6, "$x_2 \\leq 6$ ?", "test")
    node(1.3, 2.2, "+", "+", 17); node(3.9, 2.2, M, M, 17)
    node(6.1, 2.2, M, M, 17); node(8.7, 2.2, "+", "+", 17)
    edge(5, 8.8, 2.4, 5.6, "yes", -.45); edge(5, 8.8, 7.6, 5.6, "no", .45)
    edge(2.4, 5.6, 1.3, 2.2, "yes", -.42); edge(2.4, 5.6, 3.9, 2.2, "no", .42)
    edge(7.6, 5.6, 6.1, 2.2, "yes", -.42); edge(7.6, 5.6, 8.7, 2.2, "no", .42)
    ax.set_title("The same model as a tree\nprediction = walk root -> leaf,  $O(depth)$",
                 fontsize=10.5)
    save(fig, "decision_tree_partition.png")


# ---------------------------------------------------------------------------
# 17. Generative vs discriminative
# ---------------------------------------------------------------------------
def fig_generative_vs_discriminative():
    n = 90
    m0, m1 = np.array([-1.25, -0.5]), np.array([1.3, 1.0])
    C = np.array([[1.05, 0.35], [0.35, 0.75]])
    L = np.linalg.cholesky(C)
    A = m0 + rng.normal(size=(n, 2)) @ L.T
    B = m1 + rng.normal(size=(n, 2)) @ L.T

    g = np.linspace(-4.4, 4.6, 300)
    h = np.linspace(-3.6, 4.2, 300)
    G, H = np.meshgrid(g, h)
    grid = np.c_[G.ravel(), H.ravel()]

    Cinv = np.linalg.inv(C)

    def dens(mu):
        D = grid - mu
        return np.exp(-.5*np.einsum('ij,jk,ik->i', D, Cinv, D)).reshape(G.shape)

    d0, d1 = dens(m0), dens(m1)

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.0))

    ax = axes[0]
    ax.contour(G, H, d0, levels=[.12, .35, .7], colors="#12457a", linewidths=1.7)
    ax.contour(G, H, d1, levels=[.12, .35, .7], colors="#c07800", linewidths=1.7)
    ax.scatter(A[:, 0], A[:, 1], s=20, color="#12457a", alpha=.65)
    ax.scatter(B[:, 0], B[:, 1], s=20, color="#c07800", marker="s", alpha=.65)
    ax.text(m0[0], m0[1]-2.35, r"$P(x \mid y=0)$", color="#12457a",
            fontsize=11.5, fontweight="bold", ha="center")
    ax.text(m1[0]+.5, m1[1]+2.05, r"$P(x \mid y=1)$", color="#c07800",
            fontsize=11.5, fontweight="bold", ha="center")
    ax.set_title("GENERATIVE\nmodels each class density $P(x\\mid y)$ and $P(y)$\n"
                 "-> can SAMPLE new data", fontsize=10.5)

    ax = axes[1]
    Z = (d1*0.5 > d0*0.5).astype(float)
    ax.contourf(G, H, Z, levels=[-.5, .5, 1.5],
                colors=["#cfe0f5", "#f8ddb0"], alpha=.75)
    ax.contour(G, H, Z, levels=[.5], colors="#d1495b", linewidths=2.6)
    ax.scatter(A[:, 0], A[:, 1], s=20, color="#12457a", alpha=.65)
    ax.scatter(B[:, 0], B[:, 1], s=20, color="#c07800", marker="s", alpha=.65)
    ax.text(-3.9, 3.5, "decision boundary\nonly", color="#d1495b",
            fontsize=11, fontweight="bold")
    ax.set_title("DISCRIMINATIVE\nmodels $P(y \\mid x)$ / the boundary directly\n"
                 "-> cannot generate data", fontsize=10.5)

    for ax in axes:
        ax.set_xlim(g[0], g[-1]); ax.set_ylim(h[0], h[-1])
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    save(fig, "generative_vs_discriminative.png")


if __name__ == "__main__":
    # Weeks 1-3
    fig_pca()
    fig_kernel_pca()
    fig_kmeans()
    fig_elbow()
    # Week 5
    fig_linear_regression()
    fig_projection()
    fig_gradient_descent()
    fig_kernel_regression()
    # Week 6
    fig_cross_validation()
    fig_ridge_mse()
    fig_l1_l2_geometry()
    fig_coefficient_paths()
    # Week 7
    fig_knn_boundary()
    fig_curse_of_dimensionality()
    fig_entropy_curve()
    fig_decision_tree_partition()
    fig_generative_vs_discriminative()
    print("done")
