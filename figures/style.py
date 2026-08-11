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
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11.5,
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
