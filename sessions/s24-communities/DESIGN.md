# Session 24 — The wire is now outside the cell

Tuesday 17 November 2026. Assigned at the close of session 23: Balagaddé et al.,
*Mol Syst Biol* **4**:187 (2008), and Basu et al., *Nature* **434**:1130–1134
(2005) — two required papers under the s23 override. Optional, all four
declared in `readings.yaml` with focus lines: Karig et al., *PNAS*
**115**:6572–6577 (2018); Tsoi et al., *PNAS* **115**:2526–2531 (2018);
Tamsir, Tabor & Voigt, *Nature* **469**:212–215 (2011); and Zhou, Qiao, Edgar &
Stephanopoulos, *Nat Biotechnol* **33**:377–383 (2015).

**Precedence.** If anything here disagrees with a built artifact, the artifact
is right and this file is stale.

**Revision note, 7 November.** Version 3. Version 1 is kept as `DESIGN.v1.md`;
version 2 came out of its adversarial review, which found four false statements
that would have reached the room, an assessed technique demonstrated nowhere, a
paper assigned and taught nowhere, and the session's best sentence wrong.
Version 3 closes version 2's own open list, §11, which had nine items; five of
them were real decisions rather than wording. §9 lists what changed in both
passes, and §11 now records how each item was decided.

The library this session imports is **built and green**: `posb/communities.py`
and `tests/test_communities.py`, 176 tests passing. §7 is written off the
module rather than ahead of it.

**Move 5 gained a technique later the same day.** T76 — decide whether to split
a pathway across strains — is now in `docs/coverage-matrix.md`, assessed by the
session 24 home guide and on the final rather than on PS9. §10 records the
decision; §7.4 specifies the guide item, which is the technique's only practice
vehicle; and move 5's release was rewritten, because the version that stood
before did not demonstrate what a guide item would ask.

---

## 0 · The title and the opening

**Title slide:** **The wire is now outside the cell.** Unchanged through both
reviews.
**Subtitle:** *Your signal now takes time to arrive and fades with distance.
Both are things you choose.*

**The main point:** for twenty-three sessions every connection in a circuit has
been a molecule inside one cell. The moment a signal leaves, the connection
acquires **a length scale and a delay**, and those become design parameters that
belong to the medium rather than the plasmid.

**The opening names three things:** that the wire has left the cell; that the
number now governing the circuit is a diffusion coefficient the room already
knows how to use; and that a population can therefore do things one cell cannot.

---

## 1 · Where this sits

Sessions 19–23 were a ladder of contexts that break a circuit, ending with
selection, which cannot be rejected. Session 24 inverts it: **the population
stops being what breaks your circuit and becomes what you build with.**

| session | the population is |
|---|---|
| 19–22 | coupling you did not design |
| 23 | the adversary |
| **24** | **the device** |
| 25 | the carrier |

---

## 2 · What the room has never seen

Census across all 22 built decks — `decks/s01*.py` through `decks/s23*.py`;
there is no s15 deck and sessions 24 onward do not exist yet.
`PRIOR-YEARS.md` §4 holds the first run. Every count below was recounted from
those sources on 7 November, because two earlier runs disagreed.

> **The standard this section counts under.** A count is of
> **slide-facing text only** — titles, segment headers, body text, the body
> text that loop data renders, and foot lines. **Speaker notes do not count**,
> and neither do file paths or module docstrings. The reason is
> `docs/lecture-design.md` §5b, which settled that a demonstration a student
> cannot go back and read satisfies the coverage rule for nobody — and a
> speaker note is instructor-facing by design. Totals
> including notes are given in brackets where they differ, because
> `PRIOR-YEARS.md` §4 reports totals and the two files have to be readable
> against each other.

**Session 10 taught a sender/receiver AHL circuit on slides.** Its slide-facing
counts: `AHL` **9** [15 with notes], `receiver` **4** [4], `sender` **2** [4],
`LuxR` **1** [2], and `LuxI` **0** [0]. Session 10 also read Basu *2004*, the
pulse generator, from the same laboratory, and taught coherent and incoherent
feed-forward loops properly: **8** slide-facing mentions of the loop, naming it
either "feedforward loop" or "FFL", **6** slide-facing mentions of Mangan &
Alon, and the sign rule twice. (Version 1 quoted `sender` 9, `receiver` 12,
`AHL` 24, `LuxR` 5, which are corpus totals across all 22 decks rather than
session 10's, and "14 hits" for the feed-forward loop, which no run reproduces.
The conclusion held both times; the evidence did not.)

**Zero occurrences anywhere, notes included, so these are zero under either
standard:** quorum sensing · autoinducer · acyl-homoserine lactone · LuxI ·
LasR · pattern formation · Turing · morphogen · lawn · consortium ·
co-culture · cross-feeding · mutualism · predator · prey · Lotka–Volterra ·
carrying capacity · chemostat · band-pass · length scale · division of labor
(searched under both spellings).

`dilution rate` has exactly **one** hit in 22 decks and it is a session 20
speaker note, so it is zero slide-facing — which is why the chemostat row
below is a row and not a callback.

So the gap is not the signal. **It is the synthase, the arena, the second
population, and the word quorum.**

| object | why it cannot be words |
|---|---|
| **LuxI** | session 10's slide says a sender "makes AHL", and never names or draws the enzyme that makes it |
| **a plate, a lawn, a sender disk** | the room has never seen one, and every spatial intuition this hour needs is a picture of one |
| **a chemostat and a dilution rate** | the predator–prey result is a statement about a reactor |
| **two populations in one vessel** | two cells, two arrows, before any model |

**Three collisions to disarm:**

- **Session 10 already gave distance a meaning**, on a slide: *distance is the
  rate of rise*. This session wants distance to mean a steady-state
  concentration. Say which, and when it changed.
- **Session 10's 47 nM is a saturation level, not a threshold.** Its slide reads
  that above about 47 nM the output stops growing — more signal, no more output.
  Version 1's retrieval question asked what the receiver did *above* 47 nM as
  though it were a switch-on. That turns a saturation into a threshold in the
  first question of the hour.
- **The dilution rate D** is not session 22's controller gain and not session
  25's antiviral fraction two days later.

**Cheapest new mathematics:** Lotka–Volterra. Recounted slide-facing, with
totals in brackets: nullcline **20** [24], fixed point **24** [28], Jacobian
**14** [16], eigenvalue **11** [20], phase plane **11** [15], bifurcation **4**
[10]. All of it is in hand.

> **Which of the two runs to believe.**
> `PRIOR-YEARS.md` §4 reports Jacobian **22**; six of those hits are image
> filenames of the form `s14_jacobian_stage1.png`, which nobody reads. Excluding
> file paths gives 16 total and 14 slide-facing, and the other six machinery
> rows reproduce `PRIOR-YEARS.md`'s totals exactly. **Take the counts above.**
> The only row where the standard changes the teaching conclusion is
> `bifurcation`: 10 total but 4 slide-facing, three of which are session 9's,
> so the room has met the word on a slide and has not met it often.

**The Hopf, stated under the same standard.** Session 11 computed the crossing
for the repressilator and the room watched it: the eigenvalues, the bisection
sweep, and a slide that says the amplitude "grows continuously out of zero —
like √(α − α_c) near onset". Its slide foot reads
`posb.sweep, posb.leading_real_part, posb.hopf_boundary — and you write the
loop yourself on PS5 before you import ours`. Locating that boundary
numerically by parameter sweep is session 11's technique T29, and it is
autograded on PS5.

**So the room has done the thing. The word is thinner than that.** Counted
slide-facing, `Hopf` is **0** across all 22 decks. It reaches students three
ways and all three are the function name: session 11's foot line above, and
PS5's Question 5, which says `hopf_boundary` three times and is itself headed
*Find the boundary without the algebra*. In prose the word appears only in two
session-11 speaker notes, which nobody reads. **Session 24 is therefore the
first student-facing text in this course to say "Hopf bifurcation" in words**,
to a room that has already located one numerically and been graded on it. Say
it that way round. What is new in the mathematics is
**deriving the crossing analytically for a two-population community**, against
session 11's numerical sweep of a ring of three — and the crossing turns out
not to be where the room will first look for it, which is move 4's whole
shape.

---

## 3 · The five moves

### Move 1 — A molecule that leaves

FRAME on **Basu Fig. 1a**, which already draws what version 1 proposed to
hand-draw and then show later. The caption says what is in it: the AHL and
protein levels at high, medium and low AHL (top left), "approximation of the
AHL gradient as a function of the distance from the senders" (bottom left), and
the protein activities in cells at three distances from the senders (right).
Show the paper's object first.

> **The synthase is not in Fig. 1a, and it is the one thing §2 says cannot be
> words.** Fig. 1a's caption labels the sender's response proteins
> "constitutively expressed" and names no synthase. `luxI` appears in the
> **sender plasmid map, Fig. 1b**, and in the Methods: *pSND encodes LuxI
> controlled by* P<sub>LTet-O1</sub>. So the frame is Fig. 1a **and** Fig. 1b,
> and `basu2005_fig1b` is in §7.3's crop list for that reason.
>
> **And do not say TetR drives LuxI.** An earlier version of this design did.
> P<sub>LTet-O1</sub> is a TetR-*repressed* promoter, the strain is DH5α, and
> there is no TetR in it — which is why the caption calls the sender's
> expression constitutive. The promoter's name carries a repressor the
> construct does not use.

BUILD. Two things follow from a molecule being outside:

- **It reports density.** One cell's AHL is undetectable; a population's is a
  concentration, and no cell counts anything. The two assigned papers bracket
  the range between them: Balagaddé's microchemostat holds **10² to 10⁴ cells**
  in 9 nL against **≥10⁹** in a macroscale culture, and their detection limit
  is **~75 cells per reactor**. **With a threshold**:
  Karig's SI gives measured half-activation thresholds of **0.003 µM** for
  3OC12HSL and **3 µM** for C4HSL, each for its own cognate signal — two
  homologous systems a thousandfold apart in sensitivity. **And they are still
  not orthogonal**: Karig's SI §4 is titled "Signal Specificity and Competitive
  Inhibition" and measures 3OC12HSL competitively binding RhlR. Orthogonality
  in their circuit comes from promoter choice, not from the threshold gap. An
  earlier version of this design asserted the opposite, and the paper it cited
  measures the crosstalk it was said to rule out. **Draw this on their own
  Fig. 1A**, whose caption names the competitive binding, so the thousandfold
  gap and the crosstalk are on one slide rather than in two sentences. Version 1
  asserted density sensing in one bullet with no model, no threshold and no
  number, for the first topic in the session title.
- **It reports position**, which is move 2.

**Then write the model.** Sender/receiver model construction — technique T64 —
is assessed on PS9 **and on the final**, and version 1 tagged it on no slide and
demonstrated it nowhere. The minimal pair, written with the room:

    sender:    dA/dt = k_I·S − γ_A·A   (− D·A in a reactor)
    receiver:  output = Hill(A)

Both papers refuse to supply the sender rate — Basu's model is receiver-only and
its Methods tune the senders to put a ring at 7 mm without printing a value, and
Balagaddé's equations are in a supplement this repo does not hold. **So the
session supplies k_I itself and says that it is doing so**, which is honest and
is also the engineering consequence segment 1 otherwise lacks: k_I is a
promoter choice.

