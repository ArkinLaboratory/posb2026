# Session 24 — Communities: quorum sensing, patterning, division of labour

Prior-year archive mining and vocabulary census. No deck source exists for this
session. Produced 7 November 2026 under the AGENTS.md rule *"Mine the prior
years before designing or building a session."*

This file also holds the **shared vocabulary census for sessions 24 and 25**
(§4). `sessions/s25-populations/PRIOR-YEARS.md` points here rather than
repeating it.

**What this file is not.** It is grounding material — derivations, systems,
numbers, questions, figures — not a template. The 2026 course diverges from
every prior year and the segment order below is recorded only so it can be
ignored deliberately.

---

## 1 · What the archive actually holds for this session

The triage note in `docs/deck-triage.md` — *"4 passing mentions of 'quorum', no
treatment"* — is **true of the 2025 PDFs and misleading about the archive.**
Three distinct bodies of session-24 material exist, none of them in 2025 text
where a grep for "quorum" would find them.

| source | what it is | status |
|---|---|---|
| 2018 L24 *BioCompiler — Resource Sharing — Analog*, pp. 15–21 | the **Turing / two-AHL patterning block**, Lu & Karig, PNAS 2018 | richest material in the archive; dropped after 2018 |
| 2019 L24 *Synthetic Morphology*, slides 4–17 | a **reaction–diffusion history and simulation block** | dropped after 2019 |
| 2016 L20 / 2018 L22 / 2019 L24 / 2020 L23 / 2024 L23 & L26 / 2025 L24 | the **Basu 2005 band-detect** slides, carried unchanged for nine years | survives into 2025, inside a deck the triage sent to S18 |
| `Dropbox (1)/2019/PoSB Textbook Chapters/20.405_LectureNotes.docx` | prose on Danino, Prindle/Chen, and the Voigt distributed XOR | never in a Berkeley deck |

Paths, verified this session:

- `Dropbox (1)/2018/PoSB Lectures/2018-12-06 Lecture 24 - BioCompiler - Resource Sharing - Analog/Lecture_24 Biocompiler_TuringPatterns_presented.pdf` (30 pp.)
- `Dropbox (1)/2019/PoSB Lectures/2019-12-05 Lecture 24 - Synthetic Morphology and Last Lecture for Berkeley/…_Lecture_24_Synthetic Morphology_LastBerkeleyLecture.pptx`
- `2025/Lectures/2025-12-02-Lecture 24- Protein-Circuits-and-more.pptx`, slides 63–67
- `Dropbox (1)/2019/PoSB Textbook Chapters/20.405_LectureNotes.docx`
- `Dropbox (1)/2019/PoSB Textbook Chapters/Weiss & Arkin PoSB Chapter 2.pdf`

---

## 2 · The grounding, by kind

### 2.1 Worked derivations

**There is no Turing-instability derivation anywhere in the archive.** No
dispersion relation, no condition on D_a/D_b, no linearisation about a
homogeneous steady state. What exists instead is one quantitative *claim* and
one *simulation*.

**2018 L24 p. 16, the claim.** The slide reads, verbatim and in bold under the
circuit: <q>need for significant difference in activator/inhibitor diffusion
rates</q>, then, in brackets on its own line:

> `[>100x difference required, 20x measured]`

That bracket is the whole engineering argument of the slide and it is stated,
not derived. The ratio that is required and the ratio that was achieved are the
two numbers session 24 can hang a derivation on — a student who is handed
">100× required, 20× measured" and asked where the 100 comes from is being asked
exactly the right question, and no prior year asked it.

**2018 L24 p. 21, the escape hatch.** Stochastic Turing patterns, with Nigel
Goldenfeld and Michael Martini credited. The slide's own words: fluctuations in
morphogen number <q>reduce required separation in diffusion rates</q> and
<q>enlarge the parameter space in which patterns can form</q>. The axes of the
3-D stability plot are defined on the slide: `v/u` ratio of AHL diffusion
coefficients, `e/p` ratio of AHL production rates, `d/p` ratio of degradation to
production rate; `v/u` runs 0–100, `e/p` 0–1, `d/p` 0–4. The measured-parameter
ellipsoid sits inside the green "stochastic neutral stability" region and
outside the deterministic one. The radial power spectrum of GFP is fitted with
slope **2.3**, the simulated one **−2.4**. This is a genuine quantitative
payoff and it is the only place in the archive where noise and pattern meet.

