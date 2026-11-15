# Session 24, rebuilt — the plan

Agreed with Adam 14 November 2026, after a slide-by-slide review of the built
deck. This replaces the five-move structure, not the research: `NUMBERS.md`,
`DESIGN.md` §7 and every crop in `paper_figures.yaml` stand.

Reading list unchanged — required and optional stay as the syllabus has them.

---

## The thesis

**Put the work in more than one cell and place them in space. It buys spatial
function, and it spreads the burden.**

Adam's own statement of it: *the use of division of labor and spatial
cell/colony placement to reduce burden and engineer spatial function.*

**Title slide.** Plain title, then one sentence that says what the hour teaches
— not a clever phrase. Working text:

> **Two cells, placed apart**
> A signal that leaves the cell turns position into an input. Splitting the
> work across cells puts each half's burden in a different cell.

Everything in the hour serves one of those two clauses. Anything serving
neither is not in the hour.

---

## The shape

| | slides |
|---|---|
| open — title, retrieval, goals, where this sits | 4 |
| **Stop 1 · Basu 2005** — position becomes an input | 20 |
| **Stop 2 · Karig 2018** — how far the signal reaches | 12 |
| **Stop 3 · Tamsir 2011** — placement becomes the program | 4 (built 14 Nov) |
| **Stop 4 · Zhou 2015 → Tsoi 2018** — splitting the work | 11 (built 14 Nov) |
| design ledger, compressed | 4 (done 14 Nov) |
| reading | 1 |
| **hour** | **62 as built** |

Against 93 now. The predator-prey segment and eleven slides of ledger are what
pay for it.

**Every stop is built in the same five parts, in this order.** Adam, 14
November: *"introduce the paper; take us through the teach purpose and the paper
logic and results, extract the key design features, analysis and results with
specific learning for each."*

1. **The paper, introduced** — authors, title, journal and year; what they
   built; their main finding; **why this paper here**; what we will teach from
   it. One slide, two at most.
2. **Their logic and results** — how they got there, on their own figures.
3. **The design features** — what a designer can set, and what they inherit.
4. **The analysis** — the derivation or calculation the room does.
5. **The learning** — one sentence the student leaves with, on its own slide.

---

## Stop 1 · Basu 2005 — position becomes an input

**The paper.** Basu, Gerchman, Collins, Arnold & Weiss, *A synthetic
multicellular system for programmed pattern formation*, **Nature** 434,
1130–1134 (2005). They built sender colonies that synthesize AHL and a lawn of
receiver cells carrying a circuit whose output is on only over a middle range
of AHL. The lawn forms a **ring** at a distance from the senders, and receiver
variants with different detection thresholds ring at different radii.

**Why this paper here.** It is the only paper on the list where the design
variable is *where you put the cells*. It is also required reading, so the room
arrives with the figures.

**What we teach from it.** That a diffusible signal makes position an input,
and that a band — not a switch — is what makes a position readable.

**Their logic and results.** Fig. 1a for the system, Fig. 1b for the sender
plasmid, because the synthase is in the plasmid map and in the Methods and
nowhere in Fig. 1a. Then the three cases they work on p. 1130: close to the
senders, far from them, and in between. Two repression routes of opposite
parity, and the middle case is the one that does the work — both routes to dark
are open at once, so the reporter lights. Their own sentence: the repression
efficiency of CI is much higher than that of the mutant LacI.

**The design features.** Set: the two repression coefficients, by choosing
repressor and operator; the detection threshold, by a receptor point mutation
or by plasmid copy number; the synthase expression, by promoter choice; where
the senders sit. Inherited: the signal's diffusion coefficient, and the
receiver's saturation — above about 47 nM more AHL buys no more output, which
session 10 already established.

**The analysis.** Build the minimal sender/receiver model, then solve both band
edges from Basu's printed BD2 parameters. β_L = 0.8 µM for LacI on GFP, β_C =
8 nM for CI on LacI, a ratio of 100. Edges at **2.61 and 6.93 nM**, 2.65× apart,
peak at 3.973 nM. The inequality β_C ≪ β_L is what opens the window: make the
two coefficients equal and the two dark regions meet, leaving no band. The data
cannot say CI is the better repressor — only that β_C is much smaller.

**The learning.** *A band, not a switch, is what makes a distance readable —
and the window exists only because the two repressors act at concentrations
far apart.*

Techniques carried: sender/receiver model construction, band-detect analysis.

**Hands forward.** The ring sits at a radius. Nothing so far says what sets it.

---

## Stop 2 · Karig 2018 — how far the signal reaches

**The paper.** Karig, Martini, Lu, DeLateur, Goldenfeld & Weiss, *Stochastic
Turing patterns in a synthetic bacterial population*, **PNAS** 115, 6572–6577
(2018). They measured effective cell-to-cell diffusion for two AHLs in a
bacterial lawn and got patterns at a diffusion ratio far below what the
classical Turing condition asks for.

**Why this paper here.** It is the only source on the list for what a signal's
movement through a lawn of cells actually costs. Stop 1 left a radius
unexplained; this is the paper that explains it.

