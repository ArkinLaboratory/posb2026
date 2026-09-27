# PS5 — Feedforward Loops and Oscillation

[← all problem sets](../README.md) · **Out Oct 1 · Due Oct 8** · 42 points (BioE 247: 48)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps05-feedforward/ps05.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps05-feedforward/ps05.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

Two sessions, two circuits, one question: what does a circuit do with *time*?
Session 10's feedforward loop delays one event or turns a step into a pulse;
session 11's ring of three refuses to settle at all.

Two of these questions are items your handouts said would be here. They are the
same items.

| | |
|---|---|
| **Q1** | The sign rule, as code; then what each of the two common wirings does to a step, and which one Basu built. |
| **Q2** | The delay, measured against a matched comparison circuit — and a test of the sharp-gate formula that shows where it fails and why. |
| **Q3** | Adaptation: peak, final, and the adaptation error, read off the curve rather than solved for. Then tune it. |
| **Q4** | The ring: the symmetric point, the loop gain, and the criterion *g* = 2 with the α<sub>c</sub> it implies. |
| **Q5** | The same boundary with no algebra at all — your own sweep and bisection, then checked against `posb`. |
| **Q6** | *Required for BioE 247, extra credit for BioE 147* — a ring of *N*, the general criterion, and why an even ring is a toggle rather than a clock. |

### Before you start

**The delay convention is not optional bookkeeping.** It is printed at the top
of the notebook and on the session 10 handout: response time is the time for
*Z* to reach 50% of its steady state, a delay is measured against simple
regulation tuned to the **same** steady state, and the ON and OFF steps are
reported separately. A delay quoted without its comparison and its direction
earns no marks.

The feedforward model is **given** in the notebook — you built its argument in
class, so the work here is measuring it, not retyping it. The ring model comes
from `posb.repressilator_model`.

**Q5 before Q5c, please.** `posb` has `sweep`, `leading_real_part` and
`hopf_boundary`, and Q5c is where you may import them. The point of Q5a–b is
that you write the loop once yourself; that is the same rule as every other
tool in this course.

### What the visible tests mean

They check *properties* — symmetries, counts, limits, signs. A green visible
check means "not obviously broken", not "right". The hidden tests check values.
