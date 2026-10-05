"""Session 13 figures — the digital abstraction, and what it costs.

Everything comes from `posb.digital`: `Repressor`, `noise_margins`,
`rbs_window` and `loglinear_range_hill` are what the students call after they
have found a unity-gain point by hand. The gate used throughout is

    y = y_min + (y_max - y_min)/(1 + (x/K)^n),   K = 1, y_max/y_min = 100

in units of the receiving promoter's K, so one gate can feed an identical one.

Run:  python tools/build_figures.py s13
"""
import numpy as np

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN, RULE
from posb.digital import Repressor, noise_margins, rbs_window, loglinear_range_hill

plt = use()
OUT = "figures/build"
XS = np.logspace(-2, 2.5, 600)
GATE = Repressor(0.1, 10.0, 1.0, 2.0, "n = 2")


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _curve(ax, g, color=TEAL, lw=3.0, label=None):
    ax.loglog(XS, g(XS), color=color, lw=lw, label=label)
    ax.set_xlabel("input  x / K")
    ax.set_ylabel("output  y / K")


# ---------------------------------------------------------------------------
# 1. The derivation's pictures, one per step
# ---------------------------------------------------------------------------
def fig_gain_steps():
    """Four panels for the split surface: curve, gain, n, thresholds."""
    # p1 -- the transfer curve, log-log
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    _curve(ax, GATE)
    ax.set_title("a leaky repressor, n = 2")
    ax.text(0.012, 0.13, "leak  y_min", color=MUTED, fontsize=15)
    ax.text(0.012, 6.0, "y_max", color=MUTED, fontsize=15)
    _save(fig, "s13_gain_p1")

    # p2 -- gain magnitude, leak-free against leaky
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    free = Repressor(1e-9, 10.0, 1.0, 2.0)
    ax.semilogx(XS, np.abs(free.gain(XS)), color=MUTED, lw=2.4, ls="--",
                label="no leak:  g")
    ax.semilogx(XS, np.abs(GATE.gain(XS)), color=TEAL, lw=3.0, label="with leak")
    ax.axhline(1.0, color=RED, lw=1.6)
    ax.text(0.012, 1.06, "|G| = 1", color=RED, fontsize=15)
    ax.set_ylim(0, 2.2)
    ax.set_xlabel("input  x / K")
    ax.set_ylabel("|gain|  =  |d ln y / d ln x|")
    ax.set_title("the leak pulls the gain back down")
    ax.legend(loc="upper left")
    _save(fig, "s13_gain_p2")

    # p3 -- cooperativity: n = 1 never restores
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    for n, c in [(1, MUTED), (2, TEAL), (4, CYAN)]:
        g = Repressor(0.1, 10.0, 1.0, n)
        ax.semilogx(XS, np.abs(g.gain(XS)), color=c, lw=3.0, label=f"n = {n}")
    ax.axhline(1.0, color=RED, lw=1.6)
    ax.set_ylim(0, 3.6)
    ax.set_xlabel("input  x / K")
    ax.set_ylabel("|gain|")
    ax.set_title("n = 1 never gets above 1")
    ax.legend(loc="upper left")
    _save(fig, "s13_gain_p3")

    # p4 -- the thresholds and output levels on the curve
    x_il, x_ih = GATE.thresholds()
    y_ol, y_oh = GATE.output_levels()
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    _curve(ax, GATE)
    ax.axvspan(x_il, x_ih, color=AMBER, alpha=0.18, lw=0)
    for x, lab in [(x_il, "x_IL"), (x_ih, "x_IH")]:
        ax.axvline(x, color=AMBER, lw=1.8, ls="--")
        ax.text(x * 1.08, 0.035, lab, color=AMBER, fontsize=15)
    ax.plot([x_il, x_ih], [y_oh, y_ol], "o", ms=11, color=RED, zorder=5)
    ax.text(x_il * 0.012, y_oh * 0.45, f"y_OH = {y_oh:.2f}", color=RED, fontsize=15)
    ax.text(x_ih * 1.15, y_ol * 1.35, f"y_OL = {y_ol:.2f}", color=RED, fontsize=15)
    ax.set_ylim(0.03, 30)
    ax.set_title("the band where |G| > 1")
    _save(fig, "s13_gain_p4")
    return x_il, x_ih, y_ol, y_oh


