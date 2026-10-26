# Session 21 — rebuild spine, 26 October

Written after four adversarial reviews (correctness, pedagogy, presentation,
voice) against the 25 October deck. The correctness review found that the hour's
headline claim does not apply to the paper the hour builds to. This document is
the corrected spine. It supersedes `DESIGN.md` §3–§4 and `NUMBERS.md` §4–§6
where they disagree.

Every number below was re-derived independently on 26 October by integrating the
two-state binding kinetics (`scipy` LSODA, rtol 1e-11) and, where a closed form
is claimed, by checking the closed form against those kinetics. Agreement is
stated per claim.

---

## 1 · What was wrong

The old spine said: a downstream load costs you **two** things, level and speed,
in **one** ratio p_tot/X_T, **independent of affinity** — and Mishra 2014
confirms it.

Four defects, each verified:

1. **The two costs live in different models.** The level cost exists only if the
   bound complex is diluted or degraded. The speed cost exists either way. The
   old slides computed the level shift in one model and the slowdown in the
   other and reported them as one result.
2. **Mishra's system has no level cost, and they say so.** p. 1273: *"neither the
   inclusion of the load driver nor the presence of load affected the final
   steady state… consistent with a system in which the interconnecting species
   (SKN7m) is protected from degradation when bound to DNA."* These are
   exponentially growing cultures. Slide 4 asserted the opposite.
3. **"Independent of affinity" is true of the speed cost and false of the level
   cost.** The level cost carries an explicit occupancy factor in K_d.
4. **α = 1/(1+R) was recorded as an inference. The paper prints α.** Box 1,
   p. 1270: *"α = 1 for the unloaded system and α = (1 + p/K_d)⁻¹ for the loaded
   system, where K_d = k_off/k_on."* That is our R evaluated at **empty** sites,
   not our R.

## 2 · The corrected spine

The two models are not a caveat. They are the hour.

**The object.** A factor X made at k, diluted at γ, with p_tot downstream binding
sites. Bound complex C(X) = p_tot·X/(K_d + X). Retroactivity
R(X) = dC/dX = p_tot·K_d/(K_d + X)².

**Model A — the complex protects X from degradation.**
d(X + C)/dt = k − γX. Steady state **X_ss = k/γ exactly, at every load.**
Reduced equation dX/dt = (k − γX)/(1 + R).
*Verified:* X_ss = 1000.000000000000 at p_tot = 0, 10, 100, 1000, 3000
(relative deviation ≤ 1.1e-16).

**Model B — the complex is diluted with everything else.**
d(X + C)/dt = k − γX − γC. Steady state **X + C = k/γ**: free X falls by exactly
the number of molecules parked on the sites.
Reduced equation dX/dt = (k − γX − γC(X))/(1 + R).
*Verified:* |X + C − k/γ| ≤ 3.4e-13 at every load tested.

**So which costs you pay is an experimental question, and it has a one-line
signature: measure the steady state with and without load.** No change →
protected. Change → not. This is the move the hour is built on, and it is the
move the room can make.

### 2.1 · The speed cost, and why affinity does not touch it

Both models slow down. In Model A the target is load-independent (X_ss is always
k/γ), so the half-time integrates in closed form:

    slowdown − 1 = (γ/ln 2) · ∫₀^{X_T/2} R(X) dX / (k − γX)

*Verified:* against the full kinetics at K_d ∈ {0.01, 1, 100} × p_tot ∈ {10, 300,
1000} — agreement 9.3e-10 to 3.5e-7 in all nine cells.

The reason affinity barely matters is a **conservation identity**, not a
coincidence:

    ∫₀^∞ R(X) dX = ∫₀^∞ (dC/dX) dX = C(∞) − C(0) = p_tot

*Verified:* 1.000000000 for every K_d × p_tot combination tested.

**The total extra material the loaded system must synthesize is p_tot, whatever
K_d is.** Affinity decides *when* during the approach you pay it, not *how much*.
That is the sentence the thesis slide should carry.

And it gives the weak-load limit by a three-line physical argument rather than a
fit. If K_d ≪ X_T the sites are full well before half-max, so by then the loaded
system has made p_tot extra molecules. At rate k that costs p_tot/k. The
unloaded half-time is ln2/γ. Therefore

    slowdown − 1  →  (p_tot/k)·(γ/ln 2)  =  (p_tot/X_T)/ln 2

