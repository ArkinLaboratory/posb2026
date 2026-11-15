"""Session 25 figures -- design at population scale.

ONE MODEL PER FIGURE, AND THE MODEL IS NAMED ON THE FIGURE (session 21's rule,
kept by 22 and 23). This session has two models that produce the same binomial
and a different answer -- W03's burst SCALES as (1+P)^2, a capped burst
PARTITIONS a fixed n -- so every figure says which one drew it.

Every curve comes out of `posb.populations`, the same functions PS9 imports,
AND THERE IS NO LONGER AN EXCEPTION. `fig_setpoint_valley` needs the full
six-compartment COEXISTENCE EQUILIBRIUM of equations [1]-[6]; that solver was
moved into the library on 9 November 2026 and is imported here as
`posb.populations.coexistence`. PS9's autograder imports the same function,
because a figure and an autograder solving one steady state two different ways
is a defect waiting for the first student who checks.

W03'S PANELS ARE NOT REDRAWN HERE. Figs. 1, 2a, 2b, 2c and 3 go on slides as
PAPER FIGURES with their own attribution. The one exception is
`fig_design_space`, whose right panel replots the RED/CYAN STABILITY BOUNDARY
read off the floor of W03 Fig. 3a -- a model boundary, not a measurement,
digitized by us and disclosed as such on the figure. The brief asks for that
comparison explicitly, because W03 says it checked the closed form against
that floor only in a supplement nobody here has.

WHAT THE DIGITIZATION FOUND, and it is the point of that figure. Our analytic
contour P^2*D = 2.0667 and their floor boundary have the same shape and the
same scale, and they are not the same curve: over D = 0.08 to 0.20 their
boundary sits at P^2*D = 1.14 to 1.29, and over D = 0.35 to 0.50 it rises to
2.15 to 3.86, crossing ours near D = 0.35. The coefficient band -- 1 - 1/R0
runs 0.47 to 0.95 over R0 in [1.9, 20], so the threshold runs 1.05 to 2.11 --
contains their boundary for D below about 0.35 and not above it. A slide that
printed one sharp contour and claimed the simulation agreed would be
overclaiming in both directions. See the module's W03_FIG3A_FLOOR table.

AND SINCE 7 NOVEMBER THAT IS A FINDING ABOUT THEIR FIGURE, NOT ABOUT OUR
ALGEBRA. NUMBERS.md 18 re-derives R0_T from equations 4-6 by a
next-generation matrix and gets P^2*D*(1 - 1/R0) three independent ways --
symbolically, by the sign of the leading eigenvalue of the full 6x6 Jacobian
at 352 points, and by integrating the nonlinear system -- with the threshold
at exactly 31/15 = 2.0666666667, and bisecting that eigenvalue with no
formula at all returns the same number at D = 0.01, 0.2, 0.4 and 1.0. The
closed form is settled. What the right-hand panel shows is that W03's own
Fig. 3a floor does not sit on it.

Numbers on these figures are in sessions/s25-populations/NUMBERS.md with their
kind, and each figure prints the kind where it matters. NOTHING HERE IS
MEASURED. n = 200 and the other burst sizes are QUOTED -- W03 takes 200 from
Haase 1996 for a SINGLY HIV-1-infected cell (NUMBERS.md 4c, p.4) and measures
nothing itself; it is a theory paper. Calling n = 200 a measurement OF THIS
MODEL, which an earlier draft of this docstring and of `fig_burst_ledger`'s
teal label both did, attaches somebody else's experiment to an assumption and
to a different object: the axis those figures carry reads "virions from one
I_D cell", and Haase counted a singly infected one.

Run:  python tools/build_figures.py s25
"""
import io

import numpy as np

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           MINT, RULE, TYPE)
from posb.populations import (diploid_packaging, infectious_fraction,
                              heterozygote_waste, burst_output, basic_R0,
                              therapeutic_R0, P_min, D_min,
                              coexistence as _coexistence)

plt = use()
OUT = "figures/build"

# -- the hour's pinned parameter set -------------------------------------
# Table 1 as printed (NUMBERS.md 2), with c = 30 and R0 = 1.9375 pinned for
# every item and every figure. The footnote's c = 3 gives T* = 80 against a
# stated T0 = 800 and cannot be used without rescaling k.
LAM, KINF, NBURST, CLEAR, DUNINF, DELTA = 31.0, 1.875e-4, 200.0, 30.0, 0.02, 0.7
R0 = basic_R0(LAM, KINF, NBURST, CLEAR, DUNINF)        # 1.9375, COMPUTED
R0_PRINTED = basic_R0(LAM, KINF, NBURST, CLEAR, DELTA)  # 0.0554, the slip
T_HEALTHY = LAM / DUNINF                                # 1550 cells/ul
D_FIG = 0.4         # MODELLED, Fig. 3b caption and Fig. 2a caption
P_HEAD = 100.0      # MODELLED, Fig. 3b's HAART-comparable design point
# The coefficient band the threshold is a band BECAUSE of. NUMBERS.md 5b.
R0_LO, R0_HI = 1.9, 20.0

# EVERY piece of text inside a figure is content the room has to read, so it
# sits at the body floor. TYPE["caption"] inside a figure is for a literature
# citation and nothing else.
LBL = TYPE["body"]
PAGE = "#F8FAF9"


def _plate(pad=0.3):
    """Page-colored backing for a label that sits over plotted data."""
    return dict(facecolor=PAGE, edgecolor="none", pad=pad)


def _tag(ax, x, y, s, color, ha="left", va="bottom", plate=True, size=None):
    """A short label beside the curve it names, in axes fractions.

    `size` is for ONE thing: a literature citation, at TYPE["caption"].
    Everything else on these figures is content and sits at the body floor.
    """
    ax.text(x, y, s, transform=ax.transAxes, color=color, fontsize=size or LBL,
            ha=ha, va=va, bbox=_plate() if plate else None, zorder=7)


# -- PLACEMENT COMES FROM THE DECK, AND FROM NOWHERE ELSE ------------------
# This guard used to carry its own two bands: 5.40 x 4.95 in for the step
# panels and image_centered's 10.2 x 4.60 in default for everything else. The
# deck uses NEITHER for the two panels it places explicitly -- it writes
# `d.image(s, ..., 4.76, 4.30)` for `s25_urn_6` and `s25_chain_5` -- and its
# `image_centered` calls pass a `band=` per figure rather than the default.
# So the guard and the deck were each self-consistent, agreed with each
# other nowhere, and the figures were shrunk anyway while this printed
# nothing. deck-bar D5a item 5 is a size guard committing the error it was
# written to catch, and a guard measuring a box nobody used is the same
# defect wearing a different hat.
#
# tools/figure_fit.py ALREADY parses every deck's `image` / `image_centered`
# call, so that parser is reused rather than copied: one source of truth, and
# when it cannot read a placement this says so instead of substituting a
# reassuring default. STEP_FIG below is the canvas these panels are AUTHORED
# on; it is not a claim about where they land.
_PLACEMENTS = None


def _deck_placements():
    """stem -> (max_w_in, box_h_in), read from the decks by figure_fit."""
    global _PLACEMENTS
    if _PLACEMENTS is None:
        try:
            from tools.figure_fit import _placements
            _PLACEMENTS = _placements()
        except Exception as exc:                  # noqa: BLE001
            print(f"  !! could not read the decks' placement calls ({exc}) "
                  f"-- NO figure's type floor is checked in this run")
            _PLACEMENTS = {}
    return _PLACEMENTS


def _written_size(fig, **kw):
    """The size savefig ACTUALLY writes, in inches, read back from the bytes.

    Not `get_size_inches()` and not `get_tightbbox()` plus an assumed pad:
    `bbox_inches="tight"` crops, `pad_inches` may or may not be added, and
    deck-bar D5a item 5 is this function's predecessor reporting 5.36 x 4.90
    for a file that was 4.76 x 4.30. Render the same call into a buffer and
    measure the PNG header. It also works under `tools/figure_fit.py`, which
    hooks `Figure.savefig` and writes nothing -- a buffer has no name, so the
    hook passes it straight through to the real savefig.
    """
    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", **kw)
    buf.seek(0)
    iw, ih = Image.open(buf).size
    dpi = float(plt.rcParams["savefig.dpi"])
    return iw / dpi, ih / dpi


def _report(name, w, h):
    """Say what the deck's own box does to this file's type.

    `theme.image(x, y, bw, bh)` fits the PNG inside (bw, bh) preserving
    aspect, and `image_centered(band=b)` does the same inside (10.2, b), so
    the projected scale is min(bw, bh * aspect) / w -- which, for any figure
    the width does not bind, is just bh / h. The floor is the body size,
    because every piece of text in these figures is at it.
    """
    box = _deck_placements().get(name)
    if box is None:
        print(f"  ?? {name}: saved {w:.3f} x {h:.3f} in -- no deck call "
              f"places it, so the type floor is NOT checked here")
        return None
    bw, bh = box
    scale = min(bw, bh * (w / h)) / w
    if LBL * scale < LBL - 0.5:
        print(f"  !! {name}: saved {w:.3f} x {h:.3f} in into the deck's "
              f"{bw:.2f} x {bh:.2f} in box -- scale {scale:.3f}, so {LBL} pt "
              f"lands at {LBL * scale:.1f} pt, under the {LBL} pt floor. "
              f"Re-author the panel or raise the deck's box; do NOT shrink "
              f"the type (deck-gauntlet 5.3)")
    return scale


def _settle(fig, passes=6):
    """Run `tight_layout` to its fixed point, not once.

    `tight_layout` is content-dependent (deck-gauntlet 5.2) and on an
    aspect-equal axes it is not idempotent: the first call insets from the
    tight bbox, the aspect then re-fits the box, and the next call sees a
    different bbox. The locus plate (measured under the transitional stem
    `s25_locus_alleles`, since retired; the same drawing is now
    `s25_locus_2`) ran 0.853 -> 0.8239 -> 0.8181 -> 0.8170 of the figure
    width over four passes. `tools/figure_fit.py` calls
    it once more before measuring, so the geometry the gate scored was 3.4%
    narrower than the PNG on disk -- it could report a collision the file
    does not have, and worse, hide one it does. Settling here means the gate
    measures what was saved, which is the whole of deck-bar D5a.
    """
    last = None
    for _ in range(passes):
        fig.tight_layout()
        now = tuple(round(v, 5) for ax in fig.axes
                    for v in ax.get_position().bounds)
        if now == last:
            return
        last = now


def _save(fig, name, fixed=False):
    """Write one PNG and say what the DECK's own box does to its type.

    `fixed=True` is the step-panel path, and it does NOT write at figsize.
    `bbox_inches=None` is indistinguishable from the argument being absent,
    so matplotlib falls back to rcParams["savefig.bbox"], which this repo
    sets to "tight". An earlier version of this function believed it was
    writing a fixed canvas and reported `get_size_inches()`: the PNG on disk
    was 4.76 x 4.30 in while the guard printed 5.36 x 4.90. That is the
    measurement error deck-bar D5a is about, committed by the check meant to
    catch it, so the size is now read back from the bytes savefig writes.

    No band is passed in. The box is whatever the deck's own `image` /
    `image_centered` call says, read by `_report`; a figure no deck places
    is reported as unchecked rather than measured against a default.

    The panels still come out identical to one another, which is what a
    derivation series needs -- not because the canvas is pinned but because
    every label fits inside the axes, so the tight bbox IS the axes box and
    `tight_layout` puts that in the same place every time. A label that
    outgrows the axes breaks that, and is reported.
    """
    _settle(fig)                    # see _settle: the gate measures the fixed point
    kw = dict(pad_inches=0) if fixed else {}
    if fixed:
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        ab = fig.axes[0].get_window_extent()
        for ax in fig.axes:
            for t in list(ax.texts) + [ax.title]:
                if not t.get_text().strip():
                    continue
                bb = t.get_window_extent(r)
                over = max(ab.x0 - bb.x0, bb.x1 - ab.x1,
                           ab.y0 - bb.y0, bb.y1 - ab.y1)
                if over > 1:
                    print(f"  !! {name}: {t.get_text()[:40]!r} runs "
                          f"{over:.0f} px outside the axes, so this panel "
                          f"crops to a different size from its siblings and "
                          f"the picture moves between steps")
    w, h = _written_size(fig, **kw)
    _report(name, w, h)
    fig.savefig(f"{OUT}/{name}.png", **kw)
    plt.close(fig)
    return w, h           # a series compares its stages against these bytes


# =====================================================================
# SEGMENT 2 -- the urn fills as the algebra advances. T67.
#
# theme.derivation_fig() places these in a 5.4 x 4.95 in column beside the
# step stack, so they are drawn on a FIXED 5.30 x 4.50 in canvas: inside that
# column, inside figure_fit's 4.60 in band, and identical from step to step
# so the picture does not jump while the algebra moves.
# =====================================================================

STEP_FIG = (5.36, 4.90)
YMAX = 10.0
XMAX = YMAX * STEP_FIG[0] / STEP_FIG[1]        # equal x and y units
CX = XMAX / 2.0
P_DRAW = 3.0          # the urn is drawn at P = 3: one HIV-1, three crHIV-1
_HIV, _VEC = AMBER, TEAL


def _panel():
    """A fixed canvas with one axes filling it and no frame.

    A SUBPLOT, not `add_axes`. An axes without a subplotspec makes every
    `tight_layout()` call on the figure raise "This figure includes Axes that
    are not compatible with tight_layout, so results might be incorrect" --
    and `tools/figure_fit.py` calls it on everything it audits. A gate whose
    own measurement is warned to be unreliable is not a gate
    (deck-gauntlet 5.7), so these eleven panels are subplots and the warning
    is gone.

    `_save` then runs the SAME `tight_layout()` the gate runs, so the
    geometry the gate measures is the geometry that is saved -- which is the
    whole point of deck-bar D5a. That only works because the axes starts at
    the full canvas: from `plt.subplots`' default 0.125--0.9 rect every label
    overflows, tight_layout insets by a different amount per panel
    (0.100 to 0.149 of the width, depending on which step's text is present),
    and the urn moves on the slide as the algebra advances. Starting full,
    nothing overflows, the inset is the fixed pad, and all eleven panels come
    out with the identical axes rect.
    """
    fig, ax = plt.subplots(figsize=STEP_FIG)
    # Start from the whole canvas. plt.subplots opens at left=0.125,
    # right=0.9, which maps these data units into 77% of the width -- every
    # label then overflows and tight_layout insets differently per panel.
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, XMAX); ax.set_ylim(0, YMAX)
    ax.axis("off")
    return fig, ax


def _txt(ax, x, y, s, color=INK, ha="center", va="bottom", size=None,
         weight=None):
    ax.text(x, y, s, color=color, ha=ha, va=va, fontsize=size or LBL,
            zorder=8, linespacing=1.25,
            **({"fontweight": weight} if weight else {}))


def _dish(ax, cx, cy, w, h):
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((cx, cy), w, h, facecolor="white",
                         edgecolor=MUTED, lw=2.2, zorder=1))


def _strand(ax, x, y, color, r=0.38):
    from matplotlib.patches import Circle
    ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor="none",
                        zorder=3))


def _capsid(ax, cx, cy, left, right, w=2.5, h=1.7, dim=False):
    """A virion: one capsid, two single strands. The session's whole object.

    ONE GLYPH FOR ONE OBJECT. `s25_objects` used to draw its own virion as a
    rounded box with two ellipses inside while this drew an ellipse with two
    circles, so the room met the hour's central object twice in two shapes.
    The strand offset and radius scale with `w` -- at the default 2.5 they
    are exactly the 0.52 and 0.38 the urn series was authored with, so those
    eleven panels are unchanged to the pixel.

    `dim=True` greys the whole virion. It is how `s25_urn_6` says "the model
    sets this one to zero": a red X over it was a full strike on a block the
    same panel calls a PARTIAL block, and an unlabelled drawn symbol besides.
    """
    from matplotlib.patches import Ellipse, Circle
    shell = MUTED if dim else MINT
    edge = MUTED if dim else INK
    ax.add_patch(Ellipse((cx, cy), w, h, facecolor=shell,
                         alpha=0.18 if dim else 0.40,
                         edgecolor=edge, lw=2.2, zorder=2))
    for dx, col in ((-0.208 * w, left), (0.208 * w, right)):
        if col is None:
            ax.add_patch(Circle((cx + dx, cy), 0.152 * w, facecolor="white",
                                edgecolor=MUTED, lw=2.0, ls=":", zorder=3))
        else:
            _strand(ax, cx + dx, cy, MUTED if dim else col, r=0.152 * w)


def fig_urn_series(stem="s25_urn"):
    """Segment 2's derivation series: the urn filling as the binomial builds.

    Six panels for `derivation_fig`, one per BUILD step. The object is drawn
    at P = 3 -- one HIV-1 transcript, three crHIV-1 -- because P = 3 is a row
    of NUMBERS.md 4b (0.0625, 0.3750, 0.5625) and because it is the smallest
    P a room can count off a picture.

    MODEL: W03's binomial, two independent draws from a pool at 1 : P.
    """
    pr = [float(x) for x in diploid_packaging(P_DRAW)]      # 1/16, 6/16, 9/16
    assert abs(sum(pr) - 1.0) < 1e-12
    inf3 = float(infectious_fraction(P_DRAW))               # 0.6250, 4b
    for step in range(1, 7):
        fig, ax = _panel()
        # "W03" IS A NUMBERS.md TAG AND NO SLIDE EXPANDS IT (see the note
        # on the chain panels' title). The urn is drawn, so "the urn" was
        # the picture naming itself; the eight characters that buys pay for
        # the author's name. MEASURED: 9.31 of 10.94 data units, centerd.
        _txt(ax, CX, 9.33, "Weinberger's binomial, $P$ = 3", color=MUTED)

        _dish(ax, CX, 7.75, 5.0, 2.4)
        _strand(ax, CX - 1.34, 7.95, _HIV, r=0.44)
        for dx, dy in ((-0.09, 8.15), (-1.04, 7.15), (0.81, 7.35)):
            _strand(ax, CX + dx, dy, _VEC, r=0.44)
        # BOTH SPECIES LABELS ARE OUTSIDE THE URN AND BOTH HAVE A LEADER.
        # "HIV-1" ended at x = 3.20 and the ellipse's own left border at
        # that height is x = 3.00, so the label ran across the border from
        # outside it -- deck-bar D5a item 1, the collision figure_fit does
        # not look for. "crHIV-1" had the opposite problem: it floated at
        # x = 8.60 with nothing between it and three teal dots two units
        # away, so the only thing attaching the word to the object was its
        # color, and color alone is deck-bar C3. Each now sits clear of
        # the ellipse and runs a leader to the dot it names.
        _txt(ax, 2.70, 7.95, "HIV-1", color=_HIV, ha="right", va="center")
        ax.annotate("", xy=(3.50, 7.95), xytext=(2.82, 7.95),
                    arrowprops=dict(arrowstyle="-", color=_HIV, lw=1.8,
                                    shrinkA=0, shrinkB=0), zorder=6)
        _txt(ax, 8.30, 8.10, "crHIV-1", color=_VEC, ha="left", va="center")
        ax.annotate("", xy=(5.98, 8.13), xytext=(8.18, 8.10),
                    arrowprops=dict(arrowstyle="-", color=_VEC, lw=1.8,
                                    shrinkA=0, shrinkB=0), zorder=6)
        # AND THE BARE RATIO IS GONE. It read "1 : P,  P = 3" -- a ratio
        # with neither side named, which DESIGN.md sec 6 item 8 rules out
        # in terms: `posb/populations.py` writes this same pool P : 1 and
        # the figures write 1 : P, and read the wrong way round q becomes
        # 1/(1+P) and every genotype probability in the segment inverts.
        # It was also the title's "P = 3" said twice. The panel does not
        # print a ratio now: it DRAWS one amber strand against three teal
        # ones with both named, which `fig_objects` already establishes is
        # how the room gets the pool.

        if step >= 2:
            # "each" read as per-DOT beside three teal dots. q is a
            # property of one DRAW, which is the whole of the next step.
            _txt(ax, XMAX - 0.08, 6.90, "$q = 3/4$\nper draw", color=_VEC,
                 ha="right", va="top")
        # THE TWO ARROWS BELONG TO STEP 3 ONLY. They were pinned at
        # (CX +/- 0.55, 5.70) when there was one capsid under them, and left
        # drawn from step 4 on, when there are three -- so both still
        # converged on the MIDDLE one and the picture said two draws produce
        # the heterozygote while the two homozygotes came from nowhere. On
        # step 6 they pointed at the genotype the panel sets to zero. Step 3
        # is where they are true: one blank capsid, two draws into it.
        if step == 3:
            _txt(ax, 0.08, 5.95, "two draws", color=MUTED, ha="left")
            for dx0, dx1 in ((-1.0, -0.55), (1.0, 0.55)):
                ax.annotate("", xy=(CX + dx1, 5.70), xytext=(CX + dx0, 6.45),
                            arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                            lw=2.4, shrinkA=0, shrinkB=0))
            _capsid(ax, CX, 4.70, None, None)
            _txt(ax, CX, 2.88, "one capsid, two strands")

        XS = (2.05, CX, XMAX - 2.05)
        if step >= 4:
            _capsid(ax, XS[0], 4.70, _HIV, _HIV)
            _capsid(ax, XS[1], 4.70, _HIV, _VEC, dim=(step == 6))
            _capsid(ax, XS[2], 4.70, _VEC, _VEC)
        if step == 4:
            for x, lab in zip(XS, ("$(1{-}q)^2$", "$2q(1{-}q)$", "$q^2$")):
                _txt(ax, x, 2.88, lab)
        if step >= 5:
            for i, (x, lab) in enumerate(zip(
                    XS, ("$1/(1{+}P)^2$", "$2P/(1{+}P)^2$",
                         "$P^2/(1{+}P)^2$"))):
                _txt(ax, x, 2.88, lab,
                     color=MUTED if (step == 6 and i == 1) else INK)
            # STEP 6 IS AN ARITHMETIC STEP, NOT A STRIKE. A red X over the
            # middle capsid was a FULL strike on a block this panel's own
            # footer calls PARTIAL, and an unlabelled drawn symbol besides.
            # The capsid greys (dim=True above) and the number says what the
            # model does to it, which is the thing to read out loud.
            for i, (x, v) in enumerate(zip(XS, pr)):
                if step == 6 and i == 1:
                    _txt(ax, x, 2.03, f"{v:.4f} $\\to$ 0", color=RED)
                else:
                    _txt(ax, x, 2.03, f"{v:.4f}", color=MUTED)
        if step == 6:
            # AND THE PANEL FINISHES ITS OWN SUM. It stopped one step short:
            # the middle genotype went to zero and the infectious fraction
            # that follows -- NUMBERS.md 4b's COMPUTED 0.6250 at P = 3 --
            # was never printed anywhere in the series.
            assert abs(inf3 - (pr[0] + pr[2])) < 1e-12
            _txt(ax, CX, 1.18, f"infectious: {inf3:.4f} at $P$ = 3")

        foot = {
            1: "equal packaging · independent\ndraws — and nothing tests either",
            2: "$q = P/(1{+}P)$ is the chance one\nstrand drawn is the vector",
            3: "diploid: TWO strands per capsid,\nnot one and not three",
            # NOT "Show they sum to one -- do not assert it": that was a
            # note to whoever built this panel, projected at 20 pt, and the
            # panel did not show it either. What the room needs off the
            # picture is that the three capsids are the whole list.
            4: "three outcomes and no others,\nso they sum to one",
            # NOT the deck's own aside. This footer read "W03 prints
            # 1 : 2P : P^2 -- same, with the (1+P)^2 dropped", which is
            # derivation_fig step 6's aside almost word for word, set
            # beside it on the same slide. What the panel can say that the
            # stack cannot is what that ratio IS for the object drawn here:
            # 1 : 6 : 9 at P = 3, whose normalisation is the 0.0625 /
            # 0.3750 / 0.5625 printed under the three capsids. CHECKED:
            # 1 : 2P : P^2 at P = 3 is 1 : 6 : 9, and 1/16, 6/16, 9/16 are
            # the three values the panel prints.
            5: "at $P$ = 3 that ratio is 1 : 6 : 9",
            # ONE line, because step 6 prints the infectious fraction below
            # the genotypes and two lines of footer would land on it. The
            # deck slide beside this panel carries An et al.'s finding and
            # W03's rounding in full.
            # AND IT STAYS SHORTER THAN THE ORIGINAL. Spelling W03 out
            # here as "Weinberger" put this line 397 px past the axes, so
            # tight_layout could not fit it, urn_6 saved 5.55 in wide
            # against its siblings' 4.76, the whole series resized 16.7%
            # between stages and every label on the panel fell under the
            # type floor. One line, one figure, five gate findings --
            # deck-gauntlet 5.5b exactly. Who rounds is the deck row's job
            # beside this panel; the panel carries what was rounded.
            6: "An et al.: PARTIAL, rounded to 0",
        }[step]
        _txt(ax, CX, 0.05, foot, color=RED if step == 6 else INK)
        _save(fig, f"{stem}_{step}", fixed=True)


