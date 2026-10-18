"""Session 16 figures — combinational and sequential logic.

Every table here is COMPUTED by `posb.logic`, from the gate list, at render
time. None of the numbers is typed into this file. That matters more than
usual for this session: the whole point of the timing table is that it is
derived rather than asserted, and a figure carrying hand-typed ticks would be
the exact defect the session is about.

Layout rule, from `docs/lecture-design.md`: no row pitch is written down. A
table asks how tall its own text is at the current point size and pitches
itself from that, and every caption is placed relative to where its table
actually ended rather than at a y chosen by eye.

SIZE. matplotlib point sizes are ABSOLUTE, so a figure's text scales with the
figure when the deck places it. A figure authored 12in wide and dropped into a
12in slot lands at 1:1 -- and 14pt type is then 14pt on the wall, under the
20pt content floor in `posb-slide-legibility`. Session 14's figures are
authored 5-9in wide and UPSCALE about 1.7x into the slide, which is what puts
their 12pt labels over the floor. These follow that: wide figures are authored
near SLOT/UP, so the deck enlarges them.

Run:  python tools/build_figures.py s16
"""
import numpy as np

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN, RULE
from posb.logic import (
    classifier_2025, classifier_fixed, GateNetwork, NOT, NOR, NAND,
    BUF, hazards, TruthTable, cascade_half_time,
    cascade_step_response,
)

plt = use()
OUT = "figures/build"


def _save(fig, name):
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# measured table rendering
# ---------------------------------------------------------------------------
def _row_pitch(fig, ax, fontsize):
    """Height of one text row, in AXES fraction, measured not guessed.

    A point is 1/72 inch, so a row is fontsize/72 inches of type plus half a
    line of air. Expressing that as a fraction of the axes needs the AXES
    height in inches -- `ax.get_position().height` times the figure height --
    not the figure height itself. Dividing by the figure height is correct by
    accident on a single-axes figure and halves the pitch on a two-row grid,
    which is how the first build of this file came out with every table
    collapsed on top of itself.
    """
    ax_h_in = ax.get_position().height * fig.get_size_inches()[1]
    return (fontsize / 72.0) * 1.55 / ax_h_in


def _table(ax, fig, headers, rows, *, fontsize=20, mark=None, title=None):
    """Draw a tick-by-tick table.

    `mark` is a set of (row, col) cells to ring in red -- the glitch.
    Returns (y_of_last_row, pitch) so the caller can put a caption under a
    table whose length it did not choose.
    """
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    pitch = _row_pitch(fig, ax, fontsize)
    ncol = len(headers)
    xs = [(i + 0.5) / ncol for i in range(ncol)]
    y = 1.0 - pitch * 0.7
    if title:
        ax.text(0.0, y, title, fontsize=fontsize + 1, color=INK,
                fontweight="bold", va="top", ha="left")
        y -= pitch * 1.45 * (1 + title.count("\n"))

    for x, h in zip(xs, headers):
        ax.text(x, y, h, fontsize=fontsize, color=MUTED, va="center",
                ha="center", fontweight="bold")
    y -= pitch * 0.55
    ax.plot([0.0, 1.0], [y, y], color=RULE, lw=1.4)
    y -= pitch * 0.75

    for r, row in enumerate(rows):
        for c, (x, v) in enumerate(zip(xs, row)):
            ax.text(x, y, str(v), fontsize=fontsize, color=INK,
                    va="center", ha="center", fontfamily="DejaVu Sans Mono")
            if mark and (r, c) in mark:
                ax.add_patch(plt.Circle((x, y), pitch * 0.46, fill=False,
                                        edgecolor=RED, lw=2.2, zorder=5))
        y -= pitch
    return y, pitch


def _rows_from(net, assignment, ticks, wires):
    tbl = net.timing_table(assignment, initial=0, ticks=ticks)
    return [[r["t"]] + [int(r[w]) for w in wires] for r in tbl], tbl


# ---------------------------------------------------------------------------
# 1. the circuit, and what it is supposed to do
# ---------------------------------------------------------------------------
def _gene(ax, x, y, label, w=0.16, h=0.13, edge=TEAL):
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor="white",
                               edgecolor=edge, lw=2.2, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=20, color=INK,
            zorder=4)


def _repress(ax, p0, p1, color=RED, bar=0.030):
    """A repression arm: a line ending in a crossbar, not an arrowhead."""
    (x0, y0), (x1, y1) = p0, p1
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-", color=color, lw=2.4))
    d = np.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / d, (y1 - y0) / d
    ax.plot([x1 - uy * bar, x1 + uy * bar], [y1 + ux * bar, y1 - ux * bar],
            color=color, lw=3.0, solid_capstyle="butt")


def fig_classifier():
    """The 2025 two-input classifier, and the truth table it must settle to."""
    fig, (axc, axt) = plt.subplots(1, 2, figsize=(12.0, 4.00),
                                   gridspec_kw={"width_ratios": [1.5, 1.0]})
    axc.set_axis_off(); axc.set_xlim(0, 1); axc.set_ylim(0, 1)

    # The circuit lives in the upper band and every caption sits below it, so
    # no repression arm is ever drawn through text.
    _gene(axc, 0.09, 0.88, "B"); _gene(axc, 0.09, 0.46, "A")
    _gene(axc, 0.38, 0.88, "R1"); _gene(axc, 0.61, 0.62, "R2")
    _gene(axc, 0.85, 0.62, "R3", edge=AMBER)

    # R2's TWO promoters, drawn. One box with two repression bars on it is
    # exactly the picture the NOR slide uses, so reusing it here said the
    # opposite of what the caption says -- four slides after teaching the
    # room that the DNA layout is what picks the gate.
    for dx in (-0.040, 0.040):
        px = 0.61 + dx
        axc.plot([px, px], [0.687, 0.748], color=GREEN, lw=2.2)
        axc.annotate("", xy=(px + 0.038, 0.748), xytext=(px, 0.748),
                     arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.2,
                                     mutation_scale=13))

    _repress(axc, (0.175, 0.88), (0.292, 0.88))          # B -| R1
    _repress(axc, (0.175, 0.49), (0.540, 0.700))         # A -| promoter 1
    _repress(axc, (0.448, 0.845), (0.636, 0.795))        # R1 -| promoter 2
    _repress(axc, (0.695, 0.62), (0.763, 0.62))          # R2 -| R3

    axc.text(0.935, 0.62, "out", fontsize=20, color=AMBER,
             ha="left", va="center")
    axc.text(0.0, 0.30, "R1 = NOT B", fontsize=20, color=MUTED, ha="left")
    axc.text(0.0, 0.22,
             "R2 is ONE gene behind TWO promoters,\n"
             "each with its own operator, so either\n"
             "repressor silences it:  NAND(A, R1).",
             fontsize=20, color=MUTED, ha="left", va="top")
    axc.set_title("A AND NOT B, built from repressors", loc="left",
                  fontsize=20, color=INK, fontweight="bold")

    spec = TruthTable.from_function(("A", "B"), lambda a, b: a and not b)
    assert classifier_2025().realised_truth_table().rows == spec.rows
    rows = [[int(a), int(b), int(spec(a, b))] for (a, b) in sorted(spec.rows)]
    y, p = _table(axt, fig, ["A", "B", "R3"], rows,
                  title="what it must settle to")
    axt.text(0.0, y - p * 0.8, "and nothing here says WHEN",
             fontsize=20, color=AMBER, va="top", fontweight="bold")
    _save(fig, "s16_classifier")


