<!--
title: Session 25 — Design at population scale
subtitle: A home guide, worked after class. Item 1 is the one mutation the six equations have no term for; item 2 is their stability floor against our closed form, which disagree; item 3 is the rounding that decides the threshold exactly where the threshold sits; item 4 is a gene drive's invasion, its resistance and its containment, which are three different claims. Answers come on a separate sheet.
session: 25
-->

# How to use this

Work it after class, on paper. The answers are on a separate sheet — read
them **after** you have written something down, not instead of writing
something down.

Nothing here asks you to compute the genotype partition of a co-infected
cell, or to solve the threshold for $P$ or for $D$. Those are the two
calculations the session ran and they are the two you will be graded on;
this guide works the territory around them, which is where the mistakes
get made. None of it needs a computer. Items 1, 2 and 3 need the
Weinberger paper open and send you to its figures and its discussion by
name. Item 4 is self-contained — every number from Noble it uses is printed
below, so you can work it whether or not you read the optional paper.

**The symbols, once.** $P$ is the **packaging advantage**: the cytoplasmic
crHIV-1 : HIV-1 mRNA ratio in a dually infected cell is $P : 1$, so $P = 8$
means eight vector transcripts for every viral one. $D$ is the **antiviral
effect**, and it is the fraction of HIV-1 production that **remains** — so
$D = 1$ is no inhibition and $D = 0.01$ is a cargo that removes 99% of viral
output. $n = 200$ is the burst size, virions released from an infected cell;
$c = 30$ day⁻¹ is the virion clearance rate; $d = 0.02$ day⁻¹ and
$\delta = 0.7$ day⁻¹ are the death rates of an uninfected and an
HIV-infected cell. An $I_T$ cell carries the vector and makes no virus; an
$I_D$ cell is dually infected and makes both; $V_T$ is free vector. For this
patient $R_0 = 1.9375 = 31/16$, so $1 - 1/R_0 = 15/31$ and

$$R_0^T = P^2 D \left(1 - \tfrac{1}{R_0}\right), \qquad
\text{persistence needs } P^2 D > \tfrac{31}{15} = 2.0667$$

**One warning about $D$, because item 1 turns on it.** The paper's prose
defines $D$ as "the fraction by which the HIV-1 titer produced from $I_D$
cells is therapeutically downregulated", which reads the opposite way round
from how the equations use it. The equations are what we follow: $D$
multiplies production, so a bigger $D$ is a worse drug.

**And one about $R_0^T$.** Every numerical value of $R_0^T$ below counts a
new infection at the moment a cell becomes an $I_T$ cell, which is the
convention the session derived. Build the next-generation matrix the
textbook way — counting virion production as a new infection too — and you
get the square root of the same quantity, and you are right. The threshold
at one is the same either way; the magnitude is not.

---

## 1. The equations have no term for a vector that loses its cargo

Equations [1]–[6] carry $P$ and $D$ as constants. Nothing in them changes
either one over time, and no term anywhere describes a vector whose sequence
has changed. Weinberger says so and calls mutation "of more concern" than
recombination, closing with a sentence about what is missing: "Models that
examine the likelihood of crHIV-1 mutation into a nontherapeutic virus must
be examined."

So take the hour's own construct and let one mutate. A vector at $P = 8$
needs $D > 0.0323$ to persist, so a construct built at $P = 8$ with
$D = 0.0323$ sits exactly at $R_0^T = 1$ — a 96.8%-effective cargo, as good
as this packaging advantage can afford. Now one virion's cargo gene is
broken by a point mutation that leaves the packaging elements, the promoter
and therefore $P$ untouched. Assume $P$ really is unchanged.

**(a)** What is the broken vector's $D$? Weinberger states the answer for
this exact case on journal page 10031, in one clause. Then compute its
$R_0^T$ and compare it with the therapy's. (If your answer makes the
cargo-less vector *worse* at spreading, read the warning about $D$ again.)

**(b)** Write the ratio of the two reproductive ratios in symbols, for a
therapy at any $(P, D)$. Then say what it does as the cargo gets better, and
why that is the paradox from this morning arriving a second time with a
different sign.

