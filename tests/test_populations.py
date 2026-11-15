"""Session 25 -- diploid packaging, burst output and the two reproductive ratios.

Every number pinned here appears in sessions/s25-populations/NUMBERS.md -- the
reference tables are sec 4b (packaging probabilities), sec 4c (burst
arithmetic), sec 0 (the R0 denominator) and sec 5b (thresholds) -- or is about
to appear on a slide, in which case the design file says so and this file says
which.

HOUSE RULE: closed forms are checked against quadrature or against an
independent computation, NEVER against an ODE solver. There is no ODE in
`posb.populations` and there is no integrator in this file; the independent
computations used instead are scipy's binomial pmf, a seeded urn drawn by
Monte Carlo, quadrature on the analytic derivative, and a bracketed root find
for the threshold crossing.

Tolerances are two-sided on purpose. `assert x < c` also passes when a
computation breaks and returns zero, and a one-sided bound on a quantity that
is not monotone can straddle an extremum it never touches -- which is exactly
what `heterozygote_waste` and `infectious_fraction` do at P = 1. Several
assertions below are equalities to 0.0 or to 1.0 rather than strict
inequalities, because the correct answer at those points IS the boundary and a
test that demanded a strict difference would fail the right answer.
"""
import numpy as np
import pytest
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import binom

from posb import populations as pp

# Table 1 as printed (NUMBERS.md sec 2), with c = 30 and R0 = 1.9375 pinned.
TABLE1 = dict(lam=31.0, k=1.875e-4, n=200.0, c=30.0, d=0.02)
DELTA = 0.7          # death rate of HIV-1-infected cells; the printed slip
R0_PATIENT = 1.9375  # NUMBERS.md sec 0, from Table 1 with the c*d denominator

# A sweep that covers W03's own range of P (1 to 100) and a decade below it.
P_SWEEP = np.logspace(-1.0, 2.0, 1201)


# ------------------------------------------------- the three probabilities ---
def test_the_three_probabilities_sum_to_one():
    """Shown, not asserted -- which is also what the slide has to do.

    Worst absolute deviation from 1 measured across this sweep when written:
    2.2e-16. The bound is two-sided and inclusive, because an exact 1.0 is the
    right answer at every P and is what most of the grid actually returns.
    """
    P = np.concatenate([[0.0], P_SWEEP])
    hiv, het, vec = pp.diploid_packaging(P)
    total = hiv + het + vec
    worst = float(np.max(np.abs(total - 1.0)))
    assert 0.0 <= worst <= 1e-12, f"worst |sum - 1| = {worst:.3e}"
    for p in (hiv, het, vec):
        assert np.all((p >= 0.0) & (p <= 1.0))
    # and at P = 0 there is no vector transcript at all
    hiv0, het0, vec0 = (float(x) for x in pp.diploid_packaging(0.0))
    assert (hiv0, het0, vec0) == (1.0, 0.0, 0.0)


def test_probabilities_match_an_independent_binomial():
    """Two draws at q = P/(1+P), computed by scipy rather than by this module.

    The module writes the three outcomes in P directly; scipy writes them as a
    binomial pmf in q. They are the same model or one of them is wrong.
    """
    q = P_SWEEP / (1.0 + P_SWEEP)
    hiv, het, vec = pp.diploid_packaging(P_SWEEP)
    for j, got in enumerate((hiv, het, vec)):
        want = binom.pmf(j, 2, q)
        assert np.allclose(got, want, rtol=1e-12, atol=0.0), j


@pytest.mark.parametrize("P,p_hiv,p_het,p_vec,p_inf", [
    (1,   0.2500,    0.5000,    0.2500,  0.5000),
    (3,   0.0625,    0.3750,    0.5625,  0.6250),
    (10,  0.008264,  0.16529,   0.82645, 0.8347),
    (30,  0.0010406, 0.062435,  0.93652, 0.9376),
    (100, 9.8030e-5, 0.0196059, 0.98029, 0.9804),
])
def test_reference_values_from_numbers_4b(P, p_hiv, p_het, p_vec, p_inf):
    """The autograder's own table. If one of these moves, T67 moves with it."""
    hiv, het, vec = (float(x) for x in pp.diploid_packaging(P))
    assert hiv == pytest.approx(p_hiv, rel=1e-4)
    assert het == pytest.approx(p_het, rel=1e-4)
    assert vec == pytest.approx(p_vec, rel=1e-4)
    assert hiv + het + vec == pytest.approx(1.0, rel=1e-14)
    inf = float(pp.infectious_fraction(P))
    assert inf == pytest.approx(p_inf, rel=1e-4)
    # the infectious fraction IS the two homozygotes, exactly
    assert inf == pytest.approx(hiv + vec, rel=1e-14)
    assert float(pp.heterozygote_waste(P)) == pytest.approx(het, rel=1e-14)


