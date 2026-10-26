# Session 21 — Retroactivity: reading a signal changes it, and the first repair in Part II

**Thursday 5 November 2026.** Part II, sixth session. **PS7 due; PS8 posted.**
Required reading: Mishra, Rivera, Lin, Del Vecchio & Weiss, *Nat Biotechnol* 32
1268–1275 (2014) — the **load driver**. **PDF not yet held**; PMC4262674 serves a
JavaScript interstitial on every route tried, so it needs a browser or Adam.

**Status: DESIGN. §3's claim is SETTLED — derived, integrated and swept on 26
October; see `NUMBERS.md`. It refuted the hypothesis it was written to test, and
the session is better for it. Mishra's measured numbers in §4 remain
[unverified], taken from `readings.yaml`'s focus note rather than the paper.**

---

## 1 · Where this sits in the arc

Rung 3 of the ladder in `sessions/s20-metabolic/DESIGN.md` §1. Two things make
this session different from the two before it, and both should be said out loud:

**It is the third instance of one mechanism, and the room has been told to
expect it.** `decks/s19_resources.py:_close` put a three-row ladder on the
board — a transcription factor held by its decoy sites (S18), a ribosome held by
every other mRNA (S19), **a regulator held by its downstream targets (S21)** —
and its speaker note calls that *"the surface the hour exists for."* So **this
session opens by collecting on that promise**, not by introducing a topic.
Sequestration is not an analogy across the three: it is literally the same move,
and this is where it gets a name and a number.

**It is the first repair.** Rungs 1 and 2 diagnose — measure the burden, compute
the fluxes. Rung 3 is the first place in Part II where a context problem is
*engineered away*, with the load driver. That escalation is the session's shape:
derive the damage, then build the thing that undoes it.

It also closes an old debt. `docs/coverage-matrix.md` records retroactivity as
**assessed for 20 points on PS5 in a prior year with no demonstrating lecture**,
and `docs/deck-triage.md` finds *"retroactivity"* **0 times in 962 pages** of
2025 decks. This session is that fix.

## 2 · The object before the model

A transcription factor X is produced and removed. Downstream, a promoter carries
operator sites that X binds. The diagram draws an arrow from X to the downstream
module, and **the arrow is a lie about the physics**: an arrow carries
information and costs nothing, while an operator site is a molecule that *holds*
X. Name the molecules before any algebra: which X, which sites, how many copies.

## 3 · The derivation, and the result — SETTLED NUMERICALLY 26 OCTOBER

X + p ⇌ C on p_tot downstream sites, production and removal of free X given by
f(X). Conservation gives C(X) at quasi-steady state — **the same QSSA move as
session 4 and the same occupancy as session 6, pointed at a third pool.**
Nothing new has to be invented, and the deck should say so: third time, same
move. The chain rule then gives

> **dX/dt = f(X) / (1 + R(X))**, with **R(X) = p_tot·K_d/(K_d + X)²**

**Verified**: this reproduces the full binding kinetics' half-time to 2 × 10⁻⁷.
All numbers below are in `NUMBERS.md` with the scripts that produced them.

### What the earlier draft of this section got wrong

It claimed the load leaves the steady state untouched and changes only the
speed, and concluded that *"a student measuring endpoints would not detect
retroactivity at all."* **That is true only if the sequestered molecule is no
longer being removed.** Two models:

- **Complex not removed:** the steady state of free X is **exactly** k/γ at
  every load — verified to 10⁻¹⁶. Only the dynamics change.
- **Complex removed at γ — the growing cell, and the physical case:**
  **X + C = k/γ exactly**, so free X falls by precisely the number of molecules
  parked on the sites. **The level does move.**

In the growing cell the level shift and the slowdown are the **same order** —
both linear in p_tot/X_T, within a factor of 1.45 of each other — so endpoints
are about as informative as dynamics. **The "endpoints miss it" surface is cut.**

### The result, and it reverses the intuition students will bring

The hypothesis this was written to test — level shift scaling as p_tot/X_T,
slowdown as p_tot/K_d, so tight binding buys sharpness at the cost of speed —
**is wrong.** Sweeping affinity over four orders of magnitude at fixed load
changes the slowdown by **under 3%.** What sets both costs is the **number of
sites relative to the number of molecules**:

| p_tot/X_T | slowdown | relative level shift |
|---|---|---|
| 0.01 | 1.0145 | 0.00999 |
| 0.1 | 1.1448 | 0.09989 |
| 1 | 2.4483 | 0.96887 |
| 10 | 15.4833 | 0.99989 |

In the weak-load limit the level shift is **exactly p_tot/X_T** and the slowdown
is **about one and a half times it** — the ratio is constant at 1.450 over
fiftyfold in load, and **that coefficient is measured, not derived**, so no slide
presents it as a closed form. Deriving it is a good 247 item.

**Affinity re-enters only once K_d ≳ X_T**, where the sites stop being
saturated — and there the load vanishes because the occupancy does. Which gives
the session its engineering sentence:

> **You can escape the load by weakening the operator, and it buys you nothing:
> an operator with K_d ≫ X_T is an empty operator, and an empty operator
> regulates nothing. The load is the price of the regulation, and you cannot pay
> less without buying less.**

