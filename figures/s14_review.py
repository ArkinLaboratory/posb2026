"""Session 14 figures — the review session.

Every panel here exists to carry a step of a derivation that session 14 works
through, and no panel uses a circuit the midterm asks about. That is enforced
by `_assert_not_exam_circuit` below rather than asserted in prose, because an
earlier version of this docstring claimed the separation while three of the
panels broke it.

The two that matter:

  * the basin panel is mutual ACTIVATION, not a toggle. An asymmetric toggle
    differs from the exam's symmetric one in its parameters only, which is not
    a different circuit; mutual activation has different states (both off,
    both on) and carries the lesson better, because its dividing line crosses
    the x-axis far outside the saddle's x-coordinate.
  * the ring panels are mixed-sign loops. Pure repression rings of three, four
    and five are all on the paper, the ring of five included.

Run:  python tools/build_figures.py s14
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN, RULE

plt = use(legacy=True)   # see figures.style.LEGACY_SCALE
OUT = "figures/build"

# Mutual activation, for the basin panel. Two stable states (both off, both on)
# and a saddle on the diagonal.
MA_A, MA_N = 3.0, 2.0

# One gene activating itself, for the handout's written basin item. Bistable in
# ONE dimension, so its divide is a number rather than a curve.
AA_B, AA_A, AA_N = 0.2, 2.0, 3.0


def _save(fig, name, tight=True):
    if tight:
        fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)
    return f"{OUT}/{name}.png"


# ---------------------------------------------------------------------------
# 1. The round trip — one flip at a time, on a MIXED loop the exam does not use
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# The leak guard
# ---------------------------------------------------------------------------
#
# Added after a cold reviewer found that three of the session's circuits were
# the exam's, while two docstrings in this file claimed none of them were. A
# claim in a comment is not a check. This is.
#
# The exam's circuits, as edge sets (node names normalised to positions):
#   pure repression ring of three   X-|Y-|Z-|X
#   pure repression ring of four
#   symmetric two-gene mutual repression (its B1 phase plane, and B1.4's signs)
def _pure_ring(k):
    nm = [chr(ord("A") + i) for i in range(k)]
    return frozenset((nm[i], nm[(i + 1) % k], True) for i in range(k))


# Rings of three, four and FIVE are all on the paper: B3.1 and B3.2 compare
# three against four, and B3.5 is the ring of five by name. The handout once
# set a ring of five as its "now you" item and its answer sheet published
# B3.5's reasoning; that is what this list is for.
EXAM_EDGE_SETS = [
    _pure_ring(3),
    _pure_ring(4),
    _pure_ring(5),
    frozenset({("A", "B", True), ("B", "A", True)}),
]


def _assert_not_exam_circuit(edges, where):
    """Refuse to draw a circuit the midterm asks about.

    `edges` is a list of (from, to, is_repression). Node NAMES are ignored --
    renaming X to P is exactly the evasion this is meant to catch -- so the
    edges are relabelled by first appearance before comparing.
    """
    order, norm = {}, []
    for a, b, rep in edges:
        for nm in (a, b):
            if nm not in order:
                order[nm] = chr(ord("A") + len(order))
        norm.append((order[a], order[b], bool(rep)))
    if frozenset(norm) in EXAM_EDGE_SETS:
        raise AssertionError(
            f"{where}: this is an exam circuit. Teaching the skill on the "
            f"question is rehearsal, not teaching. Change the wiring, not the "
            f"node names.")


NODE_R = 0.17          # node circle radius, shared by every loop panel


def _draw_edges(ax, nodes, edges, curve=0.0, where="figure"):
    """Arms between nodes, with a blunt head on every repression.

    The head is placed with the "|-|" arrowstyle so it is square to its arm in
    POINTS at any aspect ratio, and the perpendicular offset is computed from
    the unordered node pair so the two arms of a mutual pair sit on opposite
    sides instead of on top of each other.
    """
    _assert_not_exam_circuit(edges, where)
    for (a, b, rep) in edges:
        p, q = np.array(nodes[a], float), np.array(nodes[b], float)
        u = (q - p) / np.linalg.norm(q - p)
        lo, hi = sorted((a, b))
        base = np.array(nodes[hi], float) - np.array(nodes[lo], float)
        base = base / np.linalg.norm(base)
        nrm = np.array([-base[1], base[0]])
        off = nrm * (curve if a == lo else -curve)
        # An arm displaced sideways must be trimmed by the chord, not by the
        # radius, or it stops short and floats clear of the circle it is
        # supposed to touch. Offsets at or beyond the radius cannot meet the
        # node at all, so they are not allowed.
        d = abs(curve)
        assert d < NODE_R, f"offset {d} must be inside the node radius {NODE_R}"
        trim = np.sqrt(NODE_R ** 2 - d ** 2) + 0.055   # clear of the outline
        p2, q2 = p + off + u * trim, q + off - u * trim
        ax.annotate("", xy=q2, xytext=p2, zorder=2,
                    arrowprops=dict(arrowstyle="-" if rep else "-|>",
                                    lw=2.0, color=MUTED, mutation_scale=16,
                                    shrinkA=0, shrinkB=0))
        if rep:
            ax.annotate("", xy=q2, xytext=q2 - u * 0.02, zorder=3,
                        arrowprops=dict(arrowstyle="|-|,widthA=0,widthB=6",
                                        lw=3.2, color=MUTED, mutation_scale=1,
                                        shrinkA=0, shrinkB=0))


def _loop_panel(ax, nodes, edges, known, caption, back=None, curve=0.0):
    """One frame of a walk around a loop.

    `curve` bows the edges apart, which a two-node loop needs: drawn straight,
    X -| Y and Y -| X land on the same segment and read as a single edge.
    Limits are computed from the node positions rather than typed, so the
    aspect stays equal without squashing the drawing.
    """
    xs = [p[0] for p in nodes.values()]
    ys = [p[1] for p in nodes.values()]
    pad = 0.78
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad - 0.12, max(ys) + pad)
    ax.axis("off")
    ax.set_aspect("equal")

    _draw_edges(ax, nodes, edges, curve, where=caption)
    for name, (x, y) in nodes.items():
        st = known.get(name)
        # "back-*" is the disturbance ARRIVING home. The last panel used to
        # repeat the previous one exactly and assert a return it never drew.
        col = {"up": TEAL, "down": AMBER,
               "back-down": RED, "back-up": RED, None: RULE}[st]
        ax.add_patch(plt.Circle((x, y), 0.16, facecolor="white",
                                edgecolor=col, lw=3.0, zorder=4))
        ax.text(x, y, name, ha="center", va="center", fontsize=17,
                fontweight="bold", color=INK if st else MUTED, zorder=5)
        if st:
            glyph = {"up": "\u2191", "down": "\u2193",
                     "back-up": "\u21d1", "back-down": "\u21d3"}[st]
            ax.text(x, y - 0.56, glyph, ha="center", va="center",
                    fontsize=22 if st.startswith("back") else 19, color=col,
                    fontweight="bold", zorder=5)
            if st.startswith("back"):
                ax.text(x, y - 0.95, "returned", ha="center", va="center",
                        fontsize=11, color=RED, style="italic", zorder=5)
    if back:
        ax.text(np.mean(xs), max(ys) + 0.34, back, ha="center", fontsize=13,
                color=RED, fontweight="bold")
    ax.set_title(caption, fontsize=13.5, color=INK, pad=14)


def fig_round_trip():
    """Walk a disturbance around a MIXED loop, one step per panel.

    X -| Y, Y -| Z, Z -> X: two repressions and one activation. Two inversions,
    an EVEN number, so the disturbance returns UNFLIPPED and the loop latches.

    The exam uses PURE repression rings of three, four and five -- B3.1 and
    B3.2 compare three against four, and B3.5 is the ring of five by name.
    Drawing any of them here would be rehearsing the question rather than
    teaching the walk, so the worked loop carries a mixed sign set and the
    handout hands over a four-gene MIXED loop, then the same loop with one
    edge changed.
    """
    nodes = {"X": (0.5, 0.74), "Y": (1.5, 0.74), "Z": (1.0, 0.10)}
    edges = [("X", "Y", True), ("Y", "Z", True), ("Z", "X", False)]
    steps = [({"X": "up"}, "nudge X up", None),
             ({"X": "up", "Y": "down"}, "X represses Y \u2192 Y falls", None),
             ({"X": "up", "Y": "down", "Z": "up"},
              "Y represses Z \u2192 Z rises", None),
             ({"X": "back-up", "Y": "down", "Z": "up"},
              "Z ACTIVATES X \u2192 X is pushed UP",
              "two flips \u2014 comes back UNFLIPPED")]
    fig, axes = plt.subplots(1, 4, figsize=(13.6, 3.7))
    for ax, (known, cap, back) in zip(axes, steps):
        _loop_panel(ax, nodes, edges, known, cap, back)
    return _save(fig, "s14_round_trip")


def fig_even_latch():
    """The even case, on a mutual ACTIVATION pair.

    X -> Y -> X: zero inversions, which is even, so the disturbance returns
    UNFLIPPED and reinforces what began it. The pair latches.

    Two-gene mutual REPRESSION would make the same point and is the exam's own
    circuit for B1 and B1.4, so it is not drawn here -- `_assert_not_exam_circuit`
    refuses it. Mutual activation also sets up the basin item on the handout,
    which uses this circuit.
    """
    nodes = {"X": (0.55, 0.42), "Y": (1.45, 0.42)}
    edges = [("X", "Y", False), ("Y", "X", False)]
    steps = [({"X": "up"}, "nudge X up", None),
             ({"X": "up", "Y": "up"}, "X activates Y \u2192 Y rises", None),
             ({"X": "back-up", "Y": "up"},
              "Y activates X \u2192 X rises further",
              "zero flips \u2014 comes back UNFLIPPED, so it LATCHES")]
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.8))
    for ax, (known, cap, back) in zip(axes, steps):
        _loop_panel(ax, nodes, edges, known, cap, back, curve=0.12)
    return _save(fig, "s14_even_latch")


# ---------------------------------------------------------------------------
# 2. Basins — the thing B1.3 assesses, on a circuit whose boundary is NOT x = y
# ---------------------------------------------------------------------------
def fig_basins():
    """MUTUAL ACTIVATION: two stable states, a saddle, and the dividing line.

    Not mutual repression. The exam's B1 phase plane is the symmetric toggle
    and B1.3 asks what decides which state a pulse leaves you in, so teaching
    that skill on *any* mutual-repression plane is rehearsal of the question --
    an asymmetric toggle differs from the exam's only in its parameters, which
    is the "different in naming only" failure. This circuit is a different one:

        x -> y,  y -> x        (both ACTIVATING)

    Its two stable states are both-off and both-on rather than high-low and
    low-high, so the picture cannot be transferred to the exam by memory; and
    it carries the idea the session is actually for, because the dividing line
    crosses the x-axis a long way outside the saddle's x-coordinate. A student
    who has learned "get past the middle point" gets this wrong, which is the
    whole point of putting it on the slides.
    """
    a, n = MA_A, MA_N
    rhs = lambda t, s: [a * s[1] ** n / (1 + s[1] ** n) - s[0],
                        a * s[0] ** n / (1 + s[0] ** n) - s[1]]
    # Fixed points on the diagonal: the off state at the origin, the saddle,
    # and the on state. Solved, not quoted.
    h = lambda x: a * x ** n / (1 + x ** n) - x
    xs = np.linspace(1e-6, a * 1.2, 20000)
    v = [h(x) for x in xs]
    diag = [brentq(h, xs[i], xs[i + 1]) for i in range(len(xs) - 1)
            if v[i] * v[i + 1] < 0]
    assert len(diag) == 2, diag
    saddle_x, on_x = sorted(diag)
    saddle, on = (saddle_x, saddle_x), (on_x, on_x)

    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    top = on_x * 1.28

    # Shade by which stable state each starting point reaches.
    gx = np.linspace(0.0, top, 110)
    GX, GY = np.meshgrid(gx, gx)
    dest = np.zeros_like(GX)
    for i in range(GX.shape[0]):
        for j in range(GX.shape[1]):
            s = solve_ivp(rhs, [0, 80], [GX[i, j], GY[i, j]],
                          t_eval=[80], rtol=1e-6, atol=1e-9)
            dest[i, j] = 1.0 if s.y[0, -1] > saddle_x else 0.0
    ax.contourf(GX, GY, dest, levels=[-0.5, 0.5, 1.5],
                colors=[AMBER, CYAN], alpha=0.16)

    # The dividing line is the saddle's STABLE manifold: step off the saddle
    # along its stable eigenvector and integrate BACKWARD.
    def _jac(x, y):
        d = lambda u: a * n * u ** (n - 1) / (1 + u ** n) ** 2
        return np.array([[-1.0, d(y)], [d(x), -1.0]])

    w, V = np.linalg.eig(_jac(*saddle))
    assert np.allclose(w.imag, 0), "a saddle has real eigenvalues"
    w = w.real
    assert w.min() < 0 < w.max(), w
    stable_vec = V[:, int(np.argmin(w))].real
    for sign in (+1, -1):
        p0 = np.array(saddle) + sign * 1e-6 * stable_vec
        sol = solve_ivp(lambda t, s: [-q for q in rhs(t, s)], [0, 30], p0,
                        rtol=1e-11, atol=1e-14, max_step=0.05)
        xp, yp = sol.y
        keep = (xp >= 0) & (yp >= 0) & (xp <= top) & (yp <= top)
        ax.plot(xp[keep], yp[keep], color=RED, lw=2.8, zorder=5)

    # Where the dividing line crosses the x-axis -- the number that kills the
    # "get past the middle point" rule. Found by integrating from (x, 0).
    def _lands_on(x0):
        s = solve_ivp(rhs, [0, 300], [x0, 0.0], t_eval=[300],
                      rtol=1e-10, atol=1e-13)
        return s.y[0, -1] - saddle_x
    xcross = brentq(_lands_on, saddle_x + 1e-3, on_x, xtol=1e-9)
    assert xcross > saddle_x * 1.5, (xcross, saddle_x)

    # nullclines
    uu = np.linspace(0.0, top, 700)
    ax.plot(a * uu ** n / (1 + uu ** n), uu, color=TEAL, lw=2.6,
            label=r"$\dot{x}=0$")
    ax.plot(uu, a * uu ** n / (1 + uu ** n), color=AMBER, lw=2.6, ls="--",
            label=r"$\dot{y}=0$")

    for (px, py), kind in [((0.0, 0.0), "stable"), (saddle, "saddle"),
                           (on, "stable")]:
        ax.plot(px, py, "o", ms=13, zorder=6, clip_on=False,
                mfc="white" if kind == "saddle" else INK,
                mec=RED if kind == "saddle" else INK, mew=3.0)
    ax.annotate(f"saddle\n({saddle_x:.3f}, {saddle_x:.3f})", xy=saddle,
                xytext=(0.78, 1.62), color=RED, fontsize=13, ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax.text(0.055, 0.30, "both OFF", color=INK, fontsize=12.5, rotation=90,
            va="bottom")
    ax.text(on_x * 1.12, on_x * 0.62, "both ON\nwins", color=INK,
            fontsize=13.5, va="top", ha="center")

    # The x-axis crossing, marked, because it is the lesson.
    ax.plot([xcross], [0.0], marker="v", ms=12, color=RED, zorder=7,
            clip_on=False)
    ax.annotate(f"the dividing line meets the $x$-axis\n"
                f"at {xcross:.3f} — not at {saddle_x:.3f}",
                xy=(xcross, 0.02), xytext=(1.22, 0.70),
                color=RED, fontsize=12.5,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))

    ax.set_xlim(0, top); ax.set_ylim(0, top)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$", rotation=0, labelpad=12)
    ax.set_title(rf"mutual ACTIVATION, $\alpha={a:g}$, $n={n:g}$",
                 fontsize=15)
    ax.legend(loc="upper left", framealpha=0.95, fontsize=12)
    return _save(fig, "s14_basins")


# ---------------------------------------------------------------------------
# 2b. The same idea in ONE dimension, where the divide is a NUMBER
# ---------------------------------------------------------------------------
def fig_autoactivator():
    """Positive autoregulation of a single gene: rate balance, three crossings.

    This is the handout's written basin item, and it is one-dimensional on
    purpose. In 1-D the divide between the two states is a single number you
    can read off the plot; the slide's two-gene case then shows why that
    convenience disappears the moment there are two axes. Nothing on the exam
    uses positive autoregulation -- A9 is a single gene REPRESSING itself, and
    it asks about oscillation, not about states.
    """
    b, a, n = AA_B, AA_A, AA_N
    prod = lambda x: b + a * x ** n / (1 + x ** n)
    f = lambda x: prod(x) - x
    xs = np.linspace(1e-9, 3.0, 40000)
    v = [f(x) for x in xs]
    fps = [brentq(f, xs[i], xs[i + 1]) for i in range(len(xs) - 1)
           if v[i] * v[i + 1] < 0]
    assert len(fps) == 3, fps
    low, mid, high = fps

    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    xg = np.linspace(0, 3.0, 700)
    ax.plot(xg, prod(xg), color=TEAL, lw=3.0, label="production  $\\beta + \\alpha x^n/(1+x^n)$")
    ax.plot(xg, xg, color=AMBER, lw=3.0, ls="--", label="removal  $x$")

    for p, kind in zip(fps, ["stable", "unstable", "stable"]):
        ax.plot(p, p, "o", ms=12, zorder=6,
                mfc="white" if kind == "unstable" else INK,
                mec=RED if kind == "unstable" else INK, mew=2.8)
    ax.annotate(f"the divide\n$x = {mid:.3f}$", xy=(mid, mid),
                xytext=(mid - 0.08, mid + 0.80), color=RED, fontsize=13,
                ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax.text(low - 0.03, low + 0.16, f"OFF\n{low:.3f}", color=INK,
            fontsize=12.5, ha="center", va="bottom")
    ax.text(high + 0.30, high - 0.10, f"ON\n{high:.3f}", color=INK,
            fontsize=12.5, ha="left", va="center")

    # Flow on the x-axis: production above removal pushes right.
    for x0 in (0.10, 0.45, 1.00, 1.60, 2.45):
        d = f(x0)
        ax.annotate("", xy=(x0 + 0.17 * np.sign(d), -0.085),
                    xytext=(x0, -0.085), annotation_clip=False,
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.0,
                                    mutation_scale=12))

    ax.set_xlim(0, 3.0); ax.set_ylim(-0.24, 2.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("rate", rotation=0, labelpad=16)
    ax.set_title(rf"one gene activating itself: $\beta={b:g}$, "
                 rf"$\alpha={a:g}$, $n={n:g}$", fontsize=14)
    ax.legend(loc="upper left", framealpha=0.95, fontsize=11.5)
    return _save(fig, "s14_autoactivator")


# ---------------------------------------------------------------------------
# 3. Signs of a Jacobian, read straight off the wiring
# ---------------------------------------------------------------------------
def fig_jacobian_signs():
    """Two wirings, two sign patterns, and where every entry comes from.

    The point of the panel is that NOTHING is differentiated: each entry is
    read off the diagram. The diagonal carries the species' own removal; an
    off-diagonal carries only how j changes i's production.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2))
    # The exam's B1.4 asks for the MUTUAL REPRESSION sign pattern on exactly
    # these equations, so that circuit is not drawn here. Worked: the
    # activator-repressor. Contrast: a two-step cascade, where one species does
    # not act on the other at all and an off-diagonal is therefore ZERO -- a
    # case neither the exam nor any handout has shown them.
    panels = [
        ("activator \u2013 repressor", [("X", "Y", False), ("Y", "X", True)],
         [["\u2212", "\u2212"], ["+", "\u2212"]],
         "one POSITIVE off-diagonal"),
        ("a cascade,  X \u2192 Y", [("X", "Y", False)],
         [["\u2212", "0"], ["+", "\u2212"]],
         "Y does not act on X at all \u2014 that entry is ZERO"),
    ]
    for ax, (name, edges, signs, note) in zip(axes, panels):
        ax.set_xlim(0, 2.0); ax.set_ylim(-1.45, 1.05)
        ax.axis("off"); ax.set_aspect("equal")
        nodes = {"X": (0.62, 0.62), "Y": (1.38, 0.62)}
        _draw_edges(ax, nodes, edges, curve=0.12, where=name)
        for nm, (x, y) in nodes.items():
            ax.add_patch(plt.Circle((x, y), 0.17, facecolor="white",
                                    edgecolor=INK, lw=2.4, zorder=4))
            ax.text(x, y, nm, ha="center", va="center", fontsize=17,
                    fontweight="bold", color=INK, zorder=5)

        # the sign matrix, with tight brackets
        cx, cy, dx, dy = 1.00, -0.52, 0.22, 0.26
        ax.text(cx - 0.52, cy, "$J=$", fontsize=19, color=INK,
                ha="right", va="center")
        for r in range(2):
            for c in range(2):
                ax.text(cx + (c - 0.5) * 2 * dx, cy + (0.5 - r) * 2 * dy,
                        signs[r][c], fontsize=23, ha="center", va="center",
                        fontweight="bold",
                        color=(TEAL if signs[r][c] == "+"
                               else (MUTED if signs[r][c] == "0" else INK)))
        for sx in (cx - 2.1 * dx, cx + 2.1 * dx):
            ax.plot([sx, sx], [cy - 1.45 * dy, cy + 1.45 * dy],
                    color=INK, lw=2.0)
        ax.text(cx, cy - 2.4 * dy, note, fontsize=13.5, color=RED,
                ha="center", va="top", fontweight="bold")
        ax.set_title(name, fontsize=15, color=INK)

    axes[0].text(1.0, -1.38,
                 "diagonal = that species' own removal (\u2212 unless it acts on itself)",
                 fontsize=12, color=MUTED, ha="center", va="bottom")
    axes[1].text(1.0, -1.38,
                 "off-diagonal = how j changes i's PRODUCTION \u2014 none, none",
                 fontsize=12, color=MUTED, ha="center", va="bottom")
    return _save(fig, "s14_jacobian_signs")


