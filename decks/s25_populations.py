"""Session 25 — It has to spread on its own.

Thursday 19 November 2026. Part II, tenth session, and the one where the
object stops being a circuit inside a host you own and becomes an infectious
agent. Weinberger, Schaffer & Arkin, J. Virol. 77(18):10028-10036 (2003) was
assigned at the close of session 24.

WHAT THIS SESSION IS. Once the thing you build has to spread by itself, the
specification stops being a transfer function and becomes a reproductive
ratio greater than one. And WHAT TRADES AGAINST WHAT in that ratio is a
property of the architecture, not of the idea:

    in Weinberger's vector the therapeutic payload sits INSIDE the vector's
    own fitness, so there is an optimum rather than a maximum;
    in a gene drive the two come apart.

A student who leaves with only move 4's lesson has learned a fact about
lentiviral vectors and mistaken it for a principle. That is why move 5 is not
an appendix.

THE ROOM HAS NEVER SEEN A VIRUS. The census in the session design is the
reason the hour opens on drawings: virion, capsid, diploid, heterozygous,
allele, helper virus, R0, invasion and transcritical are all ZERO across the
22 built decks, while steady states, eigenvalues and bifurcations run to tens
of slide-facing hits each. This session has no mathematics problem. It has an
object problem, and segment 1 is built for that and nothing else.

NOTATION, AND IT IS RECORDED IN docs/symbols.md. P is the packaging advantage
and D the antiviral effect; both are autograded on PS9 (T67, T73) and sit on
the final, so neither letter moves. Noble ALSO prints P for his homing
efficiency, and he names his alleles W, D and R. The gene-drive material is
T75, assessed by the home guide and the final and hand-graded, so it is the
side that moves: the homing efficiency is h here, the invasion condition is
f(1 + h) > 1 and the boundary f > 1/(1+h). The allele names stay Noble's,
because they are on his crops -- but they are written as GENOTYPES (WW, WD,
DD, DR) or as noun phrases ("the W gamete", "the resistant allele"), never as
a bare letter in a place where it reads as a quantity. His crops still carry
his own axis label P, so segment 5's first crop slide says once, in body type,
that his P is our h. That is a bridge to a published figure, not a
disambiguation of two live meanings, and a foot note would not do it: deck-bar
B1 counts a symbol settled only in a foot or a speaker note as unsettled.

THE TWO THINGS A LATER PASS MUST NOT UNDO, both of which an earlier draft of
the design got wrong:

  * R0_T is PROPORTIONAL to P^2*D, not approximately equal to it. The
    coefficient 1 - 1/R0 is 15/31 at this patient's R0, and dropping it is
    not a rounding -- a student who takes P^2*D > 1 as the threshold gets
    P > 2.236 at D = 0.2 where the figure, the autograder and this deck all
    say 3.21. T73 is autograded on PS9 AND sits on the final.
  * infectious_fraction is NOT monotone. It FALLS to 1/2 at P = 1 and rises
    after. An evenly balanced co-infected cell is the worst case, not the
    best one.

R0_T IS DERIVED HERE, NOT CITED. W03 puts its derivation in a supplementary
file behind a dead URL. It was re-derived from equations 4-6 by
next-generation matrix (NUMBERS.md 18, three independent verifications) and
the published form is exactly right with no added assumption. So segment 3
teaches the derivation, and it says out loud -- while the matrix is on the
slide -- that the textbook van den Driessche-Watmough split gives
sqrt(P^2*D*(1 - 1/R0)) instead, that the threshold at 1 is identical, and
that a student who builds it that way IS RIGHT. They should not find that
out from a mark.

THE PAPER IS ADAM'S. No hedging and no apology on a slide, and it gets
checked as hard as anyone else's. The hour finds ONE transcription slip --
the printed delta where a d belongs in R0 -- and TWO facts about how the
model got its numbers: lambda and k were back-solved from T0 and V0 rather
than measured, and the burst-size assumption is stated plainly in three
places and bounded in none of them. One slip and two honesties, not three
errors.

Numbers: sessions/s25-populations/NUMBERS.md, every one tagged with its kind.
Nothing on a slide that is not in that file, with three disclosed exceptions
noted at their call sites: the Fig. 3a floor digitization, which lives in
figures/s25_populations.py and is marked INFERRED BY US there; session 24's
and session 2's retrieval answers, which are in those sessions' own NUMBERS
files; and the van den Driessche & Watmough citation on the convention slide
-- Math. Biosci. 180:29-48 (2002) -- which is a reference and not a number,
and which NUMBERS.md 18.4 names without its year.

Build:  python tools/build_decks.py s25_populations
"""
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN, HEAD)

# W03 FIG. 2a's OWN FIVE CURVE colorS, SAMPLED FROM THE CROP'S PIXELS.
# Deliberately NOT theme colors: these exist to be matched against the
# raster beside them, so a swatch that is "our teal" instead of "their
# blue" is a key that does not key anything. Sampled from
# private/paper-figures/weinberger2003_fig2a.png (modal stroke color of
# each legend swatch, cross-checked against the same curve in the plot
# body away from the legend box).
#
# THE D VALUES ARE NOT READ OFF THE LEGEND -- the legend is the thing that
# is illegible. They are NUMBERS.md 5c, which lists exactly five curves,
# D = 0.8, 0.6, 0.4, 0.2, 0.01, read there at 600 dpi. The color-to-value
# mapping is then anchored three ways rather than assumed: NUMBERS.md 5c
# names the OSCILLATING trace D = 0.2 and it is the gray one; 5c and
# NUMBERS.md 9 name the trace flat at the pretherapy set point D = 0.01
# and it is the green one; and the remaining three order by set point,
# which falls as D falls to ~0.4 (NUMBERS.md 9). Three anchors, one
# mapping, and the legend was not consulted for any of them.
W03_CURVES = [("D = 0.8",  RGBColor(0xD7, 0x28, 0x3C)),    # red
              ("D = 0.6",  RGBColor(0xEE, 0xCE, 0x3B)),    # yellow
              ("D = 0.4",  RGBColor(0x3C, 0x46, 0x92)),    # blue
              ("D = 0.2",  RGBColor(0x8C, 0x86, 0x84)),    # gray
              ("D = 0.01", RGBColor(0x47, 0x94, 0x50))]    # green

FIG = "figures/build/"
FILENAME = "s25-populations"


