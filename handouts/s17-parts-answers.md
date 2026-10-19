<!--
title: Session 17 — Answers
subtitle: What a part is, and what it costs to make one. Every number here is recomputed from the papers' own data.
session: 17
-->

# Session 17 — answers

---

## 1 · Move a promoter

**(a)** Four plausible ones, classified. Any sensible four is fine; the
classification is what is being marked.

| | class |
|---|---|
| high-copy plasmid → chromosome (copy number falls) | **host** |
| different gene downstream, so a different 5′UTR at the junction | **compositional** (physical) |
| DH5α → a production strain | **host** |
| LB → minimal medium, so a different growth rate | **environmental**, acting through the host |

**(b)** The **different gene downstream** is different in kind. The other
three shift a number that belongs to the promoter. This one means there was
never a number belonging to the promoter alone: the junction encodes part of
the transcript's 5′UTR, the 5′UTR sets stability, so the quantity you called
"promoter strength" was always a property of the *pair*.

**(c)**

| | |
|---|---|
| copy number | **model it.** It is close to a multiplier and you already have the machinery — this is the one context effect that behaves. |
| strain | **hold it fixed and report it.** There is no model; a LacI-family circuit in the literature worked in two of seven *E. coli* strains. |
| medium / growth rate | **hold it fixed and report it.** Growth-rate coupling is systematic but not parameterisable from anything you can measure about the part. |

Holding fixed and reporting *is* what a characterisation context is. Saying
"we measured in DH5α, LB, 37 °C" is not an apology; it is the only thing that
makes the number mean anything.

---

## 2 · How much of the answer do the parts own?

**(a)** The RBS sets the rate of translation initiation, which does not change
how much RNA is made — hence only 4% of RNA variance. But protein is
(RNA level) × (translation rate), so the RBS enters the protein number
directly. Credit also for noting that ribosome loading *protects* a transcript,
which is the mechanism behind (b).

**(b)** This is the third failure — **joining changes both**. A translational
element reaching back to alter transcript abundance means the output cannot be
factored into "what the promoter did" times "what the RBS did", because the
promoter's own contribution now depends on which RBS is downstream.

Ill-posed rather than inaccurate: an inaccurate model has a true value it
misses. Here there is no $p$ to estimate — the quantity is not a function of
the promoter alone, so no amount of extra measurement converges on it.

**(c)** With independence, $0.64^{10} = 0.0115$ — about **1.2%**, or one build
in 87. (For comparison, at the manufactured 93%: $0.93^{10} = 0.48$, about
half.)

Independence is **not** safe, and students should say which way it cuts.
Arguments either way earn full credit if they are mechanistically grounded:

- *Optimistic:* the deviations share causes — host load, growth rate, the same
  strain and medium — so failures cluster, and a build that goes wrong tends
  to go wrong in several genes at once. Clustering makes the all-pass
  probability **higher** than 1.2%, so the independent estimate is
  pessimistic about *this* quantity.
- *Pessimistic:* the 13-fold tail is what actually kills a build, and one gene
  13-fold off is fatal regardless of the other nine. A whole-build success
  criterion that only asks "all within twofold" understates the damage.

The point to land: **the tail, not the bulk, is the design constraint.**

---

## 3 · Where prediction works

**(a)** The pooled $r = 0.62$ averages a near-exact model over one class with a
failing model over three others. The split says the model is not weak — it is
**narrow**. That is actionable in a way "weak" is not: you can check whether
your terminator is in the good class before trusting the prediction.

**(b)** Because the paper identifies the failure classes *as classes*, not as
scatter. A model that is wrong unpredictably is unusable. A model that is
wrong on three named, recognisable categories comes with its own domain of
validity attached — which is most of what you want from a model.

**(c)** Any of these, or equivalent:

- *"…when the class is drawn tightly enough that the features the model uses are the features that vary."*
- *"…when you have imposed a definition, not discovered one."*
- *"…when you can tell in advance whether the part is the kind of thing the model is about."*

The sentence to reject: *"…when the part is simple."* Terminators are not
simpler than promoters; they have been **defined** more tightly.

---

## 4 · Overhangs

**(a)** A four-base overhang is palindromic when it equals its own reverse
complement — so base 1 pairs with base 4 and base 2 with base 3. Choose bases
1 and 2 freely and the other two are forced: $4 \times 4 = \mathbf{16}$.

**(b)** $256 - 16 = 240$ non-palindromic overhangs, and each is paired with its
distinct reverse complement, so they form $240 / 2 = \mathbf{120}$ junction
identities.

**(c)** Because the constraint is not *how many* overhangs exist but *how
different any two of them are allowed to be*. Two junctions one base apart
misligate, so each overhang you pick removes a neighbourhood around itself
from the pool, not just itself. That is a birthday-problem shape: collisions
arrive far sooner than the raw count suggests — at random, even odds by about
five parts. Which is exactly why published assembly standards ship a **fixed,
designed** overhang set with measured fidelity rather than telling you to
choose your own.

**(d)** The scar is not neutral. A junction chosen purely for cloning
convenience is four bases of sequence sitting in the transcript, near the
start codon if the junction is at the 5′ end of the coding sequence — and
secondary structure in exactly that window is 83% of what Cambray's design
properties explain. So **a decision made on the bench, for bench reasons,
lands inside the dominant determinant of translation.** The physical and
functional layers are not separable even here.

---

## Stretch

No model answer; the question is open and is a 247 project in miniature. A
strong paragraph will:

- identify **who pays and who benefits** — the measuring lab pays, the
  downstream user benefits, which is the classic public-goods shape and the
  honest reason adoption is hard;
- give a failure reason that is structural rather than about effort. Good
  ones: a quality statistic is only meaningful across a context *set* that
  somebody has to agree on; it devalues parts already in catalogues; it makes
  a lab's own parts look worse than an unmeasured competitor's; there is no
  journal or funder requiring it;
- avoid "people are lazy" and avoid "we need better tools", both of which
  explain nothing.

Credit for noticing that the manufacturing fix and the measurement standard
came from the same group in the same year, and that **only one of them was
adopted** — the one that made individual builds work, not the one that would
have made the field's numbers comparable.
