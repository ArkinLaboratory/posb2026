"""Session 23 figures — burden becomes selection.

ONE MODEL PER FIGURE, AND THE MODEL IS NAMED ON THE FIGURE (the rule session
21 added and session 22 kept). This session has the hazard in its sharpest
form yet, because the whole hour turns on two models that produce the SAME
PICTURE: one cassette carrying a fitness cost, and three cassettes carrying
none. `fig_confounded` exists to show exactly that, so every other figure
states which model drew it.

Every curve comes out of `posb.evolution`, the same functions PS9 imports.

ROTTINGHAUS' DATA IS NOT REDRAWN HERE. We hold their reported numbers but not
the points behind any panel, so Figs. 1a, 1d, 1f, 1g, 2e, 2g, 3a and 3b/c go
on slides as PAPER FIGURES with their own attribution. `fig_on_their_axes`
draws OUR model on THEIR axis ranges and says so on the figure; it plots no
measured point. Inventing points to redraw a panel is the thing this course
keeps telling students not to do.

Numbers on these figures are in sessions/s23-evolution/NUMBERS.md with their
kind. Every s here is MODELLED -- Rottinghaus report no fitness cost -- and
each figure that uses one says so.

Run:  python tools/build_figures.py s23
"""
import numpy as np

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           RULE, TYPE)
from posb.evolution import (broken_fraction, multi_hit_broken_fraction,
                            time_to_failure)

plt = use()
OUT = "figures/build"

# The hour's reference point. MODELLED, from session 19's Scott 2010 result.
S_REF, MU_REF = 0.05, 1e-6
NIH = 1e-8            # QUOTED: NIH OBA figure, Rottinghaus p.4
MEASURED_FLOOR = 10 ** -8.6   # MEASURED: optimized 2-gRNA switch, p.4
GEN_PER_DAY = 8.0     # the paper's rounding; log2(250) = 7.9658


# EVERY piece of text inside a figure is content the room has to read, so it
# sits at the body floor. TYPE["caption"] inside a figure is for a literature
# citation and nothing else. An earlier cut of these figures set the legends,
# the in-plot annotations, the region labels and the bar values at caption --
# which projected the five numbers the ledger exists to deliver SMALLER than
# the foot line beneath them. A legend entry carrying an RMS is not a caption.
LBL = TYPE["body"]
PAGE = "#F8FAF9"          # style.py's savefig.facecolor


def _plate(pad=0.3):
    """Page-colored backing for a label that sits over plotted data.

    Without it a curve runs straight through the text. Cheaper and more
    reliable than hand-placing every label into whatever gap the data leaves.
    """
    return dict(facecolor=PAGE, edgecolor="none", pad=pad)


def _tag(ax, x, y, s, color, ha="left", va="bottom"):
    """A short label beside the curve it names, in axes fractions.

    These figures carry no legends. At the 20 pt floor a four-entry key is
    1000-1700 px wide and these panels are 520-1270 px, so inside the axes
    there is no anchor that misses the data -- an opaque key deletes the
    curve it is explaining, a transparent one gets struck through. Putting
    the key underneath instead cost 30 per cent of the plot height, which
    is worse. A two-word tag in the curve's own color costs neither, and on
    a projected slide it saves the round trip to a key.
    """
    ax.text(x, y, s, transform=ax.transAxes, color=color, fontsize=LBL,
            ha=ha, va=va, bbox=_plate(), zorder=7)


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _slope(f, t1, t2):
    return np.log10(f(t2) / f(t1)) / np.log10(t2 / t1)