**(c)** Two things could be wrong with a batch of vector. One: every
particle in it is slightly leakier than specified. Two: a fraction of
particles lose the cargo each round of replication. For each, say whether
equations [4]–[6] can represent it by a choice of $P$ and $D$, or whether it
needs something the model does not have — and if it needs something, say
exactly what.

**(d)** The paper offers one design move that would make the escape mutant
harmless, and one claim about mutation that it states with no model behind
it. Name both, and say which one you would put in a grant application.

---

## 2. Their floor and our contour are not the same line

The closed form above gives one curve in the $(P, D)$ plane: $P^2D = 31/15$,
with everything above it persisting. Sweeping $R_0$ from 1.9 to 20 moves the
threshold between about 1.05 and 2.11, which is the band the design-space
figure carries.

Fig. 3a of the paper carries a different boundary, got a different way. Its
floor is a stability map of the simulated model, painted in three colors:
**red** where the pretherapy HIV-1 steady state is stable and crHIV-1 dies,
**cyan** where the crHIV-1 solution is stable, and **black** where the
system oscillates. Reading the red-to-cyan transition off that floor at
300 dpi and converting it to the product $P^2D$:

| $D$ range | their boundary, as $P^2D$ | ours |
|---|---|---|
| 0.08 – 0.20 | 1.14 – 1.29 | 2.0667 |
| 0.35 – 0.50 | 2.15 – 3.86 | 2.0667 |

The same two boundaries written as the least $P$ that survives, at two
values of $D$:

| | $D = 0.2$ | $D = 0.5$ |
|---|---|---|
| their floor | $P = 2.39$ to $2.54$ | $P = 2.07$ to $2.78$ |
| our contour | $P = 3.21$ | $P = 2.03$ |

Two things about the reading itself. The transition is not a hairline: it is
0.12 to 0.26 wide in $P$. And the digitization has a calibration check that
**passes** — the black pixels come out at $P > 11$ and $D$ from 0.05 to 0.13,
median 0.094, against a text that puts the oscillatory region at "$P > 10$
and $D \approx 0.1$".

**(a)** You have a construct at $P = 2.8$ and $D = 0.2$. Which way does each
boundary vote, and what would you have built on the strength of each? Give
the product.

**(b)** Here are three explanations for the gap. For each one, work out which
way it would push their boundary and roughly how far, and say which of the
three could produce a boundary that *crosses* ours rather than sitting to
one side of it.

- The floor was digitized off a perspective drawing, so the coordinates are
  imprecise.
- Their simulations include the 1.5-day viral eclipse phase, which our closed
  form leaves out. A delay between infection and production puts a survival
  factor into every generation and lowers $R_0^T$.
- Table 1's footnote says analyses without the eclipse phase used $c = 3$
  rather than $c = 30$. That gives $R_0 = 19.375$ instead of 1.9375.

**(c)** The calibration check passes. Say what that buys you and what it does
not.

**(d)** Read the floor's own legend again, and say what the red-to-cyan
transition is a boundary *of*. Then write the one sentence you would put
under a figure that shows both lines. "The simulation confirms the closed
form" is not it, and neither is "the closed form is wrong".

---

## 3. The rounding that matters most where the threshold is

An $I_D$ cell packages two strands per capsid, so it releases three kinds of
particle, and the middle kind carries one strand of each. An et al. (1999)
found that heterozygous lentiviral virions infect and are internalized and
then meet a partial preintegration, postfusion block. Weinberger rounds that
partial block to zero, which strikes the heterozygotes out of the infectious
output and makes the infectious ratio $1 : P^2$, HIV-1 first.

Were they infectious instead, the ratio would be $1 : P(P+2)$ and every
$R_0^T$ in the session would be multiplied by $(P+2)/P$:

| $P$ | 1 | 2.27 | 3.21 | 8 | 100 |
|---|---|---|---|---|---|
| $(P+2)/P$ | 3.00 | 1.88 | 1.62 | 1.25 | 1.02 |

For scale: the fraction of everything an $I_D$ cell makes that is a
heterozygote is $2P/(1+P)^2$, which is largest at $P = 1$, where it is
exactly one half.

