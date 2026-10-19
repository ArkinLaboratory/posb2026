<!--
title: Session 17 — What a part is, and what it costs to make one
subtitle: Four to work. Everything on this sheet is about the same thing: the number you measured on a part may not belong to the part.
session: 17
-->

# What a part is, and what it costs to make one

**The claim the whole hour tests.** A parts list promises you this:

$$\text{protein out} \;=\; p \times r$$

where $p$ is what the promoter does and $r$ is what the RBS does. Two numbers,
each belonging to one part, multiplied. Every abstraction in this course so
far has assumed something of this shape: **composing two things combines their
behaviours and leaves the things alone.**

**The three ways a promoter refuses to be a thing.**

| | |
|---|---|
| **no boundary** | 5′-RACE tells you where transcription *started*. There is no second edge — not operationally, not in the annotation, not in any model. |
| **not contained** | strength depends on flanking DNA, on the host, on ribosome availability. None of that is in the tube, and we have no model for how it moves the number. |
| **joining changes both** | the transcript's 5′UTR is encoded at the junction, and the 5′UTR sets RNA stability. Attaching a promoter to a gene changes the mRNA's lifetime — and so the RNA level you were about to call "promoter strength". |

**Three classes of context**, after Cardinale & Arkin (2012). Use these names;
they have different fixes.

| | |
|---|---|
| **compositional** | what the neighbours do. *Physical*: parts on one DNA, RNA or polypeptide interacting. *Functional*: two consumers drawing on one shared output — retroactivity. |
| **host** | parasitic interaction with the cell's own machinery; competition for ribosomes, tRNAs, proteases; coupling to growth and replication. |
| **environmental** | temperature, pH, medium — directly, and through the host's response. |

---

## 1 · Move a promoter, and say what kind of trouble you are in

You characterised promoter **P** carefully: high-copy plasmid, GFP downstream,
DH5α, LB, 37 °C. You now want it on the chromosome, in front of a different
gene, in a production strain, in minimal medium.

**(a)** Name **four** things that could move the number, and classify each one
as compositional, host or environmental.

**(b)** Exactly one of your four is different in kind from the other three.
Which, and what is the difference? *One sentence.*

**(c)** For each of the other three, say whether you would **model it**, or
**hold it fixed and report it**. There is no third option, and the choice is
not the same for all three.

---

## 2 · How much of the answer do the parts own?

Kosuri *et al.* (2013) built all 114 × 111 promoter × RBS combinations —
12,653 constructs — and decomposed the variance:

| | promoter | RBS | unexplained |
|---|---|---|---|
| RNA level | 92% | 4% | 4% |
| protein level | 54% | 30% | 16.7% |

**(a)** The RBS is a *translational* element. Give a mechanism by which it
takes 30% of the variance in protein but only 4% in RNA.

**(b)** In the same study, a **10-fold** change in translation efficiency moved
RNA abundance about **3-fold**. Which of the three failures on the front page
is this, and why does it make the $p \times r$ model not merely inaccurate but
**ill-posed**?

**(c)** 64% of protein levels land within twofold of the $p\times r$
prediction; the worst 5% are off by **13-fold**. You are designing a
ten-gene pathway and need every gene within twofold. Assuming independence,
what fraction of ten-gene builds has every gene inside tolerance? Is
independence a safe assumption here, and does it make your estimate optimistic
or pessimistic?

---

## 3 · Where prediction works, and what that tells you

Cambray *et al.* (2013) fitted a biophysical model of terminator strength.
Recomputed from the paper's own supplementary data, 54 terminators:

| class | n | $r$ | median miss (TE points, out of 100) |
|---|---|---|---|
| `terminator` | 31 | 0.97 | 2.6 |
| extended (ET) | 6 | 0.89 | 8.3 |
| low folding frequency (LFFT) | 9 | 0.16 | 11.9 |
| low efficiency (LET) | 7 | 0.38 | 44.4 |

**(a)** Over all 54, $r = 0.62$. Over the 31 in the first row, $r = 0.97$. A
colleague reports the 0.62 and concludes the model is weak. What has the split
by class told you that the pooled number hides?

**(b)** The paper itself names ET, LFFT and LET as the classes its model
overestimates. Why does that make the result **stronger** rather than weaker?

**(c)** Complete the sentence in your own words, in no more than fifteen:
*"Prediction from sequence works when ______."*

---

## 4 · Joining them, and the arithmetic of overhangs

Golden Gate uses a Type IIS enzyme that cuts **outside** its recognition site,
so the site leaves with the scrap and the junction is four bases of your
choosing.

**(a)** There are $4^4 = 256$ four-base overhangs. A **palindromic** overhang
equals its own reverse complement and so ligates to itself. How many
palindromic four-base overhangs are there? *Show the counting.*

**(b)** An overhang and its reverse complement are the same junction identity.
Using your answer to (a), how many **distinct usable** junction identities are
there?

**(c)** Assembling $n$ parts in one pot needs $n+1$ junctions. Your answer to
(b) looks like plenty. In class we saw that picking them at random gives even
odds of two junctions differing by a single base at about **five parts**. Why
does the *number* of available overhangs turn out not to be the binding
constraint?

**(d)** The four-base scar you choose for cloning convenience sits inside the
transcript. Cambray *et al.* (2018) found that secondary structure around the
start codon accounts for 83% of what designed sequence properties explain.
**Connect those two sentences.** *Two lines.*

---

## Stretch — the one nobody has answered

Manufacturing works: with transcription elements that encode a **common mRNA
start** and bicistronic translation elements, Mutalik *et al.* (2013) landed
arbitrary genes within twofold of a target window about **93%** of the time,
against 64% for collected parts.

The same group, the same year, also proposed a **measurement standard** for
part collections — an ANOVA framework reporting a part's *activity* and a
second statistic, its *quality*, which tracks how much that activity moves
across contexts.

The standard did not take.

**Write one paragraph.** What would a part-measurement standard have to offer a
working lab for that lab to pay the cost of adopting it? Be concrete about who
pays and who benefits, and name one reason the 2013 proposal might have failed
that is *not* "people are lazy".

---

*Sources for every number here: Cardinale & Arkin, Biotechnol J 7:856–866
(2012); Kosuri et al., PNAS 110:14024–14029 (2013); Cambray et al., NAR
41:5139–5148 (2013); Mutalik et al., Nat Methods (2013), two papers; Cambray,
Guimaraes & Arkin, Nat Biotechnol (2018).*
