<!--
title: Session 12 — Four problems, and the scaffolding falls away
subtitle: Counts, bursts and feedback. Start wherever the scaffolding stops helping you.
session: 12
-->

# Four problems, and the scaffolding falls away

One gene, made at rate $k$ and removed at rate $\gamma$ per molecule. The count
$n$ is a whole number that changes by one at a time.

**Today's three results, and nothing else.**

$$\text{birth–death:}\quad \langle n\rangle = \sigma^2 = \frac{k}{\gamma},
\qquad \text{Fano} = \frac{\sigma^2}{\langle n\rangle} = 1,
\qquad \eta^2 = \frac{\sigma^2}{\langle n\rangle^2} = \frac{1}{\langle n\rangle}$$

$$\text{bursts of } b \text{ proteins per mRNA:}\quad \text{Fano} \approx 1 + b$$

$$\text{self-repression at the same mean:}\quad
\text{Fano} = \frac{1}{1+g}, \qquad g = \frac{n\,u^{n}}{1+u^{n}},\quad u = \frac{x}{K}$$

Two identities do all the bookkeeping: $\eta^2 = \text{Fano}/\langle n\rangle$,
and noise sources that are independent add as squares,
$\eta_{\text{tot}}^2 = \eta_{\text{int}}^2 + \eta_{\text{ext}}^2$. At each
transition this sheet asks *why does that step follow?* Answer in writing before
you go on.

---

## 1 — Fully worked: an unregulated gene at a mean of 25

<div class="q" markdown="1">

Take $k = 25$ per lifetime and $\gamma = 1$ per lifetime. The stationary
distribution is Poisson, so

$$\langle n\rangle = \sigma^2 = 25, \qquad
\text{Fano} = \frac{\sigma^2}{\langle n\rangle} = 1,$$

$$\eta^2 = \frac{\text{Fano}}{\langle n\rangle} = \frac{1}{25}, \qquad
\eta = \mathbf{0.20}.$$

Going through the Fano factor looks like a detour here, because it is 1. It is
the route every other item takes, so it is worth walking once while the answer
is known.

Now double the promoter, $k = 50$. The mean doubles, $\eta^2 = 1/50$, and
$\eta = 0.141$: the noise falls by a factor of 1.41, not 2. *Why does that step
follow?* — because the spread of a count grows as the square root of the count,
so the *relative* spread shrinks only as one over its square root.

</div>

## 2 — One step given: the same mean, made in bursts

<div class="q" markdown="1">

Keep the mean at 25 proteins, but make them from a weak promoter and a strong
RBS: each mRNA now makes $b = 4$ proteins on average before it decays, and the
mRNA is short-lived compared with the protein.

$$\text{Fano} \approx 1 + b = \underline{\phantom{00000}}, \qquad
\eta^2 = \frac{\text{Fano}}{\langle n\rangle} = \underline{\phantom{000000}},
\qquad \eta = \underline{\phantom{000000}}$$

<div class="rule"></div>

*Why does that step follow?* — same mean, same promoter-times-RBS product. Say in
one sentence what changed that the mean cannot see.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

Which would you build if you needed this protein at 25 per cell with as little
cell-to-cell variation as possible, and what would you change to get there?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## 3 — Nothing given: the same gene, repressing itself

<div class="q" markdown="1">

Back to one protein at a time (no bursts), now at a mean of 100. Make the gene
repress itself with cooperativity $n = 3$, and tune the promoter so the steady
state sits at $x = K$, i.e. $u = 1$ — the same mean as the constitutive gene you
are about to compare it with.

$$g = \frac{n\,u^{n}}{1+u^{n}} = \underline{\phantom{00000}}, \qquad
\text{Fano} = \frac{1}{1+g} = \underline{\phantom{00000}}$$

<div class="rule"></div>

Compare $\eta$ with the constitutive gene at the same mean of 100:

$$\eta_{\text{constitutive}} = \underline{\phantom{000000}}, \qquad
\eta_{\text{self-repressed}} = \underline{\phantom{000000}}$$

<div class="rule"></div>

*Why does that step follow?* — the feedback did not change how often molecules
are made or destroyed. What did it change?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## 4 — Bare problem: read Table 1

<div class="q" markdown="1">

Elowitz et al. 2002, Table 1 (p. 1185), noise in units of $10^{-2}$:

| strain | intensity | $\eta_{\text{int}}$ | $\eta_{\text{ext}}$ | $\eta_{\text{tot}}$ |
|---|---|---|---|---|
| M22, constitutive | 1 | 5.5 | 5.4 | 7.7 |
| RP22, LacI-repressed | 0.030 | 25 | 33 | 41 |
| RP22 + IPTG | 1.00 | 6.3 | 9.8 | 11.7 |
| M22 + repressilator | 0.18 | 12 | 42 | 43 |

Pick **two rows** whose comparison tells you something. Say which column moved,
by how much, and what in the cell moved it. Then check one row against
$\eta_{\text{tot}}^2 = \eta_{\text{int}}^2 + \eta_{\text{ext}}^2$.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>
