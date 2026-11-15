"""Design at population scale -- session 25's object, PS9's T67 and T73.

THE CHANGE OF OBJECT, AND IT IS A SECOND ONE. Session 23 moved the state
variable from a concentration inside one cell to a FRACTION OF A POPULATION.
This module moves what is being designed. The artifact here is an infectious
agent, not a circuit inside a host you own, so the specification stops being a
transfer function or a settling time and becomes a REPRODUCTIVE RATIO GREATER
THAN ONE. Everything below is either a composition probability or a count of
secondary infections. Nothing in this module is a concentration.

THE PAPER. Weinberger, Schaffer & Arkin, J. Virol. 77(18):10028-10036 (2003),
called W03 throughout. A conditionally replicating HIV-1 vector (crHIV-1)
carries an antiviral payload, cannot replicate on its own, and borrows every
protein it needs from wild-type HIV-1 in the same cell. Two engineering knobs:

    P  the PACKAGING ADVANTAGE. The cytoplasmic crHIV-1 : HIV-1 mRNA ratio in
       a dually infected cell is P : 1, by definition of P. Intracellular, and
       therefore not measurable in vivo. Swept 1 to 100.

       ALWAYS WRITE THE ORDER. This is the same ratio the figures and
       NUMBERS.md write as 1 : P, because they order it HIV-1 : crHIV-1.
       Both are correct and they are not a contradiction. Read either one
       the wrong way round and q becomes 1/(1+P) instead of P/(1+P), which
       inverts every genotype probability in the session -- so no docstring,
       figure or slide here states this ratio without naming which species
       comes first.
    D  the ANTIVIRAL EFFECT, and its sense reads backwards from its name.
       W03's prose calls D "the fraction by which the HIV-1 titer is
       therapeutically downregulated", but equation [3] MULTIPLIES the viral
       production term by D, so D IS THE FRACTION REMAINING: D = 1 is no
       inhibition at all and D = 0 is total inhibition. W03 says so itself at
       p.4 ("if no therapeutic gene is encoded ... D = 1 ... there is no
       reduction") and in the Fig. 3b caption ("D ~ 0.4, i.e. downregulation
       is ~60% effective"). Any problem statement using D must spell out which
       end is the good drug rather than reuse the paper's wording.

TWO DRAWS FROM AN URN. Retroviruses are diploid: two single strands of mRNA go
into one capsid. If every RNA pair is equally likely to be packaged, a capsid
in a dually infected cell is two independent draws from a pool holding
crHIV-1 and HIV-1 at P : 1, so with q = P/(1+P) the probability a drawn
transcript is vector,

    HIV-1 homozygote   (1-q)^2  =  1   / (1+P)^2
    heterozygote       2q(1-q)  =  2P  / (1+P)^2
    crHIV-1 homozygote  q^2     =  P^2 / (1+P)^2

and those three sum to one. W03 prints the same thing as the ratio 1 : 2P : P^2
with the denominator dropped. THE TWO FORMS DIFFER BY (1+P)^2 AND THAT IS HOW
THIS CALCULATION IS GOT WRONG, which is why `diploid_packaging` takes a
`normalized` flag and no default is silent about it.

WHAT THE BINOMIAL RESTS ON, SINCE NOTHING TESTS IT. A binomial needs equal
packaging probability and independent draws. W03 asserts the first in one
clause and the second not at all, and no experiment in the assigned papers
measures either. The calculation is still the right one for WHICH genotype a
virion is; see `burst_output` for the place where it is used for a quantity it
cannot settle.

THE STRIKE-OUT. An et al. (J. Virol. 73:7671, 1999) report that heterozygous
lentiviral virions fuse and enter but meet a PARTIAL preintegration,
postfusion block, with near-zero heterozygous integration in vitro. W03 rounds
that to zero, and the infectious ratio collapses to 1 : P^2. The rounding is
the modeling decision, not the biology, and `infectious_fraction` is that
decision written down: (1 + P^2)/(1+P)^2.

THAT FRACTION IS NOT MONOTONE, which is the one shape in this module worth
checking by hand before plotting anything. It falls on (0, 1), reaches exactly
one half at P = 1, and rises again for P > 1, tending to 1 at both ends. The
waste, 2P/(1+P)^2, is its complement and is MAXIMAL at P = 1 where it is
exactly one half: d/dP of 2P/(1+P)^2 is (2 - 2P)/(1+P)^3, which vanishes only
at P = 1. An evenly balanced co-infected cell throws away half of everything
it makes. A sweep coarse enough to skip P = 1 sees none of this.

HOW MANY VIRIONS, WHICH IS A DIFFERENT QUESTION. W03 does not partition a
fixed burst: it SCALES one. Over its lifetime a dually infected cell is taken
to release D*n HIV-1, 2*P*D*n heterozygotes and P^2*D*n crHIV-1, hence
(1+P)^2*D*n in total, against a measured burst size of n = 200 virions per
infected cell. At the paper's own headline point, P = 100 and D = 0.4, that is
816,080 virions from one cell -- about 4,080 times n, and twenty times the
40,000 that W03 cites for env-deleted SIV from unpublished data as the most
extreme output anyone has reported. W03 does not hide the assumption: it is in
the Introduction, in the model paragraph that supplies 200, and in the
Discussion ("the I_D cell burst size is greater than n"). What it never does
is say how much greater, or set its own ceiling against what its equations
demand.

AND THE LIMITING CASE, WHICH REFUTES THE SESSION'S OWN HEADLINE. Suppose
packaging is capped instead -- the cell makes n particles whatever happens.
Then the composition is still the binomial but the counts are n/(1+P)^2,
2*P*n/(1+P)^2 and P^2*n/(1+P)^2, which at P = 100 is about 196 vector
particles, 4 heterozygotes and one HIV-1 particle per 51 cells. D HAS LEFT THE
VECTOR'S OUTPUT ENTIRELY. The argument that the payload sits inside the
vector's own fitness runs through D appearing in both production terms, so in
this model that argument collapses and so does the paradox. Which model is
right is an empirical question nobody has answered. `burst_output(fixed=True)`
exists so the counterexample can be run rather than described.

THE TWO REPRODUCTIVE RATIOS, AND WHOSE THEY ARE.

`basic_R0` counts new HIV-1 infections from one infected cell when almost
every cell is uninfected. `therapeutic_R0` counts new crHIV-1 infections from
one I_T CELL -- a cell that already carries the vector and is waiting for the
virus to arrive. The therapy's susceptible pool is not uninfected cells; it is
cells already carrying the vector and nothing to replicate it. Read R0_T as
"R0 of the vector" and the whole point is gone.

WHAT A DESIGNER CONTROLS HERE. P and D, and nothing else in the formulas. R0
belongs to the patient's infection; n, c, delta, lambda and d belong to the
virus and the host; diploidy -- two draws, not three and not one -- belongs to
the chassis. The threshold is a statement about the construct and not about
the patient, and that is the sentence the hour is for.
"""
import numpy as np

