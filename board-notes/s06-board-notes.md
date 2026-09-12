<!--
title: Session 6 — Board notes
subtitle: One ledger, three lines, written once and never wiped — plus one line the room writes for you and you leave up.
session: 6
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written*.

**This session is not a board session.** Both derivations are step-slide runs.
The board carries **three ledger lines**, plus **the answer to retrieval
question 3**, which the room produces in the first five minutes and which you
must not wipe — the whole hinge depends on it still being there at minute 36.

**Conventions.** **ASK** — put it to the room before writing, and the answer to
expect. **POINT** — the moments you turn and point at the board rather than the
screen. **IF ASKED** — the question that always comes.

<div class="rule"></div>

## The board plan

Same room as sessions 3, 4 and 5: blackboard across the front, screen down in
the **centre**, a **left wing** and a **right wing**.

**LEFT WING — the ledger. Three lines, written as they are derived, never
wiped.**

**RIGHT WING — two things, both in the room's own handwriting.** Retrieval
question 3 at minute 4, which stays until minute 36; and below it, at minute 12,
**the room's list of what you can change in the lab**, which stays until the
ledger at 75. This is the one exception to session 5's rule that the right wing
stays empty, and both entries earn it: the session's argument is that the old
answer is a special case of the new one, and that the Knobs column is not a
list you are handed but the list they already made before any mathematics.

<div class="rule"></div>

## Right wing — minute 4, written by whoever answers

$$\theta = \frac{[x]}{K_d + [x]}$$

Take it from the room. Do not tidy their notation into yours — you want *their*
version up there, because at minute 36 you are going to point at it and say
*that is what you get when you set $f = 0$.*

**ASK:** *what did you have to assume to write that?* Expect: binding is fast
and at equilibrium. Good — that assumption survives today. Say so now, because
it is the one thing from session 4 that today does **not** overturn.

**DO NOT WIPE.** If a colleague uses the room before you, check it is still
there before you start.

<div class="rule"></div>

## Right wing — minute 12, the list the room makes

Closing question of the promoter-anatomy slide: **what can you actually change,
and what would you have to do to change it?** Take four or five and write them
up. What you are fishing for:

| they say | it moves | what it costs you |
|---|---|---|
| mutate the operator sequence | $K$ | cloning |
| move the site / change the spacing | whether the two proteins can touch at all | cloning |
| swap the core promoter | $p$ | cloning |
| mutate the protein surface | $\omega$ or $f$ | cloning, and much harder |
| add inducer | $[A]$ | a pipette, today, reversibly |

**ASK once they are up: which of these can you change during an experiment?**
Only the last. The rest you build once and then inherit — which is the
Knobs/Constraints split, made by the room forty minutes before the ledger slide
names it.

Leave the list up. At minute 75 you point at it and say that this is exactly
what Ackers had, and at 78 that these are the Knobs.

**DO NOT WIPE.**

<div class="rule"></div>

## Line 1 — at minute 20, during derivation 1

Written at step 5 of the first run, while the slide showing it is up.

$$p_{\text{bound}} = \frac{p\,F_{\text{reg}}}{1 + p\,F_{\text{reg}}}
\qquad\qquad
p = \frac{P}{N_{NS}}\,e^{-\Delta\varepsilon_p / k_BT}$$

**ASK before writing $p$:** *what is the reservoir?* Expect "the cytoplasm" and
correct it: the **genome**. $N_{NS} = 5 \times 10^6$ non-specific sites, and
almost every polymerase in the cell is stuck to one of them.

**IF ASKED** *is $N_{NS}$ really the genome length?* — it is the number of
places a polymerase can sit non-specifically, which is of order the number of
base pairs. Bintu's figure legend uses $5 \times 10^6$ for *E. coli*. Do not
defend the second significant figure; the quantity is about to cancel.

<div class="rule"></div>

## Line 2 — at minute 22, the last step of derivation 1

Directly under line 1, and **box it**.

$$\text{fold-change} = F_{\text{reg}} \qquad (p \ll 1)$$

**POINT at line 1 while you write it.** The condition in the bracket is not
decoration — it is the entire content of ConcepTest 1, six minutes later, and
the room will vote on it.

**ASK:** *what have we not needed to know?* Expect silence, then take it
yourself: the number of polymerases, the size of the genome, and every binding
energy in the problem. Say it as a list of three. It is the best argument for
the method they will hear today.

<div class="rule"></div>

## Line 3 — at minute 36, the last step of derivation 2

Under line 2.

$$F_{\text{reg}} = \frac{1 + fa}{1 + a}, \qquad a = \frac{[A]}{K_A}$$

**Then turn to the right wing.** This is the moment the session turns:

> Set $f = 0$. One state stops transcribing, and you get **that** — the thing
> you wrote in the first five minutes, from a completely different argument.

**ASK:** *so was session 4 wrong?* No. It was the special case, and it could
not have told you it was a special case. That distinction is what the midterm
will ask about.

**IF ASKED** *why is it $f = 0$ and not $f < 1$?* — $f < 1$ is a repressor that
binds *near* rather than *over* the polymerase site and makes it fire less
often. $f = 0$ is full occlusion. Both are real; item 1 of the handout is the
occlusion case and the answer sheet notes the other.

<div class="rule"></div>

## What does **not** go on the board

- The four-state weight table. It is on the slide and on the handout, and
  copying it out costs three minutes and buys nothing.
- $\lambda$ P$_{RM}$'s numbers. They are on the slide, they are read off a
  figure, and they are in the paper.
- Anything during the handout. Circulate instead.

<div class="rule"></div>

## If you are running late

Cut in this order:

1. **The $\lambda$ O$_R$ segment at 62 min** — down to two minutes: put up
   Table 3, say *these five measured numbers are the switch*, and move on.
2. **ConcepTest 3's argue-and-revote** — take the first vote, give the answer,
   and keep the Limits column, which is where that content actually lives.
3. **Nothing else.** Do not cut the design ledger and do not cut the closing
   question: Thursday opens on it, and session 7 has no cold start without it.

**Never cut:** the third check on handout item 2 — $[\mathrm{cI}_2] \to \infty$
gives $f$ whatever $\omega$ is. If the room runs out of time to do it, do it
yourself on the board in one line. It is the session's design result and
everything on the ledger slide depends on it.
