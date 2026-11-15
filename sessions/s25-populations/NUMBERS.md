# Session 25 — every number, with its kind

**Design at population scale: defective interfering particles, TIPs, gene drives.**
Thu 19 November 2026. Thesis: the thing you are engineering is supposed to spread.

Sources. Page numbers are **PDF pages** of the files in `private/readings/`;
where a paper prints its own journal page numbers I give both.

| tag | file | pages |
|---|---|---|
| **W03** | `Session 25 - weinberger-schaffer-arkin-2003-gene-therapy-to-prevent-aids.pdf` — Weinberger, Schaffer & Arkin, *J. Virol.* 77(18):10028–10036 (2003). REQUIRED. | 9 (journal 10028–10036) |
| **N18** | `Session 25 - noble-2018-gene-drives-invasive-OPTIONAL.pdf` — Noble, Adlam, Church, Esvelt & Nowak, *eLife* 7:e33423 (2018). OPTIONAL. | 30 incl. appendix |
| **HB70** | `Session 25 - huang-baltimore-1970-defective-viral-particles-OPTIONAL.pdf` — Huang & Baltimore, *Nature* 226:325–327 (1970). OPTIONAL. | 3 (journal 325–327) |

PDF page *p* of W03 = journal page 10027 + *p*. So Table 1 is PDF p.4 = journal 10031.

Kinds used here, exactly as the brief specifies: **MEASURED** (measured in an
experiment), **QUOTED** (the authors state it, citing someone else),
**MODELLED** (out of their simulation, fit or sweep — not an instrument),
**DERIVED** (follows analytically from stated equations), **COMPUTED** (we
calculated it from their numbers; arithmetic shown), **INFERRED BY US** (a
judgement call of ours, flagged).

> **W03 is a theory paper.** Almost nothing in it is MEASURED. Table 1's own
> reference column separates parameters taken from measurement from the two
> that are marked engineerable-but-never-measured-in-vivo. Section 2 gets that
> distinction right row by row, and it is the difference between *this is what
> HIV does* and *this is what somebody would have to build*.

> **Figure-panel caution.** Everything below that comes from inside a figure
> panel was read by rendering the page at 300–600 dpi and looking at it, and
> digitized against the **printed tick labels**. `pdftotext` does not see
> W03's figures at all — they are embedded rasters. It *does* see N18's,
> which are vector; N18 panel values below were still checked by eye.

---

## 0 · THE ONE THING THE BRIEF ASKED TO SETTLE — the Basic Model R₀ denominator

**Resolution: the paper prints a Greek delta. The printed formula is wrong.
The denominator that follows from the paper's own equations, and the only one
that reproduces the paper's own results, is *c·d*.**

**What is printed.** W03 p.6 (journal 10033), right column:

> R₀ = λkn/cδ

The last glyph was read at 400 dpi, magnified 3×, against the Latin *d* in
"spread" one line above. It has no straight ascender and carries the looped
top-left stroke of lowercase **δ**. There is no ambiguity in the rendering.
**KIND: QUOTED (what the page says).**

**What the equations give.** Fig. 1 (W03 p.3, journal 10030) prints the model.
Setting equations 1–3 to zero with V_T = I_T = I_D = 0:

    T* = c/(kn)                     from [2] and [3]
    R0 = (lambda/d) / T* = lambda*k*n/(c*d)

**KIND: DERIVED.** The *d* enters through the uninfected-cell steady state
T₀ = λ/d; δ cancels, exactly as it does in the standard Nowak–May result.

**The arithmetic, both ways, from Table 1 (λ=31, k=1.875e-4, n=200, c=30,
d=0.02, δ=0.7). KIND: COMPUTED.**

    with d:      31 * 1.875e-4 * 200 / (30 * 0.02)  =  1.9375
    with delta:  31 * 1.875e-4 * 200 / (30 * 0.70)  =  0.05536

**Three independent checks, all of which pick *d*. KIND: COMPUTED.**

1. **λ/d = 31/0.02 = 1550 cells/µl**, and Fig. 2c's inset shows total
   non-HIV-infected cells (T + I_T) climbing to about **1500 cells/µl** — the
   paper calls that "consistent with healthy individuals" (p.4). The healthy
   T-cell level in this model *is* λ/d.
2. **T\* = c/(kn) = 30/(1.875e-4 × 200) = 800.0 cells/µl exactly**, which is
   Table 1's T₀. And λ = dT\* + δI\* = 0.02(800) + 0.7(21.43) = **31.0
   exactly**, with I\* = cV\*/(nδ) = 21.43 cells/µl giving V\* = 100
   virions/µl = **10⁵ virions/ml exactly**, which is Table 1's V₀. λ and k are
   not independent data: they are back-solved so that the model sits on
   T₀ = 800 and V₀ = 10⁵. The paper says so in one line on p.5 (journal
   10032): "λ and k were calculated by steady-state analysis".
3. **The threshold reproduces the paper's own stated number.** With
   R₀ = 1.9375, 1 − 1/R₀ = 0.48387, so R₀ᵀ > 1 needs P²D > 2.0667. At the
   paper's stated optimum D ≈ 0.2 that is **P > 3.21** — and the text (p.5,
   journal 10032) says crHIV-1 reaches coexistence "as P is increased in value
   beyond ~3". With δ in the denominator, R₀ = 0.055 < 1, so 1 − 1/R₀ =
   **−17.06** and R₀ᵀ is negative for every P and D. The paper's own figures
   could not exist.

**So: δ in the printed formula is a typographical or transcription error for
*d*.** Record it that way. The session can use it — it is a two-line
dimensional-consistency check a student can do, and it is the instructor's own
paper, so nobody is being embarrassed.

**Where the derivation of R₀ᵀ itself lives: the SI, and we do not have it.**
W03 p.6 says R₀ᵀ = P²D(1 − 1/R₀) has "the following form (derived in the SI)".
The SI URL printed in the paper is `http://genomics.lbl.gov/suppinfo/JVI/index.html`
(Table 1 footnote *a* and five places in the text). **We did not retrieve it
and did not search the web.** `docs/project-papers.md` says that URL is dead.
So: **the R₀ᵀ derivation is not in the assigned PDF.** This file used to mark
it `[unverified]` and name two routes out: locate the 2003 SI, or re-derive
R₀ᵀ from equations 4–6 by next-generation matrix on the I_T → I_D → V_T loop.
**The second route was taken on 7 November 2026 and it closes. See §18.** The
published form is exactly right, the threshold is exactly 31/15, and no
assumption beyond the paper's own printed text is needed to get there. The SI
is no longer load-bearing for anything this session teaches.

---

## 1 · The six equations, as W03 writes them — QUOTED (Fig. 1, p.3 / journal 10030)

Read off the rendered figure, symbol for symbol. Overdots are W03's own.

    [1]  dT/dt    =  lambda - d*T - k*V*T - k*VT*T
    [2]  dI/dt    =  k*V*T - delta*I
    [3]  dV/dt    =  n*delta*I - c*V + D*n*delta'*ID
    [4]  dIT/dt   =  k*VT*T - d*IT - k*V*IT
    [5]  dID/dt   =  k*V*IT - delta'*ID
    [6]  dVT/dt   =  P^2*D*n*delta'*ID - c*VT

State variables (W03 p.2, journal 10029):

| symbol | what it is |
|---|---|
| **T** | uninfected CD4⁺ T cells |
| **I** | productively HIV-1-infected T cells |
| **V** | free HIV-1 virions |
| **I_T** | therapeutically infected cells — carry an integrated crHIV-1, produce no virus, "functionally equivalent to T cells" |
| **I_D** | dually infected cells — produce both HIV-1 and crHIV-1 |
| **V_T** | free crHIV-1 therapy virions |

Equations 1–3 in the **red box** are the Basic Model plus exactly two added
terms: −kV_T T in [1], and Dnδ′I_D in [3]. Equations 4–6 in the **blue box**
are new. W03 states this on p.2.

**Structural points a session must not lose, all DERIVED from the above:**

- **I_T dies at rate *d*, not δ** ([4]). The therapy vector alone is not
  cytopathic; an I_T cell is a healthy cell. This is why T + I_T, not T, is
  the clinically relevant count.
- **I_T can be superinfected by HIV ([4], −kVI_T), but I_D cannot be
  superinfected.** W03's reason (p.2): HIV Nef downregulates CD4, so an
  HIV-infected cell resists superinfection — but I_T carries no Nef, so HIV
  can still get in. The whole therapy runs through that asymmetry.
- **D multiplies the crHIV output as well as the HIV output.** It is in [3]
  *and* in [6]. This single fact is the paradox of §5.
- **δ′ cancels.** W03 p.6: viral production and cell death are reciprocally
  linked, so δ′ drops out of every steady state except I_D's. **DERIVED**, and
  the paper verifies it algebraically.
- **The crHIV-to-HIV burden ratio at steady state.** From [3] and [6] at
  steady state, V_T*/V* = P² · [Dnδ′I_D] / [nδI + Dnδ′I_D] ≤ **P²**, with
  equality only when I → 0. **DERIVED.** At P = 30 that upper bound is 900;
  Fig. 2b's P = 30 traces settle at roughly 9×10² (HIV) and 3.5×10⁵ (crHIV),
  a ratio near 390, so singly-infected I cells are still carrying a large
  share of HIV production at the new set point.

## 2 · Table 1, row by row, with the kind the paper's own reference column implies

W03 p.4 (journal 10031). The reference column is the thing to get right.
`††` is W03's own footnote: *"crHIV-1 can be genetically engineered to change
the value of this parameter (see the text), but in vivo measurements have not
been carried out."* `†` means dimensionless.

| symbol | biological meaning | value | units | W03 ref | **KIND** |
|---|---|---|---|---|---|
| **λ** | birth rate constant of uninfected CD4⁺ T cells | 31 | cells µl⁻¹ day⁻¹ | 45 (Phillips 1996) | **DERIVED** — see note below; *not* measured |
| **d** | death rate of uninfected CD4⁺ T cells | 0.02 | day⁻¹ | 36 | **QUOTED** |
| **k** | infection rate of activated CD4⁺ T cells per virion | 1.875 × 10⁻⁴ | µl virion⁻¹ | **"No data"** | **DERIVED** — back-solved, see below |
| **δ** | death rate of HIV-1-infected cells (I) | 0.7 | day⁻¹ | 21, 51 (Ho 1995; Ramratnam) | **QUOTED** |
| **δ′** | death rate of dually infected cells (I_D) | δ′ = D × δ | day⁻¹ | `††` | **MODELLED** — an assumption, relaxed in the SI via a function F(δ,n) we do not have |
| **n** | burst size: virions released from an HIV-1-infected cell | 200 | † dimensionless | 17 (Haase 1996) | **QUOTED** |
| **c** | clearance rate of V and V_T virions | 30 | day⁻¹ | 21, 47 | **QUOTED** |
| **P** | fold increase in crHIV-1 mRNA concentration vs. HIV-1 mRNA in the cytoplasm of an I_D cell | **1–100** (swept) | † dimensionless | `††` | **ENGINEERING TARGET — never measured in vivo** |
| **D** | antiviral effect: fractional therapeutic downregulation of HIV-1 virion production from I_D cells | **0.0–1.0** (swept) | † dimensionless | `††` | **ENGINEERING TARGET — never measured in vivo** |
| **T₀** | initial concentration of uninfected CD4⁺ T cells in plasma | 800 | cells/µl | 40 (Nowak & May) | **QUOTED** |
| **V₀** | initial HIV-1 set point, before crHIV-1 | 10⁵ | virions/ml | 40 | **QUOTED** |

**Ranges also tested (Table 1 footnote *a*), all MODELLED sweeps, reported as
not changing the qualitative result:** λ 20–50; k 10⁻³ to 10⁻⁵; δ 0.4–0.9;
n 100–1,000; T₀ 500–1,200; V₀ 10⁴–10⁷. **And: "analytical studies that did not
include the viral eclipse phase used c = 3 instead of c = 30."**

### 2a · λ and k are not data, and Table 1 half-hides it — DERIVED, then INFERRED BY US

Table 1 gives λ a literature reference and marks k "No data". But the body
text, p.5 (journal 10032), says: *"λ and k were calculated by steady-state
analysis"*. Our §0 arithmetic confirms both to the last digit: k = c/(nT₀) =
30/(200 × 800) = 1.875 × 10⁻⁴ exactly, and λ = dT₀ + δI\* = 31.0 exactly with
I\* set by V₀. **COMPUTED.**

**INFERRED BY US, and worth a slide:** two of the eleven rows look like
measurements and are not. They are *fitted so that the model passes through
the clinical observables T₀ = 800 and V₀ = 10⁵*. The consequence is that
**R₀ = 1.9375 is not an independent prediction — it is (λ/d)/T₀ = 1550/800**,
i.e. the ratio of the healthy CD4 count to the set-point CD4 count. That is a
genuinely nice result and it is also a tautology given how k and λ were
chosen. Say both.

### 2b · One more parameter is a sentence, not a row

**Viral eclipse phase ≈ 1.5 days** between infection of a cell and the start
of virion production — **QUOTED** (W03 p.1 citing ref 35; p.4 citing ref 38).
It is in the simulations ("equations 1 to 6 were altered accordingly, see SI")
but it has no Table 1 row and the altered equations are in the SI we do not
have. `[unverified]` — the altered equations would be settled by the SI.
W03 states neglecting it "did not alter the qualitative behavior" (p.4).

---

## 3 · P and D: what they are physically, and what you would change to move them

The session turns on these being the two knobs. W03 defines both twice, in the
Theory section (p.2, journal 10029) and in Table 1.

### P — the packaging advantage

**Definition.** "the intracellular concentration of crHIV-1 mRNA relative to
HIV-1 mRNA" (p.2). An **intracellular** parameter. By definition the
cytoplasmic HIV-1 : crHIV-1 mRNA ratio in an I_D cell is **1 : P**.
Swept **1 to 100**.

**What you change in the construct to move P** — W03 p.7 (journal 10034)
names four routes, all QUOTED from the cited literature:

| route | effect claimed | ref |
|---|---|---|
| remove the vector's splice signals, raising the proportion of full-length genomic mRNA | — | 10 (Cui 1999) |
| abrogate Rev-dependence with a constitutive transport element (Mason–Pfizer monkey virus CTE) for nuclear export | — | 30 (Mautino 2000) |
| add an mRNA stabilizing element — the woodchuck hepatitis virus posttranscriptional regulatory element (**WPRE**) | **increases mRNA half-life by up to 10-fold in vitro** | 52 |
| improve the HIV-1 packaging signal Ψ | **W03 says this "will likely fail"** — Ψ and other HIV-1 regulatory domains "are believed to be optimally evolved" | 29 (Marzio 2002) |

**The headline feasibility claim, and its status.** W03 p.7: combining these
"may yield crHIV-1 vectors capable of packaging 100 times more efficiently
than HIV-1 **(Weinberger et al., unpublished)**." **KIND: QUOTED to an
unpublished source.** The entire P ≈ 100 regime — the one in which Fig. 3b
reaches HAART-comparable set points — rests on a 2003 personal communication
in the same group. It is not MEASURED, it is not even published. Put that on
the slide; it is the honest version of the twenty-three-year-old question.

