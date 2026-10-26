"""Tests for posb.fba -- session 20.

Two things these are built to catch, both of which have bitten this repo:

*   A claim that drifts. Every teaching claim in `teaching_network`'s docstring
    has a test here, including the two LIMITATIONS -- vertex solutions and
    alternate optima. If a later edit makes the alternate optimum go away, the
    slide about it becomes false and this suite says so.
*   A test that passes for the wrong reason. The hand derivation gives exact
    rationals (4 and 10/3), so these assert the exact values rather than
    "greater than zero", and the lethal knockouts are asserted to be exactly
    zero rather than merely small.
"""
import numpy as np
import pytest

from posb.core import Reaction, Model
from posb.fba import (
    FluxModel, teaching_network, solve_fba, knockout_growth,
    flux_ranges, coupled_pairs, has_alternate_optima, CARBONS, PSEUDO,
)


@pytest.fixture
def net():
    reactions, external, bounds = teaching_network()
    return FluxModel(reactions, external=external), bounds


# ------------------------------------- S is session 3's matrix, and provably so
def test_S_matches_posb_core_exactly():
    """fba assembles the same S as core.Model, with the rate column thrown away.

    The session is sold as "the same matrix from session 3, asked a different
    question". This is that sentence as a test.
    """
    spec = [({"A": 1}, {"B": 2}, "r1"),
            ({"B": 1, "C": 3}, {"D": 1}, "r2"),
            ({}, {"A": 1}, "r3"),
            ({"D": 1}, {}, "r4")]
    fm = FluxModel(spec)
    core = Model([Reaction(a, b, k=1.0, name=n) for a, b, n in spec])
    assert fm.metabolites == core.species
    np.testing.assert_allclose(fm.S, core.S)


def test_external_metabolites_get_no_row():
    fm = FluxModel([({"A": 1}, {"B": 1, "X": 2}, "r1")], external=("X",))
    assert fm.metabolites == ["A", "B"]
    assert fm.S.shape == (2, 1)
    with pytest.raises(ValueError):
        FluxModel([({"A": 1}, {"B": 1}, "r1")], external=("Z",))


def test_duplicate_reaction_names_rejected():
    with pytest.raises(ValueError):
        FluxModel([({"A": 1}, {"B": 1}, "r"), ({"B": 1}, {"A": 1}, "r")])


# --------------------------------------------- the hand derivation, exactly
def test_optimum_is_exactly_four(net):
    m, bounds = net
    best, v = solve_fba(m, "v_biomass", bounds)
    assert best == pytest.approx(4.0, abs=1e-9)
    for name, expected in [("v_uptake", 10.0), ("v_pgi", 6.0), ("v_zwf", 4.0),
                           ("v_tpi", 6.0), ("v_lower", 4.0), ("v_tca", 4.0),
                           ("v_ackA", 0.0), ("v_atpm", 0.0)]:
        assert v[name] == pytest.approx(expected, abs=1e-9), name


def test_branch_point_is_all_or_nothing(net):
    """One arm pays strictly better here, so the optimum takes it outright. (That
    is about THIS network, not about linear programs: see the isozyme test.)"""
    m, bounds = net
    _, v = solve_fba(m, "v_biomass", bounds)
    assert v["v_ackA"] == pytest.approx(0.0, abs=1e-9)
    assert v["v_tca"] > 1.0


def test_lethal_knockouts_are_exactly_zero(net):
    m, bounds = net
    ko = knockout_growth(m, "v_biomass", bounds,
                         ["v_pgi", "v_zwf", "v_tpi", "v_lower",
                          "v_ackA", "v_tca", "v_atpm"])
    for r in ("v_pgi", "v_zwf", "v_tpi", "v_lower"):
        assert ko[r] == 0.0, f"{r} should be lethal, got {ko[r]!r}"
    # and these are NOT lethal -- a test that would fail if everything were zero
    assert ko["v_ackA"] == pytest.approx(4.0, abs=1e-9)
    assert ko["v_atpm"] == pytest.approx(4.0, abs=1e-9)


def test_tca_knockout_moves_the_optimum_to_ten_thirds(net):
    m, bounds = net
    best, v = solve_fba(m, "v_biomass", bounds, knockouts=("v_tca",))
    assert best == pytest.approx(10.0 / 3.0, abs=1e-9)
    assert v["v_tca"] == pytest.approx(0.0, abs=1e-12)
    assert v["v_ackA"] > 1.0          # acetate now carries all the pyruvate


def test_null_space_dimension(net):
    m, _ = net
    assert m.null_space_dimension == len(m.names) - np.linalg.matrix_rank(m.S)
    assert m.null_space_dimension == 3


# ------------------------------------------------------- coupling and atoms
def test_pgi_and_tpi_are_perfectly_coupled(net):
    """F6P has exactly one producer and one consumer, so the network has already
    decided this ratio and no regulation can change it."""
    m, bounds = net
    pairs = coupled_pairs(m, "v_biomass", bounds)
    assert pairs[("v_pgi", "v_tpi")] == pytest.approx(1.0, abs=1e-9)


