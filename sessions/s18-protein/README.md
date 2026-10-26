# Session 18 — Protein circuits: a parameter is manufactured, not found

**Tuesday 27 October 2026.** Part II, third session. Mishra *et al.*, *Science*
2021 was handed out at the close of session 17 and **the room has read it**.
Nothing is due today; PS6 is due Thursday night and PS7 goes out Thursday.

Scope settled by Adam on 25 October. Three documents specified this session and
did not agree — `decks/s02_substrate.py`'s speaker notes said **host context**
(four times), `docs/syllabus.md:396` said **protein circuits**, and
`docs/coverage-matrix.md` said T45/T46/T47. All three are satisfiable, because
they are one session asked from three directions: *what does this medium make
easy that was hard in the last one, and what does it cost?* **The cost, stated:**
scaffolds and recruitment (Dueber 2003/2007, Bashor 2008) are surfaces inside
segment 3, not a segment of their own, for the second year running. Both halves
of the deck changed substantially on 25–26 October; read the deck and
`NUMBERS.md`, not `DESIGN.md`'s account of them.

## The one thing to remember

**A parameter is manufactured, not found.**

Session 9 closed on the slide its own notes call *"THE slide of the lecture"* —
cooperativity is the parameter that most determines bistability and the one you
can least control, and Gardner solved it by **choosing** a repressor that
already dimerises. Today is the answer. A covalent modification cycle reaches an
apparent Hill coefficient of **26** from **one** modification site with **no
cooperative binding anywhere in it**, and the knob that places the switch is
V₁/V₂ — a ratio of two expression levels, which is session 9's *easy* axis.

Thursday's thesis was the same sentence about a **part**. That is what makes
Part II continuous with Part I rather than a change of subject.

And the bill is exact. The half-maximal stimulus is a ratio of (k + ½), so as
the Michaelis constants shrink — which is what buys the sharpness — **the
threshold walks to 1 and stops being yours**. The protein layer buys sharpness
the transcriptional layer cannot; the transcriptional layer still sets the
threshold. **You need both**, which is why today is not an argument for
abandoning promoters.

## What happens

| | |
|---|---|
| **Retrieval** | Two from Thursday — what physically changed when the promoter's number moved, and part identity against part sequence. Then session 9: the toggle needs cooperativity on one arm; where did Gardner *get* his? |
| **1 · The object** | Glycogen phosphorylase, Cori & Green, Krebs & Fischer: one protein, two states, a kinase and a phosphatase both running. The four numbers you may ask of a switch, from Dueber 2007 Fig. 1b. Then the cycle drawn, and **the first conserved total in the course**. Then the knobs, as a question to the room — and the sting that k = K_m/W_T. |
| **2 · The derivation** | Two four-step runs. Michaelis–Menten twice, equal-and-opposite flux, the conservation law, one unknown; then W_T leaves as k and V₂ leaves as a ratio, down to a quadratic in w. Then the authors' Eq. 7 **with its printed typo**, the notation bridge (their capital K is our lowercase k), and the two exact results. |
| **3 · What saturation buys** | The ruler: R, why a hyperbola scores exactly 81, and n = ln81/ln R. Their Fig. 1, then the conserved-pool movie, then why zero order does this. Our apparent-Hill curve. **Session 4's debt discharged, out loud.** Their Fig. 2 and the axis that stops at 12. Then the two routes people have really built — autoinhibition (Dueber) and recruitment (Bashor), with the scaffold vocabulary first and the 2008 erratum after — and the ladder. T44a. |
| **4 · What it costs** | The threshold trade-off. Then: saturate one enzyme and you have almost nothing — **the property belongs to the pair**. Then their Fig. 3, where the authors violate their own scarce-enzyme assumption, and **sequestration** gets named. Then decoy titration, ribosomes and retroactivity as **one mechanism, three sessions**. Then the design ledger, checked against the room's own list. |
| **5 · Mishra 2021** | Topology before biochemistry: Fig. 3A as a logic diagram, recognised as Gardner's wiring. Then why these gates compose at all (phospho in, phospho out), that OR and NOT are functionally complete (session 16's argument, different complete set), how each is built physically, the toggle as pseudocode, and the five deletions. Then Fig. 3B, Fig. 4A, Fig. 4C. Then **the obvious reading and why it fails**, and the line-by-line correspondence with session 9. |
| **6 · The other two media** | The pivot, announced: the rest of the hour is about **materials**, not sharpness. CRISPRi — specificity you can type out, the steric mechanism, and the repression model. T46. Recombinases — the state machine, session 16's latch made physical. T47. |
| **7 · The comparison** | Four media on orthogonality, speed and load, every cell sourced and kinded, **one cell left empty**. Then session 2's question 3, asked on 1 September, answered. T45. |
| **Close** | The thesis, the bill, and the hand-off. **Hand out Ceroni 2015.** |

