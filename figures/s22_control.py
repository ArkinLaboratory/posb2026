"""Session 22 figures — an integrator that does not need to know the disturbance.

ONE MODEL PER FIGURE, AND THE MODEL IS NAMED ON THE FIGURE. Session 21's
rebuild added that rule after a figure spliced two models; this session has the
same hazard in a different costume, because "ideal" (delta = 0) and "leaky"
(delta > 0) disagree about the one thing the hour claims.

Every curve comes out of `posb.control`, the same functions the students call.

AOKI'S DATA IS NOT REDRAWN HERE. We hold the paper's two p-values but not the
growth-rate points behind them, so Fig. 3d goes on a slide as a PAPER FIGURE
with its own attribution. Inventing points to redraw it would be exactly the
thing this course keeps telling students not to do.

What this session has to draw:

  * THE MOTIF. `fig_motif` -- Z1 carries the set point, Z2 senses the output,
    the two annihilate. Drawn, because the subtraction that makes it an
    integrator is visible in the picture.
  * THE CLAIM. `fig_plant_does_not_matter` -- the output against time for four
    different plants. They land on the same line. This is the figure the hour
    exists for.
  * THE HINGE. `fig_patch_vs_feedback` -- the three feedforward patches of
    rungs 1-3, each needing its own named disturbance and its own model,
    against one feedback loop that needs no list. It is the frame surface's
    whole argument, which was five rows of text before.
  * THE REJECTION. `fig_step` -- closed and open loop under the same step
    disturbance.
  * THE LIMIT. `fig_leak` -- SET-POINT error against the dilution rate, log
    on log, slope one.

Run:  python tools/build_figures.py s22
"""
import numpy as np

from matplotlib.lines import Line2D

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           RULE, TYPE)
from posb.control import (ControlParams, simulate, closed_loop_steady_state,
                          open_loop_steady_state, setpoint_error,
                          step_response)

plt = use()
OUT = "figures/build"
P = ControlParams()


# Every piece of text inside a figure is content and sits at the body floor;
# TYPE["caption"] inside a figure is for a literature citation and nothing
# else. The two-level hierarchy these diagrams need is emphasis (24) for a
# box's name and body (20) for its gloss -- NOT body and caption, which puts
# the gloss at 16 and, once image_centered scales the figure down to fit the
# band, at 14.7 on the wall. tools/figure_fit.py measures the product.
SUB = TYPE["body"]


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def fig_motif(banner=True, name="s22_motif"):
    """The antithetic motif, drawn as biology: two proteins, four reactions.

    `banner=False` renders the topology ALONE, for the frame surface that has
    to come before the room is asked to subtract the two rate equations. The
    banner version is the debrief, and it is the ONLY place X = mu/theta
    appears. The two rate equations appear in both, because they are what the
    room subtracts, not the answer.

    FOUR REACTIONS, each drawn as a reaction, each with its rate constant:

        SET POINT       nothing -> Z1              at a constant rate mu
        ACTUATION       Z1 drives the plant        at rate k
        SENSING         nothing -> Z2              at rate theta * X
        SEQUESTRATION   Z1 + Z2 -> SigW.RsiW       at rate eta

    WHY THE PRODUCT IS A COMPLEX AND NOT nothing. An earlier version of this
    figure drew Z1 + Z2 -> 0, which is what Aoki writes for abstract Z1 and
    Z2. Once the species are NAMED it stops being true: RsiW does not destroy
    SigW, it binds it into a 1:1 complex that goes on existing -- in B.
    subtilis that complex is resolved by regulated intramembrane proteolysis
    and SigW is released again. Aoki's own Fig. 1 caption hedges it the same
    way, "annihilate (or sequester) each other", and the body text for this
    pair says RsiW "stably sequesters and holds SigW inactive".

    What the integral actually needs is weaker than destruction: the two have
    to leave circulation TOGETHER, ONE FOR ONE. Then the eta term is
    identical in both rate laws and cancels on subtraction. Destruction does
    that; stoichiometric sequestration does that; reversible binding does
    not. The mathematics does not care which, and that is exactly why the
    motif is buildable in a cell. Session 22's sigma / anti-sigma slide picks
    this up to argue why sequestration counts as an annihilation; the phrase
    "one for one" is the hand-off, so it is the phrase on the figure.

    WHY THE TWO RATE EQUATIONS ARE ON THE FIGURE. Without them the banner is
    a result handed down: nothing shows where eta went. With them the
    cancellation is a subtraction the room performs, because the -eta Z1 Z2
    term is drawn in the same red as the junction that produces it, written
    identically, and aligned so the two instances sit one above the other.
    Linear algebra is the weak axis in this cohort, so an algebraic step that
    is SHOWN cancelling is worth more here than one that is asserted.

    WHY k IS ON THE ACTUATION ARROW. Because it then never reappears. Every
    other constant in the figure is in X = mu/theta; k is not, and neither is
    anything inside the plant. That absence is the robustness claim, and the
    speaker note should say so out loud.

    The plant is DRAWN unknown rather than described as unknown: unnamed
    nodes, two nodes that are a literal question mark, a repression bar
    alongside the activations so the topology is not all one sign.

    GEOMETRY. Lengths are in data units, roughly one inch each; placements
    were set from measured text extents, not estimated. If you change a
    string, re-measure -- the widths here have no slack.
    """
    fig, ax = plt.subplots(figsize=(10.28, 4.85))
    ax.set_xlim(0, 10.0); ax.set_ylim(0, 4.40); ax.axis("off")

    EM, BD = TYPE["emphasis"], SUB
    TINT_C = "#E9F2F2"     # controller fill: a teal so pale it reads as paper
    TINT_P = "#ECEFEE"     # plant fill: neutral grey, because you did not pick it
    SLATE = "#4A6663"      # the plant's lettering: NOT the controller's teal

    def arrow(x1, y1, x2, y2, colour, rad=0.0, lw=2.6, style="-|>"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=5,
                    arrowprops=dict(arrowstyle=style, color=colour, lw=lw,
                                    shrinkA=0, shrinkB=0,
                                    connectionstyle=f"arc3,rad={rad}"))

    # ---- the two circuits, named apart ---------------------------------
    # Different colour, different wording, different alignment, and only one
    # of them says "plant" -- because at the back of the room CONTROLLER and
    # CONTROLLED in the same ink at the same size are one word with a blurred
    # ending, which is the distinction this whole session turns on.
    CX0, CY0, CX1, CY1 = 0.04, 0.44, 5.70, 3.50
    PX0, PY0, PX1, PY1 = 7.70, 1.20, 9.96, 3.42
    for x0, y0, x1, y1, edge, fill in [(CX0, CY0, CX1, CY1, TEAL, TINT_C),
                                       (PX0, PY0, PX1, PY1, MUTED, TINT_P)]:
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, lw=2.4,
                                   edgecolor=edge, facecolor=fill, zorder=1))
    ax.text(CX0, 3.52, "CONTROLLER circuit", ha="left", va="bottom",
            color=TEAL, fontsize=EM)
    ax.text(PX1, 3.52, "CONTROLLED \u2014 the plant", ha="right",
            va="bottom", color=SLATE, fontsize=EM)

    # ---- the two controller proteins ------------------------------------
    ZX0, ZX1 = 2.40, 5.60
    Z1Y0, Z1Y1 = 2.46, 3.46
    Z2Y0, Z2Y1 = 0.50, 1.50
    y1 = (Z1Y0 + Z1Y1) / 2                      # 2.96
    y2 = (Z2Y0 + Z2Y1) / 2                      # 1.00
    for y0, yt, tag, gloss, colour in [
            (Z1Y0, Z1Y1, "$Z_1$ = SigW", "$\\sigma$ factor", TEAL),
            (Z2Y0, Z2Y1, "$Z_2$ = RsiW", "anti-$\\sigma$ factor", AMBER)]:
        ax.add_patch(plt.Rectangle((ZX0, y0), ZX1 - ZX0, yt - y0, lw=2.8,
                                   edgecolor=colour, facecolor="white",
                                   zorder=3))
        ax.text((ZX0 + ZX1) / 2, yt - 0.27, tag, ha="center", va="center",
                color=colour, fontsize=EM, zorder=4)
        ax.text((ZX0 + ZX1) / 2, y0 + 0.24, gloss, ha="center", va="center",
                color=INK, fontsize=BD, zorder=4)

    # ---- reaction 1.  nothing -> Z1, at a constant rate mu ---------------
    # Nothing upstream: that is what makes mu a SET POINT and not a signal.
    # The empty-set glyph is glossed here, the one place the figure uses it,
    # and the gloss sits DIRECTLY under the glyph. It used to sit below and
    # left of it with SET POINT in between, where it could be read as the
    # tail of that phrase rather than as the gloss.
    # Role above the arrow, rate below it -- the same way round as ACTUATOR
    # / rate k and SENSOR / rate theta X. This reaction had them inverted.
    ax.text(0.26, y1, "$\\varnothing$", ha="center", va="center", color=INK,
            fontsize=EM, zorder=4)
    ax.text(0.10, 2.64, "nothing", ha="left", va="top", color=INK,
            fontsize=BD, zorder=4)
    arrow(0.50, y1, ZX0, y1, TEAL)
    ax.text(2.35, y1 + 0.05, "SET POINT", ha="right", va="bottom", color=TEAL,
            fontsize=BD, zorder=4)
    ax.text(1.60, y1 - 0.06, "$\\mu$", ha="center", va="top", color=TEAL,
            fontsize=EM, zorder=4)

    # ---- reaction 2.  Z1 actuates, at rate k ----------------------------
    # k is here so that its ABSENCE downstream can be pointed at: it is the
    # one rate constant in the figure that does not survive into X = mu/theta.
    arrow(ZX1, y1, 7.95, y1, TEAL)
    ax.text(6.70, y1 + 0.04, "ACTUATOR", ha="center", va="bottom",
            color=TEAL, fontsize=BD, zorder=4)
    ax.text(6.70, y1 - 0.04, "rate $k$", ha="center", va="top", color=TEAL,
            fontsize=BD, zorder=4)

    # ---- reaction 3.  nothing -> Z2, at rate theta X --------------------
    # An elbow, not a diagonal: orthogonal runs keep the two labels off the
    # line. The headless legs are a Line2D, because a headless annotate
    # registers in figure_fit as a zero-length label spilling the plant box.
    # The leg turns down OUTSIDE the plant, not inside it: dropped at the
    # output node's own x it runs straight through the condition caption
    # under the box. Leaving by the plant's left edge and
    # turning in the gap keeps the caption tucked under its box.
    ax.plot([7.95, 7.50, 7.50, 6.40], [1.75, 1.75, y2, y2], color=AMBER,
            lw=2.6, solid_capstyle="butt", zorder=5)
    arrow(6.40, y2, ZX1, y2, AMBER)
    ax.text(6.70, y2 + 0.04, "SENSOR", ha="center", va="bottom", color=AMBER,
            fontsize=BD, zorder=4)
    ax.text(6.70, y2 - 0.04, "rate $\\theta X$", ha="center", va="top",
            color=AMBER, fontsize=BD, zorder=4)

    # ---- reaction 4.  Z1 + Z2 -> an inert complex, at rate eta ----------
    # Two arrows INTO one reaction node, one arrow out of it to a product
    # that is a DEAD END and is not an empty set: RsiW does not destroy
    # SigW, it holds it. And not a double-headed arrow either -- that is the
    # reversible-binding glyph, and reversible binding is the one case that
    # would break the cancellation, so the figure must not look like it.
    arrow(2.70, Z1Y0, 2.70, 2.07, RED)
    arrow(2.70, Z2Y1, 2.70, 1.89, RED)
    ax.add_patch(plt.Circle((2.70, 1.98), 0.075, color=RED, zorder=6))
    ax.plot([2.66, 2.00], [1.98, 1.98], color=RED, lw=2.6,
            solid_capstyle="butt", zorder=5)
    arrow(2.00, 1.98, 2.00, 1.48, RED)
    # eta belongs on its own reaction. It sits on the leg leaving the
    # junction, between the node and the turn down into the complex, in the
    # junction's red so it reads with the two red terms in the rate laws.
    # Above the leg rather than below it: below, a 24pt eta lands on the
    # complex box's top edge, and dropping it to 20pt would make it the only
    # rate constant in the figure set smaller than the rest.
    ax.text(2.25, 2.02, "$\\eta$", ha="center", va="bottom", color=RED,
            fontsize=EM, zorder=4)
    ax.add_patch(plt.Rectangle((0.20, 0.50), 2.10, 0.94, lw=2.6,
                               edgecolor=RED, facecolor="white", zorder=3))
    ax.text(1.25, 1.19, "SigW\u00b7RsiW", ha="center", va="center",
            color=RED, fontsize=BD, zorder=4)
    ax.text(1.25, 0.73, "sequestered", ha="center", va="center", color=INK,
            fontsize=BD, zorder=4)

    # ---- the cancellation, written out ----------------------------------
    # The point of the hour. Each rate law is two text objects, so the shared
    # term can be set in the junction's own red, written identically, and
    # left-aligned at the same x in both lines -- the room SEES the two
    # copies that cancel instead of being told that they do.
    SHARED = "$-\\eta Z_1Z_2$"
    for yy, va, hd in [(2.40, "top", "$\\dot{Z}_1 = \\mu$"),
                       (1.56, "bottom", "$\\dot{Z}_2 = \\theta X$")]:
        ax.text(4.20, yy, hd, ha="right", va=va, color=INK, fontsize=BD,
                zorder=4)
        ax.text(4.28, yy, SHARED, ha="left", va=va, color=RED, fontsize=BD,
                zorder=4)
    # The deck's own words, which the sigma / anti-sigma slide repeats.
    ax.text(CX0 + 0.06, 0.40, "they leave circulation one for one",
            ha="left", va="top", color=RED, fontsize=BD, zorder=4)

    # ---- the plant: drawn unknown, not described as unknown -------------
    # Two of the nodes ARE question marks, and one edge is a repression bar,
    # so the picture is not a single topology of a single sign.
    nin, nout = (7.95, y1), (7.95, 1.75)
    q1, nb, q2, nd = (8.80, 3.05), (9.70, 3.05), (9.45, 2.45), (8.20, 2.45)
    for p0, p1, st in [(nin, q1, "-|>"), (q1, nb, "-|>"), (nb, q2, "-|>"),
                       (q2, nd, "-|>"), (nd, nout, "-|>")]:
        arrow(p0[0], p0[1], p1[0], p1[1], MUTED, rad=0.12, lw=2.0, style=st)
    arrow(q1[0], q1[1], nd[0], nd[1], MUTED, rad=-0.2, lw=2.0,
          style="-[, widthB=0.42, lengthB=0.0")
    for nx, ny in [nb, nd, nin]:
        ax.add_patch(plt.Circle((nx, ny), 0.10, color=MUTED, zorder=6))
    for nx, ny in [q1, q2]:
        ax.add_patch(plt.Circle((nx, ny), 0.26, facecolor="white",
                                edgecolor=MUTED, lw=2.2, zorder=6))
        ax.text(nx, ny, "?", ha="center", va="center", color=INK,
                fontsize=BD, zorder=7)
    ax.add_patch(plt.Circle(nout, 0.13, color=INK, zorder=6))
    ax.text(8.15, 1.75, "output $X$\n= sfGFP", ha="left", va="center",
            color=INK, fontsize=BD, linespacing=1.15, zorder=7)
    # THE CONDITION, NOT A BOAST. This said "any topology, any parameters",
    # which is false as an unconditional statement: a plant whose output the
    # actuator cannot move has no integral action to speak of, however many
    # unknown nodes are drawn in it. The caption now names the condition the
    # picture already satisfies -- five activating arrows run from the
    # actuation node at (7.95, y1) through q1, nb, q2 and nd to the output
    # node at (7.95, 1.75), and the sensor leg leaves FROM that same output
    # node. So the drawn plant is one Z1 can move and Z2 can see, which is
    # exactly what the result needs. Two lines, not three: the band on the
    # debrief slide is 4.60in against a 4.43in PNG, and a third caption line
    # takes the placement scale under 1.0 and 20 pt under the floor.
    ax.text(8.78, PY0 - 0.08, "any topology,\nif $Z_1$ can move $X$",
            ha="center", va="top", color=SLATE, fontsize=BD,
            linespacing=1.15, zorder=4)

    # ---- the banner: its own band, nothing else in it -------------------
    if banner:
        ax.text(5.00, 4.24,
                "$d(Z_1 - Z_2)/dt = \\mu - \\theta X$"
                # "no k, no gamma, no d", NOT "no k". k is not the only
                # thing absent from mu/theta and naming it alone invites the
                # reading that gamma or d might still be in there -- which
                # is exactly the push-back the release slide expects ("k and
                # gamma must do something"). All three are named because all
                # three are gone.
                "   $\\Rightarrow$   steady state  $X = \\mu/\\theta$"
                # AND THE SHORT FORM OF IT, measured rather than chosen.
                # "no k, no gamma, no d" is twelve characters wider than
                # "no k" was, and the banner already runs most of the axes'
                # width: tight_layout answers a wider banner by shrinking
                # the axes, which pulls every label on the figure together
                # in data units, and "any topology, if Z1 can move X" then
                # landed on 'SENSOR' and on a drawn arrow. Clean in the
                # container, two problems on the instructor's machine.
                " — no $k$, $\\gamma$ or $d$",
                ha="center", va="center", color=INK, fontsize=BD)

    _save(fig, name)


