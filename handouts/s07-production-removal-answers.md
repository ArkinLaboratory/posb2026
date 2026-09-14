<!--
title: Session 7 — The same two curves, four times: answers
subtitle: Items 1 and 2, worked. Items 3 and 4 are PS3; those solutions post to bCourses after the deadline.
session: 7
-->

# Answers — items 1 and 2

The key to the two items we did **in the room**. Items 3 and 4 are **PS3**;
their solutions post to bCourses after the deadline, not here. The drawing was
never the hard part — the prose under each **▶** is.

<div class="rule"></div>

<div class="q" markdown="1">

## 1 · The constitutive unit — what the stability argument does not use

$$p^* = \frac{\alpha_0}{\mu} = \frac{23.1}{0.0231} = 1000 \ \text{molecules}$$

**▶ Name one thing you could change about the production curve that would leave
the stability argument untouched.** Almost anything: make it fall with $p$, make
it rise and saturate, put a bump in it. The argument only needs the gap
$\alpha(p) - \mu p$ to go from **positive to negative** as $p$ increases through
the crossing. It never asks what $\alpha(p)$ is.

That is not a throwaway. It is why the same argument survives into two
dimensions on Tuesday, where you cannot draw a single crossing at all and have
to reason about the sign of a flow instead. A stability criterion that depends
on the functional form is a criterion you have to re-derive for every circuit;
this one you do not.

*Worth noticing:* the one thing that **would** break it is a production curve
that crosses the removal line from below with a steeper slope. You will meet
exactly that crossing in item 3 — work out for yourself what the sign of the gap
does either side of it.

</div>

<div class="rule"></div>

<div class="q" markdown="1">

## 2 · Negative autoregulation — which curve moved

**Fix the level.** At the crossing, production equals removal:

$$\frac{\alpha}{1 + p^*/K} = \mu\, p^* = \alpha_0
\qquad\Longrightarrow\qquad
\alpha = \alpha_0\left(1 + \frac{p^*}{K}\right)$$

With $K = p^*$ that is $\alpha = 2\alpha_0 = 46.2$ per minute — the **repression
ratio**, and it is the promoter strength you have to order.

**▶ Which curve moved, and which did not.** The **production** curve moved
twice: down, when repression was added, and back up, when $\alpha$ was raised to
restore the target. The **removal** curve never moved at all — it is $\mu p$
before and after, because negative autoregulation does not touch $\gamma$ or the
growth rate.

So the synthesis rate **at the crossing** is $\mu p^* = \alpha_0 = 23.1$ per
minute, exactly what it was in item 1. At steady state, NAR is free.

**It is not free overall, and that distinction is the session.** The bill
$\alpha = 46.2$ is what the promoter fires at while $p$ is still small and the
operator still empty — early in the transient, which is when the extra protein
gets made. The lunch is not free; it is prepaid. PS3 asks you to price it over a
day against the tag route, which pays every minute forever instead of once.

**▶ Why it is faster.** At $p = p^*/2 = 500$: item 1 has production $23.1$ and
removal $11.6$, a gap of $11.5$. Item 2 has production $46.2/1.5 = 30.8$ and the
same removal $11.6$, a gap of $19.2$ — **two-thirds larger**. The gap *is*
$dp/dt$, so the NAR circuit is climbing harder at the same level, and it keeps
that advantage all the way up because its production curve is falling toward the
crossing while the flat one just waits there. Half-time $16.8$ min against
$30.0$ — a **1.79-fold** speed-up. That is the same as the best degradation tag
in Andersen 1998 buys ($1.75$), to within the precision of a measured half-life;
do not read the 2% as a win. What matters is that NAR gets it **without moving
the removal line at all**. The ratio that would match the tag exactly is $1.94$.

**▶ Let $K \to \infty$.** The repressor never occupies the operator, so the
promoter never sees it; $\alpha/(1+p/K) \to \alpha$, and the required $\alpha$
collapses to $\alpha_0$. A circuit with an operator nothing binds is a
constitutive circuit — and notice you can say that without doing the limit.

**▶ Make it aggressive: $K = p^*/10$.** Then $\alpha = 11\alpha_0 = 254$ per
minute: an eleven-fold stronger promoter, and a much faster circuit. But the
synthesis rate at the crossing is **still** $\mu p^* = 23.1$. The steady-state
cost did not move, because the removal curve did not move and the crossing is
where the two agree.

**What changed and what did not is the whole result.** Speed came from the
*shape* of the production curve; cost is set by the *crossing*, and the crossing
is pinned by removal. That is why a degradation tag — which moves the removal
line — is the expensive route and this one is not.

*The honest caveat:* aggressive repression is not free in practice. An
eleven-fold promoter is eleven-fold leaky before the repressor accumulates, the
transient overshoot is larger, and you have spent a strong promoter and a tight
operator that you might have wanted for something else.

</div>
