# Session 16 — Combinational and sequential logic

[← all sessions](../README.md) · **Tuesday, October 20, 2026** · Part II opens

> The first session of the engineering half. Session 13 asked what must be true
> of a gene before you may call it a gate; this one wires gates together and
> finds out what a truth table does *not* promise you. Then it gives the circuit
> a memory, and asks where the memory should physically live.

## The one thing to remember

> **A truth table says what the circuit must settle to and nothing about what it
> does on the way. A circuit built from repressors starts with every gate ON, so
> the first answer it gives is the wrong one — and the repair is a promoter that
> requires activation, not a better repressor.**

## The artifacts

**Nielsen et al., *Science* 2016 — Cello** (required; assigned at the end of
session 14 on 13 October, so **the room has read it**). 13 pp. The NOR gate
response functions, the circuit-scoring rule, and the honest numbers: 60
circuits designed, all 60 built with no additional tuning, **45 correct in every
output state**, 92% of 412 output states as predicted, up to 10 regulators and
55 parts (abstract, p. 1). Circuit score S is *"the ratio of the lowest
predicted ON state to the highest predicted OFF state (fig. S26 and eq. S2)"*
(Fig. 2 caption, p. 4) — which is session 13's noise margin written as a ratio.

**Ham, Lee, Keasling & Arkin, *PLoS ONE* 3(7):e2815 (2008)** (not assigned;
shown). The double inversion recombination switch — FimB and Hin, state encoded
in the DNA sequence itself, four states reachable from the *order* of two
inputs, ~1 kb excluding the reporters. And the honest result: the *hin* arm
worked, the *fim* arm did not, and of 50 isolates sequenced none carried the
inverted *fim* orientation.

**Yang et al., *Nat Methods* 11:1261 (2014)** (shown, one slide). 34 integrases
screened, 13 built into switches, **11 perfectly orthogonal**, 1.375 bytes.

