# Session 21 — NUMBERS

Every entry below was **computed on 26 October 2026** by integrating the full
binding kinetics with `scipy.integrate.solve_ivp` (LSODA, rtol 1e-12, atol
1e-14) and locating half-times with `brentq`. No QSSA shortcut was used to
produce a number that is then checked against QSSA. Scripts:
`private/scratch/s21/retro_claim.py`, `retro_scaling.py`, `retro_boundary.py`.

**Kinds:** sections 1–5 are **derived** — our model, our arithmetic. Section 6
is **measured**, read off Mishra 2014 on 26 October now that the PDF is held.

## The model

X produced at rate k, free X removed at rate γ. Downstream, p_tot operator sites,
X + p ⇌ C with K_d = k_off/k_on. Binding fast against γ throughout
(k_on ≥ 10⁴γ/K_d). Reference parameters: k = 10, γ = 0.01, so the unloaded total
**X_T = k/γ = 1000**.

Two models, and the difference is whether the sequestered molecule is still
being removed:

- **Model A — the complex is not removed.** Conservative binding.
- **Model B — the complex is removed at γ too.** ~~This is the growing cell,
  and it is the physical case.~~ **FLAGGED 31 October, NOT resolved — do not
  build a slide on either side of this.** The deck declines the sentence: its
  foot reads *"Same algebra, two conclusions. Which one holds is a fact about
  the molecule, not a modelling preference"*, and the hour builds to Mishra
  p. 1273, where load did not move the steady state **in exponentially growing
  culture** — Model A's signature, in a growing cell. So growth alone does not
  settle which model you are in, and this line claimed it does. The unresolved
  physics is **dilution versus degradation**: Mishra's protection is of SKN7m
  *from degradation* while bound to DNA, and growth dilutes a complex whatever
  it is bound to. Either dilution of the bound fraction is negligible on their
  timescale, or the protection does more than the phrase implies, or the
  measurement is less sharp than the sentence. **This needs the paper's own
  numbers, not a ruling from here.** `posb/retroactivity.py:13` carries the
  same retired sentence — not a second opinion, the same one.

---

## 1 · Model A: the steady state is EXACTLY untouched

| p_tot | X_ss | relative deviation from k/γ | slowdown in t½ |
|---|---|---|---|
| 0 | 1000.00000000 | 0 | 1.000 |
| 10 | 1000.00000000 | 0 | 1.014 |
| 100 | 1000.00000000 | 1.14 × 10⁻¹⁶ | 1.145 |
| 1000 | 1000.00000000 | 0 | 2.448 |

**Exact, not approximate**, and it follows from the algebra: at steady state the
binding flux is zero, so the load term drops out of dX/dt entirely.

## 2 · Model A: the QSSA formula is right

**dX/dt = (k − γX)/(1 + R(X))** with **R(X) = p_tot·K_d/(K_d + X)²**, against
the full kinetics' half-time:

| p_tot | t½ from QSSA | t½ from full kinetics | relative error |
|---|---|---|---|
| 10 | 70.3186 | 70.3186 | 1.7 × 10⁻⁷ |
| 100 | 79.3537 | 79.3538 | 2.9 × 10⁻⁷ |
| 1000 | 169.7050 | 169.7050 | 2.1 × 10⁻⁷ |

## 3 · Model B: total X is pinned, and free X falls by exactly what is parked

**X + C = k/γ exactly** (to 10⁻¹⁶ at every load tested), and
**C = p_tot·X/(K_d′ + X)** with **K_d′ = (k_off + γ)/k_on**, verified to
1.8 × 10⁻¹⁶.

| p_tot | X_ss | C_ss | X+C | relative level shift |
|---|---|---|---|---|
| 10 | 990.01009 | 9.98991 | 1000.000000 | 0.0100 |
| 100 | 900.11099 | 99.88901 | 1000.000000 | 0.0999 |
| 1000 | 31.12826 | 968.87174 | 1000.000000 | 0.9689 |

So in a growing cell **the level does move**, and it moves by precisely the
number of molecules parked on the sites.

## 4 · THE RESULT — both costs are set by p_tot/X_T, and NOT by the affinity

This is the session's thesis and it **refuted the hypothesis it was written to
test.** The guess on 26 October was that the level shift would scale as
p_tot/X_T while the slowdown would scale as p_tot/K_d, so that tight binding
would buy sharpness at the cost of speed. **That is wrong.**

Affinity swept over four orders of magnitude at fixed load (Model A, p_tot/X_T
fixed):

| p_tot/X_T | K_d = 0.01 | K_d = 1 | K_d = 100 |
|---|---|---|---|
| 0.10 | 1.1443 | 1.1448 | 1.1389 |
| 0.50 | 1.7214 | 1.7242 | 1.6946 |
| 1.00 | 2.4428 | 2.4483 | 2.3892 |
| 2.00 | 3.8856 | 3.8967 | 3.7785 |

