"""Session 12 figures — counts, the master equation, and what feedback buys.

Everything here comes from `posb.stochastic`: `gillespie`, `time_average`,
`birth_death`, `two_stage` and `negative_autoregulation` are the functions the
students call after they have written their own SSA, so the plot on the slide is
the plot in the notebook. Every simulation is seeded.

The session's results, derived in class and checked here:

    birth-death:          stationary Poisson, Fano = 1, eta^2 = 1/<n>
    bursting (two-stage): Fano = 1 + k_p/(gamma_m + gamma_p)  ~  1 + b
    negative autoregulation, at matched mean:
                          Fano = 1/(1 + g),  g = n u^n/(1 + u^n)  -- session 11's g

Run:  python tools/build_figures.py s12
"""
import numpy as np

from figures.style import use, TEAL, CYAN, AMBER, MUTED, INK, RED, RULE
from posb.stochastic import (gillespie, time_average, fano, birth_death,
                             two_stage, negative_autoregulation,
                             two_stage_fano, nar_fano_lna)

plt = use()
OUT = "figures/build"


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def _occupancy(t, x, t_max, t_burn, bins):
    """Fraction of TIME spent at each count -- the stationary distribution."""
    ends = np.append(t[1:], t_max)
    dt = np.clip(ends, t_burn, None) - np.clip(t, t_burn, None)
    h = np.zeros(len(bins))
    for xi, w in zip(x, dt):
        if 0 <= xi < len(bins):
            h[int(xi)] += w
    return h / h.sum()


def _poisson(mu, ns):
    from math import lgamma
    return np.array([np.exp(n * np.log(mu) - mu - lgamma(n + 1)) for n in ns])