__all__ = [
    "diploid_packaging", "infectious_fraction", "heterozygote_waste",
    "burst_output",
    "basic_R0", "therapeutic_R0", "P_min", "D_min",
    "coexistence",
]


def _check_P(P):
    """P is a ratio of two mRNA concentrations, so it is non-negative."""
    P = np.asarray(P, float)
    if np.any(~np.isfinite(P)):
        raise ValueError("P must be finite; the P -> infinity limit is a "
                         "statement to make, not a number to return")
    if np.any(P < 0.0):
        raise ValueError(
            f"P is the crHIV-1 : HIV-1 cytoplasmic mRNA ratio and cannot be "
            f"negative; got min {float(np.min(P))}. W03 sweeps P from 1 to "
            f"100. P = 0 is allowed and means no vector transcript at all.")
    return P


def _check_D(D):
    """D is the fraction of HIV-1 production REMAINING, so it is in [0, 1]."""
    D = np.asarray(D, float)
    if np.any(~np.isfinite(D)):
        raise ValueError(f"D must be finite; got {D}")
    if np.any((D < 0.0) | (D > 1.0)):
        raise ValueError(
            f"D is a surviving fraction of HIV-1 production and lies in "
            f"[0, 1]; got min {float(np.min(D))}, max {float(np.max(D))}. "
            f"D = 1 is NO inhibition and D = 0 is total inhibition -- the "
            f"sense is opposite to the paper's prose definition.")
    return D


