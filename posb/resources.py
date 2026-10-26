"""
posb.resources — competition for a shared translational pool.

Introduced in Session 19. You derive the steady state on the board first; this
is the same algebra made reusable, and it is what PS7 asks you to call.

THE SYSTEM. Ribosomes bind mRNA reversibly and are released on completion:

    R + m_i  <->  C_i          dissociation constant K_i      (fast)
    C_i      ->   p_i + R + m_i   rate k_i
    p_i      ->   0               rate gamma

THE DERIVATION, and it is session 4's move applied to a new object. Put the
binding step at quasi-steady state -- the same approximation used to derive
Michaelis-Menten, except that the thing being held at equilibrium is the
RIBOSOME's occupancy rather than an enzyme's:

    C_i = R m_i / K_i

Ribosomes are conserved. Writing the DEMAND of gene i as d_i = m_i / K_i:

    R_T = R + sum_i C_i = R (1 + sum_i d_i)
    R   = R_T / (1 + sum_i d_i)

    p_i (steady state) = (k_i R_T / gamma) * d_i / (1 + sum_j d_j)

THAT DENOMINATOR IS SESSION 6'S PARTITION FUNCTION with a different pool in it.
In session 6 the competing demands were transcription factors for an operator
and the sum ran over binding configurations; here they are mRNAs for the
ribosome pool and the sum runs over genes. Nothing new had to be invented to
write it down, which is the argument for having derived it the hard way once.

THREE RESULTS, all exact, and all of them about composition rather than about
ribosomes:

  1. THE EDGE THAT IS NOT IN THE DIAGRAM. p_i depends on d_j for every other
     gene j. Inducing one gene lowers the output of a gene it has no
     regulatory connection to. Nothing in a circuit schematic records this.

  2. THE FALL IS A HYPERBOLA, indistinguishable in shape from repression by a
     factor with Hill coefficient 1:

         p_1(d_2) = p_1(0) / (1 + d_2 / (1 + d_1))

     so the phantom repressor has apparent dissociation constant
     K_app = 1 + d_1 -- it depends on the demand of the gene being apparently
     repressed. A real repressor's dissociation constant does not. That is the
     experimental signature that tells resource coupling from regulation, and
     `apparent_K` returns it.

  3. THE ISOCOST LINE. Normalise each output by what it would reach alone at
     unlimited demand. Then the normalised outputs sum to
     (sum d) / (1 + sum d), which is below one always and approaches one as
     total demand grows. The achievable outputs are confined BELOW a straight
     line whose intercepts are the single-gene maxima, and the sum depends only
     on the total demand, not on how it is split between genes.

     Measured in Gyorgy, Jimenez, Yazbek, Huang, Chung, Weiss & Del Vecchio,
     "Isocost lines describe the cellular economy of genetic circuits",
     Biophys J 109(3):639-646 (2015).

WHAT IS NOT IN THIS MODULE, DELIBERATELY. Growth coupling -- the fact that
diverting ribosomes slows growth, that growth sets the dilution rate gamma, and
that gamma is therefore not a constant of the circuit's own dynamics. The
structure is in `dilution_coupled_steady_state`, but the empirical coefficient
that turns demand into a growth penalty is an argument the caller must supply
with its source. No measured growth law is hard-coded here, because the numbers
differ by host, medium and construct, and a coefficient baked into a library
loses the citation that makes it meaningful.
"""

import numpy as np

__all__ = [
    "free_fraction", "expression", "apparent_K", "isocost_sum",
    "competition_model", "dilution_coupled_steady_state",
]


def _demands(demands):
    d = np.asarray(demands, dtype=float)
    if d.ndim != 1:
        raise ValueError("demands must be one-dimensional")
    if np.any(d < 0):
        raise ValueError("a demand cannot be negative")
    return d


def free_fraction(demands):
    """Fraction of the ribosome pool left unbound: 1 / (1 + sum of demands).

    This single number is what every gene in the cell is multiplied by, which
    is why it is the right object to think in. Halving it halves every output
    at once.
    """
    return 1.0 / (1.0 + _demands(demands).sum())


def expression(demands, capacity=1.0):
    """Steady-state output of each gene, as an array in the input order.

    `capacity` is k_i R_T / gamma, the output a single gene would reach if it
    had the whole pool and infinite demand. Passing a scalar applies it to
    every gene; pass an array for genes with different translation rates.
    """
    d = _demands(demands)
    return np.asarray(capacity, dtype=float) * d / (1.0 + d.sum())


