"""Shared matplotlib style, keyed to the course palette.

Import this at the top of every figure script so lecture slides, notebooks and
problem sets all look like one course.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

TEAL   = "#0E4F57"
GREEN  = "#1A4D33"
CYAN   = "#4FD1C5"
MINT   = "#A5D6A7"
AMBER  = "#D98E32"
RED    = "#B3261E"
INK    = "#0B3A3F"
MUTED  = "#6E8B87"
RULE   = "#D3DEDA"

CYCLE = [TEAL, CYAN, AMBER, GREEN, RED, MUTED]


# Type scale inside a figure, mirroring theme.TYPE for slides.
#
# The old numbers here (font 15, labels 15, ticks 14, legend 14) came with a
# comment saying a figure is "scaled into a 13in slide", so small type inside
# it grows. That has not been true since `_fig()` started placing figures at
# pixels/dpi with savefig.dpi = 160: the scale is exactly 1.000, so a point
# authored here is a point on the wall. The rcParams were therefore setting a
# course-wide content floor of 14, against a stated floor of 20.
#
# Roles match decks/theme.py: nothing below 20 carries content; caption (16)
# is for source lines and figure refs; micro (12) is for nothing that is read.
# One knob -- change the dict, rebuild, and every figure moves. See
# posb-slide-legibility.
TYPE = {"micro": 12, "caption": 16, "body": 20, "emphasis": 24, "title": 26}

# Modules authored against the old 14--16 floor whose layouts have not yet
# been re-checked at 20. They render with the legacy scale and are REPORTED by
# tools/build_figures.py every build, so nobody believes they are clean. The
# list only ever shrinks -- same contract as GRANDFATHERED in build_decks.py.
LEGACY_SCALE = {
    "s01_specification", "s02_movie", "s02_substrate", "s03_modeling_i",
    "s04_modeling_ii", "s05_expression", "s06_promoter_occupancy",
    "s07_autoregulation", "s08_phase_plane", "s09_bistability",
    "s10_feedforward", "s11_oscillators", "s12_noise", "s13_digital",
    "s14_movie", "s14_review",
}

_LEGACY = {"font.size": 15, "axes.titlesize": 16, "axes.labelsize": 15,
           "xtick.labelsize": 14, "ytick.labelsize": 14, "legend.fontsize": 14}


def use(legacy=False):
    """Apply the course style. `legacy=True` keeps the pre-20pt figure scale.

    Callers in LEGACY_SCALE pass legacy=True until their layouts have been
    re-checked at the content floor; everything else gets the floor.
    """
    scale = _LEGACY if legacy else {
        "font.size": TYPE["body"],
        "axes.titlesize": TYPE["body"],
        "axes.labelsize": TYPE["body"],
        "xtick.labelsize": TYPE["body"],
        "ytick.labelsize": TYPE["body"],
        "legend.fontsize": TYPE["body"],
    }
    mpl.rcParams.update({
        "figure.dpi": 160,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        **scale,
        "lines.linewidth": 2.6,
        # The slide ground, so the figure does not sit in a white rectangle.
        "figure.facecolor": "#F8FAF9",
        "axes.facecolor": "#F8FAF9",
        "savefig.facecolor": "#F8FAF9",
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.prop_cycle": mpl.cycler(color=CYCLE),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "grid.color": RULE,
        "legend.frameon": False,
    })
    return plt
