<!--
title: Session 4 — Board notes
subtitle: Every line to write, in order. Thirty-two minutes of board across five segments.
session: 4
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written*.

**Thirty-two minutes across five segments** — three of them consecutive, from
minute 8 to minute 30, and two late ones at 62 and 67.

**Conventions.** **ASK** — put it to the room before writing the next line, and
the answer to expect. **CHECK** — do it out loud; doing them is the habit being
taught. **IF ASKED** — the question that always comes. **CUT** — drop this first
if you are behind, decided now rather than at minute 70.

<div class="rule"></div>

## The board plan

Same room as session 3: blackboard across the front, screen down in the
**centre**, a **left wing** and a **right wing**.

**LEFT WING — the ledger. Written once at minute 20, never wiped.** Two lines,
and the session breaks without them:

$$v = \frac{V_{\max}[S]}{K_M + [S]}, \qquad
K_M \equiv \frac{k_{-1} + k_2}{k_1}, \qquad V_{\max} \equiv k_2 E_{\text{tot}}$$

Every one of ConcepTest 1 (34 min), the two figures (38–46) and the handout
debrief (58) points back at those definitions. The ConcepTest is unanswerable if
they have been erased — the whole question is *what are these two symbols made
of*.

**RIGHT WING — the workings, wiped between segments:** the nondimensionalisation,
the four steps of the derivation, the two clocks, the $81^{1/n}$ algebra, the
four-state column.

**Two lines to carry forward.** At minute 30, under the ledger on the **left
wing**, write and box both of these:

$$\frac{E_{\text{tot}}}{K_M + S_0} \ll 1
\qquad\text{and}\qquad E_{\text{tot}} \ll K_M + S_0$$

They are the same statement. The second is the projected slide at 30–34 min.
The 42-minute figure is a plot of that same group, so the room needs to be
looking at a symbol it derived rather than one that appeared on a slide.

<div class="rule"></div>

## 1 · 8–14 min — The small parameter

**Board 1 of 5 · 6 min · cumulative 6**

From Thursday's cascade, already on their notes:

$$\frac{dm}{dt} = \alpha - \gamma_m m, \qquad
\frac{dp}{dt} = k_p m - \gamma_p p, \qquad
\gamma_m = 0.5,\; \gamma_p = 0.05$$

> **ASK:** *Which is the fast variable, and how do you know without simulating?*
> Expect "mRNA, because $\gamma_m$ is bigger." Push once: bigger **than what**?
> The answer you want is that $\gamma_m/\gamma_p = 10$, a pure number.

**Nondimensionalise in front of them.** Do not show the scaled equations
finished — the point is watching the $\varepsilon$ appear.

$$\tau = \gamma_p t, \qquad \mu = \frac{m}{\alpha/\gamma_m}, \qquad
\pi = \frac{p}{k_p\alpha/\gamma_m\gamma_p}$$

Substitute. The mRNA equation becomes

$$\varepsilon\,\frac{d\mu}{d\tau} = 1 - \mu, \qquad
\frac{d\pi}{d\tau} = \mu - \pi, \qquad
\varepsilon \equiv \frac{\gamma_p}{\gamma_m} = 0.1$$

> **Say it while the chalk is still on the board:** $\varepsilon$ is the ratio of
> two clocks. It is not a statement about enzymes, or about concentrations, or
> about anything chemical.

**The sentence to land.** Setting $\varepsilon = 0$ does not say $dm/dt = 0$. It
says $dm/dt$ is small *compared with the terms in its own equation*, each of
which is order $\alpha$. Write both sides:

$$\frac{dm}{dt} = \underbrace{\alpha}_{\text{large}} - \underbrace{\gamma_m m}_{\text{large}}
\;=\; \text{small}$$

> **CHECK, out loud:** at $\alpha = 10$, $\gamma_m = 0.5$: the two terms are each
> about 10 and their difference is about 1. Small *because it is a difference of
> two big numbers*, not because nothing is happening.

**The lost initial condition.** A first-order equation had one; the algebraic
equation has none. $m$ jumps to $\alpha/\gamma_m$ instantly.

> **IF ASKED** *"so the approximation is just wrong at $t = 0$?"* — yes, and that
> is the honest answer. It is wrong for about $1/\gamma_m \approx 1.4$ min. It is
> a boundary layer; they will meet the words in a fluids course. The error you
> cannot remove lives there.

**CUT if behind:** the boundary-layer paragraph. Keep the two-big-numbers check.

<div class="rule"></div>

## 2 · 14–26 min — Michaelis–Menten, four named steps

**Board 2 of 5 · 12 min · cumulative 18**

Head the wing with the scheme:

$$\mathrm{E} + \mathrm{S} \;\underset{k_{-1}}{\overset{k_1}{\rightleftharpoons}}\;
\mathrm{ES} \;\overset{k_2}{\longrightarrow}\; \mathrm{E} + \mathrm{P}$$