def fig_block_diagram():
    """The standard control loop, with the summing junction that forms the error.

    Astrom & Murray draw the junction before anything else (Feedback Systems
    2e, Fig. 6.13), because forming the error is what makes a thing a
    controller. The figure this replaces had no junction at all, so
    `e = mu/theta - X` floated beside it as a caption and the error was never
    linked to the plant -- notes 5, 6 and 7-10 of the 7 November review are
    all that one omission.

    Left to right: the set point r enters, the measured output is subtracted
    at the first junction, and the difference LEAVES as the controller's
    input e. The controller emits u, the plant takes u, the disturbance d
    enters at a second junction after the plant, and the output X leaves and
    is tapped back through the sensor into the minus input of the junction.

    FIVE SYMBOLS, NO MORE: r, e, u, d, X, each on its arrow and each defined
    in the key under the loop, in signal order, so the room can be walked
    along it one signal at a time. The set point is r here and NOT mu/theta.
    This is the orientation figure; mu, theta, Z1 and Z2 belong to the motif
    figure, where "the set point is mu/theta, fixed by the controller and not
    by the plant" arrives as a derived result instead of being asserted as a
    label on the first arrow the room meets. The two circuits are still named
    apart in the captions above the boxes, which is what this figure is for.

    The sensor is unity gain and says so, so the error the key writes,
    e = r - X, is the error the picture forms. A sensor of any other gain
    would need its own symbol on the return arrow and a different expression
    in the key.

    THE SLIDE IS TITLED "The words this hour is made of" AND IT OWES THE ROOM
    FIVE: plant, actuator, set point, error, and open versus closed. All five
    are IN the figure -- plant and actuator as labels on the box and the arrow
    that are those things, set point and error on the first two arrows and in
    the key, and open-versus-closed as a break mark on the return path with
    the consequence written beside it. Putting any of them in the speaker
    note instead is the move deck-bar C4 and D4 exist to stop: an argument
    that can be made graphically is made graphically.
    """
    # ONE AXIS UNIT IS ONE INCH, and that is the whole reason this function
    # pins the axes itself. Left to tight_layout, an axes whose labels reach
    # past its own limits is shrunk to contain them, which makes those labels
    # wider in data units, which shrinks it again: the first draft of this
    # rebuild settled at 0.50 in per unit, so every gap computed in units was
    # half what it looked like and sixteen labels landed at 18.8 pt. An axes
    # locator re-pins the axes to the whole figure on every draw -- it is
    # applied after tight_layout has written its position, so it wins -- and
    # a gap of 0.07 units below is then 0.07 in, which is 11 px on the slide.
    # tight_layout answers that it cannot lay such an axes out, which is the
    # point, so that one warning is silenced.
    #
    # Sizes the arithmetic below uses, measured off this font at this dpi: a
    # 20 pt line is 0.333 in tall and about 0.13 in per character, a 24 pt
    # line is 0.41 in tall. figure_fit wants 10 px (0.0625 in) between any
    # two text boxes, so no gap here is under 0.07 and every string was
    # measured before it was placed.
    #
    # Saved: 10.2 x 4.58 in, the 0.1 in savefig pad included. Inside the
    # 10.2 x 4.60 band and width-limited, so image_centered places it at
    # 1.000 and 20 pt stays 20 pt on the wall.
    #
    # Both imports are local, to keep this rebuild inside the one function
    # it was asked to touch.
    import warnings
    from matplotlib.transforms import Bbox

    warnings.filterwarnings(
        "ignore", message="This figure includes Axes that are not compatible")
    fig, ax = plt.subplots(figsize=(10.0, 4.38))
    ax.set_axes_locator(lambda ax_, renderer: Bbox.from_bounds(0, 0, 1, 1))
    ax.set_xlim(0, 10.0); ax.set_ylim(0, 4.38); ax.axis("off")

    Y   = 3.432     # the forward signal line
    BH  = 1.00      # block height
    RJ  = 0.306     # junction radius: ms=44 pt is 0.611 in across
    CAP = 4.00      # block captions sit above the blocks, as in Fig. 6.13
    FB  = 2.44      # the feedback line

    def box(x0, x1, name, gloss, colour):
        ax.add_patch(plt.Rectangle((x0, Y - BH / 2), x1 - x0, BH, fill=False,
                                   lw=2.2, edgecolor=colour, zorder=3))
        # Name at emphasis, gloss at the body floor, centres 0.47 in apart so
        # the two text boxes keep 0.098 in -- 16 px -- between them.
        ax.text((x0 + x1) / 2, Y + 0.235, name, ha="center", va="center",
                color=colour, fontsize=TYPE["emphasis"], zorder=4)
        ax.text((x0 + x1) / 2, Y - 0.235, gloss, ha="center", va="center",
                color=colour, fontsize=SUB, zorder=4)

    def caption(xc, text, colour):
        ax.text(xc, CAP, text, ha="center", va="bottom", color=colour,
                fontsize=SUB, zorder=4)

    def junction(xc, colour):
        # A marker, not a Circle patch: markers are sized in points, so this
        # stays round whatever the axes aspect turns out to be.
        ax.plot([xc], [Y], marker="o", ms=44, mfc="none", mec=colour,
                mew=2.2, zorder=3)
        ax.text(xc, Y, "$\\Sigma$", ha="center", va="center", color=colour,
                fontsize=TYPE["emphasis"], zorder=4)

    def arrow(x1, y1, x2, y2, colour):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.2))

    def wire(x1, y1, x2, y2, colour):
        ax.plot([x1, x2], [y1, y2], color=colour, lw=2.2,
                solid_capstyle="projecting", zorder=2)

    def on_line(xc, text, colour):
        ax.text(xc, Y + 0.08, text, ha="center", va="bottom", color=colour,
                fontsize=TYPE["emphasis"], zorder=4)

    # --- the error is formed first, and the picture shows where -----------
    XS = 1.35
    arrow(0.10, Y, XS - RJ, Y, TEAL)
    on_line(0.57, "$r$", TEAL)
    junction(XS, TEAL)
    caption(1.31, "the error is formed", TEAL)
    ax.text(XS - 0.34, Y + 0.27, "$+$", ha="center", va="center", color=TEAL,
            fontsize=TYPE["emphasis"], zorder=4)
    # Beside the return arrow's shaft, just under the rim, so it reads as the
    # sign on THAT input. It cannot sit higher: the Sigma glyph's own text box
    # runs 0.20 down and 0.11 across from the centre -- far wider than the
    # painted glyph -- so anything nearer than 0.47 below centre lands inside
    # figure_fit's 10 px gap, wherever it is put around the rim.
    ax.text(XS + 0.20, Y - 0.49, "$-$", ha="center", va="center", color=AMBER,
            fontsize=TYPE["emphasis"], zorder=4)

    # --- the controller: the circuit you build ----------------------------
    arrow(XS + RJ, Y, 3.10, Y, TEAL)
    on_line(2.38, "$e$", TEAL)
    # "antithetic motif" used to sit in this box: the same sequencing error
    # as mu/theta on the first arrow, naming the motif a figure before the
    # motif figure. The box says what the thing does where the student meets
    # it.
    box(3.10, 5.10, "controller", "you build this", TEAL)
    caption(4.14, "the controller circuit", TEAL)

    # --- the plant: the circuit being controlled --------------------------
    arrow(5.10, Y, 6.60, Y, TEAL)
    on_line(5.85, "$u$", TEAL)
    # THE ACTUATOR, named on the element that is one: the arrow that carries
    # the controller's decision into the plant. The gap between the two boxes
    # was widened from 1.05 to 1.50 in to hold the word clear of both; at
    # 0.13 in of air it read as a third box gloss that had lost its box.
    ax.text(5.85, Y - 0.09, "actuator", ha="center", va="top", color=TEAL,
            fontsize=SUB, zorder=4)
    # "any topology" was the overclaim's first appearance in the deck, on the
    # orientation figure, before anything had been derived. What the room is
    # owed here is the word's MEANING, and the plant's status is that you did
    # not pick it and do not know it -- not that every topology is covered.
    # The condition itself is drawn on this figure already: the actuator
    # arrow goes in, the output arrow comes out and is tapped back through
    # the sensor. The box is 304 px of rendered width and figure_fit measures
    # the ink: "unknown to you" came out 334 and spilled by 30, "any topology"
    # fitted with 8 px a side, which is inside the margin macOS metrics eat.
    # One word, 167 px, 68 px of air on each side.
    box(6.60, 8.50, "plant", "unknown", INK)
    caption(7.55, "the controlled circuit", INK)

    # --- the disturbance enters after the plant, at its own junction -------
    XD = 9.20
    arrow(8.50, Y, XD - RJ, Y, INK)
    junction(XD, INK)
    arrow(XD, 4.20, XD, Y + RJ, RED)
    # Beside the arrow, as in Fig. 6.13, and 0.18 in clear of the top edge:
    # at 4.08 against an arrow starting at 4.33 the pair read as jammed into
    # the corner.
    ax.text(XD + 0.08, 4.00, "$d$", ha="left", va="center", color=RED,
            fontsize=TYPE["emphasis"], zorder=4)

    # --- the output, and the tap that closes the loop ----------------------
    arrow(XD + RJ, Y, 9.95, Y, INK)
    on_line(9.78, "$X$", INK)
    wire(9.78, Y, 9.78, FB, AMBER)
    arrow(9.78, FB, 6.65, FB, AMBER)
    # UNITY GAIN, and it says so. The key writes the error as e = r - X, so
    # the thing coming back has to BE X; a sensor of any other gain would
    # need its own symbol here and a different expression in the key. The
    # box is 2.40 wide because the label is 2.14 at emphasis.
    ax.add_patch(plt.Rectangle((4.25, FB - 0.30), 2.40, 0.60, fill=False,
                               lw=2.2, edgecolor=AMBER, zorder=3))
    ax.text(5.45, FB, "sensor, gain 1", ha="center", va="center", color=AMBER,
            fontsize=TYPE["emphasis"], zorder=4)
    # OPEN VERSUS CLOSED. The loop is closed because this path exists, so
    # the break mark goes ON it and the consequence beside it. A gap painted
    # in the ground colour, then two strokes across it: the standard break
    # symbol, and the only one that reads at the back of the room.
    YC = 2.90
    ax.plot([9.78, 9.78], [YC - 0.07, YC + 0.07], color=ax.get_facecolor(),
            lw=5.0, zorder=4, solid_capstyle="butt")
    for dy in (0.0, 0.08):
        ax.plot([9.70, 9.86], [YC - 0.09 + dy, YC + 0.01 + dy], color=INK,
                lw=2.0, zorder=5, solid_capstyle="round")
    # 0.10 in clear of the plant box above, 0.14 in clear of the mark, and
    # it keeps off the drop wire at 9.78.
    ax.text(8.35, FB + 0.06, "cut this: open loop", ha="center", va="bottom",
            color=AMBER, fontsize=SUB, zorder=4)
    wire(4.25, FB, XS, FB, AMBER)
    arrow(XS, FB, XS, Y - RJ, AMBER)
    ax.text(2.05, FB + 0.07, "$X$", ha="center", va="bottom",
            color=AMBER, fontsize=TYPE["emphasis"], zorder=4)
    # The other half of the word pair. The return path is what CLOSES the
    # loop, so the path is labelled closed where it runs clear, and the break
    # mark upstream says what cutting it costs. Both words the slide owes the
    # room are on the wire that decides which one applies.
    ax.text(3.35, FB + 0.06, "closed loop", ha="center", va="bottom",
            color=AMBER, fontsize=SUB, zorder=4)

    # --- the key: every symbol on the loop, in signal order ----------------
    ax.plot([0.08, 9.90], [2.07, 2.07], color=RULE, lw=1.4, zorder=1)
    key = [("$r$", TEAL,
            "set point \u2014 the value $X$ should settle to"),
           ("$e = r - X$", TEAL,
            "error \u2014 set point minus measured output"),
           ("$u$", TEAL,
            "the actuator \u2014 what the controller pushes the plant with"),
           ("$d$", RED,
            "disturbance \u2014 an unmeasured push on the output"),
           ("$X$", INK,
            "output \u2014 the quantity being controlled")]
    for i, (sym, colour, gloss) in enumerate(key):
        y = 2.00 - 0.41 * i
        ax.text(0.08, y, sym, ha="left", va="top", color=colour,
                fontsize=SUB, zorder=4)
        ax.text(1.40, y, gloss, ha="left", va="top", color=INK,
                fontsize=SUB, zorder=4)

    _save(fig, "s22_block_diagram")


