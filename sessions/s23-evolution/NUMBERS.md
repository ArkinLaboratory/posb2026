# Session 23 — every number, with its kind

Source for everything marked MEASURED or QUOTED:
Rottinghaus *et al.*, *Nat Commun* **13**:672 (2022),
`private/readings/Session 23 - rottinghaus-2022-crispr-kill-switches.pdf`.
Page numbers are PDF pages of that file (17 pages total).

Kinds used here: **MEASURED** (they measured it), **QUOTED** (they state it,
citing someone else), **DERIVED** (algebra, exact), **COMPUTED** (our code, from
their inputs), **MODELLED** (our model with a parameter we chose), **INFERRED BY
US** (a conclusion of ours from their data — never attribute to the authors).

> Two cautions for any later pass. `pdftotext` cannot see numbers printed
> inside a figure panel, so a grep returning nothing is not evidence a number
> is absent — render the panel and look. And the MathJax in a handout renders
> to SVG, so a text diff of a built PDF cannot see a changed formula either.

---

## 1 · Generations from the passage protocol — DERIVED

The stability experiment passaged the strain at a **250× daily dilution** for
**28 days** (p.5, and methods p.9 and p.14).

    log2(250) = 7.9658 generations per passage
    28 days x 7.9658 = 223.0 generations
    14 days x 7.9658 = 111.5 generations

The paper reports **224 generations** at 28 days and **112 generations** at
14 days (p.2, p.6), i.e. it rounds to exactly 8 generations per day. 8
generations would be a 256× dilution. The gap is 0.4% and is not worth a word
on a slide, but the division is worth doing in front of the room, because it is
where "generations" stops being a word and becomes a unit derived from a
protocol.

## 2 · What they measured, in their own units — MEASURED

Fraction viable is CFU(+aTc) / CFU(−aTc) (p.3-4).

| quantity | value | page |
|---|---|---|
| single-target gRNA kill switches, best per target gene | 10⁻⁴ to 10⁻⁵ | 4 |
| plasmid Cas9 → four genomic integrations (Int X4) | 10× lower fraction viable | 4 |
| initial 2-gRNA switch | below 10⁻⁶·⁶ | 4 |
| optimized 2-gRNA switch, **with antibiotics, single timepoint (Fig. 1h)** | below 10⁻⁸·⁶ | 4 |
| mutated **cas9** cassettes — **Fig. 1d, plasmid Cas9 + single ile-2 gRNA, 30 survivors** | 80 ± 19 % | 4 |
| mutated **gRNA** cassettes — same strain, same panel | 10 ± 14 % | 4 |
| mutated **tetR** cassettes — same strain, same panel | 3 ± 6 % | 4 |
| Int X4 survivors, 24 sequenced — primary source of instability (Fig. 1g) | P*tet*-gRNA promoter | 4 |
| **pooled across strains (Fig. 6b)** — P*tet*-*cas9* and P*tet*-gRNA cassettes | **~45 % each** | 11 |
| of all observed mutations, 25 bp deletions taking an operator and most of −35 (Fig. 6c) | over 50 % | 11 |
| non-functional cells first appear | 14 days = 112 generations | 6 |
| authors' summary: killing "maintained" through | 28 days = 224 generations | 2, 6 |
| **28-day stability, CRISPRks strain, no antibiotics (Fig. 2e)** | **rises from ~10⁻⁸ at day 1 to 10⁻⁶·³⁵ at day 28** | 5 |
| half-maximal aTc | 21 ng/mL | 6 |
| complete killing by | 3 h of induction | 6 |
| gut-emulating assay (minimal medium, micro-aerobic, no shaking), monoculture, 24 h | 10⁻³·³ | 6 |
| same assay, 1:1 competitor, 24 h | 10⁻⁴·² | 6 |
| monoculture rebound to pre-induction levels | by 48 h | 6 |
| with competition, population eliminated — **CRISPRks Δrpdu** | by 72 h | 6 |
| competition still effective at — **Δrpdu** | 1:1000 | 6 |
| *in vivo* gavage dose | 10⁸ CFU | 6 |
| aTc in drinking water | 105 ng/mL | 6 |
| fecal titre reduction at 24 h, Δrpdu | 4-log | 2, 6 |
| fecal titre reduction at 24 h, CRISPRks | 1-log | 6 |

