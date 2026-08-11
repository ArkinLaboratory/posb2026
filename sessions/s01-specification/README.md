# Session 1 — What synthetic biology is in 2026

[← all sessions](../README.md) · **Thursday, August 27, 2026**

No notebook. This session is an argument and a diagnostic; the computing starts
with [PS0](../../problem-sets/ps00-environment/), due Tuesday.

## The organising question

> **Can we specify what we want a biological system to do, and then build a cell
> that does it?**

Thirty years in, the answer is *partially*. The whole course is about which part.

## What happens

| | | |
|---|---|---|
| 0–3 | The question | And the honest answer |
| 3–11 | **Diagnostic** | Ungraded, on paper. [PDF](../../handouts/s01-diagnostic.pdf) · [source](../../handouts/s01-diagnostic.md) |
| 11–26 | **Three specifications** | Groups of 3–4. [PDF](../../handouts/s01-launch-problem.pdf) · [source](../../handouts/s01-launch-problem.md) |
| 26–34 | Consolidation | Sense · compute · actuate · **survive** |
| 34–42 | Why this is not electrical engineering | Four things that are not true of transistors |
| 42–48 | What 2026 can and cannot do | An honest scorecard |
| 48–50 | The architecture | Two halves |
| 50–70 | **Why the course is built this way** | Twenty minutes. The most important twenty of the term. |
| 70–76 | Mechanics | Assessment, PS0, DataHub |
| 76–80 | Forward link | To the cell as a physical substrate |

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

**None.** PS0 instead — ten minutes, ungraded, due Tuesday.

## What was cut from the 2025 version

Six slides of Global Risks Report / population-projection / "the age of biology
is here" framing (2025 L01, pp. 4–9). It is 2016-era advocacy, it is the
seductive-details pattern the slide-design evidence says measurably costs
comprehension, and none of it survives the only question this session asks:
*what would you have to know to build one?* See
[Deck Triage](../../docs/deck-triage.md).

## Before you teach it

**Print two handouts.** Two pages each, so both duplex onto one sheet.

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
