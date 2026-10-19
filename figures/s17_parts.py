"""Session 17 figures — parts, context, and why composition is not composition.

Every number is COMPUTED here from the papers' own data, never typed in.
The terminator panel reads Cambray's supplementary table and recomputes the
per-class fit at render time, so the claim on the slide cannot drift from the
data behind it.

SIZE. matplotlib point sizes are ABSOLUTE and `decks/*.py::_fig()` places a
figure at width = pixels/dpi, so the scale is exactly 1.000: a point authored
here is a point on the wall. The 20pt floor in `posb-slide-legibility` has to
be met in this file. Nothing below 20 carries content.

LICENCE. This repo is public and CC BY 4.0. `decks/paper_figures.yaml` keeps
*images reproduced from papers* out of the tree, which is a different thing
from data: the terminator panel plots 54 (measured, predicted, class) triples
from the supplementary table of Cambray et al., NAR 2013 -- open access, and
Adam agreed on 18 October, as an author, that they may go out under CC BY 4.0.
So the data is committed at `figures/data/s17_cambray_terminators.csv` with its
provenance, the figure reads the CSV rather than the SI, and the whole thing
rebuilds and verifies from a clean clone. Regenerate the CSV with
`tools/extract_cambray_terminators.py` if the SI ever changes.

Run:  python tools/build_figures.py s17
"""
import os

import numpy as np

from posb.assembly import junction_identities, clash_probability
from figures.style import (use, TYPE, TEAL, CYAN, AMBER, GREEN, MUTED,
                           INK, RED, RULE)

plt = use()

OUT = "figures/build"
CAMBRAY_CSV = "figures/data/s17_cambray_terminators.csv"


# Slide is 13.333in wide with 0.7in margins (decks/theme.py), and `_fig()`
# places a figure at pixels/dpi, so anything wider than this runs off the
# slide. Measured after the save, because bbox="tight" decides the real size.
USABLE_IN = 13.333 - 2 * 0.7
BODY_IN = 4.65         # decks place a figure at y=1.95 and foot() defaults to
                       # y=6.75, so this is the real budget. It was 5.6 and
                       # four figures overlapped the foot -- invisibly, because
                       # the deck's overlap gate compares text shapes and this
                       # text is baked into a PNG.
DPI = 160
# savefig writes a tight bbox, which adds matplotlib's default 0.1in of pad
# on every side. A figure that computes its own height analytically has to
# subtract this or it clears its own budget and still fails in _save.
PAD_SAVE = 0.20


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    path = f"{OUT}/{name}.png"
    fig.savefig(path)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(path).size
    if w / DPI > USABLE_IN:
        raise AssertionError(
            f"{name}: {w / DPI:.2f}in wide, over the {USABLE_IN:.2f}in slide "
            f"column. Cut text or narrow the figure -- do not shrink the type.")
    if h / DPI > BODY_IN:
        raise AssertionError(
            f"{name}: {h / DPI:.2f}in tall, over the {BODY_IN:.2f}in band "
            f"left under a slide title. Cut rows -- do not shrink the type.")
    return w / DPI, h / DPI


def _cambray_table():
    """Measured and predicted termination efficiency, by functional class.

    Reads the committed CSV, so this figure rebuilds from a clean clone. The
    file is required -- a missing one is a broken repository, not a degraded
    build, and should fail loudly.
    """
    import pandas as pd
    d = pd.read_csv(CAMBRAY_CSV, comment="#")
    return d.rename(columns={"klass": "Type", "measured_te": "Mean TE Cell",
                             "predicted_te": "Predicted TE"})


# The five classes the SI actually contains. The paper, p. 5146: "predicted
# activities of LETs were highly overestimated, LFFTs also tended to be
# overestimated, whereas ETs were UNDERESTIMATED". An earlier version of this
# module said the model overestimates all three, dropped the fifth class
# entirely, and so showed 53 of 54 rows. Direction is now computed and shown,
# not asserted.
CLASSES = [
    ("terminator",         "curated",      TEAL,  "o"),
    ("terminator (ET)",    "extended",     CYAN,  "s"),
    ("terminator (LFFT)",  "low folding",  AMBER, "^"),
    ("terminator (LET)",   "low efficiency", RED, "D"),
    ("terminator (LFFT/ET)", "both",       MUTED, "v"),
]

# What the PAPER reports for its own model, p. 5146 and Fig. 5B. These are not
# reproducible from the SI's "Predicted TE" column -- recomputing from it gives
# r = 0.62 and 0.97 -- so the paper's numbers are quoted and the SI is used
# only for the per-terminator residuals, which are robust to that discrepancy.
CAMBRAY_FIT = {"curated_n": 31, "curated_r": 0.9, "curated_cv": 0.85,
               "full_n": 54, "full_r": 0.67, "full_cv": 0.61}