**"Complete killing at 28 days" is the abstract's framing, not a measurement
at 28 days.** The Fig. 2e row above is the measurement, and it is 10⁻⁶·³⁵ —
about two logs worse than day 1. Both belong in the file; only the second
belongs on a slide, and the gap between them is itself worth a sentence.

**The 72 h elimination and the 1:1000 result are Δrpdu, not plain CRISPRks.**
In plain CRISPRks, competition improved the 24 h kill from 10⁻³·³ to 10⁻⁴·² and
that is all. Elimination needed competition *and* the lowered
induction-dependent mutation rate. Two levers, not one — do not compress them.

**The mutation spectrum error bars are wider than some of the values.** gRNA at
10 ± 14 % and tetR at 3 ± 6 % both include zero; do not put 10% or 3% on a
slide as though they were resolved.

**And the ordering does not survive the redundancy — this file said it did,
until 8 November.** The note here used to read that cas9 ≫ gRNA, tetR "is what
the redundancy argument needs and that ordering is safe." It is not safe, and
the table above it already said so in two rows that nobody read against the
prose. The 80/10/3 split is **Fig. 1d**, measured on the strain with
plasmid-borne Cas9 and a single ile-2 gRNA — the sentence immediately after it
in the paper is the authors announcing the four genomic integrations. Once
those exist the limiting element moves: sequencing 24 non-functional **Int X4**
isolates identified the P*tet*-gRNA promoter as the primary source of
instability (Fig. 1g), and pooled across all strains the two cassette classes
each account for about 45 % of observed mutations (Fig. 6b).

So the correct statement is that **the limiting element moves as you add
redundancy**, which is a better result than the one this file was claiming:
redundancy on one side does not reduce escape, it relocates the weak point to
the other side. Do not carry the 80/10/3 ordering into any statement about
CRISPRks.

## 2b · The paper's OWN two routes, and what actually mutates — MEASURED/QUOTED

Found 2 November by reading the discussion; **absent from the original DESIGN
and it changes the hour.** The authors name two routes (their Fig. 6a):

**Route 1 — stochastic inactivation during normal replication.** "the natural
and slow accumulation of errors that occurs during DNA replication" (p.11).
Mitigated by redundant Cas9 and gRNA cassettes; gave stability for at least
28 days, though inactivated variants were still detected after about 14 days.

**Route 2 — SOS-mediated mutagenesis caused by the device's own cuts.**
Cas9 double-strand breaks induce the SOS response, which raises the cell's
mutation rate through recA and error-prone polymerases. Knocking out recA,
polB, dinB and umuDC gives the **Δrpdu** strain. Critically: "Escape mutants
of our CRISPRks strain only arose via this process **when tested in vivo or
with in vivo-like conditions** where resources and growth are limited" (p.11).
And Δrpdu changes nothing in optimal growth — both strains show "similar
long-term killing efficiencies, kill switch inactivation rates, and mutation
patterns in optimal growth conditions" (Fig. 4d–f).

**The causality runs the opposite way from the obvious reading, and the handout
had it backwards until 8 November.** SOS is induced by Cas9's breaks in *both*
conditions — if anything more in a flask, where expression is higher. The
condition-dependent step is downstream of that. In a nutrient- and
growth-limited environment per-cell protein production falls, so Cas9 is
expressed weakly and cleavage of the multi-copy replicating chromosome is
incomplete; the paper's own words are that low DSB levels per cell "would
allow daughter cells to survive with intact copies of the chromosome", while
SOS-activated and mutagenizing. They support it with a genome-integrated GFP
reporter significantly weaker in minimal than in rich medium (Supplementary
Fig. 8). In rich medium those mutagenized daughters are cut and die; in the
gut-like assay they live, and they are the escapers.

