<!--
title: Session 6 — Regulation functions by counting states
subtitle: Two in the room, two on the problem set. Start wherever the scaffolding stops helping you.
session: 6
-->

# Regulation functions by counting states

Four promoters of increasing architecture, and **one procedure applied to all
four**, with less of my working shown each time. **We do items 1 and 2 in the
room** — ten minutes, and item 1 is already done. Items 3 and 4 are on **PS3**.

The procedure, every time:

<table>
<tr><th>1</th><td>List every state the promoter can be in.</td>
    <th>3</th><td>Say which states transcribe, and how fast.</td></tr>
<tr><th>2</th><td>Give each state a weight.</td>
    <th>4</th><td>Divide the transcribing weight by the total.</td></tr>
</table>

Throughout: $a = [A]/K_A$ is an occupancy variable, $p$ is the polymerase
weight, and $f = e^{-\varepsilon_{ap}/k_BT}$ is charged **only** to a state in
which two proteins are actually touching. Every answer below is taken in the
**weak-promoter limit** ($p \ll 1$), where the fold-change is the regulation
factor and $p$ cancels.

---

<div class="q" markdown="1">

## 1 · Fully worked — simple repression at a truncated lac promoter

lacUV5 cut down to a single operator $O_m$, with LacI$_4$ binding it. The
operator **overlaps the polymerase site**: the repressor and RNAP cannot both
be bound.

**List the states.** Three, not four. The missing one is what makes this repression.

| state | weight | transcribes? |
|---|---|---|
| empty | $1$ | no |
| LacI$_4$ on $O_m$ | $r = [R]/K_m$ | no |
| RNAP on the promoter | $p$ | yes, at rate 1 |
| *both* | — | **does not exist** |

**Divide the transcribing weight by the total.**

$$p_{\text{bound}} = \frac{p}{1 + r + p}$$

**Take the ratio to the unregulated promoter** ($r = 0$), which is what an
experiment reports:

$$\text{fold-change} = \frac{p/(1 + r + p)}{p/(1 + p)} = \frac{1 + p}{1 + r + p}$$

**Take the weak-promoter limit,** $p \ll 1$:

$$\boxed{\;F_{\text{reg}} = \frac{1}{1 + [R]/K_m}\;}$$

which is exactly the form you derived in session 4 from a binding equilibrium —
reached here by counting states, with no $[P]$ to cancel.

**▶ Why does that step follow?** There is no $f$ anywhere in this answer.
Answer from the *mechanism*, not the algebra: what would $f$ have been charged
for, and what about this architecture means there is nothing to charge?

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 2 · The last step is yours — cooperative activation at $\lambda$ P$_{RM}$

Two operators. cI$_2$ at $O_R2$ **activates** — it contacts polymerase, with
enhancement factor $f$. cI$_2$ at $O_R1$ does **not** contact polymerase at
all; it helps recruit the other dimer, through a cooperative interaction
$\omega$ between the two bound dimers. One protein species, so both occupancies
move together: write $a = [\mathrm{cI}_2]/K_{R2}$ and $h = [\mathrm{cI}_2]/K_{R1}$.

**List the states, and give each a weight.** Four of them. Two are filled in.

| state | weight | transcribes at |
|---|---|---|
| empty | $1$ | 1 |
| cI$_2$ on $O_R2$ only | $a$ | $f$ |
| cI$_2$ on $O_R1$ only | | |
| both | | |

<div class="rule"></div>

**▶ Where does $\omega$ go, and where does it not?** One line, before you
write the answer down.

<div class="rule"></div>

**Now divide, and take the weak-promoter limit.**

$$F_{\text{reg}} = $$

<div class="rule"></div>
<div class="rule"></div>

**Three checks, and do all three — they are worth more than the derivation.**

**▶ Set $\omega = 1$.** What should the expression become, physically, and does
it?

<div class="rule"></div>

**▶ Set $h = 0$** (delete $O_R1$). You should recover item 2 of the lecture.

<div class="rule"></div>

**▶ Let $[\mathrm{cI}_2] \to \infty$.** Show that the answer is $f$, **whatever
$\omega$ and $K_{R1}$ are.** This is one line, and it is the whole design
result: the helper site cannot raise the ceiling.

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 3 · On PS3 — two different proteins at *melAB*

MelR$_2^*$ binds the weak proximal operator $O2$ and activates. CRP$_2^*$ binds
the upstream operator $O1$, helps recruit MelR, and **does not itself activate**.

Two species now, so the two occupancies move independently. Write the state
list, the regulation factor, and then answer the question that matters:
**whose $f$ appears in the saturating fold-change, and why is there only one of
them?**

</div>

---

<div class="q" markdown="1">

## 4 · On PS3 — the design item

Design a promoter whose fold-change is **AND-like** in two inducers: low unless
both are present. Give the architecture, the state list, the regulation factor,
and the truth table it produces.

Then say **which knob you turned** to make it AND-like rather than OR-like, and
what you would have to measure to know whether your promoter actually does it.

</div>
