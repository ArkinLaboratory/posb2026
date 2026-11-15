# Session 24 — The wire is now outside the cell

Tuesday 17 November 2026. Readings assigned at the close of session 23:
Balagaddé, Song, Ozaki, Collins, Barnet, Arnold, Quake & You, *Molecular
Systems Biology* **4**:187 (2008), "A synthetic *Escherichia coli*
predator–prey ecosystem"; and Basu, Gerchman, Collins, Arnold & Weiss,
*Nature* **434**(7037):1130–1134 (2005), "A synthetic multicellular system for
programmed pattern formation".

Optional: Karig, Martini, Lu, DeLateur, Goldenfeld & Weiss, *PNAS*
**115**(26):6572–6577 (2018), for the Turing half; Tsoi, Wu, Zhang, Bewick,
Karig & You, *PNAS* **115**(10):2526–2531 (2018), for division of labour.

**Precedence.** If anything here disagrees with a built artifact, the artifact
is right and this file is stale. Every number is in `NUMBERS.md` with its kind
and its page.

---

## 0 · The title and the opening carry the main point

**Published catalog title, already in students' hands:** *Communities:
cell–cell communication, quorum sensing, patterning, division of labor.*
`course.yaml` and the syllabus keep it.

**Title slide:** **The wire is now outside the cell.** One claim. Chosen over
"Engineering a community", "Two strains, one circuit" and "Distance is a
concentration" because it names what changed rather than the subject, and
because every one of the session's three topics is a consequence of it.

**The main point, in one sentence:** for twenty-three sessions every connection
in a circuit has been a molecule inside one cell, and the moment a signal
leaves the cell the connection acquires **a length scale and a delay** —
so a population can compute what no single cell can, and the new design
parameters belong to the medium rather than to the plasmid.

**The opening names three things and no more:** that the wire has left the cell;
that the number which now governs the circuit is a diffusion coefficient the
room already knows how to use; and that a population can therefore read its own
density, each cell's position, and split a job — none of which a single cell
can do.

What the opening must NOT do: open on quorum sensing as a biology topic. The
chemistry arrives in segment 1 as the object, after the claim.

---

## 1 · Where this sits: from the context that breaks a circuit to the context that *is* the circuit

Sessions 19–23 were one ladder, each rung a context that breaks a circuit:
competition for ribosomes, stoichiometry, a load the block diagram mis-draws, a
controller that rejects disturbances, and finally selection, which session 23
showed you cannot reject at all. Session 23 closed on a finding: the levers
that actually worked in Rottinghaus were **intra-niche competition and host
deletions**, neither of them circuit design.

Session 24 takes that seriously and inverts the ladder. **The population stops
being the thing that breaks your circuit and becomes the thing you build with.**

| session | the population is |
|---|---|
| 19–22 | a source of coupling you did not design |
| 23 | the adversary — it deletes the circuit |
| **24** | **the device** — another strain holds this one's life |
| 25 | the carrier — the thing you build is supposed to spread |

---

## 2 · The room has met the motif, and has never seen a plate

The vocabulary census across all 22 built decks is in `PRIOR-YEARS.md` §4. Two
results, and they point opposite ways.

**What the room already has, and the session must not re-teach.** Session 10
genuinely taught a sender/receiver AHL circuit on slides: `sender` 9 hits,
`receiver` 12, `AHL` 24, `LuxR` 5, including the line that receivers pulse
above 47 nM AHL. Session 10 also assigned Basu *2004*, the pulse generator,
from the same laboratory. **So the room has met senders, receivers, AHL, LuxR
and the feed-forward loop.**

**What has zero occurrences anywhere**: quorum sensing, autoinducer,
acyl-homoserine lactone, LuxI, pattern formation, Turing, morphogen, lawn,
consortium, co-culture, cross-feeding, mutualism, predator, prey,
Lotka–Volterra, carrying capacity, chemostat, division of labour.

So the gap is not the signal. **It is the synthase, the arena, and the second
population.** Specifically:

| object | why it cannot be words |
|---|---|
| **LuxI, the synthase half** | s10 drew cells that *respond* to AHL and never drew a cell that *makes* it. Without the synthase, quorum sensing is not a readout of anything |
| **a plate, with a lawn and a sender disk** | the room has never seen one. Every spatial intuition this hour needs is a picture of a Petri dish |
| **a chemostat, and a dilution rate** | the predator–prey result is a statement about a reactor, and D is its knob |
| **two populations in one vessel** | drawn as two cells with two arrows between them, before any model |