def test_coupling_finds_these_two_pairs_AND_NO_OTHERS(net):
    """The asserting-one-pair version of this test passed against an
    implementation that returned all 21 pairs of the network's nonzero fluxes,
    because every flux is pinned when the optimum is unique. Pinned is not
    coupled. Name the whole set, so a regression to that behaviour fails."""
    m, bounds = net
    pairs = coupled_pairs(m, "v_biomass", bounds)
    assert set(pairs) == {("v_pgi", "v_tpi"), ("v_zwf", "v_biomass")}
    for ratio in pairs.values():
        assert ratio == pytest.approx(1.0, abs=1e-9)


def test_coupling_does_not_depend_on_the_objective(net):
    """Full coupling is a property of S and the bounds. If the objective can
    change the answer, the function is reporting something else."""
    m, bounds = net
    assert coupled_pairs(m, "v_biomass", bounds) == coupled_pairs(
        m, "v_atpm", bounds)


def test_a_second_route_breaks_the_P5P_coupling():
    """zwf and biomass are coupled only because P5P has ONE producer. Add a
    second and the link is gone, while F6P's pair is untouched."""
    reactions, external, bounds = teaching_network(isozyme=True)
    m = FluxModel(reactions, external=external)
    pairs = coupled_pairs(m, "v_biomass", bounds)
    assert ("v_pgi", "v_tpi") in pairs
    assert ("v_zwf", "v_biomass") not in pairs
    # The two routes share a fixed SUM, not a fixed ratio, so neither pair
    # involving them is coupling.
    assert ("v_zwf", "v_zwf2") not in pairs


def test_every_real_reaction_balances_carbon():
    """The session's thesis is that S counts atoms exactly. Keep it true."""
    reactions, _, _ = teaching_network(isozyme=True)
    for reactants, products, name in reactions:
        if name in PSEUDO:
            continue
        lhs = sum(CARBONS[m] * n for m, n in reactants.items())
        rhs = sum(CARBONS[m] * n for m, n in products.items())
        assert lhs == rhs, f"{name}: {lhs}C -> {rhs}C"


# ------------------------------- the limitation, as a predicate not a sentence
def test_core_network_has_a_unique_optimum(net):
    m, bounds = net
    assert has_alternate_optima(m, "v_biomass", bounds) is False
    for lo, hi in flux_ranges(m, "v_biomass", bounds).values():
        assert hi - lo < 1e-7


def test_isozyme_creates_alternate_optima_without_changing_the_objective():
    """Add a parallel route and the prediction splits in two, invisibly.

    The objective is unchanged, so no growth measurement can distinguish them.
    That is the whole of Mahadevan & Schilling's point, and it is why the slide
    may not present a flux map as 'the' answer.
    """
    r0, e, b = teaching_network()
    r1, _, _ = teaching_network(isozyme=True)
    m0, m1 = FluxModel(r0, external=e), FluxModel(r1, external=e)
    best0, _ = solve_fba(m0, "v_biomass", b)
    best1, _ = solve_fba(m1, "v_biomass", b)
    assert best1 == pytest.approx(best0, abs=1e-9)

    assert has_alternate_optima(m1, "v_biomass", b) is True
    ranges = flux_ranges(m1, "v_biomass", b)
    for r in ("v_zwf", "v_zwf2"):
        lo, hi = ranges[r]
        assert lo == pytest.approx(0.0, abs=1e-7)
        assert hi == pytest.approx(4.0, abs=1e-7)


# ------------------------------------------------------------- failure modes
def test_infeasible_returns_nan_not_an_exception(net):
    """A lethal knockout is an answer, not an error."""
    m, bounds = net
    value, fluxes = solve_fba(m, "v_biomass", bounds, knockouts=("v_zwf",))
    assert value == 0.0 or np.isnan(value) or abs(value) < 1e-9
    bad = dict(bounds); bad["v_uptake"] = (5.0, 1.0)
    with pytest.raises(ValueError):
        solve_fba(m, "v_biomass", bad)


def test_unknown_reaction_names_are_rejected(net):
    m, bounds = net
    with pytest.raises(ValueError):
        solve_fba(m, "v_biomass", bounds, knockouts=("v_nope",))
    with pytest.raises(KeyError):
        solve_fba(m, "v_nope", bounds)


def test_no_uptake_means_no_growth(net):
    m, _ = net
    best, _ = solve_fba(m, "v_biomass", {"v_uptake": (0.0, 0.0)})
    assert abs(best) < 1e-9 or np.isnan(best)


def test_objective_can_be_a_weighted_dict(net):
    m, bounds = net
    a, _ = solve_fba(m, "v_biomass", bounds)
    b, _ = solve_fba(m, {"v_biomass": 2.0}, bounds)
    assert b == pytest.approx(2.0 * a, abs=1e-8)
