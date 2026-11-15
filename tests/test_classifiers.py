"""Session 26 -- a multi-input classifier, and a budget for its mistakes.

EVERY RESPONSE MATRIX IN THIS FILE IS SYNTHETIC AND IS LABELLED SO, WITH ONE
EXCEPTION NAMED BELOW. Apart from `XIE_FIG2D`, none of these numbers is
Xie's. Fig. 2D's digitization was not finished when this file was written,
and a test suite that waits on a digitization is a suite that does not
run -- so the panels here are invented, with marker and cell-line names
borrowed from the paper only to keep the shape honest (7 lines, 5
sensor modules, one positive, two markers required HIGH and three required
ABSENT). Their values are chosen so that every output, ratio and count below
can be checked by hand in the margin.

THE EXCEPTION, AND WHY IT IS ONE. `XIE_FIG2D` is the real digitized Fig. 2D
matrix, copied from `sessions/s26-therapeutics/NUMBERS.md` sec 2.2, which
stays the source of truth for it. It is here because the regression it locks
cannot be reproduced on an invented panel: the per-marker sense check that
`convention_check` replaced fired on THAT matrix, in the correct convention,
with the right senses, and on four of its five leave-one-out subsets. A
synthetic panel would have let the fix pass without ever meeting the input
that broke.

WHAT THIS FILE IS FOR, WHICH IS NOT THE ARITHMETIC. The product of five
factors is not where this gets got wrong. What gets got wrong is the SENSE of
a marker -- whether a NOT term has been applied once or twice -- and the
DIRECTION in which error rates move with the threshold. A reversed sense
scores a correct answer as wrong, which on an autograded problem set is worse
than a crash. So most of what is locked here is a property: a sign, an
inequality, a monotonicity, or a refusal.

HOUSE RULE, INHERITED FROM test_populations.py: tolerances are two-sided, and
`assert x < c` is avoided where `x == 0` would also pass it.
"""
import itertools
import pathlib

import numpy as np
import pytest

from posb import classifiers as cf
from posb import evolution as ev

# --------------------------------------------------------------------------
# SYNTHETIC panel A -- hand-computable, with exact zeros and ones.
# Xie's shape: HeLa positive, miR-21 and miR-17-30a required HIGH, miR-141,
# miR-142(3p) and miR-146a required ABSENT. THE VALUES ARE INVENTED.
# --------------------------------------------------------------------------
MARKERS = ["miR-21", "miR-17-30a", "miR-141", "miR-142-3p", "miR-146a"]
SENSE = {"miR-21": "high", "miR-17-30a": "high",
         "miR-141": "absent", "miR-142-3p": "absent", "miR-146a": "absent"}
LINES = ["HeLa", "MCF7", "SKBR3", "T47D", "DAOY", "SH-SY5Y", "HEK293"]
PANEL_A = cf.response_table(
    [[1.0, 1.0, 0.0, 0.0, 0.0],      # HeLa    -> 1.0
     [0.5, 1.0, 0.5, 0.0, 0.0],      # MCF7    -> 0.25
     [1.0, 0.5, 0.0, 0.5, 0.0],      # SKBR3   -> 0.25
     [0.0, 1.0, 0.0, 0.0, 0.0],      # T47D    -> 0.0
     [1.0, 1.0, 0.0, 0.0, 0.5],      # DAOY    -> 0.5
     [0.5, 0.5, 0.0, 0.0, 0.0],      # SH-SY5Y -> 0.25
     [1.0, 1.0, 0.0, 0.0, 0.9]],     # HEK293  -> 0.1
    LINES, MARKERS)
OUT_A = {"HeLa": 1.0, "MCF7": 0.25, "SKBR3": 0.25, "T47D": 0.0,
         "DAOY": 0.5, "SH-SY5Y": 0.25, "HEK293": 0.1}

# SYNTHETIC panel B -- the same shape with no exact zeros, so that an
# inverted sense still produces a computable (and wrong) classifier instead
# of a division by zero. Every line misses on exactly one factor, so the
# declared classifier is clean at Xie's 20% cut: HeLa is 0.9^5 = 0.59049 and
# no negative exceeds 0.0729, a ratio of 0.123.
PANEL_B = cf.response_table(
    [[0.9, 0.9, 0.1, 0.1, 0.1],      # HeLa    -> 0.59049
     [0.1, 0.9, 0.1, 0.1, 0.1],      # MCF7    -> 0.0729
     [0.9, 0.1, 0.1, 0.1, 0.1],      # SKBR3   -> 0.0729
     [0.2, 0.2, 0.1, 0.1, 0.1],      # T47D    -> 0.02916
     [0.9, 0.9, 0.9, 0.1, 0.1],      # DAOY    -> 0.06561
     [0.9, 0.9, 0.1, 0.9, 0.1],      # SH-SY5Y -> 0.06561
     [0.9, 0.9, 0.1, 0.1, 0.9]],     # HEK293  -> 0.06561
    LINES, MARKERS)

INVERTED = {m: ("absent" if s == "high" else "high") for m, s in SENSE.items()}


# ------------------------------------------------------------ the product ---
def test_output_is_the_product_of_the_sensor_contributions():
    """Checked against the hand arithmetic in the panel's own comments."""
    got = cf.classifier_output(PANEL_A, MARKERS, SENSE)
    assert set(got) == set(LINES)
    for line, want in OUT_A.items():
        assert got[line] == pytest.approx(want, rel=1e-14, abs=1e-15), line
    # and independently, as an explicit product over the five factors
    for line in LINES:
        row = PANEL_A[line]
        hand = 1.0
        for m in MARKERS:
            hand *= row[m] if SENSE[m] == "high" else 1.0 - row[m]
        assert got[line] == pytest.approx(hand, rel=1e-14, abs=1e-15)


def test_the_positive_line_is_the_largest_output_under_the_right_sense():
    got = cf.classifier_output(PANEL_A, MARKERS, SENSE)
    assert max(got, key=got.get) == "HeLa"
    assert all(got["HeLa"] > got[ln] for ln in LINES if ln != "HeLa")


def test_an_output_is_a_fraction_not_a_boolean():
    """The session's first move: the logic is continuous, with a cut on it.

    Three distinct interior values among six negatives -- nothing here is 0
    or 1 -- is what makes a threshold a design variable rather than a
    formality.
    """
    got = cf.classifier_output(PANEL_A, MARKERS, SENSE)
    interior = sorted({v for v in got.values() if 0.0 < v < 1.0})
    assert len(interior) >= 3, got
    assert all(0.0 <= v <= 1.0 for v in got.values())


def test_empty_and_repeated_marker_sets_are_refused():
    with pytest.raises(ValueError, match="at least one marker"):
        cf.classifier_output(PANEL_A, [], SENSE)
    with pytest.raises(ValueError, match="repeat"):
        cf.classifier_output(PANEL_A, ["miR-21", "miR-21"], SENSE)