@pytest.mark.parametrize("P", [1.0, 3.0, 10.0])
def test_a_drawn_urn_reproduces_the_probabilities(P):
    """The object before the model: draw the urn and count the capsids.

    400,000 capsids, two draws each, seeded. The standard error on the worst
    cell here is 6.8e-4, so 0.005 is about seven sigma -- loose enough not to
    flake and tight enough that a wrong q fails it.
    """
    rng = np.random.default_rng(2511)
    q = P / (1.0 + P)
    draws = rng.random((400_000, 2)) < q          # True = a vector strand
    k = draws.sum(axis=1)
    seen = np.array([np.mean(k == j) for j in (0, 1, 2)])
    assert float(seen.sum()) == pytest.approx(1.0, rel=1e-14)
    want = np.array([float(x) for x in pp.diploid_packaging(P)])
    worst = float(np.max(np.abs(seen - want)))
    assert 0.0 <= worst < 0.005, f"P={P}: {seen} vs {want}"


def test_unnormalized_is_the_paper_ratio_and_differs_by_one_plus_P_squared():
    """W03 prints 1 : 2P : P^2. The two forms differ by (1+P)^2 -- except at
    P = 0, where (1+P)^2 = 1 and they coincide exactly.

    That last clause is why this test does not assert a strictly positive
    difference anywhere: at P = 0 the correct difference is 0.0.
    """
    P = P_SWEEP
    u_hiv, u_het, u_vec = pp.diploid_packaging(P, normalized=False)
    assert np.allclose(u_hiv, 1.0, rtol=0.0, atol=0.0)
    assert np.allclose(u_het, 2.0 * P, rtol=1e-15, atol=0.0)
    assert np.allclose(u_vec, P * P, rtol=1e-15, atol=0.0)
    n_hiv, n_het, n_vec = pp.diploid_packaging(P, normalized=True)
    scale = (1.0 + P) ** 2
    for norm, unnorm in ((n_hiv, u_hiv), (n_het, u_het), (n_vec, u_vec)):
        assert np.allclose(norm * scale, unnorm, rtol=1e-12, atol=0.0)
    # the gap is a factor, and it is large over the paper's own range
    assert float(np.min(scale)) == pytest.approx(1.21, rel=1e-12)
    assert float(np.max(scale)) == pytest.approx(10201.0, rel=1e-12)
    # P = 0: identical, and asserted as such rather than as a difference
    at0 = [float(x) for x in pp.diploid_packaging(0.0, normalized=True)]
    un0 = [float(x) for x in pp.diploid_packaging(0.0, normalized=False)]
    assert at0 == un0 == [1.0, 0.0, 0.0]


# -------------------------------------------------- the non-monotone pair ---
def test_heterozygote_waste_is_maximal_at_P_one_by_a_fine_sweep():
    """Maximal at P = 1 and EXACTLY one half there -- by 20,001 points.

    A fine sweep rather than sampled points, because the quantity is
    non-monotone and a coarse grid straddles the extremum. The grid is built
    to contain P = 1 exactly and that is asserted before anything is read off
    it, since logspace landing on 1.0 is a property of the point count.
    """
    P = np.logspace(-2.0, 2.0, 20001)
    assert P[10000] == 1.0, "this sweep must contain P = 1 exactly"
    w = pp.heterozygote_waste(P)
    assert int(np.argmax(w)) == 10000
    assert float(w[10000]) == 0.5          # exact in binary: 2*1/2^2
    assert np.all(w <= 0.5)
    off = np.delete(w, 10000)
    assert float(np.max(off)) < 0.5
    # one sign change in the difference, at the maximum and nowhere else
    signs = np.sign(np.diff(w))
    assert np.all(signs[:10000] > 0.0) and np.all(signs[10000:] < 0.0)
    # the complement identity, across the whole sweep. Exact in exact
    # arithmetic; in floating point the two closed forms round separately and
    # 1.0 - f costs another ulp, so the measured gap is 4.4e-16 -- two ulps of
    # 1.0. Bounded absolutely rather than relatively, and bounded below at
    # 0.0, because 0.0 is a perfectly good answer here.
    gap = float(np.max(np.abs(w - (1.0 - pp.infectious_fraction(P)))))
    assert 0.0 <= gap <= 1e-15, f"complement identity off by {gap:.3e}"


