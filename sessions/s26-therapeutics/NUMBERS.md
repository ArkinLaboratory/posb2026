# Session 26 — Therapeutic circuits · NUMBERS

**Tue 24 Nov. Worked example: design a multi-input classifier to a false-positive
budget. Techniques T69 (AUTO, PS9 + final) and T70 (HAND, PS9).**

Reading: Xie, Z., Wroblewska, L., Prochazka, L., Weiss, R. & Benenson, Y.
*Multi-Input RNAi-Based Logic Circuit for Identification of Specific Cancer
Cells.* Science **333**(6047), 1307–1311 (2011). doi:10.1126/science.1205527

On disk: `private/readings/Session 26 - xie-2011-multi-input-rnai-logic-circuit-cancer-classifier.pdf`
(main article, 6 pp.) and `private/readings/Session 26 - xie-2011-SOM.pdf`
(supplementary, obtained 8 November 2026).

---

## 0 · Sourcing, and one thing to get right before anything is built

The standing rule applies: every number on a slide traces to a printed,
rendered source and is marked **MEASURED / QUOTED / MODELLED / DIGITIZED /
INFERRED BY US**. A number that cannot be sourced cannot ship.

### 0.1 The supplement does NOT contain the sensor-response values — checked 8 November 2026

**This reverses the assumption the session was scoped on, so it is recorded
first.** Fig. 2D's caption reads "miRNA marker sensor responses in different
cell lines **(tables S1 and S3)**", which was taken to mean S1 and S3 hold the
measured values. They do not.

Read from the SOM's own text layer, all six tables are **methods**:

| table | what it actually is |
|---|---|
| **S1** | "Transfection configuration for samples used to generate some of the data shown in Fig. 2D and all data in fig. S4." Nanogram plasmid amounts per construct. |
| **S2A / S2B** | Plasmids used to construct circuit variants; transfection configuration for fig. S6. |
| **S3A** | "The plasmids used to construct different circuit variants." |
| **S3B** | "Transfection configuration for the experiments shown in Fig. 2D (HeLa-high sensors), Fig. 3 and fig. S8." Nanogram amounts. |
| **S4 / S5** | Transfection configuration for Fig. 4 and fig. S7. |
| **S6** | Oligonucleotide sequences. |

So the caption's "(tables S1 and S3)" points at **how those experiments were
built**, not at the data. **There is no table of measured sensor responses
anywhere in the supplement.** The 7 cell lines × 5 sensors = 35 values exist
only as **bar heights in Fig. 2D**, with no numeric labels on or above any bar
(checked at 600 dpi).

**Consequence: T69 is a DIGITIZED build.** Fig. 2D needs a digitization pass
like session 25's, and every value carries the DIGITIZED mark. The supplement
does not change that, and obtaining it did not upgrade a single number to
QUOTED. This is not the session 24 situation — nothing has to be rebuilt on a
model — but the distinction must be honest on the slides and in the autograder.

**What the supplement IS good for:** full methods provenance (cell lines with
ATCC numbers, culture, transfection and nucleofection protocols, flow cytometry
instruments), fig. S4's three independent replicates behind Fig. 2D's error
bars, fig. S8's circuit diagrams, and the cell-line descriptions in §0.2.

### 0.2 The classifier is not a cancer detector, and the room will assume it is — QUOTED (SOM, cell-line list)

The paper's title says "Specific Cancer Cells", and the SOM lists what the
seven lines are:

- **HeLa** — cervical cancer (the one POSITIVE)
- **MCF7** — breast cancer
- **SKBR3** — breast cancer
- **T47D** — breast cancer
- **DAOY** — brain cancer
- **SH-SY5Y** — brain cancer
- **HEK293** — human embryonic kidney

**Six of the seven are cancer lines, and five of the six negatives are
cancer.** So the circuit does not separate cancer from healthy tissue; it
separates **one cell type from six others**, five of which are also cancer.
A false positive here is *the wrong cancer*, not *a healthy cell*.

That is the sharpest thing available for the false-positive budget, and it is
free: it needs no digitization, it comes straight off the SOM's own list, and
it corrects the reading a student brings to the title. Worth putting in front
of the room before any arithmetic.

### 0.3 Printed in the main article, usable without digitizing

- **The Boolean expression — QUOTED (p.1308, and across the top of Fig. 2E):**
  miR-21 AND miR-17-30a AND NOT(miR-141) AND NOT(miR-142(3p)) AND NOT(miR-146a).
- **Five sensor modules, six markers** — miR-17 and miR-30a share one composite
  HeLa-high sensor, so Fig. 2D's legend shows five series. A student counting
  bars finds five and must not conclude they have misread.
- **The false-positive definition — QUOTED (Fig. 2A caption, p.1309):** "the
  contour line shows input combinations that result in 20% output relative to
  HeLa cells (red dot). Dots above the contour line represent 'false-positive'
  cell types for this specific circuit configuration."
- **No sensitivity, specificity, FPR or FNR appears anywhere in numeric form.**
  The only false-positive sentence is qualitative (p.1311).
---

## 1 · How every number below was obtained — and why it is not pixel digitization

**Read this before using anything in §2–§6.** The method is different from
§19 of `s25-populations/NUMBERS.md`, and it is better.

### 1.1 The panels are vector art, not images

`pdfimages -list` on the main article returns 34 embedded rasters. Every one of
them is a micrograph or a flow-cytometry dot plot. **Not one bar chart is an
image.** The bars are filled rectangles in the PDF content stream, the axis tick
marks are filled rectangles or stroked lines, and all of it carries coordinates
to three decimal places of a point.

So these values were not read off a render. They were read out of the page's own
geometry with `pdfminer.six`. A 600 dpi render resolves 0.12 pt; the content
stream resolves 0.001 pt. **The limiting error is no longer our reading of the
figure — it is the draughtsmanship of the figure itself**, and that is measured
and reported for every panel below as the tick-fit residual.

The digitizer is `_scratch/s26_xie/digitize_xie2011.py`. It is runnable, it
takes the PDF path as its one argument, and it writes
`_scratch/s26_xie/xie2011_digitized.{json,csv}`. Every table in §2–§6 is
generated from that JSON by `_scratch/s26_xie/emit_numbers_md.py`; no value in
this file was typed by hand. Any future argument about what one of these panels
says can be settled by re-running it.

### 1.2 Calibration — stated, as the house style requires

For each panel the **y-axis tick marks** are located (never the glyph bounding
boxes of the tick labels, never a bar count, never a guessed baseline), each
tick centre is paired with its printed label, and value → y is fitted by
ordinary least squares. The residuals are the panel's own drafting jitter:

| panel | axis | ticks used | pt per unit | max residual (pt) | max residual (in axis units) |
|---|---|---|---|---|---|
| **Fig. 2D** | Sensor response, rel. u. | 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2 | 53.15679 | 0.0011 | 0.00002 |
| **Fig. 2C left** | Minimal ratio (fold) | 0, 2, 4, 6, 8, 10 | 4.11696 | 0.0007 | 0.00017 |
| **Fig. 2C right** | Average ratio (fold) | 0, 40, 80, 120, 160, 200 | 0.20585 | 0.0004 | 0.00204 |
| **Fig. 3C left** | % AmCyan+ cells | 0, 3, 6, 9, 12 | 4.20532 | 0.1427 | 0.03393 |
| **Fig. 3C right** | Killing efficiency, r. u. | 0, 0.5, 1.0 | 43.02200 | 0.1230 | 0.00286 |
| **Fig. 4A** | DsRed+ cells (count) | 0, 1000, 2000, 3000, 4000 | 0.01315 | 0.1319 | 10.02996 |
| **Fig. 4B** | DsRed+ cells (count) | 0, 500, 1000, 1500, 2000, 2500 | 0.02105 | 0.1235 | 5.86552 |

