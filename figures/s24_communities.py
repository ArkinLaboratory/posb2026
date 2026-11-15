"""Session 24 figures -- the wire is now outside the cell.

ONE MODEL PER FIGURE, AND THE MODEL IS NAMED ON THE FIGURE. This session
carries four models with four different provenances and they must never be
read as one:

  * `t = L^2/2D_A` -- session 2's convention, with Karig's ESTIMATED
    cell-to-cell coefficients (NUMBERS.md sec 19.1).
  * `ell_A = sqrt(D_A/gamma_A)` -- taught as a formula. THERE IS NO NUMBER
    IN THIS FOLDER and that is the lesson (sec 19.4). Nothing here prints
    0.32 mm or 0.71 mm: the first is computed from Basu's xi and inherits
    xi's defect, the second combines Karig's 3OC12HSL with Basu's gamma_A,
    which is a different signal in a different lawn.
  * Basu's equations (1)-(4) in the liquid-phase limit, with their printed
    BD2 set -- `band_detect_response`, `band_peak`, `band_edges`.
  * THE BIOMODELS DEPOSIT BIOMD0000000296, not Balagadde's text, which prints
    no equations at all. Every predator-prey figure says "deposited model".

Every curve comes out of `posb.communities`, the same functions PS9 imports.
Nothing here re-derives any of that mathematics.

NO PUBLISHED PANEL IS REDRAWN. We hold Basu's and Balagadde's reported
numbers, not the points behind their panels, so Basu Figs. 1a, 2b, 2d, 3, 4,
5 and Balagadde Box 1A/1B, Figs. 2A, 2B, 2C, 3C go on slides as PAPER FIGURES
with their own attribution. `fig_model_vs_experiment` plots the model against
the regime the authors state IN THEIR OWN TEXT at each dilution rate
(NUMBERS.md sec 2.4, 3.4, 20.5) -- not a coordinate read off a panel -- and
says so on the figure.

TWO SHAPES OF FIGURE HERE.
  * The wide ones are placed by `theme.image_centered` in a 4.60 in band, so
    their SAVED TIGHT BBOX stays under 4.60 in tall and 10.2 in wide. Past
    either, the deck scales the whole picture down and 20 pt authored lands
    under the content floor.
  * The `*_step_*` ones are for `Deck.derivation_fig`, whose figure column is
    5.4 x 4.95 in: the picture advances as the algebra does, so each is one
    stage of a derivation and none carries a caption, because derivation_fig
    already prints the step label above the equation.

TEXT WIDTH IS THE BINDING CONSTRAINT AND IT IS WORTH WRITING DOWN. At the
20 pt content floor and savefig.dpi = 160, a character is about 22 px, so a
10 in figure holds about 60 characters of title and a half-panel about 28. The
first cut of this module was written against a guess of half that and every
wide figure overflowed its own placement band -- which is not a cosmetic
defect: it scaled 20 pt down to 14.2 pt on the wall.

Numbers on these figures are in sessions/s24-communities/NUMBERS.md with their
kind, and the constant block below names the section for each one.

Run:  python tools/build_figures.py s24
"""
import functools

import matplotlib.ticker as mpl_ticker
import numpy as np

from figures.style import (use, TEAL, CYAN, AMBER, GREEN, MUTED, INK, RED,
                           RULE, TYPE)
from posb.communities import (BASU_XI, KARIG_D_3OC12HSL, KARIG_D_C4HSL,
                              PP_IPTG,
                              band_detect_response, band_edges, band_peak,
                              basu_params, diffusion_time, dol_criterion,
                              penetration_depth, pp_hopf_D, pp_jacobian,
                              sender_receiver,
                              pp_leading_real_part, pp_params, pp_qss_model,
                              pp_steady_states)

plt = use()
OUT = "figures/build"

# --- every number printed on a figure in this module, with its section ------
# sec 19.1   KARIG_D_3OC12HSL = 83 um^2/s, KARIG_D_C4HSL = 1810 um^2/s.
#            MODELLED from MEASURED -- their word is "estimated", obtained by
#            fitting a fluorescence wave profile. Both are EFFECTIVE
#            CELL-TO-CELL coefficients through a bacterial lawn, and neither
#            molecule is Basu's 3OC6HSL.
# sec 19.1   the measured ratio of the two, 21.6 +/- 10, MEASURED (their word).
# sec 13.1   BASU_XI = 0.001 mm^2/min, PRINTED by Basu p.1134, and NOT a
#            diffusion coefficient.
# sec 13.3   the ring lengths it is checked against -- 6 mm (Fig. 4b,
#            simulated), 7 mm (Methods, tuned), 10 mm (Fig. 4a, measured) --
#            the 36 h the experiment ran, and the conclusion that xi is one to
#            two orders of magnitude too small for the figures it generated.
# sec 7.2    Basu's printed BD2 set, MODELLED, reached through `basu_params`.
#            beta_L = 0.8 uM and beta_C = 0.008 uM are printed there; the peak
#            and the two edges are COMPUTED from that set by this module.
# sec 20.1   the deposited parameter set, QUOTED from BIOMD0000000296.
# sec 20.4   the two Hopf crossings and the 73.6 h period, COMPUTED -- and
#            recomputed here by `pp_hopf_D` rather than quoted.
# sec 20.5   the five dilution rates the authors ran, and the regime they
#            state at each. MEASURED.
# Only the 10 mm row is an experiment. 6 mm is the ring in the SIMULATED
# Fig. 4b and 7 mm is the position the Methods tuned the senders to, so a
# "36 h experiment" rule applies to one of these three rows (sec 13.3).
BASU_RINGS = ((6.0, "simulated"), (7.0, "tuned"), (10.0, "measured"))
BASU_RUN_H = 36.0                       # h, sec 13.3
# The oscillatory window, COMPUTED from the deposit and pinned by
# tests/test_communities.py to one part in 1e5 (DESIGN sec 7.2). It is
# RECOMPUTED by `pp_hopf_D` on every build and checked against these, so the
# figure cannot drift away from the number the tests hold. The digitization
# of the paper's Fig. 3C is what these are checked AGAINST, not their source.
PINNED_HOPF = (0.0367268, 0.1674282)
DEPOSIT = "the deposited model, BIOMD0000000296, not the paper's text"
# The same provenance, short enough for a two-panel figure's suptitle. At
# 20 pt a suptitle is the widest artist on the figure and it is what sets the
# tight bbox, so DEPOSIT itself overflows a 9.6 in two-panel placement band.
DEPOSIT_2P = "the deposited model BIOMD0000000296, not the paper's"

# EVERY piece of text inside a figure is content the room has to read, so it
# sits at the body floor. TYPE["caption"] inside a figure is for a literature
# citation and nothing else.
LBL = TYPE["body"]
PAGE = "#F8FAF9"          # style.py's savefig.facecolor


def _plate(pad=0.3):
    """Page-colored backing for a label, TRANSLUCENT on purpose.

    An opaque plate turns a legibility defect into an occlusion defect, and
    the occlusion is worse because it is silent: the figure looks clean and
    the curve is simply gone. At alpha 0.75 a struck curve is still visibly
    struck, so the defect announces itself in the render instead of hiding
    there. It is not a licence to put labels on data -- it is what makes the
    mistake findable by eye when one gets through.
    """
    return dict(facecolor=PAGE, edgecolor="none", pad=pad, alpha=0.75)


def _tag(ax, x, y, s, color, ha="left", va="bottom"):
    """A short label beside the curve it names, in axes fractions."""
    ax.text(x, y, s, transform=ax.transAxes, color=color, fontsize=LBL,
            ha=ha, va=va, bbox=_plate(), zorder=7, linespacing=1.3)


def _point(ax, xy, text, color, xytext, ha="left", va="center"):
    """A label in empty space with a leader to the thing it names.

    The point is the EMPTY SPACE: the label goes where there is room and the
    leader does the pointing, so nothing is printed over a curve. An earlier
    version of this docstring justified the leader by what figure_fit would
    score it -- which is designing to the metric, and it produced three
    occlusions the gate could not see. Place by the pixels; the gate is a
    floor, not a target.

    THE LEADER IS MUTED, THE LABEL KEEPS ITS COLOUR, AND THAT IS A MODULE-WIDE
    CONVENTION RATHER THAN A STYLE CHOICE. A leader that inherits its label's
    color can be read as the curve it points at: on this module's phase
    plane a leader at lw 1.6 met a nullcline at lw 3.2 in the same cyan, and
    at the rendered page's own size the stroke-weight difference that
    separates them disappears and the two read as ONE path that bottomed out
    and rose again -- a shape the data does not have (bar sec D5f, gauntlet
    sec 5.8). Re-aiming the leader fixes one instance; grey fixes the class,
    because grey is not a data color anywhere in this module and so cannot
    be mistaken for one. The tie between label and curve survives in the
    LABEL's color, which is where it was always carried.

    And the defect is invisible under magnification: at 330 dpi the 2x
    stroke-weight difference is obvious and the join looks correct. Verify
    this at page size.
    """
    return ax.annotate(text, xy=xy, xycoords="data", xytext=xytext,
                textcoords="axes fraction", color=color, fontsize=LBL,
                ha=ha, va=va, bbox=_plate(), zorder=7, linespacing=1.3,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.6))


def _settle(fig, ax, passes=8):
    """Run `tight_layout` to its FIXED POINT and return the settled axes box.

    bar sec D5a item 3: `tight_layout` is not idempotent here. On this
    module's two-panel phase plane the left axes walked 653.1 -> 636.2 px
    wide between the first pass and the second before holding. Both
    `figure_fit.audit` and `_save` run one more pass of their own, so a
    measurement taken after a single call describes a geometry that is never
    written to disk -- which is the same class of error as measuring before
    `tight_layout` at all (sec D5b). Settle first, measure second.
    """
    last = None
    for _ in range(passes):
        fig.tight_layout()
        fig.canvas.draw()
        box = ax.get_window_extent(fig.canvas.get_renderer())
        now = (box.x0, box.y0, box.width, box.height)
        if last is not None and max(abs(a - b) for a, b in zip(now, last)) < 0.05:
            return box
        last = now
    raise AssertionError(
        "_settle: tight_layout did not reach a fixed point in "
        f"{passes} passes -- the geometry measured is not the geometry "
        f"saved, so nothing below this line can be trusted.")


def _title_ceiling(ax, box, rend, want=14.0):
    """How high a label's TOP may reach, in axes fractions, and still clear
    the AXES TITLE by `want` px.

    MEASURED FROM THE TITLE, not from the axes top. A label is free to end
    above the axes -- what it must not do is arrive at the title, and the
    daylight between the two is a property of the title's own box, which
    moves with its line count and its font metrics.

    `want` is `figure_fit`'s 10 px GAP plus 4. The margin is not decoration:
    gauntlet sec 5.1 records three label pairs that measured clean in the
    cloud container and collided by 5-9 px on the machine the deck is built
    on. Sizing to exactly 10 px is sizing to one renderer.
    """
    t = ax.title
    lid = t.get_window_extent(rend).y0 if t.get_text().strip() else box.y1
    return (lid - want - box.y0) / box.height


def _data_top_below(ax, box, x0, x1, limit):
    """Highest DRAWN data point under an x span, below `limit`, in fractions.

    Both artist families, because only one of them was sampled once and bar
    sec D5d item 4 is the record of it: a contour is a LineCollection and a
    scatter is a PathCollection, neither of which is in `ax.lines`, and a
    plate erased about 50 px of a nullcline with the gate calling it clean.
    Returns -inf when the span is empty, so a caller's clearance is large
    rather than undefined.

    THE TOP OF THE PAINTED INK, NOT OF THE VERTICES. A nullcline here is
    drawn at lw 3.2, which is 4.4 px wide, so a plate sitting 1.2 px above
    the center LINE is sitting about 1 px ON the curve. That is not a
    hypothetical rounding argument: the Cdot_2 = 0 plate on this module's
    phase plane measures 1.2 px of vertex clearance and a 330 dpi crop of
    the rendered page shows it lightening the lower edge of the branch
    above it. Half the stroke is added back here so that a caller's
    threshold is a count of VISIBLE daylight.
    """
    best = -np.inf
    for fx, fy, half in _painted(ax, box):
        sel = (fx > x0) & (fx < x1) & (fy + half < limit)
        if sel.any():
            best = max(best, float((fy + half)[sel].max()))
    return best


def _data_bottom_above(ax, box, x0, x1, limit):
    """Mirror of `_data_top_below`: lowest painted ink above `limit`."""
    best = np.inf
    for fx, fy, half in _painted(ax, box):
        sel = (fx > x0) & (fx < x1) & (fy - half > limit)
        if sel.any():
            best = min(best, float((fy - half)[sel].min()))
    return best


def _data_blocking_x(ax, box, bot, top, margin):
    """Rightmost x a plate spanning `bot`..`top` would still land on.

    A plate is clean over a span when no painted ink enters the band
    [bot - margin, top + margin] inside it. Every artist is tested, so the
    answer accounts for the other nullcline and the fixed-point markers as
    well as the branch directly above -- all three were in the way of the
    Cdot_2 = 0 label at one x or another. Everything to the RIGHT of what
    this returns is free, which makes the placement a solve rather than a
    scan: there is no x to search for, only a boundary to step past.
    """
    best = -np.inf
    for fx, fy, half in _painted(ax, box):
        sel = (fy + half > bot - margin) & (fy - half < top + margin)
        if sel.any():
            best = max(best, float(fx[sel].max()))
    return best


def _curve_side_point(ax, coll, anchor_px, end_px=34.0):
    """The point on a curve nearest `anchor_px`, excluding its ENDS.

    A LEADER THAT LANDS ON A CURVE'S CUT END READS AS THE CURVE CARRYING ON.
    Found by eye on 8 November, on this module's phase plane, as the defect
    created by the fix directly above it: moving the Cdot_2 = 0 label right
    to stop it bleaching the branch above lengthened its leader, and because
    the leader is the label's own color and met the nullcline end-on, the
    curve and the leader read as ONE cyan path that bottomed out and rose
    again to the right. The nullcline does no such thing -- it is cut where
    the sampling grid stops, which this figure's suptitle says out loud.
    Distance checks are blind to it: the leader was 8.2 px clear of
    everything it passed and still said something false.

    Landing on the SIDE of the curve makes the same leader read as pointing,
    which is why the Cdot_1 leader was never ambiguous. Ends are taken per
    path, so a contour returned in several pieces is handled.
    """
    ends, verts = [], []
    for pth in coll.get_paths():
        v = pth.vertices
        if len(v):
            verts.append(v)
            ends += [v[0], v[-1]]
    if not verts:
        raise AssertionError("_curve_side_point: nothing drawn to point at.")
    v = np.vstack(verts)
    d = ax.transData.transform(v)
    e = ax.transData.transform(np.vstack(ends))
    far = np.min(np.hypot(d[:, None, 0] - e[None, :, 0],
                          d[:, None, 1] - e[None, :, 1]), axis=1) > end_px
    if not far.any():
        raise AssertionError(
            "_curve_side_point: every point on this curve is within "
            f"{end_px} px of an end -- it is too short to be pointed at "
            "without reading as continued.")
    dist = np.hypot(d[far, 0] - anchor_px[0], d[far, 1] - anchor_px[1])
    return tuple(v[far][int(np.argmin(dist))])


