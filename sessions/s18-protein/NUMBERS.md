# Session 18 — every number, with its source and its kind

Companion to `DESIGN.md`. **No number goes on a surface unless it is in this
table with a kind attached.** `figures/README.md`'s rule, and three of week 9's
worst defects were a correct number with the wrong kind on it.

Verified 19 October, and **re-verified the same day against the PDFs Adam
supplied** — every paper named here is now in `private/readings/`. Where
something is still unverified it says so.

---

## 1 · Goldbeter & Koshland 1981 — the derivation

Goldbeter, A. & Koshland, D. E. Jr. "An amplified sensitivity arising from
covalent modification in biological systems." *PNAS* **78**(11):6840–6844
(1981).

> ⚠️ **Every number in this paper is computed. There is not one measurement in
> it.** The authors say so, p. 6844: *"It should be emphasized that the data are
> not yet available to say with certainty that this device for added sensitivity
> is actually utilized in biological systems, although preliminary observations
> on phosphorylation systems in our laboratory are encouraging."* A slide
> calling any of this "measured" is the defect we are guarding against.

**Their sensitivity measure**, p. 6841, verbatim: *"The analogous quantity R_v
is defined as the ratio of V₁/V₂ when 90% of the protein is in the modified
form to V₁/V₂ when 10% is in the modified form."*

**Their Eq. 10** — a closed form for it:

    R_v = 81 (K₁ + 0.1)(K₂ + 0.1) / [(K₁ + 0.9)(K₂ + 0.9)]

**Their Eq. 8**, the implicit steady state — this is the one for the slide:

    V₁/V₂ = W*(1 − W* + K₁) / [(1 − W*)(W* + K₂)]

**Their Eq. 9**, the V₁ = V₂ case: `W* = K₂/(K₁ + K₂)`.

**Their parameter definition**, p. 6841, verbatim: *"K₁ and K₂ are the
respective Michaelis constants K_m1 and K_m2 divided by W_T."*

**The Michaelian value**, p. 6841, verbatim: *"In the limiting case when K₁ and
K₂ are much greater than 1, the value of R_v is 81, exactly the same as the
ratio of the ligand concentrations needed to go from 10% to 90% saturation of a
Michaelis–Menten protein."*

**Their definition of the regime, verbatim from the same page** — the sentence
to put on the slide that names the thing: the response is *"**zero-order** in
the protein substrate, which saturates the enzyme surface, and **ultrasensitive**
because it is more sensitive than a Michaelis–Menten response to stimulus."*

**And their normalisation, verbatim:** *"V₁ = k₁E_1T, V₂ = k₂E_2T,
K₁ = (d₁+k₁)/(a₁W_T) = K_m1/W_T … Note that K₁ and K₂ are the respective
Michaelis constants K_m1 and K_m2 divided by W_T."* Also: *"we shall use W and
W* to indicate mole fractions — i.e., [W]/W_T and [W*]/W_T."* `posb.protein`
uses exactly these conventions.

### Cross-check: their closed form against our root-finder

`posb.protein.sensitivity_index` solves the steady-state condition twice and
divides. Their Eq. 10 is algebra. **The two agree to 5.3 × 10⁻¹⁴ over 35
parameter pairs**, so each confirms the other and the closed form can go on a
slide.

| K₁ = K₂ | R_v | apparent Hill n = ln81/ln R_v | kind |
|---|---|---|---|
| 10 | 69.546 | 1.036 | computed |
| 1 | 27.150 | 1.331 | computed |
| 0.1 | 3.2400 | 3.738 | computed |
| **0.01** | **1.18355** | **26.077** | computed |
| 0.001 | 1.01784 | 248.56 | computed |

### The two exact results, checked numerically — 25 October

Neither had an entry here before today, and the second surface carried a
tolerance ("checked to 1 × 10⁻⁸") with nothing behind it. Both now checked.

**Crossing at V₁/V₂ = 1.**  w = k₂/(k₁+k₂) = K_m2/(K_m1+K_m2), independent of
the pool. With K_m1 = 0.3, K_m2 = 1.7 and W_T swept over nine orders of
magnitude (10⁻³ to 10⁶), the root stays at **0.850000000000** to twelve
figures against the predicted 0.85. | kind: computed

