<!--
title: Session 6 — Regulation functions by counting states: answers
subtitle: Items 1 and 2, worked. Items 3 and 4 are PS3; those solutions post to bCourses after the deadline.
session: 6
-->

# Answers — items 1 and 2

The key to the two items we did **in the room**. Items 3 and 4 are **PS3**;
their solutions post to bCourses after the deadline, not here. The algebra was
never the hard part — the prose under each **▶** is.

<div class="rule"></div>

<div class="q" markdown="1">

## 1 · Simple repression — why there is no $f$

$$F_{\text{reg}} = \frac{1}{1 + [R]/K_m}$$

**▶ Why there is no $f$.** $f$ is the price of a **contact**: it is
$e^{-\varepsilon_{ap}/k_BT}$, the extra Boltzmann weight of a state in which two
proteins are touching each other on the DNA. In this architecture there is no
such state. LacI and RNAP cannot be bound at the same time, so no state exists
in which they could interact, so there is no interaction energy to charge.

The repressor works by **deleting a state from the sum**, not by changing the
rate of one. That is the mechanical difference between repression-by-occlusion
and activation, and it is why the two have different functional forms rather
than the same form with a sign flipped.

*Worth noticing:* a repressor that binds **next to** rather than **over** the
polymerase site is a different problem — that state does exist, and it carries
an $\omega$-like factor. Not every repressor occludes.

</div>

<div class="rule"></div>

<div class="q" markdown="1">

## 2 · Cooperative activation at $\lambda$ P$_{RM}$

| state | weight | transcribes at |
|---|---|---|
| empty | $1$ | 1 |
| cI$_2$ on $O_R2$ only | $a$ | $f$ |
| cI$_2$ on $O_R1$ only | $h$ | 1 |
| both | $\omega a h$ | $f$ |

**▶ Where $\omega$ goes.** On the **doubly-occupied state only**. $\omega$ is
an interaction between two bound dimers, so it can only appear in a state where
there are two bound dimers. It is not a property of a site, and it does not
multiply $a$ or $h$ on their own. Putting $\omega$ on a single-occupancy state
is the most common error on this item.

**▶ Why the $O_R1$-only state still transcribes at 1, not $f$.** $O_R1$ is not
in contact with polymerase. Its dimer recruits the *other* dimer; it does
nothing to transcription directly. The enhancement belongs to the contact, and
the contact belongs to $O_R2$.

$$\boxed{\;F_{\text{reg}} = \frac{1 + fa + h + f\omega a h}{1 + a + h + \omega a h}\;}$$

### The three checks

**▶ $\omega = 1$.** The expression factorises:

$$F_{\text{reg}} = \frac{(1+fa)(1+h)}{(1+a)(1+h)} = \frac{1 + fa}{1 + a}$$

The helper occupancy cancels completely: with no cooperativity a second site
that does not touch polymerase does **nothing at all** — not a weak effect,
exactly zero. Cooperativity is not a bonus on top of a second site; it is the
whole mechanism by which a second site matters.

**▶ $h = 0$.** Same expression, $F_{\text{reg}} = (1 + fa)/(1 + a)$: the
single-site result from the lecture, sensitivity $s = (\sqrt f - 1)/(\sqrt f + 1)
= 0.54$ at $f = 11$.

**▶ $[\mathrm{cI}_2] \to \infty$.** Both $a$ and $h$ grow without bound and the
$ah$ terms dominate top and bottom:

$$F_{\text{reg}} \longrightarrow \frac{f\omega a h}{\omega a h} = f$$

$\omega$ cancels. So does $K_{R1}$. **The helper site cannot raise the
ceiling**, and no amount of cooperativity will do it either — at saturation
every dimer that can be bound is bound, and what is left is the one contact
that fires the promoter. Cooperativity buys sharpness, not amplitude.

### Where $\omega$ comes from, and why two papers give different answers

The slide showed $s = 0.93$ with the helper against $0.54$ without, from Bintu
et al.'s Figure 2, computed with $f \approx 11$ and $\omega \approx 100$.

Ackers, Johnson & Shea measured that interaction in 1982:
$\Delta G_{12} = -1.99 \pm 0.06$ kcal/mol at 37 °C, which is $\omega = 25$, and
their Table 3 is on the slide. So where does 100 come from? **The same
laboratory, at the same temperature, ten years later.** Koblan & Ackers,
*Biochemistry* 31:57 (1992), Table II, 37 °C: $\Delta G_{12} = -2.7 \pm 0.3$
kcal/mol, which is $\omega = 80$ with a range of 49 to 130. Bintu's 100 sits
inside that. This is one group revising its own number with a better method —
quantitative footprint titration analysed simultaneously across the wild-type
operator and three reduced-valency mutants.

Three things are worth taking from that, and none of them is "scientists
disagree."

**The 1982 value is outside the 1992 interval.** $-1.99$ is not in
$[-3.0, -2.4]$. The earlier number was displaced, not merely imprecise.

**The later error bar is five times wider.** $\pm 0.06$ became $\pm 0.3$,
because the 1992 confidence intervals include systematic differences between
separate experiments and between operator templates, not only the imprecision of
one fit. A tighter error bar is not automatically a better measurement. It is
often a narrower definition of "error", and you cannot tell which from the
number alone.

**Cooperativity is temperature-invariant; site affinity is not.** Across 5–37 °C
the 1992 paper finds $\Delta G_{12}$ between $-1.9$ and $-3.0$ with no
interpretable trend, while the intrinsic affinities move steadily and
*differentially* — $\Delta G_1$ goes from $-12.5$ to $-13.5$ kcal/mol as the
temperature falls. So the quantity that changes with temperature is the
**discrimination between the two sites**: $K_{R2}/K_{R1}$ is 26 at 37 °C and 92
at 5 °C. Bintu's "realistic" ratio of 25 is the 37 °C row.

### And now the result worth the whole detour

Put each temperature's *measured* pair into the expression you derived and ask
what happens to the sharpness:

| T (°C) | $\omega$ | $K_{R2}/K_{R1}$ | $s$ |
|---|---|---|---|
| 37 | 80 | 26 | 0.92 |
| 30 | 75 | 20 | 0.93 |
| 20 | 172 | 73 | 0.91 |
| 10 | 102 | 85 | 0.86 |
| 5 | 31 | 92 | 0.76 |

Both inputs swing by a factor of three to five. **The sharpness barely moves**
until the cell is colder than anything $\lambda$ normally sees. The design is
robust to precisely the parameters that are worst measured — and you could not
have known that from staring at the error bars, only from pushing them through
the model.

That is the argument for deriving a regulation function rather than quoting one.
A formula you built yourself is a formula you can feed a bad parameter and find
out whether it matters.

</div>