# ---------------------------------------------------------------------------
# 2. the timing table, as a derivation run
# ---------------------------------------------------------------------------
def fig_timing_steps():
    """Four surfaces: the table empty, filling, the glitch, all four cases."""
    net = classifier_2025()
    # A and B are held constant through this run, so showing them as two
    # columns of zeros only makes the table too wide for derivation_fig's
    # 5.4in picture column. The titles carry the inputs instead.
    wires = ["R1", "R2", "R3"]
    hdr = ["t"] + wires

    # p1 -- cold start. Every gate reads 0 because no protein exists yet.
    fig, ax = plt.subplots(figsize=(5.2, 2.30))
    rows, _ = _rows_from(net, {"A": 0, "B": 0}, 1, wires)
    y, p = _table(ax, fig, hdr, rows, fontsize=16,
                  title="A=0, B=0   ·   t = 0")
    ax.text(0.0, y - p, "No protein yet, so every\n"
                        "gate reads 0. Not a steady\n"
                        "state — an empty cell.",
            fontsize=16, color=MUTED, va="top")
    _save(fig, "s16_timing_p1")

    # p2 -- one tick. R3 goes high while R2 is still absent.
    fig, ax = plt.subplots(figsize=(5.2, 2.55))
    rows, _ = _rows_from(net, {"A": 0, "B": 0}, 2, wires)
    y, p = _table(ax, fig, hdr, rows, fontsize=16,
                  title="t = 1   ·   one gate delay", mark={(1, 3)})
    ax.text(0.0, y - p, "R3 = NOT R2, and R2 was 0,\n"
                        "so R3 switches ON. But\n"
                        "A = 0: it should be 0.",
            fontsize=16, color=MUTED, va="top")
    _save(fig, "s16_timing_p2")

    # p3 -- settled, glitch named from posb.logic rather than from the slide
    fig, ax = plt.subplots(figsize=(5.2, 3.05))
    rows, tbl = _rows_from(net, {"A": 0, "B": 0}, 4, wires)
    hz = hazards(tbl, "R3")
    assert len(hz) == 1 and hz[0].kind == "static-0", hz
    y, p = _table(ax, fig, hdr, rows, fontsize=16,
                  title="settled, and wrong on the way", mark={(1, 3)})
    ax.text(0.0, y - p, "R3 holds 0 at both ends and\n"
                        f"visits 1 between: a\n{hz[0].kind} hazard.",
            fontsize=16, color=RED, va="top")
    _save(fig, "s16_timing_p3")

    # p4 -- all four input cases, kinds computed
    fig, axes = plt.subplots(1, 4, figsize=(12.0, 3.30))
    fig.subplots_adjust(top=0.74, bottom=0.10)
    for ax, (a, b) in zip(axes, [(0, 0), (0, 1), (1, 0), (1, 1)]):
        rows, tbl = _rows_from(net, {"A": a, "B": b}, 4, ["R3"])
        hz = hazards(tbl, "R3")
        kind = hz[0].kind if hz else "clean"
        y, p = _table(ax, fig, ["t", "R3"], rows, fontsize=20,
                      title=f"A={a}   B={b}")
        ax.text(0.0, y - p * 0.8, kind, fontsize=20,
                color=RED if hz else GREEN, va="top", fontweight="bold")
    fig.suptitle("every input case glitches — and one of them twice",
                 fontsize=24, color=INK, y=0.96)
    _save(fig, "s16_timing_p4")


# ---------------------------------------------------------------------------
# 3. the wrong explanation, and the right one
# ---------------------------------------------------------------------------
def fig_cold_start():
    """Balance does not save you: a balanced depth-2 circuit still glitches."""
    bal = GateNetwork([NOT("na", "A"), NOT("nb", "B"), NOR("Z", "na", "nb")],
                      inputs=("A", "B"), output="Z")
    assert bal.is_balanced() and not bal.is_fail_safe()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 3.90),
                                   gridspec_kw={"width_ratios": [1.0, 1.05]})
    fig.subplots_adjust(wspace=0.32)
    rows, tbl = _rows_from(bal, {"A": 0, "B": 0}, 4,
                           ["A", "B", "na", "nb", "Z"])
    hz = hazards(tbl, "Z")
    assert len(hz) == 1 and hz[0].kind == "static-0"
    y, p = _table(ax1, fig, ["t", "A", "B", "na", "nb", "Z"], rows,
                  title="Z = NOR(NOT A, NOT B)", mark={(1, 5)})
    ax1.text(0.0, y - p, "Both inputs reach Z in two gates — balanced.\n"
                         "It still glitches.",
             fontsize=20, color=RED, va="top", fontweight="bold")

    ax2.set_axis_off(); ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
    ax2.text(0.0, 0.97, "so it is not the path lengths",
             fontsize=24, color=INK, fontweight="bold", va="top")
    ax2.text(0.0, 0.76,
             "A repressor-based gate is ON when its\n"
             "repressor has not arrived yet.\n\n"
             "An empty circuit is one with every inverter\n"
             "switched on, and that false ON propagates\n"
             "while the circuit fills.",
             fontsize=20, color=MUTED, va="top")
    ax2.text(0.0, 0.19,
             "So balance is not the whole story.\n"
             "The other half is the promoter.",
             fontsize=20, color=GREEN, va="top", fontweight="bold")
    _save(fig, "s16_cold_start")


