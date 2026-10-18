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

**Say once, and do not belabour it:** only two of those can happen in a cell
that has just been made. From an empty cell every gene starts at 0, so the
output's first move is always upward — a **static-1 needs a circuit that is
already running**, which is what handout item 3(d) has them do. It is also
why, in a cold start, the kind carries no information the settled value did
not already give you: settles to 0 and it is static-0, settles to 1 and it
is dynamic, every time.

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

## Centre, at fix-separate — what actually decides it

The slide has the computed table. The board has the one line it comes down
to. Write the line **before** the table goes up, and leave it:

> **an absent activator holds a gene off — an absent repressor lets it fire**

**ASK before showing the slide:** *we refuted "balance is enough". Is "OFF
when empty" enough?* Most of the room will say yes, because it is the answer
the previous two slides set up. It is not, and the slide has the
counterexample: take $Z = \mathrm{NOR}(\lnot A, \lnot B)$ — already balanced
— and bolt an activator-driven output onto it. Now it is OFF when empty
**and** balanced, and it still glitches three times in four.

Then the row that does the other half of the work, and it is worth slowing
down for:

> $g = \mathrm{BUF}(A)$, out $=$ a promoter needing $g$, blocked by $B$
> — two genes, **unbalanced** (A in two, B in one), **clean in all four**,
> and it computes $A \wedge \lnot B$, the classifier we have failed to build
> all hour

**ASK:** *why does this one get away with unequal legs?* Because the late
signal is the **activator**. Write the condition as the inequality it is:

$$\text{depth(repressors)} \;\le\; \text{depth(activators)}$$

**CHECK out loud:** a repressor arriving *early* is harmless — the gate is
held off either way. Equal depth is the special case, not the condition.
That is the whole reason balance looked like the answer for two slides.

**IF ASKED** *so can I just put an activator on the output of anything?* No,
and (ii) is why: $Z$ is a NOR, so $Z$ is already **wrong**, and the
$\mathrm{BUF}$ relays the wrong value one tick later. The condition has to
hold at every gene on the route, not only the last. You cannot repair a
circuit at its output.

**IF ASKED** *is the last column a theorem?* It is a **sufficient**
condition — it refuses some circuits that are in fact clean — checked by
exhaustion over every two- and three-gate network in this model
(`cold_start_safe`, `tests/test_logic.py`). Every gate here has one unit of
delay and real promoters do not. Say that; it is ten seconds and it is the
honest end of the segment.

> **This surface has been wrong twice.** First "unequal paths cause it",
> refuted by $Z$. Then "fix the promoter, not the wiring", refuted by the
> padded repair. Then "you need both", refuted by the two rows above. If you
> find yourself about to state a *new* sufficient condition at the board,
> don't — point at the computed column instead.

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
3. The inequality at **fix-separate** — the computed slide carries the
   verdict column; the board version is for the room that wants to see why
   a late activator is safe and a late repressor is not. Keep the one-line
   rule even if you cut the derivation of it.

Do **not** cut the counting at nor-debrief. The wrong number is the one thing
on this sheet that the room will otherwise carry out of the building.
