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
    different corner of the feasible region.
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
import functools

from posb import fba

plt = use()
OUT = "figures/build"

_REACTIONS, _EXTERNAL, BOUNDS = fba.teaching_network()
MODEL = fba.FluxModel(_REACTIONS, external=_EXTERNAL,
                      metabolites=["G6P", "F6P", "P5P", "T3P", "PYR",
                                   "ATP"])
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


def _save_pinned(fig, name):
    """Save without cropping to content, for a figure drawn in reveal stages.

    `style.use()` sets savefig.bbox = "tight", which crops to the artists that
    happen to be present. For a sequence that grows across slides that means
    every stage is cropped differently and the picture JUMPS as it advances,
    which is the opposite of a figure advancing beside an argument. Passing
    bbox_inches=None does not help: matplotlib falls back to the rcParam.
    """
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    with plt.rc_context({"savefig.bbox": None}):
        fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _annotate_column(fig, axl, axm):
    """Mark the v_tpi column, which is the one the room just wrote by hand.

    The debrief for the column release IS this picture: the nine lines they
    read off the pathway, the same nine counted, and their own answer marked
    inside it. Describing the matrix in words on the slide BEFORE the figure
    appeared was the defect Adam named -- show, do not only tell.

    WHAT WAS TRIED AND FAILED, both found by rendering. Callouts placed beside
    the two marked entries need arrows that cross the matrix, and those arrows
    land on the lower, ackA, tca and biomass cells and obscure them -- a -1
    reads as 1. Ledger lines placed in the left panel land on the reaction
    list, which fills it. So: the box carries the emphasis, one caption under
    the matrix names the answer, and the ledger belongs in the slide's rows.
    """
    j = list(MODEL.names).index("v_tpi")
    rows = list(MODEL.metabolites)

    axm.set_ylim(len(rows) - 0.4, -1.9)
    axm.add_patch(plt.Rectangle(
        (j - 0.5, -0.5), 1.0, len(rows), fill=False, edgecolor=TEAL,
        linewidth=3.4, zorder=4))
    axm.annotate("the column you just wrote", xy=(j, -0.56),
                 xytext=(j + 0.4, -1.55), ha="left", va="center",
                 color=TEAL, fontsize=TYPE["body"],
                 arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4))
    axm.text(0.5, -0.33, "$-$1 on F6P,  $+$2 on T3P.    "
                         "Six carbons in, six carbons out.",
             transform=axm.transAxes, ha="center", va="top", color=TEAL,
             fontsize=TYPE["body"])


def fig_network(annotate=False):
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
    if annotate:
        _annotate_column(fig, axl, axm)
        _save(fig, "s20_network_annotated")
    else:
        _save(fig, "s20_network")


def _flux_bars(ax, fluxes, title, colour):
    # All nine. v_atpm is 0 in both panels, and the zero is worth seeing on
    # an hour that has said "nine reactions" five times.
    names = list(MODEL.names)
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
    """The optimum the room just derived by hand, as nine numbers."""
    # ONE PANEL, 31 October. Adam: the slide this lands on debriefs five steps
    # of hand algebra about the WILD TYPE, and the second panel was a TCA
    # knockout -- a concept that does not exist for another segment. "What are
    # we debriefing exactly, where did the two scenarios come from?" The
    # knockout comparison is already carried by fig_knockouts, where knockouts
    # have been introduced, so nothing is lost by dropping it here.
    fig, ax = plt.subplots(figsize=(11.8, 5.4))
    best, v = fba.solve_fba(MODEL, OBJ, BOUNDS)
    _flux_bars(ax, v, f"biomass = {best:g},  from ten glucose", TEAL)
    # The zero is the whole point of the slide, so it gets said rather than
    # left to the reader: ackA is EXACTLY zero, which is what a corner means.
    # Along the ackA row itself, which is the one band with no bar in it.
    ax.annotate("exactly zero, not nearly zero",
                xy=(0.30, 5), xytext=(6.4, 5), va="center", ha="left",
                color=RED, fontsize=TYPE["body"],
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.0,
                                shrinkA=8, shrinkB=2))
    fig.tight_layout()
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
    # Middle of the panel, which is clear because v_uptake (the only bar out
    # past 6) is the top row and the text sits well below it.
    ax.text(0.98, 0.44,
            "two routes, same stoichiometry.\n"
            "no growth measurement can tell them apart.",
            transform=ax.transAxes, ha="right", va="center",
            color=INK, fontsize=TYPE["body"], linespacing=1.25)
    _save(fig, "s20_alternate_optima")