def test_a_coarse_grid_misses_the_maximum_by_eleven_percent():
    """The mistake this course has already shipped once, made executable.

    Four sampled points that straddle P = 1 report a maximum of 4/9, not 1/2.
    Anyone reading the ceiling off such a grid under-reports the waste by 11%
    and would have no reason to put a derivative on a slide.
    """
    coarse = np.array([0.2, 0.5, 2.0, 5.0])
    seen = float(np.max(pp.heterozygote_waste(coarse)))
    assert 0.444 < seen < 0.445
    assert seen == pytest.approx(4.0 / 9.0, rel=1e-12)
    assert seen < 0.5
    assert 0.11 < 1.0 - seen / 0.5 < 0.12


@pytest.mark.parametrize("P", [0.5, 1.0, 3.0, 10.0, 100.0])
def test_the_derivative_slide_integrates_back_to_the_waste(P):
    """Quadrature on (2 - 2P)/(1+P)^3, which is move 2's own slide.

    The derivative is taught on a slide of its own and is not a function in
    the module, so it is checked here instead: integrating it from 0 must
    return 2P/(1+P)^2, since the waste vanishes at P = 0.
    """
    got = quad(lambda x: (2.0 - 2.0 * x) / (1.0 + x) ** 3, 0.0, P,
               limit=200)[0]
    assert got == pytest.approx(float(pp.heterozygote_waste(P)), rel=1e-9)


def test_the_derivative_vanishes_only_at_P_one():
    """And it is exactly zero there, not merely small.

    Asserted as an equality. A test that demanded |derivative| > 0 at the
    extremum would fail the correct answer, which is how this suite has been
    wrong before.
    """
    def dwdP(x):
        return (2.0 - 2.0 * x) / (1.0 + x) ** 3
    assert dwdP(1.0) == 0.0
    assert dwdP(0.9) > 0.0 and dwdP(1.1) < 0.0
    assert brentq(dwdP, 0.1, 10.0) == pytest.approx(1.0, rel=1e-12)


def test_infectious_fraction_falls_then_rises():
    """Decreasing on (0, 1), increasing on P > 1, minimum exactly 0.5 at P = 1.

    An earlier specification called this monotone increasing on (0, infinity);
    the falling branch is the half that was wrong, and both branches are
    asserted here so that neither can be dropped.
    """
    below = np.logspace(-2.0, 0.0, 2001)
    above = np.logspace(0.0, 2.0, 2001)
    assert below[-1] == 1.0 and above[0] == 1.0
    f_lo, f_hi = pp.infectious_fraction(below), pp.infectious_fraction(above)
    assert np.all(np.diff(f_lo) < 0.0), "must DECREASE on (0, 1)"
    assert np.all(np.diff(f_hi) > 0.0), "must INCREASE on P > 1"
    assert float(f_lo[-1]) == 0.5 and float(f_hi[0]) == 0.5
    assert float(np.min(np.concatenate([f_lo, f_hi]))) == 0.5
    # tends to 1 at both ends, and is strictly below 1 for every P > 0
    for end in (1e-6, 1e6):
        v = float(pp.infectious_fraction(end))
        assert 1.0 - 1e-5 < v < 1.0
    # equal to 1 at P = 0 exactly: the boundary is the right answer there
    assert float(pp.infectious_fraction(0.0)) == 1.0
    # the explicit counterexample to "monotone increasing"
    assert float(pp.infectious_fraction(0.5)) == pytest.approx(1.25 / 2.25,
                                                               rel=1e-14)
    assert float(pp.infectious_fraction(0.5)) > float(
        pp.infectious_fraction(1.0))


