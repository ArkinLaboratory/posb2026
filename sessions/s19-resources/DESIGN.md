# Session 19 — Resource sharing and burden: the edge that is not in the diagram

**Thursday 29 October 2026.** Part II, fourth session. **PS6 due; PS7 posted.**
Required reading: Ceroni, Algar, Stan & Ellis, *Nat Methods* 2015 — **the PDF
is not yet in `private/readings/` and has to be handed out at the close of
session 18 on Tuesday.**

**Status: DESIGN. The competition algebra is derived and verified; the
measured growth-law and burden numbers are pending PDFs and are marked below.**

---

## 1 · What the session is for

Session 17 showed composition failing because parts change each other through
what they share physically — a junction encodes a 5′UTR, so attaching a
promoter changes the mRNA stability you were about to call promoter strength.
Its cure was to **impose boundaries**: fix the junction, insulate, standardise,
and the abstraction becomes true because you made it true.

**Session 19 is composition failing again, and this time there is no boundary
to impose.** Two genes with no regulatory connection change each other's output
because they draw on the same ribosomes. You can fix a 5′UTR. You cannot give
your circuit its own ribosome pool.

That escalation is the session, and it is the first rung of the ladder
`docs/course-map.md` builds the rest of Part II on:

> **Sessions 19–25 — the ladder of contexts that break it.** One axis, climbed
> one rung at a time: the host's economy (19, 20), the module next door (21),
> disturbance (22), time and evolution (23), the community (24), the population
> of hosts (25).

So S19 carries a framing job beyond its three techniques: it has to establish
that the circuit lives in something that pushes back, and name the axis.

### The mechanism that runs through three sessions, named here

Session 18's segment on decoy titration, session 19's resource competition and
session 21's retroactivity are **one mechanism**: a molecule held by something
that is not its target.

| session | what is sequestered | by what |
|---|---|---|
| 18 | a transcription factor | decoy binding sites |
| **19** | **a ribosome** | **every other mRNA in the cell** |
| 21 | an upstream regulator | its own downstream binding sites |

A student who leaves with these as three unrelated topics has missed the axis.
S19 names it forward and S21 should call back. Both are one line.

---

## 2 · The object before the model

The required reading's focus line is already written and it sets the opening:

> *"The capacity-against-expression curve. Come able to state what is being
> measured in what units, because 'burden' is otherwise a word."*

So the session opens on **the instrument**, not the algebra. Ceroni's capacity
monitor is a reporter whose output reads the host's spare translational
capacity, and the first question to the room is what it is reading and in what
units — because "burden" with no instrument behind it is a word that sounds
like an explanation.

Before that, one surface on the fact that makes a growth law possible at all,
and it is a genuinely surprising one worth the time: **Schaechter, Maaløe and
Kjeldgaard (1958) found that a bacterium's macromolecular composition is set by
its growth rate and not by the medium that produced it.** Two different media
giving the same doubling time give the same cell. That is why "the cell's
economy" is a thing you can write an equation about rather than a metaphor.
*(Numbers pending the PDF — requested.)*

### The vocabulary check

Run as `posb-teaching-derivations` §1 prescribes, across decks s04–s18:

| term | status going in |
|---|---|
| ribosome | used in s02 (the transcription/translation schematic) |
| growth rate, dilution | **well established** — s05 derived t½ = ln2/(γ + μ) |
| proteome, allocation, growth law | **absent.** New vocabulary. |
| burden, capacity | **absent.** The reading introduces them; the session must define them against the instrument. |

The 2025 and 2024 "cell growth processes" lectures do **not** help here. I read
them: they are population ecology — exponential and logistic growth, carrying
capacity, intraspecific competition, community spatial scales and diffusion
times. Nothing on ribosome allocation, growth laws or burden. `deck-triage.md`
sends "L08 growth/burden → S19", but the material it points at is not about
either. **This session is net-new.** The diffusion-time material in those decks
already went to S02 and S24.

---

## 3 · The derivation, and why it needs nothing new

Quasi-steady state on ribosome binding — session 4's move, with the ribosome in
the place of the enzyme:

    R + m_i <-> C_i  (fast, dissociation constant K_i)
    C_i -> p_i + R + m_i

    C_i = R m_i / K_i
    R_T = R (1 + sum_j d_j)        with demand  d_i = m_i / K_i
    p_i = (k_i R_T / gamma) * d_i / (1 + sum_j d_j)

**That denominator is session 6's partition function with a different pool in
it.** In session 6 the sum ran over binding configurations of an operator; here
it runs over the genes in the cell. The derivation that took a whole session in
September is reused in five minutes here, which is the argument for having done
it the hard way once — and it is worth saying so to the room.

---

## 4 · The three results, all exact, all verified

Derived and checked in `posb/resources.py` against integrating the full binding
kinetics with `posb.core` — 128 tests pass.

**The edge that is not in the diagram.** Gene 1's output falls as gene 2 is
induced, with no regulatory connection between them:

| gene 2's demand (× gene 1's) | gene 1's output falls by |
|---|---|
| 0.25 | 11.1% |
| 1 | 33.3% |
| 4 | 66.7% |
| 16 | 88.9% |
| 64 | 97.0% |

**The fall is exactly a hyperbola** — indistinguishable in shape from
repression by a factor with Hill coefficient 1:

    p_1(d_2) = p_1(0) / (1 + d_2/K_app),     K_app = 1 + d_1

and that is the engineering payoff, because **K_app depends on the demand of
the gene being apparently repressed.** A real repressor's dissociation constant
does not. So measuring the apparent K at two expression levels of the reporter
distinguishes resource competition from regulation **without cloning
anything** — which is a diagnostic a student can design, and the kind of
consequence `posb-teaching-derivations` §3 says has to land on the surface
that earns it.

