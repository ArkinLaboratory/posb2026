"""Session 2 — the confinement movie.

Separate from s02_substrate.py because encoding takes tens of seconds and you do
not want it in the loop every time you rebuild a static figure:

    python tools/build_figures.py s02_movie

What it shows, and why it is worth thirty seconds of lecture. Two populations of
particles do *exactly the same random walk* -- the same generator, the same step
size, ordinary diffusion at every step. One is unconfined. The other has a cell
wall. On the right, their mean square displacements build up as you watch, and
the confined one visibly peels away from the 2Dt line and flattens.

The point is that nothing in the confined walk is anomalous. The apparent
subdiffusion is the wall. That is the argument of Valverde-Mendez et al., PNAS
122(4) e2406340121 (2025) -- their simulations resolve timescales the microscope
cannot reach and find the exponent goes back to normal there -- and it is worth
seeing happen rather than being told.

Output: figures/build/s02_confinement.mp4 and a poster frame beside it.
"""
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.patches import FancyBboxPatch

from figures.style import use, AMBER, INK, MUTED, RULE, TEAL

plt = use()
OUT = "figures/build"

D = 7.7                 # um^2/s, GFP in E. coli cytoplasm
DT = 2e-3               # s per frame-step
N_PART = 60
N_FRAME = 220
HALF_X, HALF_Y = 1.0, 0.4      # half-length and half-width of the cell, um
FPS = 25


def _walk(rng, confine):
    """One trajectory set. Same physics both times; only the wall differs."""
    step = np.sqrt(2 * D * DT)
    xy = np.zeros((N_FRAME, N_PART, 2))
    p = np.zeros((N_PART, 2))
    for i in range(N_FRAME):
        p = p + rng.normal(0, step, (N_PART, 2))
        if confine:
            p[:, 0] = np.clip(p[:, 0], -HALF_X, HALF_X)
            p[:, 1] = np.clip(p[:, 1], -HALF_Y, HALF_Y)
        xy[i] = p
    return xy


def fig_confinement_movie():
    """Two identical random walks, one with a wall. Watch the MSD peel away."""
    rng = np.random.default_rng(7)
    free = _walk(np.random.default_rng(7), confine=False)
    conf = _walk(np.random.default_rng(7), confine=True)

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.2, 4.0))

    # -- left: the cell, and the particles in and out of it -------------------
    ax.add_patch(FancyBboxPatch(
        (-HALF_X, -HALF_Y), 2 * HALF_X, 2 * HALF_Y,
        boxstyle="round,pad=0,rounding_size=0.38", facecolor="#F4F8F7",
        edgecolor=INK, linewidth=2.0, zorder=1))
    free_pts, = ax.plot([], [], "o", ms=4.5, color=TEAL, alpha=0.55, zorder=3)
    conf_pts, = ax.plot([], [], "o", ms=5.0, color=AMBER, zorder=4)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-2.3, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0, 2.0, "same walk, same seed — one of them has a wall",
            ha="center", fontsize=10.5, color=INK)
    ax.text(-4.1, -2.1, "unconfined — leaves", fontsize=10, color=TEAL, weight="bold")
    ax.text(4.1, -2.1, "confined — cannot", fontsize=10, color=AMBER,
            weight="bold", ha="right")

    # -- right: the MSD, built up as it happens -------------------------------
    t = np.arange(1, N_FRAME) * DT
    bx.loglog(t, 4 * D * t, lw=1.3, ls=":", color=MUTED, label=r"$4Dt$")
    free_line, = bx.loglog([], [], lw=2.6, color=TEAL, label="unconfined")
    conf_line, = bx.loglog([], [], lw=2.6, color=AMBER, label="confined")
    bx.set_xlim(DT, N_FRAME * DT)
    bx.set_ylim(1e-3, 3.0)
    bx.set_xlabel("lag time (s)")
    bx.set_ylabel("mean square displacement (µm²)")
    bx.set_title("Ordinary diffusion at every step")
    bx.legend(fontsize=9, loc="lower right")
    bx.grid(True, which="both", lw=0.5, alpha=0.3)
    note = bx.text(0.035, 0.045, "", transform=bx.transAxes, fontsize=10,
                   color=AMBER, va="bottom", weight="bold")

    def msd(tr, upto):
        """MSD from displacement since t=0, over the frames seen so far."""
        return np.mean(np.sum(tr[1:upto] ** 2, axis=2), axis=1)

    def update(i):
        j = max(i, 2)
        free_pts.set_data(free[i, :, 0], free[i, :, 1])
        conf_pts.set_data(conf[i, :, 0], conf[i, :, 1])
        free_line.set_data(t[:j - 1], msd(free, j))
        conf_line.set_data(t[:j - 1], msd(conf, j))
        if t[j - 2] > 0.06:
            note.set_text("the confined walk has left the line\n"
                          "— and nothing about it changed")
        return free_pts, conf_pts, free_line, conf_line, note

    fig.tight_layout()
    anim = FuncAnimation(fig, update, frames=N_FRAME, interval=1000 / FPS,
                         blit=False)
    anim.save(f"{OUT}/s02_confinement.mp4",
              writer=FFMpegWriter(fps=FPS, bitrate=2400,
                                  extra_args=["-pix_fmt", "yuv420p"]))
    update(N_FRAME - 1)                       # poster frame = the end state
    fig.savefig(f"{OUT}/s02_confinement_poster.png")
    plt.close(fig)


FIGURES = [fig_confinement_movie]