**The slowdown is flat in K_d to within 3.4% across 10⁴ in affinity at
p_tot = X_T** — and the three-point sampling above understates it. The slowdown
is NOT monotone in K_d: it rises about 1% to a shallow maximum at K_d ≈ 16
(2.4691) before the sites begin to empty, so min and max over [0.01, 100] are
2.3892 and 2.4691, a 3.34% spread. The bound also grows with the load: 0.67% at
p_tot = 0.1 X_T, 2.26% at 0.5, 3.34% at 1, 4.05% at 2. Recomputed 31 October on
the figure's own parameters (k = 10, γ = 0.01, X_T = 1000, protected model). What sets
both costs is the **number of sites relative to the number of molecules**:

| p_tot/X_T | slowdown (A) | relative level shift (B) |
|---|---|---|
| 0.01 | 1.0145 | 0.00999 |
| 0.1 | 1.1448 | 0.09989 |
| 0.3 | 1.4345 | 0.29957 |
| 1 | 2.4483 | 0.96887 |
| 3 | 5.3450 | 0.99950 |
| 10 | 15.4833 | 0.99989 |

**Weak-load limit — both are linear in p_tot/X_T with a constant ratio:**

| p_tot/X_T | slowdown − 1 | level shift | ratio |
|---|---|---|---|
| 0.002 | 0.002897 | 0.001998 | 1.450 |
| 0.005 | 0.007242 | 0.004995 | 1.450 |
| 0.01 | 0.014483 | 0.009990 | 1.450 |
| 0.02 | 0.028967 | 0.019980 | 1.450 |
| 0.05 | 0.072417 | 0.049947 | 1.450 |
| 0.1 | 0.144833 | 0.099889 | 1.450 |

The level shift is **exactly** p_tot/X_T to three figures. The slowdown is
**1.450 × p_tot/X_T**, constant to four digits over fifty-fold in load.
~~**The 1.450 is measured and NOT derived**~~ — **WRONG, and corrected
31 October. It is 1/ln 2 = 1.442695, and the derivation is three lines**: in the
protected model the loaded system must synthesise p_tot extra molecules before
it reaches the same half-way point, which costs p_tot/k against an unloaded
half-time of ln 2/γ, giving (p_tot/X_T)/ln 2. `REBUILD.md` §2.1 carries it and
says outright that it belongs on the board. The deck does derive it, on the
segment 5 slide headed "where 1.44 comes from", and the answer sheet 4(d)–(e)
derives it too.

**So the instruction that used to sit here — "the slide says about one and a
half times and does not present 1.450 as a closed form" — would, if followed,
strip a correct derivation off a slide and out of an answer key. Do not follow
it. If this file and the deck disagree, the deck is right.** The residual
between the measured 1.4483 at K_d = 1 and 1.442695 is the finite-K_d
correction, not a fitting error: the identity is exact only as the sites
saturate.

## 5 · The boundary of the claim, and the engineering consequence

Affinity stops being irrelevant once the sites are no longer saturated. At the
heavy load p_tot = X_T:

| K_d | K_d/X_T | slowdown (A) | level shift (B) | C_ss/p_tot |
|---|---|---|---|---|
| 0.01 | 10⁻⁵ | 2.4428 | 0.99684 | 0.99684 |
| 1 | 10⁻³ | 2.4483 | 0.96887 | 0.96887 |
| 100 | 0.1 | 2.3892 | 0.72984 | 0.72984 |
| 10³ | 1 | 1.6367 | 0.38197 | 0.38197 |
| 10⁴ | 10 | 1.0947 | 0.08392 | 0.08392 |
| 10⁵ | 100 | 1.0099 | 0.00980 | 0.00980 |
| 10⁶ | 10³ | 1.0010 | 0.00100 | 0.00100 |

The crossover is at **K_d ≈ X_T**, and the last column is the whole story —
**but read the identity at the right generality.** In the diluted model
X + C = X_T exactly, so

    level shift = C_ss/X_T = (p_tot/X_T) × (C_ss/p_tot) = (p_tot/X_T) × occupancy

The level shift *equals* the occupancy **only because this table sits at
p_tot = X_T**, which makes the prefactor 1. Away from that load it does not:
at p_tot = 0.1 X_T a fully occupied operator shifts the level by 0.1, not by 1.
`posb.retroactivity` has the general form in its module docstring, item 4.
**Earlier wording here dropped the prefactor; it is an artefact of the chosen
load and not an identity.**

**So the load can be escaped by weakening the operator — and that is useless,
because an operator with K_d ≫ X_T is an empty operator, and an empty operator
regulates nothing.** The regime in which the load vanishes is the regime in which
the downstream module is not being driven.

