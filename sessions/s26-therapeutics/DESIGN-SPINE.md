# Session 26 — the spine, as settled with Adam on 8 November 2026

**Tue 24 Nov. Therapeutic circuits: logic-gated cell therapies, synNotch, in
vivo delivery. Worked example: design a multi-input classifier to a
false-positive budget.** Reading: Xie et al., *Science* 333, 1307 (2011),
with its SOM. Assessed: **T69** (AUTO, PS9 + final), **T70** (HAND, PS9).

Adam approved this on 8 November. The full DESIGN.md is built from it.

## The thesis, which is assigned rather than chosen

`docs/course-map.md` makes sessions 26–28 **the same object three times — a
classifier with a threshold and a budget for its mistakes** — and gives each
session one thing a population does that a circuit cannot. **Session 26's is:
the population is the thing being classified, and specificity is a population
statistic.**

`private/sources/ps09-PLAN.md` §1 then binds the arithmetic. PS9's two ends are
the same calculation: T63 is a per-cell escape fraction × 10⁸ CFU against a
budget of **one**; T69 is a per-cell error rate × a treated population against a
budget of **one**. *"Same shape, opposite sign — one is a device that must not
act, the other a device that must not act on the wrong cell."* The set opens on
the first and closes on the second.

**So T69 is a COUNT, not a fraction.** An earlier draft of this spine framed it
as "pick a marker set and threshold that meets a budget", fraction against
fraction. That does not close the set. The population size is what turns a
per-cell rate into a clinical event, and arguing about it is T70.

## The six moves

**1 · FRAME — what "specific" means here, and it is not what the title says.**
The seven cell lines, from the SOM's own list: HeLa (cervical cancer, the one
POSITIVE), MCF7 / SKBR3 / T47D (breast), DAOY / SH-SY5Y (brain), HEK293
(embryonic kidney). **Six of seven are cancer lines; five of the six negatives
are cancer.** The circuit separates one cell type from six others. **A false
positive is the wrong cancer, in a patient.** Costs no digitization, comes off
a printed list, and it is the session's thesis rather than a correction to a
title.

**2 · BUILD — a classifier is a threshold on a product, not a Boolean circuit.**
The printed expression (p.1308), six markers, **five** sensor modules (miR-17
and miR-30a share one). How AND and NOT are implemented in RNAi. The move the
room must make: the logic is continuous, with a cut on it. That is what makes a
budget possible.

**3 · BUILD — the false positive is DEFINED, and the definition is a choice.**
Fig. 2A's caption prints it: the contour is input combinations giving **20%
output relative to HeLa**, and dots above it are false positives *"for this
specific circuit configuration."* **You do not get a classifier. You get a
family of them, indexed by a threshold.**

**And the family is coarse, which is the second half of the lesson.** On §2.2's
published table the false-positive set is **SKBR3 and T47D for every threshold
from 0.116 to 0.381** — a factor of 3.3 in a number the paper chose and did not
defend, over which nothing changes (NUMBERS §7.1 gives the full staircase). The
threshold is a free parameter the room will want to tune, and tuning it does
almost nothing. What moves the answer is which markers you hold, not where you
put the cut.

**4 · BUILD — design to a budget, and watch the composition look good.** From
Fig. 2D's 7×5 response matrix: pick markers and a threshold, get a per-cell
error rate. Fig. 2C says more markers buys selectivity — minimal ~6-fold,
average ~160-fold at 5–6 markers, both corroborated by printed prose.

**The Average series dips by 2.65× at three markers, and it is not a
contradiction with the prose** (NUMBERS §3.2). The caption says the circuit at
each marker count is chosen to maximize the *worst* output ratio; the Average is
a by-product of that choice and is optimized for nothing. The Minimal series is
monotone 1.02 → 2.10 → 2.40 → 5.34 → 6.61 over one to five markers, exactly as
p.1308 claims. So the beat is not "read the figure over the sentence" — it is
**the quantity you optimize is the quantity that behaves; everything else is
free to move.** That is a minimax lesson a room of engineers should own, and it
is free here.

**5 · RELEASE / DEBRIEF — Fig. 4B. Now put them in one dish.**
HeLa-EYFP and HEK293-Cerulean **in the same mixture**, DsRed⁺ counts of
surviving transfected cells, three conditions. **Digitized** (§5.1): the
classifier kills **75.0% ± 5.6** of the cells it is meant to kill and
**33.1% ± 7.6** of the cells it is meant to spare.

