# Session 16 — Combinational and sequential logic

**Design, for approval before build.** Tuesday 20 October 2026. Written 18
October after your rulings on PS6 scope, the triage correction, and the
recombinase paper. Build starts when you sign this off; nothing is built
against an unsettled design.

---

## 0 · Two corrections to this morning's handoff

**The Cello paper WAS assigned, and you are right.** `HANDOFF-2026-10-18.md` §2
says it never went out because class 15 was the exam. That is wrong, and the
repo says so in two places: `SESSION-LOG.md:850` — *"it assigns Nielsen at the
end of **session 14**, not the midterm, so nothing is handed out at the end of
an exam"* — and `decks/s14_review.py:657-663`, a slide headed **"The reading
for 20 October"** with the speaker note *"The Cello paper is for session 16 and
the obligation lands on this deck only because the midterm sits between."*
`build_readings.py` placed it there deliberately on 26 September.

**So Tuesday is built for a room that has read Nielsen.** That reverses the
handoff's instruction to make the Cello material land on what is shown rather
than on what was read. It also removes the only slack I had identified in the
week, and it means the Cello segment can ask them to *use* the paper rather
than be shown it. §2 of the handoff gets struck; the structural note in it —
that a session after an exam cannot have its reading assigned at the end of
class N−1 — was never the live problem it claimed to be, because the builder
already solved it. I will correct the handoff in place.

**Triage understates the supply, not just misroutes it.** My brief said L09 +
L10 contain nothing for S16, which is true, and that about 68 usable pages
exist across L13/L16/L18/L21. With the 2024 recombinase deck in scope that
rises to roughly **90 pages**, and the sequential half is far better supplied
than the brief said. Details in §3.

---

## 1 · Are we building up properly? Yes — and the ramp is shorter than it looks

You thought the timing tables so far only tee this up. That is exactly right,
and it is worth being precise about what the room already owns, because it
makes Tuesday's genuinely new content narrow.

| they already have | where | what it gives Tuesday |
|---|---|---|
| **A delay measured with a stated convention** — response time = time for Z to reach 50% of steady state; t_D = t_half(FFL) − t_half(simple), per direction | **T25, session 10**; the convention is printed on the s10 handout; **PS5 Q2 graded it**, 4+2+2+2 points | They can already put a number on a delay. T41 is not a new idea, it is the same measurement applied to a chain. |
| **Per-stage delay, measured in a real cascade** | **S13**, Hooshangi 2005 Fig. 3A; Hill coefficients 2.3 → 7.0 → 7.5 over one, two and three stages (p. 3583) | The number for T41 comes from a paper they have read, not from an invented unit delay. |
| **Unequal path delays through a reconvergent fork change the output's shape** | **s14 practice item 5** and **midterm B2.1**: Loop P the cascade is *late at both ends, symmetrically*; Loop Q with a shortcut and an OR gate is late at **one** end only | **This is the hazard mechanism, in analog form.** They have already reasoned about two paths of different length meeting at one gate. |
| **The toggle, in the phase plane: two stable states, a separatrix, which side a perturbation lands on** | S9; rebuilt into s14 with the `s14_basins` figure and practice item 4 | The SR latch is a *renaming*, not a derivation. |
| **What makes a gate digital** — transfer curve, gain, thresholds, noise margins, whether B can read A | S13, with Cello's own Table S4 gates through `posb.digital` | "Signal separation" in Nielsen is their own margin, in their own units. |

**So what is actually new on Tuesday:** (a) discretizing a circuit to Boolean
values and ticks; (b) the tick-by-tick table as an object; (c) the hazard
taxonomy — static-1, static-0, dynamic — and that a hazard is a transient
through a value *neither* steady state has; (d) the fix living in the wiring
rather than the parts; (e) memory held in DNA rather than in protein state.

Everything else is a renaming of something they own. **That is the slack in
this week**, and it is why the session can afford to be tutorial.

**The bridge sentence**, which I would put on the frame slide verbatim:

> On the midterm you drew a loop whose shortcut made it late at one end and not
> the other. Today the same fork is Boolean and the clock ticks — and the thing
> that was a *shape* becomes a *wrong answer the circuit gives on the way to
> the right one*.

---

## 2 · The arc (order, not minutes)

Four moves per segment, `docs/lecture-design.md` §5e. Every RELEASE is on a
different object from the worked one and every DEBRIEF is illustrated and
immediate.

**R · Retrieval (3 items).** Loop Q from the midterm — which end did the
shortcut change, and why only one? A gate's two thresholds. The toggle's two
states.

