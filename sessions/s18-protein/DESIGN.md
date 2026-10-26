# Session 18 — Protein circuits: a parameter is manufactured, not found

**Tuesday 27 October 2026.** Part II, third session. Required reading already
handed out: Mishra *et al.*, *Science* 2021 (verified in `private/readings/`).

**Status: BUILT, 25 October.** §2 approved by Adam, 25 Oct. `decks/s18_protein.py`
is clean through `slide_fit` and the prior-year gate. 24 paper figures are
*declared* in the manifest and the deck *places* a subset of them; the build's
"all paper figures embedded" means every figure the deck references was found
on disk, which is not the same claim. Handout, answer sheet and board notes are
still to do, and the deck has not yet had its F4.5 adversarial review.

---

## 1 · The thesis, and where it comes from

Session 9 ended on a slide its own speaker notes call *"THE slide of the
lecture"*:

> **β, γ — HARD.** Cooperativity is set by the repressor's oligomerisation and
> the operator architecture. **You choose it by choosing a protein.**
>
> *The parameter that most determines bistability is the one you can least
> control. That asymmetry is the design problem.*

and the note under it:

> The math says cooperativity opens the wedge; the biology says it is what you
> can least tune. Gardner solved it by CHOOSING a repressor that already
> dimerises, not by tuning cooperativity — and then tuned alpha, the easy axis,
> with RBSs.

**Session 18 is the answer to that slide.** Zero-order ultrasensitivity
produces effective cooperativity — an apparent Hill coefficient of 26 at
k = 0.01, verified — out of a system with **no cooperative binding anywhere in
it**. And the knob that places the switch is the ratio of two enzymes' maximal
rates, which is an expression level: session 9's *easy* axis.

Session 17's thesis was *a part is manufactured, not found*. Session 18's is
the same sentence about a **parameter**. That is the line the session turns on,
and it makes Part II continuous with Part I instead of a change of subject.

### What this corrects in the S17 → S18 bridge

`sessions/s17-parts/DESIGN.md` §2 currently sets Tuesday up as *"So stop using
promoters."* The algebra says the opposite. The half-maximal stimulus is
exactly

    (V₁/V₂)₅₀ = (k₁ + ½) / (k₂ + ½)

a ratio of (k + ½), not of k — so as the Michaelis constants shrink, which is
what buys the sharpness, **the threshold walks to 1 and stops being tunable**.
At apparent Hill 32 it is confined within 3.3% of the point where the two
enzyme capacities are equal, whatever affinities are chosen. What places a
sharp switch is the ratio V₁/V₂, the expression ratio.

**So the protein layer buys sharpness the transcriptional layer cannot, and
the transcriptional layer still sets the threshold. You need both.** The bridge
line in S17's design doc should be amended; I will do it unless told otherwise.

---

## 2 · Scope — THE DECISION

Three documents specify this session and they do not agree.

| source | what S18 is | status |
|---|---|---|
| `decks/s02_substrate.py` speaker notes, ×4 | **Host context** — why the same DNA behaves differently in another chassis | **taught 1 Sep** |
| `docs/syllabus.md:396` | **Protein circuits** — scaffolds, recruitment, allosteric switches, phosphorylation toggles, ultrasensitivity with no promoter | **published to students** |
| `docs/coverage-matrix.md` | **T45** gate families on orthogonality/speed/load · **T46** CRISPRi repression model · **T47** recombinase state model | the assessment contract |

Session 2 is the one nobody has noticed. It posed, as an objectives-as-pretest
question to the room on 1 September:

> *"Why does the same circuit behave differently in a bacterium and in a human
> cell, before you change anything?"*

with the note *"Q3 is the one that pays off furthest away: **it is why session
18 exists** and why nothing from E. coli transfers for free"*, and again at its
close, *"the whole reason session 18 exists as a separate session rather than
an aside."*

**Recommendation: all three are satisfiable, because they are the same session
asked from three directions.** The organising question is

> **What does this medium make easy that was hard in the last one — and what
> does it cost?**

- Session 2 asked why a circuit does not transfer. The answer that matters
  here is on the **speed** axis: transcription is slow, and diffusion in a cell
  twenty times larger is two orders of magnitude slower (session 2's own L²
  argument). That is a reason to change medium, and it is where S2's promise
  gets paid.
- The syllabus gets protein circuits and ultrasensitivity-without-cooperativity,
  which is §1's thesis and the mathematical core.
- The matrix gets T45, T46, T47 — four media compared on three axes.

**The cost, stated:** scaffolds and recruitment (Bashor 2008, Dueber 2003/2007)
compress to one surface, for the second year running. `docs/coverage-2025.md`
§3 recommended keeping Bashor for the gain argument; this keeps it as a surface
and not a segment. The alternative — demote T46 (CRISPRi) to a stated result
and give scaffolds a segment — re-creates an assessed-but-not-demonstrated row,
since T46 is graded on PS7.

---

## 3 · Two promises this session is obliged to keep

**Session 4 promised zero-order ultrasensitivity to session 13, and session 13
did not deliver it.** From `decks/s04_modeling_ii.py:551`, in a ConcepTest
resolution note taught on 8 September:

> *"Zero-order ultrasensitivity in a phosphorylation cycle gives an apparent n
> above 20 from ONE site; so does titration by a decoy. **Both are session
> 13.**"*

`decks/s13_digital.py` contains zero occurrences of "ultrasensit", "zero-order"
and "phosphoryl". Session 13 was taught on 8 October. So a numerical claim was
made to the room, attributed to a future session, and that session did not
carry it.

The claim itself is **correct** — my derivation gives an apparent Hill
coefficient of **26.08** at k₁ = k₂ = 0.01 from a single modification site,
verified against the numerical root of the steady-state condition. So S18
discharges it, and the forward pointer in s04 should read session 18.

**The second mechanism in that note — titration by a decoy — is also taught
nowhere** ("decoy" and "titrat" appear once each, both in s04, both in this
same note). It is worth one surface here, because it is the same mechanism as
S19's resource competition and S21's retroactivity: a molecule sequestered by
something that is not its target. Three sessions, one mechanism, and naming it
here makes the ladder visible early.

---

## 4 · The object before the model

The vocabulary check from `posb-teaching-derivations` §1, run across every deck
s04 → s17:

| term | occurrences in decks s04–s17 |
|---|---|
| kinase | **0** |
| phosphatase | **0** |
| conserved (of a pool) | 1 (s07, unrelated) |
| ultrasensitiv- | 2 (one in s04's note above, one in s17) |
| zero-order | 1 (s04's note) |
| Michaelis | 8 — **all in s04**, nothing since |

So **the session may assume none of it.** A covalent modification cycle has to
be drawn before it is modelled, and Michaelis–Menten has to be re-established
after a seven-week gap.

The structural point to make while drawing it, because it is what makes the
mathematics come out differently: **this is the first system in the course
whose total is conserved.** Every circuit so far had a species made at some
rate and removed at another, and its steady state was a balance of production
against dilution. Here nothing is made and nothing is destroyed — the pool only
moves between two forms. That is the whole reason saturation can do what it
does, and a student who does not notice it will not see where the sharpness
comes from.

**Tee up the controls as a question** (`posb-teaching-derivations` §4), before
any algebra: *you have this cycle in your hands — what can you change, and what
would you have to do to change each one?* The split to fish for, which the
design ledger at the end is then checked against rather than handed down:

| knob | how you turn it |
|---|---|
| v₁, v₂ — the two maximal rates | **expression level.** Cloning, or an inducer. Session 9's easy axis. |
| K₁, K₂ — the two Michaelis constants | mutate the enzyme or swap a domain. Session 9's hard axis. |
| W_T — the size of the pool | express more substrate — and note this changes k₁ and k₂ *both*, since they are K/W_T |

The third row is the one worth the pause: the saturation parameters are not
properties of the enzymes alone. **Expressing more substrate makes both enzymes
MORE saturated at once and sharpens the switch**, because k = K_m/W_T.

> ⚠️ **This paragraph said the opposite until 25 October** — "desaturates …
> flattens" — and the error reached the knobs slide, the design ledger and the
> close before the F4.5 review caught it. Verified against `posb.protein` with
> the enzymes held fixed: W_T from 0.1 to 1000 takes the apparent Hill
> coefficient from 1.04 to 248.6. An enzyme is saturated when its substrate sits
> well above its K_m, so more substrate is more saturated.

Two consequences the plan missed, both now in the deck. **W_T cancels exactly
out of the crossing point** — w(V₁/V₂ = 1) = k₂/(k₁+k₂) = K_m2/(K_m1+K_m2) —
so the pool size sets the sharpness without moving where the curves cross;
verified to twelve figures across a thousandfold change in W_T. And **the pool
size is a promoter**, which makes it session 9's *easy* axis. That is the
session's title delivered rather than asserted. The price is the threshold,
which is segment 4's existing result. The hinge into session 19 is sharper for
it: the cheapest sharpness knob you own is the one Thursday takes away.

---

## 5 · Segments

| | segment | techniques |
|---|---|---|
| **F** | **Retrieval.** Two from Thursday (the compositor; part identity vs part sequence), one from session 9 — *the toggle criterion needs cooperativity on at least one arm. Where did Gardner get it?* The answer, *he chose a protein that already dimerises*, is the question this session answers. | — |
| **1** | **The object.** Draw the cycle. Conserved pool, two opposing enzymes, Michaelis–Menten re-established. Then the knobs, as a question to the room. | — |
| **2** | **The derivation.** Set the fluxes equal; normalise by the pool; cross-multiply to a quadratic. Then the two exact results, each on its own surface because each is a step where something disappears: at V₁/V₂ = 1 the quadratic term vanishes and w = k₂/(k₁+k₂); setting w = ½ gives (V₁/V₂)₅₀ = (k₁+½)/(k₂+½). | — |
| **3** | **What saturation buys.** The sensitivity index and why a hyperbola needs 81-fold. Then the unsaturated limit (hyperbolic, apparent n → 1) against the saturated one (n = 26 at k = 0.01). **This is where s04's promise is discharged, out loud.** | — |
| **4** | **What it costs, and the wrong turn.** (V₁/V₂)₅₀ looks like a tunable ratio and is not. The reachable-threshold table. Then the resolution: sharpness from the protein layer, threshold from the transcriptional layer. And: both enzymes must be saturated — k₁ = 0.005 with k₂ relaxed from 0.005 to 0.5 collapses apparent n from 51 to 3.2, so **the property belongs to the pair**, which is session 17's orthogonality lesson in a new place. | — |
| **5** | **Mishra 2021 — the toggle with no promoter in it.** The topology first (Fig. 3A), so the room sees Gardner's wiring before it sees twenty protein names; then the pathway, then the result, then the control. A **row-by-row correspondence** with session 9 rather than a claim that everything transfers: the nullclines, the Jacobian and the wedge do transfer, and **the equations do not have the same form** — what plays Gardner's −u degradation/dilution term is the OPPOSING ENZYME. Closes on the wrong turn: Mishra's bistability needs the feedback loop, not saturation alone, and their "ultrasensitivity" is a threshold claim, not a steepness claim. | — |
| **6** | **The other two media.** CRISPRi: specificity from base pairing rather than protein–DNA coevolution, with its repression model. Recombinase: the state model, and it is session 16's latch made physical and irreversible. One surface each for the mechanism, one for the model. | **T46, T47** |
| **7** | **The comparison.** Four media — transcription factor, protein phosphorylation, CRISPRi, recombinase — on orthogonality, speed and load. Every cell sourced and every number carrying its kind; cells with no measurement **say so**. Close on session 2's question 3, asked eight weeks ago. | **T45** |
| — | **Hand out Ceroni 2015** for Thursday. | — |

Scaffolds and recruitment (Bashor 2008) sit inside segment 6 or 7 as the
"gain is set by recruitment" surface, not as a segment of their own.

---

## 6 · The mathematics, verified in this session

`posb/protein.py`, written and tested — 128 tests pass, including the closed
forms checked against bracketing the steady-state condition itself and against
integrating the two-enzyme system with `posb.core`.

| result | value | kind |
|---|---|---|
| closed form vs numerical root, over a 5×5×3 grid | agree to 1 × 10⁻¹⁰ | computed |
| unsaturated limit, k = 1000 | apparent n = 1.0004 | computed |
| apparent n at k = 1 | 1.33 | computed |
| apparent n at k = 0.1 | 3.74 | computed |
| **apparent n at k = 0.01** | **26.08** | computed |
| apparent n at k = 0.001 | 248.6 | computed |
| scaling | n ≈ k^−0.92 over k ∈ [0.001, 0.1] | computed |
| w at V₁/V₂ = 1 | k₂/(k₁+k₂) exactly, worst error 3.4 × 10⁻¹⁴ | exact |
| (V₁/V₂)₅₀ | (k₁+½)/(k₂+½) exactly, worst rel. error 9.7 × 10⁻⁹ | exact |
| threshold range at apparent n = 32 | (V₁/V₂)₅₀ ∈ [0.968, 1.033] | computed |
| one enzyme saturated only (k₁ = 0.005, k₂ = 0.5) | apparent n = 3.15 vs 50.8 for both | computed |

Every one of these is a property of the equations. **The measured Hill
coefficients reported for real engineered switches are a different kind of
number and belong beside these with their own citations**, which is why
`posb.protein` computes the first and hard-codes none of the second.

---

## 7 · What is still needed

- ~~**Decision on §2.**~~ Approved 25 October; the deck is built to it.
- ~~**PDFs**~~ — all four are in `private/readings/` and all four have been
  read rather than recalled. Three findings came out of doing so:
  - **Bashor Fig. 4 was corrected.** The PDF's first line says *"CORRECTED
    22 AUGUST 2008; SEE LAST 2 PAGES"*; pages 7–8 reissue the circuit
    diagrams of panels B and D. The article page carries the superseded
    ones. Corrected crops are declared separately.
  - **Goldbeter & Koshland Fig. 2's n_H axis stops at 12**, which is where
    their ">13" comes from while their own Eq. 10 gives 26.08.
  - **Eq. 7 spans both columns of the printed page**, which is why a column
    crop of it both cut the equation and rendered it unreadably small.
- **T45's table has cells with no measurement in the literature.** Load for
  CRISPRi and for phosphorylation gates, in particular. The table will say so
  rather than estimate, and the empty cells are a 247 discussion.
- ~~**Figures**~~ — six built in `figures/s18_protein.py`, `--verify` clean.
- ~~**Paper figures**~~ — 24 declared in `decks/paper_figures.yaml`, every one
  cropped and looked at. Convention settled while cutting them: **crop the
  plot only and let the deck carry the attribution**, because a journal
  caption set at 7–8 pt is unreadable projected. An equation crop is the
  exception, since there the text is the content.
- **Still to build:** handout, answer sheet, board notes; PS7 under the
  approved rebalance.
- **Still to do:** the F4.5 adversarial review of the deck, then F4.6 on the
  corrections.
- **Ceroni 2015 must be handed out at the close**, so the PDF is needed before
  Tuesday.