def _one_row(net, name, title, colour, expect_clean):
    """One row of four input cases for a classifier variant, full slide width.

    Split out of a 2x4 grid: eight stacked tables do not fit a slide band
    without being shrunk past the legibility floor, and two surfaces read
    better than one anyway -- the broken circuit, then the repair.
    """
    fig, axes = plt.subplots(1, 4, figsize=(12.0, 3.70))
    fig.subplots_adjust(top=0.80, bottom=0.05, wspace=0.80)
    for ax, (a, b) in zip(axes, [(0, 0), (0, 1), (1, 0), (1, 1)]):
        rows, tbl = _rows_from(net, {"A": a, "B": b}, 4, ["R3"])
        hz = hazards(tbl, "R3")
        assert bool(hz) != expect_clean, (name, a, b, hz)
        y, p = _table(ax, fig, ["t", "R3"], rows, fontsize=20,
                      title=f"A={a}   B={b}")
        ax.text(0.0, y - p * 0.8, hz[0].kind if hz else "clean",
                fontsize=20, color=GREEN if expect_clean else RED,
                va="top", fontweight="bold")
    fig.text(0.02, 0.97, title, fontsize=20,
             color=GREEN if expect_clean else RED, fontweight="bold",
             va="top")
    _save(fig, name)


def fig_timing_broken():
    """The unrepaired classifier: every input case glitches, one of them twice."""
    net = classifier_2025()
    assert not net.is_fail_safe()
    _one_row(net, "s16_timing_broken",
             "R3 = NOT R2   \u2014 ON while the cell is still empty",
             RED, expect_clean=False)


def fig_timing_fixed():
    """The repair: activation required, so the empty cell presents nothing."""
    net = classifier_fixed()
    assert net.is_fail_safe()
    _one_row(net, "s16_timing_fixed",
             "R3 = Act1 AND NOT R2   \u2014 activation required, OFF while empty",
             GREEN, expect_clean=True)


def fig_hazard_types():
    """The three kinds, named by what the output was supposed to do."""
    traces = {
        "static-0\nshould hold 0": [0, 1, 0, 0, 0],
        "static-1\nshould hold 1": [1, 0, 1, 1, 1],
        "dynamic\nshould change once": [0, 1, 0, 1, 1],
    }
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.30))
    fig.subplots_adjust(top=0.72, bottom=0.22)
    for ax, (name, tr) in zip(axes, traces.items()):
        t = np.arange(len(tr))
        ax.step(t, tr, where="post", color=TEAL, lw=3.0)
        ax.plot(t, tr, "o", color=TEAL, ms=6)
        ax.set_ylim(-0.35, 1.35)
        ax.set_yticks([0, 1])
        ax.set_xlabel("tick")
        ax.set_title(name, fontsize=20)
        ax.grid(axis="y", lw=1.0)
    _save(fig, "s16_hazard_types")


# ---------------------------------------------------------------------------
# 4. cascade delay (T41)
# ---------------------------------------------------------------------------
def fig_cascade_delay():
    """Each extra stage costs very nearly one protein lifetime."""
    ns = np.arange(1, 9)
    th = np.array([cascade_half_time(int(n), 1.0) for n in ns])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.30))
    fig.subplots_adjust(wspace=0.28, bottom=0.16)

    for n, c in zip((1, 2, 3, 5), (TEAL, CYAN, AMBER, GREEN)):
        t = np.linspace(0, 10, 400)
        ax1.plot(t, cascade_step_response(n, t, 1.0), color=c, lw=2.8,
                 label=f"{n} stage{'s' if n > 1 else ''}")
        ax1.plot([cascade_half_time(n, 1.0)], [0.5], "o", color=c, ms=7)
    ax1.axhline(0.5, color=MUTED, lw=1.2, ls=":")
    ax1.set_xlabel("time  (lifetimes)")
    ax1.set_ylabel("output, scaled")
    ax1.set_title("the same step, more stages")
    ax1.legend(loc="lower right", fontsize=16)

    ax2.plot(ns, th, "o-", color=TEAL, lw=2.8, ms=7, label=r"$t_{1/2}$")
    ax2.plot(ns, ns - 1 / 3, "--", color=AMBER, lw=2.4,
             label=r"$(n-\frac{1}{3})\,\tau$")
    ax2.set_xlabel("stages  n")
    ax2.set_ylabel(r"$t_{1/2}$  (lifetimes)")
    ax2.set_title("one stage, one lifetime")
    ax2.legend(loc="upper left", fontsize=16)
    gaps = np.diff(th)
    ax2.text(0.98, 0.04,
             f"per stage: {gaps[0]:.3f} → {gaps[-1]:.3f} τ",
             transform=ax2.transAxes, ha="right", fontsize=16, color=MUTED)
    _save(fig, "s16_cascade_delay")


# ---------------------------------------------------------------------------
# 5. memory
# ---------------------------------------------------------------------------
def fig_dirs_states():
    """Ham 2008: the state is the sequence, and the ORDER of inputs picks it."""
    fig, ax = plt.subplots(figsize=(12.0, 4.30))
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    nodes = {"0": (0.07, 0.56), "1": (0.32, 0.83), "2": (0.32, 0.29),
             "3": (0.60, 0.83), "4": (0.60, 0.29)}
    unobserved = {"3"}      # predicted, never seen -- see the caption
    for name, (x, y) in nodes.items():
        ax.add_patch(plt.Circle((x, y), 0.048, facecolor="white",
                                edgecolor=MUTED if name in unobserved else TEAL,
                                ls="--" if name in unobserved else "-",
                                lw=2.4, zorder=3))
        ax.text(x, y, name, ha="center", va="center", fontsize=20,
                color=MUTED if name in unobserved else INK, zorder=4)

    def arc(a, b, label, color, below=False, ls="-"):
        (x0, y0), (x1, y1) = nodes[a], nodes[b]
        ax.annotate("", xy=(x1 - 0.052 * np.sign(x1 - x0), y1),
                    xytext=(x0 + 0.052 * np.sign(x1 - x0), y0),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2,
                                    mutation_scale=15, linestyle=ls))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + (-0.10 if below else 0.07),
                label, fontsize=20, color=color, ha="center")

    arc("0", "1", "FimB", AMBER)
    arc("0", "2", "Hin", GREEN, below=True)
    arc("1", "3", "then Hin", MUTED, ls="--")
    arc("2", "4", "then FimB", AMBER, below=True)

    ax.text(0.73, 0.56,
            "two invertases,\nfour reachable states —\n"
            "and 3 ≠ 4, so the circuit\nremembers the ORDER",
            fontsize=20, color=INK, va="center")
    # Kept short and in two columns: one long caption line made the tight
    # bbox 14.7in wide -- wider than the slide -- which forced the whole
    # figure to be scaled DOWN and undid setting the type at the deck scale.
    ax.text(0.0, 0.11,
            "Dashed: state 3 was predicted and never observed \u2014 the\n"
            "fim arm barely inverted, and of 50 isolates sequenced\n"
            "none carried it. A proof of principle that says so.",
            fontsize=16, color=MUTED, va="top")
    _save(fig, "s16_dirs_states")