def fig_terminator_model():
    """Cambray's model against his own measurements, split by class.

    The teaching point is the split, not the scatter: the model is near-exact
    on the class its features were identified over and useless outside it. So
    predictability is a property of how tightly the class is drawn, which is
    the session's thesis stated where prediction WORKS.

    Layout: a square scatter beside a computed table. No row pitch is written
    down -- the table asks the current point size how tall a line is and
    pitches itself from that, per docs/lecture-design.md.
    """
    d = _cambray_table()
    FS = TYPE["body"]                      # 20pt, the content floor
    H = 4.42                               # figure height, inches
    fig = plt.figure(figsize=(11.6, H))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.12], wspace=0.08)
    ax = fig.add_subplot(gs[0, 0])
    tx = fig.add_subplot(gs[0, 1])
    tx.set_axis_off()
    tx.set_xlim(0, 1)
    tx.set_ylim(0, 1)
    tx.set_autoscale_on(False)

    ax.plot([0, 100], [0, 100], lw=1.4, color=RULE, zorder=1)
    ax.text(52, 46, "model exact", fontsize=TYPE["caption"], color=MUTED,
            ha="center", va="center", rotation=45,
            bbox=dict(fc="white", ec="none", pad=1.5))

    rows = []
    for key, label, colour, marker in CLASSES:
        g = d[d["Type"] == key]
        if g.empty:
            continue
        m = g["Mean TE Cell"].to_numpy()
        pr = g["Predicted TE"].to_numpy()
        # SIGNED, predicted minus measured: positive = the model overestimates
        med = float(np.median(pr - m))
        ax.scatter(pr, m, s=78, facecolor=colour, edgecolor="white",
                   linewidth=0.9, marker=marker, zorder=3)
        rows.append((label, colour, marker, len(g), med))

    ax.set_xlim(-2, 106)
    ax.set_ylim(-2, 106)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel("predicted TE  (%)")
    ax.set_ylabel("measured TE  (%)")
    ax.set_aspect("equal", adjustable="box")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    # --- the table: row pitch AND column x measured, never chosen ---------
    line_in = FS / 72.0 * 1.62              # point size -> inches, with lead
    step = line_in / H                      # -> axes fraction of this figure

    def _w(txt, weight=None):
        """Width of `txt` at the table font, as a fraction of the tx panel."""
        t = tx.text(0, -5, txt, fontsize=FS, weight=weight,
                    transform=tx.transAxes)
        fig.canvas.draw()
        bb = t.get_window_extent(fig.canvas.get_renderer())
        frac = bb.width / tx.get_window_extent().width
        t.remove()
        return frac

    LAB_X = 0.085                            # after the marker swatch
    GAP = _w("  ")
    col_n = LAB_X + max(_w(lbl) for lbl, *_ in rows) + GAP + _w("n")
    col_m = col_n + GAP + _w("error")
    if col_m > 1.0:                          # measured, so this can be checked
        raise AssertionError(
            f"table columns need {col_m:.2f} of the panel; shorten the labels")

    y = 0.96
    tx.text(0.00, y, "median predicted − measured",
            fontsize=FS, color=INK, va="top", weight="bold",
            transform=tx.transAxes)
    y -= step * 1.5
    for x, h in ((col_n, "n"), (col_m, "error")):
        tx.text(x, y, h, fontsize=FS, color=MUTED, va="top", ha="right",
                transform=tx.transAxes)
    y -= step * 1.05                         # clear the descenders
    tx.plot([0, col_m], [y, y], transform=tx.transAxes, color=RULE, lw=1.2)
    y -= step * 0.70
    for label, colour, marker, n, med in rows:
        tx.plot([0.015], [y - step * 0.30], transform=tx.transAxes,
                marker=marker, color=colour, markersize=10,
                markeredgecolor="white", markeredgewidth=0.9, clip_on=False)
        tx.text(LAB_X, y, label, fontsize=FS, color=INK, va="top",
                transform=tx.transAxes)
        tx.text(col_n, y, f"{n}", fontsize=FS, color=INK, va="top", ha="right",
                transform=tx.transAxes)
        tx.text(col_m, y, f"{med:+.0f}", fontsize=FS,
                color=RED if abs(med) > 20 else INK, va="top", ha="right",
                transform=tx.transAxes)
        y -= step
    y -= step * 0.35
    tx.plot([0, col_m], [y, y], transform=tx.transAxes, color=RULE, lw=1.2)

    if y - 0.5 * step < -0.02:
        raise AssertionError("table overflows its panel: lower FS or raise H")
    fig.subplots_adjust(left=0.085, right=0.985, top=0.97, bottom=0.145)
    _save(fig, "s17_terminator_model")
    return [(l, n, m) for l, _c, _mk, n, m in rows]


# Published summary statistics. These cannot be derived from anything in this
# repository, so they are typed -- once, here, each with the sentence it came
# from. Every use below reads these names; none re-types a number.
KOSURI = {                      # PNAS 110(34):14024-14029 (2013), ANOVA, Fig. 3
    "rna":     [("promoter", 92.0), ("RBS", 4.0), ("unexplained", 4.0)],
    "protein": [("promoter", 54.0), ("RBS", 30.0), ("unexplained", 16.7)],
}
CAMBRAY18 = {                   # Nat Biotechnol 36 (2018), nbt.4238
    # "design properties and first-order interactions could only explain 28%
    #  of PNI variance, suggesting that there are important factors that are
    #  not accounted for"
    "explained": 28.0,
    # "...(design error) represent 8% of the variance and vastly exceed the
    #  experimental error"
    "design_error": 8.0,
}


