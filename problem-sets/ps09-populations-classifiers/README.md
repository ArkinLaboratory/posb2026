# PS9 — Evolutionary Failure, Communities, Populations and Classifiers

[← all problem sets](../README.md) · **Out Nov 19 · Due Dec 3** · 50 points (BioE 247: 58)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps09-populations-classifiers/ps09.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps09-populations-classifiers/ps09.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

One question, asked four times at four scales: **what does this design do to a
population you are not watching?**

Questions 1–3 are one strain losing a kill switch, and containment turns out
not to be a number — it is a duration. Questions 4–6 are cells signalling to
each other, where the receiver is a density meter and the *geometry* decides
what the circuit can possibly know. Questions 7–8 are a parasite engineered so
that it spreads, where $R_0 > 1$ is the design target rather than the failure.
Questions 9–10 are a classifier deciding which cells to kill, and the deciding
turns out to be one comparison made outside the circuit entirely.

| | |
|---|---|
| **Q1** | A kill switch on a plasmid, lost to mutation and selection. Its half-life, then the two redesigns the hour priced — halve the burden, or harden the DNA — and which one buys more **on this construct**. The ranking is not the one the lecture ledger shows, and the reason is one ratio. |
| **Q2** | Nobody hands you a fitness cost. Two measurements of the same strain, made the same week by the same person, disagree by a lot. Estimate both, then say which you would report and what the other would need before it could be believed. |
| **Q3** | Containment. The requirement from a dose, the escapers at the best fraction viable in the literature, and then the number that reframes the whole thing: how many **generations** the claim survives. |
| **Q4** | A sender/receiver link is two equations. Read a cell density off a receiver's output, in a dish and in a chemostat where dilution competes against the molecule's own decay. Then add a lactonase and say what a colleague measuring only the steady state can and cannot tell. |
| **Q5** | Basu's band detector, with one operator weakened. Find the window's two edges and its width as a ratio — the response is not monotone, so locate the peak before you root-find. |
| **Q6** | Two estimates from two different sessions that answer **different questions**: how far a signal gets before it decays, and how long it takes to get there. Then retune the one knob you actually have, and say what the square root costs a designer who wants twice the reach. |
| **Q7** | Retroviruses are diploid, so a capsid takes two strands and a vector prep has three kinds of particle in it. What fraction can infect anything at all — and then the number your titer assay actually reports, which is not the same number. |
| **Q8** | A therapeutic parasite in a patient. Its $R_0$, its floor, and then what happens to the floor when a collaborator remeasures the burst size — computed **twice**, holding different things fixed. The two answers straddle the original, and only one of them is a coherent perturbation of this model. |
| **Q9** | Design the cut. Five sensor modules, seven cell lines, one positive — and the deciding is one comparison you make, not something the circuit does. Walk a pinned grid of cuts, then do the clinical arithmetic, where two of the three numbers are **yours**. |
| **Q10** | *Written.* What a seven-line panel cannot establish. A search says this design meets its budget with zero wrongly acted-on cells; say why that number may not be reported. |
| **Q11** | *Required for BioE 247, extra credit for BioE 147* — Q3 and Q9 were the same arithmetic with the sign reversed. See it, then apply Q9's discipline back to Q3, where you let a measured rate stand as a number. |

### This set posts before two of its four sessions have happened

Deliberate — you get the whole thing early — but start at the top and do not
worry about the bottom:

| questions | you can start | after |
|---|---|---|
| **1–3** | immediately | session 23 (Nov 12) |
| **4–6** | immediately | session 24 (Nov 17) |
| **7–8** | after Nov 19 | session 25 |
| **9–11** | after Nov 24 | session 26 |

Nine days remain after session 26. If you work Q1–Q6 in the first week the
rest is comfortable; if you wait, it is not.

### Before you start

**Report numeric answers to at least four significant figures.** Every graded
value is checked to a relative tolerance of $10^{-3}$, so four figures leaves a
full order of magnitude of slack — but rounding to two or three will fail.

**Several questions check that your answers agree with each other**, not just
with ours. Q1's half-life has to run forward through the model and give one
half. Q6's lit edge has to invert your own penetration depth. Q8's floor has to
be a root of your own patient's threshold. A number you remembered or borrowed
cannot satisfy these, which is the point of them.

**Units are load-bearing in three places.** Q5 mixes µM and nM and asks for
each in a stated one. Q6 wants millimetres and minutes. Q8's table is per
microlitre throughout **except one row printed per millilitre**, and that
conversion is worth a factor of a thousand.

**Q4d, Q10 and Q11 are written, not computed.** No credit is available for
repeating arithmetic you have already done. A wrong number for a stated and
sensible reason scores better than a right number with no reasoning.

**Q9 hands you two of its three clinical numbers to choose yourself**, and one
of them may not be zero. Six negative cell lines cannot resolve a rate finer
than one in six, so a false-positive count of zero means *below this panel's
resolution* — never *zero*. Q10 is where that argument is marked.

### What the visible tests do

They check shape, sign, ordering and self-consistency — not your exact numbers.
**The values are checked by hidden tests**, so a green visible check means "not
obviously broken", not "right". Some visible checks carry no points at all;
they are there to tell you something is wrong early, and a set of invented
numbers can sometimes satisfy them.

Several questions have a check you can do by hand first. Q3's requirement is
one survivor per dose. Q7's three particle classes are a binomial and must sum
to one. Q9's specificity at each cut is one minus a count over six. Work those
on paper before you trust the code; if the code disagrees with the paper, the
error is usually upstream of the test.

### Solutions

Distributed through bCourses after the deadline, as always. Not in this
repository.