# ---------------------------------------------------------------------------
# 4. What makes a time course — start, initial slope, end
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 5. Noise margins on log axes — the A6 convention, built one step at a time
# ---------------------------------------------------------------------------
def fig_margins_steps():
    """Four panels building the log-axis margin construction, one move each.

    Session 13's convention: the gain is the LOG slope, a threshold is where
    its magnitude is 1, and a margin is a horizontal DISTANCE on the input
    axis rather than a subtraction of two numbers read off different axes.

    The whole trick is the carry across out = in, so panel 3 draws the carry
    itself — along to the diagonal, then down — instead of asserting it.

    This gate is NOT the exam's. Exam: ymin 0.2, ymax 8, K 0.8, n 4. Here the
    levels are further apart so both margins are a visible distance on a
    projected slide.
    """
    ymin, ymax, K, n = 0.12, 16.0, 0.8, 5.0
    y = lambda x: ymin + (ymax - ymin) / (1 + (x / K) ** n)
    h = 1e-6
    G = lambda x: (np.log(y(x * (1 + h))) - np.log(y(x))) / np.log1p(h)
    xIL = brentq(lambda x: abs(G(x)) - 1, 1e-4, K)
    xIH = brentq(lambda x: abs(G(x)) - 1, K, 200)
    yOH, yOL = y(xIL), y(xIH)
    NML, NMH = np.log10(xIL / yOL), np.log10(yOH / xIH)
    assert NML > 0.3 and NMH > 0.3, (NML, NMH)
    assert (ymin, ymax, K, n) != (0.2, 8.0, 0.8, 4.0), "must not be the exam gate"

    LO, HI = 0.05, 60.0
    xx = np.geomspace(LO, HI, 1400)
    fig, axes = plt.subplots(1, 4, figsize=(15.6, 4.5))
    titles = ["1.  the transfer curve, log–log",
              "2.  thresholds: where $|G| = 1$",
              "3.  carry each output across $out=in$",
              "4.  the margin is the gap that is left"]

    for k, ax in enumerate(axes):
        ax.loglog(xx, y(xx), color=TEAL, lw=3.0, zorder=4)
        ax.loglog([LO, HI], [LO, HI], color=MUTED, lw=1.5, ls="--", zorder=2)
        ax.text(HI * 0.55, HI * 0.80, "$out=in$", color=MUTED, fontsize=12,
                ha="right", va="bottom", rotation=45, rotation_mode="anchor")

        if k >= 1:
            for xv, lab in ((xIL, "$x_{IL}$"), (xIH, "$x_{IH}$")):
                ax.plot([xv, xv], [LO, y(xv)], color=RULE, lw=1.5, zorder=3)
                ax.text(xv, LO * 1.12, lab, fontsize=13, color=INK,
                        ha="center", va="bottom")
        if k >= 2:
            # carry y_OL and y_OH across the diagonal and down to the x axis
            for yv, col in ((yOL, AMBER), (yOH, AMBER)):
                ax.plot([LO, yv], [yv, yv], color=col, lw=1.6, ls=":", zorder=3)
                ax.plot([yv, yv], [yv, LO], color=col, lw=1.6, ls=":", zorder=3)
                ax.plot([yv], [yv], "o", ms=6, color=col, zorder=5)
            ax.text(LO * 1.15, yOH * 0.62, "$y_{OH}$", fontsize=13, color=INK,
                    ha="left", va="top")
            ax.text(LO * 1.15, yOL, "$y_{OL}$", fontsize=13, color=INK,
                    ha="left", va="bottom")
        if k == 3:
            for (a, b, lab, yband) in ((yOL, xIL, "$NM_L$", 0.085),
                                       (xIH, yOH, "$NM_H$", 0.085)):
                ax.annotate("", xy=(b, yband), xytext=(a, yband), zorder=6,
                            arrowprops=dict(arrowstyle="<|-|>", color=RED,
                                            lw=2.6, mutation_scale=14,
                                            shrinkA=0, shrinkB=0))
                ax.text(np.sqrt(a * b), yband * 1.22, lab, color=RED,
                        fontsize=16, ha="center", va="bottom")

        ax.set_xlim(LO, HI); ax.set_ylim(LO, HI)
        ax.set_aspect("equal")
        ax.set_title(titles[k], fontsize=13.5, color=INK)
        ax.set_xlabel("input  (log)", fontsize=12)
        if k == 0:
            ax.set_ylabel("output  (log)", fontsize=12)

    return _save(fig, "s14_margins_steps")


