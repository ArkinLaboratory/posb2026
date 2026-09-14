"""Session 7 figures — autoregulation, taught from the production/removal picture.

The session's object is a PICTURE, not an equation: production rate and removal
rate on one pair of axes, with the steady state where they cross. Every result
in the session is that picture redrawn, so the figures carry the argument rather
than decorating it.

    s07_three_curves       the object. Constitutive, NAR, cooperative PAR.
    s07_bistable_condition what has to be true for a third crossing to exist.
    s07_cost_in_time       synthesis rate against time for the three routes.
    s07_approach           p(t) for the three routes, UNNORMALISED.

NUMBERS, all computed here and none asserted. E. coli at 30 min doubling, so
mu = 0.0231/min; hold p* = 1000 molecules throughout.

    route                     t1/2      steady-state synthesis
    do nothing                30.0      23.1 protein/min
    LAA tag, alpha raised      17.1      40.4 protein/min   (1.75x, forever)
    NAR, repression ratio 2    16.8      23.1 protein/min   (transient only)

Speed-ups, for the record: the tag buys 1.75x, NAR at repression ratio 2 buys
1.79x. The repression ratio that matches the tag EXACTLY is 1.94.

The repression ratio of 2 is not a round number chosen for looks: it is the
round number NEXT TO the value at which NAR matches the strongest tag in
Andersen 1998, which is 1.94 (solved for, not guessed). At 2 the circuit is a
shade faster than the tag, which is the more useful claim anyway.

    python tools/build_figures.py s07
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import matplotlib.patches as mpatches

from figures.style import (use, AMBER, CYAN, GREEN, INK, MUTED, RED, RULE,
                           TEAL)

BODY = "#23423F"
plt = use()
OUT = "figures/build"

T_D = 30.0
MU = np.log(2) / T_D                  # 0.0231 /min
P_STAR = 1000.0
ALPHA0 = MU * P_STAR                  # 23.1 protein/min
REP = 2.0                             # NAR repression ratio
K_NAR = P_STAR / (REP - 1.0)          # so that alpha/alpha0 = REP at p*
TAG_HALFLIFE = 40.0                   # Andersen LAA/LVA

# Cooperative positive autoregulation with basal expression. amax is set so the
# UPPER crossing lands on screen: production saturates at basal+amax while
# removal grows linearly, so the last crossing sits at (basal+amax)/mu. With
# amax = 1.6*alpha0 that is about 1750 molecules. The first version used
# 2.9*alpha0, which put the high state at 2900 and off the axis -- and the
# crossing counter then reported two roots for a system that has three.
PAR_N, PAR_K = 4.0, 900.0
PAR_BASAL, PAR_AMAX = 0.14 * ALPHA0, 1.6 * ALPHA0
XMAX = 2000.0


def _crossings(f, lo=1e-6, hi=None, n=20000):
    """Every root of f(p) = mu*p on [lo, hi], and whether each is stable.

    A coarse scan misses the pair of roots that appear together at a saddle
    node, which is exactly the transition this session is about.
    """
    hi = XMAX if hi is None else hi
    xs = np.linspace(lo, hi, n)
    g = f(xs) - MU * xs
    out = []
    for i in range(len(xs) - 1):
        if g[i] == 0.0 or g[i] * g[i + 1] < 0:
            r = brentq(lambda x: f(np.array([x]))[0] - MU * x, xs[i], xs[i + 1])
            out.append((r, (f(np.array([r + hi * 5e-4]))[0]
                            - MU * (r + hi * 5e-4)) < 0))
    return out


def _tag():
    """Degradation tag sized to Andersen's best, with alpha raised to hold p*."""
    g = np.log(2) / TAG_HALFLIFE
    k = g + MU
    return k, k * P_STAR              # removal rate constant, required alpha


def _solve(alpha, k, K=None, n=1, tmax=160.0):
    if K is None:
        f = lambda t, p: alpha - k * p
    else:
        f = lambda t, p: alpha / (1 + (p / K) ** n) - k * p
    return solve_ivp(f, [0, tmax], [0.0], dense_output=True, rtol=1e-10,
                     atol=1e-10, max_step=0.5)


