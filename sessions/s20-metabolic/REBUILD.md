# Session 20 — rebuild, settled 31 October 2026

**This file is the specification. It supersedes `DESIGN.md` §§2–7 and the
structure recorded in `NUMBERS.md`. If this file and the built deck disagree,
fix whichever is wrong and say which — but do not reopen the decisions below.**

Adam reviewed the built deck slide by slide on 31 October. Everything in
section 1 is his call, already made. Section 2 is the consequence. Section 3 is
the target structure. Nothing here is a proposal.

---

## 1 · The decisions, made and closed

1. **The hour needs a reason to exist that comes from outside the method.**
   Dynamics are hard; for most systems we do not have the kinetics or the real
   abundances; and for a great many questions the thing we actually want is
   steady-state growth and productivity. Constraint-based analysis buys an
   end-run around rate laws, paid for with mass balance, biomass composition
   and resource availability. **This goes on the opening frame.** "The algebra
   ran out" is not a motivation and will not be used as one.

2. **Draw the pathway.** Glycolysis and the pentose phosphate branch, as a
   picture, before any matrix. Prefer the paper's own drawing if it has one.

3. **The acetate/TCA branch gets its own surface.** Name it overflow
   metabolism, say why there is a decision there, and carry real data. The
   all-or-nothing result later lands on this branch and the room currently
   does not know it is a branch worth caring about.

4. **Every release must be answerable from surfaces already shown.** The
   column-writing release was not: `F6P` and `T3P` first appear in the question
   itself, `P5P` appears nine slides later, and the six balanced metabolites
   are never enumerated anywhere. Replace it with a drawn pathway and a
   step-through that asks the room to predict the next arrow, then ask for the
   column.

5. **Show the matrix and annotate it.** Arrows and callouts on the column they
   just wrote. The debrief currently describes the matrix in words on the
   surface before the figure appears. Show, do not only tell.

6. **Mass conservation does not constrain the space, and that has to be
   drawn.** A flux cone, two flux vectors that both satisfy S·v = 0, traded
   against each other with mass conserved in both. Step 5 of the null-space run
   asserts this today.

7. **Say what makes the solution unique, biologically.** Irreversibility;
   the biomass function as *measured composition*, which is where the previous
   session's material enters; enzyme capacity entering as flux bounds rather
   than as v_max and K_m; transport in and out; enzyme presence and absence,
   informed by expression where available; that this is a convex program; and
   that the medium has to be specified exactly. **The through-line: S is exact
   and says nothing, the objective is a hypothesis, and the bounds are where
   the biology lives.** That sentence is then collected at Fong, whose model
   was handed its own measured uptake rates, and again at the close.

8. **The six-line solution of the toy becomes a build surface.** It is the
   hour's central calculation and it currently exists only on the board and in
   the handout, which is why the flux map "appears with no explanation."
   `docs/lecture-design.md` §5b moved derivations off the board; this one never
   moved.

9. **A knockout is shown before it is asserted.** State what a deletion does,
   then show the network with and without the gene, then ask which are lethal.

10. **The paper is taught, not cited.** `fong2004_fig1a.png` is already cropped
    and has never been placed — it carries Before and After, which *is* the
    "evolved" argument, and the eleven failures are labelled on it by name.
    Fig. 1b's Lac, Mal and Suc panels carry the two correct no-growth calls and
    the one real structural miss. Segment 6 gets a release and a debrief; it
    currently has neither.

---

## 2 · The structural defect underneath all of it

**Not one of the seven segments has the four moves in the prescribed order,
and three release before they build.**

| segment | built order | |
|---|---|---|
| 1 · the object | frame → release → debrief → build | build last |
| 2 · null space | build only | no frame, release, debrief |
| 3 · the program | frame → build | no release, no debrief |
| 4 · knockouts | frame → release → build → debrief → debrief | build after release |
| 5 · alternates | frame → release → debrief → build | build last |
| 6 · Fong | frame → build → build | no release, no debrief |
| 7 · the eleven | release → debrief | no frame, no build |

`docs/lecture-design.md` §5e: four moves, in that order, none optional. Every
header carries the right word, so every mechanical check passed — **nothing in
the repo verifies the sequence.** That is the whole explanation for "how would
they do this in class?", and it is a build gate, not a prose rule.

**One exception, deliberate.** Segment 5 releases before it builds and that
stays: "two routes are identical, so trade them" is answerable from the frame
alone, which is the condition the rule exists to protect. The letter is broken
and the reason is satisfied. Do not reorder it.

---

## 3 · Target structure

