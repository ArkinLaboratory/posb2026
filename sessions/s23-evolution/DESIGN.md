# Session 23 — Burden becomes selection

Thursday 12 November 2026. Reading already assigned at the close of session 22:
Rottinghaus, Ferreiro, Fishbein, Dantas & Moon, *Nature Communications* **13**:672
(2022), "Genetically stable CRISPR-based kill switches for engineered microbes".

**Precedence.** If anything in this document disagrees with a built artifact,
the artifact is right and this file is stale. Every number quoted here is in
`NUMBERS.md` with its kind and its page.

---

## 0 · The title and the opening carry the main point

Standing rule, stated by Adam on 1 November: a session's title slide and its
opening are not scene-setting — they state the single claim the hour
establishes, in the words the session will use for it. The test: read the title
and the first slides and say what the session proves. If that is not the main
point, the title is decoration.

**Published catalog title, unchanged and already in students' hands:**
*Evolutionary failure and containment.* `course.yaml` and the syllabus keep it.

**Title slide:** **Burden becomes selection.** One claim. Chosen over "Your
circuit has a half-life" and "The circuit the population deletes" because it
makes the hour continuous with session 19 rather than announcing a new topic —
the room has already measured this number.

**The main point, in one sentence, and the opening has to establish it:** the
growth cost measured in session 19 is a selection coefficient, so a population
removes a circuit on a schedule you can compute — and that schedule is
logarithmic in the mutation rate and inverse in the cost **for s/μ above
413**, so in that regime cutting burden buys far more than hardening DNA — **for the
longevity question only.** (Added 2 November: §7b of NUMBERS.md shows the
containment question has the opposite sensitivity, 80× on μ against 1.1× on s.
The main point as written above is true and is the spine; it needs the scope
word or segment 5 contradicts segment 3. **Adam to confirm the phrasing.**)
Below 413 the ranking reverses and dividing μ by a hundred wins; the boundary
is measured, identical at five values of s, and is a good thing to make the
room find.

**So the first minute names three things and no more:** that the state variable
is now a fraction of a population rather than a concentration; that the clock
is generations; and that the number driving all of it is one the room measured
three weeks ago. The corollary about containment being a duration rather than a
measurement is segment 5's and is not pre-announced.

What the opening must NOT do: pose evolutionary failure as a new subject, or
open on the kill switch. The kill switch is the object (segment 1) and it
arrives after the claim, not before it.

---

## 1 · This rung breaks the ladder

Part II has been one ladder, and every rung has been a coupling the designer
can do something about:

| rung | session | the coupling | what you do about it |
|---|---|---|---|
| 1 | 19 | the circuit draws on shared ribosomes | measure the burden |
| 2 | 20 | stoichiometry bounds the achievable flux | compute the bound |
| 3 | 21 | the downstream load retroacts on the module | insulate it |
| 4 | 22 | a disturbance moves the output | reject it, exactly |

The trajectory is increasing designer power — from a tax you must pay to a
disturbance you can annihilate. Session 23 is the first failure mode that
answers to none of it. The circuit is not perturbed; it is **selected against**,
and the population removes it on purpose. There is no insulation device for
mutation, and feedback cannot help, because the controller is encoded in the
thing being removed.

What makes this teachable rather than merely sobering is that **session 19's
burden is the same number read a second way.** Session 19 measured the cost of
a circuit as a growth-rate decrement, from Scott 2010's linear laws — roughly
two percent of growth rate per one percent of proteome diverted. Put two
strains in one flask and that decrement is a *selection coefficient*. Rung 1
comes back as the thing that kills the device. That connection is free and it
is the session's spine.

**The honest conclusion, which the arithmetic in §4 forces:** three of the four
levers against evolutionary failure are not circuit design. That is why this
session sits where it does. Sessions 24, 25 and 26 are all about designing
*with* population-level processes rather than against them, and session 23 is
the hinge that earns them.

---

## 2 · The room has never met the three words this session runs on

The count, taken across `decks/s01*.py` through `decks/s22*.py` before anything
was designed:

| term | mentions in decks s01–s22 |
|---|---|
| **fitness** | **0** |
| **selection coefficient** | **0** |
| **mutation rate** | **0** |
| kill switch | 0 |
| containment / biocontainment | 0 |
| SOS response | 0 |
| probiotic | 0 |
| serial passage | 0 |
| aTc | 175 |
| TetR | 32 |
| generation | 32 |
| Cas9 | 16 |
| evolution / evolv- | 26 |
| gRNA | 10 |
| escape | 7 |
| mutant | 5 |

