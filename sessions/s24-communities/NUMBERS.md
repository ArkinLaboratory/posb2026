# Session 24 — every number, with its kind

Extraction only. Nothing here is a segment, a slide or a session plan.

**Sources.** PDF page numbers are pages of the file named; journal pages are
given where they differ.

| tag | file | PDF pp. | journal pp. |
|---|---|---|---|
| **BAL** | `private/readings/Session 24 - balagadde-2008-predator-prey-ecosystem.pdf` | 1–8 | *Mol Syst Biol* **4**:187, pp. 1–8 |
| **BASU** | `private/readings/Session 24 - basu-2005-programmed-pattern-formation.pdf` | 1–5 | *Nature* **434**:1130–1134 |
| **TSOI** | `private/readings/Session 24 - tsoi-2018-metabolic-division-of-labor-OPTIONAL.pdf` | 1–6 | *PNAS* **115**(10):2526–2531 |

BASU PDF p.1 = journal p.1130 and begins with the tail of an unrelated paper on
long-tailed tits; the Basu text starts in the right-hand column of that page.

Kinds used, exactly as the brief defines them: **MEASURED**, **QUOTED**,
**MODELLED**, **DERIVED**, **COMPUTED**, **INFERRED BY US**.

> **Everything in §2.2, §3.3, §8.2 and §9 came out of a rendered page, not out
> of `pdftotext`.** Panel numbers are invisible to text extraction. Where a
> value was read off a curve rather than printed, it says so and gives the
> calibration. Every digitization below is calibrated against **printed tick
> labels**, never against a count of markers.

> **The single most consequential finding, stated once here so it is not
> buried.** Neither required paper prints a numeric AHL threshold, a numeric
> ring radius with error, or a measured diffusion coefficient. BASU prints a
> complete model with a complete parameter set; BAL prints no model equations
> at all (they are in a supplement this repo does not hold). So **T65 and T66
> have to be built on BASU's printed model, not on either paper's data**, and
> T66 additionally needs a diffusion coefficient that **no paper here
> supplies**. See §9, §13 and §16.

---

## 1 · BAL — the circuit, wired exactly

Read off **Box 1A, p.2** (rendered), cross-checked against the Box 1 caption
(p.2), the Results text (pp.2–3) and the Plasmids methods (p.6).

### 1.1 Predator cell (*E. coli* **MG1655** unless noted; p.3)

| element | promoter | what it does |
|---|---|---|
| `luxR`–`lasI` operon | **P**<sub>LtetO-1</sub> | constitutive in MG1655 (p.3) |
| LasI | — | synthesizes **3OC12HSL** → exported to the prey |
| LuxR | — | receiver for **3OC6HSL** arriving from the prey |
| `ccdA` (antidote) | **P**<sub>luxI</sub> | activated by LuxR·3OC6HSL |
| `ccdB` (suicide) | **P**<sub>lac/ara-1</sub> | induced by IPTG |
| `gfpuv-lva` | **P**<sub>LtetO-1</sub> (plasmid ptetGFPuv(LVA)) | marks the predator (p.3) |

CcdA inhibits CcdB; CcdB kills the predator. So **the predator dies by
default and is rescued by the prey's signal.**

### 1.2 Prey cell (*E. coli* **Top10F'** unless noted; p.3)

| element | promoter | what it does |
|---|---|---|
| `luxI`–`lasR` operon | **P**<sub>lac/ara-1</sub> | induced by IPTG |
| LuxI | — | synthesizes **3OC6HSL** → exported to the predator |
| LasR | — | receiver for **3OC12HSL** arriving from the predator |
| `ccdB` (killer) | **P**<sub>luxI</sub> | activated by LasR·3OC12HSL |

So **the prey is killed by the predator's signal**, and has no antidote.

### 1.3 The two directions, in one line each

- **Prey → predator (rescue):** LuxI → 3OC6HSL → LuxR → P<sub>luxI</sub> →
  **CcdA** → neutralizes CcdB → predator lives.
- **Predator → prey (killing):** LasI → 3OC12HSL → LasR → P<sub>luxI</sub> →
  **CcdB** → prey dies.

**Both arms terminate on the same promoter, P<sub>luxI</sub>, in different
cells.** The authors say why: both active LuxR and active LasR initiate at
P<sub>luxI</sub> (p.3, citing Gray *et al.* 1994). QUOTED — they cite it and
show it only in Supplementary Figure S3.

### 1.4 The killing effector, and the part that had to be re-engineered

- The toxin is **CcdB**, as a **LacZα′–CcdB fusion** (p.2–3). MEASURED/QUOTED.
- The original **LacZα–CcdB** fusion from You *et al.* 2004 "might lack the
  necessary toxicity (data not shown)" (p.2). **The supporting data are not
  shown**; flag it rather than teach it as a result.
- Fix: deleting **32 amino acids** from LacZα gave **an eight-fold increase in
  potency** (p.3, Supplementary Figure S2). MEASURED — but the supporting
  figure is supplementary and this repo does not hold it. `[unverified in the
  file we hold]`
- Underlying DNA edit: **96 base pairs** deleted between two NstI sites in the
  LacZα–CcdB coding region (p.6, Plasmids). MEASURED.
- The antidote is **CcdA**, cloned from the **F plasmid** (p.6).

### 1.5 Plasmids as printed (p.6)

| plasmid | origin | marker | contents |
|---|---|---|---|
| `placCcdBs` | **p15A** | Kan<sup>R</sup> | `lacZα′-ccdB` + its upstream *lac* promoter, in pPROLar.A122 |
| `ptetLuxRLasI-luxCcdA` | **SC101** | Cm<sup>R</sup> | P<sub>LtetO-1</sub>–`luxR`–`lasI`; P<sub>luxI</sub>–`ccdA` in the opposite direction |
| `pLasRLuxI-luxCcdBs` | **p15A** | Kan<sup>R</sup> | P<sub>lac/ara-1</sub>–`lasR`–`luxI`; P<sub>luxI</sub>–`lacZα′-ccdB` |
| `ptetGFPuv(LVA)` | **ColE1** | Cm<sup>R</sup> | GFPuv with a C-terminal LVA tag |

- p15A copy number stated as **20 per cell** (p.3). QUOTED.
- **A printed inconsistency.** The methods sentence describing
  `ptetLuxRLasI-luxCcdA` places `ccdA` "in opposite direction from the
  P<sub>LtetO-1</sub>-***lasR***-`lasI` cassette" (p.6), but the cassette built
  two sentences earlier is **`luxR`-`lasI`**, and Box 1A draws `luxR`-`lasI`.
  Treat the methods sentence as a typo for `luxR`. INFERRED BY US.

---

## 2 · BAL — the three regimes, and what moves between them

### 2.1 The three regimes, named by the authors

Box 1B caption, p.2: a line of **Hopf bifurcation points** demarcates
**(i) prey domination, (ii) predator–prey oscillation, (iii) predator
domination**. MODELLED — this is their bifurcation analysis of equations
S14–S17, not an experiment.

### 2.2 Box 1B left panel, read off the rendered page (p.2)

Axes as printed: *x* = **predator growth rate k<sub>c1</sub> (h⁻¹)**, 0.0–2.0;
*y* = **predator death rate d<sub>c1</sub> (h⁻¹)**, 0.0–2.0. A dashed line at
**d<sub>c1</sub> = 1.0** carries three marked points, labeled in the right
panel as:

| point | k<sub>c1</sub> (h⁻¹) | regime | right-panel trace |
|---|---|---|---|
| i | **0.2** | prey domination | prey ≈ 75 ×10³ cells µL⁻¹, predator ≈ 0 |
| ii | **0.8** | oscillation | prey swings 0 → 80 ×10³, ~3 cycles in 400 h |
| iii | **1.2** | predator domination | predator ≈ 8–9 ×10³, prey ≈ 2–3 ×10³ |

All MODELLED. The k values are **printed** in the right panel labels
("i. k<sub>c1</sub> = 0.2", etc.), so no digitization was needed; the
population values are read off the printed y-axis ticks (0/40/80 for i and ii,
0/6/12 for iii) and are approximate.

**Read the right-panel y-axis.** It is **10³ cells per microliter** — a
*concentration*. Every other population number in this paper is **cells per
reactor**. Do not put the two on the same axis.

**A caption/axis mismatch worth knowing before anyone builds a slide.** The
caption says the bifurcation is in **d<sub>c</sub> ( = d<sub>c1</sub>
(predator) = d<sub>c2</sub> (prey))** and **k<sub>c</sub> ( = k<sub>c1</sub> =
k<sub>c2</sub>)** — i.e. both species are set equal — while the printed axis
labels say "**Predator** death rate d<sub>c1</sub>" and "**Predator** growth
rate k<sub>c1</sub>". The axes are labeled for one species and the caption
says they apply to both. INFERRED BY US; the caption is the authority.

### 2.3 The one qualitative statement they make about d<sub>c1</sub>

"increasing d<sub>c1</sub> significantly broadens the parameter region that
gives rise to oscillation" (p.2). MODELLED. No number is attached to
"significantly" anywhere in the main text.

### 2.4 The two control parameters they actually turn, experimentally

| knob | what it does, in the authors' words | regime it buys |
|---|---|---|
| **IPTG** | induces `ccdB` in the predator and the QS system in the prey (p.3) | 0 → prey washout; ≥5 µM → oscillation (p.4) |
| **dilution rate *D*** | washout | 0.11 h⁻¹ → coexistence; 0.20 h⁻¹ → damped, short period; 0.31 h⁻¹ → predator washout (p.5) |

Both MEASURED as experimental settings. Note that **IPTG acts on both
populations at once** — it is not a clean single-parameter knob, and the
authors say so: it raises 3OC6HSL production by the prey *and* CcdB expression
by the predator (p.4).

---

## 3 · BAL — every number in the paper, with its kind

### 3.1 Liquid-culture controls, Figure 1 (p.3)

| quantity | value | kind | where |
|---|---|---|---|
| culture volume per condition | 2 mL, split from 6 mL LBK | MEASURED | Fig. 1 caption, p.3 |
| IPTG in the "+IPTG" cultures | **1 mM** | MEASURED | Fig. 1 caption, p.3 |
| AHL in the "+IPTG+AHL" cultures | **100 nM** | MEASURED | Fig. 1 caption, p.3 |
| incubation before OD read | **20 h** | MEASURED | Fig. 1 caption, p.3 |
| replicates | triplicate; error bars = s.d. | MEASURED | Fig. 1 caption, p.3 |

Qualitative results (p.3, MEASURED): predator grows high in OFF, is strongly
inhibited by 1 mM IPTG, and is **rescued by 100 nM 3OC6HSL**; rescued
predators grow "slightly slower" than OFF. Prey grows in OFF and in IPTG
alone, and **perishes with IPTG + 3OC12HSL**; IPTG alone retards prey growth.

The authors offer **two unresolved explanations** for the residual growth
retardation in each panel — metabolic burden, incomplete CcdA neutralization
(predator, p.3); metabolic burden, basal CcdB from **3OC6HSL–LasR crosstalk**
(prey, p.3) — and settle neither. That crosstalk admission matters: the
circuit's orthogonality is not clean.

### 3.2 Microchemostat conditions (pp.3, 6, 7)

| quantity | value | kind | where |
|---|---|---|---|
| reactor volume, this version | **~9 nL** (reduced from ~16 nL) | MEASURED | p.3 |
| reactors per chip | **14** (up from 6) | MEASURED | pp.3, 6 |
| population per reactor | **~10²–10⁴ cells** vs ≥~10⁹ in macroscale | QUOTED/MEASURED | p.3 |
| **detection limit** | **~75 cells per reactor** | MEASURED | p.4 |
| imaging-section height | **3 µm** over a **150 µm** stretch (vs ~10 µm elsewhere) | MEASURED | p.6 |
| phase-contrast images per count | typically **8**, with rotary mixing between | MEASURED | p.6 |
| fluorescence images per count | typically **4** | MEASURED | p.6 |
| GFPuv filter set | ex **395/40**, em **510/40** | MEASURED | p.6 |
| device material | PDMS (GE RTV 615), multilayer soft lithography | — | p.6 |
| seeding density | **~20 cells nL⁻¹** | MEASURED | p.7 |
| medium | LBK: 10 g tryptone, 5 g yeast extract, 7 g KCl per L | MEASURED | p.6 |
| buffering | 100 mM weak acid; PIPES pH 6.2 & 6.6, MOPS pH 7.0; KOH to pH | MEASURED | p.6 |
| microchemostat pH used | **7.0** | MEASURED | p.7 |
| anti-adhesion adjuvant | **5 g L⁻¹ BSA** | MEASURED | p.7 |
| antibiotics, microchemostat | **50 µg mL⁻¹ Kan + 15 µg mL⁻¹ Cm** | MEASURED | p.7 |
| antibiotics, liquid culture | **50 µg mL⁻¹ Cm + 50 µg mL⁻¹ Kan** | MEASURED | p.6 |
| macro-scale activation | **1 mM IPTG + 0.05 % arabinose** | MEASURED | p.7 |
| shaking, tube culture | 37 °C, 250 r.p.m., 12 mL tube | MEASURED | p.7 |
| starter dilution | **1000-fold** into 4 mL | MEASURED | p.7 |
| preculture | 2 mL + 10 µL mini-stock, 280 r.p.m., ~9 h, 37 °C | MEASURED | p.7 |
| growth temperature | **37 °C** throughout | MEASURED | pp.6–7 |

**Why the microchemostat, in the authors' own argument (p.3).** The small
population "reduces the number of cell division events per unit time and hence
slows down microbial evolution", and the circuit's "short-lived stability" in
macro-sized populations meant "function was lost before the circuit behavior
could be appreciably observed" (p.3). **This is session 23's thesis arriving
as an experimental constraint**, and it is QUOTED/MEASURED, not an aside.

### 3.3 Figure 2 — IPTG as the control parameter

Printed in the text and caption (MEASURED):

| quantity | value | where |
|---|---|---|
| Fig. 2A conditions | **IPTG = 5 µM, D = 0.1125 h⁻¹** | caption p.4 |
| Fig. 2A period | **~180 h** | p.3, caption p.4 |
| prey peak, Fig. 2A | **~35 000 cells per reactor**, reached in ~10 h | p.3 |
| prey trough, Fig. 2A | "just a few cells per reactor" | p.4 |
| predator recovery, Fig. 2A | **~5 000 → >20 000 cells per reactor in 10 h** | p.3 |
| predator decline begins | **~35 h** | p.4 |
| prey recovery after that | **~10 h later** | p.4 |
| prey extinction without IPTG | after **~50 h** | p.4 |
| IPTG threshold for oscillation | **≥ 5 µM** | p.4, caption p.4 |
| Fig. 2B dilution rate | **0.1125 h⁻¹** throughout | caption p.4 |
| trough below detection, Fig. 2B row 1 cols 1–2 | from **~10 h to ~80 h** | p.4 |

**Fig. 2B panel grid, read off the rendered page (p.2 of §0's caution
applies).** Twelve reactors, 4 columns × 3 rows, each 0–200 h:

| row | IPTG per panel (µM) | y-axis, cells ×10³ |
|---|---|---|
| 1 | **1000, 250, 250, 50** | 0–80 |
| 2 | **5, 5, 5, 10** | 0–100 |
| 3 | **0, 0, 0, 0** | 0–60 |

Blue = predator, red = prey (labeled in row 1, col 1). In all four row-3
(IPTG = 0) panels the **prey crashes toward zero and the predator persists** —
the washout the text describes.

**Fig. 2C, digitized.** Bifurcation diagram, predator cells (×10³) vs IPTG
(µM), log *x*. Calibration: the six major *x* ticks were located by their tick
length and read against the **printed labels 0.1, 1, 10, 100, 1000**
(114.1 px/decade, 1 at x = 716 px at 200 dpi); the *y* scale from the printed
0/10/20/30 ticks (6.567 px per 10³ cells).

| quantity | digitized value | kind |
|---|---|---|
| **Hopf point** | **IPTG ≈ 1.9 µM**, predator ≈ **6.4 ×10³** | MODELLED (their model), COMPUTED (our digitization) |
| stable predator SS at low IPTG | ≈ **23.3 ×10³** | same |
| limit-cycle **maximum** at IPTG ≈ 308 µM | ≈ **31.4 ×10³** | same |
| **unstable** steady state (dashed) at the same IPTG | ≈ **4.9 ×10³** | same |
| limit-cycle **minimum** | ≈ **0** | same |

The model's Hopf at ~1.9 µM and the experiment's "oscillation at ≥5 µM" are
consistent in direction and within a factor of ~3 in value. That is the
honest statement; the paper only says "qualitatively consistent" (p.4).

**Fig. 2C inset** (period of oscillations vs IPTG): rises from the
bifurcation and **saturates at ≈ 235–240 h above about 30 µM**. MODELLED,
digitized against the printed 80/120/160/200/240 ticks. **The inset's x-axis
is printed as "IPTG (M)"; the units are µM** — a figure typo. Do not
reproduce it.