Fig. 2D's ticks are uniform to **0.0011 pt — two parts in 10⁵ of a sensor-response
unit.** That panel is, for our purposes, exact. The three count/percentage panels
are jittery at the 0.12–0.14 pt level, which is 6–10 cells on Fig. 4A/4B and
0.03 percentage points on Fig. 3C(left). That jitter, not our method, sets the
precision of §5 and §6.

### 1.3 The zero, and why we report bar HEIGHT

In Figs. 3C, 4A and 4B the bar rectangles are drawn translated upward from the
frame the ticks define, by half the axis stroke width — Fig. 4B's bars sit at
y = 82.719 while the zero tick's centre is y = 82.5535, a gap of 0.1655 =
0.331/2. The translation moves a bar's bottom and its top equally, so **it
cancels in the height**, and we report

    value = (bar_top − bar_bottom) / scale

**This is checked, not assumed.** The error bars are drawn on the untranslated
frame, so `(error-bar centre − zero tick)` must reproduce the same number. Both
are in the JSON as `value` and `value_from_errbar_centre`. In Fig. 2D they agree
to **0.00003 rel. u.**; in Fig. 4B to **2.3 cells in 1900**; in Fig. 3C(left) to
**0.05 percentage points**. Had we taken the tick-centre zero and the bar top
instead, every Fig. 4B count would be low by about 8 cells.

### 1.4 Error bars

Each error bar is a vertical line with a cap rectangle at both ends; the
half-length is the plotted SD. The captions say these are **mean ± SD over three
independent replicates** (Fig. 2D caption, p.1309: "Bars show mean ± SD of
normalized sensor output measured in three independent flow cytometry
experiments (fig. S4)"; Fig. 3C and Fig. 4 captions, p.1310, likewise). They are
SDs of n = 3, **not** SEMs, and nothing below treats them as SEMs.

Where only the upper cap is drawn, the lower arm ran below zero and was clipped
at the axis. That happens exactly once, and it matters — see §4.

### 1.5 The vector method is cross-checked against ordinary pixel digitization

The vector method is not trusted on its own say-so.
`_scratch/s26_xie/crosscheck_pixel.py` re-reads the same bars by **ordinary
pixel digitization of a 600 dpi render**, calibrated against the same printed
ticks, and compares.

**Fig. 4B — they agree.** Sampling a column 20% in from each bar's left edge,
clear of the error bar, all six bars match the vector reading to within
**7.8 cells**, which is 1.4 pixels at 600 dpi.

**Fig. 2D — they agree only after a trap is removed, and the trap is worth
recording.** Sampling at the bar's *centre*, pixel digitization comes out **low
on every bar, by almost exactly that bar's SD**, because the black error bar is
drawn over the bar top and the topmost bar-coloured pixel is the bottom of the
error bar's lower arm:

| cell line | sensor | vector | naive pixel read at bar centre | error | that bar's plotted SD |
|---|---|---|---|---|---|
| DAOY | T141 | 0.96052 | 0.94859 | -0.01192 | 0.01248 |
| HeLa | P21 | 0.93251 | 0.86732 | -0.06518 | 0.06609 |
| HEK293 | T146a | 1.23044 | 1.20143 | -0.02901 | 0.02986 |
| MCF-7 | T141 | 0.10571 | 0.10204 | -0.00367 | 0.00293 |

Add the SD back and the two methods agree to **0.00090 rel. u.** The point is not
that pixel digitization cannot be done here — it is that **on this figure the
obvious way to do it is wrong by up to 0.065 rel. u., 7% of the value, on HeLa's
own P21 bar**, and wrong in the direction that makes HeLa look like a weaker
positive than it is. The vector route has no such failure mode.

### 1.6 One claim of absence, settled exhaustively rather than by resolution


§0.1 records that Fig. 2D carries no numeric labels, checked at 600 dpi. That is
now settled better than any render can settle it: **the PDF text layer contains
zero glyphs inside Fig. 2D's plotting rectangle** (x 359–557, y 385–455 on
p.1309). The text layer is exhaustive, so this is not a resolution-limited
claim. §0.1 stands.

---

## 2 · Fig. 2D — the response matrix, all 35 values — DIGITIZED, 8 November 2026

Seven cell lines × five sensor modules. Axis "Sensor response, rel. u.", ticks
0 / 0.2 / … / 1.2. Calibration: the seven tick marks at x 357.781–358.993 on
p.1309, y = 384.336 / 394.967 / 405.598 / 416.230 / 426.860 / 437.493 / 448.124,
fitted at **53.15679 pt per unit**, residual ≤ 0.0011 pt. Bar bottoms all sit on
y = 384.336, which is the fitted zero to 0.0004 pt.

Series identity is not inferred from bar order. Each legend swatch's fill colour
was matched to its bar's fill colour exactly: P21 = (0.569, 0.714, 0.851),
P17-30a = (0.141, 0.416, 0.659), T141 = (0.8, 0.494, 0.494),
T142(3p) = (0.894, 0.251, 0.271), T146a = (0.745, 0.118, 0.176). Group identity
comes from the seven x-axis separator ticks, each of which brackets exactly one
printed cell-line label.

### 2.1 CONVENTION — read this before the table, or the numbers will be wrong

**These 35 values are SENSOR OUTPUTS as published. They are NOT marker levels.**

Every one of Fig. 2D's five series is oriented so that **HeLa reads high**,
including the three T-sensors. Digitized, HeLa's row is P21 0.933, P17-30a 0.717,
T141 0.894, T142(3p) 0.849, T146a 0.854 — high in all five. T141, T142(3p) and T146a read
high in HeLa precisely *because* HeLa lacks miR-141, miR-142(3p) and miR-146a:
**the three NOT terms of the Boolean expression are already applied inside the
sensors.**

So a consumer that takes normalized marker levels — where 1.0 means the marker
is PRESENT, and a `sense="absent"` marker contributes `1 − r` — **must convert at
the data boundary.** `posb.classifiers.marker_levels_from_sensor_outputs` exists
for exactly that. Feed these bars in as marker levels and the three inversions
are applied **twice**, silently, and the classifier stops working.

**That conversion is a modelling step, not bookkeeping.** `1 − r` inverts an
*idealized* sensor. A real RNAi sensor has leak, a ceiling below 1 and a slope
that is not 1, and all three get absorbed into whatever "marker level" comes out
the other side. Anything derived through that conversion is MODELLED, not
DIGITIZED, and must be marked so.

**The decisive check, and it settles the question rather than leaving it to
judgement.** Under the correct reading, the bare product of the five sensor
outputs is the circuit's output and **HeLa must be the maximum across all seven
lines**. Computed from the unrounded geometry behind the table below, one
multiplication per line:

| reading | winner | value | runner-up | value |
|---|---|---|---|---|
| **as sensor outputs (correct)** | **HeLa** | 0.433555 | T47D | 0.293775 |
| as if they were marker levels (double inversion) | **SKBR3** | 0.002029 | HeLa | 0.001561 |

**HeLa wins by 1.48× when the bars are read as sensor outputs.** Read as marker
levels, **SKBR3 wins and HeLa comes second** — the classifier silently picks the
wrong cell line. There is no judgement call here; the matrix is in the sensor-
output convention.

