# Session 13 — The digital abstraction, and its price

[← all sessions](../README.md) · **Thursday, October 8, 2026**

> The last content session before review and the midterm. It earns the word
> "digital" rather than assuming it: what must be true of a measured transfer
> curve before a gene may be called a switch, how you check with numbers that
> two gates can be wired together, and what the abstraction costs.

## The one thing to remember

> **A gate is only digital at its two ends. The cooperativity that buys it a
> restoring region and a matching window is the same cooperativity that
> destroys its range as a measuring instrument — 9^(1/n)-fold, and no more.**

## The artifacts

**Hooshangi, Thiberge & Weiss, *PNAS* 2005** (required, free on PMC, assigned
6 October). Three cascades one, two and three repressors deep, all on one
plasmid each. Hill coefficients 2.3, 7.0, 7.5; transition widths 1.75, 0.36,
0.21 µM aTc (p. 3583). Their Fig. 2B is the noise cost, Fig. 3A the delay.

**Nielsen et al., *Science* 2016 — Cello** (S16's reading; used here for one
figure). Fig. 2B shows PhlF driving BetI connecting, and the reverse failing.
Their **Table S4** gives every insulated gate's fitted y_min, y_max, K and n in
RPU, which makes the signal-matching example use measured gates rather than
invented ones.

**Daniel, Rubens, Sarpeshkar & Lu, *Nature* 2013** (optional for 147, the 247
companion). The positive-feedback-plus-shunt circuit that stays logarithmic over
three to four decades, and the same circuit made digital-like by raising one
plasmid's copy number (Fig. 2e).

## What happens

| | | |
|---|---|---|
| 0–5 | **Retrieval** | η at 25 molecules; what feedback changed; n = 1 on the toggle |
| 5–8 | Goals as questions | when is it a switch; does B read A; what does the switch discard |
| 8–15 | **The artifact** | the three cascades; 2.3 → 7.0 → 7.5, and the third stage's seven per cent |
| 15–23 | **Argue**, groups | why stacking sharpens; where it stops; why stage three failed to |
| 23–26 | Sorted | gains multiply where the stages overlap: peak 1.64 → 2.35, or 0.06 if misaligned |
| 26–38 | **Run**, T36–T37 | the curve → log slope → g → n > 1 → the leak → two thresholds → four numbers |
| 38–44 | **Signal matching**, T38 | the margin test; the identical-gate pair fails; the RBS window |
| 44–50 | **Two real gates** | Nielsen Fig. 2B, then their Table S4 numbers and our margins |
| 50–56 | **The price** | noise amplified in the transition; delay and lost synchrony; the low-pass payback |
| 56–60 | The alternative | a switch discards the middle; Hill is log-linear over 9^(1/n)-fold |
| 60–68 | **Run**, the analog half | feedback, then a shunt; ln(1+x) over three decades; digital again at high copy |
| 68–73 | **ConcepTest** | NM_L +0.70, NM_H −0.30: which fixes it *(A and C)* |
| 73–79 | **Faded set** | [four problems](../../handouts/s13-digital.md) |
| 79–80 | Forward link | review Tuesday, midterm Thursday; PS5 and M1 due tonight |

## The results this session exists to produce

**Gain, and why it is a log slope (T36).** G = d ln y/d ln x, because input and
output are different molecules and a linear slope depends on the units chosen.
For the leaky Hill repressor |G| = g (y − y_min)/y with g = n uⁿ/(1 + uⁿ) — the
session 11 loop gain, discounted by the leak. Two consequences: |G| can exceed 1
only if n > 1, and the leak is what pulls it back down at high input, so a
threshold exists at all.

**Thresholds and levels (T37).** When the peak |G| clears 1 — which needs n > 1
*and* a swing large enough that the leak does not hold the peak down — |G| = 1
has two solutions, x_IL and x_IH, and they name y_OH = y(x_IL) and
y_OL = y(x_IH). For K = 1, n = 2, hundredfold swing: **1.02, 9.80, 4.95, 0.20**.
At n = 3: 0.80, 5.80, 6.65, 0.15. Thresholds scale with K; output levels do not.
The method is grid, peak, bisect — on the handout and in the board notes,
because nothing else demonstrates it.

