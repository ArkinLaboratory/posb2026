# Coverage audit — what Fall 2025 taught, and where each piece went

[← back to README](../README.md) · See also [Deck Triage](deck-triage.md) ·
[Coverage Matrix](coverage-matrix.md) · [Project papers](project-papers.md)

**What this is.** [Deck triage](deck-triage.md) audited the 2025 material page by
page and decided which decks survive. It tracked *pages*. This tracks *papers and
topics* — the thing a page count cannot see, because a slide carrying someone
else's figure with no citation line looks identical to a slide carrying your own.

**Method.** All 22 decks in `Classes--PoSB/2025/Lectures` were opened with
`python-pptx` and every text frame, table and speaker note extracted — 1,048
slides. Twenty of those decks are Fall 2025; two (L06, L07, dated 2026-09-16 and
2026-09-18) are this year's and are filed in the same folder. Citation-like lines (an author-year, a journal name or a DOI) were pulled
out mechanically. Topic presence in 2026 was then checked by grep against
`syllabus.md`, `course-map.md` and `coverage-matrix.md`.

**First finding, and it frames everything else.** Across 1,048 slides there are
**69 distinct citation lines**. Five decks — L01, L02, L09, L10 and L12 — carry
no citation at all, and L09/L10/L12 are the parts-and-compositors block, which is
built almost entirely on other people's measurements. The 2025 corpus is not a
reading list with slides attached; it is slides with a reading list mostly
missing. So "what did 2025 cover" cannot be answered from citations alone, and
the topic audit below is the load-bearing half.

---

## 1. Topics with no home in the 2026 syllabus

Checked by grep across the syllabus, course map and coverage matrix. Zero hits
means the word appears nowhere in any of the three.

| Topic in 2025 | Where it lived | Hits in 2026 | Verdict |
|---|---|---|---|
| Karnaugh maps, two-level minimisation, canonical forms | L17, L18 | 1 (a syllabus aside) | **Deliberate cut.** Triage §2 is right: this is EE 101, not synthetic biology. |
| Verilog, netlists, circuit scoring, Eugene | L15–L19 | 0 | **Mostly right to cut**, but S16 keeps Cello, and Cello *is* a netlist compiler. Something has to explain what it compiles. |
| Sequential logic: SR latch, clocked memory, registers | L21 | 0 | **Gap.** S9 builds a toggle, which *is* an SR latch, and never says so. One slide closes this. |
| Analog computation — log, add, ratiometer | L24 | 0 | **Real loss.** See §3. |
| Protein circuits in depth: scaffolds, ultrasensitivity, allosteric switches | L24 (83 slides) | 0 for "scaffold", 0 for "ultrasensit" | **Compressed to one clause** of S18. 83 slides into a clause. |
| Synthetic morphogenesis, organoids, GATA6 symmetry breaking | L24 | 0 | **Real loss.** The only multicellular-development content in the course. |
| Epidemics, defective interfering particles, TIPs, gene drives | L25 (39 slides) | 0 | **Loss by relabelling.** Triage sends L25 to S28 "biosecurity and governance"; the syllabus text for S28 is about screening and governance, not epidemic dynamics. |
| DNA strand displacement (Qian & Winfree) | L15, L16 | 0 | Defensible cut — it is molecular computing, not cellular. |
| miRNA cell classifiers (Xie 2011, Gam 2018) | L13–L16 (3 lectures) | 0 for "miRNA" | **Gap.** S26 says "logic-gated cell therapies, synNotch". The miRNA classifier is the other half and is the one with a model students can build. |

Two of these — analog computation and the DIP/TIP material — are not small.
Together they were about 60 slides of 2025 and they are the two places where the
course's mathematics did something other than gene circuits.

---

## 2. The citation inventory

Every paper cited anywhere in the 2025 decks, with where it lands in 2026.
**R** = in `readings.yaml`. **P** = in [project-papers.md](project-papers.md).
**—** = cited in 2025 and currently nowhere in 2026.

