# Design Notes

[← back to README](../README.md)

Why this course is built the way it is. Written partly for students, who
deserve to know what the design is trying to do, and partly for instructors
considering adapting it.

---

## The problem this rebuild solves

This course ran for fifteen years as a team-taught collaboration between
Berkeley and MIT. It was rebuilt for 2026, and the rebuild was driven by a
specific, documented failure — a student wrote, in a course evaluation:

> *"The lectures are fantastic and definitely helped with the exam, but it
> doesn't feel like it helps at all for the problem sets."*

That sentence is diagnostic. It says the lectures and the problem sets were
assessing different things. An audit of the previous version confirmed it, and
the numbers were worse than the impression:

- **Fixed points and linear stability** were worth 20 points on a problem set.
  The only lecture material on them was a slide listing what the symbols meant.
- **Retroactivity** was worth 20 points on a problem set. Across nineteen
  lecture decks, the phrase "impedance matching" appeared twice, both times as
  a phrase in a bullet list. There was no derivation, no example, and no
  worked calculation anywhere in the semester.
- **The criterion for oscillation** was assessed. It was never stated, in words
  or in symbols, at any point in the term.
- Meanwhile, **Boolean logic minimisation** — Karnaugh maps, gate conversion —
  was demonstrated eight or more times and assessed lightly.

Separately, roughly a quarter of class time was duplicated content. A
line-level comparison of the lecture decks found several with one or two unique
lines relative to the deck before them.

None of this reflects on the individual lectures, which students consistently
praised. It reflects a course that had accumulated fifteen years of additions
without a corresponding audit of what it was actually asking students to do.

---

## The four design rules

### 1. Nothing is assessed that was not demonstrated first

Every session contains a **worked example**: not a walk-through of a paper, but
a problem being solved in real time, using the exact technique the next problem
set demands.

This is enforced mechanically rather than by good intentions. The course
maintains a **coverage matrix** — 74 techniques, each mapped to the session
that demonstrates it and the instrument that assesses it. Before a problem set
is released, every problem is checked against a row whose demonstrating session
has already happened.

The matrix is not decoration. When it was first built for the 2026 calendar it
immediately caught the *same failure recurring*: stochastic simulation was
scheduled for October 6, examined October 15, and not practised on any graded
set until after the exam. That got fixed before it reached a student.

### 2. Derive, do not assert

The Hill function is the clearest example. It is used on nearly every problem
set in a course like this. In the previous version it appeared as three
title-only slides and was then used as if it were common knowledge.

Deriving it takes about fifteen minutes from equilibrium binding, and it pays
for itself immediately: once you have derived it, the cooperativity exponent
*n* stops being a fitting parameter and becomes a statement about binding
stoichiometry, and you know exactly which assumptions you are making when you
use it. The same argument applies to Michaelis–Menten, to promoter occupancy,
to the negative-autoregulation speed-up, and to retroactivity.

Where a result *is* asserted rather than derived — and some are, for time — the
lecture says so explicitly and points at where the derivation lives.

### 3. No black boxes in the tooling

The course moved from MATLAB to Python, and the temptation in that move is to
adopt a systems-biology framework that hides the numerics. The course does not.

`posb` is plain NumPy and SciPy. There is no hidden solver, no symbolic engine,
no simulation framework. The governing rule:

> **Nothing in `posb` is abstracted away before it has been built by hand in class.**

Session 3 is the model of how this works. The same reaction network is solved
three times:

1. **By hand** — every derivative written out explicitly, so you see the
   redundancy: the same flux terms repeating with different signs
2. **As a matrix** — build **S** yourself, integrate `S @ v`, then `assert` the
   result matches the hand-written version to 10⁻⁹
3. **With the package** — hand the same network to `posb.Model`, then `assert`
   again against the hand-written version

The abstraction is *validated in front of you* rather than asserted. This costs
about fifteen minutes of class time and buys two things: you can debug the
package when it misbehaves, and you never mistake it for an oracle.

The same pattern recurs. In session 12 you write a Gillespie simulator from
scratch before `posb.stochastic` exists. In session 20 you solve flux balance
analysis as a linear program with `scipy.optimize.linprog` on a stoichiometric
matrix you typed yourself — no COBRA.

### 4. Structure and kinetics are separable, and that separation is reused

d**x**/d*t* = **S·v** is introduced in session 3 as bookkeeping. It is not just
bookkeeping. **S** is *structure* — a constant integer matrix that comes
straight from the reaction list and knows nothing about rate constants or
concentrations. **v** is *kinetics* — where all the biology and all the
parameters live.

In session 20 the course takes exactly the same **S**, discards the kinetics
entirely, and asks a different question of it: *what flux distributions are
consistent with steady state?* That is flux balance analysis, and it is
constraint-based rather than dynamic.

Same matrix, different question. Students who see that connection understand
both topics better than students who meet FBA as an unrelated technique in
week 11.

---

## Choices worth arguing about

Presented as decisions, not as settled truths.

**Digital logic went from roughly seven sessions to two.** The digital
abstraction is a genuinely useful lens on biological circuits — transfer
curves, gain, noise margins, and signal matching all transfer directly. Karnaugh
maps and gate minimisation do not: cells do not have the fan-out or the
composability to make automated logic synthesis pay off, which is roughly why
that research programme plateaued after 2016. The course now teaches the
abstraction (session 13), then teaches *why the abstraction leaks* (session 16),
which is more useful than teaching students to minimise Boolean expressions.

**The second half is deliberately unusual.** Resource competition, retroactivity,
feedback control, evolutionary stability, and containment are underrepresented
in synthetic biology courses relative to how often they are what actually kills
a design. A circuit that works on a plasmid in *E. coli* and fails in a chassis,
in a consortium, or after 200 generations has failed for reasons in sessions
19–23, not for reasons in sessions 8–13.

**Exams are proctored and worth 40%, down from 60%.** Problem sets are
open-book, open-collaboration, and open-tool, which is right for learning and
makes them a weak signal of individual understanding. Two proctored exams at a
reduced combined weight is the trade: much less exam pressure than the course
used to carry, while preserving a real measure of individual capability. This
is stated openly in the syllabus rather than left implicit.

**The frontier material carries a quantitative test.** Machine-learning design,
minimal cells, therapeutic circuits, and biosecurity are the most seductive
lecture material available and the easiest to deliver as a slideshow of
impressive results — which is precisely the failure the previous version was
criticised for. Each of those sessions therefore has a worked example with
numbers in it. The test applied to every one: *can a student be examined on
this?* If not, it is a seminar, not a lecture, and the time goes back to
sessions 19–23.

---

## Acknowledged weaknesses

**Eight consecutive dynamics-heavy sessions (8–13) may lose the students with
biology backgrounds.** The cohort spans biology to physics to EECS. Mitigations
are a diagnostic in session 1, a weekly discussion hour, and the
[Biological Circuit Design](https://biocircuits.github.io) chapters as a second
voice on the same material. It remains a real risk.

**Sessions 27–28 get no formative practice.** They fall after the last problem
set and are assessed only on the final. Accepted deliberately; weighted
accordingly.

**Roughly half the assessed techniques are not autogradable.** Derivations
require a human reader, and the load is front-weighted onto the first half of
the term, which is exactly where the course's value-add lives. That is the
wrong place to economise, so the cost is simply carried.

---

## If you are adapting this

See [For Instructors](for-instructors.md). The short version: the coverage
matrix is the reusable artifact. The lectures are replaceable and the notebooks
are adaptable, but the discipline of mapping every assessed technique to a
demonstrating session is what actually fixed this course, and it transfers to
any quantitative course regardless of subject.