def fig_latch_state_table():
    """Session 9's toggle, renamed: the cross-coupled NOR pair as an SR latch."""
    latch = GateNetwork([NOR("Q", "R", "Qbar"), NOR("Qbar", "S", "Q")],
                        inputs=("S", "R"), output="Q")
    runs = [("hold Q = 1\nS = 0, R = 0", {"S": 0, "R": 0},
             {"Q": True, "Qbar": False}),
            ("hold Q = 0\nS = 0, R = 0", {"S": 0, "R": 0},
             {"Q": False, "Qbar": True}),
            ("SET\nS = 1, R = 0", {"S": 1, "R": 0},
             {"Q": False, "Qbar": True}),
            ("RESET\nS = 0, R = 1", {"S": 0, "R": 1},
             {"Q": True, "Qbar": False})]

    # Two lines per title, because one panel is a quarter of the figure and
    # "hold Q=1  (S=0 R=0)" at 21pt needs about half of one. The combining
    # macron on Q-bar is dropped by the monospace cell font, so the column is
    # headed the way the rest of the deck writes a complement.
    fig, axes = plt.subplots(1, 4, figsize=(12.0, 3.90))
    fig.subplots_adjust(top=0.88, bottom=0.08)
    for ax, (label, assign, init) in zip(axes, runs):
        tbl = latch.timing_table(assign, initial=init, ticks=4)
        rows = [[r["t"], int(r["Q"]), int(r["Qbar"])] for r in tbl]
        _table(ax, fig, ["t", "Q", "¬Q"], rows, fontsize=20, title=label)
    _save(fig, "s16_latch_state_table")

# ---------------------------------------------------------------------------
# 6. where the gate comes from -- the DNA architecture, and the rate law drawn
# ---------------------------------------------------------------------------
def _dna(ax, y, elements, *, gene="output"):
    """One stretch of DNA, drawn left to right from a list of elements.

    `elements` is a sequence of ("op", name, colour) and ("prom",). The gene
    is drawn last, at the right-hand end, and every promoter on the strand
    transcribes it -- which is the whole point of the NAND panel: two
    promoters IN TANDEM upstream of one ORF, not two separate transcription
    units. The first version of this figure drew two gene boxes under a title
    that said one gene, in the figure whose entire job is that the DNA layout
    picks the gate.
    """
    x = 0.03
    ax.plot([0.01, 0.99], [y, y], color=INK, lw=2.8, solid_capstyle="butt")
    for el in elements:
        if el[0] == "op":
            _, name, col = el
            ax.add_patch(plt.Rectangle((x, y - 0.040), 0.115, 0.080,
                                       facecolor=col, edgecolor=INK, lw=1.8,
                                       zorder=3))
            ax.text(x + 0.0575, y + 0.085, name, ha="center", va="bottom",
                    fontsize=20, color=col, fontweight="bold")
            x += 0.135
        else:
            ax.plot([x + 0.01, x + 0.01], [y, y + 0.105], color=GREEN, lw=2.6)
            ax.annotate("", xy=(x + 0.105, y + 0.105),
                        xytext=(x + 0.01, y + 0.105),
                        arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.6,
                                        mutation_scale=16))
            x += 0.135
    ax.add_patch(plt.Rectangle((x + 0.02, y - 0.055), 0.34, 0.110,
                               facecolor="white", edgecolor=TEAL, lw=2.2,
                               zorder=3))
    ax.text(x + 0.19, y, gene, ha="center", va="center", fontsize=20,
            color=INK, zorder=4)


def _occupancy_grid(n=260, lo=-2.0, hi=2.0):
    r = np.logspace(lo, hi, n)
    return r, *np.meshgrid(r, r)


def _arch(name, title, strands, P, corners, caption):
    """One DNA architecture beside the rate law it produces, as a picture.

    Split from a single two-column figure because that came out 6.9in tall --
    past the slide band -- and because showing NOR, then NAND as its contrast,
    is the better order anyway.
    """
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("posb", ["#F8FAF9", CYAN, TEAL])
    r = np.logspace(-2, 2, 260)

    fig, (axd, axp) = plt.subplots(1, 2, figsize=(11.0, 4.0),
                                   gridspec_kw={"width_ratios": [1.15, 1.0]})
    # The title spans BOTH panels, so it belongs to the figure. Hung off the
    # left axes it ran past that panel and landed on the heatmap's y-label.
    fig.subplots_adjust(top=0.80, bottom=0.16, wspace=0.28)

    axd.set_axis_off(); axd.set_xlim(0, 1); axd.set_ylim(0, 1)
    _dna(axd, 0.58, strands)
    axd.text(0.01, 0.10, caption, ha="left", va="bottom", fontsize=20,
             color=MUTED)
    fig.suptitle(title, fontsize=20, color=INK, fontweight="bold", y=0.96)

    im = axp.pcolormesh(r, r, P(*np.meshgrid(r, r)), cmap=cmap,
                        shading="auto", vmin=0.0, vmax=1.0)
    axp.set_xscale("log"); axp.set_yscale("log")
    axp.set_xlabel("repressor A  (units of K)", fontsize=20)
    axp.set_ylabel("repressor B  (units of K)", fontsize=20)
    axp.tick_params(labelsize=18)
    # The badge is READ OFF the rate law at the marker, not typed: the NAND's
    # two single-repressor corners sit at half amplitude, and badging them
    # "1" asserted something the colour underneath contradicts.
    for (i, j) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        x, y = 10 ** (-1.6 + 3.2 * i), 10 ** (-1.6 + 3.2 * j)
        v = float(P(np.array([[x]]), np.array([[y]]))[0, 0])
        lab = "1" if v > 0.75 else ("0" if v < 0.25 else "\u00bd")
        dark = v > 0.75
        axp.text(x, y, lab, ha="center", va="center", fontsize=22,
                 fontweight="bold", color="white" if dark else INK,
                 bbox=dict(boxstyle="circle,pad=0.20",
                           fc=INK if dark else "white", ec=INK, lw=1.8))
    fig.colorbar(im, ax=axp, fraction=0.045, pad=0.03)
    _save(fig, name)


