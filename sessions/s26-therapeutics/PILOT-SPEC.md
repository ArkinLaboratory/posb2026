# Session 26 — PILOT SPECIFICATION for the PS9 block (T69, T70)

**Written 15 November 2026.** Narrow purpose: fix enough of session 26 that
PS9's session-26 block can be written against something real. This is not a
deck design and it does not replace `DESIGN.md`. Where it contradicts
`DESIGN-SPINE.md` or `DESIGN.md` it says so and recommends which wins.

Sources read in full: `DESIGN.md`, `DESIGN-SPINE.md`, `NUMBERS.md`,
`posb/classifiers.py`, `tests/test_classifiers.py`,
`private/review/ps-bar.md`, `private/review/ps09-collision-check-2026-11-15.md`,
`private/sources/ps09-PLAN.md`, `docs/symbols.md`.

Every number in §3 was computed twice — once through `posb/classifiers.py`
and once by arithmetic that imports nothing from `posb` — and both runs are
printed.

---

## 1 · The two techniques, stated exactly

**T69 — design a multi-input classifier to a false-positive budget. AUTO,
PS9 and the final.**

> Given a panel of marker levels for one positive cell line and several
> negative ones, pick a marker subset and a cut on the classifier's output,
> count how many negative **lines** the cut calls positive, turn that count
> into a per-**cell** false-positive rate you state and defend, multiply it by
> a treated population you state, and say whether the result clears a budget
> of one wrongly acted-on cell.

**T70 — sensitivity/specificity trade-off reasoning. HAND, PS9.**

> Say what moving the cut buys and costs — which negative lines leave the
> false-positive set, and what happens to the one positive line — and say what
> the panel cannot establish: that a fraction of negative *lines* is not a
> per-*cell* rate, that six negative lines resolve no rate finer than 1/6 and
> bound the per-cell rate only from above, and that specificity measured one
> line at a time understates the rate measured beside the target.

T69 is a **count**, not a fraction — `DESIGN-SPINE.md` is explicit, and the
set's two ends are then the same arithmetic as T63's (`ps09-PLAN.md` §1). The
population is the student's and has to be defended; the autograder checks the
arithmetic and the direction, not the value.

### Where the DESIGN documents and the library disagree

**1.1 · `design_to_budget` makes, silently, the substitution the module
refuses by name. The recommendation is that T69's graded chain not use it.**

`design_to_budget` computes `rate = fp / n_neg` — a fraction of negative
**cell lines** — and then `wrong = rate * pop`, reported as `Design.wrong_cells`
(`posb/classifiers.py:1157-1162`). That is exactly the step
`wrong_cells_per_dose`'s docstring refuses: *"A fraction of misclassified CELL
LINES is not this quantity, even though it is also a number in [0, 1]."* The
function never calls `wrong_cells_per_dose`, so nothing warns.

**Recommendation: the library wins on the search, the docstring wins on the
units.** T69's autograded chain is `confusion(...)` → the student's own stated
`φ_cell` → `wrong_cells_per_dose(φ_cell, N_dose)`. `design_to_budget` may be
used as an exhibit and may be graded on `markers`, `threshold` and `fp_lines`;
**no autograded answer should be keyed to `Design.wrong_cells`**, because
accepting it teaches the error T70 exists to mark.

**1.2 · The convention. `DESIGN.md` §3 wins, and it costs nothing.**

`DESIGN.md` §3 settles **marker levels**: normalize, convert at the boundary
with `marker_levels_from_sensor_outputs`, declare the three T-markers
`absent`. The library's own canonical Xie configuration is the other one —
`tests/test_classifiers.py:823` sets `XIE_SENSE = {m: "high" for m in
XIE_MARKERS}`, sensor outputs with the NOTs already inside the sensors.

**They are not in conflict; they are the same numbers.** Verified both ways in
§3: the two routes agree to 6.9 × 10⁻¹⁸ and give an identical ordering, and
`convention_check` returns `ok=True, alternative=None` with margin 1.475135 on
both. **Adam's 9 November decision stands** — it puts p.1308's three NOT terms
in the student's code. The tests must **not** be rewritten to match: they lock
a regression that only exists in the all-`high` reading
(`test_no_leave_one_out_subset_blames_the_convention`,
`test_the_fig2d_bars_read_as_marker_levels_are_caught_and_named`).

