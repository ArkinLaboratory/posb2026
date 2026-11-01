# Session 20 — NUMBERS


> **SUPERSEDED IN PART, 26 October 2026.** The two-cause story below — one failure a missing route, the other a wrong objective — is NOT what Fong & Palsson conclude. Their only diagnosis covers BOTH genes and is network incompleteness (p. 1057). Eleven is 8 + 3: eight are ppc or tpi, three are single replicates the authors decline to diagnose. The model was also RIGHT about tpi on malate and succinate. The deck's segment 7 carries the corrected version; prefer it.
Read off the PDFs on **26 October 2026**: the 3-page article plus all three
supplementary files, which arrived that morning. **Record the kind, not only the
value** — for this session the kinds *are* the argument.

Held: `Session 20 - fong-palsson-2004-deletion-strains-evolve-to-predicted-phenotypes.pdf`
and its SI as `-SI-table1-uptake-rates`, `-SI-fig1-evolution-trajectories`,
`-SI-methods`.

---


## 0 · What this session now contains — rebuilt 31 October

**Read `REBUILD.md` first; it is the specification.** This file is the number
record and the sections below predate the rebuild except where they say
otherwise. The structure is now:

| segment | moves | what was added |
|---|---|---|
| 1 | frame, build ×6, release, debrief | why the method exists; the pathway drawn in four reveal stages; the acetate branch as a decision; the release rewritten so it is answerable; the matrix annotated |
| 2 | build ×2, debrief | the flux cone |
| 3 | frame, build, debrief | the bounds frame; the six lines as a derivation surface rather than board-only |
| 4 | frame, build ×2, release, debrief ×2 | the biomass flow traced back; one deletion worked |
| 5 | frame ×2, release, debrief ×2 | the coupling frame, moved here from segment 4 |
| 6 | frame, build ×2, release, debrief | **Fig. 1a**; a release that reads it; "Evolved" moved to the debrief |
| 7 | release, build, debrief | **Fig. 1b**, lactate and malate |

**Paper figures shown: 3** (Fig. 1a, Fig. 1b lac/mal, Supplementary Fig. 1),
against 1 before the rebuild.

### Numbers added by the rebuild, all verified

- **Overflow.** A fast-growing *E. coli* excretes acetate with oxygen present;
  as much as **15%** of the glucose carbon can leave that way — Holmes, *Curr
  Top Cell Regul* **28**:69 (1986), which is where Zeng & Yang, *BMC Syst
  Biol* **13**:3 (2019), Background, take it from. Zeng & Yang are an FBA
  modeling paper and measured nothing; cite them and the slide names the
  wrong kind of source. The mechanism is proteome cost:
  *"the proteome cost of energy biogenesis by respiration exceeds that by
  fermentation"*, measured by quantitative mass spectrometry — Basan, Hui,
  Okano, Zhang, Shen, Williamson & Hwa, *Nature* **528**:99–104 (2015). Senior
  author Terry Hwa, who is also the Hwa of Scott, Gunderson, Mateescu, Zhang &
  Hwa (2010), session 19's paper. **Kind: measured for Basan; for the 15%,
measured by Holmes and reported secondhand by Zeng & Yang.** The toy's
  1-against-3 ATP ratio is **ours**, chosen so the board arithmetic stays in
  integers; the real per-pyruvate ratio is nearer an order of magnitude, and
  the slide says so.
- **The flux cone.** Projected onto (v_ackA, v_tca) with uptake ≤ 10, the
  feasible set is exactly the triangle **v_ackA + v_tca ≤ 20** — ten glucose
  is twenty pyruvate, and nothing else in the chemistry bounds the branch.
  With **no** cap on uptake, every point of the positive quadrant is feasible;
  checked directly, not assumed. Biomass over the triangle runs 0 to 4.
  **Kind: computed from `posb.fba`, in the figure, nothing typed in.**
- **Fong's own numbers, from the paper.** Every evolved strain gained at least
  **15%**; across the **46 of 50** that grew the average increase was **87%**
  (p. 1057). The four that did not grow are tpi⁻ on malate and succinate, in
  duplicate — and those are the model's **correct** no-growth calls. The
  authors name a candidate for the missing chemistry: *"possibly activation of
  the methylglyoxal bypass"* (p. 1057).
