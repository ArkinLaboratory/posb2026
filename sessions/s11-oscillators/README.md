# Session 11 — Oscillators

[← all sessions](../README.md) · **Thursday, October 1, 2026**

> The toggle held a state. The feedforward loop timed one event. This one runs
> forever — or fails to, and one inequality decides which.
> `docs/design-notes.md` records the oscillation criterion as never having been
> stated at all in prior years. That gap is why this session exists.

## The one thing to remember

> **A clock is a steady state that failed, and it failed in a particular way:
> a complex pair of eigenvalues crossing together.**

## The artifact this is built on

Elowitz & Leibler, *Nature* 2000 — the repressilator. Three repressors in a ring
on one plasmid, GFP on a second. It oscillated with a period near 150 min, longer
than the cell cycle, and it kept terrible time. It is **not** an assigned reading
(paywalled, no deposit anywhere), so it lives on the slide as the construct.

The assigned reading, handed out at session 10 and discussed here, is
**Potvin-Trottier et al., *Nature* 2016** — the same circuit with its noise
sources removed one at a time. That pairing is the session's second argument:
the criterion tells you *whether* it ticks and has nothing to say about *how
well*, and the reading is the evidence for that claim.

## What happens

| | | |
|---|---|---|
| 0–5 | **Retrieval**, notes closed | FFL sign rule; why a C1 rejects a flicker; what went wrong at n = 1 on the toggle |
| 5–8 | Goals as questions | Why should three in a ring give no stable state? What do you check? What was destroying the period? |
| 8–13 | **The artifact** | Elowitz Fig. 1 and Fig. 2 — the ring, and traces that wander |
| 13–23 | **Argue**, groups | Chase the logic round the loop; odd vs even; what would have to be true for a middling state to hold |
| 23–27 | Sorted | Odd ring = net negative feedback · the symmetric state always exists · so the question is stability |
| 27–40 | **Run**, the criterion | α = x(1+xⁿ) → J = −I − gP → cube roots of unity → Re λ = −1 + g/2 → **g = 2** |
| 40–44 | The period | λ = ±i√3 at onset, so **T = 2π/√3 ≈ 3.63 lifetimes**; where that stops being true |
| 44–50 | **T29 numerically** | Sweep α, watch max Re λ cross, bisect. 3.780 against 3.780 |
| 50–54 | The design space | α_c(n), the wall at n ≤ 2, and the comparison to the toggle's n > 1 |
| 50–54 | **Their own boundary** | Elowitz Fig. 1b — the same design space, on axes we scaled away, with their construct marked inside it |
| 54–62 | **The reading** | Potvin-Trottier: four modifications, none of which changes g. What our model cannot see |
| 62–67 | **ConcepTest** | Longer period? *(A and C both — and why B is the trap)* |
| 67–71 | Delay (T30) | The ring's real trick was delay; negative feedback plus delay oscillates without a ring |
| 71–78 | **Faded set** | [Four problems](../../handouts/s11-oscillators.md): n = 3 worked, n = 4, a ring of five, and one design |
| 78–80 | Forward link | Every run of our model is identical; no cell is. Session 12 |

## The results this session exists to produce

**The criterion (T28).** At the symmetric fixed point the Jacobian is
**J = −I − gP** with **g = n xⁿ/(1 + xⁿ)**, and P's eigenvalues are the cube
roots of unity, so λ_k = −1 − g ω_k. The complex pair has real part −1 + g/2, so
the state loses stability exactly when

**g = 2**, giving **α_c = [2/(n−2)]^(1/n) · n/(n−2)**, infinite for n ≤ 2.

At n = 4, α_c = 2 exactly. Verified against numerical bisection to ~1e-9 for
n = 2.5, 3, 4, 5, 8 in `tests/test_analysis.py`.

**The period at onset.** g = 2 makes the pair ±i√3, so **T = 2π/√3 ≈ 3.63
protein lifetimes** — measured 3.64 just above the boundary, drifting to 5.2 at
3×α_c and 8.0 at 10×α_c. The linear result is a local one and the slide says so.

**The general ring (handout item 3).** Re λ_k = −1 − g cos(2πk/N), so the
criterion is g > 1/max_k(−cos(2πk/N)): **2 for N = 3, 1.236 for N = 5, 1.110 for
N = 7**. For even N the worst root is ω = −1, which is *real* — so an even ring
goes bistable rather than oscillating. That is the algebraic form of the room's
odd/even argument.

## Coverage

T27 (construct the model), T28 (state and apply the criterion), T29 (locate the
Hopf boundary numerically by sweep), T30 (delay as a driver of oscillation).
All four assessed on **PS5**, out today, due Thursday 8 October.

## New in `posb` — the week's public surface

`repressilator_model`, `loop_gain`, `repressilator_alpha_critical`, `sweep`,
`leading_real_part`, `hopf_boundary`. Eight new tests; the suite is 32 passing.
The governing rule holds: **students write the sweep on PS5 before they import
ours.**

## Built

| | |
|---|---|
| Figures | `s11_ring_dynamics`, `s11_crit_p1..p5` (the eigenvalue reveal), `s11_sweep`, `s11_alpha_critical` |
| Deck | `decks/s11_oscillators.py` — 19 slides |
| Handout | [s11-oscillators](../../handouts/s11-oscillators.md) (4 pp) + [answers](../../handouts/s11-oscillators-answers.md) (2 pp) |

## Paper figures — all present

`elowitz2000_fig1` (panel a, the two plasmids), `elowitz2000_fig1b` (their
stability diagram), `elowitz2000_fig2`, `potvintrottier2016_fig1d` and
`potvintrottier2016_fig3a` are all cropped into `private/paper-figures/` with
their boxes and provenance recorded in `decks/paper_figures.yaml`. The deck
reports *all paper figures embedded*.

⚠ **Two of these were originally described wrongly** and were corrected on
26 September against the PDF. Potvin-Trottier's Fig. 1 is *reducing reporter
interference*, not "the four modifications"; Fig. 3 is *robustness to growth
conditions*, not "period variability". The slide now uses **Fig. 1d** — a
single cell losing its reporter plasmid and starting to keep time — and
**Fig. 3a**, the 14-generation period across temperatures and media.

## Open

- **Elowitz 2002 goes out at the end of this session.** Adam supplied the PDF on
  26 September; it is `private/readings/Session 12 - elowitz-2002-stochastic-gene-expression-in-a-single-cell.pdf`.
  It still has no free public copy, so students reach it through the library
  proxy — say that out loud when the assignment slide goes up.
- Badges are placeholders; the run sheet is Adam's.
