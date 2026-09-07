<!--
title: Session 4 — Where a regulation function comes from: answers
subtitle: Items 1 and 2, worked. Items 3 and 4 are PS1; those solutions post to bCourses after the deadline.
session: 4
-->

# Answers — items 1 and 2

This is the key to the two items we did **in the room**. Items 3 and 4 of your
handout are **PS1 Q4b and Q5**; their worked solutions post to bCourses after
the deadline, not here.

If your algebra differs from mine but your answer agrees, you are fine. The
prose under each **▶** is the part worth reading — the algebra was never the
hard bit.

<div class="rule"></div>

<div class="q" markdown="1">

## 1 · One site — the whole derivation

$$\mathrm{P} + \mathrm{X} \rightleftharpoons \mathrm{PX}, \qquad
K_d = \frac{[\mathrm{P}]\,x}{[\mathrm{PX}]}
\;\Longrightarrow\; [\mathrm{PX}] = \frac{[\mathrm{P}]\,x}{K_d}$$

$$f_{\text{bound}} = \frac{[\mathrm{PX}]}{[\mathrm{P}] + [\mathrm{PX}]}
= \frac{[\mathrm{P}]x/K_d}{[\mathrm{P}]\left(1 + x/K_d\right)}
= \frac{x/K_d}{1 + x/K_d} = \frac{x}{K_d + x}$$

A Hill function with $n = 1$ and $K = K_d$. The half-point sits at $x = K_d$,
which is what a dissociation constant means.

**▶ Why does $[\mathrm{P}]$ cancel, and what would have to be true for it not
to?**

$[\mathrm{P}]$ appears in **every term of both the numerator and the
denominator**, because every state of the promoter in this model is reached from
the empty promoter by multiplying by a factor. The empty state is the reference,
and a reference state always divides out of a fraction of states.

It would fail to cancel if the promoter could occupy a state that is **neither
empty nor reachable from empty by binding X** — a second conformation, a
competing repressor, a state with RNA polymerase bound. Then the denominator
carries a term that is not proportional to $[\mathrm{P}]$ and the cancellation
breaks. That is the whole subject of session 6: once the denominator is a real
partition function over states you chose, "which states did you include" becomes
a modelling decision with consequences you can measure.

</div>

<div class="rule"></div>

<div class="q" markdown="1">

## 2 · $n$ sites, all or nothing

$$\mathrm{P} + n\,\mathrm{X} \rightleftharpoons \mathrm{PX}_n, \qquad
K_d = \frac{[\mathrm{P}]\,x^{\,n}}{[\mathrm{PX}_n]}
\;\Longrightarrow\; [\mathrm{PX}_n] = \frac{[\mathrm{P}]\,x^{\,n}}{K_d}$$

$$f_{\text{bound}} = \frac{[\mathrm{PX}_n]}{[\mathrm{P}] + [\mathrm{PX}_n]}
= \frac{x^{\,n}/K_d}{1 + x^{\,n}/K_d} = \frac{x^{\,n}}{K_d + x^{\,n}}$$

To read that as $x^n/(K^n + x^n)$, set $K^n = K_d$:

$$\boxed{\,K = K_d^{\,1/n}\,}$$

**▶ Your $K$ is not $K_d$. What is it?**

$K$ is the **concentration of X at half occupancy** — a concentration, in molar.
$K_d$ here is an equilibrium constant for a reaction that consumes $n$ molecules
of X at once, so it has units of **concentration$^n$**. They are not the same
kind of object, and the fastest way to catch the error is dimensional analysis
rather than algebra: a quantity with units of M$^n$ cannot be a half-point.

Two promoters with the **same $K$ and different $K_d$** therefore differ in $n$.
They switch at the same input concentration and with different sharpness: same
threshold, different steepness. That is exactly the pair of knobs you want
separated when you are designing a circuit, and it is why quoting $K_d$ alone
tells you almost nothing about how a promoter behaves.

**▶ "No partially bound states" is a lie. Whose lie is it?**

It is the **infinite-cooperativity limit**: binding the first X must make binding
the rest so favourable that the intermediate states are never populated. Real
cooperativity is finite, so intermediates always have some occupancy and the
true curve is shallower than $x^n/(K^n + x^n)$ with $n$ = the number of sites.

It is a *good* lie when the free-energy gain from the first binding event is
large compared with $k_BT$ — strongly cooperative systems such as haemoglobin
sit close enough to it to be useful, which is where the whole formalism came
from.

To find out whether it is a good lie **here**: fit the measured dose–response for
$n$ and compare it with the **structurally known site count**. If the fitted $n$
comes back well below the number of sites, the intermediates are populated and
the two-state idealisation is doing real damage. That comparison — a fitted
exponent against a counted number — is the subject of the last twenty minutes of
the session, and of ConcepTest 2.

</div>

<div class="rule"></div>

**Items 3 and 4** are PS1 Q4b and Q5. Solutions post to bCourses after the
deadline. If you are stuck before then, the discussion hour is the place — the
answer to Q5 in particular turns on a distinction (*which* fraction you are
computing) rather than on algebra, and that is much faster to sort out in
conversation.
