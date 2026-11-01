"""Session 21 — Retroactivity: reading a signal changes it.

Thursday 5 November 2026. PS7 is due today; PS8 is posted today.
Mishra 2014 was assigned at the close of session 20. Aoki is assigned today.

WHAT THIS SESSION IS. Rung 3 of the ladder, and two things make it different
from the two before it. First, it is the THIRD instance of one mechanism and
the room has already been told to expect it -- session 19's close slide put a
three-row ladder on the board and its note calls that "the slide the hour
exists for". So this session opens by COLLECTING on that promise, not by
introducing a topic. Second, it is the FIRST REPAIR in Part II: rungs 1 and 2
diagnose, this one engineers the problem away.

It also closes an old debt. Retroactivity was assessed for 20 points on PS5 in
a prior year with no demonstrating lecture, and "retroactivity" appears 0 times
in 962 pages of the 2025 decks.

THE SPINE, REBUILT 26 OCTOBER. See sessions/s21-retroactivity/REBUILD.md; it
supersedes DESIGN.md 3-4 and NUMBERS.md 4-6 where they disagree. Four
adversarial reviews found that the previous spine's headline claim did not
apply to the paper the hour builds to. The corrected spine:

TWO MODELS ARE THE HOUR, not a caveat on slide 4. If the bound complex is
protected from degradation, the steady state of free X is EXACTLY k/gamma at
every load -- no level cost, only a speed cost. If the complex is diluted with
everything else, X + C is pinned and free X falls by what is parked. Which one
you are in is an EXPERIMENTAL question with a one-line signature: measure the
steady state with and without load. And Mishra answers it -- for their system,
in a growing culture, p. 1273: "neither the inclusion of the load driver nor
the presence of load affected the final steady state ... consistent with a
system in which the interconnecting species (SKN7m) is protected from
degradation when bound to DNA." The paper is the protected model, so the paper
pays only the speed cost, which is exactly why it reports response time and
bandwidth and never levels.

THE SPEED COST IS AFFINITY-BLIND BY CONSERVATION, and this is the result the
hour turns on. integral of R dX from 0 to infinity = C(inf) - C(0) = p_tot,
exactly, for every K_d. The total extra material the loaded system must
synthesize is the SITE COUNT, whatever the affinity; K_d decides only WHEN
during the approach you pay it. So a weaker operator buys nothing -- and the
boundary falls out of the same argument: past K_d ~ X_T the sites never fill,
so you never pay all of p_tot, and the regulation goes with the load.

THE 1.45 IS 1/ln 2. Three lines, not a measured constant: if K_d << X_T the
sites are full before half-max, so the loaded system has made p_tot extra
molecules, costing p_tot/k against an unloaded half-time of ln2/gamma. Ratio
(p_tot/X_T)/ln 2 = 1.442695. Verified to 1.442697 at K_d = 1e-4.

THE TWO COSTS ARE NOT ONE RATIO. The speed cost scales with total sites and is
affinity-blind; the level cost scales with sites OCCUPIED, (p_tot/X_T)*theta,
and is affinity-dependent -- and exists only in the diluted model. That
contrast is the payoff, and it replaces a claim that was false.

ALPHA IS NOT OUR R, and the deck says so rather than asserting an identity.
Box 1, p. 1270, prints it: "alpha = 1 for the unloaded system and
alpha = (1 + p/K_d)^-1 for the loaded system". That is our R with the sites
EMPTY; their Box 1 holds p constant with no site conservation. Inverting their
Box 1, alpha = 0.80 means p/K_d = 0.25 -- the only thing the paper constrains.
Our p_tot and K_d are invented teaching numbers, so the deck does NOT compare
the two: an earlier draft did, and it was comparing our toy's load against
their measured one, with our side evaluated in the wrong model column.

WHERE THE NUMBERS COME FROM. REBUILD.md, every one with its KIND and its
verification. TEACH THE MINUTES, not the percentage: 396 -> 699 min. The 76%
carries a denominator convention, and so does the bandwidth: 0.0175 -> 0.0140
is 20% of what you had, not a quarter. Mishra's four bandwidths are CALCULATED
(Fig. 4c caption), not measured -- so they may not be drawn as markers.

THE 9% INSULATION COST IS NOT SIGNIFICANT at n = 3 (Welch t = 2.55, p = 0.10),
and the buffered series is non-monotonic in load. That is now a RELEASE asking
the room whether the difference is real, not a number PS8 grades a calculation
off.

FOUR MOVES, which the previous build of this deck had none of. frame, build,
release, debrief -- docs/lecture-design.md 5e. Three releases: the steady-state
signature, the conservation integral, and the n = 3 significance question.

MISHRA 2014 IS NOT MISHRA 2021 -- but it IS the same Deepak Mishra, with Ron
Weiss senior on both, nine days apart in this course. Same author reusing the
same yeast chassis, which is a better beat than a surname coincidence. Every student-facing slide cites the year.

WHAT SESSION 18 ACTUALLY TAUGHT. It taught decoy sites explicitly (segment 4,
"held by DECOY SITES that are not its promoter ... Titration") and named
SEQUESTRATION as the through-line. But its sharpness came from ZERO-ORDER
saturation -- "an apparent Hill coefficient of 26 from one site, with no
cooperative binding" -- and in s18 sequestration SOFTENED the switch. So the
ladder may not say the holding is what made it sharp. s19's close slide
carries the same error and needs the same fix.

NO PRINTED TIME RANGES. Minutes are Adam's.

Run:  python tools/build_decks.py s21
"""
from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)

FIG = "figures/build/"
FILENAME = "s21-retroactivity"