# ---------------------------------------------------------------------------
# 1. The anatomy of one run: when, and which
# ---------------------------------------------------------------------------
def fig_ssa_anatomy():
    """Twelve events of birth-death, every waiting time and every choice shown."""
    stoich, a = birth_death(k=10.0, gamma=1.0)
    t, X = gillespie(stoich, a, [8], t_max=1.4, rng=3)
    t, x = t[:13], X[:13, 0]
    fig, ax = plt.subplots(figsize=(10.8, 4.2))
    ax.step(t, x, where="post", color=INK, lw=2.4)
    for i in range(1, len(t)):
        up = x[i] > x[i - 1]
        ax.plot(t[i], x[i], "o", ms=9, color=TEAL if up else AMBER, zorder=5)
    # mark two waiting times
    for i in (3, 8):
        ax.annotate("", xy=(t[i + 1], x[i] - 0.55), xytext=(t[i], x[i] - 0.55),
                    arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
        ax.text(0.5 * (t[i] + t[i + 1]), x[i] - 1.25, r"$\tau$", color=RED,
                ha="center", fontsize=16)
    ax.plot([], [], "o", color=TEAL, label="a birth  (rate k)")
    ax.plot([], [], "o", color=AMBER, label=r"a death  (rate $\gamma n$)")
    ax.legend(loc="upper left", ncol=2)
    ax.set_xlim(t[0], t[-1] + 0.02)
    ax.set_ylim(min(x) - 2.2, max(x) + 2.6)
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("molecules  n")
    ax.set_title("each step: draw WHEN the next event happens, then WHICH one")
    _save(fig, "s12_ssa_anatomy")

    # the same twelve events, sized for the 5.4in column of a split surface
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    ax.step(t, x, where="post", color=INK, lw=2.4)
    for i in range(1, len(t)):
        up = x[i] > x[i - 1]
        ax.plot(t[i], x[i], "o", ms=9, color=TEAL if up else AMBER, zorder=5)
    for i in (3, 8):
        ax.annotate("", xy=(t[i + 1], x[i] - 0.55), xytext=(t[i], x[i] - 0.55),
                    arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
        ax.text(0.5 * (t[i] + t[i + 1]), x[i] - 1.35, r"$\tau$", color=RED,
                ha="center", fontsize=16)
    ax.plot([], [], "o", color=TEAL, label="birth")
    ax.plot([], [], "o", color=AMBER, label="death")
    ax.legend(loc="upper right")
    ax.set_xlim(t[0], t[-1] + 0.02)
    ax.set_ylim(min(x) - 2.2, max(x) + 2.6)
    ax.set_xlabel("time  (lifetimes)")
    ax.set_ylabel("molecules  n")
    ax.set_title("twelve events, k = 10, γ = 1")
    _save(fig, "s12_ssa_anatomy_col")


# ---------------------------------------------------------------------------
# 2. Birth-death: a count that wanders, and the Poisson it wanders over
# ---------------------------------------------------------------------------
def fig_birth_death():
    """Birth-death by Gillespie: one trajectory, and its Poisson."""
    k, gamma, T = 10.0, 1.0, 4000.0
    stoich, a = birth_death(k, gamma)
    t, X = gillespie(stoich, a, [0], t_max=T, rng=11)
    x = X[:, 0]
    m, v = time_average(t, X, T, t_burn=10.0)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3),
                             gridspec_kw={"width_ratios": [1.7, 1]})
    ax = axes[0]
    keep = t <= 30.0
    ax.step(t[keep], x[keep], where="post", color=TEAL, lw=1.8)
    ax.axhline(k / gamma, color=RED, lw=1.6, ls="--")
    ax.text(30.3, k / gamma, r"$k/\gamma$", color=RED, va="center", fontsize=15)
    ax.set_xlim(0, 30)
    ax.set_xlabel("time  (protein lifetimes)")
    ax.set_ylabel("molecules  n")
    ax.set_title("one cell, one gene, no regulation")
    ax = axes[1]
    ns = np.arange(0, 26)
    occ = _occupancy(t, x, T, 10.0, ns)
    ax.bar(ns, occ, color=CYAN, width=0.85, label="time spent at n")
    ax.plot(ns, _poisson(k / gamma, ns), "o-", color=INK, ms=6, lw=1.6,
            label="Poisson, mean 10")
    ax.set_xlabel("n")
    ax.set_ylabel("fraction of time")
    ax.set_title(f"mean {m[0]:.2f}, variance {v[0]:.2f}")
    ax.set_ylim(0, 0.18)
    ax.legend(loc="upper right", fontsize=12)
    _save(fig, "s12_birth_death")
    return m[0], v[0]


# ---------------------------------------------------------------------------
# 3. Bursting: same mean, two RBSs
# ---------------------------------------------------------------------------
BURST = [  # (label, k_m, gamma_m, k_p, gamma_p) -- both mean 50
    ("strong promoter, weak RBS", 50.0, 10.0, 10.0, 1.0),     # b = 1
    ("weak promoter, strong RBS", 5.0, 10.0, 100.0, 1.0),     # b = 10
]


def fig_bursting():
    """Same mean of 50, b = 1 against b = 10: Fano 1.9 against 10.1."""
    T = 3000.0
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3),
                             gridspec_kw={"width_ratios": [1.7, 1]})
    out = []
    for (lab, km, gm, kp, gp), c, seed in zip(BURST, (TEAL, AMBER), (5, 6)):
        stoich, a = two_stage(km, gm, kp, gp)
        t, X = gillespie(stoich, a, [0, 50], t_max=T, rng=seed)
        m, v = time_average(t, X, T, t_burn=20.0)
        F = fano(m, v)[1]
        Fx = two_stage_fano(kp, gm, gp)
        out.append((lab, m[1], F, Fx, kp / gm))
        keep = t <= 25.0
        axes[0].step(t[keep], X[keep, 1], where="post", color=c, lw=1.8,
                     label=f"b = {kp / gm:.0f}, {km:.0f} mRNA per lifetime")
        ns = np.arange(0, 181, 4)
        occ = _occupancy(t, X[:, 1], T, 20.0, np.arange(0, 400))
        coarse = np.add.reduceat(occ[:181], np.arange(0, 181, 4))
        axes[1].plot(ns + 2, coarse[:len(ns)], color=c, lw=2.6,
                     label=f"Fano {F:.1f}")
    axes[0].axhline(50, color=MUTED, lw=1.2, ls="--")
    axes[0].set_xlim(0, 25)
    axes[0].set_ylim(0, 165)
    axes[0].set_xlabel("time  (protein lifetimes)")
    axes[0].set_ylabel("proteins")
    axes[0].set_title("same mean, 50 proteins")
    axes[0].legend(loc="upper left", fontsize=15)
    axes[1].set_xlabel("proteins")
    axes[1].set_ylabel("fraction of time")
    axes[1].set_title("same mean, different spread")
    axes[1].legend(loc="upper right", fontsize=15)
    _save(fig, "s12_bursting")
    return out


