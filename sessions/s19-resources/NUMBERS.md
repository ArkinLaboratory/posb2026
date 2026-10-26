# Session 19 — every number, with its source and its kind

Companion to `DESIGN.md`. **No number goes on a surface unless it is in this
table with a kind attached.**

Verified 19 October. **Updated the same day: Adam supplied the PDFs, and every
number below that was previously secondhand is now read from the primary
source.** The files are in `private/readings/` under the Session NN naming
convention. Where something is still unverified it says so.

---

## 1 · The growth laws — T50

**Scott, Klumpp, Mateescu & Hwa, *Mol Syst Biol* 10:747 (2014)**, open access,
is the cleanest citable source for the laws as equations.

**Growth law 1 — nutrient quality.** Eq. 1, p. 2, verbatim:

> *"when growth rate is changed by modifying the nutrient composition of the
> medium, the mass fraction of ribosomal proteins φR varies linearly with the
> growth rate λ and has a positive slope (1/c), φR = φR^min + λ/c"*

**Growth law 2 — translational inhibition.** Eq. 2, p. 2, verbatim:

> *"when growth rate is changed by inhibiting protein synthesis (for example, by
> antibiotics), the mass fraction of ribosomal proteins φR remains linearly
> dependent on the growth rate λ, but now with a negative slope (−1/m),
> φR = φR^max − λ/m"*

**Parameter values**, Scott **2014** Fig. 2 legend (article p. 5), verbatim:
*"The remaining parameters are γ₀ = 5.9/h, ϕmin_R = 0.07 and ϕmax_R = 0.55
(Scott et al, 2010)."*

> ⚠️ **Corrected 25 October.** This was recorded here as *"c₀ = 5.9/h"* and
> propagated into the s19 deck. The symbol is **γ₀ (gamma-zero)**, the
> translational efficiency — `pdftotext` renders a Greek gamma as the
> character `c`, and the artifact was copied in as if it were verbatim.
> Re-checked against the PDF. Note also that the 2014 legend attributes all
> three values to Scott 2010, but only φ_R^max ≈ 0.55 and φ_c ≈ 0.48 appear
> in the 2010 main text; γ₀ and φ_R^min are not in the 2010 paper at all.
> **Cite these three to Scott 2014.**

| quantity | value | kind |
|---|---|---|
| γ₀, translational efficiency | 5.9 h⁻¹ | **fitted**; stated in Scott **2014** Fig. 2 legend |
| φR^min | 0.07 | fitted in Scott 2010, cited here |
| φR^max | **0.48–0.55 — see below** | fitted in Scott 2010, cited here |
| slope of law 1, 1/γ₀ | ≈ 0.17 h | **derived by us** from γ₀ |

> ✅ **RESOLVED from Scott 2010 itself, and the apparent conflict was a naming
> collision between two different quantities.** The paper states both:
>
> - **φ_R^max = ρ·r_max ≈ 0.55** — the maximum allocation to the ribosomal
>   R-class, verbatim: *"the maximum allocation to the R-class proteins as
>   derived from the value of r_max, φ_R^max = ρ·r_max ≈ 0.55, is well below 1."*
> - **φ_c = ρ·(r_max − r_0) ≈ 0.48** — a *different* number, the intercept at
>   which growth extrapolates to zero as unnecessary protein is expressed.
>
> Mori 2017's *"φ_R^max ≈ 48%"* is Scott's **φ_c** under Scott's other symbol.
> **There is no 0.48-versus-0.55 range to quote.** Use 0.55 for the ribosomal
> ceiling and 0.48 for the burden intercept, with Scott's own names, and do not
> present them as rival estimates of one thing — an earlier version of this file
> did, and the burden figure drew two lines because of it.

Mori 2017 also gives, independently measured in LB + glucose: *"λf = 2.45 ±
0.2/h and φR,f = 0.50 ± 0.01"*, and φR0^WT = 7% for their strain, with
λR^max ≈ 2.9/h. Translational capacity νR ≈ 2.9/0.48 ≈ **6.0/h** (derived by
us), consistent with Scott 2014's γ₀ = 5.9/h — two independent routes to the
same constant, which is worth showing.

### Schaechter, Maaløe & Kjeldgaard 1958 — the observation the laws rest on

*J Gen Microbiol* 19(3):592–606. **The full text could not be obtained and the
record carries no abstract.**