### D — the antiviral effect, and a definition that reads backwards

**Definition as printed** (p.2, and Table 1): "the fraction by which the HIV-1
titer produced from I_D cells is therapeutically downregulated". Swept
**0.0 to 1.0**.

**How it is actually used: D is the fraction REMAINING.** Three places in W03
settle it. (i) Equation [3] multiplies the I_D HIV-production term by D.
(ii) p.4: "If no therapeutic gene is encoded in the crHIV-1 and **D = 1** …
there is no reduction in the number of HIV-1 virions produced." (iii) Fig. 3b
caption, p.6: HAART-comparable set points at "P ≈ 100 and **D ≈ 0.4** (i.e.,
downregulation is ~60% effective)."

**INFERRED BY US — and this will trip students and autograders both.** The
prose definition and the model's use of D are opposite in sense. D = 1 is *no
inhibition*; D = 0 is *total inhibition*. Any T73 problem statement must say
"D is the fraction of HIV-1 production that remains" and must not reuse W03's
own wording. This is a wording trap in the required paper, and it is cheap to
teach: ask the room which end of the D axis is the good drug, before telling
them.

**What you change in the construct to move D.** W03 p.7: the antiviral cargo
gene — antisense, RNAi, ribozymes, intrabodies, transdominant Rev mutants,
TAR RNA decoys (refs 31, 32). And a one-line experimental recipe that is the
best thing in the paper for a design course: *"D can be experimentally
measured simply by quantifying the HIV-1 titer in the supernatant of cell
cultures in the absence or presence of the crHIV-1."* **D is extracellular and
measurable; P is intracellular and is not.** W03 says this explicitly (p.2)
and it is the reason the two knobs are not symmetric.

**One caveat W03 states against itself** (p.7): "If D is defined as reduction
in full-length HIV-1 cytoplasmic mRNA, then each class of antiviral genes
described in the literature requires a different model (L. Weinberger, D.
Schaffer, and A. Arkin, unpublished data)." The generality of D is bought by
keeping it extracellular.

---

## 4 · T67 — the binomial genome partition

### 4a · What W03 writes — QUOTED (p.3, journal 10030, "Viral competition and recombination")

Retroviruses are diploid and package **two** single strands of mRNA per
capsid. In an I_D cell the cytoplasmic HIV-1 : crHIV-1 mRNA ratio is 1 : P by
definition of P. "By using a binomial distribution", the three diploid virion
species come out in the ratio

    homozygous HIV-1 : heterozygous : homozygous crHIV-1  =  1 : 2P : P^2

and because all RNA pairs are equally likely to be packaged, that is also the
ratio of **virions released** from the I_D cell.

**The strike-out.** W03 p.4: An et al. (ref 2, *J. Virol.* 73:7671, 1999)
show that heterozygous lentiviral virions can infect and be internalized but
meet "some **preintegration (but postfusion) block**". Therefore

    ratio of INFECTIOUS virions  =  1 : P^2

"since heterozygous virions do not produce viable infections."

**The burst statement, verbatim in substance (p.4):** an I_D cell will produce
**D × 200** HIV-1 virions and **P² × D × 200** crHIV-1 virions. With n = 200.
That is exactly the Dnδ′I_D and P²Dnδ′I_D terms of [3] and [6].

### 4b · The arithmetic an autograder needs — DERIVED, then COMPUTED

Let q = P/(1+P) be the probability that a randomly drawn transcript is
crHIV-1, so 1 − q = 1/(1+P) is the probability it is HIV-1. Binomial, two
draws:

    HIV homozygote   (1-q)^2   =  1      / (1+P)^2
    heterozygote     2q(1-q)   =  2P     / (1+P)^2
    crHIV homozygote q^2       =  P^2    / (1+P)^2

**These are exact probabilities and they sum to 1.** The paper's 1 : 2P : P²
is the same thing with the (1+P)² denominator dropped. **A T67 item must be
explicit about which of the two it wants** — normalized probabilities or the
unnormalized ratio — because they differ by (1+P)² and that is the commonest
way this calculation is got wrong.

Reference values, **COMPUTED**:

| P | p(HIV·HIV) | p(hetero) | p(crHIV·crHIV) | infectious fraction (1+P²)/(1+P)² |
|---|---|---|---|---|
| 1 | 0.2500 | 0.5000 | 0.2500 | 0.5000 |
| 3 | 0.0625 | 0.3750 | 0.5625 | 0.6250 |
| 10 | 0.008264 | 0.16529 | 0.82645 | 0.8347 |
| 30 | 0.0010406 | 0.062435 | 0.93652 | 0.9376 |
| 100 | 9.8030e-5 | 0.0196059 | 0.98029 | 0.9804 |

**The heterozygote waste, 2P/(1+P)², is maximal at P = 1, where it is exactly
one half.** DERIVED (d/dP of 2P/(1+P)² vanishes at P = 1). Half of everything
an evenly balanced co-infected cell makes is thrown away by the An et al.
block. This is the clean, checkable, exam-sized consequence of diploidy and it
is the best candidate for the T67 autograded item.

### 4c · THE PROBLEM WITH THE PARTITION, and it is the richest thing in §4 — COMPUTED

**W03's model does not partition a fixed burst. It scales the burst up by
(1+P)².** From [3] and [6], one I_D cell releases over its lifetime:

    HIV-1 virions      =  D*n                      = D*200
    crHIV-1 virions    =  P^2*D*n                  = P^2*D*200
    heterozygotes      =  2*P*D*n                  (produced, non-infectious)
    TOTAL released     =  (1+P)^2 * D * n

**COMPUTED, per I_D cell:**

| P | D | HIV out | crHIV out | total virions released |
|---|---|---|---|---|
| 1 | 1.0 | 200 | 200 | 800 |
| 3 | 0.2 | 40 | 360 | 640 |
| 10 | 0.4 | 80 | 8,000 | 9,680 |
| 20 | 0.5 | 100 | 40,000 | 44,100 |
| **30** | **0.4** (Fig. 2a) | 80 | 72,000 | **76,880** |
| **100** | **0.4** (Fig. 3b's HAART-comparable point) | 80 | 800,000 | **816,080** |
| 100 | 1.0 | 200 | 2,000,000 | 2,040,200 |

**Set that against the burst sizes W03 itself cites (all QUOTED, p.4):**
~**200** virions per infected cell in vivo (ref 17, Haase 1996); **3 to 5
times more** when CD8⁺ cells are depleted in rhesus macaques (ref 23, Jin
1999); "or even up to **40,000** virions when *env* is unnaturally deleted
from the SIV genome (Alan Perelson and David Ho, **unpublished data**)".

**So at the paper's own headline design point (P ≈ 100, D ≈ 0.4) a dually
infected cell must release 816,000 virions — twenty times the most extreme
figure the paper can cite, and that figure is itself unpublished.** W03 is not
hiding this. It says, p.8 (journal 10035): "our model assumes that the I_D
cell burst size is greater than n, implying that intracellular packaging
resources are not limited", and devotes a paragraph to Gag-Pol as a possible
limiting resource, noting that in vitro work (ref 8, Bukovsky 1999) found
encapsidation resources in a dually infected cell **are** limited. The abstract
and the Fig. 3b caption do not carry the caveat.

**This is the session's best wrong turn.** The binomial is the right
calculation for *which* genotype a virion is. It is the wrong calculation for
*how many* virions there are, and W03 silently swaps one for the other.
A student who computes the fixed-burst version instead —
n/(1+P)² HIV and nP²/(1+P)² crHIV out of a fixed 200 — gets at P = 100
**0.02 HIV virions and 196 crHIV virions per cell**, which is a different
model with a different threshold. **Decide which one T67 asks for and say so
in the item.** The honest framing: the binomial fixes the composition; the
burst size is a separate, measurable, unmeasured quantity, and W03's result
depends on it being enormous.

### 4d · Recombination and mutation — reported ABSENT, with one shaky citation

**Heterozygous recombination is reported as absent, twice.** W03 p.4 (journal
10031): "An et al. (2) go on to show that virtually none of the these
heterozygous integrations occur **in vitro**. Others report that these
heterozygous recombinations are **absent in mice** (46)." **KIND: QUOTED.**

**Mechanistic reason given, QUOTED (p.4):** retroviral recombination happens
during reverse transcription when RT jumps between the two strands; "the large
size discrepancy between HIV-1 and a smaller HIV-1-based vector (**10 versus
~4 kb**) does not permit reverse transcriptase to proceed through all of the
steps required" to make the closed circular DNA needed for integration.

**A citation problem, flagged.** W03's **ref 46 is Podsakoff, G. M. 2001,
*Mol. Ther.* 4:282–283, "Lentiviral vectors approach the clinic but fall back:
National Institutes of Health Recombinant DNA Advisory Committee review of a
first clinical protocol for use of a lentiviral vector."** That is a two-page
RAC-review commentary. It is cited twice for *experimental mouse results* —
for absent heterozygous recombination (p.4) and for "preliminary results from
a mouse model indicate that it is difficult for HIV-1 to mutate around this
construct" (p.7). The commentary may report RAC-submitted mouse data, but the
assigned PDF gives no way to check, and a one-line citation to a committee
review is thin support for the claim that strikes out half of an evenly balanced I_D cell's output (2P/(1+P)^2, maximal at P=1 where it is exactly 1/2; CORRECTED 7 Nov 2026 from 'two-thirds', which exceeds the quantity's maximum). **`[unverified]` — settled by reading Podsakoff 2001.**
This is a good adversarial exercise and it is aimed at the required paper.

**Mutation, QUOTED (p.7, journal 10034).** W03 calls mutation "of more
concern" than recombination. Two routes: HIV escape mutants that abolish the
therapeutic effect, and crHIV-1 itself mutating into a non-therapeutic virus,
"a possibility that is highly dependent upon the type and size of antiviral
gene encoded". Their mitigations, all QUOTED: Dropulic's antisense-*env*
vector then entering phase I (ref 13); mutations in *tat* and TAR induce
latency in cell lines (ref 15), so a crHIV-1 attacking *tat*/TAR may be
escape-resistant because the escapers would be latent; and the claim, offered
without a model, that "crHIV-1 mutation may be beneficial since crHIV-1 has
the potential to reciprocally match any mutation that HIV-1 might make."
W03 states the gap in its own words: "Models that examine the likelihood of
crHIV-1 mutation into a nontherapeutic virus must be examined." **No mutation
appears anywhere in equations 1–6.**

---

## 5 · T73 — R₀ for a therapeutic interfering particle, and the paradox

### 5a · The two reproductive ratios — QUOTED (W03 p.6, journal 10033)

**R₀**, defined as "the number of new HIV-1 infections produced from a single
infected cell, assuming that virtually all cells are uninfected". Printed as
λkn/cδ; **the correct denominator is cd (§0)**. Transition at R₀ = 1 is a
transcritical bifurcation.

**R₀ᵀ**, "a new therapeutic reproductive ratio … the number of new crHIV-1
infections produced from one **I_T** cell, assuming that the system is at
steady state for HIV-1 infection (i.e., virtually all cells are uninfected by
crHIV-1)":

    R0_T  =  P^2 * D * (1 - 1/R0)

W03's own gloss (p.6): since R₀ > 1 is assumed, 1 − 1/R₀ < 1, so persistence
"is predicated upon choosing a large enough value of the product **P²D**".
R₀ᵀ is called "an invasion parameter that describes the rate of infection
spread". W03 reports it was verified against the Fig. 3 blue region — in the SI.

**Note the base unit.** R₀ counts infections from an **infected cell**. R₀ᵀ
counts infections from an **I_T cell** — a cell that is carrying the vector
and is *waiting to be infected by HIV*. The therapy's "susceptible" pool is
not uninfected cells; it is cells already carrying the vector. A session that
glosses R₀ᵀ as "R₀ of the vector" without saying what the index case is will
lose the whole point.

### 5b · Reference values for an autograded item — COMPUTED, from Table 1

With R₀ = 1.9375, **1 − 1/R₀ = 0.483871**, so **R₀ᵀ = 0.483871 × P²D** and the
persistence threshold R₀ᵀ > 1 is **P²D > 2.06667**.

Minimum P for persistence at each D. **Note the middle column: it is the
threshold on P² alone, not on the product.** The product P²D is 2.0667 at every
row by construction -- that is what the threshold means. Header corrected
7 November 2026; it previously read "P²D threshold", which would mislead anyone
writing an item from this table.

