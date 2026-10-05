<!--
title: Session 12 — Board notes
subtitle: Thursday's leftovers on the slides; the ladder, the exponential and the live code are the board's.
session: 12
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written*, and what gets *typed*.

**Three board moments.** The ladder at step 6 of the master equation, which is
where something disappears. The exponential at step 2 of Gillespie. And the
live code, which is the board for five minutes.

**Conventions.** **ASK**: put it to the room before writing, and the answer to
expect. **POINT**: turn and point at the board rather than the screen.
**IF ASKED**: the question that always comes.

<div class="rule"></div>

## Before class, left wing: Thursday's two numbers

Leave these up from the start. The first six surfaces finish Thursday and lean
on them.

$$g = \frac{n\,x^{n}}{1+x^{n}} = 2 \qquad\qquad \alpha_c = \left(\frac{2}{n-2}\right)^{1/n}\frac{n}{n-2}$$

Underneath, smaller: **a clock needs gain and delay.**

<div class="rule"></div>

## Right wing, minutes 25–31: the group answers

Draw a square with its diagonal. Write each group's answer **where it moves a
point**: shared causes (polymerase, ribosomes, cell size, LacI) along the
diagonal; private causes (which polymerase arrived, when an mRNA decayed) across
it.

**ASK at 31, before the sorted surface:** *which of these would still be there
with a perfect microscope?* All of them. Uncorrelated measurement error would
also spread points across the diagonal and pass for intrinsic noise, which is
why Elowitz checked that the two colours had equivalent intensity
distributions before measuring anything (p. 1184).

<div class="rule"></div>

## Centre, at 36: the ladder

The run is projected. **Draw the ladder** beside it, because it is a picture and
the slide has it as symbols.

Rungs $0, 1, 2, 3, \ldots$ stacked vertically. Between each pair, an up-arrow
labelled $k$ and a down-arrow labelled $\gamma n$ (with the $n$ of the upper
rung). Then write, at step 5:

$$J_n = k\,P_{n-1} - \gamma n\,P_n$$

**At step 6, POINT at the bottom rung.** Say: there is nothing below zero, so no
traffic can cross the floor. $J_0 = 0$. Steady state makes every $J$ equal, so
every $J$ is zero. **ASK:** *what does $J_n = 0$ let you do with $P_n$?* Solve for
it from the rung below. Then climb:

$$P_1 = \frac{k}{\gamma}P_0, \quad P_2 = \frac{k}{2\gamma}P_1, \quad
P_3 = \frac{k}{3\gamma}P_2 \quad\Longrightarrow\quad
P_n = P_0\frac{(k/\gamma)^n}{n!}$$

Let the factorial appear on its own. **IF ASKED** why $P_0 = e^{-k/\gamma}$: the
probabilities sum to one, and $\sum (k/\gamma)^n/n!$ is the series for
$e^{k/\gamma}$.

<div class="rule"></div>

## Centre, at 49: the exponential

At Gillespie step 2, write:

$$\Pr(\text{no event in } \tau) = (1 - a_0\,dt)^{\tau/dt} \;\longrightarrow\; e^{-a_0\tau}$$

**ASK:** *who has seen this before?* Radioactive decay, a Poisson process, a
memoryless wait. Then invert it: $u = e^{-a_0\tau}$, so $\tau = -\ln u / a_0$.

**CHECK out loud:** a bigger $a_0$ gives a shorter wait. If the code divides by
$a_0$ where it should, that is what it does.

<div class="rule"></div>

## Live code, at 53: type this

Into a fresh notebook cell, projected. Type it, do not paste it. The room
should see it built.

```python
import numpy as np
rng = np.random.default_rng(0)
k, g, T = 10.0, 1.0, 5000.0
t, n = 0.0, 0
ts, ns = [0.0], [0]
while True:
    a = np.array([k, g * n])
    a0 = a.sum()
    tau = -np.log(rng.random()) / a0
    if t + tau > T:
        break
    t += tau
    n += 1 if rng.random() * a0 < a[0] else -1
    ts.append(t); ns.append(n)
ts, ns = np.array(ts), np.array(ns)
dt = np.diff(np.append(ts, T))           # how long each state was held
keep = ts > 10                           # drop the climb from n = 0
m = np.sum(ns[keep] * dt[keep]) / dt[keep].sum()
v = np.sum((ns[keep] - m) ** 2 * dt[keep]) / dt[keep].sum()
m, v
```

**Expect** both near 10 (seed 0 gives 10.03 and 9.91, in under a second). **Then run** `ns[keep].mean()` and show it comes out
near 10.5 (seed 0: 10.53). **ASK:** *why too high?* A state with more molecules has a higher
total rate $k + \gamma n$, so it is left sooner and logged more often per unit
time. The event-weighted mean is
$\langle n(k+\gamma n)\rangle / \langle k+\gamma n\rangle = 210/20 = 10.5$
exactly.

**If late:** skip the event-average comparison and say it in one sentence. Do
not skip the time weighting.

<div class="rule"></div>

## Centre, at 58: the rule, calibrated

Write the rule before the NAR run uses it, and check it on the case already
solved:

$$\sigma^2 = \frac{\text{noise in}}{2 \times \text{return rate}}
\qquad\text{constitutive:}\quad \frac{k + \gamma n}{2\gamma} = \frac{2k}{2\gamma} = \frac{k}{\gamma}\;\checkmark$$

Then underneath, for self-repression at the same mean:

$$\frac{2\gamma x}{2\gamma(1+g)} \quad\Longrightarrow\quad \text{Fano} = \frac{1}{1+g}$$

**POINT** at the left wing: that $g$ is Thursday's $g$.

<div class="rule"></div>

## What to cut if you are late

In this order, last first:

1. The Becskei slide's fine print. Keep the number, say "measured during a
   transient" in one breath.
2. The event-average half of the live code.
3. Item 4 on the handout. Items 1–3 cover T31, T35 and T17.

**Never cut** the sweep surface (PS5 Q5a–b is due Thursday), the ladder, or the
NAR run (T17 is owed to PS6 and has no other demonstration).
