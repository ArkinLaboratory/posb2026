"""posb.assembly — the Session 17 / PS7 Golden Gate arithmetic.

These lock the numbers that appear on slides and in the handout. If one of
them fails, a claim students are being taught has changed.
"""
import pytest

from posb.assembly import (BASES, STANDARD_SETS, clash_probability, distance,
                           is_palindromic, junction_identities, revcomp)


def test_revcomp_is_an_involution():
    for o in ("AATG", "GGAG", "TACT", "ACGT"):
        assert revcomp(revcomp(o)) == o


def test_palindromic_means_self_complementary():
    all_o, pal, _ = junction_identities()
    assert set(pal) == {o for o in all_o if o == revcomp(o)}


def test_the_counting_on_the_slide():
    """256 overhangs, 16 palindromic, 120 usable identities."""
    all_o, pal, classes = junction_identities()
    assert (len(all_o), len(pal), len(classes)) == (256, 16, 120)
    assert len(classes) == (len(all_o) - len(pal)) // 2


def test_no_identity_is_the_complement_of_another():
    _a, _p, classes = junction_identities()
    s = set(classes)
    assert not any(revcomp(o) in s for o in classes)


def test_distance_sees_the_reverse_complement():
    """TACT and GGTA differ at all four bases, yet are one base apart.

    revcomp(GGTA) is TACC. Scoring only the direct comparison is how a
    hand-picked set turns out not to be distinguishable.
    """
    assert sum(a != b for a, b in zip("TACT", "GGTA")) == 4
    assert distance("TACT", "GGTA") == 1


def test_distance_is_symmetric():
    _a, _p, classes = junction_identities()
    for x, y in zip(classes[:40], classes[40:80]):
        assert distance(x, y) == distance(y, x)


def test_published_set_carries_no_palindromes():
    s = STANDARD_SETS["common_syntax"]["overhangs"]
    assert not [o for o in s if is_palindromic(o)]
    assert len(set(s)) == len(s)


def test_the_standard_cds_fusion_site_contains_the_start_codon():
    """AATG is the common-syntax CDS fusion site; its last THREE bases are ATG.

    Only three of the four were determined by the biology. The leading A is a
    real choice from four candidates, and it sits at -1 in the 5'UTR, inside
    the window Cambray 2018 reports as carrying most of the design properties'
    effect. So the standard makes this junction CONSTANT, not harmless -- an
    earlier docstring here said "the scar cannot do harm", which overclaims by
    exactly one base and the answer key used to penalise students who saw it.
    """
    d = STANDARD_SETS["common_syntax"]
    assert d["cds_fusion_site"] == "AATG"
    assert d["cds_fusion_site"] in d["overhangs"]
    assert d["cds_fusion_site"].endswith("ATG")


def test_the_rule_is_a_screen_not_an_answer():
    """The lesson, pinned.

    Students derive 'every pair at least two bases apart, checked against the
    reverse complement'. Over the published set that rule flags THREE pairs of
    55. Pryor et al. measured all 256 overhangs and found one of those three,
    GGTA/TACT, carries most of the expected error: 81% predicted error-free
    for the set, 92% if that pair is avoided.

    So the rule narrows the field and cannot rank it. If this ever stops being
    true, three slides, a handout item and the board notes are wrong.
    """
    d = STANDARD_SETS["common_syntax"]
    s = d["overhangs"]
    flagged = [tuple(sorted((x, y))) for i, x in enumerate(s) for y in s[i + 1:]
               if distance(x, y) < 2]
    assert len(flagged) == 3, flagged
    assert tuple(sorted(d["worst_pair"])) in flagged
    assert d["predicted_fidelity"] < d["predicted_without_worst_pair"]


def test_the_worst_pair_is_invisible_without_the_reverse_complement():
    """GGTA and TACT differ at all four bases compared directly.

    Scoring only the direct comparison passes the pair that Pryor et al. say
    causes most of the error. This is the trap the board notes spring.
    """
    a, b = "GGTA", "TACT"
    assert sum(x != y for x, y in zip(a, b)) == 4
    assert distance(a, b) == 1


def test_clash_probability_is_seeded_and_rises_with_k():
    assert clash_probability(4) == clash_probability(4)
    ps = [clash_probability(k, trials=800) for k in (2, 5, 10, 15)]
    assert ps == sorted(ps)
    assert ps[0] < 0.3 < ps[-1]


def test_clash_probability_crosses_even_odds_between_four_and_five():
    """The figure interpolates the crossing to 4.2 junctions."""
    assert clash_probability(4) < 0.5 <= clash_probability(5)


@pytest.mark.parametrize("bad", ["AAA", "AAAAA"])
def test_distance_rejects_ragged_input(bad):
    """zip() truncates silently, so distance used to score ragged pairs.

    distance("AATG", "AAA") returned 1 and distance("AATG", "AAAAA")
    returned 2 -- both meaningless. The old version of this test passed only
    because its own assert raised, not because the module did.
    """
    with pytest.raises(ValueError):
        distance("AATG", bad)


def test_the_rule_does_point_at_the_culprit():
    """GGTA is in two of the three flagged pairs, and is the one that matters.

    Three documents used to tell the grader that the rule "cannot rank its
    three suspects". It can: GGTA is the hub, appearing in TCCC/GGTA and
    TACT/GGTA, and GGTA is exactly the overhang Pryor et al. name as the
    dominant error source. A student who says so is right.
    """
    from collections import Counter
    d = STANDARD_SETS["common_syntax"]
    s = d["overhangs"]
    flagged = [(x, y) for i, x in enumerate(s) for y in s[i + 1:]
               if distance(x, y) < 2]
    hub, n = Counter(o for p in flagged for o in p).most_common(1)[0]
    assert n == 2 and hub in d["worst_pair"]


def test_every_flagged_pair_needs_the_reverse_complement():
    """Skipping the reversal hides the whole flagged list, not just one pair.

    Direct Hamming for the three flagged pairs is 4, 4 and 2 -- all pass a
    two-base rule. Only against the reverse complement do they score 1.
    """
    d = STANDARD_SETS["common_syntax"]["overhangs"]
    flagged = [(x, y) for i, x in enumerate(d) for y in d[i + 1:]
               if distance(x, y) < 2]
    assert flagged
    for x, y in flagged:
        assert sum(a != b for a, b in zip(x, y)) >= 2, (x, y)