So the environment does **not** switch SOS on. It removes the killing that
would otherwise clear the SOS-mutagenized cells. Any slide, note or answer
that says the SOS route "only operates when the device is cutting" has the
arrow reversed — the device is cutting in both, and the difference is whether
the cutting finishes.

**What actually mutates — and the designer put it there.** The P*tet*
promoters were the primary source of instability. P*tet* "contains two
identical 19 bp tet operator sites", and **over 50 % of all observed mutations
were 25 bp deletions** removing one operator and most of the −35 site
(Fig. 6c, p.11). These arise by recombination between the tandem repeat —
RecA-dependent homologous recombination, or RecA-independent replication
slippage and single-strand annealing.

**Why this matters more than it looks.** The failure mode is not random point
mutation. It is **recombination between a repeat the designer chose**, in a
promoter the designer picked, duplicated across cassettes the designer added
for redundancy. Redundancy and repeat are the same thing. The authors say so:
promoter variants with one operator, or lower sequence identity, or no
internal homology "may further improve the stability".

This is also **why the fitted μ of §5b is a lumped parameter and not a
mutation rate.** Our model treats μ as a constant per-cell-per-generation rate
of random inactivation. The real rate is set by sequence choices and by whether
the device is currently cutting. It is not a constant of nature; it is a
consequence of design — which is the one sentence of §2b that has to reach the
room.

## 2c · What is on the plasmid, and what that lets the model absorb — QUOTED, then DERIVED

**The split.** *cas9* is exclusively genomic, in four cassettes at named
neutral integration sites. The gRNA cassettes, *tetR*, and a constitutive
*infA* cassette sit together on one plasmid, and the chromosomal *infA* was
knocked out — so a cell that drops the plasmid cannot make protein and dies.

**Why that matters to the model, and it is not what the handout used to say.**
Add segregational loss at per-generation rate λ and the equation becomes

    dq/dt = (1-q)(sq + μ) + λ(1-q) ≡ (1-q)(sq + (μ + λ))

identically — verified symbolically, the difference is exactly zero. Plasmid
loss is **perfectly** absorbed into μ. A within-population conjugative inflow
of a working plasmid contributes −βq(1−q) and is likewise absorbed into
s → s − β. So the one-state model does **not** need a new term for either, and
the honest statement is the sharper one: **a fitted μ silently contains the
plasmid-loss rate**, and the model cannot tell the two apart. The *infA* trick
is what removes that channel from the real strain, which is why the authors
built it.

What no choice of s and μ can represent is transfer of the construct **out of
the modeled population** — into another organism or a reservoir — because q is
defined within one population and the recipient is not in it. That needs a
second state variable, not a term. The authors address it in the discussion:
the only plasmid-borne elements are TetR and the gRNAs, the gRNAs are specific
to the EcN genome and inert without Cas9, and the selective markers would be
dropped in a clinical version.

## 3 · The containment requirement — QUOTED, and matched to the dose

The paper states a **killing efficiency of 10⁻⁸ recommended by the NIH Office
of Biotechnology Activities** (p.4, their reference 38). QUOTED — they cite it,
they did not measure it.

Also QUOTED, as prior art (p.2): a temperature-inducible toxin–antitoxin switch
stable over **140 generations** *in vitro* and ≥10 days in the mouse gut; a
combined temperature- and pH-inducible switch stable over ≥**100 generations**;
a CRISPR-Cas3 system stable for **1700 generations** applied to plasmid removal,
with the paper noting it is unclear whether that would hold for cell death; and
an **11-log limit of detection** in one earlier combined switch.

COMPUTED, from their dose of 10⁸ CFU:

| fraction viable | survivors per 10⁸ dose |
|---|---|
| 10⁻⁸ (the NIH figure) | **1** |
| below 10⁻⁸·⁶ (optimized, upper bound) | 0.25 |
| 10⁻⁶·⁶ (initial 2-gRNA) | 25 |
| 10⁻⁴·⁵ (single gRNA) | 3 200 |