> ✅ **SUPERSEDED 25 October — Adam obtained the paper.** It is in
> `private/readings/` as `mic-19-3-592.pdf`: Schaechter, Maaløe & Kjeldgaard,
> *J. gen. Microbiol.* **19**:592–606 (1958), *"Dependency on Medium and
> Temperature of Cell Size and Chemical Composition during Balanced Growth of
> Salmonella typhimurium"*. ***Salmonella typhimurium*, not *E. coli***.

**What they measured**, from the Summary: *"Cell mass, the average number of
nuclei/cell and the content of RNA and DNA were studied in Salmonella
typhimurium during balanced (steady state) growth in different media."*

**The result everybody quotes**, p. 593: mass, RNA and DNA per cell and
nuclei per cell *"can be described as exponential functions of the growth
rate"* — across media, at one temperature.

🔴 **The result almost nobody quotes, and the deck had it backwards.** p. 593,
verbatim: *"**In a given medium, cell size and composition are almost
independent of the growth temperature.** The characteristics of the cells
would therefore seem to be determined primarily by the pattern of biochemical
activities imposed by the medium."* And the data behind it, p. 597, Table 2
(five media at 37 °C and 25 °C): *"In all cases, the growth rate at 25° was
about half that at 37°; nevertheless, mass, RNA, DNA and number of nuclei/cell
remained nearly constant for a given medium."*

> **So the 1958 claim is NOT "composition is a function of growth rate".** It
> is that composition is a function of the MEDIUM, and the growth-rate
> correlation holds only when the medium is what you changed. Halve the growth
> rate with temperature and nothing moves. The s19 slide said *"composition
> tracks the GROWTH RATE and is largely independent of which nutrients
> produced it"*, which is the Scott 2014 restatement — a later, looser
> generalisation that, read literally, contradicts the temperature result.
> Corrected on the slide 25 October.
>
> It is also a better teaching point than the version it replaced: if the cell
> were regulating on its own growth rate, cooling it would have changed the
> composition. It did not. The sensor is reading the medium — which is the
> question the ppGpp surface answers.

**And the origin of the constant-elongation assumption**, from the Summary:
*"Calculations indicate that the rate of protein synthesis per unit RNA is
nearly the same at all growth rates"*; restated p. 593 as *"per unit of RNA,
the number of protein molecules synthesized/minute is almost independent of
the growth rate."* This is what the mass-balance argument on the
"why ribosomes" surface leans on — and Bremer & Dennis Table 3 shows it is
only approximately true, with peptide elongation rising from 13 to 22 aa/s
across the range. Both are worth saying.

**The Scott 2014 restatement**, for comparison and still quotable as *theirs*:
*"the macromolecular composition of Escherichia coli is correlated simply with
the growth rate of the culture, largely independent of the specific nutrients
in the growth medium."*

### Bremer & Dennis — the tabulation, for the "ribosome budget" surface

✅ **SOURCE OBTAINED 25 October and every row replaced.** Adam filed the
authors' own 2008 revision, which supersedes the Neidhardt chapter and removes
the edition ambiguity entirely:

> Bremer, H. & Dennis, P. P. "Modulation of Chemical Composition and Other
> Parameters of the Cell at Different Exponential Growth Rates." *EcoSal Plus*
> 3(1), 2008. doi:10.1128/ecosal.5.2.3. In `private/readings/`.

**Table 3**, p. 8 of the PDF — *"Parameters pertaining to the macromolecular
synthesis rates in exponentially growing E. coli B/r as a function of growth
rate at 37°C"*. Columns as published. **The table's own "Observed
parameters" column distinguishes what was measured from what was computed
from it, and that distinction matters** — it is why the ppGpp and rRNA-
initiation curves are NOT two independent measurements:

| µ (doublings/h) | 0.6 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | kind, per the table |
|---|---|---|---|---|---|---|---|
| ribosomes/cell, N_r (×10³) | 8 | 15 | 26 | 44 | 61 | 73 | derived from RC, f_s, f_t |
| r-protein / total protein, α_r (%) | 7.7 | 9.2 | 11.6 | 15.0 | 18.8 | 22.7 | **observed** |
| peptide chain elongation, c_p (aa/s) | 13 | 18 | 21 | 22 | 22 | 22 | indirect |
| ribosome activity, β_r (%) | 85 | 85 | 85 | 85 | 85 | 85 | indirect |
| ppGpp, ppGpp/M (pmol/OD₄₆₀) | 55 | 38 | 22 | 15 | 10 | 6 | **observed** |
| initiations/min at each *rrn* gene, i_rrn | 4 | 10 | 20 | 37 | 54 | 68 | derived from N_r, N_rrn |
| *rrn* genes/genome | 7.9 | 8.4 | 8.8 | 9.1 | 9.3 | 9.4 | derived from C |

