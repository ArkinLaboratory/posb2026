<!--
title: Session 24 — Communities and quorum sensing
subtitle: A home guide, worked after class. Item 1 asks what Basu's own data settles and what it does not; item 2 asks what a published diffusion coefficient is worth; item 3 asks what a shared signal costs you; item 4 is one pathway and whether to split it. Three bonus items on the Balagaddé reactor follow. Answers come on a separate sheet.
session: 24
-->

# How to use this

Work it after class, on paper. The answers are on a separate sheet — read
them **after** you have written something down, not instead of writing
something down.

Nothing in items 1 to 4 asks you to write a sender/receiver model, solve a
band edge, or estimate a diffusion length. Those are the hour's three
computational techniques and they are the ones the problem set will ask for.
This guide works the territory around them: what the measurements are worth,
what you inherit rather than set, and what a shared signal costs. Item 4 is a
design decision you will not meet anywhere else before the final. None of it
needs a computer.

**The bonus items** at the end are the Balagaddé predator–prey reactor, worked
in full. They are not required and they are not on the final. They are there
because the model is deposited, the paper is good, and licensing an
approximation you cannot afford is a mistake worth making once on paper. The
slides for them are in the deck's appendix.

**The symbols, once.** $\beta_C$ and $\beta_L$ are Basu's two repression
coefficients, in concentration units — the signal level at which each
repressor is effective. $D_A$ is the **signal's diffusion coefficient**;
in this session a bare $D$ is never a diffusion coefficient, it is a
reactor's dilution rate, and it only appears in the bonus items.
$\gamma_A$ is the signal's first-order decay rate and
$\ell_A = \sqrt{D_A/\gamma_A}$ the steady-state length it reaches.

In item 4 the transport inefficiency is $\varepsilon_T = \delta_{me}/\eta$,
with $\eta$ the intermediate's transport rate and $\delta_{me}$ its turnover
outside the cell. Item 4's burdens are written $B_1$ and $B_2$ and they are
**per enzyme**. The single cell carries their sum. Tsoi writes the same thing
as $\beta e_1$ and $\gamma e_2$; this course writes $B$ because $\gamma$ is a
decay rate everywhere else and $\beta_L, \beta_C$ are Basu's printed
thresholds in the same hour.

The bonus items use the reactor's own symbols and define them where they start.

---

## 1. What Basu's own data settles, and what it does not

Basu's receiver lights in a ring because two repression routes of opposite
parity act at concentrations far apart: close to the senders CI shuts the
reporter, far away the mutant LacI shuts it, and in between neither is
effective. The printed coefficients are $\beta_C = 8$ nM and
$\beta_L = 0.8\ \mu$M — a factor of a hundred.

Three results from the paper, all real:

| | what they report | where |
|---|---|---|
| three band-detect variants | the **ordering** of the three band positions matches the model; the absolute positions are shifted by 2–3× in AHL | Fig. 2c vs 2d |
| one strain, two bullseyes | BD2-Red rings at **30 mm** in one experiment and **22 mm** in another — a 36 % difference | Fig. 3b, 3c |
| what they say about it | they attribute the difference to variation in sender and receiver growth rates and densities, and to nutrient and agar differences | p. 1130–1131 |

**(a)** Without algebra, from the two routes alone: what happens to the band
if $\beta_C$ and $\beta_L$ are made equal, and why? Then say what the data
can and cannot tell you about which of the two repressors is "better".

**(b)** The paper writes that the measurements "correlated well with model
predictions." Given that the ordering matches and the absolute positions are
shifted two- to threefold, write the sentence that claim is actually entitled
to. One sentence, and be precise about what is being compared.

**(c)** You want to use ring radius as a quantitative readout of something.
The same strain gave 30 mm and 22 mm. Neither explanation the authors offer is
a circuit parameter. Say what that means for your readout, name one change
that would make the radius more reproducible, and say what that change costs
you.

**(d)** Name the measurement Basu do not report that would let you decide
whether the 36 % is the plate or the circuit. Say what you would expect to see
under each.