# ------------------------------------------------------- the pathway drawn ---
# ORIENTATION ONLY. Adam, 31 October: "why not show a piece of the glycolytic
# pathway and the pentose phosphate path?" -- the session asks the room to
# model an object it had only ever described in prose.
#
# `fig_network`'s docstring records an earlier node-and-arrow attempt that was
# abandoned because boxes touched and labels clipped. Three things are
# different here and each one was found by rendering, not by reasoning:
#   * BIOMASS IS NOT IN THIS FIGURE. It is segment 3's object, and putting it
#     to the right of PYR forces the P5P and T3P arrows across the spine --
#     which is exactly the collision that killed the first attempt.
#   * The figure gets a whole slide, not half of one beside a matrix.
#   * The lumping note lives in the slide foot, not on the arrows; two
#     "3 enzymes" labels crowded the arrows and one read as belonging to pgi.
#
# AND IT WITHHOLDS THE 2 IN tpi. F6P -> 2 T3P is what the release asks the
# room to write, and the carbon balance in that coefficient is the thing the
# release exists to catch. Do not label it here.
_P_GLC, _P_G6P, _P_F6P = (7, 48), (22, 48), (39, 48)
_P_T3P, _P_PYR = (56, 48), (73, 48)
_P_P5P, _P_ACE, _P_CO2 = (30, 88), (93, 80), (93, 16)


def _p_node(ax, p, label, colour=INK, sub=None):
    ax.text(p[0], p[1], label, ha="center", va="center", color=colour,
            fontsize=TYPE["emphasis"], zorder=5,
            bbox=dict(boxstyle="round,pad=0.40", facecolor="#F8FAF9",
                      edgecolor=colour, linewidth=2.0))
    if sub:
        text, (dx, dy, ha, va) = sub
        ax.text(p[0] + dx, p[1] + dy, text, ha=ha, va=va, color=MUTED,
                fontsize=TYPE["caption"], zorder=5)


def _p_arrow(ax, p0, p1, colour=INK, shrinkB=30):
    # shrinkB is in points and has to clear the TARGET node's bbox, which is
    # opaque and drawn at zorder 5. A wide label ("acetate", "biomass",
    # "3 CO2") swallows the head at the default, and on a slide about the
    # direction of flow a headless line is the whole figure lost.
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.8,
                                shrinkA=30, shrinkB=shrinkB))


def _p_lab(ax, p0, p1, text, colour=INK, dx=0, dy=7, size="body"):
    ax.text((p0[0] + p1[0]) / 2 + dx, (p0[1] + p1[1]) / 2 + dy, text,
            ha="center", va="center", color=colour, fontsize=TYPE[size],
            zorder=6, bbox=dict(boxstyle="round,pad=0.16",
                                facecolor="#F8FAF9", edgecolor="none"))


def _p_tokens(ax, x, y, n, colour):
    """n filled circles, as a countable stand-in for n ATP."""
    for i in range(n):
        ax.plot(x + i * 4.6, y, "o", ms=17, color=colour, zorder=6)


