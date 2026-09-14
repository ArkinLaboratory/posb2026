<!--
title: Session 7 — The same two curves, four times
subtitle: Two in the room, two on the problem set. Start wherever the scaffolding stops helping you.
session: 7
-->

# The same two curves, four times

One picture, four wirings, and **less of my working shown each time**. **We do
items 1 and 2 in the room** — nine minutes, and item 1 is already done. Items 3
and 4 are on **PS3**.

The procedure, every time:

<table>
<tr><th>1</th><td>Draw the production rate against $p$.</td>
    <th>3</th><td>Mark every crossing.</td></tr>
<tr><th>2</th><td>Draw the removal rate on the same axes.</td>
    <th>4</th><td>Classify each by the <em>sign of the gap</em> either side.</td></tr>
</table>

Throughout, one host and one target: a protein that must sit at
$p^* = 1000$ molecules in *E. coli* dividing every 30 minutes, so
$\mu = \ln 2/30 = 0.0231\ \mathrm{min^{-1}}$. Unless a tag is added, $\gamma = 0$
and removal is dilution alone. The unregulated promoter that hits the target is
therefore $\alpha_0 = \mu p^* = 23.1$ proteins per minute.

---

<div class="q" markdown="1">

## 1 · Fully worked — the constitutive unit

No feedback, so production does not depend on $p$:

$$\frac{dp}{dt} \;=\; \underbrace{\alpha_0}_{\text{production}} \;-\; \underbrace{\mu\, p}_{\text{removal}}$$

**Draw them.** Production is a horizontal line at $23.1$. Removal is a straight
line through the origin of slope $\mu$ — a *fraction* of the pool leaves per
minute, so the amount leaving grows with the pool.

<svg viewBox="0 0 420 240" width="420" height="240" style="max-width:100%">
  <line x1="50" y1="200" x2="400" y2="200" stroke="#0B3A3F" stroke-width="2"/>
  <line x1="50" y1="200" x2="50" y2="20" stroke="#0B3A3F" stroke-width="2"/>
  <line x1="50" y1="120" x2="400" y2="120" stroke="#0E4F57" stroke-width="2.5"/>
  <line x1="50" y1="200" x2="370" y2="30" stroke="#0B3A3F" stroke-width="2" stroke-dasharray="5 4"/>
  <circle cx="200" cy="120" r="5" fill="#0E4F57" stroke="#0B3A3F" stroke-width="1.5"/>
  <text x="212" y="150" font-size="13" fill="#0B3A3F">p* = 1000</text>
  <text x="60" y="112" font-size="13" fill="#0E4F57">production = 23.1</text>
  <text x="288" y="52" font-size="13" fill="#0B3A3F">removal = &#956;p</text>
  <text x="210" y="225" font-size="13" fill="#0B3A3F">protein p</text>
  <text x="6" y="110" font-size="13" fill="#0B3A3F">rate</text>
</svg>

**Find the crossing.** $\alpha_0 = \mu p^*$, so $p^* = \alpha_0/\mu = 1000$.
That is the only thing the crossing tells you, and it is the *level*.

**Show it is stable, without solving anything.** To the right of the crossing
removal is above production, so $dp/dt < 0$ and $p$ falls back. To the left,
production is above removal, so $p$ rises. The gap **changes sign** through the
crossing, from positive to negative — that is what stable means, and notice the
argument never used the functional form of either curve.

**▶ Why does that matter?** Name one thing you could change about the
production curve that would leave this stability argument untouched.

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 2 · The last step is yours — negative autoregulation

Now the protein represses its own promoter, so production falls as $p$ rises:

$$\frac{dp}{dt} \;=\; \frac{\alpha}{1 + p/K} \;-\; \mu\, p$$

Take $K = p^* = 1000$, which is a **repression ratio of 2** — a modest circuit.

**Draw both curves on these axes.** Removal first, then production.

<svg viewBox="0 0 420 240" width="420" height="240" style="max-width:100%">
  <line x1="50" y1="200" x2="400" y2="200" stroke="#0B3A3F" stroke-width="2"/>
  <line x1="50" y1="200" x2="50" y2="20" stroke="#0B3A3F" stroke-width="2"/>
  <text x="210" y="225" font-size="13" fill="#0B3A3F">protein p</text>
  <text x="6" y="110" font-size="13" fill="#0B3A3F">rate</text>
</svg>

**▶ Fix the level.** Repression pulls the production curve down, so the
crossing moves left and the cell misses its target. Choose $\alpha$ so the
crossing sits back at $p^* = 1000$. One line:

$$\alpha \;=\; $$

<div class="rule"></div>

**▶ Which curve moved, and which did not?** Answer for the production curve and
for the removal curve separately, and say what that means for the rate of
synthesis **at the crossing**.

<div class="rule"></div>
<div class="rule"></div>

**▶ Why is it faster?** Compare the vertical gap between the two curves at
$p = p^*/2$ in item 1 and in item 2. Which is larger, and what does the gap
*mean*?

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 2 *continued* · two checks, and do both — they are worth more than the drawing

**▶ Let $K \to \infty$.** You should recover item 1 exactly. Say why in words,
not algebra.

<div class="rule"></div>

**▶ Now make the repression aggressive:** $K = p^*/10$. What happens to
$\alpha$, and what happens to the synthesis rate at the crossing? One of those
two changes and one does not, and that is the entire cost result.

<div class="rule"></div>
<div class="rule"></div>

</div>

---

<div class="q" markdown="1">

## 3 · On PS3 — positive autoregulation

The protein now **activates** its own promoter, with $n$ sites bound
cooperatively and a leaky basal rate:

$$\frac{dp}{dt} \;=\; \alpha_{\text{basal}} + \alpha_{\max}\frac{p^{n}}{K^{n} + p^{n}} \;-\; \mu\, p$$

Find every crossing and classify each one. Then find the value of $n$ at which
the middle pair appears, and say what happens to a cell sitting exactly at the
unstable crossing.

**And the question that matters:** $\mu$ is the *slope of the removal line*.
What happens to your answer when the same construct is grown in minimal medium?

</div>

---

<div class="q" markdown="1">

## 4 · On PS3 — the design item

You are handed a protein that must reach $p^*$ in **under 15 minutes** and then
hold that level for **a day**. You may add a degradation tag, wire negative
autoregulation, or both.

Pick a route, **price it** — proteins per minute, integrated over the day — and
defend the choice. Then say what you would measure to know whether the circuit
you built is the circuit you designed.

</div>
