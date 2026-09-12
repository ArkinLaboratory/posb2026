# Session 6 — Promoter occupancy from statistical thermodynamics

[← all sessions](../README.md) · **Tuesday, September 15, 2026**

**Plan settled; built Wednesday 9 September** — early, under *Earlier is always
allowed* in [the weekly ritual](../../docs/weekly-ritual.md), because the design
was settled and session 7 needed Friday. Deck, four figures, handout, answer
sheet and board notes all exist; `preflight.py 6` exits 0. Not yet reviewed on
paper, and no `private/taught/` copy.

Covers **T13** (promoter occupancy from a partition function) and **T14**
(derive activator, repressor and AND-like regulation functions). Both are
hand-derived and assessed on **PS3 and the midterm**. Discussed today:
**Bintu et al. 2005, models**. Handed out today: **Rosenfeld et al. 2002**.

## The one thing to remember

> **Enumerate the states, weight each by its Boltzmann factor, divide by the
> sum. Everything else — repressor, activator, cooperativity, an AND gate — is
> that one calculation with different states in the list.**

And the design consequence, which is where the session lands:

> **Cooperativity buys sharpness, not amplitude. Session 5's two requirements
> shared a knob; today's do not — and which case you are in is a property of the
> mechanism, not of how hard you push.**

## Where this sits relative to 2025

**It has no 2025 ancestor.** Searching all twenty-four of last year's lecture
PDFs: *partition function*, *Boltzmann*, *statistical mechanics*, *Shea*,
*Ackers* — **zero hits in any deck**. *Hill coefficient* and *cooperativity*
appear twice each, in L20 (Sequential Dynamics, 6 November) and L21 (Latches II
and Oscillators, 13 November), and nowhere else.

So in 2025 the Hill function first appeared in **November**, as a modelling
convenience inside a latch, and where a regulation function comes from was never
taught. The order was also inverted: L12–L18 were six lectures of logic
synthesis and gate minimisation **before** any dynamics, with the gate taken as
given.

2026 derives the gate in week 3 and defers the digital abstraction to S13. That
is the whole structural change, and this session is its hinge.

## The hinge — why we derive this again

Session 4 already produced a regulation function: write the binding equilibrium,
form the bound fraction, cancel [P], out comes *x*/(*K*ᵈ + *x*).

**That method cannot DERIVE an activator, only assume one.** You can always
posit a productive bound state and hand it a rate constant — 2025's L10 did
exactly that, and Chapter 3 §3.3.7 does it with $k_b$ and $k_t$ — but the method
cannot tell you what that rate is, how two sites combine, or why the answer does
not depend on the size of the genome. Activation is not "blocked or not": an
activator either **recruits** RNAP — a protein–protein contact — or **stimulates
the closed-to-open transition**, and there is no dissociation constant for
*makes transcription more likely*.

*Rephrased 9 September.* The earlier wording — "that method cannot do an
activator" — is too strong and a student who did the assigned Chapter 3 reading
can catch it. Assuming a productive state is not deriving one, and that is the
sharper claim.

The statistical-mechanics route can, because it enumerates **states of the
promoter** and gives each a weight. As Gedeon et al. put it, the Shea–Ackers
nonlinearity *"is a generalization of the Hill function that naturally allows for
multiple binding factors."* Session 4 gave the special case; today gives the
general one, and the generality is the point.

## What happens

**Revised 11 September, and the revision is structural.** The first build taught
the mathematics with no biology under it — see the log entry for that day. Three
tutorial surfaces now precede any counting, and they are paid for by cutting the
Ackers segment and ConcepTest 3.

| | | |
|---|---|---|
| 0–5 | **Retrieval**, notes closed | Two from Thursday, one from session 4 — the Hill derivation, today's hinge |
| 5–8 | Map + goals as questions | |
| 8–12 | **The object** | A promoter, drawn. −35, −10, +1, and an operator in both positions. Where the site sits decides the mechanism |
| 12–16 | **Where the polymerase is** | Bintu Fig. 1a: almost all RNAP is stuck to DNA. Session 2's search problem, with the other consequence. *N*_NS arrives as a fact about cells. Fig. 1c makes the weak-promoter limit visible — lac at 10⁻³ |
| 16–20 | **Two levers, and only two** | Recruitment versus the closed-to-open transition, drawn. Today's model charges for the first and holds the second fixed, and the room is told so while the choice is made |
| 20–22 | **The hinge** | Try to write an activator's regulation function the session-4 way |
| 22–34 | **Derivation 1**, 8 step slides | States, weights, *p*_bound, the weak-promoter limit |
| 34–38 | **Rhythm 1** | Do you need to know *N*_NS to read a fold-change? |
| 40–49 | **Derivation 2**, 7 step slides | Simple activation: *lac* + CRP₂*. *K*_A and *f* |
| 49–55 | **Rhythm 2** | Ten-fold out, four-fold in |
| 55–59 | λ P_RM, from the paper | Cooperativity **buys sharpness, not amplitude** |
| 59–61 | **Pause** | |
| 61–70 | **Handout, items 1–2** | |
| 70–74 | The answers | |
| 74–78 | **λ O_R as a solved specification** | Ackers 1982. Two outputs, opposite requirements, one input — met with the knobs on the right wing |
| 78–81 | **Design ledger** | Knobs · Constraints · Limits, checked against the room's own minute-12 list |
| 81–83 | **The comparison** | Thursday's one knob against today's two, on its own surface |
| 83–87 | Consolidation; **Rosenfeld 2002 handed out** | |