So the three load-bearing quantities of the hour are new vocabulary, and a
session written from the mathematics outward would open with two symbols the
room has never seen. This is the session-6 failure exactly, and §6 is built to
avoid it.

The compensation is large and should be used: **aTc and TetR are the most
heavily used parts in the entire course.** Rottinghaus drive Cas9 and the gRNAs
from P*tet*, repressed by constitutively expressed TetR, released by aTc. The
room knows that circuit cold. The only genuinely new object in the construct is
the *name* kill switch and the containment framing around it.

**What must be drawn before anything is modelled:**

1. **A population, not a cell.** Every prior session modelled one cell, or
   concentrations inside one. The state variable here is a *fraction of a
   population*. That is as large a change of object as the phase plane was in
   session 8, and it gets its own slides.
2. **Generations as the clock.** Not minutes. Derived from the passage protocol
   on a slide — see NUMBERS.md §1, it is one division.
3. **Fitness as a growth-rate ratio, and s as its complement**, arriving out of
   session 19's measured decrement rather than as a definition.

---

## 3 · The four moves

**Move 1 — Two strains in a flask.** Start from the s19 burden number the room
already has. One strain carries the circuit and grows at (1−s) times the other.
Ask for the ratio after 200 generations before any algebra. The answer is large
and it does the motivating work.

**Move 2 — Add mutation and derive the failure time.** The broken fraction q
obeys

    dq/dt = (1 − q)(s q + μ)

which separates, and the integral is elementary. In closed form

    t(q) = ln[ (s q + μ) / (μ (1 − q)) ] / (s + μ)

Both limits are worth their own slides. With no cost (s = 0) this is
q = 1 − e^(−μt), pure accumulation. With μ ≪ s the half-life is

    t₅₀ ≈ ln(s/μ) / s

**The design consequence is counterintuitive and exact: failure time is
logarithmic in the mutation rate and inverse in the selection coefficient.**
Reducing μ a hundredfold buys less than halving s. The ledger is in NUMBERS.md
§4 and it belongs on the slide that earns it, not at the end of the hour.

> ## ⛔ MOVE 3 IS WITHDRAWN — 1 November, after adversarial review
>
> **The k ≥ 3 inference below is wrong and must not be built.** It rests on a
> detection threshold of 10⁻³ that I chose and never wrote down. Rottinghaus
> state their plating sensitivity twice — *"Fraction viable values of <−8 or
> <−9 had no colonies obtained from cultures receiving aTc"* (Fig. 2 caption)
> and *"<-7"* (Fig. 4d). At 10⁻⁷ the same procedure returns **k = 1 at every
> burden**, and a one-hit model with s = 0 and μ = 8.9×10⁻¹⁰ fits both target
> numbers exactly. So "no single-mutation model fits all three measured
> numbers" is false; it was true only at my threshold.
>
> **"A one-hit process has no onset" is also false.** It holds at s = 0 only.
> With a cost the one-hit curve bends on log–log axes: at the session's own
> reference s = 0.05 a single-hit process reads as slope **2.55** over a
> decade and **5.59** locally — indistinguishable from three cassettes.
> Selection and redundancy are confounded on that plot. Pinned now in
> `test_selection_alone_forges_a_multi_hit_slope`.
>
> **Two further defects in the same argument.** The two numbers come from
> different strains — 10⁻⁸·⁶ is the optimized 2-gRNA plasmid construct, the
> 112-generation onset is the three-gRNA InfA CRISPRks rebuild, and the paper
> says the intermediate steps *lost* efficiency. And the paper's own
> conclusion is that escapers arose **de novo during induction** via the SOS
> response, not from standing variation during permissive growth — which is
> the mechanism this whole model describes.
>
> **What survives:** the ODE and its closed form (verified to 4×10⁻¹³), the
> ledger, the dose/requirement matching, the generations arithmetic, and the
> thesis that containment is a duration rather than a measurement. The
> *conclusion* of move 4 is right; the arithmetic offered for it is not.
>
> **The replacement is better and is Adam's call.** The honest lesson is that
> you *cannot* read the architecture off a stability curve, because burden
> bends it the same way redundancy does — and that the real mechanism is a
> device which raises its own mutation rate when operated, which is what
> Δrpdu removes. That is rule 6 at a higher level than the version below.

**Move 3 — The data refuses the model (rule 6).** ⛔ **WITHDRAWN, see above.** Fit μ from the paper's own
onset — non-functional cells appearing at 112 generations. The fitted μ then
predicts a standing escape fraction one to three orders of magnitude *above*
the escape fraction the same paper measures. Push s up to fix it and the model
says the circuit is essentially all broken by 224 generations, which contradicts
the measured stability. **No single-mutation model fits all three measured
numbers at once.**