Moves in order within each segment. New surfaces marked NEW; new figures named.

| # | move | surface |
|---|---|---|
| | **open** | title · retrieval · goals (goals rewritten to ask why this method) |
| 1 | frame | **NEW** — why constraint-based analysis exists: no kinetics, no abundances, steady-state is the question |
| 1 | frame | **NEW** — the pathway, drawn · `fig_pathway` |
| 1 | build | **NEW** — step through the pathway, predicting the next arrow · `fig_pathway` advancing |
| 1 | build | **NEW** — the branch: acetate against the TCA, and why it is called overflow |
| 1 | release | write one column — now answerable |
| 1 | debrief | **NEW** — the matrix, annotated: their column arrowed, entries called out · `fig_matrix_annotated` |
| 2 | build | the null-space run, five steps |
| 2 | build | **NEW** — the flux cone: two vectors, both S·v = 0 · `fig_cone` |
| 3 | frame | the bounds are where the biology lives (rewritten) |
| 3 | build | **NEW** — the six lines, on slides, flux map advancing |
| 3 | debrief | biomass 4, and the vertex is visible · `s20_flux_map` |
| 4 | frame | a knockout is a bound set to zero |
| 4 | build | **NEW** — cut the arrow, watch the flow die · `fig_cuts` |
| 4 | release | which deletions kill it? |
| 4 | debrief | four lethal, two free, one costly · `s20_flux_map` right panel |
| 5 | frame | a second route to the same place |
| 5 | release | find a second answer |
| 5 | debrief | the answer stops being an answer — **and the coupling that disappears, moved here from segment 4, where it had nothing to pay off** |
| 5 | build | the optimal face is an edge · `fig_cone` again, plus FVA ranges |
| 6 | frame | six deletions, fifty strains, and what was fed in |
| 6 | build | **Fig. 1a** — Before and After · `fong2004_fig1a` |
| 6 | build | evolved — 87% average increase, 46 of 50 grew |
| 6 | release | **NEW** — on Fig. 1a: which points are the failures, and what would you check? |
| 6 | debrief | the eleven, named on their own figure |
| 7 | build | **Fig. 1b**, tpi on Lac, Mal, Suc · `fong2004_fig1` |
| 7 | debrief | the authors' conclusion, and the methylglyoxal bypass they name |
| | close | where this goes · what to read |

**Paid for by:** folding "You have met this object before" into the annotated
matrix debrief; moving the coupling debrief out of segment 4 into segment 5;
and merging "Evolved" into the Fig. 1a surfaces once the figure carries the
result. Slide count is reported after the build, not budgeted before it.

---

## 4 · Verified against the paper, 31 October

Read from `private/readings/Session 20 - fong-palsson-2004-...pdf`, all three
pages. Everything the deck already says checks out. Three things it does not
say and should:

- **87%.** "For the 46 evolved strains that grew (all strains except tpi⁻ on
  malate and succinate), the average growth-rate increase was 87%" (p. 1057).
  Every evolved strain gained at least 15%.
- **46 of 50 grew.** The four that did not are the tpi⁻ strains on malate and
  succinate — in duplicate — which are the model's *correct* no-growth calls.
- **The methylglyoxal bypass.** *Corrected 31 October: this entry used to
  call the quote "the paper's own candidate for the missing chemistry." It
  is not. The sentence sits in the paragraph on RATE OF ADAPTATION, two
  columns after the "reconstructed network may be incomplete" sentence, and
  the paper never says iJR904 lacks the bypass or links the two. The deck
  now says it is their guess at why that strain adapted slowly.* The quote: "growth on glucose after deleting the gene tpi may result in a
  large change in metabolic flux distributions (possibly activation of the
  methylglyoxal bypass) and lead to a gradual increase in growth rate"
  (p. 1057). What is teachable is the SHAPE of it — a named route a
  biochemist can go and check — not a claim about what the reconstruction
  contains, which the authors do not make and this repo cannot verify.

Counts, for the record: 24 evolution cases (22 in duplicate, 2 in triplicate)
giving 50 strains; 39 of 50 within 10%; eight of the eleven misses are ppc⁻ or
tpi⁻; nine carbon sources used for the post-evolution characterisation.

---

## 5 · Voice

Notes are rewritten as Adam thinking about what he will say. No imperatives
aimed at the lecturer, no bare times, no "worth a beat", and no repo history —
`posb.fba.coupled_pairs returns exactly these two, and the test names the set`
and `An earlier version of this slide said` are both in the current deck and
both come out. Every question a surface asks has its answer written in the
note, arithmetic included.