def build():
    d = Deck("Session 25 — It has to spread on its own", session=25)
    # No printed time ranges. Adam runs about a third faster than any
    # slide-count estimate and has said so twice, so a badge carrying a
    # range is read as a commitment the deck cannot keep.
    d.show_badges = False
    # Adam, 8 Nov: the new aside standard applies going forward. Week 13
    # opts in; the taught decks keep what is posted.
    d.aside_standard = True
    _opening(d)
    _retrieval_threshold(d)
    _retrieval_threw_away(d)
    _retrieval_binomial(d)
    _goals(d)
    _where_this_sits(d)

    _weinberger_intro(d)
    _s1_frame_objects(d)
    _s1_frame_words(d)
    _s1_build_ledger(d)
    _s1_build_1970(d)
    _s1_release(d)
    _s1_debrief(d)

    _s2_frame(d)
    _s2_build(d)
    _s2_strikeout(d)
    _s2_infectious(d)
    _s2_release(d)
    _s2_debrief(d)

    _s3_frame_count(d)
    _s3_frame_clinical(d)
    _s3_frame_model(d)
    _s3_build_chain(d)
    _s3_build_printed(d)
    _s3_build_backsolve(d)
    _s3_build_construction(d)
    _s3_build_names(d)
    _s3_build_equilibrium(d)
    _s3_build_waiting(d)
    _s3_build_factors(d)
    _s3_build_threshold_line(d)
    _s3_build_deltaprime(d)
    _s3_build_ngm(d)
    _s3_build_matrix(d)
    _s3_build_meaning(d)
    _s3_build_clinical_threshold(d)
    _s3_build_band(d)
    _s3_build_theirs(d)
    _s3_release(d)
    _s3_debrief_ours(d)

    _s4_frame_model(d)
    _s4_frame_dsense(d)
    _s4_build_shared(d)
    _s4_build_fig2a(d)
    _s4_build_setpoint(d)
    _s4_build_fig2b(d)
    _s4_poll(d)
    _s4_poll_debrief(d)
    _s4_build_burst(d)
    _s4_build_assumption(d)
    _s4_build_capped(d)
    _s4_build_capped_number(d)
    _s4_build_evidence(d)
    _s4_build_pitchai(d)
    _s4_build_1970(d)
    _s4_release(d)
    _s4_debrief(d)

    _s5_change(d)
    _s5_frame(d)
    _s5_build_super_mendelian(d)
    _s5_build_idealisation(d)
    _s5_build_f(d)
    _s5_build_invasion(d)
    _s5_build_release_size(d)
    _s5_build_containment(d)
    _s5_build_exhaust(d)
    _s5_build_title(d)
    _s5_release(d)
    _s5_debrief(d)

    _close_ledger(d)
    _close_limits(d)
    _close_sentence(d)
    _close_reading(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    s = d.dark()
    d.text(s, "Session 25  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    # PLAIN TITLE, SUBTITLE CARRIES THE CLAIM, and no technical form on the
    # slide the room reads first. R0_T > 1 is the hour's result and it
    # arrives in segment 3 where it is derived; a symbol this course has
    # never defined is opaque on a title slide however exact it is.
    d.text(s, "It has to spread on its own",
           M, 2.72, 8.6, 1.5, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "You still have only molecular knobs — and what they now set "
              "is whether it spreads faster than it is removed.",
           M, 4.30, 8.6, 1.70, size=18, color=MINT, spacing=1.2)
    d.notes(s,
           "The title is the claim and the subtitle is the whole hour in one "
           "sentence. I say it before anything else.\n "
           "The object today is not a circuit inside a host I own. It is an "
           "infectious agent, and its specification is a number greater than "
           "one.\n "
           "I do not open on HIV biology and I do not open on gene drives. "
           "The room already has every piece of mathematics this needs — a "
           "steady state, a threshold at an eigenvalue crossing, and a "
           "selection coefficient from last Thursday. What it does not have "
           "is the objects, and that is the first segment.")


def _retrieval_dilution(d):
    # THE SYSTEM IS REDRAWN ON THE SLIDE THAT ASKS ABOUT IT (deck-bar F1),
    # AND SINCE 8 NOVEMBER IT IS ACTUALLY THE SYSTEM.
    # This slide used to carry session 24's `s24_hopf_D` -- leading Re lambda
    # against D, under an eleven-symbol parameter header. That satisfied F1
    # on a technicality and failed it in substance: the slide asks "what
    # happened to the PREDATOR", and there was no predator in the picture,
    # no chemostat, no two strains and no quorum signal. Not one of the
    # eleven symbols was needed to answer it. F1 asks for the SYSTEM
    # redrawn, not the conclusion replotted.
    # `s25_recall_chemostat` draws the vessel, the inflow and outflow both
    # labeled D, the four species as a loop, and grays the predator out
    # past 0.31 h^-1 -- which is the answer the question is fishing for. It
    # uses session 24's own colors so the room recognizes the object.
    s = d.light()
    d.header(s, "open", "retrieval — on your own paper, session 24")
    d.title(s, "What raising session 24's D did")
    d.image_centered(s, FIG + "s25_recall_chemostat.png", top=1.80,
                     band=4.14)
    d.foot(s, "What quantity was D there, and what happened to the predator "
              "as you turned it up?")
    d.notes(s,
           "D was the dilution rate of the chemostat — the rate the culture "
           "was washed out, and the one knob they could still turn after the "
           "strains were built.\n "
           "Raising it washes the predator out. Fig. 3B of the chemostat "
           "paper measures coexistence at 0.15, a damped oscillation at "
           "0.23, and predator washout at 0.31 per hour.\n "
           "I want the letter D said out loud and attached to that meaning "
           "before I introduce today's D, because today's is a different "
           "quantity and it reads backwards — D = 1 will mean no drug at "
           "all. Two D's in one week is a trap I would rather spring on "
           "purpose.")


def _retrieval_qssa(d):
    s = d.light()
    d.header(s, "open", "retrieval — on your own paper, session 24")
    d.title(s, "What the approximation threw away")
    # Was `s24_qss_no_hopf`, whose right panel plotted |tr J| against |the
    # closed form| over 4000 random interior fixed points -- a BUILDER'S
    # PARITY CHECK, projected into a lecture hall, with its purpose stated
    # nowhere on the slide. It answered nothing the room was asked. The
    # check itself is stronger in the test suite, where it already lives
    # three times over (test_communities.py), and where a failure is loud
    # and a pass is silent.
    # `s25_recall_qssa` draws the discarded thing instead: the same circuit
    # at D = 0.11, integrated twice, differing only in whether the signals
    # keep their own dynamics. Limit cycle, then damped to the same point.
    d.image_centered(s, FIG + "s25_recall_qssa.png", top=1.80, band=4.14)
    d.foot(s, "You set the two signals to steady state and the oscillation "
              "vanished. What had you discarded?")
    d.notes(s,
           "The lag between a population and its own signal. With the "
           "signals at quasi-steady state the trace of the Jacobian is "
           "negative at every interior fixed point, so a two-state system "
           "cannot have a Hopf bifurcation, and the oscillation the whole "
           "session was about is simply gone.\n "
           "The answer I want is that the approximation deleted the "
           "phenomenon it was applied to, and the algebra says it had to.\n "
           "This is the item the close of today depends on. Every row of "
           "today's Limits column is the same question asked of a different "
           "assumption: what did this model throw away, and what would tell "
           "me I had left the regime where throwing it away was fine.")


def _retrieval_threshold(d):
    """Replaces _retrieval_dilution, 14 November 2026.

    The old slide asked what raising session 24's dilution rate did to the
    predator. Session 24's predator-prey reactor moved to its appendix on
    14 November, so that question reached back at something Tuesday no
    longer teaches. This one reaches at what Tuesday now closes on -- a
    quantity that has to beat a threshold before a design is worth doing --
    which is the direct ancestor of today's reproductive ratio.

    It gives the problem rather than testing recall: every number it needs
    is printed on it.
    """
    s = d.light()
    d.header(s, "open", "retrieval — on your own paper, session 24")
    d.title(s, "A number that has to beat another number")
    d.rows(s, [
        ("what you did Tuesday",
         "you decided whether to split a pathway across two strains. The "
         "rule was not “is the burden high” — it was whether one ratio "
         "beat another number."),
        ("the two sides", "biomass you gain by splitting, against the "
                          "intermediate you lose in transit. Split when the "
                          "first beats the second."),
        ("so, before we start",
         "name the quantity that had to be exceeded, say in one sentence "
         "what it was made of, and say what happens at exactly equal.",
         AMBER),
    ], top=2.05, label_w=3.1)
    d.notes(s,
            "θ_{I}, the inefficiency factor. It was built from the "
            "intermediate's transport rate and its turnover outside the "
            "cell — both of them, not their ratio — and from the "
            "downstream population's biomass.\n "
            "At exactly equal there is nothing in it: the split and the "
            "single cell produce the same, and the decision is made on "
            "something else.\n "
            "What I want said out loud is the SHAPE, because the hour runs "
            "on it: a design is worth doing when one number beats another, "
            "and the whole job is working out what is on each side. Today "
            "the number on the right is one."
            )


def _retrieval_threw_away(d):
    """Replaces _retrieval_qssa, 14 November 2026.

    Same cause: the old slide asked what the quasi-steady-state
    approximation deleted from the predator-prey model, and that move is in
    session 24's appendix now. Karig is the better vehicle and session 24
    teaches it properly -- a deterministic analysis that needs a
    hundredfold, a system that patterns at 21.6, and fluctuations that turn
    out to be part of the mechanism rather than noise on top of it.

    The close of today depends on this question: every row of the Limits
    column asks what a model threw away.
    """
    s = d.light()
    d.header(s, "open", "retrieval — on your own paper, session 24")
    d.title(s, "What the smooth model threw away")
    d.rows(s, [
        ("the requirement", "the deterministic analysis of Karig's lawn "
                            "needs the two signals to differ in diffusion "
                            "by about a HUNDREDFOLD before a pattern can "
                            "form."),
        ("what they measured", "21.6 — five times short of it."),
        ("and the lawn patterned anyway",
         "spots appeared, and the same kinetics run stochastically produce "
         "them at the measured ratio.", AMBER),
        ("so, before we start",
         "the model is not wrong. Say what it threw away, and why throwing "
         "it away removed the very thing being modelled."),
    ], top=1.98, label_w=3.1)
    d.notes(s,
            "It threw away the fluctuations. A deterministic treatment is "
            "continuous concentrations and effectively infinite "
            "populations, and that is an approximation with a validity "
            "condition like every other one in this course — large "
            "numbers. A lawn of bacteria with a handful of molecules per "
            "cell does not satisfy it.\n "
            "So the noise is not sitting on top of the dynamics. It is "
            "part of what makes the pattern, and smoothing it away deleted "
            "the phenomenon.\n "
            "This is the item the close of today depends on. Every row of "
            "today's Limits column is this question asked of a different "
            "assumption: what did this model throw away, and what would "
            "you see if it mattered?")


def _retrieval_binomial(d):
    s = d.light()
    d.header(s, "open", "retrieval — on your own paper, session 2")
    d.title(s, "A calculation this course owes you")
    d.rows(s, [
        ("you saw this", "a plasmid at five copies splits binomially between "
                         "two daughters, and P(one daughter gets none) is "
                         "2·(½)⁵, about six percent"),
        ("the promise", "that slide said session 25 does the full binomial "
                        "for a genome. Today is session 25"),
        ("so, before we start", "in that calculation, what was being drawn, "
                                "how many draws were there, and what fixed "
                                "the probability of each draw?"),
    ], top=2.05, label_w=3.1)
    d.notes(s,
           "Five copies, each going to one of two daughters, and the "
           "probability is one half because the physics fixes it. Two times "
           "a half to the fifth is 0.0625.\n "
           "Segment two pays this off and the difference is the lesson. "
           "Today there are exactly TWO draws, not five, and the probability "
           "is not fixed by physics — the engineer sets it. That is the only "
           "tunable thing in the whole hour that enters a probability.\n "
           "Session 2 asked about LOSS: does a daughter get nothing. Today "
           "asks about COMPOSITION: which genotype is this particle. Same "
           "distribution, different question.")


def _goals(d):
    s = d.light()
    d.header(s, "open", "what you should be able to do by the end")
    d.title(s, "Three questions")
    d.rows(s, [
        ("the partition", "A cell is making two kinds of genome at once and "
                          "packaging two strands per particle. What fraction "
                          "of what it releases can infect anything?"),
        ("the threshold", "A therapy that has to spread needs a reproductive "
                          "ratio above one. Whose reproduction, counted from "
                          "which cell, and what sets the number?"),
        ("the trade", "Why does making the drug stronger eventually kill the "
                      "therapy — and why does that stop being true the "
                      "moment you change the architecture?"),
    ], top=2.05, label_w=2.6)
    d.notes(s,
           "I answer all three now, briefly, so the hour has somewhere to "
           "land.\n "
           "The partition: a binomial on two draws. At the worst setting, "
           "exactly half of everything the cell makes is thrown away, and "
           "the worst setting is the balanced one.\n "
           "The threshold: counted from a cell that already carries the "
           "vector and is waiting for the virus. The number is the product "
           "of the packaging advantage squared and the drug's leak, and it "
           "has to clear about two.\n "
           "The trade: the payload sits inside the vector's own production "
           "term, so turning the drug up turns the vector down. Change the "
           "architecture so the payload competes instead of suppressing, and "
           "the optimum becomes a maximum. That is the last twenty minutes.")


def _where_this_sits(d):
    s = d.light()
    d.header(s, "frame", "where this sits")
    d.title(s, "The unit of design becomes the population")
    d.rows(s, [
        ("session 23", "the population REMOVES the circuit — selection is "
                       "the adversary"),
        ("session 24", "the population CONTROLS the circuit — another strain "
                       "holds its life"),
        ("today", "the population CARRIES the circuit — the genome is split "
                  "across cells", AMBER),
        ("session 26", "the population IS the thing being classified"),
    ], top=2.10, label_w=2.5)
    d.foot(s, "Session 23 asked how long a circuit survives a population. "
              "Today asks what it takes for one to invade.")
    d.notes(s,
           "Sessions 19 to 22 were one ladder — measure the burden, compute "
           "the bound, insulate the interface, reject the disturbance — and "
           "session 23 broke it, because selection is not a disturbance you "
           "can reject. It closed on levers that were not circuit design at "
           "all: intra-niche competition and a host-genome edit.\n "
           "Today is the same algebra with the opposite sign on the design "
           "goal. Last time we wanted the thing to persist against a "
           "population that was deleting it. Today we want it to invade one "
           "that never asked for it.\n "
           "That sign change is the whole reason this sits where it does.")


# ------------------------------ segment 1 · what you are allowed to delete ---
def _weinberger_intro(d):
    # RULE 17: the paper gets its setup before any of its content is used.
    # Its first use was a "Weinberger p.4" cite inside the ledger two slides
    # from here, which is a citation, not an introduction. Four parts, in
    # order: name and title, the finding, why this paper, what we teach.
    s = d.light()
    d.header(s, "open", "frame — the paper the hour is built on")
    d.title(s, "One paper designs a therapy that has to spread")
    d.rows(s, [
        ("the paper", "Weinberger, Schaffer & Arkin, “Theoretical design of "
                      "a gene therapy to prevent AIDS but not human "
                      "immunodeficiency virus type 1 infection”, "
                      "J. Virol. 77(18):10028 (2003)"),
        ("what they found", "a conditionally replicating HIV-1 vector — "
                            "crHIV-1 — spreads through the infected-cell "
                            "population on HIV-1’s own machinery, drops the "
                            "set point and holds the CD4 count up", AMBER),
        ("why this one", "it is the design in the reading where the therapy "
                         "is itself a population that has to spread, modelled "
                         "end to end with clinical parameters — so today’s "
                         "threshold is a number we compute rather than a "
                         "slogan"),
        ("what we take", "the packaging partition in segment 2, the "
                         "reproductive ratio in segment 3, and the valley in "
                         "D in segment 4"),
    ], top=1.86, label_w=2.6)
    d.foot(s, "Figure 1 is the model, Table 1 the parameters, Figure 3 the "
              "surfaces. All three go up today.")
    d.notes(s,
           "I wrote this one with Leor Weinberger and David Schaffer in "
           "2003, and I am putting it up because it is the cleanest case I "
           "know of a therapy designed as a population rather than as a "
           "molecule.\n "
           "The idea is to take HIV-1’s own machinery and parasitise it. The "
           "vector carries no polymerase and no capsid of its own. It waits "
           "inside a cell until wild-type HIV-1 arrives, borrows everything, "
           "and leaves with a packaging advantage.\n "
           "Which means the therapy only works if it SPREADS — and that is a "
           "reproductive ratio, counted from a cell that is waiting. That "
           "number is what the middle of the hour builds.\n "
           "Everything after this is from this paper unless I say "
           "otherwise. Noble and colleagues arrive at the end, for the "
           "organism-scale version of the same question.")


def _s1_frame_objects(d):
    s = d.light()
    d.header(s, "segment 1", "frame — the objects")
    d.title(s, "Four objects you have not met in this course")
    d.image_centered(s, FIG + "s25_objects.png", top=1.74, band=4.26)
    # P IS DEFINED HERE, on the slide where the ratio first appears, and in
    # words rather than only as a glyph on the figure (deck-bar B1).
    d.foot(s, "P is the packaging advantage: how many vector transcripts "
              "there are for each HIV-1 transcript in that cell's cytoplasm.")
    d.notes(s,
           "Four drawings and no algebra. None of these words has been on a "
           "slide in this course and I am not going to pretend otherwise.\n "
           "A retrovirus is diploid: it packages TWO single strands of RNA "
           "into one capsid. So which genotype a particle is was decided by "
           "a draw, and that is segment two.\n "
           "A co-infected cell is making both genomes at once. The ratio in "
           "the cytoplasm is one HIV-1 to P vector, by definition of P — I "
           "have drawn it at one to three so you can count it. P is "
           "intracellular, and the paper says plainly it is not the one you "
           "can measure.\n "
           "The vector is the short bar. The shaded end is what it kept; "
           "everything else it deleted, and what it deleted is what "
           "something else now has to supply.\n "
           "The locus is the one most of you have least chance of having "
           "met. Two copies of every gene, one from each parent. That is "
           "two draws again, and it is where the last twenty minutes live.")


def _s1_frame_words(d):
    # B3: every term of art defined BEFORE it carries an argument. cis,
    # trans and helper all carry the ledger on the next three slides.
    s = d.light()
    d.header(s, "segment 1", "frame — two words the ledger runs on")
    d.title(s, "Why a parasite deletes its proteins first")
    d.rows(s, [
        ("in cis", "a sequence that only works where it physically is — a "
                   "packaging signal is read off the very molecule that gets "
                   "packaged. Delete it and that molecule is not packaged."),
        ("in trans", "a product that works anywhere in the cell once it is "
                     "made — a protein. It does not matter which genome "
                     "encoded it."),
        ("a helper", "whatever supplies the trans products the parasite "
                     "deleted. For the vector it is HIV-1 itself.", AMBER),
    ], top=2.05, label_w=2.2)
    d.foot(s, "A parasite genome keeps what is read in cis and deletes what "
              "acts in trans, because trans can be borrowed.")
    d.notes(s,
           "This is the one piece of vocabulary the next three slides cannot "
           "be read without, so it gets its own slide.\n "
           "Cis means the sequence has to be on the molecule to do its job. "
           "A packaging signal is the example: it is read off the very RNA "
           "that gets packaged, so it cannot be supplied by anything else.\n "
           "Trans means the product diffuses and does not care where it came "
           "from. A capsid protein will package any RNA carrying the signal, "
           "including one that contributed nothing to making it.\n "
           "That asymmetry is the whole design. Keep the cis elements, "
           "delete the trans genes, and let somebody else pay for them.")


def _s1_build_ledger(d):
    # THE LEDGER IS BUILT ONE SYSTEM PER STEP, with the drawing advancing
    # beside it (lecture-design 5e: BUILD with the picture attached). The
    # panel carries the shape; this column carries the wording, which is
    # why the figure's own labels are short.
    d.derivation_fig(
        "segment 1", "build  ·  the same trade three times",
        "Three parasites made the same trade",
        [
            ("crHIV-1 keeps",
             "cis packaging elements, cargo, promoter",
             # THE PLATE NOW CARRIES THE LEGEND, so this aside does not.
             # "kept (cis)" and "deleted (trans)" are drawn on the panel and
             # persist on all three steps, and each row's helper is labeled
             # beside its arrow. This aside said the same thing at caption
             # size on the LIVE step only -- one click of a three-click
             # build, explaining shading that stays up for all three -- so
             # the two could disagree and only one of them was legible.
             # What the plate cannot hold at the type floor is the
             # provenance of the one proportion it draws to scale, so that
             # is what this slot is for (NUMBERS.md §8, QUOTED, W03 p.4).
             "the kept block is drawn to scale: ~4 kb of 10 kb, "
             "Weinberger p.4. HIV-1 supplies Gag-Pol, cleaved into the "
             "capsid"),
            ("a DI particle keeps",
             "part of the genome, in viral coat protein",
             "Huang & Baltimore's third defining property: it reproduces "
             "only where helper virus is"),
            ("a split CRISPR drive keeps",
             "the guide RNA and the homology arms",
             "Cas9 comes from the host genome or a separate construct; the "
             "smallest drive element demonstrated is a guide RNA alone"),
        ],
        [FIG + "s25_cistrans_1.png", FIG + "s25_cistrans_2.png",
         FIG + "s25_cistrans_3.png"],
        closing="So a parasite can only reproduce where its helper already "
                "is.",
        note="Three systems, sixty years apart, that arrived at the same "
             "architecture. I build them one at a time and ask what is "
             "common before I say it.\n "
             "The common thing is the closing line. And it has a "
             "consequence the whole hour turns on: a parasite that has "
             "deleted its trans genes can only reproduce where the helper "
             "already is. Its reproductive ratio is not defined in a "
             "healthy person.\n "
             "That is also the premise of move four. The vector is an "
             "obligate parasite of the very thing it was built to suppress.")


def _s1_build_1970(d):
    s = d.light()
    d.header(s, "segment 1", "build — the 1970 picture")
    d.title(s, "Drawn by hand in 1970")
    d.paper_figure(s, "huangbaltimore1970_fig1", 3.73, 1.70, 5.88, 3.70,
                   "Huang & Baltimore, Nature 226:325–327 (1970), Fig. 1",
                   "III: only defective particles, no yield.",
                   show_caption=True)
    d.notes(s,
           "Huang and Baltimore coined the term DI particle in this paper — "
           "defective interfering — and this hand-drawn figure is the whole "
           "model.\n "
           "Outcome one is standard virus alone and you get a normal crop. "
           "Outcome two is co-infection, where the defective particles "
           "replicate at the expense of the standard virus. Outcome three is "
           "defective particles alone, and it produces no yield.\n "
           "Outcome three is obligate trans-dependence drawn thirty-three "
           "years before anybody wrote the equations down. Equations four to "
           "six of today's paper ARE this picture.\n "
           "One thing to be careful about, because it is easy to run them "
           "together. Outcome three is the no-helper case — there is nothing "
           "to borrow from. It is not the therapy failing to spread in a "
           "patient who does have HIV. That is a different number and we "
           "derive it after the break.")


def _s1_release(d):
    s = d.light()
    d.header(s, "segment 1", "pose — three minutes on your own paper")
    d.title(s, "A satellite virus")
    d.rows(s, [
        ("the object", "A satellite virus encodes its own coat protein, so "
                       "it builds its own particle. It encodes no "
                       "polymerase, so it cannot copy its own genome."),
        ("question 1", "What must its helper provide?"),
        ("question 2", "What can it afford to delete, and what can it never "
                       "delete?", AMBER),
    ], top=2.10, label_w=2.2)
    d.foot(s, "Use the cis and trans test, not what you remember about "
              "viruses.")
    d.notes(s,
           "A different object from the three we just built, and on purpose: "
           "it breaks the pattern, because this one keeps a trans gene.\n "
           "The helper has to provide the polymerase. That is a protein, it "
           "acts in trans, and the satellite deleted it.\n "
           "It can delete any other trans function it can borrow. It can "
           "never delete the cis sequences — the origin or promoter its "
           "genome is copied from, and whatever its own coat recognizes — "
           "because those are read off the molecule itself.\n "
           "The point I want out of the room is that coat protein is a trans "
           "gene it chose to KEEP. So cis-versus-trans tells you what CAN be "
           "deleted, not what must be. What must be kept is only the cis "
           "part.")


def _s1_debrief(d):
    s = d.light()
    d.header(s, "segment 1", "debrief")
    d.title(s, "The test bounds what may be deleted")
    d.rows(s, [
        ("the helper supplies", "the polymerase — a protein, acting in "
                                "trans, and the satellite deleted it"),
        ("it can never delete", "the cis sequences: whatever its replication "
                                "machinery and its own coat have to read off "
                                "the molecule itself"),
        ("and the twist", "the coat is a trans gene it chose to KEEP. So the "
                          "test bounds what may be deleted; it does not say "
                          "what will be.", AMBER),
        ("why that matters today", "every trans gene the vector keeps is one "
                                   "it does not have to borrow — and one "
                                   "more thing its helper's presence stops "
                                   "controlling"),
    ], top=1.94, label_w=3.0)
    d.notes(s,
           "I take answers first and then put this up, so the people who did "
           "not speak also find out.\n "
           "The polymerase is the answer to the first question and most of "
           "the room will get it.\n "
           "The second is the one worth the time. The satellite keeps a "
           "trans gene — its coat — and it is still a satellite. So the "
           "cis-trans test is a bound on what you MAY delete, not a "
           "prediction of what any particular parasite did delete.\n "
           "And that last row is where segment four goes. The more trans "
           "functions you borrow, the more completely your fate is tied to "
           "the helper's. Today's vector borrows all of them.")


# ------------------------------------- segment 2 · two draws from an urn ---
def _s2_frame(d):
    s = d.light()
    d.header(s, "segment 2", "frame — the promise from session 2")
    d.title(s, "This time the engineer sets the probability")
    d.rows(s, [
        ("what is drawn", "session 2: five plasmid copies, each into one of "
                          "two daughters   ·   today: two RNA strands, each "
                          "HIV-1 or vector"),
        ("how many draws", "session 2: n = 5   ·   today: n = 2. Exactly "
                           "two, because the capsid holds two"),
        ("the probability", "session 2: ½, fixed by physics   ·   today: "
                            "P/(1+P), and the ENGINEER sets it", AMBER),
        ("the question", "session 2 asked about loss — does a daughter get "
                         "none?   ·   today asks about composition — which "
                         "genotype is this particle?"),
    ], top=1.96, label_w=2.7)
    d.notes(s,
           "Session 2 promised you this calculation and this is it. Two "
           "binomials over the same distribution, and the differences are "
           "the lesson.\n "
           "The row that matters is the third. In session 2 the probability "
           "was one half and nothing you could do changed it. Today the "
           "probability is set by how hard your vector competes for "
           "packaging, and that is a design variable. P is the only tunable "
           "thing in the hour that enters a probability.\n "
           "And the question changed. Loss versus composition. Same algebra, "
           "different thing being asked of it.")


def _s2_build(d):
    # SEVEN STEPS, ONE MOVE EACH, with the urn filling beside them. The
    # derivative gets its own step rather than riding in a parenthesis
    # beside the result it produces, because it is the only move in this
    # run a student can get wrong.
    d.derivation_fig(
        "segment 2", "build  ·  two draws from an urn",
        "Two draws decide what a particle is",
        [
            ("first, what the binomial needs",
             "equal packaging, and two independent draws",
             "Weinberger asserts equal packaging. Nothing in the reading "
             "set tests either assumption — this is a Limits row"),
            ("q, the chance one strand is vector",
             "q = P/(1+P),   so   1 − q = 1/(1+P)",
             "straight off the cell's pool, 1 HIV-1 to P vector"),
            ("the capsid takes two",
             "two draws, three outcomes",
             "HIV·HIV, one of each, vector·vector"),
            ("so the three probabilities are",
             "(1−q)²,   2q(1−q),   q²",
             "the 2 counts both orders of the heterozygote"),
            ("and they must sum to one",
             "(1−q)² + 2q(1−q) + q² = (q + 1 − q)² = 1",
             "shown, not asserted — if they did not sum to one the pool "
             "would not be a probability"),
            ("in P, and Weinberger prints the ratio",
             "1/(1+P)²,   2P/(1+P)²,   P²/(1+P)²",
             "Weinberger prints 1 : 2P : P², the same thing with the "
             "(1+P)² dropped. Say which form you are using"),
            ("where is the heterozygote worst",
             "d/dP [2P/(1+P)²] = (2 − 2P)/(1+P)³",
             "zero at P = 1, positive below, negative above — so a "
             "maximum, and the value there is exactly one half"),
        ],
        # urn_5 prints the P-forms, so it arrives on the step that writes
        # them. Step 5 is still in q and keeps urn_4's three outcomes.
        # Step 7 is the derivative and wants a P = 1 plate; until one
        # exists it holds urn_5, and the note says out loud that the
        # picture is drawn at P = 3 while the result is about P = 1.
        [FIG + "s25_urn_1.png", FIG + "s25_urn_2.png", FIG + "s25_urn_3.png",
         FIG + "s25_urn_4.png", None, FIG + "s25_urn_5.png", None],
        closing="A balanced cell is the WORST case: half of what it makes "
                "is one of each.",
        note="One genuine move a slide. The assumption goes first, because a "
             "binomial that has not been licensed is just a formula.\n "
             "The derivative gets its own click. Two P over (1+P) squared "
             "differentiates to two times (1+P) squared minus 2P times two "
             "times (1+P), over (1+P) to the fourth — cancel one (1+P) and "
             "the numerator is 2 + 2P − 4P, which is 2 − 2P. Zero at P = 1, "
             "positive below, negative above. So it is a maximum, and the "
             "value there is two over four, exactly one half.\n "
             "The last line is the one to hold on to. Everybody's intuition "
             "says a balanced cell is the fair case. It is the worst one.\n "
             "And say which form you are using. The normalized "
             "probabilities and Weinberger's printed ratio differ by (1+P) "
             "squared, and that is the commonest way this gets got wrong.")


def _s2_strikeout(d):
    s = d.light()
    d.header(s, "segment 2", "build — what the model does with the middle one")
    d.title(s, "A rounding strikes the heterozygotes out")
    # EXPLICIT PLACEMENT, not image_centered: this slide carries text beside
    # the figure, and image_centered centers on the whole slide width.
    #
    # THE BOX IS derivation_fig'S BOX, 5.4 x 4.95, and that is the whole
    # point of the number. s25_urn_1..5 are placed by `derivation_fig` at
    # that size -- scale 1.135 against the 4.756 x 4.300 in PNG -- and this
    # slide used to hold the same PNG at 4.98 x 4.52, scale 1.047. Same
    # picture, adjacent slide, same role, projected 8.4% narrower: the urn
    # shrank on the click that strikes the heterozygotes out. Nothing
    # complained, because 20pt type at 1.047 is still 20.9pt and the floor
    # was never what was at risk. `derivation_fig` exists so the drawing
    # grows with the algebra, and a picture that RESIZES between stages
    # breaks that while staying legible. The text column moves right to
    # clear the wider image rather than the image staying small to suit it.
    d.image(s, FIG + "s25_urn_6.png", M, 1.72, 5.40, 4.95)
    d.rows(s, [
        ("An et al. 1999 measured", "a PARTIAL preintegration, postfusion "
                                    "block — heterozygous virions infect and "
                                    "are internalized, then mostly stall"),
        ("Weinberger rounds it to zero",
         "so the INFECTIOUS output is 1 : P², HIV-1 first, and "
         "2P/(1+P)² of everything made is discarded", AMBER),
    ], top=1.90, bottom=5.70, left=6.26, side=False)
    # The sources drop below the image, which now reaches 6.64 rather than
    # 6.23. They run full width from the left margin, so there is nowhere
    # beside the picture for them to go.
    d.sources(s, [("the partial block",
                   "An et al., J. Virol. 73:7671 (1999)"),
                  ("the rounding to zero",
                   "Weinberger, Schaffer & Arkin 2003, p.10031")], y=6.70)
    d.notes(s,
           "This is a modeling decision and it is what I want you to take "
           "from this slide, not the conclusion it licenses.\n "
           "An et al. report a partial block — the particles get in and then "
           "mostly fail before integrating. Weinberger rounds that to zero "
           "strikes the heterozygotes out of the infectious output "
           "altogether.\n "
           "The rounding is probably fine and it is not free. If "
           "heterozygotes were infectious the ratio would be 1 to P times "
           "P plus 2 instead of 1 to P squared — a two percent correction at "
           "P = 100, and a factor of three at P = 1. So it matters most "
           "exactly where the threshold sits, which is the uncomfortable "
           "version. It is on the limits slide at the end.\n "
           "The supporting citation is also thin: one in vitro paper, and a "
           "two-page committee review cited for mouse results. I have not "
           "been able to check the second one.")


def _s2_infectious(d):
    # THE QUANTITY THE OBJECTIVES SLIDE PROMISED, finally written down.
    # "the partition" on the goals slide asks what fraction of what a cell
    # releases can infect anything, the strikeout slide gives the DISCARDED
    # fraction, and the debrief plots the surviving one and calls it "the
    # infectious fraction" -- but (1+P²)/(1+P)² appeared nowhere in the deck,
    # and it is what the autograded partition item asks for. Two moves,
    # because the second one is where the 2P disappears.
    d.derivation(
        None, "segment 2", "build  ·  what survives the rounding",
        "The infectious fraction is one minus the middle one",
        [
            ("all of it, less the middle",
             "infectious fraction = 1 − 2P/(1+P)²",
             "the two homozygous classes are all that is left once the "
             "middle one is struck out"),
            ("over the one denominator",
             "= [(1+P)² − 2P] / (1+P)²",
             "(1+P)² = 1 + 2P + P², so the 2P goes. At P = 3: 10/16 = "
             "0.6250, the number under the urn"),
        ],
        closing="infectious fraction = (1 + P²)/(1 + P)²",
        note="This is the answer to the first of the three questions I put "
             "up at the start, so it gets written down rather than left on "
             "a plot.\n "
             "Start from everything the cell makes and take away the class "
             "the rounding just killed. What is left is the two homozygous "
             "classes — all vector, or all virus.\n "
             "The second line is the only algebra. Expand the square on top "
             "and the two P cancels the two P, which is why the answer is "
             "as clean as it is: one plus P squared over one plus P, "
             "squared.\n "
             "Check it where we already know the answer. At P equals one "
             "that is two over four, a half — the number the vote lands "
             "on. At P equals three it is ten over sixteen, which is the "
             "0.6250 printed under the urn in the build.\n "
             "And notice what it does NOT contain. No burst size, no rates, "
             "nothing but the packaging advantage. The partition is a "
             "property of one cell’s packaging and nothing else.")


def _s2_release(d):
    s = d.light()
    d.header(s, "segment 2", "pose — three minutes on your own paper, then vote")
    d.title(s, "A DI particle with no packaging advantage")
    d.rows(s, [
        ("the object", "a defective interfering particle that competes for "
                       "packaging no better than the virus it came from, so "
                       "P = 1, in a cell co-infected one to one"),
        ("the question", "Of ALL the virions that cell releases, what "
                         "fraction carry TWO copies of the defective "
                         "genome?", AMBER),
        ("your options", "a quarter   ·   a half   ·   three quarters   ·   "
                         "it depends on the burst size"),
    ], top=2.10, label_w=2.2)
    d.foot(s, "Eyes down for the first vote. Then argue with the person next "
              "to you and vote again.")
    d.notes(s,
           "A quarter. At P = 1, q is one half, so the three probabilities "
           "are a quarter, a half and a quarter — the 1 : 2 : 1 ratio.\n "
           "The stem says TWO copies on purpose. Three quarters of the "
           "output carries at LEAST one defective strand, and half of the "
           "INFECTIOUS output is defective once the heterozygotes are struck "
           "out. All three numbers are defensible answers to differently "
           "worded questions, which is why I pinned the wording.\n "
           "The burst-size option is the one to take seriously when I poll. "
           "It is wrong here — the FRACTIONS do not depend on the burst size "
           "— but the burst size is about to become the whole problem in "
           "segment four, so anybody who picked it is early rather than "
           "wrong, and I say that.")


def _s2_debrief(d):
    s = d.light()
    d.header(s, "segment 2", "debrief")
    d.title(s, "The balanced cell is the worst one")
    d.image_centered(s, FIG + "s25_genotypes.png", top=1.76, band=4.30)
    d.foot(s, "At P = 1: a quarter, a half, a quarter. Half of everything "
              "made is a heterozygote, and half of what is released can "
              "infect.")
    d.notes(s,
           "The left panel is the answer. At P = 1 the three curves are at a "
           "quarter, a half and a quarter — read it off the dot.\n "
           "The right panel is the thing worth the extra thirty seconds. The "
           "waste PEAKS at P = 1 and the infectious fraction BOTTOMS there, "
           "both at exactly one half. Walk away from P = 1 in either "
           "direction and the cell wastes less — including downward, which "
           "surprises people, because a cell making mostly virus and almost "
           "no vector also makes very few of one of each.\n "
           "So the infectious fraction is not monotone in P. It falls to a "
           "half and then rises. If you are checking your own work with a "
           "coarse grid that starts at P = 1 you will miss that.")


# ------------------------------------ segment 3 · whose reproductive ratio ---
def _s3_frame_count(d):
    # R0 HAS ZERO PRIOR OCCURRENCES IN THIS COURSE, so it is defined as a
    # COUNT before any algebra touches it (deck-bar B1, B3).
    s = d.light()
    d.header(s, "segment 3", "frame — a number this course has never used")
    d.title(s, "R_{0} is a count")
    d.rows(s, [
        ("R_{0}", "the number of new infections produced by ONE infected cell, "
               "when almost every other cell is still uninfected"),
        ("above one", "each infection more than replaces itself, so the "
                      "infection establishes"),
        ("below one", "each infection fails to replace itself, so it dies "
                      "out — whatever the initial dose was"),
        ("the crossing", "a transcritical bifurcation: two fixed points "
                         "swap stability as a parameter passes through. New "
                         "name, machinery you have had since session 9.",
         AMBER),
    ], top=1.96, label_w=2.0)
    d.foot(s, "Everything today hangs on a count, and on WHICH cell you "
              "start counting from.")
    d.notes(s,
           "A count, in words, before any algebra. This is the one genuinely "
           "new idea in the segment and it is not a hard one.\n "
           "One infected cell, dropped into a population that is almost all "
           "uninfected. How many new infected cells does it leave behind "
           "before it dies? Above one and the thing takes off; below one and "
           "it dies out no matter how much you injected.\n "
           "Transcritical is the only new word and it is cheap: fixed "
           "points, eigenvalues and bifurcations are all in hand since "
           "sessions 8 and 9. Two fixed points exchange stability as they "
           "pass through each other.\n "
           "The last line is the one I will come back to four times. Which "
           "cell you count FROM is the whole content of the second "
           "derivation.")


def _s3_frame_clinical(d):
    # THE TWO NUMBERS MOVE 3 IS ABOUT GO ON THE PAGE, in body type. They were
    # in the speaker note alone, so the room read the main panel's own axis as
    # "the count" -- and the whole claim lives in a 2.5cm inset with no axis
    # label and a y-scale about 25x the main panel's, with nothing on the page
    # saying so (deck-bar B1, F5: the note is not the slide). The figure moves
    # right to make the column, and the old foot became a row because a foot
    # renders at caption size, which is below the content floor.
    s = d.light()
    d.header(s, "segment 3", "frame — what the therapy does to a patient")
    d.title(s, "The count is restored by making a new kind of cell")
    d.rows(s, [
        ("uninfected T alone", "settles near 300/µl — far below the healthy "
                               "800, and never restored"),
        ("T + I_{T} together", "climbs to about 1,500/µl — the count is "
                               "restored by CONVERTING cells into a new "
                               "class", AMBER),
        ("an I_{T} cell", "makes no virus, and dies at the UNINFECTED rate d"),
        ("the inset carries the claim", "a y-axis 25× the main panel's"),
    ], top=1.78, bottom=6.50, side=False, right=5.60)
    d.paper_figure(s, "weinberger2003_fig2c", 5.80, 1.70, 6.80, 3.90,
                   "Weinberger, Schaffer & Arkin, J. Virol. 77:10028 (2003), "
                   "Fig.\u00a02c",
                   "Cells, not virions. Inset: T, I_{T}, T_{TOT} = their "
                   "sum.",
                   show_caption=True)
    d.notes(s,
           "Before any algebra, what the therapy does to a patient, because "
           "it decides which cell we count from.\n "
           "The two numbers are on the page and they are the whole frame. "
           "Uninfected T cells alone stay in the AIDS regime. T plus I_T "
           "climbs to about fifteen hundred. The count comes back by "
           "converting cells into a new class, not by protecting the old "
           "one.\n "
           "The heights in the main panel will mislead them if I let them. "
           "The inset runs on its own scale, about twenty-five times the "
           "main panel's, so the recovery is read off the inset and the "
           "numbers are what to trust.\n "
           "An I_T cell has the vector integrated, makes no virus, and dies "
           "at d rather than delta. A healthy cell carrying a passenger.\n "
           "One number here I will not use. The pretherapy infected level "
           "reads about 58 per microlitre and Table 1's steady state is "
           "21.4. The simulations carry an eclipse delay whose equations are "
           "in a supplement we do not have, so that gap is unresolved and I "
           "am not putting the two numbers side by side as if they agreed.")


def _s3_frame_model(d):
    # THE SIX EQUATIONS, BEFORE ANYTHING CITES THEM. Both derivations in this
    # segment argue from equation [1] and the vector's output comes out of [6],
    # and `weinberger2003_fig1` used to appear for the first time in segment 4
    # -- after the derivations were over. deck-bar F1 and B4: the system a
    # slide argues about is drawn on or before that slide, and a paper is
    # introduced before its results are quoted. The panel goes up twice; this
    # is the reference showing, and segment 4's frame is the one knob on two
    # arrows. T, I and V are defined here because this is where they first
    # appear, and the star convention with them -- I* lands on the back-solve
    # run and T*, V* on the second derivation.
    s = d.light()
    d.header(s, "segment 3", "frame — the six equations")
    d.title(s, "The whole model is six equations")
    d.rows(s, [
        ("[1]–[3]", "the Basic Model: T uninfected cells, I HIV-infected, "
                    "V free virions"),
        ("[4]–[6]", "the therapy: I_{T} has the vector, I_{D} has both, "
                    "V_{T} free vector"),
        ("a star", "the steady-state value: T*, I*, V*", AMBER),
    ], top=1.80, bottom=6.40, side=False, right=5.00)
    d.paper_figure(s, "weinberger2003_fig1", 5.40, 1.70, 7.20, 4.00,
                   "Weinberger, Schaffer & Arkin, J. Virol. 77:10028 (2003), "
                   "Fig. 1",
                   "Red: [1]–[3]. Blue: [4]–[6].",
                   show_caption=True)
    d.notes(s,
           "Six equations, and everything in the next half hour is read off "
           "them, so they go up before I cite a number in brackets.\n "
           "The first three are the Basic Model and they are standard HIV "
           "dynamics: uninfected cells T born at lambda and dying at d, "
           "cells I infected by HIV alone, free virions V cleared at c.\n "
           "The second three are the therapy. I_T carries the vector and "
           "makes nothing. I_D carries both and makes both. V_T is free "
           "vector. Those are the three compartments the second derivation "
           "linearises in.\n "
           "And the notation I will use without comment from here: a star "
           "means that variable at steady state. T star, I star, V star.\n "
           "I come back to this panel in the next segment for a different "
           "reason — to count where D appears.")


def _s3_build_chain(d):
    d.derivation_fig(
        "segment 3", "build  ·  the infection chain",
        "Count the chain one link at a time",
        [
            ("start from one infected cell",
             "it lives 1/δ = 1.43 days",
             "δ = 0.7 per day is a RATE; the lifetime is its reciprocal"),
            ("over that life it emits",
             "n · δ · (1/δ) = n = 200 virions",
             "n is the burst size: virions released per infected cell"),
            ("each virion survives",
             "1/c = 0.033 days,   c = 30 per day",
             "c is the clearance rate of free virions"),
            ("and while it survives it infects at",
             "k · T,   with T = λ/d = 1550 cells per µl",
             "λ is the birth rate of uninfected T cells, d their death "
             "rate, k the infection rate per virion"),
        ],
        [FIG + "s25_chain_1.png", FIG + "s25_chain_2.png",
         FIG + "s25_chain_3.png", FIG + "s25_chain_4.png"],
        closing="R_{0} = n · k · (λ/d) / c = λkn/(cd) = 1.9375",
        note="One link a click, and every symbol is defined on the click "
             "that produces it.\n "
             "The distinction I am careful about is delta. Delta is a death "
             "RATE, 0.7 per day, so the lifetime is one over delta, about a "
             "day and a half. Same for c: thirty per day, so a virion lasts "
             "about forty-eight minutes.\n "
             "Notice the burst size falls out clean. The cell emits at rate "
             "n delta for a time one over delta, so the deltas cancel and it "
             "emits exactly n. That cancelation is going to happen again, "
             "in a more surprising place, in about ten minutes.\n "
             "Equivalently: the virus-free steady state is T = lambda over "
             "d, the infected one is T star = c over k n, and R0 is the "
             "ratio of the two. Same number, two routes.")


def _s3_build_printed(d):
    s = d.light()
    d.header(s, "segment 3", "build — the paper's printed form")
    d.title(s, "The printed denominator cannot be right")
    d.rows(s, [
        # BOTH DENOMINATORS PARENTHESISED. "lkn / cd" reads as (lkn/c)*d,
        # which is the one misreading this slide cannot afford: the slide's
        # whole subject is which symbol sits in the denominator.
        ("the paper prints", "R_{0} = λkn/(cδ)"),
        ("we just derived", "R_{0} = λkn/(cd)   —   the d arrives through the "
                            "virus-free steady state T = λ/d"),
        # One case per line. Run into one paragraph, the two arithmetics
        # read as a single sum and the room cannot see which is which.
        ("put Table 1 in", "with d:   31 × 1.875e-4 × 200 / (30 × 0.02) = "
                           "1.9375\n"
                           "with δ:   the same over (30 × 0.70) = 0.055",
         AMBER),
        ("so", "0.055 is a virus that cannot sustain an infection, in a "
               "patient who demonstrably has one. Every figure in the paper "
               "would be impossible."),
    ], top=1.90, label_w=2.6)
    d.foot(s, "Dimensionally both are fine, which is why it survived review. "
              "Only the arithmetic catches it.")
    d.notes(s,
           "This is my paper and it has a transcription slip in it. We are "
           "going to find it the way you find one in anybody's paper.\n "
           "I ask the room for the number with delta before I show it. "
           "0.055. Then: can a virus with R0 of 0.055 give somebody AIDS? "
           "No. It dies out.\n "
           "The derivation is what makes this evidence rather than "
           "numerology, and that is why we did it first. The virus-free "
           "steady state of equation one IS lambda over d, so d is what "
           "belongs in that denominator.\n "
           "And the lesson that outlives the slip: dimensional analysis "
           "passes this. Delta and d are both per-day rates. Only putting "
           "numbers in catches it.")


def _s3_build_backsolve(d):
    # THE UNIT CONVERSION IS A LINE OF THE DERIVATION, not an aside beside
    # it. Leave it out and I* comes back a thousandfold wrong -- 21,430
    # infected cells per microlitre in a patient whose whole T0 is 800.
    d.derivation(
        None, "segment 3", "build  ·  where λ and k came from",
        "Two of those numbers were never measured",
        [
            ("first, the units",
             "V_{0} = 10⁵ virions/ml = 10⁵/10³ = 100 virions/µl",
             "Table 1 is per µl throughout EXCEPT V_{0}, printed per ml"),
            ("I* at steady state",
             "I* = cV_{0}/(nδ) = 30 × 100/(200 × 0.7) = 21.43 cells/µl",
             "without the conversion: 21,430, where T_{0} = 800 cells/µl"),
            ("now back out k from T_{0}",
             "k = c/(nT_{0}) = 30/(200 × 800) = 1.875e-4 µl/virion",
             "exactly what Table 1 prints, marked “no data”"),
            ("and λ from the cell balance",
             "λ = dT_{0} + δI* = 16 + 15 = 31.0 cells/µl/day",
             "0.02×800 + 0.7×21.43; Table 1 cites λ to the literature"),
        ],
        closing="λ and k were fitted so the model sits at "
                "T_{0} = 800 cells/µl, V_{0} = 10⁵ virions/ml.",
        note="The first line is a line of the derivation and not an aside. "
             "V zero is the only concentration in the table printed per "
             "millilitre, and every number after it depends on noticing "
             "that.\n "
             "What the run shows is that two of the eleven rows of Table 1 "
             "are not measurements. The paper says so in one line of body "
             "text — lambda and k were calculated by steady-state analysis — "
             "while the table gives lambda a literature citation and marks k "
             "'no data'. Both of those readings are half true and together "
             "they are misleading.\n "
             "I am not scolding anybody. This is extremely common and it is "
             "worth being able to spot in a table you are reading at two in "
             "the morning.")


def _s3_build_construction(d):
    s = d.light()
    d.header(s, "segment 3", "build — what that costs the result")
    d.title(s, "R_{0} = 1.9375 is true by construction")
    d.rows(s, [
        ("rewrite it", "R_{0} = (λ/d)/T_{0} = 1550/800 = 1.9375 = 31/16"),
        ("read that again", "the healthy CD4 count divided by the "
                            "set-point CD4 count — and λ and k were CHOSEN "
                            "so those two numbers come out right", AMBER),
        ("so it is", "a genuinely nice result AND a restatement of two "
                     "inputs. Both are true and the slide says both."),
        ("what it is not", "an independent prediction. The model cannot be "
                           "wrong about the set point, because the set "
                           "point was used to build it."),
    ], top=1.94, label_w=2.6)
    d.foot(s, "λ/d = 1550 against Fig. 2c's inset is a consistency check, "
              "not evidence — λ/d contains no c, δ, k or n.")
    d.notes(s,
           "This is the second of the two honesties and it is the subtler "
           "one.\n "
           "R0 for this patient is the ratio of the healthy T cell count to "
           "the set-point count. That is a nice way to think about R0 and I "
           "would teach it. It is also a tautology here, because the two "
           "parameters that make it come out were back-solved from exactly "
           "those two observables.\n "
           "The foot matters. People reach for lambda over d equals 1550 "
           "against the figure's fifteen hundred as proof that d is the "
           "right denominator. It is not. Lambda over d contains no c, no "
           "delta, no k and no n, so it cannot distinguish the two "
           "denominators at all. It is a consistency check and I label it "
           "as one.")


def _s3_build_names(d):
    # R0_T IS NAMED BEFORE IT IS USED. Pages 1-37 of this deck carried ZERO
    # prior occurrences of the symbol, and its first appearance was the
    # degeneracy claim on the equilibrium slide -- a claim ABOUT a quantity
    # nothing had defined, with the paper's own definition (NUMBERS.md 5a) on
    # no slide at all and the nearest thing to it seven slides later, as a
    # negative. deck-bar B1 and F2, and T73 is autograded on PS9 and on the
    # final. So R0_T gets the row R0 got, in the same words and the same
    # place: a count, and WHICH cell it counts from.
    #
    # D IS DEFINED HERE, in body type, because this is the first slide in the
    # segment whose own text uses it. It was settled only in a step aside --
    # caption size, italic, gray, live for one click -- and then re-argued in
    # segment 4's frame, three derivations after the room first read it off
    # an axis.
    s = d.light()
    d.header(s, "segment 3", "build — what the second count counts")
    d.title(s, "R_{0}^{T} counts from a cell that is waiting")
    d.rows(s, [
        ("today's two knobs", "P, the packaging advantage · D, the antiviral "
                              "effect — HIV-1 production REMAINING, so "
                              "D = 1 is NO inhibition"),
        ("the therapy's state variables", "I_{T} cells carrying the vector "
                                          "and making nothing · I_{D} cells "
                                          "dually infected and making both · "
                                          "V_{T} free vector virions"),
        ("R_{0}^{T}", "the number of new crHIV-1 infections produced by ONE "
                   "I_{T} cell, with HIV-1 already at its own steady state",
         AMBER),
    ], top=1.94, label_w=3.0)
    d.foot(s, "R_{0} counts from an infected cell. R_{0}^{T} counts from a cell "
              "that carries the vector and is waiting for the virus.")
    d.notes(s,
           "Every symbol here is new, so I name all three before I use any "
           "of them. I_T carries the vector and makes nothing. I_D has both "
           "and makes both. V_T is free vector.\n "
           "And the quantity the rest of the segment derives. R0_T is the "
           "same kind of object as R0 — a count of new infections from one "
           "cell — with two changes. The infections counted are vector "
           "infections, and the cell they start from is an I_T cell.\n "
           "That second change is the whole content of what follows. The "
           "therapy's susceptible pool is not uninfected cells. It is cells "
           "that already carry the vector and have nothing to replicate "
           "it.\n "
           "D is on the slide in words because the paper's own prose defines "
           "it the other way round. D is the fraction of HIV-1 production "
           "that REMAINS, so D = 1 is no drug at all.")


def _s3_build_equilibrium(d):
    # T* = T0 AND V* = V0, SAID ON THE SLIDE. The deck runs T0/V0 through the
    # back-solve, switches to T*/V* for the whole second derivation, and goes
    # back to T0/V0 in segment 4 -- and never once said the two are the same
    # numbers. deck-bar B2, on the central quantities of the derivation.
    s = d.light()
    d.header(s, "segment 3", "build — which equilibrium")
    d.title(s, "Linearise at the infection")
    d.rows(s, [
        ("if we linearise at V* = 0", "an I_{T} cell can never be "
                                      "superinfected, I_{D} is never "
                                      "populated, and R_{0}^{T} ≡ 0 for EVERY "
                                      "P and every D — degenerate, not "
                                      "merely different", AMBER),
        ("so we stand here", "T* = T_{0} = 800 cells/µl   ·   V* = V_{0} = 100 "
                             "virions/µl   ·   I* = 21.43 cells/µl"),
        ("and that is the reason", "the index case is an I_{T} cell. The "
                                   "vector is an obligate parasite of an "
                                   "established infection — it is forced, "
                                   "not stipulated."),
    ], top=1.96, label_w=3.0)
    d.foot(s, "The starred values ARE Table 1's observables: the back-solve "
              "put the steady state on T_{0} and V_{0} by construction.")
    d.notes(s,
           "The choice that decides the whole derivation. If we linearise "
           "where there is no virus, the answer is not a different number — "
           "it is identically zero, for every setting of both knobs. There "
           "is nothing for the vector to borrow.\n "
           "That is segment one coming back. A parasite that deleted its "
           "trans genes has no reproductive ratio in a healthy person.\n "
           "Notation, said once. T star and V star are the steady-state "
           "values, and at these parameters they ARE T zero and V zero — "
           "eight hundred and a hundred — because that is what the "
           "back-solve was for. Same numbers, two names.\n "
           "So the index case being an I_T cell is forced by the algebra "
           "rather than chosen by the authors, and that is worth more than "
           "a definition the room has to take on trust.")


def _s3_build_waiting(d):
    # THE FIRST cancelATION, BUILT. NUMBERS.md 18.2 calls the two
    # cancellations THE derivation and DESIGN 6 marks them never-cut, and this
    # one was two asserted lines: the ratio appeared, and the next step
    # announced it equals 1 - 1/R0 with "from kV*T* = l - dT* in equation [1]"
    # as its aside. Two things were missing and both are steps here.
    #
    # WHY THE RATIO IS A PROBABILITY AT ALL. It is a competing risk: the
    # superinfection hazard kV* against the death hazard d, and the chance
    # superinfection comes first is its share of the total. For a room of
    # biologists and chemists this is the step most likely to lose them, and
    # it is step one of the segment's central derivation.
    #
    # THE ALGEBRA FROM THE HINT TO THE RESULT. From kV*T* = l - dT* you need
    # d + kV* = l/T* before anything collapses, and that line was on no
    # slide. The second cancelation was built properly -- T* = c/(kn) is
    # printed beside it -- which made the asymmetry worse, not better.
    #
    # THE PICTURE IS ATTACHED, which is what this run was missing. DESIGN.md
    # section 7 build need 5 asks for the R0_T generation chain built beside
    # the algebra with both cancellations marked on the drawing WHERE THEY
    # HAPPEN, and `figures/s25_populations.py` now builds it as
    # s25_rtchain_1..6 on the same fixed canvas as the urn and the first
    # chain. Until this call the six panels were unplaced, so every build
    # reported them `placement unknown` and NOTHING checked their type floor
    # (deck-bar D5a item 6). They are placed in two runs of three.
    #
    # WHY IT IS WORTH THE SWITCH, beyond placing the panels. A critic reading
    # this deck front to back as a student reported slides 41-46 as the one
    # place it finished a build LESS confident than it started -- "I reached
    # slide 42 holding a formula I could not reconstruct" -- because four
    # consecutive slides of bare algebra is where the competing-risk argument
    # lives. deck-bar C4: an argument that can be made graphically is made
    # graphically.
    #
    # STAGE-TO-STEP, and the correspondence is exact rather than decorative.
    # Stage 1 is the waiting I_T cell with no formula on it at all; stage 2
    # opens the two exits, kV* and `d (dies first)`, which is step 2's
    # competing risk drawn; stage 3 completes the SAME mark in place to
    # kV*/(d + kV*) = 1 - 1/R0 and brings in the I_D cell, which is step 3's
    # result. The mark does not move between stages 2 and 3, it finishes --
    # so the picture says the cancelation happened on that arrow.
    #
    # Two runs rather than one six-step run. `derivation_fig` reserves 5.4in
    # for the picture and gives the step stack 1.62 to 5.40 with a closing
    # box, which three steps fit and six do not. It also shows an aside only
    # on the step that is LIVE -- see the note on _s3_build_factors -- so a
    # long run would carry its early asides on one click each.
    d.derivation_fig(
        "segment 3", "build  ·  the waiting cell's first factor",
        "Where 1 − 1/R_{0} comes from",
        [
            ("an I_{T} cell is waiting",
             "kV*/(d + kV*)",
             "superinfected before it dies of old age, or never"),
            ("two hazards, one winner",
             "the chance kV* fires before d does",
             "competing risks: each hazard's share of kV* + d"),
            ("so put equation [1] in",
             "d + kV* = λ/T*, so the ratio is 1 − dT*/λ",
             "kV*T* = λ − dT* at steady state, divided by T*"),
        ],
        [FIG + "s25_rtchain_1.png", FIG + "s25_rtchain_2.png",
         FIG + "s25_rtchain_3.png"],
        closing="kV*/(d + kV*) = 1 − 1/R_{0} = 15/31",
        note="The first factor, and I build it rather than assert it.\n "
             "A cell with the vector in it is sitting there with two clocks "
             "running. One is superinfection, at rate k V star. The other is "
             "ordinary death, at rate d. Whichever fires first decides what "
             "that cell was for.\n "
             "That is a competing risk, and the chance superinfection wins "
             "is its share of the total rate: k V star over k V star plus d. "
             "A ratio of rates is a probability when the rates are the only "
             "two ways out.\n "
             "Now the algebra, and the line that does it is d plus k V star "
             "equals lambda over T star. That comes from equation one at "
             "steady state — k V star T star is lambda minus d T star — "
             "divided through by T star. Put it in and the ratio is one "
             "minus d T star over lambda.\n "
             "And d T star over lambda is one over R zero, because R zero is "
             "lambda over d divided by T star. Fifteen over thirty-one for "
             "this patient.")


def _s3_build_factors(d):
    # THE PRODUCT IS WRITTEN OUT. The three factors used to arrive one per
    # step and the closing box printed the finished result, so the spine of
    # the generation argument -- that R0_T is these three MULTIPLIED -- was
    # never on the slide: no times sign anywhere in the run. The last step is
    # now the product itself, and the closing box is the same product with
    # both cancellations substituted, which is where the n and the delta
    # prime go.
    #
    # AND THE ORDER IS FIXED. The I_D output P^2*D*n used to be asserted a
    # slide before the step that produces it (production P^2*D*n*delta'
    # against a lifetime 1/delta'), which arrived on the delta-prime slide
    # afterwards. It is this step's own aside now.
    #
    # STAGES 4-6 OF THE SAME CHAIN, continuing _s3_build_waiting's 1-3, so
    # the drawing the room has been watching since "an I_T cell is waiting"
    # finishes here rather than restarting. Stage 4 puts the burst on an
    # arrow off the I_D CELL and marks it P^2*D*n -- which is step 1 -- so
    # the output is attached to the cell that makes it instead of floating
    # beside the algebra. Stage 5 marks kT*/c = 1/n on the LAST arrow, the
    # second cancelation at the place it happens, which is step 2. Stage 6
    # and no stage before it prints R0_T = P^2*D*(1 - 1/R0) at the foot, so
    # the room never sees the answer before the product that makes it --
    # which is the whole reason `derivation_fig` exists.
    #
    # ONE THING THIS COSTS, AND IT IS A THEME.PY QUESTION RATHER THAN A DECK
    # ONE. `derivation` renders an aside on every step once the pitch clears
    # 0.86in; `derivation_fig` renders it only on the step that is LIVE. So
    # every aside here still reaches the room, each on its own click, but the
    # LAST slide of each run no longer carries the earlier ones. The aside
    # that matters for provenance is step 1's, "production P^2*D*n*delta'
    # over an I_D lifetime 1/delta'", and _s3_build_deltaprime, two slides
    # later, is four rows about exactly that cancelation, so nothing is
    # lost from the deck. Raised with the theme owner rather
    # than worked around here: theme.py is not this file's to change.
    d.derivation_fig(
        "segment 3", "build  ·  three factors and two cancellations",
        "R_{0}^{T} one generation at a time",
        [
            ("that I_{D} cell then emits",
             "P² · D · n vector virions",
             "production P²Dnδ′ over an I_{D} lifetime 1/δ′"),
            ("new I_{T} cells per virion",
             "kT*/c = 1/n  exactly, since T* = c/(kn)",
             "the burst size cancels — R_{0}^{T} contains NO n"),
            ("so multiply the three",
             "R_{0}^{T} = kV*/(d + kV*) × P²Dn × kT*/c",
             "one generation: a waiting cell, I_{D}, virions, new I_{T}"),
        ],
        [FIG + "s25_rtchain_4.png", FIG + "s25_rtchain_5.png",
         FIG + "s25_rtchain_6.png"],
        closing="R_{0}^{T} = (1 − 1/R_{0}) × P²Dn × 1/n = P² · D · (1 − 1/R_{0})",
        note="Three factors, multiplied, and two exact cancellations doing "
             "all the work.\n "
             "The middle factor is the I_D cell's output over its whole "
             "life: it produces at P squared D n delta prime and it lives "
             "one over delta prime, so delta prime is already gone before we "
             "get to the threshold.\n "
             "The second cancelation is the one that should surprise you. k "
             "T star over c is exactly one over n, because T star IS c over "
             "k n. So the P squared D n coming out of the cell meets a one "
             "over n going in, and the burst size disappears completely.\n "
             "Hold on to that, because in twenty minutes the burst size is "
             "going to be the entire problem. It is absent from the "
             "THRESHOLD and decisive for whether the model is right.")


def _s3_build_threshold_line(d):
    # THE GRADED LINE. Everything downstream quotes 31/15 -- the delta-prime
    # robustness row, the matrix slide, the clinical threshold, the band --
    # and the inequality that produces it was never on a surface. The delta
    # prime slide after this one CHECKS that the threshold is stable before
    # the threshold has been obtained, which is the wrong way round.
    d.derivation(
        None, "segment 3", "build  ·  the line the rest of the hour quotes",
        "Spreading puts a floor under P²D",
        [
            ("the ratio must clear one",
             "R_{0}^{T} = P²D(1 − 1/R_{0}) > 1",
             "the factor we just derived, set against the only threshold a "
             "reproductive ratio has"),
            ("divide by that probability",
             "P²D > 1/(1 − 1/R_{0}) = R_{0}/(R_{0} − 1)",
             "it is below one, so dividing RAISES the floor — the therapy "
             "pays for the cells that die before HIV-1 ever reaches them"),
        ],
        closing="R_{0} = 31/16, so the floor is R_{0}/(R_{0} − 1) = "
                "31/15 = 2.0667",
        note="One inequality, and it is the line the rest of the hour "
             "quotes, so we do it properly rather than quoting the "
             "number.\n "
             "A reproductive ratio has exactly one interesting value and it "
             "is one. Put the expression we just built against it.\n "
             "Now divide. One minus one over R nought is a probability — it "
             "is the chance the waiting cell meets the virus before it dies "
             "— so it is less than one, and dividing by it pushes the floor "
             "UP. That is the therapy paying for every cell that dies "
             "before HIV-1 gets there.\n "
             "And read what the floor is made of. R nought over R nought "
             "minus one contains nothing of the therapy at all. The bar the "
             "vector has to clear is set entirely by how fast the "
             "wild-type virus is spreading in that patient.\n "
             "For this patient R nought is thirty-one sixteenths, so the "
             "floor is thirty-one fifteenths, 2.0667. Hold that number.")


def _s3_build_deltaprime(d):
    s = d.light()
    d.header(s, "segment 3", "build — the assumption that does not matter here")
    d.title(s, "δ′ cancels out of the threshold entirely")
    d.rows(s, [
        ("the assumption", "Weinberger sets δ′ = D·δ: a dually infected "
                           "cell's "
                           "death rate is made a function of a knob. At "
                           "D = 0.4 an I_{D} cell lives 3.6 days against "
                           "an HIV-only I cell's 1.43; at D = 0.01 it lives "
                           "143 days."),
        ("where it cancels", "production carries P²Dnδ′ and the I_{D} "
                             "lifetime is 1/δ′. They multiply, so δ′ is "
                             "gone.", AMBER),
        ("checked", "the threshold stays 31/15 for δ′ from 0.001 to 50"),
        ("so what δ′ does set", "the I_{D} population and the length of the "
                                "transient — not the threshold. It is not a "
                                "limit on this result."),
    ], top=1.90, label_w=2.6)
    d.foot(s, "The paper calls its δ′ assumptions “benign”. This is the "
              "algebra behind that word, and we can state it rather than "
              "quote it.")
    d.notes(s,
           "Delta prime carries the paper's own double-dagger footnote — "
           "engineerable, never measured in vivo — and it is an odd "
           "assumption: it makes how fast a cell dies a function of how good "
           "your drug is.\n "
           "And it does not touch the threshold, for the same reason the "
           "burst size did not. Production scales with delta prime and "
           "lifetime goes as one over delta prime, so they multiply out.\n "
           "I want this said precisely, because it is easy to file delta "
           "prime under limitations and leave it there. It is a limit on the "
           "trajectory and on how many I_D cells there are. It is not a "
           "limit on the number we just derived, which does not contain "
           "it.\n "
           "What would falsify it is whether dually infected cells really do "
           "live measurably longer as the cargo gets stronger.")


def _grid(d, s, x, y, name, entries, cell=1.38, lab=0.85, row_h=0.42):
    """A 3x3 matrix drawn as a labeled grid, one text box per entry.

    A matrix set as three lines of text does not line up: the deck's body font
    is proportional, so "d - klambda n/c" and "0" are different widths and the
    columns wander. One box per cell, centerd, is aligned by construction --
    and the row and column headers are worth more than brackets would be,
    because they say what each entry MEANS: the row is the compartment the
    flow goes to, the column the one it came from.
    """
    names = ["I_{T}", "I_{D}", "V_{T}"]
    d.text(s, name, x, y - 0.46, lab + 3 * cell, 0.40, role="body",
           font=HEAD, bold=True, color=TEAL)
    for j, cn in enumerate(names):
        d.text(s, cn, x + lab + j * cell, y, cell, 0.38, role="caption",
               font=HEAD, bold=True, color=MUTED, align="c")
    for i, rn in enumerate(names):
        yy = y + (i + 1) * row_h
        d.text(s, rn, x, yy, lab, 0.38, role="caption", font=HEAD, bold=True,
               color=MUTED)
        for j in range(3):
            d.text(s, entries[i][j], x + lab + j * cell, yy, cell, 0.38,
                   role="body", color=INK, align="c")


def _s3_build_ngm(d):
    # THE MATRIX SLIDE HAD NO MATRIX. The convention warning -- the session's
    # single autograder risk, NUMBERS.md 18.4 -- was delivered as "same
    # matrices, split differently" to a room that has never seen F or V, and
    # there was no next-generation matrix anywhere in the 80-slide deck. So
    # the warning landed only for students who already knew the recipe, which
    # is the half of the cohort it was NOT written for. F and V are printed
    # here, from NUMBERS.md 18.1, before the slide that says the split can be
    # taken two ways.
    #
    # "Spectral radius" is said once and then translated, because it appeared
    # nowhere else in the course and was never defined anywhere in the deck.
    s = d.light()
    d.header(s, "segment 3", "build — the machine that produced it")
    d.title(s, "The same algebra, as a matrix")
    d.rows(s, [
        ("the compartments", "x = (I_{T}, I_{D}, V_{T}), empty until the "
                             "therapy invades"),
        ("the split", "F holds the terms that make a NEW infection · V "
                      "holds every other way out"),
        ("R_{0}^{T} is", "the spectral radius of F·V⁻¹ — its largest "
                      "eigenvalue", AMBER),
    ], top=1.80, bottom=3.86, label_w=3.0)
    _grid(d, s, 0.90, 4.52, "F  ·  new infections",
          [["0", "0", "c/n"],
           ["0", "0", "0"],
           ["0", "0", "0"]])
    _grid(d, s, 6.60, 4.52, "V  ·  everything else",
          [["kλn/c", "0", "0"],
           ["d − kλn/c", "δ′", "0"],
           ["0", "−P²Dnδ′", "c"]])
    d.foot(s, "Rows are where the flow goes, columns where it came from. "
              "Only one entry of F is non-zero.")
    d.notes(s,
           "The same derivation again, in the form somebody with an "
           "epidemiology course behind them will recognize.\n "
           "Three compartments, and they are the three that are empty before "
           "the therapy arrives: I_T, I_D and free vector. Everything else in "
           "the model is sitting at its steady state.\n "
           "F collects the terms that create a new infection and V collects "
           "every other way out — death, clearance, progression. R0_T is the "
           "spectral radius of F times V inverse, which is a phrase worth "
           "translating once: the largest eigenvalue.\n "
           "Look at F. One entry. A free vector virion infecting a waiting "
           "cell is the only thing in this model that counts as a new "
           "infection of the therapy, and c over n is where the burst size "
           "will cancel.\n "
           "Multiply out and the eigenvalues are zero, zero, and P squared D "
           "times one minus one over R zero. Same answer as the three "
           "factors.")


def _s3_build_matrix(d):
    # SAID WHILE THE MATRIX IS ON THE SLIDE (DESIGN 3, NUMBERS 18.4). A
    # student who builds the next-generation matrix by the textbook recipe
    # gets the square root and IS RIGHT; they should not discover that
    # from a mark. T73 is autograded on PS9 and sits on the final.
    #
    # THE TEXTBOOK IS CITED, with its year and its journal. It was "van den
    # Driessche and Watmough" and nothing else -- deck-bar B4, a paper
    # introduced before its result is quoted. The citation is the third
    # disclosed exception to the nothing-not-in-NUMBERS rule, and it is a
    # reference rather than a number; NUMBERS.md 18.4 names the authors
    # without the year.
    #
    # Each spectral radius sits on its own line, forced, because both of them
    # wrapped mid-expression -- after the minus sign of 1 - 1/R0, which is
    # the worst available place for a line to break.
    s = d.light()
    d.header(s, "segment 3", "build — the other answer that is also right")
    d.title(s, "The threshold survives both conventions")
    d.rows(s, [
        ("what we built", "new infections are counted when a cell becomes "
                          "I_{T}\nlargest eigenvalue:   P²D(1 − 1/R_{0})"),
        ("the textbook recipe", "van den Driessche & Watmough, Math. Biosci. "
                                "180:29 (2002), count virion PRODUCTION as a "
                                "new infection too — the same two matrices, "
                                "split differently\nlargest eigenvalue:   "
                                "√(P²D(1 − 1/R_{0}))", AMBER),
        ("the threshold at 1", "IDENTICAL. √x > 1 exactly when x > 1, so "
                               "P²D > 31/15 either way and nothing in this "
                               "hour moves"),
        ("the magnitude", "is NOT identical. Build the matrix by the recipe "
                          "and you get the square root, and you are right. "
                          "Any question asking for a numerical R_{0}^{T} has to "
                          "say which convention."),
    ], top=1.86, label_w=2.8)
    d.foot(s, "Both were computed. The published form matches ours, so "
              "Weinberger counted the way we did.")
    d.notes(s,
           "This is the one place in the hour where two correct answers "
           "differ, and you should hear it from me rather than from a mark.\n "
           "If you have met next-generation matrices you will split F and V "
           "so that a virion being produced counts as a new infection of the "
           "free-virus compartment. That is the standard recipe, from van "
           "den Driessche and Watmough in 2002, and it gives the square root "
           "of what we derived.\n "
           "Threshold at one is the same number — the square root of "
           "something exceeds one exactly when the something does. So "
           "2.0667 is convention-free and everything today is safe.\n "
           "The magnitude is not. If a problem asks you for a numerical "
           "R0_T and does not state the convention, that is a defect in the "
           "question and you should say so.")


def _s3_build_meaning(d):
    # THE BEST LINE IN THE SESSION, AND IT GETS A SLIDE OF ITS OWN.
    s = d.light()
    d.header(s, "segment 3", "build — what that factor is")
    d.title(s, "1 − 1/R_{0} is a probability")
    # Explicit placement, not image_centered: there is text beside it. The
    # box is derivation_fig's 5.4 x 4.95, so s25_chain_5 is projected at the
    # same scale as s25_chain_1..4 in the first derivation -- see the note on
    # the urn slide. The chain must not shrink on the slide that reads
    # 1 - 1/R₀ off it.
    #
    # THIS IS ALSO THE ONLY PICTURE THE SECOND DERIVATION HAS, and it is not
    # in it: DESIGN 7 item 5 asks for a `derivation_fig` chain run with the
    # two cancellations marked on the arrows, and that series does not exist
    # yet. When it does, `_s3_build_waiting` and `_s3_build_factors` become
    # derivation_fig runs and this slide keeps the finished panel.
    d.image(s, FIG + "s25_chain_5.png", M, 1.72, 5.40, 4.95)
    d.text(s, "It is the probability that an I_{T} cell ever meets the "
              "wild-type virus it needs in order to replicate at all.",
           6.32, 2.04, 6.31, 1.70, role="emphasis", color=INK)
    d.text(s, "So R_{0}^{T} is not “R_{0} of the vector”. It is indexed on a cell "
              "that is WAITING — and the therapy's susceptible pool is cells "
              "that already carry the vector and have nothing to replicate "
              "it.",
           6.32, 4.04, 6.31, 1.80, role="body", color=MUTED)
    d.notes(s,
           "If you remember one sentence from this hour, this is it.\n "
           "One minus one over R zero looks like a correction factor bolted "
           "onto a product of two knobs. It is not. It is a probability — "
           "the chance that a cell sitting there with your vector in it ever "
           "encounters the virus it needs in order to do anything at all.\n "
           "Which is why the index case has to be an I_T cell, and why "
           "calling this quantity R0 of the vector loses the whole point. "
           "The susceptible pool for this therapy is not uninfected cells. "
           "It is cells that already have the therapy and are waiting.\n "
           "Fifteen over thirty-one, for this patient. So a bit under half "
           "of the waiting cells ever get the chance.")


def _s3_build_clinical_threshold(d):
    s = d.light()
    d.header(s, "segment 3", "build — the threshold in things you can measure")
    d.title(s, "Four clinical numbers and the burst size")
    d.rows(s, [
        ("substitute the back-solve", "k = c/(nT_{0})  and  λ = dT_{0} + cV_{0}/n — "
                                      "the two fitted parameters go away"),
        ("R_{0} becomes", "1 + cV_{0}/(n·d·T_{0}) = 1 + 3000/3200 = 1.9375 = 31/16"),
        ("and the threshold", "P²D > 1 + n·d·T_{0}/(c·V_{0}) = 1 + 3200/3000 = "
                              "31/15 = 2.0667", AMBER),
        ("with V_{0} as", "100 virions/µl — the unit conversion doing its work "
                       "a second time"),
    ], top=1.94, label_w=3.0)
    d.foot(s, "No fitted parameter left in it: a virion clearance rate, a "
              "burst size, a T-cell death rate, a CD4 count and a set point.")
    d.notes(s,
           "This is the form I would quote to somebody designing "
           "one of these.\n "
           "Put the back-solve back in and lambda and k — the two numbers "
           "that were never measured — disappear. What is left is four "
           "things a clinic measures plus the burst size.\n "
           "And the conversion comes back. V zero enters as a hundred per "
           "microlitre, not ten to the fifth. Get that wrong here and the "
           "threshold is off by a factor of a thousand.\n "
           "One caution if anybody does sensitivity on this. The dependence "
           "on n and c changes SIGN depending on whether you hold lambda and "
           "k fixed or T zero and V zero fixed. Because lambda and k were "
           "back-solved, only the second is a coherent perturbation of this "
           "model.")


def _s3_build_band(d):
    s = d.light()
    d.header(s, "segment 3", "build — how firm is that number")
    d.title(s, "R_{0}^{T} is proportional to P²D")
    d.rows(s, [
        ("the coefficient", "1 − 1/R_{0} runs 0.47 to 0.95 as R_{0} is swept from "
                            "1.9 to 20 — a sweep of this model's own "
                            "parameters, not a range of patients"),
        ("and the top of it", "comes from Table 1's alternative c = 3, which "
                              "cannot be used without rescaling k. Every "
                              "item here pins c = 30."),
        ("so the threshold", "P²D between about 1.05 and 2.11 — and 2.0667 "
                             "at this patient's R_{0}, which is what every "
                             "figure and every item here uses", AMBER),
        ("it is not", "R_{0}^{T} ≈ P²D. The coefficient is about one half and "
                      "dropping it is not a rounding"),
        ("what it costs you", "take the threshold as P²D > 1 and at D = 0.2 "
                              "you get P > 2.236 where it is really 3.21 — "
                              "a FACTOR of √2.0667 = 1.4376, not a "
                              "difference"),
    ], top=1.90, label_w=2.8)
    d.foot(s, "The threshold is a statement about the construct. The band "
              "is what the model does as R_{0} is swept.")
    d.notes(s,
           "Proportional to, not approximately equal to. The coefficient is "
           "about a half and it does not go away.\n "
           "The cost of dropping it, with the arithmetic out loud. You "
           "design a vector at P = 2.24, it does not spread, and the real "
           "bar at that D is 3.21. Those two differ by a FACTOR of 1.4376, "
           "the square root of 2.0667 — not by the 0.98 between them.\n "
           "Where the band comes from, and I am careful here. It is R0 swept "
           "from 1.9 to 20 inside this model, not a survey of patients. The "
           "top end comes from Table 1's alternative c of 3, which also "
           "drops T star to 80 and contradicts T zero of 800, so it cannot "
           "be used without rescaling k. Every item we set pins c at 30.\n "
           "What the sweep does show is how little R0 buys: a factor of ten "
           "in R0 moves the threshold by less than a factor of two. The "
           "threshold is a statement about your construct.")


def _s3_release(d):
    s = d.light()
    d.header(s, "segment 3", "pose — four minutes on your own paper")
    d.title(s, "Your construct measures P = 8")
    d.rows(s, [
        ("what you have", "a vector characterized at a packaging advantage "
                          "of 8, in a patient with R_{0} = 1.9375. Remember "
                          "D is the fraction of virus production that "
                          "REMAINS."),
        ("the question", "What is the smallest D this construct can get "
                         "away with and still spread?", AMBER),
        ("and then", "say in one sentence what a LOWER bound on D means for "
                     "how good the drug is allowed to be"),
    ], top=2.10, label_w=2.2)
    d.foot(s, "You have the threshold. Rearrange it for D rather than for P.")
    d.notes(s,
           "D has to exceed 2.0667 over P squared. P squared is 64, so D "
           "must be above 0.0323.\n "
           "The second part is the one I want argued about. D is the "
           "fraction of virus production that REMAINS, so a LOWER bound on D "
           "is an UPPER bound on how effective the cargo may be. This "
           "construct may suppress HIV-1 production by at most about 96.8 "
           "percent. Any better and the therapy cannot spread.\n "
           "That sentence is the whole of segment four in one inequality, "
           "and I would rather they wrote it down than heard it from me. I "
           "run it this direction — D given P — because that is the "
           "direction the question gets asked in a lab.")


def _s3_build_theirs(d):
    # THE SOURCE COMES BEFORE THE DIGITIZATION. Our replot of Weinberger's
    # floor is the right panel of `s25_design_space`, and the panel it was
    # read off used to appear AFTER it -- so the comparison the debrief turns
    # on could never be seen at once (DESIGN 5, segment 3, asks for the two
    # beside each other). This slide now closes the build: the room reads
    # their figure, gets the comparison in body type, and then meets the
    # replot on the debrief with the original already in hand.
    #
    # AND THE TITLE NO LONGER ASSERTS WHAT NUMBERS.md 19 FORBIDS. It read
    # "The threshold is a curve on their floor", which presents their
    # simulated boundary as confirming our closed form -- the one thing 19
    # rules out in terms -- while the debrief's own note said the two are NOT
    # the same line. The false one was the 32pt title. 19's finding is the
    # title now, and the note says what the red-cyan boundary IS: the same
    # object, computed by simulation rather than in closed form.
    s = d.light()
    d.header(s, "segment 3", "build — where that boundary came from")
    d.title(s, "Their floor crosses our band near D = 0.35")
    d.rows(s, [
        ("their boundary, as P²D", "1.14–1.29 over D = 0.08–0.20 · "
                                   "2.15–3.86 over D = 0.35–0.50"),
        ("ours", "2.0667 here; 1.05–2.11 over the band"),
        ("so", "runs along our band’s FLOOR at small D, ABOVE it past "
               "D ≈ 0.35", AMBER),
        ("the coordinates are ours", "read off panel (a) at 300 dpi; panel "
                                     "(b) runs P to 100"),
    ], top=1.80, bottom=6.50, side=False, right=5.60)
    # The slot carries the crop's own aspect (1550 x 1797, portrait), centerd
    # in the column left of the text: a 6.8in-wide slot held a 3.19in image
    # and floated it.
    d.paper_figure(s, "weinberger2003_fig3", 7.62, 1.70, 3.22, 3.70,
                   "Weinberger, Schaffer & Arkin, J. Virol. 77:10028 (2003), "
                   "Fig. 3",
                   "Floor of (a): red dies, cyan persists.",
                   show_caption=True)
    d.notes(s,
           "The figure the session is built on, and thirty seconds on how to "
           "read it.\n "
           "The surface is the HIV set point the patient ends up at, on a log "
           "axis. The floor underneath carries the stability map. Red is "
           "where the pretherapy state is stable and the vector dies out. "
           "Cyan is where it persists. Black is the oscillatory band, and "
           "panel b runs P out to a hundred on a different axis.\n "
           "That red-cyan boundary is the same object we derived — the "
           "R0_T = 1 contour — computed by simulating the full model instead "
           "of in closed form. So the honest comparison is between a closed "
           "form and a simulation, and the two do not land on top of each "
           "other.\n "
           "Theirs runs under our band at small D, around 1.1 to 1.3 in P "
           "squared D where we have 2.07, crosses us near D of 0.35, and "
           "leaves the band above that, out to 3.9. Same shape, not the same "
           "line. Which is why the design space goes up as a band.\n "
           "And why we replotted rather than drawing our contour on top. "
           "This is a perspective projection with the floor tilted away from "
           "you, so the same P and D land in different places at different "
           "depths. The twelve coordinates we read off are ours and the "
           "figure beside them says so.")


def _s3_debrief_ours(d):
    # THE SENTENCE THE RELEASE ASKED FOR IS WRITTEN ON THE PAGE. The title
    # carried "96.8% effective" and the figure carried "P = 8 needs
    # D = 0.0323", and the step between them -- D is the fraction REMAINING,
    # so 1 - 0.0323 = 96.8% -- was in the speaker note alone, with the
    # conditions (P = 8, R0 = 1.9375) nowhere on the title line.
    #
    # THE BAND IS 4.30, AND THAT IS NOT A STYLE CHOICE. It was 3.40 while
    # s25_design_space saves 9.794 x 4.238 in, so the HEIGHT bound the
    # placement: 3.40/4.238 = 0.802, and the figure's eleven 20pt labels
    # projected at 16.0pt, under the floor, on a slide DESIGN.md 6 puts on
    # the never-cut list. The shrink was visible on the rendered page --
    # in-figure type plainly smaller than the slide's own body type. The
    # figure cannot be re-authored into a 3.0 aspect without cutting the
    # wrapped D-sense x-labels that deck-bar F5 requires, so the DECK gives
    # it the room. At band 4.30 the width binds instead (4.30 x 2.3113 =
    # 9.938 < max_w 10.2) and the placement scale is 1.015.
    #
    # WHAT PAID FOR THE 0.90 IN. The emphasis line, cut from 99 rendered
    # characters to 68 so it sets on ONE line (0.40in) rather than two
    # (0.81in) -- deck-gauntlet 5.3, cut text before loosening geometry,
    # and never shrink type. Nothing numeric was lost: 2.0667/64, 0.0323
    # and the 1 - 0.0323 step are all still here. What went is "At " and
    # the trailing "is the most it may suppress", which the TITLE already
    # says in the same words. The foot stays where Adam put feet (6.75);
    # the image now reaches 6.04 and the emphasis runs 6.14-6.60, so the
    # three clear each other by 0.10 and 0.15 in. deck-bar D5c: slide_fit
    # does not check an image against the text below it, so that sum is
    # done here rather than left to the gate.
    s = d.light()
    d.header(s, "segment 3", "debrief")
    d.title(s, "At P = 8 the drug may be at most 96.8% effective")
    d.image_centered(s, FIG + "s25_design_space.png", top=1.74, band=4.30)
    d.text(s, "R_{0} = 1.9375:  D > 2.0667/64 = 0.0323 REMAINS, so "
              "1 − 0.0323 = 96.8%.",
           M, 6.14, W - 2 * M, 0.46, role="emphasis", color=INK)
    # THE FOOT CARRIES WHAT THE FIGURE DOES NOT. The left panel's own title
    # reads "P = 8 needs D = 0.0323" and marks that point and no other, so a
    # foot repeating the construct would duplicate the plate in different
    # words. What the plate cannot say is why a point is the wrong object to
    # read: the threshold is a curve, and the trade between the two knobs is
    # what the curve means.
    d.foot(s, "Read the contour, not a point: the threshold is a CURVE in "
              "(P, D), so a better cargo has to be bought with a better P.")
    d.notes(s,
           "The mark is the construct you just worked: P of eight, D of "
           "nought point oh three two three, and the panel title says so. P "
           "squared D is sixty-four times that, which is 2.0667 — the "
           "contour it sits on.\n "
           "The sentence on the slide is the one I want written down. D is "
           "the fraction REMAINING, so a lower bound on D is an upper bound "
           "on how good the cargo may be. Improve it past 96.8 percent and "
           "this construct stops spreading.\n "
           "If somebody asks about the 3.21 from the band: that is a "
           "different construct, at D of nought point two, on this same "
           "contour. It is not drawn here, and it does not need to be — the "
           "contour is the object, not either point on it.\n "
           "The right panel is the boundary we read off their Fig. 3a, "
           "replotted flat; that digitization is ours and the figure says "
           "so. Same shape and same scale as ours, and not the same line — "
           "near the bottom of our band at small D, crossing around "
           "D = 0.35, outside it above.\n "
           "So the closed form and the simulation agree about the shape of "
           "the design space and not about its exact location. I would "
           "rather show that than a single sharp contour claiming agreement "
           "nobody checked.")


# ------------------------- segment 4 · your payload is the vector's fitness ---
def _s4_frame_model(d):
    s = d.light()
    d.header(s, "segment 4", "frame — two arrows that share a knob")
    d.title(s, "Everything today is in this one panel")
    d.paper_figure(s, "weinberger2003_fig1", 3.89, 1.68, 5.55, 4.05,
                   "Weinberger, Schaffer & Arkin, J. Virol. 77:10028 (2003), "
                   "Fig. 1",
                   "Red: [1]–[3]. Blue: the therapy equations.",
                   show_caption=True)
    d.notes(s,
           "Everything we have derived is in this one panel, and the arrows "
           "carry their own rate labels so you can read the equations off "
           "the picture.\n "
           "Three things to point at. I_T dies at d, the uninfected rate, "
           "not at delta — it is a healthy cell. HIV can infect an I_T cell "
           "but not an I_D cell, because Nef pulls CD4 off the surface and "
           "an I_T cell has no Nef. And the P squared is attached to vector "
           "production only.\n "
           "Now the thing I want them to find. Look for D on this "
           "diagram and count where it appears. It is on the HIV production "
           "arrow out of an I_D cell, in equation three — and it is ALSO on "
           "the vector production arrow, in equation six. One knob, two "
           "arrows.\n "
           "That is the whole of the next fifteen minutes and it is visible "
           "before any algebra.")


def _s4_frame_dsense(d):
    s = d.light()
    d.header(s, "segment 4", "pose — hands up, thirty seconds")
    d.title(s, "The paper defines D backwards")
    d.rows(s, [
        ("D is defined in the paper as", "“the fraction by which the HIV-1 "
                                         "titer produced from I_{D} cells is "
                                         "therapeutically downregulated”"),
        ("D is USED in the equations as", "a multiplier on HIV-1 production, "
                                          "so D = 1 is NO inhibition — the "
                                          "reverse of the sentence above. "
                                          "Which would you trust, and how "
                                          "would you check?", AMBER),
        ("and while we are here", "n = 200 is the burst size: virions "
                                  "released per infected cell. Session 12's "
                                  "burst size was a TRANSLATIONAL burst, "
                                  "geometric with mean k_{p}/γ_{m}. Same "
                                  "words, different object."),
    ], top=2.00, label_w=3.1)
    d.notes(s,
           "We have been using D as the fraction remaining since the "
           "threshold, so the room already knows which end is which. What "
           "is new here is that the paper's own prose definition says the "
           "opposite, and I want them to notice it in a paper rather than "
           "be told.\n "
           "How to check: read the equations. D multiplies the production "
           "term, so D = 1 leaves production untouched.\n "
           "In the equations D multiplies the production term, so D = 1 "
           "leaves production untouched — no inhibition at all — and D = 0 "
           "is total inhibition. The paper itself says so in another place: "
           "if no therapeutic gene is encoded and D = 1, there is no "
           "reduction.\n "
           "So read D as the fraction REMAINING. If you take the prose "
           "definition at face value every sign in this segment comes out "
           "backwards.\n "
           "And the burst size collision, here where n arrives. Session 12's "
           "burst was proteins per mRNA, geometric. This one is virions per "
           "cell. I would rather spring that deliberately than have somebody "
           "quietly confused for twenty minutes.")


def _s4_build_shared(d):
    s = d.light()
    d.header(s, "segment 4", "build — one knob on two arrows")
    d.title(s, "The vector parasitises what it suppresses")
    d.rows(s, [
        ("equation [3]", "HIV-1 production from an I_{D} cell carries D"),
        ("equation [6]", "the VECTOR's own production from that same cell "
                         "carries the same D", AMBER),
        ("so as D → 0", "R_{0}^{T} = P²D(1 − 1/R_{0}) → 0. The cargo cannot "
                        "inhibit HIV without equally inhibiting the vector, "
                        "because in this architecture they share one "
                        "production term."),
        ("meanwhile", "singly infected I cells never see the inhibition at "
                      "all, so they keep making virus at the old rate and "
                      "the set point rebounds"),
    ], top=1.92, label_w=2.4)
    d.foot(s, "The authors' own phrase is that crHIV-1 ends up “shooting "
              "itself in the molecular foot”.")
    d.notes(s,
           "This is the mechanism and it is structural rather than "
           "numerical.\n "
           "The vector has no capsid genes. It is packaged by Gag-Pol that "
           "the virus makes. So a cargo that shuts down viral production "
           "shuts down the supply of the very protein the vector needs to "
           "leave the cell. Suppress hard enough and the cell stops making "
           "anything, including your therapy.\n "
           "And the cruelty of it is the last row. The inhibition only acts "
           "inside dually infected cells. Every singly infected cell in the "
           "patient carries on exactly as before, so the virus comes back to "
           "its old set point while your vector has stopped spreading.\n "
           "The phrase in quotes is theirs, from the paper.")


def _s4_build_fig2a(d):
    # A DECK-SIDE KEY, BECAUSE THE PANEL'S OWN LEGEND CANNOT BE READ. W03's
    # Fig. 2 panels are embedded rasters at the source's resolution
    # (NUMBERS.md 9 says so and asks for them to be redrawn rather than
    # cropped). On the wall this legend renders "D=D.8 ... D=D.0I": five
    # curves against five D values with no legible mapping between them,
    # which is deck-bar C3 -- several curves against several parameters
    # arriving as a picture rather than a comparison. And NEITHER panel
    # names a quantity or a unit on either axis.
    #
    # A RE-CROP CANNOT FIX EITHER. The legend is a raster at the source's
    # own resolution, so enlarging it enlarges the blur; and the axis
    # labels the panel is missing were never there to crop. Nor may the
    # figure be redrawn -- it is the authors' published panel and this deck
    # does not alter published figures. So the key goes BESIDE the crop, in
    # BODY type, and the crop is not touched or resized: it moves from
    # x = 3.00 to the left margin, which costs it nothing and opens a
    # 4.30in column on the right. Never shrink type (deck-gauntlet 5.3).
    #
    # THE SWATCHES ARE THE PAPER'S colorS, NOT OURS -- see W03_CURVES at
    # the head of this module for where each one came from and for the
    # three anchors that fix the color-to-D mapping without reading the
    # legend. Every number printed here traces to NUMBERS.md: the five D
    # values to 5c, the 0-360 days and the pretherapy 10**5 to 9 (and the
    # 10**5 again to 18.1's V* = 10**5/ml).
    #
    # ONE DISCLOSED EXCEPTION, and it is the fourth in this deck (the
    # module docstring names the other three). The two y-axis RANGES --
    # 10**2-10**5 left, 10**4-10**8 right -- are read off the panel's own
    # tick labels, verified at 2x, and are not in NUMBERS.md. They are the
    # reason the right panel is a mirror in SHAPE and not in scale, which
    # is the one thing a reader cannot get from the picture at this size,
    # and the room can check them against the ticks in front of it.
    # REQUESTED: a line in NUMBERS.md 9 recording both ranges.
    s = d.light()
    d.header(s, "segment 4", "build — one knob at a time: D")
    d.title(s, "Turning the drug up is not monotone")
    d.paper_figure(s, "weinberger2003_fig2a", M, 1.70, 7.33, 3.70,
                   "Weinberger, Schaffer & Arkin, J. Virol. 77:10028 (2003), "
                   "Fig. 2a",
                   "Fixed P = 30; five values of D.",
                   show_caption=True)
    # The crop occupies 0.70-8.03 across and 1.70-5.40 down; its citation
    # and caption run to 6.51 in the SAME column, so the key column starts
    # at 8.33 and nothing of it lands on either. It ends at 6.75, clear of
    # the slide number in the bottom-right corner (7.10 down).
    KX, KW = 8.33, 4.30
    d.text(s, "the five curves, in D", KX, 1.74, KW, 0.34,
           role="body", font=HEAD, bold=True, color=TEAL)
    for i, (lab, col) in enumerate(W03_CURVES):
        yy = 2.14 + i * 0.44
        d.shape(s, S.RECTANGLE, KX, yy + 0.05, 0.40, 0.24, fill=col,
                line=None)
        d.text(s, lab, KX + 0.52, yy, 1.80, 0.34, role="body", color=INK)
    # EVERY LINE BREAK BELOW IS EXPLICIT. At 20pt this column holds 30
    # characters, and a block left to wrap on its own takes a different
    # number of lines the moment a word changes -- which is how a key
    # written to fit ends up three lines deep on the slide number.
    # WHICH PANEL IS WHICH SPECIES comes first: this figure's whole point
    # lives in the DIFFERENCE between its two panels, and a student who does
    # not know that the left is HIV-1 and the right is crHIV-1 cannot read it
    # at all. NUMBERS 9: "2a, split HIV-1 / crHIV-1 ... five D values at
    # fixed P = 30".
    d.text(s, "x: 0–360 days, y: virions/ml\nleft HIV-1, right crHIV-1",
           KX, 4.44, KW, 0.70, role="body", color=INK)
    d.text(s, "left 10²–10⁵, right 10⁴–10⁸\ndifferent scales, read apart",
           KX, 5.26, KW, 0.70, role="body", color=INK)
    # THIS LINE SAID "same shape, other scale" AND THAT WAS FALSE -- and
    # false about the one thing the session is built on. NUMBERS 9: "The
    # crHIV panel on the right shows the MIRROR image: at D = 0.01 the
    # vector barely rises." Not a rescaling: at the smallest D the HIV
    # trace goes back UP to its pretherapy set point while the vector goes
    # DOWN, which is the non-monotone paradox in one click. The speaker
    # note had it right all along and the slide contradicted it -- the same
    # note-right / slide-wrong shape as the defect fixed on slide 53 today,
    # and the slide is the half the room reads.
    d.text(s, "green D = 0.01: HIV at set\npoint, vector never appears",
           KX, 6.08, KW, 0.70, role="body", color=INK)
    d.notes(s,
           "One knob at a time, and this is D with P held at thirty.\n "
           "Read the left panel downward. As D falls from 0.8 to about 0.4 "
           "the HIV set point falls — the drug is working. Keep going and at "
           "D = 0.2 it oscillates. Go all the way to D = 0.01 and the green "
           "trace sits flat at the pretherapy level: over these three "
           "hundred and sixty days the therapy has done nothing.\n "
           "Say the window, because it matters. That is what their panel "
           "shows, and it is not what the model says. At P of thirty, R "
           "nought T is four point three five — the vector cannot die out "
           "at D = 0.01, it is still arriving. Run it out and the set point "
           "lands at one point three times ten to the four, a sevenfold "
           "reduction. The end where the therapy really does nothing is "
           "D below nought point zero zero two three, where R nought T "
           "falls through one. We put that on the next slide.\n "
           "The right panel is the mirror image. At D = 0.01 the vector "
           "never appears on that panel at all — its axis starts at ten to "
           "the four and the green trace never gets there, because it has "
           "suppressed its own supply.\n "
           "So there is a valley in D rather than a slope. The best drug is "
           "somewhere in the middle, and that is the paradox with a picture "
           "under it.\n "
           "One honest wrinkle. The caption says oscillations arise at "
           "D = 0.1; the panel's own legend has no 0.1 curve and labels the "
           "oscillating trace 0.2. That is a mismatch inside the paper, and "
           "I say so here rather than leave them to find it alone.")


def _s4_build_setpoint(d):
    """Where the 360-day window ENDS UP: the set point against D.

    This slide exists because the paper's Fig. 2a is a WINDOW and the room has
    just been reading it as an outcome. NUMBERS 20.1: at D = 0.2 the system is
    still on its damped oscillation at day 360, and at D = 0.01 it is deep in a
    transient that does not finish until about day 1500. Two of their five
    curves are therefore not set points at all.

    It is a separate slide rather than a panel beside the crop, deliberately.
    The two pictures are DIFFERENT QUANTITIES -- theirs a 360-day window, ours
    the asymptote -- and side by side they read as the same thing at two
    scales. That is the false identification bar F8 already records twice in
    this deck (the threshold-vs-floor slide, and this one's own former "same
    shape, other scale"). A separate slide lets the transition be SAID: that
    was 360 days; here is where it ends up.

    It is also segment 3's payoff. R0_T = 1 was built over seventeen slides as
    algebra; here it arrives as the left wall of a clinical curve.
    """
    s = d.light()
    d.header(s, "segment 4", "build — and where that window ends up")
    d.title(s, "The valley has a wall at each end, for opposite reasons")
    # Band must be >= 4.15 or the placement scale drops under 1.0 and the
    # type goes under Adam's floor. At 4.30 it renders 10.147 x 4.299,
    # bottom edge 6.039 -- which clears `sources` at 6.220 by 0.18in.
    # Checked by hand: deck-bar D5c, `slide_fit` does not compare an image
    # with the full-width text under it, and on this very session an image
    # bottom at 6.231 silently overlapped a sources block at 6.220.
    # top 1.74 / band 4.30 was authored against a shorter title band and
    # `slide_fit` caught the title sitting ON the picture. Recomputed rather
    # than nudged: at top 1.82, band 4.22 the fit is min(10.2/9.794,
    # 4.22/4.150) = 1.017, so it renders 9.960 x 4.220 with its bottom at
    # 6.040 -- scale still over 1.0, and 0.18in of daylight to `sources`.
    d.image_centered(s, FIG + "s25_setpoint_valley.png", top=1.82, band=4.22)
    d.foot(s, "Both ends sit on the pretherapy line. On the right there is no "
              "inhibition; on the left the vector cannot persist.")
    d.notes(s,
           "Same model, same P of thirty, but now solved rather than watched "
           "for a year.\n "
           "The floor is six hundred and fifty-eight virions per millilitre "
           "at D of nought point three one — a hundred and fifty-two fold "
           "below pretherapy. Worth one remark: the paper's text picks nought "
           "point two as the best D and its own Fig. 3b caption picks nought "
           "point four. The floor is flat enough that both are within "
           "eighteen percent of the true minimum, so they disagree and it "
           "does not matter.\n "
           "The right wall is easy. D of one is no inhibition at all.\n "
           "The left wall is the thing we built in the last segment. R "
           "nought T falls through one at D of nought point zero zero two "
           "three, the vector cannot persist, and the set point goes back to "
           "pretherapy. That is the threshold, arriving as a wall on a "
           "picture of clinical outcome.\n "
           "The dotted stretch has no set point at all — the equilibrium is "
           "unstable there and the gray band is the limit cycle it settles "
           "into instead. That window agrees with their own stability map, "
           "which is a stronger check on our equations than any level "
           "comparison, because it tests the dynamics.\n "
           "Three of their five points are on here as diamonds. The other "
           "two are missing on purpose: at D of nought point two and nought "
           "point zero one their curves had not arrived by day three sixty, "
           "so there is nothing to compare.")


def _s4_build_fig2b(d):
    s = d.light()
    d.header(s, "segment 4", "build — one knob at a time: P")
    d.title(s, "Turning the packaging up just works")
    d.paper_figure(s, "weinberger2003_fig2b", 3.91, 1.70, 5.51, 3.70,
                   "Weinberger, Schaffer & Arkin, J. Virol. 77:10028 (2003), "
                   "Fig. 2b",
                   "Fixed D = 0.4; P = 10, 30, 50.",
                   show_caption=True)
    d.foot(s, "D has an optimum. P has a direction.")
    d.notes(s,
           "Same model, same axes, the other knob. P at ten, thirty and "
           "fifty with D held at 0.4.\n "
           "This one is monotone. More packaging advantage lowers the set "
           "point further and gets there faster. No valley, no oscillation, "
           "no penalty.\n "
           "So the two knobs do not behave alike, and the reason is "
           "structural: P appears only in the vector's own production term, "
           "while D appears in both. A knob that is in one place is a "
           "direction. A knob that is in two places is a trade.\n "
           "That also explains the abstract's recommendation — push "
           "packaging efficiency hard and downregulate only moderately. "
           "Which is a strange thing to tell a drug developer, and it is "
           "correct in this architecture.")


def _s4_poll(d):
    s = d.light()
    d.header(s, "segment 4", "pose — three minutes on your own paper, then vote")
    d.title(s, "You improve the cargo tenfold")
    d.rows(s, [
        ("what you have", "a construct at P = 5 in a patient with "
                          "R_{0} = 1.9375, currently running at D = 0.2"),
        ("what you do", "you engineer a better antiviral gene. It now "
                        "suppresses HIV-1 production ten times harder, so "
                        "D goes from 0.2 to 0.02.", AMBER),
        ("the question", "Does the therapy still spread? Work out R_{0}^{T} "
                         "before and after."),
    ], top=2.06, label_w=2.3)
    d.foot(s, "P is pinned at 5 for a reason — with P unspecified both "
              "answers are defensible.")
    d.notes(s,
           "Before: R0_T is 0.4839 times P squared times D, so 0.4839 times "
           "25 times 0.2, which is 2.42. Above one — it spreads.\n "
           "After: 0.4839 times 25 times 0.02, which is 0.242. Below one — "
           "it dies out.\n "
           "So a tenfold better drug takes a working therapy and kills it. "
           "The drug got ten times better and the therapy stopped "
           "existing.\n "
           "P is pinned on the stem deliberately. At P = 30 the same "
           "tenfold improvement leaves R0_T at 8.7 and the therapy is fine, "
           "so without a stated P both 'it still works' and 'it dies' are "
           "correct and the room argues about the question instead of the "
           "biology.")


def _s4_poll_debrief(d):
    s = d.light()
    d.header(s, "segment 4", "debrief")
    d.title(s, "A tenfold better drug kills this therapy")
    d.rows(s, [
        ("before", "R_{0}^{T} = 0.4839 × 25 × 0.2 = 2.42   —   above one, it "
                   "spreads"),
        ("after", "R_{0}^{T} = 0.4839 × 25 × 0.02 = 0.242   —   below one, it "
                  "dies out", AMBER),
        ("so", "a tenfold better drug destroyed a working therapy, and "
               "nothing about the drug got worse"),
        ("and at P = 30", "the same improvement leaves R_{0}^{T} at 8.7 and the "
                          "therapy is fine. The trade is between the two "
                          "knobs, not a property of the cargo alone."),
    ], top=1.94, label_w=2.0)
    d.notes(s,
           "I take the two numbers from the room and put them up.\n "
           "The sentence I want said out loud is that nothing about the drug "
           "got worse. It got better at the only thing it was designed to "
           "do, and the therapy died.\n "
           "The last row stops this being a slogan. At a high enough "
           "packaging advantage the same improvement is harmless. So this is "
           "not 'better drugs are bad'. It is that in this architecture the "
           "two knobs are coupled, and you cannot set one without knowing "
           "the other.")


def _s4_build_burst(d):
    s = d.light()
    d.header(s, "segment 4", "build — what the model asks the cell to do")
    d.title(s, "The binomial does not fix how many")
    d.image_centered(s, FIG + "s25_burst_ledger.png", top=1.76, band=4.20)
    d.foot(s, "Weinberger does not partition a burst, it MULTIPLIES one: "
              "one I_{D} cell releases D·n virus, P²·D·n vector and "
              "2P·D·n heterozygotes — (1+P)²·D·n in all.")
    d.notes(s,
           "This is the session's best wrong turn and the paper walks into "
           "it with its eyes open.\n "
           "The binomial is the right calculation for WHICH genotype a "
           "particle is. It is not a calculation about how many particles "
           "there are, and equations three and six quietly swap one for the "
           "other: output scales as one plus P, squared.\n "
           "Put the headline design point in — P = 100, D = 0.4 — and one "
           "dually infected cell has to release eight hundred and sixteen "
           "thousand virions. That is the red dot.\n "
           "Against what? Two hundred in vivo, from Haase, which is the n in "
           "Table 1. Three to five times that under CD8 depletion in "
           "macaques. And up to forty thousand for an env-deleted SIV, which "
           "the paper attributes to unpublished data. So the headline point "
           "needs about four thousand times the measured burst and twenty "
           "times the most extreme number the paper can cite anywhere.")


def _s4_build_assumption(d):
    s = d.light()
    d.header(s, "segment 4", "build — what the paper says about that")
    d.title(s, "The assumption is never bounded")
    d.rows(s, [
        ("journal 10029", "the introduction: the burst size of "
                          "therapy-producing cells must exceed that of "
                          "HIV-1-infected cells, packaging resources are "
                          "taken not to be limiting, and the study "
                          "“highlights the need to determine” the maximum "
                          "viral output and whether Gag-Pol is limiting"),
        ("journal 10031", "the Theory section — the same paragraph that "
                          "supplies 200, “3 to 5 times more”, and 40,000"),
        ("journal 10035", "the discussion: “our model assumes that the "
                          "I_{D} cell burst size is greater than n”"),
        ("so the claim is narrow", "the paper never says HOW MUCH greater, "
                                   "and never sets its own ceiling of "
                                   "40,000 against the 816,080 its "
                                   "equations demand", AMBER),
    ], top=1.84, label_w=2.4)
    d.foot(s, "The abstract and the Fig. 3b caption carry none of it.")
    d.notes(s,
           "I want to be exact about what is wrong here, because the "
           "tempting version is wrong.\n "
           "The paper does not hide this. It states the assumption three "
           "separate times and I can give you the page for each. It even "
           "names the two experiments that would settle it.\n "
           "What it never does is put a number on it. Nowhere does it say "
           "how much greater than n, and nowhere does it set its own "
           "best-case forty thousand against the eight hundred thousand its "
           "own equations require at the design point it recommends.\n "
           "That is a different and much more common failure than hiding "
           "something, and it is worth being able to name. An assumption "
           "stated is not an assumption bounded.")


def _s4_build_capped(d):
    s = d.light()
    d.header(s, "segment 4", "build — the other model of the same cell")
    d.title(s, "Cap the burst and D leaves the vector's output")
    d.image_centered(s, FIG + "s25_burst_capped.png", top=1.80, band=4.16)
    d.foot(s, "Suppose the cell makes n particles whatever happens. The "
              "binomial still fixes the composition — 196 of 200 at P = 100 "
              "— and the count carries no D at all.")
    d.notes(s,
           "Same cell, same binomial, one different assumption: packaging "
           "resources ARE limited, so the cell makes about n particles "
           "however hard the cargo pushes.\n "
           "The composition is unchanged — at P = 100 the binomial still "
           "says 196 of the 200 are vector, about four are heterozygotes and "
           "roughly one virus particle per fifty dually infected cells.\n "
           "But look at the teal line. It is flat in D. Under a cap, D does "
           "not appear in the vector's output AT ALL. The shared production "
           "term that makes the payload the vector's own fitness is simply "
           "gone, and move four's own title is false in this model.\n "
           "That is why I keep saying 'in this architecture'. This is not a "
           "caveat I am adding for politeness. It is a second model of the "
           "same cell with the opposite conclusion, and it is in the library "
           "with a test asserting that the vector's output does not move "
           "when D does.")


def _s4_build_capped_number(d):
    s = d.light()
    d.header(s, "segment 4", "build — and the capped model has a number")
    d.title(s, "Under a capped burst the therapy never invades")
    d.rows(s, [
        ("run the same construction", "the same next-generation argument on "
                                      "the capped model gives "
                                      "R_{0}^{T} = [P²/(1+P)²] · D · (1 − 1/R_{0})"),
        ("and P²/(1+P)² < 1 always", "while D ≤ 1, so R_{0}^{T} < 1 − 1/R_{0} = "
                                     "15/31 = 0.4839 for EVERY P and every "
                                     "D", AMBER),
        ("the bound holds either way", "apply the inhibition before the cap "
                                       "and D survives in the expression; "
                                       "let the cell make n whatever happens "
                                       "and D drops out. The supremum is "
                                       "15/31 in both."),
        ("so", "the burst-size assumption is not bookkeeping. It is the "
               "difference between a therapy that invades and one that "
               "cannot."),
    ], top=1.86, label_w=3.0)
    d.foot(s, "Confirmed on the full Jacobian out to P = 10⁶.")
    d.notes(s,
           "The limiting case stops being a worry and becomes an "
           "inequality.\n "
           "P squared over one plus P, all squared, is always less than one "
           "— it approaches one from below as P grows. Multiply by a D that "
           "is at most one and by fifteen thirty-firsts, and the whole thing "
           "is capped at 0.4839. It can never reach one.\n "
           "So under a capped burst this therapy does not invade slowly. It "
           "does not invade at all, at any setting of either knob.\n "
           "And it does not matter how you write the cap. Both readings give "
           "the same bound, because the binding constraint is the "
           "composition factor rather than the drug.\n "
           "That is the whole of this segment in one line: everything "
           "depends on a quantity nobody has measured.")


def _s4_build_evidence(d):
    s = d.light()
    d.header(s, "segment 4", "build — which model does the evidence favor")
    d.title(s, "The one direct measurement favors the cap")
    d.rows(s, [
        ("what exists",
         "Weinberger cites in vitro work — ref 8, Bukovsky 1999 — "
         "finding that encapsidation resources in a dually infected cell "
         "ARE limited"),
        ("how Weinberger answers it",
         "with a mechanism rather than a measurement: in vivo, immune "
         "killing ends the cell before it reaches its ceiling, so the in "
         "vitro ceiling is not the real one", AMBER),
        ("and then names", "the two experiments that would decide it — the "
                           "maximum viral output of an infected cell, and "
                           "whether Gag-Pol is a limited intracellular "
                           "resource in vivo"),
        ("neither has been made", "so the sharper version is not “nobody "
                                  "knows”. It is: the only direct "
                                  "measurement points the other way, and "
                                  "the deciding experiment is the one the "
                                  "paper asks for."),
    ], top=1.84, label_w=2.6)
    d.notes(s,
           "I used to hand this to a room as an open question and shrug. It "
           "is sharper than a shrug.\n "
           "There is one direct measurement and it favors the capped model "
           "— encapsidation resources in a dually infected cell are limited, "
           "in vitro.\n "
           "The paper does not dispute the measurement. It argues past it "
           "with a mechanism: in a patient, the immune system kills the cell "
           "before it runs out of Gag-Pol, so the in vitro ceiling is an "
           "artifact of the dish. That is a reasonable argument and it is "
           "not evidence.\n "
           "Then it names exactly the two experiments that would settle it, "
           "and neither has been done. Being able to say that precisely — "
           "which claim rests on a measurement and which on a mechanism — is "
           "most of what reading a modeling paper well consists of.")


def _s4_build_pitchai(d):
    s = d.light()
    d.header(s, "segment 4", "build — twenty-one years later")
    d.title(s, "They built one by removing the knob")
    d.rows(s, [
        ("2024, same lab", "Nagoor Pitchai et al. built a replicating "
                           "therapeutic interfering particle whose "
                           "interference IS competition for viral Gag "
                           "polyprotein — not suppression of it"),
        ("tied to packaging", "deleting the packaging signal Ψ blunted the "
                              "interference by about 30%, so the effect "
                              "travels with the packaging competition"),
        ("our reading, not theirs", "with nothing suppressing production "
                                    "there is no D in the vector's own "
                                    "production term. The two knobs collapse "
                                    "to one, and the optimum becomes a "
                                    "maximum.", AMBER),
        ("so", "2003 finds one of its two knobs has an optimum. 2024 "
               "builds a working vector by designing that knob out."),
    ], top=1.82, bottom=5.86, label_w=2.8)
    d.sources(s, [("the TIP and the Ψ deletion",
                   "Nagoor Pitchai et al., Science 385:eadn5866 (2024)"),
                  ("the mapping onto D",
                   "ours — the 2024 paper does not frame itself this way")],
                 y=6.16)
    d.notes(s,
           "The question this segment used to hand you is answered, and the "
           "answer is no — the paradox does not survive.\n "
           "The 2003 vector SUPPRESSES production and depends on what it "
           "suppresses. The 2024 particle suppresses nothing. It competes "
           "for Gag that has already been made — the paper calls it "
           "stealing essential viral proteins.\n "
           "And they tied that to packaging experimentally: knock out the "
           "packaging signal and the interference drops by about thirty "
           "percent.\n "
           "The third row is mine and the slide says so. They never frame "
           "their construct against Weinberger's D. But if interference "
           "IS "
           "competition, there is no D in equation six, the shared term is "
           "gone, and more of your one remaining knob helps both things at "
           "once.\n "
           "The paradox was a property of the architecture, and the "
           "architecture changed. Worth noticing that the 2003 introduction "
           "leaves this door open in a parenthesis — competition for "
           "packaging resources is not ruled out and is the focus of "
           "ongoing research.")


def _s4_build_1970(d):
    s = d.light()
    d.header(s, "segment 4", "build — the oscillation was measured in 1970")
    d.title(s, "The oscillation belongs to the host cell")
    d.paper_figure(s, "huangbaltimore1970_table1", 2.92, 1.78, 7.50, 2.57,
                   "Huang & Baltimore, Nature 226:325–327 (1970), Table 1",
                   "Five undiluted passages, two cell lines.",
                   show_caption=True)
    d.rows(s, [
        ("hamster ovary", "falls to 0.0058% of passage 1 by passage 3 — then "
                          "rebounds 768-fold at passage 4", AMBER),
        ("bovine kidney", "never drops below 21%, and is back to 98% by "
                          "passage 5"),
    ], top=5.40, bottom=6.70, label_w=2.2)
    d.notes(s,
           "Nothing today is assessed on this slide. It is here because it "
           "is the best thing in the optional reading.\n "
           "Same virus, same medium, two cell lines. In hamster ovary cells "
           "the standard virus collapses to about six parts in a hundred "
           "thousand by the third passage — then comes roaring back, "
           "seven hundred and sixty-eight fold, at the fourth. In bovine "
           "kidney cells it barely moves.\n "
           "Huang and Baltimore read that as their outcome two cycling, and "
           "they are right: it is a predator-prey oscillation, measured in "
           "1970.\n "
           "Now put it beside Fig. 2a's oscillating trace. What Weinberger "
           "finds as a Hopf bifurcation in a two-knob design space was "
           "measured "
           "thirty-three years earlier — and the two cell lines say the "
           "oscillation belongs to the HOST, not to the virus. Same virus, "
           "two hosts, two completely different answers.")


def _s4_release(d):
    s = d.light()
    d.header(s, "segment 4", "pose — three minutes on your own paper")
    d.title(s, "An influenza defective interfering particle")
    d.rows(s, [
        ("the object", "influenza's genome is in eight separate segments, "
                       "and a particle has physical room for a fixed number "
                       "of them. A DI particle carries a shortened segment "
                       "in place of a full one."),
        ("the question", "Does this hour's paradox apply to it — does making "
                         "the DI particle interfere harder eventually stop "
                         "it spreading?", AMBER),
        ("say which model", "and say which of the two burst models your "
                            "answer assumes, because that is the whole "
                            "question"),
    ], top=2.00, label_w=2.2)
    d.notes(s,
           "A different object, and one where the answer is decided by the "
           "thing we just spent ten minutes on.\n "
           "Influenza's packaging cap is PHYSICAL — a particle holds eight "
           "segments and no more. So the capped model is not a hypothesis "
           "here, it is the architecture. Output is partitioned, not "
           "multiplied.\n "
           "Which means this hour's paradox does not apply in the form we "
           "derived it. A better interferer takes a larger share of a fixed "
           "number of particles. There is no shared production term for it "
           "to strangle.\n "
           "But there is a trade, and it is a different one: a DI segment "
           "spreads only in cells co-infected with a full virus, so "
           "interfering too well locally starves it of co-infections. That "
           "is a competition-for-hosts limit, not a shared-production limit, "
           "and I will take that answer happily if somebody gets there.")


def _s4_debrief(d):
    s = d.light()
    d.header(s, "segment 4", "debrief")
    d.title(s, "Influenza caps its particles by construction")
    d.rows(s, [
        ("the cap is physical", "eight segments and no more, so output is "
                                "PARTITIONED rather than multiplied. That is "
                                "the capped model by construction, not by "
                                "assumption."),
        ("so", "no shared production term, no D in the particle's own "
               "output, and this hour's paradox does not arise in the form "
               "we derived it"),
        ("but a different limit does", "a DI segment replicates only where a "
                                       "full virus also is. Interfere too "
                                       "well and you run out of "
                                       "co-infections.", AMBER),
        ("the transferable part", "not the result. The METHOD: find every "
                                  "place your knob appears, and ask whether "
                                  "the thing you are helping and the thing "
                                  "you are hurting share a term."),
    ], top=1.84, label_w=3.0)
    d.notes(s,
           "Take answers first, then this.\n "
           "The thing to land is the last row. If the room leaves believing "
           "'interfering particles have an optimal potency', they have "
           "learned a fact about one lentiviral vector and mistaken it for a "
           "law.\n "
           "What transfers is the question, not the answer. Where does my "
           "knob appear? Does the thing I am helping share a term with the "
           "thing I am hurting? For Weinberger the answer is yes and you "
           "get an "
           "optimum. For influenza, for a capped burst, and for the 2024 "
           "competition TIP the answer is no and you get a maximum.\n "
           "Same specification — a reproductive ratio above one — and "
           "completely different design advice.")


# ------------------- segment 5 · the same arithmetic, a population unasked ---
def _s5_change(d):
    s = d.dark()
    d.header(s, "segment 5", "the question changes")
    d.title(s, "Everything so far has been one patient")
    d.text(s, "Now the thing you build is released into a population that "
              "never consented, and the specification is the same: a "
              "reproductive ratio greater than one.",
           M, 2.90, 9.0, 1.60, size=24, color=MINT, spacing=1.15)
    d.text(s, "What changes is WHAT TRADES AGAINST WHAT.",
           M, 4.70, 9.0, 0.70, role="emphasis", color=WHITE)
    d.notes(s,
           "A hard stop, because this is a change of question rather than "
           "the next step of an argument.\n "
           "Everything until now has been inside one patient who was given a "
           "therapy. The vector spreading between people is named in the "
           "paper as the single largest risk of the approach, and it is one "
           "sentence with no arithmetic under it.\n "
           "Noble and colleagues are that sentence with the arithmetic done, "
           "for a different organism. Same specification — something has to "
           "spread on its own — and the trade comes apart completely.\n "
           "If you leave today with only the last segment's lesson you have "
           "a fact about lentiviral vectors. This is the twenty minutes that "
           "turns it into a principle.")


def _s5_frame(d):
    s = d.light()
    # "two collisions" was the old label, when both letters were disarmed on
    # this slide. One of them is now renamed rather than disarmed, so the
    # label says what the slide does: s23's s still collides and is disarmed
    # out loud, and h is a new letter being introduced, not a collision.
    d.header(s, "segment 5", "frame — the locus, one collision, one new "
                             "letter")
    d.title(s, "The locus you met in the first segment")
    # STAGE 1 OF A TWO-STAGE SERIES, and the split is the point.
    # DESIGN 5 segment 5 assigns the locus to the FRAME and the gamete
    # probabilities to the BUILD, and one plate cannot serve both: with the
    # fan on it, this slide printed (1+h)/2 and (1-h)/2 a click before the
    # slide that reads them, and that slide then said them again as text.
    # So stage 1 is the locus and the three alleles with NO gamete chips --
    # nothing drawn is left unlabelled, so deck-bar D2 costs nothing -- and
    # stage 2 carries the germline and the fan on the next slide.
    #
    # The two stages save at an identical 9.637 x 2.806 in and differ only
    # in columns 887-1518: zero differing pixels left of the bracket, so the
    # locus does not move by one pixel between the clicks. Both are placed
    # at the SAME band for that reason; a series that resizes between stages
    # is the defect `series_consistency` exists to catch.
    #
    # The old dead-plate workaround here is gone: that figure carried 12.2%
    # empty below against 4.5% above and the rows were set against the
    # measured INK to dodge it. The figure closed its own dead space (now
    # 4.0% below against 4.9% above), so the rows can be set against the
    # BOX. RE-MEASURED 8 November, because the numbers that stood here were
    # wrong in the safe direction and a later builder would have trusted
    # them: the placed box runs to 4.685 and the last ink to 4.566, so
    # top=4.70 clears the drawing by 0.134in, not the 0.27 claimed before.
    # Identical on both stages -- same ink rows, 22 to 430 of 449.
    d.image_centered(s, FIG + "s25_locus_1.png", top=1.58, band=3.24)
    d.rows(s, [
        ("session 23's s", "there a burden you wanted to CUT — here one you "
                           "IMPOSE"),
        ("the new letter", "h is the HOMING EFFICIENCY — the chance a cut "
                           "in a WD germline is repaired into a drive copy "
                           "rather than into a resistant allele", AMBER),
    ], top=4.70, bottom=6.80, label_w=2.0, gap=0.06)
    d.notes(s,
           "The locus from the first segment, now with three allele classes "
           "on it. Wild type, drive, resistant — and resistant is made by "
           "the drive, which is the paper's whole point.\n "
           "Two collisions and I would rather spring both deliberately.\n "
           "Session 23's selection coefficient was a cost you wanted to get "
           "rid of. Here it is a cost you are choosing to carry, and the "
           "construct spreads regardless. Same letter, opposite sign on what "
           "you want from it.\n "
           "And the letters. Noble writes the homing efficiency P, which is "
           "this hour's packaging advantage, so on our slides it is h — the "
           "rename is in docs/symbols.md and the invasion boundary goes with "
           "it. His allele names stay his: I say the drive allele and the "
           "resistant allele, and I write the pairs, WD and DR, so a letter "
           "never sits where a number should. His own crops still carry his "
           "P — this plate says so in its own footer, and the first crop "
           "slide says it again in body type, which is where it counts.")


def _s5_build_super_mendelian(d):
    s = d.light()
    d.header(s, "segment 5", "build — super-Mendelian inheritance")
    # THE TITLE STATES THE MECHANISM AND NOT THE TRANSMISSION RESULT, which
    # is deliberate and is what keeps deck-bar F3 intact across the split
    # below. An allele that has been cut cannot be inherited whatever the
    # homing efficiency is; "no wild-type gamete from a WD heterozygote" is
    # true only while every cut lands, and that condition is row 1 of this
    # slide and the title of the next one.
    d.title(s, "An allele the drive cuts is never passed on")
    # STAGE 2 OF THE SERIES, ON THE SLIDE THAT READS IT. DESIGN 5 segment 5
    # assigns the BUILD row "super-Mendelian inheritance, with the gamete
    # probabilities the plate prints", so this is stage 2's home: the same
    # locus as the frame slide, now with the germline bracket and the gamete
    # fan carrying (1+h)/2, (1-h)/2 and the struck W gamete.
    #
    # SAME top AND band AS THE FRAME SLIDE, AND THAT IS NOT A STYLE CHOICE.
    # The two stages save at an identical 9.638 x 2.806 in and differ only in
    # columns 887-1518, so placed identically the locus does not move by one
    # pixel between the clicks. A series that resizes between stages is the
    # defect `series_consistency` exists to catch.
    #
    # MEASURED, 8 November: aspect 3.434, so WIDTH binds at max_w 10.2 and
    # the figure renders 10.200 x 2.970 at y = 1.715, bottom edge 4.685.
    # `slide_fit` does not compare an image with the text under it
    # (deck-bar D5c, found on this very session), so that edge is computed
    # here rather than waited for: the row stack starts at 4.70, the plate's
    # last ink is at 4.566, and the two clear each other by 0.134in.
    d.image_centered(s, FIG + "s25_locus_2.png", top=1.58, band=3.24)
    # TWO ROWS, BECAUSE THE PLATE SAYS THE REST. This slide and the next one
    # were a single four-row slide until 8 November. It did not fit -- the
    # row stack needed 4.33 in in the 1.80 in left beside the figure -- and
    # it was also two moves on one click: rows 1-2 are the mechanism, rows
    # 3-4 are the caveat. Splitting on that seam is what the content wanted
    # anyway (deck-bar C1: a load-bearing slide is a build, not a wall of
    # text), and the figure then fits what remains.
    #
    # ROW 2 DOES NOT ENUMERATE THE GAMETE PROBABILITIES ANY MORE. It used to
    # spell out "the drive gamete is (1+h)/2, the resistant one (1-h)/2,
    # and wild type never", because there was no plate on the slide. The
    # plate prints both halves on the gametes themselves, so reading them
    # back in text is the verbal redundancy lecture-design 5 scores at
    # g = 0.06. What a drawing cannot say is what the MISSING entry means,
    # so that is the row: (1+h)/2 > 1/2 for every h above zero, so the zero
    # over-transmits the drive at any homing efficiency, and h sets only how
    # fast. The per-cut probabilities h and 1-h stay in row 1, where they
    # are the repair outcome and not a gamete frequency -- the plate does
    # not print those, and keeping them apart is the per-cut-versus-per-
    # gamete distinction the note carries.
    d.rows(s, [
        ("the assumption", "the drive INVARIABLY cuts the wild-type allele "
                           "in a WD germline. Only the repair is in "
                           "question, and PER CUT it is a drive copy with "
                           "probability h or a resistant allele with "
                           "1 − h."),
        ("the missing entry", "a WD heterozygote holds a wild-type allele "
                              "and sends on none. Transmission stops being a "
                              "fair coin: the drive is in MORE than half the "
                              "gametes for any h above zero. That is "
                              "super-Mendelian.", AMBER),
    ], top=4.70, bottom=6.80, label_w=2.4, gap=0.06)
    d.notes(s,
           "A normal heterozygote sends each allele on half the time. A "
           "drive heterozygote sends on no wild type at all, because the "
           "drive cut it — the only question is whether the repair made "
           "another drive copy or a resistant allele.\n "
           "The halves on the figure come from that cut. The drive gamete is "
           "one half plus h over two: half of it is the copy the germline "
           "already had, and half is the cut one when the repair copies the "
           "drive. The resistant gamete is the other half of the cut, "
           "(1 − h) over two. Per cut the chance is h; per gamete it is "
           "(1 + h) over two, and those are not the same number.\n "
           "That zero in the gamete table IS super-Mendelian inheritance. It "
           "is not a new mechanism; it is an entry that is missing.\n "
           "And the zero does not depend on h at all. One plus h over two is "
           "above one half for every h above zero, so transmission favors "
           "the drive even when the homing is poor — what h buys is how "
           "fast. Whether that beats the fitness cost is the invasion "
           "condition, and that comes later in this segment.")


def _s5_build_idealisation(d):
    # F3/F4: the condition travels WITH the result, on the slide that
    # states it. The result -- no wild-type gamete from a WD heterozygote --
    # is on the slide before this one, and the condition it rests on is
    # stated there too, as that slide's first row ("INVARIABLY") and in a
    # title that claims only what a cut allele cannot do. This slide is
    # where the condition is named in a title and measured against Noble's
    # own appendix, which runs 14% to 100%. So the condition arrives with
    # its result and is then held one click, rather than arriving three
    # slides later, which is what F3 forbids.
    s = d.light()
    d.header(s, "segment 5", "build — the assumption the table rests on")
    d.title(s, "Noble assumes every cut happens")
    # THE IDEALISATION ROW NAMES THE TABLE IT QUALIFIES, in words rather
    # than by position:
    # "the table only looks like that because every cut happens". Without
    # that clause the split would relocate the condition instead of keeping
    # it, which is the defect deck-bar F2 names for symbols and F3 for
    # conditions. The slide after this one carries it one click further in
    # its foot -- "All of it assumes the drive cuts every time."
    d.rows(s, [
        ("it is an IDEALISATION", "the table only looks like that because "
                                  "every cut happens. The homing "
                                  "efficiencies in Noble’s own appendix "
                                  "run from 14% to 100%, and real "
                                  "constructs do leave wild type behind."),
        # CORRECTED 8 November, and the correction is the point of the
        # slide. This row used to read "every assumption in the paper is
        # chosen to be worst-case FOR the drive ... So every number is a
        # lower bound by construction." NUMBERS 6b-i: that generalizes
        # Noble's argument past where Noble makes it. Every worst-case
        # claim in the paper is scoped to ONE named assumption (the
        # fitness ordering p.4, neutral resistance p.19, zero inbreeding
        # depression pp.6/18), always-cuts is not among them -- it is
        # justified by "Consistent with experiments" -- and the phrase
        # "lower bound" does not occur in the paper at all.
        ("why they do it anyway", "the OTHER assumptions are stacked "
                                  "against the drive — resistance is free, "
                                  "the cost is dominant. This one runs FOR "
                                  "it, so the numbers are a floor INSIDE "
                                  "the idealisation, not across it."),
        # NUMBERS 6b-i's MAY list. Note what this row must NOT say: the
        # appendix counts drive alleles only (T and D, two counts) and
        # classifies no non-drive allele, so "Noble counts uncut wild type
        # as resistant" is false about the paper. The pooling is the
        # MODEL's, one step later, where (1-h)/2 takes the whole remainder.
        ("and h is a CONDITIONAL", "h is the repair outcome GIVEN a cut. A "
                                   "germline that never cuts has no slot in "
                                   "this model at all — so the appendix "
                                   "numbers and this h agree only while "
                                   "every cut lands.", AMBER),
    ], top=2.50, bottom=6.10, label_w=3.0)
    d.notes(s,
           "The gamete table only looks like that because every cut lands, "
           "and I say so here rather than letting them find it out later. "
           "Their own appendix has homing efficiencies as low as fourteen "
           "percent, and a construct that misses leaves wild type in the "
           "gametes.\n "
           "Their defense: every other assumption in the paper is stacked "
           "AGAINST the drive. Resistance costs nothing, the drive’s own "
           "cost is dominant.\n "
           "This one is not, and that is the sharp bit. Perfect cutting runs "
           "FOR the drive. So a floor inside the idealisation is not a floor "
           "across it, and the words lower bound do not appear anywhere in "
           "the paper.\n "
           "And h is a conditional: the repair outcome given a cut. A "
           "germline that never cuts has no slot in this model at all, so "
           "the appendix numbers and this h are the same quantity only while "
           "every cut lands.\n "
           "One thing I do not say, because it is false about the paper. "
           "Noble does not count uncut wild type as resistant. Their "
           "appendix counts drive alleles against alleles at risk, two "
           "numbers, and types nothing else. The pooling happens a step "
           "later, in the model, where one minus h over two takes the whole "
           "remainder.")


def _s5_build_f(d):
    # THE OTHER GRADED LINE. The next slide prints the boundary f > 1/(1+h)
    # and f is glossed only inside Noble's own axis label at about 7 px.
    # The gamete fan on the super-Mendelian slide already gives (1+h)/2, so
    # this run adds one letter and one comparison.
    d.derivation(
        None, "segment 5", "build  ·  one letter, then the condition",
        "A drive spreads when the bias beats the cost",
        [
            ("f, the one new letter",
             "f = a WD heterozygote’s fitness, relative to wild type",
             "it is a COST: f < 1 means carrying the drive is expensive. "
             "Noble’s axis calls it DW fitness"),
            ("what a WD parent sends on",
             "the drive is in (1+h)/2 of its gametes",
             "the gamete fan, earlier in this segment. A wild-type "
             "allele goes to exactly half"),
            ("bias against cost",
             "f × (1+h)/2   against   1 × 1/2",
             "one rare drive allele against one wild-type allele, each "
             "carried by its own parent"),
        ],
        closing="f(1 + h) > 1, that is f > 1/(1 + h)  ·  at h = 0.14 the "
                "drive needs f > 0.877",
        note="One new letter in the last twenty minutes, and then the "
             "condition falls out.\n "
             "f is a cost, not a benefit. It is how well a drive carrier "
             "does against a wild-type individual, so f below one is the "
             "normal case — you have put a nuclease and a cargo into the "
             "organism and it is carrying them around.\n "
             "The transmission side we already have. A WD heterozygote "
             "sends the drive to one plus h over two of its gametes instead "
             "of a half. That is the whole of super-Mendelian "
             "inheritance.\n "
             "So a rare drive allele passes on f times one plus h over two, "
             "and the wild-type allele it is competing with passes on a "
             "half. Divide one by the other and the halves go.\n "
             "f times one plus h greater than one. The bias has to beat the "
             "cost, and nothing in it depends on how common the drive is — "
             "which is why this is an INVASION condition, about a drive "
             "that is still rare.\n "
             "At a homing efficiency of fourteen percent that asks for f "
             "above 0.877. Keep that number for the next slide.")


def _s5_build_invasion(d):
    s = d.light()
    d.header(s, "segment 5", "build — what resistance does not stop")
    d.title(s, "Resistance does not prevent invasion")
    # THE BRIDGE TO A PUBLISHED FIGURE, in body type and said once. Noble's
    # own axis says P; this hour's P is the packaging advantage and is
    # autograded on two techniques, so the homing efficiency is h everywhere
    # we write it (docs/symbols.md). His figure is not relabelled, so the
    # slide carrying the first crop says which letter is whose -- and it says
    # it at the content floor, because deck-bar B1 counts a symbol settled
    # only in a foot or a note as unsettled and the foot renders at caption
    # size. The crop moves right to open the column; the boundary and the one
    # number that rides on it now live in that column instead of the foot.
    d.paper_figure(s, "noble2018_fig1b", 8.83, 1.70, 3.00, 3.30,
                   "Noble, Adlam, Church, Esvelt & Nowak, eLife 7:e33423 "
                   "(2018), Fig. 1B",
                   "f against homing efficiency.",
                   show_caption=True)
    d.rows(s, [
        ("the letter on his axis", "Noble prints the homing efficiency P. In "
                                   "this hour P is the packaging advantage, "
                                   "so we write it h. The figure is his; the "
                                   "letter is ours."),
        ("the boundary", "f > 1/(1+h). At h = 0.14 that is f > 0.877, and "
                         "Noble's own f = 0.9 clears it by 2.3 points — the "
                         "window is narrow, not absent.", AMBER),
    ], top=1.80, bottom=6.40, right=7.70, side=False)
    d.foot(s, "All of it assumes the drive cuts every time.")
    d.notes(s,
           "A drive is initially favored if its fitness times one plus the "
           "homing efficiency exceeds one. That is the shaded region, and "
           "the vertical lines are every published construct.\n "
           "They are all far inside it. Yeast at essentially a hundred "
           "percent, fruit flies in the fifties and sixties, mosquitoes in "
           "the eighties and nineties.\n "
           "The interesting line is the one at fourteen percent — the female "
           "arm of a mosquito construct whose male arm is ninety-eight. A "
           "sevenfold sex difference in the same construct, and the paper's "
           "own headline range of 0.37 to 0.99 quietly drops it.\n "
           "And it is not the exception it looks like. The condition at "
           "h = 0.14 is f above 0.877, and their f is 0.9 — so it clears by "
           "2.3 points. The window is narrow, not absent. Worth saying "
           "because the eye reads that line as a counterexample.")


def _s5_build_release_size(d):
    s = d.light()
    d.header(s, "segment 5", "build — how many organisms it takes")
    d.title(s, "Two organisms is enough at 90% homing")
    d.paper_figure(s, "noble2018_fig1f", 4.11, 1.70, 5.11, 3.70,
                   "Noble, Adlam, Church, Esvelt & Nowak, eLife 7:e33423 "
                   "(2018), Fig. 1F",
                   "Homing 0.9, 0.5, 0.15. N = 500.",
                   show_caption=True)
    d.foot(s, "Read the homing efficiency off the legend: the three curves "
              "differ a hundredfold at a release of two.")
    d.notes(s,
           "Read the top curve, which is ninety percent homing. One organism "
           "released gives a median peak drive of essentially zero — about "
           "half a percent. TWO organisms gives about 0.895.\n "
           "Everything after two is flat. The paper's own summary is that "
           "ten individuals nearly guarantees invasion.\n "
           "I insist on the homing efficiency being read off the legend "
           "every time, because the three curves are two orders of magnitude "
           "apart at a release of two. At fifty percent, two organisms give "
           "about 0.285; at fifteen percent, about one percent. Quoting '0.9 "
           "at a release of two' without saying which column is meaningless.\n "
           "The distributions behind these medians are bimodal — the drive "
           "either drifts to extinction early or goes most of the way. There "
           "is not much middle.")


def _s5_build_containment(d):
    s = d.light()
    d.header(s, "segment 5", "build — what decides containment")
    d.title(s, "Containment is a property of gene flow")
    d.paper_figure(s, "noble2018_fig2d", 4.78, 1.70, 3.78, 3.15,
                   "Noble, Adlam, Church, Esvelt & Nowak, eLife 7:e33423 "
                   "(2018), Fig. 2D",
                   "Five demes of 100; 15 drives into one.",
                   show_caption=True)
    d.foot(s, "A cliff in migration rate near 10⁻³, nearly independent of "
              "homing efficiency above about 0.3.")
    d.notes(s,
           "Escape here is a defined thing: the drive reaching ten percent "
           "in a subpopulation other than the one it was released into. "
           "They call the cutoff arbitrary and it is.\n "
           "The shape is the result. There is a vertical cliff in migration "
           "rate at around ten to the minus three, and above a homing "
           "efficiency of about 0.3 the cliff barely moves. So what decides "
           "whether a drive escapes is the migration rate, not how good your "
           "construct is.\n "
           "Put a number on ten to the minus three. With five hundred "
           "individuals that is one migration event every two generations. "
           "One mosquito every two generations.\n "
           "The consequence for design is uncomfortable and it is the point "
           "of the paper. You cannot make a self-propagating drive "
           "field-testable by making it less efficient. Containment is a "
           "property of the landscape, and they recommend molecular "
           "confinement — a split drive, or a synthetic target site — "
           "instead.")


def _s5_build_exhaust(d):
    s = d.light()
    d.header(s, "segment 5", "build — what the drive leaves behind")
    d.title(s, "The resistant alleles are the drive's own exhaust")
    d.rows(s, [
        ("where resistance comes from", "the drive makes it, at rate 1 − h "
                                        "per cut, out of wild-type alleles "
                                        "the drive has already destroyed"),
        ("so in both cases", "the drive on average irreversibly ALTERS "
                                  "A MAJORITY of the population — either by "
                                  "the drive spreading, or by "
                                  "drive-created resistant alleles "
                                  "spreading", AMBER),
        ("which means", "resistance is not a containment mechanism. It is a "
                        "second engineered sequence loose in a wild "
                        "population, and it is the one that wins."),
        ("standing variation", "pre-existing resistance above 0.5 frequency "
                               "is needed to hold peak drive under 10%. "
                               "Measured resistance in flour beetles ranges "
                               "0 to 0.375, averaging about 0.1."),
    ], top=1.82, label_w=3.0)
    d.notes(s,
           "This is the clause a session must not drop, and it is easy to "
           "drop because it sounds like a technicality.\n "
           "People reach for resistance as the reassuring part — resistance "
           "evolves, so the drive will not fix, so it is fine. Follow where "
           "the resistant alleles come from. The drive cuts the wild-type "
           "allele and the repair fails to copy the drive. So the drive "
           "manufactured them, out of the wild-type alleles it destroyed.\n "
           "Which is why the paper says a majority of the population is "
           "irreversibly altered either way. If the drive spreads, "
           "the drive altered it. If resistance spreads instead, the drive "
           "still altered it — a wild-type allele that has been cut and "
           "repaired is not wild type any more.\n "
           "The last row kills the other hope. You would need pre-existing "
           "resistance at half the population; the one real measurement "
           "averages a tenth.")


def _s5_build_title(d):
    s = d.light()
    d.header(s, "segment 5", "build — where today's title earns itself")
    d.title(s, "The trade belongs to the architecture")
    d.rows(s, [
        ("Weinberger's vector", "the payload D and the vector's own fitness "
                                "are ONE quantity — D sits in equation [6] "
                                "as well as [3]. So there is an optimum, and "
                                "a better drug can kill the therapy."),
        ("Noble's drive", "the homing bias and the fitness cost are TWO "
                          "separate quantities, and the invasion condition "
                          "f(1 + h) > 1 multiplies them. A costlier cargo "
                          "does not reduce the homing bias.", AMBER),
        ("so the specification is the same", "something has to spread on its "
                                             "own, which is a reproductive "
                                             "ratio above one"),
        ("and the trade is not", "what trades against what is a property of "
                                 "the ARCHITECTURE, not of the idea. That is "
                                 "the sentence to leave with."),
    ], top=1.84, label_w=3.0)
    d.notes(s,
           "This is why segment five is not an appendix.\n "
           "In the vector, the thing that makes it therapeutic and the thing "
           "that makes it spread are the same number. Turn one up and the "
           "other goes down. That is an optimum.\n "
           "In a drive they come apart. The cargo's cost and the homing bias "
           "are separate quantities that multiply in the invasion condition. "
           "Making the cargo more burdensome lowers f; it does nothing to h. "
           "So you can pay for a more expensive payload with a better "
           "nuclease, which is a trade Weinberger's vector cannot make at "
           "all.\n "
           "Same specification, completely different design advice. A "
           "student who leaves with only segment four has a fact about "
           "lentiviral vectors and thinks it is a principle, and that is the "
           "specific mistake this segment exists to prevent.")


def _s5_release(d):
    s = d.light()
    d.header(s, "segment 5", "pose — three minutes on your own paper")
    d.title(s, "A drive whose cargo HELPS the organism")
    d.rows(s, [
        ("the object", "a gene drive carrying a cargo that is beneficial to "
                       "the organism carrying it — so the drive heterozygote "
                       "is FITTER than wild type, f > 1"),
        ("question 1", "What happens to the invasion condition f(1 + h) > 1, "
                       "and what release size would it take?"),
        ("question 2", "Does that make it easier or harder to contain — and "
                       "is “beneficial” a design parameter you control?",
         AMBER),
    ], top=2.02, label_w=2.2)
    d.notes(s,
           "The invasion condition is satisfied for any positive homing "
           "efficiency, and in fact for h = 0 as well, because f alone "
           "already exceeds one. It is not a drive any more at that point — "
           "it is just a beneficial allele, and it would spread by ordinary "
           "selection.\n "
           "Release size collapses. The drive no longer needs the homing "
           "bias to overcome a cost, so it establishes from very few "
           "individuals.\n "
           "Containment gets strictly harder, and this is the answer I want. "
           "Noble's containment argument already says gene flow decides it. "
           "Now even migrants carrying no drive-specific advantage are "
           "selected for, and reducing the homing efficiency — the one "
           "molecular lever — buys nothing, because f alone does the work.\n "
           "And the second half of question two matters: beneficial to the "
           "organism is not a property you set. It depends on the "
           "environment, and an environment changes.")


def _s5_debrief(d):
    s = d.light()
    d.header(s, "segment 5", "debrief")
    d.title(s, "A beneficial cargo is the hardest one to contain")
    d.rows(s, [
        ("the condition", "f > 1 satisfies f(1 + h) > 1 for ANY homing "
                          "efficiency, including zero. It is no longer a "
                          "drive — it is a beneficial allele, and ordinary "
                          "selection spreads it."),
        ("release size", "collapses. The bias was only ever paying for a "
                         "cost, and there is no cost."),
        ("containment", "strictly harder. Lowering the homing efficiency is "
                        "the one molecular lever and it now buys nothing.",
         AMBER),
        ("and the trap", "“beneficial” is not a parameter you set. It is a "
                         "statement about an environment, and environments "
                         "change."),
    ], top=1.84, label_w=2.3)
    d.foot(s, "Noble's own recommendation is molecular confinement — a split "
              "drive, or a synthetic target site — precisely because it does "
              "not depend on the cargo.")
    d.notes(s,
           "Take answers, then this.\n "
           "The row I want argued about is the third. Most intuitions say a "
           "beneficial cargo is the safe case — it is helping, after all. It "
           "is the hardest to contain, because the only knob you own stops "
           "mattering.\n "
           "And the trap underneath it. Fitness is not a number you write "
           "into a construct. It is a relationship between an organism and "
           "an environment, and a cargo that is beneficial in this decade's "
           "environment may not be in the next.\n "
           "Which is why their recommendation is molecular rather than "
           "ecological or selective: a split drive or a synthetic target "
           "site is contained by construction, whatever the cargo turns out "
           "to be worth.")


# ------------------------------------------------------------------ close ---
def _close_ledger(d):
    s = d.light()
    d.header(s, "close", "the design ledger")
    d.title(s, "The two knobs are not symmetric")
    d.rows(s, [
        ("knobs", "P, the packaging advantage — raised by removing the "
                  "vector's splice signals, adding a transport element, or "
                  "a WPRE for mRNA half-life. Improving Ψ will likely fail. "
                  "P is intracellular and NOT the one you can measure.   ·   "
                  "D, the antiviral effect, set by the cargo gene — and it "
                  "IS measurable: HIV-1 titre in culture supernatant with "
                  "and without the vector. D = 1 is no inhibition."),
        ("constraints", "R_{0} of the patient's own infection   ·   diploidy: "
                        "two draws, not three, and the heterozygote block "
                        "that comes with the chassis   ·   n = 200 virions "
                        "per cell; c = 30 per day, so a virion lasts 0.033 "
                        "days; δ = 0.7 per day, so an infected cell lasts "
                        "1.43 days   ·   λ and d, which are the host's"),
        ("limits", "eight of them, each with the observable that tells you "
                   "you have left it — next slide", AMBER),
    ], top=1.80, label_w=2.2)
    d.notes(s,
           "Written last, as always, and in today's own symbols.\n "
           "The two knobs are not symmetric and that is the thing to carry "
           "away. P is the one that works — it enters squared — and it is "
           "intracellular, so you cannot measure it in the system you care "
           "about. D is measurable with a titre assay and it is the one that "
           "bites you if you push it.\n "
           "Note what is in constraints that people try to put in knobs. "
           "Diploidy is the chassis. Two strands per capsid is not "
           "negotiable, and the whole binomial follows from it.\n "
           "And the rates, said as rates. Delta is 0.7 per day, so the "
           "lifetime is 1.43 days. I have seen that inverted in a problem "
           "set answer and it changes every number after it.")


def _close_limits(d):
    # TWO SLIDES FOR THE CLOSE, which DESIGN.md states as a departure from
    # lecture-design 5d's "a slide, not a lecture": eight limits with their
    # observables will not meet the Dwinelle type floor on one. Each row is
    # <what breaks> -> <the measurement that tells you you have left it>,
    # because a limit without an observable is a disclaimer.
    s = d.light()
    d.header(s, "close", "the limits and their observables")
    d.title(s, "Eight places this stops being true")
    d.rows(s, [
        ("the burst size", "scales as (1+P)²Dn; the headline needs "
                           "4,080 × n  →  measure a dually infected "
                           "cell's burst", AMBER),
        ("equal packaging", "and two draws, neither tested  →  "
                            "composition at a 1:P mix"),
        ("D in one shared term", "holds in THIS architecture  →  delete Ψ: "
                                 "competition blunted, suppression not"),
        ("δ′ = Dδ", "NOT a limit on the threshold, which has no δ′  →  do "
                    "I_{D} cells live longer at stronger cargo?"),
        ("the An et al. rounding", "2% at P = 100, a FACTOR OF 3 at P = 1  "
                                   "→  do heterozygotes integrate in "
                                   "primary cells?", AMBER),
        ("no virion loss", "equation [6] has no −kV_{T}T; 0.5% at n = 200  "
                           "→  is free vector depleted by binding?"),
        ("no superinfection of I_{D}", "Nef removes CD4  →  can HIV-1 "
                                       "re-enter an I_{D} cell?"),
        ("one patient", "→ vector recovered from somebody never dosed"),
    ], top=1.62, bottom=6.60, label_w=2.6, gap=0.04)
    d.notes(s,
           "Eight rows and each one names the measurement that would tell "
           "you. A limit without an observable is a disclaimer, and I am not "
           "interested in disclaimers.\n "
           "The two in amber change a number you would be marked on. The "
           "burst size decides whether the therapy invades at all. The An et "
           "al. rounding is worth a factor of three at P = 1 — largest "
           "exactly where the threshold sits, which is the uncomfortable "
           "version.\n "
           "Delta prime is on here for the opposite reason: to say it is NOT "
           "a limit on the threshold. It does not appear in R0_T at all. "
           "What it sets is the I_D population and the transient.\n "
           "If we are short I keep the burst size, the An et al. rounding "
           "and delta prime. Those three change an answer.")


def _close_sentence(d):
    s = d.light()
    d.header(s, "close", "the sentence the paper ends on")
    d.title(s, "A therapy built to spread will not stop")
    d.rows(s, [
        ("Weinberger's own words",
         "“the most significant risk of the crHIV-1 approach is the "
         "potential for crHIV-1 to be TRANSMITTED BETWEEN INDIVIDUALS. "
         "The propagation of this genetic material within the "
         "HIV-1-infected population poses significant concerns”"),
        ("Noble 2018 is that sentence", "with the arithmetic done, for a "
                                        "different organism: two organisms "
                                        "released, escape decided by gene "
                                        "flow, and a majority of the "
                                        "population irreversibly altered "
                                        "either way", AMBER),
        ("so the design question", "is not only “will it spread far "
                                   "enough”. It is “where does it stop”, "
                                   "and that has to be designed in rather "
                                   "than hoped for."),
        ("session 28 picks this up", "what limits the field, and how little "
                                     "a thing needs to carry"),
    ], top=1.82, label_w=2.8)
    d.notes(s,
           "The hinge of the hour is in the required paper, in its own "
           "words, and it is one sentence with nothing under it.\n "
           "A therapy whose entire specification is that it spreads inside a "
           "patient will also, if it is any good, spread between them. The "
           "2003 paper names that as its largest risk and says it may be "
           "worth examining.\n "
           "Noble is what happens when somebody does examine it. Different "
           "organism, same question, and the answer is that containment is "
           "a property of gene flow rather than of your construct.\n "
           "So the thing I want them to walk out with: once your "
           "specification is a reproductive ratio above one, where it STOPS "
           "is a design requirement, and it is not one you get for free by "
           "making the thing weaker.")


def _close_reading(d):
    s = d.light()
    d.header(s, "close", "what to read before Tuesday")
    d.title(s, "The reading for next time")
    d.assignment(s, y=2.10, row_h=0.80)
    d.text(s, "Today's home guide is on bCourses, answers on a separate "
              "sheet.",
           M, 1.60, W - 2 * M, 0.34, role="body", color=INK)
    d.notes(s,
           "The home guide first. The gene-drive material from the last "
           "segment is assessed there and on the final rather than on PS9, "
           "so the guide is the only place you will practise it before the "
           "exam. Answers are a separate file so you write something down "
           "before you look.\n "
           "PS9 posts today and carries the binomial partition and the "
           "reproductive-ratio calculation from the middle of the hour.\n "
           "The reading for Tuesday is a truth table implemented inside a "
           "human cell — six sensor modules and a classifier. Come able to "
           "say which input does which job, and what a false positive costs "
           "when the output is a cell-death gene.")
