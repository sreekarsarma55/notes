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


if __name__ == "__main__":
    fig_pca()
    fig_kernel_pca()
    fig_kmeans()
    fig_elbow()
    print("done")