def _leader_min_gap(ax, box, p0, p1, ignore_px=30.0):
    """Smallest gap, in px, between a leader and any painted data it passes.

    THE WHOLE PATH, NOT THE ENDPOINT. D5d item 3 is a leader crossing the
    object it points past, and slide 20 earlier today was the sharper
    version: a leader that merely ENDED 0.13 units short of a receiver rim
    read as pointing at the rim. A leader is supposed to arrive at the curve
    it names, so a radius around its target is ignored and everything else
    on the way is measured. `p0`, `p1` are in display px.
    """
    t = np.linspace(0.0, 1.0, 240)
    sx = p0[0] + t * (p1[0] - p0[0])
    sy = p0[1] + t * (p1[1] - p0[1])
    keep = np.hypot(sx - p1[0], sy - p1[1]) > ignore_px
    sx, sy = sx[keep], sy[keep]
    if not len(sx):
        return np.inf
    px_per_pt = ax.figure.dpi / 72.0
    best = np.inf
    for fx, fy, half in _painted(ax, box):
        dx = fx * box.width + box.x0
        dy = fy * box.height + box.y0
        for i in range(len(sx)):
            d = np.hypot(dx - sx[i], dy - sy[i]).min() - half * box.height
            best = min(best, float(d))
    return best


def _painted(ax, box):
    """Every drawn data artist as (x_frac, y_frac, half stroke in fractions).

    Both artist families, every time: a contour is a LineCollection and a
    scatter is a PathCollection, neither of which is in `ax.lines` (bar sec
    D5d item 4). The half stroke is returned with them because VERTEX
    DISTANCE IS NOT INK DISTANCE -- a nullcline here is drawn at lw 3.2,
    which is 4.4 px wide, so a plate 1.2 px above the center line is about
    1 px ON the curve. That is how the Cdot_2 = 0 plate came to bleach the
    branch above it while measuring "clear".
    """
    px_per_pt = ax.figure.dpi / 72.0
    out = []
    for c in ax.collections:
        verts = [pth.vertices for pth in c.get_paths()]
        if verts:
            half = float(np.max(np.atleast_1d(c.get_linewidth()))) / 2.0
            out.append((np.vstack(verts), half))
    for ln in ax.lines:
        xd, yd = ln.get_data()
        if len(xd):
            half = max(float(ln.get_linewidth()),
                       float(ln.get_markersize())) / 2.0
            out.append((np.column_stack([np.asarray(xd), np.asarray(yd)]),
                        half))
    done = []
    for arr, half_pt in out:
        d = ax.transData.transform(arr)
        done.append(((d[:, 0] - box.x0) / box.width,
                     (d[:, 1] - box.y0) / box.height,
                     half_pt * px_per_pt / box.height))
    return done


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _save_column(fig, name):
    """Save a derivation_fig column figure at its exact authored size.

    The tight bbox would crop each stage to its own ink, so the deck would
    place a differently shaped picture on every slide of a run and the drawing
    would jump as the algebra advanced. These are padded by hand instead.
    """
    with plt.rc_context({"savefig.bbox": None}):
        fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _col(figsize=(5.3, 4.5)):
    return plt.subplots(figsize=figsize)


# ===========================================================================
# MOVE 1 -- a molecule that leaves, and the pair the room writes down
# ===========================================================================
# Karig's measured half-activation for 3OC12HSL -- the receiver's half-output
# concentration, written theta_A and NOT bare theta, which session 22 uses for
# the antithetic set-point ratio (docs/symbols.md). NUMBERS.md sec 19.3,
# MEASURED, from their SI dosage-response. The companion value for C4HSL is
# 3 uM -- a thousandfold away, and sec 19.3 is explicit that the gap buys no
# orthogonality, because the same SI measures 3OC12HSL competitively binding
# RhlR. That pair and that caution are segment 1's karig2018_fig1 slide; this
# figure takes the one threshold it needs to place a dose-response.
KARIG_THETA_3OC12 = 0.003              # uM


def fig_sender_receiver(name="s24_sender_receiver"):
    """The minimal pair, composed: the promoter decides which density is noticed.

    MOVE 1's BUILD, and this is T64 -- sender/receiver model construction,
    assessed on PS9 and on the final. The two equations the room writes are

        sender:    dA/dt = k_I S - gamma_A A   (- D A in a reactor)
        receiver:  output = alpha A^n / (theta_A^n + A^n)

    and the figure is what you get when you COMPOSE them. The sender's steady
    state is one line, A* = k_I S/(gamma_A + D), so the signal a receiver sees
    is a promoter divided by a pump -- and the two rules on this figure are the
    SAME population of senders behind two different promoters.

    k_I IS OURS AND THE FIGURE SAYS SO. Neither required paper prints a sender
    synthesis rate: Basu's model is receiver-only and their Methods tune the
    senders to put a ring at 7 mm without printing the value, and Balagadde's
    equations are in a supplement this repo does not hold. So the session
    supplies k_I, out loud, and k_I is a PROMOTER CHOICE -- which is the one
    design knob this half of the model has.

    WHAT A STUDENT CONCLUDES: a population reports its own density, and the
    density at which the receiver notices is set by the sender's promoter.

    MODEL: the course's own minimal pair, through `posb.sender_receiver`.
    """
    theta, n = KARIG_THETA_3OC12, 2.0
    gamma_A, D = 0.01, 0.0          # 1/min; a plate, so no dilution
    kI_S = 1.0e-5                   # uM/min -- OURS, and unprinted
    lo_star = kI_S / (gamma_A + D)
    hi_star = 4.0 * lo_star
    # The steady state is the module's own equation, not a restatement of it:
    # at A* the sender's dA/dt is zero, and this asserts it rather than says it.
    for Astar, k in ((lo_star, kI_S), (hi_star, 4.0 * kI_S)):
        assert abs(float(sender_receiver(Astar, 1.0, k, gamma_A, D)[0])) < 1e-12

    A = np.logspace(-4.2, -1.4, 600)
    out = sender_receiver(A, 1.0, kI_S, gamma_A, D, theta=theta, n=n)[1]
    lo_out = float(sender_receiver(lo_star, 1.0, kI_S, gamma_A, D,
                                   theta=theta, n=n)[1])
    hi_out = float(sender_receiver(hi_star, 1.0, 4.0 * kI_S, gamma_A, D,
                                   theta=theta, n=n)[1])

    fig, ax = plt.subplots(figsize=(10.0, 4.02))
    ax.semilogx(A, out, color=TEAL, lw=3.4, zorder=4)
    # The half-activation guide only has to reach theta_A. Run full width it
    # crossed every clear region the figure had left.
    ax.plot([1e-4, theta], [0.5, 0.5], color=MUTED, lw=1.8, ls=":",
            zorder=2)
    ax.plot([theta] * 2, [0.0, 0.5], color=MUTED, lw=1.8, ls=":", zorder=2)
    for xv, yv, col in ((lo_star, lo_out, MUTED), (hi_star, hi_out, AMBER)):
        ax.plot([xv, xv], [0.0, yv], color=col, lw=2.6, ls="--", zorder=3)
        ax.plot([xv], [yv], "o", ms=12, color=col, zorder=6)

    ax.set_xlim(1e-4, 4e-2)
    ax.set_ylim(0, 1.24)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.grid(True, which="major", color=RULE, lw=0.7)
    # Below the half-activation rule and right of the theta_A rule: at the
    # top left this tag reached down across 580 px of the 0.5 line.
    _tag(ax, 0.98, 0.03, f"$\\theta_A$ = {theta:g} µM", MUTED, ha="right",
         va="bottom")
    # The two promoters name their own rules from a second axis. In the plot
    # they sat on the rules they labeled, and there is no corner of a
    # sigmoid that a sentence fits in without touching either the curve or
    # one of the two verticals.
    sec = ax.secondary_xaxis("top")
    sec.set_xticks([lo_star, hi_star])
    # Short labels: "one promoter" and "4x that promoter" are 0.6 of a decade
    # apart on this axis and overprinted each other into one run of text.
    # Tick labels are frame, so the gate never sees that happen.
    #
    # BUT THEY MUST NOT BE RATES. This axis is A in µM, and the two ticks
    # were labeled "k_I" and "4k_I" -- k_I is the per-sender SYNTHESIS RATE
    # defined one slide earlier, so a rate was naming a position on a
    # concentration axis. The quantity at the tick is the steady state the
    # rate produces, A*(k_I) = k_I S/(gamma_A + D), which is what the
    # suptitle's own equation calls it. This room's engineers stop on that.
    sec.set_xticklabels(["$A^*(k_I)$", "$A^*(4k_I)$"])

    ax.set_xlabel("signal the senders hold up,  $A$   (µM)", fontsize=LBL)
    ax.set_ylabel("receiver output", fontsize=LBL)
    # No axes title: it needed pad=38 to clear the second axis, and the deck
    # places this one in a 3.90 in band, so every line of furniture is paid
    # for out of the picture.
    # NO TECHNIQUE CODE. "T64:" is an internal label from the coverage
    # matrix -- the only one anywhere in this module -- and it means nothing
    # to the room. It belongs in the docstring, which already carries it.
    fig.suptitle("sender $A^* = k_I S/(\\gamma_A{+}D)$, receiver "
                 "Hill($A$)\n"
                 "$k_I$ is OURS; $\\theta_A$ is Karig's, MEASURED\n"
                 f"the same senders read {lo_out * 100:.0f} % against "
                 f"{hi_out * 100:.0f} %",
                 fontsize=LBL, color=INK, linespacing=1.25)
    _save(fig, name)


# ===========================================================================
# MOVE 2 -- the ledger: how long the wire takes
# ===========================================================================
def fig_diffusion_ledger(name="s24_diffusion_ledger"):
    """Transit time against distance: four decades of L is eight of t.

    MOVE 2's FRAME, where DESIGN sec 3 puts it. For twenty-three sessions a
    connection was a molecule
    inside one cell and its transit time was never a design
    parameter. Put the
    same molecule outside and t goes as L^2, so the wire that crosses a cell in
    milliseconds takes days to cross a plate -- and nothing on the plasmid
    changes that number. The only knob here is WHICH SIGNAL you pick, and
    Karig measured that it is worth about twentyfold.

    WHAT A STUDENT CONCLUDES: outside the cell, delay is set by the geometry
    and the medium, not by the circuit, and it is quadratic in distance.

    MODEL: t = L^2/2D_A, session 2's convention, stated before the number.
    D: Karig's two ESTIMATED effective cell-to-cell coefficients (sec 19.1).
    """
    # FROM ONE CELL UP. Karig's coefficients are EFFECTIVE CELL-TO-CELL
    # values through a lawn (sec 19.1), so below about a cell length there is
    # no lawn for them to be effective through and the curve would be an
    # extrapolation into a regime where the number has no meaning.
    L = np.logspace(0.3, 5.2, 400)           # um
    fig, ax = plt.subplots(figsize=(10.0, 4.6))

    for D, col in ((KARIG_D_3OC12HSL, TEAL), (KARIG_D_C4HSL, CYAN)):
        ax.loglog(L, diffusion_time(L, D), color=col, lw=3.2, zorder=3)

    ax.set_xlim(1.8, 1.4e5)
    ax.set_ylim(1e-3, 2e8)
    ax.set_xticks([10, 1e2, 1e3, 1e4, 1e5])
    ax.set_xticklabels(["10 µm", "100 µm", "1 mm", "10 mm", "100 mm"])
    # The claim is QUADRATIC -- four decades of L is eight of t -- and the y
    # axis is named time units at uneven log positions, so without a decade
    # reference the one thing this figure is for cannot be checked off it.
    # Minor ticks ARE the decades; they carry the grid and no label.
    ax.yaxis.set_minor_locator(mpl_ticker.LogLocator(base=10.0, subs=(1.0,),
                                                     numticks=20))
    # The decades carry the GRID and no label: left formatted, matplotlib
    # printed 10^-2 ... 10^8 straight through "1 ms", "1 s", "1 min",
    # "1 day" and "100 days" and the whole axis was unreadable.
    ax.yaxis.set_minor_formatter(mpl_ticker.NullFormatter())
    # The scales themselves, on a second axis, where a tick is frame and
    # cannot collide with anything. 10 mm is Basu's measured ring (sec 13.3).
    sec = ax.secondary_xaxis("top")
    sec.set_xticks([2.0, 1e4])
    sec.set_xticklabels(["one cell", "Basu's ring, 10 mm"])
    # Named time units as TICKS rather than as labeled rules: a tick is
    # frame, so it cannot collide with a curve, and the room reads "1 day"
    # without doing arithmetic on an exponent.
    # No "1000 days": it sits one decade above "100 days", which at this
    # figure height is 42 px for a 44 px label, and tick labels are frame --
    # the gate never looks at them, so this one has to be looked at.
    # No "1 h": it sits 1.38 decades under "1 day", which at this figure
    # height is 10 px of clearance for a 43 px glyph box and reads as
    # touching from the back of the room. Tick labels are frame, so the gate
    # never looks at them -- this one has to be looked at.
    ax.set_yticks([1e-3, 1.0, 60.0, 86400.0, 8.64e6])
    ax.set_yticklabels(["1 ms", "1 s", "1 min", "1 day", "100 days"])
    ax.grid(True, which="minor", axis="y", color=RULE, lw=0.6)
    ax.grid(True, which="major", axis="x", color=RULE, lw=0.7)

    # Both labels sit in the empty wedge BELOW the faster curve. Parallel
    # log-log lines of slope 2 leave two large empty triangles, and this is
    # the one a 20 pt label fits in; the leaders do the pointing.
    _point(ax, (2.2e3, diffusion_time(2.2e3, KARIG_D_3OC12HSL)),
           f"3OC12HSL,  {KARIG_D_3OC12HSL:.0f} µm²/s", TEAL, (0.42, 0.26))
    _point(ax, (1.2e4, diffusion_time(1.2e4, KARIG_D_C4HSL)),
           f"C4HSL,  {KARIG_D_C4HSL:,.0f} µm²/s", CYAN, (0.42, 0.07))

    # TWO lines, not three. The third ("measured ratio 21.6 +/- 10") pushed
    # the block 44 px lower and put its corner on 22 px of the 3OC12HSL
    # curve. The ratio is move 2's Turing number and has a slide there; the
    # three qualifications that must travel with 83 um^2/s are all still here.
    _tag(ax, 0.02, 0.94,
         "Karig 2018, both ESTIMATED:\n"
         "effective cell-to-cell in a lawn", INK, va="top")

    ax.set_xlabel("distance the signal crosses,  $L$", fontsize=LBL)
    ax.set_ylabel("transit time,  $t$", fontsize=LBL)
    # D_A, not a bare D: in this deck a bare D is the reactor's DILUTION
    # RATE, and this is the signal's diffusion coefficient. Renamed with the
    # deck on 8 November; it now sits beside ell_A, gamma_A and theta_A.
    ax.set_title("$t \\approx L^2/2D_A$  ·  session 2's convention, "
                 "stated first",
                 fontsize=LBL, color=INK)
    _save(fig, name)