# ------------------------------------------------------- the sign, locked ---
def test_sensor_response_is_level_for_high_and_one_minus_level_for_absent():
    """THE SIGN TEST. This fails if the convention is ever reversed.

    'high' passes the marker level through; 'absent' subtracts it from one.
    A module that swapped these would still produce a product, still produce
    confusion matrices, and still look like a classifier -- it would just be
    a classifier for everything the target cell is not.
    """
    assert float(cf.sensor_response(0.0, "high")) == 0.0
    assert float(cf.sensor_response(1.0, "high")) == 1.0
    assert float(cf.sensor_response(0.0, "absent")) == 1.0
    assert float(cf.sensor_response(1.0, "absent")) == 0.0
    lv = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    assert np.allclose(cf.sensor_response(lv, "high"), lv, rtol=0, atol=0)
    assert np.allclose(cf.sensor_response(lv, "absent"), 1.0 - lv,
                       rtol=0, atol=0)
    # and the two senses agree nowhere except at exactly one half
    same = np.isclose(cf.sensor_response(lv, "high"),
                      cf.sensor_response(lv, "absent"))
    assert same.tolist() == [False, False, True, False, False]


def test_inverting_every_sense_turns_a_good_classifier_into_a_bad_one():
    """THE SECOND SIGN TEST, at the level of the whole circuit.

    Panel B has no exact zeros, so the inverted circuit is computable rather
    than degenerate -- and it is not merely worse, it is upside down. Under
    the declared sense HeLa has the LARGEST output and no negative line
    clears a 20% cut. Under the globally inverted sense HeLa has the SMALLEST
    output in the panel, every negative line outputs more than the target
    cell does, and there is therefore no threshold anywhere that excludes
    even one of them: T47D outputs 64 times HeLa (0.8^2 * 0.1^3 / 0.1^5).

    This is the defect that an autograder cannot survive. The inverted
    circuit raises nothing, returns plausible fractions, and marks the right
    answer wrong.
    """
    good = cf.classifier_output(PANEL_B, MARKERS, SENSE)
    bad = cf.classifier_output(PANEL_B, MARKERS, INVERTED)
    assert max(good, key=good.get) == "HeLa"
    assert min(bad, key=bad.get) == "HeLa"
    assert all(bad[ln] > bad["HeLa"] for ln in LINES if ln != "HeLa")
    assert bad["T47D"] / bad["HeLa"] == pytest.approx(64.0, rel=1e-12)

    c_good = cf.confusion(PANEL_B, MARKERS, SENSE, "HeLa", 0.2)
    assert c_good.as_tuple() == (1, 0, 6, 0)
    for thr in (0.05, 0.1, 0.2, 0.4, 0.8, 1.0):
        c_bad = cf.confusion(PANEL_B, MARKERS, INVERTED, "HeLa", thr)
        assert c_bad.fp == 6, (thr, c_bad)
        assert c_bad.specificity == 0.0
        assert c_bad.fp >= cf.confusion(PANEL_B, MARKERS, SENSE,
                                        "HeLa", thr).fp


def test_inverting_the_sense_on_panel_a_switches_the_target_cell_off():
    """With exact zeros the inverted circuit does not even run, and the
    refusal names the cause rather than returning a confusion matrix over a
    division by zero."""
    out = cf.classifier_output(PANEL_A, MARKERS, INVERTED)
    assert out["HeLa"] == 0.0
    with pytest.raises(ValueError, match="CANNOT HELP"):
        cf.confusion(PANEL_A, MARKERS, INVERTED, "HeLa", 0.2)


def test_sense_check_is_silent_when_right_and_names_convention_when_wrong():
    """The complaint is now ONE statement about the panel, not one per marker.

    It used to be per marker, and asserting that every marker got named is
    what made the check look thorough while it was in fact firing on correct
    inputs -- see `convention_check`. The per-marker reporting moved to
    `marker_utility`, which is not a complaint channel, so what is locked
    here is the panel-wide statement and its direction.
    """
    assert cf.sense_check(PANEL_B, MARKERS, SENSE, "HeLa") == []
    complaints = cf.sense_check(PANEL_B, MARKERS, INVERTED, "HeLa")
    assert len(complaints) == 1, complaints
    said = complaints[0]
    assert "'HeLa' is not the panel maximum" in said
    assert "inverting EVERY marker's sense" in said
    got = cf.convention_check(PANEL_B, MARKERS, INVERTED, "HeLa")
    assert got.ok is False and got.alternative == "global-polarity"
    assert got.message == said
    # and the per-marker reporting still names every marker, elsewhere
    rows = cf.marker_utility(PANEL_B, MARKERS, INVERTED, "HeLa")
    assert [r.marker for r in rows] == MARKERS


def test_sense_check_names_a_marker_that_switches_the_target_off():
    panel = cf.response_table([[1.0, 0.0], [0.5, 0.5]],
                              ["TARGET", "OTHER"], ["A", "B"])
    said = cf.sense_check(panel, ["A", "B"], {"A": "high", "B": "high"},
                          "TARGET")
    assert any("fires on nothing" in s and "'B'" in s for s in said), said


def test_sense_check_names_an_uninformative_marker():
    """A marker with the same contribution everywhere cancels out of every
    ratio, so under a relative threshold it changes no call at all."""
    panel = cf.response_table([[1.0, 0.4], [0.2, 0.4]],
                              ["TARGET", "OTHER"], ["A", "FLAT"])
    said = cf.sense_check(panel, ["A", "FLAT"], {"A": "high", "FLAT": "high"},
                          "TARGET")
    assert any("cancels out" in s for s in said), said
    one = cf.confusion(panel, ["A"], {"A": "high"}, "TARGET", 0.5)
    both = cf.confusion(panel, ["A", "FLAT"],
                        {"A": "high", "FLAT": "high"}, "TARGET", 0.5)
    assert one.as_tuple() == both.as_tuple()


def test_a_boolean_sense_is_refused_with_the_reason():
    with pytest.raises(ValueError, match="never True/False"):
        cf.sensor_response(0.5, True)
    with pytest.raises(ValueError, match="not a sense"):
        cf.sensor_response(0.5, "low")
    with pytest.raises(ValueError, match="ambiguous"):
        cf.sensor_response(0.5, "off")
    with pytest.raises(ValueError, match="no sense given"):
        cf.classifier_output(PANEL_A, MARKERS,
                             {m: "high" for m in MARKERS[:2]})


# ------------------------------------------------------- the threshold -----
def test_the_threshold_has_no_default():
    """The session's whole point. A default would hand back one member of a
    family and hide the family."""
    with pytest.raises(TypeError):
        cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa")


@pytest.mark.parametrize("thr,fp", [(0.05, 5), (0.2, 4), (0.3, 1), (0.5, 1),
                                    (0.6, 0), (1.0, 0)])
def test_the_family_indexed_by_the_threshold(thr, fp):
    """Four false positives at Xie's printed 20% cut, none at 60%.

    Ratios to HeLa in panel A are 0.25, 0.25, 0.0, 0.5, 0.25, 0.1, so the cut
    crosses them at 0.1, 0.25 and 0.5 and the counts step there. One
    classifier, six answers.
    """
    c = cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", thr)
    assert c.fp == fp
    assert c.tp == 1 and c.fn == 0
    assert c.tn == 6 - fp
    assert c.fp_rate == pytest.approx(fp / 6.0)
    assert c.specificity == pytest.approx(1.0 - fp / 6.0)
    assert c.sensitivity == 1.0


def test_a_line_exactly_on_the_threshold_is_called_positive():
    """The comparison is >=, which is what makes the positive line a true
    positive at threshold 1.0, and it has to be a stated convention."""
    c = cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", 0.5)
    assert c.fp == 1          # DAOY sits exactly at 0.5
    assert cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", 1.0).tp == 1


