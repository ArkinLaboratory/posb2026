"""Tests for posb.logic -- each checks a result derived at the board in session 16.

House rule from 11 October: a gate that re-types the expected value is not a
gate. Every table below is COMPUTED from the gate list, or checked against an
independent definition, never asserted from a literal copied off a slide. The
two exceptions are marked and are the 2025 lecture's own published tables,
which is the point of checking them.
"""
import numpy as np
import pytest

from posb.logic import (
    Gate, NOT, BUF, AND, OR, NAND, NOR, HYBRID,
    GateNetwork, TruthTable, Hazard, hazards,
    classifier_2025, classifier_fixed,
    cascade_step_response, cascade_half_time, cascade_delay,
)


# -- gates -------------------------------------------------------------------

def test_gate_kinds_against_python_operators():
    state = {}
    for a in (False, True):
        for b in (False, True):
            state = {"a": a, "b": b}
            assert NOT("g", "a")(state) == (not a)
            assert BUF("g", "a")(state) == a
            assert AND("g", "a", "b")(state) == (a and b)
            assert OR("g", "a", "b")(state) == (a or b)
            assert NAND("g", "a", "b")(state) == (not (a and b))
            assert NOR("g", "a", "b")(state) == (not (a or b))


def test_hybrid_is_activation_required_repression_dominant():
    g = HYBRID("R3", activators=("A",), repressors=("R",))
    assert g({"A": True, "R": False}) is True
    assert g({"A": True, "R": True}) is False     # repression dominates
    assert g({"A": False, "R": False}) is False   # activation required
    assert g({"A": False, "R": True}) is False


def test_hybrid_without_an_activator_is_refused():
    with pytest.raises(ValueError, match="activation is required"):
        HYBRID("R3", activators=(), repressors=("R",))


def test_undefined_wire_is_refused():
    with pytest.raises(ValueError, match="undefined wire"):
        GateNetwork([NOT("R1", "nowhere")], inputs=("A",))


# -- truth tables ------------------------------------------------------------

def test_truth_table_from_function_and_minterms():
    t = TruthTable.from_function(("A", "B"), lambda a, b: a and not b, name="R3")
    assert t.minterms() == [(True, False)]
    assert t(True, False) is True
    assert t(True, True) is False


def test_truth_table_needs_every_row():
    with pytest.raises(ValueError, match="every input combination"):
        TruthTable(("A", "B"), {(False, False): True})


@pytest.mark.parametrize("fn,name", [
    (lambda a, b: a and not b, "andnotb"),
    (lambda a, b: a != b, "xor"),
    (lambda a, b: a == b, "xnor"),
    (lambda a, b: not (a or b), "nor"),
    (lambda a, b, c: (a and b) or c, "three"),
])
def test_nor_compilation_realises_the_table(fn, name):
    """The compiled network must settle to the table it was compiled from."""
    n_in = fn.__code__.co_argcount
    inputs = ("A", "B", "C")[:n_in]
    spec = TruthTable.from_function(inputs, fn, name=name)
    net = spec.to_nor_network()
    got = net.realised_truth_table()
    assert got.rows == spec.rows


def test_nor_compilation_uses_only_not_nor_and_buf():
    spec = TruthTable.from_function(("A", "B"), lambda a, b: a != b)
    net = spec.to_nor_network()
    assert {g.kind for g in net.gates} <= {"not", "nor", "buf"}


# -- path lengths, the structural diagnostic --------------------------------

def test_classifier_path_lengths_differ_by_one():
    net = classifier_2025()
    assert net.path_lengths("A") == [2]        # A -> R2 -> R3
    assert net.path_lengths("B") == [3]        # B -> R1 -> R2 -> R3
    # each input arrives by a single depth, but the two depths differ, and it
    # is the gate that joins them that sees fresh against stale
    assert net.is_balanced() is False


def test_fixed_classifier_is_balanced():
    net = classifier_fixed()
    assert net.path_lengths("A") == [2]        # A -> R2 -> R3
    assert net.path_lengths("B") == [2]        # B -> Act1 -> R3
    assert net.is_balanced() is True


def test_reconvergent_fork_reports_both_path_lengths():
    # X reaches Z by one gate and by two; the list must show both.
    net = GateNetwork(
        [NOT("Y", "X"), NOR("Z", "X", "Y")], inputs=("X",), output="Z")
    assert net.path_lengths("X") == [1, 2]
    assert net.is_balanced() is False


