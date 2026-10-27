"""Session 22 figures — an integrator that does not need to know the disturbance.

ONE MODEL PER FIGURE, AND THE MODEL IS NAMED ON THE FIGURE. Session 21's
rebuild added that rule after a figure spliced two models; this session has the
same hazard in a different costume, because "ideal" (delta = 0) and "leaky"
(delta > 0) disagree about the one thing the hour claims.

Every curve comes out of `posb.control`, the same functions the students call.

AOKI'S DATA IS NOT REDRAWN HERE. We hold the paper's two p-values but not the
growth-rate points behind them, so Fig. 3d goes on a slide as a PAPER FIGURE
with its own attribution. Inventing points to redraw it would be exactly the
thing this course keeps telling students not to do.

What this session has to draw:

  * THE MOTIF. `fig_motif` -- Z1 carries the set point, Z2 senses the output,
    the two annihilate. Drawn, because the subtraction that makes it an
    integrator is visible in the picture.
  * THE CLAIM. `fig_plant_does_not_matter` -- the output against time for four
    different plants. They land on the same line. This is the figure the hour
    exists for.
  * THE REJECTION. `fig_step` -- closed and open loop under the same step
    disturbance.
  * THE LIMIT. `fig_leak` -- SET-POINT error against the dilution rate, log
    on log, slope one.

Run:  python tools/build_figures.py s22
"""
import numpy as np

from figures.style import (use, TEAL, CYAN, AMBER, MUTED, INK, RED, GREEN,
                           RULE, TYPE)
from posb.control import (ControlParams, simulate, closed_loop_steady_state,
                          open_loop_steady_state, setpoint_error)

plt = use()
OUT = "figures/build"
P = ControlParams()


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png")
    plt.close(fig)


def fig_motif():
    """The antithetic motif, drawn so the subtraction is visible.

    Z1 is made at a constant rate (the set point). Z2 is made in proportion to
    the output (the sensor). They annihilate, and because annihilation removes
    them at the SAME rate it cancels when you subtract -- which is why Z1 - Z2
    integrates the error and nothing else in the circuit matters.
    """
    fig, ax = plt.subplots(figsize=(10.4, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.3); ax.axis("off")

    def box(x, y, w, h, label, colour, sub=None):
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, lw=2.2,
                                   edgecolor=colour, zorder=3))
        ax.text(x + w / 2, y + h / 2 + (0.20 if sub else 0), label,
                ha="center", va="center", color=colour,
                fontsize=TYPE["emphasis"], zorder=4)
        if sub:
            ax.text(x + w / 2, y + h / 2 - 0.36, sub, ha="center", va="center",
                    color=MUTED, fontsize=TYPE["caption"], zorder=4)

    def arrow(x1, y1, x2, y2, colour, rad=0.0):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.2,
                                    connectionstyle=f"arc3,rad={rad}"))

    # The equation gets a band of its own at the top; nothing else enters it.
    ax.text(5.0, 5.85,
            "$\\dfrac{d(Z_1 - Z_2)}{dt} = \\mu - \\theta X$"
            "      $\\Rightarrow$      steady state forces  $X = \\mu/\\theta$",
            ha="center", va="center", color=INK, fontsize=TYPE["emphasis"])

    box(0.4, 3.45, 2.3, 1.1, "$Z_1$", TEAL, "set point, rate $\\mu$")
    box(0.4, 0.45, 2.3, 1.1, "$Z_2$", AMBER, "sensor, rate $\\theta X$")
    box(7.1, 2.00, 2.5, 1.1, "the plant", INK)
    ax.text(8.35, 1.72, "any topology, any parameters", ha="center",
            va="top", color=MUTED, fontsize=TYPE["caption"])

    # annihilation, between the two Z boxes, with its text in the empty
    # middle band -- left of the plant, right of the arrow
    ax.annotate("", xy=(1.45, 1.55), xytext=(1.45, 3.45),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.4))
    ax.text(1.85, 2.98, "$Z_1 + Z_2 \\rightarrow \\varnothing$", color=RED,
            fontsize=TYPE["emphasis"], va="center")
    # va="top" from 2.55 puts two caption lines at roughly 2.55 -> 1.85, which
    # clears the Z2 box at y=1.55. At the original 2.30 the second line sat on
    # the box's top edge (caught in the 26 October render).
    ax.text(1.95, 2.55, "removes both at the same rate,\nso it cancels on subtraction",
            color=RED, fontsize=TYPE["caption"], va="top", linespacing=1.3)

    arrow(2.7, 4.05, 7.1, 2.95, TEAL, rad=-0.18)
    ax.text(4.9, 4.45, "$Z_1$ drives the output", color=TEAL,
            fontsize=TYPE["body"], ha="center")
    arrow(7.1, 2.15, 2.7, 1.05, AMBER, rad=-0.18)
    ax.text(5.1, 0.72, "the output is sensed", color=AMBER,
            fontsize=TYPE["body"], ha="center")

    _save(fig, "s22_motif")


