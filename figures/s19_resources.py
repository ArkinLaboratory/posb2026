"""Session 19 figures — the cell's economy, shared ribosomes, and burden.

Every curve that comes from a model comes out of `posb.resources`, the same
functions the students call. Every point that comes from a measurement carries
its source in `sessions/s19-resources/NUMBERS.md` and is drawn as a marker, not
a line, so the two kinds of thing never look alike on a slide.

What this session has to draw:

  * THE ECONOMY. `fig_growth_law` draws Scott's two growth laws. `fig_ribosome_budget`
    draws Bremer & Dennis's measured ribosome counts. **These are deliberately
    two figures on two axes** -- the conversion between the r-protein fraction
    they tabulate and Scott's phi_R could not be verified, so putting both on
    one axis would assert a reconciliation this course cannot source.
  * THE EDGE THAT IS NOT IN THE DIAGRAM. `fig_hidden_edge` -- induce one gene,
    watch an unconnected one fall, and the apparent dissociation constant of
    the phantom repressor moves with the reporter's own demand.
  * THE ISOCOST LINE. `fig_isocost` -- the achievable region is bounded by a
    straight line and the bound depends only on total demand.
  * THE PRICE. `fig_burden_cost` -- linear, with growth arrest at the ceiling.
    The slope is DERIVED from published fitted parameters and the figure says
    so on its face.
  * THE CLOSE. `fig_rate_balance` and `fig_bifurcation` -- a noncooperative
    positive feedback loop that is bistable anyway, because the nonlinearity
    is in the dilution. Setting the burden to zero removes it.

Run:  python tools/build_figures.py s19
"""
import numpy as np
from scipy.optimize import brentq

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           RULE, TYPE)
from posb import resources

plt = use()                 # the 20pt content floor, not LEGACY_SCALE
OUT = "figures/build"


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 1 . The economy
# ---------------------------------------------------------------------------
# Scott, Klumpp, Mateescu & Hwa, Mol Syst Biol 10:747 (2014), Eqs. 1-2 and the
# Fig. 2 legend. FITTED in Scott et al. 2010, cited there. See NUMBERS.md §1.
PHI_R_MIN = 0.07
C0 = 5.9                    # per hour
# Scott 2010 states BOTH of these and they are different quantities. An earlier
# version of this module treated them as rival estimates of one ceiling.
PHI_R_MAX = 0.55            # = rho * r_max, the maximum ribosomal allocation
PHI_C = 0.48                # = rho * (r_max - r_0), the zero-growth intercept
                            # for unnecessary protein (Scott 2010, Fig. 4)


