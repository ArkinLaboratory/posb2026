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


def use():
    mpl.rcParams.update({
        "figure.dpi": 160,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        # Projected in a lecture hall: 11pt inside a figure that is then
        # scaled into a 13in slide lands around 7pt of ink on the wall. The
        # floor is 15.
        "font.size": 15,
        "axes.titlesize": 16,
        "axes.labelsize": 15,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "legend.fontsize": 14,
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
