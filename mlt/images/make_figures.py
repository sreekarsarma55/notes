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
    print("done")
