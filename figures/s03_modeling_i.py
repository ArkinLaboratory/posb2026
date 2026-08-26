"""Session 3 figures — mass action, stoichiometry, and dx/dt = S v.

Three figures, and each one exists to make a claim checkable rather than
decorative:

  * the three implementations agree, and "agree" is a NUMBER (~1e-12), not an
    adjective about two curves that look the same at slide resolution;
  * a conservation law is the cheapest test of a model, and one flipped sign
    breaks it visibly while the trajectory still looks plausible;
  * the cascade separates timescales by an order of magnitude, which is the
    observation session 4 is built on.

Everything here runs through `posb`, deliberately: the plot on the slide is
produced by the same code the students call in the notebook, so the figure
cannot drift from what they will see on their own screens.

    python tools/build_figures.py s03
"""
import numpy as np
from scipy.integrate import solve_ivp

from posb import Model, Reaction
from figures.style import use, AMBER, CYAN, GREEN, INK, MUTED, RED, RULE, TEAL

plt = use()
OUT = "figures/build"

# The binding example, identical to sections 1-3 of the notebook.
KF, KR = 1.0, 0.2
X0 = {"A": 1.0, "B": 1.5, "C": 0.0}
TSPAN = (0, 15)

# The cascade, identical to section 4 of the notebook. Half-lives ~1.4 min for
# the mRNA and ~14 min for the protein: the tenfold separation is the generic
# bacterial situation, not a convenience of the numbers chosen.
CASCADE = {"alpha": 10.0, "gamma_m": 0.5, "k_p": 4.0, "gamma_p": 0.05}


def _hand(t, y):
    """The long way: every derivative written out, no matrix anywhere."""
    A, B, C = y
    return [-KF * A * B + KR * C,
            -KF * A * B + KR * C,
            +KF * A * B - KR * C]


def _by_matrix(t, y):
    """The short way: S and v, assembled by hand."""
    S = np.array([[-1, +1], [-1, +1], [+1, -1]])
    A, B, C = y
    v = np.array([KF * A * B, KR * C])
    return S @ v


def _binding_model():
    """The shorter way: posb builds S from the reaction list."""
    return Model([Reaction({"A": 1, "B": 1}, {"C": 1}, k=KF, name="forward"),
                  Reaction({"C": 1}, {"A": 1, "B": 1}, k=KR, name="reverse")],
                 species=["A", "B", "C"])


def fig_three_ways():
    """Three implementations, one system -- and 'identical' as a number."""
    t_eval = np.linspace(*TSPAN, 400)
    y0 = [X0[s] for s in "ABC"]
    hand = solve_ivp(_hand, TSPAN, y0, t_eval=t_eval, rtol=1e-10, atol=1e-12)
    mat = solve_ivp(_by_matrix, TSPAN, y0, t_eval=t_eval, rtol=1e-10, atol=1e-12)
    traj = _binding_model().simulate(X0, TSPAN, n_points=400,
                                     rtol=1e-10, atol=1e-12)

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.4, 4.1))

    from matplotlib.lines import Line2D
    for i, (name, c) in enumerate(zip("ABC", (TEAL, CYAN, AMBER))):
        ax.plot(hand.t, hand.y[i], lw=4.5, color=c, alpha=0.30)
        ax.plot(mat.t, mat.y[i], lw=1.8, color=c, ls="--")
        ax.plot(traj.t, traj[name], lw=1.0, color=INK, ls=":")
        ax.annotate(name, (0.30, hand.y[i][14]), fontsize=13, weight="bold",
                    color=c, xytext=(-14, -4), textcoords="offset points")
    # Hand-built legend: the real handles are 30%-alpha and read as grey.
    ax.legend(handles=[Line2D([], [], lw=4.5, color=MUTED, alpha=0.45,
                              label="written out by hand"),
                       Line2D([], [], lw=1.8, color=MUTED, ls="--",
                              label="S · v, assembled by hand"),
                       Line2D([], [], lw=1.2, color=INK, ls=":",
                              label="posb.Model")],
              fontsize=9.5, loc="center right", framealpha=0.95)
    ax.set_xlabel("time")
    ax.set_ylabel("concentration")
    ax.set_title("One system, three implementations")
    ax.grid(True, lw=0.5, alpha=0.3)

    # The point of the right panel: "they look the same" is not a result.
    d_mat = np.max(np.abs(mat.y - hand.y), axis=0)
    d_posb = np.max(np.abs(traj.y - hand.y), axis=0)
    bx.semilogy(t_eval, np.maximum(d_mat, 1e-16), lw=2.2, color=TEAL,
                label="hand  vs  S·v")
    bx.semilogy(traj.t, np.maximum(d_posb, 1e-16), lw=2.2, color=AMBER,
                label="hand  vs  posb")
    bx.axhline(1e-9, lw=1.2, ls=":", color=RED)
    bx.text(TSPAN[1] * 0.97, 1.6e-9, "the notebook's assert: < 1e-9",
            fontsize=9.5, color=RED, ha="right", style="italic")
    bx.set_ylim(1e-16, 1e-6)
    bx.set_xlabel("time")
    bx.set_ylabel("largest disagreement, any species")
    bx.set_title("Agreement is a number, not an impression")
    bx.legend(fontsize=9, loc="upper left")
    bx.grid(True, which="both", lw=0.5, alpha=0.3)
    # The teal trace sits on the floor of the axis and reads as a missing
    # line unless you say why: same RHS, same solver, same arithmetic.
    bx.text(0.4, 2.2e-16, "hand vs S·v — identical to the last bit",
            fontsize=9.5, color=TEAL, va="bottom", weight="bold")

    fig.tight_layout()
    fig.savefig(f"{OUT}/s03_three_ways.png")
    plt.close(fig)