**Half-maximal stimulus.**  (V₁/V₂)₅₀ = (k₁+½)/(k₂+½). Fed the predicted
ratio back into the quadratic and solved for w at four (k₁, k₂) pairs
spanning 10⁻⁴ to 10 — (0.01, 0.01), (10, 1), (0.3, 1.7), (10⁻⁴, 5×10⁻³).
Worst departure from w = ½ is **1.1 × 10⁻¹³**, which is root-finder noise.
| kind: computed

So the slide's claim of exactness is supported and the 10⁻⁸ figure can be
replaced by the arithmetic whenever that surface is next touched.

### Two places the paper's prose disagrees with the paper's equation

Both worth teaching, under the standing rule about showing the evolution of the
logic.

1. p. 6841, verbatim: *"A covalent modification scheme having the constants
   K₁ = K₂ = 10⁻² would correspond in sensitivity to the saturation curve of a
   cooperative protein with a Hill coefficient **greater than 13**."* Their own
   Eq. 10 gives **26.08**. The statement is true and weak by a factor of two.
2. p. 6841, verbatim: *"A value of R_s = 4.5 corresponds to a Hill coefficient
   of 2.9 … The same degree of steepness is obtained by a reversible covalent
   modification system in which K₁ = K₂ = 10⁻¹."* R_s = 4.5 ↔ n_H = 2.92 ✓, but
   Eq. 10 at K = 0.1 gives R_v = **3.24**, i.e. n_H = **3.74**, not 2.9.

**Lesson: evaluate the closed form; do not read the value off the figure.**

Fig. 2's n_H axis runs **2 to 12 and stops** — verified 25 Oct by cropping the
figure and looking at it (`private/paper-figures/gk1981_fig2.png`). At
K₁ = K₂ = 10⁻² the K₁ = K₂ curve bottoms near R ≈ 1.2, which on the dashed R_s
curve lies past the right-hand edge. So ">13" is where their graph ran out.
**The axis range is verified; that it explains the authors' wording is our
inference and the paper does not say it** — offer it as inference or leave it
out.

### A typo in the printed Eq. 7 — read off the page at 200 dpi

**Verified from the PDF, not relayed.** `private/readings/Session 18 -
goldbeter-koshland-1981-amplified-sensitivity-INSTRUCTOR.pdf`, page 6841, Eq. 7:
the discriminant's last term is printed

    + 4K₂(V₂/V₂ − 1)(V₁/V₂)

The rendered page really does read **V₂/V₂** in that factor; the crop is saved
as `private/paper-figures/gk1981_eq7.png` and can go straight on a slide. Since
V₂/V₂ − 1 = 0 the term vanishes, the discriminant collapses to the squared
bracket alone, and the formula returns nonsense. **The correct factor is
V₁/V₂ − 1.**

**Confirmed independently, twice over.** Eq. 8 on the same page reads

    V₁/V₂ = W*(1 − W* + K₁) / [(1 − W*)(W* + K₂)]

which rearranges to `(1−u)w² + [u(1−K₂) − 1 − K₁]w + uK₂ = 0` with u = V₁/V₂ —
**exactly `posb.protein._coefficients`**, written before the PDF was in hand.
Its −4ac term is +4K₂·u·(u−1), matching the corrected factor and not the printed
one.

A canonical equation in a canonical 45-year-old paper has a typo, and rederiving
from the adjacent equation catches it. That is a better lesson about reading
primary literature than the equation is — and the slide can show the page.

### Nomenclature

**The "Goldbeter–Koshland function" G(v₁, v₂, J₁, J₂) does not appear in this
paper**, under that name or in that notation. It is a later accretion from the
Tyson/Novák review literature. The 1981 paper has Eq. 7 and Eq. 8 only. Do not
write "Goldbeter & Koshland define G(…)".

### The failure mode worth a surface

