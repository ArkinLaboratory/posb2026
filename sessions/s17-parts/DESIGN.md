# Session 17 — Parts, context, implementation media, DNA assembly

**Design question, for Adam, 18 October.** Thursday 22 October. Nothing built.
**M2 (Specific Aims and the model) is due the same day**, Canvas 9154515.

---

## 1 · What the session is for, in one line

Session 16 ends on a number: 45 of 60 Cello circuits worked, 34 integrases
screened gave 11 orthogonal, and in both cases **the architecture was fine and
the parts set was the limit.** Session 17 is the answer to the question that
leaves hanging:

> **What is a part, where does one come from, and why does its number change
> when you move it?**

That framing makes S17 the hinge of Part II rather than a miscellany, and it is
already what the readings were chosen for.

## 2 · The three-session arc this sits in

| | claim | evidence |
|---|---|---|
| **S16** | The orthogonal parts set is the bottleneck, not the design method | Cello 45/60; 34 integrases -> 11 orthogonal |
| **S17** | A part is a *measurement*, not a name — and the measurement moves with context. New parts come from mining, and mining has brutal attrition | Cambray's terminator model; Chen's 582-terminator catalogue; Stanton's mined repressors; Cello's insulated gates |
| **S18** | So stop using promoters. Protein circuits get ultrasensitivity with no transcription at all, on a timescale of seconds | Mishra's phospho-toggle — the S8/S9 toggle with no promoter in it |

The bridge is explicit: **S17 names the escape routes from the orthogonality
limit, and S18 takes one of them.** One escape is programmable specificity
(CRISPRi/a, bridge RNAs — specificity set by a guide sequence rather than by
protein–DNA coevolution). The other is changing physical layer entirely, which
is S18.

## 3 · The scope problem, and the decision Adam owes

The syllabus line for S17 names **nine** things: parts, compositors, context
dependence, CRISPRi/a, bridge RNAs, Golden Gate/MoClo, Gibson, enzymatic
synthesis, syn1.0 and syn3A. That is three sessions of material.

**Recommendation — cut to five segments, and keep the syllabus's promise with
one forward-pointing slide rather than a block:**

| | segment | rows | source |
|---|---|---|---|
| 1 | **A part is a measurement.** Cambray's biophysical model of intrinsic terminators: which sequence features set strength, and which of them a designer can change. Against Chen's 582-terminator catalogue — *the catalogue and the model are different things and a designer needs both* (Adam, 26 Sep). | — | Cambray 2013; Chen 2013 |
| 2 | **The measurement moves.** Context dependence, quantified — T43. Why Cello needed *insulated* gates, and what insulation buys in the units of S13's transfer curves. | T43 | L16 pp. 25–29; L09 pp. 7–19 |
| 3 | **Where parts come from.** Stanton's genomic mining: how many candidates in, how many orthogonal gates out. Third instance of the same attrition in two sessions. | — | Stanton 2014 |
| 4 | **Putting them together physically.** Golden Gate/MoClo overhang design, Gibson, and why overhang choice is a combinatorial problem with a real failure mode. | T44 | L08 pp. 35–61 |
| 5 | **Compose in code.** The compositor abstraction — a part is a *process* with state-variable inputs — ported from 2010 MATLAB to `posb.Model`/`Reaction`. | T42 | L09 pp. 20–41; L10 pp. 45–51 |
| — | **Closing slide, not a segment.** CRISPRi/a and bridge RNAs: specificity by guide sequence, which is the escape from the orthogonality limit. One slide, pointing at S18. | — | — |

**Moved out, and this needs Adam's agreement because the syllabus promised it
on Thursday:**

- **CRISPRi/a as taught content -> S18.** `docs/coverage-matrix.md` already puts
  **T46 (CRISPRi repression model) in S18**, so the matrix and the syllabus
  currently disagree and the matrix is the one with the assessment attached.
  Resolving in favour of the matrix costs nothing and removes a whole segment.
- **Enzymatic synthesis, syn1.0, syn3A -> S19 or a closing note.** Genome-scale
  construction sits naturally beside resource sharing and burden (S19), where
  the minimal genome is the obvious example.

**The cost of doing this:** the published syllabus says Thursday covers CRISPRi/a
and bridge RNAs. Narrowing it is a visible change. The forward-pointing slide
keeps the promise honestly (they will have *met* the idea) and S18 does the
model. If Adam would rather hold the syllabus exactly, something else has to go,
and my next choice would be segment 5 — T42 is on PS7 now, not PS6, so the
compositor can be demonstrated in S18 or carried entirely by the PS7 worked
example.

## 4 · What is genuinely new work

- **Porting the compositor.** L09/L10's `BioSystem()` / `Compositor()` code is
  2010 MATLAB. A compositor is a `Reaction` with named state-variable inputs, so
  `posb.core` already supports it — this is a worked example to write, not new
  package surface. **No new `posb` module is needed for S17**, because T42–T44
  moved to PS7 and nothing is autograded off this session this week.
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