**Consequence for the autograder: accept both routes.** A student who keeps
the sensor outputs and declares every sense `high` is arithmetically right and
must not be marked wrong. The stem says which route it wants and the hidden
test tolerates either, because they are the same number.

**1.3 · The marker keys are sensor-module names, and the stem must print
them.** The library's Xie keys are `P21`, `P17-30a`, `T141`, `T142-3p`,
`T146a` — sensor modules — while the convention is the **level of** miR-21,
miR-17-30a, miR-141, miR-142(3p), miR-146a. `NUMBERS.md` prints `T142(3p)` and
the library spells it `T142-3p` (`tests/test_classifiers.py:858`,
`_MD_MARKER_RENAMES`). **Do not rename anything.** The stem prints the five
keys verbatim, in order, with one line saying the key names the sensor and the
value is the marker's level. A stem that writes "miR-141" where the notebook
wants `"T141"` costs a student an hour for nothing.

**1.4 · The two functions do not compose, and normalization is not optional.**
`normalize_responses` takes a dict; `marker_levels_from_sensor_outputs` takes a
matrix (`DESIGN.md` §9, `DESIGN-SPINE.md`). It is not avoidable by skipping
normalization: five of §2.2's values exceed 1.0, so `response_table`'s range
check refuses the published table outright. `DESIGN.md` §10 asks whether to add
a compose helper. **Recommendation: do not add it for PS9's sake.** `ps-bar.md`
§G freezes `posb/` from the build, and §D means the recipe has to be on a deck
surface whether or not a helper exists — so the helper buys the autograder
nothing the slide does not already have to supply. Print the four-line recipe
in the stem and on the slide. If Adam wants the helper for the notebook's
sake, it lands **before** the autograder snapshot, not after.

**1.5 · `sense_check() == []` must not appear in a T69 stem, and
`fp_rate` must not be called a rate.** `DESIGN-SPINE.md` already makes the
first point: silence is strictly stronger than "the convention is right", so a
student with a legitimately weak marker subset gets told their convention is
broken. If the item checks the convention at all it checks
`convention_check(...).alternative is None`, which is the field that answers
the narrow question. And `Confusion.fp_rate` is a fraction of **lines**; a stem
that calls it a false-positive rate has pre-conceded T70.

**1.6 · `DESIGN.md` §7's closing numbers are a hand-set configuration, not the
library's search result.** §7 gives 3.3 × 10⁸ and 7.3 × 10⁸ at 10⁹ delivered
cells, from 2/6 and from the 0.7287 bound. Those follow from **all five
markers at a cut of 0.20**. `design_to_budget` with its own default
`thresholds=(0.1, 0.2, 0.3, 0.5)` returns something else: `found=False`,
markers `('P21', 'T141')`, cut 0.5, **1/6** false-positive lines, 1.67 × 10⁸
wrong cells. Put 0.7 in the grid and it returns `found=True` with **0** false
positives and `wrong_cells = 0.0`. Three different answers, all correct, from
the same panel. **The threshold grid is therefore part of the item, not a
default to inherit**; T69's stem fixes it explicitly, and the deck has to say
that the designed answer depends on it (§4, item 11).

**1.7 · `fp_rate_upper_bound`'s general case cannot be derived in the hour.**
`DESIGN-SPINE.md` commits s26 to deriving only the zero-event case,
`p < 1 − α^(1/n)`, and lets students use the general case without deriving it.
The library's general case is `beta.ppf(confidence, k+1, n−k)`. Under
`ps-bar.md` §D an autograded item may not rest on a formula the deck only
asserts. **Recommendation: the autograded part of any bound item uses the
zero-event closed form, which the deck derives; the 2/6 bound (0.7287) belongs
to hand-graded T70, where the student argues with a number the deck printed
rather than reproducing a formula it asserted.**

