# Session 25 — Design at population scale: DIPs, TIPs, gene drives

Prior-year archive mining. No deck source exists for this session. Produced
7 November 2026 under the AGENTS.md rule *"Mine the prior years before designing
or building a session."*

**The vocabulary census for sessions 24 and 25 lives in
[`../s24-communities/PRIOR-YEARS.md` §4](../s24-communities/PRIOR-YEARS.md).**
It is not repeated here. §4 below gives only what follows from it for this
session.

**What this file is not.** Grounding material, not a template. The segment order
of the ancestor decks is recorded so it can be departed from deliberately.

---

## 1 · The ancestor is one deck, taught eight times, essentially unchanged

Every lecture under the titles *DIPS, TIPS and Gene Drives* and *Epidemics* is
the same deck with slides added at the front and cut from the middle. Verified
by extracting all eight and comparing.

| year | lecture | file | pages/slides |
|---|---|---|---|
| 2016 | L21 | folder holds `TIPSWeinberger.pdf` (**corrupt — "Document stream is empty"**) | — |
| 2018 | L20 | `Dropbox (1)/2018/PoSB Lectures/2018-11-20 .../Lecture_20 DIPS, Tips and Gene Drives_presented.pdf` | 51 |
| 2019 | L20 | `Dropbox (1)/2019/PoSB Lectures/2019-11-19 .../…Lecture_20 DIPS, Tips and Gene Drives_presented.pdf` | same |
| 2020 | L20 | `Dropbox (1)/2020/PoSB Lectures/[PUBLIC] PoSB Lectures/Lecture-20-DIPS, Tips and Gene Drives-2020-11-12.pdf` | same |
| 2021 | L22 | `Dropbox (1)/2021 PoSB/PoSB Lectures/2021-12-02- .../2021-12-02 Lecture 21 DIPS, Tips and Gene Drives.pptx` | 52 |
| 2023 | L27 | `2023/Lectures/2023-11-30 Lecture 27 DIPS, Tips and Gene Drives.pdf` | 52 |
| 2024 | L26, L27 | `2024/Lectures/2024-11-27-Lecture 26-ProgrammableTissue and Epidemics.pdf`; `…2024-12-05-Lecture 27-Epidemics.pdf` | — |
| **2025** | **L25** | `2025/Lectures/2025-12-04-Lecture 25-Epidemics.pdf` | **39** |

**Correction to the brief.** 2023 L27 is not the most recent. **2025 L25
*Epidemics*, 4 December 2025, is**, and it is the best evidence of how Adam last
taught this. It is the 2023 deck with the fourteen-slide viral-genetics block
(recombination / reassortment / complementation / pseudotypes) **cut**, and
nothing added. 39 slides where 2023 had 52.

What was added between 2018 and 2023 was the COVID material: three slides
(2025 slides 8–10) carrying the Chen et al. BHRP compartment model, pulled from
*"A mathematical model for simulating the phase-based transmissibility of a
novel coronavirus"* and linked on the slide. 2018 has no SEIR of any kind.

---

## 2 · What the archive supplies, by kind

### 2.1 Worked derivations — there are none

This is the central finding and it is unambiguous across all eight versions.

**There is no R₀ derivation, no threshold condition and no partitioning
calculation anywhere in the lineage.** The slide that would carry it is titled
*"TIPS: Engineering R0>1"* and appears verbatim, byte-identical, in 2018, 2019,
2020, 2021, 2023, 2024 L26, 2024 L27 and 2025 L25. Its entire content, rendered
and read this session:

> **TIPS: Engineering R0>1**
> • `DIPS cannot outcompete wild-type alone. They need to do better in a way–
>   produce more virions per co-infected cell than its competitor.`
> • `Reproductive Ratio  (R0>1)`
> • `More efficient packaging by` — `Greater number of genomes per cell.`
> *Tanner EJ, Kirkegaard KA, Weinberger LS (2016) PLOS Genetics 12(5): e1005986*

R₀ is **named, asserted as a requirement, and never written down.** There is no
equation on the slide, no symbol table, no number. "How far did he take it" has
a one-word answer: nowhere.