# ---------------------------------------------------------------------------
# 6. Feedforward, on two loops the exam does not use
# ---------------------------------------------------------------------------
#
# The exam's pair is an INCOHERENT type-1 with AND (a pulse) and a COHERENT
# type-1 with AND (a delayed rise). Neither appears here. These two are:
#
#   cascade  X -> Y -> Z            delayed BOTH ways -- a symmetric delay
#   C1 + OR  X -> Z and X -> Y -> Z fast up, delayed DOWN -- sign-sensitive,
#                                   and in the OPPOSITE direction to the
#                                   exam's AND version
#
# A student who leaves with "coherent feedforward delays the ON step" gets
# this one wrong, which is the point: the gate decides the direction.
KZ_FAST = 5.0          # Z follows its promoter quickly; Y sets the clock
X_ON, X_OFF = 0.0, 12.0


def _ffl_traces():
    from scipy.integrate import solve_ivp
    H = lambda u, K=0.4, n=3: u ** n / (K ** n + u ** n)
    xof = lambda t: 1.0 if X_ON <= t < X_OFF else 0.0

    def casc(t, s):
        Y, Z = s
        return [H(xof(t)) - Y, KZ_FAST * (H(Y) - Z)]

    def c1or(t, s):
        Y, Z = s
        return [H(xof(t)) - Y, KZ_FAST * (max(H(xof(t)), H(Y)) - Z)]

    t = np.linspace(0, 20, 20001)
    out, nodes = {}, {}
    for name, f in (("cascade", casc), ("c1or", c1or)):
        sol = solve_ivp(f, [0, 20], [0, 0], dense_output=True, max_step=0.005,
                        rtol=1e-10, atol=1e-12)
        out[name] = sol.sol(t)[1]
        # Every node, not just the output. Adam, 11 October: the worked slide
        # plotted Z alone, so the mechanism -- Y lagging, and Z in the OR loop
        # leaving with X rather than with Y -- was invisible on the one
        # surface built to show it.
        nodes[name] = {"X": np.array([xof(tt) for tt in t]),
                       "Y": sol.sol(t)[0], "Z": sol.sol(t)[1]}
    _ffl_traces.nodes = nodes
    # the contract: the cascade is late both ways; the OR loop only on the way down
    def delays(Z):
        m = Z.max()
        on = t[np.argmax(Z >= 0.5 * m)]
        aft = t >= X_OFF
        return on, t[aft][np.argmax(Z[aft] <= 0.5 * m)] - X_OFF
    on_c, off_c = delays(out["cascade"])
    on_o, off_o = delays(out["c1or"])
    assert on_c > 3 * on_o, (on_c, on_o)        # the OR loop is prompt
    assert off_o > 4 * on_o, (off_o, on_o)      # and late coming down
    return t, out, (on_c, off_c, on_o, off_o)


def _ffl_mini_circuit(ax, shortcut, title):
    """The wiring, small, to sit above a column of traces.

    Adam, 11 October: "I don't think it is clear how the circuit changed from
    slide 46 to 47." It was not: the worked surface and the release surface
    both carried traces labelled "Loop P" and "Loop Q", neither drew a loop,
    and the one wire that separates them was six slides back.

    Drawn LEFT TO RIGHT. A vertical chain in a wide, short cell is scaled to
    the cell's height by `set_aspect("equal")` and ends up a thumbnail with
    the gate sitting on top of the output node.
    """
    _assert_not_exam_circuit(
        [("X", "Y", False), ("Y", "Z", False)] +
        ([("X", "Z", False)] if shortcut else []), title)
    ax.set_xlim(-0.45, 2.70); ax.set_ylim(-1.02, 0.62)
    ax.axis("off"); ax.set_aspect("equal")
    # Z is pushed out to 2.25 so the gate has a visible arm on BOTH sides of
    # it: at Z = 2.0 the gap between gate and node came out at 0.015.
    pos = {"X": (0.0, 0.0), "Y": (1.0, 0.0), "Z": (2.25, 0.0)}
    R, GX, GR = 0.20, 1.60, 0.145          # node r, gate centre x, gate r

    def arm(p, q, pa, pb, color=MUTED, lw=2.2):
        p, q = np.array(p, float), np.array(q, float)
        u = (q - p) / np.linalg.norm(q - p)
        ax.annotate("", xy=q - u * pb, xytext=p + u * pa,
                    arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                    mutation_scale=15, shrinkA=0, shrinkB=0))

    arm(pos["X"], pos["Y"], R + 0.04, R + 0.04)
    if shortcut:
        arm(pos["Y"], (GX, 0.0), R + 0.04, GR + 0.04)
        arm((GX, 0.0), pos["Z"], GR + 0.04, R + 0.04)
        # the direct arm, bowed UNDER the chain and into the gate
        ax.annotate("", xy=(GX - 0.02, -GR - 0.03), xytext=(0.0, -R - 0.03),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color=RED,
                                    mutation_scale=15,
                                    connectionstyle="arc3,rad=0.38"))
        ax.text(0.80, -0.86, "the extra wire", fontsize=12.5, color=RED,
                ha="center", va="center")
        ax.add_patch(plt.Circle((GX, 0.0), GR, facecolor="white",
                                edgecolor=TEAL, lw=2.4, zorder=5))
        ax.text(GX, 0.0, "OR", ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=TEAL, zorder=6)
    else:
        arm(pos["Y"], pos["Z"], R + 0.04, R + 0.04)
        ax.text(1.12, -0.86, "one route only", fontsize=12.5, color=MUTED,
                ha="center", va="center")
    for name, (x, y) in pos.items():
        ax.add_patch(plt.Circle((x, y), R, facecolor="white",
                                edgecolor=RULE, lw=3.0, zorder=7))
        ax.text(x, y, name, ha="center", va="center", fontsize=17,
                fontweight="bold", color=MUTED, zorder=8)
    ax.set_title(title, fontsize=15.5, color=INK, pad=6)


def _ffl_grid(fig):
    """Four rows per column: the circuit, then X, then Y, then Z."""
    return fig.add_gridspec(4, 2, height_ratios=[1.00, 0.60, 0.60, 1.02],
                            hspace=0.46, wspace=0.17)


def _ffl_node_rows(fig, gs, col, key):
    """The two GIVEN traces, X and Y, under a column's circuit."""
    t, _, _ = _ffl_traces()
    nodes = _ffl_traces.nodes
    for row, (nm, c) in enumerate((("X", AMBER), ("Y", TEAL)), start=1):
        ax = fig.add_subplot(gs[row, col])
        ax.plot(t, nodes[key][nm], color=c, lw=2.6)
        ax.set_xlim(0, 20); ax.set_ylim(-0.08, 1.16)
        ax.set_yticks([]); ax.set_xticks([])
        ax.set_ylabel(nm, rotation=0, labelpad=12, fontsize=15, color=c)
        ax.grid(True, axis="x", color=RULE, lw=0.7, alpha=0.5)


def fig_ffl_axes():
    """Blank Z axes for the student — WITH the circuit and the given traces.

    The student is asked to draw Z for each loop. That cannot be done from a
    label, so each column carries its own wiring diagram and its own X and Y;
    only the Z panel is empty, which is the panel the item is about.
    """
    fig = plt.figure(figsize=(10.4, 7.0))
    gs = _ffl_grid(fig)
    for col, (key, shortcut, title) in enumerate(
            (("cascade", False, "Loop P — cascade"),
             ("c1or", True, "Loop Q — shortcut + OR"))):
        _ffl_mini_circuit(fig.add_subplot(gs[0, col]), shortcut, title)
        _ffl_node_rows(fig, gs, col, key)
        axz = fig.add_subplot(gs[3, col])
        axz.set_xlim(0, 20); axz.set_ylim(0, 1.16)
        axz.set_yticks([])
        axz.set_ylabel("Z", rotation=0, labelpad=12, fontsize=16, color=INK)
        axz.set_xlabel("time  (Y lifetimes)", fontsize=13)
        axz.grid(True, axis="x", color=RULE, lw=0.8, alpha=0.6)
        axz.text(10, 0.56, "draw Z here", ha="center", va="center",
                 fontsize=15, color=MUTED, style="italic")
    fig.suptitle("X is given. Y is given — it is the slow one. Draw Z.",
                 fontsize=16.5, color=INK, y=0.98)
    fig.subplots_adjust(top=0.87)
    return _save(fig, "s14_ffl_axes", tight=False)


