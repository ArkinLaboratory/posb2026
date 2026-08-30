<!--
title: Session 4 — Where a regulation function comes from
subtitle: Two in the room, two on the problem set. Start wherever the scaffolding stops helping you.
session: 4
-->

# Where a regulation function comes from

Four versions of one derivation, with **less of my working shown each time**.
**We do items 1 and 2 in the room** — ten minutes, and item 1 is already done.
Items 3 and 4 are the same technique with the scaffolding gone; they are on
**PS1**, and they are there rather than here because they take longer than ten
minutes and this room is worth more than that.

The **bold labels** say what each step *accomplishes*. At each **▶ Why does that
step follow?**, answer in writing before going on.

<table>
<tr><th>Notation</th><td>$x = [\mathrm{X}]$, the free transcription factor</td>
    <th>Site</th><td>$\mathrm{P}$ = empty promoter, $\mathrm{PX}$ = bound</td></tr>
<tr><th>Dissociation constant</th><td>$K_d = [\mathrm{P}][\mathrm{X}]/[\mathrm{PX}]$ — *large* $K_d$ means *weak* binding</td>
    <th>Assume</th><td>binding equilibrates far faster than transcription</td></tr>
</table>

---

<div class="q" markdown="1">

## 1 · Fully worked — one site

> A transcription factor X binds a single site on a promoter. What fraction of
> promoters are bound, as a function of $[\mathrm{X}]$?

**Write the equilibrium, and say what is held fixed.**

$$\mathrm{P} + \mathrm{X} \rightleftharpoons \mathrm{PX}, \qquad
K_d = \frac{[\mathrm{P}]\,x}{[\mathrm{PX}]}
\quad\Longrightarrow\quad [\mathrm{PX}] = \frac{[\mathrm{P}]\,x}{K_d}$$

*X is buffered: there is far more of it than there is promoter, so binding does
not deplete it. That is why $x$ is a parameter and not a variable.*

**Form the fraction — the thing you actually want, not the concentration.**

$$f_{\text{bound}} = \frac{[\mathrm{PX}]}{[\mathrm{P}] + [\mathrm{PX}]}
= \frac{[\mathrm{P}]x/K_d}{[\mathrm{P}] + [\mathrm{P}]x/K_d}$$

**Cancel the thing you cannot measure.**

$$f_{\text{bound}} = \frac{x/K_d}{1 + x/K_d} = \frac{x}{K_d + x}$$

> **Worth carrying:** that *is* a Hill function, with $n = 1$ and $K = K_d$.
> The half-point is at $x = K_d$ — which is what a dissociation constant means.

**▶ Why does that step follow?** $[\mathrm{P}]$ cancelled. Why is that not an
accident of this problem — what would have to be true for it *not* to cancel?

<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 2 · The last step is yours — $n$ sites, all or nothing

> Now the promoter has $n$ identical sites, and cooperativity is so strong that
> only two states are ever populated: **empty**, or **fully occupied**. Nothing
> in between.

**Write the equilibrium for the idealised two-state promoter.**

$$\mathrm{P} + n\,\mathrm{X} \rightleftharpoons \mathrm{PX}_n, \qquad
K_d = \frac{[\mathrm{P}]\,x^{\,n}}{[\mathrm{PX}_n]}$$

**Now you: form the fraction, cancel, and put it in Hill form** — that is,
identify the $K$ for which your answer reads $x^n/(K^n + x^n)$.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

**▶ Why does that step follow?** Your $K$ is not $K_d$. Say in one sentence what
$K$ *is*, and what it would mean physically for two promoters with the same $K$
to have different $K_d$.

<div class="rule"></div>

**▶ And the honest question.** "No partially bound states" is a lie. Whose lie
is it — what physical situation makes it a *good* lie, and what would you
measure to find out whether it is one here?

<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## On the problem set — the same technique, unscaffolded

These are **PS1 Q4b and Q5**. They are not homework in the sense of "more of the
same"; each one is the place where the idealisation you just used gets tested.

<div class="q" markdown="1">

### 3 · The last two steps are yours — what $n$ actually buys you

> How much must $x$ change to take the promoter from **10% to 90%** occupied?

**State what you are solving.** Set $x^n/(K^n + x^n)$ equal to $0.1$, and again
to $0.9$, and solve each for $x$. Do it **algebraically** — no numerical search.

**Now you: everything else.** You should find the ratio $x_{90}/x_{10}$ depends
only on $n$, not on $K$. Report it as a formula, then evaluate it for
$n = 1, 2, 4, 8$.

> This number is the entire practical content of a Hill coefficient. A circuit
> that must switch cleanly needs a small fold-change here; that requirement is
> what sends people looking for cooperativity in the first place.

</div>

<div class="q" markdown="1">

### 4 · Bare problem — *BioE 247; 147 may attempt it for no credit*

> Relax the idealisation. Two **independent, identical** sites — binding at one
> does nothing to the other — each with dissociation constant $K_d$.
>
> Write the partition function over all four states (empty, site 1 only, site 2
> only, both), derive the fractional occupancy, and put it in Hill form.

State your assumptions as you go. Two things to be careful about, both of which
are the actual question rather than a technicality:

- **Say which fraction you are computing.** "Fraction of sites occupied" and
  "fraction of promoters with at least one site bound" are different functions
  of $x$, and only one of them is a Hill function at all.
- **Then state what your answer implies** for reading a measured Hill
  coefficient off a dose–response curve, and what would have to be true of the
  binding energetics to recover $n = 2$.

</div>

---

*A Hill coefficient is not a count of binding sites. It is a measure of
cooperativity, and the number of sites is only its ceiling — a bound you reach
in a limit that nothing in a cell quite occupies.*