# -- the circuits both compute the right function once settled ---------------

def test_both_classifiers_compute_a_and_not_b():
    spec = TruthTable.from_function(("A", "B"), lambda a, b: a and not b, name="R3")
    for net in (classifier_2025(), classifier_fixed()):
        assert net.realised_truth_table().rows == spec.rows


# -- hazards -----------------------------------------------------------------

def test_classifier_glitches_in_every_input_case():
    """Computed from the gate list. The 2025 slides tabulate the same four runs."""
    net = classifier_2025()
    found = {}
    for a in (0, 1):
        for b in (0, 1):
            tbl = net.timing_table({"A": a, "B": b}, initial=0, ticks=6)
            hs = hazards(tbl, "R3")
            assert len(hs) == 1, f"expected a hazard at A={a} B={b}"
            found[(a, b)] = hs[0].kind
    # A=1,B=0 is the one case whose settled output is 1, so its glitch is a
    # dynamic hazard -- 0 -> 1 -> 0 -> 1 -- not a static one.
    assert found[(1, 0)] == "dynamic"
    assert found[(0, 0)] == found[(0, 1)] == found[(1, 1)] == "static-0"


def test_classifier_trace_matches_the_2025_lecture_table():
    """The one place a published table is checked literally.

    L13 p.27-28 (2025), R3 column over ticks 0-3, cold start. If this test ever
    fails, either the circuit in `classifier_2025` is wrong or the lecture's
    table is -- do not change the expectation without resolving which.
    """
    net = classifier_2025()
    expected = {(0, 0): [0, 1, 0, 0],
                (0, 1): [0, 1, 0, 0],
                (1, 0): [0, 1, 0, 1],
                (1, 1): [0, 1, 0, 0]}
    for (a, b), want in expected.items():
        tbl = net.timing_table({"A": a, "B": b}, initial=0, ticks=4)
        got = [int(r["R3"]) for r in tbl]
        assert got == want, f"A={a} B={b}: got {got}, lecture says {want}"


def test_the_fix_removes_the_hazard_in_every_case():
    net = classifier_fixed()
    for a in (0, 1):
        for b in (0, 1):
            tbl = net.timing_table({"A": a, "B": b}, initial=0, ticks=8)
            assert hazards(tbl, "R3") == [], f"unexpected glitch at A={a} B={b}"


def test_inserting_a_stage_on_the_shared_tail_only_delays_the_hazard():
    """The 2025 lecture's first repair, and why its own next slide rejects it.

    Act1 = NOT R2 between R2 and R3 lengthens BOTH paths by one, so their
    difference -- which is what causes the glitch -- is unchanged.
    """
    delayed = GateNetwork(
        [NOT("R1", "B"), NAND("R2", "A", "R1"), NOT("Act1", "R2"), BUF("R3", "Act1")],
        inputs=("A", "B"), output="R3")
    base = classifier_2025()
    assert delayed.path_lengths("B")[0] - delayed.path_lengths("A")[0] == \
           base.path_lengths("B")[0] - base.path_lengths("A")[0] == 1
    tbl = delayed.timing_table({"A": 0, "B": 0}, initial=0, ticks=8)
    hs = hazards(tbl, "R3")
    assert len(hs) == 1 and hs[0].kind == "static-0"
    # and it arrives one tick later than in the unrepaired circuit
    base_h = hazards(base.timing_table({"A": 0, "B": 0}, initial=0, ticks=8), "R3")
    assert hs[0].ticks[0] == base_h[0].ticks[0] + 1


def test_balance_alone_does_not_prevent_a_cold_start_glitch():
    """The claim 'equalise the paths and the glitch goes away' is FALSE here.

    Z = NOR(not A, not B) = A AND B is perfectly balanced at depth 2, and it
    still glitches on a cold start, because a NOR gate whose repressors have
    not arrived yet is ON. Balance and fail-safety are independent, and this
    test exists so neither claim can quietly absorb the other.
    """
    net = GateNetwork(
        [NOT("na", "A"), NOT("nb", "B"), NOR("Z", "na", "nb")],
        inputs=("A", "B"), output="Z")
    assert net.is_balanced() is True
    assert net.is_fail_safe() is False          # NOR output: ON when empty
    tbl = net.timing_table({"A": 0, "B": 0}, initial=0, ticks=8)
    hs = hazards(tbl, "Z")
    assert len(hs) == 1 and hs[0].kind == "static-0"