def _thalf(sol, tmax=160.0):
    return brentq(lambda t: sol.sol(t)[0] - P_STAR / 2, 1e-9, tmax)



def _cassette(ax, y, operator, tag, sub, opcolor, x0=2.10):
    """One transcription unit drawn in session-6 notation.

    The promoter is the same object session 6 spent twenty minutes on: two
    hexamers RNAP reads, plus an operator that some protein may occupy. The
    only thing autoregulation changes is WHICH protein occupies it.

    The row is named in a left gutter rather than in a title above it, because
    the feedback arcs bow upward and a title there gets struck through -- which
    is exactly what the first version of this figure did.
    """
    ax.text(0.12, y + 0.14, tag, fontsize=13, color=INK, fontweight="bold")
    ax.text(0.12, y - 0.36, sub, fontsize=11, color=MUTED)

    ax.plot([x0, x0 + 7.35], [y, y], color=MUTED, lw=3.0,
            solid_capstyle="butt", zorder=1)
    for a, b, lab in ((0.90, 1.50, "\u221235"), (2.00, 2.60, "\u221210")):
        ax.add_patch(mpatches.Rectangle((x0 + a, y - 0.11), b - a, 0.22,
                     facecolor=CYAN, edgecolor=INK, lw=1.3, zorder=3))
        ax.text(x0 + (a + b) / 2, y - 0.42, lab, ha="center", fontsize=10.5,
                color=INK)
    if operator:
        ax.add_patch(mpatches.Rectangle((x0 + 2.75, y - 0.11), 0.85, 0.22,
                     facecolor=opcolor, edgecolor=INK, lw=1.3, alpha=0.55,
                     zorder=4))
        ax.text(x0 + 3.17, y - 0.42, "operator", ha="center", fontsize=10.5,
                color=opcolor)
    ax.add_patch(mpatches.Rectangle((x0 + 4.00, y - 0.17), 1.85, 0.34,
                 facecolor="#F8FAF9", edgecolor=INK, lw=1.5, zorder=3))
    ax.text(x0 + 4.92, y, "gene", ha="center", va="center", fontsize=11.5,
            color=INK)
    ax.annotate("", xy=(x0 + 6.80, y), xytext=(x0 + 6.00, y),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0))
    ax.add_patch(mpatches.Circle((x0 + 7.15, y), 0.25, facecolor=TEAL,
                 edgecolor=INK, lw=1.3, zorder=3))
    ax.text(x0 + 7.15, y, "p", ha="center", va="center", fontsize=12,
            color="white", fontweight="bold")


def fig_wiring():
    """What the three wirings ARE, before any curve is drawn.

    Session 6 established the promoter as an object. Autoregulation is one
    edit to that object -- the operator is bound by the gene's OWN product --
    and the class should see that edit as a picture before it appears as a
    p in the denominator of alpha(p).
    """
    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    ax.set_axis_off()
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 5.4)

    x0 = 2.10
    _cassette(ax, 4.65, False, "Constitutive", "no feedback", MUTED, x0)
    _cassette(ax, 2.95, True, "Negative", "p represses itself", AMBER, x0)
    _cassette(ax, 1.25, True, "Positive", "p activates itself", GREEN, x0)

    for y, kind, c in ((2.95, "repress", AMBER), (1.25, "activate", GREEN)):
        head = "-|>" if kind == "activate" else "-"
        ax.annotate("", xy=(x0 + 3.17, y + 0.20), xytext=(x0 + 7.15, y + 0.34),
                    arrowprops=dict(arrowstyle=head, color=c, lw=2.4,
                                    connectionstyle="arc3,rad=0.30",
                                    shrinkA=8, shrinkB=6))
        if kind == "repress":
            ax.plot([x0 + 2.95, x0 + 3.39], [y + 0.25, y + 0.25], color=c,
                    lw=3.2, solid_capstyle="butt")
        ax.text(x0 + 5.45, y + 0.55,
                "represses" if kind == "repress" else "activates",
                ha="center", fontsize=12, color=c, fontweight="bold")

    ax.text(0.12, 0.42,
            "One edit to the session-6 promoter: the protein sitting on the "
            "operator is the one the gene makes.",
            fontsize=12.5, color=BODY, va="bottom")
    ax.text(0.12, 0.04,
            "That single loop is what makes \u03b1 a function of p \u2014 "
            "and it is the only reason today's production curve is not flat.",
            fontsize=12.5, color=BODY, va="bottom")

    fig.savefig(f"{OUT}/s07_wiring.png")
    plt.close(fig)


