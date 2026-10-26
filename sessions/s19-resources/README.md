# Session 19 — Resource sharing and burden: your circuit is not alone in there

**Thursday 29 October 2026.** Part II, fourth session. **PS6 is due tonight**
(Canvas 9160475 for BioE 147, 9160495 for 247), and **PS7 is posted today**,
due 5 November, covering sessions 17, 18 and 19. Required reading: Ceroni,
Algar, Stan & Ellis, *Nat Methods* 2015, handed out at the close of session 18
and **in `private/readings/`**.

`DESIGN.md` is **stale** and should not be read as the plan: it still says
"Status: DESIGN", it says four PDFs are pending that are now all filed, and its
§2 states the 1958 result backwards. The deck and `NUMBERS.md` are the
authority, and both were corrected substantially on 25–26 October.

## The one thing to remember

**Your circuit is not alone in there — and this time you cannot insulate.**

Session 17 showed composition failing because parts change each other through
what they physically share, and its cure was to **impose a boundary**: fix the
junction, insulate, standardise, and the abstraction becomes true because you
made it true.

Today composition fails again and **there is no boundary to impose**. Two genes
with no regulatory connection change each other's output because they draw on
the same ribosomes. You can fix a 5′UTR. **You cannot give your circuit its own
ribosome pool.** That escalation is the hour, and it makes today the harder
problem rather than the easier one.

And the host does more than tax you. It supplies a nonlinearity your diagram
does not contain: a noncooperative positive feedback loop, which by session 9's
analysis cannot be bistable, is bistable — because activating it slows growth,
slower growth dilutes less, and the dilution term saturates.

## What happens

| | |
|---|---|
| **Retrieval** | From Tuesday: where did the covalent cycle's sharpness come from, given that nothing binds cooperatively? From session 6: write the occupancy of an operator two factors compete for, and say what is in the denominator and why — **this one goes on the board and stays there.** From session 5: t½ = ln2/(γ + μ); what is μ, and what did we assume about it? |
| **Goals** | Three questions, asked and not answered: what sets a cell's composition, rate or diet? Two genes, no wire — induce one, what happens to the other and how would you tell it from regulation? Your circuit slows the cell; what does that do to the circuit? |
| **1 · The economy** | Schaechter, Maaløe & Kjeldgaard 1958, with the result almost nobody quotes. Then why ribosomes, of all things — what one is made of, and the mass balance. The ribosome budget, measured. Scott's two correlations, and the second is a surprise. The two laws, and they disagree about the sign. Then **the controller**, as a drawn mechanism rather than a causal chain of undrawn nouns, and then the same controller in numbers. Then two minutes on paper: spend a tenth of the cell on nothing. **T50.** |
| **2 · The instrument** | Burden is a word until something is measured, in units, by an instrument you can describe. Ceroni's capacity monitor, trace by trace. Then why not weigh the cells: **capacity moves first.** Then the result the reading asked for — same output, different price. |
| **3 · The derivation** | Two definitions first, so the run is uninterrupted: the binding step, and demand d_i = m_i/K_i, **which is a sequence you can order**. Then five steps to R = R_T/(1 + Σd). Then the debrief: you have seen this denominator before, on 15 September. |
| **4 · The hidden edge** | An edge with no arrow — and it is not crosstalk, because both parts are perfectly specific. Then the room commits a number in writing before anything goes up. Then the figure, and the diagnostic: K_app = 1 + d₁, so **measure the apparent K at two expression levels of your own reporter**. No cloning. **T48.** |
| **5 · The isocost line** | Stop asking who loses; ask what the budget is. Ours from a partition function, then Gyorgy's out of a cytometer. Then induce one gene and watch an unconnected one fall — and then **move one of them to the chromosome**, which our one-pool model says cannot matter. Debrief: the pool has an edge and the model does not know where it is. **T48, and the S17/S19 half of T42 and T43.** |
| **6 · The burden loop** | The price in growth, linear all the way to a stop. Scott's Fig. 4B, where **the slope was known before the points were**. Then Fig. 4C: three proteins, four expression systems, one curve. Then the loop closes — go back to the board and edit September's μ. **T49.** |
| **7 · Emergent bistability** | Session 9 says this circuit cannot do what it does. The circuit, then a vote, hands up. Then what happened. Then where the nonlinearity was hiding — in the dilution, not the regulation, with γ = 0 as the controlled test. Then its wedge, and the two saddle-nodes fail differently. |
| **8 · The design ledger** | You cannot insulate, so what *can* you do — and the last row is what you cannot. |
| **Close** | The same mechanism, three times: decoy sites Tuesday, ribosomes today, downstream targets in session 21. **Hand out Fong & Palsson.** |

## The results this session exists to produce

### The growth laws — T50

**Scott, Klumpp, Mateescu & Hwa, *Mol Syst Biol* 10:747 (2014)**, open access,
is the cleanest citable source for the laws as equations. Law 1, nutrient
quality: φ_R = φ_R^min + λ/c, *"the mass fraction of ribosomal proteins φR
varies linearly with the growth rate λ and has a positive slope"*. Law 2,
translational inhibition: φ_R = φ_R^max − λ/m, *"now with a negative slope"*.

