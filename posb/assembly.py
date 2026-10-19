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
not ligation chemistry. Real fidelity is measured. The published standard sets
in `STANDARD_SETS` carry the measured numbers, and the gap between them and
the toy is the point: those sets were designed and assayed, not sampled.
"""

from functools import lru_cache
from itertools import product
import random

BASES = "ACGT"
_COMP = {"A": "T", "C": "G", "G": "C", "T": "A"}

# The common-syntax / MoClo fusion sites, with NEB's measured fidelity for the
# set as a whole. These are the PLANT common syntax (Patron et al. 2015 and
# the Phytobrick standard); the principle is general, the particular set is
# not universal. AATG is the fusion site at the 5' end of a coding sequence --
# its last three bases ARE the start codon, which is how the standard puts a
# junction where the sequence was already determined and so cannot do harm.
STANDARD_SETS = {
    "moclo_L1": {
        "overhangs": ["GGAG", "TACT", "CCAT", "AATG", "AGGT",
                      "TTCG", "GCTT", "GGTA", "CGCT"],
        "fidelity": 0.93,
        "note": "transcriptional units; AATG is the CDS start fusion site",
    },
    "moclo_L2": {
        "overhangs": ["TGCC", "GCAA", "ACTA", "TTAC", "CAGA",
                      "TGTG", "GAGC", "GGGA"],
        "fidelity": 0.95,
        "note": "multigene constructs",
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
    return min(sum(x != y for x, y in zip(a, b)),
               sum(x != y for x, y in zip(a, revcomp(b))))


def clash_probability(k, trials=4000, seed=17, min_distance=2):
    """P(some pair among k randomly chosen junctions is too close).

    A crude proxy for misligation: a pair clashes when `distance` puts it
    below `min_distance`. Real fidelity is measured, not derived -- see
    STANDARD_SETS. Sampling is seeded so the curve is reproducible.
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