RELEASE — a different object: a receiver whose output is an *antidote* rather
than a reporter. Write its equation. DEBRIEF immediately.

### Move 2 — How far the signal gets

FRAME: session 2's own slide, quoted — t ~ L²/2D, with its standing instruction
to state the convention before the number. The room has used it three times
already; session 3 used it to argue there is **no** spatial gradient worth
speaking of inside one cell.

BUILD, with `derivation_fig` beside it.

**A community is where that inequality turns over**, because L changed by four
orders of magnitude. The numbers, from Karig's main text, both of them:

| molecule | D | where |
|---|---|---|
| 3OC12HSL | **83 µm²/s** | effective cell-to-cell, through a lawn |
| C4HSL | **1,810 µm²/s** | the same measurement, the other signal |
| GFP in *E. coli* | 7.7 µm²/s | session 2 |
| GFP in water | 87 µm²/s | session 2 |

> **Say what 83 is, because version 1 did not.** It is an *estimate*, obtained
> by fitting a fluorescence wave profile — a modelled number resting on
> measurement, not an instrument reading. It is an **effective cell-to-cell**
> coefficient through a bacterial lawn, slowed by 3OC12HSL partitioning into the
> membrane; the free-solution prediction for the ratio is only about 1.5, and the
> measured ratio is 21.6 ± 10. Version 1 put 83 beside session 2's 87 for GFP in
> free water and said the signal "travels at about the speed of a protein in
> water". Those are physically unlike quantities and the coincidence is not a
> result. **And 83 is 3OC12HSL — neither of Basu's signals.** Version 1 applied
> it to Basu's 10 mm ring, which is the wrong molecule for that geometry.

**The ratio is where Turing arrives.** A Turing instability needs the inhibitor
to diffuse faster than the activator, and **how much faster depends on the
kinetics** — the critical ratio falls out of the Jacobian of whatever scheme
you assume, so there is no universal number. For *their* scheme, Karig's SI
reports that the constants must be separated by a factor on the order of 100
**in their non-stochastic simulation**. They measured **21.6**, and got patterns
anyway, because noise does work the deterministic theory does not account for —
their abstract says the stochastic version puts "no severe requirement on the
ratio". The prior-year deck carried this as a bare bracket, *>100× required,
20× measured*, stated and never attributed. **Attribute it to their
simulation.** An earlier version of this design called the 100 a classical
requirement and proposed that the room derive it, which cannot be done without
naming a kinetic scheme. `readings.yaml` carried the same error in Karig's focus
line and it is corrected there.

**And say what kind of knob the ratio is, because §4's ledger has to agree with
this slide.** A diffusion coefficient is not a dial. You pick a signal and you
inherit its coefficient in the medium you have. What a designer sets is **which
pair of signals the circuit uses**, out of a short menu — and Karig's own
numbers say the menu matters less than the cells do: Wilke–Chang predicts a
free-solution ratio of about **1.5** for their pair, and through the lawn they
measured **21.6 ± 10**. The factor of roughly fourteen between those is a
property of cells, not of molecules. So: **the pair is a choice, the
coefficients are inherited, and the lawn is where most of the ratio came
from.**

**The design knob, taught as a formula and not as a number.** Basu hands the
physics over on p. 1134: γ_A sets the steepness of the gradient and is
pH-sensitive. So a signal that decays as it spreads has a penetration depth

    ell_A = sqrt(D / gamma_A)

and **γ_A is the knob** — you change it by changing the medium.

> **This folder cannot give you a number for ℓ_A.**
> Combining Basu's γ_A with Basu's ξ gives 0.32 mm — but ξ is not a diffusion
> coefficient (see below), so that number inherits ξ's defect, and
> `NUMBERS.md` §13.4 runs exactly that arithmetic as a *reductio against* ξ:
> 0.32 mm against a 7 mm band is 22 e-foldings. Combining it with Karig's
> 83 µm²/s gives 0.71 mm, but that is a different signal measured in a
> different lawn. **There is no sourced D in this folder that can legitimately
> be put with Basu's γ_A.** Teach ℓ_A = √(D/γ_A) and say what it would take to get
> a number for it. An earlier version of this design computed 0.32 mm and
> presented it as a design knob, six lines above the blockquote forbidding the
> number it came from.

> **The cautionary tale.** Basu prints
> ξ = 0.001 mm²/min for AHL. Substitute it into L²/2ξ and their own 10 mm ring
> takes **833 hours** against a 36-hour experiment. Their equation (5) is a bare
> discrete Laplacian with no grid spacing, so ξ is really D/Δx² and Δx is never
> stated — the published number is off by **one to two orders of magnitude** as
> a diffusion coefficient. Version 1 said "a factor of twenty", which is the low
> end. **Do not take a diffusion coefficient from a paper without checking its
> units against the paper's own geometry.** That is T66's engineering lesson and
> it is better than any number.

RELEASE — a different object, a signal pair the session has not used. *You have
two signals whose free-solution diffusion coefficients differ by a factor of 3.
Name two things you could change to widen the ratio the circuit sees,
and one reason you might get a pattern without widening it at all.*

> **Why the question was rewritten.** It used to read *diffusion ratio of 3,
> what would you change and which direction?*, which expects "raise it" and has
> no written answer in the folder. At a ratio of 3 the honest answer is that you
> cannot tell from the ratio, and the question now asks for that.

**DEBRIEF, immediately, on two slides, because the answer has two halves.**

1. **Where a ratio comes from.** The free-solution ratio is close to fixed by
   molecular size — Wilke–Chang gives about 1.5 for Karig's pair. They
   measured 21.6 ± 10 through a lawn. So the two things you change are the
   **signal's interaction with the cells** and the **lawn itself**: Karig
   attribute their slow signal to 3OC12HSL partitioning into the membrane, and
   they hedge it — "likely due to" in the main text, "one possible
   explanation" in the SI. Say it hedged. The number you can move is the
   *effective* coefficient, not the molecule's.
2. **Why you might not need to widen it.** There is no universal ratio to hit.
   The critical ratio comes out of the Jacobian of your kinetics, and for
   Karig's scheme their own non-stochastic simulation wanted about 100 — they
   measured 21.6 and got patterns, because their populations are small enough
   that noise does work the deterministic analysis leaves out. **So the answer
   to "is 3 enough" is: not answerable from the ratio. Name your kinetics, then
   ask how big your population is.**

The engineering lesson of the hour's length-scale technique (T66, the diffusion
length scale in a community) is this and the ξ arithmetic above, not a number.

### Move 3 — The same motif reading a new input

FRAME: Basu's printed truth table in Fig. 1a — AHL high/medium/low against CI,
LacI_M1, LacI and GFP, with GFP on only in the middle. **Non-monotonicity as a
logical fact, before any kinetics.**

BUILD, the three cases, one slide each, in the paper's own words:

- **Close:** AHL high, both repressors high, GFP off.
- **Far:** AHL low, both at basal levels — which *enables* wild-type LacI from
  the second plasmid, and GFP is off again.
- **Between:** CI shuts off wild-type LacI while LacI_M1 is still below the
  threshold that would silence GFP. **GFP on.**

**Then the callback, at the strength it supports.** The paper calls this a
feed-forward loop beginning with LuxR and ending in GFP, and session 10 taught
feed-forward loops. **Same topology — different consequence.** Session 10's
pulse in time came from a *slow arm*, a kinetic delay. Basu's band in space
comes from **two repression thresholds far apart**: β_L = 0.8 µM against
β_C = 0.008 µM in the printed BD2 parameter set, a factor of 100. **What makes
the response non-monotonic is β_C ≪ β_L**; the hundredfold is BD2's value, not
a requirement. Basu's own Figs. 4b and 4c form rings at ratios of 28.6 and 3.3,
and BD1 and BD3 differ from BD2 in ρ_R, α_G, α_L2 and [LuxR] with β untouched.
An earlier version of this design called the hundredfold "the only thing the
band rests on", which the same paper refutes twice.

> Version 1 said *"the ring is the pulse, drawn in space"* and called the two
> one motif reading two inputs. That is false as mechanism: session 10's object
> is a kinetic delay producing a transient, this is a non-monotonic
> steady-state dose–response, and `s10_feedforward.py` contains zero
> occurrences of "band" or "non-monotonic". The wiring transfers; the mechanism
> does not. The corrected sentence is a better slide because it names a
> parameter.

**Solve the two edges**, from equations (1)–(4) in the liquid-phase limit the
paper defines by dropping equation (5), with β_L and β_C on the slide. This is
the session's band-detect analysis technique, T65, assessed on PS9; version 1
tagged it on a naming slide that demonstrated nothing. `posb.band_edges` solves
it rather than reading it off a plot, and on the printed BD2 set the two
half-maximum edges sit at 2.61 × 10⁻³ and 6.93 × 10⁻³ µM, a factor of 2.65
apart, with the peak at 3.97 × 10⁻³ µM. Those are properties of the printed
parameters in that limit and not of the measured strains, and the slide says
so.

**Then the knob, because the ledger claims it.** Basu did not take one band and
describe it — they built three receivers that band in three different places,
and the model says exactly what they changed. BD1 is BD2 with ρ_R tenfold
higher, which is how the paper represents the hypersensitive **LuxR-G2F**
mutant, and nothing else changes. BD3 is BD2 with α_G, α_L2 and [LuxR] halved,
which is the **halved plasmid copy number**. **A receiver's detection threshold
is set by a point mutation in a receptor and by a copy number**, and that is the
slide the session's "deliberately tuned" claim rests on.

Put their **measured** triple, Fig. 2d, beside the three curves
`posb.band_detect_response` draws from `basu_params("BD1")`, `("BD2")` and
`("BD3")`. Our curves stand in for their Fig. 2c, which is their *simulation* of
the same printed model — so the slide loses nothing, saves a crop, and is exact
where a crop would be approximate. **What the slide claims is the ordering and
the spread**: the three bands sit in the same order in the model and in the
data, and they span 0.85 decades computed against about a decade measured.

> **What the slide must not claim is an absolute position, and the reason is a
> defect this pass found.** `NUMBERS.md` §8.3's digitized AHL positions for
> Fig. 2c are a uniform factor of **6.8** above what the printed parameters
> give, while the peak *heights* and the *spacings* agree to three digits — so
> the digitization's x calibration is off by 0.83 decades, not the model.
> §8.4's measured positions were calibrated the same way and are in the same
> doubt, and with them §8.4's old claim that the data sit "2–3× above" the
> simulation, which an earlier draft of this move repeated. **Teach ordering and
> spread; teach no absolute AHL number off those panels** until the two panels
> are re-digitized. The computed edges above are safe because they come from
> printed parameters, and they are pinned in the test suite.

**The counterintuitive part is not the one version 1 named.** The
high-detect component sets the upper edge and the low-detect the lower, exactly
as the names suggest — version 1 said the names were backwards and they are not.
What *is* counterintuitive is that **a high-detect strain on its own is an
inverter**: Fig. 2b shows the three HD strains inversely correlated with AHL,
dark at high signal and bright at low. The band is two inverted responses
overlapped.

**The wrong turn, and it is in a *Nature* abstract.** The abstract says
experimental and theoretical analyses reveal which kinetic parameters most
affect ring development. The analysis is 100 simulations drawn from 2,000
random parameter sets, regressed **against their own inputs** — γ_L against
shift-begin R² = 0.91, CI repression efficiency against positional shift
R² = 0.05, everything else R² < 0.001 with P > 0.75. No experiment enters the
regression. Show it, ask what was measured, let them find it.

