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
| `__init__.py` | — | exports, plus `check_environment()` |

Planned: `analysis.py` (session 8), `stochastic.py` (session 12), `fba.py`
(session 20).

`core.py` is about 250 lines including docstrings, and `Model._build_S` — the
function that turns a reaction list into a stoichiometric matrix — is nine of
them. Reading it is faster than reading the reference page, and is the intended
way to use this library.
