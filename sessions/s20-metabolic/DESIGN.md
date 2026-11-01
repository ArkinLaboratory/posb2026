# Session 20 — Metabolic engineering: the coupling you can write down exactly, and still cannot predict


> **SUPERSEDED IN PART, 26 October 2026.** The two-cause story below — one failure a missing route, the other a wrong objective — is NOT what Fong & Palsson conclude. Their only diagnosis covers BOTH genes and is network incompleteness (p. 1057). Eleven is 8 + 3: eight are ppc or tpi, three are single replicates the authors decline to diagnose. The model was also RIGHT about tpi on malate and succinate. The deck's segment 7 carries the corrected version; prefer it.
**Tuesday 3 November 2026.** Part II, fifth session. Required reading: Fong &
Palsson, *Nat Genet* 36(10) 1056–1058 (2004) — **held**, assigned at the close
of session 19. At the close of this session, Mishra 2014 is assigned for S21.

**Status: SUPERSEDED IN PART. The Fong & Palsson numbers are verified off the
PDF (§3).** The line that used to stand here — that the worked network and the
`posb.fba` results were "specified but NOT yet derived or tested" — was true
when written and is **not true now**: `posb/fba.py` and `tests/test_fba.py` both
exist, the network was built and verified on 26 October (`NUMBERS.md` §6, 16
test functions), and the deck calls into it live. §7 below is pre-build text
that was never retired; read it as history.

---

## 1 · Where this sits in the arc, and why that decides the session

`docs/course-map.md` frames sessions 19–25 as one ladder of contexts that break
a circuit. Sessions 19–22 are its first four rungs, and the thing that
distinguishes them is **how visible the coupling is** — which is also what
decides the engineering move each session can teach:

| rung | session | the coupling | how visible | the move it permits |
|---|---|---|---|---|
| 1 | 19 | competition for shared machinery | **invisible** — two genes, no wire, 66.7% drop | measure it; budget against it |
| 2 | **20** | stoichiometric coupling through shared metabolites | **completely specified** — **S** writes every one of them down exactly | compute it — and discover that is not enough |
| 3 | 21 | sequestration at an interface | **mis-drawn** — the arrow says *signal*, the molecule says *binding site* | derive it, then **insulate** it |
| 4 | 22 | all of the above, as disturbances | — | **reject** them structurally |

Session 19 ended on a shared pool nobody can divide and a hidden edge nobody
can see. **Session 20 is the opposite case: a coupling so completely known that
you can write every stoichiometric coefficient down, and prediction is still
hard.** That is the session's whole reason to exist in this position, and it is
not a session about a technique.

**Do not frame this as a fourth rung of the sequestration ladder.** Session 19's
close surface explicitly separates it — *"session 20 is not a fourth rung of
the sequestration ladder — it is the host's economy again at the level of
metabolites"* — and the deck must honour that, because the room was told so four
days earlier.

## 2 · The thesis

**The stoichiometric matrix is the only part of the cell you can write down
exactly. The price of that exactness is that it says nothing about rates.**

So the constraints are free and the prediction is not: to get a number out you
must **import an objective**, and the objective is a hypothesis about what
selection has done, not a property of the network. Fong & Palsson is what
happens when somebody tests the hypothesis.

This is session 17's sentence — *a parameter is manufactured, not found* —
arriving at network scale, and it is the setup for S22, where the thing you
import is a controller rather than an assumption.

## 3 · Fong & Palsson, verified off the PDF 26 October

Record the **kind** of every number, not just its value. The kinds are the
argument here.

| claim | kind | where |
|---|---|---|
| Six in-frame metabolic deletions: **ackA, frd, pck, ppc, tpi, zwf** | design | p. 1056, opening paragraph |
| **50** evolved deletion strains across substrates | design | p. 1056 |
| Growth rates predicted computationally in **39 of 50 (78%)** strains | **measured against predicted, AFTER adaptive evolution** | abstract; restated in results |
| Incorrect predictions are **the ppc⁻ and tpi⁻ strains** | measured | results |
| **tpi⁻: no growth computationally predicted at all** on lactate, malate, succinate | predicted (a structural failure of the reconstruction) | Fig. 1 caption |
| **ppc⁻ on α-ketoglutarate: grew 11–12% slower than predicted** | measured against predicted (a quantitative miss) | results |
| Fig. 1 arrows mark strains **>10%** different from prediction | convention | Fig. 1 caption |

