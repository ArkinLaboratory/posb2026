"""Session 20 figures — the coupling you can write down exactly.

Every number here comes out of `posb.fba` -- the same functions the students
call -- on `posb.fba.teaching_network()`, the nine-reaction network solved by
hand in `sessions/s20-metabolic/NUMBERS.md` section 6. Nothing is typed in.

What this session has to draw:

  * THE OBJECT. `fig_network` -- the network as a diagram beside its
    stoichiometric matrix. The same thing twice, which is the session's point:
    S is just the picture, counted.
  * THE ANSWER. `fig_flux_map` -- the optimum, and the same network with the
    TCA knocked out. The branch point goes all-or-nothing both times, to a
    different vertex.
  * THE KNOCKOUTS. `fig_knockouts` -- four lethal, one costly, two free.
  * THE LIMITATION. `fig_alternate_optima` -- add a parallel route and two
    fluxes become undetermined while the objective does not move.

Fong & Palsson's own Figure 1 is a PAPER figure and belongs in a paper-figure
slot, not here; this module draws only what is ours.

Run:  python tools/build_figures.py s20
"""
import numpy as np

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           RULE, TYPE)
from posb import fba

plt = use()
OUT = "figures/build"

_REACTIONS, _EXTERNAL, BOUNDS = fba.teaching_network()
MODEL = fba.FluxModel(_REACTIONS, external=_EXTERNAL)
OBJ = "v_biomass"

# Node positions for the network diagram: a straight spine with the two
# branches hanging off it, so the branch point is visually a branch point.
POS = {
    "G6P": (0, 3), "F6P": (0, 2), "T3P": (0, 1), "PYR": (0, 0),
    "P5P": (1.6, 2.4), "ATP": (1.6, 0.6),
}


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def fig_network():
    """The nine reactions in words, beside the same nine as a matrix.

    An earlier draft drew a node-and-arrow diagram here. At the 20pt floor the
    metabolite boxes touched and every arrow label was clipped by one, and the
    diagram was adding nothing the reaction list does not say more precisely.
    The pairing that carries the session's point is words-to-matrix: these are
    the same nine lines, and S is what you get by counting them.
    """
    fig, (axl, axm) = plt.subplots(
        1, 2, figsize=(14.0, 5.8), gridspec_kw={"width_ratios": [1.0, 1.35]})

    lines = [
        ("uptake",  "$\\rightarrow$ G6P", "$\\leq 10$"),
        ("pgi",     "G6P $\\rightarrow$ F6P", ""),
        ("zwf",     "G6P $\\rightarrow$ P5P + CO$_2$", ""),
        ("tpi",     "F6P $\\rightarrow$ 2 T3P", ""),
        ("lower",   "T3P $\\rightarrow$ PYR + ATP", ""),
        ("ackA",    "PYR $\\rightarrow$ Ace + CO$_2$ + ATP", ""),
        ("tca",     "PYR $\\rightarrow$ 3 CO$_2$ + 3 ATP", ""),
        ("biomass", "2 T3P + P5P + 4 ATP $\\rightarrow$", ""),
        ("atpm",    "ATP $\\rightarrow$", ""),
    ]
    for i, (name, eqn, note) in enumerate(lines):
        y = 1.0 - (i + 0.5) / len(lines)
        colour = AMBER if name == "ackA" else (RED if name == "tca" else INK)
        axl.text(0.00, y, name, transform=axl.transAxes, color=colour,
                 fontsize=TYPE["body"], va="center", ha="left")
        axl.text(0.30, y, eqn, transform=axl.transAxes, color=colour,
                 fontsize=TYPE["body"], va="center", ha="left")
        if note:
            axl.text(1.0, y, note, transform=axl.transAxes, color=MUTED,
                     fontsize=TYPE["body"], va="center", ha="right")
    axl.axis("off")
    axl.set_title("nine reactions", pad=10)

    S = MODEL.S
    axm.imshow(np.sign(S), cmap="PuOr_r", vmin=-2, vmax=2, aspect="auto")
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            if S[i, j]:
                axm.text(j, i, f"{S[i, j]:+.0f}", ha="center", va="center",
                         color=INK, fontsize=TYPE["body"])
    axm.set_xticks(range(len(MODEL.names)))
    axm.set_xticklabels([n.replace("v_", "") for n in MODEL.names],
                        rotation=45, ha="right")
    axm.set_yticks(range(len(MODEL.metabolites)))
    axm.set_yticklabels(MODEL.metabolites)
    axm.set_title("the same nine, counted:  $\\mathbf{S}$", pad=10)
    axm.tick_params(length=0)
    for spine in axm.spines.values():
        spine.set_visible(False)
    _save(fig, "s20_network")