**The isocost line.** Normalising each output by what it would reach alone,

    p_1/A + p_2/A = (d_1 + d_2) / (1 + d_1 + d_2)

which is below 1 always and approaches it. The achievable outputs are confined
below a straight line whose intercepts are the single-gene maxima, and **the
sum depends only on the total demand, not on how it is split** — verified
constant to twelve figures across five splits at two total demands. You cannot
have both genes at full output, and the trade is linear.

Measured in Gyorgy, Jiménez, Yazbek, Huang, Chung, Weiss & Del Vecchio,
*Biophys J* 109(3):639–646 (2015). *(Which of their numbers are measured and
which fitted — pending the PDF.)*

---

## 5 · The twist, and it is the session's best surface

Session 5 derived the response time and PS2 assessed it:

    t½ = ln2 / (gamma + mu)

with μ the dilution rate set by growth. **Session 5 treated μ as a constant of
the experiment. It is not — it is a property of the host's state, and the
circuit perturbs it.** Induce the circuit, divert ribosomes, growth slows, μ
falls, and every protein in the cell gets a longer effective lifetime,
including the circuit's own.

So the response time computed in session 5 and used on PS2 is not the response
time the circuit will show once it is switched on. Nothing about the DNA
changed. That is T49, and it is the strongest available statement that the host
is not a passive substrate.

`posb.resources.dilution_coupled_steady_state` carries the structure. **It
takes the growth penalty as a required argument with no default**, because the
coefficient that turns demand into a growth penalty differs by host, medium and
construct, and a number baked into a library loses the citation that makes it
mean anything. The course supplies it from Ceroni 2015 once the PDF is in hand.

**Candidate close, pending verification:** Tan, Marguet & You, *Nat Chem Biol*
2009 — a circuit whose bistability is produced by growth feedback rather than
by anything in its diagram. If it holds up, that is the session's last word:
the host did not merely tax the circuit, it added a behaviour. I have not yet
verified what is measured versus modelled in that paper, so it is not in the
plan as a result.

---

## 6 · Segments

| | segment | techniques |
|---|---|---|
| **F** | **Retrieval.** Two from Tuesday (the two exact results of the cycle; why both enzymes must be saturated), one from session 6 — *write the occupancy of an operator with two competing factors*. The answer's shape is the one segment 3 reuses. | — |
| **1** | **The economy.** Schaechter–Maaløe–Kjeldgaard: composition follows growth rate, not medium. Then the growth law. **T50** — argued, not computed, which matches its HAND grading. | **T50** |
| **2** | **The instrument.** Ceroni's capacity monitor. What is measured, in what units. The reading's question, answered by the room. | — |
| **3** | **The derivation.** QSSA on the ribosome; the partition function again; p_i ∝ d_i/(1+Σd). Explicitly a reuse, explicitly cheap. | — |
| **4** | **The hidden edge.** Induce one gene, watch an unconnected one fall. Then the hyperbola, and K_app = 1 + d₁ as the experimental signature. The worked example the syllabus promises — the shared-resource simulation — lives here. | **T48** |
| **5** | **The isocost line.** The bound, and that the trade is linear and depends only on the total. | **T48** |
| **6** | **Burden closes a loop.** Demand → growth → dilution → the circuit's own dynamics. Session 5's t½ revisited with μ no longer a constant. | **T49** |
| **7** | **What a designer does, since insulation is not available.** Lower the demand; use an orthogonal pool; close a feedback loop on burden itself (Ceroni 2018); or characterise in place and stop pretending the number transfers. Checked against the room's own list from segment 1. | — |
| — | **Forward.** S20 is the same conservation argument applied to metabolites, with the same **S** from session 3. S21 is the same sequestration mechanism at an interface instead of in the machinery. | — |

---

## 7 · Scope decisions

**S19 does not take enzymatic synthesis, syn1.0 or syn3A.** S17's design doc
moved them here on the reasoning that genome-scale construction sits beside
resource sharing. Enzymatic DNA synthesis is an assembly topic with no burden
content, and minimal-gene-set reasoning already has a home — **T68 is assigned
to S25**. If the syllabus promise matters it is one closing line in S17
pointing at S25, not a segment here.

**PS7 is posted at the end of this session**, so its scope has to be settled
before Thursday. See finding 1 of `private/log/WEEK10-PLAN-2026-10-19.md`:
counting the matrix, the handoff's recommended option moves the overload from
PS7 to PS8 rather than removing it, and the fix is to rebalance all three
remaining sets to roughly ten techniques each.

---

## 8 · What is still needed

- **Ceroni 2015 PDF — time-critical.** Required reading, handed out Tuesday.
  Also shapes segment 2, which is built on its figure.
- Scott *et al.* 2010 for the growth law's fitted slope and intercept; Schaechter
  1958 for what was actually measured; Dong/Nilsson/Kurland 1995 for the
  gratuitous-protein cost. **No growth-law number goes on a slide until its
  kind is known** — `figures/README.md`'s new rule, and three of week 9's worst
  defects were a correct number with the wrong kind attached.
- Gyorgy 2015 and Tan 2009, as above.
- **Figures**: the growth law; the capacity-against-expression curve from
  Ceroni's data if it is extractable; output of gene 1 against gene 2's demand
  with the hyperbola fit over it; the isocost plane with the achievable region
  shaded and the line approached; the response-time shift under induction.
- **Paper figures** for `decks/paper_figures.yaml`: Ceroni's capacity curve,
  Gyorgy's isocost measurement.