### Carried forward, already placed

| Paper (as cited in 2025) | 2025 deck | 2026 home | |
|---|---|---|---|
| Gardner & Collins, Nature 2000 | L20 | S8, S9 | R P |
| Basu et al., PNAS 2004 | L18, L19 | S10 | R |
| Elowitz & Leibler, Nature 2000 | L09, L15, L21 | S11 | screened — no deposit |
| Nielsen et al., Science 2016 (Cello) | L04, L15–L19 | S16 | superseded by Cello 2.0 (P) |
| Potvin-Trottier et al., Nature 2016 | L21 | S11 | P |
| Gibson 2008/2010; Carr & Church 2009; Stemmer 1995; Weber 2011 (MoClo); Chao, Science 2015 | L08 | S17 | assembly block |
| Endy, Science 2008 (genome reconstruction); JCVI-syn3.0 | L08 | S17, S25 | |
| Fuqua et al., Nat Rev MCB 2002 (quorum sensing) | L18, L19 | S24 | review |
| Canton et al., Nat Biotech 2008 (datasheets); Kelly et al., JBE 2009 | L04, L05 | S13, S17 | screened — figures only |

### Cited in 2025, no home in 2026

These are the ones worth a decision. Each was on a slide in front of the room
last year.

| Paper | 2025 deck | What it gives | Where it would go |
|---|---|---|---|
| **Hooshangi et al., PNAS 2005** | L03, L04, L13 | Noise propagation through a 3-stage transcriptional cascade — measured, with an ultrasensitivity model | **S12 or S13.** The single best fit for the noise gap. |
| **Xie et al., Science 2011** | L04, L13–L16 | The HeLa miRNA classifier: a truth table implemented in a cell | **S26**, and the strongest project source in the set |
| **Gam et al., Nat Comm 2018** | L13–L15 | Antagonistic/synergistic miRNA repression model; classifier optimisation over a design space | S26 |
| **Daniel, Rubens, Sarpeshkar & Lu, Nature 2013** | L24 | Analog log, addition and ratiometer circuits — wide dynamic range from few parts | nowhere; see §3 |
| **Mishra et al., Science 2021** | L24 | A toggle built from protein phosphorylation, not transcription | **S18**, and it is the natural bookend to S9 |
| **Bashor et al., Science 2008**; Dueber 2003/2007; O'Shaughnessy, Cell 2011 | L24 | Scaffold-tuned feedback: same network, gain set by recruitment | S18 |
| **Sprinzak et al., Nature 2010** | L24 | Notch cis-inhibition producing a sharp boundary — reconstituted, with a simple model | S24 or S26 |
| **Guye et al., Nat Comm 2016** | L24 | Programmed organoid formation from GATA6 symmetry breaking | nowhere |
| **Tanner, Kirkegaard & Weinberger, PLoS Genet 2016**; Frensing & Heldt, PLoS One 2013 | L25 | Therapeutic interfering particles; R₀ engineered above 1 | S28, if S28 keeps epidemic dynamics |
| **Fung et al., Nature 2005** (metabolator) | L21 | A metabolic oscillator — oscillation from flux, not repression | S11 or S20 |
| **Atkinson et al., Cell 2003**; Danino 2010; Prindle 2012; Chen, Science 2015 | L21 | Relaxation oscillator; synchronised quorum oscillators; two-strain consortium oscillator | S11, S24 |
| **Chen et al., Nat Methods 2013** (terminators) | L15–L17 | 582 characterised terminators | S17, beside Cambray |
| **Lou et al., Nat Biotech 2012**; Stanton, Nat Chem Biol 2014; Nielsen & Voigt, MSB 2014; Fernandez-Rodriguez, ACS SB 2015 | L15–L17 | Insulation; repressor libraries; CRISPRi circuits; invertase memory | S16, S17, S18 |
| **Qian & Winfree, Science 2011** | L15, L16 | DNA strand-displacement cascades | nowhere — defensible |
| **Miller et al., PLoS Comp Biol 2012** (GRO); Jang, ACS SynBio 2012 | L04, L05 | A cell-programming language and simulator | nowhere |