**Where the word "Hopf" is and is not. CORRECTED 8 November 2026 — the
earlier finding here was wrong.** This section previously said, on the
strength of a 7 November rendering of p.4 at **200 dpi**, that the word was
**not** printed on Fig. 2C and that the panel marked the branch point with an
"unlabelled green dot". **Re-rendered at 400 dpi and at 2× magnification on 8
November, the word `Hopf` is plainly set in bold immediately below-left of the
green dot, inside the panel, in the paper's own typeface.** It was never
absent; 200 dpi could not resolve it. `decks/paper_figures.yaml` had it right
all along ("with the Hopf point marked") and the two files were never
reconciled.

So: the word **is** printed on **Fig. 2C**, beside the green branch-point dot.
It is **not** in the Fig. 2 caption, which reads only "(C) Bifurcation diagram
of the predator density versus IPTG level. The inset shows the oscillation
period as a function of IPTG." The word also appears four times in text:
**Box 1B's caption** ("A line connecting Hopf bifurcation points demarcates
three regions"), twice in the Results ("region bound by the loci of Hopf
bifurcation points"; "Increasing IPTG beyond a critical level enables crossing
of a Hopf bifurcation point and elicits oscillatory dynamics"), once more in
the Results ("These results suggest the crossing of a Hopf bifurcation point
using the IPTG level as the control parameter"), and in a reference title.
QUOTED.

**A slide may say that Fig. 2C labels the branch point Hopf — it does.** What a
slide may *not* say is that the *caption* uses the word, or that the panel
leaves the dot unlabelled.

**Why this is recorded at length.** A wrong finding in this file is worse than
a wrong slide, because every downstream artefact trusts it without re-checking.
This one propagated into `DESIGN.md` and onto two slides, one of which asserted
"unlabelled green dot" beside a projected figure with the word in it. It is
also exactly the failure `deck-bar.md` §D5c's 400 dpi crop method exists to
catch, committed in the file that records the method. **Resolution is part of a
finding: any claim that something is absent from a panel is provisional until
it has been checked at 400 dpi or better, and must say the resolution it was
checked at.** Noted because `pdftotext` cannot see inside these panels — §0's
caution — so a text search finding "Hopf" four times says nothing about what
is printed in the figure.

### 3.4 Figure 3 — dilution rate as the control parameter

All Fig. 3 experiments at **IPTG = 50 µM** (caption, p.5). MEASURED.

| panel | strain pair | *D* schedule (h⁻¹) | what happened | kind |
|---|---|---|---|---|
| **3A** | predator **MG1655** / prey **Top10F′** | **0.11** then **0.20** at ~230 h, to 510 h | coexistence, then damped oscillation of period **~50 h** | MEASURED |
| **3B** | predator **Top10F′** / prey **Top10F′** | **0.15**, then **0.23** at ~150 h, then **0.31** at ~250 h | coexistence, then damped oscillation of period **~30 h**, then **predator washout** | MEASURED |

Read off the rendered panels (y = cells ×10³, printed ticks 0/20/40/60/80;
x = Hours): 3A prey peaks ≈ **80 ×10³** at ~30 h and the predator reaches
≈ **22 ×10³** by the *D* switch; after the switch the predator spikes to
≈ **60 ×10³** while the prey falls to ≈ 0. 3B prey peaks ≈ **72 ×10³** at
~35 h and the predator reaches ≈ **75 ×10³** at ~75 h. COMPUTED (digitized
against printed ticks); treat as one significant figure.

**Fig. 3C, the model, digitized against printed ticks.** Main panel: predator
cells (×10³, ticks 0/20/40/60) vs *D* (h⁻¹, ticks 0.00–0.30 by 0.05).

| quantity | value | kind |
|---|---|---|
| predator SS at *D* = 0 | ≈ **17 ×10³** | MODELLED |
| oscillatory branch begins | **D ≈ 0.035–0.04 h⁻¹** | MODELLED |
| limit-cycle maximum, at its peak | ≈ **64 ×10³** at *D* ≈ 0.04 | MODELLED |
| limit-cycle lower envelope | ≈ **0** throughout | MODELLED |
| **predator washout above** | **D ≈ 0.18 h⁻¹** | MODELLED |

**Fig. 3C inset** (period vs *D*, printed ticks 50–250 h and 0.06–0.18 h⁻¹):
maximum period ≈ **212 h at D ≈ 0.063**, falling to ≈ **73 h at D ≈ 0.168**.
MODELLED.

**Fig. 3C bottom row**, three simulated traces: *D* = **0.1 h⁻¹** sustained
spikes with inter-peak spacing ≈ **175 h** (consistent with the inset);
*D* = **0.17 h⁻¹** damped, settling to ≈ **2.8 ×10³**; *D* = **0.3 h⁻¹**
washout within ~10 h. MODELLED.

**A caption defect.** The Fig. 3 caption calls panel C a "Bifurcation diagram
of **oscillatory period** versus *D*", but the main panel's printed *y*-axis
is **Predator cells (×10³)**; only the inset is period. INFERRED BY US.

### 3.5 Numbers that exist only as prose

- "**one of the most complicated synthetic circuits reported to date**" (p.3).
  QUOTED, no metric attached.
- Macroscopic tube cultures "hinted at oscillatory dynamics (data not shown)"
  (p.3). **Data not shown** — do not teach it as a result.
- Fluctuations of prey density around zero in Fig. 2B were "numerical
  artifacts of imaging processing" (p.4). MEASURED artifact, acknowledged.
- The species-counting method is **one-color**: only one species carries
  GFPuv, and the other is obtained by subtraction, so a dim fluorescent cell
  "gets counted as non-fluorescent species cells" (p.6). **This is a
  systematic, direction-known bias** — it transfers predator counts into the
  prey channel. The authors propose two markers as the fix (p.6). MEASURED
  limitation.

---

## 4 · BAL — the model, as far as the paper we hold states it

**The main text contains no model equations.** It names
"equations **S14–S17**" (Box 1 caption, p.2) and "Supplementary information and
**Figure S5**" (p.2). The supplement is **not in `private/readings/`**, so the
equations cannot be transcribed from what this repo holds.

Symbols the main text does print:

| symbol | meaning | where |
|---|---|---|
| **d<sub>c1</sub>** | CcdB killing rate constant, predator | p.2, Box 1 caption |
| **d<sub>c2</sub>** | killing rate constant, prey | Box 1 caption, p.2 |
| **d<sub>c</sub>** | the common value when d<sub>c1</sub> = d<sub>c2</sub> | Box 1 caption, p.2 |
| **k<sub>c1</sub>, k<sub>c2</sub>, k<sub>c</sub>** | growth rate constants, same convention | Box 1 caption, p.2 |
| **D** | microchemostat dilution rate, h⁻¹ | pp.4–5 |

The quantities the model is said to depend on are "rates of cell growth, cell
death controlled by AHL, as well as production and degradation of AHL" (p.2).
QUOTED. **No AHL production rate, degradation rate, threshold or diffusion
coefficient appears anywhere in BAL.** Verified by searching the extracted
text for `diffus`, `cm2`, `mm2` — zero hits.

### 4.1 BioModels BIOMD0000000296

**BAL never mentions BioModels.** Searching the extracted text for
`BioModels` and `BIOMD` returns zero hits across all 8 pages. The accession
comes from `readings.yaml` (s24 `focus`) and `private/log/week13-handoff.md`
§3, which say the model is there "so the session can hand students a model to
run rather than retype". Per the brief, the entry was **not downloaded**.

`[unverified]` — what the entry contains is not established by anything in
this repo or in the paper. What would settle it: open the BioModels page for
BIOMD0000000296 and check (a) that it is curated from
*Mol Syst Biol* 4:187, (b) which figure it reproduces, (c) whether its
parameter names match d<sub>c1</sub>/k<sub>c1</sub>/D. **Do not put
"BioModels has the model" on a slide until someone has done that.**

---

## 5 · BASU — the constructs, gene by gene

From Methods *Plasmids* (PDF p.4 = journal p.1133) and the plasmid maps in
Fig. 1b–d (PDF p.2 = p.1131, rendered).

### 5.1 Sender — `pSND`

| element | promoter | note |
|---|---|---|
| `luxI` | **P**<sub>LTet-O1</sub> | ColE1 origin, Cam<sup>R</sup>, T0/T1 terminators (Fig. 1b) |

LuxI catalyses AHL synthesis; AHL "diffuses through the cell membrane and
forms a chemical gradient around the senders" (p.1130). QUOTED mechanism.

### 5.2 Receiver — two plasmids

**High-detect plasmid `pHD{x}`** (ColE1, Cam<sup>R</sup>; Fig. 1c):

| gene | promoter |
|---|---|
| `luxR` | **P**<sub>lux(L)</sub> — native RBS, not RBSII |
| `lacI`<sub>M1</sub> | **P**<sub>lux(R)</sub> |
| `gfp` | **P**<sub>lac</sub> |

**Low-detect plasmid `pLD`** (p15A, Kan<sup>R</sup>; Fig. 1d):

| gene | promoter |
|---|---|
| `cI` (destabilized λ repressor) | **P**<sub>lux(R)</sub> |
| `lacI` (wild type) | **λP**<sub>(R-O12)</sub> |

Other construction facts (p.1133, MEASURED/QUOTED):

- `lacI`<sub>M1</sub> is **codon-modified**, explicitly "to reduce the
  likelihood of recombination with the wild-type `lacI`" on pLD. *(Session
  23's repeat-recombination failure mode, pre-empted by design, in 2005.)*
- **pHD1** = pHD2 with the hypersensitive LuxR variant **LuxR-G2F**.
- **pHD3** = a variant of **pHD1** with an **AT → TA mutation at ColE1 *ori*
  positions 222–223** that "approximately halves the plasmid copy number
  (data not shown)". **Data not shown** — the halving is asserted.
- **pHD2-Red** = pHD2 with GFP replaced by **DsRed-Express**.
- All proteins except LuxR carry the strong synthetic RBS **RBSII**.
- **CI and GFP carry an 11-amino-acid ssrA LVA tag**; LacI does not.

> **Note the pHD3 lineage.** The Results text says HD3 "express LuxR from a
> reduced-copy-number plasmid" and Fig. 2 caption calls HD3 "a
> reduced-copy-number plasmid", which reads as *wild-type LuxR at half copy*.
> The Methods say pHD3 derives from **pHD1**, i.e. it carries the
> **hypersensitive LuxR-G2F** at half copy. The Methods are specific and the
> Results are loose. INFERRED BY US — use the Methods.

### 5.3 Why this is a band-detect and not a monotone response

The logic, printed as a truth table in **Fig. 1a, top left** (rendered):

| AHL | CI | LacI<sub>M1</sub> | LacI | GFP |
|---|---|---|---|---|
| ++ | ++ | ++ | − | **−** |
| + | + | + | − | **+** |
| − | − | − | ++ | **−** |

- **Low AHL (far from senders) — the low-threshold branch.** No LuxR·AHL, so
  no CI; without CI, λP<sub>(R-O12)</sub> runs and **wild-type LacI is high**,
  which represses P<sub>lac</sub>. **GFP off.**
- **Intermediate AHL — the window.** LuxR·AHL turns on P<sub>lux(R)</sub>,
  making CI *and* LacI<sub>M1</sub>. **CI shuts off wild-type LacI while
  LacI<sub>M1</sub> is still below the level needed to repress GFP.**
  **GFP on.**
- **High AHL (near the senders) — the high-threshold branch.**
  LacI<sub>M1</sub> is now high enough to repress P<sub>lac</sub>.
  **GFP off.**

The authors' stated reason the window exists: "the repression efficiency of CI
is significantly higher than that of LacI<sub>M1</sub>" (p.1130). QUOTED.

**Which component sets which threshold** (p.1130, QUOTED):
the **high-detect component determines the AHL threshold above which GFP is
muted**; the **low-detect component determines the lowest AHL that elicits a
GFP response**. So *high-detect* = the **upper** edge of the band and
*low-detect* = the **lower** edge -- which is what the names suggest, not the
opposite. CORRECTED 7 Nov 2026 against p.1130 and Fig. 2b: an earlier version of
this file said the naming was backwards and it is not. The real surprise is that
a high-detect strain ON ITS OWN is an inverter -- Fig. 2b shows the three HD
strains inversely correlated with AHL. The superseded sentence read: "the
naming is the opposite way round from
what the words suggest; it has misled readers before.

**The inverter chain, written out.** AHL → (LuxR·AHL) ⊣⊣ GFP by two
independent routes of opposite parity:
`AHL → CI ⊣ LacI ⊣ GFP` (double inversion, so AHL **turns GFP on**), and
`AHL → LacI_M1 ⊣ GFP` (single inversion, so AHL **turns GFP off**). The
on-route is **faster/stronger at low AHL**, the off-route **dominates at high
AHL**; the band is the gap between the two thresholds. The paper calls the
same object "a feed-forward loop that begins with LuxR and culminates in GFP"
(p.1130) and credits the combination with "the desired non-monotonic response
to AHL dosages" (p.1130).

**In the model, the asymmetry lives in two numbers, not in two proteins** —
see §7.2. β<sub>C</sub> = 0.008 µM against β<sub>L</sub> = 0.8 µM, a factor of
**100**.

---

## 6 · BASU — every stated experimental number

| quantity | value | kind | where |
|---|---|---|---|
| strain | *E. coli* **DH5α** (λ⁻, recA1⁻), CGSC **7855** | MEASURED | p.1133 |
| medium | M9 minimal + **0.2 % casamino acids, 200 µM thiamine, 100 µM CaCl₂** | MEASURED | p.1133 |
| antibiotics | **50 µg mL⁻¹ Kan, 25 µg mL⁻¹ Cm** | MEASURED | p.1133 |
| growth temperature | **37 °C** | MEASURED | p.1133 |
| harvest density | **OD₆₀₀ = 0.3** | MEASURED | p.1133 |
| inducer, liquid phase | **3OC6HSL** (Sigma-Aldrich) | MEASURED | p.1133 |
| FACS | Beckman Coulter Altra, **488 nm** excitation, **515–545 nm** emission | MEASURED | p.1133 |
| calibration beads | Spherotech SPHERO Rainbow **RCP-30-5A** | MEASURED | p.1133 |
| data point definition | **median** FACS value | MEASURED | p.1133 |
| plating density | diluted into 2 mL of **0.7 % agarose** to **OD₆₀₀ = 0.15** | MEASURED | p.1133 |
| plate | **M9, 1.5 % agarose** | MEASURED | p.1133 |
| sender concentration | **50-fold** | MEASURED | p.1133 |
| sender volume on the disk | **20 µL** on a Whatman 3 paper disk, plate center | MEASURED | p.1133 |
| objective | **2.5×** brightfield; ORCA-ER, **1344 × 1024** px | MEASURED | p.1133 |
| CFP filters | **436/20** ex, **470/30** em | MEASURED | p.1133 |
| GFP filters | **470/40** ex, **525/50** em | MEASURED | p.1133 |
| DsRed-Express filters | **565/30** ex, **620/60** em | MEASURED | p.1133 |

### 6.1 Ring and timing numbers

| quantity | value | kind | where |
|---|---|---|---|
| time-course duration (BD2) | **36 h** | MEASURED | p.1131 |
| sampling interval | every **90 min** | MEASURED | p.1131 |
| region imaged | **30 mm × 4 mm** rectangle protruding from the sender disk | MEASURED | p.1131 |
| no fluorescence for the first | **15 h** | MEASURED | p.1131 |
| low fluorescence first emerges at | **~10 mm** from the senders | MEASURED | p.1131 |
| fluorescence rises significantly between | **5 and 18 mm** | MEASURED | p.1131 |
| values stabilize after | **~32 h** | MEASURED | p.1131 |
| steady-state maximum at | **10 mm** | MEASURED | p.1131 |
| observable positional shift over 36 h | **none** | MEASURED | p.1131 |
| **BD2-Red ring diameter, experiment 1 (Fig. 3b)** | **30 mm** | MEASURED | p.1130 |
| **BD2-Red ring diameter, experiment 2 (Fig. 3c)** | **22 mm** | MEASURED | p.1130 |
| scale bar, Fig. 3b,c | **5 mm** | MEASURED | Fig. 3 caption, p.1132 |
| incubation for the bullseye | **overnight** | MEASURED | Fig. 3 caption |

**The 30 mm / 22 mm pair is the paper's own reproducibility number.** The same
strain, the same threshold, two experiments, **a 36 % difference in ring
diameter**. (COMPUTED: 30/22 = 1.364.) The authors attribute it to variation
in the AHL gradient from "differences in the growth rates and population
densities of senders and receivers", plus nutrient and agar differences
(p.1130–1131). Note that neither explanation is a circuit parameter.

### 6.2 LacI-decay regimes, stated in the text

| γ<sub>L</sub> range (min⁻¹) | behavior | kind | where |
|---|---|---|---|
| **< 0.02** | no positional shift, but "very slow emergence of fluorescence long after the AHL gradient has stabilized" | MODELLED | pp.1131–1132 |
| **0.02 – 0.04** | ring forms at the final position only, no significant time delay | MODELLED | p.1132 |
| **fast** (toward 1) | fluorescence emerges quickly, far from the steady-state position, then shifts outward | MODELLED | p.1131 |

All three are conclusions about **simulations**, not measurements. In the
experiment, "LacI degradation is due mainly to dilution by cell growth"
(p.1132) — no rate is given.

### 6.3 Figure 2 caption numbers, and what they are NOT

The caption prints two sets of six numbers (p.1131):

- HD1 **2.03/6.58**, HD2 **2.47/4.14**, HD3 **2.78/5.12**
- BD1 **0.48/4.43**, BD2 **7.36/18.55**, BD3 **1.1/8.23**

each introduced as "the 95% confidence intervals have minimum/maximum values
of …". **The caption never says which fitted parameter these bound.** The
fitted forms are given in Methods (p.1133): a sigmoid
y = y₀ + α/(1 + (AHL/β)ⁿ) for Fig. 2c and a bell-shaped
y = δ + (α₁−δ)/(1+(AHL/β₁)^n₁) + (α₂−δ)/(1+(AHL/β₂)^−2n₂) for Fig. 2d, and the
magnitudes are plausible for a Hill exponent rather than a concentration.

**`[unverified]` — do not use these as AHL thresholds.** What would settle it:
the Supplementary Information, which this repo does not hold. Until then they
are six numbers with no named referent, and the safest treatment is to leave
them out of any assessed item.

Two further caption slips in the same caption: it says the simulations are
panel **a** and the band-detect simulations panel **c**, then says the CIs are
"for the curve fits" of **2c** in Methods while 2c is the *simulation*. The
Methods sentence "Figure 2c curves were fitted to a sigmoidal function"
almost certainly means **Fig. 2b**, since 2b is the measured high-detect
dosage response and 2c is simulated. INFERRED BY US; flag, do not silently
correct.

---

## 7 · BASU — the model, exactly as printed (p.1134)

### 7.1 The equations

Five species: **G** = GFP, **L** = LacI, **C** = CI, **R** = LuxR/AHL complex,
**A** = AHL, plus a **fixed** LuxR concentration.

```
dG/dt = α_G / (1 + (L/β_L)^η1)  −  γ_G G                                  (1)

dL/dt = α_L1 / (1 + (C/β_C)^η2)  +  α_L2 R^η3 / (θ_R^η3 + R^η3)  −  γ_L L  (2)

dC/dt = α_C R^η3 / (θ_R^η3 + R^η3)  −  γ_C C                              (3)

dR/dt = ρ_R [LuxR]^2 A^2  −  γ_R R                                        (4)

dA_{x,y,z}/dt = ξ ( A_{x−1,y,z} + A_{x+1,y,z} + A_{x,y−1,z}
                  + A_{x,y+1,z} + A_{x,y,z−1} + A_{x,y,z+1}
                  − 6 A_{x,y,z} )  −  γ_A                                 (5)
```

Transcribed from the rendered page, not from `pdftotext` (which mis-reads
θ<sub>R</sub> as ν<sub>R</sub> and ξ as υ).

**Two defects in equation (5), both printed.**

1. **The decay term is `− γ_A`, with no `A`.** As printed it is a constant
   removal rate, not first-order decay. It must be **− γ_A A**. A student who
   types equation (5) literally gets a different model. DERIVED/INFERRED BY US
   — the parameter is named "AHL decay (γ_A, 0.01 min⁻¹)", a first-order rate.
2. **No grid spacing.** The bracket is a discrete Laplacian
   Σ(neighbors) − 6A, which is dimensionless-in-A, so ξ must have units of
   **min⁻¹** for the equation to balance. ξ is printed with units
   **mm² min⁻¹**. The only self-consistent reading is **ξ = D/Δx²** with a
   lattice spacing Δx the paper never states. DERIVED. This is the single
   reason T66 cannot take ξ as a diffusion coefficient — see §13.

**Where the model simplifies the biology.** There are only five species, so
**LacI and LacI<sub>M1</sub> are lumped into one variable `L`** with one
repression coefficient β<sub>L</sub>. The two production terms in eq. (2) are
the wild-type route (CI-repressible) and the LacI<sub>M1</sub> route
(LuxR·AHL-activated). So the model **cannot express** the prose mechanism
"CI represses better than LacI<sub>M1</sub>" as a property of two repressors;
it expresses it as β<sub>C</sub> ≪ β<sub>L</sub>. INFERRED BY US, and worth
saying out loud rather than papering over.

**Equation (4) is quadratic in both [LuxR] and A**, which the paper justifies:
LuxR and AHL bind, then the complex dimerizes, "hence the quadratic terms in
equation (4)" (p.1134, citing Choi & Greenberg). QUOTED. Note that η3 = 1,
so the *promoter* response to R is non-cooperative; the cooperativity is all
in the complex formation.

### 7.2 The BD2 parameter set — printed, complete, and runnable

"The following parameters approximate the behaviour of **BD2**" (p.1134).
MODELLED (a chosen parameter set, not a fit to data reported here).

| symbol | value | what it is |
|---|---|---|
| α_G | **2 µM min⁻¹** | GFP synthesis |
| α_L1 | **1 µM min⁻¹** | LacI synthesis, CI-repressible route |
| α_L2 | **1 µM min⁻¹** | LacI synthesis, LuxR·AHL-activated route |
| α_C | **1 µM min⁻¹** | CI synthesis |
| **β_L** | **0.8 µM** | repression coefficient, LacI on GFP |
| **β_C** | **0.008 µM** | repression coefficient, CI on LacI |
| γ_C, γ_G | **0.0692 min⁻¹** | protein decay (LVA-tagged) |
| γ_L, γ_R | **0.0231 min⁻¹** | protein decay (untagged) |
| θ_R | **0.01 µM** | LuxR/AHL activation coefficient |
| η1, η2, η3 | **2, 2, 1** | cooperativity / multimerization |
| ρ_R | **0.5 µM⁻³ min⁻¹** | LuxR/AHL dimerization |
| **ξ** | **0.001 mm² min⁻¹** | "AHL intercellular diffusion" |
| γ_A | **0.01 min⁻¹** | AHL decay |
| [LuxR] | **0.5 µM** | fixed |

COMPUTED half-lives from those decay constants: ln2/0.0692 = **10.02 min**
(CI and GFP — the ssrA-LVA tag), ln2/0.0231 = **30.01 min** (LacI and R),
ln2/0.01 = **69.3 min** (AHL). The first two are 10 min and 30 min to three
figures, so they were chosen as round half-lives, not fitted.

**β_C/β_L = 0.008/0.8 = 1/100.** COMPUTED. This is the quantitative form of
"CI represses better than LacI<sub>M1</sub>", and it is the one number the
whole band-detect rests on.

### 7.3 How the variants were simulated

- **HD1 and BD1:** ρ_R increased **tenfold** from the table above (p.1134).
- **HD3 and BD3:** α_G, α_L2 and [LuxR] **halved** (p.1134).
- **Liquid-phase simulations omit equation (5)** entirely (p.1134).
- **High-detect-only liquid simulations also drop equation (3) and the CI
  repression term in equation (2)** (p.1134).

All MODELLED. Note that the *only* change between BD2 and BD1 in the model is
the dimerization constant ρ_R — the hypersensitive LuxR-G2F mutant is
represented by a 10× ρ_R, nothing else.

### 7.4 The two kinetic parameter sets behind Fig. 4b and 4c

Printed as `4b/4c` pairs (p.1134), MODELLED:

| symbol | Fig. 4b | Fig. 4c |
|---|---|---|
| β_L | **543 nM** | **230 nM** |
| β_C | **19 nM** | **69 nM** |
| γ_C | **0.116 min⁻¹** | **0.496 min⁻¹** |
| γ_G | **0.404 min⁻¹** | **0.366 min⁻¹** |
| **γ_L** | **0.018 min⁻¹** | **0.902 min⁻¹** |
| γ_R | **0.036 min⁻¹** | **0.050 min⁻¹** |
| θ_R | **0.249 µM** | **0.063 µM** |
| ρ_R | **2.102 µM⁻³ min⁻¹** | **3.374 µM⁻³ min⁻¹** |

**Eight parameters differ, not one.** The text names only the γ_L difference —
"an important difference between these two kinetic parameter sets is a shorter
half-life for LacI in Fig. 4b" (p.1132). COMPUTED: γ_L differs by a factor of
**50.1**; β_L/β_C is **28.6** in 4b and **3.3** in 4c, against **100** in the
BD2 set. INFERRED BY US: **4b vs 4c is not a one-parameter comparison**, and
presenting it as "stable LacI vs fast LacI" alone overstates the control.

**Note the direction of the sentence.** The text says 4b has the **shorter**
LacI half-life, but γ_L(4b) = 0.018 min⁻¹ is the **slower** decay — i.e. the
**longer** half-life — and the very next sentence postulates "the relatively
**long** half-life of LacI … accounts for the similarity" between Fig. 4a and
Fig. 4b (p.1132). The parameters and the second sentence agree; the first
sentence is backwards. INFERRED BY US, with the arithmetic:
ln2/0.018 = **38.5 min** (4b) vs ln2/0.902 = **0.77 min** (4c).

### 7.5 The statistical procedure (p.1134)

| step | value | kind |
|---|---|---|
| random parameter sets generated | **2,000** | MODELLED |
| drawn uniformly around the BD2 values | — | MODELLED |
| fraction with band-detect behavior (gain > 3, above a threshold) | **about 30 %** | MODELLED |
| sets carried forward | the **first 100** | MODELLED |
| sender AHL synthesis rate re-tuned in every set so that the ring sits at | **7 mm** | MODELLED |
| "shift begin" | first spatiotemporal coordinate in the ring middle, closest to origin, with fluorescence **> 50 %** of maximum overall steady-state fluorescence | MODELLED |
| "shift end" | same criteria, at the final steady-state ring position | MODELLED |
| positional shift | position<sub>steady</sub> − position<sub>start</sub> | MODELLED |
| response times fitted with | **power-series** equations | MODELLED |
| positional shift fitted with | a **sigmoidal** fit | MODELLED |
| software | GraphPad PRISM | — |

---

## 8 · BASU — the dose–response panels, digitized

Calibration for every number in this section: major *x* ticks located by tick
length and matched to the **printed decade labels 10⁻⁴ … 10¹**. Panel a:
10⁻⁴ at x = 915 px, **52.1 px/decade**. Panel c: 10⁻⁴ at x = 1253.5 px,
**48.4 px/decade**; *y* from printed 0/10/20/30 ticks. Panel d: decades fitted
to the five located major ticks, 10⁻⁴ at x = 1244.6 px, **54.03 px/decade**;
*y* from printed 0/25/50/75/100 ticks. All at 200 dpi.

### 8.1 Fig. 2a — high-detect, SIMULATED (MODELLED + COMPUTED digitization)

| strain | plateau GFP (µM) | half-max AHL (µM) |
|---|---|---|
| HD1 (blue, hypersensitive LuxR) | ≈ 28.7 | ≈ **2 × 10⁻²** |
| HD2 (red, wild-type LuxR) | ≈ 28.7 | ≈ **7 × 10⁻²** |
| HD3 (black, half copy) | ≈ **14.5** | ≈ **1.3 × 10⁻¹** |

HD3's plateau is **half** of HD1/HD2's — exactly what halving α_G, α_L2 and
[LuxR] produces (§7.3). Monotone **decreasing** in AHL: the high-detect
component is an inverter.

### 8.2 Fig. 2b — high-detect, MEASURED (digitized)

| strain | high plateau (a.u.) | midpoint AHL (µM) | floor (a.u.) |
|---|---|---|---|
| HD1 | ≈ 95 | ≈ **1 × 10⁻³** | ≈ 3 |
| HD2 | ≈ 91 | ≈ **2 × 10⁻²** | ≈ 11 |
| HD3 | ≈ 76 | ≈ **2 × 10⁻¹** | ≈ 10 |

**Model and data agree on the ordering and disagree on the spacing.**
COMPUTED: in the simulation HD1 and HD2 are **~3.5×** apart; in the data they
are **~20×** apart. The paper says the experimental responses were "in
agreement with model predictions (Fig. 2a)" (p.1130). That claim is about
*shape and rank*, and it should be taught that way.

### 8.3 Fig. 2c — band-detect, SIMULATED (MODELLED + COMPUTED digitization)

| strain | peak GFP (µM) | peak AHL (µM) |
|---|---|---|
| BD1 | **19.6** | **8.5 × 10⁻³** |
| BD2 | **19.6** | **2.7 × 10⁻²** |
| BD3 | **12.2** | **6.0 × 10⁻²** |

Band positions span **0.85 decades** across the three variants. COMPUTED:
log₁₀(0.060/0.0085) = 0.85.

> **The AHL positions in this table are wrong by a constant factor of about
> 6.8, and the evidence says the error is the digitization's, not the model's.**
> Found 7 November 2026 by running BASU's printed BD2 set through
> `posb.band_detect_response`, which is §7.1's equations (1)–(4) in the
> liquid-phase limit of §7.3 — the same limit this panel is simulated in.
>
> | variant | peak GFP, computed | peak GFP, this table | peak AHL, computed | peak AHL, this table | AHL ratio |
> |---|---|---|---|---|---|
> | BD1 | 19.607 µM | 19.6 | 1.256 × 10⁻³ µM | 8.5 × 10⁻³ | **6.77×** |
> | BD2 | 19.607 µM | 19.6 | 3.973 × 10⁻³ µM | 2.7 × 10⁻² | **6.80×** |
> | BD3 | 12.161 µM | 12.2 | 8.934 × 10⁻³ µM | 6.0 × 10⁻² | **6.72×** |
>
> **The peak heights agree to about one part in 2,500**, and the *spacings*
> agree too: computed BD2/BD1 = 3.1623 against 3.176 here, BD3/BD2 = 2.2486
> against 2.222, and the total spread 0.852 decades against 0.849. A model that
> reproduces three peak heights and two spacings to three digits and misses
> every absolute position by the same 6.8× is not the thing that is wrong. A
> uniform 0.83-decade shift (log₁₀ 6.78 = 0.831) at this panel's stated
> 48.4 px/decade is **40 px**, which is the size of a mis-located 10⁻⁴ tick.
> DERIVED.
>
> **Consequences, and one of them is unresolved.**
> 1. **Use the computed values, not these, for anything a student sees.** They
>    come from printed parameters in a limit the paper itself defines, and
>    `tests/test_communities.py` pins them two-sided.
> 2. **§8.4's panel-d positions were calibrated the same way and are now also
>    in doubt**, and with them §8.4's statement that the measured band sits
>    "2–3× above" the simulated one — which compared one digitization against
>    another. Against the computed peak, §8.4's fitted BD2 peak of ~4 × 10⁻²
>    µM is a factor of about **10** away, not 2–3.
> 3. **What survives either way:** the ordering of the three variants, and the
>    spread of about a decade across them, in both the simulation and the data.
>    Those are what §15.9's "ordinal, not quantitative" reading rests on and
>    they are untouched.
>
> `[unverified]` — settling it needs panels c and d re-digitized with the
> decade ticks re-located. **Until then no absolute AHL position from §8 goes
> on a slide**, which §8's own closing note already required for a different
> reason.

### 8.4 Fig. 2d — band-detect, MEASURED (digitized)

| strain | topmost point (a.u.) | AHL at that point (µM) |
|---|---|---|
| BD1 | ≈ **46** | ≈ **2 × 10⁻²** |
| BD2 | ≈ **98** (a raw marker; the fitted curve peaks near **87**) | ≈ **9 × 10⁻²** raw; fitted peak nearer **4 × 10⁻²** |
| BD3 | ≈ **83** | ≈ **2 × 10⁻¹** |

COMPUTED, one significant figure, because the mask used to find the envelope
cannot separate a raw marker from the fitted line. Band positions span
**~1 decade** in the data against 0.85 in the simulation — the same ordering
and roughly the same spread, shifted up by a factor of ~2–3 in absolute AHL.

> **No numeric AHL threshold is printed anywhere in BASU.** Every value in
> §8 is ours. An autograded T65 built on these would be grading a
> digitization. Build T65 on §7 instead.

---

## 9 · BASU — the patterns, and which protein reports which band

### 9.1 Fig. 3 — the bullseyes (p.1132, rendered)

| panel | lawn | senders | result |
|---|---|---|---|
| 3a | — | — | photograph of the dish with the sender disk in the middle |
| **3b** | **BD2-Red + BD3** mixed | **CFP**-expressing, center | **BD3 green ring INNER, BD2-Red red ring OUTER** |
| **3c** | **BD1 + BD2-Red** mixed | center | **BD2-Red red ring INNER, BD1 green ring OUTER** |

Reporters: **GFP** reports BD1, BD2 and BD3; **DsRed-Express** reports
BD2-Red (a BD2 variant with DsRed in place of GFP) in both Fig. 3 panels.
Senders in Fig. 3 express **CFP** (caption, p.1132); senders in **Fig. 5**
express **DsRed-Express** (caption, p.1133). MEASURED.

**The geometry inverts the sensitivity order, and that is the lesson.** AHL is
highest at the sender. The **most sensitive** variant (BD1, hypersensitive
LuxR, lowest band) therefore lights up **farthest** from the sender; the
**least sensitive** (BD3) lights up **closest**. Both panels are consistent
with that and with §8.3. DERIVED from the paper's own ordering.

### 9.2 Fig. 5 — the other patterns (p.1133, rendered)

| panel | what | senders |
|---|---|---|
| **5a** | **ellipse** | **simulation**, two senders |
| **5b** | **ellipse** | experiment, **two** sender disks |
| **5c** | **heart** | experiment, **three** sender disks |
| **5d** | **clover** | experiment, **four** sender disks |

The caption says the patterns are formed "based on the placement **and initial
concentrations** of sender cells" (p.1133) — so the knobs are **number,
placement and density**, not placement alone. The text lists them: "the
number of, distance between, and density of sender cells" (p.1133). QUOTED.

The caption's own opening, QUOTED in full because the panel labels matter:
"Formation of various patterns. **a**, Simulation of band-detect behaviour on
solid media with two senders that results in the formation of an ellipse.
**b–d**, Experimental results showing various GFP patterns formed based on the
placement and initial concentrations of sender cells expressing DsRed-Express:
**b**, ellipse, two sender disks; **c**, heart, three sender disks; and **d**,
clover, four sender disks." So **the paper itself labels 5a a simulation**, and
the figure is four panels with three results.

**Which receiver strain the Fig. 5 lawn is, the caption does not say.** The
patterns are GFP, so the lawn is a GFP band-detect variant rather than BD2-Red,
but the panel is not attributed to BD1, BD2 or BD3 anywhere in the caption or
the text. `[unverified]` — Supplementary Table S1 or the SI would settle it. A
slide should say "a lawn of band-detect receivers" rather than name a strain.
ADDED 7 November 2026.

**The paper has a heart as well as the ellipse and the clover.** Any list that
gives only bullseye/ellipse/clover is missing one of the four. In Fig. 5b the
two sender disks are visibly different sizes; in 5d the four sender disks are
large and the green is the four-lobed region between them.

---

## 10 · BASU — the kinetic analysis, and what kind it is

This is the part most likely to be mis-tagged, so it is set out in full.

**The claim, as the abstract makes it** (p.1130): "Experimental and
theoretical analyses reveal which kinetic parameters most significantly affect
ring development over time."

**What the analysis actually is.** 100 spatiotemporal **simulations**, drawn
from 2,000 random parameter sets around the BD2 values (§7.5). The regression
correlates each **model rate constant** against **simulated** shift times and
shift distances.

| correlation | R² | P | kind |
|---|---|---|---|
| **γ_L (LacI decay) vs shift begin** | **0.91** | < 0.0001 | **MODELLED** |
| **γ_L vs shift end** | **0.71** | < 0.0001 | **MODELLED** |
| **γ_L vs positional shift** | **0.76** | < 0.0001 | **MODELLED** |
| CI repression efficiency vs positional shift | **0.05** | **0.0191** | **MODELLED** |
| every other rate constant in eqs. (1)–(4) | **< 0.001** | **> 0.75** | **MODELLED** |

**These are MODELLED, not MEASURED, and not even partly measured.** The
regression has no experimental input: the points are simulations and the
parameters are the simulations' own inputs. The "experimental" half of the
abstract's sentence contributes the single BD2 time course of Fig. 4a, which
is compared to Fig. 4b **by eye** ("accounts for the similarity", p.1132).
The experiment never measured γ_L — the paper says LacI loss is "due mainly to
dilution by cell growth" and gives no rate.

**The 0.05 is the one to be careful with.** R² = 0.05 with P = 0.0191 means
**5 % of the variance** in positional shift tracks CI repression efficiency,
over 100 points, and the P value only says that 5 % is unlikely to be exactly
zero. The paper calls it "a weak correlation" (p.1133), which is right. It is
not a design lever.

### 10.1 Fig. 4, digitized (printed ticks only)

**4a — EXPERIMENT.** Heat map, *x* = Distance (mm) with printed ticks
0/5/10/15/20/25, *y* = Time (h) with printed ticks 7.5/15.0/22.5/30.0, color
bar **×10⁴**, 0.5 to 4.0. Uniform dark below ~15 h; a band centered near
**10 mm** brightening from ~22 h.

**4b, 4c — SIMULATIONS.** *x* = Distance (mm), ticks 0/2/4/6/8/10; *y* = Time
(h), 0–40; color bar log, 10⁻⁰·² to 10⁻⁰·⁸.

| | 4b (γ_L = 0.018) | 4c (γ_L = 0.902) |
|---|---|---|
| fluorescence first appears | ~**15 h**, at ~**5 mm** | ~**2–3 h**, at ~**0.5–2 mm** |
| black shift line runs | ~6.3 → ~6.4 mm, t ≈ 28 → 32 h | ~2.2 → ~6.4 mm, t ≈ 3.5 → 22 h |
| positional shift | ≈ **0.1 mm** | ≈ **4.2 mm** |

COMPUTED (digitized against printed ticks), one significant figure.

**The scale mismatch between 4a and 4b/4c is unreconciled in the paper.** The
experiment's axis runs to **28 mm** with the ring at **10 mm**; the
simulations' axis runs to **11 mm** with the ring at **6.5 mm**, and the
Methods tuned every simulation to put the ring at **7 mm**. The paper compares
them and never says the distances differ by ~1.4×. INFERRED BY US.

**4d, 4e.** *x* = **LacI decay, γ_L (min⁻¹)**, log, printed ticks 0.01 / 0.1 / 1.
4d *y* printed 0/20/40/60 and 4e *y* printed 0/2/4/6, **both with no axis
title**. From the text's definitions the units are **hours** (4d) and
**millimeters** (4e), but **the units are not printed** — `[unverified]`;
the Supplementary Information or the axis titles in the published HTML would
settle it.

Digitized trend-line values (COMPUTED, one significant figure):

| γ_L (min⁻¹) | shift begin (4d) | shift end (4d) | positional shift (4e) |
|---|---|---|---|
| 0.012 | ~52 | ~30 | ~0.3 |
| 0.03 | ~20 | ~27 | ~0.8 |
| 0.1 | ~11 | ~24 | ~2 |
| 0.9 | ~3 | ~21 | ~5 |

**A warning about the left end of 4d.** At γ_L ≲ 0.02 min⁻¹ the filled
diamonds (shift begin) sit **above** the open triangles (shift end) — which
the definitions forbid, since a shift cannot end before it begins. The two
fitted trend lines converge near ~55 at the far left while the plotted
triangles there are ~30–35. INFERRED BY US: read the left-hand end as scatter,
not as structure, and do not quote a shift-begin value below γ_L = 0.02 as
though it were resolved.

---

## 11 · TSOI — the criterion, and every variable in it

OPTIONAL reading. Everything in §11–§12 is **MODELLED or DERIVED**: the paper
is entirely analysis, with no experiment of its own.

### 11.1 The single-cell (SC) model, dimensionless (p.2527, Eqs. 1–3)

```
dm/dt   = α1 e1 − η (m − m_e) − α2 e2 m          (1)
dm_e/dt = υ η (m − m_e) − δ_me m_e               (2)
dp/dt   = α2 e2 m − p                            (3)
```

### 11.2 The DOL model (p.2527, Eqs. 4–7)

```
dm1/dt  = α1 e1 − η (m1 − m_e)                           (4)
dm_e/dt = υ1 η (m1 − m_e) − υ2 η (m_e − m2) − δ_me m_e   (5)
dm2/dt  = η (m_e − m2) − α2 e2 m2                        (6)
dp/dt   = α2 e2 m2 − p                                   (7)
```

### 11.3 Growth (p.2527–2528, Eqs. 8–10)

```
dυ/dt   = μ υ (1 − υ/ρ) − δ_υ υ                  (8)
dυ1/dt  = μ1 υ1 (1 − υ1/ρ1) − δ_υ1 υ1            (9)
dυ2/dt  = μ2 υ2 (1 − υ2/ρ2) − δ_υ2 υ2           (10)
```

### 11.4 Burden (p.2528, Eqs. 11–13)

```
μ  = μ_max  G  / (1 + (β e1 + γ e2)^n)          (11)
μ1 = μ_max,1 G1 / (1 + (β e1)^n)                (12)
μ2 = μ_max,2 G2 / (1 + (γ e2)^n)                (13)
```

### 11.5 Every parameter, what it means physically, and whether they call it measurable

| symbol | meaning, in the paper's words | where |
|---|---|---|
| **S, M, M_e, P** | substrate; intracellular intermediate; extracellular intermediate; final product | p.2527 |
| **E1, E2** | the two enzymes; E1 makes M from S, E2 makes P from M | p.2527 |
| **e_i** | "the steady-state concentration of E_i per cell" | p.2527 |
| **α_i** | "the production rate of M and P, respectively" | p.2527 |
| **η** | "the transport rate constant of M across the cell membrane" | p.2527 |
| **δ_me** | "the turnover rate constant of M in the extracellular space" | p.2527 |
| **υ, υ1, υ2** | steady-state cell volume (∝ total biomass) of SC, DOL-1, DOL-2 | p.2527 |
| **δ_υ, δ_υi** | "the turnover rate constant of the population" | p.2528 |
| **μ, μ_i** | growth rate constant | p.2528 |
| **μ_max** | maximum growth rate | p.2528 |
| **ρ, ρ_i** | carrying capacity | p.2528 |
| **β** | "the metabolic burden per unit of E1" ("relative burden of E1") | p.2528 |
| **γ** | "the metabolic burden per unit of E2" | p.2528 |
| **n** | the Hill coefficient of the burden function | p.2528 |
| **G, G1, G2** | "additional intermediate growth effects such as toxic byproducts or crucial metabolites"; multipliers of μ_max in [0,1] | p.2528 |
| **ε = δ_me/η** | DOL's transport inefficiency | p.2528 |
| **θ_I** | the inefficiency factor; see §11.7 | p.2528 |
| **τ** | dimensionless time | Eqs. 1–13 |

> **How this course writes the burden, and why.** Tsoi's printed symbols
> above are left exactly as printed: **β** is the burden per unit of E1 and
> **γ** per unit of E2, so their total is **βe₁ + γe₂**. Session 24 cannot
> reuse either letter — **γ** is decay throughout the course, and **β_L** and
> **β_C** are Basu's printed repression thresholds in µM *in the same hour*.
> So the deck writes the burden **B**: **B₁ = βe₁** and **B₂ = γe₂** are the
> two enzymes' burdens, and the single cell carries the total
> **B = B₁ + B₂**. `docs/symbols.md` records the decision.
>
> **`posb.dol_criterion`'s two burden arguments are B₁ and B₂ — PER
> ENZYME.** Passing a pathway total halves what the model sees and can
> reverse `dol_favored`. Move 5's release and debrief quote per-enzyme
> burdens (1.2, 1.3) and per-enzyme borders (1.135146, 1.355143); the
> `s24_dol` figure's axes are the TOTAL B, so its crossing (2.27) is on
> twice that scale. Any number taken from either must say which it is.

**What the paper says is measurable.** It does not use the word. The nearest
statements are that the criterion "can determine which design strategy to use
**given pathway parameters**" (p.2530) and that Eq. 17 shows "the metabolic
burden caused by each enzyme (βe)ⁿ **and host growth parameters** determine if
DOL is favored" (p.2528). The operational reading: the quantities a designer
would have to supply are **βe (burden per enzyme × expression level — our
B₁ and B₂)**,
**μ_max/δ_υ (the host's resilience to burden)**, **n**, and **θ_I**, which
needs **δ_me, η, α₂e₂** and the steady-state volumes. QUOTED plus INFERRED BY
US for the list.

**Standing assumptions, stated** (p.2527): well-mixed (or fast transport),
**negligible intracellular degradation of metabolite**, **excess initial
substrate**, **transport by passive diffusion**, enzymes always at steady
state, constant cell size. Plus, for DOL: "the populations consume different
resources and **do not compete**" (p.2528), each with its own carrying
capacity.

### 11.6 Steady-state product, Eqs. 14 and 15 (p.2528)

```
p_SC  = α1 e1 (δ_me + η υ)  /  ( δ_me + δ_me η/(α2 e2) + η υ )      (14)

p_DOL = α1 e1 η υ1          /  ( δ_me + δ_me η/(α2 e2) + η υ2 )     (15)
```

**As printed, Eq. 14's middle denominator term reads δ_m η/(α₂e₂), with
subscript `m`, not `m_e`.** Eq. 15 and θ_I both print **δ_me**, and the model
defines only δ_me. Read Eq. 14's δ_m as a typo for **δ_me**. INFERRED BY US,
confirmed by rendering the equation at high zoom.

### 11.7 The criterion itself, Eq. 16 (p.2528) — the mathematical condition

DOL is favored when total product yield is higher, i.e. **p_DOL υ₂ > p_SC υ**,
which they rewrite as:

```
        ῡ²_DOL
      ───────────   >   θ_I                                        (16)
        υ² + ε υ
```

with

```
ε     = δ_me / η

        δ_me + δ_me η/(α2 e2) + η υ2
θ_I  = ───────────────────────────────
        δ_me + δ_me η/(α2 e2) + η υ

ῡ_DOL = sqrt( υ1 υ2 )          (geometric mean of the DOL steady-state densities)
```

**Reading of the two sides, in the authors' words** (p.2528): the left-hand
side "represents the net gain in biomass by utilizing DOL"; the right-hand
side "represents the reduced per-cell productivity of DOL". QUOTED.

**The degenerate case, stated:** "If ε = 0 and θ_I = 1, DOL does not reduce
efficiency, and maximizing product yield is the same as maximizing biomass"
(p.2528). QUOTED.

### 11.8 The simplified criterion, Eq. 17 (p.2528)

Under δ_me ≪ η (so ε ≈ 0) **and** e1 ≈ e2, β ≈ γ, μ_max ≈ μ_max,1 ≈ μ_max,2,
δ_υ1 ≈ δ_υ2, ρ1 ≈ ρ2 ≈ ρ/2:

```
                ( μ_max/δ_υ − 1 ) ( 2 sqrt(θ_I) − 1 )
    (β e)^n  >  ─────────────────────────────────────                (17)
                     2^(n+1) sqrt(θ_I) − 1
```

DERIVED (by the authors; the derivation is in SI Appendix §2.3, which this
repo does not hold — `[unverified]` as to its steps, verified as to the
printed form, which was read off the rendered page).

**What Eq. 17 says, term by term** (p.2528, QUOTED and paraphrased):

- Higher **(βe)ⁿ** — more enzyme, or more burden per unit enzyme — **favors
  DOL**.
- Higher **μ_max**, or lower **δ_υ** (population turnover), lets the host
  "support higher burden, **favoring SC**".
- "kinetic parameters do not significantly affect which strategy performs
  better (SI Appendix, Fig. S1)" (p.2528).

The one-line statement the authors give: "DOL is favored when the pathway
burden overcomes both the host's resilience to burden and the inefficiency of
DOL" (p.2528).

**Note ρ1 ≈ ρ2 ≈ ρ/2 among the assumptions.** The two DOL populations split
the SC carrying capacity. The biomass "gain" in Eq. 16 is therefore not a gain
in total carrying capacity — it is a gain in how much of a *halved* capacity
each population can actually occupy once the burden is split. DERIVED.

---

## 12 · TSOI — the quantitative claims about when DOL wins or loses

### 12.1 Fig. 1D, the parameter plane (p.2527, rendered)

Axes as printed: *x* = **Relative burden**, ticks 0/30/60/90/120; *y* =
**Diffusivity (×10⁴)**, ticks 0/2/4/6/8/10. **Neither axis carries units** —
both are dimensionless model quantities (relative burden is βe, diffusivity is
η).

> **"Relative burden is βe" is our inference and the printed numbers do not
> support it.** Added 7 November 2026. Put the border position back through the
> paper's own Eq. 17: for the SC/DOL border to sit at a relative burden of
> **70**, Eq. 17 needs μ_max/δ_υ ≈ **200** if n = 1, ≈ **4 × 10⁴** if n = 2, and
> ≈ **7 × 10⁸** if n = 4. COMPUTED. Nothing in the paper states a host that
> resilient, and n is introduced as an ordinary Hill coefficient. So the axis
> labelled "Relative burden" is **not** the βe that appears in Eq. 17, or the
> figure's n and parameters are not recoverable from the main text. Either way:
> **do not place a βe value computed from Eq. 16 or Eq. 17 on Fig. 1D's axis**,
> and do not read a βe off that axis. `[unverified]` — SI Appendix §3.1.1 would
> settle which quantity the axis is.
>
> **What survives, and it is what the figure is for:** the *direction* the
> border moves. It sits at a lower burden at high diffusivity and a higher
> burden as diffusivity falls (≈ 70 → ≈ 88 → ≈ 100 across the plotted range),
> which is the same direction `posb.dol_criterion` gives in any regime — slow
> transport means the burden has to be worse before splitting pays. The shape
> transfers; the numbers on the axis do not. Colour bar: **ln( ῡ²_DOL / (θ_I (υ² + εν)) )**, from ≤ −5 to ≥ 5.

Regions, as the caption names them (p.2527):

| region | meaning |
|---|---|
| left of the border | **SC** produces more P than DOL |
| right of the border | **DOL** produces more P than SC |
| **white** | SC population **extinct**, so DOL always wins |
| **black** | **both** DOL populations extinct |

Border positions, digitized against the printed ticks (COMPUTED, one
significant figure): at diffusivity 10 ×10⁴ the SC/DOL border sits near
**relative burden ≈ 70**; at diffusivity 2 ×10⁴ near **≈ 88**; as diffusivity
→ 0 near **≈ 100**. The white (SC-extinct) boundary is roughly vertical near
**burden ≈ 100**. No black region appears inside the plotted range.

**A printed internal contradiction.** The caption locates the border at
**ln(ῡ²_DOL/(θ_I(υ² + εν))) = 1**, but Eq. 16 says DOL is favored when
ῡ²_DOL/(υ² + εν) > θ_I, i.e. when that logarithm is **> 0**. The border must
be at **ln = 0**. The color bar's own pink/grey transition sits between the
−1 and +1 labels, i.e. at 0, so the **figure is drawn correctly and the
caption's "= 1" is wrong**. DERIVED from Eq. 16; INFERRED BY US as to which
of the two is the error.

### 12.2 Fig. 2 — growth effects and burden form (p.2529, rendered)

**2C.** "The analytical border separating SC- and DOL-favored parametric
spaces shifts with different product growth effects." Beneficial metabolites
reduce the effective burden and **shift the border right** (more SC);
toxic metabolites **shift it left** (more DOL). QUOTED/MODELLED. **No border
values are printed.**

The caption's own exception, worth keeping: "At low diffusivity, the shapes of
the borders for Toxic M and Beneficial M_e change such that at low burden
increasing diffusivity favors SC" (p.2529) — because there, raising
diffusivity improves SC growth more than it costs DOL. This is the one place
the monotone story in Fig. 4 fails, and the authors print it.

**2D — the functional form of burden moves the border by ~5×.** Three forms
are drawn on the same axes (0–120 relative burden, 0–~5 ×10⁴ diffusivity):

| burden form | border at relative burden ≈ |
|---|---|
| **linear, 1 − B** (green) | **20** |
| **exponential, e^(−B)** (red) | **36** |
| **Hill, 1/(1 + Bⁿ)** (blue) | **78** at high diffusivity, curving to **~105** at low |

COMPUTED (digitized against the printed 0/60/120 ticks), one significant
figure. The caption's claim is the right one — "Changing the mathematical
representation of burden does not change the **form** of the criterion"
(p.2529) — but the **location** of the border moves by a factor of about
**five**. Both halves belong in the file.

**The caption also says the three forms were not matched to each other, and
that is the sentence that decides how the ~5× can be used.** QUOTED, p.2529,
read off the rendered page and confirmed in the extracted text: "In this
example, parameters are chosen such that Hill-type burden reduces growth the
least and linear burden reduces growth the most." So the ordering of the three
borders is built into the example's parameters. ADDED 7 November 2026, because
a session claim rested on it and this file did not hold it.

The ordering is also a fact about the functions, independently of the
parameters: for every B >= 0, 1/(1+B^n) >= exp(-B) >= 1-B, with equality only
at B = 0. DERIVED. So Hill leaves the host growing fastest at the same burden
and linear slowest, and the burden at which DOL starts to win is highest for
Hill and lowest for linear. **What is the chosen example is the SIZE of the
spread, not its direction.**

### 12.3 The qualitative design guidelines (Fig. 4, p.2530)

"high enzyme burden, toxicity of intermediates/products, pathway complexity,
or number of extracellular steps will promote DOL over SC" (Fig. 4 caption).
QUOTED. No numbers.

### 12.4 Coverage and scope claims

| claim | value | kind | where |
|---|---|---|---|
| architectures analyzed | **24** common architectures of metabolic pathways | QUOTED | abstract, p.2526 |
| architectures drawn in Fig. 3 | **5** SC architectures with their 5 DOL counterparts | MODELLED | p.2529 |
| criterion valid for pathways longer than two steps | yes, SI Appendix §5 | MODELLED, `[unverified]` — SI not held | p.2529 |
| ε drops out of the generalized criteria | because "both SC and DOL require metabolite and/or enzyme transport" | DERIVED | p.2530 |
| corollary | DOL more easily beats SC when part or all of the pathway runs extracellularly — "easier for DOL to outperform SC" (p.2530) | DERIVED | p.2530 |

### 12.5 The literature examples they cite as consistent (all QUOTED)

- *E. coli*–*S. cerevisiae* coculture: **scoulerine from dopamine in a
  seven-enzyme pathway**, against an *S. cerevisiae* monoculture using **four**
  enzymes from norlaudanosoline (p.2530).
- *Trichoderma reesei*–*E. coli* coculture converting AFEX-pretreated biomass
  to **isobutanol**, against monoculture routes from glucose with fewer steps
  (p.2530).
- **Nitrification**: ammonia-oxidizers → nitrite, nitrite-oxidizers → nitrate
  (p.2526). Exists in **both** SC and DOL form (p.2530).
- **Syringate → acetate** by *Acetobacterium woodii* and *Pelobacter
  acidigallici* (p.2526). Also exists both ways.

**The authors' own honest caveat about their best examples.** For nitrification
and syringate, "what constrained these different implementations remains an
open question" (p.2530), and the DOL-vs-SC comparison in their engineered
examples may be confounded "in part due to less effort in optimizing DOL
implementations" (p.2530). QUOTED. Their criterion does not decide these
cases; it is consistent with them.

**One mechanistic prediction they do commit to, and check.** Their criterion
predicts the SC nitrifier should have the **lower growth rate** because it
expresses more enzymes, and they note this is "consistent with experimental
results — the SC cases were found to grow in biofilms, where a slower-growing
organism would have a higher fitness" (p.2530). QUOTED. Note that the check
is a consistency argument from the literature, not a measurement here.

---

## 13 · Diffusion, for T66 — what exists and what does not

### 13.1 The complete inventory

| paper | diffusion number stated or cited? |
|---|---|
| **BAL** | **None.** Searching the extracted text of all 8 pages for `diffus`, `cm2`, `mm2` returns **zero hits**. AHL transport is never quantified; the system is a well-mixed 9 nL chemostat, so it never needed to be. |
| **TSOI** | A dimensionless **"Diffusivity (×10⁴)"** axis in Figs. 1D and 2C–D, and a transport rate constant **η**. **No physical value, no units, no citation.** |
| **BASU** | **One number only: ξ = 0.001 mm² min⁻¹, "AHL intercellular diffusion"** (p.1134). **MODELLED** — it is an entry in a chosen parameter set, with no source cited and no measurement behind it. |

**SUPERSEDED 7 Nov 2026 -- see §19. Karig et al. 2018 was added to
`private/readings/` after this section was written and does supply two
coefficients.** The sentence below stood before that:

**No paper here supplies a measured or cited diffusion coefficient for AHL or
any comparable small signaling molecule in any medium.** Stating that plainly
is the finding; T66's number has to come from somewhere else.

### 13.2 Unit conversions of ξ, for whoever does source a comparator

COMPUTED: 0.001 mm² min⁻¹ = **1000 µm² min⁻¹** = **16.7 µm² s⁻¹** =
**1.67 × 10⁻⁷ cm² s⁻¹**.

For scale inside this course: session 2's README records D(GFP) in *E. coli*
cytoplasm as **7.7 ± 2.5 µm² s⁻¹** and D(GFP) in water as **~87 µm² s⁻¹**.
BASU's ξ sits between the two — i.e. it is in the range of a **protein** in a
cell, not of a **small molecule in agar**, which is a reason to be suspicious
of it before any arithmetic.

### 13.3 ξ fails every consistency check against BASU's own figures

Using the course's own convention t ~ L²/2D (T2, session 2; `diffusion_time`
in PS1), with D = ξ = 0.001 mm² min⁻¹. **COMPUTED, arithmetic shown.**

| L | t = L²/(2ξ) | |
|---|---|---|
| 6 mm (the simulated ring, Fig. 4b) | 36/0.002 = 18 000 min = **300 h** = 12.5 d | the figure shows the ring at ~15–30 h |
| 7 mm (the tuned ring position, Methods) | 49/0.002 = 24 500 min = **408 h** = 17 d | — |
| 10 mm (the measured ring, Fig. 4a) | 100/0.002 = 50 000 min = **833 h** = **34.7 d** | the experiment ran **36 h** |

Running it the other way, L = sqrt(2 ξ t): at t = 15 h, **1.34 mm**; at
t = 32 h, **1.96 mm**; at t = 36 h, **2.08 mm**. The measured ring is at
**10 mm**.

The diffusion coefficient needed to put a front at the observed place and time
is **D = L²/2t**:

| target | required D (mm² min⁻¹) | as a multiple of ξ |
|---|---|---|
| 10 mm at 15 h | 0.0556 | **56 ×** |
| 10 mm at 32 h | 0.0260 | **26 ×** |
| 6 mm at 15 h (their own Fig. 4b) | 0.0200 | **20 ×** |

**ξ is one to two orders of magnitude too small for the figures it generated.**

### 13.4 And a second, independent check fails harder

With first-order decay γ_A = 0.01 min⁻¹, a diffusing-decaying signal has a
steady-state penetration depth **ℓ_A = sqrt(D/γ_A)**. COMPUTED:
ℓ_A = sqrt(0.001/0.01) = **0.316 mm**. At 7 mm that is **22 e-foldings** — a
concentration ratio of about **4 × 10⁹** between the sender edge and the band.
DERIVED. No AHL synthesis rate makes that a usable design.

### 13.5 The resolution, and what it means for T66

§7.1 already gives it: **equation (5) is a discrete Laplacian with no grid
spacing**, so ξ in that equation has to be **D/Δx²** (units min⁻¹), and the
printed units mm² min⁻¹ are the units of **D**. The paper never states Δx.
Every inconsistency in §13.3–13.4 dissolves if Δx ≈ 4–5 mm, which is not a
credible lattice for resolving a 6 mm ring — so the likeliest reading is that
the simulation's length unit is not the millimetre the figures are labeled
in. **It cannot be settled from the main text.** What would settle it: the
Supplementary Information, or the modeling tool of ref. 14 (Basu *et al.*,
PNAS 2004 — which **is** in `private/readings/` as the session-10 reading).

> **Gap, stated for the session author.** T66 needs a defensible AHL diffusion
> coefficient with a stated medium (agar, not water, for the Basu geometry).
> **No paper in this session supplies one**, and **BASU's ξ must not be used
> as one** for the three reasons above. Source it separately, record it with
> its medium and its citation, and — because the course teaches wrong turns —
> consider making §13.3 the exercise rather than hiding it: *here is the
> paper's own parameter, here is its own figure, show they disagree.*

---

## 14 · Which figures are worth working on a slide

The standing rule is that an assigned paper's figures are **taught**, not
cited. There are plenty here. What each one lets a student conclude:

### BAL (required)

| figure | what it shows | what a student can conclude from it |
|---|---|---|
| **Box 1A** (p.2) | the full two-cell wiring diagram, both AHLs, both receivers, CcdA/CcdB | **The single best object in the paper.** Two cells, two signals, one promoter used twice. A student can trace each arm and answer "what happens if I delete `ccdA`?" without any model. This is where T64's sender/receiver model gets its structure. |
| **Box 1B left** (p.2) | the d_c vs k_c plane with three labeled operating points | A **two-parameter regime diagram** of a community. Lets a student say which parameter they would change to move from prey-domination to oscillation, and see that the regimes are separated by a *curve*, not a threshold. |
| **Box 1B right** (p.2) | three simulated time courses, one per region | What extinction, oscillation and domination *look like*. Pair with the left panel so the point and the trace are on the same slide. |
| **Fig. 1A, 1B** (p.3) | the two strains tested separately, OFF / +IPTG / +IPTG+AHL | The **decomposition discipline**: each half verified alone before coupling. Also where the crosstalk and burden admissions live (§3.1). A good slide for "what a control is for". |
| **Fig. 2A** (p.4) | the clean ~180 h oscillation, one reactor | The headline result. Lets a student measure a period off a printed axis and compare it to a model. |
| **Fig. 2B** (p.4) | **all twelve reactors**, four IPTG levels | **Teach this one.** It is the reproducibility slide, and it is the honest companion to 2A. See §15.1. |
| **Fig. 2C** (p.4) | bifurcation diagram vs IPTG, with the Hopf point marked and a period inset | Lets a student connect a *bifurcation* to a *knob they turned in a lab*, and compare Hopf ≈ 1.9 µM to the measured ≥ 5 µM. |
| **Fig. 3A, 3B** (p.5) | dilution-rate steps in two strain pairings | The second knob, and a second strain pair, so the result is not one configuration. Also where the model/experiment mismatch lives (§15.2). |
| **Fig. 3C** (p.5) | bifurcation vs *D* with a period inset and three traces | Lets a student read "raise *D* and the period falls, then everything washes out" off a diagram — and then notice the experiment sits outside it. |

### BASU (required per the brief; see §16.1)

| figure | what it shows | what a student can conclude from it |
|---|---|---|
| **Fig. 1a** (p.1131) | circuit operation at three AHL levels, with the AHL-gradient sketch and the **printed truth table** | **The band-detect in one picture.** The truth table makes the non-monotonicity a logical fact before any kinetics. This is the slide T65 should be built against. |
| **Fig. 1b–d** (p.1131) | the three plasmid maps | Which gene sits behind which promoter, on which replicon. Lets a student answer "which plasmid sets the upper edge of the band?" |
| **Fig. 2a vs 2b** (p.1131) | simulated and measured high-detect dose response, three variants | The **inverter**, and a direct simulation-vs-data comparison where the ordering matches and the spacing does not (§8.2). |
| **Fig. 2c vs 2d** (p.1131) | simulated and measured band-detect dose response, three variants | The band itself, and three bands at three positions from three LuxR variants. The clearest "we tuned a threshold on purpose" result in the session. |
| **Fig. 3b, 3c** (p.1132) | the two bullseyes | The **geometry inversion** (§9.1): the most sensitive strain makes the *outermost* ring. Also the 30 mm / 22 mm irreproducibility, if 3b and 3c go on the same slide. |
| **Fig. 4a** (p.1132) | the measured space–time heat map of ring formation | A **kymograph of a pattern forming**. Lets a student read the 15 h dead period, the 10 mm position and the ~32 h stabilization straight off printed axes — and then compute a diffusion time from them (§13.3). |
| **Fig. 4b vs 4c** (p.1132) | two simulated space–time maps, shift and no-shift | What a *positional shift* is, and that the same final ring can arrive two different ways. The honest version also says eight parameters differ, not one (§7.4). |
| **Fig. 4d, 4e** (p.1132) | the regression of response time and shift on γ_L | What "R² = 0.91" looks like when every point is a simulation. A good slide for the MODELLED-vs-MEASURED distinction the whole course rests on. |
| **Fig. 5a–d** (p.1133) | ellipse (simulated), ellipse, heart, clover | **Senders are the program.** Same receiver lawn, four sender layouts, four patterns. The cheapest possible demonstration that the pattern lives in the boundary conditions. |

### TSOI (optional)

| figure | what it shows | what a student can conclude from it |
|---|---|---|
| **Fig. 1A vs 1B** (p.2527) | SC and DOL schematics side by side | The one structural difference: in DOL the intermediate **must** cross two membranes and survive the extracellular space. |
| **Fig. 1C** (p.2527) | the inequality with its two sides annotated | **Biomass gain vs transport inefficiency**, as a picture. Worth a slide on its own. |
| **Fig. 1D** (p.2527) | burden × diffusivity plane with the border and the extinction region | Lets a student locate a design in a plane and see that above a burden the question stops being "which is better" and becomes "which one survives". |
| **Fig. 2D** (p.2529) | three burden functional forms, three borders | **The modeling-choice slide**: the form of the burden function moves the answer by ~5× without changing the criterion's shape (§12.2). |
| **Fig. 3** (p.2529) | five SC architectures, five DOL counterparts, and the five criteria | That the criterion generalizes, and that only θ_I changes. Good as a single wide slide, not read aloud. |

---

## 15 · What undercuts a clean teaching story

Listed because the course teaches wrong turns.

### 15.1 BAL — Fig. 2A is one reactor out of twelve, and the other eleven do not all oscillate

The caption's own hedge is "oscillatory dynamics were **elicited in several
reactors**" (p.4), not in all of them. Reading the twelve panels (§3.3):
the four IPTG = 0 reactors show prey washout (as intended); of the eight
induced reactors, several show the **prey rising and staying high with the
predator flat and low for 200+ h** (row 1 cols 2 and 3, at 250 µM; row 2
col 3, at 5 µM) — prey domination, not oscillation. **The clean 180 h trace of
Fig. 2A is a selected reactor**, and the parallel-reactor design the paper
sells as a feature is also what makes the irreproducibility visible. Both
halves are true and both should be said.

### 15.2 BAL — the model's oscillatory window does not contain the experiments that oscillate

COMPUTED from §3.4. The model (Fig. 3C) has oscillations only for
**0.04 ≲ D ≲ 0.18 h⁻¹**, with a minimum period of **~73 h**. The experiments
that the text calls damped oscillations are at **D = 0.20 h⁻¹** with period
**~50 h** (Fig. 3A) and **D = 0.23 h⁻¹** with period **~30 h** (Fig. 3B) —
**both outside the model's oscillatory range entirely, and both faster than
the model's fastest oscillation.** The paper's word for this is
"qualitatively accounts for" (p.5), used twice, and that phrase is carrying
the entire discrepancy. The *trend* (period falls as *D* rises) is reproduced;
the *values* are not.

### 15.3 BAL — three different washouts, of two different species

Worth separating before anyone draws a single "washout" arrow:
**(a)** IPTG = 0 → **prey** washed out, because the predator (MG1655) simply
grows faster (p.4); **(b)** Fig. 3A at D = 0.20 → **prey** falls to ~0 while
the predator oscillates; **(c)** Fig. 3B at D = 0.31 → **predator** washed
out (p.5), which is also what Fig. 3C's bottom-right panel predicts. The
model's washout is the predator's; two of the three observed washouts are the
prey's.

### 15.4 BAL — "damped predator–prey oscillation" with the prey at zero

In Fig. 3A after the step to D = 0.20 h⁻¹, the ~50 h ringing is in the **blue
(predator)** trace while the **red (prey)** trace sits near zero from ~350 h
to the end of the run. INFERRED BY US from the rendered panel: an oscillation
in one species with the other extinct is not a predator–prey oscillation, and
the text's "damped oscillatory dynamics with much shorter periods (~50 h)"
(p.5) does not distinguish the two cases.

### 15.5 BAL — IPTG is not a clean knob, and the authors say so

It induces `ccdB` in the predator **and** the QS system in the prey (p.3), and
the bifurcation analysis "accounts for the effects of IPTG on 3OC6HSL
production by the prey **and** CcdB expression by the predator" (p.4). A
single-parameter bifurcation diagram drawn against IPTG is therefore a path
through a two-parameter space, not a one-parameter sweep. DERIVED.

### 15.6 BAL — the counting method is one-color and biased in a known direction

Only one species is GFP-tagged; the other is obtained by **subtraction**, so
any dim tagged cell is counted as the *untagged* species (p.6). Combined with
a **~75 cells per reactor** detection limit (p.4) and the admitted imaging
artifacts near zero (p.4), the troughs — the most interesting part of an
oscillation — are the least trustworthy part of the data.

### 15.7 BASU — the headline kinetic claim is entirely simulated

§10. The abstract's "Experimental and theoretical analyses reveal which
kinetic parameters most significantly affect ring development" is, in the
Results, **100 simulations and one regression**. The experimental contribution
is one BD2 time course compared by eye to one simulation. This is the clearest
MEASURED/MODELLED mis-tag available in the session, and it is in the abstract
of a *Nature* paper, which is why it is worth teaching rather than scolding.

### 15.8 BASU — equation (5) is wrong as printed, twice

§7.1: the decay term lacks its `A`, and the discrete Laplacian lacks its grid
spacing. A student handed equations (1)–(5) and told to reproduce Fig. 4 will
fail, and the failure is the paper's, not theirs. If the session hands out the
model, hand out the correction with it, labeled.

### 15.9 BASU — the "agreement" between model and data is ordinal, not quantitative

§8.2 and §8.4. The model's HD1/HD2 separation is ~3.5× against the data's
~20×; the band positions are shifted by 2–3× in absolute AHL. The claim
"correlated well with model predictions" (p.1130) is true of the ranking.

### 15.10 BASU — the irreproducibility is in the paper and is not a circuit parameter

The same BD2-Red strain made a **30 mm** ring in one experiment and a
**22 mm** ring in another (p.1130). Everything the authors offer as an
explanation — sender and receiver growth rates, population densities,
nutrients, agar density — is an **environment** variable. Nothing a designer
tunes inside the cell moved it by 36 %.

### 15.11 BASU — "no shift" in the experiment is not the same as "no shift" in the model

The experiment ran **36 h** and found no observable positional shift
(p.1131). Fig. 4b's simulated shift is ≈ **0.1 mm** over the same window
(§10.1) — below what a 2.5× objective over a 30 mm field would resolve.
INFERRED BY US: the experiment is consistent with the stable-LacI simulation
but does not *discriminate* it from a small shift, and the paper's own
language ("accounts for the similarity", p.1132) is an eyeball comparison.

### 15.12 BASU — pHD3's lineage is stated two different ways

§5.2. Results and the Fig. 2 caption read as "wild-type LuxR at half copy";
Methods say pHD3 derives from pHD1, i.e. **hypersensitive** LuxR at half copy.
Anyone building a dose-response exercise needs the Methods version.

### 15.13 TSOI — the figure caption contradicts the criterion

§12.1. Caption says the border is at ln(·) = 1; Eq. 16 puts it at 0.

### 15.14 TSOI — the criterion's own best natural examples do not decide

§12.5. Nitrification and syringate metabolism exist in **both** SC and DOL
form, and the authors say what constrained the difference "remains an open
question" (p.2530). The paper is honest about this; a slide that uses
nitrification as a *confirmation* of the criterion would not be.

### 15.15 TSOI — no experiment, anywhere

The paper is analysis only. Every number in §11–§12 is MODELLED or DERIVED.
It is also the **only** source in this session for the division-of-labour
third of the title — and it is the **optional** reading.

---

## 16 · Contradictions with what the repo says about this session

Checked against `docs/coverage-matrix.md` (lines 136–140, 234),
`readings.yaml` (s24 block, `limits` block) and
`private/log/week13-handoff.md`, all read this session.

### 16.1 The brief calls Basu 2005 required; `readings.yaml` does not list it at all

`readings.yaml` `s24:` contains **one** entry, `balagadde2008`, `required:
true`. There is **no `basu2005` key anywhere in the file** (searched). The
Basu and Tsoi PDFs were added to `private/readings/` on **7 November 2026**
(`ls -la` timestamps 15:57 and 15:58) — i.e. today, after the handoff was
written.

The handoff says so explicitly in §4(a): the band-detect paper "is **not
declared anywhere**", and names **three** routes out (teach it from the deck
unassigned; swap it in and demote Balagadde; or narrow T65 so band-detect
becomes a worked example). It calls that **"Adam's call, not a design decision
to make quietly"**.