| D | **P² threshold = 2.06667/D** | **P_min = sqrt(2.06667/D)** |
|---|---|---|
| 1.0 (no inhibition at all) | 2.0667 | **1.4376** |
| 0.5 | 4.1333 | **2.0331** |
| 0.4 | 5.1667 | **2.2730** |
| 0.3 | 6.8889 | **2.6247** |
| **0.2** (W03's stated optimal D) | 10.333 | **3.2146** |
| 0.1 | 20.667 | **4.5461** |
| 0.01 | 206.67 | **14.376** |

R₀ᵀ at the paper's worked points:

| P | D | R₀ᵀ = 0.483871·P²D |
|---|---|---|
| 1 | 1.0 | 0.4839 — dies out |
| 3 | 0.4 | 1.742 |
| 10 | 0.4 | 19.35 |
| 20 | 0.5 | 96.77 |
| 30 | 0.4 | 174.2 |
| 100 | 0.4 | 1935 |
| 100 | 0.01 | 48.39 |

**Two sanity facts for item design, both COMPUTED.**
(i) **P alone cannot save a bad D.** R₀ᵀ ∝ P²D, so halving D costs the same
as dividing P by √2. The quadratic in P is the entire argument of the
abstract: *"shifting the search for more potent antiviral genes toward
engineering optimized therapy viruses that package ultraefficiently while
downregulating viral production moderately."*
(ii) **R₀ᵀ is nearly insensitive to R₀ once the infection is established.**
1 − 1/R₀ runs 0.484 at R₀ = 1.94 and 0.948 at R₀ = 19.4 (the value you get
from the same Table 1 with the alternative c = 3). A factor of ten in R₀ moves
the threshold P²D by less than a factor of two. **So R₀ᵀ is PROPORTIONAL to P²D with a coefficient between 0.47 and 0.95 over
R₀ in [1.9, 20] -- threshold between 1.05 and 2.11, and 2.0667 at this
patient's R₀. **CORRECTED 7 Nov 2026: this section previously read "R₀ᵀ ≈ P²D",
which understates the threshold by about a factor of two and conflicts with the
autograded value. Do not reinstate it.** The superseded wording was

**Guard for the autograder.** With Table 1 as printed, R₀ = 1.9375. With
c = 3 (Table 1 footnote *a*, for analyses without the eclipse phase) the same
formula gives R₀ = 19.375 — but then T\* = c/(kn) = 80 cells/µl, which
contradicts T₀ = 800, so c = 3 cannot be used without rescaling k. **Pin
c = 30 and R₀ = 1.9375 in the item, and state the parameter set.**

### 5c · THE PARADOX: "shooting itself in the molecular foot"

**The authors' own term is `crHIV-1 "shooting itself in the molecular foot"`**
— W03 p.5–6, journal 10032–10033, spanning the column break. **QUOTED.**

**The claim, from the abstract (p.1):** "Paradoxically, highly efficient
therapeutic inhibition of HIV-1 was found to be disadvantageous."

**The mechanism, exactly.** W03 p.5–6: "if HIV-1 downregulation is highly
efficient (D ≤ 0.1), crHIV-1 propagation itself is constrained by the dearth
of HIV-1 packaging proteins in the cell … viral production from I_D cells
becomes so efficiently inhibited that these cells stop producing virus
altogether and crHIV-1 infection and propagation within the individual die
out. **Importantly, I cells still produce HIV-1 at the same rate**, allowing
the HIV-1 set point to rebound to the pretherapy level."

**Why it is structural, DERIVED, in one line:** D appears in equation **[6]**
as well as equation [3]. The vector is an obligate molecular parasite of the
very Gag-Pol it is suppressing. R₀ᵀ = P²D(1 − 1/R₀) → 0 as D → 0. **There is
no setting of the cargo gene that inhibits HIV without equally inhibiting the
vector**, because in this model they share one production term. The
inhibition acts only inside I_D cells; singly-infected I cells never see it.

**The numbers of the paradox, from the text and from the panels:**

| claim | value | kind | where |
|---|---|---|---|
| D at which crHIV-1 propagation is constrained | **D ≤ 0.1** | MODELLED | p.5 text |
| D at which oscillations arise (per the Fig. 2 **caption**) | **D = 0.1** | MODELLED | Fig. 2a caption, p.5 |
| D of the oscillating trace per the **panel legend** | **D = 0.2** | MODELLED | Fig. 2a legend, read at 600 dpi |
| D at which the set point rebounds to pretherapy | **D = 0.01** | MODELLED | Fig. 2a caption and legend (agree) |
| Hopf region in the (P, D) plane | **P > 10 and D ≈ 0.1** | MODELLED | p.6 text; black band on Fig. 3's floor |
| W03's stated optimal D | **≈ 0.2** | MODELLED | p.6 text, journal 10033 |
| Fig. 3b's HAART-comparable design point | **P ≈ 100, D ≈ 0.4** | MODELLED | Fig. 3b caption |

> **Two caption/panel mismatches in W03, both found by rendering the panel.**
> **(1)** Fig. 2a's caption says oscillations arise at D = 0.1 and that
> "oscillations for D = 0.1 persist and are stable for many years [see SI]".
> The panel's legend, read at 600 dpi, lists exactly five curves:
> **D = 0.8, 0.6, 0.4, 0.2, 0.01**. There is no D = 0.1 curve. The grey
> oscillating trace is labelled **D = 0.2**.
> **(2)** The text (p.6) says "The optimal value of D is ~0.2"; the Fig. 3b
> caption says HAART-comparable reduction at "D ≈ 0.4". Both are MODELLED and
> they are not the same number. A slide must pick one and say which.
> Neither mismatch changes the mechanism. Both are exactly the kind of thing
> this course asks students to find, in a paper by the instructor.

**What the paradox is NOT.** It is not a statement that better antiviral genes
are bad for patients. It is a statement that, *in this architecture*, the
therapeutic payload and the vector's own fitness are the same quantity. A
session that drops "in this architecture" is teaching a slogan. Note that
Pitchai et al. 2024 and Chaturvedi et al. — the descendants in
`docs/project-papers.md` — use TIPs defined by **deletion**, where the TIP
competes for Gag rather than suppressing its production, and that is a
*different* coupling. Whether the same paradox survives that change is not
answered by any paper in this folder. `[unverified]`, and it is a good open
question to hand the room.

### 5d · Simulation results worth a number — MODELLED, W03 pp.4–5

| quantity | value | where |
|---|---|---|
| time to the new reduced HIV-1 set point | ~**100 days** after crHIV-1 administration, varying with P and D | p.4 text |
| crHIV-1 viral load reached | up to **10⁷ virions/ml** | p.4 text; Fig. 2a right panel |
| total non-HIV-infected cells (T + I_T) level off at | ~**1,500 cells/µl** | p.4 text; Fig. 2c inset |
| uninfected T alone drops into the AIDS regime | **< 200 cells/µl** | Fig. 2c caption |
| initial crHIV-1 inoculum used | V_T = **10⁵ virions/ml**, "equivalent to an inoculation of ~5 × 10⁷ total crHIV-1 virions" | Fig. 2 caption |
| higher P and D | **reduce** the time to the new steady state | Fig. 2a, 2b captions |
| HAART failure threshold (clinical, QUOTED, ref 18) | set point rebound to **> 400 copies/ml** | Fig. 3b caption |

**COMPUTED from the Fig. 2 caption:** 5 × 10⁷ virions ÷ 10⁵ virions/ml =
**500 ml of plasma**. An adult has roughly 3 litres of plasma, so the implied
compartment is about six times too small, or the two figures are not meant to
be consistent. Minor, but if a problem set asks students to convert a dose to
a concentration, do not use this pairing. **INFERRED BY US.**

**A discrepancy in Fig. 2c, flagged, not resolved.** The panel's pretherapy
infected-cell level (green *I* and red *I_TOT*, both at t = 0) reads
**≈ 58 cells/µl** against printed ticks at 0,10,…,60. The Basic Model steady
state from Table 1 is **I\* = (λ − dT\*)/δ = (31 − 16)/0.7 = 21.43 cells/µl**
(COMPUTED), which is the value that reproduces V₀ = 10⁵ virions/ml exactly.
The panel is 2.7× higher. The simulations include the eclipse-phase delay and
"equations 1 to 6 were altered accordingly (see SI)", so the extra may be
eclipse-phase cells counted into *I*. **`[unverified]` — settled by the SI's
eclipse-phase equations.** Do not put 58 cells/µl and Table 1 on the same
slide without this note.

---

## 6 · Noble 2018 — gene drives. Almost nothing here is MEASURED.

**NOTATION IN THIS SECTION — added 8 November 2026.** Every quotation below
keeps Noble's own letters, because a quotation that has been relettered is not
a quotation. **The deck does not keep them.** N18 writes its homing efficiency
**P**, which is this session's packaging advantage (§3, autograded in T67 and
T73 and on the final), so on every slide the homing efficiency is **h**, the
invasion condition is **f(1 + h) > 1** and the boundary is **f > 1/(1+h)**.
N18's allele names W, D and R stay his, because they are printed on the crops,
but no slide writes one as a bare letter: alleles appear as **genotypes** (WW,
WD, DD, DR) or as **noun phrases** ("the W gamete", "the resistant allele"),
since a bare D in a quantity position reads as the antiviral effect.
`docs/symbols.md` holds the decision and the reasoning. **Anything written for
PS9, the home guide or the final must match the deck rather than this
section.** Below: read every P as the homing efficiency, and every D in §6a
and §6b as an allele name or an allele count, never as the antiviral effect.

N18 is a modelling paper. The only empirical numbers in it are the homing
efficiencies in Appendix 1—table 1, which are **QUOTED** from five published
drive constructs and recomputed by N18 to a common definition, and two
demographic parameters for *An. gambiae*.

### 6a · The three allelic classes and the model — QUOTED (N18 pp.4, 8)

**W** wild-type, **D** gene drive, **R** drive-resistant. Six genotypes: WW,
WD, WR, DD, DR, RR. Diploid, N individuals, random mating, **Moran process**
with sexual reproduction: each time step, two parents are chosen with
probability proportional to fitness, one offspring is produced, one individual
chosen **uniformly** dies. **A generation is N time steps**, equal to the mean
lifespan of an individual.

**The drive mechanism, and the one assumption that drives everything:**
"we assume that the drive **invariably** cuts the wild-type allele in the
germline of a heterozygous WD individual, converting to a drive allele with
probability **P**, or a resistant allele with probability **1 − P**."

**Gamete production probabilities, printed in the Materials and methods (p.8)
— QUOTED:**

    q^W_WW = q^D_DD = q^R_RR = 1
    q^D_WD = (1+P)/2        q^R_WD = (1-P)/2
    q^W_WR = q^R_WR = q^D_DR = q^R_DR = 1/2
    all others zero

**The two non-trivial rows in the deck's notation:** q^D_WD = (1+h)/2 and
q^R_WD = (1−h)/2. Same numbers, our letter.

**Note what is missing: q^W_WD = 0.** A WD heterozygote never transmits a
wild-type allele. The W allele is destroyed in every heterozygote; only its
*fate* is in question. **This is the structural analogue of W03's binomial**
— a genotype-production table over gametes instead of over RNA pairs — and it
is the cleanest way to put the two halves of the session on one slide.

**Worked cross printed in Fig. 1C (read at 300 dpi), WD × WR:**

| offspring | probability |
|---|---|
| WD | (1+P)/4 |
| WR | (1−P)/4 |
| DR | (1+P)/4 |
| RR | (1−P)/4 |

**DERIVED check:** they sum to 1, and they are exactly the product of
{D:(1+P)/2, R:(1−P)/2} from WD with {W:1/2, R:1/2} from WR. No WW offspring is
possible, because WD contributes no W. Good student exercise.

**Fitness normalization, QUOTED (N18 p.4):** fitnesses are "normalized such
that the wild-type homozygote has fitness one (f_WW = 1), the drive confers a
**dominant** cost (f_DW = f_DD = f_DR < 1), and resistance is **neutral**
(f_WR = f_RR = 1)." Throughout the main figures, **f = 0.9** — a 10% dominant
drive cost. N18 states this ordering "conservatively represents the worst-case
scenario for drive spread", and says so again for neutral resistance:
resistance "can increase in frequency without being selected against".
**Every headline number in N18 is therefore a lower bound by construction — GIVEN THAT EVERY CUT LANDS**, and with respect to the fitness and resistance assumptions N18 names. **Scope restored 8 November**; this line previously claimed it flatly. See §6b-i: the always-cuts idealisation is the one named assumption that runs FOR the drive, N18 scopes each of its own worst-case claims to a single assumption, and **the phrase "lower bound" does not occur anywhere in the paper.**

**Deterministic invasion condition, QUOTED (N18 p.3):** a drive is initially
favored if **f(1 + P) > 1**. Fig. 1B plots that boundary, f = 1/(1+P), with
"Initially favored" above it; the x axis is P from 0 to 1 and the y axis is DW
fitness f from 0.5 to 1 (read against printed ticks). Vertical red lines mark
the empirical efficiencies.

**The boundary in the deck's notation, with the one number that rides on it —
COMPUTED, re-verified 8 November 2026.** The condition is **f > 1/(1+h)**. At
**h = 0.14** — the female AsMCRkh2 construct, the leftmost vertical line in
Fig. 1B — the boundary is **1/1.14 = 0.877193**, which the slide prints as
**f > 0.877**; N18's own **f = 0.9** therefore clears it by **0.022807, i.e.
2.28 percentage points, printed as 2.3 points**. Equivalently
f(1 + h) = 0.9 × 1.14 = **1.026 > 1**. So the 14% line sits *inside* the
invading region with a narrow window, not outside it — which is the sentence
segment 5's crop slide carries in body type. For the other simulated values,
1/(1+h) is 0.8696 at h = 0.15, 0.6667 at h = 0.5 and 0.5263 at h = 0.9, all
of them under f = 0.9.

### 6b-i · The always-cuts idealisation is the one assumption that runs FOR the drive — INFERRED BY US, 8 November 2026

**Status: INFERRED BY US.** Every component fact below is QUOTED. The join is
ours. N18 nowhere states this and nowhere contradicts it.

**Fact 1 — P is defined conditionally, twice — QUOTED (N18 pp.3–4, p.4).**
Definition: the homing efficiency "(P), or the probability of undergoing
homology-directed repair instead of nonhomologous repair" — conditional on
repair, hence on a break. Mechanism: "**Consistent with experiments**, we
assume that the drive **invariably** cuts the wild-type allele in the germline
of a heterozygous WD individual, converting to a drive allele with probability
P, or a resistant allele with probability 1 − P." The two branches are
exhaustive. There is no third outcome.

**Fact 2 — there is no parameter for a cut that does not happen — QUOTED
(N18 p.8); already recorded in §6a.** The gamete table gives q^D_WD = (1+P)/2
and q^R_WD = (1−P)/2, and "The remaining values not listed … are zero", so
**q^W_WD = 0 identically, for every P < 1**. Fig. 1A draws the same thing: read
at 600 dpi, the arrow labelled "cut" carries **no probability**, and only the
two arrows after it are labelled — HR with P, NHEJ with 1 − P. No branch
returns a W outcome.

**Fact 3 — N18's worst-case claims are each scoped to a named assumption, and
always-cuts is not one of them — QUOTED.** p.4, the fitness ordering: "This
ordering of the parameters conservatively represents the worst-case scenario
for drive spread." p.19, neutral resistance: "assuming resistance is always
neutral represents the worst-case scenario for drive invasiveness." pp.6, 18,
zero inbreeding depression: "the worst-case scenario for drive". The
always-cuts sentence is justified by "Consistent with experiments" — an
empirical appeal, not a conservatism one. **N18 makes no global claim**, and
the phrase "lower bound" does not occur anywhere in the paper.

**Fact 4 — direction.** Perfect cutting maximises the fraction of W alleles
converted or destroyed; relaxing it can only return W gametes to the pool,
lowering both conversion and resistance generation. So always-cuts runs **FOR**
the drive while resistance-neutral and dominant-cost run **against** it.

**Fact 5 — what Appendix 1—table 1 does, and the correction to the obvious
reading — QUOTED (N18 pp.24–29). VERIFIED INDEPENDENTLY 8 November** against
the PDF's own text layer, because this is the fact that overturned the first
version of this finding. The recomputation uses exactly two counts: "we
calculate two numbers for each drive construct: (i) the total number of initial
alleles counted which were drives or were subject to drive, T, and (ii) the
total number of resulting drive alleles, D." **The table does not tabulate
resistance.** Four columns only — Organism, Ref., System name, Efficiency —
one value per row, no resistance column, no NHEJ column, no sample sizes, no
footnote. A non-drive allele is **never classified**. So the appendix
misclassifies nothing.

**The pooling happens one step later, and it is the MODEL's.** The appendix's
efficiency is read into q^R_WD = (1−P)/2, which assigns the whole non-drive
remainder to R. N18 makes that substitution explicitly: the vertical lines in
Fig. 1B and the dashed white lines in Fig. 7 are "the empirically measured
homing efficiencies from Appendix 1—table 1" (p.13 caption), plotted on the
model's P axis.

**What follows.** D/T estimates the drive-gamete fraction (1+P)/2, which is
exactly q^D_WD, so the empirical number is a sound estimate of **that**. It is
the model's conditional P only if every non-drive gamete is resistant — i.e.
only under always-cuts. If some germlines never cut, the empirical number is
**not** N18's P, and the residual is typed as permanent heritable resistance
when part of it is still-cuttable wild type. Opposite things downstream:
resistance is permanent, a failed cut is not.