**The requirement and the dose are matched to each other**: 10⁸ × 10⁻⁸ = 1.
The NIH figure is "fewer than one survivor per dose". Let the room find that.

## 4 · The failure-time result — DERIVED, then COMPUTED

With q the broken fraction, s the selection coefficient and μ the per-cell
per-generation inactivation rate,

    dq/dt = (1 - q)(s q + mu)

separates to the exact closed form

    t(q) = ln[ (s q + mu) / (mu (1 - q)) ] / (s + mu)

**DERIVED.** Verified against numerical integration over s ∈ {0, 10⁻⁴, 10⁻³,
0.01, 0.05, 0.2, 0.5} × μ ∈ {10⁻⁸, 10⁻⁶, 10⁻⁴} × q ∈ {10⁻³, 0.1, 0.5, 0.9};
**worst relative error 2.26 × 10⁻¹⁴** — exact to double precision. Pinned in
`tests/test_evolution.py`.

> **Corrected 2 November. Three error figures were in circulation and all
> three measured the wrong thing.** This file said 6.3 × 10⁻¹¹, DESIGN.md's
> withdrawal box said 4 × 10⁻¹³, and an LSODA run gave 1.15 × 10⁻⁸. All three
> are **integrator** error at the stiff corner (s = 0.5, μ = 10⁻⁸, q = 10⁻³),
> not error in the closed form. The figure above is against 40-digit
> quadrature of the separable integral. **Test a closed form against
> quadrature, never against an ODE solver.**

Limits, each exact:

- s = 0: q = 1 − e^(−μt), and t₅₀ = ln2/μ.
- μ ≪ s: t₅₀ ≈ ln(s/μ)/s. COMPUTED agreement with the exact form to four
  decimal places at (s, μ) = (0.02, 10⁻⁶), (0.02, 10⁻⁷), (0.05, 10⁻⁶),
  (0.05, 10⁻⁷), (0.1, 10⁻⁶), (0.1, 10⁻⁷).

**The ledger — COMPUTED.** Reference point s = 0.05, μ = 10⁻⁶, t₅₀ = 216.4
generations:

| change | t₅₀ (generations) | bought |
|---|---|---|
| reference | 216.4 | — |
| μ ÷ 10 | 262.4 | +46 |
| μ ÷ 100 | 308.5 | +92 |
| s ÷ 2 | 405.1 | **+189** |
| s ÷ 10 | 1703.2 | **+1487** |

Halving the burden beats dividing the mutation rate by a hundred — **for
s/μ > 413**. Writing r = s/μ, t₅₀ = ln(r + 2) / (μ(r + 1)), so the same 1/μ
sits on both sides of the comparison and the boundary depends on r alone. It
is the root of

    2 ln(r/2 + 2) / (r + 2)  =  100 ln(100r + 2) / (100r + 1)

which is **r\* = 413.000027** (40-digit root-finding; bisection returns the
same value at s = 1e-3, 5e-3, 0.01, 0.05 and 0.2). Below it the ranking
reverses.

**An adversarial review proposed 100·e^(2ln2) = 400, and that is not an error —
it is the exact μ → 0 asymptote of the equation above.** Drop the +2 and +1
terms, which are the μ-dependent ones, and the root is 400 exactly. The 3.25 %
gap between 400 and 413.000027 is the finite-μ correction. Use 413 for the
number and 400 for the reason: *a hundredfold cut in μ and a halving of s trade
off at a burden-to-mutation ratio of a few hundred* is the sentence, and 400 is
where the few-hundred comes from. This is the one number in the hour that
changes what a designer does, and it belongs on the slide that derives it, with
its regime.

**The reference s is MODELLED, not measured here.** s = 0.05 is a round value
chosen to sit inside the range session 19's Scott 2010 result implies — about
two percent of growth rate per one percent of proteome diverted — for a strain
carrying a plasmid and four chromosomal cassettes. Rottinghaus do not report a
fitness cost. Say so on the slide: real numbers first, and name the simplified
one as simplified.

