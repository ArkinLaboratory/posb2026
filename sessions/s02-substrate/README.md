# Session 2 — The cell as a physical substrate

[← all sessions](../README.md) · **Tuesday, September 1, 2026**

No notebook — this is board work and paper. The computing starts Thursday in
[Session 3](../s03-modeling-i/). **PS0 is due tomorrow, Wednesday 2 September** —
and the discussion hour straight after this class, in Dwinelle 88, is where it
gets fixed for anyone it is fighting.

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
| 39–63 | **Faded worked set** — *two blocks, not one* | Items 1–3, ~8 min · **stop, take the numbers** · then item 4, ~5 min, *set it up, do not finish it*. [PDF](../../handouts/s02-faded-estimates.pdf) · [source](../../handouts/s02-faded-estimates.md) |
| 63–67 | **The answers** — items 1, 2, 3 | The numbers, and the *sign* of the assumption under each |
| 67–71 | What the numbers force — counting | Noise is unavoidable; an average is not a cell |
| 71–74 | — slowness and size | Growth caps circuit speed; geometry changes the answer |
| 74–77 | How to be wrong by less than 10× | The transferable part |
| 77–81 | **Item 4** — both estimates were wrong | Two routes, opposite errors, one mechanism |
| 81–83 | **The third exponent** — *optional; the designated cut* | Why sliding alone would be worse: N², not N |
| 83–87 | **Consolidation + retrieval**, in writing | The three questions again — then look at the board |
| 87–89 | Forward link | To d**x**/d*t* = **S**·**v** |

**Twenty-two slides.** 43 minutes of exposition over 13 slides — about 3.3
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

Item 4 — a repressor finding one site in 4.6 Mb — is meant to come out **wrong**,
and in a cohort this mixed it comes out wrong **two different ways**:

| Route | What it gives | Who takes it |
|---|---|---|
| Count the sites: 4.6 Mb / 20 bp ≈ 2×10⁵ looks, 65 ms to cross the cell between each | ~1.5×10⁴ s ≈ **4 hours** — ten cell cycles, far too slow | the biologists |
| Diffusion-limited capture: $t = V/4\pi D a$, $a$ ≈ 5 nm | ~**2 s** — far too fast | the physicists |
| **Measured** | **3–5 min** for one LacI dimer in a living cell ([Hammar 2012](https://doi.org/10.1126/science.1221648)) | — |

Both are two orders of magnitude out, **in opposite directions**, and neither
group can see its own error from inside its own method. Route 1 assumes the
protein returns to the bulk between looks; it does not — it binds DNA
non-specifically and slides ~40 bp per encounter. Route 2 assumes a free sphere
at $D = 7.7$; in a real cell the protein is stuck to DNA about 90% of the time.
In vivo the two errors largely cancel, which is why the honest statement is
*both models are wrong*, not *the three-dimensional model is too slow*. The
historical paradox is the in vitro one: at low salt the measured association
rate is ~100× the three-dimensional diffusion limit, and that excess is what
motivated the sliding model.

That is the best advertisement for estimating anyone has: *an estimate that
disagrees with a measurement is how you find a mechanism you were not looking
for.*

**An earlier version of this session asserted only the first route** ("a plain
three-dimensional search predicts hours") with no working and no source. It
loses the half of the room that reaches for a capture rate, at the payoff of the
session.

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
| $D_{\text{GFP}}$ in **eukaryotic** cytoplasm | ~27 µm²/s — **3.5× faster than in *E. coli*** | [Swaminathan, Hoang & Verkman, *Biophys. J.* **72**:1900–1907 (1997)](https://doi.org/10.1016/S0006-3495(97)78835-0) |
| $D_{\text{GFP}}$ in water | ~87 µm²/s | same comparison — the 11× is the crowding |
| LacI operator search, *in vivo* | **3–5 min** for one dimer (56 ± 2 s for 3–5 dimers) | [Hammar et al., *Science* **336**:1595–1598 (2012)](https://doi.org/10.1126/science.1221648) |

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

**Due today:** Phillips, R. & Milo, R. *A feeling for the numbers in biology.*
PNAS **106**(51), 21465–21471 (2009). Handed out at the end of session 1 and
posted to bCourses under Files → Readings. Focus: the case study on
pp. 21467–21468 that ends at *4% of the membrane*. Seven pages, no figures —
the argument is the text. See [readings](../../docs/readings.md).

It is background for the estimation habit this session teaches, not a paper the
session argues about, so nothing here depends on having read it. It is also the
right thing to point at when a student asks for more worked estimates while
doing PS1 Q1.

**Nothing is handed out at the end of this session.** PS0 is due tomorrow,
Wednesday 2 September; PS1 goes out Thursday.
