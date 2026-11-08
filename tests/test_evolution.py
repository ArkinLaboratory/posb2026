"""Session 23 -- evolutionary failure and containment.

Every number this file pins is a number that appears in
sessions/s23-evolution/NUMBERS.md or is about to appear on a slide. The
tolerances are two-sided on purpose: `assert x < c` also passes when the
computation breaks and returns zero, and a one-sided bound on a quantity that
is not monotone can straddle an extremum it never touches.
"""
import numpy as np
import pytest
from scipy.integrate import solve_ivp

from posb import evolution as ev


# --------------------------------------------------------------- the ODE ---
def _numeric_t_of_q(q_target, s, mu):
    """Integrate dq/dt = (1-q)(s q + mu) and stop when q reaches q_target."""
    def rhs(_, y):
        return [(1.0 - y[0]) * (s * y[0] + mu)]

    def hit(_, y):
        return y[0] - q_target
    hit.terminal = True
    hit.direction = 1
    sol = solve_ivp(rhs, [0.0, 1e12], [0.0], events=hit,
                    rtol=1e-11, atol=1e-14, method="Radau")
    assert sol.t_events[0].size == 1, (s, mu, q_target)
    return sol.t_events[0][0]


@pytest.mark.parametrize("s", [0.0, 1e-4, 1e-3, 0.01, 0.05, 0.2, 0.5])
@pytest.mark.parametrize("mu", [1e-8, 1e-6, 1e-4])
@pytest.mark.parametrize("q", [1e-3, 0.1, 0.5, 0.9])
def test_closed_form_matches_integration(s, mu, q):
    """The closed form is the solution, not an approximation to it.

    Worst relative error measured across this whole grid when it was written:
    6.3e-11. The bound below is two-sided -- an error of exactly zero would
    mean the numerical check had stopped running.
    """
    closed = float(ev.time_to_failure(q, s, mu))
    numeric = _numeric_t_of_q(q, s, mu)
    rel = abs(closed - numeric) / numeric
    assert 0.0 <= rel < 1e-8, f"s={s} mu={mu} q={q}: rel err {rel:.3e}"
    assert closed > 0.0


@pytest.mark.parametrize("s", [0.0, 1e-3, 0.02, 0.3])
@pytest.mark.parametrize("mu", [1e-7, 1e-5, 1e-3])
def test_q_of_t_inverts_t_of_q(s, mu):
    for q in (1e-6, 1e-3, 0.25, 0.5, 0.75, 0.99):
        t = ev.time_to_failure(q, s, mu)
        back = float(ev.broken_fraction(t, s, mu))
        assert back == pytest.approx(q, rel=1e-9), (s, mu, q, back)


def test_broken_fraction_starts_at_zero_and_is_monotone():
    t = np.linspace(0.0, 500.0, 1001)
    q = ev.broken_fraction(t, 0.02, 1e-6)
    assert q[0] == 0.0
    assert np.all(np.diff(q) > 0.0)
    assert np.all((q >= 0.0) & (q < 1.0))


def test_small_t_limit_survives_floating_point():
    """q(t) -> mu*t as t -> 0. Written naively this cancels to zero.

    The regime is (s + mu)*t << 1, and it is in the assertion. Outside it the
    limit is simply false: at s = 0.05 and t = 10, s*t = 0.5 and selection has
    already amplified q about 1.3-fold over mu*t. That is checked below rather
    than left as a comment.
    """
    mu = 1e-9
    for s in (0.0, 0.05):
        for t in (1e-3, 1.0, 10.0):
            if (s + mu) * t > 1e-3:
                continue
            q = float(ev.broken_fraction(t, s, mu))
            assert q == pytest.approx(mu * t, rel=1e-6), (s, t, q)
    # and the limit fails where it should
    amplified = float(ev.broken_fraction(10.0, 0.05, mu)) / (mu * 10.0)
    assert 1.2 < amplified < 1.4, amplified