## 5 · Escape needs more than one mutation — INFERRED BY US, with its regime

For k cassettes mutating independently at μ₁, each intact with probability
e^(−μ₁t), escape requires all k broken:

    q(t) = (1 - e^(-mu1 t))^k   ~   (mu1 t)^k      DERIVED

Verified two ways. **(i)** The full (k+1)-state mutation–selection chain with
s = 0 reproduces the closed form to a **relative** error of 4.4 × 10⁻⁷ (worst
over k = 2, 3, 4 at μ₁ = 10⁻⁴, t ≤ 2000, points with q > 10⁻¹²). The absolute
agreement is 1.4 × 10⁻¹⁴, which is the figure this file used to quote and is
nearly vacuous: q itself is ~10⁻¹² over most of that range, so an absolute
difference of 10⁻¹⁴ is no test at all. **Quote relative error whenever the
quantity spans decades.** **(ii)** The log–log slope of q against t, **measured
over t = 10 → 100 generations at μ₁ = 10⁻⁶**, is 1.0000, 2.0000, 2.9999,
3.9999 for k = 1, 2, 3, 4 — the slope is k. At μ₁ = 10⁻⁴ the same window gives
0.998, 1.996, 2.994, 3.992; the slope only equals k while μ₁t ≪ 1, and the
window and μ₁ are part of the number. COMPUTED.

**A one-hit process has no onset — but only at s = 0.** q = μt is linear from
the first generation *when the circuit is free*. Give it a cost and the one-hit
curve bends on log–log axes exactly the way redundancy does. See the
confounding table below; this is why the k ≥ 3 inference was withdrawn.

> ## ⛔ THE QUANTITATIVE k ≥ 3 ARGUMENT IS WITHDRAWN — see DESIGN.md
>
> It rested on a plating detection threshold of 10⁻³ that was chosen and never
> written down. Rottinghaus state their sensitivity as <10⁻⁸ or <10⁻⁹ (Fig. 2
> caption) and <10⁻⁷ (Fig. 4d); at 10⁻⁷ the same procedure returns k = 1 at
> every burden. Do not rebuild it.

**What replaces it: selection and redundancy are confounded.** Measured
2 November. Window t = 10 → 100 generations for the decade slope, t = 95 → 105
for the local slope, μ = 10⁻⁶ — **the slopes are insensitive to μ below 10⁻⁵**,
and stating the window is the whole point, since not stating it is what broke
the previous argument.

| model | decade slope | local slope |
|---|---|---|
| one cassette, s = 0 | 1.00 | 1.00 |
| one cassette, s = 0.02 | 1.46 | 2.31 |
| **one cassette, s = 0.05** | **2.36** | **5.02** |
| one cassette, s = 0.08 | 3.37 | 7.70 |
| k = 2 cassettes, s = 0 | 2.00 | — |
| k = 3 cassettes, s = 0 | 3.00 | — |
| k = 4 cassettes, s = 0 | 4.00 | — |

A single cassette carrying a 5 % fitness cost reads as **two to five**
independent cassettes. Matched at t = 100 with μ₁ = 1.55 × 10⁻³, one-hit-with-
cost and three-hits-without agree within a factor of 4 across the whole decade
and coincide exactly at t = 100. They separate only past t ≈ 200, where the
one-hit curve runs 16× higher.

**So you cannot read the architecture off a stability curve.** That is the
lesson, and it is a better one than the inference it replaces, because it is a
statement about what the measurement can and cannot support.

The authors did build **four** redundant P*tet*-cas9 cassettes and **three**
gRNA cassettes (p.4, and Fig. 2c). The model does **not** recover that from the
performance data, and must never be presented as doing so.

> **An earlier replacement draft in DESIGN.md's withdrawal box quoted slopes of
> 2.55 and 5.59.** Those do not reproduce at any μ; its time window was never
> recorded — the same defect a second time. Use the table above.

