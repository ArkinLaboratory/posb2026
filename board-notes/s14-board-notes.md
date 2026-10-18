<!--
title: Session 14 — Board notes
subtitle: Review by working five motions, three of them at the board, not by re-presenting eleven sessions. Nothing from Thursday's paper appears here.
session: 14
-->

# Board notes

Print this and carry it. Session 14 is **review and worked problems**. There **is**
a deck — `s14-review` — and it carries five derivations as step runs plus the
figures. These notes are the stage directions that go with it: what to ask,
where to stop, and what to cut if you are short. The board keeps the ledger (the two
boxes from Board 1), the improvised answers, and nothing that is assessed.

**The governing rule for this hour: nothing on Thursday's paper appears here.** Not
its circuits, not its parameter sets, not its figures. Every example below is
deliberately a different circuit from the one the exam uses on the same skill, and
that is not an accident you may improvise away from at the board. If a student asks
whether something is on the exam, the answer is the scope sheet, not a hint.

**Five motions, and why these five.** The first three are moves this course asked
students to *watch* rather than *do*. The fourth — basins — is the one that was
taught at the board only, and `docs/lecture-design.md` 5b forbids that for anything
assessed, which is why it is now on slides and in the handout. The record is
specific:

| motion | what they actually practiced | what is missing |
|---|---|---|
| follow a disturbance round a loop | the result (odd rings oscillate) stated in s11 and in PS5 | the walk itself, out loud, on a MIXED loop, where edges and flips are different counts |
| signs of a Jacobian | `toggle_jacobian` once in code (PS4 Q2a); eigenvalues from numbers everywhere | reasoning from wiring to sign pattern. s08 *defines* $g_1,g_2$ as negated partials, so the sign bookkeeping was engineered out |
| draw a time course | watched the s10 panels projected; drew nullclines and rate curves | no handout or problem set has ever asked for a time trace |
| say which state a circuit reaches | saw the picture at the board in s9 and after | it appears in no slide, handout or problem set — **this is the one the deck exists for** |
| find a divide with one variable | never | the handout's item 4, on a one-gene autoactivator: a rate-balance sketch, three crossings, and the divide as a NUMBER |

**Conventions.** **ASK** — put it to the room before writing, and the answer to
expect. **POINT** — turn and point at the board rather than the screen. **IF
ASKED** — the question that always comes.

<div class="rule"></div>

## Open: what the hour is for

Say it plainly, once: *this is not a summary of eleven sessions. It is three things
you have seen me do and have not done yourself.* Then hand out
`s14-review-practice.md` and leave it face down until the first worked example is on
the board.

<div class="rule"></div>

## Board 1 — the round trip

Draw three boxes in a triangle: **X ⊣ Y, Y ⊣ Z, Z → X** — two bars and one arrow.
Then walk it, out loud, with a finger:

> nudge **X** up → **Y** down → **Z** up → **X** UP.

Write under it: **two flips, even, comes back unchanged.**

**Two bars and an arrow — never an all-repression ring.** A ring whose every arm is a
repression is what Thursday asks about, and drawing one here is rehearsing the
question rather than teaching the walk.

**ASK before you walk it a second time:** *does it matter how strong each repression
is, for deciding whether it comes back flipped?* No — strength decides whether it
comes back *shrunk*. **Those are two separate questions and they are the whole of
this.** Write the two words apart on the board and box them:

$$\textbf{FLIPPED?} \qquad\qquad \textbf{SHRUNK?}$$

Leave that up for the rest of the hour. Everything in motion 1 hangs off it.

**Then the odd case — change exactly one edge.** Rub out the **first bar** and make
it an arrow: now **X → Y, Y ⊣ Z, Z → X**, one bar in three arms. Walk it again:
X up → Y **up** → Z **down** → X **down**. **Comes back reversed.** **ASK:** *so can
THIS one be a clock?* Fish for: only if it also comes back unshrunk, and only if the
trip takes long enough. Flipped is necessary, never sufficient — that is the sentence
they most often get wrong.

**Keep exactly one repression in it.** Turning every arm into a repression gives you
Thursday's B3.1, and that is the easiest slip to make at the board, because it is the
picture you have drawn all term. One bar, not more.

**POINT at FLIPPED?:** no amount of gain fixes a failure here. Gain is the *other*
box — and passing both still is not enough on its own, because the trip has to take
long enough as well. This is the sentence worth the hour.

**IF ASKED** *"why does an even loop have two states and not one?"* — because
whichever way it is pushed, it pushes itself further that way; it runs to one
extreme or the other and the two extremes are the two states. Do not go near
eigenvectors.

**Then release them onto item 1** of the sheet. They have a FOUR-gene mixed loop,
and then the same loop with exactly one edge changed — the verdict reverses and
nothing else moves.

<div class="rule"></div>

