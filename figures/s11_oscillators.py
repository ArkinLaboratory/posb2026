"""Session 11 figures — the repressilator, the criterion, and the Hopf boundary.

Everything here comes from `posb`: `repressilator_model`, `loop_gain`,
`leading_real_part`, `sweep` and `hopf_boundary` are the same functions the
students call, so the plot on the slide is the plot in the notebook.

The session's result, derived in class and verified here:

    the symmetric ring loses stability exactly when the loop gain g = 2,
    which gives   alpha_c = (2/(n-2))**(1/n) * n/(n-2),   infinite for n <= 2.

`fig_criterion` is the five-panel reveal for `Deck.derivation_fig`: the
eigenvalues of the cyclic Jacobian walk out of the left half plane as the gain
rises, and the trajectory beside them stops decaying and starts ticking.
`fig_sweep` is T29 -- the boundary located numerically, by sweeping alpha and
watching the leading real part cross zero, with the analytic value on top.

Run:  python tools/build_figures.py s11
"""
import numpy as np

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN, RULE
from posb import (repressilator_model, repressilator_alpha_critical, loop_gain,
                  sweep, leading_real_part, hopf_boundary, fixed_points,
                  jacobian)

plt = use()
OUT = "figures/build"
N = 3                                  # cooperativity used throughout
AC = repressilator_alpha_critical(N)   # 3.7798 at n = 3
X0 = {"x1": 1.2, "x2": 1.0, "x3": 0.9}


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _run(alpha, t=60.0, n_points=6000, x0=None):
    m = repressilator_model(alpha=alpha, n=N)
    return m.simulate(x0 or X0, (0.0, t), n_points=n_points)


def _eigs(alpha):
    m = repressilator_model(alpha=alpha, n=N)
    p = {"alpha": alpha, "n": N}
    pt = fixed_points(m, [[1.0, 1.0, 1.0]], p)[0]
    return np.linalg.eigvals(jacobian(m, pt, p)), pt


# ---------------------------------------------------------------------------
# 1. The object: three repressors in a ring, below and above the boundary
# ---------------------------------------------------------------------------
def fig_ring_dynamics():
    """Same circuit, two promoter strengths: one settles, one keeps time."""
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4), sharey=False)
    for ax, mult, title in [(axes[0], 0.7, f"$\\alpha = {0.7*AC:.2f}$  —  it settles"),
                            (axes[1], 1.6, f"$\\alpha = {1.6*AC:.2f}$  —  it ticks")]:
        tr = _run(mult * AC)
        for s, c in zip(("x1", "x2", "x3"), (TEAL, CYAN, AMBER)):
            ax.plot(tr.t, tr[s], color=c, lw=2.6, label=s)
        ax.set_xlim(0, 40)
        ax.set_xlabel("time  (protein lifetimes)")
        ax.set_title(title)
        ax.legend(loc="upper right", ncol=3)
    axes[0].set_ylabel("concentration")
    _save(fig, "s11_ring_dynamics")


# ---------------------------------------------------------------------------
# 2. The criterion, revealed one step at a time
# ---------------------------------------------------------------------------
def _plane(ax, ev, g):
    ax.axvline(0, color=MUTED, lw=1.2)
    ax.axhline(0, color=RULE, lw=1.0)
    ax.plot(ev.real, ev.imag, "o", ms=13, color=INK, zorder=5)
    ax.set_xlim(-3.6, 1.4)
    ax.set_ylim(-2.6, 2.6)
    ax.set_xlabel("Re $\\lambda$")
    ax.set_ylabel("Im $\\lambda$")
    ax.set_title(f"$g = {g:.2f}$")