**The one place N18 comes near it, and it does not cover this — QUOTED (N18
pp.6–7).** "Fundamentally, we exercise caution by omitting application-specific
phenomena that might aid containment in particular instances but not in
general." Cut failure would aid containment, so it arguably falls under the
blanket. Against: N18 never names it, the examples given are ecological and
demographic, and nuclease cutting efficiency is not "application-specific".
**Treat it as a general disclaimer, not as the paper handling the point.** Note
it points the OPPOSITE way from a lower bound: omitting containment-aiding
effects makes the drive look stronger. The paper's two framings genuinely pull
in opposite directions, which is further reason the flat "lower bound" reading
was wrong.

**The honest counterexample — QUOTED (N18 p.27).** For the 14% entry, the
largest deficit in the table, N18 reports the authors' mechanism as resistance,
not cut failure: in crosses between transgenic females and wild-type males,
"maternal deposition of Cas9 in eggs results in NHEJ-mediated disruption of the
paternally derived wild-type chromosome in the early embryo." For that
construct the non-drive remainder really is NHEJ product and the model's
assignment is right.

**[unverified]** whether Champer et al. 2017 (the 52% and 62% entries)
genotyped resistant alleles well enough to bound cut failure. Not in
`private/readings/`; not read. N18's recomputation discards the information
either way.

**WHAT A SLIDE MAY SAY ON THE STRENGTH OF THIS.**
- MAY: "Every cut is assumed to land. That one assumption runs FOR the drive;
  the others run against it."
- MAY: "h is the repair outcome GIVEN a cut. A germline that never cuts has no
  slot in the model — a WD heterozygote sends on no wild-type gamete at all."
- MAY: "So the appendix numbers and the model's h are the same quantity only
  while every cut lands."
- MAY NOT: "Noble counts uncut wild type as resistant." The appendix counts
  drive alleles only and classifies nothing. The pooling is the model's. **This
  was the first draft of this finding and it was false about the paper.**
- MAY NOT: "the 14% figure is contaminated by failed cutting." N18 attributes
  that deficit to maternal-deposition NHEJ (p.27).
- MAY NOT: "every number is a lower bound by construction" — unqualified. True
  INSIDE the idealisation, not across it. §6a's scope is restored accordingly.

### 6b · Appendix 1—table 1, the only empirical data — QUOTED (N18 p.24)

N18 recomputes every published homing efficiency to one definition,
**P = 2D/T − 1**, where T is the total number of initial alleles that were
drives or were subject to drive and D the total resulting drive alleles. At
P = 1, D/T = 1; at P = 0, D/T = 1/2.

**In the deck's notation: h = 2A_D/T − 1**, with A_D the resulting drive
alleles — spelled out because N18's D in *this* formula is a **count of drive
alleles**, which is neither the antiviral effect nor the name of the drive
allele. The formula is ledger-only; no slide carries it.

| organism | source paper | system name | efficiency |
|---|---|---|---|
| Yeast | DiCarlo et al. 2015 | ade2::sgRNA | >99% |
| | | ade2::sgRNA + URA3 | 100% |
| | | sgRNA + ABD1 | 100% |
| | | cas9 + sgRNA | >99% |
| | | ADE2 + sgRNA + cas9 | >99% |
| Fruit flies | Gantz & Bier 2015 | g-MCR | 97% |
| | Champer et al. 2017 | nanos | 62% |
| | | vasa | 52% |
| | | additional nanos | 40–62% |
| | | additional vasa | 37–53% |
| Mosquitoes | Gantz et al. 2015 | AsMCRkh2 (**male**) | 98% |
| | | AsMCRkh2 (**female**) | **14%** |
| | Hammond et al. 2016 | AGAP011377 | 83% |
| | | AGAP005958 | 95% |
| | | AGAP007280 | 99% |

**Range N18 quotes in the main text: 0.37 to 0.99** (p.4; cited as p.3 here until 8 November — only the lead-in clause sits at the foot of p.3). **Note that this
range excludes the 14% female AsMCRkh2 value**, which appears in the table and
as the leftmost vertical line in Fig. 1B. A sex-specific 7× difference in the
same construct is the most interesting number in the table and it is the one
the summary range drops. **INFERRED BY US**, and worth a sentence.

**The three homing efficiencies N18 simulates, and what they stand for**
(QUOTED, Fig. 1D; P in the paper, **h** on our slides, where the three are
spoken as percentages off the figure legend):
- **P = 0.15** — "a low-efficiency, constitutively active system", i.e. a
  constitutively expressed nuclease + gRNA cassette targeting the neutral site
  of insertion, "an arrangement that could occur **accidentally**" (p.7).
- **P = 0.5** — "conservative", N18's lower-bound estimate of empirical
  efficiency.
- **P = 0.9** — "high efficiency".

**Fitness is NOT measured.** N18 p.3: "the fitness parameter, f, is typically
**not measured** in proof-of-concept studies". Every f in N18 is MODELLED.

### 6c · The release-size result — MODELLED (Fig. 1D–F, Fig. 3)

Baseline for all of Fig. 1: **N = 500**, release of **15** drive homozygotes
(DD) into a wild-type population, **f = 0.9**, neutral resistance, 10³
simulations per point.

**"Peak drive"** is N18's own term: the maximum frequency of drive alleles
reached during a simulation. A drive has **"invaded"** if it establishes;
**"escaped"** if it reaches frequency **0.1** in a subpopulation other than
the one it was released into (N18 p.5 and p.19; N18 calls the 0.1 cutoff
"arbitrary").

**Median peak drive vs. number of organisms released** — digitized from
Fig. 1F at 300 dpi against the printed y ticks 0, 0.2, 0.4, 0.6, 0.8, 1.0.
**MODELLED (theirs), digitization INFERRED BY US to ±0.01:**

| organisms released | P = 0.15 | P = 0.5 | P = 0.9 |
|---|---|---|---|
| 1 | ~0.005 | ~0.005 | ~0.005 |
| **2** | ~0.01 | **0.285** | **0.895** |
| 3 | ~0.015 | 0.325 | 0.915 |
| 4 | ~0.02 | 0.345 | 0.92 |
| 5 | ~0.025 | 0.355 | 0.93 |
| 6 | ~0.03 | 0.37 | 0.93 |
| 7 | ~0.03 | 0.37 | 0.935 |
| 8 | ~0.035 | 0.38 | 0.94 |
| 9 | ~0.04 | 0.375 | 0.94 |
| **10** | **~0.045** | **0.38** | **0.94** |

**The number for the slide is the 1 → 2 step.** At P = 0.9 the median peak
drive goes from essentially zero to **0.895** when the release goes from one
organism to two. Everything after that is flat. N18's own summary (p.5): "for
the parameters studied, a release of **10** individuals nearly guarantees
invasion with substantial peak drive", and the distributions are **bimodal** —
one mode at the initial frequency (drift to extinction), one near the
deterministic maximum.

**Population size barely matters** (Fig. 3, MODELLED): repeating Fig. 1E at
N = 500, 1000, 2500, 5000, 10000, "the distributions narrow for larger N until
plateauing at roughly N = 5000. However, the **central tendencies show little
change**." That is what licenses reading a 500-individual simulation as a
statement about a wild mosquito population.

### 6d · Population structure and the escape threshold — MODELLED (Fig. 2)

Setup: **five subpopulations, complete graph, 100 individuals each (N = 500
total)**, 15 drive homozygotes into one of them, P = 0.5 unless stated,
f = 0.9, neutral resistance. Escape probability from 10³ simulations per
pixel (Fig. 2D); Fig. 2E from 10⁴ per point.

**Mean time between migrations, DERIVED and printed as N18's Equation 3:**

    E[T]  =  (1 - m) / (N*m)     generations

**COMPUTED check of N18's own gloss:** at m = 10⁻³ and N = 500,
(1 − 0.001)/(500 × 0.001) = **1.998 generations** — N18 says "a single
migration event every 2 generations on average". Confirms N = 500 is the
*total*, not the per-deme size, in Equation 3.

**The result, QUOTED (N18 p.6):** at m = 10⁻³ escape is "virtually
guaranteed … for moderate drive efficiencies". Extremely low m contains the
drive; high m guarantees invasion of every linked subpopulation; the
transition sits at "migration rates on the order of the **inverse of the drive
extinction time**". Fig. 2D sweeps m from 10⁻⁵ to 10⁻¹ against P from 0 to 1.
Fig. 2C shows typical traces at m = 10⁻¹, 10⁻², 10⁻³, 10⁻⁴ over 100
generations.

**The analytic result, DERIVED by N18 (p.20), with its asymptotic form:**

    P{E}  ~  e_{i,0} * ( 1 - exp[ -( e_{1,0}*f_DD + e_{0,1}*(f_WD + f_DR) ) ] )

"when the migration rate is on the order of the inverse of the drive
extinction time, the invasion probability is **order 1**." **The primary
determinant of spread between adjacent populations is the average number of
migrants per generation** — N18 p.7 says so and offers it as the basis for
comparing alteration drives with suppression drives.

### 6e · What resistance does and does not prevent — the paper's whole point

**QUOTED, abstract:** "although resistance prevents spread to **fixation** in
large populations, even the least effective drive systems reported to date are
likely to be **highly invasive**."

**QUOTED, p.2:** "While we agree that resistance should prevent drive fixation,
an allele can nonetheless spread to significant frequency **without fixing**."

**QUOTED, p.4:** in all three simulated cases "the drive, on average,
**irreversibly alters a majority of the population**, either via invasion of
the drive itself or via spread of **drive-created resistant alleles**."

That last clause is the one a session must not drop. The resistant alleles are
*made by the drive*, at rate 1 − P per cut, out of wild-type alleles that the
drive has already destroyed. Resistance is not a containment mechanism; it is
the drive's own exhaust, and it is itself an engineered sequence spreading
through a wild population.

**Standing genetic variation — MODELLED (Fig. 4, 5000 simulations per point):**
pre-existing resistance **linearly** decreases mean peak drive, **R² = 0.996**,
over initial resistance frequencies 0 to 0.5. N18's headline (p.11–12): at
P = 0.5, f = 0.9, neutral resistance, release of 15, "pre-existing resistance
of greater than **0.5** frequency is required to contain peak drive to below
**10%** of the population, compared to **35%** in the absence of SGV."
The empirical anchor, **QUOTED** from Drury et al. 2017 (flour beetles,
sequencing): resistance-conferring mutations "exist at a wide range of
frequencies, from **0 to 0.375**, with an average of roughly **0.1**."
**COMPUTED consequence:** the observed average (0.1) is five times below the
0.5 needed to contain the drive.

**Family size — MODELLED (Fig. 5, 6), with real arithmetic.** Extending to k
adult offspring per mating, N18 derives (their Equation 5, from Hill 1972):

    N_e  =  4N / (2k + 6)       and at k = 1, N_e = N/2

so releases and population sizes scale by **4/(2k+6)**. **For *An. gambiae*,
N18 estimates k ≈ 9.76** from n ≈ 186 eggs per batch (the highest value in
Hammond et al. 2016) times a survival-to-adult probability
p = θ₀·θ_L·θ_P = 0.831 × 0.076 × 0.831 = **0.0525** (parameters QUOTED from
Deredec et al. 2011). So "a release of **7** individuals roughly corresponds
to a release of **1** individual in our basic model", and "an organism which
typically has 100 offspring that survive to adulthood would need a release
size of roughly **258** to surpass the 10-individual initial release
threshold". **The 10-individual threshold is a census release size; the
effective release size is i_e = 5.**

**Fitness sweeps — MODELLED (Fig. 7, 51×51 grid, 100 simulations per point):**
peak drive > 0.3 across most of the regime; at P = 0.5 "drives can confer
fitness costs as high as **20%** before the peak drive drops below 0.3"; at
P > 0.8 peak drive is typically > 0.5 even at f ≈ 0.7, and low-cost drives
(f > 0.9) have peak drive > 0.9. Whether the cost acts on birth rate or death
rate makes almost no difference (Fig. 7 left vs. right). **N18's summary
claim:** if a drive is predicted to invade by the deterministic model, "then
it will **almost certainly** reach a maximum frequency greater than 0.1."

**Costly resistance — MODELLED (Fig. 8).** With resistance cost s (RR fitness
1 − s) and P = 1/2, the deterministic condition is f > 2/3. Two regimes: for
**s < 1/3**, drive spread improves dramatically (often to fixation) whenever
f > 1 − s; for **s > 1/3** the improvement saturates, because the drive can be
cheaper than resistance and still too costly to invade. N18 notes that making
resistance costly — multiplex targeting of essential genes — is exactly what
real applications will do, so real drives are expected to spread **better**
than N18's neutral-resistance baseline.

**Inbreeding — MODELLED (Fig. 9, partial selfing rate s, 1000 simulations per
point, no inbreeding depression = worst case for containment).** The upper
mode of the peak-drive distribution dominates until selfing **s ≈ 0.75** at
P = 0.9 and **s ≈ 0.6** at P = 0.5. Converting with N18's **F = s/(2 − s)**:
effective drive tolerates inbreeding coefficient **F ≈ 0.6**, conservative
drive **F ≈ 0.43**.

### 6f · Self-propagating vs. self-exhausting — QUOTED (N18 eLife digest and discussion)

"Gene drives can be **'self-propagating' or 'self-exhausting'**: the former are
designed so that they can always spread as long as there are wild organisms
around, whereas the latter are expected to lose their ability to spread over
time." N18's whole result is about self-propagating **alteration** drives, and
it says three limits on itself:

1. It does **not** generalize to self-propagating **suppression** drives,
   "which could potentially self-extinguish before invading other
   populations", nor to sex-ratio distorters or genetic-load drives.
2. The containment recommendations it endorses are **ecological confinement**
   (do not build a self-propagating drive for a species that is endemic where
   your lab is) and **intrinsic molecular confinement** — "synthetic site
   targeting or split drive" — as recommended by the National Academies.
3. Its policy conclusion, QUOTED: "self-propagating gene drive is best suited
   to applications such as malaria prevention that seek to affect **all** wild
   populations of the target species", and contained field trials "could
   potentially result in unintended spread to additional populations."

**Code and data.** N18 deposits C++/Matlab simulation code, data files and
figure-reproduction code at GitHub (Noble, 2018), archived at
`github.com/elifesciences-publications/drive-invasiveness`. **QUOTED from the
paper; not verified by us** — `[unverified]`, settled by fetching the repo.

---

## 7 · Huang & Baltimore 1970 — the definition and the claim

Three pages. This is where "DI particle" comes from; the term is coined in
this paper.

### 7a · The definition — QUOTED (HB70 p.1, journal 325)

The defective particles they mean have **four** properties, printed as a
numbered list:

> "(1) they contain normal viral structural protein; (2) they contain a part
> of the viral genome; (3) they can reproduce in the presence of helper virus;
> (4) they interfere specifically with the intracellular replication of
> non-defective homologous virus."

And the coinage: "we propose to call them **DI particles** (DI = defective
interfering). The non-defective homologous virions which are capable of
independent replication are called **standard virus**."