# =====================================================================
# SEGMENT 3 -- the infection chain assembles as R0 does. T73.
# Same fixed 5.30 x 4.50 in canvas as the urn series, same column.
# =====================================================================

def _cell(ax, x, y, fill, edge=None, r=0.60, lw=3.0):
    from matplotlib.patches import Circle
    ax.add_patch(Circle((x, y), r, facecolor=fill,
                        edgecolor=edge or MUTED, lw=lw, zorder=4))


def _virions(ax, cx, cy, color, n=7, r=0.20):
    from matplotlib.patches import Circle
    spots = [(-0.95, 0.55), (-0.05, 0.75), (0.85, 0.50), (-1.05, -0.35),
             (-0.15, -0.15), (0.75, -0.40), (0.30, 0.18)][:n]
    for dx, dy in spots:
        ax.add_patch(Circle((cx + dx, cy + dy), r, facecolor=color,
                            edgecolor="none", zorder=4))


def _flow(ax, x0, x1, y=8.45):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.6,
                                shrinkA=0, shrinkB=0))


def fig_chain_series(stem="s25_chain"):
    """Segment 3's derivation series: the infection chain, built one link
    at a time, then re-indexed on an I_T cell.

    Steps 1-4 are the Basic Model, equations [1]-[3]. They carry the three
    factors of R0 as SYMBOLS on the objects they belong to -- n on the
    emission arrow, 1/c on the virions, kT on the infection arrow -- and no
    numeric value and no result: every number in this derivation is in
    derivation_fig's own step stack and closing box beside the panel, and
    the printed-c*delta verdict is the next slide's. See the long note in
    the step-1-to-4 branch for what was cut and why.

    Step 5 is the SAME count with a different index case -- an I_T cell,
    which is the thing readers of R0_T get wrong -- and names the second
    model on the panel.

    MODEL: Weinberger equations [1]-[3] (steps 1-4), [4]-[6] (step 5).
    """
    for step in range(1, 6):
        fig, ax = _panel()
        tip = step == 5
        # "W03" IS A NUMBERS.md TAG AND IT WAS ON THE WALL. No slide in the
        # deck expands it, so a room that never read the file saw a label
        # naming nothing. MEASURED on this canvas at the body floor:
        # "Weinberger therapy · eqns [4]–[6]" is 9.63 of the 10.94 data
        # units, centerd 0.65 to 10.29, so the full name fits and the model
        # stays named on the figure (this module's first rule).
        _txt(ax, CX, 9.33,
             "Weinberger therapy · eqns [4]–[6]" if tip
             else "Weinberger basic · eqns [1]–[3]", color=MUTED)

        from matplotlib.patches import Circle
        if tip:
            # THREE STATIONS, AND THE MIDDLE ONE IS THE WHOLE POINT.
            #
            # This panel used to draw the burst coming off the I_T cell. An
            # I_T cell emits nothing: NUMBERS.md 18.2 reads P^2Dn as
            # "crHIV-1 virions per I_D cell over its lifetime", and 4a,
            # quoted from W03 p.4, says "an I_D cell will produce D x 200
            # HIV-1 virions and P^2 x D x 200 crHIV-1 virions" -- those are
            # the Dn*delta'*I_D and P^2*Dn*delta'*I_D terms of [3] and [6],
            # and [6] is the equation this panel's own title cites. The
            # superinfecting virion was drawn arriving and the cell it
            # produces was never drawn, recoloured or named, so the
            # compartment the hour's paradox lives in -- D acting inside
            # I_D, while a singly infected I cell never sees it -- was
            # absent from the picture that claims to be the chain.
            #
            # So: an I_T cell, then HIV arriving and the SAME cell redrawn
            # as I_D, then the burst off the I_D cell. Stacked rather than
            # strung across, because three named stations plus their labels
            # do not fit on one row of this canvas at the body floor and
            # deck-gauntlet 5.3 says the type does not move.
            _cell(ax, 1.05, 8.45, CYAN, edge=TEAL, r=0.56)
            ax.add_patch(Circle((1.05, 8.45), 0.22, facecolor=TEAL,
                                edgecolor="none", zorder=5))
            _txt(ax, 2.05, 8.45, "an $I_T$ cell — has the vector",
                 ha="left", va="center")

            ax.annotate("", xy=(1.05, 6.95), xytext=(1.05, 7.89),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.4,
                                        shrinkA=0, shrinkB=0))
            ax.add_patch(Circle((2.35, 7.60), 0.24, facecolor=AMBER,
                                edgecolor="none", zorder=4))
            _txt(ax, 2.78, 7.60, "HIV-1", color=AMBER, ha="left",
                 va="center")
            ax.annotate("", xy=(1.45, 6.58), xytext=(2.14, 7.44),
                        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.4,
                                        shrinkA=0, shrinkB=0))

            # the SAME cell, recoloured and renamed: amber rim and an amber
            # genome beside the teal one.
            _cell(ax, 1.05, 6.10, CYAN, edge=AMBER, r=0.66, lw=3.6)
            ax.add_patch(Circle((0.83, 6.24), 0.20, facecolor=TEAL,
                                edgecolor="none", zorder=5))
            ax.add_patch(Circle((1.27, 5.94), 0.20, facecolor=AMBER,
                                edgecolor="none", zorder=5))
            _txt(ax, 2.05, 6.10, "an $I_D$ cell — vector and HIV",
                 ha="left", va="center")

            ax.annotate("", xy=(1.05, 4.70), xytext=(1.05, 5.44),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.4,
                                        shrinkA=0, shrinkB=0))
            _virions(ax, 1.45, 3.70, TEAL)
            _flow(ax, 2.70, 3.70, y=3.70)
            _cell(ax, 4.35, 3.95, CYAN, edge=TEAL, r=0.44)
            _cell(ax, 5.05, 3.30, CYAN, edge=TEAL, r=0.44)
            for cxx, cyy in ((4.35, 3.95), (5.05, 3.30)):
                ax.add_patch(Circle((cxx, cyy), 0.16, facecolor=TEAL,
                                    edgecolor="none", zorder=5))
            _txt(ax, 5.90, 3.70, "$P^2Dn$ vector,\nnew $I_T$ cells",
                 ha="left", va="center")
        else:
            # THE CHAIN RUNS DOWN THE CANVAS AND THE POPULATION FILLS THE
            # RIGHT THIRD. Three things were wrong with the old layout and
            # the third is why it is rebuilt rather than nudged.
            #
            # 1. DEAD SPACE. The chain ran left to right across the top band
            #    and the algebra stacked under it, so once the algebra went
            #    (below) the drawing was a cluster of cells in the top-left
            #    with the footer four inches beneath it: step 1 had a 2.58 in
            #    unbroken empty band, step 2 1.67 in. Measured on the PNG, by
            #    empty pixel rows, not by eye.
            # 2. THE PANEL RE-RAN THE DECK'S OWN ALGEBRA COLUMN. It printed
            #    "lives 1/delta = 1.4 d, emits n", "each virion lives
            #    1/c = 0.03 d", "infects at kT, T = lambda/d = 1550/ul" and
            #    "R0 = lambda k n/(c d) = 1.9375" -- four lines the step
            #    stack beside it already carries, at 1.43 d and 0.033 d, so
            #    the room read one argument twice in two typefaces rounded
            #    two ways, and R0 appeared in the panel AND in
            #    derivation_fig's closing box. Cut, per deck-gauntlet 5.2:
            #    cut text rather than nudge coordinates. What is left is the
            #    three factors as SYMBOLS on the three things they belong
            #    to -- n on the emission arrow, 1/c on the virions, kT on
            #    the infection arrow -- which is what a picture adds. Every
            #    numeric value is the stack's.
            # 3. AND IT REVEALED A STEP EARLY. "infects at kT, T = lambda/d
            #    = 1550/ul" was gated on step >= 3 and it is the deck's STEP
            #    4. The arrow it became arrives at step 4.
            #
            # The field of well cells is the frame, not decoration: "one
            # cell, when nearly all are well" is the linearisation this
            # whole count rests on, and it was a sentence at the bottom of
            # an empty canvas. Drawn, it also fills the right third at every
            # step, so step 1 reads as one infected cell beside a population
            # rather than as a drawing in a corner. Early-step emptiness in
            # a four-step derivation_fig build cannot be removed altogether
            # -- cropping to the ink would resize the panel between stages,
            # which is the one thing derivation_fig and figure_fit's
            # series_consistency check exist to stop.
            #
            # X BUDGET, AND MEASURE IT AFTER `_settle`, NOT BEFORE. On the
            # raw canvas this axes is 78.4 px per data unit; `tight_layout`
            # insets it to rect (0.056, 0.061, 0.888, 0.878) and the scale
            # becomes 69.6 px per unit, so every string is 12.6% WIDER in
            # data units than it measures before the settle. Budgeting on
            # the pre-settle number put three labels into the cell field and
            # ran the field's own label 7 px off the axes -- deck-gauntlet
            # 5.2 is exactly this, and here it bites through the measuring
            # instrument. Post-settle widths, in data units at the body
            # floor: "one infected cell" 5.30, "each lives 1/c" 4.40, "new
            # infections" 4.63, "well cells" 2.80, footer 10.49. The field's
            # left ink is at 7.50 and no label passes 7.45.
            FIELD_X = (7.95, 9.10, 10.25)
            FIELD_Y = [1.75 + k * 1.15 for k in range(6)]
            rng = np.random.default_rng(25)       # deterministic build
            for fx in FIELD_X:
                for fy in FIELD_Y:
                    _cell(ax, fx + float(rng.uniform(-0.13, 0.13)),
                          fy + float(rng.uniform(-0.13, 0.13)),
                          MINT, r=0.32, lw=2.0)
            _txt(ax, 7.95, 8.15, "well cells", color=MUTED, ha="left")

            # station A -- the index case
            _cell(ax, 1.10, 8.20, RED, edge=RED, r=0.66)
            _txt(ax, 2.05, 8.20, "one infected cell", ha="left", va="center")

            if step >= 2:
                ax.annotate("", xy=(1.10, 6.55), xytext=(1.10, 7.20),
                            arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                            lw=2.4, shrinkA=0, shrinkB=0))
                _txt(ax, 1.55, 6.80, "emits $n$", ha="left", va="center")
                _virions(ax, 1.60, 5.25, AMBER)
                _txt(ax, 3.05, 5.60, "free virions", ha="left")
            if step >= 3:
                _txt(ax, 2.90, 4.80, "each lives $1/c$", ha="left")
            if step >= 4:
                ax.annotate("", xy=(1.10, 3.75), xytext=(1.10, 4.55),
                            arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                            lw=2.4, shrinkA=0, shrinkB=0))
                _txt(ax, 1.55, 4.15, "infects at $kT$", ha="left",
                     va="center")
                _cell(ax, 1.00, 3.05, RED, edge=RED, r=0.52)
                _cell(ax, 1.75, 2.05, RED, edge=RED, r=0.52)
                _txt(ax, 2.60, 2.50, "new infections", ha="left",
                     va="center")

        if tip:
            _txt(ax, CX, 1.60, "$R_0^T = P^2 D\\,(1 - 1/R_0)$", color=TEAL)
            _txt(ax, CX, 0.45, "$1{-}1/R_0$ = chance it meets HIV",
                 color=MUTED)
        else:
            # NEITHER R0 NOR THE PRINTED c*delta IS PRINTED HERE ANY MORE,
            # and a later pass must not restore either.
            #
            # R0 = lambda k n/(c d) = 1.9375 is derivation_fig's own CLOSING
            # BOX on this very slide -- `closing="R0 = n . k . (lambda/d)/c =
            # lambda k n/(c d) = 1.9375"` -- so the panel printed the
            # slide's result a second time, in a second typeface.
            #
            # The red "printed c*delta: 0.055, impossible" was worse: it is
            # the whole of the NEXT slide, `_s3_build_printed`, titled "The
            # printed denominator cannot be right", which puts both
            # arithmetics up and asks the room for 0.055. Printed at step 4
            # it answered the question one click before it was asked. It
            # does NOT move to step 5 either: step 5 is the panel beside the
            # "1 - 1/R0 is a probability" slide, which is the wrong home for
            # the Basic Model's transcription slip, and the deck states the
            # verdict in body type on its own slide after asking the room.
            _txt(ax, CX, 0.30, "one cell, when nearly all are well",
                 color=MUTED)
        _save(fig, f"{stem}_{step}", fixed=True)


# =====================================================================
# SEGMENT 3's SECOND derivation -- R0_T, three factors, two cancellations.
#
# DESIGN.md sec 7 build need 5 asks for a `derivation_fig` run here with
# "the two cancellations marked on the picture where they happen", and the
# deck has been running the hardest argument of the hour -- the one sec 6
# says must never be cut -- as two three-step `derivation` calls with no
# picture at all. These are the six panels that run is missing.
#
# `s25_chain_5` cannot be reused inside the run: it prints the endpoint
# R0_T = P^2*D*(1 - 1/R0) at its foot, and six stages of a build that
# already shows its answer is not a build. It keeps its own slide; stage 6
# here is the same drawing with the three factors marked on their segments.
#
# THE HARD CONSTRAINT, stage by stage, against the deck's two runs:
#   `_s3_build_waiting`  step 1 -> stage 1   nothing printed at all
#                        step 2 -> stage 2   kV* and d, the two hazards
#                        step 3 + closing -> stage 3   = 1 - 1/R0
#   `_s3_build_factors`  step 1 -> stage 4   P^2*D*n, aside P^2Dn*d'  x 1/d'
#                        step 2 -> stage 5   kT*/c = 1/n
#                        step 3 + closing -> stage 6   R0_T = P^2 D (1-1/R0)
# No stage prints a quantity its own step has not reached.
#
# AND THE BURST COMES OFF THE I_D CELL. An earlier round of this module
# drew an I_T cell emitting it. P^2*D*n is per I_D cell: NUMBERS.md 18.2
# reads it as "crHIV-1 virions per I_D cell over its lifetime", and 4a
# quotes Weinberger p.4 -- "an I_D cell will produce D x 200 HIV-1 virions
# and P^2 x D x 200 crHIV-1 virions". Those are the P^2*D*n*delta'*I_D term
# of equation [6] and the D*n*delta'*I_D term of [3]. The I_T cell in this
# picture emits NOTHING; it waits, and either meets HIV-1 or dies.
# =====================================================================

def fig_rtchain_series(stem="s25_rtchain"):
    """The R0_T generation chain, six stages, both cancellations on the
    picture at the point where each one happens.

    MODEL: Weinberger equations [4]-[6], linearised at the HIV-endemic
    therapy-free equilibrium (NUMBERS.md 18.1). Same fixed canvas as
    `s25_chain_*` and `s25_urn_*`, so all three series project at the one
    scale in derivation_fig's 5.4 x 4.95 in column.
    """
    from matplotlib.patches import Circle
    for step in range(1, 7):
        fig, ax = _panel()
        _txt(ax, CX, 9.33, "Weinberger therapy · eqns [4]–[6]", color=MUTED)

        # -- stage 1: the I_T cell, waiting, and nothing else ----------
        _cell(ax, 1.05, 8.70, CYAN, edge=TEAL, r=0.56)
        ax.add_patch(Circle((1.05, 8.70), 0.22, facecolor=TEAL,
                            edgecolor="none", zorder=5))
        _txt(ax, 2.05, 8.70, "an $I_T$ cell — has the vector",
             ha="left", va="center")

        # -- stage 2: TWO EXITS FROM ONE CELL --------------------------
        # The competing risk, drawn. This is the step the room is most
        # likely to be lost on and the one thing the picture carries that
        # the algebra cannot: the cell is not waiting for HIV-1, it is
        # racing it against its own death, and kV*/(d + kV*) is which of
        # two clocks fires first. So the two hazards are two arrows
        # LEAVING ONE CELL in different directions, one of them ending in
        # nothing.
        if step >= 2:
            ax.annotate("", xy=(0.35, 7.10), xytext=(0.78, 8.10),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                        lw=2.4, shrinkA=0, shrinkB=0))
            ax.annotate("", xy=(2.60, 7.55), xytext=(1.32, 8.10),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                        lw=2.4, shrinkA=0, shrinkB=0))
            _txt(ax, 0.15, 6.45, "$d$ (dies first)", ha="left", va="top")
            # the virion that drives the other exit, at that arrow's head
            ax.add_patch(Circle((2.95, 7.88), 0.28, facecolor=AMBER,
                                edgecolor="none", zorder=4))
            _txt(ax, 3.40, 7.88, "HIV-1", color=AMBER, ha="left",
                 va="center")

        # -- stage 3: CANCELLATION ONE, ON THE ARROW IT HAPPENS ON -----
        # Same anchor as stage 2's bare kV*: the mark on the superinfection
        # arrow does not move, it COMPLETES. That is what DESIGN.md sec 7
        # build need 5 asks for -- "the two cancellations marked on the
        # picture where they happen" -- and it costs no band of its own,
        # which is what kept the I_D cell and the burst below it on the
        # canvas. MEASURED: the full string is 7.77 of 10.94 data units, so
        # from x = 2.95 it ends at 10.72 inside an axes that runs to 10.94.
        _txt(ax, 2.95, 7.00,
             "$kV^*/(d + kV^*) = 1 - 1/R_0$" if step >= 3 else "$kV^*$",
             color=TEAL if step >= 3 else AMBER, ha="left", va="center")
        if step < 2:
            # stage 1 is the cell and its name, and nothing else at all
            ax.texts[-1].remove()

        if step >= 3:
            # the I_D cell is where the superinfection arrow goes: the SAME
            # cell, recoloured and renamed -- amber rim, amber genome beside
            # the teal one.
            _cell(ax, 1.05, 4.95, CYAN, edge=AMBER, r=0.66, lw=3.6)
            ax.add_patch(Circle((0.83, 5.09), 0.20, facecolor=TEAL,
                                edgecolor="none", zorder=5))
            ax.add_patch(Circle((1.27, 4.79), 0.20, facecolor=AMBER,
                                edgecolor="none", zorder=5))
            _txt(ax, 2.05, 4.95, "an $I_D$ cell", ha="left", va="center")

        # -- stage 4: the burst, and it comes off the I_D CELL ---------
        if step >= 4:
            ax.annotate("", xy=(1.05, 3.95), xytext=(1.05, 4.22),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                        lw=2.4, shrinkA=0, shrinkB=0))
            _virions(ax, 1.55, 2.95, TEAL)
            # BESIDE IT, NOT UNDER IT. Stacked, the factor and the
            # production-over-lifetime aside that explains it came within
            # 6 px of each other and then within 6 px of the next
            # cancellation below -- figure_fit's GAP is 10 px and all
            # three pairs were flagged. Side by side they clear by 0.43
            # data units and the stack below gets 0.75 units back, which
            # is what let the foot keep its daylight.
            _txt(ax, 3.05, 3.35, "$P^2Dn$", color=TEAL, ha="left",
                 va="center")
            _txt(ax, 5.10, 3.35, "$P^2Dn\\delta' \\times 1/\\delta'$",
                 color=MUTED, ha="left", va="center")

        # -- stage 5: CANCELLATION TWO, on the last arrow --------------
        if step >= 5:
            ax.annotate("", xy=(1.05, 1.80), xytext=(1.05, 2.30),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                        lw=2.4, shrinkA=0, shrinkB=0))
            # ONE ARTIST, TWO LINES. The mark and the noun were two
            # labels stacked, and measured on the render they cleared each
            # other by 9.0 px against figure_fit's 10 px GAP, while the
            # noun then overlapped the foot by 0.8 px -- and there was no
            # room left in the column to pull them apart, because the foot
            # already sits 8 px off the bottom of the axes. Making them one
            # text block removes the pair the gate was comparing and costs
            # nothing: they say one thing.
            _txt(ax, 2.80, 1.90, "$kT^*/c = 1/n$\nnew $I_T$ cells",
                 color=TEAL, ha="left", va="center")
            for cxx, cyy in ((1.05, 1.28), (1.85, 1.02)):
                _cell(ax, cxx, cyy, CYAN, edge=TEAL, r=0.44)
                ax.add_patch(Circle((cxx, cyy), 0.16, facecolor=TEAL,
                                    edgecolor="none", zorder=5))

        # -- stage 6: and ONLY now the product -------------------------
        if step >= 6:
            _txt(ax, CX, 0.12, "$R_0^T = P^2 D\\,(1 - 1/R_0)$", color=TEAL)
        _save(fig, f"{stem}_{step}", fixed=True)


