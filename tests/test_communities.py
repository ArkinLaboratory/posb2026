"""Session 24 -- the wire outside the cell, the band detector, and the Hopf.

Every number this file pins comes from sessions/s24-communities/NUMBERS.md,
from the papers it indexes, or from decks/s02_substrate.py, and the test says
which. Three standing rules, all of them learned here the hard way:

NO ODE SOLVER ANYWHERE IN THIS FILE. Every quantity in posb.communities is a
closed form or the root of one, so an integrator checking it mostly measures
the integrator -- the previous session shipped three error figures that were
all doing exactly that. The independent computations below are quadrature-free
by construction: a formula written out a second way, a central difference, a
scaling law, or an exact rational value.

BOUNDS ARE TWO-SIDED. `assert x < c` also passes when the computation breaks
and returns zero, and a one-sided bound on a non-monotone quantity can straddle
an extremum it never touches.

AND EVERY ASSERTION IS ATTACKED WITH THE RIGHT ANSWER TOO. A test in this
repository once failed the correct answer by demanding a strictly positive
difference where the exact answer is 0.0. Where an exact answer here is 0.0 --
the residual at a fixed point, the trace at the Hopf, the gap between the three
burden forms at zero burden -- the bound admits it and says so.

WHAT IS DELIBERATELY NOT TESTED. There is no predicate on Balagadde's
oscillatory window. The window (roughly 0.04-0.18 h^-1) is this repository's
one-significant-figure digitization of their Fig. 3C, and the model in
posb.communities is the course's rather than theirs, so a test on it would
freeze an accident in place. The model-against-data mismatch is taught as a
reading of their figure and is not asserted in code.
"""
import inspect
import pathlib

import numpy as np
import pytest
from scipy.optimize import brentq

from posb import communities as cm

ROOT = pathlib.Path(__file__).resolve().parent.parent
S02 = ROOT / "decks" / "s02_substrate.py"


# ======================================================================
# T66, part one -- the diffusion time, and session 2's convention
# ======================================================================
def test_diffusion_time_reproduces_session_2s_printed_numbers():
    """The three numbers printed on session 2's answer slide, to its own digits.

    decks/s02_substrate.py, the slide badged "63 - 67 min" and titled
    "Items 1 to 3, and the sign of every assumption". Items 2 and 3 print:

        t ~ L^2/2D = (1 um)^2 / (2 x 7.7 um^2/s) ~ 65 ms
        t ~ (20 um)^2 / (2 x 7.7 um^2/s) ~ 26 s, so ~400x longer
        [and in water] 11x higher, so it would have given ~6 ms

    with D(GFP) in E. coli cytoplasm = 7.7 um^2/s (Elowitz 1999) and D(GFP) in
    water = 87 um^2/s. If this module and that slide ever disagree the course
    has two conventions, which is the thing session 2's closing slide exists
    to forbid.
    """
    # L in um, D in um^2/s, so t comes out in seconds.
    assert float(cm.diffusion_time(1.0, 7.7)) == pytest.approx(0.0649350649,
                                                               rel=1e-9)
    assert round(float(cm.diffusion_time(1.0, 7.7)) * 1e3) == 65      # 65 ms
    assert float(cm.diffusion_time(20.0, 7.7)) == pytest.approx(25.974026,
                                                                rel=1e-7)
    assert round(float(cm.diffusion_time(20.0, 7.7))) == 26           # 26 s
    assert round(float(cm.diffusion_time(1.0, 87.0)) * 1e3) == 6      # 6 ms

    # "so ~400x longer. Because t goes as L^2, not L." The ratio is exactly
    # 400 because D cancels -- that is the slide's point and it is not a
    # rounded number, so it is asserted exactly.
    ratio = (float(cm.diffusion_time(20.0, 7.7))
             / float(cm.diffusion_time(1.0, 7.7)))
    assert ratio == pytest.approx(400.0, rel=1e-13)

    # The water-versus-cytoplasm factor of 11 IS the crowding, same slide.
    assert (float(cm.diffusion_time(1.0, 87.0))
            / float(cm.diffusion_time(1.0, 7.7))) == pytest.approx(
                7.7 / 87.0, rel=1e-13)


def test_session_2s_slide_still_says_the_convention_this_module_assumes():
    """Read the deck, do not assume it. The drift this guards is real.

    The numbers above are hard-coded, so if someone edits session 2's slide to
    the 3-D convention L^2/6D the hard-coded values would keep passing while
    the course acquired two conventions. These four fragments are the slide
    text that fixes it: the two worked answers, the "state the convention"
    habit, and the instruction to use L^2/2D.
    """
    src = S02.read_text(encoding="utf-8")
    assert "/2D = (1 " in src, "session 2's item 2 no longer shows L^2/2D"
    assert "65 ms" in src
    assert "26 s, so ~400" in src
    assert "/2D, and say so" in src
    assert "/2D or L" in src and "6D? Say which" in src, (
        "session 2's 'state the convention' habit has moved or changed")


@pytest.mark.parametrize("L", [0.5, 1.0, 7.0, 10.0])
@pytest.mark.parametrize("D", [1e-3, 7.7, 83.0, 1810.0])
def test_diffusion_time_is_quadratic_in_L_and_inverse_in_D(L, D):
    """t ~ L^2, not L -- session 2's "L squared, not L", asserted exactly."""
    t = float(cm.diffusion_time(L, D))
    assert t == pytest.approx(L * L / (2.0 * D), rel=1e-15)
    assert float(cm.diffusion_time(2.0 * L, D)) == pytest.approx(4.0 * t,
                                                                 rel=1e-13)
    assert float(cm.diffusion_time(L, 2.0 * D)) == pytest.approx(0.5 * t,
                                                                 rel=1e-13)
    assert t > 0.0


def test_basus_own_ring_takes_833_hours_on_basus_own_xi():
    """T66's cautionary slide, as arithmetic. NUMBERS.md sec 13.3.

    Basu print xi = 0.001 mm^2/min for AHL. Put it through the course's own
    convention at their own measured ring radius of 10 mm and the signal
    arrives in 833 hours, against a 36-hour experiment. That is the reductio,
    and it is why `penetration_depth` has no default D.
    """
    t_min = float(cm.diffusion_time(10.0, cm.BASU_XI))     # mm, mm^2/min -> min
    assert t_min == pytest.approx(50000.0, rel=1e-13)
    assert t_min / 60.0 == pytest.approx(833.333, abs=1e-3)     # hours
    assert 20.0 < (t_min / 60.0) / 36.0 < 25.0       # against the experiment

    # NUMBERS.md sec 13.3 runs it the other way too: the coefficient needed to
    # put a front at 10 mm in 15 h is 0.0556 mm^2/min, about 56x xi.
    D_needed = 10.0 ** 2 / (2.0 * 15.0 * 60.0)
    assert D_needed == pytest.approx(0.0555556, rel=1e-5)
    assert D_needed / cm.BASU_XI == pytest.approx(55.6, rel=1e-3)
    assert float(cm.diffusion_time(10.0, D_needed)) == pytest.approx(
        900.0, rel=1e-12)                            # 900 min = 15 h, exactly


# ======================================================================
# T66, part two -- the penetration depth, and its units
# ======================================================================
def test_penetration_depth_units_are_right_in_two_unit_systems():
    """A worked value from first principles, in micrometres and in millimetres.

    Take D = 400 um^2/s and gamma = 0.01 /s. Then

        lambda = sqrt(D/gamma) = sqrt(400 um^2/s / 0.01 /s)
               = sqrt(40000 um^2) = 200 um

    exactly. The same physical situation in the session's own units:

        D     = 400 um^2/s = 4e-4 mm^2/s = 0.024 mm^2/min
        gamma = 0.01 /s    = 0.6 /min
        lambda = sqrt(0.024/0.6) = sqrt(0.04 mm^2) = 0.2 mm = 200 um

    Both are exact, so both are asserted to machine precision: a function that
    had length and time muddled would fail one of the two and not the other.
    """
    assert float(cm.penetration_depth(400.0, 0.01)) == pytest.approx(
        200.0, rel=1e-15)                                        # um
    assert float(cm.penetration_depth(0.024, 0.6)) == pytest.approx(
        0.2, rel=1e-14)                                          # mm
    # and the two agree once converted, which is the units claim itself
    assert float(cm.penetration_depth(0.024, 0.6)) * 1e3 == pytest.approx(
        float(cm.penetration_depth(400.0, 0.01)), rel=1e-13)
    # scaling, exactly: four times the D is twice the depth
    assert float(cm.penetration_depth(1600.0, 0.01)) == pytest.approx(
        400.0, rel=1e-14)
    assert float(cm.penetration_depth(400.0, 0.04)) == pytest.approx(
        100.0, rel=1e-14)