def fig_variance():
    """Where the variance in expression actually lives.

    Two decompositions, and they are NOT the same measurement. The top two
    partition variance across 114x111 part IDENTITIES. The bottom is variance
    explained by continuous sequence PROPERTIES in a different library, where
    the promoter and RBS were held fixed and a designed 96-nt window varied.
    An earlier version's docstring claimed "the figure says so" when the
    figure said nothing of the kind; the footnote now does.

    No legend: each bar's key is its own subtitle, with every category word in
    its segment's colour, placed by measuring the word that precedes it. That
    also stops the third bar's teal reading as "promoter" -- it has its own
    colour and says so on the line above.

    Layout note. Every height here is in inches and the axes is set so that
    one y-unit IS one inch, so type and geometry cannot drift apart. The
    previous version worked in a `line_in` that set_ylim then silently
    rescaled; the arithmetic happened to clear at a 16pt key, and the moment
    the key went to the 20pt content floor every title landed on the bar
    above it. A pitch that is a magic multiple of the font size is a pitch
    nobody measured.
    """
    FS = TYPE["body"]
    SUB = TYPE["body"]

    bars = [
        ("Kosuri 2013 · RNA level",
         [("promoter", 92.0, TEAL), ("RBS", 4.0, CYAN),
          ("unexplained", 4.0, RULE)]),
        ("Kosuri 2013 · protein level",
         [("promoter", 54.0, TEAL), ("RBS", 30.0, CYAN),
          ("unexplained", 16.7, RULE)]),
        ("Cambray 2018 · protein level  (a different library)",
         [("sequence features", CAMBRAY18["explained"], GREEN),
          ("unexplained", 100.0 - CAMBRAY18["explained"], RULE)]),
    ]
    FOOTNOTE = ("Top two: variance by part IDENTITY, 114×111 pairs.\n"
                "Bottom: variance by sequence PROPERTIES, promoter and RBS "
                "held fixed.")

    LINE = FS / 72.0 * 1.2              # one line box of the heading type
    KEY = SUB / 72.0 * 1.2
    BAR = 0.26
    PAD = 0.05                          # within a group
    GAP = 0.14                          # between groups
    FOOT_L = SUB / 72.0 * 1.4
    n_foot = FOOTNOTE.count("\n") + 1
    group_h = LINE + PAD + KEY + PAD + BAR
    H = (len(bars) * group_h + (len(bars) - 1) * GAP
         + 0.20 + n_foot * FOOT_L + 0.06)
    if H + PAD_SAVE > BODY_IN:
        raise AssertionError(
            f"fig_variance needs {H + PAD_SAVE:.2f}in on the slide, over the "
            f"{BODY_IN}in band. Cut a row or a footnote line -- do not "
            f"shrink the type.")

    fig = plt.figure(figsize=(10.9, H))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, H)
    ax.set_axis_off()
    ax.set_autoscale_on(False)

    def _wpts(txt, size, weight=None):
        """Width of `txt` in x-data units (the axis spans 0-100).

        The probe must carry the SAME weight as the string it is measuring.
        Measuring bold text with a regular probe under-reports the width,
        and the error grows with the string: "promoter" lost a point or two
        and nobody noticed, while "sequence features" swallowed the middot
        that follows it.
        """
        t = ax.text(0, H, txt, fontsize=size, weight=weight)
        fig.canvas.draw()
        w = t.get_window_extent(fig.canvas.get_renderer()).width
        t.remove()
        return 100.0 * w / ax.get_window_extent().width

    cur = H - 0.04
    for title, parts in bars:
        ax.text(0, cur, title, fontsize=FS, color=INK, va="top",
                weight="bold")
        cur -= LINE + PAD
        # the key: category words in their own colours, laid out by measurement
        x = 0.0
        sep = "   ·   "
        for i, (name, _v, c) in enumerate(parts):
            if i:
                ax.text(x, cur, sep, fontsize=SUB, color=MUTED, va="top")
                x += _wpts(sep, SUB)
            ax.text(x, cur, name, fontsize=SUB,
                    color=MUTED if c is RULE else c, va="top", weight="bold")
            x += _wpts(name, SUB, weight="bold")
        cur -= KEY + PAD
        # The paper prints 54 / 30 / 16.7, which sums to 100.7 -- two values
        # rounded and one not. Draw each segment as its share of the row's
        # own total so the bars align, and label what the paper says.
        total = sum(v for _n, v, _c in parts)
        left = 0.0
        for name, v, c in parts:
            w = 100.0 * v / total
            ax.barh(cur - BAR / 2, w, left=left, height=BAR,
                    color=c, edgecolor="white", linewidth=1.2, zorder=3)
            if w >= 9:
                ax.text(left + w / 2, cur - BAR / 2, f"{v:g}%",
                        fontsize=FS, color=MUTED if c is RULE else "white",
                        ha="center", va="center", zorder=4)
            left += w
        cur -= BAR + GAP

    cur += GAP - 0.26
    ax.text(0, cur, FOOTNOTE, fontsize=SUB, color=MUTED, va="top",
            linespacing=1.4)

    _save(fig, "s17_variance")
    return [(t, [v for _n, v, _c in p]) for t, p in bars]

MUTALIK = {                     # Nat Methods (2013), nmeth.2404
    # "We studied all combinations of curated elements, demonstrating that
    #  arbitrary genes are reliably expressed to within twofold relative
    #  target expression windows with ~93% reliability", over elements
    #  "across a 1,000-fold observed dynamic range"
    "within_twofold": 93.0,
    "dynamic_range": 1000,
    # The baseline in the SAME paper's own introduction, at the SAME metric
    # and the SAME tolerance, which is the only reason the two bars may sit
    # on one axis: "For example, the best available computational tool for
    # designing context-optimized translation control elements for use in
    # E. coli gives an ~47% chance to design elements that express proteins
    # to within twofold of a target expression level[10]." Reference 10 is
    # Salis, Mirsky & Voigt, Nat Biotechnol 27:946-950 (2009) -- the RBS
    # Calculator. An earlier draft compared the 93% against Kosuri's 64%,
    # which is a different measurement entirely.
    "predicted_within_twofold": 47.0,
}

KOSURI_WITHIN_2X = {            # PNAS 110(34):14024-14029 (2013)
    # "80% of RNA levels and 64% of protein levels fell within twofold of
    #  prediction"; "the worst 5% of protein deviations were off by 13-fold
    #  on average"
    "protein": 64.0,
    "rna": 80.0,
    "worst5_fold": 13,
}