def fig_confounded(name="s23_confounded"):
    """The figure the hour turns on: you cannot read k off a stability curve.

    Plotting the two curves together invites the answer "but they look
    different" -- they do, outside the window you can actually measure in.
    So this plots the thing the inference actually uses: the log-log SLOPE a
    one-cassette circuit returns, against its true burden. A circuit with one
    cassette and a 5 per cent cost returns a slope between 2.4 and 5.0, which
    reads as two to five cassettes. The architecture is not recoverable.

    MODEL: one cassette throughout. Every point on both curves is k = 1.
    """
    ss = np.linspace(0.0, 0.10, 200)
    dec, loc = [], []
    for s in ss:
        dec.append(_slope(lambda x: broken_fraction(x, s, MU_REF), 10.0, 100.0))
        loc.append((np.log(broken_fraction(105.0, s, MU_REF))
                    - np.log(broken_fraction(95.0, s, MU_REF)))
                   / (np.log(105.0) - np.log(95.0)))

    fig, ax = plt.subplots(figsize=(9.4, 4.55))
    # Four "k cassettes" labels used to sit on these lines. At the body
    # floor each is 254 px wide and the curves sweep the panel, so every one
    # of them covered data. The y-axis already reads 2, 3, 4, 5 and the
    # ylabel now says what the dashed lines mean, so the labels are cut.
    for k in (2, 3, 4, 5):
        ax.axhline(k, color=RULE, lw=1.4, ls="--", zorder=1)
    ax.plot(ss, dec, color=AMBER, lw=3.2, zorder=3)
    ax.plot(ss, loc, color=TEAL, lw=3.2, zorder=3)
    _tag(ax, 0.54, 0.02, "decade fit, t = 10–100", AMBER)
    # 0.46 put this tag on 440 px of the teal curve. The old occlusion
    # check sampled a curve by its DATA POINTS and missed it; the corrected
    # one samples the rendered path. Upper left is the clear quadrant.
    _tag(ax, 0.62, 0.62, "local fit, t = 95–105", TEAL)

    ax.axvline(S_REF, color=RED, lw=2.0, zorder=2)
    ax.plot([S_REF, S_REF], [2.36, 5.02], "o", color=RED, ms=9, zorder=4)
    ax.annotate("one cassette at s = 0.05\nreads as 2.4 to 5.0",
                xy=(S_REF, 3.7), xycoords="data", xytext=(0.02, 0.62),
                textcoords="axes fraction", color=RED, fontsize=LBL,
                linespacing=1.3, bbox=_plate(), zorder=7,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax.set_xlabel("true selection coefficient  $s$  (one cassette)",
                  fontsize=LBL)
    # Short enough not to be clipped by the tight bbox at 20 pt.
    ax.set_ylabel("measured log–log slope", fontsize=LBL)
    ax.set_xlim(0, 0.10); ax.set_ylim(0.6, 8.0)
    ax.grid(True, axis="y", color=RULE, lw=0.5)
    # The fitting windows are part of the numbers (NUMBERS.md 5), so they go
    # in the title, which has the full figure width, not in a key.
    # Short enough that the centered title stays inside the axes; the longer
    # version pushed the tight bbox out past the ylabel.
    ax.set_title("every point is ONE cassette  ·  dashed = k cassettes",
                 fontsize=LBL, color=INK)
    _save(fig, name)


# Fig. 2e digitized from the extracted panel by tools/fit_s23_fig2e.py.
# These are THEIR measurements, read off their panel by image analysis and
# disclosed as such on the figure -- not points we invented, and not a
# redrawing of their figure. The panel itself goes on the preceding slide.
# Assay days 4, 7, 10, 14, 17, 21, 24, 28 (day 1 is below detection and is
# not plotted). An earlier version anchored the first marker at day 0, which
# put every point about a day late.
FIG2E = [(31.9, -6.81), (55.8, -6.67), (79.7, -6.84), (111.5, -6.64),
         (135.4, -6.51), (167.3, -6.23), (191.2, -6.42), (223.0, -6.35)]


def fig_measure_s(name="s23_measure_s"):
    """The stability curve bounds the burden from above: s is below ~0.02.

    An earlier version of this figure claimed the model was REFUTED by this
    data. That rested on using 1e-8.6 -- Fig. 1h, a different strain, with
    antibiotics, one timepoint -- as if it were the 28-day bound. Fig. 2e is
    the CRISPRks strain and it does not sit at a floor: it rises from about
    1e-8 at day 1 to 1e-6.35 over 224 generations.

    And the rise is barely resolved. A flat line scores RMS 0.204 decades
    against the best one-hit fit's 0.151, and the data's own log-log slope is
    0.63 where every model in this family predicts at least 1. So the panel is
    drawn to support a BOUND -- s >~ 0.02 excluded -- and the flat null is
    plotted so the room can see how little the rise is worth.

    So this is an UPPER BOUND on the burden, not a measurement of it. What
    the curve genuinely excludes is s >~ 0.02 (RMS 0.474, three times worse)
    and s = 0.05 (1.215). Plotting the flat line is the honest thing to do
    and it is why it is on the figure.
    """
    t = np.linspace(1.0, 232.0, 500)
    fig, ax = plt.subplots(figsize=(9.4, 4.55))

    gx = [p[0] for p in FIG2E]
    gy = [p[1] for p in FIG2E]
    ax.plot(gx, gy, "D", ms=10, color=RED, zorder=5,
)

    gm = float(np.mean(gy))
    ax.plot([t[0], t[-1]], [gm, gm], color=MUTED, lw=2.2, ls=":")
    ax.plot(t, np.log10(broken_fraction(t, 0.0, 2.63e-9)), color=TEAL, lw=3.0)
    ax.plot(t, np.log10(broken_fraction(t, 0.05, 2.83e-11)), color=AMBER,
            lw=3.0, ls="--")
    _tag(ax, 0.02, 0.72, "no rise", MUTED)
    _tag(ax, 0.86, 0.80, "s = 0", TEAL)
    _tag(ax, 0.30, 0.90, "s = 0.05", AMBER)

    # The RMS block that used to sit here said, word for word, what the
    # slide's own foot says, and it said it lying across 78 px of the data
    # it was explaining. At the 20 pt floor it measures 996 x 146 px and
    # there is NO position inside these axes that clears both curves -- so
    # it does not belong inside the axes. The foot carries the claim; the
    # speaker note carries the s = 0.05 residual for anyone who asks.

    ax.set_xlabel("generations of serial passage", fontsize=LBL)
    ax.set_ylabel("$\\log_{10}$ fraction viable", fontsize=LBL)
    ax.set_xlim(0, 232); ax.set_ylim(-9.2, -5.2)
    ax.grid(True, color=RULE, lw=0.6)
    # The build script name belongs in NUMBERS.md, not on a lecture slide.
    # NO BARE SLOPE HERE. The title used to read "Their own log-log slope
    # is 0.63". Three things wrong with that on this slide: the axes are
    # log-linear, so the quantity cannot be read off the figure it is
    # printed on; no window is given, which is the exact sin the
    # confounding slide accuses everyone else of two clicks later; and
    # 0.63 is BELOW ONE, which the k-cassette model on the slide before
    # this one does not allow for any k. It belongs in the discussion of
    # what the slope cannot do, not in a caption here.
    ax.set_title("red: Rottinghaus Fig. 2e, eight timepoints",
                 fontsize=LBL, color=MUTED)
    _save(fig, name)


def fig_ledger(name="s23_ledger"):
    """What halving the burden buys against what dividing mu by 100 buys.

    Left: the ledger at the reference point. Right: the regime. Halving s
    beats mu/100 for s/mu > 413.0 (the mu -> 0 asymptote of the same
    condition is exactly 100*exp(2*ln2) = 400) -- located by bisection and
    identical at
    s = 1e-3, 5e-3, 0.01, 0.05 and 0.2, so it is a property of the ratio.

    MODEL: one cassette, selection and mutation, no redundancy. This is the
    LONGEVITY question. The containment question has the opposite sensitivity
    -- see fig_two_asymmetries.
    """
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.55))

    rows = [("reference", S_REF, MU_REF), ("$\\mu \\div 10$", S_REF, 1e-7),
            ("$\\mu \\div 100$", S_REF, 1e-8), ("$s \\div 2$", 0.025, MU_REF),
            ("$s \\div 10$", 0.005, MU_REF)]
    labels = [r[0] for r in rows]
    vals = [time_to_failure(0.5, r[1], r[2]) for r in rows]
    cols = [MUTED, CYAN, CYAN, AMBER, AMBER]
    y = np.arange(len(rows))[::-1]
    axL.barh(y, vals, color=cols, height=0.62)
    for yy, v in zip(y, vals):
        extra = v - vals[0]
        txt = f"{v:.0f}" + ("" if extra == 0 else f"   ({extra:+.0f})")
        # These five numbers ARE the slide. They were set at caption, which
        # rendered them smaller in ink than the foot line.
        axL.text(v + 36, yy, txt, va="center", color=INK, fontsize=LBL)
    axL.set_yticks(y); axL.set_yticklabels(labels, fontsize=LBL)
    axL.set_xlabel("generations to half broken  ($t_{50}$)", fontsize=LBL)
    axL.set_xlim(0, 2600)      # headroom for the +1487 label at 20 pt
    axL.set_title("s = 0.05, $\\mu$ = $10^{-6}$  (s MODELLED)",
                  fontsize=LBL, color=MUTED)
    axL.grid(True, axis="x", color=RULE, lw=0.6)

    ss = np.logspace(-3.4, -0.3, 160)
    mus = np.logspace(-9, -2.9, 160)
    S, M = np.meshgrid(ss, mus, indexing="ij")
    gain_s = np.vectorize(lambda a, b: time_to_failure(0.5, a / 2, b))(S, M)
    gain_mu = np.vectorize(lambda a, b: time_to_failure(0.5, a, b / 100))(S, M)
    axR.contourf(S, M, (gain_s > gain_mu).astype(float), levels=[-0.5, 0.5, 1.5],
                 colors=[CYAN, AMBER], alpha=0.30)
    axR.plot(ss, ss / 413.0, color=INK, lw=2.6)
    # AMBER is where halving s wins -- BELOW the line, large s/mu. The first
    # cut of this figure had these two labels the wrong way round, which put
    # the reference point in the region labeled against it.
    # One line each. The two-line versions were 283-315 px wide in a 436 px
    # panel and could not fit inside their own wedge without crossing the
    # boundary line into the region they argue against. The 413 goes in the
    # panel title, where it has the full width.
    axR.text(0.97, 0.04, "halving $s$ wins", transform=axR.transAxes,
             color=INK, fontsize=LBL, ha="right", va="bottom",
             bbox=_plate(), zorder=7)
    axR.text(0.03, 0.96, "$\\mu \\div 100$ wins", transform=axR.transAxes,
             color=INK, fontsize=LBL, ha="left", va="top",
             bbox=_plate(), zorder=7)
    axR.set_title("boundary: $s/\\mu$ = 413", fontsize=LBL, color=INK)
    # Anchored on the boundary line itself, mid-panel. Its old position put
    # the text on top of the "reference" label, and both became illegible.
    # No separate label on the boundary line: both region labels already
    # carry "(s/mu > 413)" and "(s/mu < 413)", so a third one was redundant
    # and there is no room in this panel for it at the body floor.
    axR.plot([S_REF], [MU_REF], "o", color=RED, ms=11, zorder=6)
    # Offset in POINTS, so the label tracks its own dot whatever the limits.
    axR.annotate("reference", xy=(S_REF, MU_REF), xytext=(16, 0),
                 textcoords="offset points", color=RED, fontsize=LBL,
                 ha="left", va="center", bbox=_plate(), zorder=7)
    axR.set_xscale("log"); axR.set_yscale("log")
    axR.set_xlabel("selection coefficient  $s$", fontsize=LBL)
    axR.set_ylabel("mutation rate  $\\mu$", fontsize=LBL)
    axR.grid(True, which="both", color=RULE, lw=0.6)
    _save(fig, name)


