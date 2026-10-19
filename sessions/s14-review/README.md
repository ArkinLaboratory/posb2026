# Session 14 — Review, by working five motions

[← all sessions](../README.md) · **Tuesday, October 13, 2026**

> Not a summary of eleven sessions. Things this course asked students to *watch*
> rather than do, each worked once and then handed to them **on a different
> circuit**. Plus one idea that is examined on Thursday and has never been on paper.

## The one thing to remember

> **A disturbance either comes back flipped or it does not, and either comes back
> shrunk or it does not. Those are two separate questions and together they decide
> whether a loop is a clock, a latch, or neither.**

## What exists

| | |
|---|---|
| Student handout | `handouts/s14-review-practice.md` — five motions, each worked then handed over |
| Answers | `private/handouts/s14-review-practice-answers.md` — all five worked. **Posts after class.** |
| Figures | `figures/s14_review.py` — nine panels. Every drawn circuit is checked against the exam's by `_assert_not_exam_circuit`, which refuses pure repression rings of three, four and five and two-gene mutual repression |
| Scope sheet | `handouts/s14-midterm-review.md` — what is on Thursday's paper and what is not |
| Board notes | `private/board-notes/s14-board-notes.md` — Boards 1, 1b, 2, 3 and what to cut if short |
| Deck | `decks/s14_review.py` — five step-run derivations, eight figures |

**Nothing from Thursday's paper appears in this session.** Every example is
deliberately a different circuit from the one the exam uses on the same skill. That
is a constraint on improvisation at the board, not a preference.

## The open item — basins, and why it is a release condition

**This is the one thing in session 14 that another item depends on.**

The midterm's **B1.3** asks what decides whether a brief pulse returns the cell to
its starting state or carries it to the other one, with α and *n* held fixed. That is
coverage-matrix row **T23a**, added 11 October.

Basins and the separatrix were covered at the board in session 9 and again across the
four sessions since. **They are in no slide, no handout and no problem set.** The
`s09_separatrix` figure is built and the session 9 README lists it as retained, but
`decks/s09_bistability.py` places it on no slide.

`docs/lecture-design.md` §5b is Adam's own rule, written 7 September: *the board
carries nothing that is assessed.* B1.3 currently breaks it.

**What has to ship, and where:**

- A **written, student-readable** treatment in `handouts/s14-review-practice.md` —
  the nullclines, the line that runs INTO the middle fixed point (the flow arrives
  along it and stops), and the one sentence that inside it you return and outside it
  you switch. **Shipped**, on mutual activation.
- **One worked question of the B1.3 shape, with its answer**, on a circuit that is
  not the one the exam uses. **Shipped**: item 4's "now you" is a one-gene
  autoactivator, where the divide is a number, followed by the one line on why the
  two-variable case cannot be answered with a number.
- Board 1b in `private/board-notes/s14-board-notes.md` is already written but **does not
  satisfy this** — board notes are instructor-facing by design, which is the whole
  point of §5b.

**This shipped on 11 October, so B1.3 stays on the paper.** `DECISIONS-OPEN.md` §10
is CLOSED. What satisfies it: the deck's basin segment (26–39 min, four-step run plus
two worked slides on mutual activation), handout item 4 and its answer.

**None of it is a toggle.** An asymmetric toggle was used until 11 October and was
removed: it differs from the exam's symmetric phase plane in its parameters alone,
which is not a different circuit.

## Also on the list, not for this week

| Item | Where it goes |
|---|---|
| Practice problems on basins **with answers**, beyond the single worked one above | A problem set or a practice set; Adam's call which |
| Put `s09_separatrix` on a session 9 slide, with the step treatment | Next revision of `decks/s09_bistability.py` — the permanent fix, since session 9 has already run |
| Sharpen the scope sheet's "Read a dynamical picture" line | It currently puts "what the flow tells you" and "what happens when a parameter is changed" adjacent and undifferentiated, and B1.3 turns on exactly that distinction |

## Why these motions, and not others

The record is specific about what students practiced versus what they only watched:

| motion | what they actually practiced | what was missing |
|---|---|---|
| follow a disturbance round a loop | the *result* (odd rings oscillate), stated in s11 and in PS5 | the walk itself, out loud, on a mixed loop |
| signs of a Jacobian | `toggle_jacobian` once in code (PS4 Q2a); eigenvalues from numbers everywhere | reasoning from wiring to sign pattern — s08 *defines* g₁, g₂ as negated partials, so the sign bookkeeping was engineered out |
| draw a time course | watched the s10 panels projected; drew nullclines and rate curves | no handout or problem set has ever asked for a time trace |

Each is a motion the course demonstrated and never required. That is the selection
rule, and it is why a fourth motion was not added for its own sake — basins are here
because Thursday examines them, not because the pattern called for a fourth.
