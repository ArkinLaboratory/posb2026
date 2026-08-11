"""
posb.core — reactions, models, and simulation.

This module does exactly one thing: it turns a list of reactions into the
system of differential equations

    dx/dt = S @ v(x, p)

and integrates it.  Nothing here is magic, and you are expected to read it.
Every function is short enough to hold in your head.  If you ever wonder what
`Model.simulate` is doing, open this file — that is the point.

Introduced in Session 3.
"""

import numpy as np
from scipy.integrate import solve_ivp

__all__ = ["Reaction", "Model", "Trajectory"]


class Reaction:
    """A single chemical reaction.

    Parameters
    ----------
    reactants, products : dict
        Maps species name -> stoichiometric coefficient (a positive integer).
        Use an empty dict for synthesis from nothing or degradation to nothing.
        Example: {"A": 1, "B": 2} means A + 2B.
    k : float or str, optional
        Mass-action rate constant.  If a string, it is looked up in the
        parameter dictionary at simulation time, so you can sweep it.
        The flux is then  k * prod([S]**stoichiometry)  over all reactants.
    rate : callable, optional
        Use this instead of `k` when the flux is not mass action (a Hill
        function, for instance).  Signature: rate(c, p) -> float, where `c`
        is a dict of current concentrations keyed by species name and `p` is
        the parameter dict.
    name : str, optional
        Label, used in error messages and plots.

    Examples
    --------
    >>> Reaction({"A": 1, "B": 1}, {"C": 1}, k=0.5)          # A + B -> C
    >>> Reaction({}, {"m": 1}, rate=lambda c, p: p["alpha"]) # -> m
    >>> Reaction({"m": 1}, {}, k="gamma")                    # m -> 0
    """

    def __init__(self, reactants, products, k=None, rate=None, name=None):
        if (k is None) == (rate is None):
            raise ValueError(
                "Give exactly one of k (mass action) or rate (custom flux)."
            )
        self.reactants = dict(reactants)
        self.products = dict(products)
        self.k = k
        self.rate = rate
        self.name = name or self._default_name()

    def _default_name(self):
        def side(d):
            if not d:
                return "0"
            return " + ".join(
                (f"{n} {s}" if n != 1 else s) for s, n in d.items()
            )
        return f"{side(self.reactants)} -> {side(self.products)}"

    def species(self):
        """Every species this reaction touches."""
        return set(self.reactants) | set(self.products)

    def flux(self, c, p):
        """Reaction velocity given concentrations `c` (dict) and params `p` (dict)."""
        if self.rate is not None:
            return self.rate(c, p)
        k = p[self.k] if isinstance(self.k, str) else self.k
        v = k
        for s, n in self.reactants.items():
            v = v * c[s] ** n
        return v

    def __repr__(self):
        return f"Reaction({self.name!r})"


class Trajectory:
    """The result of a simulation.

    Access a species by name: `traj["mRNA"]` returns its time course as a
    1-D array.  `traj.t` is the time vector.  `traj.y` is the raw
    (n_species, n_times) array in `traj.species` order.
    """

    def __init__(self, t, y, species, model=None):
        self.t = t
        self.y = y
        self.species = list(species)
        self.model = model
        self._index = {s: i for i, s in enumerate(self.species)}

    def __getitem__(self, key):
        if key not in self._index:
            raise KeyError(
                f"No species {key!r}. Available: {', '.join(self.species)}"
            )
        return self.y[self._index[key]]

    def final(self):
        """Concentrations at the last time point, as a dict."""
        return {s: self.y[i, -1] for i, s in enumerate(self.species)}

    def as_dict(self):
        return {s: self.y[i] for i, s in enumerate(self.species)}

    def __repr__(self):
        return (
            f"Trajectory({len(self.species)} species, "
            f"{len(self.t)} time points, t=[{self.t[0]:g}, {self.t[-1]:g}])"
        )


