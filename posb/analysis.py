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
        # Tolerance, not rounding: two solves of the same root that straddle a
        # rounding boundary (6.7341635 vs 6.7341634) used to count as two fixed
        # points. Seen on the Gardner 2000 pTAK117 parameters, 18 Sep 2026.
        if not any(np.allclose(sol, f, atol=10.0 ** -decimals, rtol=0)
                   for f in found):
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


# ---------------------------------------------------------------------------
# The repressilator, and its oscillation condition          (session 11)
# ---------------------------------------------------------------------------

def repressilator_model(alpha=None, n=3):
    """The symmetric three-gene repressor ring, in scaled form.

        dx_i/dt = alpha / (1 + x_{i-1}**n) - x_i,     i = 1, 2, 3

    Same scaling as `toggle_model`: time in protein lifetimes, concentration in
    units of the repression threshold, so only `alpha` and the cooperativity
    `n` survive. Built here because sessions 11 and 22 both need it.

    This is Elowitz & Leibler's circuit with the mRNA step folded away. The
    real device has six variables and a translational delay; dropping to three
    keeps the geometry (a cyclic Jacobian) and therefore the criterion, and it
    is what the class derives by hand.
    """
    from .core import Reaction, Model

    a = 10.0 if alpha is None else alpha
    # max(x, 0) for the same reason as toggle_model: the root finder probes
    # negative concentrations and a negative base to a fractional power is NaN.
    ring = [("x1", "x3"), ("x2", "x1"), ("x3", "x2")]
    rxns = []
    for target, repressor in ring:
        rxns.append(Reaction(
            {}, {target: 1},
            rate=lambda c, p, r=repressor: p["alpha"] / (1 + max(c[r], 0.0) ** p["n"]),
            name=f"synthesis of {target}, repressed by {repressor}"))
        rxns.append(Reaction({target: 1}, {}, k=1.0, name=f"removal of {target}"))

    return Model(rxns, params={"alpha": a, "n": n},
                 species=["x1", "x2", "x3"])


def loop_gain(alpha, n):
    """Gain around the ring at the symmetric fixed point.

        g = n * x**n / (1 + x**n),    where x solves  x (1 + x**n) = alpha

    Each repression contributes |df/dx| at the operating point; `g` is that
    quantity, and it is the number the oscillation criterion is stated in.
    """
    from scipy.optimize import brentq

    x = brentq(lambda y: y * (1 + y ** n) - alpha, 1e-12, max(alpha, 1.0) + 1.0)
    return n * x ** n / (1 + x ** n)


def repressilator_alpha_critical(n):
    """Smallest alpha that makes the symmetric three-gene ring oscillate.

        alpha_c = (2 / (n - 2))**(1/n) * n / (n - 2),     valid for n > 2

    Derivation, which is the session 11 worked example.

    At the symmetric fixed point x1 = x2 = x3 = x,

        x = alpha / (1 + x**n)        so     alpha = x (1 + x**n)

    The Jacobian there is  J = -I - g P,  where P is the cyclic permutation
    that sends each gene to the one it represses and

        g = alpha n x**(n-1) / (1 + x**n)**2 = n x**n / (1 + x**n).

    P's eigenvalues are the cube roots of unity, so J's are

        lambda_k = -1 - g * omega_k,    omega_k = 1, e^(2 pi i / 3), e^(-2 pi i / 3).

    The real root is -1 - g < 0 always. The complex pair has real part
    -1 + g/2, so the fixed point loses stability exactly when

        **g = 2**

    -- a Hopf bifurcation, and the criterion this session exists to produce.
    Solving g = 2 for x gives x**n = 2 / (n - 2), hence the alpha above, and it
    is infinite for n <= 2: **a ring of three with no cooperativity cannot
    oscillate, no matter how strong the promoters.**

    Compare `toggle_alpha_critical`: the toggle needs n > 1, this ring needs
    n > 2. Adding a gene to the loop made the cooperativity requirement
    harder, not easier.

    ⚠ TWO CAVEATS, both of which matter when teaching this.

    1. SIGN CONVENTION. `toggle_alpha_critical` defines its coupling with the
       derivative's own sign (negative) and then uses the magnitude;
       here `g` is defined positive from the start. Same letter, opposite
       sign, two sessions apart. If you are comparing the two derivations,
       compare |g|.
    2. n > 2 IS A PROPERTY OF THIS THREE-VARIABLE REDUCTION, not of
       repressilators. Folding away mRNA is the worst case. Elowitz &
       Leibler keep the mRNA step, and their Fig. 1b shows an unstable
       region at n = 2 -- which is where they put their own design. Do not
       tell students a ring of three "cannot oscillate at n = 2"; tell them
       OUR model says so, and that keeping mRNA relaxes it.
    """
    if n <= 2:
        return float("inf")
    return (2.0 / (n - 2)) ** (1.0 / n) * n / (n - 2)


def sweep(model, param, values, quantity, params=None):
    """Evaluate `quantity` across a one-parameter sweep. Returns a list.

    `quantity(model, params)` is called once per value with `param` set to it,
    and whatever it returns is collected. This is deliberately thin -- it is a
    for-loop with the bookkeeping done once -- because the point of the session
    is that the student writes the loop first and imports it afterwards.

        >>> sweep(repressilator_model(n=3), "alpha", [2.0, 4.0], leading_real_part)
        [-0.25, 0.0186]

    (At alpha = 2, n = 3 the fixed point is exactly x = 1, so g = 3/2 and
    Re lambda = -1 + g/2 = -0.25. At alpha = 4 it has just crossed.)
    """
    out = []
    for v in values:
        p = {**(params or {}), param: v}
        out.append(quantity(model, p))
    return out


def leading_real_part(model, params=None, guess=None):
    """Largest real part of the Jacobian eigenvalues at the fixed point.

    Positive means the steady state is unstable, so the system leaves it. For
    the repressilator that is the oscillation test, and sweeping this across
    alpha is how session 11 locates the Hopf boundary numerically.
    """
    if guess is None:
        guess = {s: 1.0 for s in model.species}
    pts = fixed_points(model, [[guess[s] for s in model.species]], params)
    if not pts:
        return float("nan")
    J = jacobian(model, pts[0], params)
    return float(np.max(np.linalg.eigvals(J).real))


def hopf_boundary(model, param, lo, hi, params=None, tol=1e-10):
    """Bisect for the parameter value where the fixed point loses stability.

    Returns the value of `param` at which `leading_real_part` crosses zero.
    Raises if the interval does not bracket a crossing, which is the honest
    failure: if both ends are stable there is no boundary in between.
    """
    from scipy.optimize import brentq

    def f(v):
        return leading_real_part(model, {**(params or {}), param: v})

    if f(lo) * f(hi) > 0:
        raise ValueError(
            f"{param} = {lo} and {hi} are both on the same side of the "
            f"boundary (leading real parts {f(lo):.3g} and {f(hi):.3g}); "
            f"widen the bracket")
    return brentq(f, lo, hi, xtol=tol)
