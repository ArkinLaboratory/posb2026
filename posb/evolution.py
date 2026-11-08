"""Evolutionary failure and containment -- session 23's object, PS9's T61-T63.

THE CHANGE OF OBJECT, AND IT IS THE LARGEST ONE SINCE THE PHASE PLANE. Every
module before this describes one cell, or concentrations inside one cell, on a
clock measured in minutes or protein lifetimes. Here the state variable is a
FRACTION OF A POPULATION and the clock is GENERATIONS. Nothing in this module
is a concentration. Read the units on every argument.

WHERE s COMES FROM. The selection coefficient is session 19's burden read a
second way. Session 19 measured the cost of a circuit as a growth-rate
decrement -- Scott 2010's linear laws, roughly two percent of growth rate per
one percent of the proteome diverted. Put the circuit-bearing strain and a
plain one in the same flask and that decrement is the thing that removes your
circuit. Rung 1 of part II comes back as the failure mode.

THE ONE-HIT MODEL. q is the fraction of the population whose circuit no longer
works. Functional cells grow at (1 - s) times the broken ones and convert to
broken at rate mu per cell per generation; back-mutation is neglected.

    dq/dt = (1 - q) (s q + mu)

The two terms are different mechanisms and the factors say so. Selection acts
through s*q*(1-q): it needs broken cells to already exist, so it does nothing
at q = 0. Mutation acts through mu*(1-q): it needs functional cells left to
break, so it does nothing at q = 1.

This separates. Partial fractions on 1/[(1-q)(s q + mu)] give 1/(s+mu) times
[1/(1-q) + s/(s q + mu)], and both integrate to logarithms:

    t(q) = ln[ (s q + mu) / (mu (1 - q)) ] / (s + mu)

exactly, for every s >= 0 and mu > 0. Inverting it,

    q(t) = mu (E - 1) / (s + mu E),      E = exp((s + mu) t)

TWO LIMITS, BOTH TAUGHT.

1.  NO COST (s = 0). The selection term vanishes and q = 1 - exp(-mu t), pure
    accumulation, with a half-life of ln2/mu. A circuit that costs nothing
    still decays -- just slowly, and on the mutation clock alone.

2.  CHEAP MUTATION (mu << s). t50 -> ln(s/mu)/s. THE FAILURE TIME IS
    LOGARITHMIC IN THE MUTATION RATE AND INVERSE IN THE SELECTION
    COEFFICIENT. Dividing mu by a hundred buys you 2*ln(10)/s generations;
    halving s doubles the whole thing. That asymmetry is the one result here
    that changes what a designer does, and it is why `half_life` is a function
    you are meant to call twice with different s.

WHAT A STABILITY CURVE CAN AND CANNOT TELL YOU ABOUT ARCHITECTURE.
Rottinghaus et al. (Nat Commun 13:672, 2022) report non-functional cells first
appearing at about 112 generations and, over 28 days of passage without
antibiotics, a fraction viable that rises from below detection to 10^-6.35
(their Fig. 2e). It is tempting to read redundancy off that curve. With k
cassettes mutating independently at mu1, each is still intact with probability
exp(-mu1 t), and escape needs all k gone:

    q(t) = (1 - exp(-mu1 t))^k   ~   (mu1 t)^k   for mu1 t << 1

so on log-log axes the slope is k, while a one-hit process at s = 0 is a
straight line of slope 1.

DO NOT USE THAT TO COUNT CASSETTES. Give one cassette a fitness cost and
selection bends its curve the same way redundancy does: at mu = 1e-6, measured
over t = 10 to 100 generations, a single cassette with s = 0.05 has a log-log
slope of 2.36, and measured locally at t = 100 it reads 5.02. Selection and
redundancy are confounded in exactly the observable you would reach for. The
authors did build four Ptet-cas9 and three gRNA cassettes (p.4, Fig. 2c), and
nothing in this module recovers that count from performance data.

What the Fig. 2e curve does constrain is the burden, and only from one side.
Fit this family to the eight detectable points and the best fit is s = 0 with
mu = 2.6e-9 (RMS 0.151 decades); a flat line scores 0.204, so the rise itself
is barely resolved, and the data's own log-log slope is 0.63 when every model
in the family predicts at least 1. Read it as an UPPER BOUND -- s >~ 0.02 is
excluded -- and not as a measurement of s.

`mutation_selection_chain` is the honest version of the same thing: a
(k+1)-state chain where a cell with j broken cassettes converts at rate
(k-j)*mu1, intermediates are still killed on induction, and only the k-state
escapes and carries the growth advantage. With s = 0 it reproduces the closed
form above, which is the check worth running before trusting either.

WHAT THIS MODULE DELIBERATELY DOES NOT DO. There is no stochastic escape
model. The deterministic treatment is wrong in exactly the regime that matters
for a single small inoculum, where whether an escaper exists at all is a
coin-flip rather than a fraction, and saying so is part of the session. Use
posb.stochastic if you want to build that; it is not abstracted here because
it has not been built by hand in class.
"""
import numpy as np

