"""
posb.assembly — Golden Gate junctions: counting, distinguishability, fidelity.

Introduced in Session 17. You do the counting and the overhang design by hand
on paper in class first; this is the same arithmetic made reusable, and it is
what PS7 asks you to call.

A Type IIS enzyme recognises one sequence and cuts at a fixed offset OUTSIDE
it, so the recognition site leaves with the scrap and the four bases left in
the join are bases the designer picked. Two consequences run through
everything below.

  * A 4-nt overhang anneals to its reverse complement, so an overhang and its
    complement are ONE junction identity, not two. A palindromic overhang is
    its own complement: it ligates to a copy of itself and the fragment can go
    in either way round, so it is unusable. 256 overhangs, 16 palindromic,
    (256 - 16) / 2 = 120 usable identities.

  * 120 is not the binding constraint. Junctions fail by being ALIKE, not by
    running out, and similarity has to be measured against the reverse
    complement too.

`clash_probability` is a deliberately crude proxy -- a Hamming-distance rule,
not ligation chemistry. `STANDARD_SETS` carries the published set and the
PREDICTED fidelities for it, and the gap between the two is the session's
point. Mind the chronology, which is easy to get backwards: the standard was
REASONED first (Patron et al. 2015) and PRICED later (Potapov's exhaustive
measurement 2018, Pryor's predictions 2020). The measurement then found a bad
pair the committee's own criteria had missed.
"""

from functools import lru_cache
from itertools import product
import random

BASES = "ACGT"
_COMP = {"A": "T", "C": "G", "G": "C", "T": "A"}

# The plant common syntax / Phytobrick fusion sites -- ONE set, used throughout
# session 17. AATG is in it. Its last THREE bases are the start codon; the
# leading A is a real choice, at the -1 position of the 5'UTR, made from four
# candidates (AATG/CATG/GATG/TATG). So fixing it makes that junction CONSTANT
# across every construct, not harmless -- an earlier draft said the scar "adds
# nothing", which is false by exactly one base, and that base sits inside the
# +/-30 window around the start codon that Cambray 2018 reports as carrying 83%
# of the design properties' total effect.
#
# The numbers are PREDICTED, not assayed. NEB publishes a "93%" for the nine
# overhang MoClo Level 1 set and labels it predicted fidelity, with no enzyme or
# reaction conditions given; an earlier version of this module recorded it as
# measured and the session called it "the assay", which was wrong twice over --
# it is a prediction, and it is for a different set than the one the AATG claim
# comes from. Both numbers below are from a primary source that says what they
# are:
#
#   Pryor JM et al. (2020) "Enabling one-pot Golden Gate assemblies of
#   unprecedented complexity using data-optimized assembly design." PLOS ONE.
#   DOI 10.1371/journal.pone.0238592.
#
# They report this set as 81% predicted error-free, rising to about 92% if the
# GGTA/TACT mispair is avoided, and name that mispair as the dominant source of
# expected assembly error. Pryor does not define the counterfactual (whether an
# overhang was dropped or replaced), and the prediction assumes BsmBI-v2 with
# 42C/16C cycling while this is a BsaI standard -- so quote it as "about 92%",
# not as a price.
#
# CHRONOLOGY, and it is the opposite of the obvious guess. The set was REASONED:
# Patron et al. 2015 chose fusion sites to be unique and non-palindromic, with
# in-CDS sites picked for the amino acids they encode, and report no ligation
# measurement. Potapov's exhaustive profiling of all 256 overhangs is 2018
# (DOI 10.1021/acssynbio.8b00333); Pryor's predictions are 2020. The standard
# predates its own pricing by three to five years -- and the pricing found a
# mispair the committee's criteria had missed. That is the session's point: a
# standard is manufactured by people reasoning carefully, who still ship a bad
# pair, and only exhaustive measurement says what it cost.
STANDARD_SETS = {
    "common_syntax": {
        "overhangs": ["GGAG", "TGAC", "TCCC", "TACT", "CCAT", "AATG",
                      "AGCC", "TTCG", "GCTT", "GGTA", "CGCT"],
        "predicted_fidelity": 0.81,
        "predicted_without_worst_pair": 0.92,
        "worst_pair": ("GGTA", "TACT"),
        "cds_fusion_site": "AATG",
        "source": "Pryor et al. 2020, 10.1371/journal.pone.0238592",
    },
}



def revcomp(seq):
    """Reverse complement of an uppercase ACGT string."""
    return "".join(_COMP[b] for b in reversed(seq))


def is_palindromic(overhang):
    """True if the overhang is its own reverse complement, so it self-ligates."""
    return overhang == revcomp(overhang)


@lru_cache(maxsize=None)
def junction_identities(n=4):
    """(all overhangs, palindromic ones, usable identities) for length n.

    An overhang and its reverse complement are merged into one identity, and
    palindromes are dropped. For n = 4 this is (256, 16, 120).
    """
    all_o = ["".join(p) for p in product(BASES, repeat=n)]
    palindromic = [o for o in all_o if is_palindromic(o)]
    seen, classes = set(), []
    for o in all_o:
        if o in palindromic or o in seen:
            continue
        seen.add(o)
        seen.add(revcomp(o))
        classes.append(o)
    return all_o, palindromic, classes


def distance(a, b):
    """Mismatches between two overhangs, measured against b AND revcomp(b).

    Ligation does not care which strand you wrote down, so an overhang one
    base from another's complement is just as dangerous as one base from the
    other itself. Forgetting the second term is the usual way a hand-picked
    set turns out not to be distinguishable.
    """
    if len(a) != len(b):
        raise ValueError(f"overhangs must be the same length: {a!r}, {b!r}")
    return min(sum(x != y for x, y in zip(a, b)),
               sum(x != y for x, y in zip(a, revcomp(b))))


def clash_probability(k, trials=4000, seed=17, min_distance=2):
    """P(some pair among k randomly chosen junctions is too close).

    A crude proxy for misligation: a pair clashes when `distance` puts it
    below `min_distance`. Real fidelity is measured pair by pair (Potapov
    2018) and then predicted for a whole set (Pryor 2020); this rule does
    neither. Sampling is seeded so the curve is reproducible.
    """
    _all, _pal, classes = junction_identities()
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        pick = rng.sample(classes, k)
        bad = False
        for i in range(k):
            for j in range(i + 1, k):
                if distance(pick[i], pick[j]) < min_distance:
                    bad = True
                    break
            if bad:
                break
        hits += bad
    return hits / trials