# =====================================================================
# SEGMENT 2's payoff -- the three genotypes, and the extremum at P = 1.
# =====================================================================

def fig_genotypes(name="s25_genotypes"):
    """Where P = 1 sits: a MAXIMUM of the waste, a MINIMUM of what infects.

    The sweep is fine (1600 points over three decades) because both
    quantities turn at P = 1 and a coarse grid straddles the extremum. The
    direction is the thing: `heterozygote_waste` RISES to 0.5 at P = 1 and
    falls after; `infectious_fraction` FALLS to 0.5 at P = 1 and rises after.
    An earlier draft of the session had that backwards.

    What a student concludes: an evenly balanced co-infected cell is the
    WORST case -- it throws away exactly half of everything it makes.

    MODEL: W03's binomial on a 1 : P pool. No measured point is plotted.
    """
    P = np.logspace(-1, 2, 1600)
    hiv, het, vec = diploid_packaging(P)
    inf = infectious_fraction(P)
    waste = heterozygote_waste(P)
    assert np.isclose(waste.max(), 0.5) and np.isclose(inf.min(), 0.5)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.45))

    for ax in (axL, axR):
        ax.axvline(1.0, color=RULE, lw=1.6, ls="--", zorder=1)
        ax.axhline(0.5, color=RULE, lw=1.6, ls=":", zorder=1)
        ax.set_xscale("log")
        ax.set_xlim(0.1, 100); ax.set_ylim(0, 1.0)
        ax.set_xlabel("packaging advantage  $P$", fontsize=LBL)
        ax.grid(True, axis="y", color=RULE, lw=0.5)

    axL.plot(P, hiv, color=AMBER, lw=3.0, zorder=3)
    axL.plot(P, het, color=RED, lw=3.0, zorder=3)
    axL.plot(P, vec, color=TEAL, lw=3.0, zorder=3)
    axL.plot([1, 1], [0.25, 0.5], "o", color=INK, ms=9, zorder=6)
    _tag(axL, 0.01, 0.86, "HIV·HIV", AMBER)
    _tag(axL, 0.55, 0.52, "crHIV·crHIV", TEAL)
    _tag(axL, 0.70, 0.22, "hetero", RED)
    # SHORTER, AND ONE ON EACH PANEL. "fraction of virions released" set
    # 589 px of type against an axes about 350 px tall -- the tallest
    # object in the figure -- and the right panel had no y-label at all,
    # so the panel that carries the session's extremum did not say what it
    # was plotting.
    axL.set_ylabel("fraction of virions", fontsize=LBL)
    # THE LEFT PANEL'S TITLE IS CUT, AND THE MODEL NAME MOVES TO THE
    # SUPTITLE. Expanding the tag W03 -> Weinberger took this title from 23
    # characters to 30, and a title is CENTRED on its axes: at 568 px of
    # axes it was 618 px wide, so it overhung both ends. On the left it
    # printed through the y-tick label "1.0" (9.6 x 14.7 px of real
    # overlap, which the gate cannot see -- deck-bar D5d item 1 -- and
    # which no amount of shortening below 28 characters would have fixed
    # alone); on the right it closed to 7.0 px of the "HIV.HIV" tag's
    # plate, inside figure_fit's 10 px gap, with the descender of
    # "binomial" sitting over the tag's cap height.
    #
    # SHORTENING IT CANNOT WORK, AND THAT IS WHY IT IS GONE. The tag's
    # right edge is at 360.6 px and the axes center at 470.1, so a centerd
    # title clears the tag only below about 199 px -- ten characters, which
    # is "Weinberger" and nothing else. And the vertical gap is not a width
    # problem at all: the tag sits at axes fraction 0.86 with 44 px of type
    # above it in a 344 px axes, so its top is at 0.988 whatever the title
    # says. Cutting characters buys nothing there (deck-gauntlet 5.2 runs
    # the other way here: the title's height is one line either way).
    #
    # So the model name goes OUT OF THE AXES INTO FRAME, which is deck-bar
    # D5d's own closing note, and the suptitle is two characters SHORTER
    # than it was. The right panel keeps its title: it is the panel whose
    # claim is the one-half, its title does not overhang its axes, and its
    # tags are 117 px below it.
    axL.set_title("", fontsize=LBL, color=MUTED)

    axR.plot(P, waste, color=RED, lw=3.4, zorder=3)
    axR.plot(P, inf, color=TEAL, lw=3.4, zorder=3)
    axR.plot([1], [0.5], "o", color=INK, ms=12, zorder=6)
    # NO PLATE, AND OFF THE REFERENCE LINE. At (0.86, 0.62) va="top" this
    # label's page-colored plate deleted 1.36 in of the y = 0.5 line --
    # 217 px, from x = 1214 to 1431, exactly its own width -- on a panel
    # titled "both exactly 1/2 at P = 1". That line IS the panel's
    # argument, and it was the only break in it not explained by a marker
    # or a tangent curve (deck-bar D5b: a plate is an occlusion defect
    # wearing a legibility defect's clothes). Nothing runs through the
    # label here: the teal curve is at 0.95 and the red at 0.05 where it
    # sits, so it needs no plate at all.
    # x 0.61-0.99, y 0.54-0.66: under the teal curve (0.77 at the box's
    # left edge) and over the red one (0.23 there). Moving it off the
    # reference line first put it ON its own curve for 171 px, which is the
    # worse of the two; this anchor clears both by a quarter of an inch.
    _tag(axR, 0.99, 0.66, "infectious", TEAL, ha="right", va="top",
         plate=False)
    _tag(axR, 0.99, 0.26, "waste", RED, ha="right", va="top", plate=False)
    axR.set_ylabel("fraction of virions", fontsize=LBL)
    axR.set_title("both exactly $\\frac{1}{2}$ at $P = 1$", fontsize=LBL,
                  color=MUTED)

    fig.suptitle("Weinberger's binomial: waste MAXIMAL at $P = 1$, "
                 "infectious MINIMAL", fontsize=LBL, color=INK)
    _save(fig, name)


# =====================================================================
# SEGMENT 4 -- the burst ledger. Two models, and D leaves one of them.
# =====================================================================

def fig_burst_ledger(name="s25_burst_ledger"):
    """What one dually infected cell has to release, if the burst SCALES.

    W03's equations [3] and [6] do not partition a fixed burst, they multiply
    one: total output is (1+P)^2*D*n, so the paper's own headline design
    point -- P = 100, D = 0.4 -- needs 816,080 virions out of a single cell.
    That is 4,080 times the n = 200 measured in vivo. The capped model is the
    flat line at n.

    THE 40,000 IS DELIBERATELY NOT DRAWN, and a later pass should not put it
    back. W03 cites "up to 40,000 virions" for env-deleted SIV (NUMBERS.md
    4c) to Perelson and Ho as UNPUBLISHED DATA. The room cannot check it, and
    every number on a slide has to trace to something it can. It is good
    context -- the headline point needs twenty times the largest figure the
    paper can cite anywhere -- so it belongs in the speaker note, said out
    loud, not printed on the picture. Drawn, it also cost 427 px of the
    scaling curve to the plate that kept it legible, which is the occlusion
    deck-bar D5 exists to stop.

    What a student concludes: the binomial is the right calculation for WHICH
    genotype a virion is, and the wrong one for HOW MANY virions there are.

    MODEL: W03 equations [3] and [6], scaling, against a capped burst of n.
    """
    P = np.logspace(0, 2, 600)
    scale_tot = sum(burst_output(P, D_FIG, n=NBURST))
    cap_tot = sum(burst_output(P, D_FIG, n=NBURST, fixed=True))
    head = float(sum(burst_output(P_HEAD, D_FIG, n=NBURST)))
    assert np.allclose(cap_tot, NBURST)

    fig, ax = plt.subplots(figsize=(10.2, 4.30))
    ax.loglog(P, scale_tot, color=AMBER, lw=3.6, zorder=4)
    ax.loglog(P, cap_tot, color=TEAL, lw=3.6, zorder=4)
    ax.plot([P_HEAD], [head], "o", color=RED, ms=12, zorder=6)
    # The scaling curve runs corner to corner, so every label sits in one of
    # the two triangles it leaves: above it on the left, below it on the right.
    # THE TAG IS THE LAW, AND THE NAME MOVED TO THE SUPTITLE. Expanding
    # W03 -> Weinberger took this tag from 701 px wide; its right edge then
    # reached 922.8 px, PAST the axes center at 889.0, so the centerd panel
    # title -- which no cut can pull right of it -- overlapped it in x and
    # closed to 8.7 px in y, inside figure_fit's 10 px gap. Cutting the
    # tag to the law alone is the only move that separates them: at 269 px
    # it ends at 491 and the shortened title starts at 662, which is 171 px
    # of daylight rather than a nine-and-a-half-pixel margin
    # (deck-gauntlet 5.2). "Weinberger" is not lost -- it is in the
    # suptitle, in frame, where the room reads it first.
    #
    # THE WIDTHS, MEASURED RATHER THAN GUESSED, because the first cut here
    # threw away a word it did not have to. The tag starts at 221.7 px and
    # the shortened title starts at 658.5, so the tag may be 426.7 px wide
    # before figure_fit's 10 px gap closes. "scales as $(1+P)^2Dn$" is
    # 426.6 -- a 0.1 px margin, which is the s22 callout's 9.7-against-10
    # all over again, so NOT that one. "$(1+P)^2Dn$, scaling" is 393.5 and
    # leaves 43 px, and it keeps the word this module's docstring makes the
    # distinction on: W03's burst SCALES, a capped burst PARTITIONS. It
    # also matches the teal tag's shape below -- value, then which model.
    _tag(ax, 0.02, 0.82, "$(1{+}P)^2Dn$, scaling", AMBER)
    # "capped: n = 200 (Haase)" WAS WRONG TWICE. The teal line is the CAPPED
    # MODEL's output -- a limiting case of ours, NUMBERS.md 18.6 reading (b)
    # -- not anybody's measurement; and Haase's 200 is the burst of a SINGLY
    # HIV-1-infected cell, QUOTED by W03 at p.4 and not measured by it,
    # against an axis that reads "virions from one I_D cell", which is a
    # different object. So a modeling assumption carried someone else's
    # name on the wrong quantity. The line says what the model does; the
    # attribution goes on the reference VALUE at caption size, which is what
    # TYPE["caption"] inside a figure is reserved for.
    #
    # TOTAL, in capitals, because the next figure in the same segment draws
    # another flat teal line that is the VECTOR's output. Two consecutive
    # flat teal lines with color doing all the work read as a redraw.
    _tag(ax, 0.99, 0.115, "$n$ = 200 TOTAL, capped model", TEAL,
         ha="right")
    # THE HAASE ATTRIBUTION IS CUT, AND IT IS A CUT RATHER THAN A MOVE.
    # It read "n = 200: W03 quoting Haase", MUTED, just above the teal
    # label. Three things were wrong with it at once and one cut answers
    # all three.
    #   * Spelling W03 out made the line long enough to reach the scaling
    #     curve -- figure_fit: 101 px of drawn line. Nudging it is
    #     deck-gauntlet 5.2's treadmill; this curve runs corner to corner,
    #     so there is no wide slot to nudge it into.
    #   * Two labels both beginning "n = 200", one above the other, both in
    #     the lower-right triangle, read as two names for the one teal
    #     line. They were not: one named the line, the other sourced a
    #     number.
    #   * And the number it sourced is not this panel's. Haase counted the
    #     burst of a SINGLY HIV-1-infected cell; this axis reads "virions
    #     from one I_D cell", and the teal line is the capped MODEL's
    #     output, a result of ours, not anybody's measurement. The comment
    #     below already records that putting Haase's name near this line
    #     was "wrong twice"; it was wrong a third way.
    # Where 200 comes from is carried in body type on the deck's own
    # `_s4_build_assumption` slide, with the journal pages, which is where
    # a provenance claim can be made at length. ONE judgment call for Adam:
    # this removes the only literature attribution from this plate.
    # The callout moved into the upper-left triangle: the lower-right one
    # now carries the capped model's two lines, and the leader runs above
    # the scaling curve the whole way rather than across it.
    ax.annotate(f"{head:,.0f} = {head / NBURST:,.0f} $\\times$ $n$",
                xy=(P_HEAD, head), xytext=(0.03, 0.56),
                textcoords="axes fraction", color=RED, fontsize=LBL,
                ha="left", va="bottom", bbox=_plate(), zorder=7,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8,
                                shrinkB=10))
    ax.set_xlabel("packaging advantage  $P$", fontsize=LBL)
    ax.set_ylabel("virions from one $I_D$ cell", fontsize=LBL)
    # a little headroom past P = 100 so the marker is not clipped by the spine
    ax.set_xlim(1, 115); ax.set_ylim(80, 4e6)
    ax.grid(True, which="both", color=RULE, lw=0.5)
    # 23 characters rather than 44. "over the cell's life" is carried by
    # the y-label's "from one $I_D$ cell" plus "total" here, and the
    # y-label is NOT the place to put the extra word: it is already 504 px
    # of rotated type against a 336 px axes, so lengthening it is the one
    # change on this plate that could move the axes (deck-bar D5d item 5).
    ax.set_title("total output, $D$ = 0.4", fontsize=LBL, color=MUTED)
    # Three characters shorter than it was, and it now carries the name.
    fig.suptitle("Weinberger's binomial fixes WHICH genotype, not HOW MANY",
                 fontsize=LBL, color=INK)
    _save(fig, name)


def fig_burst_capped(name="s25_burst_capped"):
    """Cap the burst and D leaves the vector's output entirely.

    The session's own executable counterexample, and the reason move 4's
    title is a result about an architecture rather than a law. If the cell
    makes n particles whatever happens, the binomial still fixes the
    composition -- at P = 100 that is 196 vector particles of 200 -- but the
    count carries no D at all. R0_T then has no D in it, the shared
    production term that makes the payload the vector's own fitness is gone,
    and the paradox does not arise. Nagoor Pitchai et al. 2024 built a TIP
    that works that way: it competes for Gag rather than suppressing it, so
    the optimum becomes a maximum (NUMBERS.md 16).

    What a student concludes: which of the two lines is right is an
    empirical question, and nobody has measured it.

    THE BOUND IS NOT ON THIS PLATE, AND A LATER PASS MUST NOT PUT IT BACK.
    NUMBERS.md 18.6's sup R_0^T_fixed = 1 - 1/R0 = 15/31 = 0.48387 is the
    ENTIRE content of the next slide, `_s4_build_capped_number`, titled
    "Under a capped burst the therapy never invades", which states it in
    body type with both readings of the cap and the Jacobian check. Printed
    here it arrived one click early and destroyed that slide; printed here
    WITHOUT its subscript -- which is how it shipped -- it also read as a
    claim about the amber curve on the same panel, where
    therapeutic_R0(100, 0.4, 1.9375) = 1935.5, false by a factor of 4000.
    Two defects, one line, and the line was never this panel's job: R_0^T
    is not plotted here and cannot be, because the panel holds P at 100.
    What this plate shows is the flat teal line. That is the argument.

    MODEL: W03 equation [6], scaling, against a capped burst of n. P = 100.
    """
    D = np.logspace(-2, 0, 400)
    scale_vec = burst_output(P_HEAD, D, n=NBURST)[2]
    # One call per D, so the flat line is a RESULT and not a constant drawn
    # across the panel: in fixed mode D is absent from the vector's output.
    cap_vec = np.array([float(burst_output(P_HEAD, d, n=NBURST, fixed=True)[2])
                        for d in D])
    assert np.ptp(cap_vec) == 0.0

    fig, ax = plt.subplots(figsize=(10.2, 4.30))
    ax.loglog(D, scale_vec, color=AMBER, lw=3.6, zorder=4)
    ax.loglog(D, cap_vec, color=TEAL, lw=3.6, zorder=4)
    # 0.80, NOT 0.70. The amber curve runs 0.510 to 0.936 of the axes
    # across this panel, and the longer name pushed the tag's right edge
    # from 0.29 to 0.39 of the width -- where the curve has climbed to
    # 0.676 and the tag's plate reached it, 48 px by the gate. Raising the
    # anchor puts the whole block above the curve's highest point inside
    # its own x range.
    _tag(ax, 0.02, 0.80, "Weinberger scales as $P^2Dn$", AMBER)
    # THE LABEL SITS ON ITS LINE. It used to float about 120 px above the
    # flat teal line it names and 30 px under the amber curve, with color
    # doing all the work of saying which was which.
    #
    # VECTOR, in capitals, against the previous figure's TOTAL: those are
    # two consecutive flat teal lines in one segment, and without the word
    # the second reads as a redraw of the first. They are different
    # quantities -- 200 virions of every kind from an I_D cell there, 196
    # vector virions of those 200 here.
    #
    # AND THE BOUND IS GONE FROM THE LABEL -- see the docstring. One line
    # now, naming the line it sits on. ONE LINE ALSO BUYS CLEARANCE: the
    # two-line block topped out at 0.41 of the axes against a scaling curve
    # whose left end is at 0.510, a margin of 0.10; one line tops out at
    # 0.27 and clears it by 0.24.
    _tag(ax, 0.02, 0.125,
         f"capped: {float(cap_vec[0]):.0f} VECTOR of 200 at every $D$", TEAL)
    ax.set_xlabel("antiviral effect  $D$   ($D$ = 1 is no inhibition)",
                  fontsize=LBL)
    # WRAPPED, NOT CUT. Set on one line this label was 508 px of rotated
    # type against a 335 px axes -- 1.52x the thing it labels, overhanging
    # the axes at both ends. Wrapping costs no words and no type size
    # (deck-gauntlet 5.3): the rotated HEIGHT becomes the longest line, 309
    # px, which fits inside the axes. It is not what binds this figure's
    # saved height -- the suptitle and the x-label are -- so this buys
    # legibility, not headroom.
    ax.set_ylabel("vector virions\nreleased", fontsize=LBL)
    ax.set_xlim(0.01, 1); ax.set_ylim(80, 4e6)
    ax.grid(True, which="both", color=RULE, lw=0.5)
    ax.set_title("the vector's own output from one $I_D$ cell, $P$ = 100",
                 fontsize=LBL, color=MUTED)
    # NO SUPTITLE. It read "cap the burst and D leaves the vector's output
    # entirely" and the slide it lands on, `_s4_build_capped`, is titled
    # "Cap the burst and D leaves the vector's output" -- the same sentence
    # at 32 pt directly above it, found by rendering the deck page. The
    # panel title says what is plotted and the axis says in what units;
    # the headline is the slide's job. It also buys placement: the file
    # goes from 4.11 in tall to about 3.83, which takes the projected scale
    # in the deck's 4.16 in band from 1.012 to 1.041.
    _save(fig, name)


# =====================================================================
# SEGMENT 3's design space -- our contour, and W03's own floor beside it.
# =====================================================================

# W03 Fig. 3a's floor, digitized by us. NOT a measurement and NOT a redrawn
# data panel: it is the red/cyan line of the paper's own stability
# projection -- red = pretherapy HIV steady state stable (crHIV dies), cyan =
# crHIV solution stable -- read off the page rendered at 300 dpi.
#
# HOW, so the number can be checked. The floor is an affine parallelogram;
# its three visible corners were located as the extreme points of the
# red-or-cyan mask and the mapping inverted. The calibration test is W03's
# own text: it says the oscillatory (black) region sits at "P > 10 and
# D ~ 0.1", and the black pixels map to P > 11 with D from 0.05 to 0.13,
# median 0.094. Each row below is the midpoint of the last red and the first
# cyan pixel along a line of constant D; that transition is 0.12 to 0.26 wide
# in P over the range kept here. Below D = 0.06 the black band interferes and
# above D = 0.50 the plotted surface hides the floor, so neither is listed.
#
# KIND: INFERRED BY US (digitization). It is NOT in NUMBERS.md -- that file
# records the floor only qualitatively, in 9 and in 5c. See the module
# docstring for what the comparison shows.
W03_FIG3A_FLOOR = [(0.06, 4.77), (0.08, 3.77), (0.10, 3.38), (0.13, 2.97),
                   (0.16, 2.79), (0.20, 2.54), (0.25, 2.47), (0.30, 2.46),
                   (0.35, 2.48), (0.40, 2.63), (0.45, 2.67), (0.50, 2.78)]
# The oscillatory (Hopf) region. W03 p.6 places it at "P > 10 and D ~ 0.1"
# -- QUOTED, NUMBERS.md 5c -- and that sentence is all NUMBERS.md records. The
# extent drawn here is the black band of the same floor, from the same
# digitization as W03_FIG3A_FLOOR: black pixels run P = 11 to the top of the
# panel's P axis and D = 0.05 to 0.13, median 0.094. The P ceiling is the edge
# of Fig. 3a, not a boundary. KIND: INFERRED BY US, and its agreement with
# W03's own sentence is what calibrates the digitization above.
HOPF_P, HOPF_D = (10.0, 20.0), (0.05, 0.13)