__all__ = [
    "generations_per_passage",
    "broken_fraction", "time_to_failure", "half_life",
    "multi_hit_broken_fraction", "multi_hit_time_to_failure",
    "multi_hit_log_slope", "mutation_selection_chain",
    "fitness_cost_from_growth", "fitness_cost_from_competition",
    "containment_requirement", "escapers_per_dose", "retention_time",
]


def _check(s, mu):
    s = float(s)
    mu = float(mu)
    if s < 0.0:
        raise ValueError(f"s is a cost, so s >= 0; got {s}. A circuit that "
                         f"makes its host grow FASTER is a different model.")
    if mu <= 0.0:
        raise ValueError(f"mu must be > 0; got {mu}. At mu = 0 nothing ever "
                         f"breaks and the failure time is infinite -- that is "
                         f"a statement to make, not a number to return.")
    return s, mu


def generations_per_passage(dilution):
    """Generations of growth between daily passages at a given dilution.

    A serial-passage experiment reports its duration in days and its result in
    generations, and the conversion is one division: diluting 1:D and growing
    back to the same density takes log2(D) doublings.

    Rottinghaus et al. passaged at 250x for 28 days and report 224
    generations. log2(250) = 7.966, so 28 days is 223.0 -- they rounded to 8
    generations per day, which would be a 256x dilution. The gap is 0.4%.
    """
    dilution = np.asarray(dilution, float)
    if np.any(dilution <= 1.0):
        raise ValueError("a dilution must exceed 1; growing back from a 1x "
                         "dilution takes no generations")
    return np.log2(dilution)


def broken_fraction(t, s, mu):
    """Fraction of the population whose circuit no longer works, at time t.

    t is in GENERATIONS. Closed-form solution of dq/dt = (1-q)(s q + mu) from
    q(0) = 0. Exact, including at s = 0.
    """
    s, mu = _check(s, mu)
    t = np.asarray(t, float)
    if np.any(t < 0.0):
        raise ValueError("t is generations elapsed and cannot be negative")
    if s == 0.0:
        return -np.expm1(-mu * t)
    # q = mu(E-1)/(s + mu E) with E = exp((s+mu)t). Written with expm1 so the
    # small-t limit q -> mu*t survives in floating point. Past (s+mu)t ~ 710
    # expm1 overflows to inf and inf/inf returns NaN, which this returned
    # silently for every long horizon -- q is 1.0 to machine precision there.
    k = s + mu
    big = k * t > 700.0
    safe = np.where(big, 0.0, k * t)
    em1 = np.expm1(safe)
    q = mu * em1 / (s + mu * (em1 + 1.0))
    return np.where(big, 1.0, q)


def time_to_failure(q, s, mu):
    """Generations for the broken fraction to reach q, starting from none.

    T61. The closed form

        t(q) = ln[ (s q + mu) / (mu (1 - q)) ] / (s + mu)

    which at s = 0 reduces to -ln(1-q)/mu.

    q is a fraction strictly inside (0, 1): q = 0 is t = 0 and q = 1 never
    happens in finite time, and both are worth saying rather than returning.
    """
    s, mu = _check(s, mu)
    q = np.asarray(q, float)
    if np.any((q <= 0.0) | (q >= 1.0)):
        raise ValueError("q must lie strictly in (0,1): q=0 is t=0, and the "
                         "last functional cell is never lost in finite time")
    if s == 0.0:
        return -np.log1p(-q) / mu
    return np.log((s * q + mu) / (mu * (1.0 - q))) / (s + mu)


def half_life(s, mu):
    """Generations until half the population has lost the circuit.

    Call it twice. The point of this function is the comparison: halving s
    buys more than dividing mu by a hundred, and you should see that rather
    than be told it.
    """
    return time_to_failure(0.5, s, mu)


def multi_hit_broken_fraction(t, mu1, k):
    """Escape fraction when k cassettes must each be hit independently.

    (1 - exp(-mu1 t))^k. For mu1*t << 1 this is (mu1 t)^k, so the log-log
    slope against t is k -- which is how you read the number of independent
    lesions off a stability curve.
    """
    mu1 = float(mu1)
    if mu1 <= 0.0:
        raise ValueError(f"mu1 must be > 0; got {mu1}")
    if k != int(k) or k < 1:
        raise ValueError(
            f"k is a number of cassettes: an integer >= 1. Got {k}. This used "
            f"to truncate, so k=2.9 silently returned the k=2 answer.")
    k = int(k)
    t = np.asarray(t, float)
    if np.any(t < 0.0):
        raise ValueError("t is generations elapsed and cannot be negative")
    return (-np.expm1(-mu1 * t)) ** k