The specificity claim, QUOTED: the interference "can occur in the **absence of
detectable interferon** and is dependent on the **nucleic acid** contained in
defective particles." That is the whole argument for calling it engineering
rather than immunology.

### 7b · The disease claim and the model — QUOTED (HB70 pp.1–2, journal 325–326)

The thesis, from the abstract: such particles "may play a major part in the
**evolution of viral diseases**."

**Fig. 1** is a hand-drawn schematic with three labelled outcomes, and it is
the whole model:
- **I** — a cell infected by standard virus only: produces a new crop of
  standard virions.
- **II** — co-infection: DI particles replicate at the expense of standard
  virus until "DI particles are the predominant component in the viral
  progeny", standard virions fall, and "at this stage specific antibodies or
  other factors can neutralize the remaining virions." HB70 offers this as
  **acute, self-limiting viral disease**.
- **III** — a cell infected by DI particles only: **"will produce no yield."**

The conditional-replication requirement in one clause: "Because their ability
to replicate is dependent on standard virions, the concentration of DI
particles will decline as the infection spreads."

The persistent-disease branch, QUOTED: "synthesis of standard and DI particles
may be in such balance that only a very few virions are synthesized and the
infection would remain in a **subacute or latent form** until the balance is
upset." Worked through for lymphocytic choriomeningitis, measles/SSPE, fowl
plague.

**Honest caveat they state themselves (p.2):** "DI particles have **not been
isolated from naturally occurring infections in animals**." The whole paper is
an extrapolation from tissue culture and eggs to disease, and it says so.

### 7c · Table 1, the only data — MEASURED (HB70 p.3, journal 327)

VSV plaque-forming units per ml through successive **undiluted** passages,
same virus, same medium, two cell lines. Read at 400 dpi.

| undiluted passage | Chinese hamster ovary | Madin–Darby bovine kidney |
|---|---|---|
| 1 | 7.55 × 10⁸ | 4.68 × 10⁸ |
| 2 | 3.02 × 10⁶ | 1.25 × 10⁸ |
| 3 | 4.40 × 10⁴ | 1.00 × 10⁸ |
| 4 | **3.38 × 10⁷** | 3.95 × 10⁸ |
| 5 | — | 4.60 × 10⁸ |

**COMPUTED, as fractions of passage 1:**

| passage | CHO | MDBK |
|---|---|---|
| 2 | 0.400 % | 26.7 % |
| 3 | **0.00583 %** | 21.4 % |
| 4 | 4.48 % | 84.4 % |
| 5 | — | 98.3 % |

**The cyclic rebound is the point and it is real:** CHO passage 3 → 4 rises
**768-fold**, which HB70 reads as the model's result II cycling — "standard
virus undergoes a **burst of synthesis as predicted by the model**". That is a
predator–prey oscillation, measured in 1970, and it is the same oscillation
W03 finds as a supercritical Hopf bifurcation in Fig. 3 thirty-three years
later. **Put those two side by side.**

> **Two loose statements in HB70's text, both checkable against its own
> Table 1. COMPUTED.** (i) The text says two successive undiluted passages in
> CHO "reduce the standard virus to **0.1 per cent** of the original titre";
> Table 1 gives **0.40 %** at passage 2 and 0.0058 % at passage 3. Neither is
> 0.1 %. (ii) The text says MDBK "produce standard VSV at about **10 per
> cent** of the original titre through five successive undiluted passages";
> Table 1's MDBK minimum is **21 %** and by passage 5 it is back to 98 %. Both
> are mild, both point the right way, and both are findable by a student in
> two minutes. Good adversarial-reading material on an optional paper.

### 7d · Genome architecture sets the DI formation rate — QUOTED (HB70 p.3)

"The frequency of formation and the size of such a small piece of nucleic acid
must necessarily depend on the mechanism of nucleic acid replication of the
different viruses and might be viewed as the **production of a deletion
mutant**. For instance, **influenza** virus which has its genome in several
small pieces forms DI particles with **greater frequency** than **poliovirus**
which contains a single piece of RNA."

**This is the T68 hinge and it is a direct prediction about genome
architecture**: segmented genomes make defectives more often than
monopartite ones. HB70 also notes influenza DI particles "are antigenically
identical to standard virions but are **lacking the largest of the RNA
species** found in standard virions and contain small, unidentified pieces of
RNA" (ref 9, Duesberg 1968) — a specific deletion, named.

Mechanism of interference, QUOTED: with VSV "complete interference is
correlated with cessation of **all** viral RNA synthesis", partial
interference with "a competition between the synthesis of small RNA and large
RNA" — and the analogy HB70 reaches for is **Qβ**: "Small Qβ RNA fragments
compete successfully with the large complete Qβ RNA for replicase and
ultimately dominate the reaction" (ref 41, Mills, Peterson & Spiegelman 1967).
Spiegelman's monster, cited as the molecular mechanism of a DIP, in 1970.

---

## 8 · T68 — minimal gene set material in these three papers

`docs/deck-triage.md` line 111 still carries a row **"S25 | Minimal and
synthetic cells | new"**, which predates the 19 October decision that moved
the DIP/TIP material into S25. (See §11.) So T68 now has to live in a
population-scale session, and this is the material that bears on it. **No
design here — just what the papers supply.**

**The common structure, across all three papers:** a parasite keeps the
sequences that are read *in cis* and deletes everything that acts *in trans*,
and the helper supplies the trans functions. Write it as a three-column
ledger.

| | **what the parasite KEEPS (cis)** | **what it DELETES (trans)** | **what the HELPER supplies** |
|---|---|---|---|
| **crHIV-1** (W03 p.1) | QUOTED: crHIV-1 vectors "contain only the **cis** and none of the **trans** elements necessary for viral packaging", plus an antiviral cargo gene and an HIV-1-induced promoter | all trans elements | HIV-1 supplies the packaging machinery; W03 names "the HIV-1 **Gag-Pol** polyprotein that is cleaved into the HIV-1 capsid" |
| **DI particle** (HB70 p.1) | QUOTED: "they contain a part of the viral genome" and "normal viral structural protein" | the rest of the genome — for influenza, "the **largest** of the RNA species" | QUOTED: "they can reproduce in the presence of **helper virus**" |
| **split CRISPR drive** (N18 p.24, from DiCarlo 2015) | the gRNA cassette and the homology arms — "the basic **split drive** system containing only a guide RNA" | *cas9* | the host genome, or a separate construct, supplies Cas9 |

**The size numbers, such as they are:**

| quantity | value | kind | where |
|---|---|---|---|
| HIV-1 genome vs. an HIV-1-based vector | **10 kb vs. ~4 kb** | QUOTED | W03 p.4 |
| crHIV-1 HIV-1 output per I_D cell | D × 200 | DERIVED | W03 p.4 |
| crHIV-1 own output per I_D cell | P² × D × 200 | DERIVED | W03 p.4 |
| CRISPR drive construct contents | CRISPR nuclease + gRNA + "cargo" sequence | QUOTED | N18 Fig. 1A |
| minimal accidental drive | "a simple, constitutively expressed CRISPR nuclease and guide RNA cassette targeting the neutral site of insertion" | QUOTED | N18 p.7 |
| smallest drive element demonstrated | gRNA only (yeast `ade2::sgRNA`), efficiency **>99%** | QUOTED (from DiCarlo 2015) | N18 p.24 |

**Two consequences the session can use without inventing anything.**

1. **Deletion buys replication speed and costs autonomy.** The 4 kb vector
   cannot integrate from a heterozygous virion precisely *because* it is small
   (W03 p.4: the 10-vs-4 kb discrepancy stops reverse transcriptase). The
   same deletion that makes it a better competitor for packaging makes it a
   worse recombination partner. One design choice, two opposite consequences.
2. **The minimal element is the dangerous one.** N18's lowest-efficiency case,
   P = 0.15, is a bare nuclease-plus-gRNA with no cargo — the *simplest*
   construct, "an arrangement that could occur accidentally", and it still
   reaches a median peak drive of ~0.045 on 10 released organisms and
   irreversibly alters a majority of the population through drive-created
   resistant alleles. Minimal does not mean inert.

**What no paper here supplies for T68:** a number for how small a genome can
get and still be packaged. HB70 says influenza DI particles contain "small,
**unidentified** pieces of RNA". W03 gives ~4 kb for a lentiviral vector but
no lower bound and no packaging-limit curve. There is no minimal-gene-set
*measurement* anywhere in these three PDFs. See §10.

---

## 9 · Figures worth working on a slide, and what each one lets a student conclude

The standing rule is that the assigned paper gets **taught**, with its figures
worked on a slide, not referred to in passing. W03 has exactly **three**
figures, so all three are in, and there is no excuse here for a one-figure
session. The optional papers each have one figure or table that earns a slide.

**W03 Fig. 1 — the schematic and the six equations (p.3, journal 10030).**
Red/blue colour coding: red box = Basic Model + two terms, blue box = the
three new equations. A student can read off the whole architecture: that I_T
dies at *d* and not δ; that HIV can infect I_T but not I_D; that D sits on
both the HIV production arrow (Dnδ′) and the crHIV production arrow (P²Dnδ′);
and that the P² is attached to crHIV production only. **This panel alone
contains the paradox** — you can point at the two arrows that share a D. The
schematic also prints the per-arrow rate labels (nδ, Dnδ′, P²Dnδ′, k, λ, d, δ,
δ′), so the equations can be built on the slide from the picture.

**W03 Fig. 2 — three simulation panels (p.5, journal 10032).** A raster, so it
will need redrawing rather than cropping if it is to meet the 20 pt floor.
- **2a**, split HIV-1 / crHIV-1, 0–360 days, five D values at fixed P = 30.
  **Axis ranges, read off the panels' own printed tick labels at 7× on 8
  November: left (HIV-1) 1.0E+02 to 1.0E+05, right (crHIV-1) 1.0E+04 to
  1.0E+08**, both log, both virions/ml. Recorded because the deck prints them
  and §0 forbids anything on a slide that is not here. **The legend is also
  legible at 7×** and gives the colour map directly — D = 0.8 red, 0.6 yellow,
  0.4 blue, 0.2 grey, 0.01 green — which agrees with all three of the indirect
  anchors used before it was read (the oscillating trace is D = 0.2 and it is
  grey; the flat-at-set-point trace is D = 0.01 and it is green; the rest
  order by set point). QUOTED from the panel, not digitized.
  **The two panels are NOT the same curve at two scales**, and a slide must
  not say so: at D = 0.01 the HIV trace returns to its pretherapy set point
  while the vector **never reaches the panel floor at all**. That inversion
  is the paradox.
  Lets a student conclude that the D axis is **non-monotone**: the set point
  falls as D drops to ~0.4, oscillates at D = 0.2, and at D = 0.01 the green
  trace sits flat at the pretherapy 10⁵ — the therapy has done nothing.
  The crHIV panel on the right shows the mirror image: at D = 0.01 the green
  trace **is absent — zero pixels anywhere in that panel**, whose axis starts
  at 1.0E+04. **CORRECTED 8 November**: this read "the vector barely rises",
  which overstates what is drawn. Checked twice and independently — by eye on
  the crop, and by a calibrated digitization of the panel against its printed
  ticks. **Say what the picture shows: the trace is absent, not small.**
  One picture, the entire paradox, with the oscillation in between as the
  bifurcation you cross on the way.
- **2b**, fixed D = 0.4, three P values (10, 30, 50), 0–240 days. Lets a
  student conclude that P moves the set point **monotonically** and
  **shortens** the transient — the opposite behaviour from D. Two knobs, two
  different shapes of response.
- **2c**, cells rather than virions, with an inset. Lets a student conclude
  the thing that makes this a *therapy*: uninfected T drops into the AIDS
  regime (<200/µl) while **T + I_T climbs to ~1500/µl**. The patient's CD4
  count is restored by converting cells into a new class, not by protecting
  the old one. Carries the Fig. 2c discrepancy of §5d — teach it with the
  note or redraw it from the model.

**W03 Fig. 3 — the two (P, D) surfaces (p.6, journal 10033).** The best figure
in the paper and the one the session is built on. 3a: P 0→20; 3b: P 0→100;
both D 0→1; z is the HIV-1 set point in virus/mL on a log axis (3a labelled
100 to 100000; 3b labelled 10 to 100000). The floor carries a stability
projection: **red** (pretherapy HIV steady state stable, crHIV dies), **cyan**
(crHIV solution stable), **black** (oscillatory, the Hopf region, hugging low
D at larger P). A student can read directly off it: that there is a *valley*
in D rather than a monotone improvement; that the red wedge at low P is the
R₀ᵀ < 1 region and therefore that the P²D threshold is a *curve* on the floor,
not a point; and that going from 3a to 3b (P to 100) is what buys the extra
two decades of set-point reduction. **It is also the figure to overlay with
the analytic threshold P²D = 2.0667 from §5b** — if the red/cyan boundary on
the floor matches that curve, the closed form and the simulation agree in
front of the room, which is the one thing W03 says it checked only in the SI.

**N18 Fig. 1 — the six-panel drive figure (p.3).** Vector, so it crops
cleanly.
- **1A** is the cleanest published picture of HR-vs-NHEJ with P and 1−P on the
  two arrows. Put it beside W03 Fig. 1: same shape, same two-outcome branch.
- **1B** is the deterministic invasion boundary f = 1/(1+P) — **his axis label
  is P; our slides write that quantity h**, and the slide carrying this crop
  says so once in body type — with the empirical
  efficiencies as vertical lines. A student can conclude in one look that
  **every published construct is far inside the invading region**, and see the
  lone mosquito line at 0.14 that is not.
- **1C** is the Moran step plus the WD × WR offspring table — the gene-drive
  analogue of W03's binomial, and the slide where the two halves of the
  session meet.
- **1D** shows drive (red) and resistant (blue) allele frequencies over 80
  generations at three P. Lets a student conclude that **resistance wins and
  the population is altered anyway** — the blue curve rising as the red falls
  is the entire argument of the paper.
- **1F** is the release-size curve. One slide, one number: two organisms.

**N18 Fig. 2 — population structure (p.5).** 2D (escape probability over
migration rate × homing efficiency) lets a student conclude that containment
is a property of **gene flow**, not of the construct: there is a vertical
cliff in m at around 10⁻³ that is nearly independent of P above P ≈ 0.3.
2E (probability of invading 1, 2, 3 or 4 further populations) is the policy
slide.

**HB70 Fig. 1 — the hand-drawn three-outcome model (p.2, journal 326).**
Worth a slide precisely because it is hand-drawn and has no equations. A
student can conclude that W03's equations 4–6 are this picture written down,
and that outcome III — a cell that gets only DI particles and "produces no
yield" — is the conditional-replication requirement that becomes R₀ᵀ.

**HB70 Table 1 — the two cell lines (p.3, journal 327).** The passage-4
rebound in CHO, 768-fold, against the flat MDBK column. Lets a student
conclude that the oscillation is **not** a property of the virus but of the
host cell, which is exactly the "host control" section's claim and exactly
what W03 rediscovers as a Hopf bifurcation in a (P, D) plane.

---

