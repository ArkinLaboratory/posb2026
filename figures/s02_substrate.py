"""Session 2 figures — the cell as a physical substrate.

Two figures, and between them they carry the session. Every number in both is
sourced in the docstrings below, because the whole point of session 2 is that
these are quantities you can look up and check rather than adjectives.

    python tools/build_figures.py s02
"""
import numpy as np
from matplotlib.patches import FancyBboxPatch

from figures.style import use, AMBER, CYAN, GREEN, INK, MUTED, RED, RULE, TEAL

plt = use()
OUT = "figures/build"

# --- the constants, with provenance -----------------------------------------
NA = 6.022e23          # /mol
V_ECOLI = 1e-15        # L. A rod ~1 x 2 um; the standard round number.
KT = 4.14e-21          # J at 300 K
ETA_WATER = 1e-3       # Pa s
D_GFP = 7.7            # um^2/s, GFP in E. coli DH5-alpha cytoplasm.
                       # Elowitz, Surette, Wolf, Stock & Leibler,
                       # J Bacteriol 181:197-203 (1999). +/- 2.5, and ~11x
                       # slower than the same protein in water -- the factor of
                       # 11 IS the crowding, and it is the point of the session.


# Effective viscosity is NOT a property of the cytoplasm alone -- it depends on
# how big the thing moving through it is, because a small probe slips between
# obstacles a large one has to push past.
#
#   ~4-5 nm  (GFP)            ~12 cP     Elowitz et al. 1999
#   20-50 nm (ribosome-sized) ~100 cP    Valverde-Mendez et al., PNAS 122(4),
#                                        e2406340121 (2025)
#
# Water is 1 cP. So the crowding penalty is a factor of ~12 for a small protein
# and ~100 for a ribosome, and a single number for "the viscosity of cytoplasm"
# is not a thing that exists.
ETA_EFF = [(2.3, 12.0), (10.0, 100.0), (25.0, 100.0)]   # (radius nm, cP)


def eta_effective(a_nm):
    """Effective viscosity in cP for a probe of radius a_nm, log-interpolated."""
    xs = np.log([a for a, _ in ETA_EFF])
    ys = np.log([e for _, e in ETA_EFF])
    return np.exp(np.interp(np.log(a_nm), xs, ys))


def stokes_einstein(a_nm, eta_cP):
    """D in um^2/s from the Stokes-Einstein relation, D = kT / 6 pi eta a."""
    a = np.asarray(a_nm) * 1e-9
    eta = np.asarray(eta_cP) * ETA_WATER
    return KT / (6 * np.pi * eta * a) * 1e12


def molecules_per_cell(conc_M, volume_L=V_ECOLI):
    """Copy number from concentration. The one calculation of session 2."""
    return conc_M * volume_L * NA


def diffusion_time(L_um, D=D_GFP):
    """t ~ L^2 / 2D, the one-dimensional convention.

    The convention matters and the course states it every time: 1-D gives
    L^2/2D, 3-D gives L^2/6D. A factor of three is nothing next to the factor
    of 400 that comes from squaring the distance, but a stated convention is
    the difference between an estimate and a guess.
    """
    return L_um ** 2 / (2 * D)


# ---------------------------------------------------------------------------

def fig_copy_number():
    """Where 'concentration' stops being a sensible variable."""
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    conc = np.geomspace(1e-12, 1e-5, 400)          # 1 pM to 10 uM
    n = molecules_per_cell(conc)

    ax.loglog(conc * 1e9, n, lw=2.4, color=TEAL)
    ax.axhline(1, color=RED, lw=1.4, ls="--")
    ax.axhspan(n.min(), 1, color=RED, alpha=0.06)
    ax.text(9e3, 1.5e-3, "below this line there is fewer than one\n"
                         "molecule per cell — 'concentration' is then\n"
                         "a statement about a population,\n"
                         "not about this cell",
            fontsize=9, color=RED, ha="right", va="bottom", linespacing=1.5)

    for c_nM, lab in [(1, "1 nM\n≈ 1 molecule"),
                      (100, "100 nM\n≈ 60"),
                      (1000, "1 µM\n≈ 600")]:
        y = molecules_per_cell(c_nM * 1e-9)
        ax.plot([c_nM], [y], "o", ms=7, color=AMBER, zorder=5)
        ax.annotate(lab, (c_nM, y), textcoords="offset points",
                    xytext=(-6, 12), fontsize=9, color=INK, ha="right",
                    linespacing=1.4)

    ax.set_xlabel("concentration  (nM)")
    ax.set_ylabel("molecules in one $E.\\ coli$  (1 fL)")
    ax.set_title("One nanomolar is one molecule per cell")
    ax.grid(True, which="both", lw=0.5, alpha=0.35)
    fig.tight_layout()
    fig.savefig(f"{OUT}/s02_copy_number.png")
    plt.close(fig)