def test_fail_safety_is_a_property_of_the_output_gate():
    assert classifier_2025().is_fail_safe() is False     # R3 = NOT R2
    assert classifier_2025().cold_start_output() is True
    assert classifier_fixed().is_fail_safe() is True     # R3 requires Act1
    assert classifier_fixed().cold_start_output() is False


def test_static_one_hazard_is_named_correctly():
    trace = [{"t": 0, "w": 0}, {"t": 1, "w": 1}, {"t": 2, "w": 0}, {"t": 3, "w": 1}, {"t": 4, "w": 1}]
    hs = hazards(trace, "w", settle=1)
    assert len(hs) == 1 and hs[0].kind == "static-1"


def test_a_clean_single_transition_is_not_a_hazard():
    trace = [{"t": 0, "w": 0}, {"t": 1, "w": 0}, {"t": 2, "w": 1}, {"t": 3, "w": 1}]
    assert hazards(trace, "w", settle=1) == []


# -- latching: the sequential half ------------------------------------------

def test_cross_coupled_nor_pair_has_no_steady_state_and_says_so():
    """Session 9's toggle, named: two NOR gates, each repressing the other.

    With both set and reset low the pair holds whatever it held, so there is no
    single settled value to return and `steady_state` must refuse rather than
    invent one.
    """
    latch = _sr_latch()
    with pytest.raises(RuntimeError, match="latches or oscillates"):
        latch.steady_state({"S": 0, "R": 0}, initial={"Q": 0, "Qbar": 0})


def _sr_latch():
    """The standard cross-coupled NOR pair. S drives the Qbar gate, R the Q gate."""
    return GateNetwork(
        [NOR("Q", "R", "Qbar"), NOR("Qbar", "S", "Q")],
        inputs=("S", "R"), output="Q")


def test_sr_latch_holds_its_state_after_the_set_pulse_is_removed():
    latch = _sr_latch()
    setting = latch.timing_table({"S": 1, "R": 0}, initial={"Q": 0, "Qbar": 1}, ticks=6)
    held = {w: setting[-1][w] for w in ("Q", "Qbar")}
    assert held["Q"] is True and held["Qbar"] is False
    after = latch.timing_table({"S": 0, "R": 0}, initial=held, ticks=8)
    assert all(r["Q"] is True for r in after), "the latch did not hold Q after S was removed"


# -- cascade delay (T41) -----------------------------------------------------

def test_one_stage_response_is_the_session_5_exponential():
    t = np.linspace(0, 5, 41)
    assert np.allclose(cascade_step_response(1, t, tau=1.0), 1 - np.exp(-t))


def test_step_response_matches_the_regularised_gamma():
    from scipy.stats import gamma as gamma_dist
    for n in (1, 2, 3, 5, 9):
        t = np.linspace(0.01, 20, 60)
        assert np.allclose(cascade_step_response(n, t, tau=1.0),
                           gamma_dist.cdf(t, a=n, scale=1.0), atol=1e-12)


def test_step_response_is_monotone_and_bounded():
    for n in (1, 2, 4, 8):
        y = cascade_step_response(n, np.linspace(0, 40, 400), tau=1.0)
        assert np.all(np.diff(y) >= -1e-15)
        assert y[0] == pytest.approx(0.0, abs=1e-12)
        assert y[-1] <= 1.0
        # strictly below 1 while the exponential is still resolvable
        assert float(cascade_step_response(n, 5.0, tau=1.0)) < 1.0


def test_single_stage_half_time_is_tau_ln2():
    assert cascade_half_time(1, tau=1.0) == pytest.approx(np.log(2), rel=1e-10)
    assert cascade_half_time(1, tau=3.0) == pytest.approx(3 * np.log(2), rel=1e-10)


def test_half_time_is_where_the_response_really_is_a_half():
    for n in (1, 2, 3, 7):
        th = cascade_half_time(n, tau=1.0)
        assert float(cascade_step_response(n, th, tau=1.0)) == pytest.approx(0.5, abs=1e-10)


def test_half_time_grows_about_one_lifetime_per_added_stage():
    th = [cascade_half_time(n, tau=1.0) for n in range(1, 9)]
    gaps = np.diff(th)
    assert np.all(gaps > 0.75) and np.all(gaps < 1.0)
    assert np.all(np.diff(gaps) > 0)      # each extra stage costs a little more