**The only mathematics on any of these slides is pasted in and not worked.**
2025 slide 9 (2023 slide 9) is a wall of **seventeen ODEs** — the full Chen
BHRP system, S/E/I/R for bats, hosts and people plus a reservoir W, with
`dS_B/dt = Λ_B − m_B S_B − β_B S_B I_B` at the top — set beside a four-item
bullet list reading `Susceptible / Exposed / Infected / Removed`. The equations
are an image. Nothing is derived from them, no R₀ is extracted from them, and
the next slide is a curve fit of reported against simulated Wuhan case counts,
08/12/2019–01/01/2020, peaking at 9 new cases a day.

**The DIP dynamics are likewise shown, not derived.** 2025 slide 19, *"Model of
Continuous Infection in the Presence and Absence of DIPs"* (Frensing & Heldt et
al., PLOS ONE 8(9) e72288, 2013), is a two-panel schematic — uninfected →
STV-infected / DIP-infected → co-infected, with apoptosis and degradation — and
two simulated time courses. Read off the rendered page: **without DIPs**, HA and
TCID₅₀ flat at ~10⁹ virions/mL over **180 days**; **with DIPs**, sustained
oscillation between roughly 10³ and 10⁹ over **18 days**, period about 4 days.
This is the best quantitative figure in the deck and the slide says nothing
about why the oscillation happens.

**The only closed-form threshold in the speaker notes** is in the pasted Rouzine
& Weinberger (J. Virol. 2013;87:2081–2093) figure caption on 2025 slides 29–30,
which carries the parameters the paper used: DIP/HIV-1 production ratio
`P = 5`, basic reproduction ratio `R0 = 10`, capsid-to-genome ratio
`η = 2, 5, 10`, capsid waste `κ`, and an untreated set-point of
`3 × 10⁴ RNA copies/ml blood`. These are in the **note**, verbatim from the
journal, and none of them is on a slide. By AGENTS.md's own standard a note is
not teaching.

**Gene drives are taught entirely by cartoon.** 2025 slide 34, rendered: a
*Bay Nature* comic strip (`Cartoons taken from Bay Nature, June 27, 2016.
(Alison Hawkes & Donna Almendrala)`) titled "Understanding Gene Drives II",
captioned `100 % of offspring get the allele.` There is no allele-frequency
recursion, no super-Mendelian inheritance ratio, no fitness cost, no resistance
allele, and no release-threshold calculation in any year.

### 2.2 The real systems and the numbers

Everything quantitative in the lineage, exhaustively:

| system | the numbers on the slide | source as cited |
|---|---|---|
| Influenza DIP production in continuous culture | A/PR8/34 H1N1 in **AGE1.CR duck** cells; virion **Ø 70–120 nm**; cell lines table (MDCK dog kidney, Vero monkey kidney, HEK293.sus, CAP human amniocytes, AGE1.CR duck retinoblasts) at `> 1 × 10⁷ cells/mL`; the 180-day and 18-day traces above | Frensing & Heldt et al., PLOS ONE 8(9) e72288 (2013) |
| HIV / TIP design case | herd immunity `>80%` required for a vaccine to prevent spread; **~10 years** to AIDS untreated against **>>10 years** with a TIP (2025 slide 26, Notton figure, three scales: epidemiological / individual patient / single cell) | Notton, Sardanyes, Weinberger & Weinberger, *Trends in Biotechnology* 32(8):400–405 (2014) |
| HIV DIP model parameters | `P = 5`, `R0 = 10`, `η = 2/5/10`, set-point `3 × 10⁴ copies/ml` — **speaker note only** | Rouzine & Weinberger, J. Virol. 87:2081–2093 (2013) |
| Conditionally replicating lentiviral vector | *"Phase I Clinical Trials by Virxsys"*; `With Leor Weinberger, David Schaffer` | Levine et al., PNAS 103:17372 (2006) |
| Epidemic history table | thirteen rows: 1918 influenza **75,000,000**; Black Death **75–100 million, 30–60% of population**; HIV/AIDS **>30,000,000** | WIKIPEDIA, credited on the slide |
| Malaria burden | **214 million cases**, **438,000 deaths** (2015); **$12 bn/year** African economic loss | `Source: WIKIPEDIA` |
| COVID fit | Wuhan onset-date case counts 08/12/2019–01/01/2020, ≤9/day | Chen et al., linked on slide 8 |
| DIP host range | `murine leukemia virus / Rous sarcoma virus / vesicular stomatitis virus / influenza virus / dengue fever virus`; absent from `poxviruses (MVA), coronaviruses, and parvoviruses?` | 2025 slide 20–21 |
| Gene drive history | Burt **2003** homing endonuclease; Esvelt/Church **2014** CRISPR/Cas9; `100 %` inheritance | 2025 slides 32–35 |

