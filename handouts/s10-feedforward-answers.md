<!--
title: Session 10 — Four problems, answers
subtitle: Posted after class. Every number here is computed in figures/s10_feedforward.py.
session: 10
-->

# Four problems — answers

## 1 — Classify by sign

The rule: sign of the direct path $X \to Z$, against the **product** of the signs
along $X \to Y \to Z$. Same → coherent; opposite → incoherent.

**Now you:** $X \xrightarrow{-} Y$, $Y \xrightarrow{+} Z$, $X \xrightarrow{+} Z$.

Direct $+$; indirect $(-)(+) = -$. Opposite, so **incoherent**. With $X$
repressing $Y$ and both $X$ and $Y$ activating $Z$, this is **incoherent type 4**
in Mangan & Alon's numbering — their own words, p. 11982: *"in the type 4
incoherent FFL, when $S_x$ turns on, $Z$ is first induced by the joint action of
$X$ and $Y$. Meanwhile, $Y$ production is repressed by $X$."* Their Table 2
records it as rare — 1 in *E. coli*, 0 in yeast — and gives the reason: with an
AND gate its steady-state output responds to *neither* $S_x$ nor $S_y$, so it has
less function than types 1 and 2, which respond to both.

Note what it *is* good at, because it is the opposite of what the abundance
suggests: Table 2 marks type 4 as the only **strong** pulser on an $S_x$
on-step, where type 1 is marked *weak*. Rare in nature, useful in a design.

## 2 — The delay table

$t_D = \ln\!\left[\dfrac{Y_{\max}-Y_{\min}}{Y_{\max}-K_{yz}}\right]$ with
$Y_{\max}=1$, $Y_{\min}=0$, so $t_D = \ln\!\left[\dfrac{1}{1-K_{yz}}\right]$.

| $K_{yz}$ | formula | simulated at $H=2$ | OFF step |
|---|---|---|---|
| $0.2$ | $\ln 1.25 = 0.23$ | $0.35$ | $0$ |
| $0.5$ | $\ln 2 = 0.69$ | $0.75$ | $0$ |
| $0.8$ | $\ln 5 = 1.61$ | $1.02$ | $0$ |

The OFF-step delay is $0$ in every row, and that is not an approximation: the
measured value is $-0.0000$ lifetimes. With an AND gate, removing $X$ opens the
gate immediately no matter what $Y$ is doing, so the FFL and the simple circuit
fall on exactly the same curve.

**Why the formula fails at $K_{yz} = 0.8$.** It **overestimates**, 1.61 against
1.02 — and notice it errs the *other* way at $K_{yz}=0.2$ (0.23 against 0.35).
The error is not a consistent offset, so it is not a fudge factor you can carry.

What it is: the formula is the **sharp-gate limit**. It assumes $Z$ is strictly
off until $Y$ crosses $K_{yz}$, which is only true for $H \gg 1$. Raising $H$ in
the simulation drives every row onto the formula — at $H = 40$ all three agree to
within $0.04$ lifetimes — so the whole discrepancy is gate softness and nothing
else.

At $H = 2$ the gate leaks. $f(Y, K_{yz})$ is a few percent open even when $Y$ is
well below $K_{yz}$, and because we matched the two circuits to the same steady
state, the FFL's $Z$ promoter is strong enough that a few percent is enough to
start it climbing. That leak is what shortens the wait at large $K_{yz}$, where
the formula is predicting a very long one.

The design reading, and it is the one worth carrying: **a threshold is only as
good as it is sharp, and sharpness is cooperativity.** The parameter that opened
the toggle's wedge on Thursday is the same parameter that decides whether a delay
you designed on paper is the delay you get.

**The OR gate.** The delay moves to the **OFF step**, and the ON step becomes
immediate. With OR, either input alone turns $Z$ on, so an ON step of $X$ fires
$Z$ at once; on an OFF step $Z$ stays up until $Y$ has decayed below its
threshold. Mangan & Alon, Table 1: the FFL's functions survive the swap, with the
sign sensitivity reversed.

<div class="pagebreak"></div>

## 3 — The adaptation error

Integrating the incoherent type-1 with $B_y = 0.4$, $K_{yz} = 0.5$,
$\beta_z = 6$, stepping $X$ from $0$ to $1$:

- **peak** $= 1.099$, reached at $t = 1.07$ lifetimes
- **final** $= 0.681$
- **adaptation error** $= 0.681 / 1.099 = \mathbf{0.62}$

**The two instruments.** An adaptation error near $0$ is a circuit that returns
almost to where it started even though the input is still on: it reports *change*
and is blind to level. That is what bacterial chemotaxis does, and it is why a
cell swimming up a gradient responds to getting better rather than to being in a
good place. An error near $1$ barely pulsed at all: it reports *level*, and the
incoherent wiring has bought only a faster approach to it. Both are useful; you
have to say which one you are building, because the same three genes give you
either depending on $B_y$ and the strength of the repression.

## 4 — The design problem

**Two answers are defensible, and the difference between them is the whole
item.** Both are coherent, both take an AND gate, and Mangan & Alon's Table 1 —
projected at minute 28 — records both as delaying the $S_x$ on-step and neither
as delaying the off-step. The incoherent types are out: they respond immediately
and then adapt.

**Answer A: coherent type 1 with an AND gate.** The delay you derived in item 2
*is* a persistence filter: the output fires only if the input stays on longer
than $t_D$, because a shorter pulse never lets $Y$ *rise* to $K_{yz}$.