**The one callback that does most of the work.** Basu's band detector is not a
new motif. The paper says so: the non-monotonic response comes from the
different repression efficiencies of CI and LacI_M1 "in combination with a
feed-forward loop that begins with LuxR and culminates in GFP". **Session 10
taught feed-forward loops and the pulse they make in time. Session 24 feeds the
same motif a spatial gradient and gets a band in space.** A pulse in time and a
ring on a plate are one motif reading two different inputs. That sentence
belongs on a slide in segment 2, and it converts the band detector from a new
object into a known one with a new input.

**Name collision to disarm:** the dilution rate D in the predator–prey model is
not session 22's controller gain d, and not session 25's antiviral fraction D
two days later. Say so when it first appears.

**Cheapest new mathematics in the session:** Lotka–Volterra. Nullclines (24
hits), Jacobian (22), eigenvalues (20) and the phase plane (15) are all in hand
from session 8. The room can do the stability analysis of a two-species system
the first time it sees one.

---

## 3 · The four moves

### Move 1 — The object: a molecule that leaves

Draw a cell making AHL — LuxI, the synthase, which session 10 never drew. Draw
it leaving. Then the two things that fall out of a molecule being *outside*:

- **It reports density.** One cell's AHL is undetectable; ten million cells in
  the same volume is a concentration. The cell has no way to count its
  neighbours and does not need one.
- **It reports position.** Put the makers in one place and the concentration at
  any point is a function of distance from them.

**Then the number.** Session 2 established t ~ L²/2D and said, on the slide,
to state the convention before the number. Karig et al. estimate the
cell-to-cell diffusion coefficient of 3OC12HSL at **83 µm²/s**. Session 2's own
numbers were 7.7 µm²/s for GFP inside *E. coli* and 87 µm²/s for GFP in water.
**So the signal between cells travels at about the speed of a protein in water
and roughly ten times faster than a protein inside a cell** — and the room
computes the consequence rather than being told it.

This is **T66**, and it is the fourth use of session 2's result. The sharp point
is the reversal: session 3 used the same relation to argue there is *no*
spatial gradient worth speaking of inside one cell. A community is exactly
where that inequality turns over. Same formula, opposite conclusion, because L
changed by four orders of magnitude.

> **A gap, stated and not hidden.** Basu prints ξ = 0.001 mm²/min for AHL, and
> it cannot be used: substituted into L²/2ξ it puts Basu's own 10 mm ring at
> 833 hours against a 36-hour experiment. The cause is in their equation (5),
> a discrete Laplacian written with no grid spacing, so ξ is really D/Δx² and
> Δx is never stated. **Do not take a diffusion coefficient from Basu.** The
> Karig number is the sourced one. `NUMBERS.md` §16.6 carries the arithmetic.

### Move 2 — One motif, a new input: the band

Set up the paper properly (rule 11). Senders carry LuxI under an inducible
promoter. Receivers carry LuxR, and AHL·LuxR drives two repressors — CI and a
codon-modified LacI. Work the logic from the paper's own words, because it is
a three-case argument and each case is a slide:

- **Close to the senders**, AHL is high, both repressors are high, GFP is off.
- **Far from the senders**, AHL is low, both are at basal levels — which
  *enables* expression of wild-type LacI from the second plasmid, and GFP is
  off again.
- **In between**, CI represses LacI harder than LacI_M1 represses GFP, so CI
  shuts off the wild-type LacI while LacI_M1 is still below the threshold that
  would silence GFP. **GFP is on only in the middle.**

Then name it: that is a feed-forward loop, the room met it in session 10, and
the only new thing is that its input is a distance. **The ring is the pulse,
drawn in space.**

**The naming trap, which must be pinned before any prompt is written:** the
*high-detect* component sets the AHL concentration **above which** GFP is
muted — the band's upper edge — and the *low-detect* component sets the
lowest AHL that elicits a response — the lower edge. The names are the reverse
of what they sound like, and the paper states it plainly on p. 1130.

**T65 is built on the model, not on the data.** Basu prints no numeric
threshold, band position, band width or error bar anywhere — every such number
in circulation is a digitization. What the paper *does* print is a complete
five-species model, equations (1)–(5), a fourteen-parameter set for BD2, the
exact variant rules for BD1 and BD3, and the two fitted dose–response forms
(a sigmoid for the high-detect strains, a bell for the band strains). The
autograded item uses the **liquid-phase limit**, which the paper itself defines
by dropping equation (5) and which is therefore fully specified.