def fig_arch_nor():
    """One promoter with two operators: either repressor silences it -- NOR."""
    _arch("s16_arch_nor",
          "ONE promoter, TWO operators   \u2192   P_on = 1 / (1+r_A)(1+r_B)",
          [("op", "A", AMBER), ("op", "B", RED), ("prom",)],
          lambda A, B: 1.0 / ((1.0 + A) * (1.0 + B)),
          None,
          "Either repressor blocks\nthe one promoter.")


def fig_arch_nand():
    """Two promoters driving one gene: both must be blocked -- NAND."""
    _arch("s16_arch_nand",
          "TWO promoters, ONE gene   \u2192   out \u221d 1/(1+r_A) + 1/(1+r_B)",
          [("op", "A", AMBER), ("prom",), ("op", "B", RED), ("prom",)],
          lambda A, B: 0.5 * (1.0 / (1.0 + A) + 1.0 / (1.0 + B)),
          None,
          "Tandem promoters, one gene.\nSilent only if BOTH\nare blocked.")


def fig_universal():
    """Complement plus aggregator is everything: NOR and NAND each suffice."""
    fig, ax = plt.subplots(figsize=(11.0, 3.3))
    # The axes, not the figure, is what block() measures against: matplotlib's
    # default margins leave it 9.3in wide inside a 12in figure, and "every
    # logic function" at 19pt bold needs 3.3in in a box that was therefore
    # only 2.8in. Give the axes the whole figure so a 0.30 block really is
    # 3.6 inches. (Same class of error as _row_pitch, found the same way:
    # by rendering the slide and looking at it.)
    ax.set_position([0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    def block(x, head, body, col, w=0.30):
        ax.add_patch(plt.Rectangle((x, 0.28), w, 0.50, facecolor="white",
                                   edgecolor=col, lw=2.4))
        ax.text(x + w / 2, 0.685, head, ha="center", va="center", fontsize=19,
                color=col, fontweight="bold")
        ax.text(x + w / 2, 0.435, body, ha="center", va="center", fontsize=16,
                color=MUTED)

    block(0.010, "a COMPLEMENT", "turn it over\nNOT", AMBER, w=0.26)
    block(0.340, "an AGGREGATOR", "ANY of them  (OR)\nor  ALL of them  (AND)",
          TEAL, w=0.32)
    block(0.680, "every logic function", "no third ingredient\nis needed",
          GREEN, w=0.32)
    for x in (0.283, 0.645):
        ax.annotate("", xy=(x + 0.030, 0.53), xytext=(x, 0.53),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.4,
                                    mutation_scale=16))
    ax.text(0.5, 0.10,
            "NOR is NOT(OR).   NAND is NOT(AND).\nEach packs both "
            "ingredients into one piece of DNA,\nso either one, alone, can "
            "build anything.",
            ha="center", va="center", fontsize=18, color=INK)
    _save(fig, "s16_universal")



# ---------------------------------------------------------------------------
# 7. one truth table, two NOR networks -- the choice the table does not make
#
# Added 18 October. The XNOR exercise had been debriefed with one network
# presented as THE answer, and with its depths mis-stated. Both defects came
# from the same omission: a truth table has many realisations, and choosing
# between them is what the compiler actually does. So this figure shows two,
# and -- following the rule at the top of this file -- the gene counts and the
# path lengths on it are COMPUTED from the gate lists by posb.logic, never
# typed. That is how the mis-stated depths were caught.
# ---------------------------------------------------------------------------
XGW, XGH = 0.105, 0.130
NOT_A, NOT_B = "¬A", "¬B"


def _xgene(ax, x, y, label, edge=TEAL):
    ax.add_patch(plt.Rectangle((x - XGW / 2, y - XGH / 2), XGW, XGH,
                               facecolor="white", edgecolor=edge, lw=2.2,
                               zorder=4))
    ax.text(x, y, label, ha="center", va="center", fontsize=20, color=INK,
            zorder=5)


def _xwire(ax, src, dst, chan, dy=0.0, color=RED):
    """A repression arm routed at right angles, ending in a crossbar.

    Right angles rather than diagonals: a diagonal across a crowded layer
    lands on a neighbouring gene's label, and a schematic wire is read faster
    than a vector. `dy` separates the two arms arriving at a two-operator
    promoter so that both are visible where they land, and every fan-out gets
    its own vertical channel -- sharing one put A's trunk and B's on the same
    x, which reads as a wire from A to B.
    """
    gap, bar = 0.016, 0.034
    x0, y0 = src
    x1, y1 = dst[0], dst[1] + dy
    x0e, x1e = x0 + XGW / 2, x1 - XGW / 2 - gap
    ax.plot([x0e, chan], [y0, y0], color=color, lw=2.2, zorder=2)
    ax.plot([chan, chan], [y0, y1], color=color, lw=2.2, zorder=2)
    ax.plot([chan, x1e], [y1, y1], color=color, lw=2.2, zorder=2,
            solid_capstyle="butt")
    ax.plot([x1e, x1e], [y1 - bar, y1 + bar], color=color, lw=3.4, zorder=3,
            solid_capstyle="butt")


def _xstats(net):
    """'<n> genes' and the longest and shortest input-to-output path, counted.

    `path_lengths` is per source, so the extremes are taken over every input:
    the quantity that matters is how far apart the arrivals at the output are,
    whichever inputs they came from.
    """
    lens = [n for i in net.inputs for n in net.path_lengths(i)]
    return f"{len(net.gates)} genes\nlongest path {max(lens)}, shortest {min(lens)}"


def _xpanel(ax, nodes, edges, title, gloss, stats):
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    for name, (x, y, edge) in nodes.items():
        _xgene(ax, x, y, name, edge=edge)
    for src, dst, chan, dy in edges:
        _xwire(ax, nodes[src][:2], nodes[dst][:2], chan, dy)
    ax.set_title(title, fontsize=20, color=INK, loc="left", fontweight="bold")
    ax.text(0.0, 0.03, gloss, fontsize=16, color=MUTED, ha="left", va="top")
    ax.text(0.0, -0.21, stats, fontsize=20, color=INK, ha="left", va="top",
            fontweight="bold")


def fig_xnor_two_ways():
    """One truth table, two NOR networks: six genes deep four, or four deep three."""
    recipe = GateNetwork(
        [NOT("nA", "A"), NOT("nB", "B"),
         NOR("P", "A", "B"), NOR("Q", "nA", "nB"),
         NOR("R", "P", "Q"), NOT("out", "R")],
        inputs=("A", "B"), output="out")
    minimal = GateNetwork(
        [NOR("P", "A", "B"), NOR("S", "A", "P"), NOR("T", "B", "P"),
         NOR("out", "S", "T")],
        inputs=("A", "B"), output="out")
    xnor = TruthTable.from_function(("A", "B"), lambda a, b: a == b)
    for net in (recipe, minimal):
        assert net.realised_truth_table().rows == xnor.rows

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(12.0, 5.2))
    fig.subplots_adjust(top=0.90, bottom=0.26, left=0.015, right=0.985,
                        wspace=0.09)
    U = 0.024

    # 0.96 put the top of the box at 1.025, outside the axes, and matplotlib
    # clipped its upper border away. Keep every node inside the band.
    L = {"A": (0.050, 0.68, MUTED), "B": (0.050, 0.34, MUTED),
         NOT_A: (0.240, 0.91, AMBER), NOT_B: (0.240, 0.11, AMBER),
         "P": (0.240, 0.58, TEAL), "Q": (0.450, 0.32, TEAL),
         "R": (0.650, 0.52, TEAL), "out": (0.870, 0.52, GREEN)}
    LE = [("A", NOT_A, 0.172, 0.0), ("A", "P", 0.172, +U),
          ("B", NOT_B, 0.112, 0.0), ("B", "P", 0.112, -U),
          (NOT_A, "Q", 0.362, +U), (NOT_B, "Q", 0.330, -U),
          ("P", "R", 0.578, +U), ("Q", "R", 0.540, -U),
          ("R", "out", 0.775, 0.0)]
    _xpanel(axl, L, LE, "what the recipe gives you",
            "P = NOR(A, B)        Q = NOR(" + NOT_A + ", " + NOT_B + ")\n"
            "R = NOR(P, Q)        out = NOT R",
            _xstats(recipe))

    R = {"A": (0.075, 0.80, MUTED), "B": (0.075, 0.22, MUTED),
         "P": (0.330, 0.52, TEAL),
         "S": (0.580, 0.88, TEAL), "T": (0.580, 0.13, TEAL),
         "out": (0.860, 0.52, GREEN)}
    RE = [("A", "P", 0.210, +U), ("A", "S", 0.502, +U),
          ("B", "P", 0.172, -U), ("B", "T", 0.395, -U),
          ("P", "S", 0.455, -U), ("P", "T", 0.432, +U),
          ("S", "out", 0.752, +U), ("T", "out", 0.718, -U)]
    _xpanel(axr, R, RE, "the minimum, found by search",
            "P = NOR(A, B)        S = NOR(A, P)\n"
            "T = NOR(B, P)        out = NOR(S, T)",
            _xstats(minimal))

    _save(fig, "s16_xnor_two_ways")



