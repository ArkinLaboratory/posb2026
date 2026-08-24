# Session 1 — What synthetic biology is in 2026

[← all sessions](../README.md) · **Thursday, August 27, 2026**

No notebook. This session is an argument and a diagnostic; the computing starts
with [PS0](../../problem-sets/ps00-environment/), due Wednesday September 2.

## The organising question

> **Can we specify what we want a biological system to do, and then build a cell
> that does it?**

Thirty years in, the answer is *partially*. The whole course is about which part.

## What happens

**80 minutes — 8:10 to 9:30.** The room is listed as 8:00–9:29 in the Student
Information System; under Berkeley Time instruction begins ten minutes after the
official start, and the `:29` is an SIS workaround, not a real end time. This is
what [Lecture Design §6](../../docs/lecture-design.md) assumed all along.

| | | |
|---|---|---|
| 0–3 | The question | And the honest answer: *partially* |
| 3–8 | **Diagnostic** | Ungraded, on paper, **five minutes**. Four questions; the background grid was collected online before today. [PDF](../../handouts/s01-diagnostic.pdf) · [source](../../handouts/s01-diagnostic.md) |
| 8–28 | **Three specifications** | 5 min alone, then 15 in groups. [PDF](../../handouts/s01-launch-problem.pdf) · [source](../../handouts/s01-launch-problem.md) |
| 28–38 | Consolidation | Sense · compute · actuate · **survive** |
| 38–41 | **ConcepTest 1** | Why the field sensors stopped turning red |
| 41–46 | Why this is not electrical engineering | Circuit board, or burrito |
| 46–49 | **ConcepTest 2** | The same promoter, a different construct |
| 49–53 | What 2026 can and cannot do | Nine built objects, four unsolved problems |
| 53–55 | The whole course as one picture | [`figures/build/s01_pipeline.png`](../../figures/build/s01_pipeline.png) |
| 55–75 | **Why the course is built this way** | Twenty minutes. The most important twenty of the term. |
| 75–77 | Forward link | To the cell as a physical substrate |
| 77–80 | Where the computing lives | Show the links, name the Colab fallback, and stop. See below |

### The session is 80 minutes, not 89

An earlier draft of this README read *"89 minutes — 8:00–9:29, not the 80 the
template assumes."* That was wrong and the template was right. Berkeley's
convention is that **instruction begins ten minutes after the official start
time**, and classes are published with `:59` and `:29` end times only as a
workaround for a Student Information System constraint — the Academic Senate
and the Registrar are explicit that those published times "are not intended to
affect actual class meeting times," and that instructors may end on the hour or
half hour. So 8:00–9:29 on the schedule is **8:10–9:30 in the room: 80 minutes.**

Nine minutes had to come out. Where they came from:

- **The nine-minute laptops-open DataHub close is now three minutes.** It was
  the weakest use of the time. Thirty-five students hitting a JupyterHub spawn
  simultaneously in the last ten minutes of an 8am class is a coin flip, the
  most common failure — *DataHub login fails, you are not enrolled yet* — is
  one nobody in the room can fix, and attention at minute 77 is gone.
  Three minutes to put the link and the Colab fallback on screen and say what
  to do when it breaks. **The real environment session belongs in the Tuesday
  discussion hour**, which is otherwise unused in week one and is where someone
  can sit next to a stuck student.
- One minute each from *why this is not EE*, *what 2026 can and cannot do*, and
  consolidation.

Untouched: the launch problem, both ConcepTests, and the twenty minutes on why
the course is built this way. Those are the session.

**Note that the online background form is now load-bearing.** It bought three
minutes back from the diagnostic. Without it this session would be twelve
minutes over, not nine.

### Where the diagnostic's three minutes went

The diagnostic used to be eight minutes and five questions. Question 5 — the
sixteen-box *what have you actually used* grid, plus *what do you want out of
this course* — is **self-report**, and self-report has two properties that
argue for collecting it online, before the term: it cannot be inflated by
looking something up, and it is only useful to the instructor *before* he
teaches. It now goes out with the welcome announcement, along with the
self-rating scales that used to sit, uselessly late and in the wrong container,
in [PS0](../../problem-sets/ps00-environment/).

