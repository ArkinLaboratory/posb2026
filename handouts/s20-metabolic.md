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

## 2 · Last step blank — knock out the TCA

Set $v_{\text{tca}} = 0$. Every line above still holds down to the ATP balance,
which is the only one that mentioned the TCA. Now all pyruvate goes to
acetate, which pays **one** ATP where the TCA paid three — so each T3P is
worth two ATP rather than four:

$$\underline{\qquad\qquad} \cdot (20 - 4b) \;\geq\; 4b$$

**▶ $b \leq$** <span class="blank"></span>, which is **$\underline{\qquad}$% of
the wild type.**

**▶ Why does that step follow?** The flux map is not the wild-type map scaled
down — $v_{\text{ackA}}$ goes from carrying nothing to carrying everything. Say
in one sentence why a *linear* objective moves the answer to a different corner
rather than shrinking it in place.

<div class="rule"></div>
<div class="rule"></div>

---

## 3 · More blank — counting what is left over, and what kills it

**(a) Degrees of freedom.** $S$ has one row per balanced metabolite and one
column per reaction.

Rows: <span class="blank"></span>  Columns: <span class="blank"></span>
 rank $S$ = <span class="blank"></span>

$$\dim \operatorname{null}(S) \;=\; n_{\text{rxn}} - \operatorname{rank}(S) \;=\; \underline{\qquad\qquad}$$

**▶ Why does that step follow?** You found three directions the stoichiometry
cannot choose between. Session 3 wrote a null-space dimension too, and got a
different formula. In one sentence: what was *its* $n$ counting, and why is it
not this one?

<div class="rule"></div>

**(b) Lethality by inspection.** Of the seven real reactions, four deletions
drive $b$ to exactly zero. Name them, and for each name *the one thing biomass
needs that nothing else can make*.

| deleted | $b =$ | because nothing else makes |
|---|---|---|
| | | |
| | | |
| | | |
| | | |

**▶ Why does that step follow?** Two of the remaining three cost nothing at all.
Which two, and what do they have in common at the optimum?

<div class="rule"></div>

---

## 4 · Entirely yours — the answer stops being unique

Add one reaction, $v_{\text{zwf2}}$, with **exactly** the stoichiometry of
$v_{\text{zwf}}$: G6P $\rightarrow$ P5P + CO₂. Nothing else changes.

**(a)** What is the optimal $b$ now? Justify it in one line, without solving
anything.

<div class="rule"></div>

**(b)** The solver returns $v_{\text{zwf}} = 4$, $v_{\text{zwf2}} = 0$. Write
down a *different* flux vector that is just as optimal. Then a third.

<div class="rule"></div>

**(c)** How many optimal flux vectors are there? Describe the set in one
sentence, and say whether every member of it is a vertex of the feasible
region.

<div class="rule"></div>

**(d)** Flux variability analysis re-solves for the smallest and largest value
each flux can take while $b$ stays optimal. What does it return for
$v_{\text{zwf}}$, and what for $v_{\text{pgi}}$? Why are the two answers
different in kind?

<div class="rule"></div>

**(e)** In §3(b) you found $v_{\text{zwf}}$ and $b$ locked to each other. Is
that still true here? What broke it, and what does that tell you about where
coupling comes from?

<div class="rule"></div>
<div class="rule"></div>

---

## Before Thursday

Mishra *et al.*, *Nat Biotechnol* 32:1268 (2014) — a load driver. A circuit
slows down because something downstream is *reading* it. Read Figure 1 and the
rise times in the Online Methods.

Come able to say what the "load" physically is.