RELEASE — a different object: a band detector built from two *activators*
instead of two repressors. Can it band? DEBRIEF immediately.

### Move 4 — Two populations

FRAME on **Balagaddé Box 1A**: two strains, each controlling the other's
survival — the predator kills the prey by inducing a killer protein, the prey
rescues the predator by inducing an antidote.

BUILD, over eight step slides. Version 1 gave the whole of it one segment row;
session 11 gave an object of the same size eight numbered steps, and this one
carries the session's only eigenvalue argument.

1. the two logistic growth terms sharing a carrying capacity
2. the cross-death terms, each modulated by the **other population's signal**
3. the dilution rate, common to both — and note that writing the signals down
   doubles the number of places it appears, from **two** to **four**: it leaves
   with each population and it leaves with each signal
4. **the signals get their own equations**: made in proportion to the
   population that makes them, removed by decay *and* by dilution
5. **Try to get rid of them.** Session 4's QSSA: the signals are fast, so set
   them to steady state — A₁ = k_A1·C₁/(d_AA1 + D), A₂ = k_A2·C₂/(d_AA2 + D),
   in the deposit's own symbols — and the system collapses to two states in C₁
   and C₂ alone
6. the nullclines and the Jacobian of that 2×2 system, **drawn as a matrix**
7. **the trace, and the shock**: at any interior fixed point the logistic terms
   cancel against the death terms and tr J = −(k_c1·C₁ + k_c2·C₂)/C_m exactly —
   **strictly negative, for every parameter value.** This system cannot
   oscillate. There is no Hopf to find
8. **so put the signals back.** The oscillation was in the lag between a
   population and its own signal, and the QSSA threw it away. Restore the four
   states, find where the leading real part crosses zero, and name it: **a Hopf
   bifurcation**, pointing back at session 11's ring of three

> **The dead end in this move is what fixed it.** The design
> originally specified the two-state model and asked the room to find a Hopf in
> it. There is none — proved above and verified numerically over 4000 random
> interior fixed points. The fix is better than the original: **the room applies
> an approximation it already knows, watches the phenomenon disappear, and
> learns that the approximation was the thing that killed it.** That is the same
> result as session 11's repressilator and as T30 — delay drives oscillation —
> arriving in a new substrate, and it is a far sharper lesson than finding a
> crossing where one was promised.

> **Whose model this is.** Settled on 7 November, and the answer changed. The
> *paper* prints no equations; they are in a supplement this repo does not hold.
> The model is deposited in **BioModels as BIOMD0000000296**, and reading that
> deposit settles it: eight reactions, four state variables, and every rate
> constant. `NUMBERS.md` §20 has them. **IPTG enters through exactly two
> assignment rules** — it tunes the prey's signal synthesis and the predator's
> death rate and nothing else — which is why the paper's own route across the
> Hopf is IPTG rather than dilution.
>
> **The deposit is the paper's model, not a course reconstruction.** Run from
> the deposited constants it reproduces the paper's own Fig. 3C to three
> digits: the oscillatory branch opens at D = 0.03673 against their printed
> 0.035–0.04, the upper crossing is at D = 0.16743 with a period of 73.6 h
> against their ~73 h at ~0.168, and coexistence is lost near D = 0.176 against
> their washout above 0.18. So **two things are true at once and a slide has to
> keep them apart**: the *structure* is what the room writes from Box 1A, which
> is the session's own construction and the point of the model-construction
> technique (T64); the *equations and every constant* are the deposit's, which
> is a different provenance from the paper's text. Label the equations
> "BioModels BIOMD0000000296, curated from Balagaddé 2008" — never "the
> paper's", which prints none, and no longer "ours", which the three-digit
> agreement above refutes.
>
> What the paper does print is Box 1B's axes — predator growth rate k_c1 and
> death rate d_c1, both in h⁻¹, with traces at 0.2, 0.8 and 1.2 — and the
> dilution rates. Version 1 said the paper "prints no rate constant of any
> kind", which is false and was contradicted by the figure version 1 itself put
> on a slide.

**The design consequence, corrected.** Box 1B's bifurcation plane is spanned by
two *strain* parameters, and the paper's own experimental route across the Hopf
is **IPTG**, not dilution. So the regime depends on the strains **and** the
reactor; D is the parameter you can still change after the strains are built.
Version 1 said the oscillation is "not a property of the strains", which Box 1B
refutes.

**Show Fig. 2C** — the paper's own bifurcation diagram against a knob the
experimenters turned, with the period inset. Version 1 dropped it, which left
the session's eigenvalue argument without the paper's version of it.

> **Where the paper says "Hopf". CORRECTED 8 November — this block previously
> said the opposite.** Fig. 2C **does** print the word, in bold, immediately
> beside the green branch-point dot. The earlier claim that the dot was
> "unlabelled" came from a 200 dpi rendering that could not resolve it;
> `NUMBERS.md` §3.3 now records the correction and the resolution it was found
> at. The Fig. 2 **caption** still never uses the word — it says only
> "Bifurcation diagram of the predator density versus IPTG level" — and the
> word is also in **Box 1B's caption** ("a line connecting Hopf bifurcation
> points demarcates three regions") and three times in the Results. So Box 1B
> is where the authors draw the *locus* of Hopf points, and Fig. 2C is where
> they **cross** one with a knob and say so on the panel.
>
> Two more things to take off that panel while it is up: the inset's x-axis is
> printed **"IPTG (M)"** and the units are µM, which is a figure typo and must
> not be reproduced; and the axis warning — Box 1B is 10³ cells/µl, Figs. 2
> and 3 are cells per reactor, never on one axis.

**The honest reading of the data, and it is now a computation rather than a
digitization.** Fig. 2A is a single trace pair; the "several reactors" hedge
belongs to the Fig. 2B caption, not 2A's. Put 2A and 2B together: of the
induced reactors in 2B, several show prey high and predator flat across 200
hours.

Then run the deposited model at the five dilution rates the authors ran, and
put it beside what they saw:

| D (h⁻¹) | what they observed | the model |
|---|---|---|
| 0.11 | coexistence, steady | **oscillates**, 168 h |
| 0.15 | coexistence, steady | **oscillates**, 122 h |
| 0.20 | damped oscillation, ~50 h | **no coexistence state at all** |
| 0.23 | damped oscillation, ~30 h | **no coexistence state at all** |
| 0.31 | predator washout | washout — agrees |

**Four disagreements out of five, in opposite directions.** Where the experiment
is steady the model oscillates; where the experiment oscillates the model has
already lost coexistence. And the timescale is wrong as well as the place: the
cycle the model settles into at D = 0.11 runs **168 h**, about 3.4× the slowest
oscillation the reactor ever showed, so nothing the model does at any dilution
rate resembles the experiment's 30–50 h damped oscillations.

**Close the loop before anyone calls it a transcription error.** The deposited
model reproduces the paper's *own* Fig. 3C to three digits — oscillatory branch
beginning at 0.0367 against their 0.035–0.04, upper crossing at 0.1674 with
period 73.6 h against their ~73 h at ~0.168. The model is faithfully the
paper's. It still disagrees with their experiment.

So the phrase to put in front of the room is the authors' own: the model
**"qualitatively accounts for"** the observations. Ask what that phrase is doing,
and let them find that it is carrying all of the above. Rule 6 — teach the
reading, why it fails, and what replaces it — and here the replacement is that a
four-state chemostat model of two engineered strains gets the *shape* right
and the *numbers* wrong, which is the honest standing of most models in this
course.

RELEASE — a different object: predict what happens to the predator if you double
the dilution rate, using the nullclines just drawn. DEBRIEF immediately.

**Poll, in this segment, with P pinned and options written out.** Split the stem
into the two questions, because that makes the model–data mismatch the subject
rather than a footnote: *what does the model predict* / *what did the experiment
do*. Version 1's single stem had three defensible options.

### Move 5 — When a second strain is worth it

Declare the change of question. The first four moves built communities; this one
asks when you should.

**This move carries a technique, decided 7 November 2026.** Deciding whether to
split a pathway across strains — technique T76 — is assessed by the **session 24
home guide and on the final**, and **not on PS9**, which stays at ten
techniques because it posts on 19 November. So the guide is T76's only practice
vehicle, and §7.4 specifies the item. Moves 1–4 each carry a technique; until
this decision move 5 ran five build slides carrying none, which
`docs/coverage-matrix.md`'s decision 13 makes a gap of the same kind as an
assessment with no demonstration. Adam's call was to close it by assessing the
move rather than by shrinking it. HAND-graded, because the answer is a design
argument with a stated criterion rather than an arithmetic result.

**What follows from that.** T76's demonstration is move 5's release and
debrief. They have to demonstrate the thing a guide item will ask — a stated
criterion applied to a named pathway — or the row asserts a demonstration that
did not happen. The release below was rewritten for that reason.

**Lead with the engineering reason, which needs no model.** Tamsir, Tabor &
Voigt build an XOR out of **three NOR gates and a buffer gate, one per *E. coli*
strain**, spotted onto an agar plate and wired together with AHL — and then
produce every one of the sixteen two-input Boolean functions from a small
library of such strains, by changing where the colonies sit. Their own argument for
doing it that way is the one this move wants: **a program can be built from a
smaller number of orthogonal parts (for example transcription factors) by
re-using them in multiple cells.** That sentence is in their introduction, not
their abstract, and `readings.yaml` pointed students at the abstract until this
pass. Session 17 spent an hour on how few orthogonal parts there are. This is
what you do about it.

**Name the wires, because this session has already insisted on it once.** The
XOR's wires are **3OC12-HSL** from LasI and **C4-HSL** from RhlI — which are
**not** Basu's 3OC6HSL, and saying "the same AHL the session opened on" would
repeat the error move 2 spends a blockquote correcting. They are instead
**exactly Karig's two molecules**, so the honest callback is to move 2: the pair
whose diffusion coefficients the room read off a table in the first half is the
pair Voigt's gates are wired with in the second.

The plate has numbers on it, and they are the cheapest slide in the move:
colonies spotted 1 µL each on a **7 mm** square grid, and each layer spotted
**12 h** after the one before "to ensure communication signals had propagated
sufficiently". The authors call that delay an **external clock** and say why
they need one: genetic computing is asynchronous, and mismatched delays produce
hazards — transient wrong outputs. A length and a time on the same plate.
**Do not turn them into a diffusion coefficient**: 12 h is stated as sufficient,
not as an arrival time.

> **The archive route to this is blocked; the paper is not.** `PRIOR-YEARS.md`
> §6 found this material in `20.405_LectureNotes.docx`, whose molecule names are
> equation objects that extract as blanks, under a standing instruction that
> nothing from those paragraphs reaches a slide until the file is opened in
> Word. **Citing Tamsir 2011 directly removes the dependency entirely**, and
> the primary paper carries more than the lecture notes did: measured transfer
> functions in Figs. 1c and 2, with printed inducer grids and error bars from
> three experiments, and induction ranging from 5-fold for the XOR to 335-fold
> for the B gate. They are measured and plotted rather than given as fitted
> parameters, so promise the curves and not a table.