**2019 L24 slides 9–17, the simulation.** A numerical reaction–diffusion
treatment with no analysis. Slide 12 is titled *"Analytical Solution?"* and
answers itself: <q>Closed-form solution: difficult/impossible (except when F,G
very simple).</q> — <q>Discretize and Solve numerically.</q> Slide 13,
*"Turing's Solution"*, defines the symbols and nothing else: `a_i` inhibitor,
`b_i` activator, `D_a`, `D_b` diffusion rates, `β` random substrate, `k`
reaction rate, initial concentrations of a and b = 4. The parameter sets are on
the slides: 2-D at `Da=0.1 Db=0.02 β=0.1 k=0.02`; a sweep at `Da=0.1 Db=0.02`
over `k = 0.001, 0.002, 0.005, 0.01` and `β = 0.05, 0.1, 3`; 3-D at
`Da=0.125 Db=0.03125 β=0.1 k=0.0125`. The speaker note on the 2-D slide is one
line: <q>a diffuses more rapidly than b.</q> Attribution on the deck is
*"Reaction-Diffusion by A. Sacan & S. Girgin"*, which is a third-party teaching
deck, not a paper.

**The textbook does carry the equation.** Weiss & Arkin Chapter 2 writes Fick's
second law in two dimensions as its eq. (12) and the reaction–diffusion form as
eq. (13), introduced with <q>When reactions and passive transport intermix you
get reaction-diffusion equations.</q> It calls the diffusion constant `c`, not
`D`, and it does **not** give the `t ~ L²/2D` scaling — session 2's form is the
course's own. It points to *"Appendix B for a review of molecular diffusion and
transport"* `[unverified: Appendix B was not located in the four chapter PDFs
in this folder; settled by listing the 2019 Textbook Chapters folder for an
appendix file, or by opening Chapter 0's table of contents]`.

**Correction to AGENTS.md's precedent.** AGENTS.md records that Weiss & Arkin
Chapter 3 contains an undetected derivation that session 6 should have cited.
The equivalent check here comes out the other way: **"Turing" appears zero times
in all four Weiss & Arkin chapters and zero times in `20.405_LectureNotes.docx`**
(all apparent hits are inside "manufacturing" and "capturing"). There is no
hidden pattern-formation derivation in the textbook. Session 24 is free of the
session-6 hazard on this point.

### 2.2 The real systems and the numbers

**Lu & Karig, PNAS 2018 — the two-AHL Turing circuit (2018 L24, pp. 16–21).**
The best-grounded system in the archive for this session.

- Activator **3OC12HSL**, made by **LasI**, read by **LasR** on `p(Las)`.
  Inhibitor **C4HSL**, made by **RhlI**, read by **RhlR** on `p(Rhl)`. **CI** is
  the third node. Reporters dsRed and GFP. **IPTG** is the tuning input.
- p. 18 title, verbatim: *"Las and Rhl homologous quorum systems allow for
  different activation thresholds"*, with the two columns labelled **"Short
  range (activator)"** and **"Long range (use as inhibitor)"**.
- p. 18 measured dose–response (read off the rendered page): 3OC12HSL on plasmid
  **pFNK503** is half-maximal near **10⁻³–10⁻² µM**; C4HSL on **pFNK202** is
  half-maximal near **10¹ µM**. Roughly **three to four decades** of threshold
  separation, from two homologous systems. This is the number a design argument
  can be built on.
- p. 18 also carries the spatial data directly: fluorescence against distance
  over **±4 cm** on a plate, at **0, 2.5, 5 and 8 hours**, for both signals.
  This is a measured diffusion front at centimetre scale over hours — see §3.
- p. 16 lower-left panel is labelled **"cellular lawn"** on the x-axis "Space",
  with 3OC12HSL and C4HSL traces above RFP/GFP traces. The word *lawn* does not
  appear anywhere in the 2026 decks (§4).
