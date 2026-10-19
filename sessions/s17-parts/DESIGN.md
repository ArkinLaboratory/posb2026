# Session 17 — Parts, context, implementation media, DNA assembly

**SETTLED 18 October.** Thursday 22 October. **M2 (Specific Aims and the
model) is due the same day**, Canvas 9154515 — published, and in the Week 9
module.

**Adam's decision on §3: narrow to five segments.** CRISPRi/a and bridge RNAs
become one closing slide pointing at S18; enzymatic synthesis, syn1.0 and
syn3A move to S19. The compositor (segment 5, T42) **stays**. The syllabus
cost is accepted: students meet CRISPRi/a and bridge RNAs on Thursday and
model them in S18, where `docs/coverage-matrix.md` already put T46.

---

## 1 · What the session is for — Adam's framing, 18 October

Session 16 ends on a number: 45 of 60 Cello circuits worked, 34 integrases
screened gave 11 orthogonal, and in both cases **the architecture was fine and
the parts set was the limit.** The obvious follow-up is "so what is a part?"

**Adam's answer, and the session's thesis: there isn't one.** Not physically,
not functionally. Take a promoter:

1. **No crisp physical boundary.** There is no defensible place to cut. 5'-RACE
   pins the transcription start site and that is the only edge we get
   operationally. Strength depends on the flanking DNA, on the host, on
   ribosome availability. **The promoter is not contained in the sequence you
   ordered**, and the model for how its dynamics shift with context is not
   known.
2. **Composition is reciprocal.** Joining a promoter to a downstream element
   changes *that element's* intrinsic properties and its own: the transcript's
   5'UTR, which the junction partly encodes, sets RNA stability. Parts change
   each other's "intrinsic" numbers.
3. **There is no agreed model or measurement set** that would settle either.

Point 2 is the one that does structural damage. Every abstraction this course
has used — mass action, QSSA, transfer curves, truth tables, the compositor —
assumes composition **leaves the operands alone and combines their behaviors**.
If attaching A to B changes A's and B's parameters, that is not context
dependence bending a model. **It is composition failing to be composition.**

So the session is not "parts are noisy." It is: *the object our whole design
layer is written in terms of does not exist as a separable thing, here is the
measurement showing it, and here is what engineers do about it.*

**The constructive close, and it must be said or the session is nihilism.**
Cello still got 45 of 60. It got there by **manufacturing** parts — insulated
gates, one characterization context, fixed junctions — not by discovering them.
**A part is manufactured, not found.** Segment 3 is the catalogue of
manufacturing moves and what each one costs. Adam, 18 October: the lesson is a
manufacturing lesson.

## 2 · The three-session arc this sits in

| | claim | evidence |
|---|---|---|
| **S16** | The orthogonal parts set is the bottleneck, not the design method | Cello 45/60; 34 integrases -> 11 orthogonal |
| **S17** | **A part is not a separable object** — no boundary, not contained in its sequence, and composition changes its operands. So a part is *manufactured*, not discovered | Cardinale & Arkin's context taxonomy; Kosuri's 12,653 promoter×RBS constructs (RBS takes 30% of protein variance, 10×→3× reciprocity); Cambray's terminators as the control; Stanton's attrition as the price of screening |
| **S18** | So stop using promoters. Protein circuits get ultrasensitivity with no transcription at all, on a timescale of seconds | Mishra's phospho-toggle — the S8/S9 toggle with no promoter in it |

The bridge is explicit: **S17 names the escape routes from the orthogonality
limit, and S18 takes one of them.** One escape is programmable specificity
(CRISPRi/a, bridge RNAs — specificity set by a guide sequence rather than by
protein–DNA coevolution). The other is changing physical layer entirely, which
is S18.

## 3 · Scope — settled 18 October

The syllabus line for S17 names **nine** things: parts, compositors, context
dependence, CRISPRi/a, bridge RNAs, Golden Gate/MoClo, Gibson, enzymatic
synthesis, syn1.0 and syn3A. That is three sessions of material.

**Settled — five segments, and the syllabus's promise kept with one
forward-pointing slide rather than a block:**

