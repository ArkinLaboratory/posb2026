<!--
title: Session 9 — Four problems, and the scaffolding falls away
subtitle: Ten minutes in two halves. Start wherever the scaffolding stops helping you.
session: 9
-->

# Four problems, and the scaffolding falls away

The symmetric toggle, with $\alpha = 2$ throughout so that the crossing on the
diagonal is $x = 1$ by hand:

$$\frac{du}{dt} = \frac{\alpha}{1+v^{n}} - u \qquad\qquad \frac{dv}{dt} = \frac{\alpha}{1+u^{n}} - v$$

Tuesday's two tools, and nothing else: **fixed points are where the nullclines
cross**, and a crossing is a **saddle exactly when $g_1 g_2 > 1$**, with

$$g_1 = \frac{n\,u\,v^{\,n-1}}{1+v^{n}}, \qquad g_2 = \frac{n\,v\,u^{\,n-1}}{1+u^{n}},
\qquad \lambda = -1 \pm \sqrt{g_1 g_2}.$$

At each transition the sheet asks *why does that step follow?* Answer in
writing before you go on.

---

## 1 · Fully worked — $n = 4$, $\alpha = 2$

**The diagonal crossing.** On $u = v = x$ both equations read $x + x^{5} = 2$,
and $x = 1$ solves it: $1 + 1 = 2$.

**Is it a saddle?** At $u = v = 1$, $g_1 = g_2 = 4 \cdot 1 \cdot 1/(1+1) = 2$,
so $g_1 g_2 = 4 > 1$. Yes: $\lambda = -1 \pm 2 = +1,\ -3$. The cell does not sit
there.

**The other two crossings.** They are off the diagonal and mirror each other.
`stability_report(toggle_model(2, 2, n=4))` puts them at $(0.118,\ 2.000)$ and
$(2.000,\ 0.118)$. Check one by hand: $2/(1 + 2.000^{4}) = 2/17 = 0.118$ ✓ and
$2/(1 + 0.118^{4}) = 2/1.0002 = 2.000$ ✓.

**▶ Why does that step follow?** Why is there always a crossing on the diagonal,
and why do the other two come as a mirror pair?

<div class="rule"></div>
<div class="rule"></div>

---

## 2 · Last step blank — classify the pair

At $(u, v) = (0.118,\ 2.000)$, with $n = 4$:

$$g_1 = \frac{4 \cdot 0.118 \cdot 2.000^{3}}{1 + 2.000^{4}} = \underline{\qquad\qquad}
\qquad
g_2 = \frac{4 \cdot 2.000 \cdot 0.118^{3}}{1 + 0.118^{4}} = \underline{\qquad\qquad}$$

**▶ $g_1 g_2 = $** <span class="blank"></span> **so the point is** <span class="blank"></span>, with $\lambda = $ <span class="blank"></span>.

**▶ Why does that step follow?** One factor comes out roughly twenty times the
other. Say in one sentence why the *product* is what decides, and what it means
that one factor is so small.

<div class="rule"></div>


---

<div class="q" markdown="1">

## 3 · Last two blank — $n = 1$, $\alpha = 2$

**The diagonal crossing.** $x + x^{2} = 2$, so $x = 1$ again.

**▶ Build $g_1$ and $g_2$ there,** then classify:

<div class="rule"></div>
<div class="rule"></div>

**▶ How many crossings are there in total, and why?** Sketch the two nullclines
for $n = 1$ on the axes and say what Tuesday's handout proved about this case.

<svg viewBox="0 0 420 170" width="420" height="170" style="max-width:100%">
  <line x1="50" y1="140" x2="400" y2="140" stroke="#0B3A3F" stroke-width="2"/>
  <line x1="50" y1="140" x2="50" y2="15" stroke="#0B3A3F" stroke-width="2"/>
  <text x="220" y="162" font-size="13" fill="#0B3A3F">u</text>
  <text x="30" y="80" font-size="13" fill="#0B3A3F">v</text>
</svg>

</div>

---

<div class="q" markdown="1">

## 4 · Bare problem — weaken one arm

Back to $n = 4$. Keep $\alpha_1 = 2$ and lower $\alpha_2$ from 2 toward 1, so
the $u$ arm is now the stronger one. Which nullcline moves, and how? Which of
the three crossings dies first, what does it die *with*, and what is the cell
left in? Draw it; then name the event in the language of today's lecture, and
name the plasmid in the paper that did this to itself.

<svg viewBox="0 0 420 170" width="420" height="170" style="max-width:100%">
  <line x1="50" y1="140" x2="400" y2="140" stroke="#0B3A3F" stroke-width="2"/>
  <line x1="50" y1="140" x2="50" y2="15" stroke="#0B3A3F" stroke-width="2"/>
  <text x="220" y="162" font-size="13" fill="#0B3A3F">u</text>
  <text x="30" y="80" font-size="13" fill="#0B3A3F">v</text>
</svg>

<div class="rule"></div>
<div class="rule"></div>

</div>