def test_penetration_depth_refuses_to_supply_a_diffusion_coefficient():
    """D is required. The session's T66 lesson is that nobody may default it.

    There is no sourced D in this folder that may legitimately be put with
    Basu's gamma_A: xi is D/dx^2 with dx never stated, and Karig's 83 um^2/s is
    3OC12HSL measured through a different lawn -- neither of Basu's signals.
    """
    sig = inspect.signature(cm.penetration_depth)
    assert list(sig.parameters) == ["D", "gamma"]
    for name in ("D", "gamma"):
        assert sig.parameters[name].default is inspect.Parameter.empty, (
            f"{name} acquired a default, and a defaulted diffusion "
            f"coefficient is the error this signature exists to prevent")
    with pytest.raises(TypeError):
        cm.penetration_depth(0.001)          # no gamma, no answer


def test_the_basu_penetration_depth_is_a_reductio_and_not_a_design_number():
    """NUMBERS.md sec 13.4, run as what it is: an argument against xi.

    Combining Basu's gamma_A with Basu's xi gives 0.32 mm, and their band sits
    at 7 mm. That is 22 e-foldings and a concentration ratio of about 4e9
    between the sender edge and the band, which no synthesis rate makes into a
    usable design. The number is pinned here so that it cannot be quoted as a
    penetration depth by accident -- it inherits every defect of xi.
    """
    lam = float(cm.penetration_depth(cm.BASU_XI, 0.01))          # mm
    assert lam == pytest.approx(0.316228, rel=1e-5)
    assert 0.31 < lam < 0.33
    e_foldings = 7.0 / lam
    assert 22.0 < e_foldings < 22.3
    assert 2e9 < float(np.exp(e_foldings)) < 1e10

    # Karig's sourced coefficient gives 0.71 mm with the same gamma_A -- and is
    # the wrong molecule in the wrong medium, which is why that number is not
    # anywhere in the module either. 83 um^2/s = 0.00498 mm^2/min.
    D_karig_mm2_min = cm.KARIG_D_3OC12HSL * 60.0 * 1e-6
    assert D_karig_mm2_min == pytest.approx(0.00498, rel=1e-3)
    assert float(cm.penetration_depth(D_karig_mm2_min, 0.01)) == \
        pytest.approx(0.7057, rel=1e-3)
    # the two candidates differ by more than a factor of two, so the choice of
    # D is not a rounding question
    assert float(cm.penetration_depth(D_karig_mm2_min, 0.01)) / lam > 2.0


def test_karig_coefficients_and_their_ratio():
    """NUMBERS.md sec 19.1. The SI originals are in cm^2/hr and must agree.

    0.003 cm^2/hr and 0.065 cm^2/hr, converted, are 83.3 and 1806 um^2/s. The
    measured ratio they report is 21.6 +/- 10 where free solution predicts
    about 1.5, so the ratio is a property of cells and not of the molecules.
    """
    per = 1e8 / 3600.0                       # cm^2/hr -> um^2/s
    assert 0.003 * per == pytest.approx(83.3, rel=1e-3)
    assert 0.065 * per == pytest.approx(1806.0, rel=1e-3)
    ratio = cm.KARIG_D_C4HSL / cm.KARIG_D_3OC12HSL
    assert 21.0 < ratio < 22.3               # their 21.6, two-sided
    assert ratio / 1.5 > 10.0                # against the Wilke-Chang 1.5


# ======================================================================
# T65 -- the band detector, in the liquid-phase limit
# ======================================================================
# Basu's own dose-response axis, Fig. 2, runs 1e-4 to 1e1 uM (NUMBERS.md sec 8
# locates its printed decade labels). Every sweep below uses that window,
# because outside it the response is flat to within 1.5e-7 of its asymptote
# and a sweep there measures floating-point rounding rather than the circuit.
PAPER_AXIS = (-4.0, 1.0)


def _closed_form_limits(p):
    """G at zero AHL and at saturating AHL, written out a second way.

    An independent computation of the two tails: at A = 0 the activation is
    zero, so C = 0 and only the CI-repressible route makes LacI; at saturating
    A the activation is one, so C is at its maximum and that route is shut
    while the LuxR-AHL route runs flat out.
    """
    g_max = p["alpha_G"] / p["gamma_G"]
    L_zero = p["alpha_L1"] / p["gamma_L"]
    C_sat = p["alpha_C"] / p["gamma_C"]
    L_sat = (p["alpha_L1"] / (1.0 + (C_sat / p["beta_C"]) ** p["eta2"])
             + p["alpha_L2"]) / p["gamma_L"]
    return (g_max / (1.0 + (L_zero / p["beta_L"]) ** p["eta1"]),
            g_max / (1.0 + (L_sat / p["beta_L"]) ** p["eta1"]))


@pytest.mark.parametrize("variant", ["BD1", "BD2", "BD3"])
def test_band_detect_tails_match_a_closed_form_written_out_again(variant):
    """Both tails, against the algebra done separately. No sweep, no solver."""
    p = cm.basu_params(variant)
    lo, hi = _closed_form_limits(p)
    assert float(cm.band_detect_response(0.0, p)) == pytest.approx(lo,
                                                                   rel=1e-13)
    assert float(cm.band_detect_response(1e-9, p)) == pytest.approx(lo,
                                                                    rel=1e-6)
    assert float(cm.band_detect_response(1e4, p)) == pytest.approx(hi,
                                                                   rel=1e-6)
    # THE TWO TAILS ARE DARK FOR TWO DIFFERENT REASONS, and how close they come
    # is set by alpha_L1 against alpha_L2. At zero AHL, LacI comes entirely from
    # the CI-repressible route at alpha_L1; at saturating AHL that route is shut
    # and LacI comes entirely from the LuxR-AHL route at alpha_L2. So the two
    # tail LacI levels are in the ratio alpha_L1/alpha_L2, and deep in
    # repression GFP goes as 1/L^eta1 -- which makes the tail brightness ratio
    # (alpha_L1/alpha_L2)^eta1. BD1 and BD2 have the two rates equal and their
    # tails coincide to five decimal places; BD3 halves alpha_L2 alone, so its
    # high tail is four times the brighter. A test that asserted the tails were
    # always equal would be asserting BD2's accident.
    assert lo != hi
    predicted = (p["alpha_L1"] / p["alpha_L2"]) ** p["eta1"]
    if p["alpha_L1"] == p["alpha_L2"]:
        assert predicted == 1.0
        assert abs(lo - hi) / lo < 1e-5
    else:
        assert predicted == pytest.approx(4.0, rel=1e-13)
        assert hi / lo == pytest.approx(predicted, rel=2e-3)
        assert 3.9 < hi / lo < 4.1


@pytest.mark.parametrize("variant", ["BD1", "BD2", "BD3"])
def test_band_detect_response_has_a_single_interior_maximum(variant):
    """A FINE sweep, not three sampled points. The response is non-monotone.

    200 001 points across Basu's own five decades, about 40 000 per decade.
    Exactly one strict interior maximum, and the sign of the first difference
    changes exactly once -- so the response rises, turns once, and falls, which
    is what "band" means. Counting maxima alone would not exclude a second
    turning point that happens to be a minimum.
    """
    lg = np.linspace(PAPER_AXIS[0], PAPER_AXIS[1], 200001)
    G = cm.band_detect_response(10.0 ** lg, cm.basu_params(variant))
    assert np.all(G > 0.0)
    interior = G[1:-1]
    maxima = int(np.sum((interior > G[:-2]) & (interior > G[2:])))
    minima = int(np.sum((interior < G[:-2]) & (interior < G[2:])))
    assert maxima == 1, f"{variant}: {maxima} interior maxima, expected 1"
    assert minima == 0, f"{variant}: {minima} interior minima, expected 0"
    sign = np.sign(np.diff(G))
    sign = sign[sign != 0.0]
    assert int(np.sum(sign[1:] != sign[:-1])) == 1
    # and the gain is large, so the band is a band and not a ripple
    assert G.max() / G.min() > 100.0