## 10 · Gaps — what T67, T68 and T73 need that no paper here supplies

**T67 (binomial genome partitioning, AUTO, also on the final).**
- **The quantity is still not pinned**, which `private/log/week13-handoff.md`
  §4(b) already flags. §4b above gives the exact probabilities and §4c gives
  the trap. **Choose between the normalized binomial and W03's unnormalized
  ratio and write the choice into the item.**
- **No paper here measures the packaging competition.** P is swept, never
  measured. There is no measured co-packaging frequency for any real
  vector/helper pair in these three PDFs. If T67 wants a *measured* anchor,
  it has to come from outside — `docs/project-papers.md` claims Pitchai et al.
  2024 measured R₀^TIP by three-colour flow (§11), which is the closest thing,
  and we have not read that paper.
- **The equal-packaging assumption is asserted, not measured.** W03 p.3:
  "Since all of these RNA pairs have equal chance of being packaged
  (explained further in the Discussion)". A binomial requires it. Nothing here
  tests it.

**T68 (minimal gene set, HAND).**
- **No minimal genome size is measured anywhere in these three papers.** §8
  gives 10 vs ~4 kb for HIV-1 vs. a lentiviral vector and nothing below that.
  HB70's DI RNAs are "unidentified pieces".
- **No packaging-capacity curve.** Nothing relates deletion size to
  packaging efficiency, which is the quantity a minimal-gene-set argument
  would actually need. `docs/project-papers.md` says Pitchai et al. Table S1
  and Fig. 2A give the actual constructs — "the original ~2.5 kb *pol–vpr*
  deletion, TIP-1 with cPPT restored, TIP-2 with *tat/rev/vpu/env* ablated" —
  which is exactly the ledger T68 wants, and it is **not in this folder**.
  That is the single most useful thing a session author could add.
- **Nothing here on minimal cells.** If any residue of the old "minimal and
  synthetic cells" framing survives (§11), it has no source in this reading
  set.

**T73 (R₀ for a TIP, AUTO, also on the final).**
- **The R₀ᵀ derivation is in a supplementary file we do not have** (§0). The
  item can still be written from the closed form, but a session that promises
  to *derive* it must either re-derive from equations 4–6 or say the
  derivation is cited to an SI.
- **The printed Basic Model R₀ has the wrong denominator** (§0). Any item that
  asks a student to compute R₀ from Table 1 must state the formula itself, or
  must be designed to have the student find the error — which is the better
  item.
- **No parameter in R₀ᵀ was ever measured in a patient.** Both P and D carry
  W03's `††` footnote. An autograded item should ask for the threshold, not
  for a prediction about a human.
- **W03 provides no uncertainty on anything.** No confidence intervals, no
  sensitivity other than the Table 1 footnote-*a* ranges. An autograder with a
  tolerance band will have to invent the band.

---

## 11 · Contradictions with what the repo already says

Checked against `docs/coverage-matrix.md`, `docs/project-papers.md`,
`docs/deck-triage.md` and `private/log/week13-handoff.md` as they stood on
7 November 2026.

**(a) `private/log/week13-handoff.md` omits T73 from session 25.** Its §2
table lists only two S25 targets — T67 and T68 — and says "T64 and T67 are
also on the final." But `docs/coverage-matrix.md` line 146 assigns
**T73, "Compute R₀ for a therapeutic interfering particle", to S25 (Nov 19),
PS9 + Final, AUTO**, and line 234 lists PS9 as covering "T61–T70, T73". The
matrix rows are out of numerical order, which is how T73 was missed.
**S25 owes three assessed techniques, two of them autograded, and the handoff
undercounts the week's library work.**

**(b) `docs/deck-triage.md` line 111 still describes S25 as "Minimal and
synthetic cells".** Line 82 of the same file already says "L25 Epidemics |
KEEP — DIPs/TIPs → population-scale design | S25", so the file contradicts
itself. The stale row predates the 19 October decision. T68 now sits in a
population-scale session; §8 is the material that connects them.

**(c) `docs/project-papers.md` on T₀.** It says Table 1 gives "burst size
≈ 200, clearance ≈ 30/day, **T₀ = 800/µl**". **All three are correct as
printed.** But the *healthy* T-cell level in the model is λ/d = **1550/µl**,
not 800 — 800 is the infected set-point value, and Fig. 2c's inset recovers
~1500. A session that uses 800 as "normal CD4" will get R₀ wrong by a factor
of two. Not an error in project-papers.md; a trap it does not warn about.

**(d) `docs/project-papers.md` says the W03 supplementary URL is dead.**
We did not test it (no web access was used). The URL printed in the paper is
`http://genomics.lbl.gov/suppinfo/JVI/index.html`. If `project-papers.md` is
right, then **seven** distinct results W03 cites to its SI are unavailable:
the R₀ᵀ derivation, the eclipse-phase equations, F(δ,n), the crHIV
superinfection variant, the viral-loss-on-infection variant, the oscillation
figure, and the immune-response model variant. That is a material fraction of
the paper's claims and the session should say so rather than cite them.

**(e) `docs/project-papers.md` calls W03 "the only closed-form R₀ in the whole
TIP literature".** Nothing we read contradicts it, and `readings.yaml` repeats
it. **We cannot confirm it** — it is a claim about a literature, and we read
three papers. `[unverified]`; harmless on a slide only if phrased as "the
closed form that the later papers fit numerically", which is what
`project-papers.md`'s own next clause says.

**(f) `docs/project-papers.md` on the descendants, which we have NOT read.**
Recorded here so a session author knows what is being claimed on faith:
Pitchai et al. *Science* 385 (2024) — SHIV TIPs in macaques, "R₀ ≈ 24 for HIV
alone, ≈ 12 with TIPs present", 94% titre reduction in vitro, 3–4 log₁₀ plasma
viral load reduction for ~30 weeks, public repo at
`github.com/khetanneha/HIV-SIV-TIP-Modeling` and Zenodo 10.5281/zenodo.11391302;
Chaturvedi et al. *Cell* 184 (2021) — SARS-CoV-2 TIPs, measured R₀ ≈ 1.57; and
Chaturvedi et al. *PNAS* 119 (2022) — hamsters, ρ = 1.5, ψ = 0.02.
**Two things to flag.** First, project-papers.md's R₀ ≈ 24 for SHIV is an
order of magnitude above W03's R₀ = 1.9375 for HIV, which is a real
discrepancy between the 2003 parameterization and the 2024 one and is worth a
sentence rather than a quiet reconciliation — §5b shows the threshold barely
cares, which is the reassuring version. Second, **Pitchai's TIPs are deletion
mutants competing for Gag, not inhibitors suppressing Gag production**, so
W03's D-knob does not map onto them cleanly and the §5c paradox may not
transfer. Neither point is settled by anything in this folder.

**(g) Nothing contradicts `docs/coverage-matrix.md`** beyond (a).

---

## 12 · Anything that undercuts a clean teaching story

Collected so a session author can choose which wrong turns to teach. Ranked.

1. **§4c, the burst-size blow-up.** W03's binomial fixes composition but its
   equations scale total output by (1+P)². At the headline design point the
   I_D cell must release 816,000 virions. The paper's own best-case cited
   burst is 40,000, unpublished; its measured one is 200. **This is the
   richest item in the session** and it is a wrong turn the paper walks into
   with its eyes open — p.8 states the assumption plainly, and the abstract
   does not.
2. **§5c, the paradox, and the limit of the paradox.** It is a property of
   *this* architecture, where D multiplies both production terms. Teaching it
   as a general law of interfering particles would be a defect. The deletion-
   based TIPs that followed may not share it.
3. **§3, D reads backwards.** The paper's prose definition and its equations
   disagree in sense. A student who takes the definition at face value gets
   every sign wrong.
4. **§0, the printed R₀ has a δ where a *d* belongs.** Dimensionally the
   formula is fine either way, which is why it survived review; only the
   arithmetic catches it. Good lesson about what dimensional analysis cannot
   do.
5. **§2a, λ and k are fitted, not measured, and Table 1 half-hides it.**
   R₀ = 1.9375 is (λ/d)/T₀ = 1550/800 by construction. The model cannot be
   wrong about the set point because the set point was used to build it.
6. **§4d, the heterozygote strike-out rests on one in-vitro paper and one
   committee-review citation.** Two-thirds of every I_D cell's output is
   deleted from the model on that basis. If heterozygous virions *were*
   infectious the ratio would be 1 : 2P + P² = 1 : P(P+2), changing R₀ᵀ by
   (P+2)/P — only 2% at P = 100, but a factor of 3 at P = 1. **COMPUTED.**
   So the assumption matters most exactly where the threshold is, which is the
   uncomfortable version.
7. **W03's two caption/panel mismatches** (§5c box): D = 0.1 vs. D = 0.2 for
   the oscillating trace, and optimal D = 0.2 vs. 0.4. Small, real, findable.
8. **HB70's two loose text-vs-Table-1 percentages** (§7c box).
9. **N18's headline efficiency range, 0.37–0.99, silently drops the 14%
   female mosquito value** that is in its own Appendix table and its own
   Fig. 1B (§6b).
10. **N18 is entirely a model and says so.** "The fitness parameter, f, is
    typically not measured in proof-of-concept studies." Every invasion
    probability in it is conditional on a fitness nobody has measured. Its
    defence — that every assumption is worst-case for the drive — is sound and
    should be stated, not assumed.

---

## 13 · How much of this is twenty-three years old

**What W03 itself claims about feasibility — QUOTED, so the session can hold
the paper to its own words:**

| claim | status in the paper |
|---|---|
| P ≈ 100 is reachable by combining splice-signal removal, a CTE, and WPRE | "**may** yield crHIV-1 vectors capable of packaging 100 times more efficiently than HIV-1 (**Weinberger et al., unpublished**)" (p.7) |
| the therapy needs only one dose | "crHIV vectors have long-term therapeutic potential with a **single administration**, thereby reducing expense, eliminating the need for strong patient compliance" (p.8) |
| a very high crHIV-1 burden may be tolerable | high lentiviral vector loads do not cause disease in rats (ref 24); wild African green monkeys carry SIV at **3 logs higher** than human AIDS patients and stay healthy (ref 22). Both **QUOTED**, both about other species. (p.7) |
| the system will reach a steady state at all | argued from precedent — HAART, apheresis, anti-CD8 in macaques, HIV-1/HIV-2 and HIV-1/HCV co-infection all push patients to new stable set points (pp.7–8). An argument by analogy, and W03 labels it as one: "there is **ample precedent for assuming**". |
| **the largest risk, in the paper's own words** | "the most significant risk of the crHIV-1 approach is the potential for crHIV-1 to be **transmitted between individuals**. The propagation of this genetic material within the HIV-1-infected population poses significant concerns" (p.8) |

That last row is the session's hinge and it is in the required paper: **a
therapy designed to spread inside a patient will also spread between
patients**, and W03 says the authors think that "may also be worthwhile to
examine". Noble 2018 is the same sentence about a different organism, written
fifteen years later with the arithmetic done. **The two optional readings are
the before and the after of the required one** — HB70 is the natural
phenomenon, W03 is the engineering proposal, N18 is what happens when
somebody computes the escape probability.

**W03's own stated open experimental questions, QUOTED (p.8):** "Our results
emphasize the importance of quantifying both the maximum viral output from
HIV-1-infected cells and determining conclusively whether HIV-1 encapsidation
proteins are a limited intracellular resource in vivo." Both bear directly on
§4c.

**What we did NOT look up, and a session author may want to — flagged, not
answered.** No web search was performed for this file. Each of these is open:

- **Did anything move P?** W03's P ≈ 100 rests on a 2003 personal
  communication. Whether any published construct has reached it is unknown
  to us.
- **What happened to Dropulic's antisense-*env* vector** that W03 reports
  "currently entering phase I clinical trials" (p.7, ref 13)?
- **Did a crHIV-1 / TIP ever go into humans?** `docs/project-papers.md` puts
  the state of the art in **macaques** (Pitchai 2024) and **hamsters**
  (Chaturvedi 2022). We have read neither.
- **Is the An et al. preintegration block still the accepted account** of
  heterozygous lentiviral virions, 27 years on?
- **Has the inter-individual transmission risk W03 names been addressed?**
  Pitchai's conditional-replication framing (R₀^TIP > 1) is the same design
  variable; whether anybody has published an inter-host model is unknown to
  us. `project-papers.md` points to Metzger, Lloyd-Smith & Weinberger,
  *PLoS Comput Biol* 7:e1002015 (2011) as the three-scale model — unread.
- **What has happened in gene-drive field policy since 2018?** N18's
  recommendations are addressed to a National Academies report that was two
  years old when it was written.

---

## 14 · What is NOT claimed in this file

- **We did not read the W03 supplementary information.** Seven results are
  cited to it and are marked `[unverified]` above.
- **We did not read Chaturvedi 2021 or Chaturvedi 2022.** Nagoor Pitchai 2024 WAS read on 7 November -- see §16.
  Everything about them in §11(f) is quoted from `docs/project-papers.md`,
  which was written earlier and may be stale.
- **We performed no web search.** Every `[unverified]` in §13 stays open.
- **No number here is a claim about human therapy.** W03 is a model; its
  only in-vivo anchors are rhesus macaques, African green monkeys, rats and
  mice, all cited second-hand.
- **The Fig. 1F digitization is ours**, to about ±0.01, calibrated against
  printed tick labels and not against marker counts. N18's own text values
  (0.35 at a release of 15, 0.38 asymptote at P = 0.5) agree with it.
- **The Fig. 2c discrepancy of 58 vs. 21.4 cells/µl is unresolved.** Do not
  present either number as settled.
- **"The only closed-form R₀ in the TIP literature" is not ours**; it is
  `project-papers.md`'s and `readings.yaml`'s, and we cannot confirm it.

---

## 15 · Cross-references found after the main pass

`sessions/s25-populations/PRIOR-YEARS.md` landed in this directory while this
file was being written. Two of its findings change what §4 and §11 have to
say, and are recorded here rather than silently folded in.

**(a) Session 2 already promised this binomial, on a slide students have
seen.** PRIOR-YEARS §5.1 quotes `decks/s02_substrate.py`, the 67–71 min slide,
body text: *"A plasmid at 5 copies splits binomially: P(one daughter gets
none) = 2·(½)⁵ ≈ 6%"*, with the forward reference `→ sessions 12, 25`, and the
speaker note *"Session 25 does the full binomial calculation for a genome."*

**These are two different binomials over the same distribution, and the
difference is the lesson. INFERRED BY US.**

| | session 2's binomial | W03's binomial (§4) |
|---|---|---|
| what is drawn | 5 plasmid copies, each to one of 2 daughters | 2 RNA strands, each HIV-1 or crHIV-1 |
| n, p | n = 5, p = 1/2 | **n = 2**, p = P/(1+P) |
| the quantity | P(a daughter gets none) = 2·(1/2)⁵ = 0.0625 | the three virion genotypes, 1 : 2P : P² |
| what it is a statement about | **loss** — a partition failure | **composition** — which genotype a particle is |

