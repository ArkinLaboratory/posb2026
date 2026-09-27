<!--
title: Session 10 — Four problems, and the scaffolding falls away
subtitle: Two halves. Start wherever the scaffolding stops helping you.
session: 10
-->

# Four problems, and the scaffolding falls away

$X$ is the input, $Y$ the middle gene, $Z$ the output, and every edge is $+$
(activation) or $-$ (repression):

$$\frac{dY}{dt} = B_y + f(X, K_{xy}) - \alpha_y Y \qquad\qquad
\frac{dZ}{dt} = \beta_z\, G(X, Y) - Z$$

with $f(u,K) = \dfrac{(u/K)^{H}}{1+(u/K)^{H}}$ for an activator and
$\dfrac{1}{1+(u/K)^{H}}$ for a repressor. **AND** means
$G = f(X,K_{xz})\,f(Y,K_{yz})$. **OR** means either input alone suffices; the
form is $G = f(X,K_{xz}) + f(Y,K_{yz}) - f(X,K_{xz})f(Y,K_{yz})$, and you will
not need it until the last line of item 2.

**Every number in this handout uses** $H = 2$, $K_{xy} = K_{xz} = 0.1$,
$\alpha_y = \alpha_z = 1$ and $\beta_y = 1$, so time is in protein lifetimes and
the input step is $X: 0 \to 1$. $B_y$ and $\beta_z$ are stated per item — they
are $0$ and $1$ unless an item says otherwise.

**The sign rule.** Compare the sign of the direct path $X \to Z$ with the
*product* of the signs along $X \to Y \to Z$. Same → **coherent**; opposite →
**incoherent**.

**The delay convention — state it before you use it.** Response time is the time
for $Z$ to reach **50% of its steady state**; a delay is measured only against
simple regulation of $Z$ by $X$ alone, with $\beta_z$ chosen so both reach **the
same steady-state $Z$**. Then $t_D = t_{1/2}(\text{FFL}) - t_{1/2}(\text{simple})$,
reported separately for the ON and OFF steps. A delay with no stated comparison
and no stated direction is not a number anyone else can check.

---

## 1 — Fully worked: classify by sign

<div class="q" markdown="1">

**(a)** $X \xrightarrow{+} Y$, $Y \xrightarrow{+} Z$, $X \xrightarrow{+} Z$, AND.
Direct $+$; indirect $(+)(+)=+$ → **coherent type 1**; the AND gate makes $Z$
wait for $Y$, so **delay on the ON step**.

**(b)** $X \xrightarrow{+} Y$, $Y \xrightarrow{-} Z$, $X \xrightarrow{+} Z$, AND.
Direct $+$; indirect $(+)(-)=-$ → **incoherent type 1**: $X$ drives $Z$ up and,
more slowly, drives up $Z$'s repressor. **A pulse, then adaptation.**

**(c)** $X \xrightarrow{-} Y$, $Y \xrightarrow{-} Z$, $X \xrightarrow{+} Z$, AND.
Direct $+$; indirect $(-)(-)=+$ → **coherent**, type 4. *Why does that follow?* —
a path's sign is the product of its edges.

**Now you:** $X \xrightarrow{-} Y$, $Y \xrightarrow{+} Z$, $X \xrightarrow{+} Z$.
Coherent or incoherent? <span class="blank"></span>

</div>

## 2 — Last step blank: the delay table

<div class="q" markdown="1">

Circuit (a), with $Y_{\min}=0$, $Y_{\max}=1$. On an ON step $Z$ stays off until
$Y$ crosses $K_{yz}$; since $Y(t)=Y_{\max}(1-e^{-\alpha_y t})$, setting
$Y=K_{yz}$ gives

$$t_D = \alpha_y^{-1}\ln\!\left[\frac{Y_{\max}-Y_{\min}}{Y_{\max}-K_{yz}}\right]
\qquad\text{so at } K_{yz}=0.5,\; t_D=\ln 2 \approx 0.69.$$

On an OFF step the AND gate opens the moment $X$ drops, so $t_D = 0$.
That formula is the **sharp-gate** ($H \gg 1$) limit. Ours run at $H=2$.

**Write your convention here, then fill the two blank columns.**

<div class="rule"></div>
<div class="rule"></div>

| $K_{yz}$ | $t_D$, formula | $t_D$, simulated at $H=2$ | $t_D$, OFF step |
|---|---|---|---|
| $0.2$ | <span class="blank"></span> | $0.35$ | <span class="blank"></span> |
| $0.5$ | $\ln 2 \approx 0.69$ | $0.75$ | $0$ |
| $0.8$ | <span class="blank"></span> | $1.02$ | <span class="blank"></span> |

*Why does that step follow?* — formula and simulation agree at $K_{yz}=0.5$ and
disagree badly at $0.8$. Which way is the formula wrong there, and what does
$H=2$ do to the claim that $Z$ "stays off until $Y$ crosses"?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

**One more line.** Same circuit, **OR** gate instead of AND. Which step is
delayed now — ON, OFF, or both? <span class="blank"></span>

</div>

<div class="pagebreak"></div>

## 3 — Three blanks: peak, final, and the adaptation error

<div class="q" markdown="1">

Circuit (b), and now $Y$ has a **basal level**: $B_y = 0.4$, $K_{yz}=0.5$,
$\beta_z = 6$. Step $X$ from 0 to 1 and integrate. $Z$ rises fast, then $Y$
builds and pulls it back to a plateau that is **not** zero. Both numbers below
are *measured off the curve*, not solved for.

peak <span class="blank"></span> final <span class="blank"></span>

$$\text{adaptation error} = \frac{Z_{\text{final}}}{Z_{\text{peak}}} = \underline{\phantom{0.000}}$$

*Why does that step follow?* — an error near 0 and one near 1 are two different
instruments. What is each good for?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

## 4 — Bare problem

<div class="q" markdown="1">

You need a circuit that fires **only if the input has been on for more than about
an hour**, and shuts off the moment the input goes away. Every protein you have
has a lifetime near 30 minutes.

Which FFL type, and which gate? Then: which parameter would you go after to put
the threshold near an hour — and can it actually get you there?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>