## 5b · The stability curve BOUNDS the burden FROM ABOVE — COMPUTED

> **Corrected 2 November, second time.** This section previously claimed the
> model was *refuted* by the 28-day data. That rested on reading
> **10⁻⁸·⁶ as the 28-day bound. It is not.** 10⁻⁸·⁶ is **Fig. 1h** — the
> optimized 2-gRNA switch, with antibiotics, a single timepoint, the number
> the authors compare to the NIH figure (p.4). The 28-day measurement is
> **Fig. 2e** and it is a **different strain** (CRISPRks). Using one strain's
> number as another's bound is the exact defect that killed the k ≥ 3
> argument. Check the strain and the conditions, every time.

**What Fig. 2e actually shows.** Not a floor — a rise, and a barely resolved
one. Digitized from the
extracted panel by locating the markers and calibrating against the tick
labels (`tools/fit_s23_fig2e.py`, reproducible):

| day | generations | log₁₀ fraction viable |
|---|---|---|
| 1 | 8.0 | −8.03, at the detection limit |
| 4 | 31.9 | −6.81 |
| 7 | 55.8 | −6.67 |
| 10 | 79.7 | −6.84 |
| 14 | 111.5 | −6.64 |
| 17 | 135.4 | −6.51 |
| 21 | 167.3 | −6.23 |
| 24 | 191.2 | −6.42 |
| 28 | 223.0 | −6.35 |

> **The day axis was wrong once.** The first pass assigned days by linear
> interpolation from day 0 across the nine markers, giving 0, 3.1, 6.2 … 28.
> The panel's x-axis is labeled at 1, 4, 7, 10, 14, 17, 21, 24, 28 — the
> authors' own sampling schedule, which is not evenly spaced. The marker
> positions were re-read against the tick labels. This moved μ from 2.8 × 10⁻⁹
> to 2.63 × 10⁻⁹ and the RMS from 0.179 to 0.151 decades. **Calibrate a
> digitization against the printed tick labels, never against the marker
> count.**

**And the model fits it.** Least squares on the eight detectable points:

| s | best μ | RMS (decades) |
|---|---|---|
| **0** | **2.63 × 10⁻⁹** | **0.151** |
| 0.005 | 1.86 × 10⁻⁹ | 0.203 |
| 0.01 | 1.31 × 10⁻⁹ | 0.278 |
| 0.02 | 5.62 × 10⁻¹⁰ | 0.473 |
| 0.05 | 2.83 × 10⁻¹¹ | 1.215 |
| 0.10 | 1.12 × 10⁻¹³ | 2.558 |
| *flat — no rise at all* | *n/a* | *0.204* |

RMS 0.151 decades at zero cost is inside the scatter of the data and of the
digitization, and the fit degrades monotonically with burden: the hour's
reference s = 0.05 misses by 1.2 decades. **But read the flat row before
claiming anything.** A horizontal line scores 0.204, so the one-hit rise beats
*no rise at all* by only 25 % in RMS on eight points. That is the whole
difference between a bound and a measurement.

**The s = 0.02 row was stale until 8 November** — it read 5.54 × 10⁻¹⁰ / 0.474,
which is a pre-day-axis-correction value. Refitting all six rows against the
digitized table above reproduces every other row inside a percent and moves
that one to 5.62 × 10⁻¹⁰ / 0.473. When a digitization is re-calibrated, refit
**every** row, not the headline one.

**What counts as excluded, so the handout can ask for it.** Treat a model as
excluded when its RMS is roughly 3× the best: with eight points and one free
parameter that is about a one-in-three-hundred coincidence. A 25 % gap — the
flat row — is about one in four, which is nothing. This is why s ≳ 0.02 is
excluded (3.1× the best) and the flat line is not.