HELD = "$\\mu=10,\\ \\theta=2,\\ k=1,\\ \\gamma=0.5,\\ \\eta=50$"

# THE SAME RUN, WRITTEN FOR THE SURFACES THAT COME BEFORE THE MOTIF EXISTS.
# mu and theta are the antithetic motif's own two rate constants and they are
# not produced until its two rate laws are subtracted, twelve slides after the
# step and plant-sweep figures go up. Those runs quote the SET POINT instead,
# which is the only thing about mu and theta they use: r = mu/theta = 10/2 = 5,
# so nothing about the runs changes and no symbol arrives without an origin.
# eta is out for the same reason one symbol over -- the plant run's last click
# introduces it by name with both its values and defines it in the foot.
HELD_R = "$r=5,\\ \\ k=1,\\ \\ \\gamma=0.5$"


# THE RUN, newest change last. OWNERSHIP IS IN THE LABEL and it is not
# decoration: k and gamma are the PLANT's constants, eta is the CONTROLLER's.
# Aoki's claim is about "the topology and parameters of the circuit of
# interest", so a figure that files eta under "a different plant" is quietly
# making a second and different claim. Both claims are true -- neither
# constant reaches mu/theta -- and the labels now say which is which, because
# the deck's own design ledger already does ("k and gamma belong to the
# plant. eta belongs to the protein pair you picked").
#
# The fifth field is the short form the later stages carry in their muted
# history line. The long form is only ever shown for the LIVE change.
PLANT_RUNS = [
    ("the reference plant",
     P, TEAL, "-", None),
    ("plant gain  $k$:  $1 \\to 4$",
     ControlParams(k=4.0), CYAN, "--", "$k$: $1\\to4$"),
    ("plant removal  $\\gamma$:  $0.5 \\to 0.1$",
     ControlParams(gamma=0.1), AMBER, "-.", "$\\gamma$: $0.5\\to0.1$"),
    ("controller rate constant  $\\eta$:  $50 \\to 500$",
     ControlParams(eta=500.0), RED, ":", "$\\eta$: $50\\to500$"),
]


