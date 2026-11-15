# Session 25 — It has to spread on its own

Thursday 19 November 2026. Reading assigned at the close of session 24:
Weinberger, Schaffer & Arkin, *J. Virol.* **77**(18):10028–10036 (2003).
Optional: Noble, Adlam, Church, Esvelt & Nowak, *eLife* **7**:e33423 (2018);
Huang & Baltimore, *Nature* **226**:325–327 (1970).

**Precedence.** If anything here disagrees with a built artifact, the artifact
is right and this file is stale. Every number is in `NUMBERS.md` with its kind
and its page.

**Revision note, 7 November.** This is version 2; the earlier draft is kept as
`DESIGN.v1.md`. Section 8 lists what changed and why, so a later pass does not
reinstate any of it. Everything outside section 8 states the requirement rather
than the history it came from, because a line in this file can reach a speaker
note.

**The paper is Adam's.** No hedging and no apology on a slide. It also gets
checked as hard as anyone else's, and the session finds **one transcription
slip and two facts about how the model got its numbers** — not three errors.
The slip is the printed δ in R₀ (`NUMBERS.md` §0). The two facts are that λ and
k were back-solved from T₀ and V₀ rather than measured (§2a), and that the
burst-size assumption is stated plainly in three places and bounded in none of
them (§4c, §17a).

---

## 0 · The title and the opening carry the main point

Standing rule: a session's title slide and its opening state the single claim
the hour establishes, in the words the session will use for it.

**Published catalog title, already in students' hands:** *Design at population
scale: defective interfering particles, therapeutic interfering particles, gene
drives — engineering a thing whose point is that it spreads.*

**Title slide:** **It has to spread on its own.**
**Subtitle:** *You still have only molecular knobs — and what they now set is
whether it spreads faster than it is removed.*

> **Subtitle changed 14 November 2026.** It read *"Once the thing you build has
> to spread by itself, making it a better drug can stop it working."* That is
> move 4's claim, and the note immediately below this one explains why the
> TITLE is not allowed to carry it — because move 5 contradicts it. The
> subtitle was carrying it anyway, so it held for three moves of five. The
> replacement holds for all five and names the link Adam asked for: the knobs
> are the same molecular ones the course has used for twenty-four sessions,
> and the quantity they now move is a population's. **The architecture claim —
> whether the payload rides inside the vector's fitness or fights it — becomes
> the hour's CLOSING sentence**, which is where a finding belongs. The title
> says what the hour is about; the last slide says what it established.

Title plain, subtitle carrying the claim — session 23's pattern. The technical
form, R₀ᵀ > 1, arrives in move 3 where it is derived, rather than sitting on a
title slide in a symbol the course has never defined.

> **Why the title is not *"Your payload is the vector's own fitness"*.** That
> claim is established by moves 2–4 and **contradicted by move 5**, where a
> gene drive's cargo cost and its homing bias are two separable quantities. It
> is the title of move 4, which is where it holds.

**The main point, in one sentence:** when the thing you are designing has to
spread, the specification stops being a transfer function and becomes a
reproductive ratio greater than one — and **what trades against what in that
ratio is a property of the architecture, not of the idea.** In Weinberger's
vector the therapeutic payload sits inside the vector's own fitness, so there
is an optimum rather than a maximum; in a gene drive the two come apart.

**The opening names three things and no more:** that the thing being designed
is an infectious agent rather than a circuit inside a host you own; that its
specification is therefore a number greater than one; and that the room already
has every piece of mathematics this needs — a steady state, a threshold at an
eigenvalue crossing, and a selection coefficient from last Thursday.

What the opening must NOT do: open on HIV biology, or on gene drives.

---

## 1 · Where this sits

Sessions 19–23 were one ladder, each rung a context that breaks a circuit.
Session 23 broke the ladder, because selection is not a disturbance you can
reject, and closed on a finding: the levers that worked in Rottinghaus were
**intra-niche competition and a host-genome edit**, neither of them circuit
design. (Use the sources' wording: `s23-evolution/DESIGN.md` says Δrpdu and
ps09-PLAN says "a host-genome edit".)

`private/sources/ps09-PLAN.md` §1, quoted exactly:

| session | what the population does |
|---|---|
| 23 | removes the circuit — selection is the adversary |
| 24 | controls the circuit — another strain holds its life |
| 25 | **carries the circuit — the genome is split across cells** |
| 26 | is the thing being classified |

**Session 23 asked how long a circuit survives a population. Session 25 asks
what it takes for one to invade.** Same algebra, opposite sign on the design
goal.

---

## 2 · The room has never seen a virus

From the census in `s24-communities/PRIOR-YEARS.md` §4, re-run independently
during review. **Zero occurrences on any slide, body line or speaker note
across all 22 built decks:** virus · virion · capsid · encapsidation · diploid
· heterozygous · homozygous · helper virus · defective interfering · DIP · TIP
· interfering particle · R₀ · basic reproductive ratio · transcritical ·
invasion · epidemic · SIR · co-infection · superinfection · allele · homing ·
super-Mendelian · minimal gene set.

Four terms look non-zero; three are false positives (`gene drive` = "one gene
driven by", `tip` = "tip of my tongue" and "tip the balance", `package` = a
Python package — note `packaging` itself is zero). **`burst size` is not a false
positive**: two real hits in session 12, with a different object, which is the
collision disarmed below.

The mathematics, by contrast, is everywhere: steady states, cooperativity,
fixed points, nullclines, Jacobians, eigenvalues and bifurcations all run to
tens of slide-facing hits each. **This session has no mathematics problem. It
has an object problem.** (Counts are not quoted here because two independent
runs disagreed on four of seven terms; `tools/census.py` derives them, and the
zero list above is the part both runs agreed on.)

**Drawn before anything is modelled:**

| object | where it is drawn | why it cannot be words |
|---|---|---|
| a virion with two RNA strands in one capsid | **segment 1 FRAME** | the whole binomial follows from this picture |
| a dually infected cell with a 1 : P cytoplasmic pool | **segment 1 FRAME** | this is the urn the binomial draws from |
| the vector beside the full genome | **segment 1 FRAME** | makes "what you can delete" visible |
| cis versus trans — what the vector keeps, what the helper supplies | **segment 1 BUILD** | the root of move 4's paradox: the vector is an obligate parasite of what it suppresses |
| **a diploid locus carrying two alleles** | **segment 1 FRAME** | drawn with the other objects, before any of the mathematics, because move 5 reads super-Mendelian inheritance straight off it. Of the five it is the object the room has least chance of having met: `allele`, `diploid`, `heterozygous` and `homozygous` are all zero across the 22 built decks |

**Two collisions to disarm out loud.** Session 12's *burst size* is a
translational burst, geometric with mean k_p/γ_m; here n = 200 is virions per
cell. And session 23's selection coefficient is a burden the designer wants to
cut, while a gene drive's fitness cost is one the designer imposes and the
drive wins anyway — same symbol, opposite intent, seven days apart. **Both are
disarmed where the colliding object appears** rather than in the opener: s12's
in segment 4's frame, where n = 200 arrives, and s23's in segment 5's frame,
where the drive's fitness cost arrives. §5 open says why.

**Two more collisions are RENAMED, not disarmed — `docs/symbols.md` is the
authority.** A disarming line tells the room a collision exists; it does not
remove it, and `deck-bar.md` §B1 counts a symbol settled only in a foot or a
speaker note as unsettled. So, added 8 November 2026:

- **Noble's homing efficiency, which he also prints P, is `h` here.** This
  hour's P is the packaging advantage, autograded in T67 and T73 and on the
  final; the gene-drive material is T75, assessed by the home guide and the
  final and hand-graded, so the cheaper side moves. The invasion condition is
  **f(1 + h) > 1** and the boundary **f > 1/(1+h)**.
- **Noble's allele names W, D and R stay his, but never as bare letters.**
  They are printed on his crops, so renaming them would make our slide
  contradict the figure beside it. Instead every allele is written as a
  **genotype** (WW, WD, DD, DR) or inside a **noun phrase** ("the W gamete",
  "the resistant allele"): a genotype pair cannot be read as a scalar, which
  is the only way a bare **D** collides with the antiviral effect.
- **The bridge, and it is required.** The crops still carry Noble's own axis
  label P, and published figures are not relabelled — so the slide carrying
  the first crop says once, **in body type**, that his P is our h. That is a
  bridge between our notation and a figure in front of the room, not a
  disambiguation of two live meanings. `s25_locus_1` / `s25_locus_2` (a two-stage series split 8 Nov so the FRAME shows the locus and the BUILD shows the gametes), which is ours,
  prints h and carries the same line in its own footer.

**Cheapest new term:** *transcritical*. Fixed points, eigenvalues and
bifurcations are all in hand; only the name is new.

---

## 3 · The five moves

### Move 1 — What you are allowed to delete

FRAME with the objects above. Then the ledger. **This is no longer T68** —
minimal gene set reasoning moved to session 28 on 7 November — but the ledger
stays, because move 4's paradox rests on it:

| | keeps (cis) | the helper supplies (trans) |
|---|---|---|
| crHIV-1 vector | the cis elements needed for packaging, plus the antiviral cargo gene and an HIV-1-induced promoter | every trans element — W03 names the Gag-Pol polyprotein that is cleaved into the HIV-1 capsid |
| a DI particle | part of the viral genome, in normal viral structural protein | helper virus, which is HB70's third defining property: "they can reproduce in the presence of helper virus" |
| a split CRISPR drive | the gRNA cassette and the homology arms | Cas9, from the host genome or from a separate construct |

