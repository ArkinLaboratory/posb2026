"""Tests for posb.stochastic.

Every test checks a simulated statistic against a result derived on the board
in session 12. Tolerances are set from the run length, not tuned to pass.
"""
import numpy as np
import pytest

from posb.stochastic import (gillespie, time_average, fano, cv, birth_death,
                             two_stage, negative_autoregulation,
                             two_stage_fano, nar_fano_lna)


def test_time_average_weights_by_holding_time():
    # state 0 held for 9, state 10 held for 1: mean 1, not 5
    t = np.array([0.0, 9.0])
    X = np.array([[0], [10]])
    m, v = time_average(t, X, t_max=10.0)
    assert np.isclose(m[0], 1.0)
    assert np.isclose(v[0], 0.9 * 1 + 0.1 * 81)


def test_birth_death_is_poisson():
    stoich, a = birth_death(k=50.0, gamma=1.0)
    t, X = gillespie(stoich, a, [50], t_max=2000.0, rng=0)
    m, v = time_average(t, X, 2000.0, t_burn=20.0)
    assert abs(m[0] - 50.0) < 1.5
    assert abs(fano(m, v)[0] - 1.0) < 0.08
    assert np.isclose(cv(m, v)[0], np.sqrt(v[0]) / m[0])


def test_two_stage_fano_is_one_plus_burst_size():
    # b = k_p / gamma_m = 10; exact Fano = 1 + 20/(2+0.1) = 10.52
    stoich, a = two_stage(k_m=1.0, gamma_m=2.0, k_p=20.0, gamma_p=0.1)
    t, X = gillespie(stoich, a, [0, 100], t_max=8000.0, rng=1)
    m, v = time_average(t, X, 8000.0, t_burn=100.0)
    assert abs(m[1] - 100.0) < 8.0
    pred = two_stage_fano(20.0, 2.0, 0.1)
    assert np.isclose(pred, 1 + 20 / 2.1)
    assert abs(fano(m, v)[1] - pred) / pred < 0.15


@pytest.mark.parametrize("n,beta,pred", [(2, 200.0, 0.5), (4, 200.0, 1 / 3)])
def test_nar_matches_linear_noise_at_matched_mean(n, beta, pred):
    # K = 100 and beta = 200 put the steady state at x = K = 100, the same
    # mean as a constitutive gene at k = 100.
    assert np.isclose(nar_fano_lna(n, 1.0), pred)
    stoich, a = negative_autoregulation(beta=beta, K=100.0, n=n, gamma=1.0)
    t, X = gillespie(stoich, a, [100], t_max=3000.0, rng=2)
    m, v = time_average(t, X, 3000.0, t_burn=30.0)
    assert abs(m[0] - 100.0) < 2.0
    assert abs(fano(m, v)[0] - pred) < 0.06


def test_same_seed_same_trajectory():
    stoich, a = birth_death(5.0, 1.0)
    t1, X1 = gillespie(stoich, a, [0], 50.0, rng=7)
    t2, X2 = gillespie(stoich, a, [0], 50.0, rng=7)
    assert np.array_equal(t1, t2) and np.array_equal(X1, X2)


def test_absorbing_state_stops_cleanly():
    stoich, a = birth_death(0.0, 1.0)
    t, X = gillespie(stoich, a, [3], 100.0, rng=0)
    assert X[-1, 0] == 0 and len(t) == 4