# ------------------------------------------------------- the burst ledger ---
@pytest.mark.parametrize("P,D,hiv,vec,total", [
    (1,   1.0, 200.0, 200.0,     800.0),
    (3,   0.2,  40.0, 360.0,     640.0),
    (10,  0.4,  80.0, 8000.0,   9680.0),
    (20,  0.5, 100.0, 40000.0, 44100.0),
    (30,  0.4,  80.0, 72000.0, 76880.0),
    (100, 0.4,  80.0, 800000.0, 816080.0),
    (100, 1.0, 200.0, 2000000.0, 2040200.0),
])
def test_burst_reference_values_from_numbers_4c(P, D, hiv, vec, total):
    """W03's own per-cell output, n = 200. Scaling model."""
    got_hiv, got_het, got_vec = (float(x) for x in pp.burst_output(P, D))
    assert got_hiv == pytest.approx(hiv, rel=1e-12)
    assert got_vec == pytest.approx(vec, rel=1e-12)
    assert got_hiv + got_het + got_vec == pytest.approx(total, rel=1e-12)
    assert got_het == pytest.approx(2.0 * P * D * 200.0, rel=1e-12)


@pytest.mark.parametrize("n", [200.0, 1000.0])
def test_scaling_mode_totals_one_plus_P_squared_times_D_n(n):
    """The defining property of W03's model: it SCALES the burst.

    Checked across the paper's own sweeps -- P from 1 to 100 (Table 1) and n
    from 200 to 1,000 (Table 1 footnote a) -- against the total computed
    independently as (1+P)^2*D*n.
    """
    P = np.logspace(0.0, 2.0, 201)
    for D in (0.01, 0.2, 0.4, 0.5, 1.0):
        hiv, het, vec = pp.burst_output(P, D, n=n)
        total = hiv + het + vec
        want = (1.0 + P) ** 2 * D * n
        assert np.allclose(total, want, rtol=1e-12, atol=0.0), D


def test_the_headline_design_point_needs_four_thousand_bursts():
    """P = 100, D = 0.4: 816,080 virions from one cell.

    Against n = 200 measured in vivo and the 40,000 W03 cites for env-deleted
    SIV from unpublished data, which is the largest output the paper can
    point to. Both ratios are bounded two-sided so the numbers are recorded.
    """
    total = float(sum(pp.burst_output(100, 0.4)))
    assert total == pytest.approx(816080.0, rel=1e-12)
    assert 4080.0 < total / 200.0 < 4081.0
    assert 20.3 < total / 40000.0 < 20.5


@pytest.mark.parametrize("P", [1.0, 3.0, 10.0, 30.0, 100.0])
@pytest.mark.parametrize("D", [0.01, 0.2, 0.4, 1.0])
def test_fixed_mode_totals_exactly_n(P, D):
    """The capped-packaging model: the cell makes n particles whatever happens.

    Exact to machine precision rather than approximately n, and the
    composition is still the binomial.
    """
    hiv, het, vec = (float(x) for x in pp.burst_output(P, D, fixed=True))
    assert hiv + het + vec == pytest.approx(200.0, rel=1e-12)
    probs = [float(x) for x in pp.diploid_packaging(P)]
    for got, p in zip((hiv, het, vec), probs):
        assert got == pytest.approx(200.0 * p, rel=1e-14)


def test_fixed_mode_vector_output_is_independent_of_D():
    """THE SESSION'S OWN COUNTEREXAMPLE, EXECUTABLE.

    Sweep D over its whole range, including both ends, and the vector's
    output does not move at all -- the spread is exactly 0.0, which is
    asserted as an equality because that is the right answer. With D gone from
    the vector's output, R0_T loses its D, the shared-production-term argument
    collapses and move 4's own title is false in this model.

    The same sweep in the scaling model moves the vector's output by the full
    factor of 100 that D spans, which is what makes this a contrast rather
    than a broken function.
    """
    D = np.linspace(0.01, 1.0, 25)
    for P in (1.0, 5.0, 30.0, 100.0):
        _, _, vec_fixed = pp.burst_output(P, D, fixed=True)
        vec_fixed = np.broadcast_to(np.asarray(vec_fixed, float), D.shape)
        assert float(np.ptp(vec_fixed)) == 0.0, P
        assert float(vec_fixed[0]) == pytest.approx(
            200.0 * P * P / (1.0 + P) ** 2, rel=1e-14)
        _, _, vec_scaled = pp.burst_output(P, D)
        assert float(np.max(vec_scaled) / np.min(vec_scaled)) == \
            pytest.approx(100.0, rel=1e-12)


def test_the_capped_model_at_the_headline_point():
    """NUMBERS.md sec 4c: 196 vector, about 4 heterozygotes, 0.02 HIV-1.

    One HIV-1 particle per 51 dually infected cells, which is the number the
    slide carries.
    """
    hiv, het, vec = (float(x) for x in pp.burst_output(100, 0.4, fixed=True))
    assert 196.0 < vec < 196.1
    assert 3.9 < het < 3.95
    assert 0.0196 < hiv < 0.0197
    assert 50.9 < 1.0 / hiv < 51.1


