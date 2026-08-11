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

The mechanism is the **backward-faded worked-example set**. Not one worked
problem, but a short series of isomorphic problems in which the instructor's
solution is progressively withdrawn:

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
nobody has to announce their background to the room.**

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
faded set. And [Sinha & Kapur's own finding](https://janfasen.nl/wp-content/uploads/2023/05/Sinha-and-Kapur-PS-I.pdf) that stacking many design features into one short session *backfires* is a direct warning against using every technique on this page every day.

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

**Slide provision.** Post the **complete deck after class**; hand out the
**skeletal faded-example sheet during** class **[B]**. The reasoning is that the
handout is the thing students must construct on, and construction is the point.
The laptop-versus-longhand finding everyone cites
([Mueller & Oppenheimer 2014](https://journals.sagepub.com/doi/abs/10.1177/0956797620965541)) **failed to replicate** ([Urry et al. 2021](https://journals.sagepub.com/doi/abs/10.1177/0956797620965541)) **[C]** — do not tell students to close laptops on that basis. Multitasking on a laptop *does* harm neighbours ([Sana et al. 2013](https://www.sciencedirect.com/science/article/pii/S0360131512002254)) **[B]**, which is a different and better argument.

---

## 6. The template

**80 minutes** (Berkeley time: a nominal 90-minute slot).

| Time | Segment | What happens | Evidence |
|---|---|---|---|
| **0–5** | **Retrieval opener** | 2–3 questions, notes closed. Two from last session, **one from ~3 sessions back**. Elaborative, not factual. | Testing effect **[A]**, spacing **[A]**, interleaving **[A]**. Placement **[C]** |
| **5–8** | **Map + goals as questions** | Course map with today highlighted; three questions students cannot yet answer. | Signaling **[A]**; objectives-as-pretest **[B]**; map **[C]** |
| **8–20** | **Generation** *(concept days only)* | A launch problem they cannot yet solve, in groups of 3–4, with **contrasting cases**. Collect solutions. **No feedback yet.** | PS-I *g* = 0.36; *g* = 1.03 for postgraduates **[A/B]** |
| **20–48** | **Concept, in ~3 segments** | ~9 min each, each ending in a vote → discuss → revote. Reference student solutions **by name**. | Peer instruction **[A]**; segmenting **[B]**; PF consolidation fidelity **[A]** |
| **48–50** | **Pause** | Two minutes, instructor silent: compare and revise notes with a neighbour. | Pause procedure **[B]** |
| **50–72** | **Faded worked-example set** | 3–4 isomorphic problems on a skeletal handout, backward-faded. Subgoal labels throughout. Self-explanation prompt at each transition. Circulate. | Backward fading **[A]**; subgoal labels **[A]**; self-explanation **[A]** |
| **72–78** | **Consolidation + retrieval** | Close the loop on the launch problem explicitly. Then two minutes: notes closed, write one-sentence answers to the three opening questions. | PF consolidation **[A]**; second retrieval **[A]** |
| **78–80** | **Forward link** | One slide: today's result as a *constraint* on next session's problem, posed as a question. | Prequestion **[B]**, with a null result; the ritual **[C]** |

On non-concept days, drop the generation phase and give the extra 12 minutes to
the faded set.

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
   lecture.** The self-paced faded handout is my best inference, not a finding.
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

1. The **backward-faded worked-example set** with subgoal labels and
   self-explanation prompts
2. The **spaced, interleaved retrieval opener**
3. The **day-one conversation** about feeling-of-learning versus actual learning

Strongest evidence, clearest mechanism, lowest implementation cost. Add
generation to a few concept lectures and see whether it earns its twelve
minutes.
