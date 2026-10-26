<!--
title: Session 19 — Your circuit is not alone in there
subtitle: Four to work. Everything on this sheet is about one thing: two genes with no wire between them still change each other.
session: 19
-->

# Your circuit is not alone in there

**Thursday's problem had a cure.** A part has no boundary until you
manufacture one — so manufacture it. Fix the junction, insulate, standardise,
and the abstraction becomes true because you made it true.

**Today's does not.** Two genes with no regulatory connection change each
other's output because they draw on the same ribosomes. You can fix a 5′UTR.
**You cannot give your circuit its own ribosome pool.**

**The one result the hour turns on.** With $d_i = m_i/K_i$ the *demand* of
gene $i$ — how hard it pulls on the pool, message abundance and binding
strength in one number —

$$p_i \;\propto\; \frac{d_i}{1 + \sum_j d_j}$$

One weight on top, a sum over everything competing underneath. **You derived
this shape on 15 September** for an operator that two factors compete for.
The sum ran over configurations of one piece of DNA; here it runs over the
genes of a cell.

---

## 1 · The edge that is not in the diagram

Gene 1 runs at demand $d_1 = 1$. You induce gene 2.

**(a)** By what factor does gene 1's output fall when $d_2 = 4$? Do it in two
lines.

$$\rule{11cm}{0.4pt}$$

**(b)** Write $p_1$ at demand $d_2$, divided by $p_1$ at $d_2 = 0$, and
simplify until no $p$ appears.

$$\rule{11cm}{0.4pt}$$

**(c)** That expression is a Hill function in $d_2$. What is its Hill
coefficient, and what is its half-point $K_{\text{app}}$?

$$\rule{11cm}{0.4pt}$$

**(d)** So the fall is *exactly* the shape of repression by a non-cooperative
repressor, and nothing is repressing anything. Given (c), design a measurement
that distinguishes the two **without cloning anything**. One sentence, and say
what you would vary.

$$\rule{11cm}{0.4pt}$$

<div class="rule"></div>

## 2 · The budget

**(a)** Normalise each gene's output by what it would reach **alone at
unlimited demand**. Show that

$$p_1 + p_2 = \frac{\sum d}{1 + \sum d}$$

and say in one line why no $d_1$ or $d_2$ appears separately.

$$\rule{11cm}{0.4pt}$$

**(b)** You have a fixed total demand and you are free to split it between
two genes however you like. What shape is the set of achievable $(p_1, p_2)$?

$$\rule{11cm}{0.4pt}$$

**(c)** The sum approaches 1 and never reaches it. Say what a designer is
buying, and what they are paying, as they push the total demand up.

$$\rule{11cm}{0.4pt}$$

**(d)** Gyorgy *et al.* measured this and found something the one-pool model
does **not** predict: induce a gene on a plasmid and a reporter on the *same
plasmid* drops by up to 60%, while a reporter in the *chromosome* does not
move. They also built a strain to show a chromosomal drop would have been
visible. Why does that control matter, and what does the result say about
where the pool ends?

$$\rule{11cm}{0.4pt}$$

<div class="rule"></div>

## 3 · The price, in growth

Scott *et al.* model a protein the cell has no use for as a neutral component
and predict

$$\frac{\lambda}{\lambda_0} = 1 - \frac{\varphi_U}{\varphi_c}, \qquad \varphi_c \approx 0.48$$

where $\varphi_U$ is the fraction of total protein given over to it.

**(a)** You express a useless protein at 10% of total protein. Estimate the
growth-rate cost.

$$\rule{11cm}{0.4pt}$$

**(b)** Growth extrapolates to zero at $\varphi_U = 0.48$, not at 1.0. What is
the other 52% doing, and why is that a ceiling rather than an accounting
error?

$$\rule{11cm}{0.4pt}$$

**(c)** The model charges you for **proteome fraction and nothing else** — not
amino acids, not ATP per peptide bond, not chaperone capacity. Their Fig. 4C
puts three different proteins, from four expression systems, on the same
relation. Why is that the evidence that licenses the simplification?

$$\rule{11cm}{0.4pt}$$

<div class="rule"></div>

## 4 · The thing you already own, which was wrong

Session 5 gave you the response time of a protein:

$$t_{1/2} = \frac{\ln 2}{\gamma + \mu}$$

and PS2 used it with $\mu$ taken as a number the medium hands you.

**(a)** Your circuit switches on and diverts ribosomes. Which way does $\mu$
move, and which way does $t_{1/2}$ move?

$$\rule{11cm}{0.4pt}$$

**(b)** **Which proteins** does that affect?

$$\rule{11cm}{0.4pt}$$

**(c)** Nothing about the DNA changed. In two sentences: what does this do to
the idea that a part has a response time you can look up?

$$\rule{11cm}{0.4pt}$$

**(d)** The direction here is unambiguous and the magnitude is not. Say what
you would have to measure, in your own strain, before you could put a number
on it.

$$\rule{11cm}{0.4pt}$$

<div class="rule"></div>

## The ledger — fill this in before the last ten minutes

You cannot insulate. So what *can* you do?

| move | what it costs you |
|---|---|
| lower the demand | |
| spend it better | |
| close a loop on burden itself | |
| characterise in place | |
| **what you cannot do** | |

<div class="rule"></div>

## Before Tuesday

Fong & Palsson, *Nat Genet* 2004 — three pages in which a model predicts a
growth rate, somebody builds the strain, evolves it, and checks. Read
Supplementary Table 1 and the predicted-against-observed comparison: 39 of 50
right.

Come with a guess about what the eleven failures have in common.

**PS7 goes out at the end of this session** and is due 5 November. It covers
sessions 17, 18 and 19.
