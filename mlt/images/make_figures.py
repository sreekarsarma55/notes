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


# ---------------------------------------------------------------------------
# 18. Parameter explosion: full generative model vs Naive Bayes
# ---------------------------------------------------------------------------
def fig_nb_parameter_explosion():
    d = np.arange(1, 31)
    full = 2*(2.0**d - 1) + 1
    nb = 2*d + 1

    fig, ax = plt.subplots(figsize=(6.8, 4.7))
    ax.plot(d, full, "-o", color="#d1495b", lw=2.2, ms=4,
            label=r"full model:  $2(2^d - 1) + 1$")
    ax.plot(d, nb, "-o", color="#2a9d8f", lw=2.2, ms=4,
            label=r"Naive Bayes:  $2d + 1$")
    ax.set_yscale("log")
    ax.set_xlabel("number of binary features  d")
    ax.set_ylabel("number of parameters  (log scale)")
    ax.set_title("The naive assumption turns EXPONENTIAL into LINEAR\n"
                 "this is the whole reason Naive Bayes exists", fontsize=11)
    ax.grid(alpha=.3, which="both")
    ax.legend(loc="upper left", fontsize=9.5)
    for dd in (10, 20, 30):
        i = dd - 1
        ax.annotate(f"d={dd}:  {int(full[i]):,}  vs  {int(nb[i])}",
                    xy=(dd, full[i]), xytext=(dd-8.5, full[i]*3.2),
                    fontsize=8.6, color="#8a2436", fontweight="bold",
                    arrowprops=dict(arrowstyle="-|>", color="#8a2436", lw=1.1))
    ax.set_ylim(1, full[-1]*400)
    save(fig, "nb_parameter_explosion.png")


# ---------------------------------------------------------------------------
# 19. Laplace smoothing removes the annihilating zero
# ---------------------------------------------------------------------------
def fig_nb_laplace_smoothing():
    # counts from the worked example:  y=1 -> (1,1),(1,1),(1,0) ; y=0 -> (0,0),(0,1)
    labels = [r"$p_1^1$", r"$p_2^1$", r"$p_1^0$", r"$p_2^0$"]
    raw = [3/3, 2/3, 0/2, 1/2]
    sm = [(3+1)/(3+2), (2+1)/(3+2), (0+1)/(2+2), (1+1)/(2+2)]

    x = np.arange(4)
    w = 0.36
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    b1 = ax.bar(x - w/2, raw, w, label="MLE (unsmoothed)", color="#d1495b")
    b2 = ax.bar(x + w/2, sm, w, label="Laplace smoothed", color="#2a9d8f")

    for b, v in zip(b1, raw):
        ax.text(b.get_x()+b.get_width()/2, v + .03, f"{v:.2f}", ha="center",
                fontsize=9, fontweight="bold", color="#8a2436")
    for b, v in zip(b2, sm):
        ax.text(b.get_x()+b.get_width()/2, v + .03, f"{v:.2f}", ha="center",
                fontsize=9, fontweight="bold", color="#1d6b60")

    ax.annotate("ZERO -> annihilates\nthe whole product",
                xy=(2 - w/2, 0.035), xytext=(2 - w/2, 0.86),
                color="#8a2436", fontsize=9.6, fontweight="bold",
                ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#8a2436", lw=1.6))
    ax.annotate("lifted off 0", xy=(2 + w/2, 0.28),
                xytext=(2 + w/2 + 0.02, 0.56),
                color="#1d6b60", fontsize=9.6, fontweight="bold",
                ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#1d6b60", lw=1.6))

    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=13)
    ax.set_ylabel(r"estimate of  $P(x_j = 1 \mid y)$")
    ax.set_ylim(0, 1.18)
    ax.set_title("Laplace smoothing:  (count + 1) / (n$_y$ + 2)\n"
                 "removes zeros AND pulls estimates off the extremes",
                 fontsize=11)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=.3, axis="y")
    save(fig, "nb_laplace_smoothing.png")