def fig_timescales():
    """Every process in the course, on one logarithmic axis."""
    fig, ax = plt.subplots(figsize=(12.6, 4.75))

    # (label, seconds, colour, note). Sources in the module docstring and here.
    rows = [
        ("protein crosses E. coli\n(1 µm)", diffusion_time(1.0), CYAN,
         "$L^2/2D$, D = 7.7 µm²/s"),
        ("transcribe a 1 kb gene", 1000 / 55, TEAL, "~55 nt/s"),
        ("translate a 300 aa protein", 300 / 17, TEAL, "~17 aa/s"),
        # Plotted at the SAME D as E. coli, which is the question the handout's
        # item 3 asks and the comparison the axis is for. Say "same D" on the
        # annotation: GFP actually moves ~27 µm²/s in eukaryotic cytoplasm
        # (Swaminathan, Hoang & Verkman, Biophys J 72:1900, 1997), so the real
        # crossing is ~7 s and the real ratio ~110×. The exponent is the point;
        # an unqualified "400×" would contradict the answers slide at 63 min.
        ("protein crosses a HeLa cell\n(20 µm)", diffusion_time(20.0), CYAN,
         "20× the distance, 400× the time — at the same D"),
        ("mRNA lifetime", 5 * 60, GREEN, "~2–8 min in E. coli"),
        ("cell division", 25 * 60, AMBER, "rich medium"),
        ("stable protein lifetime\n(set by dilution)", 25 * 60 / 0.693, AMBER,
         "no degradation tag: halved by growth alone"),
        ("the toggle fails", 40 * 3600, RED, "session 9"),
    ]

    for i, (lab, t, c, note) in enumerate(rows):
        y = len(rows) - i + 0.75
        ax.plot([2e-2, t], [y, y], lw=1.0, color=RULE, zorder=1)
        ax.plot([t], [y], "o", ms=11, color=c, zorder=3)
        nlines = lab.count("\n") + 1
        ax.text(t * 1.5, y + (0.10 if nlines > 1 else 0), lab, va="center",
                fontsize=9.5, color=INK, linespacing=1.3)
        ax.text(t * 1.5, y - (0.34 if nlines > 1 else 0.28), note,
                va="center", fontsize=8, color=MUTED, style="italic")

    ax.set_xscale("log")
    ax.set_xlim(2e-2, 3e7)
    ax.set_ylim(0.0, len(rows) + 1.75)
    ax.set_yticks([])
    ax.set_xlabel("seconds")
    for spine in ("left", "right", "top"):
        ax.spines[spine].set_visible(False)

    for t, lab in [(1, "1 s"), (60, "1 min"), (3600, "1 hr"),
                   (86400, "1 day")]:
        ax.axvline(t, color=RULE, lw=0.8, zorder=0)
        ax.text(t, len(rows) + 1.4, lab, ha="center", fontsize=8.5,
                color=MUTED)

    ax.text(2.4e-2, 0.35,
            "Nine orders of magnitude. Anything you design lives somewhere on "
            "this axis — and the fast things are already at equilibrium by the "
            "time the slow things move.",
            fontsize=9.5, color=INK, style="italic")
    fig.tight_layout()
    fig.savefig(f"{OUT}/s02_timescales.png")
    plt.close(fig)


