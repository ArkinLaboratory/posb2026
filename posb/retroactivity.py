"""Session 21. Retroactivity: what a downstream load costs the module driving it.

A transcription factor X is produced and removed. Downstream, `p_tot` operator
sites bind it:  X + p <-> C,  with K_d = k_off/k_on. The circuit diagram draws
an arrow from X to the downstream module; the arrow is wrong about the physics,
because an operator site is a molecule that *holds* X.

Two models, and the difference is whether the sequestered molecule is still
being removed:

    CONSERVATIVE  the complex is not degraded or diluted.
    DILUTED       the complex is removed at the same rate as free X. This is
                  the growing cell, and it is the physical case.

The results below are derived, integrated and swept in
`sessions/s21-retroactivity/NUMBERS.md`. Three of them are worth stating here
because they are the session's argument and they are easy to get backwards:

1.  CONSERVATIVE leaves the steady state of free X EXACTLY untouched. The
    binding flux is zero at steady state, so the load term drops out of dX/dt.

2.  DILUTED pins the TOTAL:  X + C = k/gamma exactly. Free X therefore falls by
    precisely the number of molecules parked on the sites.

3.  The SPEED cost is affinity-blind in the CONSERVATIVE model, by a
    conservation identity: the integral of R over all X is C(inf) - C(0) =
    p_tot exactly, whatever K_d is, because the target never moves. In the
    DILUTED model the endpoint itself moves with K_d, so the speed cost is NOT
    flat -- it falls about 20% over three decades.
4.  The LEVEL cost exists in the diluted model only, and is (p_tot / X_T) times
    the site OCCUPANCY. It is therefore affinity-DEPENDENT, and it is never
    "exactly p_tot / X_T".
    See sessions/s21-retroactivity/REBUILD.md, which supersedes NUMBERS.md
    sections 4-6, for both.
5.  Weakening the operator escapes the load only by emptying the sites, and an
    empty operator regulates nothing. The load is the price of the regulation.

There is no hidden solver here. Everything is NumPy and SciPy. Read the source.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

__all__ = [
    "retroactivity",
    "loaded_rhs",
    "simulate_load",
    "steady_state",
    "response_half_time",
    "slowdown",
    "level_shift",
    "affinity_is_irrelevant",
]


def retroactivity(x, p_tot, K_d):
    """R(x) = p_tot * K_d / (K_d + x)**2 -- the retroactivity term.

    The slow-manifold reduction of the loaded system is

        dX/dt = f(X) / (1 + R(X))

    so R is a dimensionless, state-dependent *slowdown*: it never changes where
    f(X) = 0, only how fast the module gets there. Verified against the full
    binding kinetics to 2e-7 in NUMBERS.md section 2.

    R is largest at x = 0 (R(0) = p_tot/K_d) and falls as x**-2 once x >> K_d,
    so most of the slowing happens during the *approach*, while the sites are
    still empty and greedy -- not at the operating point.
    """
    x = np.asarray(x, dtype=float)
    if np.any(x < 0):
        raise ValueError("x must be non-negative")
    if p_tot < 0:
        raise ValueError("p_tot must be non-negative")
    if K_d <= 0:
        raise ValueError("K_d must be positive")
    return p_tot * K_d / (K_d + x) ** 2


def loaded_rhs(t, y, k, gamma, k_on, k_off, p_tot, complex_decays):
    """Full binding kinetics, no quasi-steady-state assumption.

    State is (X, C): free transcription factor and bound complex. Free sites are
    p_tot - C, so the model carries site conservation rather than assuming it.

    `complex_decays` selects the model: False is CONSERVATIVE, True is DILUTED.
    """
    X, C = y
    free_sites = p_tot - C
    binding = k_on * X * free_sites - k_off * C
    dX = k - gamma * X - binding
    dC = binding - (gamma * C if complex_decays else 0.0)
    return [dX, dC]


def _solve(k, gamma, K_d, p_tot, complex_decays, k_on=None, t_end_lifetimes=6000.0):
    if K_d <= 0:
        raise ValueError("K_d must be positive")
    # Binding must be fast against gamma for the slow-manifold picture to hold.
    if k_on is None:
        k_on = max(1e4 * gamma / K_d, 1e4 * gamma)
    k_off = k_on * K_d
    t_end = t_end_lifetimes / gamma
    sol = solve_ivp(
        loaded_rhs, (0.0, t_end), [0.0, 0.0],
        args=(k, gamma, k_on, k_off, p_tot, complex_decays),
        rtol=1e-12, atol=1e-14, method="LSODA", dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(f"integration failed: {sol.message}")
    return sol, t_end


def simulate_load(k, gamma, K_d, p_tot, complex_decays=True, t_end_lifetimes=6000.0):
    """Integrate the loaded system from zero. Returns the solve_ivp solution."""
    return _solve(k, gamma, K_d, p_tot, complex_decays,
                  t_end_lifetimes=t_end_lifetimes)[0]


def steady_state(k, gamma, K_d, p_tot, complex_decays=True):
    """Return (X_ss, C_ss) for the loaded system, by integration.

    CONSERVATIVE: X_ss == k/gamma exactly, at every load.
    DILUTED:      X_ss + C_ss == k/gamma exactly; X_ss falls by C_ss.
    """
    sol, _ = _solve(k, gamma, K_d, p_tot, complex_decays)
    return float(sol.y[0, -1]), float(sol.y[1, -1])


def response_half_time(k, gamma, K_d, p_tot, complex_decays=True):
    """Time for free X to first reach half of its OWN final value.

    Half of its own final value, not half of the unloaded one: this measures
    the speed of the response and not the level, so that the slowdown and the
    level shift stay separate quantities.
    """
    sol, t_end = _solve(k, gamma, K_d, p_tot, complex_decays)
    X_final = sol.y[0, -1]
    if X_final <= 0:
        raise RuntimeError("no steady state reached")
    return float(brentq(lambda t: sol.sol(t)[0] - 0.5 * X_final,
                        1e-10, t_end, xtol=1e-12))


def slowdown(k, gamma, K_d, p_tot, complex_decays=True):
    """Loaded half-time divided by unloaded half-time. 1.0 means no cost.

    WHICH MODEL YOU ARE IN DECIDES WHAT THIS MEANS, and the default is not the
    one the closed form below describes. Pass complex_decays=False for the
    PROTECTED model, where the bound regulator is shielded from removal; the
    default True is the DILUTED model, where it is not.

    In the PROTECTED model and the weak-load limit this is
    1 + (p_tot / X_T) / ln 2. The coefficient is 1/ln 2 = 1.442695 and it is
    DERIVED, not measured: the loaded system must synthesise p_tot extra
    molecules to fill the sites before it reaches the same half-way point,
    which costs p_tot/k against an unloaded half-time of ln2/gamma. See
    sessions/s21-retroactivity/REBUILD.md section 2.1, which supersedes
    NUMBERS.md section 4 -- that file called the coefficient measured and not
    derivable, and proposed deriving it as an open exercise. It is three lines.

    In the DILUTED model there is no such clean coefficient: the steady state
    itself moves with the load, so the ratio of the speed cost to the level
    cost drifts from 1.44 at p_tot/X_T = 0.002 to 1.71 at 0.3.
    """
    loaded = response_half_time(k, gamma, K_d, p_tot, complex_decays)
    bare = response_half_time(k, gamma, K_d, 0.0, complex_decays)
    return loaded / bare


def level_shift(k, gamma, K_d, p_tot):
    """Fractional drop in the steady state of free X, in the DILUTED model.

    Equals C_ss / X_T exactly: the shift *is* the parked fraction. In the weak
    load limit it is p_tot / X_T.

    DILUTED model only, and there is no model switch: in the conservative
    model this quantity is identically zero, so there is no question to ask.
    Use `steady_state` to see that nothing moves there.
    """
    X_ss, _ = steady_state(k, gamma, K_d, p_tot, complex_decays=True)
    X_T = k / gamma
    return (X_T - X_ss) / X_T


def affinity_is_irrelevant(k, gamma, p_tot, K_ds, tol=0.05, complex_decays=False):
    """Is the slowdown flat in K_d across `K_ds`?

    The session's claim as a checkable predicate rather than a sentence: while
    the sites are saturated, the cost of a load is set by how MANY sites there
    are and not by how tightly they bind. Returns (verdict, spread, slowdowns).

    `spread` is the relative range of the slowdown over `K_ds`. Pass affinities
    that are all well below X_T = k/gamma and it is True; include K_d >= X_T and
    it is False, because there the sites empty out and the load disappears along
    with the regulation.
    """
    vals = np.array([slowdown(k, gamma, K_d, p_tot, complex_decays) for K_d in K_ds])
    spread = float((vals.max() - vals.min()) / vals.min())
    return bool(spread < tol), spread, vals
