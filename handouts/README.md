# Handouts

[← back to README](../README.md) · See also [Lecture Design](../docs/lecture-design.md)

Paper. Things that get printed and written on: diagnostics, launch problems, and
the handout sets — one derivation repeated with less of my working shown
each time — that are the course's central
pedagogical device.

**The PDFs in this folder are committed**, which is a deliberate exception to
this repository's rule that build artifacts are not tracked. The reason is the
failure mode the whole toolchain exists to prevent: it is 7am, class is at 8,
and you need forty copies. At that moment you open a file and press print — no
Python, no browser automation, no network.

| | |
|---|---|
| [`s01-diagnostic.md`](s01-diagnostic.md) | Session 1, ungraded. Four questions, one from each background the room contains, plus a what-have-you-used grid. Two pages, so it duplexes onto one sheet. |
| [`s01-launch-problem.md`](s01-launch-problem.md) | Session 1. Three given specifications — arsenic sensor, tumour-selective T cell, nitrogen-fixing cereal — with room to write and a ranking to defend. |
| [`s02-faded-estimates.md`](s02-faded-estimates.md) | Session 2. Four estimates, backward-faded — the first worked in full, the last entirely yours. Start where the scaffolding stops helping you. |
| [`s03-board-sheet.md`](s03-board-sheet.md) | Session 3. The structure is printed and the algebra is blank, filled in as it goes up on the board. |
| [`s04-regulation-functions.md`](s04-regulation-functions.md) | Session 4. Where a regulation function comes from. Two items in the room, two on the problem set. |
| [`s05-decay-fitting.md`](s05-decay-fitting.md) | Session 5. Getting a removal rate out of decay data. Two in the room, two on the set. |
| [`s06-regulation-functions.md`](s06-regulation-functions.md) | Session 6. The same object as session 4, rebuilt by counting states instead of by kinetics. |
| [`s07-production-removal.md`](s07-production-removal.md) | Session 7. The same two curves, four times. |
| [`s08-asymmetric-toggle.md`](s08-asymmetric-toggle.md) | Session 8. Gardner's switch with γ = 1 — the diagonal is gone and the argument is not. Two in the room, two on PS4. |
| [`s09-faded-toggle.md`](s09-faded-toggle.md) | Session 9. Four toggle problems, ten minutes in two halves, the scaffolding falling away across them. |
| [`s10-feedforward.md`](s10-feedforward.md) | Session 10. Four feedforward problems in two halves. |
| [`s11-oscillators.md`](s11-oscillators.md) | Session 11. Four oscillator problems in two halves. |
| [`s12-noise.md`](s12-noise.md) | Session 12. Counts, bursts and feedback. |
| [`s13-digital.md`](s13-digital.md) | Session 13. Gates, thresholds and the price of a switch. |
| [`s14-midterm-review.md`](s14-midterm-review.md) | Session 14. Midterm scope and preparation. Not a worksheet — it carries no front matter and so prints without the course header. |
| [`s14-review-practice.md`](s14-review-practice.md) | Session 14. Five motions in the shape they will be asked. Not a practice exam: five things this course asked you to watch rather than do, each worked once and then handed to you. |
| [`s16-logic.md`](s16-logic.md) | Session 16. Ticks, glitches and depth. Three to work, one worked for you, one stretch — everything starts at zero, which is the whole difficulty. |
| [`s17-parts.md`](s17-parts.md) | Session 17. Four to work, all of them on one thing: the number you measured on a part may not belong to the part. |
| [`s18-protein.md`](s18-protein.md) | Session 18. One derivation — the covalent cycle — three times, with less of the working shown each time. |
| [`s19-resources.md`](s19-resources.md) | Session 19. Four to work, all on one thing: two genes with no wire between them still change each other. |
| [`s20-metabolic.md`](s20-metabolic.md) | Session 20. A home guide. The nine-reaction network solved by hand four times, fully worked to entirely yours. Answer key in `private/handouts/`. |
| [`s21-retroactivity.md`](s21-retroactivity.md) | Session 21. A home guide. The retroactivity derivation four times: the chain-rule run worked in full, then the protected and diluted models, then the conservation integral entirely yours. Answer key in `private/handouts/`. |

**Answer keys are not here.** They live in `private/handouts/`, which is a
separate repository with its own remote and is gitignored by this one. Board
notes are in `private/board-notes/` for the same reason. This folder is public.

## Building

```
pip install markdown playwright && playwright install chromium
python tools/build_handouts.py             # all
python tools/build_handouts.py s01         # matching only
python tools/build_handouts.py --check     # CI: are the PDFs stale?
```

`--check` compares a hash of the rendered page against a sidecar in `.build/`.
It needs neither the browser nor the MathJax download, which is what makes it
cheap enough to run on every push.

## Writing one

Markdown, plus front matter in an HTML comment so the source still renders on
GitHub:

```
<!--
title: Session 8 — One derivation, four times
subtitle: Start wherever the scaffolding stops helping you.
session: 8
-->
```

The session number is what puts the right date in the masthead — it comes from
[`course.yaml`](../course.yaml), not from anything typed here.

**Mathematics is full LaTeX**, `$inline$` and `$$display$$`. It is rendered to
SVG at build time by MathJax running inside headless Chromium, so the PDF holds
vector glyphs and depends on no font, script, or network at print time. Markdown
and LaTeX fight over `_`, `*` and `\`, so math spans are lifted out before the
Markdown processor runs and put back afterwards — without that, `$x_1$` quietly
becomes `$x<em>1$`.

Four layout hooks, and deliberately no more:

| | |
|---|---|
| `<div class="rule"></div>` | a ruled writing line |
| `<span class="blank"></span>` | an inline blank |
| `<div class="pagebreak"></div>` | force a new page |
| `<div class="q" markdown="1">…</div>` | keep a question with its answer lines |
| two spaces at a line's end | a hard break — see below |

## Blockquotes run their lines together

Markdown joins consecutive lines into one paragraph, inside a blockquote as
much as anywhere else. A board-notes block written as

    > GGTA
    > reverse:     ATGG
    > complement:  TACC

prints as a single run-on line, and nothing in the build complains, because
nothing is wrong with it — it is what markdown means. **End every line that
must stand alone with two spaces.** The s16 board notes shipped with their
three hazard kinds run together this way and were taught from.

Do not fix this with a blanket pass over the sources. Most multi-line
blockquotes are ordinary wrapped prose, and adding breaks to those puts a
line break in the middle of a sentence — worse than the problem. The two
cases look identical to a script and have to be told apart by reading.

## Aim for an even page count

Two pages duplex onto one sheet; three pages waste one. When a handout spills by
a couple of lines, cut a writing line before you cut the question.