Scored by the SOM's own killing-efficiency formula (§4.3), off-target killing is
**0.360 ± 0.082** in the mixture against **0.145 ± 0.267** for HEK293 measured
alone in **Fig. 3C(right)** — a factor of **2.48**, not the 2× this spine was
scoped on. On-target killing does not move: 0.915 → 0.930. **The control column
is what rules out "the two panels are on different scales,"** which is the first
objection the room will raise.

**And the paper cannot resolve its own effect.** The gap is **0.81 of
Fig. 3C's own plotted SD** (§5.4), and Fig. 3C(right)'s HEK293 bar has
**SD/mean = 1.84**, drawn with no lower cap because the lower arm falls below
zero (§4.1). A slide may not say the paper showed this. §5.4's defensible
sentence is the one to use: the same circuit, same formula, 15% off-target alone
and 36% beside its target, on-target unchanged — **and nobody measured it well
enough to know their own false-positive rate.** That lands harder than a clean
2× would. Two structural confounds come with it (unmodified HEK293 under table
S3B versus HEK293-Cerulean under table S4), and the session says so rather than
being caught by it.

**An independent check, and it passes** (§6.2). Fig. 4A is a reporter — no
apoptosis, different panel, different experiment. The circuit's HEK293 output is
**0.320** of its HeLa output against Fig. 4B's measured **0.331**: agreement to
1.1 points. The false-positive rate is not an artifact of the killing readout.
And the whole 2× spread in this paper's false-positive numbers is reproducible
**inside Fig. 4A alone**, purely by choosing whether to subtract the OFF state.
A room about to be handed a false-positive budget should see how easily a factor
of two is manufactured out of nothing.

**6 · DEBRIEF — the budget was written in the wrong units.**
NUMBERS §6.3, INFERRED BY US; the paper neither computes nor comments on it. In
the same dish, floor-subtracted both times, the circuit's **output** in HEK293 is
**0.125** of its achievable range while its **killing** of HEK293 is **0.360** of
achievable killing. Same cells, same classifier, two readouts of the same event:
**a classifier specified to a 12% output budget delivers a 36% kill rate.** hBax
is a thresholded, amplifying effector — a little off-target output buys a lot of
off-target death. **You do not get to specify the classifier's output. You have
to specify the effector's outcome.**

> **Open, and it must close before DESIGN.** §6.3 states this two ways that do
> not give the same factor: 0.125 → 0.360 absolute is **2.88×**, and the
> ratio-of-ratios 0.159 → 0.388 is **2.44×**. Both are in §6.3. The session must
> pick one framing and one number.

That is the hour: you can characterize every sensor in isolation, compose them,
predict selectivity from the composition, hit your output budget — and a third
of the wrong cells still die. **Specificity is not a property of the circuit, is
not recoverable from per-line characterization, and is not even measured in the
units the budget was written in.** Then multiply by a treated population and
compare to one. T69's arithmetic and T63's are now literally the same.

Move 4 earns the prediction. Moves 5 and 6 break it twice, for two different
reasons.

## Three questions, answered

- **synNotch and in vivo delivery stay in the syllabus line with no move of
  their own.** synNotch is a different *implementation* of the same object; in
  vivo delivery is **where move 5's population multiplier comes from**. They
  frame the budget rather than compete with it.
- **The reading is Xie, and `docs/reading-plan.md`'s open Xie-or-Tousley line
  should close.** Tousley was offered on the grounds that its failure mode is
  "threshold sharpness"; the paper does not support that framing — the word
  appears once, to say the work was not done, and its Source Data has no sheet
  for the in vitro specificity figures. Better access, no numbers.
- **The treated-population number is the STUDENT's**, not ours. With Fig. 4B's
  measured 33% in hand they have something to check a designed rate against, so
  they pick a population and defend it. **T69's autograder checks the
  arithmetic and the direction, not the value.** That is also what makes T70 a
  real question.

## Two library decisions, settled 8 November