**Huang & Baltimore's outcome III belongs here.** Their Fig. 1 outcome III is a
cell entered only by DI particles, producing no yield. That is **obligate
trans-dependence drawn in 1970** — the premise that makes a reproductive ratio
well defined at all. It is not R₀ᵀ < 1, and the slide says which is which: R₀ᵀ
counts vector infections from a cell in a patient *at HIV steady state*, with
helper present, while outcome III is the no-helper case.

**Why the assessed technique left for session 28.** No paper
assigned here measures a minimal genome size. W03's 10 kb against ~4 kb appears
in the *recombination* paragraph, as why reverse transcriptase cannot finish a
heterozygous template — it is not a packaging-capacity result. The ledger above
is handed to the room rather than derived, and a handed-over table is not a
demonstration of a technique. So the ledger is taught here as the premise it
is, and the assessed technique moved to **session 28**, where "how little does
a cell need" has a paper behind it.

### Move 2 — Two draws from an urn

**Session 2 owes this room a calculation.** On a slide students saw: a plasmid
at 5 copies splits binomially, P(one daughter gets none) = 2·(½)⁵ ≈ 6%, with
the forward reference to sessions 12 and 25; and the speaker note says session
25 does the full binomial for a genome. `binomial` has exactly two occurrences
in the course and both are that promise. **Move 2 pays it and says so.**

| | session 2's plasmid | session 25's capsid |
|---|---|---|
| draws | n = 5 copies into a daughter | n = 2 strands into a capsid |
| p | ½ — fixed by physics | **P/(1+P) — set by the engineer** |
| the question | **loss**: does a daughter get none? | **composition**: which genotype is this virion? |

BUILD, one genuine move per slide, with `derivation_fig` advancing beside the
symbols:

1. **The assumption, stated before the algebra.** W03: all RNA pairs have an
   equal chance of being packaged. **A binomial requires equal packaging and
   independent draws, and nothing in the paper tests either.** The binomial is
   not written down until what licenses it has been said out loud. This is also
   a Limits row and a fair distractor for T67.
2. q = P/(1+P) is the probability a drawn transcript is vector.
3. The three outcomes, each shown rather than asserted: (1−q)², 2q(1−q), q².
4. **Shown to sum to one**, not asserted.
5. In P: 1/(1+P)², 2P/(1+P)², P²/(1+P)². W03 prints 1 : 2P : P², the same thing
   with the denominator dropped. **A slide must say which form it is using**;
   they differ by (1+P)² and that is how this calculation is got wrong.
6. **The derivative gets its own slide**: d/dP of 2P/(1+P)² is (2−2P)/(1+P)³,
   zero at P = 1. It is shown rather than asserted, and it does not ride in a
   parenthesis beside the result it produces.
7. The maximum: **at P = 1 the heterozygote fraction is exactly one half.**

Then the strike-out, stated at the strength the source supports. **An et al.
report a *partial* preintegration, postfusion block and near-zero heterozygous
integration *in vitro*. W03 rounds that to zero**, and the infectious ratio
becomes 1 : P². The absolute is W03's rounding and not An et al.'s result, so
the slide attributes each to the paper that made it. The rounding is the
modelling decision, and it is what the slide teaches — not only the conclusion
it licenses.

RELEASE — a different object from the worked one: a DI particle with no
packaging advantage at all (P = 1) in a cell co-infected at 1:1. What fraction
of released particles can infect anything? DEBRIEF on that object immediately.

**This is T67.** The item states whether it wants the normalized probabilities
or W03's unnormalized ratio. Reference values in `NUMBERS.md` §4b.

### Move 3 — Whose reproductive ratio

FRAME: R₀ has zero prior occurrences in this course, so define it as a count
before any algebra — the number of new infections from one infected cell when
almost every cell is uninfected. Then `weinberger2003_fig2c`, for what an I_T
cell is clinically: uninfected T drops into the AIDS regime below 200/µl while
T + I_T climbs to about 1,500, so the patient's CD4 count is restored by
converting cells into a new class rather than by protecting the old one. That is
why R₀ᵀ's index case has to be an I_T cell. The panel's pretherapy infected level
reads ≈ 58 cells/µl against Table 1's I\* = 21.43, unresolved, so those two
numbers do not share a slide without the note in `NUMBERS.md` §5d.

BUILD. **The derivation gets its own slide, because it is the step that decides
d against δ**, and it runs one move per slide rather than arriving in one line:

    one infected cell lives 1/δ  →  emits n·δ·(1/δ) = n virions
    each virion lives 1/c        →  infects at rate k·T, with T = lambda/d
    so  R0 = n · k · (lambda/d) / c = lambda·k·n / (c·d)

Equivalently the two steady states are T = λ/d virus-free and T* = c/(kn)
infected, and R₀ is their ratio. **Now** show the printed form, λkn/cδ, and ask
the room for the number. With δ it is **0.055** — a virus that cannot sustain
an infection, in a patient who demonstrably has one. With d it is **1.9375**.

**Why that is evidence, stated at the right strength.** The derivation above is
the argument: the virus-free steady state of equation [1] *is* λ/d, so d is
what belongs there. The threshold then reproduces the paper's own prose —
1 − 1/R₀ = 0.4839, persistence needs P²D > 2.0667, and at D = 0.2 that is
P > 3.21 against a text that says coexistence appears as P passes about 3.
λ/d = 1550 against Fig. 2c's inset is a **consistency check and not evidence**,
because λ/d contains no c, δ, k or n and cannot discriminate between the two
denominators. It goes on the slide labelled as the check it is.

**Then where the parameters came from.** λ and k are not measurements. W03 says
in one line that both were obtained by steady-state analysis. The back-solve is
exact, and it gets a step run of its own, one move per slide, because the first
step is a unit conversion that decides every number after it: every
concentration in Table 1 is per µl except V₀, which is printed per ml.

    V0 = 1e5 virions/ml  =  1e5 / 1e3  =  100 virions/ul
    I* = c*V0/(n*delta)  =  30*100/(200*0.7)  =  21.43 cells/ul
    k  = c/(n*T0)        =  30/(200*800)      =  1.875e-4  ul/virion, as Table 1 prints it
    lambda = d*T0 + delta*I*  =  0.02*800 + 0.7*21.43  =  16 + 15  =  31.0

**Leave the conversion out and I\* comes back a thousandfold wrong** — 21,430
cells/µl of infected cells in a patient whose total T₀ is 800. So the conversion
is a line of the derivation and not an aside beside it.

So **R₀ = (λ/d)/T₀ = 1550/800 = 1.9375 is true by construction** — a correct
number and a restatement of two inputs at once. Table 1 gives λ a literature
citation and marks k "no data", which is how that half-hides.

**Then R₀ᵀ, derived rather than cited.** W03 puts its derivation in a
supplementary file behind a dead URL. It has since been re-derived here from
equations 4–6 by next-generation matrix, and **the published form is exactly
right, with no added assumption** — `NUMBERS.md` §18, three independent
verifications. So move 3 teaches the derivation, which is what §5b asks for and
what a dead URL could not deliver.

**Start with which equilibrium, because the answer is this move's title.**
Linearise at the **HIV-endemic, therapy-free** steady state and not the
virus-free one. At V\* = 0 an I_T cell can never be superinfected, I_D is never
populated, and **R₀ᵀ ≡ 0 for every P and every D** — degenerate, not merely
different. The vector is an obligate parasite of an established infection, and
that is the *reason* the index case is an I_T cell rather than a stipulation
about it. Equation [1] fixes where we stand: T\* = 800 cells/µl,
V\* = 100 virions/µl, I\* = 21.43 cells/µl.

Then R₀ᵀ is a product of three factors, one move per slide, and **two exact
cancellations do all the work**:

    k*V*/(d + k*V*)  =  1 - 1/R0      an I_T cell is superinfected before it dies
    P^2 * D * n                       vector virions out of that I_D cell
    k*T*/c           =  1/n           new I_T cells per vector virion

    so  R0_T  =  P^2 * D * (1 - 1/R0)

- **kT\*/c = 1/n exactly**, because T\* = c/(kn). The burst size cancels
  against the steady state it sets, so **R₀ᵀ contains no n at all** — the
  threshold does not contain the burst size, which is the quantity move 4 then
  makes the whole problem.
- **kV\*/(d + kV\*) = 1 − dT\*/λ = 1 − 1/R₀**, from kV\*T\* = λ − dT\* in
  equation [1].
- **δ′ never appears.** It cancels between production P²Dnδ′ and the I_D
  lifetime 1/δ′ — checked over δ′ from 0.001 to 50, where the threshold stays
  31/15. That is the algebra behind W03's own word for its δ′ assumptions,
  "benign", and it can be stated now instead of quoted.

**And one thing said out loud while the matrix is on the slide.** Count virion
*production* as a new infection too — which is the textbook recipe, and what a
student who has met next-generation matrices will reach for — and the spectral
radius comes out as √(P²D(1 − 1/R₀)) instead. **The threshold at 1 is the same
number either way**, so nothing in the hour moves; the *magnitude* of R₀ᵀ does.
Say it here, because a student who builds it that way is right and should not
find that out from a mark. `NUMBERS.md` §18.4.

