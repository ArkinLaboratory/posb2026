"""Tests for posb.digital -- each checks a result derived on the board in session 13."""
import numpy as np
import pytest

from posb.digital import Repressor, noise_margins, rbs_window, loglinear_range_hill


def test_gain_matches_finite_difference():
    g = Repressor(0.1, 10.0, 1.0, 2.0)
    for x in (0.3, 1.0, 3.0, 20.0):
        h = 1e-6
        fd = (np.log(g(x * np.exp(h))) - np.log(g(x * np.exp(-h)))) / (2 * h)
        assert np.isclose(g.gain(x), fd, rtol=1e-6)


def test_leak_free_gain_is_session_11s_g():
    # with y_min -> 0 the gain magnitude is n u^n/(1+u^n)
    g = Repressor(1e-12, 1.0, 1.0, 3.0)
    for u in (0.5, 1.0, 2.0):
        assert np.isclose(abs(g.gain(u)), 3 * u**3 / (1 + u**3), rtol=1e-6)


def test_no_cooperativity_no_restoring_region():
    for leak in (1e-6, 0.01, 0.1):
        with pytest.raises(ValueError):
            Repressor(leak, 1.0, 1.0, 1.0).thresholds()


def test_unity_gain_points_have_unit_gain():
    g = Repressor(0.1, 10.0, 1.0, 2.0)
    x_il, x_ih = g.thresholds()
    assert x_il < x_ih
    assert np.isclose(abs(g.gain(x_il)), 1.0) and np.isclose(abs(g.gain(x_ih)), 1.0)
    assert np.isclose(x_il, 1.021, atol=2e-3) and np.isclose(x_ih, 9.796, atol=5e-3)


def test_rbs_moves_outputs_not_thresholds():
    g = Repressor(0.1, 10.0, 1.0, 2.0)
    h = g.scaled(3.0)
    assert np.allclose(g.thresholds(), h.thresholds())
    assert np.allclose(np.array(h.output_levels()), 3 * np.array(g.output_levels()))


def test_self_matching_window_n2():
    # n = 2, 100-fold leak ratio, K = 1: an identical-gate chain matches only for
    # y_max between about 19.8 and 50.5 (K units) -- a 2.55-fold RBS window.
    g = Repressor(0.1, 10.0, 1.0, 2.0)
    lo, hi = rbs_window(g, g)
    assert np.isclose(lo * 10, 19.80, atol=0.05) and np.isclose(hi * 10, 50.5, atol=0.2)
    nml, nmh = noise_margins(g, g)
    assert nml > 0 > nmh                       # as built, the high side fails
    mid = g.scaled(np.sqrt(lo * hi))
    a, b = noise_margins(mid, mid)
    assert np.isclose(a, b, atol=1e-6) and a > 0


def test_loglinear_range_is_nine_to_the_one_over_n():
    for n in (1, 2, 4):
        assert np.isclose(loglinear_range_hill(n), 9 ** (1 / n))
