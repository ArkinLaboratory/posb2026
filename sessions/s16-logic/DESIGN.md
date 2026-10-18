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
  presented as one. Then the measured version: SR latches in RPU,
  registers, the gated D latch. (The "31 of 41 functional" figure came off
  the 2025 deck with no paper named and nothing in `private/readings`
  supports it, so it is cut from the slide until a source is found.)
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

**34 found, 13 selected and built, 11 orthogonal.** Note what the steps are:
34 → 13 is a CHOICE (at most 60% amino-acid identity, p. 4), not an attrition,
and 11 of the 13 tested worked. An earlier draft called this "one-in-three
attrition" and rhymed it with Stanton's mined repressors; that rhyme is wrong
in its arithmetic and unnecessary, because the real shared constraint is
stronger and lands on the same conclusion: **the architecture is not the bottleneck, the
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

---

## 8 · The combinatorics behind Ham — the paper's numbers, and a correction (18 Oct, revised)

Adam asked whether the Ham surfaces should outline **theoretically** how the
architecture works and where the power comes from. Yes, and the theory is
small enough to derive in the room, which makes "enormous state space" a
number rather than an adjective.

> **Correction, 18 October (second pass).** The first version of this section
> put a table of my own enumeration on the slide — 1 024 states at three
> invertases, 917 504 at six. Ham gives **15** and **1 956**. The slide was
> 68× to 470× out, with the caveat only in the speaker notes, next to a slide
> drawing Ham's five-state graph that the big numbers cannot be reconciled
> with. The deck now carries Ham's formula and Ham's numbers. See §8.5 for
> what my enumerator was actually counting and why it is not settled.

### 8.1 The model, as Ham states it

DNA is a sequence of segments separated by recombination sites. An invertase
reverses the stretch between its own two sites, flipping the order and the
orientation of everything inside, sites included. A **state** is a distinct
arrangement of the region between the outermost sites.

Ham's counting argument, p. 2815-3:

> "Simply counting the internal nodes of the state transition graphs like
> those in Figure 1C shows that the number of states (excluding state 0) for
> such devices is the number of permutations of non-empty subsets of
> {1,…,N}"

which is

$$S(N) \;=\; \sum_{k=1}^{N} k!\binom{N}{k}$$

A state records **which** invertases have fired and **in what order**, so a
state is an ordered sequence drawn from a subset of the N available
invertases, and the sum counts exactly those. It is derivable at the board in
about three lines, which is why it is on the slide rather than quoted.

### 8.2 The numbers

| invertases N | site layout | states | 2^N | gain |
|---:|---|---:|---:|---:|
| 1 | single | 2 | 2 | 1× |
| 2 | independent | 4 | 4 | 1× |
| 2 | **nested** (one pair inside the other) | **4** | 4 | **1×** |
| 2 | **staggered** (Fig. 1C) | **5** | 4 | 1.25× |
| 3 | independent or nested | 8 | 8 | 1× |
| 3 | staggered | 16 | 8 | 2× |
| 6 | staggered | 1 957 | 64 | 31× |
| 10 | staggered | 9 864 101 | 1 024 | 9 633× |

The counts in the table are `1 + S(N)`, including the starting state;
Ham's `S(N)` excludes it. Ham's own words for the last row: devices with ten
invertases "have maximal state-spaces of nearly 10⁷" (Fig. 1E, red curve).
Note that Fig. 1E plots **two** curves and they are different quantities —
the blue one is how many ways the sites can be ARRANGED, "more than 10¹⁰" at
ten invertases, and the red one is the state space of one such arrangement.
Do not quote one for the other.

**Three results, and the middle one is the teachable surprise.**

1. **Independent sites give exactly 2^N.** N invertases, N bits. A register,
   and it is what Yang/Voigt built: 11 orthogonal integrases, 2¹¹ = 2048
   states, 1.375 bytes.
2. **Nested sites also give exactly 2^N.** Nesting *looks* as though it must
   create interaction — one inversion carries another's sites bodily with it
   — and it buys nothing. Ham, Fig. 1B caption: when one pair of sites is
   fully contained by another "the resultant number of possible 'states' of
   the system is only four". This is the wrong intuition worth showing, per
   the standing rule on teaching the evolution of the logic.