**The load-bearing kind, and the one easiest to lose:** 78% is agreement *after
adaptive evolution* — the paper's strains were passaged daily for **25 to 50
days**, until growth rate stopped changing. (Corrected 31 October: this line
said "after fifty days", flattening a range into its top value. The deck says
25–50 in both its docstring and on the slide.) The paper's claim is that the
model predicts **where selection goes**, not where a freshly built knockout
sits. A naive deletion strain is not at the predicted optimum. **Any slide that
presents 78% as "the model predicts knockout growth rates" is wrong in exactly
the way the week-9 retrospective is about.**

**The payoff surface.** `readings.yaml` asks students to come with a guess about
what the eleven failures have in common. **They do not have one thing in
common**, and that is the better lesson: one failure is the network missing a
route it actually has, the other is the objective being slightly wrong. Those
need different fixes, and neither is "add more constraints."

## 4 · The mathematics, and what must be derived in the room

Session 3 built **S** and integrated d**x**/d*t* = **S·v**. This session sets
the left side to zero and asks what is left.

1. **Steady state is S·v = 0**, and that is the entire constraint. Derive it,
   do not assert it — the room has had **S** since session 3 and has never seen
   it used this way.
2. **The solution set is the null space of S intersected with the flux bounds.**
   Its dimension is what you have left to choose, and it is large: a network
   with more reactions than metabolites is underdetermined **by construction**.
   This is where the need for an objective arrives, and it should arrive as a
   consequence, not as a step in a recipe.
3. **Linear objective + linear constraints = a linear program**, hence
   `scipy.optimize.linprog`. Say why it is linear, because the room will assume
   optimisation is hard.
4. **SOME optimum of a linear program sits at a vertex** — not every one, and
   not the optimum. So FBA *reports* a corner, which is not the same as the
   corner being the only answer, and **alternate optima are generic**.
   (Corrected 31 October; this item used to say FBA "predicts a corner", which
   the deck's segment 5 counterexample refutes. The deck is right.) This is the honest limitation and it must be stated on a slide,
   not in a note: two different flux distributions can both be optimal, and the
   solver returns one of them without telling you.
5. **Knockout = a bound set to zero.** One line of code, and the reason this is
   a *design* tool.

## 5 · The worked example — specified, NOT yet built

A hand-written network small enough to solve by hand and large enough to have a
branch point whose split the objective decides. Requirements:

- fewer than ten reactions, written as a table students can read off a slide;
- **one branch point** where carbon can go to a product or to biomass;
- a knockout that moves the optimum to a different vertex;
- a knockout for which the predicted growth is **exactly zero**, because that
  is the tpi⁻ case the paper turns on and it should be met in the toy before it
  is met in the data;
- at least one pair of **coupled** fluxes, so flux coupling is demonstrated
  rather than defined.

**Do the math when we can:** the whole example should be checkable by hand at
the board, with `linprog` used to confirm and then to scale.

## 6 · Segments

1. **The object before the model.** A real pathway, named enzymes and
   metabolites, and the conservation statement in words before any matrix.
2. **S again, from session 3** — the same object, the time derivative set to
   zero. What that buys and what it throws away.
3. **The null space, and why an objective is forced.** Dimension counted on the
   toy network.
4. **The linear program.** Vertex solutions and alternate optima. `linprog` on
   the toy.
5. **Knockouts and coupling.** The zero-growth knockout. The coupled pair.
6. **Fong & Palsson.** The design, the 39/50 *after evolution*, and the two
   failures that fail differently.
7. **What an objective commits you to**, and the forward link to S21 — where
   the coupling is not written down anywhere, and is mis-drawn in the diagram.

## 7 · What is still needed

- ~~`posb.fba` does not exist.~~ **Built and tested 26 October; this whole
  section is history, kept for the reasoning rather than the status.** It did
  not exist when this was written, and `posb/__init__.py:41` declared it under
  *"Coming later in the term"*. Build it on `posb.core`'s existing **S** assembly rather
  than beside it — the syllabus sells this session as session 3's matrix
  re-asked, and the code should make that literally true.
- The toy network, chosen against §5's five requirements, solved by hand, then
  verified against `linprog`.
- A test that an alternate optimum exists in the toy and that the two vertices
  have equal objective value, so the limitation in §4.4 is **executable** rather
  than asserted.
- Figures. Fong & Palsson's Fig. 1 is the one paper figure this session needs;
  crop it only after reading the PDF to the last page.