# --------------------------------------------------------------- the ratios ---
def test_basic_R0_reproduces_table_1():
    """1.9375, and the independent route to it is the ratio of steady states.

    T* = c/(k*n) = 800 is exactly Table 1's T0 and lambda/d = 1550 is the
    healthy CD4 count, so R0 = 1550/800. Both are computed here rather than
    taken from the function under test.
    """
    got = float(pp.basic_R0(**TABLE1))
    assert got == pytest.approx(1.9375, rel=1e-12)
    T_star = TABLE1["c"] / (TABLE1["k"] * TABLE1["n"])
    T_zero = TABLE1["lam"] / TABLE1["d"]
    assert T_star == pytest.approx(800.0, rel=1e-12)
    assert T_zero == pytest.approx(1550.0, rel=1e-12)
    assert got == pytest.approx(T_zero / T_star, rel=1e-12)


def test_the_printed_c_delta_denominator_gives_an_impossible_value():
    """The slip the session teaches, run rather than described.

    W03 prints R0 = lambda*k*n/(c*delta). With delta = 0.7 that is 0.0554 --
    a virus that cannot sustain an infection, in a patient who demonstrably
    has one. The two values differ by exactly delta/d = 35, and the
    coefficient 1 - 1/R0 goes to -17.06, so no figure in the paper could
    exist. `therapeutic_R0` refuses such an R0 rather than returning a
    negative reproductive ratio.
    """
    wrong = float(pp.basic_R0(**{**TABLE1, "d": DELTA}))
    assert 0.0553 < wrong < 0.0554
    assert wrong < 1.0
    assert float(pp.basic_R0(**TABLE1)) / wrong == pytest.approx(
        DELTA / TABLE1["d"], rel=1e-12)
    assert -17.07 < 1.0 - 1.0 / wrong < -17.06
    with pytest.raises(ValueError, match="ESTABLISHED"):
        pp.therapeutic_R0(100.0, 0.4, wrong)


@pytest.mark.parametrize("P,D,want", [
    (1,   1.0,  0.4839),
    (3,   0.4,  1.742),
    (10,  0.4,  19.35),
    (20,  0.5,  96.77),
    (30,  0.4,  174.2),
    (100, 0.4,  1935.0),
    (100, 0.01, 48.39),
])
def test_therapeutic_R0_reference_values_from_numbers_5b(P, D, want):
    got = float(pp.therapeutic_R0(P, D, R0_PATIENT))
    assert got == pytest.approx(want, rel=1e-3)


def test_therapeutic_R0_crosses_one_at_P2D_equal_2_0667():
    """Bracketed on both sides, and located independently by a root find.

    The crossing is a property of the PRODUCT P^2*D, so it is swept in the
    product: below 2.0667 the therapy dies out, above it it invades.
    """
    def r0t_of_product(prod):
        return float(pp.therapeutic_R0(np.sqrt(prod), 1.0, R0_PATIENT))

    assert r0t_of_product(2.06) < 1.0
    assert r0t_of_product(2.07) > 1.0
    assert r0t_of_product(2.0666667) == pytest.approx(1.0, abs=1e-6)
    root = brentq(lambda x: r0t_of_product(x) - 1.0, 1.0, 5.0, xtol=1e-12)
    assert root == pytest.approx(2.0666667, rel=1e-6)
    # and the same threshold reached through D instead of P
    assert r0t_of_product(2.0666667 * 0.999) < 1.0 < \
        r0t_of_product(2.0666667 * 1.001)


def test_the_poll_2_arithmetic():
    """DESIGN.md sec 5, poll 2: P pinned at 5, D from 0.2 to 0.02.

    A tenfold better cargo takes R0_T from 2.42 to 0.242 and the therapy dies
    out. The poll has one defensible answer only because P is on the stem, so
    the pair is pinned here together.
    """
    strong = float(pp.therapeutic_R0(5.0, 0.2, R0_PATIENT))
    better = float(pp.therapeutic_R0(5.0, 0.02, R0_PATIENT))
    assert 2.41 < strong < 2.43 and strong > 1.0
    assert 0.241 < better < 0.243 and better < 1.0
    assert strong / better == pytest.approx(10.0, rel=1e-12)