def fig_manufacture():
    """What manufacturing the parts buys, in ONE metric measured ONE way.

    An earlier version of this figure put Kosuri's 64% beside Mutalik's 93%
    and carried a caveat saying they are different measurements -- prediction
    accuracy against hitting a target window. True, and a caveat is a poor
    substitute for the right comparison. Mutalik's own introduction supplies
    it: the best available computational tool gives ~47% within twofold of a
    target, against their ~93%. Same question, same tolerance, same authors,
    same paper. Kosuri's 64% stays in fig_variance, answering its own.

    Layout in true inches, for the reason given in fig_variance: the row
    pitch used to be a multiple of the font size that set_ylim then rescaled,
    so raising the sub-line to the 20pt content floor put it against the next
    row's title.
    """
    FS = TYPE["body"]
    SUB = TYPE["body"]

    rows = [
        ("designed with the best predictor",
         "the computational tool, as Mutalik et al. report it:\n"
         "chance of landing within 2× of a target level",
         MUTALIK["predicted_within_twofold"], TEAL),
        ("built from manufactured elements",
         "the same question, the same tolerance, same paper:\n"
         f"elements spanning {MUTALIK['dynamic_range']:,}-fold",
         MUTALIK["within_twofold"], GREEN),
    ]

    LINE = FS / 72.0 * 1.2
    SUBL = SUB / 72.0 * 1.45
    BAR = 0.34
    PAD = 0.07
    GAP = 0.24
    n_sub = max(sub.count("\n") + 1 for _l, sub, *_ in rows)
    row_h = LINE + PAD + BAR + PAD + n_sub * SUBL
    H = len(rows) * row_h + (len(rows) - 1) * GAP + 0.08
    if H + PAD_SAVE > BODY_IN:
        raise AssertionError(
            f"fig_manufacture needs {H + PAD_SAVE:.2f}in on the slide, over "
            f"the {BODY_IN}in band -- do not shrink the type.")

    fig = plt.figure(figsize=(10.4, H))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, H)
    ax.set_axis_off()
    ax.set_autoscale_on(False)

    cur = H - 0.04
    for label, sub, v, c in rows:
        ax.text(0, cur, label, fontsize=FS, color=INK, va="top",
                weight="bold")
        cur -= LINE + PAD
        ax.barh(cur - BAR / 2, 100, left=0, height=BAR,
                color=RULE, edgecolor="white", linewidth=1.2, zorder=2)
        ax.barh(cur - BAR / 2, v, left=0, height=BAR,
                color=c, edgecolor="white", linewidth=1.2, zorder=3)
        ax.text(v - 1.2, cur - BAR / 2, f"{v:g}%", fontsize=FS, color="white",
                ha="right", va="center", zorder=4)
        cur -= BAR + PAD
        ax.text(0, cur, sub, fontsize=SUB, color=MUTED, va="top",
                linespacing=1.45)
        cur -= n_sub * SUBL + GAP

    _save(fig, "s17_manufacture")
    return [(l, v) for l, _s, v, _c in rows]

INSULATORS = [
    # move, layer, what it removes
    ("spacer, 100–1000 bp", "DNA", "nothing — it failed"),
    ("insulated promoter", "DNA", "upstream DNA"),
    ("RNA cleavage, Csy4", "RNA", "the promoter's 5′UTR"),
    ("ribozyme, RiboJ", "RNA", "the same, self-cleaving"),
    ("common start + BCD", "design", "both, by construction"),
]


def fig_insulators():
    """Insulation is a device, not a distance.

    The first row is the one that earns the slide: putting space between two
    parts does not separate them. Every move that works replaces the junction
    with something that defines it.
    """
    FS = TYPE["body"]
    H = 4.35
    fig, ax = plt.subplots(figsize=(11.2, H))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_autoscale_on(False)

    def _w(txt, weight=None):
        t = ax.text(0, -5, txt, fontsize=FS, weight=weight,
                    transform=ax.transAxes)
        fig.canvas.draw()
        f = t.get_window_extent(fig.canvas.get_renderer()).width / \
            ax.get_window_extent().width
        t.remove()
        return f

    line_in = FS / 72.0 * 1.62
    step = line_in / H
    GAP = _w("    ")
    c_move = 0.0
    c_layer = c_move + max(_w(m) for m, *_ in INSULATORS) + GAP
    c_what = c_layer + max(_w(l) for _m, l, _w2 in INSULATORS) + GAP
    end = c_what + max(_w(w) for *_x, w in INSULATORS)
    if end > 1.0:
        raise AssertionError(f"insulator table needs {end:.2f} of the width")

    y = 0.95
    for h, x in (("move", c_move), ("layer", c_layer),
                 ("what it removes", c_what)):
        ax.text(x, y, h, fontsize=FS, color=MUTED, va="top",
                transform=ax.transAxes)
    y -= step * 1.05
    ax.plot([0, end], [y, y], transform=ax.transAxes, color=RULE, lw=1.2)
    y -= step * 0.75
    for move, layer, what in INSULATORS:
        failed = "failed" in what
        ax.text(c_move, y, move, fontsize=FS, va="top",
                color=MUTED if failed else INK, transform=ax.transAxes)
        ax.text(c_layer, y, layer, fontsize=FS, color=MUTED, va="top",
                transform=ax.transAxes)
        ax.text(c_what, y, what, fontsize=FS, va="top",
                color=RED if failed else INK, transform=ax.transAxes)
        y -= step * 1.02
    y -= step * 0.20
    ax.plot([0, end], [y, y], transform=ax.transAxes, color=RULE, lw=1.2)
    y -= step * 0.95
    ax.text(0, y, "Insulation is a device, not a distance.",
            fontsize=FS, color=INK, va="top", weight="bold",
            transform=ax.transAxes)
    if y - step < -0.02:
        raise AssertionError("insulator table overflows; cut a row")

    fig.subplots_adjust(left=0.012, right=0.995, top=0.99, bottom=0.015)
    _save(fig, "s17_insulators")
    return INSULATORS


# --- T44: Golden Gate overhangs ------------------------------------------
# The counting and the clash proxy live in posb.assembly, not here: they are
# student-facing science that PS7 calls, and a figure generator is the wrong
# home for them. This module only draws them.


