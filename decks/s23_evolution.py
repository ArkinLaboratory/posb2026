"""Session 23 — Evolutionary failure and containment: burden becomes selection.

Thursday 12 November 2026. Part II, eighth session, and the rung that breaks
the ladder. Rottinghaus et al., Nature Communications 13:672 (2022) was
assigned at the close of session 22.

WHAT THIS SESSION IS. Rungs 1 to 4 were each a coupling the designer could do
something about -- measure the burden, compute the bound, insulate the
interface, reject the disturbance -- and the trajectory was increasing power.
This rung answers to none of it:

    THE GROWTH COST YOU MEASURED IN SESSION 19 IS A SELECTION COEFFICIENT.

The circuit is not perturbed. It is selected against, and the population
removes it on purpose. There is no insulation device for mutation, and
feedback cannot help, because the controller is encoded in the thing being
removed.

WHAT MAKES IT TEACHABLE RATHER THAN MERELY SOBERING is that session 19's
number is the same number read a second way. Scott 2010 gave a growth-rate
decrement; put two strains in one flask and that decrement IS a selection
coefficient. Rung 1 comes back as the thing that kills the device, and that
connection is free.

THE TURN. The hour builds a mutation-selection model, gets a real result out
of it -- failure time is logarithmic in the mutation rate and inverse in the
selection coefficient, so cutting burden beats hardening DNA whenever
s/mu > 413 -- and then does what that result demands: goes and BOUNDS the
burden, by fitting the model to Rottinghaus' own 28-day stability curve.

    Fig. 2e, fitted: best fit is s = 0 with mu = 2.63e-9 per cell per
    generation, RMS 0.151 decades. A flat line with no rise at all scores
    0.204, so the rise is barely resolved and this is an UPPER BOUND, not a
    measurement: s above about 0.02 is excluded, and s = 0.05 -- the hour's
    own reference -- misses by 1.2 decades.

So the circuit is nearly free under permissive growth, which is why it
survives 224 generations in a flask. The model is how you see that, and the
bound is how you say it honestly.

AND THEN IT RUNS OUT, WHICH IS THE REAL TURN. If the circuit is costless and
stable for a month in vitro, why did it fail in a mouse? Because nothing in
this model describes the second route. Their Fig. 6a names two: slow
replication error, which redundancy fixes, and SOS mutagenesis caused by the
device's own double-strand breaks, which redundancy cannot touch and which
the authors report appears ONLY in vivo. The device raises its own mutation
rate when operated. The model is complete for permissive growth and silent
about operation.

A WARNING FOR ANY LATER PASS. An earlier version of this deck claimed the
model was REFUTED here, using 1e-8.6 as the 28-day bound. That number is
Fig. 1h -- a different strain, with antibiotics, one timepoint. Fig. 2e is
the CRISPRks strain and it rises to 1e-6.3. Using one strain's number as
another's bound is the same defect that killed the k >= 3 argument. Check the
strain and the conditions.

AND THE THING THAT ACTUALLY MUTATES IS SOMETHING THE DESIGNER CHOSE. Over
half of all observed mutations are a 25 bp deletion across the two identical
19 bp tet operators inside Ptet. The failure is recombination between a
repeat, in a promoter they picked, duplicated across cassettes they added for
redundancy. Redundancy and repeat are the same thing. That is why mu is not a
constant of nature: it depends on the sequence you chose and on
whether the device is cutting.

NEVER PRESENT THE REFUTATION AS REFUTING ROTTINGHAUS. They propose no model.
They engineered, measured and iterated. The model that fails is the one this
room just built, which is the honest and more useful version of rule 6.

Numbers: sessions/s23-evolution/NUMBERS.md, every one tagged with its kind.
Every s in this deck is MODELLED from session 19; the paper reports no
fitness cost, and the slides say so.

Build:  python tools/build_decks.py s23_evolution
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)

FIG = "figures/build/"
FILENAME = "s23-evolution"


def build():
    d = Deck("Session 23 — Evolutionary failure and containment", session=23)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _goals(d)
    _frame(d)
    _object(d)
    _population(d)
    _fitness(d)
    _derivation(d)
    _solution(d)
    _limits(d)
    _ledger(d)
    _forward(d)
    _architecture(d)
    _redundancy(d)
    _measure(d)
    _mechanism(d)
    _requirement(d)
    _fluctuation(d)
    _retention(d)
    _competition(d)
    _target(d)
    _close(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    s = d.dark()
    d.text(s, "Session 23  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "Burden becomes selection",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "The growth cost you measured in session 19 is a selection "
              "coefficient. So a population removes your circuit on a "
              "schedule you can compute — and halving the burden beats "
              "dividing the mutation rate by a hundred.",
           M, 4.42, 8.6, 1.70, size=18, color=MINT, spacing=1.2)
    d.notes(s,
           "The title is the claim and I say it in the first sentence. The "
           "state variable today is a fraction of a population, not a "
           "concentration. The clock is generations, not minutes. And the "
           "number that drives all of it is one this room measured three "
           "weeks ago.\n "
           "I do not pose evolutionary failure as a new subject and I do not "
           "open on the kill switch. The kill switch is the object and it "
           "arrives after the claim.")


def _retrieval(d):
    s = d.light()
    d.header(s, "open", "retrieval — sessions 19, 21 and 22")
    d.title(s, "Before we start")
    d.rows(s, [
        ("1", "Session 19: your circuit occupies ten percent of the "
              "proteome. By Scott's linear laws, what happens to the growth "
              "rate — and roughly by how much?"),
        ("2", "Session 21: a downstream module read your regulator. What did "
              "that load cost you, and what could you not do about it?"),
        ("3", "Session 22: the antithetic controller rejected a disturbance "
              "it never measured. Name the one thing it still could not "
              "survive."),
        ("4", "All three of those are about one cell. What would change if "
              "the thing you cared about were a flask of ten billion of "
              "them, grown for a month?"),
    ], top=2.05, label_w=0.7)
    d.notes(s,
           "One is the number the hour runs on. Scott 2010 gives roughly two "
           "percent of growth rate per one percent of proteome diverted, so "
           "ten percent of the proteome is about a twenty percent growth "
           "decrement. I want that number spoken out loud before anything "
           "else happens.\n "
           "Two: load cost speed and, if the complex dilutes, level, and you "
           "could not lower it, because the bill is the site count.\n "
           "Three: dilution of the controller species. The integrator leaks "
           "and adaptation stops being exact.\n "
           "Four is the pivot and I take answers. The one I am steering "
           "toward is that the cells are not identical and do not stay "
           "identical. Everything in Part II so far has modeled one cell or "
           "concentrations inside one cell.")


def _goals(d):
    s = d.light()
    d.header(s, "open", "what you should be able to do by the end")
    d.title(s, "Three questions")
    d.rows(s, [
        ("the schedule", "A population deletes your circuit. What sets how "
                         "long that takes, and which of the two knobs is "
                         "the better buy?"),
        ("the measurement", "You will build a model and fit it to their data. "
                            "What does the fit tell you about the circuit, "
                            "and what is it silent about?"),
        ("the lever", "Only two of the four levers that work are circuit "
                      "design, and the second of those disappoints. Why is "
                      "that the honest conclusion rather than a defeat?"),
    ], top=2.05)
    d.notes(s,
           "I answer all three now, briefly, so the hour has somewhere to "
           "land.\n "
           "The schedule: failure time goes as the logarithm of the mutation "
           "rate and inversely with the selection coefficient. Cutting "
           "burden beats hardening DNA, and there is an exact boundary.\n "
           "The measurement: fitted to their own stability curve the model "
           "returns a burden of essentially zero, which is why the circuit "
           "lasts a month. What it is silent about is the route that only "
           "appears in a mouse.\n "
           "The lever: lower the cost, lower the rate, add redundancy, "
           "change the selection environment. Only the first is circuit "
           "design in the sense this course has meant it, and that is what "
           "sets up sessions 24 to 26.")


def _frame(d):
    s = d.light()
    d.header(s, "frame", "where this sits")
    # THE SESSIONS ARE NAMED, NOT NUMBERED AS RUNGS. "Rung" was never
    # defined on a slide anywhere in this course, and session 12 already
    # spends it on screen for a different object -- one rung per molecule
    # number in the master-equation ladder. Sessions 19, 21 and 22 all put
    # this same arc on a slide and all name the sessions; this was the last
    # place that did not. The title now carries the claim the note makes.
    d.title(s, "A controller cannot regulate its own deletion")
    d.rows(s, [
        ("session 19", "the circuit draws on shared ribosomes  →  "
                       "measure the burden"),
        ("session 20", "stoichiometry bounds the achievable flux  →  "
                       "compute the bound"),
        ("session 21", "the downstream load retroacts  →  insulate it"),
        ("session 22", "a disturbance moves the output  →  reject it, "
                       "exactly"),
        ("today", "the population deletes the circuit  →  there is no device "
                  "for this"),
    ], top=2.00, label_w=2.5)
    d.foot(s, "Feedback cannot help here: the controller is encoded in the "
              "thing being removed.")
    d.notes(s,
           "The ladder has been one trajectory, from a tax you must pay to a "
           "disturbance you can annihilate. Each cure was more powerful than "
           "the last.\n "
           "This rung answers to none of it. The circuit is not perturbed, "
           "it is selected against, and the population removes it on "
           "purpose. There is no insulation device for mutation.\n "
           "Every control "
           "strategy in session 22 assumed the controller still exists. "
           "Here the failure mode is that it stops existing, and a "
           "controller cannot regulate its own deletion.")


# --------------------------------------------------- segment 1 · the object ---
def _object(d):
    s = d.light()
    d.header(s, "segment 1", "the object, before any model")
    d.title(s, "Built almost entirely from parts you know")
    d.paper_figure(s, "rottinghaus2022_fig1a", 4.10, 1.84, 5.13, 4.05,
                   "Rottinghaus et al., Nat Commun 13:672 (2022), Fig. 1a",
                   "The single-input CRISPR kill switch.",
                   show_caption=True)

    s = d.light()
    d.header(s, "segment 1", "the object, before any model")
    d.title(s, "What Ptet is wired to")
    # FIVE ROWS, NOT THREE, AND "session 6" SPELLED OUT.
    #  - "s6" is this repo's shorthand and the room has never seen it. Every
    #    other cross-reference in this deck says "session 19", "session 22".
    #  - The gRNA row was missing. Fig. 1a on the click before this one shows
    #    TWO Ptet-driven cassettes, and slide 17 later counts four Ptet-cas9
    #    and three gRNA cassettes, so the room has to meet the gRNA here or
    #    the repeat argument at the recombination slide has nothing to count.
    #  - "cutting, not blocking" is one clause against a real collision:
    #    session 17 taught Cas9 as dCas9, a transcriptional repressor that
    #    does not cut. Same protein name, opposite action, and the whole
    #    failure mode of this hour depends on the double-strand break.
    #  - The last row puts the hour's framing question ON the slide. It was
    #    in the speaker note only, and the close ("check these against the
    #    list you made") depends on it, which made a board moment
    #    load-bearing -- lecture-design.md 5b's own release condition.
    d.rows(s, [
        ("known since session 6", "TetR, constitutively expressed, "
                                  "repressing Ptet"),
        ("known since session 6", "aTc relieves that repression"),
        ("new", "Ptet drives Cas9 — which CUTS the host's chromosome. "
                "Session 17's dCas9 blocked transcription; this one breaks "
                "DNA."),
        ("new", "Ptet also drives the gRNA, which picks the site it cuts"),
        ("your turn", "you have this strain in your hands. What could you "
                      "change about it, and what would changing each one "
                      "take?", AMBER),
    ], top=2.00, label_w=3.3)
    d.notes(s,
           "The only genuinely new thing on this slide is the word kill "
           "switch and what Ptet is wired to. TetR and aTc are the most "
           "heavily used parts in this entire course — we have been drawing "
           "this repression since session 6.\n "
           "So the construct is familiar and the framing is not. Add aTc and "
           "the cell cuts its own chromosome. The intended use is a living "
           "therapeutic you can switch off after it has done its job.\n "
           "The question I want in the room before we model anything: you "
           "have this strain in your hands. What can you change about it, "
           "and what would you have to do to change each thing?\n "
           "The list I expect: lower the burden, harden the DNA, add "
           "redundant copies, change what else is growing in the flask, "
           "change the host. I write their answers on the board and check "
           "them against the five levers at the close. The question itself "
           "is on the slide, so a student who was not here can still see "
           "what the close is checking against.")


def _population(d):
    s = d.light()
    d.header(s, "segment 1", "a change of object")
    d.title(s, "The state variable is a fraction of a population")
    d.rows(s, [
        ("every session until now", "one cell, or concentrations inside one "
                                    "cell. X, Z, flux, occupancy."),
        ("today", "q, the fraction of the population whose circuit no longer "
                  "works. A number between zero and one."),
        ("the clock", "generations, not minutes — and it comes out of the "
                      "protocol, not out of a textbook."),
    ], top=2.05, label_w=3.2)
    d.to_board(s, "250x daily dilution  →  log2(250) = 7.97 generations per "
                  "day  →  28 days = 223 generations")
    d.notes(s,
           "This is as large a change of object as the phase plane was in "
           "session 8.\n "
           "I derive the generations at the board. They diluted 250-fold "
           "every day. Each cell has to double enough times to refill the "
           "flask, so the number of doublings per passage is log base two of "
           "250, which is 7.97. Over 28 days that is 223.\n "
           "The paper says 224 generations and 112 at day 14, so they "
           "rounded to eight per day, which would be a 256-fold dilution. "
           "The gap is four tenths of a percent and I am not going to make "
           "anything of it. The point of doing the division in front of them "
           "is that generations stops being a word and becomes a unit "
           "derived from a protocol.")


# ------------------------------------------- segment 2 · fitness and s19 ---
def _fitness(d):
    s = d.light()
    d.header(s, "segment 2", "the number you already have")
    d.title(s, "The same number, read a second way")
    d.rows(s, [
        ("session 19 measured", "a growth-rate decrement — about two percent "
                                "of growth rate per one percent of proteome "
                                "diverted (Scott 2010)"),
        ("two strains, one flask", "the one carrying the circuit grows "
                                         "at (1 − s) times the other"),
        ("so s is", "the selection coefficient. It is the same number, read "
                    "a second way."),
        ("commit before the algebra", "after 200 generations at s = 0.05, "
                                      "what is the ratio of the two "
                                      "populations?"),
    ], top=2.00, label_w=3.4)
    # "wild-type GFP levels" was incoherent: wild-type E. coli has no GFP,
    # and a reporter level is not a burden readout in any case. And
    # "MODELLED, from session 19" claimed a provenance the number does not
    # have -- session 19's circuit took a tenth of the proteome and cost
    # about 20%, which is the number the room computed on the retrieval
    # slide six slides ago. 0.05 is a stipulated reference, and saying so
    # here is what stops the room reading it as session 19's answer.
    d.foot(s, "s = 0.05 is a STIPULATED reference, not session 19's 20% — "
              "that circuit took a tenth of the proteome and this one "
              "evidently does not. Rottinghaus report no fitness cost.")
    d.notes(s,
           "This is the connection the session is built on and it is free. "
           "Session 19 measured a cost to growth. A cost to growth, in a "
           "population, is a selection coefficient. Rung one comes back as "
           "the thing that kills the device.\n "
           "I take a commitment on the ratio before showing it. At s = 0.05 "
           "the broken cells outgrow the working ones by one over one minus "
           "s each generation, so over 200 generations the ratio is 0.95 to "
           "the minus 200 — about twenty-nine thousand. The room will guess "
           "low, which is "
           "the point: nobody has intuition for compounding over hundreds of "
           "generations, and that is what makes this failure mode sneak up "
           "on people.\n "
           "The foot matters and I say it out loud. Every s in this hour is "
           "ours, carried over from session 19. The paper does not report a "
           "fitness cost. Real numbers first, and name the simplified one as "
           "simplified.")


def _derivation(d):
    d.derivation(
        None, "segment 3", "build  ·  mutation against selection",
        "A schedule you can compute",
        [
            # "no longer works", NOT "dead". The device on the table is a
            # KILL SWITCH and the data axis four slides on is FRACTION
            # VIABLE, so "dead" reads as dead cells -- which is the exact
            # opposite of what q counts. Slide 7 already says "no longer
            # works"; this is that wording, kept.
            ("the broken fraction",
             # 54 rendered characters against the step row's cap of 56.
             # "no longer works" was 60 and wrapped onto its own aside.
             "q = fraction of the population whose circuit is broken",
             "these are the cells that SURVIVE induction"),
            # mu IS DEFINED HERE, where it first appears (bar B1). It had
            # no definition on any slide: it entered inside this rate, was
            # first named in words four clicks later, and its one gloss --
            # that it is a lumped whole-circuit rate -- sat in a speaker
            # note eight slides further on. Two days ago mu was session
            # 22's set-point numerator, so the glyph is not neutral either.
            ("mutation makes broken cells",
             "rate = μ (1 - q)",
             # 40 characters. The 61-character version wrapped onto the
             # step below it: theme's line_cap over-estimates what fits an
             # aside, as it does a figure caption, so this was measured in
             # the built deck rather than predicted.
             "μ = circuit loss per cell per generation"),
            ("selection multiplies them",
             "rate = s q (1 - q)",
             "working cells grow at (1 - s) times broken ones"),
            ("so the whole thing is",
             "dq/dt = (1 - q)(s q + μ)",
             "one equation, two mechanisms"),
            # THREE CLICKS, NOT ONE. The run used to spend four steps on
            # the four easy moves and then jump the only step anyone can
            # get wrong -- which teaches the room that the hard move is
            # not worth watching. The partial fractions are the move.
        ],
        note="Both terms carry (1 - q), and for opposite reasons: only a "
             "working circuit has something to lose, and only a broken one "
             "can be multiplied. This mu is LUMPED -- the rate of losing "
             "the circuit by any route, not a per-base mutation rate, and "
             "not session 22's mu.\n "
             "Mutation is a source that does not care how many broken cells "
             "there are. Selection is a multiplier that does nothing until "
             "there is something to multiply. Completely different "
             "signatures, and it is why the two design questions later in "
             "the hour have opposite answers.")


# TWO RUNS, NOT ONE OF SEVEN STEPS. Seven steps in a single run puts
# the pitch under 0.86, and below that only the live step keeps its
# aside -- which is where the definitions live. Splitting at the ODE
# is where the argument splits anyway: the first run builds the
# equation, the second solves it.
def _solution(d):
    d.derivation(
        None, "segment 3", "build  ·  and now solve it",
        "One separation, two logs, one constant",
        [
            ("the equation you just built",
             "dq/dt = (1 - q)(s q + μ)",
             "separable: all the q on one side, dt on the other"),
            ("split the fraction",
             "1/[(1-q)(sq+μ)] = [ 1/(1-q) + s/(sq+μ) ] / (s+μ)",
             "check it: the numerators add to s+μ"),
            ("integrate both sides",
             "[ -ln(1-q) + ln(sq+μ) ] / (s+μ) = t + C",
             "two logs and one constant"),
            ("q = 0 at t = 0 fixes C",
             "t(q) = ln[ (s q + μ) / (μ (1 - q)) ] / (s + μ)",
             "exact — for constant s and μ"),
        ],
        # NO CLOSING BOX. It restated the line standing immediately above
        # it, and its height is part of what pushes a run under the pitch
        # that lets every step keep its aside -- which is where the
        # definitions live. A duplicate was costing the definitions.
        note="The partial fractions are the step worth watching and I do "
             "not hurry it. The two numerators have to add to s + μ; that "
             "is the check, and I ask for it out loud.\n "
             "The constant is the other thing people drop. q is zero at "
             "t = zero — no broken circuits at the start — and that is what "
             "turns two indefinite integrals into a formula you can put a "
             "number into.\n "
             "What exact does NOT mean: it assumes s and μ are constants, "
             "one well-mixed population, and no way back from broken to "
             "working. Every one of those is false somewhere later in the "
             "hour, and segment four is where the first one goes.")


def _limits(d):
    s = d.light()
    d.header(s, "segment 3", "the two limits")
    d.title(s, "No cost is accumulation. A cost is a race.")
    d.rows(s, [
        ("s = 0, no burden at all", "q = 1 − exp(−μ t),  and the half-life "
                                    "is ln2 / μ. Pure accumulation; nothing "
                                    "is amplifying anything."),
        ("μ much less than s", "t₅₀ ≈ ln(s / μ) / s. The mutation rate is "
                                "inside a logarithm. The selection "
                                "coefficient is not."),
        ("which is the whole design consequence", "failure time is "
                                                  "LOGARITHMIC in the "
                                                  "mutation rate and INVERSE "
                                                  "in the cost."),
    ], top=2.05, label_w=3.4)
    d.notes(s,
           "The second limit is the one that changes what a designer does, "
           "and I want them to see why before they see the numbers.\n "
           "Mutation is inside a logarithm because it only has to happen "
           "once — it seeds the thing. Selection is in the denominator "
           "because it acts every generation on everything already there. "
           "Dividing the seeding rate by a hundred moves a logarithm by "
           "about 4.6. Halving the growth advantage doubles a denominator.\n "
           "So the asymmetry is not a numerical accident, it is structural. "
           "Picture first, then the price.")

    # THE SHAPE, BEFORE THE PRICE. The rows above are the algebra and the
    # ledger one click on is the money, and between them the room had
    # nothing to look at: the structural claim of the hour arrived as
    # prose on a half-empty slide and the bar chart then argued from
    # numbers to someone who had not yet seen why the two parameters
    # cannot trade. Two axes do that in one look, and the figure carries
    # no numbers so the ledger keeps its own.
    s = d.light()
    d.header(s, "segment 3", "the two limits")
    d.title(s, "The same two parameters, two different shapes")
    d.image_centered(s, FIG + "s23_two_shapes.png", top=1.80, band=4.60)
    d.foot(s, "Left: a hundredfold change in μ is one step down a straight "
              "line. Right: s in a denominator, so the cost of halving it "
              "is paid back twice over.")
    d.notes(s,
           "Same quantity on both y-axes — generations until half the "
           "population has lost the circuit.\n "
           "Left, against the mutation rate on a log axis: a straight line. "
           "That IS what logarithmic means, and it is why a hundredfold "
           "improvement in fidelity moves you one modest step.\n "
           "Right, against the burden on a linear axis: one over s. It runs "
           "away at the left-hand end, which is why halving a small burden "
           "is worth so much more than it sounds.\n "
           "I do not put numbers on this one on purpose. The next slide is "
           "the ledger and it owns the numbers; this one owns the shapes.")


def _ledger(d):
    s = d.light()
    d.header(s, "segment 3", "the result that changes what you do")
    d.title(s, "Halving the burden beats a hundredfold fidelity")
    d.image_centered(s, FIG + "s23_ledger.png", top=1.80, band=4.60)
    d.foot(s, "Boundary at s/μ = 413. But this prices BENEFIT only — the "
              "two moves are not equal effort, and later this hour μ is not "
              "a continuous dial at all.")
    d.notes(s,
           "Reference point on the left: half the population has a broken "
           "circuit after 216 generations. Dividing the mutation rate by ten "
           "buys 46 more generations, by a hundred buys 92. Halving the "
           "burden buys 189 — more than a hundredfold improvement in DNA "
           "fidelity. Cutting the burden by ten buys fifteen hundred.\n "
           "The right panel is the regime, because this is not universal. "
           "Below s over mu of 413 the ranking reverses and hardening the "
           "DNA is the better buy. We are at fifty thousand, far inside the "
           "region where burden wins.\n "
           "The boundary depends only on the ratio, and the reason is "
           "worth ten seconds. Write r for s over mu. The half-life is "
           "log of r plus two, all over mu times r plus one. The same "
           "one-over-mu sits on both sides of the comparison, so it "
           "cancels and only r survives. The root is four hundred "
           "thirteen. And take the mutation rate to zero and the root is "
           "exactly four hundred: a hundred, for the fidelity gain, times "
           "two squared, for the two factors of two in halving s. Four "
           "hundred is where the answer comes from. Four hundred thirteen "
           "is the finite-mutation-rate correction, three percent.\n "
           "And I say the caveat in the foot out loud, because a ledger that "
           "prices benefit and says nothing about cost is half an argument. "
           "Nothing here tells you what halving a burden costs in redesign, "
           "or what a hundredfold fidelity gain costs in anything. Hold that "
           "thought: later in the hour mu stops being a dial at all.")


def _forward(d):
    s = d.light()
    d.header(s, "segment 3", "the same asymmetry, run backwards")
    d.title(s, "Run it backwards and it is a search time")
    d.rows(s, [
        # NOT "finds and fixes". Fixation is a term of art this course has
        # never defined, and it is the wrong one anyway: ln(s/μ)/s is the
        # time to HALF the population, under μ much less than s. And the
        # second row re-points both symbols at different quantities, which
        # the slide now says out loud instead of leaving the room to
        # notice.
        ("what we just derived", "ln(s / μ) / s is how long a broken variant "
                                 "takes to reach half the population — when "
                                 "μ is much smaller than s."),
        ("read it the other way", "same formula, symbols re-pointed: μ the "
                                  "rate of making a BETTER variant, s the "
                                  "advantage you gave it. Same arithmetic, "
                                  "opposite intent."),
        ("the recipe", "raise μ on one locus, hold it at background "
                       "everywhere else, impose a selection you designed. "
                       "That is directed evolution."),
    ], top=2.05, label_w=3.0)
    d.coming_up(s)
    d.notes(s,
           "The asymmetry is not only a statement about losing a circuit. "
           "Crossing sequence space is the same arithmetic with the sign of "
           "your intent flipped. A mutation rate raised on one locus against "
           "a selection you chose is directed evolution, and ln(s over mu) "
           "over s read that way is a search time rather than a failure "
           "time.\n "
           "Continuous-evolution systems do this for a living, and session "
           "27 is where they turn up.")


# ------------------------- segment 4 · fit it, then find its boundary ---
def _architecture(d):
    """The object the next three slides argue about, before they argue.

    WHY THIS EXISTS. Slides on the model, the confounding plot and the vote
    all reason about "four Ptet-cas9 cassettes and three gRNA cassettes",
    and that phrase was a single line of prose. Three slides is a long time
    to reason about a structure nobody has seen (bar F1). Their own Fig. 2c
    draws it, so the deck shows theirs rather than drawing a worse one.

    AND IT SETTLES SOMETHING THE PROSE LEFT OPEN. "Three gRNA cassettes"
    could be one array with three spacers in it, which would make the gRNA
    side a single point of failure and the whole redundancy argument
    different. It is not: the paper's own caption for this panel says
    "optimized groL-2, ile-2, and rrs-2 Ptet-gRNA expression cassettes" --
    three cassettes, each behind its own Ptet. That is what makes the
    series/parallel count work, and it is also why SEVEN copies of the same
    promoter sequence are sitting in one cell, which is the whole of the
    mutation slide four clicks later.
    """
    s = d.light()
    d.header(s, "segment 4", "the object, counted")
    d.title(s, "Seven cassettes, and two ways to break the switch")
    # 6.00 x 3.95 for a 674 x 444 panel: aspect 1.518, so width is the
    # binding dimension and the slot has to be no wider than 3.95 x 1.518
    # or the bottom of the schematic goes outside the box.
    # Short ref: the ref line is as wide as the DRAWN image, not the slot,
    # and the full citation wrapped with "2c" alone on a second line. The
    # full form is on the slide where this paper is introduced.
    d.paper_figure(s, "rottinghaus2022_fig2c_map", 3.65, 1.80, 6.00, 3.95,
                   "Rottinghaus et al. 2022, Fig. 2c",
                   "The CRISPRks construct. X4 means four copies.",
                   show_caption=True)
    d.notes(s,
           "I walk this once, slowly, because the next three slides argue "
           "about it and it has only been a phrase until now.\n "
           "Top left: a Ptet promoter driving a gRNA. There are three of "
           "these, one each for groL-2, ile-2 and rrs-2 — three separate "
           "cassettes, each with its own Ptet, not one array with three "
           "spacers in it. The paper's caption for this panel says so.\n "
           "Bottom left: Ptet driving cas9, marked X4. Four copies, "
           "integrated at four neutral sites in the chromosome.\n "
           "Top right: tetR, constitutive, which is the repressor holding "
           "all seven of those Ptet promoters shut until aTc arrives.\n "
           "Bottom right in red: infA, a complement for a genomic knockout. "
           "It is their addiction module and it is not today's subject — I "
           "name it and move on.\n "
           "Then the count I want on the board: seven Ptet promoters in one "
           "cell. Hold that; it is the whole of the mutation slide later.")

    s = d.light()
    d.header(s, "segment 4", "the object, counted")
    d.title(s, "Seven cassettes, and two ways to break the switch")
    d.rows(s, [
        ("cutting needs two things", "a Cas9 to do the cutting, and a gRNA "
                                     "to say where. Lose either side "
                                     "completely and nothing is cut."),
        ("so the switch survives", "while ONE of the four cas9 copies works "
                                   "AND one of the three gRNA cassettes "
                                   "works."),
        ("and escape needs", "all four cas9 dead, OR all three gRNAs dead. "
                             "Not all seven — the two sides are in series, "
                             "the copies within a side are in parallel.",
         AMBER),
        ("which side goes first", "the one that needs fewer hits. Three "
                                  "beats four, so the gRNA side sets the "
                                  "early behavior.", AMBER),
        ("hold on to", "seven copies of the same Ptet promoter, in one "
                       "cell.", TEAL),
    ], top=2.00, label_w=3.2)
    d.foot(s, "A redundancy argument is a counting argument, and the count "
              "depends on the wiring, not on the number of parts.")
    d.notes(s,
           "This is the step the next slide's model skips, so I do it here "
           "by hand.\n "
           "Killing is an AND: Cas9 and a gRNA. So the device is dead when "
           "either side is wiped out, and the two sides are in SERIES even "
           "though the copies inside each side are in parallel. That is the "
           "same reliability picture as any redundant system — it is worth "
           "saying out loud that this is not a biology fact, it is a "
           "counting fact.\n "
           "Ask for the exponent before giving it. If each cassette is lost "
           "independently at rate mu-one, the chance all four cas9 are gone "
           "early goes as mu-one t to the fourth, all three gRNAs as "
           "mu-one t cubed, and the sum is dominated by the cube. So the "
           "early log-log slope this architecture predicts is three, not "
           "seven, and not four.\n "
           "Nobody should leave thinking seven redundant copies means "
           "seven hits. And keep the seven promoters in view: they are "
           "identical sequence, which is what recombination needs.")


def _redundancy(d):
    s = d.light()
    d.header(s, "segment 4", "the obvious next move")
    d.title(s, "The slope should tell you how many cassettes")
    d.rows(s, [
        # μ_c, NOT μ1, AND THE MODEL IS NAMED AS A DIFFERENT ONE. "μ1"
        # reads as a typo for μ and invites the room to substitute it into
        # the equation they just derived, which has selection in it and
        # one cassette. This is a per-CASSETTE rate in a selection-free
        # model, and both facts belong on the slide.
        # μ1, NOT μ_c: the home guide for this session writes μ1 and the
        # room works it on paper, so renaming the symbol here would put
        # the slide and the handout in two alphabets (bar B2). What was
        # missing was never the letter, it was the definition and the
        # fact that this model has no selection in it.
        ("k independent cassettes", "each still intact with probability "
                                    "exp(−μ1 t), where μ1 is the loss rate "
                                    "for ONE cassette; escape needs all k "
                                    "broken"),
        ("so, with no selection at all", "q(t) = (1 − exp(−μ1 t))^k  ≈  "
                                         "(μ1 t)^k  for small t"),
        ("which means", "on log–log axes the slope IS k. Measure the slope, "
                        "read off the architecture."),
        # The series/parallel count is taught on its own slides now, with
        # their Fig. 2c on the screen, so this row points back rather than
        # repeating the argument in a row box.
        ("and they did build redundancy", "the seven cassettes we just "
                                          "counted — so this model's k is "
                                          "three, from the gRNA side."),
    ], top=2.05, label_w=3.2)
    d.foot(s, "With no selection the log–log slope is k. With selection "
              "it is not.")
    d.notes(s,
           "I build this honestly and I let the room want it, because it is "
           "genuinely the obvious thing to do and because the slides that "
           "follow take it away.\n "
           "The algebra is right. If k cassettes fail independently then the "
           "escape fraction really does go as t to the k at early times, and "
           "the log-log slope really is k when there is no selection.\n "
           "Fitting that slope to their data gives k of at least three. That "
           "inference does not hold, and the next slides are why.")


def _measure(d):
    s = d.light()
    d.header(s, "segment 4", "what 28 days looks like")
    d.title(s, "Their stability curve is not a floor. It rises.")
    # Portrait panel, so the band's height is the binding constraint and
    # the slide is going to have white on both sides. Take the full height
    # anyway: at the old 1.92in the tick labels projected at about 10pt.
    d.paper_figure(s, "rottinghaus2022_fig2e", 5.20, 1.78, 2.93, 3.88,
                   "Rottinghaus et al., Nat Commun 13:672 (2022), Fig. 2e",
                   "")
    # The paper puts no label on this panel's y-axis, so this line is the
    # only place the quantity is named. It has to stay.
    d.foot(s, "y-axis is log₁₀ fraction viable ≈ the model's broken "
              "fraction q. Day 1 is at detection; day 28 is 10⁻⁶·³.")
    d.notes(s,
           "Before anything is fitted, look at what they measured. Their "
           "first point is day one, sitting on the detection limit at ten "
           "to the minus eight. By day 28 the escape fraction is around ten "
           "to the minus 6.3 — a rise of about one and a half orders over "
           "224 generations.\n "
           "Their y-axis is doing our work for us. Fraction viable is CFU "
           "with aTc over CFU without, so a functional cell dies and a "
           "broken one survives, and the axis is approximately q. It is an "
           "approximation — killing is not perfect even for a working "
           "circuit — but it means we can put our model on their units.\n "
           "This is the CRISPRks strain without antibiotics. The ten to the "
           "minus 8.6 figure later in the hour is a different strain, with "
           "antibiotics, at one timepoint, and I do not let the two stand "
           "in for each other.")

    s = d.light()
    d.header(s, "segment 4", "fit it, and see what it rules out")
    d.title(s, "The curve bounds the burden from above")
    d.image_centered(s, FIG + "s23_measure_s.png", top=1.80, band=4.60)
    # 196 characters against the foot's 200. RMS is in decades, over their
    # eight timepoints; without those two facts the room is handed three
    # numbers to compare and told nothing about what they measure.
    d.foot(s, "RMS residual, in decades, over their eight timepoints: flat "
              "line 0.20, the s = 0 fit 0.15 — the rise is barely separable "
              "from none. s = 0.05 misses by 1.2; above s = 0.02 it misses "
              "badly.")
    d.notes(s,
           "Segment 3 said the burden is the parameter with the leverage. So "
           "go and measure it — and the stability curve is enough to do "
           "that, because the shape of the rise depends on s and the height "
           "depends on mu.\n "
           "Fit the model to their eight points and it comes back with a "
           "mutation rate near three times ten to the minus nine and a "
           "fitness cost that is statistically zero. Push the burden up to "
           "the five percent this hour has been assuming and the curve "
           "bends the wrong way — it cannot be flat early and still reach "
           "the right place at day 28.\n "
           "So the circuit is close to free, and that is why it lasts a "
           "month. It is a design achievement and the model is how you see "
           "it.\n "
           "The residuals, if anyone asks: s = 0 fits at RMS 0.151 "
           "decades, a flat line with no rise at all at 0.204, and the "
           "five percent this hour assumes at 1.215. The flat row is "
           "why this is a bound and not a measurement.\n "
           "Pulling a parameter out of a performance curve works. It does "
           "not work for the number of cassettes, which is next.\n "
           "Two things I say before anyone else does. This mu is a LUMPED "
           "rate for losing the whole circuit, not a per-event rate: the "
           "mechanism we come to is recombination between a repeat, "
           "which runs around ten to the minus five or six per repeat, and "
           "there are seven of them. The fit cannot see that, which is "
           "another way of saying escape is not one hit.\n "
           "And the hour now has three values of s. Retrieval primed twenty "
           "percent from Scott. This slide adopted five. The curve excludes "
           "anything above two. The retrieval number is for a circuit "
           "occupying a tenth of the proteome; this one evidently does not.\n "
           "If someone asks why this mu is not the 1e-6 from the ledger: "
           "that was a round number for a generic circuit, chosen to show "
           "the trade-off. This one is measured, and it is theirs. Both "
           "sit far above s/mu = 413, so the ledger's conclusion is "
           "unchanged.")

    s = d.light()
    d.header(s, "segment 4", "and the slope argument dies too")
    d.title(s, "A burden bends the curve like redundancy does")
    d.image_centered(s, FIG + "s23_confounded.png", top=1.80, band=4.60)
    # THEIR OWN SLOPE BELONGS HERE, with its window, not in a caption two
    # slides back on log-linear axes. Least squares over the eight
    # detectable points of Fig. 2e gives 0.63 (all nine, including the
    # censored day-1 point, gives 1.08 -- which is the window argument
    # making itself). The home guide states it and draws the consequence;
    # the deck should not be the quieter of the two.
    d.foot(s, "Every point on both curves is ONE cassette. And their own "
              "data, over the eight detectable points, has a log–log slope "
              "of 0.63 — below 1, which no multi-hit model allows at any k.")
    d.notes(s,
           "This is the second thing that dies. Every point on this plot is "
           "a single cassette. The only thing varying is its fitness cost.\n "
           "Their own slope is in the foot and I read it out: 0.63, over "
           "the eight detectable points. Below one. No multi-hit model "
           "produces that at any k, so the data do not merely fail to "
           "identify k — they are outside the family. Over all nine "
           "points, censored day one included, the same data give 1.08, "
           "which is the window argument making itself.\n "
           "At our own reference burden of five percent, one cassette "
           "returns a slope between 2.4 and 5.0 depending on where you fit "
           "it — which reads as anywhere from two to five independent "
           "cassettes. The slope does not identify k once there is "
           "selection. A slope quoted without the window it was fitted over "
           "is not a measurement.\n "
           "So the honest conclusion is negative, and it is the more useful "
           "one: you cannot read an architecture off a stability curve. "
           "That is a statement about what the measurement can "
           "support, and it is the kind of statement I want them making.")

    s = d.dark()
    d.header(s, "segment 4", "Vote  ·  argue with your neighbor  ·  vote again")
    d.title(s, "A colleague measures a log–log slope of 3.0")
    d.text(s, "They tell you it proves their construct carries three "
              "redundant cassettes. What is the strongest thing you can "
              "say back?",
           M, 2.10, 11.9, 0.75, size=18, color=WHITE)
    for i, (k, opt) in enumerate([
            ("A", "They are right — the slope is the number of cassettes."),
            ("B", "They have at least three; the slope is a lower bound."),
            ("C", "One cassette with a burden between 3 and 7 "
                  "percent gives the same slope."),
            ("D", "The slope is meaningless without the detection "
                  "threshold.")]):
        y = 3.10 + i * 0.78
        d.shape(s, S.OVAL, M, y, 0.46, 0.46, fill=CYAN, line=None)
        d.text(s, k, M, y + 0.08, 0.46, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.04, 11.2, 0.45, size=16, color=WHITE)
    d.notes(s,
           "I take a silent vote, let them argue, and vote again without "
           "revealing anything between.\n "
           "The answer is C and the previous slide contains it, which is the "
           "point — this checks whether they read the figure or just "
           "watched it.\n "
           "B is the attractive wrong answer and it is the one I held "
           "myself. It feels safe because it only claims a "
           "bound. It is wrong in the same direction as A: both assume the "
           "slope is about architecture, and selection forges the same slope "
           "with one cassette.\n "
           "D is true and insufficient. If someone picks D I say so: the "
           "threshold matters, and even with a perfect one the confounding "
           "stands. They are thinking well.")


def _mechanism(d):
    s = d.light()
    d.header(s, "segment 4", "what the paper says is happening")
    d.title(s, "Two routes, and only one of them is in our model")
    d.paper_figure(s, "rottinghaus2022_fig6a", 3.89, 1.84, 5.56, 4.05,
                   "Rottinghaus et al., Nat Commun 13:672 (2022), Fig. 6a",
                   "How the authors say the switch dies.",
                   show_caption=True)

    s = d.light()
    d.header(s, "segment 4", "what the paper says is happening")
    d.title(s, "Two routes, and only one of them is in our model")
    d.rows(s, [
        ("route 1", "slow loss of a cassette — replication error, and "
                    "recombination between the repeats we meet next slide. "
                    "The authors credit redundancy for the 28 days; our fit "
                    "credits the near-zero burden, and the curve cannot "
                    "separate them."),
        ("route 2", "Cas9's own double-strand breaks induce the SOS "
                    "response, which raises the cell's mutation rate."),
        ("and route 2 only appears", "in vivo, or in vivo-like conditions "
                                     "where resources and growth are "
                                     "limited."),
        ("the fix is not a circuit", "knock out recA, polB, dinB, umuDC — "
                                     "the Δrpdu strain."),
    ], top=2.00, label_w=2.9)
    d.notes(s,
           "Here is the thing our model has no term for. The device raises "
           "its own mutation rate when it is operated. Cas9 cuts, the cut "
           "induces SOS, SOS turns on error-prone polymerases, and the "
           "cells that survive with an intact chromosome now mutate faster.\n "
           "In their words, escape mutants of the CRISPR strain only arose "
           "via this process when tested in vivo or under in vivo-like "
           "conditions. In rich medium with plenty of resources you never "
           "see it, which is why a clean benchtop stability curve is not "
           "the measurement you want.\n "
           "Be careful which way the arrow points here, because the obvious "
           "reading is backwards. SOS is induced in both conditions -- if "
           "anything harder in a flask, where expression is higher. What "
           "changes is downstream. Starved and barely growing, the cell "
           "makes less of everything, Cas9 included, so the cut across a "
           "replicating multi-copy chromosome does not finish. Daughters "
           "come through with an intact copy and an SOS response already "
           "running. In rich medium those same mutagenized daughters get "
           "cut and die. The environment does not switch the mutagenesis "
           "on -- it takes away the killing that was clearing the "
           "mutagenized cells. Their evidence is a genome-integrated GFP "
           "reporter that is markedly dimmer in minimal medium.\n "
           "And notice what the fix is. Not a better promoter, not more "
           "cassettes. Four host genes deleted. That is one of the two "
           "levers on today's list that are not circuit design at all — "
           "the other is the competitor, and it is coming.")

    s = d.light()
    d.header(s, "segment 4", "what mutates")
    d.title(s, "The failure is a repeat the designer chose")
    d.paper_figure(s, "rottinghaus2022_fig6c", 0.90, 2.60, 11.5, 1.58,
                   "Rottinghaus et al., Nat Commun 13:672 (2022), Fig. 6c",
                   "The commonest inactivating mutation in Ptet.",
                   show_caption=True)

    s = d.light()
    d.header(s, "segment 4", "what mutates")
    d.title(s, "The failure is a repeat the designer chose")
    d.rows(s, [
        ("Ptet contains", "two identical 19 base-pair tet operator sites"),
        ("over half of all observed mutations", "a 25 base-pair deletion "
                                                "removing one operator and "
                                                "most of the −35 site"),
        ("mechanism", "recombination between the tandem repeat — RecA "
                      "homologous recombination, or slippage and "
                      "single-strand annealing"),
        ("so μ is not a constant of nature", "it is a consequence of the "
                                              "sequence you picked"),
    ], top=2.00, label_w=3.1)
    d.notes(s,
           "The thing that breaks is not a random point mutation somewhere "
           "in the twenty-odd kilobases they integrated. It is a deletion between two identical "
           "nineteen base-pair operators sitting inside the promoter they "
           "chose — and that promoter is duplicated across every cassette "
           "they added for redundancy. Redundancy and repeat are the same "
           "thing. They made the circuit more robust and more "
           "recombinogenic in one move.\n "
           "Our model treats mutation as a constant rate of random damage. "
           "A single constant fits 28 days in a flask and says nothing "
           "about a mouse, because the real rate depends on the sequence "
           "you chose and on whether the device is cutting. The authors "
           "say the fix is "
           "promoter variants with one operator or lower sequence identity, "
           "and that is a design decision at the level of base pairs.")


# ------------------------- segment 5 · the requirement and the real lever ---
def _requirement(d):
    s = d.light()
    d.header(s, "segment 5", "the specification")
    d.title(s, "Two numbers that were built to be compared")
    d.rows(s, [
        ("the requirement", "a killing efficiency of 1e-8, the figure the "
                            "NIH Office of Biotechnology Activities "
                            "recommends"),
        ("their dose", "1e8 colony-forming units per gavage"),
        # Deliberately blank: the room answers this one. A bare em dash
         # read as a failed substitution, so say what the blank is for.
        ("so what is the requirement, in cells?", "[ the room answers ]"),
        # NAME THE STRAIN. The slide before last counted "three gRNA
        # cassettes" and this one says "2-gRNA", which reads as a cassette
        # going missing. They are different constructs and the deck has to
        # say so where the numbers meet.
        ("what they achieved", "below 1e-8.6 — their optimized 2-gRNA "
                               "switch, a DIFFERENT strain from the "
                               "28-day CRISPRks, with antibiotics, at one "
                               "timepoint. A quarter of a survivor per "
                               "dose."),
        ("and one more step", "one survivor per dose is a MEAN. Given a "
                              "batch's escape fraction the count is Poisson, "
                              "so a dose averaging one carries a 63 percent "
                              "chance of at least one — and their 0.25 "
                              "carries 22 percent."),
    ], top=2.00, label_w=3.4)
    d.foot(s, "The requirement is QUOTED — they cite it, they did not "
              "measure it.")
    d.notes(s,
           "I leave the third row blank and wait. Ten to the eight cells "
           "times ten to the minus eight is one. The requirement is fewer "
           "than one survivor per dose, and the two numbers were chosen "
           "against each other.\n "
           "I let them find it. A specification that reduces to one "
           "intelligible sentence is rarer than it should be.\n "
           "Their optimized switch measures below ten to the minus 8.6, a "
           "quarter of a survivor per dose. On the face of it they have "
           "cleared the bar with room to spare.\n "
           "Expected number "
           "and probability of occurrence are different quantities. A dose "
           "whose expectation is exactly one escaper has a 63 percent chance "
           "of containing at least one, because one minus e to the minus one "
           "is 0.632. Session 12 gave them the machinery for this, and a "
           "requirement written as a mean is a weaker promise than it "
           "sounds.")


def _fluctuation(d):
    """Why a containment number measured once is a weaker promise than it looks.

    WHY IT IS HERE AND NOT CUT. The slide before this one asks the room to
    turn a mean into a probability, and the Poisson step it uses is right
    only INSIDE one batch. Across batches the escape fraction itself
    varies, and not by a little -- which is the Luria-Delbruck result, and
    it is this session's own model run inside a single flask. Leaving it
    out would have the hour teach mutation-plus-selection for forty
    minutes and then quietly assume it away at the one place a number
    leaves the lab.

    TAUGHT FROM SCRATCH. The room has not met the fluctuation test. They
    have, however, just derived why an early mutant is worth more than a
    late one, so the jackpot is not a new idea to them -- only a new name
    and a new consequence.
    """
    s = d.light()
    d.header(s, "segment 5", "the same number, measured twice")
    d.title(s, "Do it again and you get a different answer")
    d.rows(s, [
        ("inside one batch", "given that batch's escape fraction, the count "
                             "in a dose IS Poisson. That is the 63 percent "
                             "we just did."),
        ("between batches", "the escape fraction itself moves, because a "
                            "mutant that appeared early was doubled by "
                            "every generation after it.", AMBER),
        ("so the spread is not Poisson", "most batches land near each other "
                                         "and a few land orders of magnitude "
                                         "high. Luria and Delbrück named "
                                         "those jackpots in 1943.", AMBER),
        ("and here it is worse", "their mutants were neutral. Ours grow "
                                 "faster than the cells they came from, so "
                                 "the early ones run further.", AMBER),
        ("what that costs you", "one plating of one batch is one draw from "
                                "a long-tailed distribution. A containment "
                                "spec wants the distribution, not the draw.",
         TEAL),
    ], top=1.90, label_w=3.4)
    d.foot(s, "Luria and Delbrück ran this experiment to prove mutations "
              "come before selection, not because of it. The spread was the "
              "evidence.")
    d.notes(s,
           "I teach this from scratch because they have not met it, and it "
           "takes two minutes because they have already derived the hard "
           "part.\n "
           "Set it up as a question: you grow the same strain in twenty "
           "flasks from the same inoculum, plate all twenty, and count "
           "escapers. How much do the counts differ? The room expects "
           "Poisson scatter — square root of the mean.\n "
           "They do not. Most are similar and a few are enormous, and the "
           "reason is the thing we spent segment three on. A mutation in "
           "generation two is doubled by every generation after it; a "
           "mutation in the last generation is one cell. The timing of the "
           "event, not the rate, sets the size of the result.\n "
           "That is the Luria-Delbrück fluctuation test, 1943. Their point "
           "was that the spread is only explicable if mutations happen "
           "before you apply the selection — which is the opposite of the "
           "Lamarckian alternative they were testing. It is one of the "
           "cleanest experiments in biology and it is this session's own "
           "equation run inside one flask.\n "
           "Then the design consequence, which is the reason I spend the "
           "time: ten to the minus 8.6 was one measurement of one batch. "
           "The honest version of a containment claim is a distribution "
           "over independent batches, and nobody in this literature "
           "reports one.\n "
           "If someone asks whether selection makes the tail heavier: yes. "
           "Luria and Delbrück's mutants grew at the same rate as everyone "
           "else. Ours have a growth advantage, so an early escaper runs "
           "further than it would in their experiment.")


def _retention(d):
    s = d.light()
    d.header(s, "segment 5", "commit to a number before you see it")
    d.title(s, "How long does that quarter-of-a-survivor last?")
    d.rows(s, [
        ("what they measured", "fraction viable below 1e-8.6, against a "
                               "requirement of 1e-8"),
        ("now let it grow", "permissive conditions, no aTc, the population "
                            "doubling normally"),
        ("write down a number", "how many generations before the standing "
                                "escape fraction crosses back over 1e-8?"),
    ], top=2.15, label_w=3.4)
    d.foot(s, "You have the floor and the requirement. One number: "
              "generations until the escape fraction crosses 1e-8.")
    d.notes(s,
           "Everyone writes a number. I take three out loud before "
           "advancing, and I want the spread on the record because it is "
           "usually two or three orders of magnitude wide.\n "
           "Most of the room says hundreds of generations, by analogy with "
           "the 224 they have been looking at all hour. The answer is "
           "under twenty generations everywhere on the grid, and under one "
           "generation over most of it — at eight generations a day, that "
           "is hours to a couple of days, not months.\n "
           "224 generations is how long until the circuit is mostly "
           "broken, and that is a completely different question from how "
           "long until one escaper in a hundred million exists.")

    s = d.light()
    d.header(s, "segment 5", "the question the assay does not answer")
    d.title(s, "Containment is a duration")
    d.image_centered(s, FIG + "s23_retention.png", top=1.80, band=4.60)
    # 0.02 TO 18 GENERATIONS, NOT 0.01 TO 7.5. The old numbers came from
    # somewhere narrower than the grid the figure plots: swept over the
    # ranges the figure itself uses (s from 0.004 to 0.2, mu from 4e-10 to
    # 4e-7) the crossing runs 0.019 to 17.7 generations, which at this
    # session's own 7.97 generations per day is up to two and a quarter
    # days, not "under a day in every case". The slide's whole claim is
    # that the conclusion survives not knowing the parameters, so a
    # caption that fails on the grid behind it hands the room the
    # counterexample.
    # The fit two segments back bounds s under 0.02 and this grid runs
    # well past it on purpose: the point is that the answer does not
    # depend on which value you pick, so the grid has to include the ones
    # the fit excludes. Saying so here is what stops a student who read
    # that foot from thinking the deck forgot its own result.
    d.foot(s, "Swept over s from 0.004 to 0.2 — deliberately past the "
              "bound the fit set — and μ from 4×10⁻¹⁰ to 4×10⁻⁷: the "
              "crossing takes 0.02 to 18 generations, at most about two "
              "days, everywhere.")
    d.notes(s,
           "They clear the requirement at the moment of the assay. Start "
           "there and ask how long it lasts, and the standing escape "
           "fraction crosses back over the NIH line within a few "
           "generations of permissive growth.\n "
           "I want to be careful about what this is. Both s and mu here are "
           "ours; the paper measures neither. What makes the point robust "
           "is that the answer is under a day everywhere on the grid, so it "
           "does not depend on getting the parameters right.\n "
           "A measured fraction viable and a containment requirement are "
           "not the same kind of quantity. One is a number you take once. "
           "The other is a promise about a period of time, and nothing in "
           "the plating assay speaks to it.")

    s = d.light()
    d.header(s, "segment 5", "and the two questions pull opposite ways")
    d.title(s, "The two questions have opposite answers")
    d.image_centered(s, FIG + "s23_two_asymmetries.png", top=1.80, band=4.60)
    # "retention" is named on the figure and defined here. It is NOT how
    # long the circuit is retained -- that is the other curve on the same
    # panel -- and the close asks for it as a specification, so the room
    # needs the definition in words where the quantity is first plotted.
    d.foot(s, "retention = generations of permissive growth before the "
              "escape fraction climbs back over the NIH line, starting "
              "from their measured floor.")
    d.notes(s,
           "This is the result I would most like them to leave with, and it "
           "is not in the paper — it falls out of the model we built, which "
           "is the model's one good day.\n "
           "Across the panels: how long the circuit lasts moves by a "
           "factor of about forty on the burden and by a factor of one and "
           "a half on the mutation rate. How long containment holds moves "
           "by a factor of several hundred on the mutation rate and by one "
           "percent on the burden. Same two parameters, opposite "
           "sensitivities, and the figure prints both ratios from the "
           "curves rather than from my memory.\n "
           "The reason is that containment lives in the far left tail, "
           "around ten to the minus eight, where selection has had nothing "
           "to amplify yet. Crossing the requirement is pure mutation "
           "accumulation. Selection only starts to matter once there is a "
           "population of escapers to multiply.\n "
           "Which is why the ledger from segment 3 applies to the first "
           "question and not the second, and why knocking out the SOS "
           "response — which lowers mu and does nothing to s — is aimed at "
           "exactly the right one.")

    s = d.light()
    d.header(s, "segment 5", "why believe a fit this weak")
    d.title(s, "The crossover is at q* = μ / s")
    d.rows(s, [
        ("the two terms are equal when", "s q = μ,  that is  q* = μ / s. "
                                         "Below q* mutation does the work; "
                                         "above it selection does."),
        ("so it depends on where you ask", "a containment threshold of 1e-8 "
                                           "sits BELOW q*; a half-life at "
                                           "q = 0.5 sits far above it."),
        ("which is why", "a fit too weak to pin the rate still gets the "
                         "SHAPE right: q* moves with the rates, but the fit "
                         "bounds it — μ ≈ 2.6e-9 and s < 0.02 put q* above "
                         "1e-7, which is above the threshold we care about."),
        ("the regime, stated", "this holds while s/μ < 1e8. Above that even "
                               "containment becomes selection-limited."),
    ], top=2.00, label_w=3.4)
    d.foot(s, "Checked against a mutation rate that jumps 100-fold under "
              "induction: retention still moves with μ and not with s.")
    d.notes(s,
           "Someone should have objected by now, and if nobody does "
           "I raise it myself: we spent segment 4 destroying this model and "
           "segment 5 using it. Why is that allowed?\n "
           "Because the two are different kinds of claim. Segment 4 withdrew "
           "a statement about absolute timescales, which depends on mu being "
           "a particular constant. This is a statement about which of two "
           "mechanisms dominates, and that depends only on where the "
           "threshold you care about sits relative to mu over s.\n "
           "Below mu over s the selection term contributes almost nothing "
           "whatever the rates are. I checked it with mu jumping a "
           "hundredfold to imitate the SOS effect, and retention still "
           "barely moves with s.\n "
           "The last row is the discipline. This has a regime and I state "
           "it. A fit without its window stated is not a result.")


def _competition(d):
    # THE EXPERIMENT BEFORE THE RESULT. This segment used to open on their
    # Fig. 3a with a four-word caption and no note, and the slide after it
    # named three strains -- "CRISPRks", "CRISPRks, 1:1 competitor",
    # "CRISPRks drpdu" -- as bare strings. Two of those three had never
    # been defined anywhere on a slide, and the room was being asked to
    # read four traces off a figure whose conditions nobody had said out
    # loud. The object before the model, which is this repo's own rule.
    s = d.light()
    d.header(s, "segment 5", "the lever that is not a circuit at all")
    d.title(s, "Three strains in one flask, and what is in each")
    d.rows(s, [
        # About 110 characters shorter than the first draft: five rows of
        # this length needed 5.11in in a 4.54in band.
        ("CRISPRks", "the construct we counted: four Ptet-cas9, three "
                     "Ptet-gRNA, tetR."),
        ("the competitor", "the SAME strain with its gRNAs removed. Cas9 "
                           "with nothing to aim at, so it survives "
                           "induction and eats the same food.", AMBER),
        ("CRISPRks Δrpdu", "that kill switch in a host missing recA, polB, "
                           "dinB, umuDC — the four SOS genes. Those "
                           "initials are the name.", AMBER),
        ("the assay", "anaerobic, static, minimal glucose at 37 °C — their "
                      "in vivo-like condition. Add aTc, plate survivors "
                      "for three days."),
        ("what you are looking at", "log₁₀ fraction viable: survivors with "
                                    "aTc over survivors without. Down is "
                                    "killing; the −8 floor means no "
                                    "colonies.", TEAL),
    ], top=1.86, label_w=3.1, bottom=6.40)
    d.foot(s, "One strain alone, and the same strain sharing a flask with a "
              "cousin that cannot kill itself.")
    d.notes(s,
           "Three strains and one question, and I set all of it out before "
           "the figure goes up.\n "
           "CRISPRks is the thing we have been studying all hour. The "
           "competitor is the clever part of the design: it is the same "
           "strain with the gRNA cassettes removed, so it is as close to "
           "isogenic as you can get. Same growth rate, same niche, same "
           "everything — it simply cannot cut itself. That is what makes "
           "this a clean experiment rather than a confound.\n "
           "Delta-rpdu is the SOS knockout: recA, polB, dinB, umuDC. The "
           "name is just those four initials, and it is the fidelity lever "
           "from segment four arriving in the same flask as the ecology "
           "lever.\n "
           "The conditions matter and I say them. Anaerobic, static, "
           "minimal medium — which is their in vivo-like condition, the one "
           "where route two showed up at all. A benchtop LB culture would "
           "not have found this.\n "
           "And the axis: fraction viable with aTc over without. Zero means "
           "induction killed nobody. Minus eight means no colonies on the "
           "plate. So a curve that comes back UP is a population that has "
           "stopped being killable.")

    s = d.light()
    d.header(s, "segment 5", "the lever that is not a circuit at all")
    d.title(s, "Make the escaper's advantage negative")
    d.paper_figure(s, "rottinghaus2022_fig3a", 3.94, 1.84, 5.45, 4.05,
                   "Rottinghaus et al. 2022, Fig. 3a",
                   "Each strain alone, and at 1:1 with the no-gRNA cousin.",
                   show_caption=True)
    d.notes(s,
           "Now the figure, and I walk the traces rather than let them "
           "hunt.\n "
           "Time runs along the bottom in hours of aTc, out to 72. Fraction "
           "viable up the side, so lower is better killing and the bottom "
           "of the axis is no survivors.\n "
           "Everything drops hard in the first few hours — that is the kill "
           "switch working, five or six logs of it.\n "
           "Then watch which curves come back. CRISPRks on its own climbs "
           "back to where it started: the cells that survived have broken "
           "switches, nothing is killing them, and they refill the culture. "
           "That is the whole session in one trace.\n "
           "Then be careful about the other traces, because this is where "
           "the paper is easiest to over-read. Plain CRISPRks WITH the "
           "competitor kills better at 24 hours — about a log better — and "
           "on its own that is all competition bought. The trace that never "
           "comes back is Delta-rpdu with the competitor, and that is TWO "
           "levers: the competitor holding the niche and the SOS knockout "
           "lowering the rate at which escapers appear at all. I say that "
           "explicitly, because crediting elimination to competition alone "
           "is the mistake this figure invites.\n "
           "Three biological replicates and the error bars are standard "
           "deviations. A point drawn at the floor means that replicate "
           "gave no colonies, which is a bound rather than a measurement — "
           "the same distinction we made with the NIH number."
           )

    s = d.light()
    d.header(s, "segment 5", "the lever that is not a circuit at all")
    d.title(s, "Make the escaper's advantage negative")
    d.rows(s, [
        # Each row now says what HAPPENED, not what it is called. "Rebound"
        # and "bounded standing fraction" were both doing work the room had
        # no way to unpack.
        ("alone", "killed, then back where it started by 48 hours. The "
                  "survivors have broken switches and nothing is removing "
                  "them, so they refill the flask."),
        # CORRECTED 8 November against NUMBERS.md, which says in terms:
        # "In plain CRISPRks, competition improved the 24 h kill from
        # 10^-3.3 to 10^-4.2 and that is all." The row used to claim it
        # STAYED killed, at a standing fraction of 1e-4 to 1e-6 -- a range
        # the provenance file does not carry and a claim it explicitly
        # warns against, because elimination took competition AND the
        # lowered mutation rate. Two levers, not one, and the next row is
        # where the second one arrives.
        ("with the cousin", "a better kill at 24 hours — 10⁻³·³ down to "
                            "10⁻⁴·² — and on its own, that is all it did.",
         AMBER),
        # The 1:1000 result is Supplementary Fig. 4c, not the panel on the
        # screen, and reading a number off a figure the room cannot see is
        # the habit bar B4 exists against.
        ("Δrpdu, with the cousin", "no survivors at all by 72 hours — a "
                                   "lower mutation rate and nowhere to "
                                   "expand, together. Their supplement gets "
                                   "the same result at one competitor in a "
                                   "thousand.", AMBER),
        ("what it does to the model", "it does not touch μ. Write it as a "
                                      "negative s and you get a bounded "
                                      "steady state at q = μ/|s| instead of "
                                      "runaway to one."),
    ], top=2.00, label_w=3.0)
    d.notes(s,
           "A closely related strain without the kill switch, sharing the "
           "niche. The escaper is no longer the fittest thing in the "
           "flask.\n "
           "This is ecology, not circuit design, and it is the single most "
           "effective intervention in the paper. It acts on s, which the "
           "closed form already told us is the parameter with the leverage "
           "for the longevity question.\n "
           "And it changes the equation qualitatively, not just "
           "quantitatively. Put s negative into dq/dt = (1-q)(sq + mu) and "
           "the broken fraction no longer runs away to one. It settles at mu "
           "over the magnitude of s, a standing level set by mutation "
           "against purging. That is a different dynamical object from "
           "everything else in the hour.\n "
           "A caution on the arithmetic: negative s is a re-parameterization, "
           "not the mechanism. There are three populations here, and the "
           "broken cell's advantage over its own parent has not changed. "
           "What the competitor does is occupy the niche that induction "
           "clears, so the escaper cannot expand into it. The paper calls it "
           "inter-strain exclusion. Writing it as negative s happens to give "
           "the right bounded steady state.\n "
           "Little of today's toolbox is in this. No promoter, no feedback, "
           "no insulation. You change what else is in the room.")


def _target(d):
    s = d.light()
    d.header(s, "close", "the variable nobody in this paper could change")
    d.title(s, "The other move changes the target")
    d.rows(s, [
        ("a kill switch fails by LOSS", "break any of twenty-plus "
                                        "kilobases, or recombine out an "
                                        "operator. Losing is easy."),
        ("synthetic auxotrophy fails by GAIN", "redesign an essential enzyme "
                                               "to need an amino acid no "
                                               "cell can make. Escape means "
                                               "ACQUIRING a pathway."),
        ("measured", "Mandell 2015, Nature 518: no escape detected over "
                     "14 days, limit of detection 2.2e-12."),
        ("a third route we never modeled", "gRNAs and tetR are plasmid-borne, "
                                           "and today's equation has no term "
                                           "for DNA leaving a cell."),
        ("so μ was never a constant", "it is the mutational target size you "
                                       "designed."),
    ], top=2.16, label_w=3.5, bottom=6.00)
    d.foot(s, "Not assigned. Mandell et al. open by arguing that kill "
              "switches impose selection to eject themselves — today's "
              "thesis, published in 2015.")
    d.notes(s,
           "I add this because an hour spent on one paper can leave the "
           "impression that its four strategies are the field, and they are "
           "not.\n "
           "Everything today moved a rate. Lower the burden, lower the "
           "mutation rate, add cassettes, change the competition. All of it "
           "takes the failure mode as given and tries to slow it down.\n "
           "The other move is to change what failure requires. A kill switch "
           "dies by losing something, and losing things is easy — that is "
           "the whole hour. Make the cell depend on a molecule that does not "
           "exist outside a laboratory and escape now requires inventing a "
           "biosynthetic pathway. Mandell's group and Rovner's did that in "
           "two separate 2015 papers, and Mandell "
           "measured escape below detection at two times ten to the minus "
           "twelve — three orders below what we have been admiring, and "
           "that is their detection limit, not a measured escape rate.\n "
           "And I want them to notice the date. Mandell's opening argument "
           "is that existing containment imposes evolutionary pressure on "
           "the organism to eject the circuit — which is the thesis of this "
           "entire session, published seven years before the paper they "
           "read for today. Rottinghaus know this. They are solving the "
           "harder problem of making the loss-of-function architecture work "
           "in a real gut. But the design question "
           "underneath is what has to mutate, and that is the one you "
           "should carry out of here.")


def _close(d):
    s = d.light()
    # THE COUNT, SETTLED. This slide said "Five levers. One is circuit
    # design.", its own note said "three of these four", slide 3 promised
    # "three of the four things that work", and the note on the SOS slide
    # said "the second of the three things on today's list". Four counts
    # for one list. The fifth row was never a lever -- it does not change
    # the failure, it is what you do about a failure you cannot stop --
    # and the note already treats it that way ("the fifth item ... the
    # engineering move"), so it is set apart and the count is four.
    #
    # "segment 1" is out of the kicker for the same reason "rung" came out
    # of session 22: the room has never been shown a segment map, so a
    # reference to one resolves to nothing. The question itself is now on
    # the slide where it was asked, so the kicker can point at that.
    d.header(s, "close", "check these against the list you made at the start")
    d.title(s, "Two of the four levers are circuit design")
    d.rows(s, [
        ("lower s", "reduce the burden. Circuit design, and session 19's "
                    "whole subject."),
        ("lower μ", "sequence choices — drop the internal repeats — and "
                     "knock out SOS mutagenesis. Not circuit design."),
        ("raise k", "redundant cassettes. Circuit design too — and we "
                    "counted what it buys: an exponent of three, and one "
                    "more repeat per copy."),
        ("change the selection", "intra-niche competition. Ecology."),
        ("and not a lever at all", "state the retention time: put a finite "
                                   "number on it as a specification, and "
                                   "design the protocol around it.", AMBER),
    ], top=1.82, label_w=2.9, bottom=5.36)
    d.notes(s,
           "Back to the board from the start of the hour and we check what "
           "they listed against what works.\n "
           "Two of the four levers are circuit design, and I want the room "
           "to feel the shape of that rather than take a count from me. "
           "Lowering the burden is the real one. Redundancy is circuit "
           "design too, and we spent three slides watching it fail to do "
           "what it looks like it does — the exponent is three rather than "
           "seven, and the copies are the repeats the thing recombines "
           "out. So the honest version is: one lever that works, one that "
           "works less than it looks, and two that are not circuit design "
           "at all. That is the conclusion, and it is not a defeat. It is also why this "
           "session sits where it does: sessions 24, 25 and 26 are all "
           "about designing with population-level processes rather than "
           "against them, and this hour is what earns them.\n "
           "The last row is the one I most want to land, and it is not a "
           "lever. The paper's own "
           "framing is that you cannot make this permanent, so the "
           "engineering move is to state how long containment holds, treat "
           "that as a specification like any other, and build the dosing "
           "protocol around the number. A circuit that fails on a schedule "
           "you published is a different object from one that fails on a "
           "schedule you did not.")

    # THE READING GETS ITS OWN SLIDE. Session 24 now carries two required
    # papers rather than one, so the box is six rows and 3.88 in tall. Under
    # five rows of levers it has nowhere to go: assignment() clamps it upward
    # and it lands on top of them -- 20 of this deck's 23 overlapping text
    # pairs were that collision. A reading list the room is meant to act on
    # is not a footnote to another slide anyway.
    s = d.light()
    d.header(s, "close", "what to read before Tuesday")
    d.title(s, "The reading for next time")
    # Six rows on a slide of their own: 0.52 + 0.80*6 = 5.32 in, so the box
    # runs 1.95 to 7.27 against the 7.32 limit, and each blurb gets two lines
    # instead of colliding with the next citation.
    d.assignment(s, y=1.95, row_h=0.80)
    # Above the box, because assignment() starts at 1.95 and fills the
    # rest of the slide. One line: at this width a second one does not fit
    # between the title and the box.
    d.text(s, "Today's home guide is on bCourses — four items, answers on "
              "a separate sheet.",
           M, 1.48, W - 2 * M, 0.34, role="body", color=INK)
    d.notes(s,
           "Point at the home guide before the reading. Four items, after "
           "class, on paper, and the answers are a separate file so they "
           "write something down first. It is not graded and it is the "
           "best preparation for PS9 that exists.\n "
           "Two required this time, not one, because session 24 needs both "
           "the chemostat paper and the band detector.\n "
           "I say which is which: one is the two-species oscillator, the "
           "other is pattern formation from a diffusible signal. They are "
           "the same idea at two scales.\n "
           "The optional four are there for the term projects, not for "
           "Tuesday.")
