# Reading plan — sessions 11 to 28

[← back to README](../README.md) · [Readings](readings.md) · [Project papers](project-papers.md) · [Coverage audit](coverage-2025.md)

**Status: proposed, not adopted.** Nothing here is in `readings.yaml` except
session 25. Adam reviews, then it goes in and `tools/build_readings.py`
regenerates [readings.md](readings.md).

**The constraints this has to satisfy**, from `readings.yaml`:

- A paper discussed in class *N* is assigned at the end of class *N−1*. Never on
  the day.
- One required paper per assignment, **twelve pages maximum**, with a named
  figure to focus on. Exceptions must be declared per session with a reason.
- Fourteen days' notice at the outside, or they forget.

**The bar each paper had to clear**, tightened after the [coverage
audit](coverage-2025.md): somebody built the thing, there is a model simple
enough to re-derive, and there is something a student can compute with. Every
paper below is already verified in [project-papers.md](project-papers.md) with
its deposit checked, except where flagged.

---

## Part I — the three sessions before the midterm

### S11 · Thu Oct 1 · Oscillators
**Potvin-Trottier, Lord, Vinnicombe & Paulsson**, *Nature* 538, 514–517 (2016). 4 pp. [doi:10.1038/nature19841](https://doi.org/10.1038/nature19841) · free: PMC5637407

**Why this and not Elowitz & Leibler.** The 2000 repressilator is where the
circuit comes from and it has to be on the slide, but as a *reading* it teaches
the wrong lesson: it oscillates badly, and the session's question is what makes
an oscillator keep time. This paper is the same circuit with its noise sources
removed one at a time, so the reading is an argument about which term was
destroying the period — which is the session's argument. Assign Elowitz &
Leibler as optional background for the students who have not seen it.

**Focus.** The four modifications and what each one removes. Come able to say
which of them you would expect to matter most before you see the data.

### S12 · Tue Oct 6 · Noise
**Elowitz, Levine, Siggia & Swain**, *Science* 297, 1183–1186 (2002). 4 pp. [doi:10.1126/science.1070919](https://doi.org/10.1126/science.1070919)

**Why.** The two-colour decomposition is the session's whole apparatus, and it
is four pages. A designed two-reporter strain, built for the purpose — it meets
the brief even though it predates deposited data. **Flag: no data deposit, no
PMC.** Free access needs the library or the CaltechAUTHORS copy.

**Focus.** Figure 2 and the algebra that turns the difference between two
colours in one cell into intrinsic noise. Come able to say what is being held
equal, because that is what the whole decomposition rests on.

### S13 · Thu Oct 8 · The digital abstraction and its price
**Two papers, 11 pp total** — needs a `max_required_per_assignment: 2` override,
precedent being s09.

**Hooshangi, Thiberge & Weiss**, *PNAS* 102(10), 3581–3586 (2005). 6 pp. [doi:10.1073/pnas.0408507102](https://doi.org/10.1073/pnas.0408507102) · free: PMC552778
**Daniel, Rubens, Sarpeshkar & Lu**, *Nature* 497(7451), 619–623 (2013). 5 pp. [doi:10.1038/nature12148](https://doi.org/10.1038/nature12148)

**Why both.** The session now has two halves and they argue with each other.
Hooshangi is the digital half done honestly: a three-stage cascade, measured
Hill coefficients of 2.3, 7.0 and 7.5, and the noise that sharpening costs you —
so the students arrive having seen the price of the abstraction rather than
being told about it. Daniel is the alternative: the same Hill function used as
arithmetic instead of a switch, computing a ratio with three transcription
factors. Reading them together makes the session's claim — that digital is a
choice — something the students can already see. **Flag: Daniel is paywalled
with no PMC deposit.** If library access is awkward, it becomes the 247 paper
and Hooshangi stands alone.

**Focus.** Hooshangi Figure 2A, the transfer curves and their fitted Hill
coefficients. Daniel Figure 1 and the range over which the response is
logarithmic.

*S14 is review and S15 is the midterm. No reading.*

---

## Part II — engineering design

### S16 · Tue Oct 20 · Combinational and sequential logic
**Nielsen, Der, Shin, Vaidyanathan, Paralanov, Strychalski, Ross, Densmore & Voigt**, *Science* 352(6281), aac7341 (2016). [doi:10.1126/science.aac7341](https://doi.org/10.1126/science.aac7341)

**Why.** It is the paper the session is about — the compiler, the gate library,
and the honest failure rate. The alternative, Cello 2.0 (*Nat Protoc* 2022), is
a seventeen-page protocol: better for the project list, wrong for a reading.
**Flag: long, page count not verified, and Science blocked verification of its
data statement.** Assign a narrow figure range rather than the whole paper, and
declare a page override once the count is known.

**Focus.** The NOR gate response functions and the circuit-scoring rule. Come
able to say what "signal separation" means in the units of the previous
session's transfer curves — that continuity is the point of putting S13 before
this.

**The sequential half has no reading yet.** The natural candidates are the
recombinase-memory papers cited in the 2025 decks — Fernandez-Rodriguez et al.,
*ACS Synth Biol* 2015 (invertases), or a resettable-register paper — and none
of them has been verified. Alternatively the session leans on S9's toggle,
which the students already own, and assigns nothing extra. **Decision needed.**

### S17 · Thu Oct 22 · Parts in context, and assembly from oligos to genomes
**Chen, Liu, Nielsen, Brophy, Clancy, Peterson & Voigt**, *Nature Methods* 10(7), 659–664 (2013). 6 pp. [doi:10.1038/nmeth.2515](https://doi.org/10.1038/nmeth.2515)

**Why.** Five hundred and eighty-two terminators with measured strengths is the
cleanest demonstration in the field that a part is a number, not a name — which
is the session's thesis. It also hands the students an actual parts catalogue
in xlsx, which the project list needs and which nothing else on the course
supplies. **Flag: paywalled, no PMC.** Cambray et al. (*NAR* 2013, open access,
and Adam is an author) covers the same ground with a biophysical model and is
the fallback if access is a problem — or the 247 companion if it is not.

**Focus.** Table 1 and the design constraints: what makes a terminator strong,
and why context moves it.

### S18 · Tue Oct 27 · Protein circuits
**Mishra, Bepler, Teague, Berger, Broach & Weiss**, *Science* 373(6550), eaav0780 (2021). [doi:10.1126/science.aav0780](https://doi.org/10.1126/science.aav0780) · free: PMC11203391

**Why.** A toggle with no promoter in it. Everything the students proved in S8
and S9 — nullclines, the Jacobian, the bistable region — transfers unchanged,
but the timescale is seconds rather than hours and the parts are phosphorylation
sites. That transfer is the best argument available that they learned a method
and not a special case. **Flag: long, page count not verified.** Narrow focus
and a declared override.

**Focus.** The phospho-toggle network and its bifurcation analysis. Come able to
draw its phase plane on the S8 axes.

### S19 · Thu Oct 29 · Resource sharing and burden
**Ceroni, Algar, Stan & Ellis**, *Nature Methods* 12(5), 415–418 (2015). 4 pp. [doi:10.1038/nmeth.3339](https://doi.org/10.1038/nmeth.3339)

**Why.** Four pages, a capacity monitor in the cell, and a linear relationship
between what you express and what you take away from the host. It is the
cheapest possible way to make "your circuit is not alone" quantitative, and its
source data is deposited.

**Focus.** The capacity-against-expression curve. Come able to state what is
being measured in what units, because "burden" is otherwise a word.

### S20 · Tue Nov 3 · Metabolic engineering and constraint-based design
**Fong & Palsson**, *Nature Genetics* 36(10), 1056–1058 (2004). 3 pp. [doi:10.1038/ng1432](https://doi.org/10.1038/ng1432)

**Why.** Three pages in which a model predicts a growth rate, someone builds the
strain, evolves it, and checks — 39 of 50 right. It is the clearest example in
the course of a design calculation being tested rather than admired, and the
eleven failures are more interesting than the successes.

**Focus.** Supplementary Table 1 and the predicted-against-observed comparison.
Come with a guess about what the eleven have in common.

### S21 · Thu Nov 5 · Retroactivity and insulation
**Mishra, Rivera, Lin, Del Vecchio & Weiss**, *Nature Biotechnology* 32, 1268–1275 (2014). 8 pp. [doi:10.1038/nbt.3044](https://doi.org/10.1038/nbt.3044)

**Why.** Retroactivity is the most counter-intuitive idea in Part II — that
reading a signal changes it — and this paper puts a number on it: 76% of the
response time and 25% of the bandwidth, lost to a downstream load, and mostly
recovered by an insulating stage. The supplementary MATLAB is the model.

**Focus.** The delay and bandwidth measurements with and without the load
driver. Come able to say where the timescale separation is doing the work.

### S22 · Tue Nov 10 · Robustness and control
**Aoki, Lillacci, Gupta, Baumschlager, Schweingruber & Khammash**, *Nature* 570, 533–537 (2019). 5 pp. [doi:10.1038/s41586-019-1321-1](https://doi.org/10.1038/s41586-019-1321-1)

**Why.** Two molecules that annihilate each other are an integrator. That one
sentence is the session, and this is the paper that built it and measured the
adaptation. Source data deposited for the step responses.

**Focus.** The step-response figures and what "perfect" in perfect adaptation
is claiming. Then ask what dilution does to it — that is the session's argument.

### S23 · Thu Nov 12 · Evolutionary failure and containment
**Rottinghaus, Ferreiro, Fishbein, Dantas & Moon**, *Nature Communications* 13, 672 (2022). 10 pp. [doi:10.1038/s41467-022-28163-5](https://doi.org/10.1038/s41467-022-28163-5) · open access

**Why.** A kill switch is the one device whose specification is that it must not
evolve, and this one is tracked over 224 generations with the source data
published. The session's calculation — time to circuit failure from mutation
rate and fitness cost — has a measured answer to check against.

**Focus.** The viability-against-generations series. Fit an exponential before
class and bring the number.

**The 247 companion** is Chlebek et al., *NAR* 51(13), 7094–7108 (2023), open
access: the toxin encoded in the +1 frame of an essential gene, so that losing
the circuit costs the cell something. **Flag: 15 pp, over the cap — optional,
not required.** It supplies no model, which is what makes it a good project.

### S24 · Tue Nov 17 · Communities
**Balagaddé, Song, Ozaki, Collins, Barnet, Arnold, Quake & You**, *Molecular Systems Biology* 4, 187 (2008). 7 pp. [doi:10.1038/msb.2008.24](https://doi.org/10.1038/msb.2008.24) · open access

**Why.** Two strains, each holding the other's life in a quorum-sensing
molecule, with three dynamical regimes and bifurcations between them. It is
Lotka–Volterra that somebody built, and the model is deposited in BioModels
(BIOMD0000000296) so the students can run it rather than retype it.

**Focus.** The three regimes and what moves the system between them.

**The alternative**, if you want recent over canonical, is Li et al., *Methods
Ecol Evol* 13(7), 1608–1621 (2022) — programmable competition, mutualism or
exploitation, with a Zenodo CSV. **Flag: 14 pp, over the cap.**

### S25 · Thu Nov 19 · Design at population scale
**Weinberger, Schaffer & Arkin**, *J. Virol.* 77(18), 10028–10036 (2003). 9 pp. — **already in `readings.yaml`.**

**Why.** Six ODEs and the only closed-form threshold in the interfering-particle
literature, R₀ᵀ = P²D(1 − 1/R₀). Everything published since fits parameters
numerically. The session derives that threshold; the students should arrive
having seen where it comes from, and having worked out what P and D are
physically.

**The payoff, for the slide rather than the reading:** Pitchai et al.,
*Science* 385, eadn5866 (2024) — the same two knobs turned in macaques, R₀ ≈ 24
for HIV against ≈ 12 with TIPs present, with a public code repository. Twenty-one
years between the threshold and the animal.

### S26 · Tue Nov 24 · Therapeutic circuits
**Xie, Wroblewska, Prochazka, Weiss & Benenson**, *Science* 333(6047), 1307–1311 (2011). 5 pp. [doi:10.1126/science.1205527](https://doi.org/10.1126/science.1205527)

**Why.** A truth table implemented inside a HeLa cell, from six characterised
miRNA sensors. It is the session's worked example — a multi-input classifier
held to a false-positive budget — already done, which means the class period can
argue about the budget rather than explain the construction. **Flag: data is
"available on request"; no PMC deposit.**

**The alternative** is Tousley et al., *Nature* 615, 507–516 (2023) — the AND
gate built from native T-cell signalling, with single-cell RNA-seq at GEO. Ten
pages, mammalian, current. Choose by which failure mode you want to teach:
Xie's is selectivity, Tousley's is threshold sharpness.

### S27 · Tue Dec 1 · Machine learning as the specification layer
**Zhang, Wang, Xu, Wei, Liu, Hu & Wang**, *Nature Communications* 14, 6309 (2023). 11 pp. [doi:10.1038/s41467-023-41899-y](https://doi.org/10.1038/s41467-023-41899-y) · open access

**Why this rather than RFdiffusion.** The session's worked example is
design–filter–validate arithmetic: what hit rate beats directed evolution. This
paper designs promoters, synthesises them and measures them, in *E. coli* and in
mammalian cells, with the designed-and-measured set on Zenodo — so the hit rate
is in the reading. RFdiffusion (Watson et al., *Nature* 620, 1089–1100, 2023) is
the more famous paper and belongs on the slide, but its subject is protein
structure, which this course has not taught.

**Focus.** The designed-against-measured expression comparison. Come able to say
what fraction of designs worked, because that number is the session.

### S28 · Thu Dec 3 · Biosecurity and governance
**No candidate.** This is the one session with nothing proposed, and I will not
invent one. The session's stated subject — why sequence-similarity screening
fails on generated sequences — is recent and contested enough that the reading
should be chosen deliberately rather than pattern-matched. It is also the
session where a badly chosen reading does the most harm.

Three directions, none verified: a paper on the limits of nucleic-acid synthesis
screening; a red-team study of biodesign-tool safeguards; or a governance
document rather than a paper, read as a technical specification and criticised
as one. **Adam's call, and it needs a literature search of its own.**

---

## Summary of what needs deciding

| Session | Decision |
|---|---|
| S13 | Approve the two-paper override (11 pp total). Confirm Daniel is reachable through the library. |
| S16 | Page count and override for Nielsen 2016. **And whether the sequential half gets a reading at all.** |
| S17 | Chen (paywalled, better catalogue) or Cambray (open, your own paper) as the required one. |
| S18 | Page count and override for Mishra 2021. |
| S24 | Balagaddé (canonical, deposited model) or Li (recent, deposited data, over cap). |
| S26 | Xie (selectivity) or Tousley (threshold sharpness). |
| S28 | Everything. Needs its own search. |

Once these are settled the entries go into `readings.yaml` and
`tools/build_readings.py` regenerates the student-facing table. Nothing is
published to bCourses until then.