**Segment 1 — combinational: from a truth table to a circuit made of NOR.** (T39)
- FRAME: the specification problem in its logic form. A truth table is a
  *contract*; a circuit is an *implementation*; nothing in the contract says
  when. Drawn: a two-input table beside an empty circuit box.
- BUILD: why NOR is the native biological primitive — one promoter, two
  operators, repression is the default mechanism (straight back to S6's
  promoter occupancy, where they derived exactly this rate law). Derive the
  NOR response from the two-operator occupancy they already have, rather than
  asserting it. Then truth table → NOR network, one move at a time.
- RELEASE: a different table (XNOR, or a 3-input), build the network.
- DEBRIEF: the worked network, drawn.

**Segment 2 — the classifier, and the glitch.** (T40, the spine)
- FRAME: the real design problem — detect A HIGH and B LOW, a cancer-cell
  profile match. The circuit, drawn, with its intended truth table.
- BUILD: **the timing table, tick by tick**, as a derivation run — one row per
  tick, the table growing beside the circuit. R3 goes to 1 when it must not.
  Name it: a **static-0 hazard**. Then the root cause, stated as the general
  rule: *two paths from the same input reconverge at one gate with different
  numbers of stages.* Point back at Loop Q explicitly.
- RELEASE: a different circuit, their turn, complete the table and say whether
  it glitches and of which kind.
- DEBRIEF: the completed table, the glitch circled.