### Budgeted to 87 against an 80-minute room

Adam, 12 September: sessions have been finishing **five to twelve minutes
early**. Four of the extra minutes bought back the λ O_R case study; the other
three came from expanding both derivations after he found derivation 1 doing
the multinomial, the *P* ≪ *N*_NS limit and the definition of *p* in a single
step. Six steps became eight, five became seven, and both runs now sit at
1.3–1.5 min/step.

Seven minutes over an eighty-minute budget only works at the optimistic end of
the observed slack, so **two segments are designated to go, in order**, and the
board notes carry the list: λ O_R at 74 first, then the prompts under the
answers at 70. Both are placed where dropping them costs nothing downstream.

### What was cut, and why

**ConcepTest 3 (was 66–72), and the λ O_R segment, since restored.** Together
they bought the twelve minutes of biology.

ConcepTest 3 asked the room to accept that an activator can repress. That claim
is *entirely* about the two levers — recruitment versus isomerisation — and
before the 16-minute slide existed it rested on vocabulary nobody had been
taught. It is now a stated entry in the Limits column with Gedeon cited, which
is what that column is for. It stays cut.

**λ O_R was restored on the 12th** on the strength of the observed slack: it is
the session's only worked engineering case study, and it now closes the loop the
minute-12 question opens.

### Where the engineering lands, surface by surface

The first build put every design consequence in the last six minutes. Now:

| surface | what it lets you choose |
|---|---|
| 8–12 the object | **the tee-up question**: what can you change, and what would you have to do to change it? The room's answers go on the right wing and stay there until 75 |
| 16–20 two levers | which lever a part uses decides whether it travels between constructs |
| 22–32 derivation 1 | a part is characterised in fold-change, not in molecules, because everything unmeasurable cancelled |
| 36–38 ConcepTest 1 resolve | **the composability result** — *p* is the core promoter and it cancelled, so the same part on any weak promoter gives the same fold-change. And C is that reuse breaking: modularity is a property of the regime, not the part |
| 46–52 ConcepTest 2 | a specification you can price and reject before cloning |
| 52–56 λ P_RM | sharpness and amplitude are separate knobs |
| 71–75 λ O_R | a two-output specification met with exactly the knobs on the right wing |
| 75–80 ledger + comparison | whether your requirements share a knob is a property of the mechanism |

The minute-12 question is the spine of that column: the Knobs list is not handed
down at 75, it is the room's own list from before any mathematics, checked.

### The cost, stated plainly

Student working time falls from **37 of 80 minutes (42%) to 30 (34%)**. The
tutorial block is exposition, and no relabelling changes that — `min/step` on
both derivation runs is 1.6–1.7, well inside the cap, so the session is not
rushed, it is simply more expository than session 5. 34% sits inside the course
band (s04 28%, s09 34%, s01 38%) at the low end.

The honest alternative is that **this is two sessions' material**: T13 and T14,
a ledger, and two historical case studies do not fit in eighty minutes once the
biology is taught properly. Nothing in the schedule makes room, so the cut above
is the answer for this year, and the note for next year is in the log.

Two derivation runs on slides, not four — see below.

## The handout — one derivation, four times

Per [lecture-design §1](../../docs/lecture-design.md): the same problem repeated
with **less of my working shown each time**, so a physicist can start at item 3
and a biologist can work item 1 carefully, and neither has to announce which
they are. Four versions of one calculation — list the states, weight them, sum,
divide — on promoters of increasing architecture:

| item | promoter | how much working is shown | where |
|---|---|---|---|
| 1 | **Simple repression** — truncated *lac* (lacUV5), LacI₄ at O_m, one parameter *K*_m | all of it, every step labelled | in the room |
| 2 | **Activator + helper** — λ P_RM, cI₂ at O_R2 and O_R1, with ω | all but the **last step** | in the room |
| 3 | **Two different TFs** — *melAB*: MelR₂* activates at O2, CRP₂* helps at O1 but does not itself activate | all but the **last two** | PS3 |
| 4 | Design a promoter whose fold-change is AND-like; give the truth table | none | PS3 |

Header instruction, as on every one of these: *start wherever the scaffolding
stops helping you.*

## Why two derivations on slides and two on paper

**Not for pacing reasons.** An earlier revision of this plan argued the split
from session 8's numbers and claimed four derivation runs would drop the room to
22% working time. That was a measurement error — session 8's handout block was
mislabelled and counted as exposition; it is **36%**, and all four of its runs
are paced at 1.6–2.5 min/step, inside session 5's own range. Four runs is fine.
The retraction is recorded in the decisions log.

The split is a content judgement, and it holds on its own:

- **The machinery goes on slides** because it is new, it is the assessed skill
  (T13), and there is no shorter route to it.
- **The activator goes on slides** because it is the reason the session exists —
  it is the thing session 4's method cannot do, and if the room does not watch
  that happen, the session is session 4 with more notation.
- **The repressor goes on the handout** because it is *not a new result*. They
  already have the answer from session 4. Its whole value is as a check that the
  new machinery reproduces the old one, and confidence is exactly what a fully
  worked first item is for. Deriving it on slides would spend ten minutes
  arriving somewhere they can already see.
- **The AND case goes on PS3** because it is a **design** question — choose an
  architecture that meets a truth table — not a derivation. Design questions
  need room to be wrong in, and eighty minutes does not have it.

## The real systems, and where the numbers come from

All four cases are worked in **Bintu et al. 2005, applications** (Curr Opin
Genet Dev 15:125–135), which is now in `literature/`. Its Table 1 is the
preceding paper's Table 1, and the weak-promoter limit is what makes fold-change
equal the regulation factor.

| case | promoter | parameters |
|---|---|---|
| simple repression | lacUV5, O_m | *K*_m |
| simple activation | *lac*, CRP₂* | *K*_A, enhancement *f* |
| activator + helper | λ P_RM, cI₂ at O_R1/O_R2 | *K*_R1, *K*_R2, cooperativity ω, *f* |
| two TFs | *melAB*, MelR₂* + CRP₂* | *K*_1, *K*_2, ω, *f* |

**Extracted 9 September**, all read off rather than recalled:

| quantity | value | where |
|---|---|---|
| *N*_NS | 5 × 10⁶ | models paper, Fig. 1 legend |
| *f* (λ P_RM) | ≈ 11 | applications, Fig. 2 legend |
| ω | 80 (range 49–130); Bintu round to 100 | Koblan & Ackers 1992, Table II, 37 °C |
| ω | 25.2 — **superseded** | Ackers, Johnson & Shea 1982, Table 3 |
| *K*_R2/*K*_R1 | ≈ 25 | applications, text |
| sensitivity *s* | .54, .66, .84, .93 for ratios ∞, 10³, 10⁻¹, 25 | applications, Fig. 2b legend |

*K*_A and *f* for *lac*/CRP are **not stated numerically** in the applications
paper — they are defined as things you read off Figure 1b, and the paper says
its inferred in vivo *K*_A is "not expected to be accurate to within a factor of
2." The slide says so too.

