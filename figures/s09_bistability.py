"""Session 9 figures — the separatrix, the threshold, and the hysteresis.

Every one of these is generated from `posb`, using the same functions students
call in the notebook. The plot on the slide is the plot they can reproduce.

Re-cut 18 September 2026: the nullcline-count and a_c(n) figures moved to
session 8 (`figures/s08_phase_plane.py`), which now derives both. What is new
here is the thing session 8 does not do -- turn ONE knob on Gardner's actual
device and watch a stable state be annihilated by the saddle. `fig_fold` is
four states of that drawing for `Deck.derivation_fig()`; `fig_hysteresis` is
Fig. 5a's theoretical curve recomputed from the legend's own parameters, and
it puts the threshold at 39 uM IPTG, which is where the paper's data jump.

Run:  python tools/build_figures.py s09
"""
import numpy as np

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN, RULE
from posb import (toggle_model, stability_report, nullcline,
                  toggle_alpha_critical)

plt = use()
OUT = "figures/build"
PANEL = (5.4, 4.9)
U_COL, V_COL = TEAL, AMBER          # du/dt = 0 and dv/dt = 0, as in session 8

# pTAK117, from the Fig. 5 legend of Gardner, Cantor & Collins 2000.
A1, A2, BETA, GAMMA = 156.25, 15.6, 2.5, 1.0
K_IPTG, ETA = 2.9618e-5, 2.0015     # M, and the cooperativity of IPTG binding


def iptg_model(iptg=0.0):
    """pTAK117 with the Fig. 5 IPTG term: u -> u / (1 + I/K)^eta in dv/dt.

    Bound LacI does not repress, so promoter 2 sees less u. `s` below is
    that factor; s = 1 with no inducer.
    """
    from posb.core import Reaction, Model
    s = (1 + iptg / K_IPTG) ** ETA
    return Model(
        [Reaction({}, {"u": 1},
                  rate=lambda c, p: A1 / (1 + max(c["v"], 0.0) ** BETA),
                  name="LacI synthesis, repressed by cI"),
         Reaction({"u": 1}, {}, k=1.0, name="removal of LacI"),
         Reaction({}, {"v": 1},
                  rate=lambda c, p: A2 / (1 + (max(c["u"], 0.0) / s) ** GAMMA),
                  name="cI synthesis, repressed by IPTG-free LacI"),
         Reaction({"v": 1}, {}, k=1.0, name="removal of cI")],
        params={"s": s}, species=["u", "v"])


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _points(ax, m, ms=11):
    pts = stability_report(m, grid=(1e-3, 300, 9))
    for f in pts:
        p, kind = f["point"], f["type"]
        if kind.startswith("stable"):
            ax.plot(p["u"], p["v"], "o", ms=ms, color=INK, zorder=6)
        else:
            ax.plot(p["u"], p["v"], "o", ms=ms, mfc="white", mec=RED, mew=2.4,
                    zorder=6)
    return pts


# ---------------------------------------------------------------------------
# Kept from the first build, at legible sizes
# ---------------------------------------------------------------------------

def fig_nullclines():
    """The central claim, restated: cooperativity bends the nullcline."""
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.9))
    grid = np.linspace(0.001, 4.0, 400)
    for ax, n in zip(axes, (1, 2)):
        m = toggle_model(3.0, 3.0, n=n)
        ax.plot(nullcline(m, "u", "v", grid), grid, lw=2.8, color=U_COL)
        ax.plot(grid, nullcline(m, "v", "u", grid), lw=2.8, color=V_COL)
        pts = _points(ax, m)
        n_st = sum(1 for f in pts if f["type"].startswith("stable"))
        ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_aspect("equal")
        ax.set_xlabel("$u$"); ax.set_ylabel("$v$", rotation=0, labelpad=12)
        ax.set_title(rf"$n={n}$, $\alpha=3$: {n_st} stable "
                     f"state{'s' if n_st > 1 else ''}")
    axes[0].text(1.4, 3.1, "$du/dt = 0$", color=U_COL, fontsize=15,
                 fontweight="bold")
    axes[0].text(2.2, 1.3, "$dv/dt = 0$", color=V_COL, fontsize=15,
                 fontweight="bold")
    _save(fig, "s09_nullclines")