def fig_design_space(name="s25_design_space"):
    """The persistence threshold is a BAND, and W03's own floor sits in it.

    LEFT, ours: R0_T = 1 is P^2*D = 2.0667 at this patient's R0 = 1.9375, and
    the shaded band is what the same condition gives over R0 from 1.9 to 20,
    where the coefficient 1 - 1/R0 runs 0.47 to 0.95 and the threshold on the
    product runs 1.05 to 2.11 (NUMBERS.md 5b). One sharp contour would be
    overclaiming: the band is a statement about the construct, not the
    patient, and its width is the patient.

    RIGHT, theirs: the red/cyan stability boundary of W03's own Fig. 3a,
    digitized by us and replotted flat, with the oscillatory region the text
    places at P > 10 and D ~ 0.1. Their figure is a perspective-projected
    surface with the stability map on a tilted floor; it cannot take a 2-D
    contour, so this is a replot beside ours rather than an overlay.

    What a student concludes: the closed form and the simulation agree on
    shape and scale and are not the same curve -- theirs sits near the bottom
    of our band at small D, crosses ours near D = 0.35, and leaves the band
    above it. W03 says it checked the two against each other only in a
    supplement whose URL is dead.
    """
    D = np.logspace(-1.7, 0, 500)
    lo = P_min(D, R0_HI)            # coefficient 0.95 -> threshold 1.05
    hi = P_min(D, R0_LO)            # coefficient 0.47 -> threshold 2.11
    mid = P_min(D, R0)              # 2.0667 at this patient's R0
    # THE MARK IS THE CONSTRUCT THE DEBRIEF IS ABOUT. It used to sit at
    # P = 3.21, D = 0.2 -- NUMBERS.md 5b's reference value, and a different
    # point from the one segment 3 releases the room on, which is a
    # construct measured at P = 8 needing D_min(8, 1.9375) = 0.0323. Both
    # lie on P^2*D = 2.0667, so a slide carrying the first and arguing the
    # second has to explain the difference in its foot, which is a patch
    # over the wrong mark.
    p_work = 8.0
    d_work = float(D_min(p_work, R0))              # 0.032292
    assert abs(float(therapeutic_R0(p_work, d_work, R0)) - 1.0) < 1e-9

    # 4.64 in: the x-labels gained a line and both titles gained one,
    # and the deck places this at band = 4.30, so the SAVED height has to
    # stay inside that or the type goes under the floor with the figure.
    # Height is the whole of the placement arithmetic here -- scale is
    # min(10.2, band*aspect)/w, which for anything the width does not bind
    # is just band/h. Authored 4.64 crops to about 4.26 saved; measured,
    # not assumed, because tight_layout makes the crop content-dependent,
    # and every inch not spent on chrome is axes the labels can use.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.64))
    for ax in (axL, axR):
        ax.fill_between(D, lo, hi, color=CYAN, alpha=0.38, lw=0, zorder=1)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(0.02, 1.0); ax.set_ylim(1.0, 20.0)
        # D'S SENSE, ON THE AXES THE ROOM FIRST READS D OFF. NUMBERS.md 3
        # records, INFERRED BY US, that W03's prose and W03's equations use
        # D in opposite senses and calls it a wording trap in the required
        # paper. `s25_burst_capped` disarms it -- but that figure is in
        # segment 4, after the room has read D off two segment-3 axes.
        # deck-bar F5: the measurement comes before the statistic. Same
        # string as the later figure, wrapped because a panel here is 4.3 in
        # wide and that line is 5.9.
        ax.set_xlabel("antiviral effect  $D$\n($D$ = 1 is no inhibition)",
                      fontsize=LBL)
        ax.set_axisbelow(True)        # or the grid stripes the shaded bands
        ax.grid(True, which="both", color=RULE, lw=0.5)
        ax.set_yticks([1, 2, 5, 10, 20])
        ax.set_yticklabels(["1", "2", "5", "10", "20"])

    axL.plot(D, mid, color=TEAL, lw=3.4, zorder=4)
    axL.plot([d_work], [p_work], "o", color=RED, ms=11, zorder=6)
    # NO SUPTITLE, AND THAT IS WHY THE REST FITS. With one, the axes came
    # out 254 px tall inside the deck's 4.30 in band, a line of body type
    # was 0.22 of the axes, and the four things the left panel has to say
    # could not be placed without one of them landing on the contour --
    # which runs corner to corner, so there is no wide slot anywhere in the
    # middle. Dropping it buys 0.45 in of axes; the headline it carried is
    # now split between the two panel titles, where it is also closer to the
    # thing it describes.
    #
    # No plates in this figure. A plate is for text a CURVE would strike
    # through; here the only thing behind these labels is the shaded band,
    # and a page-colored plate punches a visible notch out of it.
    # THE SHADED BAND IS DATA. `figure_fit` samples ax.collections now, so
    # a label resting on the fill scores exactly like a label resting on a
    # curve -- rightly, because the band IS the panel's second statement.
    # That leaves two clear regions, above the band's upper edge and below
    # its lower one, and the contour runs corner to corner between them, so
    # every label here is anchored against those two lines rather than
    # against the axes.
    _tag(axL, 0.97, 0.98, "$R_0^T > 1$: spreads", INK, ha="right",
         va="top", plate=False)
    _tag(axL, 0.03, 0.02, "$R_0^T < 1$: dies out", INK, plate=False)
    # THE LEADER IS GONE, AND THE GEOMETRY SAYS IT HAD TO GO. It ran from
    # "band: 1.05 to 2.11" down to (0.33, 0.50) and its ARROWHEAD LANDED ON
    # THE CONTOUR -- cropped at 3x and looked at, the head overlaps the
    # teal line and the tip sits just inside the shading, so the leader
    # named the line rather than the band. deck-gauntlet 5.5b records this
    # as one of the defects the LAST round's fix created, and it was still
    # here.
    #
    # It cannot be cured by moving it, and the algebra says why rather than
    # a fourth guess (deck-bar D5d's closing note). In axes fractions the
    # three edges are parallel straight lines of the same slope:
    #     band bottom  y = 0.662 - 0.653 x
    #     the contour  y = 0.774 - 0.653 x
    #     band top     y = 0.779 - 0.653 x
    # The contour is 0.005 under the band's TOP edge, so the band is
    # essentially all below the contour and EVERY approach from above
    # crosses it. From below is clean -- but the free triangle beneath the
    # band holds exactly one line of body type beside "dies out", measured:
    # a 2.58 in label on a 3.80 in panel reaches x = 0.68, where the band's
    # lower edge has fallen to 0.26, and the block's own top is at 0.30.
    #
    # So the band's name goes into FRAME, in the panel title, and its
    # NUMBERS go nowhere here: `_s3_build_band` states "P²D between about
    # 1.05 and 2.11" in body type two slides earlier, and this plate was
    # repeating it. Cut text, move what is left out of the axes.
    # JUDGMENT CALL FOR ADAM: the debrief plate no longer carries the
    # band's range, only the word.
    # THE WORKED CONSTRUCT IS NAMED IN THE TITLE, NOT IN THE AXES. Three
    # text blocks is one more than this panel holds: it is 3.8 x 2.0 in,
    # a line of body type is 0.28 in, and the contour and the band between
    # them leave two clear regions, one above and one below. The mark is
    # the only marker on the panel, so the title labels it without
    # ambiguity -- and deck-gauntlet 5.2 says move content into frame
    # rather than keep nudging coordinates.
    axL.set_ylabel("packaging advantage  $P$", fontsize=LBL)
    # "· band" names the shading, and it is MEASURED to fit: 3.66 in on a
    # 3.80 in panel, so it does not widen the figure and cannot meet the
    # right panel's title, which is 3.59 in with 1.15 in of gap between the
    # two (deck-bar D5d items 2 and 5).
    axL.set_title(f"ours: $P^2D$ = 2.0667 · band\n"
                  f"$P$ = {p_work:.0f} needs $D$ = {d_work:.4f}",
                  fontsize=LBL, color=MUTED)

    axR.plot(D, mid, color=TEAL, lw=2.2, ls="--", zorder=3)
    fx = [p[0] for p in W03_FIG3A_FLOOR]
    fy = [p[1] for p in W03_FIG3A_FLOOR]
    # MARKERS, NO CONNECTING LINE, AND SMALLER. These twelve points are a
    # DIGITIZATION, not a curve: joining them draws boundary we did not read
    # between readings we did. At ms = 10 the last five overlapped each
    # other, which is the digitization claiming a resolution it has not got.
    axR.plot(fx, fy, "D", color=AMBER, ms=8, zorder=5)
    # Opaque, not alpha: a translucent block lets the minor grid through and
    # the oscillatory region comes out striped like a barcode.
    axR.fill_between(HOPF_D, HOPF_P[0], HOPF_P[1], color="#B9C6C6", lw=0,
                     zorder=2)
    # WHERE THEY CROSS, RINGED. NUMBERS.md 19 is explicit that a slide may
    # not present their boundary as confirming ours, and two near-coincident
    # curves with nothing said about them read as confirmation by default.
    # So the crossing is marked and both halves of 19's finding are written
    # down: the title says where they cross, the amber tag says what happens
    # past it.
    axR.plot([0.35], [2.455], "o", mfc="none", mec=INK, mew=2.2, ms=19,
             zorder=7)
    # 0.60, down from 0.70: the oscillatory tag gained a line and came
    # within figure_fit's 10 px of this one. At 0.60 the block spans 0.48
    # to 0.60 of the axes and the band's upper edge below it has fallen to
    # 0.34, so it clears the data as well as the label above.
    _tag(axR, 0.97, 0.60, "ours, dashed", TEAL, ha="right", va="top",
         plate=False)
    # THE SWATCH SAYS WHAT KIND OF THING IT IS. Drawn grey with the single
    # word "oscillatory" it was the one block on this figure with no
    # provenance: the amber points carry "digitized by us" and the dashed
    # line is ours by its title, while this -- read off the same floor of
    # the same perspective projection, from the same 300 dpi render -- read
    # as a region of (P, D) somebody had measured. Its bottom edge at
    # P = 10 is a reading, and its top edge is the edge of Weinberger's
    # panel rather than a boundary.
    # va="top" AT 0.88, NOT va="bottom" AT 0.80. Adding the second line
    # grew this tag UPWARD into the right panel's own two-line title --
    # "above our band past 0.35" printed through "oscillatory" on the
    # rendered slide. figure_fit cannot see it: it treats the axes title as
    # frame and excludes it from the box list, which is deck-bar D5d item 2
    # (title against title) one level down. Found by rendering the deck
    # page, not by the gate. Anchored from the top, the block spans 0.76 to
    # 0.88 of the axes, beside the grey swatch (0.769 to 1.0) and clear of
    # both the title above and "ours, dashed" at 0.70 below.
    _tag(axR, 0.50, 0.88, "oscillatory\n(digitized)", INK, va="top",
         plate=False)
    # EMPHASIS INVERTED. "W03 Fig. 3a floor" used to be the loud amber line
    # inside the panel and "digitized by us" the quiet grey title, so the
    # admission was the faintest thing on a figure whose whole point is that
    # the amber points are OURS and do not sit on our algebra.
    _tag(axR, 0.03, 0.01, "digitized by us\ncrosses at 0.35",
         AMBER, plate=False)
    # THE RIGHT PANEL SAYS WHAT ITS y IS. It had no y-label at all, so the
    # panel that carries the digitized boundary relied on the reader
    # carrying "packaging advantage P" across 1.15 in of gap from the other
    # panel (deck-bar D2). It costs width and nothing else: while the deck
    # fits this figure by HEIGHT, the placement scale is band/h and does not
    # move when the figure gets wider.
    axR.set_ylabel("packaging advantage  $P$", fontsize=LBL)
    axR.set_title("theirs: Weinberger Fig. 3a\nabove our band past 0.35",
                  fontsize=LBL, color=MUTED)
    _save(fig, name)



# =====================================================================
# SEGMENT 1 -- the objects, drawn before anything is modelled.
#
# WHY THESE EXIST. The census in DESIGN.md sec 2 is the reason: virion,
# capsid, diploid, heterozygous, allele and helper virus all have ZERO
# occurrences on any slide, body line or speaker note across the 22 built
# decks. This session has no mathematics problem -- steady states,
# eigenvalues and bifurcations run to tens of hits each -- it has an OBJECT
# problem, and an object problem is not fixed by a sentence in a speaker
# note. lecture-design.md sec 5e's FRAME move asks for the object DRAWN,
# and deck-bar F1 asks for it drawn on the slide that argues about it.
#
# DESIGN.md sec 7 lists these as build needs 1 and 2 under the names
# `objects_fig` and `cistrans_fig`. They did not exist when the deck was
# built on 8 November, so they are here. Any later pass that finds two
# generators for one picture should keep these and delete the other.
# =====================================================================

def fig_objects(name="s25_objects"):
    """The four objects of this hour, drawn, with no algebra on the plate.

    DESIGN.md sec 2 names all four and says why none of them can be words:
    the binomial follows from the capsid, the urn the binomial draws from IS
    the dually infected cell, "what you can delete" is only visible against
    the full genome, and move 5 reads super-Mendelian inheritance straight
    off the locus. The locus is drawn HERE rather than in segment 5 because
    it is the object the room has least chance of having met -- allele,
    diploid, heterozygous and homozygous are all zero across the 22 built
    decks -- and it should not arrive in the same five minutes as the
    argument that uses it.

    NO ALGEBRA ON THIS PLATE, which is DESIGN.md sec 7's own constraint. The
    one symbol is the ratio label on the cytoplasmic pool. That label is NOT
    a definition of P and does not claim to be one -- it says which two
    populations the ratio is between, which is the part a reader cannot
    recover from the picture; the slide beside it defines P. Counts are
    drawn rather than written: one HIV-1 transcript against three vector
    transcripts, so the room can count the pool off the picture before
    anybody writes q = P/(1+P).

    TWO BY TWO, NOT FOUR ACROSS. Four columns across 10.2 in gives each
    object about 2.5 in, and at the 20 pt body floor an eighteen-character
    header is already 2.7 in wide -- so the first draft's headers
    overlapped each other by 12 and 14 px, and the labels under them by
    more. A 2 x 2 plate gives each object 5.1 in and the collisions go away
    without the type moving (deck-gauntlet 5.3: never shrink type; a layout
    problem is a text problem wearing a disguise, and here it was a column
    count wearing the same one).

    What a student concludes: a retrovirus packages TWO strands, so which
    genotype a particle is was decided by a draw; and the vector is the
    short bar, so what it deleted is what it now has to be given.

    MODEL: none. This is a drawing of the objects, not a result.
    """
    from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle
    fig, ax = plt.subplots(figsize=(10.2, 4.58))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, 10.2); ax.set_ylim(0, 4.58)
    ax.axis("off")
    ax.set_aspect("equal")

    # The plate uses the full 4.60 in band. image_centered sizes from the
    # aspect, so at 10.2 x 4.58 it places at scale 1.000 and the 20 pt type
    # projects at 20 pt.
    QL, QR = 2.46, 7.56           # quadrant centers
    MIDT, MIDB = 3.56, 1.42       # the two drawing center lines

    def head(x, y, t):
        ax.text(x, y, t, color=INK, ha="center", va="bottom", fontsize=LBL,
                fontweight="bold")

    def under(x, y, t):
        ax.text(x, y, t, color=INK, ha="center", va="bottom", fontsize=LBL)

    # -- 1. a virion: one capsid, two single strands -------------------
    # NEUTRAL STRANDS, AND `_capsid` DRAWS IT. Two things were wrong here.
    # One amber strand beside one teal one IS the heterozygote -- the exact
    # genotype segment 2 crosses out in red twenty minutes later -- offered
    # as the generic virion, in a figure that is the room's first sight of
    # the object. And it was drawn as a rounded box with two ellipses while
    # `_capsid` drew the same object as an ellipse with two circles in every
    # urn panel, so one object arrived in two shapes. Both strands are now
    # MUTED: at this point the claim is "two of them", not "which two".
    head(QL, 4.22, "a virion")
    _capsid(ax, QL, MIDT, MUTED, MUTED, w=1.52, h=1.04)
    under(QL, 2.62, "two strands, one capsid")

    # -- 2. a dually infected cell and its cytoplasmic pool ------------
    # The label sits BELOW the circle with daylight, not across it. At the
    # first 2 x 2 pass the circle ran to r = 0.86 and "its cytoplasm sits
    # at 1 : P" crossed its lower border -- a label striking a patch edge
    # from outside, which deck-bar D5a item 1 records as the collision
    # figure_fit cannot see. Caught by rendering the PNG and looking at it.
    head(QR, 4.22, "a co-infected cell")
    ax.add_patch(Circle((QR, MIDT), 0.58, facecolor="white", edgecolor=MUTED,
                        lw=2.6, zorder=2))
    # One HIV-1 transcript against three vector transcripts, on a 2 x 2 grid
    # so the four are separately countable: the room reads 1 : 3 off the
    # picture before anybody writes q = P/(1+P), and 1 : 3 is the urn
    # segment 2 then draws from. Scattered, two of them touched and a third
    # ran into the cell border.
    for dx, dy, col in ((-0.19, 0.17, _HIV), (0.19, 0.17, _VEC),
                        (-0.19, -0.17, _VEC), (0.19, -0.17, _VEC)):
        ax.add_patch(Ellipse((QR + dx, MIDT + dy), 0.17, 0.26, facecolor=col,
                             edgecolor="none", zorder=4))
    # P IS A RATIO OF TWO NAMED THINGS, AND THE LABEL HAS TO SAY WHICH.
    # "its cytoplasm sits at 1 : P" names neither side, so the reader had to
    # already know that amber is HIV-1 from a key in a different quadrant,
    # and the hazard is live: `posb/populations.py` writes the same pool as
    # "P : 1" while every figure in this module writes "1 : P". Read the
    # wrong way round, q = P/(1+P) inverts and every number in segment 2
    # flips. Naming both sides where the pool is drawn costs eleven
    # characters.
    under(QR, 2.62, "HIV-1 : crHIV-1  =  1 : P")

    # -- 3. the vector beside the full genome --------------------------
    # Bar names go beside each bar's RIGHT end, clear of the border. Set
    # over the bar they overlapped it from outside, which is the same D5a
    # defect as the cell label above.
    head(QL, 2.06, "the vector and the genome")
    for y, w, col, lab in ((MIDB + 0.10, 2.36, _HIV, "HIV-1"),
                           (MIDB - 0.46, 0.88, _VEC, "vector")):
        ax.add_patch(Rectangle((QL - 1.18, y), w, 0.36, facecolor="white",
                               edgecolor=MUTED, lw=2.2, zorder=2))
        ax.add_patch(Rectangle((QL - 1.18, y), 0.52, 0.36, facecolor=col,
                               edgecolor="none", zorder=3))
        ax.text(QL + 1.32, y + 0.18, lab, color=col, ha="left", va="center",
                fontsize=LBL)
    under(QL, 0.44, "the shaded end is kept")

    # -- 4. a diploid locus carrying two alleles -----------------------
    # BOTH COPIES THE SAME NEUTRAL COLOUR. Drawn amber and teal they read
    # as the HIV-1 and vector of the two panels above, which is a different
    # distinction entirely. At this point in the hour the locus makes one
    # claim -- there are two copies -- and the three allele CLASSES get
    # their own colors in segment 5, where they are introduced.
    head(QR, 2.06, "a diploid locus")
    for y in (MIDB + 0.10, MIDB - 0.46):
        ax.add_patch(Rectangle((QR - 0.74, y), 1.48, 0.36, facecolor="white",
                               edgecolor=MUTED, lw=2.2, zorder=2))
        ax.add_patch(Rectangle((QR - 0.19, y), 0.38, 0.36, facecolor=MUTED,
                               edgecolor=INK, lw=1.6, zorder=3))
    under(QR, 0.44, "two copies, one per parent")

    _save(fig, name)


def _kept_block(ax, x0, y0, w, h, col, ragged):
    """What the parasite still has: a solid block off the genome's left end.

    `ragged=True` breaks the right edge in a zigzag, the ordinary genome-map
    mark for "the drawing stops here". It is drawn for the two systems whose
    kept fraction NUMBERS.md 8 does not size -- the influenza DI particle and
    the split drive -- so the block says what is kept without claiming how
    much, which is the whole difference between those rows and crHIV-1's.
    """
    from matplotlib.patches import Polygon, Rectangle
    if not ragged:
        ax.add_patch(Rectangle((x0, y0), w, h, facecolor=col, edgecolor=INK,
                               lw=2.0, zorder=3))
        return
    # A ZIGZAG, NOT A POINT. The first attempt put one outward spike on the
    # right edge and rendered as a gene arrow, which in a genome map means
    # direction -- a claim, and the wrong one. Five alternating teeth read
    # as a torn edge.
    d = 0.11
    edge = [(x0 + w + (d if k % 2 == 0 else -d), y0 + k * h / 5.0)
            for k in range(6)]
    ax.add_patch(Polygon([(x0, y0)] + edge + [(x0, y0 + h)],
                         closed=True, facecolor=col, edgecolor=INK,
                         lw=2.0, zorder=3))


