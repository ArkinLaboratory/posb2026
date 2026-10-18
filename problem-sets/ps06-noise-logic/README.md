# PS6 — Noise, Gates and Logic in Time

[← all problem sets](../README.md) · **Out Oct 20 · Due Oct 29** · 48 points (BioE 247: 56)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps06-noise-logic/ps06.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps06-noise-logic/ps06.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

Three sessions and one thread: a circuit is not its steady state.

Session 12 said a mean is not a measurement — two cells with the same average
behave differently, and you need a distribution. Session 13 said a gate is not
a curve — it is four numbers, and whether two gates connect is arithmetic you
can do before you build anything. Session 16 said a truth table is not a
circuit — it tells you where the output ends up and nothing about what it does
on the way.

| | |
|---|---|
| **Q1** | The master equation for the simplest unit there is, by hand, and why its stationary distribution is Poisson. |
| **Q2** | A Gillespie SSA you write yourself, then the mean, variance, Fano factor and CV of a constitutive gene. |
| **Q3** | Does negative autoregulation actually reduce noise? At **matched mean**, measured — the claim session 7 made and could not check. |
| **Q4** | Bursting: burst size and frequency from the rate constants alone, and the Fano factor they imply. |
| **Q5** | The gate datasheet, whether two measured gates connect, and the RBS window that rescues them. |
| **Q6** | A truth table compiled to a circuit, the timing table it does not specify, and what actually decides whether an output is safe — which is not what the first two guesses say. |
| **Q7** | How late a deep circuit is, and the rule of thumb for any depth. |
| **Q8** | *Required for BioE 247, extra credit for BioE 147* — intrinsic against extrinsic noise, and what your own Q3 could not see. |

### Before you start

**Two of these are items your handouts promised.** The RBS window is session
13's item 4, and it is Q5c here. Session 16's item 5 has you *discover* the
rule from three given circuits in class; Q6c has you *build* both of them and
check the property with `cold_start_safe`. Deliberately not the same item —
the session 16 answer sheet is public and goes up before this set is due.

**The tick convention for Q6 and Q7** is printed at the top of the notebook
and on the session 16 handout:

> Time runs in ticks. At each tick every gene reads its inputs **as they were
> at the previous tick** and updates; all genes update together. At *t* = 0
> the cell has just been made, so **every gene is at 0**.

**Your stochastic numbers will not match anyone else's.** They are not
supposed to. The tests allow the spread a finite run actually has. If one
fails by a hair, run longer before you change your code.

**Q2a asks you to write a Gillespie loop from scratch.** `posb.stochastic`
has one. Do not use it there, and do use it everywhere after — the debt is
paid once.

### What the visible tests do

They check *properties*: symmetries, limits, counts, agreement with a second
route to the same number. A green check means "not obviously broken", not
"right". Several of the point-carrying checks are hidden.

### Collaboration

Encouraged. Discuss, argue, work at a whiteboard together, then write your own
solution and your own code, and record who you worked with in the first cell.
If you used an LLM, say so and say what for. The conditions are that you can
explain anything you submit and that the code you submit runs.
