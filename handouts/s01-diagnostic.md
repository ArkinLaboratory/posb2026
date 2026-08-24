<!--
title: Session 1 — Diagnostic
subtitle: Ungraded, and it affects nothing. Five minutes.
session: 1
-->

# Diagnostic

**Name** <span class="blank" style="width:2.6in"></span> **Course** BioE 147 / 247 *(circle one)*

This isn't graded and doesn't touch your grade. It's here so I can pitch the
next few weeks at *you* rather than at an imaginary average student.

The form told me what you've used. These four are the other half — what you can
do right now, cold. They come from four different backgrounds on purpose, and
**almost nobody answers all four.** If you haven't seen something, leave it
blank: a blank tells me something a guess doesn't, and it costs you nothing.
Please don't look anything up — if you do, I'll cheerfully skip past something
you'd rather I explained.

---

<div class="q" markdown="1">

### 1. Molecular

A gene is preceded by a promoter. A protein called a *repressor* binds a site
that overlaps that promoter.

In one or two sentences: what physically stops the gene being expressed, and
what would happen to expression if you doubled the number of repressor molecules
in the cell?

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

### 2. Dynamical

A protein is made at a constant rate $\alpha$ (molecules per minute) and each
molecule is removed with probability per unit time $\gamma$, so

$$\frac{dx}{dt} \;=\; \alpha - \gamma x .$$

**(a)** What is the steady-state value of $x$?

<div class="rule"></div>
<div class="rule"></div>

**(b)** Starting from $x=0$, roughly how long does it take to get most of the
way there? Give the answer in terms of $\alpha$ and $\gamma$.

<div class="rule"></div>
<div class="rule"></div>

</div>

<div class="pagebreak"></div>

<div class="q" markdown="1">

### 3. Physical

An *E. coli* cell is about **1 femtolitre** ($10^{-15}$ L).

Approximately how many molecules are in that cell at a concentration of
**1 nM**? (Avogadro's number is $6\times10^{23}$ mol$^{-1}$.) An order of
magnitude is a complete answer; show whatever working you use.

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

### 4. Computational

```python
import numpy as np

def f(v):
    return np.array([v[1], -v[0]])

x = np.array([1.0, 0.0])
for _ in range(3):
    x = x + 0.1 * f(x)
print(x)
```

What does this print, approximately? And what is this code doing?

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

</div>

---

*Leave this with me on your way out. Nothing here goes near the gradebook — I
read them, I work out what to do differently, and that's the end of it. If a
question looked like a foreign language, that's fine, and it's exactly what I
want to know.*
