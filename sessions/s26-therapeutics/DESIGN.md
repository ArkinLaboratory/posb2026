# Session 26 — Therapeutic circuits · Tue 24 November 2026

Built from `DESIGN-SPINE.md` (settled with Adam 8 November) and `NUMBERS.md`
(1110 lines, reproducible from `_scratch/s26_xie/emit_numbers_md.py` below line
92 — **edit the generator, never the file**).

Assigned paper: **Xie, Wroblewska, Mitchell, Lim & Weiss, *Science* 333, 1307
(2011)** — the HeLa miRNA classifier.

Techniques: **T69**, design a multi-input classifier to a false-positive budget
(autograded, on PS9 and the final) and **T70**, sensitivity/specificity
trade-off reasoning (hand-graded, on PS9).

---

## 0 · The main point, the title, and the opening

**Main point, one claim:** you can characterize every sensor in isolation,
compose them, predict selectivity from the composition, hit your output
budget — and a third of the wrong cells still die.

**Title: "A budget the circuit cannot keep."** Parallel in construction to
session 22's *"A set point the circuit cannot move"* and session 23's *"Burden
becomes selection"*, and chosen for the same reason: it names the result rather
than the move. The condition travels with the claim everywhere it is said —
**the circuit computes an output, the effector produces an outcome, and the
budget was written on the first.**

**Subtitle, on the title surface:** *Every sensor is characterized, the
composition predicts the selectivity, the output budget is met — and the
therapy still kills a third of the cells it was built to spare.*

The opening does not set a scene. Per rule 15 it states the claim the hour
establishes, in the words the session will use for it.

---

## 1 · Where this sits

`docs/course-map.md` makes sessions 26–28 **the same object three times — a
classifier with a threshold and a budget for its mistakes** — and gives each
session one thing a population does that a circuit cannot. **Session 26's is:
the population is the thing being classified, and specificity is a population
statistic.**

`private/sources/ps09-PLAN.md` §1 binds the arithmetic at both ends of PS9.
T63, from session 23, is a per-cell escape fraction × 10⁸ CFU against a budget
of **one**. T69 is a per-cell error rate × a treated population against a
budget of **one**. *"Same shape, opposite sign — one is a device that must not
act, the other a device that must not act on the wrong cell."* The set opens on
the first and closes on the second.

**So T69 is a COUNT, not a fraction.** The population size is what turns a
per-cell rate into a clinical event, and arguing about that is T70.

---

## 2 · What the room has never seen, and what each half of it needs

The cohort is mixed by design — biology, bioengineering, EE, chemistry,
chemical engineering, seniors and graduate students — and `[[posb_session0_onboarding]]`
puts the weak axis on linear algebra, not differential equations: **only 5 of 21
respondents have ever linearized a system or seen a phase portrait**, while the
biology is the strongest axis with 15 of 21 having cloned a plasmid. So in this
session the mathematical load is light and the modeling load is conceptual, and
the risk runs the other way from session 8's: the arithmetic is five
multiplications, and what is genuinely new is **what the numbers are of**.

Per `[[posb_teaching_derivations]]` rule 1, teach the object before the model.
Four things have no precedent anywhere in the course or in the 2023–2025
archive:

| new object | why it has no precedent | which half of the room needs the setup |
|---|---|---|
| **A numerical HI/LO threshold on a marker** | In every prior year markers are high or low **by assertion**. Xie's printed 20% cut is the room's first numerical marker threshold. | both, and it is the session's hinge |
| **A per-cell-line marker-abundance table** | The archive has no such table, so converting Fig. 2D into marker levels is new work with no precedent. | the engineers, who will want to know what was measured |
| **A false positive as a defined, chosen quantity** | The string does not occur in ten prior decks. | both |
| **An RNAi sensor's physical behavior** — leak, ceiling, slope | The Boolean inversion `1 − r` idealizes a device that has all three. | the biologists get the mechanism, the engineers get why the inversion is a model |

**The seam this session can close.** Speaker notes on slides 22, 27 and 28 of
the 2023–2025 "Logic Therapies" block carry Adam's own bracket:
**`[DIFFERENT THAN THE COMPOSITOR VIEW, BUT WILL FIX LATER]`** — the Boolean
inversion does not line up with the parts-and-compositors transfer function
taught earlier. The `1 − r` conversion walks straight into that seam, and
NUMBERS §2.1's sentence is the fix: **it inverts an idealized sensor, while a
real RNAi sensor has a leak, a ceiling and a slope.** Say it on the surface
where the conversion first appears. Three years of "later" is now.

