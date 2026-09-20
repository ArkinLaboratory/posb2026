"""Session 8 figures — the phase plane, drawn one step at a time.

WHY THESE EXIST (18 September 2026). The session-8 deck had twenty-five
surfaces of symbols about a plane that was never drawn, in a room where 5 of
21 had ever seen a phase portrait. Adam was the graphics engine, live, at the
board. These are the drawings, generated from the same `posb` functions the
notebook uses, so the picture on the slide is the picture a student can
reproduce.

Most of them come in numbered states (`_p1`, `_p2`, ...): one drawing, advanced
one element per derivation step, for `Deck.derivation_fig()`. Panels are sized
for the 5.4in left column of that surface; the two that stand alone
(`crossings`, `tau_delta`) are wider.

The running example is the symmetric toggle at n = 2, a = 3 — NOT a = 2, which
is a_c exactly and gives one crossing. The design-space figure is the
asymmetric toggle of Gardner, Cantor & Collins 2000, Fig. 2c,d, recomputed.

Run:  python tools/build_figures.py s08
"""
import numpy as np

from figures.style import use, TEAL, AMBER, MUTED, INK, RED, GREEN, RULE, CYAN
from posb import (toggle_model, stability_report, nullcline,
                  toggle_alpha_critical)

plt = use()
OUT = "figures/build"
PANEL = (5.4, 4.9)          # the left column of a split derivation surface
N, A = 2, 3.0               # the running example
LIM = 3.4

U_COL, V_COL = TEAL, AMBER  # du/dt = 0 and dv/dt = 0, everywhere in the session


def _model(a=A, n=N):
    return toggle_model(a, a, n=n)


def _axes(fig_size=PANEL, lim=LIM):
    fig, ax = plt.subplots(figsize=fig_size)
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.set_xlabel("$u$"); ax.set_ylabel("$v$", rotation=0, labelpad=12)
    ax.set_aspect("equal")
    return fig, ax


def _nullclines(ax, m, lim=LIM, which=("u", "v"), lw=2.8):
    grid = np.linspace(0.001, lim, 400)
    if "u" in which:
        ax.plot(nullcline(m, "u", "v", grid), grid, lw=lw, color=U_COL)
    if "v" in which:
        ax.plot(grid, nullcline(m, "v", "u", grid), lw=lw, color=V_COL)


def _fixed_points(ax, m, ms=11, saddle=True, label=False):
    pts = stability_report(m, grid=(1e-3, 20, 9))
    for f in pts:
        p, kind = f["point"], f["type"]
        if kind.startswith("stable"):
            ax.plot(p["u"], p["v"], "o", ms=ms, color=INK, zorder=6)
        elif saddle:
            ax.plot(p["u"], p["v"], "o", ms=ms, mfc="white", mec=RED,
                    mew=2.4, zorder=6)
    return pts


def _flow(ax, m, lim=LIM, density=0.9):
    U, V = np.meshgrid(np.linspace(0.05, lim, 24), np.linspace(0.05, lim, 24))
    dU, dV = np.zeros_like(U), np.zeros_like(V)
    for i in range(U.shape[0]):
        for j in range(U.shape[1]):
            dU[i, j], dV[i, j] = m.rhs(0.0, [U[i, j], V[i, j]])
    ax.streamplot(U, V, dU, dV, color=MUTED, linewidth=0.8, density=density,
                  arrowsize=1.0)


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Run 1: where can the system sit still?  Five states of one drawing.
# ---------------------------------------------------------------------------