**The 1.45 is 1/ln 2 = 1.442695.** *Verified:* at p_tot/X_T = 0.01, the
coefficient runs 1.448326 (K_d=1) → 1.443591 → 1.442818 → 1.442711 → **1.442697**
(K_d=1e-4).

Six files currently call this coefficient "MEASURED and NOT derived," and
`DESIGN.md` §3 proposes deriving it as a 247 exercise. It is three lines and it
belongs on the board.

**The boundary falls out of the same argument.** When K_d ≳ X_T the sites never
fill during the approach, so the system never pays all of p_tot — which is why
the effect dies at K_d ≈ X_T, the crossover already recorded in `NUMBERS.md` §5.
Same mechanism, now explained rather than observed.

### 2.2 · The level cost, which affinity does touch

Model B only:

    level shift = (p_tot/X_T) · θ,    θ = X_ss/(K_d + X_ss)

*Verified exactly* (ratio 1.000000 at every K_d ∈ {0.01, 1, 10, 100} × p_tot ∈
{10, 300, 1000}).

**Sites per molecule, times how full they are.** Never "exactly p_tot/X_T" — that
is the saturated limit. At p_tot = X_T, K_d = 1 the shift is 0.969, not 1; at
K_d = 100 it is 0.730.

So the two costs are **not** one ratio. They differ in exactly the interesting
way:

| cost | scales with | affinity | exists in |
|---|---|---|---|
| speed | total sites p_tot | **blind**, by conservation | both models |
| level | sites *occupied*, p_tot·θ | **dependent**, via θ | Model B only |

That is three true derived statements replacing one false one, and the contrast
is the payoff of the derivation.

## 3 · Mishra 2014, read honestly

The paper is Model A, measured, with the mechanism named (§1 item 2). So the
paper pays **only** the speed cost — which is precisely what it reports:
response time and bandwidth, never levels. The question `NUMBERS.md` §6.6 left
open — *why does this paper measure time and not levels* — is answered in the
paper's own sentence on p. 1273. It was open because the extraction missed it.

**Numbers, all verified against the PDF:**

- rise time, unbuffered: 396.1 ± 23.0 (0× load) → 698.9 ± 47.9 (2×), s.d., n = 3
- rise time, buffered: 432.4 ± 8.9 (0×), 420.2 (1×), 423.2 ± 21.5 (2×)
- bandwidths, unbuffered: 0.0175 and 0.0140 min⁻¹ — **the Fig. 4c caption states
  these in the reverse order; `NUMBERS.md` §6.4's correction stands** (I re-read
  the panel at 200 dpi: the right-hand vertical at 10^−1.76 drops from the
  unloaded curve)
- bandwidths, buffered: 0.0142 and 0.0143 min⁻¹

**Three corrections to how the deck uses them:**

1. **The bandwidths are calculated, not measured.** Fig. 4c caption: *"Dotted
   lines correspond to calculated bandwidths."* Fig. 4b is simulation from a
   fitted parameter set. The amplitudes are the measurement. The figures-module
   rule is that measured points are markers and model output is a line, so these
   four may not be markers.
2. **"A quarter of the bandwidth gone" is 20%.** 1 − 0.0140/0.0175 = 0.200. The
   paper's 25% uses the loaded value as denominator. `NUMBERS.md` §6.9 already
   wrote the instruction to give both numbers; the deck ignored it.
3. **The 9% insulation cost is not significant at n = 3.** 432.4 ± 8.9 against
   396.1 ± 23.0: Welch t = 2.55, **p = 0.097**. The buffered series is also
   non-monotonic in load (432.4 / 420.2 / 423.2), so its 0× value is the slowest
   of its own three. PS8 was going to grade a crossover calculation off this
   difference. Replace that item with *"is this difference real at n = 3?"* —
   which fits the measurement-literacy thread the course already runs.

### 3.1 · The α loose end — show it, do not paper over it

The paper's α = 1/(1 + p/K_d) is our 1/(1 + R) with **R evaluated at X = 0**,
i.e. in the limit where the sites never fill. Box 1's own eq. (1) writes
k_on·p·y with p held constant — no site conservation. Our model conserves sites.
The two agree in shape and disagree in regime, and the disagreement is not small:

- our R at the operating point (K_d = 1, X_T = 1000, 300 sites): R = 6.1e-4 →
  α = 0.9994, a 0.06% bandwidth loss
- our R at X = 0 (= p_tot/K_d): R = 300 → α = 0.0033
- what Fig. 4c gives: **α = 0.80**

Neither evaluation reproduces the measurement. The deck may not say "the same R
you derived this morning." What it can say, truthfully: *the paper's α is our R
in the empty-site limit; our saturating version does not reproduce their 0.80
from these parameters; the simple theory gives the shape and not the number.*

That is a better slide than a false identification, and it is a real 247 item:
reconcile the two, or show what measurement would distinguish them.

**[unverified]** Supplementary Note 1.2 is not in the held PDF (11 pp: article
1268–1275 + Online Methods). It may state α with site saturation. Until it is
read, the reconciliation above stands as the honest account and the deck says so.

## 4 · What this changes, file by file

**Deck.** Segment order unchanged through the derivation. Then: the two models
become the hour's hinge rather than slide 4; the thesis slide carries the
conservation identity instead of "four decades, same cost"; the two-costs slide
carries the three-row table in §2.2; the Mishra segment opens with the p. 1273
sentence as the *answer* to the models question; the α slide states the regime
mismatch; the bandwidth figure is replaced (§5).

**Also structural, from the pedagogy review:** the deck has 16 headered surfaces
against 36 for each of the two preceding taught sessions, and **zero** of the
four moves — no frame, build, release or debrief, no student work, no design
ledger. `docs/lecture-design.md` §5e: *"Every teaching segment is four moves, in
this order. None is optional."* Three releases go in: the steady-state signature
(which model are you in, from a measurement), the conservation identity, and the
n = 3 significance question.

**Figures.** `fig_affinity` keeps its Model A computation and gains an explicit
model label; its annotation becomes the conservation statement. `fig_both_costs`
is currently built and shown on no slide — it goes on a slide, redrawn to the
§2.2 table's logic, with the two curves labelled by model. `fig_bandwidth` is
**circular** — R is defined as 1/α − 1 from each measured ratio, so both points
lie on α = 1/(1+R) by construction, and the deck tells the lecturer to point at
that as evidence. Replace with the four bandwidths as calculated values against
load, no R axis, no derived curve. `fig_step_response`: axis label says
"time (1/γ units)" for an axis running 0–4 lifetimes; level number printed as
30% in the figure and 31% in two other places; its 1.51× slowdown is Model B and
appears in no NUMBERS section. Module docstring still carries the retracted
"level barely moves" claim.

**`posb/retroactivity.py`.** Defaults to Model B; docstrings describe Model A;
`slowdown()`'s stated 1.45 limit holds only for the non-default path; every
claim test passes `complex_decays=False` explicitly, so **no test covers the
default** a student gets from `slowdown(k, γ, K_d, p)`. Add the closed form, add
the conservation identity as a test, and cover both paths.

**`NUMBERS.md`.** Two sections numbered 6. §4's "measured not derived" is wrong.
§6.6's open question is answered. "Nothing in section 6 is unverified" is false
on its own terms. Decade count disagrees across three files (four / six / seven;
the sweep is `logspace(-2,5)`).

**PS8.** Q3 was built on the refuted affinity hypothesis and the crossover item
on a 1.5σ difference. Both change per §2.2 and §3 item 3.

**Cross-deck, from the pedagogy review and not yet fixed.** s21's ladder row 1
says session 18 taught that decoy sites *held* the factor and that is what made
it sharp. s18's own foot says *"No cooperative binding anywhere — the sharpness
comes from two enzymes being unable to go any faster,"* and its note says
*"nothing binds anything."* The first rung of the ladder this hour collects on
is wrong about what the room was taught. Separately, s20's derivation uses
`dim = n − rank S` for the flux null space, which is session 3's **left**
null-space formula; s3 taught `dim = r − rank S` for this one.

**Permanent fix.** s18 carries a cross-deck vocabulary grep in its docstring
(*"kinase 0, phosphatase 0, Michaelis 9"*). Neither s20 nor s21 ran one. It would
have caught the s18 error, the null-space collision, and that glycolysis, TCA,
pyruvate, biomass, knockout, vertex and bandwidth all have **zero** prior
occurrences in eighteen decks.
