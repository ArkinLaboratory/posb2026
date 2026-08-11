# Figures

[← back to the repository root](../README.md)

Every figure in the lecture slides is **generated from `posb`**, using the same
functions students call in their notebooks.

```bash
python tools/build_figures.py          # all
python tools/build_figures.py s09      # one session
```

Output lands in `figures/build/` and is **committed**, so slides and READMEs can
embed a figure without anyone running code. But those PNGs are build artifacts —
**edit the script, never the image.**

| File | |
|---|---|
| `style.py` | The course palette as a matplotlib style. Import it first in every figure script. |
| `s09_bistability.py` | Nullclines at *n* = 1 vs 2, the separatrix, and the bifurcation boundary. |

## Why generate rather than draw

A hand-drawn figure and the code it illustrates drift apart. Generating means
they cannot: if the model changes, the figure changes, and if the figure is
wrong the code is wrong.

It also lets a figure make a claim that would otherwise be an assertion.
`s09_bifurcation.png` plots the analytic boundary
α_c = n(n−1)^−(n+1)/n as a line and the numerically-found boundary as points,
on the same axes. That the two agree is the evidence that the derivation on the
slide is right — and it is regenerated on every build, so it stays evidence.
