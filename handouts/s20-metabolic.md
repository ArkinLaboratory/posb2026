<!--
title: Session 20 — The network solved by hand, four times
subtitle: A home guide. The first one is worked for you; by the fourth the scaffolding is gone. Answers are released after the session.
session: 20
-->

# The network solved by hand, four times

Nine reactions, six balanced metabolites. Everything below is done with the
same six lines, and a solver is never needed:

| reaction | | carbon |
|---|---|---|
| $v_{\text{uptake}}$ | $\rightarrow$ G6P, capped at 10 | source |
| $v_{\text{pgi}}$ | G6P $\rightarrow$ F6P | 6 → 6 |
| $v_{\text{zwf}}$ | G6P $\rightarrow$ P5P + CO₂ | 6 → 6 |
| $v_{\text{tpi}}$ | F6P $\rightarrow$ 2 T3P | 6 → 6 |
| $v_{\text{lower}}$ | T3P $\rightarrow$ PYR + ATP | 3 → 3 |
| $v_{\text{ackA}}$ | PYR $\rightarrow$ Ace + CO₂ + ATP | 3 → 3 |
| $v_{\text{tca}}$ | PYR $\rightarrow$ 3 CO₂ + 3 ATP | 3 → 3 |
| $v_{\text{biomass}}$ | 2 T3P + P5P + 4 ATP $\rightarrow$ | sink |
| $v_{\text{atpm}}$ | ATP $\rightarrow$ | sink |

**The only tool is $S\mathbf{v} = 0$**: for every balanced metabolite, what is
made equals what is used. Write $b$ for $v_{\text{biomass}}$ throughout.

At each transition the sheet asks *why does that step follow?* Answer in
writing before you go on.

---

## 1 · Fully worked — the wild type

**P5P.** One producer, $v_{\text{zwf}}$. One consumer, biomass, which takes one
P5P per unit. So $v_{\text{zwf}} = b$.

**G6P.** Made at 10, used by two reactions: $10 = v_{\text{pgi}} + v_{\text{zwf}}$,
so $v_{\text{pgi}} = 10 - b$.

**F6P.** One producer, one consumer, so $v_{\text{tpi}} = v_{\text{pgi}} = 10 - b$.

> $v_{\text{tpi}}$ and $v_{\text{zwf}}$ are both lumps. $v_{\text{tpi}}$ is phosphofructokinase, aldolase and triose phosphate isomerase on one line; the isomerase by itself only interconverts the two trioses. Worth holding on to when you read what Fong & Palsson's model predicts for the *tpi* deletion.

**T3P.** Made at $2v_{\text{tpi}}$, used by biomass (2 per unit) and by
$v_{\text{lower}}$:

$$2(10-b) = 2b + v_{\text{lower}} \quad\Longrightarrow\quad v_{\text{lower}} = 20 - 4b$$

**ATP.** Every pyruvate goes round the TCA, which pays best. Each T3P through
$v_{\text{lower}}$ yields one ATP and then three more:

$$4(20-4b) \;\geq\; 4b \quad\Longrightarrow\quad 80 - 16b \geq 4b \quad\Longrightarrow\quad b \leq 4$$

So **$b = 4$**, and the rest falls out: $v_{\text{zwf}} = 4$,
$v_{\text{pgi}} = v_{\text{tpi}} = 6$, $v_{\text{lower}} = 4$,
$v_{\text{tca}} = 4$, $v_{\text{ackA}} = 0$, $v_{\text{atpm}} = 0$.

**Check it.** ATP made $= 4 + 3(4) = 16$; ATP used $= 4b = 16$. Nothing spare,
nothing short.

**▶ Why does that step follow?** The branch at pyruvate went *all* to the TCA
and none to acetate. Nothing in $S\mathbf{v} = 0$ says it must. What made the
split all-or-nothing?

<div class="rule"></div>
<div class="rule"></div>

---

## 2 · Last step blank — less glucose, not less network

Nothing is deleted. The medium is leaner: glucose now arrives at **5** instead
of 10, and every reaction is still there.