**1.8 · `NUMBERS.md` §7.1 undercounts its own precision-disputed bands, and
one of the unnamed ones is where a clean design lives.** §7.1 names two bands
in which the rounded and unrounded matrices disagree about one line. All six
breakpoints differ; two of them fall inside 0.10–0.50, which is the range
§7.1's claim is scoped to, so the file is not wrong where it is careful. But
the T47D breakpoint sits at **0.677595** unrounded and **0.677904** on the
published table — a disputed band of 3.1 × 10⁻⁴ **immediately below the only
cuts at which this panel has zero false positives.** T69 must not put a cut in
0.6776–0.6779. Safe cuts, clear of every band: 0.25, 0.30, 0.45, 0.60, 0.72.

**1.9 · `DESIGN.md`'s segment list never writes "sensitivity" or
"specificity", and T70 is named on them.** Move 3 carries the staircase and
move 4 the margins; neither word appears in §8's table. See §4, item 5 — this
is a section-D gap, not a numbers problem.

---

## 2 · Notation, and every collision checked

### The symbols T69 and T70 will use

| symbol | means | why this one |
|---|---|---|
| **x_m(i)** | the normalized **level** of marker m in line i; 1.0 = the most of that marker seen in **these** lines | x is session 13's letter for a gate's input level (`decks/s13_digital.py:202-209`, `x_IL`, `x_IH`), and s26's RETRIEVAL already recalls s13's threshold on a continuous output |
| **y(i)**, **y₊** | the classifier's output in line i; y₊ is the positive line's output | s13 writes gate outputs `y_OL`, `y_OH`; same object, same letter |
| **y_c** | the cut on the output, **always written as a fraction of y₊** | no single letter for the fraction; see the `t` collision below |
| **TP, FP, TN, FN** | counts of **cell lines** | the library's own field names; no letter can be mistaken for a rate |
| **N₋** | the number of negative lines (6 here) | never `n` |
| **N_dose** | the treated population, in cells | never `n` |
| **φ_cell** | the per-**cell** false-positive rate — the student's claim | never `p` |
| **φ₉₅** | the one-sided 95% upper limit on φ_cell from (FP, N₋) | names the confidence in the symbol |
| **N_wrong** | φ_cell · N_dose, against a budget of one | never `W` |
| **KE** | the SOM's killing efficiency, §4.3's printed formula | the paper's own words, spelled out |

Fractions of lines are written as **FP/N₋**, a count over a count, and never
given a letter. That is the whole of T70 in the notation.

### Collisions found, each with the rename

Checked against `docs/symbols.md` and against every symbol already live on
PS9: P, D, λ, s, h, f, n, and also q, t, k, c, μ, θ_A, ℓ_A, D_A, β_L, β_C, γ,
B, ε_T.

1. **`t` — COLLISION, and it is the damaging kind.** `NUMBERS.md` §7.1 writes
   the whole threshold staircase in **t**. On PS9, **t is time in generations**
   on an autograded technique in the same document: T61 lives on
   `t(q) = ln[(sq+μ)/(μ(1−q))]/(s+μ)` and `t₅₀ ≈ ln(s/μ)/s`
   (`ps09-PLAN.md` §2, `ps09-S23-DRAFT.md` Q1). Two autograded techniques, one
   set, one letter. **Rename: the threshold gets no letter.** Write the cut as
   **y_c**, and state it as a percentage of y₊ — which is also Xie's own
   phrasing, *"20% output relative to HeLa cells"*. `NUMBERS.md` §7.1's `t` is
   internal to that file and may stay there; nothing student-facing uses it.

2. **`n` — COLLISION.** `fp_rate_upper_bound(fp_lines, n_negative)` and
   `DESIGN-SPINE.md`'s `p < 1 − α^(1/n)` use n for the number of negative
   lines. `docs/symbols.md` has **n spoken for as the burst size** (s25,
   autograded T73, on this set). `NUMBERS.md` also writes n = 3 for the
   replicates. **Rename: N₋ for negative lines; the replicate count is written
   "three replicates" in words; the burst size keeps n.**

3. **`p` — COLLISION, by one case.** `DESIGN-SPINE.md` and
   `fp_rate_upper_bound`'s docstring write the per-cell rate as **p**. **P is
   the packaging advantage** (`docs/symbols.md`, "cannot move", autograded on
   T67 and T73 on this set). A per-cell rate `p` and a packaging ratio `P` one
   case apart in one document is a `ps-bar.md` §B hazard. **Rename: φ_cell.**

