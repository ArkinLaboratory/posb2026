"""Session 20. Flux balance analysis as a linear program.

Session 3 built the stoichiometric matrix S and integrated

    dx/dt = S @ v(x, p)

This module takes the same S, sets the left-hand side to zero, and throws the
rate column away:

    S @ v = 0,    lo <= v <= hi,    maximise  c @ v

That is the whole of flux balance analysis, and the thing worth noticing is
what is *missing*. There are no rate constants here. S is the only part of a
cell you can write down exactly -- it is counting atoms -- and the price of
that exactness is that it says nothing about how fast anything goes. So the
constraints are free and the prediction is not: to get a number out you must
supply an objective, and the objective is a hypothesis about what selection
has done to the organism, not a property of the network.

Fong & Palsson (2004) is what happens when somebody tests that hypothesis.
Given measured substrate and oxygen uptake rates as inputs, a 904-gene model
predicted the growth rate of 39 of 50 *evolved* deletion strains to within
10%. The strains had to evolve first; a freshly built knockout is not where
the model says it should be. See `sessions/s20-metabolic/NUMBERS.md`.

Two limitations are built into the shape of the problem and are not defects:

*   A linear program always has **an** optimum at a **vertex**, so a solver
    hands back an all-or-nothing split at a branch point. That is a fact
    about what you are shown, not about what is optimal: when two arms tie,
    every blend of them is equally optimal too. See `has_alternate_optima`.
*   **Alternate optima are generic**: several different flux distributions can
    hit the same optimal objective, and the solver returns one of them without
    saying so. `flux_ranges` is the standard way to find out -- it is flux
    variability analysis, after Mahadevan & Schilling, Metab Eng 5, 264 (2003).

Everything here is NumPy and `scipy.optimize.linprog`. There is no hidden
solver and no COBRA toolbox. Read the source.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog

__all__ = [
    "FluxModel",
    "teaching_network",
    "solve_fba",
    "knockout_growth",
    "flux_ranges",
    "coupled_pairs",
    "has_alternate_optima",
]

_DEFAULT_UPPER = 1000.0          # a stand-in for "unbounded", as every FBA code uses


class FluxModel:
    """A reaction network as a stoichiometric matrix, with no rates at all.

    Parameters
    ----------
    reactions : list
        Each entry is either a `posb.core.Reaction`, or a tuple
        ``(reactants, products, name)`` of two dicts and a string. Use an empty
        dict for an exchange: ``({}, {"Glc": 1}, "v_uptake")`` is uptake and
        ``({"Ace": 1}, {}, "v_acetate")`` is secretion.
    metabolites : list of str, optional
        Fixes the row order of S. Defaults to sorted order, as `posb.core.Model`
        does, so the two agree.
    external : iterable of str, optional
        Metabolites that are NOT balanced -- a medium component, or something
        secreted and gone. They keep their rows out of S entirely, so the
        network needs no exchange reaction for each one. This is standard FBA
        practice and it is what keeps a teaching network small enough to read.

    Every other metabolite is **balanced**: S @ v = 0 applies to it. A
    metabolite that is balanced and has only one producer and one consumer has
    already had its flux ratio decided by the network, which is where coupling
    comes from.

    Attributes
    ----------
    S : ndarray, shape (metabolites, reactions)
        Identical in convention to `posb.core.Model.S`, and tested to be.
    """

    def __init__(self, reactions, metabolites=None, external=()):
        self.reactions = []
        for r in reactions:
            if hasattr(r, "reactants") and hasattr(r, "products"):
                self.reactions.append((dict(r.reactants), dict(r.products),
                                       getattr(r, "name", None)))
            else:
                reactants, products, name = r
                self.reactions.append((dict(reactants), dict(products), name))

        self.names = [n or f"v{j}" for j, (_, _, n) in enumerate(self.reactions)]
        if len(set(self.names)) != len(self.names):
            raise ValueError("reaction names must be unique")

        found = set()
        for reactants, products, _ in self.reactions:
            found |= set(reactants) | set(products)
        self.external = set(external)
        stray = self.external - found
        if stray:
            raise ValueError(f"External metabolite(s) not in the network: {sorted(stray)}")
        balanced = found - self.external
        if metabolites is None:
            self.metabolites = sorted(balanced)
        else:
            missing = balanced - set(metabolites)
            if missing:
                raise ValueError(f"Metabolites not listed: {sorted(missing)}")
            extra = set(metabolites) & self.external
            if extra:
                raise ValueError(f"External metabolite(s) given a row: {sorted(extra)}")
            self.metabolites = list(metabolites)

        self._row = {m: i for i, m in enumerate(self.metabolites)}
        self._col = {n: j for j, n in enumerate(self.names)}
        self.S = self._build_S()

    def _build_S(self):
        """S[i, j] = net stoichiometry of metabolite i in reaction j.

        The same three lines as `posb.core.Model._build_S`, on purpose.
        """
        S = np.zeros((len(self.metabolites), len(self.reactions)))
        for j, (reactants, products, _) in enumerate(self.reactions):
            for m, n in reactants.items():
                if m in self.external:
                    continue
                S[self._row[m], j] -= n
            for m, n in products.items():
                if m in self.external:
                    continue
                S[self._row[m], j] += n
        return S

    @property
    def null_space_dimension(self):
        """How many degrees of freedom are left after S @ v = 0.

        reactions - rank(S). This is what you have to choose, and in any network
        with more reactions than independent balances it is large -- which is
        where the need for an objective comes from. It is a consequence, not a
        step in a recipe.
        """
        return len(self.names) - np.linalg.matrix_rank(self.S)

    def index(self, name):
        return self._col[name]

    def _bound_arrays(self, bounds, knockouts=()):
        unknown = (set(bounds) | set(knockouts)) - set(self.names)
        if unknown:
            raise ValueError(f"Unknown reaction(s): {sorted(unknown)}")
        out = []
        for n in self.names:
            lo, hi = bounds.get(n, (0.0, _DEFAULT_UPPER))
            if n in knockouts:
                lo, hi = 0.0, 0.0          # a knockout is a bound set to zero
            if lo > hi:
                raise ValueError(f"{n}: lower bound {lo} above upper {hi}")
            out.append((lo, hi))
        return out

    def __repr__(self):
        return (f"FluxModel({len(self.metabolites)} balanced metabolites"
                + (f" + {len(self.external)} external" if self.external else "")
                + f", {len(self.names)} reactions, "
                f"null space {self.null_space_dimension})")


def _objective_vector(model, objective):
    c = np.zeros(len(model.names))
    if isinstance(objective, str):
        c[model.index(objective)] = 1.0
    else:
        for name, weight in objective.items():
            c[model.index(name)] = float(weight)
    return c


def solve_fba(model, objective, bounds, knockouts=(), sense="max"):
    """Maximise (or minimise) a linear objective subject to S @ v = 0.

    Parameters
    ----------
    model : FluxModel
    objective : str or dict
        A reaction name, or {name: weight}.
    bounds : dict
        {reaction name: (lo, hi)}. Anything unlisted gets (0, 1000).
    knockouts : iterable of str
        Reaction names forced to zero flux. That is all a knockout is here.
    sense : {"max", "min"}

    Returns
    -------
    (objective_value, flux_dict). If the problem is infeasible, returns
    (nan, None) -- which is a real answer and not an error: it means the
    network as constrained cannot carry flux, and it is how a lethal knockout
    presents itself.
    """
    c = _objective_vector(model, objective)
    sign = 1.0 if sense == "max" else -1.0
    res = linprog(
        c=-sign * c,
        A_eq=model.S,
        b_eq=np.zeros(model.S.shape[0]),
        bounds=model._bound_arrays(bounds, knockouts),
        method="highs",
    )
    if not res.success:
        return float("nan"), None
    return float(sign * (-res.fun)), dict(zip(model.names, res.x))


def knockout_growth(model, objective, bounds, reactions):
    """Predicted objective value for each single knockout, plus the wild type.

    Returns {reaction_name: value}, with `"wild type"` included. A value of 0.0
    is the structural case -- the network cannot make biomass at all without
    that reaction -- and is exactly the shape of Fong & Palsson's tpi strains,
    for which no growth was computationally predicted on three substrates.
    """
    out = {"wild type": solve_fba(model, objective, bounds)[0]}
    for r in reactions:
        value, _ = solve_fba(model, objective, bounds, knockouts=(r,))
        if np.isnan(value) or abs(value) < 1e-9:
            value = 0.0                     # also clears a signed -0.0
        out[r] = value
    return out


def flux_ranges(model, objective, bounds, knockouts=(), fraction=1.0, tol=1e-9):
    """Flux variability analysis: min and max of every flux at the optimum.

    Holds the objective at `fraction` of its optimal value and then minimises
    and maximises each flux in turn. A reaction whose min and max differ is not
    determined by the optimum -- the solver's single answer for it was a
    choice, not a prediction.

    This is Mahadevan & Schilling, Metab Eng 5, 264-276 (2003).

    Returns {reaction_name: (lo, hi)}, or None if infeasible.
    """
    best, _ = solve_fba(model, objective, bounds, knockouts)
    if np.isnan(best):
        return None
    c = _objective_vector(model, objective)

    # Pin the objective with an inequality so numerical slack cannot make it
    # infeasible:  c @ v >= fraction * best   <=>   -c @ v <= -fraction * best
    A_ub = (-c).reshape(1, -1)
    b_ub = np.array([-(fraction * best - tol)])
    bnds = model._bound_arrays(bounds, knockouts)

    out = {}
    for j, name in enumerate(model.names):
        e = np.zeros(len(model.names)); e[j] = 1.0
        lo_res = linprog(c=e, A_eq=model.S, b_eq=np.zeros(model.S.shape[0]),
                         A_ub=A_ub, b_ub=b_ub, bounds=bnds, method="highs")
        hi_res = linprog(c=-e, A_eq=model.S, b_eq=np.zeros(model.S.shape[0]),
                         A_ub=A_ub, b_ub=b_ub, bounds=bnds, method="highs")
        if not (lo_res.success and hi_res.success):
            return None
        out[name] = (float(lo_res.fun), float(-hi_res.fun))
    return out


def has_alternate_optima(model, objective, bounds, knockouts=(), tol=1e-6):
    """Does more than one flux distribution achieve the optimum?

    True when any flux has a non-degenerate range at the optimal objective.
    Stated as a predicate so the teaching claim is checkable rather than
    asserted on a slide -- and so a figure that stops carrying the argument
    fails its test.
    """
    ranges = flux_ranges(model, objective, bounds, knockouts)
    if ranges is None:
        return False
    return any(hi - lo > tol for lo, hi in ranges.values())


def _feasible_vertices(model, bounds, knockouts=()):
    """Flux vectors at the vertices reached by driving each flux to its extremes.

    Used by `coupled_pairs`. Nothing is held at an optimum here: the whole
    feasible space is sampled, because full coupling is a property of S and the
    bounds and has nothing to do with which objective you happened to pick.
    """
    bnds = model._bound_arrays(bounds, knockouts)
    zeros = np.zeros(model.S.shape[0])
    pts = []
    for j in range(len(model.names)):
        e = np.zeros(len(model.names))
        e[j] = 1.0
        for c in (e, -e):
            r = linprog(c=c, A_eq=model.S, b_eq=zeros, bounds=bnds,
                        method="highs")
            if r.success:
                pts.append(dict(zip(model.names, r.x)))
    return pts


def coupled_pairs(model, objective=None, bounds=None, knockouts=(), tol=1e-7):
    """Pairs of reactions whose flux ratio is fixed everywhere in the network.

    For each pair, v_i / v_j is checked at every vertex `_feasible_vertices`
    visits. A pair is reported only if the ratio is the same at all of them and
    at least two of them say something -- so a reaction that merely happens to
    sit at a fixed value is NOT reported as coupled to every other fixed one.

    Fully coupled pairs are the ones worth showing in class, because they are
    the places where the *network* has already decided something and no
    regulation can change it -- a metabolite made by exactly one reaction and
    consumed by exactly one other.

    `objective` is accepted for call compatibility and deliberately ignored.
    That is the teaching point rather than an oversight: coupling holds under
    every objective you could have chosen, so an objective must not appear in
    the test. An earlier version of this function sampled only the optimal face
    and reported the pairs whose fluxes `flux_ranges` found pinned there. On a
    network with a unique optimum that is every reaction, so it returned all 21
    pairs of the teaching network's nonzero fluxes -- the ratio of two
    constants, reported as though it were a structural fact -- while missing
    the genuinely linked pairs whenever they varied.

    Returns {(a, b): ratio}.
    """
    pts = _feasible_vertices(model, bounds if bounds is not None else {},
                             knockouts)
    if not pts:
        return {}
    names = list(model.names)
    out = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ratios = []
            consistent = True
            for f in pts:
                va, vb = f[a], f[b]
                if abs(va) <= tol and abs(vb) <= tol:
                    continue                       # both idle: says nothing
                if abs(vb) <= tol:                 # one carries flux, one not
                    consistent = False
                    break
                ratios.append(va / vb)
            if not consistent or len(ratios) < 2:
                continue
            if max(ratios) - min(ratios) <= tol * max(1.0, abs(ratios[0])):
                out[(a, b)] = ratios[0]
    return out


# --------------------------------------------------------------- the teaching network

def teaching_network(isozyme=False):
    """The session-20 network: 9 reactions, 6 balanced metabolites, hand-solvable.

    Returns ``(reactions, external, bounds)`` ready for
    ``FluxModel(reactions, external=external)`` and ``solve_fba(m, "v_biomass",
    bounds)``.

    Small enough to read off a slide and big enough to carry every point the
    session needs. **Every reaction balances carbon** (there is a test), which
    matters because the session's thesis is that S counts atoms exactly:

    ====================  =========================================  =========
    reaction              stoichiometry                              C balance
    ====================  =========================================  =========
    v_uptake              -> G6P                                     (source)
    v_pgi                 G6P -> F6P                                 6 -> 6
    v_zwf                 G6P -> P5P + CO2                           6 -> 6
    v_tpi                 F6P -> 2 T3P                               6 -> 6
    v_lower               T3P -> PYR + ATP                           3 -> 3
    v_ackA                PYR -> Ace + CO2 + ATP                     3 -> 3
    v_tca                 PYR -> 3 CO2 + 3 ATP                       3 -> 3
    v_biomass             2 T3P + P5P + 4 ATP ->                     (sink)
    v_atpm                ATP ->                                     (sink)
    ====================  =========================================  =========

    Glucose uptake is capped at 10 and that is the only numerical constraint.
    The answers are integers, and the board can get them in six lines:

        P5P has one producer and one consumer, so  v_zwf = b
        G6P:  10 = v_pgi + v_zwf                   v_pgi = 10 - b
        F6P has one producer and one consumer, so  v_tpi = v_pgi     [coupled]
        T3P:  2 v_tpi = 2b + v_lower               v_lower = 20 - 4b
        ATP, all pyruvate through the TCA:  4(20 - 4b) >= 4b
                                                   b <= 4

    so **biomass = 4 exactly**, with v_pgi = v_tpi = 6, v_zwf = 4,
    v_lower = v_tca = 4 and v_ackA = 0. The branch point goes all-or-nothing to
    the TCA because it yields 3 ATP against acetate's 1. That optimum is a
    vertex -- but note the theorem is that SOME optimum is a vertex, not that
    it is unique. See `isozyme` below, where it is not.

    Knock out the TCA and the same six lines give **b <= 10/3**: the optimum
    moves to a different vertex, acetate now carries all the pyruvate, and the
    cost of the knockout is exact rather than simulated.

    Knock out v_pgi, v_zwf, v_tpi or v_lower and biomass is **exactly zero** --
    the network has no other route to T3P, to P5P or to ATP. That is the shape
    of Fong & Palsson's tpi strains, for which no growth was computationally
    predicted on lactate, malate or succinate.

    Parameters
    ----------
    isozyme : bool
        Add ``v_zwf2``, a second route with stoichiometry identical to
        ``v_zwf``. The optimal biomass does not change, and the split between
        the two routes becomes completely free: `flux_ranges` reports both over
        [0, 4]. This is the alternate-optima limitation made executable instead
        of asserted -- the solver reports one of the two and no measurement of
        growth rate can tell them apart.

        **This reaction is a modelling device, not a biological claim.**
        *E. coli* has a single glucose-6-phosphate dehydrogenase, so there is no
        real duplicate of ``v_zwf``. It is constructed here because an exactly
        degenerate pair makes the tie hand-checkable. Real networks do carry
        genuine redundancy of this kind -- parallel electron-transport branches,
        duplicated transhydrogenases -- and that is where alternate optima come
        from in practice; say that in class rather than implying this particular
        isozyme exists.
    """
    external = ("Ace_x", "CO2_x")
    reactions = [
        ({},                            {"G6P": 1},                             "v_uptake"),
        ({"G6P": 1},                    {"F6P": 1},                             "v_pgi"),
        ({"G6P": 1},                    {"P5P": 1, "CO2_x": 1},                 "v_zwf"),
        ({"F6P": 1},                    {"T3P": 2},                             "v_tpi"),
        ({"T3P": 1},                    {"PYR": 1, "ATP": 1},                   "v_lower"),
        ({"PYR": 1},                    {"Ace_x": 1, "CO2_x": 1, "ATP": 1},     "v_ackA"),
        ({"PYR": 1},                    {"CO2_x": 3, "ATP": 3},                 "v_tca"),
        ({"T3P": 2, "P5P": 1, "ATP": 4}, {},                                    "v_biomass"),
        ({"ATP": 1},                    {},                                     "v_atpm"),
    ]
    if isozyme:
        reactions.append(({"G6P": 1}, {"P5P": 1, "CO2_x": 1}, "v_zwf2"))
    bounds = {"v_uptake": (0.0, 10.0)}
    return reactions, external, bounds


#: Carbons per metabolite in `teaching_network`, for the atom-balance test.
CARBONS = {"G6P": 6, "F6P": 6, "P5P": 5, "T3P": 3, "PYR": 3,
           "Ace_x": 2, "CO2_x": 1, "ATP": 0}

#: Reactions in `teaching_network` that are pseudo-reactions (a source or a
#: sink) and so are not expected to balance carbon.
PSEUDO = ("v_uptake", "v_biomass", "v_atpm")
