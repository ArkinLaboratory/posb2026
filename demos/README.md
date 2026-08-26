# Classroom Demos

[← back to the repository root](../README.md)

Interactive notebooks built to be **projected and driven live during lecture**.
Nothing here is graded and nothing is submitted.

| Demo | For | What you turn |
|---|---|---|
| [Crowding](d02-crowding/) | Session 2 | Probe size, and a wall — two predictions, both wrong by a lot |
| [Toggle Explorer](d09-toggle-explorer/) | Session 9 | α₁, α₂, and *n* — watch bistability appear and vanish |

## What makes a good demo here

A demo earns its two minutes of lecture time if **the parameter you drag
changes the answer to a question you just asked the room**. If it only makes a
pretty picture move, it belongs in a notebook, not on the projector.

The toggle explorer works because it lets you do something a static figure
cannot: set *n* = 1 and then fail, publicly and repeatedly, to produce
bistability at any α. That failure is the lesson.

**Take the prediction before the cell runs.** That is the whole difference
between a demo and a slide that moves. A simulation students watch teaches
about as much as a figure; a simulation they have committed a number to first
is a ConcepTest with better feedback. Demo 2 asks twice — *a ribosome is four
times bigger than GFP, so how much slower?* (thirty-five times) and *this is
ordinary diffusion at every step, so what exponent will it show once I put a
wall on it?* (0.75, which is what the microscope reports).

**A demo is not the fix for every thin slide.** If the claim is *quantitative*
— there is a ceiling, the ratio is thirty-five — it wants an axis, and a figure
delivers it in ten seconds with nothing to go wrong. Reach for a demo only when
the claim is about *behaviour*: something appears, or refuses to, as you turn a
knob. Session 2's dilution ceiling is a curve that saturates, so it is a figure.
Session 9's bistability vanishing at *n* = 1 cannot be drawn once, so it is a
demo.

**One per session, not one per point.** Stacking design features into a single
session backfires (Sinha & Kapur), and an engaging-but-tangential animation
measurably costs comprehension — that is the seductive-details effect, and it
is well replicated. A demo belongs at the one moment where the concept is about
behaviour over time or parameter that no static figure can carry.

## Running one in class

Open it on DataHub before lecture and run every cell — the first widget render
takes a few seconds and you do not want that pause live. Demos use `ipywidgets`,
which is installed on DataHub; in Colab, standard widgets work but you may need
`from google.colab import output; output.enable_custom_widget_manager()`.

Students can open the same link afterwards and keep playing. That is most of
the value — the lecture use is a demonstration, the after-class use is where
someone actually builds intuition.

| **[Demo 2 — Crowding](d02-crowding/)** | Two things a single diffusion coefficient will not tell you. For session 2. |