**The line that gets a slide of its own:** *1 − 1/R₀ is not a correction factor.
It is the probability that an I_T cell ever meets the wild-type virus it needs
in order to replicate at all.* That answers the move's title. R₀ᵀ is not
"R₀ of the vector" — it is indexed on a cell that is waiting.

**And the threshold in clinical observables, with no fitted parameter in it.**
Substitute W03's own back-solve, k = c/(nT₀) and λ = dT₀ + cV₀/n:

    R0             = 1 + c*V0/(n*d*T0) = 1 + 3000/3200 = 1.9375 = 31/16
    threshold P^2D = 1 + n*d*T0/(c*V0) = 1 + 3200/3000 = 2.0667 = 31/15

Four clinical numbers and the burst size. V₀ enters as 100 virions/µl, which is
the unit conversion from the back-solve doing its work a second time.

**The index case goes on the slide.** R₀ counts infections from an *infected*
cell. R₀ᵀ counts them from an **I_T cell — one already carrying the vector,
waiting for the virus**. The therapy's susceptible pool is cells that already
have the vector and nothing to replicate it.

**The design result, stated so that it agrees with the autograder.** Over any
established infection 1 − 1/R₀ runs from about 0.47 to 0.95, so

    R0_T  is PROPORTIONAL to  P^2·D,  with a coefficient between 0.47 and 0.95

and the persistence threshold therefore sits **between P²D ≈ 1.05 and
P²D ≈ 2.11** across that range — **at this patient's R₀ it is 2.0667, exactly
31/15**, which is the number every item and every figure uses. **It is a
statement about the construct, not about the patient.**

> **No slide says R₀ᵀ ≈ P²D.** The coefficient is about one half, and dropping
> it is not a rounding. A student who takes P²D > 1 as the threshold solves it
> and gets **P > 2.236** at D = 0.2 where this session pins 3.21 — the two
> differ by exactly √2.0667 = 1.4376 — while the figure draws the 2.0667
> contour and the autograder marks against it. T73 is autograded on PS9 and on
> the final, so the slide and the autograder have to carry the same number.

RELEASE — a different object: given a construct measured at P = 8, what D does
it need to persist? DEBRIEF immediately, on that construct. **This is T73**, and
the release is `D_min(P, R0)` — `P_min` run backwards, which is the direction the
question is asked in. At P = 8 and R₀ = 1.9375 the answer is
D > 2.0667/64 = 0.0323, so the cargo may suppress HIV-1 production by at most
about 96.8% and still leave the vector able to spread.

**The debrief puts `weinberger2003_fig3` beside our design-space figure**, with
their stability floor read off and replotted in 2-D. The red wedge at low P is
the R₀ᵀ < 1 region, so the threshold is a *curve* in (P, D) and not a point.
Whether their boundary and our P²D = 2.0667 contour are the same line is
`[unverified]`, and the room finds out in front of the figure.

**Pin for every item: c = 30 and R₀ = 1.9375.** Table 1's footnote offers c = 3,
which gives R₀ = 19.375 but also T* = 80, contradicting T₀ = 800.

### Move 4 — Your payload is the vector's own fitness

The claim holds here and nowhere else in the hour. Move 5 is where it comes
apart.

FRAME on `weinberger2003_fig1`: the two arrows that share a D, before any
algebra. Then a question before the answer — which end of the D axis is the good
drug? D = 1 is no inhibition, the reverse of the paper's own prose definition,
and `NUMBERS.md` §3 asks for that settled out loud before anything is computed
with D. **The SENSE is settled earlier than this, and has to be** — segment 3's
"Linearise at the infection" slide names both knobs in body type at D's first
slide-facing use, and `s25_design_space`'s two axes carry "D = 1 is no
inhibition" where the room first reads D off an axis (`deck-bar.md` F5: the
measurement comes before the statistic). What this frame adds is the catch that
the paper's own PROSE says the opposite, which is a thing to find in a paper
rather than be told. **Session 12's burst size is disarmed here**, where n = 200 first
appears: s12's was a translational burst, geometric with mean k_p/γ_m, and this
one is virions per cell.

BUILD. **D appears in equation [6] — the vector's own production — as well as
in [3].** The vector is an obligate parasite of the Gag-Pol it suppresses, so
R₀ᵀ → 0 as D → 0. No cargo gene inhibits the virus without equally inhibiting
the vector, because they share one production term; meanwhile singly infected
cells never see the inhibition and rebound the set point. The authors' phrase
is crHIV-1 **"shooting itself in the molecular foot"**. Fig. 2a is non-monotone
in D; Fig. 2b is monotone in P. **Two knobs, two shapes.**

**So D has an optimum, not a maximum.**

**Which D: the session uses 0.4 and says on the slide that the text says 0.2.**
Fig. 3b's caption puts the HAART-comparable point at D ≈ 0.4. The text (journal
10033) puts the optimum at ≈ 0.2. Fig. 2a's caption gives neither — it says
oscillations arise at D = 0.1 while the panel's own legend labels the
oscillating trace D = 0.2, which is a second mismatch rather than a second vote.
So: **a figure caption against a sentence of text**, and the panel behind the
caption, where the set point falls as D drops to about 0.4. The session uses 0.4
and names the mismatch where the number is used, with the paper's other internal
mismatches collected on the Limits slide. `NUMBERS.md` §5c.

**Then the assumption itself.** The binomial fixes which
genotype a virion is. It does not fix how many there are, and W03 does not
partition a fixed burst — it multiplies. One dually infected cell releases
D·n virus, P²·D·n vector and 2P·D·n heterozygotes: **(1+P)²·D·n in total.**

| P | D | total from one cell |
|---|---|---|
| 10 | 0.4 | 9,680 |
| 30 | 0.4 | 76,880 |
| **100** | **0.4** | **816,080** |

Against the burst sizes W03 itself cites: **200** in vivo (Haase), three to five
times that under CD8 depletion, and **40,000** for *env*-deleted SIV, which W03
attributes to unpublished data. **The headline design point needs about 4,080
times the measured burst and 20 times the most extreme number the paper can
cite.**

> **How to say this.** W03 does not hide the assumption. It states it in three
> places, and each now has a page (`NUMBERS.md` §17a). **Journal 10029**, in the
> introduction's summary of results: that the burst size of therapy-producing
> cells must exceed that of HIV-1-infected cells, that packaging resources are
> taken not to be limiting, and that the study "highlights the need to determine
> both the maximum possible viral output from HIV-1-infected cells and the
> potential of Gag-Pol to act as a limiting intracellular resource in vivo".
> **Journal 10031**, in the Theory section, in the same paragraph that supplies
> 200, "3 to 5 times more", and 40,000. **Journal 10035**, in the discussion:
> "our model assumes that the I_D cell burst size is greater than n". **So the
> claim the slide makes is the narrow one: the paper never says how much greater
> than n, and never sets its own ceiling of 40,000 against the 816,080 its
> equations demand.** The abstract and the Fig. 3b caption carry none of it.
> (W03 has no Materials and Methods section. Its two body headings are Theory
> and Results and Discussion.)

**And the limiting case.** Suppose packaging *is* capped — the cell makes n
particles whatever happens. Then the vector's output is n·P²/(1+P)², which at
P = 100 is 196 of 200 particles, with about 4 heterozygotes and **one virus
particle per 51 dually infected cells**. In that model **D does not appear in
the vector's output at all**, so R₀ᵀ loses its D, the shared-production-term
argument collapses, and move 4's own title is false. Both models are in
`posb/populations.py`, and a test asserts that `burst_output(..., fixed=True)`
gives a vector output that does not move when D does.

**And the limiting case now has a number.** Run the same next-generation
construction on the capped model:

    R0_T_fixed  =  [P^2/(1+P)^2] * D * (1 - 1/R0)  <  15/31  =  0.4839

**below one for every P and every D — under a capped burst the therapy can never
invade at all.** The bound does not turn on how the cap is written: apply the
inhibition before the cap and D survives in the expression, let the cell make n
particles whatever happens and D drops out, but P²/(1+P)² < 1 and D ≤ 1, so the
supremum is 1 − 1/R₀ = 15/31 either way. Confirmed on the Jacobian out to
P = 10⁶. `NUMBERS.md` §18.6. **So the burst-size assumption is not bookkeeping.
It is the difference between a therapy that invades and one that cannot**, and
that is the whole of move 4 in one inequality.

**Where the evidence sits.** The one direct measurement points at the capped
model: W03 itself cites in vitro work (ref 8, Bukovsky 1999) finding that
encapsidation resources in a dually infected cell *are* limited. W03 argues past
it with a mechanism rather than a measurement — that immune killing ends the cell
before it reaches its ceiling — and then names the two measurements that would
decide it, the maximum viral output of an infected cell and whether Gag-Pol is a
limited resource in vivo. Neither has been made. `NUMBERS.md` §17b. W03 flags a
neighbouring problem in its own voice: if the cargo acts on full-length
cytoplasmic mRNA rather than on virion production, D and P stop being
independent and each class of antiviral gene needs a different model. That is
what "in this architecture" means.