def test_a_coarse_grid_straddles_the_peak_and_reports_the_wrong_story():
    """The mistake this course has already shipped, demonstrated.

    One point per decade across the paper's axis puts no sample within a
    factor of 2.5 of the true peak: it reports a maximum nearly six times too
    low, and it reports it at the last sampled point before the fall, so the
    band reads as a response that is still rising. Both halves are asserted,
    two-sided, so that a future refactor cannot quietly make the coarse grid
    "good enough".
    """
    p = cm.basu_params("BD2")
    A_peak, G_peak = cm.band_peak(p)
    lo, hi = cm.band_edges(p)
    coarse_lg = np.arange(PAPER_AXIS[0], PAPER_AXIS[1] + 0.5, 1.0)
    coarse_A = 10.0 ** coarse_lg
    coarse = cm.band_detect_response(coarse_A, p)

    # NOT ONE SAMPLE LANDS IN THE BAND. The half-maximum band runs from
    # 2.6e-3 to 6.9e-3 uM and the two nearest samples are 1e-3 and 1e-2, so the
    # grid steps straight over the feature it is meant to measure.
    assert not np.any((coarse_A >= lo) & (coarse_A <= hi))
    # so the peak it reports is nearly six times too low
    assert 5.0 < G_peak / coarse.max() < 7.0
    # and it is reported at an AHL two and a half times too high
    i = int(np.argmax(coarse))
    assert 2.0 < coarse_A[i] / A_peak < 3.0
    # the fine locator lands inside the band it is describing, by construction
    assert lo < A_peak < hi


@pytest.mark.parametrize("variant", ["BD1", "BD2", "BD3"])
@pytest.mark.parametrize("frac", [0.1, 0.25, 0.5, 0.75, 0.9])
def test_band_edges_round_trip_against_the_response(variant, frac):
    """The edges are where the response is `frac` of its peak. Both of them.

    This is the round trip the design asks for: solve for the edge, evaluate
    the response there, and get the fraction back. The tolerance is on the
    RESPONSE and not on the AHL, because near the peak the response is flat and
    a loose edge still reproduces the level -- which is exactly the direction
    an edge solver fails in.
    """
    p = cm.basu_params(variant)
    A_peak, G_peak = cm.band_peak(p)
    lo, hi = cm.band_edges(p, frac=frac)
    assert 0.0 < lo < A_peak < hi
    for A in (lo, hi):
        got = float(cm.band_detect_response(A, p)) / G_peak
        assert got == pytest.approx(frac, rel=1e-10), (variant, frac, A, got)


@pytest.mark.parametrize("variant", ["BD1", "BD2", "BD3"])
def test_a_higher_fraction_gives_a_narrower_band(variant):
    """Monotone by construction, and bounded on both sides at each step."""
    p = cm.basu_params(variant)
    widths = [cm.band_edges(p, frac=f)[1] / cm.band_edges(p, frac=f)[0]
              for f in (0.1, 0.25, 0.5, 0.75, 0.9)]
    for a, b in zip(widths, widths[1:]):
        assert 1.0 < b < a
    assert widths[-1] > 1.0, "a band of zero width is not a band"


def test_bd2_half_maximum_band_is_pinned():
    """NUMBERS.md sec 7.2's printed set, in the liquid-phase limit.

    These are headed for a figure and for a PS9 reference value, so they are
    pinned two-sided rather than bounded. The band is narrow -- a factor of
    2.65 between the half-maximum edges -- and that is a property of the
    printed parameters in the liquid-phase limit, not of the measured strains.
    """
    p = cm.basu_params("BD2")
    A_peak, G_peak = cm.band_peak(p)
    assert A_peak == pytest.approx(3.9733e-3, rel=1e-4)      # uM
    assert G_peak == pytest.approx(19.60697, rel=1e-5)       # uM GFP
    lo, hi = cm.band_edges(p)
    assert lo == pytest.approx(2.61316e-3, rel=1e-5)
    assert hi == pytest.approx(6.92806e-3, rel=1e-5)
    assert hi / lo == pytest.approx(2.65122, rel=1e-5)
    # beta_C/beta_L = 1/100 in this set, which is BD2's value and not a
    # requirement: Basu's own Figs. 4b and 4c band at 28.6 and 3.3.
    assert p["beta_C"] / p["beta_L"] == pytest.approx(0.01, rel=1e-13)


def test_bd1_is_exactly_bd2_shifted_down_by_root_ten():
    """An exact analytic check, and the cleanest one in this file.

    BD1 differs from BD2 in rho_R alone, tenfold (Basu p.1134). AHL enters the
    whole cascade only through R = rho_R [LuxR]^2 A^2 / gamma_R, so a tenfold
    rho_R is a rescaling of A by 1/sqrt(10) and NOTHING ELSE: every edge, the
    peak position and the band width move by exactly that factor, and the peak
    HEIGHT does not move at all. If the implementation ever stopped composing
    the cascade in one direction, this is the test that would notice.
    """
    root10 = float(np.sqrt(10.0))
    b1, b2 = cm.basu_params("BD1"), cm.basu_params("BD2")
    for f in (0.1, 0.5, 0.9):
        lo1, hi1 = cm.band_edges(b1, frac=f)
        lo2, hi2 = cm.band_edges(b2, frac=f)
        assert lo2 / lo1 == pytest.approx(root10, rel=1e-10)
        assert hi2 / hi1 == pytest.approx(root10, rel=1e-10)
    p1, g1 = cm.band_peak(b1)
    p2, g2 = cm.band_peak(b2)
    assert p2 / p1 == pytest.approx(root10, rel=1e-8)
    assert g2 / g1 == pytest.approx(1.0, rel=1e-10)      # the height is unmoved
    # alpha_G halving in BD3 cannot move an edge defined as a fraction of the
    # peak either, for the same reason: it scales the output and nothing else.
    scaled = dict(b2)
    scaled["alpha_G"] = 0.5 * b2["alpha_G"]
    half_lo, half_hi = cm.band_edges(b2)
    assert cm.band_edges(scaled)[0] == pytest.approx(half_lo, rel=1e-12)
    assert cm.band_edges(scaled)[1] == pytest.approx(half_hi, rel=1e-12)
    assert cm.band_peak(scaled)[1] == pytest.approx(0.5 * g2, rel=1e-12)


def test_the_three_variants_band_at_three_different_positions_in_this_order():
    """BD1 low, BD2 middle, BD3 high. The ordering is what the ConcepTest turns on.

    BD1 raises rho_R tenfold -- the hypersensitive LuxR-G2F mutant -- so it
    detects a LOWER AHL. BD3 halves [LuxR], and R goes as [LuxR]^2, so it needs
    a HIGHER AHL. The gaps are bounded on both sides: the BD1-to-BD2 step is
    exactly sqrt(10) because nothing but rho_R moves, while the BD3 step is
    NOT a pure rescaling -- halving alpha_L2 changes the shape, which is why
    its low and high edges move by different factors and its band is wider.
    """
    lo1, hi1 = cm.band_edges(cm.basu_params("BD1"))
    lo2, hi2 = cm.band_edges(cm.basu_params("BD2"))
    lo3, hi3 = cm.band_edges(cm.basu_params("BD3"))
    assert lo1 < lo2 < lo3
    assert hi1 < hi2 < hi3
    assert cm.band_peak(cm.basu_params("BD1"))[0] \
        < cm.band_peak(cm.basu_params("BD2"))[0] \
        < cm.band_peak(cm.basu_params("BD3"))[0]
    # three separated bands, not three overlapping ones
    assert hi1 < lo3, "BD1 and BD3 bands overlap; the ordering is not visible"
    assert lo2 / lo1 == pytest.approx(3.16228, rel=1e-5)
    assert hi2 / hi1 == pytest.approx(3.16228, rel=1e-5)
    assert lo3 / lo2 == pytest.approx(2.05924, rel=1e-5)
    assert hi3 / hi2 == pytest.approx(2.63166, rel=1e-5)
    assert lo3 / lo2 != pytest.approx(hi3 / hi2, rel=1e-3), \
        "BD3 is not a pure rescaling and the test must not imply it is"
    assert (hi3 / lo3) / (hi2 / lo2) == pytest.approx(1.27798, rel=1e-4)


def test_band_edges_guards():
    with pytest.raises(ValueError, match="strictly in"):
        cm.band_edges(cm.basu_params("BD2"), frac=0.0)
    with pytest.raises(ValueError, match="strictly in"):
        cm.band_edges(cm.basu_params("BD2"), frac=1.0)
    with pytest.raises(ValueError, match="cannot be negative"):
        cm.band_detect_response(-1.0, cm.basu_params("BD2"))
    with pytest.raises(ValueError, match="missing"):
        cm.band_detect_response(1.0, {"alpha_G": 2.0})
    with pytest.raises(ValueError, match="variant must be"):
        cm.basu_params("HD1")
    # mutating the returned dict must not reach the module constant
    p = cm.basu_params("BD2")
    p["beta_L"] = 99.0
    assert cm.BASU_BD2["beta_L"] == 0.8