---

## 3 · The convention: MARKER LEVELS

**Settled by Adam, 9 November.** His reason reorders the session rather than
just the data handling: **start with what we would measure in the cell to drive
design and operation.** Fig. 2D plots sensor outputs, with the three NOT terms
already applied inside the sensors; the room converts back at the data boundary
before reasoning about them.

**Validated end to end, and it costs nothing in the arithmetic.** Normalize the
published table, convert with `marker_levels_from_sensor_outputs`, run
`classifier_output` with the three T-markers declared `absent`: HeLa
**0.444059189**, margin **1.475135×**, `convention_check` ok with
`alternative=None`, `sense_check` silent, round trip identity to 5.6e-17.
**Bit-identical to the sensor-output route, same ordering.** Re-verified
14 November by `_scratch/s26_minvsprod/minvsprod.py`.

**What the levels table buys, and it is move 2's best beat.** HeLa's row reads
**1.000 / 0.950 / 0.192 / 0.167 / 0.306** — the Boolean expression visible as a
row of numbers. MCF-7 then reads **0.998** on miR-21 against HeLa's 1.000: the
marker a student reaches for first does not separate the two lines at all, and
what rejects MCF-7 is miR-141 at 0.904, costing it a factor of ten. **Every
line in the panel has a specific NOT term doing the work of rejecting it.** None
of that is visible in sensor outputs.

**Two costs, handled on the surface rather than discovered by a student.**

1. `normalize_responses` takes a dict and `marker_levels_from_sensor_outputs`
   takes a matrix, **so they do not compose.** The recipe goes on the slide:
   build the dict, normalize, rebuild the matrix, convert. Verified working in
   `_scratch/s26_minvsprod/minvsprod.py` lines 20–25.
2. **Per-column normalization forces exact zeros** — HEK293 on miR-141 and
   miR-146a, MCF-7 on miR-142(3p) all read 0.0000. That means *this line is the
   panel maximum on the inverted sensor*, **not** *this marker is absent*. Say
   so where the table first appears. It is also the first instance of the
   general point that normalization is panel-relative: add an eighth cell line
   and every number changes.

---

## 4 · The six moves

**One thesis, six beats.** Moves 1–3 build the claim, move 4 earns it, moves 5
and 6 break it twice for two different reasons. Every move below declares four
things before a slide is written: its **teaching point**, the **phenomenon it
draws** for the half of the room arriving from EE, chemistry or chemical
engineering, the **derivation it builds** for the half arriving from biology,
and the **technique** it serves.

### Move 1 — FRAME · What "specific" means here, and it is not what the title says

- **Teaching point.** Specificity is a statement about a population of cell
  types, not a property of a device. A false positive is **the wrong cancer, in
  a patient.**
- **Phenomenon drawn.** The seven lines, from the SOM's own printed list: HeLa
  (cervical cancer — the one POSITIVE), MCF-7 / SKBR3 / T47D (breast), DAOY /
  SH-SY5Y (brain), HEK293 (embryonic kidney). **Six of seven are cancer lines;
  five of the six negatives are cancer.** The circuit separates one cell type
  from six others, all but one of which are tumors.
- **Derivation built.** None. This is a frame, and it costs no digitization —
  it comes off a printed list.
- **Technique.** None; it is the frame T69 and T70 are argued inside.

This is the session's thesis, not a correction to a title. Put it first.

### Move 2 — BUILD · A classifier is a threshold on a product, not a Boolean circuit

- **Teaching point.** The logic is **continuous, with a cut on it.** That is
  what makes a budget possible at all — a Boolean circuit has no budget, it
  either fires or does not.
- **Phenomenon drawn.** How AND and NOT are physically implemented in RNAi: the
  printed expression from p.1308, six markers but **five** sensor modules
  because miR-17 and miR-30a share one. The sensor's leak, ceiling and slope,
  named here, which is where the three-year compositor-view bracket closes
  (§2 above).
- **Derivation built.** The marker-level conversion, `1 − r`, with the
  idealization stated as it is used. Then HeLa's row of five numbers and the
  product. The MCF-7 beat: 0.998 on miR-21 against HeLa's 1.000 separates
  nothing; miR-141 at 0.904 is what rejects it, at a cost of a factor of ten.
- **Technique.** T69 opens here.