Lifetimes are near 30 minutes, so one hour is $t_D \approx 2$ lifetimes. Setting
$\ln[1/(1-K_{yz})] = 2$ gives

$$K_{yz} = 1 - e^{-2} = 0.865,$$

i.e. put $Y$'s operator at about 87% of $Y$'s maximum level — a weak-affinity
site on the $Y \to Z$ arm.

**And answer A does not reach an hour, which is half the point of the item.**

Item 2 already warned that the formula overestimates in this regime. Simulate
$K_{yz}=0.865$ at $H=2$ and the delay is **1.06** lifetimes, about half an hour,
not one. Push the threshold higher and it barely moves: $0.90 \to 1.08$,
$0.95 \to 1.11$, $0.99 \to 1.13$. **The delay saturates near 1.1 lifetimes, and
no value of $K_{yz}$ reaches 2.** You cannot buy an hour by moving the operator,
because the leak through a soft gate sets a ceiling the threshold cannot raise.

The obvious second knob fails too, but not for the reason you would guess.
Slowing $Y$ looks like it should stretch the delay, since $\alpha_y^{-1}$ sits in
front of the formula — but $\alpha_y$ also sets the ceiling, $Y_{\max} =
\beta_y/\alpha_y$, so a longer-lived $Y$ climbs past $K_{yz}$ *sooner relative to
its own scale*. The two effects nearly cancel. At $K_{yz} = 0.865$ the measured
delay goes $1.06 \to 1.23 \to 1.25$ for $\alpha_y = 1, 0.5, 0.25$ — a 17%
gain, not the doubling the prefactor promises. The sharp-gate formula, with
$Y_{\max}$ tracking $\alpha_y$, actually predicts the delay *falls*: $2.07 \to
1.15 \to 0.99$. Slow $Y$ down and you must raise $K_{yz}$ in step, and then you
are back at the same ceiling.

**What works is sharpening the gate.** Holding $K_{yz} = 0.8$ and raising the
cooperativity of the $Y \to Z$ interaction: $H=2 \to 1.02$, $H=4 \to 1.41$,
$H=6 \to 1.60$, $H=10 \to 1.73$. To specify an hour you need a cooperative
**activator** at $Y$'s site on the $Z$ promoter — a dimer, or a pair of binding
sites. Note that none of the numbers above reaches 2 on its own: the combination
that does is $H = 10$ with $K_{yz} = 0.865$, giving $t_D = 2.01$ lifetimes. By
then the formula is telling the truth, so you can place $K_{yz}$ from it rather
than by search.

**Answer B: coherent type 4 with an AND gate — and this one hits the hour at
$H = 2$.** You have already classified this wiring: it is item 1(c). $X \dashv Y$,
$Y \dashv Z$, $X \to Z$. Now the delay is built on the *other* side of the
threshold. When $X$ turns on, $Y$ stops being made and *decays* past $K_{yz}$,
and only then is $Z$ released. So

$$t_D = \alpha_y^{-1}\ln\!\left[\frac{Y_{\max}}{K_{yz}}\right],$$

which runs to infinity as $K_{yz} \to 0$ instead of hitting a wall at
$Y_{\max}$. There is no ceiling to saturate against, and the soft gate no longer
fights you — it is working on a decaying exponential, not on the approach to a
plateau. Simulated at $H = 2$ with the same parts:

| $K_{yz}$ | 0.5 | 0.2 | **0.168** | 0.1 | 0.05 |
|---|---|---|---|---|---|
| $t_D$ (on) | 0.91 | 1.82 | **2.00** | 2.56 | 3.35 |
| $t_D$ (off) | 0 | 0 | **0** | 0 | 0 |

$K_{yz} \approx 0.17$ gives exactly one hour at 30-minute lifetimes, with the
shut-off still immediate. No cooperative activator required.

**The design reading, and it is the point of the item.** Both circuits delay.
What separates them is *which side of the threshold the delay is built on*:

- Type 1 waits for $Y$ to **climb** to $K_{yz}$. The climb is bounded by
  $Y_{\max}$, so the threshold you can usefully set is bounded too, and a soft
  gate leaks before you get there. **Cooperativity is a prerequisite.**
- Type 4 waits for $Y$ to **fall** past $K_{yz}$. A decaying exponential has no
  floor, so the threshold can go as low as you can build it. **Cooperativity is
  a luxury.**

That is a sharper statement than "you need a cooperative repressor," and it
generalizes: whenever a timer is built out of a concentration crossing a
threshold, ask whether it is approaching a ceiling or leaving one. Thursday's
engineerability conclusion still stands for type 1 — the parameter the design
most depends on is the one you buy by choosing a protein — but the right
first move is to check whether you have to be in that regime at all.

*Marking:* full credit for either answer, argued. A student who reaches type 4
and sees why it escapes the ceiling has done something this session did not do
from the front, and should be told so. A student who answers type 1 and reports
the ceiling honestly has done exactly what item 2 trained them to do.

**Why you rarely see type 4 in the wild.** Mangan & Alon count 1 in *E. coli*
and 0 in yeast, against 28 and 26 for type 1. Their argument is evolutionary,
not engineering (p. 11984): types 3 and 4 need $X$ to act with opposite signs on
$Y$ and $Z$, which is "well established" as biologically feasible but leaves the
circuit with less steady-state function. Rare is not the same as unbuildable,
and this is a course about building.

One part of the specification is free in both answers: with an AND gate the
shut-off is immediate, which is what was asked. An OR gate would have given you a
circuit that fires instantly and lingers — the exact opposite, from the same
three genes.