def fig_growth_law():
    """The two growth laws, drawn so the disagreement in sign is the picture.

    REBUILT 25 October on Adam's note that this surface is critical and hard
    to follow. The previous version put both line families on one axis with a
    legend in the corner and nothing saying which way each arm is traversed,
    so the room saw crossing lines and no story.

    Three changes. Every line is labelled where it lives, not in a legend box
    the reader has to look up mid-sentence. Each arm carries an arrow saying
    what you DO to move along it. And the headroom above the ceiling is left
    empty so the conclusion can be stated in clear space instead of being
    inferred from two slopes.
    """
    lam = np.linspace(0, 2.6, 300)
    fig, ax = plt.subplots(figsize=(11.9, 4.6))

    # ---- the ceiling ------------------------------------------------------
    ax.axhline(PHI_R_MAX, color=RED, lw=2.4, ls=":", zorder=1)
    ax.text(2.56, PHI_R_MAX + 0.012, "$\\varphi_R^{max}$ = 0.55",
            color=RED, fontsize=TYPE["caption"], ha="right", va="bottom")

    # ---- law 1: change the food ------------------------------------------
    ax.plot(lam, PHI_R_MIN + lam / C0, color=TEAL, lw=3.8, zorder=4)
    ax.annotate("", xy=(2.34, PHI_R_MIN + 2.34 / C0),
                xytext=(1.80, PHI_R_MIN + 1.80 / C0),
                arrowprops=dict(arrowstyle="-|>", lw=3.0, color=TEAL,
                                mutation_scale=26), zorder=5)
    ax.text(2.30, 0.365, "richer medium",
            color=TEAL, fontsize=TYPE["caption"], ha="center", va="top")

    # ---- law 2: poison the ribosomes, from two different media -----------
    for i, (lam0, col) in enumerate([(1.8, CYAN), (1.0, AMBER)]):
        phi0 = PHI_R_MIN + lam0 / C0
        m = lam0 / (PHI_R_MAX - phi0)             # hits the ceiling at lambda=0
        ll = np.linspace(0, lam0, 80)
        ax.plot(ll, PHI_R_MAX - ll / m, color=col, lw=3.0, zorder=3)
        ax.plot([lam0], [phi0], "o", ms=14, color=col, zorder=6,
                markeredgecolor="white", markeredgewidth=1.6)
        xa, xb = lam0 * 0.62, lam0 * 0.30
        ax.annotate("", xy=(xb, PHI_R_MAX - xb / m),
                    xytext=(xa, PHI_R_MAX - xa / m),
                    arrowprops=dict(arrowstyle="-|>", lw=2.6, color=col,
                                    mutation_scale=24), zorder=5)
        # Both arms get labelled. Previously only one did, so nothing on
        # the page said the second arm was a second medium. Both labels sit
        # BELOW their arm -- above, the first one was struck through by the
        # dotted ceiling.
        # Hand-placed, not derived from the arrowhead: the two arms
        # converge at the ceiling, so labels hung off both arrowheads sit on
        # each other. The cyan one goes just under its own arm; the amber
        # one goes down into the empty wedge between the amber and teal
        # lines, which is the only clear space on this plot.
        if i == 0:
            ax.text(0.62, 0.478, "more chloramphenicol", color=col,
                    fontsize=TYPE["caption"], ha="left", va="top")
        else:
            ax.text(0.42, 0.340, "same drug, poorer medium", color=col,
                    fontsize=TYPE["caption"], ha="left", va="top")

    ax.plot([0], [PHI_R_MIN], "o", ms=12, color=TEAL, zorder=6)
    ax.text(0.04, 0.012, "$\\varphi_R^{min}$ = 0.07",
            color=TEAL, fontsize=TYPE["caption"], ha="left", va="bottom")
    # The branch point needs naming but every direction out of it is
    # occupied by a line, so the label goes to the empty lower-right and
    # points back.
    ax.annotate("one medium, no drug —\nwhere the two laws meet",
                xy=(1.82, PHI_R_MIN + 1.80 / C0 - 0.012),
                xytext=(2.52, 0.215), ha="right", va="top",
                color=INK, fontsize=TYPE["caption"],
                arrowprops=dict(arrowstyle="-", lw=1.6, color=MUTED,
                                shrinkA=4, shrinkB=8))

    # ---- the conclusion, in the empty band above the ceiling -------------
    # Wrapped and raised to the 20pt content floor, 26 October: this is the
    # figure's conclusion, not a source line, and at 16pt it also ran to
    # x = 12.35in and pushed the tight bbox past the 11.93in text column.
    ax.text(0.05, 0.775,
            "Two ways to slow this cell down — and they move\n"
            "the ribosome fraction in OPPOSITE directions.\n"
            "Starve it and ribosomes fall with growth.\n"
            "Poison the ribosomes and they rise as growth falls.",
            color=INK, fontsize=TYPE["body"], ha="left", va="top",
            linespacing=1.25)

    ax.set_xlabel("growth rate $\\lambda$   (h$^{-1}$)")
    ax.set_ylabel("ribosomal protein\nmass fraction $\\varphi_R$")
    ax.set_xlim(0, 2.6)
    ax.set_ylim(0, 0.82)
    _save(fig, "s19_growth_law")