Making both required also breaks two stated limits:
`max_required_per_assignment: 1` and `max_required_pages_per_assignment: 12`
(Balagadde 7 pp. + Basu 5 pp. = **12 pp.**, so the page cap is met exactly,
but the **one-paper cap is not**).

**This is unresolved, not resolved.** The extraction covers both papers fully
either way, so nothing here depends on the answer — but a session built on
"two required readings" is built on an override that does not exist in
`readings.yaml` yet.

### 16.2 Tsoi 2018 is undeclared too

No `tsoi` key in `readings.yaml`. The brief calls it OPTIONAL, which in this
course's schema means `required: false` ("optional depth, usually for 247
students"). There is no such row. It also has no `focus` line, and the file's
own comment says `focus` is **required** and that "Read the paper" is not an
assignment.

### 16.3 `readings.yaml` asserts the BioModels entry; the paper does not

The s24 `focus` reads "The model is in BioModels as BIOMD0000000296, so run it
rather than retype it", and the handoff §3 repeats it. **Balagadde never
mentions BioModels** (§4.1). The accession may well be right — it is not
*wrong* for a curated model to exist without the paper naming it — but
nothing in this repo or in the PDF establishes what the entry contains.
`[unverified]`, as above.

### 16.4 The handoff's "one paper, three topics" problem is real and is worse than stated

