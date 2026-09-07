# PS2 — Expression Dynamics and the Cost of Speed

[← all problem sets](../README.md) · **Out Sep 10 · Due Sep 17** · 31 points (BioE 247: 36)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps02-expression/ps02.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps02-expression/ps02.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

A short set, on purpose: one first-order differential equation examined
properly, rather than five techniques examined shallowly.

$$\frac{dp}{dt} = \alpha - (\gamma + \mu)\,p$$

Every number comes from Thursday — *E. coli* dividing every 30 minutes, and the
four ssrA tag variants of Andersen et al. 1998.

| | |
|---|---|
| **Q1** | Two removal processes, one rate. Response time, steady state, and why speeding a circuit up costs level. |
| **Q2** | A specification you were handed, and cannot meet with a tag. |
| **Q3** | Getting a removal rate out of noisy data — and whether what you fitted is γ or γ + μ. |
| **Q4** | Two routes to the same curve — integrate it numerically, compare with the algebra. |
| **Q5** | *BioE 247* — induction is not a step. Solve the ramp. |

### Before you start

Q3 uses `posb.data.decay_timecourse`, which is **synthetic**: drawn from the
model the session derives, using Andersen's published half-lives, with
reproducible noise on top. It is not laboratory data and does not pretend to be.
The exercise is the fitting and the interpretation.

### Collaboration

Encouraged. Discuss, argue, work at a whiteboard, then write your own solution
and your own code. Record who you worked with in the first cell. If you used an
LLM, say so and say what for — the conditions are that you can explain anything
you submit and that the code you submit runs.
