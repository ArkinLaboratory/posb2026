"""Session 4 figures — timescale separation, Michaelis-Menten, and the Hill form.

Four figures, each one built to make a claim the session would otherwise have to
assert:

  * the QSSA is not a statement about enzymes, it is a statement about a small
    parameter -- so the figure that matters is the one where the parameter is
    NOT small and the reduction visibly fails;
  * the validity condition is E_tot << K_M + S_0, not the textbook E << S, and
    the error scales linearly in that ratio over four decades, which is what
    makes it a condition rather than a slogan;
  * a Hill coefficient is a sensitivity, and 81^(1/n) is the whole content of
    that sentence;
  * two INDEPENDENT sites give a Hill function with n = 1. Not 2. This is the
    single most common misreading of a fitted Hill coefficient in the
    literature the students are about to start reading.

The enzyme parameters are the ones PS1 Q3 uses -- k1 = 1, k_-1 = 1, k2 = 0.1,
S0 = 1, and E0 either 0.001 or 1.0 -- deliberately, so the figure on the slide
is the numerical experiment they are asked to reproduce, not a cousin of it.

    python tools/build_figures.py s04
"""
import numpy as np
from scipy.integrate import solve_ivp

from figures.style import use, AMBER, CYAN, INK, MUTED, RED, RULE, TEAL

plt = use()
OUT = "figures/build"

# PS1 Q3's parameters, exactly.
K1, KM1, K2 = 1.0, 1.0, 0.1
S0 = 1.0
KM = (KM1 + K2) / K1          # 1.1
VMAX_PER_E = K2               # V_max = k2 * E_tot


def _full(t, y):
    """E + S <-> ES -> E + P, every species tracked. y = [E, S, ES, P]."""
    E, S, ES, P = y
    bind = K1 * E * S
    back = KM1 * ES
    cat = K2 * ES
    return [-bind + back + cat,
            -bind + back,
            +bind - back - cat,
            +cat]


def _reduced(t, y, e_tot):
    """The Michaelis-Menten reduction: two variables, one algebraic rate."""
    S, P = y
    v = VMAX_PER_E * e_tot * S / (KM + S)
    return [-v, +v]


def _pair(e_tot, t_end):
    """Integrate both models on a shared grid. Returns (t, P_full, P_reduced)."""
    t = np.linspace(0, t_end, 2000)
    kw = dict(t_eval=t, rtol=1e-10, atol=1e-12, method="LSODA")
    full = solve_ivp(_full, (0, t_end), [e_tot, S0, 0.0, 0.0], **kw)
    red = solve_ivp(_reduced, (0, t_end), [S0, 0.0], args=(e_tot,), **kw)
    return t, full.y[3], red.y[1]


def qssa_error(e_tot, t_end):
    """max |P_full - P_reduced| / S0 -- the metric PS1 Q3c asks students to write."""
    _, pf, pr = _pair(e_tot, t_end)
    return float(np.max(np.abs(pf - pr)) / S0)


# --------------------------------------------------------------------------
def tau(e_tot):
    """The natural clock: time to turn over one S_0's worth of substrate.

    Both panels of the regime figure run to the same number of these, and so
    does PS1 Q3c, which asks for five. A fixed wall-clock window would compare
    the approximation in one case and the integration window in the other,
    because tau is inversely proportional to E_tot -- and worse, would spread a
    fixed output grid so thinly over a fast reaction that the peak error is
    missed entirely.
    """
    return (KM + S0) / (VMAX_PER_E * e_tot)


