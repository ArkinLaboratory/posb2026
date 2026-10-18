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
    classifier_2025, classifier_fixed, GateNetwork, NOT, NOR, hazards,
    TruthTable, cascade_half_time, cascade_step_response,
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
    _gene(axc, 0.38, 0.88, "R1"); _gene(axc, 0.61, 0.67, "R2")
    _gene(axc, 0.85, 0.67, "R3", edge=AMBER)

    _repress(axc, (0.175, 0.88), (0.292, 0.88))          # B -| R1
    _repress(axc, (0.175, 0.49), (0.535, 0.620))         # A -| R2
    _repress(axc, (0.448, 0.840), (0.580, 0.742))        # R1 -| R2
    _repress(axc, (0.695, 0.67), (0.763, 0.67))          # R2 -| R3

    axc.text(0.935, 0.67, "out", fontsize=20, color=AMBER,
             ha="left", va="center")
    axc.text(0.0, 0.25, "R1 = NOT B", fontsize=20, color=MUTED, ha="left")
    axc.text(0.0, 0.15,
             "R2 has two promoters, each independently repressed,\n"
             "so either repressor silences it  →  NAND(A, R1)",
             fontsize=16, color=MUTED, ha="left", va="top")
    axc.set_title("A AND NOT B, built from repressors", loc="left")

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
             "Fix the promoter, not the wiring:\n"
             "make the output REQUIRE an activator.",
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
    runs = [("hold Q=1  (S=0 R=0)", {"S": 0, "R": 0},
             {"Q": True, "Qbar": False}),
            ("hold Q=0  (S=0 R=0)", {"S": 0, "R": 0},
             {"Q": False, "Qbar": True}),
            ("SET  (S=1 R=0)", {"S": 1, "R": 0}, {"Q": False, "Qbar": True}),
            ("RESET  (S=0 R=1)", {"S": 0, "R": 1}, {"Q": True, "Qbar": False})]

    fig, axes = plt.subplots(1, 4, figsize=(12.0, 3.80))
    fig.subplots_adjust(top=0.70, bottom=0.08)
    for ax, (label, assign, init) in zip(axes, runs):
        tbl = latch.timing_table(assign, initial=init, ticks=4)
        rows = [[r["t"], int(r["Q"]), int(r["Qbar"])] for r in tbl]
        _table(ax, fig, ["t", "Q", "Q̄"], rows, fontsize=20, title=label)
    fig.suptitle("session 9's toggle, named: an SR latch", fontsize=24,
                 color=INK, y=0.97)
    _save(fig, "s16_latch_state_table")

# ---------------------------------------------------------------------------
# 6. where the gate comes from -- the DNA architecture, and the rate law drawn
# ---------------------------------------------------------------------------
def _dna(ax, x0, x1, y, *, operators, label, gene="output"):
    """A stretch of DNA: operator boxes, a promoter arrow, and the gene."""
    ax.plot([x0, x1], [y, y], color=INK, lw=2.6, solid_capstyle="butt")
    n = len(operators)
    for i, (name, col) in enumerate(operators):
        bx = x0 + 0.08 + i * 0.13
        ax.add_patch(plt.Rectangle((bx, y - 0.035), 0.11, 0.07,
                                   facecolor=col, edgecolor=INK, lw=1.6,
                                   zorder=3))
        ax.text(bx + 0.055, y + 0.075, name, ha="center", va="bottom",
                fontsize=16, color=col, fontweight="bold")
    px = x0 + 0.10 + n * 0.13
    ax.annotate("", xy=(px + 0.10, y + 0.085), xytext=(px, y + 0.085),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.2,
                                mutation_scale=14))
    ax.plot([px, px], [y, y + 0.085], color=GREEN, lw=2.2)
    ax.add_patch(plt.Rectangle((px + 0.12, y - 0.045), 0.30, 0.09,
                               facecolor="white", edgecolor=TEAL, lw=2.0,
                               zorder=3))
    ax.text(px + 0.27, y, gene, ha="center", va="center", fontsize=16,
            color=INK, zorder=4)
    ax.text(x0, y - 0.11, label, ha="left", va="top", fontsize=16,
            color=MUTED)


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
    for y, ops, gene in strands:
        _dna(axd, 0.02, 0.98, y, operators=ops, label="", gene=gene)
    axd.text(0.02, 0.06, caption, ha="left", va="bottom", fontsize=16,
             color=MUTED)
    fig.suptitle(title, fontsize=20, color=INK, fontweight="bold", y=0.96)

    im = axp.pcolormesh(r, r, P(*np.meshgrid(r, r)), cmap=cmap,
                        shading="auto", vmin=0.0, vmax=1.0)
    axp.set_xscale("log"); axp.set_yscale("log")
    axp.set_xlabel("repressor A  (units of K)", fontsize=18)
    axp.set_ylabel("repressor B  (units of K)", fontsize=18)
    axp.tick_params(labelsize=16)
    for (i, j), v in corners.items():
        axp.text(10 ** (-1.6 + 3.2 * i), 10 ** (-1.6 + 3.2 * j), v,
                 ha="center", va="center", fontsize=22, fontweight="bold",
                 color="white" if v == "1" else INK,
                 bbox=dict(boxstyle="circle,pad=0.20",
                           fc=INK if v == "1" else "white", ec=INK, lw=1.8))
    fig.colorbar(im, ax=axp, fraction=0.045, pad=0.03)
    _save(fig, name)


def fig_arch_nor():
    """One promoter with two operators: either repressor silences it -- NOR."""
    _arch("s16_arch_nor",
          "ONE promoter, TWO operators   \u2192   P_on = 1 / (1+r_A)(1+r_B)",
          [(0.55, [("A", AMBER), ("B", RED)], "output")],
          lambda A, B: 1.0 / ((1.0 + A) * (1.0 + B)),
          {(0, 0): "1", (1, 0): "0", (0, 1): "0", (1, 1): "0"},
          "Either repressor blocks it.")


def fig_arch_nand():
    """Two promoters driving one gene: both must be blocked -- NAND."""
    _arch("s16_arch_nand",
          "TWO promoters, ONE gene   \u2192   out \u221d 1/(1+r_A) + 1/(1+r_B)",
          [(0.74, [("A", AMBER)], "out"), (0.34, [("B", RED)], "out")],
          lambda A, B: 0.5 * (1.0 / (1.0 + A) + 1.0 / (1.0 + B)),
          {(0, 0): "1", (1, 0): "1", (0, 1): "1", (1, 1): "0"},
          "Outputs add: silent only if\nboth are blocked.")


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
    for x in (0.285, 0.675):
        ax.annotate("", xy=(x + 0.040, 0.53), xytext=(x, 0.53),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.4,
                                    mutation_scale=16))
    ax.text(0.5, 0.10,
            "NOR is NOT(OR).   NAND is NOT(AND).\nEach packs both "
            "ingredients into one promoter,\nso either one, alone, can "
            "build anything.",
            ha="center", va="center", fontsize=18, color=INK)
    _save(fig, "s16_universal")


FIGURES = [fig_arch_nor, fig_arch_nand, fig_universal,
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
