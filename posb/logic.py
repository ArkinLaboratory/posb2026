"""
posb.logic — truth tables, gate networks, timing tables and hazards.

Introduced in Session 16. You fill a timing table in by hand in class first,
one tick per row, and find the glitch with your own eyes; this is the same
bookkeeping made reusable.

What a timing table is, and what it is not
------------------------------------------
A truth table is a *contract*: for each combination of inputs, what the output
must be once everything has settled. It says nothing about *when*. A timing
table is the other half — the value on every wire at every tick while the
circuit is settling.

The model here is the simplest one that shows the effect: **synchronous
unit delay**. Every gate reads its inputs as they were at tick t and presents
its own output at tick t+1. One gate, one tick. Real promoters are not
synchronous and their delays are not equal, which makes the effect below worse
rather than better -- see `cascade_half_time` for the continuous version with
real lifetimes.

Where the wrong answer comes from
---------------------------------
This is session 14's Loop P / Loop Q question in Boolean form. There, two
paths from one input reconverged having taken different amounts of time, and
the output's shape showed it. Here the same fork is discrete, and a transient
wrong answer is called a **hazard**. Three kinds, named for what the output
was supposed to do:

    static-0   should hold 0, momentarily goes to 1
    static-1   should hold 1, momentarily goes to 0
    dynamic    should change once, changes three or more times

Two different things cause one, and **in a cell it is the second that
matters** -- which is the opposite of the electronics case, so it is worth
separating them.

**1. Unequal path lengths, on an input change.** If two paths from one input
reconverge at a gate after a different number of stages, the gate sees a
stale value on one leg and a fresh one on the other, and for as many ticks as
the difference it computes its function of a combination that never exists in
the steady state. `path_lengths` and `is_balanced` are the diagnostics, and
they tell you before you simulate.

**2. Cold start, which is how a cell actually meets a circuit.** A circuit
delivered into a cell begins with every protein at zero -- not at a settled
state. For the first few ticks every gate is computing its function of
*initial* values rather than of the inputs, and the output is whatever that
produces. Equal path lengths do **not** save you here: a balanced network
whose output gate is a NOR still reads 1 while its inputs are still absent,
because **a repressor-based gate is ON when its repressor has not arrived
yet.** The empty circuit is a circuit with every inverter switched on.

The fix for (2) is the promoter architecture, not the wiring:

    make the output gate REQUIRE an activator, so the empty state is OFF.

`is_fail_safe` checks exactly that -- it evaluates the output gate with every
wire at zero and asks whether the answer is 0. For a therapeutic actuator
this is the whole game: a classifier that transiently fires while it is still
filling has already killed the cell it was deciding about.

`classifier_2025` fails (2) and `classifier_fixed` passes it; both are
balanced-or-not as `is_balanced` reports, and the two properties are
independent. Do not conflate them.

The worked circuit (session 16's spine)
----------------------------------------
The two-input cancer-cell classifier, R3 = A AND NOT B, built from repressors:

    R1 = NOT B                      B -| R1
    R2 = NAND(A, R1)                A -| R2,  R1 -| R2   (two promoters, summed)
    R3 = NOT R2                     R2 -| R3

R2 is one gene read by two independently repressed promoters, so it is ON
unless *both* repressors are present -- that is NAND, not NOR, and it is worth
saying out loud because the sum of two repressions is the one place in this
course where the biology picks the gate for you.

Path lengths to R3:  A -> R2 -> R3 is 2;  B -> R1 -> R2 -> R3 is 3.
They differ by one, so the circuit glitches for one tick in every input case.

The 2025 lecture's first repair inserts an activator between R2 and R3, and
its own next slide admits the hazard is only *delayed* -- correctly, because
inserting a stage on the shared tail changes both path lengths equally and so
changes nothing about their difference. The repair that works replaces R1 with
an activator and gives R3 a hybrid promoter (activation required, repression
dominant):

    Act1 = NOT B                    R2 = NOT A                R3 = Act1 AND NOT R2

Now A -> R2 -> R3 is 2 and B -> Act1 -> R3 is 2. Equal, and the glitch is gone
in all four input cases. `hybrid` is one promoter and therefore one tick; that
is the whole reason the fix works, and modelling it as AND-of-NOT across two
ticks would hide it.

Plain Python and NumPy. Read the source.
"""

