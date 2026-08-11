"""Tests for posb.analysis.

The bifurcation tests are the important ones: they check an analytic result
against independent numerics, which is exactly what the session 9 worked
example asks students to do.
"""
import numpy as np
import pytest

from posb import (Model, Reaction, fixed_points, jacobian, classify,
                  stability_report, toggle_model, toggle_alpha_critical)


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