# ===========================================================================
# MOVE 2 -- how far does it get, and the number this folder cannot give you
# ===========================================================================
def fig_lambda_scaling(name="s24_lambda_scaling"):
    """gamma_A is the knob, and ell_A only goes as its square root.

    MOVE 2's design knob. Once the signal decays, L^2/2D_A is the wrong tool
    and the length scale is ell_A = sqrt(D_A/gamma_A), written $\\ell_A$ on the
    figure -- NOT lambda, which is an eigenvalue in move 4 and in sessions 8,
    11 and 14 (docs/symbols.md). The function and PNG names below are
    historical and were left alone; the symbol the room sees is ell_A. Basu
    hand the physics over on
    p.1134: gamma_A sets the steepness of the gradient and is pH-sensitive, so
    you change it by changing the medium. What the square root costs is on this
    figure -- to double the reach the signal has to last FOUR times as long.

    AND THERE IS NO ell_A FOR BASU'S BAND ON THIS FIGURE, which is T66's real
    lesson (sec 19.4). Both curves are Karig's signals in Karig's own lawn;
    neither molecule is Basu's 3OC6HSL, and Basu's own xi is not a diffusion
    coefficient at all -- see `fig_xi_check`.

    WHAT A STUDENT CONCLUDES: reach is bought with lifetime, at a square-root
    exchange rate, and you cannot read your own ell_A off someone else's
    coefficient.

    MODEL: ell_A = sqrt(D_A/gamma_A), from `penetration_depth`.
    """
    g = np.logspace(-5.2, -0.8, 400)         # 1/s
    fig, ax = plt.subplots(figsize=(10.0, 4.6))

    for D, col in ((KARIG_D_C4HSL, CYAN), (KARIG_D_3OC12HSL, TEAL)):
        ax.loglog(g, penetration_depth(D, g) / 1e3, color=col, lw=3.2,
                  zorder=3)

    ax.set_xlim(5e-6, 2e-1)
    ax.set_ylim(2e-2, 1.4e2)
    ax.grid(True, which="major", color=RULE, lw=0.7)
    # THE LIFETIME, ON THE FIGURE. What costs four times is 1/gamma_A, and
    # the plotted axis is a rate, so without this the title's "four times the
    # lifetime" names a quantity that appears nowhere -- next to a figure
    # whose y axis was just labeled "transit time".
    _inv = lambda v: 1.0 / np.maximum(np.abs(v), 1e-30)
    sec = ax.secondary_xaxis("top", functions=(_inv, _inv))
    sec.set_xlabel("signal lifetime,  $1/\\gamma_A$   (s)", fontsize=LBL)

    # Both in the wedge below the slower curve. These are straight diagonal
    # lines, so a horizontal label anywhere between them crosses one of them:
    # the only clear region is outside the pair.
    _point(ax, (2.3e-4, penetration_depth(KARIG_D_3OC12HSL, 2.3e-4) / 1e3),
           f"3OC12HSL,  {KARIG_D_3OC12HSL:.0f} µm²/s", TEAL, (0.03, 0.03),
           va="bottom")
    _point(ax, (1.7e-3, penetration_depth(KARIG_D_C4HSL, 1.7e-3) / 1e3),
           f"C4HSL,  {KARIG_D_C4HSL:,.0f} µm²/s", CYAN, (0.03, 0.97),
           va="top")

    # Basu's gamma_A = 0.01/min IS inside this range, so the forbidden
    # combination is a readable coordinate on the teal curve. A sweep that
    # contains a point does not assert it -- but the figure has to say why
    # that point is not Basu's ell_A, and that the axis is a sweep at all:
    # no paper in this folder prints a decay rate for either Karig signal.
    _tag(ax, 0.98, 0.95,
         "NOT Basu's $\\ell_A$ — another lawn\n"
         "$\\gamma_A$ swept, not sourced", RED, ha="right", va="top")

    ax.set_xlabel("signal decay rate,  $\\gamma_A$   (s$^{-1}$)", fontsize=LBL)
    # SHORT, because a y label is rotated: at 20 pt "penetration depth,
    # ell_A (mm)" is 600 px of ink against a 416 px axes, so it overflows
    # top and bottom and the tight bbox clips it. The name goes in the title.
    ax.set_ylabel("$\\ell_A$   (mm)", fontsize=LBL)
    ax.set_title("penetration depth $\\ell_A=\\sqrt{D_A/\\gamma_A}$\n"
                 "four times the lifetime buys twice the reach",
                 fontsize=LBL, color=INK, linespacing=1.25)
    _save(fig, name)


def _box(ax, x, y, t, c=INK, pad=0.34):
    """A node plate. RETURNS the artist, because its drawn extent is needed.

    The plate is opaque and sits at zorder 6; anything that has to stop at its
    edge has to be measured against the edge the renderer actually drew, not
    against a constant. See `_plate_halves`.
    """
    return ax.text(x, y, t, ha="center", va="center", color=c, fontsize=LBL,
                   zorder=6, linespacing=1.25,
                   bbox=dict(boxstyle=f"round,pad={pad}", facecolor=PAGE,
                             edgecolor=c, linewidth=2.0))


# Move 2's derivation column. ONE SCENE, TWO STAGES: the senders, the signal,
# the receivers and the distance axis are identical in both, and stage 2 adds
# the profile above them. `derivation_fig` exists so that the drawing grows as
# the algebra does -- a cartoon in stage 1 replaced by a graph in stage 2 is a
# scene change, not a build.
#
# THE GEOMETRY IS A PLANE SOURCE, AND THE FIGURE SAYS SO. exp(-x/ell_A) is
# the steady profile of a diffusing, decaying signal from a PLANAR source in
# one dimension. A localized sender gives K_0(r/ell_A) in two dimensions and
# exp(-r/ell_A)/r in three, and neither is an exponential -- so the senders
# are drawn as a wall and the receivers as a line running away from it, which
# is the geometry the algebra assumes. The previous cartoon drew a localized
# sender and then answered with the 1-D solution.
#
# AND IT HAS THE MECHANISM IN IT: LuxI in the senders, AHL as a labeled
# species out in the medium with its gradient drawn, LuxR in the receivers.
# The earlier version drew a filled circle labeled S -- which named nothing,
# and collided with the S of dA/dt = k_I S - gamma_A A in the same hour.
_LAM_CELLS = (0.75, 1.75, 2.85, 3.95)


def fig_lambda_step(step):
    """Move 2's derivation column: the senders and receivers, then the profile.

    The length on the x axis is ell_A = sqrt(D_A/gamma_A), drawn $\\ell_A$. The
    function and PNG names are historical; see `fig_lambda_scaling`.
    """
    if step not in (1, 2):
        raise ValueError(f"fig_lambda_step: no step {step}")
    from matplotlib.patches import Ellipse

    fig, ax = _col()
    ax.set_xlim(-1.3, 4.3)
    ax.set_ylim(-1.08, 1.22)

    # --- the scene, identical in both stages -------------------------------
    ax.add_patch(plt.Rectangle((-1.3, -0.46), 1.3, 0.36, facecolor=TEAL,
                               edgecolor="none", zorder=4))
    ax.text(-0.65, -0.28, "LuxI", ha="center", va="center", color=PAGE,
            fontsize=LBL, zorder=6)
    # The gradient, drawn: AHL sampled with density proportional to
    # exp(-x/ell_A), which is the profile stage 2 then plots.
    rng = np.random.default_rng(24)
    xs = -np.log(rng.uniform(np.exp(-4.25), 1.0, 150))
    ax.plot(xs, rng.uniform(-0.44, -0.12, xs.size), "o", ms=5, color=AMBER,
            alpha=0.8, zorder=5)
    for cx in _LAM_CELLS:
        # Ellipse, not Circle: x and y are on different pixel scales here, so
        # a Circle renders as an oval.
        ax.add_patch(Ellipse((cx, -0.28), 0.44, 0.21, facecolor=PAGE,
                             edgecolor=CYAN, linewidth=2.8, zorder=6))
    # Out where the profile has decayed: nearer the wall the label sat
    # either on the curve or on the very dots it names.
    #
    # AND THE LEADER COMES DOWN THE MIDDLE OF A GAP. It used to end at
    # x = 3.2, which is 0.13 from the rim of the receiver at 2.85 (the
    # ellipses are 0.44 wide, so that one runs 2.63 to 3.07) -- close enough
    # that the leader read as pointing AT a receiver rather than at the
    # signal between them. That is bar sec D5d item 3, a leader crossing the
    # object it points past, and it is the one defect on this figure a
    # reader cannot resolve by looking harder.
    #
    # The receivers sit at 0.75, 1.75, 2.85 and 3.95, so the clear lanes are
    # 0.97-1.53, 1.97-2.63 and 3.07-3.73. The target is the CENTRE of the
    # last one, 3.40, which is 0.33 from either rim, and the label is
    # centerd over it so the leader falls vertically down that lane instead
    # of slanting across it. In axes fractions 3.40 is (3.40+1.3)/5.6.
    _point(ax, (3.40, -0.30), "AHL", AMBER, ((3.40 + 1.3) / 5.6, 0.62),
           ha="center", va="bottom")
    ax.text(0.75, -0.52, "LuxR", ha="center", va="top", color=CYAN,
            fontsize=LBL, zorder=7)
    ax.text(4.25, -0.80, "a plane source, one dimension", ha="right",
            va="top", color=MUTED, fontsize=LBL, zorder=7)

    ax.set_xlabel("distance from the senders,  $x$", fontsize=LBL)
    ax.spines["left"].set_visible(step == 2)
    ax.spines["bottom"].set_visible(True)

    if step == 1:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(1.5, 0.62, "$A(x) = ?$", ha="center", va="center", color=INK,
                fontsize=TYPE["emphasis"], zorder=7)
    else:
        u = np.linspace(0, 4.25, 400)
        ax.plot(u, np.exp(-u), color=TEAL, lw=3.4, zorder=4)
        ax.plot([1.0, 1.0], [0.0, np.exp(-1.0)], color=AMBER, lw=2.4,
                ls="--", zorder=3)
        ax.plot([0.0, 1.0], [np.exp(-1.0)] * 2, color=MUTED, lw=1.8, ls=":",
                zorder=3)
        ax.plot([1.0], [np.exp(-1.0)], "o", color=AMBER, ms=11, zorder=6)
        ax.set_xticks([0, 1, 2, 3, 4])
        ax.set_xticklabels(["0", "$\\ell_A$", "2$\\ell_A$",
                            "3$\\ell_A$", "4$\\ell_A$"])
        # A_0 IS DEFINED BY THE AXIS: it is the signal at the wall, which is
        # where the tick sits. Naming it only in the y label would be a
        # quantity arriving from nowhere.
        ax.set_yticks([0.0, np.exp(-1.0), 1.0])
        ax.set_yticklabels(["0", "$A_0/e$", "$A_0$"])
        ax.set_ylabel("signal  $A$", fontsize=LBL)
        ax.text(1.15, 1.18, "$\\ell_A=\\sqrt{D_A/\\gamma_A}$", ha="left",
                va="top", color=AMBER, fontsize=LBL, zorder=7)

    fig.subplots_adjust(left=0.23, right=0.97, top=0.99, bottom=0.17)
    _save_column(fig, f"s24_lambda_step_{step}")


def fig_xi_check(name="s24_xi_check"):
    """Basu's own xi puts Basu's own ring weeks after the experiment ended.

    MOVE 2's cautionary slide, and T66's engineering lesson. Substituting the
    paper's printed xi into the course's own t = L^2/2D_A sends every ring in
    paper's own figures far past the end of its 36-hour experiment. Equation
    (5) is a bare discrete Laplacian with no grid spacing, so xi is really
    D/dx^2 with dx never stated: the printed units are the units of D and the
    quantity is not one.

    WHAT A STUDENT CONCLUDES: check a published coefficient's units against
    that paper's own geometry before using it, because this one fails its own
    figures by one to two orders of magnitude.

    MODEL: t = L^2/2xi -- the course's convention run on the paper's number.
    """
    fig, ax = plt.subplots(figsize=(10.0, 4.17))

    ys = np.arange(len(BASU_RINGS))[::-1]
    hours = [float(diffusion_time(L, BASU_XI)) / 60.0 for L, _ in BASU_RINGS]
    # LINEAR, and that is the whole figure. On a log axis a bar from `left`
    # encodes log(t) - log(left), so 833 h drew about 30 % longer than 300 h
    # when it is 2.8x longer, and the 36 h rule sat just beside bars that are
    # 8x to 23x past it -- a figure arguing "one to two orders of magnitude"
    # in which nothing looked like an order of magnitude. Linear from zero
    # makes the rule a sliver and the bars enormous, which IS the argument.
    ax.barh(ys, hours, color=RED, height=0.46, alpha=0.85, zorder=2)
    for y, h in zip(ys, hours):
        ax.text(h + 18.0, y, f"{h:.0f} h", va="center", ha="left", color=INK,
                fontsize=LBL, zorder=6)
    ax.set_yticks(ys)
    # ONE LINE EACH: two-line tick labels on rows 87 px apart overlap each
    # other, and tick labels are frame, so the gate cannot see it happen.
    ax.set_yticklabels([f"{L:.0f} mm · {src}" for L, src in BASU_RINGS],
                       fontsize=LBL)

    ax.axvline(BASU_RUN_H, color=INK, lw=3.0, zorder=4)
    ax.set_xlim(0, 900)
    ax.set_ylim(-1.5, 2.6)
    ax.grid(True, axis="x", which="major", color=RULE, lw=0.7)

    # In the empty lane BETWEEN two bar rows: at the top it ran into the
    # "300 h" value label, and at the bottom its center would fall inside a
    # bar, which is checked for text spilling its patch.
    # ABOVE the top bar, in headroom made for it. Between the rows there is
    # only 61 px of clear lane and this tag is 110 px tall; at the bottom its
    # center would land inside a bar, which is checked for text spilling its
    # own patch. Both were measured, not guessed.
    # The rule is labeled IN the figure: a symbol drawn and not named is a
    # symbol the room has to be told about out loud.
    _point(ax, (BASU_RUN_H, -0.62), "the 36 h the experiment ran", INK,
           (0.10, 0.06), va="bottom")

    ax.set_xlabel("time to reach the ring,  $t = L^2/2\\xi$", fontsize=LBL)
    # The 36 h rule is named in the title rather than labeled in the axes.
    # A label for it had nowhere to sit that did not either cross the rule
    # itself or print on top of a bar -- and a label on a bar is invisible to
    # figure_fit, because a bar is a patch and not plotted data.
    # Everything but the bar values and the rule's own label is title. A
    # three-row panel has no corner a two-line note fits in: it collided
    # with a value label at the top, with a bar in the middle and with the
    # rule's label at the bottom, and each move produced the next collision.
    ax.set_title("Basu's own $\\xi$ = 0.001 mm²/min, used as a $D_A$\n"
                 "really $D_A/\\Delta x^2$; $\\Delta x$ unstated; only 10 mm "
                 "is an experiment", fontsize=LBL, color=INK,
                 linespacing=1.3)
    _save(fig, name)


# ===========================================================================
# MOVE 3 -- one motif, a new input: the band detector
# ===========================================================================
def _band_curve(ax, params):
    """Basu's band response on a log AHL axis, in nM. Returns peak and edges."""
    A_peak, G_peak = band_peak(params)
    lo, hi = band_edges(params)
    # lo/6 to hi*6, not lo/20 to hi*20: at twenty the off-states ate 55-60 %
    # of the plot width as a flat line at zero and the band itself was a
    # spike. Six still shows OFF at both ends and doubles the band.
    A = np.logspace(np.log10(lo / 6.0), np.log10(hi * 6.0), 800)
    ax.semilogx(A * 1e3, band_detect_response(A, params), color=TEAL, lw=3.4,
                zorder=4)
    ax.set_xlim(lo * 1e3 / 6.0, hi * 1e3 * 6.0)
    ax.set_ylim(0, G_peak * 1.16)
    ax.grid(True, which="major", color=RULE, lw=0.7)
    return A_peak, G_peak, lo, hi