def _check_R0(R0):
    """R0_T is derived at HIV-1 steady state, which needs R0 > 1."""
    R0 = float(R0)
    if not np.isfinite(R0):
        raise ValueError(f"R0 must be finite; got {R0}")
    if R0 <= 1.0:
        raise ValueError(
            f"got R0 = {R0:g}, but R0_T = P^2 D (1 - 1/R0) is derived for a "
            f"patient whose infection is ESTABLISHED, i.e. R0 > 1. At R0 <= 1 "
            f"the coefficient is zero or negative and R0_T is not a "
            f"reproductive ratio: with the printed c*delta denominator "
            f"R0 = 0.0554 and 1 - 1/R0 = -17.06, so the paper's own figures "
            f"could not exist. That is the arithmetic the session teaches, "
            f"and it is `basic_R0` that computes it -- not this function.")
    return R0


def diploid_packaging(P, normalized=True):
    """The three diploid virion genotypes from a dually infected cell. T67.

    Returns (p_HIV_homozygote, p_heterozygote, p_crHIV_homozygote).

    Two independent draws from a cytoplasmic pool at crHIV-1 : HIV-1 = P : 1,
    with q = P/(1+P) the chance a drawn transcript is vector. W03 p.3.
    The figures write the same ratio as 1 : P, ordering it HIV-1 : crHIV-1.

    `normalized=True` returns the probabilities

        1/(1+P)^2,  2P/(1+P)^2,  P^2/(1+P)^2

    which sum to one. `normalized=False` returns W03's printed ratio

        1 : 2P : P^2

    which is the same calculation with the (1+P)^2 denominator dropped. THE
    TWO DIFFER BY A FACTOR OF (1+P)^2 and an item that does not say which it
    wants is the commonest way this gets scored wrong. At P = 0 the two
    coincide, because then (1+P)^2 = 1.

    The binomial requires equal packaging probability and independent draws.
    Nothing in the assigned papers tests either; see the module docstring.
    """
    P = _check_P(P)
    hiv = np.ones_like(P)
    het = 2.0 * P
    vec = P * P
    if not normalized:
        return hiv, het, vec
    denom = (1.0 + P) ** 2
    return hiv / denom, het / denom, vec / denom


def infectious_fraction(P):
    """Fraction of released virions that can infect anything. T67.

        (1 + P^2) / (1 + P)^2

    the two homozygote probabilities, after An et al.'s preintegration block
    strikes out the heterozygotes and W03 rounds their PARTIAL block to a
    total one. Equivalently 1 - `heterozygote_waste(P)`.

    NOT MONOTONE ON (0, infinity), and a sweep that skips P = 1 will not show
    it. Strictly decreasing on (0, 1), strictly increasing on (1, infinity),
    with its MINIMUM of exactly 0.5 at P = 1, and tending to 1 at both ends --
    at P = 0 because every virion is wild-type HIV-1 and at large P because
    almost every virion is pure vector. It equals exactly 1.0 at P = 0 and is
    strictly below 1 for every P > 0.
    """
    P = _check_P(P)
    return (1.0 + P * P) / (1.0 + P) ** 2