**Ask for each step before you write it.** They can do 1 and 2 unaided; making
them produce those two is what buys attention for 3 and 4.

**Step 1 — QSSA on the complex.**

> **ASK:** *Which is the fast variable here, and what replaces its differential
> equation?* Expect ES. Then write:

$$k_1[\mathrm{E}][\mathrm{S}] = (k_{-1} + k_2)[\mathrm{ES}]$$

**Step 2 — enzyme conservation.**

> **ASK:** *What is conserved?* Someone will say "the enzyme." Write it, then
> name it: this is a **left null vector** of the stoichiometric matrix, from
> Thursday. Thirty seconds, and it connects two things they hold separately.

$$[\mathrm{E}] + [\mathrm{ES}] = E_{\text{tot}}$$

**Step 3 — eliminate $[\mathrm{E}]$.** Substitute and collect:

$$[\mathrm{ES}] = \frac{E_{\text{tot}}[\mathrm{S}]}{K_M + [\mathrm{S}]},
\qquad K_M \equiv \frac{k_{-1} + k_2}{k_1}$$

> **Slow down here.** $K_M$ is a **ratio of rate constants**. Half the room
> arrives believing $K_M$ is "the concentration at half $V_{\max}$" — which is a
> *consequence* of this definition, not the definition, and the difference bites
> the moment $k_2$ is not small.

**Step 4 — the rate.**

$$v = k_2[\mathrm{ES}] = \frac{V_{\max}[\mathrm{S}]}{K_M + [\mathrm{S}]},
\qquad V_{\max} \equiv k_2 E_{\text{tot}}$$

**Now move the two definitions to the LEFT WING and leave them there.**

> **CHECK, out loud:** units. $K_M = (k_{-1} + k_2)/k_1$ — s⁻¹ over M⁻¹s⁻¹ gives
> M. It *is* a concentration, and it is built entirely out of rate constants.

> **IF ASKED** *"isn't $K_M$ just $K_d$?"* — only when $k_2 \ll k_{-1}$. Then
> $K_M \to k_{-1}/k_1 = K_d$. Write that limit down; the gap between $K_M$ and
> $K_d$ when it fails is a real experimental headache and it saves an argument in
> session 6.

**Close the segment on the debt, not on the result:** step 1 was an
*assumption*, and nothing so far says when it is allowed.

**CUT if behind:** the $K_M \to K_d$ limit. Nothing later depends on it.

<div class="rule"></div>

## 3 · 26–30 min — Where the substrate goes

**Board 3 of 5 · 4 min · cumulative 22**

This segment pays the debt from segment 2. **It was rewritten on 7 September**:
the earlier version derived the condition from τ₁ ≪ τ₂, and that argument does
not survive checking. Holding $E_{\text{tot}}/(K_M+S_0)$ at 0.5 and driving
τ₁/τ₂ down three decades leaves the error pegged at 16%. Worse, the deck refuted
itself — slide 9's right panel has τ₁/τ₂ = 0.023, clocks separated 44-fold, and
Michaelis–Menten wrong by 15%. Clock separation is **necessary** and nowhere near
sufficient. What controls the error is substrate bookkeeping.

**First: there is a fast variable.** One line each, no derivation needed.

$$\tau_1 \approx \frac{1}{k_1(E_{\text{tot}} + K_M + S_0)}, \qquad
\tau_2 \approx \frac{K_M + S_0}{V_{\max}} = \frac{K_M + S_0}{k_2 E_{\text{tot}}}$$

> Note the $E_{\text{tot}}$ inside τ₁. The older slide dropped it and claimed the
> fast clock was independent of enzyme; that is only true once you have already
> assumed the answer, and at $E_{\text{tot}} = 1$ it is wrong by 46%.

> **Say it and move on:** you need τ₁ ≪ τ₂ or there is no fast variable to
> eliminate. It is necessary. It is also nearly free, and on its own it buys you
> almost nothing.

**Second, and this is the one that bites: where does the substrate go?**

> **ASK, and this is the question the segment exists for:** *the reduced model
> has one equation, for S. The full model has S and ES. Where did the substrate
> in ES go?*
> Expect a pause. The answer is that the reduced model has no account of it at
> all.

At quasi-steady state, and largest at the start:

$$[\mathrm{ES}] \;=\; \frac{E_{\text{tot}}\,S}{K_M + S}
\;\le\; \frac{E_{\text{tot}}\,S_0}{K_M + S_0}$$

**Demand that be negligible against the substrate you are tracking:**

$$\frac{E_{\text{tot}}\,S_0}{K_M + S_0} \;\ll\; S_0
\qquad\Longrightarrow\qquad
\boxed{\;\frac{E_{\text{tot}}}{K_M + S_0} \;\ll\; 1\;}
\qquad\text{i.e.}\qquad \boxed{\;E_{\text{tot}} \ll K_M + S_0\;}$$