def fig_overhangs():
    """How many parts fit in one pot before two junctions look alike.

    T44. The counting is exact; the clash curve is an explicitly crude proxy
    for misligation, which in practice is measured rather than derived.
    """
    FS = TYPE["body"]
    H = 4.15          # 3.70 did not leave room for the model note at 20pt
    all_o, pal, classes = junction_identities()
    ks = list(range(2, 21))
    ps = [clash_probability(k) for k in ks]

    fig = plt.figure(figsize=(11.4, H))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.80], wspace=0.10)
    ax = fig.add_subplot(gs[0, 0])
    tx = fig.add_subplot(gs[0, 1])
    tx.set_axis_off()
    tx.set_xlim(0, 1)
    tx.set_ylim(0, 1)
    tx.set_autoscale_on(False)

    ax.plot(ks, [100 * p for p in ps], lw=3.0, color=TEAL, zorder=3)
    ax.scatter(ks, [100 * p for p in ps], s=40, color=TEAL, zorder=4,
               edgecolor="white", linewidth=0.8)
    ax.axhline(50, color=RULE, lw=1.4, zorder=1)
    # Interpolate the actual 50% crossing. Marking the first sampled k with
    # p >= 0.5 put the line at 5, where the curve is already at 64% -- "even
    # odds" pointing two-thirds of the way up a chart the room can see.
    half = None
    for (k0, p0), (k1, p1) in zip(zip(ks, ps), zip(ks[1:], ps[1:])):
        if p0 < 0.5 <= p1:
            half = k0 + (0.5 - p0) / (p1 - p0) * (k1 - k0)
            break
    if half:
        ax.axvline(half, color=RED, lw=1.6, ls=(0, (4, 3)), zorder=2)
        ax.text(half + 0.35, 17, f"even odds\nat {half:.1f} junctions",
                fontsize=FS, color=RED, va="center", linespacing=1.4)
    ax.set_xlabel("junctions chosen at random")
    ax.set_ylabel("chance of a clash  (%)")
    ax.set_xlim(2, 20)
    ax.set_ylim(0, 100)
    ax.set_xticks([2, 5, 10, 15, 20])
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    line_in = FS / 72.0 * 1.62
    step = line_in / H
    y = 0.95
    facts = [
        ("4-nt overhangs", f"{len(all_o)}"),
        ("palindromic, self-ligating", f"{len(pal)}"),
        ("usable junction identities", f"{len(classes)}"),
    ]
    tx.text(0.0, y, "the counting, exactly", fontsize=FS, color=INK,
            va="top", weight="bold", transform=tx.transAxes)
    y -= step * 1.45
    for lab, val in facts:
        tx.text(0.0, y, lab, fontsize=FS, color=INK, va="top",
                transform=tx.transAxes)
        tx.text(1.0, y, val, fontsize=FS, color=TEAL, va="top", ha="right",
                weight="bold", transform=tx.transAxes)
        y -= step * 1.12
    y -= step * 0.30
    tx.plot([0, 1], [y, y], transform=tx.transAxes, color=RULE, lw=1.2)
    y -= step * 1.0
    # This defines the number students read off the curve, so it sits at the
    # content floor like everything else -- which means it has to be narrow
    # enough for the right-hand panel, not merely short enough to fit on two
    # lines at 16pt. _save bounds the figure on a tight bbox, so an overlong
    # line here widens the whole figure past the slide column.
    cap = ("Toy model: clash = within\n"
           "one base of each other\n"
           "or of the reverse complement.")
    tx.text(0.0, y, cap, fontsize=TYPE["body"], color=MUTED, va="top",
            linespacing=1.4, transform=tx.transAxes)
    cap_h = (cap.count("\n") + 1) * (TYPE["body"] / 72.0 * 1.4) / H
    if y - cap_h < -0.02:
        raise AssertionError(
            f"overhang panel overflows by {cap_h - y - 0.02:.3f} of its "
            f"height; cut a line or raise H")

    fig.subplots_adjust(left=0.085, right=0.99, top=0.97, bottom=0.145)

    # A rotated y-label longer than its own axis gets its tail cut off, and
    # nothing else in the build notices: the figure is still the right size,
    # the words are just not all there. "chance two junctions clash (%)" at
    # 20pt wanted 3.75in of a 3.42in axis.
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    lab = ax.yaxis.label.get_window_extent(r).height
    if lab > ax.get_window_extent().height:
        raise AssertionError(
            f"y-label needs {lab / fig.dpi:.2f}in of a "
            f"{ax.get_window_extent().height / fig.dpi:.2f}in axis; shorten "
            f"it -- do not shrink the type.")
    _save(fig, "s17_overhangs")
    return {"all": len(all_o), "palindromic": len(pal),
            "usable": len(classes), "half_clash_at": half}