**1 · SETTLED 9 November — MARKER LEVELS, and the session starts from what you
would measure in the cell.** Adam's call, and his reason reorders the session
rather than just the data handling: *start with what we would measure in the
cell to drive design and operation.* Marker abundance is what you would assay
in a patient sample and what you would design a circuit against. Fig. 2D's bars
are a measurement of **one paper's circuit**, not of the cell, so they get
converted back before the room reasons about them. **This is also how the
material was taught in prior years** — the "Logic Therapies" block, three
lectures in 2024 and 2025 and four in 2023; that treatment is being read and
this decision will be reconciled with it.

**Validated end to end, 9 November, and the arithmetic is Xie's own.** Normalize
the published table, convert at the boundary with
`marker_levels_from_sensor_outputs`, then run `classifier_output` with the three
T-markers declared `absent`: HeLa **0.444059189**, margin **1.475135×**,
`convention_check` ok with `alternative=None`, `sense_check` silent, and the
round trip identity to 5.6 × 10⁻¹⁷. **Bit-identical to the sensor-output route**,
same ordering — so the decision costs nothing in the numbers and buys the three
NOTs in the student's code.

**What the levels table shows that the sensor table cannot, and it is move 2's
best beat.** HeLa's row reads 1.000 / 0.950 / 0.192 / 0.167 / 0.306 — **the
Boolean expression, visible as a row of numbers**: two high, three low. Then
MCF-7 reads **0.998** on miR-21 against HeLa's 1.000. *The marker a student
reaches for first does not separate the two lines at all.* What rejects MCF-7 is
miR-141 at 0.904, and that one NOT term costs it a factor of ten. Every line in
the panel has a specific NOT term doing the work of rejecting it, and the levels
table is where you can point at which one. In sensor outputs it is buried.

**Two costs, both to be handled in the problem statement.**

- **The two functions do not compose.** `normalize_responses` takes a dict of
  responses; `marker_levels_from_sensor_outputs` takes a matrix. The student has
  to normalize, rebuild the matrix, then convert. Hand them the recipe
  explicitly or add a helper — this is the thing most likely to cost a student
  an hour, replacing the convention confusion that used to hold that title.
- **Per-column normalization forces exact zeros.** HEK293's miR-141 and miR-146a
  levels and MCF-7's miR-142(3p) level all come out **0.0000**, which reads as
  "this marker is wholly absent" when it only means *this line is the panel's
  maximum on the inverted sensor*. Say so on the slide. It is also a second
  instance of the panel-relative point: add a cell line and every number moves.

**And §2.1's label obligation stands.** Everything downstream of the conversion
is **MODELLED**, not DIGITIZED, because `1 − r` inverts an *idealized* sensor and
a real RNAi sensor's leak, ceiling and slope get absorbed into whatever "level"
comes out — session 13's object, which the room has already met. Say that at the
conversion, not in a footnote: it is the one place the session admits that its
central table is a model of a measurement rather than a measurement.

**The decision, as it now reads:**

**The matrix is in MARKER LEVELS, and the conversion happens at the data
boundary.** `classifier_output` takes normalized levels where 1.0 means the
marker is PRESENT, so an `"absent"` marker contributes `1 - r` and **the three
NOT terms in the printed expression are visible in the student's code.**

Fig. 2D plots **sensor outputs**, already oriented so HeLa reads high in every
series — the NOT is baked into the sensor. Feeding those straight in applies
the inversions **twice, silently**. `marker_levels_from_sensor_outputs`
converts at the boundary, and that conversion is a **modelling step, not
bookkeeping**: `1 - r` inverts an *idealized* sensor, and a real RNAi sensor's
leak, ceiling and slope are absorbed into whatever "level" comes out. Say that
on the slide.

The alternative is Xie's own — treat the sensor outputs as the quantities the
product runs over and declare every sense `"high"`. Defensible arithmetic, and
a worse teaching object: three NOTs on p.1308 and none in the code.

**The decisive check, and it is one multiplication per line:** under the right
convention HeLa is the **strict maximum** of the five-marker product across all
seven lines. Verified against the digitized matrix — HeLa 0.4336 against T47D
0.2938, **1.48×** from the full-precision geometry and **1.4751×** from §2.2's
published three-decimal table, the same ratio measured on two different
precisions — and verified to fail the other way: read as marker levels, SKBR3
wins and HeLa comes second (§2.1).

