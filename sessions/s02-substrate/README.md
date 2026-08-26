# Session 2 — The cell as a physical substrate

[← all sessions](../README.md) · **Tuesday, September 1, 2026**

No notebook — this is board work and paper. The computing starts Thursday in
[Session 3](../s03-modeling-i/). **PS0 is due today.**

## The one thing to remember

> **1 nM is about one molecule per *E. coli*.**

Everything else in the session is that number times something, or that number
squared.

## What happens

**89 minutes** — 8:00–9:29.

| | | |
|---|---|---|
| 0–5 | **Retrieval**, notes closed | The three questions session 1 ended on. Write the room's guesses on the board and leave them there. |
| 5–8 | Map + goals as questions | |
| 8–11 | Setting the scale | One femtolitre — and 10³⁰ of them on Earth |
| 11–15 | The one number | 1 nM ≈ 1 molecule. Arithmetic at the board. [figure](../../figures/build/s02_copy_number.png) |
| 15–18 | **ConcepTest 1** | A transcription factor at 100 pM — what is true of the individual cells? |
| 18–22 | Crowding | 70% water, 20% protein, and $D$ 11× lower than water — measured |
| 22–25 | **Demo 2** — what one $D$ hides | [`demos/d02-crowding/`](../../demos/d02-crowding/) · predict-first, twice |
| 25–28 | **ConcepTest 2** | The same protein in a HeLa cell. 20× or 400×? |
| 28–32 | Nine orders of magnitude | [figure](../../figures/build/s02_timescales.png) |
| 32–35 | Which pairs can you treat as instantaneous? | The QSSA, informally, two sessions early |
| 35–37 | Nothing outruns division | Growth is a removal term whether or not you wrote one |
| 37–39 | **The pause** | Two minutes. Say nothing. |
| 39–63 | **Faded worked set** | Four estimates. [PDF](../../handouts/s02-faded-estimates.pdf) · [source](../../handouts/s02-faded-estimates.md) |
| 63–67 | What the numbers force — counting | Noise is unavoidable; an average is not a cell |
| 67–70 | — slowness and size | Growth caps circuit speed; geometry changes the answer |
| 70–74 | How to be wrong by less than 10× | The transferable part |
| 74–77 | Item 4 — your estimate was wrong | And being wrong is the result |
| 77–83 | **Consolidation + retrieval**, in writing | The three questions again — then look at the board |
| 83–86 | Forward link | To d**x**/d*t* = **S**·**v** |
| 86–89 | Slack | First working session; it will run long |

**Twenty slides.** 43 minutes of exposition over 13 slides — about 3.3
min/slide — and **43 of 89 minutes (48%) given to the students.**

An earlier draft did the same 43 minutes on *seven* slides, 6.1 min/slide.
That is not a short lecture, it is an improvised one, and it is invisible in the
source. `tools/build_decks.py` now measures minutes-of-exposition per slide for
every segment and flags anything past 4.5.

## Why a faded set and not a launch problem

Session 1 opened with a launch problem; this one does not. Per
[Lecture Design §2](../../docs/lecture-design.md): *generation for concepts,
faded worked examples for procedures.* Estimating a copy number is a procedure.
Asking students to invent it is not productive failure, it is twenty minutes
spent rediscovering that you multiply by Avogadro's number.

Item 4 — a repressor finding one site in 4.6 Mb — is meant to come out **wrong**.
A plain three-dimensional search predicts hours; the measured association is
minutes. The estimate is not wrong by arithmetic, it is wrong because the
mechanism is not what the problem said: the protein slides along the DNA in one
dimension between three-dimensional hops. That is the best advertisement for
estimating anyone has: *an estimate that disagrees with a measurement is how you
find a mechanism you were not looking for.*

## The demo

[**Demo 2 — Crowding**](../../demos/d02-crowding/) runs at minute 22 and takes
a prediction before each of its two cells.

1. *A ribosome is four times bigger than GFP, so how much slower does it cross
   the cell?* The room says four. It is **thirty-five** — because effective
   viscosity is not a property of the cytoplasm but of the cytoplasm *and the
   probe*: ~100 cP for a ribosome-sized particle against ~12 cP for GFP.
2. *This is a plain random walk — ordinary diffusion at every step. What
   exponent will it show once I put a wall on it?* The room says one. It is
   **0.75**, which is exactly what the 2025 tracking measurements report for
   large particles.

Both come from [Valverde-Mendez et al., *PNAS* **122**(4), e2406340121
(2025)](https://doi.org/10.1073/pnas.2406340121), and the demo reproduces them
from scratch in about thirty lines.

**The methodological point is deliberately not laboured here.** Item 4 of the
faded set carries "the estimate was wrong and that is the result"; saying it
twice in eighty-nine minutes turns it into a slogan. The paper's job in this
session is to make the crowding claim visual and quantitative.

Worth one sentence in the room, though: *nobody needed anomalous-diffusion
theory to explain an anomalous-looking exponent.* When a measurement looks
exotic, check whether something boring and geometric produces the same
signature first.

## Coverage

Demonstrates **T1** (molecule counts from concentration and volume), **T2**
(diffusion timescale $t \sim L^2/2D$), **T3** (comparing process timescales) —
all three assessed in **PS1**, out Thursday. This is the first session where
"nothing is assessed that was not demonstrated" has to hold, and it does: the
faded set *is* the PS1 technique. See the
[Coverage Matrix](../../docs/coverage-matrix.md).

## Numbers, and where they come from

| | | |
|---|---|---|
| $D_{\text{GFP}}$ in *E. coli* cytoplasm | 7.7 ± 2.5 µm²/s | [Elowitz, Surette, Wolf, Stock & Leibler, *J. Bacteriol.* **181**:197–203 (1999)](https://journals.asm.org/doi/10.1128/jb.181.1.197-203.1999) |
| ~11× slower than in water | | same paper — the factor **is** the crowding |
| Cell volume | 1 fL | standard round number |
| Effective viscosity, ribosome-sized probe | ~100 cP (vs ~12 for GFP) | [Valverde-Mendez et al., *PNAS* **122**(4) e2406340121 (2025)](https://doi.org/10.1073/pnas.2406340121) |
| Apparent MSD exponent | α ≈ 0.75 large, 0.45 at 20 nm — from confinement, not the medium | same paper |
| Mutation rate | ~1 × 10⁻³ per genome per generation | [Lee, Popodi, Tang & Foster, *PNAS* **109**:E2774 (2012)](https://doi.org/10.1073/pnas.1210309109) |

Every constant used by the figures is defined once, with its source, at the top
of [`figures/s02_substrate.py`](../../figures/s02_substrate.py).

### One correction to the 2025 deck

The 2025 "Some numbers to contemplate" slide gives the mutation rate as
**10⁻⁷ per bp per generation**. The whole-genome-sequencing measurement is
~1 × 10⁻³ per *genome* per generation, which over 4.6 Mb is ~2 × 10⁻¹⁰ per bp —
about three orders of magnitude lower. The 10⁻⁷ figure is very close to the rate
**per gene** (≈10³ bp × 2 × 10⁻¹⁰ ≈ 2 × 10⁻⁷), so the number is probably right
and the *units* wrong. Worth fixing either way, because session 23 computes
time-to-circuit-failure from it and a factor of 10³ there is not survivable.

## Reading

**None.** PS0 is due today; PS1 goes out Thursday.