**A composition failure that session 17 earns.** The
tandem-promoter gates behave as the **sum** of their two input promoters'
transfer functions, and the paper's prediction matched the experiment for six
of seven. The seventh, P<sub>Tet</sub>–P<sub>BAD</sub>, did not — and it is
P<sub>BAD</sub>–P<sub>Tet</sub> with the two promoters swapped in order. The
authors offer DNA looping, binding-site occlusion or output-mRNA stability and
settle none of them. A part that composes in one order and not the other is
session 17's subject arriving as a measurement.

**Then the experiment that shows what it costs.** Zhou, Qiao, Edgar &
Stephanopoulos split the paclitaxel precursor pathway across *E. coli*, which
makes taxadiene, and yeast, which oxygenates it. Neither can make the product
alone. The teaching value is that they report **both** versions, and the
mechanism of the first failure is what the second design acts on:

- **On glucose it falls over, and the agent is ethanol.** Taxadiene does cross
  into the yeast and does get oxygenated, but *E. coli* density and total
  taxane titer both fall when the yeast is present. The cause they identify and
  test is the **ethanol the yeast makes on glucose** — at the highest
  concentration they observed, 50 g/L, it stopped *E. coli* growth and
  taxadiene production outright. Say "the ethanol the yeast makes on glucose",
  not "the yeast": the fix removes the ethanol, not the yeast.
- **On xylose it holds, because each one removes the other's problem.**
  *E. coli* on xylose excretes acetate, which inhibits its own growth. Yeast
  cannot eat xylose at all but can live on acetate as its sole carbon source,
  and does so without making ethanol. So the yeast grows only when *E. coli* is
  there, the acetate falls, and the ethanol goes below the 0.1 g/L detection
  limit. The paper designed this and calls it a mutualistic relationship.

**And the number that keeps the slide honest.** Stability is what the second
design bought — not yield. Oxygenated taxanes went from 2 mg/L to 4 mg/L in
72 h, with only about 8 % of the taxadiene oxygenated. The headline 33 mg/L
needed three more pieces of engineering after that, and the last one is where
the ecology gets designed rather than discovered: they **knocked out `atpFH`**
to disable oxidative phosphorylation, so that making acetate became
*E. coli*'s primary route to ATP and it was forced to feed the yeast. Their own word for
the design goal is to **enforce** the cooperation. The species ratio then
regulates itself — inoculated at about 40:1 yeast to *E. coli*, it settles to
1:2 by 41 h, because yeast growth is limited by the acetate *E. coli* makes.

**That is the move's result and the session's thesis with an experiment behind
it:** splitting the job is the easy part, and the thing you have to engineer is
the ecology between the two strains. A community is two strains with a reason to
keep each other alive, which is what Balagaddé built in move 4 — the same
coupling, pointed the other way, with a toxin instead of a carbon source.

Then Tsoi's criterion, **stated with its assumption attached**, not derived:
splitting a pathway reduces the burden each population carries, and you pay to
move the intermediate between cells. Their Fig. 1C draws the two sides of the
inequality and is the slide — biomass gain against transport inefficiency.
Their Fig. 2D is the caveat: three functional forms for burden, three borders,
and the border moves by about **five-fold** between the linear form and the
Hill form. The caption's own words are that "parameters are chosen such that
Hill-type burden reduces growth the least and linear burden reduces growth the
most", so **the size of that spread is the spread of a chosen example**. The
*direction* is not a choice — 1/(1+Bⁿ) ≥ e⁻ᴮ ≥ 1 − B for every burden — and the
slide separates the two.

RELEASE — a different object, and **two named pathways rather than two kinds of
pathway**. Every number is printed on the slide, and each one says what quantity
it is:

> Both pathways are two enzymes in the same host. Burden is Hill-form with
> **n = 2**; the host has **μ_max/δ_υ = 10**.
>
> **A** — intermediate crosses freely: transport rate **η = 1.0**, extracellular
> turnover **δ_me = 0.001**. Burden **B₁ = B₂ = 1.2, per enzyme**.
> **B** — intermediate is charged and crosses slowly: **η = 1.0**,
> **δ_me = 0.5**. Burden **B₁ = B₂ = 1.3, per enzyme**.
>
> *Split one of them across two strains. Which, and what would you measure to
> be sure?*

> **"Per enzyme" is load-bearing and the slide must say it.** Read as a
> *pathway* total, A's two enzymes carry B = 0.6 each, which is far below its
> border — and the criterion then says **leave A alone**, the opposite verdict,
> reached by correct reasoning from an ambiguous stem. The release says per
> enzyme, the debrief repeats it, and §7.4 requires it of the guide item.

> **Why the question had to be rewritten.** It used to read *here are two pathways, one
> whose intermediate is membrane-permeable and one whose intermediate is not —
> which would you split?* **That does not demonstrate T76.** It names a kind of
> intermediate rather than a pathway, it can be answered on permeability alone
> without the criterion being used at all, and it exercises only the transport
> half of Tsoi's inequality. The version above forces both halves, because
> **the two pathways pull opposite ways**: B carries the higher burden, which
> argues for splitting it, and B's intermediate moves slowly, which argues
> against. A guide item can be written against this release; it could not be
> written against the old one.

**DEBRIEF, immediately and illustrated.** Evaluate the criterion for each, with
`posb.dol_criterion` on the slide. All four columns are per enzyme:

| | η, δ_me | ε = δ_me/η | θ_I | B₁=B₂ | its border | split it? |
|---|---|---|---|---|---|---|
| **A** | 1.0, 0.001 | 0.001 | 1.166 | **1.2** | **1.135146** | **yes** |
| **B** | 1.0, 0.5 | 0.500 | 1.116 | **1.3** | **1.355143** | **no** |

> **Why η and δ_me are printed and ε is not enough.** A first version of this
> slide specified each pathway by ε alone. **ε does not pin the border**, because
> θ_I depends on η and δ_me separately: sweeping η from 0.2 to 10 with δ_me
> held at 0.5η — every pair giving ε = 0.5 — moves the border by about **0.03**,
> from 1.338 to 1.366. The family is open, so that spread is what was sampled
> rather than a bound. The two transport numbers go on the slide, not their
> ratio.

**So the higher-burden pathway is the one you leave alone**, and "more burden
means split it" is the wrong rule used on its own. Slow transport moves the
border to higher burden: when the intermediate is expensive to move, the burden
has to be worse before splitting pays. **That direction is the shape of Tsoi's
own Fig. 1D**, where the border runs from a relative burden near 70 at the top
of their diffusivity axis to near 100 as diffusivity goes to zero — the same
way, in their own figure, as the two borders computed above.

**Both populations are alive in both cases**, which matters — this is the part
of the plane where the criterion is deciding something, not the white region
where the single cell has simply died of its own burden.

**What you would measure**, which is the half of the question that is not
arithmetic: the burden per unit enzyme times its expression level, which is
B per enzyme; the
host's μ_max/δ_υ, which is its resilience to carrying that burden; and, for ε,
the intermediate's transport rate η across the membrane against its turnover
δ_me outside the cell. Zhou is the worked case of the last one: their
intermediate crosses freely, and the thing they ended up engineering was not the
pathway but the reason each strain kept the other alive.

> **Three caveats that belong on the debrief slide, not in a footnote.**
> 1. **The burden numbers are ours, and they are not on Tsoi's axis.** 1.2 and
>    1.3 are values the session picked, evaluated with their criterion at
>    μ_max/δ_υ = 10 and n = 2, which the slide prints. They are **not** points on
>    Fig. 1D's "Relative burden" axis: that axis runs 0–120 with no units, and
>    putting its border position back through the paper's own Eq. 17 would need
>    μ_max/δ_υ ≈ 4 × 10⁴ at n = 2, which the paper nowhere supports. So the axis
>    is not the βe of Eq. 17 — which is our B — `NUMBERS.md` §12.1 now says
>    so, and **what
>    transfers between their figure and this slide is the direction the border
>    moves, not a number.**
> 2. **The border moves about five-fold with the burden functional form**, and
>    Tsoi's Fig. 2D caption says its parameters were chosen so that the Hill
>    form reduces growth least. A and B are compared under the *same* form, so
>    the comparison survives; neither border position does.
> 3. **Tsoi contains no experiment anywhere**, and their own best natural
>    examples do not decide: nitrification and syringate metabolism exist in
>    both single-cell and divided form, and the authors write that what
>    constrained the difference "remains an open question". **And one sentence
>    more, which is the honest end of the hour:** we cannot reproduce their own
>    Fig. 1D from their own inequality — the border they draw at a relative
>    burden of 70 would need a host with μ_max/δ_υ of order 10⁴, so the axis is
>    not the burden the criterion is written in. A computed verdict here is an
>    argument, not a decision procedure, which is exactly why T76 is
>    hand-graded. §10 records why this is one sentence rather than a segment.

**Why this move survived the review that recommended cutting it.** Both reviews
wanted division of labor cut, on the grounds that it had one optional modelling
paper behind it, no experiment anywhere, and a headline number that was our own
digitization of a chosen example. That was the right call against the material
the move then had. It now leads on two experimental papers — Tamsir for why you
would split a job at all, Zhou for what it takes to make the split hold — with
Tsoi demoted to the criterion it is. Both new papers are declared in
`readings.yaml` with focus lines, and `NUMBERS.md` §§21–22 now hold their
numbers, which they did not when the reviews were written. The move also has a
release and an immediate debrief, which it lacked against §5e's four-move rule.
§10 keeps the scope question open for Adam, because keeping the move is a
judgement about the hour's budget rather than about the sources.

---

## 4 · The design ledger

`docs/lecture-design.md` §5d. Version 1 had none.

Written last, as §5d requires, and **every Limits entry names the observable
that tells you you have left the limit**.