# ---------------------------------------------------------------------------
# 8. the engineering result, stated as the conjunction it actually is
#
# Added 18 October after an adversarial review found that the deck refuted
# "balance is enough" with fig_cold_start and then asserted the mirror-image
# overclaim -- "fix the promoter, not the wiring" -- without testing it. It
# is false: the deck's OWN first repair (pad the short path with an
# activator) is fail-safe and still glitches in all four cases. Both
# conditions are needed, each has a counterexample in this session, and the
# four rows below are computed rather than asserted.
# ---------------------------------------------------------------------------
def fig_two_conditions():
    """Fail-safe or balanced alone is not enough; the counterexample is computed."""
    padded = GateNetwork(
        [NOT("R1", "B"), NAND("R2", "A", "R1"), NOT("Act", "R2"),
         BUF("R3", "Act")],
        inputs=("A", "B"), output="R3")
    balanced = GateNetwork(
        [NOT("na", "A"), NOT("nb", "B"), NOR("Z", "na", "nb")],
        inputs=("A", "B"), output="Z")

    cases = [
        ("the 2025 classifier", classifier_2025()),
        ("Z = NOR(¬A, ¬B)", balanced),
        ("pad the short path", padded),
        ("require an activator", classifier_fixed()),
    ]
    rows, bad = [], []
    for i, (name, net) in enumerate(cases):
        n_bad = sum(bool(hazards(_rows_from(net, {"A": a, "B": b}, 4,
                                            [net.output])[1], net.output))
                    for a in (0, 1) for b in (0, 1))
        if n_bad:
            bad.append(i)
        rows.append((name,
                     "yes" if net.is_fail_safe() else "no",
                     "yes" if net.is_balanced() else "no",
                     "clean" if n_bad == 0 else f"glitches {n_bad}/4"))
    # The lesson exists only if exactly the last row is clean.
    assert bad == [0, 1, 2], bad

    # Not _table: that centres every column on an equal share of the width,
    # and the first column here is a circuit name rather than a digit. The
    # pitch is still measured.
    fig, ax = plt.subplots(figsize=(11.6, 3.30))
    fig.subplots_adjust(left=0.015, right=0.985, top=0.97, bottom=0.03)
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    pitch = _row_pitch(fig, ax, 20)
    xs = (0.00, 0.41, 0.67, 0.89)
    heads = ("circuit", "OFF when empty?", "paths equal?", "result")

    y = 1.0 - pitch * 0.7
    ax.text(0.0, y, "Two conditions, and neither is enough on its own",
            fontsize=21, color=INK, fontweight="bold", va="top")
    y -= pitch * 1.5
    for x, h in zip(xs, heads):
        ax.text(x, y, h, fontsize=20, color=MUTED, va="center",
                ha="left" if x == 0.0 else "center", fontweight="bold")
    y -= pitch * 0.55
    ax.plot([0.0, 1.0], [y, y], color=RULE, lw=1.4)
    y -= pitch * 0.8
    for name, fs, bal, verdict in rows:
        colour = GREEN if verdict == "clean" else RED
        ax.text(xs[0], y, name, fontsize=20, color=INK, va="center")
        for x, v in zip(xs[1:3], (fs, bal)):
            ax.text(x, y, v, fontsize=20, color=INK, va="center",
                    ha="center", fontfamily="DejaVu Sans Mono")
        ax.text(xs[3], y, verdict, fontsize=20, color=colour, va="center",
                ha="center", fontweight="bold")
        y -= pitch
    ax.text(0.0, y - pitch * 0.2,
            "The middle two rows are the counterexamples: one for each "
            "condition on its own.",
            fontsize=20, color=MUTED, va="top")
    _save(fig, "s16_two_conditions")



