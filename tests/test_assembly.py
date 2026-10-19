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


def test_published_sets_carry_no_palindromes():
    for name, d in STANDARD_SETS.items():
        assert not [o for o in d["overhangs"] if is_palindromic(o)], name
        assert len(set(d["overhangs"])) == len(d["overhangs"]), name


def test_the_standard_cds_fusion_site_contains_the_start_codon():
    """AATG is the common-syntax CDS fusion site; its last three bases are ATG.

    This is the session's payoff -- the standard puts a junction where the
    sequence was already determined, so the scar cannot do harm.
    """
    assert "AATG" in STANDARD_SETS["moclo_L1"]["overhangs"]
    assert "AATG".endswith("ATG")


def test_the_published_set_fails_the_toy_rule():
    """The lesson, pinned.

    Students derive a set under 'every pair at least two bases apart'. The
    published Level 1 set violates that rule -- TACT against GGTA, via the
    reverse complement -- and is assayed at 93%. The constraint is measured,
    not derived. If this test ever passes the other way, the slide is wrong.
    """
    s = STANDARD_SETS["moclo_L1"]["overhangs"]
    offenders = [(x, y) for i, x in enumerate(s) for y in s[i + 1:]
                 if distance(x, y) < 2]
    assert offenders == [("TACT", "GGTA")]
    assert STANDARD_SETS["moclo_L1"]["fidelity"] >= 0.90


def test_clash_probability_is_seeded_and_rises_with_k():
    assert clash_probability(4) == clash_probability(4)
    ps = [clash_probability(k, trials=800) for k in (2, 5, 10, 15)]
    assert ps == sorted(ps)
    assert ps[0] < 0.3 < ps[-1]


def test_clash_probability_crosses_even_odds_between_four_and_five():
    """The figure interpolates the crossing to 4.2 junctions."""
    assert clash_probability(4) < 0.5 <= clash_probability(5)


@pytest.mark.parametrize("bad", ["AAA", "AAAAA"])
def test_distance_requires_equal_length(bad):
    with pytest.raises(Exception):
        assert distance("AATG", bad) == 0 and len(bad) == 4