4. **`r` — COLLISION, against a document the students will already have
   worked.** `NUMBERS.md` §2.1 and the library write a response as **r**
   (`1 − r`), and the figure's unit is "rel. u.". The s23 **answer sheet**
   uses **r = s/μ** and names its crossover r\* = 413
   (`private/handouts/s23-evolution-answers.md:135-142`, finding C-1). C-6 in
   the same review treats precisely this pattern — a letter a student met on an
   s23 sheet reappearing in another meaning on PS9 — as a collision worth a
   rename. **Rename: x for the level.** `1 − r` stays in the library docstring,
   where no student is graded.

5. **`k` — COLLISION.** The natural letter for the false-positive count. **k
   is Weinberger's infectivity constant** on autograded T73 (`ps09-PLAN.md`,
   "λ and k back-solved from T₀ and V₀") and s23's redundant-cassette count in
   `(1 − e^{−μ₁t})^k`. **Rename: FP.**

6. **`q` — taken twice, and not needed.** T67's q = P/(1+P) (autograded) and
   s23's broken fraction q (autograded). s26 uses no q.

7. **Declared out of the s26 block entirely, because each is live on PS9 in
   another meaning:** **s** (selection coefficient — so sensitivity and
   specificity are written as words, or Sn/Sp, never s), **f** (drive-carrier
   fitness — so "fraction killed" is written in words), **h** (homing
   efficiency), **D** (the antiviral effect, and s24's dilution rate — so the
   dose is N_dose and the killing efficiency is KE), **λ**, **μ**, **γ**,
   **θ**, **ε**, **B**, **ℓ_A**, **D_A**. None of them is needed.

8. **`x` and `y` are a deliberate re-use, not a collision.** s13's x and y are
   a gate's input and output levels; s26's are a sensor's input level and the
   classifier's output. Same kind of quantity, one hour apart in meaning, and
   the session is already built to recall s13. The deck says so once, in body
   type, at first use.

9. **`α` = 0.05, the one-sided confidence level.** Unused elsewhere on PS9 and
   unlisted in `docs/symbols.md`. Free. Record it there when this lands.

**What to add to `docs/symbols.md`** (not added by this spec): rows for x, y,
y_c, N₋, N_dose, φ_cell, φ₉₅, N_wrong, and the four resolutions above with
their reasons. The registry's own rule applies — the side that moves is the
one not assessed and not a quoted published symbol, and in every case above
that is s26's, because the s26 deck does not exist yet.

---

## 3 · The worked numbers, each computed twice

Route 1 is `posb/classifiers.py` (`PYTHONPATH=. python3`). Route 2 is exact
rational arithmetic in `fractions.Fraction` plus a bisection on the binomial
CDF, importing nothing from `posb`. The input to both is **`NUMBERS.md` §2.2's
published three-decimal table**, which §2.2's closing line makes normative for
assessment, and which `tests/test_classifiers.py:903` keeps mirrored.

### 3.1 The two routes to the matrix agree

| quantity | route 1 (library) | route 2 (hand) |
|---|---|---|
| column maxima | 0.933, 0.755, 1.106, 1.019, 1.230 | same |
| product of column maxima | 0.976479247 | 0.976479247 |
| bare product, HeLa | — | 0.433614583 |
| bare product, T47D | — | 0.293949171 |
| **y₊ = y(HeLa), normalized** | **0.4440591889239366** | **0.444059188924** |
| y(T47D) | 0.3010296140732302 | 0.301029614073 |
| **margin y₊ / best negative** | **1.475135** | **1.4751346** |

`DESIGN.md` §3's validated pair — HeLa **0.444059189**, margin **1.475135** —
reproduces exactly on both routes. The sensor-output route (all senses `high`)
and the marker-level route (three T-markers `absent` after
`marker_levels_from_sensor_outputs`) differ by at most **6.9 × 10⁻¹⁸** and
give the identical ordering; in exact rationals they are **equal**.
`convention_check` on both: `ok=True`, `alternative=None`, margin 1.475135.
`sense_check` on both: `[]`.

### 3.2 Outputs relative to y₊, and the staircase

