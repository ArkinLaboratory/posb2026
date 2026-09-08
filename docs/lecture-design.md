# Lecture and Deck Design

[← back to README](../README.md) · See also [Design Notes](design-notes.md) (why the *course* is built this way)

The template every session in this course follows, and the evidence for it.

**Evidence grades used throughout:**

| | |
|---|---|
| **[A]** | Replicated, meta-analytic, moderators known |
| **[B]** | Real evidence, but thin, contested, or heavily context-dependent |
| **[C]** | Convention. Reasonable, unsupported. Stated as such. |

**A caveat that applies to everything here.** Nearly the whole quantitative
evidence base comes from laboratory studies with short retention intervals, or
from large introductory courses. This is a 35-person advanced course with
mixed-background students and high element-interactivity content. Every number
below is an extrapolation. The graded claims are about the *findings*, not about
their transfer to this room.

---

## The problem this template has to solve

Three things make this course hard to design for, and they pull in different
directions.

**The cohort is genuinely bimodal.** Students arrive from biology, physics, and
EECS. For a physicist, deriving Michaelis–Menten from the QSSA is a routine
manipulation; for a molecular biologist it may be the first time they have
eliminated a fast variable. This is not a gap in ability — it is a gap in
*prior knowledge*, and prior knowledge is the single strongest moderator in the
instructional-design literature.

**Worked examples are the course's central pedagogical commitment** — and worked
examples are exactly the intervention whose benefit reverses with expertise.

**High element interactivity.** A two-species phase plane cannot be understood
one piece at a time; nullclines, fixed points, the Jacobian, and eigenvalues
have to be held together. That is precisely the regime where working-memory
limits bind hardest, and where instructional design has the most leverage.

---

## 1. The expertise reversal effect — the finding that shapes everything

Studying worked examples beats solving equivalent problems, **for novices**
(Sweller & Cooper 1985) **[A]**. The reverse is also true: for learners with
sufficient prior knowledge, worked examples become *less* effective than
solving problems outright, and the redundant guidance actively costs them
(Kalyuga et al. 2001) **[A]**.