def fig_cistrans_series(stem="s25_cistrans"):
    """Segment 1's ledger, built one system per step.

    Three parasites that made the same trade: keep what is read in cis,
    delete what acts in trans, and let a helper supply the trans functions.
    NUMBERS.md sec 8 is the three-column ledger behind it.

    THE LABELS HERE ARE SHORT ON PURPOSE. This panel sits in
    theme.derivation_fig's 5.4 in figure column, beside a step stack that
    holds about 52 rendered characters a line, so the WORDING of the ledger
    belongs in the stack and the SHAPE belongs here. Two reasons, and the
    second is mechanical. A line past about 34 characters is wider than this
    canvas; it then overflows the axes, `tight_layout` insets the axes to
    make room, and because the inset depends on how much text a given step
    happens to carry, the three panels come out three different widths and
    the picture jumps as the ledger builds. Measured: the first draft ran
    796, 803 and 952 px. Cut text rather than move coordinates
    (deck-gauntlet 5.2).

    What a student concludes: obligate trans-dependence is not an HIV
    curiosity, it is the architecture three different systems arrived at --
    so a reproductive ratio for the parasite is well defined only while the
    helper is there.

    MODEL: none. NUMBERS.md sec 8, drawn.
    """
    from matplotlib.patches import Polygon, Rectangle
    # NAME AND HELPER ONLY. A third label per row -- what the parasite
    # keeps -- sat 0.3 in above the next row's name and the gate read the
    # two as one run of text on steps 2 and 3. The kept column is the step
    # stack's job: derivation_fig gives it about 52 rendered characters a
    # line, which is where "the cis packaging elements, the cargo gene and
    # an HIV-1-induced promoter" belongs. The panel carries the SHAPE.
    #
    # THE DI PARTICLE IS NOT AMBER. Amber is HIV-1 everywhere else in this
    # hour -- it is the key `s25_objects` sets ten minutes earlier and the
    # color of the superinfecting virion in `s25_chain_5` -- so an amber
    # bar here said "HIV-1" about a 1970 influenza particle. deck-bar B2 is
    # one alphabet per quantity; a palette is an alphabet.
    # EVERY ARROW NAMES A HELPER, WHICH IS WHAT THE ARROWS ARE FOR. They
    # used to read "Gag-Pol", "helper virus", "Cas9" -- a protein, an
    # organism and a protein -- so the one column all three rows share was
    # drawn with two different kinds of object in it, and the panel's own
    # closing line, "cis is kept, trans is borrowed", has no subject for
    # the middle row: you borrow Gag-Pol, you do not borrow a helper virus.
    #
    # The fix goes the other way round, to the SUPPLIER, because that is
    # the column NUMBERS.md 8 fills with quoted material for all three and
    # the product column it does not: Weinberger p.1 names the Gag-Pol
    # polyprotein, Noble p.24 names the host genome or a separate
    # construct, and Huang & Baltimore p.1 says only that DI particles
    # "can reproduce in the presence of HELPER VIRUS" -- 1970 does not name
    # what the helper hands over to an influenza DI particle, and writing
    # "polymerase" here would be us inventing it. So the arrow says who
    # lends, in all three rows, and the trans functions themselves --
    # Gag-Pol and Cas9 -- belong in the step stack beside the panel, which
    # this docstring already names as the home for the ledger's wording.
    # REQUESTED OF THE DECK: carry Gag-Pol and Cas9 in the step text.
    rows = [
        ("crHIV-1 vector", _VEC, "HIV-1"),
        ("a DI particle", CYAN, "helper virus"),
        ("a split CRISPR drive", GREEN, "the host genome"),
    ]
    # DELETION SHORTENS THE BAR, which is the grammar `s25_objects` already
    # taught the room: there the vector is a SHORT bar (0.88) against the
    # genome (2.36), about 37%, consistent with W03's ~4 kb against 10 kb.
    # This panel used to draw all three parasites as a full-length bar with
    # 23.7% shaded, which is a different grammar for the same object in the
    # same hour -- and a shared proportion nothing licenses: NUMBERS.md 8
    # gives a size only for crHIV-1, records influenza DI particles as
    # deleting "the largest of the RNA species" with no figure, and gives
    # the split drive as deleting cas9 from a construct whose other parts
    # are not sized.
    #
    # So the dashed outline is the complete genome, the solid block is what
    # the parasite still has, and only crHIV-1's block is drawn to a
    # proportion: 0.40 of the genome, W03 p.4's ~4 kb of 10 kb. The other
    # two break off in a ragged edge, which is the standard "the drawing
    # stops here, this is not a length" mark. Drawing three different
    # invented lengths would have replaced one unlicensed number with three.
    # AND ONLY ROW 1'S BLOCK HAS A LENGTH. All three were drawn at the
    # identical 3.72 -- 40% of the genome -- with rows 2 and 3 given a
    # ragged edge to say "this is not a length". A torn edge cannot undo a
    # proportion the eye has already measured against the row above it, and
    # three blocks of exactly one width assert a shared fraction that
    # NUMBERS.md 8 sizes for crHIV-1 alone. The torn rows are drawn as a
    # STUB instead: visibly shorter than the one row that is to scale, and
    # visibly not a measurement of anything.
    FULL, KEPT, STUB = 9.30, 3.72, 1.90   # 3.72 = 0.40 * 9.30, p.4's ~4 of 10 kb
    for step in range(1, 4):
        fig, ax = _panel()
        # COLUMN HEADERS, which this panel needed and did not have: the
        # shaded block and the open remainder were drawn regions with no
        # label on any step, and NUMBERS.md 8's "what the parasite KEEPS
        # (cis)" column was absent from the picture entirely (deck-bar D2).
        # An earlier attempt put them at the very top where the right-hand
        # one landed 2 px outside the axes; they sit at 9.22 now, over the
        # two regions of the first row's bar, and persist on all three
        # steps.
        _txt(ax, 0.20, 9.22, "kept (cis)", color=INK, ha="left")
        _txt(ax, 0.20 + (KEPT + FULL) / 2, 9.22, "deleted (trans)",
             color=INK)
        for j, (title, col, helper) in enumerate(rows[:step]):
            # THE NAME SITS ON ITS OWN BAR, WHICH IT DID NOT. An earlier
            # pass tried to fix this with an uneven pitch and left the
            # helper label and its arrow BETWEEN the name and the bar it
            # names, so measured on the render "a DI particle" sat 37 px
            # under the crHIV-1 bar and 109 px above its own: every row
            # label read as a caption on the row above, and a student takes
            # all three systems away wrong. figure_fit cannot see it -- it
            # compares text with text, and these are far apart.
            #
            # So the order inside a row is now name, bar, then the helper
            # coming in from BELOW. The arrow still terminates outside the
            # rectangle with daylight, which is the point of the old
            # arrangement -- the deletion stays deleted and only the gene
            # PRODUCT is supplied, in trans -- and it now does so under the
            # bar instead of over it. MEASURED, in data units: the name's
            # baseline is 0.20 above its own bar's top edge and 1.65 above
            # the bar of the row above, a ratio of better than eight to
            # one, against the old 0.37 against 1.09 the wrong way round.
            base = 8.35 - j * 2.85
            live = (j == step - 1)
            # FINISHED ROWS KEEP THEIR COLOUR. They used to grey out to
            # RULE on PAGE -- 1.25:1 -- so a panel captioned "three
            # systems, the same architecture" showed two of them as blank
            # outlines. The live row is marked by WEIGHT instead, which
            # costs no contrast, and the step stack beside the panel marks
            # it again.
            # THE NAME IS INK, THE BAR CARRIES THE COLOUR. Set in the
            # row's own color, "a DI particle" came out CYAN on PAGE --
            # 1.7:1, which is a fill color and not a text color. The bar
            # directly beneath the name does the color-coding.
            _txt(ax, 0.20, base, title, color=INK, ha="left",
                 weight="bold" if live else None)
            # the complete genome, dashed; then what the parasite still has,
            # 0.20 below the name and nothing in between.
            ax.add_patch(Rectangle((0.20, base - 0.72), FULL, 0.52,
                                   facecolor="none", edgecolor=MUTED, lw=2.0,
                                   ls=(0, (5, 4)), zorder=2))
            _kept_block(ax, 0.20, base - 0.72, KEPT if j == 0 else STUB,
                        0.52, col, ragged=j > 0)
            # THE ARROW STOPS OUTSIDE THE BAR, from underneath. It once
            # ended 0.26 units INSIDE the rectangle, which drew the helper
            # being written back into the sequence the parasite deleted --
            # the exact inverse of NUMBERS.md 8, where the deletion STAYS
            # deleted and only the gene PRODUCT is supplied, in trans, in
            # the cytoplasm. It terminates 0.20 units clear of the border.
            # The label is to its LEFT, right-aligned, so the widest of the
            # three -- "the host genome", 5.2 of 10.94 data units -- runs
            # from 1.10 and never reaches the axes edge.
            # AND THE SHAFT IS 0.76 UNITS, NOT 0.43. At 0.43 the whole
            # artist was 30 px of which the arrowhead took about 20, so it
            # rendered as a bare triangle sitting after the label -- "HIV-1
            # a" -- rather than as an arrow pointing at anything. 0.76 is
            # 53 px and reads as a direction. The rows re-pitch from 3.00
            # to 2.85 to pay for it and the bottom row still clears the
            # footer by 0.28 units.
            _txt(ax, 6.30, base - 1.30, helper, color=INK, ha="right",
                 va="center")
            ax.annotate("", xy=(6.71, base - 0.92),
                        xytext=(6.71, base - 1.68),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2,
                                        shrinkA=0, shrinkB=0), zorder=5)
        if step == 3:
            # ONE line, not two. The second line put the footer's top 7 px
            # inside the bottom row's genome rectangle -- a label striking a
            # patch border from outside it, which is deck-bar D5a item 1 and
            # which nothing but that check would have seen.
            _txt(ax, 0.20, 0.05, "cis is kept, trans is borrowed",
                 color=INK, ha="left")
        _save(fig, f"{stem}_{step}", fixed=True)


# =====================================================================
# SEGMENT 5 -- the locus, in two stages. DESIGN.md sec 5 segment 5 gives
# FRAME and BUILD two different rows -- "the diploid locus from segment 1,
# now with three alleles" and "super-Mendelian inheritance, with the gamete
# probabilities the plate prints" -- and one plate cannot serve both. On
# the single plate the gamete probabilities printed on the FRAME slide, one
# click BEFORE the slide that reads them, and `_s5_build_idealisation` then
# said the same things again as text.
#
# The canvas, the data box and every coordinate are shared, so the two
# stages save at the same size and the picture does not move between
# clicks -- which is what figure_fit's `series_consistency` exists to
# catch, and how the urn series broke on the morning of 8 November.
# =====================================================================

LOCUS_FIG = (11.4, 3.21)
LOCUS_X, LOCUS_Y0, LOCUS_Y1 = 10.2, 0.28, 3.10


def _locus_panel():
    """The shared canvas for both locus stages: one axes, aspect-equal.

    THE DATA BOX IS 10.2 x 2.82 AND THE CANVAS IS 11.4 x 3.21, WHICH IS NOT
    A MISTAKE. `tight_layout` insets by a pad in INCHES -- measured, exactly
    48 px a side here -- and on an aspect-equal axes that inset costs a
    larger FRACTION of a short canvas than of a tall one. An earlier pass
    cut the data box to 3.10 and left the canvas at 10.2 wide: the settled
    axes gave 129 px per data unit against the old 138, every string came
    out 7% wider in data units, and the two column headers collided. So the
    canvas is given back the inches the inset takes and the coordinates in
    `_locus_plate` keep meaning what they meant: MEASURED, this settles to
    148.1 px per data unit, the same as the 11.4 x 3.47 it replaces.

    WHY THE BOX NOW STARTS AT y = 0.28 RATHER THAN 0. The saved PNG carried
    0.375 in of dead plate along its bottom edge -- MEASURED, ink in rows
    22 to 430 of 491, so 4.5% empty above and 12.2% below -- because the
    bridge line is the lowest ink and its box bottom sat at y = 0.283 in a
    data box that ran to 0. The deck had already compensated by setting its
    rows against the measured ink rather than the image box, which worked
    but made the deck pay for the figure's slack; and the image box ran to
    4.82 in against rows starting at 4.70, an overlap `slide_fit` does not
    check (deck-bar D5c). Cutting the box to the ink and giving the canvas
    back the same 41.9 px of height keeps 148.1 px per unit EXACTLY, so not
    one coordinate below had to move: the file saves 9.64 x 2.81 in, the
    width still binds the deck's band, and the body floor projects at
    21.2 pt.
    """
    fig, ax = plt.subplots(figsize=LOCUS_FIG)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, LOCUS_X); ax.set_ylim(LOCUS_Y0, LOCUS_Y1)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def _locus_plate(ax, gametes=True):
    """Segment 5's locus plate, drawn into a caller's axes, in two stages.

    `gametes=False` is stage 1 -- the three allele classes and the diploid
    locus from segment 1, and nothing else. `gametes=True` adds the
    germline bracket and the gamete fan. Every coordinate is shared, so the
    two stages differ only in what is present; see `_locus_panel` for the
    canvas and why it is the size it is.

    WHY IT IS DRAWN RATHER THAN SAID. Move 5 reads super-Mendelian
    inheritance off this picture, and the line that does the reading is an
    ABSENCE: NUMBERS.md sec 6a's gamete table prints q^W_WD = 0, so a WD
    heterozygote never transmits a wild-type allele. An absence in a printed
    table is the hardest thing in this hour to carry in words, and
    deck-bar F1 asks for the system drawn on the slide that argues about it.
    Noble's Fig. 1C is not in the crop set, so this is ours.

    NOTATION, AND IT IS RENAMED RATHER THAN ANNOTATED. docs/symbols.md is
    the authority. Noble writes P for homing efficiency and D for the drive
    allele; this hour has already spent P on the packaging advantage and D
    on the antiviral effect, and T67 and T73 are both autograded and both
    on the final, so neither of those can move. The gene-drive technique is
    hand-graded, so it is the cheaper side:

      * homing efficiency is **h** here, so the invasion boundary is
        f > 1/(1+h). A footer saying "P here means something else" told the
        room the collision existed without removing it, which is exactly
        what deck-bar B1 rules out.
      * the ALLELES keep Noble's W, D and R, because his cropped figures
        carry those names and we do not alter published figures -- but no
        bare allele letter is written where it could be read as a quantity.
        They appear as genotypes (WD) or inside noun phrases ("the W
        gamete", "resistant allele"). A genotype pair cannot be mistaken
        for a scalar.

    What is left is one honest bridge, and it stays visible rather than
    sitting in the faintest type on the plate: Noble prints this h as P,
    and his crops still say P.

    WIDTH BUDGET. The data box is 10.2 units across and settles to 148.1 px
    per unit, so a line starting at x = 0.16 holds about 66 characters of
    20 pt body type, and the two columns are kept apart by giving the right
    one x = 5.10. The first draft ran the two column headers into each
    other so they read as one sentence, and set a 36-character allele label
    that ran under the locus drawing. Both were found by rendering the PNG
    and looking at it, not by the gate. NOTHING MAY REACH PAST x = 10.2:
    the tight crop would take the overflow on the stage that has the artist
    and not on the stage that does not, and the plate would change size
    between clicks.

    What a student concludes: the wild-type allele is destroyed in every
    heterozygote, so only its FATE is in question -- drive with probability
    (1+h)/2, resistant with (1-h)/2, and wild type never.

    MODEL: NUMBERS.md sec 6a's gamete-production table, drawn.
    """
    from matplotlib.patches import Rectangle

    # RED IS "THIS DOES NOT HAPPEN", EVERYWHERE IN THIS MODULE. The urn's
    # step 6 prints its struck genotype in RED, `fig_chain_series` prints the
    # impossible c*delta in RED, and the strike on the W gamete below is RED.
    # The drive allele was ALSO red, so one plate used one color for two
    # meanings -- the defect the module's own "a palette is an alphabet"
    # comment (deck-bar B2) raises for the DI particle and then committed
    # here. The drive moves to GREEN, which is already the split CRISPR
    # drive's color in `s25_cistrans`, so the room has met it; white on
    # GREEN is about 10:1.
    _W, _D, _R = MUTED, GREEN, CYAN
    CHIP = 0.44

    def chip(x, y, col, lab):
        ax.add_patch(Rectangle((x, y), CHIP, CHIP, facecolor=col,
                               edgecolor=INK, lw=1.6, zorder=3))
        ax.text(x + CHIP / 2, y + CHIP / 2, lab, color="white", ha="center",
                va="center", fontsize=LBL, fontweight="bold", zorder=5)

    def header(x, t):
        ax.text(x, 3.06, t, color=INK, ha="left", va="top", fontsize=LBL,
                fontweight="bold")

    # -- left column: the three allele classes -------------------------
    header(0.16, "three alleles at one locus")
    for i, (col, lab, what) in enumerate(((_W, "W", "wild-type allele"),
                                          (_D, "D", "drive allele"),
                                          (_R, "R", "resistant allele"))):
        # 0.62 rather than 0.66: the lower block grew by the two lines
        # deck-bar F4 asks for, and the saved height has to stay inside the
        # deck's band or the type goes under the floor with it.
        y = 2.06 - i * 0.62
        chip(0.16, y, col, lab)
        ax.text(0.78, y + CHIP / 2, what, color=INK, ha="left", va="center",
                fontsize=LBL)

    # -- right column: what a WD germline sends on ---------------------
    # Shifted left from 5.10 to 4.50 and the bars narrowed, to buy the
    # gamete rows enough width for a NOUN beside each chip. With a bare
    # letter against "(1+h)/2" the D chip read as a quantity, which is the
    # one collision docs/symbols.md says must not be written.
    # The header sits a little right of its column: at 4.50 it ran into the
    # left column's header, and the bars need the width more than the
    # header needs the alignment.
    #
    # THE TWO COLUMNS ARE OFFSET BY 0.40 IN, AND THAT IS THE POINT. With the
    # gamete chips at the PARENTAL bar centers -- 3.48 and 2.88 exactly -- the
    # bracket below was true and unread: magnified it is a 12 px staple the
    # eye skips, and the dominant reading was still the original wrong one,
    # W row -> D gamete and D row -> R gamete, straight across. Nothing is
    # level with anything now: the parental bars drop 0.26 and the gametes
    # rise 0.14, so every gamete sits 0.40 in (55 px) off the nearest bar
    # center and the bracket is the only thing that connects them. Done this
    # way round rather than by dropping the gamete column 0.46, which is the
    # same cure: the lowest gamete row then lands 41 px inside the measured
    # top edge of the Noble block below it, and buying that space costs a
    # line of deck-bar F4 content.
    # THE RIGHT HEADER IS THE ONE THING THAT CHANGES RATHER THAN GROWS.
    # Stage 1 names the object the room is looking at -- D2 wants every
    # drawn symbol labeled in its own figure, and at stage 1 the two bars
    # are the only thing on this side of the plate. Stage 2 is the same
    # individual, now shown transmitting. Both fit the 5.10 units between
    # this anchor and the box edge; "the diploid locus, two copies" does
    # not, and a header that overflows the axes changes the saved width
    # and breaks the series.
    header(5.10, "a WD germline sends on" if gametes else
                 "a WD heterozygote")
    PAR_Y = (1.80, 1.20)              # bar bottoms; centers 2.02 and 1.42
    GAM_Y = (2.20, 1.60, 1.00)        # chip bottoms; centers 2.42, 1.82, 1.22
    for yy, col, lab in zip(PAR_Y, (_W, _D), ("W", "D")):
        ax.add_patch(Rectangle((4.50, yy), 1.40, CHIP, facecolor="white",
                               edgecolor=MUTED, lw=2.2, zorder=2))
        chip(4.50 + 0.70 - CHIP / 2, yy, col, lab)

    if gametes:
        # THE GAMETES FAN OUT OF THE PAIR, not out of one bar each. With an
        # arrow level with each bar the picture said W sends on D and D sends
        # on R, which is not the claim -- the two bars together ARE the WD
        # genotype, and all three gametes come from that one germline.
        #
        # BUT THE FIRST FIX LANDED ON A WORSE CLAIM. The stem was drawn at
        # y = 2.88, which is the exact center of the D bar, so it left the LOWER
        # bar's right edge and nothing touched W at all: the picture then said D
        # sends on D, R and never-W, leaving unconnected the one allele this
        # panel exists to talk about -- the wild type, destroyed in every
        # heterozygote, NUMBERS.md 6a's q^W_WD = 0. A bracket now spans both
        # bars and the stem leaves its midpoint, y = 3.18, so the germline the
        # gametes come from is visibly BOTH copies.
        #
        # THE BRACKET IS ALSO TIGHTER -- 5.90 to 6.06 rather than to 6.18 -- which
        # is where the gamete arrows get the length they need below.
        MID = sum(PAR_Y) / 2 + CHIP / 2   # midpoint of the two bar centers, 1.72
        SPINE = 6.06
        for yc in [y + CHIP / 2 for y in PAR_Y]:
            ax.plot([5.90, 5.98], [yc, yc], color=MUTED, lw=2.4, zorder=4,
                    solid_capstyle="round")
        ax.plot([5.98, 5.98], [min(PAR_Y) + CHIP / 2, max(PAR_Y) + CHIP / 2],
                color=MUTED, lw=2.4, zorder=4, solid_capstyle="round")
        ax.plot([5.98, SPINE], [MID, MID], color=MUTED, lw=2.4, zorder=4,
                solid_capstyle="round")
        ax.plot([SPINE, SPINE],
                [min(GAM_Y) + CHIP / 2, max(GAM_Y) + CHIP / 2],
                color=MUTED, lw=2.4, zorder=4, solid_capstyle="round")

        # A NOUN BESIDE EVERY CHIP, and the probability in h rather than P.
        #
        # THE ARROWS ARE 0.84 IN RATHER THAN 0.52. At 0.52 the dashed one below
        # was 72 px of which the arrowhead took about 22 and the red slash
        # another 8, leaving a dash and a half: the dashedness that carries
        # "this one does not happen" barely survived. 0.84 in is 116 px and
        # about three dashes clear of both.
        # SHIFTED LEFT BY 0.08, AND EVERY INTERNAL GAP IS UNCHANGED.
        # At 7.60 the noun "resistant, (1-h)/2" ran 5.8 px PAST the data
        # box's right edge. It cost nothing on the single plate -- the
        # tight crop simply took the extra 5.8 px -- but stage 1 has no
        # nouns, so the two stages would have cropped to different widths
        # and the plate would have jumped between clicks. Moving the
        # arrowhead, the chip and the noun together by the same 0.08
        # leaves the chip-to-noun gap at 0.16 and shortens the arrow from
        # 124 px to 112 px, still well clear of the 77 px the comment
        # above records as too short to read as dashed.
        ARR0, ARR1, CHIPX, NOUNX = SPINE, 6.82, 6.92, 7.52
        for y, col, lab, what in ((GAM_Y[0], _D, "D", "drive, (1+$h$)/2"),
                                  (GAM_Y[1], _R, "R", "resistant, (1−$h$)/2")):
            ax.annotate("", xy=(ARR1, y + CHIP / 2), xytext=(ARR0, y + CHIP / 2),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.4,
                                        shrinkA=0, shrinkB=0), zorder=5)
            chip(CHIPX, y, col, lab)
            ax.text(NOUNX, y + CHIP / 2, what, color=INK, ha="left", va="center",
                    fontsize=LBL)

        # THE GAMETE THAT NEVER HAPPENS, AT A CONTRAST THAT CAN BE SEEN. Arrow,
        # box border and glyph were all RULE on PAGE -- 1.25:1 -- so in Dwinelle
        # the whole element disappeared and a red slash was left pointing at
        # blank page. NUMBERS.md 6a's missing q^W_WD is the hardest thing in
        # this hour to carry in words, and an absence has to be VISIBLE to read
        # as an absence. MUTED is 3.4:1; the arrow is dashed, which is what
        # carries "this one does not happen" without hiding it.
        NOW = GAM_Y[2] + CHIP / 2         # 1.22, the row that never happens
        ax.annotate("", xy=(ARR1, NOW), xytext=(ARR0, NOW),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.4,
                                    linestyle=(0, (4, 2.5)),
                                    shrinkA=0, shrinkB=0), zorder=5)
        ax.add_patch(Rectangle((CHIPX, GAM_Y[2]), CHIP, CHIP, facecolor="white",
                               edgecolor=MUTED, lw=1.8, ls=(0, (4, 2.5)),
                               zorder=3))
        ax.text(CHIPX + CHIP / 2, NOW, "W", color=MUTED, ha="center",
                va="center", fontsize=LBL, fontweight="bold", zorder=5)
        ax.text(NOUNX, NOW, "no W gamete", color=RED, ha="left",
                va="center", fontsize=LBL, fontweight="bold")
        # The strike goes across the ARROW, not across the allele box. Drawn
        # over the box it crossed the W glyph and figure_fit scored the letter
        # as sitting on 61 px of drawn line -- rightly, because a struck letter
        # is a letter you cannot read. Striking the transmission rather than the
        # allele is the truer picture anyway: the allele exists, it just never
        # leaves the germline.
        # It also crosses the MIDDLE of the longer shaft, 0.43 in from the tail
        # and 0.41 from the head, so it covers about 8 px of one dash instead of
        # most of the artist.
        # CENTRED ON THE SHAFT, NOT MEASURED FROM ITS TAIL. It was
        # ARR0 + 0.22 to ARR0 + 0.64, which sat 0.22 from the tail and 0.20
        # from the head while the shaft was 0.84 long. Shortening the shaft
        # to 0.76 left those two unequal -- 0.22 against 0.12 -- and pushed
        # the slash's upper end toward the arrowhead. Anchoring it to the
        # shaft's midpoint restores the authored symmetry and keeps it if
        # the shaft ever changes length again.
        _sh = (ARR0 + ARR1) / 2.0
        ax.plot([_sh - 0.21, _sh + 0.21], [NOW - 0.22, NOW + 0.22],
                color=RED, lw=3.4, zorder=9, solid_capstyle="round")

    # THE IDEALISATION IS NOT ON EITHER STAGE, AND A LATER PASS MUST NOT
    # PUT IT BACK. It used to carry three lines -- "Noble assumes the drive cuts
    # the W allele in every WD germline", what happens where it does not,
    # and "h measured: 0.14 to 1.00" -- citing deck-bar F4, a result carries
    # its failure boundary where it is stated. But this plate is on segment
    # 5's FRAME slide ("The locus you met in the first segment"), and the
    # slide that STATES the gamete table is the next one,
    # `_s5_build_super_mendelian`, titled "An allele the drive cuts is
    # never passed on". THOSE FOUR ROWS ARE NOW TWO SLIDES OF TWO (split
    # 8 November, DESIGN.md sec 5 segment 5): super_mendelian carries the
    # assumption and the gamete table, and `_s5_build_idealisation`,
    # titled "Noble assumes every cut happens", carries the 14%-to-100%
    # appendix range and why the idealisation is worst-case FOR the drive.
    # So the plate was printing the next slide's rows a click early and F4
    # was already satisfied one slide later, on the slide that states the
    # result -- which is what F4 actually asks for. The drawing is what this
    # column is for. THE SPLIT SETTLES THE REST OF THAT ARGUMENT: the
    # gamete probabilities were also printing a click early, because the
    # single plate sat on the FRAME slide and carried them. They are now on
    # stage 2, which is the BUILD slide that reads them, and stage 1 shows
    # the locus with no gamete chips at all.
    # THE BRIDGE, AND NOT IN THE FAINTEST TYPE ON THE PLATE. The slides in
    # this segment carry Noble's own cropped figures, which axis-label this
    # quantity P; we do not alter published figures, so the figure says
    # once whose letter is whose. This replaces the old "P is Noble's
    # homing efficiency, not this hour's packaging advantage", which named
    # the collision instead of removing it (deck-bar B1).
    ax.text(0.16, 0.60, "Noble prints $h$ as P. His figures are shown as "
                        "published.",
            color=INK, ha="left", va="top", fontsize=LBL, linespacing=1.3)