The resolution is the architecture. With k cassettes mutating independently,
each intact with probability e^(−μ₁t),

    q(t) = (1 − e^(−μ₁ t))^k  ≈  (μ₁ t)^k

so the log–log slope of escape against time *is* k. A one-hit process is linear
from the first generation and **has no onset at all**; an onset is the
signature of redundancy. Fitting the paper's two numbers forces **k ≥ 3** over
the burden range session 19 implies — and the authors built four redundant
P*tet*-cas9 cassettes and three gRNA cassettes. The model recovers the
architecture from the performance data.

Both explanations for the measured diminishing returns at the fourth
integration get taught, because both are real and the pair is the lesson:
theirs is measured — the bottleneck moved to the P*tet*-gRNA promoter, which
they sequenced — and ours is that each added cassette raises s while lowering
μ₁, and the closed form says s is the expensive direction.

**Move 4 — The requirement, and the thing a circuit cannot do.** The NIH Office
of Biotechnology Activities figure is a fraction viable of 10⁻⁸. Their gavage
dose is 10⁸ CFU. Those two numbers are matched: the requirement is *fewer than
one survivor per dose*, and the room should be asked to notice that before
being told.

The measured circuit clears it — 10⁻⁸·⁶ is a quarter of a survivor per dose.
Then ask how long that claim lasts. With the fitted parameters the standing
escape fraction crosses 10⁻⁸ in **0.01 to 7.5 generations** across the whole
plausible grid of s and μ (NUMBERS.md §7) — under a day in every case. "About
three generations" stood here until 2 November and is not reproducible at any
point on that grid; quote the range, which makes the point better anyway. The assay is a snapshot; containment is a duration, and the
two are not the same quantity.

Which is why the paper needs the thing that is not a circuit. Intra-niche
competition does not lower μ at all. It changes the sign of the escaper's
advantage — competitive exclusion, which in the model is a re-parameterization
of s rather than a new term. Their own results, with the strains kept straight:
plain CRISPRks monoculture rebounds to pre-induction levels by 48 h, and a 1:1
competitor improves the 24 h kill from 10⁻³·³ to 10⁻⁴·² — an improvement, not
an elimination. **Elimination by 72 h, and the 1:1000 result, are CRISPRks
Δrpdu**: competition plus the lowered induction-dependent mutation rate. Two
levers together. Do not credit the elimination to competition alone, and do not
credit it to the plain strain.

**The four levers, and the close:** lower s (circuit design, partly), lower μ₁
(sequence and architecture, not circuit), raise k (architecture), change the
selection environment (ecology). Plus the fifth thing that is not a lever at
all — state a finite retention time as a specification and design the protocol
around it. One of those is the toolbox the room has been building. That is the
hand-off to sessions 24–26.

---

## 4 · The paper has to be taught, not cited (rule 11)

Sessions 20 and 21 showed **three** and **five** paper figures and session 22
shows **one** — and
rule 11 names that as the defect. Session 19 is the shape that works: a
dedicated move label, with paper slides woven through segments 1, 2 and 5
rather than collected into a block after the derivation has spent the room's
attention.

Target for this session: **at least seven paper figure slides**, distributed.
The panels that must be worked rather than referred to, with what each is for:

| panel | what it shows | where it goes |
|---|---|---|
| Fig. 1a | the circuit — P*tet*-cas9, P*tet*-gRNA, TetR, aTc | segment 1, the object |
| Fig. 1d | the mutation spectrum: which cassette breaks | segment 3, why redundancy targets Cas9 |
| Fig. 1f | Int X1→X4, fraction viable falling | segment 3, redundancy working |
| Fig. 1g | Int X4 survivors — the bottleneck has moved | segment 3, why it stops working |
| Fig. 2e | 28-day stability, fraction viable against day | segment 2, **this is q(t) on the paper's own axes** |
| Fig. 2g | generation time against log fraction viable | segment 4, the growth-rate coupling back to s19/s20 |
| Fig. 3a | competition against monoculture | segment 5, the lever that is not a circuit |
| Fig. 3b/c | survivor mutation profiles | segment 5, Δrpdu lowers induced μ only |

**Fig. 2e is the gift.** Fraction viable is CFU(+aTc)/CFU(−aTc): a functional
cell dies on induction and a broken one survives, so the paper's y-axis *is*
the model's state variable q. The model can be drawn on their axes. Note the
mapping explicitly on the slide — it is an approximation, since killing is not
perfect even for functional cells, and NUMBERS.md §6 says so.

---

## 5 · Three things not to let a later pass undo

