<!--
title: Session 22 — Robustness and control
subtitle: A home guide, worked after class. Item 1 is the controller we did not build and why it is not enough; item 2 is what the annihilation really is once a molecule has to do it; item 3 is their evidence and what the controller does not pin; item 4 is the sequestration thread across four sessions. Answers come on a separate sheet.
session: 22
-->

# How to use this

Work it after class, on paper, before you touch PS8 Q4 and Q5. The answers are
on a separate sheet — read them **after** you have written something down, not
instead of writing something down.

Some of this we work in class and some of it we do not reach. Either way,
do it again here with the answers beside you — recalling something a day
later is what makes it stick, which is the whole reason these go out after
the session rather than during it. Work them before you start PS8.

**The symbols, once, so they mean the same thing on every page.** $X$ is the
output — the thing the circuit is built to hold steady. $u$ is the controller's
action on it, and in the antithetic circuit $u$ **is** a molecule: $u = Z_1$.
Keep those two joined, because the fact that an action has to be made of
something is half of item 1. $Z_2$ is the anti-$Z_1$ species, produced in
proportion to the output. $\mu$ is the rate $Z_1$ is made at, $\theta$ the rate
the output drives $Z_2$ at, so $\mu/\theta$ is the set point. $k$ is the plant
gain — how hard $u$ moves $X$ — and $\gamma$ the rate the output decays at.
$d$ is a constant disturbance. $\eta$ is the rate $Z_1$ and $Z_2$ destroy each
other at, $\kappa$ the proportional gain of item 1, and $\delta$ the dilution
rate of the two controller species in item 3. Where a number is quoted below
it is at $\mu = 10$, $\theta = 2$, $k = 1$, $\gamma = 0.5$, $\eta = 50$ and a
disturbance of $d = 1$, which is the session's reference.

---

## 1. Why proportional feedback is not enough

Class derived that a controller obeying

$$\frac{du}{dt} = \mu - \theta X$$

drives the error to exactly zero — in any plant the controller can move and
can see, while the loop is stable and $Z_1$ has range left. The
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

The **antithetic** motif — $Z_1$ made at $\mu$, $Z_2$ made at $\theta X$, and
the two destroying each other — has a third reaction,
$Z_1 + Z_2 \to \varnothing$ at rate $\eta Z_1 Z_2$. Class showed the
**output's** steady state does not contain $\eta$ at all — not for large
$\eta$, but for every $\eta > 0$. The controller's own levels do contain it:
$Z_2$ falls as $1/\eta$. Hold on to that, because $\eta$ comes back in item 3
when the integrator leaks.

**(a)** The derivation assumed $Z_1$ and $Z_2$ are lost **only** by
annihilating each other. List every other way a protein is lost in a
growing *E. coli* cell, and mark which of them remove $Z_1$ and $Z_2$ together,
one for one, and which remove them independently.

**(b)** Aoki implement the annihilation with SigW and RsiW — a σ factor and
its anti-σ factor — and the paper says RsiW "stably sequesters and holds SigW
inactive." A sequestration complex is not destroyed; it is bound.
Write the reaction they have, with a complex $C$ on the right.

**(c)** Under what condition does your reaction in (b) behave like the
annihilation the derivation assumed? Your condition will involve both $C$ and
the unbinding rate, not $C$ alone. Then name the session where a complex that
*persists* was first a problem, and say in one clause what it was called
there.

---

## 3. Reading their evidence

Aoki et al. 2019, Fig. 3d. They perturb temperature, 37 °C against 30 °C, and
measure each strain's growth rate normalized to its own 37 °C rate, $n = 3$.
They compare each strain's 30 °C values against its 37 °C values with a
two-tailed unpaired *t*-test that does not assume equal variances. $P$ is the
probability of seeing a difference at least this large if both sets came from
the same distribution. Closed loop $P = 0.2261$; open loop
$P = 7.769 \times 10^{-5}$.

**(a)** The closed-loop bars sit at 1.00 and 1.03; the open-loop ones at
1.00 and 0.33. Before any statistics: which of those two differences would you
have believed from the picture alone, and what does the picture not tell you?

**(b)** The open-loop strain is the closed-loop circuit with the anti-σ module
deleted. (i) Say why that is a better control than the same strain with no
circuit at all. (ii) Now compare it with a strain whose anti-σ module is
replaced by an inert protein of the same length: which is the better control,
and on which axis? Say what each one does and does not hold fixed.

**(c)** The controller holds the *mean*. In their sfGFP circuit Aoki report
that the closed loop **tended to** show *more* cell-to-cell variability than
the open loop at steady state, and *less* cell-to-cell variability upon
perturbation. Does either of those contradict the adaptation claim? Say what
integral feedback pins and what it does not — and if you can, say why a
controller with no leak would be expected to do this.

**(d)** They replaced sfGFP with *metE* in a Δ*metE* host, and describe the
result as regulating the cell's growth rate. Why is that a harder test of the
controller than regulating a fluorescent protein? Give the reason in terms of
what the controller is now inside of — and say first what the loop actually
senses, because it is not growth rate.

---

## 4. The ladder — four sessions, one reaction

**(a)** For each of sessions 18, 19, 21 and 22, name the molecule that was
held and the thing that held it.

**(b)** On three of those four, the holding was a problem. On one it is the
mechanism of the cure. Write the one sentence that is true of all four, and
then say what changes sign in session 22.

**(c)** Part II's four devices each bought something and charged for it on a
different axis. Fill the three empty cells:

| session | what you bought | what it cost |
|---|---|---|
| 19 | a budget you can hold to | measuring the burden, per construct |
| 20 | exact fluxes | an objective you had to import |
| 21 | a regulator that outruns its load | ? |
| 22 | ? | ? |
