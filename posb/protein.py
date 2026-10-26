"""
posb.protein — covalent modification cycles and zero-order ultrasensitivity.

Introduced in Session 18. You derive the steady-state condition on the board
first and solve the quadratic by hand; this is the same algebra made reusable,
and it is what PS7 asks you to call.

THE SYSTEM. One substrate pool of fixed total size W_T, two opposing enzymes:

    kinase       W  -> W*     Michaelis-Menten, maximal rate v1, constant K1
    phosphatase  W* -> W      Michaelis-Menten, maximal rate v2, constant K2

Nothing is synthesised and nothing is degraded, so W + W* = W_T throughout.
This is the first system in the course whose total is conserved rather than set
by a balance of production and dilution, and that is the whole reason it
behaves differently.

THE DERIVATION. At steady state the two fluxes are equal. Write w = W*/W_T for
the fraction modified, and normalise each Michaelis constant BY THE SUBSTRATE
POOL -- the move that makes the result visible:

    k1 = K1/W_T,   k2 = K2/W_T,   u = v1/v2

        u (1 - w) / (k1 + 1 - w)  =  w / (k2 + w)

Cross-multiplying gives a quadratic in w:

        (1 - u) w^2  +  [u(1 - k2) - k1 - 1] w  +  u k2  =  0

so the response curve is available in closed form, with no new mathematics
beyond session 4's Michaelis-Menten.

WHAT THE NORMALISATION MEANS. k = K_m/W_T is the Michaelis constant measured in
units of the substrate pool, so it answers "is this enzyme saturated by its own
substrate pool?" k >> 1 is unsaturated and the cycle is first-order in w;
k << 1 is saturated and the cycle is ZERO-order -- the enzyme runs flat out and
does not care how much substrate there is. The second regime is the one that
produces a switch.

TWO EXACT RESULTS, and the second one is the design constraint:

    w(u = 1) = k2 / (k1 + k2)          at any degree of saturation
    u_50     = (k1 + 1/2) / (k2 + 1/2)

A WRONG TURN WORTH KEEPING. u_50 is a ratio, so it looks as though scaling both
Michaelis constants down should sharpen the response while leaving the
threshold put -- two independent knobs. It is a ratio of (k + 1/2), not of k.
As the constants shrink, which is exactly what buys the sharpness, numerator
and denominator both approach 1/2 and u_50 approaches ONE. At an apparent Hill
coefficient of 32 the threshold is confined to within about 3% of the point
where the two enzyme capacities are equal, whatever affinities are chosen.

So affinities cannot place a sharp switch. What places it is u = v1/v2, the
ratio of the two enzymes' maximal rates, which is set by how much of each
enzyme the cell expresses -- an expression level, and the subject of sessions 5
through 7. The protein layer buys the sharpness; the transcriptional layer sets
the threshold. Neither replaces the other.

PROVENANCE. The amplification is Goldbeter, A. & Koshland, D. E. Jr., "An
amplified sensitivity arising from covalent modification in biological
systems", PNAS 78(11):6840-6844 (1981). `sensitivity_index` below returns their
ratio of the stimulus needed for 90% modification to that needed for 10%; a
hyperbolic response needs a factor of 81, and anything below 81 is sharper than
hyperbolic. Every number this module produces is COMPUTED from the model, not
measured -- `apparent_hill` is a property of the equations, and the measured
Hill coefficients reported for real engineered switches belong beside it with
their own citations, not inside it.
"""

import math

import numpy as np
from scipy.optimize import brentq

__all__ = [
    "modified_fraction", "crossing_fraction", "half_maximal_stimulus",
    "stimulus_for_fraction", "sensitivity_index", "apparent_hill",
    "HYPERBOLIC_SENSITIVITY_INDEX", "cycle_model",
]

# A hyperbolic (Michaelian) response goes from 10% to 90% of maximum over an
# 81-fold change in stimulus: solve x/(1+x) = 0.1 and 0.9 and take the ratio.
# Goldbeter and Koshland's index is referred to this value.
HYPERBOLIC_SENSITIVITY_INDEX = 81.0


def _coefficients(u, k1, k2):
    """The quadratic a w^2 + b w + c, exactly as derived above."""
    a = 1.0 - u
    b = u * (1.0 - k2) - k1 - 1.0
    c = u * k2
    return a, b, c


def modified_fraction(u, k1, k2):
    """Fraction of the substrate pool modified at steady state.

    Parameters
    ----------
    u : float
        Ratio of maximal rates, v1/v2. The stimulus.
    k1, k2 : float
        Michaelis constants of the forward and reverse enzymes, each divided by
        the total substrate pool. Small means saturated.

    Returns the root of the quadratic that lies in [0, 1]; there is exactly one.
    """
    u = float(u)
    if u < 0 or k1 <= 0 or k2 <= 0:
        raise ValueError("u must be non-negative and k1, k2 strictly positive")
    if u == 0.0:
        return 0.0
    a, b, c = _coefficients(u, k1, k2)
    if abs(a) < 1e-13:                      # u == 1: the quadratic degenerates
        return -c / b
    disc = b * b - 4.0 * a * c
    if disc < 0.0:                          # only ever round-off at a tangency
        disc = 0.0
    # STABLE ROOTS, 26 October. The textbook form (-b +/- sqrt(disc))/(2a)
    # cancels catastrophically whenever |b| >> |4ac| -- which is precisely the
    # saturated, far-from-u=1 corner this module exists to describe. Measured
    # before the fix: at u = 1e12, k1 = k2 = 1e-4 it returned w = 1.0 with a
    # relative residual of 0.11, and sensitivity_index inherited the flattening
    # so apparent_hill(1e-10, 1e-10) returned -20.85 with no warning. Numerical
    # Recipes 5.6: form q = -(b + sign(b)*sqrt(disc))/2, whose two terms never
    # cancel, and take the roots as q/a and c/q.
    root = math.sqrt(disc)
    if b != 0.0:
        q = -0.5 * (b + math.copysign(root, b))
    else:
        q = -0.5 * root
    candidates = (q / a, c / q) if q != 0.0 else (0.0, -b / a)
    for w in candidates:
        if -1e-9 <= w <= 1.0 + 1e-9:
            return min(max(float(w), 0.0), 1.0)
    raise RuntimeError(
        f"no steady state in [0,1] for u={u}, k1={k1}, k2={k2}"
    )