def test_proportionality_is_a_predicate_over_an_established_infection():
    """R0_T is PROPORTIONAL to P^2*D, with the coefficient swept.

    Over R0 in [1.9, 20] -- any established infection -- the coefficient
    1 - 1/R0 stays inside (0.47, 0.96) and the implied threshold on P^2*D
    stays inside [1.04, 2.13]. Endpoints recorded: 0.4737 and 2.1111 at
    R0 = 1.9, 0.95 and 1.0526 at R0 = 20.

    Proportionality itself is asserted as an identity: R0_T/(P^2*D) does not
    depend on P or on D.
    """
    R0 = np.linspace(1.9, 20.0, 1901)
    coeff = 1.0 - 1.0 / R0
    thresh = 1.0 / coeff
    assert np.all((coeff > 0.47) & (coeff < 0.96))
    assert np.all((thresh >= 1.04) & (thresh <= 2.13))
    assert float(coeff[0]) == pytest.approx(0.473684, rel=1e-5)
    assert float(thresh[0]) == pytest.approx(2.111111, rel=1e-5)
    assert float(coeff[-1]) == pytest.approx(0.95, rel=1e-12)
    assert float(thresh[-1]) == pytest.approx(1.052632, rel=1e-5)
    for r in (1.9375, 2.5, 5.0, 19.375):
        c = 1.0 - 1.0 / r
        for P, D in ((1.0, 1.0), (3.0, 0.4), (100.0, 0.01)):
            got = float(pp.therapeutic_R0(P, D, r))
            assert got / (P * P * D) == pytest.approx(c, rel=1e-14)


def test_the_band_is_false_below_R0_1_9():
    """Why the sweep stops at 1.9 and must not be widened to 1.2.

    At R0 = 1.2 the threshold on P^2*D is exactly 6.0, three times the top of
    the [1.04, 2.13] band, so the claimed band would be false and the
    autograded 2.0667 would look like one point in a range that does not
    contain it.
    """
    thresh_12 = 1.0 / (1.0 - 1.0 / 1.2)
    assert 5.999 < thresh_12 < 6.001
    assert thresh_12 > 2.13
    assert float(pp.therapeutic_R0(np.sqrt(2.0666667), 1.0, 1.2)) < 0.35


def test_approximating_R0_T_as_P2D_understates_the_threshold():
    """The defect a slide saying "R0_T ~ P^2 D" would ship.

    The coefficient at this patient's R0 is about one half, so a student
    solving P^2*D > 1 at D = 0.2 gets sqrt(5) = 2.236 where the session pins
    3.2146 -- short by a factor of sqrt(2.0667) = 1.4376, and on the wrong
    side of the contour every figure draws.
    """
    coeff = 1.0 - 1.0 / R0_PATIENT
    assert 0.483 < coeff < 0.484
    naive = float(np.sqrt(1.0 / 0.2))
    pinned = float(pp.P_min(0.2, R0_PATIENT))
    assert naive == pytest.approx(2.23607, rel=1e-5)
    assert naive < pinned
    assert pinned / naive == pytest.approx(np.sqrt(1.0 / coeff), rel=1e-12)
    assert 1.43 < pinned / naive < 1.44
    # a construct at the naive P does NOT persist, which is the whole point
    assert float(pp.therapeutic_R0(naive, 0.2, R0_PATIENT)) < 1.0


# ------------------------------------------------------- the two thresholds ---
@pytest.mark.parametrize("D,p_squared,p_min", [
    (1.0,  2.0667, 1.4376),
    (0.5,  4.1333, 2.0331),
    (0.4,  5.1667, 2.2730),
    (0.3,  6.8889, 2.6247),
    (0.2,  10.333, 3.2146),
    (0.1,  20.667, 4.5461),
    (0.01, 206.67, 14.376),
])
def test_P_min_reference_values_from_numbers_5b(D, p_squared, p_min):
    """The P_min column of sec 5b, and the column beside it.

    NOTE THE HEADER ON THAT MIDDLE COLUMN. NUMBERS.md calls it "P^2 D
    threshold", but 4.1333 at D = 0.5 is 2.0667/D, so the entries are the
    threshold on P^2 ALONE -- the product P^2*D is 2.0667 at every row, which
    is the whole content of the threshold. Both are asserted here so the
    mislabeling cannot propagate into an item.
    """
    got = float(pp.P_min(D, R0_PATIENT))
    assert got == pytest.approx(p_min, rel=1e-4)
    assert got * got == pytest.approx(p_squared, rel=1e-4)
    assert got * got * D == pytest.approx(2.0666667, rel=1e-6)
    assert float(pp.therapeutic_R0(got, D, R0_PATIENT)) == pytest.approx(
        1.0, rel=1e-12)