def _gauss_contours(ax, mu, cov, color, levels=(.12, .4, .78)):
    g = np.linspace(-5.2, 5.4, 260)
    h = np.linspace(-4.4, 4.6, 260)
    G, H = np.meshgrid(g, h)
    P = np.c_[G.ravel(), H.ravel()] - mu
    Ci = np.linalg.inv(cov)
    Z = np.exp(-.5*np.einsum('ij,jk,ik->i', P, Ci, P)).reshape(G.shape)
    ax.contour(G, H, Z, levels=list(levels), colors=color, linewidths=1.8)


# ---------------------------------------------------------------------------
# 20. The conditional-independence assumption forces axis-aligned densities
# ---------------------------------------------------------------------------
def fig_nb_independence_assumption():
    n = 160
    C = np.array([[1.25, 0.95], [0.95, 1.05]])       # strongly correlated
    L = np.linalg.cholesky(C)
    m0, m1 = np.array([-1.35, -0.9]), np.array([1.45, 1.0])
    A = m0 + rng.normal(size=(n, 2)) @ L.T
    B = m1 + rng.normal(size=(n, 2)) @ L.T

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.0))
    for ax, use_diag, title, note in [
            (axes[0], False, "TRUE class densities",
             "features are correlated within each class\n(tilted ellipses)"),
            (axes[1], True, "What NAIVE BAYES can represent",
             "conditional independence ⇒ DIAGONAL covariance\n(axis-aligned ellipses only)")]:
        for data, mu, c in [(A, m0, "#12457a"), (B, m1, "#c07800")]:
            cov = np.cov(data.T)
            if use_diag:
                cov = np.diag(np.diag(cov))          # what NB assumes
            _gauss_contours(ax, data.mean(axis=0), cov, c)
        ax.scatter(A[:, 0], A[:, 1], s=17, color="#12457a", alpha=.55)
        ax.scatter(B[:, 0], B[:, 1], s=17, color="#c07800", marker="s", alpha=.55)
        ax.set_title(f"{title}\n{note}", fontsize=10.5)
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
        ax.set_xlim(-5.2, 5.4); ax.set_ylim(-4.4, 4.6)
        ax.set_aspect("equal")
    fig.suptitle("Pitfall: Naive Bayes cannot model correlation between features",
                 fontsize=12)
    save(fig, "nb_independence_assumption.png")