| quantity | value | kind |
|---|---|---|
| γ₀, translational efficiency | **5.9 h⁻¹** | **fitted**; stated in Scott **2014** Fig. 2 legend |
| φ_R^min | 0.07 | fitted in Scott 2010, cited via Scott 2014 |
| **φ_R^max = ρ·r_max** | **≈ 0.55** — the ribosomal ceiling | fitted, stated in Scott 2010 |
| **φ_c = ρ·(r_max − r_0)** | **≈ 0.48** — the zero-growth intercept for unnecessary protein | stated in Scott 2010 |
| slope of law 1, 1/γ₀ | ≈ 0.17 h | **derived by us** |

> **φ_R^max ≈ 0.55 and φ_c ≈ 0.48 are different quantities, both from Scott
> 2010.** There is no 0.48-versus-0.55 range to quote. An earlier version of
> `NUMBERS.md` presented them as rival estimates of one ceiling and the burden
> figure drew two lines because of it. Mori 2017's *"φ_R^max ≈ 48%"* is Scott's
> φ_c under Scott's other symbol. Segment 1's foot carries 0.55 and segment 6's
> carries 0.48, and segment 6 says out loud that they are not the same number.

> **Also corrected 25 October:** this was recorded as *"c₀ = 5.9/h"* and that
> propagated into the deck. The symbol is **γ₀**; `pdftotext` renders a Greek
> gamma as `c`, and the artifact was copied in as if it were verbatim. And
> although the 2014 legend attributes all three values to Scott 2010, only
> φ_R^max and φ_c appear in the 2010 main text — **cite all three to Scott
> 2014.**

Mori 2017 gives, independently measured in LB + glucose, λ_f = 2.45 ± 0.2/h and
φ_R,f = 0.50 ± 0.01, with λ_R^max ≈ 2.9/h; translational capacity
ν_R ≈ 2.9/0.48 ≈ **6.0/h**, derived by us and consistent with Scott 2014's
γ₀ = 5.9/h. Two independent routes to the same constant.

### Schaechter, Maaløe & Kjeldgaard 1958 — and the deck had it backwards until 25 October

*J. gen. Microbiol.* **19**:592–606, *"Dependency on Medium and Temperature of
Cell Size and Chemical Composition during Balanced Growth of Salmonella
typhimurium"*. ***Salmonella typhimurium*, not *E. coli***. Obtained by Adam on
25 October and filed as `private/readings/mic-19-3-592.pdf`.

The result everybody quotes, p. 593: mass, RNA, DNA and nuclei per cell *"can be
described as exponential functions of the growth rate"* — **across media, at one
temperature**.

**The result almost nobody quotes**, p. 593, verbatim: *"**In a given medium,
cell size and composition are almost independent of the growth temperature.**
The characteristics of the cells would therefore seem to be determined primarily
by the pattern of biochemical activities imposed by the medium."* And the data,
p. 597, Table 2, five media at 37 °C and 25 °C: *"In all cases, the growth rate
at 25° was about half that at 37°; nevertheless, mass, RNA, DNA and number of
nuclei/cell remained nearly constant for a given medium."*

> **So the 1958 claim is that composition is set by the MEDIUM.** Scott 2014's
> restatement — *"the macromolecular composition of Escherichia coli is
> correlated simply with the growth rate of the culture, largely independent of
> the specific nutrients"* — is a **later generalisation**, and read literally
> it contradicts the temperature result. The slide said the restatement and
> attributed it to 1958; corrected 25 October, and the slide now carries both
> sentences with Scott's marked as Scott's.
>
> It is also the better teaching point: **if the cell were regulating on its own
> growth rate, cooling it would have changed the composition. It did not.** The
> sensor is reading the medium — which is the question the ppGpp surface answers.

And the origin of the constant-elongation assumption, from their Summary:
*"per unit of RNA, the number of protein molecules synthesized/minute is almost
independent of the growth rate."* The mass-balance argument leans on it, and
Bremer & Dennis Table 3 shows it is only approximately true.

### What the cell owns — Bremer & Dennis 2008, Table 3

Bremer, H. & Dennis, P. P., *EcoSal Plus* **3**(1), 2008, doi:10.1128/ecosal.5.2.3
— the authors' own revision of the Neidhardt chapter, which removes the edition
ambiguity entirely. *E. coli* B/r at 37 °C. **The table's own "Observed
parameters" column distinguishes what was measured from what was computed from
it, and that distinction matters** — it is why the ppGpp and rRNA-initiation
curves are not two independent measurements.

