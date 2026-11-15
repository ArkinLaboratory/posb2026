# `posb`

[← back to the repository root](../README.md) · [API reference](../docs/posb-reference.md)

A deliberately small package for building and simulating reaction networks.
Plain NumPy and SciPy: no hidden solver, no symbolic engine, no simulation
framework.

**Design rule:**

> Nothing here is abstracted away before it has been built by hand in class.

| File | Introduced | Contents |
|---|---|---|
| `core.py` | Session 3 | `Reaction`, `Model`, `Trajectory` — builds **S**, integrates d**x**/d*t* = **S·v** |
| `data.py` | Session 5 | synthetic decay and induction timecourses, seeded |
| `analysis.py` | Sessions 8, 11 | nullclines, fixed points, Jacobian, linear stability, the toggle bifurcation, the repressilator and its Hopf boundary |
| `stochastic.py` | Session 12 | Gillespie SSA, time-weighted averages, Fano and CV |
| `digital.py` | Session 13 | transfer curves, log gain, unity-gain thresholds, noise margins |
| `logic.py` | Session 16 | truth tables, NOR networks, timing tables, hazards |
| `assembly.py` | Session 17 | Golden Gate overhangs, distinguishability, the published sets with their measured fidelity |
| `protein.py` | Session 18 | covalent modification cycles, zero-order ultrasensitivity |
| `resources.py` | Session 19 | competition for a shared translational pool, the isocost line |
| `fba.py` | Session 20 | flux balance analysis as a linear program, vertex solutions, alternate optima |
| `retroactivity.py` | Session 21 | what a downstream load costs its driver, and why weakening the operator buys nothing |
| `control.py` | Session 22 | antithetic integral feedback, the set point as a ratio, and the two limits where it fails |
| `evolution.py` | Session 23 | burden as a selection coefficient, the exact failure time |
| `communities.py` | Session 24 | diffusion time and penetration depth, Basu's band detector, the predator-prey chemostat and its Hopf |
| `populations.py` | Session 25 | diploid packaging, heterozygote waste, the vector's reproductive ratio |
| `classifiers.py` | Session 26 | a classifier as a threshold on a product of sensor responses, the marker senses carried explicitly, confusion over a cell-line panel, and a false-positive budget in wrong cells |
| `__init__.py` | — | exports, plus `check_environment()` |

`core.py` is about 250 lines including docstrings, and `Model._build_S` — the
function that turns a reaction list into a stoichiometric matrix — is nine of
them. Reading it is faster than reading the reference page, and is the intended
way to use this library.
