<!--
title: Session 12 — Four problems, answers
subtitle: Posted after class. The formulas are checked against simulation in tests/test_stochastic.py.
session: 12
-->

# Four problems — answers

Item 1 is worked in full on the handout.

## 2 — The same mean, made in bursts

$$\text{Fano} \approx 1 + b = \mathbf{5}, \qquad
\eta^2 = \frac{5}{25} = \mathbf{0.20}, \qquad \eta = \mathbf{0.447}.$$

More than twice item 1's 0.20, at the same mean. **What changed that the mean
cannot see** is the size of each arrival. Item 1's proteins arrive one at a
time; these arrive four at a time, from a quarter as many transcripts. The mean
is the product of how often and how many, so it cannot tell the two apart. The
spread can.

The design rule this gives you: at a fixed mean, a strong promoter with a weak
RBS is quieter than a weak promoter with a strong RBS. A promoter library and an
RBS library that reach the same expression level are not interchangeable.

**Which to build for 25 per cell with the least variation:** raise the promoter
and weaken the RBS until $b$ is near 1. At $b = 1$ the Fano factor is about 2
and $\eta = \sqrt{2/25} = 0.28$; the floor, as $b$ falls toward zero, is the
Poisson's 0.20. Going lower than that takes feedback, which is item 3.

The exact two-stage result is $\text{Fano} = 1 + k_p/(\gamma_m + \gamma_p)$,
which is $1 + b$ only when the mRNA lifetime is much shorter than the protein's.
For the $b = 10$ pair on the slides, with mRNA ten times shorter-lived, that
formula gives **10.09** against $1 + b = 11$, and the simulation gave **10.3**.
The same correction applies here: at $b = 4$ with the same lifetime ratio the
exact value is 4.64, not 5, so $\eta$ is nearer 0.43 than 0.45. Either is a
full answer — the handout says the mRNA is short-lived, which is the regime
where $1 + b$ is meant to hold.

## 3 — The same gene, repressing itself

$$g = \frac{3 \times 1}{1 + 1} = \mathbf{1.5}, \qquad
\text{Fano} = \frac{1}{1+1.5} = \mathbf{0.4}$$

$$\eta_{\text{constitutive}} = \frac{1}{\sqrt{100}} = \mathbf{0.100}, \qquad
\eta_{\text{self-repressed}} = \sqrt{\frac{0.4}{100}} = \mathbf{0.063}$$

Cutting the Fano factor to 0.4 cuts $\eta$ by $\sqrt{2.5} = 1.58$. The slide
showed $n = 1, 2, 4$ and 8; $n = 3$ falls between them, as it should.

**What the feedback changed.** Not the event rate: at the same mean, births and
deaths each happen at $\gamma x$ per unit time with or without feedback, so the
noise going *in* is identical. What changed is how fast a fluctuation is pulled
back. A cell that drifts high makes less, so it returns at rate $\gamma(1+g)$
instead of $\gamma$. Each fluctuation lasts a shorter time, and the variance is
the noise going in divided by twice that return rate. It is the same mechanism
that made the self-repressed gene respond faster in session 7.

Two limits. The result is for proteins made one at a time;
with bursts the benefit is smaller. And the result is about intrinsic noise
only. Slow extrinsic changes in the gene's own rates are buffered too, and more
strongly: at steady state $\gamma x = f(x)$, so
$d\ln x^*/d\ln\beta = 1/(1+g)$, and a slow wobble in the promoter strength
reaches $x$ divided by $1+g$ in CV, not by $\sqrt{1+g}$.

## 4 — Reading Table 1

There is more than one good answer. Three comparisons that each tell you
something:

- **RP22 with and without IPTG.** Same strain, inducer only. Intrinsic noise
  falls from 25 to 6.3 as expression rises about thirtyfold (intensity 0.030 →
  1.00). That is the $1/\langle n\rangle$ law: more transcripts, smaller
  relative spread. Extrinsic noise falls too, from 33 to 9.8, because saturating
  IPTG makes the cell-to-cell variation in LacI irrelevant (the paper's own
  explanation, note 13, p. 1186).