Handoff §4(a): "The session title carries quorum sensing, **patterning**, and
division of labour. T65 is band-detect/patterning. Balagadde is predator–prey
— it does not do patterning at all." **Confirmed by reading it**: Balagadde
contains no spatial data of any kind; its system is a 9 nL well-mixed
chemostat and the word *diffusion* does not occur.

The part the handoff does not say: **division of labour is also unserved by
the required reading**, and the only source for it is Tsoi, which is optional
and has no experiment. So the one required paper covers **one** of the three
things in the session title.

### 16.5 `readings.yaml` records Balagadde as 7 pages; the PDF has 8

`pages: 7` with the note "[unverified: page count — article-numbered]".
`pdfinfo` reports **8 pages**; the journal's own page footers run **1 to 8**,
with pp. 7–8 being references. If the cap is meant to count reading load,
7 is arguably right (pp. 1–6 are text); if it is meant to count the PDF, it is
8. Small, but it is the same defect class that bit Nielsen 2016 (s14 note in
`readings.yaml`).

### 16.6 `PRIOR-YEARS.md` §3 proposes taking the diffusion coefficient from Basu — which §13 shows would be wrong

`sessions/s24-communities/PRIOR-YEARS.md` (it appeared under that name during
this session; it was `.PRIOR-YEARS.part1`, ending at §2.6, when this
extraction began) now carries a §3 that pins T2's form and convention:
`t ~ L²/2D` with the factor of 2 explicit, D(GFP) = 7.7 µm² s⁻¹ in *E. coli*
cytoplasm, 87 µm² s⁻¹ in water, ~27 µm² s⁻¹ in eukaryotic cytoplasm, and a
standing instruction to state the convention before the number. Session 24 is
its **fourth** reuse, not its second (s03 and s18 precede it).