- p. 20: *"Control of pattern characteristics: IPTG, via negative feedback,
  modulates spot sizes"* — one knob, one observable, and the mechanism named.

**Basu et al., Nature 2005 — the band detector.** Carried unchanged from 2016 to
2025. The slide states the specification as pseudocode, verbatim:

> `case (AHL)  low: RFP = off   med: RFP = on   high: RFP = off`

and the behaviour as <q>"Ring-like spatial patterns"</q> with the bio-program
<q>Cell type: sender send (AHL)</q> / <q>Cell type: receiver input: AHL</q>.
The receiver circuit on the slide is LuxR, CI, LacI, LacIM1 and the reporter.
**No numbers appear on these slides at all** — no AHL concentration, no ring
radius, no plate dimension, no time. Nine years of teaching this figure and the
quantitative content is zero.

**Tabor et al., Cell 2009 — the edge detector.** Present as exactly one slide,
*"Edge detection: Programming spatial response"*, in 2018 L22 and 2019 L24 only,
with the citation and no analysis.

**Danino et al., Nature 2010 — synchronised quorum of genetic clocks.** Only in
`20.405_LectureNotes.docx`, never in a Berkeley deck. The notes carry real
quantities and mechanism: oscillation period <q>roughly 90-100 minutes</q>; a
microfluidic trapping chamber where cell growth and washout balance; flow rate
as the AHL-dilution knob, with faster flow giving **longer period and larger
amplitude**; cell density as a second, weaker knob; and a regime at
<q>low density and slow decay</q> where oscillations do not occur at all. The
spatiotemporal result is stated plainly — oscillations <q>start in the center of
a group of cells and propagate outwards</q>, because central cells see more
neighbours inside a fixed radius. **Caveat:** the species symbols in this
document are OMML equation objects and extract as blanks, so every molecule name
in those paragraphs is missing from the text. They must be read in Word before
any of this is quoted to students.

**The Chen/Prindle two-strain oscillator** (same notes) is the archive's only
*division-of-labour* system: an <q>activator strain</q> and a <q>repressor
strain</q>, coupled by two AHL variants, where neither oscillates alone.

**Voigt's distributed XOR** (same notes): NOR gates placed in **four separate
colonies** in a diamond on a plate, wired by AHL diffusion, <q>in close enough
proximity such that small molecules could diffuse</q>. The argument given for
splitting the circuit across cells is orthogonality — the gates reuse the same
three promoters and cannot coexist in one cell. That is a *reason to build a
consortium* stated in engineering terms, and it is the strongest available
motivation for the division-of-labour half of this session.

### 2.3 Discussion questions that were used

The 2019 L24 framing slide (slide 2), which is the only place the archive states
the session's own problem, in its own words:

> <q>From these differential patterns can we drive dynamic mechanochemical
> changes that pattern tissue</q> … <q>This requires a "synthesis" of nearly
> everything we have learned!</q>

2025 L24 slide 62 is a live Poll Everywhere prompt, verbatim: *"What are some
real-world applications for analog genetic circuits?"* — the mechanism (a free-
text poll) is reusable even though the question is not session 24's.

The archive contains **no vote–argue–vote ConcepTest** on patterning, and no
question with a right answer. Everything above is open-ended, which AGENTS.md
rules out for this cohort.

### 2.4 Readings already assigned

**None, for this topic, in any year examined.** The 2018/2019/2020 syllabus
`.docx` files are roughly 1,400 characters each and contain no reading list; the
lecture folders for the morphology and biocompiler decks hold only decks. The
papers below appear as *citations on slides*, which is not the same as an
assignment:

| paper | cited on |
|---|---|
| Basu et al., Nature 2005 | 2016 L20, 2018 L22, 2019 L24, 2020 L23, 2024 L23/L26, 2025 L24 |
| Tabor et al., Cell 2009 | 2018 L22, 2019 L24 |
| Lu et al., PNAS 2018 | 2018 L24 pp. 16–17 |
| Beal, Bachrach, SCW 2008; Beal, Lu & Weiss, PLoS ONE 2011 | 2018 L24 p. 15 |
| Guye et al., Nat. Comm. 2016 | all morphology decks |