1. **Do not open with the model.** §2 is the reason. The three words do not
   exist in this course yet.
2. **The engineering consequence of t₅₀ ≈ ln(s/μ)/s goes on the slide that
   derives it** (rule 3), not into a design ledger at the end. It is the one
   result in the hour that changes what a designer does.
3. **k ≥ 3 is an inference of ours with a stated regime, not the paper's
   claim.** It holds for s ≲ 0.05 and weakens above s ≈ 0.08, where burden
   alone explains the delay. It is also sensitive to the assumed plating
   detection threshold. Never write it as something Rottinghaus report. The
   bounds are in NUMBERS.md §5 and in the test suite.

---

## 6 · Segments

Written as content, with no durations. Student work in short bouts per the
in-class rule; no breakout rooms.

**Segment 1 — the object before the model.** What a kill switch is and what it
is for. Fig. 1a, which is TetR and aTc doing what the room has watched them do
since session 6, now wired to Cas9 cutting the genome. Then the change of
object: one cell becomes a population, minutes become generations. Derive
generations from the passage protocol at the board and on the slide (rule 14).
Close with the question that tees up the controls: *you have this strain in
your hands; what can you change, and what would you have to do to change each
one?* Answers go on the board and stay there until the four levers in segment 5
are checked against them.

**Segment 2 — fitness, and the number you already have.** Two strains, one
flask, session 19's decrement. Define fitness as a ratio and s as its
complement. Commit to a number for the ratio after 200 generations, then show
it. Fig. 2e: here is what the measurement actually looks like over 28 days, and
here is the quantity on its y-axis.

**Segment 3 — the derivation, one move per slide.** Mutation added; the ODE;
separate; partial fractions; integrate; invert. Then the two limits, each on
its own slide. Then the ledger: what halving s buys against what dividing μ by
a hundred buys. This is the segment the hour is built on and it is where the
design consequence lands.

**One slide closes segment 3: the same asymmetry, run backwards.** The ledger
has just shown that s dominates μ. Two sentences, then stop. The asymmetry is
not only a statement about losing a circuit — it is a statement about crossing
sequence space. A mutation rate raised on one locus and held at background
everywhere else, against a selection you chose, is how proteins are actually
engineered, and ln(s/μ)/s read that way is a search time rather than a failure
time. Point at session 27 and move on.

**Why here and not in segment 5.** Segment 5 carries the thesis, and the hour
overruns at the end, so whatever sits last is what gets cut. This slide belongs
where the ledger earns it.

**And it creates an obligation, which this repository has been bitten by
before.** `docs/coverage-matrix.md` records a session-4 speaker note that
promised a quantitative result "in session 13" against a deck that never
carried it, and a grep for forward pointers naming session 18 turned up four
more. A note promising a future session is an unchecked cross-reference and
nothing in the build catches it. So: **session 27 must demonstrate how a
continuous-evolution system works** — a locus mutated far above background, the
chassis protected from it, a selection imposed — or this slide is a promise the
course does not keep. Session 27 owes that demonstration in any case: T72 asks
students on the final to compare generative design against directed-evolution
yield, and at present no session shows them what directed evolution is
mechanically. Before session 27 is built, run
`grep -n -o -i "session 27[^.\"]\{0,70\}" decks/*.py` and treat every hit as
a contract.

**Segment 4 — our model is the one the data refuses (rule 6, turned on
ourselves).** Rewritten 2 November; the previous version built the withdrawn
k ≥ 3 argument and must not be restored.

Build the redundancy model honestly: k independent cassettes, each intact with
probability e^(−μ₁t), so q = (1 − e^(−μ₁t))^k and the log–log slope is k.
Invite the room to read the architecture off the stability curve — it is the
obvious move and it is what a modeller wants to do.

**Then do what segment 3 demands: go and put a number on the burden.** Show
Fig. 2e first — it is not a floor, it rises from about 10⁻⁸ at day 1 to
10⁻⁶·³⁵ at day 28. Fit the model to it (NUMBERS.md §5b, figure
`s23_measure_s`): the best fit is s = 0 with μ = 2.63 × 10⁻⁹, RMS 0.151
decades, and s = 0.05 misses by 1.2.

**But plot the flat null on the same axes, and say what it costs you.** A
horizontal line scores 0.204 — the rise beats no-rise-at-all by 25 % in RMS on
eight points, and the data's own log–log slope is 0.63 where every model in
this family predicts ≥ 1. So the honest claim is a **bound**: s is below about
0.02, and the hour's own reference s = 0.05 is excluded by the authors' data.
Say *bounds from above*, never *measures*. The circuit is nearly free under
permissive growth, which is why it lasts a month — and the room gets to watch
the difference between a bound and a measurement, which is worth more than the
number.