**This is the session's engineering result: the load is the price of the
regulation, and you cannot pay less without buying less.** It is the same shape
as session 18's u₅₀ walking to 1 as the switch sharpens, and session 17's *a
parameter is manufactured, not found*. And it is why the cure is **insulation by
timescale separation** rather than affinity tuning: the load driver changes
neither p_tot nor K_d — it makes the upstream module fast enough that the parking
does not matter.

## 6 · What this corrects in DESIGN.md

The design's §3 claimed the steady state is untouched and only the speed changes,
and concluded that *"a student measuring endpoints would not detect retroactivity
at all."* **That is true of Model A and false of the growing cell.** In Model B
the level shift and the slowdown are the same order — both linear in p_tot/X_T,
within a factor of 1.45 of each other — so endpoints are about as informative as
dynamics. §3 is rewritten accordingly, and the "endpoints miss it" surface is
cut.

**Open for when Mishra 2014 arrives:** why that paper measures response time and
bandwidth rather than levels. Possibly because p_tot/X_T is small in their
system, possibly because the dynamic measurement is cleaner. **Do not guess this
on a slide** — read it off the paper.


---

# 6 · Mishra 2014 — MEASURED, read off the paper 26 October

`private/readings/Session 21 - mishra-2014-load-driver-for-modularity.pdf`.
Author list verified off page 1: **Deepak Mishra, Phillip M Rivera, Allen Lin,
Domitilla Del Vecchio & Ron Weiss**, *Nat Biotechnol* 32, 1268–1275 (2014).
**In *S. cerevisiae*, not *E. coli*.**

## 6.1 · The construct, and why it belongs in this course four days after S18

From the Figure 1 caption, read in full:

- **Unbuffered:** DOX induces **SKN7m**, which binds **PTR-SSRE** → GFP.
- **Buffered:** DOX induces **STAT5-HKRR**; JH1 phosphorylates it; it activates
  **YPD1** by **phosphotransfer**; two YPD1 doubly activate **SKN7**; ppSKN7
  binds PTR-SSRE → GFP.
- **The load** is **TR-SSRE promoter sites on high-copy 2µ plasmids**. Every
  other promoter is single-copy chromosomal. So the load is literally *extra
  binding sites*, which is p_tot in our model.
- Strain background: ***hot1Δ hog1Δ sln1Δ***.

**YPD1, SLN1, HOG1 and HOT1 are the same yeast osmolarity pathway session 18
already names from Mishra 2021** — same lab, same chassis, deletions of the same
cross-talk. **SKN7 is NOT, and this line used to claim it was.** Counted in the
Mishra 2021 text on 31 October: YPD1 34 occurrences, SLN1 46, HOG1 74, HOT1 37,
SKN7 **zero**. The deck already says four and not five; if a future pass finds
the deck and this file disagreeing, THE DECK IS RIGHT. The room meets these proteins on 27 October and meets them again on
5 November doing a different job. **Say so**; it is the cheapest continuity in
the week.

And the mechanism of the repair is **phosphotransfer** — session 18's covalent
cycle, used as the fast stage. The device that fixes retroactivity is the object
session 18 spent an hour on.

YPD1 and SKN7 were expressed at **6,325 and 2,572 protein copies per cell**
(75th and 53rd percentiles of yeast expression). *Kind: estimated from a
reference proteome dataset, not measured in these strains.*

## 6.2 · Box 1 — their model is ours with a different f

Box 1, transcribed:

```
dy/dt = G·(u(t) − y) − k_on·p·y + k_off·c
dc/dt = k_on·p·y − k_off·c
```

**This is the model in sections 1–5 with f(y) = G·(u − y) in place of
f(X) = k − γX.** The load driver's defining feature is that **G is large**.

Their result: the cutoff frequency — the ω at which the gain M drops to 1/√2 —
is **α·G**, with **α < 1** because of retroactivity. So:

> **α = 1/(1 + R) ONLY IN THE EMPTY-SITE LIMIT, and NOT as an identity.**

Box 1 prints α = (1 + p/K_d)⁻¹ with **p held constant**, i.e. free sites never
depleted. Our R is p_tot·K_d/(K_d + X)², which equals p_tot/K_d **at X = 0 and
nowhere else** — it falls as X⁻² once X ≫ K_d. So 1/(1 + R) reproduces their α
only where the sites are empty, which is the start of the approach and not the
operating point the session spends its hour on. Writing "α = 1/(1 + R)" flat is
the error this file used to make, and it would also hand the room a tidy
identity that **does not reproduce the measured bandwidth from the paper's own
parameters** (see the deck's segment 7 debrief, which inverts Box 1 to α = 0.80,
gets p/K_d = 0.25, and says plainly that the gap cannot be closed without their
Supplementary Note 1.2). **The deck deliberately declines this identity. Do not
"repair" the deck to match an earlier version of this line.**