| | |
|---|---|
| **Knobs** | **k_I**, the synthase expression — a promoter choice, and the one number the session supplies itself because neither paper prints it. **γ_A**, the signal's decay, set by the medium and its pH, which moves the penetration depth √(D/γ_A). **β_L and β_C**, the two repression thresholds, which set the band's edges and are a choice of repressor and operator. **A receiver's detection threshold**, moved by a point mutation in the receptor — Basu's LuxR-G2F, represented in their model as ρ_R tenfold up — and by plasmid copy number, which is how BD1, BD2 and BD3 band in three different places. **Which pair of signals the circuit uses**, chosen from a short menu, which fixes the diffusion ratio you start from. **D**, the dilution rate, which you can still change after the strains are built. **The senders on the plate — how many, how far apart, and how dense**, which is what turns one lawn into an ellipse, a heart or a clover. **Whether the pathway runs in one strain or two**, which is the whole of move 5's technique — and, with it, **the expression level e**, because each enzyme’s burden B is proportional to it, and expression is the part you set. |
| **Constraints** | The diffusion coefficient of the signal you chose, **in the medium you have** — you inherit it once the pair is picked, and most of the ratio you end up with comes from the lawn rather than from the molecules: Karig's pair is about 1.5 apart in free solution and 21.6 apart through cells. The carrying capacity. Growth rates. The cell's own AHL export. **The thousandfold sensitivity gap between two homologous quorum systems** — 0.003 µM against 3 µM, each to its own cognate signal — which comes with the receptor pair and which **does not buy orthogonality**: Karig measure 3OC12HSL competitively inhibiting RhlR in the same paper. **the burden per unit of each enzyme** (Tsoi’s β and γ; times expression they are our **B₁** and **B₂**), and **μ_max/δ_υ**, the host's resilience to carrying it — both belong to the host and the enzyme, not to your design. **δ_me**, how fast the intermediate turns over once it is outside a cell, which with the transport rate η sets the penalty ε you pay for splitting. |
| **Limits** | **t ~ L²/2D is a first estimate with a stated convention, and it is the wrong tool once decay matters** — then the length is √(D/γ_A). *Observable:* the front stops advancing. A band that sits still instead of moving outward is a steady profile, not a spreading one, and Basu see no positional shift over 36 h. **A published diffusion coefficient may not be one:** Basu's ξ is really D/Δx² and Δx is never printed. *Observable:* put the paper's own geometry and duration into its own parameter and the arithmetic misses — 833 h for their 10 mm ring against a 36 h experiment. **The hundredfold diffusion ratio is Karig's own non-stochastic simulation of their scheme, not a classical requirement**, and there is no universal ratio. *Observable:* you get a pattern at a ratio the deterministic analysis of your own kinetics forbids, which is what they saw at 21.6, and their stochastic treatment puts "no severe requirement on the ratio". **The band edges are solved in the liquid-phase limit**, which the paper defines by dropping equation (5) — AHL becomes an imposed constant rather than a state variable, and Balagaddé's 9 nL chemostat assumes the same thing from the other side. *Observable:* the answer stops being a concentration and becomes a position. Fluorescence that varies with where you look at fixed time means no single AHL value describes the culture, and the two edges then locate a ring rather than a dose. **Move 4's growth is logistic with one carrying capacity shared between the two strains**, so both are assumed to draw on one pooled resource and growth is assumed to fall linearly in total density. *Observable:* grow each strain alone and then together. If the two monoculture saturating densities and the pair's combined saturating density are not the same number, there is no single C_m, and the cancellation that makes tr J strictly negative does not hold either. **The four-state chemostat model gets the shape right and the numbers wrong.** It is faithfully the paper's — it reproduces their Fig. 3C to three digits — and it still disagrees with their experiment at four of the five dilution rates they ran, in opposite directions. *Observable:* the model has no coexistence state where the experiment shows a steady one, and the timescale is wrong as well as the place: the cycle the model settles into at D = 0.11 runs **168 h**, about 3.4× the slowest oscillation the reactor ever showed, so nothing the model does at any dilution rate resembles the experiment's 30-50 h damped oscillations. (A **linearised** period, 2pi/|Im lambda| at the fixed point, is not a cycle period; the 49 h this row carried until 8 Nov was one, and comparing it with a measured period compares unlike quantities.) **Tsoi's criterion assumes the two split populations consume different resources and do not compete**, that each takes half the single cell's carrying capacity, and that the intermediate moves by passive diffusion. *Observable:* grow the two split strains together and separately and add up the biomass. If the pair's combined steady-state density falls below the sum of the two monocultures', they are competing and the biomass gain the left-hand side of the criterion is built on is not there. A second one: if the intermediate needs a transporter rather than crossing on its own, η is no longer a property of the molecule and the transporter is more enzyme, so it lands on the burden side as well. |

---

## 5 · Segments

FRAME → BUILD → RELEASE → DEBRIEF, none optional; one in-class rhythm (pose,
two to four minutes on their own paper, poll silently, discuss); nothing
collected.

Every crop key named in §7 appears in exactly one row below, and every row
that uses a crop names it, so the two lists can be checked against each other
by eye.

| badge | move | content | crops |
|---|---|---|---|
| open | retrieval — s2, s10, s19 | s02's L²/2D and its convention; **what happens above s10's 47 nM** (saturation, not switch-on); s19's burden number | — |
| open | by the end | three questions | — |
| frame | where this sits | the ladder inverted | — |
| segment 1 | FRAME | the AHL gradient against distance from the senders, and the protein activities in receivers at three distances — the paper's own object, not a redraw | `basu2005_fig1a` |
| segment 1 | FRAME | **the synthase**, which Fig. 1a does not carry: the sender plasmid map, `luxI` under P<sub>LTet-O1</sub>. The sender is constitutive in DH5α, which has no TetR — so the promoter's name carries a repressor this construct does not use | `basu2005_fig1b` |
| segment 1 | BUILD | **density read out as a concentration, with Karig's two measured half-activations** (0.003 µM for 3OC12HSL, 3 µM for C4HSL) — drawn on their circuit, with the competitive inhibition their Fig. 1A caption names, so the thousandfold gap is shown *not* buying orthogonality | `karig2018_fig1` |
| segment 1 | BUILD | **the minimal sender/receiver model**, which is the session's model-construction technique T64 (assessed on PS9 and on the final): dA/dt = k_I·S − γ_A·A, output = Hill(A), with k_I supplied by the session and labelled a promoter choice | — |
| segment 1 | RELEASE/DEBRIEF | a receiver whose output is an antidote rather than a reporter — write its equation; debrief on the antidote's own object | — |
| segment 2 | FRAME | session 2's slide, quoted, convention before number | — |
| segment 2 | BUILD | the four diffusion coefficients on log–log; what 83 µm²/s is and is not; the measured ratio 21.6 ± 10 against the ~100 their *non-stochastic simulation* wants; **which pair of signals you use is the choice, the coefficients are inherited** | — |
| segment 2 | BUILD | penetration depth ℓ_A = √(D/γ_A) **as a formula, with no number this folder can source for Basu's system** | — |
| segment 2 | BUILD | **Basu's ξ and the 833 hours** — the length-scale technique T66's engineering lesson: check a published coefficient's units against the paper's own geometry | — |
| segment 2 | RELEASE | two signals a factor of 3 apart: name two things you could widen the effective ratio with, and one reason a pattern might appear anyway | — |
| segment 2 | DEBRIEF (two slides) | where a ratio comes from — 1.5 in free solution against 21.6 through a lawn, with their hedge on partitioning; then why there is no universal ratio to hit | — |
| segment 3 | FRAME | Basu Fig. 1a's printed truth table — non-monotonicity as a logical fact before any kinetics | `basu2005_fig1a` (reused) |
| segment 3 | BUILD | the three cases, one slide each, in the paper's own words; same topology as session 10's feed-forward loop, different mechanism; β_L against β_C | — |
| segment 3 | BUILD | **the two band edges solved** from equations (1)–(4) in the liquid-phase limit — the band-detect analysis technique T65, assessed on PS9 — with `posb.band_edges`'s printed-parameter values on the slide | — |
| segment 3 | BUILD | **the inverter surprise**: a high-detect strain on its own runs *backwards*, dark at high AHL and bright at low | `basu2005_fig2b` |
| segment 3 | BUILD | **three strains, three thresholds, deliberately tuned** — their measured triple beside the three curves `posb.band_detect_response` draws from `basu_params("BD1"/"BD2"/"BD3")`, with ρ_R ×10 for the LuxR-G2F mutant and halved copy number for BD3 named as the two changes. Our curves stand in for their Fig. 2c, which saves a crop and is exact: the module *is* their printed model. This is the slide §4's detection-threshold knob rests on, and `readings.yaml` promises Fig. 2d to students | `basu2005_fig2d` |
| segment 3 | BUILD | **the two bullseyes, on one slide**: the sensitivity order inverts in space — the most sensitive strain makes the *outermost* ring — and the same strain made a 30 mm ring once and a 22 mm ring another time, a 36 % difference whose every offered explanation is an environment variable | `basu2005_fig3b`, `basu2005_fig3c` |
| segment 3 | BUILD | **the senders are the program**: a lawn of receivers, three sender layouts, three patterns — ellipse from two sender disks, heart from three, clover from four. The knobs are the number of senders, the distance between them and their density, which is what the caption and the text say. Fig. 5a is labelled *Simulation* in the paper's own caption and is not on this slide, which is why it has no crop key | `basu2005_fig5b`, `basu2005_fig5c`, `basu2005_fig5d` |
| segment 3 | BUILD | the regression against its own inputs — R² = 0.91 with no experiment in it, in a *Nature* abstract. Show it, ask what was measured, let them find it | — |
| segment 3 | RELEASE/DEBRIEF | a band detector built from two *activators* instead of two repressors — can it band? | — |
| segment 4 | FRAME | two strains, each controlling the other's survival, with the killer and the antidote drawn | `balagadde2008_box1a` |
| segment 4 | BUILD | eight derivation slides: the four-state model, the QSSA that kills the oscillation, and the Hopf once the signals are restored. Equations labelled **BioModels BIOMD0000000296, curated from Balagaddé 2008** | — |
| segment 4 | BUILD | the two-parameter regime diagram, three labelled operating points at k_c1 = 0.2, 0.8 and 1.2 — **and this is where the authors draw the locus**: "a line connecting Hopf bifurcation points demarcates three regions". Axis warning: this panel is 10³ cells/µl, Figs. 2 and 3 are cells per reactor, never on one axis | `balagadde2008_box1b` |
| segment 4 | BUILD | the paper's own bifurcation diagram against IPTG, with the branch point **labelled `Hopf` on the panel itself**, beside the green dot, and the period inset. The Fig. 2 *caption* never uses the word; Box 1B draws the locus of Hopf points, and this is the panel where they **cross** one with a knob and print it. Do not reproduce the inset's printed "IPTG (M)"; the units are µM | `balagadde2008_fig2c` |
| segment 4 | BUILD | the clean 180 h trace beside all twelve reactors — several induced reactors show prey high and predator flat for 200 h | `balagadde2008_fig2a`, `balagadde2008_fig2b` |
| segment 4 | BUILD | the deposited model at the authors' own five dilution rates against what they saw: four disagreements out of five, in opposite directions — then the three-digit agreement with their own Fig. 3C, so nobody can call it a transcription error, and "qualitatively accounts for" put in front of the room | `balagadde2008_fig3c` |
| segment 4 | RELEASE/DEBRIEF + poll | double the dilution rate and predict what happens to the predator, off the nullclines just drawn; the two-part poll (*what does the model predict* / *what did the experiment do*) with P pinned and options written out | — |
| segment 5 | FRAME | the XOR as four colonies on a plate — three NOR gates and a buffer gate, one gate per strain, wired with 3OC12-HSL and C4-HSL, which are **Karig's two molecules from segment 2 and not Basu's signal** | `tamsir2011_fig3` |
| segment 5 | BUILD | all sixteen two-input functions from one small library, by moving colonies, with no further genetic manipulation; 7 mm spacing and a 12 h delay per layer as an external clock; 5-fold to 335-fold induction across the set. One spoken line, no crop: their tandem gates add their two promoters' transfer functions and the prediction held for six of seven — the seventh is the same two promoters swapped in order, which is session 17's subject as a measurement | `tamsir2011_fig4` |
| segment 5 | BUILD | the same split built twice — ethanol on glucose breaks it, xylose-and-acetate makes each strain remove the other's problem; 2 → 4 mg/L, and the `atpFH` knockout that forced the cooperation | `zhou2015_fig1`, `zhou2015_fig2` |
| segment 5 | BUILD | Tsoi's criterion stated with its two sides drawn — biomass gain against transport inefficiency. **This is the criterion the session's split-or-not technique T76 is applied with** (assessed by the home guide and on the final, not on PS9) | `tsoi2018_fig1c` |
| segment 5 | BUILD | the caveat: three burden forms, three borders, ~5× apart — and a caption that says the parameters were *chosen* so the ordering comes out that way. The direction is a fact about the functions; the size is a chosen example | `tsoi2018_fig2d` |
| segment 5 | RELEASE | **two named pathways**, both two-enzyme in the same host, Hill burden with n = 2 and μ_max/δ_υ = 10: A has η = 1.0, δ_me = 0.001 and **B₁ = B₂ = 1.2 per enzyme**; B has η = 1.0, δ_me = 0.5 and **B₁ = B₂ = 1.3 per enzyme**. Split one. Which, and what would you measure to be sure? **This is T76's demonstration**, so the stem names pathways rather than kinds of pathway, prints η and δ_me rather than their ratio, and says **per enzyme** — read as a pathway total the verdict on A reverses | — |
| segment 5 | DEBRIEF | the criterion evaluated for each, with `posb.dol_criterion` on the slide: **split A, leave B** — A's border is **1.135146** and it sits at 1.2; B's is **1.355143** and it sits at 1.3. **The higher-burden pathway is the one you leave alone**, because slow transport pushes the border up, which is the direction their Fig. 1D moves. Both populations alive in both cases (single-cell yields 0.32 and 0.13), so this is the deciding part of the plane and not the region where the single cell has died of its own burden. What you measure: B per enzyme, the host's μ_max/δ_υ, and η against δ_me — with Zhou as the worked case. Three caveats on the same slide: the burden values are the session's own and are not points on Tsoi's axis, the border moves ~5× with the burden form, and Tsoi has no experiment anywhere — nor can their own Fig. 1D be reproduced from their own inequality | — |
| close | the design ledger | Knobs, Constraints, Limits, with an observable on every Limit | — |
| close | before next class | assign the session 25 reading — **Weinberger, and the two optional papers** | — |