3. **Staggered sites break it open**, because staggered inversions do not
   commute: the result depends on the order they fired in, so history is part
   of the state. The gain is modest at small N (1.25× at two, 2× at three)
   and superexponential after: 31× at six, four orders of magnitude at ten.
   Say both halves of that. "It explodes" is true only once N is past four.

### 8.3 Why this belongs in THIS session

The session's organising distinction is combinational versus sequential —
output from inputs, against output from inputs **and history**. Staggered
inversions are the DNA instance of exactly that distinction:

> **Ham's DIRS is a sequential circuit written in DNA.** Its five states are
> five because the two inputs can arrive in two orders, and state 3 ≠ state
> 4. At N = 2 that is barely more states than a two-bit register — it is
> *different* states, selected by history. That is the definition of
> sequential logic, implemented without a single protein holding the state.

At N = 2 staggering buys order-dependence rather than count. The count
arrives later, and that is the honest sequence to present it in.

### 8.4 Where the power actually comes from — the footprint argument

| | register (integrases) | shufflon (one invertase, many sites) |
|---|---|---|
| states | 2^N | S(N), superexponential past N ≈ 4 |
| enzymes | **one orthogonal enzyme per bit** | **one enzyme, many sites** |
| writer DNA | ~1.4–1.8 kb of CDS per bit | constant in the number of sites |
| addressable? | yes, bit by bit | no — the enzyme flips everything it recognises |
| readout | sequencing | the state **is** the program; selection reads it |

R64 is the natural instance: *rci* encodes **one** Rci invertase, and the
adjacent shufflon is **four DNA segments flanked by seven *sfx* sites**.
One enzyme, combinatorial output. That is the compactness claim in its
strongest form — not that DNA memory is dense, but that **the writer cost
stops scaling with the state space** once the sites share a recombinase.

### 8.5 What my enumerator was counting, and why it is parked

The enumerator I wrote took the reachable set to be the orbit of the starting
arrangement under the group generated by the available inversions, with sites
carried along and invertases allowed to fire repeatedly. That gives 24 at
N = 2 against Ham's 5, and 1 024 at N = 3 against Ham's 16.

The gap is not arithmetic. Ham counts states as **distinct input histories**,
which is bounded by permutations of subsets because a history is a sequence
of distinct invertases. My orbit allows an invertase to fire again after
others have moved its sites, which reaches arrangements no non-repeating
history reaches. Whether those are physically distinguishable states of a
real device is a real question and I have not settled it.

Until it is settled it stays out of the deck. If it is worth pursuing it is a
nice 247 problem — "enumerate the orbit and compare it with Ham's count" is
about twenty-five lines of Python and the discrepancy is the interesting part
— but it is not something to assert to a 147 room as the paper's result.

---

## 9 · What your slide critique changed, 18 October

You read the first build and said four things. All four are now in the deck.

**"We generally start the class with a few reminder questions, then tell them
what they are going to learn."** The opening was the other way round. The
retrieval questions are now slides 2, and the objectives slide — *Where today
goes* — follows at 3. The objectives are written as four things the hour will
do, with the fourth deliberately withheld so they can name it at the close.

**"Where did a truth table come from on slide four? No introduction, no review
of what they are supposed to have read, no circuit examples or graphics."**
There is now a segment 0 before any abstraction: **Nielsen Fig. 1A on the
screen**, the whole Cello pipeline, with the slide after it carrying the
paper's headline numbers and the question (*what is the missing quarter made
of?*) that the Cello segment collects on an hour later. The truth table then
arrives as the output of the *Verilog parsing* box in a diagram they are
looking at, not as an assertion.

**"You start with the assertion of an equation. How did we get there? On page
six we could plot the equation as a function of r₁ and r₂ to SHOW them."**
Done, in that order:

| slide | what it does |
|---|---|
| `universal` | complement + aggregator → every logic function, as a figure |
| `nor-build` | four states → weights → *Z* = (1+r_A)(1+r_B) → *P*_on, one line per click, from session 6 |
| `arch-nor` | that same *P*_on drawn over the whole (r_A, r_B) plane, log–log, four corners circled 1/0/0/0 |
| `arch-nand` | one operator moved to its own promoter; the map, and the gate, flip |

**"The idea that you can build ANY logic out of a complement and an aggregator
is totally lost, and why NOR and not NAND is not well explained
mechanistically."** The universality claim is now its own figure before any
algebra. The NOR/NAND contrast is mechanical rather than asserted: **one
promoter with two operators** gives *P*_on = 1/(1+r_A)(1+r_B), which is NOR;
**two promoters driving one gene** gives out ∝ 1/(1+r_A) + 1/(1+r_B), which is
NAND. Same two repressors, same two operator sites, different layout, opposite
gate. That also settles the inconsistency the old deck had — it derived NOR as
"what biology gives you" and then used a NAND for R2 in the classifier. R2 is
the two-promoter architecture, and now the room has seen why.

A bonus the heatmap gives for free: the NAND's two single-repressor ON corners
sit at about **half** the amplitude of the double-off corner, because only one
of the two promoters is firing. That is a noise margin, and it is in the
speaker notes as a forward reference to the Cello score.

**"Check my slides from last year for good figures — the Cello circuit
optimizer. We tend NOT to show the actual work we are doing and the papers we
are discussing, and this is a bad habit."** Two real figures are now in the
deck, both extracted from the PDF and declared in `decks/paper_figures.yaml`:

- `nielsen2016_fig1a` — the pipeline, at the top of the hour.
- `nielsen2016_fig5a` — fraction correct against number of repressors, placed
  *after* the students commit to one of four explanations for 45/60, so the
  data settles the bet rather than pre-empting it.

Both were recropped once after looking at the rendered slide: Fig. 1A had a
sliver of the journal's sideways margin credit, Fig. 5A a sliver of panel B.

