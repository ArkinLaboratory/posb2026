<!--
title: Session 11 — Four problems, and the scaffolding falls away
subtitle: Two halves. Start wherever the scaffolding stops helping you.
session: 11
-->

# Four problems, and the scaffolding falls away

The symmetric ring of repressors, each gene shut off by the one behind it:

$$\frac{dx_i}{dt} = \frac{\alpha}{1 + x_{i-1}^{\,n}} - x_i, \qquad i = 1 \ldots N$$

with time in protein lifetimes and concentration in units of the repression
threshold, so $\alpha$ and $n$ are all that is left.

**Today's three tools, and nothing else.** At the symmetric fixed point
$x_1 = \cdots = x_N = x$:

$$\alpha = x\left(1 + x^{n}\right), \qquad
g = \frac{n\,x^{n}}{1+x^{n}}, \qquad
J = -I - gP$$

$P$ is the cyclic shift, so its eigenvalues are the $N$th roots of unity
$\omega_k = e^{2\pi i k/N}$, and therefore

$$\lambda_k = -1 - g\,\omega_k, \qquad
\operatorname{Re}\lambda_k = -1 - g\cos\!\left(\frac{2\pi k}{N}\right).$$

The state holds while every $\operatorname{Re}\lambda_k < 0$; it fails when the
worst one reaches zero. At each transition this sheet asks *why does that step
follow?* Answer in writing before you go on.

---

## 1 — Fully worked: the ring of three at $n = 3$

<div class="q" markdown="1">

The worst $\cos(2\pi k/3)$ is $-\tfrac{1}{2}$ (at $k = 1, 2$), so
$\operatorname{Re}\lambda = -1 + g/2$ and the state fails when $g = 2$.

Setting $g = 2$: $\;n x^{n} = 2(1+x^{n})$, so $x^{n}(n-2) = 2$, giving
$x^{n} = 2/(n-2)$. At $n = 3$: $x^{3} = 2$, so $x = 2^{1/3} = 1.260$, and

$$\alpha_c = x(1+x^{n}) = 1.260 \times 3 = \mathbf{3.780}.$$

Below $3.780$ the ring settles; above it, it oscillates. *Why does that step
follow?* — because $g$ rises with $\alpha$, so crossing $g = 2$ once means
crossing it for good.

</div>

## 2 — Last step blank: the ring of three at $n = 4$

<div class="q" markdown="1">

Same three tools, one number changed. From $x^{n} = 2/(n-2)$ with $n = 4$:

$$x^{4} = \frac{2}{2} = 1, \qquad\text{so}\qquad x = \underline{\phantom{0.000}}$$

$$\alpha_c = x\left(1+x^{n}\right) = \underline{\phantom{0.000}}$$

<div class="rule"></div>

*Why does that step follow?* — is raising $n$ from 3 to 4 making the oscillator
easier or harder to build, and does that match what you would have guessed?

<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## 3 — Last two blank: a ring of five

<div class="q" markdown="1">

Now $N = 5$ instead of 3. Nothing about the derivation changes except which
roots of unity appear. The five values of $\cos(2\pi k/5)$ for $k = 0 \ldots 4$
are

$$1,\quad 0.309,\quad -0.809,\quad -0.809,\quad 0.309.$$

The worst case is the most negative one, $-0.809 = -\cos(\pi/5)$, so

$$\operatorname{Re}\lambda_{\text{worst}} = -1 + \underline{\phantom{0.0000}}\;g
\qquad\Longrightarrow\qquad
\text{the state fails when } g = \underline{\phantom{0.0000}}$$

<div class="rule"></div>

*Why does that step follow?* — a ring of five needs **less** gain than a ring of
three. Say why in one sentence, in terms of what going once around the loop
costs you.

<div class="rule"></div>
<div class="rule"></div>

**And the one that is not symmetric.** Try $N = 4$. What is the worst
$\cos(2\pi k/4)$, and what is different about the eigenvalue that achieves it?
What does that tell you about a ring with an even number of repressors?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## 4 — Bare problem

<div class="q" markdown="1">

You have a working three-gene ring oscillator. Your collaborator needs it to
**stop oscillating** and sit at a steady level — and they cannot change $\alpha$,
because the promoters are doing other work in the same cell.

Name a change you would make, say which quantity in today's derivation it moves,
and say which way. There is more than one right answer; give two if you can, and
say which you would try first and why.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>