### Move 3 — BUILD · The false positive is defined, and the definition is a choice

- **Teaching point.** **You do not get a classifier. You get a family of them,
  indexed by a threshold** — and tuning the threshold does almost nothing. What
  moves the answer is which markers you hold.
- **Phenomenon drawn.** Fig. 2A's contour, with the caption's own words: input
  combinations giving **20% output relative to HeLa**, dots above it false
  positives *"for this specific circuit configuration."* It is the only printed
  definition of a false positive in the paper.
- **Derivation built.** The threshold staircase, NUMBERS §7.1. Relative to
  HeLa the panel reads 100.0 / 67.8 / 38.1 / 11.6 / 9.7 / 5.5 / 0.25 percent,
  so the false-positive set is **SKBR3 and T47D for every threshold from 0.116
  to 0.381** — a factor of **3.3** in a number the paper chose and did not
  defend, across which nothing changes. One step per negative line, half-open
  in *t* because `confusion` calls a line sitting exactly on the cut positive.
- **Technique.** T70 opens here — this is the trade-off, made numerical.

### Move 4 — BUILD · Design to a budget, and watch the composition look good

- **Teaching point.** **The quantity you optimize is the quantity that behaves;
  everything else is free to move.** A minimax lesson a room of engineers
  should own, and it is free here.
- **Phenomenon drawn.** Fig. 2C's two series and Fig. 2D's 7×5 response matrix.
  Fig. 2C says more markers buys selectivity: minimal ~6-fold, average
  ~160-fold at five to six markers, both corroborated by printed prose.
- **Derivation built.** Pick markers and a threshold, get a per-cell error rate.
  Then the two results that complicate it:
  - **The Average series dips by 2.65× at three markers, and it is not a
    contradiction with the prose** (§3.2). The caption says the circuit at each
    marker count is chosen to maximize the *worst* output ratio; the Average is
    a by-product of that choice and is optimized for nothing. The Minimal series
    is monotone 1.02 → 2.10 → 2.40 → 5.34 → 6.61 over one to five markers,
    exactly as p.1308 claims. **The beat is not "read the figure over the
    sentence."**
  - **§2.3: no single sensor identifies HeLa.** On four of the five sensors
    HeLa is not the highest line in the panel, and on miR-146a five of the six
    negatives sit above it. The one sensor where HeLa leads every negative is
    miR-21, by **0.0019** rel. u. against MCF-7 — **0.029 of HeLa's own plotted
    SD.** The identification lives in the product and nowhere else.
- **Technique.** T69's demonstration. This is the move the home-guide and PS9
  items are keyed to.
- **Carries the Fight 1 panel.** See §5.

### Move 5 — RELEASE / DEBRIEF · Now put them in one dish

- **Teaching point.** **Specificity measured alone is not specificity measured
  beside its target** — and nobody measured it well enough to know their own
  false-positive rate.
- **Phenomenon drawn.** Fig. 4B. HeLa-EYFP and HEK293-Cerulean **in the same
  mixture**, DsRed⁺ counts of surviving transfected cells, three conditions.
  Digitized (§5.1): the classifier kills **75.0% ± 5.6** of the cells it is
  meant to kill and **33.1% ± 7.6** of the cells it is meant to spare.
- **Derivation built.** Score both panels with the SOM's own killing-efficiency
  formula (§4.3). Off-target killing is **0.360 ± 0.082** in the mixture against
  **0.145 ± 0.267** for HEK293 measured alone in Fig. 3C(right) — a factor of
  **2.48**. On-target killing does not move: 0.915 → 0.930. **The control column
  is what rules out "the two panels are on different scales,"** which is the
  first objection the room will raise.
- **Technique.** T70.

**Three guards this move must carry, each of which the session says rather than
being caught by.**

1. **The paper cannot resolve its own effect.** The gap is **0.81 of Fig. 3C's
   own plotted SD** (§5.4), and Fig. 3C(right)'s HEK293 bar has **SD/mean =
   1.84**, drawn with no lower cap because the lower arm falls below zero
   (§4.1). **A slide may not say the paper showed this.** §5.4's defensible
   sentence is the one to use: the same circuit, same formula, 15% off-target
   alone and 36% beside its target, on-target unchanged — **and nobody measured
   it well enough to know their own false-positive rate.** That lands harder
   than a clean 2× would.
2. **Two structural confounds come with it** — unmodified HEK293 under table
   S3B against HEK293-Cerulean under table S4. Named on the surface.