def crossing_fraction(k1, k2):
    """Fraction modified when the two enzymes have equal maximal rates (u = 1).

    Exact: the w^2 coefficient is (1 - u), which vanishes at u = 1, leaving a
    linear equation whose solution is k2/(k1 + k2). Note what this says --
    equal Michaelis constants put the crossing at exactly one half, however
    saturated the enzymes are. Saturation sets the sharpness of the response,
    not where it crosses.
    """
    return k2 / (k1 + k2)


def half_maximal_stimulus(k1, k2):
    """The stimulus u at which half the pool is modified.

    Exact: set w = 1/2 in the steady-state condition and solve for u, giving
    (k1 + 1/2)/(k2 + 1/2). Read the module docstring before using this to tune
    a threshold -- it collapses towards 1 as the response sharpens.
    """
    return (k1 + 0.5) / (k2 + 0.5)


def stimulus_for_fraction(frac, k1, k2, lo=1e-12, hi=1e12):
    """The stimulus u that drives the cycle to a given modified fraction."""
    if not 0.0 < frac < 1.0:
        raise ValueError("frac must lie strictly between 0 and 1")
    f = lambda u: modified_fraction(u, k1, k2) - frac
    return brentq(f, lo, hi, xtol=1e-14, rtol=1e-15)


def sensitivity_index(k1, k2):
    """Goldbeter and Koshland's sensitivity index: u(90%) / u(10%).

    81 is a hyperbolic response. Below 81 is sharper than hyperbolic, which is
    what "ultrasensitive" means. There is no cooperative binding anywhere in
    this model -- the sharpening comes from saturation alone.
    """
    return (stimulus_for_fraction(0.9, k1, k2)
            / stimulus_for_fraction(0.1, k1, k2))


def apparent_hill(k1, k2):
    """The Hill coefficient a Hill function would need to be this sharp.

    A Hill function of coefficient n covers 10% to 90% over a stimulus factor
    of 81^(1/n), so n = ln(81) / ln(index). This is a DESCRIPTION of a curve
    that contains no cooperativity, not a claim that anything binds
    cooperatively -- which is the point worth taking away: a measured Hill
    coefficient above 1 does not establish cooperative binding.
    """
    try:
        index = sensitivity_index(k1, k2)
    except (ValueError, RuntimeError) as exc:   # brentq cannot bracket
        raise ValueError(
            f"cannot locate the 10% and 90% stimuli for k1={k1}, k2={k2}: the "
            "response is too steep for the bracketing solver to separate them "
            f"in double precision. This is the index running out, not the "
            f"root: below about k = 6e-8 there is no resolvable n ({exc})."
        ) from exc
    # GUARD, 26 October. Below roughly k = 1e-5 the two stimuli that bracket
    # 10% and 90% are so close that the index rounds to 1 and n runs away; a
    # hair further and it rounds BELOW 1 and n comes back NEGATIVE. Silently.
    # An apparent Hill coefficient is only defined for an index above 1, so say
    # so rather than returning a number that looks like an answer.
    if not index > 1.0 + 1e-6:
        raise ValueError(
            f"sensitivity index {index!r} is too close to 1 for k1={k1}, "
            f"k2={k2}: the stimuli at 10% and 90% differ by less than a part "
            "in a million, so ln(index) is numerical noise and no apparent "
            "Hill coefficient can be read off it. Measured, the guard fires "
            "below about k = 6e-8; above that the returned n is sound -- "
            "n*k holds at 0.247188 to six figures from k = 1e-6 down to the "
            "guard. Before this guard existed (26 October) k = 1e-10 "
            "returned -20.85 with no warning."
        )
    return np.log(HYPERBOLIC_SENSITIVITY_INDEX) / np.log(index)


def cycle_model(v1=1.0, v2=1.0, K1=0.01, K2=0.01, W_total=1.0):
    """The same cycle as a `posb.core.Model`, for integrating the transient.

    The closed form above is the steady state. This is the system it is the
    steady state OF, built from two Michaelis-Menten rate laws on a conserved
    pool, so that the approach to the switch can be watched rather than
    asserted. State is [W, Wstar].
    """
    from .core import Reaction, Model

    forward = Reaction(
        {"W": 1}, {"Wstar": 1},
        rate=lambda c, p: p["v1"] * c["W"] / (p["K1"] + c["W"]),
        name="kinase",
    )
    reverse = Reaction(
        {"Wstar": 1}, {"W": 1},
        rate=lambda c, p: p["v2"] * c["Wstar"] / (p["K2"] + c["Wstar"]),
        name="phosphatase",
    )
    return Model(
        [forward, reverse],
        params={"v1": v1, "v2": v2, "K1": K1, "K2": K2},
        species=["W", "Wstar"],
    )