### Ribosome composition, for the "why ribosomes at all" surface

Added 25 October. These were on a slide before they were in this file, which
is the rule this document exists to enforce — recording them after the fact.

| quantity | value | kind | source |
|---|---|---|---|
| RNA as a fraction of ribosome mass | ≈ 2/3 | textbook constant | Milo & Phillips, *Cell Biology by the Numbers* (2015), **printed p. 87**: *"the RNA makes up close to 2/3 of the mass of the ribosome and proteins only a third"* |
| ribosomal proteins per bacterial ribosome | **56** | counted | same page: *"over 50 proteins (56 in bacteria, BNID 100111…)"* |
| rRNA as a fraction of total cellular RNA | **≈ 85%** | measured | Scott 2010, **p. 1099**: *"In Escherichia coli, most of the RNA (~85%) is rRNA folded in ribosomes"*; independently Milo & Phillips printed p. 188 |
| share of ribosomes engaged in making ribosomes | = the ribosome share of the proteome | **derived, and it is theirs** | Scott 2014, **p. 8**: *"if ribosomes represent 30% of the proteome in steady state, it also means that 30% of the ribosomes are engaged in producing ribosomes"* |

> ⚠️ Milo & Phillips is a numbers reference, not a primary paper. Cite it as
> the book. Its printed and PDF page numbers differ by two — printed 87 is
> PDF 89, printed 188 is PDF 190 — and a slide foot briefly mixed the two
> systems in one citation.

> ⚠️ **What is NOT sourced, and must be said as background if said at all:**
> the mass-balance argument gives PROPORTIONALITY, but law 1 is affine
> (φ_R^min = 0.07), and it assumes a growth-rate-independent elongation
> rate, which Table 3 above contradicts below about µ = 1.5 (c_p rises 13 →
> 22 aa/s). No paper in `private/readings/` argues "ribosomes are
> autocatalytic, therefore φ_R ∝ λ".

**Table 2**, p. 6, gives the growth law directly as RNA/mass over protein/mass —
0.057, 0.069, 0.086, 0.110, 0.140, 0.168 nucleotides per amino acid across the
same six columns. That is Scott's *r*, from a different laboratory, thirty
years earlier.

> 🔴 **Every row we had before was wrong, and wrongly labelled "measured".**
> The previous values were transcribed from page scans that are not in the
> repository and never were. They disagree with the published table in every
> row, with a diagnostic pattern — our µ = 2.5 entries matched the table's
> µ = 3.0 column, and the r-protein row matched the next column along
> throughout. **It was read off by one column.** For the record:
>
> | row | what we had | what the table says |
> |---|---|---|
> | ribosomes/cell (×10³) | 6.8, 13.5, 26.3, 45.1, 72.0 | 8, 15, 26, 44, 61, 73 |
> | r-protein (%) | 9, 11, 13.5, 18, 21.6 | 7.7, 9.2, 11.6, 15, 18.8, 22.7 |
> | peptide elongation (aa/s) | 12, 16, 18, 20, 21 | 13, 18, 21, 22, 22, 22 |
> | ribosome activity (%) | 80 | **85** |
>
> **The headline was wrong too.** "A tenfold change in ribosomes per cell
> across a fourfold change in growth rate" is not in the data: µ 0.6 → 3.0 is
> **5×** and ribosomes 8 → 73 is **9×**. The slide and the figure now say
> five and nine. Anything anywhere still quoting "4× / 10×", 80% activity, or
> the old ribosome counts is stale and predates 25 October.

> ⚠️ **A gap that remains.** The conversion Scott 2010 uses to turn the
> RNA/protein ratio into φR (often quoted as φR ≈ 0.76·r) **could not be
> verified from any open source.** So the Bremer–Dennis r-protein rows and
> Scott's φR^min = 0.07 cannot be cleanly reconciled here — the measured r-protein
> fraction is strictly ribosomal proteins, while φR includes ribosome-affiliated
> proteins. **Present them as two separate things** or get Scott 2010's SOM.