**Board.** Move 4's steps 4–7 are the natural board segment. If they go to the
board they need a script in `private/board-notes/`, every line in order, and
§5e still requires the slide-resident version for anything assessed. Version 1
referenced board notes with no board segment.

---

## 6 · What a later pass must not undo

1. **83 µm²/s is an estimate, an effective cell-to-cell coefficient, and the
   wrong molecule for Basu's geometry.** All three qualifications stay.
2. **Same topology, different consequence.** Not "the ring is the pulse".
3. **The high/low names are correct.** The inverter is the surprise.
4. **Balagaddé prints rate constants** — on Box 1B's axes and as dilution rates.
5. **The predator–prey equations are the BioModels deposit's, and the deposit
   is faithfully the paper's model** — it reproduces their Fig. 3C to three
   digits. Label the provenance; do not label the model "ours". What is ours is
   the *construction* the room does from Box 1A.
6. **The hundredfold diffusion ratio belongs to Karig's non-stochastic
   simulation**, never to classical Turing theory.
7. **Tamsir's wires are 3OC12-HSL and C4-HSL** — Karig's pair, not Basu's
   3OC6HSL. The session does not say "the same AHL" about them.
8. **Zhou's first co-culture fails through ethanol**, which is what the second
   design removes. Name the ethanol.

9. **Move 5 carries a technique**, T76, deciding whether to split a pathway
   across strains — home guide and final, not PS9. Its release and debrief are
   that technique's only demonstration anywhere in the course.

**If short, cut in this order:** Tamsir's sixteen-gate slide to one line,
keeping the XOR; then Fig. 3b/3c's reproducibility pair; then the diffusion
ledger down to the two Karig coefficients. **Never cut** move 1's
sender/receiver model (T64, which is on the final), move 2's ξ cautionary
slide, move 5's release and debrief, or any other RELEASE/DEBRIEF pair.

> **Tsoi's criterion came off the cut list on 7 November.** Version 3 had it
> first — "cut to one line, keeping the burden-form caveat" — which was written
> when move 5 carried no technique. It carries T76 now, the criterion is what
> T76 is applied with, and the home guide is its only practice vehicle. **You
> cannot cut to one line the only demonstration of a thing you assess.**
>
> **Three things are not cuttable while §4 stands as written.** The ledger
> claims the senders on the plate as a knob, so Basu Fig. 5's slide stays unless
> that knob comes out of the ledger; it claims a receiver's detection threshold
> as a knob, so the three-strain slide stays unless that one does too; and it
> now claims one-strain-or-two as a knob, with B, μ_max/δ_υ and δ_me as the
> constraints against it, so segment 5's criterion slide and its release stay.
> Cutting a slide that a ledger entry rests on leaves the ledger asserting a
> knob the session never showed.

---

## 7 · What the build needs

### 7.1 What the module exports

`posb/communities.py` and `tests/test_communities.py` exist and are green as of
7 November. **The list below is what the module exports, read off its own
`__all__`**, so a builder can import against it rather than guess:

| group | names | provenance |
|---|---|---|
| length and time | `diffusion_time(L, D)` wrapping s02's convention; `penetration_depth(D, gamma)`, which has **no default D** | the course's |
| the sourced coefficients | `KARIG_D_3OC12HSL`, `KARIG_D_C4HSL`, `BASU_XI` | Karig's two estimates; Basu's ξ as printed, with its warning |
| Basu's band detector | `BASU_BD2`, `basu_params(variant)`, `band_detect_response(AHL, params)` in the liquid-phase limit, `band_peak(params)`, `band_edges(params)` solved rather than read off a plot | **Basu's printed model and printed parameters.** Nothing fitted, nothing ours |
| the pair written with the room | `sender_receiver(A, S, k_I, gamma_A, D=0.0, ...)`, with `k_I` a required argument and no default | ours, and the slide says so |
| the predator–prey community | `PP_PARAMS`, `PP_INITIAL`, `PP_IPTG`, `iptg_assignment_rules`, `pp_params`, `predator_prey_model`, `pp_qss_signals`, `pp_qss_model`, `pp_steady_states`, `pp_jacobian`, `pp_oscillatory_focus`, `pp_leading_real_part`, `pp_hopf_D` | **BioModels BIOMD0000000296**, four-state, curated from Balagaddé 2008 — not the paper's text, which prints no equations, and not a course invention |
| division of labor | `burden_form(name, n)`, `dol_criterion(...)` | Tsoi's printed criterion, evaluated with a burden form the caller picks |

**`turing_ratio_required(...)` is gone, and it should stay gone.** There is no
universal ratio to return: the critical ratio falls out of the Jacobian of
whatever kinetics are assumed, and the only number in the folder — Karig's
~100 — belongs to their own non-stochastic simulation of their own scheme. A
function with that name would have to take a kinetic scheme, and no slide in
this session asks for one. Version 1 specified it; implementation dropped it,
correctly.

### 7.2 What the tests pin

The suite is 176 tests. The ones the design depends on:

- `diffusion_time` reproduces session 2's printed numbers exactly, and
  session 2's slide is itself asserted still to state the convention this
  module assumes.
- Basu's own 10 mm ring takes **833 h** on Basu's own ξ — the T66 arithmetic,
  pinned.
- `penetration_depth` is checked in two unit systems against a value worked out
  inside the test, **not** against 0.32 mm; a separate test asserts that the
  0.32 mm figure is a *reductio* against ξ and not a design number; and the
  function refuses to supply a diffusion coefficient of its own.
- `band_detect_response` has a single interior maximum by a fine sweep, and a
  companion test shows that a coarse grid straddles the peak and reports the
  wrong story. `band_edges` round-trips against the response. BD1 is BD2
  shifted down by exactly √10, which is the cleanest analytic check in the
  file.
- The quasi-steady-state reduction's trace is exactly −(k_c1·C₁ + k_c2·C₂)/C_m
  and is negative across a wide sweep, so **the reduced system has no Hopf
  anywhere** and the error message says why.
- The four-state system has **two** Hopf crossings, bracketed two-sided at four
  step sizes each, with the leading real part zero to machine precision and a
  nonzero imaginary part at the crossing.

> **The oscillatory window is now pinned, and version 2's reason for refusing to
> pin it has been overtaken.** Version 2 said the window was our
> one-significant-figure digitization of their Fig. 3C and that the model was
> ours, so a test would freeze an accident. Both halves were wrong once the
> deposit was read: the window is **computed** from the deposited model, not
> digitized, and it comes out at D = 0.0367268 and D = 0.1674282. Those are
> asserted to one part in 10⁵, and the digitization of their Fig. 3C is what
> they are *checked against*, agreeing to three digits. What stays untested is
> the comparison with the **experiment** — that is a reading of their data, it
> is taught in the room, and freezing it in a test would assert a claim about
> their reactor rather than about our code.

**Figures:** `derivation_fig` for moves 2, 3 and 4; the band response with both
edges in the derivation's symbols; the phase plane with nullclines and an
eigenvalue inset **carrying its held-fixed parameters**; the diffusion ledger
against length on log–log. `tools/figure_fit.py` is an **auditor** run by
`build_figures --verify` — version 1 said figures were built "through" it, which
would send a builder looking for an API that does not exist.

### 7.3 Crops

**Twenty-two keys, and every one is used by a row in §5** — one row each,
except `basu2005_fig1a`, which segment 1 and segment 3 both frame on, from
different parts of the panel. The list and the table are meant to be read
against each other; if a key here has no row there, one of the two is wrong.

| paper | keys | the row that uses it |
|---|---|---|
| Balagaddé | `balagadde2008_box1a` | segment 4 FRAME |
| | `_box1b` | segment 4, the regime plane |
| | `_fig2a`, `_fig2b` | segment 4, the clean trace against all twelve reactors |
| | `_fig2c` | segment 4, where the paper prints *Hopf* |
| | `_fig3c` | segment 4, the model at the five dilution rates |
| Basu | `basu2005_fig1a` | segment 1 FRAME and segment 3 FRAME (one crop, two rows) |
| | `basu2005_fig1b` | segment 1 FRAME, the sender plasmid map — the only place `luxI` is drawn |
| | `_fig2b` | segment 3, the inverter |
| | `_fig2d` | segment 3, the measured triple |
| | `_fig3b`, `_fig3c` | segment 3, the two bullseyes on one slide |
| | `_fig5b`, `_fig5c`, `_fig5d` | segment 3, the senders as the program |
| Karig | `karig2018_fig1` | segment 1, the two thresholds on their circuit |
| Tamsir | `tamsir2011_fig3` | segment 5 FRAME, the XOR as four colonies |
| | `tamsir2011_fig4` | segment 5, all sixteen functions |
| Zhou | `zhou2015_fig1`, `zhou2015_fig2` | segment 5, the same split built twice |
| Tsoi | `tsoi2018_fig1c` | segment 5, the criterion's two sides |
| | `tsoi2018_fig2d` | segment 5, the burden-form caveat |

**`basu2005_fig2c` and `basu2005_fig5a` are deliberately absent.** Fig. 2c is
the *simulated* band-detect triple, and `posb.band_detect_response` draws the
same three curves from the same printed parameters, exactly, so the slide uses
ours. Fig. 5a is a *simulation* of the ellipse and a slide must not put it
beside 5b–d as though all four were data.

None of these sixteen keys is in `decks/paper_figures.yaml` yet. Adding them,
with `shows`, `used_in: ["s24"]` and a note, is build work.

**Wire-in, part done already.** `figures.s24_communities` is already in
`MODULES` in `tools/build_figures.py` and `s24_communities` is already in
`DECKS` in `tools/build_decks.py`. What does **not** exist is
`figures/s24_communities.py` itself, so the registration currently points at
nothing.

**Handout, answer sheet, board notes** — built off the PS9 items.

---

### 7.4 The T76 guide item

