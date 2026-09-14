# Session 7 — Autoregulation

[← all sessions](../README.md) · **Thursday, September 17, 2026**

**Revision 2. Drafted and built 12 September from the session 6 lessons.**
Deck, handout, answer sheet and board notes all exist; `preflight.py 7` is
green except the two manual items (approve into `private/taught/`, stage the
PRINT-THIS copy). Covers **T15** (derive the negative-autoregulation speed-up), **T16**
(positive autoregulation → graphical bistability condition) and **T17**
(variance reduction under NAR). **T15 and T16 land on PS3** — T15 HAND, T16
MIX. **T17 is demonstrated here but assessed on PS6** (moved 14 September):
it cannot be computed until session 12 hands them the Gillespie sampler and
the CV, and on PS3 it could only be described. See the coverage matrix note.

Discussed today: **Rosenfeld, Elowitz & Alon 2002**, handed out at session 6.

## The one thing to remember

> **Negative autoregulation buys the same speed-up as a degradation tag and does
> not pay for it at steady state. The tag takes out a standing charge;
> autoregulation buys on credit and pays it back during the transient.**

## The object, before the model

Session 6's lesson, applied from the start: **the room sees the two curves
before it sees an equation.** The object here is not a promoter, it is a
*picture* — production rate and removal rate plotted on the same axes against
protein level, with the steady state where they cross.

Everything in this session is that one picture redrawn:

| | production curve | crossing |
|---|---|---|
| no regulation | flat line at α | one, and it is the whole of session 5 |
| negative autoregulation | decreasing | one, and the curves meet at a steeper angle |
| positive autoregulation, cooperative, with basal | increasing, sigmoid | **three**, and the middle one is unstable |

The speed-up, the bistability condition and the variance argument are all read
off that picture before any of them is derived. This is the Weiss & Arkin
Chapter-8 treatment — see below — and it is the right order for this cohort,
because the graphical argument is available to the whole room while the algebra
is not.

## What the archive already has

`20.405_LectureNotes.docx`, **"Lecture 8: Autoregulatory feedback"**, under
`Classes/PoSB/Dropbox (1)/2019/PoSB Textbook Chapters/`. It carries all three
techniques in sequence, and the 2025 deck (L10/L12) pointed students at it for
the "optional analytical comparison of steady states for open and closed loop"
without ever teaching it.

| technique | where in the notes | what it gives us |
|---|---|---|
| T15 | "Creating and understanding negative autoregulation" | the open-loop/closed-loop comparison, and a **calculus argument** rather than a simulation: at *p* = 0 the two production functions agree; the NAR derivative is < 1 where the open-loop derivative is exactly 1; therefore the NAR steady state is lower. Clean, short, and it is a proof |
| T16 | "Graphical analysis of positive auto-regulation" | three intersections, the middle one unstable, and cooperativity plus basal expression as the condition for the third to exist |
| T17 | "Comparing the kinds of autoregulation" | the distributional comparison across the three motifs — and, valuably, the notes state plainly that **ODEs cannot show this** and a stochastic model is needed |

2023–2025 decks have autoregulation only as a four-bullet summary card (NAR
speeds response, decreases variance; PAR slows, increases variance, can create
bistability) attributed to Alon. **2026 derives all four of those bullets.**
That is the session's hinge, and it is the same structural change session 6 made.

## The hinge

Session 5 ended on **one knob, two requirements**: *p** and *t*½ share the
denominator (γ + μ), so a degradation tag buys speed and pays in level, one for
one. Session 6 found a case where the knobs separate.

Session 7 asks the question session 6 left open at 81 minutes and did not
answer:

> Two cells. One expresses a protein with a degradation tag, one without, and
> both hold the same steady level. Which cell is spending more?

Most of the room says *the same*. The answer is the tagged cell, by exactly the
factor it gained in speed, forever — and the way out is not a better knob but a
different topology.

## The landing point — verified arithmetic

Host dividing every 30 min, so μ = 0.0231 min⁻¹. Hold *p** = 1000 molecules.

| route | *t*½ | steady-state synthesis | cost |
|---|---|---|---|
| do nothing | 30.0 min | 23.1 protein/min | — |
| degradation tag (40 min), α raised to hold the level | 17.1 min | **40.4 protein/min** | **1.75×, forever** |
| negative autoregulation, repression ratio 2 | 16.8 min | **23.1 protein/min** | the transient only |

**The identity is the point and it is exact, not approximate.** Since
*p** = α/(γ+μ), holding the level while adding a tag forces α up by precisely
the factor by which *t*½ falls. The energy cost of speed *is* the speed-up
factor. NAR never touches γ, so its steady-state flux equals doing nothing.

The speed-ups, stated exactly because the deck states them exactly: the tag
buys **1.75×**, NAR at repression ratio 2 buys **1.79×**, and the repression
ratio that matches the tag to the minute is **1.94**. The round design point is
2; the claim on the slide is "a shade better than the best tag", not "the same".

That is a quantitative reason NAR is the most over-represented single-node motif
in *E. coli*, and it is the session's design ledger.

## What happens — 34 surfaces, 87 min

Built, not drafted. The room comes in 5–12 minutes early, which is where the
87th minute lives; the cut order is in `board-notes/s07-board-notes.md` and the
first two cuts are cheap.