---

## 2 · The cost of a useless protein — T49

This is the session's load-bearing number and the verification is thinner than
the rest. Read this section before putting a slope on a slide.

**Now read from Scott 2010 directly.** The paper models it and names it,
verbatim:

> *"We modeled the expression of unnecessary protein (of mass fraction φ_U) as
> an additional (neutral) component of the proteome that effectively causes a
> reduction of r_max to r_max − φ_U/ρ (Fig. 4A). Equation 5 then predicts a
> **linear reduction of the growth rate** … extrapolating toward zero growth at
> **φ_c = ρ·(r_max − r_0) ≈ 0.48**."*

and the prediction was tested: *"The lines are predictions by Eq. 6, using the
growth rate λ(φ_U = 0) and intercept φ_c = 0.48 computed from the average r_max
(table S4) … The prediction quantitatively described the observed growth defect."*
Fig. 4C compares several expression systems, including β-lactamase from the bla
promoter on a medium-copy plasmid.

    λ(φ_U) / λ(0)  =  1 − φ_U / φ_c          with φ_c ≈ 0.48

| quantity | value | kind |
|---|---|---|
| **φ_c, the zero-growth intercept** | **≈ 0.48** | **stated in Scott 2010**, computed there from r_max |
| **growth loss per 1% of proteome diverted** | **≈ 2.1% of λ** | **our arithmetic**: 0.01/0.48 |
| growth arrest extrapolates at | **≈ 48% of the proteome** | stated |

**So the intercept is the paper's, not ours.** An earlier version of this file
reached 0.48 by subtracting 0.55 − 0.07 and labelled the whole thing "derived by
us" — the arithmetic happened to be right, because φ_c *is* φ_R^max − φ_0, but
the number did not need deriving. Only the per-1% slope is ours, and it is one
division. **The design-ledger line — "every 1% of the proteome you divert costs
about 2% of your growth rate" — now rests on a stated intercept.**

This is the coefficient `posb.resources.dilution_coupled_steady_state` takes as
its required `growth_penalty` argument. The function has no default precisely so
that this citation travels with it.

**Dong, Nilsson & Kurland, *J Bacteriol* 177(6):1497–1504 (1995)** — ✅ **full
text obtained and read, 25 October**; it is in `private/readings/`. The earlier
"abstract verified, full text not obtained" note here was stale. *E. coli*,
T7-driven lacZ reaching **30% of
total bacterial protein**; verbatim: *"there is a cumulative breakdown of rRNAs,
which results in a loss of ribosomes and protein synthetic capacity … Finally,
after several hours of overexpression of either test protein, the bacteria are no
longer viable."*

> ⚠️ **Do not use Dong 1995 as the source of the linear slope.** It is a
> transient, toxic, T7-driven overexpression ending in rRNA destruction and loss
> of viability. Scott 2010's relation is a steady-state balanced-growth law.
> Different regimes. Also relevant: Shachrai, Zaslaver, Alon & Dekel, *Mol Cell*
> 2010, find the cost of unneeded protein **falls after several generations** —
> so the cost is history-dependent.

**What Dong 1995 IS good for, and the s18/s19 ledger now uses it**: it saw the
heat-shock response to gratuitous overexpression twenty-three years before
Ceroni 2018 mapped it transcriptome-wide. Verbatim, **p. 1500**: *"the heat
shock proteins DnaK and GroEL increase by roughly 90 and 27%, respectively.
Accordingly, there is both a graded decrease in the accumulation of uninduced
proteins and a specific enhancement of heat shock proteins in response to the
overexpression of either b-galactosidase or ΔEF-Tu."* Measured. Seen in 1995,
mapped in 2018, **mechanism still open** — Ceroni 2018 p. 389 says so in as
many words.

---

## 3 · Shared resources, measured — T48

**Gyorgy, Jiménez, Yazbek, Huang, Chung, Weiss & Del Vecchio, *Biophys J*
109(3):639–646 (2015).** Open access. The best measured-coupling source.

**The isocost relation**, Eq. 1, verbatim: *"the attainable output (p₁,p₂) …
satisfies the following formula: **αp₁ + βp₂ = Y** … With the available budget Y
of ribosomes, the cell can produce p₁ units of p₁ at price α and p₂ units of p₂
at price β."* Modelled — and it is the same straight line
`posb.resources.isocost_sum` produces from the partition function.