def fig_band_response(name="s24_band_response"):
    """One interior maximum, with both edges solved from the printed parameters.

    MOVE 3, and T65. The response is OFF, ON, OFF across AHL: L has two
    production terms that move in opposite directions with A, so GFP is dark
    at high signal, dark at low signal, and bright only where CI has silenced
    wild-type LacI while LacI_M1 is still under the threshold that would
    silence GFP.

    BOTH EDGES ARE SOLVED, NOT READ OFF THE PLOT. `band_edges` roots
    G(A) - 0.5 G_peak in log A by Brent's method, at the half maximum because
    that is Basu's own ring criterion (p.1134). On the printed BD2 set they
    come back a factor of 2.65 apart.

    WHAT A STUDENT CONCLUDES: this circuit's output is non-monotone in its
    input, and its two edges are properties of the printed parameters that you
    can solve for rather than measure off a curve.

    MODEL: Basu 2005 equations (1)-(4), liquid-phase limit, printed BD2 set.
    """
    p = basu_params("BD2")
    fig, ax = plt.subplots(figsize=(10.0, 4.36))
    A_peak, G_peak, lo, hi = _band_curve(ax, p)

    ax.axhline(0.5 * G_peak, color=MUTED, lw=2.0, ls=":", zorder=3)
    for edge in (lo, hi):
        # To the HALF MAXIMUM and no further, because that is where the edge
        # is defined: rule, dotted half-max line and curve then meet at one
        # point instead of the rules stopping in blank space above it.
        ax.plot([edge * 1e3] * 2, [0.0, 0.5 * G_peak], color=AMBER, lw=2.4,
                ls="--", zorder=3)
    ax.plot([A_peak * 1e3], [G_peak], "o", color=AMBER, ms=12, zorder=6)
    # BESIDE their own rules, at a third of the rule's height. Pushed out
    # to the foot of the axes they sat four-fold away from the rule they
    # name and read as labeling nothing.
    for edge, nm, k in ((lo, "lo", 1 / 1.6), (hi, "hi", 1.6)):
        ax.text(edge * 1e3 * k, 0.30 * G_peak, f"$A_{{\\rm {nm}}}$",
                ha="center", va="center", color=AMBER, fontsize=LBL,
                zorder=7)

    _tag(ax, 0.02, 0.97, "BD2, as printed:\n$\\beta_L$ = 0.8 µM\n"
                         "$\\beta_C$ = 0.008 µM", INK, va="top")
    _tag(ax, 0.02, 0.47, "50 % of the peak", MUTED, va="bottom")
    peak_lbl = ax.text(A_peak * 1e3, G_peak * 1.035,
                       f"peak {G_peak:.1f} µM", ha="center",
                       va="bottom", color=AMBER, fontsize=LBL, bbox=_plate(),
                       zorder=7)
    # The SPREAD leads, because the spread and the ordering are what the
    # printed parameters support. The two absolute edges are here because
    # `band_edges` solves them FROM those printed parameters -- they are not,
    # and must never be, a position digitized off the paper's panel.
    _tag(ax, 0.98, 0.97,
         f"{hi / lo:.2f}$\\times$ apart\n"
         f"$A_{{\\rm lo}}$ = {lo * 1e3:.2f} nM\n"
         f"$A_{{\\rm hi}}$ = {hi * 1e3:.2f} nM", AMBER, ha="right",
         va="top")

    ax.set_xlabel("AHL,  $A$   (nM)", fontsize=LBL)
    ax.set_ylabel("GFP,  $G$   (µM)", fontsize=LBL)
    ax.set_title("Basu 2005 eqs (1)–(4), printed BD2 set  ·  model, not "
                 "measured", fontsize=LBL, color=INK)

    # THE HEADROOM IS MEASURED, NOT GUESSED -- the same solve as
    # `fig_band_variants`, for the same defect one figure over. "peak 19.6
    # uM" is anchored in DATA at 1.035 G_peak so that it stays attached to
    # the marker it names, and under a y limit of 1.16 G_peak its plate
    # finished 8.4 px under the axes title: inside `figure_fit`'s 10 px GAP,
    # and close enough at the back of Dwinelle 219 to read as one block with
    # the provenance line. Text against a title is bar sec D5d item 2, and
    # the gate was blind to it until `ax.title` became a collision target.
    #
    # THIS RUNS LAST, AFTER EVERY PIECE OF FURNITURE INCLUDING `set_title`.
    # Measured before the title exists, the axes is 0.35 in taller than the
    # one that is saved and the label is credited with room it then loses.
    #
    # SOLVED, NOT NUDGED. The label's height is a constant FRACTION f of the
    # axes, so expanding the limit by "label top times a margin" makes the
    # label taller in data units again and the correction creeps in by a few
    # per cent a pass. The fixed point is closed form: the label's bottom
    # sits at `anchor` data units, so its top is at anchor/R + f of the axes,
    # and anchor/R + f <= ceiling gives R >= anchor / (ceiling - f). It is
    # then VERIFIED by re-measuring, because f itself shifts when the y tick
    # labels change width and move the axes box.
    anchor = G_peak * 1.035
    for _ in range(8):
        box = _settle(fig, ax)
        rend = fig.canvas.get_renderer()
        bb = peak_lbl.get_bbox_patch().get_window_extent(rend)
        ceiling = _title_ceiling(ax, box, rend)
        f = bb.height / box.height
        if (bb.y1 - box.y0) / box.height <= ceiling:
            break
        if ceiling - f <= 0.0:
            raise AssertionError(
                f"fig_band_response: the peak label is {f:.2f} of the axes "
                f"tall against a ceiling of {ceiling:.2f}, so no y limit can "
                f"clear the title. The axes has to get taller or the label "
                f"has to leave the axes.")
        ax.set_ylim(0, max(G_peak * 1.16, anchor / (ceiling - f)))
    else:
        raise AssertionError(
            "fig_band_response: the peak label would not settle clear of "
            "the axes title in eight passes -- look at the pixels before "
            "trusting this figure.")
    _save(fig, name)



def fig_band_variants(name="s24_band_variants"):
    """Three strains, three detection thresholds -- and one of them is a knob.

    MOVE 3's threshold slide, which DESIGN sec 5 asks for by name: our three
    curves stand in for Basu's Fig. 2c, and they are exact, because the module
    IS their printed model run on their printed BD1, BD2 and BD3 sets. Their
    MEASURED triple goes on the same slide as a paper crop with its own
    attribution; nothing measured is drawn here.

    WHAT THE THREE CHANGES DO. BD1 is BD2 with rho_R raised tenfold, which is
    how the hypersensitive LuxR-G2F mutant is represented -- and since A enters
    only as rho_R [LuxR]^2 A^2 / gamma_R, that shifts the whole response to
    lower AHL by EXACTLY sqrt(10) and changes its shape not at all. The tests
    pin that to nine digits, and it is the cleanest analytic check in the file.
    BD3 halves alpha_G, alpha_L2 and [LuxR]: halving [LuxR] moves the response
    the other way, halving alpha_G lowers the peak, and halving alpha_L2
    changes the SHAPE -- so BD3's band is also wider, 3.39x against 2.65x.

    WHAT A STUDENT CONCLUDES: a receiver's detection threshold is something you
    set -- by a point mutation in the receptor, or by copy number -- and the two
    routes do not have the same side effects.

    MODEL: Basu 2005 equations (1)-(4), liquid-phase limit, printed BD1/BD2/BD3.
    """
    sets = (("BD1", TEAL), ("BD2", AMBER), ("BD3", CYAN))
    peaks, edges = {}, {}
    for v, _ in sets:
        q = basu_params(v)
        peaks[v] = band_peak(q)
        edges[v] = band_edges(q)

    lo_x = edges["BD1"][0] / 8.0
    hi_x = edges["BD3"][1] * 8.0
    A = np.logspace(np.log10(lo_x), np.log10(hi_x), 900)

    fig, ax = plt.subplots(figsize=(10.0, 3.94))
    for v, col in sets:
        ax.semilogx(A * 1e3, band_detect_response(A, basu_params(v)),
                    color=col, lw=3.4, zorder=4)
    top = max(g for _, g in peaks.values())
    ax.set_xlim(lo_x * 1e3, hi_x * 1e3)
    ax.set_ylim(0, top * 1.22)
    ax.grid(True, which="major", color=RULE, lw=0.7)

    labels = []
    for v, col in sets:
        Ap, Gp = peaks[v]
        ax.plot([Ap * 1e3], [Gp], "o", color=col, ms=11, zorder=6)
        # NO PLATE. These sit in empty space above their own peaks and need
        # none, and at Gp*1.04 under an ms=11 marker the plate's pad took a
        # bite out of all three dots -- 123 px of BD3's cyan apex -- which
        # the gate scores zero because a text box never touches a *point*.
        labels.append(
            ax.text(Ap * 1e3, Gp * 1.09, v, ha="center", va="bottom",
                    color=col, fontsize=LBL, zorder=7))


    # THE ONLY TEXT INSIDE THE AXES IS THE THREE STRAIN NAMES. Three bumps
    # in a row leave no corner that a sentence fits in without landing on a
    # peak label or on a curve, so everything else is title, which has the
    # full figure width and is frame rather than content-over-data.
    shift = peaks["BD2"][0] / peaks["BD1"][0]
    w3 = edges["BD3"][1] / edges["BD3"][0]
    w2 = edges["BD2"][1] / edges["BD2"][0]
    spread = float(np.log10(peaks["BD3"][0] / peaks["BD1"][0]))
    ax.set_xlabel("AHL,  $A$   (nM)", fontsize=LBL)
    ax.set_ylabel("GFP,  $G$   (µM)", fontsize=LBL)
    # BD3's peak is lower because alpha_G is halved, and wider because
    # alpha_L2 is -- "halved copies" was one phrase for three changes with
    # three different effects, on the figure where the room has to tell them
    # apart. And the spread is the quantity this figure can honestly carry.
    # Three bumps in a row leave no corner a sentence fits in without
    # touching a peak label, so everything but the three names is frame.
    ax.set_title("BD1: $\\rho_R\\times10$, exactly $\\sqrt{10}$ lower\n"
                 "BD3: $\\alpha_G$ halved, so lower", fontsize=LBL,
                 color=MUTED, linespacing=1.2)
    fig.suptitle("Basu's printed BD1/BD2/BD3 — model, not measured\n"
                 f"eqs (1)–(4); read ordering and spread "
                 f"({spread:.3f} decades)",
                 fontsize=LBL, color=INK, linespacing=1.25)

    # THE HEADROOM IS MEASURED, NOT GUESSED. BD1 and BD2 have the SAME peak
    # height -- BD1 is BD2 with rho_R raised, which shifts the response and
    # does not change its shape -- so both sat at top*1.09 under a ylim of
    # top*1.22, and a 20 pt label is about 0.14 of the axes tall. Both ran
    # out through the top of the axes into the axes title, where "BD2"
    # printed through "BD3: alpha_G halved, so lower". Text against a title
    # is bar sec D5d item 2, and neither `figure_fit` nor `slide_fit` sees it.
    #
    # THIS RUNS LAST, AFTER EVERY PIECE OF FURNITURE. Placed up beside the
    # labels it measured an axes that had no title yet -- so tight_layout
    # gave it the full height, the labels fitted, the loop broke on its first
    # pass, and then `set_title` took 0.35 in back and put them out again.
    # A measurement is only worth what the geometry was when it was taken.
    #
    # Raising ylim by another hand-picked multiplier is the move that put the
    # labels there, so the renderer is asked instead: open the axes until the
    # labels are inside it.
    #
    # AND THE MEASUREMENT HAS TO BE TAKEN AFTER `tight_layout`, which is the
    # trap bar sec D5b closes with: tight_layout makes the axes size
    # content-dependent, so a label measured before it occupies FEWER data
    # units than the same label after it. Measuring first gave a label height
    # of 0.14 of the axes where the saved figure has 0.27, the correction was
    # half what it needed to be, and "BD2" still printed through the title --
    # a fix that measured the wrong geometry and reported success.
    #
    # SOLVED, NOT NUDGED. Expanding ylim by "label top times a margin" is a
    # fixed-point iteration that creeps: the label's height is a constant
    # FRACTION f of the axes, so each expansion makes the label taller in
    # data units again and the correction converges by a few per cent a pass.
    # Five passes was not enough and the guard fired. The fixed point has a
    # closed form -- anchor + f.R <= R/margin gives R >= margin.anchor /
    # (1 - margin.f) -- so it is solved directly and then VERIFIED by
    # re-measuring, because f itself shifts a little when the y tick labels
    # change width and move the axes box.
    for _ in range(8):
        fig.tight_layout()
        fig.canvas.draw()
        rend = fig.canvas.get_renderer()
        inv = ax.transData.inverted()
        hi = ax.get_ylim()[1]
        boxes = [t.get_window_extent(rend) for t in labels]
        if max(inv.transform([b.x0, b.y1])[1] for b in boxes) <= hi / 1.01:
            break
        f = max(b.height for b in boxes) / ax.get_window_extent(rend).height
        anchor = max(g for _, g in peaks.values()) * 1.09
        if 1.0 - 1.04 * f <= 0.0:
            raise AssertionError(
                f"fig_band_variants: a strain label is {f:.2f} of the axes "
                f"tall, so no y limit can contain it. The axes has to get "
                f"taller or the label has to leave the axes.")
        ax.set_ylim(0, max(top * 1.22, 1.04 * anchor / (1.0 - 1.04 * f)))
    else:
        raise AssertionError(
            "fig_band_variants: the strain labels would not settle inside "
            "the axes in eight passes -- look at the pixels before trusting "
            "this figure.")
    _save(fig, name)


def fig_band_step(step):
    """Move 3's derivation column: find the peak, define the edge, solve it."""
    p = basu_params("BD2")
    fig, ax = _col()
    A_peak, G_peak, lo, hi = _band_curve(ax, p)
    ax.set_xlabel("AHL,  $A$  (nM)", fontsize=LBL)
    ax.set_ylabel("GFP,  $G$  (µM)", fontsize=LBL)

    if step not in (1, 2, 3):
        raise ValueError(f"fig_band_step: no step {step}")
    # STAGE 1 IS THE CURVE AND NOTHING ELSE. It used to carry the peak marker
    # and "peak 19.6 µM" while the run's first algebra line says only "the
    # response we have" -- so the figure answered the run's SECOND step,
    # "find the peak", one slide before the step was put. The lambda run two
    # segments earlier gets this right: its stage 1 shows "A(x) = ?".
    #
    # The deck advances this run as [stage 1, unchanged, stage 2, stage 3],
    # so "find the peak" is put against the bare curve and the answer arrives
    # with stage 2 -- which is the step that first USES G_peak, because half
    # the maximum cannot be drawn before the maximum.
    if step >= 2:
        ax.plot([A_peak * 1e3], [G_peak], "o", color=AMBER, ms=12, zorder=6)
        _tag(ax, 0.03, 0.97, f"peak {G_peak:.1f} µM", AMBER, va="top")
        ax.axhline(0.5 * G_peak, color=MUTED, lw=2.0, ls=":", zorder=3)
        _tag(ax, 0.03, 0.46, "50 %", MUTED, va="bottom")
    if step >= 3:
        for edge in (lo, hi):
            ax.plot([edge * 1e3] * 2, [0.0, 0.5 * G_peak], color=AMBER,
                    lw=2.4, ls="--", zorder=3)
        ax.text(lo * 1e3 / 1.6, 0.30 * G_peak, "$A_{\\rm lo}$",
                ha="center", va="center", color=AMBER, fontsize=LBL,
                zorder=7)
        ax.text(hi * 1e3 * 1.6, 0.30 * G_peak, "$A_{\\rm hi}$",
                ha="center", va="center", color=AMBER, fontsize=LBL,
                zorder=7)
        _tag(ax, 0.97, 0.97, f"{hi / lo:.2f}$\\times$", AMBER,
             ha="right", va="top")
    fig.subplots_adjust(left=0.21, right=0.97, top=0.97, bottom=0.18)
    _save_column(fig, f"s24_band_step_{step}")


