"""
posb.analysis — nullclines, fixed points, stability, and bifurcation.

Introduced in Session 8. Everything here is done by hand in class first:
you find nullclines by setting derivatives to zero, you find fixed points by
root-finding, you build the Jacobian by differentiating, and you classify by
looking at eigenvalues. This module removes the bookkeeping, not the ideas.

Nothing here is more than a thin wrapper on `scipy.optimize` and
`numpy.linalg`. Read the source.
"""

import numpy as np
from scipy.optimize import brentq, fsolve

__all__ = [
    "nullcline",
    "fixed_points",
    "jacobian",
    "classify",
    "stability_report",
    "toggle_model",
    "toggle_alpha_critical",
]


# ---------------------------------------------------------------------------
# Nullclines
# ---------------------------------------------------------------------------

def nullcline(model, species, along, grid, params=None, bracket=(1e-9, 1e4)):
    """Solve d[species]/dt = 0 for `species` as `along` is swept over `grid`.

    Parameters
    ----------
    model : posb.Model
    species : str
        The species whose derivative is set to zero.
    along : str
        The species swept over `grid`.
    grid : array
        Values of `along` to sweep.
    params : dict, optional
    bracket : (lo, hi)
        Bracket for the root in `species`. Widen it if you get NaNs.

    Returns
    -------
    array, same length as `grid`. NaN where no sign change was bracketed.

    Notes
    -----
    Only valid for a 2-species system, and only where the nullcline is a
    function of `along` (one root per value). For anything more general, plot
    the sign of the derivative on a mesh and contour it at zero.
    """
    i = model.species.index(species)
    other = [s for s in model.species if s != species]
    if len(other) != 1:
        raise ValueError("nullcline() expects a 2-species model; "
                         f"this one has {len(model.species)}")
    if along != other[0]:
        raise ValueError(f"`along` must be {other[0]!r} for species={species!r}")

    def f(x, a):
        state = {species: x, along: a}
        return model.rhs(0.0, [state[s] for s in model.species], params)[i]

    out = np.full(len(grid), np.nan)
    lo, hi = bracket
    for k, a in enumerate(np.asarray(grid, dtype=float)):
        try:
            if f(lo, a) * f(hi, a) > 0:
                continue
            out[k] = brentq(f, lo, hi, args=(a,), xtol=1e-12)
        except (ValueError, RuntimeError):
            continue
    return out


# ---------------------------------------------------------------------------
# Fixed points
# ---------------------------------------------------------------------------

def fixed_points(model, guesses, params=None, tol=1e-8, decimals=6):
    """Find fixed points by root-finding from a list of initial guesses.

    Unlike integrating forward, this finds **unstable** fixed points too --
    which is the whole reason session 8 replaces `Model.steady_state`. The
    saddle in a toggle switch is the object that defines the separatrix, and
    no amount of forward integration will ever land on it.

    Returns a list of dicts, deduplicated.
    """
    found = []
    for g in guesses:
        x0 = np.array([g[s] for s in model.species] if isinstance(g, dict)
                      else g, dtype=float)
        sol, info, ier, _ = fsolve(
            lambda x: model.rhs(0.0, x, params), x0, full_output=True)
        if ier != 1:
            continue
        if np.max(np.abs(model.rhs(0.0, sol, params))) > tol:
            continue
        if np.any(sol < -tol):          # negative concentrations are not physical
            continue
        key = tuple(np.round(sol, decimals))
        if key not in [tuple(np.round(f, decimals)) for f in found]:
            found.append(sol)
    found.sort(key=lambda v: tuple(v))
    return [dict(zip(model.species, f)) for f in found]


# ---------------------------------------------------------------------------
# Linear stability
# ---------------------------------------------------------------------------

def jacobian(model, point, params=None, eps=1e-7):
    """Jacobian at `point` by central differences.

    Central rather than forward differences: the error is O(eps^2) instead of
    O(eps), which matters near a saddle where the two eigenvalues are close in
    magnitude and opposite in sign.
    """
    x = np.array([point[s] for s in model.species] if isinstance(point, dict)
                 else point, dtype=float)
    n = len(x)
    J = np.zeros((n, n))
    for j in range(n):
        h = eps * max(1.0, abs(x[j]))
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        J[:, j] = (model.rhs(0.0, xp, params) - model.rhs(0.0, xm, params)) / (2 * h)
    return J