| µ (doublings/h) | 0.6 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | kind, per the table |
|---|---|---|---|---|---|---|---|
| ribosomes/cell, N_r (×10³) | 8 | 15 | 26 | 44 | 61 | 73 | derived from RC, f_s, f_t |
| r-protein / total protein, α_r (%) | 7.7 | 9.2 | 11.6 | 15.0 | 18.8 | 22.7 | **observed** |
| peptide chain elongation, c_p (aa/s) | 13 | 18 | 21 | 22 | 22 | 22 | indirect |
| ribosome activity, β_r (%) | 85 | 85 | 85 | 85 | 85 | 85 | indirect |
| ppGpp (pmol/OD₄₆₀) | 55 | 38 | 22 | 15 | 10 | 6 | **observed** |
| initiations/min at each *rrn* gene | 4 | 10 | 20 | 37 | 54 | 68 | derived from N_r, N_rrn |
| *rrn* genes/genome | 7.9 | 8.4 | 8.8 | 9.1 | 9.3 | 9.4 | derived from C |

**The headline is five and nine**: µ 0.6 → 3.0 doublings/h is **5×** and
ribosomes 8 → 73 × 10³ is **9×**. ppGpp falls about **ninefold** while the
per-gene rRNA initiation rate rises about **seventeenfold** — a repressor going
down while the thing it represses goes up, and the honest sentence is that one
observed quantity falls while a quantity *computed from the ribosome budget*
rises. Table 2, p. 6, gives the growth law directly as RNA/mass over
protein/mass: 0.057, 0.069, 0.086, 0.110, 0.140, 0.168 nucleotides per amino
acid across the same six columns — Scott's *r*, from a different laboratory,
thirty years earlier.

> **Every row we had before 25 October was wrong and wrongly labelled
> "measured".** The old values were transcribed from page scans that were never
> in the repository, and they were **read off by one column** — our µ = 2.5
> entries matched the table's µ = 3.0, and the r-protein row matched the next
> column along throughout. The old headline, *"a tenfold change in ribosomes
> across a fourfold change in growth rate"*, is not in the data either.
> **Anything still quoting "4× / 10×", 80% ribosome activity, or the old
> ribosome counts predates 25 October and is stale.**

**Why ribosomes at all.** RNA is ≈ **2/3** of a ribosome's mass and there are
**56** ribosomal proteins in bacteria (Milo & Phillips, *Cell Biology by the
Numbers*, 2015, printed p. 87 — a numbers reference, not a primary paper, and
its printed and PDF page numbers differ by two). About **85%** of *E. coli*'s
RNA is rRNA folded into ribosomes (Scott 2010 p. 1099), which is why an
RNA-to-protein ratio *is* a ribosome count read with a spectrophotometer. And
the machine makes itself — Scott 2014 p. 8: *"if ribosomes represent 30% of the
proteome in steady state, it also means that 30% of the ribosomes are engaged in
producing ribosomes."*

> **What is NOT sourced, and is given as background if at all:** the mass
> balance yields **proportionality**, while law 1 is affine (φ_R^min = 0.07),
> and it assumes a growth-rate-independent elongation rate, which Table 3
> contradicts below about µ = 1.5 (c_p rises 13 → 22 aa/s). **No paper in
> `private/readings/` argues "ribosomes are autocatalytic, therefore φ_R ∝ λ"**,
> and the session does not argue it either.

**ppGpp control of rRNA synthesis is FEEDFORWARD, not feedback.** The cell is
not counting ribosomes and correcting; it measures an upstream mismatch — amino
acid supply against the rate translation burns them — and acts ahead of the
consequence, which is session 10's architecture. The top chain is one passage of
Scott 2014, p. 6, flat bar included. **The antibiotic reversal is not in that
passage**: it is Scott 2010, p. 1100, and there it is hedged as *"implemented
POSSIBLY through the relief of repression"*, so the surface gives it as the
leading explanation rather than as settled — which means **law 2 is a
better-established observation than its own mechanism**. Trap recorded on the
surface: Scott 2010's Fig. 3B legend says ppGpp *"up-regulates ribosome
synthesis"*, which is loose wording for the *fall* in ppGpp doing the
up-regulating; the deck quotes the 2014 sentence instead.

### The instrument — Ceroni *et al.* 2015, the required reading

**Capacity is the GFP production rate per cell from a chromosomally integrated,
unregulated cassette, expressed as a percentage of untransformed cells (= 100%).**
The instrument is a synthetic strong constitutive promoter (**BBa_J23100**), a
synthetic RBS and codon-optimised superfolder GFP, integrated at the λ (pAH63)
locus — and segment 2 draws exactly that.

**The argument for the instrument is better than any single number in the
paper**, verbatim: capacity *"was substantially reduced compared to that of
uninduced cells **within 30 min** of operon induction, and this rapid change
contrasted with the **smaller, slower decreases in growth** … The observation
that a change in capacity **preceded** a change in growth rate after induction
… supports the view that decreased expression resources cause a decline in
growth rate."* **Growth rate is a lagging and blunt proxy for burden**, which is
why the session opens on the instrument rather than the algebra, and it is the
answer to "why not just weigh the cells". Also, for segment 6: *"Decreases in
capacity in both strains led to subsequent growth-rate decreases of similar
magnitude."*

The library is a gratuitous-protein experiment, which connects it straight to
Scott 2010: *"a library of inducible constructs that express a large protein
with **no function in our cells**"* — VioB fused to mCherry — varied by plasmid
copy number, core promoter, RBS strength, and codon optimisation against
de-optimisation.