2026 assigns **Balagadde et al., Mol Syst Biol 2008** (`readings.yaml`, s24) —
the synthetic predator–prey ecosystem. **No prior year assigned or cited it.**

### 2.5 Figures, by source, and what each argued

| figure | source | the argument it was used to make |
|---|---|---|
| band-detect circuit + ring plates | Basu 2005 | a specification in three cases becomes a spatial pattern |
| activator/inhibitor topology + lawn traces | Lu PNAS 2018, 2018 L24 p. 16 | a cheetah and a bacterial lawn are the same mechanism |
| Las/Rhl dose–response + plate time series | Lu PNAS 2018, 2018 L24 p. 18 | two homologous systems give you range separation for free |
| IPTG spot-size series | Lu PNAS 2018, 2018 L24 p. 20 | the pattern has a tunable length scale |
| 3-D stability volume + power spectra | Goldenfeld/Martini, 2018 L24 p. 21 | noise widens the region where patterns exist |
| 1-D/2-D/3-D RD simulations | Sacan & Girgin, 2019 L24 slides 14–17 | parameter sweeps give spots, stripes, labyrinths |
| Gata6 symmetry breaking | Guye 2016 | identical cells break symmetry and differentiate by neighbourhood |

### 2.6 What is genuinely new in 2026 — and what a prior year did better

**New, and defensible on a slide:**

1. **Any quantitative treatment of a community.** `consortium`, `consortia`,
   `co-culture`, `cross-feeding`, `mutualism`, `commensalism`, `predator`,
   `prey`, `Lotka-Volterra`, `carrying capacity`, `chemostat`, `syntrophy` and
   both spellings of `division of labour` are **all zero across all prior-year
   decks examined and all 2026 decks** (§4). No year of this course has modelled
   two interacting populations.
2. **A reading with a runnable model.** Balagadde 2008, BioModels
   `BIOMD0000000296`. No prior year assigned a paper here at all.
3. **The diffusion length scale as a design constraint**, connected back to
   session 2 (§3). Every prior year showed spatial data and never once put a
   number on how far a signal gets.
4. **Lotka–Volterra as an object built rather than named.** Absent from every
   prior deck and from the textbook.

**What a prior year did better, and should be taken back:**

- **2018 L24 is better than anything 2019–2025 on patterning**, and it was cut.
  The ">100× required, 20× measured" line, the Las/Rhl threshold separation, the
  IPTG spot-size knob and the stochastic-Turing result are all there and all
  gone from the later decks.
- **The 2019 L24 history block (slides 4–7)** — Turing 1952 through Bard,
  Murray, Meinhardt, Swindale, Young, Kauffman, Turk — is a better motivation
  than anything in the 2020–2025 line. It is four slides and it earns them.
- **The nine-year-old Basu slides are not better**, but they are the only thing
  the course has taught continuously, so students who have seen a PoSB talk may
  recognise them. They carry no numbers and should not be reused unchanged.

---
## 3 · Session 2's diffusion result, exactly as it stands

Session 24 is required by `docs/coverage-matrix.md` T66 — *"Diffusion length
scale in a community (reuses T2)"* — to reuse this. T2 is *"Diffusion
timescale, t ~ L²/2D"*, taught in S2 and assessed in PS1 and the Final. Session
24 must call back to it in this form and not re-derive it differently.

**The form on the slide.** `decks/s02_substrate.py`, slide *"Items 1 to 3, and
the sign of every assumption"* (63–67 min), item 2, verbatim:

> `t ~ L²/2D = (1 µm)² / (2 × 7.7 µm²/s) ≈ 65 ms.  Tens of milliseconds.`

**The factor of 2 is there, and the convention is explicitly flagged.** The
habit slide at 74–77 min, verbatim:

> *State the convention before the number* — `L²/2D or L²/6D? Say which. A
> factor of three is nothing; an unstated convention is an argument you cannot
> settle afterwards.`

