"""Session 18 figures — covalent modification cycles and zero-order ultrasensitivity.

Every curve comes out of `posb.protein`, the same functions the students call,
so the plot on the slide is the plot they can reproduce.

What this session has to draw, and where each is verified:

  * THE OBJECT, before any model. A conserved pool and two opposing enzymes.
    `fig_cycle` is a drawing, not a plot -- the vocabulary check in
    sessions/s18-protein/DESIGN.md found that "kinase" and "phosphatase" appear
    zero times in any deck from s04 to s17, so the thing has to be drawn.
  * THE RESPONSE, at four saturations. `fig_response` shows a hyperbola
    becoming a switch, with the crossing pinned at one half throughout --
    which is `posb.protein.crossing_fraction` being exact.
  * THE SHARPENING, against the paper's own two claims. `fig_apparent_hill`
    plots apparent Hill coefficient against saturation and marks where
    Goldbeter & Koshland's prose and their own Eq. 10 disagree.
  * THE PRICE. `fig_threshold_tradeoff` -- a sharp switch cannot be placed with
    affinities. This is the design constraint and it is the one surface that
    has to land.
  * THE PAIR. `fig_both_saturated` -- saturating one enzyme buys almost
    nothing. Session 17's orthogonality lesson in a new place.

No number here is measured. Every value is a property of the equations, and
`sessions/s18-protein/NUMBERS.md` carries the measured counterparts from
Dueber 2007 and Bashor 2008 with their citations.

Run:  python tools/build_figures.py s18
"""
import numpy as np

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           RULE, TYPE)
from posb import protein

plt = use()                 # the 20pt content floor, not LEGACY_SCALE
OUT = "figures/build"

# The four saturation regimes the session walks through, and the colour each
# keeps on every surface so the room can track one curve across figures.
REGIMES = [(10.0, MUTED, "unsaturated"),
           (1.0, TEAL, None),
           (0.1, CYAN, None),
           (0.01, AMBER, "saturated")]


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# The object: a conserved pool and two opposing enzymes
# ---------------------------------------------------------------------------
def fig_cycle():
    """A drawing. Nothing is made and nothing is destroyed -- the pool moves."""
    fig, ax = plt.subplots(figsize=(11.9, 4.8))
    ax.set_xlim(0, 11.9)
    ax.set_ylim(0, 4.8)
    ax.set_aspect("equal")      # otherwise plt.Circle renders as an ellipse
    ax.axis("off")

    # the two forms of the same molecule
    for x, label, sub, col in [(3.3, "W", "unmodified", TEAL),
                               (9.3, "W*", "modified", GREEN)]:
        ax.add_patch(plt.Circle((x, 2.5), 0.82, facecolor=col, edgecolor="none",
                                zorder=3))
        ax.text(x, 2.5, label, ha="center", va="center", color="white",
                fontsize=34, fontweight="bold", zorder=4)
        ax.text(x, 1.30, sub, ha="center", va="center", color=MUTED,
                fontsize=TYPE["caption"])

    # Forward and reverse arcs. The reverse arc bows down to about y = 1.3 at
    # its midpoint, so its labels sit below that, not at 0.9 where the first
    # build put them -- the word "phosphatase" was struck through by the arc.
    ax.annotate("", xy=(8.45, 3.05), xytext=(4.15, 3.05),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.7",
                                color=INK, lw=3.0,
                                connectionstyle="arc3,rad=-0.30"))
    ax.annotate("", xy=(4.15, 1.95), xytext=(8.45, 1.95),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.7",
                                color=INK, lw=3.0,
                                connectionstyle="arc3,rad=-0.30"))
    ax.text(6.30, 4.30, "kinase", ha="center", color=INK,
            fontsize=TYPE["body"], fontweight="bold")
    ax.text(6.30, 3.90, "$V_1$,  $K_{m1}$", ha="center", color=INK,
            fontsize=TYPE["body"])
    ax.text(6.30, 0.62, "phosphatase", ha="center", color=INK,
            fontsize=TYPE["body"], fontweight="bold")
    ax.text(6.30, 0.22, "$V_2$,  $K_{m2}$", ha="center", color=INK,
            fontsize=TYPE["body"])

    # The conservation statement, which is the whole reason this behaves
    # differently from every circuit so far. Clear of the W disc -- the first
    # build ran the box under it.
    ax.add_patch(plt.Rectangle((0.15, 2.10), 1.85, 0.82, facecolor="none",
                               edgecolor=RULE, lw=2.0))
    ax.text(1.075, 2.51, "$W + W^*$\n$= W_T$", ha="center", va="center",
            color=INK, fontsize=TYPE["caption"])
    _save(fig, "s18_cycle")