3. **The 33.3% and the 33.1% are not the same quantity, and their agreement is
   a coincidence** (§7.2). 33.3% is a fraction of **cell lines** — how many of
   six negative cultured lines have a predicted product above a declared
   fraction of HeLa's, a quantity that can take only seven values. 33.1% is a
   fraction of **cells** — the proportion of HEK293 cells in one dish that died,
   SD 7.6 points over n = 3. Move the threshold and the first changes while the
   second does not. **A sentence of the form "the matrix predicts a third and
   the experiment measured a third" is a validation claim and nothing supports
   one.** What the slide may say: at Xie's own cut the matrix calls 2 of 6
   negative lines false positives, and the mixture kills about a third of the
   one negative line it tested. Both are bad news for a budget; neither is
   evidence for the other.

**And an independent check that does pass** (§6.2), which is why guard 3 is
about rigor and not about pessimism. Fig. 4A is a reporter — no apoptosis,
different panel, different experiment. The circuit's HEK293 output is **0.320**
of its HeLa output against Fig. 4B's measured **0.331**: agreement to 1.1
points, two measurements of the same quantity through readouts sharing no
apoptosis. The false-positive rate is not an artifact of the killing readout.
**And the whole 2× spread in this paper's false-positive numbers is reproducible
inside Fig. 4A alone**, purely by choosing whether to subtract the OFF state. A
room about to be handed a false-positive budget should see how easily a factor
of two is manufactured out of nothing.

### Move 6 — DEBRIEF · The budget was written in the wrong units

- **Teaching point.** **You do not get to specify the classifier's output. You
  have to specify the effector's outcome.**
- **Phenomenon drawn.** hBax as a thresholded, amplifying effector: a little
  off-target output buys a lot of off-target death.
- **Derivation built.** Same dish, floor-subtracted both times. The circuit's
  **output** in HEK293 is **0.125** of its achievable range while its
  **killing** of HEK293 is **0.360** of achievable killing — same cells, same
  classifier, two readouts of the same event, a factor of **2.88×**. A
  classifier specified to a 12.5% output budget delivers a 36.0% kill rate.
- **Technique.** T69 closes — then multiply by a treated population and compare
  to one. T69's arithmetic and T63's are now literally the same, which is what
  closes PS9.

**The spine lists the framing as open; it is closed, and the spine is stale.**
NUMBERS §6.3 decides it: **the session carries the absolute pair**, 0.125
against 0.360, **2.88×**, because those two numbers are the ones a budget is
written on and each is a fraction of its own readout's range. The alternative
is the selectivity pair — 0.159 against 0.388, **2.44×** — which divides out the
on-target value, and HeLa's two on-target values are not equal (0.787 of range
in the reporter against 0.930 in the killer), which is the whole of why the two
factors differ. **The caveat goes on the surface:** the two ranges are set by
different controls — constitutively-repressed-to-constitutive for the reporter,
no-hBax-to-constitutively-active-hBax for the killer — so treating both as "a
fraction of the achievable range" treats two different normalizers as
commensurable. **This is INFERRED BY US; the paper neither computes nor comments
on it**, and the surface says so.

---

## 5 · The two fights with Adam's own prior material, resolved

Both are live because the 2023–2025 "Logic Therapies" block is **Adam's own**,
and both were put to him on 14 November 2026. These are the resolutions he
chose, not options.

### Fight 1 — his own prior lectures refute this session's arithmetic

**The problem.** This session takes a product over five markers; so does Xie's
Fig. 2C. Three slides earlier in his own prior block, the Gam 2018 material says
the product does not work. Slide 42: *"poor correlation between miRNA activity
and abundance."* Speaker notes, slides 44–45: *"We expected that miRNA
repression from these miRNA target sites would be fully independent such that we
could multiply the fold changes for each to generate a good prediction. But the
target sites appear to be largely non-independent"*; *"Emphasis: combined effect
is more complex than composition."* Slide 45 puts `min()` against the product as
competing models. **The session cannot multiply five responses silently.**

**Adam's decision, 14 November: name the product as Xie's model and state its
known failure where it is used; carry one figure panel putting `min()` against
the product on the real matrix; and fold non-independence into §7.2's
false-positive argument as a single sentence.** One slide, bounded cost.

**The panel, computed 14 November** (`_scratch/s26_minvsprod/minvsprod.py`,
which reproduces the validated HeLa 0.444059189 and 1.475135× exactly):

