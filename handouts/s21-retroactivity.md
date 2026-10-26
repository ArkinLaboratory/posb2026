<!--
title: Session 21 — The same derivation, four times
subtitle: A home guide. The first is worked for you; by the fourth the scaffolding is gone. Answers are released after the session.
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

**So the dynamics.** With $f(X)$ whatever drives the total — here
$f(X) = k - \gamma X$ —

$$\boxed{\;\frac{dX}{dt} \;=\; \frac{f(X)}{1 + R(X)}\;}$$

**Read it.** A load does not add a term. It **divides the rate**, by a factor
that depends on where you are. At $X = 0$ the division is by
$1 + p_{\text{tot}}/K_d$; once $X \gg K_d$ the sites are full, $R \to 0$, and
the division goes away.

**▶ Why does that step follow?** $f(X)$ is untouched — the same $k - \gamma X$
it always was. It is tempting to conclude that the steady state is therefore
untouched too. State the assumption that conclusion needs, in one sentence.

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

**(b)** So free $X$ falls. Take the easy case first: $K_d \ll X$, so the sites
are essentially full and $C \approx p_{\text{tot}}$. Write the fractional drop
in free $X$:

$$\frac{X_T - X_{ss}}{X_T} \;\approx\; \underline{\qquad\qquad}$$

**(c)** Put the numbers in: $p_{\text{tot}} = 300$, $X_T = 1000$. The drop is
<span class="blank"></span>%.

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

**(d)** In the protected model, the loaded system must make $p_{\text{tot}}$
extra molecules before it reaches the same half-way point, at synthesis rate
$k$. The unloaded half-time is $\ln 2/\gamma$. Put those together to get the
weak-load slowdown as a multiple of $p_{\text{tot}}/X_T$.

<div class="rule"></div>

**(e)** Your answer to (d) is a pure number. Which one, to four figures?

<div class="rule"></div>

**(f)** Past $K_d \approx X_T$ the slowdown really does fall away. Explain why,
using (a) — and say why this is not a way of escaping the load.

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
