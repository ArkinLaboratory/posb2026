<!--
title: Session 8 — The switch Gardner built has γ = 1: answers
subtitle: Items 1 and 2, worked. Items 3 and 4 are PS4; those solutions post to bCourses after the deadline.
session: 8
-->

# Answers — items 1 and 2

The key to the two items we did **in the room**. Items 3 and 4 are **PS4**;
their solutions post to bCourses after the deadline, not here.

<div class="rule"></div>

<div class="q" markdown="1">

## 1 · Which curve is the hyperbola

The $v$-nullcline, $v = \alpha_2/(1+u)$, is the hyperbola: with $\gamma = 1$
there is no inflection because $1/(1+u)$ has none — it is the session-4 curve
with $n = 1$, the one that could never be steep. On log axes it is the nearly
straight line of slope $-1$ at large $u$. The $u$-nullcline,
$u = \alpha_1/(1+v^{2.5})$, is the sigmoid, and its steep drop near $v \approx 1$
is what lets the two curves meet three times.

*Worth noticing:* the right-hand panel is the same $\alpha_1$, $\alpha_2$ with
$\beta$ also set to 1. No promoter strength rescues it — the bound
$g_1 g_2 < 1$ holds everywhere. That is the sentence from the lecture,
*no cooperativity, no switch*, in its correct form: **no cooperativity on
either arm**.

</div>

<div class="rule"></div>

<div class="q" markdown="1">

## 2 · pTAK117's three crossings

At B, $u = 1.317$, $v = 6.734$:

$$g_1 = 2.5\cdot\frac{1.317 \cdot 6.734^{1.5}}{1 + 6.734^{2.5}} = 0.485,
\qquad
g_2 = 1\cdot\frac{6.734}{1 + 1.317} = 2.907,
\qquad
g_1 g_2 = 1.41 .$$

$\lambda = -1 \pm \sqrt{1.41} = -1 \pm 1.19$, so $\lambda = +0.19$ and $-2.19$.
A saddle: one direction leaves, slowly. (`jacobian` from posb gives the same
four numbers by finite differences — check yourself.)

For the record, A gives $g_1 g_2 = 0.62$ and C gives $0.008$; both stable.

**▶ Why the product decides.** A perturbation has to go round the loop: a
change in $u$ alters $dv/dt$ by $g_2$, the resulting change in $v$ alters
$du/dt$ by $g_1$, and what comes back is the product. A gain of 12 on one arm
and 0.0006 on the other is a loop that returns 0.008 of what left — deeply
stable. Neither factor alone means anything; it is the same reason a two-stage
amplifier's gain is a product.

At C, $u = 156$ and $v = 0.1$: LacI is high and cI is essentially off. LacI is
in charge — the $u$-nullcline is vertical there, and $g_2 \approx 0.001$ says
cI has no purchase on it at all ($g_2 = 6 \times 10^{-4}$).

**▶ Which is the low state.** The reporter (GFP) sits with cI, so **C, the LacI-high
state, is the low state**, and A is the high state. Its loop gain is $0.008$
against $0.62$ for A: C sits far from marginal, A sits close to it, which is
the paper's *the low state is more stable than the high state*. The asymmetry
in the $\alpha$'s (156 against 15.6) is the asymmetry in the gains. (The
bimodal culture in Fig. 5c is a different fact — a population straddling the
fold at which the *low* state is annihilated — and it is Thursday's.)

</div>