| | | |
|---|---|---|
| 0–5 | **Retrieval**, notes closed | Two from Tuesday (fold-change = F_reg; what cancelled), one interleaved from session 5 (*t*½ and *p** share a denominator) |
| 5–8 | Map + goals as questions | |
| 8–10 | **Tuesday's unanswered question** | The two cells. Take the vote, tally it on the right wing, do not resolve |
| 10–12 | **The wiring** | Autoregulation drawn as ONE EDIT to session 6's promoter: constitutive, NAR, PAR, in course notation. This is the biology slide session 6's review said was missing, moved to the front |
| 12–14 | **The object** | Production and removal on one pair of axes, built with the room. The axes go on the board here and stay all period |
| 14–16 | **How to read it** | Crossing = level; sign of the gap = stability; steepness = speed. Speed and level are separable, and that separation is the session's engineering result |
| 16–26 | **Derivation 1 — the cost identity** | 7 steps. Hold *p** fixed, raise γ, read off what α must do. Resolves the 8-minute vote at step 7 with an exact factor |
| 26–32 | **Rhythm 1** | Price the other route. Answer C, and the clue is that NAR never touches γ |
| 32–44 | **Derivation 2 — NAR** | 8 steps. Graphical argument first (the gap below *p** is larger), then α raised to compensate, then the calculus proof that the closed loop settles lower, then the two bills side by side |
| 44–47 | **Rosenfeld 2002 — the design** | What they built and what the control was, BEFORE any result. Axes taken from the room |
| 47–50 | **Rosenfeld 2002 — the result** | 0.21 against 1.0 cell cycles; both curves land in the same place; 5× measured against our 1.8× derived, and the repression ratio is why |
| 50–56 | **Rhythm 2** | Which route is the expensive one, read off synthesis rate against time |
| 56–65 | **Handout, items 1 and 2** | The same two curves, four times |
| 65–69 | The answers | Which curve moved, and which did not |
| 69–71 | **PAR — the production curve** | Same loop, opposite sign. One site saturates and can only cross once; cooperativity makes it S-shaped |
| 71–74 | **PAR — the third crossing** | The geometric condition, and the classification by sign of the gap — item 2 from minute 14, reused verbatim |
| 74–77 | **PAR — what it buys** | Memory with no memory element; the knobs are ones they already have; the threshold drifts with growth rate because μ is the line's slope |
| 77–81 | **T17 — variance, and the honest limit** | Why NAR narrows the distribution, and why the ODE cannot show it. Derivation deferred to session 12, explicitly |
| 81–84 | **Design ledger** | Knobs · Constraints · Limits |
| 84–87 | Consolidation; Gardner assigned; the closing question | *Two proteins, each repressing the other. Draw that picture.* They cannot — that is session 8's cold open |

## Where each surface lands on an engineering choice

| surface | the choice it hands them |
|---|---|
| the wiring, 10 min | a regulatory edge is a sequence change, not a new mechanism: the operator is the same object as Tuesday |
| how to read it, 14 min | speed lives in the shape of the production curve, level in the crossing — so they can be designed separately |
| derivation 1 | a degradation tag is a standing charge, and the charge is exactly the speed-up |
| derivation 2 | NAR gets the same speed for the same steady-state flux; the repression ratio is the knob, and it is set by operator affinity and promoter strength |
| Rosenfeld | the design variable is one you can order from a catalogue, and the control that makes the claim is a chemical one |
| rhythm 2 | duration decides between the two routes, and nothing in the equations says so — that is item 4 of the handout |
| PAR, 74 min | cooperativity bought for sharpness is cooperativity that buys memory; and the switching threshold moves with the medium |

## The three open questions, as resolved

1. **T16 graphically**, with the algebra on PS3. Session 8 formalises.
2. **T17 stated with its mechanism, derivation deferred to session 12**, and the
   deferral said out loud on the slide. The 20.405 notes flag the same limit.
   *Amended 14 September:* the assessment was deferred with it, from PS3 to
   PS6. The slide promises session 12 and PS6 — it must not promise a PS3
   question, because there is no longer one.
3. **The cost identity got its own derivation run** (7 steps), because it is the
   session's whole argument and the opening vote hangs on it.

## Figures — all built and verified

`figures/s07_autoregulation.py`, five of them, every number computed:

1. `s07_wiring` — the three wirings drawn in session-6 notation. Added in
   revision 2; without it the session opens on a curve for an object the room
   has never seen.
2. `s07_three_curves` — THE object, three panels.
3. `s07_bistable_condition` — the cooperativity sweep, crossings marked, filled
   for stable and open for unstable.
4. `s07_cost_in_time` — synthesis rate against time for the three routes.
5. `s07_approach` — *p*(*t*), unnormalised, all three reaching the same level.

Plus `rosenfeld2002_fig3`, cropped and declared with provenance. **Recropped in
revision 2:** the first box cut the x axis off the figure, which made the
"read the axes out loud" cue impossible to obey.

## Materials

| | |
|---|---|
| deck | `decks/s07_autoregulation.py` → 34 surfaces |
| handout | `handouts/s07-production-removal.md` (4 pp) |
| answers | `handouts/s07-production-removal-answers.md` (2 pp) |
| board notes | `board-notes/s07-board-notes.md` (3 pp) |

## Lessons carried from building it

- **The pacing check earns its keep.** Three segments of 6, 6 and 8 minutes on
  single surfaces were all flagged "you would be improvising", and all three
  were genuinely underbuilt — the fix in each case added content the session
  needed, not filler.
- **Two new build-time checks came out of this session.** A step label longer
  than the label column wraps and runs into the next row; a step equation past
  ~62 characters wraps onto its own aside. Both now print at build time, and
  both caught real collisions in decks that were already written.
- **Render the PDF and look at it.** Every one of those collisions was invisible
  in the source and obvious at 100 dpi.