@pytest.mark.parametrize("R0", [1.9375, 3.0, 10.0, 19.375])
@pytest.mark.parametrize("D", [0.01, 0.1, 0.2, 0.4, 0.5, 1.0])
def test_P_min_round_trips(R0, D):
    """P_min, then D_min, then back. Both are roots of R0_T = 1."""
    P = float(pp.P_min(D, R0))
    assert float(pp.therapeutic_R0(P, D, R0)) == pytest.approx(1.0, rel=1e-12)
    assert float(pp.D_min(P, R0)) == pytest.approx(D, rel=1e-12)


@pytest.mark.parametrize("R0", [1.9375, 3.0, 10.0, 19.375])
@pytest.mark.parametrize("P", [2.0, 4.0, 8.0, 16.0, 100.0])
def test_D_min_round_trips(R0, P):
    """And the other direction, which is what segment 3's release asks for.

    P is kept above 1.4376 so that D_min lands inside [0, 1]; the P below
    which no admissible D exists is pinned separately.
    """
    D = float(pp.D_min(P, R0))
    assert 0.0 < D <= 1.0
    assert float(pp.therapeutic_R0(P, D, R0)) == pytest.approx(1.0, rel=1e-12)
    assert float(pp.P_min(D, R0)) == pytest.approx(P, rel=1e-12)


def test_D_min_answers_segment_3_release():
    """A construct measured at P = 8: what D does it need?

    2.0667/64 = 0.0323. D is the fraction of HIV-1 production REMAINING, so
    this is a floor on D and a ceiling on the drug: suppress by at most about
    96.8% or the vector cannot spread.
    """
    got = float(pp.D_min(8.0, R0_PATIENT))
    assert 0.030 < got < 0.035
    assert got == pytest.approx(2.0666667 / 64.0, rel=1e-6)
    assert float(pp.therapeutic_R0(8.0, got, R0_PATIENT)) == pytest.approx(
        1.0, rel=1e-12)
    # below P_min(D = 1) no admissible D exists, and the value says so
    assert float(pp.D_min(1.0, R0_PATIENT)) == pytest.approx(2.0666667,
                                                             rel=1e-6)
    assert float(pp.D_min(1.0, R0_PATIENT)) > 1.0
    assert float(pp.D_min(1.4376, R0_PATIENT)) == pytest.approx(1.0, rel=1e-4)


# -------------------------------------------------------------- the guards ---
def test_P_zero_is_allowed_because_it_is_a_real_answer():
    """No vector transcript at all is a state, not an error.

    Attacked with the right answer: the probabilities are (1, 0, 0), the
    infectious fraction is exactly 1.0 and the waste is exactly 0.0. A guard
    that rejected P = 0, or a test that demanded a positive waste, would both
    be wrong here.
    """
    assert [float(x) for x in pp.diploid_packaging(0.0)] == [1.0, 0.0, 0.0]
    assert float(pp.infectious_fraction(0.0)) == 1.0
    assert float(pp.heterozygote_waste(0.0)) == 0.0
    hiv, het, vec = (float(x) for x in pp.burst_output(0.0, 0.4))
    assert (hiv, het, vec) == (80.0, 0.0, 0.0)
    assert float(pp.therapeutic_R0(0.0, 0.4, R0_PATIENT)) == 0.0


def test_guards():
    for bad in (-1e-9, -1.0):
        with pytest.raises(ValueError, match="cannot be negative"):
            pp.diploid_packaging(bad)
        with pytest.raises(ValueError, match="cannot be negative"):
            pp.infectious_fraction(np.array([1.0, bad]))
    with pytest.raises(ValueError, match="must be finite"):
        pp.heterozygote_waste(np.inf)
    for bad in (-0.01, 1.01, 2.0):
        with pytest.raises(ValueError, match=r"lies in \[0, 1\]"):
            pp.burst_output(10.0, bad)
    with pytest.raises(ValueError, match="burst size"):
        pp.burst_output(10.0, 0.4, n=0.0)
    for bad in (1.0, 0.9, 0.0553, -2.0):
        with pytest.raises(ValueError, match="ESTABLISHED"):
            pp.therapeutic_R0(10.0, 0.4, bad)
        with pytest.raises(ValueError, match="ESTABLISHED"):
            pp.P_min(0.4, bad)
        with pytest.raises(ValueError, match="ESTABLISHED"):
            pp.D_min(10.0, bad)
    with pytest.raises(ValueError, match="at D = 0 no P persists"):
        pp.P_min(0.0, R0_PATIENT)
    with pytest.raises(ValueError, match="at D = 0 no P persists"):
        pp.P_min(np.array([0.2, 0.0]), R0_PATIENT)
    with pytest.raises(ValueError, match="never packaged"):
        pp.D_min(0.0, R0_PATIENT)
    for bad in ("lam", "k", "n", "c", "d"):
        with pytest.raises(ValueError, match="must be"):
            pp.basic_R0(**{**TABLE1, bad: 0.0})


