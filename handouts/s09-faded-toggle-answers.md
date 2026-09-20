<!--
title: Session 9 — Four problems: answers
subtitle: All four items, worked. Numbers from posb; every one checked by hand where a hand can reach it.
session: 9
-->

# Answers — the faded set

<div class="q" markdown="1">

## 1 · Why the diagonal, and why a mirror pair

Swapping $u \leftrightarrow v$ leaves the pair of equations unchanged. So the
set of fixed points is symmetric under the swap: a crossing at $(u, v)$ implies
one at $(v, u)$. Crossings therefore come either on the diagonal, where the swap
does nothing, or in mirror pairs. And there is *always* one on the diagonal
because $x + x^{n+1} = \alpha$ has exactly one positive root — the left side
increases from 0 without bound.

</div>

<div class="q" markdown="1">

## 2 · The pair, classified

$$g_1 = \frac{4 \cdot 0.118 \cdot 8}{17} = 0.222, \qquad
g_2 = \frac{4 \cdot 2 \cdot 0.00164}{1.0002} = 0.013, \qquad
g_1 g_2 = 0.0029 .$$

Stable: $\lambda = -1 \pm \sqrt{0.0029} = -0.946,\ -1.054$. A node, and a deep
one — both eigenvalues near $-1$, which is to say the two proteins relax almost
independently, each at its own lifetime.

**Why the product.** A perturbation has to go round the loop — $u$ changes
$dv/dt$ by $g_2$, the change in $v$ changes $du/dt$ by $g_1$ — and what comes
back is the product. The tiny factor is $g_2$: at $u = 0.118$ the repressor
$u$ is far below its threshold, so promoter 2 does not feel it at all
($u^{4} = 0.0002$). That is what a *committed* state looks like: one arm has
lost its grip entirely.

</div>

<div class="q" markdown="1">

## 3 · $n = 1$

At $u = v = 1$: $g_1 = g_2 = 1 \cdot 1 \cdot 1/(1+1) = \tfrac12$, so
$g_1 g_2 = \tfrac14 < 1$. Stable node, $\lambda = -\tfrac12,\ -\tfrac32$.

**One crossing in total.** Both nullclines are hyperbolas, $u = 2/(1+v)$ and
$v = 2/(1+u)$; neither has an inflection, so they meet once. Tuesday's handout
proved the general statement: with $\beta = \gamma = 1$, $g_1 g_2 =
uv/((1+u)(1+v)) < 1$ at *every* point, so no crossing can ever be a saddle,
and without a saddle there cannot be three crossings.

</div>

<div class="q" markdown="1">

## 4 · Weaken one arm

Only the $v$-nullcline moves: $v = \alpha_2/(1+u^{4})$ sinks toward the
$u$-axis as $\alpha_2$ falls; the $u$-nullcline is unchanged. The $v$-high
crossing near $(0.12, 2)$ and the saddle approach each other and meet — a
**saddle-node** — and the cell is left in the single remaining state, $u$ high
and $v$ off: $(2.000,\ 0.059)$ at $\alpha_2 = 1$. From `stability_report`,
three crossings survive down to $\alpha_2 \approx 1.4$ and only one remains by
$1.3$; the point has walked out of the wedge through one edge.

Same event as 39 µM IPTG, produced by construction instead of by inducer. In the
paper it is **pIKE105**: the arm TetR represses (P$_\text{LtetO-1}$, driving
*lacI*) was left too strong relative to the other, one state swallowed the
other, and the plasmid sits monostable in its low, LacI-on state — the
$u$-high state here. Whether you weaken one arm or strengthen the other is the
same move in the wedge.

</div>