def fig_size_dependence():
    """A ribosome is not a slow protein. It is in a different fluid."""
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.4, 4.3))
    a = np.geomspace(1.5, 40, 300)

    ax.loglog(a, stokes_einstein(a, 1.0), lw=2.2, color=MUTED, ls="--",
              label="if the cell were water")
    ax.loglog(a, stokes_einstein(a, eta_effective(a)), lw=2.6, color=TEAL,
              label="measured in E. coli")
    ax.set_xlabel("probe radius  (nm)")
    ax.set_ylabel("D  (µm²/s)")
    ax.set_title("The medium depends on the probe")
    ax.legend(fontsize=9)
    ax.grid(True, which="both", lw=0.5, alpha=0.3)

    for a0, lab, c in [(2.3, "GFP", CYAN), (10, "ribosome-\nsized", AMBER)]:
        ax.plot([a0], [stokes_einstein(a0, eta_effective(a0))], "o", ms=8,
                color=c, zorder=5)
        ax.annotate(lab, (a0, stokes_einstein(a0, eta_effective(a0))),
                    textcoords="offset points", xytext=(6, -18), fontsize=9,
                    color=INK, linespacing=1.3)

    t_cross = 1.0 ** 2 / (2 * stokes_einstein(a, eta_effective(a)))
    bx.loglog(a, t_cross, lw=2.6, color=TEAL)
    bx.loglog(a, 1.0 / (2 * stokes_einstein(a, 1.0)), lw=2.2, color=MUTED,
              ls="--")
    for a0, lab, c in [(2.3, "GFP\n~65 ms", CYAN),
                       (10, "ribosome\n~2 s", AMBER)]:
        y = 1.0 / (2 * stokes_einstein(a0, eta_effective(a0)))
        bx.plot([a0], [y], "o", ms=8, color=c, zorder=5)
        bx.annotate(lab, (a0, y), textcoords="offset points", xytext=(8, -6),
                    fontsize=9, color=INK, linespacing=1.3)
    bx.set_xlabel("probe radius  (nm)")
    bx.set_ylabel("time to cross 1 µm  (s)")
    bx.set_title("Thirty-five times slower, not four")
    bx.grid(True, which="both", lw=0.5, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f"{OUT}/s02_size_dependence.png")
    plt.close(fig)


