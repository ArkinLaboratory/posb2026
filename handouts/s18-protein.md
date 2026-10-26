<!--
title: Session 18 — The same cycle, three times, with less of my working each time
subtitle: One derivation. Start wherever the scaffolding stops helping you.
session: 18
-->

# The same cycle, three times

A protein that exists already, and the only thing changing is whether a
phosphate is on it. One kinase pushing right, one phosphatase pushing left:

$$\text{forward} = \frac{V_1 W}{K_{m1} + W}, \qquad
  \text{back} = \frac{V_2 W^{*}}{K_{m2} + W^{*}}, \qquad
  W + W^{*} = W_T .$$

Two tools, and nothing else. **Steady state is equal and opposite flux**, not
zero flux — both enzymes run flat out and the pool sits still. And **the total
is conserved**, which is the first time in this course that anything has been.

Throughout, $w = W^{*}/W_T$ is the fraction modified, and

$$k_1 = \frac{K_{m1}}{W_T}, \qquad k_2 = \frac{K_{m2}}{W_T}.$$

Those two are the whole session. They are dimensionless, they are **not**
properties of the enzymes, and a bigger pool makes them **smaller**.

At each transition the sheet asks *why does that step follow?* Answer in
writing before you go on.

---

## 1 · Fully worked — where the curve crosses one half

**Set the fluxes equal.**

$$\frac{V_1 W}{K_{m1} + W} = \frac{V_2 W^{*}}{K_{m2} + W^{*}}$$

**Put the conservation law in.** $W = W_T(1-w)$ and $W^{*} = W_T w$, so every
numerator carries a factor of $W_T$:

$$\frac{V_1 W_T (1-w)}{K_{m1} + W_T(1-w)} = \frac{V_2 W_T\, w}{K_{m2} + W_T w}$$

**Divide through by $W_T$.** It cancels from the numerators and divides into
each $K_m$ downstairs, leaving $k_1$ and $k_2$ behind:

$$\frac{V_1 (1-w)}{k_1 + 1 - w} = \frac{V_2\, w}{k_2 + w}$$

**Divide by $V_2$.** Only the ratio survives — five parameters are now three:

$$\frac{(V_1/V_2)(1-w)}{k_1 + 1 - w} = \frac{w}{k_2 + w}$$

**Now set $w = 1/2$** and ask what ratio puts it there:

$$\frac{(V_1/V_2)\cdot\tfrac12}{k_1 + \tfrac12} = \frac{\tfrac12}{k_2 + \tfrac12}
\qquad\Longrightarrow\qquad
\left(\frac{V_1}{V_2}\right)_{50} = \frac{k_1 + \tfrac12}{k_2 + \tfrac12}$$

**▶ Why does that step follow?** $W_T$ divided out of the equation. Explain,
in one sentence, why the pool size nevertheless still matters.

<div class="rule"></div>

## 2 · Partly worked — the one point every response curve passes through

Now ask a different question. Sweep $V_1/V_2$ at several different
saturations and you get a family of curves — and they all meet at a single
point, at $V_1/V_2 = 1$. Find the $w$ at which they cross, as a function of
$k_1$ and $k_2$ only.

**The condition.** Put $V_1/V_2 = 1$ into the quadratic. The $w^2$ term
disappears, because its coefficient is $(1 - V_1/V_2)$ — which is why this is
the one stimulus where the model has an exact answer. Show it.

$$\rule{11cm}{0.4pt}$$

$$\rule{11cm}{0.4pt}$$

**The answer**, which you should reach:

$$w = \frac{k_2}{k_1 + k_2} = \frac{K_{m2}}{K_{m1} + K_{m2}}$$

**▶ Why does that step follow?** $W_T$ appears in both $k_1$ and $k_2$ and
cancels in the ratio, so the crossing point does not move when you change the
pool size — at all, exactly. Say in one sentence what that means for a designer
who wants to shift *where* the switch sits.

<div class="rule"></div>

## 3 · Scaffolding gone — how sharp, and in what units

A cycle has $k_1 = k_2 = k$ and you may vary $V_1/V_2$.

**(a)** Goldbeter and Koshland's ruler: $R$ is the $V_1/V_2$ needed to reach
$w = 0.9$, divided by the $V_1/V_2$ needed to reach $w = 0.1$. Work out $R$ for
a plain Michaelis–Menten curve $y = x/(1+x)$. You should get a pure number,
the same for every $K$.

$$\rule{11cm}{0.4pt}$$

**(b)** A Hill curve of coefficient $n$ scores $81^{1/n}$ on that ruler. Invert
it to get $n$ in terms of $R$.

$$\rule{11cm}{0.4pt}$$

**(c)** For $k = 10^{-2}$ the model gives $R \approx 1.18$. What apparent Hill
coefficient is that? Compare it with hemoglobin, which is about 3.

$$\rule{11cm}{0.4pt}$$

**(d)** Nothing in this cycle binds cooperatively. In one sentence: where does
the sharpness come from?

$$\rule{11cm}{0.4pt}$$

**▶ Why does that step follow?** A sharper switch has a **smaller** $R$.
Explain why the ruler runs that way round.

<div class="rule"></div>

## 4 · The ledger — what you would actually turn

You have three things you can change: the expression ratio $V_1/V_2$, the two
Michaelis constants $K_{m1}$ and $K_{m2}$, and the pool size $W_T$.

| you want to move | which one, and why |
|---|---|
| **where the switch crosses** | |
| **how sharp it is** | |
| **where it fires** | |

**(e)** Two of those three answers are a promoter and one is protein
engineering. Which is which?

**(f)** One pair of goals cannot both be had. Name the pair, and say what the
trade is.

$$\rule{11cm}{0.4pt}$$

**(g)** The cycle costs ATP continuously, even when nothing is changing and
the output is not moving. Why — and what does that tell you about when **not**
to use this design?

$$\rule{11cm}{0.4pt}$$

<div class="rule"></div>

## Before Thursday

Mishra, Bepler, Teague, Berger, Broach & Weiss, *Science* **373** (2021) — a
toggle switch with no promoter in it, built from eleven phospho-in,
phospho-out elements. Come able to put their network on session 8's axes:
activity of one branch across, activity of the other up, the two nullclines
drawn, every intersection marked, and a statement about which are stable.

Their Fig. 4C is the control that earns the result. Work out what it is
controlling for before you read what they say about it.