def test_half_time_scales_with_tau():
    for n in (1, 3, 6):
        assert cascade_half_time(n, tau=5.0) == pytest.approx(5 * cascade_half_time(n, tau=1.0), rel=1e-9)


def test_cascade_delay_uses_session_10s_convention():
    """t_D = t_half(circuit) - t_half(the simple reference), in lifetimes."""
    for n in (2, 3, 5):
        assert cascade_delay(n, tau=1.0) == pytest.approx(
            cascade_half_time(n, 1.0) - cascade_half_time(1, 1.0), rel=1e-12)
    assert cascade_delay(1, tau=1.0) == pytest.approx(0.0, abs=1e-12)


def test_cascade_delay_is_reported_in_lifetimes_consistently():
    assert cascade_delay(4, tau=2.0) == pytest.approx(2 * cascade_delay(4, tau=1.0), rel=1e-9)


def test_bad_inputs_are_refused():
    with pytest.raises(ValueError):
        cascade_step_response(0, 1.0)
    with pytest.raises(ValueError):
        cascade_step_response(2, -1.0)
    with pytest.raises(ValueError):
        cascade_half_time(2, level=1.0)


# ---------------------------------------------------------------------------
# the cold-start rule, and why it is tested exhaustively
#
# Session 16's engineering result drifted twice. The first version said the
# glitch came from unequal path lengths; a balanced circuit refuted it. The
# repair said "fix the promoter, not the wiring"; the padded circuit refuted
# that. The third version said BOTH conditions are needed -- and that is false
# in both directions, which nothing in this file could see, because the claim
# was prose in a deck and a handout rather than code.
#
# It is code now. These tests fail if anyone restates either overclaim.
# ---------------------------------------------------------------------------

def _all_small_networks(max_gates=3):
    """Every network of up to `max_gates` gates over two free inputs."""
    import itertools
    names = ["g1", "g2", "g3", "g4"][:max_gates]
    ctor = {"not": lambda n, s: NOT(n, s[0]), "buf": lambda n, s: BUF(n, s[0]),
            "nor": lambda n, s: NOR(n, *s), "nand": lambda n, s: NAND(n, *s),
            "hyb": lambda n, s: HYBRID(n, (s[0],), (s[1],))}
    for k in range(2, max_gates + 1):
        gn = names[:k]
        for kinds in itertools.product(ctor, repeat=k):
            pools = [list(("A", "B")) + gn[:i] for i in range(k)]
            choices = []
            for i, kind in enumerate(kinds):
                p = pools[i]
                if kind in ("not", "buf"):
                    choices.append([(s,) for s in p])
                elif kind in ("nor", "nand"):
                    choices.append([tuple(c) for c in itertools.combinations(p, 2)])
                else:
                    choices.append([(x, y) for x in p for y in p if x != y])
            for combo in itertools.product(*choices):
                try:
                    yield GateNetwork(
                        [ctor[kind](gn[i], src)
                         for i, (kind, src) in enumerate(zip(kinds, combo))],
                        inputs=("A", "B"), output=gn[-1])
                except ValueError:
                    continue


def _glitch_count(net, ticks=10):
    return sum(bool(hazards(net.timing_table({"A": a, "B": b},
                                             initial=0, ticks=ticks), net.output))
               for a in (0, 1) for b in (0, 1))


def test_cold_start_rule_is_sound():
    """Nothing cold_start_safe() certifies may glitch. No exceptions allowed.

    This is the whole point: the predicate is permitted to be conservative
    and refuse a circuit that is in fact clean, but a single false positive
    means the rule taught in session 16 is wrong again.
    """
    certified = bad = 0
    for net in _all_small_networks(3):
        if not net.cold_start_safe():
            continue
        certified += 1
        if _glitch_count(net):
            bad += 1
            raise AssertionError(
                f"cold_start_safe() certified a circuit that glitches: "
                f"{[repr(g) for g in net.gates]}")
    assert certified > 1500, f"only {certified} networks certified; sweep broke"
    assert bad == 0