def fig_confinement():
    """Apparent subdiffusion from geometry alone -- no anomalous physics."""
    rng = np.random.default_rng(2026)          # fixed: a figure must repeat
    n_walk, n_step, dt, D = 400, 4000, 1e-3, 7.7
    step = np.sqrt(2 * D * dt)
    half = 0.4                                  # confine to +/- 0.4 um

    free = np.cumsum(rng.normal(0, step, (n_walk, n_step)), axis=1)

    conf = np.zeros((n_walk, n_step))
    x = np.zeros(n_walk)
    for i in range(n_step):
        x = x + rng.normal(0, step, n_walk)
        x = np.clip(x, -half, half)             # reflect at the wall
        conf[:, i] = x

    tau = np.geomspace(1, n_step // 4, 40).astype(int)
    def msd(tr):
        return np.array([np.mean((tr[:, k:] - tr[:, :-k]) ** 2) for k in tau])

    t = tau * dt
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.loglog(t, msd(free), lw=2.4, color=TEAL, label="unconfined")
    ax.loglog(t, msd(conf), lw=2.4, color=AMBER, label="same walk, in a box")
    ax.loglog(t, 2 * D * t, lw=1.3, color=MUTED, ls=":", label=r"$2Dt$  ($\alpha = 1$)")

    lo = t < 3e-2
    alpha = np.polyfit(np.log(t[lo]), np.log(msd(conf)[lo]), 1)[0]
    hi = t > 3e-1
    alpha_hi = np.polyfit(np.log(t[hi]), np.log(msd(conf)[hi]), 1)[0]
    ax.text(1.15e-3, 11.0,
            f"short window:  α ≈ {alpha:.2f}      "
            f"long window:  α ≈ {max(alpha_hi, 0):.2f}  (plateau)",
            fontsize=10, color=INK, va="top")
    ax.text(1.15e-3, 5.2,
            "Every step of this walk is ordinary diffusion.\n"
            "The apparent anomaly is the wall — and 0.75 is what\n"
            "the 2025 measurement reports for large particles.",
            fontsize=9.5, color=RED, style="italic", va="top",
            linespacing=1.6)

    ax.set_xlabel("lag time  (s)")
    ax.set_ylabel("mean square displacement  (µm²)")
    ax.set_title("Confinement looks like subdiffusion")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, which="both", lw=0.5, alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{OUT}/s02_confinement.png")
    plt.close(fig)




# --- growth as a removal term ------------------------------------------------
# Doubling times, E. coli, 37 C. Rich defined medium ~20-25 min; glucose
# minimal ~60 min; poor carbon source / slow chemostat, hours. The point of
# putting three on one axis is that the CEILING moves with the medium, so the
# slowest dynamics a circuit can express is set by the growth condition and not
# by the designer.
T_DOUBLE = [(20.0, "rich"), (40.0, "glucose minimal"), (90.0, "poor carbon")]

# Degradation-tag half-lives. Reported values scatter badly and depend on the
# tag, on protease load, and on the medium the measurement was made in:
# Gfp(LVA) and Gfp(LAA) come out at ~40 min after a shift from rich to minimal
# medium without inducer (Andersen et al., Appl Environ Microbiol 64:2240-2246,
# 1998; BNID 105186), which is a near-starvation condition and therefore NOT a
# clean degradation rate. Strong tags in fast growth are faster. The figure
# deliberately plots the whole axis rather than asserting one number.
TAG_BAND = (5.0, 60.0)      # min, the range worth believing


def effective_half_life(t_deg_min, t_double_min):
    """Half-life of a protein removed by degradation AND dilution.

    Removal rates add:  mu + gamma,  with mu = ln2/Td and gamma = ln2/tau_deg,
    so the half-lives combine like resistors in parallel:

        tau_eff = (Td * tau_deg) / (Td + tau_deg)   <=   Td

    which is the whole point: the doubling time is a CEILING. No tag, no
    promoter, no protein chemistry gets you above it.
    """
    t_deg = np.asarray(t_deg_min, dtype=float)
    return (t_double_min * t_deg) / (t_double_min + t_deg)


def fig_dilution():
    """Growth is a removal term. Two panels: it happens, and it is a ceiling."""
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.4, 4.3))

    # -- A: switch the promoter off and watch, rich medium ---------------------
    Td = 20.0
    t = np.linspace(0, 100, 400)
    for k in range(1, 5):                      # divisions, as tick marks
        ax.axvline(k * Td, lw=0.8, color=MUTED, alpha=0.35, zorder=0)
    ax.text(Td * 4 - 1.5, 0.035, "one division", fontsize=8.5, color=MUTED,
            ha="right", va="bottom", rotation=90)
    for t_deg, c, lab, dy in [
            (np.inf, TEAL, "no tag — dilution only", 10),
            (10.0, AMBER, "strong tag, $\\tau_{deg}$ = 10 min", -20)]:
        tau = effective_half_life(t_deg, Td) if np.isfinite(t_deg) else Td
        ax.plot(t, 2 ** (-t / tau), lw=2.6, color=c, label=lab)
        ax.plot([tau], [0.5], "o", ms=7, color=c, zorder=5)
        ax.annotate(f"{tau:.1f} min", (tau, 0.5), textcoords="offset points",
                    xytext=(9, dy), fontsize=11, color=c, weight="bold")
    ax.axhline(0.5, lw=0.9, ls=":", color=MUTED)
    ax.set_xlabel("time after the promoter is switched off  (min)")
    ax.set_ylabel("concentration, relative")
    ax.set_title("A perfectly stable protein still disappears")
    ax.set_ylim(0, 1.02)
    ax.set_xlim(0, 100)
    ax.legend(fontsize=9.5, loc="upper right", framealpha=0.95)
    ax.grid(True, lw=0.5, alpha=0.3)

    # -- B: the ceiling, and that it moves with the medium ---------------------
    td = np.geomspace(1, 3000, 300)
    for Td, name in T_DOUBLE:
        bx.loglog(td, effective_half_life(td, Td), lw=2.4,
                  label=f"{name},  $T_d$ = {Td:.0f} min")
        bx.axhline(Td, lw=0.9, ls=":", color=MUTED)
    bx.axvspan(*TAG_BAND, color=AMBER, alpha=0.12, lw=0)
    bx.text(np.sqrt(TAG_BAND[0] * TAG_BAND[1]), 1.35,
            "where tags\nput you", fontsize=9, color=AMBER, ha="center",
            weight="bold", linespacing=1.4)
    bx.text(2600, 115, "ceiling = $T_d$", fontsize=10, color=INK, ha="right",
            style="italic")
    bx.set_xlabel("degradation half-life you engineer,  $\\tau_{deg}$  (min)")
    bx.set_ylabel("half-life you actually get  (min)")
    bx.set_title("You can go faster. You cannot go slower.")
    bx.set_ylim(1, 200)
    bx.legend(fontsize=9, loc="lower right")
    bx.grid(True, which="both", lw=0.5, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f"{OUT}/s02_dilution.png")
    plt.close(fig)


FIGURES = [fig_copy_number, fig_timescales, fig_size_dependence,
           fig_confinement, fig_dilution]