def test_perfect_separator_gives_no_false_positives_at_any_cut_between():
    """FP = 0 for every threshold strictly between the classes, and the
    property is checked across the whole gap rather than at one point."""
    panel = cf.response_table(
        [[1.0, 0.0], [0.3, 0.0], [0.2, 0.0], [0.25, 0.0]],
        ["TARGET", "N1", "N2", "N3"], ["A", "B"])
    sense = {"A": "high", "B": "absent"}
    out = cf.classifier_output(panel, ["A", "B"], sense)
    gap_lo = max(out[ln] for ln in ("N1", "N2", "N3")) / out["TARGET"]
    assert gap_lo == pytest.approx(0.3)
    for thr in np.linspace(0.31, 1.0, 40):
        c = cf.confusion(panel, ["A", "B"], sense, "TARGET", float(thr))
        assert c.as_tuple() == (1, 0, 3, 0), thr
    # and below the gap every negative is a false positive, so the test is
    # not passing because the computation returned zero for everything
    c = cf.confusion(panel, ["A", "B"], sense, "TARGET", 0.19)
    assert c.fp == 3


@pytest.mark.parametrize("seed", range(12))
def test_raising_the_threshold_cannot_increase_fp_or_tp(seed):
    """T70, LOCKED IN BOTH DIRECTIONS. Raising the cut can only remove calls:
    false positives are non-increasing and true positives are non-increasing,
    and the trade-off is that they move together. A module in which one of
    them went up with the threshold would be computing something else.

    Random panels, both threshold conventions, because the property is about
    the comparison and not about the arithmetic above it.
    """
    rng = np.random.default_rng(seed)
    marks = [f"m{i}" for i in range(4)]
    sense = {m: ("high" if rng.random() < 0.5 else "absent") for m in marks}
    lines = [f"L{i}" for i in range(6)]
    panel = cf.response_table(rng.random((6, 4)), lines, marks)
    grid = np.linspace(0.02, 1.0, 50)
    for relative in (True, False):
        fps, tps = [], []
        for thr in grid:
            c = cf.confusion(panel, marks, sense, "L0", float(thr),
                             relative=relative)
            fps.append(c.fp)
            tps.append(c.tp)
        assert np.all(np.diff(fps) <= 0), (relative, fps)
        assert np.all(np.diff(tps) <= 0), (relative, tps)
    # the sweep must actually move, or the monotonicity is vacuous
    assert cf.confusion(panel, marks, sense, "L0", 0.02).fp >= \
        cf.confusion(panel, marks, sense, "L0", 1.0).fp


def test_a_relative_threshold_outside_its_range_is_refused():
    with pytest.raises(ValueError, match="fraction of the positive"):
        cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", 1.5)
    with pytest.raises(ValueError, match="fraction of the positive"):
        cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", 0.0)
    with pytest.raises(ValueError, match="output level"):
        cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", 2.0, relative=False)


def test_absolute_and_relative_agree_when_the_positive_output_is_one():
    """Panel A's HeLa output is exactly 1.0, so the two conventions coincide
    there -- which is the only place they do, and worth pinning so the
    difference elsewhere is not read as a bug."""
    for thr in (0.1, 0.3, 0.6):
        a = cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", thr,
                         relative=False)
        r = cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", thr, relative=True)
        assert a.as_tuple() == r.as_tuple()


# -------------------------------------------------- adding a marker -------
def test_adding_a_marker_absent_in_the_positive_line_cannot_help():
    """It switches the circuit off in the cell you are trying to hit.

    Under the relative convention there is no threshold at all -- a fraction
    of zero is not a cut -- and the refusal says so. Under the absolute
    convention the arithmetic runs and loses the true positive, which is the
    same fact with a number attached.
    """
    marks = MARKERS + ["miR-dead"]
    sense = dict(SENSE, **{"miR-dead": "high"})
    panel = {ln: dict(row, **{"miR-dead": 0.0 if ln == "HeLa" else 0.8})
             for ln, row in PANEL_A.items()}
    assert cf.classifier_output(panel, marks, sense)["HeLa"] == 0.0
    with pytest.raises(ValueError, match="CANNOT HELP"):
        cf.confusion(panel, marks, sense, "HeLa", 0.2)
    lost = cf.confusion(panel, marks, sense, "HeLa", 0.2, relative=False)
    assert lost.tp == 0 and lost.fn == 1
    kept = cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", 0.2, relative=False)
    assert kept.tp == 1


@pytest.mark.parametrize("seed", range(12))
def test_adding_a_marker_that_separates_must_not_hurt(seed):
    """Under the relative cut, a marker whose contribution in the positive
    line is at least its contribution in every negative multiplies each
    negative's RATIO by a factor <= 1 and leaves the positive's ratio at
    exactly 1. So FP cannot rise and the true positive cannot be lost.

    This is the property that makes the relative convention the right one,
    and it is checked against random panels rather than argued.
    """
    rng = np.random.default_rng(1000 + seed)
    marks = [f"m{i}" for i in range(4)]
    sense = {m: "high" for m in marks}
    lines = [f"L{i}" for i in range(6)]
    panel = cf.response_table(rng.random((6, 4)), lines, marks)
    # a separating marker: full level in the positive, anything below it
    # elsewhere
    sep = {ln: (1.0 if ln == "L0" else float(rng.random())) for ln in lines}
    grown = {ln: dict(panel[ln], sep=sep[ln]) for ln in lines}
    for thr in (0.05, 0.2, 0.5, 0.9, 1.0):
        before = cf.confusion(panel, marks, sense, "L0", thr)
        after = cf.confusion(grown, marks + ["sep"],
                             dict(sense, sep="high"), "L0", thr)
        assert after.fp <= before.fp, (thr, before, after)
        assert after.tp == before.tp == 1


def test_an_absolute_threshold_can_lose_the_positive_to_a_good_marker():
    """The documented asymmetry, pinned as a counterexample rather than left
    as a claim in a docstring. The marker below separates perfectly -- 0.3 in
    the target against 0.1 in every negative -- and under an absolute cut of
    0.4 adding it destroys the classifier it should improve. Under the
    relative cut at the same number it does not.
    """
    panel = cf.response_table([[1.0, 0.3], [0.5, 0.1], [0.45, 0.1]],
                              ["TARGET", "N1", "N2"], ["A", "SEP"])
    sense = {"A": "high", "SEP": "high"}
    one = cf.confusion(panel, ["A"], sense, "TARGET", 0.4, relative=False)
    two = cf.confusion(panel, ["A", "SEP"], sense, "TARGET", 0.4,
                       relative=False)
    assert one.tp == 1 and one.fp == 2
    assert two.tp == 0, "the absolute cut should have lost the true positive"
    rel = cf.confusion(panel, ["A", "SEP"], sense, "TARGET", 0.4)
    assert rel.tp == 1 and rel.fp == 0


# ----------------------------------------------- the population statistic --
def test_wrong_cells_per_dose_is_linear_in_both_arguments():
    base = float(cf.wrong_cells_per_dose(0.01, 1e6))
    assert base == pytest.approx(1e4, rel=1e-14)
    assert float(cf.wrong_cells_per_dose(0.02, 1e6)) == pytest.approx(
        2.0 * base, rel=1e-14)
    assert float(cf.wrong_cells_per_dose(0.01, 3e6)) == pytest.approx(
        3.0 * base, rel=1e-14)
    r = np.array([0.0, 1e-6, 1e-3, 0.5, 1.0])
    n = np.array([1e3, 1e6, 1e9])
    got = cf.wrong_cells_per_dose(r[:, None], n[None, :])
    assert got.shape == (5, 3)
    assert np.allclose(got, r[:, None] * n[None, :], rtol=0, atol=0)