**The apparent interaction between genetically unconnected modules — the number
the session turns on**, verbatim: *"Induction of GapA with AHL has the same
effect on GFP as inducing RFP, **decreasing GFP production by up to 60%**."*
Measured, flow cytometry, mean ± SD of three independent experiments.

**And it scales with copy number**, Fig. 4A, measured:

| plasmid copies | change in GFP |
|---|---|
| 64 ± 2 | **60%** |
| 18 ± 4 | **48%** |
| 4 ± 1 | **29%** |

Verbatim from the Discussion: *"The extent of this coupling is substantial
ranging from 60% when circuits are on medium copy number plasmids to 29% when
circuits are on very low copy number plasmids."*

**The straight line was measured too**, verbatim: *"when plotting GFP over RFP
we observe, as predicted by the isocost line (Eq. 1), a linear relationship
between RFP and GFP productions (Fig. 3 B). Further, when the RBS of RFP becomes
weaker, we observe that the slope becomes steeper."*

**Which resource is limiting — both, and the paper separates them**, verbatim:
*"the decrease in GFP is mostly attributable to the limited availability of
ribosomes … However, the increase in slope of the isocost line when the RBS
strength for RFP is decreased cannot be predicted unless RNAP is limiting."*

### ✅ The plasmid/chromosome result — RESOLVED from the PDF, and it is the best surface in the segment

The guess recorded here earlier was right about the mechanics and wrong to call
it a guess, so here is what the paper actually does. **There are two GFPs in two
different experiments**, and the contrast between them is deliberate and
controlled:

| | GFP location | gapA induced → GFP |
|---|---|---|
| **Fig. 1B** | **chromosome** | **no effect** |
| **Fig. 1C** | **same plasmid** | **down up to 60%** |

Verbatim: *"although the expression of a gene (gapA) affects that of another gene
on the same plasmid (RFP), it has no effect on the steady-state expression of a
third gene located on the chromosome (GFP) … This indicates a separation between
the resources available to the genes on the plasmid and those available to the
chromosomal genes."* And again: *"the pools of RNAP and ribosomes available to
the genes on the plasmid are essentially separated from those available to the
chromosomal genes."*

**The null result is controlled, not an absence of evidence.** They built
MBP-tetR with chromosomal GFP and plasmid-borne TetR *"to demonstrate that
possible reductions to the chromosomal GFP expression are detectable."* And the
MBP-dRFP control (RFP gene removed) shows GFP unaffected, so *"the GFP decrease
is not because of the product RFP itself but rather to the process that produces
RFP."*

They then build the separation into the model: *"we let X and Y represent the
concentration of RNAP and ribosomes, **available to the genes on the plasmid**."*

**Why this is worth teaching rather than hiding.** The partition function in
`posb.resources` has one pool, and the naive reading of it is that everything in
the cell couples to everything. The measurement says otherwise: the coupling was
confined to the plasmid. So **"the shared pool" has a boundary, and where it
falls is an experimental question, not a modelling assumption.** That is session
17's thesis arriving from the other side — there the boundary of a *part* had to
be manufactured; here the boundary of a *resource pool* has to be found.

**Growth rate is NOT the explanation here**, verbatim: *"This combination of
factors contributes to the rather modest change in growth rate that we have
observed in our experiments upon AHL induction."* No numeric growth change is
given. So the 60% coupling is a resource effect, not a growth effect — which
keeps segments 4/5 and segment 6 of the session distinct.

**Qian, Huang, Jiménez & Del Vecchio, *ACS Synth Biol* 6(7):1263–1272 (2017)** —
read from the bioRxiv preprint; equations are images and could not be extracted
verbatim. Its teachable object is the **shared denominator**
`1 + J₁ + J₂F₂(x₁) + J₃F₃(x₂)` across all three nodes of a cascade, and an
effective interaction graph containing **non-regulatory edges**. ⚠️ **No
magnitude is recoverable from it** — the data are normalised to each plot's
maximum, and the *"more than 60%"* in the text is attributed to prior work.
**Use Gyorgy's 60%, not Qian's.**

---

## 4 · Burden, measured — the required reading

**Ceroni, Algar, Stan & Ellis, *Nat Methods* 12(5):415–418 (2015).** Not open
access; read from the bioRxiv preprint (10.1101/013110), which is **not** the
published version.

