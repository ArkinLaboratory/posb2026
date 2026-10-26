"""Session 18 — the covalent cycle, as motion.

Separate from `s18_protein.py` for the reason `s02_movie.py` and
`s14_movie.py` are separate from their figure modules: encoding takes seconds
rather than milliseconds, and a module rebuilt on every deck build should not
pay that.

WHAT IT SHOWS, AND WHY IT IS WORTH THE SECONDS. Adam, 25 October 2026, on
segment 2: an animation through the cycle. The static response curve says that
a saturated pair gives a sharp switch; it does not show the thing that makes
the sharpness surprising, which is that NOTHING IS BEING MADE. The pool only
moves. Two cycles run side by side under the same sweep of the stimulus:

    left,  k1 = k2 = 1       the unsaturated pair -- a hyperbola
    right, k1 = k2 = 0.01    the saturated pair   -- a switch

In each, W and W* are drawn as discs whose AREA is the amount in that form, so
the two areas sum to a constant on every frame. That is the conservation law
made visible, and it is the structural fact segment 1 spends two surfaces
establishing. The third panel traces both response curves with a dot on each,
so the room sees the left pair drift while the right pair sits still, sits
still, and then flips.

THE POSTER FRAME is the END of the clip -- both cycles fully modified, both
curves complete -- because `theme.movie()` shows the poster until someone
clicks, and a slide that is never clicked still has to make the argument.

Run:  python3 -m figures.s18_movie
"""
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation

from figures.style import use, TEAL, AMBER, MUTED, INK, RED, RULE, CYAN
from posb import protein

plt = use(legacy=True)          # see figures.style.LEGACY_SCALE
OUT = "figures/build"

FPS = 24
N_FRAME = 200
K_SLACK = 1.0                   # unsaturated pair
K_TIGHT = 0.01                  # saturated pair
U_LO, U_HI = 1e-2, 1e2

# Disc geometry. The discs are drawn with scatter, whose marker size is an
# AREA in points-squared and is independent of the axes' aspect ratio. Drawing
# them as plt.Circle in data coordinates gave ellipses, because these panels
# are not square and never will be. Area carries the amount, so the two areas
# sum to a constant on every frame -- which is the conservation law, visible.
S_MAX = 4200.0
Y_MID = 2.50


def _w(u, k):
    return protein.modified_fraction(u, k, k)


def _draw_cycle(ax, title, k):
    """Static furniture for one cycle. Returns the two discs and the readout."""
    ax.set_xlim(0, 6.2)
    ax.set_ylim(0, 4.7)
    ax.axis("off")
    ax.set_title(title, color=INK, pad=8)

    left, right = 1.6, 4.6
    ghost = ax.scatter([left, right], [Y_MID, Y_MID], s=S_MAX,
                       facecolors="none", edgecolors=RULE, linewidths=1.4,
                       zorder=2)
    unmod = ax.scatter([left], [Y_MID], s=S_MAX, color=TEAL, zorder=3)
    mod = ax.scatter([right], [Y_MID], s=1.0, color=AMBER, zorder=3)

    ax.annotate("", xy=(right - 0.95, Y_MID + 0.62),
                xytext=(left + 0.95, Y_MID + 0.62),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0,
                                connectionstyle="arc3,rad=-0.40"))
    ax.annotate("", xy=(left + 0.95, Y_MID - 0.62),
                xytext=(right - 0.95, Y_MID - 0.62),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0,
                                connectionstyle="arc3,rad=-0.40"))
    ax.text(3.1, Y_MID + 1.42, "kinase", ha="center", color=INK)
    ax.text(3.1, Y_MID - 1.22, "phosphatase", ha="center", color=INK)
    ax.text(left, 0.86, "W", ha="center", color=INK, fontweight="bold")
    ax.text(left, 0.44, "unmodified", ha="center", color=MUTED)
    ax.text(right, 0.86, "W*", ha="center", color=INK, fontweight="bold")
    ax.text(right, 0.44, "modified", ha="center", color=MUTED)
    ax.text(3.1, 4.34, f"$k_1 = k_2$ = {k:g}", ha="center", color=MUTED)
    readout = ax.text(3.1, 0.02, "", ha="center", color=TEAL,
                      fontweight="bold")
    return unmod, mod, readout


def fig_cycle_movie():
    """The pool moving between two forms, slack pair against saturated pair."""
    us = np.logspace(np.log10(U_LO), np.log10(U_HI), N_FRAME)
    w_slack = np.array([_w(u, K_SLACK) for u in us])
    w_tight = np.array([_w(u, K_TIGHT) for u in us])

    fig = plt.figure(figsize=(13.0, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.25],
                          wspace=0.24, left=0.03, right=0.985,
                          bottom=0.17, top=0.90)
    axL, axR, axP = (fig.add_subplot(gs[0, i]) for i in range(3))

    uL, mL, rL = _draw_cycle(axL, "an unsaturated pair", K_SLACK)
    uR, mR, rR = _draw_cycle(axR, "a saturated pair", K_TIGHT)

    axP.plot(us, w_slack, color=TEAL, lw=3.0, label=f"$k$ = {K_SLACK:g}")
    axP.plot(us, w_tight, color=AMBER, lw=3.0, label=f"$k$ = {K_TIGHT:g}")
    axP.set_xscale("log")
    axP.set_xlim(U_LO, U_HI)
    axP.set_ylim(-0.03, 1.03)
    axP.set_xlabel("$V_1/V_2$")
    axP.set_ylabel("fraction modified")
    axP.legend(loc="upper left")
    sweep = axP.axvline(us[0], color=MUTED, lw=1.4, ls=":")
    dotL, = axP.plot([us[0]], [w_slack[0]], "o", color=TEAL, ms=11, zorder=5)
    dotR, = axP.plot([us[0]], [w_tight[0]], "o", color=AMBER, ms=11, zorder=5)

    def update(i):
        for disc_u, disc_m, read, w in ((uL, mL, rL, w_slack[i]),
                                        (uR, mR, rR, w_tight[i])):
            disc_u.set_sizes([max(S_MAX * (1.0 - w), 1.0)])
            disc_m.set_sizes([max(S_MAX * w, 1.0)])
            read.set_text(f"{100 * w:.0f}% modified")
        sweep.set_xdata([us[i], us[i]])
        dotL.set_data([us[i]], [w_slack[i]])
        dotR.set_data([us[i]], [w_tight[i]])
        return uL, mL, uR, mR, sweep, dotL, dotR, rL, rR

    anim = FuncAnimation(fig, update, frames=N_FRAME, interval=1000 / FPS,
                         blit=False)
    out = f"{OUT}/s18_cycle_sweep.mp4"
    anim.save(out, writer=FFMpegWriter(fps=FPS, bitrate=2400,
                                       metadata={"title": "s18 cycle sweep"}))
    # Poster = the END state, per theme.movie()'s contract.
    update(N_FRAME - 1)
    fig.savefig(f"{OUT}/s18_cycle_sweep_poster.png", dpi=160,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  wrote {out} and its poster")


FIGURES = [fig_cycle_movie]

if __name__ == "__main__":
    fig_cycle_movie()
