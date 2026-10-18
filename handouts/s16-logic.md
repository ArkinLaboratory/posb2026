<!--
title: Session 16 — Ticks, glitches and depth
subtitle: Four problems. Everything starts at zero, and that is the whole difficulty.
session: 16
-->

# Ticks, glitches and depth

**The rule for every table on this sheet.** Time runs in ticks. At each tick
every gene looks at the values of its inputs **as they were at the previous
tick** and updates. All genes update together. At $t = 0$ the cell has just
been made, so **every gene is at 0** and the inputs are already at their given
values.

**The three kinds of glitch**, named by what the output was supposed to be
doing:

| | the output should have | what it does instead |
|---|---|---|
| **static-0** | stayed at 0 | goes up and comes back |
| **static-1** | stayed at 1 | goes down and comes back |
| **dynamic** | changed once | changes more than once on the way |

**One number for depth.** A chain of $n$ genes, each driving the next, with a
step at the input and every protein sharing a lifetime $\tau$:

$$t_{1/2}(n) \;=\; \text{time for the output to reach half its final value},
\qquad t_{1/2}(n) \;\approx\; \left(n - \tfrac{1}{3}\right)\tau .$$

---

## 1 — Fully worked: the classifier, $A = 1$, $B = 0$

<div class="q" markdown="1">

The circuit from class. $R_1 = \mathrm{NOT}\,B$. $R_2$ is one gene behind two
promoters, one repressed by $A$ and one by $R_1$, so
$R_2 = \mathrm{NAND}(A, R_1)$. $R_3 = \mathrm{NOT}\,R_2$, and $R_3$ is the
output. With $A = 1$ and $B = 0$ the table settles to $R_3 = 1$.

| $t$ | $R_1$ | $R_2$ | $R_3$ |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 0 | 0 |
| 3 | 1 | 0 | 1 |
| 4 | 1 | 0 | 1 |

Read the last column: 0, 1, 0, 1, 1. The output was supposed to change once,
from its reset value to 1. It changed three times. **That is a dynamic
hazard**, and it is the case whose correct answer is 1 — the circuit arrives
at the right answer having first given it, taken it back, and given it again.

*Why does that step follow?* — at $t = 1$ every gene turns on at once. $R_2$
is a NAND, which is ON unless both its repressors are present, and at $t = 0$
neither is. $R_3$ is a NOT, which is ON unless its repressor is present, and
at $t = 0$ $R_2$ is not. An empty cell is a cell with every repressor gate
already switched on.

</div>

## 2 — Compile XNOR, and count the depths

<div class="q" markdown="1">

XNOR is 1 when $A$ and $B$ agree. Build it from NOT and NOR gates only. Write
the network as a list of genes, each line saying what represses what.

$$\underline{\phantom{0000000000000000000000000000000000000000}}$$
$$\underline{\phantom{0000000000000000000000000000000000000000}}$$
$$\underline{\phantom{0000000000000000000000000000000000000000}}$$
$$\underline{\phantom{0000000000000000000000000000000000000000}}$$
$$\underline{\phantom{0000000000000000000000000000000000000000}}$$
$$\underline{\phantom{0000000000000000000000000000000000000000}}$$

Count gates along every route from an input to the output.

$$\text{longest path} = \underline{\phantom{00000}} \text{ genes}, \qquad
\text{shortest path} = \underline{\phantom{00000}} \text{ genes}$$

<div class="rule"></div>

*Why does that step follow?* — a different group will hand in a different
network that computes the same table. What, if anything, makes one of them
better?

<div class="rule"></div>
<div class="rule"></div>

</div>

## 3 — A different circuit

<div class="q" markdown="1">

Three genes, two inputs, wired differently from item 1:

$$R_1 = \mathrm{NOT}\,A, \qquad
R_2 = \mathrm{NOR}(B,\, R_1), \qquad
\mathrm{out} = \mathrm{NOT}\,R_2 .$$

Fill four ticks for each input case. Every gene starts at 0.

| $t$ | $R_1$ | $R_2$ | out | | $t$ | $R_1$ | $R_2$ | out |
|---|---|---|---|---|---|---|---|---|
| **$A=0,\ B=0$** | | | | | **$A=0,\ B=1$** | | | |
| 0 | | | | | 0 | | | |
| 1 | | | | | 1 | | | |
| 2 | | | | | 2 | | | |
| 3 | | | | | 3 | | | |
| 4 | | | | | 4 | | | |
| **$A=1,\ B=0$** | | | | | **$A=1,\ B=1$** | | | |
| 0 | | | | | 0 | | | |
| 1 | | | | | 1 | | | |
| 2 | | | | | 2 | | | |
| 3 | | | | | 3 | | | |
| 4 | | | | | 4 | | | |

**(a)** What function does it settle to? Write the truth table.

$$\begin{array}{c|c|c}
A & B & \mathrm{out} \\ \hline
0 & 0 & \underline{\phantom{00}} \\
0 & 1 & \underline{\phantom{00}} \\
1 & 0 & \underline{\phantom{00}} \\
1 & 1 & \underline{\phantom{00}}
\end{array}$$

**(b)** Which input cases glitch, and which kind is each?

<div class="rule"></div>

**(c)** One sentence. Not "because it glitches." **What in the wiring let a
wrong value out?**

<div class="rule"></div>
<div class="rule"></div>

</div>

## 4 — How late is a four-gene chain?

<div class="q" markdown="1">

Four genes in a chain, every protein with the same lifetime $\tau$, a step at
the input at $t = 0$. Do not compute the sum; use the rule of thumb.

$$t_{1/2}(4) \;\approx\; \underline{\phantom{000000}}\ \tau$$

How much later is that than the three-gene chain?

$$\underline{\phantom{000000}}\ \tau$$

<div class="rule"></div>

*Why does that step follow?* — would you have guessed that number before this
session? Most people underestimate depth. What about the first stage makes it
misleading?

<div class="rule"></div>

</div>

## 5 — Stretch: two conditions, and neither is enough

<div class="q" markdown="1">

A circuit is **fail-safe** if its output is 0 in a cell that has only just
been made. It is **balanced** if every route from any input to the output has
the same number of genes.

Item 3's circuit is neither. Item 1's is neither. In class we saw a balanced
circuit that still glitches.

**Build a circuit that is fail-safe and NOT balanced, and show that it still
glitches.** You may use an activator: a gene whose promoter *requires* a
protein to be present rather than being blocked by one.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

*This one is on the problem set, and it is the one that is actually hard.*

</div>