**The instrument, verified:** a chromosomally integrated constitutive GFP
cassette — synthetic strong constitutive promoter (**BBa_J23100**), synthetic
RBS, codon-optimised superfolder GFP — integrated at the lambda (pAH63) locus.
That is what segment 2 draws.

### The definition, which is what the reading asks students to come with

Read from the published PDF. **Capacity is the GFP production rate per cell from
a chromosomally integrated, unregulated cassette, expressed as a percentage of
untransformed cells (= 100%).** Verbatim on the normalisation: *"we compared the
percentage decrease in the capacity of the full system … to the capacity of
untransformed GFP+ cells (100%)."* And on the quantity: *"Capacity (determined as
the GFP production rate per cell)."*

### The argument for the instrument — better than any single number

Verbatim:

> *"Capacity … was substantially reduced compared to that of uninduced cells
> **within 30 min** of operon induction, and this rapid change contrasted with
> the **smaller, slower decreases in growth** observed when culture optical
> density was measured. The observation that a change in capacity **preceded** a
> change in growth rate after induction (Supplementary Fig. 2) supports the view
> that decreased expression resources cause a decline in growth rate."*

**Growth rate is a lagging and blunt proxy for burden.** Capacity moves in half
an hour; growth moves later and by less. That is why the session opens on the
instrument rather than on the algebra, and it is the answer to "why not just
weigh the cells."

Also verbatim, and useful for segment 6: *"Decreases in capacity in both strains
led to subsequent growth-rate decreases of **similar magnitude**"* (Supplementary
Fig. 3) — qualitative, but it is the link between this session's two halves.

**The library is a gratuitous-protein experiment**, which connects it directly to
Scott 2010: *"a library of inducible constructs that express a large protein with
**no function in our cells**, the Chromobacterium violaceum enzyme VioB fused to
mCherry"*, varied by plasmid copy number, core promoter, RBS strength, and codon
optimisation versus de-optimisation.

> ⚠️ **The per-construct capacity percentages live only in the plots** (Fig. 1c,
> 1d, Fig. 2a–c) — there is no table of them in the text, so crop the panel,
> do not transcribe numbers off it.
>
> ⚠️ **Panel letters, corrected 25 October.** This note previously called
> Fig. 2a "the capacity-against-output scatter". It is not. From the Fig. 2
> legend: **(a)** is per-design bar charts of output, capacity and growth
> rate, with bold text marking a strong core promoter and RBS; **(b)** is
> growth rate against capacity; **(c)** is **capacity against output** — the
> scatter, with the unattainable region shaded — and **(c)** is the panel the
> reading's focus line is really about and the one now on the slide.
> **(d)** is a simulated heat map; the s19 crop of "2a" had picked up panel
> d's bold label from across the page gutter.

Numbers that *are* verified, with their correct referents:

| value | refers to | kind |
|---|---|---|
| ≈1.5-fold | output gain, mutated pBad over wild type | measured |
| ≈3-fold | output gain, strong vs weak RBS | measured |
| ≈5-fold | output gain, high vs medium copy | measured |
| **≈3.5-fold** | **capacity difference between scFv designs**, *"a close match to the simulation predicted increase"* | **measured** |
| >3-fold | capacity gain predicted for shorter CDS | **simulated** |
| 26,300 | total ribosomes assumed in the simulation | **assumed** |

> **The ≈3.5-fold measured capacity difference between scFv constructs whose
> growth rates were comparable and whose output was equivalent is the strongest
> verified number in the paper, and it is a better teaching point than a
> growth-rate number anyway:** two designs, same growth rate, same output,
> 3.5-fold different capacity. Growth rate alone would have told you nothing.

**Ceroni et al., *Nat Methods* 15(5):387–393 (2018)**, burden-driven feedback —
mechanism verified, recovery numbers not. The burden sensors are native
**σ32-regulated** promoters driving chaperone and protease genes — *ibpAB,
dnaKJ, htpG, groSL* — and **htpG1** was used in the controller. Measured:
**11.7% (pD864-LacZ) to 47.3% (pLys-M1)** of mapped RNA-seq reads came from the
synthetic construct 15 min after induction. What the dCas9 feedback recovered
is plotted only — **not verified.**

**Promoter induction — CORRECTED 25 October.** Recorded here previously as
"10- to 1000-fold in DH10B", which is wrong and was on a slide. The paper,
p. 389, verbatim: *"We observed increases in promoter activity of **up to
50-fold in DH10B cells and 10-fold in MG1655 cells**."* There is no
"1000-fold" anywhere in the paper.

