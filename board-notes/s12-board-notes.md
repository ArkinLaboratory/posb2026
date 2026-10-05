<!--
title: Session 12 — Board notes
subtitle: Thursday's leftovers on the slides; the ladder, the exponential, the live code and the return rate are the board's.
session: 12
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written*, and what gets *typed*.

**Four board moments.** The ladder, drawn beside the master-equation run — the
picture the slide has only as symbols. The exponential, at step 3 of Gillespie.
The live code. And the one-line calibration of the variance rule, before the
feedback run spends it.

**Conventions.** **ASK**: put it to the room before writing, and the answer to
expect. **POINT**: turn and point at the board rather than the screen.
**IF ASKED**: the question that always comes.

<div class="rule"></div>

## Before class, left wing: Thursday's two numbers

Leave these up from the start. The first six surfaces finish Thursday and lean
on them.

$$g = \frac{n\,u^{n}}{1+u^{n}} = 2, \quad u = \frac{x}{K}
\qquad\qquad \alpha_c = \left(\frac{2}{n-2}\right)^{1/n}\frac{n}{n-2}$$

Session 11 wrote this with $x$, because its $x$ was already in units of $K$.
Today's $x$ is a molecule count, so the $u$ is not decoration: at a mean of 100
with $K = 100$, $u = 1$ and $g = 1.5$ at $n = 3$, where reading $x$ literally
would give 3.

Underneath, smaller: **a clock needs gain and delay.**

<div class="rule"></div>

## Right wing, minutes 23–29: the group answers

Draw a square with its diagonal. Write each group's answer **where it moves a
point**: shared causes (polymerase, ribosomes, cell size, LacI) along the
diagonal; private causes (which polymerase arrived, when an mRNA decayed) across
it.

The scatter is on the screen this time, with its two directions marked **A**
(along the diagonal) and **B** (across it) and deliberately not named. Write
their names when the room supplies them, not before.

**ASK at 29, before the sorted surface:** *which of these would still be there
with a perfect microscope?* All of them — but note what the plot cannot do:
uncorrelated read noise in the two channels also spreads points across the
diagonal and is counted as intrinsic. Nothing on this scatter separates the
two, which is why the noise floor has to be measured separately (their
supplement). What the main text does report is the prerequisite for the
estimator at all: the two reporters gave statistically equivalent intensity
distributions (p. 1184).

<div class="rule"></div>

## Centre, 37–47: the ladder

The run is projected, in two parts: **37–42 builds** the equation and **42–47
solves** it. **Draw the ladder** beside it at the start, because it is a picture
and the slide has it as symbols, and leave it up across both parts.

Rungs $0, 1, 2, 3, \ldots$ stacked vertically. Between each pair, an up-arrow
labelled $k$ and a down-arrow labelled $\gamma n$ (with the $n$ of the upper
rung). Then write, at part one's step 5:

$$J_n = k\,P_{n-1} - \gamma n\,P_n$$

**Part one's step 6 is the half-minute that buys the rest.** Expand
$J_n - J_{n+1}$ on the board and show it reproduces the master equation term for
term. The biologists need to see it is the same equation rewritten, not a new
one.

**Part one ends with $J$ unknown.** Before turning the surface, **ASK:** *what
could possibly pin that constant down?* Fish for the end of the ladder.

**At part two's step 1, POINT at the bottom rung.** Nothing below zero, so no
traffic can cross the floor: $J_0 = 0$, and steady state has already made every
$J$ equal, so every $J$ is zero. **ASK:** *what does $J_n = 0$ let you do with
$P_n$?* Solve for it from the rung below. Then climb:

$$P_1 = \frac{k}{\gamma}P_0, \quad P_2 = \frac{k}{2\gamma}P_1, \quad
P_3 = \frac{k}{3\gamma}P_2 \quad\Longrightarrow\quad
P_n = P_0\frac{(k/\gamma)^n}{n!}$$