Its §3 then says the AHL gap is **"[unverified: no AHL diffusion coefficient
in agar appears on any prior-year slide or in the 2026 decks. Settled by
taking D from Lu et al., PNAS 2018 **or Basu et al., Nature 2005** and citing
it.]"**

**The Basu half of that suggestion does not survive reading Basu.** §13 of
this file shows that BASU's only diffusion number, ξ = 0.001 mm² min⁻¹
(= 16.7 µm² s⁻¹), is a model parameter with no source, is **20–56× too small
to reproduce Basu's own figures**, and sits in an equation whose grid spacing
is never stated. **Do not take T66's D from Basu 2005.** The Lu & Karig route
is still open and is the better one — `PRIOR-YEARS.md` §2.2 records a
*measured* front, "±4 cm on a plate at 0, 2.5, 5 and 8 hours", from 2018 L24
p.18. `[unverified]` — that slide was not opened this session.

Its §3 also uses "D ≈ 5 × 10² µm² s⁻¹ for a small molecule in agar" to get
"hours, not milliseconds" at L = 1 cm. That value is **30× larger than BASU's
ξ**, which is a second, independent reason to distrust ξ — and the 5 × 10²
figure itself carries no citation in that file either. Both need sourcing.

### 16.7 Nothing in the coverage matrix contradicts the papers