def fig_plant_does_not_matter():
    """THE SESSION'S CLAIM. Four different plants, one set point.

    Aoki: "it does not depend on the topology and parameters of the controlled
    network". So vary the controlled network and show the output landing in
    the same place. The transients differ -- that is the plant -- and the
    destination does not.
    """
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    t = np.linspace(0, 120, 1200)
    runs = [
        ("reference",                 P,                                      TEAL,  "-"),
        ("plant gain $k$: $1 \\to 4$", ControlParams(k=4.0),                  CYAN,  "--"),
        ("removal $\\gamma$: $0.5 \\to 0.1$", ControlParams(gamma=0.1),       AMBER, "-."),
        ("annihilation $\\eta$: $50 \\to 500$", ControlParams(eta=500.0),     RED,   ":"),
    ]
    for label, q, colour, ls in runs:
        sol = simulate(q, d=0.0, t_end=400.0)
        ax.plot(t, sol.sol(t)[0], color=colour, ls=ls, lw=2.3, label=label)

    ax.axhline(P.set_point, color=MUTED, lw=1.4, ls=":")
    ax.text(118, P.set_point + 0.18, "$\\mu/\\theta = 5$", color=MUTED,
            fontsize=TYPE["body"], ha="right", va="bottom")
    ax.set_xlabel("time")
    ax.set_ylabel("output $X$")
    ax.set_xlim(0, 120); ax.set_ylim(0, 11.6)
    ax.set_title("Four different plants, one set point   "
                 "(ideal controller, $\\delta = 0$)", pad=14)
    # Upper right: past t = 60 every curve is within half a unit of 5, so
    # the whole top-right quadrant is empty.
    ax.legend(loc="upper right", frameon=False, fontsize=TYPE["caption"])
    # Top LEFT band, above every curve's peak, so nothing is written over.
    ax.text(0.035, 0.97,
            "the transients differ — that is the plant.\n"
            "the destination does not.",
            transform=ax.transAxes, va="top", color=INK,
            fontsize=TYPE["body"], linespacing=1.3)
    _save(fig, "s22_plant_does_not_matter")


def fig_step():
    """Closed and open loop, same plant, same step disturbance."""
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    t = np.linspace(0, 200, 1400)
    d = 2.0

    sol = simulate(P, d=0.0, t_end=400.0)
    ax.plot(t, sol.sol(t)[0], color=MUTED, lw=1.8, ls=":",
            label="no disturbance")
    sol_c = simulate(P, d=d, t_end=400.0)
    ax.plot(t, sol_c.sol(t)[0], color=TEAL, lw=2.6,
            label=f"closed loop, $d = {d:g}$")

    open_ss = open_loop_steady_state(P, d)
    base = open_loop_steady_state(P, 0.0)
    ax.axhline(open_ss, color=RED, lw=2.6, ls="--",
               label=f"open loop, $d = {d:g}$")

    ax.annotate("", xy=(118, open_ss), xytext=(118, base),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.0))
    ax.text(113, (open_ss + base) / 2, f"+{open_ss - base:.0f}", color=RED,
            fontsize=TYPE["emphasis"], ha="right", va="center")

    ax.set_xlabel("time")
    ax.set_ylabel("output $X$")
    ax.set_xlim(0, 200)
    # Headroom above the open-loop line so the sentence has a band of its own.
    ax.set_ylim(0, 12.6)
    ax.set_title("The same disturbance, with the loop closed and open   "
                 "(ideal controller, $\\delta = 0$)", pad=14)
    # Lower right: past t = 30 the only curve is the closed loop, flat at 5.
    ax.legend(loc="lower right", frameon=False, fontsize=TYPE["caption"])
    ax.text(0.035, 0.965,
            "the closed loop lands back on $\\mu/\\theta$\n"
            "and the open loop does not move back at all",
            transform=ax.transAxes, va="top", color=INK,
            fontsize=TYPE["body"], linespacing=1.3)
    _save(fig, "s22_step")


def fig_leak():
    """THE LIMIT. Adaptation error against the dilution rate, slope one.

    The integrator is exact only if Z1 and Z2 are lost ONLY by annihilation.
    Dilute them and mu - theta*X = delta*(Z1 - Z2), so the error is first
    order in delta. This is the session's link back to rung 1: growth rate was
    what the circuit changed, and here it is what degrades the guarantee.
    """
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    deltas = np.logspace(-3.4, -0.7, 18)
    errs = [abs(setpoint_error(ControlParams(delta=float(dl)), 2.0))
            for dl in deltas]

    ax.loglog(deltas, errs, "o-", color=TEAL, lw=2.4, ms=8)
    ref = errs[0] * (deltas / deltas[0])
    ax.loglog(deltas, ref, color=MUTED, lw=1.4, ls=":")
    # Label the reference line partway along it, BELOW the data, so it never
    # reaches the title band.
    ax.text(deltas[9], ref[9] * 0.45, "slope 1", color=MUTED,
            fontsize=TYPE["body"], ha="center", va="top")

    ax.set_xlabel("dilution rate of the controller species,  $\\delta$")
    ax.set_ylabel("|adaptation error|")
    ax.set_title("Dilute the controller and the integrator leaks", pad=14)
    ax.text(0.035, 0.95,
            "$\\mu - \\theta X = \\delta\\,(Z_1 - Z_2)$\n"
            "so the error is FIRST ORDER in $\\delta$ —\n"
            "and $\\delta$ is the growth rate.",
            transform=ax.transAxes, va="top", color=INK,
            fontsize=TYPE["body"], linespacing=1.35)
    ax.text(0.985, 0.045, "LEAKY controller. at $\\delta = 0$ the error is exactly zero.",
            transform=ax.transAxes, ha="right", va="bottom",
            color=MUTED, fontsize=TYPE["caption"])
    _save(fig, "s22_leak")


FIGURES = [fig_motif, fig_plant_does_not_matter, fig_step, fig_leak]


if __name__ == "__main__":
    for f in FIGURES:
        f(); print("drew", f.__name__)