- **Duplicates and alternate optima** (for the rewritten home guide §4).
  Computed on the teaching network at uptake ≤ 10: duplicating **v_tca** gives
  biomass 4 with v_tca and v_tca2 each free over [0, 4] and **both** coupled
  pairs surviving; duplicating **v_ackA** gives biomass 4 with **nothing**
  free, because ackA carries no flux at the optimum. Duplicating v_zwf — the
  class case — frees that pair and kills the zwf/biomass coupling.
  **The two conditions are different**: a duplicate creates alternate optima
  only if the copied reaction carries flux at the optimum, and breaks a
  coupling only if it adds an entry to a row of S that had exactly two.

---

## 1 · THE CENTRAL CLAIM, corrected by reading the supplementary methods

The headline number is **39 of 50 (78%)**, from the article's own abstract. But
the Supplementary Methods change what it is a claim *about*, and the corrected
form is the one that goes on the slide:

> **Given the experimentally measured substrate and oxygen uptake rates as
> inputs, flux balance analysis on a 904-gene, 1327-reaction *E. coli* model
> predicted the growth rate of 39 of 50 *evolved* deletion strains to within
> 10%.**

Three qualifications, each read off a page, each load-bearing:

| qualification | source |
|---|---|
| The uptake rates are **measured and fed in**, not predicted. *"For direct comparison with experimental strains, experimentally determined substrate and oxygen uptake rates were used as input parameters for the computational simulations."* The values are **Supplementary Table 1** | SI Methods, p. 1; SI Table 1 |
| The strains are **evolved**, not naive. Supplementary Fig. 1 is the time course — normalised growth rate against DAYS of evolution (0-50) for each replicate on each substrate | abstract; SI Fig. 1 |
| **"Right" means within 10%** — Fig. 1's arrows mark the strains that deviate by more than that | Fig. 1 caption |

**So the model is handed its own boundary conditions and asked for one number.**
That is a real and useful result, and it is *not* "the genome predicts growth."
Any slide that drops a qualification is wrong in the way the week-9 and week-10
retrospectives are about.

## 2 · Supplementary Table 1 — the model's inputs, measured

mmol/g-DW/hr. SUR = substrate uptake rate, OUR = oxygen uptake rate. **Kind:
measured.**

| carbon source | SUR | OUR |
|---|---|---|
| α-ketoglutarate | 13 | 17 |
| glucose | 10 | 17 |
| glycerol | 17 | 19 |
| lactate | 20 | 30 |
| malate | 17 | 19 |
| ribose | 10 | 15 |
| succinate | 13 | 17 |

**`readings.yaml`'s focus note is wrong about this table.** It says *"Supplementary
Table 1 and the predicted-against-observed comparison."* Supplementary Table 1 is
**not** the comparison — it is the uptake rates. The comparison is **Figure 1** in
the article, and the evolution time course is **Supplementary Figure 1**. Focus
note corrected the same day; the table is still worth sending students to,
because *noticing that these are measured inputs* is the whole qualification in §1.

## 3 · The design

**Kind: design.** Six in-frame deletions, built by homologous recombination with
the λ red system in *E. coli* K-12 MG1655 (SI Methods):