def classify(J, tol=1e-9):
    """Classify a fixed point from its Jacobian.

    Returns (label, eigenvalues). Labels follow the usual 2-D taxonomy;
    higher dimensions collapse to 'stable' / 'unstable' / 'saddle'.
    """
    ev = np.linalg.eigvals(J)
    re = ev.real
    if np.any(np.abs(re) < tol):
        return "non-hyperbolic", ev
    if np.all(re < 0):
        base = "stable"
    elif np.all(re > 0):
        base = "unstable"
    else:
        return "saddle", ev
    if len(ev) == 2 and np.any(np.abs(ev.imag) > tol):
        return base + " spiral", ev
    return base + " node", ev


def stability_report(model, params=None, guesses=None, grid=(0.01, 20, 7)):
    """Find every fixed point on a coarse grid of guesses and classify each.

    Returns a list of {point, type, eigenvalues}, sorted by the first species.
    """
    if guesses is None:
        lo, hi, k = grid
        axes = [np.geomspace(lo, hi, k) for _ in model.species]
        mesh = np.meshgrid(*axes)
        guesses = np.column_stack([m.ravel() for m in mesh])
    out = []
    for p in fixed_points(model, guesses, params):
        J = jacobian(model, p, params)
        label, ev = classify(J)
        out.append({"point": p, "type": label, "eigenvalues": ev})
    return out


# ---------------------------------------------------------------------------
# The toggle switch, and its bifurcation condition
# ---------------------------------------------------------------------------

def toggle_model(alpha1=None, alpha2=None, n=2, m=None):
    """The Gardner-Cantor-Collins toggle, in scaled form.

        du/dt = alpha1 / (1 + v**m) - u
        dv/dt = alpha2 / (1 + u**n) - v

    Time is in units of protein lifetime and concentration in units of the
    repression threshold, so only the synthesis rates and the two cooperativity
    exponents remain. Built here rather than in a notebook because sessions 9,
    11 and 23 all need the same model.
    """
    from .core import Reaction, Model

    # max(x, 0) inside the rate laws: fsolve probes negative concentrations
    # while hunting for a root, and a negative number to a fractional power is
    # NaN. Clipping keeps the search well behaved without changing any
    # physically meaningful value.
    m = n if m is None else m
    a1 = 10.0 if alpha1 is None else alpha1
    a2 = a1 if alpha2 is None else alpha2

    return Model(
        [
            Reaction({}, {"u": 1},
                     rate=lambda c, p: p["alpha1"] / (1 + max(c["v"], 0.0) ** p["m"]),
                     name="synthesis of u, repressed by v"),
            Reaction({"u": 1}, {}, k=1.0, name="removal of u"),
            Reaction({}, {"v": 1},
                     rate=lambda c, p: p["alpha2"] / (1 + max(c["u"], 0.0) ** p["n"]),
                     name="synthesis of v, repressed by u"),
            Reaction({"v": 1}, {}, k=1.0, name="removal of v"),
        ],
        params={"alpha1": a1, "alpha2": a2, "n": n, "m": m},
        species=["u", "v"],
    )


def toggle_alpha_critical(n):
    """Smallest alpha giving bistability in the symmetric toggle.

        alpha_c = n * (n - 1) ** (-(n + 1) / n),   valid for n > 1

    Derivation (this is the session 9 worked example, and it is short).

    At a symmetric fixed point u = v = x,

        x = alpha / (1 + x**n)          so      alpha = x + x**(n+1)

    The Jacobian there is [[-1, g], [g, -1]] with

        g = -alpha * n * x**(n-1) / (1 + x**n)**2

    Using (1 + x**n) = alpha / x this collapses to |g| = n * x**(n+1) / alpha.
    Eigenvalues are -1 +/- |g|, so the symmetric point turns from a stable node
    into a saddle exactly when |g| > 1:

        n * x**(n+1) > alpha = x + x**(n+1)
        (n - 1) * x**n > 1
        x > (n - 1) ** (-1/n)

    which is impossible for n <= 1 -- **cooperativity is not a helpful extra,
    it is a necessary condition**. Substituting back into alpha = x(1 + x**n)
    gives the bound above.

    Returns np.inf for n <= 1: no alpha, however large, produces bistability.
    """
    n = float(n)
    if n <= 1:
        return np.inf
    return n * (n - 1) ** (-(n + 1) / n)