def fig_ffl_worked():
    """WORKED: both circuits, every node, and the delays measured on Z.

    Rebuilt 11 October. The previous version plotted the OUTPUT only, for two
    loops it did not draw, with the input squeezed onto the same axis as a
    thin line -- so the one thing the surface exists to show, why the OR loop
    is prompt going up, could not be read off it. With X, Y and Z stacked it
    is visible directly: in Loop Q, Z leaves with X; in Loop P it waits for Y.
    """
    t, out, (on_c, off_c, on_o, off_o) = _ffl_traces()

    fig = plt.figure(figsize=(11.6, 6.6))
    gs = _ffl_grid(fig)
    for col, (key, shortcut, title, (don, doff), note) in enumerate((
            ("cascade", False, "Loop P — cascade", (on_c, off_c),
             "late BOTH ways"),
            ("c1or", True, "Loop Q — shortcut + OR", (on_o, off_o),
             "prompt up, late down"))):
        _ffl_mini_circuit(fig.add_subplot(gs[0, col]), shortcut, title)
        _ffl_node_rows(fig, gs, col, key)
        axz = fig.add_subplot(gs[3, col])
        axz.plot(t, out[key], color=INK, lw=3.2, zorder=4)
        for x0, dd, tag in ((X_ON, don, "ON"), (X_OFF, doff, "OFF")):
            axz.annotate("", xy=(x0 + dd, 0.50), xytext=(x0, 0.50),
                         arrowprops=dict(arrowstyle="<|-|>", color=RED,
                                         lw=2.2, mutation_scale=12))
            axz.text(x0 + dd + 0.5, 0.50, f"{tag} {dd:.1f}", color=RED,
                     fontsize=13.5, ha="left", va="center")
        axz.set_xlim(0, 20); axz.set_ylim(0, 1.16)
        axz.set_yticks([])
        axz.set_ylabel("Z", rotation=0, labelpad=12, fontsize=16, color=INK)
        axz.set_xlabel("time  (Y lifetimes)", fontsize=13)
        axz.grid(True, axis="x", color=RULE, lw=0.8, alpha=0.6)
        axz.text(6.6, 0.26, note, fontsize=14.5, color=RED, ha="center")

    # The claims this panel makes about its own curves, checked against them.
    # The window is 0.3 Y-lifetimes: by t = 1 the cascade has caught up to
    # 0.66 and the comparison stops meaning anything, which is exactly why
    # "leaves with X" has to be measured at the leaving and not later.
    zc, zo = out["cascade"], out["c1or"]
    early = t < 0.3
    assert zo[early].max() > 4 * zc[early].max(), \
        (zo[early].max(), zc[early].max())
    assert on_o < on_c / 4, (on_o, on_c)          # prompt vs late, going up
    assert abs(off_o - off_c) < 0.25, (off_o, off_c)   # same, coming down
    fig.suptitle("Same input, same slow Y — one extra wire, and only the ON "
                 "end moves", fontsize=16.5, color=INK, y=0.98)
    fig.subplots_adjust(top=0.87)
    return _save(fig, "s14_ffl_worked", tight=False)


# ===========================================================================
# FRAMES AND DEBRIEFS
# ===========================================================================
#
# WHY THESE EXIST (11 October 2026). Adam, reviewing the first build of this
# deck: every segment "starts in the middle and stops before the end". Each
# motion opened on a title and a first algebra line -- no object, no question,
# no statement of what a finished answer looks like -- and every one of the
# five student releases cut straight to an unrelated topic, so the room worked
# a problem and never saw it answered.
#
# The rule that came out of it, now in docs/lecture-design.md: FRAME, BUILD,
# RELEASE, DEBRIEF. These figures are the first and last of those four.
#
# A frame figure draws the OBJECT and the possible ANSWERS before any algebra.
# A debrief figure answers the released item, on the item's own circuit.


def fig_loop_outcomes():
    """FRAME for motion 1: the three things a wiring diagram can tell you.

    The outcome the session is actually after, which the first build buried
    under the word "buys": given a wiring diagram and nothing else, say what
    the circuit DOES -- oscillate, latch into one of two states, or settle to
    one -- without solving anything.

    Three circuits, three verdicts, none of them the exam's. The panels share
    one set of limits rather than taking them from their own node positions,
    because three equal-aspect panels of different extents put their titles
    and their verdicts at three different heights.
    """
    cases = [
        ("one inversion in three  (odd)",
         {"X": (0.30, 0.80), "Y": (1.30, 0.80), "Z": (0.80, 0.10)},
         [("X", "Y", False), ("Y", "Z", True), ("Z", "X", False)],
         "comes back FLIPPED",
         "could be a CLOCK", "if also unshrunk, and slow enough", TEAL),
        ("no inversions at all  (zero is even)",
         {"X": (0.30, 0.45), "Y": (1.30, 0.45)},
         [("X", "Y", False), ("Y", "X", False)],
         "comes back UNFLIPPED",
         "a LATCH", "it has two states, and it keeps one", AMBER),
        ("no loop at all",
         {"X": (0.10, 0.45), "Y": (0.80, 0.45), "Z": (1.50, 0.45)},
         [("X", "Y", False), ("Y", "Z", True)],
         "never comes back",
         "SETTLES", "nothing returns, so nothing can be amplified", MUTED),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.6))
    for ax, (what, nodes, edges, back, verdict, why, col) in zip(axes, cases):
        ax.set_xlim(-0.45, 1.95); ax.set_ylim(-0.55, 1.35)
        ax.axis("off"); ax.set_aspect("equal")
        _draw_edges(ax, nodes, edges,
                    curve=0.10 if len(nodes) == 2 else 0.0, where=what)
        for name, (x, y) in nodes.items():
            ax.add_patch(plt.Circle((x, y), 0.16, facecolor="white",
                                    edgecolor=RULE, lw=3.0, zorder=4))
            ax.text(x, y, name, ha="center", va="center", fontsize=17,
                    fontweight="bold", color=MUTED, zorder=5)
        ax.text(0.5, 1.02, what, transform=ax.transAxes, ha="center",
                fontsize=16, color=INK)
        ax.text(0.5, -0.03, back, transform=ax.transAxes, ha="center",
                fontsize=16, color=INK, style="italic")
        ax.text(0.5, -0.17, verdict, transform=ax.transAxes, ha="center",
                fontsize=20, color=col, fontweight="bold")
        ax.text(0.5, -0.30, why, transform=ax.transAxes, ha="center",
                fontsize=14, color=MUTED)
    # No suptitle: the slide this sits on carries the same sentence as its
    # title, and printing it twice wastes the only band of space the panel
    # has for the three verdicts.
    fig.subplots_adjust(bottom=0.24, top=0.88, left=0.02, right=0.98)
    return _save(fig, "s14_loop_outcomes", tight=False)


def fig_loop_debrief():
    """DEBRIEF for item 1: the four-gene loop, answered, beside its variant.

    The released item and the one-edge change, side by side with the walk
    resolved on each, so the room sees that parity is the only thing that
    moved.

    Not drawn with `_loop_panel`: that helper hangs each node's up/down glyph
    directly BELOW the node, which works for a triangle and collides on a
    square -- X's glyph lands on W, and W's falls off the panel. Here the
    glyph is pushed radially OUTWARD from the centre of the loop, so a layout
    of any shape keeps its labels clear of its own nodes.
    """
    nodes = {"X": (0.0, 1.0), "Y": (1.0, 1.0),
             "Z": (1.0, 0.0), "W": (0.0, 0.0)}
    cx = np.mean([p[0] for p in nodes.values()])
    cy = np.mean([p[1] for p in nodes.values()])

    panels = [
        ([("X", "Y", True), ("Y", "Z", False), ("Z", "W", True),
          ("W", "X", True)],
         "as released:  three bars, one arrow",
         {"X": ("back-down", "\u21d3"), "Y": ("down", "\u2193"),
          "Z": ("down", "\u2193"), "W": ("up", "\u2191")},
         "THREE flips — odd", "returns FLIPPED — passes the FIRST test only", TEAL),
        ([("X", "Y", True), ("Y", "Z", False), ("Z", "W", False),
          ("W", "X", True)],
         "one edge changed:  Z → W",
         {"X": ("back-up", "\u21d1"), "Y": ("down", "\u2193"),
          "Z": ("down", "\u2193"), "W": ("down", "\u2193")},
         "TWO flips — even", "returns UNFLIPPED — it latches, at ANY gain", AMBER),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.6))
    for ax, (edges, cap, known, count, verdict, col) in zip(axes, panels):
        ax.set_xlim(-0.75, 1.75); ax.set_ylim(-0.78, 1.72)
        ax.axis("off"); ax.set_aspect("equal")
        _draw_edges(ax, nodes, edges, where=cap)
        for name, (x, y) in nodes.items():
            state, glyph = known[name]
            back = state.startswith("back")
            c = RED if back else (TEAL if state == "up" else AMBER)
            ax.add_patch(plt.Circle((x, y), 0.16, facecolor="white",
                                    edgecolor=c, lw=3.0, zorder=4))
            ax.text(x, y, name, ha="center", va="center", fontsize=17,
                    fontweight="bold", color=INK, zorder=5)
            # Outward along the radius from the loop's centre.
            d = np.array([x - cx, y - cy], float)
            d /= np.linalg.norm(d)
            gx, gy = x + d[0] * 0.40, y + d[1] * 0.40
            ax.text(gx, gy, glyph, ha="center", va="center",
                    fontsize=23 if back else 20, color=c, fontweight="bold",
                    zorder=5)
            if back:
                ax.text(gx + d[0] * 0.46, gy + d[1] * 0.34, "the nudge,\nback home",
                        ha="center", va="center", fontsize=10.5, color=RED,
                        style="italic", zorder=5)
        ax.set_title(cap, fontsize=17, color=INK, pad=12)
        ax.text(0.5, -0.04, count, transform=ax.transAxes, ha="center",
                fontsize=20, color=col, fontweight="bold")
        ax.text(0.5, -0.15, verdict, transform=ax.transAxes, ha="center",
                fontsize=16, color=INK)
    fig.suptitle("Same four genes, same strengths — change one edge and the "
                 "verdict reverses", fontsize=16, color=INK, y=0.98)
    fig.subplots_adjust(bottom=0.16, top=0.82)
    return _save(fig, "s14_loop_debrief", tight=False)


# ---------------------------------------------------------------------------
# The basin segment, staged
# ---------------------------------------------------------------------------
def _ma_model():
    """Mutual activation: the model, its fixed points, and its divide.

    One place, so the staged frames, the worked panel, the trajectories and
    the movie cannot drift apart from each other.
    """
    a, n = MA_A, MA_N
    rhs = lambda t, s: [a * s[1] ** n / (1 + s[1] ** n) - s[0],
                        a * s[0] ** n / (1 + s[0] ** n) - s[1]]
    h = lambda x: a * x ** n / (1 + x ** n) - x
    xs = np.linspace(1e-6, a * 1.2, 20000)
    v = [h(x) for x in xs]
    diag = [brentq(h, xs[i], xs[i + 1]) for i in range(len(xs) - 1)
            if v[i] * v[i + 1] < 0]
    saddle_x, on_x = sorted(diag)

    def jac(x, y):
        d = lambda u: a * n * u ** (n - 1) / (1 + u ** n) ** 2
        return np.array([[-1.0, d(y)], [d(x), -1.0]])

    w, V = np.linalg.eig(jac(saddle_x, saddle_x))
    w = w.real
    stable_vec = V[:, int(np.argmin(w))].real
    sep = []
    for sign in (+1, -1):
        p0 = np.array([saddle_x, saddle_x]) + sign * 1e-6 * stable_vec
        sol = solve_ivp(lambda t, s: [-q for q in rhs(t, s)], [0, 30], p0,
                        rtol=1e-11, atol=1e-14, max_step=0.05)
        sep.append(sol.y)

    def lands_on(x0):
        s = solve_ivp(rhs, [0, 300], [x0, 0.0], t_eval=[300],
                      rtol=1e-10, atol=1e-13)
        return s.y[0, -1] - saddle_x
    xcross = brentq(lands_on, saddle_x + 1e-3, on_x, xtol=1e-9)
    return rhs, saddle_x, on_x, sep, xcross


def _ma_axes(ax, top):
    ax.set_xlim(0, top); ax.set_ylim(0, top)
    ax.set_xlabel("$x$   (protein X)")
    ax.set_ylabel("$y$", rotation=0, labelpad=12)
    ax.set_aspect("equal")