def fig_homing(stem="s25_homing"):
    """How a homing drive copies itself -- the MECHANISM, which segment 5
    argued about without ever drawing.

    `s25_locus_*` draw the OUTCOME: the gamete fan, the struck-out W. They
    never show the event that produces it, so "super-Mendelian" arrived as
    a ratio rather than as something that happens to a chromosome.

    THE TWO REPAIRS BRANCH, THEY DO NOT CHAIN. A first pass laid the four
    stages in one row, which drew an arrow from the DD cell to the DR cell
    and said that homing TURNS INTO resistance. They are alternative
    repairs of the same cut and the plate has to fork.

    LAYOUT BUDGET. The box is 10.2 x 2.82 and settles to about 0.155 data
    units per character of 20 pt type. A chip pair at CH = 0.34 is 0.76
    tall, so two forked rows plus clearance fit the 2.82 where a pair at
    0.44 would not. Outcome labels sit to the RIGHT of their chips rather
    than under them, because stacking a two-line label under each fork
    needs 1.6 units of height that is not there.

    The consequence sentence is NOT on the plate: 50 characters is 7.8
    units and crosses a column wherever it goes. It belongs in the deck's
    rows beside the figure.

    NOTATION follows `_locus_plate`: alleles keep Noble's W, D and R and
    appear only inside genotypes or noun phrases, never as bare letters
    that could be read as quantities; homing efficiency is h, never P.

    MODEL: Noble 2018's homing step under the every-cut-happens assumption
    the deck states on its own slide -- every wild-type allele in a
    heterozygote is cut, and only its REPAIR is in question.
    """
    from matplotlib.patches import Rectangle, FancyArrowPatch
    _W, _D, _R = MUTED, GREEN, CYAN
    CW, CH, GAP = 1.14, 0.34, 0.08
    PH = 2 * CH + GAP

    fig, ax = _locus_panel()

    def chip(x, y, col, dashed=False):
        ax.add_patch(Rectangle((x, y), CW, CH,
                               facecolor=PAGE if dashed else col,
                               edgecolor=RED if dashed else "none",
                               lw=2.0, ls=(0, (3, 2)) if dashed else "-",
                               zorder=5))

    def pair(x, ybot, top, bot, bot_dashed=False):
        chip(x, ybot + CH + GAP, top)
        chip(x, ybot, bot, dashed=bot_dashed)

    def arrow(x0, y0, x1, y1, col=MUTED):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                     mutation_scale=15, color=col, lw=2.0,
                                     zorder=6))

    X0, X1, X2 = 0.30, 2.80, 5.45
    YM = 1.28                      # the two left stages
    YU, YL = 2.22, 0.42            # the fork
    midM, midU, midL = YM + PH / 2, YU + PH / 2, YL + PH / 2

    pair(X0, YM, _D, _W)
    _txt(ax, X0 + CW / 2, YM + PH + 0.10, "drive / wild type", color=MUTED,
         va="bottom")
    _txt(ax, X0 + CW / 2, YM - 0.16, "a WD\ngermline cell", va="top")

    arrow(X0 + CW + 0.12, midM, X1 - 0.12, midM)
    pair(X1, YM, _D, PAGE, bot_dashed=True)
    _txt(ax, X1 + CW / 2, YM - 0.16, "the wild-type\nallele is cut",
         color=RED, va="top")

    arrow(X1 + CW + 0.12, midM + 0.10, X2 - 0.12, midU - 0.06, _D)
    arrow(X1 + CW + 0.12, midM - 0.10, X2 - 0.12, midL + 0.06, _R)
    _txt(ax, 4.70, midU + 0.06, "h", color=_D, va="bottom")
    _txt(ax, 4.92, 0.84, "1 \u2212 h", color=_R, va="top")

    pair(X2, YU, _D, _D)
    _txt(ax, X2 + CW + 0.22, YU + CH, "repair copies the drive",
         color=_D, ha="left", va="center")
    pair(X2, YL, _D, _R)
    _txt(ax, X2 + CW + 0.22, YL + CH, "repair fails: resistance",
         color=_R, ha="left", va="center")

    _save(fig, stem)


def fig_locus_series(stem="s25_locus"):
    """Segment 5's two stages: the locus, then what it sends on.

    `s25_locus_1` is the FRAME plate -- the three allele classes and the
    diploid locus from segment 1, drawn, with NO gamete chips. Nothing on
    it is unlabelled, so deck-bar D2 costs this stage nothing, and it does
    not print the next slide's arithmetic a click early.

    `s25_locus_2` is the BUILD plate -- the same drawing with the germline
    bracket and the gamete fan added, carrying `drive, (1+h)/2`,
    `resistant, (1-h)/2` and `no W gamete`. Those three stay: D2 asks for
    every drawn symbol to be labeled in its own figure, and without them
    the right half is three unexplained squares.

    THE SIZE GUARD IS THE POINT OF READING IT BACK. A derivation series
    that changes size between stages resizes the picture while the algebra
    advances, which is what `derivation_fig` exists to prevent and what
    `series_consistency` catches once a deck places both stems. Until it
    does, the two stems report `placement unknown` and that check cannot
    run -- so the equality is asserted here, against the bytes savefig
    writes, rather than waited for.
    """
    sizes = []
    for i, gam in enumerate((False, True), start=1):
        fig, ax = _locus_panel()
        _locus_plate(ax, gametes=gam)
        sizes.append(_save(fig, f"{stem}_{i}"))
    if sizes[0] != sizes[1]:
        print(f"  !! {stem}_*: stage 1 saved {sizes[0][0]:.3f} x "
              f"{sizes[0][1]:.3f} in against stage 2's {sizes[1][0]:.3f} x "
              f"{sizes[1][1]:.3f} -- the plate will resize between clicks. "
              f"Something in one stage reaches outside the data box.")



# =====================================================================
# THE TWO SESSION-24 RECALL PANELS, slides 2 and 3.
#
# WHY THEY LIVE IN THIS MODULE. They are drawn for session 25's opener, not
# for session 24's deck, and `figures/s24_communities.py` is not ours to
# edit. Both reuse session 24's own visual language so the room recognises
# them -- predator TEAL, prey CYAN, signals AMBER, "rescues" GREEN, "kills"
# RED, exactly `fig_pp_step`'s ring of four -- and both come out of
# `posb.communities`, the tested library, rather than a re-derivation.
#
# WHAT THEY REPLACE, and why. Both openers asked the room to recall session
# 24 and both drew session 24's CONCLUSIONS instead of its SYSTEM, which is
# deck-bar F1: a system the slide argues about is drawn on that slide.
#   - slide 2 asked "what quantity was D, and what happened to the predator"
#     over a leading-Re-lambda-against-D plot under an eleven-symbol
#     parameter header. No chemostat, no strains, no signal, and NO PREDATOR
#     anywhere in the picture the question is about. Not one of the eleven
#     symbols is needed to answer it.
#   - slide 3 asked "you set the signals to steady state and the oscillation
#     vanished -- what had you discarded" over tr J against D (the algebraic
#     shadow of the answer) beside |tr J| against the closed form over 4000
#     random fixed points -- a builder's parity check, projected into a
#     lecture hall, with its purpose stated nowhere. That check belongs in
#     the test suite, where a failure is loud and a pass is silent.
# =====================================================================

# FIG. 3B'S OWN DILUTION SCHEDULE, AND ONLY IT. MEASURED, s24 NUMBERS.md 3.4:
# predator Top10F', prey Top10F', D = 0.15, then 0.23 at ~150 h, then 0.31 at
# ~250 h -- coexistence, then a damped oscillation of about 30 h, then
# predator washout.
#
# THE FIRST CUT OF THIS FIGURE ALSO PLOTTED 0.11 AND 0.20 and credited all
# five to Fig. 3B, which is wrong twice. Those two are **Fig. 3A**, a
# DIFFERENT STRAIN PAIR (predator MG1655, prey Top10F'), and in 3A it is the
# PREY that falls to about zero after the switch to 0.20 -- so the panel was
# drawing a filled "prey present" marker at a dilution rate where the
# experiment measured the prey collapsing, in somebody else's experiment. No
# gate in this repo can see that: it is a fact about which panel a number
# came from. It came from reading NUMBERS.md 3.4 rather than the summary
# table in 20.5, which lists all five rates in one column.
#
# Nothing here is the DEPOSITED MODEL's boundary, which loses coexistence at
# D = 0.176 (s24 NUMBERS.md 20.4). The model and the experiment disagree at
# four of the five rates in 20.5 and agree only at washout -- which is
# exactly the one this figure draws. Keeping the measured value out of the
# model's panel and the model out of the measured panel is the whole of the
# provenance discipline here, and it is why the two live in separate panels
# with separate titles.
BAL_D = (0.15, 0.23, 0.31)
BAL_WASHOUT = 0.31


def _ink_on(color):
    """White or INK, whichever the fill can carry. Relative luminance, sRGB.

    CYAN is light and TEAL is dark, and the same hard-coded "white" on both
    put near-invisible text on one of them. Asked rather than assumed.
    """
    r, g, b = (int(color[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
           for c in (r, g, b)]
    lum = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    return INK if lum > 0.32 else "white"


def _node(ax, x, y, text, color):
    return ax.text(x, y, text, ha="center", va="center", fontsize=LBL,
                   color=_ink_on(color), zorder=6, linespacing=1.15,
                   bbox=dict(boxstyle="round,pad=0.36", facecolor=color,
                             edgecolor="none"))


def _box_in(fig, ax, art):
    """One label's drawn plate as (half-width, half-height) in INCHES.

    The s24 lesson, re-implemented rather than imported because that module
    is not ours to touch: a hand-coded half-extent there was wrong by a
    factor of two and an arrowhead finished 50 px INSIDE the opaque plate it
    pointed at, on six slides. There is no constant to re-guess -- the
    renderer is asked where it put the plate.
    """
    bb = art.get_bbox_patch().get_window_extent(fig.canvas.get_renderer())
    return bb.width / fig.dpi / 2.0, bb.height / fig.dpi / 2.0


def fig_recall_chemostat(name="s25_recall_chemostat"):
    """Session 24's SYSTEM, for the slide that asks what D was and what it did.

    LEFT, the architecture: a chemostat fed and drained at rate D, with the
    four species of BIOMD0000000296 inside it -- predator C1, prey C2, and
    the two acyl-homoserine lactones they talk with. The loop is the one
    session 24 built: the predator makes 3OC12HSL, which KILLS the prey; the
    prey makes 3OC6HSL, which RESCUES the predator from a death rate it
    cannot survive alone. D leaves the vessel in two senses at once and both
    arrows carry it: it washes cells out and it washes SIGNAL out, which is
    why it sits in all four of the deposit's removal terms.

    RIGHT, the answer the opener is fishing for: the three dilution rates of
    Balagadde's Fig. 3B, in the order that one reactor ran them, MEASURED.
    Both strains at 0.15 and at 0.23; at 0.31 the predator is gone and the
    prey is not. That is predator washout, and the deposited model agrees
    with the experiment at this one rate (s24 NUMBERS.md 20.5) -- which is
    why it is safe to put the measured point beside the deposited
    architecture, and why no OTHER rate on that axis is claimed to be
    anything the model reproduces. The slide's own speaker note already
    names these three and no others (deck-bar F8: when a note and its slide
    make the same claim they are read against each other).

    THE ELEVEN-SYMBOL PARAMETER HEADER IS GONE. IPTG, d1, k_A2, k_c1, k_c2,
    d2, C_m, K1, K2, k_A1, d_AA1 and d_AA2 were printed over the panel this
    replaces, and not one of them is needed to say what D was or what raising
    it did. A retrieval slide needs the accession and nothing else.

    THE VERBS ARE INSIDE THE SIGNAL BOXES, not floating beside the arrows.
    The first cut put "makes", "kills" and "rescues" at the corners of a
    diamond, the way s24's derivation column does -- and s24's column is
    5.4 x 4.95 in while this panel is about 5.6 x 2.8, so the diamond's three
    rows of two-line plates did not fit the height and every label landed on
    another. Four plates, four arrows, no floating text (deck-bar D5d's
    closing note: cut text and move it into something that already exists).

    THE PANEL IS LAID OUT IN INCHES, measured after `tight_layout` reaches
    its fixed point, so one data unit is one inch and a 20 pt line is
    0.28 of one. A 0-100 drawing square mapped into a wide, short panel makes
    the vertical unit twice the horizontal one, which is how the first cut
    came out with the ring collapsed on itself.
    """
    # 4.50, UP FROM 4.34, AND THE GUARD BELOW IS WHY. Raising both titles by
    # 10 pt to clear the inflow label took that 0.11 in straight off the
    # shared axes height, and the vessel's own fit guard then reported
    # 0.17 in of vertical room for the arrows against the 0.28 it needs --
    # deck-gauntlet 5.5b, a fix creating the next defect one line below it.
    # The saved file comes out 4.08 in, inside the deck's 4.14 in band, so
    # the height is bought from padding rather than from the type.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.50),
                                   gridspec_kw={"width_ratios": [1.58, 1.0]})
    _recall_ruler(axR)
    axL.axis("off")
    # pad=16, NOT the default 6, AND ON BOTH TITLES. `figure_fit` reported
    # "'medium in, $D$' touches 'the chemostat ...'" -- measured, the two
    # boxes did not overlap, they cleared by 0.043 in, which is 6.9 px at
    # this dpi and inside the gate's threshold. A clearance that small is a
    # collision that has not happened yet. The alternative was widening the
    # vessel's top strip, which costs 0.24 in of interior height off a panel
    # that has about 0.4 in spare; raising the title costs 0.11 in of figure
    # height, and the saved file stays inside the deck's 4.14 in band. Both
    # titles get it or the two sit at different heights across the seam.
    axL.set_title("the chemostat  ·  BIOMD0000000296", fontsize=LBL,
                  color=MUTED, pad=16.0)
    # THE BOX HAS TO STOP MOVING BEFORE IT CAN BE MEASURED. Both axes share a
    # height set by the RIGHT panel's xlabel and ticks, so the left panel's
    # drawing area is not knowable from figsize; and `tight_layout` is
    # content-dependent and not idempotent (deck-bar D5a item 3), so it is
    # run to its fixed point first.
    _settle(fig)
    fig.canvas.draw()
    bb = axL.get_window_extent(fig.canvas.get_renderer())
    W, H = bb.width / fig.dpi, bb.height / fig.dpi
    axL.set_xlim(0.0, W); axL.set_ylim(0.0, H)
    _recall_vessel(fig, axL, W, H, name)
    # NOTHING THE LEFT PANEL DRAWS LEAVES ITS AXES, so `tight_layout` has
    # nothing new to respond to and the inch mapping stays true through the
    # save. Asserted rather than assumed, because if it ever stops being true
    # every coordinate below is silently wrong.
    _settle(fig)
    fig.canvas.draw()
    bb2 = axL.get_window_extent(fig.canvas.get_renderer())
    moved = max(abs(bb2.width - bb.width), abs(bb2.height - bb.height)) / fig.dpi
    if moved > 0.02:
        print(f"  !! {name}: the left axes moved {moved:.3f} in after its "
              f"contents were drawn, so the inch-coordinate layout no longer "
              f"matches the axes it was computed against. Re-measure.")
    _save(fig, name)


def _px_to_in_x(ax, x_data, fig):
    """Companion to `_px_to_in` for the horizontal direction."""
    return ax.get_window_extent(fig.canvas.get_renderer()).x0 / fig.dpi + x_data


def _px_to_in(ax, y_data, fig):
    """This panel's data unit IS the inch, so y in data is y in inches from
    the axes' bottom -- but the clearance above is measured in FIGURE inches,
    so the axes' own origin has to be added back."""
    return ax.get_window_extent(fig.canvas.get_renderer()).y0 / fig.dpi + y_data


def _recall_vessel(fig, ax, W, H, name):
    """The vessel and its four species, laid out in inches inside (W, H)."""
    from matplotlib.patches import FancyBboxPatch
    strip = 0.30                       # top and bottom, for the D arrows
    vx0, vx1 = 0.03, W - 0.03
    vy0, vy1 = strip, H - strip
    nodes = {
        "C1": _node(ax, 0, 0, "predator\n$C_1$", TEAL),
        "A1": _node(ax, 0, 0, "$A_1$  3OC12HSL\nkills $C_2$", AMBER),
        "C2": _node(ax, 0, 0, "prey\n$C_2$", CYAN),
        "A2": _node(ax, 0, 0, "$A_2$  3OC6HSL\nrescues $C_1$", AMBER)}
    fig.canvas.draw()
    half = {k: _box_in(fig, ax, a) for k, a in nodes.items()}
    hb = max(h for _, h in half.values())
    # A RECTANGLE LOOP, clockwise: C1 -> A1 -> C2 -> A2 -> C1. Two rows, two
    # columns, each column as wide as the wider of its two plates.
    cw0 = max(half["C1"][0], half["A2"][0])
    cw1 = max(half["A1"][0], half["C2"][0])
    # 0.06 OF WALL MARGIN, DOWN FROM 0.15, AND THE RENDERED SLIDE IS WHY.
    # At 0.15 the gap between the two columns came out 0.74 in and the word
    # "makes" is 0.72 in wide, so each horizontal arrow's label cleared the
    # plate beside it by 0.01 in -- deck-bar D5a item 1, a label striking a
    # box edge FROM OUTSIDE, which `figure_fit` structurally cannot see: it
    # compares text with text and text inside a patch, never text against a
    # patch's border. It was found by rendering the page, not by the gate.
    inner = (vx1 - vx0) - 0.12
    gap_x = inner - 2 * cw0 - 2 * cw1
    x_l = vx0 + 0.06 + cw0
    x_r = vx1 - 0.06 - cw1
    y_hi = vy1 - 0.10 - hb
    y_lo = vy0 + 0.10 + hb
    gap_y = (y_hi - hb) - (y_lo + hb)
    print(f"     {name}: vessel box {W:.2f} x {H:.2f} in, plates leave "
          f"{gap_x:.2f} in across and {gap_y:.2f} in down for the arrows")
    if gap_x < 0.55 or gap_y < 0.28:
        print(f"  !! {name}: the vessel's four plates leave {gap_x:.2f} in "
              f"across and {gap_y:.2f} in down for the four arrows, against "
              f"0.55 and 0.28 needed. Cut a word from a plate -- do NOT "
              f"shrink the type (deck-gauntlet 5.3).")
    for k, (x, y) in (("C1", (x_l, y_hi)), ("A1", (x_r, y_hi)),
                      ("C2", (x_r, y_lo)), ("A2", (x_l, y_lo))):
        nodes[k].set_position((x, y))
    ax.add_patch(FancyBboxPatch((vx0, vy0), vx1 - vx0, vy1 - vy0,
                                boxstyle="round,pad=0,rounding_size=0.10",
                                facecolor="white", edgecolor=MUTED, lw=2.6,
                                zorder=1))
    # NO CULTURE LINE. A dashed rule across the top of the vessel was drawn
    # to make it read as liquid, and it is an unlabelled symbol on a figure
    # whose other four symbols are all named (deck-bar D2) -- sitting 0.1 in
    # above two plates, where at page size it reads as a divider between the
    # top row and the rest. The vessel reads as a vessel from its inflow and
    # outflow arrows alone.
    fig.canvas.draw()
    half = {k: _box_in(fig, ax, a) for k, a in nodes.items()}
    pos = {k: nodes[k].get_position() for k in nodes}

    def arrow(a, b, color, axis):
        (ax0, ay0), (ax1, ay1) = pos[a], pos[b]
        ha, hbb = half[a], half[b]
        if axis == "x":
            s = 1.0 if ax1 > ax0 else -1.0
            p0 = (ax0 + s * (ha[0] + 0.05), ay0)
            p1 = (ax1 - s * (hbb[0] + 0.05), ay1)
        else:
            s = 1.0 if ay1 > ay0 else -1.0
            p0 = (ax0, ay0 + s * (ha[1] + 0.05))
            p1 = (ax1, ay1 - s * (hbb[1] + 0.05))
        ax.annotate("", xy=p1, xytext=p0, zorder=4,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.8,
                                    shrinkA=0, shrinkB=0, mutation_scale=20))
        return p0, p1

    (mx0, my0), (mx1, _) = arrow("C1", "A1", AMBER, "x")
    arrow("A1", "C2", RED, "y")
    (nx0, ny0), (nx1, _) = arrow("C2", "A2", AMBER, "x")
    arrow("A2", "C1", GREEN, "y")
    # "makes" twice, on the two horizontal arrows and nowhere else: the other
    # two verbs are inside the plates they belong to. Each sits ABOVE its own
    # arrow, in a gap measured to hold it.
    # NO PLATE. A page-colored plate is for text a curve would strike
    # through (deck-bar D5b); cropped at 3x, these two sit in empty vessel
    # with the arrow entirely below them, so the plate erased nothing and
    # printed a pale rectangle for it. The clearance that makes that safe is
    # MEASURED TO THE STROKE, not to the arrow's center line -- a 2.8
    # linewidth is painted about 0.019 in either side of it, and deck-bar
    # D5e is a label that cleared every vertex and still bleached the curve.
    for xa, xb, ya in ((mx0, mx1, my0), (nx0, nx1, ny0)):
        t = ax.text((xa + xb) / 2.0, ya + 0.07, "makes", ha="center",
                    va="bottom", color=AMBER, fontsize=LBL, zorder=7)
        fig.canvas.draw()
        tb = t.get_window_extent(fig.canvas.get_renderer())
        clear = tb.y0 / fig.dpi - _px_to_in(ax, ya, fig) - 0.019
        if clear < 0.03:
            print(f"  !! {name}: \"makes\" clears its own arrow's painted "
                  f"edge by {clear:.3f} in. Raise it or shorten a plate.")
        # AND THE SIDEWAYS CLEARANCE, which is the one the gate cannot see.
        # Measured from the word's own drawn box to the two plate edges it
        # sits between, in the same inches the plates were measured in.
        side = min(tb.x0 / fig.dpi - _px_to_in_x(ax, min(xa, xb), fig),
                   _px_to_in_x(ax, max(xa, xb), fig) - tb.x1 / fig.dpi)
        if side < 0.08:
            print(f"  !! {name}: \"makes\" clears the plate beside it by "
                  f"{side:.3f} in. `figure_fit` compares text with text and "
                  f"never with a patch BORDER (deck-bar D5a item 1), so "
                  f"nothing else will report this. Widen the column gap or "
                  f"cut a word from a plate.")
    # IN AND OUT, BOTH AT RATE D, because the answer to the slide's first
    # question is that D is the rate the vessel is fed and drained at. The
    # labels sit BESIDE their arrows in the 0.30 in strips rather than above
    # them, which is the only place a 20 pt line fits on a panel this short.
    # THE HEADS CROSS THE WALL. Stopping 0.02 in short of it drew two short
    # chevrons floating beside the vessel, which is a picture of an arrow
    # rather than of a flow; a feed arrow that does not enter the vessel does
    # not say the medium goes in. They stop 0.09 in inside, clear of the top
    # row of plates, which begins 0.10 in further down.
    ax.annotate("", xy=(vx0 + 0.55, vy1 - 0.09), xytext=(vx0 + 0.55, H),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=3.0,
                                shrinkA=0, shrinkB=0, mutation_scale=20))
    ax.annotate("", xy=(vx1 - 0.55, 0.0), xytext=(vx1 - 0.55, vy0 + 0.09),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=3.0,
                                shrinkA=0, shrinkB=0, mutation_scale=20))
    ax.text(vx0 + 0.70, vy1 + strip / 2.0, "medium in,  $D$", ha="left",
            va="center", fontsize=LBL, color=INK, zorder=7)
    ax.text(vx1 - 0.70, vy0 - strip / 2.0, "culture out,  $D$", ha="right",
            va="center", fontsize=LBL, color=INK, zorder=7)