Questions 1–4 stay on paper, in the room. They are **performance** items, and
three of the four are trivially lookup-able — question 4 is four lines of NumPy
anyone can paste into Colab. Unproctored they would not measure the room; they
would measure who bothered to check, and the bias runs toward apparent
competence, which would make you under-scaffold sessions 3–9. The paper version
also guarantees the sample: an online instrument gets 60–80% of a roster that
is still churning, and the non-responders are not a random draw.

The three recovered minutes go to **consolidation**, which was the real
bottleneck: harvesting from ~10 groups in 8 minutes is 48 seconds each.

### Two things an earlier draft of this session got wrong

**It had 22 minutes of unbroken instructor talk**, at 8am, on day one. There are
now two ConcepTests at the seams — vote, argue with your neighbour, vote again.
Both are answerable from first principles by a room that has been taught
nothing, and both seed a later session: ConcepTest 1 is selection acting on your
circuit (sessions 19, 23), ConcepTest 2 is context-dependence (17, 21).

**It had no figures at all.** That was an over-correction. The seductive-details
evidence justifies cutting the 2025 deck's pp. 4–9 — Global Risks Report,
population projections — because those are tangential decoration. It says
nothing against *explanatory* diagrams, which
[Lecture Design §5](../../docs/lecture-design.md) grades **[A]**. Three figures
come back from the 2025 deck (sense/compute/actuate, circuit-vs-burrito,
prototypes-to-applications) and one is generated from
[`figures/s01_specification.py`](../../figures/s01_specification.py).

## The launch problem

Three real specifications, **given rather than invented**:

- **A** — a bacterium that turns visibly red above 10 µg/L arsenic in well water
- **B** — a T cell that kills a tumour cell and spares a healthy cell of the same tissue
- **C** — a cereal that fixes its own nitrogen

Contrasting cases are the active ingredient here, and students inventing their
own applications reliably produce three variants of the same easy problem.
Ranking them is the part worth arguing about: most rooms rank C hardest for the
wrong reason (*it is a plant*) rather than the right one (nitrogenase is
oxygen-sensitive, the energy cost is enormous, and the host is a community you
do not control).

Every list the room produces contains **sense, compute, actuate** — and omits
**survive**, which is half of this course.

## The twenty minutes

Active-learning formats raise learning ~0.46 SD while *lowering* perceived
learning ~0.56 SD ([Deslauriers et al. 2019](https://www.pnas.org/doi/10.1073/pnas.1821936116)).
That gap is the mechanism by which good course redesigns get abandoned, so week
one spends real time on it. See
[Lecture Design §7](../../docs/lecture-design.md).

## Reading

**None.** PS0 instead — ten minutes, ungraded, **due Wednesday September 2**.

The date matters. PS0 used to be due Tuesday September 1, which is the same day
as the discussion hour that is now the environment session — the repair would
have arrived on or after the deadline. Moving it to Wednesday puts the help
before the deadline and the deadline before Session 3, which is where the
notebooks actually start. It also gives you a Gradescope count on Wednesday
night telling you who is still broken before you teach the Python onboarding.

## What was cut from the 2025 version

Six slides of Global Risks Report / population-projection / "the age of biology
is here" framing (2025 L01, pp. 4–9). It is 2016-era advocacy, it is the
seductive-details pattern the slide-design evidence says measurably costs
comprehension, and none of it survives the only question this session asks:
*what would you have to know to build one?* See
[Deck Triage](../../docs/deck-triage.md).

## Before you teach it

**Print two handouts.** Two pages each, so both duplex onto one sheet.

**Check the form responses the night before.** They set the pace of sessions 3–9.

**No laptops needed.** The computing is three minutes of pointing at a screen at
the end; the environment session is the Tuesday discussion hour.

One slide has a shelf life — **"What 2026 can and cannot do."** Re-check it every
year.

Its anchor is Sc2.0, and the point is the one in the *right*-hand column.
Individual synthetic yeast chromosomes have been designed, built and debugged
for over a decade — but **the project is not finished: there is no strain
carrying all sixteen.** Do not say or imply otherwise. That is the whole lesson:
every part was verified in isolation, by people who are extremely good at this,
over fifteen years, in a genome that is small, well characterised and haploid,
and *consolidation is still the hard part*. If integration is unsolved there,
nobody should be surprised when a four-gene circuit behaves differently in a
mouse gut.