def heterozygote_waste(P):
    """Fraction of released virions that are heterozygous, hence sterile. T67.

        2P / (1 + P)^2

    MAXIMAL AT P = 1, WHERE IT IS EXACTLY ONE HALF. The derivative is

        d/dP [ 2P/(1+P)^2 ] = (2 - 2P) / (1 + P)^3

    which vanishes only at P = 1 and changes sign there, so an evenly balanced
    dually infected cell throws away half of everything it makes. Half, not
    two thirds: one half is this quantity's ceiling over all P.

    The An et al. rounding that makes this waste rather than yield is largest
    exactly where the threshold sits, which is why it is worth a slide: it
    changes R0_T by (P + 2)/P, a factor of 3 at P = 1 and 2% at P = 100.
    """
    P = _check_P(P)
    return 2.0 * P / (1.0 + P) ** 2


def burst_output(P, D, n=200, fixed=False):
    """Virions of each genotype from one dually infected cell over its life.

    Returns (HIV_1_virions, heterozygotes, crHIV_1_virions).

    TWO MODELS, AND THE CHOICE IS THE SESSION'S SHARPEST MATERIAL.

    `fixed=False` (default) is W03's own model, read off terms Dn*delta'*I_D
    in equation [3] and P^2*Dn*delta'*I_D in equation [6]. It SCALES the burst:

        D*n ,  2*P*D*n ,  P^2*D*n        total (1+P)^2 * D * n

    so total output grows without bound in P. At P = 100, D = 0.4, n = 200
    that total is 816,080 virions from one cell, against n = 200 measured in
    vivo and 40,000 for env-deleted SIV, the largest figure W03 can cite and
    itself unpublished.

    `fixed=True` partitions a FIXED burst of n instead -- the cell makes n
    particles whatever happens, so the binomial sets the composition and
    nothing sets the total:

        n/(1+P)^2 ,  2*P*n/(1+P)^2 ,  P^2*n/(1+P)^2        total exactly n

    D IS ABSENT FROM ALL THREE COUNTS, the vector's included. It is still
    accepted and still validated, because the signature is the comparison: run
    the same call both ways and the thing that changes is whether a knob
    appears at all. R0_T's D-dependence, and with it the claim that the
    payload sits inside the vector's own fitness, survives only in the scaling
    model. Which model is right has not been measured.

    n is W03's burst size, 200 virions per HIV-1-infected cell (Haase 1996).
    """
    P = _check_P(P)
    D = _check_D(D)
    n = np.asarray(n, float)
    if np.any(n <= 0.0):
        raise ValueError(f"n is a burst size in virions and must be > 0; got "
                         f"{n}. W03 uses n = 200.")
    if fixed:
        hiv, het, vec = diploid_packaging(P, normalized=True)
        return n * hiv, n * het, n * vec
    # Written as the three production terms themselves rather than as a total
    # times a probability, so that the HIV-1 count is literally D*n.
    return D * n, 2.0 * P * D * n, P * P * D * n