def _plant_panel(stage, name):
    """One moment of the four-run build: `stage` circuits drawn, newest live.

    THREE PIECES OF TEXT, and no key. The live change is named once, at the
    top, BESIDE A SAMPLE OF THE CURVE THAT JUST APPEARED, so one new curve
    and one new line of text arrive together and the identification needs no
    legend to decode. Earlier changes drop to a muted one-line history.
    Underneath sits the steady state COMPUTED for this run -- so the headline
    changes at every click and the number below it does not, which is the
    whole claim.

    The steady state is read from `closed_loop_steady_state`, at the model's
    own horizon, NOT off the right-hand edge of the plot: the slowest plant
    here is still at 4.98 at t = 120 and exact at its steady state, and a
    marker reading 5.0000 printed on a curve sitting at 4.98 is the kind of
    quiet half-truth this session cannot afford.
    """
    fig, ax = plt.subplots(figsize=(9.6, 4.90))
    t = np.linspace(0, 120, 1600)
    HI = 15.2                   # headroom over the 9.54 peak for the labels

    for i, (_lab, q, colour, ls, _short) in enumerate(PLANT_RUNS[:stage]):
        live = (i == stage - 1)
        keep = live or i == 0               # the reference stays full strength
        ax.plot(t, simulate(q, d=0.0, t_end=400.0).sol(t)[0],
                color=colour, ls=ls, lw=3.0 if live else 2.2,
                alpha=1.0 if keep else 0.45, zorder=4 if live else 2)

    ax.axhline(P.set_point, color=MUTED, lw=1.5, ls=":", zorder=1)

    # THE LIVE CHANGE: a sample of the curve that just appeared, then the
    # change named beside it in INK. Setting the headline in the curve's own
    # colour read better on a monitor and worse on a wall -- CYAN and AMBER
    # sit at 1.7:1 and 2.6:1 against this ground, which is fine for a 3pt
    # line and not fine for type at eight metres. The swatch carries the
    # identification, the ink carries the words, and nothing is a key the
    # room has to decode before it can read the picture.
    #
    # add_artist, not ax.plot: a Line2D in AXES coordinates handed to
    # ax.lines would be transformed as DATA by figure_fit's occlusion check
    # and land somewhere meaningless.
    live_lab, live_q, live_col, live_ls, _sh = PLANT_RUNS[stage - 1]
    ax.add_artist(Line2D([0.022, 0.082], [0.925, 0.925],
                         transform=ax.transAxes, color=live_col, ls=live_ls,
                         lw=3.6, solid_capstyle="butt"))
    ax.text(0.098, 0.985, live_lab, transform=ax.transAxes, va="top",
            ha="left", color=INK, fontsize=TYPE["emphasis"],
            fontweight="bold")
    done = [r[4] for r in PLANT_RUNS[1:stage - 1] if r[4]]
    if done:
        ax.text(0.098, 0.800, "already changed:    " + ",     ".join(done),
                transform=ax.transAxes, va="top", ha="left", color=MUTED,
                fontsize=SUB)

    # Below the set-point line and past t = 50, where the lowest any curve
    # goes is 4.31 and the band underneath is empty. NO LEADER ARROW: an
    # Annotation's window extent is the union of its text AND its arrow, so an
    # arrow drawn up to the line put the box across the ringing gamma = 0.1
    # curve and figure_fit counted 91 of its points under the label -- which
    # is the occlusion defect, correctly reported. The set-point line carries
    # the y tick at 5, and this line names mu/theta, so the two are tied
    # without drawing anything through the data.
    ax.text(80, 2.95,
            f"settles at  $X = r = "
            f"{closed_loop_steady_state(live_q):.4f}$",
            color=INK, fontsize=SUB, ha="center", va="top")

    ax.set_xlim(0, 120)
    ax.set_ylim(0, HI)
    ax.set_yticks([0, 5, 10])
    ax.set_xlabel("time")
    ax.set_ylabel("output $X$")
    # The MODEL, and only the model. The claim is the slide's title, and
    # printing it here as well is the verbal redundancy that scores g = 0.06
    # in docs/lecture-design.md 5 -- it is also what made this figure's
    # neighbour hard to take in (note 13).
    ax.set_title("reference values:  " + HELD_R + "\n"
                 "no dilution,  $d=0$  in every run", pad=8)
    _save(fig, name)


def fig_plant_does_not_matter():
    """THE SESSION'S CLAIM, built one changed constant at a time.

    Aoki: "it does not depend on the topology and parameters of the circuit of
    interest". So vary one constant, show the output landing in the same
    place, and only then vary the next.

    WHY IT IS A RUN AND NOT A PICTURE (note 14: "too many curves linked to too
    many parameters"). The single panel it replaced opened with four curves,
    four line styles and a four-entry key, against four parameters that had
    all already moved. Nobody can run that comparison from a chair: it is a
    result you are asked to accept. The deck bar (instructor-only) C3 says
    several curves to several parameters is taken one at a time, so here each
    stage adds exactly one changed constant against a reference that never
    moves, names it beside a sample of its own curve, and restates the
    steady state computed for that run.

    Four PNGs. The last keeps the plain name, so it is still "the figure"
    anywhere a single image is wanted, and the exported PDF carries one page
    per change -- which is the record a revising student needs, because each
    page names the one curve it introduced.
    """
    for stage in range(1, len(PLANT_RUNS) + 1):
        last = (stage == len(PLANT_RUNS))
        _plant_panel(stage, "s22_plant_does_not_matter"
                            + ("" if last else f"_{stage}"))


def _step_panel(stage, name):
    """One moment of the step run: the open loop, then the closed loop on it.

    Both circuits start AT their undisturbed steady state and the disturbance
    arrives at t = 40, so what the room sees is the response to d and not the
    start-up transient. The open loop is integrated, not drawn as a line.

    THE Y AXIS DOES NOT START AT ZERO, deliberately. Everything here lives
    between 4.68 and 7.00: a 2.00 offset against a 0.32 excursion. On an axis
    from zero the recovery is a wiggle, and "the gap is zero, not small" --
    the sentence this figure exists to let him point at -- is the one thing
    that cannot then be seen. The set-point line is drawn and labelled and the
    offset is bracketed and quantified, so the window hides nothing.

    FOUR DIRECT LABELS AND NO KEY. A label beside the thing it labels is the
    one slide-design finding that helps novices and experts equally, and a key
    makes the room decode a line style before it can read the picture.
    """
    fig, ax = plt.subplots(figsize=(9.6, 4.80))
    d, t_step, t_end = 1.0, 40.0, 200.0
    t = np.linspace(0, t_end, 1400)

    so = step_response(P, d=d, t_step=t_step, t_end=t_end, closed=False)
    ax.plot(t, so.sol(t)[0], color=RED, lw=2.8, ls="--", zorder=3)
    ax.text(58, 7.22, "loop open", color=RED, fontsize=TYPE["emphasis"],
            fontweight="bold", va="bottom", ha="left")

    ax.axvline(t_step, color=MUTED, lw=1.3, ls=":")
    ax.text(t_step - 4, 7.30, "$d$ arrives", color=INK, fontsize=SUB,
            ha="right", va="bottom")
    ax.axhline(P.set_point, color=MUTED, lw=1.3, ls=":")
    ax.text(4, 5.16, "$r$", color=MUTED, fontsize=SUB,
            ha="left", va="bottom")

    base, top = P.set_point, float(so.sol(t_end)[0])
    ax.annotate("", xy=(187, top), xytext=(187, base),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.2))
    ax.text(183, (top + base) / 2, f"$+{top - base:.0f} = d/\\gamma$",
            color=RED, fontsize=TYPE["emphasis"], ha="right", va="center")

    if stage == 2:
        sc = step_response(P, d=d, t_step=t_step, t_end=t_end, closed=True)
        ax.plot(t, sc.sol(t)[0], color=TEAL, lw=3.2, zorder=4)
        ax.text(86, 4.56, "loop closed", color=TEAL,
                fontsize=TYPE["emphasis"], fontweight="bold",
                va="top", ha="left")

    ax.set_xlabel("time")
    ax.set_ylabel("output $X$")
    ax.set_xlim(0, t_end)
    ax.set_ylim(3.9, 8.1)
    ax.set_yticks([4, 5, 6, 7, 8])
    ax.set_title("step $d=1$ at $t=40$;  no dilution\n" + HELD_R, pad=8)
    _save(fig, name)


def fig_step():
    """Closed and open loop, same plant, same step disturbance, in two moves.

    WHY IT IS A RUN (note 13: "complex slide with no build. It is ok but the
    text makes the figure hard to take in and the fonts are all small").

    THE TEXT. The panel it replaced carried its own two-line claim block
    inside the axes -- "the open loop takes the hit and keeps it. / the closed
    loop takes the hit and gives it back." -- which was also, word for word,
    the foot of the slide it was placed on. Prose on a slide beside the same
    prose spoken is the redundancy effect; prose laid over a figure collapses
    the signalling benefit to g = 0.06. Both copies cannot be right, and the
    one that goes is the one inside the data.

    THE FONTS. Nothing was authored below the floor. The old PNG saved 4.80in
    tall, and `d.image(..., h=5.05)` placed it at 1.052, so 20pt authored
    landed at 21pt on the wall -- at the floor and not a point above it. These
    save at 4.40in and place at 1.148, so the same 20pt lands at 23.0 and the
    three labels that have to carry across the room land at 27.5.

    Measured against the SAVED PNG, not against tools/figure_fit.py's bbox:
    `get_tightbbox` excludes savefig's 0.1in of pad per side, so its placement
    scale runs about two per cent optimistic.
    """
    for stage in (1, 2):
        _step_panel(stage, "s22_step" + ("_1" if stage == 1 else ""))