# ===========================================================================
# MOVE 4 -- two populations, and where the oscillation actually lives
# ===========================================================================
# THE MODEL ON EVERY FIGURE BELOW IS THE BIOMODELS DEPOSIT BIOMD0000000296,
# not Balagadde's text, which prints no equations at all. Each figure says so.
#
# The column schematics are a RING OF FOUR -- predator, its signal, prey, its
# signal -- because that is what the loop is, and it points straight back at
# session 11's ring of three. The QSSA shortens the ring to two, and the
# oscillation leaves with the two nodes it removed.
# THE RING IS LAID OUT BY HAND AND SO ARE THE ARROWS. `shrinkA/shrinkB` is a
# radial shrink from a node's CENTRE, which works for a circle and not for a
# wide rectangle: at the first cut three of the four arrowheads finished
# underneath the box they pointed at, and the two signal boxes -- which had
# the molecule names in them -- ran off both edges of the figure. So the
# molecule names moved into the stamp and each arrow is given explicit
# endpoints just outside the boxes it joins. Node centers, in the drawing
# square:
_RING = {"C1": (50.0, 86.0), "A1": (80.0, 50.0),
         "C2": (50.0, 14.0), "A2": (20.0, 50.0)}
# THE BOX HALF-EXTENTS ARE MEASURED, NOT DECLARED, and that is the whole
# point of `_plate_halves`. They were a hand-coded dict -- C1 at (14.5, 8.0)
# -- and the half-HEIGHT was wrong by a factor of two: the drawn plate of the
# two-line "predator / C_1" label is 15.69 data units tall-half, not 8.0, so
# the computed endpoint of the A2 -> C1 arrow landed 6.1 units (about 50 px)
# INSIDE the plate. The plate is opaque and sits at zorder 6 against the
# arrow's zorder 3, so that arrowhead was painted out on six slides -- the
# rescue arm, on a figure whose own stamp says "every arrow leaves the cell".
# A second hand-coded pair would produce the next one, so there is no constant
# here to re-guess: the renderer is asked where it put the plate.
#
# Measuring in DATA units is dpi-independent: the plate's pixel size and the
# axes' pixel size both scale with dpi, so the ratio does not move between the
# measuring draw and savefig.


def _plate_halves(fig, ax, boxes):
    """Half-width and half-height of each node's DRAWN plate, in data units.

    `boxes` maps node name -> the Text returned by `_box`. The figure must
    already be at its final geometry (subplots_adjust done) when this is
    called, because the data-to-pixel transform is what the conversion uses.
    """
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    half = {}
    for node, art in boxes.items():
        bb = art.get_bbox_patch().get_window_extent(rend)
        (x0, y0), (x1, y1) = inv.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
        half[node] = (abs(x1 - x0) / 2.0, abs(y1 - y0) / 2.0)
    return half


def _ring_ends(a, b, half, gap=1.6):
    """Endpoints on each box's own drawn boundary, along the center line."""
    (x0, y0), (x1, y1) = _RING[a], _RING[b]
    dx, dy = x1 - x0, y1 - y0
    out = []
    for node, sx, sy in ((a, 1.0, 1.0), (b, -1.0, -1.0)):
        hx, hy = half[node]
        # Scale along the chord until it leaves the box, then add the gap.
        t = min((hx + gap) / abs(dx) if dx else 9e9,
                (hy + gap) / abs(dy) if dy else 9e9)
        cx, cy = (_RING[node][0], _RING[node][1])
        out.append((cx + sx * t * dx, cy + sy * t * dy))
    return out[0], out[1]


def _ring_arrow(ax, a, b, color, rad=0.0, ends=None, half=None):
    p0, p1 = ends if ends else _ring_ends(a, b, half)
    ax.annotate("", xy=p1, xytext=p0, zorder=3,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.8,
                                shrinkA=2, shrinkB=2, mutation_scale=22,
                                connectionstyle=f"arc3,rad={rad}"))


def fig_pp_step(step):
    """Move 4's derivation column: the loop, the QSSA that shortens it, the lag."""
    fig, ax = _col()
    ax.set_xlim(0, 100)
    ax.set_ylim(-70, 104)
    ax.axis("off")
    # AND THE TICKS GO WITH IT, which is not belt-and-braces -- it is the
    # difference between what this figure draws and what a gate can measure.
    # `axis("off")` sets `ax.axison = False`, which short-circuits DRAWING
    # without clearing any artist's own `visible` flag, so every tick label
    # this axes never shows is still a Text with a real bounding box.
    # `figure_fit` filters tick labels on `t.get_visible()`, which is True
    # for all of them, so on 8 November the widened gate reported the stamp
    # below colliding with y-ticks '-50' and '-25' on an axes WITH NO
    # VISIBLE AXIS AT ALL. Verified pixel-identical before and after this
    # pair of calls: the render cannot change, because the axis was already
    # off and `_save_column` writes a fixed canvas, so no tick label was
    # ever reaching `tight_layout` either. Removing them makes this figure's
    # object graph say what its pixels say.
    ax.set_xticks([])
    ax.set_yticks([])
    if step not in (1, 2, 3):
        raise ValueError(f"fig_pp_step: no step {step}")
    four = step in (1, 3)

    # THE PLATES GO DOWN FIRST, THEN THE GEOMETRY IS MEASURED, THEN THE
    # ARROWS. Nothing that has to stop at a plate's edge may be placed before
    # `_plate_halves` has been asked where that edge is, and the figure has to
    # be at its final geometry before the question is asked -- so
    # `subplots_adjust` runs here rather than at the end of the function.
    boxes = {"C1": _box(ax, *_RING["C1"], "predator\n$C_1$", TEAL),
             "C2": _box(ax, *_RING["C2"], "prey\n$C_2$", CYAN)}
    if four:
        boxes["A1"] = _box(ax, *_RING["A1"], "$A_1$", AMBER)
        boxes["A2"] = _box(ax, *_RING["A2"], "$A_2$", AMBER)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0.01)
    half = _plate_halves(fig, ax, boxes)

    if four:
        # Stage 3 is stage 1's picture again, so the two nodes that came BACK
        # are marked: without this the two stages differ only in their
        # caption, on a run whose whole job is to advance the drawing.
        # The highlight is sized off the MEASURED plate too -- on the old
        # constants it was 2.6 units wider than the plate and 1.1 units
        # SHORTER, so the thing meant to frame the box was tucked inside its
        # own top and bottom edges.
        if step == 3:
            for k in ("A1", "A2"):
                hx, hy = half[k]
                ax.add_patch(plt.Rectangle(
                    (_RING[k][0] - hx - 2.6, _RING[k][1] - hy - 2.6),
                    2 * (hx + 2.6), 2 * (hy + 2.6), facecolor=AMBER,
                    alpha=0.18, edgecolor="none", zorder=2))
        _ring_arrow(ax, "C1", "A1", AMBER, half=half)
        _ring_arrow(ax, "A1", "C2", RED, half=half)
        _ring_arrow(ax, "C2", "A2", AMBER, half=half)
        _ring_arrow(ax, "A2", "C1", GREEN, half=half)
        for x, y, t, c in ((82, 74, "makes", AMBER), (82, 26, "kills", RED),
                           (18, 26, "makes", AMBER),
                           (18, 74, "rescues", GREEN)):
            ax.text(x, y, t, ha="center", va="center", color=c, fontsize=LBL,
                    zorder=6, bbox=_plate())
    else:
        # The signals are gone, so the loop is length two -- and so is the lag.
        # The x offsets are the bow; the y ends come off the measured plates,
        # where the hand-coded 70.0 cleared C1's real plate edge by 0.29 data
        # units -- 2.4 px, which is the same near-miss as the four-node ring,
        # just on the lucky side of the border.
        gap = 1.6
        y_c1 = _RING["C1"][1] - half["C1"][1] - gap
        y_c2 = _RING["C2"][1] + half["C2"][1] + gap
        _ring_arrow(ax, "C1", "C2", RED, rad=-0.55,
                    ends=((56.0, y_c1), (56.0, y_c2)))
        _ring_arrow(ax, "C2", "C1", GREEN, rad=-0.55,
                    ends=((44.0, y_c2), (44.0, y_c1)))
        ax.text(66, 50, "kills", ha="left", va="center", color=RED,
                fontsize=LBL, zorder=6, bbox=_plate())
        ax.text(34, 50, "rescues", ha="right", va="center", color=GREEN,
                fontsize=LBL, zorder=6, bbox=_plate())

    # BELOW the ring, not inside it: the signal nodes own the middle of the
    # square, and a stamp there overlapped both of them.
    # Stage 2 says only what the QSSA did. "tr J < 0 — no Hopf" is step 7's
    # shock and `fig_qss_no_hopf` delivers it where the design puts it.
    # Stage 3 uses the deposit's own symbols, and there are TWO lags, not
    # one: 1/(d_AA1+D) = 7.7 h and 1/(d_AA2+D) = 4.5 h at the deposit's
    # dilution rate.
    stamp = {1: "a loop of FOUR: every arrow\n"
                "leaves the cell.  $A_1$ is 3OC12HSL,\n$A_2$ is 3OC6HSL",
             2: "a loop of TWO:\nthe signals are at QSS",
             3: "two lags, $1/(d_{AA1}{+}D)$ and\n"
                "$1/(d_{AA2}{+}D)$ — 7.7 h and 4.5 h\n"
                "at the deposit's $D$ = 0.1125 h$^{-1}$"}[step]
    ax.text(50, -38, stamp, ha="center", va="center", color=INK,
            fontsize=LBL, zorder=7, linespacing=1.35,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=PAGE,
                      edgecolor=RULE, linewidth=1.6))
    _save_column(fig, f"s24_pp_step_{step}")


