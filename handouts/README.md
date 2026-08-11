# Handouts

[← back to README](../README.md) · See also [Lecture Design](../docs/lecture-design.md)

Paper. Things that get printed and written on: diagnostics, launch problems, and
the backward-faded worked-example sheets that are the course's central
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
title: Session 8 — Faded worked examples
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

## Aim for an even page count

Two pages duplex onto one sheet; three pages waste one. When a handout spills by
a couple of lines, cut a writing line before you cut the question.