**The wrong turn, and it is in a *Nature* abstract.** Basu's abstract says
"experimental and theoretical analyses reveal which kinetic parameters most
significantly affect ring development". The analysis is 100 simulations drawn
from 2,000 random parameter sets, regressed against their own inputs: γ_L
against shift-begin R² = 0.91, CI repression efficiency against positional
shift R² = 0.05, and every other rate constant R² < 0.001 with P > 0.75. **No
experiment enters that regression.** The experimental contribution is one time
course compared with one simulation by eye. This is the session's cleanest
MEASURED-versus-MODELLED mis-tag, it is in a paper the room has read, and it is
exactly the skill the course keeps asking for. Show the regression, ask what
was measured, let them find it.

### Move 3 — Two populations, and a stability analysis the room can already do

Balagaddé's circuit, from Box 1A: two strains, each controlling the other's
survival through a quorum signal — the predator kills the prey by inducing a
killer protein in it, the prey rescues the predator by inducing an antidote.
Draw the wiring before any equations.

Then the model. This is where the session does mathematics, and it is the
cheapest new model in the course because the room has the machinery:

- two logistic growth terms sharing a carrying capacity
- a death term for each population modulated by the *other's* signal
- a dilution rate D common to both, because this is a chemostat

Write the nullclines, take the Jacobian, and find where the eigenvalues cross
the imaginary axis. **That crossing is a Hopf bifurcation**, and the room met
the same object in session 11 for the repressilator — a ring of three. Here it
is a ring of two populations. Say that out loud; it is the second time this
session that a known motif reappears with a new substrate.

**The design consequence, which is what the move is for:** the oscillation is
not a property of the strains. It is a property of the strains *and the
dilution rate*, and D is set by the experimenter. A community's dynamics are
tuned from outside the cells.

> **The honest reading of the data, and it belongs on a slide.** Fig. 2A is one
> reactor; the caption's own hedge is that the behaviour was elicited "in
> several reactors", and the twelve-panel companion shows several induced
> reactors with prey high and predator flat for 200 hours — prey domination,
> not oscillation. Worse for the model: its oscillatory window is roughly
> 0.04 ≲ D ≲ 0.18 h⁻¹ with a minimum period near 73 h, and the two experimental
> "damped oscillations" sit at D = 0.20 and 0.23 h⁻¹ with periods of about 50
> and 30 h — **outside the window and faster than the model's fastest**. The
> paper says the model "qualitatively accounts for" the observations, and that
> phrase is carrying the whole discrepancy. Rule 6: teach the reading, why it
> fails, and what replaces it.

### Move 4 — When is a second strain worth it

Declare the change of question on its own slide (rule 9): the first three moves
built communities; this one asks when you should.

Tsoi et al. give the criterion. Split a two-step pathway across two populations
and you reduce the burden each one carries — session 19's number — but you pay
to move the intermediate between cells, and that transport is lossy. The
criterion compares the two, and the session derives its shape rather than
quoting it.

Two things from that paper belong on the slide together:

- the **border moves by a factor of five** depending on the functional form
  assumed for burden — linear, exponential or Hill — while the *form* of the
  criterion does not change. A result whose threshold depends on an unmeasured
  functional form is a result you report with its assumption attached.
- the **caption of Fig. 1D puts the border at ln(·) = 1 and equation 16 puts it
  at 0**; the figure itself is drawn correctly. Another printed defect, found
  by reading rather than assuming.

**And the honest statement of what this move rests on**: Tsoi is a modelling
paper with no experiment, and it is optional reading. Division of labour is the
one topic in this session's title with no required paper behind it, which is a
deliberate choice recorded in `readings.yaml`, not an oversight.

Close the move — and the session — on the archive's own best motivation, from
the 20.405 notes: Voigt's XOR split across four colonies on a plate, because
the gates reuse the same three promoters and cannot coexist in one cell. **The
reason to use a community is sometimes that one cell does not have enough
orthogonal parts.** That connects straight back to session 17.

---

## 4 · The paper has to be taught, not cited

Two required papers, and the standing count says sessions that showed one paper
figure failed. `NUMBERS.md` §14 lists nine Balagaddé panels, nine Basu panels
and five Tsoi panels with what each lets a student conclude. The ones this
design commits to:

| figure | move | what the room concludes |
|---|---|---|
| Balagaddé Box 1A | 3 | the complete two-cell wiring — the structural basis for **T64** |
| Balagaddé Box 1B | 3 | a two-parameter regime diagram of a community |
| Balagaddé Fig. 2B | 3 | the twelve-reactor companion — the honest version of 2A |
| Balagaddé Fig. 3C | 3 | the model's oscillatory window, against which the data sit outside |
| Basu Fig. 1a | 2 | the printed truth table — non-monotonicity as a logical fact before any kinetics |
| Basu Fig. 2d | 2 | the bell-shaped dose–response, three strains, three thresholds |
| Basu Fig. 3b + 3c | 2 | the geometry inversion: the most sensitive strain makes the **outermost** ring — and the 30 mm against 22 mm reproducibility |
| Basu Fig. 5b–d | 2 | one lawn, four sender layouts, four patterns. The pattern is in the boundary conditions |
| Tsoi Fig. 1C | 4 | biomass gain against transport inefficiency, as a picture |

Basu Fig. 5a is a **simulation**; 5b–d are experiments. The patterns are an
ellipse (two senders), a heart (three) and a clover (four) — the abstract names
only ellipses and clovers, and a slide that repeats the abstract will miscount
the figure in front of the room.

### T64 and the model students actually run

Balagaddé prints no rate constant of any kind. The parameters live in the
**BioModels** deposit, `BIOMD0000000296` — a curated SBML of the reduced model,
which independent curation reproduces parts of the paper's Fig. 2 from. Two
consequences, both of which go on the slide and into the problem-set item: it
is the **reduced** model, not the full one; and the deposit is BioModels' work,
not the paper's — the paper never mentions it. `readings.yaml` currently tells
students the model "is in BioModels" in a way that reads as the paper saying
so, and that wording gets fixed.

Basu's equations model the **receiver only**. The sender is a tuned boundary
condition and no sender synthesis rate is printed anywhere. **A T64 task asking
for a sender and a receiver must supply the sender rate itself**, and say that
it is doing so.

---

## 5 · Five things a later pass must not undo

1. **The feed-forward callback stays.** Deleting it turns the band detector
   back into a new object and wastes the only thing session 10 left for this
   hour.
2. **Do not take a diffusion coefficient from Basu.** §16.6 has the arithmetic.
   Any later pass that "sources" ξ from the paper reintroduces an error with a
   factor of twenty in it.
3. **T65 is built on the model, not the data.** Basu prints no thresholds. An
   autograded item built on digitized band positions is built on a number
   nobody published.
4. **Balagaddé Fig. 2A is one reactor.** The twelve-panel version goes beside
   it. Cutting the companion leaves the room with a cleaner result than the
   authors claimed.
5. **Division of labour's thin support is stated, not hidden.** One topic in
   the title, one optional modelling paper behind it. Say so.

**If the hour runs short, cut in this order**, and the board notes carry the
same list: Tsoi's functional-form sensitivity; then Basu Fig. 3b/3c's
reproducibility pair; then the Balagaddé window-versus-data comparison, keeping
the one-reactor caveat; then the Karig Turing material entirely. **Never cut
move 1's diffusion number or move 2's three-case band argument** — the first is
assessed as T66 and the second as T65.

---

## 6 · Segments

Badges follow s23: `open`, `frame`, `segment N`. No minute badges.

| badge | label | content |
|---|---|---|
| open | retrieval — sessions 2, 10 and 19 | three questions: s02's L²/2D and its convention; what s10's receiver did above 47 nM; what s19's burden number was |
| open | what you should be able to do by the end | three questions, posed as questions |
| frame | where this sits | the ladder inverted — the population stops breaking the circuit and becomes it |
| segment 1 | the object, before any model | LuxI, and a molecule leaving a cell |
| segment 1 | a signal that reports a crowd | density sensing, with no cell counting anything |
| segment 1 | a signal that reports a distance | the gradient, and a plate drawn for the first time |
| segment 1 | the number that governs all of it | 83 µm²/s against s02's 7.7 and 87; the reversal of s03's conclusion — **T66** |
| segment 2 | the paper · what they built | Basu Fig. 1a, the senders and receivers, and the printed truth table |
| segment 2 | three cases, and only one is on | the band logic, one case per slide |
| segment 2 | you have seen this motif | the feed-forward loop from s10, with a distance for an input |
| segment 2 | high and low, and the names are backwards | the two components and which edge each sets — **T65** |
| segment 2 | Vote · argue · vote again | a ConcepTest on which strain makes the outer ring, with its resolution |
| segment 2 | the paper · what they measured | Fig. 5b–d, and Fig. 3b/3c's 30 mm against 22 mm |
| segment 2 | what the abstract claims and what was measured | the regression against its own inputs |
| segment 3 | the paper · what they built | Balagaddé Box 1A, the two-cell wiring |
| segment 3 | two populations, two signals | the model, written down with the room |
| segment 3 | where the eigenvalues cross | nullclines, Jacobian, the Hopf — and the ring of three from s11 |
| segment 3 | a dial outside the cells | the dilution rate as the design knob |
| segment 3 | the paper · the result you read | Fig. 2B's twelve reactors, and Fig. 3C's window against the data |
| segment 4 | a different question | declare it: when is a second strain worth it |
| segment 4 | what you save and what you pay | the Tsoi criterion, derived in shape |
| segment 4 | and the threshold moves with an assumption | the five-fold functional-form result |
| close | sometimes one cell has not got enough parts | Voigt's XOR across four colonies, back to s17 |

