# Session 20 — NUMBERS


> **SUPERSEDED IN PART, 26 October 2026.** The two-cause story below — one failure a missing route, the other a wrong objective — is NOT what Fong & Palsson conclude. Their only diagnosis covers BOTH genes and is network incompleteness (p. 1057). Eleven is 8 + 3: eight are ppc or tpi, three are single replicates the authors decline to diagnose. The model was also RIGHT about tpi on malate and succinate. The deck's segment 7 carries the corrected version; prefer it.
Read off the PDFs on **26 October 2026**: the 3-page article plus all three
supplementary files, which arrived that morning. **Record the kind, not only the
value** — for this session the kinds *are* the argument.

Held: `Session 20 - fong-palsson-2004-deletion-strains-evolve-to-predicted-phenotypes.pdf`
and its SI as `-SI-table1-uptake-rates`, `-SI-fig1-evolution-trajectories`,
`-SI-methods`.

---

## 1 · THE CENTRAL CLAIM, corrected by reading the supplementary methods

The headline number is **39 of 50 (78%)**, from the article's own abstract. But
the Supplementary Methods change what it is a claim *about*, and the corrected
form is the one that goes on the slide:

> **Given the experimentally measured substrate and oxygen uptake rates as
> inputs, flux balance analysis on a 904-gene, 1327-reaction *E. coli* model
> predicted the growth rate of 39 of 50 *evolved* deletion strains to within
> 10%.**

Three qualifications, each read off a page, each load-bearing:

| qualification | source |
|---|---|
| The uptake rates are **measured and fed in**, not predicted. *"For direct comparison with experimental strains, experimentally determined substrate and oxygen uptake rates were used as input parameters for the computational simulations."* The values are **Supplementary Table 1** | SI Methods, p. 1; SI Table 1 |
| The strains are **evolved**, not naive. Supplementary Fig. 1 is the time course — normalised growth rate against DAYS of evolution (0-50) for each replicate on each substrate | abstract; SI Fig. 1 |
| **"Right" means within 10%** — Fig. 1's arrows mark the strains that deviate by more than that | Fig. 1 caption |

**So the model is handed its own boundary conditions and asked for one number.**
That is a real and useful result, and it is *not* "the genome predicts growth."
Any slide that drops a qualification is wrong in the way the week-9 and week-10
retrospectives are about.

## 2 · Supplementary Table 1 — the model's inputs, measured

mmol/g-DW/hr. SUR = substrate uptake rate, OUR = oxygen uptake rate. **Kind:
measured.**

| carbon source | SUR | OUR |
|---|---|---|
| α-ketoglutarate | 13 | 17 |
| glucose | 10 | 17 |
| glycerol | 17 | 19 |
| lactate | 20 | 30 |
| malate | 17 | 19 |
| ribose | 10 | 15 |
| succinate | 13 | 17 |

**`readings.yaml`'s focus note is wrong about this table.** It says *"Supplementary
Table 1 and the predicted-against-observed comparison."* Supplementary Table 1 is
**not** the comparison — it is the uptake rates. The comparison is **Figure 1** in
the article, and the evolution time course is **Supplementary Figure 1**. Focus
note corrected the same day; the table is still worth sending students to,
because *noticing that these are measured inputs* is the whole qualification in §1.

## 3 · The design

**Kind: design.** Six in-frame deletions, built by homologous recombination with
the λ red system in *E. coli* K-12 MG1655 (SI Methods):