What survives as the translation table is the shape, not the equality: their α
is a constant prefactor on bandwidth, our R is a state-dependent divisor on
rate; both say a load divides a speed, one in frequency and one in time. Their
sentence *"retroactivity reduces the cutoff frequency since α < 1"* is our
*"the load divides the rate by 1 + R"*, said once in frequency and once in time.

**And it is why the repair is on a different axis from the damage.** You cannot
change α — section 5 showed the load is the price of the regulation. You raise
**G** until α·G is still far above every input frequency you care about. The
load driver does not reduce the load; it outruns it.

## 6.3 · Step responses — the headline numbers, with their raw minutes

Rise time to 90% of maximum, means ± s.d., n = 3 (Online Methods):

| system | 0× load | 1× load | 2× load |
|---|---|---|---|
| **unbuffered** | **396.1 ± 23.0 min** | 474.6 ± 45.3 | **698.9 ± 47.9** |
| **buffered** | 432.4 ± 8.9 min | 420.2 ± 20.9 | 423.2 ± 21.5 |

Decay time to 10% of maximum:

| system | 0× load | 1× load | 2× load |
|---|---|---|---|
| **unbuffered** | 1,044.1 ± 31.2 min | 1,256.6 ± 19.4 | 1,364.6 ± 12.9 |
| **buffered** | 1,024.4 ± 36 min | 1,021.9 ± 38.5 | 1,043.6 ± 23.6 |

Their slowdown is **100% × (loaded − unloaded)/unloaded**, which gives the
abstract's figure:

- **unbuffered, 2× load: 76.5 ± 1.8%** — this is the "76% delay". 1× load gives
  **19.8 ± 4.5%**.
- **buffered, 2× load: 2.13 ± 2.94%** on rise and **1.88 ± 1.27%** on decay.
  Within error of zero.

**Teach the minutes, not the percentage: 396 min → 699 min.** The percentage is
a derived quantity with a denominator convention; the two times are measurements.

**An honest cost the abstract does not mention, and the deck should.** The
buffered system at 0× load is **432.4 min against the unbuffered 396.1** — the
load driver costs about **9% of response time when there is no load to drive.**
Insulation is not free. That is the right note to end the segment on, and it is
read straight off their own table.

## 6.4 · Bandwidth — and a figure that will be misread unless it is annotated

Figure 4c, unbuffered panel. **Rendered at 300 dpi and read off the plot**,
because the caption's text could not settle it:

- **0× load (unloaded): ≈ 0.0175 min⁻¹**
- **2× load (loaded): ≈ 0.0140 min⁻¹**

Load **reduces** the bandwidth, which is what Box 1 requires (α < 1).

⚠ **Two traps in this figure, both found by rendering it.**

1. **The caption's number order is reversed with respect to the plot.** It reads
   *"0.0140 min⁻¹ and 0.0175 min⁻¹ for the unloaded and loaded conditions,
   respectively"* — which would make load *increase* the bandwidth and
   contradict their own Box 1. The figure is unambiguous: the right-hand dotted
   vertical belongs to the black 0× curve, the left-hand one to the red 2×
   curve.
2. **The dotted-line colours do not match their curves.** The **dark-red**
   horizontal sits at **138 ≈ 195/√2**, which is the half-power level of the
   **black** curve; the **black** horizontal sits at **76 ≈ 107/√2**, the
   half-power level of the **red** curve. A student reading colour-to-colour
   gets the result exactly backwards. **Do not crop this panel without
   annotating it**, or redraw it.

The reduction 0.0175 → 0.0140 is **20% of the unloaded value** and **25% of the
loaded value**; the paper reports *"a 25% bandwidth reduction"*, so it used the
loaded figure as denominator. **The slide says "the unloaded system is 1.25×
faster" and gives both numbers**, which is true under either convention.

Buffered: **0.0142 (0× load)** and **0.0143 (2× load)** — the paper's
*"negligible (0.5%)"*.

## 6.5 · The rest of the periodic-input result

For the waveforms tested (50 min on, periods 150/200/250/350/500 min), load on
the unbuffered system gave **~50-min phase lag** and a **44–81% decrease in
peak-to-peak amplitude**. The buffered system showed **almost no phase lag** and
**4–12% amplitude deviation**.

## 6.6 · Still open

~~Nothing in section 6 is unverified.~~ **Settled 31 October, and both halves
of what used to be here were wrong.** Figure 4c is not reproduced; what ships is
our own plot of the four values, labelled as ours in the slide foot and inside
the figure. Their points are **not** overlaid on a derived curve — panel b is
simulation from a fitted parameter set, so that curve was fitted through them by
construction and drawing it that way would be circular. And α = 1/(1+R) is **not
an identity** to make visible in one picture; see §6.2 above, which this
paragraph used to contradict two hundred lines further down.