**Handout, answer sheet and board notes are built off the PS9 items.** T76 has
no PS9 item — it is assessed by the session 24 home guide and on the final — so
the guide is its only practice vehicle and this is the only place the
specification can live. Whoever builds the guide should treat the rest of this
subsection as the item's brief.

**What the item asks.** One pathway, named and specified, and a decision about
it with the criterion stated rather than derived. The shape that works, and it
is the release's shape with one pathway instead of two:

> A three-enzyme pathway in *E. coli*. The second enzyme is the expensive one.
> The intermediate between enzymes two and three is a charged sugar phosphate
> and crosses the membrane slowly. You are given **B per enzyme**, the host's
> μ_max/δ_υ, the Hill coefficient n, and **η and δ_me** for the intermediate —
> all printed in the stem, because none of them can be read off a figure.
>
> **(a)** State the criterion you will use and say, in one sentence each, what
> its two sides represent.
> **(b)** Apply it. Would you split this pathway across two strains?
> **(c)** Name one assumption behind the criterion that this pathway violates
> or strains, and say which way it moves your answer.
> **(d)** Name two quantities you would measure before building either version,
> and say what each one would change.

**Why each part is there.** (a) is the stated criterion, which is what the
technique is — Tsoi's Eq. 16 with the biomass gain on the left and the
transport inefficiency θ_I on the right, or Eq. 17's burden form. (b) is the
application, and the pathway is specified so that there is an answer rather
than a discussion. (c) is the part a hand-graded item exists for: the candidates
are the passive-diffusion assumption, the two populations not competing, the
halved carrying capacity ρ₁ ≈ ρ₂ ≈ ρ/2, the choice of burden functional form,
and the fact that a slow-crossing intermediate may need a transporter, which is
more enzyme and therefore lands on the burden side too. (d) is the measurement
half, which the release also asks and which students skip if it is not asked
separately.

**What full credit looks like, in the s16/s17 register the posted sheets use.**
An answer that applies the criterion and reaches either verdict earns full
credit if it names which term decided it. An answer that reaches the right
verdict by saying "high burden, so split it" does not, because that rule gives
the wrong answer on the release's own pathway B. Credit for noticing that the
criterion's own best natural examples — nitrification, syringate — exist in
both forms and do not decide.

**Three things the stem must get right, each of which has already gone wrong
once in this folder.**

1. **Say which quantity every number is, and say "per enzyme".** A burden given
   as a pathway total, split across two enzymes, halves B — and on move 5's
   own release that reverses the verdict on pathway A, from split to leave, by
   correct reasoning. On a hand-graded item the reader would be marking a
   right answer wrong.
2. **Print η and δ_me, never ε = δ_me/η.** ε does not determine the border:
   θ_I depends on the two separately: with δ_me held at 0.5η and η swept from
   0.2 to 10 — ε = 0.5 throughout — the border moves by about 0.03, and the
   family is open. A stem that gives ε alone has no single right answer.
3. **Warn about the spurious root, if the item invites a numerical search.**
   Above **B = 3.0 per enzyme** both yields are exactly zero — the split
   populations die of their own burden, as the single cell does at B = 1.5
   per enzyme carrying both
   enzymes — so the yield margin is identically zero there and **a bisection
   over any bracket containing 3.0 returns 3.0** rather than the real crossing.
   Verified: `brentq` over [0.3, 3.0] returns exactly 3.0 for both of move 5's
   pathways. `posb.dol_criterion`'s docstring now carries this. A student
   working the guide may well try to find the border numerically, and PS9 does
   not assess T76, so the guide is the only place they can be warned.

**What the item must not do.** It must not ask for a number read off Tsoi's
Fig. 1D or Fig. 2D, for two reasons that are both worse than they look. Those
border positions are our digitization at one significant figure; Fig. 2D's
caption says its parameters were chosen so the three burden forms order the way
they do; and **Fig. 1D's "Relative burden" axis is not the burden of Eq. 17 at
all** — putting its border back through the paper's own inequality would need a
host with μ_max/δ_υ ≈ 4 × 10⁴ (`NUMBERS.md` §12.1). Every number in the item
is printed in the stem, and the verdict comes from `posb.dol_criterion`.

---

## 8 · Counting Figure 5

Basu Fig. 5 is **three** experimental patterns — ellipse (two senders), heart
(three), clover (four). Panel 5a is a *simulation* of the ellipse, so the figure
has four panels and three results. The bullseye is Fig. 3, not Fig. 5. Version
1's table said four patterns from Fig. 5b–d. The abstract names only ellipses
and clovers, so a slide that repeats the abstract miscounts the figure in front
of the room.

**And the knob is not placement alone.** The caption says the patterns form
"based on the placement **and initial concentrations** of sender cells", and the
text lists "the number of, distance between, and density of sender cells". So
§4's ledger entry names all three, and the slide does too. Saying "sender
layout" and stopping drops the one knob a student could set with a pipette.

---

## 9 · What changed from version 1

| | |
|---|---|
| "prints no rate constant of any kind" | false — Box 1B's axes and the dilution rates. Also corrected in `readings.yaml` |
| "the ring is the pulse, drawn in space" | false as mechanism. Also corrected in `readings.yaml` |
| "the names are the reverse of what they sound like" | false — high/low are correct. Also corrected in `readings.yaml` |
| "the oscillation is not a property of the strains" | Box 1B's plane is two strain parameters |
| 47 nM | a saturation, not a pulsing threshold |
| s10 census numbers | were corpus totals |
| 83 µm²/s | an estimate, effective cell-to-cell, wrong molecule for Basu — and 1,810 for the other signal |
| Basu "prints no threshold... anywhere" | no *AHL* threshold and no error bars; it does print 10 mm, 5–18 mm, 30/22 mm |
| "a factor of twenty" | one to two orders of magnitude |
| Fig. 5b–d | three patterns |
| "several reactors" | belongs to the 2B caption |
| T64 | demonstrated nowhere, and on the final. Now a segment-1 model |
| T65 | tagged on a naming slide. Now the solved edges |
| T66 | no design consequence. Now √(D/γ_A) and the ξ lesson |
| Karig | assigned and taught nowhere. Now move 2 |
| quorum sensing | one bullet, no number. Now Karig's measured thresholds |
| Fig. 2A, Fig. 2C | dropped. 2C is where the paper prints "Hopf" |
| move 4's derivation | one row. Now eight slides |
| the Hopf callback | s11 computed it, never named it |
| segment structure | rebuilt as FRAME/BUILD/RELEASE/DEBRIEF |
| the design ledger | did not exist |
| seven trailing-qualifier titles, two "actually" | cut |

### 9b · The third pass, 7 November

| | |
|---|---|
| "every key now has a segment row" | was false for seven keys. §5 now carries a crop column and §7.3 a key-to-row table |
| Basu Fig. 5 | promised in `readings.yaml` and taught nowhere. Now a segment-3 slide, and the ledger's sender knob names number, distance and density |
| the diffusion ratio | called "the design parameter" in §3 and inherited in §4. Resolved: the **pair** is the choice, the coefficients are inherited, and the lawn supplied the factor of ~14 |
| the thousandfold gap | the ledger conflated two different quantities. Karig's cross-system sensitivity gap is inherited; Basu's three tuned receivers are a **knob**, set by LuxR-G2F and by copy number, and that knob is now in the ledger with a slide behind it |
| Limits | had no observables and two false entries. Every entry now names an observable; the liquid-phase limit and the shared-carrying-capacity assumption are added |
| "the classical Turing requirement" | the 100 is Karig's **non-stochastic simulation**. Corrected in §4, §6 and in `readings.yaml`'s Karig focus line |
| "the predator–prey model is ours" | false. The deposit reproduces their Fig. 3C to three digits, so it is the paper's model; what is ours is the construction from Box 1A |
| the oscillatory window | §7 refused to test it for two reasons that are both now wrong. It is computed from the deposit and pinned two-sided |
| `turing_ratio_required` | removed from §7. There is no universal ratio to return |
| §7's library list | rewritten off `posb/communities.py`'s own `__all__`; 176 tests passing |
| move 2's release | expects an answer the folder cannot give. Rewritten, with a two-slide debrief |
| move 5 | had FRAME and BUILD and no RELEASE or DEBRIEF in §5. Kept, with both, and its Tamsir and Zhou claims now sourced in `NUMBERS.md` §§21–22 |
| "the same AHL the session opened on" | false. Tamsir's wires are 3OC12-HSL and C4-HSL, which are Karig's pair, not Basu's 3OC6HSL |
| "the yeast inhibits *E. coli*" | the agent is the **ethanol** the yeast makes on glucose, which is what the second design removes |
| the census | applied two standards in one section. Now slide-facing only, with totals in brackets, recounted from `decks/` |
| `PRIOR-YEARS.md`'s Jacobian 22 | six of those hits are image filenames. 16 total, 14 slide-facing |
| the Hopf | counted slide-facing, the word appears on no prior slide. Session 24 is the first slide to say it in words, to a room that has already computed one |
| move 5 carried no technique | **T76 added to `docs/coverage-matrix.md`** — decide whether to split a pathway across strains, S24, Guide + Final, HAND. Move 5 names it, §5's rows carry it, §4's ledger carries B, μ_max/δ_υ and δ_me, §6 takes Tsoi's criterion off the cut list, and §7.4 specifies the guide item |
| move 5's release did not demonstrate T76 | it named two *kinds* of intermediate, could be answered on permeability alone, and used only the transport half of the criterion. Rewritten around two named pathways whose burden and transport pull opposite ways, with the verdicts computed from `posb.dol_criterion` |
| the release specified each pathway by ε = δ_me/η | ε does not pin the border — θ_I depends on η and δ_me separately, and sweeping η over the ε = 0.5 family moves it by about 0.03. The slide now prints η and δ_me. Borders restated at the pinned parameters: **A 1.135146, B 1.355143** |
| "relative burden 1.2" was ambiguous | it reads as a pathway total; the model takes it **per enzyme**, and the pathway reading halves B and **reverses the verdict on A**. Said explicitly in the release, the debrief and §7.4, and in `dol_criterion`'s docstring |
| a bisection for the border returns 3.0 | both yields are exactly zero above B = 3.0 per enzyme, where the split populations die as the single cell does at 1.5, so the margin is identically zero and any bracket containing 3.0 returns it. Warned in §7.4 and in the module docstring |
| "Fig. 2C does **not** print *Hopf*" | **this file's own wrong turn, and the costliest kind — a false finding in an authority file.** Settled against a 200 dpi render on 7 Nov, reversed at 400 dpi on 8 Nov: the word is printed in bold beside the green dot. It had propagated into two slides. Only the *caption* omits the word. `NUMBERS.md` §3.3 records the correction and the rule it produced: a claim that something is **absent** from a panel is provisional until checked at 400 dpi, and must state the resolution |
| §8.3's digitized AHL positions | a uniform **6.8×** above what the printed parameters give, while the peak heights and spacings agree to three digits — so the x calibration is off by 0.83 decades. §8.4 is in the same doubt, and with it the old "2–3× model-to-data shift". Move 3 now teaches ordering and spread only |
| "D appears in five places" | four: it leaves with each population and with each signal |
| "a four-parameter chemostat model" | four-**state**. The deposit has eleven parameters |
| "the sender with TetR driving LuxI" | false twice. P<sub>LTet-O1</sub> is TetR-*repressed*, the strain is DH5α and carries no TetR, and Fig. 1a names no synthase at all — its caption calls the sender's expression constitutive. `luxI` is drawn only in Fig. 1b, which is now a crop and a frame row |
| "ten million in the same volume" | an invented number. Replaced with Balagaddé's own 10²–10⁴ cells in 9 nL against ≥10⁹ macroscale, and the ~75-cell detection limit |
| two more "actually", four trailing-qualifier headings | cut |
| three symbols collided and were disambiguated in slide feet | a foot note tells the room the collision exists without removing it, which is what `deck-bar.md` §B1 rules out. Renamed, and recorded in `docs/symbols.md`: the penetration depth **λ → ℓ_A** (λ stays the eigenvalue of moves 4, and of sessions 8, 11 and 14, where T29 is autograded on PS5); the receiver's half-output concentration **bare θ → θ_A** (session 22 holds bare θ, and Tsoi's θ_I is in move 5); and Tsoi's burden **βe → B**, per enzyme **B₁/B₂**, because β_L and β_C are Basu's printed thresholds in the same hour. Both stale feet removed — `LAMBDA_NOTE` now *defines* λ rather than distinguishing it, and `THETA_NOTE` is gone |