def test_neither_fail_safe_nor_balanced_is_the_rule():
    """The two overclaims the session made, each with its counterexample.

    If someone restores "fail-safe AND balanced is the rule" to the deck, the
    handout, the board notes or PS6, these two circuits are why it is wrong.
    """
    # Fail-safe AND balanced, and it still glitches: the session's own
    # balanced counterexample with the session's own fail-safe repair on it.
    z_buf = GateNetwork([NOT("na", "A"), NOT("nb", "B"), NOR("Z", "na", "nb"),
                         BUF("out", "Z")], inputs=("A", "B"), output="out")
    assert z_buf.is_fail_safe() and z_buf.is_balanced()
    assert _glitch_count(z_buf) == 3, "sufficiency: both conditions hold, 3/4 glitch"
    assert not z_buf.cold_start_safe()

    # Fail-safe, NOT balanced, and clean -- computing the session's own spec.
    two_gene = GateNetwork([BUF("g1", "A"), HYBRID("out", ("g1",), ("B",))],
                           inputs=("A", "B"), output="out")
    assert two_gene.is_fail_safe() and not two_gene.is_balanced()
    assert _glitch_count(two_gene) == 0, "necessity: unbalanced and still clean"
    assert two_gene.cold_start_safe()
    assert (two_gene.realised_truth_table().rows
            == classifier_2025().realised_truth_table().rows)


def test_the_four_session_circuits_agree_with_the_predicate():
    """The table on the slide, as an assertion."""
    z = GateNetwork([NOT("na", "A"), NOT("nb", "B"), NOR("Z", "na", "nb")],
                    inputs=("A", "B"), output="Z")
    padded = GateNetwork([NOT("R1", "B"), NAND("R2", "A", "R1"),
                          NOT("Act", "R2"), BUF("R3", "Act")],
                         inputs=("A", "B"), output="R3")
    for net, safe, n_bad in [(classifier_2025(), False, 4), (z, False, 3),
                             (padded, False, 4), (classifier_fixed(), True, 0)]:
        assert net.cold_start_safe() is safe, repr(net.gates)
        assert _glitch_count(net) == n_bad, repr(net.gates)


def test_the_padded_repair_is_not_static_0_in_all_four():
    """The claim four documents made. (1,0) is dynamic, and has to be.

    If the padded circuit were static-0 in all four cases it would settle to 0
    everywhere and compute the constant 0, not A AND NOT B.
    """
    padded = GateNetwork([NOT("R1", "B"), NAND("R2", "A", "R1"),
                          NOT("Act", "R2"), BUF("R3", "Act")],
                         inputs=("A", "B"), output="R3")
    kinds = {}
    for a in (0, 1):
        for b in (0, 1):
            tbl = padded.timing_table({"A": a, "B": b}, initial=0, ticks=6)
            hz = hazards(tbl, padded.output)
            kinds[(a, b)] = hz[0].kind if hz else "clean"
    assert kinds == {(0, 0): "static-0", (0, 1): "static-0",
                     (1, 0): "dynamic", (1, 1): "static-0"}
    assert (padded.realised_truth_table().rows
            == classifier_2025().realised_truth_table().rows)


def test_static_1_needs_an_input_change_not_a_cold_start():
    """No cold start can produce a static-1, so the taxonomy needs a flip.

    From an all-zero start the output's first move is upward, so it can only
    hold 0 and blip (static-0) or end at 1 having wobbled (dynamic). A
    static-1 requires starting from a settled state and changing an input --
    which is what a digital-design textbook means by a hazard in the first
    place. fig_hazard_types drew one by hand with a trace that starts at 1;
    this is where a real one comes from.
    """
    item3 = GateNetwork([NOT("R1", "A"), NOR("R2", "B", "R1"),
                         NOT("out", "R2")], inputs=("A", "B"), output="out")
    for net in _all_small_networks(3):
        for a in (0, 1):
            for b in (0, 1):
                tbl = net.timing_table({"A": a, "B": b}, initial=0, ticks=10)
                hz = hazards(tbl, net.output)
                assert not hz or hz[0].kind != "static-1", repr(net.gates)

    settled = item3.steady_state({"A": 1, "B": 1}, initial=0)
    start = dict(settled, A=False, B=False)
    tbl = item3.timing_table({"A": 0, "B": 0}, initial=start, ticks=8)
    hz = hazards(tbl, "out", settle=1)
    assert hz and hz[0].kind == "static-1"
    assert [int(r["out"]) for r in tbl][:5] == [1, 1, 0, 1, 1]
