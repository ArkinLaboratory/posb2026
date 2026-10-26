"""Session 21 figures — what a downstream load costs, and what it does not.

Every curve that comes from a model comes out of `posb.retroactivity`, the same
functions the students call. Every point that comes from a measurement is a
MARKER with its source in `sessions/s21-retroactivity/REBUILD.md`, never a line,
so the two kinds of thing never look alike on a slide.

ONE MODEL PER FIGURE, AND THE MODEL IS NAMED ON THE FIGURE. This is the rule
the 26 October rebuild added, because the previous run broke it three times:
it plotted a diluted-model level shift against a protected-model slowdown on
one pair of axes, put diluted-model occupancy on the twin axis of a
protected-model curve, and annotated a protected-model sweep with a claim the
deck asserted for the diluted model. The two models disagree, so a figure that
mixes them cannot be read.

  PROTECTED  complex is shielded from degradation while bound. X_ss = k/gamma
             at every load, so there is NO level cost -- verified to 2e-16.
             The speed cost is (p_tot/X_T)/ln 2 and is flat in K_d, because
             integral R dX = p_tot exactly, whatever the affinity. Mishra 2014
             is this model (p. 1273).
  DILUTED    complex is removed with everything else. X + C is pinned, so both
             costs are real. Both depend on affinity, because the endpoint
             itself moves with K_d.

What this session has to draw:

  * THE DAMAGE. `fig_step_response` -- one module driven with and without a
    load, in the DILUTED model, so both costs are visible on one trace.
  * WHICH COSTS YOU PAY. `fig_both_costs` -- cost against load, both models on
    one axis. The protected model's level cost is identically zero; the
    diluted model's two costs are in a ratio that drifts with load, so the
    tidy 1.45 is a light-load statement and the figure says so.
  * THE THESIS. `fig_affinity` -- PROTECTED model. Sweep the operator's
    affinity four decades and the cost does not move, because the bill is the
    site count and not the binding energy. It falls only once the sites stop
    filling, and the regulation goes with it. This is the surface the hour
    exists for.
  * THE REPAIR. `fig_bandwidth` -- Mishra's four cutoff frequencies, plain
    circuit against buffered. These are CALCULATED values, not measured ones
    (Fig. 4c caption: "Dotted lines correspond to calculated bandwidths"), so
    they are drawn as calculated values and labelled as such.

    An earlier version of this figure plotted them against an inferred
    retroactivity R on our alpha = 1/(1+R) curve. That was CIRCULAR: R was
    defined as 1/alpha - 1 from each ratio, so every point lay on the curve by
    construction and the figure confirmed nothing. The deck told the lecturer
    to point at it as evidence. Removed.

Run:  python tools/build_figures.py s21
"""
import numpy as np

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           RULE, TYPE)
from posb import retroactivity as retro

plt = use()                 # the 20pt content floor, not LEGACY_SCALE
OUT = "figures/build"