def fig_conservation():
    """A missing factor of 2. The trajectory is fine; the invariant is not.

    The first draft of this figure used a flipped sign in dB/dt, and the
    flipped sign sent [B] negative -- which made the caption ("nothing here
    looks wrong") false. So it uses the error the notebook's E4 is about
    instead: dimerisation, P + P <-> P2, with the stoichiometric 2 dropped
    from the P equation. Every concentration stays positive, both species
    settle, the equilibrium ratio is even right. Only the conserved quantity
    knows.
    """
    kf, kr = 0.8, 0.4
    tspan, t_eval = (0, 15), np.linspace(0, 15, 400)
    y0 = [1.2, 0.0]                      # [P], [P2]

    def correct(t, y):
        """2P -> P2 consumes TWO P per event, so the 2 is in the P row of S."""
        P, P2 = y
        v = np.array([kf * P ** 2, kr * P2])
        return np.array([[-2, +2], [+1, -1]]) @ v

    def dropped_two(t, y):
        """The same model with the stoichiometric coefficient left at 1."""
        P, P2 = y
        v = np.array([kf * P ** 2, kr * P2])
        return np.array([[-1, +1], [+1, -1]]) @ v

    good = solve_ivp(correct, tspan, y0, t_eval=t_eval, rtol=1e-10, atol=1e-12)
    bad = solve_ivp(dropped_two, tspan, y0, t_eval=t_eval, rtol=1e-10,
                    atol=1e-12)

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.4, 4.1))

    ax.plot(bad.t, bad.y[0], lw=2.6, color=TEAL, label="P")
    ax.plot(bad.t, bad.y[1], lw=2.6, color=AMBER, label="P$_2$")
    ax.set_xlabel("time")
    ax.set_ylabel("concentration")
    ax.set_title("The model with the coefficient dropped")
    ax.set_ylim(0, 1.35)
    ax.grid(True, lw=0.5, alpha=0.3)
    ax.annotate("P", (6.0, 0.565), fontsize=13, weight="bold", color=TEAL,
                textcoords="offset points", xytext=(0, -18))
    ax.annotate("P$_2$", (6.0, 0.635), fontsize=13, weight="bold", color=AMBER,
                textcoords="offset points", xytext=(0, 8))
    ax.text(0.05, 0.97,
            "Positive. Monotone. Settles.\nThe equilibrium ratio is even right.\n"
            "There is nothing to see here.",
            transform=ax.transAxes, fontsize=10.5, color=RED, style="italic",
            va="top", linespacing=1.6)

    for sol, lab, c in [(good, "correct", TEAL), (bad, "coefficient dropped", RED)]:
        bx.plot(sol.t, sol.y[0] + 2 * sol.y[1], lw=2.8, color=c,
                label=f"[P] + 2[P$_2$], {lab}")
    bx.set_xlabel("time")
    bx.set_ylabel("[P] + 2[P$_2$]")
    bx.set_title("The conservation law is not fooled")
    bx.set_ylim(1.0, 2.05)
    bx.legend(fontsize=9.5, loc="center right")
    bx.grid(True, lw=0.5, alpha=0.3)
    bx.text(0.12, 0.27,
            "Every P$_2$ locks up two P, so this must be flat.\n"
            "Two extra lines of code, and the cheapest test\n"
            "you will ever write.",
            transform=bx.transAxes, fontsize=9.5, color=INK, va="bottom",
            linespacing=1.6)

    fig.tight_layout()
    fig.savefig(f"{OUT}/s03_conservation.png")
    plt.close(fig)