def fig_retention(name="s23_retention"):
    """Containment is a duration, not a measurement.

    The measured fraction viable clears the NIH figure AT THE MOMENT OF THE
    ASSAY. Starting there, the standing escape fraction crosses it again
    within a few generations of permissive growth.

    MODEL: one cassette. Both s and mu are MODELLED -- the paper measures
    neither. The spread across the plausible grid is 0.01 to 7.5 generations,
    which is the point: under a day in every case.
    """
    fig, ax = plt.subplots(figsize=(9.4, 4.55))
    t = np.linspace(0, 12, 600)
    TAGY = {}
    for mu, col in ((1e-7, AMBER), (1e-8, TEAL), (1e-9, GREEN)):
        t0 = time_to_failure(MEASURED_FLOOR, S_REF, mu)
        q = broken_fraction(t + t0, S_REF, mu)
        ax.semilogy(t, q, color=col, lw=3.0)
        TAGY[mu] = (col, f"$\\mu$ = $10^{{{int(np.log10(mu))}}}$")
        cross = time_to_failure(NIH, S_REF, mu) - t0
        ax.plot([cross], [NIH], "o", color=col, ms=9, zorder=5)

    ax.axhline(NIH, color=RED, lw=2.2, ls="--")
    # Both of these were struck through by a curve and pressed against a
    # spine. Shortened, pulled inboard, and plated.
    ax.text(5.6, NIH * 1.35, "NIH, $10^{-8}$  (QUOTED)", color=RED,
            ha="center", va="bottom", fontsize=LBL, bbox=_plate(), zorder=7)
    ax.axhline(MEASURED_FLOOR, color=INK, lw=1.8, ls=":")
    ax.text(5.6, MEASURED_FLOOR * 1.3, "measured, $10^{-8.6}$", color=INK,
            ha="center", va="bottom", fontsize=LBL, bbox=_plate(), zorder=7)

    ax.set_xlabel("generations of permissive growth after the assay",
                  fontsize=LBL)
    ax.set_ylabel("standing escape fraction", fontsize=LBL)
    ax.set_xlim(0, 12); ax.set_ylim(1e-9, 3e-7)
    ax.grid(True, which="both", color=RULE, lw=0.6)
    ax.set_title("$\\mu$ = $10^{-7}$, $10^{-8}$, $10^{-9}$ top to bottom;"
                 "   s = 0.05 (MODELLED)", fontsize=LBL, color=MUTED)
    _save(fig, name)