| line | y(i)/y₊, library | y(i)/y₊, hand |
|---|---|---|
| HeLa | 100.0000% | 100.0000% |
| T47D | 67.7904% | 67.7904% |
| SKBR3 | 38.1089% | 38.1089% |
| DAOY | 11.6063% | 11.6063% |
| MCF-7 | 9.7024% | 9.7024% |
| SH-SY5Y | 5.5120% | 5.5120% |
| HEK293 | 0.2430% | 0.2430% |

Staircase on the published table, half-open because `>=` calls a line on the
cut positive (`confusion`'s own convention):

| band in y_c/y₊ | FP | lines |
|---|---|---|
| 0.677904 – 1.000000 | 0 of 6 | — |
| 0.381089 – 0.677904 | 1 of 6 | T47D |
| **0.116063 – 0.381089** | **2 of 6** | **T47D, SKBR3** |
| 0.097024 – 0.116063 | 3 of 6 | + DAOY |
| 0.055120 – 0.097024 | 4 of 6 | + MCF-7 |
| 0.002430 – 0.055120 | 5 of 6 | + SH-SY5Y |
| 0 – 0.002430 | 6 of 6 | + HEK293 |

Both routes give this table. The unrounded geometry
(`_scratch/s26_xie/xie2011_digitized.json`) puts the breakpoints at 0.677595,
0.381429, 0.115927, 0.096781, 0.054866, 0.002512 — which is where §1.8's
disputed bands come from, including the unnamed one at 0.6776–0.6779.

### 3.3 The false-positive budget, end to end

The configuration `DESIGN.md` §7 closes on: **all five markers, cut at 20% of
y₊, N_dose = 10⁹ delivered cells, budget = 1 wrongly acted-on cell.**

| step | route 1 (library) | route 2 (hand) |
|---|---|---|
| TP / FP / TN / FN at y_c = 0.20 y₊ | `Confusion(tp=1, fp=2, tn=4, fn=0)` | tp 1, fp 2, tn 4, fn 0 |
| FP/N₋ | 0.3333333333333333 | 2/6 exactly |
| specificity TN/N₋ | 0.6666666666666666 | 4/6 |
| sensitivity TP/(TP+FN) | 1.0 | 1 |
| resolution floor 1/N₋ | 0.16666666666666666 | 1/6 |
| **φ₉₅ at FP = 2, N₋ = 6** | **0.7286616274802475** | **0.7286616275** |
| φ₉₅ at FP = 0, N₋ = 6 | 0.3930377689970827 | 0.3930377690 (= 1 − 0.05^(1/6)) |
| φ₉₅ at FP = 1, N₋ = 6 | 0.5818034092520259 | 0.5818034093 |
| **N_wrong, φ_cell := 2/6** | **3.333333e+08** | **3.333333e+08** |
| **N_wrong, φ_cell := φ₉₅** | **7.286616e+08** | **7.286616e+08** |

Against a budget of **one**, both fail by more than eight orders of magnitude,
and they differ from each other by 2.19× — 4.0 × 10⁸ cells, which is the part
no seven-line panel can close. The substitution of a **line** fraction for a
per-**cell** rate is said out loud wherever 2/6 is fed in; that is `DESIGN.md`
§7's rule and it holds here.

### 3.4 What the library's own search returns, which is not that

`design_to_budget(levels, sense, "HeLa", population=1e9, budget=1.0,
markers=all five)`:

| threshold grid | found | markers | cut | FP | N_wrong | φ₉₅ | N_wrong at φ₉₅ |
|---|---|---|---|---|---|---|---|
| default (0.1, 0.2, 0.3, 0.5) | **False** | P21, T141 | 0.5 | 1 | 1.667e+08 | 0.5818 | 5.818e+08 |
| (0.2,) | **False** | P21, P17-30a, T141, T146a | 0.2 | 2 | 3.333e+08 | 0.7287 | 7.287e+08 |
| (0.1, 0.2, 0.3, 0.5, 0.7) | **True** | P21, T141 | 0.7 | **0** | **0.0** | 0.3930 | **3.930e+08** |

Checked by hand on the same table, in exact rationals:

| subset | best negative | margin | FP at 0.20 | FP at 0.68 |
|---|---|---|---|---|
| P21, T141 | T47D at 0.529719 | **1.8878×** | 3 | 0 |
| P21, P17-30a, T141, T146a | T47D at 0.579015 | 1.7271× | 2 | 0 |
| all five | T47D at 0.677904 | 1.4751× | 2 | 0 |

Two things for the item writer, both verified twice. **A two-marker subset has
the largest margin on this panel and the full five the smallest** — a third,
independent refutation of Fight 2's *"can always increase specificity with
additional biomarkers"*, from the library's own search. And **a design that
meets a budget of one exists**: zero false positives, `wrong_cells = 0.0`, at
any cut above 0.678 — while φ₉₅ still permits 3.93 × 10⁸ wrong cells in the
same dose. That gap, between a met budget and what the panel establishes, is
the sharpest available form of T70, and it is why the threshold grid belongs in
the stem.

### 3.5 The digitized rates T70 may reason from

Not computable by `posb.classifiers` — it holds no data (module docstring) —
so these are checked by hand against `NUMBERS.md`'s own published counts.

| quantity | from | hand | NUMBERS |
|---|---|---|---|
| HEK293 fraction killed, Fig. 4B | 1 − 1276/1906 | 0.3305 | 33.1% (§5.1) |
| HeLa fraction killed, Fig. 4B | 1 − 347/1386 | 0.7496 | 75.0% (§5.1) |
| KE, HEK293, mixture | (1906−1276)/(1906−158) | 0.3604 | 0.360 (§5.1) |
| KE, HeLa, mixture | (1386−347)/(1386−268) | 0.9293 | 0.930 (§5.1) |
| KE, HEK293, Fig. 3C(left) recomputed | (8.84−7.82)/(8.84−2.12) | 0.1518 | 0.152 vs 0.145 digitized (§4.3) |
| mixture ÷ alone | 0.3604/0.145 | 2.4855 | 2.48× (§5.3) |
| Fig. 4A output, HEK293, floor-subtracted | (605−353)/(2368−353) | 0.1251 | 0.125 (§6.1) |
| output vs outcome | 0.3604/0.1251 | 2.8816 | **2.88×** (§6.3) |
| the selectivity pair, for the record | (0.3604/0.9293)/0.1589 | 2.4405 | 2.44× (§6.3, not carried) |

`DESIGN.md` §6 item 4 stands: **2.88×, not 2.44×**, with the
different-normalizers caveat on the surface.

---

## 4 · What must be DERIVED on a deck surface

`ps-bar.md` §D: *"For every autograded technique on the set, grep the deck for
the formula the item is graded on. If it is not on a surface, the item is not
assessable — derive it or drop the item."* This is the requirement list for the
deck build. It is not a deck.

| # | formula T69/T70 is graded on | what the deck must put on a surface | where `DESIGN.md` already plans it |
|---|---|---|---|
| 1 | y(i) = ∏_m x_m(i) for `high`, ∏_m (1 − x_m(i)) for `absent` | the product written out over the five markers, AND being multiplication, every factor in [0, 1] | move 2, BUILD (`xie2011_expression`) |
| 2 | x = 1 − r, the sensor-output → level conversion | the subtraction, on the surface where it is first used, with the idealization named: it inverts an ideal sensor, and a real RNAi sensor has leak, ceiling and slope | move 2, BUILD — and this is the surface that closes the three-year compositor bracket |
| 3 | x_m(i) = r_m(i) / max over the panel | the division, the exact-zero warning (HEK293 on T141 and T146a, MCF-7 on T142(3p) read 0.0000 and that means *panel maximum on the inverted sensor*, not *marker absent*), and that normalization is panel-relative | move 2, BUILD |
| 3a | the four-line recipe: build the dict → `normalize_responses` → rebuild the matrix → `marker_levels_from_sensor_outputs` | the four lines, as code, on a slide. §1.4: the helper does not discharge this | `DESIGN.md` §3, cost 1 — **currently a cost, not a segment. Give it a surface.** |
| 4 | the cut: a line is called positive when y(i) ≥ (y_c/y₊)·y₊, and a line exactly on the cut is called **positive** | Xie's caption verbatim, the relative convention, and the ≥ boundary rule stated once | move 3, FRAME (`xie2011_fig2a`) |
| 5 | **sensitivity = TP/(TP+FN), specificity = TN/N₋, FP/N₋** | the four counts as counts of **LINES**, and the two ratios, in body type — plus the fact that with one positive line sensitivity takes only two values | **GAP. Neither word appears in `DESIGN.md` §8's segment table.** T70 is named on this trade-off. Add it to move 3's staircase surface |
| 6 | the staircase: one step per negative line, 2 of 6 across 0.116–0.381 | the table of §3.2, or its two endpoints at minimum (the cut order allows reducing to endpoints) | move 3, BUILD, own figure |
| 7 | the resolution floor 1/N₋ = 1/6, and that a reported 0 means *below resolution* | the floor, as a number, beside a confusion matrix | move 5 or the ledger — **not currently a named surface. Add it** |
| 8 | φ₉₅ at FP = 0: 1 − α^(1/N₋) = 0.393 at N₋ = 6, α = 0.05 | the derivation, one line, as `DESIGN-SPINE.md` commits | ledger (§7's limits row cites `fp_rate_upper_bound(0, 6) = 0.393`) — **needs a derivation surface, not a ledger cell** |
| 8a | φ₉₅ at FP = 2: 0.7287 | the general Clopper–Pearson form is **asserted**, not derivable in the hour. §1.7: keep 0.7287 to hand-graded T70, or print the general form as the definition of the library call and accept that an autograded item resting on it violates §D | `DESIGN.md` §7 uses 0.7287 in the closing arithmetic |
| 9 | N_wrong = φ_cell · N_dose, against a budget of one | the product, the budget of one, and the T63 rhyme | move 6, CLOSE → LEDGER |
| 10 | that FP/N₋ is a fraction of **lines** and φ_cell is a fraction of **cells**, and substituting one for the other is a modelling leap | both quantities side by side, with the leap named out loud — `DESIGN.md` §7's "one substitution said out loud" | move 6 and move 5 guard 3 |
| 11 | that the designed answer depends on the threshold grid and the subset searched | §3.4's three outcomes, or at least two of them, on one surface: the same panel gives FP = 0, 1 or 2 and `found` True or False | **GAP. Not in `DESIGN.md`.** It is also the best available form of Fight 2 and costs one surface |
| 12 | KE = (NoDeath − Circuit)/(NoDeath − hBaxTgts) | the printed formula and both panels scored through it: 0.145 alone, 0.360 in the mixture, HeLa 0.915 → 0.930 | move 5, BUILD (`xie2011_fig3c`) |
| 13 | 0.125 of output range against 0.360 of killing range, 2.88× | both ranges' defining controls printed, the caveat that they are different normalizers, and INFERRED BY US | move 6, BUILD, own figure |

Items **5, 7, 8 and 11** are the live gaps. Items 3a and 8a are calls, not
defects. Everything else is already a planned surface in `DESIGN.md` §8 and
needs only the formula to be written in body type rather than referred to.

---

## 5 · The guide boundary, set in advance

No s26 handout and no s26 answer sheet exists —
`ps09-collision-check-2026-11-15.md` confirms `handouts/` stops at
`s25-populations.md` and `private/handouts/` at `s25-populations-answers.md`,
so *"T69 and T70 have no guide to collide with"*. This section is written so
the fourth leak does not happen. The three that already did were all in
**answer sheets**, and all three had **boundary headers asserting an absence
their own bodies violated**: `s23-evolution-answers.md:21-22`,
`s24-communities-answers.md:38-39`, `s25-populations-answers.md:23-25`.

**Locked decision 14 applies in the normal direction here**, because PS9 is
written first: the **guide** must avoid **PS9**.

### What the s26 home guide and its answer sheet must NOT ask or answer

1. **No five-marker product for any line.** Not HeLa's 0.4336 (published
   table) or 0.4441 (normalized), not T47D's 0.2939 or 0.3010, not the margin
   1.4751×, and not any line's output relative to y₊ (the 100.0 / 67.8 / 38.1 /
   11.6 / 9.7 / 5.5 / 0.24 column). Stating the HeLa row of five levels as a
   row of numbers is fine; multiplying it is T69.