**The numbers and the media.** All three D values are on slides, with sources:

| quantity | value | medium | source as cited in s02 |
|---|---|---|---|
| D(GFP) | **7.7 µm²/s** | *E. coli* cytoplasm | Elowitz et al., J Bacteriol 1999 |
| D(GFP) | **87 µm²/s** | water | same comparison |
| D(GFP) | **~27 µm²/s** | eukaryotic cytoplasm | Swaminathan, Hoang & Verkman, Biophys J 1997 |
| L | **1 µm** / **20 µm** | *E. coli* / HeLa | — |
| viscosity | ~12 cP (GFP), ~100 cP (ribosome-sized) | *E. coli* | Valverde-Mendez et al., PNAS 122(4) e2406340121 (2025) |

Item 2's self-explanation prompt, verbatim: `Use the cytoplasmic D, not the
value in water (87 µm²/s). Water is 11× higher, so it would have given ~6 ms —
too fast by an order of magnitude. That factor of eleven IS the crowding.`

Item 3, verbatim: `t ≈ (20 µm)² / (2 × 7.7 µm²/s) ≈ 26 s, so ~400× longer.
Because t ∝ L², not L.` — with the correction attached: holding D fixed makes
26 s too big; at 27 µm²/s the real crossing is **~7 s** and the real ratio
**~110×**.

**The figure.** Slide *"Two things that number will not tell you"* (22–25 min)
carries `figures/build/s02_size_dependence.png` — probe size against effective
viscosity, from Valverde-Mendez 2025 — and the course's own movie
`figures/build/s02_confinement.mp4`, captioned `ours — a random walk and a
wall, nothing else`. Its third bullet is the standing instruction:

> *So use L²/2D, and say so* — `It is the right first estimate and we will use
> it all term. Just know which direction it is wrong in: for anything large,
> optimistic by more than an order of magnitude.`

**Where else it has already been reused, so session 24 is the fourth use, not
the second:**

- `s03` — `Diffusion must beat reaction. Damköhler number Da = τ_mix / τ_rxn,
  with τ_mix ≈ L²/2D and τ_rxn ≈ 1/(k_on·C).`
- `s03` — `…crosses the cell hundreds of times before it reacts, so there is no
  spatial gradient to speak of.`
- `s18` — `diffusion across a cell twenty times wider takes about 400 times
  longer — 20². Session 2 did that arithmetic in week…`

**The consequence for session 24.** s03's line is a *denial* of a spatial
gradient: inside one cell, mixing beats reaction and there is no gradient. A
community is the case where that denial fails. Session 24's reuse of T2 is
therefore not a repetition — it is the first time in the course the inequality
runs the other way, and the archive hands over the measurement that shows it:
Lu's plate data, **±4 cm over 0 to 8 hours** (§2.2). At L = 1 cm and
D ≈ 5 × 10² µm²/s for a small molecule in agar, `L²/2D` is of order 10⁵ s —
**hours, not milliseconds.** `[unverified: no AHL diffusion coefficient in agar
appears on any prior-year slide or in the 2026 decks. Settled by taking D from
Lu et al., PNAS 2018 or Basu et al., Nature 2005 and citing it.]`

**Pitfall.** Session 2's `s03` value, the `L²/2D` convention and the word
*gradient* are all single-use in the corpus — `gradient` has **one** hit in all
of `decks/s*.py` and it is the sentence denying one. Session 24 must not use
"gradient" as known vocabulary.

---

## 4 · The vocabulary census — sessions 24 and 25

**Counted across `decks/s01*.py` … `decks/s23*.py`** (22 deck sources; there is
no s15 deck, and s24/s25/s26/s27/s28 do not exist yet), 7 November 2026, by
parsing each file's AST and attributing every string literal to the call that
renders it. `T` = slide title or header; `B` = slide body, including the tuple
lists that loops render as body text; `N` = speaker note. Python comments and
module docstrings are excluded — they are not shown to anyone.

**A note in `N` does not count as having taught something.** Several of the
non-zero rows below are N-heavy and should be read as zeros for teaching
purposes; they are marked in §5.


### Session 24 vocabulary

| term | total | where (T = slide title/header, B = slide body, N = speaker note) |
|---|---:|---|
| **quorum sensing** | **0** | — |
| **autoinducer** | **0** | — |
| AHL | 24 | s10 B9 N6; s19 B3 N5; s22 B1 |
| **acyl-homoserine lactone** | **0** | — |
| LuxR | 5 | s10 B1 N1; s13 B1; s19 B1; s22 B1 |
| **LuxI** | **0** | — |
| **LasR** | **0** | — |
| **LuxAB** | **0** | — |
| sender | 9 | s10 B2 N2; s13 B1 N3; s16 B1 |
| receiver | 12 | s10 B4; s13 B1 N6; s16 B1 |
| band detect | 1 | s01 B1 |
| **band-pass** | **0** | — |
| inverter | 5 | s16 T1 B2 N2 |
| gradient | 1 | s03 B1 |
| diffusion | 28 | s02 T1 B5 N16; s03 B1 N1; s04 N1; s10 B1; s18 B1; s20 N1 |
| diffusion coefficient | 1 | s02 T1 |
| **length scale** | **0** | — |
| **Turing** | **0** | — |
| **pattern formation** | **0** | — |
| **morphogen** | **0** | — |
| **lawn** | **0** | — |
| **consortium** | **0** | — |
| **consortia** | **0** | — |
| **co-culture** | **0** | — |
| **cross-feeding** | **0** | — |
| **mutualism** | **0** | — |
| **commensalism** | **0** | — |
| **predator** | **0** | — |
| **prey** | **0** | — |
| **Lotka-Volterra** | **0** | — |
| **carrying capacity** | **0** | — |
| **chemostat** | **0** | — |
| dilution rate | 1 | s20 N1 |
| **division of labour** | **0** | — |
| **division of labor** | **0** | — |
| **syntrophy** | **0** | — |

### Session 25 vocabulary

| term | total | where (T = slide title/header, B = slide body, N = speaker note) |
|---|---:|---|
| **virus** | **0** | — |
| **virion** | **0** | — |
| **capsid** | **0** | — |
| packaging | 2 | s02 B1; s18 N1 |
| **encapsidation** | **0** | — |
| genome | 21 | s01 N1; s02 B2 N1; s03 N1; s06 T1 B5 N1; s16 B1; s17 B1; s19 N1; s20 B3 N2; s23 B1 |
| **diploid** | **0** | — |
| **heterozygous** | **0** | — |
| **homozygous** | **0** | — |
| **helper virus** | **0** | — |
| **defective interfering** | **0** | — |
| **DIP** | **0** | — |
| TIP | 2 | s18 N1; s19 N1 |
| **interfering particle** | **0** | — |
| **R0** | **0** | — |
| **basic reproductive ratio** | **0** | — |
| **reproductive number** | **0** | — |
| **transcritical** | **0** | — |
| **invasion** | **0** | — |
| **epidemic** | **0** | — |
| **SIR** | **0** | — |
| gene drive | 1 | s10 N1 |
| **CRISPR drive** | **0** | — |
| **homing** | **0** | — |
| **super-Mendelian** | **0** | — |
| **allele** | **0** | — |
| fitness cost | 3 | s23 N3 |
| selection coefficient | 6 | s23 B4 N2 |
| mutation rate | 14 | s23 B5 N9 |
| binomial | 2 | s02 B1 N1 |
| **co-infection** | **0** | — |
| **superinfection** | **0** | — |
| burst size | 2 | s12 B2 |
| **minimal genome** | **0** | — |
| **minimal gene set** | **0** | — |

### Shared machinery both sessions assume

| term | total | where (T = slide title/header, B = slide body, N = speaker note) |
|---|---:|---|
| Hill function | 17 | s04 T1 B1 N1; s05 B1; s06 B1 N1; s07 B1; s11 B1; s12 B3; s13 B4; s19 B1 N1 |
| cooperativity | 78 | s04 B2 N1; s06 T1 B3 N2; s07 B6 N3; s08 B5 N3; s09 B6 N4; s11 B5 N3; s12 B1; s13 B3 N1; s18 B11 N7; s19 B6 N5 |
| steady state | 103 | s02 B1 N1; s03 T1 B8 N2; s04 B1 N2; s05 B4; s06 N1; s07 B9 N4; s08 N1; s09 B4 N2; s10 B6 N1; s11 B2; s12 B9 N3; s16 B1; s18 B2 N2; s19 B2 N4; s20 B3 N1; s21 B5 N4; s22 B8 N7; s23 B1 N1 |
| fixed point | 28 | s03 N2; s07 N1; s08 T1 B13; s09 B6 N1; s11 B2; s12 B1; s14 B1 |
| nullcline | 24 | s07 B1 N1; s08 B9; s09 B7; s10 B1; s11 N1; s13 N1; s14 B1; s18 B1 N1 |
| Jacobian | 22 | s03 B1; s08 B4; s09 B3; s11 B2 N1; s12 B1; s14 B8; s18 N1; s20 B1 |
| eigenvalue | 20 | s03 B1 N2; s07 N1; s08 B1 N1; s11 T1 B4 N3; s12 B1 N2; s14 B3 |
| bifurcation | 10 | s03 N1; s07 N1; s08 B1 N1; s09 B2; s11 N3; s19 B1 |
| phase plane | 15 | s06 B1; s07 B3; s08 B3; s09 B1; s10 B1; s18 B2 N3; s23 N1 |
| mass action | 7 | s02 B1; s03 T2 B2 N1; s17 N1 |
| quasi-steady-state | 19 | s02 N1; s03 B3 N3; s04 B5 N3; s09 B1; s17 N1; s19 B1; s21 B1 |

### 4.1 Five non-zero rows that are false positives, and are really zero

Checked by reading every hit in context. These must be treated as **0**:

| row | apparent | what the hits actually are |
|---|---|---|
| `gene drive` | 1 (s10 N) | `one gene driven by X` — a figure description |
| `TIP` | 2 (s18 N, s19 N) | `on the tip of my tongue` |
| `packaging` | 2 (s02 B, s18 N) | a Python *package* |
| `gradient` | 1 (s03 B) | `there is no spatial gradient to speak of` — a denial |
| `burst size` | 2 (s12 B) | **translational** burst, `geometric with mean k_p/γ_m` — a different object from a viral burst size, and a name collision session 25 must disarm explicitly |

### 4.2 The non-zero rows that are real, and what they actually established

- **`AHL` (24) and `sender`/`receiver` (9/12) are genuinely taught, in s10.**
  Session 10 builds the sender/receiver incoherent-feedforward pulse circuit on
  slides: `Sender` / `makes AHL, which diffuses to its neighbors.` and
  `Receiver` / `LuxR·AHL turns on GFP — and turns on CI, which represses GFP.`
  Concentrations appear (`pulses at AHL above 47 nM`), and s19 and s22 reuse
  AHL as an inducer. **Session 24 inherits sender, receiver, AHL and LuxR as
  known objects.** This is the single largest asset the session has.
- **But the chemistry is absent.** `LuxI` **0**, `acyl-homoserine lactone`
  **0**, `autoinducer` **0**, `quorum sensing` **0**. Students have been told a
  sender "makes AHL" and have never been shown the synthase, the molecule, or
  the reason a cell would do this.
- **`diffusion` (28)** is real but **16 of 28 hits are speaker notes**; the
  slide-facing count is 5 body + 1 title in s02, plus one line each in s03, s10,
  s18.
- **`diffusion coefficient` (1)** is a slide *title* in s02
  (`What one diffusion coefficient hides`) and appears in no body text anywhere.
- **`band detect` (1)** is one item in a list of circuit names on an s01 slide:
  `Toggle, oscillator, band detector, multi-input logic, metabolic pathway,
  classifier — sessions 9 through 26.` A forward-looking list, not a treatment.
- **`inverter` (5, s16)** is logic-gate vocabulary, including a title. It is not
  the band-detect sense and will collide if session 24 is careless.
- **`mutation rate` (14) and `selection coefficient` (6)** are entirely s23 and
  are covered in `../s25-populations/PRIOR-YEARS.md` §3.
- **The shared machinery is in excellent shape.** `steady state` 103,
  `cooperativity` 78, `fixed point` 28, `nullcline` 24, `Jacobian` 22,
  `eigenvalue` 20, `Hill function` 17, `phase plane` 15, `bifurcation` 10 — all
  with substantial body counts across many sessions. **Neither session has a
  mathematical-machinery problem.** Both have an object problem.

---

## 5 · What session 24 must introduce from nothing

"From nothing" = zero or false-positive-only hits in `decks/s01*.py`–`s23*.py`,
and therefore never shown to this cohort.

**Physical objects — these need a picture before any symbol.**

| term | what has to be on the screen |
|---|---|
| **acyl-homoserine lactone / autoinducer** | the molecule. 2018 L24 p. 18 has both structures drawn beside their synthases — reuse it |
| **LuxI / LasI / RhlI** (synthases) | the half of the circuit s10 never drew. `LuxI` 0, `LasR` 0 |
| **quorum sensing** | the *why*: cell density read out as a concentration. 0 hits, in a course that has used the molecule 24 times |
| **lawn / plate / colony** | the physical arena. `lawn` 0. Every patterning result in the archive is a plate photograph and the room has never been shown one |
| **band detector** (as a device) | 1 passing mention. Basu's `low: off / med: on / high: off` specification and the ring plates |
| **Turing pattern / morphogen** | both 0. 2018 L24 p. 16 is the slide: cheetah, two AHLs, bacterial lawn |
| **consortium / co-culture** | two strains in one vessel. 0 hits — the course has never had more than one cell type |
| **chemostat** | 0. Balagadde 2008's apparatus; `dilution rate` has 1 hit and it is an s20 speaker note |
| **predator / prey strains** | 0/0. The assigned reading's own object |
| **cross-feeding / syntrophy / mutualism / commensalism** | all 0. The interaction types |

**Mathematical ideas — these need a definition, and the room has the machinery
to take it fast.**

| term | the definition owed, and what it can lean on |
|---|---|
| **length scale** | 0 hits. √(2Dt) as the companion to T2's t ~ L²/2D. Leans directly on s02 |
| **Lotka–Volterra** | 0. Two coupled ODEs. The room has nullclines (24), Jacobian (22), eigenvalues (20) and the phase plane (15) from s08/s09 — this is the cheapest new model in the whole course |
| **carrying capacity** | 0. One parameter, one nullcline |
| **dilution rate** | effectively 0. The chemostat's control input; s22 uses `d` in the antithetic controller, so flag the reuse |
| **band-pass** | 0. The product of two transfer functions. `20.405_LectureNotes.docx` already argues it this way and names the Arkin-lab UAA-ON/UAA-OFF composition |
| **division of labour / labor** | 0/0, both spellings. A definition, not a picture: a task no single genotype performs |
| **pattern formation** | 0. The term for what the hour is about |

**Not new, and must be called back rather than redefined:** `sender`,
`receiver`, `AHL`, `LuxR`, `diffusion`, `t ~ L²/2D`, `steady state`,
`nullcline`, `Jacobian`, `eigenvalue`, `phase plane`, `Hill function`,
`cooperativity`.

---

## 6 · Weakest part of this file

The Danino, Prindle/Chen and Voigt-XOR material in §2.2 comes from
`20.405_LectureNotes.docx`, whose molecule names are equation objects and
extracted as blanks. I read the surrounding prose, not the symbols. **Nothing
from those paragraphs should reach a slide until the file is opened in Word.**

Second: I rendered and looked at 2018 L24 pp. 16, 18 and 21 and read the text
layer of the rest. Pages 17, 19 and 20 — the simulation panels, the DsRed/GFP
merge and the IPTG spot-size series — I have from text extraction only, so the
axis values and spot diameters on them are unread.

Third: the archive sweep covered 541 lecture `.pptx` and the 2023–2025 PDFs for
the thirteen session-24 keywords. Years 2010–2015 were included in the filename
and keyword sweeps but no deck from those years was opened.