**Two numbers are secondhand from Wikipedia and both are a decade stale.** The
malaria figures are 2015 and the slide still opens `As is currently painfully
evident….` — a line written for COVID and now reading as nothing in
particular. AGENTS.md requires speaker notes to carry provenance problems; this
is one.

### 2.3 Discussion questions, in their original wording

Four, and the first two survive in 2025. All open-ended; none is a
vote–argue–vote with a right answer, which AGENTS.md rules out for this cohort —
so the *wording* is reusable, the *format* is not.

**2025 slide 24 (all years), on the DIP→TIP step:**
> `How could they outcompete wt virus?` / `What about safety concerns?`

**2025 slide 35 (all years), on gene drives — the strongest of the four:**
> `What is the big innovation from the 2003 proposal of using a natural homing
> endonuclease and the 2014 proposal from Esvelt/Church to use CRISPR/Cas9?`
> `What sorts of genes should we carry along with the endonuclease?`
> `Is 100% actually a good idea? What are the risks?`
> `What might we do to mitigate them?`

**2018 L20 p. 31, cut after 2021:**
> `What would it take to make a DIP Therapeutic?` /
> `What are some of the technical and other issues with doing so.`

**2018 L20 p. 46, cut after 2021** — a closing question with a concrete answer
list (`Invasive mammals / Invasive plants / Disease vectors: Anopheles`), cited
to Esvelt et al. (2014) eLife 3:
> `What are good targets for gene drives?`

**2025 slide 39, the closing slide of the last PoSB lecture of 2025:**
> `How do we risk assess?` / `How do we regulate?` /
> `Under what conditions can we field test?` /
> `What degree of design/modeling/laboratory work is necessary?`

### 2.4 Readings already assigned — none

No reading list exists for this topic in any year examined. The 2018/2019/2020
syllabus `.docx` files carry none. The lecture folders for 2018 L20, 2019 L20
and 2020 L20 hold only decks. The one paper handed out was in 2016 —
`2016/PoSB Lectures/2016-11-28- Lecture 21/TIPSWeinberger.pdf` — and **the file
is corrupt**; `pdfinfo` and `pdftotext` both return *"Document stream is
empty"*, so which Weinberger paper it is cannot be determined from the archive.
`[unverified: settled by opening the file in Preview, or by checking the 2016
syllabus.]`

Papers cited on slides, every year: Frensing & Heldt 2013; Notton et al. 2014;
Tanner, Kirkegaard & Weinberger 2016; Rouzine & Weinberger 2013; Levine et al.
2006; Esvelt et al. 2014 (2018 only).

2026 assigns **Weinberger, Schaffer & Arkin, J. Virol. 77(18), 10028–10036
(2003)** — Adam's own paper — and **no prior year cited it on a slide.**

### 2.5 Figures, by source, and what each argued

| figure | source | the argument |
|---|---|---|
| STV/DIP schematic + two time courses | Frensing & Heldt 2013 (2025 sl. 19) | DIPs turn a steady infection into an oscillation |
| segment-specific PCR, FL vs DI | Frensing & Heldt 2013 (sl. 18) | the defective genome is a real, measurable species |
| three-scale TIP cartoon | Notton 2014 (sl. 26) | a therapy that travels the transmission route reaches the people a clinic does not |
| dominant drug targeting vs TIPs | Tanner 2016 (sl. 25) | a drug selects for escape; a competitor does not |
| DIS kissing-loop divergent evolution | Rouzine & Weinberger 2013 (sl. 29) | genome-stealing interference is **evolutionarily unstable** |
| capsid-stealing parameter surfaces | Rouzine & Weinberger 2013 (sl. 30) | capsid-stealing is stable across a broad parameter range |
| BHRP flowchart + 17 ODEs + curve fit | Chen et al. (sl. 8–10) | an epidemic is a compartment model |
| Bay Nature comic | Bay Nature 27 June 2016 (sl. 33–34) | homing converts a heterozygote into a homozygote |
| reversal / immunisation / precision drives | Esvelt et al. 2014 eLife (sl. 37–38, notes only) | a drive can be undone, fenced, or limited |

