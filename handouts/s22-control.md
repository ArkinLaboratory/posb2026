<!--
title: Session 22 — Robustness and control
subtitle: A home guide, worked after class. Item 1 is the controller we did not build and why it is not enough; item 2 is what the annihilation really is once a molecule has to do it; item 3 is their evidence and what the controller does not pin; item 4 is the ladder. Answers come on a separate sheet.
session: 22
-->

# How to use this

Work it after class, on paper, before you touch PS8 Q4 and Q5. The answers are
on a separate sheet — read them **after** you have written something down, not
instead of writing something down.

These are the questions class did not have time for. Work them before you
start PS8 — they set up the same machinery from a different angle.

---

## 1. Why proportional feedback is not enough

Class derived that a controller obeying

$$\frac{du}{dt} = \mu - \theta X$$

drives the error to exactly zero, whatever plant it is attached to. The
obvious simpler thing to try is **proportional** feedback — make the input
depend on the error directly rather than on its accumulation:

$$u = \kappa\,(\mu/\theta - X)$$

Put this on session 5's plant, $\dot X = k u - \gamma X + d$.

**(a)** Solve for the steady state $X_{ss}$ with $d = 0$.

**(b)** Now with $d \neq 0$. How much does the output move?

**(c)** You want the offset small. The algebra says to make $\kappa$ large.
Give two reasons — one from this course, one from the plant — that you cannot
simply keep turning $\kappa$ up.

**(d)** In one sentence: what does the integrator have that the proportional
controller does not?

---

## 2. What the annihilation has to be

The motif's third reaction is $Z_1 + Z_2 \to \varnothing$ at rate $\eta Z_1 Z_2$.
Class treated $\eta$ as large and showed the steady state does not contain it.

**(a)** The derivation assumed $Z_1$ and $Z_2$ are lost **only** by
annihilating each other. List every other way a protein is actually lost in a
growing *E. coli* cell, and mark which of them remove $Z_1$ and $Z_2$ together,
one for one, and which remove them independently.

**(b)** Aoki implement the annihilation with SigW and RsiW — a σ factor and
its anti-σ factor — and the paper says RsiW "stably sequesters and holds SigW
inactive." A sequestration complex is not literally destroyed; it is bound.
Write the reaction they actually have, with a complex $C$ on the right.

**(c)** Under what condition on $C$ does your reaction in (b) behave like the
annihilation the derivation assumed? Name the condition, and name the session
where you first met the thing that violates it.

---

## 3. Reading their evidence

Aoki et al. 2019, Fig. 3d. They perturb temperature, 37 °C against 30 °C, and
measure each strain's growth rate normalised to its own 37 °C rate, $n = 3$.
Closed loop $P = 0.2261$; open loop $P = 7.769 \times 10^{-5}$.

**(a)** The closed-loop bars sit at 1.00 and 1.03; the open-loop ones at
1.00 and 0.33. Before any statistics: which of those two differences would you
have believed from the picture alone, and what does the picture not tell you?

**(b)** The open-loop strain is the closed-loop circuit with the anti-σ module
deleted. Say why that is a better control than (i) the same strain with no
circuit at all, and (ii) a strain with the anti-σ module replaced by an inert
protein of the same length.

**(c)** The controller holds the *mean* growth rate. Aoki report that the
closed loop showed **increased cell-to-cell variability** compared with the
open loop. Does that contradict the adaptation claim? Say what integral
feedback pins and what it does not.

**(d)** They replaced sfGFP with *metE* in a Δ*metE* host, so the regulated
output is the cell's growth rate. Why is that a harder test of the controller
than regulating a fluorescent protein? Give the reason in terms of what the
controller is now inside of.

---

## 4. The ladder

Four sessions, one reaction.

**(a)** For each of sessions 18, 19, 21 and 22, name the molecule that was
held and the thing that held it.

**(b)** On three of those four, the holding was a problem. On one it is the
mechanism of the cure. Write the one sentence that is true of all four, and
then say what changes sign in session 22.

**(c)** Part II's four devices each bought something and charged for it on a
different axis. Fill the fourth row:

| session | what you bought | what it cost |
|---|---|---|
| 19 | a budget you can hold to | measuring the burden, per construct |
| 20 | exact fluxes | an objective you had to import |
| 21 | a regulator that outruns its load | ? |
| 22 | ? | ? |
