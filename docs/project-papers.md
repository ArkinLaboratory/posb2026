# Project papers — the curated list

[← back to README](../README.md) · [Syllabus](syllabus.md) · [Readings](readings.md)

This is the list the first project milestone draws on. Pick one paper and
answer three things: what they built and what model sits behind their main
figure, what **you** would build that their result makes possible, and what you
would have to compute to know whether your thing could work.

That second answer is the point. The projects that work in this course are
designs — a thing that should exist, with a model showing how it would be
implemented, how it would behave, and whether it is feasible. A paper is not
the assignment; it is the ground you stand on so that the design is about
something real. Every entry below therefore ends with **Build with** — the
parts, parameters or characterised components that paper hands you to
recombine. That line, not the data line, is usually the one you will use.

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
  Supplementary tables, source-data files, a Zenodo or GEO deposit.
- **Track B — a model to run.** No downloadable measurements, but a deposited
  SBML model or a parameter set complete enough in the paper to rebuild.

Either track supports a design. Track A lets you calibrate your design against
somebody's measurements; Track B lets you simulate it from their parameters.
What neither lets you do is design in the air, which is the failure mode this
milestone exists to prevent.

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

## Papers the course itself teaches from

Added 20 September after the [coverage audit](coverage-2025.md) found that the
twenty above were chosen from the 2026 topic list and a literature search, and
so missed the papers this course has actually lectured from. These five are
strong on **Build with** and weaker on downloadable data — which, for a design
project, is the right trade.