def _recall_ruler(ax):
    """Balagadde's five measured dilution rates, and where the predator stops."""
    y_pred, y_prey = 0.48, 0.22
    ax.set_xlim(0.08, 0.38); ax.set_ylim(0.0, 1.0)
    ax.set_yticks([])
    ax.set_xticks([0.1, 0.2, 0.3])
    ax.set_xlabel("dilution rate  $D$   (h$^{-1}$)", fontsize=LBL)
    ax.grid(True, axis="x", color=RULE, lw=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    # THE ROW NAMES ARE A LEGEND, NOT y TICK LABELS. As tick labels,
    # "predator $C_1$" and "prey $C_2$" took 1.70 in of WIDTH off the left of
    # a 3.3 in panel, and `tight_layout` gave up -- it warned that it "cannot
    # make Axes width small enough", and a gate whose own measurement is
    # warned to be unreliable is not a gate (deck-gauntlet 5.7). In the
    # legend they cost height in a strip no marker reaches.
    # PREDATOR FIRST, because the legend is built in draw order and the
    # predator's row is the TOP one. Drawn prey-first the key read
    # "prey  predator" above rows running predator, prey -- the colors
    # disambiguate it and the POSITIONS contradict it, which is a reader
    # matching by position getting the wrong answer on a retrieval slide.
    for j, d in enumerate(BAL_D):
        if d < BAL_WASHOUT:
            ax.plot([d], [y_pred], "o", color=TEAL, ms=17, mec=INK, mew=1.4,
                    zorder=5, label="predator" if j == 0 else None)
        else:
            # GREYED, AND OPEN. The predator is not at a low density here, it
            # is gone, and a pale filled dot reads as "a bit less".
            ax.plot([d], [y_pred], "o", mfc="white", mec=MUTED, mew=2.6,
                    ms=17, zorder=5)
        ax.plot([d], [y_prey], "o", color=CYAN, ms=17, mec=INK, mew=1.4,
                zorder=5, label="prey" if j == 0 else None)
    ax.annotate("", xy=(BAL_WASHOUT - 0.014, y_pred),
                xytext=(0.252, y_pred), zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.4,
                                shrinkA=0, shrinkB=0, mutation_scale=18))
    # ABOVE the predator row and RIGHT of the legend: the two free corners of
    # this panel are upper-left (legend) and the strip between the legend and
    # the predator row. `figure_fit` compares text with text inside one axes
    # and would catch a legend collision, but it does NOT compare text with a
    # marker (deck-bar D5a item 1 is the same hole for patches), so the
    # clearance to the open circle is measured here instead: the circle is
    # 17 pt across, 0.12 in of radius, and 0.62 - 0.46 of this axes is
    # 0.45 in.
    _tag(ax, 0.985, 0.70, "washed out", MUTED, ha="right", va="center",
         plate=False)
    # ONE ROW, NOT TWO. Stacked, the legend reached down to 0.70 of the axes
    # and `figure_fit` reported it touching "washed out" -- which it had NOT
    # done one edit earlier, before the title pad shortened the axes by
    # 0.11 in and pulled every axes-fraction gap in with it. In one row it is
    # 0.13 of the axes deep instead of 0.26, and the three blocks below it
    # each clear the next by about 0.28 in.
    ax.legend(loc="upper left", ncol=2, frameon=False, fontsize=LBL,
              numpoints=1, handletextpad=0.4, borderpad=0.1,
              columnspacing=1.4)
    ax.set_title("measured  ·  Fig. 3B", fontsize=LBL, color=MUTED,
                 pad=16.0)


# Session 24's own dilution rate for this item, and the reason it is this one
# and not the deposit's 0.1125. D = 0.11 h^-1 is one of BALAGADDE'S FIVE
# EXPERIMENTAL RATES, so it is the same axis slide 2 just drew; and s24
# NUMBERS.md 20.5 records the deposited model's limit cycle there to the
# digit -- period 168.1 h, C1 swinging 0.020 to 25.98 over 47 cycles with a
# standard deviation of 0.01 h. Every number this figure prints is in that
# file. At the deposit's own 0.1125 the period would be 166.1 h, which is
# OURS and nowhere recorded, and buying a round number with an unsourced one
# is a bad trade on a retrieval slide.
QSSA_D = 0.11
QSSA_T = 700.0          # just over four cycles of the 168.1 h limit cycle


def fig_recall_qssa(name="s25_recall_qssa"):
    """The thing the approximation discarded, DRAWN, for slide 3's opener.

    Two integrations of the same circuit at the same dilution rate from the
    same initial condition, differing in one thing: whether the two quorum
    signals keep their own dynamics. LEFT they do, and the community
    oscillates for ever. RIGHT they are set to quasi-steady state -- session
    4's move, applied to a molecule outside the cell -- and the swing dies
    inside a hundred hours. That is what was discarded: the lag between a
    population and its own signal.

    WHY THIS AND NOT THE ALGEBRA. The panels this replaces were tr J against
    D -- the shadow the answer casts on the trace of a Jacobian -- and a
    scatter of |tr J| against the closed form over 4000 random interior fixed
    points, which is a BUILDER'S PARITY CHECK and belongs in the test suite,
    where a failure is loud and a pass is silent. Neither draws the thing the
    question asks about. A lost oscillation is a picture of an oscillation
    and then a picture without one.

    WHAT THE RIGHT PANEL MAY NOT BE CALLED. It is not "no oscillation". The
    two-state reduction's Jacobian at the focus has a COMPLEX pair,
    -0.0617 +/- 0.2319i, so it rings at about 27 h and the amplitude falls
    5.3x a cycle -- three or four visible swings and then nothing. What s24
    NUMBERS.md 20.3 establishes is that tr J = -(kc1 C1 + kc2 C2)/Cm is
    strictly negative at EVERY interior fixed point of EVERY parameter set,
    so the pair can never cross and there is no Hopf at any D. The panel
    title says "damps out", which is what the curve does; "the oscillation is
    gone" would be the slide contradicting its own picture.

    AND THE FIXED POINT DOES NOT MOVE. Substituting the quasi-steady-state
    signals is exact AT a fixed point, so both panels orbit or settle on the
    same (C1*, C2*) = (5.177, 20.500). It is drawn in neither panel, because
    an unlabelled line is a symbol with no label (deck-bar D2) and a labeled
    one costs a text block the left panel has no clear room for; it is the
    speaker note's sentence, not the figure's.
    """
    from scipy.integrate import solve_ivp
    from posb.communities import (pp_params, predator_prey_model,
                                  pp_qss_model, PP_INITIAL)
    p = pp_params(D=QSSA_D)
    t = np.linspace(0.0, QSSA_T, 7001)

    def go(f, y0):
        s = solve_ivp(lambda tt, y: f(y, p), [0.0, QSSA_T], list(y0),
                      t_eval=t, rtol=1e-10, atol=1e-13, method="LSODA")
        if not s.success:
            raise RuntimeError(f"{name}: {s.message}")
        return s.y

    full = go(predator_prey_model, PP_INITIAL)
    qss = go(pp_qss_model, PP_INITIAL[:2])
    # THE RECORDED NUMBERS, CHECKED HERE RATHER THAN TRUSTED. s24 NUMBERS.md
    # 20.5 gives period 168.1 h and C1 swinging 0.020 to 25.98 at this D. If
    # the library ever stops reproducing them the figure says so at build
    # time instead of printing a caption that is no longer true.
    late = t > 200.0
    pk = [i for i in range(1, len(t) - 1) if late[i]
          and full[0][i] > full[0][i - 1] and full[0][i] > full[0][i + 1]]
    per = float(np.mean(np.diff(t[pk]))) if len(pk) > 1 else float("nan")
    lo, hi = float(full[0][late].min()), float(full[0][late].max())
    for what, got, want, tol in (("period", per, 168.1, 1.0),
                                 ("C1 trough", lo, 0.020, 0.004),
                                 ("C1 peak", hi, 25.98, 0.6)):
        if not abs(got - want) <= tol:
            print(f"  !! {name}: {what} integrates to {got:.4g}, but s24 "
                  f"NUMBERS.md 20.5 records {want} at D = {QSSA_D}. The "
                  f"caption prints the recorded value; one of the two is "
                  f"now wrong and the figure must not ship until it is "
                  f"settled.")
    # AND THE THIRD NUMBER ON THE FIGURE. "damps out inside 100 h" is OURS --
    # it is not in NUMBERS.md, because the two-state reduction's TRANSIENT is
    # not something s24 ever had to quantify; 20.3 only establishes that the
    # trace is strictly negative, which fixes the sign and not the clock. So
    # it is checked here against the curve it describes: the residual swing
    # in C1 after 100 h, as a fraction of where it settles.
    rest = float(qss[0][-1])
    tail = qss[0][t >= 100.0]
    resid = float(np.max(np.abs(tail - rest)) / rest)
    if resid > 0.02:
        print(f"  !! {name}: the quasi-steady-state panel still swings "
              f"{resid:.1%} of its resting value after 100 h, and the panel "
              f"title says it damps out inside 100 h. Change the title or "
              f"the number.")

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.40), sharey=True)
    for ax, y, title in (
            (axL, full, "signals keep their dynamics\n"
                        "sustained, period 168 h"),
            (axR, qss, "signals at quasi-steady state\n"
                       "damps out inside 100 h")):
        # SERIES NAMES WITHOUT SYMBOLS. "predator $C_1$" and "prey $C_2$" in
        # two columns measured 4.28 in inside a 4.4 in panel -- inside by
        # 0.12 in, which is not a margin, it is luck. The words name the two
        # curves on their own and the symbols are not drawn on this figure,
        # so deck-bar D2 is not engaged by dropping them.
        ax.plot(t, y[0], color=TEAL, lw=3.0, label="predator", zorder=4)
        ax.plot(t, y[1], color=CYAN, lw=3.0, label="prey", zorder=3)
        ax.set_yscale("log")
        # 1000 AT THE TOP IS NOT SLACK. The data reach 72, and the decade
        # above it is the only strip clear in BOTH panels -- which is where
        # the series names go, so that neither panel asks the room to carry a
        # legend across the gap (deck-bar D5d item 5, and the cross-axes hole
        # of D5e). Cut text, move it into a region the curves cannot enter.
        ax.set_ylim(0.01, 1000.0)
        ax.set_xlim(0.0, QSSA_T)
        ax.set_xticks([0, 200, 400, 600])
        ax.set_xlabel("hours in the chemostat", fontsize=LBL)
        ax.grid(True, which="major", color=RULE, lw=0.5)
        ax.set_axisbelow(True)
        ax.set_title(title, fontsize=LBL, color=MUTED)
        ax.legend(loc="upper center", ncol=2, frameon=False, fontsize=LBL,
                  handlelength=1.4, columnspacing=1.3, borderpad=0.1,
                  handletextpad=0.5)
    # ONE y LABEL, ON THE LEFT, and `sharey` is what makes that honest: the
    # two panels are adjacent, aligned and on one axis, so there is no gap to
    # carry a scale across -- unlike `fig_design_space`, whose two panels are
    # 1.15 in apart and therefore need the label twice (deck-bar D2). A
    # second label on the right would sit against hidden ticks and name an
    # axis the reader cannot read numbers off.
    axL.set_ylabel("density  ($C_m$ = 100)", fontsize=LBL)
    # The right panel is flat below 1.9 from end to end, which is the one
    # region of either panel no curve can reach.
    # TWO LINES, NOT ONE. On one line this ran 4.0 in across a 4.3 in panel
    # and finished hard against the figure's own right edge -- it was setting
    # the saved width, which is the dimension the deck's band divides by
    # (deck-bar D5d item 5).
    _tag(axR, 0.03, 0.03,
         f"BIOMD0000000296\n$D$ = {QSSA_D} h$^{{-1}}$", MUTED, plate=False)
    _recall_seams(fig, (axL, axR), name)
    _save(fig, name)


def _recall_seams(fig, axes, name):
    """The three things no gate on this repo looks at, measured here.

    `figure_fit` loops PER AXES and compares text with text inside one of
    them, so two panel titles meeting in the middle of a figure are invisible
    to it (deck-bar D5d item 2) and so is anything crossing the seam
    (D5e). It also treats the axes title as frame and drops it from the
    collision list, and it never enters a LEGEND as a box at all -- which on
    this figure is the one block of text sitting inside the data area.
    """
    r = fig.canvas.get_renderer()
    fig.canvas.draw()
    # 1. title against title, across the seam.
    t0, t1 = (a.title.get_window_extent(r) for a in axes)
    gap = (t1.x0 - t0.x1) / fig.dpi
    if gap < 0.15:
        print(f"  !! {name}: the two panel titles are {gap:.3f} in apart "
              f"across the seam (overlapping if negative). `figure_fit` "
              f"cannot see this -- it compares text within ONE axes. Cut "
              f"words from a title; do NOT shrink the type.")
    for ax in axes:
        lg = ax.get_legend()
        if lg is None:
            continue
        lb = lg.get_window_extent(r)
        # 2. legend against the curves it names. Sampled on the RENDERED
        #    path, not on the data, because that is what the eye reads.
        hit = 0
        for ln in ax.lines:
            pts = ax.transData.transform(ln.get_xydata())
            inside = ((pts[:, 0] >= lb.x0) & (pts[:, 0] <= lb.x1) &
                      (pts[:, 1] >= lb.y0) & (pts[:, 1] <= lb.y1))
            hit += int(inside.sum())
        if hit:
            print(f"  !! {name}: the legend covers {hit} plotted points of "
                  f"its own curves. Raise the top of the y axis or move it.")
        # 3. legend against the title above it.
        tb = ax.title.get_window_extent(r)
        v = (tb.y0 - lb.y1) / fig.dpi
        if v < 0.05:
            print(f"  !! {name}: the legend sits {v:.3f} in under its own "
                  f"panel title.")

# =====================================================================
# SEGMENT 4 -- THE VALLEY IN D, DRAWN AS A STEADY STATE AND NOT AS A
# 360-DAY WINDOW.
#
# WHY THIS FIGURE EXISTS, AND WHY IT IS NOT W03's Fig. 2a REDRAWN. The
# first attempt at this slide redrew Fig. 2a's five time courses from the
# printed equations and was refused: the LEVELS reproduce but the TRANSIENT
# CLOCK IS WRONG BY A FACTOR OF TWO -- the HIV minimum lands at day
# 28/50/53/63 against the paper's 51/84/103/115. The cause is pinned and is
# not ours: the printed equations omit the 1.5-day eclipse phase the
# simulations used ("equations 1 to 6 were altered accordingly [see SI]"),
# and the SI is not in this repo. An Erlang eclipse closes about half that
# gap and then saturates, so the shape of the delay is wrong too. A figure
# whose clock is 2x fast cannot sit one click from the paper's own crop of
# Fig. 2b.
#
# WHAT A STEADY STATE BUYS. A set point is a fixed point, and a DELAY
# CANNOT MOVE A FIXED POINT -- an eclipse phase changes when a trajectory
# arrives, not where. Verified rather than asserted: an Erlang(m) eclipse
# of mean 1.5 d inserted on all three infection events of [1]-[6] leaves
# every set point on this curve IDENTICAL TO ALL PRINTED DIGITS, for
# m = 1, 2, 5 and 20, when eclipse-phase cells do not die. If they die at
# the uninfected rate d = 0.02/day -- and with k and lambda re-back-solved
# from T0 = 800 and V0 = 100/ul exactly as W03 back-solved them
# (NUMBERS.md 2a), because that is the only way the pretherapy set point
# stays at 10**5 -- the valley floor moves by 0.9% and its location by
# 0.004 in D. If they die at delta = 0.7/day the whole infection goes
# extinct, which excludes that reading: W03's panels contain a persistent
# infection. SO THIS FIGURE DOES NOT INHERIT THE DEFECT THAT KILLED THE
# TIME COURSES, and the check is recorded because the brief asked for it
# to be demonstrated, not assumed.
#
# WHAT IS OURS AND WHAT IS THEIRS. The curve, the oscillation band, the
# minimum and the R_0^T = 1 end are ALL MODELLED BY US from equations
# [1]-[6]; the figure's title says so and the legend separates them from
# the three amber diamonds, which are W03's own panel digitized.
#
# THE CONTRACT THIS FIGURE USED TO BREAK IS MENDED. The coexistence solver
# for equations [1]-[6] lived here, because the library carried the ALGEBRA
# of the threshold (`therapeutic_R0`, `P_min`, `D_min`) and no such solver.
# It is now `posb.populations.coexistence`, imported at the top of this
# module as `_coexistence`, and PS9's autograder imports the same function.
# Its defaults are this module's own pinned Table 1 set -- lam 31.0, k
# 1.875e-4, n 200.0, c 30.0, d 0.02, delta 0.7 -- so the two-argument calls
# below mean exactly what they meant when the solver was local. Verified
# against the values this figure prints, unchanged.
#
# AND ONE CLAIM WENT WITH IT THAT WAS FALSE. The local docstring said V*
# "depends on P and D ONLY through the product A", which is wrong, and the
# library's note now records the correction: `_v_of` is a function of A
# alone, but T is not, because the residual carries I_T = (c/(kn) - T)/D
# and D therefore enters separately. Measured at a fixed A = 270: P = 20
# gives 3.35e4/ml, P = 30 gives 659/ml, P = 100 gives 407/ml -- a factor of
# 82 across one product (NUMBERS.md 20.6, locked by
# tests/test_populations.py). The THRESHOLD depends only on P^2*D, which is
# about whether the vector persists at all; the SET POINT it persists at
# does not. Nothing drawn or printed on this figure ever rested on the
# false form -- the only P^2*D claims it makes are point 2 of
# `fig_setpoint_valley`'s docstring and the "$R_0^T$ = 1 here" tag, both
# about the threshold and both correct.
# =====================================================================

P_SWEEP = 30.0          # MODELLED, Fig. 2a's fixed P (NUMBERS.md 9)