# ---------------------------------------------------------------------------
# 2. Signal matching: the sender's output against the receiver's thresholds
# ---------------------------------------------------------------------------
def _levels(ax, sender, receiver, title):
    x_il, x_ih = receiver.thresholds()
    y_ol, y_oh = sender.output_levels()
    nml, nmh = noise_margins(sender, receiver)
    ax.set_yscale("log")
    ax.set_ylim(0.03, 100)
    ax.set_xlim(0, 3)
    ax.set_xticks([0.75, 2.25])
    ax.set_xticklabels(["sender\nemits", "receiver\nreads"])
    # receiver: LOW below x_IL, forbidden between, HIGH above x_IH
    ax.fill_between([1.6, 2.9], 0.03, x_il, color=CYAN, alpha=0.30, lw=0)
    ax.fill_between([1.6, 2.9], x_il, x_ih, color=RULE, alpha=0.9, lw=0)
    ax.fill_between([1.6, 2.9], x_ih, 100, color=TEAL, alpha=0.30, lw=0)
    ax.text(2.25, np.sqrt(0.03 * x_il), "LOW", ha="center", va="center", fontsize=15)
    ax.text(2.25, np.sqrt(x_il * x_ih), "?", ha="center", va="center", fontsize=18)
    ax.text(2.25, np.sqrt(x_ih * 100), "HIGH", ha="center", va="center", fontsize=15)
    # sender: worst-case output levels
    for y, lab in [(y_ol, "y_OL"), (y_oh, "y_OH")]:
        ax.plot([0.1, 1.4], [y, y], color=INK, lw=3.0)
        ax.text(0.12, y * 1.15, f"{lab} {y:.2f}", fontsize=14, color=INK)
        ax.plot([1.4, 1.6], [y, y], color=MUTED, lw=1.2, ls=":")
    ok_l, ok_h = nml >= 0, nmh >= 0
    ax.set_title(f"{title}\nNM_L {nml:+.2f}   NM_H {nmh:+.2f}  decades",
                 color=INK if (ok_l and ok_h) else RED, fontsize=15)
    ax.set_ylabel("concentration / K")
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)


def fig_self_match():
    """The n = 2 gate driving an identical gate: as built, then retuned."""
    lo, hi = rbs_window(GATE, GATE)
    mid = GATE.scaled(np.sqrt(lo * hi))
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8))
    _levels(axes[0], GATE, GATE, "as built: y_max = 10 K")
    _levels(axes[1], mid, mid, f"RBS x{np.sqrt(lo * hi):.2f}: y_max = {mid.y_max:.1f} K")
    _save(fig, "s13_self_match")
    return lo, hi, noise_margins(GATE, GATE), noise_margins(mid, mid)


def fig_rbs_window():
    """Both margins against the RBS scale factor, for n = 2 and n = 4."""
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    fs = np.logspace(-0.5, 1.5, 300)
    out = []
    for n, c in [(2, TEAL), (4, CYAN)]:
        g = Repressor(0.1, 10.0, 1.0, n)
        nml = [noise_margins(g.scaled(f), g.scaled(f))[0] for f in fs]
        nmh = [noise_margins(g.scaled(f), g.scaled(f))[1] for f in fs]
        ax.semilogx(fs, nml, color=c, lw=2.6, ls="--")
        ax.semilogx(fs, nmh, color=c, lw=2.6, label=f"n = {n}")
        lo, hi = rbs_window(g, g)
        ax.axvspan(lo, hi, color=c, alpha=0.12, lw=0)
        out.append((n, lo, hi, hi / lo))
    ax.axhline(0, color=RED, lw=1.4)
    ax.set_xlabel("RBS scale factor on y_max = 10 K")
    ax.set_ylabel("noise margin  (decades)")
    ax.set_title("solid: NM_H   dashed: NM_L")
    ax.legend(loc="upper left")
    _save(fig, "s13_rbs_window")
    return out