---

## 2. What a published diffusion coefficient is worth

Karig measured two signals moving through a lawn of cells and reported
effective coefficients. Everything you need is printed here.

| quantity | value |
|---|---|
| 3OC12HSL, through the lawn | $83\ \mu$m$^2$/s |
| C4HSL, through the lawn | $1810\ \mu$m$^2$/s |
| their measured ratio | $21.6$ |
| molecular masses | $297$ Da and $171$ Da |
| what size alone predicts (Wilke–Chang, $D \propto V^{-0.6}$) | a ratio near $1.5$ |
| Basu's own $\xi$, with $\gamma_A = 0.01$ min$^{-1}$ | gives $\ell_A = 0.32$ mm |
| the same $\gamma_A$ with Karig's $83\ \mu$m$^2$/s | gives $\ell_A = 0.71$ mm |
| where Basu's ring actually sits, and when | $10$ mm, stable by $\sim 32$ h |
| session 2's GFP in water | $87\ \mu$m$^2$/s |

**(a)** Size accounts for about 1.5 of a measured ratio of 21.6. Say
physically what the remaining factor of roughly fourteen is. One sentence.

**(b)** Follow that through to a design consequence. If most of the ratio
belongs to the lawn rather than to the molecules, what happens to the
coefficient you would use when you change the cell density you build at? Say
which direction and why.

**(c)** Three estimates of the same reach are above and they do not agree.
Rank them by how much you trust them for Basu's plate, say why, and name the
single measurement that would settle it.

**(d)** Karig's deterministic analysis requires a diffusion ratio near 100.
They measured 21.6 and they observe patterns anyway. Say what that gap means.
"The model is wrong" is not the answer being asked for — say what kind of
thing the deterministic requirement is a statement about.

---

## 3. What a shared signal costs you

Tamsir, Tabor and Voigt put one logic gate in each strain and wire the gates
together with diffusing signal. The XOR is four strains spotted on a plate:

| strain | gate | inputs | output |
|---|---|---|---|
| cell 1 | NOR | Ara, aTc | LasI → 3OC12-HSL, to cells 2 and 3 |
| cell 2 | NOR | 3OC12-HSL + Ara | RhlI → C4-HSL |
| cell 3 | NOR | 3OC12-HSL + aTc | RhlI → C4-HSL |
| cell 4 | buffer | C4-HSL | the circuit output |

Two signals in the whole system: 3OC12-HSL, made by LasI and read by LasR, and
C4-HSL, made by RhlI and read by RhlR. A small library of these strains covers
all sixteen two-input functions with no further genetic manipulation; between
one function and the next, only the arrangement on the plate changes.

**(a)** Cells 2 and 3 both emit C4-HSL and cell 4 reads it. Cell 4 cannot tell
which of them sent it. Is that a defect or a design choice? Name the Boolean
operation the shared signal performs for free, and say where in the XOR's
truth table you can see it doing so.

**(b)** Now you want two genuinely independent connections on the same plate:
one gate talking to a second, and a third talking to a fourth, with no
crosstalk between the pairs. How many orthogonal signals does that need, and
why? Then generalise: a circuit needing $k$ independent connections needs how
many, and what does that make the binding constraint on circuit size?

**(c)** Sixteen functions and no further cloning sounds like the parts problem
is solved. Say what resource the sixteen functions actually consume, and why
session 17's count of orthogonal parts is still the thing that limits a bigger
circuit.

**(d)** Their plate carries a length and a time: 1 µL spots on a 7 mm grid,
12 h between spotting one layer and the next. Say why those two numbers are
**not** a diffusion coefficient, and name the one additional thing you would
have to measure to turn them into one.

---

## 4. Whether to split one pathway

A three-enzyme pathway runs in one *E. coli* strain and works. E1 makes the
first intermediate, E2 the second, E3 the product. **E2 is the expensive
one.** The intermediate between E2 and E3 is a charged sugar phosphate, and it
crosses the membrane slowly. You are considering cutting the pathway at that
junction and running E1 and E2 in one strain and E3 in another, with the
intermediate crossing between them.