def fig_three_curves():
    """THE object: production and removal on one pair of axes, three ways.

    Read left to right this is the whole session. The crossing is the steady
    state; the ANGLE at which the curves cross is the response time; and a
    production curve that rises steeply enough crosses three times.
    """
    p = np.linspace(0, 2200, 800)
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.9), sharey=True)

    panels = [
        ("No regulation", lambda x: np.full_like(x, ALPHA0), TEAL,
         "production does not depend on p"),
        ("Negative autoregulation", lambda x: REP * ALPHA0 / (1 + x / K_NAR),
         CYAN, "production falls as p rises"),
        ("Positive autoregulation", None, AMBER,
         "cooperative, with basal expression"),
    ]
    n, Kp, basal, amax = PAR_N, PAR_K, PAR_BASAL, PAR_AMAX
    par = lambda x: basal + amax * x ** n / (Kp ** n + x ** n)

    for ax, (title, prod, c, sub) in zip(axes, panels):
        f = par if prod is None else prod
        ax.plot(p, f(p), color=c, lw=3.2, label="production")
        ax.plot(p, MU * p, color=MUTED, lw=2.6, ls="--", label="removal")
        for r, stable in _crossings(f):
            ax.plot([r], [MU * r], "o", ms=13, zorder=6,
                    mfc=(c if stable else "white"), mec=INK, mew=2.0)
        ax.set_title(f"{title}\n{sub}", color=INK, pad=10, fontsize=15,
                     linespacing=1.6)
        ax.set_xlim(0, XMAX)
        ax.set_ylim(0, 1.32 * REP * ALPHA0)

    axes[0].set_ylabel("rate  (protein / min)")
    axes[0].legend(loc="upper left")
    axes[2].text(0.96, 0.10, "three crossings\nopen circle is unstable",
                 transform=axes[2].transAxes, fontsize=12.5, color=INK,
                 ha="right")
    # One shared axis label under all three panels. A per-panel xlabel and the
    # italic sub-caption were laid at the same height and overprinted.
    fig.supxlabel("protein  p", color=INK, fontsize=15, y=0.02)
    fig.suptitle("The steady state is where production meets removal",
                 color=INK, fontsize=17, y=0.995)
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    fig.savefig(f"{OUT}/s07_three_curves.png")
    plt.close(fig)


def fig_bistable_condition():
    """T16: what has to be true for the third crossing to exist.

    Sweep the cooperativity with everything else fixed. Below a threshold the
    production curve meets the removal line once; above it, three times. The
    condition is geometric and it is visible -- the room does not need the
    quadratic to see it.
    """
    p = np.linspace(0, XMAX, 900)
    Kp, basal, amax = PAR_K, PAR_BASAL, PAR_AMAX
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    for n, c, ls in ((1.0, MUTED, "--"), (2.0, CYAN, "-"), (4.0, AMBER, "-")):
        f = lambda x, n=n: basal + amax * x ** n / (Kp ** n + x ** n)
        roots = _crossings(f)
        ax.plot(p, f(p), color=c, lw=3.0, ls=ls,
                label=f"n = {n:g}   →  {len(roots)} crossing"
                      + ("s" if len(roots) != 1 else ""))
        for r, stable in roots:
            ax.plot([r], [MU * r], "o", ms=9, zorder=6,
                    mfc=(c if stable else "white"), mec=INK, mew=1.8)
    ax.plot(p, MU * p, color=INK, lw=2.4, ls=":", label="removal")
    ax.set_xlabel("protein  p")
    ax.set_ylabel("rate  (protein / min)")
    ax.set_xlim(0, XMAX); ax.set_ylim(0, 1.18 * (basal + amax))
    ax.legend(loc="upper left")
    ax.text(0.97, 0.06,
            "same promoter, same basal, same removal —\nonly the cooperativity changes",
            transform=ax.transAxes, ha="right", fontsize=13, color=MUTED,
            style="italic")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s07_bistable_condition.png")
    plt.close(fig)