**Signal matching (T38).** NM_L = log(x_IL(B)/y_OL(A)), NM_H = log(y_OH(A)/x_IH(B)).
The n = 2 gate driving an identical copy gives **+0.70 and −0.30**: it fails. An
RBS scales both of a gate's outputs and neither of its thresholds, because
(y − y_min)/y is scale-free, so the window of working RBS factors is
**×2.0 to ×5.1** (2.55-fold) at n = 2 and ×0.55 to ×5.7 (10.3-fold) at n = 4.

⚠ That two-knob picture is true of this model, where the output is a reporter
with its own RBS. In a repressor chain the output protein *is* the next gate's
repressor, so one RBS sets both — Nielsen's supplement §I.C reports thresholds
shifting when they changed it. The deck, the board notes and the answer sheet
all carry the caveat.

**Nielsen's two gates, from their Table S4.** PhlF P1 (0.01, 3.9, 0.03, 4.0) →
BetI E1 (0.07, 3.8, 0.41, 2.4): **+1.44 and +0.08**, connects. Reversed:
**−0.73 and +1.10**, fails on the low side, because BetI's leak of 0.12 RPU sits
above PhlF's x_IL of 0.023. Those agree with the tick and the cross in their
figure, though their own rule is different from ours — they ask that the
sender's output range span the receiver's threshold. Two of their twenty gates
(AmeR F1 and IcaRA I1, both n = 1.4 with a large leak) never reach |G| = 1 at
all, so this session's criterion says they cannot restore a signal and Cello
uses them anyway. The deck says so.

**The price, and the thesis.** The log-linear range of a Hill curve, holding the
slope within 75% of its peak, is **9^(1/n)-fold**: ninefold at n = 1, threefold
at n = 2, 1.7-fold at n = 4. Set against the matching window, which grows with
n, that is the session's sentence: the same cooperativity is in both bills with
opposite signs.

**ConcepTest numbers**, computed on the session's own gate: A (sender RBS ×3)
+0.23 / +0.18, works. B (receiver RBS ×3) +0.70 / −0.30, **unchanged** — the
trap. C (receiver n = 4) +0.58 / +0.08, works. D (a third identical gate)
inherits the mismatch and inverts the logic as well.

## Coverage

T36, T37, T38, all assessed on **PS6** (posts 20 Oct). On the midterm, S12 and
S13 are recognition-only — stated on the forward-link slide and in the scope
handout.

## New in `posb` — `posb.digital`

`Repressor` (call it, `.gain`, `.thresholds`, `.output_levels`, `.scaled`),
`noise_margins`, `rbs_window`, `loglinear_range_hill`. Seven tests. The handout
works item 1 in full, including how the two roots are found, before any of it is
imported.

## Built

| | |
|---|---|
| Figures | `s13_gain_p1..p4`, `s13_self_match`, `s13_rbs_window`, `s13_cascade`, `s13_loglin_p1..p2` |
| Deck | `decks/s13_digital.py`, 30 slides, two derivation runs |
| Handout | [s13-digital](../../handouts/s13-digital.md) (4 pp) + [answers](../../handouts/s13-digital-answers.md) (2 pp) |
| Board notes | [s13](../../board-notes/s13-board-notes.md) |

## Paper figures

`hooshangi2005_fig1`, `fig2a`, `fig2b`, `fig3a`; `daniel2013_fig1d`,
`fig2e`; `nielsen2016_fig2b`. All are declared crops of tracked parents in
`decks/paper_figures.yaml`.

## Open

- Student working time reads 27%, just under the course's usual 28–46%. Nothing
  was relabeled to move it.
- The 15–23 min block is three open prompts to groups of 3–4, which is the shape
  AGENTS.md warns about ("use individual written work, collected"). It is kept
  because each prompt has a definite answer the next surface resolves, but it is
  the first thing to reshape if the room drifts.
- The notebook and its ungraded self-checking signal-matching exercise ship with
  S12's, after class.