The plasmid case draws many objects at a fixed p; the virion case draws
exactly two objects at a p the engineer sets. **P is the only tunable thing in
the whole session that enters a probability**, and a session that puts the two
binomials side by side has the s02 promise kept and T67 motivated in one
slide. (**COMPUTED check of the s02 number: 2·(1/2)⁵ = 0.0625 = 6.25%.**)

**(b) The prior-year decks used a different parameter set, and a session
author should not mix them.** PRIOR-YEARS §2.2 records that the only HIV-DIP
model parameters in eight years of this lecture appear in a **speaker note**,
cited to Rouzine & Weinberger, *J. Virol.* 87:2081–2093 (2013): **P = 5,
R₀ = 10, η = 2/5/10, set point 3 × 10⁴ copies/ml.** W03 (the assigned paper)
has R₀ = 1.9375, V₀ = 10⁵ copies/ml, P swept 1–100, and no η at all.

**COMPUTED, so the gap is visible:** at R₀ = 10, 1 − 1/R₀ = 0.9 and the
threshold is P²D > 1.111; at P = 5 that is **D > 0.0444**. Under W03's
R₀ = 1.9375 the same P = 5 needs **D > 0.0827** — a factor of 1.86. The
threshold is robust (§5b(ii)) but the numbers are not interchangeable.
**Do not put a Rouzine number and a Weinberger 2003 number on the same slide
without saying which model each belongs to.** Rouzine & Weinberger 2013 is not
in `private/readings/` and we have not read it; η is undefined for us.
`[unverified]`.

**(c) PRIOR-YEARS §5.2 independently reaches §11(a) and §11(b) of this file.**
Two passes, two routes, same two defects: the coverage matrix points three
assessed techniques at one meeting, and `docs/deck-triage.md` contradicts
itself about what session 25 is. Treat that as corroborated, not as two
separate findings.

---

## 16 · NAGOOR PITCHAI et al., Science 385(6709):eadn5866 (2024) — read 7 November 2026

Author manuscript in `private/readings/`, 26 pp, instructor copy, not assigned.
Senior author Leor Weinberger, so this and the s25 required reading are the same
lab twenty-one years apart. **First author's surname is Nagoor Pitchai**;
`docs/project-papers.md` and `readings.yaml` both said "Pitchai" and are fixed.

### 16.1 It settles the open question move 4 hands the room

The s25 design asks whether W03's paradox — that the antiviral payload D sits in
the vector's own production term, so too much D kills the vector — survives in
the TIPs that were actually built. **It does not, and the reason is clean.**

W03's vector **suppresses** HIV production, and depends on what it suppresses.
Nagoor Pitchai's TIP does not suppress anything. **It competes for what is
already made.** QUOTED, p.4 of the manuscript: TIP RNAs are described as
"competing intracellularly for viral Gag polyprotein precursor". The framing is
set earlier in the same terms — DIPs are "parasites of the wild-type virus
within infected cells, stealing essential viral proteins". **KIND: QUOTED.**

**The experiment that ties interference to packaging, QUOTED:** deleting the
TIP's packaging signal Ψ "significantly blunted the interference effect by ~30%"
(Fig. 2H). So the interference travels with the packaging competition, not with
a suppression term.

### 16.2 What that does to the two knobs — INFERRED BY US, and stated as such

In W03 there are two, P (packaging advantage) and D (antiviral payload), and D
appears in equations [3] and [6] both, which is the whole paradox. In a
deletion-and-competition TIP **there is no D at all**: the interference *is* the
competition, so the packaging advantage is the only knob and more of it helps
both the therapy and the vector's own spread. **W03's optimum becomes a
maximum.** This is ours, not theirs — they never frame it against W03's D — and
it should be labelled INFERRED BY US on any slide.

### 16.3 Why this is better teaching than the open question it replaces

The session can now close move 4 on a twenty-one-year arc in the instructor's
own lab rather than on a shrug: 2003 writes down a threshold with two knobs and
finds that one of them has an optimum because the vector parasitizes what it
suppresses; 2024 builds a working TIP by removing that knob entirely. **The
paradox was a property of the architecture, and the architecture changed.**
That is exactly what "in this architecture" was protecting, and it is now
demonstrable rather than a caveat.

The construction, QUOTED from the abstract: the DIP was engineered into an
R₀ > 1 TIP "by introducing additional deletions to ablate splicing and eliminate
expression from all HIV reading frames and repairing the HIV central polypurine
tract". Deletions and ablation throughout — nothing added that suppresses.

---

## 17 · W03's own section structure, and where the burst-size assumption is stated — read from the PDF 7 November 2026

Added because the s25 design made two claims about W03's structure that
§§0–16 did not support. Extracted with `pdftotext -layout` from the assigned
PDF and located by the running heads, which carry the journal page of every
line.

**W03's body headings. KIND: QUOTED.** The paper has exactly two:
**THEORY** (journal 10029, right column) and **RESULTS AND DISCUSSION**
(journal 10034). There is **no Materials and Methods section**, and the
introduction runs unheaded from the abstract to the THEORY heading. So a slide
may say the paper has no Methods section. It may **not** say that Results and
Discussion is the paper's only body heading, which is what the design said
before this section existed.

### 17a · The burst-size assumption, in three places, each with its page — QUOTED

1. **The introduction's summary of results, journal 10029**, verbatim:
   *"Furthermore, our model suggests that it is important for the burst size of
   cells producing therapeutic virus to exceed the burst size of
   HIV-1-infected cells. We rely on reports that HIV-1-infected cells in vivo
   have the potential to produce much more virus than typically seen (23),
   implying that packaging resources within the infected cell (such as the
   HIV-1 Gag-Pol polyprotein that is cleaved into the HIV-1 capsid) are not
   limiting. (“Competition” for these increased packaging resources within
   infected cells is not ruled out and is the focus of ongoing research). The
   study presented here highlights the need to determine both the maximum
   possible viral output from HIV-1-infected cells and the potential of Gag-Pol
   to act as a limiting intracellular resource in vivo."*
2. **The THEORY section, journal 10031** — the paragraph that supplies 200,
   "3 to 5 times more" and 40,000, with the refs §4c above gives.
3. **The discussion, journal 10035**, verbatim: *"As stated above, our model
   assumes that the I_D cell burst size is greater than n, implying that
   intracellular packaging resources are not limited."*

So §6 of the design is right that the paper states the assumption three times,
and the statement is now citable line by line. What the paper does not do is
bound it: it never says how much greater than n, and never sets its own ceiling
of 40,000 against the 816,080 its equations demand at P = 100, D = 0.4
(§4c). The abstract and the Fig. 3b caption carry none of it.

### 17b · What W03 says about the one measurement that exists — QUOTED, journal 10035

Verbatim: *"While in vitro studies have demonstrated that encapsidation
resources, most likely Gag-Pol, within a dually infected cell are a limited
resource (8), we discussed above in vivo evidence (23) that SIV-infected rhesus
macaques cells can produce many more virions than the ~200 observed (17). This
suggests that, rather than resource depletion, immune recognition and killing
of infected cells, as well as the pathogenicity of HIV-1 proteins (such as
Nef), seem to be destroying the cell before it can produce its full potential
of virus. Our results emphasize the importance of quantifying both the maximum
viral output from HIV-1-infected cells and determining conclusively whether
HIV-1 encapsidation proteins are a limited intracellular resource in vivo."*

**Consequence, INFERRED BY US, and it corrects a sentence the design carried.**
"Which model is right is an empirical question nobody has answered" is too
strong in one direction and too weak in another. The one direct measurement
exists and it points at the **capped** model: ref 8 (Bukovsky 1999), in vitro,
found encapsidation resources in a dually infected cell to be limited. W03
argues past it — not by disputing the measurement, but by proposing that the in
vivo ceiling is set by immune killing of the cell rather than by resource
depletion. Both of its own stated open questions are the measurements that
would decide it, and neither has been made in vivo. **So: the only direct
measurement favours the capped model, W03's counterargument is a mechanism
rather than a measurement, and the deciding experiment is the one the paper
asks for.** That is the honest version, and it is sharper than a shrug.

### 17c · W03 names competition for Gag-Pol twenty-one years before Pitchai builds on it — INFERRED BY US

The parenthesis in §17a is the paper saying, in 2003, that competition for
packaging resources inside an infected cell "is not ruled out and is the focus
of ongoing research". §16 records that Nagoor Pitchai 2024's TIP interferes by
**competing intracellularly for the viral Gag polyprotein precursor**. Gag-Pol
is the packaging resource of the 2003 parenthesis, so the mechanism the later
paper is built on is the one this paper set aside as unresolved. **INFERRED BY
US** — the 2024 paper does not frame itself against this sentence, and any
slide making the connection must say whose reading it is.

---

## 18 · R₀ᵀ RE-DERIVED FROM EQUATIONS 4–6 — DERIVED BY US, 7 November 2026

**Why this section exists.** T73 is autograded on PS9 and sits on the final,
and until today the expression it assesses traced only to a supplementary file
nobody here has read, behind a dead URL. §1 named the way out and this is it.
Everything below is **DERIVED BY US**, independent of the SI. Three routes
agree.

### 18.1 The construction

Infection subsystem **x = (I_T, I_D, V_T)**, linearised at the **HIV-endemic,
therapy-free** equilibrium E\* — *not* the disease-free one. The choice is
forced by W03's own definition on p.6: R₀ᵀ is the number of new crHIV-1
infections from one I_T cell *"assuming that the system is at steady state for
HIV-1 infection."* At the disease-free equilibrium V\* = 0, an I_T cell can
never be superinfected, I_D is never populated, and **R₀ᵀ ≡ 0 for every P and
D** — degenerate, not merely different. The vector is an obligate parasite of
an established infection, which is the session's framing and is correct.

At E\*: **T\* = c/(kn) = 800.000 cells/µl**, **V\* = (kλn − cd)/(ck) = 100.000
virions/µl = 10⁵/ml**, **I\* = cV\*/(nδ) = 21.4286 cells/µl**. The 6×6 Jacobian
there is block upper-triangular, because rows 4–6 carry zero derivatives with
respect to (T, I, V) when I_T = V_T = 0. So the invasion block decouples
**exactly**; the next-generation construction is not an approximation here.

    F = [[0, 0, c/n],      V = [[ kλn/c,      0,   0],
         [0, 0,   0],           [ d−kλn/c,    δ′,  0],
         [0, 0,   0]]           [   0,   −P²Dnδ′,  c]]

    F·V⁻¹ = [[ D·P²·(kλn − cd)/(kλn),  D·P²,  1/n],
             [          0,               0,     0 ],
             [          0,               0,     0 ]]

Eigenvalues {0, 0, D·P²·(kλn − cd)/(kλn)}, so

    ρ(F·V⁻¹) = P²·D·(1 − cd/(kλn)) = **P²·D·(1 − 1/R₀)**

with R₀ = λkn/(cd). sympy confirms the difference from the published form
**simplifies identically to zero.**

### 18.2 The teachable decomposition, and the line for the slide

R₀ᵀ is a product of three factors:

| factor | value | what it is |
|---|---|---|
| kV\*/(d + kV\*) | 1 − 1/R₀ | probability an I_T cell is superinfected by HIV before it dies of old age |
| P²Dn | P²Dn | crHIV-1 virions per I_D cell over its lifetime |
| kT\*/c | 1/n | new I_T cells per crHIV-1 virion |

Two exact cancellations do all the work. **kT\*/c = 1/n exactly**, because
T\* = c/(kn) — the burst size cancels against the steady state it sets, so
P²Dn × 1/n = P²D and **R₀ᵀ contains no n at all**. And
**kV\*/(d + kV\*) = 1 − dT\*/λ = 1 − 1/R₀**, since kV\*T\* = λ − dT\* from
equation 1.

So: **1 − 1/R₀ is not a correction factor. It is the probability that an I_T
cell ever meets the wild-type virus it needs in order to replicate at all.**
That is the single best line to put on the slide, and it is what makes the
quantity an I_T-indexed ratio rather than "R₀ of the vector".

**δ′ never appears.** It cancels between production (P²Dnδ′) and I_D lifetime
(1/δ′). So the δ′ = Dδ assumption is **irrelevant to R₀ᵀ** — verified
numerically, the threshold is 2.0666666667 for δ′ ∈ {0.001, 0.05, 0.7, 5, 50}.
This is the algebraic content of W03's p.3 claim that the δ′ assumptions were
*"benign"*, and we can now state it without the SI.

### 18.3 What the derivation assumes — the complete list

1. Linearisation at the HIV-endemic therapy-free equilibrium (W03's stated
   framing; requires R₀ > 1).
2. The I_T cell as index case (W03's stated definition).
3. **No virion loss by infection** in equation 6, which W03 states explicitly
   as inherited from the Basic Model. **This one is load-bearing**: restore
   −kV_T·T and kT\*/c becomes kT\*/(c + kT\*), the 1/n cancellation breaks, and
   R₀ᵀ picks up a factor 1/(1 + 1/n) ≈ 0.995 at n = 200. W03 says relaxing it
   had "minimal quantitative effect"; it is **0.5%**, now quantified.
4. Equation 6's P² as printed, i.e. the (1+P)²-scaled burst of §4c.
5. **Not** assumed: any QSSA, any δ′ relation, the An et al. rounding, any
   neglected term.

### 18.4 The convention caveat — THE ONE AUTOGRADER RISK

Under the standard van den Driessche–Watmough split (**van den Driessche, P. & Watmough, J. *Math. Biosci.* **180**, 29–48 (2002)**, doi:10.1016/s0025-5564(02)00108-6 — QUOTED; verified against the DOI record 8 November, not from memory. Recorded here because a slide cites it, and §0 forbids anything on a slide that is not in this file), where virion *production*
also counts as new infection of the V_T compartment, F and V differ and the
spectral radius is **√(P²D(1 − 1/R₀))**. Both were computed. **The threshold at
1 is identical, so 2.0667 is convention-free** — but the *magnitude* of R₀ᵀ is
not. A student who builds the next-generation matrix by the textbook recipe
gets the square root and **is right**.

**So any item that asks for a numerical value of R₀ᵀ, rather than a threshold
or a yes/no on persistence, must state the generation convention, or it will
mark a correct answer wrong.** This is an item-design requirement, not a defect
in the formula. It applies to the PS9 autograder and to any final-exam item.

### 18.5 The numbers

    R₀       = λkn/(cd) = 31 × 1.875e-4 × 200 / (30 × 0.02) = 1.9375 = 31/16 exactly
    1 − 1/R₀ = 15/31 = 0.483871
    threshold P²D = 1/(1 − 1/R₀) = **31/15 = 2.0666666667**

A closed form worth having, from W03's own back-solve (k = c/(nT₀),
λ = dT₀ + cV₀/n):

    R₀ = 1 + cV₀/(n·d·T₀) = 1 + 3000/3200 = 1.9375
    threshold P²D = 1 + n·d·T₀/(c·V₀) = 1 + 3200/3000 = 2.0667

with V₀ = 100 virions/µl. **The threshold is a statement about four clinical
observables and the burst size, with no fitted parameter in it.**