**What we teach from it.** The length scale, derived — and that the number you
would want for Basu's system does not exist.

**Their logic and results.** 3OC12HSL at **83 µm²/s**, C4HSL at **1810 µm²/s**,
a ratio of **21.6 ± 10**. Both are *effective cell-to-cell* estimates obtained
by modeling a fluorescence wave profile, not direct measurements — the slide
says so. Wilke–Chang predicts about **1.5** for the same pair in free solution,
so **the lawn supplies nearly all of the ratio**, not the molecules. Their own
non-stochastic simulation wanted about **100**; the stochastic version is what
they argue gets patterns at 21.6. That is a statement about their scheme, not a
classical requirement.

**The analysis, and the gap this closes.** Diffusion against first-order decay
at steady state in one dimension: D·d²A/dx² = γ·A, so A = A₀·exp(−x/ℓ) with
**ℓ = √(D/γ)**. Four steps. **This is currently asserted as a formula and never
derived, and the technique that rests on it is graded** — the deck's own header
admits it. Deriving it here is the fix.

Then the honest stop: **no slide prints a length for Basu's system.** The only
two numbers available each combine mismatched sources — one inherits a defect
in Basu's printed coefficient, the other puts Karig's 3OC12HSL with Basu's
decay rate, a different signal in a different lawn. **That is the technique's
real lesson:** you can write the length scale and still not be able to evaluate
it, and knowing why is the skill.

**The design features.** Inherited: the diffusion coefficient — you pick a
molecule and a medium and take what you get, and the lawn dominates. Set: the
decay rate, and the mechanism gets stated rather than waved at — AHL's lactone
ring hydrolyzes faster as pH rises, and Basu say that rate sets the band's
steepness. Because the reach goes as a square root, **doubling it costs four
times the lifetime.**

**The learning.** *Reach is the square root of diffusion over decay. You
inherit the numerator and can only move the denominator — and in a lawn of
cells the lawn, not the molecule, sets what you inherit.*

Technique carried: the diffusion length scale in a community.

**Hands forward.** You can now place cells a chosen distance apart and know
what each one reads. Placement is a design variable.

---

## Stop 3 · Tamsir 2011 — placement becomes the program

**The paper.** Tamsir, Tabor & Voigt, *Robust multicellular computing using
genetically encoded NOR gates and chemical 'wires'*, **Nature** 469, 212–215
(2011). One NOR gate in *E. coli*, AHL as the wire between colonies. An XOR is
three NOR gates and a buffer, one per strain, spotted on a plate. A small
library of those strains covers all sixteen two-input functions.

**Why this paper here.** It is the payoff of stop 2 and the answer to session
17. Session 17 spent an hour on how short the list of orthogonal parts is;
this is what you do about it.

**What we teach from it.** That reusing the same parts in different cells buys
program size, and that the arrangement of colonies — not the DNA — is what
changes between functions.

**Their logic and results.** Fig. 3 for the XOR, then the sixteen-function
library. Their sentence from the introduction, not the abstract: a program can
be built from a smaller number of orthogonal parts by re-using them in
multiple cells.

**The design features.** Set: which gate strain goes where. Inherited: the
wire — one AHL, shared by every gate that uses it, which is the limit.

**The analysis.** None. This stop carries **no graded technique**, which is
why it came out at **four slides, not six**: the paper, their XOR (Fig. 3),
their library (Fig. 4), one sentence. The gate and the two wires ride on the
Fig. 3 slide rather than taking one of their own, and the design features are
the `what you set` / `what you inherit` rows of the learning slide, as in
stops 1 and 2.

**The learning.** *Reusing one part in several cells buys program size that
adding parts cannot.*

**Hands forward.** More cells bought computation. What else does a second cell
buy?

---

## Stop 4 · Zhou 2015 → Tsoi 2018 — splitting the work

**The papers.** Zhou, Qiao, Edgar & Stephanopoulos, *Distributing a metabolic
pathway among a microbial consortium enhances production of natural products*,
**Nature Biotechnology** 33, 377–383 (2015) — a taxane pathway split across an
*E. coli*–yeast co-culture, at much higher titer than one strain. Then Tsoi,
Wu, Zhang, Bewick, Karig & You, *Metabolic division of labor in microbial
systems*, **PNAS** 115, 2526–2531 (2018) — the criterion for when splitting
helps at all.

**Why these two here.** Zhou is the demonstration and Tsoi is the arithmetic.
Zhou alone would be an anecdote; Tsoi alone would be a criterion with nothing
under it.

**What we teach from them.** That splitting a pathway puts each half's burden
in a different cell, and that what you pay for it is transport.

**Their logic and results.** Zhou's Figs. 1 and 2 as a pair: the pathway is
split the same way both times, and what changes is the ecology. In the first the
yeast holds the *E. coli* back. In the second the *E. coli* grows on xylose and
excretes acetate, which inhibits its own growth and which the yeast can use as
its only carbon source. **Each version removes the other's problem, and what was
engineered the second time was not the pathway.** Then Tsoi's Fig. 1C and the
criterion behind it.