def fig_basin_stages():
    """BUILD for the basin segment: the plane drawn one object at a time.

    Four frames for `derivation_fig`, so the picture grows with the argument
    instead of arriving finished under a title. The first build put a bare
    phrase -- "Two states is not the whole story" -- in front of a room that
    had not been shown the circuit, the axes, or the question.
    """
    rhs, saddle_x, on_x, sep, xcross = _ma_model()
    a, n = MA_A, MA_N
    top = on_x * 1.28
    uu = np.linspace(0.0, top, 700)
    nx = a * uu ** n / (1 + uu ** n)
    out = []

    titles = ["the circuit, and the plane it lives in",
              "where each gene alone would sit still",
              "three crossings: two states and a saddle",
              "the curve that divides them"]
    for k in range(4):
        fig, ax = plt.subplots(figsize=(5.6, 5.2))
        _ma_axes(ax, top)

        if k == 0:
            # The circuit itself, inset, before any mathematics.
            ax.text(0.5, 0.60, "$X \\longrightarrow Y$\n$Y \\longrightarrow X$",
                    transform=ax.transAxes, ha="center", va="center",
                    fontsize=26, color=INK)
            ax.text(0.5, 0.34, "each gene switches the other ON.\n"
                               "a point in this plane is one cell,\n"
                               "right now.",
                    transform=ax.transAxes, ha="center", va="center",
                    fontsize=13, color=MUTED)
        if k >= 1:
            ax.plot(nx, uu, color=TEAL, lw=2.6, label=r"$\dot{x}=0$")
            ax.plot(uu, nx, color=AMBER, lw=2.6, ls="--", label=r"$\dot{y}=0$")
            ax.legend(loc="upper left", framealpha=0.95, fontsize=11.5)
        if k >= 2:
            for (px, py), kind in [((0.0, 0.0), "stable"),
                                   ((saddle_x, saddle_x), "saddle"),
                                   ((on_x, on_x), "stable")]:
                ax.plot(px, py, "o", ms=12, zorder=6, clip_on=False,
                        mfc="white" if kind == "saddle" else INK,
                        mec=RED if kind == "saddle" else INK, mew=2.8)
            # Beside each dot, horizontal and short: a rotated label up the
            # y-axis runs straight through where the divide is drawn in the
            # next frame.
            ax.text(0.04, 0.17, "both OFF", fontsize=11.5, color=INK,
                    ha="left", va="bottom")
            ax.text(on_x - 0.10, on_x + 0.16, "both ON", fontsize=12,
                    color=INK, ha="right", va="bottom")
        if k >= 3:
            for xp, yp in sep:
                keep = (xp >= 0) & (yp >= 0) & (xp <= top) & (yp <= top)
                ax.plot(xp[keep], yp[keep], color=RED, lw=2.8, zorder=5)
            ax.text(xcross + 0.10, 0.26, "the divide", color=RED,
                    fontsize=12.5)

        ax.set_title(titles[k], fontsize=13.5, color=INK)
        out.append(_save(fig, f"s14_basin_stage{k + 1}"))
    return out


def _basin_cases():
    """The four pulses the worked slide and the movie both run.

    Chosen around the x-axis crossing so two fall back and two switch, and so
    one of each pair is close enough to it that "which side" is the only thing
    separating them.
    """
    _, _, _, _, xcross = _ma_model()
    return [(0.50, "pulse to 0.50"), (round(xcross - 0.02, 3), "just inside"),
            (round(xcross + 0.02, 3), "just outside"), (1.20, "pulse to 1.20")]


def fig_basin_trajectories():
    """WORKED: the same four pulses, as paths on the plane and as traces.

    Adam, 11 October: "it might be good to have simulations of different cases
    to demonstrate". Shading says which side wins; a trajectory says what the
    cell actually did, and the pair either side of the divide is the whole
    argument -- two pulses 0.04 apart, opposite fates.

    This panel is also the POSTER FRAME of s14_basin_runs.mp4, so a slide that
    is never clicked still carries the finished comparison.
    """
    rhs, saddle_x, on_x, sep, xcross = _ma_model()
    a, n = MA_A, MA_N
    top = on_x * 1.28
    uu = np.linspace(0.0, top, 700)
    nx = a * uu ** n / (1 + uu ** n)
    cases = _basin_cases()

    fig = plt.figure(figsize=(12.6, 5.4))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1.0], hspace=0.42,
                          wspace=0.22)
    axp = fig.add_subplot(gs[:, 0])
    axx = fig.add_subplot(gs[0, 1])
    axy = fig.add_subplot(gs[1, 1])

    _ma_axes(axp, top)
    axp.plot(nx, uu, color=TEAL, lw=2.0, alpha=0.45)
    axp.plot(uu, nx, color=AMBER, lw=2.0, ls="--", alpha=0.45)
    for xp, yp in sep:
        keep = (xp >= 0) & (yp >= 0) & (xp <= top) & (yp <= top)
        # Above the trajectories: the divide is the thing being demonstrated,
        # and four paths drawn over it hide exactly the part that matters.
        axp.plot(xp[keep], yp[keep], color=RED, lw=3.0, zorder=9)

    cols = [AMBER, AMBER, TEAL, TEAL]
    styles = ["-", "--", "--", "-"]
    tt = np.linspace(0, 12, 600)
    for (x0, lab), col, ls in zip(cases, cols, styles):
        sol = solve_ivp(rhs, [0, 12], [x0, 0.0], t_eval=tt,
                        rtol=1e-10, atol=1e-13)
        axp.plot(sol.y[0], sol.y[1], color=col, lw=2.6, ls=ls, zorder=6)
        axp.plot([x0], [0.0], "o", ms=8, color=col, zorder=7, clip_on=False)
        axx.plot(tt, sol.y[0], color=col, lw=2.4, ls=ls,
                 label=f"{lab}  ($x_0={x0:g}$)")
        axy.plot(tt, sol.y[1], color=col, lw=2.4, ls=ls)

    for (px, py), kind in [((0.0, 0.0), "stable"),
                           ((saddle_x, saddle_x), "saddle"),
                           ((on_x, on_x), "stable")]:
        axp.plot(px, py, "o", ms=12, zorder=8, clip_on=False,
                 mfc="white" if kind == "saddle" else INK,
                 mec=RED if kind == "saddle" else INK, mew=2.6)
    axp.annotate(f"the divide crosses here: $x={xcross:.3f}$",
                 xy=(xcross, 0.0), xytext=(0.90, 0.60), color=RED,
                 fontsize=12,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
    axp.set_title("every pulse starts on the $x$-axis", fontsize=13.5,
                  color=INK)

    for ax, lab, ss in ((axx, "$x(t)$", on_x), (axy, "$y(t)$", on_x)):
        ax.axhline(ss, color=MUTED, ls=":", lw=1.2)
        ax.set_xlim(0, 12); ax.set_ylim(-0.1, top)
        ax.set_ylabel(lab, rotation=0, labelpad=16)
        ax.grid(True, color=RULE, lw=0.7, alpha=0.6)
    axy.set_xlabel("time  (protein lifetimes)")
    axx.legend(loc="lower right", fontsize=10.5, framealpha=0.95)

    # The pair either side of the divide must actually split, or the panel is
    # making a claim the simulation does not support.
    inside, outside = cases[1][0], cases[2][0]
    e_in = solve_ivp(rhs, [0, 300], [inside, 0.0], t_eval=[300],
                     rtol=1e-10, atol=1e-13).y[0, -1]
    e_out = solve_ivp(rhs, [0, 300], [outside, 0.0], t_eval=[300],
                      rtol=1e-10, atol=1e-13).y[0, -1]
    assert e_in < saddle_x < e_out, (inside, e_in, outside, e_out)

    # No suptitle: the slide carries this sentence as its title, and
    # printing it twice costs the height the panel needs.
    fig.subplots_adjust(top=0.94)
    return _save(fig, "s14_basin_trajectories", tight=False)


def fig_autoactivator_debrief():
    """DEBRIEF for item 4: the rate balance answered, with the traces beside it.

    Left, the sketch they were asked for, with the flow arrows that do the
    work. Right, what the cell actually does on either side of the divide --
    0.68 falls back, 0.69 climbs, which is the number the item asks for made
    visible rather than asserted.
    """
    b, a, n = AA_B, AA_A, AA_N
    prod = lambda x: b + a * x ** n / (1 + x ** n)
    f = lambda x: prod(x) - x
    xs = np.linspace(1e-9, 3.0, 40000)
    v = [f(x) for x in xs]
    low, mid, high = [brentq(f, xs[i], xs[i + 1]) for i in range(len(xs) - 1)
                      if v[i] * v[i + 1] < 0]

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(12.4, 4.6))

    xg = np.linspace(0, 3.0, 700)
    axl.plot(xg, prod(xg), color=TEAL, lw=3.0, label="production")
    axl.plot(xg, xg, color=AMBER, lw=3.0, ls="--", label="removal")
    axl.fill_between(xg, prod(xg), xg, where=(prod(xg) > xg),
                     color=TEAL, alpha=0.10)
    for p, kind in zip([low, mid, high], ["stable", "unstable", "stable"]):
        axl.plot(p, p, "o", ms=12, zorder=6,
                 mfc="white" if kind == "unstable" else INK,
                 mec=RED if kind == "unstable" else INK, mew=2.8)
    for x0 in (0.10, 0.45, 1.00, 1.60, 2.45):
        d = f(x0)
        axl.annotate("", xy=(x0 + 0.17 * np.sign(d), -0.14), xytext=(x0, -0.14),
                     annotation_clip=False,
                     arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=2.0,
                                     mutation_scale=12))
    axl.annotate(f"arrows point AWAY\n→ the divide, $x={mid:.3f}$",
                 xy=(mid, mid), xytext=(mid + 0.62, mid + 0.95), color=RED,
                 fontsize=12.5, ha="left",
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.7))
    axl.text(low - 0.03, low + 0.14, f"OFF\n{low:.3f}", color=INK,
             fontsize=12, ha="center", va="bottom")
    axl.text(high + 0.26, high - 0.10, f"ON\n{high:.3f}", color=INK,
             fontsize=12, ha="left", va="center")
    axl.set_xlim(0, 3.0); axl.set_ylim(-0.24, 2.6)
    axl.set_xlabel("$x$"); axl.set_ylabel("rate", rotation=0, labelpad=16)
    axl.set_title("arrows toward a crossing = a state; away = the divide",
                  fontsize=13, color=INK)
    axl.legend(loc="upper left", framealpha=0.95, fontsize=11)

    tt = np.linspace(0, 14, 700)
    rhs = lambda t, s: [f(s[0])]
    for x0, col, lab in ((0.68, AMBER, "pulse to 0.68"),
                         (0.69, TEAL, "pulse to 0.69")):
        sol = solve_ivp(rhs, [0, 14], [x0], t_eval=tt, rtol=1e-11, atol=1e-14)
        axr.plot(tt, sol.y[0], color=col, lw=3.0, label=lab)
        assert abs(sol.y[0, -1] - (low if x0 < mid else high)) < 1e-2
    axr.axhline(mid, color=RED, ls="--", lw=1.8)
    axr.text(13.6, mid + 0.06, f"the divide, {mid:.3f}", color=RED,
             fontsize=11.5, ha="right")
    axr.axhline(low, color=MUTED, ls=":", lw=1.2)
    axr.axhline(high, color=MUTED, ls=":", lw=1.2)
    axr.set_xlim(0, 14); axr.set_ylim(0, 2.3)
    axr.set_xlabel("time  (protein lifetimes)")
    axr.set_ylabel("$x$", rotation=0, labelpad=12)
    axr.set_title("0.01 apart, and they end in different places",
                  fontsize=13, color=INK)
    axr.legend(loc="center right", framealpha=0.95, fontsize=11.5)
    axr.grid(True, color=RULE, lw=0.7, alpha=0.6)
    return _save(fig, "s14_autoactivator_debrief")



# ---------------------------------------------------------------------------
# The Jacobian segment: the matrix, on screen, being filled in
# ---------------------------------------------------------------------------
#
# Adam, 11 October 2026, on slide 20 of the first build: "show the 'matrix'".
# Four surfaces of partial-derivative notation went by and a matrix was never
# drawn -- in a segment whose exam item asks the student to WRITE one.

