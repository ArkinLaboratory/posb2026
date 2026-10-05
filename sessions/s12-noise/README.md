# Session 12 — Noise and the master equation

[← all sessions](../README.md) · **Tuesday, October 6, 2026**

> Thursday's model runs identically every time. No cell does. This session
> builds the model that counts molecules, finds the smallest noise an
> unregulated gene can have, and shows what a circuit can do about it.

## The one thing to remember

> **At tens of molecules an unregulated gene cannot do better than
> η² = 1/⟨n⟩, and no choice of part changes that. Bursts make it worse;
> negative feedback divides the Fano factor by 1 + g — Thursday's g — because it
> shortens each fluctuation, not because it makes fewer.**

## Thursday's leftovers come first

Session 11 stopped at its slide 18. Carried here, by Adam's decision of 4 October:

| from S11 | why it cannot wait |
|---|---|
| 19 · the sweep, step by step | the demonstration of T29; PS5 Q5a–b is due Thursday 8 Oct |
| 20 · the wall at n ≤ 2 | with one sentence from 21: Elowitz & Leibler's n = 2 oscillates because they kept mRNA |
| 25 · delay | T30; PS5 Q6, and the midterm item committed on 26 September |
| 22–23 · Potvin-Trottier | compressed to one surface, and it becomes this session's bridge |

Dropped: S11's slide 21 (their Fig. 1b, beyond the one sentence) and the
ConcepTest.

## The artifact

**Elowitz, Levine, Siggia & Swain, *Science* 2002**: two copies of one promoter
in the *E. coli* chromosome, one driving CFP and one YFP, at loci equidistant
from the origin. Spread across the diagonal of Fig. 3A is intrinsic noise; spread
along it is extrinsic. Assigned at the end of S11, but S11 did not reach its
assignment slide, so this session says what it is.

⚠ The reading guide originally pointed at Fig. 2 (micrographs). Corrected to
Fig. 3A and Table 1 on 4 October. The estimator algebra is in their supplement
and in Swain, Elowitz & Siggia, PNAS 2002, not in this paper.

**The measurement for T17: Becskei & Serrano, *Nature* 2000.** Not assigned.
TetR–EGFP repressing itself: Vc 6–9% with feedback, about threefold higher
without at equal mean (p. 592). One of their two equal-mean controls was sampled
during a transient; the other (chromosomal TetR) was not, and it still shows the
threefold. That is more than our protein-only result allows (√(1+g) in CV,
about 1.7 at g ≈ 2). Buffering of slow extrinsic change, which feedback cuts by
1 + g in CV, is the likeliest reason, and the deck says that inference is ours.

## What happens

| | | |
|---|---|---|
| 0–5 | **Retrieval** | g and why α drops out; the odd ring; why NAR is faster (S7) |
| 5–8 | Goals as questions | two copies disagree; the smallest noise; a quieter reporter |
| 8–17 | **Thursday, finished** | the sweep (PS5 Q5a); the n ≤ 2 wall; delay (T30) |
| 17–21 | The bridge | Potvin-Trottier: every fix acted on the last few molecules |
| 21–25 | **The artifact** | Elowitz 2002, Fig. 3A |
| 25–31 | **Argue**, groups | what moves both colours; which way on the plot; repress 30-fold |
| 31–34 | Sorted, T34 | intrinsic and extrinsic; Table 1; they add as squares |
| 34–36 | The object | a count, a rate as a chance, no schedule |
| 36–46 | **Run**, T31 | master equation → flux → J₀ = 0 → Poisson → η² = 1/⟨n⟩ |
| 46–49 | Bursting, T35 | same mean, two RBSs; Fano ≈ 1 + b (stated, checked) |
| 49–53 | **Run**, T32 | the two draws: when, then which |
| 53–58 | **Live code** | fifteen lines; the time-weighting trap |
| 58–66 | **Run**, T17 | calibrate the rule; same noise in; faster return; Fano = 1/(1+g) |
| 66–69 | The measurement | Becskei & Serrano Fig. 3a, and its fine print |
| 69–74 | **ConcepTest** | right mean, too noisy *(A and D)* |
| 74–79 | **Faded set** | [four problems](../../handouts/s12-noise.md) |
| 79–80 | Forward link | Hooshangi for Thursday; Daniel optional / 247 |

## The results this session exists to produce

**Birth–death (T31).** The flux across rung *n* is J_n = kP_{n−1} − γnP_n. At
steady state every J is equal and J₀ = 0, so every J is zero, which gives
P_n = P₀(k/γ)ⁿ/n!, a Poisson: ⟨n⟩ = σ² = k/γ, Fano = 1, η² = 1/⟨n⟩. Simulated
at k = 10: mean 9.96, variance 9.92.

**Bursting (T35).** Fano = 1 + k_p/(γ_m + γ_p) ≈ 1 + b. Stated, not derived
(Thattai & van Oudenaarden 2001); checked: simulated 1.9 and 10.3 against exact
1.91 and 10.09 at mean 50.

**Negative autoregulation at matched mean (T17).** Calibrate
σ² = (noise in)/(2 × return rate) on the constitutive case, where it returns the
Poisson. With feedback the noise in is unchanged (2γx) and the return rate is
γ(1 + g), with g = n uⁿ/(1 + uⁿ), the S11 loop gain. So **Fano = 1/(1 + g)**.
Gillespie at x = K: 0.666, 0.494, 0.334, 0.204 for n = 1, 2, 4, 8 against 0.667,
0.5, 0.333, 0.2. Verified in `tests/test_stochastic.py`.

**ConcepTest numbers** (mean 50, from b = 10, Fano 9.7): halve RBS 5.5; double RBS
worse (exact 19.2); two half-strength copies 10.0, unchanged; NAR n = 2 retuned 5.3,
n = 4 4.0.

## Coverage

T31, T32, T33, T34, T35 and T17, all assessed on **PS6** (posts 20 Oct). On the
midterm, S12 is recognition-only. Carried from S11: T29, T30.

## New in `posb` — `posb.stochastic`

`gillespie`, `time_average`, `fano`, `cv`, `birth_death`, `two_stage`,
`negative_autoregulation`, `two_stage_fano`, `nar_fano_lna`. Seven tests.
Students write their own SSA in the notebook (ships Thursday 8 Oct) before they
import ours.

## Built

| | |
|---|---|
| Figures | `s12_ssa_anatomy(_col)`, `s12_birth_death`, `s12_bd_traj`, `s12_bd_hist`, `s12_bursting`, `s12_nar_noise`, `s12_nar_hist`, `s12_nar_fano`, `s12_two_color` |
| Deck | `decks/s12_noise.py`, 35 slides incl. three derivation runs |
| Handout | [s12-noise](../../handouts/s12-noise.md) + [answers](../../handouts/s12-noise-answers.md) |
| Board notes | [s12](../../board-notes/s12-board-notes.md), with the live code |

## Paper figures

`elowitz2002_fig3a`, `becskei2000_fig3a` (new, cropped 4 Oct) and
`potvintrottier2016_fig1d` (from S11). Boxes and provenance in
`decks/paper_figures.yaml`.

## Open

- The pacing report puts student working time at 24%, below the course's usual
  28–46%. The carried S11 material is the cause; nothing has been relabelled to
  move the number.
- The notebook and its ungraded self-checking exercise ship Thursday 8 Oct.