def fig_compositor():
    """T42 — what the compositor abstraction actually changes.

    Left: the parts-list picture, two objects each carrying a number, and
    composition as multiplication. Right: a part as a PROCESS reading and
    writing shared state variables, which is the only picture in which the
    reciprocity of segment 1 is even expressible.
    """
    FS = TYPE["body"]
    SUB = TYPE["body"]
    H = 3.95
    fig, axes = plt.subplots(1, 2, figsize=(11.3, H))
    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()
        ax.set_autoscale_on(False)

    def box(ax, x, y, w, h, label, colour, sub=None):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor="white",
                                   edgecolor=colour, linewidth=2.4, zorder=3))
        ax.text(x + w / 2, y + h / 2 + (0.035 if sub else 0), label,
                fontsize=FS, color=INK, ha="center", va="center", zorder=4)
        if sub:
            ax.text(x + w / 2, y + h / 2 - 0.055, sub, fontsize=SUB,
                    color=MUTED, ha="center", va="center", zorder=4)

    def arrow(ax, x0, y0, x1, y1, colour=MUTED, style="-|>"):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle=style, color=colour, lw=2.2))

    # ---- left: the parts list ------------------------------------------
    a = axes[0]
    a.text(0.0, 0.95, "the parts list", fontsize=FS, color=INK,
           va="top", weight="bold")
    a.text(0.0, 0.855, "each part owns a number", fontsize=SUB, color=MUTED,
           va="top")
    box(a, 0.03, 0.52, 0.40, 0.19, "promoter", TEAL, "strength  p")
    box(a, 0.57, 0.52, 0.40, 0.19, "RBS", CYAN, "efficiency  r")
    arrow(a, 0.44, 0.615, 0.56, 0.615)
    a.text(0.5, 0.36, "protein  =  p × r", fontsize=FS, color=INK,
           ha="center", va="center")
    a.text(0.5, 0.20, "Composition combines behaviours\nand leaves p and r alone.",
           fontsize=SUB, color=MUTED, ha="center", va="center",
           linespacing=1.45)

    # ---- right: the compositor -----------------------------------------
    b = axes[1]
    b.text(0.0, 0.95, "the compositor", fontsize=FS, color=INK,
           va="top", weight="bold")
    b.text(0.0, 0.855, "each part is a process over shared state",
           fontsize=SUB, color=MUTED, va="top")
    box(b, 0.33, 0.56, 0.34, 0.19, "part", GREEN, "a reaction")
    # inputs it reads
    b.text(0.01, 0.705, "RNAP", fontsize=SUB, color=MUTED, va="center")
    b.text(0.01, 0.605, "5′UTR", fontsize=SUB, color=MUTED, va="center")
    arrow(b, 0.17, 0.705, 0.32, 0.705, TEAL)
    arrow(b, 0.17, 0.605, 0.32, 0.605, TEAL)
    # outputs it writes
    # left-anchored at a common x so both arrows are the same length and
    # neither label butts up against its own arrowhead
    b.text(0.775, 0.705, "transcript", fontsize=SUB, color=MUTED,
           ha="left", va="center")
    b.text(0.775, 0.605, "5′UTR", fontsize=SUB, color=MUTED,
           ha="left", va="center")
    arrow(b, 0.68, 0.705, 0.755, 0.705, GREEN)
    arrow(b, 0.68, 0.605, 0.755, 0.605, GREEN)
    # the loop: the 5'UTR it writes is the 5'UTR it reads. Routed UNDER the
    # box, because an arrow through the box reads as flow, not feedback.
    LOOP = dict(x0=0.94, y0=0.515, x1=0.06, y1=0.515, rad=-0.18)
    b.annotate("", xy=(LOOP["x1"], LOOP["y1"]),
               xytext=(LOOP["x0"], LOOP["y0"]),
               arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4,
                               connectionstyle=f"arc3,rad={LOOP['rad']}",
                               shrinkA=2, shrinkB=2))
    loop_caption = b.text(0.5, 0.325,
                          "the 5′UTR it writes is the 5′UTR it reads",
                          fontsize=SUB, color=RED, ha="center", va="center")
    b.text(0.5, 0.145, "The only picture in which\n"
                      "“joining changes both” can be said.",
           fontsize=SUB, color=MUTED, ha="center", va="center",
           linespacing=1.45)

    fig.subplots_adjust(left=0.015, right=0.985, top=0.98, bottom=0.02,
                        wspace=0.10)

    # How far the feedback arc dips is not something to guess at. matplotlib
    # builds arc3 as a quadratic Bezier whose control point is the chord's
    # midpoint displaced perpendicular by rad x |chord|, IN DISPLAY SPACE --
    # so the dip in axes fractions depends on the panel's aspect, and two
    # successive hand-nudges still left the arc struck through its own
    # caption. Sample the curve and compare.
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    (px0, py0), (px1, py1) = b.transAxes.transform(
        [(LOOP["x0"], LOOP["y0"]), (LOOP["x1"], LOOP["y1"])])
    dx, dy = px1 - px0, py1 - py0
    cx = (px0 + px1) / 2.0 + LOOP["rad"] * dy
    cy = (py0 + py1) / 2.0 - LOOP["rad"] * dx
    ts = [i / 200.0 for i in range(201)]
    arc_low = min((1 - t) ** 2 * py0 + 2 * (1 - t) * t * cy + t ** 2 * py1
                  for t in ts)
    cap_top = loop_caption.get_window_extent(r).y1
    if arc_low < cap_top + 4:
        raise AssertionError(
            f"the feedback arc dips to {arc_low:.0f}px and its caption tops "
            f"out at {cap_top:.0f}px -- the arrow crosses the words. Lower "
            f"the caption or flatten rad.")
    _save(fig, "s17_compositor")
    return "compositor"