Eq. 12 covers nonproductive binding. p. 6842, verbatim: *"Eq. 12 shows that for
ρ₁ = ρ₂ = 1, the ratio R_v is equal to 81 regardless of the value of K₁ = K₂."*
**A side reaction that binds an enzyme without turning it over destroys the
ultrasensitivity completely**, whatever the saturation. Computed.

---

## 2 · Mishra et al. 2021 — read from the PDF in `private/readings/`

Mishra, Bepler, Teague, Berger, Broach & Weiss, *Science* **373**(6550):
eaav0780 (2021).

| claim | value | kind |
|---|---|---|
| network size, the paper's own phrase | *"built from **11** phospho-in and phospho-out signal transduction elements comprising exogenous chimeric fusion proteins and endogenous [components]"* | counted |
| organism | *S. cerevisiae* | — |
| inputs | isopentenyl adenine (IP) and sorbitol | — |
| standard characterisation | alternating **30-s** pulses, **59.5-min** pause between them, n = 100 cells | measured |
| shortest pulse tested | **2.0 s**, against a defective-toggle control | measured |
| switching speed | *"within seconds"* | measured, no numeric value given |
| input integration | *"followed a quasilinear, flux-dependent relationship (concentration multiplied by time)"* | measured |
| bistability | long-term, across cell divisions | measured |

> ⚠️ **Two corrections to the 2025 deck (L24), which this session inherits.**
>
> 1. It says **"a 15-protein protein-protein network."** The paper says **11
>    elements**, and those elements comprise both exogenous chimeric fusions
>    *and endogenous components* — so "11 proteins" would also be an
>    over-reading. Use the paper's phrase.
> 2. It says transient inputs **"as low as one second."** The shortest pulse in
>    the paper is **2.0 s**. Searching the full text for a 1-s condition returns
>    nothing.

> ⚠️⚠️ **"Ultrasensitive" in Mishra does NOT mean what it means in
> Goldbeter–Koshland, and putting them on one slide under one word would be a
> false equivalence.**
>
> **The paper contains no Hill coefficient at all** — a full-text search for
> "Hill" returns nothing. Its ultrasensitivity claim is about a *detection
> threshold*, verbatim: *"a population of toggle cells exhibited
> ultrasensitivity and were able to sense input concentrations an order of
> magnitude lower than concentrations detectable by the defective toggle
> network"*, with *"~2% of the cells reproducibly transitioned from the off to
> the on state"* at the lowest concentration.
>
> Goldbeter–Koshland ultrasensitivity is **steepness**. Mishra's is
> **threshold**. Say which one is meant, every time.

**The session 9 callback, from the paper's own discussion**, verbatim: *"Our
engineered toggle's bistability was especially dependent on the balance between
three key protein expression levels."* That is session 9's *balanced strengths*
requirement, in a system with no promoters in the loop.

**Still not obtained:** the input concentrations (the PDF's text layer flattens
superscripts and corrupts µ→m, so the concentration axes must be read off a
rendered page, not scraped), and the deletion-background genotypes. Render Fig.
4 before quoting either.

---

## 2b · Dueber, Yeh, Chak & Lim 2003 — the allosteric switch, T45 slide

✅ **PDF obtained 26 October** and in `private/readings/`. It had been used on
a slide for weeks with no entry here and no PDF — the F4.5 review caught it.
The two numbers on deck p29 and in `decks/paper_figures.yaml` are **both
correct**, now verified against the paper.

**Citation.** Dueber JE, Yeh BJ, **Chak K**, Lim WA. *Reprogramming control of
an allosteric signaling switch through modular recombination.* **Science
301**(5641):1904–1908 (26 September 2003). doi:10.1126/science.1085945.
PMID 14512628. (Third author is **Chak**, not Chakraborty — both a from-memory
citation and the review got that wrong.)

| quantity | value | kind | where |
|---|---|---|---|
| K_act, peptide for half-maximal activation of the synthetic switch | **50 µM** | **measured** | p. 1904, Fig. 1 legend and body |
| K_d of the intermolecular PDZ ligand (GVKESLV) | **8 µM** | **measured** | p. 1904, Fig. 1 legend |
| K_PDZ of the *internal* autoinhibitory ligand in switch H14 | **8 µM**, ~10-fold tighter than the parent | **measured** | p. 1906 |
| switch concentration in every assay | 50 nM | stated | p. 1904, Fig. 1 legend |

