"""Session 14 — the basin movie.

Separate from `s14_review.py` for the same reason `s02_movie.py` is separate
from `s02_substrate.py`: encoding takes seconds rather than milliseconds, and
a figure module that is rebuilt on every deck build should not pay that.

WHAT IT SHOWS. Four pulses in X, all starting on the x-axis because a pulse
raises X alone, run forward together on the mutual-activation plane. Two fall
back to both-off and two climb to both-on, and the two nearest the divide are
0.04 apart. Adam, 11 October 2026: "it might be good to have simulations of
different cases to demonstrate."

THE POSTER FRAME is `s14_basin_trajectories.png` -- the static panel that
carries the same four runs finished. `theme.movie()` shows the poster until
the clip is played, so a slide that is never clicked still makes the whole
argument, which is the failure mode the theme's own docstring warns about.

Run:  python3 -m figures.s14_movie
"""
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from scipy.integrate import solve_ivp

from figures.style import use, TEAL, AMBER, MUTED, INK, RED, RULE
from figures.s14_review import MA_A, MA_N, _ma_model, _basin_cases

plt = use(legacy=True)   # see figures.style.LEGACY_SCALE
OUT = "figures/build"

FPS = 24
T_END = 12.0
N_FRAME = 240


def fig_basin_movie():
    """Four pulses on the mutual-activation plane, as motion."""
    rhs, saddle_x, on_x, sep, xcross = _ma_model()
    a, n = MA_A, MA_N
    top = on_x * 1.28
    cases = _basin_cases()

    t = np.linspace(0, T_END, N_FRAME)
    runs = [solve_ivp(rhs, [0, T_END], [x0, 0.0], t_eval=t,
                      rtol=1e-10, atol=1e-13).y for x0, _ in cases]

    fig, ax = plt.subplots(figsize=(6.6, 5.8))
    uu = np.linspace(0.0, top, 700)
    nx = a * uu ** n / (1 + uu ** n)
    ax.plot(nx, uu, color=TEAL, lw=2.0, alpha=0.40)
    ax.plot(uu, nx, color=AMBER, lw=2.0, ls="--", alpha=0.40)
    for xp, yp in sep:
        keep = (xp >= 0) & (yp >= 0) & (xp <= top) & (yp <= top)
        ax.plot(xp[keep], yp[keep], color=RED, lw=3.0, zorder=9)
    for (px, py), kind in [((0.0, 0.0), "stable"),
                           ((saddle_x, saddle_x), "saddle"),
                           ((on_x, on_x), "stable")]:
        ax.plot(px, py, "o", ms=12, zorder=10, clip_on=False,
                mfc="white" if kind == "saddle" else INK,
                mec=RED if kind == "saddle" else INK, mew=2.6)
    ax.text(xcross + 0.08, 0.07, f"the divide meets the axis at {xcross:.3f}",
            color=RED, fontsize=11.5)
    ax.set_xlim(0, top); ax.set_ylim(0, top)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$   (protein X)")
    ax.set_ylabel("$y$", rotation=0, labelpad=12)
    ax.set_title("Four pulses in X, run forward together", fontsize=14.5,
                 color=INK)

    cols = [AMBER, AMBER, TEAL, TEAL]
    styles = ["-", "--", "--", "-"]
    paths, heads = [], []
    for (x0, lab), col, ls in zip(cases, cols, styles):
        paths.append(ax.plot([], [], color=col, lw=2.6, ls=ls, zorder=6)[0])
        heads.append(ax.plot([], [], "o", ms=9, color=col, zorder=8)[0])
        ax.plot([x0], [0.0], "o", ms=7, mfc="white", mec=col, mew=2.0,
                zorder=7, clip_on=False)
    # Top-left: the bottom-right corner is where the divide's caption and the
    # 1.20 pulse both live, and a running clock written over them is unreadable.
    clock = ax.text(0.97, 0.95, "", transform=ax.transAxes, ha="right",
                    fontsize=12.5, color=MUTED)

    def update(i):
        j = i + 1
        for p, h, y in zip(paths, heads, runs):
            p.set_data(y[0, :j], y[1, :j])
            h.set_data([y[0, j - 1]], [y[1, j - 1]])
        clock.set_text(f"t = {t[i]:4.1f} lifetimes")
        return (*paths, *heads, clock)

    fig.tight_layout()
    anim = FuncAnimation(fig, update, frames=N_FRAME, interval=1000 / FPS,
                         blit=False)
    out = f"{OUT}/s14_basin_runs.mp4"
    anim.save(out, writer=FFMpegWriter(fps=FPS, bitrate=2400,
                                       extra_args=["-pix_fmt", "yuv420p"]))
    plt.close(fig)

    # The movie and the static panel must agree about which pulses switch, or
    # the poster frame contradicts the clip it stands in for.
    ends = [y[0, -1] for y in runs]
    assert ends[0] < saddle_x and ends[1] < saddle_x, ends
    assert ends[2] > saddle_x and ends[3] > saddle_x, ends
    return out


FIGURES = [fig_basin_movie]


if __name__ == "__main__":
    for fn in FIGURES:
        print(" ", fn())