def apparent_K(own_demand):
    """Apparent dissociation constant of the phantom repressor: 1 + d_self.

    Fit a Hill-1 repression curve to the fall in gene 1's output as gene 2 is
    induced, and this is the K you get. It moves when gene 1's OWN expression
    is changed, which no real repressor's K does -- so measuring K_app at two
    different expression levels of the reporter distinguishes resource
    competition from regulation without cloning anything.
    """
    return 1.0 + float(own_demand)


def isocost_sum(demands):
    """Sum of the normalised outputs: (sum d) / (1 + sum d).

    Strictly below 1, approaching 1 as total demand grows, and a function of
    the TOTAL demand only -- which is why the achievable region is bounded by
    a straight line rather than by a curve.
    """
    s = _demands(demands).sum()
    return s / (1.0 + s)


def competition_model(demands, k=1.0, R_total=1.0, gamma=1.0, k_on=1e3):
    """The full binding kinetics as a `posb.core.Model`, without the QSSA.

    The closed forms above are the steady state of this system under the
    quasi-steady-state assumption on binding. This builds the system itself, so
    the assumption can be checked rather than believed -- which is the exercise
    session 4 set up and this session cashes.

    State is [C_1..C_n, p_1..p_n]; free ribosomes are whatever conservation
    leaves, so R_total enters through the binding flux rather than as a
    species. mRNA is held fixed and the demand is carried by K_i.
    """
    from .core import Reaction, Model

    d = _demands(demands)
    if np.any(d <= 0):
        raise ValueError("competition_model needs every demand strictly positive")
    n = len(d)
    mrna = np.ones(n)
    K = mrna / d                      # so that m_i / K_i is the demand asked for

    def free(c):
        return R_total - sum(c[f"C{j+1}"] for j in range(n))

    reactions = []
    for i in range(n):
        reactions.append(Reaction(
            {}, {f"C{i+1}": 1},
            rate=(lambda c, p, i=i: p["k_on"] * free(c) * p[f"m{i+1}"]),
            name=f"ribosome binds mRNA {i+1}",
        ))
        reactions.append(Reaction(
            {f"C{i+1}": 1}, {},
            rate=(lambda c, p, i=i: p["k_on"] * p[f"K{i+1}"] * c[f"C{i+1}"]),
            name=f"ribosome leaves mRNA {i+1}",
        ))
        reactions.append(Reaction(
            {f"C{i+1}": 1}, {f"C{i+1}": 1, f"p{i+1}": 1},
            rate=(lambda c, p, i=i: p["k_tl"] * c[f"C{i+1}"]),
            name=f"translate protein {i+1}",
        ))
        reactions.append(Reaction(
            {f"p{i+1}": 1}, {}, k="gamma",
            name=f"protein {i+1} dilutes",
        ))

    params = {"k_on": k_on, "k_tl": k, "gamma": gamma}
    for i in range(n):
        params[f"m{i+1}"] = mrna[i]
        params[f"K{i+1}"] = K[i]
    species = [f"C{i+1}" for i in range(n)] + [f"p{i+1}" for i in range(n)]
    return Model(reactions, params=params, species=species)


def dilution_coupled_steady_state(demands, growth_penalty, capacity=1.0,
                                  gamma_0=1.0):
    """Steady state when diverting ribosomes slows growth, and growth dilutes.

    `growth_penalty` is a callable mapping total demand to the FRACTION of the
    unburdened growth rate that remains, so growth_penalty(0.0) should be 1.0.
    It is a required argument and carries no default on purpose: the course
    supplies it from a measurement, with the citation attached, rather than
    from a constant in a library.

    The point of the function is structural. The dilution rate gamma is not a
    property of the protein -- it is the growth rate, and the growth rate falls
    when the circuit is induced. So inducing a circuit changes the effective
    lifetime of every protein in the cell, including its own, and the response
    time computed in session 5 is not the response time it will show.

    Returns (outputs, gamma), with gamma the dilution rate actually in force.
    """
    d = _demands(demands)
    frac = float(growth_penalty(d.sum()))
    if not 0.0 < frac <= 1.0:
        raise ValueError(
            "growth_penalty must return a fraction in (0, 1]; "
            f"got {frac} at total demand {d.sum()}"
        )
    gamma = gamma_0 * frac
    # capacity was quoted at gamma_0; slower dilution raises the steady state
    return expression(d, capacity=np.asarray(capacity) * gamma_0 / gamma), gamma