def fig_pathway(stage=4):
    """Glycolysis and the pentose phosphate branch, revealed in four stages.

    Stage 1 glucose committed; 2 the split out of G6P; 3 down to pyruvate;
    4 the branch. Each stage is a slide and the room is asked to predict the
    next one, which is the build move segment 1 did not have.
    """
    fig, ax = plt.subplots(figsize=(14.0, 5.9))
    ax.set_xlim(0, 100)
    ax.set_ylim(4, 102)
    ax.axis("off")

    _p_node(ax, _P_GLC, "glucose", MUTED)
    _p_node(ax, _P_G6P, "G6P", INK,
            ("six carbons, committed", (0, -11, "center", "top")))
    _p_arrow(ax, _P_GLC, _P_G6P, MUTED)
    _p_lab(ax, _P_GLC, _P_G6P, "uptake", MUTED, dy=14)

    if stage >= 2:
        _p_node(ax, _P_F6P, "F6P", INK)
        _p_node(ax, _P_P5P, "P5P", CYAN,
                ("ribose-5-phosphate", (7, -1, "left", "center")))
        _p_arrow(ax, _P_G6P, _P_F6P)
        _p_lab(ax, _P_G6P, _P_F6P, "pgi")
        _p_arrow(ax, _P_G6P, _P_P5P, CYAN)
        _p_lab(ax, _P_G6P, _P_P5P, "zwf", CYAN, dx=-9, dy=3)
        ax.text(_P_P5P[0] - 2, _P_P5P[1] + 11,
                "pentose phosphate \u2014 loses one C as CO$_2$",
                color=MUTED, fontsize=TYPE["caption"], ha="left", va="bottom")

    if stage >= 3:
        _p_node(ax, _P_T3P, "T3P", INK,
                ("triose phosphate", (0, -11, "center", "top")))
        _p_node(ax, _P_PYR, "PYR", INK)
        _p_arrow(ax, _P_F6P, _P_T3P)
        _p_lab(ax, _P_F6P, _P_T3P, "tpi", dy=9)
        _p_arrow(ax, _P_T3P, _P_PYR)
        _p_lab(ax, _P_T3P, _P_PYR, "lower")
        _p_lab(ax, _P_T3P, _P_PYR, "$+$1 ATP", AMBER, dy=-9, size="caption")

    if stage >= 4:
        _p_node(ax, _P_ACE, "acetate", AMBER)
        _p_node(ax, _P_CO2, "3 CO$_2$", RED)
        _p_arrow(ax, _P_PYR, _P_ACE, AMBER, shrinkB=54)
        _p_lab(ax, _P_PYR, _P_ACE, "ackA", AMBER, dx=-3, dy=7)
        _p_lab(ax, _P_PYR, _P_ACE, "$+$1 ATP", AMBER, dx=7, dy=-4,
               size="caption")
        # ackA is PYR -> Ace + CO2. Without the third carbon a student
        # counting carbons on a slide footed "counted carbons" sees 3 go
        # to 2. fig_overflow draws it; this one has to as well.
        ax.text(_P_ACE[0] - 9, _P_ACE[1], "$+$ 1 CO$_2$", color=MUTED,
                fontsize=TYPE["caption"], ha="right", va="center")
        _p_arrow(ax, _P_PYR, _P_CO2, RED, shrinkB=42)
        _p_lab(ax, _P_PYR, _P_CO2, "tca", RED, dx=-3, dy=5)
        _p_lab(ax, _P_PYR, _P_CO2, "$+$3 ATP", RED, dx=7, dy=-4,
               size="caption")

    _save_pinned(fig, f"s20_pathway_{stage}")



