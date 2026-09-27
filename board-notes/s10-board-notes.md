<!--
title: Session 10 — Board notes
subtitle: Thursday's ledger carries over. The delay convention is written once and stays up all period.
session: 10
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written*.

**This session is not a board session.** One derivation, on the split surface.
The board carries the **carried-over toggle lines** from Thursday, the **delay
convention**, and the **group answers** from the argument at 14–24.

**Conventions.** **ASK** — put it to the room before writing, and the answer to
expect. **POINT** — the moments you turn and point at the board rather than the
screen. **IF ASKED** — the question that always comes.

<div class="rule"></div>

## Before class — left wing, the two lines Thursday did not reach

Session 9 ran out at its slide 20, so the failure surface and the parameter
window are carried into the opening. Write these two before class:

$$\text{the wedge is finite} \qquad\qquad \text{failure} = \text{walking out of it}$$

Leave room underneath. The four failure mechanisms come from the room in the
first five minutes and get written there:

**mutation in a repressor · promoter mutation · plasmid loss · burden selecting
against the expressing state**

**ASK before writing any of them:** *a mutation that breaks the circuit, and
selection that breaks the population — are those the same problem?* They are
not, and they need different fixes: sequence redundancy against the first,
lower burden against the second. That distinction is the one to get on the
board, not the list.

<div class="rule"></div>

## Centre — the delay convention, written once, stays up all period

This is the T25 specification and it is on the handout. Write it in full, and
**do not erase it** — the faded set at 63 refers back to it and PS5 marks it.

$$t_{1/2} : \; Z \text{ reaches } 50\% \text{ of its steady state}$$

$$t_D \;=\; t_{1/2}(\text{FFL}) \;-\; t_{1/2}(\text{simple, same steady state})$$

**POINT at it twice:** once when the derivation reaches step 3, and again at 63
when you send them to the handout.

**ASK when you write it:** *why does the comparison circuit have to reach the
same steady state?* Because otherwise you are timing two different journeys —
half of a big number and half of a small one are not comparable, and the
difference would be an artifact of the destination rather than the route.

<div class="rule"></div>

## Right wing — minutes 14–24, the group answers

Three columns, one per question, answers **by group name**. You read them back
at 24 and sort them into the three rows of the next surface. Do not sort while
writing.

Expect column 1 to be easy (the CI arm is slow) and column 3 to be the hard
one. If no group gets column 3, do not supply it — the sorted slide's third row
is where it lands, and the figure does the arguing.

**ASK at 24, before sorting:** *did anyone's answer to 3 use the word rate
rather than the word amount?* That is the distinction the whole result turns on,
and naming the group that said it first is worth more than saying it yourself.

<div class="rule"></div>

## During the derivation — the two lines that go on the board

The run is on the split surface, so the board takes only what has to survive it.

**At step 3, write:**

$$t_D = \alpha_y^{-1}\ln\!\left[\frac{Y_{\max}-Y_{\min}}{Y_{\max}-K_{yz}}\right]
\qquad = \ln 2 \approx 0.7 \text{ at } K_{yz} = \tfrac12$$

**CHECK out loud:** put $K_{yz} \to Y_{\max}$ in your head — the log blows up,
so the delay is unbounded as the threshold approaches $Y$'s ceiling. Say that it
is *the formula* that blows up, and that the handout asks whether the circuit
does. It does not, and that is item 4.

**At step 4, write:**

$$\text{OFF step}: \quad t_D = 0$$

**POINT** at the two together. The asymmetry is the session's result and it
should be visible in one glance.

**IF ASKED — "is the formula exact?"** No, and the handout makes that the
question. It is the sharp-gate limit; at $H = 2$ it is wrong in both directions,
and raising $H$ drives the simulation onto it. Do not give the numbers away —
they are on the handout and on PS5.

<div class="rule"></div>

## If a group reaches type 4 on item 4 — and someone will

They are right, and it is the better answer. Do not wave it away and do not work
it at the front; send them to the answer sheet afterwards. What to say, in one
sentence, and it is worth writing on the board:

$$\text{type 1: } Y \text{ CLIMBS to } K_{yz} \;\;(\text{bounded by } Y_{\max})
\qquad
\text{type 4: } Y \text{ FALLS past } K_{yz} \;\;(\text{unbounded})$$

**POINT** at the two and say: a timer built on an approach to a ceiling has a
ceiling; a timer built on a decay does not. Type 4 hits the hour at $H = 2$ with
$K_{yz} \approx 0.17$, no cooperativity needed. That is the item.

<div class="rule"></div>

## Ledger — add to the running list, right-hand column

$$\boxed{\;t_D \text{ and its convention} \;\cdot\; \text{adaptation error} = Z_{\text{final}}/Z_{\text{peak}}\;}$$

Two entries. The adaptation error goes up at 45, when the number surface is on
the screen, and stays for the handout.

<div class="rule"></div>

## Closing — the one line to leave up

$$\text{coherent} \Rightarrow \text{delay} \qquad
\text{incoherent} \Rightarrow \text{pulse, adapt, accelerate} \qquad
\text{all of it, one direction only}$$

Leave it. Thursday's retrieval opens against it.