**Then the twenty-one-year arc.** The question this
move used to hand the room — does the paradox survive in a TIP somebody built? —
is answered, and the answer is no. Nagoor Pitchai et al. 2024 engineered a
replicating TIP whose interference *is* competition for the viral Gag
polyprotein precursor rather than suppression of its production, and tied the
interference to packaging by deleting the packaging signal Ψ, which blunted the
effect by about 30%. With nothing suppressing production there is no D in the
vector's own production term, the two knobs collapse to one, and **the optimum
becomes a maximum.** 2003 writes down a threshold in two knobs and finds that
one of them has an optimum, because the vector parasitizes what it suppresses;
2024 builds a working vector by designing that knob out. The
paradox was a property of the architecture, and the architecture changed.
`NUMBERS.md` §16. **The reading of Pitchai against W03's D is ours and the slide
says so**: the 2024 paper never frames itself against it. W03's own
introduction leaves the door open — competition for packaging resources "is not
ruled out and is the focus of ongoing research" (§17c).

**The 1970 oscillation closes the build.** Huang & Baltimore's Table 1, CHO
column: the standard-virus titre falls to 0.0058% of passage 1 by passage 3,
then rebounds **768-fold** at passage 4, while the MDBK column never drops below
21%. Beside it, Fig. 2a's oscillating trace at D = 0.2. The oscillation belongs
to the host cell rather than to the virus, and what W03 finds as a Hopf in a
(P, D) plane was measured thirty-three years earlier. Nothing in the session is
assessed on this slide, which is why §6 cuts it first.

RELEASE — a different object: a DI particle of influenza, where the genome is
segmented and the packaging cap is physical. Does the paradox apply? DEBRIEF
immediately.

### Move 5 — The same arithmetic in a population that was not asked

Declare the change of question on its own slide. Everything so far has been one
patient.

FRAME on the diploid locus drawn in segment 1, now with three alleles: wild
type, drive, resistant. **`h` is defined on this slide**, in body type, as the
homing efficiency — the chance a cut in a WD germline is repaired into a drive
copy rather than into a resistant allele — because the plate prints it (§2).
**Session 23's selection coefficient is disarmed here**:
there it was a burden the designer wants to cut, here a fitness cost the
designer imposes and the drive wins anyway — same symbol, opposite intent, seven
days apart.

BUILD, **two slides since 8 November.** The first carries the mechanism with
`s25_locus_2` beside it: the drive invariably cuts the wild-type allele in a WD
germline, so a drive heterozygote transmits no wild type at all, and the drive
is in more than half the gametes for any h above zero. That is super-Mendelian
inheritance, and the payoff of the locus drawn in move 1. The second carries the
caveat and is titled with it: **the table only looks like that because every cut
happens** — the empirical homing efficiencies in Noble's own appendix run from
14% to 100% and real constructs do leave wild type behind.

*Why two.* Not a style rule — a measurement. The plate is width-bound and
renders 2.97 in tall at any band that keeps its type above the floor, the body
leaves 2.17 in, and the four rows this BUILD used to carry need 4.33 in. The
condition still travels with its result (bar F3): "the drive INVARIABLY cuts"
is a row on the first slide, immediately above the claim it licenses; what
moved one click is the condition's *empirical status*, under a title that
names it.

Their results, each with the parameter that produces it on the slide beside it:

- **Resistance prevents fixation, not invasion.** Every published construct
  sits inside the invading region (`noble2018_fig1b`). The 14% female line is
  *not* an exception that fails to invade: the condition is f > 1/(1+h), which
  at h = 0.14 is f > 0.87719 — printed f > 0.877 — and Noble's own f = 0.9
  clears it by 0.0228, i.e. 2.3 points. The window is narrow, not absent.
  **This slide carries the bridge** (§2): Noble's axis says P, we write h, and
  the slide says so in body type. Re-verified against `NUMBERS.md` §6a on
  8 November 2026.
- **Release size.** At homing efficiency **0.9**, median peak drive goes from
  about 0.005 to about 0.90 between one and two organisms released; at **0.5**,
  Noble's conservative default and the value behind every deme simulation, two
  organisms reach about 0.29. Ten organisms nearly guarantee invasion. Each
  figure carries its homing efficiency on the slide, because the three columns
  differ by two orders of magnitude at a release of two.
- **Containment is a property of gene flow.** Five demes of a hundred with one
  migration event per two generations, and escape is effectively certain **for
  moderate drive efficiencies**.
- The altered majority often carries **drive-created** resistant alleles — the
  drive's own exhaust, itself an engineered sequence.

**And this is where the title earns itself.** Noble's deterministic invasion
condition makes the drive's spread depend on the homing bias *and* the fitness
cost as **two separate quantities**. In W03 they were one. So the specification
is the same — a reproductive ratio greater than one — and what trades against
what is not. A student who leaves with only move 4's lesson has learned a fact
about lentiviral vectors and mistaken it for a principle.

RELEASE — a different object: a drive with a *beneficial* cargo. DEBRIEF.

**This move is T75**, added to the coverage matrix on 7 November, and assessed
by **this session's home guide and the final** rather than PS9 — the pattern
locked decision 20 set for sessions 27–28. The guide therefore carries worked,
final-shaped gene-drive items with their answers, which is what makes this
material assessed rather than merely lectured.

**Close.** W03 names its own largest risk in one sentence: that the vector could
be transmitted between individuals. Noble is that sentence with the arithmetic
done. Hand off to session 28 — **and assign the session 26 reading, Xie et al.,
*Science* 2011**, which AGENTS.md requires at the close of the previous class.

---

## 4 · The design ledger

`docs/lecture-design.md` §5d: every session closes by saying, in the session's
own quantities, what a designer controls and what they do not. Three columns,
written last.

| | |
|---|---|
| **Knobs** | **P** — the packaging advantage: the cytoplasmic crHIV-1 : HIV-1 mRNA ratio in a dually infected cell, 1 : P by definition. W03 names three routes that move it, on journal 10034 — removing the vector's splice signals, a constitutive transport element for Rev-independent export, and a WPRE to raise mRNA half-life, "up to 10-fold in vitro" — and one it expects to fail, improving the packaging signal Ψ itself, because HIV-1's regulatory domains "are believed to be optimally evolved". **P is intracellular, and W03 says plainly that it is not the one you can measure.** **D** — the antiviral payload, set by choice of cargo gene, and the knob that *is* measurable: quantify the HIV-1 titre in the supernatant of cell cultures with and without the vector. **D's sense reads backwards from its own prose definition** — in the equations D is the fraction of HIV-1 production that REMAINS, so D = 1 is no inhibition and D = 0 is total inhibition. |
| **Constraints** | **R₀** of the patient's own infection, which you do not set. **Diploidy** — two draws, not three, and not one. The heterozygote block, which is the chassis' property. **n** = 200, the burst size; **c** = 30 day⁻¹, the virion clearance *rate*; **δ** = 0.7 day⁻¹, the infected cell's *death rate* — so the lifetimes are the reciprocals, 1/δ = 1.43 days for an infected cell and 1/c = 0.033 days for a virion. **λ** and **d**, which are the host's. |
| **Limits** | Eight of them, each with the observable that tells you you have left it — the table below. |

**The Limits column is the one that must not be skipped**, and for this session
it is nearly the whole lesson.

**The Limits column in full**, because §5d requires every limit to name the
observable that tells you when you have left it, and a limit without one is a
disclaimer rather than a limit.