def fig_plane():
    """The phase plane built up: axes, u-nullcline, v-nullcline, crossings, flow."""
    m = _model()

    # p1 — a state is a point; it moves. Sitting still = no arrow.
    fig, ax = _axes()
    p = (2.4, 2.2)
    d = m.rhs(0.0, list(p))
    ax.plot(*p, "o", ms=10, color=INK)
    ax.annotate("", xy=(p[0] + d[0] * 0.5, p[1] + d[1] * 0.5), xytext=p,
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=INK,
                                mutation_scale=18))
    ax.text(p[0] + 0.12, p[1] + 0.18, "$(u, v)$", color=INK)
    ax.text(0.15, 3.05, "a state is a point;\n$(du/dt,\\,dv/dt)$ is its arrow",
            color=MUTED, fontsize=14)
    ax.set_title("Sitting still means: no arrow")
    _save(fig, "s08_plane_p1")

    # p2 — the u-nullcline, with a point on it and a VERTICAL arrow
    fig, ax = _axes()
    _nullclines(ax, m, which=("u",))
    v0 = 2.4
    u0 = A / (1 + v0 ** N)
    d = m.rhs(0.0, [u0, v0]); d = 0.55 * d / np.linalg.norm(d)
    ax.plot(u0, v0, "o", ms=10, color=INK)
    ax.annotate("", xy=(u0 + d[0], v0 + d[1]), xytext=(u0, v0),
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=INK,
                                mutation_scale=18))
    ax.text(1.35, 2.85, "$du/dt = 0$", color=U_COL, fontsize=16,
            fontweight="bold")
    ax.text(u0 + 0.22, v0 - 0.15, "on it, $u$ is still\nand $v$ is moving",
            color=MUTED, fontsize=14)
    ax.set_title("$u = a/(1+v^n)$: a curve, not a point")
    _save(fig, "s08_plane_p2")

    # p3 — the v-nullcline, HORIZONTAL arrow
    fig, ax = _axes()
    _nullclines(ax, m)
    u1 = 2.4
    v1 = A / (1 + u1 ** N)
    d = m.rhs(0.0, [u1, v1]); d = 0.55 * d / np.linalg.norm(d)
    ax.plot(u1, v1, "o", ms=10, color=INK)
    ax.annotate("", xy=(u1 + d[0], v1 + d[1]), xytext=(u1, v1),
                arrowprops=dict(arrowstyle="-|>", lw=2.6, color=INK,
                                mutation_scale=18))
    ax.text(1.35, 2.85, "$du/dt = 0$", color=U_COL, fontsize=16,
            fontweight="bold")
    ax.text(2.2, 0.95, "$dv/dt = 0$", color=V_COL, fontsize=16,
            fontweight="bold")
    ax.text(0.85, 0.08, "on it, $v$ is still\nand $u$ is moving", color=MUTED,
            fontsize=14)
    ax.set_title("$v = a/(1+u^n)$: the other curve")
    _save(fig, "s08_plane_p3")

    # p4 — the crossings, circled
    fig, ax = _axes()
    _nullclines(ax, m)
    pts = stability_report(m, grid=(1e-3, 20, 9))
    for f in pts:
        p = f["point"]
        ax.plot(p["u"], p["v"], "o", ms=22, mfc="none", mec=RED, mew=2.4,
                zorder=6)
        ax.plot(p["u"], p["v"], "o", ms=7, color=INK, zorder=7)
    ax.text(1.35, 2.85, "$du/dt = 0$", color=U_COL, fontsize=16,
            fontweight="bold")
    ax.text(2.2, 0.95, "$dv/dt = 0$", color=V_COL, fontsize=16,
            fontweight="bold")
    ax.set_title(f"{len(pts)} crossings = {len(pts)} fixed points")
    _save(fig, "s08_plane_p4")

    # p5 — the flow everywhere else
    fig, ax = _axes()
    _flow(ax, m)
    _nullclines(ax, m)
    _fixed_points(ax, m)
    ax.set_title("Off the curves, the state moves")
    _save(fig, "s08_plane_p5")


# ---------------------------------------------------------------------------
# Rhythm 1 resolution: n = 1 versus n = 4
# ---------------------------------------------------------------------------

def fig_crossings():
    """Both nullclines decrease at any n; only a steep one crosses three times."""
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.9))
    for ax, n in zip(axes, (1, 4)):
        m = _model(n=n)
        ax.set_xlim(0, LIM); ax.set_ylim(0, LIM); ax.set_aspect("equal")
        ax.set_xlabel("$u$"); ax.set_ylabel("$v$", rotation=0, labelpad=12)
        _nullclines(ax, m)
        pts = _fixed_points(ax, m)
        ax.set_title(f"$n = {n}$, $a = {A:g}$: crosses "
                     f"{'once' if len(pts) == 1 else 'three times'}")
    axes[0].text(1.3, 2.85, "$du/dt = 0$", color=U_COL, fontsize=15,
                 fontweight="bold")
    axes[0].text(2.1, 1.1, "$dv/dt = 0$", color=V_COL, fontsize=15,
                 fontweight="bold")
    _save(fig, "s08_crossings")


# ---------------------------------------------------------------------------
# Run 2: the diagonal
# ---------------------------------------------------------------------------