# ---------------------------------------------------------------------------
# 4. T17: negative autoregulation against a constitutive gene, matched mean
# ---------------------------------------------------------------------------
def fig_nar_noise():
    """Same mean (100), two histograms; then Fano against g with SSA points."""
    T = 3000.0
    st_c, a_c = birth_death(100.0, 1.0)
    tc, Xc = gillespie(st_c, a_c, [100], t_max=T, rng=21)
    st_n, a_n = negative_autoregulation(beta=200.0, K=100.0, n=4, gamma=1.0)
    tn, Xn = gillespie(st_n, a_n, [100], t_max=T, rng=22)
    mc, vc = time_average(tc, Xc, T, 20.0)
    mn, vn = time_average(tn, Xn, T, 20.0)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4))
    ax = axes[0]
    bins = np.arange(0, 200)
    for t, X, c, lab, m, v in [(tc, Xc, MUTED, "constitutive", mc, vc),
                               (tn, Xn, TEAL, "self-repressing, n = 4", mn, vn)]:
        occ = _occupancy(t, X[:, 0], T, 20.0, bins)
        ax.plot(bins, occ, color=c, lw=2.8,
                label=f"{lab}:  mean {m[0]:.0f}, Fano {v[0] / m[0]:.2f}")
    ax.set_xlim(55, 145)
    ax.set_ylim(0, 0.098)
    ax.set_xlabel("molecules")
    ax.set_ylabel("fraction of time")
    ax.set_title("same mean, 100 molecules")
    ax.legend(loc="upper left", fontsize=11.5)

    ax = axes[1]
    gs = np.linspace(0, 4.2, 200)
    ax.plot(gs, 1 / (1 + gs), color=INK, lw=2.8, label=r"$1/(1+g)$")
    pts = []
    for n, seed in [(1, 31), (2, 32), (4, 33), (8, 34)]:
        st, a = negative_autoregulation(beta=200.0, K=100.0, n=n, gamma=1.0)
        t, X = gillespie(st, a, [100], t_max=T, rng=seed)
        m, v = time_average(t, X, T, 20.0)
        g = n * 0.5
        pts.append((n, g, v[0] / m[0], nar_fano_lna(n, 1.0)))
        ax.plot(g, v[0] / m[0], "o", ms=12, mfc="none", mec=RED, mew=2.4)
        ax.text(g + 0.08, v[0] / m[0] + 0.04, f"n = {n}", color=RED, fontsize=13)
    ax.plot([], [], "o", mfc="none", mec=RED, mew=2.4, label="Gillespie, x = K")
    ax.axhline(1.0, color=MUTED, lw=1.2, ls=":")
    ax.text(0.12, 1.03, "constitutive", color=MUTED, fontsize=13)
    ax.set_xlim(0, 4.3)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("loop gain  g = n uⁿ/(1+uⁿ)")
    ax.set_ylabel("Fano factor")
    ax.set_title("the same g as Thursday's ring")
    ax.legend(loc="center right", fontsize=12)
    _save(fig, "s12_nar_noise")
    return (mc[0], vc[0] / mc[0]), (mn[0], vn[0] / mn[0]), pts