| the limit | the observable that tells you you have left it |
|---|---|
| **The burst-size assumption.** Output is taken to scale as (1+P)²·D·n, so total release grows without bound in P, and the headline design point needs about 4,080 × n | The measured burst size of a dually infected cell. W03's own two open questions are exactly this measurement — the maximum viral output of an infected cell, and whether Gag-Pol is a limited intracellular resource in vivo. Against 200 in vivo and 40,000 for *env*-deleted SIV, 816,080 says the limit was left some way back. `NUMBERS.md` §4c, §17 |
| **Equal packaging and independent draws**, which the binomial requires and which nothing in the reading set tests | The genotype composition of released virions at a known cytoplasmic ratio. If heterozygotes are not 2P/(1+P)² of the output — half of everything at P = 1 — then the two draws are not independent, or the pairs are not equally packageable. No paper in the reading set measures it. `NUMBERS.md` §10 |
| **D sits in one shared production term.** The move-4 result holds in this architecture: not in a drive, and not in a TIP that competes for Gag instead of suppressing it | Whether the interference travels with the packaging signal. Delete Ψ: competition for Gag is blunted by it — Nagoor Pitchai 2024 measured about 30% — while suppression of production would survive it untouched. `NUMBERS.md` §16 |
| **δ′ = D·δ.** A dually infected cell's *death rate* is made a function of a knob: at D = 0.4 an I_D cell's lifetime is 1/(Dδ) = 3.6 days against an I cell's 1.43, and at D = 0.01 it is 143 days. An assumption carrying W03's own `††` footnote. **It is not a limit on R₀ᵀ**, which contains no δ′ at all — it cancels between production P²Dnδ′ and lifetime 1/δ′ | So the threshold does not move: checked over δ′ from 0.001 to 50, where it stays 31/15. What δ′ sets is the I_D population and the length of the transient, so the observable is the measured death rate of dually infected cells across cargoes of different potency — and what it would falsify is the set-point trajectory, not the threshold. If I_D cells do not live measurably longer as the cargo gets stronger, δ′ = Dδ is wrong. `NUMBERS.md` §18.2 |
| **The An et al. rounding to zero.** Heterozygotes are struck out of the infectious output on one in vitro paper and one two-page committee review. Were they infectious the ratio would be 1 : P(P+2) rather than 1 : P², changing R₀ᵀ by (P+2)/P — 2% at P = 100, but a **factor of 3 at P = 1**, largest exactly where the threshold sits | Whether heterozygous virions establish an integrated provirus in the vector and helper pair you built, in primary cells rather than a line. P_min is 1.44 at D = 1, 2.27 at D = 0.4 and 3.21 at D = 0.2, where the correction is 2.4×, 1.9× and 1.6×; by D = 0.01 P_min is 14.4 and the correction is 1.14×. So the assumption decides constructs designed close to persistence at a workable D, and barely touches the rest. `NUMBERS.md` §4d, §12.6 |
| **No virion loss on infection.** Equation [6] carries no −kV_T·T term, inherited from the Basic Model, and the R₀ᵀ derivation turns on it: restore it and kT\*/c becomes kT\*/(c + kT\*), the exact 1/n cancellation breaks, and R₀ᵀ picks up a factor 1/(1 + 1/n). W03 calls the effect "minimal"; at n = 200 it is **0.5%**, now quantified | Whether free vector is measurably depleted by binding to target cells — that is, whether c is the whole of the vector's loss rate. The neglected eclipse phase sits in the same place: a delay between infection and production adds a survival factor to each generation and *lowers* R₀ᵀ, without touching the P²D product structure, and it is still `[unverified]` because the altered equations are in the SI. `NUMBERS.md` §18.3, §18.8 |
| **No superinfection of I_D cells** | Whether CD4 stays off the surface of a dually infected cell, and whether HIV-1 can re-enter one. W03's reason is that HIV-1 Nef downregulates CD4 — and an I_T cell carries no Nef, which is why HIV-1 *can* still enter one. If an I_D cell can be superinfected, equation [5] is missing a loss term. `NUMBERS.md` §1 |
| **One patient, not a population.** Move 5 is the change of question | Vector sequence recovered from somebody who was never dosed. W03 names inter-individual transmission as the approach's largest risk, in its own words, and move 5 is that sentence with the arithmetic done. `NUMBERS.md` §13 |

**Why the close runs to two slides.** This is a departure from §5d's "a slide, not
a lecture", stated here rather than left silent. Eight limits with their observables will not
meet the type floor `decks/theme.py` enforces for Dwinelle 219 on a single
slide. So: one slide carries the three columns with the Limits column named but
not expanded, and the next carries the eight rows above. If the hour is short,
the three that cannot come off are the burst-size row, the δ′ row and the
An et al. row — the three that change a number an item is marked against.

---

## 5 · Segments

`docs/lecture-design.md` §5e: every teaching segment is **FRAME → BUILD →
RELEASE → DEBRIEF**, and none is optional. RELEASE is on a **different** object
from the worked one; DEBRIEF is immediate and illustrated, on the item's own
object. All five segments below carry all four moves, the segment carrying T73
included.

`docs/lecture-design.md` §5c: there is **one** in-class rhythm — *pose on a
slide, two to four minutes on their own paper, poll the room, discuss.* The
first poll is silent and eyes-down; the distribution gets written down; nothing
is collected. That is the only shape student work takes in this session.

Badges: `open`, `frame`, `segment N`, `close`. No minute badges.

### open
| | |
|---|---|
| retrieval — two from session 24, one from session 2 | **s24 — the D collision.** Session 24's **D** appeared in five places once the signals were written down — what was it, and what did raising it do to the predator? (the dilution rate; predator washout by 0.31 h⁻¹). Today's D is a different quantity and it reads backwards. **s24, elaborative:** you set session 24's two signals to steady state and the Hopf vanished — what had the approximation thrown away? (the lag between a population and its own signal). **s02, the spaced item:** the plasmid binomial and the convention it was stated in, which segment 2 then pays off |
| what you should be able to do by the end | three questions, posed as questions |
| frame · where this sits | the ladder, broken at 23; the unit of design becomes the population |

**Where the other two collisions went.**
`docs/lecture-design.md` §3 and §6 ask for two questions from the previous
session and one from three or four sessions back. The natural retrieval items
for this hour are session 12's *burst size* and session 23's selection
coefficient — the two collisions §2 disarms — and neither is in session 24, so an
opener built around them carries nothing from last session at all. **That
departure is not taken, because session 24 does supply two items**, both above:
its D is this session's D in a different meaning, and its QSSA step is the one
place the room has watched an approximation discard the phenomenon it was
applied to — which is what the whole Limits column of §4 asks about. The s12 and
s23 collisions are disarmed at the point of collision instead — **s12's burst
size in segment 4**, where
n = 200 first appears, and **s23's selection coefficient in segment 5**, where a
drive's fitness cost appears. §2 asks for both to be disarmed out loud; it does
not ask for them in the opener, and a collision lands better beside the object
than five minutes before it.

### segment 1 — what you are allowed to delete
| move | content |
|---|---|
| FRAME | `objects_fig` (§7), which draws all four: the virion, two strands in one capsid. The dually infected cell and its 1 : P pool. **The diploid locus with two alleles**, drawn here and not in segment 5. The vector beside the full genome |
| BUILD | the cis/trans ledger across three systems, with `cistrans_fig` (§7) building it one system per slide. Then `huangbaltimore1970_fig1`, outcome III as the 1970 picture of obligate trans-dependence — a student concludes from that crop that W03's equations 4–6 are this hand-drawn figure written down |
| RELEASE | a different object: a satellite virus that supplies its own coat but not its own polymerase. What must its helper provide, and what can it delete? |
| DEBRIEF | that object, answered on screen immediately |

### segment 2 — two draws from an urn  *(T67)*
| move | content |
|---|---|
| FRAME | session 2's promise, quoted from the slide they saw, and the table of the two binomials side by side |
| BUILD | seven slides, one move each: the equal-packaging assumption stated first; q = P/(1+P); the three outcomes shown; shown to sum to one; the form in P, with W03's unnormalized ratio named; **the derivative on its own slide**; the maximum at P = 1. Then An et al.'s partial block and W03's rounding of it |
| RELEASE | a different object: a DI particle with no packaging advantage (P = 1), co-infected 1:1. What fraction of released particles can infect anything? |
| DEBRIEF | immediately, on that object, with the 1 : 2 : 1 ratio drawn |

### segment 3 — whose reproductive ratio  *(T73)*
| move | content |
|---|---|
| FRAME | R₀ defined as a count, before any algebra. The index case named — and `weinberger2003_fig2c` for what an I_T cell is clinically: uninfected T drops into the AIDS regime below 200/µl while **T + I_T climbs to about 1,500**. A student concludes from that crop that the CD4 count is restored by converting cells into a new class rather than by protecting the old one, which is why R₀ᵀ's index case has to be an I_T cell. Carries `NUMBERS.md` §5d's note: the panel's pretherapy infected level reads ≈ 58 cells/µl against Table 1's I\* = 21.43, unresolved, so those two numbers do not share a slide without it |
| BUILD, first derivation | R₀ on its own slide — one cell lives 1/δ, emits n, each infects at kλ/d, so R₀ = λkn/(cd). **Then** the printed cδ, and the room computes 0.055. Then the back-solve for λ and k, opening on the virions/ml → virions/µl conversion, one move per slide |
| BUILD, second derivation | **R₀ᵀ derived, not cited** (`NUMBERS.md` §18). Which equilibrium and why — at V\* = 0, R₀ᵀ ≡ 0 for every P and D, so the I_T index case is forced rather than stipulated. Then the three factors, one move per slide, with the two exact cancellations marked where they happen: kT\*/c = 1/n, so R₀ᵀ contains no burst size, and kV\*/(d + kV\*) = 1 − 1/R₀. Then δ′ cancelling out entirely. **Then the slide that says what 1 − 1/R₀ is:** the probability that an I_T cell ever meets the virus it needs in order to replicate at all. Then the threshold in four clinical observables, 1 + ndT₀/(cV₀) = 31/15. Then proportional-to-P²D with the coefficient band |
| RELEASE | a different object: a construct measured at P = 8 — what D does it need? `D_min(8, 1.9375)` = 0.0323 |
| DEBRIEF | immediately, that construct, on our design-space figure with the P²D = 2.0667 contour — and **`weinberger2003_fig3` beside it**, their stability floor read off and replotted in 2-D, red wedge against cyan. A student concludes that the threshold is a *curve* in (P, D) and not a point, and that the closed form and their simulated boundary are the same line. Whether they in fact are is `[unverified]`, and if they are not, that is the finding |