# Bremer & Dennis, EcoSal Plus 3(1), 2008, doi:10.1128/ecosal.5.2.3, TABLE 3,
# "Parameters pertaining to the macromolecular synthesis rates in exponentially
# growing E. coli B/r as a function of growth rate at 37 C". Read off the PDF
# in private/readings/, 25 October.
#
# ALL FOUR ROWS HERE REPLACE TRANSCRIBED VALUES THAT WERE WRONG. The previous
# numbers came from page scans we no longer have and disagreed with the
# published table in every row, with a pattern: our mu = 2.5 entries matched
# the table's mu = 3.0 column and our r-protein row matched the next column
# along throughout. It was read off by one column. The old values were
#   ribosomes  6.8, 13.5, 26.3, 45.1, 72.0   (table: 8, 15, 26, 44, 61, 73)
#   r-protein  9.0, 11.0, 13.5, 18.0, 21.6   (table: 7.7, 9.2, 11.6, 15, 18.8, 22.7)
#   activity   80% flat                      (table: 85% flat)
#   elongation 12, 16, 18, 20, 21            (table: 13, 18, 21, 22, 22, 22)
BD_MU = np.array([0.6, 1.0, 1.5, 2.0, 2.5, 3.0])           # doublings/h
BD_RIBOSOMES = np.array([8, 15, 26, 44, 61, 73])           # x10^3 per cell, N_r
BD_RPROTEIN = np.array([7.7, 9.2, 11.6, 15.0, 18.8, 22.7])  # % total protein, alpha_r
BD_PPGPP = np.array([55, 38, 22, 15, 10, 6])               # pmol/OD460, ppGpp/M
BD_RRN_INIT = np.array([4, 10, 20, 37, 54, 68])            # init/min/gene, i_rrn


def fig_ribosome_budget():
    """What a cell actually owns, as a function of how fast it is growing."""
    lam = BD_MU * np.log(2)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.9, 4.5))

    a1.plot(lam, BD_RIBOSOMES, "o-", ms=13, lw=3.0, color=TEAL)
    a1.set_xlabel("growth rate   (h$^{-1}$)")
    a1.set_ylabel("ribosomes per cell\n(thousands)")
    a1.set_xlim(0, 2.20)
    a1.set_ylim(0, 80)
    # Checked against the table, not asserted: mu 0.6 -> 3.0 is 5x, and
    # ribosomes 8 -> 73 is 9.1x. The old caption said "4x / 10x" and neither
    # number was in the data it was drawn over.
    a1.text(0.06, 74, "a 5× change in growth rate,\na 9× change in ribosomes",
            color=INK, fontsize=TYPE["caption"], va="top")

    a2.plot(lam, BD_RPROTEIN, "o-", ms=13, lw=3.0, color=GREEN)
    a2.set_xlabel("growth rate   (h$^{-1}$)")
    a2.set_ylabel("ribosomal protein\n(% of total protein)")
    a2.set_xlim(0, 2.20)
    a2.set_ylim(0, 25)
    a2.text(0.06, 23.2, "measured, E. coli B/r at 37 °C\n"
                        "Bremer & Dennis, EcoSal Plus 2008, Table 3",
            color=MUTED, fontsize=TYPE["caption"], va="top")
    _save(fig, "s19_ribosome_budget")