def fig_qssa_regimes():
    """The same approximation, right and wrong, on the same axes.

    Two panels, identical except for E_tot, and time measured in each system's
    own turnover time so the comparison is like for like. The left is the
    textbook picture and is worth about four seconds. The right is the figure:
    nothing about the enzyme changed, the reduction is algebraically identical,
    and it is wrong by fifteen per cent of the substrate.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0))

    for ax, (e_tot, tag) in zip(axes, [
            (0.001, "E$_{tot}$ = 0.001"),
            (1.000, "E$_{tot}$ = 1.0")]):
        T = tau(e_tot)
        t, pf, pr = _pair(e_tot, 12.0 * T)
        ax.plot(t / T, pf, color=TEAL, lw=2.4, label="full, four species")
        ax.plot(t / T, pr, color=AMBER, lw=2.0, ls="--", label="Michaelis–Menten")

        err = np.max(np.abs(pf - pr)) / S0
        ratio = e_tot / (KM + S0)
        ax.set_xlabel(r"time / $\tau$,   $\tau = (K_M + S_0)/V_{max}$")
        ax.set_ylabel("[P]")
        ax.set_ylim(-0.03, 1.12)
        ax.set_xlim(0, 12)
        ax.set_title(f"{tag}    E$_{{tot}}$/(K$_M$+S$_0$) = {ratio:.3g}",
                     color=INK, fontsize=12)
        ax.text(0.5, 0.965, f"max error over the whole reaction: {err:.1e}",
                transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
                color=RED if err > 0.01 else MUTED,
                fontweight="bold" if err > 0.01 else "normal")
        ax.legend(loc="lower right", fontsize=9.5)

    fig.suptitle("Same reduction, same enzyme, same clock. Only the enzyme "
                 "CONCENTRATION changed.", color=INK, fontsize=12.5, y=1.02)
    fig.tight_layout()
    fig.savefig(f"{OUT}/s04_qssa_regimes.png")
    plt.close(fig)


def fig_qssa_error():
    """The error is set by one dimensionless group, over four decades.

    This is the figure that turns "E must be small" into a condition you can
    check before you trust a model. The x axis is the group that Segel's
    analysis says controls it; the collapse onto a straight line of slope one is
    the claim.
    """
    ratios, errs = [], []
    for e_tot in np.geomspace(1e-4, 3e0, 22):
        # Integrate long enough that the reaction actually finishes; the slow
        # cases need far more time than the fast ones, and a fixed window would
        # measure the window rather than the approximation.
        t_end = 30.0 * (KM + S0) / (VMAX_PER_E * e_tot)
        ratios.append(e_tot / (KM + S0))
        errs.append(qssa_error(e_tot, t_end))

    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ax.loglog(ratios, errs, "o-", color=TEAL, lw=2.0, ms=5,
              label="measured  max|ΔP|/S$_0$")
    ref = np.array(ratios)
    ax.loglog(ref, errs[0] * ref / ref[0], color=MUTED, lw=1.2, ls=":",
              label="slope 1")
    ax.axhline(0.01, color=RULE, lw=1.0)
    ax.text(ratios[0] * 1.2, 0.0115, "1% error", fontsize=9.5, color=MUTED)

    for e_tot, lab in [(0.001, "PS1: E$_{tot}$ = 0.001"), (1.0, "PS1: E$_{tot}$ = 1.0")]:
        r = e_tot / (KM + S0)
        e = qssa_error(e_tot, 30.0 * (KM + S0) / (VMAX_PER_E * e_tot))
        ax.plot([r], [e], "o", color=AMBER, ms=10, zorder=5)
        ax.annotate(lab, (r, e), textcoords="offset points", xytext=(8, -12),
                    fontsize=9.5, color=AMBER, fontweight="bold")

    ax.set_xlabel(r"$E_{tot} / (K_M + S_0)$   —  the group that controls it")
    ax.set_ylabel("relative error in [P]")
    ax.set_title("The QSSA fails on a ratio, not on a species", color=INK)
    ax.legend(loc="upper left", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(f"{OUT}/s04_qssa_error.png")
    plt.close(fig)


# --------------------------------------------------------------------------
def hill(x, K, n):
    return x ** n / (K ** n + x ** n)


def fig_hill_family():
    """A Hill coefficient is a sensitivity, and the sensitivity is 81^(1/n).

    Every curve crosses half occupancy at the same place. What changes is how
    much you have to move x to get from a tenth to nine tenths -- and that is
    the only thing n means.
    """
    x = np.geomspace(1e-2, 1e2, 600)
    fig, ax = plt.subplots(figsize=(7.6, 4.2))

    for n, c in zip([1, 2, 4, 8], [MUTED, CYAN, TEAL, INK]):
        ax.semilogx(x, hill(x, 1.0, n), color=c, lw=2.2, label=f"n = {n}")
        x10, x90 = (1 / 9) ** (1 / n), 9 ** (1 / n)
        ax.plot([x10, x90], [0.1, 0.9], "o", color=c, ms=4.5)

    ax.axhline(0.1, color=RULE, lw=1.0)
    ax.axhline(0.9, color=RULE, lw=1.0)
    ax.set_xlabel("[X] / K")
    ax.set_ylabel("bound fraction")
    ax.set_ylim(-0.03, 1.03)
    ax.set_title("Same half-point, four different sensitivities", color=INK)
    ax.legend(loc="upper left", fontsize=10)

    rows = "\n".join(f"n = {n}:  {81 ** (1 / n):5.2f}×" for n in (1, 2, 4, 8))
    ax.text(0.985, 0.06, "fold-change in [X],\n10% → 90%\n\n" + rows,
            transform=ax.transAxes, ha="right", va="bottom", fontsize=9.5,
            color=INK, family="monospace",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor=RULE))
    fig.tight_layout()
    fig.savefig(f"{OUT}/s04_hill_family.png")
    plt.close(fig)


def fig_independent_sites():
    """Two independent sites give n = 1. The site count is an upper bound, not a value.

    Exact fractional occupancy from the four-state partition function is
    x/(K_d + x) -- a Hill function of coefficient one, plotted against the n = 2
    curve someone would report if they assumed n counts sites.
    """
    x = np.geomspace(1e-2, 1e2, 600)
    kd = 1.0

    # Four states: empty, site 1, site 2, both. Weights 1, x/Kd, x/Kd, (x/Kd)^2.
    w = x / kd
    Z = 1 + 2 * w + w ** 2
    occupancy = (2 * w + 2 * w ** 2) / (2 * Z)      # mean sites bound / 2

    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.semilogx(x, occupancy, color=TEAL, lw=3.0,
                label="two INDEPENDENT sites, exact")
    ax.semilogx(x, hill(x, kd, 1), color=AMBER, lw=1.6, ls="--",
                label="Hill, n = 1")
    ax.semilogx(x, hill(x, kd, 2), color=RED, lw=1.8, ls=":",
                label="Hill, n = 2 — what 'two sites' would predict")
    ax.set_xlabel("[X] / K$_d$")
    ax.set_ylabel("fractional occupancy")
    ax.set_ylim(-0.03, 1.03)
    # NOT "two sites, no cooperativity, n = 1" -- that is the slide's title, and
    # a figure that repeats its slide's title wastes the only line it has.
    ax.set_title("The square cancels, and the site count disappears with it",
                 color=INK)
    ax.legend(loc="upper left", fontsize=9.5)
    ax.text(0.985, 0.06,
            "Z = 1 + 2w + w²  = (1 + w)²,   w = [X]/K$_d$\n"
            "occupancy = w(1+w)/(1+w)² = w/(1+w)",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10,
            color=INK,
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor=RULE))
    fig.tight_layout()
    fig.savefig(f"{OUT}/s04_independent_sites.png")
    plt.close(fig)


FIGURES = [fig_qssa_regimes, fig_qssa_error, fig_hill_family,
           fig_independent_sites]
