# Session 25 — Your payload is the vector's own fitness

Thursday 19 November 2026. Reading assigned at the close of session 24:
Weinberger, Schaffer & Arkin, *J. Virol.* **77**(18):10028–10036 (2003),
"Theoretical design of a gene therapy to prevent AIDS but not human
immunodeficiency virus type 1 infection".

Optional, for students who want the same arithmetic in a different organism:
Noble, Adlam, Church, Esvelt & Nowak, *eLife* **7**:e33423 (2018). Optional, for
where the idea started: Huang & Baltimore, *Nature* **226**:325–327 (1970).

**Precedence.** If anything in this document disagrees with a built artifact,
the artifact is right and this file is stale. Every number quoted here is in
`NUMBERS.md` with its kind and its page.

**The paper is Adam's.** It needs no hedging and no apology on a slide —
students like it. It also gets checked exactly as hard as anyone else's, and
this session finds three things wrong with it. That is the point, not an
awkwardness.

---

## 0 · The title and the opening carry the main point

Standing rule, stated by Adam on 1 November: a session's title slide and its
opening are not scene-setting — they state the single claim the hour
establishes, in the words the session will use for it.

**Published catalog title, already in students' hands:** *Design at population
scale: defective interfering particles, therapeutic interfering particles, gene
drives — engineering a thing whose point is that it spreads.* `course.yaml` and
the syllabus keep it.

**Title slide:** **Your payload is the vector's own fitness.** One claim.
Chosen over "A cure that has to spread", "Engineering a parasite" and "The
therapy has to infect people" because it names the *result* rather than the
subject, and because the result is the thing that makes the hour's paradox
inevitable instead of surprising.

**The main point, in one sentence:** a therapeutic parasite persists only if
its own reproductive ratio exceeds one, that ratio is **R₀ᵀ = P²D(1 − 1/R₀)**,
and the antiviral payload D sits in the vector's own production term as well as
the virus's — so the quantity that makes the therapy work is the same quantity
that makes it spread, and there is an **optimum** in D rather than a maximum.
**In this architecture.** The scope phrase is not a hedge; §5 says why dropping
it turns the result into a slogan.

**So the opening names three things and no more:** that the thing being designed
is now an infectious agent rather than a circuit inside a host you own; that
its design specification is a reproductive ratio greater than one; and that the
room has already met every piece of mathematics this needs — a steady state, a
threshold at an eigenvalue crossing, and a selection coefficient from last
Thursday.

What the opening must NOT do: open on HIV biology, or on gene drives. Gene
drives are the close (move 5), and the virology is move 1's object work. The
claim arrives first.

---

## 1 · Where this sits: the unit of design stops being the circuit

Sessions 19 through 23 were one ladder — each rung a context that breaks a
circuit, ordered by how visible the coupling is. Session 23 broke the ladder,
because selection is not a disturbance you can reject. Its close handed off a
specific finding: the levers that actually worked in Rottinghaus were
intra-niche competition and four deleted host genes, **neither of them circuit
design**.

Sessions 24 to 26 make that the subject. Fixed in `private/sources/ps09-PLAN.md`
§1 and not to be reopened:

> **The unit of design stops being the circuit and becomes the population.**

| session | what the population does |
|---|---|
| 23 | removes the circuit — selection is the adversary |
| 24 | controls the circuit — another strain holds its life |
| 25 | **carries** the circuit — and is supposed to pass it on |
| 26 | is the thing being classified |

Session 24 (Tuesday) put two strains in a chemostat and made each one's
survival depend on the other. Session 25 keeps the coupling and removes the
chemostat: the thing you build now has to get from one host to the next on its
own. **Session 23 asked how long a circuit survives a population. Session 25
asks what it takes for a circuit to invade one.** Those are the same algebra
with the sign of the design goal reversed, and saying so is how the hour starts.

---

## 2 · The room has never seen a virus

This is the binding design constraint and it comes from a count, not a hunch.
Across all 22 built 2026 decks, the following terms have **zero** occurrences
on any slide, in any body text, in any speaker note:

> virus · virion · capsid · encapsidation · diploid · heterozygous ·
> homozygous · helper virus · defective interfering · DIP · TIP ·
> interfering particle · R₀ · basic reproductive ratio · reproductive number ·
> transcritical · invasion · epidemic · SIR · co-infection · superinfection ·
> allele · homing · super-Mendelian · minimal genome · minimal gene set

Five more look non-zero and are false positives: `gene drive` (one hit, "one
gene driven by"), `TIP` (two, "on the tip of my tongue"), `packaging` (two, a
Python package), `burst size` (two, and this one is a trap — see below).

The mathematics, by contrast, is in excellent shape: steady state 103,
cooperativity 78, fixed point 28, nullcline 24, Jacobian 22, eigenvalue 20,
bifurcation 10. **This session does not have a mathematics problem. It has an
object problem**, and that is the session-6 failure mode exactly: a session
written from the algebra outward is written for the half of the room that
already knows the biology. The cohort is deliberately bimodal.

**What must be drawn before anything is modelled** (rule 1, and rule 13 —
a slide that asks for work carries the graphic the work needs):

| object | why it cannot be words |
|---|---|
| a virion with **two** RNA strands in one capsid | the entire binomial follows from this one picture; without it, "diploid" is a word |
| a dually infected cell with a 1 : P cytoplasmic pool | this is the urn the binomial draws from |
| the vector beside the full genome, **~4 kb against 10 kb** | makes "what you can delete" visible, and is T68 |
| cis versus trans — what the vector keeps, what the helper supplies | the reason the vector is obligate, which is the paradox's root |
| a diploid locus carrying two alleles | gene drives are unintelligible without it, and half the room are physicists |

**Two name collisions to disarm out loud, both of them live:**

- **Burst size.** Session 12 taught *translational* burst — geometric, mean
  k_p/γ_m. Here n = 200 is the number of virions a cell releases. Same words,
  different object, and the session must say so when n first appears.
- **The selection coefficient s.** Session 23's s is a burden the designer
  wants to *reduce* and the population removes the circuit anyway. A gene
  drive's fitness cost is one the designer *imposes* and the drive spreads
  anyway. Same symbol, opposite intent, seven days apart. Move 5 names this.

**Called back, not redefined:** population as the state variable, generations as
the clock, fitness as a growth-rate ratio, μ, s, Cas9 and gRNA — all established
by session 23. **Cheapest new term in the session:** *transcritical*. The object
is already in hand (fixed point 28, eigenvalue 20, bifurcation 10); only the
name is new.

---

## 3 · The five moves

### Move 1 — The object, and what you are allowed to delete

Draw the virion. Two strands, one capsid, and the fact that which two strands
you get is not controlled by the virus. Then draw a cell infected by both the
virus and the vector, with a cytoplasmic pool of transcripts in ratio 1 : P.

Then the deletion ledger, which is **T68 in its natural home**. A defective
interfering particle *is* a minimal genome: it is the smallest thing that still
gets packaged and still gets replicated. So "what can you delete" and "what
makes it spread" are the same question asked twice, and that is why minimal gene
set reasoning belongs in a session about population-scale design rather than
sitting beside it.

| | what it must keep (cis) | what the helper supplies (trans) |
|---|---|---|
| crHIV-1 vector | packaging signal, the sequences RT and integrase act on | Gag-Pol, Env — every protein |
| a DI particle | whatever the polymerase recognizes as an end | the polymerase itself |
| a split CRISPR drive | the guide and the target homology | the nuclease, from elsewhere in the genome |

**The honest gap, stated on the slide and not hidden in a note:** no paper
assigned here *measures* a minimal genome size. W03 gives 10 kb against ~4 kb
and nothing finer; Huang & Baltimore's DI RNAs are "unidentified pieces". The
packaging-capacity curve that would settle it does not exist in this folder.
`NUMBERS.md` §10 records this as a gap, and the slide says so — rule: say when
something is not known.

### Move 2 — Two draws from an urn, and the promise session 2 made

**Session 2 owes this room a calculation.** On a slide the students saw:

> A plasmid at 5 copies splits binomially: P(one daughter gets none) = 2·(½)⁵
> ≈ 6%. Not asymmetry — counting again, and why low-copy plasmids carry
> partition systems.  → sessions 12, 25