def fig_type2s():
    """What a Type IIS enzyme does, and why it gives you a CHOSEN junction.

    The point students must see before any overhang arithmetic: the enzyme
    recognises one sequence and cuts at a fixed offset OUTSIDE it, so the
    recognition site leaves with the scrap and the four bases left behind in
    the join are bases the designer picked. Freedom and trap in one move.

    BsaI is GGTCTC(1/5): the top strand breaks one base past the site, the
    bottom strand five bases past it. That is ONE cut, staggered, and the
    drawing has to show it as one -- an earlier version drew two full-height
    dashed lines, which reads as two blunt double-strand cuts, and left the
    scrap blunt so the complementary sticky end was nowhere on the slide.
    Every string here is argument rather than a source line, so it sits at
    the module's 20pt content floor, and each one is measured against the
    column it lives in instead of eyeballed.
    """
    FS = TYPE["body"]
    SUB = TYPE["body"]
    H = 4.55
    fig, ax = plt.subplots(figsize=(11.3, H))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    ax.set_autoscale_on(False)

    GUTTER = 0.615                      # the rule between the two columns
    checks = []                         # (artist, lo, hi) in axes fraction

    def T(*args, span=None, **kw):
        t = ax.text(*args, **kw)
        if span:
            checks.append((t, span[0], span[1]))
        return t

    def strand(y, x0, x1, colour, lw=9):
        ax.plot([x0, x1], [y, y], color=colour, lw=lw, solid_capstyle="butt",
                zorder=2)

    # --- before the cut --------------------------------------------------
    T(0.0, 0.95, "before", fontsize=FS, color=INK, va="top", weight="bold")
    yT, yB = 0.74, 0.675
    strand(yT, 0.02, 0.30, MUTED)
    strand(yB, 0.02, 0.30, MUTED)
    T(0.16, 0.655, "GGTCTC N", fontsize=SUB, color=INK, ha="center",
      va="top", span=(0.0, 0.30))
    strand(yT, 0.30, 0.355, AMBER)
    strand(yB, 0.30, 0.355, AMBER)
    strand(yT, 0.355, 0.56, TEAL)
    strand(yB, 0.355, 0.56, TEAL)
    T(0.4575, 0.655, "your part", fontsize=SUB, color=TEAL, ha="center",
      va="top", span=(0.36, GUTTER))

    # ONE staggered cut: top strand severed at 0.30, bottom at 0.355, with
    # the break stepping between them through the duplex.
    mid = (yT + yB) / 2.0
    ax.plot([0.30, 0.30, 0.355, 0.355],
            [yT + 0.040, mid, mid, yB - 0.040],
            color=RED, lw=2.4, solid_capstyle="round", zorder=5)
    T(0.3275, 0.845, "one cut, staggered", fontsize=SUB, color=RED,
      ha="center", va="bottom", span=(0.0, GUTTER))
    ax.annotate("", xy=(0.355, 0.545), xytext=(0.30, 0.545),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.8))
    T(0.3275, 0.515, "four bases offset, outside its own site",
      fontsize=SUB, color=RED, ha="center", va="top", span=(0.0, GUTTER))

    # --- after the cut ---------------------------------------------------
    T(0.0, 0.445, "after", fontsize=FS, color=INK, va="top", weight="bold")
    yT2, yB2 = 0.235, 0.172
    # scrap: bottom strand runs past the top one, so it ends sticky too
    strand(yT2, 0.02, 0.205, RULE)
    strand(yB2, 0.02, 0.205, RULE)
    strand(yB2, 0.205, 0.26, AMBER)
    # part: top strand runs past the bottom one -- the 5' overhang
    strand(yT2, 0.33, 0.385, AMBER)
    strand(yT2, 0.385, 0.59, TEAL)
    strand(yB2, 0.385, 0.59, TEAL)
    T(0.11, 0.305, "scrap", fontsize=SUB, color=MUTED, ha="center",
      va="bottom", span=(0.0, 0.29))
    T(0.49, 0.305, "your part", fontsize=SUB, color=TEAL, ha="center",
      va="bottom", span=(0.30, GUTTER))
    # the two amber stubs face each other on the drawing, so the fact that
    # they are complementary does not need saying; where the site WENT does.
    T(0.02, 0.105, "the recognition site left with the scrap",
      fontsize=SUB, color=MUTED, va="top", span=(0.0, GUTTER))

    # --- the consequence, right-hand column ------------------------------
    ax.plot([GUTTER, GUTTER], [0.03, 0.97], color=RULE, lw=1.4)
    T(0.655, 0.95, "the junction is yours", fontsize=FS, color=INK,
      va="top", weight="bold", span=(0.65, 1.0))
    for i, (lab, body) in enumerate([
            ("the freedom",
             "four bases you choose,\nso parts fit one way,\nall in one pot"),
            ("the trap",
             "the cell still reads\nthose four bases\nas sequence"),
    ]):
        y = 0.79 - i * 0.39
        T(0.655, y, lab, fontsize=SUB, color=AMBER if i else TEAL,
          va="top", weight="bold", span=(0.65, 1.0))
        T(0.655, y - 0.085, body, fontsize=SUB, color=INK, va="top",
          linespacing=1.5, span=(0.65, 1.0))

    fig.subplots_adjust(left=0.012, right=0.99, top=0.98, bottom=0.02)

    # Measure, never choose: every string must sit inside the column it was
    # placed in, or the build fails here rather than on the wall.
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    axb = ax.get_window_extent()
    bad = []
    boxes = []
    for t, lo, hi in checks:
        e = t.get_window_extent(r)
        x0 = (e.x0 - axb.x0) / axb.width
        x1 = (e.x1 - axb.x0) / axb.width
        if x0 < lo - 1e-3 or x1 > hi + 1e-3:
            bad.append(f"  {t.get_text()[:38]!r} spans "
                       f"{x0:.3f}..{x1:.3f}, allowed {lo:.3f}..{hi:.3f}")
        boxes.append((t, e))
    # ...and no two of them may share space. The first 20pt pass put "after"
    # on the same baseline as "scrap", and on the wall they read as one
    # phrase; a column check alone cannot see that.
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (ta, a), (tb, b) = boxes[i], boxes[j]
            if a.x0 < b.x1 and b.x0 < a.x1 and a.y0 < b.y1 and b.y0 < a.y1:
                bad.append(f"  {ta.get_text()[:26]!r} overlaps "
                           f"{tb.get_text()[:26]!r}")
    if bad:
        raise AssertionError("s17_type2s layout:\n" + "\n".join(bad))
    _save(fig, "s17_type2s")
    return "type2s"