def test_wrong_cells_per_dose_is_escapers_per_dose_in_the_same_units():
    """T69 and T63 are the same arithmetic with the sign of the intent
    reversed, and PS9 is one set because of it. If these two ever disagree,
    one of the two sessions is lying about the other."""
    for rate, pop in [(1e-8, 1e8), (10 ** -8.6, 1e8), (1 / 6, 1e6),
                      (0.33, 1e9)]:
        assert float(cf.wrong_cells_per_dose(rate, pop)) == pytest.approx(
            float(ev.escapers_per_dose(pop, rate)), rel=0.0, abs=0.0)
    # the matched pair the course states out loud: a rate of 1e-8 against
    # 1e8 cells is a budget of exactly one.
    assert float(cf.wrong_cells_per_dose(1e-8, 1e8)) == pytest.approx(1.0)


def test_wrong_cells_per_dose_guards_its_units():
    with pytest.raises(ValueError, match="probability in"):
        cf.wrong_cells_per_dose(1.5, 1e6)
    with pytest.raises(ValueError, match="probability in"):
        cf.wrong_cells_per_dose(-1e-9, 1e6)
    with pytest.raises(ValueError, match="positive number of cells"):
        cf.wrong_cells_per_dose(0.1, 0.0)


def test_six_clean_lines_bound_the_per_cell_rate_at_forty_percent():
    """What "no false positives in the panel" actually establishes. The exact
    one-sided bound with zero events is 1 - (1 - c)^(1/n)."""
    for n in (6, 20, 100):
        want = 1.0 - 0.05 ** (1.0 / n)
        assert cf.fp_rate_upper_bound(0, n) == pytest.approx(want, rel=1e-12)
    assert cf.fp_rate_upper_bound(0, 6) == pytest.approx(0.3930, abs=5e-5)
    # monotone in the count and in the panel size, both directions
    assert (cf.fp_rate_upper_bound(0, 6) < cf.fp_rate_upper_bound(1, 6)
            < cf.fp_rate_upper_bound(3, 6) < cf.fp_rate_upper_bound(6, 6))
    assert cf.fp_rate_upper_bound(6, 6) == 1.0
    assert cf.fp_rate_upper_bound(0, 100) < cf.fp_rate_upper_bound(0, 6)
    # the bound always covers the observed rate; a panel never beats itself
    for n in (3, 6, 20):
        for k in range(n + 1):
            assert cf.fp_rate_upper_bound(k, n) >= k / n - 1e-12


def test_the_observed_rate_and_the_bound_disagree_by_orders_of_magnitude():
    """The number T70 is about. Zero false positives among six lines meets a
    budget of one wrong cell in a million-cell dose on the observed rate, and
    misses it by five orders of magnitude on the bound.
    """
    pop = 1e6
    assert float(cf.wrong_cells_per_dose(0.0, pop)) == 0.0
    bound = cf.fp_rate_upper_bound(0, 6)
    assert float(cf.wrong_cells_per_dose(bound, pop)) > 1e5


def test_fp_rate_upper_bound_guards():
    with pytest.raises(ValueError, match="at least one negative"):
        cf.fp_rate_upper_bound(0, 0)
    with pytest.raises(ValueError, match="cannot exceed"):
        cf.fp_rate_upper_bound(7, 6)
    with pytest.raises(ValueError, match="probability in"):
        cf.fp_rate_upper_bound(0, 6, confidence=1.0)


def test_a_confusion_matrix_counts_lines_not_cells():
    """Named here so the distinction is in the suite and not only in a
    docstring: six negative lines cannot express a rate finer than 1/6."""
    rates = {cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", t).fp_rate
             for t in np.linspace(0.02, 1.0, 200)}
    assert rates <= {k / 6.0 for k in range(7)}
    assert min(r for r in rates if r > 0) == pytest.approx(1 / 6.0)


# ----------------------------------------------------- design to a budget --
def test_design_to_budget_finds_the_hand_computed_answer():
    d = cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=6.0,
                            budget=1.0, thresholds=(0.2, 0.6))
    assert d.found is True
    assert d.fp_lines == 0
    assert d.fn_lines == 0
    assert d.wrong_cells == 0.0
    assert d.threshold == 0.6
    assert d.n_negative == 6
    assert d.fp_rate_floor == pytest.approx(1 / 6.0)
    assert d.searched == (2 ** len(MARKERS) - 1) * 2
    assert d.population == 6.0 and d.budget == 1.0
    assert 0.0 < d.margin <= 1.0


def test_a_design_that_meets_its_budget_still_says_what_it_cannot_do():
    """Required behaviour, not decoration: the reason carries the resolution
    floor, the bound and the mixture caveat even on success."""
    d = cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=1e6,
                            budget=1.0, thresholds=(0.6,))
    assert d.found is True
    assert "CANNOT" in d.reason
    assert "below that resolution, not zero" in d.reason
    assert "Fig. 4B" in d.reason
    assert d.fp_rate == 0.0
    assert d.wrong_cells == 0.0
    assert d.fp_rate_bound == pytest.approx(cf.fp_rate_upper_bound(0, 6))
    assert d.wrong_cells_bound > 1e5          # the honest version of zero


def test_an_unmeetable_budget_returns_the_cannot_and_is_not_falsy():
    """The failure mode that must not read as success. `found` is False, the
    object itself is truthy, the reason says so in words, and the best
    classifier it did find is reported so the shortfall is a number.
    """
    d = cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=1e9,
                            budget=1.0, thresholds=(0.2, 0.3))
    assert bool(d) is True, "a failed search must not be falsy"
    assert d is not None and d != []
    assert d.found is False
    assert "NO SUBSET MEETS THIS BUDGET" in d.reason
    assert d.wrong_cells > d.budget
    assert d.markers and d.fn_lines == 0      # it found a real classifier
    assert "short by a factor" in d.reason


def test_a_classifier_that_calls_nothing_is_never_reported_as_found():
    """FP = 0 and FN = 1 meets every budget ever written and treats nobody.

    Under an absolute cut of 0.95, above every output any subset of panel B
    can produce in HeLa, no subset calls
    the positive line, and the search has to say that rather than hand back
    the zero.
    """
    d = cf.design_to_budget(PANEL_B, SENSE, "HeLa", population=1e6,
                            budget=1e9, thresholds=(0.95,),
                            relative=False)
    assert d.found is False
    assert "none even calls" in d.reason
    assert d.viable > 0        # the subsets were evaluable, they just missed
    # sanity: with the relative cut at the same number it does find one
    ok = cf.design_to_budget(PANEL_B, SENSE, "HeLa", population=1e6,
                             budget=1e9, thresholds=(0.95,))
    assert ok.found is True and ok.fn_lines == 0


def test_design_prefers_fewer_markers_on_a_tie_and_says_it_is_a_convention():
    """Fig. 2C's claim is about margin, not about the count, so the tie-break
    has to be visible: `margin` is reported next to the chosen subset."""
    d = cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=6.0,
                            budget=1.0, thresholds=(0.6,))
    assert d.found is True
    full = cf.confusion(PANEL_A, MARKERS, SENSE, "HeLa", 0.6)
    assert full.fp == 0                       # the full set also qualifies
    assert len(d.markers) <= len(MARKERS)
    # whatever it picked, it is a subset of the panel and it calls HeLa
    chosen = cf.confusion(PANEL_A, list(d.markers), SENSE, "HeLa",
                          d.threshold)
    assert chosen.fp == d.fp_lines and chosen.tp == 1