# ---------------------------------------------------------------------------
# The response, at four saturations
# ---------------------------------------------------------------------------
def _response(k1, k2, u):
    return np.array([protein.modified_fraction(ui, k1, k2) for ui in u])


def fig_response():
    """A hyperbola becoming a switch. The crossing never moves."""
    u = np.logspace(-2, 2, 1400)
    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    # No apparent-Hill labels here, deliberately. All four curves converge at
    # the right-hand edge so the labels collide -- and more to the point, this
    # surface comes BEFORE the sharpening is quantified, so a number on it
    # would be the s10 defect: a figure printing an answer the room has not
    # reached. The quantification is fig_apparent_hill.
    for k, col, tag in REGIMES:
        lab = f"$K_m/W_T$ = {k:g}" + (f"   ({tag})" if tag else "")
        ax.plot(u, _response(k, k, u), color=col, lw=3.0, label=lab)
    ax.axvline(1.0, color=RULE, lw=1.8, zorder=0)
    ax.axhline(0.5, color=RULE, lw=1.8, zorder=0)
    ax.set_xscale("log")
    ax.set_xlabel("$V_1/V_2$    (ratio of the two enzymes' maximal rates)")
    ax.set_ylabel("fraction modified")
    ax.set_xlim(1e-2, 1.9e2)
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="upper left", fontsize=TYPE["caption"])
    _save(fig, "s18_response")


def fig_response_crossing():
    """The same curves, with the exact crossing called out.

    A separate figure because the crossing result is derived AFTER the curves
    are first shown, and a figure must not print a number the room has not
    reached. (The s10 lesson: a committed figure that annotated three answers
    three surfaces before they were defined.)
    """
    u = np.logspace(-2, 2, 1400)
    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    for k, col, _ in REGIMES:
        ax.plot(u, _response(k, k, u), color=col, lw=3.0, label=f"{k:g}")
    ax.plot([1.0], [0.5], "o", ms=16, mfc="none", mec=RED, mew=3.5, zorder=8)
    ax.annotate("every curve crosses here\n$w = k_2/(k_1{+}k_2) = 1/2$,  exactly",
                xy=(1.0, 0.5), xytext=(2.3, 0.21), color=RED,
                fontsize=TYPE["caption"],
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
    ax.axvline(1.0, color=RULE, lw=1.8, zorder=0)
    ax.set_xscale("log")
    ax.set_xlabel("$V_1/V_2$")
    ax.set_ylabel("fraction modified")
    ax.set_xlim(1e-2, 1.9e2)
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="upper left", fontsize=TYPE["caption"], title="$k_1 = k_2 = K_m/W_T$",
              title_fontsize=TYPE["caption"])
    _save(fig, "s18_response_crossing")


# ---------------------------------------------------------------------------
# The sharpening, and where the paper disagrees with itself
# ---------------------------------------------------------------------------
def fig_apparent_hill():
    """Apparent Hill coefficient against saturation, on log axes.

    The two marked points are the two parameter values Goldbeter & Koshland
    name in their text. Their Eq. 10 and `posb.protein` agree on both; the
    paper's PROSE does not. See NUMBERS.md section 1.
    """
    k = np.logspace(-3, 1.3, 420)
    n = np.array([protein.apparent_hill(ki, ki) for ki in k])

    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    ax.plot(k, n, color=TEAL, lw=3.4, zorder=4)
    ax.axhline(1.0, color=MUTED, lw=2.2, ls="--", zorder=2)
    # The x axis is INVERTED, so "larger k" is to the LEFT. Two earlier builds
    # got this wrong: offsets multiplied onto k move text left, not right, and
    # one label left the axes entirely. Both annotations now sit in the large
    # empty region ABOVE the curve at large k, with arrows down to the markers,
    # and the positions are absolute rather than offsets.
    ax.text(1.6e-3, 1.09, "a hyperbola:  n = 1", color=MUTED,
            fontsize=TYPE["caption"], va="bottom", ha="right")

    for ki, says, col, tx, ty in [
            (0.1, "paper says 2.9", AMBER, 2.6, 26.0),
            (0.01, "paper says “> 13”", RED, 0.42, 150.0)]:
        ni = protein.apparent_hill(ki, ki)
        ax.plot([ki], [ni], "o", ms=13, color=col, zorder=6)
        ax.annotate(f"$K_m/W_T$ = {ki:g}\nequation gives {ni:.1f}\n{says}",
                    xy=(ki, ni), xytext=(tx, ty),
                    color=col, fontsize=TYPE["caption"],
                    ha="center", va="center",
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2,
                                    shrinkA=16, shrinkB=12))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("$k_1 = k_2 = K_m/W_T$    (Michaelis constant, in units of the substrate pool)")
    ax.set_ylabel("apparent Hill n")
    ax.set_xlim(1e-3, 2e1)
    ax.set_ylim(0.85, 500)
    ax.invert_xaxis()           # saturation increases to the right
    _save(fig, "s18_apparent_hill")