**The second half of this check now holds, after a repair to the library on
8 November.** `sense_check` used to fire on the *correct* matrix — on T142(3p),
with a false causal claim about double inversion — and on four of the five
leave-one-out subsets of a correct configuration. The conflated check is now
split: **`convention_check`** answers the convention question panel-wide and is
gated on this section's own decisive test, so a configuration that passes the
paper's test cannot raise a convention warning by construction; **`marker_utility`**
reports per-marker discriminating power as a table that never accuses. False
convention alarms on leave-one-out subsets went 4 of 5 to **0 of 5**, and
`sense_check` is silent on the correct matrix. **But silence is not the check to put in the problem statement.** `sense_check()
== []` is strictly stronger than "the convention is right": it also reports
degenerate and insufficient marker sets, so it is non-empty for configurations
whose convention is perfectly correct. A student handed "pick your own markers"
will produce exactly those configurations, and a problem statement that equates
silence with a right convention tells a student with a legitimately weak subset
that their convention is broken. That is the category error we just took out of
the code, re-created in prose.

**State the property, and name the field that answers the narrow question.** The
property is: **HeLa is the strict maximum of the five-marker product across all
seven lines** — one multiplication per line, and on §2.2's published table that
is HeLa 0.433615 against T47D 0.293949, a margin of **1.4751×**. The call is
`convention_check(responses, markers, sense, "HeLa")`, and the field for
*convention* is **`.alternative is None`**: no other reading of the matrix beats
the one you declared. Read `.ok` and `.margin` for whether the design is any
good — `.ok` is False whenever the positive is not the strict maximum, which an
insufficient marker subset causes with no convention error at all.

**Strictness matters, and for a guaranteed reason rather than a possible one.**
`normalize_responses` sets exactly one entry per column to 1.0, so declaring
*any* marker `absent` on a normalized table contributes exactly 0 in whichever
line is that column's maximum — always, not sometimes. Read Fig. 2D as marker
levels and HEK293, MCF-7 and SH-SY5Y all land on exactly 0.0; invert all five
senses and **HeLa itself** dies, because HeLa is P21's column maximum. The
seven-way tie at zero is a separate mechanism, needing an exact zero in every
row, and that is the one that would read as the positive line winning. NUMBERS must state which convention its table is in,
in the table's own header. **This is the thing most likely to cost a student an
hour.**

**2 · `fp_rate_upper_bound` stays, and session 26 derives its zero-event case.**
It is machinery this course has not otherwise built by hand, which is normally
a reason to keep something out of `posb/`. It stays because **it is the
sharpest available form of T70** and the case that matters is one line:

> P(0 false positives in n negative lines) = (1 - p)^n = alpha,
> so p < 1 - alpha^(1/n). At n = 6 and 95%, **p < 0.393**.

Verified against the built library: a panel with **zero observed false
positives in six negative lines still permits a 39.3% false-positive rate.**

**And the step from there to a count of cells is a modelling leap that has to be
named out loud, because it is T70.** What the panel measures is a fraction of
**cell lines**; what a dose multiplies is a per-**cell** rate, and those coincide
only if every cell type is equally abundant in the patient. `posb.classifiers`
enforces the distinction, and its two docstrings are worth reading side by side:
`wrong_cells_per_dose` refuses its input with *"a fraction of misclassified CELL
LINES is not this quantity, even though it is also a number in [0, 1]"*, while
`fp_rate_upper_bound` calls itself *"an OPTIMISTIC bound on a quantity the panel
does not measure"* and asks to be read as an order of magnitude. Both are right.
Passing the bound into the dose is legitimate **only as an acknowledged leap**,
and 393,000 wrong cells in a population of a million is that leap taken once,
with the abundance assumption stated. **A student who multiplies the two without
noticing has answered T69 and missed T70.** That is what makes T70 a real
question rather than a number to defend.

That is a better limit than Fig. 4B's measured 33%, and it is a different
limit: Fig. 4B says the mixture is worse than the per-line assays predict;
this says **the panel was never large enough to see a rate that matters.** Both
belong in move 5. The general non-zero case rests on the same logic and the
student may use it without deriving it.

## The prior treatment, read 9 November — and the two places it fights this session