**Sensitivity, and there is a trap.** The threshold depends on λ, k, n, c, d
and **not at all on δ or δ′** (elasticity exactly 0). But the sign of its
dependence on n and c *flips* with what is held fixed:

| perturbed | holding λ, k fixed | holding T₀, V₀ fixed (what W03 did) |
|---|---|---|
| n | −1.065 | **+0.516** |
| c | +1.068 | **−0.516** |
| d | +1.068 | +0.516 |
| δ, δ′ | 0 | 0 |

**CORRECTED 7 Nov 2026**, same pass: the R₀ line above printed
"1 + 3000/1600", which evaluates to 2.875 and not to 1.9375. n·d·T₀ =
200 × 0.02 × 800 = **3200**, so the fraction is 3000/3200 = 0.9375. The formula
and the result were right and the displayed denominator was not; the threshold
line, 1 + 3200/3000, was already correct. **COMPUTED.**

**The elasticities above are exact rationals**, and the table's decimals are
finite-difference estimates of them: with T₀ and V₀ held fixed they are
n gives **+16/31**, c **−16/31** and d **+16/31** (0.516129); with λ and k held
fixed, n gives **−16/15**, c **+16/15** and d **+16/15** (1.066667). The table's −1.065 and
+1.068 are that same 16/15 read off a coarse step. **DERIVED.**

Because λ and k were back-solved from T₀ and V₀, perturbing n with λ and k
fixed is not a physically coherent perturbation of this model. **Any
sensitivity item must say which pair is held fixed.** Magnitudes are order-1
either way, so 2.0667 is not fragile — Table 1's footnote ranges move it by
tens of percent, not orders of magnitude.

### 18.6 The fixed-burst wrong turn, now quantitative

§4c's "best wrong turn" can stop being a qualitative worry. Replace W03's
(1+P)²-scaled burst in equation 6 with a **fixed burst** partitioned
1 : 2P : P², and the same construction gives a therapy that cannot invade.

**"Capped" can be written two ways, and they are different models.** The first
draft of this section wrote only one of them while the library implements the
other. Both are recorded, because the design cites this section and a reader
checking it against the code must not find a contradiction.

| reading | vector production term | R₀ᵀ_fixed |
|---|---|---|
| **(a)** inhibition applied *before* the cap | P²/(1+P)² · D·n·δ′·I_D | [P²/(1+P)²] · D · (1 − 1/R₀) |
| **(b)** the cell makes n particles whatever happens, so the cap binds and D drops out | P²/(1+P)² · n·δ′·I_D | [P²/(1+P)²] · (1 − 1/R₀) |

**The bound is identical either way**, because D ≤ 1 and P²/(1+P)² < 1 for
every finite P:

    sup R₀ᵀ_fixed = 1 − 1/R₀ = 15/31 = 0.48387   (approached, never attained)

**So R₀ᵀ_fixed < 1 for every P and every D under both readings. The therapy can
never persist.** Verified on the Jacobian out to P = 10⁶ for both. The
conclusion does **not** turn on how the cap is written, which is why the design
states it in the form that holds for both.

**The library implements (b).** `burst_output(P, D, n, fixed=True)` partitions
a burst of exactly n with **D absent from all three counts** — checked at
P = 8, n = 200 across D ∈ {0.05, 0.2, 0.5, 1.0}, where all three counts are
identically 2.4691 / 39.5062 / 158.0247 and sum to exactly 200 — and
`test_fixed_mode_vector_output_is_independent_of_D` asserts that across a sweep
in D.

Reading (b) is also the session's own limiting case and the sharper one to
teach: under a binding cap **D disappears from the vector's output entirely**,
so making the payload more potent costs the vector nothing, which is the
paradox of W03's scaling model dissolving rather than being traded off. A slide
or item saying "D does not appear in the vector's output at all" is describing
(b) and is correct about the library.

So the burst-size assumption is not bookkeeping — it is the whole difference
between a therapy that invades and one that cannot. Exam-sized, checkable, and
now derivable rather than asserted. **COMPUTED, 7 November 2026; the
two-readings split added 8 November after the design pass found this section
and the library disagreeing about whether D survives the cap.**

### 18.7 How it was verified

- **Route 1, symbolic.** sympy; difference from the published form simplifies
  to 0.
- **Route 2, eigenvalue sign.** 352 (P, D, δ′) points over P ∈ [1, 100],
  D ∈ [0.01, 1], δ′ ∈ {Dδ, δ, 0.3, 5.0}: sign(R₀ᵀ − 1) matched the sign of the
  leading real eigenvalue of the full 6×6 Jacobian at **every point, zero
  mismatches**. Bisecting that eigenvalue for the critical P²D, using no
  formula at all, returns **2.0666666667** at D = 0.01, 0.2, 0.4 and 1.0 alike
  — which independently confirms both the value and that it depends on P and D
  only through the product.
- **Route 3, nonlinear integration** of equations 1–6 from E\* with
  V_T(0) = 10⁻¹², rtol 1e-13: the measured exponential growth rate of V_T
  matches the leading eigenvalue to **six significant figures** on both sides
  of threshold and across δ′ ∈ {Dδ, δ, 5.0}. At P²D = 2.0667 exactly the growth
  rate is +5.5e-07/day.
- **Code.** `therapeutic_R0` agrees with the symbolic spectral radius to
  **3.7e-12 relative** over 16,554 random parameter draws restricted to
  R₀ > 1. `P_min` and `D_min` return exact roots. 120 tests pass.

Convention A was chosen from W03's printed definition of the index case
**before** the algebra was run, and Convention B was computed and reported even
though it does not match the published magnitude. The scripts are in
`private/derivations/s25-R0T/`.

### 18.8 Still open, and what would settle each

- **W03's own SI derivation** was not retrieved. The only thing that turns on
  it now is which convention the authors used — ours matches exactly, so
  almost certainly Convention A. Nothing this session teaches depends on it.
- **The eclipse-phase equations** (§2b) are untouched. A delay would add a
  survival factor to each generation and would *lower* R₀ᵀ slightly; it cannot
  change the P²D product structure. Still `[unverified]`.
- **Fig. 2c's 58 vs 21.43 cells/µl** (§5d) is untouched by this work.

---

## 19 · W03's Fig. 3a stability floor, digitized — INFERRED BY US, 8 November 2026

**Why this exists.** §5 and §9 recorded W03's Fig. 3 floor only qualitatively,
and the design carried "whether our R₀ᵀ = 1 contour matches their boundary" as
`[unverified]`. It is now digitized, and the answer is that **it does not
match.** Because §18 settles our closed form three independent ways, this is a
finding about *their figure*, not about our algebra.

**Method.** Page 6 rendered at 300 dpi. The floor parallelogram's three visible
corners located as extremes of a red-or-cyan pixel mask, the affine map
inverted, and the red→cyan transition read along lines of constant D.
Transition width 0.12–0.26 in P over the range kept.

**Calibration check, and it passes.** W03's own text puts the oscillatory
region at *"P > 10 and D ≈ 0.1"*. The black pixels map to **P > 11,
D = 0.05–0.13, median 0.094**. So the affine inversion is sound and the
disagreement below is not a digitization artifact.

**The disagreement.**

| D range | their boundary, as P²D | ours |
|---|---|---|
| 0.08 – 0.20 | **1.14 – 1.29** | 31/15 = 2.0667 |
| 0.35 – 0.50 | **2.15 – 3.86** | 31/15 = 2.0667 |

Their boundary **crosses ours near D ≈ 0.35**. Our coefficient band (§5b,
1.05–2.11 over R₀ = 1.9 to 20) contains their boundary below D ≈ 0.35 and does
not contain it above.

**Consequence for the session.** This is the reason the design space must be
drawn as a **band and not a single sharp contour**, and the reason their floor
is replotted flat beside ours rather than taken as a check on our arithmetic. A
slide may not present their boundary as confirming ours.

**What is ours and what is theirs.** The twelve-point `W03_FIG3A_FLOOR` table
in `figures/s25_populations.py` and the drawn extent of the oscillatory block
are **INFERRED BY US**. The figure that uses them is titled "theirs, digitized
by us". The method and the calibration check are in a comment above the table.
Nothing in the paper states these coordinates numerically.

---

## 20 · The steady-state set point against D — DERIVED BY US, 9 November 2026

Written because `s25_setpoint_valley` prints numbers that are in no other
section, and §0 forbids a slide carrying a number that is not here.

### 20.1 The day-360 panel and the set point are different quantities

**This is the finding, and it invalidates an assumption this repo was working
under.** W03 Fig. 2a is a **360-day window**, not a steady state, and at two of
its five D values the system has not arrived:

| D | ours at day 360 | ours, equilibrium solved | ratio |
|---|---|---|---|
| 0.8 | 5.846e4 | 5.880e4 | 0.994 |
| 0.6 | 1.880e4 | 1.797e4 | 1.046 |
| 0.4 | 776.1 | 776.5 | 0.999 |
| 0.2 | 914.9 | 776.1 | **1.179** — still on the damped oscillation |
| 0.01 | 9.02e4 | **1.344e4** | **6.710** — transient runs to ~day 1500 |

The equilibrium is solved exactly from [1]–[6] as one scalar equation in T;
**δ′ cancels out of all five lines**, the same cancellation §18.2 records.

**Consequence: only three of W03's five points may be overlaid on a
steady-state curve.** `s25_setpoint_valley` plots those three and says so on
its face. Plotting all five would invite the reading that they agree, and at
D = 0.2 and D = 0.01 they are not the same quantity.

### 20.2 Agreement on the three that are set points — INFERRED BY US

Digitized from the panel against its printed ticks (same calibration as §19):

| D | theirs, digitized | day read | ours, set point | ours/theirs |
|---|---|---|---|---|
| 0.8 | 5.966e4 | 357.6 | 5.880e4 | **0.986** |
| 0.6 | 1.909e4 | 337.8 | 1.797e4 | **0.942** |
| 0.4 | 782.3 | 357.6 | 776.5 | **0.993** |

D = 0.6 is read at day 337.8 because the panel's own opaque legend box occludes
that trace past there; our integration moves 4% between day 338 and its set
point, so the read is settled.

### 20.3 The valley, and what sits at each end — DERIVED BY US

- **Minimum at D = 0.3067, 658 virions/ml, 152× below pretherapy.** The floor
  is flat across 0.2–0.4 (776 / 658 / 777), so **W03's own two answers for the
  best D — the text's 0.2 and the Fig. 3b caption's 0.4, the mismatch §5c says
  a slide must choose between — are both within 18% of the true minimum.** The
  mismatch is real and it does not matter.
- **Right end:** D = 1, no inhibition, set point 10⁵.
- **Left end:** R₀ᵀ = 1 at **D = 0.0023**, the vector cannot persist, set point
  back to 10⁵. Segment 3's threshold arriving as the left wall of segment 4's
  valley.
- **No set point at all for D = 0.0122 to 0.1152** at P = 30: the equilibrium
  is unstable (leading eigenvalue of the 6×6 Jacobian > 0). **This window
  agrees independently with the paper** — W03's text puts the oscillatory
  region at "P > 10 and D ≈ 0.1", and §19's digitization of their Fig. 3a floor
  gives P > 11 at D = 0.05–0.13. That agreement is a stronger check on our
  equations than any level comparison, because it tests the *dynamics*.

### 20.4 "The therapy has done nothing" is a WINDOW claim, not a model claim

**At P = 30, R₀ᵀ = 900 × 0.01 × 0.48387 = 4.355 > 1**, so crHIV-1 **cannot**
die out at D = 0.01. Verified independently against `posb.populations`'s own
`therapeutic_R0`. The equations put that set point at **1.344e4/ml — a 7.4×
reduction**, not nothing. The therapy-does-nothing end is at **D < 0.0023**,
where R₀ᵀ falls through 1.

So a slide or a note may say the therapy has done nothing **over 360 days, on
their panel**. It may **not** say the model gives nothing at D = 0.01.

**This is a second instance of §19's pattern** — W03's stability map is more
conservative than the algebra of W03's own printed equations. §5c quotes them
saying that for "D ≤ 0.1 … crHIV-1 will die out … and HIV-1 will rebound to the
pretherapy level"; at P = 30 the printed equations give R₀ᵀ > 1 for every
D > 0.0023. Recorded, not resolved.

### 20.5 The missing eclipse phase does not reach this figure — DERIVED BY US

The time courses' clock is 2× fast because the printed equations omit a 1.5-day
eclipse phase (§2b, and the SI is not in this repo). A delay cannot move a fixed
point — **but only if nothing dies during it**, so this was tested rather than
assumed. Erlang(m) eclipse, mean 1.5 d, on all three infection events:

- **No eclipse mortality:** set points identical to all printed digits for
  m = 1, 2, 5, 20, at every D tested. Exactly neutral.
- **Eclipse cells die at the uninfected rate d = 0.02/d**, with k and λ
  re-back-solved from T₀ and V₀ as §2a records W03 doing: valley floor
  658.42 → 652.5 (−0.9%), minimum location 0.30669 → 0.31049 (+1.2%). Worst
  anywhere the figure claims a set point is D = 0.6 at ×0.874.
- **Eclipse cells die at δ = 0.7/d:** the infection goes extinct
  (0.35 × 1.9375 = 0.68 < 1). Excluded — W03's panels contain a persistent
  infection.

**So this figure does not inherit the 2× clock defect**, which is why it ships
where the Fig. 2a time-course redraw did not.

### 20.6 The threshold depends only on P²D. The SET POINT does not. — DERIVED BY US

**Recorded because the opposite was written down and believed for a day.**
`figures/s25_populations.py`'s solver docstring asserted that V\* depends on P
and D only through the product A = P²D — "the same P²D the whole of segment 3
is about" — and that claim was carried into `posb.populations.coexistence`
when the solver was moved there on 9 November. A property test caught it the
same hour.

**It is false, and the reason is one line of the solve.** `V` as a function of
`T` is a function of A alone, which is what makes the claim look right. But `T`
is not: the residual carries **I_T = (c/(kn) − T)/D**, so D enters separately
and the equilibrium is not a function of A.

Measured at A = 270 held exactly constant:

| P | D | V\* |
|---|---|---|
| 20 | 0.675 | 3.35e4 /ml |
| 30 | 0.300 | 659 /ml |
| 100 | 0.027 | 407 /ml |

**A factor of 82**, over the range where D is a legal fraction. (P below ~16.4
needs D > 1, which `therapeutic_R0` refuses. A first draft of this note claimed
a factor of 1100 using P = 10, D = 2.7 — outside the model. Corrected the same
day.)

**So the distinction to teach is:** R₀ᵀ = P²D(1 − 1/R₀) depends on the product
alone, and it is a statement about **whether the vector persists at all**. The
level it persists at does not. A student leaving segment 3 with "it is all
P²D" and carrying that into segment 4's clinical outcome has over-generalised,
and `s25_setpoint_valley` is where that shows.

Locked by `tests/test_populations.py::test_the_set_point_is_NOT_a_function_of_P_squared_D_alone`,
which asserts the threshold is constant to machine precision across the same
sweep in which the set point moves by more than 50×.