**Language.** A pass over every student-facing string against the no-slop
rules. Three real finds: a foot on the Cello frame slide that was speaker
direction leaking onto the wall (*"the job of this segment is to make them use
it"*), a colon-reveal header (*"So: the free gate library"*), and a
not-X-it-is-Y construction. Two surfaces were also sharing the badge
`reading`, which the pacing bookkeeping keys on.

---

## 10 · Adversarial review, 18 October — what it found and what was done

A fresh agent that had not seen this design was given the deck source, the
figure generators, `posb.logic`, the session documents and the paper PDFs,
and told to find defects and rank them. Every finding below was re-verified
before anything was changed; two of its claims did not survive that and are
recorded as such.

### Blocking, fixed

| | finding | what was done |
|---|---|---|
| B1 | The XNOR debrief gave the two depths as 3 and 2. The network it specifies has longest path **4** and shortest **3**. | The debrief is now two surfaces built on `s16_xnor_two_ways`, and both figures' gene counts and path lengths are computed by `posb.logic` at render time rather than typed. |
| B2 | The shufflon state counts (1 024 at three invertases, 917 504 at six) were my own enumeration under a different definition of a state. Ham gives **15** and **1 956**, and the previous slide draws Ham's five-state graph, which the big numbers cannot be reconciled with. | The slide now carries Ham's own formula, S(N) = Σ k!·C(N,k), and his numbers. §8 rewritten; my enumerator parked in §8.5 as an open question, possibly a 247 problem. |
| B3 | "Clean, and not because the wiring changed — because the resting state did" is false. The deck's own first repair (pad the short path) is fail-safe and still glitches in all four cases; `classifier_fixed` is clean because it is fail-safe **and** balanced. | New computed figure `s16_two_conditions` with four rows and two counterexamples, and the consequence slide now states the rule as a conjunction. |
| B4 | On the cascade-delay slide the row stack was drawn across the figure (7.85 × 0.67 in of overlap). `slide_fit` could not see it. | Segment restructured; `tools/slide_fit.py` now checks text against pictures. |
| B5 | "31 of 41 designed latches were functional" had no source anywhere, and its own speaker note said so. | Cut from the slide; the note records what to restore it if the source is found. |
| B6 | The glitch release points at a handout, and the handout does not exist. | Still outstanding. Tuesday also needs the answer sheet, the board notes and PS6. |

### Should-fix, done

- **S1/S2.** The Hooshangi comparison set circuit 1's *settling* against circuit 3's *starting*, two different events 20 min apart, and called it "much more than two lifetimes". It now compares settling with settling, 120 against 600 min. "About two and a half lifetimes late" matched neither quantity the segment defines (t½(3) = 2.674 τ, delay against one stage = 1.981 τ); the slide now gives both and says which is which.
- **S3.** The Cello release's "best answer" was orthogonality. The paper's own failure analysis says something else: "most of the circuit failures point to unexpected behavior from the anhydrotetracycline (aTc) sensor (seven circuits) or AmtR gate (two circuits)". A new slide gives the paper's verdict first and labels the library argument as mine on top of it.
- **S4.** The dynamic hazard is panel **three** (A = 1, B = 0), not four.
- **S5/S6/S7/S13.** `fig_universal` said NAND fits on one promoter, which `fig_arch_nand` contradicts six slides later; `fig_arch_nand` drew two genes under a title saying one; all three ON corners of the NAND map were badged "1" including the two at half amplitude, on the slide whose foot tells the room to look at exactly those two; and `fig_classifier` drew R2 as one promoter with two operators, which is the NOR idiom. All four redrawn, and the corner badges are now read off the rate law rather than typed.
- **S9.** The SR latch's (0, 0) tick is a consequence of updating both cross-coupled NORs in the same tick; update them one at a time and it disappears. "That is real" is now a question put to the room.
- **S10.** "Unequal delays make it worse, never better" was unsupported; a slow output gate is the standard hazard filter.
- **S11/S12.** "In the therapy this is cloned from" cited nothing anywhere, and "Quote whichever matches the context and say which" was writer-direction rendered on a student slide.
- **S14.** Yang 2014: 34 integrases found bioinformatically, **13** selected on a ≤60% identity criterion, 11 of those orthogonal. The 34 → 13 step is a choice, so the "one-in-three attrition" rhyme with Cello was arithmetically wrong and is replaced by the real shared constraint.
- **S15.** Fig. 5A's states curve runs ~0.97 to ~0.86, not "near 0.85" and not flat.
- **S16.** The cascade segment had no RELEASE. It has one now (estimate a four-stage half-time), and segment 1's debrief has the figure the design promised.
- **M6.** Four printed minute estimates on student-facing surfaces, against the standing rule. Removed.
- **M8.** An arrow drawn inside the block it points at, in `fig_universal`.
- **M9/M10.** The hazard taxonomy is defined for a transition in a settled circuit and the deck applies it to a power-on transient — and Cello's own paper documents a fault of the first kind, with the path-length mechanism, in the paper the room has read. Both are now one slide: *"Cello's paper has one of these in it"*, which is where the path-length diagnosis turns out to be the right one after all.
- **M11.** Science's article pages are folios (aac7341-N), not PDF page numbers. Corrected throughout the Cello citations.

### Open, and needing a decision

**S8 — the legibility floor, systematically.** `_fig()` places figures at
`pixels / 160`, and `figures/style.py` saves at `savefig.dpi = 160`, so the
scale is exactly 1.000: **a figure's authored matplotlib point size is its
size on the wall.** Two docstrings say the opposite — `figures/s16_logic.py`
says wide figures are authored near SLOT/UP so the deck enlarges them, and
`figures/style.py` sets a floor of 15, not 20. Fixed in the figures this pass
touched. Still below the 20 pt content floor:

- `s16_cascade_delay` — legend, per-stage annotation and axis titles at 16, tick labels at 15 and 14
- `s16_dirs_states` — the "state 3 never observed" caption at 16, which is the honest result of the paper
- `s16_hazard_types` — axis label 15, ticks 14

Two ways to fix it and they are not equivalent: re-author those strings at
20+, or give `_fig` an explicit upscale and re-check every figure's band.
The second is one change and affects every session; the first is safe and
local. **Your call.**

Also open: `tools/slide_fit.py`'s new picture check reports 0–3 items on most
earlier decks and 10 on s14-review, untriaged. Some are the estimator being
conservative about title heights (session 13 slide 18 is fine on the wall);
some are probably real. It is advisory and does not fail a build.

### Two findings that did not survive verification

- The review read Ham's Fig. 1D as giving a **maximum of 15** states for three invertases. Fifteen is S(3), the count *excluding* the starting state; including it the figure's maximum is 16. The deck now says "4 more, so five in all" at N = 2 to keep that straight.
- It also reported `fig_arch_nand`'s corners as 0.500 exactly. They are 0.500 at the marker positions, which is what matters for the badge, but the half-amplitude plateau is not flat across the panel.

---

## 11 · Second slide review, 18 October — six items

**"We need to directly explain the VOIGT NOR and how it works before we use
it."** Correct, and the omission was hiding a contradiction. The deck derived
NOR from promoter occupancy, then used the word for the rest of the hour
without ever drawing the part. New figure `s16_voigt_nor` and a slide after
the NAND architecture: two input promoters in tandem, a repressor gene behind
them, an output promoter carrying that repressor's operator. Either input
fires → repressor made → output shut. NOR.

It also resolves a collision the deck had set up for itself. `fig_arch_nand`
draws two tandem promoters over one gene and calls it NAND; Cello draws the
same DNA and calls it NOR. **Both are right.** The difference is which
quantity you call the input: a repressor concentration in ours, which inverts
each input, or a promoter activity in theirs, which puts the inversion at the
output. Said out loud, that is one of the better lessons in the hour. Left
implicit, it was a trap, and the room would have hit it.

The slide also makes the point the universality figure asserts and never
showed: the tandem promoters are the aggregator, the repressor on the output
promoter is the complement, one part carries both. And the gate's input and
output are the same kind of quantity (promoter activity, in RPU), which is
the whole reason gates compose without converters.

**"Slide 16 figure clips the circuit."** The ¬A node sat at y = 0.96 with a
box half-height of 0.065, so its top border was at 1.025 — outside the axes,
and matplotlib clipped it away. Both panels' outer nodes pulled inside the
band.

**"To augment slide 40 we have an animated image of the different ways Cello
optimizes."** Found: PoSB 2025 Lecture 18, slides 19 and 20, Bryan Der's
animations. Eight media files; the useful ones are `media3` (best circuit
score against iteration), `media4` (predicted ON and OFF level of all eight
states) and `media5` (the circuit recolouring as the assignment changes), all
50 frames at 4 fps and perfectly synchronised.

They cannot be used as they stand: each is one animated panel with no axes,
and the labels, tick values and truth-table rows under the bars are
PowerPoint text boxes on the 2025 slide. So the slide is recomposed with
ffmpeg — page 20 rendered at 150 dpi as the background, the two chart movies
cropped to their ink and overlaid exactly on their plot areas so the
PowerPoint labels survive, and the wiring movie overlaid with a white
colour-key so the static gate outlines show through. Output is one 12.5 s mp4
at `private/paper-movies/der2016_cello_hillclimb.mp4`, embedded with
`paper_movie` and posted on its final frame. **Yes, we should use it** — it
is the only surface in the hour where the room watches a bad assignment
become a good one.

Slide 19's greedy / depth-first pair composites the same way and is at
`der2016_cello_greedy_dfs.mp4`, built but **not placed**: its ghosting is
worse (two curves per gate) and it is a second video in a deck that is
already long. Say the word and it goes in after the hill-climbing one.

**"Slide 50 has text overlap in the table image."** Four panel titles of the
form `hold Q=1  (S=0 R=0)` at 21 pt in a quarter-width panel. Two lines each
now. The figure also carried a suptitle duplicating the slide title (gone),
and headed a column `Q̄` with a combining macron that the monospace cell font
silently drops — it renders as a bare `Q`, so the column is now `¬Q`, which
is how the rest of the deck writes a complement.

**"Show the circuit and explain what SR means."** New figure
`s16_sr_circuit` and a slide before the state table: the two cross-coupled
NOR genes, S and R as inputs, Q and ¬Q as outputs, and in words what the
letters mean — S sets, R resets, both low holds, **both high is forbidden**,
which the deck never said.

**"The transition between 52 and 53 is abrupt. We don't give them a sense of
the DNA or inversion or intercalated sites."** The memory half went from "an
invertase reverses the stretch of DNA between two sites" in prose straight to
a five-node state graph. New figure `s16_inversion` between them: before and
after one inversion with the gene arrow reversed, then nested against
staggered site placement side by side. The site triangles within a pair point
**at** each other, because a pair in inverted orientation is what makes an
inversion rather than an excision — drawing them all one way would teach the
wrong thing on the figure whose whole subject is where the sites go.

### Length

62 slides, of which 52 count after the two derivation runs collapse. It is
long and you are right that it is. Candidates to cut, in the order I would
cut them, all of them surfaces that now have a better neighbour:

1. `nor-library` — the free gate library, now mostly said by the Voigt NOR slide.
2. `delay-ask` — the half-time convention, which folds into `delay-rule`.
3. `dna-count` — folds back into `dna-theory` now that the counts are the paper's.
4. `cello-frame` — the four candidates, which the release slide restates.
5. `reading-why` — the headline numbers, which fit in the Fig. 1A foot.

That is five surfaces and none of them carries a figure.

---

## 12 · Tuesday closed out, 18 October

**Five slides hidden, not cut.** `Deck.hide()` sets `show="0"` on the slide,
which PowerPoint skips in presentation mode and greys in the sorter. The
surface stays in the file, keeps its speaker notes, still exports to the PDF,
and is one keystroke from coming back. The build prints which five, so a
hidden slide cannot be quietly forgotten. 62 slides, 57 shown.

**Handout and answers.** `handouts/s16-logic.md` and `-answers.md`. Four
problems and a stretch: the classifier's tick table worked in full, compile
XNOR and count the two depths, a second three-gene circuit to fill in and
diagnose, the four-stage delay, and — the item the handout tells them is on
the problem set — build a fail-safe circuit that is not balanced and show it
still glitches. Every table in the answers is computed by `posb.logic`.

**Board notes.** `board-notes/s16-board-notes.md`. Four board moments, named
by the deck's segment rather than by the clock, because this deck prints no
timings: the four-state count at **nor-build**, the two XNOR networks at
**nor-debrief**, the two conditions at **fix-separate**, and $S(n)$ at
**dna-count**. The counting at nor-debrief is marked do-not-cut, since the
wrong depth is the one thing the room would otherwise carry out of the
building.

**PS6.** `private/sources/ps06.py` → `problem-sets/ps06-noise-logic/`. 48
points, 56 for 247. Eight questions covering T17 and T31–T41; T42–T44 move to
PS7, settled because session 17 is taught two days before this set is due and
an item cannot be assessed the week it is first seen.

Q6 is the one the set exists for. Session 16 refutes "the paths are different
lengths" with a balanced circuit that glitches, and then comes within one
sentence of asserting the mirror image. Q6c makes the students find the second
counterexample themselves and Q6d asks them to state the rule as the
conjunction it is — including what it does **not** establish. Q8, the 247
item, then turns back on Q3 and asks which of the two noise components their
own simulation could not see.

`otter assign` runs the tests against the solution notebook, so the build is
also a correctness check: **11 grader.check blocks pass**. The student
notebook is solution-free (checked for every marker, and for three of the
answer values directly).

One repo defect found on the way: `PROBLEM_SETS` in
`tools/build_problem_sets.py` still read `["ps01".."ps04"]`, so ps05 built
when named and was silently skipped by the no-argument build. Same class of
defect as `figures.s14_review` missing from `build_figures` MODULES. Both ps05
and ps06 are in the list now.

### Still owed before Tuesday

Nothing in the repo. The manual half is
`docs/session-release-checklist.md`: the Gradescope assignment pair for PS6
(147 and 247 are two assignments, two denominators), the autograder zip at
`private/build/ps06/dist/autograder/`, and the bCourses module. The solved
notebook for testing the autograder is at
`private/build/ps06/ps06-solved.ipynb`.