T64 (MIX), T65 (AUTO), T66 (AUTO), the PS9 window (Nov 19 → Dec 3) and T64's
appearance on the final are all consistent with what the papers can support —
with the AUTO caveats in §17.

---

## 17 · Gaps — what T64, T65 and T66 need that no paper here supplies

### T64 — sender/receiver model construction (MIX; also on the final)

**Supplied.** BAL Box 1A gives a complete, unambiguous two-cell topology with
two signals, two receivers and an antidote/toxin pair — enough for a student
to *write* a model. BASU §7.1–7.2 gives a complete printed sender/receiver
model with a complete parameter set, which is the better object if the task is
"build and run".

**Missing.**
1. **BAL's equations.** They are in a supplement this repo does not hold
   (§4). If T64 is meant to reproduce Balagadde's model, the supplement must
   be obtained, or the BioModels entry verified, or the task must be
   "construct your own from the wiring diagram" — which is defensible and
   arguably better, but is a different task.
2. **Any BAL rate constant.** Not one AHL production, degradation, binding or
   killing rate is printed. The only numbers the model side offers are the
   bifurcation-axis values k_c and d_c in Box 1B.
3. **A sender in BASU's model.** Equations (1)–(5) describe the **receiver**.
   The sender appears only as a boundary condition: "the senders' AHL
   synthesis rates were modified to ensure that fluorescence rings always
   formed at the same distance" (p.1131). **No sender synthesis rate is ever
   printed.** A T64 task that asks a student to model a sender and a receiver
   must supply the sender rate itself.

### T65 — band-detect / patterning analysis (AUTO — needs exact reference values)

**Supplied.** The complete BD2 model: eqs. (1)–(5) with the two corrections of
§7.1, the fourteen-parameter table of §7.2, and the printed variant rules of
§7.3 (ρ_R ×10 for BD1; α_G, α_L2, [LuxR] ÷2 for BD3). That is reproducible to
the last digit and is the right basis for an autograder.

**Missing.**
1. **Any printed numeric threshold, band position or band width.** Every
   value in §8 is our digitization. **An autograder must not use them.**
2. **What the Fig. 2 caption's six confidence-interval pairs bound** (§6.3).
   Without that, those twelve printed numbers are unusable.
3. **Error bars.** None are reported on any BASU measurement. Fig. 2b and 2d
   are single points per concentration (medians of FACS distributions); the
   ring diameters are single values; Fig. 4a is one time course.
4. **The lattice spacing for eq. (5)** (§7.1, §13.5), without which the
   spatial half of the model cannot be run as printed. **If T65 is to be
   autograded, keep it in the well-mixed (liquid-phase) limit**, which the
   paper itself defines: liquid-phase simulations omit eq. (5) entirely
   (p.1134). That limit is fully specified and fully reproducible.

### T66 — diffusion length scale in a community (AUTO, reuses T2)

**Supplied.** A length scale and a timescale to put into t ~ L²/2D: the ring
at **10 mm**, first fluorescence at **15 h**, stabilization at **~32 h**,
experiment length **36 h** (§6.1) — all MEASURED and all printed. Also the
30 mm / 22 mm ring diameters.

**Missing — and this is the hard gap.** A **diffusion coefficient**. §13:
BAL has none, TSOI has none, and BASU's ξ is a model parameter that is
**20–56× too small to reproduce BASU's own figures** and that implies a
0.32 mm penetration depth against a 7–10 mm ring. T66 cannot be built on it as
a measured value.

What the session author must do, in order:
1. Source a diffusion coefficient for **3OC6HSL (or a comparable AHL) in
   agar**, with a citation and the medium stated. Water is the wrong medium
   for a plate and should be used only as a bound.
2. Check `PRIOR-YEARS.md` §2.2's Lu & Karig slide (±4 cm at 0, 2.5, 5 and
   8 h) — that is a *measured front*, which is exactly what T66 wants and is
   better than any tabulated D. **Do not follow `PRIOR-YEARS.md` §3's other
   suggestion and take D from Basu 2005** (§16.6).
3. Decide whether §13.3's failure is the exercise. It is reproducible from
   printed numbers alone, it uses T2 unchanged, and it produces a correct
   engineering conclusion (*the printed parameter cannot be a diffusion
   coefficient*) from arithmetic a student can do in two lines.

### Across all three

- **No supplementary information is held for any of the three papers.** BAL's
  eqs. S14–S17 and Figs. S1–S7, BASU's Table S1 and surface maps, and TSOI's
  SI Appendix §§2.3, 3.1.1, 3.4, 4.1, 5 and Figs. S1, S3 are all referenced
  in this file and none can be checked. Every `[unverified]` above traces
  back to that.
- **No session-24 library module exists.** `posb/` has no `communities` or
  `populations` module (handoff §0). Three of the five week-13 targets are
  AUTO and none has a function to import.

---

## 18 · What is NOT claimed

- **No AHL concentration in BAL is a threshold.** The only AHL concentration
  in the paper is the **100 nM** supplied exogenously in the Fig. 1 controls.
  It is a dose, not a K_d and not a switch point.
- **No diffusion coefficient in this file is MEASURED.** See §13.
- **BASU's R² values are not evidence about the real circuit.** See §10.
- **The 8-fold CcdB potency gain, the pHD3 copy-number halving, and the
  macroscale "hints at oscillation" are all data-not-shown or
  supplementary-only.** Do not present any of the three as a result of the
  papers we hold.
- **Nothing here says either paper's authors designed from a model.** BAL
  tested "many combinations of promoters, origins of replication and
  bacterial host strains" and narrowed to one (p.3); BASU says the band-detect
  was "**guided by** a mathematical model" (p.1130), which is a real claim but
  a weaker one than "derived from".
- **No claim about the BioModels entry.** §4.1.
- **Every digitized value in §§2.2, 3.3, 3.4, 8, 10.1 and 12 is ours**, is
  calibrated against printed tick labels, and is good to about one
  significant figure. None of them is in a paper.

---

## 19 · KARIG et al., PNAS 115(26):6572-6577 (2018) — added 7 November 2026

Optional reading for s24, and the source of the only sourced diffusion numbers
the session has. Written after §§1-17, which is why §13.1 and §17's T66 gap are
superseded. Main text read from the PDF; SI read from the 54-page combined file
`Session 24 - karig-2018-stochastic-turing-patterns-WITH-SI-INSTRUCTOR.pdf`.

### 19.1 The two diffusion coefficients

| quantity | value | KIND | where |
|---|---|---|---|
| D, A3OC12HSL | **83 µm²/s** | **MODELLED from MEASURED** | main text p.6573 |
| D, IC4HSL | **1,810 µm²/s** | **MODELLED from MEASURED** | main text p.6573 |
| ratio of the two | **21.6 ± 10** | **MEASURED** (their word) | SI |
| SI originals | Dc12 = 0.003 cm²/hr, Dc4 = 0.065 cm²/hr | same | SI |

Quote, main text: "The estimated diffusion coefficient for A3OC12HSL is
83 µm2/s". **KIND matters here and the word is theirs: *estimated*.** The SI says
they were obtained "by parameter estimation of the fluorescence wave profile
over time" — a fit to measured data, not an instrument reading. COMPUTED check:
0.003 cm²/hr = 83.3 µm²/s and 0.065 cm²/hr = 1806 µm²/s, both consistent.