Verbatim, p. 1904: *"Peptide concentration required for half-maximal
activation (Kact) is 50 µM."* and *"Half-maximal activation (Kact) required
50 µM input."* Ligand, same page: *"NH2-GVKESLV-COOH; Kd = 8 µM."*

⚠️ **The two 8 µM are different ligands.** The Fig. 1 legend's 8 µM is the
**intermolecular** input peptide. The p. 1906 8 µM is the **internal,
autoinhibitory** PDZ ligand after the authors tightened it tenfold. A surface
that says "the PDZ ligand's K_d is 8 µM" without saying which is ambiguous;
`decks/paper_figures.yaml` currently does exactly that. Say *input peptide*
or *internal ligand*.

✅ **The AND-gate attribution is the paper's own**, not ours. p. 1906:
*"increasing the affinity of the internal PDZ ligand by ~10-fold (KPDZ = 8
µM) within the same architecture yielded a well-behaved AND gate (switch
H14)."* Note the hedge worth keeping: *"in one architectural context, the 8
µM PDZ affinity was too high to yield AND-gate behavior (switch C11), whereas
in another context this affinity was ideal (switch H14)."* So AND-gate
behaviour is **context-dependent even within this paper** — which is the s17
thesis arriving a session early, and worth one sentence in the room.

---

## 3 · Measured ultrasensitivity in engineered protein circuits

These are the measured counterparts to Goldbeter–Koshland's computed numbers,
and the gap between them is the engineering point.

**Dueber, Mirsky & Lim, *Nat Biotechnol* 25(6):660–662 (2007).** N-WASP output
domain recombined with one to five SH3 autoinhibitory modules. **Library of 10
constructs** (Fig. 2a, counted).

| switch | SH3 modules | K_d | measured n_H |
|---|---|---|---|
| A.1.1a | 1 | 0.1 µM | 1.0 |
| A.3.3b | 3 | 10 µM | 2.7 |
| A.5.3b | 3 | 10 µM | 2.4 |
| A.5.4b | 4 | 10 µM | 3.1 |
| **A.5.5b** | **5** | **10 µM** | **3.9** |

All **measured** (actin polymerisation, ≥3 experiments). Verbatim, p. 661:
*"a construct with five SH3 autoinhibitory modules (switch A.5.5b) was
completely repressed under basal conditions, but was activated with an apparent
Hill coefficient of 3.9."*

The design trade-off, verbatim p. 661: *"Interactions that were too weak led to
high background basal activity … whereas interactions that were too strong led
to switches that were nonactivatable."* Design-ledger entry.

> ⚠️ Fig. 2c is **model** curves with measured points overlaid; the interdomain
> cooperativity *"c approaching 100"* is a **fitted** parameter. Do not present
> Fig. 2c as a measurement.

**Bashor, Helman, Yan & Lim, *Science* 319(5869):1539–1543 (2008).**
⚠️ **Author list corrected** — not Horwitz and Peisajovich, who are not on this
paper. Modulators recruited to the Ste5 scaffold by leucine zippers.

| circuit | measured n_H |
|---|---|
| wild type | 1.12 ± 0.08 |
| positive feedback (Ste50 recruitment) | 2.42 ± 0.19 |
| negative feedback (Msg5 recruitment) | 1.15 ± 0.12 |
| double positive feedback | **2.84 ± 0.19** (vs WT 1.21 ± 0.06) |

Dynamics, measured: accelerator reaches WT-maximal output in **<20 min** against
**~75 min** for WT; delay circuit waits **~50 min**; simple negative feedback
adapts after **35 min**. Feedback strength set by zipper affinity,
**K_d = 6, 40, 810 nM**.