# W03 Fig. 2a LEFT panel (HIV-1), the three traces that have REACHED a set
# point inside the panel's own 360-day window -- (D, virions/ml, day read).
# DIGITIZED BY US. Method: the panel at its published raster resolution,
# dig4's calibration (x: col 135.5 = day 0, col 590.0 = day 360 against the
# 7 printed ticks; y: row 558.5 = 1.0E+02, row 125.0 = 1.0E+05, and the four
# printed y ticks are evenly spaced at rows 125.0 / 268.5 / 415.0 / 558.5),
# color-masked per trace and averaged over the last 8 visible days.
#
# TWO OF THEIR FIVE ARE NOT ON THIS LIST AND MUST NOT BE PUT ON IT.
#   D = 0.2  (grey)  is still OSCILLATING at day 360 -- the last-8-day read
#            is 2913/ml, which is wherever the swing happens to be, against
#            a set point of 776/ml. Not a level, a phase.
#   D = 0.01 (green) is still FALLING -- flat at the pretherapy 9.99e4/ml
#            across the whole window, against a set point of 1.34e4/ml,
#            which it reaches only after about 1500 days. Day 360 is deep
#            inside the transient, and the transient is the half of this
#            model we cannot reproduce.
# Their day-360 readings for those two are 3.75x and 7.43x our set point.
# That is not a disagreement about levels; it is the panel being read for a
# quantity it does not contain at those two D. The legend says "day 360"
# and the title says "3 of their 5" so the figure claims only what holds.
#
# The D = 0.6 trace is read at day 337.8, not 360: the panel's own legend
# box is opaque and occludes it past that column. Our integration moves
# 4% between day 338 and its set point, so it is settled at the read.
W03_FIG2A_SETTLED = [(0.4, 782.3, 357.6),
                     (0.6, 1.909e4, 337.8),
                     (0.8, 5.966e4, 357.6)]

# The oscillation band is integrated, and these are the only two knobs in
# it. 20,000 days is 135 to 230 cycles, and the last 1,600 days is 11 to 18
# of them; against a 30,000-day reference the envelope is within 0.08%.
_CYC_T, _CYC_TAIL = 20000.0, 1600.0


def _leading_eig(P, D, st):
    """Largest real part of the 6x6 Jacobian's spectrum at `st`.

    This is what decides whether a point on the solved curve is a SET POINT
    or only an unstable equilibrium the system orbits, and it is computed
    rather than taken from W03's prose (which puts the oscillatory region at
    "P > 10 and D ~ 0.1") or from NUMBERS.md 19's digitization of their
    Fig. 3a floor (P > 11, D = 0.05-0.13, median 0.094). Both of those are
    independent of this calculation and both agree with it, which is the
    strongest check this figure has: at P = 30 the eigenvalue crosses zero
    at D = 0.0122 and again at D = 0.1152.
    """
    dp = D * DELTA
    T, V, it, vt = st["T"], st["V"], st["IT"], st["VT"]
    J = np.array([
        [-DUNINF - KINF * V - KINF * vt, 0.0, -KINF * T, 0.0, 0.0, -KINF * T],
        [KINF * V, -DELTA, KINF * T, 0.0, 0.0, 0.0],
        [0.0, NBURST * DELTA, -CLEAR, 0.0, D * NBURST * dp, 0.0],
        [KINF * vt, 0.0, -KINF * it, -DUNINF - KINF * V, 0.0, KINF * T],
        [0.0, 0.0, KINF * it, KINF * V, -dp, 0.0],
        [0.0, 0.0, 0.0, 0.0, P * P * D * NBURST * dp, -CLEAR]])
    return float(np.linalg.eigvals(J).real.max())


def _cycle_envelope(P, D):
    """(min, max) of V on the attractor, in virions/ml, where there is no
    set point. Integrated, because a limit cycle is not a root."""
    from scipy.integrate import solve_ivp
    t_pre = CLEAR / (KINF * NBURST)
    v_pre = (KINF * LAM * NBURST - CLEAR * DUNINF) / (CLEAR * KINF)
    y0 = [t_pre, CLEAR * v_pre / (NBURST * DELTA), v_pre, 0.0, 0.0, 100.0]

    def rhs(_t, y):
        T, I, V, it, id_, vt = np.maximum(y, 0.0)
        dp = D * DELTA
        return [LAM - DUNINF * T - KINF * V * T - KINF * vt * T,
                KINF * V * T - DELTA * I,
                NBURST * DELTA * I - CLEAR * V + D * NBURST * dp * id_,
                KINF * vt * T - DUNINF * it - KINF * V * it,
                KINF * V * it - dp * id_,
                P * P * D * NBURST * dp * id_ - CLEAR * vt]

    s = solve_ivp(rhs, [0.0, _CYC_T], y0, method="LSODA", rtol=1e-9,
                  atol=1e-13, dense_output=True)
    ts = np.linspace(_CYC_T - _CYC_TAIL, _CYC_T, 6001)
    v = np.array([s.sol(t)[2] for t in ts]) * 1000.0
    return float(v.min()), float(v.max())


def _densify(p, step=1.0):
    """One sample per pixel along a rendered polyline.

    THE VERSION OF `_setpoint_seams` THAT SHIPPED FIRST DID NOT DO THIS AND
    WAS WRONG BY 1082 PIXELS. It sampled `get_xydata()`, and the pretherapy
    reference line is TWO vertices spanning the whole axes -- so a legend box
    sitting squarely on it registered zero hits and this guard printed
    nothing, while `tools/figure_fit.py` reported the same legend on 1082 px
    of that line and on 52 px of the curve. That is deck-bar D5d item 4 and
    D5e (vertex distance is not ink distance) committed INSIDE a guard
    written to catch them: a guard that samples vertices can only find a
    collision where a vertex happens to be. Kept as a comment because the
    next guard anyone adds here will be tempted the same way.
    """
    if len(p) < 2:
        return p
    out = [p[:1]]
    for a, b in zip(p[:-1], p[1:]):
        n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) / step) + 1
        out.append(a + (b - a) * np.linspace(0.0, 1.0, n + 1)[1:, None])
    return np.vstack(out)


def _setpoint_seams(fig, ax, name):
    """The two things no gate here looks at, on a one-panel figure.

    `figure_fit` never enters a LEGEND as a collision box and treats the
    axes title as frame (deck-bar D5a, D5d item 2, D5g), and this figure's
    legend sits INSIDE the data area. Sampling is on the rendered path and
    on the fill, because `ax.collections` is where the oscillation band
    lives and deck-bar D5d item 4 is that the gate used to miss exactly
    that. Measured to the STROKE, not to the vertices (D5e).
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    lg = ax.get_legend()
    boxes = [("legend", lg.get_window_extent(r))] if lg is not None else []
    boxes += [(t.get_text()[:28], t.get_window_extent(r))
              for t in ax.texts if t.get_text().strip()]
    for label, bb in boxes:
        for ln in ax.lines:
            if not len(ln.get_xydata()):
                continue
            pad = ln.get_linewidth() * fig.dpi / 72.0 / 2.0
            if ln.get_marker() not in (None, "None", "", " "):
                pad += ln.get_markersize()
            p = _densify(ax.transData.transform(ln.get_xydata()))
            hit = int(((p[:, 0] >= bb.x0 - pad) & (p[:, 0] <= bb.x1 + pad) &
                       (p[:, 1] >= bb.y0 - pad) & (p[:, 1] <= bb.y1 + pad)).sum())
            if hit:
                print(f"  !! {name}: {label!r} is within the drawn stroke of "
                      f"{hit} plotted points. `figure_fit` cannot see this.")
        for col in ax.collections:
            for path in col.get_paths():
                p = ax.transData.transform(path.vertices)
                hit = int(((p[:, 0] >= bb.x0) & (p[:, 0] <= bb.x1) &
                           (p[:, 1] >= bb.y0) & (p[:, 1] <= bb.y1)).sum())
                if hit:
                    print(f"  !! {name}: {label!r} covers {hit} vertices of a "
                          f"filled region -- the band IS data (deck-bar D5b).")
    # THE FRAME AGAINST THE FRAME, which is the hole this figure fell into.
    # `figure_fit` compares text with text INSIDE an axes and never enters a
    # legend as a box at all, so a legend placed OUTSIDE the axes -- the
    # standard remedy for a legend that was colliding with data -- lands in
    # the one place no gate looks, exactly deck-bar D5g's shape one level
    # down. The first version offset at -0.16 printed "pretherapy 10^5/ml"
    # straight through "is no inhibition" and ran its left edge into the y
    # label, `figure_fit` returned zero problems, and it was found by reading
    # the PNG at page size (deck-gauntlet 5.8). These four gaps are measured
    # here so the next change to the offset cannot repeat it.
    frame = [("title", ax.title), ("x label", ax.xaxis.label),
             ("y label", ax.yaxis.label)]
    # TICK LABELS ARE FRAME AND NOBODY CHECKS THEM. deck-bar D5d item 1: the
    # gate looks at ax.texts, the axis labels and the title, never at ticks --
    # and this figure's title is wider than its axes, so it reaches out over
    # the y tick column on the left. Found by cropping the corner at 3x after
    # the gate returned zero.
    ticks = ([("a y tick", t) for t in ax.get_yticklabels() if t.get_visible()]
             + [("an x tick", t) for t in ax.get_xticklabels() if t.get_visible()])
    pairs = [(a, b) for i, a in enumerate(frame) for b in frame[i + 1:]]
    if lg is not None:
        pairs += [(("legend", lg), f) for f in frame]
    pairs += [(a, t) for a in frame for t in ticks]
    for (na, aa), (nb, ab) in pairs:
        ba, bb = aa.get_window_extent(r), ab.get_window_extent(r)
        dx = max(ba.x0, bb.x0) - min(ba.x1, bb.x1)
        dy = max(ba.y0, bb.y0) - min(ba.y1, bb.y1)
        if dx < 0 and dy < 0:
            print(f"  !! {name}: {na} OVERLAPS {nb} by "
                  f"{-dx / fig.dpi:.3f} x {-dy / fig.dpi:.3f} in. No gate on "
                  f"this repo compares two pieces of frame.")
        elif max(dx, dy) / fig.dpi < 0.05:
            print(f"  !! {name}: {na} clears {nb} by only "
                  f"{max(dx, dy) / fig.dpi:.3f} in.")


def fig_setpoint_valley(name="s25_setpoint_valley"):
    """The HIV-1 set point against D at P = 30, and both ends are pretherapy.

    MODELLED BY US from equations [1]-[6]. What a student concludes, in the
    order the picture gives it:

    1. There is a VALLEY in D, not a slope -- the thing NUMBERS.md 9 says
       Fig. 2a exists to show. Minimum at D = 0.3067, set point 658
       virions/ml, 152x below the pretherapy 10**5.
    2. BOTH ENDS SIT ON THE PRETHERAPY LINE, FOR OPPOSITE REASONS, and that
       is the paradox with nothing left to explain. At D = 1 there is no
       inhibition and nothing has been done to the virus. At D = 0.0023 the
       inhibition is so complete that R_0^T = P^2*D*(1 - 1/R_0) falls to 1
       and the vector cannot persist at all -- segment 3's threshold,
       arriving as the left wall of segment 4's valley. "Shooting itself in
       the molecular foot" (W03's own phrase, NUMBERS.md 5c) is the left
       half of this curve.
    3. Between D = 0.0122 and D = 0.1152 there is NO SET POINT. The
       equilibrium is still there -- the dotted line inside the band -- but
       its leading eigenvalue is positive and the system orbits it instead,
       between the band's edges. That is W03's Hopf region, and our
       eigenvalue puts it where their text ("P > 10 and D ~ 0.1") and
       NUMBERS.md 19's digitization of their Fig. 3a floor (P > 11,
       D = 0.05-0.13) independently put it.

    WHERE OUR SET POINT MINIMUM FALLS SETTLES A MISMATCH INSIDE THE PAPER.
    NUMBERS.md 5c records two numbers W03 gives for the best D and says a
    slide must pick one: the text (p.6) says "~0.2" and the Fig. 3b caption
    says "~0.4". Our minimum is D = 0.31, between them, and the curve is
    flat enough across 0.2 to 0.4 -- 776, 658, 777 virions/ml -- that both
    of their numbers are within 18% of the floor. The mismatch is real and
    it does not matter, which is a better answer than choosing.

    WHAT IS THEIRS: three amber diamonds, W03's own Fig. 2a left panel
    digitized by us at day 360 -- the three of their five traces that have
    reached a set point by then. See W03_FIG2A_SETTLED for the calibration,
    and for why D = 0.2 and D = 0.01 are NOT on this figure.

    NO LEADERS ANYWHERE IN THIS FIGURE, so deck-bar D5f cannot bite: every
    label is placed against the thing it names and nothing points. MUTED is
    a data color here (the pretherapy line) and is used for no annotation,
    which is the grep D5f asks for.
    """
    d_end = float(D_min(P_SWEEP, R0))        # R_0^T = 1; 0.0022963, NUMBERS 18.5
    grid = np.logspace(np.log10(d_end * (1 + 2e-4)), 0.0, 460)
    sol = [_coexistence(P_SWEEP, d) for d in grid]
    assert all(s is not None for s in sol), "coexistence lost above R_0^T = 1"
    V = np.array([s["V"] * 1000.0 for s in sol])
    eig = np.array([_leading_eig(P_SWEEP, d, s) for d, s in zip(grid, sol)])
    stable = eig < 0.0

    from scipy.optimize import brentq, minimize_scalar
    def _eig_of(d):
        return _leading_eig(P_SWEEP, d, _coexistence(P_SWEEP, d))
    edges = [brentq(_eig_of, grid[j], grid[j + 1], xtol=1e-12)
             for j in np.nonzero(np.diff(stable.astype(int)))[0]]
    assert len(edges) == 2, f"expected one oscillatory window, got {edges}"
    d_lo, d_hi = edges
    best = minimize_scalar(lambda d: _coexistence(P_SWEEP, d)["V"] * 1000.0,
                           bracket=(0.25, 0.30, 0.36), method="brent",
                           options=dict(xtol=1e-9))
    d_best, v_best = float(best.x), float(best.fun)
    v_pre = 1.0e5                              # NUMBERS.md 18.1, V* = 10**5/ml

    # 4.55 in authored, and WIDTH is what binds here, not height -- which is
    # the opposite of `fig_design_space` and worth writing down because the
    # arithmetic is easy to carry over wrongly. The deck's box fits the PNG
    # inside (10.2, band) preserving aspect, so the scale is
    # min(10.2, band * aspect) / w. Saved 9.79 x 4.15 in is aspect 2.36, and
    # 4.30 * 2.36 = 10.16 < 10.2, so the two terms are within half a per cent
    # of each other and the figure sits at the corner where the box's width
    # and its height bind together -- the most efficient shape for the band,
    # and the reason this one clears the floor at 1.04 while being nearly
    # 10 in wide. Authoring ANY taller crosses over to height-binding and the
    # scale starts falling as 4.30/h. The saved size is measured by `_save`
    # from the bytes savefig writes, never from `get_size_inches()`
    # (deck-bar D5a item 5).
    fig, ax = plt.subplots(figsize=(10.2, 4.55))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.0018, 1.15); ax.set_ylim(1.0e2, 1.0e6)
    ax.set_axisbelow(True)                    # or the grid stripes the band
    ax.grid(True, which="both", color=RULE, lw=0.5)
    ax.set_xticks([0.002, 0.01, 0.1, 1.0])
    ax.set_xticklabels(["0.002", "0.01", "0.1", "1"])
    ax.set_yticks([1e2, 1e3, 1e4, 1e5, 1e6])

    # THE OSCILLATION IS DRAWN AS WHAT IT IS: the swing of the attractor,
    # integrated at 16 D across the window. Opaque and not alpha -- a
    # translucent block lets the minor grid through and the band comes out
    # striped (the same call `fig_design_space` learned this on).
    # SAMPLED TOWARD THE TWO ENDS, NOT EVENLY. The cycle amplitude leaves
    # each Hopf point like sqrt(D - D_edge), so 16 evenly spaced points drew a
    # visible straight-line kink in the band's lower-left edge where the real
    # boundary is steepest -- seen at 3x, not by any gate. Cosine spacing puts
    # the samples where the curvature is, and the two end points are the
    # EQUILIBRIUM itself, because the amplitude is exactly zero at a Hopf
    # point and integrating there would report whatever the transient had
    # left.
    u = (1.0 - np.cos(np.linspace(0.0, np.pi, 22))) / 2.0
    dw = 10.0 ** (np.log10(d_lo) + u * (np.log10(d_hi) - np.log10(d_lo)))
    envelope = np.array(
        [(_coexistence(P_SWEEP, d)["V"] * 1000.0,) * 2 if j in (0, len(dw) - 1)
         else _cycle_envelope(P_SWEEP, d) for j, d in enumerate(dw)])
    ax.fill_between(dw, envelope[:, 0], envelope[:, 1], color="#B9C6C6",
                    lw=0, zorder=2)

    # The stable arms SOLID and the unstable middle DOTTED: one curve, so the
    # valley reads as a valley, with the middle marked as an equilibrium the
    # system does not sit at. A gap would have read as missing data.
    for seg in np.split(np.arange(len(grid)), np.nonzero(np.diff(stable))[0] + 1):
        if stable[seg[0]]:
            ax.plot(grid[seg], V[seg], color=TEAL, lw=3.4, zorder=5,
                    solid_capstyle="round")
    mid = ~stable
    ax.plot(grid[mid], V[mid], color=TEAL, lw=1.8, ls=":", zorder=6)
    # One proxy for the legend, so the two solid arms do not enter it twice.
    ax.plot([], [], color=TEAL, lw=3.4, label="ours: set point")
    # The pretherapy level, PLOTTED and not `axhline`, so `_setpoint_seams`
    # can sample it in data coordinates like every other line.
    # "/ml" CUT FROM THIS LABEL, and it is the whole fix for the one
    # collision the widened gate found on this figure. The legend sits
    # outside the axes under the x label, centred on the axes, and at
    # 1497.1 px it was WIDER THAN THE AXES (1285.4) -- so its left end
    # reached back under the rotated y label and the two boxes overlapped
    # by 2.2 px at the corner. Measured at `_settle`'s fixed point, which
    # is the only geometry that matches the file: one tight_layout pass
    # earlier the same overlap reads 9.4 px and the direction of the
    # shallower axis is different, so a number taken before the fixed
    # point sends you after the wrong edge (deck-bar D5a item 3).
    #
    # THE UNITS ARE NOT LOST, they are inherited: the y label is "HIV-1 set
    # point (virions/ml)" and the pretherapy line is a level ON THAT AXIS,
    # so "/ml" was saying the axis's own unit a second time. Cutting three
    # characters took 55.5 px off the legend and bought 27 px of daylight
    # against the y label -- gauntlet 5.2's point that text is the lever
    # that does not move when everything else does. No coordinate moved.
    ax.plot([0.0018, 1.15], [v_pre, v_pre], color=MUTED, lw=2.0, ls="--",
            zorder=3, label="pretherapy $10^5$")
    # MARKERS, NO CONNECTING LINE: three readings, not a curve.
    ax.plot([p[0] for p in W03_FIG2A_SETTLED],
            [p[1] for p in W03_FIG2A_SETTLED], "D", color=AMBER, ms=9,
            lw=0, zorder=8, label="theirs, day 360")
    ax.plot([d_best], [v_best], "o", color=RED, ms=11, zorder=9)

    ax.set_xlabel("antiviral effect  $D$   ($D$ = 1 is no inhibition)",
                  fontsize=LBL)
    ax.set_ylabel("HIV-1 set point (virions/ml)", fontsize=LBL)
    ax.set_title(f"ours, MODELLED from equations [1]–[6] at $P$ = {P_SWEEP:.0f}"
                 f"\nminimum at $D$ = {d_best:.2f}: {v_best:.0f}/ml, "
                 f"{v_pre / v_best:.0f}× below pretherapy",
                 fontsize=LBL, color=MUTED)
    # THE LEGEND IS OUT OF THE AXES, UNDER THE x LABEL, and it got there by
    # deck-gauntlet 5.2 rather than by taste. Inside the axes it cost three
    # rounds: four entries in two rows in the top decade gave `figure_fit`
    # four collisions (the box reached left into the R_0^T tag, that tag
    # reached up into the title, and the box sat on 1082 px of the pretherapy
    # line and 52 px of the curve); cutting it to two entries in one row and
    # direct-labelling the pretherapy level moved the collision onto the
    # LABEL, 4.6 px above the line it names; and every remaining slot inside
    # the axes was measured and found too short, because the right arm climbs
    # through the only wide one. Three fixes each creating the next is 5.2
    # exactly, and 5.2's own remedy is to stop nudging and move the block into
    # FRAME. Outside the axes it cannot touch data at any y limit, which is
    # worth the 0.40 in of height it costs.
    #
    # THE LEFT END IS NAMED, THE RIGHT END IS NOT, and that is deliberate.
    # "D = 1 is no inhibition" is already in the x label, so the right arm
    # meeting the pretherapy line needs no second caption; the left arm does,
    # because nothing else on the figure says why a curve would come back UP
    # as the drug gets better.
    #
    # EVERY TAG SITS IN A MEASURED GAP, not in a nudged one. In axes
    # fractions, y log over 1e2 to 1e6 (an even 4 decades): the pretherapy
    # line is at y 0.75 and the curve TOUCHES it only at its two ends -- x
    # 0.038 on the left and x 0.979 on the right -- so the whole strip above
    # 0.75 between them is clear and the R_0^T tag has it to itself; the
    # oscillation band spans x 0.291 to 0.644 with its floor at y 0.175, and
    # the curve's own minimum is at y 0.204, so the strip below 0.175 runs
    # clear under both and holds "no set point".
    _tag(ax, 0.015, 0.95, "$R_0^T$ = 1 here", TEAL, va="top", plate=False)
    _tag(ax, 0.34, 0.02, "no set point", INK, plate=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=3,
              frameon=False, fontsize=LBL, handlelength=1.6,
              columnspacing=1.6, borderpad=0.1, handletextpad=0.5)
    _setpoint_seams(fig, ax, name)
    print(f"  .. {name}: minimum D = {d_best:.6f}, V* = {v_best:.3f}/ml; "
          f"oscillatory window D = {d_lo:.6f} to {d_hi:.6f}; "
          f"R_0^T = 1 at D = {d_end:.7f}")
    for d_i, v_i, t_i in W03_FIG2A_SETTLED:
        ours = _coexistence(P_SWEEP, d_i)["V"] * 1000.0
        ratio = ours / v_i
        flag = "" if 0.90 <= ratio <= 1.05 else "   !! OUTSIDE 0.90-1.05"
        print(f"     D = {d_i}: ours {ours:9.4g} /ml vs theirs {v_i:9.4g} /ml "
              f"at day {t_i:.1f}  ->  {ratio:.3f}x{flag}")
    _save(fig, name)


FIGURES = [fig_objects, fig_cistrans_series,
           fig_urn_series, fig_chain_series, fig_rtchain_series, fig_genotypes,
           fig_burst_ledger, fig_burst_capped, fig_design_space,
           fig_homing, fig_locus_series,
           fig_recall_chemostat, fig_recall_qssa,
           fig_setpoint_valley]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
