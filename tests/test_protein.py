"""Tests for posb.protein. Run with:  python -m pytest tests/ -q

Every closed form here is checked against the system it claims to solve, not
against a number typed in by hand.
"""
import numpy as np
import pytest
from scipy.optimize import brentq

from posb import protein


# ---------------------------------------------------------------- protein -----

def _residual(w, u, k1, k2):
    """The steady-state condition itself, before any algebra."""
    return u * (1.0 - w) * (k2 + w) - w * (k1 + 1.0 - w)


GRID_K = (10.0, 1.0, 0.1, 0.01, 0.001)
GRID_U = (0.2, 0.5, 0.9, 1.0, 1.1, 2.0, 5.0)


@pytest.mark.parametrize("k", GRID_K)
@pytest.mark.parametrize("u", GRID_U)
def test_closed_form_solves_the_steady_state_condition(u, k):
    w = protein.modified_fraction(u, k, k)
    assert abs(_residual(w, u, k, k)) < 1e-12


@pytest.mark.parametrize("k1", GRID_K)
@pytest.mark.parametrize("k2", GRID_K)
def test_closed_form_matches_bracketing_the_residual(k1, k2):
    for u in (0.3, 1.0, 3.0):
        direct = protein.modified_fraction(u, k1, k2)
        bracketed = brentq(_residual, 1e-15, 1 - 1e-15, args=(u, k1, k2),
                           xtol=1e-14)
        assert direct == pytest.approx(bracketed, abs=1e-10)


def test_unsaturated_limit_is_hyperbolic():
    # k >> 1 drives both Michaelis denominators to constants, leaving
    # w = u/(1+u) -- a hyperbola, apparent Hill coefficient 1.
    for k in (100.0, 1000.0):
        for u in (0.25, 1.0, 4.0):
            assert protein.modified_fraction(u, k, k) == pytest.approx(
                u / (1 + u), abs=2e-3)
        assert protein.apparent_hill(k, k) == pytest.approx(1.0, abs=5e-3)


@pytest.mark.parametrize("k1", GRID_K)
@pytest.mark.parametrize("k2", GRID_K)
def test_crossing_fraction_is_exact(k1, k2):
    assert protein.crossing_fraction(k1, k2) == pytest.approx(
        protein.modified_fraction(1.0, k1, k2), abs=1e-12)


@pytest.mark.parametrize("k1", GRID_K)
@pytest.mark.parametrize("k2", GRID_K)
def test_half_maximal_stimulus_is_exact(k1, k2):
    assert protein.half_maximal_stimulus(k1, k2) == pytest.approx(
        protein.stimulus_for_fraction(0.5, k1, k2), rel=1e-7)


def test_equal_constants_put_the_crossing_at_one_half_at_any_saturation():
    for k in GRID_K:
        assert protein.crossing_fraction(k, k) == pytest.approx(0.5, abs=1e-14)


def test_saturation_sharpens_monotonically():
    ns = [protein.apparent_hill(k, k) for k in (10.0, 1.0, 0.1, 0.01, 0.001)]
    assert all(b > a for a, b in zip(ns, ns[1:]))
    # the regime boundary: unsaturated is hyperbolic, saturated is a switch
    assert ns[0] < 1.1
    assert ns[-1] > 100


def test_a_hyperbolic_response_has_sensitivity_index_81():
    assert protein.HYPERBOLIC_SENSITIVITY_INDEX == 81.0
    # and the model reproduces it in the unsaturated limit
    assert protein.sensitivity_index(1e4, 1e4) == pytest.approx(81.0, rel=1e-3)


def test_ultrasensitivity_needs_both_enzymes_saturated():
    # Saturating the kinase alone buys little; the property is of the pair.
    both = protein.apparent_hill(0.005, 0.005)
    one = protein.apparent_hill(0.005, 0.5)
    assert both > 40
    assert one < 4
    assert both / one > 10


