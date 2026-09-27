"""Tests for posb.analysis.

The bifurcation tests are the important ones: they check an analytic result
against independent numerics, which is exactly what the session 9 worked
example asks students to do.
"""
import numpy as np
import pytest

from posb import (Model, Reaction, fixed_points, jacobian, classify,
                  stability_report, toggle_model, toggle_alpha_critical,
                  repressilator_model, repressilator_alpha_critical, loop_gain,
                  sweep, leading_real_part, hopf_boundary)


def n_stable(alpha, n):
    r = stability_report(toggle_model(alpha, alpha, n=n), grid=(1e-3, 100, 9))
    return sum(1 for f in r if f["type"].startswith("stable"))


def test_alpha_critical_matches_known_values():
    assert np.isclose(toggle_alpha_critical(2), 2.0)
    assert np.isclose(toggle_alpha_critical(3), 3 * 2 ** (-4 / 3))
    assert np.isinf(toggle_alpha_critical(1.0))
    assert np.isinf(toggle_alpha_critical(0.5))


@pytest.mark.parametrize("n", [1.5, 2.0, 3.0, 4.0])
def test_bifurcation_boundary_is_where_the_theory_says(n):
    ac = toggle_alpha_critical(n)
    assert n_stable(ac * 0.97, n) == 1, "should be monostable below alpha_c"
    assert n_stable(ac * 1.03, n) == 2, "should be bistable above alpha_c"


def test_no_cooperativity_means_no_bistability_at_any_alpha():
    # the sharp form of "cooperativity is required"
    for alpha in (2.0, 10.0, 100.0, 500.0):
        assert n_stable(alpha, 1.0) == 1


def test_bistable_toggle_has_a_saddle_between_two_stable_nodes():
    r = stability_report(toggle_model(3.0, 3.0, n=2), grid=(1e-3, 50, 9))
    kinds = [f["type"] for f in r]
    assert kinds.count("saddle") == 1
    assert sum(1 for k in kinds if k.startswith("stable")) == 2
    # the saddle sits on the diagonal, between the two states
    saddle = next(f for f in r if f["type"] == "saddle")["point"]
    assert np.isclose(saddle["u"], saddle["v"], rtol=1e-4)


def test_symmetric_toggle_fixed_points_have_the_closed_form():
    # for n=2, alpha=3 the outer states are (3 -/+ sqrt(5)) / 2
    r = stability_report(toggle_model(3.0, 3.0, n=2), grid=(1e-3, 50, 9))
    us = sorted(f["point"]["u"] for f in r if f["type"].startswith("stable"))
    assert np.isclose(us[0], (3 - np.sqrt(5)) / 2, rtol=1e-5)
    assert np.isclose(us[1], (3 + np.sqrt(5)) / 2, rtol=1e-5)


def test_jacobian_matches_an_analytic_one():
    # linear system: dx/dt = -2x + 3y ; dy/dt = 1x - 4y
    m = Model([Reaction({"x": 1}, {}, k=2.0),
               Reaction({"y": 1}, {"y": 1, "x": 1}, k=3.0),
               Reaction({"x": 1}, {"x": 1, "y": 1}, k=1.0),
               Reaction({"y": 1}, {}, k=4.0)], species=["x", "y"])
    J = jacobian(m, {"x": 1.0, "y": 1.0})
    np.testing.assert_allclose(J, [[-2, 3], [1, -4]], atol=1e-5)


def test_classify_labels():
    assert classify(np.array([[-1.0, 0], [0, -2.0]]))[0] == "stable node"
    assert classify(np.array([[1.0, 0], [0, 2.0]]))[0] == "unstable node"
    assert classify(np.array([[1.0, 0], [0, -2.0]]))[0] == "saddle"
    assert classify(np.array([[-1.0, -2.0], [2.0, -1.0]]))[0] == "stable spiral"


def test_fixed_points_finds_the_unstable_one():
    # forward integration can never land on the saddle; root-finding must
    pts = fixed_points(toggle_model(3.0, 3.0, n=2),
                       guesses=[{"u": 1.2, "v": 1.2}])
    assert len(pts) == 1
    assert np.isclose(pts[0]["u"], pts[0]["v"], rtol=1e-4)


# --- the repressilator and its Hopf boundary  (session 11) -----------------

def test_repressilator_needs_cooperativity_above_two():
    # A three-gene ring with n <= 2 cannot oscillate no matter how strong the
    # promoters. This is the counterpart of the toggle needing n > 1.
    assert repressilator_alpha_critical(2) == float("inf")
    assert repressilator_alpha_critical(1) == float("inf")
    assert np.isfinite(repressilator_alpha_critical(2.5))


def test_repressilator_alpha_critical_at_n_four_is_exactly_two():
    # alpha_c = (2/(n-2))**(1/n) * n/(n-2); at n = 4 that is 1**(1/4) * 2 = 2.
    assert np.isclose(repressilator_alpha_critical(4), 2.0, rtol=1e-12)


def test_loop_gain_is_two_at_the_boundary():
    # The criterion the session exists to produce: the ring loses stability
    # exactly when the gain around it reaches 2.
    for n in (2.5, 3.0, 4.0, 5.0, 8.0):
        assert np.isclose(loop_gain(repressilator_alpha_critical(n), n), 2.0,
                          rtol=1e-9)


def test_analytic_boundary_matches_numerical_bisection():
    # The analytic alpha_c against hopf_boundary, which knows nothing about it
    # and only watches the leading eigenvalue cross zero.
    for n in (2.5, 3.0, 4.0, 5.0, 8.0):
        ac = repressilator_alpha_critical(n)
        num = hopf_boundary(repressilator_model(n=n), "alpha",
                            0.3 * ac, 5.0 * ac)
        assert np.isclose(num, ac, rtol=1e-6)


def test_leading_real_part_changes_sign_across_the_boundary():
    n = 3
    ac = repressilator_alpha_critical(n)
    m = repressilator_model(n=n)
    assert leading_real_part(m, {"alpha": 0.7 * ac}) < 0
    assert leading_real_part(m, {"alpha": 1.5 * ac}) > 0


def test_sweep_collects_one_result_per_value():
    m = repressilator_model(n=3)
    vals = [2.0, 4.0, 8.0]
    got = sweep(m, "alpha", vals, leading_real_part)
    assert len(got) == len(vals)
    # monotone in alpha over this range, and it crosses zero inside it
    assert got[0] < 0 < got[-1]


def test_period_at_onset_is_two_pi_over_root_three():
    # At the boundary g = 2, so the complex pair is -1 + g/2 +/- i g sqrt(3)/2
    # = 0 +/- i sqrt(3): the emerging oscillation has period 2 pi / sqrt(3).
    n = 3
    ac = repressilator_alpha_critical(n)
    J = jacobian(repressilator_model(n=n),
                 fixed_points(repressilator_model(n=n),
                              [[1.0, 1.0, 1.0]], {"alpha": ac})[0],
                 {"alpha": ac})
    ev = np.linalg.eigvals(J)
    omega = np.max(np.abs(ev.imag))
    assert np.isclose(omega, np.sqrt(3.0), rtol=1e-6)
    assert np.isclose(2 * np.pi / omega, 3.6276, rtol=1e-4)


def test_hopf_boundary_refuses_a_bracket_that_does_not_straddle():
    m = repressilator_model(n=3)
    ac = repressilator_alpha_critical(3)
    with pytest.raises(ValueError):
        hopf_boundary(m, "alpha", 0.2 * ac, 0.5 * ac)