- **M22 against M22 + repressilator.** Extrinsic noise jumps from 5.4 to 42.
  The clock moves LacI up and down in every cell, out of phase between cells, so
  both promoters swing together, which is what extrinsic means. Be careful how
  much of that jump you credit to the clock: partial repression alone puts
  $\eta_{\text{ext}}$ in the thirties (RP22 at intensity 0.030 reads 33, MG22 at
  0.057 reads 32), and note 13 on p. 1186 says $\eta_{\text{ext}}$ peaks at
  intermediate induction. The repressilator strain sits at intensity 0.18,
  which is in that range. Intrinsic noise
  is 12, but the mean is lower too (intensity 0.18), so compare it against the
  paper's own fit to strain M22, $\eta_{\text{int}}^2 \approx c_1/m + c_2$ with
  $c_1 = 7\times10^{-4}$ and $c_2 = 3\times10^{-3}$ (Fig. 3B caption, p. 1185).
  At $m = 0.18$ that predicts $\eta_{\text{int}} = 8.3\times10^{-2}$, so the
  measured 12 is about 1.5 times higher: noise is larger while a gene is being
  switched than at a steady state (p. 1186). Use the Fig. 3B constants, not
  Fig. 3C's — that fit is for the noisier strain D22.
- **M22 against RP22.** Repressing the promoter about thirtyfold raises
  intrinsic noise from 5.5 to 25 and extrinsic from 5.4 to 33. The intrinsic
  rise is the count law again; the extrinsic rise is LacI, which varies from
  cell to cell and which the constitutive strain does not have at all.

**The check**, on all four rows. M22: $5.5^2 + 5.4^2 = 59.4$, $\sqrt{} = 7.71$
against 7.7. RP22: $25^2 + 33^2 = 1714$, $\sqrt{} = 41.4$ against 41.
RP22 + IPTG: $6.3^2 + 9.8^2 = 135.7$, $\sqrt{} = 11.65$ against 11.7.
Repressilator: $12^2 + 42^2 = 1908$, $\sqrt{} = 43.7$ against 43 — the worst of
the four at 1.6%, and still inside the 39–47 confidence interval the table
prints for it. The table rounds; the identity holds.

## Appendix — the mean and the variance, without solving for $P_n$

This is the question the room asks every year, and it has a clean answer that
needs none of the ladder. Start from the master equation,

$$\frac{dP_n}{dt} = kP_{n-1} + \gamma(n+1)P_{n+1} - (k + \gamma n)P_n,$$

multiply by $n$, and sum over all $n$. Shift the index in each sum so that
$P_m$ appears throughout:

$$\sum_n n\,kP_{n-1} = k(\langle n\rangle + 1), \qquad
\sum_n n\,\gamma(n+1)P_{n+1} = \gamma(\langle n^2\rangle - \langle n\rangle).$$

Subtract the two loss terms, $k\langle n\rangle$ and $\gamma\langle n^2\rangle$,
and everything with an $\langle n^2\rangle$ in it cancels:

$$\frac{d\langle n\rangle}{dt} = k - \gamma\langle n\rangle
\qquad\Longrightarrow\qquad \langle n\rangle = \frac{k}{\gamma}.$$

That is session 5's deterministic equation, recovered as a statement about an
average rather than assumed.

Do the same with $n^2$. The $\langle n^3\rangle$ terms cancel for the same
reason, leaving

$$\frac{d\langle n^2\rangle}{dt}
= 2k\langle n\rangle + k - 2\gamma\langle n^2\rangle + \gamma\langle n\rangle,$$

and at steady state, with $\langle n\rangle = k/\gamma$,

$$\langle n^2\rangle = \left(\frac{k}{\gamma}\right)^{2} + \frac{k}{\gamma},
\qquad \sigma^{2} = \langle n^2\rangle - \langle n\rangle^{2} = \frac{k}{\gamma}
= \langle n\rangle.$$

**Why this matters more than the arithmetic.** The equation for $\langle n\rangle$
involved only $\langle n\rangle$, and the equation for $\langle n^2\rangle$
involved only $\langle n\rangle$ and $\langle n^2\rangle$. The hierarchy
*closed*. That happens because birth and death are **linear** in $n$. Put a Hill
function in — which is what item 3 does — and the equation for $\langle x\rangle$
contains $\langle f(x)\rangle$, which is not $f(\langle x\rangle)$, and the
equation for that contains something worse. There is no exact answer to read
off, for item 3 or for almost any real circuit. That is the honest reason the
feedback result is obtained from the linear-noise approximation and then checked
against simulation, rather than derived.