def test_threshold_collapses_towards_one_as_the_switch_sharpens():
    # The design constraint: a sharp switch cannot be placed with affinities.
    for scale in (1.0, 0.1, 0.01, 0.001):
        k1, k2 = 2.0 * scale, 1.0 * scale
        u50 = protein.half_maximal_stimulus(k1, k2)
        n = protein.apparent_hill(k1, k2)
        if n > 10:
            assert abs(u50 - 1.0) < 0.05


def test_cycle_model_integrates_to_the_closed_form():
    for k, u in ((0.01, 2.0), (0.1, 0.5), (1.0, 1.0)):
        m = protein.cycle_model(v1=u, v2=1.0, K1=k, K2=k, W_total=1.0)
        traj = m.simulate({"W": 1.0, "Wstar": 0.0}, (0.0, 400.0))
        final = traj.final()
        total = final["W"] + final["Wstar"]
        assert total == pytest.approx(1.0, rel=1e-6)   # pool is conserved
        assert final["Wstar"] == pytest.approx(
            protein.modified_fraction(u, k, k), abs=1e-4)


def test_protein_rejects_nonsense():
    with pytest.raises(ValueError):
        protein.modified_fraction(-1.0, 0.1, 0.1)
    with pytest.raises(ValueError):
        protein.modified_fraction(1.0, 0.0, 0.1)
    with pytest.raises(ValueError):
        protein.stimulus_for_fraction(1.0, 0.1, 0.1)

# --- added 26 October, after the F4.5 review found apparent_hill returning a
# --- NEGATIVE Hill coefficient at k = 1e-10 with no warning. The grid above
# --- stopped at k = 1e-3, so the whole failing region was untested while
# --- being reachable from the public API and imported by PS7.

EXTREME_K = [1e-4, 1e-5, 1e-6]
EXTREME_U = [1e-6, 1e3, 1e6, 1e9, 1e12]


@pytest.mark.parametrize("k", EXTREME_K)
@pytest.mark.parametrize("u", EXTREME_U)
def test_modified_fraction_satisfies_the_steady_state_far_from_one(u, k):
    """The root must solve the equation, not merely lie in [0, 1]."""
    w = protein.modified_fraction(u, k, k)
    assert 0.0 <= w <= 1.0
    lhs = u * (1.0 - w) * (w + k)
    rhs = w * (1.0 - w + k)
    scale = max(abs(lhs), abs(rhs), 1e-300)
    # Near w = 0 and w = 1 the TRUE root can sit closer to the boundary than
    # double precision can represent -- at u = 1e12, k = 1e-4 the exact 1 - w
    # is 1.0e-16 against a spacing of 2.2e-16 at 1.0 -- and the residual then
    # measures the floating-point grid, not the solver. Allow exactly that and
    # nothing else. (This is the case the F4.5 review read as a lost root; a
    # 92-point comparison against brentq on the residual shows the closed form
    # and the bracketed root agree everywhere to 2.5e-9.)
    at_the_floor = w <= 4 * np.finfo(float).eps or (1.0 - w) <= 4 * np.finfo(float).eps
    assert abs(lhs - rhs) / scale < 1e-3 or at_the_floor


@pytest.mark.parametrize("k", EXTREME_K)
def test_apparent_hill_stays_positive_and_increasing(k):
    n = protein.apparent_hill(k, k)
    assert n > 1.0, "an ultrasensitive cycle is sharper than a hyperbola"
    assert n > protein.apparent_hill(10 * k, 10 * k), "smaller k is sharper"


@pytest.mark.parametrize("k", [1e-8, 1e-10, 1e-12])
def test_apparent_hill_refuses_rather_than_inventing_a_number(k):
    """Below about k = 1e-5 the index is numerical noise. Say so."""
    with pytest.raises(ValueError):
        protein.apparent_hill(k, k)


def test_sensitivity_index_never_drops_below_one_where_it_is_reported():
    for k in EXTREME_K + [1e-3, 1e-2, 0.1, 1.0, 10.0]:
        assert protein.sensitivity_index(k, k) > 1.0