Full ordering as sensor outputs: HeLa 0.4336, T47D 0.2938, SKBR3 0.1654, DAOY 0.0503, MCF-7 0.0420, SH-SY5Y 0.0238, HEK293 0.0011.

**Those products come from the unrounded geometry, not from §2.2's table, and
the difference is worth one line so that nobody chases it.** §2.2 publishes the
matrix to three decimals, which is the only version a reader ever sees.
Multiplying the published table instead, in exact rational arithmetic:

| source of the five factors | HeLa | T47D | ratio |
|---|---|---|---|
| unrounded digitizer geometry | 0.433555 | 0.293775 | 1.475807 |
| §2.2's published three decimals | 0.433615 | 0.293949 | 1.475135 |

That is +0.000060 on HeLa, +0.000174 on T47D and -0.000672 on the ratio.
Neither pair is wrong and they answer different questions: the first is what
the figure's geometry says, the second is what a reader can reproduce. **§2.2's
table is the normative one** — the line at the end of §2.2 says so — so a
student who multiplies the published matrix and gets 0.433615 has done it
correctly, and any check against 0.433555 needs a tolerance wider than
0.000060.

**No marker-level version of this matrix is recorded in this file.** If one is
needed, derive it in the library through `marker_levels_from_sensor_outputs`,
mark it MODELLED, and never put it in the same table as the values below.

### 2.2 The matrix

**Values. SENSOR OUTPUTS, rel. u. All DIGITIZED.**

| cell line | P21 | P17-30a | T141 | T142(3p) | T146a |
|---|---|---|---|---|---|
| **DAOY** | 0.420 | 0.429 | 0.961 | 0.697 | 0.417 |
| **HEK293** | 0.010 | 0.078 | 1.106 | 0.993 | 1.230 |
| **HeLa** | 0.933 | 0.717 | 0.894 | 0.849 | 0.854 |
| **MCF-7** | 0.931 | 0.405 | 0.106 | 1.019 | 1.033 |
| **SH-SY5Y** | 0.090 | 0.242 | 1.072 | 0.963 | 1.063 |
| **SKBR3** | 0.525 | 0.755 | 0.544 | 0.817 | 0.938 |
| **T47D** | 0.560 | 0.690 | 0.789 | 0.994 | 0.970 |

**Plotted SD (n = 3). DIGITIZED.**

| cell line | P21 | P17-30a | T141 | T142(3p) | T146a |
|---|---|---|---|---|---|
| **DAOY** | 0.051 | 0.013 | 0.012 | 0.012 | 0.016 |
| **HEK293** | — | 0.012 | — | 0.013 | 0.030 |
| **HeLa** | 0.066 | 0.074 | 0.024 | 0.014 | 0.007 |
| **MCF-7** | 0.064 | 0.037 | — | 0.085 | — |
| **SH-SY5Y** | 0.028 | 0.027 | 0.069 | 0.055 | 0.038 |
| **SKBR3** | — | 0.081 | 0.023 | 0.083 | 0.047 |
| **T47D** | 0.031 | 0.136 | 0.038 | 0.080 | 0.041 |

**Five SDs are marked — and left out. This is a finding, not a gap.** In those
five bars the drawn error bar is shorter end-to-end than the figure's own line
weight (0.459 pt), so it is not distinguishable from a dot at any resolution:

| cell line | sensor | drawn 2·SD (pt) | implied SD (rel. u.) |
|---|---|---|---|
| HEK293 | P21 | 0.044 | 0.00041 |
| HEK293 | T141 | 0.439 | 0.00413 |
| MCF-7 | T141 | 0.311 | 0.00293 |
| MCF-7 | T146a | 0.083 | 0.00078 |
| SKBR3 | P21 | 0.475 | 0.00447 |

Their **means are sound** and are given in the table above; only the SDs are
withheld. A problem set or autograder may use all 35 means; it may not use these
five SDs. Do not interpolate them.

**Three things in this matrix are worth a slide.**

- **HEK293's P21 response is 0.010 — the lowest value in the matrix**, and its
  T141 and T146a are the two highest (1.106, 1.230). HEK293 is the clean
  inverse of HeLa on three of the five sensors. That is the paper's own
  explanation for why the circuit works there (p.1309), and the numbers carry it.
- **HeLa is nowhere near 1.0 on its own high sensors** — P21 is 0.933 and
  P17-30a is 0.717. The classifier's positive is not a saturated positive.
- **SKBR3 and T47D are the dangerous lines, and the matrix says so before any
  circuit arithmetic.** Every one of their ten responses sits between 0.52 and
  0.99 — no inverse anywhere, just moderate deviation. The paper says exactly
  this (p.1309, "a sufficient number of responses deviate moderately"), and
  these are the two lines a student should expect to be hardest to reject.

**These three-decimal values are normative for the session.** The deck, the
problem set and the T69 autograder are built on this table, because it is the
only version of the matrix a student can see and reproduce. The digitizer's
unrounded geometry gives slightly different products, and §2.1 prints both
pairs; it is not published here. So anything that checks a student's arithmetic
checks it against this table, with a tolerance no tighter than 0.001 on a
product of five responses and 0.002 on a ratio of two such products.

### 2.3 No single sensor identifies HeLa — DERIVED from §2.2, no new digitization

Every number in this subsection is computed from §2.2's means. Nothing was
digitized for it, so it carries no DIGITIZED mark of its own — the provenance
is §2.2's, and the arithmetic is the only thing added.

Count, for each sensor, how many of the six negative lines read **higher** than
HeLa does on that sensor:

| sensor | HeLa | negatives above HeLa | which |
|---|---|---|---|
| **P21** | 0.933 | 0 | — |
| **P17-30a** | 0.717 | 1 | SKBR3 0.755 |
| **T141** | 0.894 | 3 | HEK293 1.106, SH-SY5Y 1.072, DAOY 0.961 |
| **T142(3p)** | 0.849 | 4 | MCF-7 1.019, T47D 0.994, HEK293 0.993, SH-SY5Y 0.963 |
| **T146a** | 0.854 | 5 | HEK293 1.230, SH-SY5Y 1.063, MCF-7 1.033, T47D 0.970, SKBR3 0.938 |

**On four of the five sensors HeLa is not the highest line in the panel**, and
on T146a five of the six negatives sit above it. The one sensor where HeLa
leads every negative is P21, and it leads by nothing that survives the error
bars: HeLa **0.933 ± 0.066** against MCF-7 **0.931 ± 0.064**, a gap of
**0.0019** rel. u., which is **0.029 of HeLa's own plotted SD**.

**That gap is far above our reading error and far below the measurement's
own.** It is 96× Fig. 2D's maximum calibration residual (§1.2: 0.00002 rel.
u.), so the ordering is real *in the drawn figure* — the artwork does put HeLa
above MCF-7, and §1.5's cross-check means that is not an artifact of how the
bars were read. What makes the ordering meaningless is the error bars, not the
digitization. Those are two different failures and keeping them apart is what
this file is for.

**The identification of HeLa lives in the product and nowhere else.** §2.1's
five-sensor product puts HeLa first by 1.476× over T47D. Remove one sensor at a
time and the margin does not merely shrink:

| configuration | argmax | runner-up | margin |
|---|---|---|---|
| all five | HeLa | T47D | 1.476× |
| drop P21 | **T47D** | HeLa | 1.128× |
| drop P17-30a | HeLa | T47D | 1.419× |
| drop T141 | HeLa | MCF-7 | 1.221× |
| drop T142(3p) | HeLa | T47D | **1.728×** |
| drop T146a | HeLa | T47D | **1.677×** |