# ---------------------------------------------------------------------------
# 5. Two colours in one cell -- our own Fig. 3A
# ---------------------------------------------------------------------------
def _two_color(mean, ext_cv, cells, rng):
    """Each cell draws its own rate (extrinsic); each copy is then an
    independent Poisson count at that rate (intrinsic). Exact stationary
    sampling, not an SSA: two birth-death genes sharing one k are independent
    Poisson draws given k."""
    sig = np.sqrt(np.log(1 + ext_cv ** 2))
    k = mean * rng.lognormal(-sig ** 2 / 2, sig, cells)
    return rng.poisson(k), rng.poisson(k)


def two_color_noise(c1, c2):
    """Swain, Elowitz & Siggia (PNAS 2002) estimators, as used by Elowitz 2002."""
    c1, c2 = np.asarray(c1, float), np.asarray(c2, float)
    m1, m2 = c1.mean(), c2.mean()
    eint2 = np.mean((c1 - c2) ** 2) / (2 * m1 * m2)
    eext2 = (np.mean(c1 * c2) - m1 * m2) / (m1 * m2)
    return np.sqrt(eint2), np.sqrt(max(eext2, 0.0)), np.sqrt(eint2 + eext2)


def fig_two_color():
    """Two copies per cell, simulated: a quiet strain and a noisy one."""
    rng = np.random.default_rng(41)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.6))
    out = []
    for ax, (mean, ext, title) in zip(axes, [(400, 0.05, "lots of transcript"),
                                             (25, 0.30, "repressed, and LacI varies")]):
        c1, c2 = _two_color(mean, ext, 1500, rng)
        ei, ee, et = two_color_noise(c1, c2)
        out.append((mean, ei, ee, et))
        lo, hi = 0, max(c1.max(), c2.max()) * 1.05
        ax.plot([lo, hi], [lo, hi], color=MUTED, lw=1.4, ls="--")
        ax.plot(c1, c2, "o", ms=3.2, color=TEAL, alpha=0.45)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_aspect("equal")
        ax.set_xlabel("copy 1  (CFP)")
        ax.set_ylabel("copy 2  (YFP)")
        ax.set_title(f"{title}: mean {mean}")
        ax.text(0.04, 0.95, f"$\\eta_{{int}}$ = {ei:.2f}\n$\\eta_{{ext}}$ = {ee:.2f}",
                transform=ax.transAxes, va="top", fontsize=19, color=INK)
    _save(fig, "s12_two_color")
    return out