def fig_leak():
    """Set-point error against the dilution rate, slope one.

    The integrator is exact only if Z1 and Z2 are lost ONLY by annihilation.
    Dilute them and mu - theta*X = delta*(Z1 - Z2), so the error is first
    order in delta. This is the session's link back to rung 1: growth rate was
    what the circuit changed, and here it is what degrades the guarantee.

    WHERE THE ANNOTATION GOES, AND WHY IT IS TWO LINES (note 26: "text and
    graph overlap and it makes it hard to understand"). The data is a positive
    diagonal across the whole axes, so the only clear ground is the upper-left
    and lower-right triangles, and how much of either is clear depends on the
    SHAPE of the block, not on which corner you pick. At the 20pt content
    floor the old three-line block rendered 805 x 218 px in a 1210 x 481 px
    axes -- two thirds of the width and nearly half the height -- and a block
    that big has no clear corner: from the upper left its bottom-right ran 230
    px along both curves, and mirrored into the lower right it would run the
    same distance along them. Moving it was never going to be enough.

    So the third line went instead. "first order in delta" was already the
    slide title, the slide foot and the "slope 1" label on this figure --
    three copies of one claim, which is the redundancy effect paid for with
    the space that made the figure illegible. What is left is the one thing
    stated nowhere else: the signed formula, and the condition under which
    the sign is the one the room is being shown. At 602 x 145 px the block
    clears both curves by 55 px, and the "slope 1" label clears them by 46.

    THE LIMITS ARE EXPLICIT, which they were not. With autoscaling the
    clearance above depends on matplotlib's margin policy and on how
    tight_layout happens to size the axes, so a layout measured clean once is
    not a layout that stays clean. Pinned limits make the geometry above a
    property of this function rather than of the rendering.

    Measured on the SAVED PNG at d.image(h=5.05): placement scale 1.052, so
    20 pt authored lands at 21.0 pt on the wall.
    """
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    deltas = np.logspace(-3.4, -0.7, 18)
    errs = np.array([abs(setpoint_error(ControlParams(delta=float(dl)), 1.0))
                     for dl in deltas])

    # The slope-one line goes UNDER the data, so the data reads as lying on it
    # rather than as a second curve crossing it.
    ax.loglog(deltas, errs[0] * (deltas / deltas[0]), color=MUTED, lw=1.6,
              ls=":", zorder=1)
    ax.loglog(deltas, errs, "o-", color=TEAL, lw=2.4, ms=8, zorder=3)

    ax.set_xlim(2.6e-4, 3.1e-1)
    ax.set_ylim(1.7e-4, 2.1e-1)
    ax.set_xlabel("dilution rate of the controller species,  $\\delta$")
    ax.set_ylabel("|set-point error|,  $|X_{ss} - \\mu/\\theta|$")
    ax.set_title("Dilute the controller and the integrator leaks\n"
                 "$\\delta>0$, $d=1$ throughout;  " + HELD, pad=12)

    # Below the line, naming it. Close enough to read as its label, 46 px
    # clear of both curves.
    ax.text(0.68, 0.52, "slope 1", color=MUTED, fontsize=SUB,
            ha="center", va="top", transform=ax.transAxes)

    # Upper left, two lines. The minus is the whole point: written without it
    # the formula says the output overshoots while every number says it
    # undershoots, and it was wrong in six files until 27 October. The
    # condition travels with it, because the sign is NOT fixed -- past
    # d = 2.05, still inside the actuator bound, the same formula overshoots.
    ax.text(0.035, 0.96,
            "$X_{ss} - \\mu/\\theta = -(\\delta/\\theta)(Z_1 - Z_2)$\n"
            "at $d = 1$ here, $X$ undershoots",
            transform=ax.transAxes, ha="left", va="top", color=INK,
            fontsize=SUB, linespacing=1.35)
    _save(fig, "s22_leak")


def fig_patch_vs_feedback():
    """THE HINGE OF THE HOUR, drawn. Three feedforward patches against one loop.

    Rungs 1-3 each ended in a device built against ONE disturbance the
    designer had already named: the burden, the metabolism, the module next
    door. That is a feedforward argument three times over, and this picture
    is why it does not scale -- every lane needs its own named source and its
    own model of it, and a source nobody listed gets no device at all.

    THE FOURTH LANE IS THE ARGUMENT, AND ITS GEOMETRY IS LOAD-BEARING. It is
    built from exactly the same parts as the three above it -- arrow, device
    slot, arrow, circuit -- so that the single difference is visible: the
    device slot is empty, and the cross sits where a device's NAME sits in
    every other lane. The dashed path then continues to the circuit and lands
    on it like all the others, because it does arrive. That is the point.
    An earlier draft put the cross on the path and stopped the arrow short of
    the circuit, which drew the exact inverse of the claim -- a disturbance
    blocked -- at the moment the argument turns. A cross on a path means
    blocked; a cross in a slot means nothing was built.

    The right panel is the alternative: one arrangement that measures the
    output. The disturbance arrow reaches the circuit without passing through
    any box, which is the claim drawn as topology rather than asserted, so
    the panel needs no words saying "no model". It does NOT claim feedback is
    free -- the footer sends the costs to the last third of the session,
    which is where saturation and the leak live.

    THE CIRCUIT IS THE SAME OBJECT ON BOTH SIDES, drawn as the same spine at
    the same height with the same rotated label, because holding it fixed
    while the machinery around it changes is the one comparison this surface
    exists to make. It was a spine on the left and a horizontal box on the
    right, which made the reader re-find it halfway across the figure.

    Colors are the control palette `fig_block_diagram` establishes: RED is a
    disturbance, TEAL is something you built, AMBER is sensing, INK is the
    circuit being controlled. "Plant" is deliberately absent, because this
    surface comes BEFORE the slide that defines the word.

    BOX WIDTHS ARE MEASURED, not guessed. At the 20pt content floor
    "the metabolism" renders 322 px and "one you missed" 331 px, so a 2.50
    unit box left 26 px of slack -- 13 px a side, which reads as text jammed
    against its own border even though figure_fit's spill check passes it.
    Every box here is its widest label plus 60 px or more.
    """
    # 4.90, not the 5.15 the other two diagrams here carry: this one shares
    # its slide with a title and a one-line definition of "patching", so it
    # gets a 4.60in band rather than 5.05. At 5.15 the saved figure is 4.69in
    # tall and that band scales it to 0.98, which puts every 20pt label on
    # the wall at 19.6. At 4.90 it saves 4.41in tall and is scaled UP to
    # 1.042. Change the slide's band and this number has to move with it.
    # The width is capped too, and by a different gate: figure_fit measures
    # against image_centered's 10.2in, so a figure wider than that fails the
    # type floor there however generous the real slide band is.
    fig, ax = plt.subplots(figsize=(10.4, 4.90))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6.5); ax.axis("off")

    def box(x, y, w, h, label, colour, dashed=False):
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, lw=2.2,
                                   edgecolor=colour, zorder=3,
                                   ls=(0, (5, 4)) if dashed else "-"))
        # SUB, not emphasis, for a box's name here. "the metabolism" at 24pt
        # is wider than any box this layout can afford, and the content floor
        # is the rule -- the two-level hierarchy is not.
        if label:
            ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                    color=colour, fontsize=SUB, zorder=4)

    def arrow(x1, y1, x2, y2, colour, dashed=False):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.2,
                                    linestyle=(0, (5, 4)) if dashed else "-"))

    def spine(x, label_x):
        """The circuit being controlled. Identical on both sides, by rule."""
        ax.add_patch(plt.Rectangle((x, 1.40), 0.60, 3.55, fill=False, lw=2.2,
                                   edgecolor=INK, zorder=3))
        ax.text(label_x, 3.17, "your circuit", ha="center", va="center",
                color=INK, fontsize=SUB, rotation=90)

    # ---- left: one lane per disturbance you had already named -------------
    ax.text(3.49, 6.15, "FEEDFORWARD", ha="center", va="center", color=INK,
            fontsize=TYPE["emphasis"])
    ax.text(1.765, 5.30, "name it first", ha="center", va="center", color=RED,
            fontsize=SUB)
    ax.text(4.775, 5.30, "built from a model", ha="center", va="center",
            color=TEAL, fontsize=SUB)

    for y, tag, source, fix in [(4.55, "19", "the burden", "a budget"),
                                (3.65, "20", "the metabolism", "a flux model"),
                                (2.75, "21", "the load", "a fast stage")]:
        ax.text(0.02, y, tag, ha="left", va="center", color=TEAL, fontsize=SUB)
        box(0.49, y - 0.36, 2.70, 0.72, source, RED)
        arrow(3.27, y, 3.61, y, TEAL)
        box(3.65, y - 0.36, 2.25, 0.72, fix, TEAL)
        arrow(5.94, y, 6.31, y, TEAL)

    # Same four parts as every lane above, same two arrows, same landing on
    # the circuit. The device slot is empty and the cross stands where a
    # device's name stands. Nothing here is drawn as stopped.
    ax.text(0.02, 1.80, "?", ha="left", va="center", color=MUTED,
            fontsize=SUB)
    box(0.49, 1.44, 2.70, 0.72, "one you missed", MUTED, dashed=True)
    arrow(3.27, 1.80, 3.61, 1.80, RED, dashed=True)
    box(3.65, 1.44, 2.25, 0.72, None, MUTED, dashed=True)
    ax.text(4.775, 1.80, "$\\times$", ha="center", va="center", color=RED,
            fontsize=TYPE["emphasis"])
    arrow(5.94, 1.80, 6.31, 1.80, RED, dashed=True)

    spine(6.35, 6.65)

    ax.text(3.49, 0.75, "no device, and it arrives anyway", ha="center",
            va="center", color=RED, fontsize=SUB)

    # Two points, so figure_fit's text-on-data check cannot be tripped by a
    # label near the divider: that check counts plotted points under a label
    # box, and its threshold is more than two.
    ax.plot([7.15, 7.15], [0.20, 5.95], color=MUTED, lw=1.4, ls=(0, (4, 4)))

    # ---- right: one loop, and no list -------------------------------------
    ax.text(9.10, 6.15, "FEEDBACK", ha="center", va="center", color=TEAL,
            fontsize=TYPE["emphasis"])

    # No box stands between this arrow and the circuit, and that gap IS the
    # claim -- so the panel carries no line saying "no model". Drawing it and
    # saying it would be the same assertion twice.
    ax.text(9.55, 4.55, "a disturbance\nnever named", ha="right",
            va="center", color=RED, fontsize=SUB, linespacing=1.3)
    arrow(9.70, 4.55, 10.21, 4.55, RED)

    spine(10.25, 10.55)

    # The loop: out of the circuit, around, and back in. Straight legs with
    # an arrowhead at each end, so the ring reads as one path.
    arrow(10.25, 1.95, 9.70, 1.95, AMBER)
    ax.plot([9.70, 8.20], [1.95, 1.95], color=AMBER, lw=2.2)
    ax.plot([8.20, 8.20], [1.95, 3.70], color=AMBER, lw=2.2)
    ax.plot([8.20, 9.85], [3.70, 3.70], color=AMBER, lw=2.2)
    arrow(9.85, 3.70, 10.21, 3.70, AMBER)
    ax.text(9.05, 2.83, "measure\nthe output", ha="center", va="center",
            color=AMBER, fontsize=SUB, linespacing=1.3)

    ax.text(9.10, 1.30, "no list needed.\ncosts come later.", ha="center",
            va="top", color=INK, fontsize=SUB, linespacing=1.3)

    _save(fig, "s22_patch_vs_feedback")