def fig_ppgpp_mechanism():
    """The controller as OBJECTS, before the words get used as vocabulary.

    Added 25 October. The ppGpp surface named uncharged tRNA, an alarmone,
    and rRNA synthesis in a causal chain without any of those things having
    been drawn, which is rule 1 and the worst bimodality failure in the deck:
    a physicist or a chemical engineer reads four unfamiliar nouns and loses
    the answer to the question the growth-law surface just asked.

    Two chains, same machinery, opposite directions. The mechanism is from
    Scott et al. 2014, p. 6; the drawing is ours.
    """
    from matplotlib.patches import FancyBboxPatch
    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 4.4); ax.axis("off")
    # tight_layout leaves this axis-free diagram with the default
    # subplot margins, so 10.4 data units were squeezed into about
    # half the canvas and every box overflowed its text.
    ax.set_position([0.006, 0.0, 0.988, 1.0])

    # Widened 26 October when FS went from 13 to the 20pt floor: at 1.84
    # units 'rRNA synthesis' and 'MORE ribosomes,' overflowed their boxes.
    # 5 boxes + 4 gaps + 2 x 0.07 inset = 10.4 exactly.
    W_, H_, G = 1.94, 0.98, 0.145
    xs = [0.07 + i * (W_ + G) for i in range(5)]
    # 13pt was below even the 16pt caption role, on the figure that exists
    # because this chain was unreadable. Raised to the 20pt content floor,
    # 26 October; the boxes were already sized in data units so they grow
    # with it.
    FS = TYPE["body"]

    def box(x, y, txt, edge):
        ax.add_patch(FancyBboxPatch((x, y), W_, H_,
                     boxstyle="round,pad=0.05", linewidth=2.4,
                     edgecolor=edge, facecolor="white", zorder=3))
        ax.text(x + W_ / 2, y + H_ / 2, txt, ha="center", va="center",
                fontsize=FS, color=INK, zorder=4, linespacing=1.25)

    def chain(y, head, head_col, labels, col, blunt_after=None):
        ax.text(0.07, y + H_ + 0.26, head, color=head_col,
                fontsize=TYPE["caption"], weight="bold", ha="left")
        for i, (x, L) in enumerate(zip(xs, labels)):
            box(x, y, L, col)
            if i < len(labels) - 1:
                ax.annotate("", xy=(x + W_ + G, y + H_ / 2),
                            xytext=(x + W_, y + H_ / 2), zorder=2,
                            arrowprops=dict(
                                arrowstyle=("-[, widthB=0.52, lengthB=0.22"
                                            if i == blunt_after else "-|>"),
                                lw=2.6, color=col, mutation_scale=34
                                if i == blunt_after else 20))

    chain(2.86, "RUN SHORT OF AMINO ACIDS", RED,
          ["amino acids\nrun short", "tRNA sits in\nthe ribosome,\nUNCHARGED",
           "ppGpp  UP", "rRNA synthesis\nrepressed",
           "fewer\nribosomes"], RED, blunt_after=2)

    # "amino acids fine" understated the mechanism and was the wrong sign.
    # Scott 2010 p. 1100: the response is "in response to the buildup of
    # intracellular amino acid pools resulting from slow translation" -- the
    # pools RISE, and the rise is what drives ppGpp down. Corrected
    # 26 October after the F4.5 review.
    chain(0.52, "OR POISON THE RIBOSOMES INSTEAD", TEAL,
          ["antibiotic slows\ntranslation",
           "amino acids\nbuild up,\ntRNA CHARGED", "ppGpp  DOWN",
           "rRNA synthesis\nreleased", "MORE\nribosomes,\nidling"],
          TEAL)

    # Two lines, 26 October. As one line this ran past the axes and
    # savefig.bbox="tight" grew the PNG to 13.46in on a 13.33in slide, so the
    # closing "(flat bar = represses)" -- which tells the room how to read the
    # glyph -- was cut off the right edge.
    ax.text(5.2, 2.40,
            "the cell never measures its own growth rate —\n"
            "it measures whether a charged tRNA is ready",
            ha="center", va="center", fontsize=TYPE["body"], color=MUTED,
            linespacing=1.25)
    ax.text(5.2, 1.98, "flat bar = represses",
            ha="center", va="center", fontsize=TYPE["caption"], color=MUTED)
    fig.savefig(f"{OUT}/s19_ppgpp_mechanism.png")
    plt.close(fig)


def fig_ppgpp():
    """The controller, measured: ppGpp down, rRNA initiation up."""
    lam = BD_MU * np.log(2)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.9, 4.5))

    a1.plot(lam, BD_PPGPP, "o-", ms=13, lw=3.0, color=RED)
    a1.set_xlabel("growth rate   (h$^{-1}$)")
    a1.set_ylabel("ppGpp\n(pmol / OD$_{460}$)")
    a1.set_xlim(0, 2.20)
    a1.set_ylim(0, 60)
    a1.set_title("the alarm signal", fontsize=TYPE["body"], color=INK)
    a1.text(0.80, 52, "9× DOWN", color=RED, fontsize=TYPE["body"], weight="bold")

    a2.plot(lam, BD_RRN_INIT, "o-", ms=13, lw=3.0, color=TEAL)
    a2.set_xlabel("growth rate   (h$^{-1}$)")
    a2.set_ylabel("initiations per minute\nat each rRNA gene")
    a2.set_xlim(0, 2.20)
    a2.set_ylim(0, 75)
    a2.set_title("what it is holding down", fontsize=TYPE["body"], color=INK)
    a2.text(0.12, 66, "17× UP", color=TEAL, fontsize=TYPE["body"], weight="bold")
    # No in-plot attribution on this panel: the rising curve runs through the
    # only space it would fit, and the slide foot already carries the source.
    _save(fig, "s19_ppgpp")