**Segment 3 — fixing it, and why the first fix fails.** (T40 cont.)
- FRAME: three candidate fixes, named.
- BUILD: the activator route (it moves the hazard, it does not remove it — and
  the 2025 deck's own next slide admits this); then the hybrid promoter with
  NOT(NOT X), activation required and repression dominant; the fixed timing
  table beside the broken one.
- DEBRIEF: *what would still break this* — if activation and repression
  dynamics differ, the fix is only as good as the matching. This is the
  honest ending and it is already the 2025 deck's discussion slide; it becomes
  a shown answer rather than an open question.

**Segment 4 — cascade delay as a number.** (T41)
- FRAME: how late is late? The question in the form PS6 will ask it.
- BUILD: activation vs repression cascades; sum of per-stage response times;
  then the measured version — Hooshangi's three cascades, and the delay read
  off Fig. 3A. The convention is **S10's**, reused verbatim, not a new one.
- RELEASE: estimate the delay of a four-stage chain from a per-stage number.
- DEBRIEF: the arithmetic, shown.

**Segment 5 — Cello, which they have read.** (no new technique row)
- FRAME: they have the paper. The question is not what it does but **what its
  number means**: 60 designed, all 60 built, **45 correct in every output
  state**, 92% of 412 output states as predicted, up to 10 regulators and 55
  parts (Nielsen 2016, abstract and p. 1; the 13-page PDF is in
  `private/readings/`).
- BUILD: the pipeline (Verilog → logic synthesis → gate assignment →
  performance prediction); the **circuit score** S = *"the ratio of the lowest
  predicted ON state to the highest predicted OFF state (fig. S26 and eq. S2)"*
  (Fig. 2 caption, p. 4) — and the point that **this is their noise margin from
  session 13, written as a ratio**. The assignment problem growing faster than
  exponentially; why search is needed.
- RELEASE: given two gates from Table S4, say whether the assignment scores
  well — they did this computation in S13 with `posb.digital`.
- DEBRIEF: then the showpiece — the 7-segment digit display, 68 kb, 62
  transcription factors — and the honest reading of 45/60: *the compiler is not
  the bottleneck; the gate library is.* Forward pointer to Stanton and Thursday.

**Segment 6 — sequential: memory.**
- FRAME: combinational vs sequential, drawn (output depends on inputs / output
  depends on inputs **and history**).
- BUILD (a): **session 9's toggle is an SR latch.** Say it in those words. Take
  the phase plane they own and write the state table beside it — the two stable
  states are Q and Q̄; SET and RESET are the inducer pulses they already
  analysed in PS4 and on the midterm. This is a renaming and should be
  presented as one. Then the measured version: SR latches in RPU, 31 of 41
  functional; registers; the gated D latch.
- BUILD (b): **non-volatile memory — Ham et al. 2008.** Protein-state memory
  dies with the cell; DNA-orientation memory does not. The double inversion
  recombination switch: two overlapping invertase systems, **FimB** and **Hin**,
  each flipping a segment between inverted repeats, so **the state is the
  sequence itself**. Four states reachable from the order of two inputs — the
  circuit remembers not just *that* inputs arrived but *in what order*. ~1 kb
  excluding the reporters. And the honest result, which is why it belongs in
  this course: *proof of principle* — the hin arm worked, the fim arm was
  inefficient, and **the FimB-then-Hin state was never observed**; of 50
  isolates sequenced, none carried the inverted fim orientation.
  (Ham, Lee, Keasling & Arkin, *PLoS ONE* 3(7):e2815, 2008; open access,
  PMC2481393.)
- DEBRIEF / forward: recombinase memory as a *state model* is **T47, session
  18**, where the syllabus puts it. Tuesday names it and shows the data;
  nothing in PS6 depends on it.

**Close.** Hand out **Cambray et al., *NAR* 41:5139 (2013)** for Thursday —
required, gold open access, yours with Mutalik, Carothers and Endy. One line
saying why: Thursday's thesis is that a part is a measurement, not a name, and
this is the version with a model under it.

---

## 3 · Source pages, verified by extraction on 18 October

| supplies | deck | pages |
|---|---|---|
| Classifier, timing table, **the hazard**, the two fixes, cascade delay | **L13** Logic Cascades + Therapies (2025) | **20–36** |
| NOR from a repressor–promoter pair; truth table → circuit; XNOR from NORs; gate library; the assignment problem | **L16** Logic Synthesis (2025) | **12–29** |
| Cello pipeline, performance prediction, probabilistic transfer functions, search comparison, 60 circuits, 7-segment display | **L18** Gate Minimization III (2025) | **13–36** |
| SR latch in RPU, 31/41 functional, registers, gated D latch | **L21** Latches II + Oscillators (2025) | **15–23** |
| **Combinational vs sequential frame; volatile vs non-volatile memory; DNA as digital storage; Ham 2008 multi-state** | **L25 Recombinase Circuits (2024)** | **2–12** |
| The commitment latch, mapped to physical elements | L04 Top Down Design (2025) | 62–63 |

L13 pp. 20–36 and L14 pp. 6–22 are the same pages; use L13. L18 pp. 1–12 are
NAND/NOR form conversion — cut, as triage said. **L09 and L10 contribute
nothing here and go to session 17.**

**`docs/deck-triage.md` corrections owed** (lines 69–70, 77, 146): L09 KEEP →
S17 not S16; L10 MERGE → S17; L18 "CUT except Cello" understates it — pp.
13–36 are 24 usable pages; and **L13, L16 and L21 all send material to S16**,
which triage does not record at all.

---

## 4 · What gets built

**Figures** (all generated, none lifted):
- `s16_truth_to_nor` — a table and the network it compiles to, built in stages
- `s16_classifier` — the A AND NOT B circuit, drawn
- `s16_timing_table` — the tick table as a derivation figure, hazard marked
- `s16_timing_fixed` — the repaired table beside the broken one
- `s16_hazard_types` — static-1, static-0, dynamic, three small panels
- `s16_cascade_delay` — stage count against delay, with Hooshangi's measured points
- `s16_cello_score` — the circuit score as a ratio, on S13's own transfer-curve axes
- `s16_latch_state_table` — the S9 phase plane beside its state table
- `s16_dirs_states` — Ham's four states and the two inversions

**`posb/logic.py`** — on the critical path, built first, with tests:
`TruthTable`, `to_nor_network()`, `GateNetwork.timing_table()`, `hazards()`
returning `(tick, wire, kind)`, and `cascade_delay()` reusing S10's convention
and `posb.digital.Repressor` thresholds. **Tests compute the classifier's
hazard from the gate list, not from a literal copied off the slide** — the 11
October lesson.

**Handout + answer sheet + board notes**, the usual four-item faded set.

---

## 5 · Three questions before I start

1. **Cello segment placement.** I have it after the combinational half and
   before memory, so the score lands on the margins they just used. The 2025
   decks run it the other way. Keep my order?
2. **Ham depth.** One slide (the switch and the four states) or two (adding the
   honest failure — the fim arm, and the state never observed)? I recommend
   two: the failure is the pedagogy, and it rhymes with 45/60.
3. **The 247 extra-credit item on PS6** — you said yes, as in previous sets.
   I propose it on **T34**, the two-colour intrinsic/extrinsic decomposition
   from Elowitz Table 1, since that is the one row with real algebra that the
   147 set can do without. Agreed, or would you rather it sat on the hazard
   question?

---

## 6 · The Ham state-space argument, worked out (Adam, 18 Oct)

Adam's proposal: the lesson of Ham 2008 is that a *mechanical* switch lets you
exploit DNA geometry to reach enormous state spaces in a compact footprint,
limited by recombinase quality, and modern recombinases may now overcome that.

The core of this is right and it should be taught. Three places it needs
sharpening before it goes on a slide, and the third is the interesting one.

### 6.1 "Recombinase quality" is two different limits, and only one is a parts problem

What Ham hit was **both**:

- **Efficiency and context sensitivity.** The *fim* arm barely worked -- of 50
  isolates sequenced, none carried the inverted orientation; the paper
  attributes it to the sensitivity of *fim* to IHF and LRP positioning, and the
  *hin* site had to be swapped to *hixC* to invert reliably. This is a parts
  problem and better parts fix it.
- **Reversibility.** FimB and Hin catalyse both directions. Ham's own analysis
  says what that costs: after induction you get a ~50/50 mix of start and end
  state; a two-input sequence puts ~1/4 of the population in each of four
  states; three inputs send ~1/8 to state 5. **The state space is realised as a
  population distribution, not as a defined state per cell**, and order
  information decays as the population keeps flipping.

No improvement in efficiency fixes the second one. It was fixed by changing
**enzyme class** -- from reversible DNA invertases to **large serine
integrases**, which are unidirectional: attB x attP -> attL x attR, and the
reverse needs a separate recombination directionality factor. That is the
substantive correction to the framing: not a better *fim*, a different
mechanism.

### 6.2 The modern scoreboard, and it rhymes with Cello

Yang, Nielsen, Fernandez-Rodriguez et al., *Nat Methods* 11:1261 (2014),
"Permanent genetic memory with >1-byte capacity" (Voigt lab):

- **34** phage integrases identified bioinformatically
- **13** used to build memory switches
- **11** perfectly orthogonal to each other and to FimE and HbiF
- **1.375 bytes** = **11 bits** recorded in one array in *E. coli*
- negligible background switching uninduced; no additive growth defect

**34 screened, 11 usable.** That is the same one-in-three attrition as
Stanton's mined repressors behind Cello, and it lands on the same conclusion
from the other direction: **the architecture is not the bottleneck, the
orthogonal parts set is.** Both halves of session 16 arrive there
independently, which is the through-line worth building the session on.

### 6.3 The super-exponential claim is still unrealised, and that is the good ending

Ham's theoretical argument: 10 invertases give >10^10 possible site
arrangements, and a 10-input device has a maximal state space of nearly
**10^7**. Yang/Voigt's 11 integrases gave **2^11 = 2048** states.

Four orders of magnitude, and the gap is structural rather than technical.
10^7 ~ 2^23 from 10 invertases requires **interleaved or nested sites**, where
the inversions do not commute and the reachable set is a group orbit rather
than a bit vector. What was actually built is a **register of independent
bits** -- n recombinases, n bits, 2^n states. Independent switches are easy to
design and easy to read; interleaved ones are neither, and interleaving is
exactly what Ham could not make work.

So the blocker has **moved**, not disappeared: from enzyme quality to the
design and readout of interleaved architectures. Nobody has shipped the
compact super-exponential memory the 2008 paper argued for. For a class whose
thesis is that specification is the hard part, that is a better closing line
than "and then it was solved."

### 6.4 One thing to add to the argument, and one cost to be honest about

**Add readout.** Ham diagnosed states with state-specific PCR primers, which
costs one primer pair per state and does not scale past a handful. A large
state space is worthless if it cannot be read. Cheap sequencing is a genuine
modern enabler of this idea and it is not an enzyme improvement at all --
worth saying, because it is the kind of enabling advance students never
think to count.

**Be honest about the footprint.** The compactness claim holds for *where the
information sits*: a state is a few hundred bp of orientation, costs nothing
to hold, survives cell death, and needs no standing expression -- all of which
a transcriptional latch fails. It does **not** hold for the machine that
writes it. A large serine integrase CDS is roughly 1.4-1.8 kb
[verify against a sequence before this goes on a slide], so 11 integrases is
~17 kb of writer machinery around a switch of ~1 kb. The memory is compact;
the recorder is not. That is why the architecture won where you install once
and record for a long time -- lineage tracing, in vivo event recorders -- and
not as general-purpose registers.

### 6.5 What this means for the slides

Three surfaces rather than two, and the third is the one that earns the paper:

1. **The mechanism.** DIRS: two overlapping inversion systems, FimB and Hin,
   state encoded in the sequence itself, four states from the order of two
   inputs, ~1 kb. Volatile vs non-volatile, against the toggle they just saw.
2. **The honest result.** The *hin* arm worked, the *fim* arm did not, the
   FimB-then-Hin state was never observed, and reversibility spreads the
   population across states. Proof of principle, stated as such by its authors.
3. **What happened next, and what did not.** 34 -> 11 orthogonal -> 1.375
   bytes, unidirectional integrases, negligible background. Then the open
   question: 2^11 against a predicted 10^7, and why the gap is interleaving
   rather than enzymes.

---

## 7 · The shufflon, and why Adam's "readout by action" point is the stronger one (18 Oct)

Adam's addition: Ham's architecture gives not just memory but **action** — place
promoters, terminators and genes correctly and an inversion *assembles* a
working transcription unit, so the state is the program. He compared it to a
natural system generating large numbers of surface variants, and asked not to
overclaim.

**It is not an overclaim, and the natural precedent is better than the one he
named.** One correction and one upgrade.

### 7.1 The correction: it is R64, not *Neisseria*

The **shufflon** is the R64 plasmid system, not *Neisseria*. *Neisseria* pilin
antigenic variation works by **gene conversion** from silent *pilS* cassettes
into the expressed *pilE* locus — a different mechanism that would not support
the argument. The shufflon is inversion-based, which is exactly Ham's
architecture occurring in nature.

Verified against Katalinić, Richards, Auyang, Millett, Kogenaru & Windbichler,
*ACS Synth. Biol.* (2025), doi 10.1021/acssynbio.4c00790, CC BY, PMC11852207:

> "The pil operon harbors the rci gene, coding for shufflon invertase *Rci*,
> and the adjacent shufflon made of **four DNA segments** separated and flanked
> by **seven** recognition sites, also known as shufflon crossover or *sfx*
> sites, specifically recognized by *Rci*."

> "...a DNA inversion system that functions as a biological switch to select
> between alternative **C-terminal segments of the pilV protein**."

> "...the pilV products are tip-located adhesins of the type IV pilus that
> recognize lipopolysaccharides of recipient bacterial cells and thus determine
> **recipient specificity in matings**."

So the natural lineage runs straight into Ham: **Hin** (one inversion, two
flagellin states, *Salmonella* — and the very enzyme Ham used) -> **the R64
shufflon** (four segments, seven *sfx* sites, one recombinase, combinatorial
PilV variants) -> Ham's DIRS, which is a deliberate two-invertase version of
the same idea.

### 7.2 The upgrade: "readout by action" dissolves the objection I raised

In §6.4 I argued that a large state space is worthless without readout, and
that sequencing was the modern enabler. **Adam's point is the better answer and
it makes that objection mostly irrelevant for one of the two use cases.** If the
inversion reconstitutes a promoter–gene–terminator arrangement, there is no
decoding step at all: you do not read the state, you *run* it. The decoder is
free because the DNA arrangement **is** the expression program. Nature does not
sequence its shufflon; it expresses a different adhesin.

That splits the field cleanly, and the split is worth a slide:

| | **register / recorder** | **program / diversity generator** |
|---|---|---|
| state is | a bit to be read | the function itself |
| readout | sequencing or PCR — costs scale with states | selection or phenotype — free |
| needs | unidirectional, orthogonal, low background | high rate, many sites, combinatorial reach |
| exemplar | Yang/Voigt 2014: 11 orthogonal integrases, 1.375 bytes | R64 shufflon; Ham's DIRS; synthetic shufflons |

The field went hard down the left column. The right column is Ham's deeper
idea and it is the one still open.

### 7.3 And "modern recombinases might now overcome this" is confirmed, in 2025

The same ACS Synth. Biol. paper names Adam's limitation in its own abstract and
then fixes it:

> "However, the availability of a **single enzyme with moderate rates of
> recombination** has hampered the more widespread use of SIs. We identified
> **14 previously untested SI genes** and their *sfx* sites in public databases...
> determined cross-recognition to identify **orthogonal SI/*sfx* pairs**. We
> describe SI enzymes with **substantially improved shuffling rates**..."

And its closing claim is Adam's claim, stated by someone else:

> "...synthetic shufflons enable the generation of **millions of sequence
> variants in vivo** for applications such as barcoding or experimental
> selection."

Note what the application is: **barcoding and experimental selection** — the
right-hand column. Diversity you select on, not states you read. That is the
honest form of the claim and it is stronger than the version I wrote in §6.3,
which measured the idea against a register and found it four orders short.
Measured against what it is actually for, it is being realised right now.

### 7.4 What changes in the slides

Ham's third surface (§6.5) becomes the fork, not just the scoreboard:

- the register road — unidirectional integrases, 34 -> 11, 1.375 bytes, the
  same attrition as Cello's gate library;
- the program road — the state *is* the expression unit, no decoder, natural
  precedent in R64's four segments and seven *sfx* sites, and a 2025 toolkit
  paper aiming at millions of variants in vivo.

One line to close on, which is the honest version of Adam's instinct:
**the compact super-exponential state space is real, and it was never going to
be read — it was going to be selected on.**
