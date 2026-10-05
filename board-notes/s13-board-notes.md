<!--
title: Session 13 — Board notes
subtitle: The gain derivation is projected; the board carries the log-slope argument, the matching test, and the two bills.
session: 13
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written*.

**Three board moments.** Why a log slope, at 28. The matching test as four
numbers and two inequalities, at 38. And the two bills side by side, at 56,
which is the sentence the session exists to produce.

**Conventions.** **ASK**: put it to the room before writing, and the answer to
expect. **POINT**: turn and point at the board rather than the screen.
**IF ASKED**: the question that always comes.

<div class="rule"></div>

## Before class — left wing, the gate

Draw it once and leave it up all period. A promoter, a repressor arriving, a
protein leaving:

**x ⊣ [ P ] → y**

and underneath, the curve in one line:

$$y = y_{\min} + \frac{y_{\max}-y_{\min}}{1+(x/K)^{n}}$$

Leave the center board empty. It fills at 28.

<div class="rule"></div>

## Right wing, minutes 15–23 — the group answers

Three columns, one per question. Column 1 is the one every group reaches:
stage two's steep part sits on stage one's swing. Write their words, then write
the chain rule underneath them:

$$\frac{d\ln z}{d\ln x} = \frac{d\ln z}{d\ln y}\cdot\frac{d\ln y}{d\ln x}$$

**ASK at 23, before sorting:** *what has to be true for that product to be
bigger than either factor?* Both factors above 1, at the same input. That is
the whole session in one line, and it is better coming from them.

Column 3 is where to spend the time. Hooshangi's own **first** three-stage
build failed this way — a mutant λ promoter with an elevated low output,
replaced with the original OR1 (p. 3585) — but that was a prototype they
discarded, so it shows that leak can ruin a stage rather than explaining the
seven percent the shipped circuit 3 delivered. Their candidates for that are on
the same page: noise limiting the gain from added elements, and LacI expressed
far above what full repression of cI needs.

<div class="rule"></div>

## Center, at 28 — why a log slope

This is the step where the room will nod along without understanding, so make
them do it. Write:

$$\text{electronics: } \frac{dV_{\text{out}}}{dV_{\text{in}}}
\qquad\qquad \text{here: } \frac{d[\text{TetR}]}{d[\text{aTc}]} = ?$$

**ASK:** *what are the units of the second one?* Molecules of TetR per molecule
of aTc — and nobody chose those units for a reason. **Then ASK:** *what happens
to that number if I report TetR in nM and you report it in molecules per cell?*
It changes by a thousand, and the gate did not.

**Write the fix:**

$$G = \frac{d\ln y}{d\ln x} = \frac{x}{y}\frac{dy}{dx}
\qquad \text{(fractional out per fractional in — no units)}$$

**And the method, because nothing else demonstrates it.** $|G| = 1$ does not
factor. Evaluate $|G|$ on a grid, find the peak, then bisect on each side.
Write those three words on the board — *grid, peak, bisect* — because that is
what handout item 2 asks for and what `posb.digital` does.

**IF ASKED** whether this is standard: Daniel et al. call the same quantity
sensitivity (p. 623), and for a chain of identical gates measured in the same
units the two definitions agree about where the restoring region is.

<div class="rule"></div>

## Center, at 32 — the leak, and why it is welcome

At derivation step 5, before the slide shows it:

**ASK:** *we have been treating leak as a nuisance all term. Here it does
something useful — what?* Let them look at the gain curve on the screen. Without
$y_{\min}$ the gain would stay above 1 forever and there would be no upper
threshold, no defined HIGH, and nothing to match against.

Write underneath:

$$|G| = g\cdot\frac{y-y_{\min}}{y}
\qquad\Longrightarrow\qquad |G| = 1 \text{ has two roots}$$

**CHECK:** at $n \le 1$, $g < 1$ everywhere, so there are no roots at all.
Point at the left wing: that is the toggle's condition from session 9, and the
ring's from session 11, doing a third job.

**And the half that is easy to miss:** $n > 1$ is necessary, not sufficient.
The peak has to clear 1, and a large enough leak stops it. At $n = 2$ a
hundredfold swing gives a peak of 1.64, a tenfold swing 1.04, and a fivefold
swing 0.76 — no switch at all. Two of Cello's twenty gates are in that class,
which is the surface at 44.

<div class="rule"></div>

## Center, at 38 — the matching test

Four numbers and two inequalities. Write them as a box and leave them up for the
rest of the session:

$$x_{IL},\; x_{IH} \quad\text{(what a gate reads)} \qquad
y_{OL},\; y_{OH} \quad\text{(what a gate emits)}$$

$$\mathrm{NM_L} = \log\frac{x_{IL}(B)}{y_{OL}(A)} > 0, \qquad
\mathrm{NM_H} = \log\frac{y_{OH}(A)}{x_{IH}(B)} > 0$$

**POINT** at which letter is A and which is B each time. Getting the sender and
the receiver the wrong way round is the commonest error, and it gives a
plausible wrong answer rather than an obvious one.

**ASK before the RBS slide:** *name a change that moves what a gate emits and
not what it reads.* Fish for the RBS. Then write the reason, because it is one
line and it is the whole argument:

$$y \to f\,y \;\Longrightarrow\; \frac{y-y_{\min}}{y} \text{ unchanged}
\;\Longrightarrow\; G \text{ unchanged} \;\Longrightarrow\; x_{IL},\,x_{IH}
\text{ unchanged}$$

**Then the caveat, in one line, because the slide carries it:** that holds when
the output has its own RBS. In a repressor chain the output protein *is* the
next gate's repressor, so one RBS sets both, which is why Nielsen's thresholds
moved when they changed it.

<div class="rule"></div>

## Center, at 56 — the two bills, and the sentence

Clear a space and write these two lines under each other. They are the point of
the session:

$$\text{matching window} \;\uparrow\; \text{with } n
\qquad\qquad \text{log-linear range} = 9^{1/n} \;\downarrow\; \text{with } n$$

**Say it, slowly:** the same cooperativity that makes a gate easy to wire to
other gates is what makes it useless as a measuring instrument. Digital is not
free and it is not a property of the biology. It is a regime you pay to operate
in.

**IF ASKED** where $9^{1/n}$ comes from: on a log axis the slope of
$u^n/(1+u^n)$ is $n\,y(1-y)$, largest at $y = 1/2$; staying within 75% of that
peak keeps $y$ between $1/4$ and $3/4$, and the input ratio between those two
points is $9^{1/n}$. It is on the answer sheet.

<div class="rule"></div>

## What to cut if you are late

In this order, last first:

1. The second Nielsen surface (the numbers). Keep the figure and say which side
   fails without the arithmetic.
2. The synchrony row on the delay slide.
3. Handout item 4 — but then say the $9^{1/n}$ sentence out loud, because it is
   the session's thesis and item 4 is where it otherwise lands.

**Never cut** the matching test (PS6 assesses it), the leak step (it is what
makes a threshold exist), or the two bills at 56.