| model | HeLa | runner-up | margin |
|---|---|---|---|
| product | 0.444059189 | T47D 0.301030 | **1.4751×** |
| `min()` | 0.694308943 | T47D 0.600214 | **1.1568×** |

Two results, both on the surface.

- **The margin collapses by 22%**, 1.475× → 1.157×. A classifier meant to pick
  one line out of seven separates HeLa from T47D, under the pessimistic model,
  by sixteen percent.
- **The ranking of the negative lines changes.** Under the product MCF-7 is
  fifth and SH-SY5Y sixth; under `min()` they swap and land almost on top of
  each other, **0.0958 against 0.0965**. Which off-target line is the dangerous
  one is model-dependent.

And the mechanism is readable off one row: **under the product, five weak NOT
terms multiply into a strong rejection; under `min()`, you get only as much
rejection as your single best NOT term.**

**The framing to use, and it avoids an unverified claim.** The spine's reading —
that *"the data can't keep up with the increasing repression"* means saturation,
so the product **overestimates** selectivity — is an inference from one sentence
of a speaker note, Gam 2018 is not in this repo, and it is **[unverified]**.
It is also unnecessary. Non-independence means the truth lies between full
independence (the product) and complete dominance by one site (`min()`), so
**the two models bracket the answer: the real margin is between 1.157× and
1.475×, and nobody has measured where.** That is Gam's actual point, it is
rigorous without a claim about direction, and it is the shape of rule 6 — show
the evolution of the logic, including the wrong turn.

**Do not put the saturation claim on a slide** unless someone reads Gam 2018
and settles the direction. The bracket does the teaching without it.

### Fight 2 — a standing claim this session contradicts

**Slide 39 of the same block, stated flat: "In principle, can always increase
specificity with additional biomarkers."** Quote his own line, then test it.
This is the cleanest opening move 4 can have, and after Fight 1 it has **two
independent refutations on the same panel**:

1. **On Xie's real panel two of the five markers reduce the margin**, and
   dropping miR-21 breaks the classifier outright (§2.3).
2. **Under `min()` the fifth marker does nothing at all** unless it happens to
   be the minimum — so the claim is not merely false on this data, it is false
   in the model Adam's own later material prefers.

And §7.2 gives the limit from the other direction: **six negative lines cannot
bound the false-positive rate below 73%.** More markers cannot fix a panel that
small, because the bound is set by the number of negatives, not the number of
sensors.

---

## 6 · What a later pass must not undo

1. **The convention is marker levels**, settled 9 November, for a reason about
   teaching order and not about data handling.
2. **§2.2 is normative for assessment**, not §2.1's geometry. §2.1 printed
   products from unrounded values (0.433555) while §2.2 publishes three decimals
   whose correct product is 0.433615. An autograder keyed to the first fails
   every student who multiplies the second correctly.
3. **The five withheld SDs stay withheld.** Their drawn error bars are shorter
   end-to-end than the figure's own line weight, so they are not
   distinguishable from a dot. The means are sound and all 35 may be used; the
   five SDs may not, and must not be interpolated.
4. **`2.88×`, not `2.44×`** (§6.3), with the different-normalizers caveat on the
   surface.
5. **The 33.3% / 33.1% agreement is a coincidence** and the slide says so.
6. **No slide claims the paper demonstrated the alone-versus-mixture effect.**
7. **The saturation direction is unverified** and does not appear on a surface.

---

## 7 · The design ledger

Built the way session 6 established and `[[posb_teaching_derivations]]` rule 4
requires: the room's own list goes on the board at the end of move 1 — *you are
building this therapy; what can you choose, and what would you have to do to
change each one?* — and stays there until this ledger, which is **checked
against their list** rather than handed down.