def _iffl_sketch(ax):
    """Session 10's incoherent feedforward loop, drawn on the panel that
    compares it with today's controller.

    WHY IT IS HERE AT ALL. The review: "Slide 11 comes from nowhere. What is
    the system? What are we showing here? Asking them to remember a system
    from over 10 sessions ago makes no sense." Half of this panel was session
    10's I1-FFL and the loop itself was nowhere on the surface, so the only
    way to know what the amber and red curves were was to remember a circuit
    from twelve sessions back. A figure whose subject is invisible is not a
    figure.

    WHY THE TOPOLOGY AND NOT A SINGLE NUMBER. The alternative is to cut the
    sweep and print 0.6193 beside the circuit. That loses the claim the
    panel exists to make -- the feedforward loop's adaptation error MOVES
    when its own rate constants move, and today's does not move at all --
    and the sweep is the only thing on the surface that shows it. So the
    sweep stays and the subject becomes visible.

    NAMED BY ROLE, NOT BY LETTER. Session 10 calls the three species X, Y
    and Z. X is this session's controlled output and Z1, Z2 are its
    controller species, so reusing those letters here would put two meanings
    of X on one panel. "input", "repressor", "output" needs no glossary and
    collides with nothing.

    Three activations and one repression bar, all of them annotations: an
    arrow's ink is excluded from tools/figure_fit.py's label boxes by design,
    so the three words are the only things the gate has to keep apart, and
    they sit above y = 1.2, where no curve in this figure goes: the highest
    point plotted is 0.832. Every clearance below was measured off the
    rendered PNG at 160 dpi, not estimated.
    """
    # ONE ROW, BECAUSE THE BAND IS 80 px TALL. This axes is 397 px high for
    # its whole y range, so a 20 pt line is 54 px of it and a stacked
    # topology does not fit above the data without either shrinking the type
    # -- which is the one thing that is never traded -- or growing the figure
    # until the placement scale drops under 1.0 and the whole panel loses a
    # point. The chain reads left to right and the bypass edge arcs beneath
    # it, which is the I1-FFL exactly: the input drives the repressor, the
    # input drives the output, and the repressor holds the output down.
    ROW, UNDER = 1.38, 1.19
    EDGE = dict(color=AMBER, lw=2.4, shrinkA=3, shrinkB=3)
    for x1, x2, y, rad, style in [
            (0.635, 0.705, ROW, 0.0, "-|>"),           # input -> repressor
            (0.965, 1.035, ROW, 0.0,                   # repressor -| output
             "-[, widthB=0.34, lengthB=0.0"),
            (0.555, 1.125, UNDER, -0.10, "-|>")]:      # input -> output
        ax.annotate("", xy=(x2, y), xytext=(x1, y), zorder=5,
                    arrowprops=dict(arrowstyle=style,
                                    connectionstyle=f"arc3,rad={rad}",
                                    **EDGE))
    for x, word in [(0.50, "input"), (0.72, "repressor"), (1.05, "output")]:
        ax.text(x, ROW, word, ha="left", va="center", color=INK,
                fontsize=SUB, zorder=6)