A meta-analysis of 60 studies confirms the reversal is real and general
([Tetzlaff et al. 2025, *Learning and Instruction* 98:102142](https://doi.org/10.1016/j.learninstruc.2025.102142)) **[A]**.

The literature's own answer to mixed expertise is *adaptive per-student
sequencing*, which a lecture cannot deliver. So the design here is the best
available inference, not a finding:

> **Give everyone the same materials, but let them enter at different points.**

The mechanism, said plainly, is **a short series of the same problem with less
of my working shown each time.** The handouts say exactly that at the top, and
that phrasing is the one to use — in the room, in a session plan, and in this
document. (In the literature it is the *backward-faded worked-example set*;
the term is worth knowing once and then not using, because a label a student
cannot parse is a label that does not tell them what to do.)

Four versions of one derivation, the solution withdrawn a step at a time:

| Item | What students get | Who it serves |
|---|---|---|
| 1 | Fully worked, every step labelled | novices — the worked-example effect |
| 2 | Worked except the **last** step | |
| 3 | Worked except the **last two** steps | |
| 4 | Bare problem | experts — the reversal, avoided |

Fading beats both pure worked examples and pure problem solving
([Atkinson, Renkl & Merrill 2003](https://mrbartonmaths.com/resourcesnew/8.%20Research/Making%20the%20most%20of%20examples/Fading%20out%20and%20Prompts.pdf), effect sizes ~0.23–0.42) **[A]**, and *backward* fading — removing the last step first — outperforms forward fading, because the final step is the one whose purpose is most visible once the earlier work is in front of you.

Delivered as a handout, this is self-paced: a physicist starts at item 3, a
biologist works item 1 carefully. **Nobody is told which to start with, and
nobody has to announce their background to the room.** The instruction on every
such handout is the same sentence — *start wherever the scaffolding stops
helping you* — which is the whole design in eight words.

Two additions with independent support:

- **Subgoal labels.** Name what each step *accomplishes* ("eliminate the fast
  variable"), not just what it does algebraically. Improves transfer,
  *d* ≈ 0.44 ([Margulieux et al. 2020](https://link.springer.com/article/10.1186/s40594-020-00222-7)) **[A]**.
- **Self-explanation prompts.** At each fading transition, ask *why* the step
  follows. Meta-analytic *g* ≈ 0.55 ([Bisra et al. 2018](https://link.springer.com/article/10.1007/s10648-018-9434-x)) **[A]**.

---

## 2. Generation before instruction — and its boundary conditions

Having students attempt a problem *before* being taught the method — productive
failure, or "inventing to prepare for future learning" — improves conceptual
understanding and transfer, meta-analytic *g* ≈ 0.36
([Sinha & Kapur 2021](https://journals.sagepub.com/doi/full/10.3102/00346543211019105)) **[A]**.

Two details matter enormously here.

**It is much larger for advanced learners.** The postgraduate/professional
subgroup shows *g* ≈ 1.03 — though that rests on a thin subset **[B]**. If it
holds, this course is close to the best case for the technique.

**It has fidelity conditions, and failing them wastes the time.** The
consolidation phase must explicitly name and compare what students actually
produced — "group 3 proposed this; here is where it breaks; here is why the
canonical form fixes it." That is the strongest predictor of whether productive
failure works at all. A launch problem followed by a lecture that ignores the
attempts is just a slower lecture.

**It appears to conflict with cognitive load theory, and that conflict is
unresolved [B].** Both literatures are sound; the moderator that would tell you
which regime applies to a *specific* topic has not been measured. The working
resolution used here:

> **Generation for concepts. Faded worked examples for procedures.**

Bistability, adaptation, and why retroactivity exists are concept days — worth
a launch problem. Deriving the Hill function is a procedure — go straight to the
handout set. And [Sinha & Kapur's own finding](https://janfasen.nl/wp-content/uploads/2023/05/Sinha-and-Kapur-PS-I.pdf) that stacking many design features into one short session *backfires* is a direct warning against using every technique on this page every day.

---

## 3. Retrieval, spacing, interleaving

Retrieving material from memory beats re-reading it, robustly and in real
classrooms ([Roediger et al. 2011](https://pdf.retrievalpractice.org/guide/Roediger_Agarwal_etal_2011_JEPA.pdf)) **[A]**. Spacing **[A]** and interleaving **[A]** ([Cepeda et al. 2006](https://augmentingcognition.com/assets/Cepeda2006.pdf); [Rohrer et al. 2020](https://notes.andymatuschak.org/zHvJf88XUgLPMhdTigkoiUR)) are among the best-supported findings in the field.

Two practical consequences:

- **The opener retrieves from more than last time.** Two questions from the
  previous session, **one from three or four sessions back**. A pure warmup on
  yesterday's material forgoes the spacing benefit entirely.
- **Ask elaborative questions, not factual ones.** "Why would this fail?" and
  "when does this assumption break?" transfer better than recall
  ([Pan & Rickard 2018](https://notes.andymatuschak.org/zC1oBp6yE72b7YHzaJZmjXf)) **[A]**.

*Placement at the start of class is convention* **[C]**. What matters is that it
happens and that it is spaced.

---

## 4. Learning goals, maps, and signaling

**Signaling the structure of material works** — headings, consistent visual
roles, arrows on figures — with *g* ≈ 0.33–0.53, and notably it is **not
moderated by prior knowledge** ([Schneider et al. 2018](https://isiarticles.com/bundles/Article/pre/pdf/87157.pdf)) **[A]**. It is one of the few things here that helps the whole bimodal room equally.

**Stating learning objectives as declarative statements has surprisingly weak
support.** What does have evidence is posing them as **questions students cannot
yet answer** — objectives-as-pretest outperformed objectives-as-statements
([Sana et al. 2020, *CBE—Life Sciences Education*](https://www.lifescied.org/doi/10.1187/cbe.19-11-0257)) **[B]**.

So this course's decks open with:

> **By 9:30 you should be able to answer:**
> 1. Why does a toggle switch need cooperativity?
> 2. What destroys bistability?
> 3. …

rather than "Learning objectives: understand bistability."

**The daily course map is convention [C].** It is retained because the course
has an explicit two-half architecture that students should be able to locate
themselves in, and because it costs eight seconds — not because there is
evidence for it.

**Bloom's taxonomy is not used as a design tool here.** Its internal assumptions
do not hold up well empirically ([CBE—LSE](https://www.lifescied.org/doi/10.1187/cbe.20-08-0170)) **[B/C]**, and "learning styles" have no support at all ([Pashler et al. 2008](https://journals.sagepub.com/doi/full/10.1111/j.1539-6053.2009.01038.x)) **[C — debunked]**.

---

## 5. Slide design

Best-supported rules ([Cromley & Chen 2025](https://experts.illinois.edu/en/publications/a-meta-analysis-of-richard-mayers-multimedia-learning-research-se/) meta-analysis of Mayer's programme; [Adesope & Nesbit 2012](https://www.academia.edu/7820678/Verbal_Redundancy_in_Multimedia_Learning_Environments_A_Meta_Analysis) on redundancy; [Sundararajan & Adesope 2020](https://link.springer.com/article/10.1007/s10648-020-09522-4) on seductive details):

**[A] Do:**

- **Extracted key terms and equations, not sentences.** The contrast is stark:
  *g* ≈ 0.99 for extracted keywords versus *g* ≈ 0.21 for verbatim text
  alongside speech.
- **Labelled diagrams**, with labels spatially adjacent to what they label.
- **Consistent signaling** — the same visual role always looks the same.
- **Cut decorative content ruthlessly.** The engaging-but-tangential organism
  photograph measurably costs comprehension. This is the "seductive details"
  effect and it is well replicated.

**[A] Do not:**

- Put prose on a slide and read near it. Verbal redundancy hurts.
- Overlay text on an already-rich diagram — the signaling benefit collapses to
  *g* ≈ 0.06.

**[C] Ignore:** "one idea per slide," 6×6 rules, slide-count targets, and the
claim that attention collapses after 10–15 minutes — that last one has been
looked for and not found ([Wilson & Korn 2007](https://journals.sagepub.com/doi/10.1080/00986280701291291)).

**Attach a source to the claim it supports, not to the slide.** A single
citation in the footer reads as *the source for this slide*, and stops being
true the moment a second source appears on it. `Deck.sources()` takes
`(what, citation)` pairs for exactly this reason — it makes the omission
visible while you are writing the slide rather than while thirty-five people
are looking at it. This is convention **[C]**, adopted after a slide carried a
diffusion coefficient from one paper under a movie from another with only the
first one credited.

**Slide provision.** Post the **complete deck after class**; hand out the
**skeletal handout of the same problem four times, with less working each time, during** class **[B]**. The reasoning is that the
handout is the thing students must construct on, and construction is the point.
The laptop-versus-longhand finding everyone cites
([Mueller & Oppenheimer 2014](https://journals.sagepub.com/doi/abs/10.1177/0956797620965541)) **failed to replicate** ([Urry et al. 2021](https://journals.sagepub.com/doi/abs/10.1177/0956797620965541)) **[C]** — do not tell students to close laptops on that basis. Multitasking on a laptop *does* harm neighbours ([Sana et al. 2013](https://www.sciencedirect.com/science/article/pii/S0360131512002254)) **[B]**, which is a different and better argument.

---

## 5b. Derivations live on slides, not on the board

**Added 7 September 2026, after sessions 3 and 4 were built.** This section
exists because a practice entered the course without ever being decided.

### What happened

Nothing above this line mentions a blackboard. The template was written without
one. Sessions 3 and 4 nevertheless put **37 and 32 minutes** of derivation at the
board — and they are the only two sessions that do. Sessions 1, 2 and 9 have
none. The habit arrived with the two sessions carrying the hardest derivations
in Part I, which is the worst possible place for an undecided practice to land.

It cost student time. Sessions 1 and 2 give the room 38% and 46% of the period.
Sessions 3 and 4 give 35% and 29%. **Session 4 has the lowest student-activity
fraction in the course**, and it bought that with board minutes.

### Why it has to stop for anything assessed

PS1 Q3a assesses the QSSA validity condition. Before this change, the derivation
of that condition existed in exactly two places: a blackboard that was erased,
and `board-notes/s04-board-notes.md`, which is written in the instructor's stage
directions — *ASK*, *CHECK*, *CUT if behind*. A student who missed the class, or
who was present but a step behind, had the result on a slide and the argument
nowhere they could read.

`docs/coverage-matrix.md` says nothing is assessed that was not demonstrated
first. An **ephemeral** demonstration satisfies that only for students who were
in the room *and* took good notes in real time — which is precisely the filter
§1's bimodal-cohort argument exists to remove. It falls hardest on the student
who needs to read the elimination of a fast variable three times, which is the
student the whole design is for.

> **The rule.** The board carries nothing that is assessed. Every technique with
> a T-number in the coverage matrix has a derivation that lives on slides.

### Why a finished derivation on one slide is worse than chalk

Do not read the rule as "paste the algebra onto a slide." A completed derivation
shows the endpoint before the room has processed step one, and the reason
blackboards work is not the medium — it is the **rate**. Chalk moves at roughly
the speed at which a person can follow a manipulation they have not seen, and
the student watches the argument being *made* rather than meeting it finished.

So derivations are built as **step slides**: one slide per step, each identical
to the last plus one line, the live line in full colour and the earlier ones
dimmed. In the room it advances on the clicker at chalk speed. In the exported
PDF each page is a step and the final page carries the whole argument, which is
the artifact a revising student needs. `Deck.derivation()` in `decks/theme.py`
emits the run from a single list of steps, so the near-duplicate slides cost
nothing to author and one edit propagates through all of them. **This is only
affordable because the decks are generated**; a hand-built deck could not carry
six near-identical surfaces per derivation.

`Deck.pacing()` excludes intermediate step slides from the slide-rate check — an
earlier moment of the same surface is not another slide's worth of material.

### What the board keeps

A blackboard does one thing no deck can: it is **parallel and persistent**.
Slides are serial. Session 4's K<sub>M</sub> and V<sub>max</sub> definitions sit
on the left wing for forty minutes and ConcepTest 1 is unanswerable without them;
no slide can hold that while other slides are showing. So the board keeps:

- **The ledger** — the two or three results that must stay visible across the
  whole period.
- **Working a student's wrong answer**, which is unplannable by definition.
- **Anything improvised** in response to the room.

Board notes stay, and stay instructor-facing, but they now script the ledger and
the responses rather than a derivation the slides do not carry.

---

## 5c. One in-class rhythm, not four

**Also 7 September 2026.** Session 4 as first built ran four distinct student
activity modes with four sets of conventions: a retrieval opener, vote–argue–vote
ConcepTests, a written pause, and the handout set. A mixed-background room
spends attention learning each format, and that attention is not spent on the
content.

### The rhythm

> **Pose on a slide → 2–4 minutes on their own paper → poll the room → discuss.**

Everything that was a "ConcepTest" and everything that was a "short class
problem" is now this one shape. Students learn it once.

**Nothing is collected.** An earlier draft of session 4 had students write
answers on paper and hand them in for the instructor to read that evening. That
was a mistake and it is worth recording why: the feedback went to the
*instructor*, not to the student, who got nothing back until the next meeting and
— because the slips were anonymous — never individually. A minute paper is an
instrument for a hall too large to talk to. **This room is about 31 students.**
Collecting slips from 31 people you could simply ask is the wrong tool.

**The first vote is silent and eyes-down.** Public hands induce conformity, which
is the specific failure vote–argue–vote exists to prevent; a show of hands before
the argument has to be a private one.

**Record the poll distribution.** That is the between-class signal the collected
slips were really buying, and writing down "18 for B, 9 for A" after each vote
costs nothing.

### What this does NOT replace

**The handout set — the same problem four times with less of my working each
time — stays exactly as §1 describes it.** It is
a different instrument for a different job — self-paced entry into a procedure,
serving novice and expert from one handout — and it is the course's central
pedagogical commitment. Three modes, not one: the rhythm above, the handout set,
and the retrieval opener.

### Where this is weakest

Whether step slides are adequate for the highest element-interactivity content is
untested. A phase plane — nullclines, fixed points, Jacobian, eigenvalues held
together at once — is exactly where a parallel persistent surface may beat any
serial one, and session 8 is where the cohort is thinnest (5 of 21 respondents
had seen a phase portrait). **Session 8 is the deliberate test case**: built with
slide-resident derivations, keeping one board segment for the ledger, with a
student-facing derivation handout as the record. Revisit this section after it is
taught.

---

## 5d. Every session ends with a design ledger

This course is taken by engineers. A session that derives a result and stops has
told them how the world works and left them no better at building anything in
it. **Every session closes by saying, in the session's own quantities, what a
designer controls and what they do not.**

Three columns. They are short — a slide, not a lecture — and they are written
last, after the content is settled, because a knob you cannot name in the
session's own symbols is not a knob you taught.

| | the question it answers |
|---|---|
| **Knobs** | What can I *set*? Which symbol in today's result is a design variable, and what physical change moves it — a sequence, a copy number, a medium, a part choice |
| **Constraints** | What is set *for* me? Which symbols belong to the host, the physics or the shared economy of the cell, and what determines them |
| **Limits** | Where does today's result stop being true? Every derivation here is taken in some limit; name it, and name the observable that tells you when you have left it |

**The Limits column is the one that must not be skipped**, and it is the one
that is hardest to write, because it requires knowing the derivation's
assumptions well enough to say what breaks them. It is also what separates a
course that teaches models from one that teaches modelling.

### Why the ledger, rather than "applications"

An applications slide shows what other people built. A ledger says what *this
student* could now change, and what would stop them. It is the difference
between an anecdote and a specification.

It also creates the course's only recurring cross-session argument. Session 5's
ledger ends with **one knob for two requirements** — speed and level share the
denominator (γ+μ), so a degradation tag cannot buy both. Session 6's ledger ends
with the opposite — cooperativity buys **sharpness** without touching amplitude,
so those two requirements *do* separate. A student who has both ledgers has
learned something no single session teaches: **whether your requirements share a
knob is a property of the mechanism, and finding out is the first thing a
designer does.**

### What it is not

Not a "real world" aside, not a company logo, not a list of products. If it does
not use the symbols that were on the board that day, it is decoration.

---

## 6. The template

**80 minutes** (Berkeley time: a nominal 90-minute slot).

| Time | Segment | What happens | Evidence |
|---|---|---|---|
| **0–5** | **Retrieval opener** | 2–3 questions, notes closed. Two from last session, **one from ~3 sessions back**. Elaborative, not factual. | Testing effect **[A]**, spacing **[A]**, interleaving **[A]**. Placement **[C]** |
| **5–8** | **Map + goals as questions** | Course map with today highlighted; three questions students cannot yet answer. | Signaling **[A]**; objectives-as-pretest **[B]**; map **[C]** |
| **8–20** | **Generation** *(concept days only)* | A launch problem they cannot yet solve, in groups of 3–4, with **contrasting cases**. Collect solutions. **No feedback yet.** | PS-I *g* = 0.36; *g* = 1.03 for postgraduates **[A/B]** |
| **20–48** | **Concept, in ~3 segments** | ~9 min each. Derivations as step-slide runs (§5b); each segment ends in the rhythm of §5c — pose, 2–4 min on paper, silent vote, discuss, revote. | Peer instruction **[A]**; segmenting **[B]**; PF consolidation fidelity **[A]** |
| **48–50** | **Pause** | Two minutes, instructor silent, individual: revise your own notes. Not collected — see §5c. | Pause procedure **[B]** |
| **50–72** | **The handout set** | The same derivation 3–4 times on one sheet, with less of my working shown each time. Subgoal labels throughout. Self-explanation prompt at each transition. Circulate. | Backward fading **[A]**; subgoal labels **[A]**; self-explanation **[A]** |
| **72–78** | **Consolidation + retrieval** | Close the loop on the launch problem explicitly. Then two minutes: notes closed, write one-sentence answers to the three opening questions. | PF consolidation **[A]**; second retrieval **[A]** |
| **78–80** | **Forward link** | One slide: today's result as a *constraint* on next session's problem, posed as a question. | Prequestion **[B]**, with a null result; the ritual **[C]** |

On non-concept days, drop the generation phase and give the extra 12 minutes to
the handout set.

---

## 7. Telling students why

This matters more than any single technique on this page.

Active-learning formats reliably raise exam performance ([Freeman et al. 2014](https://math.stanford.edu/~conrad/papers/PNAS.pdf), ~0.47 SD, 225 studies) **[A]**. But students in those formats **feel like they are learning less** — in a controlled comparison, actual learning rose ~0.46 SD while *perceived* learning fell ~0.56 SD ([Deslauriers et al. 2019, *PNAS*](https://www.pnas.org/doi/10.1073/pnas.1821936116)) **[A]**.

That gap is the mechanism by which good course redesigns get abandoned. A
course that makes students struggle productively will be *rated lower* while
teaching more, unless the students are told what is happening.

So, in week one, budget the full twenty minutes Deslauriers used:

1. What the format is and why it is built that way
2. **Show them the numbers** — learning up 0.46 SD, feeling of learning down 0.56 SD
3. That the struggle is the mechanism, not a defect in the teaching
4. Return a graded assessment early, so they have objective evidence about
   themselves rather than a feeling

Repeat it briefly at the midterm.

One further finding worth acting on: instructor trust predicts student buy-in
more than twice as strongly as growth mindset does ([Cavanagh et al.](https://www.lifescied.org/doi/10.1187/cbe.20-08-0185)) **[B]**. In a class of 35, the highest-leverage move available is knowing every student's name and background by week three.

---

## 8. Where this is weakest

Stated plainly, because the rest of this page is confident.

1. **Nothing in the literature tells you how to serve a bimodal room in a single
   lecture.** The self-paced handout set is my best inference, not a finding.
2. **Graduate-level pedagogy is barely studied.** The two encouraging moderators
   — Freeman's null for course level, PS-I's postgraduate effect — rest on thin
   subsets.
3. **Productive failure versus cognitive load theory is unresolved** for any
   specific topic. The concept/procedure split used here is a working rule, not
   a result.
4. **Slide design for expert audiences is an evidence vacuum.** Confident claims
   about it, including some above, are extrapolated from novice studies.
5. **The template as a whole is untested.** Every component has support in
   isolation, usually against a do-nothing control. Whether stacking seven of
   them is additive or interfering is unknown — and there is direct evidence
   that cramming too many productive-failure features into one session
   *backfires*.

**Which argues for staging the adoption.** If only three things are adopted:

1. The **handout set** — one derivation, four times, less working each time — with subgoal labels and
   self-explanation prompts
2. The **spaced, interleaved retrieval opener**
3. The **day-one conversation** about feeling-of-learning versus actual learning

Strongest evidence, clearest mechanism, lowest implementation cost. Add
generation to a few concept lectures and see whether it earns its twelve
minutes.