# ---------------------------------------------------------------------------
# 2 . The edge that is not in the diagram
# ---------------------------------------------------------------------------
def fig_hidden_edge():
    """Induce gene 2; gene 1 falls. And the phantom repressor's K moves."""
    d2 = np.logspace(-2, 2, 500)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.9, 4.5))

    # left: the fall itself, at one demand for gene 1
    d1 = 1.0
    p1 = np.array([resources.expression([d1, x])[0] for x in d2])
    alone = resources.expression([d1, 0.0])[0]
    a1.plot(d2, p1 / alone, color=TEAL, lw=3.4)
    a1.axhline(1.0, color=RULE, lw=2.0)
    for x, lab in [(1.0, "−33%"), (4.0, "−67%"), (16.0, "−89%")]:
        y = resources.expression([d1, x])[0] / alone
        a1.plot([x], [y], "o", ms=12, color=AMBER, zorder=6)
        a1.annotate(lab, xy=(x, y), xytext=(x, y + 0.14), color=AMBER,
                    fontsize=TYPE["caption"], ha="center")
    a1.set_xscale("log")
    a1.set_xlabel("demand of gene 2")
    a1.set_ylabel("gene 1 output\n(relative to gene 2 absent)")
    a1.set_ylim(0, 1.15)
    a1.set_title("no wire between them", fontsize=TYPE["body"], color=INK)

    # right: the apparent K moves with the reporter's OWN demand, which is the
    # signature that distinguishes this from regulation
    for dd, col in [(0.2, CYAN), (1.0, TEAL), (5.0, AMBER)]:
        pp = np.array([resources.expression([dd, x])[0] for x in d2])
        al = resources.expression([dd, 0.0])[0]
        K = resources.apparent_K(dd)
        a2.plot(d2, pp / al, color=col, lw=3.0,
                label=f"$d_1$ = {dd:g}   $K_{{app}}$ = {K:g}")
        a2.plot([K], [0.5], "v", ms=14, color=col, zorder=6)
    a2.axhline(0.5, color=RULE, lw=2.0)
    a2.set_xscale("log")
    a2.set_xlabel("demand of gene 2")
    a2.set_ylabel("gene 1 output\n(fraction of its own max)")
    a2.set_ylim(0, 1.15)
    # upper right: every curve has fallen to near zero there. The first build
    # put this lower left, where the legend covered all three curves and a
    # marker sat on top of a legend label.
    a2.legend(loc="upper right", fontsize=TYPE["caption"])
    a2.set_title("a real repressor's $K$ would not move",
                 fontsize=TYPE["body"], color=INK)
    _save(fig, "s19_hidden_edge")


# ---------------------------------------------------------------------------
# 3 . The isocost line
# ---------------------------------------------------------------------------
def fig_isocost():
    """The achievable region, bounded by a straight line it never reaches."""
    fig, ax = plt.subplots(figsize=(11.9, 4.6))

    # the frontier: every split of a fixed total demand
    # 100 was indistinguishable from the bound it is supposed to approach,
    # so the figure showed four lines and promised five. 30 is visibly inside.
    for total, col in [(1.0, MUTED), (3.0, CYAN), (10.0, TEAL), (30.0, AMBER)]:
        fr = np.linspace(0.001, 0.999, 300)
        pts = np.array([resources.expression([total * f, total * (1 - f)])
                        for f in fr])
        ax.plot(pts[:, 0], pts[:, 1], color=col, lw=3.0,
                label=f"total demand {total:g}")

    # NOT an isocost line. Each SOLID line is an isocost line -- one fixed
    # total demand (Gyorgy Eq. 1: alpha*p1 + beta*p2 = Y, one budget Y). This
    # dashed line is the limit the family approaches as the total demand goes
    # to infinity, and labelling it "the isocost line" contradicted both the
    # slide foot and the paper. Found in review, 25 October.
    ax.plot([0, 1], [1, 0], color=RED, lw=2.8, ls="--",
            label="the bound as total demand $\\to\\infty$")
    # The identity p1 + p2 = (sum d)/(1 + sum d) is only true against the
    # SATURATING maximum, so the axes have to say that is what 1.0 means.
    ax.set_xlabel("gene 1 output   (fraction of what it makes alone,\n"
                  "at unlimited demand)")
    ax.set_ylabel("gene 2 output\n(same normalisation)")
    ax.set_xlim(0, 1.26)
    ax.set_ylim(0, 1.06)
    # NO equal aspect: it squeezed the axes into a square and shrank the whole
    # figure to 40% of the slide width. The claim here is that the frontiers
    # are straight and parallel, which does not need a 45 degree slope.
    # Everything ABOVE the dashed line is unreachable, so the legend goes there.
    ax.legend(loc="upper right", fontsize=TYPE["caption"])
    _save(fig, "s19_isocost")