def fig_two_asymmetries(name="s23_two_asymmetries"):
    """The two questions have OPPOSITE sensitivities. This is the spine.

    How long the circuit lasts is driven by s. How long containment holds is
    driven by mu. Containment lives in the far-left tail, q ~ 1e-8, where
    selection has had nothing to amplify yet, so crossing the requirement is
    pure mutation accumulation.

    So burden reduction is the LONGEVITY lever and mutation-rate reduction is
    the CONTAINMENT lever, and they are not interchangeable.
    """
    # Shorter than the others because this one carries a figure-level key
    # under the panels; at 4.55 the saved height came to 4.66 in, past the
    # 4.60 in band, and the whole figure was scaled DOWN to fit -- which put
    # the body type at 19.8 pt, under the floor.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.20))

    ss = np.logspace(-2.4, -0.7, 120)
    mus = np.logspace(-9.4, -6.4, 120)

    def ret(s, mu):
        return time_to_failure(NIH, s, mu) - time_to_failure(MEASURED_FLOOR, s, mu)

    # THE TWO RATIOS ARE COMPUTED FROM THE CURVES, NOT TYPED IN.
    # They were literals -- "4.4x" and "80x" -- measured over sub-ranges
    # (s in [0.02, 0.1], mu in [1e-9, 1e-7]) that appear nowhere on the
    # axes. Over the ranges actually PLOTTED the curves move 37x and 574x,
    # so the slide the instructor calls the result he most wants them to
    # leave with was annotated eight times low, on panels whose axes the
    # room has just been trained to read. A number beside a computed curve
    # is computed from that curve or it drifts.
    tL = [time_to_failure(0.5, s, 1e-7) for s in ss]
    rL = [ret(s, 1e-7) for s in ss]
    axL.loglog(ss, tL, color=AMBER, lw=3.0,
               label="$t_{50}$  (circuit lifetime)")
    axL.loglog(ss, rL, color=TEAL, lw=3.0,
               label="retention  (containment)")
    # Markers, not sentences. These panels are 523 px wide and a sentence at
    # the body floor is 470-520 px, so there is no anchor in either panel
    # that misses the data. "4.4x" is 90 px and says the same thing.
    axL.set_xlabel("selection coefficient  $s$", fontsize=LBL)
    axL.set_ylabel("generations", fontsize=LBL)
    axL.set_title("vary $s$ at $\\mu = 10^{-7}$", fontsize=LBL, color=INK)
    axL.text(0.30, 0.88, f"$t_{{50}}$:  {max(tL) / min(tL):.0f}$\\times$",
             transform=axL.transAxes, color=AMBER,
             fontsize=LBL, ha="left", va="bottom", bbox=_plate(), zorder=7)
    axL.text(0.30, 0.07, "retention:  flat", transform=axL.transAxes,
             color=TEAL,
             fontsize=LBL, ha="left", va="bottom", bbox=_plate(), zorder=7)

    tR = [time_to_failure(0.5, S_REF, m) for m in mus]
    rR = [ret(S_REF, m) for m in mus]
    axR.loglog(mus, tR, color=AMBER, lw=3.0)
    axR.loglog(mus, rR, color=TEAL, lw=3.0)
    axR.set_xlabel("mutation rate  $\\mu$", fontsize=LBL)
    axR.set_title("vary $\\mu$ at $s = 0.05$", fontsize=LBL, color=INK)
    axR.text(0.03, 0.88, "flat", transform=axR.transAxes, color=AMBER,
             fontsize=LBL, ha="left", va="bottom", bbox=_plate(), zorder=7)
    axR.text(0.03, 0.07, f"{max(rR) / min(rR):.0f}$\\times$",
             transform=axR.transAxes, color=TEAL,
             fontsize=LBL, ha="left", va="bottom", bbox=_plate(), zorder=7)

    for ax in (axL, axR):
        ax.grid(True, which="both", color=RULE, lw=0.6)
        ax.set_ylim(1e-3, 1e4)
    # THE KEY IS GONE AND THE CURVES CARRY THEIR OWN NAMES.
    # The figure-level key sat at y = -0.03 and ran straight through both
    # x-axis labels: "retention (containment)" crossed "mutation rate mu"
    # closely enough that the axis label read as "mutation.rate" on the
    # built slide. figure_fit does not compare a figure-level legend with
    # axes text, so it scored this clean. Labelling curves rather than
    # keying them is the house habit anyway -- a key is one more box
    # competing for the same four inches.
    #
    # And "retention" is defined here rather than left to the reader. It
    # is NOT how long the circuit is retained, which is the other curve on
    # the same panel; it is how long the population stays under the NIH
    # line, which is why the fifth row of the close can ask for it as a
    # specification.
    # ONE PLATE PER CURVE, carrying the name AND the ratio. Two plates per
    # curve do not fit a 523 px panel -- the names collided with the
    # ratios and sat on the curve itself. The right panel keeps the bare
    # ratios: the colours are the same two curves one panel over.
    fig.suptitle("burden is the longevity lever; mutation rate is the "
                 "containment lever", fontsize=LBL, color=INK)
    _save(fig, name)