One line. No bound, no bracket, no chain of inequalities — and it is the boxed
line on the next slide, which is why that slide now says "nothing new here."

> **CHECK, out loud:** the group is a *fraction of substrate*. That is what makes
> it dimensionless and that is why it is the thing the error scales with.

> **The number that makes it physical, and it is on the next figure:** at
> $E_{\text{tot}} = 1$, **35% of all the substrate is sitting in complex** at the
> peak. Michaelis–Menten is tracking the other 65% and calling it everything.
> That is the 15% error.

> **IF ASKED** *"so is the clock argument wrong?"* — no, it is incomplete. You
> need both: a fast variable to eliminate (clocks) and a negligible amount of
> stuff hiding in it (bookkeeping). Only the second one sets the size of the
> error. Segel 1988 does both properly.

**Write both boxed lines on the left wing, under the ledger, and leave them.**

**CUT if behind:** the τ₁/τ₂ lines. The bookkeeping argument stands alone and is
the one the next three surfaces use.

<div class="rule"></div>

## 4 · 62–67 min — What $n$ buys you

**Board 4 of 5 · 5 min · cumulative 27**

Four lines. This is **PS1 Q4b**, which asks for it analytically and forbids a
numerical search — so what you write here is the worked method for a question
they are about to be graded on.

$$\frac{x^n}{K^n + x^n} = 0.1 \;\Longrightarrow\; x_{10} = K\left(\tfrac{1}{9}\right)^{1/n},
\qquad
\frac{x^n}{K^n + x^n} = 0.9 \;\Longrightarrow\; x_{90} = K\,(9)^{1/n}$$

$$\frac{x_{90}}{x_{10}} = 81^{1/n}$$

> **ASK:** *where did $K$ go?* It cancels. The fold-change depends on $n$ alone,
> which is why every curve in the projected family crosses half occupancy in the
> same place.

**The number to make them feel.** $n = 1$ needs an **eighty-one-fold** change in
input to go from a tenth on to nine tenths on. That is a slope, not a switch.
$n = 2$ needs nine-fold; $n = 4$ needs three-fold.

> **Then run it backwards, out loud — this is the engineering direction.** "My
> circuit has to switch on a three-fold change in input." Read the table the
> other way: three-fold means $n \approx 4$, so you need cooperativity, so you
> go looking for a protein that has it. Requirement → number → mechanism. That
> is the direction they will use in the project, and the table is a **spec
> sheet** read in that direction.

> **IF ASKED** *"is that why real switches are cooperative?"* — yes, and it is
> the reason every toggle in the second half of this course has an $n$ in it.
> Session 9's bistability condition is
> $\alpha_c = n(n-1)^{-(n+1)/n}$, which is **infinite** for $n \le 1$: no
> cooperativity, no switch.

**CUT if behind:** the session-9 forward reference.

<div class="rule"></div>

## 5 · 67–72 min — Two independent sites

**Board 5 of 5 · 5 min · cumulative 32**

**Write the four states as a column before you write $Z$.** This is a partition
function, and it is session 6 arriving a week early — say so, because **PS1 Q5**
asks the 247 students for exactly this and it would otherwise be assessing
something untaught.

With $w = x/K_d$:

| state | weight |
|---|---|
| empty | $1$ |
| site 1 only | $w$ |
| site 2 only | $w$ |
| both | $w^2$ |

$$Z = 1 + 2w + w^2 = (1+w)^2$$

$$f_{\text{sites}} = \frac{\tfrac{1}{2}(w + w) + w^2}{(1+w)^2}
= \frac{w(1+w)}{(1+w)^2} = \frac{w}{1+w}$$

> **The square cancels.** $n = 1$, from two sites.

> **MAKE THEM SAY WHICH FRACTION.** "Fraction of *sites* occupied" is
> $w/(1+w)$. "Fraction of *promoters* with at least one site bound" is
> $1 - 1/(1+w)^2$, which is **not a Hill function at all**. Same molecules, same
> physics, two different curves — and a paper may not tell you which one it
> plotted. This is the single most common mark lost on PS1 Q5.

**The generalisation, one line:** $N$ independent identical sites give
$Z = (1+w)^N$ and site occupancy $w/(1+w)$, always. Independence is what makes
the sites invisible to a dose–response curve.

> **ASK, to set up ConcepTest 2:** *so what does a fitted $n$ of 1.9 tell you?*
> Leave it. That is the vote.

> **The vote's answer is D, and you need both halves.** *No ceiling*: $n \le$
> number of sites — that is the theorem you have just proved, and it is about an
> equilibrium **binding** curve. *No floor*: a **dose–response** is binding plus
> everything downstream, and downstream steps sharpen — zero-order
> ultrasensitivity or decoy titration gives an apparent $n$ above 20 from a
> single site (both are session 13). B is right for the curve on this slide and
> wrong for the one in the stem. **Which curve did you measure?**

**CUT if behind:** the $N$-site generalisation. The two-site case carries the
argument.