def multi_hit_time_to_failure(q, mu1, k):
    """Generations for the k-hit escape fraction to reach q. Closed form.

    Inverting (1 - exp(-mu1 t))^k = q gives t = -ln(1 - q^(1/k))/mu1.
    """
    mu1 = float(mu1)
    if mu1 <= 0.0:
        raise ValueError(f"mu1 must be > 0; got {mu1}")
    if k != int(k) or k < 1:
        raise ValueError(f"k must be an integer >= 1; got {k}")
    k = int(k)
    q = np.asarray(q, float)
    if np.any((q <= 0.0) | (q >= 1.0)):
        raise ValueError("q must lie strictly in (0,1)")
    return -np.log1p(-q ** (1.0 / k)) / mu1


def multi_hit_log_slope(t1, t2, mu1, k):
    """Log-log slope of escape fraction against time, between t1 and t2.

    Returns d log q / d log t measured as a secant. In the small-mu1*t regime
    this equals k. It is a diagnostic of the MODEL, not an estimator for data:
    a single cassette under selection produces the same steepening, so do not
    invert a measured slope to count cassettes. See the module docstring.
    """
    t1, t2 = float(t1), float(t2)
    if t1 <= 0.0 or t2 <= 0.0:
        raise ValueError(f"a log-log slope needs positive times; got {t1}, {t2}")
    if t1 == t2:
        raise ValueError("t1 and t2 must differ")
    q1 = multi_hit_broken_fraction(t1, mu1, k)
    q2 = multi_hit_broken_fraction(t2, mu1, k)
    return (np.log(q2) - np.log(q1)) / (np.log(t2) - np.log(t1))


def mutation_selection_chain(t, mu1, k, s):
    """The (k+1)-state chain, integrated. Returns (times, escape_fraction).

    State j is the fraction of the population with j of its k cassettes
    broken. A cell with j broken has k-j intact, each mutating at mu1, so it
    converts to j+1 at rate (k-j)*mu1. Only state k survives induction, and
    only state k carries the growth advantage s; every j < k is still killed,
    which is why intermediates are neutral among themselves.

    With s = 0 this must reproduce (1 - exp(-mu1 t))^k exactly. Run that check
    before trusting either form -- it is the only thing that establishes that
    the closed form and the mechanism are the same model.
    """
    from scipy.integrate import solve_ivp
    mu1 = float(mu1)
    k = int(k)
    s = float(s)
    if mu1 <= 0.0 or k < 1 or s < 0.0:
        raise ValueError(f"need mu1 > 0, k >= 1, s >= 0; got {mu1}, {k}, {s}")
    if float(t) <= 0.0:
        raise ValueError(f"t must be > 0; got {t} (this used to raise "
                         f"IndexError from inside the solver)")
    if s >= 1.0:
        raise ValueError(f"s >= 1 means the functional strain does not grow; "
                         f"got {s}")
    w = np.array([1.0 - s] * k + [1.0])

    def rhs(_, x):
        dx = x * (w - float(x @ w))
        for j in range(k):
            flux = (k - j) * mu1 * x[j]
            dx[j] -= flux
            dx[j + 1] += flux
        return dx

    x0 = np.zeros(k + 1)
    x0[0] = 1.0
    ts = np.linspace(0.0, float(t), 2001)
    sol = solve_ivp(rhs, [0.0, float(t)], x0, t_eval=ts,
                    rtol=1e-11, atol=1e-16, method="Radau")
    if not sol.success:
        raise RuntimeError(f"chain integration failed: {sol.message}")
    return sol.t, sol.y[k]


def fitness_cost_from_growth(t, n_circuit, n_control):
    """s from two growth curves measured separately. T62.

    Fits ln(n) against t by least squares for each strain and returns
    1 - lambda_circuit/lambda_control.

    This is the weaker of the two estimators and the session says so. Two
    cultures grown separately differ in inoculum, aeration and the day, and the
    difference you are after is a few percent of the slope. The competition
    assay below measures the difference directly and is what Rottinghaus use.
    """
    t = np.asarray(t, float)
    a = np.asarray(n_circuit, float)
    b = np.asarray(n_control, float)
    if t.shape != a.shape or t.shape != b.shape:
        raise ValueError(f"t, n_circuit and n_control must have the same "
                         f"shape; got {t.shape}, {a.shape}, {b.shape}")
    if t.size < 2:
        raise ValueError("need at least two timepoints to fit a slope")
    if np.any(a <= 0.0) or np.any(b <= 0.0):
        raise ValueError("densities must be positive to take a logarithm")
    lam_c = np.polyfit(t, np.log(a), 1)[0]
    lam_0 = np.polyfit(t, np.log(b), 1)[0]
    if lam_0 <= 0.0:
        raise ValueError(f"the reference strain must be growing; fitted "
                         f"lambda_control = {lam_0:.4g}")
    s = 1.0 - lam_c / lam_0
    if s >= 1.0:
        raise ValueError(
            f"fitted s = {s:.4g}. s >= 1 means the circuit strain is not "
            f"growing at all, so a selection coefficient is the wrong "
            f"description and time_to_failure would take it anyway.")
    return s