| gene | enzyme (article's own wording, p. 1056) |
|---|---|
| **ackA** | acetate kinase A |
| **frd** | fumarate reductase |
| **pck** | phosphoenolpyruvate carboxykinase |
| **ppc** | phosphoenolpyruvate carboxylase |
| **tpi** | triosephosphate isomerase |
| **zwf** | glucose 6-phosphate-1-dehydrogenase |

**50 evolved strains** across substrates. Supplementary Fig. 1 labels the
replicates: ack1–2, frd1–2, pck1–3, ppc1–2, tpi1–2, zwf1–2.

**The model: 904 genes, 1327 reactions** (SI Methods) — iJR904, which is Reed,
Vo, Schilling & Palsson, *Genome Biol* 4, R54 (2003), held as an instructor
companion. A knockout is simulated by **deleting the reactions associated with
the gene from the reaction list**, which is the paper's own description and is
exactly the one line of code session 20 teaches.

## 4 · The eleven failures, and they do NOT share a cause

**Kind: measured against predicted.** This is the payoff surface.

| failure | what went wrong | kind |
|---|---|---|
| **tpi⁻** on lactate, malate, succinate | **No growth was computationally predicted at all**, and the strains grew. A route the reconstruction does not have | predicted (structural failure) |
| **ppc⁻** on α-ketoglutarate, both replicates | Grew **11–12% slower than predicted**. The network is right and the objective is slightly wrong | measured vs predicted (quantitative) |

`readings.yaml` asks students to come with a guess about what the eleven failures
have in common. **They do not have one thing in common**, and that is the better
lesson: one is a gap in the network, the other is a gap in the objective, and
neither is fixed by adding constraints.

## 5 · Where Ibarra 2002 comes in

**Ibarra, R. U., Edwards, J. S. & Palsson, B. O., *Nature* 420, 186–189 (2002)** —
Fong's reference 4, held as an instructor companion, author list read off the
page. Title: *"Escherichia coli K-12 undergoes adaptive evolution to achieve in
silico predicted optimal growth."*

This is the paper that licenses session 20's thesis. Fong & Palsson shows the
agreement; Ibarra shows the **mechanism** of the agreement — a population
starting at a sub-optimal growth rate moving onto the line of optimality in the
phenotype phase plane. **Without it, "flux balance predicts where selection
goes" is our sentence. With it, it is a citation.**

## 6 · The teaching network — BUILT AND VERIFIED 26 October

`posb.fba.teaching_network()`. **9 reactions, 6 balanced metabolites**, two
external (acetate, CO₂), glucose uptake capped at 10 as the only numerical
constraint. Every real reaction balances carbon, and there is a test asserting
it, because the session's thesis is that **S** counts atoms exactly.

| reaction | stoichiometry | C |
|---|---|---|
| v_uptake | → G6P | source |
| v_pgi | G6P → F6P | 6 → 6 |
| v_zwf | G6P → P5P + CO₂ | 6 → 6 |
| v_tpi | F6P → 2 T3P | 6 → 6 |
| v_lower | T3P → PYR + ATP | 3 → 3 |
| v_ackA | PYR → Ace + CO₂ + ATP | 3 → 3 |
| v_tca | PYR → 3 CO₂ + 3 ATP | 3 → 3 |
| v_biomass | 2 T3P + P5P + 4 ATP → | sink |
| v_atpm | ATP → | sink |

### The board gets it in six lines, and the answers are integers

```
P5P   one producer, one consumer          ->  v_zwf   = b
G6P   10 = v_pgi + v_zwf                  ->  v_pgi   = 10 - b
F6P   one producer, one consumer          ->  v_tpi   = v_pgi      [COUPLED]
T3P   2 v_tpi = 2b + v_lower              ->  v_lower = 20 - 4b
ATP   all pyruvate to the TCA (3 vs 1):   4(20 - 4b) >= 4b
                                          ->  b <= 4
```

**Optimum: biomass = 4 exactly.** v_pgi = v_tpi = 6, v_zwf = 4,
v_lower = v_tca = 4, **v_ackA = 0**, v_atpm = 0. ATP: 4 + 12 = 16 = 4 × 4,
balanced. Confirmed by `linprog` to 10⁻⁹.

**The branch point goes all-or-nothing** — v_ackA is exactly 0 because the TCA
yields 3 ATP against acetate's 1. That is a vertex, which is where every linear
program's optimum sits, and it is why FBA never predicts a graded split.

### Knockouts, all exact

| knockout | biomass | why |
|---|---|---|
| wild type | **4** | — |
| v_pgi, v_zwf, v_tpi, v_lower | **exactly 0** | no other route to T3P, to P5P or to ATP |
| **v_tca** | **10/3** | the optimum moves to a different vertex; acetate now carries all the pyruvate. Same six lines: 2(20 − 4b) ≥ 4b → b ≤ 10/3 |
| v_ackA, v_atpm | 4 | unused at the optimum, so free to lose |

The four lethal ones are the structural case — the shape of Fong & Palsson's
tpi⁻ strains, for which **no growth was computationally predicted at all** on
lactate, malate and succinate.

### Coupling

**v_pgi / v_tpi = 1.0000 exactly.** F6P has one producer and one consumer, so
the network has already fixed this ratio and no regulation can change it. That
is the honest definition of flux coupling and it is visible by inspection, which
is the right way to meet it first.

### Alternate optima — executable, not asserted

Adding `v_zwf2`, a route with stoichiometry identical to v_zwf, **leaves the
optimal biomass at 4** and makes the split between the two completely free:
flux variability reports both over **[0, 4]**. The solver returns one of them
and says nothing; no growth measurement can distinguish them.

This is **Mahadevan, R. & Schilling, C. H., *Metab Eng* 5, 264–276 (2003)**,
*"The effects of alternate optimal solutions in constraint-based genome-scale
metabolic models"* — Fong's reference 12, held, title and authors read off page
1. The slide cites it rather than asserting the limitation.

⚠ **v_zwf2 is a modelling device and the deck must say so.** *E. coli* has a
single glucose-6-phosphate dehydrogenase; there is no real duplicate of v_zwf.
An exactly degenerate pair is constructed because it makes the tie
hand-checkable. Real redundancy of this kind exists — parallel
electron-transport branches, duplicated transhydrogenases — and that is where
alternate optima come from in practice. Recorded in the function's docstring
too, so the caveat travels with the code.

### Library state

`posb.fba`: `FluxModel` (with external metabolites and a null-space dimension),
`solve_fba`, `knockout_growth`, `flux_ranges` (flux variability),
`coupled_pairs`, `has_alternate_optima`, `teaching_network`. **16 test
functions.** One of them asserts that `fba`'s **S** equals `posb.core.Model`'s
**S** for the same network — the session is sold as session 3's matrix re-asked,
and that test is the sentence made literally true.
