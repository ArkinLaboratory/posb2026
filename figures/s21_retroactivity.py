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
             The speed cost APPROACHES (p_tot/X_T)/ln 2 as the sites
             saturate and is NEARLY flat in K_d -- 3.34% over four decades at
             p_tot = X_T, non-monotonically, peaking near K_d = X_T/60. The
             reason it is not exactly flat: TWO effects compete. The system
             only travels 0 -> X_T, so it pays p_tot * X_T/(K_d + X_T) and
             not all of p_tot -- that falls with K_d. But a weaker operator
             also parks its molecules LATER in the approach, where each one
             costs more delay because dX/dt is already small -- that rises
             with K_d. Timing wins below K_d ~ X_T/60 and the shrinking
             bill wins above it, which is the peak. Verified by quadrature:
             1 + (integral of R/(k - gamma X) from 0 to X_T/2)/(ln2/gamma)
             reproduces slowdown() to four decimals at every K_d tried.
             Mishra 2014 is this model (p. 1273).
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
    filling, and the regulation goes with it. This is the figure the hour
    exists for.
  * THE REPAIR. `fig_bandwidth` -- Mishra's four cutoff frequencies, plain
    circuit against buffered. These are CALCULATED values, not measured ones
    (Fig. 4c caption: "Dotted lines correspond to calculated bandwidths"), so
    they are drawn as calculated values and labeled as such.

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

    Time is plotted in UNLOADED LIFETIMES, 1/gamma. The previous run labeled
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
    ax.text(0.04, 0.965, "DILUTED model", transform=ax.transAxes,
            ha="left", va="top", color=MUTED, fontsize=TYPE["caption"])

    ax.set_xlabel("time  (unloaded lifetimes, $1/\\gamma$)")
    ax.set_ylabel("free regulator X")
    ax.set_title("Both costs arrive together — if the complex is diluted")
    ax.legend(loc="lower right", frameon=False)
    ax.set_xlim(0, 4.0); ax.set_ylim(0, 1150)
    _save(fig, "s21_step_response")