def fig_pp_phase_plane(name="s24_pp_phase_plane"):
    """The reduced community has one coexistence point, and it is a stable spiral.

    MOVE 4, steps 6 and 7. The nullclines are contours of `pp_qss_model`'s own
    output -- of the PER-CAPITA rates, so the trivial C = 0 nullclines do not
    clutter the picture -- and the fixed points come from `pp_steady_states`,
    which serves both models because substituting the quasi-steady-state
    signals is exact AT a fixed point.

    THE EIGENVALUE PANEL IS THE EVIDENCE AND ITS HELD-FIXED PARAMETERS ARE ON
    THE FIGURE, because an eigenvalue plot without them is unreadable as
    evidence. It is a side panel rather than a true inset for one reason: at
    the 20 pt content floor an inset's own tick labels do not fit inside a
    phase plane, and a figure whose inset cannot be read from the back of the
    room has no evidence on it either.

    WHAT A STUDENT CONCLUDES: with the signals eliminated the community has a
    single coexistence state and it is stable -- the pair spirals in, and the
    trace cannot reach zero to let it do anything else.

    MODEL: the deposited model with the signals at quasi-steady state.
    """
    q = pp_params()
    # 4.52 in authored, not 4.19: the held-fixed block went from two lines to
    # three (see the suptitle). Growing the canvas by the line keeps the
    # panels the height they were -- the comment below warns that a FOURTH
    # line crushed them to 110 px, and it was right, because that line was
    # taken out of the picture instead of being paid for. Measured here:
    # panels 1.29 in before, 1.25 in after, file 4.01 in before, 4.31 after,
    # against the deck's 4.40 in band. `get_tightbbox` omits savefig's
    # pad_inches, 0.1 per side, so the file is 0.20 in taller than the bbox.
    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(9.6, 4.52), gridspec_kw={"width_ratios": [1.5, 1.0]})

    c1 = np.linspace(0.05, 30.0, 420)
    c2 = np.linspace(0.05, 90.0, 420)
    G1, G2 = np.meshgrid(c1, c2, indexing="ij")
    F = pp_qss_model(np.stack([G1, G2], axis=-1), q)
    axL.contour(G1, G2, F[..., 0] / G1, levels=[0.0], colors=[TEAL],
                linewidths=3.2)
    c2_curve = axL.contour(G1, G2, F[..., 1] / G2, levels=[0.0], colors=[CYAN],
                           linewidths=3.2)

    ss = pp_steady_states(q)
    focus = ss["coexistence"][0]
    for key in ("washout", "prey_only", "coexistence"):
        for st in ss[key]:
            ev = np.linalg.eigvals(pp_jacobian(st[:2], q))
            stable = float(np.max(ev.real)) < 0.0
            # zorder above the grid: at zorder 6 the washout marker was
            # bisected by the y = 0 gridline and read as a dome.
            axL.plot([st[0]], [st[1]], "o", ms=14, zorder=9, clip_on=False,
                     color=AMBER if stable else PAGE,
                     markeredgecolor=AMBER if stable else INK, mew=2.6)

    # The Cdot_2 = 0 label used to sit at 0.56, 0.44 -- which is ON the
    # Cdot_1 = 0 branch, so the only text printed over the teal nullcline
    # said "Cdot_2 = 0". Both now sit clear, with leaders.
    # MEASURED, after a wrong guess worth recording: `_plate`'s `pad` is in
    # POINTS, not in fractions of the font size. Halving it from 0.3 moves
    # the plate's edge by 0.4 px, so there is no padding to reclaim here --
    # the plate IS the label's ink box, 61 px of it in a 206 px panel. The
    # room has to come from somewhere else, and below it comes from width.
    c1_lbl = _point(axL, (13.0, 60.0), "$\\dot C_1 = 0$", TEAL, (0.70, 0.90))
    # NOTE: a contour is a LineCollection, not ax.lines, so figure_fit is
    # blind to both nullclines here -- this placement is eye-only, and the
    # earlier one lightened the Cdot_1 = 0 lower branch for about 50 px.
    c2_lbl = _point(axL, (8.4, 3.0), "$\\dot C_2 = 0$", CYAN, (0.56, 0.01),
                    va="bottom")
    # A little negative margin: both boundary fixed points sit ON C1 = 0,
    # and at xlim 0 the left spine cut each marker in half.
    axL.set_xlim(-1.6, 22)
    axL.set_ylim(-5.0, 92)
    axL.set_xlabel("predator,  $C_1$", fontsize=LBL)
    axL.set_ylabel("prey,  $C_2$", fontsize=LBL)
    axL.grid(True, color=RULE, lw=0.6)
    # Every nullcline end in this panel is where the sampling grid stops,
    # not where the branch does -- said here because an unmarked cut makes
    # the Cdot_1 = 0 branch look as though it passes through the prey-only
    # fixed point, and it does not: there the predator's per-capita rate is
    # +0.040 h^-1.
    axL.set_title("filled = stable, open = saddle", fontsize=LBL,
                  color=MUTED)

    ev = np.linalg.eigvals(pp_jacobian(focus[:2], q))
    axR.fill_between([-0.40, 0.0], -0.42, 0.42, color=CYAN, alpha=0.12,
                     zorder=1)
    axR.axvline(0.0, color=RED, lw=2.6, zorder=3)
    axR.axhline(0.0, color=MUTED, lw=1.4, zorder=2)
    axR.plot(ev.real, ev.imag, "o", ms=15, color=AMBER, zorder=6)
    axR.set_xlim(-0.40, 0.14)
    axR.set_ylim(-0.42, 0.42)
    axR.set_xlabel("Re $\\lambda$   (h$^{-1}$)", fontsize=LBL)
    axR.set_ylabel("Im $\\lambda$", fontsize=LBL)
    axR.set_title("a stable spiral at coexistence", fontsize=LBL,
                  color=MUTED)
    axR.grid(True, color=RULE, lw=0.6)

    # Each line a complete clause: the first break used to land after "not
    # the paper's", which reads as though the next line finishes it.
    # FOUR lines, and four is the FLOOR, not a lapse. This block used to say
    # "THREE lines, and no more" -- written when a fourth line was added
    # WITHOUT paying for it and crushed the panels to 110 px. The line was
    # paid for afterwards (canvas 4.19 -> 4.52 in) and the comment was never
    # corrected, so the file spent a day warning against the state it was in.
    # Re-balancing back to three was measured on 8 November and does not fit,
    # for the reason the old comment gives -- WIDTH:
    #
    #   * The four lines render 8.10, 6.70, 7.84 and 8.14 in wide. Re-wrapped
    #     into three, the best balance still needs a 9.996 in line and the
    #     others run to 12.5 in.
    #   * The budget is 9.709 in -- the figure's own ink width. Past that the
    #     suptitle becomes the widest artist and starts setting the tight
    #     bbox; past about 10.04 in the placement scale drops under 1.0 and
    #     20 pt lands under Adam's floor (sec 5.3).
    #   * Three lines would therefore need about 1.7 in of text cut, and the
    #     only candidates are the deposit's accession, "signals at QSS" and
    #     the grid-cut caveat -- each of which is on this figure because
    #     leaving it off was a defect.
    #
    # Nor can the sky come from the canvas instead: a suptitle line costs
    # 53 px of panel, and the type floor leaves only 11 px of figure height
    # (h <= 4.40 in at the deck's 4.40 band) before 20 pt projects under 20.
    # So the panels are 206 px and the labels below are placed against that,
    # not against room that could be found somewhere else.
    # A panel title centerd on the narrow left axes also spills past the
    # figure's left edge, so the binding width is the union, not any line.
    # THREE THINGS WERE WRONG WITH THIS BLOCK AND ALL THREE ARE EXPENSIVE
    # HERE, because slides 65, 66 and 69 teach the room to read a panel off
    # its axes and catch the authors' own unit slips.
    #
    #  * "all h^-1" covered eight quantities of which THREE are not rates:
    #    C_m is a density, K_1 is in (concentration)^2 -- it is added to
    #    A^2 -- and IPTG is a micromolar concentration. The groups are now
    #    split and the second one is named "not rates" out loud.
    #  * It was not reproducible. k_A1, d_AA1 and d_AA2 set a_1 = k_A1/
    #    (d_AA1+D), which is inside BOTH nullclines, and k_A2 sets a_2; none
    #    of the four was printed, so the panel could not be rebuilt from the
    #    figure. All four are here now.
    #  * It printed one K where the model slides and slide 64 write K_1 and
    #    K_2 as distinct symbols. Two generated figures in one move disagreed
    #    about whether there is one K or two; they now both print K_1=K_2.
    fig.suptitle("BIOMD0000000296 — not the paper's text, signals at QSS\n"
                 "h$^{-1}$: $D$=0.1125, $k_{c1}$=0.8, $k_{c2}$=0.4, "
                 "$d_1$=1, $d_2$=0.3,\n"
                 "$d_{AA1}$=0.017, $d_{AA2}$=0.11.   Not rates: "
                 "$k_{A1}$=0.1, $k_{A2}$=0.035,\n"
                 "$C_m$=100, $K_1$=$K_2$=10, IPTG=5 µM;  nullclines cut "
                 "at the grid", fontsize=LBL, color=INK, linespacing=1.2)

    # THE Cdot_1 = 0 LABEL IS PLACED BY THE RENDERER, NOT BY HAND. At its
    # authored (0.70, 0.90) the plate ran to 1.047 of the axes -- 9.7 px out
    # through the top of the panel and 5.3 px INTO "filled = stable, open =
    # saddle". That is bar sec D5d item 2, and it was invisible until
    # `ax.title` became a collision target; it is visible in the 8 November
    # 19:16 deck render, so it predates everything done to this module today.
    #
    # WHY IT IS SOLVED SIDEWAYS AS WELL AS DOWN. This panel is 206 px tall
    # and the plate is 61 of them, so there is one label-height of free sky
    # between the upper Cdot_1 branch and the title and no more. Dropping the
    # label straight down to clear the title leaves 3.5 px over the nullcline
    # -- which is sec D5b's occlusion waiting for the next font-metric
    # difference. Buying the sky by raising the y limit is worse: it pushes
    # every curve DOWN in axes fractions, and the Cdot_2 = 0 label on the
    # floor of this same panel already sits 1.2 px off the lower Cdot_1
    # branch, so the fix would land on the figure's other label. That is
    # gauntlet sec 5.5b in advance rather than in hindsight.
    #
    # The branch DESCENDS to the right, so width is where the room is: the
    # plate is pushed to the right spine, which lowers the curve beneath it
    # by 0.027 of the axes and costs nothing. Both clearances then come out
    # near 10 px and the type never moves (sec 5.3).
    #
    # Offsets are asked of the renderer rather than assumed. `ha="left"` and
    # the plate's own padding mean the anchor is not the plate's corner, and
    # a hand-declared half-extent on this very figure is what buried an
    # arrowhead in an opaque box on six slides.
    # 0.012 of the axes, about 8 px, between the plate and the right spine.
    # This number is the whole budget: the branch under the plate descends
    # about 0.004 of the axes for every 0.01 the plate moves right, so every
    # pixel of inset given back to the spine is a pixel taken off the
    # daylight over the nullcline. At 0.012 the panel yields 14 px above the
    # plate and about 7 below it, and there is no third place to get more.
    RIGHT_INSET = 0.012                 # axes fractions, plate to spine
    for _ in range(8):
        box = _settle(fig, axL)
        rend = fig.canvas.get_renderer()
        bb = c1_lbl.get_bbox_patch().get_window_extent(rend)
        w = bb.width / box.width
        h = bb.height / box.height
        px0 = (bb.x0 - box.x0) / box.width
        pcy = ((bb.y0 + bb.y1) / 2.0 - box.y0) / box.height
        at = c1_lbl.xyann
        ceiling = _title_ceiling(axL, box, rend)
        goal = (1.0 - RIGHT_INSET - w - (px0 - at[0]),
                ceiling - h / 2.0 - (pcy - at[1]))
        if max(abs(at[0] - goal[0]), abs(at[1] - goal[1])) < 1e-3:
            break
        c1_lbl.xyann = goal
    else:
        raise AssertionError(
            "fig_pp_phase_plane: the Cdot_1 label would not settle in eight "
            "passes -- look at the pixels before trusting this figure.")

    # VERIFIED, both ways, on the geometry that is about to be written.
    top = (bb.y1 - box.y0) / box.height
    bottom = (bb.y0 - box.y0) / box.height
    if top > ceiling + 1e-6 or px0 < 0.0 or px0 + w > 1.0:
        raise AssertionError(
            f"fig_pp_phase_plane: the Cdot_1 plate settled at x "
            f"{px0:.3f}..{px0 + w:.3f}, top {top:.3f} against a ceiling of "
            f"{ceiling:.3f} -- it does not fit this panel.")
    # 6 px of VISIBLE daylight -- `_data_top_below` now returns the top of
    # the painted stroke, so this is ink to ink, not center line to plate.
    clear = (bottom - _data_top_below(axL, box, px0, px0 + w, bottom))
    if clear * box.height < 6.0:
        raise AssertionError(
            f"fig_pp_phase_plane: the Cdot_1 plate clears the nullcline "
            f"beneath it by {clear * box.height:.1f} px. Under 6 px a "
            f"translucent plate reads as sitting on the curve (bar sec "
            f"D5b) -- the panel needs height or the label needs to leave "
            f"the axes.")

    # AND THE SAME SOLVE FOR Cdot_2 = 0, which was BLEACHING the branch it
    # sits under. At its authored x its plate top measured 1.2 px from the
    # lower Cdot_1 branch's center line -- which, the branch being 4.4 px
    # wide, is about 1 px ON it, and a 330 dpi crop of the 8 November render
    # shows the teal line visibly lightened for the width of the plate. A
    # label bleaching the curve it names is bar sec D5d item 4, and on this
    # panel the curve IS the content. `figure_fit` cannot see it: no vertex
    # falls strictly inside the plate, so the gate is green either way and
    # the verification has to be a measurement and a crop.
    #
    # It cannot go DOWN -- it is already on the floor of the panel at 0.01 --
    # and it cannot go up. The lower branch RISES to the right, so the room
    # is again sideways, and the boundary is solved rather than searched:
    # everything right of the last painted point that would enter the
    # plate's band is free. The leader gets longer, which is the trade --
    # a long leader is legible, a bleached nullcline is not.
    for _ in range(8):
        box = _settle(fig, axL)
        rend = fig.canvas.get_renderer()
        bb2 = c2_lbl.get_bbox_patch().get_window_extent(rend)
        w2 = bb2.width / box.width
        qx0 = (bb2.x0 - box.x0) / box.width
        qbot = (bb2.y0 - box.y0) / box.height
        qtop = (bb2.y1 - box.y0) / box.height
        at2 = c2_lbl.xyann
        edge = _data_blocking_x(axL, box, qbot, qtop, 6.0 / box.height)
        goal_x = edge + 0.004 - (qx0 - at2[0])
        if abs(at2[0] - goal_x) < 1e-3:
            break
        c2_lbl.xyann = (goal_x, at2[1])
    else:
        raise AssertionError(
            "fig_pp_phase_plane: the Cdot_2 label would not settle in eight "
            "passes -- look at the pixels before trusting this figure.")
    if qx0 + w2 > 1.0 - RIGHT_INSET:
        raise AssertionError(
            f"fig_pp_phase_plane: clearing the branch above Cdot_2 = 0 needs "
            f"the plate at x {qx0:.3f}..{qx0 + w2:.3f}, which runs past the "
            f"right spine. The label has to leave the axes.")
    above = (_data_bottom_above(axL, box, qx0, qx0 + w2, qtop) - qtop)
    if above * box.height < 6.0:
        raise AssertionError(
            f"fig_pp_phase_plane: the Cdot_2 plate is {above * box.height:.1f} "
            f"px under the branch above it -- still bleaching it.")

    # AND THE LEADER LANDS ON THE CURVE'S SIDE, NOT ON ITS CUT END. Moving
    # the label right is what made this matter: the longer leader met the
    # nullcline end-on and in the same cyan, so the two read as one path
    # that turned and rose. `_curve_side_point` re-aims it at the nearest
    # point on the curve's body, measured from where the plate actually
    # settled rather than from the authored (8.4, 3.0).
    c2_lbl.xy = _curve_side_point(
        axL, c2_curve, (bb2.x0, (bb2.y0 + bb2.y1) / 2.0))

    # AND WHAT THE TWO LEADERS PASS, not where they end. Both labels moved,
    # and a longer leader is the price paid for the Cdot_2 move, so the path
    # is the most likely place in this figure for the next defect
    # (gauntlet sec 5.5b).
    for lbl, who in ((c1_lbl, "Cdot_1"), (c2_lbl, "Cdot_2")):
        pb = lbl.get_bbox_patch().get_window_extent(rend)
        tip = axL.transData.transform([lbl.xy])[0]
        start = (pb.x0 if tip[0] < pb.x0 else pb.x1,
                 (pb.y0 + pb.y1) / 2.0)
        gap = _leader_min_gap(axL, box, start, tip)
        if gap < 6.0:
            raise AssertionError(
                f"fig_pp_phase_plane: the {who} leader passes within "
                f"{gap:.1f} px of something it does not name. A leader that "
                f"grazes an object reads as pointing at it (bar sec D5d "
                f"item 3).")
    _save(fig, name)


