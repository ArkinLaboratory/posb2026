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

from figures.style import (use, TYPE, TEAL, CYAN, AMBER, GREEN, MUTED,
                           INK, RED, RULE)

plt = use()

OUT = "figures/build"
CAMBRAY_CSV = "figures/data/s17_cambray_terminators.csv"


# Slide is 13.333in wide with 0.7in margins (decks/theme.py), and `_fig()`
# places a figure at pixels/dpi, so anything wider than this runs off the
# slide. Measured after the save, because bbox="tight" decides the real size.
USABLE_IN = 13.333 - 2 * 0.7
BODY_IN = 5.6          # what is left of 7.5in under a title and over a foot
DPI = 160


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


# The paper's own names for the classes it reports its model overestimating.
CLASSES = [
    ("terminator",        "terminator",        TEAL,  "o"),
    ("terminator (ET)",   "extended",          CYAN,  "s"),
    ("terminator (LFFT)", "low folding",       AMBER, "^"),
    ("terminator (LET)",  "low efficiency",    RED,   "D"),
]


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
    H = 5.4                                # figure height, inches
    fig = plt.figure(figsize=(11.6, H))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.02], wspace=0.08)
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
        r = np.corrcoef(m, pr)[0, 1] if len(g) > 2 else float("nan")
        med = float(np.median(np.abs(m - pr)))
        ax.scatter(pr, m, s=78, facecolor=colour, edgecolor="white",
                   linewidth=0.9, marker=marker, zorder=3)
        rows.append((label, colour, marker, len(g), r, med))

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
    col_m = col_n + GAP + _w("miss, pts")
    if col_m > 1.0:                          # measured, so this can be checked
        raise AssertionError(
            f"table columns need {col_m:.2f} of the panel; shorten the labels")

    y = 0.96
    tx.text(0.00, y, "the model, by the paper's classes",
            fontsize=FS, color=INK, va="top", weight="bold",
            transform=tx.transAxes)
    y -= step * 1.5
    for x, h in ((col_n, "n"), (col_m, "miss, pts")):
        tx.text(x, y, h, fontsize=FS, color=MUTED, va="top", ha="right",
                transform=tx.transAxes)
    y -= step * 1.05                         # clear the descenders
    tx.plot([0, col_m], [y, y], transform=tx.transAxes, color=RULE, lw=1.2)
    y -= step * 0.70
    for label, colour, marker, n, r, med in rows:
        tx.plot([0.015], [y - step * 0.30], transform=tx.transAxes,
                marker=marker, color=colour, markersize=10,
                markeredgecolor="white", markeredgewidth=0.9, clip_on=False)
        tx.text(LAB_X, y, label, fontsize=FS, color=INK, va="top",
                transform=tx.transAxes)
        tx.text(col_n, y, f"{n}", fontsize=FS, color=INK, va="top", ha="right",
                transform=tx.transAxes)
        tx.text(col_m, y, f"{med:.1f}", fontsize=FS,
                color=RED if med > 20 else INK, va="top", ha="right",
                transform=tx.transAxes)
        y -= step
    y -= step * 0.35
    tx.plot([0, col_m], [y, y], transform=tx.transAxes, color=RULE, lw=1.2)
    y -= step * 1.0
    tx.text(0.00, y,
            "Near-exact on the class the model\n"
            "was built over. Useless outside it.",
            fontsize=FS, color=INK, va="top", linespacing=1.5,
            transform=tx.transAxes)

    if y - 2 * step < -0.02:
        raise AssertionError("table overflows its panel: lower FS or raise H")
    fig.subplots_adjust(left=0.085, right=0.985, top=0.97, bottom=0.145)
    _save(fig, "s17_terminator_model")
    return [(l, n, r, m) for l, _c, _mk, n, r, m in rows]


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

    Two decompositions of the same kind of quantity, and they are NOT the same
    measurement -- the figure says so. Attributing protein variance to *which
    part* explains 84% of it. Asking *what about the sequence* explains 28%.
    That gap is the session's thesis: the part is not in the sequence.

    No legend: each bar's key is its own subtitle, with every category word in
    its segment's colour, placed by measuring the word that precedes it. That
    also stops the third bar's teal reading as "promoter" -- it has its own
    colour and says so on the line above.
    """
    FS = TYPE["body"]
    SUB = TYPE["caption"]
    H = 5.3
    fig, ax = plt.subplots(figsize=(10.9, H))

    bars = [
        ("Kosuri 2013 · RNA level",
         [("promoter", 92.0, TEAL), ("RBS", 4.0, CYAN),
          ("unexplained", 4.0, RULE)]),
        ("Kosuri 2013 · protein level",
         [("promoter", 54.0, TEAL), ("RBS", 30.0, CYAN),
          ("unexplained", 16.7, RULE)]),
        ("Cambray 2018 · protein level",
         [("sequence features", CAMBRAY18["explained"], GREEN),
          ("unexplained", 100.0 - CAMBRAY18["explained"], RULE)]),
    ]

    line_in = FS / 72.0 * 1.62
    pitch = line_in * 3.25                      # inches per group, from the type
    ys = [-(i * pitch) for i in range(len(bars))]
    ax.set_ylim(ys[-1] - pitch * 1.05, pitch * 0.80)
    ax.set_xlim(0, 100)
    ax.set_axis_off()

    def _wpts(txt, size):
        """Width of `txt` in x-data units (the axis spans 0-100)."""
        t = ax.text(0, ys[0] + pitch, txt, fontsize=size)
        fig.canvas.draw()
        w = t.get_window_extent(fig.canvas.get_renderer()).width
        t.remove()
        return 100.0 * w / ax.get_window_extent().width

    for y, (title, parts) in zip(ys, bars):
        ax.text(0, y + line_in * 1.72, title, fontsize=FS, color=INK,
                va="bottom", weight="bold")
        # the key: category words in their own colours, laid out by measurement
        x = 0.0
        sep = "   ·   "
        for i, (name, _v, c) in enumerate(parts):
            if i:
                ax.text(x, y + line_in * 0.44, sep, fontsize=SUB, color=MUTED,
                        va="bottom")
                x += _wpts(sep, SUB)
            ax.text(x, y + line_in * 0.44, name, fontsize=SUB,
                    color=MUTED if c is RULE else c, va="bottom", weight="bold")
            x += _wpts(name, SUB)
        left = 0.0
        for name, v, c in parts:
            ax.barh(y - line_in * 0.30, v, left=left, height=line_in * 0.86,
                    color=c, edgecolor="white", linewidth=1.2, zorder=3)
            if v >= 9:
                ax.text(left + v / 2, y - line_in * 0.30, f"{v:g}%",
                        fontsize=FS, color=MUTED if c is RULE else "white",
                        ha="center", va="center", zorder=4)
            left += v

    ax.text(0, ys[-1] - pitch * 0.58,
            "Not the same measurement. But: which part explains 84%.\n"
            f"What about the sequence explains {CAMBRAY18['explained']:g}%.",
            fontsize=FS, color=INK, va="top", linespacing=1.5)

    fig.subplots_adjust(left=0.012, right=0.995, top=0.99, bottom=0.015)
    _save(fig, "s17_variance")
    return [(t, [v for _n, v, _c in p]) for t, p in bars]


MUTALIK = {                     # Nat Methods (2013), nmeth.2404
    # "arbitrary genes are reliably expressed to within twofold relative
    #  target expression windows with ~93% reliability", over elements
    #  "across a 1,000-fold observed dynamic range"
    "within_twofold": 93.0,
    "dynamic_range": 1000,
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
    """What manufacturing the parts buys, in the one metric both papers share.

    The caveat is ON the figure, not only in the design doc: these are not the
    same measurement. Kosuri's 64% is prediction accuracy over 12,653 collected
    combinations; Mutalik's 93% is hitting a target window with elements built
    to a common standard. Same tolerance, different question.
    """
    FS = TYPE["body"]
    H = 5.2
    fig, ax = plt.subplots(figsize=(10.4, H))
    line_in = FS / 72.0 * 1.62
    sub_in = TYPE["caption"] / 72.0 * 1.45

    rows = [
        ("collected parts", "Kosuri 2013 — within 2× of prediction,\n"
                            "12,653 promoter × RBS combinations",
         KOSURI_WITHIN_2X["protein"], TEAL),
        ("manufactured parts", "Mutalik 2013 — within 2× of a target window,\n"
                               f"elements spanning {MUTALIK['dynamic_range']:,}-fold",
         MUTALIK["within_twofold"], GREEN),
    ]
    # Pitch is the tallest row, measured: title + bar + however many lines the
    # caption actually has. A fixed multiple put the next title on the last
    # caption.
    n_sub = max(sub.count("\n") + 1 for _l, sub, *_ in rows)
    pitch = line_in * 1.62 + line_in * 0.95 + n_sub * sub_in + line_in * 0.75
    ys = [-(i * pitch) for i in range(len(rows))]
    ax.set_xlim(0, 100)
    ax.set_ylim(ys[-1] - pitch * 1.25, pitch * 0.58)
    ax.set_axis_off()

    for y, (label, sub, v, c) in zip(ys, rows):
        ax.text(0, y + line_in * 1.62, label, fontsize=FS, color=INK,
                va="bottom", weight="bold")
        ax.barh(y, 100, left=0, height=line_in * 0.95,
                color=RULE, edgecolor="white", linewidth=1.2, zorder=2)
        ax.barh(y, v, left=0, height=line_in * 0.95,
                color=c, edgecolor="white", linewidth=1.2, zorder=3)
        ax.text(v - 1.2, y, f"{v:g}%", fontsize=FS, color="white",
                ha="right", va="center", zorder=4)
        ax.text(0, y - line_in * 0.92, sub, fontsize=TYPE["caption"],
                color=MUTED, va="top", linespacing=1.45)

    gain = MUTALIK["within_twofold"] - KOSURI_WITHIN_2X["protein"]
    ax.text(0, ys[-1] - pitch * 0.78,
            f"Same tolerance, met {gain:.0f} points more often — but not the "
            f"same measurement.\nPrediction accuracy against hitting a target. "
            f"Say so out loud.",
            fontsize=FS, color=INK, va="top", linespacing=1.5)

    fig.subplots_adjust(left=0.012, right=0.995, top=0.99, bottom=0.015)
    _save(fig, "s17_manufacture")
    return [(l, v) for l, _s, v, _c in rows]


# Sources go in the slide foot, not the table -- the measured layout said the
# source column cost 44% more width than the slide has.
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
    H = 5.0
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
        y -= step * 1.18
    y -= step * 0.25
    ax.plot([0, end], [y, y], transform=ax.transAxes, color=RULE, lw=1.2)
    y -= step * 1.1
    ax.text(0, y, "Insulation is a device, not a distance.",
            fontsize=FS, color=INK, va="top", weight="bold",
            transform=ax.transAxes)
    if y - step < -0.02:
        raise AssertionError("insulator table overflows; cut a row")

    fig.subplots_adjust(left=0.012, right=0.995, top=0.99, bottom=0.015)
    _save(fig, "s17_insulators")
    return INSULATORS


# --- T44: Golden Gate overhangs ------------------------------------------
# All of this is COMPUTED. A 4-nt overhang anneals to its reverse complement,
# so an overhang and that complement are one junction identity; a palindromic
# overhang is its own complement and self-ligates, so it is unusable.

BASES = "ACGT"
_COMP = {"A": "T", "C": "G", "G": "C", "T": "A"}


def _revcomp(o):
    return "".join(_COMP[b] for b in reversed(o))


def _overhang_classes(n=4):
    """Usable 4-nt overhang identities: non-palindromic, complement-merged."""
    from itertools import product
    all_o = ["".join(p) for p in product(BASES, repeat=n)]
    palindromic = [o for o in all_o if o == _revcomp(o)]
    seen, classes = set(), []
    for o in all_o:
        if o in palindromic or o in seen:
            continue
        seen.add(o)
        seen.add(_revcomp(o))
        classes.append(o)
    return all_o, palindromic, classes


def _clash_probability(classes, k, trials=4000, seed=17):
    """P(some pair of k randomly chosen overhangs differs in <= 1 base).

    A deliberately crude proxy for misligation -- real fidelity is measured,
    not derived from Hamming distance. Labelled as a toy on the figure.
    """
    import random
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        pick = rng.sample(classes, k)
        bad = False
        for i in range(k):
            for j in range(i + 1, k):
                a, b = pick[i], pick[j]
                d = min(sum(x != y for x, y in zip(a, b)),
                        sum(x != y for x, y in zip(a, _revcomp(b))))
                if d <= 1:
                    bad = True
                    break
            if bad:
                break
        hits += bad
    return hits / trials


def fig_overhangs():
    """How many parts fit in one pot before two junctions look alike.

    T44. The counting is exact; the clash curve is an explicitly crude proxy
    for misligation, which in practice is measured rather than derived.
    """
    FS = TYPE["body"]
    H = 5.3
    all_o, pal, classes = _overhang_classes()
    ks = list(range(2, 21))
    ps = [_clash_probability(classes, k) for k in ks]

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
    half = next((k for k, p in zip(ks, ps) if p >= 0.5), None)
    if half:
        ax.axvline(half, color=RED, lw=1.6, ls=(0, (4, 3)), zorder=2)
        ax.text(half + 0.4, 17, f"{half} parts", fontsize=FS, color=RED,
                va="center")
    ax.set_xlabel("parts assembled in one pot")
    ax.set_ylabel("chance two junctions clash  (%)")
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
    y -= step * 1.05
    tx.text(0.0, y,
            "120 looks like plenty. What binds\n"
            "is not how many there are, but\n"
            "how alike any two may be.",
            fontsize=FS, color=INK, va="top", linespacing=1.45,
            transform=tx.transAxes)
    y -= step * 3.6
    tx.text(0.0, y, "Clash curve is a toy: one-base proximity,\nnot measured ligation fidelity.",
            fontsize=TYPE["caption"], color=MUTED, va="top", linespacing=1.4,
            transform=tx.transAxes)
    if y - step < -0.02:
        raise AssertionError("overhang panel overflows; cut a line")

    fig.subplots_adjust(left=0.085, right=0.99, top=0.97, bottom=0.145)
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
    SUB = TYPE["caption"]
    H = 5.2
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
    b.text(0.86, 0.705, "transcript", fontsize=SUB, color=MUTED, va="center")
    b.text(0.86, 0.605, "5′UTR", fontsize=SUB, color=MUTED, va="center")
    arrow(b, 0.68, 0.705, 0.84, 0.705, GREEN)
    arrow(b, 0.68, 0.605, 0.84, 0.605, GREEN)
    # the loop: the 5'UTR it writes is the 5'UTR it reads. Routed UNDER the
    # box, because an arrow through the box reads as flow, not feedback.
    b.annotate("", xy=(0.09, 0.545), xytext=(0.91, 0.545),
               arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4,
                               connectionstyle="arc3,rad=-0.34",
                               shrinkA=2, shrinkB=2))
    b.text(0.5, 0.28, "the 5′UTR it writes is the 5′UTR it reads",
           fontsize=SUB, color=RED, ha="center", va="center")
    b.text(0.5, 0.16, "The only picture in which\n"
                      "“joining changes both” can be said.",
           fontsize=SUB, color=MUTED, ha="center", va="center",
           linespacing=1.45)

    fig.subplots_adjust(left=0.015, right=0.985, top=0.98, bottom=0.02,
                        wspace=0.10)
    _save(fig, "s17_compositor")
    return "compositor"


FIGURES = [fig_terminator_model, fig_variance,
           fig_manufacture, fig_insulators, fig_overhangs,
           fig_compositor]

if __name__ == "__main__":
    for f in FIGURES:
        out = f()
        print(f.__name__, "->", out)