def fig_partial_vs_exact():
    """THE PAYOFF OF THE HOUR, DRAWN. Session 10's number moves; this one is 0.

    The hour opens by asking the room for session 10's adaptation error --
    final / peak = 0.6193, computed on PS5 Q3a -- and until now the answer
    lived only in a speaker note, so the question was posed at the top of the
    hour and never answered on screen. It is answered here, next to the result
    the derivation just landed.

    THE SAME QUESTION, ASKED OF BOTH DESIGNS: scale a rate constant of the
    circuit and look at what is left of the step once everything has settled.
    The feedforward motif's answer moves with whatever you scale. The integral
    controller's answer is zero whatever you scale in the plant, which is what
    the five lines just showed -- X_ss = r, and r is the controller's own
    number. The ratio it turns out to be made of is twelve slides away and
    is not spent here.

    TWO MODELS ON ONE AXIS, WHICH THIS MODULE'S "one model per figure" RULE
    normally forbids and which the comments over the axis set out in full. The
    short version: the two curves measure the same quantity by two different
    formulas, both formulas are written on the panel rather than merged into
    one name, and the arithmetic that makes them the same quantity was checked
    rather than assumed.

    WHAT IS NOT CLAIMED. "It moves with every rate constant" is too strong and
    was checked: beta_z cancels out of final / peak entirely, so scaling it
    moves nothing. K_yz and B_y both move it, which is the honest claim and
    the one drawn -- change the motif's parameters and the number you quote
    changes with them.

    IMPORT NOTE. `figures.s10_feedforward` calls `use(legacy=True)` at import,
    so importing it at module scope would silently drop every figure built
    after it in this process to the pre-20pt scale. It is imported inside this
    function and the 20pt scale is re-applied before anything is drawn.
    """
    from figures.s10_feedforward import iffl_numbers
    use()                 # undo s10's legacy scale -- see the import note

    x = np.linspace(0.5, 2.0, 13)
    kyz = [iffl_numbers(Kyz=0.5 * v)["adaptation_error"] for v in x]
    by = [iffl_numbers(By=0.4 * v)["adaptation_error"] for v in x]
    e_k = [setpoint_error(ControlParams(k=1.0 * v), 1.0) for v in x]
    e_g = [setpoint_error(ControlParams(gamma=0.5 * v), 1.0) for v in x]

    # ONE PANEL, NOT TWO. The first build of this figure put the two designs
    # in side-by-side axes. At the 20 pt content floor each panel is about
    # four inches wide, which is roughly twenty-eight characters a line: the
    # key alone covered nine of the thirteen plotted points of both
    # feedforward curves, and the two y-labels ran into the two titles. The
    # type floor is not negotiable, so the geometry gave way instead.
    #
    # ONE AXIS IS HONEST HERE, and that had to be checked rather than assumed.
    # Session 10's adaptation error is a RATIO (final / peak) and this
    # session's set-point error is a DIFFERENCE (X_ss - r) -- the
    # overload the session docstring records and PS8 Q4c flags. They share an
    # axis only because Z's pre-step baseline is exactly 0, so session 10's
    # final / peak IS the fraction of the excursion still there, and the
    # controller's numerator is exactly 0, so any normalization gives 0. Both
    # definitions are written on the panel rather than merged into one name.
    fig, ax = plt.subplots(figsize=(10.2, 4.65))

    # -- the old way: the number is a function of the motif's own constants --
    ax.plot(x, kyz, color=AMBER, lw=2.8)
    ax.plot(x, by, color=RED, lw=2.8, ls="--")
    ax.plot([1.0], [0.6193], marker="o", ms=11, color=INK, zorder=5)

    # -- today: the answer has no plant constant in it to move --------------
    ax.plot(x, e_k, color=TEAL, lw=3.6)
    ax.plot(x, e_g, color=CYAN, lw=2.6, ls="--")

    # Labels on the curves, not in a key: a key is one more box competing for
    # the same four inches. Each one sits in a band the data never enters,
    # and the gaps were measured off the rendered PNG rather than eyeballed:
    # the tightest pair on this panel clears by 27 px against figure_fit's
    # 10 px rule, which is the margin macOS font metrics need.
    ax.text(0.50, 1.93, "session 10's incoherent feedforward loop",
            color=AMBER, fontsize=SUB, ha="left", va="top")
    _iffl_sketch(ax)
    # Which constants were scaled, on the row with the circuit they belong
    # to and in the curves' own amber. It was the second line of the heading
    # and the heading now has to be one line: a two-line heading plus the
    # topology is more than the band above the data holds.
    ax.text(2.03, 1.38, "$K_{yz}$ or $B_y$ scaled", color=AMBER,
            fontsize=SUB, ha="right", va="center")
    # Bottom right, which is the one band this panel leaves empty: the
    # feedforward curves run 0.50 to 0.83 and the controller's two run flat
    # on zero, so a label between them is under one of them. It used to sit
    # at 0.40 with four pixels of daylight over the red curve, and the band
    # above the data is now the topology's.
    # (1.543, 0.30), NOT (1.52, 0.18). At 0.18 this box and the teal label
    # to its left shared a horizontal band and cleared by 1.7 px when the
    # figure was rendered on the instructor's machine -- clean in the
    # container, a touch on his. The container is not a faithful proxy for
    # his font metrics and this is the second time that gap has bitten, so
    # the fix buys margin in BOTH directions rather than the minimum in one:
    # 22 px of daylight to the teal label's right edge, 21 px under the
    # lowest feedforward curve right of x = 1.45 (y = 0.683), and 13 px
    # inside the axes' right edge. Measured off the rendered PNG on the
    # instructor's machine, not estimated here.
    ax.annotate("0.6193 on PS5 Q3a", xy=(1.0, 0.6193), xytext=(1.543, 0.30),
                color=INK, fontsize=SUB, ha="left", va="bottom",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    # "today's controller", NOT "today's integral controller". Moving the
    # 0.6193 callout up and right bought 8 px against this label's right
    # edge and no more -- tight_layout re-flows the axes when the callout
    # moves, so the margin a measurement predicts is not the margin that
    # renders. Nine characters of label is worth about 190 px and does not
    # move when anything else does. "integral" is what the room has just
    # spent five steps deriving and the pairing this label is half of --
    # session 10's against today's -- is what the panel argues, so the word
    # that goes is the one the five steps already put in the room.
    ax.text(0.50, 0.09, "today's controller, $k$ or $\\gamma$ scaled",
            color=TEAL, fontsize=SUB, ha="left", va="bottom")

    ax.set_xlabel("a rate constant of the circuit, \u00d7 its nominal value")
    ax.set_ylabel("fraction left")
    ax.set_xlim(0.45, 2.05)
    # Headroom for the topology, not for data: nothing plotted here goes
    # above 0.832, and the band from 0.95 up is empty in every run of this
    # figure. The curves keep every pixel of ink they had.
    ax.set_ylim(-0.08, 1.95)
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.axhline(0.0, color=RULE, lw=1.2, zorder=0)
    # The subtitle names BOTH definitions, because the two curves measure the
    # same thing by two different formulas and merging them into one name is
    # the `adaptation_error` / `setpoint_error` overload. It says "no
    # dilution" rather than "delta = 0": delta belongs to the leak segment
    # much later in the hour and nothing has defined it by the time this is
    # on the wall, which is the rule this deck is being rebuilt against.
    # "today: X - r" and not "X - mu/theta": this panel is on the wall
    # twelve slides before the subtraction produces either constant, and the
    # derivation it debriefs ended at X = r.
    ax.set_title("What is left of the step once everything has settled\n"
                 "session 10: final / peak.   "
                 "today: $X-r$, no dilution",
                 pad=10)

    _save(fig, "s22_partial_vs_exact")


def fig_defenses_traded():
    """WHAT THE HOUR TRADED, drawn. Four defenses, and the price of the fourth.

    THIS IS NOT THE HINGE FIGURE AGAIN, and the difference is the whole
    reason it exists. `fig_patch_vs_feedback` runs at the top of the hour and
    argues one thing: a disturbance you never named gets no device, so a
    longer list is not the answer. It draws the fourth lane's device slot
    EMPTY and sends the costs away -- "costs come later" is printed on it.
    Nothing in the deck ever went back and closed that promise. Between the
    two figures the hour derived X = mu/theta, watched four plants land on it,
    built the motif out of a sigma and an anti-sigma factor, and measured
    three ways a cell misses it. This figure is the hinge's own question
    answered: the fourth defense needs no list, and here is what it needs
    instead.

    SO THE CLAIM IS AN EXCHANGE, and neither existing figure makes it.
    `fig_patch_vs_feedback` has the left half (you stop naming disturbances)
    and no right half at all. `fig_partial_vs_exact` has a different claim
    entirely -- session 10's 0.6193 moves when the motif's constants move and
    today's zero does not -- which is quantitative, mid-derivation, and about
    one number rather than about four sessions. The trade itself has only
    ever been prose, in the design ledger's guarantee row and in the
    "Running out is not the same as leaking" rows.

    NO CROSS, DELIBERATELY. The hinge figure's cross means "nothing was built
    here", and its docstring records the draft that put a cross on the PATH
    and accidentally drew a disturbance being blocked. Lane 22 here HAS a
    device, so a cross would be the inverse of the claim twice over. What
    carries the punchline instead is an absence of text where the other three
    columns carry some: "nothing", set at TYPE["emphasis"] because it is the
    one word on the surface that has to land.

    THE SESSIONS ARE NAMED, NOT NUMBERED AS RUNGS. "Rung" and "ladder" are
    this repo's private scaffolding vocabulary and they were never defined on
    a slide; worse, session 12 already spends "ladder" and "rung" ON SCREEN on
    the infinite ladder of master equations, one rung per molecule number, in
    a derivation run and in its closing box. Sessions 19 and 21 both put this
    same arc on a slide and both name the sessions instead -- s21's row labels
    are "session 18 / session 19 / today". This figure follows that
    convention.

    PALETTE IS `fig_block_diagram`'s, as the hinge figure's is: RED is a
    disturbance, TEAL is something you built or got, AMBER is a limit -- the
    same role AMBER plays on the design ledger's limits row. INK is neutral
    statement.

    GEOMETRY, AND A UNIT THAT IS NOT SQUARE. tight_layout leaves this axes
    1728 x 512 px, so against xlim 10.4 and ylim 3.85 one x unit is 166 px
    and one y unit is 133 px. They are not interchangeable, and the first
    draft of this figure was laid out as though they were -- seven of
    figure_fit's "touches", every one a gap of 10.4 px against a threshold
    of 10. Boxes are 2.40 x units wide for a widest label ("the metabolism")
    of 1.96, which is the hinge figure's "widest label plus 60 px" rule with
    72 px to spare.

    THE SLIDE PLACES THIS IN A 11.93 x 3.90 BAND, shorter than the deck's
    usual 5.05, because the surface also carries the two sentences Part III
    opens on underneath it. Short and wide is what makes that affordable:
    saved at 11.00 x 3.40 the aspect is 3.24 against the band's 3.06, so the
    fit is WIDTH-limited and the placement scale is 11.93/11.00 = 1.085 --
    20 pt lands at 21.7 on the wall. Trimming the band further costs nothing
    until the aspect drops under 3.06. Change the band or any string and
    re-measure: tight_layout makes the saved size depend on the content.
    """
    # EVERY NUMBER BELOW IS MEASURED off a render of this figure, not
    # estimated from a 0.5-em advance: at dpi 160 a 20 pt line's box is
    # 53.8 px, and the axes comes out 1728 x 512 px, so one x unit is
    # 166 px and one y unit is 133 px -- NOT the same size. The first draft
    # was laid out in inches on the assumption that they were, and
    # figure_fit returned seven "touches", every one of them a gap that was
    # 10.4 px where the threshold is 10. Text-to-text gaps here are 21 px at
    # the tightest and 40 px at the widest. Re-measure after any string
    # change: tight_layout makes the axes size depend on the content.
    fig, ax = plt.subplots(figsize=(11.4, 3.80))
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 3.85); ax.axis("off")

    COLS = (1.30, 3.90, 6.50, 9.10)          # column centres
    BOXW = 2.40                              # widest label 1.96 + 72 px

    # ---- what each session was up against --------------------------------
    for cx, tag, source in zip(
            COLS, ("session 19", "session 20", "session 21", "session 22"),
            ("the burden", "the metabolism", "the load", "any constant d")):
        ax.text(cx, 3.60, tag, ha="center", va="center", color=TEAL,
                fontsize=SUB)
        ax.add_patch(plt.Rectangle((cx - BOXW / 2, 2.60), BOXW, 0.60,
                                   fill=False, lw=2.2, edgecolor=RED,
                                   zorder=3))
        ax.text(cx, 2.90, source, ha="center", va="center", color=RED,
                fontsize=SUB, zorder=4)

    # ---- and what each one had to be told before you could build ---------
    ax.text(5.20, 2.20, "and what each one had to be told in advance",
            ha="center", va="center", color=MUTED, fontsize=SUB)

    for cx, known in zip(COLS, ("how big it is", "the flux map",
                                "its size and speed")):
        ax.text(cx, 1.60, known, ha="center", va="center", color=INK,
                fontsize=SUB)
    # The one word on this surface that has to land, so the one word above
    # the content floor. No cross: the hinge figure spends a cross on
    # "nothing was built here", and lane 22 has a device.
    ax.text(COLS[3], 1.60, "nothing", ha="center", va="center", color=TEAL,
            fontsize=TYPE["emphasis"])

    # Two points and no marker. figure_fit counts a label's overlap with
    # rendered ink, and this divider is the only line on the figure.
    ax.plot([0.10, 10.30], [1.13, 1.13], color=MUTED, lw=1.4, ls=(0, (4, 4)))

    # ---- the price of needing no list ------------------------------------
    # AMBER, because these three ARE the design ledger's limits column read
    # as requirements, and AMBER is that column's colour one click earlier.
    # The observables are NOT repeated here -- the ledger's limits step
    # carries each one (Z1 pinned and X at d/gamma, the error tracking the
    # growth rate, the ringing), and saying them twice in two minutes cost
    # this figure a row it could not afford.
    ax.text(5.20, 0.81, "session 22 needs these four instead", ha="center",
            va="center", color=TEAL, fontsize=SUB)

    # FOUR, NOT THREE, AND SHORT ENOUGH TO SIT IN FOUR COLUMNS. The row said
    # three and the design ledger's guarantee row says four -- the plant
    # condition went in when "any plant, any parameters" came out, and this
    # figure is the surface that summarises the same list, so a count of
    # three here contradicts the ledger four clicks later.
    #
    # WHY THEY ARE THIS TERSE. Four columns on this axes is 2.60 data units
    # of centre-to-centre room, which is about sixteen characters at the
    # 20 pt body floor, and the floor does not move for a layout. So each
    # condition is a NAME here and its full statement is on the ledger:
    # "in any plant the controller can move and can see -- while the loop is
    # stable, it is lost only to itself, and Z1 has range left." The order
    # matches the ledger's sentence, left to right, so the room reads the
    # same list twice in the same order.
    for cx, cond in zip(COLS, ("$Z_1$ can move $X$",
                               "loop is stable",
                               "little dilution",
                               "$Z_1$ has range")):
        ax.text(cx, 0.25, cond, ha="center", va="center", color=AMBER,
                fontsize=SUB)

    _save(fig, "s22_defenses_traded")