Everything you need is printed here, because none of it can be read off a
figure.

| quantity | value |
|---|---|
| burden of E1, E2, E3, **per enzyme** | $0.25$, $1.15$, $0.30$ |
| burden form | Hill, $1/(1+B^n)$, with $n = 2$ |
| host resilience $\mu_{max}/\delta_\upsilon$ | $10$ |
| carrying capacity $\rho$ | $1$, and Tsoi's $\rho_1 = \rho_2 = \rho/2$ |
| transport rate of the intermediate, $\eta$ | $0.8$ |
| its turnover outside the cell, $\delta_{me}$ | $0.4$ |
| the downstream enzyme's $\alpha_2 e_2$ | $1$ |

Tsoi's criterion, stated. A population's steady-state biomass is
$\upsilon = \rho\left(1 - \delta_\upsilon/\mu\right)$ where
$\mu = \mu_{max}/(1+B^n)$ and $B$ is the burden that population carries, and a
population whose $\mu$ falls to $\delta_\upsilon$ does not persist. Splitting
is favored when

$$\frac{\bar\upsilon_{DOL}^{\,2}}{\upsilon^2 + \varepsilon_T\upsilon}
\;>\; \theta_I,
\qquad
\bar\upsilon_{DOL} = \sqrt{\upsilon_1\upsilon_2},
\qquad
\varepsilon_T = \frac{\delta_{me}}{\eta}$$

$$\theta_I = \frac{\delta_{me} + \delta_{me}\eta/(\alpha_2 e_2) + \eta\upsilon_2}
{\delta_{me} + \delta_{me}\eta/(\alpha_2 e_2) + \eta\upsilon}$$

with $\upsilon$ the single cell's biomass, $\upsilon_1$ the upstream
population's and $\upsilon_2$ the downstream population's.

One warning, for anyone who goes looking for the burden at which the verdict
flips by bisecting on a computer. Both yields are **identically zero** once
the single cell and the split populations are all dead of their own burden, so
the margin between them is identically zero there too, and a bracket that
reaches into that region returns its own endpoint rather than a crossing.
Bracket below the burden at which the populations die, or scan the margin first
and bracket a sign change you have seen for yourself.

**(a)** Evaluate every symbol in the criterion for this pathway: the three
biomasses, $\bar\upsilon_{DOL}$, $\varepsilon_T$ and $\theta_I$. Then say in
one sentence each what the two sides of the inequality represent.

**(b)** Would you split this pathway across two strains? Name the term that
decided it. Then test your reason: set $\delta_{me}$ to zero, so the
intermediate is free to move, and say whether the verdict changes.

**(c)** Name one assumption behind the criterion that this pathway strains or
violates, and say which way it moves your answer. "Which way" is the part
being asked for.

**(d)** Name two quantities you would measure before building either version.
For each, say what value would change your verdict, and how you would measure
it.

---

# Bonus — the predator–prey reactor

Not required, and not on the final. Balagaddé et al. built a two-strain
community in a chemostat where each strain holds the other's survival, and
deposited a model of it. These three items work that model and that reactor.
The slides are in the appendix of the session deck.

**The symbols for this section.** $C_1$ and $C_2$ are the predator and prey
densities; $A_1$ is the signal the predator makes and $A_2$ the signal the
prey makes. $k_{c1}, k_{c2}$ are the two growth rates and $C_m$ the carrying
capacity they share. $d_1$ and $d_2$ scale the two death terms, with $K_1$ and
$K_2$ their half-saturation constants. $k_{A1}, k_{A2}$ are signal synthesis
rates and $d_{AA1}, d_{AA2}$ the signals' abiotic decay rates. $D$ is the
**dilution rate** of the reactor, in h$^{-1}$. $\varepsilon$ is the clock
ratio a quasi-steady-state argument has to satisfy, written the way session 4
wrote it — the rate of the **slow** thing over the rate of the thing you are
eliminating.

## B1. Licensing the approximation costs you the circuit