# ---------------------------------------------------------------------------
# 6. Single panels for the two split-surface derivations (5.4in figure column)
# ---------------------------------------------------------------------------
def fig_derivation_panels():
    """Panels for Deck.derivation_fig: the wandering count, its distribution,
    and the NAR comparison as two separate pictures."""
    k, gamma, T = 10.0, 1.0, 4000.0
    stoich, a = birth_death(k, gamma)
    t, X = gillespie(stoich, a, [0], t_max=T, rng=11)
    x = X[:, 0]

    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    keep = t <= 20.0
    ax.step(t[keep], x[keep], where="post", color=TEAL, lw=1.8)
    ax.axhline(k / gamma, color=RED, lw=1.6, ls="--")
    ax.set_xlim(0, 20)
    ax.set_xlabel("time  (lifetimes)")
    ax.set_ylabel("molecules  n")
    ax.set_title("k = 10, γ = 1: one cell")
    _save(fig, "s12_bd_traj")

    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    ns = np.arange(0, 26)
    occ = _occupancy(t, x, T, 10.0, ns)
    ax.bar(ns, occ, color=CYAN, width=0.85, label="time at n, simulated")
    ax.plot(ns, _poisson(k / gamma, ns), "o-", color=INK, ms=6, lw=1.6,
            label="Poisson, mean 10")
    ax.set_ylim(0, 0.18)
    ax.set_xlabel("n")
    ax.set_ylabel("P(n)")
    ax.set_title("the ladder's answer")
    ax.legend(loc="upper right", fontsize=12)
    _save(fig, "s12_bd_hist")

    st_c, a_c = birth_death(100.0, 1.0)
    tc, Xc = gillespie(st_c, a_c, [100], t_max=3000.0, rng=21)
    st_n, a_n = negative_autoregulation(beta=200.0, K=100.0, n=4, gamma=1.0)
    tn, Xn = gillespie(st_n, a_n, [100], t_max=3000.0, rng=22)
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    bins = np.arange(0, 200)
    for tt, XX, c, lab in [(tc, Xc, MUTED, "constitutive"),
                           (tn, Xn, TEAL, "self-repressing")]:
        m, v = time_average(tt, XX, 3000.0, 20.0)
        ax.plot(bins, _occupancy(tt, XX[:, 0], 3000.0, 20.0, bins), color=c,
                lw=2.8, label=f"{lab}\nCV {np.sqrt(v[0]) / m[0]:.3f}")
    ax.set_xlim(60, 140)
    ax.set_ylim(0, 0.115)
    ax.set_xlabel("molecules")
    ax.set_ylabel("P(n)")
    ax.set_title("same mean, 100")
    ax.legend(loc="upper left", fontsize=14)
    _save(fig, "s12_nar_hist")

    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    gs = np.linspace(0, 4.2, 200)
    ax.plot(gs, 1 / (1 + gs), color=INK, lw=2.8)
    for n, seed in [(1, 31), (2, 32), (4, 33), (8, 34)]:
        st, a = negative_autoregulation(beta=200.0, K=100.0, n=n, gamma=1.0)
        tt, XX = gillespie(st, a, [100], t_max=3000.0, rng=seed)
        m, v = time_average(tt, XX, 3000.0, 20.0)
        ax.plot(n * 0.5, v[0] / m[0], "o", ms=12, mfc="none", mec=RED, mew=2.4)
        ax.text(n * 0.5 + 0.1, v[0] / m[0] + 0.05, f"n = {n}", color=RED,
                fontsize=13)
    ax.axhline(1.0, color=MUTED, lw=1.2, ls=":")
    ax.set_xlim(0, 4.4)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("loop gain  g")
    ax.set_ylabel("Fano factor")
    ax.set_title("1/(1+g), and Gillespie")
    _save(fig, "s12_nar_fano")


# ---------------------------------------------------------------------------
# 7. The scatter frame, before anyone is told what the directions mean
# ---------------------------------------------------------------------------
def fig_scatter_axes():
    """An EMPTY two-colour frame for the argue slide (5 October 2026).

    Adam's review of the built deck: the argue surface asks which direction an
    answer moves a point, and the plot it refers to does not appear until the
    following surface. So the room was being asked to reason about an object it
    had not seen. This is that object with the answer withheld: real axes, a
    real cloud, the diagonal, and the two directions labelled A and B instead
    of `intrinsic` and `extrinsic`. Naming them is the next surface's job, and
    it should be the room that does it.
    """
    rng = np.random.default_rng(7)
    c1, c2 = _two_color(120, 0.18, 700, rng)
    fig, ax = plt.subplots(figsize=(5.0, 4.5))
    hi = max(c1.max(), c2.max()) * 1.08
    ax.plot([0, hi], [0, hi], color=MUTED, lw=1.4, ls="--")
    ax.plot(c1, c2, "o", ms=3.4, color=TEAL, alpha=0.35)

    # Two double-headed arrows through the middle of the cloud: one along the
    # diagonal, one across it. Deliberately unlabelled beyond A and B.
    m, L = 120.0, 56.0
    for lab, (dx, dy), col in [("A", (1, 1), AMBER), ("B", (1, -1), RED)]:
        n = np.hypot(dx, dy)
        dx, dy = dx / n * L, dy / n * L
        ax.annotate("", xy=(m + dx, m + dy), xytext=(m - dx, m - dy),
                    arrowprops=dict(arrowstyle="<->", lw=3.0, color=col))
        ax.text(m + dx * 1.22, m + dy * 1.22, lab, color=col, fontsize=22,
                fontweight="bold", ha="center", va="center")

    ax.set_xlim(0, hi)
    ax.set_ylim(0, hi)
    ax.set_aspect("equal")
    ax.set_xlabel("copy 1  (CFP)")
    ax.set_ylabel("copy 2  (YFP)")
    ax.set_title("one point per cell, both colors measured")
    _save(fig, "s12_scatter_axes")