| value | refers to | kind |
|---|---|---|
| ≈1.5-fold | output gain, mutated pBad over wild type | measured |
| ≈3-fold | output gain, strong vs weak RBS | measured |
| ≈5-fold | output gain, high vs medium copy | measured |
| **≈3.5-fold** | **capacity difference between scFv designs**, *"a close match to the simulation predicted increase"* | **measured** |
| >3-fold | capacity gain predicted for a shorter CDS | **simulated** |
| 26,300 | total ribosomes assumed in the simulation | **assumed** |

**The 3.5-fold is the strongest verified number in the paper and the better
teaching point anyway:** two designs, same growth rate, equivalent output,
3.5-fold different capacity. Growth rate alone would have told you nothing.

> **The per-construct capacity percentages live only in the plots** — there is
> no table of them in the text. Crop the panel; do not transcribe numbers off
> it, and do not read axis numbers out loud.
>
> **Panel letters, corrected 25 October.** Fig. 2 **(a)** is per-design bar
> charts, **(b)** is growth rate against capacity, **(c)** is **capacity
> against output** with the unattainable region shaded, and **(d)** is a
> simulated heat map. The slide and the reading's focus line are about **(c)**;
> an earlier crop labelled "2a" had picked up panel d's bold label from across
> the page gutter.
>
> **Fig. 1a trace readings, corrected 26 October.** At t = 120 min the capacity
> traces are black 9.3, blue 5.0, **red 5.2**, orange 1.6 (× 10³ GFP/h) — red
> is **on** blue, by construction, because red is the culture induced *at* 120
> minutes. The note used to say orange and red were both already far below, and
> that contradicted the projected figure on the surface the whole capacity
> argument rests on. Wording care on the same surface: the paper says capacity
> is *"reduced compared to that of uninduced cells"*, which is a gap between
> curves, not a fall — every trace is still rising.

### Shared resources, derived — T48

Quasi-steady state on ribosome binding, which is session 4's move with a
ribosome in the enzyme's place, gives

    R = R_T / (1 + Σ_j d_j)        and        p_i ∝ d_i / (1 + Σ_j d_j)

with demand d_i = m_i/K_i. **That denominator is session 6's partition function
with a different pool in it** — one weight on top, a sum over everything
competing underneath. In September the sum ran over binding configurations of
one operator; here it runs over the genes in the cell. Derived and checked in
`posb/resources.py` against integrating the full binding kinetics with
`posb.core`; 128 tests pass.

| gene 2's demand (× gene 1's) | gene 1's output falls by | kind |
|---|---|---|
| 0.25 | 11.1% | computed |
| 1 | 33.3% | computed |
| **4** | **66.7%** | **computed** |
| 16 | 88.9% | computed |
| 64 | 97.0% | computed |

**The fall is exactly a hyperbola** — p₁(d₂)/p₁(0) = 1/(1 + d₂/K_app) with
**K_app = 1 + d₁**, a Hill function in d₂ with exponent 1. It does not resemble
a dose–response; it *is* one, which is why the mistake is easy to make from real
data. **And that is the engineering payoff**, because K_app depends on the demand
of the gene being apparently repressed, and a real repressor's dissociation
constant does not. Fitted K comes out at **1.2, 2 and 6** for d₁ of 0.2, 1 and
5 — 1 + d₁ each time. So measure the apparent K at two expression levels of your
own reporter: **if it moves, you are looking at the pool.** No cloning required,
and a student could run it this semester.

**The isocost line.** Normalising each output by what it would reach alone **at
unlimited demand**, p₁ + p₂ = Σd/(1 + Σd), which contains no d₁ or d₂
separately — **verified constant to twelve figures across five splits at two
total demands.** At fixed total demand the achievable outputs lie on a straight
line; raising the total walks that line outward toward a bound it never reaches.
The qualifier is load-bearing: the identity is false if you normalise by what
each gene reaches alone *at its own demand*.

### Shared resources, measured — Gyorgy *et al.* 2015

Gyorgy, Jiménez, Yazbek, Huang, Chung, Weiss & Del Vecchio, *Biophys J*
**109**(3):639–646 (2015), open access. **The author is Gyorgy, not Györgyi.**

The isocost relation is their Eq. 1, modelled: *"αp₁ + βp₂ = Y … With the
available budget Y of ribosomes, the cell can produce p₁ units of p₁ at price α
and p₂ units of p₂ at price β"* — the same straight line `posb.resources.isocost_sum`
produces from the partition function. **The number the session turns on**,
measured by flow cytometry, mean ± SD of three independent experiments:
*"Induction of GapA with AHL has the same effect on GFP as inducing RFP,
**decreasing GFP production by up to 60%**."*

| plasmid copies | change in GFP | kind |
|---|---|---|
| 64 ± 2 | **60%** | measured |
| 18 ± 4 | **48%** | measured |
| 4 ± 1 | **29%** | measured |