# ---------------------------------------------------------------------------
# 21. Gaussian NB: shared variances -> linear ; per-class -> quadratic
# ---------------------------------------------------------------------------
def fig_gaussian_nb_boundaries():
    g = np.linspace(-5.0, 5.0, 420)
    h = np.linspace(-4.2, 4.2, 420)
    G, H = np.meshgrid(g, h)

    def log_score(mu, sd, prior):
        """log P(y) + sum_j log N(x_j; mu_j, sd_j^2)   (diagonal = Naive Bayes)"""
        out = np.log(prior)
        for j, (m, s) in enumerate(zip(mu, sd)):
            V = (G if j == 0 else H)
            out = out - 0.5*np.log(2*np.pi*s**2) - (V - m)**2/(2*s**2)
        return out

    cases = [
        # shared variances across the two classes -> x^2 terms cancel
        dict(ax=0, m0=(-1.3, -0.6), s0=(1.0, 0.8),
             m1=(1.5, 0.9), s1=(1.0, 0.8),
             title="Shared variances  ($\\sigma_j^1 = \\sigma_j^0$)",
             note="the $x_j^2$ terms CANCEL  ⇒  LINEAR boundary"),
        # per-class variances -> x^2 terms survive
        dict(ax=1, m0=(0.0, 0.0), s0=(0.62, 0.62),
             m1=(0.35, 0.2), s1=(2.1, 2.1),
             title="Per-class variances  ($\\sigma_j^1 \\neq \\sigma_j^0$)",
             note="the $x_j^2$ terms SURVIVE  ⇒  QUADRATIC boundary"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.0))
    for c in cases:
        ax = axes[c["ax"]]
        m0, s0, m1, s1 = c["m0"], c["s0"], c["m1"], c["s1"]
        Z = log_score(m1, s1, .5) - log_score(m0, s0, .5)
        ax.contourf(G, H, (Z > 0).astype(float), levels=[-.5, .5, 1.5],
                    colors=["#cfe0f5", "#f8ddb0"], alpha=.8)
        ax.contour(G, H, Z, levels=[0], colors="#d1495b", linewidths=2.8)

        for mu, sd, col, mk in [(m0, s0, "#12457a", "o"), (m1, s1, "#c07800", "s")]:
            pts = np.c_[rng.normal(mu[0], sd[0], 90), rng.normal(mu[1], sd[1], 90)]
            ax.scatter(pts[:, 0], pts[:, 1], s=16, color=col, marker=mk, alpha=.6)
            ax.scatter(*mu, marker="X", s=170, color=col, edgecolor="white",
                       linewidth=1.4, zorder=6)
        ax.set_xlim(g[0], g[-1]); ax.set_ylim(h[0], h[-1])
        ax.set_aspect("equal")
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
        ax.set_title(f"{c['title']}\n{c['note']}", fontsize=10.5)
    fig.suptitle("Gaussian Naive Bayes: the variance structure decides the boundary shape",
                 fontsize=12)
    save(fig, "gaussian_nb_boundaries.png")