# ---------------------------------------------------------------------------
# 8. Three numbers off one histogram -- the vocabulary surface
# ---------------------------------------------------------------------------
def fig_noise_vocab():
    """sigma, eta and Fano read off a single simulated distribution.

    Adam's review, 5 October 2026: "the difference between sigma, and eta --
    std dev and Fano likely need to be explained to them." Three symbols were
    being used interchangeably across four surfaces. This draws all three off
    one picture, with their units, so the distinction is visual before it is
    algebraic.
    """
    k, gamma, T = 40.0, 1.0, 6000.0
    stoich, a = birth_death(k, gamma)
    t, X = gillespie(stoich, a, [0], t_max=T, rng=3)
    x = X[:, 0]
    m, v = time_average(t, X, T, t_burn=20.0)
    m, v = float(m[0]), float(v[0])
    sd = np.sqrt(v)

    bins = np.arange(0, int(m + 5 * sd) + 1)
    h = _occupancy(t, x, T, 20.0, bins)

    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    ax.bar(bins, h, width=1.0, color=TEAL, alpha=0.55, linewidth=0)
    ax.axvline(m, color=RED, lw=2.0)
    ax.annotate("", xy=(m + sd, 0.45 * h.max()), xytext=(m, 0.45 * h.max()),
                arrowprops=dict(arrowstyle="<->", lw=2.4, color=AMBER))
    ax.text(m + sd + 1.2, 0.45 * h.max(), "$\\sigma$", color=AMBER, fontsize=24,
            ha="left", va="center", fontweight="bold")
    ax.text(m - 1.5, 0.80 * h.max(), "$\\langle n\\rangle$", color=RED,
            fontsize=22, ha="right", va="center", fontweight="bold")
    ax.set_xlabel("molecules  n")
    ax.set_ylabel("fraction of TIME at n")
    ax.set_ylim(0, h.max() * 1.12)
    ax.set_xlim(0, bins[-1])
    ax.set_title(f"⟨n⟩ = {m:.1f}   σ = {sd:.1f}   "
                 f"η = {sd/m:.3f}   Fano = {v/m:.2f}")
    _save(fig, "s12_noise_vocab")
    return {"mean": m, "sd": sd, "eta": sd / m, "fano": v / m}