---

## 3. The three judgement calls

Everything above is inventory. These three are decisions.

**Analog computation.** Daniel et al. 2013 is the only place in either year's
course where a circuit computes a continuous function rather than a Boolean one,
and it does it with a handful of parts because it exploits the physics instead of
fighting it — the log of a concentration falls out of the Hill function you
already derived in session 4. The 2026 course derives that Hill function three
times and never once shows it being used as arithmetic. Cutting this leaves the
implicit claim that engineering a cell means making it digital, which the course
elsewhere spends a session (S13) arguing is a costly abstraction. **Recommend
restoring it**, as half of S13 or as a named block in S16.

**Protein circuits.** L24 was 83 novel pages and is now a clause. The specific
loss is not "protein circuits exist" but ultrasensitivity — zero-order,
multi-step, the sharpening that makes a switch switch. S9 asserts that the
toggle needs cooperativity and PS4 Q3 makes students find that n = 1 fails; the
protein material is where cooperativity gets built rather than assumed.
**Recommend** Mishra 2021 as S18's anchor paper, since a protein-level toggle
makes S9's analysis portable, and keeping Bashor 2008 for the gain argument.

**Epidemics and TIPs.** This one is a genuine choice about what the course is.
It is the only material that leaves the single cell and the single population and
asks about transmission — and the model is a page of algebra with a threshold in
it, which is exactly the kind of thing this course teaches well. It also sits
next to the biosecurity session's real subject. **Recommend** either that S28
explicitly takes the epidemic dynamics (not just governance), or that it is cut
honestly rather than absorbed by a relabelling.

---

## 4. What this does to the project-paper list

[project-papers.md](project-papers.md) was built forward — from the 2026 topic
list and a literature search — and it therefore missed the papers this course
actually teaches from. That is a defect in how it was made, not a close call.
Six additions, in priority order:

1. **Hooshangi et al., PNAS 2005** — closes the noise gap named in that file.
2. **Xie et al., Science 2011** — the miRNA classifier; a truth table in a cell.
3. **Mishra et al., Science 2021** — S9's analysis at the protein level.
4. **Daniel et al., Nature 2013** — analog computation; small model, large idea.
5. **Chen et al., Nat Methods 2013** — 582 terminators, beside Cambray.
6. **Tanner et al., PLoS Genet 2016** — TIPs; an R₀ argument.

Each still needs the deposit check that the other twenty passed, and none is in
that file until it does.

**A harder problem the archive exposes.** `PoSB Term Project Examples/PoSB
Project ideas.xlsx` lists 32 project titles from 2014. Nearly every one is a
*design* — a mucus-degrading bacterium for cystic fibrosis, a bistable switch
for an oil-spill microbe, a relaxation oscillator to regenerate cartilage, a
cell classifier for hepatocellular carcinoma. Almost none is "extend the analysis
in an excellent paper," which is what the syllabus advises and what the whole
paper list is built to support. Either the advice has never been followed, or it
is aspirational and the real assignment is design. That matters for the new
milestone: a list of papers serves re-analysis projects well and design projects
only as a source of parameters. If the projects students actually want to do are
designs, the first milestone should ask for a paper *and the design it suggests*,
and the list needs a column saying what each paper gives you to design **with**.

---

*Method note. Slide text extracted 20 September 2026 from the 22 decks in
`Classes--PoSB/2025/Lectures` (1,048 slides). Citation lines were matched
mechanically and are a lower bound — uncited figures are invisible to this
method, and L09, L10 and L12 contain many. Topic presence in 2026 was checked by
case-insensitive grep against `docs/syllabus.md`, `docs/course-map.md` and
`docs/coverage-matrix.md`; a zero in the table means zero hits in all three.
Citations are reproduced as the 2025 slides give them and have **not** been
verified against publisher records — several are partial (no volume, no page).
Verify before any of them reaches a syllabus.*