def fig_diagonal():
    """Symmetry u <-> v: one crossing is always on the diagonal; the others pair."""
    m = _model()
    fig, ax = _axes()
    _nullclines(ax, m)
    ax.plot([0, LIM], [0, LIM], ls="--", lw=1.6, color=MUTED)
    pts = stability_report(m, grid=(1e-3, 20, 9))
    for f in pts:
        p = f["point"]
        on = abs(p["u"] - p["v"]) < 1e-6
        ax.plot(p["u"], p["v"], "o", ms=11, color=RED if on else INK, zorder=6)
        if on:
            ax.annotate("$u = v = x$\n$x + x^{n+1} = a$", xy=(p["u"], p["v"]),
                        xytext=(1.75, 2.35), color=RED, fontsize=15,
                        arrowprops=dict(arrowstyle="-", color=RED, lw=1.2))
    ax.text(0.15, 3.0, "the pair, mirrored", color=INK, fontsize=14)
    ax.text(2.35, 3.15, "$u = v$", color=MUTED, fontsize=14)
    ax.set_title("One crossing is on the diagonal")
    _save(fig, "s08_diagonal")


# ---------------------------------------------------------------------------
# Run 3: nudge it.  Three states of one drawing, zoomed on the saddle.
# ---------------------------------------------------------------------------

def _symmetric_point(a=A, n=N):
    from scipy.optimize import brentq
    return brentq(lambda x: x + x ** (n + 1) - a, 1e-6, a)


def fig_perturb():
    """Perturb the symmetric point: the nudge, its two components, which one wins."""
    m = _model()
    x = _symmetric_point()
    g = N * x ** (N + 1) / A
    win = 0.75
    eps = np.array([0.40, 0.14])
    e_sym = eps.sum() / 2 * np.array([1, 1])        # component along (1,1)
    e_anti = (eps[0] - eps[1]) / 2 * np.array([1, -1])  # along (1,-1)

    def base(title, faint=False):
        fig, ax = plt.subplots(figsize=PANEL)
        ax.set_xlim(x - win, x + win); ax.set_ylim(x - win, x + win)
        ax.set_aspect("equal")
        ax.set_xlabel("$u$"); ax.set_ylabel("$v$", rotation=0, labelpad=12)
        _nullclines(ax, m, lim=LIM, lw=2.0)
        if faint:                      # the linear world: curves fade back
            for ln in ax.lines:
                ln.set_alpha(0.25)
        ax.plot(x, x, "o", ms=11, mfc="white", mec=RED, mew=2.4, zorder=6)
        ax.set_title(title)
        return fig, ax

    def arrow(ax, frm, to, color, lw=2.6):
        ax.annotate("", xy=to, xytext=frm,
                    arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                    mutation_scale=18))

    # p1 — the nudge
    fig, ax = base("Nudge the fixed point by $\\varepsilon$")
    arrow(ax, (x, x), (x + eps[0], x + eps[1]), INK)
    ax.text(x + eps[0] + 0.05, x + eps[1] + 0.02, "$(u^*+\\varepsilon_1,\\ v^*+\\varepsilon_2)$",
            color=INK, fontsize=14)
    ax.text(x - 0.68, x + 0.55, "$u^* = v^* = x$", color=RED, fontsize=15)
    _save(fig, "s08_perturb_p1")

    # p2 — decompose along (1,1) and (1,-1)
    fig, ax = base("Two directions the matrix cannot mix", faint=True)
    ax.plot([x - win, x + win], [x - win, x + win], ls="--", lw=1.4,
            color=GREEN)
    ax.plot([x - win, x + win], [x + win, x - win], ls="--", lw=1.4, color=RED)
    arrow(ax, (x, x), (x + eps[0], x + eps[1]), MUTED, lw=2.0)
    arrow(ax, (x, x), (x + e_sym[0], x + e_sym[1]), GREEN)
    arrow(ax, (x + e_sym[0], x + e_sym[1]), (x + eps[0], x + eps[1]), RED)
    ax.text(x + 0.02, x + 0.58, "symmetric (1, 1)\n$\\lambda = -1-g$",
            color=GREEN, fontsize=14)
    ax.text(x + 0.05, x - 0.62, "antisymmetric (1, $-$1)\n$\\lambda = -1+g$",
            color=RED, fontsize=14)
    ax.text(x + eps[0] + 0.04, x + eps[1] + 0.04, "$\\varepsilon$", color=MUTED,
            fontsize=15)
    _save(fig, "s08_perturb_p2")

    # p3 — the symmetric part dies, the antisymmetric part grows
    fig, ax = base(f"$g = {g:.2f} > 1$: the antisymmetric one wins",
                   faint=True)
    ax.plot([x - win, x + win], [x - win, x + win], ls="--", lw=1.4,
            color=GREEN)
    ax.plot([x - win, x + win], [x + win, x - win], ls="--", lw=1.4, color=RED)
    arrow(ax, (x + 0.42, x + 0.42), (x + 0.12, x + 0.12), GREEN)
    arrow(ax, (x - 0.42, x - 0.42), (x - 0.12, x - 0.12), GREEN)
    arrow(ax, (x + 0.12, x - 0.12), (x + 0.48, x - 0.48), RED)
    arrow(ax, (x - 0.12, x + 0.12), (x - 0.48, x + 0.48), RED)
    tr = m.simulate({"u": x + eps[0], "v": x + eps[1]}, (0, 6), n_points=600)
    ax.plot(tr["u"], tr["v"], lw=2.4, color=INK)
    ax.plot(x + eps[0], x + eps[1], "o", ms=7, color=INK)
    ax.text(x + 0.02, x + 0.62, "comes back", color=GREEN, fontsize=14)
    ax.text(x + 0.05, x - 0.68, "leaves: the two\ngenes diverge", color=RED,
            fontsize=14)
    _save(fig, "s08_perturb_p3")


