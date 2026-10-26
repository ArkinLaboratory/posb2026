"""Session 21 — Retroactivity: reading a signal changes it.

Thursday 5 November 2026. PS7 is due today; PS8 is posted today.
Mishra 2014 was assigned at the close of session 20. Aoki is assigned today.

WHAT THIS SESSION IS. Rung 3 of the ladder, and two things make it different
from the two before it. First, it is the THIRD instance of one mechanism and
the room has already been told to expect it -- session 19's close surface put a
three-row ladder on the board and its note calls that "the surface the hour
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
same yeast chassis, which is a better beat than a surname coincidence. Every student-facing surface cites the year.

WHAT SESSION 18 ACTUALLY TAUGHT. It taught decoy sites explicitly (segment 4,
"held by DECOY SITES that are not its promoter ... Titration") and named
SEQUESTRATION as the through-line. But its sharpness came from ZERO-ORDER
saturation -- "an apparent Hill coefficient of 26 from one site, with no
cooperative binding" -- and in s18 sequestration SOFTENED the switch. So the
ladder may not say the holding is what made it sharp. s19's close surface
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
           "than characterising a problem, and I say so early — rungs one and "
           "two diagnosed, this one repairs.\n "
           "And it is the third time they meet one mechanism. I promised them "
           "that on Thursday the 29th and the next surface collects on it.")


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
           "need it loaded before the next surface.\n "
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
                  "and the binding is what produces the behaviour.", CYAN),
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
    d.header(s, "open", "what you should be able to do by 9:30")
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
    d.rows(s, [
        ("the diagram", "an arrow from module A to module B. Arrows carry "
                        "information and cost nothing."),
        ("the molecule", "an operator site. A piece of DNA that BINDS the "
                         "transcription factor and holds it — takes it out of "
                         "circulation while it is there."),
        ("so the numbers that matter", "how many sites, and how many molecules "
                                       "of the factor. Call them p_tot and "
                                       "X_T."),
        ("and notice", "the downstream module did not ask for this. It is "
                       "reading the signal, and reading it is what changes it."),
    ], top=1.98)
    d.foot(s, "Every diagram in this course has been lying about this since session 1.")
    d.notes(s,
           "I name the molecules out loud: this is a promoter with operators in "
           "it, on a plasmid or on the chromosome, and the copy number is the "
           "site count.\n "
           "LEDGER, left wing, stays up all period: p_tot = sites, "
           "X_T = k/gamma = the factor's unloaded abundance. Every number "
           "today is one of those two or a ratio of them.\n "
           "Reading a signal changes it. There is no passive measurement here, "
           "because measuring means binding.")


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
            ("X + p ⇌ C",
             "the factor, the sites, and the complex",
             None),
            ("QSSA on the binding",
             "C(X) = p_tot·X / (K_{d} + X)",
             "session 4's move, session 6's occupancy"),
            ("X_{T} = X + C(X)",
             "total is free plus parked",
             None),
            ("dX_{T}/dt = (1 + R)·dX/dt",
             "with R = dC/dX",
             "chain rule, nothing more"),
            ("dX/dt = f(X) / (1 + R)",
             "R(X) = p_tot·K_{d} / (K_{d} + X)²",
             "the load divides the rate"),
        ],
        board="R(X) = p_tot K_d / (K_d + X)^2",
        note="Third time they have done this move — session 4 on an enzyme, "
             "session 6 on a promoter, today on downstream sites. I say that out "
             "loud: nothing new had to be invented.\n "
             "The last line is the result. A load does not add a term to the "
             "dynamics; it DIVIDES the rate, by a factor that depends on where "
             "you are.\n "
             "LEDGER: R(X) goes up, under p_tot and X_T.\n "
             "And now the trap. f(X) looks untouched, so it is tempting to say "
             "the steady state is untouched. Whether that is true depends on a "
             "physical question I have not asked yet, and the next segment is "
             "that question. Do NOT resolve it here.")


def _two_models(d):
    s = d.light()
    d.header(s, "segment 4", "frame  ·  the algebra will not answer this alone")
    d.title(s, "Does the level move, or only the speed?")
    d.rows(s, [
        ("the question", "when the factor is sitting in the complex, is it "
                         "still being degraded and diluted? Or does the site "
                         "protect it?"),
        ("if the complex is protected", "then only free X is removed. "
                                        "f(X) = 0 is untouched, so the steady "
                                        "state of free X is exactly what "
                                        "it was, at every load. Speed cost "
                                        "only."),
        ("if the complex is diluted", "then total removal counts both. "
                                      "X + C is pinned at k/γ and free X "
                                      "falls by exactly what is parked. Both "
                                      "costs."),
    ], top=2.00)
    d.foot(s, "Same algebra, two conclusions. Which one holds is a fact about the molecule, not a modelling preference.")
    d.notes(s,
           "This is the hinge of the hour and it used to be a throwaway. I "
           "want them to see that the SAME derivation gives two different "
           "answers depending on one physical question — and that the question "
           "is answerable in an afternoon.\n "
           "I do not tell them which one. The next surface makes them design "
           "the measurement, and Mishra answers it for their own system in "
           "segment 6.\n "
           "Both are real. A protected complex is what you get when binding "
           "buries the degron or the protein is stable and the site is the only "
           "thing holding it; dilution-dominated removal in a growing cell with "
           "an exposed complex gives the other.")

    s = d.light()
    d.header(s, "segment 4", "release  ·  two minutes, on paper")
    d.title(s, "Design the measurement")
    d.rows(s, [
        ("the question", "You have a working circuit and a plasmid that adds "
                         "downstream binding sites. Design the experiment that "
                         "tells you which of those two models your system is "
                         "in."),
        ("you have what you need", "two steady states and one perturbation. "
                                   "Say what you measure and what each outcome "
                                   "would mean."),
    ])
    d.foot(s, "Two minutes. I want the comparison and the inference, not a protocol.")
    d.notes(s,
           "Short and sharp, and almost everyone gets there — which is the "
           "point. The answer is one line and it makes the distinction feel "
           "like physics rather than bookkeeping.\n "
           "What I am fishing for: measure the FINAL level with and without "
           "the load. If it does not move, the complex is protected. If it "
           "drops, it is not. No kinetics needed, no fitting, one comparison.\n "
           "If someone proposes measuring the response time instead, that is a "
           "good wrong answer and worth a beat: the time changes in BOTH "
           "models, so it cannot distinguish them. The level is the "
           "discriminating observable. That is a general lesson about picking "
           "an observable and it is worth saying as one.")

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
    d.header(s, "segment 4", "build  ·  the diluted case, on one trace")
    d.title(s, "Three hundred sites, complex diluted")
    d.image(s, FIG + "s21_step_response.png", M + 1.05, 1.72, w=7.2)
    d.foot(s, "The diluted model, so both costs are on the page. In the protected model this figure's plateaus would coincide.")
    d.notes(s,
           "One module, driven twice, in the DILUTED model — I say which model "
           "this figure is, every time I show it. The dotted plateaus are the "
           "levels and the dashed verticals are the half-times.\n "
           "Thirty percent off the level and fifty-one percent onto the "
           "response time. Comparable, and in this model there is no "
           "measurement that is safe from the load.\n "
           "Worth saying what the protected version of this figure looks like: "
           "the two plateaus land on top of each other and only the verticals "
           "move. That is the picture for Mishra's system.")


def _thesis(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  the knob you were going to reach for")
    d.title(s, "Would a weaker operator help?")
    d.rows(s, [
        ("the instinct", "the load is molecules parked on sites. Bind more "
                         "weakly and fewer park. So a higher K_d should buy "
                         "the speed back."),
        ("it is a good instinct", "it is the first thing an engineer reaches "
                                  "for, and it is the thing you can "
                                  "change — K_d is 20 nucleotides or a few "
                                  "residues away."),
        ("vote", "yes, no, or depends. Then we will compute it rather than "
                 "arguing about it.", CYAN),
    ], top=2.00, label_color=CYAN)
    d.notes(s,
           "Second vote of the hour, hands up, and I count. Most of the room "
           "says yes.\n "
           "I want the vote ON RECORD before the next surface, because the "
           "release that follows refutes it in one line of calculus and the "
           "refutation lands much harder if they have committed.")

    s = d.light()
    d.header(s, "segment 5", "release  ·  one integral, ninety seconds")
    d.title(s, "How much extra does the loaded system have to make?")
    d.rows(s, [
        ("compute", "the integral of R(X) dX from 0 to ∞, with R = dC/dX and "
                    "C(X) = p_tot·X/(K_{d} + X)."),
        ("you do not need the integrand", "you need what R is the derivative "
                                          "of, and the two endpoints."),
    ])
    d.foot(s, "No algebra required. This is a fundamental-theorem question wearing a biology costume.")
    d.notes(s,
           "Ninety seconds. R is dC/dX, so the integral is C(∞) − C(0) = "
           "p_tot − 0 = **p_tot**. The K_d cancels because it was never in the "
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
        ("what you just proved", "∫R dX = C(∞) − C(0) = p_tot, exactly, "
                                 "for every K_d. The affinity is not in the "
                                 "answer.", CYAN),
        ("read it physically", "the extra material the loaded system must "
                               "synthesize on its way up is the number of "
                               "sites. Full stop."),
        ("so what does K_d do", "it decides WHEN during the approach you pay — "
                                "early and steeply, or late and gradually. Not "
                                "how much."),
    ], label_color=CYAN)
    d.foot(s, "The vote said yes. The fundamental theorem of calculus says no.")
    d.notes(s,
           "LEDGER: integral of R dX = p_tot. Affinity sets the schedule, not "
           "the bill.\n "
           "This is the sentence of the hour and I slow down for it. It is also "
           "the honest version of a claim an earlier draft of this session got "
           "wrong — that draft asserted affinity-independence as an empirical "
           "observation from a parameter sweep. It is a conservation statement, "
           "and a conservation statement is worth more than a sweep.\n "
           "Then the figure, which is now a confirmation rather than an "
           "argument.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  and the sweep agrees")
    d.title(s, "Four decades of affinity")
    d.image(s, FIG + "s21_affinity.png", M + 0.75, 1.62, w=7.8)
    d.foot(s, "The protected model, a heavy load. The cost barely moves until the sites stop filling — and then the regulation goes with it.")
    d.notes(s,
           "Under 3% across four orders of magnitude, which is what the "
           "integral said it would be. The figure is the check, not the claim.\n "
           "The right-hand axis is the occupancy and it carries the boundary. "
           "While K_d sits below the factor's abundance the sites FILL during "
           "the approach, so the system pays all of p_tot. Past K_d ≈ X_T they "
           "never fill, the bill shrinks — and the occupancy shrinks with it, "
           "which means the downstream module is no longer being regulated.\n "
           "That is not a cure, it is a disconnection, and it is the same "
           "sentence as session 18's: the thing you want and the thing it "
           "costs are the same knob.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  so which costs do you pay?")
    d.title(s, "It depends on the complex")
    d.image(s, FIG + "s21_both_costs.png", M + 0.75, 1.68, w=7.8)
    d.foot(s, "Protected: one cost, and it lands exactly on (p_tot/X_T)/ln2. Diluted: two costs, and the ratio between them is not a constant.")
    d.notes(s,
           "This closes segment 4's hinge with numbers, and it is the "
           "correction to a claim this session used to make — that both costs "
           "sat in one fixed ratio. They do not, and the truth is more useful.\n "
           "PROTECTED model, the triangles: ONE cost. The level shift is not "
           "small, it is identically zero — the solver gives 2e-16 at every "
           "load — and the speed cost sits on (p_tot/X_T)/ln 2 across the whole "
           "range.\n "
           "DILUTED model: two costs, both roughly linear at light load, but "
           "the ratio between them runs from 1.44 at the left of this figure to "
           "1.71 at the right. A clean coefficient belongs to the protected "
           "model; in the diluted model it is a light-load approximation and I "
           "say so.\n "
           "Which matters for Mishra, in twenty minutes: their system is the "
           "protected one, so everything they report is on the time axis.")

    s = d.dark()
    d.header(s, "segment 5", "build  ·  where 1.44 comes from")
    d.title(s, "The slowdown, in three lines")
    d.rows(s, [
        ("in the protected model", "the target never moves — X_ss is k/γ at "
                                   "every load. So \"half way\" means the same "
                                   "number of molecules loaded or not, and the "
                                   "comparison is clean."),
        ("at half-max the sites are full", "if K_d is well below X_T they filled "
                                           "before. So the loaded system has "
                                           "made p_tot extra molecules to get "
                                           "to the same place."),
        ("that costs time", "at synthesis rate k, making p_tot extra molecules "
                            "takes p_tot / k."),
        ("against what", "the unloaded half-time, ln2 / γ. The ratio is "
                         "(p_tot/X_T) / ln 2, and 1/ln 2 = 1.4427.", CYAN),
    ], label_color=CYAN)
    d.foot(s, "Protected model. Not a fitted constant: the extra time is the time to fill the sites, measured in unloaded half-lives.")
    d.notes(s,
           "I derive this on the board rather than asserting it, because it "
           "turns a mystery coefficient into a sentence they can rebuild: the "
           "delay IS the fill time.\n "
           "Numerically the coefficient runs 1.4483 at K_d = 1 down to 1.442697 "
           "as K_d goes to 1e-4, against 1/ln 2 = 1.442695. The residual is the "
           "sites not being quite full at half-max.\n "
           "LEDGER: slowdown − 1 = (p_tot/X_T)/ln 2 in the weak, saturated "
           "limit.\n "
           "An earlier draft of this deck called this coefficient measured and "
           "not derivable, and proposed deriving it as a 247 exercise. It is "
           "three lines, so it belongs here.")


# ----------------------------------------------------------------- Mishra ---
def _mishra(d):
    s = d.light()
    d.header(s, "segment 6", "frame  ·  somebody measured this")
    d.title(s, "A load you can count, in yeast")
    d.rows(s, [
        ("the circuit", "doxycycline in, GFP out, in S. cerevisiae — a "
                        "hot1Δ hog1Δ sln1Δ background, so the native "
                        "osmolarity signalling is out of the way."),
        ("the load", "extra copies of the target promoter on high-copy 2µ "
                     "plasmids. Everything else is single-copy chromosomal. "
                     "The load is more binding sites, and nothing else."),
        ("the proteins", "SKN7 and YPD1 carry the signal; SLN1's domains "
                         "appear in the chimera. You met this pathway on "
                         "Tuesday the 27th, in a different Mishra paper doing "
                         "a different job."),
    ], top=2.00)
    d.notes(s,
           "I flag the two Mishras again, out loud. 2021 was the phospho-toggle "
           "on Tuesday the 27th; 2014 is the load driver. Same first author, same "
           "senior author — the same Deepak Mishra, reusing the same yeast "
           "chassis, nine days apart on this syllabus.\n "
           "Careful on the third row: HOG1 and HOT1 are DELETED in this "
           "background, so they are not part of the device — an earlier draft "
           "of this slide listed HOG1 among the working proteins, which is "
           "wrong. SLN1 is in there as domains of the STAT5-HKRR chimera.\n "
           "The chassis continuity is worth a beat — they already know what "
           "SKN7 and YPD1 are, and the triple deletion is there for the same "
           "reason the quintuple deletion was in the other paper.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  the two circuits, side by side")
    d.title(s, "With and without the fast stage")
    # Slot sized to the crop's OWN aspect (1426x751 = 1.899), centred, so the
    # image fills it instead of floating in an empty box -- the s19 lesson.
    d.paper_figure(s, "mishra2014_fig1", (W - 7.41) / 2, 1.78, 7.41, 3.9,
                   "Mishra et al. 2014, Fig. 1c-e",
                   "unbuffered, and buffered by the phosphotransfer cascade",
                   show_caption=True)
    d.notes(s,
           "Panel d is the plain circuit: doxycycline makes SKN7m, it binds "
           "the promoter, GFP comes out. Panel e inserts the cascade — "
           "STAT5-HKRR, phosphorylated, handing phosphate to YPD1, two YPD1 "
           "activating SKN7.\n "
           "Their symbols on this panel are u, y, p and c. Mine are X, f(X), "
           "p_tot and C. I put the pairs on the board before I trace the path, "
           "because the panel is the first time today they see the paper's "
           "notation and the translation should not wait for segment 7.\n "
           "The extra stage is the whole device, and it is made of the object "
           "from session 18.")

    s = d.dark()
    d.header(s, "segment 6", "debrief  ·  your measurement, already run")
    d.title(s, "Which model is their cell in?")
    d.rows(s, [
        ("what they did", "exactly your comparison from segment 4 — the final "
                          "level, with load and without, in exponentially "
                          "growing culture."),
        ("what they found", "\"neither the inclusion of the load driver nor "
                            "the presence of load affected the final steady "
                            "state.\" — p. 1273. No level shift.", CYAN),
        ("and they name the reason", "\"consistent with a system in which the "
                                     "interconnecting species (SKN7m) is "
                                     "protected from degradation when bound to "
                                     "DNA.\" The protected model."),
    ], label_color=CYAN)
    d.foot(s, "Mishra et al. 2014, p. 1273. So this system pays the speed cost and not the level cost — which is why the paper reports times, never levels.")
    d.notes(s,
           "This is the payoff of segment 4 and I say so explicitly: you "
           "designed this measurement forty minutes ago, and here it is, run, "
           "in a growing culture, with the answer.\n "
           "And it explains a thing they might otherwise find odd about the "
           "paper — every number in it is a time or a frequency and none is a "
           "level. That is not an oversight. In a protected system the level is "
           "not where the cost shows up.\n "
           "They also say this contrasts with other studies where the complex "
           "is NOT protected, and that those systems do show steady-state "
           "effects. Both models are real and the literature has both. Worth "
           "one sentence, because it stops the room from filing \"protected\" "
           "as the universal answer.\n "
           "LEDGER: Mishra = protected model = speed cost only.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  what the load cost them")
    d.title(s, "Minutes, not percentages")
    d.rows(s, [
        ("no load", "the circuit reaches 90% of its final level in "
                    "396 ± 23 minutes."),
        ("with the load", "699 ± 48 minutes. Same circuit. The only change "
                          "is extra binding sites downstream."),
        ("the abstract calls this", "a 76% delay. That is these two numbers, "
                                    "and the two numbers are the measurement."),
    ], top=2.00)
    d.foot(s, "Mishra et al. 2014, Online Methods. Rise time to 90% of maximum, n = 3.")
    d.notes(s,
           "I give them the minutes and keep the percentage subordinate. A "
           "percentage carries a denominator convention; 396 and 699 are what "
           "was measured.\n "
           "Nearly six hours longer, from adding plasmid copies of a promoter "
           "that is not even in the circuit's signalling path — it is just "
           "downstream sites.\n "
           "And the level did not move, which they just saw. The whole cost "
           "landed on the clock.")


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
           "The move is the thing to land here, and it lands because segment 5 "
           "closed the other door. They know the load is fixed, so the only "
           "remaining variable is speed.\n "
           "And the device is session 18's object. The thing that fixes "
           "retroactivity is the covalent cycle they spent an hour on nine "
           "days ago, and I say so.\n "
           "Timescales: transcription is minutes to hours, phosphotransfer is "
           "sub-second. That gap is the entire engineering margin.")

    s = d.light()
    d.header(s, "segment 7", "debrief  ·  how their alpha relates to our R")
    d.title(s, "The same shape, a different regime")
    d.rows(s, [
        ("what Box 1 prints", "α = 1/(1 + p/K_{d}) — p. 1270. Their p is held "
                              "constant; there is no site conservation in that "
                              "box."),
        ("what that is, in ours", "our 1/(1 + R) with R evaluated at X = 0 "
                                  "— the empty-site limit, where nothing has "
                                  "filled yet."),
        ("and we cannot close it", "inverting their own Box 1, α = 0.80 "
                                   "means p/K_{d} = 0.25. Our p_tot and K_{d} "
                                   "are invented teaching numbers, so there "
                                   "is nothing here to check that against — "
                                   "their values are in a Supplement we do "
                                   "not hold.", AMBER),
    ], top=1.98, label_color=TEAL)
    d.foot(s, "Their formula and our derivation agree where the sites are empty and part company where they are full. Which regime their system is in, we cannot say from what we hold.")
    d.notes(s,
           "I am deliberately NOT claiming their α is our R. An earlier draft "
           "of this deck said \"the same R you derived this morning\" and that "
           "is false: their Box 1 holds the free site concentration constant, "
           "ours conserves sites, and the two coincide only when X is far below "
           "K_d — the "
           "opposite of the saturated regime our whole result lives in.\n "
           "Saying so costs me nothing and buys something. The room has just "
           "spent an hour on a conserved-site model; showing them that the "
           "published simplified version does not reproduce the measured number "
           "from the same parameters is a better lesson than a tidy identity.\n "
           "Their Supplementary Note 1.2 may state α with saturation; I do not "
           "have it, and I say that rather than guessing. It is on the 247 list "
           "as a reconciliation problem.\n "
           "If nobody asks, I move on. If someone does, that is the best "
           "question of the hour and I say so.")

    s = d.light()
    d.header(s, "segment 7", "build  ·  and it works")
    d.title(s, "What the fast stage buys")
    d.image(s, FIG + "s21_bandwidth.png", M + 0.6, 1.62, w=8.1)
    d.foot(s, "Mishra 2014, Fig. 4c. These four are CALCULATED bandwidths — the caption says so; the measurement is the amplitude response behind them.")
    d.notes(s,
           "Plain circuit: 0.0175 per minute unloaded, 0.0140 loaded. That is "
           "20% of the bandwidth it had — I give the ratio both ways, because "
           "the paper's 25% divides by the loaded value and the convention is "
           "exactly the kind of thing that gets copied without checking.\n "
           "With the load driver: 0.0142 and 0.0143. Half a percent. The "
           "circuit stopped caring whether anything was listening.\n "
           "I am careful to call these CALCULATED. The caption says \"dotted "
           "lines correspond to calculated bandwidths\" and panel b is "
           "simulation from a fitted parameter set — the amplitudes are the "
           "data, the bandwidths are read off a model of it. An earlier version "
           "of this figure drew them as measured points on a derived curve, "
           "which was circular: the curve was fitted through them by "
           "construction.\n "
           "Their published panel also states its two unbuffered bandwidths in "
           "the reverse order in the caption and colours its guide lines "
           "opposite to the curves they belong to, so anyone reading it "
           "colour-to-colour gets the result backwards. Worth pointing at as a "
           "figure-reading lesson.")


def _cost(d):
    s = d.light()
    d.header(s, "segment 8", "frame  ·  the part the abstract leaves out")
    d.title(s, "Insulation is not free")
    d.rows(s, [
        ("buffered, with the load", "423 ± 22 minutes — within error of its "
                                    "own unloaded value. The repair works."),
        ("buffered, with NO load", "432 ± 9 minutes, against 396 ± 23 for "
                                   "the plain circuit with no load driver in "
                                   "it."),
        ("so the claim would be", "about 9% of response time, paid whether or "
                                  "not there is a load to drive. You bought "
                                  "immunity and the premium is always due."),
    ], top=2.00)
    d.foot(s, "Read off their own Online Methods, n = 3. Every insulator costs something — but before we spend it, look at those error bars.")
    d.notes(s,
           "This is in their Online Methods and not in the abstract, and the "
           "honest close to the hour is to interrogate it rather than repeat "
           "it.\n "
           "I read the third row as a CLAIM, not a result, and I pause on the "
           "word \"would\". The next surface is the room's job.")

    s = d.light()
    d.header(s, "segment 8", "release  ·  ninety seconds")
    d.title(s, "Is the 9% real?")
    d.rows(s, [
        ("the numbers", "432.4 ± 8.9 against 396.1 ± 23.0 minutes. Standard "
                        "deviations, n = 3 each."),
        ("the question", "would you report a 9% insulation cost from this? Say "
                         "what you would need in order to claim it."),
    ])
    d.foot(s, "Ninety seconds. You have everything you need, including a reason to be careful.")
    d.notes(s,
           "They can do this in their heads to within a factor: the difference "
           "is 36 minutes and the larger s.d. is 23, with n = 3. Welch gives "
           "t = 2.55 and **p ≈ 0.10**.\n "
           "The second thing I want someone to spot: the buffered series is "
           "432.4, 420.2, 423.2 across 0×, 1× and 2× load. It is "
           "NON-MONOTONIC, and the 0× value is the slowest of its own three. "
           "The within-series spread is about a third of the effect being "
           "claimed.\n "
           "Third, and strongest if it comes from the room: these are "
           "different strains carrying different constructs, not one circuit "
           "with and without a driver.\n "
           "An earlier draft of PS8 asked them to compute a crossover load "
           "from this number. That would have graded arithmetic on a 1.5-sigma "
           "difference, so it is now this question instead.")

    s = d.dark()
    d.header(s, "segment 8", "debrief  ·  the design ledger")
    d.title(s, "What you can now do, and what it costs")
    d.rows(s, [
        ("the cost of being read", "∫R dX = p_tot. The bill is the site count "
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
           "This is the ledger surface and it is the thing I would want them to "
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
           "PS8 reaches into a session they have not had yet, which is "
           "deliberate and worth saying — the control questions are answerable "
           "after Tuesday.\n "
           "The dilution question is the whole of session 22's argument and I "
           "want them arriving with it already bothering them. It is also "
           "today's two models again: dilution is exactly what decides whether "
           "a bound molecule is still being removed.")