def fig_two_shapes(name="s23_two_shapes"):
    """THE SHAPE OF THE RESULT, before anything is priced.

    WHY IT EXISTS. The limits slide carried the structural claim of the
    hour -- failure time is LOGARITHMIC in the mutation rate and INVERSE
    in the cost -- as three rows of prose on a half-empty slide, and the
    next slide then priced the asymmetry with a bar chart. So the room
    met the number before it met the shape, which is backwards: the bar
    chart is persuasive only to someone who already knows why the two
    parameters cannot be traded off against each other.

    NO NUMBERS ON IT, DELIBERATELY. The ledger one click later owns the
    numbers (216, +46, +92, +189, +1487) and this figure would steal them.
    What it owns is the two shapes: a straight line against log mu, and a
    hyperbola against s. Two pictures, one sentence each.

    THE AXES ARE THE ARGUMENT. Left is semilog-x, so "logarithmic in mu"
    IS the straight line the room is looking at. Right is linear-linear,
    so "inverse in s" is the curve that runs away at small s. Putting
    either on the other's axes would hide exactly the thing it is for.
    """
    # 4.45 in tall, not 3.55: at 3.55 the 20 pt y-axis label did not fit
    # the figure and tight_layout clipped it, and the two sentences had
    # nowhere to sit that was not on a curve. The band is 4.60 in and the
    # slot is 10.2 in wide, so this is the largest the figure can be and
    # still place at scale 1.0 or better.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.0, 4.45))

    mus = np.logspace(-9, -5, 200)
    axL.semilogx(mus, [time_to_failure(0.5, S_REF, m) for m in mus],
                 color=TEAL, lw=3.0)
    axL.set_xlabel("mutation rate  $\\mu$   (log scale)", fontsize=LBL)
    axL.set_ylabel("generations to half broken", fontsize=LBL)
    axL.set_title(f"vary $\\mu$ at $s = {S_REF}$", fontsize=LBL, color=INK)
    # Bottom left: this curve falls from about 350 to about 170 across
    # the panel, so the empty quadrants are bottom-left and top-right.
    axL.text(0.03, 0.05, "straight against log $\\mu$",
             transform=axL.transAxes, color=TEAL, fontsize=LBL,
             ha="left", va="bottom", bbox=_plate(), zorder=7)

    ss = np.linspace(0.004, 0.10, 200)
    axR.plot(ss, [time_to_failure(0.5, v, MU_REF) for v in ss],
             color=AMBER, lw=3.0)
    axR.set_xlabel("selection coefficient  $s$", fontsize=LBL)
    axR.set_title(f"vary $s$ at $\\mu = 10^{{-6}}$", fontsize=LBL, color=INK)
    # Top right: this one hugs the left edge and the floor, so the whole
    # right-hand half above the curve is empty.
    axR.text(0.97, 0.68, "one over $s$", transform=axR.transAxes,
             color=AMBER, fontsize=LBL,
             ha="right", va="bottom", bbox=_plate(), zorder=7)

    for ax in (axL, axR):
        ax.grid(True, which="both", color=RULE, lw=0.6)
        ax.tick_params(labelsize=LBL)
    _save(fig, name)


FIGURES = [fig_confounded, fig_measure_s, fig_ledger, fig_retention,
           fig_two_asymmetries, fig_two_shapes]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
