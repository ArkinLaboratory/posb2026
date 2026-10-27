"""Session 22's claims, as tests.

Every test here is a sentence the deck says out loud. If one fails, a slide is
wrong -- that is the point of the file.

The failure mode this suite is built against is session 21's: a result proved
in one model and quoted under another. So every test names its model, and the
dilution rate is always explicit rather than defaulted.
"""
import numpy as np
import pytest

from posb.control import (
    ControlParams, simulate, closed_loop_steady_state, open_loop_steady_state,
    setpoint_error, settles, max_rejectable_disturbance, step_response,
    disturbance_rejection, error_scaling_exponent,
)


@pytest.fixture
def P():
    return ControlParams()


# ------------------------------------------------- the set point is mu/theta
def test_output_goes_to_mu_over_theta(P):
    """The one sentence of the session."""
    assert closed_loop_steady_state(P) == pytest.approx(5.0, abs=1e-6)
    assert P.set_point == 5.0


@pytest.mark.parametrize("label,q", [
    ("plant gain",   ControlParams(k=4.0)),
    ("removal rate", ControlParams(gamma=0.1)),
    ("annihilation", ControlParams(eta=500.0)),
    ("all at once",  ControlParams(k=4.0, gamma=0.1, eta=500.0)),
])
def test_the_plant_does_not_get_a_vote(label, q):
    """Aoki: "it does not depend on the topology and parameters of the
    circuit of interest". Change the plant; the answer may not move."""
    assert closed_loop_steady_state(q) == pytest.approx(5.0, abs=1e-6), label


# ------------------------------------------------------ disturbance rejection
@pytest.mark.parametrize("d", [0.5, 1.0, 2.0])
def test_closed_loop_rejects_what_open_loop_does_not(P, d):
    assert closed_loop_steady_state(P, d) == pytest.approx(5.0, abs=1e-6)
    # the open loop moves one-for-one with d/gamma, so it had better move
    assert open_loop_steady_state(P, d) > open_loop_steady_state(P, 0.0) + 0.5


def test_open_loop_and_closed_loop_agree_with_no_disturbance(P):
    """Otherwise the comparison figure is drawing two different circuits."""
    assert open_loop_steady_state(P, 0.0) == pytest.approx(
        closed_loop_steady_state(P, 0.0), abs=1e-6)


# ------------------------------------------------------- the actuator bound
def test_the_bound_is_gamma_times_the_set_point(P):
    assert max_rejectable_disturbance(P) == pytest.approx(2.5)


def test_inside_the_bound_it_settles_and_outside_it_does_not(P):
    """Past the bound there is NO steady state -- Z2 grows without bound. A
    test that only checked X would miss this, because X looks convergent."""
    assert settles(P, 2.4) is True
    assert settles(P, 2.6) is False


def test_past_the_bound_z2_really_is_still_growing(P):
    """The honest version of the previous test: name the mechanism."""
    z2 = [float(simulate(P, 5.0, t_end=t).y[2, -1]) for t in (4000.0, 8000.0)]
    assert z2[1] / z2[0] > 1.8, (
        "Z1 has hit zero, so the annihilation removing Z2 has stopped and Z2 "
        "grows roughly linearly in time")


# ----------------------------------------------------------------- the leak
def test_no_dilution_no_error(P):
    assert setpoint_error(P, 2.0) == pytest.approx(0.0, abs=1e-6)


def test_dilution_breaks_adaptation(P):
    leaky = ControlParams(delta=0.1)
    assert abs(setpoint_error(leaky, 2.0)) > 1e-3


def test_the_leak_makes_it_undershoot(P):
    """Sign matters: the output falls BELOW the set point."""
    assert setpoint_error(ControlParams(delta=0.05), 1.0) < 0


def test_error_is_first_order_in_the_dilution_rate(P):
    assert error_scaling_exponent(P) == pytest.approx(1.0, abs=0.02)