Let the factorial appear on its own. **IF ASKED** why $P_0 = e^{-k/\gamma}$: the
probabilities sum to one, and $\sum (k/\gamma)^n/n!$ is the series for
$e^{k/\gamma}$.

**IF ASKED where the variance comes from without quoting the Poisson** — and it
is the best question in the hour — multiply the master equation by $n$ and sum
over all $n$. The $\langle n^2\rangle$ terms cancel between the birth and death
sums:

$$\frac{d\langle n\rangle}{dt} = k - \gamma\langle n\rangle$$

which is session 5's ODE, recovered as a statement about an average. Do it again
with $n^2$ and the $\langle n^3\rangle$ terms cancel, leaving
$2\gamma\langle n^2\rangle = 2k\langle n\rangle + k + \gamma\langle n\rangle$,
so $\sigma^2 = k/\gamma$. **Say that the hierarchy closing is special to a
LINEAR birth–death** — it is the honest reason the feedback run later has to
borrow an approximation. It is worked on the answer sheet.

<div class="rule"></div>

## Centre, at 50: the exponential

At Gillespie step 3, write:

$$\Pr(\text{no event in } \tau) = (1 - a_0\,dt)^{\tau/dt} \;\longrightarrow\; e^{-a_0\tau}$$

**ASK:** *who has seen this before?* Radioactive decay, a Poisson process, a
memoryless wait. **Then say the sentence that is the whole explanation:** between
events nothing about the system changes, so the chance of something happening in
the next instant is the same instant after instant. A process that forgets how
long it has already waited can only have an exponential wait. The exponential is
not a modelling choice here; it is forced.

Then invert it: $u = e^{-a_0\tau}$, so $\tau = -\ln u / a_0$.

**CHECK out loud:** a bigger $a_0$ gives a shorter wait. If the code divides by
$a_0$ where it should, that is what it does.

<div class="rule"></div>

## Live code, at 54: type this

Into a fresh notebook cell, projected. Type it, do not paste it. The room
should see it built.

```python
import numpy as np
rng = np.random.default_rng(0)
k, gam, T = 10.0, 1.0, 5000.0
t, n = 0.0, 0
ts, ns = [0.0], [0]
while True:
    a = np.array([k, gam * n])
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

## Centre, at 57: the rule, calibrated

Write the rule before the feedback run spends it, and check it on the case
already solved. Define the return rate **first**, in one line, because it is the
only new object in the run:

$$\text{kick it by } \Delta: \quad \frac{d\Delta}{dt} = -r\,\Delta
\quad\Longrightarrow\quad \Delta \sim e^{-rt}$$

so $1/r$ is how long a fluctuation *lasts*. Then:

$$\sigma^2 = \frac{\text{noise in}}{2 \times \text{return rate}}
\qquad\text{constitutive:}\quad \frac{k + \gamma n}{2\gamma} = \frac{2k}{2\gamma} = \frac{k}{\gamma}\;\checkmark$$

Then underneath, for self-repression at the same mean:

$$\frac{2\gamma x}{2\gamma(1+g)} \quad\Longrightarrow\quad \text{Fano} = \frac{1}{1+g}$$

**POINT** at the left wing: that $g$ is Thursday's $g$.

<div class="rule"></div>

## What to cut if you are late

In this order, last first:

1. The second Becskei surface's arithmetic. Keep the threefold — it is the
   chromosomal control, which is not the transient one — and keep the sentence
   that their "stability" is our return rate. Drop the $\sqrt{2}$ comparison.
2. The event-average half of the live code.
3. Item 4 on the handout. Items 1–3 cover T31, T35 and T17 — but item 4 is the
   only student practice on the sum of squares before PS6, so say the identity
   out of the deck rather than leaving it stated and unused.

**Never cut** the sweep surface (PS5 Q5a–b is due Thursday), the ladder, or the
NAR run (T17 is owed to PS6 and has no other demonstration).