**The two ω values are the same laboratory at the same temperature, ten years
apart.** Bintu's *f* ≈ 11 is Hawley & McClure 1982; their ω ≈ 100 and their
"realistic" *K*_R2/*K*_R1 ≈ 25 both come from the 37 °C row of Koblan & Ackers
1992 (measured ω = 80, range 49–130; measured ratio 26). The 1982 value of 25
lies **outside** that interval, and the 1992 error bar is five times wider
because it now includes systematic differences between experiments and between
operator templates. Both curves are on the figure.

The 1992 paper also kills an inference I had made from its title: cooperativity
is **temperature-invariant** across 5–37 °C. What moves with temperature is the
intrinsic site affinity, and differentially — so it is *K*_R2/*K*_R1 that is
temperature-controlled, 26-fold at 37 °C and 92-fold at 5 °C. Feeding each
temperature's measured pair through the derived expression gives *s* = 0.92,
0.93, 0.91, 0.86, 0.76 from 37 °C down to 5 °C: **both inputs swing by a factor
of four and the sharpness barely moves.** That robustness result is the answer
sheet's closing argument, and it is only visible because the regulation function
was derived rather than quoted.

**The regulation factors are derived, not transcribed.** Bintu's Table 1 is an
image in both PDFs and cannot be extracted as text, so
`figures/s06_promoter_occupancy.py` derives the forms from the state list. Those
derived forms then reproduce **all four** sensitivities in the Figure 2b legend
— .54, .66, .84 and .93 — which is the check that the algebra on the slides is
the algebra in the paper.

## The design ledger

Per [lecture-design §5d](../../docs/lecture-design.md#5d-every-session-ends-with-a-design-ledger).
This session has an unusually good one, because the whole derivation is a list
of things a sequence can change.

| | |
|---|---|
| **Knobs** | **Operator affinity *K*** — it is a binding site, so it is a sequence, and you can mutate it. **Number and spacing of sites** — add a helper operator. **The interaction energy ω** — whether two bound proteins touch, which is protein-surface and linker design. **The enhancement factor *f*** — which activation mechanism you recruit through. **Promoter strength** — the core −10/−35. |
| **Constraints** | ***N*_NS is the genome.** You do not set the number of non-specific sites, and this is *why* fold-change rather than absolute occupancy is the observable — the unknown drops out of the ratio. **RNAP availability is shared**, set by growth rate and by every other promoter in the cell. ***k*_B*T* is not adjustable**, which is what makes ~2–3 *k*_B*T* of cooperative interaction a large effect and 0.1 nothing. **And synthesis flux is a currency you have not been charged for yet** — see below. |
| **Limits** | **The weak-promoter limit** is what makes fold-change equal *F*_reg. Strong promoters break it, and the observable that tells you is expression approaching the ribosomal genes'. **Equilibrium** — the whole framework assumes binding equilibrates fast against transcription; milliseconds against minutes, so it holds in bacteria and is shakier in eukaryotes. **The monotone arrow** — see below. |

### The result the ledger turns on

From the applications paper, λ P_RM: the helper operator O_R1 **does not change
the degree of full activation, which is still *f***. What it changes is the
log–log slope of the transition region.

**Cooperativity buys sharpness, not amplitude.** So if a specification asks for a
sharper switch, add a helper site; if it asks for a higher ON level, that is a
different knob. Two requirements, two knobs.

Session 5 ended on the opposite result — *t*½ and *p** share the denominator
(γ+μ), so a degradation tag cannot buy speed without paying in level. **One knob,
two requirements.** Putting the two ledgers side by side is the point:
*whether your requirements share a knob is a property of the mechanism*, and
finding out is the first thing a designer does. That comparison is the strongest
single thing in this session and it should be said out loud.

### λ O_R: the specification, already solved

Ackers, Johnson & Shea 1982 (PNAS 79:1129) — now in `literature/` — is the
original of this whole framework, and it reads as an engineering document. All
interaction parameters measured at 37 °C, 0.2 M KCl from DNase protection. With
them, the model predicts the repression curves at **two divergent promoters at
once**: at physiological repressor concentration, P_R is nearly completely
repressed while **P_RM remains highly active**.

One input, one operator region, two outputs with opposite requirements — met by
tuning site affinities and the cooperative interaction between adjacent dimers.
That is a two-output specification solved with the knobs in the table above, and
it is worth saying that evolution got there first and that Gardner (session 9)
does the same thing deliberately.

### Where the abstraction stops: the monotone arrow

Bintu's weak-promoter treatment assumes transcription rate ∝ *p*_bound. The
Shea–Ackers model is more general: each control state *s* carries **both** an
association constant *K*_B(*s*) **and** an initiation rate *k*(*s*), because a
bound activator can change how often RNAP is *there* or how often it *fires*
once it is.

Restore that second lever and Gedeon et al. 2008 show the monotonicity everyone
assumes *"is correct only for the simplest of promoters."* **An activator can
repress.** Every network diagram in this course, and in Alon, puts a + or − on
every edge; that labelling is the simple-promoter limit of what was derived
today. It belongs in the Limits column, and it is the reason the Limits column
exists.

### The same mathematics one level down

Arkin & Ross 1994: the steady states of enzymatic mechanisms are *"analogous to
either Boolean or fuzzy logic gates"*, and *"nearly perfect digital function is
obtained only in the regime in which the enzymes are saturated with their
substrates."* With real rate laws their AND-like mechanism is an **asymmetric
fuzzy AND**.

Two levels, one lesson, and both halves matter to an engineer: the machinery
**generalises** — states and weights work at the promoter and at the enzyme,
which is the reason to learn it rather than memorise Hill functions — and the
**labels do not**. Saturation is the enzymatic version of the weak-promoter
limit: another regime you have to know you are standing in.

### The foreshadow — one question, no arithmetic

The full pricing belongs in session 7, where negative autoregulation makes it
sharp. Session 6 leaves exactly one question on the consolidation slide, asked
and **not answered**:

> Two cells. One expresses a protein with a degradation tag, one without, and
> both hold the **same steady level**. Which cell is spending more?

Most of the room will say *the same* — the levels are equal, so what is there to
spend? It is the wrong answer and they cannot yet see why, which is the same
deliberate non-resolution as session 5's ConcepTest 1. Fifteen seconds, no
numbers, and Thursday opens on it.

It also does real work in this session. The Constraints column already says RNAP
is a shared reservoir; every promoter in the cell draws on the same pool, and
today's calculation treated that pool as infinite. The question above is the
first crack in that assumption, and S19 is where it becomes the whole subject.

## What this sets up

**S07 — autoregulation, and where the cost question is answered.** Two threads
land there. Rosenfeld's speed-up needs the regulation function to be decreasing
*everywhere* — now a checkable condition rather than a picture, and the check is
the one derived today.

The second thread answers Tuesday's closing question, and it is the session's
design ledger. **Three ways to reach the same steady level 1.75× faster**, in a
host dividing every 30 minutes, holding *p** = 1000 molecules:

| route | *t*½ | steady-state synthesis | what it costs |
|---|---|---|---|
| do nothing | 30.0 min | 23.1 protein/min | — |
| **degradation tag**, α raised to hold the level | 17.1 min | **40.4 protein/min** | **1.75×, forever** |
| **negative autoregulation** | ~17 min | **23.1 protein/min** | the transient only |

Since *p** = α/(γ+μ), holding the level while adding a tag forces α up by exactly
the factor the response time falls — **the energy cost of speed is the speed-up
factor, identically.** NAR does not touch γ, so at steady state its flux is the
same as doing nothing: it buys the identical speed-up and pays only during the
rise, with a strong promoter that throttles itself as the protein accumulates.

**The tag takes out a standing charge; autoregulation buys on credit and pays it
back.** That is a quantitative reason why NAR is the most over-represented
single-node motif in *E. coli*, and it is the answer to Tuesday's question.

**S08 / S09 — phase plane and the toggle.** A nullcline **is** a regulation
function. Its shape decides how many fixed points there are, so Gedeon's
non-monotonicity is not an aside — it is a claim about how many intersections
two nullclines can have. Gardner's toggle works because he chose promoters where
the arrow is reliably negative, and after today that reads as a **design
decision** rather than as biology.

**S10 — feedforward loops.** The motif literature labels every edge + or −. We
will use it, and the students will know what that labelling costs.

**S13 — the digital abstraction.** Arkin & Ross's "only in saturation" is the
caveat S13 exists to install, with noise margins as the quantitative form of it.

## Before Friday's build

- [ ] Paper figures: `bintu2005models_fig1` (reservoir + states); from the
      applications paper, `bintu2005apps_fig1` (*lac*/CRP fold-change),
      `fig2` (λ P_RM, the sharpness result), `fig3` (*melAB*, two TFs)
