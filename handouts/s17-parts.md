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

**What they built.** Kosuri *et al.* (2013) designed all 114 × 111 promoter ×
RBS combinations — 12,654, less one that created an incompatible restriction
site, so **12,653** — synthesised them as an oligo library,
and cloned them into a single vector carrying **sfGFP** as the output and a
constitutive **mCherry on the same plasmid** as an internal control. Protein
levels came from **FlowSeq**: sort the population into twelve log-spaced bins
by the sfGFP/mCherry ratio, sequence each bin, and reconstruct every
construct's level from where its reads landed. RNA came from RNA-seq, reported
as an RNA/DNA ratio.

Note what the mCherry is for: it divides out the cell-to-cell and
plasmid-to-plasmid variation that would otherwise be mistaken for part
behaviour. **The instrument needs insulating before the parts do.**

With that, the variance decomposes as:

| | promoter | RBS | unexplained |
|---|---|---|---|
| RNA level | 92% | 4% | 4% |
| protein level | 54% | 30% | 16.7% |

**(a)** The RBS is a *translational* element. Give a mechanism by which it
takes 30% of the variance in protein but only 4% in RNA.

**(b)** In the same study, a 10-fold increase in translation efficiency
**correlates with** about a 3-fold increase in RNA abundance — though it
saturates: the weakest-to-strongest RBS span of 87-fold corresponds to only
about 4.3-fold in mRNA.

Which of the three failures on the front page is this? And why does it mean
the $p \times r$ model is not merely inaccurate but has **no true $p$ to
estimate** — so that collecting more data cannot fix it?

**(c)** 64% of protein levels land within twofold of the $p\times r$
prediction; the largest 5% of deviations are off by **an average of 13-fold**. You are designing a
ten-gene pathway and need every gene within twofold. Assuming independence,
what fraction of ten-gene builds has every gene inside tolerance? Is
independence a safe assumption here, and does it make your estimate optimistic
or pessimistic?

---

## 3 · Where prediction works, and what that tells you

**What they built.** You cannot measure a terminator with one reporter — you
would be measuring the promoter too. So Cambray *et al.* (2013) built a
measurement device: **green and red fluorescent reporters bracketing the
terminator test site**, and read-through estimated as the ratio of downstream
to upstream fluorescence. Termination efficiency is what is left; 100% means
every arriving polymerase was stopped.

A ratio is still contaminated, because mRNA stability differs on either side.
So the device also carries **RNase sites flanking the test site, to
standardise the ends of the processed mRNA** — the same move as item 2's
mCherry, one layer down.

They then fitted a **linear model**: four sequence features chosen by
stepwise selection out of twelve candidates, fitted on **31 curated
terminators**, and then used to predict **23 that were held out**. The
features are biophysically motivated — hairpin stability normalised by length,
the U-tail, the closing base pair.

The paper reports **r = 0.9 (cross-validated 0.85) on the 31 it trained on**,
and r = 0.67 (CV 0.61) across all 54. Below, recomputed from the supplementary
table, is the median **signed** error per class — positive means the model
predicted more termination than was measured:

| class | n | median predicted − measured (TE points, out of 100) |
|---|---|---|
| `terminator` — the curated training set | 31 | +0.7 |
| extended (ET) | 6 | **−8.3** |
| low folding frequency (LFFT) | 9 | +5.3 |
| low efficiency (LET) | 7 | **+44.4** |
| both (LFFT/ET) | 1 | +26.1 |

**(a)** A colleague reports the pooled correlation over all 54 and concludes
the model is weak. Two things are wrong with stopping there. Name both: one is
about the **classes**, and one is about **which terminators the model was
fitted on**.

**(b)** Look at the sign column. The model does not miss at random: LET and
LFFT are **over**predicted, ET is **under**predicted, and the paper says
exactly this. Explain why a model that fails in named, *directional* ways is
more useful than one with the same average error scattered at random.

**(c)** Complete the sentence in your own words, in **no more than fifteen
words**: *"Prediction from sequence works when ______."*

---

## 4 · Joining them, and the arithmetic of overhangs

**Why this method and not another.** Restriction cloning puts the junction
wherever a usable site happens to be, and leaves that site in the product.
Gibson joins on a 20–40 bp overlap built into the ends — scarless, but the
junction is whatever the parts' ends are, and you cannot standardise it across
a library. **Golden Gate uses a Type IIS enzyme, which recognises one sequence
and cuts at a fixed offset *outside* it.** Put the recognition site on the
scrap side and it departs with the scrap: the product carries no site, and the
junction left behind is **four bases you chose**. One pot, many parts, in a
defined order.

Gibson's overlap is designer-specified too, but it is long, different for
every pair, and cannot be standardised across a library. Golden Gate's junction
is **short, enzyme-defined and fixable community-wide** — which is why it is
the method this session cares about.

**(a)** There are $4^4 = 256$ four-base overhangs. A **palindromic** overhang
equals its own reverse complement, so it anneals to a copy of itself and the
fragment can go in either way round — directionality is lost. How many
palindromic four-base overhangs are there? *Show the counting.*

**(b)** An overhang and its reverse complement are the same junction identity.
Using your answer to (a), how many **distinct usable** junction identities are
there?

**(c)** Your answer to (b) looks like plenty. In class we saw that choosing
junctions at random gives even odds that two of them are one base apart — or
one base from each other's reverse complement — at about **four junctions**.
Why does the *number* of available overhangs turn out not to be the binding
constraint? (A circular assembly of $n$ parts plus a backbone needs $n+1$
junctions, so four junctions is a three-part build.)

**(d)** The four-base scar you choose for cloning convenience sits inside the
transcript. Cambray *et al.* (2018) found that secondary structure around the
start codon accounts for 83% of what designed sequence properties explain.
**Connect those two sentences.** *Two lines.*

---

## Stretch — the one nobody has answered

Manufacturing works. Mutalik *et al.* (2013) report that the best available
computational tool for designing translation control elements gives about a
**47%** chance of landing within twofold of a target expression level. With
transcription elements that encode a **common mRNA start** and bicistronic
translation elements, they landed arbitrary genes within that same twofold
window about **93%** of the time. Same question, same tolerance, same paper.

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