def build():
    d = Deck("Session 21 — Retroactivity and insulation", session=21)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _ladder(d)
    _goals(d)
    _object(d)
    _derivation(d)
    _two_models(d)
    _thesis(d)
    _mishra(d)
    _repair(d)
    _cost(d)
    _close(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    s = d.dark()
    d.text(s, "Session 21  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "Reading a signal changes it",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "The arrow in your circuit diagram says SIGNAL. The molecule it "
              "stands for says BINDING SITE. Today that difference costs you "
              "something, and then we build the thing that fixes it.",
           M, 4.50, 8.6, 1.2, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.45, 9.0, 0.4, size=13, color=SILVER)
    d.notes(s,
           "This is the first session in Part II that ENGINEERS a fix rather "
           "than characterizing a problem, and I say so early — rungs one and "
           "two diagnosed, this one repairs.\n "
           "And it is the third time they meet one mechanism. I promised them "
           "that on Thursday the 29th and the next slide collects on it.")


def _retrieval(d):
    s = d.light()
    d.header(s, "open", "two from Tuesday, one from further back")
    d.title(s, "Before we start")
    d.rows(s, [
        ("1", "S·v = 0 is the whole constraint. Why does that leave you "
              "unable to predict a flux, and what did we have to add?"),
        ("2", "Two reactions turned out to run at exactly the same rate under "
              "every objective. What about the network forced that?"),
        ("3", "From session 18: a transcription factor with a hundred decoy "
              "sites nearby. What do the decoys do to how much of it is "
              "available to work?"),
    ], top=2.05, label_w=0.7)
    d.notes(s,
           "One and two are Tuesday. Three is session 18, and it is the one "
           "that matters — it is the first rung of today's ladder and they "
           "need it loaded before the next slide.\n "
           "Answers: stoichiometry has no rates, so an objective had to be "
           "imported. The coupled pair came from a metabolite with exactly one "
           "producer and one consumer.\n "
           "The decoys HOLD the factor, so the free pool is smaller than the "
           "total — that is availability, and it is the word I want. Careful "
           "with the third one: session 18's SHARPNESS came from saturating "
           "two enzymes, not from the holding. In that session sequestration "
           "SOFTENED the switch — the dashed curve in their Fig. 3 with the "
           "enzyme at W_T had no switch left. Do not let the room walk away "
           "thinking sequestration makes things sharp; today it makes things "
           "slow.")


def _ladder(d):
    s = d.dark()
    d.header(s, "segment 1", "frame  ·  collecting on a promise")
    d.title(s, "The same move, for the third time")
    d.rows(s, [
        ("session 18", "a transcription factor held by decoy sites that are "
                       "not its promoter, and substrate held in enzyme "
                       "complex. You named the mechanism: sequestration."),
        ("session 19", "a ribosome held by every other mRNA in the cell. The "
                       "same holding — and no boundary you can put around it."),
        ("today", "a regulator held by its own downstream targets. Something "
                  "that should be free is bound by something that binds it, "
                  "and the binding is what produces the behavior.", CYAN),
    ], label_color=CYAN)
    d.foot(s, "Not an analogy across the three. Literally the same move: a molecule held by something that is not its target is not available.")
    d.notes(s,
           "I put this exact ladder on the board on 29 October and said the "
           "third row was coming. I collect on it in those words.\n "
           "Session 18's own foot says it: in all three the molecule is held "
           "by something that is not its target, so it is not available to do "
           "its job. That is the invariant — availability, not sharpness.\n "
           "If they leave today with burden, decoy titration and retroactivity "
           "as three topics, the rest of Part II will not cohere and I will be "
           "re-explaining it in session 24.")


def _goals(d):
    s = d.light()
    d.header(s, "open", "what you should be able to do by the end")
    d.title(s, "Three questions")
    d.rows(s, [
        ("the cost", "You attach a downstream module to a working circuit. "
                     "What exactly does the upstream module lose — and does "
                     "it lose level, or speed, or both?"),
        ("the knob", "Your operator binds too tightly, you think. Will a "
                     "weaker one give you the load back?"),
        ("the cure", "If you cannot reduce the load, what is left to change?"),
    ], top=2.05)
    d.notes(s,
           "The first question has a twist the room will not expect: the "
           "answer depends on one physical fact about the complex, and it is a "
           "fact you can measure. That is segment 4.\n "
           "The middle question is the one the hour turns on and almost "
           "everyone's first instinct is wrong. I vote it now and again in "
           "segment 5 — the answer is no, and there is a one-line reason.")


# ----------------------------------------------------------------- object ---
def _object(d):
    s = d.light()
    d.header(s, "segment 2", "frame  ·  the object, before any model")
    d.title(s, "What the arrow is")
    d.image_centered(s, FIG + "s21_object.png")
    d.foot(s, "Every diagram in this course has been lying about this since session 1. Reading a signal means binding it, and binding it takes it out of circulation.")
    d.notes(s,
           "The top strip is every circuit diagram they have drawn since "
           "session 1. The bottom strip is the same two modules with the "
           "molecules put back in, and the boxes are in the same places so it "
           "reads as one picture told twice.\n "
           "I point at each thing as I name it. An operator site is a piece "
           "of DNA — a promoter with operators in it, on a plasmid or on the "
           "chromosome, and the copy number IS the site count. The molecules "
           "sitting on it are the same molecules as the ones floating free; "
           "nothing about them has changed except that they are not "
           "available.\n "
           "LEDGER, left wing, stays up all period: p_tot = sites, "
           "X_T = k/gamma = the factor's unloaded abundance. Every number "
           "today is one of those two or a ratio of them, and the fact that "
           "they are DIFFERENT numbers is the whole of step three of the "
           "derivation.\n "
           "Four of the six sites are taken in the drawing. What fraction is "
           "taken is what K_d sets, and that is the quantity the affinity "
           "argument later in the hour turns on.\n "
           "The last line out loud: module B never asked for any of this. It "
           "is reading the signal, and reading it is what changes it. There "
           "is no passive measurement here.")


def _derivation(d):
    # Three length limits, all measured by the build and all three violated by
    # the first draft of session 20's run: label <= 28 chars, equation <= 56,
    # and ASIDE <= ONE LINE. theme.derivation() enables an aside at pitch
    # >= 0.70 but places it in a 0.44in box, which holds one line at the 20pt
    # floor and not two -- a two-line aside runs into the next step's
    # equation. Reported-not-fixed in theme.py; this run is written around it.
    d.derivation(
        None, "segment 3", "build  ·  the same move, a third pool",
        "What the holding costs",
        [
            ("the binding",
             "X + p <=> C",
             "the factor, the sites, and the complex"),
            ("QSSA on the binding",
             "C(X) = p_{tot}·X / (K_{d} + X)",
             "session 4's move, session 6's occupancy"),
            ("X_{T}^{inst} = X + C(X)",
             "free plus parked — NOT X_{T} = k/γ",
             "k/γ is the unloaded abundance, a different number"),
            ("differentiate it",
             "dX_{T}^{inst}/dt = (1 + R)·dX/dt,   R = dC/dX",
             "chain rule, nothing more"),
            ("dX/dt = f(X) / (1 + R)",
             "R(X) = p_{tot}·K_{d} / (K_{d} + X)²",
             "f is the law the TOTAL obeys. WHICH law is open"),
        ],
        board="R(X) = p_{tot} K_{d} / (K_{d} + X)^2",
        note="Third time they have done this move — session 4 on an enzyme, "
             "session 6 on a promoter, today on downstream sites. I say that out "
             "loud: nothing new had to be invented.\n "
             "The last line is the result. A load does not add a term to the "
             "dynamics; it DIVIDES the rate, by a factor that depends on where "
             "you are.\n "
             "LEDGER: R(X) goes up, under p_tot and X_T.\n "
             "And now the trap. f looks untouched, so it is tempting to say "
             "the steady state is untouched. But f is whatever law the TOTAL "
             "obeys, and that is not settled yet: if the parked molecules are "
             "shielded, only free X is removed and f is k − γX; if they are "
             "diluted along with everything else, f is k − γ(X + C). Those have "
             "their zeros in different places.\n "
             "The last line is where the next segment starts. Do NOT resolve "
             "it here — the room should leave this slide knowing the answer "
             "turns on a physical fact, not on a modeling choice.")


def _two_models(d):
    s = d.light()
    d.header(s, "segment 4", "frame  ·  the algebra will not answer this alone")
    d.title(s, "Does the level move, or only the speed?")
    d.rows(s, [
        ("the question", "when the factor is sitting in the complex, is it "
                         "still being degraded and diluted? Or does the site "
                         "protect it?"),
        ("if the complex is protected", "only free X is removed, "
        "so f = k − γX. Its zero does not move with the load, so "
        "the free steady state is exactly what it was. Speed cost "
        "only.", CYAN),
        ("if the complex is diluted", "both are removed, so f = k "
        "− γ(X + C). Its zero is a condition on the TOTAL, so free X "
        "falls by exactly what is parked. Both costs.", AMBER),
    ], top=2.00)
    d.foot(s, "Same algebra, two conclusions. Which one holds is a fact about the molecule, not a modeling preference.")
    d.notes(s,
           "This is where the hour turns. I "
           "want them to see that the SAME derivation gives two different "
           "answers depending on one physical question — and that the question "
           "is answerable in an afternoon.\n "
           "Both rows are the last line of the derivation with f filled "
           "in, so nothing new is assumed here. The zeros land in "
           "different places because the two laws are different laws, "
           "not because we changed our minds about the model.\n "
           "I do not tell them which one. The next slide makes them design "
           "the measurement, and Mishra answers it for their own system in "
           "segment 6.\n "
           "Both are real. A protected complex is what you get when binding "
           "buries the degron or the protein is stable and the site is the only "
           "thing holding it; dilution-dominated removal in a growing cell with "
           "an exposed complex gives the other.")

    s = d.light()
    d.header(s, "segment 4", "release  ·  design it, on paper")
    d.title(s, "Design the measurement")
    d.rows(s, [
        ("protected", "f = k − γX. Removal sees only the free pool.",
         CYAN),
        ("diluted", "f = k − γ(X + C). Removal sees everything.", AMBER),
        ("your turn", "you have a working circuit and a plasmid that "
                      "adds downstream binding sites. Design the "
                      "experiment that tells you which one your system "
                      "is in — and say what each outcome would mean."),
    ])
    d.foot(s, "Two minutes. I want the comparison and the inference, not a protocol.")
    d.notes(s,
           "Short and sharp, and almost everyone gets there — which is the "
           "point. The answer is one line and it makes the distinction feel "
           "like physics rather than bookkeeping.\n "
           "What I am fishing for: measure the FINAL level with and without "
           "the load. If it does not move, the complex is protected. If it "
           "drops, it is not. No kinetics needed, no fitting, one comparison.\n "
           "If someone proposes measuring the response time instead, that is a good wrong answer and I take it slowly: the time changes "
                                                                     "in BOTH models, so it cannot distinguish them. The level is the "
           "discriminating observable. That is a general lesson about picking an observable, and I say it as one.")

    s = d.dark()
    d.header(s, "segment 4", "debrief  ·  what you just built")
    d.title(s, "One comparison, two models separated")
    d.rows(s, [
        ("the signature", "steady state unchanged by load → the complex is "
                          "protected. Steady state drops → it is not. Nothing "
                          "else distinguishes them.", CYAN),
        ("why not the response time", "it slows in both models. A dynamic "
                                      "measurement cannot tell you which one "
                                      "you are in; the endpoint can."),
        ("and hold this", "you will see this exact comparison run, in yeast, "
                          "later this morning — and you will see which "
                          "answer their system gave."),
    ], label_color=CYAN)
    d.foot(s, "Both models predict a slowdown. Only one predicts a level shift.")
    d.notes(s,
           "LEDGER: two models, one discriminating observable — the endpoint.\n "
           "I plant the Mishra forward reference deliberately and in those "
           "words, so that when p. 1273 lands in segment 6 it is the answer to "
           "a question they asked rather than a fact about a paper.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  why a divided rate is a longer time")
    d.title(s, "Where the extra time comes from")
    d.rows(s, [
        ("the last line of the derivation", "dX/dt = f(X) / (1 + R). A load "
                                            "does not add a term to the "
                                            "dynamics. It DIVIDES the rate."),
        ("so turn it over", "dt = (1 + R)/f(X) · dX. The time to climb one "
                            "slice of X is one over the rate you climb it at."),
        ("and add the slices up", "t(0 \u2192 X*)  =  \u222b dX/f(X)   +   "
                                  "\u222b R(X)/f(X) dX", CYAN),
        ("what the two pieces are", "the first is the time it would take with "
                                    "no load at all. The second is everything "
                                    "the load costs you.", CYAN),
    ], top=2.00, label_color=CYAN)
    d.foot(s, "Every number left in this hour is that second integral, evaluated somewhere.")
    d.notes(s,
           "This is the step that turns the rest of the hour into arithmetic "
           "instead of assertion, and without it the room has to take my word "
           "for it that a divided rate is a slower response.\n "
           "Two lines on the board. Invert the rate to get time per slice, "
           "integrate, and the (1 + R) splits into the unloaded time plus a "
           "correction. Nothing clever happens.\n "
           "Then I read the second integral out loud as a product of two "
           "things, because that reading is what the next two segments are. "
           "R dX is HOW MANY molecules get parked. One over f is HOW "
           "EXPENSIVE time is at the moment they are parked — and f shrinks "
           "as X climbs, so a molecule parked late costs more delay than one "
           "parked early.\n "
           "Segment 5 does the first factor exactly, and it does not depend "
           "on affinity at all. The weight is where the leftovers live.\n "
           "I do NOT evaluate anything here. The slide is the shape of the "
           "answer, and the room should leave it knowing what it is they are "
           "about to compute.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  the diluted case, on one trace")
    d.title(s, "Three hundred sites, complex diluted")
    d.image_centered(s, FIG + "s21_step_response.png")
    d.foot(s, "The diluted model, so both costs are on the page. In the protected model this figure's plateaus would coincide.")
    d.notes(s,
           "One module, driven twice, in the DILUTED model — I say which model "
           "this figure is, every time I show it. The dotted plateaus are the "
           "levels and the dashed verticals are the half-times.\n "
           "Thirty percent off the level and fifty-one percent onto the "
           "response time. Comparable, and in this model there is no "
           "measurement that is safe from the load.\n "
           "In the protected version of this figure the two plateaus land on "
            "top of each other and only the verticals move. That is the picture for Mishra's system.")


def _thesis(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  the knob you were going to reach for")
    d.title(s, "Would a weaker operator help?")
    d.rows(s, [
        ("the instinct", "the load is molecules parked on sites. Bind more "
                         "weakly and fewer park. So a higher K_{d} should buy "
                         "the speed back."),
        ("it is a good instinct", "it is the first thing an engineer reaches "
                                  "for, and it is the thing you can "
                                  "change — K_{d} is 20 nucleotides or a few "
                                  "residues away."),
        ("vote", "yes, no, or depends. Then we will compute it rather than "
                 "arguing about it.", CYAN),
    ], top=2.00, label_color=CYAN)
    d.notes(s,
           "Second vote of the hour, hands up, and I count. Most of the room "
           "says yes.\n "
           "I want the vote ON RECORD before the next slide, because the "
           "release that follows refutes it in one line of calculus and the "
           "refutation lands much harder if they have committed.")

    s = d.light()
    d.header(s, "segment 5", "release  ·  one integral")
    d.title(s, "How much extra does the loaded system have to make?")
    d.rows(s, [
        ("compute", "the integral of R(X) dX from 0 to ∞, with R = dC/dX and "
                    "C(X) = p_{tot}·X/(K_{d} + X)."),
        ("you do not need the integrand", "you need what R is the derivative "
                                          "of, and the two endpoints."),
    ])
    d.foot(s, "No algebra required. This is a fundamental-theorem question wearing a biology costume.")
    d.notes(s,
           "Ninety seconds. R is dC/dX, so the integral is C(∞) − C(0) = "
           "p_tot − 0 = p_tot, FULL STOP. The K_d cancels because it was never in the "
           "endpoints.\n "
           "Some of the room will start trying to integrate the rational "
           "function. I let that run for about twenty seconds and then say "
           "\"look at what R IS\" — the recognition is the whole exercise.\n "
           "This is the one thing from today I want them to be able to "
           "reconstruct in June, so it goes on the board in their words before "
           "I say it in mine.")

    s = d.dark()
    d.header(s, "segment 5", "debrief  ·  why the knob does nothing")
    d.title(s, "The total you pay is the site count")
    d.rows(s, [
        ("what you just proved", "∫R dX = C(∞) − C(0) = p_{tot}, exactly, "
                                 "for every K_{d}. The affinity is not in the "
                                 "answer.", CYAN),
        ("read it physically", "the extra material the loaded system must "
                               "synthesize on its way up is the number of "
                               "sites. Full stop."),
        ("so what does K_{d} do", "it decides WHEN during the approach you pay — "
                                "early and steeply, or late and gradually. Not "
                                "how much."),
    ], label_color=CYAN)
    d.foot(s, "The vote said yes. The fundamental theorem of calculus says no.")
    d.notes(s,
           "LEDGER: integral of R dX = p_tot. Affinity sets the schedule, not "
           "the bill.\n "
           "I slow down for this sentence. And it "
           "is a CONSERVATION statement, not an observation off a parameter sweep, and that distinction matters "
                                                "more than the result itself. A sweep could "
           "always have missed a regime. A conservation argument cannot.\n "
           "Then the figure, which is now a confirmation rather than an "
           "argument.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  the bill, drawn")
    d.title(s, "Same ceiling, different approach")
    d.image_centered(s, FIG + "s21_conservation.png")
    d.foot(s, "C(X) is the running total of what has been parked. At X_{T} the four curves have paid 299.7, 295.3, 272.7 and 150.0 of a 300-site bill.")
    d.notes(s,
           "This is the conservation result as a picture, and it is the one I "
           "point at rather than the sweep. Four affinities, four different "
           "routes, and every one of them levels off at the same height. "
           "Affinity slides the curve left and right. It does not move the "
           "ceiling.\n "
           "Then the vertical line, which is the other half of the argument. "
           "The system stops climbing at X_T, so what it has ACTUALLY paid is "
           "where its own curve crosses that line. For the first three "
           "affinities that crossing is at or near the ceiling — 300, 295, "
           "273 — which is why the cost is flat across four decades.\n "
           "The red one crosses at 150. Half the bill, because the sites "
           "never filled. That is the boundary, and the sweep on the next "
           "slide is the same fact plotted against K_d.\n "
           "If someone asks why the red curve is cheaper and that is not a "
           "cure: look at where it crosses. Half the sites are empty at the "
           "operating point, so half the regulation is gone too.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  and the sweep agrees")
    d.title(s, "Seven decades of affinity")
    d.image_centered(s, FIG + "s21_affinity.png")
    d.foot(s, "Protected model, heavy load. Across four decades the cost moves 3% — not constant, SMALL, and the previous slide says why. Past K_{d} ≈ X_{T} the sites stop filling and the regulation goes too.")
    d.notes(s,
           "The x axis is SEVEN decades, 10^-2 to 10^5, and the flat claim "
           "covers the first FOUR of them: K_d from 0.01 to 100. Across those "
           "four the cost moves three percent at this load - 2.39 at K_d = "
           "100, rising to 2.47 near K_d = 16. Non-monotonic, and the "
           "conservation argument does not predict that — it counts "
           "molecules and says nothing about when they are paid. "
           "Flat, not constant: the spread grows with the load, under a "
           "percent at a tenth of this many sites and four percent at twice. "
           "The figure is the check, not the claim.\n "
           "The right-hand axis is the occupancy and it carries the boundary. "
           "While K_d sits below the factor's abundance the sites FILL during "
           "the approach, so the system pays all of p_tot. Past K_d ≈ X_T they "
           "never fill, the bill shrinks — and the occupancy shrinks with it, "
           "which means the downstream module is no longer being regulated.\n "
           "That is not a cure, it is a disconnection, and it is the same "
           "sentence as session 18's: the thing you want and the thing it "
           "costs are the same knob.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  the two costs, each in one line")
    d.title(s, "What you are actually comparing")
    d.rows(s, [
        ("the level cost", "C(X_{ss}) / X_{T}. The molecules sitting on sites "
                           "once the system has settled. A COUNT — and it is "
                           "zero in the protected model, because X_{ss} does "
                           "not move.", CYAN),
        ("the speed cost", "(1/t_{un}) · \u222b R/f dX. The same molecules, each "
                           "weighted by how slow the system was when it paid "
                           "for that one. A count with a WHEN on it.", AMBER),
        ("so why no single number relates them", "one is a count and the "
                                                 "other is a count times a "
                                                 "weight. The weight moves "
                                                 "with the load. The ratio "
                                                 "has to move with it.",
         AMBER),
    ], top=2.00, label_color=CYAN)
    d.foot(s, "Both are built from the same integral. They differ only in whether the 1/f weight is in there.")
    d.notes(s,
           "Worth slowing down, because this is the sentence that stops them "
           "memorizing 1.44 as a law. The two costs are not two unrelated "
           "numbers and they are not one number either. They are the same "
           "molecules counted two ways.\n "
           "The level cost is what is parked at the end. You can read it "
           "straight off the steady state and it needs no dynamics at all.\n "
           "The speed cost is what was parked on the WAY there, with each "
           "molecule charged at the rate the system happened to be moving. "
           "That is the second integral from segment 4.\n "
           "In the protected model the first is identically zero, so there is "
           "only ever one cost. In the diluted model both are real, and the "
           "figure next shows the ratio between them drifting from 1.44 to "
           "1.71 across the loads plotted. There is no coefficient to carry "
           "away from that, which is the point.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  so which costs do you pay?")
    d.title(s, "It depends on the complex")
    d.image_centered(s, FIG + "s21_both_costs.png")
    d.foot(s, "K_{d} = 1 throughout. Protected: one cost, flat at 1.4483 here, against 1/ln 2 = 1.4427 as the sites saturate. Diluted: two costs, and the ratio between them is not a constant.")
    d.notes(s,
           "This closes segment 4's hinge with numbers. Two costs, and "
           "the ratio between them is NOT a constant — which is more "
           "useful than a constant would have been.\n "
           "PROTECTED model, the triangles: ONE cost. The level shift is not "
           "small, it is identically zero — the solver gives 2e-16 at every "
           "load — and the speed cost sits on (p_tot/X_T)/ln 2 across the whole "
           "range.\n "
           "DILUTED model: two costs, both roughly linear at light load, but "
           "the ratio between them runs from 1.44 at the left of this figure to "
           "1.71 at the right. A clean coefficient belongs to the protected "
           "model; in the diluted model it is a light-load approximation and I "
           "say so.\n "
           "Which matters when Mishra lands: their system is the protected "
            "one, so everything they report is on the time axis.")

    s = d.dark()
    d.header(s, "segment 5", "build  ·  where 1.44 comes from")
    d.title(s, "The slowdown, in three lines")
    d.rows(s, [
        ("start from the integral", "the extra time is \u222b R/f dX — the "
                                   "second piece of the time integral, "
                                   "from earlier this morning. Nothing "
                                   "here is new."),
        ("while the sites fill, f \u2248 k", "if K_{d} is well below X_{T} the "
                                        "sites fill early, when X is still "
                                        "small and f = k \u2212 γX is still "
                                        "essentially k."),
        ("so the weight comes out", "extra time \u2248 (1/k)·\u222b R dX = "
                                    "p_{tot}/k. The integral you just did, "
                                    "divided by the synthesis rate."),
        ("against what", "the unloaded half-time, ln2 / γ. The ratio is "
                         "(p_{tot}/X_{T}) / ln 2, and 1/ln 2 = 1.4427.", CYAN),
    ], label_color=CYAN)
    d.foot(s, "Protected model. Not a fitted constant: the extra time is the time to fill the sites, measured in unloaded half-lives.")
    d.notes(s,
           "I derive this on the board rather than asserting it, because it "
           "turns a mystery coefficient into a sentence they can rebuild: the "
           "delay IS the fill time.\n "
           "Numerically the coefficient runs 1.442697 at K_d = 1e-4, against "
           "1/ln 2 = 1.442695, and RISES to 1.4483 at K_d = 1 and 1.4691 near "
           "K_d = 16 before it falls away.\n "
           "If anyone asks why it rises, two things compete and they pull "
           "opposite ways. A weaker operator means fewer molecules are parked "
           "by the time X reaches half-max — that lowers the bill. But it also "
           "means they are parked LATER in the approach, and a molecule made "
           "later costs more delay, because the system is already slowing as "
           "it nears its target. Below K_d of about 16 the timing wins; above "
           "it the shrinking bill does.\n "
           "I would only take that live if someone presses. The three-line "
           "argument is the thing worth keeping and it is exact in the "
           "saturated limit.\n "
           "LEDGER: slowdown − 1 = (p_tot/X_T)/ln 2 in the weak, saturated "
           "limit.\n "
           "The coefficient is derivable in three lines, so it belongs in the "
           "hour rather than parked as a 247 exercise.")


# ----------------------------------------------------------------- Mishra ---
def _mishra(d):
    # The device goes up BEFORE anything is claimed about it. Until 1 November
    # this segment opened with three rows naming proteins in a circuit the room
    # had not seen, and the circuit arrived on the following slide.
    s = d.light()
    d.header(s, "segment 6", "frame  ·  somebody measured this")
    d.title(s, "A load you can count, in yeast")
    d.paper_figure(s, "mishra2014_fig1", (W - 7.41) / 2, 1.78, 7.41, 3.9,
                   "Mishra et al. 2014, Fig. 1c-e",
                   "unbuffered, and buffered by the phosphotransfer cascade",
                   show_caption=True)
    d.foot(s, "Doxycycline in, GFP out. The load is extra copies of the target promoter on high-copy plasmids — more binding sites, and nothing else.")
    d.notes(s,
           "The circuit before the claim. Panel d is the plain one: "
           "doxycycline makes SKN7m, it binds the promoter, GFP comes out. "
           "Panel e inserts the cascade — STAT5-HKRR, phosphorylated, handing "
           "phosphate to YPD1, two YPD1 activating SKN7.\n "
           "I trace the path with a finger before I say a single number about "
           "it, and I point at where the LOAD attaches: the plasmid copies of "
           "P_TR-SSRE. Those are the operator sites from this morning's first "
           "picture, in a real organism, at a copy number somebody chose.\n "
           "The extra stage in panel e is the whole device, and it is made of "
           "the object from session 18.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  what it is made of")
    d.title(s, "The parts, and why they bothered")
    d.rows(s, [
        ("the chassis", "S. cerevisiae, a hot1Δ hog1Δ sln1Δ background, so "
                        "the native osmolarity signaling is out of the way."),
        ("the load", "extra copies of the target promoter on high-copy 2µ "
                     "plasmids. Everything else is single-copy chromosomal."),
        ("the proteins", "SKN7 and YPD1 carry the signal; SLN1's domains "
                         "appear in the chimera. YPD1 and SLN1 you met on "
                         "Tuesday the 27th, in Mishra 2021, doing a "
                         "different job. SKN7 is new today."),
        ("why they built it", "a part you can connect a module to without "
                              "the module changing — \"fundamental building "
                              "blocks in the creation of complex, "
                              "higher-level genetic circuits.\" p. 1268.",
         CYAN),
    ], top=1.92, label_color=CYAN)
    d.notes(s,
           "Their own sentence for why this is worth building, and it is the "
           "Part II thesis in their words: a module whose behavior changes "
           "when you connect it is not a part, and a field that cannot make "
           "parts cannot compose anything.\n "
           "I flag the two Mishras again, out loud. 2021 was the "
           "phospho-toggle on Tuesday the 27th; 2014 is the load driver. Same "
           "first author, same senior author — the same Deepak Mishra, "
           "reusing the same yeast chassis, nine days apart on this "
           "syllabus.\n "
           "Careful on the chassis row: HOG1 and HOT1 are DELETED in this "
           "background, so they are not part of the device. SLN1 is in there "
           "as domains of the STAT5-HKRR chimera.\n "
           "YPD1 and SLN1 they have, from session 18. SKN7 they do NOT — it "
           "is not in the 2021 paper at all, so I introduce it rather than "
           "assuming it. The triple deletion is there for the same reason the "
           "quintuple deletion was in the other paper.\n "
           "The translation to our notation goes on the board here, because "
           "segment 7 runs on it. Their Box 1 is dy/dt = G(u − y) − r and "
           "dc/dt = r, so d(y + c)/dt = G(u − y). Against our d(X + C)/dt = "
           "f(X): our X is their y (ppSKN7), our C is their c, our p_tot is "
           "their p, and our f(X) is their G(u − y). Their u is the INPUT, "
           "STAT5-HKRR — it has no counterpart in our one-module picture, and "
           "pairing X with u is the mistake to avoid.")

    s = d.light()
    d.header(s, "segment 6", "debrief  ·  the measurement you designed, already run")
    d.title(s, "Three loads. Three rise times. One plateau.")
    # Height-limited, so the box width is not what sets the rendered size. The
    # caption went into the foot: drawn as well it collided with it.
    d.paper_figure(s, "mishra2014_fig3a", (W - 9.2) / 2, 1.68, 9.2, 4.24,
                   "Mishra et al. 2014, Fig. 3a — unbuffered, step up", "",
                   show_caption=False)
    d.foot(s, "0×, 1× and 2× load plasmids, error bars s.d., n = 3. The curves separate on the way up and land together: the level does not move, so the complex is protected. p. 1273.")
    d.notes(s,
           "This is the payoff of the measurement they designed, and I say so "
           "in those words: you asked for the final level with load and "
           "without, and here it is, run in a growing culture, with the "
           "answer.\n "
           "I make them read it before I say anything. Three curves, black "
           "and blue and red, no load and one copy and two. They come apart "
           "in the middle and they end in the same place, a little under "
           "three thousand. Same level, different time — which is the left "
           "column of the board.\n "
           "Their sentence for it: \"neither the inclusion of the load driver "
           "nor the presence of load affected the final steady state ... "
           "consistent with a system in which the interconnecting species "
           "(SKN7m) is protected from degradation when bound to DNA.\" The "
           "first four words matter — it is about the UNBUFFERED system, "
           "which is this panel.\n "
           "They also say this contrasts with studies where the complex is "
           "NOT protected, and that those systems do show steady-state "
           "effects. Both models are real and the literature has both. One "
           "sentence, so nobody files protected as the universal answer.\n "
           "LEDGER: Mishra = protected model = speed cost only.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  the same step, on the buffered circuits")
    d.title(s, "One of these is the repair. The other is a warning.")
    d.paper_figure(s, "mishra2014_fig3b", 0.72, 1.95, 5.60, 3.45,
                   "Fig. 3b — buffered, LOW expression", "", show_caption=False)
    d.paper_figure(s, "mishra2014_fig3c", 7.02, 1.95, 5.60, 3.45,
                   "Fig. 3c — buffered, MODERATE expression", "",
                   show_caption=False)
    d.foot(s, "Left: the plateaus separate, so these levels DO drop with load — p. 1272. Right: three curves, one line. That is the circuit every number in this segment comes from.")
    d.notes(s,
           "Two panels, and the room should read them before I talk. On the "
           "left the three curves end at different heights. On the right they "
           "are indistinguishable.\n "
           "The left one is the other column of our board, measured: \"the "
           "final output levels of the buffered system with low SKN7 and YPD1 "
           "expression were reduced as a result of load\" (p. 1272). So the "
           "diluted-looking behavior is not hypothetical — it is in this "
           "paper, two panels away from the protected one.\n "
           "What separates them is not the model, it is the ABUNDANCE. With "
           "enough SKN7 and YPD1 around, the sites are a small perturbation "
           "on a large pool. Their own qualifier: \"provided that the amounts "
           "of SKN7 were sufficiently high.\"\n "
           "So there are two different rescues in this paper and I name both: "
           "the unbuffered circuit is level-flat because the complex is "
           "protected, and the moderate buffered one is level-flat because "
           "there is plenty of protein. If somebody spots that both are flat "
           "and asks whether that undercuts the argument, it does not — the "
           "protected claim is about the unbuffered circuit, and the quote is "
           "about that one.\n "
           "The right-hand panel is also the repair working, three slides "
           "early. I let them see it and say we will come back to how.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  what the load cost them")
    d.title(s, "Minutes, not percentages")
    d.rows(s, [
        ("no load", "the circuit reaches 90% of its unloaded final "
                    "level in 396 ± 23 minutes."),
        ("with the load", "699 ± 48 minutes to the same mark. Same "
                          "circuit. The only change is extra binding "
                          "sites downstream."),
        ("the abstract calls this", "a 76% delay. That is these two numbers, "
                                    "and the two numbers are the measurement."),
    ], top=2.00)
    d.foot(s, "Mishra et al. 2014, Online Methods, unbuffered system, n = 3. Both rows are timed to 90% of the UNLOADED mean — a mark they can only share because the level is flat.")
    d.notes(s,
           "I give them the minutes and keep the percentage subordinate. A "
           "percentage carries a denominator convention; 396 and 699 are what "
           "was measured.\n "
           "Nearly six hours longer, from adding plasmid copies of a promoter "
           "that is not even in the circuit's signaling path — it is just "
           "downstream sites.\n "
           "And the level did not move, which they have now seen on the "
           "figure rather than been told. The whole cost landed on the "
           "clock.\n "
           "Worth one sentence on the convention, because it is this "
           "session's own thesis turning up inside their methods: both times "
           "are to 90% of the UNLOADED mean, not to 90% of each trajectory's "
           "own plateau. That metric is only meaningful because the steady "
           "state does not move. In the diluted model it would be measuring "
           "the level shift and the slowdown at once, and you could not "
           "separate them.")


def _repair(d):
    s = d.light()
    d.header(s, "segment 7", "frame  ·  the first repair in Part II")
    d.title(s, "If you cannot lower the cost, outrun it")
    d.rows(s, [
        ("their notation", "the bandwidth of a module is α·G. G is how "
                           "fast the stage is; α is the fraction retroactivity "
                           "leaves you."),
        ("what you cannot do", "lower the load. You proved that this morning — "
                               "the bill is the site count and the affinity "
                               "knob does not touch it."),
        ("so the move is", "raise G. Put a fast stage between the two "
                           "modules, fast enough that α·G is still above every "
                           "input frequency you care about.", CYAN),
        ("what they used", "a phosphotransfer cascade — session 18's covalent "
                           "cycle, running in seconds against transcription's "
                           "minutes to hours."),
    ], top=1.92, label_color=CYAN)
    d.foot(s, "The repair is on a different axis from the damage: not a smaller load, a faster stage.")
    d.notes(s,
           "The move lands because segment 5 closed the other door. They know the load is fixed, so the only "
           "remaining variable is speed.\n "
           "And the device is session 18's object. The thing that fixes "
           "retroactivity is the covalent cycle they spent an hour on nine "
           "days ago, and I say so.\n "
           "Timescales: transcription is minutes to hours, phosphotransfer is "
           "sub-second. That gap is the entire engineering margin.")

    s = d.light()
    d.header(s, "segment 7", "build  ·  how their alpha relates to our "
    "R")
    d.title(s, "The same shape, a different regime")
    d.rows(s, [
        ("what Box 1 prints", "α = 1/(1 + p/K_{d}) — p. 1270. Their p is held "
                              "constant; there is no site conservation in that "
                              "box."),
        ("what that is, in ours", "our 1/(1 + R) with R evaluated at X = 0 "
                                  "— the empty-site limit, where nothing has "
                                  "filled yet."),
        ("and we cannot close it", "their own Fig. 4c gives α = "
                                   "0.0140/0.0175 = 0.80, and inverting "
                                   "Box 1 makes that p/K_{d} = 0.25. Our "
                                   "p_{tot} and K_{d} "
                                   "are invented teaching numbers, so there "
                                   "is nothing here to check that against — "
                                   "their values are in a Supplement we do "
                                   "not hold.", AMBER),
    ], top=1.98, label_color=TEAL)
    d.foot(s, "Their formula and our derivation agree where the sites are empty and part company where they are full. Which regime their system is in, we cannot say from what we hold.")
    d.notes(s,
           "I am deliberately NOT claiming their α is our R, and it would be "
           "false to: their Box 1 holds the free site concentration constant, "
           "ours conserves sites, and the two coincide only when X is far below "
           "K_d — the "
           "opposite of the saturated regime our whole result lives in.\n "
           "Saying so costs me nothing and buys something. The room has "
           "just spent an hour on a conserved-site model, and the "
           "published simplified one is a different model that happens to "
           "agree with ours in a corner. Naming the corner is the lesson. "
           "I do NOT claim their number fails to reproduce ours — we hold "
           "no parameters of theirs to try it with, which is what the "
           "third row says.\n "
           "Their Supplementary Note 1.2 may state α with saturation; I do not "
           "have it, and I say that rather than guessing. It is on the 247 list "
           "as a reconciliation problem.\n "
           "If nobody asks, I move on. If someone does, I say so and take "
           "question of the hour and I say so.")

    s = d.light()
    d.header(s, "segment 7", "build  ·  and it works")
    d.title(s, "What the fast stage buys")
    d.image_centered(s, FIG + "s21_bandwidth.png")
    d.foot(s, "Our plot of the four bandwidths in Mishra 2014, Fig. 4c — not their panel. The values are CALCULATED, as their caption says; the measurement is the amplitude response behind them.")
    d.notes(s,
           "Plain circuit: 0.0175 per minute unloaded, 0.0140 loaded. That is "
           "20% of the bandwidth it had — I give the ratio both ways, because "
           "the paper's 25% divides by the loaded value and the convention is "
           "exactly the kind of thing that gets copied without checking.\n "
           "With the load driver: 0.0142 and 0.0143. The paper calls that "
           "difference negligible and puts it at 0.5%; the two rounded figures "
           "I just read out divide to 0.7%, and the gap is the rounding, not a "
           "disagreement - so I quote their number as theirs. Either way the "
           "circuit stopped caring whether anything was listening.\n "
           "I am careful to call these CALCULATED. The caption says \"dotted "
           "lines correspond to calculated bandwidths\" and panel b is "
           "simulation from a fitted parameter set — the amplitudes are the "
           "data, the bandwidths are read off a model of it. So they are not "
           "measured points to scatter on a derived curve — that curve was "
           "fitted through them by construction, and drawing it that way "
           "would be circular.\n "
           "Their published panel also states its two unbuffered bandwidths in "
           "the reverse order in the caption and colors its guide lines "
           "opposite to the curves they belong to, so anyone reading it "
           "color-to-color gets the result backwards. I point at it as a "
           "figure-reading lesson.")

    s = d.light()
    d.header(s, "segment 7", "build  ·  the panel those numbers came off")
    d.title(s, "Their figure, and how to read it")
    # Slot at the crop's OWN aspect (2134x628 = 3.398). At 6.9x3.9 the
    # panel filled 52% of its box and rendered 2in tall, which is not
    # readable, and this slide exists to be read closely.
    d.paper_figure(s, "mishra2014_fig4c", (W - 10.0) / 2, 2.20, 10.0, 2.95,
                   "Mishra et al. 2014, Fig. 4c",
                   "amplitude against injection frequency, with the "
                   "calculated bandwidths marked",
                   show_caption=True)
    d.foot(s, "Two traps in one panel: the caption lists the unbuffered bandwidths in the reverse order from the plot, and the dotted guide lines are colored opposite to the curves they belong to.")
    d.notes(s,
           "Worth the minute. Anyone reading this panel color to color gets "
           "the result backwards, and the paper is not a sloppy one — this "
           "is what a figure error looks like in a good journal.\n "
           "How to see it from the floor. The dotted horizontals are the "
           "minus-three-decibel marks, each at its own curve's peak over "
           "root two. The black curve peaks near 195, so its mark belongs "
           "at about 138 — and the line drawn there is RED. The red curve "
           "peaks near 110, so its mark belongs at about 78 — and that "
           "line is BLACK. Read it color to color and you get the two "
           "bandwidths the wrong way round.\n "
           "How I caught it: the caption's numbers do not match the order "
           "of the curves, so I rendered the panel and read the crossings "
           "off the plot rather than trusting either.\n "
           "The general move is the one I want them to keep. When a caption "
           "and a plot disagree, the plot is the measurement and the caption "
           "is prose about it.")

    s = d.light()
    d.header(s, "segment 7", "release  ·  size the stage")
    d.title(s, "Did the repair make it faster?")
    d.rows(s, [
        ("the four numbers", "plain circuit, 0.0175 unloaded and 0.0140 "
                             "loaded. With the load driver, 0.0142 and "
                             "0.0143. All per minute."),
        ("your input", "something that cycles once an hour, so 0.0167 per "
                       "minute. Which of those four circuits tracks it?"),
        ("then the real question", "the load driver sits in the circuit "
                                   "whether or not anything is attached. "
                                   "Compare 0.0175 against 0.0142 and say "
                                   "what the repair actually bought you.",
         CYAN),
    ], top=2.00, label_color=CYAN)
    d.foot(s, "Ninety seconds, and the second question is the one worth arguing about.")
    d.notes(s,
           "The first part is arithmetic and it is meant to be: one cycle an "
           "hour is 0.0167 per minute, and exactly one of the four numbers "
           "sits above it — the plain circuit with nothing attached. The "
           "loaded one does not track it, and neither does the buffered one, "
           "loaded or not.\n "
           "The second part is where the room should get uncomfortable. "
           "0.0175 down to 0.0142 is nineteen percent of the bandwidth, paid "
           "the moment the driver is in the circuit — against the twenty "
           "percent the load itself would have taken. The repair did not "
           "give the speed back. It bought a circuit whose speed does not "
           "depend on what is listening, and it paid roughly the full price "
           "of the damage to do it.\n "
           "Predictability over performance is the trade, and it is the "
           "right trade for a part somebody else will connect to. It is also "
           "the premium, in the frequency domain, and the next segment finds "
           "the same premium on the clock.\n "
           "Same cautions as everywhere else in this paper: these four are "
           "CALCULATED, they carry no error bars, and the buffered and plain "
           "circuits are different strains. If someone raises that here, "
           "they have arrived at segment 8 early and I tell them so.")


def _cost(d):
    s = d.light()
    d.header(s, "segment 8", "frame  ·  the part the abstract leaves out")
    d.title(s, "Insulation is not free")
    d.rows(s, [
        ("the same premium, in minutes", "you just read nineteen percent of "
                                         "the bandwidth gone, load or no "
                                         "load. It shows up on the clock "
                                         "too.", AMBER),
        ("buffered, with the load", "423 ± 22 minutes — within error of its "
                                    "own unloaded value. The repair works."),
        ("buffered, with NO load", "432 ± 9 minutes, against 396 ± 23 for "
                                   "the plain circuit with no load driver in "
                                   "it."),
        ("so the claim would be", "about 9% of response time, paid whether or "
                                  "not there is a load to drive. You bought "
                                  "immunity and the premium is always due."),
    ], top=1.94, label_color=CYAN)
    d.foot(s, "Read off their own Online Methods, n = 3. Every insulator costs something. Whether THIS number measures it is the next slide.")
    d.notes(s,
           "This is in their Online Methods and not in the abstract, and the "
           "honest close to the hour is to interrogate it rather than repeat "
           "it.\n "
           "The last row is a CLAIM, not a result, and I pause on the word "
           "\"would\". The next slide is the room's job.")

    s = d.light()
    d.header(s, "segment 8", "release  ·  read their numbers")
    d.title(s, "Is the 9% real?")
    d.image_centered(s, FIG + "s21_response_times.png")
    d.foot(s, "Every rise time in the paper, with its spread. Ninety seconds: would you report a 9% insulation cost from this, and what would you need in order to claim it?")
    d.notes(s,
           "They can do this in their heads to within a factor: the difference "
           "is 36 minutes and the larger s.d. is 23, with n = 3. Welch gives "
           "t = 2.55 and p ≈ 0.10.\n "
           "The second thing I want someone to spot: the buffered series is "
           "432.4, 420.2, 423.2 across 0×, 1× and 2× load. It is "
           "NON-MONOTONIC, and the 0× value is the slowest of its own three. "
           "The within-series spread is about a third of the effect being "
           "claimed.\n "
           "Third, and strongest if it comes from the room: these are "
           "different strains carrying different constructs, not one circuit "
           "with and without a driver.\n "
           "That is why PS8 asks whether the difference is real rather than "
           "asking for a crossover load off it — the second would be grading "
           "arithmetic on a 1.5-sigma difference.")

    s = d.dark()
    d.header(s, "segment 8", "debrief  ·  what the spread says")
    d.title(s, "Three reasons to be careful, and one that decides it")
    d.rows(s, [
        ("the bars do not overlap", "396.1 ± 23.0 against 432.4 ± 8.9 — they "
                                    "clear each other by four minutes. That "
                                    "is not a significance test.", CYAN),
        ("the test", "Welch gives t = 2.55 on about 2.6 degrees of freedom, "
                     "so p ≈ 0.10. At n = 3 the standard error is the s.d. "
                     "over √3 and the tails are fat."),
        ("look along the green", "432.4, 420.2, 423.2. Non-monotonic, the "
                                 "no-load value is the slowest of its own "
                                 "three, and that spread is a third of the "
                                 "effect being claimed.", AMBER),
        ("and the one that decides it", "different strains carrying "
                                        "different constructs — not one "
                                        "circuit with and without a driver.",
         AMBER),
    ], label_color=CYAN)
    d.foot(s, "Bars that just miss each other are the most persuasive picture in biology, and at n = 3 they are worth p = 0.10.")
    d.notes(s,
           "The first row is the one I most want them to keep, and it is the "
           "opposite of what the picture suggests. Those two bars clear each "
           "other, which looks decisive, and the test on the same six "
           "numbers comes back at one in ten. Error bars at one standard "
           "deviation are not a hypothesis test and they never were.\n "
           "If the room wants the arithmetic: the difference is 36 minutes, "
           "the pooled standard error is 14.2, so t is 2.55 — and with three "
           "replicates a side there are not three degrees of freedom to "
           "spend, there are about two and a half.\n "
           "The green series is the reading I most hope comes from the "
           "floor, because it needs no statistics at all. Adding load made "
           "that circuit FASTER twice, which cannot be a load effect, so "
           "twelve minutes of it is just what this measurement does.\n "
           "The last row is the strongest and it is structural rather than "
           "statistical. No amount of replication fixes a comparison between "
           "two different strains.\n "
           "So the honest sentence is that the load driver may cost around "
           "nine percent of response time and this experiment does not "
           "establish it. That is also why PS8 asks whether the difference "
           "is real instead of asking for a number computed off it.")

    s = d.dark()
    d.header(s, "segment 8", "debrief  ·  the design ledger")
    d.title(s, "What you can now do, and what it costs")
    d.rows(s, [
        ("the cost of being read", "∫R dX = p_{tot}. The bill is the site count "
                                   "and affinity sets only the schedule.", CYAN),
        ("which cost you pay", "level and speed if the complex is diluted; "
                               "speed only if it is protected. One endpoint "
                               "comparison tells you which."),
        ("the repair", "you cannot lower α, so raise G. A stage faster than "
                       "everything around it makes the parking stop mattering."),
        ("the premium", "an insulator costs something always. Whether this "
                        "paper measured that cost at n = 3 is a question you "
                        "can now answer.", AMBER),
    ], label_color=CYAN)
    d.foot(s, "Four things on the ledger. The last one is a habit, not a fact.")
    d.notes(s,
           "This is the ledger slide and it is the thing I would want them to "
           "photograph. Everything on it was derived or measured in this room "
           "today.\n "
           "The fourth row is the one I care about most by June. They will read "
           "hundreds of papers with an effect and three replicates, and the "
           "move is always the same: look at the spread before you quote the "
           "number.")


def _close(d):
    s = d.dark()
    d.header(s, "close", "where this goes")
    d.title(s, "Three contexts, three cures, and a pattern")
    d.rows(s, [
        ("19", "the host's machinery. Measured it, budgeted against it."),
        ("20", "the host's metabolism. Computed it — and had to import an "
               "assumption to do so."),
        ("21", "the module next door. Derived it, then built a device that "
               "outruns it.", CYAN),
        ("Tuesday", "each of those cures is specific to its disturbance. Next "
                    "week: a controller that does not need to know what the "
                    "disturbance is."),
    ], label_color=CYAN)
    d.foot(s, "Three patches. Then the question of whether you can stop patching.")
    d.notes(s,
           "I name the escalation. Measure, compute, insulate — each one is "
           "tailored to its own problem, and that is the limitation session 22 "
           "attacks.\n "
           "Two molecules that annihilate each other are an integrator, and an "
           "integrator does not need to know what hit it. That one sentence is "
           "Tuesday.")

    s = d.light()
    d.header(s, "close", "before Tuesday")
    d.title(s, "What to read, and what is due")
    d.rows(s, [
        ("tonight, 11:59", "PS7 is due."),
        ("today", "PS8 goes out. Session 18, Tuesday, today and next "
                  "Tuesday — four sessions, one set."),
        ("the paper", "Aoki et al., Nature 2019. Read the step responses, "
                      "then ask what dilution does to the guarantee."),
    ], top=2.05)
    d.assignment(s, y=4.70)
    d.notes(s,
           "PS8 reaches into a session they have not had yet, which is deliberate and I say so — the control questions are "
                                                              "answerable after Tuesday.\n "
           "The dilution question is the whole of session 22's argument and I "
           "want them arriving with it already bothering them. It is also "
           "today's two models again: dilution is exactly what decides whether "
           "a bound molecule is still being removed.")