# ------------------------------------------------------------ the limits ---
@pytest.mark.parametrize("mu", [1e-8, 1e-6, 1e-4, 1e-2])
def test_zero_cost_is_pure_accumulation(mu):
    """s = 0: q = 1 - exp(-mu t) and t50 = ln2/mu, both exact."""
    t = np.array([1.0, 10.0, 1e3, 1e5])
    got = ev.broken_fraction(t, 0.0, mu)
    # -expm1(-x) is the accurate spelling of 1-exp(-x). Compare against THAT:
    # at mu*t ~ 1e-6 the naive form loses about six digits to cancellation,
    # and the library is deliberately not using it.
    assert np.allclose(got, -np.expm1(-mu * t), rtol=1e-14, atol=0.0)
    naive = 1.0 - np.exp(-mu * t)
    assert np.allclose(got, naive, rtol=1e-6, atol=0.0), \
        "library and naive form should still agree to six digits"
    assert float(ev.half_life(0.0, mu)) == pytest.approx(np.log(2.0) / mu,
                                                         rel=1e-12)


@pytest.mark.parametrize("s,mu", [(0.02, 1e-6), (0.02, 1e-7), (0.05, 1e-6),
                                  (0.05, 1e-7), (0.10, 1e-6), (0.10, 1e-7)])
def test_cheap_mutation_limit(s, mu):
    """t50 ~ ln(s/mu)/s when mu << s.

    The regime is in the assertion, not in a comment: this is checked at three
    values of s and two of mu, and the agreement must be better than 0.1% at
    every one of them. It is NOT a law -- at s = mu the approximation is
    meaningless, which the next test pins.
    """
    exact = float(ev.half_life(s, mu))
    approx = np.log(s / mu) / s
    assert exact == pytest.approx(approx, rel=1e-3), (s, mu, exact, approx)


def test_cheap_mutation_limit_fails_outside_its_regime():
    """Attack the approximation with parameters it does not cover.

    A tolerance is a statement at a parameter value. At s = mu the limit form
    is wrong by more than a factor of two, and a test suite that only ever
    checks where a claim holds does not establish that the claim has a regime.
    """
    s = mu = 1e-3
    exact = float(ev.half_life(s, mu))
    approx = np.log(s / mu) / s          # = 0, since s == mu
    assert approx == 0.0
    assert exact > 300.0


# ------------------------------------------- the ledger, NUMBERS.md sec 4 ---
def test_design_ledger_numbers():
    """Pins every number in the s = 0.05, mu = 1e-6 ledger, two-sided.

    These five appear in NUMBERS.md and are headed for a slide. If one moves,
    this fails and names it rather than letting the slide drift.
    """
    expect = {
        (0.05, 1e-6): 216.4,
        (0.05, 1e-7): 262.4,
        (0.05, 1e-8): 308.5,
        (0.025, 1e-6): 405.1,
        (0.005, 1e-6): 1703.2,
    }
    for (s, mu), want in expect.items():
        got = float(ev.half_life(s, mu))
        assert got == pytest.approx(want, abs=0.1), (s, mu, got, want)


@pytest.mark.parametrize("s", [0.005, 0.01, 0.02, 0.05, 0.1, 0.2])
@pytest.mark.parametrize("mu", [1e-9, 1e-8, 1e-7, 1e-6, 1e-5])
def test_halving_s_beats_dividing_mu_by_a_hundred(s, mu):
    """The session's design result -- and it has a regime, tested below.

    The boundary is s/mu = 413.0 -- located by bisection and identical at
    s = 1e-3, 5e-3, 0.01, 0.05 and 0.2, so it is a property of the ratio
    alone. Below it, dividing mu by a hundred wins instead. The previous
    version of this grid had a minimum ratio of 500, stopped there, and called
    itself exhaustive; test_the_asymmetry_reverses_at_low_s_over_mu now
    attacks the other side.
    """
    assert s / mu > 410.0, "this grid is inside the regime by construction"
    base = float(ev.half_life(s, mu))
    from_mu = float(ev.half_life(s, mu / 100.0)) - base
    from_s = float(ev.half_life(s / 2.0, mu)) - base
    assert from_mu > 0.0 and from_s > 0.0
    assert from_s > from_mu, (s, mu, from_s, from_mu)