# ---------------------------------------------------------------------------
# 22. Sigmoid: turning a score into a probability
# ---------------------------------------------------------------------------
def fig_sigmoid_logistic():
    z = np.linspace(-8, 8, 600)
    s = 1/(1 + np.exp(-z))

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.4))

    ax = axes[0]
    ax.plot(z, s, color="#3b7dd8", lw=2.8, label=r"$\sigma(z)=1/(1+e^{-z})$")
    ax.plot(z, s*(1-s), color="#2a9d8f", lw=2.0, ls="--",
            label=r"$\sigma'(z)=\sigma(1-\sigma)$")
    ax.axhline(.5, color="grey", lw=.8, ls=":")
    ax.axvline(0, color="grey", lw=.8, ls=":")
    ax.scatter([0], [.5], s=110, color="#d1495b", zorder=6)
    ax.annotate(r"$\sigma(0)=0.5$" + "\n(decision threshold)", xy=(0, .5),
                xytext=(1.4, .24), color="#d1495b", fontsize=9.5,
                fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#d1495b"))
    ax.set_xlabel(r"score  $z = w^T x$"); ax.set_ylabel("value")
    ax.set_title("Sigmoid squashes any score into (0,1)\n"
                 r"$P(y=1\mid x)=\sigma(w^T x)$", fontsize=10.5)
    ax.legend(loc="upper left", fontsize=9); ax.grid(alpha=.3)

    # right: the boundary is linear because sigma(z)=0.5  <=>  z=0
    ax = axes[1]
    n = 70
    A = rng.normal([-1.2, -0.7], .85, size=(n, 2))
    B = rng.normal([1.3, 0.9], .85, size=(n, 2))
    g = np.linspace(-4.2, 4.4, 260); h = np.linspace(-3.8, 4.0, 260)
    G, H = np.meshgrid(g, h)
    w, b = np.array([1.0, 0.9]), -0.15            # illustrative fitted model
    P = 1/(1 + np.exp(-(w[0]*G + w[1]*H + b)))
    cf = ax.contourf(G, H, P, levels=np.linspace(0, 1, 21), cmap="RdYlBu_r",
                     alpha=.75)
    ax.contour(G, H, P, levels=[.5], colors="black", linewidths=2.6)
    ax.scatter(A[:, 0], A[:, 1], s=20, color="#12457a", alpha=.8)
    ax.scatter(B[:, 0], B[:, 1], s=20, color="#7a1220", marker="s", alpha=.8)
    fig.colorbar(cf, ax=ax, label=r"$P(y=1\mid x)$")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_title("Logistic regression: smooth probabilities,\n"
                 r"but the boundary $\sigma=0.5$ is a straight LINE", fontsize=10.5)
    save(fig, "sigmoid_logistic.png")


# ---------------------------------------------------------------------------
# 23. Perceptron finds SOME separator; SVM finds the MAXIMUM MARGIN one
# ---------------------------------------------------------------------------
def fig_perceptron_vs_svm():
    # symmetric data, so the max-margin boundary is known analytically to be
    # x1 + x2 = 0 (direction w ∝ (1,1), b = 0)
    pos = np.array([[2.2, 1.0], [1.0, 2.2], [3.0, 2.4], [2.0, 3.2], [3.4, 1.6]])
    neg = np.array([[-1.0, -2.2], [-2.2, -1.0], [-2.4, -3.0], [-3.2, -2.0],
                    [-1.6, -3.4]])

    t = np.linspace(-4.6, 4.6, 2)
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.0))

    for ax, kind in [(axes[0], "perceptron"), (axes[1], "svm")]:
        ax.scatter(pos[:, 0], pos[:, 1], s=52, color="#12457a", label="$y=+1$",
                   zorder=4)
        ax.scatter(neg[:, 0], neg[:, 1], s=52, color="#c07800", marker="s",
                   label="$y=-1$", zorder=4)

        if kind == "perceptron":
            # a valid but arbitrary separator (small margin)
            wv, bv = np.array([1.0, 0.30]), 0.55
            ax.plot(t, -(wv[0]*t + bv)/wv[1], color="#d1495b", lw=2.6)
            ax.set_title("PERCEPTRON\nany separator will do — margin is tiny\n"
                         "(depends on init / point order)", fontsize=10.5)
        else:
            # Rescale the known direction so that min_i y_i(w^T x_i + b) = 1,
            # which is the SVM normalisation. Only then do the lines
            # w^T x + b = ±1 actually pass through the support vectors.
            w0, b0 = np.array([1.0, 1.0]), 0.0
            m = np.r_[pos @ w0 + b0, -(neg @ w0 + b0)].min()
            wv, bv = w0/m, b0/m
            ax.plot(t, -(wv[0]*t + bv)/wv[1], color="#d1495b", lw=2.8)
            for c in (1, -1):
                ax.plot(t, -(wv[0]*t + bv - c)/wv[1], color="#2a9d8f",
                        lw=2.0, ls="--")
            # A diagonal band would be clipped by the axes and make the
            # boundary look off-centre, so annotate the width along w instead.
            u = wv/np.linalg.norm(wv)              # unit normal
            half = (1/np.linalg.norm(wv))          # margin on each side
            p0, p1 = -u*half, u*half
            ax.annotate("", xy=p1, xytext=p0,
                        arrowprops=dict(arrowstyle="<|-|>", color="#2a9d8f",
                                        lw=2.2))
            ax.text(0.15, 1.35, r"$2/\|w\|$", color="#1d6b60",
                    fontsize=11.5, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white",
                              ec="none", alpha=.85))
            # support vectors are exactly the points with y(w^T x + b) = 1
            for P, y in [(pos, 1), (neg, -1)]:
                sv = P[np.isclose(y*(P @ wv + bv), 1.0)]
                ax.scatter(sv[:, 0], sv[:, 1], s=230, facecolor="none",
                           edgecolor="#d1495b", linewidth=2.6, zorder=6)
            width = 2/np.linalg.norm(wv)
            ax.set_title("SVM\nMAXIMUM margin; circled points are the\n"
                         r"SUPPORT VECTORS ($\alpha_i>0$)"
                         f"   —   width $2/\\|w\\|$ = {width:.2f}", fontsize=10.5)

        ax.axhline(0, color="grey", lw=.6); ax.axvline(0, color="grey", lw=.6)
        ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.4, 4.4)
        ax.set_aspect("equal")
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    axes[0].legend(loc="lower right", fontsize=9)
    save(fig, "perceptron_vs_svm_margin.png")