# ----------------------------------------------- the branch as a decision ---
# Adam, 31 October: expand the acetate/TCA branch, say why it is called
# overflow and why there is a decision there. The REAL numbers go in the slide
# rows with their citations; this figure draws only what is exact in the toy,
# so nothing on it is invented.
#
# CARBON MUST BALANCE ON THE PICTURE. ackA is PYR -> Ace + CO2, so the third
# carbon is drawn; without it a student counting carbons sees 3 go to 2 on a
# slide whose whole argument is that S counts atoms.
def fig_overflow():
    """One pyruvate, two fates: carbons out against ATP in.

    Toy numbers throughout, and the figure says so. Real E. coli yields nearer
    an order of magnitude more ATP down the respiratory route; that comparison
    belongs on the slide with its source, not in here.
    """
    fig, ax = plt.subplots(figsize=(13.6, 6.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(2, 100)
    ax.axis("off")

    PYR, ACE, CO2 = (13, 50), (56, 82), (56, 23)
    _p_node(ax, PYR, "PYR\n3 C", INK)

    _p_arrow(ax, PYR, ACE, AMBER, shrinkB=54)
    ax.text(31, 73, "ackA", color=AMBER, fontsize=TYPE["body"], ha="center")
    _p_node(ax, ACE, "acetate\n2 C", AMBER)
    ax.text(ACE[0], ACE[1] - 15, "$+$ 1 CO$_2$", color=MUTED,
            fontsize=TYPE["caption"], ha="center", va="top")
    ax.text(70, 82, "excreted", color=AMBER, fontsize=TYPE["body"],
            ha="left", va="center")
    ax.text(70, 71, "two of three carbons\nleave the cell unburned",
            color=MUTED, fontsize=TYPE["caption"], ha="left", va="top")
    _p_tokens(ax, 70, 92, 1, AMBER)
    ax.text(70 + 1 * 4.6 + 2.5, 92, "1 ATP", color=AMBER,
            fontsize=TYPE["body"], ha="left", va="center")

    _p_arrow(ax, PYR, CO2, RED, shrinkB=42)
    ax.text(31, 30, "tca", color=RED, fontsize=TYPE["body"], ha="center")
    _p_node(ax, CO2, "3 CO$_2$", RED)
    ax.text(70, 23, "all three burned", color=RED, fontsize=TYPE["body"],
            ha="left", va="center")
    ax.text(70, 13, "nothing left to excrete", color=MUTED,
            fontsize=TYPE["caption"], ha="left", va="top")
    _p_tokens(ax, 70, 37, 3, RED)
    ax.text(70 + 3 * 4.6 + 2.5, 37, "3 ATP", color=RED,
            fontsize=TYPE["body"], ha="left", va="center")

    ax.text(50, 50, "one pyruvate,\ntwo fates", color=INK,
            fontsize=TYPE["body"], ha="center", va="center")
    ax.text(0.012, 0.015,
            "ATP yields are the nine-reaction model's, not E. coli's",
            transform=ax.transAxes, color=MUTED, fontsize=TYPE["caption"],
            ha="left", va="bottom")
    _save_pinned(fig, "s20_overflow")



# ----------------------------------------------------- what S leaves open ---
# Adam, 31 October, on the last step of the null-space run: "The space is NOT
# constrained. Mass conservation is not enough! Showing this as a flux cone and
# demonstrating we can trade fluxes against each other while still conserving
# mass shows the problem. We need a visual for that."
#
# So this is the real projected feasible set, computed, not a cartoon. Two
# facts it draws, both exact for this network:
#   * with uptake <= 10 the projection onto (v_ackA, v_tca) is the triangle
#     v_ackA + v_tca <= 20 -- ten glucose is twenty pyruvate, and nothing else
#     bounds the branch;
#   * with NO cap on uptake every point of the positive quadrant is feasible,
#     which is the cone, and is why the slide can say the set runs off the page.
# Biomass is a field over the triangle and runs 0 to 4, so the picture says
# both halves at once: mass balance admits all of this, and it does not care
# which point you take.
def _cone_best(a, t, cap=10.0):
    """Largest biomass compatible with v_ackA = a, v_tca = t. NaN if infeasible."""
    from scipy.optimize import linprog
    names = list(MODEL.names)
    ia, it = names.index("v_ackA"), names.index("v_tca")
    ib, iu = names.index(OBJ), names.index("v_uptake")
    bnd = [(0, None)] * len(names)
    bnd[iu] = (0, cap)
    bnd[ia] = (a, a)
    bnd[it] = (t, t)
    c = np.zeros(len(names))
    c[ib] = -1.0
    r = linprog(c, A_eq=MODEL.S, b_eq=np.zeros(MODEL.S.shape[0]), bounds=bnd,
                method="highs")
    if r.status != 0:
        return float("nan")
    b = -r.fun
    return 0.0 if abs(b) < 1e-9 else b


def fig_cone():
    """The feasible set in two of its nine dimensions, coloured by biomass."""
    from matplotlib.colors import LinearSegmentedColormap
    n, LIM = 61, 23.0
    g = np.linspace(0, 22, n)
    A, T = np.meshgrid(g, g)
    Z = np.where(A + T <= 20.0 + 1e-9, 0.0, np.nan)
    for i in range(n):
        for j in range(n):
            if not np.isnan(Z[i, j]):
                Z[i, j] = _cone_best(A[i, j], T[i, j])
    cmap = LinearSegmentedColormap.from_list("biomass", ["#EEF4F2", CYAN, TEAL])

    fig, ax = plt.subplots(figsize=(13.4, 5.7))
    ax.add_patch(plt.Rectangle((0, 0), LIM, LIM, facecolor="#EFF3F2",
                               edgecolor="none", zorder=0))
    m = ax.pcolormesh(A, T, Z, cmap=cmap, shading="gouraud", vmin=0, vmax=4,
                      zorder=1)
    ax.plot([0, 20, 0, 0], [20, 0, 0, 20], color=INK, lw=2.6, zorder=3)
    fig.colorbar(m, ax=ax, pad=0.02).set_label("biomass this state allows")

    for a, t, col in [(0.0, 4.0, TEAL), (6.0, 6.0, AMBER), (10.0, 10.0, RED)]:
        b = _cone_best(a, t)
        ax.plot(a, t, "o", ms=15, color=col, mec="white", mew=2.2, zorder=6)
        ax.annotate(f"biomass {b:g}", (a, t), textcoords="offset points",
                    xytext=(-128 if a >= 9 else 14, 11), color=col,
                    fontsize=TYPE["body"], zorder=7,
                    bbox=dict(boxstyle="round,pad=0.18",
                              facecolor="#F8FAF9", edgecolor="none"))

    ax.annotate("uptake $\\leq$ 10 draws this edge:\n"
                "ten glucose is twenty pyruvate",
                xy=(12.6, 7.4), xytext=(22.2, 15.6), color=INK,
                fontsize=TYPE["body"], ha="right", va="center", zorder=7,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#F8FAF9",
                          edgecolor="none"),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2))
    ax.text(21.6, 21.6, "with no cap on glucose,\nout here balances mass too",
            color=MUTED, fontsize=TYPE["caption"], ha="right", va="top",
            zorder=7)

    ax.set_xlabel("flux to acetate,  $v_{ackA}$")
    ax.set_ylabel("flux round the TCA,  $v_{tca}$")
    ax.set_xlim(-0.6, LIM)
    ax.set_ylim(-0.6, LIM)
    ax.set_title("$\\mathbf{S}\\,v = 0$ and $v \\geq 0$ allow all of this")
    _save(fig, "s20_cone")