# U+2212 MINUS SIGN, not hyphen: a hyphen set at 30pt bold reads as a tick
# mark next to a "+" of the same size, which is exactly the comparison the
# panel is asking the room to make.
MINUS = "\u2212"
_SIGN_COL = {MINUS: AMBER, "+": TEAL, "0": RED, "": RULE}


def _matrix_panel(ax, names, entries, title=None, hi=None, box=True):
    """Draw a square sign matrix with its rows and columns labelled.

    `entries` is a dict {(i, j): "+"/"-"/"0"/""} over index pairs. An empty
    string leaves the cell blank, which is what makes this usable as a run of
    frames: the same grid, one more cell filled each time.
    `hi` is a set of cells to ring, for "this is the one that just landed".
    """
    k = len(names)
    ax.set_xlim(-1.25, k + 0.35); ax.set_ylim(-0.30, k + 0.60)
    ax.axis("off"); ax.set_aspect("equal")

    for j, nm in enumerate(names):
        ax.text(j + 0.5, k + 0.18, f"$\\partial {nm}$", ha="center",
                va="bottom", fontsize=14, color=MUTED)
    for i, nm in enumerate(names):
        ax.text(-0.18, k - i - 0.5, f"$\\partial \\dot{{{nm}}}$", ha="right",
                va="center", fontsize=14, color=MUTED)

    if box:
        for xo in (0.0, k):
            side = 1 if xo == 0 else -1
            ax.plot([xo, xo], [0, k], color=INK, lw=2.4)
            ax.plot([xo, xo + side * 0.16], [0, 0], color=INK, lw=2.4)
            ax.plot([xo, xo + side * 0.16], [k, k], color=INK, lw=2.4)

    for (i, j), val in entries.items():
        cx, cy = j + 0.5, k - i - 0.5
        if val:
            ax.text(cx, cy, val, ha="center", va="center", fontsize=30,
                    fontweight="bold", color=_SIGN_COL[val])
        else:
            ax.plot([cx - 0.22, cx + 0.22], [cy - 0.26, cy - 0.26],
                    color=RULE, lw=2.2)
        if hi and (i, j) in hi:
            ax.add_patch(plt.Circle((cx, cy), 0.40, fill=False,
                                    edgecolor=RED, lw=2.4, zorder=6))
    if title:
        ax.set_title(title, fontsize=13.5, color=INK, pad=10)


def fig_jacobian_stages():
    """BUILD for the Jacobian segment: J filled in, one rule at a time.

    Worked on the activator-repressor, which is not an exam circuit. Four
    frames for `derivation_fig`, so the matrix on the left grows as the rule
    on the right is stated -- rather than four slides of notation with no
    matrix anywhere, which is what shipped first.
    """
    nodes = {"X": (0.30, 0.45), "Y": (1.30, 0.45)}
    edges = [("X", "Y", False), ("Y", "X", True)]
    names = ["x", "y"]

    frames = [
        ({}, set(), "the empty matrix, and the wiring it comes from"),
        ({(0, 0): MINUS, (1, 1): MINUS}, {(0, 0), (1, 1)},
         "diagonal: each protein's own removal"),
        ({(0, 0): MINUS, (1, 1): MINUS, (1, 0): "+"}, {(1, 0)},
         "X activates Y  →  raising x raises Y's production"),
        ({(0, 0): MINUS, (1, 1): MINUS, (1, 0): "+", (0, 1): MINUS}, {(0, 1)},
         "Y represses X  →  raising y lowers X's production"),
    ]
    out = []
    for k, (entries, hi, title) in enumerate(frames):
        fig, (axc, axm) = plt.subplots(
            1, 2, figsize=(5.4, 3.0),
            gridspec_kw={"width_ratios": [1.0, 1.15]})
        axc.set_xlim(-0.25, 1.85); axc.set_ylim(-0.42, 1.05)
        axc.axis("off"); axc.set_aspect("equal")
        _draw_edges(axc, nodes, edges, curve=0.10, where="jacobian stages")
        for name, (x, y) in nodes.items():
            axc.add_patch(plt.Circle((x, y), 0.16, facecolor="white",
                                     edgecolor=RULE, lw=3.2, zorder=4))
            axc.text(x, y, name, ha="center", va="center", fontsize=19,
                     fontweight="bold", color=MUTED, zorder=5)
        axc.text(0.5, 0.02, "X activates Y\nY represses X", ha="center",
                 transform=axc.transAxes, fontsize=12, color=MUTED)

        full = {(i, j): entries.get((i, j), "") for i in range(2)
                for j in range(2)}
        _matrix_panel(axm, names, full, hi=hi)
        # NO suptitle. On a split surface the step's own label sits beside
        # this picture and says the same sentence; printing it twice costs
        # the height that makes the circuit and the matrix readable from the
        # back of the room. `title` is kept for the caller's sake.
        _ = title
        fig.subplots_adjust(top=0.98, bottom=0.02, wspace=0.02,
                            left=0.02, right=0.98)
        out.append(_save(fig, f"s14_jacobian_stage{k + 1}", tight=False))
    return out


def fig_jacobian_debrief():
    """DEBRIEF for item 2: the cascade's matrix, filled, with its zeros ringed.

    The four claims that follow from it live in `rows()` on the slide, not in
    this figure: at the sizes `posb_slide_legibility` requires for content, a
    text column set inside a figure cannot be read from row 8. The matrix is
    the part that has to be drawn.
    """
    names = ["x", "y", "z"]
    entries = {(0, 0): MINUS, (0, 1): "0", (0, 2): "0",
               (1, 0): "+", (1, 1): MINUS, (1, 2): "0",
               (2, 0): "0", (2, 1): MINUS, (2, 2): MINUS}

    fig, axm = plt.subplots(figsize=(6.6, 5.0))
    _matrix_panel(axm, names, entries, hi={(0, 1), (0, 2), (1, 2), (2, 0)})
    axm.add_patch(plt.Polygon([[1, 3], [3, 3], [1, 1]], closed=True,
                              facecolor=RED, alpha=0.10, zorder=0))
    axm.set_ylim(-1.15, 3.70)
    axm.text(1.5, -0.78, "every entry ABOVE the diagonal is zero\n"
                         "\u2014 and one below it is too",
             ha="center", va="center", fontsize=16, color=RED)
    axm.set_title("the cascade: nine entries, four of them zero",
                  fontsize=17, color=INK, pad=12)
    return _save(fig, "s14_jacobian_debrief")


# ---------------------------------------------------------------------------
# The time-course segment, back on a real gene
# ---------------------------------------------------------------------------
#
# Adam, 11 October 2026: "I mean a trace of what? What curve? What is the
# point? We are being too abstract." He is right, and the abstraction was mine:
# the first version of this panel compared an unregulated gene with a
# negatively autoregulated one at a matched final level, which is the exam's
# A3.2 and A4 in a picture, and the fix I reached for was to strip the biology
# out rather than change the vehicle. A decaying exponential with no gene
# attached teaches nobody to draw a trace.
#
# So: a real protein, a real promoter, a real degradation rate, with the three
# features named ON the curve -- and the thing that moves is the DEGRADATION
# TAG, which is a lab intervention rather than an exam set-up.

CURVE_B, CURVE_G = 12.0, 0.35      # nM/min and 1/min: a protein, not a shape


def _curve(t, b=CURVE_B, g=CURVE_G, x0=0.0):
    return b / g + (x0 - b / g) * np.exp(-g * t)


def fig_curve_anatomy():
    """FRAME + WORKED for motion 3: what a trace is made of, on a real protein.

    beta = 12 nM/min, gamma = 0.35 /min: the steady level is 34 nM and the
    half-life is about two minutes, so every number on the axes is one a
    student could have measured.
    """
    g = CURVE_G
    ss = CURVE_B / g
    thalf = np.log(2) / g
    t = np.linspace(0, 5 / g, 800)
    y = _curve(t)

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(t, y, color=TEAL, lw=3.2, zorder=4)
    ax.axhline(ss, color=MUTED, ls=":", lw=1.6)

    # 1. where it starts
    ax.plot([0], [0], "o", ms=11, color=RED, zorder=6)
    ax.annotate("STARTS at zero\nno protein yet", xy=(0, 0),
                xytext=(1.9, 5.5), fontsize=12.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.7))
    # 2. how fast it leaves: the initial tangent, which IS beta
    tl = np.linspace(0, 1.25 / g * 0.55, 50)
    ax.plot(tl, CURVE_B * tl, color=RED, lw=2.2, ls="--", zorder=5)
    ax.annotate(f"LEAVES at $\\beta = {CURVE_B:g}$ nM/min\n"
                "the promoter's full rate,\nbefore anything accumulates",
                xy=(1.4, CURVE_B * 1.4), xytext=(3.6, 15.5), fontsize=12.5,
                color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.7))
    # 3. where it ends
    ax.annotate(f"ENDS at $\\beta/\\gamma = {ss:.0f}$ nM\n"
                "production balances removal",
                xy=(11.5, ss), xytext=(6.6, 25.0), fontsize=12.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.7))
    # the clock
    ax.plot([thalf, thalf], [0, ss / 2], color=MUTED, lw=1.4, ls=":")
    ax.plot([0, thalf], [ss / 2, ss / 2], color=MUTED, lw=1.4, ls=":")
    ax.plot([thalf], [ss / 2], "o", ms=8, color=MUTED, zorder=6)
    ax.text(thalf + 0.25, ss / 2 - 3.2,
            f"half-way at $\\ln 2/\\gamma$ = {thalf:.1f} min",
            fontsize=11.5, color=MUTED)

    assert abs(y[-1] - ss) < 0.3 and abs(_curve(thalf) - ss / 2) < 1e-9
    ax.set_xlim(0, 5 / g); ax.set_ylim(0, ss * 1.22)
    ax.set_xlabel("time  (minutes)")
    ax.set_ylabel("protein  (nM)")
    ax.set_title(rf"$\beta={CURVE_B:g}$ nM/min,   "
                 rf"$\gamma={g:g}$ min$^{{-1}}$", fontsize=14.5, color=INK)
    return _save(fig, "s14_curve_anatomy")


def fig_curve_moves():
    """WORKED, second surface: what each knob actually moves, and what it drags.

    TWO THINGS WENT WRONG IN THE FIRST VERSION OF THIS PANEL, both caught by
    the assertion at the bottom rather than by reading it.

    1. It claimed the three features "move independently" and drew a panel
       that started the protein part-made with beta and gamma unchanged. That
       moves the START and the DEPARTURE RATE together, because the rate is
       beta - gamma*x and therefore depends on where you are. The honest
       lesson is the one the measurement gives: beta drags the departure rate
       and the destination together; where you start drags the departure rate
       too, and leaves the destination alone. Nothing here moves one feature
       and nothing else, and that is worth saying out loud.

    2. The obvious third panel -- add a degradation tag, raise gamma -- is
       the midterm's A3 verbatim, and restoring the level afterwards is A3.2.
       So gamma is not touched anywhere in this session; `check_s14_firewall`
       now refuses it.
    """
    g, b = CURVE_G, CURVE_B
    t = np.linspace(0, 5 / g, 800)
    base = _curve(t)
    ss = b / g

    panels = [
        ("a stronger promoter", _curve(t, b=b * 1.7),
         "$\\beta$ up 1.7x", "DEPARTURE RATE and END",
         "both, together — they are $\\beta$ and $\\beta/\\gamma$"),
        ("a weaker promoter", _curve(t, b=b * 0.55),
         "$\\beta$ down to 0.55x", "DEPARTURE RATE and END",
         "the same pair, the other way"),
        ("start it part-made", _curve(t, x0=ss * 0.45),
         "15 nM already in the cell", "START and DEPARTURE RATE",
         "it leaves slower: removal is already running"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.4), sharey=True)
    for ax, (lab, curve, how, moved, why) in zip(axes, panels):
        ax.plot(t, base, color=MUTED, lw=2.0, ls=":",
                label="the protein above")
        ax.plot(t, curve, color=AMBER, lw=3.0, label="after the change")
        ax.axhline(ss, color=MUTED, ls=":", lw=1.1)
        ax.set_title(f"{lab}\n{how}", fontsize=16, color=INK)
        ax.text(0.5, -0.40, f"moves: {moved}", transform=ax.transAxes,
                ha="center", fontsize=16, color=AMBER, fontweight="bold")
        ax.text(0.5, -0.53, why, transform=ax.transAxes, ha="center",
                fontsize=13.5, color=MUTED)
        ax.set_xlabel("time  (min)")

    # Measure all three features off the drawn arrays and check each panel
    # moves exactly the pair it advertises -- nothing more, nothing less.
    def feats(c):
        return c[0], (c[1] - c[0]) / (t[1] - t[0]), c[-1]
    s0 = feats(base)
    NAMES = ["START", "DEPARTURE RATE", "END"]
    for lab, curve, _how, moved, _why in panels:
        f1 = feats(curve)
        claimed = {NAMES.index(w.strip()) for w in moved.split(" and ")}
        for i in range(3):
            moved_i = abs(f1[i] - s0[i]) > max(0.35, 0.02 * abs(s0[i]))
            assert moved_i == (i in claimed), (lab, NAMES[i], s0[i], f1[i])

    axes[0].set_ylabel("protein  (nM)")
    axes[0].legend(loc="lower right", fontsize=11, framealpha=0.95)
    # No suptitle: the slide carries this sentence as its title, and
    # printing it twice costs the height the panel needs.
    fig.subplots_adjust(bottom=0.40, top=0.88)
    return _save(fig, "s14_curve_moves", tight=False)


