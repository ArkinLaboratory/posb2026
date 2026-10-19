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

## Every number carries its kind

**New, 19 October 2026.** Three of week 9's worst defects were the same shape:
a real number, correctly transcribed, with the wrong *kind* attached.

- NEB publishes 93% for an overhang set and labels it a **predicted** fidelity.
  It reached a slide as "the assay says 93%".
- Cambray 2018's 83% is 83% **of what the design properties explain**, and
  those properties explain 28% of the variance. It reached a deck as "83% of
  the explained variance".
- Cambray 2013's r = 0.9 is on the **31 terminators the model was fitted to**.
  It was presented as the model's performance.

None of these is a citation error. The source was right and the transcription
was right; what was lost was whether the number had been *measured*,
*predicted*, *modelled* or *self-reported*. That distinction is usually the
whole argument — a session whose thesis is "a part is a measurement" cannot
afford to call a prediction a measurement.

So: **a number entering a data module carries its kind beside its value**, in
the key name or in a comment on the same line, before it is used anywhere.

```python
STANDARD_SETS = {
    "common_syntax": {
        "overhangs": [...],
        "predicted_fidelity": 0.81,            # Pryor 2020, PREDICTED
        "predicted_without_worst_pair": 0.92,  # not an assay of this set
    },
}
```

The prefix is doing real work: `predicted_fidelity` cannot be read off as a
measurement by a later reader, including a later you. Where the kind is not
obvious from the name, say it in the comment and name the source there too.

And when the number is load-bearing for the session's claim, **pin it with a
test** that fails if it drifts — see `tests/test_assembly.py`, which fails if
GGTA/TACT stops being the sole pair the handout's rule flags.