Here is the predator–prey community as it is deposited — BioModels
BIOMD0000000296, curated from Balagaddé 2008 by reproducing the paper's
figures. The paper itself prints no equations.

$$\dot C_1 = k_{c1}C_1\!\left(1 - \tfrac{C_1+C_2}{C_m}\right) -
\left(D + d_1\tfrac{K_1}{K_1+A_2^2}\right)C_1$$

$$\dot C_2 = k_{c2}C_2\!\left(1 - \tfrac{C_1+C_2}{C_m}\right) -
\left(D + d_2\tfrac{A_1^2}{K_2+A_1^2}\right)C_2$$

$$\dot A_1 = k_{A1}C_1 - (d_{AA1}+D)A_1 \qquad
\dot A_2 = k_{A2}C_2 - (d_{AA2}+D)A_2$$

At IPTG = 5 µM the deposited constants are $k_{c1} = 0.8$, $k_{c2} = 0.4$,
$C_m = 100$, $d_1 = 1.0$, $d_2 = 0.3$, $K_1 = K_2 = 10$, $k_{A1} = 0.1$,
$k_{A2} = 0.035$, $d_{AA1} = 0.017$, $d_{AA2} = 0.11$ and $D = 0.1125$, all
rates per hour.

Class put $A_1$ and $A_2$ at quasi-steady state, watched the oscillation
disappear, and then checked the condition. A signal is removed at
$d_{AA}+D$, so

$$\varepsilon_1 = \frac{k_{c1}}{d_{AA1}+D} = \frac{0.8}{0.1295} = 6.18
\qquad
\varepsilon_2 = \frac{k_{c2}}{d_{AA2}+D} = \frac{0.4}{0.2225} = 1.80$$

against session 4's 0.1. Both are above 1, which is the wrong side. The
algebra was correct and the premise was false.

This item asks the obvious next question, which class did not ask: **what
would it take to make the premise true?** Three parameters appear in
$\varepsilon_1$ and you may move one at a time. For scale: at the deposited
constants the interior coexistence state is $C_1 = 5.12$, $C_2 = 20.98$,
$A_1 = 3.96$, $A_2 = 3.30$, and it exists only for $D$ below about 0.176.

**(a)** Raise $D$. Find the $D$ at which $\varepsilon_1$ reaches session 4's
0.1, and then say what the reactor contains at that dilution rate. Two
thresholds help: a population whose growth rate is below $D$ cannot hold its
place, and $k_{c2} = 0.4$.

**(b)** Raise $d_{AA1}$ instead — the signal's own decay, which the hour
established is a property of the medium and is yours to set.
Find the value that puts $\varepsilon_1$ at 0.1, as a multiple of what the
deposit has. Then take the prey's death term, $d_2 A_1^2/(K_2+A_1^2)$, and say
what has happened to it. Compare it with $D$ before you write your answer.

**(c)** Lower $k_{c1}$. Find the value needed, compare it with $D$, and say
why this route is not available either.

**(d)** Put (a), (b) and (c) together into one sentence saying where this
reduction *can* be used. Then write the general version: when a reduction's
validity condition fails, what is the second question to ask before you
discard the reduction?

---

## B2. What the one agreement is worth

The deposited model is faithfully the paper's. Run from the deposited
constants it lands on three things their own Fig. 3C prints — the oscillatory
branch opening at $D = 0.0367$ against their 0.035–0.04, the upper crossing at
$D = 0.1674$ with a period of 73.6 h against their ~73 h at ~0.168, and
coexistence lost near 0.176 against their washout above 0.18.

Its regime map in dilution rate, computed. Every $D$ below is in h$^{-1}$:

| $D$ | the model's interior state |
|---|---|
| below 0.0367 | coexistence, **stable** — the system spirals in |
| 0.0367 to 0.1674 | coexistence, **unstable** — a sustained cycle |
| 0.1674 to ~0.176 | coexistence, **stable** again |
| above ~0.176 | **no coexistence state at all.** The only surviving state is prey-only: the predator washes out |