# ---------------------------------------------------------------------------
# 24. Soft margin: the effect of C
# ---------------------------------------------------------------------------
def fig_svm_soft_margin_C():
    n = 45
    A = rng.normal([-1.0, -0.5], 1.15, size=(n, 2))
    B = rng.normal([1.2, 0.8], 1.15, size=(n, 2))
    Xd = np.vstack([A, B]); yd = np.r_[-np.ones(n), np.ones(n)]

    def fit_hinge(C, iters=6000, eta=2e-3):
        """min 1/2||w||^2 + C * sum hinge   via subgradient descent"""
        w = np.zeros(2); b = 0.0
        for _ in range(iters):
            m = yd*(Xd @ w + b)
            viol = m < 1
            gw = w - C*(yd[viol, None]*Xd[viol]).sum(axis=0)
            gb = -C*yd[viol].sum()
            w -= eta*gw; b -= eta*gb
        return w, b

    t = np.linspace(-5, 5, 2)
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.0))
    for ax, C, note in [
            (axes[0], 0.01, "SMALL C — violations tolerated\nWIDE margin, more regularised (underfit risk)"),
            (axes[1], 100.0, "LARGE C — violations punished\nNARROW margin, close to hard margin (overfit risk)")]:
        w, b = fit_hinge(C)
        ax.scatter(A[:, 0], A[:, 1], s=26, color="#c07800", marker="s", alpha=.8)
        ax.scatter(B[:, 0], B[:, 1], s=26, color="#12457a", alpha=.8)
        ax.plot(t, -(w[0]*t + b)/w[1], color="#d1495b", lw=2.6)
        for c in (1, -1):
            ax.plot(t, -(w[0]*t + b - c)/w[1], color="#2a9d8f", lw=1.8, ls="--")
        ax.fill_between(t, -(w[0]*t + b - 1)/w[1], -(w[0]*t + b + 1)/w[1],
                        color="#2a9d8f", alpha=.13)
        width = 2/np.linalg.norm(w)
        ax.set_title(f"C = {C:g}\n{note}\nmargin width $2/\\|w\\|$ = {width:.2f}",
                     fontsize=10)
        ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.2, 4.2)
        ax.set_aspect("equal"); ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    save(fig, "svm_soft_margin_C.png")


