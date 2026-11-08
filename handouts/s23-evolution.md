<!--
title: Session 23 — Evolutionary failure and containment
subtitle: A home guide, worked after class. Item 1 is why you cannot count cassettes from a stability curve; item 2 is the difference between a bound and a measurement, on their data; item 3 is their evidence and which strain earned which claim; item 4 is the mutational target and what the model has no term for. Answers come on a separate sheet.
session: 23
-->

# How to use this

Work it after class, on paper. The answers are on a separate sheet — read
them **after** you have written something down, not instead of writing
something down.

Nothing here asks you to compute a failure time or a retention time. Those
are the two things the session derived and they are the two things you will
be graded on; this guide works the territory around them, which is where
the mistakes actually get made. None of it needs a computer. All of it needs
the Rottinghaus paper open — items 2, 3 and 4 send you to their figures and
their discussion by name.

**The symbols, once.** $q$ is the fraction of the population whose kill switch
no longer works. $s$ is the per-generation growth advantage a cell gets from
losing the switch, so $s = 0.02$ means two per cent faster per generation.
$\mu$ is the per-cell per-generation probability that a working switch breaks,
lumped over every way it can break. $\mu_1$ is that probability for **one
cassette**, so with $k$ identical cassettes $\mu$ is built out of $\mu_1$ —
they are different numbers and the difference is item 1. A dot means
$d/dt$, and $t$ is in **generations** throughout, never hours.

One warning about $q$, because item 1 uses the letter twice. In the redundancy
argument below, $P_{\text{side}}(t)$ is the probability that one whole side of
the construct has broken; $q$ is the fraction of the **population** that has
escaped. They are related but they are not the same quantity, and the
distinction is what item 1(b) turns on.

---

## 1. You cannot count cassettes from a stability curve

Killing needs two things at once — a Cas9 to cut and a gRNA to say where — so
the construct has two *sides*, and escape needs one whole side gone. Within a
side the copies are redundant. With $k$ copies on a side, each mutating
independently at rate $\mu_1$ and still intact with probability
$e^{-\mu_1 t}$, that whole side is gone with probability

$$P_{\text{side}}(t) = \left(1 - e^{-\mu_1 t}\right)^k \;\approx\;
(\mu_1 t)^k \qquad \text{for } \mu_1 t \ll 1$$

Escape needs **either** side gone, so the two add:

$$q \;\approx\; (\mu_1 t)^{k_{cas9}} + (\mu_1 t)^{k_{gRNA}}$$

and for small $\mu_1 t$ the **smaller** exponent dominates. The real construct
is four *cas9* cassettes and three gRNA cassettes, so the early behavior is
$(\mu_1 t)^4 + (\mu_1 t)^3 \approx (\mu_1 t)^3$ — the structure predicts a
slope of **three**, not four and not seven. Notice what that means for the
fourth *cas9* cassette: once one side needs fewer hits than the other, extra
redundancy on the longer side changes the early escape rate by essentially
nothing.

So on log–log axes the early slope is the smaller $k$. That is a real result
and it is tempting to run it backwards: measure the slope of a stability
curve, read off the architecture.

Class showed that this does not work. Here is the table it rests on — one
cassette, so $\mu = \mu_1 = 10^{-6}$. **Decade slope** is the straight line
through the two endpoints $t = 10$ and $t = 100$ — a secant, not a
least-squares fit, and those differ enough to matter, which is itself the
item. **Local slope** is the same construction over the narrow window
$t = 95$ to $105$:

| burden on ONE cassette | slope over a decade | slope measured locally at $t = 100$ |
|---|---|---|
| $s = 0$ | 1.00 | 1.00 |
| $s = 0.02$ | 1.46 | 2.31 |
| $s = 0.05$ | 2.36 | 5.02 |
| $s = 0.08$ | 3.37 | 7.70 |

**(a)** A colleague measures a log–log slope of 3.0 and tells you the circuit
has three redundant cassettes. Give the competing explanation, with a number
from the table.

**(b)** Both columns are the same circuit. Why do they disagree, and what does
that tell you about quoting a log–log slope without saying anything else?

**(c)** The authors did build four $P_{tet}$-*cas9* cassettes and three gRNA
cassettes. Does the slope argument recover that? Say what it would take to
measure $k$ directly — not from a stability curve.

**(d)** One sentence: a negative result like this one is more useful than the
inference it replaced. Why?

---

## 2. A bound is not a measurement

Their Fig. 2e is 28 days of passage without antibiotics, nine timepoints,
the CRISPRks strain. What they plot is *fraction viable* — colonies with the
inducer over colonies without it — so a working cell dies on induction and a
broken one survives, and fraction viable $\approx q$. That is an
approximation, not an identity: killing is imperfect even for working cells,
and several of the floors in this paper are detection limits rather than
zeros. It is what lets the model be drawn on their axes at all.

Fitting $\dot q = (1-q)(sq + \mu)$ to the eight detectable points, by least
squares on $\log_{10}$:

| model | best $\mu$ | RMS (decades) |
|---|---|---|
| $s = 0$ | $2.63 \times 10^{-9}$ | **0.151** |
| $s = 0.005$ | $1.86 \times 10^{-9}$ | 0.203 |
| $s = 0.01$ | $1.31 \times 10^{-9}$ | 0.278 |
| $s = 0.02$ | $5.62 \times 10^{-10}$ | 0.473 |
| $s = 0.05$ | $2.83 \times 10^{-11}$ | 1.215 |
| a flat line — the null, *not* a member of the family | — | **0.204** |