**The nine-point slope of 1.08 is a CENSORING artifact, not window dependence.**
Including the day-1 point, which sits at the detection limit and is therefore an
upper bound rather than a measurement, drags the left end of the fit down and
returns 1.0777 over all nine points against 0.6287 over the eight detectable
ones. COMPUTED, same window in days or generations. Do **not** explain this as
the secant-window effect of §5 — that is a curved function sampled over
different windows, and this is a censored point treated as data. Two different
lessons; conflating them teaches the wrong one inside the item named "a bound is
not a measurement."

**So this is a bound, not a measurement — and the distinction is the lesson.**
A flat line with no rise at all scores RMS 0.204 against the one-hit fit's
0.151, so the rise is resolved by only about 25 % in RMS, and the data's own
log–log slope is **0.63** while every model in this family predicts ≥ 1. The
curve is therefore not a measurement of s. What it does do is **exclude** the
large values: s ≳ 0.02 misses by 3× the residual of the best fit. Report it as
*s is below about 0.02*, never as *s = 0*.

That still matters: the hour's reference s = 0.05 is excluded by the authors'
own stability data, so the ledger's reference point is MODELLED and known to be
on the high side. Say so.

**This is what the withdrawn k ≥ 3 argument was reaching for** — a parameter
constrained by a performance curve — done on the one parameter this curve can
constrain, and only in the direction it can constrain it. It bounds s. It does
not constrain k (§5).

**Where the model then runs out, and it is the hour's real turn.** If the
circuit is nearly costless and stable for a month in a flask, why did it fail
in a mouse? Because nothing in this model describes the second route: SOS
mutagenesis caused by the device's own double-strand breaks, which the authors
report appears **only in vivo or in vivo-like conditions** (§2b). The model is
complete for permissive growth and silent about operation. Figure
`s23_measure_s`.

## 6 · Fraction viable as the model's state variable — INFERRED BY US

Fraction viable is CFU(+aTc)/CFU(−aTc). A functional cell dies on induction, a
broken one survives, so fraction viable ≈ q. That mapping is what lets the model
be drawn on Fig. 2e's own axes, and it is an **approximation**: killing is not
perfect even for functional cells, and the paper's own floors are limits of
detection in several panels. Put the approximation on the slide, not in a note.

## 7 · Retention time — COMPUTED

Recomputed 2 November **without the withdrawn §5 fit**, which it no longer
needs. From the measured upper bound (fraction viable below 10⁻⁸·⁶) to the NIH requirement
(10⁻⁸), one-hit model, in generations:

| s | μ = 10⁻⁶ | μ = 10⁻⁷ | μ = 10⁻⁸ | μ = 10⁻⁹ |
|---|---|---|---|---|
| 0 | 0.01 | 0.07 | 0.75 | 7.49 |
| 0.01 | 0.01 | 0.07 | 0.74 | 7.05 |
| 0.02 | 0.01 | 0.07 | 0.74 | 6.67 |
| 0.05 | 0.01 | 0.07 | 0.73 | 5.74 |
| 0.10 | 0.01 | 0.07 | 0.71 | 4.69 |

Divide by 8 for days. **The whole grid spans 0.01 to 7.5 generations** — under
a day in every case. The thesis is stronger than it was, because it now rests
only on the measured upper bound, the quoted requirement and a mutation rate, with no
fitted k and no chosen detection threshold.

**A few generations, not a few hundred.** The measured bound of 10⁻⁸·⁶ clears the
requirement *at the moment of the assay*; it does not survive days of
permissive growth. The assay is a snapshot and containment is a duration.

This is why intra-niche competition is doing a different job from redundancy.
Redundancy raises the exponent and delays the onset; competition removes the
standing stock by making the escaper's advantage negative. The paper is explicit
that the SOS knockout is a third thing again: Δrpdu reduces *induction-dependent*
inactivation and has **"no impact on the mutation rate during normal DNA
replication"** (p.6).

## 7b · The two asymmetries point opposite ways — COMPUTED

The hour's two questions have opposite sensitivities, and this is the result
the session should be built on.

