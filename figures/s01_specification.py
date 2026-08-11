"""Session 1 figures.

One figure, and it is the spine of the whole course: the pipeline from a
specification to a working cell, drawn with the places it actually breaks marked
on it. Session 1 introduces it; every later session is a return to one of the
gaps.

    python tools/build_figures.py s01
"""
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from figures.style import use, AMBER, INK, MUTED, RED, RULE, TEAL

plt = use()
OUT = "figures/build"

# Each stage: label, the question it answers, and whether the field can do it.
# `gap` is what breaks on the way OUT of this stage, and the session that treats
# it -- which is the only reason this figure is worth drawing rather than saying.
STAGES = [
    ("SPECIFY", "what should it do?", "no",
     "There is no language for this.\nEvery spec here is English.", "1, 27"),
    ("DESIGN", "what circuit computes it?", "partly",
     "Works on paper. Predicts\nthe wrong numbers.", "3–13, 16"),
    ("BUILD", "assemble the DNA", "yes",
     "Genuinely solved.\nSynthesis is not the bottleneck.", "17"),
    ("RUN IN A HOST", "does it work in a cell?", "partly",
     "Parts change value in\ncontext. Load is not free.", "18–21"),
    ("KEEP WORKING", "for how long, out there?", "no",
     "Burden, mutation, selection,\nan environment you don't control.", "19, 22–25"),
]

VERDICT = {"yes": TEAL, "partly": AMBER, "no": RED}


def fig_pipeline():
    """Specification to working cell, with the handoffs that actually break."""
    fig, ax = plt.subplots(figsize=(11.5, 3.5))
    ax.set_xlim(0, 10 * len(STAGES))
    ax.set_ylim(-3.6, 3.4)
    ax.axis("off")

    w, h = 9.1, 1.5
    for i, (name, q, verdict, gap, sess) in enumerate(STAGES):
        x = i * 10 + 0.4
        c = VERDICT[verdict]

        ax.add_patch(FancyBboxPatch(
            (x, -h / 2), w, h, boxstyle="round,pad=0.25,rounding_size=0.5",
            facecolor="white", edgecolor=c, linewidth=2.0, zorder=3))
        ax.text(x + w / 2, 0.34, name, ha="center", va="center", zorder=4,
                fontsize=11, fontweight="bold", color=INK)
        ax.text(x + w / 2, -0.32, q, ha="center", va="center", zorder=4,
                fontsize=8.5, style="italic", color=MUTED)

        # The gap sits BELOW the arrow leaving the stage, because it is what
        # goes wrong in the handoff, not inside the box.
        if i < len(STAGES) - 1:
            ax.add_patch(FancyArrowPatch(
                (x + w + 0.05, 0), (x + 10 + 0.30, 0),
                arrowstyle="-|>", mutation_scale=16,
                linewidth=1.6, color=RULE, zorder=2))

        ax.text(x + w / 2, -1.35, gap, ha="center", va="top", fontsize=8,
                color=c, linespacing=1.45)
        ax.text(x + w / 2, -2.62, f"sessions {sess}", ha="center", va="top",
                fontsize=8, color=MUTED, fontweight="bold")

    for i, (lab, c) in enumerate([("solved", TEAL), ("partly", AMBER),
                                  ("not solved", RED)]):
        ax.plot([0.8 + i * 7.5], [2.75], "s", color=c, markersize=7)
        ax.text(1.6 + i * 7.5, 2.75, lab, va="center", fontsize=9, color=INK)

    ax.text(10 * len(STAGES) - 0.4, 2.75,
            "the pipeline is only as good as its worst handoff",
            ha="right", va="center", fontsize=9.5, style="italic", color=MUTED)

    fig.savefig(f"{OUT}/s01_pipeline.png")
    plt.close(fig)


FIGURES = [fig_pipeline]