**Katalinić et al., *ACS Synth. Biol.* 14(2):363 (2025)** (shown, one slide).
The R64 shufflon as the natural precedent — *rci* plus four DNA segments flanked
by seven *sfx* sites — and 14 new shufflon invertases with orthogonal
SI/*sfx* pairs, aiming at "millions of sequence variants in vivo".

## What happens

Order, not minutes. Four moves per segment — frame, build, release, debrief —
per `docs/lecture-design.md` §5e.

| | |
|---|---|
| **Retrieval** | Loop Q from the midterm: which end did the shortcut change, and why only one? A gate's two thresholds. The toggle's two states. |
| **Truth table → NOR network** | Why NOR is the native biological primitive, derived from session 6's two-operator occupancy rather than asserted. T39. |
| **The classifier, and the glitch** | A AND NOT B, built from repressors. The timing table tick by tick, as a derivation run. T40. |
| **Root cause, and the first repair that fails** | Unequal path lengths; then the activator, which moves the glitch by one tick and does not remove it — and why. |
| **The repair that works** | The hybrid promoter: activation required, repression dominant. The fixed table beside the broken one. |
| **Cascade delay as a number** | Session 10's convention, reused. Theory against Hooshangi's measured cascades. T41. |
| **Cello** | They have read it. The pipeline, the score as a margin, the search; then 45/60 and the 7-segment display. |
| **Memory: the toggle, named** | Session 9's toggle **is** an SR latch. A renaming, not a derivation. Then latches in RPU, registers, the gated D latch. |
| **Memory in DNA** | Ham's DIRS; the honest failure; then the fork — the register road and the program road. |
| **Close** | Hand out Cambray for Thursday. |

## The results this session exists to produce

**The classifier, exactly as 2025 built it** (L13 p. 24). R1 = NOT B;
**R2 = NAND(A, R1)** — one gene read by two independently repressed promoters,
so it is off only when both repressors are present, and the biology picks the
gate; R3 = NOT R2. Settles to A AND NOT B in all four cases.

**The glitch, computed from the gate list** (`posb.logic`, not from the slide).
Cold start, every wire at zero, unit delay per gate. R3 over ticks 0–3:

| A B | R3 trace | hazard |
|---|---|---|
| 0 0 | 0 1 0 0 | static-0 |
| 0 1 | 0 1 0 0 | static-0 |
| 1 0 | 0 1 0 1 | **dynamic** — three transitions where one was due |
| 1 1 | 0 1 0 0 | static-0 |

Those reproduce L13 pp. 27–28 exactly, and a test asserts it: if the circuit in
`classifier_2025` and the lecture's published table ever disagree, the build
fails rather than quietly picking one.

**The wrong explanation, which is taught alongside the right one** (standing
rule, `posb-teaching-derivations` §6). The obvious reading is *unequal path
lengths — A reaches R3 in two gates, B in three — so equalise them.* The path
lengths are real and the diagnosis is wrong: **Z = NOR(NOT A, NOT B) is
perfectly balanced at depth 2 and still glitches on a cold start.** The actual
cause is that a repressor-based gate is ON when its repressor has not arrived,
so an empty circuit is one with every inverter switched on, and that false ON
propagates while the circuit fills. `is_balanced` and `is_fail_safe` are
separate checks in `posb.logic` and a test forbids either from absorbing the
other.

**Why the 2025 repair works, which is not what the slide says.** Inserting an
activator between R2 and R3 lengthens both paths equally, so it moves the glitch
one tick later and nothing else — verified. The repair that works replaces R1
with an activator and gives R3 a **hybrid promoter: activation required,
repression dominant**. The empty circuit then presents 0, so the output can only
rise when the real answer arrives. No glitch in any of the four cases.
**For a therapeutic actuator the fail-safe state must be the empty state**,
which is the engineering consequence this session exists for.

**Cascade delay (T41).** For n identical first-order stages after a step,
y_n(t) = 1 − e^(−t/τ) Σ_{k<n} (t/τ)^k/k!. Half-times in lifetimes: **0.693,
1.678, 2.674, 3.672, 4.671** for n = 1…5 — each extra stage costs very nearly
one lifetime, and **t_half ≈ (n − ⅓)τ** is good to 0.008τ by n = 3. Hooshangi's
measured cascades are slower than that (s13 quoted the room circuit 1 settling
by 120 min against circuit 3 starting at 140), and their paper names why: the
delay also carries *"protein decay, protein production, and repression
thresholds"* (p. 3585) — a repressor must clear threshold before the next stage
moves. The gap between the clean theory and the measurement is the debrief.

⚠ **Hooshangi's half-time is not session 10's.** They take *"the time required
for the cells to cross the halfway point between the low and high levels based
on a logarithmic scale, which is the geometric mean of the two"* (p. 3583);
session 10's convention is 50% of the steady state on linear axes. Say so when
the two are put side by side.

**Memory, and the fork.** Protein-state memory dies with the cell; DNA-
orientation memory does not. The register road: unidirectional serine
integrases: 34 found in prophage genomes, 13 selected to be at most 60%
identical and built, 11 of those perfectly orthogonal — 1.375 bytes. The
34 → 13 step is a selection, not a failure rate, so this is not the
"one-in-three attrition" an earlier draft claimed; the shared limit with
Cello is that EVERY pair has to be orthogonal, not that a third of parts
survive. The program road:
if the inversion reconstitutes a promoter–gene–terminator arrangement then the
state *is* the expression program, there is no decoding step, and the natural
precedent is R64's four segments and seven *sfx* sites making PilV variants.
Closing line: **the compact state space is real, and it was never going to be
read — it was going to be selected on.**

## Coverage

**T39** (truth table → circuit, HAND), **T40** (hazard identification and the
complete timing table, AUTO — and **on the final**), **T41** (cascade delay
estimation, AUTO). All three assessed on **PS6**, which posts the same day.
Recombinase memory is named here and modelled in **S18**, where T47 lives.

## New in `posb` — `posb.logic`

`TruthTable` (`from_function`, `minterms`, `to_nor_network`), `Gate` with
`hybrid` promoters, `GateNetwork` (`timing_table`, `steady_state`,
`path_lengths`, `is_balanced`, `cold_start_output`, `is_fail_safe`,
`realised_truth_table`), `hazards` returning static-0 / static-1 / dynamic,
`classifier_2025`, `classifier_fixed`, and `cascade_step_response`,
`cascade_half_time`, `cascade_delay`. **36 tests**, run in the cloud container
(the device shell has no scipy). The tests compute every table from the gate
list; the one literal expectation is the 2025 lecture's own published trace,
and it is labelled as such.

## Built

| | |
|---|---|
| Figures | 17 PNGs from `figures/s16_logic.py`, all verifying: the three architectures (`s16_arch_nor`, `s16_arch_nand`, `s16_universal`), the Cello gate (`s16_voigt_nor`), the two XNOR realisations (`s16_xnor_two_ways`), the classifier and its tick tables (`s16_classifier`, `s16_timing_p1..p4`, `s16_timing_broken`, `s16_timing_fixed`), the two counterexamples (`s16_cold_start`, `s16_two_conditions`), `s16_hazard_types`, `s16_cascade_delay`, the inversion and site layouts (`s16_inversion`), and the latch (`s16_sr_circuit`, `s16_dirs_states`, `s16_latch_state_table`) |
| Paper figures | Nielsen Fig. 1A, 2A, 2C, 2E, 5A; Hooshangi Fig. 1 and 3A — all declared in `decks/paper_figures.yaml`, the Fig. 2 panels as crops of the parent |
| Movie | `private/paper-movies/der2016_cello_hillclimb.mp4` — Bryan Der's search animations from PoSB 2025 Lecture 18, recomposed so the axis labels survive. `der2016_cello_greedy_dfs.mp4` is built but not placed. |
| Deck | `decks/s16_logic.py` → 62 slides, **5 hidden** (`reading-why`, `nor-library`, `delay-ask`, `cello-frame`, `dna-count`): in the file, skipped in the room |
| Handout + answers | `handouts/s16-logic.md` + `-answers.md`, both built to PDF |
| Board notes | `board-notes/s16-board-notes.md`, built to PDF. Anchored to segment names rather than minutes, because this deck prints no timings. |
| Problem set | `private/sources/ps06.py` → `problem-sets/ps06-noise-logic/ps06.ipynb`. 48 points, 56 for 247. Covers T17, T31–T41; T42–T44 moved to PS7. |

Every table in those figures is computed by `posb.logic` at render time; none
of the ticks is typed into the figure source. `fig_classifier` asserts the
circuit really computes A AND NOT B, `fig_timing_steps` asserts the hazard is
the kind the caption names, `fig_cold_start` asserts the balanced circuit is
*not* fail-safe, and `fig_timing_fixed` asserts the repair is clean in all
four input cases. A figure that stops being true stops building.

Design and decisions: [DESIGN.md](DESIGN.md).
