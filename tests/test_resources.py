"""Tests for posb.resources. Run with:  python -m pytest tests/ -q

Every closed form here is checked against the system it claims to solve, not
against a number typed in by hand.
"""
import numpy as np
import pytest

from posb import resources


# -------------------------------------------------------------- resources -----

def test_free_fraction_and_expression_agree_with_the_derivation():
    d = [0.5, 1.5, 3.0]
    assert resources.free_fraction(d) == pytest.approx(1 / 6)
    assert resources.expression(d) == pytest.approx(
        np.array(d) / 6.0)


def test_inducing_one_gene_lowers_an_unconnected_gene():
    alone = resources.expression([1.0, 0.0])[0]
    for d2 in (0.25, 1.0, 4.0, 16.0):
        assert resources.expression([1.0, d2])[0] < alone


def test_the_fall_is_exactly_a_hyperbola_with_apparent_K():
    for d1 in (0.2, 1.0, 5.0):
        p0 = resources.expression([d1, 0.0])[0]
        K = resources.apparent_K(d1)
        for d2 in (0.3, 3.0, 30.0):
            exact = resources.expression([d1, d2])[0]
            hill1 = p0 / (1.0 + d2 / K)
            assert exact == pytest.approx(hill1, rel=1e-12)


def test_apparent_K_moves_with_the_reporters_own_demand():
    # This is the experimental signature. A real repressor's K would not move.
    assert resources.apparent_K(0.1) != pytest.approx(resources.apparent_K(5.0))


def test_isocost_sum_depends_only_on_total_demand():
    for total in (1.0, 10.0, 100.0):
        ref = resources.isocost_sum([total])
        for frac in (0.1, 0.3, 0.5, 0.7, 0.9):
            split = [total * frac, total * (1 - frac)]
            assert resources.expression(split).sum() == pytest.approx(ref,
                                                                      rel=1e-12)
            assert resources.isocost_sum(split) == pytest.approx(ref, rel=1e-12)


def test_isocost_sum_is_below_one_and_approaches_it():
    assert resources.isocost_sum([1e6]) < 1.0
    assert resources.isocost_sum([1e6]) > 0.999
    assert resources.isocost_sum([0.0]) == 0.0


def test_competition_model_integrates_to_the_closed_form():
    for d in ([0.5, 0.5], [2.0, 0.1], [0.1, 9.0]):
        m = resources.competition_model(d, k=1.0, R_total=1.0, gamma=1.0,
                                        k_on=1e3)
        x0 = {s: 0.0 for s in m.species}
        traj = m.simulate(x0, (0.0, 600.0), method="LSODA",
                          rtol=1e-9, atol=1e-12)
        final = traj.final()
        got = np.array([final["p1"], final["p2"]])
        assert got == pytest.approx(resources.expression(d), abs=2e-3)


def test_dilution_coupling_requires_a_sourced_penalty():
    with pytest.raises(TypeError):
        resources.dilution_coupled_steady_state([1.0])        # no default
    with pytest.raises(ValueError):
        resources.dilution_coupled_steady_state([1.0], lambda s: 0.0)


def test_dilution_coupling_raises_the_steady_state_when_growth_slows():
    # Slower growth dilutes less, so the same synthesis gives more protein.
    out_fast, g_fast = resources.dilution_coupled_steady_state(
        [1.0], lambda s: 1.0)
    out_slow, g_slow = resources.dilution_coupled_steady_state(
        [1.0], lambda s: 0.5)
    assert g_slow < g_fast
    assert out_slow[0] > out_fast[0]


def test_resources_rejects_nonsense():
    with pytest.raises(ValueError):
        resources.expression([-1.0])
    with pytest.raises(ValueError):
        resources.expression([[1.0, 2.0]])
    with pytest.raises(ValueError):
        resources.competition_model([1.0, 0.0])