# ---------------------------------------------------------------------------
# 4 . The price of a useless protein
# ---------------------------------------------------------------------------
def fig_burden_cost():
    """Linear, to arrest at the ceiling. The slope is DERIVED, and it says so."""
    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    # ONE line. An earlier build drew two, labelled "phi_R^max = 0.55 (Scott
    # 2014)" and "phi_R^max = 0.48 (Mori 2017)", as if they were rival
    # estimates of one quantity. Reading Scott 2010 itself showed they are two
    # DIFFERENT quantities: phi_R^max = rho*r_max ~ 0.55 is the ribosomal
    # ceiling, and phi_c = rho*(r_max - r_0) ~ 0.48 is the zero-growth
    # intercept for unnecessary protein. It is phi_c that governs this curve,
    # and Scott 2010 states it. The same build also printed the per-percent
    # loss 100x too large.
    phi = np.linspace(0, PHI_C, 200)
    per_percent = 0.01 / PHI_C
    ax.plot(100 * phi, 1 - phi / PHI_C, color=TEAL, lw=3.6,
            label=(f"$\\lambda/\\lambda_0 = 1 - \\varphi_U/\\varphi_c$,   "
                   f"$\\varphi_c$ = {PHI_C:g}   →  {per_percent:.1%} of "
                   f"$\\lambda$ per 1%"))
    ax.plot([100 * PHI_C], [0], "o", ms=14, color=TEAL, zorder=6)
    # Two annotations were tried here and both collided with the line and with
    # each other. The "growth stops at 48%" callout is cut rather than moved:
    # the marker already sits at 48 on the axis and the legend already carries
    # phi_c. Cut the text first, loosen geometry second.
    ax.set_xlabel("proteome given to an unnecessary protein,  $\\varphi_U$   (%)")
    ax.set_ylabel("growth rate\n(fraction of unburdened)")
    ax.set_xlim(0, 58)
    ax.set_ylim(0, 1.06)
    ax.legend(loc="upper right", fontsize=TYPE["caption"])
    # The per-percent figure appears NOWHERE in Scott 2010 or Scott 2014 --
    # checked against both PDFs, 25 October. It is 0.01/0.48 and it has to say
    # so, because it sits in the legend next to a number that IS theirs.
    ax.text(1.5, 0.05,
            "Linear form and $\\varphi_c$ = 0.48 are stated in Scott et al. 2010\n"
            "(Eq. 6, Fig. 4B). The 2.1% per 1% is our arithmetic: 0.01/0.48.",
            color=MUTED, fontsize=TYPE["caption"], va="bottom", ha="left")
    _save(fig, "s19_burden_cost")


# ---------------------------------------------------------------------------
# 5 . The close: emergent bistability
# ---------------------------------------------------------------------------
# Tan, Marguet & You, Nat Chem Biol 5:842 (2009), in the form published by
# Ochab-Marcinek, Eur Phys J E (2012), arXiv:1108.3720 Eq. 1, whose parameters
# that paper states are those of Tan et al. SECONDARY provenance -- see
# NUMBERS.md §6. What is shown is the MECHANISM, not a replication.
DELTA, PHI = 0.01, 20.0
GAMMA = 10.0