**(a)** Which way does the rounding push $R_0^T$? Then answer the question
that matters: is it a conservative assumption, and conservative about what?
There are two claims in this paper that it does not treat the same way.

**(b)** Read the table and say where the correction has leverage. Then say
why that location is uncomfortable, given where the paper's headline design
point sits and where the threshold sits.

**(c)** Two sources hold the rounding up. An et al. is one in vitro paper
reporting a partial block. The other is reference 46, Podsakoff 2001,
*Mol. Ther.* 4:282–283 — a two-page commentary reviewing a first clinical
protocol for a lentiviral vector, cited here for experimental mouse results.
Write the one-sentence referee comment you would send.

**(d)** An et al. give a mechanism for the block: reverse transcriptase has
to jump between two strands of very different length — 10 kb against about
4 kb — and cannot finish the steps integration needs. Take that mechanism
seriously and it predicts something about **your** construct that "heterozygous
virions are not infectious" does not. Say what it predicts, and what you would
build and measure to test it.

---

## 4. Invasion, resistance and containment are three different claims

Noble's drive sits at one locus with three alleles: wild type, drive and
resistant. Six genotypes, and one row does all the work. In the germline of
a WD heterozygote the drive cuts the wild-type allele and the cut is repaired
either into a drive copy, with probability $h$, or into a resistant allele,
with probability $1 - h$. So that heterozygote's gametes are $(1+h)/2$ drive
and $(1-h)/2$ resistant, **and no wild type at all**. $h$ is the homing
efficiency, and it is a repair outcome *given a cut*.

What you need from the paper is here:

| | |
|---|---|
| deterministic invasion condition | $f(1+h) > 1$, where $f$ is the WD genotype's fitness and wild-type fitness is 1 |
| $h$ from a cross | $h = 2A_D/T - 1$, where $T$ counts the alleles that were drives or were subject to drive and $A_D$ the resulting drive alleles |
| published efficiencies | 14% to 100% across five constructs; the paper's own summary range is 0.37 to 0.99 |
| the fitness used | $f = 0.9$ in every main figure, a dominant cost, with resistance neutral. Noble states that $f$ "is typically not measured in proof-of-concept studies" |
| what the simulations say about cost | at $h = 0.5$, a drive tolerates costs up to 20% before median peak drive falls below 0.3 |
| escape | the drive reaching frequency 0.1 in a subpopulation other than the one it was released into. Noble calls the 0.1 cutoff "arbitrary" |
| migration | with a migration probability $m$ and $N$ individuals in total, the mean time between migration events is $(1-m)/(Nm)$ generations |
| offspring | with $k$ adult offspring per mating the effective population size is $4N/(2k+6)$, and the basic model is $k = 1$. Noble's own consequence: an organism with 100 surviving offspring needs a release of about 258 to clear a threshold that is 10 individuals in the basic model |

**(a)** Crosses with a new construct give $A_D/T = 0.76$. What is $h$, what
is the largest fitness cost the deterministic condition lets it carry, and
which number in that verdict has never been measured for any drive? Then
compare your answer with the 20% in the table and say why the two numbers
differ.

**(b)** A referee writes: "resistance prevents the drive from spreading, so
an escaped drive is self-limiting." Two things are wrong with that sentence.
Give both, and name where the resistant alleles came from.

**(c)** $h$ is a repair outcome given a cut, and the model has no parameter
for a germline that does not cut. Suppose some fraction of WD germlines
never cut.

1. Which of the two gamete probabilities is then wrong, and in which
   direction?
2. A classmate concludes that the appendix table therefore counts uncut wild
   type as resistance. Is that what the appendix does? Say what it reports
   and where the pooling happens instead.
3. Of the paper's two headline claims — that the drive invades, and that
   resistance spreads instead where it does not — say which one this
   weakens, and why the other survives.

**(d)** You are assessing an accidental release of two organisms into a
species with about 100 offspring surviving to adulthood. Use the table: what
does "two organisms" become as a count of animals, and does high fecundity
make escape easier or harder? Then, given your answer to (b), say which
quantity a containment specification has to bound, and why the frequency of
the drive allele is not it.