| gene | enzyme (article's own wording, p. 1056) |
|---|---|
| **ackA** | acetate kinase A |
| **frd** | fumarate reductase |
| **pck** | phosphoenolpyruvate carboxykinase |
| **ppc** | phosphoenolpyruvate carboxylase |
| **tpi** | triosephosphate isomerase |
| **zwf** | glucose 6-phosphate-1-dehydrogenase |

**50 evolved strains** across **24 gene-substrate cases** — 22 in duplicate,
2 in triplicate. Supplementary Fig. 1 is a 6 × 4 grid of those 24 cases, and
labels the replicates ack1–2, frd1–2, pck1–3, ppc1–2, tpi1–2, zwf1–2. Those
**thirteen labels repeat in every panel of a column** and are not a lineage
count; the deck caption said "thirteen parallel lineages" until 31 October.

**The model: 904 genes, 1327 reactions** (SI Methods) — iJR904, which is Reed,
Vo, Schilling & Palsson, *Genome Biol* 4, R54 (2003), held as an instructor
companion. A knockout is simulated by **deleting the reactions associated with
the gene from the reaction list**, which is the paper's own description and is
exactly the one line of code session 20 teaches.

## 4 · The eleven failures, and they do NOT share a cause

**Kind: measured against predicted.** This is the payoff surface.

**CORRECTED 31 October. The table below used to have two rows and a tidy moral
(tpi⁻ structural, ppc⁻ a gap in the objective). All of that was wrong, the deck
was rebuilt on 26 October against the paper, and this file is now catching up.
IF THIS FILE AND `decks/s20_metabolic.py` EVER DISAGREE ON THIS SECTION, THE
DECK IS RIGHT — its `_failures` function carries the quotes.**

Eleven is **8 + 3**, and the 3 are not diagnosed by the authors:

| failure | what went wrong | kind |
|---|---|---|
| **tpi⁻** on **lactate** | No growth predicted; it grew above 0.70 h⁻¹ | predicted (structural) |
| **tpi⁻** on **glucose** | Grew **~33% slower** than predicted | measured vs predicted |
| **ppc⁻** on **glucose** | Grew **~28% slower** than predicted | measured vs predicted |
| **ppc⁻** on **α-ketoglutarate**, both replicates | Grew **11–12% slower** than predicted | measured vs predicted |
| **pck⁻** on α-ketoglutarate; **zwf⁻** on glucose and on glycerol | **The other three.** Single replicates only; the authors decline to diagnose them — *"may be a result of experimental and evolutionary variability"* | unexplained, and the paper says so |

**Two things the old table got backwards and that are quotable against it:**

- **tpi⁻ on malate and on succinate were PREDICTED CORRECTLY.** *"all strains
  except tpi⁻ on malate and succinate"* (p. 1057) — no growth was predicted
  there and none was observed. The old row scored two correct predictions as
  failures.
- **The paper's only diagnosis is structural and covers BOTH genes**, not the
  objective: *"Predicted growth rates were accurate in half the cases for both
  the ppc⁻ and tpi⁻ strains, suggesting that the reconstructed network may be
  incomplete."* There is no objective-function diagnosis in the paper to cite.

`readings.yaml` asks students to come with a guess about what the eleven failures
have in common. **They do not have one thing in common**, and the real shape is
the better lesson: the miss depends on the **substrate**, and an objective
function is the same on every substrate.

## 5 · Where Ibarra 2002 comes in

**Ibarra, R. U., Edwards, J. S. & Palsson, B. O., *Nature* 420, 186–189 (2002)** —
Fong's reference 4, held as an instructor companion, author list read off the
page. Title: *"Escherichia coli K-12 undergoes adaptive evolution to achieve in
silico predicted optimal growth."*

This is the paper that licenses session 20's thesis. Fong & Palsson shows the
agreement; Ibarra shows the **mechanism** of the agreement — a population
starting at a sub-optimal growth rate moving onto the line of optimality in the
phenotype phase plane. **Without it, "flux balance predicts where selection
goes" is our sentence. With it, it is a citation.**

## 6 · The teaching network — BUILT AND VERIFIED 26 October

`posb.fba.teaching_network()`. **9 reactions, 6 balanced metabolites**, two
external (acetate, CO₂), glucose uptake capped at 10 as the only numerical
constraint. Every real reaction balances carbon, and there is a test asserting
it, because the session's thesis is that **S** counts atoms exactly.

| reaction | stoichiometry | C |
|---|---|---|
| v_uptake | → G6P | source |
| v_pgi | G6P → F6P | 6 → 6 |
| v_zwf | G6P → P5P + CO₂ | 6 → 6 |
| v_tpi | F6P → 2 T3P | 6 → 6 |
| v_lower | T3P → PYR + ATP | 3 → 3 |
| v_ackA | PYR → Ace + CO₂ + ATP | 3 → 3 |
| v_tca | PYR → 3 CO₂ + 3 ATP | 3 → 3 |
| v_biomass | 2 T3P + P5P + 4 ATP → | sink |
| v_atpm | ATP → | sink |

### The board gets it in six lines, and the answers are integers

```
P5P   one producer, one consumer          ->  v_zwf   = b
G6P   10 = v_pgi + v_zwf                  ->  v_pgi   = 10 - b
F6P   one producer, one consumer          ->  v_tpi   = v_pgi      [COUPLED]
T3P   2 v_tpi = 2b + v_lower              ->  v_lower = 20 - 4b
ATP   all pyruvate to the TCA (3 vs 1):   4(20 - 4b) >= 4b
                                          ->  b <= 4
```

**Optimum: biomass = 4 exactly.** v_pgi = v_tpi = 6, v_zwf = 4,
v_lower = v_tca = 4, **v_ackA = 0**, v_atpm = 0. ATP: 4 + 12 = 16 = 4 × 4,
balanced. Confirmed by `linprog` to 10⁻⁹.

**The branch point goes all-or-nothing** — v_ackA is exactly 0 because the TCA
yields 3 ATP against acetate's 1. That is a vertex, and some optimum of a linear
program always sits at one.

**CORRECTED 31 October: the old last clause said "and it is why FBA never
predicts a graded split." That is false, and the deck already says so.** The
theorem promises that a corner is optimal; it does not promise the corner is
alone. When two arms tie, every blend of them is equally optimal, and "sixty
percent down this arm" is a perfectly good answer the solver will simply never
volunteer. Section 20's own segment 5 builds the counterexample — (4,0), (0,4),
(2,2) and every point between all give biomass 4, and none of the interior ones
is a corner. The segment-5 note retires the old wording explicitly and the answer sheet
4(c) states the correct version. **The wording was never on a surface**, so
the segment-5 note frames it as taking back the obvious generalization of
segment 3 rather than as a quotation of himself. **If
this file and the deck disagree, the deck is right.**

### Knockouts, all exact

| knockout | biomass | why |
|---|---|---|
| wild type | **4** | — |
| v_pgi, v_zwf, v_tpi, v_lower | **exactly 0** | no other route to T3P, to P5P or to ATP |
| **v_tca** | **10/3** | the optimum moves to a different vertex; acetate now carries all the pyruvate. Same six lines: 2(20 − 4b) ≥ 4b → b ≤ 10/3 |
| v_ackA, v_atpm | 4 | unused at the optimum, so free to lose |

The four lethal ones are the structural case — the shape of Fong & Palsson's
tpi⁻ strains, for which **no growth was computationally predicted at all** on
lactate, malate and succinate.

### Coupling

**There are TWO coupled pairs, not one.** `tests/test_fba.py` asserts the set
is exactly `{("v_pgi", "v_tpi"), ("v_zwf", "v_biomass")}` in a test named
`..._AND_NO_OTHERS`, written to stop exactly the drift this paragraph used to
invite — it named only the first, and the deck and answer sheet 4(e) both carry
both. Corrected 31 October.

- **v_pgi / v_tpi = 1.0000 exactly.** F6P has one producer and one consumer, so
  the network has already fixed this ratio and no regulation can change it.
- **v_zwf / v_biomass = 1.0000 exactly.** P5P has one producer and one
  consumer, and biomass takes one P5P per unit, so v_zwf = b. The handout
  derives this in §1.

That is the honest definition of flux coupling, and both are visible by
inspection, which is the right way to meet it first. **Pinned is not coupled**
— every flux is pinned when the optimum is unique, which is the bug the
AND_NO_OTHERS test exists to catch.

### Alternate optima — executable, not asserted

Adding `v_zwf2`, a route with stoichiometry identical to v_zwf, **leaves the
optimal biomass at 4** and makes the split between the two completely free:
flux variability reports both over **[0, 4]**. The solver returns one of them
and says nothing; no growth measurement can distinguish them.

This is **Mahadevan, R. & Schilling, C. H., *Metab Eng* 5, 264–276 (2003)**,
*"The effects of alternate optimal solutions in constraint-based genome-scale
metabolic models"* — Fong's reference 12, held, title and authors read off page
1. The slide cites it rather than asserting the limitation.

⚠ **v_zwf2 is a modeling device and the deck must say so.** *E. coli* has a
single glucose-6-phosphate dehydrogenase; there is no real duplicate of v_zwf.
An exactly degenerate pair is constructed because it makes the tie
hand-checkable. Real redundancy of this kind exists — parallel
electron-transport branches, duplicated transhydrogenases — and that is where
alternate optima come from in practice. Recorded in the function's docstring
too, so the caveat travels with the code.

### Library state

`posb.fba`: `FluxModel` (with external metabolites and a null-space dimension),
`solve_fba`, `knockout_growth`, `flux_ranges` (flux variability),
`coupled_pairs`, `has_alternate_optima`, `teaching_network`. **16 test
functions.** One of them asserts that `fba`'s **S** equals `posb.core.Model`'s
**S** for the same network — the session is sold as session 3's matrix re-asked,
and that test is the sentence made literally true.

---

## Figure 1a, extracted — 31 October 2026

Fig. 1a in the main PDF is **vector art**, so markers can be read as coordinates
rather than guessed from pixels. A blue marker is five subpaths with one
full-width slab; a pink marker is one subpath. Tick-based calibration (exact
axis ticks, not label centers): `x = 66.12 + 135.69·v` pt, `y = 499.76 −
108.92·v` pt. One marker is 0.019 wide × 0.022 tall in h⁻¹. Resolution ±0.002.

**Counts.** 50 blue markers and 47 pink (three coincident pairs), after
dropping the legend swatches. Fifty blue is a clean internal check against the
paper's fifty evolved strains.

**The legend is a trap.** The "Before" and "After" swatches sit inside the plot
area, low on the right, at predicted ≈0.78 / measured 0.135 and 0.066. They
read as data points at high predicted and low measured growth. **They are not
data.** Any count that includes them is wrong.

### Distinct predicted values: 12 before, 12–13 after, for 50 strains

| | Before (blue) | After (pink) |
|---|---|---|
| distinct predicted values | 12 incl. the zero group | 12–13 incl. the zero group |
| non-zero predicted range | 0.432 – 0.654 | 0.594 – 0.880 |
| markers | 50 | 47 |

Up to eight strains share one predicted value. **Fifty strains, twelve
predictions — so the FBA inputs are per carbon source, not per strain.** Any
account of this figure that assumes a per-strain prediction is wrong.

### The two input sets

The predicted axis moves between stages and the clouds are nearly disjoint in
x. An FBA prediction moves only if a bound moves, so there are **two uptake
input sets, one per stage**, each applied one-pair-per-carbon-source.

The evidence that this is the structure and not an artifact of extraction:

- **The per-gene ratios are preserved across stages.** Within glucose, pink
  `0.880 / 0.832 / 0.765` = `1 / 0.945 / 0.869`; blue `0.654 / 0.623 / 0.568` =
  `1 / 0.953 / 0.868`. Same three network variants, same gene effects, lower
  input.
- **The pink triplet reproduces the paper's own sentences.** `0.832 → 0.603`
  is 27.5% below predicted, against *"~28% slower"* for ppc⁻ on glucose;
  `0.765 → 0.521` is 31.8%, against *"~33%"* for tpi⁻. Both replicates of each
  genotype share one predicted value to within 0.004 h⁻¹.
- **The zero group holds exactly six markers in each color** — tpi⁻ on
  lactate, malate and succinate, in duplicate, matching the Fig. 1 caption.

**The paper does not document the second set.** Supplementary Methods:
*"Uptake rate measurements were conducted at the end of adaptive evolution."*
The *"measured throughout the course of exponential growth"* that follows is
sampling within one batch culture, not across evolution. The main text is
careful that growth rates were taken *"at the beginning and end"* and leaves
the uptake rates unqualified, pointing at the single-set Supplementary Table 1.
**Read literally, the methods deny making the measurement the figure requires.**
nature.com offers exactly the three SI files this repo holds; there is no
missing supplement.

Where the lower set came from is **unresolved**. Two candidates, which nothing
found separates: day-zero rates on the unevolved deletion strains (routine in
Fong 2003 and Fong 2005, both of which measure SUR/OUR at intervals and at day
0), or reused wild-type rates per carbon source. Evidence that would settle it
and could not be obtained: the Methods of Ibarra, Edwards & Palsson, *Nature*
**420**:186 (2002) — closed, no open copy; the full text of Fong, Nanchen,
Palsson & Sauer, *J Biol Chem* **281**:8024 (2006), which measured uptake for
unevolved as well as evolved mutants; and Fong's UCSD dissertation.

**Kind: extracted by us from their figure, not stated by them.** The deck says
it that way — an observation, not a verdict. If the Before bounds turn out to
be wild-type rather than strain-specific, the blue cloud is a weaker claim than
the release makes, and the segment-6 note says so.

### Above and below the line

| | markers | above y = x | at the origin | below |
|---|---|---|---|---|
| Before (blue) | 50 | 4 | 4 | 42 |
| After (pink) | 47 | 10 | 8 | 29 |

The four blue above: the tpi⁻/lactate pair at predicted 0, measured 0.259 and
0.298; and one strain pair at predicted 0.447, measured 0.490 and 0.508, which
is 2.0 and 2.8 marker heights above — **not grazing**.

**The deck says "forty-two of the fifty," excludes nothing, and does not
explain the six zero-prediction strains at this point in the hour** — they are
a qualitative miss rather than an over-prediction, and that distinction is the
answer to segment 7's question. Excluding them would give 42 of 44, which is
what *"almost without exception"* used to mean; it spends segment 7's question
to buy cleaner arithmetic. (31 October ruling: use fifty.)

Counting *visually distinct blobs* instead of markers — which is what a
rasterized image gives, since overlapping markers fuse — gives 18 blue blobs
holding 50 markers, 3 of them above the line. **This is where an earlier
"3 of 22 blue blobs" came from: the 3 is right at blob granularity, the 22 was
a miscount.** Three counting levels exist; say which one is meant.

**Caption artifact.** The Fig. 1a caption reads *"whose growth rate after
evolution was 410% different"* — a mangled `>10%`. A student reading closely
will trip on it.

### "Before" is first measurable growth, per culture — settled

**Not day 0, and not a common time point across strains.** Each blue marker is
that culture's first non-zero daily growth-rate estimate.

The sentence *"Deletion strain curves begin on the first day of measurable
growth"* is in the **main Fig. 1 caption (p. 1056)**, about Fig. 1b itself —
not in the SI Fig. 1 caption. And Fig. 1b's tpi⁻/lactate curve does **not** sit
at zero and then rise: it is **absent** before day 11 and begins at day 10.9,
µ = 0.243. SI Fig. 1 is the panel that plots the zeros. The two figures never
disagreed.

**The marker match is diagnostic.** SI Fig. 1, tpi/LAC panel, by centroid: the
navy replicate reads 0.0000 at every day 1–10 and **0.2562 on day 11**; the
magenta replicate grew immediately, **0.3045 on day 1**. Fig. 1a's two blue
markers at predicted 0 are **0.259 and 0.298**. They pair one-to-one, within
marker-centering error. The replicates differ *because* one started on day 11
and the other on day 1 — a day-0 reading would have put both at zero.

**Two arithmetic constraints independently rule out day 0.** *"Each evolved
deletion strain showed an increase in growth rate of at least 15%"* and *"the
average growth-rate increase was 87%"* across the 46 that grew — which include
tpi⁻ on lactate. A percentage increase from zero is undefined.

**Mechanism**, SI Methods: *"Growth rates of each evolution culture were
monitored during the course of evolution by estimating the growth rate based
upon the dilution rate and optical density (OD) of the culture at the time of
passage into fresh medium. Growth rates were then measured in batch cultures
for each evolved strain at the end of evolution."* A culture with no measurable
OD at passage yields no estimate, so the trajectory has no point there.

**The asymmetry is worth a line in class.** "Before" is a passage-based daily
estimate; "After" is a batch-culture measurement. Same axis, two kinds of
number — which is this session's thesis applied to the paper testing it.

Four strains showed no growth for several days and their blue point is the day
they first grew: **ppc⁻ and tpi⁻ on glucose, zwf⁻ on malate, tpi⁻ on lactate**
(p. 1057). The four markers at the origin are tpi⁻ on malate and succinate, in
duplicate, which never grew at all.

**Not wild type.** Fig. 1 caption (a) says the comparison is *"for deletion
strains"*; WT appears only in Fig. 1b as dashed lines, and the WT lactate
trajectory starts at day 0, µ = 0.402, with no blue marker near it at predicted
zero.

**One gap, for the record.** The SI Fig. 1 caption in the repo PDF is truncated
mid-sentence — it ends *"…conducted for each"* and the final line is absent
from the file itself, not from the extraction. It does not affect any of the
above, which rests on the main Fig. 1b caption and the marker match, but the
authors' own words about the plotted zeros are not in hand.