# ---------------------------------------------------------------------------
# 25. Surrogate loss functions (all convex upper bounds on 0-1)
# ---------------------------------------------------------------------------
def fig_surrogate_losses():
    z = np.linspace(-3, 3, 900)
    fig, ax = plt.subplots(figsize=(7.4, 5.0))

    ax.step(z, (z <= 0).astype(float), where="post", color="black", lw=2.8,
            label="0-1 loss  (the target — NON-convex)")
    ax.plot(z, np.maximum(0, 1 - z), color="#2a9d8f", lw=2.4,
            label=r"hinge  $\max(0,1-z)$  — SVM")
    ax.plot(z, np.log(1 + np.exp(-z)), color="#3b7dd8", lw=2.4,
            label=r"logistic  $\log(1+e^{-z})$  — logistic reg.")
    ax.plot(z, np.maximum(0, -z), color="#9b5de5", lw=2.2, ls="--",
            label=r"perceptron  $\max(0,-z)$")
    ax.plot(z, np.exp(-z), color="#d1495b", lw=2.4,
            label=r"exponential  $e^{-z}$  — AdaBoost")

    ax.axvline(0, color="grey", lw=.8, ls=":")
    ax.axvline(1, color="grey", lw=.8, ls=":")
    ax.text(1.06, 0.22, "z = 1", fontsize=9, color="#4a5a6a")
    ax.text(-2.9, 3.30, "← misclassified", fontsize=9.5, color="#8a2436",
            fontweight="bold")
    ax.text(1.55, 3.30, "correctly classified →", fontsize=9.5, color="#1d6b60",
            fontweight="bold")
    ax.annotate("hinge hits exactly 0\nfor z ≥ 1", xy=(1.6, 0), xytext=(1.5, 1.05),
                color="#1d6b60", fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#1d6b60"))
    # anchor must stay INSIDE the axes or the whole annotation gets clipped
    ax.annotate("exponential explodes\n⇒ very outlier-sensitive",
                xy=(-1.55, np.exp(1.55)), xytext=(-2.92, 5.15),
                color="#8a2436", fontsize=9, fontweight="bold", ha="left",
                arrowprops=dict(arrowstyle="-|>", color="#8a2436"))

    ax.set_xlim(-3, 3); ax.set_ylim(-0.15, 6)
    ax.set_xlabel(r"margin   $z = y\,(w^T x)$")
    ax.set_ylabel("loss")
    ax.set_title("Every algorithm = a different convex SURROGATE for 0-1 loss\n"
                 "(this is how classification becomes differentiable)",
                 fontsize=11)
    ax.legend(loc="upper right", fontsize=8.8)
    ax.grid(alpha=.3)
    save(fig, "surrogate_losses.png")


# ---------------------------------------------------------------------------
# 26. Bagging (parallel, cuts variance) vs Boosting (sequential, cuts bias)
# ---------------------------------------------------------------------------
def fig_bagging_vs_boosting():
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8))

    def box(ax, x, y, w, h, txt, fc, ec, fs=9):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                                   lw=1.8, zorder=3))
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=fs,
                zorder=4, color="#12457a", fontweight="bold")

    # ---- bagging: parallel ----
    ax = axes[0]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    box(ax, 3.4, 8.4, 3.2, 1.1, "full dataset", "#e8eef7", "#3b7dd8")
    for i, yy in enumerate([6.0, 4.2, 2.4]):
        box(ax, 0.6, yy, 2.6, 1.0, f"bootstrap {i+1}\n(with replacement)",
            "#cfe0f5", "#3b7dd8", 7.6)
        box(ax, 4.4, yy, 2.4, 1.0, "deep tree", "#f8ddb0", "#c07800", 8.4)
        ax.annotate("", xy=(4.4, yy+.5), xytext=(3.2, yy+.5),
                    arrowprops=dict(arrowstyle="-|>", color="#7f8fa6", lw=1.5))
        ax.annotate("", xy=(1.9, yy+1.0), xytext=(5.0, 8.4),
                    arrowprops=dict(arrowstyle="-|>", color="#7f8fa6", lw=1.2))
        ax.annotate("", xy=(8.0, 4.9), xytext=(6.8, yy+.5),
                    arrowprops=dict(arrowstyle="-|>", color="#7f8fa6", lw=1.2))
    box(ax, 7.4, 4.4, 2.2, 1.0, "average /\nmajority vote", "#cfe0f5", "#12457a", 8)
    ax.text(5, 0.9, "PARALLEL — models are independent\nreduces VARIANCE  "
                    "(Random Forest)", ha="center", fontsize=10,
            fontweight="bold", color="#12457a")
    ax.set_title("BAGGING", fontsize=12, fontweight="bold")

    # ---- boosting: sequential ----
    ax = axes[1]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    xs = [0.5, 3.4, 6.3]
    for i, x in enumerate(xs):
        box(ax, x, 5.6, 2.5, 1.2, f"stump $h_{i+1}$\n$\\alpha_{i+1}$",
            "#f8ddb0", "#c07800", 9)
        box(ax, x, 3.2, 2.5, 1.0, "reweight\nwrong points ↑", "#fde2e4",
            "#d1495b", 7.6)
        ax.annotate("", xy=(x+1.25, 5.6), xytext=(x+1.25, 4.2),
                    arrowprops=dict(arrowstyle="-|>", color="#d1495b", lw=1.6))
        if i < 2:
            ax.annotate("", xy=(xs[i+1], 3.7), xytext=(x+2.5, 3.7),
                        arrowprops=dict(arrowstyle="-|>", color="#7f8fa6", lw=1.8))
    box(ax, 2.6, 8.2, 4.8, 1.1, r"$H(x)=\mathrm{sign}(\sum_t \alpha_t h_t(x))$",
        "#cfe0f5", "#12457a", 9.5)
    for x in xs:
        ax.annotate("", xy=(5.0, 8.2), xytext=(x+1.25, 6.8),
                    arrowprops=dict(arrowstyle="-|>", color="#7f8fa6", lw=1.1))
    ax.text(5, 1.5, "SEQUENTIAL — each model fixes the last one's mistakes\n"
                    "reduces BIAS  (AdaBoost)", ha="center", fontsize=10,
            fontweight="bold", color="#8a5300")
    ax.set_title("BOOSTING", fontsize=12, fontweight="bold")
    save(fig, "bagging_vs_boosting.png")