**Dropping P21 inverts the call.** T47D becomes the argmax and HeLa comes
second, by 1.128×. The classifier's answer on this panel therefore turns on a
single sensor whose own HeLa-against-MCF-7 lead is 0.029 of an SD. And two of
the five markers *reduce* the margin here: without T142(3p) it rises to 1.728×
and without T146a to 1.677×.

**None of this depends on the normalization, and that is algebra rather than an
observation about this panel.** `normalize_responses` divides each marker's
column by that column's maximum across the panel. Write cₘ for the maximum of
column m; each line's product becomes

    ∏ₘ r(line, m) / cₘ  =  (1 / ∏ₘ cₘ) · ∏ₘ r(line, m)

and the factor 1 / ∏ₘ cₘ is the same for every line in the panel. A factor
common to all seven lines changes no argmax and no ratio between two lines, so
the margins above and §2.1's 1.48× are identical before and after
normalization. The numerical check: the five column maxima are 0.933, 0.755,
1.106, 1.019, 1.230, whose product is **0.976422**, and §2.1's raw HeLa product
0.433555 divided by it is **0.444024** — which is what `normalize_responses`
followed by `classifier_output` returns on this table. (The library will not
take §2.2's values unnormalized; several exceed 1.0, which is what its range
check is there for.)

Computed at the digitizer's full precision. Recomputing from §2.2's printed
three-decimal values moves no margin above by more than 0.0013 and changes no
argmax.

**This is not an argument for dropping markers, and the paper's own selection
criterion says why — QUOTED (p.1308).**

> "A HeLa reference profile was constructed by choosing a set of HeLa-high and
> HeLa-low markers so that HeLa cells express high or low levels of these,
> respectively, whereas expression **in any healthy cell** differs substantially
> from that of a typical HeLa cell for at least one of these markers. Multiple
> reference profiles are possible, and **these profiles do not need to
> differentiate HeLa from other cancers.**"

Two things in that sentence dispose of the pruning reading. The criterion is
"any healthy cell", and the candidates came from a different cell set
altogether — "the top 12 candidates determined by analyzing expression data
from the MicroRNA Atlas (fig. S3)" (p.1308). Against that, §0.2 records that
six of Fig. 2D's seven lines are cancer lines and five of its six negatives
are. So the counts above score the markers on exactly the comparison the
authors declined to design for.

The HeLa-low markers have their own stated target — QUOTED (p.1308):

> "We then searched for HeLa-low markers and found that miR-141, miR-142(3p),
> and miR-146a are highly expressed in the potentially misclassified cell types
> but unexpressed in HeLa (Fig. 2B)."

The "potentially misclassified cell types" are the Atlas cell types the
two-marker miR-21 + miR-17-30a circuit failed on, not the six negatives of Fig.
2D. A marker selected to exclude cell types absent from this panel contributes
nothing to the margin on this panel and still belongs in the circuit. That is
the structural reason T142(3p) and T146a can raise the margin when they are
removed without being poor markers, and it needs no claim about which miRNA
marks which lineage — this file makes none.

§3's Fig. 2C data point the same way: selectivity keeps improving as markers
are added, over the cell set the markers were chosen against, and §3.2 records
that the dip there is real and that the caption's minimax objective accounts
for it.

**So this subsection establishes something narrower than it first reads.** On
these seven adherent cultured lines no single sensor separates HeLa, and the
separation is a property of the product. It does not follow that any marker is
redundant, because the panel on which a marker would earn its place is not this
one.

---

## 3 · Fig. 2C — selectivity against marker count — DIGITIZED, anchored by printed prose

Two series against markers 1–6: **Minimal ratio (fold)** on the left axis
(0–10) and **Average ratio (fold)** on the right (0–200). Marker centres were
taken as the centroid of each plotted glyph and snapped to the six printed
x-axis tick marks. Both y-axes calibrate to a residual of **0.0007 pt**, which
is 0.0002 fold on the left axis and 0.002 fold on the right. There are no error
bars on this panel — it is a computational sweep, not a measurement.

| markers | Minimal ratio (fold) | Average ratio (fold) |
|---|---|---|
| **1** | 1.021 | 4.003 |
| **2** | 2.100 | 48.667 |
| **3** | 2.401 | 18.336 |
| **4** | 5.338 | 89.003 |
| **5** | 6.610 | 166.335 |
| **6** | 6.561 | 166.003 |

### 3.1 The prose anchors it, and the agreement is close — QUOTED (p.1308)

> "the model predicts **at least a sixfold output difference** in HeLa cells
> relative to the closest other cell type USSC-7d and **on average about a
> 160-fold difference** relative to the rest of the cells (fig. S2E)."

The full six-marker circuit is Fig. 2C's right-hand endpoint. Digitized, that
endpoint is **Minimal = 6.56 fold** and **Average = 166.0 fold**. Against "at least
sixfold" and "about 160-fold" that is agreement on both axes at once, from one
sentence of printed text, and it is an independent check because the two axes
were calibrated separately. **The calibration of this panel is settled.**