Adam: *"We have taught this in previous years. Take a look at those slides."* The
block is **"Logic Therapies"** — 2025 Lectures 13–15, 2024 Lectures 13–15, 2023
Lectures 16–19. All ten decks read. **There is one canonical sequence and all
three years are textually identical** where they overlap; 2024 L13 and 2025 L13
differ only in the filename. So there is nothing to adjudicate between years.
Citations below are 2025 L13, the canonical copy. Extracted text is parked at
`_scratch/s26_priors/`.

**It already works in marker levels, which is why the decision above is a
return rather than a change.** The chain is explicit: slide 21 hands the room
the measurements — *"In our cancer cell of interest, and no other cell: A=HIGH,
B=LOW"* — slide 22 writes the specification **`= A and NOT(B)`** and builds the
gate circuit, and slide 41 names the pipeline outright: **Truth table → Logic
circuit → Genetic circuit**. The inversion is Boolean and narrated as a mapping
between concentrations, never as arithmetic: the speaker note on slides 22, 27
and 28 defines the INVERTER's input as *"the concentration of molecule B in the
cell"* and its output so that *"when protein B concentration is LOW, then the
concentration of R1 is HIGH."* **No `1 − x` appears anywhere in ten decks.**

**Xie is one slide, and it is validation rather than data.** 2025 L13 slide 47,
*"HeLa cervical cancer classifier circuit in action"*, cited `Xie, et al.,
Science (2011)`, carrying absolute GFP expression, single-plasmid against
six-plasmid, HeLa against HEK293, cell killing. **Fig. 2D is never shown in any
year.** What the room reasons from is the generic five-marker HI/LO table on
slides 39 and 41 — A–E against two tumor subtypes and two healthy cells. **There
is no per-cell-line marker-abundance table anywhere in the archive.** So s26
having students convert Fig. 2D back to levels and reason from the real matrix
is **new work, not a callback**, and the table it produces has no precedent.

**The minimum-marker poll is the direct ancestor of §2.3.** 2024 L15 slide 5
(image-only, read at the pixel level on 9 November) asks *"For the diagnostic
panel below, what is the minimum number of biomarkers needed to selectively
target cancer cells?"* over that same A–E panel, offering 1 through 5. **The
answer is 2** — B high and D low separates both tumor subtypes from both healthy
lines. So the room has already been asked to find a minimal marker set on a
clean HI/LO panel. §2.3 is that question asked again where levels are
continuous, the panel is real, and dropping a marker has consequences the clean
version cannot show.

### Fight 1 — his own later material refutes this session's arithmetic

s26 takes a **product** over five markers, and so does Xie's Fig. 2C. The Gam
2018 material three slides earlier says the product does not work. Slide 42:
*"poor correlation between miRNA activity & abundance."* Speaker notes, slides
44 and 45: *"We expected that miRNA repression from these miRNA target sites
would be fully independent such that we could multiply the fold changes for each
to generate a good prediction. But the target sites appear to be largely
non-independent"*; *"the data can't keep up with the increasing repression,
indicating that the repression from the three-input sensors are not independent
from one another"*; *"Emphasis: combined effect is more complex than
composition."* Slide 45 puts `min()` against the product as competing models.

**This is the sharpest unresolved thing in the s26 design and it needs Adam.**
The session cannot multiply five sensor responses in silence when the same
course teaches, in the same block, that multiplying them does not predict the
measurement. Three ways out, in increasing ambition: name the product as Xie's
model and state its known failure at the moment it is used; make the
non-independence the session's own limit on the budget, which fits §7.2's
argument that nobody has measured their own false-positive rate; or put `min()`
and the product side by side on the real matrix and let the room see how far
apart they land.

**One thing to check before any of these reaches a slide, and it is not yet
established.** *"The data can't keep up with the increasing repression"* reads as
saturation — real repression falling short of what the product predicts — which
would mean the product **overestimates** selectivity and the true false-positive
rate is worse than the matrix says. That would compound §7.2 rather than
contradict it. **But the direction has not been verified**, only inferred from
one sentence of a speaker note. Settle it against Gam 2018 before building on it.

### Fight 2 — a standing claim this session contradicts