def fig_standard():
    """The set the field uses fails the rule we just taught -- and works.

    The honest comparison here is NOT two numbers on one axis. The clash curve
    in fig_overhangs is P(some pair in a randomly chosen set is within one
    base); NEB's 93% is the fraction of nine-fragment assemblies that come out
    correct. Those are different quantities and plotting them together would
    be the same apples-to-oranges error the 64%-vs-93% draft made. What can be
    compared is a RULE'S VERDICT against a MEASURED OUTCOME, so that is what
    this figure shows: apply the two-base rule to the published set, watch it
    reject the set, then read the assay.
    """
    from posb.assembly import STANDARD_SETS, distance, revcomp

    FS = TYPE["body"]
    SET = STANDARD_SETS["moclo_L1"]
    ohs = SET["overhangs"]
    bad = [(x, y) for i, x in enumerate(ohs) for y in ohs[i + 1:]
           if distance(x, y) < 2]
    if len(bad) != 1:
        raise AssertionError(
            f"this figure is drawn around a single offending pair; the set "
            f"now has {len(bad)}: {bad}")
    (A, B) = bad[0]
    RC = revcomp(B)
    direct = sum(p != q for p, q in zip(A, B))
    viarc = sum(p != q for p, q in zip(A, RC))

    LINE = FS / 72.0 * 1.2
    CHIP_H = 0.42
    BOX_H = 0.94
    H = (0.06 + LINE + 0.10 + CHIP_H + 0.34 + 2 * LINE + 0.30
         + BOX_H + 0.26 + LINE + 0.06)
    if H + PAD_SAVE > BODY_IN:
        raise AssertionError(f"fig_standard needs {H + PAD_SAVE:.2f}in")

    W = 11.3
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_axis_off()
    ax.set_autoscale_on(False)
    r = fig.canvas.get_renderer()

    def wid(txt, size=FS, weight=None, family=None):
        """Width of a string in INCHES, measured, never guessed."""
        t = ax.text(0, 0, txt, fontsize=size, weight=weight, family=family)
        fig.canvas.draw()
        w = t.get_window_extent(fig.canvas.get_renderer()).width / fig.dpi
        t.remove()
        return w

    MONO = "DejaVu Sans Mono"
    cur = H - 0.06

    # --- the published set, as chips ------------------------------------
    ax.text(0.0, cur, "MoClo Level 1 — the nine junctions the field ships",
            fontsize=FS, color=MUTED, va="top")
    cur -= LINE + 0.10

    pad, gap = 0.13, 0.14
    widths = [wid(o, weight="bold", family=MONO) + 2 * pad for o in ohs]
    x = 0.0
    for o, w in zip(ohs, widths):
        flagged = o in (A, B)
        ax.add_patch(plt.Rectangle(
            (x, cur - CHIP_H), w, CHIP_H,
            facecolor="white" if flagged else "#F2F6F5",
            edgecolor=RED if flagged else RULE,
            linewidth=2.4 if flagged else 1.2, zorder=2))
        ax.text(x + w / 2, cur - CHIP_H / 2, o, fontsize=FS, family=MONO,
                color=RED if flagged else INK, weight="bold",
                ha="center", va="center", zorder=3)
        x += w + gap
    if x - gap > W:
        raise AssertionError(f"chips need {x - gap:.2f}in of {W}in")
    cur -= CHIP_H + 0.34

    # --- the arithmetic ---------------------------------------------------
    rows = [
        (f"{A}  vs  {B}", direct, "compared directly", MUTED),
        (f"{A}  vs  {RC}", viarc,
         f"{RC} is the reverse complement of {B}", RED),
    ]
    # Columns are set by the widest entry in each, so the two rows align and
    # the one-base row sits directly under the four-base row it overturns.
    c1 = max(wid(t, family=MONO, weight="bold") for t, *_ in rows) + 0.45
    c2 = max(wid(f"{n} difference{'s' if n != 1 else ''}", weight="bold")
             for _t, n, *_ in rows) + 0.38
    for txt, n, verdict, colour in rows:
        ax.text(0.0, cur, txt, fontsize=FS, family=MONO, color=colour,
                va="top", weight="bold")
        ax.text(c1, cur, f"{n} difference{'s' if n != 1 else ''}",
                fontsize=FS, color=colour, va="top", weight="bold")
        ax.text(c1 + c2, cur, verdict, fontsize=FS, color=colour, va="top")
        end = c1 + c2 + wid(verdict)
        if end > W:
            raise AssertionError(f"arithmetic row needs {end:.2f}in of {W}in")
        cur -= LINE
    cur -= 0.30

    # --- verdict against measurement -------------------------------------
    bw = (W - 0.40) / 2.0
    for i, (head, body, colour) in enumerate((
            ("your rule says", "reject this set", RED),
            ("the assay says", f"{SET['fidelity']:.0%} correct, all nine",
             GREEN))):
        bx = i * (bw + 0.40)
        ax.add_patch(plt.Rectangle((bx, cur - BOX_H), bw, BOX_H,
                                   facecolor="white", edgecolor=colour,
                                   linewidth=2.4, zorder=2))
        ax.text(bx + 0.22, cur - 0.20, head, fontsize=FS, color=MUTED,
                va="top", zorder=3)
        ax.text(bx + 0.22, cur - 0.20 - LINE * 0.95, body, fontsize=FS,
                color=colour, weight="bold", va="top", zorder=3)
        if wid(body, weight="bold") + 0.44 > bw:
            raise AssertionError(f"box text overflows: {body!r}")
    cur -= BOX_H + 0.26

    ax.text(0.0, cur,
            "How much similarity a ligase tolerates is measured, not counted.",
            fontsize=FS, color=INK, weight="bold", va="top")

    _save(fig, "s17_standard")
    return {"pair": (A, B), "revcomp": RC, "direct": direct, "via_rc": viarc,
            "fidelity": SET["fidelity"]}

FIGURES = [fig_terminator_model, fig_variance,
           fig_manufacture, fig_insulators, fig_type2s,
           fig_overhangs, fig_standard, fig_compositor]

if __name__ == "__main__":
    for f in FIGURES:
        out = f()
        print(f.__name__, "->", out)
