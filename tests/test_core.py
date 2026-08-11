"""Tests for posb.core. Run with:  python -m pytest tests/ -q

These also serve as worked examples of what the package guarantees.
"""
import numpy as np
import pytest

from posb import Reaction, Model


def test_stoichiometric_matrix_signs():
    # A + B -> C
    r = Reaction({"A": 1, "B": 1}, {"C": 1}, k=1.0)
    m = Model([r], species=["A", "B", "C"])
    assert m.S.shape == (3, 1)
    np.testing.assert_array_equal(m.S[:, 0], [-1, -1, 1])


def test_stoichiometric_coefficients():
    # 2A -> B
    m = Model([Reaction({"A": 2}, {"B": 1}, k=1.0)], species=["A", "B"])
    np.testing.assert_array_equal(m.S[:, 0], [-2, 1])


def test_species_appearing_on_both_sides_net_to_zero():
    # A + B -> A + C   (A is a catalyst)
    m = Model([Reaction({"A": 1, "B": 1}, {"A": 1, "C": 1}, k=1.0)],
              species=["A", "B", "C"])
    np.testing.assert_array_equal(m.S[:, 0], [0, -1, 1])


def test_mass_action_flux():
    r = Reaction({"A": 1, "B": 2}, {"C": 1}, k=3.0)
    assert r.flux({"A": 2.0, "B": 4.0}, {}) == pytest.approx(3.0 * 2.0 * 16.0)


def test_rate_constant_by_name_is_looked_up_in_params():
    m = Model([Reaction({"A": 1}, {}, k="gamma")], params={"gamma": 2.0})
    np.testing.assert_allclose(m.fluxes({"A": 3.0}), [6.0])
    # and can be overridden per call
    np.testing.assert_allclose(m.fluxes({"A": 3.0}, {"gamma": 5.0}), [15.0])


def test_exponential_decay_matches_analytic_solution():
    # X -> 0 with rate k;  X(t) = X0 exp(-k t)
    k, x0 = 0.5, 1.0
    m = Model([Reaction({"X": 1}, {}, k=k)])
    traj = m.simulate({"X": x0}, (0, 10), n_points=200)
    np.testing.assert_allclose(traj["X"], x0 * np.exp(-k * traj.t),
                               rtol=1e-5, atol=1e-8)


def test_mass_is_conserved_in_a_closed_conversion():
    # A <-> B, total should be constant
    m = Model([Reaction({"A": 1}, {"B": 1}, k=0.7),
               Reaction({"B": 1}, {"A": 1}, k=0.3)])
    traj = m.simulate({"A": 1.0, "B": 0.0}, (0, 20))
    total = traj["A"] + traj["B"]
    np.testing.assert_allclose(total, 1.0, rtol=1e-6)


def test_reversible_reaction_reaches_the_right_equilibrium():
    # A <-> B with kf, kr  =>  B/A = kf/kr at equilibrium
    kf, kr = 2.0, 0.5
    m = Model([Reaction({"A": 1}, {"B": 1}, k=kf),
               Reaction({"B": 1}, {"A": 1}, k=kr)])
    ss = m.steady_state({"A": 1.0, "B": 0.0}, t_max=500)
    assert ss["B"] / ss["A"] == pytest.approx(kf / kr, rel=1e-4)


def test_custom_rate_function():
    # Repression: -> X at alpha / (1 + (X/K)^n)
    rxn = Reaction({}, {"X": 1},
                   rate=lambda c, p: p["alpha"] / (1 + (c["X"] / p["K"]) ** p["n"]))
    m = Model([rxn, Reaction({"X": 1}, {}, k="gamma")],
              params={"alpha": 10.0, "K": 1.0, "n": 2, "gamma": 1.0})
    ss = m.steady_state({"X": 0.0}, t_max=200)["X"]
    # at steady state: alpha/(1+(x/K)^n) = gamma * x
    lhs = 10.0 / (1 + (ss / 1.0) ** 2)
    np.testing.assert_allclose(lhs, 1.0 * ss, rtol=1e-4)


def test_gene_expression_cascade_steady_state():
    # -> m -> p, both degraded.  m* = a/gm ,  p* = kp*m*/gp
    p = {"alpha": 5.0, "gamma_m": 0.5, "k_p": 2.0, "gamma_p": 0.1}
    m = Model(
        [Reaction({}, {"mRNA": 1}, k="alpha"),
         Reaction({"mRNA": 1}, {}, k="gamma_m"),
         Reaction({"mRNA": 1}, {"mRNA": 1, "protein": 1}, k="k_p"),
         Reaction({"protein": 1}, {}, k="gamma_p")],
        params=p, species=["mRNA", "protein"])
    ss = m.steady_state({"mRNA": 0.0, "protein": 0.0}, t_max=1000)
    m_star = p["alpha"] / p["gamma_m"]
    p_star = p["k_p"] * m_star / p["gamma_p"]
    assert ss["mRNA"] == pytest.approx(m_star, rel=1e-5)
    assert ss["protein"] == pytest.approx(p_star, rel=1e-5)


def test_dict_and_array_initial_conditions_agree():
    m = Model([Reaction({"A": 1}, {"B": 1}, k=1.0)], species=["A", "B"])
    t1 = m.simulate({"A": 1.0}, (0, 5))
    t2 = m.simulate([1.0, 0.0], (0, 5))
    np.testing.assert_allclose(t1.y, t2.y)


def test_helpful_errors():
    m = Model([Reaction({"A": 1}, {"B": 1}, k=1.0)])
    with pytest.raises(ValueError, match="Unknown species"):
        m.simulate({"Q": 1.0}, (0, 1))
    with pytest.raises(ValueError, match="expected 2"):
        m.simulate([1.0], (0, 1))
    with pytest.raises(KeyError, match="No species"):
        m.simulate({"A": 1.0}, (0, 1))["Q"]
    with pytest.raises(ValueError, match="exactly one"):
        Reaction({"A": 1}, {}, k=1.0, rate=lambda c, p: 1.0)


def test_rhs_equals_S_times_v_by_construction():
    m = Model([Reaction({"A": 1}, {"B": 1}, k=0.4),
               Reaction({"B": 1}, {}, k=0.9)], species=["A", "B"])
    x = np.array([2.0, 3.0])
    np.testing.assert_allclose(m.rhs(0.0, x), m.S @ m.fluxes(x))