def production(x, alpha):
    """Expression. Hill-1 in x: NO cooperativity anywhere in this term."""
    return (DELTA + alpha * x) / (1.0 + x)


def removal(x, gamma=GAMMA):
    """Dilution by growth, plus degradation. The burden makes it saturate."""
    return PHI * x / (1.0 + gamma * x) + x


def _fixed_points(alpha, gamma=GAMMA, hi=40.0, n=120000):
    xs = np.linspace(1e-12, hi, n)
    f = production(xs, alpha) - removal(xs, gamma)
    out = []
    for i in np.where(np.sign(f[:-1]) != np.sign(f[1:]))[0]:
        out.append(brentq(lambda z: production(z, alpha) - removal(z, gamma),
                          xs[i], xs[i + 1], xtol=1e-14))
    return out


def _is_stable(x, alpha, gamma=GAMMA, eps=1e-7):
    g = lambda z: production(z, alpha) - removal(z, gamma)
    return (g(x + eps) - g(x - eps)) / (2 * eps) < 0


def fig_rate_balance():
    """Three crossings with the burden, one without. The controlled test.

    Annotation rebuilt 25 October. Everything is placed in AXES coordinates,
    because the previous version positioned text in data coordinates on a
    log axis and it walked off the panel the moment the legend resized it.
    Two substantive changes as well: the y-axis says what rate it is a rate
    OF, and the figure now states why a crossing is or is not stable --
    without that the filled/open discs are a convention nobody can check.
    """
    # LOG-LOG, and not by preference: the three steady states at alpha = 14 sit
    # at x = 0.0015, 0.062 and 10.8. On a linear axis the two low ones land in
    # the same pixel and the figure's whole claim -- that there are three --
    # is invisible. The first build was linear and showed two.
    x = np.logspace(-3.4, 1.3, 4000)
    alpha = 14.0
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.9, 4.5))

    for ax, gamma, title in [(a1, GAMMA, "with burden  (γ = 10)"),
                             (a2, 0.0, "burden removed  (γ = 0)")]:
        ax.plot(x, production(x, alpha), color=TEAL, lw=3.2)
        ax.plot(x, removal(x, gamma), color=AMBER, lw=3.2)
        for pnt in _fixed_points(alpha, gamma):
            stable = _is_stable(pnt, alpha, gamma)
            ax.plot([pnt], [production(pnt, alpha)], "o", ms=15,
                    mfc=(RED if stable else "white"), mec=RED, mew=3.0,
                    zorder=7)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("T7 RNAP*  (x)")
        ax.set_xlim(4e-4, 20)
        ax.set_ylim(5e-3, 40)
        ax.set_title(title, fontsize=TYPE["body"], color=INK)
        # Curves labelled where they are, with the expression each one is.
        rem = "φx/(1 + γx) + x" if gamma else "φx + x"
        ax.text(0.03, 0.97, "MADE      (δ + αx)/(1 + x)", color=TEAL,
                fontsize=TYPE["caption"], ha="left", va="top",
                transform=ax.transAxes)
        ax.text(0.03, 0.88, f"REMOVED   {rem}", color=AMBER,
                fontsize=TYPE["caption"], ha="left", va="top",
                transform=ax.transAxes)

    a1.set_ylabel("made or removed\nper unit time")
    # The right panel had tick labels and no axis name. On a figure whose
    # whole point is that both curves are rates OF THE SAME THING, that is a
    # tutorial gap for the half of the room that is not biologists.
    a2.set_ylabel("made or removed\nper unit time")
    # A crossing is a steady state. It is NOT by itself evidence that anything
    # is stable -- that comes from which curve is steeper there. Added on
    # Adam's note, 25 October: "the crossing isn't evidence".
    a1.text(0.97, 0.02, "three crossings", color=RED,
            fontsize=TYPE["caption"], ha="right", va="bottom",
            transform=a1.transAxes)
    a2.text(0.97, 0.02, "one crossing", color=RED,
            fontsize=TYPE["caption"], ha="right", va="bottom",
            transform=a2.transAxes)
    _save(fig, "s19_rate_balance")