The straight line was measured too: *"when plotting GFP over RFP we observe, as
predicted by the isocost line, a linear relationship … Further, when the RBS of
RFP becomes weaker, we observe that the slope becomes steeper."* **Which
resource is limiting — both, and the paper separates them:** the GFP decrease is
*"mostly attributable to the limited availability of ribosomes"*, but the
steepening slope *"cannot be predicted unless RNAP is limiting"*.

**And the pool has an edge, which is the best surface in the segment.** Two
GFPs, two experiments, and the contrast is deliberate and controlled:

| | GFP location | gapA induced → GFP |
|---|---|---|
| **Fig. 1B** | **chromosome** | **no effect** |
| **Fig. 1C** | **same plasmid** | **down up to 60%** |

*"although the expression of a gene (gapA) affects that of another gene on the
same plasmid (RFP), it has no effect on the steady-state expression of a third
gene located on the chromosome (GFP) … the pools of RNAP and ribosomes
available to the genes on the plasmid are essentially separated from those
available to the chromosomal genes."* **The null result is controlled, not an
absence of evidence**: they built MBP-tetR with chromosomal GFP and plasmid-borne
TetR *"to demonstrate that possible reductions to the chromosomal GFP expression
are detectable"*, and the MBP-dRFP control shows the decrease is *"not because
of the product RFP itself but rather to the process that produces RFP"*.

**So "the shared pool" has a boundary, and where it falls is an experimental
question, not a modelling assumption.** That is session 17's thesis from the
other side: there the boundary of a *part* had to be manufactured, here the
boundary of a *resource pool* has to be found. The two figures are a different
construct, not a matched pair, and the paper puts no percentage on the
same-plasmid drop in the chromosomal experiment — so none is quoted as though it
were. **Growth rate is not the explanation here**, verbatim: *"the rather modest
change in growth rate that we have observed in our experiments upon AHL
induction"*, with no numeric value given, which keeps this segment and segment 6
distinct.

Qian, Huang, Jiménez & Del Vecchio, *ACS Synth Biol* **6**(7):1263–1272 (2017)
gives the teachable shared denominator `1 + J₁ + J₂F₂(x₁) + J₃F₃(x₂)` across a
three-node cascade and an effective interaction graph with **non-regulatory
edges**. **No magnitude is recoverable from it** — the data are normalised to
each plot's maximum and its *"more than 60%"* is attributed to prior work. **Use
Gyorgy's 60%, not Qian's.**

### The price, in growth — T49

Scott 2010 models unnecessary protein and names the result, verbatim: *"We
modeled the expression of unnecessary protein (of mass fraction φ_U) as an
additional (neutral) component of the proteome … Equation 5 then predicts a
**linear reduction of the growth rate** … extrapolating toward zero growth at
**φ_c = ρ·(r_max − r_0) ≈ 0.48**."*

    λ(φ_U) / λ(0)  =  1 − φ_U / φ_c          with φ_c ≈ 0.48

| quantity | value | kind |
|---|---|---|
| φ_c, the zero-growth intercept | **≈ 0.48** | **stated in Scott 2010**, computed there from r_max |
| growth loss per 1% of proteome diverted | **≈ 2.1% of λ** | **our arithmetic**, 0.01/0.48 |
| growth arrest extrapolates at | ≈ 48% of the proteome | stated |

**The intercept is the paper's, not ours** — an earlier version of `NUMBERS.md`
reached 0.48 by subtracting 0.55 − 0.07 and labelled the whole thing "derived by
us"; the arithmetic was right, because φ_c *is* φ_R^max − φ_0, but the number did
not need deriving. **Only the per-1% slope is ours, and it is one division.**
That coefficient is what `posb.resources.dilution_coupled_steady_state` takes as
its required `growth_penalty` argument — **the function has no default,
precisely so this citation travels with it.**

And the model's claim is strong and falsifiable: **the cell charges you for the
space, not the amino acids, not the ATP per peptide bond, not the folding.**
Scott's Fig. 4B is where the lines were drawn before the data — the slope was
fixed in advance by an r_max fitted to a *different* experiment, and each line
is anchored at its own medium's zero-induction growth rate, so the accurate
claim is *"the slope was known before the points were"* rather than "no
adjustable parameters", which is what the paper itself says. Fig. 4C is where
the one-channel model survives: three proteins across four expression systems —
β-galactosidase twice from two promoters in two papers, plus β-lactamase and a
truncated EF-Tu — all falling together. A β-lactamase is exported to the
periplasm and a truncated EF-Tu is a misfolding hazard, and they cost the same
per percent of proteome. **The honest limit, said out loud: one organism, one
growth regime, a handful of proteins.**

> **Do not use Dong 1995 as the source of the linear slope.** Dong, Nilsson &
> Kurland, *J Bacteriol* **177**(6):1497–1504 (1995) is a transient, toxic,
> T7-driven overexpression reaching **30% of total bacterial protein** and
> ending in *"a cumulative breakdown of rRNAs … loss of ribosomes and protein
> synthetic capacity … the bacteria are no longer viable"*. Scott's relation is
> a steady-state balanced-growth law. Different regimes. Relatedly, Shachrai,
> Zaslaver, Alon & Dekel, *Mol Cell* 2010 find the cost of unneeded protein
> **falls after several generations**, so the cost is history-dependent.
>
> **What Dong 1995 IS good for**, p. 1500, measured: *"the heat shock proteins
> DnaK and GroEL increase by roughly 90 and 27%, respectively"* under
> gratuitous overexpression. Seen in 1995, mapped transcriptome-wide in 2018,
> **mechanism still open** — and Ceroni 2018 says so in as many words.