from itertools import product

import numpy as np

__all__ = [
    "Gate", "NOT", "BUF", "AND", "OR", "NAND", "NOR", "HYBRID",
    "GateNetwork", "TruthTable", "Hazard", "hazards",
    "classifier_2025", "classifier_fixed",
    "cascade_step_response", "cascade_half_time", "cascade_delay",
]


# ---------------------------------------------------------------------------
# gates
# ---------------------------------------------------------------------------

_KINDS = {
    "buf":  lambda v: bool(v[0]),
    "not":  lambda v: not v[0],
    "and":  lambda v: all(v),
    "or":   lambda v: any(v),
    "nand": lambda v: not all(v),
    "nor":  lambda v: not any(v),
}


class Gate:
    """One gene, driven by its promoter(s). One gate costs one tick.

    `kind` is one of buf, not, and, or, nand, nor, hybrid. A hybrid gate takes
    `activators` and `repressors` separately and computes

        output = (any activator present) AND NOT (any repressor present)

    which is the promoter architecture of session 16's repair: activation
    required, repression dominant over activation.
    """

    def __init__(self, name, kind, inputs=(), activators=(), repressors=()):
        kind = kind.lower()
        if kind == "hybrid":
            if inputs:
                raise ValueError("a hybrid gate takes activators and repressors, not inputs")
            if not activators:
                raise ValueError(f"hybrid gate {name!r}: activation is required, so give at least one activator")
            self.activators = tuple(activators)
            self.repressors = tuple(repressors)
            self.inputs = self.activators + self.repressors
        else:
            if kind not in _KINDS:
                raise ValueError(f"unknown gate kind {kind!r}; have {sorted(_KINDS) + ['hybrid']}")
            if activators or repressors:
                raise ValueError("activators/repressors are for hybrid gates only")
            self.inputs = tuple(inputs)
            if not self.inputs:
                raise ValueError(f"gate {name!r} has no inputs")
            if kind in ("buf", "not") and len(self.inputs) != 1:
                raise ValueError(f"{kind} takes exactly one input, got {len(self.inputs)}")
            self.activators = ()
            self.repressors = ()
        self.name = name
        self.kind = kind

    def __call__(self, state):
        """Evaluate from a dict of wire -> bool, as of the PREVIOUS tick."""
        if self.kind == "hybrid":
            on = any(bool(state[w]) for w in self.activators)
            off = any(bool(state[w]) for w in self.repressors)
            return on and not off
        return bool(_KINDS[self.kind](tuple(bool(state[w]) for w in self.inputs)))

    def __repr__(self):
        if self.kind == "hybrid":
            return (f"Gate({self.name!r}, 'hybrid', activators={list(self.activators)}, "
                    f"repressors={list(self.repressors)})")
        return f"Gate({self.name!r}, {self.kind!r}, inputs={list(self.inputs)})"


def BUF(name, x):          return Gate(name, "buf", (x,))
def NOT(name, x):          return Gate(name, "not", (x,))
def AND(name, *xs):        return Gate(name, "and", xs)
def OR(name, *xs):         return Gate(name, "or", xs)
def NAND(name, *xs):       return Gate(name, "nand", xs)
def NOR(name, *xs):        return Gate(name, "nor", xs)
def HYBRID(name, activators, repressors=()):
    return Gate(name, "hybrid", activators=activators, repressors=repressors)


# ---------------------------------------------------------------------------
# networks
# ---------------------------------------------------------------------------

