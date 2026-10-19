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
| strain | **hold it fixed and report it.** There is no model. Cardinale & Arkin report a circuit whose regulators were already orthogonal, imported from *Pseudomonas syringae*, failing in five of seven *E. coli* strains while its inputs were engineered *E. coli* promoters; swapping in the exogenous Plux restored function. |
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
in 87. (At the manufactured 93% of the stretch question: $0.93^{10} = 0.48$,
about half. Note these are different metrics — item 2 is prediction accuracy,
the stretch is hitting a target — so the contrast is illustrative, not a
like-for-like comparison.)

Independence is **not** safe, and students should say which way it cuts.
Arguments either way earn full credit if they are mechanistically grounded:

- **The estimate is too pessimistic.** The deviations share causes — host
  load, growth rate, the same strain and medium — so failures cluster. A build
  that goes wrong tends to go wrong in several genes at once, which makes the
  all-pass probability **higher** than the independent 1.2%.
- **The estimate is too optimistic.** Deviations could instead be driven by
  each gene's own junction and local sequence, which are independent by
  construction across a designed pathway; and more importantly, "all within
  twofold" is the wrong success criterion — one gene 13-fold off kills the
  build regardless of the other nine, so even a passing build can fail.

Either direction earns full credit **if the mechanism is named**. A bare
"optimistic" or "pessimistic" does not.

The point to land: **the tail, not the bulk, is the design constraint.**

---

## 3 · Where prediction works

**(a)** Both of these, and the second is the one that separates a careful
student:

1. **The pooled number averages classes.** It mixes a model that works on the
   curated set with one that fails on three named others. The model is not
   weak, it is **narrow** — and narrow is actionable, because you can check
   which class your terminator is in before trusting it.
2. **The 31 are the training set.** The paper fitted four features, selected
   stepwise from twelve, on exactly those 31, and reports r = 0.9 with
   cross-validated r = 0.85. The 23 others were held out. So part of the
   in-class/out-of-class gap is a train/test gap, and the honest number for
   the curated class is the cross-validated 0.85, not the raw fit.

A student who says "that's an in-sample fit on a feature-selected model" is
**right** and should get full marks.

**(b)** Because the errors carry information. A model whose residuals are
random noise tells you only "expect to be wrong by about this much". This
model's residuals have **signs that track recognisable categories**: low-
efficiency and low-folding terminators are overpredicted, extended ones
underpredicted — and the paper says why, since an extended terminator's real
performance comes partly from elements outside the window the model looks at.

So the model arrives with its own domain of validity, *and* a diagnosis for
each way it leaves it. That is most of what you want from a model. Credit for
noting that this is only possible because somebody classified the terminators
first — the classification is doing work the model cannot.

**(c)** Any of these, or equivalent:

- *"…the class is drawn tightly enough that the model's features are the ones that vary."* (14)
- *"…you have imposed a definition rather than discovered one."* (9)
- *"…you can tell in advance which class the part is in."* (11)

These are not equivalent to each other — they name feature-variance, imposed
definition, and ex-ante classifiability. **Accept any one of the three, or any
answer that clearly lands on one of them.** Reject "…when the part is simple":
terminators are not simpler than promoters, they have been defined more
tightly.

The sentence to reject: *"…when the part is simple."* Terminators are not
simpler than promoters; they have been **defined** more tightly.

---

## 4 · Overhangs

**(a)** A four-base overhang is palindromic when it equals its own reverse
complement — so base 1 is the complement of base 4, and base 2 of base 3.
Choose bases 1 and 2 freely and the other two are forced:
$4 \times 4 = \mathbf{16}$.

Full marks also for a student who says the real failure is **loss of
directionality** — a palindromic overhang anneals to a copy of itself, so the
fragment inserts either way round, and fragments self-dimerise. That is a
better answer than "it ligates to itself".

**(b)** $256 - 16 = 240$ non-palindromic overhangs, and each is paired with its
distinct reverse complement, so they form $240 / 2 = \mathbf{120}$ junction
identities.

**(c)** Because the constraint is not *how many* overhangs exist but *how
different any two of them are allowed to be*. Two junctions one base apart
misligate, so each one you pick removes a neighbourhood around itself from the
pool, not just itself. That is a birthday-problem shape: collisions arrive far
sooner than the raw count suggests — at random, even odds at about **four
junctions**, which for a circular assembly with a backbone is a three-part
build. Which is exactly why published assembly standards ship a **fixed,
designed** overhang set with measured fidelity rather than telling you to
choose your own.

**(d)** The scar is not neutral: a junction chosen for cloning convenience is
four bases of sequence that may end up inside the transcript.

**Mark generously, and mark the caveats higher than the claim.** The strong
version — "the scar sits in the window that dominates translation" — is an
overreach, and a student who spots why deserves more credit than one who
asserts it:

- Cambray 2018 varied a designed window **inside the coding sequence**; the
  5′UTR and SD were held fixed. The 83% is 83% *of what the design properties
  explain*, and those properties explain 28% of that library's variance. It is
  not 83% of translation.
- In MoClo and the Common Syntax the CDS-side junction is **fixed at AATG**
  precisely because it must encode the start codon — so the one junction
  nearest the start is the one you do *not* choose.
- Most junctions are nowhere near a start codon, and a promoter:5′UTR junction
  can sit upstream of the transcription start and so be outside the transcript
  altogether.

The defensible claim, and the one to credit: **a four-base choice made for
assembly reasons is sequence that the functional model has to live with, and
nothing in the cloning workflow asks whether it should.**

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