**And the loop closes on the circuit's own dynamics.** Session 5 derived
t½ = ln2/(γ + μ) and PS2 assessed it with μ taken as a number the medium hands
you. **μ is a property of the host's state and the circuit perturbs it**: induce
the circuit, divert ribosomes, growth slows, μ falls, and every protein in the
cell gets a longer effective lifetime, including the circuit's own. Nothing
about the DNA changed. **The direction is unambiguous and the magnitude is not**,
which is why the library asks the student for the penalty rather than assuming
one.

### Burden-driven feedback — Ceroni *et al.* 2018

*Nat Methods* **15**(5):387–393. The burden sensors are native **σ32-regulated**
promoters driving chaperone and protease genes — *ibpAB*, *dnaKJ*, *htpG*,
*groSL* — and **htpG1** alone drives the controller. **The dCas9 is constitutive
(BBa_J23113); it is the sgRNA that is burden-driven.** Measured: **11.7%
(pD864-LacZ) to 47.3% (pLys-M1)** of mapped RNA-seq reads came from the
synthetic construct 15 min after induction. What the dCas9 feedback recovered is
plotted only and **not verified**.

**Promoter induction, corrected 25 October.** Recorded previously as
"10- to 1000-fold in DH10B", which was wrong and was on a slide. The paper,
p. 389, verbatim: *"We observed increases in promoter activity of **up to
50-fold in DH10B cells and 10-fold in MG1655 cells**."* There is no
"1000-fold" anywhere in the paper.

> **And the mechanism is explicitly not claimed**, p. 389: *"These therefore act
> as intrinsic biosensors for synthetic-construct-induced burden in E. coli,
> although **the precise mechanisms behind their activation are not fully
> understood**."* The Discussion suggests chaperones may be an additional *kind*
> of burden rather than the sensing step. **So the familiar
> DnaK-titrated-off-σ32 story is textbook background, not this paper's claim**,
> and the ledger's speaker note says so if a student offers it.

### Growth feedback changes the circuit's own behaviour

**Klumpp, Zhang & Hwa, *Cell* 139(7):1366–1375 (2009) could not be obtained**
(Cloudflare, reCAPTCHA, rate-limited DOI). Only the abstract is verified, it
does support the framing, and **no number is taken from it.**

The verified open-access substitute, and arguably the better figure:
Berthoumieux, de Jong, Baptist, Pinel, Ranquet, Ropers & Geiselmann, *Mol Syst
Biol* 9:634 (2013), measured with GFP reporters in M9 + 0.3% glucose at 37 °C,
3–4 replicates. Verbatim: *"the activities of the genes encoding the
transcription factors Fis, Crp, and RpoS closely follow the activity of a
constitutively transcribed promoter."* They reproduced it with Klumpp's own ptet
promoter and the two agreed. **What looks like specific regulation is largely
global physiology** — and this one can be shown. Also measured there: plasmid
copy number *"increases up to a factor of 2"* across the growth transition, by
qPCR, which is a second reason a circuit's output moves when nothing in it
changed.

### The close — emergent bistability

**Tan, Marguet & You,** *Nat Chem Biol* **5**(11):842–848 (2009), read from the
NIH-PA author manuscript, so page numbers are manuscript pages. Verbatim:
*"a simple circuit consisting of mutant T7 RNA polymerase (T7 RNAP*) that
activates its own expression … **Although activation by the T7 RNAP* is
noncooperative, the circuit caused bistable gene expression.** This
counterintuitive observation can be explained by growth retardation caused by
circuit activation, which resulted in nonlinear dilution of T7 RNAP* in
individual bacteria."*

**Noncooperativity was measured, not assumed**, manuscript pp. 3–4: *"CFP
exhibited a Hill's coefficient of ~0.99 with respect to EYFP (Fig. S6),
**confirming the lack of cooperativity in T7RNAP***"*. That is stronger than "no
cooperative step appears in the diagram" and it closes off the obvious
objection.

**The ON fraction: 30% before dilution and 32% eight hours after**, read off the
rendered panel on 26 October; the Fig. 1c legend rounds both to *"~31% ON cells
both before dilution and 8 hours after dilution"*, and the main text gives no
figure at all. **Say: about a third before, about a third after — it did not
move.** A 25 October review had called 30/32 a fabrication on the strength of a
`pdftotext | grep`, `NUMBERS.md` §6 carried the accusation, and the deck surface
spent a whole annotation row explaining a non-discrepancy. All three are fixed.

> **Method note, kept because it cost three numbers this week.** Figure labels,
> axis annotations and anything set as part of an image are invisible to a text
> search. **Before writing "appears nowhere in the paper", render the panel and
> look at it.**