def fig_curve_debrief():
    """DEBRIEF for item 3: the two curves, with what actually changed marked.

    Same promoter, same removal rate, negative autoregulation added. The two
    leave at the SAME initial slope -- there is no repressor at t = 0 -- and
    the regulated one settles lower and reaches its own half-way point sooner.
    Both claims are computed here, not drawn by hand.
    """
    b, g, K, nH = CURVE_B, CURVE_G, 14.0, 2.0
    t = np.linspace(0, 5 / g, 1200)
    un = _curve(t)
    nar = solve_ivp(lambda tt, s: [b / (1 + (s[0] / K) ** nH) - g * s[0]],
                    [0, t[-1]], [0.0], t_eval=t, rtol=1e-11, atol=1e-13).y[0]
    ss_un = b / g
    ss_nar = brentq(lambda x: b / (1 + (x / K) ** nH) - g * x, 1e-9, ss_un)
    th_un = np.log(2) / g
    th_nar = t[int(np.argmax(nar >= ss_nar / 2))]

    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    ax.plot(t, un, color=TEAL, lw=3.2, label="unregulated")
    ax.plot(t, nar, color=AMBER, lw=3.2, ls="--",
            label="negative autoregulation added")
    for lvl, col in ((ss_un, TEAL), (ss_nar, AMBER)):
        ax.axhline(lvl, color=col, ls=":", lw=1.5)
    tl = np.linspace(0, 1.1, 40)
    ax.plot(tl, b * tl, color=RED, lw=2.2, ls="--", zorder=6)
    ax.annotate("SAME initial slope — at $t=0$ there is\n"
                "no repressor yet, so both leave at $\\beta$",
                xy=(0.55, b * 0.55), xytext=(1.6, 27.0), fontsize=12.5,
                color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.7))
    # A vertical span between the two levels, not a stray horizontal arrow
    # into white space: the quantity being named is the GAP.
    ax.annotate("", xy=(13.4, ss_un), xytext=(13.4, ss_nar),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.2,
                                mutation_scale=13))
    ax.text(13.1, (ss_un + ss_nar) / 2,
            f"the END moved\n{ss_un:.0f} → {ss_nar:.1f} nM",
            fontsize=12, color=RED, ha="right", va="center")
    for th, lvl, col in ((th_un, ss_un, TEAL), (th_nar, ss_nar, AMBER)):
        ax.plot([th, th], [0, lvl / 2], color=col, lw=1.4, ls=":")
        ax.plot([th], [lvl / 2], "o", ms=8, color=col, zorder=7)
    ax.annotate(f"each curve's OWN half-way time:\n"
                f"{th_nar:.1f} min and {th_un:.1f} min",
                xy=(th_un, ss_un / 2), xytext=(3.6, 8.0), fontsize=12,
                color=MUTED,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5))

    assert abs((un[1] - un[0]) - (nar[1] - nar[0])) < 1e-3
    assert ss_nar < ss_un and th_nar < th_un

    ax.set_xlim(0, 5 / g); ax.set_ylim(0, ss_un * 1.24)
    ax.set_xlabel("time  (minutes)")
    ax.set_ylabel("protein  (nM)")
    ax.set_title("Same promoter, same removal rate — feedback added",
                 fontsize=14.5, color=INK)
    ax.legend(loc="lower right", framealpha=0.95, fontsize=12)
    return _save(fig, "s14_curve_debrief")



def fig_ffl_frame():
    """FRAME for the feedforward segment: the two circuits, and the question.

    The first build opened this segment on a step of algebra. What the room
    needs first is the object -- two circuits that take the SAME input and
    differ by one wire -- and the question in the shape it will be asked:
    when the input switches, which end of the output's trace moves?

    Drawn by hand rather than with `_draw_edges`, because the gate is not a
    node: both arms run INTO it and one short arm runs out of it to Z. The
    edge list still goes through the leak guard.
    """
    def panel(ax, title, shortcut, note):
        _assert_not_exam_circuit(
            [("X", "Y", False), ("Y", "Z", False)] +
            ([("X", "Z", False)] if shortcut else []), title)
        ax.set_xlim(-1.40, 1.40); ax.set_ylim(-0.55, 2.75)
        ax.axis("off"); ax.set_aspect("equal")
        # Spaced so that BOTH arms into the gate and the one out of it are
        # visible arms rather than bare arrowheads: with Y at 1.0 and the gate
        # at 0.42 the two gaps came out at 0.03 and 0.02 inches.
        pos = {"X": (0.0, 2.2), "Y": (0.0, 1.2), "Z": (0.0, 0.0)}
        R, GY, GR = 0.20, 0.60, 0.135      # node r, gate centre y, gate r

        def arm(p, q, pad_a, pad_b, **kw):
            p, q = np.array(p, float), np.array(q, float)
            u = (q - p) / np.linalg.norm(q - p)
            ax.annotate("", xy=q - u * pad_b, xytext=p + u * pad_a,
                        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=MUTED,
                                        mutation_scale=17, shrinkA=0,
                                        shrinkB=0), **kw)

        arm(pos["X"], pos["Y"], R + 0.03, R + 0.03)
        if shortcut:
            arm(pos["Y"], (0.0, GY), R + 0.03, GR + 0.03)
            arm((0.0, GY), pos["Z"], GR + 0.03, R + 0.03)
            # the direct arm, bowed clear of the chain and into the gate
            ax.annotate("", xy=(GR + 0.02, GY + 0.05), xytext=(R, 2.12),
                        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=MUTED,
                                        mutation_scale=17,
                                        connectionstyle="arc3,rad=-0.48"))
            ax.text(1.08, 1.45, "the shortcut", fontsize=12.5, color=MUTED,
                    ha="center")
            ax.add_patch(plt.Circle((0.0, GY), GR, facecolor="white",
                                    edgecolor=TEAL, lw=2.6, zorder=5))
            ax.text(0.0, GY, "OR", ha="center", va="center", fontsize=11,
                    fontweight="bold", color=TEAL, zorder=6)
        else:
            arm(pos["Y"], pos["Z"], R + 0.03, R + 0.03)

        for name, (x, y) in pos.items():
            ax.add_patch(plt.Circle((x, y), R, facecolor="white",
                                    edgecolor=RULE, lw=3.2, zorder=7))
            ax.text(x, y, name, ha="center", va="center", fontsize=19,
                    fontweight="bold", color=MUTED, zorder=8)
        ax.set_title(title, fontsize=14, color=INK, pad=10)
        ax.text(0.5, -0.05, note, transform=ax.transAxes, ha="center",
                fontsize=12, color=MUTED)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.2))
    panel(axes[0], "Loop P — a cascade", False,
          "X reaches Z only THROUGH Y")
    panel(axes[1], "Loop Q — a shortcut, with an OR gate", True,
          "X reaches Z two ways: through Y, and directly")
    # No suptitle: the slide carries this sentence as its title, and
    # printing it twice costs the height the panel needs.
    fig.text(0.5, 0.045,
             "Y is the SLOW one and sets the clock.  Z follows its own "
             "promoter quickly.",
             ha="center", fontsize=12.5, color=INK)
    fig.subplots_adjust(top=0.90, bottom=0.13)
    return _save(fig, "s14_ffl_frame", tight=False)


def fig_ffl_debrief():
    """DEBRIEF for item 5: the two released traces, with the delays measured.

    THE REASONING TABLE IS NOT IN THIS FIGURE. It was, and that was wrong:
    `posb_slide_legibility` puts the floor for anything carrying content at
    20pt, and text set at 11-12pt inside a figure that renders roughly 1:1 on
    a 13.33in slide lands at about 11pt on the wall. A four-row decision table
    is content, so it belongs in `rows()` on the slide, where it inherits the
    scale from `TYPE`. The figure keeps what only a figure can do: the curves,
    measured.

    NO AND-GATED TRACE IS DRAWN. The midterm's B2.1 asks the student to sketch
    the output of two AND-gated loops, so printing that curve two days before
    hands over the answer. The slide's table gives the reasoning instead.
    """
    t, out, (on_c, off_c, on_o, off_o) = _ffl_traces()

    fig, axes = plt.subplots(2, 1, figsize=(7.4, 5.2), sharex=True)
    for ax, key, lab, (don, doff), col in (
            (axes[0], "cascade", "Loop P \u2014 cascade", (on_c, off_c), MUTED),
            (axes[1], "c1or", "Loop Q \u2014 shortcut + OR", (on_o, off_o), TEAL)):
        ax.plot([-1, X_ON, X_ON, X_OFF, X_OFF, 20],
                [0, 0, 1.06, 1.06, 0, 0], color=AMBER, lw=2.2, ls="--")
        ax.plot(t, out[key], color=col, lw=3.4, zorder=4)
        for x0, dd, tag in ((X_ON, don, "ON"), (X_OFF, doff, "OFF")):
            ax.annotate("", xy=(x0 + dd, 0.52), xytext=(x0, 0.52),
                        arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.2,
                                        mutation_scale=12))
            ax.text(x0 + dd + 0.45, 0.52, f"{tag}  {dd:.1f}", color=RED,
                    fontsize=16, ha="left", va="center")
        ax.set_xlim(0, 20); ax.set_ylim(0, 1.16)
        ax.set_yticks([])
        ax.set_ylabel("Z", rotation=0, labelpad=14, fontsize=16)
        ax.set_title(lab, fontsize=16, loc="left", color=INK)
        ax.grid(True, axis="x", color=RULE, lw=0.8, alpha=0.6)
    axes[1].set_xlabel("time  (Y lifetimes)", fontsize=15)
    axes[1].tick_params(labelsize=14)

    assert on_o < on_c and off_o > on_o
    fig.tight_layout()
    return _save(fig, "s14_ffl_debrief", tight=False)