def fig_criterion():
    """Five panels: the eigenvalues cross, and the trajectory starts ticking."""
    # p1 -- the symmetric fixed point exists and everything decays to it
    tr = _run(0.5 * AC)
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    for s, c in zip(("x1", "x2", "x3"), (TEAL, CYAN, AMBER)):
        ax.plot(tr.t, tr[s], color=c, lw=2.6, label=s)
    ax.set_xlim(0, 30)
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("concentration")
    ax.set_title("all three settle to the same value")
    ax.legend(loc="upper right", ncol=3)
    _save(fig, "s11_crit_p1")

    # p2, p3, p4 -- eigenvalues of -I - gP as the gain rises
    for k, mult in enumerate((0.5, 1.0, 1.6), start=2):
        alpha = mult * AC
        ev, _ = _eigs(alpha)
        g = loop_gain(alpha, N)
        fig, ax = plt.subplots(figsize=(5.4, 4.6))
        _plane(ax, ev, g)
        if k == 2:
            ax.text(-3.4, 2.0, "all three in the left half plane:\nthe state is stable",
                    color=INK, fontsize=13)
        if k == 3:
            ax.text(-3.4, 2.0, "the complex pair sits ON the axis:\n"
                                "Re $\\lambda = -1 + g/2 = 0$", color=RED, fontsize=13)
            ax.plot([0, 0], [np.sqrt(3), -np.sqrt(3)], "o", ms=13, mfc="none",
                    mec=RED, mew=2.5, zorder=6)
        if k == 4:
            ax.text(-3.4, 2.0, "the pair has crossed:\nthe state cannot hold",
                    color=RED, fontsize=13)
        _save(fig, f"s11_crit_p{k}")

    # p5 -- above the boundary: a limit cycle
    tr = _run(1.6 * AC, t=120.0, n_points=12000)
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    half = len(tr.t) // 2
    ax.plot(tr["x1"][:half], tr["x2"][:half], color=RULE, lw=1.6)
    ax.plot(tr["x1"][half:], tr["x2"][half:], color=TEAL, lw=3.0)
    pt = fixed_points(repressilator_model(alpha=1.6 * AC, n=N),
                      [[1.0, 1.0, 1.0]], {"alpha": 1.6 * AC, "n": N})[0]
    ax.plot(pt["x1"], pt["x2"], "o", ms=12, mfc="white", mec=RED, mew=2.4,
            zorder=6)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title("the trajectory settles onto a closed loop")
    _save(fig, "s11_crit_p5")


