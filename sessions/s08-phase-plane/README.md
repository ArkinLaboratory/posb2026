# Session 8 — The phase plane: nullclines, fixed points, linear stability

[← all sessions](../README.md) · **Tuesday, September 22, 2026**

> **SPINE ONLY, built 7 September.** The three derivation runs, the payoff run
> and the frame are done and verified. Still missing: figures, the generation
> opener, the faded handout and its answer sheet, and board notes for the
> ledger. Built two weeks early on purpose — see below.

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
| 6–9 | Goals as questions | The third one gets an exact answer today |
| 9–19 | **Run 1**, four steps | Nullclines are curves; fixed points are their intersections |
| 19–25 | **Rhythm 1** | How many times can two decreasing curves cross? *(B — one or three)* |
| 25–35 | **Run 2**, four steps | Substitute, collapse onto the diagonal, get *x* + *x*ⁿ⁺¹ = *a* |
| 35–47 | **Run 3**, five steps | Linearise → Jacobian → λ = −1 ± β → stable iff β < 1 |
| 47–55 | **Run 4 — the payoff**, five steps | *a*<sub>c</sub> = *n*(*n*−1)<sup>−(n+1)/n</sup>, derived |
| 55–60 | Classification reference | τ, Δ, and the toggle read off it |
| 60–68 | **Rhythm 2** | *n* = 1.8, *a* = 5. Is it a switch? *(A — yes; a<sub>c</sub> = 2.55)* |
| 68–80 | Faded set, then Gardner assigned | ⬜ handout not written |

## The result this session exists to produce

The symmetric toggle, which is also Thursday's reading:

d*u*/d*t* = *a*/(1+*v*ⁿ) − *u*  ·  d*v*/d*t* = *a*/(1+*u*ⁿ) − *v*

On the diagonal *u* = *v* = *x*: **x + xⁿ⁺¹ = a**. The Jacobian there is
[[−1, −β], [−β, −1]] with **β ≡ n xⁿ⁺¹/a**, so λ = −1 ± β by inspection and the
symmetric state loses stability exactly at β = 1. Solving β = 1 together with the
fixed-point equation:

**x<sub>c</sub> = (n−1)<sup>−1/n</sup>  ·  a<sub>c</sub> = n(n−1)<sup>−(n+1)/n</sup>**

| n | x<sub>c</sub> | a<sub>c</sub> |
|---|---|---|
| 1.2 | 3.824 | 22.94 |
| 1.8 | 1.132 | 2.547 |
| 2 | 1.000 | 2.000 |
| 3 | 0.794 | 1.191 |
| 4 | 0.760 | 1.013 |

Verified numerically 7 September: β = 1.0000 and *x* + *x*ⁿ⁺¹ = *a*<sub>c</sub> to
four figures at n = 2, 3, 4, 8.

**a<sub>c</sub> → ∞ as n → 1.** No cooperativity, no switch, at any promoter
strength. That is a hard design constraint, derived rather than asserted.

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
- J and λ = −1 ± β

Runs 3 and 4 both point back at the nullclines, and Rhythm 2 needs a<sub>c</sub>
an hour after it was derived. That parallel persistence is the one thing a deck
cannot do.

## Still to build

| | |
|---|---|
| Figures | nullclines with one and three crossings; trace–determinant chart; the toggle's three fixed points with the separatrix |
| Generation opener | the 0–6 retrieval is written; a launch problem may be better |
| Faded handout | **must break the symmetry** — two different Hill coefficients. Everything derived here used u ↔ v symmetry to get onto the diagonal, and a student who only sees the symmetric case will think the diagonal is the method rather than a convenience |
| Answer sheet | items done in the room only |
| Board notes | the ledger and the responses, not a derivation |