**The design features.** Set: whether the pathway runs in one strain or two,
where the cut goes, and how much enzyme each half expresses — each enzyme's
burden is proportional to its expression. Inherited: the intermediate's
transport rate η and its turnover outside the cell δ_me, whose ratio is the
transport inefficiency ε_T = δ_me/η.

**The analysis.** Tsoi's criterion with both sides drawn: biomass gained against
intermediate lost. Two populations each carrying one enzyme grow better but
share a halved carrying capacity, so at zero burden division of labor starts a
factor of two behind and has to earn its way out. The crossing is where the gain
catches up. Then the worked case on two named pathways, both two-enzyme, at
μ_max/δ_υ = 10: pathway A at η = 1.0, δ_me = 0.001 gives θ_I = 1.1656 and a
border at B = **1.135**; pathway B at η = 1.0, δ_me = 0.5 gives θ_I = 1.1156 and
a border at B = **1.355**. Split one. The burden is **per enzyme** — read as a
pathway total, the verdict on A reverses.

**The learning.** *Splitting a pathway is worth it when the burden you remove
from each cell beats the intermediate you lose in transit — and the leakier the
intermediate, the more burden it takes to justify.*

Technique carried: decide whether to split a pathway across strains. It is the
only technique in the hour assessed on the home guide and the final rather than
the problem set, so its release and debrief stay whatever else is cut.

---

## What leaves the hour

**The predator-prey segment — Balagaddé 2008, 21 slides.** It serves neither
clause of the thesis. Its distinctive modeling lesson — the quasi-steady-state
reduction destroyed the oscillation because it threw the delay away —
re-lands session 11, which already carries the oscillation criterion and the
Hopf boundary as graded techniques. And session 25 already reaches a Hopf three
separate ways with its own papers: Weinberger's two-knob design space with
Huang & Baltimore's 1970 measurement beside it, the limit cycle the unstable
equilibrium settles into, and R₀ as the largest eigenvalue of the
next-generation matrix with the Jacobian checked to P = 10⁶.

The slides go to the appendix. They are built and they are good; they are not
this hour's argument.

**Thirteen slides of design ledger — DONE, 14 November.** It was seventeen,
and the reason was not content: all four ledger slides were built with
`d.derivation()`, which renders one slide per step. That reveal is right for an
argument being constructed and wrong for a ledger, which restates results the
hour already has and so has no endpoint to withhold. Converted to `d.rows()`:
four slides, same words, same dark treatment, same speaker notes. Nothing in
the deck points at the ledger, so this cost no dependency.

**Two consequences to handle, not ignore:**

- **Session 25's first two retrieval questions are built on Balagaddé** — "What
  raising session 24's D did" and "What the approximation threw away." Both are
  memory tests of the kind Adam ruled out on 14 November, so both need
  rewriting to pose a problem regardless. Session 25 defines its own dilution
  rate on its own slide instead of by contrast.
- **Three of the four home-guide items are Balagaddé.** The guide gets revised
  after the deck, which is the agreed order.

---

## Fixes carried into the rebuild, from Adam's slide-by-slide review

- **Title states what we teach**, not a clever phrase.
- **Retrieval questions pose a problem**, never ask what a past slide showed.
  Question 1's answer gets stated plainly. Question 2 is replaced: give them a
  receiver whose response saturates and ask what that costs when you want a
  band. Question 3 stays, and it is now a repeat several times over. Question 4
  is the pivot and stands.
- **No clause that does no work.** *"a coupling you did not design"* goes; say
  which coupling, what it did, and where the burden comes from physically.
- **One cell makes a concentration** — it is just far below the receptor's
  threshold, so nothing reads it. Precision, not a slogan.
- **Every paper introduced before it is used**, in the five-part shape above.
- **Speaker notes are Adam's own working notes** — not from me to him, not from
  him to the room. Plain, factual, formatted to read at a glance.
- **Nothing asserted that the course has not derived.** The length scale is the
  live instance and stop 2 fixes it.


---

## Built, 14 November 2026 — what actually happened

| | planned | built |
|---|---|---|
| stop 1 · Basu | 20 | 24 |
| stop 2 · Karig | 12 | 15 |
| stop 3 · Tamsir | 6 | 4 |
| stop 4 · Zhou → Tsoi | 14 | 11 |
| ledger | 6 | 3 |
| opening + reading | 5 | 5 |
| **hour** | 63 | **62** |
| appendix | — | 37 |
| **deck** | — | **103** |

**The predator-prey run went to the appendix, not out of the deck** — 23 slides
on Balagaddé's two-strain reactor, with its own annotated contents slide. Two
ledger rows rested on it (the reactor's dilution rate as a knob, and the shared
carrying capacity / Fig. 3C mismatch as limits); both were removed with it in
the same pass, which is why `_ledger_limits2` is gone and its surviving Tsoi row
folded into `_ledger_limits`.

**Open, for Adam:** three of the four s24 home guide items are Balagaddé-based.
The slides are still in the deck, so the items are answerable from the posted
PDF — but they now point at an appendix the hour does not teach from. That is
his call, not a defect to fix silently.