def fig_period():
    """T = 2*pi/sqrt(3) at onset, and how far it drifts once you leave onset.

    Three traces of x1, each at its own alpha, each with one peak-to-peak
    interval measured and marked. This is the figure the period surface needs:
    a phase portrait shows that there IS a cycle but never shows its period.
    """
    rows = [(1.02, "just past onset"),
            (3.0, r"$3\,\alpha_c$"),
            (10.0, r"$10\,\alpha_c$")]
    fig, axes = plt.subplots(3, 1, figsize=(6.0, 3.6), sharex=True)
    for ax, (mult, label) in zip(axes, rows):
        tr = _run(mult * AC, t=220.0, n_points=44000)
        t = np.asarray(tr.t)
        x = np.asarray(tr["x1"])
        keep = t >= 160.0                     # well past the transient
        t, x = t[keep], x[keep]
        pk = [j for j in range(1, len(x) - 1)
              if x[j] > x[j - 1] and x[j] >= x[j + 1]]
        T = float(np.mean(np.diff(t[pk]))) if len(pk) > 2 else float("nan")
        ax.plot(t - t[0], x, color=TEAL, lw=2.2)
        if len(pk) > 2:
            a, b = t[pk[0]] - t[0], t[pk[1]] - t[0]
            y = x[pk[0]]
            ax.annotate("", xy=(a, y), xytext=(b, y),
                        arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
            ax.text(0.5 * (a + b), y, f"  T = {T:.2f}", color=RED,
                    fontsize=11, ha="center", va="bottom")
            ax.plot(t[pk[:3]] - t[0], x[pk[:3]], "o", ms=5, color=RED, zorder=5)
        ax.set_ylabel(r"$x_1$", fontsize=10)
        ax.text(0.99, 0.94, label, transform=ax.transAxes, ha="right",
                va="top", fontsize=10, color=MUTED,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
        ax.set_xlim(0, 24)
        ax.margins(y=0.34)
        ax.tick_params(labelsize=9)
    axes[0].set_title(r"period at onset: $2\pi/\sqrt{3} = 3.628$ lifetimes",
                      fontsize=11)
    axes[-1].set_xlabel("time  (protein lifetimes)", fontsize=11)
    _save(fig, "s11_period")


# ---------------------------------------------------------------------------
# 3. T29: locate the boundary numerically, by sweeping alpha
# ---------------------------------------------------------------------------
def fig_sweep():
    """The Hopf boundary found by parameter sweep, against the analytic value."""
    m = repressilator_model(n=N)
    alphas = np.linspace(0.3 * AC, 3.0 * AC, 140)
    lrp = sweep(m, "alpha", alphas, leading_real_part, params={"n": N})
    found = hopf_boundary(m, "alpha", 0.3 * AC, 3.0 * AC, params={"n": N})

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.5))

    ax = axes[0]
    ax.axhline(0, color=MUTED, lw=1.2)
    ax.plot(alphas, lrp, color=TEAL, lw=3.0)
    ax.axvline(found, color=RED, lw=1.6, ls="--")
    ax.plot([found], [0], "o", ms=11, color=RED, zorder=6)
    ax.text(found + 0.5, min(lrp) * 0.75,
            f"sweep finds\n$\\alpha_c$ = {found:.3f}", color=RED, fontsize=14)
    ax.text(0.3 * AC + 0.1, max(lrp) * 0.72,
            f"analytic\n$\\alpha_c$ = {AC:.3f}", color=INK, fontsize=14)
    ax.set_xlabel(r"$\alpha$")
    ax.set_ylabel(r"max Re $\lambda$  at the fixed point")
    ax.set_title("the eigenvalue crosses")

    # amplitude of the resulting oscillation -- the square-root law of a Hopf
    ax = axes[1]
    amps, xs = [], np.linspace(0.6 * AC, 3.0 * AC, 46)
    for a in xs:
        tr = _run(a, t=260.0, n_points=13000)
        late = tr["x1"][len(tr.t) // 2:]
        amps.append(late.max() - late.min())
    ax.plot(xs, amps, color=TEAL, lw=3.0)
    ax.axvline(AC, color=RED, lw=1.6, ls="--")
    ax.text(AC + 0.4, max(amps) * 0.5,
            "no oscillation\nto the left of here", color=RED, fontsize=14)
    ax.set_xlabel(r"$\alpha$")
    ax.set_ylabel("amplitude of $x_1$")
    ax.set_title("amplitude grows from zero")
    _save(fig, "s11_sweep")


# ---------------------------------------------------------------------------
# 4. The boundary in the (n, alpha) plane -- the counterpart of s09's wedge
# ---------------------------------------------------------------------------
def fig_alpha_critical():
    """alpha_c(n), analytic against numerics, with the n <= 2 wall."""
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ns = np.linspace(2.05, 8.0, 240)
    ax.plot(ns, [repressilator_alpha_critical(n) for n in ns], color=TEAL,
            lw=3.0, label="analytic  $\\alpha_c$")
    ns_num = np.array([2.5, 3.0, 4.0, 5.0, 6.0, 8.0])
    num = []
    for n in ns_num:
        ac = repressilator_alpha_critical(n)
        num.append(hopf_boundary(repressilator_model(n=n), "alpha",
                                 0.3 * ac, 5.0 * ac, params={"n": n}))
    ax.plot(ns_num, num, "o", ms=11, mfc="none", mec=RED, mew=2.4,
            label="found by sweep")
    ax.axvline(2.0, color=MUTED, lw=2.0, ls=":")
    ax.text(2.1, 14, "no oscillation\nat any $\\alpha$ for $n \\leq 2$",
            color=MUTED, fontsize=14)
    ax.set_xlim(1.8, 8.2)
    ax.set_ylim(0, 20)
    ax.set_xlabel("cooperativity  $n$")
    ax.set_ylabel(r"$\alpha_c$")
    ax.legend(loc="upper right")
    _save(fig, "s11_alpha_critical")


FIGURES = [fig_ring_dynamics, fig_criterion, fig_period, fig_sweep,
           fig_alpha_critical]


if __name__ == "__main__":
    print("alpha_c(3) =", AC, " g there =", loop_gain(AC, N))