## Board 1b — the line that divides the plane  *(now on slides; this is the ASK list)*

**The segment is on the deck now** (`26 – 39 min`), with a four-step run and the
mutual-activation figure, and item 4 of the practice sheet is the written exercise
on a one-gene autoactivator.
So this is no longer a board teaching — it is what to ask while the slides are up.
Do not re-derive it on the board; the slides move at the clicker's speed and the
room should be answering, not copying.

The circuit on the slides is **mutual activation** — X → Y and Y → X — with states
*both off* and *both on*. **It is not a toggle, and do not redraw it as one at the
board**: Thursday's phase plane is a different circuit, and an improvised toggle
here is rehearsal of B1.3.

**ASK, with the figure up:** *the cell sits with both genes off. I give it a brief
pulse of X and then stop. Does it come back?* Fish for: **depends how far**. Then
push: **depends how far in WHICH direction?**

**The number is the whole segment.** The saddle is at 0.382, so everyone reaches for
"get X past 0.382." But the pulse raises X **alone**, so the cell ends on the
**x-axis** with no Y made at all — and the divide crosses that axis at **0.711**. A
pulse to 0.5 is past the middle point and still falls back off.

**POINT at where the red curve meets the axis.** Say the reason in one line: *Y has
to exist before it can hold X up, and when the pulse ends there is none.*

**POINT:** this is why a two-state circuit is memory and not just a picture with two
dots in it — the dots are the states, the divide is what remembers.

**Do not** take questions about inducer thresholds here. That is session 9's other
mechanism — a *parameter* moves and a fixed point is destroyed — and conflating the
two is the error the exam row is written to separate. If it comes up, say the
difference in one line: *kick the state, or move the landscape.*

<div class="rule"></div>

## Board 2 — signs from wiring

Write the two-line rule, and nothing else:

$$\frac{\partial \dot{x}_i}{\partial x_i}: \text{ own removal} \Rightarrow -
\qquad
\frac{\partial \dot{x}_i}{\partial x_j}: \;
j \dashv i \Rightarrow - , \quad j \to i \Rightarrow +$$

**ASK:** *where did the production term go in the diagonal?* It is there only if the
species acts on **itself**. In the toggle it does not, so the diagonal is just
$-1$. This is the step they get wrong.

Work the **activator–repressor** on the board — three negative, one positive — then
**stop and hand them the three-gene cascade** on the sheet, whose Jacobian is
triangular and has four entries that are exactly **zero**.

**The payoff is the triangle.** A triangular matrix's eigenvalues are its diagonal,
which here is −1, −1, −1 at every parameter value: the cascade cannot be unstable and
cannot oscillate. The zeros above the diagonal *are* the statement that nothing feeds
back, so there is no round trip to pass or fail. That ties Board 2 back to Board 1.

**Only those two patterns.** Any other two-gene sign pattern you might reach for is
a Thursday question on those same equations — work the activator–repressor and the
cascade, and stop.

**IF ASKED** *"do we need the trace–determinant plane?"* — no. It was handed to you
once as a reference surface and it is not how anything this term was decided.

**Do not** let this run long. The rule is two lines; the value is in them doing it.

<div class="rule"></div>

## Board 3 — draw a curve

**Three things make a curve: where it starts, how fast it leaves, where it ends.**
Write exactly that. Draw the simple on-step: starts at zero, steepest at the start,
flattens onto $\beta/\gamma$, half-way at one half-life, within a few percent by
four.

**ASK:** *which of the three does negative autoregulation change, if you add it to a
gene and touch nothing else?* Expect "the initial slope." Push back: at $t = 0$ there
is **no protein**, so there is nothing repressing anything — the departure rate is
the same $\beta$. What changes first is **where it ends**, which drops.

**Leave "faster" open.** Do not supply the comparison that makes the word mean
something; that is a question they should carry into Thursday, and A-part items turn
on being able to state it themselves. One line is enough: *two curves that end in
different places can be compared in more than one way, and the ways disagree — know
which one you mean.*

**POINT:** compare at each curve's **own** half-way time, never at the endpoints.

**If the room is slow here**, draw the first curve for them and let them draw only
the second. The skill is the second one.

<div class="rule"></div>

## What to cut if you are short

In this order, last first:

1. The one-edge change at the end of item 1. The four-gene loop already makes the
   point; the pair makes it twice.
2. The *"why does that step follow?"* line under item 2.
3. **Never cut Board 1's two boxes.** FLIPPED? and SHRUNK? is the one idea that is
   worth more on Thursday than anything else in this hour, and it is the one most
   likely to be missing.

<div class="rule"></div>

## Close

Two sentences, no more. The exam asks you to *use* this material, not recite it —
and a correct answer with no reason earns half, so the reason is where you spend
your time. Point them at the scope sheet for anything else and end on time.