> ⚠️ **Fig. 4 was corrected, and Science says exactly how.** The PDF's first
> line reads *"CORRECTED 22 AUGUST 2008; SEE LAST 2 PAGES"*. The erratum is
> **pages 6–7** — page 6 is the text, page 7 the reissued panels, page 8 is
> AAAS boilerplate. An earlier version of this note said "Science states no
> reason" and marked panel B "[unverified]"; that was wrong, and it was wrong
> because only page 7 had been read. Corrected 25 Oct.
>
> **Verbatim, p. 6:** *"There were two errors in Fig. 4 in describing the
> precise components used to construct specific circuits. In Fig. 4B, the
> leucine zippers attached to both the negative and positive modulators should
> have both been colored gray, since both modulators were fused to identical
> zippers (rather than to zippers with different affinity). The label was also
> incorrect: The resulting negative modulator does not bind with high affinity.
> In Fig. 4D, the leucine zipper attached to the positive modulator should have
> been colored black, since this modulator was fused to a zipper with higher
> affinity than the zipper (colored gray) fused to the negative modulator. The
> zipper is now black and 'high-affinity' has been added to the label."*
>
> It also corrects **three pieces of running text** — p. 1541 (delete "high
> affinity"), p. 1542 (insert "higher affinity"), and the Fig. 4 legend, whose
> corrected form reads *"Negative modulator is displaced by inducibly expressed
> positive modulator fused to a higher-affinity zipper (**K_d = 6.1 versus
> 41 nM**)"* — and states that the same errors are corrected in fig. S3 and
> tables S1 and S2.
>
> **Teaching value:** the uncorrected panel D contradicts the mechanism it
> illustrates. The switch works by competitive displacement, so if the two
> zippers bound equally nothing would displace anything. The measured numbers
> above are unaffected. Crops: `bashor2008_fig4b_corrected`,
> `bashor2008_fig4d_corrected`. Elapsed: published 14 March 2008, corrected
> 22 August 2008 — **five months**, not four.

**So: theory permits an apparent Hill coefficient of 26 from one site; the best
measured engineered protein switches reach 2.8–3.9.** That gap is a real
question to leave the room with, and it is honest — one is a property of
equations, the other of molecules.

---

## 4 · CRISPRi — T46

**Qi, Larson, Gilbert, Doudna, Weissman, Arkin & Lim, *Cell* 152(5):1173–1183
(2013).** All measured, in vivo fluorescence, ≥3 biological replicates.

| result | value |
|---|---|
| headline, *E. coli* | up to **1,000-fold** repression |
| nontemplate strand, coding region | 10- to 300-fold |
| template strand, coding region | little effect |
| promoter targeting at the −35 box | ~100-fold |
| ~100 bp upstream of the promoter | no effect |
| two sgRNAs at ~300-fold each, combined | up to 1,000-fold |
| minimal base-pairing for silencing | 12 bp |
| **mammalian (HEK293), guide eNT2 vs EGFP** — a DIFFERENT guide and a different reporter from the *E. coli* rows above | **46% repression** integrated; **63%** from a plasmid. The 46/63 pair is the paper's only same-sgRNA comparison, and it is within HEK293. |

Position dependence, verbatim p. 1177: *"repression was inversely correlated
with the target distance from the transcription start site … A strong linear
correlation was observed for mRFP."* Strand dependence disappears for promoter
targets, verbatim p. 1176: *"targeting of template or nontemplate strands is
equally effective."*

Kinetics, Fig. 2E, measured — **the speed-axis numbers**: repression begins
within **10 min**, reaches full at **240 min**; after washout, recovery begins
after **50 min** and takes about **300 min**, by dilution rather than
degradation.

> ⚠️ **NOT the same sgRNA, and not one guide.** Corrected 25 Oct after reading
> the paper: the *E. coli* headline is **two sgRNAs combined**, each at about
> 300-fold, against **mRFP** — verbatim, *"Combining two sgRNAs—each with about
> 300-fold repression—allowed us to increase the overall silencing to up to
> 1,000-fold."* The mammalian number uses a **different guide (eNT2) against a
> different reporter (EGFP)** — verbatim, Fig. 7A, *"Cotransfection of dCas9 and
> an sgRNA (eNT2) that targets the nontemplate DNA strand of EGFP decreases
> fluorescence (~46%)."* The paper's only "same sgRNA" sentence compares
> integrated against plasmid delivery **within HEK293** (46% vs 63%). There is
> **no same-guide cross-species comparison in Qi 2013.** Say "the same chemistry
> of recognition", never "the same guide". The table above is kept for the
> comparison it does support — between MEDIA — and that is
> session 2's question 3 — *why does the same circuit behave differently in a
> bacterium and in a human cell, before you change anything?* — answered with a
> measured number, from the room's own instructor's paper. This is the surface
> that pays off session 2's promise.

**Burden in Qi 2013: not quantified.** The paper reports only that dCas9
*"alleviated this lethality"* relative to wild-type Cas9 (Figs. S2A/S2B). It
establishes that dCas9 is *less* toxic, not that it is free.

---

## 5 · Load, and the bridge into session 19

**Zhang & Voigt, *Nucleic Acids Res* 46(20):11115–11125 (2018).** Open access,
all measured in *E. coli*.

| result | value |
|---|---|
| max dCas9 per cell before growth or morphology is affected | **530 ± 40 molecules** |
| same for engineered dCas9*_PhlF | **9,600 ± 800** (~18×) |
| orthogonal sgRNA–promoter pairs characterised as NOT gates | **30** |
| **dynamic range after 15 sgRNAs are co-expressed** | **< 10-fold** |
| per variant | dCas9 falls below 10-fold after **7**; dCas9*_PhlF after **14** |
| practical ceiling on dCas9 gates | **~15** |

Verbatim, the sentence for the slide: *"A set of 30 orthogonal sgRNA–promoter
pairs are characterized as NOT gates; however, the simultaneous use of multiple
sgRNAs leads to a monotonic decline in repression and after 15 are co-expressed
the dynamic range is <10-fold."*

And from the Discussion: *"This is about on par with the number of available
protein-based gates and is a harsh limitation to the huge number of potential
gates considering sgRNA programmability alone."*

> **This is the hand-off to session 19 and it should be said out loud.**
> CRISPRi's selling point is programmable orthogonality — roughly 10⁷ possible
> sgRNA–promoter pairs, specificity set by base pairing rather than by protein
> evolution. Thirty are characterised. Co-express fifteen and the dynamic range
> collapses, because they all draw on one dCas9 pool. **The medium's headline
> advantage is destroyed by resource competition**, which is Thursday's
> mathematics, arriving a session early as a measured fact.

---

## 6 · Recombinases — T47

**Yang, Nielsen, Fernandez-Rodriguez, McClune, Laub, Lu & Voigt, *Nat Methods*
11(12):1261–1266 (2014).**

| result | value | kind |
|---|---|---|
| integrases predicted bioinformatically | 34 | counted |
| built and tested | 13 | counted |
| functional | 11 of 13 | measured |
| **mutually orthogonal** | **11**, plus FimE and HbiF = **13** | measured |
| memory capacity | 11 bits = 1.375 bytes, 2,048 states, in 2 kb | counted |
| switching | **>90% after 8 h** | measured |
| speed | fastest Int8 **<2 h**; six 2–4 h; four 4–6 h | measured |
| growth cost | reduced **>25%** only at very high expression; *"the majority is non-toxic"* | measured |

Honesty note, verbatim: the switching times *"include the time required to
activate the arabinose-inducible promoter, the expression of the integrase, the
switching rate, and the expression of the GFP reporter."* **Whole-circuit, not
the recombination step.** Do not say "the recombinase flips DNA in two hours."

Why the orthogonality is different in kind, verbatim: *"The recombinases
demonstrate exquisite orthogonality, with essentially no measureable crosstalk …
All 11 integrases that were functional were also highly orthogonal and none had
to be eliminated due to crosstalk."*

The cost, verbatim: *"Logic operations based solely on recombinases are
irreversible (once observed, an input signal can never be forgotten) and are
thus unable to resolve the order or co-occurrence of input signals."*

**Reversibility, Bonnet, Subsoontorn & Endy, *PNAS* 109(23):8884–8889 (2012)**
— Bxb1 integrase plus gp47 excisionase. Set **>95%**, reset **>90%**, held over
**100+ cell divisions**, all measured; pulses were **16 h**, shortest working
input ~4 h. The price of reversibility is a second regulated protein, hours-long
timescales, and a stochastic distribution of states rather than a clean flip.
*(Single-pass extraction; re-check before release. Fig. 1C's 95%/75%/55% are
model predictions, not measurements.)*

**Weinberg et al., *Nat Biotechnol* 35(5):453–462 (2017), BLADE** — mammalian.
12 recombinases tested, **10 orthogonal**; **109 of 113 circuits worked without
optimisation = 96.5%**, measured. The strongest quantitative argument that
recombinase logic needs less tuning than TF logic.

---

## 7 · The comparison table — T45

**Orthogonality (mutually orthogonal members demonstrated)**

| family | number | source | kind |
|---|---|---|---|
| transcription factor | **16** of 73 mined, 5- to 207-fold | Stanton et al., *Nat Chem Biol* 10:99–105 (2014) | measured |
| CRISPRi | **30** characterised, **~15** usable at once | Zhang & Voigt 2018 | measured |
| recombinase | **13** (11 integrases + 2 invertases); 10 of 12 in mammalian cells | Yang 2014; Weinberg 2017 | measured |
| protein phosphorylation | **no measurement exists** that could be found | — | — |

**The column's real content is that the three limits are different in kind**, and
the table should say so rather than just ranking the numbers:

- **TF** — limited by operator cross-reactivity. 73 mined gives 16. You screen n².
- **CRISPRi** — *not* limited by specificity at all; base pairing gives ~10⁷
  possible pairs. Limited by **competition for one shared dCas9 pool**.
- **Recombinase** — limited by nothing much. None were eliminated for crosstalk.

**Speed**

| family | value | source | kind |
|---|---|---|---|
| TF, single stage, *E. coli* | "a few to tens of minutes" | Cheng et al., *ACS Synth Biol* 6:1996 (2017) | measured (range only verified) |
| TF, whole pathway, yeast MAPK | WT ~75 min; accelerated <20 min | Bashor 2008 Fig. 4B | measured |
| CRISPRi, *E. coli* | onset <10 min, full 240 min; reversal onset 50 min, full ~300 min | Qi 2013 Fig. 2E | measured |
| recombinase, *E. coli* | <2 h to 4–6 h, whole circuit | Yang 2014 Fig. 2f | measured |
| protein phosphorylation | **"seconds"** | Mishra 2021 | measured, no numeric value published |

> ⚠️ **Hooshangi 2005 does not carry a per-stage delay number** and should not be
> cited for one. It is about steady-state ultrasensitivity and noise
> propagation. For a measured per-stage transcriptional delay, Cheng et al. 2017
> is the right citation, and only its stated range is verified.

> ⚠️ **Gander et al. 2017's 184.9 ± 0.2 min/layer is SIMULATED** — a regression
> over simulated response times with four experimental points overlaid. Its
> *"effectively zero transcriptional leak"* (L = 0.6 ± 0.1%) is a **model-fit
> parameter**. And its authors are Gander, Vrana, **Voje**, Carothers & Klavins
> (Washington) — not Voigt, who is a different group entirely.

**Load**

| family | value | source | kind |
|---|---|---|---|
| transcription factor | **no measurement** found | — | — |
| CRISPRi | 530 ± 40 dCas9/cell before growth is affected; dynamic range <10-fold past 15 sgRNAs | Zhang & Voigt 2018 | measured |
| recombinase | growth reduced >25% only at very high expression | Yang 2014 Fig. 2g | measured |
| protein phosphorylation | **no measurement exists** that could be found | — | — |

**One of four cells in the load row is empty, and the slide says so** — the
phosphorylation gate. CRISPRi was filled on 25 Oct from Zhang & Voigt 2018 (§5),
which the first build of the deck had wrongly left blank. CRISPRi is the
well-characterised one because the shared-resource problem forced the field to
measure it, and that is itself the argument for Thursday.