**Three qualifications, all of which must travel with the number:**

1. It is an **effective cell-to-cell** coefficient through a bacterial lawn, not
   a free-solution value. Main text attributes the slowness to partitioning of
   A3OC12HSL into the membrane — and **hedges it**: "likely due to". The SI says
   "One possible explanation". Do not state the mechanism flat.
2. The free-solution prediction for the ratio, by Wilke–Chang, is about **1.5**.
   The measured 21.6 is therefore a property of cells, not of the molecules.
3. **This is 3OC12HSL.** Basu's inducer is **3OC6HSL** (Basu p.1133). Neither of
   Karig's two molecules is Basu's. INFERRED BY US: these coefficients cannot be
   combined with Basu's γ_A or applied to Basu's ring geometry.

### 19.2 The hundredfold, and what it is NOT

Quote, SI: the diffusion constants "must be separated by a factor on the order
of 100 **in our non-stochastic simulation**". **KIND: MODELLED, and
system-specific.**

**It is not a classical Turing requirement.** There is no universal hundredfold;
the critical ratio falls out of the Jacobian of whatever kinetics are assumed.
Karig's own abstract points the other way — their stochastic theory has "no
severe requirement on the ratio" — and the introduction notes that natural
morphogens do not have widely differing diffusion coefficients.

**Consequence for the session: "derive the requirement, then watch it be beaten"
cannot be done without naming a kinetic scheme.** Attribute the 100 to their
simulation, or name the scheme and derive it properly. The prior-year deck's
bare bracket `[>100x difference required, 20x measured]` (2018 L24 p.16) is the
same unattributed claim.

### 19.3 Quorum thresholds — and they are NOT an orthogonality argument

| quantity | value | KIND | where |
|---|---|---|---|
| half-activation, 3OC12HSL | **0.003 µM** | **MEASURED** | SI, dosage-response |
| half-activation, C4HSL | **3 µM** | **MEASURED** | SI, dosage-response |

These are the sensitivities of **two different reporter constructs each to its
own cognate signal**. They say nothing about crosstalk.

**The crosstalk question is answered the other way in the same paper.** SI §4 is
titled "Signal Specificity and Competitive Inhibition" and reports that
A3OC12HSL competitively binds RhlR, measured over 0–30 µM against C4HSL held at
3 µM, with fluorescence falling monotonically. The main text's Fig. 1A caption
says the inhibitor acts "with additional repression by A3OC12HSL via
competitive binding". Orthogonality in their circuit comes from **promoter
choice**, not from the threshold gap.

**So a slide saying the thousandfold gap "is what lets one circuit use both
without crosstalk" is false**, and the paper measures the crosstalk it denies.
The honest teaching point is better: two homologous systems a thousandfold apart
in sensitivity are **still not orthogonal**, and someone had to measure that.

### 19.4 What §13.1's gap now looks like

T66 has sourced diffusion coefficients — **for Karig's system, in Karig's
geometry.** It still has none that can legitimately be combined with Basu's
γ_A = 0.01 min⁻¹, because ξ is D/Δx² (§13.3) and Karig's are a different signal
in a different lawn. **INFERRED BY US: the penetration depth √(D/γ) should be
taught as a formula, with the statement that this folder cannot source its value
for Basu's system — which is T66's actual lesson.** Any number presented as
"Basu's penetration depth" is computed from ξ and inherits ξ's defect; §13.4
runs that arithmetic as a *reductio against* ξ, not as a design knob.

---

## 20 · BALAGADDE's MODEL, from the BioModels deposit — resolved 7 November 2026

§4.1 marked every claim about BIOMD0000000296 `[unverified]` and said not to put
"BioModels has the model" on a slide until someone checked. **Checked.** Read
from the JWS Online curation of the deposit, which states it was obtained from
BioModels as BIOMD0000000296 and curated by reproducing the figures.

**The model is FOUR-dimensional. The signals are state variables with their own
dynamics.** That is the finding, and it changes session 24's move 4.

### 20.1 The reactions, as deposited — QUOTED

    J0  predator growth   kc1 * C1 * (1 - (C1 + C2)/Cm)
    J1  predator death    (D + d1 * K1/(K1 + A2^2)) * C1
    J2  prey growth       kc2 * C2 * (1 - (C1 + C2)/Cm)
    J3  prey death        (D + d2 * A1^2/(K2 + A1^2)) * C2
    J4  3OC12HSL synth    kA1 * C1
    J5  3OC12HSL removal  (dAA1 + D) * A1
    J6  3OC6HSL synth     kA2 * C2
    J7  3OC6HSL removal   (dAA2 + D) * A2

| parameter | value | note |
|---|---|---|
| kc1, kc2 | 0.8, 0.4 | predator and prey growth, h⁻¹ |
| Cm | 100 | shared carrying capacity |
| d1 | 1.0 at IPTG = 5 | **set by an assignment rule** |
| d2 | 0.3 | |
| K1, K2 | 10, 10 | |
| kA1 | 0.1 | |
| kA2 | 0.035 at IPTG = 5 | **set by an assignment rule** |
| dAA1, dAA2 | 0.017, 0.11 | abiotic signal decay |
| D | 0.1125 | dilution |
| initial | C1 = C2 = 20, A1 = A2 = 0.1, IPTG = 5 | |

**KIND: QUOTED** from the deposit. The *paper* prints none of this — its
equations are in a supplement this repo does not hold (§4.1). So these are the
deposited model's values, which is a different provenance from the paper's text
and a slide must say which it is using.

### 20.2 The two assignment rules, and why IPTG is the experimental knob

    kA2 = 0.02 + 0.03 * IPTG^2/(5^2 + IPTG^2)
    d1  = 0.5  +        IPTG^2/(5^2 + IPTG^2)

**IPTG enters nowhere else.** It tunes the prey's signal synthesis and the
predator's death rate, and nothing else. That is exactly why the paper's own
route across the Hopf is IPTG rather than dilution, and it settles the question
the s24 review raised about Box 1B being spanned by strain parameters.

### 20.3 The design consequence — DERIVED, and it corrects the session

The session's DESIGN specified a **two**-state model: two logistic growths
sharing a carrying capacity, cross-death terms modulated by the other's signal,
and a common dilution rate, with the signals eliminated. **That model cannot
oscillate, at any parameter values.** At any interior fixed point the logistic
terms cancel against the death terms and

    tr J = -(kc1*C1 + kc2*C2)/Cm

exactly — strictly negative for every parameter choice, so the interior fixed
point never loses stability and there is no Hopf at any D. Verified two ways:
analytically, and numerically over 4000 random interior fixed points, where the
closed form held to 1e-5 and the trace was negative in every case.

**The oscillation lives in the signal dynamics.** Put A1 and A2 at
quasi-steady state — A1 = kA1·C1/(dAA1+D), A2 = kA2·C2/(dAA2+D) — and you
recover exactly the 2-state model above, and the oscillation disappears with
them.

**That is a better move than the one the design had**, and it is sourced:
apply session 4's QSSA to the signals, watch the Hopf vanish, and conclude that
the lag between a population and its own signal is what makes the community
oscillate. Same lesson as session 11's repressilator and T30, in a new
substrate.

### 20.4 The deposit reproduces Fig. 3C — so the mismatch with the EXPERIMENT is real

**First, the transcription is right.** Computed from the deposited model against
§3.4's digitization of the paper's own Fig. 3C:

| | deposited model, computed | Fig. 3C, digitized |
|---|---|---|
| oscillatory branch begins | **D = 0.03673** | 0.035–0.04 |
| upper crossing | **D = 0.16743**, period **73.6 h** | period ≈ 73 h at D ≈ 0.168 |
| coexistence lost | **D ≈ 0.1762–0.1765** | washout above D ≈ 0.18 |

Three independent agreements. **The deposit is the paper's model**, and nothing
below is a transcription error.

### 20.5 The model against the experiment, at the paper's own dilution rates — COMPUTED

Experimental observations are §3.4 and §2.4, MEASURED. Model column computed
from the deposit.

| D (h⁻¹) | experiment | deposited model | |
|---|---|---|---|
| 0.11 | coexistence, steady | **oscillates**, limit cycle **168.1 h** | disagree |
| 0.15 | coexistence, steady | **oscillates**, limit cycle **122.5 h** | disagree |
| 0.20 | damped oscillation, ~50 h | **no coexistence state at all** | disagree |
| 0.23 | damped oscillation, ~30 h | **no coexistence state at all** | disagree |
| 0.31 | predator washout | no coexistence state | agree |

**The model and the experiment disagree at four of the five dilution rates the
paper ran, and they disagree in opposite directions.** Where the experiment is
steady, the model oscillates. Where the experiment oscillates, the model has
already lost coexistence. The one agreement is washout at 0.31.

**The model does not merely oscillate in the wrong place, it oscillates on the
wrong timescale.** At D = 0.11 it sustains a limit cycle of **168 h** where the
experiment was steady — about 3.4× the slowest oscillation the reactor ever
showed. Nothing the model does at any dilution rate resembles the experiment's
~30–50 h damped oscillations.

> **CORRECTED 8 November 2026, and the correction matters.** This table first
> read "period 49 h" and "period 55 h", and the closing sentence set the 49 h
> beside the experiment's ~50 h at D = 0.20 as a near-coincidence at the wrong
> dilution rate. **Those were linearised periods**, 2π/|Im λ| at the unstable
> fixed point (49.50 h and 54.58 h, reproducible), not the periods of the
> oscillations the model actually settles into. Comparing them with a measured
> period compares unlike quantities. Integrating the four-state deposit to
> t = 20,000 h with rtol 1e-10 and measuring peak-to-peak in C₁ over the last
> 8,000 h gives **168.1 h at D = 0.11** (47 cycles, sd 0.01 h, C₁ swinging
> 0.020 → 25.98) and **122.5 h at D = 0.15** (64 cycles, sd 0.01 h, 0.345 →
> 9.10). COMPUTED. The "sustained oscillation" classification was right; the
> numbers beside it were the wrong ones.
>
> One linear period in this file **is** sound and should not be swept with the
> rest: the **73.65 h at the upper Hopf crossing**. At a Hopf the linear period
> is the period of the cycle that emerges, so there the two agree by
> construction.

**This supersedes §15.2's version of the mismatch**, which compared a digitized
window against two experimental points. This is computed from the deposited
model at the authors' own settings, and it is much sharper. The paper's
"qualitatively accounts for" is carrying all of it.


---

## 21 · TAMSIR, TABOR & VOIGT, *Nature* 469(7329):212–215 (2011) — added 7 November 2026

Optional reading for s24, declared in `readings.yaml` as `tamsir2011`. Read
from `private/readings/Session 24 - tamsir-2011-multicellular-computing-nor-gates-OPTIONAL.pdf`,
which is the **NIH-PA author manuscript** (9 PDF pages, journal pp. 212–215);
page numbers below are the manuscript's own, which is what the PDF carries.
Added because session 24's move 5 leads on this paper and nothing in this file
held any of it.

### 21.1 The gate, and the wire

| item | what it is | KIND |
|---|---|---|
| the gate | a **NOR** gate: two tandem promoters as inputs drive a repressor, which inactivates the output promoter | QUOTED, abstract |
| inputs and output | **both are promoters**, which is why gates layer | QUOTED |
| the wire | "Acyl homoserine lactone (AHL) cell–cell communication devices are used as signal-carrying 'wires'" | QUOTED |
| synthases | *P. aeruginosa* PAO1 **LasI** or **RhlI**, expressed as a gate's output | QUOTED |
| receivers | *P. aeruginosa* PAO1 **LasR** or **RhlR** | QUOTED |
| the two molecules | **3OC12-HSL** (from LasI) and **C4-HSL** (N-butyryl-homoserine lactone, from RhlI) | QUOTED |

> **Which AHLs these are, stated because it has already been got wrong once.**
> Tamsir's wires are **3OC12-HSL and C4-HSL**. BASU's inducer is **3OC6HSL**
> (Basu p.1133), and BAL uses 3OC6HSL and 3OC12HSL (§1.1–1.2). So Tamsir's
> wires are **not** Basu's signal. They **are** exactly KARIG's two molecules
> (§19.1), which is the legitimate link: the pair Karig measured diffusion
> coefficients for is the pair Tamsir wires gates with. INFERRED BY US from the
> two papers' own molecule names.

### 21.2 The XOR, as built

QUOTED, p.3 (manuscript): "An XOR gate is built with three NOR gates and a
buffer gate (Fig. 3a)." **Four strains, each carrying a different logic gate**,
"spotted onto an agar plate in the spatial arrangement required to perform this
function (Fig. 3b)".

| strain | gate | inputs | output |
|---|---|---|---|
| cell 1 | NOR | Ara, aTc | **LasI** → 3OC12-HSL to cells 2 and 3 |
| cell 2 | NOR | 3OC12-HSL + **Ara** | **RhlI** → C4-HSL |
| cell 3 | NOR | 3OC12-HSL + **aTc** | **RhlI** → C4-HSL |
| cell 4 | **buffer** | C4-HSL | the circuit output |

All QUOTED from p.3. "The output of a buffer gate is 'on' only when the input
is 'on'." Each intermediate colony was checked by replacing its output gene
with YFP (Fig. 3c).

### 21.3 All sixteen gates, and what that costs

QUOTED, p.3: "We constructed a small library of strains that act as simple
logic gates, most of which are components of the XOR gate (Fig. 4a). Circuit
diagrams showing how all of the sixteen possible two-input logic gates can be
constructed using the library are shown in Fig. 4b. Each circuit diagram is
reproduced by the spatial arrangement of the component strains. **None of these
circuits required additional genetic manipulation.**"

| quantity | value | KIND |
|---|---|---|
| two-input Boolean functions covered | **16**, all of them | QUOTED |
| induction range across the set | **5-fold (XOR) to 335-fold (B gate)** | MEASURED, p.3 |
| the abstract's version of the same range | "5- to >300-fold" | QUOTED |
| signal degradation with layer count | "**No degradation** in the signal is observed as a function of the number of layers" | QUOTED/MEASURED |

### 21.4 The reason the session wants this paper — QUOTED, and it is in the INTRODUCTION

"In addition, a program can be built from a smaller number of orthogonal parts
(for example transcription factors) by re-using them in multiple cells."

**This sentence is in the introduction, not the abstract.** `readings.yaml`'s
`tamsir2011` focus line sent students to "the sentence in the abstract"; it is
not there. CORRECTED in `readings.yaml` 7 November 2026.

The abstract's own version of the argument is different and weaker for this
purpose: it says compartmentalizing "produces more reliable computation by
population-averaging the response".

### 21.5 The plate, as a set of numbers a slide can use

MEASURED, Methods (manuscript p.8):

| quantity | value |
|---|---|
| plate | **12 mL LB agar** (1.5 % agar, 2.5 % LB-Miller) in a **100 mm** Petri dish |
| inducers in the plate | **2 mM Ara** and/or **500 ng mL⁻¹ aTc** |
| spot volume | **1 µL** overnight culture |
| colony spacing | **7 mm**, square grids |
| delay between layers | **12 h**, "to ensure communication signals had propagated sufficiently" |
| readout | output colony scraped at 12 h after the last layer; cytometry, ≥ **50,000** events |

**The 12 h delay per layer is an external clock, and the authors say so**
(p.4): "Another source of robustness is the external clock that is implemented
by delaying the spotting of colonies for each layer. Genetic computing is
asynchronous and this may result in hazards, that is, transient incorrect
outputs that occur as a result of mismatched delays in the circuit." QUOTED.
Note the 7 mm spacing against the 12 h delay — that is a propagation length and
a propagation time for an AHL on agar, and the only pair of its kind in this
session's folder. **It is not a diffusion coefficient**, and turning it into
one would need a front position rather than a sufficiency statement: 12 h is
stated as *enough*, not as the arrival time. INFERRED BY US; do not compute a D
from it.

### 21.6 What is NOT in the file we hold

- The robustness claim "with respect to the distance between colonies and the
  time and density at which they are spotted" cites **Supplementary Figure
  10**, which this repo does not hold. `[unverified]`
- Supplementary Table 5 (the strain/plasmid list behind Fig. 4a) is not held.
  `[unverified]`
- No transfer function is printed as **fitted parameters** anywhere. They are
  **measured and plotted**, which is a different and sufficient thing — see
  §21.7, which corrects a first draft of this bullet that said the paper has no
  transfer functions at all.

### 21.7 The transfer functions, which the paper does measure

Added 7 November 2026 after §21.6's first draft understated this.

**Fig. 1c, MEASURED.** The caption defines the object: "The transfer function is
defined as the output as a function of input at steady state." Three rows are
plotted — P<sub>BAD</sub> and P<sub>Tet</sub> individually (top), the
P<sub>BAD</sub>–P<sub>Tet</sub> tandem promoter (middle), and the NOR gate
(bottom). Inducer grids, printed: **0, 0.0005, 0.005, 0.05, 0.5 and 5 mM Ara**
(left to right) and **0, 0.025, 0.25, 2.5, 25 and 250 ng mL⁻¹ aTc** (bottom to
top). "Fluorescence values and their error bars are calculated as mean ± s.d.
from three experiments." QUOTED.

