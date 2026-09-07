"""Session 5 figures — response time, dilution, and the speed/level trade.

Two figures, each making a claim the session would otherwise assert:

  * a degradation tag speeds the response AND lowers the steady state, by the
    same factor, because both are set by (gamma + mu);
  * dilution is a floor: with gamma = 0 the response time IS the doubling time,
    and the best tag in Andersen 1998 buys a factor of 1.75, not a factor of ten.

Parameters are the ones PS2 uses: E. coli at 30 min doubling, and the four ssrA
variants of Andersen et al. 1998 Fig 3A.

    python tools/build_figures.py s05
"""
import numpy as np

from figures.style import use, AMBER, CYAN, INK, MUTED, RED, RULE, TEAL

plt = use()
OUT = "figures/build"

T_D = 30.0                      # doubling time, minutes
MU = np.log(2) / T_D            # 0.0231 /min
# Andersen et al. 1998, Fig 3A: degradation half-lives after medium downshift.
TAGS = [("no tag",  None,  INK),
        ("ASV",     110.0, MUTED),
        ("AAV",      60.0, TEAL),
        ("LAA/LVA",  40.0, CYAN)]


def _rates(t_half_deg):
    gamma = 0.0 if t_half_deg is None else np.log(2) / t_half_deg
    return gamma, gamma + MU, np.log(2) / (gamma + MU)


def fig_response_tags():
    """Approach to steady state for each tag, on one axis, unnormalised.

    Unnormalised on purpose: normalising each curve to its own steady state is
    the conventional plot and it hides the entire point, which is that the fast
    curves are also the low ones.
    """
    t = np.linspace(0, 90, 800)
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    alpha = 1.0                                  # same promoter throughout
    for name, th, c in TAGS:
        g, k, thalf = _rates(th)
        p = (alpha / k) * (1 - np.exp(-k * t))
        ax.plot(t, p, color=c, lw=3.0,
                label=f"{name}:  t½ = {thalf:.1f} min,  p* = {alpha/k:.1f}")
        ax.plot([thalf], [(alpha / k) / 2], "o", color=c, ms=8, zorder=5)
    ax.axvline(T_D, color=RULE, lw=1.4, ls="--")
    ax.text(T_D + 1.2, ax.get_ylim()[1] * 0.94,
            "doubling time — the floor\nwith no tag at all",
            fontsize=13, color=INK, va="top")
    ax.set_xlabel("time after induction  (min)")
    ax.set_ylabel("protein per cell  (same $\\alpha$ throughout)")
    ax.set_xlim(0, 90)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s05_response_tags.png")
    plt.close(fig)


def fig_speed_level():
    """The trade, as a curve you cannot get above.

    x is response time, y is steady-state level. Every tag is one point on a
    single hyperbola, because both coordinates are set by the same (gamma+mu).
    There is no knob that moves you up and left.
    """
    k = np.geomspace(MU, MU * 12, 400)
    fig, ax = plt.subplots(figsize=(9.2, 4.9))
    ax.plot(np.log(2) / k, 1.0 / k / (1.0 / MU), color=TEAL, lw=3.0,
            label="what one knob can reach")
    for name, th, c in TAGS:
        g, kk, thalf = _rates(th)
        ax.plot([thalf], [(1.0 / kk) / (1.0 / MU)], "o", color=c, ms=13,
                zorder=5)
        # stagger, or LAA/LVA collides with AAV
        off = {"LAA/LVA": (-14, -22), "AAV": (10, 6),
               "ASV": (10, 6), "no tag": (-18, 12)}[name]
        ax.annotate(name, (thalf, (1.0 / kk) / (1.0 / MU)),
                    textcoords="offset points", xytext=off,
                    fontsize=14, color=INK, fontweight="bold")
    ax.annotate("", xy=(5.5, 1.02), xytext=(15.5, 0.78),
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=2.6,
                                connectionstyle="arc3,rad=-0.18"))
    ax.text(4.0, 1.06, "where you want to be\n(fast AND high)",
            fontsize=13.5, color=AMBER, fontweight="bold", va="bottom")
    ax.set_xlabel("response time  t½  (min)")
    ax.set_ylabel("steady state, relative to untagged")
    ax.set_xlim(0, 34)
    ax.set_ylim(0, 1.18)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s05_speed_level.png")
    plt.close(fig)


FIGURES = [fig_response_tags, fig_speed_level]


def fig_repressilator_ring():
    """The repressilator as a ring, drawn rather than reproduced.

    The NETWORK is an idea and we draw it in our own notation; the DATA are
    Elowitz & Leibler's and go on the slide as a cited paper figure. Drawing it
    ourselves also lets us annotate the thing this session is about -- every
    repressor carries an ssrA tag -- which the paper's own figure does not
    emphasise, because it was not the paper's point.
    """
    import matplotlib.patches as mpatches
    from matplotlib.path import Path

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.set_aspect("equal"); ax.axis("off")
    R = 1.05
    names = [("TetR", 90.0), ("$\\lambda$cI", 330.0), ("LacI", 210.0)]
    pos = {n: np.array([R*np.cos(np.radians(a)), R*np.sin(np.radians(a))])
           for n, a in names}
    order = ["TetR", "$\\lambda$cI", "LacI"]      # TetR -| cI -| LacI -| TetR

    for i in range(3):
        a, b = pos[order[i]], pos[order[(i + 1) % 3]]
        d = b - a
        L = np.linalg.norm(d)
        u = d / L
        perp = np.array([-u[1], u[0]])
        # pull the chord outward into an arc, and stop short of both boxes
        start = a + u * 0.46 + perp * 0.10
        end = b - u * 0.46 + perp * 0.10
        ctrl = (a + b) / 2 + perp * 0.34
        path = Path([start, ctrl, end],
                    [Path.MOVETO, Path.CURVE3, Path.CURVE3])
        ax.add_patch(mpatches.PathPatch(path, facecolor="none",
                                        edgecolor=TEAL, lw=3.2, zorder=2))
        # blunt bar AT the target end, perpendicular to the arc's tangent there
        tan = end - ctrl
        tan = tan / np.linalg.norm(tan)
        nrm = np.array([-tan[1], tan[0]])
        p0, p1 = end - nrm * 0.13, end + nrm * 0.13
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=TEAL, lw=5.0,
                solid_capstyle="butt", zorder=3)

    for n in order:
        x, y = pos[n]
        ax.add_patch(mpatches.FancyBboxPatch((x - 0.34, y - 0.145), 0.68, 0.29,
                     boxstyle="round,pad=0.07", facecolor="#EEF3F1",
                     edgecolor=INK, lw=2.2, zorder=4))
        ax.text(x, y + 0.005, n, ha="center", va="center", fontsize=17,
                color=INK, fontweight="bold", zorder=5)
        ax.text(x, y - 0.33, "ssrA", ha="center", va="center", fontsize=13.5,
                color=AMBER, fontweight="bold", zorder=5)

    ax.text(0, 0.02, "each represses\nthe next", ha="center", va="center",
            fontsize=13.5, color=MUTED, style="italic", zorder=1)
    ax.set_xlim(-1.78, 1.78); ax.set_ylim(-0.98, 1.62)
    fig.tight_layout(pad=0.2)
    fig.savefig(f"{OUT}/s05_repressilator_ring.png")
    plt.close(fig)


FIGURES = [fig_response_tags, fig_speed_level, fig_repressilator_ring]