**RMS (decades)** is the root-mean-square residual measured in powers of ten:
0.151 means the model typically misses each point by about 0.15 of a decade, a
factor of 1.4. Treat a model as **excluded** when its RMS is roughly three
times the best — with eight points and one free parameter that is about a
one-in-three-hundred coincidence. A 25 % gap is about one in four, which is
nothing. Read the $s = 0.005$ row against the flat row before you conclude
anything.

The data's own log–log slope is **0.63** over those eight points, and every
model in this family predicts at least 1. Why at least 1: at small $q$ the
equation reduces to $\dot q \approx \mu + sq$, so $q \approx \mu t$ when
$s = 0$ — a log–log slope of exactly 1 — and any positive $s$ bends it upward
from there. A measured slope below 1 is outside the family altogether, not a
member of it with an unlucky parameter.

(The day-1 point sits at the detection limit, so it is an upper bound and not
a measurement; include it anyway and the left end of the fit is dragged down
and the nine points return 1.08. That is **not** item 1(b) — that was a curved
function sampled over different windows. This is a censored point treated as
data, which is this item's own lesson committed on the way in.)

**(a)** The best fit is $s = 0$. Write the sentence you would actually put in
a paper, and say why "we measured the fitness cost to be zero" is not it.

**(b)** Compare the top row with the bottom row. What does that comparison
cost you, and what does it leave intact?

**(c)** The hour's reference point for the ledger was $s = 0.05$. What does
this table say about that choice? Does it invalidate the ledger?

**(d)** The fitted $\mu$ is about $3 \times 10^{-9}$ per cell per generation.
Give one reason this number is not a mutation rate, using something from
their discussion.

---

## 3. Which strain earned which claim

Six results from the paper, all real, all about kill switches in the same
organism — *E. coli* Nissle 1917:

| | number | where |
|---|---|---|
| i | fraction viable below $10^{-8.6}$ | Fig. 1h |
| ii | rises to about $10^{-6.35}$ by day 28 | Fig. 2e |
| iii | fraction viable $10^{-3.3}$ at 24 h, monoculture | Fig. 3a |
| iv | improving to $10^{-4.2}$ at 24 h with a 1:1 competitor | Fig. 3a |
| v | population eliminated by 72 h | Fig. 3a |
| vi | still eliminated at competitor ratios down to 1:1000 | Supplementary Fig. 4c |

Strains, since the paper's names are not self-explanatory. **CRISPRks** is
four genomic P*tet*-*cas9* cassettes plus three optimized P*tet*-gRNA
cassettes on one plasmid with *tetR* and *infA*. **CRISPRks Δrpdu** is that
same strain with *recA*, *polB*, *dinB* and *umuDC* deleted. **aTc** is
anhydrotetracycline, the inducer; **P*tet*** is the TetR-repressed promoter it
acts through.

**(a)** Two of these are the optimized 2-gRNA switch with antibiotics at a
single timepoint, and the plain CRISPRks strain over 28 days without them.
Which is which, and what goes wrong if you use the first as the 28-day bound?

**(b)** Result (v) is not the same strain as (iii) and (iv). Which strain is
it, and what else had to be true besides the competition? Say what you would
be claiming if you credited (v) to competition alone.

**(c)** Result (iii) is a gut-emulating assay — minimal medium, low oxygen, no
shaking. The same strain does far better in a flask. Their discussion gives a
**two-step** reason, and both steps are needed. What are they? (If your answer
has the environment switching a mechanism on, check the direction again.)

**(d)** You are refereeing a paper that cites this one for "CRISPR kill
switches achieve $10^{-8.6}$ containment." Write the one-sentence referee
comment. Two things are wrong with that sentence, not one.

---

## 4. The mutational target

Class ended on the claim that $\mu$ was never a constant of nature — it is a
property of what you made escape require.

**(a)** $P_{tet}$ contains two identical 19 bp *tet* operator sites, and over
half of all observed mutations are a 25 bp deletion removing one of them
**and most of the −35 site**. Explain why redundancy and repeat are the same
thing here, name the mechanism, and say why the deletion kills the promoter
rather than merely shortening it.

**(b)** Mandell et al. (2015) built strains whose essential enzymes require a
non-natural amino acid, and saw no escape over 14 days down to a detection
limit of $2.2 \times 10^{-12}$. Contrast the mutational target with a CRISPR
kill switch's, in one sentence each.

**(c)** The gRNA cassettes, *tetR* and a constitutive *infA* cassette sit
together on one plasmid in this design; *cas9* is exclusively genomic, and the
chromosomal *infA* was knocked out, so a cell that drops the plasmid cannot
make protein. Write down the term that $\dot q = (1-q)(sq + \mu)$ would need
in order to describe what plasmid-borne DNA makes possible. Then do the
algebra: say which part of it $s$ and $\mu$ absorb after all, which part the
*infA* trick removes from the real strain, and which part no choice of $s$ and
$\mu$ can represent.

**(d)** Rank these four levers from *least* a matter of circuit design to
*most*: lower $s$; lower $\mu_1$; raise $k$; change the selection environment.
Then say which lever or levers the authors actually used to get elimination —
and for the one you ranked most a matter of circuit design, say what item 2
has already told you about how much travel it has left on this construct.