def fitness_cost_from_competition(generations, ratio):
    """s from a head-to-head competition. T62, and the better estimator.

    `ratio` is n_circuit/n_control at each timepoint. The two strains share
    every condition, so

        d/dt ln(n_circuit/n_control) = (1 - s) - 1 = -s

    per generation of the reference strain, and s is minus the slope of the log
    ratio. Returns s.
    """
    g = np.asarray(generations, float)
    r = np.asarray(ratio, float)
    if g.shape != r.shape:
        raise ValueError(f"generations and ratio must have the same shape; "
                         f"got {g.shape} and {r.shape}")
    if g.size < 2:
        raise ValueError("need at least two timepoints to fit a slope")
    if np.any(r <= 0.0):
        raise ValueError("a ratio of counts must be positive")
    return -np.polyfit(g, np.log(r), 1)[0]


def containment_requirement(dose, max_escapers=1.0):
    """The fraction viable a circuit must achieve for a given dose. T63.

    A requirement on a fraction is really a requirement on a number of
    survivors, and the two are joined by the dose. The NIH Office of
    Biotechnology Activities figure quoted by Rottinghaus is a fraction viable
    of 1e-8; their gavage dose is 1e8 CFU. Those two numbers are matched, and
    the room should be asked to notice it: the requirement is fewer than one
    survivor per dose.
    """
    dose = np.asarray(dose, float)
    if np.any(dose <= 0.0):
        raise ValueError("a dose is a positive number of cells")
    if max_escapers <= 0.0:
        raise ValueError("max_escapers must be > 0; zero survivors is not a "
                         "fraction any finite circuit achieves")
    req = float(max_escapers) / dose
    if np.any(req >= 1.0):
        raise ValueError(
            f"this dose needs a fraction viable of {np.max(req):.3g}, which is "
            f"not a requirement -- it is satisfied by doing nothing. The dose "
            f"is smaller than the number of escapers you are allowing.")
    return req


def escapers_per_dose(dose, fraction_viable):
    """Expected survivors when `dose` cells are released. T63."""
    dose = np.asarray(dose, float)
    fv = np.asarray(fraction_viable, float)
    if np.any(dose <= 0.0):
        raise ValueError("a dose is a positive number of cells")
    if np.any((fv < 0.0) | (fv > 1.0)):
        raise ValueError("a fraction viable lies in [0, 1]")
    return dose * fv


def retention_time(limit, s=None, mu=None, k=1, mu1=None):
    """Generations for which a containment claim holds. T63.

    The generation at which the escape fraction first exceeds `limit`. With
    k = 1 this is time_to_failure against the requirement rather than against
    a half-life; with k > 1, pass mu1 (the PER-CASSETTE rate) and it uses the
    k-hit form.

    The distinction this function exists to make: a measured fraction viable
    is a SNAPSHOT and a containment requirement is a DURATION. A circuit can
    clear 1e-8 in an assay and cross it again within a few generations of
    permissive growth, and those are not contradictory measurements.
    """
    limit = np.asarray(limit, float)
    if np.any((limit <= 0.0) | (limit >= 1.0)):
        raise ValueError("a containment limit is a fraction in (0,1)")
    if k != int(k) or k < 1:
        raise ValueError(f"k must be an integer >= 1; got {k}")
    if int(k) == 1:
        if mu1 is not None:
            raise ValueError("mu1 is the per-cassette rate and is meaningless "
                             "at k = 1; pass mu")
        return time_to_failure(limit, s, mu)
    if mu1 is None:
        raise ValueError("with k > 1 the per-cassette rate mu1 is required; "
                         "mu is the whole-circuit rate and the two differ by "
                         "orders of magnitude")
    # The k > 1 branch is a PURE MUTATION model: it has no selection in it, so
    # s and mu are not used and must not be passed, or the caller will believe
    # a crossing time responds to a burden it is completely insensitive to.
    # This returned the same answer for s = 0, 0.02, 0.5 and -1.
    if s is not None or mu is not None:
        raise ValueError(
            "at k > 1 this uses the pure multi-hit form, which carries no "
            "selection: pass s=None, mu=None so it is clear that the answer "
            "does not depend on them. Selection enters only through the fit "
            "that produced mu1.")
    return multi_hit_time_to_failure(limit, mu1, k)
