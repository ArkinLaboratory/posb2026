<!--
title: Session 11 — Four problems, answers
subtitle: Posted after class. Every number here is checked in tests/test_analysis.py.
session: 11
-->

# Four problems — answers

## 2 — The ring of three at $n = 4$

$x^{4} = 2/(4-2) = 1$, so $x = 1$, and

$$\alpha_c = x\left(1+x^{n}\right) = 1 \times (1+1) = \mathbf{2} \quad\text{exactly.}$$

**Easier, and that is the general pattern.** Going from $n = 3$ to $n = 4$ drops
$\alpha_c$ from 3.780 to 2. More cooperativity means you need weaker promoters to
oscillate, and $\alpha_c \to 1$ as $n$ grows. Against that, $\alpha_c \to \infty$
as $n \to 2$ from above: at $n \leq 2$ **no promoter strength whatever will make
a ring of three oscillate.**

Worth noticing that $\alpha_c = 2$ exactly at $n = 4$ here, and the symmetric
toggle had $\alpha_c = 2$ exactly at $n = 2$. Both are coincidences of the
scaling, not a deep fact, but they make good checks: if your code disagrees with
either, your code is wrong.

## 3 — The ring of five

$\operatorname{Re}\lambda_{\text{worst}} = -1 + 0.809\,g$, so the state fails
when

$$g = \frac{1}{\cos(\pi/5)} = \frac{1}{0.809} = \mathbf{1.236}.$$

**Why five is easier than three.** Each stage of the ring contributes a lag, and
what destabilises the steady state is the signal coming back around *out of
phase* with what is there now. Five stages put the returning signal closer to
perfectly out of phase than three do, so less gain per stage is needed to tip it
over. Three stages need $g > 2$; five need only $g > 1.236$; seven need
$g > 1.110$. More stages, more delay, easier to oscillate — which is the same
statement as the delay result at the end of the session.

**The ring of four, and why it is a different animal.** The values of
$\cos(2\pi k/4)$ are $1, 0, -1, 0$, so the worst is $-1$, at $k = 2$, and
$\omega_2 = e^{i\pi} = -1$ is **real**. The eigenvalue that crosses is therefore
real, not a complex pair, and it crosses at $g = 1$.

That difference is the whole point. A real eigenvalue crossing zero is the
session-9 story: a state loses stability and the system falls into one of two
others — **bistability, not oscillation.** A complex pair crossing together is a
Hopf, and that is a clock. So:

- **odd ring** → complex pair crosses → oscillator
- **even ring** → real eigenvalue crosses → toggle

which is the algebraic form of the argument the room made in the first ten
minutes: an even ring can be consistently colored high-low-high-low and an odd
one cannot.

## 4 — Stopping the oscillation without touching $\alpha$

Anything that pushes $g$ below 2, or that changes which roots of unity appear.
The three that work, best first:

**Lower the cooperativity.** $g = n x^{n}/(1+x^{n}) < n$, so $n \leq 2$ makes
$g < 2$ impossible to beat at any $\alpha$ — the ring cannot oscillate however
the promoters are set. Concretely: swap one repressor for one that binds a single
operator instead of cooperatively at two. This is the answer to try first,
because it is the only one that is robust to whatever your collaborator later
does to $\alpha$.

**Add a fourth repressor to the ring.** From item 3, an even ring crosses on a
real eigenvalue: you get a bistable switch rather than a clock. This is a large
change and it replaces one behavior with another rather than removing it, but it
is decisive.

**Weaken one arm.** Our derivation assumed all three arms identical, but it
survives more than you would think. With different $\alpha_i$ or $n_i$ and equal
removal rates the Jacobian is still $-I$ minus a cycle, only now a weighted one,
and its characteristic polynomial is $\lambda^3 = g_1g_2g_3$. So the eigenvalues
are $-1 - (g_1g_2g_3)^{1/3}\omega_k$ and the criterion is simply

$$g_1g_2g_3 > 8,$$

the symmetric $g > 2$ with the gain replaced by the geometric mean. Weakening one
arm is a single RBS swap and it is the cheapest thing to try in the lab.

What *does* destroy the closed form is **unequal removal rates** — tag one
repressor and the $-I$ becomes $-\mathrm{diag}(\delta_1,\delta_2,\delta_3)$, the
factorisation is gone, and you locate the boundary numerically. That is the same
thing that happened to the toggle in PS4 when one repressor was tagged, and it is
the honest reason the numerical method exists.

**Degradation tags on all three repressors — and this one is subtler than it
looks.** In our scaling $\alpha = \beta/(\gamma K)$, so raising the removal rate
$\gamma$ **lowers** $\alpha$, which lowers $x$, which lowers $g$. Tag hard enough
and the ring drops below $\alpha_c$ and stops. So tags *do* work, and they work
through $\alpha$ — which means they are only available to you here because the
constraint in the question was on the **promoters**, not on $\alpha$ itself. Say
which reading of the constraint you are using and you get the credit either way.

This is the same fact session 9 put on its engineerability slide: *an ssrA tag
shortens a lifetime, and in scaled units that lowers $\alpha$, so you move the
operating point and the timescale together.*

**What genuinely does not change whether it oscillates:** relabelling which
repressor sits where in the ring. The ring is symmetric; the order is a name, not
a parameter.