def test_a_monotone_circuit_has_no_band_and_says_so():
    """Attack band_edges with parameters that do not give a band.

    Remove the CI-repressible route (alpha_L1 = 0) and LacI is produced only by
    the LuxR-AHL-activated arm, so GFP falls monotonically with AHL: the
    circuit is a plain inverter and there is no interior peak to find. The
    error names the window rather than returning an endpoint.
    """
    p = cm.basu_params("BD2")
    p["alpha_L1"] = 0.0
    lg = np.linspace(PAPER_AXIS[0], PAPER_AXIS[1], 20001)
    G = cm.band_detect_response(10.0 ** lg, p)
    # non-increasing to within floating point: the low-AHL tail is flat at
    # alpha_G/gamma_G to machine precision, so an exact <= 0 would be a test of
    # rounding rather than of the circuit.
    assert np.all(np.diff(G) <= 1e-12 * G.max()), \
        "this control is supposed to be monotone in AHL"
    assert G[0] / G[-1] > 100.0
    with pytest.raises(ValueError, match="edge of the search window"):
        cm.band_edges(p)


# ======================================================================
# T64 -- the minimal sender/receiver pair
# ======================================================================
def test_sender_receiver_requires_k_I_and_has_no_default_for_it():
    """Neither paper prints a sender synthesis rate, so the caller supplies one.

    Basu's model is receiver-only and their Methods tune the senders to put a
    ring at 7 mm without printing the value; Balagadde's equations are in a
    supplement this repository does not hold. The signature is the place that
    fact is enforced.
    """
    sig = inspect.signature(cm.sender_receiver)
    for name in ("A", "S", "k_I", "gamma_A"):
        assert sig.parameters[name].default is inspect.Parameter.empty, name
    assert sig.parameters["D"].default == 0.0          # a plate, not a reactor
    with pytest.raises(TypeError):
        cm.sender_receiver(1.0, 1.0)                   # no k_I, no answer


@pytest.mark.parametrize("k_I", [0.01, 1.0, 37.0])
@pytest.mark.parametrize("S", [0.1, 1.0, 1e3])
@pytest.mark.parametrize("gamma_A,D", [(0.01, 0.0), (0.01, 0.1), (0.0231, 0.5)])
def test_sender_steady_state_is_the_ratio_and_the_derivative_vanishes_there(
        k_I, S, gamma_A, D):
    """A* = k_I S / (gamma_A + D), computed here and fed back in.

    The independent computation is the closed form written out in the test, and
    the check is that the model's own derivative is zero at it. Exactly zero is
    the right answer and the bound admits it -- the residual is compared to the
    scale of the two terms it is a difference of, so a bound that excluded zero
    would be failing the correct result.
    """
    A_star = k_I * S / (gamma_A + D)
    dA, out = cm.sender_receiver(A_star, S, k_I, gamma_A, D)
    scale = k_I * S
    assert 0.0 <= abs(float(dA)) <= 1e-12 * scale
    # above it the signal falls, below it the signal rises -- two-sided
    assert float(cm.sender_receiver(1.5 * A_star, S, k_I, gamma_A, D)[0]) < 0.0
    assert float(cm.sender_receiver(0.5 * A_star, S, k_I, gamma_A, D)[0]) > 0.0
    assert 0.0 <= float(out) <= 1.0


def test_dilution_competes_with_decay_in_the_reactor():
    """The (- D A) term, and what it is worth.

    On a plate D = 0 and the signal is set by k_I S / gamma_A. In a reactor run
    at Balagadde's own 0.11 h^-1 against an AHL decay of 0.01 min^-1 = 0.6
    h^-1, dilution removes a sixth as much signal as decay does, so the steady
    state falls by that fraction and no more. The arithmetic is here rather
    than on a slide alone because it is the one place the two halves of the
    session's units meet.
    """
    gamma_A_per_h = 0.01 * 60.0                      # 0.01 /min = 0.6 /h
    plate = cm.sender_receiver(0.0, 1.0, 1.0, gamma_A_per_h)[0] / gamma_A_per_h
    reactor = (cm.sender_receiver(0.0, 1.0, 1.0, gamma_A_per_h, 0.11)[0]
               / (gamma_A_per_h + 0.11))
    assert float(plate) == pytest.approx(1.0 / 0.6, rel=1e-13)
    assert float(reactor) / float(plate) == pytest.approx(0.6 / 0.71, rel=1e-13)
    assert 0.84 < float(reactor) / float(plate) < 0.85


@pytest.mark.parametrize("n", [1.0, 2.0, 4.0])
def test_receiver_hill_is_half_maximal_at_theta_and_bounded(n):
    """Hill(theta) = alpha/2 exactly, for every n. And the bounds are tight."""
    _, out = cm.sender_receiver(2.0, 1.0, 1.0, 0.01, 0.0,
                                alpha=3.0, theta=2.0, n=n)
    assert float(out) == pytest.approx(1.5, rel=1e-14)
    _, lo = cm.sender_receiver(0.0, 1.0, 1.0, 0.01, 0.0,
                               alpha=3.0, theta=2.0, n=n)
    assert float(lo) == 0.0
    _, hi = cm.sender_receiver(1e6, 1.0, 1.0, 0.01, 0.0,
                               alpha=3.0, theta=2.0, n=n)
    # alpha is the ceiling, and a Hill function reaches it in floating point:
    # at n = 4 and A = 1e6 the answer is EXACTLY 3.0, so the upper bound has to
    # admit it. `< 3.0` here failed the correct answer.
    assert 2.99 < float(hi) <= 3.0


def test_sender_receiver_guards():
    with pytest.raises(ValueError, match="cannot be negative"):
        cm.sender_receiver(-1.0, 1.0, 1.0, 0.01)
    with pytest.raises(ValueError, match="S is a density"):
        cm.sender_receiver(1.0, -1.0, 1.0, 0.01)
    with pytest.raises(ValueError, match="k_I is a synthesis rate"):
        cm.sender_receiver(1.0, 1.0, -1.0, 0.01)
    with pytest.raises(ValueError, match="gamma_A \\+ D must be"):
        cm.sender_receiver(1.0, 1.0, 1.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="theta must be"):
        cm.sender_receiver(1.0, 1.0, 1.0, 0.01, theta=0.0)


# ======================================================================
# MOVE 4 -- the deposited four-state model, the QSSA, and the Hopf
# ======================================================================
# Specification: NUMBERS.md sec 20, transcribed from the BioModels deposit
# BIOMD0000000296 through the JWS Online curation. The paper's own text prints
# no equations, so nothing in this section is a test of the paper.
#
# STILL NOT TESTED, deliberately: the WIDTH of the oscillatory region in D
# against the repository's digitization of Balagadde's Fig. 3C. The two
# crossings below are pinned as what the deposited parameters give, which is a
# regression test on this module; comparing them to a one-significant-figure
# reading off a rendered page would be a different and much weaker claim.


@pytest.fixture(scope="module")
def hopf_Ds():
    """Both crossings, computed once -- the scan is the slowest thing here."""
    return cm.pp_hopf_D(cm.PP_PARAMS, which="all")


def test_the_iptg_assignment_rules_are_exact_at_the_deposits_own_iptg():
    """kA2 = 0.035 and d1 = 1.0 at IPTG = 5, exactly. NUMBERS.md sec 20.2.

        kA2 = 0.02 + 0.03 * IPTG^2/(5^2 + IPTG^2)
        d1  = 0.5  +        IPTG^2/(5^2 + IPTG^2)

    At IPTG = 5 both Hill terms are exactly one half, so both values are exact
    rationals and are asserted to machine precision rather than bounded.
    """
    kA2, d1 = cm.iptg_assignment_rules(5.0)
    assert float(kA2) == pytest.approx(0.035, rel=1e-15)
    assert float(d1) == pytest.approx(1.0, rel=1e-15)
    assert float(kA2) == pytest.approx(0.02 + 0.03 * 0.5, rel=1e-15)
    assert float(d1) == pytest.approx(0.5 + 0.5, rel=1e-15)
    # the uninduced end, also exact
    kA2_0, d1_0 = cm.iptg_assignment_rules(0.0)
    assert float(kA2_0) == 0.02 and float(d1_0) == 0.5
    # and the saturating end, which both rules approach but never reach
    kA2_inf, d1_inf = cm.iptg_assignment_rules(1e9)
    assert 0.0499 < float(kA2_inf) <= 0.05
    assert 1.4999 < float(d1_inf) <= 1.5
    # monotone in between, two-sided at each step
    iptg = np.linspace(0.0, 50.0, 201)
    a, b = cm.iptg_assignment_rules(iptg)
    assert np.all(np.diff(a) > 0.0) and np.all(np.diff(b) > 0.0)
    assert np.all((a >= 0.02) & (a <= 0.05))
    assert np.all((b >= 0.5) & (b <= 1.5))
    with pytest.raises(ValueError, match="cannot be negative"):
        cm.iptg_assignment_rules(-1.0)