> ⛔ **Do not rebuild the refutation version.** An earlier pass on 2 November
> claimed the model was refuted here, using 10⁻⁸·⁶ as the 28-day bound. That
> number is **Fig. 1h** — a different strain, with antibiotics, one timepoint.
> Fig. 2e is CRISPRks. Using one strain's number as another's bound is exactly
> what killed the k ≥ 3 argument, committed a second time.

Second, the confounding. Put a one-cassette circuit with a 5 % burden on the
same axes. It reads as slope 2.36 over a decade and 5.02 locally: two to five
cassettes. Matched at t = 100 the two curves agree within a factor of 4 across
the whole decade. Selection bends the curve exactly the way redundancy does,
and **the measurement cannot separate them** (NUMBERS.md §5, with the window
stated — not stating it is what broke the first version of this argument).

So the honest conclusion is a negative one, and it is the more useful result:
you cannot infer the architecture from a stability curve. What you *can* do is
notice what the paper's own data says about mechanism — escapers arose **de
novo during induction** via the SOS response, not from standing variation
during permissive growth. **The device raises its own mutation rate when it is
operated.** That is not in any version of the model above, and it is what
Δrpdu removes.

Fig. 1d, 1f, 1g in sequence: which cassette breaks, what redundancy bought,
where it stopped buying — shown as what the authors measured and iterated on,
not as confirmation of a fit. Fig. 2g for the growth-rate coupling: the
circuit's performance depends on how fast the cells are growing, which is
session 19 and session 20 arriving in a containment problem.

**Then the turn that actually matters.** If the circuit is costless and
stable for a month in a flask, why did it fail in a mouse? Nothing in this
model describes the second route — SOS mutagenesis from the device's own
cuts, which the authors report appears only in vivo. The model is complete for
permissive growth and silent about operation. That is a better failure than a
refutation, because the room has just watched the model succeed.

Close the segment on the two asymmetries (NUMBERS.md §7b): t₅₀ moves 4.4× on s
and 1.4× on μ; retention moves 1.1× on s and 80× on μ. Burden reduction is the
longevity lever, mutation-rate reduction is the containment lever, and Δrpdu is
aimed at the right one. **This is the result segment 5's thesis rests on.**

**Segment 5 — the requirement, and the lever that is not a circuit.** The NIH
figure and their dose; let the room match them. The retention calculation.
Then Fig. 3a and 3b/c: competition, and what Δrpdu does and does not do. The
four levers, checked against the board from segment 1. Close by assigning the
session 24 readings -- **both of them**, Balagadde 2008 and Basu 2005, under the
`s23` override in `readings.yaml` (two required papers, 13 pages). Session 24
carries three topics and one paper does not serve them; the override's `reason`
field carries the argument. Optional alongside: Karig 2018 and Tsoi 2018.

---

## 7 · What the build needs, in order

Design → numbers → library → tests → figures → deck. That order held for
session 22 and session 23 has more library in it than any session since 20.

1. **`NUMBERS.md`** — written, beside this file.
2. **`posb/evolution.py`** — written. `time_to_failure`, `broken_fraction`,
   `multi_hit_broken_fraction`, `fitness_cost_from_growth`,
   `fitness_cost_from_competition`, `escapers_per_dose`, `retention_time`.
   T61 and T63 are autograded on PS9 and T61 is on the final, so these are the
   functions the problem set will import.
3. **`tests/test_evolution.py`** — written. Closed form against numerical
   integration over a grid including s = 0; the log–log slope against k by
   exhaustion; two-sided bounds on every number quoted in this file.
4. **Figures** — not built. Needed: q(t) for one hit against k hits on log–log
   axes with the slope annotated; the s-against-μ ledger as a contour or a
   small table of t₅₀; the retention crossing against the NIH line; the model
   drawn on Fig. 2e's axes.
5. **Deck** — not built, and it should not be built until the segment structure
   above is approved. **Segment 3's closing slide pointing at session 27 is
   approved and is part of the plan** (Adam, 1 November), with the session-27
   obligation it creates recorded beside it.
6. **Home guide, answer sheet, board notes** — not built. PS9 may not re-ask a
   guide item, and the guide/problem-set collision check runs across the whole
   set, not per tagged session.

**PS9 dependency.** PS9 posts 19 November and carries T61 and T63 as autograded
items. It cannot be authored before this library exists, and sessions 24, 25
and 26 are also in its window and also unbuilt. That, not this session, is the
schedule's binding constraint.