# ---------------------------------------------------------------------------
# Run 4: the birth of the switch, and a_c(n)
# ---------------------------------------------------------------------------

def fig_tangent():
    """Below, at and above a_c for n = 2: the crossings appear where the curves touch."""
    fig, ax = _axes(lim=3.0)
    for a, col, lab in ((1.5, MUTED, "$a = 1.5$"), (2.0, RED, "$a = a_c = 2$"),
                        (3.0, INK, "$a = 3$")):
        m = _model(a=a)
        grid = np.linspace(0.001, 3.0, 400)
        ax.plot(nullcline(m, "u", "v", grid), grid, lw=2.4, color=col)
        ax.plot(grid, nullcline(m, "v", "u", grid), lw=2.4, color=col,
                ls="--")
        ax.plot([], [], color=col, lw=2.4, label=lab)
    ax.plot([0, 3], [0, 3], ls=":", lw=1.2, color=MUTED)
    ax.plot(1, 1, "o", ms=11, mfc="white", mec=RED, mew=2.4, zorder=6)
    ax.text(1.1, 1.12, "$x_c = 1$", color=RED, fontsize=15)
    ax.legend(loc="upper right", fontsize=14)
    ax.set_title("$n = 2$: the curves touch at $a_c$")
    _save(fig, "s08_tangent")


def fig_ac_curve():
    """a_c(n): the boundary of bistability, and its n -> 1 wall."""
    ns = np.linspace(1.03, 4.5, 400)
    ac = np.array([toggle_alpha_critical(n) for n in ns])

    def base():
        fig, ax = plt.subplots(figsize=PANEL)
        ax.fill_between(ns, ac, 60, color=TEAL, alpha=0.10)
        ax.plot(ns, ac, lw=2.8, color=TEAL)
        ax.set_yscale("log")
        ax.set_xlim(0.8, 4.5); ax.set_ylim(0.5, 60)
        ax.set_xlabel("cooperativity $n$")
        ax.set_ylabel("$a$")
        ax.text(2.4, 8, "switch", color=TEAL, fontsize=16, fontweight="bold")
        ax.text(2.6, 0.7, "one state", color=MUTED, fontsize=16)
        return fig, ax

    # p1 — the curve, with n = 2 read off it
    fig, ax = base()
    ax.plot(2, 2, "o", ms=10, color=INK)
    ax.text(2.15, 1.3, "$n = 2,\\ a_c = 2$", color=INK, fontsize=14)
    ax.set_title("$a_c = n\\,(n-1)^{-(n+1)/n}$")
    _save(fig, "s08_ac_curve_p1")

    # p2 — the wall at n = 1, and the two Rhythm-2 points
    fig, ax = base()
    ax.axvline(1.0, color=RED, lw=1.8, ls="--")
    ax.fill_betweenx([0.5, 60], 0.8, 1.0, color=RED, alpha=0.08)
    ax.text(1.05, 30, "$a_c \\to \\infty$\nas $n \\to 1$", color=RED,
            fontsize=14)
    ax.plot(1.8, 5, "o", ms=10, color=INK)
    ax.text(1.9, 5.6, "$n = 1.8,\\ a = 5$", color=INK, fontsize=14)
    ax.set_title("No cooperativity, no switch")
    _save(fig, "s08_ac_curve_p2")


