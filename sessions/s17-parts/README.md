# Session 17 — Parts, context, and why composition is not composition

**Thursday 22 October 2026.** Part II, second session. **M2 (Specific Aims
and the model) is due tonight**, Canvas 9154515.

Scope settled by Adam on 18 October: five segments. CRISPRi/a and bridge RNAs
become one closing slide pointing at S18; enzymatic synthesis, syn1.0 and
syn3A move to S19. The published syllabus promised the first two today, so the
narrowing is announced out loud in the goals slide rather than left for
students to notice.

## The one thing to remember

**A part is manufactured, not found.**

The object has no edges — 5′-RACE pins a transcription start and nothing else,
and the strength lives in flanking DNA, the host and ribosome availability,
none of which is in the tube. Worse, joining two parts changes both of them:
the transcript's 5′UTR is encoded at the junction and sets RNA stability, so
attaching a promoter changes the mRNA lifetime you were about to call
"promoter strength". That is not context bending a model. It is **composition
failing to be composition** — every abstraction this course has used assumes
composing A and B leaves A and B alone.

So you impose edges. Insulate, standardise, fix the junction, and the
abstraction becomes true because you made it true.

## What happens

| | |
|---|---|
| **Retrieval** | Tuesday's 45/60. The cold-start rule. And: a gate's gain — what did we have to measure to get one, and does that number travel? |
| **Frame: what context means** | Cardinale & Arkin's three classes — compositional (physical, functional), host (parasitic, resource, growth), environmental (direct, host-mediated). Vocabulary before measurement. |
| **1 · There is no promoter** | Draw the boundary; three failures; then move a measured promoter and classify what could change. The debrief separates "makes the measurement harder" from "means the thing measured does not exist". |
| **2 · How badly, measured** | Kosuri's 12,653 promoter × RBS constructs. The ANOVA, the 13-fold tail, the 10× → 3× reciprocity, and Cambray 2018's 28%. T43. |
| **3 · Where prediction works** | Cambray's terminator model on his own data: r = 0.97 inside the class, 44 points off outside it. Predictability is a property of the definition. |
| **4 · Manufacture the part** | Insulation as a device, not a distance. Four moves across three layers. Then 64% → 93%. Then the rival strategy — screen — and what it costs. |
| **5 · Composing anyway** | Golden Gate overhangs: 120 usable junctions, even odds of a clash at five parts. T44. Then the compositor as a process over shared state. T42. |
| **Close** | The standard that was proposed in 2013 and did not take. Then CRISPRi/a and bridge RNAs as the escape, pointing at Tuesday. Hand out Mishra. |

## The results this session exists to produce

**Composition fails, with numbers.** Kosuri *et al.*, PNAS 110(34):14024–14029
(2013), 114 promoters × 111 RBSs = 12,653 constructs:

| | |
|---|---|
| ANOVA, protein | promoter **54%**, RBS **30%**, unexplained **16.7%** |
| ANOVA, RNA | promoter 92%, RBS 4%, unexplained 4% |
| within 2× of the multiplicative prediction | 80% of RNA, **64%** of protein |
| worst 5% of protein deviations | **13-fold** off, on average |
| reciprocity, measured | **10× translation efficiency ↔ ~3× RNA abundance** |

**And deeper.** Cambray, Guimaraes & Arkin, *Nat Biotechnol* (2018),
`nbt.4238`, 244,000 designed sequences, 242,269 measured: design properties and
their first-order interactions explain **28%** of protein variance; structure
around the start codon is 83% of what they do explain; and sequences built to
be the same part differ by **8% of total variance**, which "vastly exceeds the
experimental error".

Attributing variance to *which part* explains 84%. Asking *what about the
sequence* returns 28%. **Part identity predicts; part sequence does not.**

**Where prediction works, and why.** Recomputed from Cambray *et al.*, NAR
41(9):5139–5148 (2013), Suppl. Table 1 — 54 terminators, committed as
`figures/data/s17_cambray_terminators.csv`:

| class | n | r | median abs. residual |
|---|---|---|---|
| `terminator` | 31 | **0.974** | **2.6** TE points |
| extended (ET) | 6 | 0.895 | 8.3 |
| low folding frequency (LFFT) | 9 | 0.165 | 11.9 |
| **low efficiency (LET)** | 7 | **0.378** | **44.4** |

The paper names ET, LFFT and LET itself as the classes its model overestimates.
Near-exact inside the class its features were identified over, useless outside.

**What manufacturing buys.** Mutalik *et al.*, *Nat Methods* (2013),
`nmeth.2404`: transcription elements encoding a **common mRNA start** plus
bicistronic translation elements, spanning 1,000-fold, land arbitrary genes
**within twofold of a target window ~93%** of the time — against Kosuri's 64%
within twofold of prediction. **These are not the same measurement** and both
the figure and the speaker notes say so.

**Two attritions that differ in kind.** Chen *et al.* (2013): 582 terminators
measured → 39 strong, 6.7%, attrition on *strength*, a property of the part
alone. Stanton *et al.* (2014): 73 mined TetR-family repressors → 16
orthogonal (5- to 207-fold), 22%, attrition on *orthogonality*, a property of
the **set**, which no single-part measurement can reveal. Better single-part
models make the first cheaper and do nothing for the second.

**The open question to close on.** Mutalik *et al.*, `nmeth.2403`, proposed an
ANOVA framework and a part **quality** statistic in 2013 — a certification that
would tell a designer in advance whether a part will hold its number. It did
not take. Why not, and what would it have to offer a working lab? That is a
247 project.

## Coverage

| | |
|---|---|
| T42 | Compose parts in code (the compositor abstraction) — demonstrated here, **assessed on PS7** |
| T43 | Quantify context dependence of a part — demonstrated here, assessed on PS7 |
| T44 | Golden Gate overhang and primer design — demonstrated here, assessed on PS7 |

T42–T44 moved from PS6 to PS7 on 18 October: this session is taught two days
before PS6 is due and an item cannot be assessed the week it is first seen.
`docs/coverage-matrix.md` still routed them to PS6 until the evening PS6
shipped without them; corrected the same evening.

## Readings

| | |
|---|---|
| Required, read before today | Cambray *et al.*, NAR 2013 — intrinsic transcription terminators (handed out Tuesday) |
| Optional | Chen *et al.*, Nat Methods 2013 — 582 terminators; Stanton *et al.*, Nat Chem Biol 2014 — genomic mining |
| Handed out today, for Tuesday | Mishra *et al.* 2021 — protein phosphorylation toggle |
| Cited, not assigned | Cardinale & Arkin 2012; Kosuri *et al.* 2013; Mutalik *et al.* 2013 (`2403`, `2404`); Cambray *et al.* 2018; Davis *et al.* 2011; Qi *et al.* 2012; Lou *et al.* 2012; Qi & Arkin 2014 |

## Built

| | |
|---|---|
| Figures | 6 PNGs from `figures/s17_parts.py`, all verifying: `s17_terminator_model` (real SI data, per-class fit recomputed at render time), `s17_variance`, `s17_manufacture`, `s17_insulators`, `s17_overhangs` (counting exact, clash curve an explicit toy), `s17_compositor` |
| Data | `figures/data/s17_cambray_terminators.csv` — 54 rows from the NAR 2013 SI, redistributed under CC BY 4.0 with Adam's agreement as an author, 18 October. Regenerate with `tools/extract_cambray_terminators.py` |
| Deck | `decks/s17_parts.py` → 29 slides |
| Handout + answers | *not yet written* |
| Board notes | *not yet written* |

Every figure is gated against the slide's usable width (11.93 in) and body
height (5.6 in) at save time, because a figure that runs off the slide should
fail the build rather than be noticed.