# ---------------------------------------------------------------------------
# 9. Panels for the "why they add as squares" run
# ---------------------------------------------------------------------------
def fig_squares_panels():
    """Three frames: shared causes only, private causes only, and both.

    Adam's review, 5 October 2026: slide 10 asserted eta_int^2 + eta_ext^2 =
    eta_tot^2 and he asked why noise adds as squares and why that matters. The
    algebra is one line of independence; what makes it land is seeing that the
    two causes make clouds of DIFFERENT SHAPE, and that the shapes are what the
    cross term being zero looks like.
    """
    rng = np.random.default_rng(19)
    mean, cells = 120, 700

    # extrinsic only: one rate per cell, both copies read it exactly
    sig = np.sqrt(np.log(1 + 0.25 ** 2))
    kk = mean * rng.lognormal(-sig ** 2 / 2, sig, cells)
    ext = (kk, kk.copy())
    # intrinsic only: one rate for every cell, independent counting at each copy
    ins = (rng.poisson(mean, cells).astype(float),
           rng.poisson(mean, cells).astype(float))
    # both
    both = _two_color(mean, 0.25, cells, rng)

    hi = max(max(p.max() for p in pair) for pair in (ext, ins, both)) * 1.08
    for name, (c1, c2), title in [
            ("s12_squares_ext", ext, "shared cause only: both copies move together"),
            ("s12_squares_int", ins, "private cause only: each copy counts for itself"),
            ("s12_squares_both", both, "a real strain: both at once")]:
        fig, ax = plt.subplots(figsize=(5.0, 4.4))
        ax.plot([0, hi], [0, hi], color=MUTED, lw=1.4, ls="--")
        ax.plot(c1, c2, "o", ms=3.4, color=TEAL, alpha=0.38)
        ei, ee, et = two_color_noise(c1, c2)
        ax.text(0.04, 0.96,
                f"$\\eta_{{int}}$ = {ei:.3f}\n$\\eta_{{ext}}$ = {ee:.3f}\n"
                f"$\\eta_{{tot}}$ = {et:.3f}",
                transform=ax.transAxes, va="top", fontsize=17, color=INK)
        ax.set_xlim(0, hi)
        ax.set_ylim(0, hi)
        ax.set_aspect("equal")
        ax.set_xlabel("copy 1")
        ax.set_ylabel("copy 2")
        ax.set_title(title, fontsize=14)
        _save(fig, name)


# ---------------------------------------------------------------------------
# 10. Narrow panels for the bursting run (5.4in figure column)
# ---------------------------------------------------------------------------
def fig_burst_panels():
    """The same two runs as fig_bursting, split into column-width panels.

    The wide two-panel version is for a full surface. A derivation run gets
    5.4 inches, and the traces are the whole argument there -- the room has to
    SEE that one of them arrives in lumps.
    """
    T = 3000.0
    fig1, ax1 = plt.subplots(figsize=(5.4, 4.3))
    fig2, ax2 = plt.subplots(figsize=(5.4, 4.3))
    out = []
    for (lab, km, gm, kp, gp), c, seed in zip(BURST, (TEAL, AMBER), (5, 6)):
        stoich, a = two_stage(km, gm, kp, gp)
        t, X = gillespie(stoich, a, [0, 50], t_max=T, rng=seed)
        m, v = time_average(t, X, T, t_burn=20.0)
        F = fano(m, v)[1]
        out.append((lab, float(m[1]), float(F), two_stage_fano(kp, gm, gp),
                    kp / gm))
        keep = t <= 25.0
        ax1.step(t[keep], X[keep, 1], where="post", color=c, lw=1.8,
                 label=f"b = {kp / gm:.0f}")
        occ = _occupancy(t, X[:, 1], T, 20.0, np.arange(0, 400))
        ns = np.arange(0, 181, 4)
        coarse = np.add.reduceat(occ[:181], np.arange(0, 181, 4))
        ax2.plot(ns + 2, coarse[:len(ns)], color=c, lw=2.6,
                 label=f"b = {kp / gm:.0f}: Fano {F:.1f}")
    ax1.axhline(50, color=MUTED, lw=1.2, ls="--")
    ax1.set_xlim(0, 25)
    ax1.set_ylim(0, 165)
    ax1.set_xlabel("time  (protein lifetimes)")
    ax1.set_ylabel("proteins")
    ax1.set_title("both means are 50")
    ax1.legend(loc="upper left", fontsize=15)
    _save(fig1, "s12_burst_traj")

    ax2.set_xlabel("proteins")
    ax2.set_ylabel("fraction of time")
    ax2.set_title("same mean, different spread")
    ax2.legend(loc="upper right", fontsize=14)
    _save(fig2, "s12_burst_hist")
    return out