(The sentence cites fig. S2E rather than Fig. 2C. Same circuit, same two
quantities; treat it as corroboration of the scale, which is what it is, and
not as a claim that Fig. 2C's endpoint is printed numerically anywhere.)

### 3.2 The non-monotonicity is REAL — and the caption explains it

The Average series is **4.0 → 48.7 → 18.3 → 89.0 → 166.3 → 166.0**. It dips by a factor of
**2.65 at three markers**. Confirmed visually at 600 dpi and then settled
exactly in the vector geometry: the three-marker glyph's centre is 3.774 pt above
the zero tick against 10.018 pt for the two-marker glyph, a gap of 6.2 pt against
a calibration residual of 0.0004 pt. **It is not a digitization artifact and it
is not close to one.**

**But it is not a contradiction with the prose, and the session should not teach
it as one.** The caption (p.1309) says what the two series are:

> "For a given number of markers (x axis), we computationally generate all
> possible classifier circuits by choosing subsets of markers from the set of six
> chosen markers and evaluate circuit output in HeLa cells and in the profiled
> healthy cell types. **We then choose a circuit that maximizes the worst output
> ratio** between HeLa and all non-HeLa cell types ("minimal") **and also
> calculate the average output ratio for this circuit** ("average")."

So **the circuit at each marker count is selected to maximise the Minimal ratio.
The Average is a by-product of that choice and is optimized for nothing.** The
three-marker circuit that best protects the worst case happens to have a worse
average than the two-marker one. That is exactly what one should expect from a
minimax objective, and it is a better teaching point than a contradiction:
*the quantity you optimize is the quantity that behaves; everything else is
free to move.*

And the prose is about the optimized series. p.1308: selectivity "steadily
increases as the number of markers goes from **one to five**". The Minimal
series is 1.02 → 2.10 → 2.40 → 5.34 → 6.61 over 1→5 — **monotone, exactly as claimed.**

### 3.3 Why the sentence stops at five — a small finding

The Minimal series **dips at six markers: 6.610 → 6.561**, a fall of 0.7%. That is
0.20 pt in the artwork against a 0.0007 pt residual, so it is real in the figure.
It is also not mysterious: at k markers the authors maximize over C(6,k)
candidate circuits, and at k = 6 there is only one circuit to choose from, while
at k = 5 there are six. **The authors' odd "one to five" is the honest
phrasing** — they stopped where their own curve stops rising.

As a scientific claim the dip is 0.7% and nobody should lean on it. As a reading
of why the sentence is worded the way it is, it is solid, and it is the kind of
thing worth showing a room that is learning to read figures against text.

---

## 4 · Fig. 3C — per-line killing, and the formula that defines it

**First, a correction to the panel names the session was scoped on.** Fig. 3B is
a *schematic* (the hBax/bcl2 construct), not data. The two bar charts are both
**Fig. 3C**: the caption (p.1310) reads "(C) Apoptosis assays in HeLa and HEK293
cell lines … **(Right)** Comparison of the circuit-killing efficiency for HEK293
versus HeLa cells". Confirmed from the panel letters in the page's text layer —
"C" sits at x 366.76, y 534.78, above the left-hand chart. Call them
**Fig. 3C(left)** and **Fig. 3C(right)** on slides and in the autograder.

### 4.1 Fig. 3C(right) — killing efficiency, r. u. — DIGITIZED

Ticks 0 / 0.5 / 1 at y = 479.319 / 501.014 / 522.341; **43.022 pt per unit**,
residual 0.123 pt = 0.003 r. u.

| cell line | killing efficiency (r. u.) | plotted SD | SD / mean |
|---|---|---|---|
| **HEK293** | 0.145 | 0.267 | 1.84 |
| **HeLa** | 0.915 | 0.120 | 0.13 |

**The HEK293 error bar is drawn with no lower cap.** Its vertical line runs
down to y = 479.135 — the bottom edge of the axis rule itself — and stops. That
is a clipped arm: mean − SD = 0.145 − 0.267 = **−0.122**, below zero, so the
lower half could not be drawn. The SD above is therefore recovered from the
upper cap alone, and it is honest only as "the upper arm reaches 0.412 r. u.".

**This is a limits item in its own right, and it is the single most important
caveat in this file.** HEK293's killing efficiency is determined to **SD/mean =
1.84**. The paper's own error bar does not exclude zero and does not exclude
0.4. Anything the session builds on "HEK293 is killed at about 0.15" must
survive that, and §5.3 checks whether the session's payoff does.

### 4.2 Fig. 3C(left) — the raw % AmCyan⁺ data — DIGITIZED

Ticks 0 / 3 / 6 / 9 / 12 at **4.20532 pt per unit**, residual 0.143 pt = 0.034
percentage points. AmCyan⁺ indicates **survival** (caption, p.1310).

| cell line | No cell death | hBax-Tgts | Circuit |
|---|---|---|---|
| **HeLa** | 9.77 ± 1.49 | 2.71 ± 0.38 | 3.31 ± 0.43 |
| **HEK293** | 8.84 ± 1.91 | 2.12 ± 0.13 | 7.82 ± 0.64 |

### 4.3 The definition is PRINTED, and it closes the loop — QUOTED (SOM, PDF p.19 = printed p.18)

> "The killing efficiency in Fig. 3C is calculated by dividing the difference
> between the percentage of AmCyan+ cells of the 'No cell death' control sample
> and that of the circuit sample by the difference between the percentage of
> AmCyan+ cells of the 'No cell death' control sample and that of the hBax-Tgts
> sample."

That is

    KE = (NoCellDeath − Circuit) / (NoCellDeath − hBaxTgts)

**This is the only quantitative definition the paper gives for any rate, and it
is the one the session's false-positive budget should use.** §0.3 records that no
FPR appears in numeric form anywhere; this formula is how one is built.

**The independent check the house style asks for, and it passes.** Recomputing
Fig. 3C(right) from Fig. 3C(left) through that formula, against the digitized
right-hand panel:

| cell line | recomputed from Fig. 3C(left) | digitized from Fig. 3C(right) | difference |
|---|---|---|---|
| **HEK293** | 0.152 | 0.145 | 0.007 |
| **HeLa** | 0.916 | 0.915 | 0.001 |

Two panels, calibrated separately against different axes, in different units,
reconciled through a formula printed in a different document. **The agreement is
0.001 on HeLa and 0.007 on HEK293.** Fig. 3C and Fig. 3C(left) are both settled,
and so is our reading of what "killing efficiency, r. u." means.

---

## 5 · Fig. 4B — the mixture, and the session's payoff

HeLa-EYFP and HEK293-Cerulean **in the same dish**. Counts are of **surviving
transfected cells** — Fig. 4 caption, p.1310: "The scatter plots show the
fractions of HeLa-EYFP and HEK293-Cerulean cells among the DsRed+ cell
population **interpreted as surviving transfected cells**. The bar chart shows
the absolute number of surviving HEK293 and HeLa DsRed+ cells (mean ± SD)."

Calibration: six ticks 0–2500 at **0.02105 pt per cell** (47.51 cells per pt),
residual 0.124 pt = 5.9 cells. Series from legend swatch colours —
HEK293 = (0.576, 0.8, 0.863), HeLa = (0.992, 0.753, 0.063).

**Counts. DIGITIZED.**

| condition | HEK293 | HeLa |
|---|---|---|
| **No hBax output** | 1906 ± 126 | 1386 ± 221 |
| **Constitutively-active hBax** | 158 ± 32 | 268 ± 55 |
| **Classifier-controlled hBax** | 1276 ± 118 | 347 ± 55 |

**Adam's approximate read was right.** He had 1915 / 1390, 170 / 280, 1285 / 355
against the digitized 1906 / 1386, 158 / 268, 1276 / 347 — every one of the six within
1% except the two small bars, which are within 13 and 4 cells. Nothing below
rests on his read; it is recorded because it was offered as a check and it
checks out.

### 5.1 The two rates — INFERRED BY US

Counts are survivors, so the fraction killed is 1 − n/n(no hBax).

| | HEK293 (false positive) | HeLa (true positive) |
|---|---|---|
| **classifier-controlled hBax, fraction killed** | **33.1% ± 7.6** | **75.0% ± 5.6** |
| constitutively-active hBax, fraction killed | 91.7% | 80.7% |
| **killing efficiency, SOM formula (§4.3)** | **0.360 ± 0.082** | **0.930 ± 0.069** |

**The false-positive rate is 33.1% and the true-positive rate is 75.0%.**
Adam's ~33% and ~74% are confirmed; the true-positive rate is 75.0%, a point
higher than his read.

SDs are propagated from the plotted SDs treating the three conditions as
independent. They share a transfection batch, so they are not independent, and
these are therefore an **upper bound** on the spread. They are also SDs of n = 3,
not SEMs.

### 5.2 Two ways to say "false positive", and the session must pick one

The raw fraction killed (33.1%) and the SOM's killing efficiency (0.360) are
different quantities and they differ by three points. The raw number asks *what
fraction of HEK293 cells died*; the SOM number asks *what fraction of the
achievable killing the classifier delivered in HEK293*, with constitutively-active
hBax as the ceiling. **The second is the one that compares to Fig. 3C**, because
it is the formula Fig. 3C is built from. Use the raw number when the sentence is
about patients and cells, and the SOM number when the sentence is about Fig. 3C.
Do not mix them inside one comparison.

### 5.3 The payoff — characterise one line at a time and you underestimate your own false-positive rate

**It survives, and it is stronger than the version the session was scoped on.**

| | HEK293 | HeLa (control) |
|---|---|---|
| **Fig. 3C — one cell line at a time** | **0.145** | 0.915 |
| **Fig. 4B — same circuit, same formula, in a mixture** | **0.360** | 0.930 |
| ratio | **2.48×** | 1.02× |

The comparison Adam asked for was 0.16 against 0.33. Digitized, Fig. 3C's HEK293
value is **0.145**, not 0.16 — slightly lower — and the mixture value under the
*same formula* is **0.360**. So the gap is **2.48×, not 2×.**

**What makes this worth a slide is the control column.** HeLa's killing
efficiency is 0.915 one line at a time and 0.930 in the mixture — unchanged. The two
experiments agree on the positive and disagree by a factor of 2.5 on the
negative. That is what rules out "the two panels are just on different scales",
which is the first objection a good student will raise, and it is only available
because the SOM prints the formula.

### 5.4 The honest caveat — and it is a real one

**Fig. 3C's HEK293 error bar swallows the effect.** The gap between 0.145 and 0.360 is
**0.81 of Fig. 3C's own plotted SD** (§4.1: SD = 0.267 on a mean of 0.145). The paper
cannot distinguish its single-line HEK293 killing from its mixture value. The
difference is real *as a difference between two printed panels*; it is **not**
established by the paper's own statistics, and a slide may not say the paper
showed it.

**Two further confounds, both structural.** Fig. 3C uses unmodified HEK293 under
the transfection recipe of table S3B; Fig. 4B uses **HEK293-Cerulean** cocultured
with **HeLa-EYFP** under table S4. So "in a mixture" is confounded with a
different cell-line variant and a different transfection. The mixture
interpretation is the natural one and the paper offers it, but the experiment is
not a clean single-variable comparison, and the session should say so rather than
be caught by it.

**The defensible sentence for the room:** *the same circuit, scored by the same
formula, shows a 15% off-target killing efficiency when HEK293 is measured
alone and 36% when HEK293 is sitting next to its target — while the on-target
number does not move. The paper's own error bars cannot resolve that difference,
which is itself the lesson: nobody measured this well enough to know their own
false-positive rate.* That lands harder than a clean 2× would.

---

## 6 · Fig. 4A — the reporter version, and a second estimate of the same rate

Same mixture, same dish, **reporter instead of killing**: DsRed output rather
than hBax. Ticks 0–4000 at **0.01315 pt per cell** (76.0 cells per pt), residual
0.132 pt = 10 cells.

**Counts. DIGITIZED.**

| condition | HEK293 | HeLa |
|---|---|---|
| **Constitutive output** | 2368 ± 302 | 3249 ± 290 |
| **Constitutively-repressed output** | 353 ± 63 | 176 ± 13 |
| **Circuit output** | 605 ± 76 | 2594 ± 793 |

### 6.1 The reporter's own false-positive rate — INFERRED BY US

This panel has a floor as well as a ceiling: "constitutively-repressed output"
is the OFF state. **Whether you subtract it changes the answer by a factor of
two, and that is the finding.**

| | HEK293 | HeLa | HEK293 / HeLa |
|---|---|---|---|
| circuit ÷ constitutive (no floor subtraction) | 0.255 | 0.798 | **0.320** |
| (circuit − repressed) ÷ (constitutive − repressed) | 0.125 | 0.787 | **0.159** |

### 6.2 Do the two estimates agree? Yes — but only pairwise, and that is informative

| estimate | value |
|---|---|
| Fig. 4B, killing, raw fraction of HEK293 killed | 0.331 |
| Fig. 4A, reporter, **no** floor subtraction | 0.320 |
| Fig. 3C, killing, one line at a time | 0.145 |
| Fig. 4A, reporter, floor subtracted | 0.159 |

**The reporter and the killing readout agree to within 1.1 points when the
same convention is used — 0.331 against 0.320.** So §5's false-positive rate is
confirmed by a completely independent readout, from a different panel, in a
different experiment, with no apoptosis in it. **That is the check the session
needs, and it passes.**

And the floor-subtracted reporter value, 0.159, lands on Fig. 3C's 0.145. So the
whole 2× spread in this paper's false-positive numbers is reproduced *within
Fig. 4A alone*, purely by the choice of whether to subtract the OFF state.

**What to make of that — and it is a judgement call, flagged for Adam in §8.**
Two readings are available and they are not equivalent:

1. **The 2× is a normalization choice.** Fig. 3C's formula divides by the
   achievable range, which is a floor-subtracted quantity; Fig. 4B's raw fraction
   killed does not. On this reading the session's payoff is partly about
   bookkeeping, not biology.
2. **The 2× is real and §5.3 already controls for it.** §5.3 applies the *same*
   floor-subtracting formula to both panels and still gets 0.145 against 0.360, with
   HeLa unchanged. Bookkeeping cannot produce that, because the bookkeeping is
   identical on both sides.

**Reading 2 is the one the numbers support**, and §5.3 is the comparison that
should go on the slide. But Fig. 4A shows how easy it is to manufacture the same
factor of two out of nothing, and a room full of engineers should see that
before they are handed a false-positive budget to design against.

### 6.3 The reporter and the killer do not report the same thing — and this belongs in a therapeutics session

In the mixture, each readout scored against its own achievable range:

- Fig. 4A (§6.1): the circuit's **output** in HEK293 is **0.125** of HEK293's
  own constitutive-minus-repressed range.
- Fig. 4B (§5.3, the SOM formula): the circuit's **killing** of HEK293 is
  **0.360** of HEK293's own achievable killing.

Same cells, same dish, same classifier — **a 2.88× discrepancy between what the
circuit computes and what the circuit does.** The obvious reading is that hBax
is a thresholded, amplifying effector: a little off-target output buys a lot of
off-target death. **That is the sharpest therapeutic point in the paper and the
session does not currently have it.** A classifier specified to a 12.5% output
budget delivers a 36.0% kill rate, because the budget was written in the wrong
units — you do not get to specify the classifier's output, you have to specify
the *effector's* outcome.

**Two pairs of numbers are available here and they give different factors, so
this subsection says which pair it means.** The pair above is absolute: 0.125
and 0.360 are each HEK293's value as a fraction of its own readout's achievable
range, and they are the two quantities the budget sentence is about. The
alternative is the selectivity pair, each readout's HEK293 value divided by its
HeLa value: **0.159** for the output against **0.388** for the killing, a
factor of **2.44×**. Both are defensible and they are not the same quantity.
The selectivity pair divides out the on-target value, and HeLa's two on-target
values are not equal (0.787 of range in the reporter against 0.930 in the
killer), which is the whole of why 2.88 and 2.44 differ. **The session carries
the absolute pair**, because its two numbers are the ones a budget is written
on and because each is a fraction of its own readout's range. Its own caveat:
those two ranges are set by different controls — constitutively-repressed to
constitutive for the reporter, no-hBax to constitutively-active hBax for the
killer — so treating both as "a fraction of the achievable range" treats two
different normalizers as commensurable.

This is INFERRED BY US. The paper neither computes nor comments on it.

---

## 7 · Fig. 2A — the false-positive definition, verbatim — QUOTED (Fig. 2 caption, p.1309)

Nothing to digitize. This is the only printed definition of a false positive in
the paper, and §0.3 already carries it; it is repeated here in full, in its
caption context, because §5 and §6 are built against it:

> "**(A)** Simulated output levels of a two-input circuit with miR-21 and
> miR-17-30a inputs. Each dot represents a particular cell type, and **the
> contour line shows input combinations that result in 20% output relative to
> HeLa cells (red dot). Dots above the contour line represent "false-positive"
> cell types for this specific circuit configuration.** The numbers on the axes
> are given in cloning frequency (CF) units."

Three things the session should take from the exact wording.

- **The threshold is 20% of HeLa output — a declared convention, not a measurement.**
  It is chosen, not derived, and nothing in the paper defends the number 20.
  A false-positive budget is a *choice of threshold* before it is anything else,
  and this is the paper handing the room that point in its own words.
- **"For this specific circuit configuration."** The authors scope the definition
  to one circuit. A false positive is not a property of a cell type.
- **It is defined on a two-input simulation**, in cloning-frequency units, on the
  Fig. 2A panel only. It is **not** the definition behind Fig. 3C or Fig. 4B,
  which are experiments scored by the killing-efficiency formula in §4.3.
  Two different notions of "false positive" live in this paper and the session
  must not let them blur: **§7 is a threshold on predicted output; §4.3 is a
  measured killing rate.**

### 7.1 The matrix at Xie's own 20% cut — DERIVED from §2.1 and §2.2

Apply §7's printed convention — output at 20% of HeLa's, relative — to the
five-sensor product of §2.2, in the sensor-output convention §2.1 settles, with
every sense declared high. Relative to HeLa the seven lines read:

| cell line | output, relative to HeLa |
|---|---|
| **HeLa** | 100.0% |
| **T47D** | 67.8% |
| **SKBR3** | 38.1% |
| **DAOY** | 11.6% |
| **MCF-7** | 9.7% |
| **SH-SY5Y** | 5.5% |
| **HEK293** | 0.25% |

At the 0.20 cut, **2 of the 6 negative lines clear the threshold: SKBR3 and
T47D. That is 2 of 6, 33.3%.** `posb.classifiers.confusion` with
`threshold=0.20, relative=True` returns fp = 2 and tn = 4 on this table.

**The answer is not delicate in the threshold.** Because the cut is a fraction
of HeLa's own output, the false-positive set changes only where the threshold
crosses a negative line's relative output, so the whole family is a staircase
with one step per negative line. `confusion` calls a line sitting exactly on
the cut positive, so the steps are half-open in t:

| threshold t | false positives | lines |
|---|---|---|
| 0.6776 < t ≤ 1.0000 | 0 of 6 | — |
| 0.3814 < t ≤ 0.6776 | 1 of 6 | T47D |
| **0.1159 < t ≤ 0.3814** | **2 of 6** | **T47D, SKBR3** |
| 0.0968 < t ≤ 0.1159 | 3 of 6 | T47D, SKBR3, DAOY |
| 0.0549 < t ≤ 0.0968 | 4 of 6 | T47D, SKBR3, DAOY, MCF-7 |
| 0.0025 < t ≤ 0.0549 | 5 of 6 | T47D, SKBR3, DAOY, MCF-7, SH-SY5Y |
| 0 < t ≤ 0.0025 | 6 of 6 | T47D, SKBR3, DAOY, MCF-7, SH-SY5Y, HEK293 |

**The 2-of-6 answer holds for every threshold from 0.1159 to 0.3814** — a
factor of 3.29 in t — and Xie's 0.20 sits inside that span rather than at
either edge. At 0.10 DAOY joins and the count is 3 of 6; at 0.50 only T47D is
left, 1 of 6.

**§2.2's third bullet already named these two lines**, from the shape of the
matrix and before any circuit arithmetic, on the ground that every one of
SKBR3's and T47D's ten responses sits between 0.52 and 0.99 with no inverse
anywhere. The product selects the same two lines and no others. The qualitative
read of the matrix and the arithmetic over it are independent of each other, so
their agreement is worth recording.

Computed at the digitizer's full precision. From §2.2's printed three-decimal
values — the normative ones — the relative outputs move in the third digit, and
HEK293's goes from 0.251% to 0.243% because its P21 value of 0.010 carries one
significant figure at that precision.

**No count in this subsection changes with the precision, and that is checked
rather than assumed.** At every threshold from 0.10 to 0.50 in the steps a
problem set would use, the rounded and unrounded matrices give the identical
false-positive set — SKBR3 and T47D at 0.20, and the same membership at every
step of the staircase above. §7.2's bound takes counts rather than responses,
so it does not move either.

**They do not agree at every conceivable threshold, and the exception is worth
naming.** Two of the staircase's breakpoints sit in slightly different places
under the two precisions, so inside these narrow bands the two matrices
disagree about one line:

| band in t | line in dispute | width |
|---|---|---|
| 0.381089 < t ≤ 0.381429 | SKBR3 | 3.4 × 10⁻⁴ |
| 0.115927 < t ≤ 0.116063 | DAOY | 1.4 × 10⁻⁴ |

Together those bands span 0.000476 of the 0.40-wide interval, about one part in
841, and Xie's 0.20 falls in neither. The lesson is not that the answer is
fragile. It is that a cut placed on top of a breakpoint inherits the precision
of the matrix underneath it, so a problem set should not put one there.

### 7.2 The 33.3% here and §5.1's 33.1% are not the same quantity

§5.1's measured false-positive rate in the Fig. 4B mixture is **33.1% ± 7.6**.
§7.1's matrix count at Xie's own cut is **33.3%**. They agree to two tenths of
a point. **The agreement is a coincidence, and a slide that shows both numbers
has to say so.**

The two count different things.

- **33.3% is a fraction of cell lines.** It is how many of 6 negative cultured
  lines have a predicted five-sensor product above a declared fraction of
  HeLa's — a threshold on predicted output, which is what §7's closing
  paragraph says the Fig. 2A convention is. No cell was killed to produce it,
  and the quantity can take only the 7 values 0, 1/6, …, 1.
- **33.1% is a fraction of cells.** It is the proportion of HEK293 cells in one
  dish that died, from §5.1's count ratio: a measured killing rate for a single
  negative line, with an SD of 7.6 points over n = 3.

Move the threshold and the first changes while the second does not. Add an
eighth cell line to the panel and the same holds. §5.4's confounds — the
Cerulean variant, the different transfection recipe — move the second and leave
the first untouched. The two quantities share no denominator and no experiment,
and they print the same digits here because of how the seven lines happened to
fall. A sentence of the form "the matrix predicts a third and the experiment
measured a third" is a validation claim, and nothing in this file supports one.

**What a slide may say instead:** at Xie's own cut the matrix calls 2 of 6
negative lines false positives, and the mixture experiment kills about a third
of the one negative line it tested. Both are bad news for a therapeutic budget.
Neither is evidence for the other.

**§6.2 is a different thing and it does pass.** §6.2 puts Fig. 4A's reporter
false-positive ratio (0.320) against Fig. 4B's raw killing fraction (0.331) —
two measurements of *the same quantity*, the off-target fraction in the same
mixture, through readouts that share no apoptosis. Agreement to 1.1 points
there is a genuine cross-readout check and §6.2 is right to call it one. The
coincidence in this subsection is between a fraction of cell lines and a
fraction of cells. **Do not let §6.2's strength be read as support for it.**

**What the panel does establish is a bound, and that is the stronger lesson.**
With 2 false positives out of 6 negative lines,
`posb.classifiers.fp_rate_upper_bound(2, 6)` returns **0.7287**. The function
is the exact one-sided Clopper–Pearson upper limit, `beta.ppf(confidence, k +
1, n − k)` at confidence 0.95: a one-sided 95% upper limit on a binomial rate,
not half of a two-sided interval, and an upper limit only — the panel's point
estimate of 2/6 is the lower end of nothing. So the defensible statement is
that **a seven-line panel at this cut is consistent with a false-positive rate
anywhere up to 73%.** The function's own docstring adds that the negative lines
are not independent draws from one per-cell rate, which makes 0.7287 an
optimistic bound on a quantity the panel does not measure.

That is §5.3's lesson reached a second way. §5.3 gets there from two
experiments that disagree by 2.48× on the same cell line; this gets there from
the width of a binomial bound on 6 lines. Neither argument depends on the
other, which is why both are worth the room's time.

**The dose consequence, with one substitution said out loud.**
`wrong_cells_per_dose(fp_rate, treated_population)` returns the product of its
two arguments, and its docstring is explicit that `fp_rate` is a **per-cell**
rate and that a fraction of misclassified cell lines is not that quantity.
Feeding 2/6 into it reads the panel's line fraction as though it were a
per-cell rate — the substitution the function warns against. Made with that
stated, at 10⁹ delivered cells:

| rate fed in | wrongly acted-on cells per dose |
|---|---|
| point estimate, 2/6 = 0.3333 | 3.3 × 10⁸ |
| 95% upper limit, 0.7287 | 7.3 × 10⁸ |

The two differ by 2.19×, or 4.0 × 10⁸ cells. Against PS9's budget of one wrong
cell both fail by more than eight orders of magnitude, and the distance between
them is the part no seven-line panel can close.

---

## 8 · What is not readable, and what is a call for Adam

### 8.1 Not readable — stated, and left out

- **Five of Fig. 2D's 35 SDs** (§2). Drawn shorter than the figure's own line
  weight. Means are good; those five SDs are withheld and must not be
  interpolated.
- **Fig. 3C(right)'s HEK293 lower error arm** (§4.1). Clipped at the axis
  because mean − SD < 0. The SD quoted there is from the upper cap alone.
- **No numeric value is printed on any bar in any of these panels.** Settled
  exhaustively from the text layer, not by rendering (§1.6).

Everything else in §2–§6 is read from the page's own vector geometry and is
limited by the figures' drafting jitter, which is tabulated in §1.2.

### 8.2 Calls for Adam

1. **The payoff is sound but its headline number changes.** §5.3's comparison is
   **0.145 → 0.360 (2.48×)**, not 0.16 → 0.33 (2×), once both sides use the SOM's own
   formula. The HeLa control is flat across the same comparison, which is what
   makes it credible. **Decide whether the slide says "roughly double" (safe,
   and true under every convention) or "two and a half times" (true, and only
   under the matched formula).**
2. **The paper's own error bars do not resolve the payoff** (§5.4) — the gap is
   0.81 of Fig. 3C's HEK293 SD. This can be taught as a failure of the
   measurement rather than hidden, and it is probably the better session, but it
   is a different session from the one currently scoped. **Your call.**
3. **Fig. 4A manufactures the same factor of two from a normalization choice
   alone** (§6.2). If the room is shown §5.3 without §6.2, a sharp student can
   reasonably accuse the session of the bookkeeping error §6.2 rules out. **Worth
   30 seconds of the deck.**
4. **The reporter-versus-killer discrepancy (§6.3) is new and unclaimed** —
   off-target output 0.125 of HEK293's own range against off-target killing 0.360
   of its own range, a 2.88× gap, in the same dish. It is the strongest
   therapeutics point available here and it costs no extra digitization.
   **Recommend promoting it into the closing move.**
5. **Panel naming is wrong in the session scope** (§4). Fig. 3B is a schematic;
   both bar charts are Fig. 3C. The library, deck, problem set and autograder
   should say Fig. 3C(left) and Fig. 3C(right).
6. **The naive product of Fig. 2D does NOT reproduce Fig. 2C, and the worked
   example must not pretend it does.** Multiplying the five digitized sensor
   outputs gives HeLa 0.4336 against T47D 0.2938 — a worst-case margin of
   **1.48×**, not Fig. 2C's **6.56-fold**. Fig. 2C is a *model* over the MicroRNA
   Atlas cell types using the paper's full circuit response function (p.1308,
   fig. S2E); Fig. 2D is seven measured lines through a bare product. They are
   different calculations over different cell sets and they should not be put on
   one axis. **A student who multiplies the matrix and expects sixfold will
   think they have made an error.** Say so in the prompt.