**And the mechanism is explicitly NOT claimed**, p. 389, verbatim: *"These
therefore act as intrinsic biosensors for synthetic-construct-induced burden
in E. coli, although **the precise mechanisms behind their activation are not
fully understood**."* The Discussion (p. 392) suggests chaperones may be an
additional *kind* of burden rather than the sensing step. So the familiar
DnaK-titrated-off-σ32 story is textbook background, **not this paper's claim**,
and must not be put on a slide as if it were.

**Two construct details the deck got loose.** Only **htpG1** drives the
controller, not "σ32 promoters" plural; and the **dCas9 is constitutive**
(BBa_J23113) — it is the **sgRNA** that is burden-driven.

---

## 5 · Growth feedback changes the circuit's own dynamics

**Klumpp, Zhang & Hwa, *Cell* 139(7):1366–1375 (2009)** — **could not be
obtained** (Cloudflare, reCAPTCHA, rate-limited DOI). Only the abstract is
verified, and it does support the session's framing: *"important global
parameters such as the abundance of RNA polymerases and ribosomes are all
growth-rate dependent … a feedback mechanism mediated by general
growth-dependent effects that does not require explicit gene regulation if the
expressed protein affects cell growth. This mechanism can lead to growth
bistability."* **No numbers from it.**

**A verified open-access substitute, and arguably the better figure:**
Berthoumieux, de Jong, Baptist, Pinel, Ranquet, Ropers & Geiselmann, *Mol Syst
Biol* 9:634 (2013). Measured, GFP reporters in M9 + 0.3% glucose at 37 °C, 3–4
replicates. Verbatim: *"A first surprising finding of this study is that the
activities of the genes encoding the transcription factors Fis, Crp, and RpoS
closely follow the activity of a constitutively transcribed promoter."* They also
reproduced the result with Klumpp's own ptet promoter and found the two agreed.
**What looks like specific regulation is largely global physiology** — and this
one can be shown.

Also measured there: plasmid copy number *"increases up to a factor of 2"*
across the growth transition, by qPCR. A second reason a circuit's output moves
when nothing in it changed.

---

## 6 · The close — emergent bistability

**Tan, Marguet & You, *Nat Chem Biol* 5(11):842–848 (2009).** ✅ **Full text
obtained and read, 25 October** — the NIH-PA author manuscript, in
`private/readings/`, so page numbers below are MANUSCRIPT pages. The earlier
"abstract verified, full text not obtained" note here is what let a wrong
number onto a slide; see the Fig. 1c block below. Verbatim:

> *"a simple circuit consisting of mutant T7 RNA polymerase (T7 RNAP*) that
> activates its own expression … **Although activation by the T7 RNAP* is
> noncooperative, the circuit caused bistable gene expression.** This
> counterintuitive observation can be explained by growth retardation caused by
> circuit activation, which resulted in nonlinear dilution of T7 RNAP* in
> individual bacteria."*

Figure titles, verified from the publisher preview: Fig. 2 is *"Circuit
activation reduces bacterial growth rates."*

### ✅ The ON-fraction — the "fabrication" was not one. CORRECTED AGAIN, 26 October

**Read the panel, not the text layer.** `private/paper-figures/tan2009_fig1c.png`,
rendered at 2x and looked at on 26 October, is annotated **"30% ON"** on the
before-dilution histogram and **"32% ON"** on the 8-hours-after one. Those are
figure labels, so they are not in `pdftotext` output — which is how the
25 October note came to call them invented.

The Fig. 1c legend, manuscript p. 13, rounds both:

> *"The cell culture gave rise to **~31% ON cells both before dilution and 8
> hours after dilution**."*

and the main text (p. 3) gives no figure at all: *"We observed that each
population after the second cycle of growth contained a similar percentage of
ON cells as its seeding culture before the dilution (Figs. 1c & S3)."*

So **30 and 32 are the paper's own numbers**, 31 is the legend's rounding of
them, and there is no discrepancy to teach. The 25 October note said the deck
"appears to have assembled" the numbers from unrelated places; that was wrong,
and deck slide 37 had been given a whole annotation row explaining a
non-discrepancy. Both are fixed.