| | |
|---|---|
| **Knobs** | **Which markers, and how many** — the choice the session shows actually moves the answer. **The threshold** on the product, which is a free parameter the room will reach for first and which does almost nothing over a 3.3× range (§7.1). **The effector**, and this is the knob the hour discovers: hBax is thresholded and amplifying, so a graded effector would change the output-to-outcome factor of 2.88× directly. **The delivered dose**, the treated population size, which is what turns a per-cell rate into a clinical count. **Which sensor architecture** — leak, ceiling and slope are properties of the RNAi sensor you build, not of the marker. |
| **Constraints** | The **panel is seven lines**, six negative, and that number alone bounds what any experiment on it can establish. **Markers are not independent** (Fight 1), so the product is a model and not a measurement. **Normalization is panel-relative** — add an eighth line and all 35 numbers change. **The two readouts have different normalizers** (§6.3), so output and outcome are not directly commensurable. |
| **Limits, each with its observable** | *More markers always buys specificity* — **false**, observable as two of five markers reducing the margin (§2.3) and as the fifth marker doing nothing under `min()`. *A clean panel proves specificity* — **false**, observable as `fp_rate_upper_bound(0, 6) = 0.393`: six clean lines bound the rate below forty percent, not zero. *Characterizing each line separately predicts the mixture* — **false**, observable as 0.145 alone against 0.360 beside its target, a factor of 2.48. *Meeting the output budget meets the budget* — **false**, observable as 0.125 of output range delivering 0.360 of achievable killing, a factor of 2.88. |

**The closing arithmetic, and it is T69's and T63's the same.**
`wrong_cells_per_dose` at 10⁹ delivered cells: the point estimate 2/6 gives
**3.3 × 10⁸** wrongly acted-on cells, the 95% upper limit 0.7287 gives
**7.3 × 10⁸**. **Against PS9's budget of one wrong cell, both fail by more than
eight orders of magnitude, and the distance between them is the part no
seven-line panel can close.**

One substitution is said out loud on the surface, because the library refuses it
by name in its own docstring: feeding 2/6 into `wrong_cells_per_dose` reads a
fraction of **cell lines** as though it were a per-cell rate. It is done anyway,
with that stated, because the order of magnitude is the lesson and the
substitution is itself worth teaching.

---

## 8 · Segments

**No furniture rule is applied, and none should be.** An earlier version of this
section cited a one-frame-per-move rule from the deck scope review; that rule was
**retracted** on 14 November after a blind critic showed it cuts exactly the
frames where the biological object gets drawn, which is rule 1 in reverse and the
most cohort-damaging cut available. Frames here are sized by what the room needs
to see, and release/debrief pairs are kept.

**This session does not need a cap, because it teaches one paper.** The review's
§2 finding is that length tracks the number of assigned papers, since rule 11
prices each at a setup plus its figures worked on a surface: sessions 20–23 teach
one paper each and run 42–50 slides, session 24 teaches six and runs 101. **s26
teaches one — Xie 2011 — and carries two techniques and one phenomenon**, so it
should land near the s20–s23 shape on its own, with every item on the protected
list carried in full: complete derivations, every question slide followed by
surfaces walking the answer, each paper figure worked rather than referred to,
and a graphic on every surface that asks for work.

**Carry a cut order.** Per the review's §4b, a deck this size records its own
graded cut order in DESIGN keyed to what each surface is assessed by. This
session's: **if short, cut the §3.2 Average-series digression to one line,
keeping the minimax sentence; then the §6.2 cross-readout check; then the
threshold staircase down to its two endpoints.** **Never cut** the Fight 1
panel, move 5's three guards, move 6's output-against-outcome comparison, or any
release/debrief pair — the first three are what the hour proves and the last is
deck-bar C2.