7. **Fig. 2C's non-monotonicity is real but is not a contradiction** (§3.2). The
   caption's minimax objective explains it. If a slide was going to say "the
   prose and the figure disagree", it should not; the better line is about
   optimized versus reported quantities.
8. **Convention on Fig. 2D is load-bearing and is recorded in §2.1.** The bars are
   sensor outputs, not marker levels; a consumer must convert through
   `marker_levels_from_sensor_outputs`, and anything through that conversion is
   MODELLED. The check is in §2.1 and in the digitizer's
   `convention_check_Fig2D` block. **The failure is silent** — under the wrong
   reading the classifier selects SKBR3 over HeLa.
9. **§6.3 stated its factor two ways and now carries one.** It is the absolute
   pair — off-target output 0.125 of HEK293's own range against off-target
   killing 0.360 of its own range, **2.88×** — and not the selectivity pair
   (0.159 against 0.388, 2.44×). Both are defensible, and the absolute pair
   is the one the budget sentence in that subsection is written on. §6.3
   records the other with its value so that a reader who recomputes it does
   not conclude the file is wrong. **Reverse it there if you would rather the
   slide said the smaller factor.**

### 8.3 What is NOT claimed in §1–§8

- No claim that any value here is printed numerically anywhere in the paper or
  the SOM. §0.1 stands: all 35 of Fig. 2D's values and every count in Figs. 4A
  and 4B exist only as drawn geometry.