And what the reactor did at the five dilution rates the authors ran:

| $D$ | the experiment | the model |
|---|---|---|
| 0.11 | coexistence, steady | sustained cycle, **168 h** |
| 0.15 | coexistence, steady | sustained cycle, **122 h** |
| 0.20 | damped ringing, period ~50 h | no coexistence |
| 0.23 | damped ringing, period ~30 h | no coexistence |
| 0.31 | **predator** washout | no coexistence |

Four disagreements and one agreement. The authors' phrase for the whole of
this is that the model "qualitatively accounts for" what they saw.

**(a)** A colleague says the pumps must have been off by a constant factor, and
that multiplying every $D$ in the right-hand column by one number $c$ will
reconcile the table. Work out what the best $c$ can do: say which rows it
fixes, which it breaks, and what that tells you about the kind of error this
is. (Treat "steady" and "damped ringing" as the same thing for this part —
both are a stable coexistence state.)

**(b)** The agreement is at $D = 0.31$. Say what it is worth, using the model's
regime map rather than the table. Then name an observation at $D$ above 0.18
that would have been evidence for the model.

**(c)** Above 0.176 the model's only surviving state is prey-only. Put that
beside Fig. 3A, where the step to $D = 0.20$ is followed by the predator
spiking to about $60 \times 10^3$ while the prey falls to near zero and stays
there. This is a disagreement the five-row table does not show. State it, and
say why it is the one a designer should care about most.

**(d)** Class used the three Fig. 3C agreements to rule out a transcription
error, and they do rule one out. But the deposit was curated by reproducing
the paper's own figures. Say what that does to those three agreements as
evidence, and name the kind of error they therefore cannot rule out.

---

## B3. Which reactor earned which claim

Six results, all real, all from Balagaddé 2008, all about the same two-strain
community:

| | what was seen | where |
|---|---|---|
| i | antiphase oscillation, period ~180 h, at IPTG = 5 µM and $D = 0.1125$ | Fig. 2A, one reactor |
| ii | the four uninduced reactors: the **prey** washes out | Fig. 2B |
| iii | several induced reactors: prey high and rising, predator flat and low, for 200 h and more | Fig. 2B |
| iv | coexistence at $D = 0.11$; a step to 0.20 at ~230 h, then damped ringing of period ~50 h, with the prey near zero from ~350 h to the end of the run at 510 h | Fig. 3A |
| v | coexistence at $D = 0.15$; a step to 0.23, then damped ringing of period ~30 h; a further step to 0.31, then **predator** washout | Fig. 3B |
| vi | only the predator carries GFPuv(LVA). The prey's count is obtained by **subtraction**, so a dim fluorescent cell is counted as prey. The imaging cannot resolve a population below about 75 cells per reactor, and the prey's fluctuations about zero in Fig. 2B are called numerical artifacts of image processing | Methods, p.6; p.4 |

Two more things from the paper, since its strain names are not
self-explanatory. Fig. 3A is predator **MG1655** with prey **Top10F′**;
Fig. 3B is predator **Top10F′** with prey **Top10F′**. And the predator dies
by default and is rescued by the prey's signal; the prey is killed by the
predator's signal and has no antidote.

**(a)** Three washouts appear in (ii), (iv) and (v). The table names the
species for two of them; name the third. Then give the three different causes,
and say what goes wrong in a summary figure that draws one arrow labeled
"washout".

**(b)** Result (iv) is described as a damped predator–prey oscillation. Which
trace is ringing, and what would have to be true of the other trace for that
phrase to be right? Say what you would call it instead.

**(c)** The bias in (vi) has a direction. Say which way it runs, then name the
result among (i)–(v) it weakens most and the one it cannot touch. For (i),
separate the part of the measurement the floor and the bias reach from the part
they do not.

**(d)** Results (iv) and (v) use different predators. Say what you cannot
conclude by putting the ~50 h and the ~30 h periods on one axis against $D$.
Box 1B's plane will help: its two axes are the predator's own growth rate and
its death rate.

---

