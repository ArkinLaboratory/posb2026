"""
posb.stochastic — the Gillespie algorithm, and how to read noise off it.

Introduced in Session 12. You write your own SSA first, in the session's
notebook; this is the same fifteen lines with the bookkeeping made reusable.

The two draws, which are the whole algorithm:

    when:   tau ~ Exponential(a0),        a0 = sum_j a_j(x)
    which:  reaction j with probability   a_j(x) / a0

The state is a vector of integer counts. A reaction changes it by one row of
`stoich`. Propensities are functions of the *counts*, not of concentrations.

One trap this module exists to keep you out of: the state between events is
constant for a random length of time, so a mean over the trajectory must be
weighted by how long each state lasted. Averaging the list of visited states
counts a state visited for a nanosecond the same as one held for an hour.
`time_average` does it correctly.

Plain NumPy. Read the source.
"""

import numpy as np

__all__ = [
    "gillespie",
    "time_average",
    "fano",
    "cv",
    "birth_death",
    "two_stage",
    "negative_autoregulation",
    "two_stage_fano",
    "nar_fano_lna",
]


# ---------------------------------------------------------------------------
# The algorithm
# ---------------------------------------------------------------------------

def gillespie(stoich, propensity, x0, t_max, rng=None, max_events=10_000_000):
    """Exact stochastic simulation (Gillespie 1977, the direct method).

    Parameters
    ----------
    stoich : array (R, S) of int
        Row j is the change in the S counts when reaction j fires.
    propensity : callable
        propensity(x) -> array of R non-negative rates for state x.
    x0 : array (S,) of int
        Initial counts.
    t_max : float
        Stop when the next event would fall after this time.
    rng : numpy.random.Generator or int, optional
        Seed or generator. Pass one: an unseeded run cannot be reproduced.
    max_events : int
        Guard against a runaway system.

    Returns
    -------
    t : array (E+1,)
        Event times, starting at 0. The state X[i] holds from t[i] to t[i+1]
        (the last state holds to t_max).
    X : array (E+1, S)
        State after each event.
    """
    rng = np.random.default_rng(rng)
    stoich = np.asarray(stoich, dtype=np.int64)
    x = np.array(x0, dtype=np.int64)
    if stoich.ndim != 2 or stoich.shape[1] != x.size:
        raise ValueError("stoich must be (reactions, species) to match x0")

    times = [0.0]
    states = [x.copy()]
    t = 0.0
    for _ in range(max_events):
        a = np.asarray(propensity(x), dtype=float)
        a0 = a.sum()
        if a0 <= 0.0:                      # nothing can happen any more
            break
        t += rng.exponential(1.0 / a0)     # when
        if t > t_max:
            break
        j = np.searchsorted(np.cumsum(a), rng.random() * a0, side="right")
        x = x + stoich[min(j, len(a) - 1)]  # which (min guards round-off)
        times.append(t)
        states.append(x.copy())
    else:
        raise RuntimeError(f"stopped after {max_events} events, t = {t:.4g}")
    return np.array(times), np.array(states)


def time_average(t, X, t_max, t_burn=0.0):
    """Time-weighted mean and variance of each species after `t_burn`.

    Each state is weighted by how long it was held. Returns (mean, var),
    arrays of length S (or scalars if X is one-dimensional).
    """
    t = np.asarray(t, dtype=float)
    X = np.asarray(X, dtype=float)
    ends = np.append(t[1:], t_max)
    dt = np.clip(ends, t_burn, None) - np.clip(t, t_burn, None)
    if dt.sum() <= 0:
        raise ValueError("no time recorded after t_burn")
    w = dt / dt.sum()
    mean = np.tensordot(w, X, axes=1)
    var = np.tensordot(w, (X - mean) ** 2, axes=1)
    return mean, var


def fano(mean, var):
    """Variance over mean. 1 for a Poisson distribution."""
    return np.asarray(var) / np.asarray(mean)


def cv(mean, var):
    """Standard deviation over mean — Elowitz et al. call this eta."""
    return np.sqrt(var) / np.asarray(mean)


# ---------------------------------------------------------------------------
# The three models session 12 uses
# ---------------------------------------------------------------------------

def birth_death(k, gamma):
    """0 -> X at rate k;  X -> 0 at rate gamma * x.  Stationary: Poisson(k/gamma)."""
    stoich = np.array([[+1], [-1]])

    def propensity(x):
        return np.array([k, gamma * x[0]])

    return stoich, propensity


def two_stage(k_m, gamma_m, k_p, gamma_p):
    """mRNA M and protein P.  Species order (M, P).

    0 -> M (k_m);  M -> 0 (gamma_m M);  M -> M + P (k_p M);  P -> 0 (gamma_p P).
    Burst size b = k_p / gamma_m proteins per transcript.
    """
    stoich = np.array([[+1, 0], [-1, 0], [0, +1], [0, -1]])

    def propensity(x):
        m, p = x
        return np.array([k_m, gamma_m * m, k_p * m, gamma_p * p])

    return stoich, propensity


def negative_autoregulation(beta, K, n, gamma):
    """X represses its own production: 0 -> X at beta / (1 + (x/K)^n)."""
    stoich = np.array([[+1], [-1]])

    def propensity(x):
        return np.array([beta / (1.0 + (x[0] / K) ** n), gamma * x[0]])

    return stoich, propensity


# ---------------------------------------------------------------------------
# What the board derivations predict
# ---------------------------------------------------------------------------

def two_stage_fano(k_p, gamma_m, gamma_p):
    """Exact stationary protein Fano factor of the two-stage model:
    1 + k_p / (gamma_m + gamma_p).  Tends to 1 + b when mRNA is short-lived."""
    return 1.0 + k_p / (gamma_m + gamma_p)


def nar_fano_lna(n, x_over_K):
    """Linear-noise Fano factor for protein-only negative autoregulation.

    Fano = 1 / (1 + g), with g = n u^n / (1 + u^n) and u = x/K at the steady
    state — the logarithmic sensitivity of the production rate, which is the
    same loop gain that set the repressilator's boundary in session 11.
    Protein-only, and intrinsic noise only: bursting reduces the benefit. Slow
    extrinsic changes in the gene's own rates are buffered more strongly,
    d ln x*/d ln beta = 1/(1 + g), i.e. by 1 + g in CV rather than sqrt(1 + g).
    """
    u = np.asarray(x_over_K, dtype=float)
    g = n * u ** n / (1.0 + u ** n)
    return 1.0 / (1.0 + g)