def basic_R0(lam, k, n, c, d):
    """New HIV-1 infections from one infected cell, almost all cells well. T73.

        R0 = lambda * k * n / (c * d)

    AND THE PAPER PRINTS THE DENOMINATOR AS c*delta, WHICH IS WRONG. This is
    recorded here rather than silently fixed, because the session teaches the
    correction and the derivation is what settles it:

        an infected cell lives 1/delta and emits n*delta*(1/delta) = n virions
        each virion lives 1/c and infects at rate k*T, with T = lambda/d
        so R0 = n * k * (lambda/d) / c = lambda*k*n / (c*d)

    delta cancels. The d that remains is the death rate of UNINFECTED cells,
    and it enters through the virus-free steady state T0 = lambda/d of W03's
    equation [1]. Equivalently R0 is the ratio of the two steady states,
    (lambda/d) / (c/(k*n)).

    THE ARITHMETIC OF THE SLIP, from Table 1 (lambda = 31 cells/ul/day,
    k = 1.875e-4 ul/virion, n = 200, c = 30/day, d = 0.02/day, delta = 0.7/day):

        with d       R0 = 1.9375
        with delta   R0 = 0.0554   -- a virus that cannot sustain an infection,
                                      in a patient who demonstrably has one

    Three further checks all pick d: lambda/d = 1550 cells/ul is the healthy
    CD4 count the model's Fig. 2c inset approaches; T* = c/(k*n) = 800 is
    exactly Table 1's T0; and R0 = 1.9375 gives a persistence threshold of
    P^2*D > 2.0667, hence P > 3.21 at D = 0.2, against a text that says
    coexistence appears as P passes about 3. With delta instead, 1 - 1/R0 is
    -17.06 and every figure in the paper would be impossible.

    One honesty to keep attached to the 1.9375. lambda and k are not
    measurements: W03 says in one line that both came from steady-state
    analysis, and back-solving gives k = c/(n*T0) = 1.875e-4 and
    lambda = d*T0 + delta*I* = 31.0 exactly. So R0 = (lambda/d)/T0 = 1550/800
    is true by construction -- a correct number that restates two inputs. Pin
    c = 30: Table 1's footnote offers c = 3, which gives R0 = 19.375 but also
    T* = 80, contradicting T0 = 800.
    """
    lam, k, n, c, d = (float(lam), float(k), float(n), float(c), float(d))
    for name, v in (("lambda", lam), ("k", k), ("n", n), ("c", c), ("d", d)):
        if not np.isfinite(v) or v <= 0.0:
            raise ValueError(f"every rate in R0 = lambda*k*n/(c*d) must be "
                             f"finite and > 0; got {name} = {v}")
    return lam * k * n / (c * d)


def therapeutic_R0(P, D, R0):
    """New crHIV-1 infections from one I_T cell at HIV-1 steady state. T73.

        R0_T = P^2 * D * (1 - 1/R0)

    THE INDEX CASE IS AN I_T CELL, and this is the thing readers get wrong.
    R0 counts infections from an INFECTED cell. R0_T counts them from a cell
    that ALREADY CARRIES THE VECTOR and is waiting for HIV-1 to arrive: the
    therapy's susceptible pool is cells carrying crHIV-1 and nothing to
    replicate it, not uninfected cells. W03 p.6 defines it as "the number of
    new crHIV-1 infections produced from one I_T cell, assuming that the
    system is at steady state for HIV-1 infection". Gloss it as "R0 of the
    vector" and the point of the quantity is lost.

    R0_T IS PROPORTIONAL TO P^2*D, NOT APPROXIMATELY EQUAL TO IT. The
    coefficient 1 - 1/R0 runs from about 0.48 to 0.95 over any established
    infection, so persistence needs P^2*D between about 1.05 and 2.11 -- and
    2.0667 at this patient's R0 = 1.9375, which is the number every item and
    every figure uses. Reading R0_T ~ P^2*D gives P > 2.24 at D = 0.2 where
    the threshold is 3.21.

    The quadratic in P against the linear D is the paper's design result: P
    alone cannot save a bad D, because halving D costs what dividing P by
    sqrt(2) costs. And R0_T -> 0 as D -> 0, which is the paradox: D multiplies
    the vector's own production in equation [6] as well as HIV-1's in [3], so
    a better drug starves the vector that delivers it.

    Raises if R0 <= 1. The formula is derived at an established HIV-1 steady
    state, and the printed-c*delta value of 0.0554 is exactly the input that
    makes it meaningless; compute that one with `basic_R0`.

    W03 attributes its derivation to supplementary material that is not in the
    PDF and whose URL is dead. It has since been re-derived here from the
    paper's equations 4-6 by next-generation matrix at the HIV-endemic
    therapy-free equilibrium, with no added assumption, and agrees exactly;
    the threshold is the rational number 31/15. See NUMBERS.md section 18 for
    the construction, three independent verification routes, and the one trap:
    the textbook van den Driessche-Watmough split counts virion production as
    a new infection and yields sqrt(P**2 * D * (1 - 1/R0)) instead. The
    THRESHOLD is identical either way, so 2.0667 is convention-free, but the
    MAGNITUDE is not -- an item asking for a numerical R0T value must state
    the generation convention or it will mark a correct answer wrong.
    """
    P = _check_P(P)
    D = _check_D(D)
    R0 = _check_R0(R0)
    return P * P * D * (1.0 - 1.0 / R0)