# ---------------------------------------------------------------------------
# coexistence() -- moved out of figures/s25_populations.py on 9 November 2026
# so PS9's autograder and the deck's figure solve the same equilibrium.
# ---------------------------------------------------------------------------

def test_coexistence_reproduces_the_set_points_the_deck_draws():
    """The three points s25_setpoint_valley overlays on W03's own panel."""
    from posb.populations import coexistence
    for D, want in ((0.8, 5.880e4), (0.6, 1.797e4), (0.4, 776.5)):
        got = coexistence(30.0, D)["V"] * 1000.0
        assert abs(got / want - 1.0) < 2e-3, (D, got, want)


def test_coexistence_returns_none_exactly_where_R0T_falls_below_one():
    """No equilibrium is not a solver failure -- it is R_0^T < 1.

    NUMBERS.md 20.3: at P = 30 the wall is D = 0.0022963.
    """
    from posb.populations import coexistence, therapeutic_R0
    R0 = 31 / 16
    for D in (0.0020, 0.0022, 0.00229):
        assert therapeutic_R0(30.0, D, R0) < 1.0
        assert coexistence(30.0, D) is None, D
    for D in (0.0023, 0.0024, 0.01, 0.5):
        assert therapeutic_R0(30.0, D, R0) > 1.0
        assert coexistence(30.0, D) is not None, D


def test_coexistence_does_not_depend_on_delta_prime():
    """delta' cancels out of all five lines (NUMBERS.md 18.2, 20.1).

    This is the property that lets the set-point figure ship while the
    time-course redraw could not: the clock is wrong, the fixed point is not.
    """
    from posb.populations import coexistence
    base = coexistence(30.0, 0.3)
    for delta in (0.35, 0.7, 1.4, 7.0):
        other = coexistence(30.0, 0.3, delta=delta)
        for key in ("T", "V", "IT"):
            assert abs(other[key] / base[key] - 1.0) < 1e-9, (delta, key)


def test_the_set_point_is_NOT_a_function_of_P_squared_D_alone():
    """The THRESHOLD depends only on P^2 D. The SET POINT does not.

    Written because the opposite was asserted in a docstring and this test
    caught it on 9 November 2026. `_v_of` is a function of A = P^2 D alone,
    which makes the claim look right -- but T is fixed by a residual
    carrying I_T = (c/(kn) - T)/D, so D enters separately.

    Holding A exactly constant, the set point moves by a factor of ~82
    across the range where D is a legal fraction.
    That is the over-generalisation to catch in a student who has just spent
    seventeen slides on R_0^T = P^2 D (1 - 1/R_0).
    """
    from posb.populations import coexistence, therapeutic_R0
    R0 = 31 / 16
    A = 30.0 ** 2 * 0.3
    vs, r0ts = [], []
    for P in (20.0, 30.0, 100.0):
        D = A / (P * P)
        vs.append(coexistence(P, D)["V"])
        r0ts.append(therapeutic_R0(P, D, R0))
    # the threshold IS a function of the product, to machine precision
    assert max(r0ts) / min(r0ts) - 1.0 < 1e-12
    # the set point emphatically is not
    assert max(vs) / min(vs) > 50.0


def test_coexistence_therapy_costs_uninfected_cells():
    """T* = c/(kn) - D*I_T, so T* is always BELOW the pretherapy 800/ul."""
    from posb.populations import coexistence
    t_pre = 30.0 / (1.875e-4 * 200.0)
    assert abs(t_pre - 800.0) < 1e-9
    for D in (0.01, 0.2, 0.4, 0.8):
        st = coexistence(30.0, D)
        assert st["T"] < t_pre
        assert abs((t_pre - st["T"]) / D - st["IT"]) < 1e-9, D
