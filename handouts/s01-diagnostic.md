<!--
title: Session 1 — Diagnostic
subtitle: Ungraded. Affects nothing. Eight minutes.
session: 1
-->

# Diagnostic

**Name** <span class="blank" style="width:2.6in"></span> **Course** BioE 147 / 247 *(circle one)*

This is not graded and does not enter your grade in any way. Its only purpose is
to tell me where this room actually is, so I can set the pace honestly rather
than guess.

The four questions below come from four different backgrounds on purpose.
**Almost nobody answers all four.** If you have never seen something, leave it
blank — a blank is more useful to me than a guess, and it costs you nothing.

---

### 1. Molecular

A gene is preceded by a promoter. A protein called a *repressor* binds a site
that overlaps that promoter.

In one or two sentences: what physically stops the gene being expressed, and
what would happen to expression if you doubled the number of repressor molecules
in the cell?

<div class="rule"></div>
<div class="rule"></div>

---

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

<div class="pagebreak"></div>

### 3. Physical

An *E. coli* cell is about **1 femtolitre** ($10^{-15}$ L).

Approximately how many molecules are in that cell at a concentration of
**1 nM**? (Avogadro's number is $6\times10^{23}$ mol$^{-1}$.) An order of magnitude is a complete answer; show whatever
working you use.

<div class="rule"></div>
<div class="rule"></div>

---

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

---

### 5. Where you are coming from

Tick anything you have **used**, not merely heard of.

<table>
<tr><th>Wet lab</th><td>&#9744; cloned a plasmid</td><td>&#9744; run a PCR</td>
    <td>&#9744; used a flow cytometer</td><td>&#9744; done a Western or qPCR</td></tr>
<tr><th>Mathematics</th><td>&#9744; solved an ODE by hand</td><td>&#9744; solved one numerically</td>
    <td>&#9744; linearised a system</td><td>&#9744; eigenvalues of a 2&times;2</td></tr>
<tr><th>Computing</th><td>&#9744; written a Python script</td><td>&#9744; used NumPy</td>
    <td>&#9744; used a Jupyter notebook</td><td>&#9744; used git</td></tr>
<tr><th>Coursework</th><td>&#9744; read a synbio paper</td><td>&#9744; built a genetic circuit</td>
    <td>&#9744; a controls course</td><td>&#9744; a stat-mech course</td></tr>
</table>

**One sentence: what do you want out of this course?**

<div class="rule"></div>