| | sensitivity to s | sensitivity to μ |
|---|---|---|
| **t₅₀** — how long the circuit lasts | **4.4×** (s: 0.01 → 0.05) | 1.4× (μ: 10⁻⁷ → 10⁻⁹) |
| **retention** — how long containment holds | 1.1× | **80×** |

t₅₀ at μ = 10⁻⁷: 1151.3 generations at s = 0.01, 262.4 at s = 0.05 —
a factor of **4.39**, not the 8× this file and the deck carried until
2 November. The ratio is ln(s₂/μ)·s₁ / (ln(s₁/μ)·s₂) ≈ 5 × (ln 10⁵ / ln 10⁴·³),
so the fivefold change in s is damped by the logarithm. Both asymmetries are
still an order of magnitude apart in opposite directions, which is the point;
the point does not need the number inflated.
Retention at μ = 10⁻⁷: 0.075 generations at both s = 0.01 and s = 0.05.
Retention at s = 0.05: 0.075 generations at μ = 10⁻⁷, 5.743 at μ = 10⁻⁹.

**Why.** Containment lives in the far-left tail, q ≈ 10⁻⁸, where selection has
had nothing to amplify yet, so crossing the requirement is pure mutation
accumulation. Selection only bites once (1 − q)·s·q competes with μ.

**The design consequence.** Burden reduction is the **longevity** lever;
mutation-rate reduction is the **containment** lever. They are not
interchangeable and the §4 ledger applies to the first question only. Δrpdu
lowers *induction-dependent* mutation with "no impact on the mutation rate
during normal DNA replication" (p.6) — aimed at exactly the right one. The
paper's architecture follows from the arithmetic, which is what the hour is for.

## 7c · Outside the assigned paper — QUOTED, for the closing slide

Added 2 November after an adversarial review found the hour taught one
architecture as though it were the field.

- **Mandell, Lajoie et al., Nature 518:55–60 (2015)**, "Biocontainment of
  genetically modified organisms by synthetic protein design". Synthetic
  auxotrophy for a non-natural amino acid. Double- and triple-enzyme
  auxotrophs showed **undetectable escape over 14 days, detection limit
  2.2 × 10⁻¹²**. Their framing of the three escape routes a containment
  strategy must survive: mutagenic drift, environmental supplementation, and
  horizontal gene transfer.
- **Rovner et al., Nature 518:89–93 (2015)**, "Recoded organisms engineered to
  depend on synthetic amino acids". Same January 2015 issue, same idea by a
  different route.
- [unverified] A follow-up reporting synthetic auxotrophy still intact after
  continuous evolution was cited here as *Science Advances* 2021. **It has not
  been located and must not go on a slide in that form.** The "containment is a
  duration" point stands on Mandell's own 14-day result; say that instead, or
  find the citation first.

**Why this belongs in the hour.** Mandell's opening argument is that existing
biocontainment imposes evolutionary pressure on the organism to eject the
circuit. That is session 23's thesis, published seven years before the paper
assigned for it. The design variable underneath every lever in §4 and §7b is
the **mutational target**: a kill switch fails by LOSS of function, which is
easy; a synthetic auxotroph fails by GAIN of a pathway for a molecule that
does not exist in nature, which is not. μ was never a constant of nature — it
is a property of what you made escape require.

**Not assigned, and the slide says so.** Rottinghaus are not being criticized:
they are solving the harder problem of making the loss-of-function
architecture work in a live gut.

## 8 · What is NOT claimed

- **No fitness cost is measured in this paper.** Every s here is modelled, from
  session 19. Do not put a measured-looking s on a slide.
- **k ≥ 3 is ours, bounded as in §5.** Not the authors' argument.
- **The 10 ± 14 % and 3 ± 6 % spectrum values are not resolved from zero.** Use
  the ordering, not the values.
- **Nothing here says the authors reasoned from a model.** They engineered,
  measured, and iterated. The model explains their architecture after the fact,
  which is worth saying out loud — it is what a design course is for.
- **No claim about human use.** The *in vivo* work is in mice.