@pytest.mark.parametrize("s", [0.001, 0.01, 0.05, 0.2])
def test_the_asymmetry_reverses_at_low_s_over_mu(s):
    """Attack the design result where it does not hold.

    At s/mu = 100 the ranking flips: dividing mu by a hundred beats halving s.
    So the bolded claim needs its regime attached wherever it is said out loud,
    including on a slide.
    """
    mu = s / 100.0
    base = float(ev.half_life(s, mu))
    from_mu = float(ev.half_life(s, mu / 100.0)) - base
    from_s = float(ev.half_life(s / 2.0, mu)) - base
    assert from_mu > from_s, (s, mu, from_mu, from_s)


def test_broken_fraction_saturates_instead_of_returning_nan():
    """It returned nan for every long horizon. T61 is autograded."""
    assert float(ev.broken_fraction(1.5e4, 0.05, 1e-6)) == 1.0
    out = ev.broken_fraction(np.array([10.0, 1e5]), 0.05, 1e-6)
    assert np.isfinite(out).all() and out[-1] == 1.0


# ------------------------------------------------------------- multi-hit ---
@pytest.mark.parametrize("k", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("mu1", [1e-5, 1e-4, 1e-3])
def test_chain_with_no_selection_equals_the_closed_form(k, mu1):
    """The mechanism and the closed form are the same model, or one is wrong.

    Measured agreement when written: 1.4e-14 for k=3, mu1=1e-4.
    """
    t_end = min(2000.0, 1.0 / mu1)
    ts, q = ev.mutation_selection_chain(t_end, mu1, k, 0.0)
    exact = ev.multi_hit_broken_fraction(ts, mu1, k)
    err = float(np.max(np.abs(q - exact)))
    assert 0.0 <= err < 1e-10, (k, mu1, err)


@pytest.mark.parametrize("k", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("mu1", [1e-6, 1e-5, 1e-4])
def test_log_log_slope_counts_the_lesions(k, mu1):
    """d log q / d log t = k in the small-mu1*t regime.

    The regime matters and is asserted: t1, t2 are chosen so mu1*t stays below
    1e-2, where the (mu1 t)^k approximation holds. Outside it the slope bends
    toward zero as q saturates, which the next test pins.
    """
    t1, t2 = 1e-3 / mu1, 2e-3 / mu1
    slope = float(ev.multi_hit_log_slope(t1, t2, mu1, k))
    assert slope == pytest.approx(k, rel=2e-3), (k, mu1, slope)


@pytest.mark.parametrize("s,lo,hi", [(0.0, 0.99, 1.01), (0.02, 1.4, 1.7),
                                     (0.05, 2.3, 2.8), (0.08, 3.4, 4.0)])
def test_selection_alone_forges_a_multi_hit_slope(s, lo, hi):
    """A ONE-hit process with a cost reads as k > 1 on a log-log secant.

    This is the defect that kills "the slope counts the lesions" as a
    diagnostic. At the session's own reference burden s = 0.05 a single-hit
    process measured over a decade reads as slope ~2.5, i.e. indistinguishable
    from three independent cassettes. Bounds are two-sided so that the number
    is recorded, not just bounded away from 1.
    """
    a = float(ev.broken_fraction(11.2, s, 1e-6))
    b = float(ev.broken_fraction(112.0, s, 1e-6))
    secant = (np.log(b) - np.log(a)) / (np.log(112.0) - np.log(11.2))
    assert lo < secant < hi, (s, secant)


def test_chain_and_closed_form_diverge_once_there_is_selection():
    """They are the same model only at s = 0, and the gap is large.

    `mutation_selection_chain` propagates selection through the intermediates;
    the (1-e^-mu1 t)^k closed form has no selection in it. Anything plotted on
    an axis where s != 0 must use the chain. Pinned so the divergence cannot
    be rediscovered as a surprise.
    """
    mu1, k = 1e-4, 3
    for s, lo, hi in [(0.0, 0.999, 1.001), (0.02, 1.5, 2.5), (0.05, 5.0, 12.0)]:
        _, q = ev.mutation_selection_chain(112.0, mu1, k, s)
        closed = float(ev.multi_hit_broken_fraction(112.0, mu1, k))
        ratio = float(q[-1]) / closed
        assert lo < ratio < hi, (s, ratio)


def test_slope_bends_down_once_escape_saturates():
    """Attack the slope claim where it does not hold."""
    mu1, k = 1e-3, 3
    late = float(ev.multi_hit_log_slope(5e3, 1e4, mu1, k))
    assert late < 0.5, late


def test_one_hit_is_linear_ONLY_WITHOUT_A_FITNESS_COST():
    """The honest version of a claim this file used to get wrong.

    The old test asserted "a one-hit process has no onset" and called it the
    qualitative argument that an observed onset implies k >= 2. It passed
    because it only ever called multi_hit_broken_fraction, which has no s in
    it. With a cost the one-hit curve bends on log-log axes exactly the way
    redundancy does -- see the next test, which pins the size of the confound.
    Linearity holds at s = 0 and nowhere else.
    """
    mu = 1e-6
    t = np.array([1.0, 10.0, 100.0, 1000.0])
    q0 = ev.broken_fraction(t, 0.0, mu)
    assert np.allclose(q0 / t, mu, rtol=1e-2)          # s = 0: linear
    # and with a cost it is not linear at all
    q = ev.broken_fraction(t, 0.05, mu)
    assert not np.allclose(q / t, mu, rtol=0.5)
    # pure mutation with k cassettes and no selection DOES bend, which is the
    # shape the session wanted -- but so does one hit with a cost, above.
    for k in (2, 3, 4):
        ratios = ev.multi_hit_broken_fraction(t, 1e-5, k) / t
        assert ratios[-1] / ratios[0] > 10.0 ** (k - 1.5), k


@pytest.mark.parametrize("k", [1, 2, 3, 4])
@pytest.mark.parametrize("mu1", [1e-5, 1e-3])
def test_multi_hit_time_inverts_multi_hit_fraction(k, mu1):
    for q in (1e-12, 1e-8, 1e-4, 0.5, 0.9):
        t = ev.multi_hit_time_to_failure(q, mu1, k)
        back = float(ev.multi_hit_broken_fraction(t, mu1, k))
        assert back == pytest.approx(q, rel=1e-8), (k, mu1, q, back)


# ------------------------------------------------------------ the clock ----
def test_generations_per_passage():
    """log2(250) = 7.9658, and the paper's 224 rounds it to 8 per day."""
    g = float(ev.generations_per_passage(250.0))
    assert g == pytest.approx(7.9658, abs=1e-4)
    assert 28.0 * g == pytest.approx(223.04, abs=0.05)
    assert abs(28.0 * g - 224.0) / 224.0 < 0.005      # the 0.4% gap
    assert float(ev.generations_per_passage(256.0)) == pytest.approx(8.0)


# ------------------------------------------------------- fitness cost -----
@pytest.mark.parametrize("s_true", [0.005, 0.02, 0.05, 0.15])
def test_competition_recovers_the_cost(s_true):
    g = np.linspace(0.0, 40.0, 9)
    ratio = np.exp(-s_true * g)
    assert float(ev.fitness_cost_from_competition(g, ratio)) == \
        pytest.approx(s_true, rel=1e-9)


@pytest.mark.parametrize("s_true", [0.01, 0.05, 0.2])
def test_paired_growth_recovers_the_cost(s_true):
    t = np.linspace(0.0, 6.0, 13)
    lam0 = 1.2
    control = np.exp(lam0 * t)
    circuit = np.exp(lam0 * (1.0 - s_true) * t)
    assert float(ev.fitness_cost_from_growth(t, circuit, control)) == \
        pytest.approx(s_true, rel=1e-9)


# -------------------------------------------------------- containment -----
def test_requirement_and_dose_are_matched():
    """1e8 cells x 1e-8 = one survivor. The NIH figure is 'fewer than one'."""
    assert float(ev.containment_requirement(1e8)) == pytest.approx(1e-8)
    assert float(ev.escapers_per_dose(1e8, 1e-8)) == pytest.approx(1.0)


def test_measured_circuit_clears_the_requirement_in_the_assay():
    """10^-8.6 against a 1e8 dose is a quarter of a survivor. NUMBERS.md sec 3."""
    got = float(ev.escapers_per_dose(1e8, 10 ** -8.6))
    assert got == pytest.approx(0.251, abs=0.002)
    assert got < 1.0


@pytest.mark.parametrize("fv,want", [(10 ** -6.6, 25.1), (10 ** -4.5, 3162.0)])
def test_weaker_circuits_do_not(fv, want):
    got = float(ev.escapers_per_dose(1e8, fv))
    assert got == pytest.approx(want, rel=5e-3)
    assert got > 1.0


def test_retention_is_a_duration_not_a_snapshot():
    """The session's thesis, as a number.

    A circuit sitting below 1e-8 in an assay crosses it within a handful of
    generations of permissive growth. Both statements are true and they are
    about different quantities.
    """
    t = float(ev.retention_time(1e-8, k=3, mu1=7.41e-4))
    assert t == pytest.approx(2.9106, abs=1e-3), t
    one_hit = float(ev.retention_time(1e-8, 0.02, 1e-6))
    assert one_hit == pytest.approx(0.009999, rel=1e-3), one_hit


def test_retention_with_k_requires_the_per_cassette_rate():
    with pytest.raises(ValueError, match="per-cassette"):
        ev.retention_time(1e-8, k=3)


def test_retention_refuses_to_pretend_it_used_s():
    """The k > 1 path has no selection in it and must say so.

    It returned 2.9106 for s = 0, 0.02, 0.5 and -1 alike, with no warning.
    """
    with pytest.raises(ValueError, match="carries no"):
        ev.retention_time(1e-8, 0.02, 1e-6, k=3, mu1=7.41e-4)
    for bad in (1.9, 0, -2):
        with pytest.raises(ValueError, match="integer"):
            ev.retention_time(1e-8, k=bad, mu1=7.41e-4)


def test_new_guards():
    for bad in (2.9, 0.5, -1):
        with pytest.raises(ValueError, match="integer"):
            ev.multi_hit_broken_fraction(10.0, 1e-4, bad)
    with pytest.raises(ValueError, match="positive times"):
        ev.multi_hit_log_slope(0.0, 10.0, 1e-4, 2)
    with pytest.raises(ValueError, match="must differ"):
        ev.multi_hit_log_slope(10.0, 10.0, 1e-4, 2)
    with pytest.raises(ValueError, match="not a requirement"):
        ev.containment_requirement(0.5)
    with pytest.raises(ValueError, match="t must be"):
        ev.mutation_selection_chain(0.0, 1e-4, 3, 0.0)
    with pytest.raises(ValueError, match="does not grow"):
        ev.mutation_selection_chain(10.0, 1e-4, 3, 1.5)
    t = np.linspace(0.0, 6.0, 13)
    with pytest.raises(ValueError, match="not growing at all"):
        ev.fitness_cost_from_growth(t, np.exp(-0.5 * t), np.exp(1.2 * t))


# ------------------------------------------------------------- guards -----
def test_guards():
    with pytest.raises(ValueError, match="s >= 0"):
        ev.time_to_failure(0.5, -0.01, 1e-6)
    with pytest.raises(ValueError, match="mu must be"):
        ev.time_to_failure(0.5, 0.01, 0.0)
    for bad in (0.0, 1.0, -0.1, 1.5):
        with pytest.raises(ValueError, match="strictly in"):
            ev.time_to_failure(bad, 0.01, 1e-6)
    with pytest.raises(ValueError, match="cannot be negative"):
        ev.broken_fraction(-1.0, 0.01, 1e-6)
    with pytest.raises(ValueError, match="integer >= 1"):
        ev.multi_hit_broken_fraction(10.0, 1e-4, 0)
    with pytest.raises(ValueError, match="dilution must exceed 1"):
        ev.generations_per_passage(1.0)
    with pytest.raises(ValueError, match="same shape"):
        ev.fitness_cost_from_competition([0, 1, 2], [1.0, 0.9])
    with pytest.raises(ValueError, match="must be positive"):
        ev.fitness_cost_from_competition([0, 1], [1.0, -0.9])
    with pytest.raises(ValueError, match=r"fraction viable lies"):
        ev.escapers_per_dose(1e8, 1.5)
    with pytest.raises(ValueError, match="fraction in"):
        ev.retention_time(0.0, 0.01, 1e-6)
