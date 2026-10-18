<!--
title: Session 16 — Board notes
subtitle: The occupancy derivation and the state count are projected one line at a time; the board carries the counting, the depths, and the two conditions.
session: 16
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records
what gets *written*.

**Four board moments**, named by the deck's segment rather than by the clock:
the four-state count at **nor-build**, the two XNOR networks at
**nor-debrief**, the two conditions at **fix-separate**, and $S(n)$ at
**dna-count**. Nothing here is on a slide except as a finished line.

**Conventions.** **ASK**: put it to the room before writing, and the answer
to expect. **CHECK**: the sanity check to do out loud, because doing them is
the habit being taught. **IF ASKED**: the question that always comes.
**CUT**: what to drop if the hour is going long, chosen now rather than
later.

<div class="rule"></div>

## Before class — left wing, and leave it up

Two things, and they stay up the whole period.

**The tick rule.**

> every gene reads its inputs **as they were last tick**, all genes update
> together, and at $t = 0$ every gene is at 0

**The three kinds.**

> **static-0** — should have stayed 0, went up and came back
> **static-1** — should have stayed 1, went down and came back
> **dynamic** — should have changed once, changed more than once

The rest of the board stays empty. It fills at **nor-build**.

<div class="rule"></div>

## Centre, at nor-build — where the gate comes from

This is the derivation the projected run shows one line at a time. Do it on
the board **first**, then advance the slides over it; the slides are the
record, the board is the rate.

Two operator sites on one promoter. Four states, and their weights relative
to the empty promoter:

$$1, \qquad r_A, \qquad r_B, \qquad r_A r_B
\qquad\text{where } r = [\text{repressor}]/K$$

**ASK before writing the next line:** *what do we do with four weights?* Add
them. They came off this in session 6 and most of the room will say it.

$$Z = 1 + r_A + r_B + r_A r_B = (1 + r_A)(1 + r_B)$$

**CHECK out loud:** it factorises. Say why that is not a coincidence — the
two sites are independent, so the partition function of the pair is the
product of the two one-site partition functions. If they are *not*
independent, it does not factorise, and that is cooperativity.

Only the empty promoter fires, so

$$P_{\text{on}} = \frac{1}{(1+r_A)(1+r_B)}$$

**ASK:** *push $r_A$ to zero and to infinity, and the same for $r_B$. Four
corners. What are they?* $1, 0, 0, 0$.

Write underneath, and leave it:

> **that is NOR, and nobody chose it — the DNA layout wrote it**

**IF ASKED** *what if the two sites overlap?* Then there is no doubly-bound
state, $Z = 1 + r_A + r_B$, and the gate is still NOR because the empty state
is still the only one that fires. Good question, and the answer is that NOR
is robust to that detail.

<div class="rule"></div>

## Right wing, at nor-debrief — the two networks, and the counting

Take the networks the room actually produced and sort them against the two
on the slide. Then do the counting on the board, because the counting is
where the error is.

Write the recipe network as a list:

> $\lnot A$, $\lnot B$, $P = \mathrm{NOR}(A,B)$,
> $Q = \mathrm{NOR}(\lnot A,\lnot B)$, $R = \mathrm{NOR}(P,Q)$,
> out $= \mathrm{NOT}\ R$

**ASK:** *how deep is it?* Expect "three". Then trace two routes with a
finger, out loud:

> $A \to P \to R \to$ out  — **three**
> $A \to \lnot A \to Q \to R \to$ out  — **four**

**Four and three, not three and two.** Say that the number people reach for
is the number of *layers in the list*, and the number that matters is the
number of *genes on a route*. This is the one place in the session where the
room will write down a wrong number and not notice.

Then the minimum, four gates with paths of 3 and 2. Do not derive it — say
that an exhaustive search over two-input NOR networks finds it and that the
search is the compiler's job.

**Leave on the board, and do not explain it:**

> **the paths are not the same length — in both of them**

The hazard segment collects on that line. It is much stronger if they wrote
the numbers themselves.

<div class="rule"></div>

## Centre, at fix-separate — the two conditions

The slide has the computed table. The board has the logic, as four boxes:

|  | OFF when empty | ON when empty |
|---|---|---|
| **paths equal** | clean | glitches |
| **paths unequal** | glitches | glitches |

**ASK before filling it in:** *we have refuted "balance is enough". Is "OFF
when empty" enough?* Most of the room will say yes, because it is the answer
the previous two slides set up. It is wrong, and the deck's own first repair
is the counterexample.

Write the padded repair beside the table:

> $\mathrm{Act} = \mathrm{NOT}\ R_2$, $R_3 = \mathrm{BUF}(\mathrm{Act})$
> — OFF when empty, unbalanced, and static-0 in **all four** cases

**CHECK:** which cell of the table is still empty of evidence? None — every
glitching cell has a named circuit from this hour behind it.

**IF ASKED** *so is the top-left cell a theorem?* No. It is true of these
circuits under a model that gives every gate the same unit delay. Say so.
That caveat is the honest end of the segment and it is worth ten seconds.

<div class="rule"></div>

## Right wing, at dna-count — counting the orders

Three lines, and it is worth doing them rather than quoting the formula.

**ASK:** *what does a state of a staggered device record?* Which invertases
have fired, **and in what order**.

So a state is an ordered sequence drawn from a subset of the $n$ available:

$$\underbrace{\binom{n}{k}}_{\text{which }k} \times
\underbrace{k!}_{\text{in what order}}
\qquad\text{summed over } k = 1 \ldots n$$

$$S(n) = \sum_{k=1}^{n} k!\,\binom{n}{k}$$

**CHECK at $n = 2$:** $2 + 2 = 4$, plus the starting state is five — and five
is what Ham's Fig. 1C draws, which is on the screen two slides earlier. Do
this check. It is the only thing standing between this formula and a number
nobody can verify.

$n = 3$ gives 15, against 8 for three independent bits. $n = 10$ gives nearly
$10^7$, against 1024.

**IF ASKED** *why doesn't nesting do this?* Because nested inversions
commute: firing $a$ then $b$ lands on the same arrangement as $b$ then $a$,
so the order is not recoverable and there is nothing extra to count.

**IF ASKED** *what about firing the same invertase twice?* Good question and
the honest answer is that Ham's count does not include it — a state is a
sequence of *distinct* invertases. Whether a real device reaches more
arrangements than that is open, and it is in `DESIGN.md` §8.5 rather than on
a slide.

<div class="rule"></div>

## CUT, in this order

1. **dna-count** at the board — quote $S(n)$ from the slide and keep only the
   $n=2$ check against Ham's five-state graph.
2. The **IF ASKED** on overlapping operator sites at nor-build.
3. The four-box table at **fix-separate** — the computed slide carries it;
   the board version is for the room that wants to see the quantifier.

Do **not** cut the counting at nor-debrief. The wrong number is the one thing
on this sheet that the room will otherwise carry out of the building.