| quantity | value | KIND |
|---|---|---|
| P<sub>BAD</sub>–P<sub>Tet</sub> OR gate induction, off (−Ara, −aTc) to on (+Ara, +aTc) | **7,000-fold** | MEASURED, p.2 |
| the OR gates' character | "some characteristics of fuzzy logic" | QUOTED |
| the NOR gates' character | "**nearly digital**" | QUOTED |

**Fig. 2, MEASURED against PREDICTED.** Three tandem promoters characterized:
P<sub>BAD</sub>–P<sub>Tet</sub>, P<sub>BAD</sub>–P<sub>Las</sub> and
P<sub>Tet</sub>–P<sub>Las</sub>, where P<sub>Las</sub> is activated by
**3OC12-HSL**. 3OC12-HSL grid: **0, 0.001, 0.01, 0.1, 1 and 10 µM** (the last
value read from the caption's printed series). The prediction is explicit and
is the teachable part: "These gates perform as the additive combination of the
individual transfer functions of the two input promoters and the CI-repressor
NOT gate", and "the predicted transfer function is the simple **sum** of the
transfer functions measured for the individual promoters". "The predicted
transfer function for the six logic gates shown in Fig. 2 matched the
experimental results." QUOTED.

**And one of them did not compose, which the paper prints.** "One tandem
promoter, P<sub>Tet</sub>–P<sub>BAD</sub>, did not function as predicted
(Supplementary Figure 3). The failure observed for P<sub>Tet</sub>–P<sub>BAD</sub>
probably arises from some position-dependent interference" — offered causes are
DNA looping, occlusion of transcription-factor binding sites, or changes in the
ratio or stability of output mRNAs, and the paper settles none of them. QUOTED.
Note that P<sub>BAD</sub>–P<sub>Tet</sub> works and P<sub>Tet</sub>–P<sub>BAD</sub>
does not: **the same two promoters, swapped in order**. The supporting figure is
supplementary and not held — `[unverified]` as to what the failure looks like,
QUOTED as to the claim.

**Dynamic range, and where it comes from.** "The range of induction varies from
5-fold (XOR) to 335-fold (B gate). The dominant contribution to the dynamic
range of the complete circuit is due to the intrinsic range of the final
circuit (Supplementary Figure 7). For example, the XOR and NAND gates are
limited by the output of P<sub>Rhl</sub>." MEASURED/QUOTED; Supplementary
Figure 7 not held.

---

## 22 · ZHOU, QIAO, EDGAR & STEPHANOPOULOS, *Nat Biotechnol* 33(4):377–383 (2015) — added 7 November 2026

Optional reading for s24, declared as `zhou2015`. Read from
`private/readings/Session 24 - zhou-2015-distributing-metabolic-pathway-OPTIONAL.pdf`,
the **HHS Public Access author manuscript** (23 PDF pages; `readings.yaml`
records `pages: 23`, and the assigned reading is Figs. 1 and 2). Added for the
same reason as §21.

### 22.1 The split, and the claim that makes it a division of labor

QUOTED, abstract: the synthetic pathway for "the acetylated diol paclitaxel
precursor" was divided "into two modules, expressed in either *S. cerevisiae*
or *E. coli*, **neither of which can produce the paclitaxel precursor on their
own**". *E. coli* makes **taxadiene**; yeast oxygenates it (yeast carries
5αCYP-CPR, a P450).

QUOTED, abstract: "Stable co-culture in the same bioreactor was achieved by
designing a **mutualistic relationship** between the two species in which a
metabolic intermediate produced by *E. coli* was used and functionalized by
yeast." Headline: **33 mg/L oxygenated taxanes**, including a monoacetylated
dioxygenated taxane. The method was also applied to tanshinone precursors and
functionalized sesquiterpenes.

### 22.2 Version one — the co-culture on glucose, and why it fell over

MEASURED, p.3 and Fig. 1:

- Taxadiene made by *E. coli* **does** cross into yeast and get oxygenated: a
  yeast-only control made no oxygenated taxanes.
- But *E. coli* cell density (Fig. 1c) and total taxane titer (Fig. 1d) "were
  significantly reduced in the presence of *S. cerevisiae*".
- **The mechanism is ethanol, not the yeast as such.** On glucose the yeast
  makes ethanol (Fig. 1e); ethanol at the highest observed concentration,
  **50 g/L**, "completely inhibited *E. coli* cell growth and taxadiene
  production". That validation is in **Supplementary Fig. 2**, which this repo
  does not hold — `[unverified]` as to the dose–response, QUOTED as to the
  claim.
- Oxygenated taxanes in this version: **2 mg/L in 72 h** (Fig. 1b). MEASURED.

> **Say "the ethanol the yeast makes on glucose", not "the yeast".** The
> paper's own causal chain runs carbon source → ethanol → *E. coli*
> inhibition, and the fix in §22.3 works by removing the ethanol, not by
> removing the yeast. A slide that says "the yeast inhibits *E. coli*" loses
> the step that the next design acts on. INFERRED BY US from the paper's own
> order of argument.

### 22.3 Version two — xylose and acetate, and what it bought

QUOTED/MEASURED, p.3 and Fig. 2:

- "When *E. coli* metabolizes xylose it excretes acetate, which is inhibitory
  to its own growth. *S. cerevisiae*, on the other hand, cannot metabolize
  xylose but can use acetate as the sole carbon source for growth **without
  producing ethanol**."
- So the carbon source was switched from glucose to **xylose**, and then
  **yeast grew only in the presence of *E. coli*** (Fig. 2b).
- Extracellular acetate fell against *E. coli* alone on xylose (Fig. 2c).
- Ethanol went **below the 0.1 g/L detection limit** throughout.
- Total taxanes from *E. coli* were "not substantially affected by the presence
  of *S. cerevisiae*" (Fig. 2d).

**The dependency runs both ways, and each direction removes the other's
problem.** Yeast gets its only carbon source from *E. coli*; *E. coli* gets its
own growth inhibitor removed by the yeast. DERIVED from the two statements
above.

**And the honest number: the yield barely moved.** Oxygenated taxanes
**4 mg/L in 72 h** (Fig. 2e) against **2 mg/L in 72 h** before, with taxadiene
oxygenation efficiency still "only 8 % of total taxadiene produced". MEASURED.
**Stability was what version two bought, not titer.**

### 22.4 The rest of the chain, for anyone tempted to quote 33 mg/L as version two's number

MEASURED, pp.3–4, Figs. 3 and 4. Each step is a separate piece of engineering:

| step | what was changed | oxygenated taxanes |
|---|---|---|
| glucose co-culture | — | **2 mg/L / 72 h** |
| xylose–acetate mutualism | carbon source | **4 mg/L / 72 h** |
| more yeast, fed nutrients | larger yeast inoculum; periodic xylose, ammonium, phosphate | **16 mg/L / 90 h** (~3× ) |
| stronger yeast promoter | **UAS-GPDp** in place of TEFp (strain TaxS4) | **25 mg/L / 90 h** |
| *E. coli* forced to make acetate | **atpFH knockout** — oxidative phosphorylation inactivated, so acetate becomes the primary ATP route (strain TaxE4) | **33 mg/L / 120 h**, up to **75 %** of taxadiene oxygenated |

Supporting numbers: TaxE4 made **5.0 ± 0.1 g/L** acetate in a test tube against
**2.3 ± 0.2 g/L** for the parent TaxE1. Overexpressing `pta` and `ackA` first
"neither increased the *S. cerevisiae* population density nor the oxygenation
efficiency substantially" (Supplementary Fig. 4, not held — `[unverified]`).

**The ratio became self-regulating, and this is the sharpest thing in the
paper for this session.** QUOTED, p.4: the inoculum ratio of yeast to *E. coli*
was set at about **40:1**, which "eliminated the inhibitory acetate levels, but
did not result in yeast overpopulation, because yeast growth was strictly
limited by the concentration of acetate produced by *E. coli*, leading to a
balanced ratio of the two species (the ratio of yeast to *E. coli* was **1:2 at
41 h**)" — "and this ratio was controllable through altering the specific
acetate productivity". MEASURED.

QUOTED, p.4, the authors' own summary of the design: "We applied additional
genetic and growth constraints to **enforce this cooperation** — for instance,
the respiration-deficient *E. coli* was forced to produce acetate as this was
its primary way to generate cellular ATP, and the yeast also had to consume
acetate because it cannot utilize xylose."

### 22.5 What is NOT claimed from this paper

- **No comparison against a single-organism control that works.** Neither
  organism can make the product alone, which is the premise, so this paper
  cannot be used as evidence that splitting beat not splitting. It is evidence
  about what a split costs once you are committed to it. INFERRED BY US.
- **No model.** There are no equations and no parameters, so it cannot be put
  against TSOI's criterion quantitatively. The two are a pair only
  rhetorically.
- Supplementary Figs. 2, 3, 4, 8 and 9 and Supplementary Table 1 are cited
  above and **none is held**. Every `[unverified]` in this section traces
  there.

---

### 20.6 The QSSA is not merely lossy here — it is unlicensed by its own criterion

**DERIVED BY US, 8 November 2026**, from §20.1's QUOTED constants. Arithmetic
only; no new source.

A quasi-steady-state elimination requires the eliminated variable to be
**fast** relative to what it couples. The signals' relaxation rate is
`d_AA + D`; the populations' rate is `k_c`:

| signal | d_AA + D | population rate k_c | k_c / (d_AA + D) |
|---|---|---|---|
| A₁, from the predator | 0.017 + 0.1125 = **0.1295 /h** | k_c1 = 0.800 /h | **6.18** |
| A₂, from the prey | 0.110 + 0.1125 = **0.2225 /h** | k_c2 = 0.400 /h | **1.80** |

The QSSA needs that ratio far below 1. **Both exceed it**, so at the deposit's
own parameters the signals are about 6× and 1.8× **slower** than the
populations they couple — the wrong side of 1, and for A₁ by more than half an
order of magnitude.

**Why this matters for how move 4 is taught.** The design's move 4 says the
QSSA "threw the oscillation away", which is true and is a statement about the
outcome. This is a statement about the *premise*: the approximation's own
validity condition fails here, and the division that shows it is two
subtractions and two divisions on constants the paper deposited. So the honest
lesson is not "an approximation cost us a phenomenon" but **"we applied an
approximation outside the regime that licenses it, and the phenomenon was what
it cost"** — which is a transferable habit rather than an anecdote, and it
gives session 4's QSSA redraw something to check itself against.

Verified against `posb.communities.pp_params(iptg=5.0)`. Note this is OURS, not
Balagaddé's: the paper does not discuss the QSSA at all, and the reduction is
the course's own construction.

---

## 23 · Findings from the rendered panels, at crop time — 7 November 2026

The week-13 crops were cut from 450–900 dpi renders and every panel was
looked at. Two things turned up that are invisible in `pdftotext` and that
constrain what a slide may ask. Both are MEASURED on the render.

### 23.0 A sub-crop of Fig. 3C, for slide 69 — added 8 November 2026

**`balagadde2008_fig3c_main` is a strict sub-region of `balagadde2008_fig3c`**,
box (1117, 1574)–(2591, 2199) of page 5 at 450 dpi against the full crop's
(1117, 1574)–(2591, 2604). It carries the main panel and the period inset and
drops the three time courses below them. **No ink is altered, added or
rearranged** — it is the same raster, cut shorter — so this is not an
alteration of the kind §23.4 governs, and it is recorded here rather than
there.

**Why.** Slide 69 is the one slide in the session whose instruction needs the
small type: it asks the room to read the panel from its axes, and to notice
that the main axes are predator cells while **only the inset is period**.
Measured on the rendered PDF, the full crop's main x-label projects at about
**6.1 pt** and the inset's labels at **4.9 pt**, against the deck's 20 pt
floor. In the full crop the slot is height-bound; dropping the unused time
courses lets it run width-bound, which magnifies what matters by about 1.6×.

**On resolution, since enlarging a crop usually makes things worse.** It does
not here, and the reason is worth stating because it is the opposite of the
Weinberger Fig. 2a case. Checked 8 November: **the source page is a 300 ppi
raster** (`pdfimages -list`: page 5 object 0, 2480×3309 at 300×300), so the
450 dpi crop was already a 1.5× upsample and there is no further detail to
extract. But the limiting quantity for legibility is **pixels per glyph**, not
ppi per slide, and that is unchanged by magnification. Inspected at 2×, the
axis digits and the `D (h⁻¹)` label have clean, well-resolved edges. So the
same pixels are simply shown larger, and the type becomes legible from the
back of the room without becoming blurred. Contrast Weinberger Fig. 2a, whose
embedded legend is **not** well resolved at source — there, enlarging enlarges
the blur, which is why that one is being redrawn from the model instead.

**Citation.** The panel letter **C** is inside this crop, so a slide citing it
says **Fig. 3C**, not 3a. The caption-versus-axes trap recorded for the full
crop applies here unchanged: the printed caption calls it a bifurcation
diagram of oscillatory period versus D, and the main axes are predator cells
versus D. **Describe it from the axes.**

### 23.1 Basu Fig. 2d has a SECOND, independent axis problem

§8.3 records that the digitized AHL positions in Basu Fig. 2 are wrong by a
uniform factor of 6.8, traced to a tick misplacement of about 0.83 of a decade.
That is not the only problem with those axes.

Measured on a 900 dpi render of both panels:

- **Neither panel b nor panel d has major ticks.** The x-axis tick comb is
  uniform in length (23–28 px) and dense enough to form a continuous band from
  one end of the axis to the other. **There is nothing a digitizer can key on
  to locate a decade.** The only positional anchor anywhere on the axis is the
  printed label text.
- Label pitch, measured on the identical "10" glyph pair so the comparison is
  direct: **panel b = 248, 247, 247, 259, 247 px**, even throughout.
  **Panel d = 248, 247, 247, 259, 207 px** — the final gap, 10⁰ to 10¹, is
  about 40 px short, so **panel d's 10¹ label sits roughly 0.16 of a decade
  left of where its own even spacing puts it.**

0.16 of a decade is a different magnitude from the 0.83 that produced the 6.8×
error, so this looks like a **second, independent defect rather than the same
one seen again.** MEASURED; the inference that they are independent is
INFERRED BY US.

**Consequence, and it is the same as §8.3's:** no absolute AHL position from
Basu Fig. 2 may appear on a slide or in a problem-set item. Every number comes
from the printed parameters through `posb.band_detect_response`, which
reproduces the peak heights to 1 part in 2,500 and the spacings to 0.5%. The
session teaches **ordering and spread**, which are sound. This finding
strengthens that decision rather than changing it.

### 23.2 Balagaddé Fig. 2C's bottom row does not separate predator from prey

The three simulated time courses along the bottom of Fig. 2C **render in a
single dark-red ink.** The predator/prey colour legend printed beside them does
**not** distinguish the two traces in that row. The bifurcation panel above it
does render predator in blue, so the legend is not wrong about the figure as a
whole — it simply does not apply to the bottom row.

**So no slide may ask the room to read predator from prey by colour in that
row, and no speaker note may describe those traces as colour-coded.** MEASURED
on the render. If the session needs a two-colour predator/prey time course, it
comes from `posb.predator_prey_model`, where the two states are ours to colour.

### 23.3 Two numbering traps, already handled but worth stating once

- **Balagaddé's Box 1 is a boxed inset, not its Figure 1.** The paper numbers
  Figures 1–3 separately and **does** have a Figure 1 — the liquid-culture
  growth controls at §3.1, p.3. A slide calling the circuit schematic "Fig. 1"
  would be naming the wrong object. Say **Box 1A**. §3.1 and the crop keys are
  already correct on this; the trap is for a later pass.
- **Balagaddé Fig. 3C's caption contradicts its own axes.** The caption reads
  as a bifurcation diagram of oscillatory *period* versus D, but the main
  panel's axes are **predator cells** versus D; it is the **inset** that is
  period versus D. §3.4 already splits these correctly. Describe the panel from
  its axes, never from its caption.

### 23.4 Three crops carry a documented alteration

Basu 2b, Basu 2d and Noble 2d interlock with a neighbouring panel such that no
vertical cut separates them, so in each a provably foreign glyph was whited
out — panel d's letter intruding on 2b, panel b's tick-row tail running under
2d, and panel E's letter sitting at the height of panel D's axis title. In each
case the blanked rectangle was verified numerically to contain **zero ink
belonging to the panel being cropped**, and the exact rectangle is recorded in
that key's `provenance` field in `decks/paper_figures.yaml`. The alternative
was losing either a panel letter or an axis title. Recorded here because an
altered published figure on a slide is the kind of thing that must be
discoverable later without reading a YAML file.

### 23.5 Four crops must not be scaled past about half a slide

Their sources are low-resolution embedded raster, not vector:
`basu2005_fig3b`, `_fig3c`, `_fig5b`, `_fig5c`, `_fig5d` (220 ppi),
`tsoi2018_fig2d` (200 ppi), and `noble2018_fig2d`, whose heat map is 358×358 at
300 ppi although its axes are vector. Each carries the warning in its key's
note. MEASURED.
