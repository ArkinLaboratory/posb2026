<!--
title: Session 13 — Four problems, answers
subtitle: Posted after class. Every number here is checked in tests/test_digital.py.
session: 13
-->

# Four problems — answers

Item 1 is worked in full on the handout.

## 2 — The same gate at $n = 3$

$$x_{IH} = \mathbf{5.80}, \qquad
y_{OH} = y(0.80) = \mathbf{6.65}, \qquad y_{OL} = y(5.80) = \mathbf{0.15}.$$

**The band narrowed, and that is good.** At $n = 2$ the uncertain region runs
from 1.02 to 9.80, a factor of 9.6. At $n = 3$ it runs from 0.80 to 5.80, a
factor of 7.3. The output levels also moved apart, 6.65 against 0.15 rather
than 4.95 against 0.20.

Both changes help the same thing: a sharper gate has a narrower band of inputs
it cannot classify, and it pushes its outputs further from that band. That is
why the next item is easier to solve for a sharper gate, and it is the first
half of the session's trade — the second half is item 4.

## 3 — Does this pair connect?

A's output levels are $y_{OL} = 0.20$ and $y_{OH} = 4.95$ (item 1). B's
thresholds are $x_{IL} = 0.80$ and $x_{IH} = 5.80$ (item 2).

$$\mathrm{NM_L} = \log_{10}\frac{0.80}{0.202} = \mathbf{+0.60}, \qquad
\mathrm{NM_H} = \log_{10}\frac{4.95}{5.80} = \mathbf{-0.07}.$$

**The high side fails, by 0.07 decades** — about 17%. A's best HIGH output is
4.95 and B does not read anything below 5.80 as HIGH. The pair is a hair short,
which is the common case in practice and the reason the test is worth doing with
numbers rather than by eye: nothing about these two curves looks wrong.

**The RBS window.** Scaling A's output by $f$ multiplies both of its levels by
$f$ and moves neither gate's thresholds:

$$\mathrm{NM_H} \ge 0 \iff f \ge \frac{5.80}{4.95} = 1.17, \qquad
\mathrm{NM_L} \ge 0 \iff f \le \frac{0.80}{0.202} = 3.96.$$

So any factor between **1.17 and 3.96** works — a 3.4-fold window — and the most
tolerant choice is its geometric middle, $f = 2.15$, which gives both margins
$+0.26$ decades.

Worth noticing against item 2: B is the *sharper* gate, and sharpening the
receiver is what made this pair nearly work. The identical-gate pair on the
slides, $n = 2$ driving $n = 2$, fails by 0.30 decades; replacing the receiver
with the $n = 3$ gate cuts that to 0.07 before any RBS is touched.

**Why the RBS does not move A's thresholds.** Multiplying $y_{\min}$ and
$y_{\max}$ by the same factor leaves $(y - y_{\min})/y$ unchanged at every $x$,
so $|G|$ is unchanged, so the two solutions of $|G| = 1$ are unchanged. The RBS
moves what a gate emits; the promoter's $K$ and $n$ set what it reads.

**One caveat, and it is about real gates rather than this model.** Here the
output is a reporter with its own ribosome binding site, separate from the
repressor's. In a repressor chain the output protein *is* the next gate's
repressor, so a single RBS sets both what the gate emits and the level at which
the next gate reads it. Nielsen et al.'s supplement (section I.C) report exactly
that: changing the RBS controlling repressor expression shifted the gate's
threshold, and in some cases eliminated the response. Two knobs here; often one
knob in the laboratory.

## 4 — A sensor that must read four decades

**Why one promoter cannot.** A Hill curve is a straight line on a log axis only
near its midpoint. The same slope that gave us gain gives us this: on a log axis
the slope of $u^n/(1+u^n)$ is $n\,y(1-y)$, largest at $y = 1/2$. Staying within
75% of that peak keeps $y$ between $1/4$ and $3/4$, and the input ratio between
those two points is

$$9^{1/n}: \quad 9\times \text{ at } n = 1,\quad
3\times \text{ at } n = 2,\quad 1.7\times \text{ at } n = 4.$$

Four decades is ten thousand-fold. Even the gentlest useful promoter, $n = 1$,
gives you not quite one decade. And the cooperativity that made item 2's gate a
better switch makes it a worse sensor — the same $n$, in both bills, with
opposite signs.

**What to change.** Both ends of the curve saturate, so remove both
saturations. Daniel et al. (*Nature* 2013) do exactly that: positive feedback
on the transcription factor, so that rising inducer makes more factor and never
saturates it, plus a high-copy plasmid of binding sites — a shunt — that soaks
up free factor so the DNA sites never saturate either. Their measured output
fits $\ln(1+x)$ over more than three decades (Fig. 1d), where the open-loop
control on the same axes is fitted by $x/(1+x)$ and spans a narrow range.

Other answers that earn full credit: several promoters of different $K$ reading
the same inducer, with their outputs combined (a segmented sensor, which is how
most instruments do it); or a slow integrator that converts concentration into
a time, trading range for speed. Any answer that names which saturation it
removes is doing the right kind of reasoning.