The Rouzine pair is the most interesting thing in the deck and is the least
taught: slide 29 says interference by genome stealing fails under evolution,
slide 30 says interference by capsid stealing does not. **That contrast is a
design rule with a mechanism, and neither slide states it in its own words** —
both titles are the journal's figure captions pasted in, and the argument lives
only in the pasted caption text in the notes.

### 2.6 What is genuinely new in 2026 — and what a prior year did better

**New, and defensible on a slide:**

1. **Any mathematics at all.** Eight prior versions name R₀ and never write it.
   `docs/coverage-matrix.md` T73 requires students to *"Compute R₀ for a
   therapeutic interfering particle"*, AUTO-graded, in **PS9 and the Final**.
   Nothing in the archive supports that. This is the session-6 failure in its
   assessable form and §4 is how to avoid it.
2. **The analytic threshold.** `readings.yaml` s25 assigns Weinberger, Schaffer
   & Arkin 2003 for `the threshold R0_T = P^2 D (1 - 1/R0)` and calls it
   *"the only analytic R0 in the interfering-particle literature, everything
   after it being fitted numerically."* No prior year assigned or cited it, and
   it is the derivation the slide titled *"Engineering R0>1"* has been missing
   since 2016.
3. **P and D as construct-level knobs.** The reading's own focus line asks
   students to say *"what you would have to change in a construct to move each
   one."* The archive never connects R₀ to anything buildable.
4. **The binomial partitioning calculation** (T67). Nothing in any prior deck.
5. **Twenty-one years of follow-through.** `readings.yaml` names Pitchai et al.,
   *Science* 2024 in macaques as what moving P and D produced. The archive stops
   at *"Phase I Clinical Trials by Virxsys"* (Levine 2006) in every year.

**What a prior year did better, and should be taken back:**

- **2018 L20's viral-genetics block.** Fourteen slides on recombination,
  reassortment, complementation, phenotypic mixing and pseudotype formation,
  cut from the 2025 deck. It is where *superinfection*, *co-infection*,
  *helper virus* and *encapsidation* are actually defined — all four are **0**
  in the 2026 decks (§4). 2025 dropped it and kept the conclusion, which is the
  wrong half to keep.
- **2018 L20's two extra discussion questions** (§2.3), cut after 2021. The
  `What are good targets for gene drives?` question with its three-item answer
  list is the only closing question in the lineage that has a checkable answer.
- **The 2024 L26/L27 split.** 2024 taught this material over two meetings and
  2025 compressed it back to one. 2026 also has one meeting, so the 2024 version
  is the better guide to what does not fit.

---

## 3 · What session 23 has already established

Read from `../s23-evolution/DESIGN.md` (24,882 bytes, last changed 2 November
2026). Session 23 is on 12 November, five days before session 24 and seven
before this one, so everything below is fresh.

**Session 23 establishes, and session 25 must build on rather than redefine:**

| idea | how s23 puts it | session 25's use |
|---|---|---|
| **population as the state variable** | s23's own words: *"A population, not a cell."* It calls this *"as large a change of object as the phase plane was in session 8"* and gives it its own slides | **done for you.** Session 25 does not have to make this move again |
| **generations as the clock** | derived at the board from the serial-passage protocol, *"Not minutes"* | reuse the unit |
| **fitness as a growth-rate ratio** | *"Fitness as a growth-rate ratio, and s as its complement"*, arriving out of session 19's measured burden rather than as a definition | reuse |
| **selection coefficient s** | 6 hits, 4 in slide body | reuse. **Do not redefine** |
| **mutation rate μ** | 14 hits, 5 in slide body | reuse. **Do not redefine** |
| **fitness cost** | 3 hits, all speaker notes — so the *phrase* is weak even though the *idea* is strong | safe to use, worth one line of restatement |
| **a mutation–selection ODE with a closed-form solution** | `dq/dt = (1 − q)(s q + μ)`, integrating to `t(q) = ln[(s q + μ)/(μ(1 − q))]/(s + μ)`, with `t₅₀ ≈ ln(s/μ)/s` for `μ ≪ s` | the room will have just solved a two-parameter population ODE in closed form. **An R₀ threshold is easier than that** |
| **the shape of the design lesson** | s23's: *"failure time is logarithmic in the mutation rate and inverse in the selection coefficient"* — 80× on μ against 1.1× on s | session 25's R₀ argument has the same shape and should not be presented as a new kind of result |
| **Cas9 and gRNA as objects** | `Cas9` 16, `gRNA` 10 across s01–s22, plus s23's own kill-switch construct, *"what Ptet drives is Cas9, cutting the host's own genome"* | **the homing endonuclease is already in the room.** A CRISPR gene drive is a Cas9 the students know, aimed at a chromosome |

