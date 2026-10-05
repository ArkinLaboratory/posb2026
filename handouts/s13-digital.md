<!--
title: Session 13 — Four problems, and the scaffolding falls away
subtitle: Gates, thresholds and the price of a switch. Start wherever the scaffolding stops helping you.
session: 13
-->

# Four problems, and the scaffolding falls away

A repressor gate, input $x$ and output $y$, both as concentrations:

$$y(x) = y_{\min} + \frac{y_{\max} - y_{\min}}{1 + (x/K)^{n}}$$

**Today's three tools, and nothing else.** The gain is the log slope, and for
this gate

$$G = \frac{d\ln y}{d\ln x}, \qquad
|G| = g\,\frac{y - y_{\min}}{y}, \qquad
g = \frac{n\,u^{n}}{1+u^{n}}, \quad u = \frac{x}{K}.$$

The two solutions of $|G| = 1$ are the input thresholds $x_{IL} < x_{IH}$, and
they name the worst-case output levels
$y_{OH} = y(x_{IL})$ and $y_{OL} = y(x_{IH})$. When gate A drives gate B,

$$\mathrm{NM_L} = \log_{10}\frac{x_{IL}(B)}{y_{OL}(A)}, \qquad
\mathrm{NM_H} = \log_{10}\frac{y_{OH}(A)}{x_{IH}(B)},$$

and both must be positive. At each transition this sheet asks *why does that
step follow?* Answer in writing before you go on.

---

## 1 — Fully worked: one gate, $n = 2$

<div class="q" markdown="1">

Take $K = 1$, $y_{\min} = 0.1$, $y_{\max} = 10$ (so a hundredfold swing).
Setting $|G| = 1$ and solving numerically:

$$x_{IL} = 1.02, \qquad x_{IH} = 9.80,$$

$$y_{OH} = y(1.02) = 4.95, \qquad y_{OL} = y(9.80) = 0.20.$$

**How those two roots were found**, since $|G| = 1$ does not factor: evaluate
$|G|$ on a grid of $x$, find where it peaks (here $|G| = 1.64$ at $x = 3.2$),
and then bisect on each side of the peak for the crossing. That is what
`posb.digital.Repressor.thresholds` does, and it raises an error rather than
returning numbers when the peak never reaches 1.

Those four numbers are the gate's datasheet. *Why does that step follow?* —
the peak $|G|$ is above 1, so $|G| = 1$ has two roots. A gate whose peak gain
never reached 1 would have none, and no digital reading at all.

</div>

## 2 — One step given: the same gate at $n = 3$

<div class="q" markdown="1">

Same $K$, same $y_{\min}$ and $y_{\max}$, cooperativity 3 instead of 2. The
peak $|G|$ is now 2.45, at $x = 2.15$, and $x_{IL} = 0.80$ is given.

$$x_{IH} = \underline{\phantom{000000}}
\qquad\text{(it is between 5 and 6)}$$

$$y_{OH} = y(x_{IL}) = \underline{\phantom{000000}}, \qquad
y_{OL} = y(x_{IH}) = \underline{\phantom{000000}}$$

<div class="rule"></div>

*Why does that step follow?* — compared with item 1, did the band between the
thresholds get wider or narrower, and is that good or bad for a designer?

<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## 3 — Nothing given: does this pair connect?

<div class="q" markdown="1">

Gate A is item 1's gate, $n = 2$. Gate B is item 2's gate, $n = 3$ — same $K$,
same leak, sharper. **A drives B.** Use your own numbers from items 1 and 2.

$$\mathrm{NM_L} = \log_{10}\frac{x_{IL}(B)}{y_{OL}(A)}
= \log_{10}\frac{\underline{\phantom{000000}}}{\underline{\phantom{000000}}}
= \underline{\phantom{000000}}$$

$$\mathrm{NM_H} = \log_{10}\frac{y_{OH}(A)}{x_{IH}(B)}
= \log_{10}\frac{\underline{\phantom{000000}}}{\underline{\phantom{000000}}}
= \underline{\phantom{000000}}$$

<div class="rule"></div>

One of the two fails, and only just. You may change A's ribosome binding site,
which multiplies $y_{\min}$ and $y_{\max}$ by the same factor $f$. What range
of $f$ makes both margins positive?

$$f \text{ from } \underline{\phantom{000000}}
\text{ to } \underline{\phantom{000000}}$$

<div class="rule"></div>

*Why does that step follow?* — say in one sentence why changing A's RBS does
not move A's own thresholds.

<div class="rule"></div>
<div class="rule"></div>

</div>


<div class="pagebreak"></div>

## 4 — Bare problem: a sensor that must read four decades

<div class="q" markdown="1">

A collaborator wants a reporter whose output tells them the inducer
concentration anywhere from 1 nM to 10 µM — four decades — not merely whether
it is above or below a threshold.

Explain why no single Hill-type promoter can do this, using a number. Then name
a change to the circuit that would widen the usable range, and say which
saturation your change removes.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

**If you finish early.** Your gate from item 2 has $n = 3$. Over what fold-range
of input is it a usable analog sensor, and how does that compare with item 1's
gate?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>
