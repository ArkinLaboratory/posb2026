<!--
title: Session 16 — Ticks, glitches and depth
subtitle: Three to work, one worked for you, one stretch. Everything starts at zero, and that is the whole difficulty.
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

Two of these can happen in a cell that has just been made. The third cannot,
and item 3(d) is where you find out why.

**One number for depth.** A chain of $n$ genes, each driving the next, with a
step at the input and every protein sharing a lifetime $\tau$:

$$t_{1/2}(n) \;=\; \text{time for the output to reach half its final value},
\qquad t_{1/2}(n) \;\approx\; \left(n - \tfrac{1}{3}\right)\tau .$$

**Two promoters, and the difference between them.** A gene behind a plain
repressed promoter is ON unless a repressor is bound. A gene behind a promoter
that **requires an activator** is OFF unless that activator is present; we
write $\mathrm{BUF}(X)$ for the one-input version, a gene that comes on one
tick after $X$ appears and is off before that.

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

*Why does that step follow?* — at $t = 1$ every gene whose repressors are all
still absent turns on at once. $R_2$ is a NAND, ON unless both its repressors
are present, and at $t = 0$ neither is. $R_3$ is a NOT, ON unless its
repressor is present, and at $t = 0$ $R_2$ is not. A gene reading only *other
genes* is therefore switched on in an empty cell. A gene reading an input
directly is not: $R_1 = \mathrm{NOT}\,B$ with $B = 1$ would stay off.

</div>

## 2 — Compile XNOR, and count the depths

<div class="q" markdown="1">

XNOR is 1 when $A$ and $B$ agree. Build it from NOT and NOR gates only.

**The recipe, if you want one.** Write the output as an OR over the rows where
it is 1; turn each row into a NOR of the complements of its literals; combine
the row terms with a NOR; invert. You may use any other route that works.

Write the network as a list of genes, each line saying what represses what.
You will not need all these lines.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

Count gates along every route from an input to the output. Count the output
gene itself.

$$\text{longest path} = \underline{\phantom{00000}} \text{ genes}, \qquad
\text{shortest path} = \underline{\phantom{00000}} \text{ genes}$$

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

Fill five rows, $t = 0$ to $t = 4$, for each input case. Every gene starts
at 0.

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

**(b)** Which input cases glitch, and which kind is each? One line per case.

| case | glitches? | which kind |
|---|---|---|
| $A=0,\ B=0$ | | |
| $A=0,\ B=1$ | | |
| $A=1,\ B=0$ | | |
| $A=1,\ B=1$ | | |

**(c)** Look at the $t = 1$ row of all four of your tables. What do the four
output values have in common, and which gene decided that?

<div class="rule"></div>
<div class="rule"></div>

**(d)** Now stop starting from an empty cell. Let the circuit settle at
$A = 1,\ B = 1$ — you have that state in your fourth table — and then drop
**both** inputs to 0 at $t = 0$, keeping the genes where they settled.

| $t$ | $R_1$ | $R_2$ | out |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

The output is 1 before the change and 1 after it. Which kind of glitch is
this, and why could it not have appeared anywhere in part (b)?

<div class="rule"></div>
<div class="rule"></div>

</div>

## 4 — How late is a four-gene chain?

<div class="q" markdown="1">

Four genes in a chain, every protein with the same lifetime $\tau$, a step at
the input at $t = 0$. **Use the rule of thumb, not the exact sum.**

$$t_{1/2}(4) \;\approx\; \underline{\phantom{000000}}\ \tau$$

By the rule of thumb, how much later is that than the three-gene chain?

$$\underline{\phantom{000000}}\ \tau$$

*Why does that step follow?* — would you have guessed that number before this
session? Most people underestimate depth. What about the **first** stage makes
it misleading?

<div class="rule"></div>

</div>

## 5 — Stretch: what actually decides it

<div class="q" markdown="1">

A circuit is **fail-safe** if its output gene is still off one tick after the
cell is made — that is, if the output promoter reads 0 while every protein in
the circuit is still absent. A NOT or NOR output is never fail-safe. A circuit
is **balanced** if every route from any input to the output has the same
number of genes.

Here are three circuits. All three compute something; two of them glitch.

| | the genes | OFF when empty? | paths equal? |
|---|---|---|---|
| **(i)** | item 1, then $\mathrm{Act} = \mathrm{NOT}\,R_2$, $R_3 = \mathrm{BUF}(\mathrm{Act})$ | yes | no |
| **(ii)** | $\lnot A$, $\lnot B$, $Z = \mathrm{NOR}(\lnot A, \lnot B)$, $\mathrm{out} = \mathrm{BUF}(Z)$ | yes | **yes** |
| **(iii)** | $g = \mathrm{BUF}(A)$, $\mathrm{out} =$ a promoter needing $g$, blocked by $B$ | yes | no |

Run three ticks of (ii) and three of (iii), at $A = 0,\ B = 0$.

<div class="rule"></div>
<div class="rule"></div>
<div class="rule"></div>

**(a)** (i) and (ii) glitch; (iii) does not. So neither "OFF when empty" nor
"equal paths" is the thing that matters. **What is true of (iii) that is false
of both the others?**

<div class="rule"></div>
<div class="rule"></div>

**(b)** State it as a rule about *when a signal arrives at a promoter*, and
say which kind of site — activating or repressing — you are allowed to be
late at.

<div class="rule"></div>
<div class="rule"></div>

</div>