class GateNetwork:
    """A set of gates over named wires, plus the names of the free inputs.

    Evaluation is synchronous: every gate reads tick t and writes tick t+1.
    """

    def __init__(self, gates, inputs, output=None):
        self.gates = list(gates)
        self.inputs = tuple(inputs)
        names = [g.name for g in self.gates]
        if len(set(names)) != len(names):
            raise ValueError("two gates share a name")
        if set(names) & set(self.inputs):
            raise ValueError("a gate and a free input share a name")
        self.by_name = {g.name: g for g in self.gates}
        known = set(names) | set(self.inputs)
        for g in self.gates:
            missing = [w for w in g.inputs if w not in known]
            if missing:
                raise ValueError(f"gate {g.name!r} reads undefined wire(s) {missing}")
        self.output = output if output is not None else names[-1]
        if self.output not in names:
            raise ValueError(f"output {self.output!r} is not a gate in this network")
        self.wires = tuple(self.inputs) + tuple(names)

    # -- structure ---------------------------------------------------------
    def path_lengths(self, src, dst=None):
        """Every path length in gates from `src` to `dst`, as a sorted list.

        This is the diagnostic. If the lengths to a reconvergence point are not
        all equal, the circuit has a hazard, and you know it without simulating.
        """
        dst = self.output if dst is None else dst
        out = []

        def walk(node, depth, seen):
            if node == src:
                out.append(depth)
                return
            if node in self.inputs or node in seen:
                return
            for w in self.by_name[node].inputs:
                walk(w, depth + 1, seen | {node})

        walk(dst, 0, frozenset())
        return sorted(out)

    def is_balanced(self, dst=None):
        """True if EVERY path from ANY input to `dst` has the same length.

        Note the quantifier. It is not enough for each input separately to
        arrive by a single depth: if A arrives in two gates and B in three,
        the gate that joins them is mixing a fresh value with a stale one,
        and that is the imbalance that matters.
        """
        lengths = set()
        for i in self.inputs:
            lengths |= set(self.path_lengths(i, dst))
        return len(lengths) <= 1

    def cold_start_output(self, dst=None):
        """What the output gate presents when every wire is still at zero.

        This is the value the circuit shows on its first tick after being
        delivered into a cell, before any input has reached it.
        """
        dst = self.output if dst is None else dst
        empty = {w: False for w in self.wires}
        return self.by_name[dst](empty)

    def is_fail_safe(self, dst=None):
        """True if the empty circuit presents 0 -- the actuator is OFF at start.

        A NOT or NOR output gate is never fail-safe: with no repressor present
        it is ON. A hybrid promoter that requires activation always is.
        """
        return self.cold_start_output(dst) is False

    # -- behaviour ---------------------------------------------------------
    def step(self, state):
        nxt = {w: state[w] for w in self.inputs}
        for g in self.gates:
            nxt[g.name] = g(state)
        return nxt

    def timing_table(self, assignment, initial=0, ticks=6):
        """Tick-by-tick values of every wire, as a list of dicts.

        `assignment` fixes the free inputs and holds them for the whole run.
        `initial` is the starting value of every gate wire -- 0 by default,
        which is the cold-start the session-16 slides tabulate. Pass a dict to
        start from a particular state (that is how you examine an input change
        rather than a start-up).
        """
        missing = [i for i in self.inputs if i not in assignment]
        if missing:
            raise ValueError(f"no value given for input(s) {missing}")
        state = {w: bool(assignment[w]) for w in self.inputs}
        if isinstance(initial, dict):
            for g in self.gates:
                state[g.name] = bool(initial.get(g.name, False))
        else:
            for g in self.gates:
                state[g.name] = bool(initial)
        rows = [dict(state, t=0)]
        for t in range(1, ticks):
            state = self.step(state)
            rows.append(dict(state, t=t))
        return rows

    def steady_state(self, assignment, initial=0, max_ticks=64):
        """Settle the circuit and return the final state.

        Raises if it does not settle -- a network that latches or oscillates
        has no single steady state, and session 16's second half is about
        exactly those.
        """
        rows = self.timing_table(assignment, initial=initial, ticks=max_ticks)
        last, prev = rows[-1], rows[-2]
        if any(last[w] != prev[w] for w in self.wires):
            raise RuntimeError(
                f"network did not settle within {max_ticks} ticks for {assignment} -- "
                "it latches or oscillates, so it has no steady state")
        return {w: last[w] for w in self.wires}

    def realised_truth_table(self, initial=0, max_ticks=64):
        """What the circuit actually computes once settled, as a TruthTable."""
        rows = {}
        for combo in product((False, True), repeat=len(self.inputs)):
            a = dict(zip(self.inputs, combo))
            rows[combo] = self.steady_state(a, initial=initial, max_ticks=max_ticks)[self.output]
        return TruthTable(self.inputs, rows, name=self.output)