2. **No false-positive count at any cut.** Not 2 of 6 at 0.20, not any other
   band, and not "which lines are the false positives at this cut".
3. **No staircase, and no band of it.** Not the breakpoints, not the 3.3×
   span, not "how far can you move the cut before the answer changes".
4. **No sensitivity, specificity, or FP/N₋ computed at a stated cut**, and no
   question asking which way either moves as the cut moves. That is T70's
   whole subject.
5. **No bound.** Not `fp_rate_upper_bound` at any (FP, N₋), not 0.393, not
   0.5818, not 0.7287, and not the zero-event derivation as an exercise. The
   guide may **restate** that six clean lines bound the rate below about forty
   percent; it may not ask a student to get there.
6. **No resolution floor as a question.** Not "what is the finest rate six
   lines can express".
7. **No wrong cells per dose, at any population.** Not 3.3 × 10⁸, not
   7.3 × 10⁸, not 1.67 × 10⁸, not the comparison to a budget of one, and not
   "pick a treated population and defend it" — that last one is the half of
   T69 the autograder cannot check and T70 is built on.
8. **No design to a budget.** No item that asks a student to choose markers
   and a cut to meet a stated budget, and no item that calls
   `design_to_budget`. Including as a demonstration with the answer printed:
   the answer sheet printing a `Design` object's `reason` string hands over
   §3.4's whole table, the φ₉₅ figure and the floor in one paste.
