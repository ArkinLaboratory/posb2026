# Session 3 — Modeling Biology I

[← all sessions](../README.md) · **Thursday, September 3, 2026**

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/sessions/s03-modeling-i/s03_modeling_i.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/sessions/s03-modeling-i/s03_modeling_i.ipynb)

## What this covers

Mass action kinetics, the stoichiometric matrix, and the form that every
deterministic model in this course takes:

$$\frac{d\mathbf{x}}{dt} = \mathbf{S}\,\mathbf{v}(\mathbf{x})$$

This is also the Python onboarding session. Everything later builds on it.

## The structure

The same reaction network is solved **three times**, in increasing abstraction,
with a numerical check at each step:

1. **By hand** — every derivative written out, so the redundancy is visible
2. **As a matrix** — build **S** yourself, integrate `S @ v`, then `assert` it
   matches the hand-written version to 10⁻⁹
3. **With `posb.Model`** — the same network in three lines, `assert`ed against
   the hand-written version again

The package is validated in front of you rather than asserted. See
[Design Notes](../../docs/design-notes.md) for why this matters.

## Worked example

A gene expression cascade: transcription → mRNA → translation → protein, with
degradation of both. Two things it is chosen to teach:

- **Translation is catalytic.** The mRNA appears on both sides of the reaction,
  so its net stoichiometry is zero. Getting this wrong is the most common
  modelling error in the first two weeks.
- **The two species equilibrate on separated timescales.** That observation is
  the entire setup for session 4, where the fast variable gets eliminated
  algebraically — which is where Michaelis–Menten and the Hill function come
  from.

## After this session you should be able to

- Write mass-action rate laws from a reaction list
- Construct **S** by hand and assemble d**x**/d*t* = **S·v**
- Integrate a system numerically with `solve_ivp`
- Predict a steady state analytically and check a simulation against it
- Find and verify a conservation law

*Coverage matrix: T4, T5, T6.*

## Prerequisites

[PS0](../../problem-sets/ps00-environment/) — the ten-minute environment check.

## Next

Session 4 — quasi-steady state; deriving Michaelis–Menten and Hill.
**PS1 goes out today.**