### segment 4 — your payload is the vector's own fitness
| move | content |
|---|---|
| FRAME | `weinberger2003_fig1`, and the two arrows that share a D. Then, before telling them, ask which end of the D axis is the good drug: D = 1 is no inhibition, the opposite of the paper's own prose definition. **The sense itself is already settled** — segment 3's equilibrium slide defines both knobs in body type at D's first use, and the design-space axes repeat it — so what this frame catches is the paper's prose contradicting the paper's equations. **Session 12's burst size disarmed here**, where n = 200 first appears — s12's was a translational burst, geometric with mean k_p/γ_m; this one is virions per cell |
| BUILD | D in [6] as well as [3]; R₀ᵀ → 0 as D → 0; the molecular-foot mechanism. `weinberger2003_fig2a` non-monotone against `weinberger2003_fig2b` monotone — two knobs, two shapes. Then (1+P)²Dn, the 816,080, and the burst sizes W03 cites, with its three statements of its own assumption and their journal pages. Then the capped-packaging limit, where D leaves the vector's output and the move's own title becomes false, with the one in vitro measurement that favours it — and its number: the same next-generation construction gives R₀ᵀ < 15/31 under a capped burst, **below one for every P and every D**, so a capped therapy never invades at all (`NUMBERS.md` §18.6). Then the twenty-one-year arc: Nagoor Pitchai 2024's competition-based TIP, the Ψ deletion that blunts interference by about 30%, the optimum becoming a maximum — labelled as our reading. **Last slide of the build, and the only one in the hour that nothing is assessed on:** `huangbaltimore1970_table1`, the CHO column falling to 0.0058% of the starting titre by passage 3 and rebounding **768-fold** at passage 4, beside Fig. 2a's oscillating trace at D = 0.2. A student concludes that the oscillation belongs to the host cell rather than to the virus, and that what W03 finds as a Hopf in a (P, D) plane was measured in 1970. That is the slide §6 cuts first |
| RELEASE | a different object: an influenza DI particle, segmented genome, physical packaging cap. Does the paradox apply? |
| DEBRIEF | immediately |

### segment 5 — the same arithmetic in a population that was not asked
| move | content |
|---|---|
| FRAME | declare the change of question. The diploid locus from segment 1, now with three alleles. **Session 23's selection coefficient disarmed here**: there it was a burden the designer wants to cut, here a fitness cost the designer imposes and the drive wins anyway — same symbol, opposite intent, seven days apart |
| BUILD | the always-cuts idealisation, named as an idealisation against the 14–100% homing efficiencies in their own appendix. Super-Mendelian inheritance, with the gamete probabilities the plate prints — (1+h)/2 drive, (1−h)/2 resistant, no W gamete. **`noble2018_fig1b`**, the invasion boundary with the empirical efficiencies as vertical lines, and **the bridge in body type: his axis says P, we write h** — a student concludes that every published construct sits inside the invading region, and that the 14% female line is not the exception it looks like: f > 1/(1+h) at h = 0.14 is f > 0.877, which Noble's own f = 0.9 clears by 2.3 points, so its window is narrow rather than absent. **`noble2018_fig1f`**, release size, with its homing efficiency on the slide. **`noble2018_fig2d`**, escape probability over migration rate against homing efficiency — a student concludes that containment is a property of gene flow and not of the construct, from a cliff in m near 10⁻³ that is nearly independent of h above about 0.3. Drive-created resistance as the drive's own exhaust |
| RELEASE | a different object: a drive carrying a cargo that is *beneficial* to the organism |
| DEBRIEF | immediately |

### close
| | |
|---|---|
| the design ledger | two slides: the three columns, then the eight limits with their observables — §4 above |
| the sentence the paper ends on | transmission between individuals; Noble as that sentence with the arithmetic done; handoff to session 28 |
| before next class | **assign Xie et al., *Science* 2011 for session 26**, which AGENTS.md requires at the close of the previous class |

**Two polls, written out in full with their options and answers in the notes:**

- **Poll 1, segment 2.** *Ask about total virions only*, which is the version
  with one defensible answer. **What fraction of all virions released from a
  co-infected cell at P = 1 carry TWO copies of the vector?** Options: a
  quarter / a half / three quarters / it depends on the burst size. Answer: a
  quarter — the 1 : 2 : 1 ratio. Three quarters carry *at least one* vector
  strand and half of the *infectious* output is vector, which is why the stem
  has to say "two copies". A stem that asks instead about "vector particles"
  has two defensible answers, and the room argues about the question rather
  than the biology.
- **Poll 2, segment 4.** **P is pinned at 5 on the stem.** You improve the
  cargo so it suppresses virus production tenfold harder: D goes from 0.2 to
  0.02. Options written out, with the arithmetic in the note — at P = 5,
  R₀ᵀ falls from 2.42 to 0.242 and the therapy dies out. With P left unspecified
  both "it still works" and "it dies" are correct, which is why the stem pins
  it.

---

## 6 · Eight things a later pass must not undo

1. **"In this architecture" stays on the paradox** — and as of 7 November it is
   demonstrable rather than a caveat. Nagoor Pitchai et al. 2024 built a working
   TIP whose interference *is* competition for Gag polyprotein rather than
   suppression of it. **The next step is ours, labelled as ours on the slide:**
   with nothing suppressing production there is no D in the vector's production term,
   so the paradox does not arise. `NUMBERS.md` §16.2 marks that INFERRED
   BY US. **Move 4 now ends on it.** The
   capped-packaging limit is where this is earned. A pass that cuts that
   limiting case removes the only place the session distinguishes a result from
   a slogan.
2. **R₀ᵀ is proportional to P²D, not approximately equal to it.** The
   coefficient is about one half at this patient's R₀. A slide saying ≈ P²D
   contradicts the autograded threshold.
3. **R₀ᵀ's index case is an I_T cell.** Not an uninfected cell.
4. **The printed-δ correction is taught, not silently fixed** — and the
   derivation comes *first*, because without it the exercise is numerology.
5. **The paper states its burst-size assumption three times** — journal 10029,
   10031 and 10035, quoted with their pages in `NUMBERS.md` §17a. Any rewrite
   that says the paper hid it is false. What it never does is bound it.
6. **Any item asking for a numerical R₀ᵀ states the generation convention.**
   The threshold at 1 is convention-free, so 31/15 is safe either way — the
   *magnitude* is not. Built by the textbook van den Driessche–Watmough recipe,
   where virion production also counts as a new infection, the spectral radius
   is **√(P²D(1 − 1/R₀))**, and a student who does it that way **is right**.
   T73 is autograded on PS9 and sits on the final. `NUMBERS.md` §18.4.

7. **The symbol renames are renames, not notes** — `h` for Noble's homing
   efficiency, alleles only as genotypes or noun phrases, and the one bridge
   line in **body type** on the slide carrying the first crop. §2 has the
   reasoning and `docs/symbols.md` is the authority. Putting either collision
   back into a slide foot reinstates the defect: a foot renders at caption
   size, which is below the content floor, so it tells the room the collision
   exists without removing it. **Anything written for PS9, the home guide or
   the final has to match the deck.**
8. **The cytoplasmic ratio is never written without naming which species
   comes first.** `posb/populations.py` writes it crHIV-1 : HIV-1 = P : 1;
   the figures and `NUMBERS.md` §3 write HIV-1 : crHIV-1 = 1 : P. Both are
   correct and they are the same ratio in opposite orders — but read either
   one the wrong way round and q becomes 1/(1+P) instead of P/(1+P), which
   inverts every genotype probability in the session. Every slide that prints
   the ratio names the order with it.

**If the hour runs short, cut in this order:** the `huangbaltimore1970_table1`
slide at the end of segment 4's build, which is the only slide in the hour that
nothing is assessed on; then segment 5's deme-escape numbers, keeping
`noble2018_fig1b` and the release-size result; then the second Limits slide down
to its three load-bearing rows, named in §4; then, inside segment 3, the
threshold-in-clinical-observables slide, which is the one slide of that
derivation nothing downstream needs. **Never cut** the two cancellations in
segment 3's second derivation, which are the derivation, nor segment 2's
normalization slide, segment 3's index-case slide with `weinberger2003_fig2c`,
the `weinberger2003_fig3` pairing in segment 3's debrief, or any RELEASE/DEBRIEF
pair. Fig. 2c came off this list when it became the slide that says what an I_T
cell is clinically.

---

## 7 · What the build needs, in order

**`posb/populations.py` — built, with `tests/test_populations.py` passing 120
tests.** The table below is the module's `__all__`, read off the module rather
than carried over from the plan:

| function | returns | notes |
|---|---|---|
| `diploid_packaging(P, normalized=True)` | three genotype probabilities | `normalized=False` gives W03's 1 : 2P : P² |
| `infectious_fraction(P)` | (1 + P²)/(1 + P)² | **not monotone on (0, ∞)** — minimum 0.5 at P = 1 |
| `heterozygote_waste(P)` | 2P/(1 + P)² | maximum 0.5 at P = 1 |
| `burst_output(P, D, n=200, fixed=False)` | virus, heterozygote, vector counts | `fixed=True` partitions n instead of scaling it. **D is absent from all three counts in fixed mode, the vector's included** — that is the session's limiting case, and a test asserts it across a sweep in D |
| `basic_R0(lam, k, n, c, d)` | λkn/(cd) | docstring records the printed cδ and why it is wrong |
| `therapeutic_R0(P, D, R0)` | P²D(1 − 1/R₀) | docstring records the I_T index case, and now the re-derivation: the form is exact, the threshold is 31/15, and the function agrees with the symbolic spectral radius to 3.7e-12 over 16,554 draws |
| `P_min(D, R0)` | √(1/(D(1 − 1/R₀))), the least P that persists at this D | 1.4376 at D = 1, 2.2730 at D = 0.4, 3.2146 at D = 0.2. Refuses D = 0 rather than returning infinity, because the useful answer there is the paradox stated |
| `D_min(P, R0)` | 1/(P²(1 − 1/R₀)), the least D a construct at this P can afford | **this is what segment 3's RELEASE runs on**, since the release asks for D given P. A *lower* bound on D is an *upper* bound on how good the drug may be, which is move 4 in one inequality. Returns a value above 1 when no admissible D persists — for P below 1.4376 at R₀ = 1.9375 |

