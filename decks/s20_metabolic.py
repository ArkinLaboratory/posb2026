"""Session 20 — Metabolic engineering: the coupling you can write down exactly.

Tuesday 3 November 2026. Fong & Palsson was assigned at the close of session 19.
Mishra 2014 is assigned at the close of today.

WHAT THIS SESSION IS, AND WHY IT IS NOT A TECHNIQUE LECTURE. Session 19 left the
room with a pool nobody can divide and an edge nobody can see. Today is the
opposite case: a coupling so completely known that every stoichiometric
coefficient can be written down -- and prediction is STILL hard, because
stoichiometry has no rates. So an objective has to be imported, and an objective
is a hypothesis about what selection has done, not a property of the network.

Rung 2 of the ladder (sessions/s20-metabolic/DESIGN.md section 1):
    19  competition for shared machinery   -- invisible          -> measure it
    20  stoichiometry through metabolites  -- fully specified    -> compute it,
                                                                    and find that
                                                                    is not enough
    21  sequestration at an interface      -- MIS-DRAWN          -> insulate it
    22  all of them, as disturbances                             -> reject them

NOT A FOURTH RUNG OF THE SEQUESTRATION LADDER. Session 19's close slide says
so explicitly, four days before this one: "session 20 is not a fourth rung --
it is the host's economy again at the level of metabolites." Honour that.

THE NUMBER THIS SESSION TURNS ON, and the three qualifications that make it
true. Fong & Palsson predicted the growth rate of 39 of 50 strains to within
10%, GIVEN the measured substrate and oxygen uptake rates as inputs
(Supplementary Table 1), for strains that had been EVOLVED for 25-50 days. Drop any one of those and the claim is false. A slide saying "the
model predicts knockout growth rates" is wrong in exactly the way the week-9
and week-10 retrospectives are about.

THE PAYOFF. The eleven failures do NOT share a cause, and this docstring used
to get the shape of that wrong -- it said tpi had no growth predicted on three
substrates and ppc revealed an objective slightly wrong. Corrected 31 October
to match _failures, which was rebuilt against the paper on 26 October:
  * ELEVEN IS 8 + 3. The other three -- pck- on a-ketoglutarate, zwf- on
    glucose and on glycerol -- are single replicates the authors decline to
    diagnose ("may be a result of experimental and evolutionary variability").
  * TPI- ON MALATE AND SUCCINATE WAS PREDICTED CORRECTLY. "all strains except
    tpi- on malate and succinate" (p. 1057). Only lactate is a no-growth miss.
  * THE PAPER'S ONLY DIAGNOSIS IS STRUCTURAL AND COVERS BOTH GENES: "the
    reconstructed network may be incomplete". There is no objective-function
    diagnosis in the paper to cite, so do not put one on a slide.
The real shape is that the miss depends on the SUBSTRATE, and an objective
function is the same on every substrate. Neither fix is "add more constraints".

WHERE THE NUMBERS COME FROM. sessions/s20-metabolic/NUMBERS.md, every one with
its KIND. The toy network's answers are integers and the board derives them in
six lines; posb.fba confirms them.

NO PRINTED TIME RANGES. Minutes are Adam's.

Run:  python tools/build_decks.py s20
"""
from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)

FIG = "figures/build/"
FILENAME = "s20-metabolic"