def _persistence_threshold(R0):
    """The value of P^2*D at which R0_T = 1. 1/(1 - 1/R0); 2.0667 at 1.9375."""
    return 1.0 / (1.0 - 1.0 / _check_R0(R0))


def P_min(D, R0):
    """Smallest packaging advantage that persists at this D. T73.

        P_min = sqrt( 1 / (D * (1 - 1/R0)) )

    the root of R0_T = 1 in P. At R0 = 1.9375 the threshold on the product is
    P^2*D > 2.0667, so P_min is 1.4376 at D = 1, 2.2730 at D = 0.4, 3.2146 at
    D = 0.2 and 14.376 at D = 0.01. Note which way that runs: a better drug
    (smaller D) demands a BETTER-packaging vector, not a worse one.

    D = 0 has no finite answer -- a vector whose cargo shuts HIV-1 production
    off completely shuts its own off too -- and is refused rather than
    returned as infinity.
    """
    D = _check_D(D)
    if np.any(D == 0.0):
        raise ValueError(
            "at D = 0 no P persists: D multiplies the vector's own production "
            "in equation [6], so total inhibition leaves the vector nothing "
            "to package. R0_T -> 0 as D -> 0 and P_min -> infinity. That is "
            "the paradox, and it is a statement to make rather than an "
            "infinity to return.")
    return np.sqrt(_persistence_threshold(R0) / D)


def D_min(P, R0):
    """Least inhibition a construct measured at P can afford. T73, and the
    direction segment 3's release actually asks for.

        D_min = 1 / (P^2 * (1 - 1/R0))

    the root of R0_T = 1 in D, i.e. `P_min` run backwards. A construct at
    P = 8 and R0 = 1.9375 needs D > 2.0667/64 = 0.0323: it may suppress HIV-1
    production by at most about 96.8% and still spread.

    READ THE SENSE BEFORE USING THE NUMBER. D is the fraction of HIV-1
    production REMAINING, so this is a LOWER bound on D and therefore an UPPER
    bound on how good the drug may be. It is the whole of move 4 in one
    inequality.

    Returns a value above 1 when no admissible D persists at this P, which
    happens for P^2 < 1/(1 - 1/R0) -- at R0 = 1.9375, for P below 1.4376. The
    value is returned rather than raised, because the useful answer there is
    "more than all of it", and a caller comparing against 1 can say so.
    """
    P = _check_P(P)
    if np.any(P == 0.0):
        raise ValueError("at P = 0 the vector is never packaged and no D "
                         "persists; D_min is infinite")
    return _persistence_threshold(R0) / (P * P)