# ---------------------------------------------------------------------------
# 27. Neural network architecture and parameter count
# ---------------------------------------------------------------------------
def fig_neural_network():
    layers = [4, 5, 3, 1]
    names = ["input\n(4)", "hidden 1\n(5)", "hidden 2\n(3)", "output\n(1)"]
    xs = np.linspace(1.0, 9.0, len(layers))

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(-0.4, 7.4)

    pos = []
    for x, k in zip(xs, layers):
        ys = np.linspace(6.2, 6.2 - 1.15*(k-1), k) if k > 1 else np.array([4.5])
        ys = ys - (ys.mean() - 4.2)
        pos.append([(x, y) for y in ys])

    for a, b in zip(pos[:-1], pos[1:]):
        for (x0, y0) in a:
            for (x1, y1) in b:
                ax.plot([x0, x1], [y0, y1], color="#c7d3e3", lw=.8, zorder=1)

    cols = ["#12457a", "#3b7dd8", "#3b7dd8", "#d1495b"]
    for (layer, c) in zip(pos, cols):
        for (x, y) in layer:
            ax.add_patch(plt.Circle((x, y), .26, facecolor="white",
                                    edgecolor=c, lw=2.2, zorder=3))

    for x, nm in zip(xs, names):
        ax.text(x, 7.0, nm, ha="center", fontsize=10, fontweight="bold",
                color="#12457a")

    calc = [f"{a}×{b} + {b} = {a*b + b}" for a, b in zip(layers[:-1], layers[1:])]
    total = sum(a*b + b for a, b in zip(layers[:-1], layers[1:]))
    for x, c in zip((xs[:-1] + xs[1:])/2, calc):
        ax.text(x, 1.55, c, ha="center", fontsize=9.5, color="#8a5300",
                fontweight="bold")
    ax.text(5, 0.55, f"total = {total} parameters", ha="center", fontsize=12.5,
            fontweight="bold", color="#d1495b")
    ax.text(5, 2.35, "per layer:   weights $n_{in}\\times n_{out}$   +   "
                     "biases $n_{out}$", ha="center", fontsize=10,
            color="#12457a")
    ax.set_title("Counting neural-network parameters   (4 → 5 → 3 → 1)",
                 fontsize=12)
    save(fig, "neural_network.png")


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
    # Week 8
    fig_nb_parameter_explosion()
    fig_nb_laplace_smoothing()
    fig_nb_independence_assumption()
    fig_gaussian_nb_boundaries()
    # Weeks 9-12
    fig_sigmoid_logistic()
    fig_perceptron_vs_svm()
    fig_svm_soft_margin_C()
    fig_surrogate_losses()
    fig_bagging_vs_boosting()
    fig_neural_network()
    print("done")