def fig_both_costs():
    """Cost per unit load, BOTH MODELS on one axis, each labeled.

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
    makes the three behaviors distinguishable at all.
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
                xy=(0.3, slow_d[-1] / fracs[-1]), xytext=(0.030, 1.99),
                color=INK, fontsize=TYPE["caption"], ha="left", va="top",
                linespacing=1.25,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    _save(fig, "s21_both_costs")


def fig_conservation():
    """Where the bill IS: C(X) is the running total, and every curve ends level.

    Adam, 1 November, on the affinity slides: "it is not clear where the 'bill'
    (p_tot) IS". It was nowhere — the conservation result was asserted in a
    row, confirmed by a sweep of a DERIVED quantity, and the thing actually
    being conserved was never drawn.

    C(X) is the integral of R up to X, so the height of each curve is the bill
    paid so far. Plotted against log X, every affinity gives the same sigmoid
    displaced sideways and every one levels off at p_tot. That is the whole
    conservation argument as a picture: K_d slides the curve left or right, it
    does not raise or lower where it ends.

    The vertical at X_T is the second half of the hour's argument and it is the
    same picture. The system stops climbing there, so what it has actually paid
    is where its curve crosses that line: 299.7, 295.3, 272.7 and 150.0 at
    K_d = 1, 16, 100 and 1000. The first three are indistinguishable from the
    full bill and the fourth is half of it — which is why the cost is flat for
    four decades and then falls away, and why past K_d ~ X_T the sites are
    empty and the regulation has gone with them.

    These four numbers are p_tot*X_T/(K_d + X_T), which is the partial integral
    section 4(g) of the home guide asks for.
    """
    fig, ax = plt.subplots(figsize=(10.0, 5.0))
    p_tot = 300.0
    xs = np.logspace(-1, 5, 400)

    # Only the two SEPARABLE crossings get a number on the figure. At K_d = 1
    # and 16 the curves cross X_T at 299.7 and 295.3, four units apart on a
    # 360-unit axis, and two labels there land on top of each other.
    for kd, colour, style, tag in ((1.0, TEAL, "-", None),
                                   (16.0, CYAN, "-", None),
                                   (100.0, AMBER, "-", "273"),
                                   (1000.0, RED, "--", "150")):
        ax.semilogx(xs, p_tot * xs / (kd + xs), style, color=colour, lw=2.6,
                    label="$K_d = %g$" % kd)
        paid = p_tot * X_T / (kd + X_T)
        ax.plot([X_T], [paid], "o", color=colour, ms=11, zorder=6)
        if tag:
            ax.text(X_T * 1.5, paid, tag, color=colour,
                    fontsize=TYPE["body"], ha="left", va="center")

    ax.axhline(p_tot, color=MUTED, lw=1.6, ls=":")
    ax.axvline(X_T, color=INK, lw=1.6, ls=":")

    ax.text(0.13, 308, "$p_{tot} = 300$ — the whole bill", color=MUTED,
            fontsize=TYPE["body"], va="bottom", ha="left")
    ax.text(X_T * 1.5, 340, "$X_T$ — the climb stops here", color=INK,
            fontsize=TYPE["body"], va="center", ha="left")

    ax.set_xlabel("free regulator  $X$")
    ax.set_ylabel("$C(X)$ — molecules parked")
    ax.set_ylim(0, 362)
    ax.set_xlim(0.1, 1e5)
    ax.set_title("Affinity slides the curve sideways; the ceiling does not move",
                 pad=14)
    ax.legend(loc="lower right", frameon=False, fontsize=TYPE["caption"],
              bbox_to_anchor=(1.0, 0.11))
    # Bottom right is the one corner no curve and no label reaches: the
    # legend stops at 0.11 and every curve is near the ceiling out there.
    ax.text(0.985, 0.02, "PROTECTED model", transform=ax.transAxes,
            ha="right", va="bottom", color=MUTED, fontsize=TYPE["caption"])
    _save(fig, "s21_conservation")


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
            "$\\int_0^\\infty R\\,dX = p_{tot}$, whatever $K_d$ is.\n"
            "the bill is the site count;\n"
            "affinity sets only the schedule.",
            transform=ax.transAxes, color=INK, fontsize=TYPE["body"],
            va="center", linespacing=1.25)
    # above the plateau, which is what the raised ylim is for
    # NO "sites empty past here" callout. 31 October: there is no band in
    # this figure wide enough to hold two lines of body text -- the amber
    # occupancy curve owns the top left, the teal curve sweeps the middle,
    # and a right-aligned label reaches back across both. Every placement
    # tried collided with a curve, the K_d = X_T rule or the right tick
    # labels. The vertical rule marks where it happens, the right-hand axis
    # shows the sites emptying, and the slide foot says it in words.
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
        # shrinkA/B must clear the 7pt marker radius or the head is drawn
        # inside the opaque square and only its barbs show.
        ax.annotate("", xy=(x + 0.13, loaded), xytext=(x - 0.13, no_load),
                    arrowprops=dict(arrowstyle="->", color=colour, lw=2.4,
                                    shrinkA=11, shrinkB=11))
        drop = 1.0 - loaded / no_load
        # Verdict sits above the group's higher marker, inside the axes.
        ax.text(x, max(no_load, loaded) + 0.0007,
                ("$-$%.0f%% of what it had" % (drop * 100)) if drop > 0.01
                else "unchanged to under 1%",
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
    # SHORT LINES, HARD AGAINST THE FLOOR. Found by rendering, twice: at this
    # figure size a 40-character caption line spans most of the axes, so a
    # three-line note anywhere inside ran through the markers and their value
    # labels whichever corner it was anchored to. The lowest marker sits at 26%
    # of the axes height, so two short lines resting on the floor clear it. The
    # deck's foot carries the full provenance; this exists so that the
    # attribution survives a screenshot of the slide.
    ax.text(0.015, 0.025,
            "our plot of the values\n"
            "calculated in Mishra 2014 Fig. 4c",
            transform=ax.transAxes, ha="left", va="bottom",
            color=MUTED, fontsize=TYPE["caption"], linespacing=1.3)
    _save(fig, "s21_bandwidth")


def fig_object():
    """The arrow as drawn, and the arrow as it actually is — on one picture.

    Two strips, deliberately sharing their geometry: module A sits directly
    above "your circuit" and module B directly above the promoter, so the lower
    strip reads as the upper one with the truth filled in rather than as a
    second, unrelated diagram. That is the whole of segment 2 — the diagram
    says SIGNAL and the molecule says BINDING SITE — and before this existed
    the slide asserted both in prose and showed neither.

    Everything segment 3 derives is labeled here and nothing else is: the
    production rate, the removal rate, the free pool, the sites, the complex,
    and the one equilibrium between them. The two quantities every number in
    the session is built from sit on the figure — p_tot, the site count, and
    X_T = k/gamma, the abundance the factor would have with no load. Step 3 of
    the derivation turns on those being different numbers.

    No model is drawn. There is no curve and no axis; the models arrive in
    segment 4 and they disagree about this picture in exactly one place, which
    is whether the gamma arrow also reaches the parked molecules.
    """
    from matplotlib.patches import Ellipse, FancyArrowPatch, Rectangle

    fig, ax = plt.subplots(figsize=(10.4, 5.6))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0.30, 6.95)
    ax.axis("off")

    # The axes are not equal-aspect, so a Circle in data coordinates comes
    # out as a flattened disc. Stretch the y radius by the ratio of the two
    # scales and the molecules are round.
    _YX = ((6.95 - 0.30) / 5.6) / (10.5 / 10.4)

    def xmol(x, y, r=0.19):
        ax.add_patch(Ellipse((x, y), 2 * r, 2 * r * _YX, facecolor=TEAL,
                             edgecolor="none", zorder=4))

    def arrow(x0, y0, x1, y1, style="->", colour=INK, lw=2.4):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style,
                                     color=colour, lw=lw, mutation_scale=22,
                                     zorder=3))

    def box(x0, y0, w, h, label, edge=MUTED):
        ax.add_patch(Rectangle((x0, y0), w, h, facecolor="none",
                               edgecolor=edge, lw=2.0, zorder=2))
        ax.text(x0 + w / 2, y0 + h / 2, label, ha="center", va="center",
                color=INK, fontsize=TYPE["body"], linespacing=1.2)

    AX, BX, BW = 1.05, 6.60, 2.05          # shared by both strips

    # ---------------- what you draw -----------------------------------------
    ax.text(0.05, 6.72, "what you draw", ha="left", va="center", color=MUTED,
            fontsize=TYPE["caption"])
    box(AX, 5.72, BW, 0.84, "module A")
    box(BX, 5.72, BW, 0.84, "module B")
    arrow(AX + BW + 0.12, 6.14, BX - 0.12, 6.14)
    ax.text((AX + BW + BX) / 2, 6.30, "signal", ha="center", va="bottom",
            color=INK, fontsize=TYPE["body"])
    ax.text(10.45, 6.14, "costs nothing", ha="right", va="center",
            color=MUTED, fontsize=TYPE["caption"])

    ax.plot([0.05, 10.45], [5.35, 5.35], color=RULE, lw=1.4, zorder=1)

    # ---------------- what is there -----------------------------------------
    ax.text(0.05, 5.08, "what is there", ha="left", va="center", color=MUTED,
            fontsize=TYPE["caption"])

    box(AX, 3.28, BW, 0.92, "your\ncircuit")
    arrow(AX + BW + 0.10, 3.74, 3.60, 3.74)
    ax.text((AX + BW + 3.60) / 2, 3.94, "$k$", ha="center", va="bottom",
            color=INK, fontsize=TYPE["emphasis"])

    for x, y in [(4.05, 4.28), (4.68, 3.96), (4.14, 3.46), (4.80, 3.20),
                 (4.52, 4.58)]:
        xmol(x, y)
    ax.text(4.45, 2.76, "free $X$", ha="center", va="top", color=TEAL,
            fontsize=TYPE["body"])

    arrow(3.92, 2.98, 3.38, 2.44)
    ax.text(3.64, 2.92, r"$\gamma$", ha="right", va="bottom", color=INK,
            fontsize=TYPE["emphasis"])

    arrow(5.35, 3.74, 6.45, 3.74, style="<->")
    ax.text(5.90, 3.94, "$K_d$", ha="center", va="bottom", color=INK,
            fontsize=TYPE["emphasis"])

    ax.add_patch(Rectangle((6.62, 3.28), 3.70, 0.17, facecolor=MUTED,
                           edgecolor="none", zorder=2))
    for i, full in enumerate([True, True, False, True, True, False]):
        sx = 6.80 + i * 0.59
        ax.add_patch(Rectangle((sx, 3.16), 0.41, 0.42, facecolor="white",
                               edgecolor=AMBER, lw=2.2, zorder=3))
        if full:
            xmol(sx + 0.205, 3.86)

    ax.text(8.45, 2.94, "$p_{tot}$ operator sites", ha="center", va="top",
            color=AMBER, fontsize=TYPE["body"])
    ax.text(8.45, 4.26, "$C$ — bound, doing nothing", ha="center",
            va="bottom", color=TEAL, fontsize=TYPE["body"])

    ax.text(0.05, 1.42,
            "$p_{tot}$ = how many sites\n"
            r"$X_T = k/\gamma$ = what $X$ would reach with no sites at all",
            ha="left", va="center", color=INK, fontsize=TYPE["body"],
            linespacing=1.35)
    ax.text(10.45, 0.52, "and module B never asked for this",
            ha="right", va="bottom", color=MUTED, fontsize=TYPE["caption"],
            style="italic")

    ax.set_title(r"$X + p \; \rightleftharpoons \; C$", pad=8,
                 fontsize=TYPE["title"])
    _save(fig, "s21_object")


# Mishra 2014, Online Methods: rise time to 90% of maximum, mean +/- s.d.,
# n = 3. These are MEASUREMENTS, so they are drawn as markers with their error
# bars and never joined by a line -- a line across three load levels would be
# an interpolation claim nobody made, and the point of the figure is that the
# room reads the spread rather than a trend.
MISHRA_RISE = {           # load multiple -> (mean minutes, s.d.)
    "unbuffered": {0: (396.1, 23.0), 1: (474.6, 45.3), 2: (698.9, 47.9)},
    "buffered":   {0: (432.4, 8.9),  1: (420.2, 20.9), 2: (423.2, 21.5)},
}


def fig_response_times():
    """Every rise time Mishra measured, with its spread, so the room can read it.

    This figure exists because segment 8 asks whether a 9% insulation cost is
    real, and the numbers it asks about were printed in prose. A question about
    whether an effect clears its error bars cannot be asked on a slide that
    does not draw the error bars.

    THE TWO NO-LOAD BARS DO NOT OVERLAP. 396.1 + 23.0 = 419.1 against
    432.4 - 8.9 = 423.5, so they clear each other by 4.4 minutes -- and the
    Welch test on the same six numbers still gives t = 2.549, df = 2.59,
    p = 0.097. That is the lesson: one-standard-deviation bars that miss each
    other are not a significance test, because at n = 3 the standard error is
    s.d./sqrt(3) and the t distribution has barely two degrees of freedom to
    work with. An earlier draft of this figure claimed the bars overlapped.
    They do not, and the truth is the better teaching point.

    Two further readings are available and neither is annotated, because
    naming them would answer the question the release asks:

      * the unbuffered series climbs 396 -> 475 -> 699 and its 0x and 2x bars
        are nowhere near each other. The load effect is not in doubt.
      * the buffered series is 432 -> 420 -> 423. It is NON-MONOTONIC, its 0x
        value is the slowest of its own three, and its internal range of
        12.2 min is 34% of the 36.3 min premium being claimed.

    The bracket names the comparison the release asks about. It does not say
    what to conclude about it.
    """
    fig, ax = plt.subplots(figsize=(9.0, 5.3))

    series = [("plain circuit", "unbuffered", RED, "o", -0.075),
              ("with load driver", "buffered", GREEN, "s", +0.075)]

    for label, key, colour, marker, dx in series:
        xs = [n + dx for n in (0, 1, 2)]
        ys = [MISHRA_RISE[key][n][0] for n in (0, 1, 2)]
        es = [MISHRA_RISE[key][n][1] for n in (0, 1, 2)]
        ax.errorbar(xs, ys, yerr=es, fmt=marker, color=colour, ms=13,
                    capsize=9, capthick=2.4, elinewidth=2.4, ls="none",
                    label=label, zorder=5)
        # Each mean beside its own marker, so the slide needs no table.
        for x, y in zip(xs, ys):
            ax.text(x + 0.10, y, "%.1f" % y, color=MUTED,
                    fontsize=TYPE["caption"], ha="left", va="center")

    # The comparison segment 8 asks about: the two no-load points, NAMED and
    # not adjudicated. The guide lines matter -- without them the arrow floats
    # in the left margin and reads as a stray glyph rather than as a bracket
    # spanning those two particular means.
    lo = MISHRA_RISE["unbuffered"][0][0]
    hi = MISHRA_RISE["buffered"][0][0]
    xb = -0.33
    for y, xm in ((lo, -0.075), (hi, +0.075)):
        ax.plot([xb, xm], [y, y], ls=":", lw=1.6, color=MUTED, zorder=2)
    ax.annotate("", xy=(xb, lo), xytext=(xb, hi),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=2.2))
    ax.text(xb - 0.09, (lo + hi) / 2, "the 9%\nclaim", color=INK,
            fontsize=TYPE["body"], ha="right", va="center", linespacing=1.2)

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["no load", r"1$\times$ load", r"2$\times$ load"])
    ax.set_xlim(-1.05, 2.50)
    ax.set_ylim(330, 790)
    ax.set_ylabel("time to 90% of final level  (min)")
    ax.set_title("Every rise time they measured, with its spread", pad=14)
    ax.legend(loc="upper left", frameon=False)
    # One line, hard into the empty left margin the bracket opened up: a
    # two-line block at lower right ran through the 420.2 and 423.2 labels.
    ax.text(0.012, 0.022,
            r"Mishra 2014, Online Methods  ·  mean $\pm$ s.d., n = 3",
            transform=ax.transAxes, ha="left", va="bottom",
            color=MUTED, fontsize=TYPE["caption"])
    _save(fig, "s21_response_times")


FIGURES = [fig_object, fig_step_response, fig_both_costs,
           fig_conservation, fig_affinity, fig_bandwidth,
           fig_response_times]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