and its speaker note: *"Session 25 does the full binomial calculation for a
genome; this is the one-line version that makes them want it."* `binomial` has
exactly two occurrences in the whole course and they are both that promise.
**Move 2 pays it, and says that it is paying it.**

The two calculations are not the same, and the difference is the lesson:

| | session 2's plasmid | session 25's capsid |
|---|---|---|
| draws | n = 5 copies into a daughter | n = 2 strands into a capsid |
| p | ½ — fixed by physics, a fair coin | **P/(1 + P) — set by the engineer** |
| the question | **loss**: does a daughter get none? | **composition**: which genotype is this virion? |

So the engineer's lever appears exactly where session 2 had a constant. That is
the move from "counting" to "design", and it is worth one slide on its own.

Now the derivation, one genuine mathematical move per slide. Let
q = P/(1+P) be the probability a drawn transcript is vector. Two draws:

    virus homozygote    (1-q)^2  =  1    / (1+P)^2
    heterozygote        2q(1-q)  =  2P   / (1+P)^2
    vector homozygote   q^2      =  P^2  / (1+P)^2

These are exact probabilities and they sum to one. **W03's printed 1 : 2P : P²
is the same thing with the denominator dropped**, and a slide must say which
form it is using, because they differ by (1+P)² and that is the commonest way
this calculation is got wrong.

Then the strike-out. An et al. report that heterozygous lentiviral virions
infect and are internalized but hit a preintegration, postfusion block, so they
produce no viable infection. The infectious ratio collapses to **1 : P²**.

**The result that earns the move:** the heterozygote waste 2P/(1+P)² is maximal
at **P = 1, where it is exactly one half**. An evenly balanced co-infected cell
throws away half of everything it makes, and it does so because the virus is
diploid — a fact about the chassis, not about the design. Derive the maximum
(the derivative vanishes at P = 1); do not assert it. Reference values for the
autograder are in `NUMBERS.md` §4b.

**This is T67.** The item must state whether it wants the normalized
probabilities or W03's unnormalized ratio.

### Move 3 — A threshold, and whose reproductive ratio it is

First the basic model's R₀, because R₀ has zero prior occurrences in this course
and the vector's version is meaningless without it. Define it as the number of
new infections from one infected cell when almost every cell is uninfected.
From W03's equations [1]–[3] the two steady states are

    uninfected:  T = lambda/d          infected:  T* = c/(k n)

and the ratio of the two is R₀:

    R0 = (lambda/d) / (c/(k n)) = lambda k n / (c d)

**And here the session does something better than restate the paper: it checks
it.** W03 prints the denominator as **cδ**, with δ the death rate of infected
cells. Put Table 1's numbers in and that gives **R₀ = 0.055** — a virus that
cannot sustain an infection, in a patient who demonstrably has one. With d, the
uninfected death rate, it gives **R₀ = 1.9375**. Three things then agree with d
and nothing agrees with δ:

- λ/d = **1550 cells/µl**, and Fig. 2c's inset levels off at about 1500.
- The threshold reproduces the paper's own prose. 1 − 1/R₀ = **0.4839**, so
  persistence needs **P²D > 2.0667**; at the paper's stated optimal D ≈ 0.2
  that is **P > 3.21**, and the text says coexistence appears as P passes ~3.
  With δ, 1 − 1/R₀ = **−17.06**, R₀ᵀ is negative everywhere, and Fig. 3 could
  not exist.
- With δ there is no reading on which the paper's own figures are consistent.

So the printed formula carries a typo, and the room finds it by substitution in
about four lines. **Teach it as a wrong turn** (rule 6): give them the printed
form, ask for the number, let the number be impossible, then fix it. A published
paper, in a journal, by the instructor, with an arithmetic slip in its central
definition — and the way you catch it is to put the numbers in.