## The results this session exists to produce

**The theory, and there is not one measurement in it.** Goldbeter, A. &
Koshland, D. E. Jr., *PNAS* **78**(11):6840–6844 (1981). The authors say so on
p. 6844. Their R is the V₁/V₂ to reach 90% modified over the V₁/V₂ to reach 10%;
a Michaelis–Menten response scores exactly **81**, so 81 is the number to beat.

| K₁ = K₂ (their notation; our k) | R | apparent n = ln81/ln R | kind |
|---|---|---|---|
| 10 | 69.546 | 1.036 | computed |
| 1 | 27.150 | 1.331 | computed |
| 0.1 | 3.2400 | 3.738 | computed |
| **0.01** | **1.18355** | **26.077** | **computed** |
| 0.001 | 1.01784 | 248.56 | computed |

`posb.protein.sensitivity_index` solves the steady-state condition twice and
divides; their Eq. 10 is algebra. **The two agree to 5.3 × 10⁻¹⁴ over 35
parameter pairs**, so each confirms the other and the closed form may go on a
slide. Scaling: n ≈ k^−0.92 over k ∈ [0.001, 0.1], and the curve visibly
flattens above that — over the whole plotted axis the slope averages −0.57, so
the surface does not say "across the range".

**Two exact results, both checked numerically on 25 October.**

| | |
|---|---|
| crossing, at V₁/V₂ = 1 | w = k₂/(k₁+k₂) = K_m2/(K_m1+K_m2). With K_m1 = 0.3, K_m2 = 1.7 and W_T swept over nine orders of magnitude, the root holds at **0.850000000000** to twelve figures. **W_T cancels exactly.** |
| half-maximal stimulus | (V₁/V₂)₅₀ = (k₁+½)/(k₂+½). Fed back through the quadratic at four (k₁, k₂) pairs spanning 10⁻⁴ to 10, the worst departure from w = ½ is **1.1 × 10⁻¹³** — root-finder noise. |

Both computed. The deck's surface still says *"checked to 1 × 10⁻⁸"*; that
figure had nothing behind it and `NUMBERS.md` §1 now carries the arithmetic that
replaces it.

**And the pool is a promoter.** With the enzymes held fixed, W_T from 0.1 to
1000 takes the apparent Hill coefficient from **1.04 to 248.6** — because
k = K_m/W_T, so more substrate means *more* saturated, not less. That paragraph
said the opposite until 25 October and the error had reached the knobs slide,
the ledger and the close before the F4.5 review caught it. The pool sets the
sharpness **without moving the crossing**, which is the session's title
delivered rather than asserted.

**What it costs, computed.**