# Reference parameters, as in REBUILD.md: X_T = k/gamma = 1000.
K, GAMMA, KD = 10.0, 0.01, 1.0
X_T = K / GAMMA
INV_LN2 = 1.0 / np.log(2.0)      # 1.442695 -- the protected-model coefficient


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def fig_step_response():
    """One module, driven with and without a downstream load. DILUTED model.

    The diluted model is the one where both costs exist, so this is the figure
    that shows them together. In the protected model the two plateaus would
    coincide exactly and only the half-time verticals would move -- that is
    said on the figure, because it is the contrast that makes the hour's hinge
    concrete.

    Time is plotted in UNLOADED LIFETIMES, 1/gamma. The previous run labelled
    the axis "time (1/gamma units)" while plotting the solver's native units,
    so an axis running 0-4 lifetimes read as 0-400 of them and the half-time
    markers read as 69 and 105 lifetimes instead of 0.69 and 1.05.
    """
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    t = np.linspace(0, 400, 900)
    tau = t * GAMMA                       # unloaded lifetimes

    for p_tot, colour, label in [(0.0, TEAL, "no load"),
                                 (300.0, AMBER, "300 sites")]:
        sol = retro.simulate_load(K, GAMMA, KD, p_tot, complex_decays=True)
        ax.plot(tau, sol.sol(t)[0], color=colour, label=label)
        ax.axhline(sol.y[0, -1], color=colour, lw=1.1, ls=":", alpha=0.8)

    th0 = retro.response_half_time(K, GAMMA, KD, 0.0) * GAMMA
    th1 = retro.response_half_time(K, GAMMA, KD, 300.0, complex_decays=True) * GAMMA
    lvl = retro.level_shift(K, GAMMA, KD, 300.0)
    for th, colour in [(th0, TEAL), (th1, AMBER)]:
        ax.axvline(th, color=colour, lw=1.1, ls="--", alpha=0.7)

    # speed cost, on the time axis, low down where both curves have left
    ax.annotate("", xy=(th1, 90), xytext=(th0, 90),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.8))
    ax.text((th0 + th1) / 2, 125, f"{th1/th0:.2f}x slower",
            color=INK, fontsize=TYPE["body"], ha="center")
    # level cost, on the value axis, at the right where both have plateaued
    ax.annotate("", xy=(3.92, (1 - lvl) * X_T), xytext=(3.92, X_T),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.8))
    ax.text(3.84, (1 - lvl / 2) * X_T, f"{lvl*100:.0f}% lower",
            color=INK, fontsize=TYPE["body"], ha="right", va="center")

    # The only clear pocket is between the two plateaus on the right, where
    # the teal curve has flattened and the level arrow has not yet started.
    # The title already says which model this is; the figure only needs the
    # tag, and the one clear band is under the loaded curve on the right.
    ax.text(1.68, 165, "DILUTED model", ha="left", va="center",
            color=MUTED, fontsize=TYPE["caption"])

    ax.set_xlabel("time  (unloaded lifetimes, $1/\\gamma$)")
    ax.set_ylabel("free regulator X")
    ax.set_title("Both costs arrive together — if the complex is diluted")
    ax.legend(loc="lower right", frameon=False)
    ax.set_xlim(0, 4.0); ax.set_ylim(0, 1150)
    _save(fig, "s21_step_response")