def build():
    d = Deck("Session 20 — Metabolic engineering and constraint-based design",
             session=20)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _goals(d)
    _why(d)
    _object(d)
    _overflow(d)
    _matrix(d)
    _nullspace(d)
    _cone(d)
    _program(d)
    _knockouts(d)
    _alternates(d)
    _fong(d)
    _failures(d)
    _close(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    s = d.dark()
    d.text(s, "Session 20  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "Everything is known, and it is still not enough",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "Thursday the coupling was invisible. Today you can write every "
              "coefficient of it down exactly — and you still cannot predict "
              "what the cell will do.",
           M, 4.50, 8.6, 1.2, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.45, 9.0, 0.4, size=13, color=SILVER)
    d.notes(s,
           "I open on the contrast. Thursday's edge was one nobody could see — "
           "two genes with no wire between them, and a 66.7% drop. Today the "
           "opposite: a network where every connection is known to the atom.\n "
           "Knowing it exactly buys the constraints and nothing else.")


def _retrieval(d):
    s = d.light()
    d.header(s, "open", "two from Thursday, one from further back")
    d.title(s, "Before we start")
    d.rows(s, [
        ("1", "Two genes, no regulatory connection between them. Induce one "
              "hard. What happens to the other, and what carried the effect?"),
        ("2", "Why did the fall in the first gene's output look exactly like "
              "repression by something with a Hill coefficient of one?"),
        ("3", "From session 18: a covalent cycle gets an apparent Hill "
              "coefficient above 20 from a single site. What has to be true "
              "of both enzymes for that to happen?"),
    ], top=2.05, label_w=0.7)
    d.notes(s,
           "Spaced retrieval. One and two are Thursday; three is session 18, "
           "last Tuesday.\n "
           "Answers: the second gene's output falls, carried by competition "
           "for ribosomes. It looks like Hill-1 repression because the "
           "partition function has the same shape — and the giveaway is that "
           "the apparent K moves with the REPORTER's own demand, which no "
           "real repressor's K does.\n "
           "Three: both enzymes saturated. The property belongs to the pair.")


def _goals(d):
    s = d.light()
    d.header(s, "open", "what you should be able to do by 9:30")
    d.title(s, "Three questions")
    d.rows(s, [
        ("the matrix", "You built S in session 3 and integrated with it. What "
                       "happens if you set the left-hand side to zero instead?"),
        ("the gap", "A network with more reactions than metabolites has many "
                    "steady flux states. Which one does the cell pick, and how "
                    "would you know?"),
        ("the test", "Somebody deletes six genes, evolves the strains, and "
                     "checks the predictions. Eleven are wrong. How many "
                     "different kinds of wrong is that, and how would you "
                     "tell?"),
    ], top=2.05)
    d.notes(s,
           "Goals as questions. The third one is the "
           "reading's own focus note, and I leave it open here — segment 7 is "
           "where it gets answered.\n "
           "The answer is NOT that they have nothing in common. Eight of the "
           "eleven are ppc or tpi strains, the "
           "other three are single replicates their own authors decline to "
           "diagnose, and the paper gives exactly one diagnosis for the eight. "
           "Asking HOW MANY KINDS is the question that makes the segment-7 "
           "slide land; asking what they have in common pre-loads an answer "
           "I am about to take away.")


# ----------------------------------------------------------------- object ---
# REBUILT 31 October against sessions/s20-metabolic/REBUILD.md. The segment
# used to run frame, release, debrief, build -- so the room was asked to write
# a column of S before any slide had drawn the pathway, named F6P or T3P, or
# enumerated the six balanced metabolites. F6P and T3P first appeared inside
# the question itself and P5P nine slides later. It now runs frame, build,
# release, debrief, and the release is answerable from what is on the wall.
def _why(d):
    s = d.light()
    d.header(s, "segment 1", "frame  ·  why this method exists at all")
    d.title(s, "When you cannot have the rates")
    d.rows(s, [
        ("what we have been doing", "every model this course has built runs "
                                    "on rate constants — k and γ from "
                                    "session 5, K_{d} and n from session 6, a "
                                    "Jacobian in session 8. All of it needs "
                                    "numbers."),
        ("why that stops working", "for a whole metabolism nobody has them: "
                                   "in vivo turnover numbers for most "
                                   "enzymes, real abundances, and the "
                                   "regulation on top of both."),
        ("what engineering asks", "how fast does it grow, and how much "
                                  "product comes out per gram of sugar. "
                                  "Both are steady-state questions, and a "
                                  "steady state does not remember how it "
                                  "got there.", CYAN),
        ("so: the trade", "give back the rate laws and keep what is exact "
                          "— atoms balance, a cell is made of something we "
                          "have measured, and the medium supplies what it "
                          "supplies."),
    ], top=1.95)
    d.foot(s, "No rate constant appears anywhere in this hour. That is what makes it exact, and in the next segment it is also what makes it not enough.")
    d.notes(s,
           "Why this method exists at all, before any algebra. Setting "
           "dx/dt to zero is a reason internal to the mathematics, not a "
           "reason anyone would pick up this tool.\n "
           "Every model since session 5 has had rate constants in it and they "
           "have always been available, because the systems were three species "
           "wide. At genome scale they are not available and they are not "
           "going to be. In vivo k_cat is known for a small fraction of E. coli "
           "enzymes, abundances move with condition, and the regulation on top "
           "is its own research program.\n "
           "The move I want them to see is that the question does not need "
           "them. Growth rate and yield are steady-state quantities.\n "
           "If someone asks what we give up, the answer is everything "
           "dynamic — how long it takes to get there, whether it overshoots, "
           "whether it oscillates on the way. Thursday and the week after are "
           "both about what happens when you do need those.")


def _object(d):
    s = d.light()
    d.header(s, "segment 1", "build  ·  the object, before any model")
    d.title(s, "Glucose, and the first commitment")
    d.image(s, FIG + "s20_pathway_1.png", M, 1.95, w=W - 2 * M)
    d.foot(s, "Phosphorylated on the way in, and now it is G6P: six carbons the cell has already paid for. Two ways out of G6P — what are they?")
    d.notes(s,
           "I draw this rather than name it. Half the room has had the pathway "
           "since high school and the other half has never seen it, and the "
           "half that has not cannot follow a matrix built out of arrows they "
           "have not been shown.\n "
           "The phosphate is the commitment: G6P cannot diffuse back out, so the cell has already spent an ATP to "
           "decide this molecule is staying.\n "
           "The question is a real one. I want both branches named from the "
           "floor — glycolysis, and the pentose phosphate pathway. If nobody "
           "offers the second I give it, because the next slide needs it.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  the object, before any model")
    d.title(s, "One branch to burn, one to build")
    d.image(s, FIG + "s20_pathway_2.png", M, 1.95, w=W - 2 * M)
    d.foot(s, "pgi carries on down glycolysis. zwf commits G6P to the pentose phosphate pathway, which pays a carbon as CO₂ to do it. What does the cell want out of each?")
    d.notes(s,
           "zwf by name, because it is one of the six genes they read about "
           "and it gets deleted later in the hour.\n "
           "The carbon accounting needs care here. zwf oxidises G6P to the "
           "lactone and releases nothing; pgl opens the ring; gnd does the "
           "decarboxylation. Our one arrow is all three, and on a slide "
           "about counting carbons I name the lump as one.\n "
           "The answer I am fishing for: P5P is ribose, so nucleotides — and "
           "NADPH alongside it, which our network does not carry and I say so. "
           "The glycolytic branch is carbon for everything else, plus the ATP "
           "to assemble any of it.\n "
           "Nobody volunteers 'and it costs a carbon to get there', so I point "
           "at the CO₂ and leave it a moment. The pentose phosphate pathway "
           "is not free.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  the object, before any model")
    d.title(s, "Down to pyruvate, and the first ATP")
    d.image(s, FIG + "s20_pathway_3.png", M, 1.95, w=W - 2 * M)
    d.foot(s, "lower is the rest of glycolysis on one line, T3P down to pyruvate, and it pays the first ATP. Pyruvate has two fates — which would you take?")
    d.notes(s,
           "Both of these arrows are lumps and both lumps pay off later.\n "
           "tpi here is phosphofructokinase, aldolase and the isomerase. The "
           "real triose phosphate isomerase on its own only swaps one triose "
           "for the other. That is exactly why deleting the real tpi does not "
           "shut this line off coming down from glucose — aldolase still "
           "makes one triose — and why the model does not call Fong's tpi "
           "strain dead on glucose, while it does call it dead on malate and "
           "succinate, where the line has to run upward and both trioses have "
           "to condense.\n "
           "The closing question sets up the branch. Most of the room says the "
           "TCA, because more ATP is obviously better, and that is the answer "
           "I want on the floor before I take it apart.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  the object, before any model")
    d.title(s, "Two fates for pyruvate")
    d.image(s, FIG + "s20_pathway_4.png", M, 1.95, w=W - 2 * M)
    d.foot(s, "Named enzymes, named metabolites, counted carbons. zwf, tpi and lower are each several enzymes on one line. The matrix comes after.")
    d.notes(s,
           "The pathway is complete and this is the picture the rest of the "
           "hour runs on.\n "
           "The branch is the thing to plant. Acetate against the TCA is a "
           "real decision a real cell makes, and it is the place the optimum "
           "goes all-or-nothing when we solve the thing in segment 3.\n "
           "The ATP numbers on the arrows are the toy's and the next two "
           "slides are about how far from real they are.")


# --------------------------------------------------------------- overflow ---
def _overflow(d):
    s = d.light()
    d.header(s, "segment 1", "build  ·  the branch, as a decision")
    d.title(s, "Throwing carbon away, with oxygen present")
    d.image(s, FIG + "s20_overflow.png", M + 0.35, 1.78, w=W - 2 * M - 0.7)
    d.foot(s, "A real cell excretes acetate while oxygen is plentiful. That is what overflow means, and it is what makes this a decision rather than a calculation.")
    d.notes(s,
           "I count the carbons out loud. Acetate takes two of the three and "
           "they leave the cell — a perfectly usable two-carbon molecule, "
           "poured into the medium. Down the TCA nothing is left to excrete "
           "and the energy is kept.\n "
           "Then the fact that makes it strange, and it is the reason this "
           "slide exists: a fast-growing E. coli does this with oxygen "
           "available. It is not fermenting because it has to.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  why a cell would do that")
    d.title(s, "The reason is protein, not carbon")
    d.rows(s, [
        ("it is real, and it is big", "a fast-growing E. coli pours acetate "
                                      "into the medium with oxygen available "
                                      "— reported at up to 15% of its "
                                      "glucose carbon. Holmes, Curr Top "
                                      "Cell Regul 28:69 (1986)."),
        ("and not only in bacteria", "the same behavior in a tumor cell is "
                                     "the Warburg effect. Basan et al., "
                                     "Nature 528:99 (2015)."),
        ("the reason", "respiration yields far more ATP per carbon, but it "
                       "costs more PROTEIN per ATP. When growth is fast the "
                       "proteome is what runs out, not the sugar. Basan "
                       "measured that difference by mass spectrometry.",
         AMBER),
        ("what our model will do", "it has no protein in it. Nine reactions, "
                                   "carbon and ATP and nothing else — so it "
                                   "will send every pyruvate down the TCA, and "
                                   "be wrong about a real cell for a reason we "
                                   "can already name."),
    ], top=1.90)
    d.foot(s, "Our 1 against 3 is simplified so the arithmetic can be done at the board. The real ratio is nearer an order of magnitude, and nothing in the model knows that an enzyme costs anything.")
    d.notes(s,
           "The honest version of the branch, and the first point in the hour "
           "where a constraint we have not written changes the answer. I want "
           "that sentence available in segment 3, because this is the example "
           "it is made of.\n "
           "I say the 15% out loud. That is not a rounding "
           "error, it is a sixth of the feedstock, and anyone who has run a "
           "fermentation has paid for it.\n "
           "Basan is Basan, Hui, Okano, Zhang, Shen, Williamson and Hwa. The "
           "senior author is Terry Hwa, who is the Hwa of Scott, Gunderson, "
           "Mateescu, Zhang and Hwa — session 19's paper, last Thursday. Same "
           "lab, same question in a different currency, and that connection "
           "is free so I make it.\n "
           "Their result is the one I like. The proteome cost of making ATP "
           "by respiration is higher than by fermentation, and they measured "
           "it rather than fitted it. So the cell is not being careless with "
           "carbon, it is being careful with ribosome output — the same kind "
           "of trade as Thursday, in a different currency.\n "
           "And I say plainly that the 1 and the 3 are ours, chosen so the "
           "board arithmetic stays in integers. The direction is right, the "
           "magnitude is not, and the model has no idea protein exists.")


def _matrix(d):
    s = d.light()
    d.header(s, "segment 1", "release  ·  one column, on paper")
    d.title(s, "Write one column")
    d.rows(s, [
        ("the six S balances", "G6P, F6P, P5P, T3P, PYR, ATP."),
        ("your turn", "the tpi arrow, F6P → T3P. Six entries in that "
                      "order, with signs."),
    ], top=1.68)
    d.image(s, FIG + "s20_pathway_4.png", M, 2.95, w=W - 2 * M, h=3.65)
    d.foot(s, "Consumed negative, produced positive. The coefficients are not on the picture — count carbons.")
    d.notes(s,
           "Short and concrete, and it catches the one thing nothing else in "
           "the hour would.\n "
           "The answer: −1 on F6P, +2 on T3P, zero on the other four.\n "
           "The picture is up because without it this is a memory test. The "
           "route to the 2 is on it: G6P is labelled six carbons, T3P is "
           "labelled triose phosphate, so one F6P makes two of them. Six "
           "carbons in, six carbons out. Nothing on the drawing gives them "
           "the coefficient.\n "
           "The two is what I am after. A student who writes +1 has written a "
           "reaction that destroys three carbons, and S is the only object in "
           "this course that cannot be wrong about that. If somebody writes +1 "
           "that is the best thing that happens in this segment and I use it.\n "
           "Handing them the six and the order is deliberate. The exercise is "
           "about the sign convention and the stoichiometry, not about "
           "remembering a list.")

    s = d.light()
    d.header(s, "segment 1", "debrief  ·  what you just wrote, inside S")
    d.title(s, "A column is a reaction, counted")
    d.image(s, FIG + "s20_network_annotated.png", M, 1.80, w=W - 2 * M)
    d.foot(s, "Session 3 built one of these and integrated with it. Nothing here is new except the question.")
    d.notes(s,
           "Their answer from the floor first, then the picture.\n "
           "LEDGER: a column is a reaction, a row is a metabolite, an entry is "
           "an atom count.\n "
           "The left half is the nine lines they just read off the pathway and "
           "the right half is the same nine counted. That is the whole claim. "
           "S is not an abstraction laid over the biology — it is the "
           "biology, with the atoms counted.\n "
           "And it is the only part of a cell anyone can write down exactly, "
           "and I say so here because in the next segment that same exactness is "
           "the reason it is not enough.")


def _nullspace(d):
    # THREE LENGTH LIMITS, all of them measured by the build rather than
    # guessed, and all three were violated by the first draft:
    #   step label     <= 28 chars at 20pt
    #   step equation  <= 56 chars at 20pt
    #   ASIDE          <= ONE LINE. theme.derivation() enables an aside when
    #                     the pitch is >= 0.70 but places it from y+0.42 to
    #                     y+0.86 -- a 0.44in box, which holds one line at the
    #                     20pt floor and not two. A two-line aside runs into
    #                     the NEXT step's equation. That is the reported-not-
    #                     fixed defect in theme.py; this run is written around
    #                     it, as session 19's was.
    d.derivation(
        None, "segment 2", "build  ·  setting the left-hand side to zero",
        "From a trajectory to a constraint",
        [
            ("dx/dt = S·v",
             "session 3 — and we integrated it",
             None),
            ("dx/dt = 0",
             "steady state: S·v = 0",
             "no rate constant appears in it"),
            ("v in null(S)",
             "intersected with the bounds on each flux",
             None),
            ("dim = r − rank(S)",
             "nine reactions, rank six, so three are left over",
             "more reactions than balances is normal"),
            ("nothing picks v",
             "the stoichiometry has run out of things to say",
             "so look at what it left"),
        ],
        board="S v = 0,  dim(null) = r - rank(S),  r = reactions",
        note="Five lines, and the last one is where the run lands: the "
             "stoichiometry has said everything it can say and it still has "
             "not picked a flux.\n "
             "Step two is the one I linger on. S v = 0 contains no rate "
             "constant — that is "
             "why it is exact, and it is also why it is not enough. Exactness "
             "and informativeness are trading against each other here.\n "
             "Session 3 put BOTH null spaces on the board and gave this one "
             "its own symbol: dim = r - rank S for the right null space, with "
             "r the reactions, beside dim = n - rank S for the left, with n "
             "the metabolites. So I use r here, which is theirs, and I say so "
             "— this is a formula they already own rather than a new one. "
             "Session 3's own note called FBA the right null space plus "
             "bounds plus an objective, which is exactly where this hour is "
             "going.\n "
             "Three degrees of freedom in a nine-reaction toy. A real "
             "reconstruction has hundreds, which is why nobody does this "
             "without an objective.")



def _cone(d):
    s = d.light()
    d.header(s, "segment 2", "build  ·  what the balance leaves open")
    d.title(s, "Mass balance does not pick a flux")
    d.image(s, FIG + "s20_cone.png", M, 1.62, w=W - 2 * M, h=5.02)
    d.foot(s, "Two axes of a three-dimensional set living in nine. Every point inside balances every metabolite exactly — and growth runs from zero to four across it.")
    d.notes(s,
           "Five steps of algebra just ended on 'nothing picks v'. That is "
           "a sentence, and this is the picture of it.\n "
           "I take the branch as the two axes because it is the branch they "
           "have already argued about. Every point in the triangle is a legal "
           "flux state: all six metabolites balance, nothing is created, "
           "nothing destroyed. I can slide along any line in there, trading "
           "acetate against the TCA, and mass conservation never complains.\n "
           "The color is what has to land. Growth is zero along the whole "
           "hypotenuse and four at a single point on the left edge, and the "
           "balance equations are indifferent between them. So S is a "
           "constraint, not a choice.\n "
           "Without the slanted edge the region is the whole quadrant — "
           "scale any solution up and it is still a solution. That is why "
           "this is called a cone, and why a model with no input limit "
           "answers 'infinity' to every question.\n "
           "Where the slanted edge comes from is the next slide, and they "
           "do it.")

    s = d.light()
    d.header(s, "segment 2", "release  ·  the third edge, on paper")
    d.title(s, "Two of those edges are physics. One is not")
    d.rows(s, [
        ("the bottom and the left", "v ≥ 0. A flux cannot run backward "
                                    "through a reaction the cell runs one "
                                    "way, so neither branch can go "
                                    "negative."),
        ("the slanted one", "is the only line in the picture that did not "
                            "come out of the chemistry. It is the medium: "
                            "glucose arrives at ten and no faster."),
        ("your turn", "one glucose makes two pyruvate. Write the inequality "
                      "that slanted edge is."),
    ], top=2.00)
    d.foot(s, "Ten in. Everything the branch does has to come out of that.")
    d.notes(s,
           "The answer is v_ackA + v_tca ≤ 20, and the intercepts on the "
           "picture are twenty on both axes, so they can check it against "
           "the drawing without me.\n "
           "What I listen for is the word AT MOST. Ten glucose makes at most "
           "twenty pyruvate, because some of the carbon leaves down the "
           "pentose branch — a student who writes equality has forgotten "
           "zwf, and that is the useful mistake here.\n "
           "This is the first time the uptake bound does any work. Every "
           "other line on the picture came from the atoms; this one came "
           "from the flask, and the next segment is about where the rest of "
           "the biology enters the same way.")

    s = d.dark()
    d.header(s, "segment 2", "debrief  ·  exact, and not enough")
    d.title(s, "A constraint is not a choice")
    d.rows(s, [
        ("what S gave us", "a SET. Every flux state in it satisfies every "
                           "balance exactly, and there is still no rate "
                           "constant anywhere in it.", CYAN),
        ("what S did not give us", "any reason to prefer one point in that "
                                   "set over another. The stoichiometry has "
                                   "said everything it can say."),
        ("so the next move is a choice", "we import a preference from outside "
                                         "the chemistry and call it an "
                                         "objective. It is a hypothesis about "
                                         "what selection did — and the second "
                                         "half of this hour is somebody "
                                         "testing it.", CYAN),
    ], label_color=CYAN, top=2.05)
    d.foot(s, "Three degrees of freedom in a nine-reaction toy. A real reconstruction has hundreds, which is why nobody does this without an objective.")
    d.notes(s,
           "LEDGER: S v = 0 gives a set, not an answer.\n "
           "I want the word hypothesis said here rather than in segment 3, "
           "because everything after this rests on it and the Fong paper is "
           "the experiment that checks it.\n "
           "Three degrees of freedom is small enough to picture and that is "
           "the only reason the toy has nine reactions. iJR904 has 1327, so "
           "the leftover dimension is in the hundreds and no amount of staring "
           "at it helps.")


def _program(d):
    # FRAME REWRITTEN 31 October. Adam: "the CONCEPT introduced is that we want
    # to make this a unique solution -- what can we add in." The old slide
    # jumped to max c.v subject to S v = 0 and lo <= v <= hi without ever
    # saying where lo and hi come from. They are where every piece of biology
    # that is not stoichiometry enters, and the session collects on that twice
    # more -- at Fong, whose model was handed its own measured uptake rates,
    # and at the close.
    s = d.light()
    d.header(s, "segment 3", "frame  ·  what we add, to get one answer")
    d.title(s, "The bounds are where the biology lives")
    d.rows(s, [
        ("fluxes have directions", "most of these reactions run one way. "
                                   "v ≥ 0 is not bookkeeping — it is "
                                   "thermodynamics, and it is what makes the "
                                   "feasible set a cone rather than a "
                                   "subspace."),
        ("the cell has to build itself", "biomass is not a reaction anyone "
                                         "discovered. It is a measured "
                                         "composition — how much protein, RNA, "
                                         "lipid, DNA per gram dry weight — "
                                         "written as if it were one reaction."),
        ("enzymes have capacities", "v_{max} and K_{m} do not disappear. They come "
                                    "back as an upper bound on a flux, and an "
                                    "enzyme that is absent is a bound of zero. "
                                    "Expression data can set them.", AMBER),
        ("the medium is a constraint", "what the cell can take up, and how "
                                       "fast. Change the carbon source and you "
                                       "change the bounds, not the matrix."),
    ], top=1.82)
    d.foot(s, "Linear in v throughout, so this is a convex program with a global optimum — scipy.optimize.linprog, four lines. The objective is still a hypothesis.")
    d.notes(s,
           "This is the spine of the second half.\n "
           "S is exact and says nothing. The objective is a guess. Everything "
           "in between — every piece of physiology, every measurement, the "
           "medium, the enzyme that is or is not expressed — enters as a "
           "BOUND. That is the sentence I want them to leave with, and it is "
           "the one that makes Fong's third row land in twenty minutes: their "
           "model was handed the measured uptake rates as bounds and asked for "
           "one number out.\n "
           "I am precise about irreversibility here. v ≥ 0 is a "
           "thermodynamic statement, not a convention, and it is what turns "
           "the null space into a cone — which is the picture they just "
           "saw.\n "
           "The biomass reaction is the one that surprises people. It is a "
           "measured composition, from the growth-law work last Thursday: "
           "grams of protein, RNA, lipid and DNA per gram dry weight, divided "
           "out and written as a single reaction. Nobody found it in a "
           "pathway.\n "
           "And v_max and K_m: I say explicitly that they have not vanished. "
           "They are upstream of an upper bound. An enzyme that is not "
           "expressed is a bound of zero, which is the same move as a knockout "
           "and is why the next segment is one line of code.\n "
           "Convexity gets one sentence. Everything in sight is linear in v, "
           "so there is a global optimum and the solver finds it. They will "
           "assume optimization is hard; this one is not.\n "
           "If someone asks which medium: glucose minimal, uptake capped at "
           "ten. That cap is the only number in the whole problem that did not "
           "come out of the chemistry, and it is the edge they saw on the "
           "triangle.")

    d.derivation_fig(
        "segment 3", "build  ·  the toy, solved by hand",
        "Six lines, and the answer is an integer",
        [("Let b be the flux to biomass",
          "v_{zwf}  =  b",
          "P5P has one maker and one user, so the two are equal"),
         ("G6P comes in at ten and leaves two ways",
          "v_{pgi}  =  10 − b",
          None),
         ("F6P. The same question as P5P",
          "v_{tpi}  =  v_{pgi}  =  10 − b",
          None),
         ("T3P: two arrive, two leave, rest runs on",
          "2(10 − b)  =  2b  +  v_lower",
          "so v_lower = 20 − 4b"),
         ("ATP: what a T3P earns, what growth spends",
          "4(20 − 4b)  ≥  4b",
          "so b ≤ 4")],
        [FIG + "s20_sixlines_1.png", FIG + "s20_sixlines_2.png",
         FIG + "s20_sixlines_3.png", FIG + "s20_sixlines_4.png",
         FIG + "s20_sixlines_5.png"],
        closing="b = 4 units of biomass per ten glucose in. "
                "Sixteen ATP made, sixteen spent.",
        note=("b is v_biomass, the flux through the biomass reaction, and it "
              "is the thing we are solving for. It goes up first and gets "
              "boxed, because every line is in terms of it. Units are "
              "arbitrary and the whole problem is scaled to ten glucose in, "
              "so b = 4 means four units of biomass per ten glucose.\n"
              "Each line is one row of S set to zero, and the picture beside "
              "it is that row: the metabolite, what makes it, what uses it. "
              "That is the whole method, and after five of them the room has "
              "done by hand what linprog does.\n"
              "I ask before each line rather than writing it. P5P: who makes "
              "it, who uses it? One of each, so the two fluxes are equal. G6P: "
              "ten in, two ways out. F6P: same question as P5P. T3P is the "
              "one that trips people and it is the only line with a 2 on both "
              "sides — two trioses arrive per F6P, two leave per unit of "
              "biomass.\n"
              "The ATP line is where the inequality appears. It is an "
              "inequality because ATP can be wasted through atpm, so the "
              "balance only has to be satisfiable, not tight. It comes out "
              "tight anyway, which is the check.\n"
              "The check out loud: ATP made is 4 + 3(4) = 16, ATP used is "
              "4b = 16. Nothing spare and nothing short. If that does not "
              "close, line four is where it went wrong.\n"
              "The question goes up on the next slide rather than hanging "
              "in the air, because it is the hinge into the objective."))

    s = d.light()
    d.header(s, "segment 3", "release  ·  one coefficient, looked at twice")
    d.title(s, "Where did the four come from?")
    d.rows(s, [
        ("line five said", "each T3P that runs on earns four ATP — the "
                           "4 in 4(20 − 4b) ≥ 4b."),
        ("your turn", "four is a sum of two reactions. Name them, and "
                      "what each one pays. Then: that sum is four only "
                      "if something is true about the pyruvate. What?"),
    ], top=1.68)
    d.image(s, FIG + "s20_pathway_4.png", M, 3.72, w=W - 2 * M, h=2.92)
    d.foot(s, "Four lines were balances. This one has a choice buried in it.")
    d.notes(s,
           "One ATP at lower, three round the TCA. Both numbers are on the "
           "pathway drawing, so the first question is a reading exercise "
           "and everybody can get it.\n "
           "The second one is the point. One plus three is four only if "
           "EVERY pyruvate goes round the TCA and none of it to acetate. "
           "Nothing in S v = 0 says that. I wrote it into the coefficient "
           "four slides ago and nobody stopped me, including me.\n "
           "So where did it come from? A preference I have not named yet: "
           "take the arm that pays better. That is the objective, and it is "
           "the move the next segment is built on. I take the answer from "
           "the room rather than saying it.\n "
           "Somebody raises 'always?' and I do NOT resolve it here. Segment "
           "5 is the answer to that question and resolving it now costs me "
           "the best slide in the hour. I say I am coming back to it.")

    s = d.light()
    d.header(s, "segment 3", "debrief  ·  the same six lines, and the solver")
    d.title(s, "Your six lines, and the solver's nine numbers")
    d.image(s, FIG + "s20_flux_map.png", M + 0.35, 1.72, w=11.2, h=4.55)
    d.foot(s, "A linear objective is always maximized at a corner of the feasible set. A corner is where fluxes sit at exactly zero.")
    d.notes(s,
           "Their six lines against the solver's, and they agree to the "
           "digit. That is the point of having done it by hand: linprog is "
           "not doing anything they cannot do, it is doing it nine hundred "
           "times.\n "
           "Now I name the theorem, because segment 5 takes it apart and "
           "cannot do that until it has been said. A linear objective over a "
           "set with flat faces is always maximized at a CORNER of that set "
           "— a point where enough constraints are tight to pin every flux. "
           "That is why ackA comes back as exactly zero rather than nearly "
           "zero, and why the answer is an integer at all.\n "
           "What I do NOT say here is that the corner is the only optimum. "
           "It is not, and that is segment 5.\n "
           "And it is the moment to collect on overflow. The model sent every "
           "pyruvate round the TCA because ATP is the only currency it has. A "
           "real cell does not, and we said why an hour ago — the constraint "
           "that would fix it is a bound this model does not carry.")


def _knockouts(d):
    s = d.light()
    d.header(s, "segment 4", "frame  ·  what you would do with this")
    d.title(s, "You want the carbon in your product")
    d.rows(s, [
        ("the job", "metabolic engineering is one sentence: get the "
                    "carbon into the thing you are making, instead of "
                    "into waste or into more cells. The lever is almost "
                    "always deleting the competition.", CYAN),
        ("the obvious move here", "acetate is waste carbon — two of every "
                                  "three leave the cell unburned. Deleting "
                                  "ackA is the first thing anyone tries."),
        ("the catch", "you cannot delete everything. Some deletions kill "
                      "the cell, some cost it growth, some cost nothing "
                      "at all — and you need to know which BEFORE you "
                      "spend a month building the strain.", AMBER),
        ("why you can ask now", "bounds[reaction] = (0, 0). No new "
                                "equations, no new parameters. One line "
                                "per strain, and nothing stops you doing "
                                "it for every reaction in a genome-scale "
                                "model."),
    ], top=1.88)
    d.foot(s, "Seven real reactions in this network. Which ones could you get away with deleting?")
    d.notes(s,
           "This is the slide that says why a synthetic biologist is in "
           "the room. Everything up to here has been a modelling method; "
           "this is the thing the method is for.\n "
           "Acetate is not a hypothetical. Overflow is the single biggest "
           "carbon leak in an industrial E. coli fermentation, and "
           "deleting the acetate branch is a standard first move — which "
           "we drew an hour ago and can now ask about.\n "
           "If somebody asks what product: this toy has none. Biomass is "
           "the only sink, so the question it can answer is the "
           "prerequisite one — which deletions leave a cell that still "
           "grows. Add a product reaction and the same machinery gives "
           "you yield, which is what a real design run does. I want them "
           "to see that the shape is identical.\n "
           "The catch row is the one that earns the segment. A deletion "
           "you cannot survive is not a design, and finding that out at "
           "the bench costs a month. Stoichiometry answers it in a line, "
           "with no kinetics, for every reaction at once.\n "
           "Then I hand the question over rather than answering it. They "
           "did the six-line derivation twenty minutes ago and they have "
           "everything they need.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  what biomass is actually made of")
    d.title(s, "Trace it back from the thing you want")
    d.image(s, FIG + "s20_cuts_none.png", M, 1.70, w=W - 2 * M, h=4.95)
    d.foot(s, "Three inputs: two trioses, one P5P, four ATP. Every one of them has to arrive from the glucose, and this is the first time biomass is on the picture.")
    d.notes(s,
           "Biomass has been the objective for twenty minutes and this is the "
           "first slide that draws it, which is deliberate — putting it on "
           "the pathway earlier would have given away the six lines.\n "
           "I trace each input back out loud. P5P comes only from zwf. The "
           "trioses come only through tpi, which comes only through pgi. The "
           "ATP comes from lower and the TCA. Four arrows carry everything "
           "biomass needs, and that is the whole of what is about to make "
           "four deletions lethal.\n "
           "The branch out to acetate and the TCA is on here too, and it is "
           "the one place where there is a genuine choice rather than a "
           "single route.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  one deletion, worked")
    d.title(s, "Cut zwf and watch what goes with it")
    d.image(s, FIG + "s20_cuts_zwf.png", M, 1.70, w=W - 2 * M, h=4.95)
    d.foot(s, "bounds[\"v_{zwf}\"] = (0, 0). No new equations, no new parameters — and biomass is exactly zero, not small.")
    d.notes(s,
           "One line of code, and the consequence is structural rather than "
           "numerical. zwf is the only producer of P5P. Biomass needs P5P. So "
           "the answer is zero and it is exact — no simulation, no noise, no "
           "tolerance.\n "
           "I sit on the exactly. Most modeling gives you a small "
           "number and asks whether it is small enough. This gives you a "
           "structural impossibility: there is no route, so there is no flux, "
           "whatever the parameters are.\n "
           "This is also the shape of Fong's tpi strains, and in twenty "
           "minutes we find out that the model was WRONG about them on one "
           "substrate. I plant that now and do not explain it.")

    s = d.light()
    d.header(s, "segment 4", "release  ·  by inspection, on paper")
    d.title(s, "Which deletions kill it?")
    d.rows(s, [
        ("the question", "of the seven real reactions, which deletions drive "
                         "biomass to exactly zero? Name them, and say what "
                         "they have in common."),
        ("you have everything you need", "the picture you just watched, and "
                                         "the six lines from the board. Ask "
                                         "what biomass needs, and whether the "
                                         "network has a second way to make "
                                         "it."),
    ])
    d.foot(s, "Two minutes. Zero or not zero, and the reason. Not the numbers in between.")
    d.notes(s,
           "The answer is pgi, zwf, tpi and lower — four of the seven — and "
           "the common property is that each is the ONLY route to something "
           "biomass needs.\n "
           "zwf is the only producer of P5P. tpi is the only producer of T3P. "
           "pgi is the only way to F6P, so it takes T3P down with it. lower is "
           "the only producer of pyruvate, so it takes all the ATP down with "
           "it — that last one is the one they have to chase two steps and it "
           "is the one worth waiting for.\n "
           "ackA and atpm are free: they carry zero flux at the optimum "
           "already, so losing them costs nothing. The TCA is the interesting "
           "one and it is neither, so it keeps until the debrief.\n "
           "I take answers before the figure. The figure is then a check on "
           "them rather than a reveal.")

    s = d.light()
    d.header(s, "segment 4", "debrief  ·  and the solver agrees")
    d.title(s, "Four of these are lethal, and exactly so")
    d.image(s, FIG + "s20_knockouts.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "Zero is not a small number here. It is the network saying there is no other way round.")
    d.notes(s,
           "I check their four against the figure, name by name.\n "
           "The four zeros are STRUCTURAL: there is no second route to T3P, to "
           "P5P or to ATP in this network. That comes back at Fong and Palsson, "
           "whose tpi strains are exactly this shape — and there the model was "
           "WRONG about them.\n "
           "ackA and atpm cost nothing because they carry nothing at the "
           "optimum. Losing a reaction you were not using is free.")

    s = d.dark()
    d.header(s, "segment 4", "debrief  ·  three kinds of answer")
    d.title(s, "Zero, free, and the one in between")
    d.rows(s, [
        ("four are lethal", "pgi, zwf, tpi, lower. Each is the only route to "
                            "something biomass needs, so the answer is zero "
                            "and it is exact — no simulation, no noise.", CYAN),
        ("two are free", "ackA and atpm carry no flux at the optimum already. "
                         "Losing a reaction you were not using costs "
                         "nothing."),
        ("one costs something", "delete the TCA and biomass falls from 4 to "
                                "10/3 — acetate now carries all the pyruvate. "
                                "A different corner, not a scaled-down one.",
         AMBER),
        ("and remember this shape", "the lethal four are exactly the shape of "
                                    "Fong's tpi strains. The model called "
                                    "those dead too — and on two substrates "
                                    "it was right, and on one it was wrong."),
    ], label_color=CYAN)
    d.foot(s, "Structural, free, or costly. Stoichiometry alone sorts all seven, before any experiment.")
    d.notes(s,
           "LEDGER: lethal = no second route. Free = unused at the optimum. "
           "Costly = a different corner.\n "
           "The last row is the forward hook and I want it said in these "
           "words, because segment 7 collects on it. A structurally dead "
           "prediction is the most confident thing this method produces, and "
           "it is also where it got caught.")

def _alternates(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  what the network has already decided")
    d.title(s, "Coupling, by inspection")
    d.rows(s, [
        ("two pairs, not a list", "pgi and tpi run at exactly the same rate. "
                                  "So do zwf and biomass. At every optimum, "
                                  "under every objective we could have "
                                  "chosen."),
        ("why", "F6P has one producer and one consumer, and so does P5P. "
                "Nothing else makes them and nothing else uses them, so the "
                "balance on that one row fixes the ratio."),
        ("the consequence", "no regulation can change it. A cell that wanted "
                            "these two fluxes to differ would have to change "
                            "the network, not the expression levels."),
    ], top=2.00)
    d.foot(s, "This is flux coupling, and you can read it off the matrix without solving anything.")
    d.notes(s,
           "I take this from the room off the S figure rather than handing it "
           "over. The F6P row has exactly two non-zero entries, +1 and −1, and "
           "the P5P row is the same shape.\n "
           "Two pairs is the whole list for this network, and that matters: "
           "coupling is RARE and structural, not a thing you find everywhere "
           "you look.\n "
           "The zwf-biomass pair is the one I carry forward. The very next "
           "slide adds a "
           "second route to P5P and that coupling disappears, while pgi-tpi "
           "survives untouched. One added reaction, and it shows what the "
           "coupling was resting on.\n "
           "The consequence is the engineering content: there are quantities "
           "in a cell that regulation cannot touch, and stoichiometry tells "
           "you which ones before you do any experiment.")


    s = d.light()
    d.header(s, "segment 5", "build  ·  a second route, added")
    d.title(s, "A second route to the same place")
    d.rows(s, [
        ("the change", "add one reaction with the same stoichiometry as zwf — "
                       "call it zwf2. Nothing else moves. The network can now "
                       "reach P5P two ways."),
        ("what you would expect", "nothing. It is the same chemistry, so the "
                                  "best the cell can do should be exactly "
                                  "what it was."),
        ("and that is right", "biomass is still 4. The objective does not "
                              "move by so much as a rounding error."),
    ], top=2.00)
    d.foot(s, "The answer did not change. What changed is whether there is one answer.")
    d.notes(s,
           "I set this up as a non-event on purpose, because the surprise is "
           "not in the objective value — it is in everything underneath it.\n "
           "The second route is a MODELING DEVICE and I say so out loud: "
           "E. coli has one glucose-6-phosphate dehydrogenase. Duplicated "
           "routes are everywhere in real reconstructions — transhydrogenases, "
           "parallel electron-transport branches — but this particular one is "
           "mine, built to make the point visible in a network they can hold "
           "in their heads.")

    s = d.light()
    d.header(s, "segment 5", "release  ·  a second optimum, on paper")
    d.title(s, "Find a second answer")
    d.rows(s, [
        ("what the solver returned", "v_{zwf} = 4, v_{zwf2} = 0, biomass = 4. "
                                     "One flux vector, printed with no "
                                     "warning attached."),
        ("your turn", "write down a DIFFERENT set of fluxes that also gives "
                      "biomass exactly 4. Then say how many such sets there "
                      "are."),
    ])
    d.foot(s, "Ninety seconds. You need no solver and no algebra — only the fact that the two routes are identical.")
    d.notes(s,
           "Almost everyone finds the mirror answer fast: v_zwf = 0, "
           "v_zwf2 = 4. I take that and then push on the second question, "
           "which is the one that matters.\n "
           "What I want is 2, 2. And then 1, 3. And then the recognition that "
           "ANY split summing to four works, so there are infinitely many — "
           "a continuum, not a list.\n "
           "If the room is quick, ask what the solver would have to print to "
           "be honest. The answer is an interval, and that is flux "
           "variability analysis, which is the next slide.")

    s = d.dark()
    d.header(s, "segment 5", "debrief  ·  what you just found")
    d.title(s, "The answer stops being an answer")
    d.rows(s, [
        ("the optimal set is an edge", "(4,0) and (0,4) both give biomass 4. "
                                       "So does (2,2), and so does every "
                                       "point between them. None of the "
                                       "interior ones is a corner.", CYAN),
        ("so the theorem was exact", "a corner IS optimal — that much is "
                                     "guaranteed. It is just not the only "
                                     "thing that is."),
        ("and the solver said nothing", "it returned one vertex of a "
                                        "continuum and reported success. "
                                        "Nothing in the output marks the "
                                        "difference."),
        ("how you find out", "flux variability analysis: re-solve for the "
                             "min and max of each flux at the optimum. Here "
                             "both routes come back [0, 4].", CYAN),
    ], label_color=CYAN)
    d.foot(s, "Mahadevan & Schilling, Metab Eng 5:264 (2003). A flux map is never THE answer until you have checked that it is the only one.")
    d.notes(s,
           "This is where I take back the obvious generalization of segment "
           "three, out loud rather than hoping nobody drew it. The natural "
           "reading of 'the better return wins outright' is that a linear "
           "program never gives you a graded split. It does, whenever there "
           "is a tie, and here is the tie.\n "
           "LEDGER: optimum at a vertex, yes. Unique, no. FVA is how you tell.\n "
           "And collect the debt from segment 4. We had TWO coupled pairs: "
           "pgi-tpi and zwf-biomass. Adding this second route gives P5P a "
           "second producer, so zwf-biomass is gone — one coupled pair "
           "now, not two. pgi-tpi is untouched, because nothing I "
           "added touches F6P. The coupling was never about the enzymes; it "
           "was about a row of S with exactly two entries in it, and I just "
           "put a third in one of those rows.\n "
           "Generic, not a quirk of the toy. Real reconstructions are full of "
           "parallel routes, and this is why a published flux map with no "
           "variability analysis beside it is an assertion rather than a "
           "result.")

    s = d.light()
    d.header(s, "segment 5", "debrief  ·  the ranges, drawn")
    d.title(s, "Two fluxes, completely undetermined")
    d.image(s, FIG + "s20_alternate_optima.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "The exact tie is ours; the limitation is general. The solver returns one point and tells you nothing about the rest.")
    d.notes(s,
           "The objective does not move — still four. But two fluxes are now "
           "undetermined across their whole range, and the solver picked one "
           "without saying so.\n "
           "The two full-width bars are where I point. That width is the "
           "thing the "
           "single flux map was hiding.")


# ------------------------------------------------------------------- Fong ---
def _fong(d):
    s = d.light()
    d.header(s, "segment 6", "frame  ·  somebody tested the hypothesis")
    d.title(s, "Six deletions, fifty strains, and a prediction each")
    d.rows(s, [
        ("the hypothesis", "that a cell's fluxes sit where growth is "
                           "fastest. If that is true, the rate FBA "
                           "predicts is the rate you measure.", CYAN),
        ("the test", "break the network, predict the new growth rate, "
                     "then go and measure it. A deletion strain is a "
                     "case nobody tuned the model to fit.", CYAN),
        ("the strains", "six genes — ackA, frd, pck, ppc, tpi, zwf — "
                        "each evolved on four carbon sources in "
                        "replicate. 24 cases, fifty strains."),
        ("the model", "iJR904: 904 genes, 1,327 reactions. A knockout "
                      "deletes that gene's reactions from the list."),
        ("the inputs", "the measured substrate and oxygen uptake rates "
                       "were fed in as constraints."),
        ("the result", "the growth rate was predicted to within 10% for "
                       "39 of 50."),
    ], top=1.95)
    d.notes(s,
           "The first two rows are what make this a test rather than a "
           "demonstration. We imported the objective in segment 3 because the "
           "stoichiometry had run out of things to say, and it was a "
           "hypothesis about selection. This is somebody checking it "
           "against fifty strains.\n "
           "The inputs row is the one nobody reads and it changes what "
           "the number means. The model was handed its own boundary conditions — "
           "the uptake rates are measurements, not predictions — and asked for "
           "ONE number out.\n "
           "That is still a real result. It is not 'the genome predicts "
           "growth', and I want them to be able to say the difference.\n "
           "904 genes and 1327 reactions is iJR904, Reed 2003, which is the "
           "reconstruction their own reference 1 points at.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  the result you were sent to read")
    d.title(s, "Predicted against measured, before and after")
    d.paper_figure(s, "fong2004_fig1a", M + 2.35, 1.70, 5.05, 4.55,
                   "Fong & Palsson 2004, Fig. 1a",
                   "blue: before evolution.  pink: after.  the line is y = x",
                   show_caption=True)
    d.notes(s,
           "This is the figure the reading assignment points at and the deck "
           "has never shown it. Everything the session claims about Fong is "
           "on this one panel.\n "
           "Axes first: predicted across, measured up, and the diagonal is "
           "perfect agreement. Then the two colors, which are the whole "
           "argument. Blue is the strain before evolution. Forty-two "
           "of the fifty sit BELOW the line — the model is wrong about "
           "it, and wrong in a consistent direction. Pink is the same "
           "strain after weeks of passaging, and it sits ON the line.\n "
           "So the model does not predict what a knockout does. It predicts "
           "where a knockout ENDS UP, and the blue cloud is the evidence that "
           "those are different claims.\n "
           "The labeled points are the eleven, and I do not take them "
           "yet. Seven labels, not eleven, because ppc and tpi are in "
           "duplicate — ppc Glu, ppc AKG, tpi Glu, tpi Lac is eight "
           "points, and zwf Glu, zwf Gly, pck Akg are one each. That is "
           "the 8 + 3, visible on the panel before anybody reads it. "
           "They are the next segment and they have been asked to come with a "
           "guess about them.\n "
           "Two points to notice if someone asks: the pair at predicted "
           "zero and measured 0.76 to 0.80 is tpi on lactate, which is "
           "the one real structural miss, and the four at the origin are "
           "predictions of no growth that came true.\n "
           "What BEFORE means, if it comes up: each culture's first "
           "measurable growth rate, not day zero. Four strains showed no "
           "growth for several days — tpi on glucose and on lactate, ppc "
           "on glucose, zwf on malate — and their blue point is the day "
           "they first grew. That is why the two tpi lactate markers "
           "differ: one replicate started on day eleven, the other on "
           "day one. It also means BEFORE is a daily estimate off the "
           "dilution rate and OD at passage, while AFTER is a proper "
           "batch measurement.\n "
           "If somebody counts: fifty blue markers, forty-two below the "
           "line, four at the origin, four above. Two of the four above "
           "are the tpi lactate pair at zero predicted; the other two are "
           "one strain pair near predicted 0.45. Set the zero-prediction "
           "six aside and it is forty-two of forty-four. The small dark "
           "marker low on the right is the LEGEND, not a data point, and "
           "it is the one thing on this panel that has caught me out.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  the evidence for the word")
    d.title(s, "Growth rate, day by day")
    d.paper_figure(s, "fong2004_sfig1", M + 2.02, 1.75, 5.18, 4.0,
                   "Fong & Palsson 2004, Supplementary Fig. 1",
                   "twenty-four cases, fifty lineages, fifty days",
                   show_caption=True)
    d.notes(s,
           "Twenty-four panels: six COLUMNS, one per gene, four substrates "
           "down each, and fifty lineages between them — most cases in "
           "duplicate, two in triplicate. The "
           "x axis is DAYS of evolution, 0 to 50 — the word 'generation' does "
           "not appear anywhere in this paper, so I do not put it in their "
           "mouths.\n "
           "Without this figure 'evolves toward the prediction' is our "
           "sentence; with it, it is theirs.\n "
           "I follow one trajectory: it starts well below, rises over weeks, "
           "flattens. That shape is the whole argument for why an optimality "
           "assumption is allowed to work at all.\n "
           "Then the part the figure is really for. These lineages do NOT "
           "move in lockstep — the paper says the rate of adaptation 'varied "
           "greatly between deletion strains', and the curves begin on the "
           "first day of MEASURABLE growth, which is not day zero for all of "
           "them. Parallel lineages of the same strain diverge: ppc1 evolved "
           "on a-ketoglutarate would not grow on glucose, glycerol, lactate "
           "or pyruvate; ppc2 did grow on all four, though more slowly — "
           "their parenthesis, and it makes it a graded result rather than a "
           "binary one. That is Fig. 2, not the trajectories on this slide.\n "
           "That divergence is the setup for the next segment, because three "
           "of the eleven failed predictions are single lineages whose "
           "parallel twin was fine.")


    s = d.light()
    d.header(s, "segment 6", "release  ·  read the two colors")
    d.title(s, "What does the blue cloud tell you?")
    d.rows(s, [
        ("the question", "the blue points are the same strains as the pink "
                         "ones, measured before evolution. Almost all of them "
                         "sit below the line. Say what that means for what "
                         "the model is claiming."),
        ("and then", "if you only had the pink points, what could you NOT "
                     "say?"),
    ], top=2.10)
    d.foot(s, "Ninety seconds, on the figure. You need nothing but the two colors and the diagonal.")
    d.notes(s,
           "A reading exercise rather than a calculation, and it is the "
           "skill I most want them to leave with: a figure is an argument, "
           "and the argument here is carried by a color.\n "
           "The answer to the first: the model is NOT predicting the "
           "phenotype of the strain you build. A fresh knockout grows slower "
           "than predicted, consistently — so if you took the prediction as "
           "a statement about your strain on day one, you would call the "
           "model wrong, and you would be right.\n "
           "The answer to the second is the one worth waiting for. With only "
           "the pink points you could not tell whether the model was "
           "predicting anything at all, or whether these strains had simply "
           "always grown at that rate. The blue cloud is what turns agreement "
           "into a result — it shows there was somewhere else to be.\n "
           "If it goes fast: ask what the equivalent control is for any "
           "model they build. Something had to move, and you have to show "
           "where it moved from.")

    s = d.light()
    d.header(s, "segment 6", "debrief  ·  the word that is doing the work")
    d.title(s, "Evolved")
    d.rows(s, [
        ("what they did", "built the deletion strain, then passaged it "
                          "daily for 25 to 50 days, until growth stopped "
                          "changing."),
        ("why it matters", "an unevolved knockout is NOT where the model "
                           "says it should be. Flux balance predicts "
                           "a destination, not a starting point — Ibarra, "
                           "Edwards & Palsson, Nature 420:186 (2002), on "
                           "wild type."),
        ("how much moved", "every evolved strain gained at least 15%, and "
                           "across the 46 that grew the average was 87%. "
                           "The four that never grew are tpi on malate "
                           "and succinate — predictions the model got "
                           "RIGHT.", AMBER),
        ("what they do not say", "the blue points sit at lower PREDICTED "
         "growth too. Those runs had a lower uptake bound, and the "
         "methods describe only one.", AMBER),
    ], top=1.95)
    d.foot(s, "An optimality assumption is a claim about selection. This is the experiment that tests it.")
    d.notes(s,
           "This is the heart of the session and it is one word in their "
           "abstract.\n "
           "Ibarra 2002 made the point first and is Fong's own reference "
           "four. I mention it and move on.\n "
           "The last row is an observation, not an accusation, and I say "
           "it that way. Blue runs 0.43 to 0.65 on the predicted axis and "
           "pink runs 0.59 to 0.88. An FBA prediction only moves if a "
           "bound moves, so there are two input sets here and the paper "
           "documents one.\n "
           "What makes it solid rather than a guess: within glucose the "
           "three network variants hold the same ratios at both stages — "
           "1, 0.95, 0.87 before and 1, 0.95, 0.87 after. Same model, "
           "same gene effects, different uptake. And the pink triplet "
           "reproduces their own sentences, 27.5% and 31.8% against the "
           "paper's ~28% and ~33%.\n "
           "Where the lower set came from is not in the paper. The two "
           "candidates are day-zero rates on the unevolved strains, which "
           "this lab measured as routine in 2003 and 2005, or reused "
           "wild-type rates per carbon source. If it is the second, the "
           "blue cloud is a weaker claim than it looks, and I say so if "
           "somebody pushes.\n "
           "This is not in a citation. It is arithmetic off their figure "
           "and I present it as that, which is also the lesson: the "
           "bounds are where the biology enters, and here they moved "
           "inside the paper that is testing the method.")

def _failures(d):
    # REWRITTEN 26 October after an adversarial read of the paper. The first
    # version said the eleven failures were "two different failures wearing one
    # number" -- tpi structural, ppc quantitative. Three things were wrong and
    # all three are quotable against it:
    #   * "all strains except tpi- on malate and succinate" (p. 1057) -- the tpi
    #     strains did NOT grow on those two, so the no-growth prediction was
    #     RIGHT there. Only on lactate did they grow when none was predicted.
    #   * eleven is 8 + 3: "The other three incorrectly predicted cases (pck- on
    #     a-ketoglutarate, zwf- on glucose and glycerol) represented only one of
    #     the replicate parallel evolution strains and may be a result of
    #     experimental and evolutionary variability."
    #   * the paper's ONLY diagnosis covers both genes and is not about the
    #     objective: "Predicted growth rates were accurate in half the cases for
    #     both the ppc- and tpi- strains, suggesting that the reconstructed
    #     network may be incomplete."
    # The true story is better than the invented one, which is the usual result.
    s = d.light()
    d.header(s, "segment 7", "release  ·  the eleven")
    d.title(s, "How many kinds of wrong is this?")
    d.rows(s, [
        ("you were asked", "to come with a guess about the eleven misses. "
                           "Hands, and I want the wrong ones too."),
        ("what I am after", "not a cause. A COUNT — one kind of wrong, or "
                            "several — and what in Figure 1 you would use to "
                            "defend it."),
        ("what Figure 1 gives you", "which gene, which substrate, how far "
                                    "off, and which direction. Four things, "
                                    "and the eleven carry labels."),
    ], top=2.05)
    d.foot(s, "Eleven wrong predictions out of fifty. One kind of wrong, or more than one?")
    d.notes(s,
           "Guesses first, and the wrong ones stand — 'they're all the same "
           "pathway', 'they're all poor carbon sources'. My own first guess "
           "was that tpi was a structural failure and ppc a quantitative one, "
           "and the paper says otherwise in a single sentence.\n "
           "Nothing of the answer is on this slide. The tpi panels come "
           "next and the sorting comes after them, so whatever the room says "
           "here is still theirs when the evidence arrives.\n "
           "If the room goes quiet: ask whether ppc and tpi being eight of "
           "the eleven is a pattern or an accident. That is enough to start "
           "it.")

    s = d.light()
    d.header(s, "segment 7", "build  ·  what tpi actually did")
    d.title(s, "Same gene, same model, two different answers")
    d.paper_figure(s, "fong2004_fig1b_lac_mal", M + 0.5, 1.80, 11.6, 3.85,
                   "Fong & Palsson 2004, Fig. 1b",
                   "growth rate against DAY of evolution.  no growth was predicted for tpi on either substrate",
                   show_caption=True)
    d.notes(s,
           "Here is the thing the text says, drawn. No growth was predicted "
           "for tpi on lactate, on malate and on succinate — that is their "
           "Figure 1 caption, three substrates, one prediction.\n "
           "On malate the tpi line is flat on the axis. Zero, for fifty days. "
           "The model said nothing would grow and nothing grew. Succinate is "
           "the same picture and I say so rather than showing a third panel.\n "
           "On lactate the same strain under the same prediction starts "
           "around day eleven and climbs to about 0.77. That is the one real "
           "structural miss in the whole paper, and it is the most "
           "interesting number in the hour: the model was not a bit off, it "
           "was categorically wrong, on one substrate out of three, for a "
           "gene it got right on the other two.\n "
           "A flat line at zero is easy to read as a missing curve. I point "
           "at it and say that is the result — two of the eleven that look "
           "like failures are successes.")

    s = d.light()
    d.header(s, "segment 7", "debrief  ·  the eleven, sorted")
    d.title(s, "Not eleven of a kind")
    d.rows(s, [
        ("eight of them are two genes", "ppc or tpi. The other three — pck "
         "on α-ketoglutarate, zwf on glucose and on glycerol — are single "
         "replicates, and the authors decline to diagnose them: \"may be a "
         "result of experimental and evolutionary variability.\""),
        ("the miss depends on the SUBSTRATE", "ppc runs ~28% slow on glucose "
         "and 11–12% slow on α-ketoglutarate. tpi runs ~33% slow on glucose "
         "— and on lactate it grew above 0.70 h⁻¹ when no growth at all was "
         "predicted. Same gene, different substrate, different kind of "
         "wrong."),
        ("and two that look like misses are not", "tpi on malate and on "
         "succinate: no growth predicted, and none observed. Correct calls "
         "that are easy to score as failures — the flat lines you just "
         "looked at."),
    ], top=1.95)
    d.foot(s, "Fong & Palsson 2004, p. 1057. Eleven misses, and they are not one phenomenon.")
    d.notes(s,
           "Three answers to the count, against whatever the room said "
           "twenty minutes ago.\n "
           "The row that surprises people is the last one. A no-growth "
           "prediction that comes true is a success, and it looks like a "
           "blank panel in the supplementary figure — the two tpi panels "
           "that say No Growth are the model getting it right.\n "
           "Lactate is the one real structural miss: predicted nothing, got "
           "0.70 per hour. Same gene, same model, three substrates, two "
           "right and one wrong. That is the sentence the next slide "
           "collects on.")

    s = d.light()
    d.header(s, "segment 7", "debrief  ·  what the authors conclude from it")
    d.title(s, "Accurate in half the cases, for both strains")
    d.rows(s, [
        ("their sentence", "\"Predicted growth rates were accurate in half the "
         "cases for both the ppc– and tpi– strains, suggesting that the "
         "reconstructed network may be incomplete.\""),
        ("they do not blame the objective", "and the reason is in the "
         "pattern: an objective is the same on every substrate, so a strain "
         "predicted correctly on two and wrongly on two others cannot have a "
         "wrong objective. What changes with the carbon source is which "
         "reactions carry flux."),
        ("and they offer a candidate", "for tpi on glucose they suggest the "
         "cell rerouted — \"possibly activation of the methylglyoxal "
         "bypass\". Their guess at why that strain adapted slowly, not "
         "their diagnosis of the miss.", AMBER),
        ("the design consequence", "a failure localizes the gap. Which "
         "substrate broke it tells you where in the network to go looking, and "
         "that is what makes a wrong prediction worth more than a right one."),
    ], top=1.90)
    d.foot(s, "A model that fails on some substrates and not others is pointing at a reaction, not at an assumption.")
    d.notes(s,
           "This is what the reading was assigned for.\n "
           "Row three I take slowly. An objective "
           "is a single assumption applied everywhere; if it were wrong you "
           "would expect to be wrong everywhere, not on half the substrates. "
           "Substrate-dependent error points at the stoichiometry.\n "
           "The methylglyoxal bypass is the part I like most, and the part "
           "I have to be careful with. They raise it to explain why the tpi "
           "strain on glucose adapted SLOWLY, not to explain the miss, and "
           "they never say the reconstruction lacks it. What is worth "
           "saying is the shape of it: a named route a biochemist can go "
           "and check, which is what 'the network may be incomplete' would "
           "have to become before anyone could act on it.\n "
           "And it closes the hour's loop. We imported an objective because "
           "the stoichiometry ran out of things to say. The failures say the "
           "stoichiometry was also the thing that was incomplete — so the "
           "fix is more biochemistry, not a better guess about selection.")


def _close(d):
    s = d.dark()
    d.header(s, "close", "where this goes")
    d.title(s, "Known exactly, and still not enough")
    d.rows(s, [
        ("what the hour traded", "the rate laws, for something exact. S "
                                 "counts atoms and cannot be wrong about "
                                 "them, and cannot pick a flux.", CYAN),
        ("so the model is three parts", "S, exact. An objective, which is "
                                        "a hypothesis about selection. And "
                                        "the bounds, where every piece of "
                                        "real biology entered.", AMBER),
        ("what that buys you", "every deletion in a genome scored before "
                               "you build one strain: lethal, costly or "
                               "free. Add a reaction for what you are "
                               "making and the same solve gives yield.",
         CYAN),
        ("and the failures told you which part to fix", "not the "
         "objective. The misses depend on the SUBSTRATE, so the fix is "
         "biochemistry, not a better guess."),
        ("Thursday — session 21", "a coupling nobody writes down, drawn "
                                  "as an arrow. The arrow is a lie about "
                                  "the physics."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "You came in able to model three genes. You leave able to score every reaction in a genome — with no rate constant anywhere.")
    d.notes(s,
           "The hour ends on what they can go and do, not on the "
           "epistemology. The third row is the payoff for the whole "
           "session: the deletion scan is a real design loop, it is what "
           "segment 4 was a toy version of, and it needs no kinetics.\n "
           "The week after, the question stops being how to model each "
           "context that breaks a circuit and becomes how to reject all "
           "of them at once.\n "
           "I close on the contrast with Thursday coming. Today: perfect "
           "knowledge, insufficient. Thursday: the connection is drawn WRONG — "
           "the arrow from one module to the next says 'signal' and the "
           "molecule says 'binding site'.\n "
           "Thursday is not a fourth rung of the sequestration ladder. I told "
           "them four days ago that session 20 is a different axis, and I am "
           "not going to blur it now.")

    s = d.light()
    d.header(s, "close", "before Thursday")
    d.title(s, "What to read")
    d.rows(s, [
        ("the paper", "Mishra, Rivera, Lin, Del Vecchio & Weiss, Nat "
                      "Biotechnol 32:1268 (2014) — a load driver. A different "
                      "PAPER from session 18's, by the same Deepak Mishra "
                      "with the same senior author, nine days apart on this "
                      "syllabus. Cite both with the year."),
        ("come able to say", "where the timescale separation is doing the "
                             "work. The numbers to look at are a response time "
                             "and a bandwidth, not a level."),
    ], top=2.05)
    d.assignment(s, y=4.70)
    d.notes(s,
           "I flag the two Mishras explicitly. They are easy to confuse, so the "
           "room will.\n "
           "I point them at response time and bandwidth. If they go looking for "
           "a change in expression LEVEL they will find a small one and "
           "conclude the effect is small, which is the trap the session opens "
           "on.")
