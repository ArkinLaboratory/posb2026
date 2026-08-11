# Figures, Demos, and Decks

[← back to README](../README.md) · See also [Lecture Design](lecture-design.md)

Where visual material comes from, and one licensing line that matters.

---

## Figures are generated, not drawn

```bash
python tools/build_figures.py          # all
python tools/build_figures.py s09      # one session
```

`figures/sNN_*.py` → `figures/build/*.png`, committed so slides and READMEs can
embed them without running anything. **Edit the script, never the PNG.**

Every figure is produced by the same `posb` functions students call in their
notebooks. That is not tidiness — it is what stops a slide from illustrating
something the code no longer does. And it lets a figure carry evidence rather
than a claim: `s09_bifurcation.png` plots the analytic boundary as a line and
the numerically-located boundary as points, on shared axes, regenerated on every
build. Agreement between them *is* the check on the derivation.

`figures/style.py` holds the course palette as a matplotlib style. Import it
first in every figure script so lecture, notebook, and problem set look like one
course.

---

## Demos are for driving live

`demos/` holds interactive notebooks meant to be projected during lecture. A
demo earns its two minutes if **the parameter you drag changes the answer to a
question you just asked the room.** Otherwise it is a moving picture.

Open and run it before class; the first widget render is slow and you do not
want that pause live.

---

## ⚠ Figures from published papers: deck yes, repository no

Lecture slides should use the original figures. A construct diagram drawn by the
people who built the thing anchors students historically and is usually better
than anything you would redraw.

**But those figures cannot go in this repository.**

This repo is public and CC BY 4.0. Reproducing a *Nature* figure in a lecture
you deliver is ordinary educational use; putting the same figure in a public
repository under a licence that grants everyone the right to redistribute and
adapt it is not something you have the right to do. The licence would be making
a promise about someone else's copyright.

So the deck sources here carry **labelled slots** — dashed amber boxes naming
the exact figure — and you drop the images in locally:

```
FIGURE FROM THE PAPER
Gardner 2000, Fig. 2
their version of this same picture
```

Two consequences:

1. **Keep the assembled deck out of the public repo.** `private/decks/` or your
   private repository. Only the *source* — the script with slots — is public.
2. **Cite on the slide**, every time. Author, year, figure number.

The generated `posb` figures have no such constraint: they are yours, they are
BSD-licensed with the rest of the code, and they live in `figures/build/`
precisely so the public repository still shows the quantitative content even
though it cannot show the paper's.

### The pairing that works in lecture

Put the paper's figure and your generated one **side by side**. Session 9 does
this with nullclines: Gardner's Figure 2 next to the same picture produced in
four lines of `posb`. It makes a point no single figure makes — that a 2000
*Nature* result is now something a student regenerates in a notebook before
lunch.