def fig_separatrix():
    """Why the saddle matters: its stable manifold decides the outcome."""
    m = toggle_model(3.0, 3.0, n=2)
    fig, ax = plt.subplots(figsize=PANEL)
    U, V = np.meshgrid(np.linspace(0.02, 4, 22), np.linspace(0.02, 4, 22))
    dU, dV = np.zeros_like(U), np.zeros_like(V)
    for i in range(U.shape[0]):
        for j in range(U.shape[1]):
            dU[i, j], dV[i, j] = m.rhs(0.0, [U[i, j], V[i, j]])
    ax.streamplot(U, V, dU, dV, color=MUTED, linewidth=0.7, density=1.0,
                  arrowsize=0.9)
    for x0 in ([0.9, 1.5], [1.5, 0.9], [0.2, 3.5], [3.5, 0.2]):
        tr = m.simulate({"u": x0[0], "v": x0[1]}, (0, 20), n_points=400)
        ax.plot(tr["u"], tr["v"], lw=2.4,
                color=TEAL if tr.final()["u"] > tr.final()["v"] else AMBER)
    _points(ax, m)
    ax.plot([0, 4], [0, 4], ls="--", lw=1.4, color=RED, alpha=.7)
    ax.text(2.55, 2.85, "separatrix", color=RED, fontsize=15, rotation=45)
    ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_aspect("equal")
    ax.set_xlabel("$u$"); ax.set_ylabel("$v$", rotation=0, labelpad=12)
    ax.set_title(r"$n=2$, $\alpha=3$: which state you reach")
    _save(fig, "s09_separatrix")


def fig_bifurcation():
    """The analytic boundary a_c(n), checked against numerics."""
    fig, ax = plt.subplots(figsize=(6.4, 4.9))
    ns = np.linspace(1.02, 5, 300)
    ax.plot(ns, [toggle_alpha_critical(n) for n in ns], lw=2.8, color=TEAL,
            label=r"$a_c = n\,(n-1)^{-(n+1)/n}$")
    for n in (1.25, 1.5, 2.0, 2.5, 3.0, 4.0):
        for alpha in np.geomspace(0.5, 30, 40):
            k = sum(1 for f in stability_report(toggle_model(alpha, alpha, n=n),
                                                grid=(1e-3, 60, 7))
                    if f["type"].startswith("stable"))
            if k >= 2:
                ax.plot(n, alpha, "o", ms=6.5, color=AMBER, zorder=4)
                break
    ax.plot([], [], "o", ms=6.5, color=AMBER, label="smallest bistable $a$, found numerically")
    ax.axvline(1.0, color=RED, ls="--", lw=1.6)
    ax.fill_betweenx([0.5, 40], 0.5, 1.0, color=RED, alpha=.06)
    ax.set_xlim(0.6, 5); ax.set_ylim(0.5, 40); ax.set_yscale("log")
    ax.set_xlabel("cooperativity $n$"); ax.set_ylabel("$a$")
    ax.set_title("Bistable region of the symmetric toggle")
    ax.legend(loc="upper right", fontsize=14)
    _save(fig, "s09_bifurcation")


# ---------------------------------------------------------------------------
# New: one knob on the real device, and a state annihilated
# ---------------------------------------------------------------------------

def iptg_threshold():
    """The IPTG concentration at which pTAK117's low state is annihilated.

    Bisection on the number of fixed points. Returns (s_c, IPTG_c in M).
    Verified 18 Sep 2026: s_c = 5.41, IPTG_c = 39 uM -- where Fig. 5a jumps.
    """
    u = np.geomspace(1e-4, 3e3, 20000)

    def count(s):
        v = A2 / (1 + (u / s) ** GAMMA)
        return np.count_nonzero(np.diff(np.sign(u - A1 / (1 + v ** BETA))) != 0)

    lo, hi = 1.0, 10.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if count(mid) == 3 else (lo, mid)
    s_c = (lo + hi) / 2
    return s_c, K_IPTG * (s_c ** (1 / ETA) - 1)


def _plane(m, title):
    fig, ax = plt.subplots(figsize=PANEL)
    grid = np.geomspace(0.02, 400, 600)
    ax.plot(nullcline(m, "u", "v", grid, bracket=(1e-6, 1e4)), grid, lw=2.8,
            color=U_COL)
    ax.plot(grid, nullcline(m, "v", "u", grid, bracket=(1e-6, 1e4)), lw=2.8,
            color=V_COL)
    pts = _points(ax, m)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.02, 400); ax.set_ylim(0.02, 400)
    ax.set_xlabel("$u$  (LacI)"); ax.set_ylabel("$v$  (cI, GFP)")
    ax.set_title(title)
    return fig, ax, pts