Slide 39, stated without qualification: **"In principle, can always increase
specificity with additional biomarkers."** §2.3 shows that on Xie's real panel
**two of the five markers reduce the margin** and dropping P21 breaks the
classifier outright, and §7.2 shows six negative lines cannot bound the
false-positive rate below 73%. The old claim is the optimistic form of exactly
what this session takes apart. **Stage the confrontation rather than leaving the
claim standing** — quote his own line, then test it on the real panel. That is
the cleanest available opening for move 4.

### A note he has carried for three years, which this session can close

Speaker notes, slides 22, 27 and 28, in his own brackets:
**`[DIFFERENT THAN THE COMPOSITOR VIEW, BUT WILL FIX LATER]`** — the Boolean
inversion does not line up with the parts-and-compositors transfer-function
treatment taught earlier in the course. That is precisely the seam the `1 − r`
conversion walks into, and §2.1's sentence is the fix: `1 − r` inverts an
*idealized* sensor, while a real RNAi sensor has a leak, a ceiling and a slope.
**Saying that at the conversion closes a note he has carried since 2023.**

### What the archive does not have, and s26 must supply

- **No numerical threshold, anywhere.** Markers are HI or LO by assertion in
  every year. The only threshold symbols in these decks (`IL`, `IH`, `OL`, `OH`,
  `ML`, `MH`) belong to the downstream Cello material, not to the classifier.
  Xie's printed 20% cut (§7) is therefore the room's first numerical threshold
  for a marker, and move 3 should know it is carrying that weight.
- **No per-cell-line marker levels.** Covered above.
- **No false-positive discussion at all.** The string does not occur in ten
  decks. The session's payoff is new material rather than a callback.

### Symbol collisions already present in his decks — for `docs/symbols.md`

Within the single Logic Therapies session, **`A` carries four meanings**:
biomarker A (slides 21–34), a row label in the five-marker table (39, 41),
activator `A1`–`A3` (35–36), and part number `A1`–`A16` in the plasmid library
(50). Also `HIGH`/`LOW` against `HI`/`LO` two slides apart, and bare integers
1–4 as target-site indices on slide 45 where `0`/`1` are Boolean levels
elsewhere. **Within-session collisions are the damaging kind**, and s26 inherits
this neighborhood.

## Limits, each with an observable

- **The false-positive rate is poorly determined in the paper itself.**
  Fig. 3C(right)'s HEK293 killing efficiency is 0.145 with a plotted SD of
  0.267 — **SD/mean = 1.84.** The bar excludes neither zero nor 0.4, and its
  lower arm is **drawn with no cap** because it would fall below the axis.
  *Observable:* the missing cap. NUMBERS §4.1 calls this the single most
  important caveat in the file.
- **No single sensor identifies HeLa.** Counting negatives that read higher than
  HeLa: P21 0 of 6, P17-30a 1, T141 3, T142(3p) 4, T146a 5 — and on P21, the one
  sensor HeLa leads, it leads MCF-7 by 0.002 against its own plotted SD of
  0.066. **The identification exists only in the product.** Derived from §2.2.
- **No sensitivity, specificity, FPR or FNR appears anywhere in numeric form.**
  The only false-positive sentence (p.1311) is qualitative.
- **Seven lines is a convenience sample**, n = 3 flow cytometry experiments,
  one positive class of one.
- **Every response value is DIGITIZED.** The supplement's tables are
  transfection recipes, not data (NUMBERS §0.1).

## What gets built

| piece | state |
|---|---|
| `sessions/s26-therapeutics/NUMBERS.md` §0 | written — **and §1 on is GENERATED: a 92-line hand-written §0 header plus the stdout of `_scratch/s26_xie/emit_numbers_md.py`. Never hand-edit below line 92; edit the generator and re-emit.** |
| NUMBERS §1–§8 — full digitization, all panels | written |
| NUMBERS §2.3, §7.1, §7.2 — per-sensor finding, the 20%-cut FP analysis, the coincidence warning | written (767 → 1110 lines) |
| `posb/classifiers.py` + `tests/test_classifiers.py` | built, **950 tests passing**; sign guard split into `convention_check` + `marker_utility`; Fig. 2D fixture is a drift-guarded mirror of §2.2 |
| `sessions/s26-therapeutics/DESIGN.md` | next, from this spine — **blocked on the convention decision above** |
| `figures/s26_therapeutics.py` | after DESIGN |
| `decks/s26_therapeutics.py` | after figures |