def test_iptg_enters_the_model_nowhere_else():
    """Sec 20.2's claim, as a test of the parameter builder.

    IPTG tunes the prey's signal synthesis and the predator's death rate and
    nothing else, which is why the paper's route across the Hopf is IPTG. If
    some later edit let IPTG touch a third parameter, the slide saying "one
    chemical, two parameters" would be wrong and this is what would catch it.
    """
    base = cm.pp_params(5.0)
    assert set(base) == set(cm.PP_PARAMS)
    assert base == pytest.approx(dict(cm.PP_PARAMS))
    for iptg in (0.0, 1.0, 2.5, 10.0):
        p = cm.pp_params(iptg)
        moved = {k for k in p if p[k] != cm.PP_PARAMS[k]}
        assert moved <= {"kA2", "d1"}, moved
        kA2, d1 = cm.iptg_assignment_rules(iptg)
        assert p["kA2"] == pytest.approx(float(kA2), rel=1e-15)
        assert p["d1"] == pytest.approx(float(d1), rel=1e-15)
    # a fresh dict every time, so a sweep cannot poison the constant
    cm.pp_params()["Cm"] = 1.0
    assert cm.PP_PARAMS["Cm"] == 100.0
    with pytest.raises(ValueError, match="not a parameter"):
        cm.pp_params(5.0, C_q=3000.0)


@pytest.mark.parametrize("D", [0.005, 0.02, 0.05, 0.1125, 0.15, 0.167, 0.2])
def test_every_returned_fixed_point_is_fixed_in_both_models(D):
    """The definition, checked -- and checked for the reduction too.

    Substituting the quasi-steady-state signals is EXACT at a fixed point, so
    every state here must kill both right-hand sides. Washout gives identically
    zero and the bound admits it: an earlier test in this repository required a
    strictly positive difference where the exact answer was 0.0 and failed the
    correct result.
    """
    q = cm.pp_params(D=D)
    assert float(np.max(np.abs(
        cm.predator_prey_model([0.0, 0.0, 0.0, 0.0], q)))) == 0.0
    for name, arr in cm.pp_steady_states(q).items():
        for s in arr:
            r4 = float(np.max(np.abs(cm.predator_prey_model(s, q))))
            r2 = float(np.max(np.abs(cm.pp_qss_model(s[:2], q))))
            assert 0.0 <= r4 <= 1e-8, (name, D, s, r4)
            assert 0.0 <= r2 <= 1e-8, (name, D, s, r2)


@pytest.mark.parametrize("D", [0.005, 0.05, 0.1125, 0.15])
def test_the_fixed_points_carry_their_own_quasi_steady_state_signals(D):
    """A1 = kA1 C1/(dAA1+D) and A2 = kA2 C2/(dAA2+D) at every fixed point.

    This is why one `pp_steady_states` serves both models, and it is worth
    asserting rather than assuming: it is the exactness that lets the session
    put the same phase portrait under the four-state system and its reduction.
    """
    q = cm.pp_params(D=D)
    for arr in cm.pp_steady_states(q).values():
        for s in arr:
            a1, a2 = cm.pp_qss_signals(s, q)
            assert float(a1) == pytest.approx(s[2], rel=1e-12, abs=1e-15)
            assert float(a2) == pytest.approx(s[3], rel=1e-12, abs=1e-15)
            assert float(a1) == pytest.approx(
                q["kA1"] * s[0] / (q["dAA1"] + D), rel=1e-14, abs=1e-15)
            assert float(a2) == pytest.approx(
                q["kA2"] * s[1] / (q["dAA2"] + D), rel=1e-14, abs=1e-15)


def test_the_two_boundary_states_are_the_closed_forms_they_should_be():
    """At one population zero the other reduces to a logistic, exactly.

    At C1 = 0 the predator's signal is absent, so A1 = 0 and the prey's death
    term is exactly D: C2 = Cm(1 - D/kc2). At C2 = 0 the prey's signal is
    absent, so K1/(K1 + 0) = 1 and the predator carries its FULL death rate:
    C1 = Cm(1 - (D + d1)/kc1).
    """
    q = cm.pp_params(D=0.2)
    prey = cm.pp_steady_states(q)["prey_only"]
    assert prey.shape == (1, 4)
    assert prey[0, 0] == 0.0 and prey[0, 2] == 0.0
    assert prey[0, 1] == pytest.approx(q["Cm"] * (1.0 - q["D"] / q["kc2"]),
                                       rel=1e-15)
    assert prey[0, 1] == pytest.approx(50.0, rel=1e-13)
    assert prey[0, 3] == pytest.approx(
        q["kA2"] * prey[0, 1] / (q["dAA2"] + q["D"]), rel=1e-14)
    # above kc2 even the prey washes out, and the state disappears rather than
    # coming back negative
    assert cm.pp_steady_states(cm.pp_params(D=0.45))["prey_only"].shape == (0, 4)


def test_the_predator_needs_the_preys_signal_and_iptg_decides_at_2_402():
    """d1 > kc1 at IPTG = 5, so there is no predator-only state at any D.

    CcdB is constitutive in the predator and the prey's signal induces the
    antidote, so with the death rate above the growth rate raising D cannot
    help -- D removes cells, not toxin. Drop IPTG and d1 falls: the state
    exists exactly when d1 + D < kc1, i.e. when

        0.5 + IPTG^2/(25 + IPTG^2) < kc1 - D = 0.6875   at D = 0.1125

    which solves to IPTG^2 < 25 * 0.1875/0.8125, IPTG < 2.4019. Both sides of
    that threshold are checked, and the closed form is checked where the state
    exists.
    """
    assert cm.PP_PARAMS["d1"] > cm.PP_PARAMS["kc1"]
    for D in (0.0, 0.1125, 0.3, 0.39):
        q = cm.pp_params(D=D)
        assert cm.pp_steady_states(q)["predator_only"].shape == (0, 4)

    threshold = float(np.sqrt(25.0 * 0.1875 / 0.8125))
    assert threshold == pytest.approx(2.40192, rel=1e-5)
    assert cm.pp_steady_states(
        cm.pp_params(threshold * 0.99))["predator_only"].shape == (1, 4)
    assert cm.pp_steady_states(
        cm.pp_params(threshold * 1.01))["predator_only"].shape == (0, 4)

    q = cm.pp_params(0.0)                      # uninduced: d1 = 0.5
    pred = cm.pp_steady_states(q)["predator_only"]
    assert pred.shape == (1, 4)
    assert pred[0, 1] == 0.0 and pred[0, 3] == 0.0
    assert pred[0, 0] == pytest.approx(
        q["Cm"] * (1.0 - (q["d1"] + q["D"]) / q["kc1"]), rel=1e-15)
    assert pred[0, 0] == pytest.approx(23.4375, rel=1e-12)
    assert pred[0, 2] == pytest.approx(
        q["kA1"] * pred[0, 0] / (q["dAA1"] + q["D"]), rel=1e-14)