def fig_both_costs():
    """Cost per unit load, BOTH MODELS on one axis, each labelled.

    This replaces a figure captioned "one ratio sets both costs", which spliced
    a diluted-model level shift and a protected-model slowdown onto one pair of
    axes and annotated the ratio between them as a constant. It is not a
    constant: within the diluted model it runs 1.441 at p/X_T = 0.002 to 1.709
    at 0.3. The tidy coefficient belongs to the PROTECTED model, where it is
    1/ln 2 exactly.

    Plotted as cost DIVIDED BY p_tot/X_T, on a linear y axis. The first attempt
    plotted the raw costs log-log, where every curve is very nearly a straight
    line of slope 1 and all three lay on top of each other -- the figure
    visually denied the annotation it carried. Dividing out the load is what
    makes the three behaviours distinguishable at all.
    """
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    fracs = np.array([0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3])

    shift = np.array([retro.level_shift(K, GAMMA, KD, f * X_T) for f in fracs])
    slow_d = np.array([retro.slowdown(K, GAMMA, KD, f * X_T,
                                      complex_decays=True) - 1.0
                       for f in fracs])
    slow_p = np.array([retro.slowdown(K, GAMMA, KD, f * X_T,
                                      complex_decays=False) - 1.0
                       for f in fracs])

    ax.semilogx(fracs, slow_d / fracs, "s-", color=AMBER, lw=2.4, ms=9,
                label="speed cost, diluted")
    ax.semilogx(fracs, slow_p / fracs, "^--", color=CYAN, lw=2.4, ms=9,
                label="speed cost, protected")
    ax.semilogx(fracs, shift / fracs, "o-", color=TEAL, lw=2.4, ms=9,
                label="level cost, diluted")
    ax.axhline(INV_LN2, color=MUTED, lw=1.3, ls=":")
    ax.text(0.0022, INV_LN2 + 0.045, "$1/\\ln 2 = 1.443$",
            color=MUTED, fontsize=TYPE["caption"], va="bottom")

    # The protected level cost is exactly zero -- draw it, because "zero" is
    # the single most surprising number in this session and a reader should
    # see the line sitting on the axis rather than infer it from a legend.
    ax.axhline(0.0, color=CYAN, lw=2.4, ls="-", alpha=0.55)
    ax.text(0.26, 0.055, "level cost, protected  $=$  0 exactly",
            color=CYAN, fontsize=TYPE["caption"], ha="right", va="bottom")

    ax.set_xlabel("sites per molecule,  $p_{tot}/X_T$")
    ax.set_ylabel("cost $\\div$  ($p_{tot}/X_T$)")
    ax.set_title("Which costs you pay depends on the complex", pad=14)
    ax.set_ylim(-0.08, 2.05)
    # Legend into the empty band between the level curve (1.0) and zero,
    # which is the only region no curve and no label occupies.
    ax.legend(loc="center left", bbox_to_anchor=(0.015, 0.33),
              frameon=False, fontsize=TYPE["caption"])
    ax.annotate("the diluted ratio\ndrifts with load",
                xy=(0.3, slow_d[-1] / fracs[-1]), xytext=(0.055, 1.90),
                color=INK, fontsize=TYPE["caption"], ha="left", va="top",
                linespacing=1.25,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    _save(fig, "s21_both_costs")


def fig_affinity():
    """THE SESSION'S THESIS. PROTECTED model.

    Slowdown against the operator's dissociation constant at a fixed number of
    sites, with site occupancy on a twin axis. The cost is flat across four
    decades because of a conservation identity, not because of a coincidence:

        integral of R dX from 0 to infinity  =  C(inf) - C(0)  =  p_tot

    exactly, for every K_d. The extra material the loaded system must make on
    its way up is the SITE COUNT; the affinity decides only when during the
    approach it is paid. So a weaker operator cannot buy the speed back.

    Past K_d ~ X_T the sites no longer fill during the approach, so the bill
    shrinks -- and so does the occupancy, which means the downstream module is
    no longer regulated. That is a disconnection, not a cure.

    Both axes are the protected model. The previous run drew diluted-model
    occupancy on the twin axis of this protected-model curve; at K_d = 1e3 the
    two occupancies are 0.500 and 0.382.
    """
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    kds = np.logspace(-2, 5, 22)
    p_tot = X_T                       # a heavy load, so the effect is visible
    slow = np.array([retro.slowdown(K, GAMMA, kd, p_tot, complex_decays=False)
                     for kd in kds])
    # Protected model: X_ss = k/gamma at every load, so occupancy is exact.
    occ = X_T / (kds + X_T)

    ax.semilogx(kds, slow, "o-", color=TEAL)
    ax.set_xlabel("operator dissociation constant  $K_d$")
    ax.set_ylabel("response time, relative to no load", color=TEAL)
    ax.tick_params(axis="y", labelcolor=TEAL)
    ax.set_ylim(0.9, 3.05)   # headroom, so the right-hand note clears the plateau

    ax2 = ax.twinx()
    ax2.semilogx(kds, occ, color=AMBER, lw=2.2, ls="--")
    ax2.set_ylabel("fraction of sites occupied", color=AMBER)
    ax2.tick_params(axis="y", labelcolor=AMBER)
    ax2.set_ylim(0, 1.05)

    ax.axvline(X_T, color=MUTED, lw=1.4, ls=":")
    # rotated: a horizontal label here collides with whichever curve passes
    ax.text(X_T * 1.3, 2.12, "$K_d = X_T$", color=MUTED, rotation=90,
            fontsize=TYPE["body"], ha="left", va="center")
    # left half, below the plateau: empty
    # Lower left: below the flat slowdown plateau and below the occupancy
    # curve, which both sit near the top of the axes on this side.
    ax.text(0.03, 0.28,
            "$\\int R\\,dX = p_{tot}$, whatever $K_d$ is.\n"
            "the bill is the site count;\n"
            "affinity sets only the schedule.",
            transform=ax.transAxes, color=INK, fontsize=TYPE["body"],
            va="center", linespacing=1.25)
    # above the plateau, which is what the raised ylim is for
    # Top right: clear only past K_d ~ 300, where BOTH curves have fallen.
    ax.text(0.985, 0.985, "sites empty past here:\nno load, no regulation",
            transform=ax.transAxes, ha="right", va="top",
            color=INK, fontsize=TYPE["body"], linespacing=1.25)
    ax.text(0.03, 0.035, "PROTECTED model, both axes",
            transform=ax.transAxes, ha="left", va="bottom",
            color=MUTED, fontsize=TYPE["caption"])
    ax.set_title("A weaker operator does not buy you anything", pad=14)
    _save(fig, "s21_affinity")


# Mishra 2014, Fig. 4c. These are CALCULATED bandwidths, not measured ones --
# the caption says so outright: "Dotted lines correspond to calculated
# bandwidths". Fig. 4b is simulation from a fitted parameter set. The
# MEASUREMENT is the amplitude response; these four are read off a model of it,
# so they are not drawn as measurement markers.
#
# The caption states the two unbuffered values in the reverse order with
# respect to its own plot; REBUILD.md section 3 records the panel read at
# 200 dpi, which is where this assignment comes from.
MISHRA_BANDWIDTH = {         # min^-1, calculated
    "unbuffered, no load": 0.0175,
    "unbuffered, 2x load": 0.0140,
    "buffered, no load":   0.0142,
    "buffered, 2x load":   0.0143,
}


def fig_bandwidth():
    """Mishra's four cutoff frequencies: plain circuit against buffered.

    No derived curve and no retroactivity axis. The previous version put these
    on our alpha = 1/(1+R) curve with R inferred from each ratio as
    1/alpha - 1, so the points lay on the curve identically -- any four numbers
    would have -- and the deck presented that as the model being confirmed.

    What the data support is a comparison: the plain circuit loses a fifth of
    its bandwidth to the load, the buffered one loses nothing measurable.
    """
    fig, ax = plt.subplots(figsize=(8.8, 5.2))

    groups = [
        ("plain circuit", 0.0,
         MISHRA_BANDWIDTH["unbuffered, no load"],
         MISHRA_BANDWIDTH["unbuffered, 2x load"], RED),
        ("with load driver", 1.0,
         MISHRA_BANDWIDTH["buffered, no load"],
         MISHRA_BANDWIDTH["buffered, 2x load"], GREEN),
    ]

    for name, x, no_load, loaded, colour in groups:
        ax.plot([x - 0.13], [no_load], "o", color=colour, ms=15, zorder=5)
        ax.plot([x + 0.13], [loaded], "s", color=colour, ms=14, zorder=5)
        ax.annotate("", xy=(x + 0.13, loaded), xytext=(x - 0.13, no_load),
                    arrowprops=dict(arrowstyle="->", color=colour, lw=2.4))
        drop = 1.0 - loaded / no_load
        # Verdict sits just under the group's lower marker, inside the axes.
        ax.text(x, max(no_load, loaded) + 0.0007,
                ("$-$%.0f%% of what it had" % (drop * 100)) if drop > 0.01
                else "no measurable change",
                color=colour, fontsize=TYPE["body"], ha="center", va="bottom")
        # Values beside their own markers, never in a shared strip.
        ax.text(x - 0.20, no_load, f"{no_load:.4f}", color=MUTED,
                fontsize=TYPE["caption"], ha="right", va="center")
        ax.text(x + 0.20, loaded, f"{loaded:.4f}", color=MUTED,
                fontsize=TYPE["caption"], ha="left", va="center")

    ax.set_xticks([0.0, 1.0])
    ax.set_xticklabels(["plain circuit", "with load driver"])
    ax.set_xlim(-0.62, 1.62)
    ax.set_ylim(0.0120, 0.0196)       # headroom both ends: verdicts above, source below
    ax.set_ylabel("cutoff frequency  (min$^{-1}$)")
    ax.set_title("What the fast stage buys", pad=14)

    # Key in the one corner no marker reaches.
    ax.text(0.985, 0.955, "circles: no load\nsquares: 2$\\times$ load",
            transform=ax.transAxes, ha="right", va="top",
            color=INK, fontsize=TYPE["caption"], linespacing=1.3)
    ax.text(0.015, 0.025,
            "calculated bandwidths, Mishra 2014 Fig. 4c\n"
            "(the measurement is the amplitude response)",
            transform=ax.transAxes, ha="left", va="bottom",
            color=MUTED, fontsize=TYPE["caption"], linespacing=1.3)
    _save(fig, "s21_bandwidth")


FIGURES = [fig_step_response, fig_both_costs, fig_affinity, fig_bandwidth]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
