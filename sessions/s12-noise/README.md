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
| 22–23 · Potvin-Trottier | rebuilt as this session's bridge, in three surfaces |

Dropped: S11's slide 21 (their Fig. 1b, beyond the one sentence) and the
ConcepTest.

## The movies

The bridge opens with two of the seven supplementary movies from the published
Nature paper, side by side: **Movie 2**, Elowitz & Leibler's original
repressilator (NDL332), oscillating and losing the beat; and **Movie 6**, the
finished triple-reporter circuit (LPT117), cycling red → green → blue for
generation after generation. Ten seconds of each, with nothing said over them,
is the session's thesis.

⚠ The PDF in `private/readings/` is the PMC author manuscript and cites exactly
one video ("S Video 1", the flask culture). The other six exist only on the
published Nature page. All seven are catalogued, with download URLs, in
`decks/paper_movies.yaml`; the two in use are in `private/paper-movies/`
(gitignored). Absent, the build draws a labelled slot and Fig. 1d on the next
surface still carries the contrast.

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
TetR–EGFP repressing itself: Vc 6–9% with feedback (p. 591), about threefold
higher without at equal mean (p. 592). One of their two equal-mean controls was
sampled during a transient; the other (chromosomal TetR) was not, and it still
shows the threefold.

Their **Vc is σ/mean** — our η, in percent (Methods, p. 594) — and their
**"stability" S is the linearisation about the steady state** (p. 590), which
is our return rate r. So their "twofold increase in stability" is
γ(1 + g) = 2γ, i.e. **g = 1 for their circuit**, and our result predicts the CV
falling by √2 = 1.41, with slow extrinsic buffering worth at most another factor
making 1 + g = 2. The measured gap is about 3. **Our model does not account for
it**, and the deck says so rather than reaching for a factor; bursts, plasmid
copy-number compensation and imperfectly matched controls are the candidates.

⚠ Corrected 5 October: an earlier build assumed g ≈ 2 here and quoted √3 ≈ 1.7.
Their own stated twofold fixes g at 1, and 1.7 was never consistent with it.

## What happens

| | | |
|---|---|---|
| 0–5 | **Retrieval** | g and why α drops out; the odd ring; why NAR is faster (S7) |
| 5–7 | Goals as questions | two copies disagree; the smallest noise; a quieter reporter |
| 7–14 | **Thursday, finished** | the sweep (PS5 Q5a); the n ≤ 2 wall; delay (T30) |
| 14–17 | The bridge, 1 | the two movies: the original circuit, then the repaired one |
| | | the four repairs, each with its mechanism |
| 17–20 | The bridge, 2 | **why** the fourth worked: a relaxation oscillator's period is a decay time |
| 20–23 | **The artifact** | Elowitz 2002: the construct, and what Fig. 3A plots |
| 23–29 | **Argue**, groups | what moves both colors; along A or across B; repress 30-fold |
| 29–31 | The vocabulary, T33 | σ, η and Fano off one histogram, before any of them is used |
| 31–33 | Sorted, T34 | their A and B are extrinsic and intrinsic; Table 1 |
| 33–35 | **Run** | why the two add as squares, and why the larger one wins |
| 35–37 | The object | a count, a rate as a chance, no schedule |
| 37–42 | **Run**, T31a | build it: master equation → flux J → steady state makes every J equal |
| 42–47 | **Run**, T31b | solve it: J₀ = 0 → recursion → climb → normalise → η² = 1/⟨n⟩ |
| 47–50 | **Run**, T35 | two stages; where b comes from; the mean is blind, the variance is not |
| 50–54 | **Run**, T32 | why the wait is exponential, then the two draws |
| 54–57 | **Live code** | twenty lines; the time-weighting trap |
| 57–65 | **Run**, T17 | why we must borrow; what a return rate is; calibrate; Fano = 1/(1+g) |
| 65–69 | The measurement | the four Becskei constructs drawn, then their S = our r |
| 69–74 | **ConcepTest** | right mean, too noisy *(A and D)* |
| 74–79 | **Faded set** | [four problems](../../handouts/s12-noise.md) |
| 79–80 | Forward link | Hooshangi for Thursday; Daniel optional / 247 |

## The results this session exists to produce

**Birth–death (T31), in two runs of seven and five steps.** The flux across rung
*n* is J_n = kP_{n−1} − γnP_n, and dP_n/dt = J_n − J_{n+1}. At steady state every
J is equal and J₀ = 0, so every J is zero, which gives
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
| Figures | `s12_ssa_anatomy(_col)`, `s12_birth_death`, `s12_bd_traj`, `s12_bd_hist`, `s12_bursting`, `s12_burst_traj`, `s12_burst_hist`, `s12_nar_noise`, `s12_nar_hist`, `s12_nar_fano`, `s12_two_color`, `s12_scatter_axes`, `s12_noise_vocab`, `s12_squares_ext/int/both`, `s12_becskei_circuits` |
| Deck | `decks/s12_noise.py`, 57 slides incl. six derivation runs |
| Handout | [s12-noise](../../handouts/s12-noise.md) + [answers](../../handouts/s12-noise-answers.md) |
| Board notes | [s12](../../board-notes/s12-board-notes.md), with the live code |

## Paper figures

`elowitz2002_fig3a`, `becskei2000_fig3a` (new, cropped 4 Oct) and
`potvintrottier2016_fig1d` (from S11). Boxes and provenance in
`decks/paper_figures.yaml`.

## Open

- The pacing report puts student working time at 24%, below the course's usual
  28–46%. The carried S11 material is the cause; nothing has been relabelled to
  move the number. The 5 October rebuild paid for its two new surfaces out of
  exposition (one minute each off goals, delay and live code), so this number is
  unchanged by it.
- The notebook and its ungraded self-checking exercise ship Thursday 8 Oct.
