# PS7 — Implementation Layers, Resources and Burden

[← all problem sets](../README.md) · **Out Oct 29 · Due Nov 5** · 48 points (BioE 247: 56)

[**Open in DataHub**](https://datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https://github.com/ArkinLaboratory/posb2026&branch=main&urlpath=lab/tree/posb2026/problem-sets/ps07-implementation/ps07.ipynb) ·
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ArkinLaboratory/posb2026/blob/main/problem-sets/ps07-implementation/ps07.ipynb)

Submit the `.ipynb` to Gradescope. One submission per student.

### What it is

Three sessions and one thread: **the number you measured does not belong to
the part.**

Session 17 said a part is manufactured, not found — a promoter has no second
edge, its strength depends on what it is next to, and joining it to a gene
changes the mRNA you were about to measure. Session 18 said the same circuit
can be built in a different medium, and the medium sets the clock: a toggle
out of phosphorylation runs in seconds, and its sharpness comes from
saturation rather than from cooperativity. Session 19 said two genes with no
wire between them still change each other, because they draw on one pool —
and this time there is no boundary you can impose.

| | |
|---|---|
| **Q1** | A promoter characterised on a plasmid, moved to the chromosome. What moves the number, which class of context each one is, and which you model versus hold fixed. |
| **Q2** | Golden Gate: the overhang count from scratch, the distance rule, and whether a proposed four-junction set will assemble. |
| **Q3** | The covalent cycle — the sensitivity index, the exchange rate into Hill coefficients, and where the sharpness comes from when nothing binds cooperatively. |
| **Q4** | CRISPRi, which is session 6's occupancy function with a different thing sitting on the promoter — and the term that is not in the model. |
| **Q5** | A recombinase memory element as a state table. No differential equation anywhere, and that is the point. |
| **Q6** | The shared-resource model: the partition function, the hyperbola that is not repression, and the diagnostic that tells them apart. |
| **Q7** | Burden coupled to growth, and what it does to a response time you already computed in PS2. |
| **Q8** | *Required for BioE 247, extra credit for BioE 147* — the two growth laws, the ceiling, and why a temperature shift does not move composition. |

### Before you start

**Q3, Q6 and Q7 use `posb` modules you have not used before** — `posb.protein`
and `posb.resources`. Both are imported for you in the setup cell, and both
are thin: every function in them is one or two lines of the algebra from the
session. Read the source if a result surprises you.

**Q4 and Q5 ask you to write the model, not to call one.** There is no
`posb.crispri` and no `posb.recombinase`, deliberately. Both models are small
enough that typing them is the exercise — one is a single occupancy
expression, and the other is a table with no calculus in it at all.

**Q1, Q5 and Q8 are written answers.** They are graded on the argument, not on
the conclusion. An answer that reaches the wrong number for a stated and
sensible reason scores better than the right number with no reasoning.

**Two of these pick up where an in-class sheet stopped.** The
K-moves-with-demand diagnostic is session 19's handout item 1(d) and is Q6c
here. Session 18's ledger — which knob is a promoter and which is protein
engineering — is that handout's section 4, and Q3d asks the half of it the
handout does not.

### What the visible tests do

They check shape, sign, structure and limiting behaviour — not your exact
numbers. A test that passes means your function returns the right *kind* of
thing and behaves correctly where the answer is forced: at zero demand, at
saturation, and in the limit where a parameter goes away. **The values are
checked by hidden tests**, so a green visible check means "not obviously
broken", not "right".

Several questions have a check you can do by hand before you trust the code —
a pure number that falls out of the algebra, an invariance that must hold
however you set a parameter, a limit you can take in your head. Work those out
on paper first. If the code disagrees with the paper, the error is usually
upstream of the test.

### Solutions

Distributed through bCourses after the deadline, as always. Not in this
repository.