**`tests/test_populations.py`** — 120 tests, passing. Closed forms against
quadrature and against an independently drawn urn, never against an ODE solver:

- the three probabilities sum to 1 across a decade of P, bounded two-sided
- `heterozygote_waste` maximal at P = 1 and equal to 0.5, by a **fine sweep**,
  because the quantity is non-monotone and a coarse grid straddles the extremum
- `infectious_fraction` monotone increasing **on P ≥ 1**, minimum 0.5 at P = 1,
  tending to 1 — and asserted to *decrease* on (0, 1), because the function is
  not monotone on (0, ∞) and asserting that it is would pass on a grid that
  starts at 1
- `burst_output` totals (1+P)²Dn in scaling mode and exactly n in fixed mode,
  **and the vector's fixed-mode output is asserted independent of D** across a
  sweep in D — the session's own counterexample, executable
- `basic_R0` reproduces 1.9375 from Table 1, and the δ substitution is asserted
  to give the impossible value, so the wrong turn is executable rather than prose
- `therapeutic_R0` crosses 1 at P²D = 2.0667, bracketed two-sided
- the proportionality claim as a **predicate**, swept over R₀ in **[1.9, 20]**:
  assert 0.47 < 1 − 1/R₀ < 0.96 and assert the implied threshold stays in
  [1.04, 2.13]. The lower end of that sweep is load-bearing: over [1.2, 20] the
  threshold reaches 6.0 and the band is false, so the predicate is stated for an
  *established* infection and the sweep starts at R₀ = 1.9
- `D_min` round-trips against `P_min` over a grid, and answers segment 3's
  release: `D_min(8, 1.9375)` = 0.0323, bracketed

**Figures** (`figures/s25_populations.py`), audited by `tools/figure_fit.py` via
`build_figures --verify`, saved inside the 4.60 in band so placement scale stays
1.000, curves tagged rather than legended:

1. `objects_fig` for **segment 1 FRAME** — one plate, four drawings, no algebra
   on it anywhere: a virion with two RNA strands in one capsid; a dually
   infected cell with its cytoplasmic pool drawn at 1 : P; the vector as a short
   bar beside the full genome as a long one; and a diploid locus carrying two
   alleles. §2 requires all four drawn before anything is modelled, and a
   student who missed the hour has to be able to read them, so they are a figure
   rather than a description in a note
2. `cistrans_fig` for **segment 1 BUILD** — the step figure the ledger is built
   on, one system per step: crHIV-1, then a DI particle, then a split CRISPR
   drive. Each is a parasite-genome bar with what it keeps shaded and an arrow
   coming in for what the helper supplies — Gag-Pol into crHIV-1, helper virus
   into the DI particle, Cas9 into the split drive. The last step carries the
   shape all three share: what is read in cis is kept, what acts in trans is
   deleted. Built from `NUMBERS.md` §8's three-column ledger
3. `derivation_fig` for segment 2 — the urn filling as the algebra advances
4. `derivation_fig` for segment 3's **first** derivation — the infection chain
   building as R₀ assembles
5. `derivation_fig` for segment 3's **second** derivation — the R₀ᵀ generation
   chain assembling: an I_T cell waiting, the wild-type virion that
   superinfects it, the I_D cell it becomes, that cell's P²Dn vector virions,
   and the new I_T cells those infect. **The two cancellations are marked on
   the picture where they happen**, kT\*/c = 1/n on the last arrow and
   kV\*/(d + kV\*) = 1 − 1/R₀ on the first, because they are the argument rather
   than steps in it
6. the three genotype probabilities against P, log axis, with the P = 1 maximum
7. the burst ledger: total output against P at fixed D, scaling against capped,
   log y — this carries segment 4
8. the design space: P against D with the P²D = 2.0667 contour, and **the
   marked point is the construct the release and debrief are about** — P = 8
   at `D_min(8, 1.9375)` = 0.0323, labelled in the left panel's own title
   ("P = 8 needs D = 0.0323"). Marking §5b's P = 3.21 at D = 0.2 instead marks
   a *different* construct on the same contour and forces the slide to explain
   the difference in its foot, which is a patch over a wrong mark; that point
   is not drawn at all now. The slide's own text says the contour rather than
   either point, so it stays true either way. **Not an overlay on W03's
   Fig. 3**, which is a perspective-projected surface with its stability map on
   a tilted floor and cannot take a 2-D contour. Read their boundary off the
   floor and replot it in 2-D beside ours. Whether the two agree is
   `[unverified]`, and segment 3's debrief is where it gets checked, in front
   of the room

**Handout, answer sheet, board notes.** The session ships all three and not the
deck alone. The home guide must be built **off the PS9 items**, because T67 and
T73 are both
autograded on a set that posts the same day and an answer sheet is public by
design. The s23 guide was checked during review and collides with nothing here;
the exposure is forward, in the unbuilt s25 guide.

**Two constraints on whoever writes the PS9 and final items.** Both come out of
`NUMBERS.md` §18 and neither is visible from the formula alone.

1. **State the generation convention** on any item asking for a *numerical*
   R₀ᵀ rather than a threshold or a persistence yes/no. The textbook
   next-generation split, which counts virion production as a new infection,
   gives √(P²D(1 − 1/R₀)). The threshold at 1 is the same, so 31/15 is safe;
   the magnitude is not, and a student who uses the textbook recipe is right.
   An item that omits the convention will mark a correct answer wrong (§18.4).
2. **State which pair is held fixed** on any sensitivity item. The threshold's
   dependence on n and c changes *sign* between the two coherent choices:
   holding λ and k fixed, n carries elasticity −16/15 and c carries +16/15;
   holding T₀ and V₀ fixed, the magnitudes become 16/31 and the signs swap.
   λ and k were back-solved from T₀ and V₀, so perturbing n at fixed λ and k is
   not a coherent perturbation of this model. The threshold does not depend on
   δ or δ′ at all, elasticity exactly zero (§18.5).

**Paper figure crops** into `private/paper-figures/`, keys in
`decks/paper_figures.yaml`: `weinberger2003_fig1`, `_fig2a`, `_fig2b`, `_fig2c`,
`_fig3`; `noble2018_fig1b`, `_fig1f`, `_fig2d`; `huangbaltimore1970_fig1`,
`huangbaltimore1970_table1`. **Ten keys, and §5 names every one of them in a
segment row, with what a student concludes from it.** Ten is above the measured
range for this course — §8's counts run 1 to 7 — and the reason is that W03 has
only three figures, so the standing rule puts all three in, and Fig. 2 alone
supplies three panels. Five of the ten are W03, three Noble, two Huang &
Baltimore. The cut order in §6 is what absorbs it. Two cautions from
`NUMBERS.md` §9. W03's Fig. 2 panels are embedded rasters, so `_fig2a`, `_fig2b`
and `_fig2c` want redrawing from the model rather than cropping if they are to
meet the type floor — a crop is the fallback, not the plan. And W03's Fig. 3 is a
perspective-projected surface, so `_fig3` goes up as the source of the boundary
we replot in 2-D, never as a panel a contour is laid over.

**Wire-in:** `figures.s25_populations` into `MODULES` in
`tools/build_figures.py`; `s25_populations` into `DECKS` in
`tools/build_decks.py`.

---

## 8 · What changed from version 1, so it is not reinstated

| | |
|---|---|
| title | was "Your payload is the vector's own fitness", which move 5 contradicts. Now the move-4 title |
| R₀ᵀ ≈ P²D | **conflicted with the autograded threshold.** Now "proportional to, coefficient 0.47–0.95" over R₀ in [1.9, 20], and 0.4839 at this patient's R₀ |
| H&B outcome III | was called "R₀ᵀ < 1 before anyone wrote it down". It is the no-helper case. Moved to segment 1 |
| the burst caveat | was "the abstract carries no such caveat". The paper states it three times. Now "never puts a number on it" |
| An et al. | was given an absolute they did not state. Now a partial block that W03 rounds |
| Noble release size | quoted the 0.9 column with no column header. Now carries its homing efficiency |
| "two thirds thrown away" | exceeds the quantity's maximum of one half |
| "three things wrong with it" | one slip and two honesties |
| paper-figure counts | measured: s22 = 1, s20 = 3, s21 = 5, s23 = 5, s16 = 7, s19 = 7 |
| `infectious_fraction` | is not monotone on (0, ∞) |
| the diploid locus | drawn in segment 1, not segment 5 |
| segment structure | rebuilt as FRAME/BUILD/RELEASE/DEBRIEF; three segments had no student work |
| the design ledger | did not exist |
| the s26 reading | was never assigned |
| "rule 11" etc. | replaced with the rule's text; the repo has no such numbered list |
| the census paragraph | said "five more" and named four; `packaging` is zero, `burst size` is a real hit |

---

## 9 · Decisions for Adam