def fig_qss_no_hopf(name="s24_qss_no_hopf"):
    """tr J = -(k_c1 C_1 + k_c2 C_2)/C_m at EVERY interior fixed point, so < 0.

    MOVE 4's hinge, step 7, drawn as evidence rather than asserted. Left: the
    trace at the interior fixed point across every dilution rate that has one,
    with the closed form drawn underneath it, and everything but D held at the
    deposit's IPTG = 5 values. Right: the same two quantities against each
    other over random parameter sets drawn across IPTG, the dilution rate and
    seven rate constants -- every point on the diagonal, and every point
    negative. The right panel is LOG-LOG IN MAGNITUDES so that the floor of
    the cloud is readable: on linear axes the nearest point to zero is 0.3 %
    of the panel away from it and the evidence cannot be told from a figure
    that touches zero.

    A 2x2 system whose trace cannot reach zero has no Hopf bifurcation. SO THE
    OSCILLATION IS NOT A PROPERTY OF THE TWO POPULATIONS. It belongs to their
    signals, and the QSSA is exactly the step that threw those away.

    WHAT A STUDENT CONCLUDES: an approximation they already know and trust
    removed the phenomenon the session is about, and the algebra says it had to.

    MODEL: the deposited model with the signals at quasi-steady state.
    """
    tr, closed, Ds = [], [], []
    for D in np.linspace(0.002, 0.185, 150):
        q = pp_params(D=D)
        for st in pp_steady_states(q)["coexistence"]:
            Ds.append(D)
            tr.append(float(np.trace(pp_jacobian(st[:2], q))))
            closed.append(-(q["kc1"] * st[0] + q["kc2"] * st[1]) / q["Cm"])

    # 4000, because NUMBERS.md sec 20.3 says 4000 and the file is the
    # authority. An internally reproducible 901 is still not the marked
    # number.
    rng = np.random.default_rng(24)
    rtr, rclosed = [], []
    while len(rtr) < 4000:
        q = pp_params(iptg=rng.uniform(0.0, 20.0), D=rng.uniform(0.0, 0.45),
                      kc1=rng.uniform(0.1, 2.0), kc2=rng.uniform(0.1, 2.0),
                      Cm=rng.uniform(10.0, 500.0), d2=rng.uniform(0.05, 2.0),
                      K1=rng.uniform(1.0, 50.0), K2=rng.uniform(1.0, 50.0),
                      dAA1=rng.uniform(0.005, 0.5),
                      dAA2=rng.uniform(0.005, 0.5))
        for st in pp_steady_states(q, grid=1201)["coexistence"]:
            rtr.append(float(np.trace(pp_jacobian(st[:2], q))))
            rclosed.append(-(q["kc1"] * st[0] + q["kc2"] * st[1]) / q["Cm"])

    # 4.32 in authored, not 3.95: the left panel gained its held-fixed line.
    #
    # THE CEILING ON THIS FIGURE IS 4.14 IN, NOT 4.40, AND IT IS NOT SET BY
    # THIS SESSION. `decks/s25_populations.py` re-uses this PNG and places it
    # at band=4.14, and `figure_fit._placements` keeps the LAST band it reads
    # for a stem, so the tighter of the two is what the type floor is checked
    # against -- correctly, because on session 25's slide the figure really
    # is scaled into 4.14. A figure shared by two decks answers to the
    # smaller band. At 4.45 the file came out 4.26 in and the placement scale
    # fell to 0.973, which puts 20 pt authored at 19.5 pt projected, under
    # the floor, ON SESSION 25'S SLIDE and invisibly from here.
    #
    # Two things to measure rather than assume: `get_tightbbox` excludes
    # savefig's pad_inches, 0.1 PER SIDE, so the file is 0.20 in taller than
    # the bbox reports (bar sec D5a item 2); and the band comes from whatever
    # deck placed it last, so read `_placements`, not the local call.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 4.32))

    axL.axhline(0.0, color=RED, lw=2.8, zorder=4)
    axL.plot(Ds, closed, "o", ms=13, color=AMBER, alpha=0.45, zorder=2)
    axL.plot(Ds, tr, ".", ms=6, color=TEAL, zorder=3)
    axL.set_xlim(0, 0.19)
    axL.set_ylim(-0.52, 0.10)

    axL.set_xlabel("dilution rate,  $D$   (h$^{-1}$)", fontsize=LBL)
    axL.set_ylabel("tr $J$   (h$^{-1}$)", fontsize=LBL)
    axL.grid(True, color=RULE, lw=0.6)
    # The low cluster is a SECOND interior fixed point, near prey
    # domination -- C_1 about 0.07 against a carrying capacity of 100 -- and
    # it is the first thing a sharp student asks about. Named in the title,
    # because in the panel the note covered the very points it names.
    # THE HELD-FIXED LINE IS NOT OPTIONAL HERE EITHER. This panel sweeps D
    # with every other parameter at the deposit's IPTG = 5 values, and it said
    # so nowhere -- the same defect `fig_pp_phase_plane`'s docstring argues
    # against two figures above. It is scoped to this panel, so it is this
    # panel's title and not the suptitle, which the right panel shares.
    axL.set_title("tr $J$ never reaches 0 — no Hopf\n"
                  "low cluster: a 2nd fixed point\n"
                  "all else: the deposit at IPTG = 5", fontsize=LBL,
                  color=RED, linespacing=1.25)


    # LOG-LOG IN MAGNITUDES, AND THAT IS A CORRECTION, NOT A STYLE CHOICE.
    # On the linear axes this panel used to carry, the cloud ran straight
    # into the corner where the two red zero lines met. The nearest of the
    # 4000 points sits at tr J = -0.00698 h^-1 against an axis range of 2.04,
    # which is 0.3 % of the panel -- 1.6 px at the deck's placement, and
    # still ambiguous at 400 dpi. A reader cannot be left unable to tell
    # whether the evidence touches zero.
    #
    # AND THE SLIDE'S FOOT NOW SENDS THEM HERE TO CHECK. It was rewritten on
    # 8 November to scope its margin claim to the LEFT panel -- "on the left
    # panel's sweep, not close: -0.10/h at the nearest D" -- precisely
    # because this panel's cloud does get close: -0.00698 h^-1 at its floor,
    # since tr J -> 0 as an interior fixed point runs out of cells (the
    # nearest point has C_1 = 0.61 against C_m = 435). The proof of absence
    # is the SIGN and it is universal; the MARGIN is not, and the foot used
    # to claim otherwise by saying "not a near miss" unqualified. So the
    # floor of this cloud has to be readable rather than lost in a corner,
    # or the panel contradicts the only claim the foot still makes about it.
    #
    # NO LINEAR LIMIT CAN FIX IT: the gap is one part in 292 of the range, so
    # any limit that shows the gap throws most of the 4000 points off the
    # panel. A log axis shows it by construction -- zero is not on a log axis
    # -- and the floor of the cloud is then readable against a decade tick.
    # The identity is still the diagonal, and the sign, which |.| removes,
    # is stated in the title instead of being left to a pixel.
    a_tr, a_cl = np.abs(rtr), np.abs(rclosed)
    hi = 1.6 * max(a_tr.max(), a_cl.max())
    lo = 0.45 * min(a_tr.min(), a_cl.min())
    axR.plot([lo, hi], [lo, hi], color=MUTED, lw=1.8, ls="--", zorder=3)
    axR.plot(a_cl, a_tr, ".", ms=7, color=TEAL, alpha=0.6, zorder=5)
    axR.set_xscale("log")
    axR.set_yscale("log")
    axR.set_xlim(lo, hi)
    axR.set_ylim(lo, hi)
    # UNITS ON THIS PANEL TOO -- it carried none while its sibling carried
    # (h^-1), on a figure whose whole subject is the size and sign of a rate.
    # BUT NOT AS A LONGER Y LABEL. A y label is rotated, so its length is
    # VERTICAL RUN: "|tr J|  (h^-1)" needs about 1.6 in of it, and at every
    # canvas height that keeps this figure inside the 4.40 in band the axes
    # are about 1.0 in tall, so the label overflowed its own axes and printed
    # through the LEFT panel's title. Measured: the overlap clears only once
    # the axes pass about 1.45 in, which costs a 4.55 in file. So the unit
    # goes on the x label, which is horizontal and where length is free, and
    # on the title, which says both axes carry it.
    axR.set_xlabel("|the closed form|   (h$^{-1}$)", fontsize=LBL)
    axR.set_ylabel("|tr $J$|", fontsize=LBL)
    axR.grid(True, which="major", color=RULE, lw=0.6)
    # This panel is an IDENTITY check -- computed trace against closed form
    # -- so its title says that. The count is of INTERIOR FIXED POINTS, which
    # is what the loop appends and what NUMBERS.md sec 20.3 marks: one
    # parameter set can contribute two, so the same number read as a count of
    # random parameter SETS overstates the draws.
    axR.set_title("over 4000 random interior fixed\n"
                  "points, all negative;  axes h$^{-1}$",
                  fontsize=LBL, color=INK, linespacing=1.25)

    # "the eigenvalues of J" was wrong and it was wrong in the one place it
    # costs the most: teal is float(np.trace(pp_jacobian(...))), the TRACE.
    # The move's entire argument is that the trace is the thing that cannot
    # reach zero and the eigenvalues are what it controls, so naming one as
    # the other in the key undoes the distinction the slide is making.
    fig.suptitle("BIOMD0000000296 — the deposit, not the paper's text\n"
                 "signals at QSS:  tr $J=-(k_{c1}C_1+k_{c2}C_2)/C_m$ always\n"
                 "amber: the closed form · teal: tr $J$ computed from the "
                 "Jacobian",
                 fontsize=LBL, color=INK, linespacing=1.25)
    _save(fig, name)


def fig_hopf_D(name="s24_hopf_D"):
    """Put the signals back and the leading real part crosses zero. Twice.

    MOVE 4, step 8. The same coexistence point, in the four-state deposited
    model: `pp_leading_real_part` across dilution rate, with both crossings
    located by `pp_hopf_D` rather than read off the curve. Between them the
    focus is unstable and the community oscillates; outside them it spirals
    in; a little above the upper crossing coexistence is lost altogether.

    THE OSCILLATION WAS IN THE LAG BETWEEN A POPULATION AND ITS OWN SIGNAL.
    That is session 11's result and T30's, arriving in a new substrate: what
    makes a loop oscillate is the delay around it. Name it -- a Hopf.

    WHAT A STUDENT CONCLUDES: restoring the two signal equations restores the
    instability the QSSA deleted, and the dilution rate is the knob that
    crosses it after the strains are built.

    MODEL: the deposited four-state model.
    """
    q0 = pp_params()
    crossings = pp_hopf_D(q0, which="all", grid=201)
    lo, hi = float(crossings[0]), float(crossings[-1])
    for got, want in zip((lo, hi), PINNED_HOPF):
        if abs(got - want) > 1e-5:
            raise AssertionError(
                f"the Hopf crossings moved: got {lo:.7f} and {hi:.7f}, "
                f"pinned at {PINNED_HOPF}. The figure, the tests and "
                f"NUMBERS.md sec 20.4 have to agree before this is drawn.")

    Ds = np.linspace(0.002, 0.185, 240)
    re = np.array([pp_leading_real_part(pp_params(D=D)) for D in Ds])
    ok = np.isfinite(re)

    qh = pp_params(D=hi)
    ev = np.linalg.eigvals(pp_jacobian(pp_steady_states(qh)["coexistence"][0],
                                       qh))
    lead = ev[int(np.argmax(ev.real))]
    period = 2.0 * np.pi / abs(lead.imag)

    # Where coexistence is lost. The deposit has one interior state to
    # D = 0.1750, three across a narrow fold at 0.1755-0.1760 and none from
    # 0.1765, so `pp_leading_real_part` goes non-finite and the curve simply
    # stops -- which says nothing unless the figure says it.
    lost = float(max(Ds[ok]))
    # WHERE COEXISTENCE IS LOST, PRINTED ON THE FIGURE THAT FIRST DRAWS IT.
    # The dotted line was marked "coexistence lost" with no value, and the
    # number reached the room only two moves later, on slides 69 and 71.
    #
    # `lost` above is the largest D of a 240-point sweep -- 0.1758, a grid
    # artefact rather than the boundary -- so the boundary is located on its
    # own fine scan at the resolution the fold needs (sec 20.4: the deposit
    # has one interior state to 0.1750, three across a narrow fold at
    # 0.1755-0.1762, and none from 0.1765). PRINTED TO THREE DIGITS, because
    # NUMBERS.md records a BAND, 0.1762-0.1765, and a fourth digit would
    # claim a resolution the fold does not allow. Three digits is also what
    # slides 69 and 71 carry, so the move no longer disagrees with itself.
    edge = np.arange(0.1740, 0.1780, 0.0002)
    alive = [float(D) for D in edge
             if len(pp_steady_states(pp_params(D=D), grid=40001)
                    ["coexistence"])]
    lost_D = max(alive)
    if not 0.1762 <= lost_D <= 0.1765:
        raise AssertionError(
            f"the coexistence boundary moved: the last D with an interior "
            f"fixed point is {lost_D:.4f}, outside NUMBERS.md sec 20.4's "
            f"0.1762-0.1765. The figure, the deck and that section have to "
            f"agree before this is drawn.")
    # THE TWO Y LIMITS ARE NAMED, because three places used them and a
    # fourth quantity -- the band label's y -- was written as a bare -0.046
    # that only made sense against one of them.
    #
    # Y_HI WAS 0.085 AND THAT WAS TOO LOW. `figure_fit` reported, before any
    # of this round's edits, that "Hopf, D = 0.1674 (73.65 h)" sat on 240 px
    # of the leading-Re curve: measured, the label's plate bottom fell at
    # 0.03014 while the curve reaches 0.03599 inside the plate's own x
    # window, so it bleached the CREST -- the feature the slide exists to
    # show. The axes is only 1.01 in tall here (a three-line suptitle and a
    # secondary axis on a figure capped at 4.14 in by session 25's re-use),
    # so there is no room to raise the label; the headroom has to come from
    # the limit.
    #
    # AND RAISING IT ALONE CREATES THE NEXT DEFECT -- gauntlet sec 5.5b. The
    # band label sits at a fixed DATA y, so opening the top of the axes slid
    # the curve down onto it: 472 px of the same collision, one label along.
    # Its y is therefore a FRACTION of the range and moves with it.
    Y_LO, Y_HI = -0.075, 0.095
    BAND_LABEL_F = 0.14          # of the range, measured clean at this Y_HI
    fig, ax = plt.subplots(figsize=(10.0, 4.31))
    ax.fill_between([lo, hi], Y_LO, Y_HI, color=AMBER, alpha=0.16,
                    zorder=1)
    ax.plot([lost] * 2, [Y_LO, 0.02], color=MUTED, lw=2.2, ls=":",
            zorder=3)
    ax.axhline(0.0, color=RED, lw=2.6, zorder=3)
    ax.plot(Ds[ok], re[ok], color=TEAL, lw=3.4, zorder=4)
    ax.plot([lo, hi], [0.0, 0.0], "o", ms=13, color=AMBER, zorder=6)

    ax.set_xlim(0, 0.19)
    ax.set_ylim(Y_LO, Y_HI)
    ax.grid(True, color=RULE, lw=0.6)
    # BOTH LABELS OUTSIDE THE BAND. Inside it, their plates punched holes in
    # the only feature marking the unstable window -- one of them erasing the
    # band's own right boundary for 260 px, so the band appeared to end at
    # the label rather than at the Hopf.
    _point(ax, (lo, 0.0), f"Hopf, $D$ = {lo:.4f}", AMBER, (0.02, 0.95),
           va="top")
    _point(ax, (hi, 0.0), f"Hopf, $D$ = {hi:.4f} ({period:.2f} h)", AMBER,
           (0.99, 0.95), ha="right", va="top")
    # On a second axis, where a tick is frame: in the plot this label had
    # only the bottom-right corner to sit in, which is also the only corner
    # the upper Hopf label and the band label can use.
    sec = ax.secondary_xaxis("top")
    sec.set_xticks([lost])
    # TWO LINES, growing upward and away from the picture. On one line the
    # label runs about 30 characters centerd at D = 0.176, which is 0.93 of
    # the way across the axes, so it overhangs the right edge and the figure's
    # own tight bbox grows with it -- bar sec D5d item 5, width binds.
    sec.set_xticklabels([f"coexistence lost\n$D$ ≈ {lost_D:.3f}"])
    ax.text(lo + 0.45 * (hi - lo), Y_LO + BAND_LABEL_F * (Y_HI - Y_LO),
            "unstable: it oscillates",
            ha="center", va="bottom", color=AMBER, fontsize=LBL, zorder=7)

    ax.set_xlabel("dilution rate,  $D$   (h$^{-1}$)", fontsize=LBL)
    ax.set_ylabel("leading Re $\\lambda$   (h$^{-1}$)", fontsize=LBL)
    # IPTG is not an optional detail: sec 20.2 makes it THE experimental
    # knob, setting d_1 and k_A2 through the two assignment rules, so "at
    # which IPTG" is load-bearing for every number on this figure.
    fig.suptitle("the deposited FOUR-state model, BIOMD0000000296\n"
                 f"IPTG={PP_IPTG:g}, so $d_1$={q0['d1']:g}, "
                 f"$k_{{A2}}$={q0['kA2']:g};  $k_{{c1}}$={q0['kc1']:g}, "
                 f"$k_{{c2}}$={q0['kc2']:g}, $d_2$={q0['d2']:g} h$^{{-1}}$\n"
                 f"$C_m$={q0['Cm']:g}, $K_1$=$K_2$={q0['K1']:g}, "
                 f"$k_{{A1}}$={q0['kA1']:g}, $d_{{AA1}}$={q0['dAA1']:g}, "
                 f"$d_{{AA2}}$={q0['dAA2']:g}",
                 fontsize=LBL, color=INK, linespacing=1.25)
    _save(fig, name)


# The five dilution rates the authors actually ran, and the regime their TEXT
# states at each. MEASURED, NUMBERS.md sec 20.5, stated in sec 2.4 and 3.4.
# THESE ARE THE AUTHORS' WORDS, NOT COORDINATES READ OFF A PANEL -- no point
# of theirs is redrawn anywhere in this module.
BAL_D = (0.11, 0.15, 0.20, 0.23, 0.31)
BAL_OBSERVED = (1, 1, 2, 2, 0)
# ONE LINE EACH. Two-line tick labels on rows 70 px apart overlap, and tick
# labels are frame, so figure_fit never sees it happen.
REGIME = ("no coexistence", "steady coexistence", "damped oscillation",
          "sustained oscillation")


