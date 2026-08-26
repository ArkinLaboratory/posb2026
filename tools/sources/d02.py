"""Demo 2 — crowding. A classroom demo, not an assignment.

Two claims, each with a prediction taken before anything runs. A simulation
students watch is a slide that moves; a simulation they have committed a number
to first is a ConcepTest with better feedback.
"""
from .common import md, code, header, SETUP

REL = "demos/d02-crowding/d02_crowding.ipynb"
TITLE = "Demo 2 — Crowding"
SUBTITLE = "Two things a single diffusion coefficient will not tell you"
DATE = "for Session 2"

CELLS = [
    header(TITLE, SUBTITLE, DATE, REL),

    md("""This is a **classroom demo**. Nothing here is graded and nothing is
submitted. It is meant to be driven live, and the two prediction prompts are
the point — if you scroll past them to the answer, the demo has done nothing
for you that a static figure would not have done.

Both claims come out of one recent measurement:

> Valverde-Mendez, Sunol, Bratton, Delarue, Hofmann, Sheehan, Gitai, Holt,
> Shaevitz & Zia. **Macromolecular interactions and geometrical confinement
> determine the 3D diffusion of ribosome-sized particles in live *Escherichia
> coli* cells.** *PNAS* **122**(4), e2406340121 (2025).
> [doi:10.1073/pnas.2406340121](https://doi.org/10.1073/pnas.2406340121)

They tracked 20–50 nm particles in three dimensions inside living cells, and
built a whole-cell colloidal simulation to see what happens on timescales the
microscope cannot reach."""),

    code(SETUP),

    md("""---
# Claim 1 · The cytoplasm does not have *a* viscosity

In lecture we used one number: $D = 7.7\\ \\mathrm{\\mu m^2/s}$ for GFP, about
**11×** slower than the same protein in water.

A ribosome is bigger — radius about 10 nm against GFP's 2.3.

## Predict first

Stokes–Einstein says $D = k_BT / 6\\pi\\eta a$, so if the cytoplasm were a fluid
with one viscosity, a 4× bigger particle would diffuse **4× slower**.

**Write down your prediction before running the next cell.** How much slower
than GFP does a ribosome-sized particle actually cross the cell?"""),

    code('''import numpy as np
import matplotlib.pyplot as plt

KT, ETA_WATER = 4.14e-21, 1e-3          # J at 300 K;  Pa s

def stokes_einstein(a_nm, eta_cP):
    """D in um^2/s for a sphere of radius a_nm in a fluid of viscosity eta_cP."""
    return KT / (6 * np.pi * eta_cP * ETA_WATER * a_nm * 1e-9) * 1e12

def crossing_time(a_nm, eta_cP, L_um=1.0):
    """t ~ L^2 / 2D, the one-dimensional convention -- as always, stated."""
    return L_um ** 2 / (2 * stokes_einstein(a_nm, eta_cP))

# The two measurements. Effective viscosity is what the CELL looks like
# to a probe of that size -- water is 1 cP.
GFP      = dict(a_nm=2.3, eta_cP=12.0)    # Elowitz et al. 1999
RIBOSOME = dict(a_nm=10.0, eta_cP=100.0)  # Valverde-Mendez et al. 2025

for name, p in [("GFP", GFP), ("ribosome-sized", RIBOSOME)]:
    print(f"{name:<16} a = {p['a_nm']:>4} nm   eta_eff = {p['eta_cP']:>5.0f} cP"
          f"   D = {stokes_einstein(**p):8.3f} um^2/s"
          f"   crosses 1 um in {crossing_time(**p):7.3f} s")

naive = crossing_time(RIBOSOME["a_nm"], GFP["eta_cP"])
print(f"\\nIf the cell had ONE viscosity, the ribosome would take {naive:.3f} s")
print(f"It actually takes                                     "
      f"{crossing_time(**RIBOSOME):.3f} s")
print(f"\\nRatio to GFP:  naive {naive/crossing_time(**GFP):.1f}x"
      f"   measured {crossing_time(**RIBOSOME)/crossing_time(**GFP):.0f}x")'''),

    md("""## What just happened

Four times bigger, but **thirty-five times slower** — not four.

The effective viscosity is not a property of the cytoplasm. It is a property of
the cytoplasm *and the probe*: a small protein slips between obstacles that a
ribosome has to push past. There is no single number you can write down for
"the viscosity of cytoplasm" and use for everything.

**Why it matters for design.** Anything you build out of large complexes —
ribosomes, polymerases, assembled multi-protein machines — moves seconds, not
milliseconds. If a circuit's function depends on a large object getting
somewhere before something else happens, the timescale you estimated from a
fluorescent protein is optimistic by more than an order of magnitude."""),

    md("""---
# Claim 2 · Confinement looks exactly like anomalous physics

Track a particle in a cell and plot mean square displacement against lag time.
Ordinary diffusion gives $\\langle x^2\\rangle = 2Dt$ — a slope of 1 on log axes.

The 2025 measurements give slopes of **0.75** for large particles and **0.45**
for small ones. That is *sub*diffusion, and for years it was read as evidence
that the cytoplasm is a strange, glassy, non-Newtonian material.

## Predict first

Below is a plain random walk. Every step is drawn from a normal distribution,
which is ordinary diffusion by construction — there is no anomalous physics
anywhere in the code.

The only thing we will do is **put a wall on it**, one cell-radius away.

**Predict:** what slope will the confined walk show?"""),

    code('''rng = np.random.default_rng(2026)      # fixed seed: a demo has to repeat
n_walk, n_step, dt, D = 400, 4000, 1e-3, 7.7
step, half = np.sqrt(2 * D * dt), 0.4  # half = half a cell, in um

free = np.cumsum(rng.normal(0, step, (n_walk, n_step)), axis=1)

conf, x = np.zeros((n_walk, n_step)), np.zeros(n_walk)
for i in range(n_step):
    x = np.clip(x + rng.normal(0, step, n_walk), -half, half)   # the wall
    conf[:, i] = x

tau = np.geomspace(1, n_step // 4, 40).astype(int)
msd = lambda tr: np.array([np.mean((tr[:, k:] - tr[:, :-k]) ** 2) for k in tau])
t = tau * dt

short = t < 3e-2
for name, tr in [("unconfined", free), ("confined", conf)]:
    a = np.polyfit(np.log(t[short]), np.log(msd(tr)[short]), 1)[0]
    print(f"{name:<12} apparent alpha over a short window = {a:.2f}")'''),

    code('''fig, ax = plt.subplots(figsize=(7, 4.2))
ax.loglog(t, msd(free), lw=2.4, label="unconfined")
ax.loglog(t, msd(conf), lw=2.4, label="same walk, in a box")
ax.loglog(t, 2 * D * t, lw=1.2, ls=":", color="0.5", label=r"$2Dt$")
ax.set_xlabel("lag time (s)"); ax.set_ylabel(r"MSD ($\\mu$m$^2$)")
ax.legend(); ax.grid(True, which="both", lw=0.5, alpha=0.3)
plt.show()'''),

    md("""## What just happened

The confined walk reports an apparent exponent of about **0.75** — the same
number the 2025 paper reports for large particles — and there is no anomalous
physics in the code at all. Every step is ordinary diffusion.

The paper makes exactly this argument, and with better evidence than a toy
walk: their simulations resolve timescales shorter than the microscope can,
and there the exponent goes back above 0.84. **The apparent subdiffusion is
produced by the boundaries** — the nucleoid, which excludes large particles,
and the cell wall — not by the medium being strange.

They also see particles sort themselves by size: a 20 nm particle spends about
60% of its time inside the nucleoid, a 50 nm particle about 30%, and a
positively charged one about 25%. The cell has spatial structure that your
well-mixed model does not."""),

    md("""---
## The habit, again

Both halves of this demo are the same move:

1. A measurement disagrees with the simple model.
2. The disagreement is not noise and not a mistake in the arithmetic.
3. Chasing it produces a mechanism — size-dependent effective viscosity in the
   first case, geometric confinement in the second.

**And note what did *not* happen.** Nobody needed anomalous-diffusion theory to
explain an anomalous-looking exponent. The first thing to check, when a
measurement looks exotic, is whether something boring and geometric produces
the same signature.

**What we keep for the rest of the course.** A single $D$ and $t \\sim L^2/2D$
is a perfectly good first estimate, and we will use it all term — as long as
you say that is what you are doing, and know which direction it is wrong in."""),
]
