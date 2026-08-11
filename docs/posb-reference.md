# `posb` Package Reference

[← back to README](../README.md)

Plain NumPy and SciPy. No hidden solver, no symbolic engine, no simulation
framework. `posb/core.py` is about 250 lines including docstrings — **reading
the source is faster than reading this page**, and is the intended way to use
the library.

```python
from posb import Reaction, Model, Trajectory
```

| Module | Introduced | Status | Contents |
|---|---|---|---|
| `posb.core` | Session 3 | available | `Reaction`, `Model`, `Trajectory` |
| `posb.analysis` | Session 8 | planned | nullclines, fixed points, Jacobian, stability |
| `posb.stochastic` | Session 12 | planned | Gillespie SSA |
| `posb.fba` | Session 20 | planned | flux balance analysis |

---

## `Reaction`

```python
Reaction(reactants, products, k=None, rate=None, name=None)
```

A single chemical reaction.

**`reactants`, `products`** — dicts mapping species name to stoichiometric
coefficient. `{"A": 1, "B": 2}` means A + 2B. Use `{}` for synthesis from
nothing or degradation to nothing.

**`k`** — mass-action rate constant. The flux is
`k * prod(concentration ** stoichiometry)` over the reactants. If `k` is a
**string**, it is looked up in the parameter dict at simulation time, which is
what makes parameter sweeps possible.

**`rate`** — a callable `rate(c, p) -> float` for non-mass-action kinetics,
where `c` is a dict of current concentrations keyed by species name and `p` is
the parameter dict. Give exactly one of `k` or `rate`.

**`name`** — label used in `summary()` and error messages. Defaults to a
readable form of the reaction.

```python
Reaction({"A": 1, "B": 1}, {"C": 1}, k=0.5)             # A + B -> C
Reaction({"m": 1}, {}, k="gamma")                        # m -> 0, rate from params
Reaction({"m": 1}, {"m": 1, "p": 1}, k="k_p")            # translation: m is catalytic
Reaction({}, {"X": 1},                                   # repression
         rate=lambda c, p: p["alpha"] / (1 + (c["X"] / p["K"]) ** p["n"]))
```

> **The catalytic pattern is the one to get right.** A species appearing on
> both sides has **zero** net stoichiometry. Translation does not consume the
> mRNA. Writing `Reaction({"m": 1}, {"p": 1}, ...)` instead is the single most
> common modelling error in the first two weeks of the course.

### Methods

| | |
|---|---|
| `.species()` | set of every species the reaction touches |
| `.flux(c, p)` | reaction velocity at concentrations `c` (dict) with params `p` |

---

## `Model`

```python
Model(reactions, params=None, species=None)
```

A reaction network. Builds the stoichiometric matrix **S** once at
construction, then evaluates d**x**/d*t* = **S·v**(**x**, *p*).

**`reactions`** — list of `Reaction`.
**`params`** — default parameter values; overridable per simulation.
**`species`** — fixes the species ordering, and therefore the row order of
**S**. If omitted, species are sorted alphabetically so results are
reproducible.

### Attributes

| | |
|---|---|
| `.S` | stoichiometric matrix, shape `(n_species, n_reactions)`. `S[i, j]` is the **net** stoichiometry of species *i* in reaction *j*. |
| `.species` | ordered list of species names (the row order of `S`) |
| `.reactions` | the reaction list (the column order of `S`) |
| `.params` | default parameter dict |

### Methods

#### `.simulate(x0, t_span, params=None, n_points=400, **kwargs)`

Integrate. Returns a [`Trajectory`](#trajectory).

`x0` may be a dict (species may be omitted; they start at zero) or an array in
`.species` order. Extra keyword arguments pass straight through to
`scipy.integrate.solve_ivp`.

Defaults: `method="LSODA"`, `rtol=1e-8`, `atol=1e-10`.

> **A caveat about `LSODA`.** It switches automatically between stiff and
> non-stiff solvers, which is convenient and is also the one place this package
> hides something from you. If you are studying a system where stiffness
> matters, pass `method="RK45"` and watch it struggle — that is instructive.

#### `.steady_state(x0, params=None, t_max=1e6, **kwargs)`

Integrate a long time; return the final state as a dict.

This is the lazy way to find a steady state, and it has two real limitations:
it only finds **stable** fixed points, and only the one whose basin of
attraction contains `x0`. Session 8 replaces it with actual root-finding, which
finds unstable fixed points too — and unstable fixed points are exactly what
you need for the toggle switch in session 9.

#### `.fluxes(x, p=None)`

The flux vector **v** at state `x`. Useful on its own for checking a model.

#### `.rhs(t, x, p=None)`

Right-hand side d**x**/d*t*. Signature matches `solve_ivp`, so you can pass it
directly to any integrator you like.

#### `.summary()`

Human-readable description of the network and its **S** matrix. Print this
whenever a model is not doing what you expect — most modelling bugs are
stoichiometry bugs and they are visible here.

```
Model: 2 species, 4 reactions
  species: mRNA, protein
  reactions:
    v0: transcription
    v1: mRNA decay
    v2: translation
    v3: protein decay
  S =
                v0    v1    v2    v3
     mRNA |     1    -1     0     0
  protein |     0     0     1    -1
```

The zero in the mRNA row under `v2` is the catalytic pattern, visible.

---

## `Trajectory`

Returned by `Model.simulate()`.

| | |
|---|---|
| `traj["mRNA"]` | time course of one species, as a 1-D array |
| `traj.t` | time vector |
| `traj.y` | raw `(n_species, n_times)` array in `traj.species` order |
| `traj.species` | ordered species names |
| `traj.final()` | concentrations at the last time point, as a dict |
| `traj.as_dict()` | every time course, as a dict of arrays |

Access by name rather than by index. Row-order mistakes are silent and
expensive; `KeyError` is neither.

---

## `check_environment(verbose=True)`

Reports Python and library versions and detects whether you are on DataHub,
Colab, or elsewhere. Returns a dict. Every notebook calls it in the setup cell.

---

## Performance

`Model.rhs` costs about **4 µs** per evaluation — it rebuilds a concentration
dict and runs a Python-level loop over reactions each time.

| Use | Cost | Verdict |
|---|---|---|
| One `solve_ivp` run (~5,000 evaluations) | ~20 ms | fine |
| Gillespie, 10⁵ steps | ~0.4 s | acceptable |
| Gillespie, 10⁶ steps | ~4 s | too slow |

Deterministic simulation is never the bottleneck. Stochastic simulation is, and
`posb.stochastic` will therefore precompute stoichiometry into arrays and close
over them rather than reusing `Model.rhs`. If you are writing your own
ensemble code over many trajectories, do the same.

---

## Design rule

> **Nothing in `posb` is abstracted away before it has been built by hand in class.**

Every notebook that first uses a new abstraction proves numerically that it
agrees with the hand-written version — see
[Session 3](../sessions/s03-modeling-i/) for the pattern, and
[Design Notes](design-notes.md) for why.