# ---------------------------------------------------------------------------
# The price: a sharp switch cannot be placed with affinities
# ---------------------------------------------------------------------------
def threshold_band(target_n, n_k2=320):
    """Range of u50 reachable at a given apparent Hill coefficient.

    For each k2, find the k1 that hits the target sharpness, then record the
    threshold that pair gives. Returns (lo, hi).
    """
    from scipy.optimize import brentq
    lo, hi = np.inf, 0.0
    for k2 in np.logspace(-4, 2, n_k2):
        f = lambda k1: protein.apparent_hill(k1, k2) - target_n
        try:
            if f(1e-6) * f(1e3) > 0:
                continue
            k1 = brentq(f, 1e-6, 1e3, xtol=1e-12)
        except (ValueError, RuntimeError):
            continue
        u50 = protein.half_maximal_stimulus(k1, k2)
        lo, hi = min(lo, u50), max(hi, u50)
    return lo, hi


def fig_threshold_tradeoff():
    """The design constraint. Sharpness is bought by giving up the threshold."""
    targets = np.array([2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0, 32.0])
    bands = [threshold_band(t) for t in targets]
    lo = np.array([b[0] for b in bands])
    hi = np.array([b[1] for b in bands])

    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    ax.fill_between(targets, lo, hi, color=CYAN, alpha=0.30, zorder=2,
                    label="thresholds reachable by choosing $k_1$, $k_2$")
    ax.plot(targets, lo, color=TEAL, lw=2.6, zorder=3)
    ax.plot(targets, hi, color=TEAL, lw=2.6, zorder=3)
    ax.axhline(1.0, color=RED, lw=2.4, ls="--", zorder=4,
               label="$V_1/V_2 = 1$: the two capacities are equal")
    ax.set_yscale("log")
    ax.set_xlabel("apparent Hill n  (how sharp you want the switch)")
    ax.set_ylabel("$(V_1/V_2)_{50}$,  where it fires")
    ax.set_xlim(2, 32)
    ax.set_ylim(1e-3, 1e3)
    ax.legend(loc="upper right", fontsize=TYPE["caption"])
    # The first build put this line directly under the legend, where it read
    # as a third legend entry. The band is flat and empty along the bottom.
    ax.text(31.2, 2.6e-3, "at n = 32 the threshold is pinned within 3.4% of 1",
            color=RED, fontsize=TYPE["caption"], ha="right", va="bottom")
    ax.text(2.4, 2.6e-3, f"at n = 2:  {lo[0]:.3f} to {hi[0]:.0f}",
            color=TEAL, fontsize=TYPE["caption"], ha="left", va="bottom")
    _save(fig, "s18_threshold_tradeoff")


# ---------------------------------------------------------------------------
# The property belongs to the pair
# ---------------------------------------------------------------------------
def fig_both_saturated():
    """Saturate one enzyme and you get almost nothing."""
    k2 = np.logspace(-3, 1, 300)
    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    for k1, col in [(0.005, AMBER), (0.05, CYAN), (0.5, TEAL)]:
        n = np.array([protein.apparent_hill(k1, kk) for kk in k2])
        ax.plot(k2, n, color=col, lw=3.0, label=f"$k_1$ = {k1:g}")
        ax.plot([k1], [protein.apparent_hill(k1, k1)], "o", ms=12, color=col,
                zorder=6)
    ax.axhline(1.0, color=MUTED, lw=2.0, ls="--")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("$k_2$    (the OTHER enzyme's saturation)")
    ax.set_ylabel("apparent Hill n")
    ax.set_xlim(1e-3, 1e1)
    ax.set_ylim(0.8, 120)
    ax.legend(loc="upper right", fontsize=TYPE["caption"])
    ax.text(1.08e-3, 1.5, "filled circle: both enzymes equally saturated",
            color=MUTED, fontsize=TYPE["caption"], va="bottom")
    _save(fig, "s18_both_saturated")


FIGURES = [fig_cycle, fig_response, fig_response_crossing,
           fig_apparent_hill, fig_threshold_tradeoff, fig_both_saturated]


if __name__ == "__main__":
    for k in (10.0, 1.0, 0.1, 0.01, 0.001):
        print(f"k = {k:<8} Rv = {protein.sensitivity_index(k, k):<10.5f} "
              f"n = {protein.apparent_hill(k, k):.3f}")
    print()
    for t in (4.0, 8.0, 16.0, 32.0):
        lo, hi = threshold_band(t)
        print(f"n = {t:<5} u50 reachable {lo:.4f} to {hi:.4f}  "
              f"(factor {hi/lo:.2f})")