# ------------------------------------------------- the six lines, in steps ---
# Adam, 31 October, on the flux-map slide: "appears with NO explanation. What
# is the actual problem here? We haven't walked them through this calculation."
#
# The six lines are the hour's central calculation and they lived only on the
# board and in the handout. docs/lecture-design.md 5b moved derivations off the
# board; this one never moved. These are the figures for the derivation_fig
# column, 5.4in wide: ONE BALANCE PER STEP, because each line of the six is
# one row of S set to zero. A whole network per step does not fit the column
# and does not say which row is being used.
#
# No captions on these. derivation_fig prints the step label above the
# equation already, and a caption at the top of a 4.7in figure lands on the
# top node -- found by rendering.
def _sl_box(ax, x, y, t, c=INK):
    ax.text(x, y, t, ha="center", va="center", color=c, fontsize=TYPE["body"],
            zorder=5, bbox=dict(boxstyle="round,pad=0.34", facecolor="#F8FAF9",
                                edgecolor=c, linewidth=2.0))


def _sl_arrow(ax, p0, p1, c=INK):
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(
        arrowstyle="-|>", color=c, lw=2.6, shrinkA=26, shrinkB=26))


def _sl_lab(ax, p0, p1, t, c=INK, dx=0, dy=8):
    ax.text((p0[0] + p1[0]) / 2 + dx, (p0[1] + p1[1]) / 2 + dy, t,
            ha="center", va="center", color=c, fontsize=TYPE["body"], zorder=6,
            bbox=dict(boxstyle="round,pad=0.14", facecolor="#F8FAF9",
                      edgecolor="none"))