def test_error_grows_monotonically_with_dilution(P):
    errs = [abs(setpoint_error(ControlParams(delta=d), 2.0))
            for d in (0.0, 0.001, 0.01, 0.05, 0.1)]
    assert errs == sorted(errs)


# --------------------------------------------- the two failures are distinct
def test_saturation_and_leak_are_different_failures(P):
    """The deck must not blur them, so neither may this suite.

    Saturation: no steady state, at delta = 0. Leak: a steady state in the
    wrong place, inside the actuator bound.
    """
    assert settles(P, 5.0) is False                      # saturation, no leak
    leaky = ControlParams(delta=0.05)
    assert settles(leaky, 2.0) is True                   # leak, not saturated
    assert abs(setpoint_error(leaky, 2.0)) > 1e-4


def test_rejection_is_infinite_only_because_the_model_is_ideal(P):
    """NUMBERS.md section 7: the honest statement is the leak, not this."""
    assert disturbance_rejection(P, 1.0) == float("inf")
    assert np.isfinite(disturbance_rejection(ControlParams(delta=0.05), 1.0))


# ---- the four facts the 27 October review found wrong, locked down -------


def test_the_bound_is_one_sided_negative_d_is_always_rejected():
    """d < 0 needs MORE Z1, and Z1 has no upper bound. Only d > 0 binds.

    The deck asked the room for the largest |d| with d negative. There is no
    such d: at d = -100 the loop sits at Z1 = 102.5 and holds the set point.
    """
    P = ControlParams()
    for d in (-2.6, -10.0, -100.0):
        assert closed_loop_steady_state(P, d) == pytest.approx(P.set_point, abs=1e-6)
        assert settles(P, d)
    assert not settles(P, max_rejectable_disturbance(P) + 0.1)


def test_the_annihilation_flux_pins_at_mu_rather_than_stopping():
    """Past the bound, eta*Z1*Z2 -> mu exactly. It does not stop.

    dZ1/dt = 0 on the Z1 plateau forces eta*Z1*Z2 = mu, so Z2 grows at
    theta*X - mu. Six files said "the annihilation stops" and one board wrote
    dZ2/dt = theta*X, which is 26x too large at d = 2.6.
    """
    P = ControlParams()
    sol = simulate(P, 5.0, 8000.0)
    X, Z1, Z2 = sol.y[:, -1]
    assert P.eta * Z1 * Z2 == pytest.approx(P.mu, rel=1e-6)
    assert X == pytest.approx(5.0 / P.gamma, rel=1e-5)   # X settles; Z2 runs


def test_the_undershoot_claim_is_only_true_below_the_sign_flip():
    """The error changes sign at d ~ 2.06, inside the actuator bound.

    d = 2 was the reference everywhere and sat 0.06 from this crossing, with
    |error| 24x smaller than at d = 0. The set now uses d = 1.
    """
    leaky = ControlParams(delta=0.05)
    assert setpoint_error(leaky, 1.0) < 0
    assert setpoint_error(leaky, 2.4) > 0
    assert settles(leaky, 2.4)          # still inside the bound


def test_step_response_starts_at_the_set_point():
    """Both loops rest at mu/theta until d arrives, so the figure shows d.

    Integrated from zero instead, the excursion on screen is the start-up
    transient, which is there with or without a disturbance.
    """
    P = ControlParams()
    closed = step_response(P, d=1.0, t_step=40.0, t_end=200.0, closed=True)
    opened = step_response(P, d=1.0, t_step=40.0, t_end=200.0, closed=False)
    for sol in (closed, opened):
        assert float(sol.sol(35.0)[0]) == pytest.approx(P.set_point, abs=1e-6)
    assert float(closed.sol(200.0)[0]) == pytest.approx(P.set_point, abs=1e-5)
    assert float(opened.sol(200.0)[0]) == pytest.approx(
        P.set_point + 1.0 / P.gamma, rel=1e-5)