| | segment | rows | source |
|---|---|---|---|
| **F** | **Frame: what "context" even means.** Cardinale & Arkin's three classes, as vocabulary before any measurement lands. **Compositional** (physical — unintended interactions between parts on the same DNA, RNA or polypeptide; functional — competition for a shared output, i.e. retroactivity and fan-out), **host** (parasitic interaction, resource loading, growth coupling), **environmental** (direct, and host-mediated). Adam: this paper is what lets students *understand* context rather than just meet it. | — | Cardinale & Arkin 2012 |
| 1 | **There is no promoter.** The three failures of the object: no boundary, no containment, reciprocity. The 5'-RACE point is the honest one — it gives us one edge and nothing else. | — | §1 above |
| 2 | **Measuring the failure.** Kosuri's 114 promoters × 111 RBSs = 12,653 constructs. RELEASE item: hand them a promoter–RBS pair, ask for the predicted protein level, then show the distribution. | T43 | Kosuri 2013 |
| 3 | **Manufacture the part.** Insulation as a device, not a distance — Cardinale notes spacers of **100–1000 bp failed** to insulate tandem RNA attenuators where ribozymes worked. Three published moves, three layers: **DNA** (Davis/Sauer insulated promoters), **RNA processing** (Qi–Doudna–Arkin Csy4 — cleave the transcript at a fixed site so the 5'UTR is identical whatever promoter sits upstream, which is **point 2 engineered away**), **ribozyme** (Lou/Voigt RiboJ). Then the payoff, measured: **64% within twofold unstandardized (Kosuri) against ~93% within twofold manufactured (Mutalik BCD)**. | T43 | Davis 2011; Qi 2012; Lou 2012; Mutalik `2404` |
| 4 | **When prediction does work, and why.** Cambray's terminator model, on his own SI data: **r = 0.97 on the 31 terminators the model's class is defined over, and r = 0.38 with a median miss of 44 TE points on the seven low-efficiency ones.** Predictability is not a property of the part type — it is a property of the part type *as the definition draws it*. Then Stanton's attrition as the price when you cannot draw it, against **Kosuri's own conclusion** that you should screen rather than predict or standardize. | — | Cambray 2013 SI; Stanton 2014; Kosuri 2013 |
| 5 | **Composing anyway.** Golden Gate / MoClo overhang design — the physical layer carrying combinatorial constraints the functional design never sees — and the compositor in code: a part as a process with state-variable inputs. Close by naming where the compositor's parameters came from, and that segment 2 showed they do not transfer. | T44, T42 | L08 pp. 35–61; L09 pp. 20–41; L10 pp. 45–51 |
| — | **Closing slide, not a segment.** ncRNA devices: specificity set by Watson–Crick pairing, so the sequence → function map becomes computable instead of screened. That is the escape from the orthogonality limit, and S18 takes it. | — | Qi & Arkin 2014 |

### The numbers segment 2 is built on — verified 18 Oct from the paper

Kosuri, Goodman, Cambray, Mutalik, Gao, Arkin, Endy, Church, *PNAS* 2013,
**110(34):14024–14029**. 114 promoters × 111 RBSs, **12,653 constructs** (the
abstract's 12,563 is a typo in the paper).

| | result |
|---|---|
| ANOVA, protein | promoter **54%**, RBS **30%**, unexplained **16.7%** |
| ANOVA, RNA | promoter **92%**, RBS **4%**, unexplained **4%** |
| naive compositional model | **80%** of RNA within 2×, only **64%** of protein |
| | R² = **0.92** RNA, **0.76** protein |
| worst 5% of protein deviations | **13-fold** off, on average |
| **reciprocity, measured** | **10× translation efficiency ↔ ~3× RNA abundance**; 87× translation gives only ~4.3× mRNA, so it saturates |
| dynamic range | protein ~4 orders of magnitude, RNA ~3; CV **0.63** within a single promoter |

The RBS row is the teaching point: a *translational* element takes **30%** of
the variance in a quantity the designer attributes to the promoter. That is
Adam's point 2 with a number on it, and the 10× ↔ 3× line is the mechanism.

### The other numbers, verified 18 Oct from the PDFs Adam added

**Cambray, Guimaraes & Arkin, *Nat Biotechnol* 2018, `nbt.4238` — 244,000
designed sequences.** This is the deepest version of Adam's point 1 and it is
the number the session should turn on:

| | result |
|---|---|
| scale | 244,000 designed sequences, 56 replicates of a full factorial; **242,269** strains measured for protein production |
| what dominates | secondary structure around the start codon (STR−30:+30) — **83% of design properties' total effect** |
| **what is explained** | design properties *and their first-order interactions* explain **only 28%** of protein-production variance — *"suggesting that there are important factors that are not accounted for"* |
| **design error** | three sequences built to be equivalent within a series differ by **8% of total variance**, which *"vastly exceeds the experimental error"* |

Put beside Kosuri: attributing variance to **which promoter** and **which RBS**
explains 83% of protein variance; asking **what about the sequence** causes it
returns 28%. Part *identity* predicts. Part *sequence* does not. That is "the
promoter is not contained in the DNA you ordered," measured twice, five years
apart, by overlapping author lists.

The 8% design-error line is the single cleanest slide in the session: sequences
designed to be the same part are not the same part, by more than the
instrument's error.

**Cambray 2013 terminators — recomputed from Suppl. Table 1 of the SI**, 54
terminators with both a measured and a predicted TE:

| class | n | r | median abs. residual |
|---|---|---|---|
| `terminator` | 31 | **0.974** | **2.6** TE points |
| extended (ET) | 6 | 0.895 | 8.3 |
| low folding frequency (LFFT) | 9 | 0.165 | 11.9 |
| **low efficiency (LET, TE < 35%)** | 7 | **0.378** | **44.4** |
| all | 54 | 0.620 | 3.8 (RMSE 22.3) |

**This kills the "terminators are the control" reading I proposed, and what
replaces it is better.** The model is near-perfect on the class it is defined
over and off by 44 points on a 0–100 scale outside it — and the paper says so
itself, naming LET, LFFT and ET as the classes it overestimates. So the lesson
is not "some part types are predictable." It is: **impose a tight enough
definition and prediction works; the definition is the engineering.** Which is
Adam's point 1 turned into a design move.

**Mutalik *et al.*, `nmeth.2403`** — Mutalik, Guimaraes, Cambray, Mai,
Christoffersen, Martin, Yu, Lam, Rodriguez, Bennett, Keasling, Endy, Arkin,
*Nat Methods* 2013. An **ANOVA framework** for part performance, and a proposed
statistic — **part "quality"** — for tracking variation across changing
contexts, plus a method to estimate ensemble-wide activity from one or two
measurements. *(Numbers still to extract from the results.)*

**Insulator citations, resolved from `nmeth.2403`'s own reference list** — no
longer a guess, and it is two papers, not one:

- Davis, Rubin & Sauer, *Nucleic Acids Res* **39**, 1131–1141 (2011) — insulated promoters, DNA level.
- **Qi, Haurwitz, Shao, Doudna & Arkin, *Nat Biotechnol* 30, 1002–1006 (2012)** — RNA processing. *Adam's own*; Csy4 is an endoribonuclease, not a ribozyme.
- **Lou, Stanton, Chen, Munsky & Voigt, *Nat Biotechnol* 30, 1137–1142 (2012)** — RiboJ. *The ribozyme*, but Voigt's.

Same journal, same volume, months apart. The slide should carry both and say
they are two answers to one problem.

### The manufacturing number — `nmeth.2404`, arrived 18 Oct

Mutalik, Guimaraes, Cambray, Lam, Christoffersen, Mai, Tran, Paull, Keasling,
Arkin & Endy, *Nat Methods* 2013.

| | result |
|---|---|
| the architecture | **transcription elements encode a common mRNA start**; translation elements use an overlapping motif — the bicistronic design |
| dynamic range | elements selected to span a **1,000-fold** observed range |
| **the payoff** | arbitrary genes expressed **within twofold of target windows with ~93% reliability** |

**"Transcription elements encode a common mRNA start" is point 2 engineered
away at the design layer.** If every promoter emits the same transcript 5' end,
the promoter can no longer reach downstream and change the transcript's
stability through the 5'UTR it would otherwise encode. Csy4 does the same thing
post-transcriptionally, by cutting. Same disease, two cures.

**The slide segment 3 is built on — and the caveat it must carry:**

> Unstandardized elements, Kosuri 2013: **64%** of protein within twofold.
> Manufactured elements, Mutalik 2013: **~93%** within twofold.

Both are "within twofold" and both come from this group in the same year, which
is what makes the comparison worth putting up. **They are not the same
measurement** and the slide must say so: Kosuri's 64% is *prediction accuracy*
for a compositional model over 12,653 combinations; Mutalik's 93% is *hitting a
target expression window* with curated elements. The honest claim is "the same
tolerance, met far more often, once the parts are manufactured rather than
collected" — not "the error fell from 36% to 7%." Written here so the
adversarial pass has it in advance.

Nothing from S17's reading set is now missing.

### Chen and Stanton — verified 18 Oct, and two different attritions

**Chen, Liu, Nielsen, Brophy, Clancy, Peterson & Voigt, *Nat Methods* 2013.**
227 annotated *E. coli* terminators (90 also tested reversed) + 265 synthetic =
**582 measured**. **39 strong** ones, >50-fold reduction downstream, with enough
sequence diversity to avoid homologous recombination when used together. Plus a
biophysical model — the hairpin displacing the U-tract from the DNA.

**An earlier draft of this design had Chen as "the catalogue" against Cambray
as "the model". That is wrong: Chen built a model too.** What the two papers
actually are is *two groups publishing competing sequence → function terminator
models in the same year from different data* — which is itself point 3, not a
catalogue-versus-model contrast. Say that.

**Stanton, Nielsen, Tamsir, Clancy, Peterson & Voigt, *Nat Chem Biol* 2014.**
**73 TetR-family repressors** mined from prokaryotic genomes → **16** that both
repress their cognate promoter (**5- to 207-fold**) and barely touch the others.
As 16 NOT/NOR gates that is **>10⁵⁴ circuits**.

**The attrition series across the week, and why the two kinds differ:**

| | in | out | yield |
|---|---|---|---|
| S16 · Cello circuits | 60 | 45 worked | 75% |
| S16 · integrases | 34 | 11 orthogonal | 32% |
| S17 · Chen terminators | 582 | 39 strong | **6.7%** |
| S17 · Stanton repressors | 73 | 16 orthogonal | 22% |

Chen's attrition is on **strength** — a property of the part alone, measurable
once, in one context. Stanton's is on **orthogonality** — a property of the
part *set*, pairwise, which no measurement of a single part can reveal. You
cannot screen for it part by part; you screen n² interactions, and the cost
does not fall when single-part models improve.

That distinction is the sharpest available statement of "a part is not a
separable object": orthogonality is a part's value *given everything else in
the cell*, and it is the property Cello ran out of first.

### Where point 3 lands

"No agreed model or measurement set" is not the same claim as "the field is
stuck." Manufacturing demonstrably works — Cello is the existence proof. What
is missing is the **certification**: a measurement standard that would let a
designer know in advance that a given part, in a given manufactured context,
will hold its number.

And a standard was **proposed** — `nmeth.2403`'s activity-and-quality ANOVA,
from this same group in the same year as the BCD paper and the Kosuri library.
So the closing line is not "nobody has tried." It is: *here is the measurement
that would settle it, published thirteen years ago, and the field did not adopt
it.* That is a better question to leave a room with than a complaint, and it is
exactly the shape of a 247 project.

**Moved out, agreed by Adam 18 October, though the syllabus promised it on
Thursday:**

- **CRISPRi/a as taught content -> S18.** `docs/coverage-matrix.md` already puts
  **T46 (CRISPRi repression model) in S18**, so the matrix and the syllabus
  currently disagree and the matrix is the one with the assessment attached.
  Resolving in favour of the matrix costs nothing and removes a whole segment.
- **Enzymatic synthesis, syn1.0, syn3A -> S19 or a closing note.** Genome-scale
  construction sits naturally beside resource sharing and burden (S19), where
  the minimal genome is the obvious example.

**The cost, accepted:** the published syllabus says Thursday covers CRISPRi/a
and bridge RNAs. Narrowing it is a visible change. The forward-pointing slide
keeps the promise honestly — they will have *met* the idea — and S18 does the
model. The alternative considered and rejected was holding the syllabus exactly
and dropping segment 5; that would have deferred T42, a stated Thursday
learning objective, to a session after the set that assesses it was written.

**Say the narrowing out loud in the room**, in one line, rather than letting
students notice the syllabus and the lecture disagree.

## 4 · What is genuinely new work

- **Porting the compositor.** L09/L10's `BioSystem()` / `Compositor()` code is
  2010 MATLAB. A compositor is a `Reaction` with named state-variable inputs, so
  `posb.core` already supports it — this is a worked example to write, not new
  package surface. **No new `posb` module is needed for S17**, because T42–T44
  moved to PS7 (settled 18 Oct; `docs/coverage-matrix.md` corrected the same
  evening, having still routed them to the PS6 that shipped without them) and
  nothing is autograded off this session this week.
- **Figures**: terminator strength against the model's predictor (from Cambray's
  own data if the SI is reachable, otherwise schematic and labelled as such);
  a context-dependence panel; an overhang-design combinatorics panel; the
  compositor as a box with state-variable arrows.
- **Readings**: Cambray handed out Tuesday (see §5 of the week brief), Mishra
  handed out Thursday for S18.

## 5 · M2 is due Thursday

Canvas 9154515, created unpublished 26 September, **published state unchecked**.
Verify with the module-state preflight before Tuesday, not by eye. Worth ninety
seconds of Thursday's class to say what "answers what it asks" means, since M1's
comments are what M2 builds on.