9. **No per-line-versus-per-cell discovery.** The guide may state the
   distinction; it may not ask a student to find it, and it may not ask what
   is wrong with multiplying 2/6 by a dose. That is the T70 item.
10. **No mixture arithmetic as an answer.** Not 0.145 against 0.360, not
    2.48×, not 0.125 against 0.360, not 2.88×, and not the two fractions
    killed (33.1%, 75.0%) computed from Fig. 4B's counts. These are the
    quantitative spine of hand-graded T70.
11. **No `confusion`, `fp_rate_upper_bound`, `wrong_cells_per_dose` or
    `design_to_budget` call anywhere in the guide or its answer sheet**, with
    output shown. A printed return value is a leak whatever the question was.

### What the guide may have, and should

Reserved for the guide now, so that PS9 does not take it: the **Fight 1
bracket** (`min()` against the product, 1.157× against 1.475×, and the
MCF-7/SH-SY5Y ranking swap); the **Fig. 2C Average-series dip** and the
minimax reading of it; the **leave-one-out margins** of §2.3, including that
dropping P21 inverts the call — margin is not the budget, and T69 does not need
it; the **33.3% / 33.1% coincidence** as a thing to explain; the **Fig. 4A
factor of two manufactured by a normalization choice**; and the **two
structural confounds** of move 5. None of those is T69's arithmetic or T70's
trade-off, and the leave-one-out reservation has to be written down because
`DESIGN.md` move 4 is currently keyed to *"the home-guide and PS9 items"*
both.

### Two rules for the answer sheet when it is written

- **Its boundary header states only what has been checked against its own
  body, line by line.** Three sheets in this repo now carry headers that are
  false of themselves. A header that cannot be verified is worse than none,
  because the next reviewer runs the check against the header.
- **Re-run the collision check** (`ps-bar.md` §E) against the built PS9, not
  against this spec, and add a T69/T70 row to
  `ps09-collision-check-2026-11-15.md`'s summary table, which currently reads
  *"no s26 guide exists; re-run if one is built"*.

### And one rule for PS9 itself

No number on the set should be a number from a slide — the precedent is the
s23 draft, which moved off the deck's own dose and μ for exactly this reason.
So T69's item should not reuse **10⁹ cells at a cut of 0.20 with all five
markers**, which is the deck's closing arithmetic. Change the population and
fix an explicit threshold grid; keep the cut clear of 0.116063–0.115927,
0.381089–0.381429 and 0.677595–0.677904 (§1.8). Safe cuts: 0.25, 0.30, 0.45,
0.60, 0.72. And print the defining equation in the stem wherever the item is
graded through a library function — `ps-bar.md` §B, and §1.1's units problem
makes that rule load-bearing here.
