<!--
title: Session 5 — Getting a removal rate out of decay data
subtitle: Two in the room, two on the problem set. Start wherever the scaffolding stops helping you.
session: 5
-->

# Getting a removal rate out of decay data

Four versions of one procedure, with **less of my working shown each time**.
**We do items 1 and 2 in the room** — eight minutes, and item 1 is already done.
Items 3 and 4 are on **PS2**; they are there rather than here because each needs
a decision defended in prose, and this room is worth more than that.

Both tables below are the same experiment: at $t = 0$ production is switched
off, and what is already in the cell is removed. The cells **keep growing**
throughout. That sentence is the whole of item 2.

<table>
<tr><th>Host</th><td>$T_d = 30$ min, so $\mu = \ln 2 / 30 = 0.0231$ min<sup>&minus;1</sup></td>
    <th>Signal</th><td>$y$ = fluorescence, arbitrary units</td></tr>
<tr><th>Model</th><td>$dp/dt = -(\gamma + \mu)\,p$ once production stops</td>
    <th>So</th><td>$\ln y$ is linear in $t$ with slope $-(\gamma + \mu)$</td></tr>
</table>

*These are the synthetic traces from `posb.data.decay_timecourse`, thinned to
seven points so you can do this on paper. PS2 gives you all forty and asks you
to fit them in code.*

---

<div class="q" markdown="1">

## 1 · Fully worked — the LAA tag

| $t$ (min) | 0 | 10 | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|---|---|
| $y$ | 101.5 | 68.0 | 44.9 | 29.5 | 20.3 | 13.5 | 8.8 |
| $\ln y$ | 4.62 | 4.22 | 3.80 | 3.38 | 3.01 | 2.60 | 2.17 |

**Take logs, and check they fall on a line.** The third row is already there.
The differences between consecutive entries are &minus;0.40, &minus;0.42,
&minus;0.42, &minus;0.37, &minus;0.41, &minus;0.43 — constant to within the
scatter, which is what "exponential" means and is the only evidence you have
that the model is the right one.

**Read the slope.** Over the whole run, $\Delta \ln y = 2.17 - 4.62 = -2.45$
across $\Delta t = 60$ min:

$$\text{slope} = \frac{-2.45}{60} = -0.0408 \ \text{min}^{-1}$$

**Name what you just measured.** The slope is $-(\gamma + \mu)$, so the
**removal rate constant** is $k = 0.0408$ min<sup>&minus;1</sup>. It is a rate
constant. Its units are per minute.

**Convert to a half-life — and this is where the marks go.**

$$t_{1/2} = \frac{\ln 2}{k} = \frac{0.693}{0.0408} = 17.0 \ \text{min}$$

> **Not 25 minutes.** $1/k = 24.5$ min is the *e*-folding time, a different
> number for a different question. The factor of $\ln 2$ is the single most
> common dropped mark in this course, and units will not catch it for you —
> both answers come out in minutes.

**▶ Why does that step follow?** You fitted a straight line to $\ln y$, not to
$y$. Give the reason in terms of the *noise*, not the algebra: what is being
assumed about the size of the measurement error, and why does a fluorescence
reading satisfy it?

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 2 · The last steps are yours — the AAV tag

Same host, same experiment, same growing cells.

| $t$ (min) | 0 | 10 | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|---|---|
| $y$ | 100.4 | 68.0 | 51.7 | 35.4 | 24.4 | 17.3 | 12.4 |

**Take logs, read the slope, and report $k$ and $t_{1/2}$**, with units on both.

$\ln y$ :

<div class="rule"></div>

<div class="rule"></div>
<div class="rule"></div>

**Now the question the number does not answer.** You have one exponential and
one rate constant. Andersen et al. report the AAV tag as a **60 minute**
half-life. Your $t_{1/2}$ is not 60 minutes and is not supposed to be.

**▶ Is what you fitted $\gamma$, or $\gamma + \mu$?** Answer from the
*description of the experiment*, not from the number — say which sentence at the
top of this page decides it.

<div class="rule"></div>

**▶ Now recover Andersen's number.** Using $\mu = 0.0231$ min<sup>&minus;1</sup>,
extract $\gamma$ from your $k$ and convert it to a degradation half-life. You
should land close to 60 min. Write the two lines of arithmetic.

<div class="rule"></div>
<div class="rule"></div>

**▶ And the transferable habit.** Andersen measured his half-lives after a
**medium downshift**, which arrests growth. Say in one sentence why that makes
his numbers safe to add to a $\mu$ of *your* choosing, and why a half-life
measured in growing cells could not be reused that way.

<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## On the problem set — the same procedure, unscaffolded

These are **PS2 Q2 and Q5**. Each is the place where the number you just
extracted has to be used for something.

<div class="q" markdown="1">

### 3 · The design question — *PS2 Q2*

> You need a reporter with a response time of $t_{1/2} = 12$ min, in a host that
> divides every **25** minutes. Which Andersen tag do you choose?

**State what you are solving.** Write down the $\gamma$ that the specification
demands, then convert it to the degradation half-life a tag would have to have.

**Now you: everything else.** Andersen's four tags are ASV 110, AAV 60, LVA 40,
LAA 40 minutes. Decide whether the specification can be met, and if it cannot,
report what the **best** available tag actually gives you — both the response
time and the steady-state level relative to untagged.

> The interesting half of this question is the part after "no". A specification
> you cannot meet by choosing a part is not a dead end; it is a question about
> which variable you were treating as fixed. Two of them are not.

</div>

<div class="q" markdown="1">

### 4 · Bare problem — *PS2 Q5; BioE 247. 147 may attempt it for extra credit*

> Everything above assumed production switches on as a step. It does not:
> inducer has to enter the cell and the promoter responds over some time. Let
> production ramp instead —
>
> $$\frac{dp}{dt} = \alpha\left(1 - e^{-t/\tau_{\text{ind}}}\right)
> - (\gamma + \mu)\,p, \qquad p(0) = 0$$
>
> Solve for $p(t)$, show it reduces to the step response as
> $\tau_{\text{ind}} \to 0$, and say whether the response time gets longer or
> shorter.

Then the part that is actually being asked: **give the condition under which
today's formula $t_{1/2} = \ln 2/(\gamma+\mu)$ is still a good description**,
stated as a comparison between two timescales in the style of session 4.

</div>

---

*A slope is a rate. A rate is not a half-life. And a half-life quoted without
saying whether the cells were growing is a number you cannot move to another
host — which means most of the ones you will read are.*
