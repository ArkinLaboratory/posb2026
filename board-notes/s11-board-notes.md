<!--
title: Session 11 — Board notes
subtitle: The criterion is derived on the split surface; the board carries the ring, the roots of unity, and the two numbers that survive.
session: 11
-->

# Board notes

Print this and carry it. The deck records what is *projected*; this records what
gets *written*.

**This is a light board session with one heavy moment** — the cube roots of
unity at step 3. That is the step where something disappears, and it is the one
worth drawing rather than projecting.

**Conventions.** **ASK** — put it to the room before writing, and the answer to
expect. **POINT** — the moments you turn and point at the board rather than the
screen. **IF ASKED** — the question that always comes.

<div class="rule"></div>

## Before class — left wing, the ring

Draw it. Three circles, three blunt-ended arrows, going round:

**x₁ ⊣ x₂ ⊣ x₃ ⊣ x₁**

and underneath, the model in one line:

$$\frac{dx_i}{dt} = \frac{\alpha}{1+x_{i-1}^{\,n}} - x_i$$

Leave the whole centre board empty. It fills at 27.

<div class="rule"></div>

## Right wing — minutes 13–23, the group answers

Three columns. Column 1 is the chase-round-the-loop argument and every group
will get it; write it as a chain, not a sentence:

**LacI high → TetR low → cI high → LacI low**  ✗

**ASK at 23, before sorting:** *what did you have to assume to write that
chain?* That "high" and "low" are the only options — which is the assumption the
next ten minutes removes. The genes do not have to be high or low; they can sit
in the middle. Getting that admission from the room is what makes the symmetric
fixed point feel necessary rather than arbitrary.

Column 3 is the one that matters and the one groups stall on. If nobody reaches
it, the sorted surface states it; do not pre-empt.

<div class="rule"></div>

## Centre, at 27 — the derivation's one board moment

The run is on the split surface, but **step 3 is drawn here**, because three
points on a circle is a picture and the slide has it as symbols.

**Draw the unit circle. Mark the three cube roots of unity:**

$$\omega_0 = 1, \qquad \omega_1 = -\tfrac12 + i\tfrac{\sqrt3}{2},
\qquad \omega_2 = -\tfrac12 - i\tfrac{\sqrt3}{2}$$

one at 0°, two at ±120°. **POINT** at the two off-axis ones and say: these are
the ones with negative real part, and that minus sign is where the instability
comes from.

**Then write, underneath:**

$$\lambda_k = -1 - g\,\omega_k \qquad\Longrightarrow\qquad
\operatorname{Re}\lambda_{1,2} = -1 + \frac{g}{2}$$

**ASK before you write the right-hand side:** *what is the real part of
$-1 - g(-\tfrac12 + i\tfrac{\sqrt3}{2})$?* Let the room do the sign. It is the
only algebra in the session that everyone can do in their head, and it is the
punchline.

**CHECK out loud:** the real root $\lambda_0 = -1-g$ is always negative. So the
ring never goes unstable "straight" — it can only go unstable by spiralling.
That is why you get a clock and not a switch, and it is worth saying in exactly
those words.

<div class="rule"></div>

## The two numbers that survive the session

$$\boxed{\; g = \frac{n x^{n}}{1+x^{n}} = 2 \;}
\qquad\qquad
\boxed{\; \alpha_c = \left(\frac{2}{n-2}\right)^{1/n}\frac{n}{n-2} \;}$$

Write both. Then, beside them, the two checks:

$$n \le 2: \;\alpha_c = \infty \qquad\qquad n = 4: \;\alpha_c = 2 \text{ exactly}$$

**IF ASKED — "why n > 2, when the toggle only needed n > 1?"** Say it plainly:
adding a gene to the loop made the requirement **harder**, not easier. Each
stage of the ring dilutes the gain, so you need more cooperativity per stage to
get round it. This is the second time this term the parameter that decides
whether the circuit works at all is the one you buy by choosing a protein.

<div class="rule"></div>

## At 40 — the period, three lines

$$g = 2 \;\Rightarrow\; \lambda = 0 \pm i\sqrt3
\;\Rightarrow\; T = \frac{2\pi}{\sqrt3} \approx 3.63 \text{ lifetimes}$$

**CHECK:** ours measures 3.64 just above the boundary. Say the agreement out
loud — it is the only place in the session where the linear theory is tested
against the simulation on a number it did not fit.

**IF ASKED — "does that give Elowitz's 150 minutes?"** Order of magnitude only,
and say so. Their effective lifetimes are tens of minutes, so a few lifetimes
lands in the hundreds of minutes. We threw away mRNA and delay; a three-variable
model does not earn a fit, and claiming one would be the kind of thing this
course is trying to teach them not to do.

<div class="rule"></div>

## Closing — the one line to leave up

$$\text{enough gain} \;+\; \text{enough delay} \;=\; \text{a clock}$$

That is T30 in one line and it is what Tuesday's noise session argues against —
our model has both and still cannot tell you whether the clock keeps time.