# ---------------------------------------------------------------------------
# 11. What Becskei & Serrano actually built -- the four bars, as circuits
# ---------------------------------------------------------------------------
def fig_becskei_circuits():
    """The autoregulated construct and the three controls, drawn.

    Adam's review, 5 October 2026: "We need the 'circuit'." The slide carried
    their Fig. 3a -- four bars labelled A to D -- and the four constructs those
    bars stand for lived only in the speaker notes. A bar chart whose categories
    are undefined is not evidence of anything.

    Identities from their Fig. 3 caption (p. 592) and Fig. 2 caption (p. 591):
    A autoregulatory; B EGFP under CHROMOSOMAL TetR; C the operator-replaced
    system of Fig. 2c, after 1 mM IPTG; D the mutant-repressor system of
    Fig. 2b, TetR carrying Y42A in the DNA-binding domain.
    """
    from matplotlib.patches import Rectangle

    panels = [
        ("A  autoregulated", "P$_L$ + 2 tetO", "TetR–EGFP", "loop", TEAL,
         "it represses its own promoter"),
        ("B  chromosomal TetR", "P$_L$ + 2 tetO", "EGFP", "open", AMBER,
         "repressor made elsewhere: no loop"),
        ("C  operator replaced", "P$_L$ + lacO", "TetR–EGFP", "none", AMBER,
         "tetO swapped for lacO: nothing to bind"),
        ("D  mutant repressor", "P$_L$ + 2 tetO", "TetR(Y42A)–EGFP", "broken",
         RED, "Y42A cannot hold the operator"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.0))
    for ax, (title, prom, gene, loop, col, sub) in zip(axes.ravel(), panels):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
        ax.set_title(title, fontsize=14, color=col, fontweight="bold", pad=1)

        ax.add_patch(Rectangle((0.3, 2.00), 3.2, 1.05, facecolor="none",
                               edgecolor=MUTED, lw=1.6))
        ax.text(1.90, 2.52, prom, ha="center", va="center", fontsize=10.5,
                color=MUTED)
        ax.add_patch(Rectangle((4.05, 2.00), 5.6, 1.05, facecolor=col,
                               edgecolor="none", alpha=0.9))
        ax.text(6.85, 2.52, gene, ha="center", va="center", fontsize=10.5,
                color="white", fontweight="bold")
        ax.annotate("", xy=(4.00, 2.52), xytext=(3.60, 2.52),
                    arrowprops=dict(arrowstyle="-|>", lw=1.8, color=MUTED))

        if loop in ("loop", "broken"):
            solid = loop == "loop"
            c = col if solid else RULE
            ls = "-" if solid else (0, (3, 2))
            ax.plot([6.85, 6.85, 1.80, 1.80], [3.05, 4.55, 4.55, 3.55],
                    lw=2.2, color=c, ls=ls, solid_capstyle="round")
            ax.plot([1.15, 2.45], [3.50, 3.50], lw=3.2, color=c,
                    solid_capstyle="butt")
            if not solid:
                ax.plot([3.9, 4.9], [5.00, 4.10], lw=2.6, color=RED)
                ax.plot([3.9, 4.9], [4.10, 5.00], lw=2.6, color=RED)
        elif loop == "open":
            ax.annotate("", xy=(1.80, 3.10), xytext=(1.80, 4.35),
                        arrowprops=dict(arrowstyle="-", lw=2.2, color=MUTED))
            ax.plot([1.15, 2.45], [3.15, 3.15], lw=3.2, color=MUTED,
                    solid_capstyle="butt")
            ax.text(1.80, 4.70, "TetR from the chromosome", ha="center",
                    va="center", fontsize=10, color=MUTED, style="italic")
        ax.text(5.0, 0.85, sub, ha="center", va="center", fontsize=10.5,
                color=INK, style="italic")
    fig.subplots_adjust(hspace=0.30, wspace=0.10)
    fig.savefig(f"{OUT}/s12_becskei_circuits.png")
    plt.close(fig)


FIGURES = [fig_ssa_anatomy, fig_birth_death, fig_bursting, fig_nar_noise,
           fig_two_color, fig_derivation_panels, fig_scatter_axes,
           fig_noise_vocab, fig_squares_panels, fig_burst_panels,
           fig_becskei_circuits]


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for f in FIGURES:
        r = f()
        if r is not None:
            print(f.__name__, r)