# ---------------------------------------------------------------------------
# truth tables
# ---------------------------------------------------------------------------

class TruthTable:
    """The contract: inputs -> required output, once settled."""

    def __init__(self, inputs, rows, name="out"):
        self.inputs = tuple(inputs)
        self.name = name
        self.rows = {tuple(bool(v) for v in k): bool(v) for k, v in rows.items()}
        expected = set(product((False, True), repeat=len(self.inputs)))
        if set(self.rows) != expected:
            raise ValueError("a truth table must give every input combination exactly once")

    @classmethod
    def from_function(cls, inputs, fn, name="out"):
        inputs = tuple(inputs)
        rows = {c: bool(fn(*c)) for c in product((False, True), repeat=len(inputs))}
        return cls(inputs, rows, name=name)

    def __call__(self, *values):
        return self.rows[tuple(bool(v) for v in values)]

    def __eq__(self, other):
        return (isinstance(other, TruthTable)
                and self.inputs == other.inputs
                and self.rows == other.rows)

    def minterms(self):
        """Input combinations for which the output is 1."""
        return [c for c, v in sorted(self.rows.items()) if v]

    def to_nor_network(self, prefix="g"):
        """Compile to a NOT/NOR network, the Cello constraint.

        Sum of products, then DeMorgan twice. Each minterm becomes one NOR over
        the complemented literals; the OR of the minterms becomes a NOR of them
        followed by a NOT. Deliberately NOT minimised -- minimisation is the
        2025 course's L17/L18 and is cut. What matters here is that a table can
        always be realised, and that the realisation has a depth you can read.
        """
        gates, inv = [], {}
        for w in self.inputs:
            inv[w] = f"{prefix}_not_{w}"
            gates.append(NOT(inv[w], w))
        ms = self.minterms()
        if not ms:
            raise ValueError("output is never 1; nothing to build")
        term_names = []
        for i, combo in enumerate(ms):
            # minterm = AND of literals = NOR of their complements
            legs = [(w if not v else inv[w]) for w, v in zip(self.inputs, combo)]
            nm = f"{prefix}_m{i}"
            gates.append(NOR(nm, *legs))
            term_names.append(nm)
        if len(term_names) == 1:
            out = f"{prefix}_{self.name}"
            gates.append(BUF(out, term_names[0]))
        else:
            nor_all = f"{prefix}_nor"
            gates.append(NOR(nor_all, *term_names))
            out = f"{prefix}_{self.name}"
            gates.append(NOT(out, nor_all))
        return GateNetwork(gates, self.inputs, output=out)

    def __str__(self):
        head = "  ".join(self.inputs) + f"  | {self.name}"
        lines = [head, "-" * len(head)]
        for c, v in sorted(self.rows.items()):
            lines.append("  ".join(str(int(x)) for x in c) + f"  | {int(v)}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# hazards
# ---------------------------------------------------------------------------

class Hazard:
    """A transient wrong answer on one wire."""

    def __init__(self, wire, kind, ticks, trace):
        self.wire, self.kind, self.ticks, self.trace = wire, kind, tuple(ticks), tuple(trace)

    def __repr__(self):
        return f"Hazard(wire={self.wire!r}, kind={self.kind!r}, ticks={list(self.ticks)})"

    def __eq__(self, other):
        return (isinstance(other, Hazard) and self.wire == other.wire
                and self.kind == other.kind and self.ticks == other.ticks)


def hazards(table, wire, settle=0):
    """Find hazards on `wire` in a timing table.

    `settle` is how many leading ticks to ignore. The default of 0 is right
    for a cold start, where tick 0 is the empty circuit and every excursion
    after it counts. Pass settle=1 or more when the table begins from an
    already-settled state and the opening tick is the input arriving.

    Returns a list with zero or one Hazard. The kind is decided by what the
    wire was supposed to do between its first counted value and its last:

        start == end, excursion present     -> static-0 / static-1
        start != end, more than one change  -> dynamic
    """
    trace = [bool(r[wire]) for r in table]
    if len(trace) < settle + 2:
        raise ValueError("timing table is too short to judge")
    seg = trace[settle:]
    start, end = seg[0], seg[-1]
    changes = sum(1 for a, b in zip(seg, seg[1:]) if a != b)
    ticks = [table[settle + i]["t"] for i, (a, b) in enumerate(zip(seg, seg[1:])) if a != b]
    if start == end:
        if changes == 0:
            return []
        return [Hazard(wire, "static-1" if start else "static-0", ticks, trace)]
    if changes > 1:
        return [Hazard(wire, "dynamic", ticks, trace)]
    return []


# ---------------------------------------------------------------------------
# the session-16 circuits
# ---------------------------------------------------------------------------

def classifier_2025():
    """The 2025 lecture's two-input classifier, R3 = A AND NOT B. It glitches.

    R1 = NOT B; R2 = NAND(A, R1) -- one gene, two independently repressed
    promoters, so it is off only when both repressors are present; R3 = NOT R2.
    """
    return GateNetwork(
        [NOT("R1", "B"), NAND("R2", "A", "R1"), NOT("R3", "R2")],
        inputs=("A", "B"), output="R3")


def classifier_fixed():
    """The repair that works. Two changes, and the second is the one that counts.

    Act1 = NOT B (an activator now); R2 = NOT A; R3 is one promoter that
    requires Act1 and is dominated by R2.

    Both inputs now reach R3 in two gates, so the network is balanced -- but
    that is not why the glitch is gone. It is gone because R3 requires
    activation, so the empty circuit presents 0 and the output can only rise
    when the real answer arrives. See `is_fail_safe`.
    """
    return GateNetwork(
        [NOT("Act1", "B"), NOT("R2", "A"),
         HYBRID("R3", activators=("Act1",), repressors=("R2",))],
        inputs=("A", "B"), output="R3")


# ---------------------------------------------------------------------------
# cascade delay, in continuous time (T41)
# ---------------------------------------------------------------------------

def cascade_step_response(n, t, tau=1.0):
    """Output of an n-stage first-order cascade at time t after a unit step.

    Each stage relaxes with lifetime tau towards the stage before it. Solving
    the chain for a step at t = 0 from rest gives the normalised output

        y_n(t) = 1 - e^{-t/tau} * sum_{k=0}^{n-1} (t/tau)^k / k!

    which is the regularised gamma function. n = 1 is the single exponential
    from session 5.
    """
    n = int(n)
    if n < 1:
        raise ValueError("need at least one stage")
    t = np.asarray(t, dtype=float)
    if np.any(t < 0):
        raise ValueError("t must be non-negative")
    u = t / float(tau)
    term = np.ones_like(u)
    acc = np.ones_like(u)
    for k in range(1, n):
        term = term * u / k
        acc = acc + term
    return 1.0 - np.exp(-u) * acc


def cascade_half_time(n, tau=1.0, level=0.5):
    """Time for an n-stage cascade to reach `level` of its steady state.

    Session 10's convention, unchanged: the response time is the time to reach
    half of the final value. Solved numerically -- there is no closed form for
    n > 1, which is itself worth saying in class.
    """
    from scipy.optimize import brentq
    if not 0.0 < level < 1.0:
        raise ValueError("level must be strictly between 0 and 1")
    n = int(n)
    f = lambda t: float(cascade_step_response(n, t, tau)) - level
    hi = tau
    while f(hi) < 0.0:
        hi *= 2.0
        if hi > 1e6 * tau:
            raise RuntimeError("could not bracket the half time")
    return brentq(f, 0.0, hi, xtol=1e-12, rtol=8.9e-16)


def cascade_delay(n, tau=1.0, reference=1, level=0.5):
    """Delay a cascade adds, against a `reference`-stage circuit.

    Session 10's T25 convention applied to a chain:

        t_D = t_half(n stages) - t_half(reference stages)

    reported in the same lifetimes. With the default reference of one stage,
    this is "how much later than simple regulation".
    """
    return cascade_half_time(n, tau, level) - cascade_half_time(reference, tau, level)