def fig_margins_frame():
    """FRAME for the noise-margin segment: why a margin exists at all.

    The segment opened on the construction. What it needs first is the thing
    the construction is FOR: one gate drives the next, the first one's output
    is the second one's input, and real signals arrive dirty. A margin is the
    amount of dirt the next stage can absorb before it stops being digital.
    """
    fig = plt.figure(figsize=(12.4, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.25], wspace=0.22)
    axl = fig.add_subplot(gs[0, 0])
    axr = fig.add_subplot(gs[0, 1])

    # Left: two gates in series, with the join called out.
    axl.set_xlim(0, 10); axl.set_ylim(0, 6); axl.axis("off")
    for x0, lab in ((1.0, "gate 1"), (5.6, "gate 2")):
        axl.add_patch(plt.Rectangle((x0, 2.4), 2.4, 1.6, facecolor="white",
                                    edgecolor=INK, lw=2.4))
        axl.text(x0 + 1.2, 3.2, lab, ha="center", va="center", fontsize=13,
                 color=INK, fontweight="bold")
    for x0, x1 in ((0.0, 1.0), (3.4, 5.6), (8.0, 9.4)):
        axl.annotate("", xy=(x1, 3.2), xytext=(x0, 3.2),
                     arrowprops=dict(arrowstyle="-|>", lw=2.2, color=MUTED,
                                     mutation_scale=18))
    axl.annotate("gate 1's OUTPUT\nis gate 2's INPUT", xy=(4.5, 3.2),
                 xytext=(4.5, 0.75), ha="center", fontsize=12.5, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    axl.text(5.0, 5.3, "the whole question lives at this join",
             ha="center", fontsize=13, color=INK)

    # Right: a clean level, a dirty level, and the band that is still safe.
    # Room to the right of the trace for the band labels: set over the
    # data they sat on top of the noise they are describing.
    axr.set_xlim(0, 13.2); axr.set_ylim(0, 1.0)
    for lo, hi, col, lab in ((0.00, 0.22, AMBER, "read as LOW"),
                             (0.78, 1.00, TEAL, "read as HIGH")):
        axr.axhspan(lo, hi, color=col, alpha=0.16)
        axr.text(13.0, (lo + hi) / 2, lab, ha="right", va="center",
                 fontsize=12, color=col, fontweight="bold")
    axr.axhspan(0.22, 0.78, color=RED, alpha=0.07)
    axr.text(13.0, 0.50, "no man's land", ha="right", va="center",
             fontsize=12, color=RED, style="italic")

    rng = np.random.default_rng(7)
    tt = np.linspace(0, 10, 900)
    clean = np.where(tt < 5, 0.93, 0.07)
    dirty = clean + rng.normal(0, 0.055, tt.size)
    axr.plot(tt, dirty, color=MUTED, lw=1.2, alpha=0.9)
    axr.plot(tt, clean, color=INK, lw=2.6)
    axr.annotate("how much dirt can this\nabsorb and still be read right?",
                 xy=(2.3, dirty[200]), xytext=(2.6, 0.42), fontsize=12.5,
                 color=RED, ha="center",
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.7))
    axr.set_yticks([0, 1]); axr.set_yticklabels(["0", "1"])
    axr.set_xticks([])
    axr.set_xlabel("time")
    axr.set_ylabel("level")
    axr.set_title("a real signal arrives with noise on it", fontsize=13,
                  color=INK)

    # No suptitle: the slide carries this sentence as its title, and
    # printing it twice costs the height the panel needs.
    fig.subplots_adjust(top=0.90)
    return _save(fig, "s14_margins_frame", tight=False)


def fig_cascade_release():
    """The object for item 2, ON THE SLIDE, with the method they will need.

    Adam, 11 October: "we should SHOW them the three gene cascade. We might
    want to remind them how to calculate eigenvalues of the matrix." The
    release surface described the circuit in a sentence and left the room to
    reconstruct it from the sheet -- the same frame-less failure as
    everywhere else, in miniature.

    The reminder is the GENERAL method, det(J - lambda I) = 0, deliberately.
    The triangular shortcut is what the item's "why does that step follow"
    asks them to find, so putting it here would answer the question.
    """
    fig = plt.figure(figsize=(12.4, 4.0))
    gs = fig.add_gridspec(1, 3, width_ratios=[0.85, 1.25, 1.10], wspace=0.08)
    axc, axe, axr = (fig.add_subplot(g) for g in gs)

    # --- the wiring ---
    pos = {"X": (0.0, 2.0), "Y": (0.0, 1.0), "Z": (0.0, 0.0)}
    edges = [("X", "Y", False), ("Y", "Z", True)]
    _assert_not_exam_circuit(edges, "cascade release")
    axc.set_xlim(-1.0, 1.0); axc.set_ylim(-0.75, 2.85)
    axc.axis("off"); axc.set_aspect("equal")
    R = 0.21
    for (a, b, rep) in edges:
        p, q = np.array(pos[a], float), np.array(pos[b], float)
        u = (q - p) / np.linalg.norm(q - p)
        p2 = p + u * (R + 0.04)
        q2 = q - u * (R + (0.10 if rep else 0.04))
        axc.annotate("", xy=q2, xytext=p2,
                     arrowprops=dict(arrowstyle="-" if rep else "-|>", lw=2.4,
                                     color=MUTED, mutation_scale=17,
                                     shrinkA=0, shrinkB=0))
        if rep:
            axc.annotate("", xy=q2, xytext=q2 - u * 0.02,
                         arrowprops=dict(arrowstyle="|-|,widthA=0,widthB=7",
                                         lw=3.4, color=MUTED,
                                         mutation_scale=1, shrinkA=0,
                                         shrinkB=0))
    for name, (x, y) in pos.items():
        axc.add_patch(plt.Circle((x, y), R, facecolor="white",
                                 edgecolor=RULE, lw=3.2, zorder=4))
        axc.text(x, y, name, ha="center", va="center", fontsize=21,
                 fontweight="bold", color=MUTED, zorder=5)
    axc.text(0.0, 2.52, "X is made at a\nconstant rate", ha="center",
             fontsize=13, color=MUTED)
    axc.text(0.0, -0.44, "nothing feeds back", ha="center", fontsize=13,
             color=RED)

    # --- the equations ---
    axe.axis("off")
    axe.text(0.5, 0.80,
             r"$\dot{x} \;=\; \beta_x \;-\; x$" "\n\n"
             r"$\dot{y} \;=\; \dfrac{\beta\,x^{\,n}}{1+x^{\,n}} \;-\; y$" "\n\n"
             r"$\dot{z} \;=\; \dfrac{\alpha}{1+y^{\,n}} \;-\; z$",
             transform=axe.transAxes, ha="center", va="center", fontsize=19,
             color=INK, linespacing=1.5)
    axe.text(0.5, 0.06, "fill in the NINE signs", transform=axe.transAxes,
             ha="center", fontsize=15, color=INK, fontweight="bold")

    # --- the reminder ---
    axr.axis("off")
    axr.text(0.0, 0.93, "and if you had to COMPUTE them",
             transform=axr.transAxes, fontsize=15, color=INK,
             fontweight="bold", va="top")
    axr.text(0.0, 0.62, r"$\det\left(J - \lambda I\right) \;=\; 0$",
             transform=axr.transAxes, fontsize=22, color=TEAL, va="center")
    axr.text(0.0, 0.36,
             "subtract $\\lambda$ down the diagonal,\n"
             "take the determinant, solve for $\\lambda$.",
             transform=axr.transAxes, fontsize=13.5, color=MUTED, va="center")
    axr.text(0.0, 0.07,
             "You are NOT asked to. Look at the pattern\n"
             "of entries first — it may answer you for free.",
             transform=axr.transAxes, fontsize=13.5, color=RED, va="center")
    return _save(fig, "s14_cascade_release", tight=False)


def _gene_cartoon(ax, beta, gamma):
    """A promoter, a gene, a protein and a sink — the thing being simulated.

    Adam, 11 October, on the time-course frame: "draw a cartoon of the system
    being 'simulated'." A trace with axes and no apparatus is a shape; the
    same trace beside the gene it came off is a measurement.

    Both rate arrows LAND on something: beta runs from the gene to the
    protein it makes, gamma from the protein to the sink it leaves by. An
    arrow into empty space is decoration.
    """
    ax.set_xlim(0, 10.6); ax.set_ylim(0, 4.4); ax.axis("off")

    # --- the DNA, with a promoter and a coding sequence on it ---
    for yy in (1.52, 1.34):
        ax.plot([0.3, 7.4], [yy, yy], color=MUTED, lw=1.6, zorder=1)
    ax.add_patch(plt.Rectangle((0.9, 1.20), 1.5, 0.46, facecolor=AMBER,
                               edgecolor="none", alpha=0.9, zorder=2))
    ax.text(1.65, 1.43, "promoter", ha="center", va="center", fontsize=11.5,
            color="white", fontweight="bold", zorder=3)
    ax.add_patch(plt.Rectangle((2.5, 1.20), 2.5, 0.46, facecolor=TEAL,
                               edgecolor="none", alpha=0.92, zorder=2))
    ax.text(3.75, 1.43, "gene", ha="center", va="center", fontsize=12.5,
            color="white", fontweight="bold", zorder=3)

    # --- beta: from the gene to the protein it makes ---
    ax.annotate("", xy=(5.55, 3.05), xytext=(3.95, 1.80),
                arrowprops=dict(arrowstyle="-|>", lw=2.8, color=TEAL,
                                mutation_scale=19,
                                connectionstyle="arc3,rad=0.22"))
    ax.text(3.95, 2.74, rf"$\beta = {beta:g}$ nM/min", fontsize=14.5,
            color=TEAL, va="center", ha="right")
    ax.text(3.95, 2.38, "transcribed, translated", fontsize=11.5,
            color=MUTED, va="center", ha="right")

    # --- the protein ---
    for dx, dy in ((0.0, 0.0), (0.44, 0.24), (0.24, -0.32)):
        ax.add_patch(plt.Circle((6.15 + dx, 3.32 + dy), 0.27, facecolor=TEAL,
                                edgecolor="white", lw=1.6, alpha=0.93,
                                zorder=4))
    ax.text(6.35, 4.06, "protein", fontsize=14.5, color=INK, ha="center")

    # --- gamma: from the protein to where it goes ---
    ax.annotate("", xy=(8.95, 2.08), xytext=(7.15, 3.10),
                arrowprops=dict(arrowstyle="-|>", lw=2.8, color=AMBER,
                                mutation_scale=19,
                                connectionstyle="arc3,rad=-0.22"))
    ax.text(8.30, 3.15, rf"$\gamma = {gamma:g}$ min$^{{-1}}$", fontsize=14.5,
            color=AMBER, va="center", ha="left")
    for i, (dx, al) in enumerate(((0.0, 0.42), (0.40, 0.24), (0.76, 0.12))):
        ax.add_patch(plt.Circle((9.25 + dx, 1.86 - i * 0.12), 0.20,
                                facecolor=AMBER, edgecolor="none", alpha=al,
                                zorder=4))
    ax.text(9.70, 1.28, "diluted away,\nand degraded", fontsize=11.5,
            color=MUTED, ha="center", va="top")

    # --- the one equation the whole trace comes from ---
    ax.text(0.3, 0.42, r"$\dot{x} \;=\; \beta \;-\; \gamma x$",
            fontsize=20, color=INK, va="center")
    ax.text(3.1, 0.42, "made at a constant rate, removed in proportion to "
                       "how much is there",
            fontsize=12.5, color=MUTED, va="center")


def fig_curve_system():
    """FRAME, first surface of motion 3: what is actually being simulated."""
    fig, ax = plt.subplots(figsize=(9.4, 3.9))
    _gene_cartoon(ax, CURVE_B, CURVE_G)
    return _save(fig, "s14_curve_system")


FIGURES = [
    # motion 1 — loops
    fig_loop_outcomes, fig_round_trip, fig_even_latch, fig_loop_debrief,
    # basins
    fig_basin_stages, fig_basins, fig_basin_trajectories,
    fig_autoactivator, fig_autoactivator_debrief,
    # Jacobian signs
    fig_jacobian_stages, fig_jacobian_signs, fig_cascade_release,
    fig_jacobian_debrief,
    # time courses
    fig_curve_system, fig_curve_anatomy, fig_curve_moves,
    fig_curve_debrief,
    # noise margins
    fig_margins_frame, fig_margins_steps,
    # feedforward
    fig_ffl_frame, fig_ffl_axes, fig_ffl_worked, fig_ffl_debrief,
]


if __name__ == "__main__":
    for fn in FIGURES:
        print(" ", fn())