def _model_regime(D):
    """Where the deposited model sits at this dilution rate. Returns 0-3."""
    q = pp_params(D=D)
    co = pp_steady_states(q)["coexistence"]
    if not len(co):
        return 0
    best = None
    for st in co:
        ev = np.linalg.eigvals(pp_jacobian(st, q))
        lead = ev[int(np.argmax(ev.real))]
        if best is None or lead.real > best.real:
            best = lead
    if best.real > 0.0:
        return 3
    return 2 if abs(best.imag) > 1e-9 else 1


def fig_model_vs_experiment(name="s24_model_vs_experiment"):
    """Faithfully the paper's model, and wrong against the paper's experiment.

    THE SHARPEST THING IN THE SESSION. The deposited model reproduces the
    paper's OWN Fig. 3C to three digits, so nothing here is a transcription
    error -- and it still disagrees with their experiment at four of the five
    dilution rates they ran, IN OPPOSITE DIRECTIONS. That is what the crossing
    is: where the experiment is steady the model oscillates, and where the
    experiment oscillates the model has already lost coexistence. The one
    agreement is washout at D = 0.31.

    The model's row is computed here by `pp_steady_states` and `pp_jacobian`;
    the experiment's row is the regime the authors state in their own text at
    each D. No panel is digitized.

    So the authors' own phrase is carrying all of it: the model "qualitatively
    accounts for" the observations. A chemostat model of two engineered strains
    gets the SHAPE right and the NUMBERS wrong, which is the honest standing of
    most models in this course.

    WHAT A STUDENT CONCLUDES: a model can be transcribed correctly, reproduce
    its own paper's figure, and still be wrong about the experiment -- and the
    direction of the error is information.

    MODEL: the deposited four-state model.
    """
    model = [_model_regime(D) for D in BAL_D]
    fig, ax = plt.subplots(figsize=(10.0, 4.29))

    for D, m, o in zip(BAL_D, model, BAL_OBSERVED):
        if m == o:
            continue
        ax.annotate("", xy=(D, m), xytext=(D, o), zorder=3,
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.6,
                                    shrinkA=14, shrinkB=14))
    # MARKERS, NOT LINES, and that is a correction rather than a style
    # choice. The y axis is four CATEGORIES at integer positions: joining
    # them ran the experiment's trace through "steady coexistence" at
    # D = 0.27, which nobody ran, and it manufactured a crossing that exists
    # only because "no coexistence" was placed below "steady". Reorder the
    # categories on any other defensible principle and the crossing goes.
    # What carries the opposite-directions structure is the ARROWS, which are
    # four real comparisons at four real dilution rates.
    ax.plot(BAL_D, BAL_OBSERVED, "o", color=TEAL, ms=15, zorder=5)
    # Offset at D = 0.31 so the one agreement does not read as model-only.
    ax.plot([D + (0.004 if D == 0.31 else 0.0) for D in BAL_D], model, "s",
            color=AMBER, ms=13, zorder=5)

    ax.set_xlim(0.085, 0.345)
    ax.set_ylim(-1.2, 4.3)
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(REGIME)
    ax.set_xticks(list(BAL_D))
    ax.set_xticklabels([f"{D:.2f}" for D in BAL_D])
    ax.grid(True, axis="x", color=RULE, lw=0.7)

    # THE DIRECTION OF THE DISAGREEMENT IS DRAWN, NOT WRITTEN: the two traces
    # cross, and the red arrows point up on the left and down on the right.
    # Two sentences saying so as well did not fit -- measured, they left 61 px
    # of clear lane for 44 px of text twice over -- so the sentence that names
    # the structure is in the suptitle, which has the full figure width, and
    # the axes carry only the three labels that say which trace is which.
    # Each label in the empty band on the far side of its own trace: above
    # the model's level, below the experiment's, and below the shared
    # endpoint. "what they saw" placed ABOVE its line covered both red
    # disagreement arrows, which are patches and therefore invisible to the
    # gate -- the same silent-occlusion class as a label on a bar.
    # BOTH KEYS LIVE IN THE AXES' OUTER MARGINS, and the margins are what
    # the y limits are for: the rows sit at 0..3 and the limits run -1.2 to
    # 4.3. THE MARKERS ARE BIG IN DATA UNITS -- this axes is about 1.3 in
    # tall for 5.5 data units, so an ms=15 marker has a radius of 0.44 of a
    # ROW. A key at 3.3 therefore overlapped the squares on row 3, whose
    # tops reach 3.38, and "what they saw" centerd at 0.5 ran straight
    # through the circles on row 1, whose bottoms reach 0.56.
    #
    # So: above 3.44 and below -0.44, which is clear of every marker, and
    # which also keeps the convention this figure already had -- the model's
    # key above the model's level, the experiment's below the experiment's.
    ax.text(0.094, 3.62, "deposited model", color=AMBER, fontsize=LBL,
            ha="left", va="bottom", bbox=_plate(), zorder=7)
    # THE TWO KEYS ARE A KEY ROW ABOVE THE PLOT, not labels among the data,
    # and that is what stops this one being re-broken a third time.
    #
    # "what they saw" began at y = 0.3 with va="top", running 0.3 down to
    # about -0.05: it sat across the "no coexistence" row while the teal
    # marker it names is on "steady coexistence" one row up, so it read as
    # an annotation of the wrong row. Centring it in the lane at y = 0.5
    # then ran it through the row-1 circles, and dropping it into the bottom
    # margin ran it through the x axis spine -- three placements, three
    # collisions, which is gauntlet sec 5.5b telling you the placement is
    # not the problem.
    #
    # THE ARITHMETIC SAYS NO IN-AXES KEY CAN FIT. This axes is about 1.3 in
    # tall for 5.5 data units, so a 20 pt label is 1.19 data units high and
    # a marker's radius is 0.44 -- more than a ROW. The clear band below the
    # markers is 1.2 units and the label needs 1.19 of it starting below
    # -0.44, which does not exist. Bar sec D5d's method note: move it out of
    # the axes into frame. Both keys sit on one line above the data, in
    # their own colors, aligned with no row and over no marker.
    ax.text(0.340, 3.62, "what they saw", color=TEAL, fontsize=LBL,
            ha="right", va="bottom", bbox=_plate(), zorder=7)
    # 0.45 cleared the row-0 markers by 0.01 data units -- 2 px -- because a
    # marker's radius here is 0.44 of a row. 0.62 is the same margin the two
    # keys get.
    ax.text(0.336, 0.62, "both agree", color=GREEN, fontsize=LBL,
            ha="right", va="bottom", zorder=7)


    ax.set_xlabel("dilution rate  $D$   (h$^{-1}$)", fontsize=LBL)
    # THE TWO IPTG LEVELS ARE ON THE FIGURE, because without them this slide
    # compares a model at the deposit's IPTG = 5 (PP_IPTG, which `pp_params`
    # defaults to and `_model_regime` therefore uses) with an experiment the
    # authors ran at IPTG = 50 µM (NUMBERS.md sec 3.4: "All Fig. 3
    # experiments at IPTG = 50 µM", caption p.5, MEASURED) and says neither
    # number. The slide is not wrong -- it was undefended, on the sharpest
    # comparison in the session.
    #
    # RUN BOTH WAYS BEFORE PRINTING THIS. The regime classification is
    # IDENTICAL at IPTG = 50: sustained oscillation at D = 0.11 and 0.15,
    # leading Re lambda 0.0472 and 0.0364 against 0.0360 and 0.0228 at
    # IPTG = 5, and no coexistence state at 0.20, 0.23 or 0.31. IPTG moves
    # d_1 from 1.0000 to 1.4901 and k_A2 from 0.03500 to 0.04970 (sec 20.2's
    # two assignment rules, which is everywhere IPTG enters) and moves no
    # verdict. So the mismatch is not an IPTG mismatch, and the figure says
    # so instead of leaving the room to wonder.
    #
    # The line this replaces -- "and it reproduces the paper's own Fig. 3C to
    # three digits" -- is the deck's next slide in full, which its own
    # speaker note calls the door-closer on a transcription error. One line
    # is what the suptitle has spare at this canvas height; spending it on
    # the undefended comparison rather than on a claim the following slide
    # makes at length is the better trade. If it is wanted on this slide too
    # it belongs in the foot, which is the deck's to set.
    fig.suptitle(DEPOSIT + "\n"
                 "four disagreements out of five, in opposite directions "
                 "(red arrows)\n"
                 "model IPTG = 5, experiment IPTG = 50 µM (their Fig. 3): "
                 "same verdict",
                 fontsize=LBL, color=INK, linespacing=1.25)
    _save(fig, name)


# ===========================================================================
# MOVE 5 -- when a second strain is worth it
# ===========================================================================
def fig_dol(name="s24_dol"):
    """Splitting the job always helps growth and always costs capacity.

    MOVE 5's criterion, stated rather than derived. Left: the single cell
    carries both enzymes, so its burden is the SUM and its density collapses
    first; the split pair each carry one term and keep growing -- but they
    share one HALVED carrying capacity, so at zero burden division of labor
    starts a factor of two behind on yield and has to earn its way out.
    Right: where the crossing sits depends on the functional form assumed for
    burden.

    AND THAT SPREAD IS A CHOSEN EXAMPLE, NOT A PROPERTY OF THE FORM. Tsoi's
    own Fig. 2D caption says the parameters were chosen so that the Hill form
    reduces growth least and the linear form most; the three windows here are
    OUR example at this module's defaults, and they have exactly the same
    standing. What IS a fact about the functions is the ORDERING, because
    f_hill >= f_exp >= f_lin at every burden: Hill latest, linear earliest.

    WHAT A STUDENT CONCLUDES: the decision to split a pathway turns on a
    burden threshold, and that threshold is an assumption about burden rather
    than a measurement.

    BOTH AXES ARE THE TOTAL BURDEN B = B_1 + B_2, and the loop below passes
    b/2 to each of `dol_criterion`'s two PER-ENZYME arguments. The crossing
    printed on the left panel is therefore a TOTAL (2.27), and move 5's
    release and debrief quote PER-ENZYME borders (1.135146, 1.355143) --
    half the scale. Never read one against the other: the axis label carries
    B = B_1 + B_2 so the factor of two is visible on the figure. Tsoi write
    the same total beta*e_1 + gamma*e_2; this course writes B, because
    session 24 already spends beta on Basu's printed thresholds beta_L and
    beta_C (docs/symbols.md).

    MODEL: Tsoi 2018, equations (8)-(16), evaluated by `dol_criterion`.
    """
    B = np.linspace(0.0, 7.0, 561)
    forms = (("linear", GREEN), ("exponential", AMBER), ("hill", TEAL))
    res = {f: [dol_criterion(b / 2.0, b / 2.0, burden=f) for b in B]
           for f, _ in forms}

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.9, 4.42))

    sc = np.array([r["yield_sc"] for r in res["hill"]])
    dol = np.array([r["yield_dol"] for r in res["hill"]])
    cross = float(B[np.argmax(dol > sc)])
    axL.plot(B, sc, color=MUTED, lw=3.4, zorder=4)
    axL.plot(B, dol, color=TEAL, lw=3.4, zorder=4)
    # To the crossing and no further: a full-height rule ran up through the
    # label above it, which the gate reads as 97 px of occluded line.
    axL.plot([cross, cross], [0.0, 0.62], color=RED, lw=2.4, ls="--",
             zorder=3)
    axL.set_xlim(0, 7)
    axL.set_ylim(0, 1.05)
    axL.set_xlabel("total burden,  $B = B_1 + B_2$", fontsize=LBL)
    axL.set_ylabel("yield", fontsize=LBL)
    axL.grid(True, color=RULE, lw=0.6)
    # NO IN-AXES TEXT IN EITHER PANEL. At this figure height each panel is
    # about 230 px tall, so a two-line label is 43 % of the axes and there is
    # no region of a decaying pair of curves it does not reach into. Both
    # series are named in the title, which is frame.
    axL.set_title(f"Hill burden, crossing at $B$ = {cross:.2f}", fontsize=LBL,
                  color=INK)

    # THE BAR STOPS WHERE THE SINGLE CELL DIES, which is the only place a
    # comparison is still a comparison. `dol_favored` stays True above that
    # point only because 0 > 0 is False, so the previous bars ran to the
    # burden at which the SPLIT PAIR THEMSELVES go extinct -- 1.80, 4.61 and
    # 6.00 -- and 80-93 % of each bar was a region where there is nothing to
    # compare against. Tsoi keeps the two apart on purpose: sec 12.1 lists
    # "SC extinct, so DOL always wins" as a region distinct from "DOL
    # produces more P than SC". The open marker is where the pair dies too.
    ys = np.arange(len(forms))[::-1]
    for y, (f, col) in zip(ys, forms):
        fav = np.array([r["dol_favored"] for r in res[f]])
        alive = np.array([r["yield_sc"] > 0.0 for r in res[f]])
        live_fav = fav & alive
        if not live_fav.any():
            continue
        start = float(B[np.argmax(live_fav)])
        sc_dead = float(B[np.argmax(~alive)])
        pair_dead = float(B[np.argmax(
            np.array([r["yield_dol"] <= 0.0 for r in res[f]]))])
        axR.barh([y], [sc_dead - start], left=start, color=col, height=0.44,
                 alpha=0.9, zorder=3)
        axR.plot([pair_dead], [y], "o", ms=13, color=PAGE,
                 markeredgecolor=col, mew=2.6, zorder=5)
    axR.set_yticks(ys)
    axR.set_yticklabels(["linear", "exponential", "Hill"], fontsize=LBL)
    axR.set_xlim(0, 7)
    axR.set_ylim(-0.7, len(forms) - 0.3)
    axR.set_xlabel("total burden,  $B$", fontsize=LBL)
    axR.grid(True, axis="x", color=RULE, lw=0.6)
    axR.set_title("bar: splitting wins, both alive\n"
                  "○ : the pair dies too",
                  fontsize=LBL, color=MUTED, linespacing=1.25)

    # delta_me = 0 is the most load-bearing of these: it is Tsoi's eps = 0
    # regime, which collapses p_SC to exactly 1, so the reduced-per-cell
    # productivity half of the criterion is identically absent and the entire
    # cost of splitting is carried by rho_1 = rho_2 = rho/2.
    fig.suptitle("Tsoi 2018 eqs (8)–(16) — grey: one cell, teal: split "
                 "in two\n"
                 "our example: $\\mu_{max}$=1, $\\delta_\\upsilon$=0.1, "
                 "$\\rho_1$=$\\rho_2$=$\\rho$/2=0.5\n"
                 "$\\delta_{me}$=0 ($\\varepsilon_T$=0): the cost is the "
                 "halved capacity", fontsize=LBL, color=INK,
                 linespacing=1.25)
    _save(fig, name)


def _bind(fn, doc, **kw):
    f = functools.partial(fn, **kw)
    f.__name__ = fn.__name__ + "_" + "_".join(str(v) for v in kw.values())
    f.__doc__ = doc
    return f


FIGURES = [
    fig_sender_receiver,
    fig_diffusion_ledger,
    fig_lambda_scaling,
    *[_bind(fig_lambda_step, f"Move 2's derivation column, stage {k} of 2.",
            step=k) for k in (1, 2)],
    fig_xi_check,
    fig_band_response,
    fig_band_variants,
    *[_bind(fig_band_step, f"Move 3's derivation column, stage {k} of 3.",
            step=k) for k in (1, 2, 3)],
    *[_bind(fig_pp_step, f"Move 4's derivation column, stage {k} of 3.",
            step=k) for k in (1, 2, 3)],
    fig_pp_phase_plane,
    fig_qss_no_hopf,
    fig_hopf_D,
    fig_model_vs_experiment,
    fig_dol,
]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