**And then the sharper lesson, which is not an error at all.** λ and k are not
measurements. W03 says in one line that both were obtained by steady-state
analysis, and the back-solve is exact: k = c/(nT₀) = 30/(200×800) = 1.875×10⁻⁴,
and λ = dT₀ + δI\* = 31.0. So **R₀ = (λ/d)/T₀ = 1550/800 = 1.9375 is true by
construction** — it is a restatement of the two numbers that were fed in, not a
prediction. Table 1 gives λ a literature citation and marks k "no data", which
is how that half-hides. The room should see both: the number is right, and it is
not evidence. This is the best available lesson on where a parameter comes
from, and it costs one slide.

Now the vector's own ratio, which W03 derives in supplementary material that is
not in the PDF — so the session states it, attributes it, and marks the
derivation path `[unverified]` rather than inventing one:

    R0_T  =  P^2 * D * (1 - 1/R0)

**The thing a session will get wrong if it is careless.** R₀ counts infections
from an *infected cell*. R₀ᵀ counts infections from an **I_T cell — a cell
already carrying the vector, waiting for the virus to arrive**. The therapy's
susceptible pool is not uninfected cells; it is cells that already have the
vector and nothing to replicate it. A slide that glosses R₀ᵀ as "the R₀ of the
vector" loses the entire point, and the index case goes on the slide.

**The design result worth the whole move:** 1 − 1/R₀ runs from 0.48 to 0.95
across a tenfold change in R₀, so

    R0_T  ~=  P^2 * D   for any established infection.

**The threshold is a statement about the construct, not about the patient.**
That is the best sentence in the hour and it is where the move ends.

**This is T73.** Pin c = 30 and R₀ = 1.9375 for every item: Table 1's footnote
offers c = 3, which gives R₀ = 19.375 but also T\* = 80, contradicting the
stated T₀ = 800.

### Move 4 — Why a better payload is a worse therapy, and where the model breaks

**The paradox first, because it is structural and it is one line.** D appears in
equation [6] — the vector's own production — as well as in equation [3]. The
vector is an obligate parasite of the Gag-Pol it is suppressing. So

    R0_T = P^2 D (1 - 1/R0)  ->  0   as D -> 0

There is no cargo gene that inhibits the virus without equally inhibiting the
vector, because in this model they share one production term. Meanwhile singly
infected cells never see the inhibition at all, so they rebound the set point to
where it started. The authors' own phrase for it is **crHIV-1 "shooting itself
in the molecular foot"**, and the figure is Fig. 2a: five values of D at P = 30,
non-monotone in D. Put beside it Fig. 2b, which is monotone in P. **Two knobs,
two shapes** — and that is the slide.

The consequence for a designer: **D has an optimum, not a maximum.** W03's text
says ~0.2 and the Fig. 3b caption says ~0.4; the session picks one and says
which, because they are both MODELLED and they are not the same number.

**Then the wrong turn that matters more, and it is the session's best material.**
The binomial fixes *which genotype* a virion is. It does not fix *how many*
virions there are — and W03 does not partition a fixed burst. It multiplies:
one dually infected cell releases D·n virus, P²·D·n vector, and 2P·D·n
heterozygotes, for a total of **(1+P)²·D·n**.

