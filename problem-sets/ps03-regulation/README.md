# PS3 — Regulation Functions and Autoregulation

[← all problem sets](../README.md) · **Out Sep 17 · Due Sep 24** · 43 points (BioE 247: 49)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps03-regulation/ps03.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps03-regulation/ps03.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

Two sessions, one method. Session 6 counted states to get a regulation function;
session 7 put that function on a pair of axes against removal and read the
circuit off the picture.

Four of these questions are the items your handouts said would be here. They are
the same items.

| | |
|---|---|
| **Q1** | *melAB* — two different proteins on one promoter, and only one of them touches polymerase. |
| **Q2** | Design an AND-like promoter: architecture, states, regulation factor, truth table. |
| **Q3** | The negative-autoregulation speed-up, and the ceiling it cannot pass. |
| **Q4** | Positive autoregulation, computationally: every crossing, classified, and the cooperativity that creates them. |
| **Q5** | Fifteen minutes to level, then hold it for a day. Pick a route and price it. |
| **Q6** | *BioE 247* — the same critical cooperativity, from tangency rather than from counting. |

### Before you start

Q3 and Q4 both ask you to find things numerically rather than in closed form.
That is deliberate: Q3's closed form exists only in a limit, and Q4's does not
exist at all in a form you would want to look at. Finding a root properly —
scanning for a sign change, then bracketing — is a technique this course will use
again in session 8.

**Q2 has no single right answer.** You choose the architecture. The tests check
that what you built behaves like an AND gate; the marks are for the state list
behind it.

### Collaboration

Encouraged. Discuss, argue, work at a whiteboard, then write your own solution
and your own code. Record who you worked with in the first cell. If you used an
LLM, say so and say what for — the conditions are that you can explain anything
you submit and that the code you submit runs.
