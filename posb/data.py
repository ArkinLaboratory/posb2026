"""posb.data — Session 5. Synthetic measurements, generated deterministically.

Design rule for this module: **the data are fake and say so.** These are not
Andersen's raw traces; they are drawn from the model the session derives, using
Andersen's published half-lives as the parameters, with reproducible noise on
top. A student who fits them recovers the number the lecture claimed, which is
the point -- the exercise is the fitting and the interpretation, not a pretence
of laboratory provenance.

Everything is seeded, so the notebook a student runs, the copy the reader marks
and the run inside the autograder all see identical arrays. A problem set whose
data change between runs cannot be autograded.

Andersen, J. B. et al., Appl. Environ. Microbiol. 64(6), 2240-2246 (1998),
Fig. 3A: degradation half-lives after a medium downshift, in minutes.
"""
import zlib

import numpy as np

# Degradation half-lives (min). np.inf = no measurable degradation, which is
# the truthful statement and needs no special case: ln2/inf is 0.0.
ANDERSEN_TAGS = {
    "none": np.inf,
    "ASV": 110.0,
    "AAV": 60.0,
    "LVA": 40.0,
    "LAA": 40.0,
}

DEFAULT_DOUBLING_MIN = 30.0     # E. coli, rich medium, the course's standard host


def _seed(*parts):
    """A stable seed from strings.

    NOT `hash()`: Python randomises string hashing per process unless
    PYTHONHASHSEED is set, so `hash()` would have given the student, the reader
    and the autograder three different datasets for the same call. crc32 is
    stable across processes, machines and versions, which is the only property
    needed here.
    """
    return zlib.crc32("|".join(str(p) for p in parts).encode()) & 0xFFFFFFFF


def removal_rate(tag="LAA", doubling_min=DEFAULT_DOUBLING_MIN, growing=True):
    """gamma + mu for a tag, per minute. `growing=False` gives gamma alone."""
    if tag not in ANDERSEN_TAGS:
        raise KeyError(f"unknown tag {tag!r}; have {sorted(ANDERSEN_TAGS)}")
    gamma = np.log(2.0) / ANDERSEN_TAGS[tag]
    mu = np.log(2.0) / doubling_min if growing else 0.0
    return gamma + mu


def decay_timecourse(tag="LAA", doubling_min=DEFAULT_DOUBLING_MIN,
                     growing=True, n=40, t_max=None, noise=0.04, seed=None):
    """A translation-shutoff experiment: production stops at t=0, signal decays.

    Returns (t_min, fluorescence). Fluorescence is arbitrary units starting near
    100. Noise is multiplicative and lognormal, because a fluorescence
    measurement is a ratio and its error is proportional, not additive -- which
    is also why the semi-log fit the problem set asks for is the right one.

    IN GROWING CELLS the observed rate is gamma + mu. That is the whole point of
    PS2 Q3b, so the default here is `growing=True` and the docstring does not
    give it away any harder than this.
    """
    k = removal_rate(tag, doubling_min, growing)
    if k <= 0:
        raise ValueError(f"tag {tag!r} in non-growing cells has no decay to fit")
    if t_max is None:
        t_max = 3.0 * np.log(2.0) / k          # about three half-lives
    # Seeded per tag so every consumer sees the same arrays.
    rng = np.random.default_rng(
        seed if seed is not None else _seed("decay", tag, growing, n))
    t = np.linspace(0.0, t_max, n)
    y = 100.0 * np.exp(-k * t) * np.exp(rng.normal(0.0, noise, size=n))
    return t, y


def response_timecourse(tag="LAA", doubling_min=DEFAULT_DOUBLING_MIN,
                        alpha=2.0, n=40, t_max=None, noise=0.04, seed=None):
    """Induction from an empty cell: p(t) = (alpha/k)(1 - exp(-k t)), plus noise."""
    k = removal_rate(tag, doubling_min, growing=True)
    if t_max is None:
        t_max = 4.0 * np.log(2.0) / k
    rng = np.random.default_rng(
        seed if seed is not None else _seed("response", tag, n))
    t = np.linspace(0.0, t_max, n)
    p = (alpha / k) * (1.0 - np.exp(-k * t))
    return t, p * np.exp(rng.normal(0.0, noise, size=n))