**Session 23 does NOT establish, despite appearances:** `allele` (0), `diploid`
(0), `heterozygous` / `homozygous` (0/0), `R0` (0), `invasion` (0),
`transcritical` (0). Session 23 is haploid-bacterial throughout. Everything
about sexual inheritance is new ground.

**One hazard.** Session 23's `s` is a *burden* on an engineered strain the
designer wants to keep. Session 25's `s` in a gene drive is a cost the designer
*imposes*, and the drive wins anyway because homing beats selection. Same
symbol, opposite sign of intent, seven days apart. Say so.

---

## 4 · What session 25 must introduce from nothing

From the shared census in
[`../s24-communities/PRIOR-YEARS.md` §4](../s24-communities/PRIOR-YEARS.md).
Zero hits across `decks/s01*.py`–`s23*.py` unless noted.

**Physical objects — these need a picture before any symbol.**

| term | what has to be on the screen |
|---|---|
| **virus / virion** | **0 / 0.** *This course has never shown a virus.* The 2025 deck's influenza schematic — HA, NA, M1, M2, ribonucleocapsid, Ø 70–120 nm — is the slide, and it is already drawn |
| **capsid** | **0.** The Rouzine argument is entirely about capsid as a *shared resource*; the object has to exist first |
| **packaging / encapsidation** | **0 / 0** (`packaging`'s 2 hits are a Python package). The step a DIP competes for |
| **helper virus** | **0.** The 2025 slide 12 definition is usable verbatim: a defective genome *"depends on simultaneous infection with infectious 'helper' virus"* |
| **co-infection / superinfection** | **0 / 0.** The cell containing both. 2018 L20's cut block defines both |
| **defective interfering particle / DIP / TIP** | **0 / 0 / 0.** The session's title objects |
| **diploid / heterozygous / homozygous** | **0 / 0 / 0.** Two chromosomes in a drawing. Gene drives are unintelligible without this and the room is half physicists |
| **allele** | **0.** The thing whose frequency the whole gene-drive argument tracks |
| **homing / gene drive / CRISPR drive** | **0 / 0 / 0** (`gene drive`'s single hit is `one gene driven by X`). Cut → repair-from-the-other-chromosome. The 2016 Bay Nature comic does this in two panels |
| **epidemic / SIR / SEIR** | **0 / 0.** Boxes and arrows. **Do not open with the 17-ODE wall** — it is in the archive and it is the thing to avoid |
| **minimal genome / minimal gene set** | **0 / 0.** Still assigned to this session by T68 — see §5 |

**Mathematical ideas — these need a definition.**

| term | the definition owed, and what it leans on |
|---|---|
| **R₀ / basic reproductive ratio / reproductive number** | **0 / 0 / 0**, and T73 assesses it in PS9 **and the Final**. Secondary infections per primary infection in a wholly susceptible population. The eight-deck precedent of naming it without writing it is exactly what must not be repeated |
| **invasion / invasion threshold** | **0.** `R₀ > 1` as a condition on a rare variant |
| **transcritical** | **0.** The bifurcation at `R₀ = 1`. The room has `bifurcation` (10), `fixed point` (28), `eigenvalue` (20) and `Jacobian` (22) from s08/s09/s11 — the *name* is new, the *object* is not. This is the cheapest new term in the session |
| **super-Mendelian inheritance** | **0.** Transmission above ½, as a number |
| **binomial** | **2 hits, and both are session 2's own forward promise** — see §5. Needs the full statement, not a reintroduction |
| **burst size** | **2 hits, and they mean the wrong thing**: s12's *translational* burst, `geometric with mean k_p/γ_m`. Session 25 must either avoid the phrase or disarm the collision in one explicit sentence |
| **selection coefficient / mutation rate / fitness cost** | **established in s23** (§3). Do not redefine |

---

## 5 · Two live inconsistencies this session inherits

Both are about session 25's own scope, both are in the repository now, and both
have to be settled before a slide is written. Neither is a design proposal —
they are recorded because mining the repo turned them up.

**5.1 Session 2 made session 25 a promise, on a slide and in a note.**
`decks/s02_substrate.py`, the 67–71 min slide, in body text students saw:

> `A plasmid at 5 copies splits binomially: P(one daughter gets none) = 2·(½)⁵
> ≈ 6%. Not asymmetry — counting again, and why low-copy plasmids carry
> partition systems.   → sessions 12, 25`

and in the speaker note: `Session 25 does the full binomial calculation for a
genome; this is the one-line version that makes them want it.`

The forward reference is on the slide, the room has been pointed at this
session by number, and `binomial`'s only two hits in the whole course are that
promise.

**5.2 The coverage matrix still assigns session 25 the minimal-cell
techniques.** `docs/coverage-matrix.md`:

| | | | |
|---|---|---|---|
| T67 | **Binomial genome-partitioning calculation** | S25 (Nov 19) | PS9, Final |
| T68 | Minimal gene set reasoning | S25 | PS9 |
| T73 | Compute *R*₀ for a therapeutic interfering particle | S25 (Nov 19) | PS9, Final |

`docs/deck-triage.md` names S25 *"Minimal and synthetic cells"* in §3 and sends
*"L25 Epidemics → DIPs/TIPs → population-scale design"* to S25 in §2 — the
triage contradicts itself. `course.yaml` says *"Design at population scale"*.
So **three assessed techniques, two of which belong to a different session's
subject, are currently pointed at one 80-minute meeting**, and PS9 is due the
day this session is taught.

This is reported, not resolved. The three ways out are: T67/T68 move elsewhere
and session 2's `→ sessions 12, 25` becomes wrong on a slide already taught;
or the binomial calculation is done here on a *viral genome* — co-infection
multiplicity and segment packaging are binomial, which keeps the promise and
serves the session's own subject; or the session carries all three and is
overloaded. **Whichever is chosen, `decks/s02_substrate.py`'s forward reference
and `docs/coverage-matrix.md` must end up agreeing, and right now they cannot
both be satisfied by a session about DIPs, TIPs and gene drives.**

---

## 6 · Weakest part of this file

**The strongest claim here is a negative one** — that no version of this lecture
derives R₀ — and negatives are the easiest thing to get wrong. What was actually
done: the full text of eight versions was extracted (`pdftotext -layout` for the
PDFs, python-pptx for slide bodies *and* speaker notes for the `.pptx`), grepped
for `R0|R_0|reproductive|reproduction number|threshold|binomial|SIR|burst size|
multiplicity`, and every hit read. Every hit in every year is one of: the
*"TIPS: Engineering R0>1"* slide, the *"multiplicity of infection"* sentence on
the DI-particle definition slide, or the pasted Rouzine caption in a speaker
note. **I then rendered and looked at** 2025 L25 pages 8, 9, 10, 19, 25, 26 and
34 to catch equations living inside images, which is where an R₀ would hide.
I did **not** render every page of every year; a derivation sitting as an image
on a page whose text layer shows none of those words would have been missed.
Settled by rasterising all 39 pages of 2025 L25 and all 52 of 2023 L27 and
looking.

Second: the 2016 `TIPSWeinberger.pdf` is corrupt and unread, so the one paper
this course is known to have handed out on this topic is unidentified.

Third: §3 is read from `s23-evolution/DESIGN.md` only. `NUMBERS.md` in the same
folder (24,833 bytes) was not read, and its §1 and §4 are cited by DESIGN.md as
holding the generations arithmetic and the μ-versus-s ledger. If session 25
reuses s23's numbers rather than its definitions, read that file first.