Four of the five lines carry straight over with 10 replaced by 5. The ATP line
is untouched — one ATP at lower, three round the TCA, four spent per unit of
biomass:

$$v_{\text{zwf}} = b \qquad v_{\text{pgi}} = v_{\text{tpi}} = 5 - b \qquad
2(5-b) = 2b + v_{\text{lower}}$$

$$\underline{\qquad\qquad} \;\geq\; 4b$$

**▶ $b =$** <span class="blank"></span>, which is **$\underline{\qquad}$% of
the wild type.**

**▶ Why does that step follow?** Halving the glucose did one thing to the
answer; deleting the TCA did something else entirely — in class the knockout
took $b$ from 4 to 10/3, and $v_{\text{ackA}}$ went from carrying nothing to
carrying everything. Say in one sentence what is different about the two
changes, in terms of where the optimum sits.

<div class="rule"></div>
<div class="rule"></div>

---

## 3 · More blank — counting what is left over, and proving what kills it

**(a) Degrees of freedom, after a deletion.** Deleting a reaction removes a
**column** of $S$. Take the network with $v_{\text{tca}}$ gone.

Rows: <span class="blank"></span>  Columns: <span class="blank"></span>
 rank $S$ = <span class="blank"></span>

$$\dim \operatorname{null}(S) \;=\; r - \operatorname{rank}(S) \;=\; \underline{\qquad\qquad}$$

**▶ Why does that step follow?** The full network had three directions the
stoichiometry could not choose between. Session 3 put **two** null spaces on
the board, one for what is conserved and one for what can flow. Which of the
two is this, and what does the *other* one count?

<div class="rule"></div>

**(b) Lethality, proved.** In class you named the four deletions that drive $b$
to exactly zero. Naming them is not proving them. For each one, write **the row
of $S$** that forces $b = 0$, and finish the argument in one line.

A row of $S$ is one metabolite's balance: what makes it, minus what uses it,
equal to zero. Two of the four need a second row to finish — say which, and
which row.

| deleted | the row that does it | and so |
|---|---|---|
| $v_{\text{zwf}}$ | | |
| $v_{\text{tpi}}$ | | |
| $v_{\text{pgi}}$ | | |
| $v_{\text{lower}}$ | | |

**▶ Why does that step follow?** Every one of those arguments used
$\mathbf{v} \geq 0$ somewhere, and would collapse without it. Point at the
place in one of them where it was used, and say what goes wrong if a flux is
allowed to run negative.

<div class="rule"></div>

---

## 4 · Entirely yours — when does a duplicate change anything?

In class we added one reaction, $v_{\text{zwf2}}$, with exactly the
stoichiometry of $v_{\text{zwf}}$, and two things happened at once: the
optimum stopped being unique, and the coupling between $v_{\text{zwf}}$ and
$b$ disappeared. Neither of those is automatic. This section is about when a
duplicate does that and when it does nothing at all.

**(a)** Add instead $v_{\text{tca2}}$, with exactly the TCA's stoichiometry:
PYR $\rightarrow$ 3 CO₂ + 3 ATP. Nothing else changes. What is the optimal
$b$? Which fluxes does flux variability analysis now report as free, and over
what range?

<div class="rule"></div>

**(b)** Which coupled pairs survive in that network? Compare with what
happened in class when $v_{\text{zwf}}$ was duplicated, and account for the
difference in one sentence about **rows of S**.

<div class="rule"></div>

**(c)** Now add $v_{\text{ackA2}}$ instead, with exactly ackA's
stoichiometry. What does flux variability analysis return this time? Say why
the answer is not the same kind as (a).

<div class="rule"></div>

**(d)** State the rule you have just found. What has to be true of a reaction
before duplicating it can create alternate optima at all?

<div class="rule"></div>
<div class="rule"></div>

---

## Before Thursday

Mishra *et al.*, *Nat Biotechnol* 32:1268 (2014) — a load driver. A circuit
slows down because something downstream is *reading* it. Read Figure 1 and the
rise times in the Online Methods.

Come able to say what the "load" physically is.