# ---------------------------------------------------------------------------
# The trace-determinant plane, with the toggle's own track on it
# ---------------------------------------------------------------------------

def fig_tau_delta():
    """Every 2x2 fixed point from two numbers; the two exits from stability."""
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    tau = np.linspace(-3.2, 3.2, 400)
    ax.fill_between(tau, -2.2, 0, color=RED, alpha=0.10)
    ax.fill_between(tau[tau < 0], 0, 3.2, color=TEAL, alpha=0.12)
    ax.fill_between(tau[tau > 0], 0, 3.2, color=AMBER, alpha=0.12)
    ax.plot(tau, tau ** 2 / 4, color=MUTED, lw=1.6, ls="--")
    ax.axhline(0, color=INK, lw=1.4); ax.axvline(0, color=INK, lw=1.4)
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-2.2, 3.2)
    ax.set_xlabel("$\\tau = $ trace $J$"); ax.set_ylabel("$\\Delta = \\det J$")
    ax.text(-0.9, -1.4, "saddle\n$\\Delta<0$", color=RED, fontsize=16,
            fontweight="bold", ha="center")
    ax.text(-1.45, 0.25, "stable node", color=TEAL, fontsize=15)
    ax.text(-1.5, 2.55, "stable spiral", color=TEAL, fontsize=15)
    ax.text(1.55, 0.35, "unstable node", color=AMBER, fontsize=15)
    ax.text(0.55, 2.55, "unstable spiral", color=AMBER, fontsize=15)
    ax.text(2.0, 1.6, "$\\tau^2 = 4\\Delta$", color=MUTED, fontsize=14)
    # the toggle: tau = -2 always, Delta = 1 - beta^2
    ax.annotate("", xy=(-2, -1.4), xytext=(-2, 1.0),
                arrowprops=dict(arrowstyle="-|>", lw=3, color=INK,
                                mutation_scale=20))
    ax.plot(-2, 1.0, "o", ms=9, color=INK)
    ax.text(-3.1, 1.15, "the toggle: $\\tau=-2$,\n$\\Delta = 1-g^2$",
            color=INK, fontsize=14)
    ax.text(-1.9, -0.55, "$g$ rising past 1:\nthe switch (today)",
            color=INK, fontsize=14)
    # the other exit: tau through 0 at Delta > 0
    ax.annotate("", xy=(0.9, 1.6), xytext=(-0.7, 1.6),
                arrowprops=dict(arrowstyle="-|>", lw=3, color=GREEN,
                                mutation_scale=20))
    ax.text(-0.75, 1.75, "$\\tau$ through 0: the oscillator (session 11)",
            color=GREEN, fontsize=14)
    ax.set_title("Two ways out of the stable region")
    _save(fig, "s08_tau_delta")


# ---------------------------------------------------------------------------
# Gardner Fig. 2c,d recomputed: the asymmetric toggle's bistable region
# ---------------------------------------------------------------------------

def n_fixed_points(a1, a2, beta, gamma, u=None):
    """Count fixed points of du/dt = a1/(1+v^beta) - u, dv/dt = a2/(1+u^gamma) - v
    for arrays of a1 (rows) and a2 (cols), by counting sign changes of
    u - a1/(1 + (a2/(1+u^gamma))^beta) on a log grid in u.

    Vectorised rather than routed through posb.fixed_points (one fsolve per
    guess). Used to CHECK the analytic boundary below, not to draw it.
    """
    if u is None:
        u = np.geomspace(1e-4, 3e3, 3000)
    A1 = np.asarray(a1, float)[:, None, None]
    A2 = np.asarray(a2, float)[None, :, None]
    U = u[None, None, :]
    V = A2 / (1 + U ** gamma)
    g = U - A1 / (1 + V ** beta)
    return np.count_nonzero(np.diff(np.sign(g), axis=2) != 0, axis=2)


def bifurcation_line(beta, gamma, n=600):
    """The saddle-node boundary of the asymmetric toggle, parametrically.

    Bistability is lost where the two nullclines become tangent. On the
    u-nullcline alpha_1 = u(1+v^beta); on the v-nullcline alpha_2 = v(1+u^gamma);
    tangency means the product of their slopes is one, which reduces to

        beta * gamma * u^gamma * v^beta = (1 + u^gamma)(1 + v^beta).

    Solve that for v^beta at each u and push through to (alpha_1, alpha_2).
    This is the bifurcation line of Gardner, Cantor & Collins 2000, Box 1,
    which the paper states without the derivation. Returns (alpha_1, alpha_2).
    """
    k = beta * gamma - 1
    if k <= 0:
        raise ValueError("no bistability unless beta*gamma > 1")
    u_min = k ** (-1 / gamma)
    u = u_min * np.geomspace(1.0005, 3e3, n)
    vb = (1 + u ** gamma) / (u ** gamma * k - 1)
    v = vb ** (1 / beta)
    return u * (1 + vb), v * (1 + u ** gamma)