---

## 10 · Decisions for Adam

### Settled

1. **Move 5's scope — settled 7 November 2026. Keep the move and give it a
   technique.** The first review recommended cutting division of labor to the
   Voigt slide and spending the space elsewhere. What decided it was not the
   hour's budget but the contract: moves 1–4 each carry a technique, so a
   five-slide move 5 carrying none was demonstrated-and-assessed-nowhere, which
   `docs/coverage-matrix.md`'s decision 13 makes a gap of the same kind as an
   assessment with no demonstration. **Adam closed the gap by assessing the
   move rather than by shrinking it.** The new row is
   *T76 — decide whether to split a pathway across strains — S24 — Guide +
   Final — HAND*, following T75's pattern: not on PS9, which stays at ten
   techniques because it posts on 19 November, and hand-graded because the item
   is a design argument with a stated criterion rather than an arithmetic
   result. Move 5 names it, §5's rows carry it, §4's ledger carries its
   quantities, §6 takes Tsoi's criterion off the cut list, and §7.4 specifies
   the guide item, which is T76's only practice vehicle.

   **What this decision forced.** T76's
   demonstration is move 5's release and debrief, so they had to demonstrate
   what a guide item would ask. **The release as written did not.** It offered
   two *kinds* of intermediate rather than two pathways, it could be answered on
   permeability alone without the criterion entering, and it exercised only the
   transport half of the inequality. It is rewritten around two named pathways
   that pull opposite ways, which forces both halves and produces a
   counterintuitive answer. A row that asserts a demonstration which did not
   happen is the defect the row exists to prevent.

2. **Teaching that Tsoi's own figure cannot be reproduced from Tsoi's own
   inequality — considered and deliberately kept to one sentence, 7 November
   2026.** The finding is real and is in `NUMBERS.md` §12.1: their Fig. 1D
   draws the single-cell/division border at a relative burden near 70, and
   putting that back through their Eq. 17 needs a host with μ_max/δ_υ of order
   10² at n = 1 and 10⁴ at n = 2. So the axis is not the burden the criterion is
   written in, and the paper gives no way to tell what it is.

   **It has the same shape as move 4's honest-reading segment, which is the
   strongest thing in the session, and that is the argument for teaching it at
   length. I did not**, for three reasons. Running the same move twice in one
   hour is what §5c and the stacking warning in §8 of
   `docs/lecture-design.md` both caution against, and move 4 already carries
   that lesson with a computation behind it. Move 5 is the last move of the
   hour and now carries a technique, a release and a debrief; it is also the
   move both reviews wanted cut for thinness, so it is the worst candidate for
   a second full segment. And placed before the release it would tell the room
   that the criterion they are about to be assessed on cannot be checked
   against its own paper — which is true, and is the wrong thing to say in the
   thirty seconds before they use it.

   **So it is one sentence, at the end of the debrief's third caveat**, where
   it completes the point that Tsoi is analysis with no experiment and whose
   own best natural examples do not decide. Say if you would rather it ran
   longer; the material is extracted and the arithmetic is in §12.1, so
   promoting it is a writing job and not a research one.

3. **The reading load — settled 7 November 2026.** Two required papers plus
   four optional on one session is approved: *"Yes. Second reading"* and
   *"We can add non-required readings to support students. We can be flexible."*
   So `readings.yaml` listing `basu2005` as required alongside `balagadde2008`,
   against `max_required_per_assignment: 1`, is a deliberate override and not a
   drift, and Karig, Tsoi, Tamsir and Zhou stay as optional rows with focus
   lines.

4. **BioModels — resolved, and then resolved harder.** The deposit is the
   reduced Balagaddé model, curated from *Mol Syst Biol* 4:187. Run from its own
   constants it reproduces the paper's Fig. 3C to three digits, so it is the
   paper's model and not a reconstruction. It also **disagrees with the
   experiment at four of the five dilution rates the authors ran, in opposite
   directions** (`NUMBERS.md` §§20.4–20.5), and move 4 teaches that
   disagreement.

### Still open

5. **The PS9 item for the sender/receiver technique (T64).** If it is to hand
   students a runnable model, the BioModels deposit is the one — and **the item
   must not ask them to match the experiment**, because the deposited model does
   not. That is a decision about what the item asks, and it is yours.

---

## 11 · §11's open list, closed on 7 November

Each item below was open after two review rounds and is now decided in this
document. The decision is recorded here so a later pass can see what was
weighed rather than re-opening it.

| what was open | what was decided |
|---|---|
| **§7's "every key now has a segment row" was false** for `basu2005_fig2d`, `_fig3b`, `_fig3c`, `_fig5b`, `_fig5c`, `_fig5d` and `karig2018_fig1`, and Tsoi's one claim came from a figure with no key | **Every key got a row, and two keys were dropped.** Fig. 2d joins the measured triple in segment 3; Figs. 3b/3c become the one bullseye slide; Figs. 5b–d become the sender-layout slide; Karig Fig. 1 becomes segment 1's drawn object for the two thresholds. `tsoi2018_fig2d` was added for the burden-form caveat and `tsoi2018_fig1c` kept for the criterion. `basu2005_fig2c` was **dropped** because `posb.band_detect_response` draws the same simulated triple from the same printed parameters, exactly, and `basu2005_fig5a` was never added because it is a simulation. Tamsir and Zhou needed keys and now have four, and `basu2005_fig1b` was added because the synthase — the one object §2 says cannot be words — is drawn in the sender plasmid map and nowhere else. Twenty-two keys. §5 carries a crop column and §7.3 a key-to-row table, so the two can be checked against each other |
| **`readings.yaml` promised Basu Fig. 5 and no segment taught it** | **Taught it.** It is one build slide at the close of segment 3, it pays the promise, it delivers the "patterning" in the title, and it is what §4's sender knob rests on. The ledger entry was also wrong: the knobs are the **number** of senders, the **distance** between them and their **density**, not placement alone. §6 records that the slide is not cuttable while that knob stands |
| **The ledger contradicted §3 on the diffusion ratio** | **The pair is the knob; the coefficients are inherited.** You do not dial a diffusion coefficient — you pick a signal and inherit it in the medium you have. And the lawn, not the molecules, supplied most of Karig's ratio: ~1.5 in free solution against 21.6 measured. Move 2 and §4 now say the same thing |
| **The ledger contradicted §3 on the thousandfold** | **Two different quantities were being run together.** Karig's 0.003 µM against 3 µM is the sensitivity gap between two *different* quorum systems, each to its own cognate signal — inherited with the receptor pair, and it buys no orthogonality. Basu's BD1/BD2/BD3 are the *same* system retuned, by the LuxR-G2F point mutation and by copy number — that is a **knob**, it is now in the ledger, and segment 3 has the slide it rests on |
| **Limits was missing the liquid-phase limit and move 4's logistic assumptions** | **Both added, and every other Limits entry got the observable §5d requires**, which none had. The liquid-phase entry says the answer stops being a concentration and becomes a position; the logistic entry says to grow each strain alone and together and see whether one carrying capacity describes all three measurements. Two existing entries were also false and are rewritten: the hundredfold is Karig's non-stochastic simulation, and the predator–prey model is the deposit's |
| **The census applied two standards in one section** | **Declared: slide-facing text only, notes excluded**, on `docs/lecture-design.md` §5b's reasoning, with totals in brackets so §4 of `PRIOR-YEARS.md` stays readable against it. Both counts restated. The mathematics census was **recounted from `decks/`** rather than given as a range, and the disagreement is explained: `PRIOR-YEARS.md`'s Jacobian 22 counts six image filenames. The recount also changed §2's Hopf claim |
| **Move 5 had FRAME and BUILD but no RELEASE or DEBRIEF in §5** | **Kept the move and wrote both.** The release is the permeable/impermeable pathway pair; the debrief answers it on Tsoi's ε = δ_me/η and on their own burden–diffusivity border, with Zhou's acetate as the worked case. §3 already carried the release; §5 did not, and the inconsistency was between the two sections rather than in the move. §10 keeps the scope question open for Adam |
| **Move 2's release had no written expected answer** | **The question was rewritten so its honest answer is the one it expects**, and the answer is walked on two debrief slides. The 100 is attributed to Karig's non-stochastic simulation throughout, never to classical theory — in §3, in §4, in §6, and in `readings.yaml` |
| **`turing_ratio_required(...)` was undefined as specified** | **Removed from §7**, and §7 now records why it should stay removed. §7's library list was rewritten off the module's own `__all__` |

### What is open after this pass

Three things, and none is a design decision I can make from the folder:

1. **§10's one remaining item**, the sender/receiver PS9 item, which is
   Adam's. The other three in §10 are now settled, move 5's scope among them.
2. **T66's diffusion coefficient for Basu's geometry does not exist in this
   folder, and the session is built on saying so.** `NUMBERS.md` §19.4 settles
   that Karig's coefficients cannot be combined with Basu's γ_A — different
   molecule, different lawn — and §13 settles that Basu's ξ cannot be used as
   one. The session teaches √(D/γ_A) as a formula and teaches why it has no
   number here, which is defensible and is §6's "never cut" item. If a sourced
   AHL coefficient in agar is wanted instead, `NUMBERS.md` §16.6 names the
   route: `PRIOR-YEARS.md` §2.2's Lu & Karig measured front, ±4 cm on a plate
   at 0, 2.5, 5 and 8 h, from the 2018 session-24 deck p.18. **That slide was
   not opened, so the number is still `[unverified]`** and no slide should carry
   it until it is.
3. **`NUMBERS.md` §8.3's and §8.4's AHL axis calibration needs re-digitizing.**
   §8.3's three simulated band positions are a uniform **6.8×** above what the
   printed parameters give, while the peak heights and the spacings agree to
   three digits — so the x axis is off by 0.83 decades, which at that panel's
   stated 48.4 px/decade is a 40 px tick misplacement. §8.4's measured positions
   were calibrated the same way and are in the same doubt. **This session is
   built so that nothing depends on it**: move 3 teaches ordering and spread,
   and every absolute number on a slide comes from the printed parameters
   through `posb.band_detect_response`, which the tests pin. But §8.4's old
   "model sits 2–3× below the data" reading is withdrawn until someone
   re-locates the decade ticks on panels c and d, and a PS9 item must not use
   any §8 position.