def fig_fold():
    """pTAK117 as IPTG rises: the low state and the saddle meet and annihilate."""
    s_c, i_c = iptg_threshold()

    def iptg_for(s):
        return K_IPTG * (s ** (1 / ETA) - 1)

    fig, ax, pts = _plane(iptg_model(0.0), "no IPTG: three crossings")
    ax.text(0.03, 0.05, "$du/dt = 0$", color=U_COL, fontsize=15, fontweight="bold")
    ax.text(15, 40, "$dv/dt = 0$", color=V_COL, fontsize=15, fontweight="bold")
    ax.annotate("low state:\nLacI on, GFP off", xy=(155, 0.1), xytext=(3, 0.25),
                color=INK, fontsize=14,
                arrowprops=dict(arrowstyle="-", color=INK, lw=1.2))
    ax.annotate("high state", xy=(0.33, 11.7), xytext=(0.05, 90), color=INK,
                fontsize=14, arrowprops=dict(arrowstyle="-", color=INK, lw=1.2))
    _save(fig, "s09_fold_p1")

    fig, ax, pts = _plane(iptg_model(iptg_for(3.0)),
                          f"{iptg_for(3.0) * 1e6:.0f} µM IPTG: still three")
    ax.text(0.03, 0.05, "the $u$-nullcline has not moved", color=U_COL,
            fontsize=14)
    ax.annotate("", xy=(60, 8), xytext=(12, 8),
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=V_COL,
                                mutation_scale=18))
    ax.text(3, 25, "the $v$-nullcline\nstretches right", color=V_COL,
            fontsize=14)
    _save(fig, "s09_fold_p2")

    fig, ax, pts = _plane(iptg_model(i_c * 0.999),
                          f"{i_c * 1e6:.0f} µM: the curves touch")
    ax.text(0.03, 0.05, "saddle-node: the low state\nand the saddle annihilate",
            color=RED, fontsize=14)
    _save(fig, "s09_fold_p3")

    fig, ax, pts = _plane(iptg_model(iptg_for(20.0)),
                          f"{iptg_for(20.0) * 1e6:.0f} µM: one state left")
    ax.plot(155, 0.1, "o", ms=11, mfc="none", mec=MUTED, mew=2, zorder=6)
    ax.annotate("", xy=(0.5, 8), xytext=(120, 0.13),
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=INK,
                                mutation_scale=20,
                                connectionstyle="arc3,rad=0.3"))
    ax.text(0.6, 0.3, "the cell has\nnowhere else to go", color=INK, fontsize=14)
    _save(fig, "s09_fold_p4")


def fig_hysteresis():
    """Fig. 5a's theoretical curve, recomputed: cI (GFP) against IPTG, with the jump."""
    s_c, i_c = iptg_threshold()
    iptg = np.geomspace(1e-7, 1e-3, 220)
    hi, lo, mid = [], [], []
    for I in iptg:
        pts = stability_report(iptg_model(I), grid=(1e-3, 300, 9))
        st = sorted([f["point"]["v"] for f in pts if f["type"].startswith("stable")])
        sd = [f["point"]["v"] for f in pts if f["type"] == "saddle"]
        hi.append(st[-1]); lo.append(st[0] if len(st) > 1 else np.nan)
        mid.append(sd[0] if sd else np.nan)
    hi, lo, mid = map(np.array, (hi, lo, mid))

    fig, ax = plt.subplots(figsize=PANEL)
    ax.plot(iptg, hi, lw=2.8, color=INK)
    ax.plot(iptg, lo, lw=2.8, color=INK)
    ax.plot(iptg, mid, lw=2.0, ls="--", color=RED)
    ax.axvline(i_c, color=MUTED, lw=1.2, ls=":")
    ax.annotate("", xy=(i_c * 1.05, hi[np.searchsorted(iptg, i_c)] * 0.8),
                xytext=(i_c * 1.05, 0.13),
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=INK,
                                mutation_scale=20))
    ax.annotate("", xy=(1.3e-7, hi[0]), xytext=(i_c * 0.8, hi[0]),
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=GREEN,
                                mutation_scale=20))
    ax.text(1.5e-7, hi[0] * 1.6, "remove IPTG: stays high", color=GREEN,
            fontsize=14)
    ax.text(i_c * 1.3, 0.5, f"jump at\n{i_c * 1e6:.0f} µM", color=INK,
            fontsize=14)
    ax.text(2e-7, 0.05, "low state\n(LacI on)", color=INK, fontsize=14)
    ax.text(3e-6, 1.6, "unstable", color=RED, fontsize=14)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1e-7, 1e-3); ax.set_ylim(0.03, 30)
    ax.set_xlabel("[IPTG]  (M)"); ax.set_ylabel("$v^*$  (cI, ∝ GFP)")
    ax.set_title("pTAK117: the threshold, from the model")
    _save(fig, "s09_hysteresis")


FIGURES = [fig_nullclines, fig_separatrix, fig_bifurcation, fig_fold,
           fig_hysteresis]