- [ ] Numbers read off the applications paper, not recalled
- [ ] Our own states-and-weights table as a figure — the object a student should
      be able to reproduce from memory
- [ ] Handout `s06-*.md`, items 1–2, plus answer sheet
- [ ] Board notes: the states table is the ledger, left wing, stays up
- [ ] Three ConcepTests

## Settled, and still open

**Settled.**

- **λ P_RM twice is right** — here in its natural context, at S09 refactored for
  use. Gardner brings its own promoters, so the repetition is spacing rather
  than a missed organism.
- **The origin to cite is Ackers, Johnson & Shea 1982 (PNAS 79:1129)**, with
  Shea & Ackers 1985 (J Mol Biol 181:211) as the full treatment — both now in
  `literature/` — and Gedeon et al. 2008 as the critique.
- **The last quarter stays.** λ O_R as a solved specification, the ledger, the
  monotone-arrow limit and the enzymatic generalisation. PS3 tests only the
  computation.

**Still open.**

1. **Where does the energy telegraph actually go?** Two minutes in S06's ledger
   as drafted. The alternative is to hold it entirely for S07, where NAR makes
   it sharper, and keep S06's ledger to promoter architecture. Doing it twice
   would be spacing; doing it twice badly would be repetition.
2. **Does the AND-like item need a real promoter?** Items 1–3 are lacUV5, λ P_RM
   and *melAB*. Item 4 is currently a design question with no organism attached,
   which is either the right kind of open-endedness for a bare item or a loss of
   the grounding the other three have.