The model, reproduced and tested here, as published in Ochab-Marcinek,
*Eur Phys J E* (2012), Eq. 1, which states its parameters are *"identical to
those reported in"* Tan *et al.*:

    dx/dt = (δ + αx)/(1 + x)  −  φx/(1 + γx)  −  x

The symbols are confirmed from Tan 2009 itself: x is [T7 RNAP*], δ its basal
expression, α its effective synthesis rate constant (which *"increases with
[IPTG]"*, so the bifurcation axis is an inducer concentration), φ the maximum
growth rate, and γ the metabolic burden. And the controlled test is the paper's
own semantics: *"**If γ = 0, bacteria always divide at ϕ. If γ > 0, expression
of T7 RNAP* reduces the effective growth rate.**"*

| result | value | kind |
|---|---|---|
| expression term | Hill-1 in x — **no cooperativity anywhere** | by inspection |
| bistable window in α at γ = 10 | **5.575 to 18.425** — a factor of 3.30 | computed |
| separation of the two stable states | ~6,000 to 7,700× | computed |
| the three steady states at α = 14 | 0.0015, 0.06, 11 | computed |
| minimum burden for bistability at α = 14 | **γ = 2.22** | computed |
| **with γ = 0, so dilution is linear** | **one stable state at every α tested** | computed |

**The controlled test is the point:** set the burden parameter to zero, dilution
becomes linear, and the bistability disappears completely. The nonlinearity is
in the dilution term, not in the regulation — a noncooperative positive feedback
loop became bistable **because the host pushed back**.

**And the two edges of the window fail differently**, which is the design
consequence: at the low edge the ON state is born; at the high edge **the OFF
state is destroyed** — the low stable point and the unstable point annihilate at
α ≈ 18.42, leaving only the high state. **Drive the synthesis rate too hard and
you lose the ability to turn the circuit off** — and you lose it by turning a
knob that looks as though it should only make the signal stronger.

> **Still secondhand: the numeric parameter values** δ = 0.01, φ = 20, γ = 10.
> They reach us through Ochab-Marcinek 2012 quoting Tan; the equations in the
> Tan PDF render as images and the supplementary table was not reached. **The
> mechanism is reproduced and tested; the two figures are our reproduction of a
> published model, not a replication of Tan's figures**, and the surface says so
> once.
>
> Two errors of ours were caught while computing the window and are recorded
> because it goes on a slide: a bisection called with an inverted bracket
> returned its own midpoint (17.000) without iterating, and a second attempt
> asserted a monostable endpoint at α = 18 that is in fact bistable. Both were
> found by asserting that a bracket brackets.

**Why this is the right close.** Three sessions, three sources of the same
nonlinearity, and a student should be able to name all three by tonight:
session 9's **cooperative binding** (*"you choose it by choosing a protein"*),
session 18's **saturation of two opposing enzymes**, and session 19's **host** —
growth slows under load, dilution saturates, and a noncooperative circuit
becomes bistable.

## Coverage

| | |
|---|---|
| T48 | Build and simulate a shared-resource model — demonstrated here (segments 3–5), assessed on PS7 and the Final. **MIX** |
| T49 | Couple burden to growth rate — demonstrated here (segment 6), assessed on PS7 and the Final. **MIX** |
| T50 | Apply bacterial growth laws — demonstrated here (segment 1), **argued rather than computed**, which matches its HAND grading. ⚠ **See the gap below** |
| T42 | Compose parts in code, and compute where composition fails — demonstrated in S17 **and here**, assessed on PS7. **MIX** |
| T43 | Quantify context dependence of a part — demonstrated in S17 **and here**, assessed on PS7. **MIX** |

**⚠ T50 is an open gap in `docs/coverage-matrix.md` as it stands tonight.** The
growth laws are assessed only in the question that is **required for BioE 247
and extra credit for BioE 147**, so for the undergraduate cohort the row is not
assessed at all. Three fixes were considered — the final carries it for 147, an
undergraduate-facing item is added, or the row admits it is a 247 row — and on
**26 October it was added to the final's scope** as the cheapest of the three,
to be revisited when the final is written. **It is the only row in the matrix
currently marked ⚠.**

**T42 and T43 were reworded on 26 October and this session is half of why.**
T43's old item only *classified* context; it is now PS7's Q1, which
**quantifies** it. T42's *"compose a two-part system in code"* was a promise
session 17 did not keep — the compositor appeared as a diagram and no student
wrote one — so PS7 now has them **write the compositor and then compute how
wrong it is**, against **this session's** shared-pool mechanism: **a factor of
three on gene 1** at the demands used in class. The grading column moved from
AUTO to MIX because the interpretation is the point, and the demonstration is
S17's slide plus **S19's derivation**. **T48's grading is now MIX** for the same
reason. All of this was found by the F4.6 pass; `DESIGN.md` §6 predates it and
lists only T48, T49 and T50.

## Readings

| | |
|---|---|
| Required, read before today | Ceroni, Algar, Stan & Ellis, *Nat Methods* 12(5):415–418 (2015) — quantifying cellular capacity. 4 pp, handed out at the close of session 18 on 27 October. Focus line: *"the capacity-against-expression curve. Come able to state what is being measured in what units, because 'burden' is otherwise a word."* Paywalled with no deposit; the published PDF is in `private/readings/` |
| Optional | none assigned |
| Handed out today, for Tuesday | Fong & Palsson, *Nat Genet* 36(10):1056–1058 (2004) — gene-deletion strains evolving to computationally predicted phenotypes. 3 pp. Supplementary Table 1 and the predicted-against-observed comparison, **39 of 50 right**; come with a guess about what the eleven failures have in common |
| Cited, not assigned | Schaechter, Maaløe & Kjeldgaard 1958; Scott *et al.* 2010 and 2014; Bremer & Dennis 2008; Milo & Phillips 2015; Mori *et al.* 2017; Gyorgy *et al.* 2015; Qian *et al.* 2017; Dong, Nilsson & Kurland 1995; Shachrai *et al.* 2010; Ceroni *et al.* 2018; Berthoumieux *et al.* 2013; Tan, Marguet & You 2009; Ochab-Marcinek 2012 |
| Cited for its abstract only, and for no number | Klumpp, Zhang & Hwa, *Cell* 2009 — **could not be obtained** |

## Built

| | |
|---|---|
| Figures | **9 PNGs from `figures/s19_resources.py`, all nine placed**: `s19_ribosome_budget`, `s19_growth_law`, `s19_ppgpp_mechanism`, `s19_ppgpp`, `s19_hidden_edge`, `s19_isocost`, `s19_burden_cost`, `s19_rate_balance`, `s19_bifurcation`. `s19_ppgpp_mechanism` **replaced** a row stack that named uncharged tRNA, an alarmone and rRNA synthesis in a causal chain without any of those objects having been drawn — the worst bimodality failure in the deck; the figure is those rows with the things in them, and segment 1 did not grow. `s19_rate_balance` now states the stability argument on the figure rather than leaving it to the notes: the crossing is not the evidence, the slopes are |
| Paper figures | **12 declared** in `decks/paper_figures.yaml`, **10 placed**. `gyorgy2015_fig1ab` and `tan2009_fig2` are cropped and held in reserve; `ceroni2015_fig2a` is cropped, correct and deliberately `used_in: []` because **2c** is the panel the reading's focus line is about. The Scott Fig. 1 caption says *"ignore B's inset"*, and the Gyorgy Fig. 1A caption warns that **the GFP axis is inverted, 0 at the top** |
| Deck | `decks/s19_resources.py` → **42 slides**. `_cell_height` and `_paper` are ported from `decks/s18_protein.py` with their reasons: the first build had seven overlapping pairs, every one short by exactly one line, and three figures sitting small in large empty slots. The derivation run carries **no closing box**, and that is arithmetic rather than taste — `theme.derivation` switches asides on at pitch ≥ 0.70 but draws them from y+0.42 to y+0.86, so any run whose pitch lands in that window overlaps itself; a closing box at five steps gives a pitch of 0.78, and without it the pitch is 1.00 and the run is clean. **Reported to Adam as a `theme.py` threshold to fix (0.70 → 0.86)**, not patched here, because it touches every deck. Same for `theme.paper_figure`, which reserves its citation line at `TYPE["caption"]` and renders it at `scale(14)` |
| Handout + answers | `handouts/s19-resources.md` (4 pp PDF) — four items, all on one thesis, closing on a ledger the room fills in before the last ten minutes. Answers at `private/handouts/s19-resources-answers.md` (5 pp). **A separate posted version**, `private/handouts/s19-resources-answers-posted.md`, **withholds the hidden-edge and response-time keys because PS7 asks them almost unchanged** (4 pp); those two go up when the set is due |
| Board notes | `private/board-notes/s19-board-notes.md` (4 pp). **Four board moments** — session 6's denominator, written in the retrieval **from the room** and left up all period; the partition function at segment 3; the isocost sum at segment 5; and the correction to μ at segment 6, written on top of what went up in September. With ASK / CHECK / IF ASKED, and a **CUT order chosen now rather than in the room** |

**The mechanism that runs through three sessions is named here**, and a student
who leaves with burden, retroactivity and decoy titration as three unrelated
topics has missed the hour: a transcription factor held by decoy sites (S18), a
ribosome held by every other mRNA in the cell (S19), an upstream regulator held
by its own downstream targets (S21). **Session 20 is a different axis and the
close says so** — it is the same conservation argument over metabolites, with
the **S** matrix from session 3, not a fourth rung of the sequestration ladder.
The two were blurred on that surface before 26 October.

**One scope decision, recorded.** S19 does **not** take enzymatic synthesis,
syn1.0 or syn3A, which S17's design doc had moved here. Enzymatic DNA synthesis
is an assembly topic with no burden content, and minimal-gene-set reasoning
already has a home — **T68 is assigned to S25**. If the syllabus promise
matters it is one closing line in S17 pointing at S25, not a segment here.