def test_design_skips_subsets_that_switch_the_target_cell_off():
    """A marker the positive line lacks makes the subset unevaluable rather
    than fatal: the search records it and moves on."""
    marks = ["A", "B", "dead"]
    panel = cf.response_table([[1.0, 0.0, 0.0], [0.2, 0.0, 0.9],
                               [0.1, 0.5, 0.9]],
                              ["TARGET", "N1", "N2"], marks)
    sense = {"A": "high", "B": "absent", "dead": "high"}
    d = cf.design_to_budget(panel, sense, "TARGET", population=2.0,
                            budget=1.0, thresholds=(0.5,))
    assert d.searched == 7 and d.viable == 3   # the four with 'dead' are off
    assert d.found is True
    assert "dead" not in d.markers


def test_the_search_states_its_combinatorial_bound_and_refuses_past_it():
    marks = [f"m{i}" for i in range(20)]
    lines = [f"L{i}" for i in range(4)]
    rng = np.random.default_rng(7)
    panel = cf.response_table(rng.random((4, 20)), lines, marks)
    sense = {m: "high" for m in marks}
    with pytest.raises(ValueError, match="EXHAUSTIVE"):
        cf.design_to_budget(panel, sense, "L0", population=1e6)
    with pytest.raises(ValueError, match="2\\^M"):
        cf.design_to_budget(panel, sense, "L0", population=1e6)
    # bounded subset size makes the same search tractable, and the count is
    # the one the docstring claims
    d = cf.design_to_budget(panel, sense, "L0", population=1e6,
                            max_markers=2, thresholds=(0.5,))
    assert d.searched == 20 + 190
    with pytest.raises(ValueError, match="max_markers must lie"):
        cf.design_to_budget(panel, sense, "L0", population=1e6,
                            max_markers=25)


def test_design_requires_a_population_and_a_sane_budget():
    with pytest.raises(TypeError):
        cf.design_to_budget(PANEL_A, SENSE, "HeLa")
    with pytest.raises(ValueError, match="treated population is positive"):
        cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=0.0)
    with pytest.raises(ValueError, match="WRONG CELLS"):
        cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=1e6,
                            budget=-1.0)
    with pytest.raises(ValueError, match="no thresholds"):
        cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=1e6,
                            thresholds=())


@pytest.mark.parametrize("seed", range(8))
def test_what_the_search_returns_is_reproducible_by_hand(seed):
    """Whatever the search reports, recomputing that one pair with
    `confusion` must give the same counts. A search that scores candidates
    differently from the function the student calls is an autograder that
    marks a right answer wrong.
    """
    rng = np.random.default_rng(2000 + seed)
    marks = [f"m{i}" for i in range(5)]
    sense = {m: ("high" if rng.random() < 0.5 else "absent") for m in marks}
    lines = [f"L{i}" for i in range(7)]
    panel = cf.response_table(rng.random((7, 5)), lines, marks)
    d = cf.design_to_budget(panel, sense, "L0", population=60.0,
                            budget=10.0, thresholds=(0.1, 0.25, 0.5, 0.75))
    assert isinstance(d.reason, str) and d.reason
    if not d.markers:
        return
    c = cf.confusion(panel, list(d.markers), sense, "L0", d.threshold)
    assert c.fp == d.fp_lines
    assert c.fn == d.fn_lines
    assert c.fp_rate == pytest.approx(d.fp_rate)
    assert float(cf.wrong_cells_per_dose(c.fp_rate, 60.0)) == pytest.approx(
        d.wrong_cells)


def test_the_search_is_exhaustive_over_the_pairs_it_claims():
    """Cross-check the reported optimum against a brute force written here,
    so the library's own loop is not the only thing that has looked."""
    thrs = (0.1, 0.25, 0.6)
    best = None
    for k in range(1, len(MARKERS) + 1):
        for sub in itertools.combinations(MARKERS, k):
            out = cf.classifier_output(PANEL_A, sub, SENSE)
            if out["HeLa"] <= 0.0:
                continue
            for t in thrs:
                c = cf.confusion(PANEL_A, sub, SENSE, "HeLa", t)
                if c.tp != 1:
                    continue
                key = (c.fp, k)
                if best is None or key < best[0]:
                    best = (key, sub, t)
    d = cf.design_to_budget(PANEL_A, SENSE, "HeLa", population=6.0,
                            budget=1.0, thresholds=thrs)
    assert d.found is True
    assert d.fp_lines == best[0][0]
    assert len(d.markers) == best[0][1]


# ------------------------------------------------------- the table itself --
def test_response_table_catches_the_transpose():
    with pytest.raises(ValueError, match="TRANSPOSE"):
        cf.response_table(np.zeros((5, 7)), LINES, MARKERS)
    with pytest.raises(ValueError, match="2-D"):
        cf.response_table([0.1, 0.2], ["A"], ["m"])
    with pytest.raises(ValueError, match="duplicate cell line"):
        cf.response_table(np.zeros((2, 1)), ["A", "A"], ["m"])
    with pytest.raises(ValueError, match="duplicate marker"):
        cf.response_table(np.zeros((1, 2)), ["A"], ["m", "m"])


def test_a_response_out_of_range_says_what_a_response_is():
    with pytest.raises(ValueError, match="NORMALIZED MARKER LEVEL"):
        cf.response_table([[1.0, 42.0]], ["A"], ["m1", "m2"])
    with pytest.raises(ValueError, match="NORMALIZED MARKER LEVEL"):
        cf.response_table([[-0.1, 0.5]], ["A"], ["m1", "m2"])


def test_a_hole_in_the_table_is_not_a_zero():
    panel = {"TARGET": {"A": 1.0}, "OTHER": {"A": 0.1, "B": 0.5}}
    with pytest.raises(ValueError, match="not a zero"):
        cf.classifier_output(panel, ["A", "B"], {"A": "high", "B": "high"})


def test_a_panel_without_negatives_is_refused_everywhere():
    only = {"HeLa": PANEL_A["HeLa"]}
    with pytest.raises(ValueError, match="at least one negative"):
        cf.confusion(only, MARKERS, SENSE, "HeLa", 0.2)
    with pytest.raises(ValueError, match="nothing to separate"):
        cf.sense_check(only, MARKERS, SENSE, "HeLa")
    with pytest.raises(ValueError, match="nothing to separate"):
        cf.convention_check(only, MARKERS, SENSE, "HeLa")
    with pytest.raises(ValueError, match="nothing to separate"):
        cf.marker_utility(only, MARKERS, SENSE, "HeLa")
    with pytest.raises(ValueError, match="negative lines to be wrong about"):
        cf.design_to_budget(only, SENSE, "HeLa", population=1e6)


def test_a_positive_line_outside_the_panel_is_refused():
    with pytest.raises(ValueError, match="not in the panel"):
        cf.confusion(PANEL_A, MARKERS, SENSE, "A549", 0.2)