def _flux_bars(ax, fluxes, title, colour):
    names = [n for n in MODEL.names if n not in ("v_atpm",)]
    vals = [fluxes[n] for n in names]
    y = np.arange(len(names))
    ax.barh(y, vals, color=colour, height=0.62)
    for yi, v in zip(y, vals):
        if v > 0.05:
            ax.text(v + 0.18, yi, f"{v:.3g}", va="center",
                    color=INK, fontsize=TYPE["body"])
        else:
            ax.text(0.18, yi, "0", va="center", color=RED,
                    fontsize=TYPE["body"])
    ax.set_yticks(y)
    ax.set_yticklabels([n.replace("v_", "") for n in names])
    # Explicit, not invert_yaxis(): with sharey the inversion applied twice and
    # the pathway came out upside down. Pin it so the order is pathway order.
    ax.set_ylim(len(names) - 0.5, -0.5)
    ax.set_xlim(0, 12.4)
    ax.set_xlabel("flux")
    ax.set_title(title, pad=10)


def fig_flux_map():
    """The optimum, and the same network with the TCA removed."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 5.6), sharey=True)
    best, v = fba.solve_fba(MODEL, OBJ, BOUNDS)
    ko, vko = fba.solve_fba(MODEL, OBJ, BOUNDS, knockouts=("v_tca",))
    _flux_bars(a1, v, f"wild type:  biomass = {best:g}", TEAL)
    _flux_bars(a2, vko, f"tca knocked out:  biomass = {ko:.3g}", AMBER)
    # No floating annotation: the ackA row says it already -- 0 on the left,
    # 6.67 on the right -- and every band wide enough to hold the sentence is
    # occupied by a bar in one panel or the other.
    fig.suptitle("A linear program answers at a vertex, so the branch is all or nothing",
                 fontsize=TYPE["title"], color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(f"{OUT}/s20_flux_map.png")
    plt.close(fig)


def fig_knockouts():
    """Four lethal, one costly, two free -- and the lethal ones are EXACT."""
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    targets = ["v_pgi", "v_zwf", "v_tpi", "v_lower", "v_tca", "v_ackA", "v_atpm"]
    ko = fba.knockout_growth(MODEL, OBJ, BOUNDS, targets)
    wt = ko.pop("wild type")
    names = ["wild type"] + targets
    vals = [wt] + [ko[t] for t in targets]
    colours = [MUTED] + [RED if ko[t] == 0 else (AMBER if ko[t] < wt - 1e-9 else TEAL)
                         for t in targets]
    x = np.arange(len(names))
    ax.bar(x, vals, color=colours, width=0.66)
    for xi, v in zip(x, vals):
        ax.text(xi, v + 0.09, "0" if v == 0 else f"{v:.3g}", ha="center",
                color=INK, fontsize=TYPE["body"])
    ax.set_xticks(x)
    ax.set_xticklabels([n.replace("v_", "") for n in names], rotation=35, ha="right")
    ax.set_ylabel("predicted biomass")
    ax.set_ylim(0, 4.9)
    ax.set_title("Four of these are lethal, and exactly so", pad=10)
    # Above the four zero bars is the only region no bar reaches, and it is
    # about 42% of the width. The first draft of this note was two 45-character
    # lines and ran straight through the tca bar. Cut the text, not the type:
    # the Fong & Palsson comparison belongs in the speaker note anyway.
    ax.text(0.17, 0.60, "no second route\nto T3P, P5P or ATP",
            transform=ax.transAxes, ha="left", va="center",
            color=INK, fontsize=TYPE["body"], linespacing=1.25)
    _save(fig, "s20_knockouts")


def fig_alternate_optima():
    """Add a parallel route: the objective does not move, two fluxes come loose."""
    r_iso, ext, bnds = fba.teaching_network(isozyme=True)
    m2 = fba.FluxModel(r_iso, external=ext)
    best1, _ = fba.solve_fba(m2, OBJ, bnds)
    rng = fba.flux_ranges(m2, OBJ, bnds)

    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    names = [n for n in m2.names if n != "v_atpm"]
    y = np.arange(len(names))
    for yi, n in zip(y, names):
        lo, hi = rng[n]
        if hi - lo > 1e-7:
            ax.plot([lo, hi], [yi, yi], color=RED, lw=9, solid_capstyle="butt")
            ax.text(hi + 0.2, yi, f"free over [{lo:g}, {hi:g}]", va="center",
                    color=RED, fontsize=TYPE["body"])
        else:
            ax.plot([lo], [yi], "o", color=TEAL, ms=11)
    ax.set_yticks(y)
    ax.set_yticklabels([n.replace("v_", "") for n in names])
    ax.invert_yaxis()
    ax.set_xlim(-0.4, 12.4)
    ax.set_xlabel("flux at the optimum")
    ax.set_title(f"Objective unchanged at {best1:g}, and the solver still picks one",
                 pad=10)
    # mid-right, clear of every point (all of which sit at flux <= 6)
    ax.text(0.98, 0.44,
            "two routes, same stoichiometry.\n"
            "no growth measurement can tell them apart.",
            transform=ax.transAxes, ha="right", va="center",
            color=INK, fontsize=TYPE["body"], linespacing=1.25)
    _save(fig, "s20_alternate_optima")


FIGURES = [fig_network, fig_flux_map, fig_knockouts, fig_alternate_optima]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