def _central_difference_jacobian(state, params, h=1e-6):
    """An independent computation of the Jacobian. No solver, no quadrature."""
    x = np.asarray(state, float)
    n = x.shape[0]
    rhs = cm.predator_prey_model if n == 4 else cm.pp_qss_model
    J = np.zeros((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = h * max(1.0, abs(x[j]))
        J[:, j] = (rhs(x + e, params) - rhs(x - e, params)) / (2.0 * e[j])
    return J


@pytest.mark.parametrize("D", [0.01, 0.05, 0.1125, 0.15, 0.167])
def test_pp_jacobian_matches_a_central_difference_in_both_shapes(D):
    """The hand-differentiated matrices against finite differences of the models.

    Both the 4x4 and the 2x2, at every interior fixed point and at two interior
    points that are not fixed points -- because a Jacobian that is only ever
    checked where the right-hand side vanishes is checked on a measure-zero
    set. The bound is two-sided, so an error of exactly zero would mean the
    difference quotient had stopped being computed.
    """
    q = cm.pp_params(D=D)
    pts = [s for s in cm.pp_steady_states(q)["coexistence"]]
    pts += [np.array([5.0, 20.0, 4.0, 3.0]), np.array([12.0, 9.0, 9.0, 2.0])]
    assert pts
    for s in pts:
        for state in (s, s[:2]):
            exact = cm.pp_jacobian(state, q)
            approx = _central_difference_jacobian(state, q)
            assert exact.shape == (len(state), len(state))
            scale = float(np.max(np.abs(exact)))
            rel = float(np.max(np.abs(exact - approx))) / scale
            assert 0.0 <= rel < 1e-7, (D, state, rel)


def test_the_jacobians_structural_zeros_say_the_wire_is_outside_the_cell():
    """Neither population responds to its OWN signal. That is the circuit.

    In the 4x4, row 0 column 2 and row 1 column 3 are EXACTLY zero: the
    predator's growth does not see the predator's own 3OC12HSL and the prey's
    does not see its own 3OC6HSL. Every interaction goes through the two
    signal rows, which are linear and whose only entries are the synthesis
    rates and the removal rates. Exact zeros are the correct answer here and
    are asserted as zeros, not as small numbers.
    """
    q = cm.PP_PARAMS
    s = cm.pp_oscillatory_focus(q)
    J = cm.pp_jacobian(s, q)
    assert J[0, 2] == 0.0, "the predator responds to its own signal"
    assert J[1, 3] == 0.0, "the prey responds to its own signal"
    assert J[2, 1] == 0.0 and J[2, 3] == 0.0
    assert J[3, 0] == 0.0 and J[3, 2] == 0.0
    assert J[2, 0] == pytest.approx(q["kA1"], rel=1e-15)
    assert J[3, 1] == pytest.approx(q["kA2"], rel=1e-15)
    assert J[2, 2] == pytest.approx(-(q["dAA1"] + q["D"]), rel=1e-15)
    assert J[3, 3] == pytest.approx(-(q["dAA2"] + q["D"]), rel=1e-15)
    # and the cross couplings have the signs the circuit demands: the prey's
    # signal RESCUES the predator (positive), the predator's KILLS the prey
    # (negative)
    assert J[0, 3] > 0.0
    assert J[1, 2] < 0.0


@pytest.mark.parametrize("D", [0.005, 0.01, 0.02, 0.05, 0.1125, 0.15, 0.167])
def test_the_qss_trace_is_exactly_minus_the_weighted_density(D):
    """NUMBERS.md sec 20.3, and it is the reason move 4 exists.

    In the two-state reduction, both per-capita rates vanish at an interior
    fixed point, so on each diagonal the growth term cancels the death term and
    only the logistic self-limitation survives:

        tr J = -(kc1 C1 + kc2 C2) / Cm

    exactly. The cross terms never enter the trace -- they are off the
    diagonal. Agreement when written: better than 1e-12 relative.
    """
    q = cm.pp_params(D=D)
    arr = cm.pp_steady_states(q)["coexistence"]
    assert arr.shape[0] >= 1, "no interior point to test the identity at"
    for s in arr:
        tr = float(np.trace(cm.pp_jacobian(s[:2], q)))
        want = -(q["kc1"] * s[0] + q["kc2"] * s[1]) / q["Cm"]
        assert tr == pytest.approx(want, rel=1e-12), (D, s, tr, want)
        assert tr < 0.0


def test_the_qss_trace_is_negative_across_a_wide_parameter_sweep():
    """The claim is "at any parameter values", so it is swept, not spot-checked.

    Every parameter of the deposited model is varied over a wide range at once
    and every interior fixed point found is tested. This is the executable form
    of the sentence the session says out loud, and it is what makes the QSSA
    move a result rather than an assertion: the trace identity holds, and the
    trace is negative, at every one of them.
    """
    rng = np.random.default_rng(24)
    checked = 0
    worst = 0.0
    for _ in range(400):
        q = cm.pp_params(
            iptg=float(rng.uniform(0.0, 30.0)),
            kc1=float(rng.uniform(0.1, 2.0)), kc2=float(rng.uniform(0.1, 2.0)),
            Cm=float(10.0 ** rng.uniform(1.0, 3.5)),
            d2=float(rng.uniform(0.05, 1.5)),
            K1=float(10.0 ** rng.uniform(-1.0, 2.0)),
            K2=float(10.0 ** rng.uniform(-1.0, 2.0)),
            kA1=float(10.0 ** rng.uniform(-2.0, 0.0)),
            dAA1=float(10.0 ** rng.uniform(-3.0, -0.5)),
            dAA2=float(10.0 ** rng.uniform(-3.0, -0.5)),
            D=float(rng.uniform(0.001, 0.5)))
        for s in cm.pp_steady_states(q, grid=1001)["coexistence"]:
            tr = float(np.trace(cm.pp_jacobian(s[:2], q)))
            want = -(q["kc1"] * s[0] + q["kc2"] * s[1]) / q["Cm"]
            assert tr < 0.0, (q, s, tr)
            worst = max(worst, abs(tr - want) / abs(want))
            checked += 1
    assert checked > 150, f"only {checked} interior points found; sweep too thin"
    assert 0.0 <= worst < 1e-9, worst


def test_the_qss_reduction_has_no_hopf_anywhere_and_the_error_says_why():
    """The negative result, raised rather than silently searched for.

    And checked directly as well: across the same dilution range on which the
    four-state system crosses twice, the reduction's leading real part never
    changes sign. It is the same fixed point and the same circuit; only the
    signal lag has been removed.
    """
    with pytest.raises(ValueError, match="no stability crossing"):
        cm.pp_hopf_D(cm.PP_PARAMS, model="qss")
    leads = []
    for D in np.linspace(0.005, 0.19, 60):
        q = cm.pp_params(D=D)
        v = cm.pp_leading_real_part(q, model="qss")
        if np.isfinite(v):
            leads.append(v)
    assert len(leads) > 40
    assert max(leads) < 0.0, "the reduction is stable wherever it coexists"
    assert min(leads) > -10.0                 # bounded, not a blow-up


def test_the_four_state_system_has_two_hopf_crossings_bracketed_two_sided(
        hopf_Ds):
    """Move 4's result: the signal dynamics put the crossing back.

    Two crossings, which bound the oscillatory region in D rather than marking
    one edge. At each, the leading real part is zero to machine precision with
    a nonzero imaginary part -- a complex pair on the axis, which is what makes
    it a Hopf and not a saddle-node -- and the leading real part has the
    OPPOSITE sign on each side. Both signs are asserted at four step sizes,
    because "the real part is small here" is true of many points that are not
    bifurcations.
    """
    assert hopf_Ds.shape == (2,)
    lo, hi = float(hopf_Ds[0]), float(hopf_Ds[1])
    assert lo == pytest.approx(0.0367268, rel=1e-5)
    assert hi == pytest.approx(0.1674282, rel=1e-5)
    assert 0.03 < lo < 0.04 and 0.16 < hi < 0.18
    assert cm.pp_hopf_D(cm.PP_PARAMS) == pytest.approx(lo, rel=1e-12)
    assert cm.pp_hopf_D(cm.PP_PARAMS, which="last") == pytest.approx(hi,
                                                                     rel=1e-12)

    # The step sets differ because the two crossings have different room.
    # Below the first there is plenty; above the second there is about 0.009,
    # because coexistence itself is lost near D = 0.1764 -- so a step of 0.012
    # there lands where there is no fixed point to linearize about, which is
    # a different statement from "stable" and must not be read as one.
    for D_c, inside, steps in ((lo, +1, (0.002, 0.005, 0.010, 0.020)),
                               (hi, -1, (0.001, 0.002, 0.004, 0.007))):
        q = cm.pp_params(D=D_c)
        st = cm.pp_oscillatory_focus(q)
        assert st is not None
        ev = np.linalg.eigvals(cm.pp_jacobian(st, q))
        lead = ev[int(np.argmax(ev.real))]
        assert abs(lead.real) < 1e-10, lead      # exactly zero is correct
        assert abs(lead.imag) > 0.05, lead       # and it is a complex pair
        period = 2.0 * np.pi / abs(lead.imag)
        assert 50.0 < period < 90.0              # hours, bounded both ways
        for step in steps:
            below = cm.pp_leading_real_part(cm.pp_params(D=D_c - step))
            above = cm.pp_leading_real_part(cm.pp_params(D=D_c + step))
            assert np.isfinite(below) and np.isfinite(above), (D_c, step)
            assert np.sign(above - below) == inside, (D_c, step, below, above)
            assert inside * below < 0.0 < inside * above
    # and coexistence really does end just above the upper crossing, which is
    # why those steps are small -- asserted rather than left as a comment
    assert cm.pp_steady_states(
        cm.pp_params(D=hi + 0.007))["coexistence"].shape[0] >= 1
    assert cm.pp_steady_states(
        cm.pp_params(D=hi + 0.012))["coexistence"].shape[0] == 0


def test_the_deposits_own_dilution_rate_sits_inside_the_oscillatory_region(
        hopf_Ds):
    """D = 0.1125 is between the two crossings, so the deposit's defaults oscillate.

    That is the consistency check on the transcription that matters: the
    curation says it was validated by reproducing the paper's figures, and
    those figures oscillate. The leading real part at the default parameters is
    pinned two-sided.
    """
    lo, hi = float(hopf_Ds[0]), float(hopf_Ds[1])
    assert lo < cm.PP_PARAMS["D"] < hi
    lead = cm.pp_leading_real_part(cm.PP_PARAMS)
    assert lead == pytest.approx(0.0359707, rel=1e-5)
    assert lead > 0.0
    st = cm.pp_oscillatory_focus(cm.PP_PARAMS)
    assert st == pytest.approx(
        np.array([5.12450, 20.98003, 3.95715, 3.30022]), rel=1e-5)
    ev = np.linalg.eigvals(cm.pp_jacobian(st, cm.PP_PARAMS))
    assert float(np.max(np.abs(ev.imag))) > 0.1
    # the same point under the reduction is STABLE, which is the whole move
    assert cm.pp_leading_real_part(cm.PP_PARAMS, model="qss") < 0.0
    assert cm.pp_leading_real_part(cm.PP_PARAMS, model="qss") == \
        pytest.approx(-0.0624580, rel=1e-5)


def test_the_saddle_at_low_dilution_is_not_mistaken_for_the_focus():
    """At low D there are two interior points and only one can carry a Hopf.

    The second sits close to prey domination and its leading eigenvalue is
    REAL and positive -- a saddle. Tracking it would return a dilution rate
    that is not a bifurcation, so `pp_oscillatory_focus` selects on the leading
    pair being complex and this is what that selection is for.
    """
    for D in (0.002, 0.005, 0.01):
        q = cm.pp_params(D=D)
        arr = cm.pp_steady_states(q)["coexistence"]
        assert arr.shape[0] == 2, (D, arr)
        kinds = []
        for s in arr:
            ev = np.linalg.eigvals(cm.pp_jacobian(s, q))
            lead = ev[int(np.argmax(ev.real))]
            kinds.append((abs(lead.imag) > 1e-6, lead.real))
        complexes = [k for k in kinds if k[0]]
        reals = [k for k in kinds if not k[0]]
        assert len(complexes) == 1 and len(reals) == 1, (D, kinds)
        assert reals[0][1] > 0.0, "the saddle should be unstable"
        assert complexes[0][1] < 0.0, "the focus is stable below the first Hopf"
        focus = cm.pp_oscillatory_focus(q)
        assert focus is not None and focus[0] > 1.0
    # and there is no focus at all once coexistence is lost
    assert cm.pp_oscillatory_focus(cm.pp_params(D=0.25)) is None
    assert not np.isfinite(cm.pp_leading_real_part(cm.pp_params(D=0.25)))


def test_the_narrow_fold_below_the_loss_of_coexistence_needs_a_finer_grid():
    """A limitation of the scan, recorded rather than discovered later.

    Just below the dilution rate where coexistence is lost there is a narrow
    fold with THREE interior points, two of them close together. Every root
    either resolution returns is genuine -- residuals at machine precision --
    but the default scan can miss one, which is why `grid` is an argument and
    why the docstring says to raise it near a fold. The test asserts the
    direction (finer never finds fewer) and the genuineness, not a particular
    count, so it records the knob without freezing the defect.
    """
    found = {}
    for D in (0.1750, 0.1755, 0.1758, 0.1760, 0.1762, 0.1765):
        q = cm.pp_params(D=D)
        for g in (4001, 40001):
            arr = cm.pp_steady_states(q, grid=g)["coexistence"]
            found[(D, g)] = arr.shape[0]
            for s in arr:
                r = float(np.max(np.abs(cm.predator_prey_model(s, q))))
                assert 0.0 <= r <= 1e-8, (D, g, s, r)
        assert found[(D, 40001)] >= found[(D, 4001)], D
    assert found[(0.1750, 40001)] == 1
    assert found[(0.1760, 40001)] == 3, "the fold has three interior points"
    assert found[(0.1765, 40001)] == 0, "coexistence is gone by here"


def test_pp_guards():
    with pytest.raises(ValueError, match="four entries"):
        cm.predator_prey_model([1.0, 2.0], cm.PP_PARAMS)
    with pytest.raises(ValueError, match="two entries"):
        cm.pp_qss_model([1.0, 2.0, 3.0, 4.0], cm.PP_PARAMS)
    with pytest.raises(ValueError, match="cannot be negative"):
        cm.predator_prey_model([-1.0, 1.0, 1.0, 1.0], cm.PP_PARAMS)
    with pytest.raises(ValueError, match="cannot be negative"):
        cm.pp_qss_model([-1.0, 1.0], cm.PP_PARAMS)
    with pytest.raises(ValueError, match="C1, C2, A1, A2"):
        cm.pp_jacobian([1.0, 2.0, 3.0], cm.PP_PARAMS)
    with pytest.raises(ValueError, match="missing"):
        cm.predator_prey_model([1.0, 1.0, 1.0, 1.0], {"kc1": 0.8})
    with pytest.raises(ValueError, match="Cm must be"):
        cm.pp_steady_states(cm.pp_params(Cm=0.0))
    with pytest.raises(ValueError, match="D_lo < D_hi"):
        cm.pp_hopf_D(cm.PP_PARAMS, D_lo=0.5, D_hi=0.1)
    with pytest.raises(ValueError, match="which must be"):
        cm.pp_hopf_D(cm.PP_PARAMS, which="middle")
    with pytest.raises(ValueError, match="model must be"):
        cm.pp_leading_real_part(cm.PP_PARAMS, model="reduced")
    with pytest.raises(ValueError, match="dAA \\+ D must be"):
        cm.pp_steady_states(cm.pp_params(dAA1=0.0, dAA2=0.0, D=0.0))


# ======================================================================
# MOVE 5 -- Tsoi's criterion, with the burden form as an argument
# ======================================================================
def test_the_three_burden_forms_are_ordered_and_are_equal_at_zero_burden():
    """f_hill >= f_exp >= f_lin, with EQUALITY at B = 0, where all three are 1.

    This is a fact about the three functions and not about Tsoi's figure. The
    equality at zero matters more than it looks: a test that demanded a
    strictly positive gap everywhere would fail the correct answer at B = 0,
    which is the mistake this file is written against.
    """
    fl = cm.burden_form("linear")
    fe = cm.burden_form("exponential")
    fh = cm.burden_form("hill", n=2.0)
    assert float(fl(0.0)) == 1.0
    assert float(fe(0.0)) == 1.0
    assert float(fh(0.0)) == 1.0
    assert float(fh(0.0)) - float(fe(0.0)) == 0.0     # exactly, and allowed
    B = np.linspace(0.0, 10.0, 1001)
    assert np.all(fh(B) >= fe(B)) and np.all(fe(B) >= fl(B))
    assert np.all(fh(B[1:]) > fe(B[1:])), "strict once the burden is nonzero"
    assert np.all(fe(B[1:]) > fl(B[1:]))
    # the linear form is floored at zero rather than going negative
    assert float(fl(2.0)) == 0.0
    assert np.all(fl(B) >= 0.0) and np.all(fe(B) > 0.0) and np.all(fh(B) > 0.0)
    assert np.all(fh(B) <= 1.0)


def test_at_zero_burden_division_of_labor_loses_by_an_exact_factor():
    """rho1 = rho2 = rho/2 is Tsoi's assumption, and at zero burden it bites.

    With no burden all three populations grow at mu_max, so
    v = rho(1 - delta/mu_max) and v1 = v2 = v/2. Then Eq. 16's left side is
    v1 v2/v^2 = 1/4 and theta_I is v2/v = 1/2, both EXACT rationals, and the
    single cell wins by a factor of two in yield. Division of labor has to earn
    its way out of that.
    """
    r = cm.dol_criterion(0.0, 0.0)
    assert r["lhs"] == pytest.approx(0.25, rel=1e-15)
    assert r["theta_I"] == pytest.approx(0.5, rel=1e-15)
    assert r["v1"] == pytest.approx(0.5 * r["v"], rel=1e-15)
    assert r["v2"] == pytest.approx(0.5 * r["v"], rel=1e-15)
    assert r["yield_dol"] / r["yield_sc"] == pytest.approx(0.5, rel=1e-13)
    assert r["dol_favored"] is False


@pytest.mark.parametrize("form", ["linear", "exponential", "hill"])
@pytest.mark.parametrize("delta_me", [0.0, 0.01, 0.2])
@pytest.mark.parametrize("B", [0.05, 0.3, 0.6, 0.85])
def test_the_ratio_form_and_the_yield_comparison_are_the_same_criterion(
        form, delta_me, B):
    """Eq. 16 is a rewriting of p_DOL v2 > p_SC v, so the two must agree in sign.

    The yield comparison is the definition; the ratio is the algebra. Checking
    them against each other is an independent computation of that algebra, and
    it is the only check in this file that touches Eq. 16 at all.

    THE BURDENS ARE CHOSEN SO THAT NOTHING WASHES OUT, for all three forms, so
    that every case here actually runs: the linear form floors at zero growth
    at B = 1 and cannot cover the turnover rate of 0.1 past B = 0.9, which
    would have turned half this grid into skips. The washed-out case is covered
    on its own below, where the ratio form is genuinely undefined.
    """
    r = cm.dol_criterion(0.5 * B, 0.5 * B, burden=form, delta_me=delta_me)
    assert r["v"] > 0.0 and r["v1"] > 0.0 and r["v2"] > 0.0
    gap = r["lhs"] - r["theta_I"]
    assert abs(gap) > 1e-9, "too close to the border to compare signs"
    assert np.sign(gap) == np.sign(r["yield_dol"] - r["yield_sc"]), r


@pytest.mark.parametrize("form,B", [
    ("exponential", 1.2), ("exponential", 1.6),
    ("exponential", 2.0), ("exponential", 2.2),
    ("hill", 1.2), ("hill", 1.8), ("hill", 2.4), ("hill", 2.8)])
def test_the_two_forms_agree_past_their_crossings_too(form, B):
    """The same algebra check on the far side, where division of labor wins.

    The linear form is absent because it has already floored at zero growth by
    B = 1; these two have not, so this is the regime the previous test cannot
    reach. The grids are per-form because the forms wash out at different
    burdens -- exp(-B) drops below the turnover rate of 0.1 at B = 2.30 while
    1/(1+B^2) does not until B = 3.00 -- and each grid straddles its own
    crossing, 1.83 for the exponential form and 2.27 for the Hill form.
    """
    r = cm.dol_criterion(0.5 * B, 0.5 * B, burden=form)
    assert r["v"] > 0.0
    gap = r["lhs"] - r["theta_I"]
    assert abs(gap) > 1e-9
    assert np.sign(gap) == np.sign(r["yield_dol"] - r["yield_sc"]), r


@pytest.mark.parametrize("form", ["linear", "exponential", "hill"])
def test_more_burden_favors_division_of_labor_and_the_crossing_is_ordered(form):
    """Eq. 17's first term, as a crossing -- and the ordering of the three forms.

    At low burden the single cell wins and at high burden division of labor
    does, so there is a crossing in between; it is bracketed two-sided here
    rather than bounded on one side. The crossings themselves come out ordered
    linear < exponential < Hill, which FOLLOWS FROM the pointwise ordering of
    the three functions and is tested there -- the Hill form lets the host
    carry the most burden before splitting pays.

    NOT TESTED, deliberately: Fig. 2D's 20, 36 and 78. Those are a
    one-significant-figure digitization of a figure whose own caption says the
    parameters were CHOSEN so that the Hill form reduces growth least and the
    linear form most, so the factor of about five between them is the spread of
    a chosen example. The ordering survives that. The numbers do not.
    """
    def gap(B):
        r = cm.dol_criterion(0.5 * B, 0.5 * B, burden=form)
        return r["yield_dol"] - r["yield_sc"]

    assert gap(1e-6) < 0.0, "the single cell must win at negligible burden"
    hi = {"linear": 1.5, "exponential": 3.0, "hill": 5.0}[form]
    assert gap(hi) > 0.0, "division of labor must win somewhere"
    B_cross = brentq(gap, 1e-6, hi, xtol=1e-12)
    expect = {"linear": 0.82918, "exponential": 1.83258,
              "hill": 2.26779}[form]
    assert B_cross == pytest.approx(expect, rel=1e-4)
    # two-sided around the crossing, and the sign changes across it
    assert gap(B_cross * 0.95) < 0.0 < gap(B_cross * 1.05)
    assert cm.dol_criterion(0.5 * B_cross * 1.1, 0.5 * B_cross * 1.1,
                            burden=form)["dol_favored"] is True
    assert cm.dol_criterion(0.5 * B_cross * 0.9, 0.5 * B_cross * 0.9,
                            burden=form)["dol_favored"] is False


def test_the_crossings_are_ordered_linear_then_exponential_then_hill():
    """The ordering on its own, since it is the only claim Fig. 2D supports."""
    def cross(form, hi):
        return brentq(lambda B: (cm.dol_criterion(0.5 * B, 0.5 * B,
                                                  burden=form)["yield_dol"]
                                 - cm.dol_criterion(0.5 * B, 0.5 * B,
                                                    burden=form)["yield_sc"]),
                      1e-6, hi, xtol=1e-12)
    lin = cross("linear", 1.5)
    exp = cross("exponential", 3.0)
    hil = cross("hill", 5.0)
    assert lin < exp < hil
    assert 1.5 < hil / lin < 4.0        # a spread, bounded both ways


def test_a_washed_out_single_cell_is_handled_rather_than_dividing_by_zero():
    """At enough burden the single cell cannot cover its own turnover.

    v = 0 there, so the yield comparison is 0 against something positive and
    division of labor wins; Eq. 16's ratio is +inf and theta_I is undefined,
    which is why `dol_favored` is computed from the yields and not the ratio.
    """
    # Each enzyme at 0.5: the single cell carries 1.0, where the linear form
    # floors at zero growth, while each DOL population carries 0.5 and grows at
    # 0.5 -- comfortably above the turnover rate of 0.1.
    r = cm.dol_criterion(0.5, 0.5, burden="linear")
    assert r["mu"] == 0.0 and r["mu1"] > 0.1 and r["mu2"] > 0.1
    assert r["v"] == 0.0
    assert r["yield_sc"] == 0.0
    assert r["v1"] > 0.0 and r["v2"] > 0.0 and r["yield_dol"] > 0.0
    assert r["dol_favored"] is True
    assert np.isinf(r["lhs"])
    # and when EVERYTHING washes out the yields are both exactly zero, so
    # neither strategy is favored -- the right answer is 0.0 == 0.0, and a test
    # that demanded a strict inequality here would fail it.
    both = cm.dol_criterion(5.0, 5.0, burden="linear")
    assert both["v"] == 0.0 and both["v1"] == 0.0 and both["v2"] == 0.0
    assert both["yield_sc"] == 0.0 and both["yield_dol"] == 0.0
    assert both["dol_favored"] is False


def test_dol_splits_the_burden_which_is_the_whole_mechanism():
    """mu sees beta_e1 + gamma_e2; mu1 sees beta_e1; mu2 sees gamma_e2."""
    r = cm.dol_criterion(0.3, 0.5, burden="hill", n=2.0)
    f = cm.burden_form("hill", n=2.0)
    assert r["mu"] == pytest.approx(float(f(0.8)), rel=1e-15)
    assert r["mu1"] == pytest.approx(float(f(0.3)), rel=1e-15)
    assert r["mu2"] == pytest.approx(float(f(0.5)), rel=1e-15)
    assert r["mu1"] > r["mu"] and r["mu2"] > r["mu"]
    # a callable is accepted, which is what "the functional form is an
    # argument" has to mean if the session is to vary it
    same = cm.dol_criterion(0.3, 0.5, burden=lambda B: 1.0 / (1.0 + B ** 2.0))
    assert same["yield_dol"] == pytest.approx(r["yield_dol"], rel=1e-15)
    assert same["yield_sc"] == pytest.approx(r["yield_sc"], rel=1e-15)


def test_eps_zero_reduces_the_criterion_to_a_biomass_comparison():
    """delta_me = 0 is Tsoi's eps = 0, and there Eq. 16 collapses to v1 > v.

    Worth pinning because it is a sharper statement than the criterion looks:
    with no extracellular turnover the whole question is whether one DOL
    population on half the carrying capacity outgrows the single cell on all
    of it.
    """
    for B in (0.1, 0.5, 0.83, 1.0, 1.4):
        r = cm.dol_criterion(0.5 * B, 0.5 * B, burden="linear", delta_me=0.0)
        assert r["eps"] == 0.0
        if r["v"] > 0.0:
            assert r["dol_favored"] == bool(r["v1"] > r["v"]), (B, r)


def test_dol_guards():
    with pytest.raises(ValueError, match="burden form must be"):
        cm.burden_form("quadratic")
    with pytest.raises(ValueError, match="Hill coefficient"):
        cm.burden_form("hill", n=0.0)
    with pytest.raises(ValueError, match="burden is non-negative"):
        cm.dol_criterion(-0.1, 0.2)
    with pytest.raises(ValueError, match="need mu_max"):
        cm.dol_criterion(0.1, 0.1, mu_max=0.0)
    with pytest.raises(ValueError, match="need eta"):
        cm.dol_criterion(0.1, 0.1, eta=0.0)


# ======================================================================
# the module itself
# ======================================================================
def test_the_module_is_importable_without_touching_the_package_init():
    """posb/__init__.py does not list this module, and must not have to.

    `from posb import communities` resolves the submodule on its own. If this
    ever fails it means something added an eager import, and a sibling module
    landing in the same week would then be able to break this one.
    """
    import posb
    assert not hasattr(posb, "__communities_imported__")
    from posb import communities
    assert communities is cm
    for name in cm.__all__:
        assert hasattr(cm, name), name
