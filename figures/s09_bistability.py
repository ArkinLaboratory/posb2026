"""Session 9 figures — nullclines, the separatrix, and the bifurcation boundary.

Every one of these is generated from `posb`, using the same functions students
call in the notebook. The plot on the slide is the plot they can reproduce.

Run:  python tools/build_figures.py s09
"""
import numpy as np

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED
from posb import toggle_model, stability_report, nullcline, toggle_alpha_critical

plt = use()
OUT = "figures/build"


def fig_nullclines():
    """The central claim of the session: cooperativity bends the nullcline."""
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.3))
    grid = np.linspace(0.001, 4.0, 400)

    for ax, n, alpha in zip(axes, (1, 2), (3.0, 3.0)):
        m = toggle_model(alpha, alpha, n=n)
        u_of_v = nullcline(m, "u", "v", grid)     # du/dt = 0
        v_of_u = nullcline(m, "v", "u", grid)     # dv/dt = 0

        ax.plot(u_of_v, grid, lw=2.2, color=TEAL, label=r"$du/dt=0$")
        ax.plot(grid, v_of_u, lw=2.2, color=CYAN, label=r"$dv/dt=0$")

        for f in stability_report(m, grid=(1e-3, 20, 9)):
            p, kind = f["point"], f["type"]
            if kind.startswith("stable"):
                ax.plot(p["u"], p["v"], "o", ms=9, color=INK, zorder=5)
            elif kind == "saddle":
                ax.plot(p["u"], p["v"], "o", ms=9, mfc="white",
                        mec=RED, mew=2.2, zorder=5)

        ax.set_xlim(0, 4); ax.set_ylim(0, 4)
        ax.set_xlabel("$u$"); ax.set_ylabel("$v$")
        ax.set_aspect("equal")
        n_st = sum(1 for f in stability_report(m, grid=(1e-3, 20, 9))
                   if f["type"].startswith("stable"))
        ax.set_title(rf"$n={n}$, $\alpha={alpha:g}$  —  "
                     f"{n_st} stable state{'s' if n_st > 1 else ''}")
        ax.legend(loc="upper right", fontsize=9.5)

    axes[0].text(0.5, 3.5, "crosses once", color=MUTED, fontsize=10.5)
    axes[1].text(0.35, 3.5, "crosses three times", color=MUTED, fontsize=10.5)
    fig.tight_layout()
    fig.savefig(f"{OUT}/s09_nullclines.png")
    plt.close(fig)


def fig_separatrix():
    """Why the saddle matters: its stable manifold decides the outcome."""
    m = toggle_model(3.0, 3.0, n=2)
    fig, ax = plt.subplots(figsize=(5.2, 4.8))

    U, V = np.meshgrid(np.linspace(0.02, 4, 22), np.linspace(0.02, 4, 22))
    dU = np.zeros_like(U); dV = np.zeros_like(V)
    for i in range(U.shape[0]):
        for j in range(U.shape[1]):
            d = m.rhs(0.0, [U[i, j], V[i, j]])
            dU[i, j], dV[i, j] = d
    ax.streamplot(U, V, dU, dV, color=MUTED, linewidth=0.6,
                  density=1.1, arrowsize=0.7)

    for x0 in ([0.9, 1.5], [1.5, 0.9], [0.2, 3.5], [3.5, 0.2]):
        tr = m.simulate({"u": x0[0], "v": x0[1]}, (0, 20), n_points=400)
        ax.plot(tr["u"], tr["v"], lw=2.0,
                color=TEAL if tr.final()["u"] > tr.final()["v"] else CYAN)

    for f in stability_report(m, grid=(1e-3, 20, 9)):
        p, kind = f["point"], f["type"]
        if kind.startswith("stable"):
            ax.plot(p["u"], p["v"], "o", ms=10, color=INK, zorder=5)
        else:
            ax.plot(p["u"], p["v"], "o", ms=10, mfc="white", mec=RED,
                    mew=2.2, zorder=5)
    ax.plot([0, 4], [0, 4], ls="--", lw=1.2, color=RED, alpha=.6)
    ax.text(2.6, 2.75, "separatrix", color=RED, fontsize=10.5, rotation=45)

    ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_aspect("equal")
    ax.set_xlabel("$u$"); ax.set_ylabel("$v$")
    ax.set_title(r"$n=2$, $\alpha=3$  —  which state you reach")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s09_separatrix.png")
    plt.close(fig)


def fig_bifurcation():
    """The analytic boundary, checked against numerics.

    This is the figure that makes 'cooperativity is required' a theorem
    rather than an observation.
    """
    fig, ax = plt.subplots(figsize=(6.2, 4.4))

    ns = np.linspace(1.02, 5, 300)
    ax.plot(ns, [toggle_alpha_critical(n) for n in ns], lw=2.4, color=TEAL,
            label=r"$\alpha_c = n\,(n-1)^{-(n+1)/n}$  (analytic)")

    # independent numerical check on a coarse grid
    ncheck = [1.25, 1.5, 2.0, 2.5, 3.0, 4.0]
    for n in ncheck:
        for alpha in np.geomspace(0.5, 30, 40):
            k = sum(1 for f in stability_report(toggle_model(alpha, alpha, n=n),
                                                grid=(1e-3, 60, 7))
                    if f["type"].startswith("stable"))
            if k >= 2:
                ax.plot(n, alpha, "o", ms=5.5, color=AMBER, zorder=4)
                break

    ax.plot([], [], "o", ms=5.5, color=AMBER,
            label="smallest bistable $\\alpha$ found numerically")
    ax.axvline(1.0, color=RED, ls="--", lw=1.4)
    ax.text(1.04, 22, "no bistability\nat any $\\alpha$ for $n\\leq 1$",
            color=RED, fontsize=10)
    ax.fill_betweenx([0.5, 40], 0.5, 1.0, color=RED, alpha=.06)

    ax.set_xlim(0.6, 5); ax.set_ylim(0.5, 40); ax.set_yscale("log")
    ax.set_xlabel("cooperativity $n$")
    ax.set_ylabel(r"synthesis rate $\alpha$")
    ax.set_title("Bistable region of the symmetric toggle")
    ax.legend(loc="upper right", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(f"{OUT}/s09_bifurcation.png")
    plt.close(fig)


FIGURES = [fig_nullclines, fig_separatrix, fig_bifurcation]