Two ConcepTests, each with a resolution slide immediately after, and each with
its answer written out in the speaker note:

- **CT1, segment 2.** BD1 carries the hypersensitive LuxR; BD2 the wild type.
  Plated together with a sender disk, which one's ring is further from the
  senders? The intuitive answer is wrong, the paper's Fig. 3c settles it, and
  the resolution is that a more sensitive detector mutes at a *lower* AHL and
  therefore sits further out.
- **CT2, segment 3.** The predator–prey culture is oscillating. You double the
  dilution rate. Options separate "faster oscillation", "damped to a fixed
  point", "prey washes out" and "predator washes out" — and the honest
  resolution includes that the paper reports **three different washouts** in
  different conditions.

---

## 7 · What the build needs, in order

**`posb/communities.py`:**

| function | returns | notes |
|---|---|---|
| `diffusion_time(L, D)` | L²/(2D) | thin wrapper on s02's convention, so T66 and s02 cannot drift apart |
| `band_detect_response(AHL, params)` | GFP output | the liquid-phase limit of Basu's five-species model, eqs (1)–(4) |
| `band_edges(params)` | low and high AHL edges | solved, not read off a plot |
| `predator_prey_model(t, y, params)` | derivatives | Balagaddé's reduced model, parameters from the BioModels deposit |
| `pp_steady_states(params)` | fixed points | analytic where possible |
| `pp_jacobian(params)` / `pp_hopf_D(params)` | the Jacobian, and the dilution rate at the Hopf | **T64** |
| `dol_criterion(...)` | the division-of-labour comparison | Tsoi's criterion, with the burden form as an argument |

**`tests/test_communities.py`** — closed forms against quadrature, never against
an ODE solver. Specific assertions:

- `band_detect_response` is genuinely non-monotonic: assert a single interior
  maximum by a fine sweep, not by three sampled points
- `band_edges` round-trips against `band_detect_response`
- the Hopf dilution rate is bracketed two-sided, and the eigenvalue real part
  is asserted to change sign across it
- the oscillatory window is asserted as a **predicate** — that the experimental
  D values 0.20 and 0.23 fall **outside** it — so the session's claim about the
  model-data mismatch is executable and cannot drift into prose
- `diffusion_time` reproduces session 2's own printed numbers exactly, which is
  what stops a second convention appearing in the course

**Figures** (`figures/s24_communities.py`), each through `figure_fit`, inside
the 4.60 in band, curves tagged rather than legended:

1. the band-detect response against AHL on a log axis, three strains, with the
   two edges marked in the symbols the derivation used
2. the predator–prey phase plane with nullclines and the limit cycle, plus a
   small inset of the eigenvalue real part against D crossing zero
3. the diffusion ledger: time against length for the three D values (7.7, 83,
   87 µm²/s) on log–log, with a cell, a colony and a plate marked

**Deck** last.

**Paper figure crops** into `private/paper-figures/`, keys in
`decks/paper_figures.yaml`: `balagadde2008_box1a`, `_box1b`, `_fig2a`, `_fig2b`,
`_fig3c`; `basu2005_fig1a`, `_fig2d`, `_fig3b`, `_fig3c`, `_fig5`;
`tsoi2018_fig1c`.

**Wire-in, or it silently will not build:** `figures.s24_communities` into
`MODULES` in `tools/build_figures.py`; `s24_communities` into `DECKS` in
`tools/build_decks.py`.