def fig_cascade():
    """The two timescales, which is the whole setup for session 4."""
    p = CASCADE
    cascade = Model(
        [Reaction({}, {"mRNA": 1}, k="alpha", name="transcription"),
         Reaction({"mRNA": 1}, {}, k="gamma_m", name="mRNA decay"),
         Reaction({"mRNA": 1}, {"mRNA": 1, "protein": 1}, k="k_p",
                  name="translation"),
         Reaction({"protein": 1}, {}, k="gamma_p", name="protein decay")],
        params=p, species=["mRNA", "protein"])

    traj = cascade.simulate({"mRNA": 0.0, "protein": 0.0}, (0, 150),
                            n_points=800)
    m_star = p["alpha"] / p["gamma_m"]
    p_star = p["k_p"] * m_star / p["gamma_p"]
    tau_m, tau_p = 1 / p["gamma_m"], 1 / p["gamma_p"]

    fig, ax = plt.subplots(figsize=(11.4, 4.1))
    bx = ax.twinx()

    # Put the real numbers in the annotation. An earlier draft said the protein
    # "has barely started" at 5 tau_m, which is false -- it is at 39% -- and a
    # figure on a slide about checking your claims cannot carry an unchecked one.
    t_mark = 5 * tau_m
    frac_m = np.interp(t_mark, traj.t, traj["mRNA"]) / m_star
    frac_p = np.interp(t_mark, traj.t, traj["protein"]) / p_star
    ax.axvspan(0, t_mark, color=CYAN, alpha=0.13, lw=0)
    ax.text(52, 0.42 * m_star,
            f"At 5$\\tau_m$ = {t_mark:.0f} min the mRNA is at {frac_m:.0%} of\n"
            f"its steady state and the protein at {frac_p:.0%}.",
            fontsize=10, color=INK, va="top", linespacing=1.5)

    ax.plot(traj.t, traj["mRNA"], lw=2.8, color=AMBER, label="mRNA")
    ax.axhline(m_star, lw=1.2, ls="--", color=AMBER)
    ax.annotate(r"$m^* = \alpha/\gamma_m = %.0f$" % m_star, (150, m_star),
                textcoords="offset points", xytext=(-6, 6), ha="right",
                fontsize=11, color=AMBER, weight="bold")
    ax.set_ylabel("mRNA (molecules)", color=AMBER)
    ax.set_ylim(0, m_star * 1.35)
    ax.tick_params(axis="y", colors=AMBER)

    bx.plot(traj.t, traj["protein"], lw=2.8, color=TEAL, label="protein")
    bx.axhline(p_star, lw=1.2, ls="--", color=TEAL)
    bx.annotate(r"$p^* = k_p\alpha/\gamma_m\gamma_p = %.0f$" % p_star,
                (150, p_star), textcoords="offset points", xytext=(-6, -16),
                ha="right", fontsize=11, color=TEAL, weight="bold")
    bx.set_ylabel("protein (molecules)", color=TEAL)
    bx.set_ylim(0, p_star * 1.35)
    bx.tick_params(axis="y", colors=TEAL)

    ax.set_xlabel("time (min)")
    ax.set_xlim(0, 150)
    ax.set_title(r"Two species, one cascade, timescales $\tau_m = %.0f$ min "
                 r"and $\tau_p = %.0f$ min" % (tau_m, tau_p))
    ax.grid(True, lw=0.5, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f"{OUT}/s03_cascade.png")
    plt.close(fig)




