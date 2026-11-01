# PS8 — Metabolism, Retroactivity and Control

[← all problem sets](../README.md) · **Out Nov 5 · Due Nov 19** · 50 points (BioE 247: 58)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps08-metabolism-control/ps08.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps08-metabolism-control/ps08.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

Four sessions and one thread, and the thread is a **column in a table**.

Question 1 asks you to choose a gate family by comparing orthogonality, speed
and **load**. The first two columns you can fill from session 18. The third
you cannot — and the rest of the set is what it takes to fill it.

Session 20 writes a coupling down *exactly*, with no rate constants in it, and
finds that exactness is not the same as enough. Session 21 takes a coupling
your diagram *mis-draws* — an arrow that is really a binding site — and prices
it. Session 22 builds a controller that rejects a disturbance without
modelling it, and then watches dilution, which is session 19's problem, eat
the guarantee.

| | |
|---|---|
| **Q1** | Four gate families on three columns. The third column is the one you cannot fill yet, and saying precisely what you would have to *measure* is the question. |
| **Q2** | A nine-reaction network: build **S**, solve it, find which single deletions are lethal and which flux pairs the network has already locked together. Then change the objective and say what the change commits you to. |
| **Q3** | Retroactivity. Derive it, then price it in **two models that disagree** — one where the complex shields the regulator from removal and one where it does not. Sweep the affinity in both; the speed cost is flat in one and not the other, and the reason is the whole question. |
| **Q4** | The antithetic controller: exact adaptation from two molecules that destroy each other, then dilution, then a disturbance the controller cannot reject for a reason that has nothing to do with dilution. |
| **Q5** | *Required for BioE 247, extra credit for BioE 147* — how the adaptation error scales with the dilution rate, from the algebra rather than from a fit. |

### Before you start

**Q2 and Q3 use `posb.fba` and `posb.retroactivity`.** Both are imported for
you. Both are thin — every function is a few lines of the algebra from the
session — and reading the source is faster than guessing.

**Q4 asks you to write the model, not to call one.** There is no
`posb.control`, deliberately. Three ODEs and `solve_ivp`; the annihilation
term is stiff, so use `method="LSODA"` and tight tolerances.

**Q3's numbers are not the home guide's.** The guide worked the case where the
downstream sites are essentially full. Here they are not, and what you lose is
the site count times the **occupancy**. If your answer is exactly
$p_{\text{tot}}/X_T$, you have assumed something the question removed.

**Q1, Q2e, Q3a, Q3d and Q4a are written answers** — 19 of the 50 points,
with Q5b hand-graded on top of them in the Question 5 section. They are graded
on the argument, not the conclusion. An answer that reaches the
wrong number for a stated and sensible reason scores better than the right
number with no reasoning.

**Q3d(ii) asks you to doubt a published number.** That is not a trick. Look at
the error bars and the sample size before you decide what the number supports.

### What the visible tests do

They check shape, sign, structure and limiting behaviour — not your exact
numbers. A test that passes means your function returns the right *kind* of
thing and behaves correctly where the answer is forced: at zero load, at
saturation, in the limit where a parameter goes away. **The values are checked
by hidden tests**, so a green visible check means "not obviously broken", not
"right".

Several questions have a check you can do by hand first. Q2's optimum is a set
of integers. Q3b's protected model has an answer you can write down without
computing anything. Q4b's target is a ratio of two rate constants. Work those
on paper before you trust the code; if the code disagrees with the paper, the
error is usually upstream of the test.

### Solutions

Distributed through bCourses after the deadline, as always. Not in this
repository.
