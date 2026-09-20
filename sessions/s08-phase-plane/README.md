# Session 8 — The phase plane: nullclines, fixed points, linear stability

[← all sessions](../README.md) · **Tuesday, September 22, 2026**

> **Rebuilt 18 September on the split surface.** Every derivation run now
> advances a picture beside the algebra (`Deck.derivation_fig`), generated from
> `posb` in [`figures/s08_phase_plane.py`](../../figures/s08_phase_plane.py).
> Handout, answer sheet and board notes are built. Adam's diagnosis, 18 Sep:
> the ten minutes lost per class go on proofs that are not clear enough on the
> slide — this session had no picture of the plane at all.

## Why this one was built first

This is the **test case** named in [lecture-design §5c](../../docs/lecture-design.md):
the highest element-interactivity content in Part I, in the session where the
cohort is thinnest, built with slide-resident derivations to find out whether the
step-slide format survives it.

The gap is documented and severe. [deck-triage §3](../../docs/deck-triage.md):
across all 962 pages of the 2025 corpus, **`nullcline`, `Jacobian`, `eigenvalue`
and `bifurcation` each appear zero times.** Of 21 onboarding respondents, 5 had
ever seen a phase portrait. Twenty coverage-matrix points are assessed on it.

**Verdict so far:** the format holds. Four runs, 4–5 steps each, 2.0–2.5
minutes per step, and the whole of each derivation is legible as a single page in
the exported PDF. Revisit after it is taught.

## The one thing to remember

> **You can tell whether a circuit is a switch without solving it. You need the
> places it can sit still, and whether it stays there when you push.**

## What happens

| | | |
|---|---|---|
| 0–6 | **Retrieval**, notes closed | Try session 5's method on coupled equations. Where does it fail? |
| 6–8 | Goals as questions | The third one gets an exact answer today |
| 8–12 | **Run 0**, four steps | Where *a* and *n* come from — Gardner Box 1 in our notation; the one-lifetime assumption named |
| 12–21 | **Run 1**, five steps, picture | Nullclines are curves; fixed points are crossings; the flow everywhere else |
| 21–27 | **Rhythm 1** + resolution figure | How many times can two decreasing curves cross? *(B — one or three)* |
| 27–36 | **Run 2**, four steps, picture | Substitute, collapse onto the diagonal, get *x* + *x*ⁿ⁺¹ = *a*; worked at **a = 3** |
| 36–43 | **Run 3a**, four steps, picture | Linearise → Jacobian → eigen-directions |
| 43–50 | **Run 3b**, five steps, picture | The toggle's entries one at a time → λ = −1 ± g → stable iff g < 1; the antisymmetric direction is the switch being born |
| 50–58 | **Run 4 — the payoff**, five steps, picture | *a*<sub>c</sub> = *n*(*n*−1)<sup>−(n+1)/n</sup>, derived, with the tangency and the *a*<sub>c</sub>(*n*) curve |
| 58–61 | Gardner Fig. 2c,d beside our recomputation | The same wedge, two different arms; pTAK117 on it |
| 61–65 | τ–Δ plane, as a figure | The toggle's track at τ = −2; the oscillator's exit labelled for session 11 |
| 65–72 | **Rhythm 2** + resolution figure | *n* = 1.8, *a* = 5. Is it a switch? *(A — yes; a<sub>c</sub> = 2.55)* |
| 72–80 | Handout, then Gardner assigned | [The switch Gardner built has γ = 1](../../handouts/s08-asymmetric-toggle.md) |

Badges on the new surfaces are placeholders subdividing the 7 September ranges;
the run sheet is Adam's.

## The result this session exists to produce

The symmetric toggle, which is also Thursday's reading:

d*u*/d*t* = *a*/(1+*v*ⁿ) − *u*  ·  d*v*/d*t* = *a*/(1+*u*ⁿ) − *v*

On the diagonal *u* = *v* = *x*: **x + xⁿ⁺¹ = a**. The Jacobian there is
[[−1, −g], [−g, −1]] with **g ≡ n xⁿ⁺¹/a**, so λ = −1 ± g by inspection and the
symmetric state loses stability exactly at g = 1. (Called β until 18 September;
renamed because Gardner's β is a cooperativity and both appear on the same day.) Solving g = 1 together with the
fixed-point equation:

**x<sub>c</sub> = (n−1)<sup>−1/n</sup>  ·  a<sub>c</sub> = n(n−1)<sup>−(n+1)/n</sup>**

| n | x<sub>c</sub> | a<sub>c</sub> |
|---|---|---|
| 1.2 | 3.824 | 22.94 |
| 1.8 | 1.132 | 2.547 |
| 2 | 1.000 | 2.000 |
| 3 | 0.794 | 1.191 |
| 4 | 0.760 | 1.013 |

Verified numerically 7 September: g = 1.0000 and *x* + *x*ⁿ⁺¹ = *a*<sub>c</sub> to
four figures at n = 2, 3, 4, 8.

**a<sub>c</sub> → ∞ as n → 1.** No cooperativity *on either arm*, no switch, at any
promoter strength. The handout proves the general form — the loop gain
g₁g₂ < β for γ = 1 — on Gardner's own device, which has γ = 1 and switches.

## Why this matters beyond session 8

[Session 4](../s04-modeling-ii/README.md) quotes this α<sub>c</sub> as a forward
reference in week 2, without proof. [Session 9](../../decks/s09_bistability.py)
uses it. **This is where it gets derived**, and that is what makes the phase
plane worth a whole period instead of a definitions slide. Say so in the room —
a promise kept three weeks later is worth more than the algebra.

## The misconception to kill

Rhythm 2 exists for it: **n = 2 is not a threshold.** The threshold is on *a*, and
*n* only sets where it is. Bistability needs n > 1, not n ≥ 2. A toggle with
n = 1.8 and a = 5 is bistable, comfortably.

## What the board keeps

The ledger, on the left wing, written once:

- the two toggle equations
- the two nullclines
- a = α/((γ+μ)K)
- J and λ = −1 ± g
- a<sub>c</sub>, boxed

Runs 3 and 4 both point back at the nullclines, and Rhythm 2 needs a<sub>c</sub>
an hour after it was derived. That parallel persistence is the one thing a deck
cannot do.

## Built

| | |
|---|---|
| Figures | 16 PNGs in `figures/build/s08_*` — the plane in five states, the crossings, the diagonal, the nudge in three states, the tangency, *a*<sub>c</sub>(*n*) in two states, the τ–Δ plane, Gardner Fig. 2c,d recomputed, pTAK117's nullclines |
| Handout | [s08-asymmetric-toggle](../../handouts/s08-asymmetric-toggle.md) — items 1–2 in the room, 3–4 on PS4; breaks the symmetry on Gardner's γ = 1 |
| Answer sheet | [items 1–2](../../handouts/s08-asymmetric-toggle-answers.md) |
| Board notes | [s08-board-notes](../../board-notes/s08-board-notes.md) — the ledger, the axes, two tallies |

## Open

- The generation opener: the 0–6 retrieval stands; a launch problem was never tried.
- Badges on the new surfaces are placeholders.