That is session 18's shape again — the threshold walking to 1 as the switch
sharpens — and session 17's *a parameter is manufactured, not found*. **And it is
why the cure is timescale separation rather than affinity tuning: the load driver
changes neither p_tot nor K_d.** It makes the upstream module fast enough that
the parking stops mattering. The repair is on a different axis from the damage,
and that is the best thing in the hour.


## 4 · Mishra 2014 — READ 26 OCTOBER, all numbers verified

Full extraction in `NUMBERS.md` §6. The four things that change the session:

1. **It is yeast, and it is session 18's pathway.** The load driver runs on
   **STAT5-HKRR → YPD1 → SKN7 → PTR-SSRE**, in a *hot1Δ hog1Δ sln1Δ*
   background. SKN7, YPD1, SLN1, HOG1 and HOT1 are the same osmolarity pathway
   session 18 names from Mishra 2021 — same lab, same chassis. **The room meets
   these proteins on 27 October and again on 5 November doing a different job.**
2. **The repair is phosphotransfer** — session 18's covalent cycle used as the
   fast stage. The device that fixes retroactivity is the object session 18
   spent an hour on. That is the arc link, and it is free.
3. **Box 1's model is ours with f(y) = G·(u − y).** Their bandwidth is **α·G
   with α < 1**, and **α = 1/(1 + R)**. That identity is the translation table
   this deck needs, the way session 18 needed K₁ ↔ k₁ — and it is also the
   proof that the repair is on a different axis: you cannot change α, so you
   raise G until α·G outruns every input frequency that matters. **The load
   driver does not reduce the load. It outruns it.**
4. **The load is literally extra binding sites** — TR-SSRE promoters on
   high-copy 2µ plasmids, everything else single-copy chromosomal. That is
   p_tot, measured.

**The numbers to teach are minutes, not percentages.** Rise time to 90%,
unbuffered: **396.1 ± 23.0 min at 0× load, 698.9 ± 47.9 min at 2×** — the
abstract's 76.5 ± 1.8%. Buffered: **432.4 → 423.2 min**, a 2.13 ± 2.94% change,
within error of zero.

**And the cost the abstract does not mention:** the buffered system at zero load
is **432.4 min against the unbuffered 396.1** — about **9% slower**. Insulation
is not free, and that is the right note to close the segment on.

**Figure 4c cannot be cropped as-is.** Its caption's number order is reversed
with respect to the plot, and its dotted-line colours do not match their curves,
so a student reading colour-to-colour gets the result backwards. Both found by
rendering it at 300 dpi; see `NUMBERS.md` §6.4. Either annotate heavily or
redraw from `posb.retroactivity` with their points overlaid — the redraw would
also make α = 1/(1+R) visible in one picture, which is probably worth doing.


## 5 · Segments

1. **Collecting on session 19's promise.** The three-row ladder again, and the
   claim that the arrow in the diagram is wrong about the physics.
2. **The object.** Named molecules, site counts, and what "load" means when the
   thing being loaded is a transcription factor.
3. **The derivation.** QSSA for the third time; R(X); the slowdown factor.
4. **What the load costs, and what it does not depend on.** Both costs set by
   sites-per-molecule; affinity swept and found irrelevant while the sites are
   saturated; and so the sentence that the load is the price of the regulation.
   **This is the session's best surface**, and it is a result the room will
   expect to come out the other way.
5. **Mishra's measurement.** The loaded module, the numbers, the figure.
6. **The repair.** The load driver: insulation by timescale separation. Why a
   fast, strong intermediate stage absorbs the load. **The first engineered cure
   in Part II.**
7. **Forward to S22.** One insulating device fixes one interface. A controller
   rejects any disturbance — which is Tuesday.

## 6 · Scope decisions

- **Derived in the room, not stated**, per locked decision 5 and the standard
  S19 set: its isocost and hidden-edge results were derived, and this is the
  same tier of result.
- **The load driver is a segment, not a mention.** It is the technique assessed
  on PS8 and the reason the session is a repair rather than a diagnosis.
- **No phosphorylation-cycle re-derivation.** Session 18 did covalent cycles; the
  load driver's mechanism gets cited back to it in one line.
- **S19 called this "Thursday" from a Thursday.** Low priority, but if the S19
  deck is touched before the 29th, that word is worth one character of fixing.

## 7 · What is still needed

- **Mishra 2014's PDF.** Blocks the figures and all four numbers in §4.
- ~~The §3 claim settled numerically~~ — **done 26 Oct**, both models, in
  `NUMBERS.md`; scripts in `private/scratch/s21/`. Next: port the three results
  into `posb.retroactivity` as tested functions so the claim is executable and
  the figures render from it, rather than living in prose that can drift.
- `posb.retroactivity` — R(X), the slowdown factor, the loaded-versus-driven
  response, and the timescale-separation condition the load driver exploits.
  Built on the existing partition-function code, tested against integration of
  the full binding kinetics the way S19's competition result was.
- Figures: the loaded-vs-unloaded step response is ours; the measurement is
  Mishra's and comes from the paper.