| | |
|---|---|
| reachable threshold at apparent n = 32 | (V₁/V₂)₅₀ ∈ **[0.968, 1.033]** — within 3.3% of 1 either side, whatever affinities are chosen. (The deck's foot rounds to 3.4%; the interval is the verified number.) |
| one enzyme saturated only | k₁ pinned at 0.005, k₂ relaxed from 0.005 to 0.5: apparent n falls from **50.8 to 3.15**. The sharpness is in neither enzyme. |
| nonproductive binding, their Eq. 12 | at ρ₁ = ρ₂ = 1, R = **81 regardless of K₁ = K₂**. A side reaction that binds an enzyme without turning it over destroys the ultrasensitivity completely. |
| enzyme not scarce, their Fig. 3 | at E_T = W_T the swing collapses from 0→1 to about **0.12→0.27**. The authors test their own assumption in the same paper. |

**Two places the paper's prose disagrees with the paper's equation**, both
taught. p. 6841 says K₁ = K₂ = 10⁻² corresponds to a Hill coefficient *"greater
than 13"*; their own Eq. 10 gives **26.08**. And *"R_s = 4.5 corresponds to a
Hill coefficient of 2.9 … the same degree of steepness is obtained … in which
K₁ = K₂ = 10⁻¹"* — but Eq. 10 at K = 0.1 gives R = 3.24, i.e. n = **3.74**.
Fig. 2's n_H axis runs **2 to 12 and stops**, verified 25 October by cropping
the figure and looking at it. **The axis range is a fact; that it explains the
authors' wording is our inference and the paper does not say so** — the surface
offers it as inference.

**A typo in the printed Eq. 7, read off the page at 200 dpi.** The last term
under the square root is printed `+ 4K₂(V₂/V₂ − 1)(V₁/V₂)`. Since V₂/V₂ − 1 = 0
the term vanishes, the discriminant collapses to the squared bracket, and the
formula returns nonsense. **The correct factor is V₁/V₂ − 1** — confirmed twice
over: by rendering p. 6841 and reading it, and because Eq. 8 on the same page
rearranges to exactly `posb.protein._coefficients`, written before the PDF was
in hand, whose −4ac term is +4K₂·u·(u−1). A canonical equation in a canonical
45-year-old paper has a typo, and rederiving from the adjacent equation catches
it. Also: **the "Goldbeter–Koshland function" G(v₁, v₂, J₁, J₂) does not appear
in this paper**, under that name or in that notation. It is a later accretion
from the Tyson/Novák review literature.

**The measured counterparts, and the gap is the point.**

| switch | apparent n_H | mechanism | kind |
|---|---|---|---|
| wild-type yeast mating pathway — Bashor 2008 | 1.12 ± 0.08 (1.21 ± 0.06 in Fig. 4D) | none engineered in | measured |
| negative feedback, Msg5 recruitment | 1.15 ± 0.12 | recruitment | measured |
| positive feedback, Ste50 recruitment | 2.42 ± 0.19 | recruitment | measured |
| **double positive feedback** | **2.84 ± 0.19** | recruitment | measured |
| hemoglobin, via Goldbeter & Koshland 1981 | ≈ 2.9 | cooperative binding, four sites | measured |
| Dueber 2007, three SH3 modules | 2.7 and 2.4 | autoinhibition | measured |
| Dueber 2007, four modules | 3.1 | autoinhibition | measured |
| **Dueber 2007, five modules (A.5.5b)** | **3.9** | autoinhibition | measured |
| one covalent cycle at k = 0.01 | **26.1** | saturation. One site. Nothing cooperative. | **DERIVED** |

Dueber, Mirsky & Lim, *Nat Biotechnol* **25**(6):660–662 (2007): a library of 10
constructs on N-WASP, measured by actin polymerisation over ≥3 experiments; one
module at K_d = 0.1 µM gives n_H = 1.0, the rest are at 10 µM. Their design
trade-off, verbatim: *"Interactions that were too weak led to high background
basal activity … whereas interactions that were too strong led to switches that
were nonactivatable."* Fig. 2c's interdomain cooperativity *"c approaching 100"*
is a **fitted** parameter, not a measurement.

Bashor, Helman, Yan & Lim, *Science* **319**(5869):1539–1543 (2008) — **not**
Horwitz and Peisajovich, who are not on this paper. Feedback strength is set by
leucine-zipper affinity, K_d = **6, 40 and 810 nM**. Dynamics, measured: the
accelerator reaches WT-maximal output in **under 20 min** against **~75 min**
for wild type, the delay circuit waits **~50 min**, and simple negative feedback
adapts after **35 min**. **Fig. 4 was corrected on 22 August 2008 and Science
says exactly how**: in 4B both zippers should have been grey and the
"high affinity" label was wrong; in 4D the positive modulator's zipper should
have been black, with the corrected legend giving **K_d = 6.1 versus 41 nM**.
The erratum also amends running text on pp. 1541 and 1542 and the tables. The
teaching point is that **the uncorrected panel contradicts the mechanism it
illustrates** — the switch works by competitive displacement, so if the two
zippers bound equally nothing would displace anything — and you only find it by
reading to the last page of the PDF. Five months, not four.

Dueber, Yeh, **Chak** & Lim, *Science* **301**(5641):1904–1908 (2003) — third
author is Chak, not Chakraborty; a from-memory citation and the review both had
it wrong, and the PDF was obtained on 26 October after the slide had carried its
two numbers for weeks. K_act for half-maximal activation of the synthetic switch
is **50 µM**, measured, p. 1904. **The two 8 µM are different ligands:** the
Fig. 1 legend's 8 µM is the **intermolecular input peptide** (GVKESLV); the 8 µM
on p. 1906 is the **internal autoinhibitory** PDZ ligand after the authors
tightened it tenfold. `decks/paper_figures.yaml` still says "the PDZ ligand"
without saying which. The AND-gate attribution is the authors' own — and so is
the hedge: the same 8 µM affinity *"was too high to yield AND-gate behavior
(switch C11), whereas in another context this affinity was ideal (switch H14)"*.
**Context dependence inside one 2003 paper**, which is Thursday's thesis
arriving a session early.

**So: theory permits an apparent Hill coefficient of 26 from one site, and the
best measured engineered protein switches reach 2.8–3.9.** That gap is honest —
one is a property of equations, the other of molecules — and it is the question
to leave the room holding.

**The reading.** Mishra, Bepler, Teague, Berger, Broach & Weiss, *Science*
**373**(6550):eaav0780 (2021).

| claim | value | kind |
|---|---|---|
| network size, the paper's own phrase | *"**11** phospho-in and phospho-out signal transduction elements comprising exogenous chimeric fusion proteins and endogenous [components]"* | counted |
| standard characterisation | alternating **30-s** pulses, **59.5-min** pause, n = 100 cells | measured |
| shortest pulse tested | **2.0 s**, against a defective-toggle control | measured |
| nuclear localisation after a 30-s pulse | stabilises by **2 min**, constant over **240 min**, maintained across cell division | measured |
| switching speed | *"within seconds"* | measured, no numeric value published |
| input integration | *"a quasilinear, flux-dependent relationship (concentration multiplied by time)"* | measured |
| the ground cleared first | Δhog1 Δhot1 Δfus3 Δkss1 Δsln1 — **five** genes deleted before anything was built | stated |

**Two corrections to the 2025 deck (L24) that this session inherits.** It said
*"a 15-protein protein-protein network"* — the paper says **11 elements**, and
those elements comprise exogenous fusions *and endogenous components*, so even
"11 proteins" over-reads. And it said transient inputs *"as low as one second"*
— the shortest pulse in the paper is **2.0 s**, and a full-text search finds no
1-s condition.

**"Ultrasensitive" in Mishra does not mean what it means in Goldbeter–Koshland.**
**The paper contains no Hill coefficient at all**; a full-text search for "Hill"
returns nothing. Its claim is about a *detection threshold* — the toggle senses
concentrations *"an order of magnitude lower than concentrations detectable by
the defective toggle network"*, with *"~2% of the cells reproducibly
transitioned"* at the lowest dose. Goldbeter–Koshland's ultrasensitivity is
**steepness**; Mishra's is **threshold**. The deck says which one is meant every
time it says the word.

And the honest close on segment 5: **Mishra's bistability needs the loop, not
saturation alone.** Break the feedback and nothing latches at any dose.
Zero-order is a floor you can build on, not the whole story. Their own
discussion also pays session 9's balanced-strengths requirement in a system with
no promoters in the loop: *"Our engineered toggle's bistability was especially
dependent on the balance between three key protein expression levels."*

**Still not obtained from Mishra:** the input concentrations and the
deletion-background genotypes. The PDF's text layer flattens superscripts and
corrupts µ→m, so the concentration axes have to be read off a rendered page.
Render Fig. 4 before quoting either.

**CRISPRi — T46.** Qi, Larson, Gilbert, Doudna, Weissman, Arkin & Lim, *Cell*
**152**(5):1173–1183 (2013). All measured, in vivo fluorescence, ≥3 biological
replicates: up to **1,000-fold** repression in *E. coli*; 10- to 300-fold on the
nontemplate strand in the coding region; little effect on the template strand;
~**100-fold** at the −35 box; nothing ~100 bp upstream; **12 bp** minimal
base-pairing. Kinetics, Fig. 2E: repression begins within **10 min** and is full
at **240 min**; after washout recovery begins after **50 min** and takes about
**300 min**, by dilution rather than degradation.

> **Not the same guide, and not one guide.** The *E. coli* headline is **two
> sgRNAs combined**, each at about 300-fold, against **mRFP**. The mammalian
> number is a **different guide (eNT2) against a different reporter (EGFP)** —
> **46%** integrated, **63%** from a plasmid, and that 46/63 pair is the paper's
> only same-sgRNA comparison, *within* HEK293. **There is no same-guide
> cross-species comparison in Qi 2013.** The surface says "the same chemistry of
> recognition", never "the same guide" — and what survives is a comparison
> between **media**, which is exactly what session 2 asked for on 1 September.

The repression model on the T46 surface is **ours**, derived from session 6 in
the weak-promoter limit — F_reg = 1/(1 + [dCas9·sgRNA]/K_d), so fold repression
= 1 + [dCas9·sgRNA]/K_d. **Qi 2013 publishes no model**, so it is not attributed
to them, and it is equilibrium occupancy of a *promoter*, which covers their
~100-fold promoter-targeting result and not the coding-region roadblock.
**Burden in Qi 2013 is not quantified** — the paper reports only that dCas9
*"alleviated this lethality"* relative to wild-type Cas9.

**The hand-off to Thursday, said out loud.** Zhang & Voigt, *Nucleic Acids Res*
**46**(20):11115–11125 (2018), all measured in *E. coli*: **530 ± 40** dCas9
molecules per cell before growth or morphology is affected, **9,600 ± 800** for
engineered dCas9*_PhlF (~18×); **30** orthogonal sgRNA–promoter pairs
characterised as NOT gates; and **after 15 sgRNAs are co-expressed the dynamic
range is < 10-fold** — dCas9 falls below 10-fold after **7**, dCas9*_PhlF after
**14**, so the practical ceiling is **~15 gates**. CRISPRi's selling point is
programmable orthogonality, roughly 10⁷ possible pairs. **The medium's headline
advantage is destroyed by resource competition**, which is Thursday's
mathematics arriving a session early as a measured fact.

**Recombinases — T47.** Yang, Nielsen, Fernandez-Rodriguez, McClune, Laub, Lu &
Voigt, *Nat Methods* **11**(12):1261–1266 (2014): **34** integrases predicted
bioinformatically, **13** built, **11** functional, **11** mutually orthogonal
plus FimE and HbiF = **13**; 11 bits = 2,048 states in 2 kb; fastest Int8 under
**2 h**, six at 2–4 h, four at 4–6 h; growth reduced **>25%** only at very high
expression, and *"the majority is non-toxic"*. The switching times are
**whole-circuit** — they *"include the time required to activate the
arabinose-inducible promoter, the expression of the integrase, the switching
rate, and the expression of the GFP reporter"* — so the surface does not say
"the recombinase flips DNA in two hours", and the often-quoted *">90% after 8 h"*
is the assay's **induction window**, not a switching time. Their orthogonality
is different in kind: *"essentially no measureable crosstalk … none had to be
eliminated due to crosstalk."* The cost is the paper's own: recombinase logic is
*"irreversible (once observed, an input signal can never be forgotten)"* and
cannot resolve input order. Reversibility costs a second regulated protein —
Bonnet, Subsoontorn & Endy, *PNAS* **109**(23):8884–8889 (2012): set **>95%**,
reset **>90%**, held over **100+ cell divisions**, with **16 h** pulses and a
shortest working input of ~4 h. *(Single-pass extraction; Fig. 1C's 95/75/55%
are model predictions, not measurements.)* In mammalian cells, Weinberg *et al.*,
*Nat Biotechnol* **35**(5):453–462 (2017): 12 recombinases tested, **10
orthogonal**, **109 of 113 circuits working without optimisation = 96.5%**.

**T45 — four media, three axes, and the column's real content is that the
limits differ in kind.** Transcription factors are limited by operator
cross-reactivity — **16** of 73 mined, 5- to 207-fold (Stanton *et al.*, *Nat
Chem Biol* 10:99–105, 2014), and you screen n². CRISPRi is not limited by
specificity at all; it is limited by **competition for one shared dCas9 pool**.
Recombinases are limited by nothing much. **One of four cells in the load row is
empty and the slide says so** — nobody has measured what a phosphorylation gate
costs its host, and the orthogonality row for phosphorylation is empty for the
same reason. CRISPRi's load cell was filled on 25 October from Zhang & Voigt,
which the first build had wrongly left blank; CRISPRi is the well-characterised
one **because the shared-resource problem forced the field to measure it**, and
that is itself the argument for Thursday.

Two speed citations are deliberately **not** used. **Hooshangi 2005 carries no
per-stage delay number** and must not be cited for one — it is about
steady-state ultrasensitivity and noise propagation; for a measured per-stage
transcriptional delay the right citation is Cheng *et al.*, *ACS Synth Biol*
6:1996 (2017), and only its stated range ("a few to tens of minutes") is
verified. And **Gander *et al.* 2017's 184.9 ± 0.2 min/layer is SIMULATED** — a
regression over simulated response times with four experimental points overlaid
— while its *"effectively zero transcriptional leak"* (L = 0.6 ± 0.1%) is a
model-fit parameter. Its authors are Gander, Vrana, **Voje**, Carothers &
Klavins, not Voigt, who is a different group.

## Coverage

| | |
|---|---|
| T44a | Derive the covalent-cycle steady state; compute the sensitivity index and the apparent Hill coefficient — demonstrated here (segments 2–4), **assessed on PS7 and the Final** |
| T45 | Compare gate families on orthogonality, speed and load — demonstrated here, **assessed on PS8** |
| T46 | CRISPRi repression model — demonstrated here, assessed on PS7 |
| T47 | Recombinase state model / memory element — demonstrated here, assessed on PS7 |

**T44a is new, added 26 October by the F4.6 pass.** PS7's largest autograded
block is the covalent cycle and the sensitivity index, and the audit had no row
for it at all, so eight points were being graded against nothing listed in
`docs/coverage-matrix.md`. **T45 moved to PS8** on the same pass.

**And this session discharges a promise, which is a failure class
`docs/coverage-matrix.md` did not previously track.** `decks/s04_modeling_ii.py:551`
told the room on 8 September that *"zero-order ultrasensitivity in a
phosphorylation cycle gives an apparent n above 20 from ONE site; so does
titration by a decoy. **Both are session 13.**"* `decks/s13_digital.py` contains
zero occurrences of "ultrasensit", "zero-order" and "phosphoryl", and session 13
was taught on 8 October. The claim is true; it lands here instead, eleven days
late, and the session says so on a dark surface rather than letting it pass.
**Decoy titration, the second half of that note, is also taught nowhere** and
gets segment 4's one-mechanism-three-sessions surface. The forward pointer in
s04 should read session 18; s04 is already taught, so that changes nothing a
student heard — it matters because s14 and the final-exam scope document are
built from these sources, and it is offered to Adam as a named line change
rather than made for him.

## Readings

| | |
|---|---|
| Required, read before today | Mishra *et al.*, *Science* 373(6550):eaav0780 (2021) — the phospho-toggle network and its bifurcation analysis, handed out at the close of session 17. Focus line: come able to draw its phase plane on session 8's axes. Published version in `private/readings/`; the PMC copy (PMC11203391) is the submitted version, so do not cite figure numbers from it |
| Optional | none assigned |
| Handed out today, for Thursday | Ceroni, Algar, Stan & Ellis, *Nat Methods* 12(5):415–418 (2015) — the capacity monitor. 4 pp. **The PDF must be in hand before the close**; it is in `private/readings/` |
| Cited, not assigned | Goldbeter & Koshland 1981; Dueber, Yeh, Chak & Lim 2003; Dueber, Mirsky & Lim 2007; Bashor *et al.* 2008 (with its 22 August 2008 erratum); Qi *et al.* 2013; Zhang & Voigt 2018; Yang *et al.* 2014; Bonnet *et al.* 2012; Weinberg *et al.* 2017; Stanton *et al.* 2014; Cheng *et al.* 2017; Gander *et al.* 2017 (cited as a *simulated* number, and for its authorship); Gardner *et al.* 2000 (the session 9 callback); Cori & Green and Krebs & Fischer (named on the opening surface as the discovery) |

## Built

| | |
|---|---|
| Figures | 6 PNGs from `figures/s18_protein.py`, `--verify` clean; **5 placed** — `s18_cycle`, `s18_response_crossing`, `s18_apparent_hill`, `s18_threshold_tradeoff`, `s18_both_saturated`. `s18_response` is built and **not placed**: Goldbeter & Koshland's own Fig. 1 carries the same object and the crossing figure carries the result with the curves attached |
| Movie | `figures/s18_movie.py` → `s18_cycle_sweep.mp4` plus a poster PNG. Two cycles under one sweep of V₁/V₂, disc **area** as the amount in each form, so the two areas sum to a constant on every frame. Generated from `posb.protein`, the same function students call in the notebook. At V₁/V₂ = 1.98 the saturated pair is at 99.0% and the unsaturated one has reached 72.9% |
| Paper figures | **25 declared** in `decks/paper_figures.yaml`, **16 placed**, every crop cut and looked at. Convention settled while cutting them: **crop the plot only and let the deck carry the attribution**, because a journal caption set at 7–8 pt is unreadable projected — an equation crop is the exception, since there the text is the content. Eq. 7 spans both columns of the printed page, which is why `gk1981_eq7_wide` exists. **Defect: `dueber2007_fig2b` is placed on a segment-3 slide and is not declared in the manifest** — the crop is on disk so the build resolves it, but the manifest does not know about it, and `dueber2007_fig2a` is cropped and declared nowhere either |
| Deck | `decks/s18_protein.py` → **62 slides**, clean through `slide_fit` and the prior-year gate. The deck's own `_fig()` refuses a figure that would reach the foot at y = 6.75; `_cell_height()` wraps greedily the way the renderer does, because `theme.text_height` divides characters by characters-that-fit and `theme.text()` maps a bare `size=` up onto the 20 pt content floor — between them that was seven overlapping pairs on the first build, every one short by exactly one line. `_paper()` takes the aspect from the file rather than a box, which was nine small images in large empty slots on the first build, all reported and none visible on the page |
| Handout + answers | `handouts/s18-protein.md` (3 pp PDF) — the same cycle three times with less working each time, fully worked → partly worked → scaffolding gone → the ledger, with a *"why does that step follow?"* at every transition. Answers at `private/handouts/s18-protein-answers.md` (4 pp) |
| Board notes | `private/board-notes/s18-board-notes.md` (4 pp). **Five board moments** — the cycle before anything is modelled and left up all period, the two derivation runs, the sensitivity ruler, and the exchange rate — with ASK / CHECK / IF ASKED / CUT conventions, and the three knobs left in the wing so the design ledger is *checked against them* rather than handed down |

**Each paper is introduced before its results** — goal, construct, measurement —
and the authors' own figure goes up before ours, with the notebook then
reproducing ours. Four of the surfaces exist only because a grep of decks s01–s17
found the room has no vocabulary for them: **"kinase" 0, "phosphatase" 0,
"allosteric" 0, "modulator" 0**, and "Michaelis" 9 — eight of them in s04, seven
weeks ago. So the biology gets its own segment before any algebra, and the
scaffold vocabulary gets a surface before the strongest measured evidence in the
hour.

**What is still open.** The deck has had the F4.5 and F4.6 passes; the one
manifest defect above is unresolved. The load row's phosphorylation cell and the
orthogonality row's phosphorylation cell are empty because no measurement could
be found, and they are a 247 discussion rather than an estimate.