def fig_past_the_bound():
    """PAST THE ACTUATOR BOUND, DRAWN: the flux pins at mu, it does not stop.

    This is the debrief of the release that asks the room for the bound, and
    it exists because of the single error that release is most likely to
    produce. Told that Z1 "runs out", a room concludes that the annihilation
    STOPS; if it stopped, Z2 would climb at theta*X = 20. It does not stop.
    dZ1/dt = mu - eta*Z1*Z2 and Z1 cannot go negative, so on the plateau the
    flux sits at mu -- the most it can ever be -- and Z2 climbs at
    theta*X - mu = 10. A room that has the wrong mechanism predicts exactly
    twice the slope it will measure in PS8 Q4c, and the error is invisible in
    the algebra. So it is drawn.

    LEFT, AND WHY IT IS A LEDGER RATHER THAN A TRAJECTORY. The temptation is
    to plot Z1 crashing to zero beside the flux holding at mu. That needs two
    quantities with different units on one axis -- a concentration against a
    rate -- which is the thing this course spends session 20 telling students
    not to do. Z2's two books have the SAME units: theta*X is what Z2 gains
    and eta*Z1*Z2 is what it loses. Drawing those two makes the gap between
    them a visible height, and that height IS dZ2/dt. Shade it and the
    runaway slope stops being a number in a note.

    RIGHT. Z2 itself, with the slope the room would predict from "it stops"
    drawn dashed alongside the one it will measure. Both horizons PS8 Q4c
    compares are marked, because the question's whole move is that doubling
    the horizon doubles the answer.

    EVERY VALUE IS COMPUTED, none typed: the two slopes and the two horizon
    readings come out of the same integration. At d = 5, delta = 0, X settles
    at d/gamma = 10, so theta*X = 20 and theta*X - mu = 10; Z2 reaches 79,979
    at t = 8000 and 159,979 at t = 16,000 (sessions/s22-control/NUMBERS.md
    section 4, and `settles` at d = 5).
    """
    d, t_end = 5.0, 16000.0
    sol = simulate(P, d=d, t_end=t_end)
    t = np.linspace(0.0, t_end, 1600)
    X, Z1, Z2 = sol.sol(t)
    gain, loss = P.theta * X, P.eta * Z1 * Z2
    late = t > 400                       # past the start-up transient
    g_ss, l_ss = float(gain[late].mean()), float(loss[late].mean())
    z2_a, z2_b = float(sol.sol(8000.0)[2]), float(sol.sol(t_end)[2])

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.6, 4.52))

    # EVERY LABEL IS SHORT, and that is a measurement rather than a taste. A
    # panel of a two-up figure is about 4.3in of axes once the tick column is
    # paid for, which at the 20pt content floor is roughly 30 characters. The
    # first draft put "Z_2 would climb at theta*X = 20" on one line -- 35
    # characters, 759 px -- and it ran straight down the dashed curve it was
    # naming. What a label cannot hold goes in the slide's rows or its note.

    # ---- left: what Z2 gains, what it loses, and the gap ------------------
    axL.fill_between(t, loss, gain, color=AMBER, alpha=0.16, zorder=1)
    axL.plot(t, gain, color=AMBER, lw=2.8, zorder=3)
    axL.plot(t, loss, color=TEAL, lw=2.8, zorder=3)
    axL.axhline(P.mu, color=MUTED, lw=1.4, ls=":", zorder=2)
    axL.set_xlim(0, t_end); axL.set_ylim(0, 30.0)
    axL.set_xticks([0, 8000, 16000])
    axL.set_yticks([0, 10, 20, 30])
    axL.set_xlabel("time")
    axL.set_ylabel("$Z_2$ made, $Z_2$ removed")
    axL.set_title("the annihilation pins at $\\mu$", pad=10)
    axL.text(700, 28.4, f"made:  $\\theta X = {g_ss:.0f}$", color=AMBER,
             fontsize=SUB, ha="left", va="top")
    axL.text(700, 15.0, f"the gap:  $dZ_2/dt = {g_ss - l_ss:.0f}$",
             color=INK, fontsize=SUB, ha="left", va="center")
    axL.text(700, 7.4, f"removed:  $\\eta Z_1 Z_2 = \\mu = {l_ss:.0f}$",
             color=TEAL, fontsize=SUB, ha="left", va="top")

    # ---- right: Z2 itself, against the slope "it stops" would give --------
    axR.plot(t, (g_ss / (g_ss - l_ss)) * Z2, color=RED, lw=2.6, ls="--",
             zorder=2)
    axR.plot(t, Z2, color=AMBER, lw=3.0, zorder=3)
    axR.set_xlim(0, t_end); axR.set_ylim(0, 3.60e5)
    axR.set_xticks([0, 8000, 16000])
    axR.set_yticks([0, 1e5, 2e5, 3e5])
    axR.set_yticklabels(["0", "100,000", "200,000", "300,000"])
    axR.set_xlabel("time")
    axR.set_ylabel("$Z_2$")
    axR.set_title("so $Z_2$ climbs at $\\theta X - \\mu$", pad=10)
    axR.text(900, 3.52e5, "if it STOPPED:\n" f"slope ${g_ss:.0f}$",
             color=RED, fontsize=SUB, ha="left", va="top", linespacing=1.3)
    axR.text(15500, 7.0e4, f"slope ${g_ss - l_ss:.0f}$", color=AMBER,
             fontsize=SUB, ha="right", va="top")

    fig.suptitle(f"past the bound: $d = {d:.0f}$, $\\delta = 0$;  " + HELD,
                 fontsize=SUB, color=INK, y=1.02)
    _save(fig, "s22_past_the_bound")


def fig_two_failures():
    """THE TWO FAILURES SIDE BY SIDE, so the room is not asked to assemble the
    comparison out of prose (note 28: "important findings in a wall of text").

    The surface this replaces listed the leak, then saturation, then the two
    limits that are Aoki's rather than ours, as four rows of sentences on a
    dark slide -- which is a comparison only in the sense that the two things
    being compared were both on it. What makes a comparison readable is that
    the same questions are asked of both columns in the same order, so the eye
    moves ACROSS a row rather than down a paragraph. That is a geometry, and a
    geometry is a figure.

    FOUR QUESTIONS, and they are the four a designer actually has:
    what caused it, what the output did, whether there is a steady state at
    all, and what you would change. The third is the one that separates these
    two failures and it is the one prose keeps burying -- the leak has a
    steady state in the wrong place, saturation has no steady state at all,
    and a simulation stopped at one horizon reports one anyway.

    "NOT k" IS ON THE SLIDE because it is the counter-intuitive half of the
    bound and it is checkable: d <= gamma*mu/theta has no k in it, and a sweep
    of k from 0.25 to 20 moves neither the last d that settles (2.4) nor the
    first that does not (2.6). A room that hears "the actuator ran out" will
    reach for a stronger actuator, and a stronger actuator buys nothing.

    NUMBERS. 2.5 is gamma*mu/theta, DERIVED. d/gamma = 10 at d = 5 and
    0.033732 at delta = 0.05, d = 1, both COMPUTED from posb.control and both
    in sessions/s22-control/NUMBERS.md sections 4 and 5.

    THE SHORT ROWS ARE THE LAYOUT. Five bands of text in a 3.0in figure is
    about eight lines of 20pt type, so every cell is one line and none runs
    past its column. The columns are measured, not guessed: 3.90in for the
    saturation column and 4.03in for the leak, which at 20pt is 28 and 29
    characters, and the first draft overran the divider by 68 px.
    """
    fig, ax = plt.subplots(figsize=(11.0, 3.52))
    ax.set_xlim(0, 12); ax.set_ylim(-0.9, 5); ax.axis("off")

    KEY, CA, CB, DIV = 0.05, 2.55, 7.35, 7.05

    ax.text(CA, 4.5, "SATURATION", color=AMBER, fontsize=TYPE["emphasis"],
            ha="left", va="center")
    ax.text(CB, 4.5, "THE LEAK", color=TEAL, fontsize=TYPE["emphasis"],
            ha="left", va="center")
    ax.plot([0, 12], [4.0, 4.0], color=RULE, lw=1.6)
    ax.plot([DIV, DIV], [0.1, 3.9], color=RULE, lw=1.6)

    rows = [
        (3.5, "what causes it",
         "$d > \\gamma\\mu/\\theta = 2.5$;  here $d = 5$",
         "$\\delta > 0$;  here $\\delta = 0.05$"),
        (2.5, "what $X$ does",
         "settles at $d/\\gamma = 10$", "settles $0.034$ low"),
        # THE CONDITION TRAVELS WITH THE CLAIM. "No steady state" is a
        # delta = 0 statement: at delta = 0.01 and d = 5 there IS one, with
        # Z2 capped at (theta*X - mu)/delta = 1000 and identical at t = 8000
        # and 16,000. What separates the two failures past the bound is how
        # BIG Z2 gets, not whether it converges, and a cell with no dilution
        # is the only place the runaway is literally unbounded.
        (1.5, "steady state?",
         "none at $\\delta = 0$: $Z_2$ runs away", "yes, in the wrong place"),
        (0.5, "the fix",
         "raise $\\gamma$ or $\\mu/\\theta$, not $k$", "lower $\\delta$: grow slower"),
    ]
    for y, key, a, b in rows:
        ax.text(KEY, y, key, color=MUTED, fontsize=SUB, ha="left",
                va="center")
        ax.text(CA, y, a, color=INK, fontsize=SUB, ha="left", va="center")
        ax.text(CB, y, b, color=INK, fontsize=SUB, ha="left", va="center")

    # Both columns quote numbers that belong to one circuit, so the circuit
    # is named on the figure -- the rule the module docstring opens with.
    ax.text(KEY, -0.5, "both:  " + HELD + ";  the leak at $d=1$",
            color=MUTED, fontsize=SUB, ha="left", va="center")

    _save(fig, "s22_two_failures")


def fig_motif_topology():
    """The same motif with the banner off, for the frame before the algebra.

    A lambda in FIGURES has no docstring, so the build printed
    "** NO DOCSTRING **" against this figure every run -- and the build's
    one-line summary is how a figure says what it is for. See fig_motif:
    banner=False is the frame that goes up BEFORE the room subtracts the
    two rate equations, and the banner version is the debrief after.
    """
    fig_motif(banner=False, name="s22_motif_topology")


FIGURES = [fig_block_diagram, fig_motif, fig_motif_topology,
           fig_patch_vs_feedback,
           fig_plant_does_not_matter, fig_partial_vs_exact, fig_step,
           fig_leak, fig_past_the_bound, fig_two_failures,
           fig_defenses_traded]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