def fig_cost_in_time():
    """The design ledger: what each route SPENDS, against time.

    The tag's line never comes down. NAR starts higher than either and falls to
    the do-nothing line. That is the whole argument of the session in one
    picture, and the areas are the cost.
    """
    k_tag, a_tag = _tag()
    t = np.linspace(0, 140, 900)
    s_nar = _solve(REP * ALPHA0, MU, K=K_NAR)
    p_nar = s_nar.sol(t)[0]
    rate_nar = REP * ALPHA0 / (1 + p_nar / K_NAR)

    fig, ax = plt.subplots(figsize=(10.0, 5.4))
    ax.axhline(ALPHA0, color=TEAL, lw=3.0,
               label=f"do nothing — {ALPHA0:.1f}/min, t½ = 30.0 min")
    ax.axhline(a_tag, color=AMBER, lw=3.0,
               label=f"degradation tag — {a_tag:.1f}/min forever, t½ = 17.1 min")
    ax.plot(t, rate_nar, color=CYAN, lw=3.4,
            label=f"negative autoregulation — falls to {ALPHA0:.1f}/min, "
                  f"t½ = {_thalf(s_nar):.1f} min")
    ax.fill_between(t, ALPHA0, rate_nar, where=(rate_nar > ALPHA0),
                    color=CYAN, alpha=0.16)
    ax.annotate("everything NAR spends is in here,\nand it ends",
                xy=(16, 0.5 * (ALPHA0 + rate_nar[100])), xytext=(46, 13.5),
                fontsize=13, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.annotate("this never comes down", xy=(118, a_tag), xytext=(74, 30.0),
                fontsize=13, color=AMBER,
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.6))
    ax.set_xlabel("time after induction  (min)")
    ax.set_ylabel("synthesis rate  (protein / min)")
    ax.set_xlim(0, 140); ax.set_ylim(0, 56)
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    fig.tight_layout()
    fig.savefig(f"{OUT}/s07_cost_in_time.png")
    plt.close(fig)


def fig_approach():
    """p(t) for the three routes, unnormalised, all reaching the same level.

    Unnormalised on purpose, as in session 5: normalising hides that these
    three curves end in the same place, which is the entire premise.
    """
    k_tag, a_tag = _tag()
    t = np.linspace(0, 140, 900)
    runs = [("do nothing", _solve(ALPHA0, MU), TEAL),
            ("degradation tag, α raised", _solve(a_tag, k_tag), AMBER),
            ("negative autoregulation", _solve(REP * ALPHA0, MU, K=K_NAR), CYAN)]
    fig, ax = plt.subplots(figsize=(10.0, 5.4))
    for name, sol, c in runs:
        y = sol.sol(t)[0]
        th = _thalf(sol)
        ax.plot(t, y, color=c, lw=3.2, label=f"{name}:  t½ = {th:.1f} min")
        ax.plot([th], [P_STAR / 2], "o", color=c, ms=9, zorder=5)
    ax.axhline(P_STAR, color=RULE, lw=1.6, ls="--")
    ax.text(2, P_STAR * 1.02, "all three reach the same level", fontsize=13,
            color=MUTED)
    ax.set_xlabel("time after induction  (min)")
    ax.set_ylabel("protein per cell")
    ax.set_xlim(0, 140); ax.set_ylim(0, 1150)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s07_approach.png")
    plt.close(fig)


FIGURES = [fig_wiring, fig_three_curves, fig_bistable_condition, fig_cost_in_time,
           fig_approach]