1. **The title change.** Reasoning in §0. Veto if you disagree.
2. **T68 — settled 7 November. It moves to session 28.** Minimal cells deserve
   real time, and with SpudCell this year there is material for it; session 28
   already asks what limits the field. The cis/trans ledger stays here as move
   4's premise. **Nagoor Pitchai 2024 has since been read and it closes move
   4's open question** — see `NUMBERS.md` §16 and the note in §6 item 1. Move 4
   now ends on the twenty-one-year arc rather than on a shrug, in §3 and in §5
   segment 4. **You have not seen that ending yet** — it is the one piece of new
   teaching content in this pass.
3. **Move 5 — settled 7 November.** T75 added to the matrix, assessed by this
   session's home guide and the final rather than PS9. PS9 drops to ten
   techniques.
4. **D = 0.4 or 0.2.** I chose 0.4: the Fig. 3b caption, and the behaviour of
   Fig. 2a's panel, against one sentence of text. It sets move 4's headline at
   816,080 and ~4,080 ×. At 0.2 those become 408,040 and
   ~2,040 ×, and 0.2 is also the curve that oscillates.
5. **What is ours in move 4's new ending.** `NUMBERS.md` §16's Pitchai material
   closes the question move 4 used to hand the room. The part that is ours rather than theirs is the mapping onto
   W03's D — that a competition-based TIP has no D in its own production term,
   so the optimum becomes a maximum. `NUMBERS.md` §16.2 marks it INFERRED BY US
   and the slide says whose reading it is. Same for the 2003 parenthesis in
   `NUMBERS.md` §17c, where W03 leaves competition for packaging resources open.
   If you would
   rather the move ended on the open question, the capped-packaging limit stands
   either way.
6. **D's sense gets a question to the room in segment 4's FRAME**, before the
   answer: which end of the D axis is the good drug? D = 1 is no inhibition,
   which is the reverse of W03's own prose definition. `NUMBERS.md` §3 asks for
   this and the session had it nowhere, with T67 and T73 both autograded.
7. **R₀ᵀ is derived in the room now, not cited.** It was re-derived from
   equations 4–6 on 7 November and the published form is exact, so §9's old
   open item is closed and move 3 changes shape: the equilibrium choice becomes
   the *reason* the index case is an I_T cell, two exact cancellations carry the
   derivation, δ′ is shown to cancel rather than assumed benign, and the
   threshold gets a closed form in four clinical observables. `NUMBERS.md` §18.
   **You have not seen this either.** It gives segment 3 two derivations instead
   of one, so §6's cut order now says what comes off inside that segment.
8. **The close is two slides.** Eight limits with their observables will not
   meet the Dwinelle type floor on one. That is a stated departure from §5d's
   "a slide, not a lecture" and is yours to veto — the fallback is the three
   load-bearing rows named at the end of §4.

---

## 10 · The known-open list, closed 7 November

Every item below is now decided in the body of this document. What follows is
the decision and where it lives, so a later pass does not reopen any of it.

| was open | decided |
|---|---|
| three crop keys with no segment row | `weinberger2003_fig2c` goes in **segment 3 FRAME**, as what an I_T cell is clinically, and comes off §6's cut list. `weinberger2003_fig3` goes in **segment 3 DEBRIEF**, as the source of the boundary our design-space figure is replotted beside, and is never cut. Huang & Baltimore's Table 1 had no key at all, so `huangbaltimore1970_table1` was added to §7 and placed as the last slide of **segment 4's build** — the 1970 measurement of what W03 finds as a Hopf — and it stays first on §6's cut list, because it is the only slide in the hour that nothing is assessed on |
| the §3 / §6 contradiction about Fig. 3 | **partly a phantom.** The phrase "the pairing worth building" appears nowhere in §3; §7's design-space figure is where that pairing is specified. §6's cut list never named Fig. 3 either — it named Huang & Baltimore's Table 1 first and Fig. 2c second. So the real defect was Fig. 2c: second on a cut list with no slide to cut. Fig. 3 is now rowed in segment 3 and marked never-cut, and §6 says so |
| §5 segment 1's `derivation_fig` unlisted in §7 | §7 gains **two** figures, not one: `cistrans_fig` for the ledger build, and `objects_fig` for the FRAME, whose four drawn objects §2 requires and §7 also did not list |
| the Limits column short three entries, and only one naming an observable | §4 now carries **eight** limits in a table of its own, each with the observable that tells you you have left it. Two of the three asked for are there as asked — δ′ = Dδ and the An et al. rounding — and the third changed character: R₀ᵀ's SI provenance stopped being a limit when the derivation was done, so that row is now the assumption the derivation does turn on, the missing −kV_T·T in equation [6], worth 0.5% at n = 200. The δ′ row was rewritten too: δ′ is **not** a limit on R₀ᵀ, which does not contain it. The close is two slides, and §4 says why |
| δ called a lifetime in the Constraints row | fixed, with the reciprocals written out: δ = 0.7 day⁻¹ so 1/δ = 1.43 days, c = 30 day⁻¹ so 1/c = 0.033 days. The sweep found no second instance — move 3's derivation and §5 segment 3 both already had it right |
| the back-solve needing a unit conversion | it is the first line of the derivation in §3 and the first move of the step run in §5 segment 3, with the error it prevents named: I\* = 21,430 cells/µl in a patient whose whole T₀ is 800 |
| the retrieval opener carrying nothing from session 24 | **the departure is not taken.** Session 24 supplies two items and the opener leads on them — its dilution rate D against this session's antiviral D, and the QSSA step that threw the Hopf away, which is the clearest case the room owns of an approximation discarding the phenomenon. The s12 and s23 collisions moved to the segments where their objects appear. §5 open carries the reasoning, including what the departure would have been |
| `P_min` specified where the release asks for D | §7 lists `D_min(P, R0)`, which the module exports and the tests exercise, and §3 and §5 segment 3 both name it with its answer: D > 0.0323 at P = 8 |
| repo history in content lines outside §8 | none now. §8 keeps it; every line outside §8 states the requirement instead. The sweep has to be whitespace-insensitive — one instance was wrapped across two lines and a line-by-line grep missed it |

**Three false statements found while closing the list:**

1. **§4 said P is "measurable as a titre ratio in supernatant".** It is the other
   way round. `NUMBERS.md` §3: P is intracellular and W03 says plainly it is not
   the one you can measure; **D** is measured by quantifying HIV-1 titre in
   culture supernatant with and without the vector. The same row also listed "a
   stronger packaging signal" among the routes that move P, where W03 says
   improving Ψ "will likely fail" because HIV-1's regulatory domains are
   believed optimally evolved.
2. **§3 said "two figures against one sentence" for D = 0.4.** Fig. 2a's caption
   gives neither 0.4 nor 0.2 — it says oscillations arise at D = 0.1, while the
   panel's own legend labels the oscillating trace D = 0.2, which is a second
   mismatch rather than a second vote. It is one figure caption and one sentence
   of text, with the panel's behaviour behind the caption. The decision does not
   change; the evidence offered for it was overstated.
3. **§3 said W03's "only body heading is Results and Discussion".** The paper
   has a **Theory** heading as well, on journal 10029. It has no Materials and
   Methods section, which is the half that was right. Read from the PDF and
   recorded as `NUMBERS.md` §17, which also pins each of the three statements of
   the burst-size assumption to its journal page — 10029, 10031 and 10035.

**Two more, in lines this pass had to touch anyway:**

4. **The §3 ledger had crHIV-1 keeping "the sequences RT and integrase act on",
   with the helper supplying "Gag-Pol, Env — every protein".** Neither
   enumeration is in `NUMBERS.md`; §8 gives the cis/trans split and names
   Gag-Pol alone. The row now says what the source says, and adds the antiviral
   cargo gene and the HIV-1-induced promoter, which §8 does list as kept in cis.
   The DI-particle row was narrowed to HB70's own wording the same way.
5. **§3 said which model of the burst is right "is an empirical question nobody
   has answered".** One direct measurement exists and it favours the **capped**
   model — W03's own ref 8, Bukovsky 1999, in vitro. W03 argues past it with a
   mechanism rather than a measurement, and names the two experiments that would
   decide it. `NUMBERS.md` §17b. Move 4 now says that, which is sharper than the
   shrug it replaces.

**What is still genuinely open.** §9 is where these sit. **The R₀ᵀ derivation is
no longer one of them.** It was re-derived from equations 4–6 on 7 November, the
published form is exact with no added assumption, and `NUMBERS.md` §18 carries
it with three independent verifications — so move 3 teaches it, §4's Limits
table lost that row, and the `[unverified]` mark came off the slide. What
remains: the **eclipse-phase equations**, still in the SI and still
`[unverified]`, which would add a survival factor per generation and lower R₀ᵀ
slightly without touching the P²D product structure; whether our P²D = 31/15
contour matches W03's own stability boundary, which segment 3's debrief finds
out in front of the room; and the Fig. 2c 58-versus-21.43 discrepancy, carried
with its note rather than resolved.

**One thing found in §18 itself while reading it in.** §18.5 printed
R₀ = 1 + cV₀/(ndT₀) = "1 + 3000/1600 = 1.9375". The formula and the result are
right; n·d·T₀ is 3200, not 1600, and 1 + 3000/1600 is 2.875. Corrected in
`NUMBERS.md` §18.5 with a dated note, because that line was a candidate for a
slide and it does not compute as printed. The threshold line beside it,
1 + 3200/3000, was already right.
