# Project papers — the curated list

[← back to README](../README.md) · [Syllabus](syllabus.md) · [Readings](readings.md)

This is the list the first project milestone draws on. Pick one paper, answer
four questions about it, and the fourth answer is your project.

**Why a list at all.** The milestone used to ask for a project description in
week 5 — the system, the objective, why it is interesting. That is the neck of
the hourglass, and it asks you to have done the literature narrowing that
section 1 of the final document exists to teach. Nobody can do it in week 5,
and the ones who try write either a restatement of a paper or a proposal with
no model under it. So the milestone now asks for something you can actually do
after four weeks of this course, and this list is what makes it possible: every
paper here is a synthetic system somebody designed and built, with a model
simple enough to re-derive, and something downloadable to compute with.

**The two tracks.** A strict "the data must be downloadable" rule would delete
every landmark in the field, because nobody deposited data before about 2010.
It would delete the toggle switch. So the rule here is *something machine-readable
must exist*, and that comes in two kinds:

- **Track A — data to fit.** Numbers you can download and fit a model to.
  Supplementary tables, source-data files, a Zenodo or GEO deposit. The project
  shape is: re-fit their model, then ask it something they did not ask.
- **Track B — a model to run.** No downloadable measurements, but a deposited
  SBML model or a parameter set complete enough in the paper to rebuild. The
  project shape is: rebuild the model, then explore where it goes that the
  paper stopped short of.

Track B is not the lesser track. Track A projects are judged partly on data
handling, which some of you have and some of you don't. Track B projects are
judged on whether you asked a good question — and PS4 is already a Track B
project in miniature: you took Gardner's published parameters, turned one knob
they did not turn, and a stable state died.

**What is not on this list.** Papers where the data is "available on request",
papers with figures and nothing behind them, and review articles. If you want
to work on a paper that is not here, bring it — the bar is the same three
things: somebody built it, there is a model, and there is something you can
download.

Papers marked **[reading]** are also assigned in class, so you will meet them
anyway. Choosing one of those is not a shortcut; it means your question has to
go further than the lecture does.

---

## Track A — download the data, fit the model, ask it something new