def test_normalization_is_per_marker_and_panel_relative():
    raw = {"TARGET": {"A": 800.0, "B": 10.0},
           "N1": {"A": 400.0, "B": 100.0}}
    with pytest.raises(ValueError, match="NORMALIZED MARKER LEVEL"):
        cf.classifier_output(raw, ["A", "B"], {"A": "high", "B": "absent"})
    norm = cf.normalize_responses(raw)
    assert norm["TARGET"]["A"] == pytest.approx(1.0)
    assert norm["N1"]["A"] == pytest.approx(0.5)
    assert norm["TARGET"]["B"] == pytest.approx(0.1)
    assert norm["N1"]["B"] == pytest.approx(1.0)
    # and the warning in its docstring is a fact: an eighth line moves
    # every number in the column
    wider = dict(raw, N2={"A": 1600.0, "B": 50.0})
    again = cf.normalize_responses(wider)
    assert again["TARGET"]["A"] == pytest.approx(0.5)
    assert again["TARGET"]["A"] != norm["TARGET"]["A"]


def test_normalizing_a_marker_no_line_expresses_is_refused():
    with pytest.raises(ValueError, match="carries no information"):
        cf.normalize_responses({"A": {"m": 0.0}, "B": {"m": 0.0}})


def test_sensor_outputs_round_trip_to_marker_levels_and_back():
    """The data boundary, since Fig. 2D holds SENSOR responses.

    An oriented matrix -- every series already high in the target line --
    converted to marker levels and then run through the product must give
    back the classifier the orientation describes. Doing it without the
    conversion applies the three NOT terms twice, and panel A's exact zeros
    make that visible as an output of zero in the target cell.
    """
    oriented = [[(v if SENSE[m] == "high" else 1.0 - v)
                 for m, v in zip(MARKERS, (PANEL_A[ln][k] for k in MARKERS))]
                for ln in LINES]
    table = cf.marker_levels_from_sensor_outputs(oriented, LINES, MARKERS,
                                                 SENSE)
    for ln in LINES:
        for m in MARKERS:
            assert table[ln][m] == pytest.approx(PANEL_A[ln][m], abs=1e-15)
    got = cf.classifier_output(table, MARKERS, SENSE)
    for ln, want in OUT_A.items():
        assert got[ln] == pytest.approx(want, rel=1e-14, abs=1e-15)
    # and the un-converted matrix is the sign error, loudly
    wrong = cf.response_table(oriented, LINES, MARKERS)
    assert cf.classifier_output(wrong, MARKERS, SENSE)["HeLa"] == 0.0
    assert cf.sense_check(wrong, MARKERS, SENSE, "HeLa") != []


def test_the_conversion_is_its_own_inverse():
    rng = np.random.default_rng(99)
    raw = rng.random((5, 3))
    marks = ["a", "b", "c"]
    sense = {"a": "high", "b": "absent", "c": "absent"}
    lines = [f"L{i}" for i in range(5)]
    once = cf.marker_levels_from_sensor_outputs(raw, lines, marks, sense)
    twice = cf.marker_levels_from_sensor_outputs(
        [[once[ln][m] for m in marks] for ln in lines], lines, marks, sense)
    for i, ln in enumerate(lines):
        for j, m in enumerate(marks):
            assert twice[ln][m] == pytest.approx(raw[i, j], abs=1e-15)


def test_the_module_exports_what_it_documents():
    for name in cf.__all__:
        assert hasattr(cf, name), name
    assert cf.SENSES == ("high", "absent")


# --------------------------------------------------------------------------
# DIGITIZED panel -- Xie Fig. 2D, and the one block of real numbers in this
# file. It is here because the regression it locks cannot be reproduced by an
# invented panel: the old per-marker sense check fired on THIS matrix, in the
# correct convention, and on four of its five leave-one-out subsets. Values
# are copied from `sessions/s26-therapeutics/NUMBERS.md` sec 2.2 (DIGITIZED,
# 8 November 2026), which remains the source of truth -- if they disagree,
# NUMBERS is right and this fixture is stale.
#
# SENSOR OUTPUTS, rel. u., NOT marker levels (NUMBERS sec 2.1). The three
# NOT terms are already applied inside the sensors, so the convention that
# matches these numbers declares every sense "high".
# --------------------------------------------------------------------------
XIE_LINES = ["DAOY", "HEK293", "HeLa", "MCF-7", "SH-SY5Y", "SKBR3", "T47D"]
XIE_MARKERS = ["P21", "P17-30a", "T141", "T142-3p", "T146a"]
# Several bars exceed 1.0 rel. u., so this cannot go through
# `response_table` -- which is right, and is the reason NUMBERS calls the
# normalization a modelling choice: 1.0 means "the most of this marker seen
# in THESE seven lines".
#
# THE THREE-DECIMAL TABLE IS THE RIGHT SOURCE, AND THE REASON IS NOT
# CONVENIENCE. NUMBERS sec 2.1's printed products (HeLa 0.433555, T47D
# 0.293775, ratio 1.48x) come from the full-precision digitized page
# geometry. These values are sec 2.2's PUBLISHED table, rounded to three
# decimals, and multiplying them gives HeLa 0.433615, T47D 0.293949, ratio
# 1.4751x -- deltas of +0.00006 and +0.00017. Neither is wrong; they answer
# different questions. A student is handed sec 2.2's table, because that is
# what NUMBERS publishes, so a student who multiplies CORRECTLY gets
# 0.433615, and an autograder keyed to 0.433555 on a tight tolerance would
# fail every correct answer. The fixture therefore mirrors the published
# table, and `test_the_fixture_mirrors_numbers_section_2_2` keeps it a
# mirror rather than a fork.
#
# The normalization is NOT the source of that discrepancy and cannot be:
# `normalize_responses` divides each column by that column's maximum, so
# every line's product picks up the same factor 1/prod(column maxima) and
# the ratio between any two lines is unchanged -- exactly, in rational
# arithmetic, not approximately.
XIE_RAW = [[0.420, 0.429, 0.961, 0.697, 0.417],      # DAOY
           [0.010, 0.078, 1.106, 0.993, 1.230],      # HEK293
           [0.933, 0.717, 0.894, 0.849, 0.854],      # HeLa
           [0.931, 0.405, 0.106, 1.019, 1.033],      # MCF-7
           [0.090, 0.242, 1.072, 0.963, 1.063],      # SH-SY5Y
           [0.525, 0.755, 0.544, 0.817, 0.938],      # SKBR3
           [0.560, 0.690, 0.789, 0.994, 0.970]]      # T47D
XIE_FIG2D = cf.normalize_responses(
    {ln: dict(zip(XIE_MARKERS, row))
     for ln, row in zip(XIE_LINES, XIE_RAW)}, XIE_MARKERS)
# The convention these numbers are in: the NOTs are in the sensors already.
XIE_SENSE = {m: "high" for m in XIE_MARKERS}
# The error: the same bars fed in as marker levels, so p.1308's three NOT
# terms get applied a second time.
XIE_DOUBLY_INVERTED = {"P21": "high", "P17-30a": "high", "T141": "absent",
                       "T142-3p": "absent", "T146a": "absent"}


# ---- the fixture above MIRRORS NUMBERS sec 2.2, and this keeps it one ----
#
# The all-synthetic rule this file breaks for `XIE_FIG2D` exists to stop
# NUMBERS being silently forked. Two copies of a constant can drift, so the
# copy is checked against the original instead of trusted: this parses sec
# 2.2's "Values" table out of the markdown and compares it cell by cell.
# READ-ONLY. NUMBERS.md is the source of truth and nothing here writes to it.

#: The one name that differs between the markdown and the library. NUMBERS
#: prints the sensor as Xie does, `T142(3p)`; `(` and `)` in an identifier
#: are awkward in a dict key a student types, so the library spells it
#: `T142-3p`. Any OTHER difference in the header is drift and must fail.
_MD_MARKER_RENAMES = {"T142(3p)": "T142-3p"}