def coexistence(P, D, lam=31.0, k=1.875e-4, n=200.0, c=30.0, d=0.02,
                delta=0.7):
    """The HIV-1 + crHIV-1 coexistence equilibrium of Weinberger's [1]-[6].

    SOLVED, not integrated. A figure or a problem that integrates to "long
    enough" has an answer that depends on how long that was, which is
    exactly the mistake W03's own Fig. 2a invites: that panel is a 360-day
    WINDOW, and at D = 0.2 the system is still on its damped oscillation
    while at D = 0.01 it is deep in a transient that does not finish until
    about day 1500 (NUMBERS.md 20.1). Two of its five curves are not set
    points at all.

    With I_T, I_D, V_T all positive the steady state collapses to one
    scalar equation in T, where A = P**2 * D:

        [5]  I_D = k V I_T / delta'
        [6]  V_T = P^2 D n k V I_T / c
        [4]  k^2 T A n V / c = d + k V    ->  V = d / (k(k T A n/c - 1))
        [3]  n k V T = c V - D n k V I_T  ->  T = c/(k n) - D I_T
        [1]  lam = d T + k V T + (d + k V) I_T, solved for T by bisection.

    One thing falls out that a slide or a problem can use: **T\* is
    c/(kn) - D*I_T**, so the therapy costs uninfected cells.

    **AND ONE CLAIM THAT LOOKS TRUE AND IS NOT**, inherited from the figure
    module's own docstring and caught by a property test on 9 November 2026:
    V\* does **NOT** depend on P and D only through the product A = P^2 D.
    It is tempting because `_v_of` is a function of A alone -- but T is not.
    The residual carries `I_T = (c/(kn) - T)/D`, so **D enters separately**,
    and the equilibrium is not a function of A.

    Measured at fixed A = 270 (so P^2 D is held exactly constant):

        P =  20, D = 0.675     V\* = 3.35e4 /ml
        P =  30, D = 0.300     V\* =  659 /ml
        P = 100, D = 0.027     V\* =  407 /ml

    a factor of **82** across the same product, and that is measured only
    over the range where D is a legal fraction -- P below about 16.4 needs
    D > 1, which `therapeutic_R0` rightly refuses. (An earlier draft of this
    note claimed a factor of 1100 by using P = 10, D = 2.7. That D is
    outside the model. Corrected the same day it was written.) So the thing that depends
    on P^2 D alone is the **THRESHOLD** -- R_0^T = P^2 D (1 - 1/R_0), which
    is about whether the vector persists at all -- and **not the set point**
    it persists at. A student who carries "it is all P^2 D" out of the
    threshold derivation and into the clinical outcome has over-generalised,
    and this is a good place to catch it.

    **delta' cancels out of all five lines**, so this equilibrium does not
    depend on the delta' = D*delta assumption, for the same reason it
    cancels out of R_0^T (NUMBERS.md 18.2): production carries delta' and
    the I_D lifetime carries 1/delta'.

    Defaults are W03's Table 1 set as back-solved in NUMBERS.md 2a and 18.1,
    the same values `therapeutic_R0` is used with elsewhere in this course.

    Returns a dict of T, I, V, IT, ID, VT (concentrations per microlitre),
    or **None where no such equilibrium exists**, which is R_0^T < 1.

    Moved here from `figures/s25_populations.py` on 9 November 2026 so that
    PS9 imports the same solver the deck draws with. A figure and an
    autograder computing a steady state two different ways is a defect
    waiting for the first student who checks.
    """
    from scipy.optimize import brentq
    A = P * P * D
    t_pre = c / (k * n)                    # 800 cells/ul, NUMBERS.md 18.1

    def _v_of(T):
        return d / (k * (k * T * A * n / c - 1.0))

    def residual(T):
        V, it = _v_of(T), (t_pre - T) / D
        return lam - (d * T + k * V * T + (d + k * V) * it)

    lo = c / (k * A * n) * (1 + 1e-12)     # V > 0 needs T above this
    hi = t_pre * (1 - 1e-14)               # I_T > 0 needs T below it
    if lo >= hi or residual(lo) * residual(hi) > 0:
        return None
    T = brentq(residual, lo, hi, xtol=1e-14, rtol=1e-14)
    V, it = _v_of(T), (t_pre - T) / D
    dprime = D * delta
    id_ = k * V * it / dprime
    return dict(T=T, I=k * V * T / delta, V=V, IT=it, ID=id_,
                VT=P * P * D * n * dprime * id_ / c)