# ---------------------------------------------------------------------------
# 9. the Cello gate itself, before the room is asked to use it
#
# Adam, 18 October: "we need to directly explain the VOIGT NOR and how it
# works before we use it." The deck derived NOR from promoter occupancy and
# then used the word for the rest of the hour without ever drawing the part.
# The part matters because of what its input and output ARE: both are
# promoter activities, which is the whole reason gates compose.
#
# It also resolves a collision the deck had set up for itself. fig_arch_nand
# draws two tandem promoters over one gene and calls it NAND; Cello draws the
# same DNA and calls it NOR. Both are right, and the difference is which
# variable you call the input -- a repressor concentration in ours, a
# promoter activity in theirs. Said out loud, that is a good lesson. Left
# implicit, it is a trap.
# ---------------------------------------------------------------------------
def fig_voigt_nor():
    """A Cello gate: two input promoters, one repressor, one output promoter."""
    fig, (axd, axt) = plt.subplots(1, 2, figsize=(12.2, 4.60),
                                   gridspec_kw={"width_ratios": [1.75, 1.0]})
    fig.subplots_adjust(top=0.90, bottom=0.14, wspace=0.12)
    axd.set_axis_off(); axd.set_xlim(0, 1); axd.set_ylim(0, 1)

    def prom(x, y, label, colour):
        axd.plot([x, x], [y, y + 0.115], color=colour, lw=3.0)
        axd.annotate("", xy=(x + 0.085, y + 0.115), xytext=(x, y + 0.115),
                     arrowprops=dict(arrowstyle="-|>", color=colour, lw=3.0,
                                     mutation_scale=16))
        axd.text(x, y + 0.155, label, ha="left", va="bottom", fontsize=20,
                 color=colour, fontweight="bold")

    y = 0.60
    axd.plot([0.01, 0.99], [y, y], color=INK, lw=3.0, solid_capstyle="butt")
    prom(0.04, y, "input 1", TEAL)
    prom(0.30, y, "input 2", TEAL)
    axd.add_patch(plt.Rectangle((0.56, y - 0.060), 0.36, 0.120,
                                facecolor="white", edgecolor=AMBER, lw=2.4,
                                zorder=3))
    axd.text(0.74, y, "repressor", ha="center", va="center", fontsize=20,
             color=INK, zorder=4)

    y2 = 0.16
    axd.plot([0.01, 0.99], [y2, y2], color=INK, lw=3.0, solid_capstyle="butt")
    axd.add_patch(plt.Rectangle((0.14, y2 - 0.042), 0.12, 0.084,
                                facecolor=AMBER, edgecolor=INK, lw=1.8,
                                zorder=3))
    prom(0.33, y2, "output", GREEN)
    axd.text(0.60, y2 + 0.075, "to the next gate", ha="left",
             va="bottom", fontsize=20, color=MUTED)

    _repress(axd, (0.74, y - 0.075), (0.205, y2 + 0.055), color=AMBER)

    axd.text(0.0, -0.14,
             "A gate's input and its output are both\n"
             "PROMOTER ACTIVITIES, in RPU.\n"
             "That is why gates plug into each other.",
             fontsize=20, color=INK, ha="left", va="top")
    axd.set_title("one Cello gate", fontsize=20, color=INK, loc="left",
                  fontweight="bold")

    tt = TruthTable.from_function(("in1", "in2"),
                                  lambda a, b: not (a or b), name="output")
    rows = [[int(a), int(b), int(tt(a, b))] for (a, b) in sorted(tt.rows)]
    ty, tp = _table(axt, fig, ["in 1", "in 2", "out"], rows, fontsize=20,
                    title="NOR")
    axt.text(0.0, ty - tp * 0.9,
             "Either input firing makes\nthe repressor, which shuts\n"
             "the output promoter.",
             fontsize=20, color=MUTED, va="top")
    _save(fig, "s16_voigt_nor")


# ---------------------------------------------------------------------------
# 10. what an inversion is, and the two ways to place two pairs of sites
#
# The memory half went from "an invertase reverses the stretch of DNA between
# two sites" in words, straight to a five-node state graph. The room had
# never seen a recombination site, an inversion, or what "staggered" means.
# ---------------------------------------------------------------------------
def _site(ax, x, y, right=True, colour=TEAL, label=None):
    """One recombination site, as a triangle pointing along the strand."""
    d = 0.016 if right else -0.016
    ax.add_patch(plt.Polygon([(x - d, y - 0.055), (x - d, y + 0.055),
                              (x + d, y)], closed=True, facecolor=colour,
                             edgecolor=INK, lw=1.4, zorder=4))
    if label:
        ax.text(x, y + 0.085, label, ha="center", va="bottom", fontsize=20,
                color=colour, fontweight="bold")


def _segment(ax, x0, x1, y, label, colour, forward=True):
    """A block arrow for the DNA between two sites, pointing with its sense."""
    tip = 0.030
    if forward:
        pts = [(x0, y - 0.045), (x1 - tip, y - 0.045), (x1, y),
               (x1 - tip, y + 0.045), (x0, y + 0.045)]
    else:
        pts = [(x1, y - 0.045), (x0 + tip, y - 0.045), (x0, y),
               (x0 + tip, y + 0.045), (x1, y + 0.045)]
    ax.add_patch(plt.Polygon(pts, closed=True, facecolor=colour,
                             edgecolor=INK, lw=1.4, alpha=0.85, zorder=3))
    ax.text((x0 + x1) / 2, y, label, ha="center", va="center", fontsize=20,
            color="white", fontweight="bold", zorder=5)