# --- the QSSA error, which is what session 4 is actually about ---------------
# Nondimensionalising the cascade collapses four parameters into one. With
# tau = gamma_p t, mu = m/m*, pi = p/p*:
#
#     dmu/dtau = (1/eps)(1 - mu),      dpi/dtau = mu - pi,     eps = gp/gm
#
# and the exact solution is
#
#     pi(tau) = 1 - [ e^-tau - eps e^(-tau/eps) ] / (1 - eps)
#
# The quasi-steady-state approximation is the eps -> 0 limit, mu = 1, giving
# pi_qssa = 1 - e^-tau. So the error is available in closed form:
#
#     pi_qssa - pi_exact = [eps/(1-eps)] ( e^-tau - e^(-tau/eps) )
#
# The maximum sits at tau ~ -eps ln(eps), where the first exponential is still
# ~1 and the second has fallen to ~eps, so the largest error approaches eps
# itself: at eps = 0.01 it is 0.0095, at eps = 0.1 it is 0.077. The error is
# the timescale separation, near enough, and that is a far more useful thing
# to know than "the approximation is good when the separation is large".
def _pi_exact(tau, eps):
    if abs(eps - 1.0) < 1e-9:               # the degenerate case, by l'Hopital
        return 1 - (1 + tau) * np.exp(-tau)
    return 1 - (np.exp(-tau) - eps * np.exp(-tau / eps)) / (1 - eps)


def _pi_qssa(tau):
    return 1 - np.exp(-tau)


def fig_qssa_error():
    """How wrong is 'set dm/dt = 0'? Exactly O(eps), and here is the exponent."""
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.4, 4.1))

    tau = np.linspace(0, 6, 1200)
    ax.plot(tau, _pi_qssa(tau), lw=3.2, color=MUTED, ls="--",
            label=r"QSSA:  $1 - e^{-\tau}$")
    for eps, c in [(0.1, TEAL), (0.4, CYAN), (0.9, AMBER)]:
        ax.plot(tau, _pi_exact(tau, eps), lw=2.4, color=c,
                label=rf"exact,  $\epsilon = {eps}$")
    ax.set_xlabel(r"scaled time  $\tau = \gamma_p t$")
    ax.set_ylabel(r"$p/p^*$")
    ax.set_title("One parameter, not four")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9.5, loc="lower right")
    ax.grid(True, lw=0.5, alpha=0.3)
    ax.text(0.06, 0.96, r"$\epsilon = \gamma_p/\gamma_m$" "\nour cascade: 0.1",
            transform=ax.transAxes, fontsize=11, color=INK, va="top",
            linespacing=1.6)

    eps = np.geomspace(1e-3, 1.0, 160)
    t = np.linspace(0, 40, 6000)
    err = np.array([np.max(np.abs(_pi_qssa(t) - _pi_exact(t, e))) for e in eps])
    bx.loglog(eps, err, lw=2.6, color=TEAL, label="max error, computed")
    bx.loglog(eps, eps, lw=1.4, ls=":", color=RED,
              label=r"$\epsilon$  — the error IS the separation")
    bx.plot([0.1], [np.max(np.abs(_pi_qssa(t) - _pi_exact(t, 0.1)))], "o",
            ms=9, color=AMBER, zorder=5)
    bx.annotate("our cascade:\n8% of $p^*$", (0.1, np.max(np.abs(
        _pi_qssa(t) - _pi_exact(t, 0.1)))), textcoords="offset points",
        xytext=(-14, 12), ha="right", fontsize=10, color=AMBER, weight="bold",
        linespacing=1.5)
    bx.set_xlabel(r"$\epsilon = \gamma_p/\gamma_m$   (timescale separation)")
    bx.set_ylabel(r"largest error in $p/p^*$")
    bx.set_title("The approximation has an error bar")
    bx.legend(fontsize=9.5, loc="upper left")
    bx.grid(True, which="both", lw=0.5, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f"{OUT}/s03_qssa_error.png")
    plt.close(fig)


FIGURES = [fig_three_ways, fig_conservation, fig_cascade, fig_qssa_error]