**Say: about a third before, about a third after — it did not move.** The room
can read 30 and 32 off the screen, so do not tell them the legend disagrees
with the panel.

> **Method note worth keeping.** Three times this week a number was called
> fabricated on the strength of a `pdftotext | grep`. Figure labels, axis
> annotations and anything set as part of an image are invisible to that
> check. Before writing "appears nowhere in the paper", render the panel and
> look at it.

### Noncooperativity was MEASURED, not assumed

Manuscript pp. 3–4, verbatim: *"CFP exhibited a Hill's coefficient of ~0.99
with respect to EYFP (Fig. S6), **confirming the lack of cooperativity in
T7RNAP***"*. This is a stronger claim than "no cooperative step appears in the
loop" and it closes off the obvious objection to the whole close.

**The model, reproduced and tested here.** The rate equation as published in
Ochab-Marcinek, *Eur Phys J E* (2012), arXiv:1108.3720, Eq. 1, which states its
parameters are *"identical to those reported in"* Tan et al.:

    dx/dt = (δ + αx)/(1 + x)  −  φx/(1 + γx)  −  x

with δ = 0.01, φ = 20, γ = 10 (the burden parameter), α varied.

**The symbols are now confirmed from Tan 2009 itself**, verbatim: *"x is the
[T7 RNAP*]; δ is the basal expression level of T7 RNAP*; α is the effective
synthesis rate constant of T7 RNAP*; ϕ is the maximum growth rate; and γ is the
metabolic burden due to expression of T7 RNAP*."*

**And the controlled test below is the paper's own semantics**, verbatim: *"The
second RHS term represents the T7 RNAP* dilution due to bacterial growth. **If
γ = 0, bacteria always divide at ϕ. If γ > 0, expression of T7 RNAP* reduces the
effective growth rate.**"* They also state the assumption that matters: *"we
assume that the impact of metabolic burden on growth has **no cooperativity**.
This assumption is consistent with our experimental observations (Fig. 2)."*

**α is an experimental knob**, verbatim: *"α, the T7 RNAP* synthesis rate
constant, **increases with [IPTG]**"*, and ϕ increases with the maximum growth
rate — so the bifurcation figure's x-axis is an inducer concentration, not an
abstraction. Tan et al. do their own bifurcation analysis in (α, ϕ), Fig. 5a.

> ⚠️ **Still secondhand: the numeric parameter values** δ = 0.01, ϕ = 20,
> γ = 10. These come from Ochab-Marcinek 2012, which states they are those of
> Tan et al.; the equations in the Tan PDF render as images and the supplementary
> table was not reached. The *mechanism* below is reproduced and tested; the
> specific numbers are a published model's, not a replication of Tan's figures.

| result | value | kind |
|---|---|---|
| expression term | Hill-1 in x — **no cooperativity anywhere** | by inspection |
| bistable window in α at γ = 10 | **5.575 to 18.425** — a factor of 3.30 | computed |
| separation of the two stable states | **~6,000 to 7,700×** | computed |
| minimum burden for bistability at α = 14 | **γ = 2.22** | computed |
| **with γ = 0, so dilution is linear** | **one stable state at every α tested** | computed |

**The controlled test is the point.** Setting the burden parameter to zero makes
dilution linear and the bistability disappears completely. The nonlinearity is
in the dilution term, not in the regulation — so a noncooperative positive
feedback loop became bistable because the host pushed back.

**And the two edges of the window fail differently**, which is the design
consequence: at the low edge the ON state is born; at the high edge **the OFF
state is destroyed** (the low stable point and the unstable point annihilate at
α ≈ 18.42, leaving only the high state). **Drive the synthesis rate too hard and
you lose the ability to turn the circuit off.**

> Two errors of ours were caught while computing this window: a bisection
> called with an inverted bracket returned its own midpoint (17.000) without
> iterating, and a second attempt asserted a monostable endpoint at α = 18 that
> is in fact bistable. Both were found by asserting that a bracket brackets.
> Recorded because the window is going on a slide.

### Why this is the right close

Three sessions, three sources of the same nonlinearity, and a student should be
able to name all three by Thursday:

| session | where the nonlinearity comes from |
|---|---|
| 9 | cooperative binding — *"you choose it by choosing a protein"* |
| 18 | saturation of two opposing enzymes — zero-order ultrasensitivity |
| **19** | **the host.** Growth slows under load, dilution saturates, and a noncooperative circuit becomes bistable |