class Model:
    """A reaction network.

    Builds the stoichiometric matrix S once, then evaluates

        dx/dt = S @ v(x, p)

    Parameters
    ----------
    reactions : list of Reaction
    params : dict, optional
        Default parameter values.  Can be overridden per simulation.
    species : list of str, optional
        Fixes the species ordering (and therefore the row order of S).
        If omitted, species are sorted alphabetically so results are
        reproducible.
    """

    def __init__(self, reactions, params=None, species=None):
        self.reactions = list(reactions)
        self.params = dict(params or {})

        found = set()
        for r in self.reactions:
            found |= r.species()
        if species is None:
            self.species = sorted(found)
        else:
            missing = found - set(species)
            if missing:
                raise ValueError(f"Species not listed: {sorted(missing)}")
            self.species = list(species)

        self._index = {s: i for i, s in enumerate(self.species)}
        self.S = self._build_S()

    def _build_S(self):
        """S[i, j] = net stoichiometry of species i in reaction j."""
        S = np.zeros((len(self.species), len(self.reactions)))
        for j, r in enumerate(self.reactions):
            for s, n in r.reactants.items():
                S[self._index[s], j] -= n
            for s, n in r.products.items():
                S[self._index[s], j] += n
        return S

    def fluxes(self, x, p=None):
        """Vector v of reaction velocities at state x (array or dict)."""
        p = {**self.params, **(p or {})}
        c = x if isinstance(x, dict) else dict(zip(self.species, x))
        return np.array([r.flux(c, p) for r in self.reactions])

    def rhs(self, t, x, p=None):
        """Right-hand side dx/dt.  Signature matches solve_ivp."""
        return self.S @ self.fluxes(x, p)

    def _x0_array(self, x0):
        if isinstance(x0, dict):
            unknown = set(x0) - set(self.species)
            if unknown:
                raise ValueError(f"Unknown species in x0: {sorted(unknown)}")
            return np.array([float(x0.get(s, 0.0)) for s in self.species])
        x0 = np.asarray(x0, dtype=float)
        if x0.shape != (len(self.species),):
            raise ValueError(
                f"x0 has length {x0.shape[0]}, expected {len(self.species)} "
                f"({', '.join(self.species)})"
            )
        return x0

    def simulate(self, x0, t_span, params=None, n_points=400, **kwargs):
        """Integrate the system.

        Parameters
        ----------
        x0 : dict or array
            Initial concentrations.  A dict may omit species (they start at 0).
        t_span : (t0, tf)
        params : dict, optional
            Overrides `self.params` for this run only.
        n_points : int
            Number of output times (uniformly spaced).  Pass `t_eval` in
            kwargs to control this directly.
        **kwargs
            Passed straight to `scipy.integrate.solve_ivp`.  Common ones:
            `method="LSODA"` for stiff systems, `rtol`, `atol`.

        Returns
        -------
        Trajectory
        """
        x0 = self._x0_array(x0)
        p = {**self.params, **(params or {})}
        kwargs.setdefault("t_eval", np.linspace(t_span[0], t_span[1], n_points))
        kwargs.setdefault("method", "LSODA")
        kwargs.setdefault("rtol", 1e-8)
        kwargs.setdefault("atol", 1e-10)

        sol = solve_ivp(lambda t, x: self.rhs(t, x, p), t_span, x0, **kwargs)
        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")
        return Trajectory(sol.t, sol.y, self.species, model=self)

    def steady_state(self, x0, params=None, t_max=1e6, **kwargs):
        """Integrate a long time and return the final state as a dict.

        This is the lazy way to find a steady state and it only finds *stable*
        ones — and only the one whose basin contains x0.  Session 8 replaces
        this with actual root-finding, which finds unstable fixed points too.
        """
        traj = self.simulate(x0, (0.0, t_max), params=params,
                             n_points=2, **kwargs)
        return traj.final()

    def summary(self):
        """Human-readable description of the network and its S matrix."""
        lines = [f"Model: {len(self.species)} species, "
                 f"{len(self.reactions)} reactions"]
        lines.append("  species: " + ", ".join(self.species))
        lines.append("  reactions:")
        for j, r in enumerate(self.reactions):
            lines.append(f"    v{j}: {r.name}")
        lines.append("  S =")
        width = max(len(s) for s in self.species)
        header = " " * (width + 3) + " ".join(
            f"{'v'+str(j):>5}" for j in range(len(self.reactions))
        )
        lines.append(header)
        for i, s in enumerate(self.species):
            row = " ".join(f"{self.S[i, j]:5.0f}"
                           for j in range(len(self.reactions)))
            lines.append(f"  {s:>{width}} | {row}")
        return "\n".join(lines)

    def __repr__(self):
        return (f"Model({len(self.species)} species, "
                f"{len(self.reactions)} reactions)")
