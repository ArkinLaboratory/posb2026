<!--
title: Session 21 — The same derivation, four times
subtitle: A home guide. Sections 1 and 2 re-run Thursday's derivation so you can do it cold. Sections 3 and 4 go past it — the numbers there are on no slide. Answers are released after the session.
session: 21
-->

# The same derivation, four times

One regulator $X$, made at rate $k$ and removed at rate $\gamma$. Downstream
sits a module that reads it: $p_{\text{tot}}$ binding sites, dissociation
constant $K_d$. Binding is fast compared with everything else.

$$X + p \rightleftharpoons C, \qquad C(X) = \frac{p_{\text{tot}} X}{K_d + X}$$

Throughout, write $X_T = k/\gamma$ for what the regulator would reach with
nothing listening, and use the reference numbers $k = 10$, $\gamma = 0.01$ —
so $X_T = 1000$ — with $K_d = 1$ and $p_{\text{tot}} = 300$ when a number is
wanted.

**One physical question decides everything below**, and it is worth writing at
the top of your own page before you start: *while the regulator is sitting in
the complex, is it still being removed?*

At each transition the sheet asks *why does that step follow?* Answer in
writing before you go on.

---

## 1 · Fully worked — where the retroactivity comes from

**The total.** Free plus parked:

$$X_T^{\text{inst}} = X + C(X)$$

**Differentiate.** $C$ depends on time only through $X$, so the chain rule
gives

$$\frac{dX_T^{\text{inst}}}{dt} = \left(1 + \frac{dC}{dX}\right)\frac{dX}{dt}$$

**Name the derivative.** That bracket is the whole of it:

$$R(X) \;=\; \frac{dC}{dX} \;=\; \frac{p_{\text{tot}} K_d}{(K_d + X)^2}$$

**So the dynamics.** With $f(X)$ the law the **total** obeys,

$$\boxed{\;\frac{dX}{dt} \;=\; \frac{f(X)}{1 + R(X)}\;}$$

**Read it.** A load does not add a term. It **divides the rate**, by a factor
that depends on where you are. At $X = 0$ the division is by
$1 + p_{\text{tot}}/K_d$; once $X \gg K_d$ the sites are full, $R \to 0$, and
the division goes away.

**▶ Why does that step follow?** The load never touched $f$, so it is tempting
to conclude that the steady state is untouched too. But nothing above said
what $f$ is. Name the one physical fact about the complex that decides it, and
say in one sentence why the conclusion needs that fact to go one particular
way.

<div class="rule"></div>
<div class="rule"></div>

---

## 2 · Last step blank — the complex is protected

Suppose the site **shields** the regulator: while bound, it is not degraded and
not diluted. Then only free $X$ is removed, so the total obeys

$$\frac{d(X + C)}{dt} \;=\; k - \gamma X$$

**▶ Setting the left side to zero gives $X_{ss} = $** <span class="blank"></span>,
**which depends on $p_{\text{tot}}$ how?** <span class="blank"></span>

**▶ Why does that step follow?** You have just shown there is no steady-state
cost at all. But the response time *does* change. In one sentence: what is the
load costing you, if not level?

<div class="rule"></div>
<div class="rule"></div>

---

## 3 · More blank — the complex is diluted

Now suppose the complex is removed like everything else — the cell is growing
and dilutes bound and free alike. Then **both** terms are removed:

$$\frac{d(X + C)}{dt} \;=\; k - \gamma X - \gamma C$$

**(a)** Set the left side to zero. What is pinned now?

$$X + C(X) \;=\; \underline{\qquad\qquad}$$

**(b)** **Use $K_d = 500$ for the rest of this section**, not the $K_d = 1$ at
the top of the sheet. The sites are no longer anywhere near full, so you cannot
write $C \approx p_{\text{tot}}$ and you have to solve it. Substitute $C(X)$
into your answer to (a) and clear the denominator. You should get a quadratic:

$$X^2 + (K_d + p_{\text{tot}} - X_T)\,X - X_T K_d \;=\; 0$$

**(c)** Put the numbers in — $p_{\text{tot}} = 300$, $X_T = 1000$, $K_d = 500$
— and take the positive root.

$$X_{ss} = \underline{\qquad\qquad} \qquad
\frac{X_T - X_{ss}}{X_T} = \underline{\qquad\qquad}\%$$

**(d)** The saturated shortcut — assume the sites are full, so the drop is just
$p_{\text{tot}}/X_T$ — would have answered 30%. Your answer is smaller. Compute
$C(X_{ss})$ and you will find it is exactly the number of molecules free $X$
lost. Say in one sentence what sets the size of the drop, given that it is not
the site count.

**▶ Why does that step follow?** You now have two models that disagree about
whether the level moves, and the algebra cannot choose between them. Design the
**measurement** that does. One sentence, and say what each outcome would mean.

<div class="rule"></div>
<div class="rule"></div>

---

## 4 · Entirely yours — what affinity does and does not touch

**(a)** Compute $\displaystyle\int_0^{\infty} R(X)\,dX$. You do not need to
integrate anything — you need to notice what $R$ is the derivative of.

<div class="rule"></div>

**(b)** Say in one sentence what that integral *means* physically, in terms of
molecules the loaded system has to make on its way up.

<div class="rule"></div>

**(c)** Hence: a colleague proposes escaping the load by engineering a weaker
operator — raising $K_d$ by two orders of magnitude. What happens to the
response time, and why? Then say what *does* change, and what it costs them.

<div class="rule"></div>

**(d)** Thursday's board got the protected model's weak-load slowdown as a
clean multiple of $p_{\text{tot}}/X_T$, by counting the extra molecules the
loaded system must make before it reaches *the same* half-way point. **That
argument fails in the diluted model.** Say which step of it breaks, and why.

<div class="rule"></div>

**(e)** Thursday's figure showed the diluted ratio running from about 1.44 at
the light-load end to about 1.71 at the heavy end. Using your answer to (d),
say why **no** constant can be right there — not a different constant, none.

<div class="rule"></div>

**(f)** Past $K_d \approx X_T$ the slowdown really does fall away. Explain why,
using (a) — and say why this is not a way of escaping the load.

<div class="rule"></div>

**(g)** Part (a) integrated over *all* $X$. But the system only ever travels
from $0$ to $X_T$, so what it actually pays on the way up is

$$\int_0^{X_T} R(X)\,dX \;=\; \underline{\qquad\qquad}$$

Evaluate it at $K_d = 1$ and at $K_d = 100$, with $p_{\text{tot}} = 300$ and
$X_T = 1000$. Thursday's sweep was *nearly* flat, not exactly flat. Say which
part of that your two numbers account for — and then name one feature of that
curve they do **not** account for. (Look at the shape of the sweep on the left
of the figure, not just its ends.)

<div class="rule"></div>
<div class="rule"></div>

---

## Before Tuesday

Aoki *et al.*, *Nature* 570:533 (2019) — an antithetic integral controller
built from two molecules that destroy each other. Read the step responses.

Then ask the question this session has prepared you for: **what does dilution
do to the guarantee?**

**PS8 goes out at the end of this session** and is due 19 November. It covers
sessions 18, 20, 21 and 22.