- No claim that the mixture effect in §5.3 is statistically established. §5.4
  says it is not.
- No claim about Fig. 2B, Fig. 2E, Fig. 2F, Fig. 3A, Fig. 3B or any
  supplementary figure. None of them was digitized.
- No claim that the SDs here are SEMs, or that n > 3.
- No claim that any marker is redundant or should be dropped (§2.3). The
  leave-one-out table is a statement about seven adherent cultured lines, and
  the paper's own selection criterion (p.1308) is scoped to healthy cell types
  drawn from the MicroRNA Atlas and explicitly declines to differentiate HeLa
  from other cancers.
- No claim that §2.3's P21 ordering between HeLa and MCF-7 means anything. The
  gap is 0.0019 rel. u., which is 0.029 of HeLa's own plotted SD — far above
  the digitization residual and far below the measurement's own spread.
- No claim about which miRNA marks which cell lineage. §2.3's counterweight is
  structural and rests on the two p.1308 sentences it quotes; no lineage
  biology is asserted anywhere in this file.
- No claim that §7.1's 33.3% validates, confirms or is comparable to §5.1's
  measured 33.1% (§7.2). One is a fraction of cell lines at a declared
  threshold on predicted output; the other is a fraction of cells killed. Their
  agreement is a coincidence. §6.2's agreement is a different matter and does
  stand.
- No claim that 2/6 is a per-cell false-positive rate. §7.2's dose figures feed
  a fraction of cell lines into `wrong_cells_per_dose`, whose docstring warns
  against exactly that, and they are reported as that substitution rather than
  as a measured rate.
- No claim that §7.2's bound is a two-sided interval or that it says anything
  about how LOW the rate could be. It is a one-sided 95% upper limit only.
- No claim that the normalization choice affects anything in §2.3 or §7.1. The
  column-maximum normalization is an exact factor common to all seven lines;
  §2.3 gives the algebra and the numerical check.
- No claim that §6.3's 2.88× and the selectivity pair's 2.44× are the same
  quantity. §6.3 carries the absolute pair and names the other.