| segment | kind | what is on the surface | paper figure |
|---|---|---|---|
| deck | OPENING | the title claim and its condition, per §0 | — |
| deck | RETRIEVAL | session 23's escape fraction × 10⁸ against a budget of one; session 13's threshold on a continuous output; session 17's sensor characterization | — |
| deck | GOALS | the six moves' teaching points, in the words §4 gives them | — |
| 1 | FRAME | the seven lines and what they are; six of seven cancer; a false positive is the wrong cancer in a patient | SOM list |
| 1 | BOARD → LEDGER | *what can you choose, and what would you have to do to change it?* — the room's list, kept until §7 | — |
| 2 | BUILD | the printed expression, six markers and five modules; AND and NOT in RNAi; the sensor's leak, ceiling and slope, and the compositor-view bracket closed | `xie2011_expression` |
| 2 | BUILD | the `1 − r` conversion with its idealization stated; the normalization recipe; the exact-zero warning | — |
| 2 | BUILD | HeLa's five levels as a row; MCF-7's 0.998 on miR-21 against HeLa's 1.000; miR-141 at 0.904 doing the rejecting | `xie2011_fig2d` |
| 3 | FRAME | Fig. 2A's contour and its caption, verbatim — the only printed definition of a false positive in the paper | `xie2011_fig2a` |
| 3 | BUILD | the threshold staircase; 2 of 6 across 0.116–0.381; one step per negative line | own figure |
| 4 | BUILD | Fig. 2C's two series; the Minimal monotone run 1.02 → 6.61; the Average dip at three markers and why it is not a contradiction | `xie2011_fig2c` |
| 4 | BUILD | §2.3: HeLa is not the highest line on four of five sensors; the miR-21 gap of 0.0019 against MCF-7, 0.029 of HeLa's own SD | own figure |
| 4 | BUILD | **the Fight 1 panel** — `min()` against the product on the real matrix, both margins annotated, the ranking swap marked | own figure |
| 4 | QUESTION → ANSWER | Fight 2: his own *"can always increase specificity with additional biomarkers"* on the surface, then the two refutations, each walked | — |
| 5 | FRAME | Fig. 4B's design: two lines in one dish, DsRed⁺ counts, three conditions | `xie2011_fig4b` |
| 5 | BUILD | the SOM formula applied to both panels; 0.145 alone against 0.360 in the mixture; the control column; on-target unchanged 0.915 → 0.930 | `xie2011_fig3c` |
| 5 | BUILD | the three guards of §4 — the paper cannot resolve its own effect, the two confounds, and the 33.3/33.1 coincidence | — |
| 5 | RELEASE → DEBRIEF | the §6.2 cross-readout check that passes, and the factor of two manufactured inside Fig. 4A alone | `xie2011_fig4a` |
| 6 | BUILD | 0.125 of output range against 0.360 of killing range; 2.88×; the different-normalizers caveat; INFERRED BY US | own figure |
| 6 | CLOSE → LEDGER | §7's ledger checked against the room's board list; then 3.3 × 10⁸ and 7.3 × 10⁸ against a budget of one | — |
| deck | READING | the assignment for session 27 | — |

---

## 9 · What the build needs

**Library.** `posb.classifiers` is built for this session and carries 950 tests.
Functions the deck and the problem set both call: `normalize_responses`,
`marker_levels_from_sensor_outputs`, `classifier_output`, `sensor_response`,
`confusion`, `fp_rate_upper_bound`, `wrong_cells_per_dose`, `design_to_budget`,
`convention_check`, `marker_utility`.

**One library gap, and it is the one students will hit.**
`normalize_responses` takes a dict and `marker_levels_from_sensor_outputs`
takes a matrix, so they do not compose. Either add a helper or hand the room
the four-line recipe. **Recommended: add the helper**, because the problem set
will otherwise ship the same four lines in every student's notebook and an
autograder has to accept all of them.

**Own figures to build.** The threshold staircase; the per-sensor margin picture
for §2.3; **the Fight 1 `min()`-against-product panel**; the output-against-
outcome comparison for move 6. Four.

**Paper crops to add to `decks/paper_figures.yaml`.** The printed expression
(p.1308), Fig. 2A, Fig. 2C, Fig. 2D, Fig. 3C(right), Fig. 4A, Fig. 4B. Seven.
Route them through a local aspect-aware crop helper as s24 does — `theme.paper_figure`
letterboxes into the box it is handed and then reports a slot-larger-than-figure
problem when the aspects disagree.

**Numbers.** All from `NUMBERS.md`, which is generated below line 92. **The
Fight 1 panel's two margins are not yet in it** — they are in
`_scratch/s26_minvsprod/minvsprod.py`. To publish them, edit
`_scratch/s26_xie/emit_numbers_md.py` and re-emit. **Do not hand-edit
`NUMBERS.md`.**

---

## 10 · Decisions for Adam

1. **Fold the Fight 1 margins into `NUMBERS.md`?** It means editing the
   generator and re-emitting a 1110-line published artifact. The numbers are
   verified and reproduce the validated HeLa output exactly.
2. **Add the compose helper to `posb.classifiers`**, or hand the room the
   recipe? Recommended: the helper, for the autograder's sake.
3. **The `min()` panel's axis.** Recommended: plot both models' outputs for all
   seven lines on one axis, with the two margins annotated and the MCF-7 /
   SH-SY5Y swap marked, rather than two panels side by side — one axis makes the
   bracket visible as a gap and two panels make it a comparison the room has to
   do itself.
4. **Does anyone read Gam 2018 before 24 November?** Without it the saturation
   direction stays off the slides and the bracket carries the lesson. With it
   the session could say which end of the bracket the truth is nearer, which is
   a stronger close to move 4. Not required.