### 1. Cambray et al. 2013 — intrinsic transcription terminators
*Cambray, G., Guimaraes, J. C., Mutalik, V. K., Lam, C., Mai, Q.-A., Thimmaiah, T., Carothers, J. M., Arkin, A. P. & Endy, D.* Measurement and modeling of intrinsic transcription terminators. **Nucleic Acids Research** 41(9), 5139–5148 (2013). [doi:10.1093/nar/gkt163](https://doi.org/10.1093/nar/gkt163) · open access · 10 pp · *session 17*

**Model.** A free-energy model of hairpin and U-tract strength, fit to measured termination efficiencies — reducible to a two-parameter logistic in sequence features.
**Data.** Supplementary Tables S1–S6: terminator sequences and measured strengths, construct and strain tables, RNA-folding output, and the fitted model coefficients themselves.
**The question in the figure.** Table S1 gives the measured strengths and Table S6 the coefficients. Hold out a subset of terminators, re-fit on the rest, and predict the held-out ones. Where the model fails, ask what sequence feature it is blind to.

### 2. Cameron & Collins 2014 — tunable protein degradation
*Cameron, D. E. & Collins, J. J.* Tunable protein degradation in bacteria. **Nature Biotechnology** 32, 1276–1281 (2014). [doi:10.1038/nbt.3053](https://doi.org/10.1038/nbt.3053) · free copy: Harvard DASH · 6 pp · *session 18*

**Model.** Mass-action degradation through an inducible protease: rate = k_cat[protease]/(K_M + [substrate]), so protein half-life becomes a dial.
**Data.** Source Data files (xlsx) for Figures 1–4; Supplementary Table 2 (degron library); GenBank KM521207–KM521212.
**The question in the figure.** Fit the Michaelis–Menten form to the Fig. 2 source data (degradation rate against inducer), then predict the circuit response time for a degron in Table 2 they did not put in a circuit. This is session 5's γ + µ with γ under your control.

### 3. Ceroni et al. 2015 — the burden monitor
*Ceroni, F., Algar, R., Stan, G.-B. & Ellis, T.* Quantifying cellular capacity identifies gene expression designs with reduced burden. **Nature Methods** 12(5), 415–418 (2015). [doi:10.1038/nmeth.3339](https://doi.org/10.1038/nmeth.3339) · 4 pp · *session 19*

**Model.** A resource-allocation balance: monitor output falls in proportion to the load a heterologous construct puts on shared transcription and translation.
**Data.** Source Data for the flow-cytometry figures; Supplementary Software (zip); six supplementary tables.
**The question in the figure.** Fit the linear burden model to the capacity-against-expression source data, then ask what it predicts for a construct whose expression is split across two plasmids — and whether the linear form should survive that.

### 4. Mishra et al. 2014 — the load driver
*Mishra, D., Rivera, P. M., Lin, A., Del Vecchio, D. & Weiss, R.* A load driver device for engineering modularity in biological networks. **Nature Biotechnology** 32, 1268–1275 (2014). [doi:10.1038/nbt.3044](https://doi.org/10.1038/nbt.3044) · 8 pp · *session 21*

**Model.** Retroactivity as an ODE problem: a phosphotransfer stage exploits timescale separation to buffer a downstream load. Measured cost of not having it — 76% delay in response time, 25% bandwidth lost.
**Data.** Supplementary Code: the MATLAB ODE models and plotting scripts (~19 MB). Plasmids GenBank KM457485–KM457490.
**The question in the figure.** Run their own code to reproduce the delay and bandwidth curves, then push the load ratio past anything they tested and find where the driver stops helping.

### 5. Aoki et al. 2019 — antithetic integral feedback, built
*Aoki, S. K., Lillacci, G., Gupta, A., Baumschlager, A., Schweingruber, D. & Khammash, M.* A universal biomolecular integral feedback controller for robust perfect adaptation. **Nature** 570, 533–537 (2019). [doi:10.1038/s41586-019-1321-1](https://doi.org/10.1038/s41586-019-1321-1) · 5 pp · *session 22*

**Model.** Sigma and anti-sigma factor annihilate each other; that one reaction is an integrator, and integral feedback gives robust perfect adaptation. Two or three ODEs.
**Data.** Source Data (xlsx) for Figures 2–3 and Extended Data Figures 4–8; plasmids MK775703–MK775710. (Strains and some code are request-only; the source data is not.)
**The question in the figure.** Fit the controller ODEs to a step-response source-data file and recover their adaptation time. Then ask what breaks it: dilution is the standard answer, so quantify how fast the cell must grow before perfect adaptation stops being perfect.

### 6. Rottinghaus et al. 2022 — kill switches that survive
*Rottinghaus, A. G., Ferreiro, A., Fishbein, S. R. S., Dantas, G. & Moon, T. S.* Genetically stable CRISPR-based kill switches for engineered microbes. **Nature Communications** 13, 672 (2022). [doi:10.1038/s41467-022-28163-5](https://doi.org/10.1038/s41467-022-28163-5) · open access · 10 pp · *session 23*

**Model.** Viable fraction against generations — an escape-rate problem. Fit an exponential and you have a mutation rate with a selection coefficient on it.
**Data.** Source Data file with the underlying values.
**The question in the figure.** Fit a decay model to the 224-generation viability series and back out the escape rate. Then compare it to the spontaneous mutation rate the course uses in session 23 (~2 × 10⁻¹⁰ per bp) and say what the difference means.

### 7. Chlebek et al. 2023 — entangling the circuit with an essential gene
*Chlebek, J. L., Leonard, S. P., Kang-Yun, C., Yung, M. C., Ricci, D. P., Jiao, Y. & Park, D. M.* Prolonging genetic circuit stability through adaptive evolution of overlapping genes. **Nucleic Acids Research** 51(13), 7094–7108 (2023). [doi:10.1093/nar/gkad484](https://doi.org/10.1093/nar/gkad484) · open access · *session 23*

**Model.** None supplied — you build it. Escape ratio over ~130 generations, with the toxin encoded in the +1 frame of an essential gene so that losing it costs the cell something.
**Data.** BioProject PRJNA970322 (whole-genome sequencing); Supplementary Tables S1–S4 including the observed mutations; Addgene 201531–201535.
**The question in the figure.** Build the selection model the paper does without, using Table S3's mutation spectrum, and predict how much entanglement buys you — then check it against their measured escape ratios. The absence of a model is the opportunity here.

### 8. Li et al. 2022 — consortia with programmed interactions
*Li, S., Xiao, J., Sun, T., Yu, F., Zhang, K., Feng, Y., Xu, C., Wang, B. & Cheng, L.* Synthetic microbial consortia with programmable ecological interactions. **Methods in Ecology and Evolution** 13(7), 1608–1621 (2022). [doi:10.1111/2041-210X.13894](https://doi.org/10.1111/2041-210X.13894) · *session 24*

**Model.** Quorum-sensing modules wired to produce competition, mutualism or exploitation on demand — two-species population dynamics of the Lotka–Volterra kind.
**Data.** Zenodo record 6471034 and Dryad [doi:10.5061/dryad.gmsbcc2qh](https://doi.org/10.5061/dryad.gmsbcc2qh), CC0, including `ModelIcompetition.csv`.
**The question in the figure.** Fit a two-species competition model to the deposited time series and locate the coexistence boundary as a function of induction strength. Then ask which parameter an experimenter could actually move.

### 9. Fong & Palsson 2004 — FBA predicted it, then they evolved it
*Fong, S. S. & Palsson, B. Ø.* Metabolic gene-deletion strains of Escherichia coli evolve to computationally predicted growth phenotypes. **Nature Genetics** 36(10), 1056–1058 (2004). [doi:10.1038/ng1432](https://doi.org/10.1038/ng1432) · *session 20*

**Model.** Genome-scale flux balance analysis, predicting the growth rate a deletion strain will reach after adaptive evolution. It matched in 39 of 50 cases.
**Data.** Supplementary Table 1 (substrate and oxygen uptake rates) and Supplementary Figure 1 (growth trajectories).
**The question in the figure.** Rebuild the prediction in COBRApy on a published *E. coli* model using the Table S1 uptake rates. The interesting subset is the eleven that did not reach the predicted optimum — ask what they have in common, and what that says about what FBA assumes.

### 10. Riglar et al. 2017 — a memory circuit living in a mouse
*Riglar, D. T., Giessen, T. W., Baym, M. et al.* Engineered bacteria can function in the mammalian gut long-term as live diagnostics of inflammation. **Nature Biotechnology** 35, 653–658 (2017). [doi:10.1038/nbt.3879](https://doi.org/10.1038/nbt.3879) · 6 pp · *session 26*

**Model.** A recombinase memory element: switching is a probability per unit time given an inducer, and retention is a decay over 200 days in a host that is selecting against you.
**Data.** BioProject PRJNA380756; RefSeq NZ_CP016007–009; SRA SAMN06671873 / SAMN06671878.
**The question in the figure.** Estimate circuit loss rate in vivo from the sequencing data, and connect it to the session 23 mutation-rate calculation. A circuit that works and a circuit that stays working are different engineering problems.

### 11. Tousley et al. 2023 — an AND gate built from native signalling
*Tousley, A. M., Rotiroti, M. C., Labanieh, L. et al.* Co-opting signalling molecules enables logic-gated control of CAR T cells. **Nature** 615, 507–516 (2023). [doi:10.1038/s41586-023-05778-2](https://doi.org/10.1038/s41586-023-05778-2) · 10 pp · *session 26*

**Model.** LINK CAR splits the signal across LAT and SLP-76, so two antigens are required — a two-input threshold, writable as a Hill-type AND.
**Data.** GEO GSE216286 (single-cell RNA-seq); construct sequences in Supplementary Table 1. Constructs themselves are MTA-only.
**The question in the figure.** From GSE216286, separate activation states under single- against dual-antigen conditions and ask how sharp the AND actually is. A gate with a soft threshold kills the wrong cell; quantify the softness.

### 12. Watson et al. 2023 — RFdiffusion
*Watson, J. L., Juergens, D., Bennett, N. R. et al.* De novo design of protein structure and function with RFdiffusion. **Nature** 620, 1089–1100 (2023). [doi:10.1038/s41586-023-06415-8](https://doi.org/10.1038/s41586-023-06415-8) · 12 pp · *session 27*

**Model.** The design model is a diffusion network, but the model *you* build is the cheap one: a classifier over design metrics that predicts which designs bound their target.
**Data.** Designs, AlphaFold2 models and experimental measurements on figshare (`https://figshare.com/s/439fdd59488215753bc3`); code at github.com/RosettaCommons/RFdiffusion; structure PDB 8SK7 / EMDB-40557.
**The question in the figure.** Using the Figs. 4–5 binder screens across five targets, fit a logistic model on the computational metrics and ask how well they predict experimental success. The honest answer is usually "worse than the paper's framing suggests" — that result is a project.

### 13. Zhang et al. 2023 — DeepSEED promoter design
*Zhang, P., Wang, H., Xu, H., Wei, L., Liu, L., Hu, Z. & Wang, X.* Deep flanking sequence engineering for efficient promoter design using DeepSEED. **Nature Communications** 14, 6309 (2023). [doi:10.1038/s41467-023-41899-y](https://doi.org/10.1038/s41467-023-41899-y) · open access · 11 pp · *session 27*

**Model.** A sequence-to-expression model used generatively: design flanking sequence, synthesise, measure. Designed promoters were tested in *E. coli* and in mammalian cells.
**Data.** Zenodo [doi:10.5281/zenodo.8307150](https://doi.org/10.5281/zenodo.8307150); Supplementary Data 1–3.
**The question in the figure.** Train something deliberately simple — k-mer regression — on part of the *E. coli* set and test on held-out designs. Then ask what the deep model buys over the simple one, in the units that matter: designs synthesised per success.

### 14. Jones et al. 2022 — Cello 2.0, and the gate library behind it
*Jones, T. S., Oliveira, S. M. D., Myers, C. J., Voigt, C. A. & Densmore, D.* Genetic circuit design automation with Cello 2.0. **Nature Protocols** 17, 1097–1113 (2022). [doi:10.1038/s41596-021-00675-2](https://doi.org/10.1038/s41596-021-00675-2) · free copy: MIT DSpace · 17 pp · *sessions 13 and 16*

**Model.** Every gate is a Hill function with four fitted numbers (y_min, y_max, K, n); a circuit is those functions composed through a Boolean netlist, scored by worst-case signal separation. This is the digital abstraction with the numbers attached.
**Data.** Zenodo [doi:10.5281/zenodo.4676314](https://doi.org/10.5281/zenodo.4676314) — the UCF gate libraries, input sensors and output devices. Also github.com/CIDARLAB/Cello-UCF, `files/v2/ucf/**/*.UCF.json`.
**The question in the figure.** Pull the Hill parameters for a handful of gates, predict the ON/OFF separation of a two-input NOR you compose yourself, and compare against Cello's own score. Session 13 does this by hand for two gates; this is the same calculation with a library behind it.

---

## Track B — rebuild the model, then take it somewhere the paper stopped

### 15. Gardner, Cantor & Collins 2000 — the toggle switch **[reading]**
*Gardner, T. S., Cantor, C. R. & Collins, J. J.* Construction of a genetic toggle switch in Escherichia coli. **Nature** 403, 339–342 (2000). [doi:10.1038/35002131](https://doi.org/10.1038/35002131) · 4 pp · *sessions 8 and 9*

**Model.** Two repressors, each in the other's denominator. Four parameters, one inequality, and a bifurcation.
**Model deposit.** BioModels **BIOMD0000000507** (`Gardner2000 - genetic toggle switch in E.coli`), SBML, runnable. The Nature page offers one supplementary PDF and no data.
**The question.** PS4 already did the first one for you — pIKE105's bistable band, and what one ssrA tag costs. Everything left over from that problem set is a project: the six variants are six points in a design space you can now draw, and only some of them are where the paper says they are. Start from what the design-space figure of session 8 cannot explain.

### 16. Rosenfeld, Elowitz & Alon 2002 — negative autoregulation, measured **[reading]**
*Rosenfeld, N., Elowitz, M. B. & Alon, U.* Negative autoregulation speeds the response times of transcription networks. **J. Mol. Biol.** 323(5), 785–793 (2002). [doi:10.1016/S0022-2836(02)00994-4](https://doi.org/10.1016/S0022-2836(02)00994-4) · 9 pp · *session 7*

**Model.** Rise time against repression ratio — the curve you derive at the board in session 7, measured in two strains that differ by one edge.
**Data.** Figures only; the parameters to rebuild Figure 2 are in the paper. [Track B]
**The question.** The speed-up is bought with a stronger promoter. Rebuild Figure 2 and then price it: how much extra expression per unit of speed-up, and at what point does session 19's burden model say you have spent more than you gained? Nobody in 2002 could ask that; you have Ceroni.

### 17. Basu et al. 2004 — the pulse generator **[reading]**
*Basu, S., Mehreja, R., Thiberge, S., Chen, M.-T. & Weiss, R.* Spatiotemporal control of gene expression with pulse-generating networks. **PNAS** 101, 6355–6360 (2004). [doi:10.1073/pnas.0307571101](https://doi.org/10.1073/pnas.0307571101) · 6 pp · *session 10*

**Model.** An incoherent feedforward loop with one fast arm and one slow one; pulse height and width follow from the ratio.
**Data.** Figures only; the circuit and its timescales are specified in the paper. [Track B]
**The question.** Session 10 asks what happens if you swap which arm is fast. Build it, then ask the design question the paper does not: for a target pulse width, what is the set of parameter pairs that delivers it — and which of those pairs is robust to the cell growing faster?

### 18. Balagaddé et al. 2008 — a predator–prey ecosystem
*Balagaddé, F. K., Song, H., Ozaki, J., Collins, C. H., Barnet, M., Arnold, F. H., Quake, S. R. & You, L.* A synthetic Escherichia coli predator–prey ecosystem. **Molecular Systems Biology** 4, 187 (2008). [doi:10.1038/msb.2008.24](https://doi.org/10.1038/msb.2008.24) · open access · 7 pp · *session 24*

**Model.** Two strains, each holding the other's life in a quorum-sensing molecule. ODEs with three regimes and bifurcations between them.
**Model deposit.** BioModels **BIOMD0000000296** (`Balagadde2008_E_coli_Predator_Prey`), SBML.
**The question.** Reproduce the three regimes and find the bifurcation boundary in the AHL-induced killing rate. Then ask the engineering question: the oscillation regime is the interesting one and also the narrow one — how much parameter drift does it survive before the consortium collapses to one strain?

### 19. Breuer et al. 2019 — the metabolism of a minimal cell
*Breuer, M., Earnest, T. M., Merryman, C. et al.* Essential metabolism for a minimal cell. **eLife** 8, e36842 (2019). [doi:10.7554/eLife.36842](https://doi.org/10.7554/eLife.36842) · open access · *session 25*

**Model.** A metabolic reconstruction of JCVI-syn3A: 493 genes, and 98% of the enzymatic reactions backed by annotation or direct experiment.
**Data.** Supplementary files including transposon insertion positions, gene essentiality calls, and the FBA stoichiometry detail. **[unverified: whether any supplementary file is a machine-readable SBML/COBRA model. syn3A is *not* in BiGG — checked. Confirm before choosing this one.]**
**The question.** Build a stoichiometric model of one subsystem — nucleotide salvage is the tractable one — and ask which genes called essential are only conditionally so, under a medium they did not use. A minimal cell is a claim about a medium as much as about a genome.

### 20. Potvin-Trottier et al. 2016 — the repressilator that kept time
*Potvin-Trottier, L., Lord, N. D., Vinnicombe, G. & Paulsson, J.* Synchronous long-term oscillations in a synthetic gene circuit. **Nature** 538, 514–517 (2016). [doi:10.1038/nature19841](https://doi.org/10.1038/nature19841) · free: PMC5637407 · 4 pp · *session 11*

**Model.** The repressilator with its noise sources removed one at a time — the paper is an argument about which term was destroying the period.
**Data.** Plasmids on Addgene (confirmed). The data statement says segmented single-cell traces are online; **[unverified: I could not locate the repository. Check with the Paulsson lab before relying on the traces.]** Treat as Track B: rebuild from the published circuit.
**The question.** Elowitz & Leibler's 2000 repressilator loses phase within a few generations; this one does not. Rebuild both and identify, in the model, the single change that accounts for the difference — then ask what it predicts for a four-repressor ring, which nobody has needed to build.

---

## What was screened out, and why

Four of the assigned readings do not meet the brief and are not project sources,
though they remain assigned:

- **Phillips & Milo 2009** — an argument about estimation. Nothing was built.
- **Bintu et al. 2005** — a methods review. The framework, not a system.
- **Mangan & Alon 2003** — a taxonomy of motifs in natural networks. It explains
  why Basu's circuit has the shape it has; it is not itself a built thing.
- **Alon 2007** — a review, and optional even as a reading.
- **Andersen et al. 1998** — four measured half-lives, which is a part
  characterisation rather than a system. Kept as a reading, and Cameron &
  Collins (#2) is the project-sized version of the same idea.

Three landmarks are absent for a stated reason. **Elowitz & Leibler 2000** (the
repressilator) and **Elowitz et al. 2002** (intrinsic and extrinsic noise) have
no deposited data and no deposited model; #20 covers the first, and the second
has no adequate replacement — see the gaps below. **Nielsen et al. 2016** (Cello
1.0) is superseded for this purpose by #14, which carries the same gate model
with a verified Zenodo deposit.

## Gaps — where this list is still thin

Three areas where nothing found meets the bar, and where a better paper would be
worth adding:

1. **Noise (session 12).** No paper found combines a built reporter library with
   downloadable single-cell distributions. Deloupy et al. 2020 (Sci Adv) was the
   best candidate and its numbers live inside a PDF, with the rest on request.
2. **Oscillators with data (session 11).** #20 is Track B for the same reason.
3. **The digital abstraction as measured devices (session 13).** #14 supplies
   fitted gate parameters, which is the abstraction's output; no verified deposit
   of raw measured transfer curves was found.

---

*Verification note. Every DOI, accession and deposit above was checked against
the publisher or repository record on 20 September 2026, and anything that could
not be confirmed is marked `[unverified]` rather than smoothed over. Two entries
carry such marks. If you find one of them is wrong, say so — that is a useful
thing to have found, and it is the same skill the project is testing.*