def fig_sixlines(step):
    """One metabolite's balance per step: what makes it, what uses it."""
    fig, ax = plt.subplots(figsize=(5.4, 4.7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    if step == 1:                                             # P5P
        A, B, C = (50, 86), (50, 50), (50, 14)
        _sl_box(ax, *A, "G6P", MUTED); _sl_box(ax, *B, "P5P", CYAN)
        _sl_box(ax, *C, "biomass", TEAL)
        _sl_arrow(ax, A, B, CYAN); _sl_lab(ax, A, B, "$v_{zwf}$", CYAN, dx=24)
        _sl_arrow(ax, B, C, TEAL); _sl_lab(ax, B, C, "$b$", TEAL, dx=18)
    elif step == 2:                                           # G6P
        A, B, L, R = (50, 88), (50, 52), (16, 14), (84, 14)
        _sl_box(ax, *A, "glucose", MUTED); _sl_box(ax, *B, "G6P", INK)
        _sl_box(ax, *L, "F6P", INK); _sl_box(ax, *R, "P5P", CYAN)
        _sl_arrow(ax, A, B, MUTED); _sl_lab(ax, A, B, "10", MUTED, dx=16)
        _sl_arrow(ax, B, L); _sl_lab(ax, B, L, "$v_{pgi}$", INK, dx=-18, dy=2)
        _sl_arrow(ax, B, R, CYAN)
        _sl_lab(ax, B, R, "$v_{zwf}$", CYAN, dx=18, dy=2)
    elif step == 3:                                           # F6P
        A, B, C = (50, 86), (50, 50), (50, 14)
        _sl_box(ax, *A, "G6P", MUTED); _sl_box(ax, *B, "F6P", INK)
        _sl_box(ax, *C, "T3P", INK)
        _sl_arrow(ax, A, B); _sl_lab(ax, A, B, "$v_{pgi}$", INK, dx=24)
        _sl_arrow(ax, B, C); _sl_lab(ax, B, C, "$v_{tpi}$", INK, dx=24)
    elif step == 4:                                           # T3P
        A, B, L, R = (50, 88), (50, 52), (16, 14), (84, 14)
        _sl_box(ax, *A, "F6P", MUTED); _sl_box(ax, *B, "T3P", INK)
        _sl_box(ax, *L, "biomass", TEAL); _sl_box(ax, *R, "PYR", INK)
        _sl_arrow(ax, A, B); _sl_lab(ax, A, B, "2 $v_{tpi}$", INK, dx=22)
        _sl_arrow(ax, B, L, TEAL); _sl_lab(ax, B, L, "2$b$", TEAL, dx=-16, dy=3)
        _sl_arrow(ax, B, R); _sl_lab(ax, B, R, "$v_{lower}$", INK, dx=18, dy=3)
    elif step == 5:                                           # ATP
        L, R, B, C = (16, 86), (84, 86), (50, 50), (50, 14)
        _sl_box(ax, *L, "lower", AMBER); _sl_box(ax, *R, "tca", RED)
        _sl_box(ax, *B, "ATP", AMBER); _sl_box(ax, *C, "biomass", TEAL)
        _sl_arrow(ax, L, B, AMBER); _sl_lab(ax, L, B, "1", AMBER, dx=-13, dy=3)
        _sl_arrow(ax, R, B, RED); _sl_lab(ax, R, B, "3", RED, dx=13, dy=3)
        _sl_arrow(ax, B, C, TEAL); _sl_lab(ax, B, C, "4$b$", TEAL, dx=18)
    else:
        raise ValueError(f"fig_sixlines: no step {step}")

    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    with plt.rc_context({"savefig.bbox": None}):
        fig.savefig(f"{OUT}/s20_sixlines_{step}.png")
    plt.close(fig)



# -------------------------------------------------- a deletion, and its cost ---
# Adam, 31 October: "we should state what a knock out does and then show +/-
# genes", and on the release that follows: "how are they going to do this.. we
# can show the network and the biomass flow connecting the inputs to them and
# THEN ask this question."
#
# So this is the only s20 figure that draws biomass, and the layout exists to
# make that possible: the pentose branch hangs BELOW the spine and biomass sits
# under it, so the P5P and T3P feeds reach biomass without crossing anything.
# Putting biomass to the right of PYR -- the obvious place -- forces both feeds
# back across the spine, which is the collision `fig_pathway` is built to avoid.
_C_GLC, _C_G6P, _C_F6P = (7, 78), (22, 78), (39, 78)
_C_T3P, _C_PYR = (56, 78), (73, 78)
_C_P5P, _C_BIO, _C_ACE, _C_CO2 = (30, 42), (56, 19), (92, 94), (92, 58)


def fig_cuts(cut=None):
    """The network with biomass, optionally with one reaction deleted."""
    dead = {"zwf": {"P5P", "biomass"}}.get(cut, set())
    grey = lambda n, c: MUTED if n in dead else c

    fig, ax = plt.subplots(figsize=(13.2, 5.9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 102)
    ax.axis("off")

    _p_node(ax, _C_GLC, "glucose", MUTED)
    for p, t in ((_C_G6P, "G6P"), (_C_F6P, "F6P"), (_C_T3P, "T3P"),
                 (_C_PYR, "PYR")):
        _p_node(ax, p, t, INK)
    _p_node(ax, _C_P5P, "P5P", grey("P5P", CYAN))
    # The ATP demand hangs off biomass itself. As a floating label it sat
    # nearer the P5P arrow than to biomass, and the segment-4 release turns
    # on a student chasing lower -> PYR -> ATP -> biomass off this picture.
    _p_node(ax, _C_BIO, "biomass", grey("biomass", TEAL),
            sub=("$+$ 4 ATP", (0, -10, "center", "top")))
    _p_node(ax, _C_ACE, "acetate", AMBER)
    _p_node(ax, _C_CO2, "3 CO$_2$", RED)

    _p_arrow(ax, _C_GLC, _C_G6P, MUTED)
    _p_lab(ax, _C_GLC, _C_G6P, "10", MUTED, dy=9)
    _p_arrow(ax, _C_G6P, _C_F6P); _p_lab(ax, _C_G6P, _C_F6P, "pgi")
    _p_arrow(ax, _C_F6P, _C_T3P); _p_lab(ax, _C_F6P, _C_T3P, "tpi")
    _p_arrow(ax, _C_T3P, _C_PYR); _p_lab(ax, _C_T3P, _C_PYR, "lower")
    _p_lab(ax, _C_T3P, _C_PYR, "$+$1 ATP", AMBER, dy=-9, size="caption")
    _p_arrow(ax, _C_G6P, _C_P5P, MUTED if cut == "zwf" else CYAN)
    _p_lab(ax, _C_G6P, _C_P5P, "zwf", RED if cut == "zwf" else CYAN,
           dx=-9, dy=0)
    _p_arrow(ax, _C_P5P, _C_BIO, grey("P5P", TEAL), shrinkB=64)
    _p_lab(ax, _C_P5P, _C_BIO, "P5P", grey("P5P", TEAL), dx=-9, dy=0)
    _p_arrow(ax, _C_T3P, _C_BIO, grey("biomass", TEAL), shrinkB=46)
    _p_lab(ax, _C_T3P, _C_BIO, "2 T3P", grey("biomass", TEAL), dx=11, dy=0)
    _p_arrow(ax, _C_PYR, _C_ACE, AMBER, shrinkB=54)
    _p_lab(ax, _C_PYR, _C_ACE, "ackA", AMBER, dx=-2, dy=6)
    _p_lab(ax, _C_PYR, _C_ACE, "$+$1 ATP", AMBER, dx=-2, dy=13,
           size="caption")
    _p_arrow(ax, _C_PYR, _C_CO2, RED, shrinkB=42)
    _p_lab(ax, _C_PYR, _C_CO2, "tca", RED, dx=-2, dy=5)
    _p_lab(ax, _C_PYR, _C_CO2, "$+$3 ATP", RED, dx=-2, dy=-4,
           size="caption")

    if cut == "zwf":
        mx = (_C_G6P[0] + _C_P5P[0]) / 2
        my = (_C_G6P[1] + _C_P5P[1]) / 2
        ax.plot([mx - 4, mx + 4], [my - 5, my + 5], color=RED, lw=4.5, zorder=8)
        ax.plot([mx - 4, mx + 4], [my + 5, my - 5], color=RED, lw=4.5, zorder=8)
        ax.text(_C_BIO[0] + 15, _C_BIO[1], "biomass = 0", color=RED,
                fontsize=TYPE["body"], ha="left", va="center")
        ax.text(6, 22, "nothing else makes P5P,\nand biomass needs it",
                color=RED, fontsize=TYPE["caption"], ha="left", va="top")

    _save_pinned(fig, f"s20_cuts_{cut or 'none'}")


def _bind(fn, doc, **kw):
    """Name a parameterised figure so the build log and .deps.json read.

    tools/build_figures.py records `fn.__name__` as the generator and prints
    the one-line docstring. A bare lambda makes eleven of sixteen entries
    read "<lambda>" with "** NO DOCSTRING **", which wipes the provenance
    record for every figure added today.
    """
    f = functools.partial(fn, **kw)
    f.__name__ = fn.__name__ + "_" + "_".join(str(v) for v in kw.values())
    f.__doc__ = doc
    return f


FIGURES = [fig_network,
           _bind(fig_network, "The network with the written column beside "
                              "it, boxed in S.", annotate=True),
           fig_flux_map, fig_knockouts, fig_alternate_optima,
           *[_bind(fig_pathway, "Glycolysis and the pentose branch, "
                                f"revealed in {k} of 4 steps.", stage=k)
             for k in range(1, 5)],
           fig_overflow, fig_cone,
           *[_bind(fig_sixlines, f"Line {k} of the six-line solution, as a "
                                 "picture of one row of S.", step=k)
             for k in range(1, 6)],
           _bind(fig_cuts, "The network with biomass, intact.", cut=None),
           _bind(fig_cuts, "The network with zwf deleted.", cut="zwf")]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