| P | D | total virions from one cell |
|---|---|---|
| 10 | 0.4 | 9,680 |
| 30 | 0.4 (Fig. 2a) | 76,880 |
| **100** | **0.4** (Fig. 3b's HAART-comparable point) | **816,080** |

Set that against the burst sizes the paper itself cites: **200** in vivo
(Haase), three to five times that under CD8 depletion, and **40,000** for
*env*-deleted SIV — a figure W03 attributes to unpublished data. **The headline
design point therefore needs one cell to release about 4,000 times the measured
burst and 20 times the most extreme number the paper can cite.**

W03 is not hiding it: p. 8 says the model assumes the dually infected burst
size exceeds n, "implying that intracellular packaging resources are not
limited", and discusses Gag-Pol as a candidate limit, noting in-vitro work that
found those resources *are* limited. **The abstract and the Fig. 3b caption
carry no such caveat.** So the room gets the contrast between what a paper
assumes in its methods and what its headline claims, which is a transferable
skill and not a gotcha.

Then the alternative, computed on the slide: hold the burst fixed at 200 and
partition it, and at P = 100 the cell releases 0.02 virus and 196 vector
particles — a different model with a different threshold. **Which one is right
is an empirical question nobody in this folder answered.** That is the honest
end of the move, and it is a better place to leave a room than a clean result.

### Move 5 — The same arithmetic, in an organism that does not consent

Declare the change of question on its own slide (rule 9). Everything so far has
been one patient. A gene drive is the same design problem — build something
whose point is that it spreads — in a population that was not asked.

Noble et al. supply the arithmetic. Three alleles: wild type, drive, resistant.
In a drive heterozygote the nuclease always cuts the wild-type allele, so a
drive heterozygote **never transmits wild type** — super-Mendelian inheritance,
and the place the diploid locus drawn in move 1 pays off. Their results, with
the kinds attached in `NUMBERS.md` §6:

- **Resistance prevents fixation, not invasion.** Every published construct
  sits far inside the invading region (Fig. 1B). The lone exception is a 14%
  female line — and the main text's stated range silently drops it.
- **Releasing one or two organisms is enough.** Median peak drive goes from
  0.005 to 0.895 between one and two organisms released; ten "nearly
  guarantees" invasion.
- **Containment is a property of gene flow, not of the construct.** Five demes
  of a hundred with a migration rate of one migrant per two generations, and
  escape is effectively certain.
- The altered majority often carries **drive-created** resistant alleles — the
  drive's own exhaust, itself an engineered sequence.

**And then the sentence that closes Part II.** W03 names its own largest risk in
one line: the most significant risk of the approach is that the vector could be
transmitted between individuals. **Noble et al. is that sentence, about a
different organism, with the arithmetic done.** A therapy whose specification is
R₀ᵀ > 1 is a thing that spreads, and "it spreads" has no clause in it that says
"only through consenting patients". That hands off to session 28 without
pre-empting it.

The session's **s-collision** is named here: session 23's s was a cost the
designer wanted to cut; here the cost is one the designer imposes and the drive
wins anyway. Same symbol, seven days apart, opposite intent.

---

## 4 · The paper has to be taught, not cited

Standing rule 11, and the count that produced it: sessions 20, 21 and 22 showed
**one** paper figure each, against seven to ten for sessions 16 to 19. From
session 20 the paper became a block at the end, after the derivation had taken
the room's attention. That is what "lost in the weeds" means here.

**W03 has exactly three figures, so there is no one-figure excuse.** All three
are used, and the paper is woven through rather than appended — the s19 shape,
which is the one that works, with a dedicated move label:

| figure | the move label | what the room concludes from it |
|---|---|---|
| **Fig. 1** | the paper · what they built | the two arrows that share a D — the paradox, visible before it is derived |
| **Fig. 2a** | the paper · the result you read | D is non-monotone. Five curves, and the best one is not the strongest |
| **Fig. 2b** | the paper · the result you read | P is monotone, and shortens the transient. Two knobs, two shapes |
| **Fig. 2c** | the paper · what it costs | T + I_T restored to ~1500 while T alone falls below the AIDS threshold |
| **Fig. 3** | the paper · the whole design space | and the one place to overlay our own analytic threshold P²D = 2.0667 on their numerical boundary |

Fig. 3 is the pairing worth building: their simulated stability floor with our
closed-form threshold drawn on top of it. W03 reports that agreement only in
the supplementary material nobody can read, so the session supplies the check
the paper's reader cannot make.

From the optional papers, if a surface wants them: Noble Fig. 1B (every real
construct inside the invading region), 1D (resistance wins, population altered
anyway), 2D (containment as gene flow); Huang & Baltimore Fig. 1 outcome III,
"produce no yield", which is R₀ᵀ < 1 thirty-three years before anyone wrote it
down, and their Table 1 — a 768-fold rebound at passage 4 in one cell line
against a flat column in another, which is the 1970 measurement of what W03
rediscovers as an oscillation.

---

## 5 · Five things a later pass must not undo

1. **"In this architecture" stays on the paradox.** The result is not that
   better antiviral genes harm patients. It is that in *this* design the payload
   and the vector's fitness are one quantity. Pitchai's deletion-based TIPs
   compete for Gag rather than suppressing its production, which is a different
   coupling, and whether the paradox survives that change is not answered by any
   paper here. Marked `[unverified]` and handed to the room as an open question.
2. **The burst-size problem is not a footnote.** It is move 4's second half. A
   later pass that trims it to a speaker note removes the only place the session
   distinguishes "the binomial is right about composition" from "the model is
   right about output".
3. **R₀ᵀ's index case is an I_T cell.** Not an uninfected cell. Any rewrite that
   simplifies this to "the vector's R₀" breaks the result.
4. **The printed-δ correction is taught, not silently fixed.** The value of it
   is the room doing the substitution and finding the impossible number. A pass
   that just prints the right formula throws away the lesson and leaves students
   unable to reconcile the slide with the PDF in their hands.
5. **λ and k are back-solved, and the session says so.** R₀ = 1550/800 is a
   tautology and a correct number at the same time. Do not "improve" this into a
   claim that the model predicts R₀.

**If the hour runs short, cut in this order**, and the board notes carry the
same list: Huang & Baltimore's Table 1 first; then Fig. 2c; then the
fixed-burst alternative arithmetic in move 4 (keep the statement that the
question is empirical); then Noble's deme-escape numbers, keeping Fig. 1B and
the one-or-two-organism result. **Never cut move 2's normalization slide or
move 3's index-case slide** — both are places students reliably go wrong, and
both are assessed.

---

## 6 · Segments

Badges follow s23: `open`, `frame`, `segment N`. No minute badges in the header
calls; `Deck.pacing()` owns the run sheet.

| badge | label | content |
|---|---|---|
| open | retrieval — sessions 2, 12 and 23 | three questions: the plasmid binomial from s02; what s12's burst size was a burst *of*; what s23's s measured |
| open | what you should be able to do by the end | three questions, posed as questions |
| frame | where this sits | the ladder, broken at 23, and the unit of design becoming the population |
| segment 1 | the object, before any model | the virion, two strands, one capsid; the dually infected cell and its 1 : P pool |
| segment 1 | what you are allowed to delete | the cis/trans ledger, 4 kb against 10 kb — **T68** — and the gap stated plainly |
| segment 2 | the promise session 2 made | the two binomials side by side; p fixed by physics against p set by the engineer |
| segment 2 | two draws from an urn | the derivation, one move per slide, to 1 : 2P : P² and the normalized form |
| segment 2 | and two thirds of it is thrown away | the An et al. strike-out, infectious ratio 1 : P², and the maximum at P = 1 — **T67** |
| segment 3 | the paper · what they built | Fig. 1, and the two arrows that share a D |
| segment 3 | a ratio the room can check | R₀ from the two steady states; the printed δ; the impossible number; the fix |
| segment 3 | where a parameter comes from | λ and k back-solved; R₀ = 1550/800 true by construction |
| segment 3 | whose reproductive ratio | R₀ᵀ = P²D(1 − 1/R₀), and the index case is an I_T cell — **T73** |
| segment 3 | a statement about the construct | R₀ᵀ ≈ P²D for any established infection |
| segment 4 | Vote · argue · vote again | a ConcepTest on whether a stronger antiviral gene helps, with its resolution slide |
| segment 4 | the paper · the result you read | Fig. 2a and 2b: two knobs, two shapes |
| segment 4 | why the better payload spreads worse | D in both production terms; the molecular-foot mechanism; the optimum |
| segment 4 | the model's own assumption | (1+P)²Dn, the 816,080 virions, and the burst sizes the paper cites |
| segment 4 | the alternative, and the open question | fixed-burst partition at P = 100; which model is right is empirical |
| segment 5 | a different question | declare the change: one patient, to a population that was not asked |
| segment 5 | super-Mendelian inheritance | the diploid locus, the drive heterozygote, and why wild type is never transmitted |
| segment 5 | resistance prevents fixation, not invasion | Noble Fig. 1B and the one-or-two-organism result |
| segment 5 | containment is gene flow | the deme result, and s23's s against this one |
| close | the sentence the paper ends on | transmission between individuals, and the handoff to session 28 |

Two ConcepTests, both vote–argue–vote with a resolution slide immediately after
(Adam's rule: every question a slide asks has its answer written out in the
note, and a question slide is followed by the slides that work the answer):

- **CT1, in segment 2.** A colleague reports that at P = 1 their vector takes
  half the output of a co-infected cell. Options that separate "half of the
  virions" from "half of the *infectious* virions" from "half of the
  transcripts". The resolution is the 1 : 2 : 1 ratio and the strike-out.
- **CT2, in segment 4.** You improve the antiviral gene so it suppresses virus
  production tenfold harder. What happens to the therapy. The resolution is
  Fig. 2a and the shared D.

---

## 7 · What the build needs, in order

Order from s23 §7, which held for 20, 22 and 23: **design → numbers → library →
tests → figures → deck.** Numbers are done (`NUMBERS.md`, 1414 lines, every
entry kinded).

**`posb/populations.py`** — the functions PS9 imports:

| function | returns | notes |
|---|---|---|
| `diploid_packaging(P, normalized=True)` | the three genotype probabilities | `normalized=False` gives W03's 1 : 2P : P² |
| `infectious_fraction(P)` | (1 + P²)/(1 + P)² | after the heterozygote strike-out |
| `heterozygote_waste(P)` | 2P/(1 + P)² | maximum at P = 1 is a test |
| `burst_output(P, D, n=200, fixed=False)` | virus, heterozygote and vector counts | `fixed=True` partitions n instead of scaling it — both models, because move 4 needs both |
| `basic_R0(lam, k, n, c, d)` | λkn/(cd) | docstring records that the paper prints cδ and why that is wrong |
| `therapeutic_R0(P, D, R0)` | P²D(1 − 1/R₀) | docstring records that the index case is an I_T cell |
| `P_min(D, R0)` | sqrt of the threshold over D | for the design-space item |
| `drive_allele_dynamics(...)` | Noble's three-allele recursion | only if move 5 gets an assessed item; T-numbers currently say it does not |

**`tests/test_populations.py`** — closed forms against quadrature, never against
an ODE solver (s23 shipped three error figures that were all measuring the
integrator). Specific assertions this module needs:

- the three probabilities sum to 1 for a decade of P, two-sided bounds
- `heterozygote_waste` maximal at P = 1 and equal to 0.5 there, checked by a
  fine sweep rather than three sampled points — the quantity is non-monotone and
  a coarse grid straddles the extremum
- `infectious_fraction` monotone increasing, limits 0.5 at P = 1 and → 1
- `burst_output` totals (1+P)²Dn in scaling mode and exactly n in fixed mode
- `basic_R0` reproduces 1.9375 from Table 1, and the δ substitution is asserted
  to give the impossible value, so the wrong turn is executable rather than
  prose
- `therapeutic_R0` crosses 1 at P²D = 2.0667, bracketed two-sided
- the claim "R₀ᵀ ≈ P²D for any established infection" is a **predicate**, tested
  by exhaustion over R₀ in [1.2, 20]: assert 1 − 1/R₀ stays within a stated
  band, and assert the band, not just an inequality

**Figures** (`figures/s25_populations.py`), each through `figure_fit`, saved
inside the 4.60 in band so placement scale stays 1.000, curves tagged rather
than legended:

1. the three genotype probabilities against P on a log axis, with the P = 1
   waste maximum marked
2. the burst ledger: total output against P at fixed D, scaling model against
   fixed model, log y — this is the one that carries move 4
3. the design space: P against D with the analytic P²D = 2.0667 contour, built
   to be overlaid on Fig. 3

**Deck** last, after the figures exist.

**Paper figure crops** into `private/paper-figures/` with keys declared in
`decks/paper_figures.yaml`: `weinberger2003_fig1`, `_fig2a`, `_fig2b`, `_fig2c`,
`_fig3`, `noble2018_fig1b`, `_fig1d`, `_fig2d`, `huangbaltimore1970_fig1`,
`_table1`.

**Wire-in, or it silently will not build:** `figures.s25_populations` into
`MODULES` in `tools/build_figures.py`, `s25_populations` into `DECKS` in
`tools/build_decks.py`. Both files have an `unregistered()` gate that reports an
unlisted module, but the no-argument build still skips it.