def fig_inversion():
    """What an invertase does to DNA, and nested against staggered sites."""
    fig, axs = plt.subplot_mosaic([["top", "top"], ["left", "right"]],
                                  figsize=(11.6, 4.90),
                                  height_ratios=[1.0, 1.05])
    fig.subplots_adjust(top=0.90, bottom=0.02, hspace=0.55, wspace=0.10)
    ax1, axL, axR = axs["top"], axs["left"], axs["right"]
    for ax in (ax1, axL, axR):
        ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    ax1.set_title("an invertase flips the DNA between its two sites: "
                  "sequence, direction and all",
                  fontsize=20, color=INK, loc="left", fontweight="bold")
    for y, fwd, tag in ((0.76, True, "before"), (0.16, False, "after")):
        ax1.plot([0.16, 0.90], [y, y], color=INK, lw=3.0)
        _site(ax1, 0.28, y, right=True, label="site" if fwd else None)
        _segment(ax1, 0.32, 0.74, y, "gene", TEAL, forward=fwd)
        _site(ax1, 0.78, y, right=False, label="site" if fwd else None)
        ax1.text(0.13, y, tag, ha="right", va="center", fontsize=20,
                 color=MUTED)
    ax1.annotate("", xy=(0.53, 0.34), xytext=(0.53, 0.58),
                 arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=3.0,
                                 mutation_scale=18))
    ax1.text(0.56, 0.46, "invertase", ha="left", va="center", fontsize=20,
             color=AMBER, fontweight="bold")

    # The two layouts sit SIDE BY SIDE rather than stacked: stacked, the
    # first caption and the second heading had nowhere to go without making
    # the figure taller than the slide band.
    #
    # The site triangles within a pair point AT each other. A pair of sites
    # in inverted orientation is what makes an inversion rather than an
    # excision, and drawing them all one way would teach the wrong thing on
    # the figure whose whole subject is where the sites go.
    panels = [(axL, "NESTED", "one pair sits inside the other",
               [(0.10, "a", TEAL, True), (0.33, "b", AMBER, True),
                (0.62, "b", AMBER, False), (0.86, "a", TEAL, False)],
               "they commute:\n2\u207f states, a register"),
              (axR, "STAGGERED", "the pairs interleave",
               [(0.10, "a", TEAL, True), (0.36, "b", AMBER, True),
                (0.61, "a", TEAL, False), (0.86, "b", AMBER, False)],
               "they do not:\nthe ORDER is part of the state")]
    for ax, head, sub, sites, tail in panels:
        ax.text(0.0, 0.93, head, ha="left", va="top", fontsize=20,
                color=INK, fontweight="bold")
        ax.text(0.0, 0.76, sub, ha="left", va="top", fontsize=20, color=MUTED)
        ax.plot([0.03, 0.93], [0.36, 0.36], color=INK, lw=3.0)
        for x, lab, col, right in sites:
            _site(ax, x, 0.36, right=right, colour=col, label=lab)
        ax.text(0.0, 0.16, tail, ha="left", va="top", fontsize=20, color=INK)
    _save(fig, "s16_inversion")


# ---------------------------------------------------------------------------
# 11. the SR latch as a circuit, before the state table
# ---------------------------------------------------------------------------
def fig_sr_circuit():
    """Two cross-coupled NOR genes, and what the two letters mean."""
    fig, ax = plt.subplots(figsize=(11.6, 3.90))
    fig.subplots_adjust(top=0.88, bottom=0.04, left=0.015, right=0.985)
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    _gene(ax, 0.40, 0.78, "Q", w=0.13, h=0.17)
    _gene(ax, 0.40, 0.22, "¬Q", w=0.13, h=0.17)
    ax.text(0.09, 0.78, "R", fontsize=20, color=RED, fontweight="bold",
            ha="center", va="center")
    ax.text(0.09, 0.22, "S", fontsize=20, color=RED, fontweight="bold",
            ha="center", va="center")
    _repress(ax, (0.125, 0.78), (0.328, 0.78))
    _repress(ax, (0.125, 0.22), (0.328, 0.22))
    # the cross-coupling, routed around the boxes rather than through them
    ax.plot([0.47, 0.56, 0.56, 0.34, 0.34], [0.22, 0.22, 0.62, 0.62, 0.70],
            color=RED, lw=2.2, zorder=1)
    ax.plot([0.47, 0.62, 0.62, 0.30, 0.30], [0.78, 0.78, 0.38, 0.38, 0.30],
            color=RED, lw=2.2, zorder=1)
    for x, y in ((0.34, 0.700), (0.30, 0.300)):
        ax.plot([x - 0.022, x + 0.022], [y, y], color=RED, lw=3.2, zorder=2)
    ax.text(0.655, 0.78, "Q", fontsize=20, color=TEAL, fontweight="bold",
            va="center")
    ax.text(0.655, 0.22, "¬Q", fontsize=20, color=TEAL, fontweight="bold",
            va="center")

    ax.text(0.72, 0.92,
            "S for SET, R for RESET.\n\n"
            "S = 1  drives Q to 1.\n"
            "R = 1  drives Q to 0.\n"
            "S = R = 0  holds whatever\n"
            "Q already was. That hold is\n"
            "the memory.\n\n"
            "S = R = 1 is forbidden: it\n"
            "pushes BOTH low, and what\n"
            "happens next depends on\n"
            "which input falls first.",
            fontsize=20, color=MUTED, ha="left", va="top")
    ax.set_title("each gene is a NOR: an input, and the other gene's product",
                 fontsize=20, color=INK, loc="left", fontweight="bold")
    _save(fig, "s16_sr_circuit")


FIGURES = [fig_arch_nor, fig_arch_nand, fig_universal,
           fig_voigt_nor, fig_inversion, fig_sr_circuit,
           fig_xnor_two_ways, fig_two_conditions,
           fig_classifier, fig_timing_steps, fig_cold_start,
           fig_timing_broken, fig_timing_fixed,
           fig_hazard_types, fig_cascade_delay, fig_dirs_states,
           fig_latch_state_table]


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for f in FIGURES:
        f()
        print(f.__name__, "ok")