NUMBERS_MD = (pathlib.Path(__file__).resolve().parents[1]
              / "sessions" / "s26-therapeutics" / "NUMBERS.md")


def _parse_numbers_fig2d_values():
    """NUMBERS sec 2.2's 'Values' table as (markers, lines, rows of float).

    Anchored on the table's own bold caption rather than on a line number,
    so inserting a section above it does not silently read the SD table
    instead -- which would be a quiet disaster, since those numbers are the
    same shape.
    """
    if not NUMBERS_MD.exists():
        pytest.skip(f"{NUMBERS_MD} is not in this checkout")
    text = NUMBERS_MD.read_text(encoding="utf-8").splitlines()
    caption = "**Values. SENSOR OUTPUTS"
    heads = [i for i, ln in enumerate(text) if ln.startswith(caption)]
    assert len(heads) == 1, (
        f"expected exactly one {caption!r} caption in {NUMBERS_MD.name}, "
        f"found {len(heads)} at lines {[h + 1 for h in heads]}")
    grid = []
    for ln in text[heads[0] + 1:]:
        s = ln.strip()
        if not s.startswith("|"):
            if grid:
                break
            continue
        cells = [c.strip().strip("*").strip() for c in s.strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue                      # the |---|---| rule row
        grid.append(cells)
    assert len(grid) == 8, f"expected a header and 7 rows, parsed {len(grid)}"
    header = grid[0]
    assert header[0].lower() == "cell line", header
    markers = [_MD_MARKER_RENAMES.get(h, h) for h in header[1:]]
    lines = [r[0] for r in grid[1:]]
    rows = [[float(v) for v in r[1:]] for r in grid[1:]]
    assert all(len(r) == len(markers) for r in rows), rows
    return markers, lines, rows


def test_the_fixture_mirrors_numbers_section_2_2():
    """`XIE_FIG2D` is NUMBERS sec 2.2, not a second opinion about it.

    Markers, cell lines, order and all 35 values are compared exactly -- both
    sides are three-decimal literals, so exact equality is the right test and
    a tolerance would hide precisely the drift this guards against. If this
    test fails, NUMBERS is right and the fixture is stale.
    """
    markers, lines, rows = _parse_numbers_fig2d_values()
    assert markers == XIE_MARKERS, (markers, XIE_MARKERS)
    assert lines == XIE_LINES, (lines, XIE_LINES)
    assert rows == XIE_RAW, (rows, XIE_RAW)
    # and the derived, normalized fixture follows from the markdown too
    mirror = cf.normalize_responses(
        {ln: dict(zip(markers, row)) for ln, row in zip(lines, rows)}, markers)
    for ln in XIE_LINES:
        for m in XIE_MARKERS:
            assert XIE_FIG2D[ln][m] == mirror[ln][m], (ln, m)


def test_the_published_table_is_not_the_published_product():
    """Sec 2.1's products come from the geometry, sec 2.2's table from the
    rounded page. They differ, both are right, and the autograder has to know
    which one a student was handed.

    Multiplying sec 2.2's three-decimal table gives HeLa 0.433615 against
    sec 2.1's printed 0.433555. A student handed the table and multiplying
    correctly produces the former, so this locks the table's own answer --
    and locks the fact that the gap is NOT the normalization, which multiplies
    every line by the same constant and cannot move a ratio.
    """
    _markers, lines, rows = _parse_numbers_fig2d_values()
    raw = {ln: dict(zip(XIE_MARKERS, row)) for ln, row in zip(lines, rows)}
    bare = {}
    for ln, row in raw.items():
        p = 1.0
        for m in XIE_MARKERS:
            p *= row[m]
        bare[ln] = p
    order = sorted(bare, key=bare.get, reverse=True)
    assert order[0] == "HeLa" and order[1] == "T47D"
    assert bare["HeLa"] == pytest.approx(0.433615, abs=5e-7)
    assert bare["T47D"] == pytest.approx(0.293949, abs=5e-7)
    table_ratio = bare["HeLa"] / bare["T47D"]
    assert table_ratio == pytest.approx(1.4751346, abs=1e-6)
    # sec 2.1's geometry products are a different, also-correct number
    assert bare["HeLa"] - 0.433555 == pytest.approx(6.0e-5, abs=1e-6)
    assert bare["T47D"] - 0.293775 == pytest.approx(1.74e-4, abs=1e-6)
    # the normalized table gives the SAME ratio, to floating-point noise
    normalized = cf.classifier_output(XIE_FIG2D, XIE_MARKERS, XIE_SENSE)
    assert (normalized["HeLa"] / normalized["T47D"]
            == pytest.approx(table_ratio, rel=1e-12))
    assert cf.convention_check(XIE_FIG2D, XIE_MARKERS, XIE_SENSE,
                               "HeLa").margin == pytest.approx(table_ratio,
                                                               rel=1e-12)


def test_the_right_fig2d_convention_raises_no_warning_at_all():
    """NUMBERS sec 2.1's decisive test, as a regression.

    These are the published bars in the published convention with the right
    senses, and HeLa is the argmax. Nothing may be said about them -- the old
    check said T142(3p) proved the NOT terms had been applied twice.
    """
    assert cf.sense_check(XIE_FIG2D, XIE_MARKERS, XIE_SENSE, "HeLa") == []
    got = cf.convention_check(XIE_FIG2D, XIE_MARKERS, XIE_SENSE, "HeLa")
    assert got.ok is True
    assert got.message is None
    assert got.alternative is None
    assert got.declared_top == ("HeLa",)
    # 1.4751x, from sec 2.2's published three-decimal table. Sec 2.1 prints
    # 1.48x from the full-precision geometry; see the fixture's comment for
    # why those differ and why it is not the normalization.
    assert got.margin == pytest.approx(1.4751, abs=0.0002)
    out = cf.classifier_output(XIE_FIG2D, XIE_MARKERS, XIE_SENSE)
    assert max(out, key=out.get) == "HeLa"


def test_the_fig2d_bars_read_as_marker_levels_are_caught_and_named():
    """The double inversion NUMBERS sec 2.1 exists to prevent.

    Declaring the three T-sensors 'absent' applies p.1308's NOT terms a
    second time; the paper's own check then picks SKBR3, with HeLa second.
    """
    out = cf.classifier_output(XIE_FIG2D, XIE_MARKERS, XIE_DOUBLY_INVERTED)
    order = sorted(out, key=out.get, reverse=True)
    assert order[0] == "SKBR3" and order[1] == "HeLa", order
    got = cf.convention_check(XIE_FIG2D, XIE_MARKERS, XIE_DOUBLY_INVERTED,
                              "HeLa")
    assert got.ok is False
    assert got.alternative == "sensor-output"
    assert got.margin < 1.0 < got.alternative_margin
    assert "SENSOR OUTPUTS" in got.message
    assert "marker_levels_from_sensor_outputs" in got.message
    for m in ("T141", "T142-3p", "T146a"):
        assert m in got.message, m
    said = cf.sense_check(XIE_FIG2D, XIE_MARKERS, XIE_DOUBLY_INVERTED, "HeLa")
    assert got.message in said


def test_the_sensor_output_hypothesis_is_not_a_global_inversion():
    """Why the convention test is not just "try flipping everything".

    A global flip of all five senses does NOT recover HeLa from the double
    inversion -- it puts HEK293 on top and HeLa sixth -- so a check built
    only on global inversion would be silent on exactly the error this
    module exists to catch. Both hypotheses are needed, and this locks the
    reason.
    """
    flipped = {m: ("absent" if s == "high" else "high")
               for m, s in XIE_DOUBLY_INVERTED.items()}
    out = cf.classifier_output(XIE_FIG2D, XIE_MARKERS, flipped)
    order = sorted(out, key=out.get, reverse=True)
    assert order[0] == "HEK293"
    assert order.index("HeLa") == 5
    # and the hypothesis that does recover it is the sensor-output one
    assert cf.convention_check(XIE_FIG2D, XIE_MARKERS, XIE_DOUBLY_INVERTED,
                               "HeLa").alternative == "sensor-output"


def test_the_named_remedy_actually_works():
    """The message tells the reader to convert at the boundary. Do that."""
    levels = cf.marker_levels_from_sensor_outputs(
        [[XIE_FIG2D[ln][m] for m in XIE_MARKERS] for ln in XIE_LINES],
        XIE_LINES, XIE_MARKERS, XIE_DOUBLY_INVERTED)
    fixed = cf.convention_check(levels, XIE_MARKERS, XIE_DOUBLY_INVERTED,
                                "HeLa")
    assert fixed.ok is True
    assert fixed.margin == pytest.approx(
        cf.convention_check(XIE_FIG2D, XIE_MARKERS, XIE_SENSE,
                            "HeLa").margin, rel=1e-12)


def test_no_leave_one_out_subset_blames_the_convention():
    """The old check's worst property, locked out.

    Dropping each marker in turn from the correct configuration, the old
    per-marker check produced a convention complaint on four of the five
    subsets. No subset may produce one now. Dropping P21 does lose HeLa the
    panel maximum -- that is true, and it is reported as a fact about the
    marker set, with `alternative` None, not as a convention diagnosis.
    """
    for drop in XIE_MARKERS:
        rest = [m for m in XIE_MARKERS if m != drop]
        got = cf.convention_check(XIE_FIG2D, rest,
                                  {m: "high" for m in rest}, "HeLa")
        assert got.alternative is None, (drop, got.message)
        if drop == "P21":
            assert got.ok is False
            assert "not a diagnosis of the convention" in got.message
            assert cf.sense_check(XIE_FIG2D, rest,
                                  {m: "high" for m in rest}, "HeLa") != []
        else:
            assert got.ok is True, (drop, got.message)
            assert cf.sense_check(XIE_FIG2D, rest,
                                  {m: "high" for m in rest}, "HeLa") == []


def test_marker_utility_reports_the_panel_and_complains_about_nothing():
    """The split, in one assertion pair.

    On the correct configuration `sense_check` is empty and `marker_utility`
    still has four markers to describe -- which is the whole point: the
    positive line not being a marker's top reader is an ordinary fact about
    a correct panel, so it cannot live in a list whose emptiness means
    "consistent".
    """
    assert cf.sense_check(XIE_FIG2D, XIE_MARKERS, XIE_SENSE, "HeLa") == []
    rows = cf.marker_utility(XIE_FIG2D, XIE_MARKERS, XIE_SENSE, "HeLa")
    assert [r.marker for r in rows] == XIE_MARKERS
    assert sum(1 for r in rows if r.note is not None) == 4
    # P21 is the one marker HeLa reads highest, and it says nothing
    p21 = next(r for r in rows if r.marker == "P21")
    assert p21.top_reader is True
    assert p21.note is None
    assert p21.deficit > 0.0


def test_marker_utility_picks_the_margin_costly_marker_and_blames_nothing():
    """T142(3p) is genuinely the most margin-costly of the five -- dropping it
    takes the margin from 1.475x to 1.727x, more than any other marker -- so
    the old check named the right marker for the wrong reason. The reason is
    now a leave-one-out number, and the note asserts no cause.
    """
    rows = cf.marker_utility(XIE_FIG2D, XIE_MARKERS, XIE_SENSE, "HeLa")
    worst = max(rows, key=lambda r: r.margin_without)
    assert worst.marker == "T142-3p"
    assert worst.panel_margin == pytest.approx(1.475, abs=0.002)
    assert worst.margin_without == pytest.approx(1.727, abs=0.002)
    assert worst.best_negative == "MCF-7"
    assert worst.deficit == pytest.approx(-0.1668, abs=0.002)
    note = worst.note
    assert "MCF-7" in note and "1.727" in note
    # no causal claim, and no advice to drop the marker
    for forbidden in ("twice", "SENSOR responses", "NOT term", "double"):
        assert forbidden not in note, forbidden
    assert "not a convention diagnosis" in note
    assert "not a reason to drop the marker" in note
    assert "may be to exclude cell types the panel does not contain" in note


def test_marker_utility_leaves_one_out_against_hand_arithmetic():
    """The leave-one-out margin is the ratio it claims to be, on panel A."""
    rows = cf.marker_utility(PANEL_A, MARKERS, SENSE, "HeLa")
    for r in rows:
        rest = [m for m in MARKERS if m != r.marker]
        sub = cf.classifier_output(PANEL_A, rest,
                                   {m: SENSE[m] for m in rest})
        best = max(sub[ln] for ln in LINES if ln != "HeLa")
        assert r.margin_without == pytest.approx(sub["HeLa"] / best, rel=1e-12)
        assert r.panel_margin == pytest.approx(1.0 / 0.5, rel=1e-12)


def test_a_single_marker_has_no_leave_one_out_margin():
    """A product over nothing is refused, so the margin without the only
    marker does not exist and is None rather than an invented number."""
    panel = cf.response_table([[1.0], [0.2]], ["TARGET", "OTHER"], ["A"])
    only = cf.marker_utility(panel, ["A"], {"A": "high"}, "TARGET")
    assert len(only) == 1
    assert only[0].margin_without is None
    assert only[0].top_reader is True


def test_a_tie_at_the_top_is_not_a_win():
    """With exact zeros an inverted circuit products to 0.0 in EVERY line, so
    the positive is the argmax of a seven-way tie. That is the sign error,
    not the absence of one, and the check must not read it as a pass."""
    out = cf.classifier_output(PANEL_A, MARKERS, INVERTED)
    assert set(out.values()) == {0.0}
    got = cf.convention_check(PANEL_A, MARKERS, INVERTED, "HeLa")
    assert got.ok is False
    assert len(got.declared_top) == len(LINES)
    assert "only TIES" in got.message
    assert got.alternative == "global-polarity"


def test_the_convention_check_object_is_not_a_boolean():
    """`Design`'s lesson. An object that means "something is wrong" must not
    be falsy, or `if convention_check(...)` un-catches the error."""
    bad = cf.convention_check(XIE_FIG2D, XIE_MARKERS, XIE_DOUBLY_INVERTED,
                              "HeLa")
    assert bool(bad) is True
    assert bad.ok is False
    assert set(bad.as_dict()) == set(cf.ConventionCheck._FIELDS)
    with pytest.raises(TypeError, match="missing"):
        cf.ConventionCheck(ok=True)
    with pytest.raises(TypeError, match="unexpected"):
        cf.ConventionCheck(**dict(bad.as_dict(), nonsense=1))
    row = cf.marker_utility(XIE_FIG2D, XIE_MARKERS, XIE_SENSE, "HeLa")[0]
    assert set(row.as_dict()) == set(cf.MarkerUtility._FIELDS)
    with pytest.raises(TypeError, match="missing"):
        cf.MarkerUtility(marker="P21")