def fig_design_space():
    """Gardner 2000 Fig. 2c,d, recomputed: bistable region in (alpha_2, alpha_1).

    Axes follow the paper -- log(alpha_2) across, log(alpha_1) up -- so this
    can sit beside the original on one surface without a mental transpose.
    """
    fig, ax = plt.subplots(figsize=PANEL)
    # Labels sit on the lines rather than in a legend: every corner of this
    # plot has a curve through it.
    for (b, g), col, lab, at in (
            ((1.1, 1.1), MUTED, "$\\beta=\\gamma=1.1$", (2.6, 2.62)),
            ((2, 2), MUTED, "$\\beta=\\gamma=2$", (2.55, 1.9)),
            ((3, 3), INK, "$\\beta=\\gamma=3$", (2.55, 0.95)),
            ((2.5, 1.0), RED, "$\\beta=2.5,\\ \\gamma=1$", (1.5, 2.8))):
        a1, a2 = bifurcation_line(b, g)
        ax.plot(np.log10(a2), np.log10(a1), color=col, lw=2.4,
                alpha=0.55 if b == 1.1 else 1.0)
        ax.text(*at, lab, color=col, fontsize=14)
    ax.plot(np.log10(15.6), np.log10(156.25), "o", ms=10, color=RED, zorder=6)
    ax.text(np.log10(15.6) + 0.12, np.log10(156.25) - 0.22, "pTAK117",
            color=RED, fontsize=14)
    ax.text(0.15, 2.85, "one state", color=MUTED, fontsize=15)
    ax.text(2.35, 0.15, "one state", color=MUTED, fontsize=15)
    ax.set_xlabel("$\\log_{10}\\alpha_2$"); ax.set_ylabel("$\\log_{10}\\alpha_1$")
    ax.set_xlim(0, 3.2); ax.set_ylim(0, 3.2); ax.set_aspect("equal")
    ax.set_title("Where the switch lives (Gardner Fig. 2c,d)")
    _save(fig, "s08_design_space")


def fig_gardner_nullclines():
    """pTAK117's own nullclines (one arm has no cooperativity) beside the same device with none."""
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.9))
    grid = np.geomspace(0.02, 400, 600)
    for ax, (b, g), title in zip(
            axes, ((2.5, 1.0), (1.0, 1.0)),
            ("pTAK117: $\\beta = 2.5$, $\\gamma = 1$",
             "the same $\\alpha$'s with $\\beta = \\gamma = 1$")):
        m = toggle_model(156.25, 15.6, n=g, m=b)
        ax.plot(nullcline(m, "u", "v", grid, bracket=(1e-6, 1e4)), grid,
                lw=2.8, color=U_COL)
        ax.plot(grid, nullcline(m, "v", "u", grid, bracket=(1e-6, 1e4)),
                lw=2.8, color=V_COL)
        for f in stability_report(m, grid=(1e-3, 300, 9)):
            p, kind = f["point"], f["type"]
            if kind.startswith("stable"):
                ax.plot(p["u"], p["v"], "o", ms=11, color=INK, zorder=6)
            else:
                ax.plot(p["u"], p["v"], "o", ms=11, mfc="white", mec=RED,
                        mew=2.4, zorder=6)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(0.02, 400); ax.set_ylim(0.02, 400)
        ax.set_xlabel("$u$  (LacI, in units of its threshold)")
        ax.set_ylabel("$v$  (cI, likewise)")
        ax.set_title(title)
    axes[0].text(0.03, 0.04, "$du/dt = 0$", color=U_COL, fontsize=15,
                 fontweight="bold")
    axes[0].text(20, 30, "$dv/dt = 0$", color=V_COL, fontsize=15,
                 fontweight="bold")
    _save(fig, "s08_gardner_nullclines")


FIGURES = [fig_gardner_nullclines, fig_plane, fig_crossings, fig_diagonal, fig_perturb, fig_tangent,
           fig_ac_curve, fig_tau_delta, fig_design_space]
