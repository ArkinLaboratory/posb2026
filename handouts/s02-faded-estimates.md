<!--
title: Session 2 — Four estimates
subtitle: Start wherever the scaffolding stops helping you. Nobody is watching where you start.
session: 2
-->

# Four estimates

Four versions of one problem, with **less of my working shown each time**. Item
1 is done for you; item 4 is not. **Start wherever the scaffolding stops helping
you** — nobody has to announce which. The **bold labels** say what each step
*accomplishes*; that is the part worth carrying forward. At each **▶ Why does
that step follow?**, answer in writing before going on.

<table>
<tr><th>Avogadro</th><td>$N_A = 6.0 \times 10^{23}\ \mathrm{mol^{-1}}$</td>
    <th><em>E. coli</em></th><td>$1\ \mathrm{fL} = 10^{-15}\ \mathrm{L}$, ~1 µm across</td></tr>
<tr><th>HeLa cell</th><td>~20 µm across</td>
    <th>Genome</th><td>$4.6 \times 10^6$ bp</td></tr>
<tr><th>GFP in cytoplasm</th><td>$D = 7.7\ \mathrm{\mu m^2/s}$ <em>(Elowitz 1999)</em></td>
    <th>Division</th><td>20–30 min, rich medium</td></tr>
</table>

---

<div class="q" markdown="1">

## 1 · Fully worked

> A repressor is present at **10 nM** in *E. coli*. How many molecules is that?

**Convert the concentration to moles in this volume.**

$$n = c\,V = (10 \times 10^{-9}\ \mathrm{mol/L})(10^{-15}\ \mathrm{L})
      = 10^{-23}\ \mathrm{mol}$$

**Convert moles to a count.**

$$N = n N_A = (10^{-23})(6.0 \times 10^{23}) = 6\ \text{molecules}$$

**State the answer at the precision you actually have.**

About **6 molecules per cell** — call it "of order ten". Not 6.02: the cell
volume is known to maybe a factor of two, so the second digit is fiction.

> **Worth carrying:** $1\ \mathrm{nM} \approx 1$ molecule per *E. coli*. Every
> other copy number in this course is that number times something.

**▶ Why does that step follow?** Why is it legitimate to report one significant
figure when the arithmetic gave you three?

<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 2 · The last step is yours

> How long does a protein take to diffuse across *E. coli*?

**State the convention before the number.**

For one-dimensional displacement, $\langle x^2 \rangle = 2Dt$, so the time to
cover a distance $L$ is $t \sim L^2/2D$. *(In three dimensions it is $L^2/6D$.
The factor of three does not matter here. Not saying which one you used does.)*

**Put in the measured numbers.**

$$L = 1\ \mathrm{\mu m}, \qquad D = 7.7\ \mathrm{\mu m^2/s}$$

**Now you: evaluate it, and say it in words.**

<div class="rule"></div>
<div class="rule"></div>

**▶ Why does that step follow?** Why use the *measured* $D$ in cytoplasm rather
than the value for the same protein in water — and which way would the answer go
if you used the wrong one?

<div class="rule"></div>

</div>

<div class="pagebreak"></div>

<div class="q" markdown="1">

## 3 · The last two steps are yours

> The same protein, in a HeLa cell instead. How long, and how many times longer
> than in *E. coli*?

**State the convention.** Same as item 2 — $t \sim L^2/2D$, one-dimensional.

**Now you: everything else.** Take $D$ to be the same, and say at the end
whether that assumption makes your answer too big or too small.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

**▶ Why does that step follow?** The cell is 20 times wider. Why is the answer
not 20 times longer?

<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 4 · Bare problem

> A repressor must find **one specific operator site** in the *E. coli* genome.
> Suppose it searches by diffusing through the cytoplasm until it happens to
> collide with the right sequence.
>
> Estimate how long that takes, and compare it to the cell cycle.

You have everything you need. State your assumptions as you go, and at the end
say which one you are least confident in.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

**▶ The real question.** Measured association times for repressors are of order
*minutes* — considerably faster than a plain three-dimensional search predicts.

Your estimate is not wrong because you made an arithmetic error. It is wrong
because the *mechanism* is not what the problem said it was.

**What could the protein be doing instead?**

<div class="rule"></div>
<div class="rule"></div>

</div>

---

*An estimate that disagrees with a measurement is not a failure. It is the only
reliable way anyone has ever found a mechanism they were not looking for.*
