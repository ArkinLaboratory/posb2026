<!--
title: Session 3 — Board sheet
subtitle: The structure is printed. The algebra is yours to fill in as it goes up.
session: 3
-->

# Board sheet

**Why you are holding this.** Most of today is on the board, and copying a
derivation is not the same as following one. The scaffolding is printed; **the
lines are blank on purpose.** Fill them in as they go up, and spend the time you
save on noticing *why* each step follows. Nothing here is collected. Everything
here is on PS1.

<div class="rule"></div>

## 1 · Where mass action comes from  <span class="sub">8–13 min</span>

A and B react only when they meet. In a well-mixed box the number of A–B
encounters per second is proportional to how many of each there are.

<div class="q" markdown="1">

Two A and three B. Distinct pairs that can meet: <span class="blank"></span>

Three A and three B: <span class="blank"></span>

So the rate law is

<div class="rule"></div>

**What does $k$ absorb?** (list at least three things)

<div class="rule"></div>
<div class="rule"></div>

</div>

A stoichiometric coefficient enters the **flux as a power** and the **balance as
a multiplier**. For $\mathrm{P} + \mathrm{P} \to \mathrm{P}_2$ the flux goes as
<span class="blank"></span>, not <span class="blank"></span>.

<div class="rule"></div>

## 2 · Is mass action allowed in an *E. coli*?  <span class="sub">13–17 min</span>

Three assumptions, three numbers. **Given:** $L = 1\ \mu$m,
$D = 7.7\ \mu\mathrm{m^2/s}$, $k_{\mathrm{on}} = 10^{8}\ \mathrm{M^{-1}s^{-1}}$,
$C = 1$ nM.

| | test | number | verdict |
|---|---|---|---|
| **well mixed** | $\mathrm{Da} = \tau_{\text{mix}}/\tau_{\text{rxn}}$ | $\tau_{\text{mix}} \approx$ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; $\tau_{\text{rxn}} \approx$ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Da $\approx$ | |
| **dilute** | activity $\propto$ concentration? | 20% protein by weight | |
| **many** | fluctuations go as $1/\sqrt{N}$ | 1 nM $\approx$ &nbsp; &nbsp; &nbsp; molecules, so $N =$ | |

**The three answers do not agree.** Which one fails, and is it the one you
expected?

<div class="rule"></div>

<div class="rule"></div>

## 3 · The long way  <span class="sub">17–21 min</span>

$$\mathrm{A} + \mathrm{B} \underset{k_r}{\overset{k_f}{\rightleftharpoons}} \mathrm{C}$$

$$\frac{d[\mathrm{A}]}{dt} = \qquad\qquad\qquad\qquad\qquad\qquad\qquad$$

$$\frac{d[\mathrm{B}]}{dt} = \qquad\qquad\qquad\qquad\qquad\qquad\qquad$$

$$\frac{d[\mathrm{C}]}{dt} = \qquad\qquad\qquad\qquad\qquad\qquad\qquad$$

How many **distinct fluxes** are there in those six terms? <span class="blank"></span>

<div class="rule"></div>

## 4 · Two fluxes, one matrix  <span class="sub">21–26 min</span>

$$v_1 = \qquad\qquad\qquad\qquad v_2 = \qquad\qquad\qquad\qquad$$

$S_{ij}$ = net molecules of species $i$ produced by reaction $j$.

| | $v_1$ (forward) | $v_2$ (reverse) |
|---|---|---|
| **A** | | |
| **B** | | |
| **C** | | |

$$\frac{d\mathbf{x}}{dt} = \qquad\qquad\qquad$$

**S is** <span class="blank"></span> — it comes off the reaction list alone and
knows nothing about rate constants, concentrations or time.

**v is** <span class="blank"></span> — every parameter and all of the biology.

<div class="rule"></div>

## 5 · Two null spaces  <span class="sub">26–33 min</span>

**LEFT.** If $\mathbf{w}^{\mathsf{T}}\mathbf{S} = \mathbf{0}$ then
$\dfrac{d}{dt}(\mathbf{w}^{\mathsf{T}}\mathbf{x}) = $ <span class="blank"></span>
for **any** $\mathbf{v}$ — so $\mathbf{w}^{\mathsf{T}}\mathbf{x}$ is conserved.

Find two for $\mathrm{A}+\mathrm{B} \rightleftharpoons \mathrm{C}$:

$\mathbf{w} =$ <span class="blank"></span> giving <span class="blank"></span> &nbsp;&nbsp;&nbsp;
$\mathbf{w} =$ <span class="blank"></span> giving <span class="blank"></span>

$\operatorname{rank}\mathbf{S} =$ <span class="blank"></span>, so
$\dim(\text{left null}) = n - \operatorname{rank}\mathbf{S} =$ <span class="blank"></span>

**RIGHT.** $\mathbf{S}\mathbf{v} = \mathbf{0}$ asks: *which patterns of reaction
rates leave every concentration unchanged?* Here that gives <span class="blank"></span>,
so $\dim(\text{right null}) = r - \operatorname{rank}\mathbf{S} =$ <span class="blank"></span>

**The cascade, for contrast.** $\varnothing \xrightarrow{\alpha} m$, &nbsp;
$m \xrightarrow{\gamma_m} \varnothing$, &nbsp; $m \xrightarrow{k_p} m + p$, &nbsp;
$p \xrightarrow{\gamma_p} \varnothing$

$\mathbf{S}$ is <span class="blank"></span> $\times$ <span class="blank"></span>
with rank <span class="blank"></span>. Conservation laws: <span class="blank"></span>.
Flux modes: <span class="blank"></span>.

**Why no conservation laws at all?**

<div class="rule"></div>

*Flux balance analysis, in session 20, is the right null space plus bounds on
$\mathbf{v}$ plus an objective. That is all it is.*

<div class="rule"></div>

## 6 · The steady state, without a computer  <span class="sub">59–63 min</span>

$$\frac{dm}{dt} = \alpha - \gamma_m m = 0 \quad\Longrightarrow\quad m^* = \qquad\qquad$$

$$\frac{dp}{dt} = k_p m^* - \gamma_p p = 0 \quad\Longrightarrow\quad p^* = \qquad\qquad$$

With $\alpha = 10$, $\gamma_m = 0.5$, $k_p = 4$, $\gamma_p = 0.05$:
&nbsp; $m^* =$ <span class="blank"></span> &nbsp; $p^* =$ <span class="blank"></span>

**The move worth naming:** a cascade solves <span class="blank"></span> —
$m^*$ does not contain $p$, so solve it alone and substitute.

<div class="rule"></div>

## 7 · Integrate it exactly  <span class="sub">63–67 min</span>

$$m(t) = m^*\left(1 - e^{-\gamma_m t}\right) \qquad\Longrightarrow\qquad \frac{dp}{dt} + \gamma_p p = k_p m(t)$$

Multiply by the integrating factor <span class="blank"></span> :

$$\frac{d}{dt}\Big[ \qquad\qquad\qquad \Big] = \qquad\qquad\qquad$$

$$p(t) = p^*\left[\,1 - \frac{\qquad\qquad\qquad\qquad\qquad}{\qquad\qquad\qquad}\right]$$

**Two checks, both worth ten seconds.** At $t=0$: <span class="blank"></span>.
As $t \to \infty$: <span class="blank"></span>.

**Two exponentials, not one.** The protein does not simply relax at $\gamma_p$ —
it also carries the mRNA's rise.

<div class="rule"></div>

## 8 · Four parameters become one  <span class="sub">70–74 min</span>

Scale by the answer: $\tau = \gamma_p t$, &nbsp; $\mu = m/m^*$, &nbsp; $\pi = p/p^*$.

$$\frac{d\mu}{d\tau} = \qquad\qquad\qquad\qquad \frac{d\pi}{d\tau} = \qquad\qquad\qquad\qquad$$

$$\varepsilon \;=\; \qquad\qquad\qquad\qquad \text{and ours is} \qquad\qquad\qquad$$

That one number is the **only** parameter left. Two cascades with wildly
different rate constants and the same $\varepsilon$ give the same curve after
rescaling.

Setting $\varepsilon = 0$ says $\mu = 1$ instantly. That is the
**quasi-steady-state approximation**, and Tuesday is about what it costs: the
largest error in $p/p^*$ turns out to be about <span class="blank"></span>.

<div class="rule"></div>

## Take away

1. Every deterministic model in this course is $\dot{\mathbf{x}} = \mathbf{S}\mathbf{v}(\mathbf{x})$; structure and kinetics separate.
2. A species on both sides of a reaction has **zero** net stoichiometry — translation is catalytic in the message.
3. Find the conserved quantity and check it. The cheapest test you will ever write.
