"""Tests for posb.retroactivity -- session 21.

These test the session's CLAIMS, not just the plumbing. Each of the four
headline results in sessions/s21-retroactivity/NUMBERS.md has a test here, so
that a later edit which quietly reverses one of them fails the build instead of
drifting through three documents.
"""
import numpy as np
import pytest

from posb.retroactivity import (
    retroactivity, steady_state, response_half_time, slowdown,
    level_shift, affinity_is_irrelevant, simulate_load,
)

K, GAMMA = 10.0, 0.01
X_T = K / GAMMA          # 1000


# ---------------------------------------------------------------- R(x) itself
def test_retroactivity_shape():
    assert retroactivity(0.0, 10.0, 1.0) == pytest.approx(10.0)      # p_tot/K_d
    # falls as x^-2 once x >> K_d
    assert retroactivity(100.0, 10.0, 1.0) == pytest.approx(10.0 * 1.0 / 101.0**2)
    # no load, no retroactivity, at any x
    assert retroactivity(np.linspace(0, 50, 7), 0.0, 1.0) == pytest.approx(0.0)


def test_retroactivity_rejects_nonsense():
    with pytest.raises(ValueError):
        retroactivity(-1.0, 10.0, 1.0)
    with pytest.raises(ValueError):
        retroactivity(1.0, -1.0, 1.0)
    with pytest.raises(ValueError):
        retroactivity(1.0, 10.0, 0.0)


# ------------------------------------------- CLAIM 1: conservative is exact
@pytest.mark.parametrize("p_tot", [10.0, 100.0, 1000.0])
def test_conservative_steady_state_is_exactly_unloaded(p_tot):
    """The load term drops out of dX/dt at steady state. Exactly, not nearly."""
    X_ss, _ = steady_state(K, GAMMA, 1.0, p_tot, complex_decays=False)
    assert X_ss == pytest.approx(X_T, rel=1e-10)


# ------------------------------------------- CLAIM 2: diluted pins the total
@pytest.mark.parametrize("p_tot", [10.0, 100.0, 1000.0])
def test_diluted_pins_total_and_shift_is_the_parked_fraction(p_tot):
    X_ss, C_ss = steady_state(K, GAMMA, 1.0, p_tot, complex_decays=True)
    assert X_ss + C_ss == pytest.approx(X_T, rel=1e-10)
    # the level shift IS the parked fraction -- same number, two descriptions
    assert level_shift(K, GAMMA, 1.0, p_tot) == pytest.approx(C_ss / X_T, rel=1e-8)


def test_diluted_level_shift_is_p_tot_over_X_T_in_the_weak_limit():
    for frac in (0.002, 0.01, 0.05):
        assert level_shift(K, GAMMA, 1.0, frac * X_T) == pytest.approx(frac, rel=2e-3)


# ------------------------------------------- CLAIM 3: the QSSA formula is right
@pytest.mark.parametrize("p_tot", [10.0, 100.0, 1000.0])
def test_qssa_reduction_reproduces_the_full_kinetics(p_tot):
    """dX/dt = (k - gamma X)/(1 + R(X)) against the full two-state system."""
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq

    def rhs(t, y):
        x = y[0]
        return [(K - GAMMA * x) / (1.0 + retroactivity(x, p_tot, 1.0))]

    t_end = 6000.0 / GAMMA
    s = solve_ivp(rhs, (0, t_end), [0.0], rtol=1e-12, atol=1e-14, dense_output=True)
    xf = s.y[0, -1]
    t_half_qssa = brentq(lambda t: s.sol(t)[0] - 0.5 * xf, 1e-10, t_end, xtol=1e-12)
    t_half_full = response_half_time(K, GAMMA, 1.0, p_tot, complex_decays=False)
    assert t_half_qssa == pytest.approx(t_half_full, rel=1e-5)


# --------------------- CLAIM 4: both costs scale with p_tot/X_T, not with K_d
def test_slowdown_is_flat_in_affinity_while_sites_are_saturated():
    """The session's thesis, as a predicate. K_d spans 10^4, all << X_T."""
    ok, spread, vals = affinity_is_irrelevant(
        K, GAMMA, p_tot=X_T, K_ds=[0.01, 1.0, 100.0], tol=0.05)
    assert ok, f"slowdown varied by {spread:.3f} across affinity: {vals}"
    assert spread < 0.03


def test_the_claim_has_a_boundary_and_the_predicate_finds_it():
    """Include K_d >= X_T and affinity DOES matter -- because the sites empty.

    This is the other half of the argument: you can escape the load with a weak
    operator, and it costs you the regulation. If this test ever passes as
    'irrelevant', the engineering sentence on the slide is wrong.
    """
    ok, spread, _ = affinity_is_irrelevant(
        K, GAMMA, p_tot=X_T, K_ds=[1.0, 1e4, 1e6], tol=0.05)
    assert not ok and spread > 0.5


def test_weak_load_slowdown_coefficient_is_stable():
    """slowdown - 1 = 1.45 * (p_tot/X_T), the 1.45 measured not derived.

    Tested as a stable ratio rather than as a closed form, which is what we are
    entitled to claim.
    """
    ratios = []
    for frac in (0.005, 0.01, 0.05, 0.1):
        s = slowdown(K, GAMMA, 1.0, frac * X_T, complex_decays=False) - 1.0
        ratios.append(s / frac)
    assert np.std(ratios) / np.mean(ratios) < 1e-3
    assert 1.40 < np.mean(ratios) < 1.50


# ----------------------------------------------------- monotonicity and sanity
def test_slowdown_is_monotone_in_load():
    vals = [slowdown(K, GAMMA, 1.0, f * X_T, complex_decays=False)
            for f in (0.0, 0.1, 0.3, 1.0, 3.0)]
    assert vals[0] == pytest.approx(1.0, rel=1e-9)
    assert all(b > a for a, b in zip(vals, vals[1:]))


def test_no_load_is_a_no_op_in_both_models():
    for dec in (False, True):
        X_ss, C_ss = steady_state(K, GAMMA, 1.0, 0.0, complex_decays=dec)
        assert X_ss == pytest.approx(X_T, rel=1e-10)
        assert C_ss == pytest.approx(0.0, abs=1e-12)
        assert slowdown(K, GAMMA, 1.0, 0.0, dec) == pytest.approx(1.0, rel=1e-9)


def test_simulate_load_conserves_sites():
    sol = simulate_load(K, GAMMA, 1.0, 100.0, complex_decays=True)
    assert np.all(sol.y[1] <= 100.0 + 1e-9)
    assert np.all(sol.y[1] >= -1e-9)