# ---------------------------------------------------------------------------
# 3. Cascades: gains multiply, if the thresholds line up
# ---------------------------------------------------------------------------
def fig_cascade():
    """Two inverters in series. Aligned: the steep parts overlap and the
    gains multiply. Misaligned: the second stage sits on a plateau."""
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4))
    a = Repressor(0.1, 10.0, 1.0, 2.0)
    for ax, (b, title) in zip(axes, [
            (Repressor(0.1, 10.0, 1.0, 2.0), "second stage centred on the first's swing"),
            (Repressor(0.1, 10.0, 30.0, 2.0), "second stage's K 30x too high")]):
        y1 = a(XS)
        z = b(y1)
        ax.loglog(XS, y1, color=MUTED, lw=2.2, ls="--", label="stage 1 alone")
        ax.loglog(XS, z, color=TEAL, lw=3.0, label="two stages")
        g2 = np.abs(a.gain(XS) * b.gain(y1))
        ax.set_title(title, fontsize=14)
        ax.text(0.012, 0.04, f"peak |G|: {np.abs(a.gain(XS)).max():.2f} -> {g2.max():.2f}",
                fontsize=14, color=INK)
        ax.set_ylim(0.02, 30)
        ax.set_xlabel("input  x / K")
    axes[0].set_ylabel("output / K")
    axes[0].legend(loc="center left", fontsize=13)
    _save(fig, "s13_cascade")


# ---------------------------------------------------------------------------
# 4. The analog half: how wide is a logarithm?
# ---------------------------------------------------------------------------
def fig_loglinear():
    """Slope on a log axis, d y/d ln x, for Hill curves and for ln(1 + x)."""
    xs = np.logspace(-3, 4, 800)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4))
    ax = axes[0]
    for n, c in [(1, TEAL), (2, CYAN), (4, AMBER)]:
        y = xs ** n / (1 + xs ** n)
        ax.semilogx(xs, y, color=c, lw=2.8, label=f"Hill, n = {n}")
    ax.semilogx(xs, np.log1p(xs) / np.log1p(xs[-1]), color=RED, lw=2.8,
                ls="--", label="ln(1 + x), scaled")
    ax.set_xlabel("input  x")
    ax.set_ylabel("output (scaled to 1)")
    ax.set_title("on a log axis")
    ax.legend(loc="upper left", fontsize=12)
    ax = axes[1]
    for n, c in [(1, TEAL), (2, CYAN), (4, AMBER)]:
        y = xs ** n / (1 + xs ** n)
        s = n * y * (1 - y)
        ax.semilogx(xs, s / s.max(), color=c, lw=2.8,
                    label=f"n = {n}: {loglinear_range_hill(n):.1f}-fold")
    s = xs / (1 + xs)
    ax.semilogx(xs, s, color=RED, lw=2.8, ls="--", label="ln(1 + x): no ceiling")
    ax.axhline(0.75, color=MUTED, lw=1.2, ls=":")
    ax.set_ylim(0, 1.1)
    ax.set_xlabel("input  x")
    ax.set_ylabel("slope on a log axis, scaled")
    ax.set_title("where it is a straight line")
    ax.legend(loc="upper left", fontsize=12)
    ax.set_ylim(0, 1.6)
    _save(fig, "s13_loglinear")


def fig_loglinear_panels():
    """The two halves of fig_loglinear sized for the split surface."""
    xs = np.logspace(-3, 4, 800)
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    for n, c in [(1, TEAL), (2, CYAN)]:
        y = xs ** n / (1 + xs ** n)
        ax.semilogx(xs, y, color=c, lw=2.8, label=f"Hill, n = {n}")
    ax.semilogx(xs, np.log1p(xs) / np.log1p(xs[-1]), color=RED, lw=2.8,
                ls="--", label="ln(1 + x), scaled")
    ax.set_xlabel("input  x")
    ax.set_ylabel("output, scaled to 1")
    ax.set_title("three curves on a log axis")
    ax.legend(loc="upper left", fontsize=13)
    _save(fig, "s13_loglin_p1")

    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    for n, c in [(1, TEAL), (2, CYAN)]:
        y = xs ** n / (1 + xs ** n)
        sl = n * y * (1 - y)
        ax.semilogx(xs, sl / sl.max(), color=c, lw=2.8,
                    label=f"n = {n}: {loglinear_range_hill(n):.0f}-fold")
    ax.semilogx(xs, xs / (1 + xs), color=RED, lw=2.8, ls="--",
                label="ln(1 + x): no ceiling")
    ax.axhline(0.75, color=MUTED, lw=1.4, ls=":")
    ax.set_ylim(0, 1.55)
    ax.set_xlabel("input  x")
    ax.set_ylabel("slope on a log axis, scaled")
    ax.set_title("where each is a straight line")
    ax.legend(loc="upper left", fontsize=13)
    _save(fig, "s13_loglin_p2")


FIGURES = [fig_gain_steps, fig_self_match, fig_rbs_window, fig_cascade,
           fig_loglinear, fig_loglinear_panels]


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for f in FIGURES:
        r = f()
        if r is not None:
            print(f.__name__, r)