def fig_bifurcation():
    """The window in alpha, and what is lost at each edge."""
    alphas = np.linspace(3.0, 22.0, 440)
    fig, ax = plt.subplots(figsize=(11.9, 4.6))
    for a in alphas:
        for p in _fixed_points(a):
            stable = _is_stable(p, a)
            ax.plot([a], [max(p, 1e-4)], ".",
                    ms=7 if stable else 5,
                    color=(TEAL if stable else MUTED))
    ax.set_yscale("log")
    ax.set_xlabel("α   (effective synthesis rate)")
    ax.set_ylabel("steady states  (x)")
    ax.set_xlim(3, 22)
    # Headroom for the construction note, which now sits at the 20pt content
    # floor and is 5 lines tall. At ylim 4000 the block overlapped the upper
    # stable branch; 2e4 clears it. The dead band above the curve is
    # deliberate -- it is the text's room, not wasted axis.
    ax.set_ylim(3e-4, 2e4)
    # axvline spans the whole axes, so it struck through the explanatory
    # block and both edge labels. Draw the markers to a ceiling instead and
    # keep the band above them clear.
    for a_c in (5.575, 18.425):
        ax.plot([a_c, a_c], [3e-4, 60.0], color=RED, lw=2.2, ls="--",
                zorder=2)
    ax.text(6.1, 2.2e-3, "ON state\nis born", color=RED,
            fontsize=TYPE["caption"], va="bottom", ha="left")
    ax.text(17.9, 2.2e-3, "OFF state\nis destroyed", color=RED,
            fontsize=TYPE["caption"], va="bottom", ha="right")
    # Where this curve comes from, on the figure. Without it the S-curve is
    # an assertion and the dashed lines are decoration -- Adam, 25 October:
    # "unclear where the nullcline comes from and why there is a saddle
    # node ... the crossing isn't evidence."
    # Short, hand-wrapped, and in AXES coordinates. A long line in data
    # coordinates runs past xlim and matplotlib widens the saved canvas to
    # fit it, which squashed the plot into a column. The full construction
    # argument lives on the slide and in its notes.
    # "each dot" described a scatter; these render as continuous curves.
    # HARD-WRAPPED, 26 October. These three lines ran to x = 14.62in on an
    # 11.90in figure, and savefig.bbox="tight" widened the saved canvas to
    # 14.32in -- so _fig centred a 14.52in PNG on a 13.33in slide at
    # x = -0.59in and the y-axis label, the tick labels and the end of this
    # very sentence were cut off the page. Keep every line under about 52
    # characters, and raise the size: this carries the argument, so it belongs
    # at the 20pt content floor, not at the 16pt caption size.
    ax.text(0.015, 0.985,
            "each point is one crossing of the\n"
            "made-against-removed picture, at one α\n"
            "at the dashed lines two crossings merge and\n"
            "vanish: the curves have gone tangent",
            color=INK, fontsize=TYPE["body"], ha="left", va="top",
            linespacing=1.25, transform=ax.transAxes)
    # Top-right. Bottom-right looked empty and is not -- the OFF branch runs
    # along the floor out to the second saddle-node and the key landed on it.
    # Above the ON branch there is real space, because ylim was raised to
    # carry the construction note.
    ax.text(0.985, 0.985, "solid = stable      faint = unstable",
            color=MUTED, fontsize=TYPE["body"], ha="right", va="top",
            transform=ax.transAxes)
    _save(fig, "s19_bifurcation")


FIGURES = [fig_growth_law, fig_ribosome_budget,
           fig_ppgpp_mechanism, fig_ppgpp,
           fig_hidden_edge, fig_isocost,
           fig_burden_cost, fig_rate_balance, fig_bifurcation]


if __name__ == "__main__":
    print("isocost sum at total demand 10:", resources.isocost_sum([5.0, 5.0]))
    for a in (5.0, 8.0, 14.0, 18.0, 19.0):
        fp = _fixed_points(a)
        print(f"alpha={a:<5} ", [(round(p, 5), _is_stable(p, a)) for p in fp])
