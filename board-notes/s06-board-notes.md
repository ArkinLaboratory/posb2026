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
wiped.** The minute marks below moved on 13 September when the derivation was
restructured around the state table; the lines themselves did not change.

**RIGHT WING — two things, both in the room's own handwriting.** Retrieval
question 3 at minute 4, which stays until **minute 35**; and below it, at minute
12, **the room's list of what you can change in the lab**, which stays until the
ledger at **76**. This is the one exception to session 5's rule that the right wing
stays empty, and both entries earn it: the session's argument is that the old
answer is a special case of the new one, and that the Knobs column is not a
list you are handed but the list they already made before any mathematics.

<div class="rule"></div>

## Right wing — minute 4, written by whoever answers

$$\theta = \frac{[x]}{K_d + [x]}$$

Take it from the room. Do not tidy their notation into yours — you want *their*
version up there, because at **minute 35** you are going to point at it and say
*that is what the table gives you when you put the repressor's row back.*

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
Knobs/Constraints split, made by the room an hour before the ledger slide names
it.

Leave the list up. At minute **72** you point at it and say that this is
exactly what Ackers had, and at **76** that these are the Knobs.

**DO NOT WIPE.**

<div class="rule"></div>

## Line 1 — at minute 28, the last step of derivation 1

Written at step 6 of the first run, while the slide showing it is up.

$$p = \frac{[\mathrm{RNAP}]}{K_{\mathrm{RNAP}}} \qquad\qquad
K_{\mathrm{RNAP}} = N_{NS}\,e^{+\Delta\varepsilon / k_BT}$$

**This line is the one the whole session leans on and it is new.** Until it is
written, $p$ is a count ratio times a Boltzmann factor. After it, $p$ is a
concentration over a dissociation constant — the same kind of object as
$a = [A]/K_A$ at minute 42. Say that out loud when you write it.

**Notation, and it matters at the board.** The polymerase *count* is
$N_P$, parallel to $N_{NS}$ — never a bare capital $P$, which in this session
would collide with the weight $p$, the core-promoter site and the concentration
all at once. The site on the cartoons is labelled **core**, not P. Keep both
conventions on the board.

**ASK before writing $p$:** *what is the reservoir?* Expect "the cytoplasm" and
correct it: the **genome**. $N_{NS} = 5 \times 10^6$ non-specific sites, and
almost every polymerase in the cell is stuck to one of them.

**IF ASKED** *is $N_{NS}$ really the genome length?* — it is the number of
places a polymerase can sit non-specifically, which is of order the number of
base pairs. Bintu's figure legend uses $5 \times 10^6$ for *E. coli*. Do not
defend the second significant figure; the quantity is about to cancel.

<div class="rule"></div>

## Line 2 — at minute 35, on the general-form surface

Directly under line 1, and **box it**.

$$p_{\text{bound}} = \frac{p\,F_{\text{reg}}}{1 + p\,F_{\text{reg}}}
\qquad\qquad
\text{fold-change} = F_{\text{reg}} \qquad (p \ll 1)$$

Say what $F_{\text{reg}}$ **is** as you write it: the factor by which the
regulator multiplies the **odds** of finding polymerase on the promoter. An odds
ratio is exactly the kind of quantity in which uncountable things cancel — which
is the vote one minute later.

**Then turn to the right wing. This is the moment the session turns.** Put the
repressor's row back into the table and $F_{\text{reg}} = 1/(1+r)$ — which is
what the room wrote on that wing in the first five minutes, from a completely
different argument.

**ASK:** *so was session 4 wrong?* No. It was the special case, and it could not
have told you it was one. That distinction is what the midterm will ask about.

**IF ASKED** *why is the repressor's row deleted rather than given a small
weight?* — because the operator overlaps the core promoter, so the state does
not exist. A repressor binding *beside* the promoter keeps its row and carries
an interaction factor instead; both are real, and item 1 of the handout is the
occlusion case.

**POINT at line 1 while you write it.** The condition in the bracket is not
decoration — it is the entire content of ConcepTest 1, six minutes later, and
the room will vote on it.

**ASK:** *what have we not needed to know?* Expect silence, then take it
yourself: the number of polymerases, the size of the genome, and every binding
energy in the problem. Say it as a list of three. It is the best argument for
the method they will hear today.

**Do not ask it any earlier.** At minute 28 all three are still sitting inside
$p$ and the honest answer is the opposite one. Asking it during the counting
pre-teaches answer **B** to the vote at 36, which is the one wrong answer the
whole ConcepTest exists to catch.

<div class="rule"></div>

## Line 3 — at minute 48, the last step of derivation 2

Under line 2.

$$F_{\text{reg}} = \frac{1 + fa}{1 + a}, \qquad a = \frac{[A]}{K_A}$$

**Say the ceiling as you write it:** $s = (\sqrt{f}-1)/(\sqrt{f}+1) < 1$ for
every finite $f$. **One site cannot be made sharp**, however good the contact.
That is the specification the next vote hands them and cannot be met.

**IF ASKED** *where does the midpoint come from?* — $a = 1/\sqrt{f}$, so in a
log–log plot the middle is $F = \sqrt{f}$, not $F = f/2$. Put $f = 11$ in and
$s = 0.54$, which is the number printed in Bintu's Figure 2 legend. Do the
differentiation on the board only if the room asks for it.

<div class="rule"></div>

## What does **not** go on the board

- **The state tables.** All three are figures on the slides and the format is
  the handout's, which is the point — copying one out costs three minutes and
  buys nothing. Build the ROWS with the room by asking, then show the slide.
- $\lambda$ P$_{RM}$'s numbers. They are on the slide, they are read off a
  figure, and they are in the paper.
- Anything during the handout. Circulate instead.

<div class="rule"></div>

## If you are running late

Cut in this order:

1. **The $\lambda$ O$_R$ segment at 72 min** — down to two minutes: put up
   Table 3, say *these five measured numbers are the switch*, and move on.
2. **ConcepTest 3's argue-and-revote at 66 min** — take the first vote, give the answer,
   and keep the Limits column, which is where that content actually lives.
3. **Nothing else.** Do not cut the design ledger and do not cut the closing
   question: Thursday opens on it, and session 7 has no cold start without it.

**Never cut:** the third check on handout item 2 — $[\mathrm{cI}_2] \to \infty$
gives $f$ whatever $\omega$ is. If the room runs out of time to do it, do it
yourself on the board in one line. It is the session's design result and
everything on the ledger slide depends on it.