### 21. Chen et al. 2013 — 582 terminators, measured
*Chen, Y.-J., Liu, P., Nielsen, A. A. K., Brophy, J. A. N., Clancy, K., Peterson, T. & Voigt, C. A.* Characterization of 582 natural and synthetic terminators and quantification of their design constraints. **Nature Methods** 10(7), 659–664 (2013). [doi:10.1038/nmeth.2515](https://doi.org/10.1038/nmeth.2515) · 6 pp · *session 17*

**Model.** Termination strength from hairpin thermodynamic stability and its displacement of the U-tract from the DNA/RNA hybrid, fit to the measured set.
**Data.** Supplementary Tables 2, 3 and 4 as **.xlsx** — 227 natural and 265 synthetic terminators with measured fold-repression. Paywalled main text; library access needed.
**Build with.** The strongest parts catalogue on this list. Tables 2 and 3 give you a sequence and a measured strength for nearly 500 terminators, 39 of them above 50-fold. If your design needs two genes at a fixed expression ratio, or an operon whose downstream gene must be insulated from its neighbour, you can pick the actual parts and predict the ratio before building anything.

### 22. Hooshangi, Thiberge & Weiss 2005 — ultrasensitivity down a cascade
*Hooshangi, S., Thiberge, S. & Weiss, R.* Ultrasensitivity and noise propagation in a synthetic transcriptional cascade. **PNAS** 102(10), 3581–3586 (2005). [doi:10.1073/pnas.0408507102](https://doi.org/10.1073/pnas.0408507102) · free: PMC552778 · 6 pp · *sessions 12 and 13*

**Model.** A Gillespie simulation of a TetR→LacI→CI repression cascade with every rate constant given in Methods, plus steady-state transfer curves fit to a Hill form.
**Data.** Figures and SI only — no deposit. [Track B]
**Build with.** The Methods section is a parts list with numbers: transcription 2 min⁻¹ unoccupied and 0.02 min⁻¹ occupied, translation 2 min⁻¹, dimerisation 0.03 nM⁻¹min⁻¹, and decay rates. Figure 2A gives measured Hill coefficients of 2.3, 7.0 and 7.5 for one-, two- and three-stage cascades. You can build a cascade of your own topology from these constants and ask what it costs you in noise to buy that sharpness — which is the trade every design on this list eventually meets.

### 23. Xie et al. 2011 — a truth table inside a HeLa cell
*Xie, Z., Wroblewska, L., Prochazka, L., Weiss, R. & Benenson, Y.* Multi-input RNAi-based logic circuit for identification of specific cancer cells. **Science** 333(6047), 1307–1311 (2011). [doi:10.1126/science.1205527](https://doi.org/10.1126/science.1205527) · 5 pp · *session 26*

**Model.** Individually measured miRNA sensor dose-responses, composed as a Boolean expression — miR-21 AND miR-17-30a AND NOT(miR-141) AND NOT(miR-142(3p)) AND NOT(miR-146a) — used to predict classifier selectivity before the circuit was built.
**Data.** "Available upon request"; Tables S1–S6 are supplementary PDF. [Track B]
**Build with.** Six characterised sensor modules with measured responses across seven cell lines (Fig. 2D, Tables S1 and S3). This is a classifier construction kit: pick a different target cell, choose the miRNAs that separate it, and compute the false-positive rate your logic would give — the worked example of session 26, on a cell type of your choosing.

### 24. Mishra et al. 2021 — a toggle with no promoter in it
*Mishra, D., Bepler, T., Teague, B., Berger, B., Broach, J. & Weiss, R.* An engineered protein-phosphorylation toggle network with implications for endogenous network discovery. **Science** 373(6550), eaav0780 (2021). [doi:10.1126/science.aav0780](https://doi.org/10.1126/science.aav0780) · free: PMC11203391 · *session 18*

**Model.** Bistability from mutual cross-repression between two MAPK phospho-signalling branches, analysed by numerical bifurcation and stochastic simulation — no closed form was tractable.
**Data.** Main text and supplementary materials; no deposit. [Track B]
**Build with.** Eleven named phospho-in/phospho-out parts — chimeric fusions plus endogenous high-osmolarity MAPK components — and the bifurcation analysis in supplementary notes 1.5–1.6.7 as a template. Session 9's phase plane transfers to this system unchanged, but the timescale is seconds rather than hours, which makes a different class of design possible. Ask what you would build that needs to switch in seconds.

### 25. Daniel, Rubens, Sarpeshkar & Lu 2013 — arithmetic, not logic
*Daniel, R., Rubens, J. R., Sarpeshkar, R. & Lu, T. K.* Synthetic analog computation in living cells. **Nature** 497(7451), 619–623 (2013). [doi:10.1038/nature12148](https://doi.org/10.1038/nature12148) · 5 pp · *session 13*

**Model.** Computation in the logarithmic domain — log-linear sensing, addition, ratiometric and power-law operations — from three transcription factors, over about four orders of magnitude.
**Data.** Supplementary Information is a PDF of 53 figures and 4 tables. Paywalled, no PMC deposit. **[unverified: whether SI Tables 1–4 contain reusable transfer-function parameters. Confirm before choosing this one.]** [Track B]
**Build with.** The idea more than the parts: the Hill function you derived in session 4 is a logarithm over the right range, so a circuit that computes a ratio needs three transcription factors rather than a gate array. Any design that must report *relative* concentration — a sensor that fires on the ratio of two metabolites rather than a threshold of one — starts here.

### 26. Pitchai et al. 2024 — a conditional parasite, in macaques
*Pitchai, F. N., Tanner, E. J., Khetan, N., Vasen, G., Levrel, C., Kumar, A. J. et al.* Engineered deletions of HIV replicate conditionally to reduce disease in nonhuman primates. **Science** 385(6709), eadn5866 (2024). [doi:10.1126/science.adn5866](https://doi.org/10.1126/science.adn5866) · free: PMC11545966 · *session 25*

**Model.** A within-host ODE for SHIV, extended so that TIPs are explicit obligate molecular parasites competing for Gag, with conditional replication stated as R₀^TIP > 1. Reported: R₀ ≈ 24 for HIV alone, ≈ 12 with TIPs present. Fit by nonlinear least squares and MCMC.
**Data.** The best on this list. Code at [github.com/khetanneha/HIV-SIV-TIP-Modeling](https://github.com/khetanneha/HIV-SIV-TIP-Modeling), archived at Zenodo [10.5281/zenodo.11391302](https://doi.org/10.5281/zenodo.11391302) — the archive holds the modelling and visualisation code under GPLv3 plus `Pitchai_et_al_ExperimentalData_File.xlsx`. Sequences at GenBank PP597405–PP597522 and PP646066–PP646153. **The only paper here with a runnable public repository.**
**Build with.** Table S1 and Fig. 2A give the actual constructs: the original ~2.5 kb *pol–vpr* deletion, TIP-1 with cPPT restored, TIP-2 with *tat/rev/vpu/env* ablated, and the optimised HIV-TIP carrying two smaller deletions. Measured: 94% titre reduction in vitro (Fig. 1C), R₀^TIP by three-colour flow (Fig. 2E–F), 3–4 log₁₀ plasma viral load reduction sustained about thirty weeks (Fig. 3C, 3E). You can design a different deletion and ask what it does to R₀^TIP. The sibling paper for a respiratory virus is Chaturvedi et al., *Cell* 184, 6022–6036.e18 (2021) — SARS-CoV-2 TIPs, GEO GSE184447, Zenodo 5579847, measured R₀ ≈ 1.57 — with a heavier two-compartment model.

### 27. Chaturvedi et al. 2022 — one dose, and it blocks transmission
*Chaturvedi, S., Beutler, N., Vasen, G., Pablo, M., Chen, X., Calia, G., Buie, L., Rodick, R., Smith, D., Rogers, T. & Weinberger, L. S.* A single-administration therapeutic interfering particle reduces SARS-CoV-2 viral shedding and pathogenesis in hamsters. **PNAS** 119(39), e2204624119 (2022). [doi:10.1073/pnas.2204624119](https://doi.org/10.1073/pnas.2204624119) · free: PMC9522362 · *session 25*

**Model.** Eight states — T, E, I, V for the virus, mirrored for the TIP — with about seven parameters including ρ = 1.5 (relative TIP production) and ψ = 0.02 (suppression). Single compartment. Genuinely a one-week build.
**Data.** All data, code and materials at Zenodo [record 6762604](https://zenodo.org/record/6762604).
**Build with.** The transmission-blocking experiment itself (Fig. 1B): infect source animals, treat, cohouse with contacts, measure shedding and onward transmission. That design is the bridge between the within-host model and the between-host one, and it is the natural thing to turn into a stochastic exercise. If you want the population scale done properly, Metzger, Lloyd-Smith & Weinberger, *PLoS Comput Biol* 7, e1002015 (2011) carries the three-scale model with risk-structured mixing.

### 28. Weinberger, Schaffer & Arkin 2003 — where the threshold came from
*Weinberger, L. S., Schaffer, D. V. & Arkin, A. P.* Theoretical design of a gene therapy to prevent AIDS but not human immunodeficiency virus type 1 infection. **Journal of Virology** 77(18), 10028–10036 (2003). [doi:10.1128/JVI.77.18.10028-10036.2003](https://doi.org/10.1128/JVI.77.18.10028-10036.2003) · free: PMC224590 · 9 pp · *session 25*

**Model.** Six ODEs — uninfected cells, HIV-infected, TIP-infected, dually infected, free virus, free TIP — and two composite design parameters: *D*, the antiviral inhibition, and *P*, the TIP's packaging advantage. Out of it falls a closed form, **R₀ᵀ = P²D(1 − 1/R₀)**, the condition for the therapy to persist.
**Data.** Figures only; the 2003 supplementary URL is dead. [Track B]
**Build with.** Table 1 is the whole parameter set — production and death rates, burst size ≈ 200, clearance ≈ 30/day, T₀ = 800/µl — with the swept ranges. Six equations and one formula, rebuildable from the paper text alone. This is the object session 25 derives, and it is the only closed-form R₀ in the whole TIP literature: everything after it fits parameters numerically. The design question it poses is still open — P and D are the two knobs, the paper draws the surface over them (Fig. 3), and #26 is what twenty-one years of trying to move those knobs produced.

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

Two areas where nothing found meets the bar, and where a better paper would be
worth adding:

1. **Oscillators with data (session 11).** #20 is Track B because its
   single-cell trace repository could not be located.
2. **The digital abstraction as measured devices (session 13).** #14 supplies
   fitted gate parameters, which is the abstraction's output; no verified deposit
   of raw measured transfer curves was found.
Noise (session 12) was a gap here until #22 closed it, and population-scale
design (session 25) until #26–#28 did. The review that looked like the obvious
candidate there — Tanner, Kirkegaard & Weinberger, PLoS Genet 2016 — has no
model, no parameters and no data; it stays a reading.

---

*Verification note. Every DOI, accession and deposit above was checked against
the publisher or repository record on 20 September 2026, and anything that could
not be confirmed is marked `[unverified]` rather than smoothed over. Two entries
carry such marks. If you find one of them is wrong, say so — that is a useful
thing to have found, and it is the same skill the project is testing.*
