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

NOT A FOURTH RUNG OF THE SEQUESTRATION LADDER. Session 19's close surface says
so explicitly, four days before this one: "session 20 is not a fourth rung --
it is the host's economy again at the level of metabolites." Honour that.

THE NUMBER THIS SESSION TURNS ON, and the three qualifications that make it
true. Fong & Palsson predicted the growth rate of 39 of 50 strains to within
10%, GIVEN the measured substrate and oxygen uptake rates as inputs
(Supplementary Table 1), for strains that had been EVOLVED for hundreds of
generations. Drop any one of those and the claim is false. A slide saying "the
model predicts knockout growth rates" is wrong in exactly the way the week-9
and week-10 retrospectives are about.

THE PAYOFF. The eleven failures do NOT share a cause: tpi had no growth
predicted at all on three substrates (a route the reconstruction lacks), ppc
grew 11-12% slower than predicted (an objective slightly wrong). Different
fixes, and neither is "add more constraints".

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
    _object(d)
    _matrix(d)
    _nullspace(d)
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
           "two weeks back by their clock.\n "
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
                     "checks the predictions. Eleven are wrong. What do the "
                     "eleven have in common?"),
    ], top=2.05)
    d.notes(s,
           "Goals as questions, per lecture-design. The third one is the "
           "reading's own focus note and the answer is that they have NOTHING "
           "in common — which is the better lesson and I want them to arrive "
           "at it having guessed wrong.")


# ----------------------------------------------------------------- object ---
def _object(d):
    s = d.light()
    d.header(s, "segment 1", "frame  ·  the object, before any model")
    d.title(s, "A pathway, as a chemist would write it")
    d.rows(s, [
        ("glucose in", "phosphorylated on the way, and now it is G6P: six "
                       "carbons, committed."),
        ("two ways out of G6P", "phosphoglucose isomerase sends it down "
                                "glycolysis. Glucose-6-phosphate dehydrogenase "
                                "— zwf — commits it to the pentose "
                                "phosphate pathway, whose oxidative branch "
                                "loses one carbon as CO₂ one step later, at "
                                "gnd."),
        ("what the cell needs", "ribose-5-phosphate for nucleotides, "
                                "triose phosphate for everything else, and ATP "
                                "to pay for assembling any of it."),
        ("the branch", "pyruvate can go to acetate, or round the TCA cycle. "
                       "Acetate is fast and wasteful. The TCA is slow, and in "
                       "the nine-reaction model we are about to write it "
                       "yields three times the ATP."),
    ], top=2.00)
    d.foot(s, "Named enzymes, named metabolites, counted carbons. The matrix comes after.")
    d.notes(s,
           "I name zwf out loud and say what it does, because it is one of the "
           "six genes they read about and it gets deleted later in the hour. "
           "Be exact about the carbon: zwf oxidises G6P to the lactone and "
           "releases nothing; pgl opens the ring and gnd does the "
           "decarboxylation. Our v_zwf lumps all three, and on a slide headed "
           "'counted carbons' the lump has to be named as one.\n "
           "The three-times-ATP number is OURS — v_tca yields 3 against "
           "acetate's 1 in the toy. Real E. coli is nearer an order of "
           "magnitude. I say 'in the model we are about to write' and mean "
           "it.\n "
           "The branch is the thing to plant. Acetate versus TCA is a real "
           "decision a real cell makes, it is overflow metabolism, and it is "
           "the place the optimum will go all-or-nothing later.")


def _matrix(d):
    s = d.light()
    d.header(s, "segment 1", "release  ·  sixty seconds, on paper")
    d.title(s, "Write one column")
    d.rows(s, [
        ("the reaction", "triosephosphate isomerase: F6P → 2 T3P. One of the "
                         "nine you just read off the pathway."),
        ("your turn", "six metabolites, so the column has six entries. Write "
                      "them down, in order, with their signs."),
    ])
    d.foot(s, "Sixty seconds. I want the signs and I want the two.")
    d.notes(s,
           "Short, concrete, and it catches two things nothing else in the "
           "hour would.\n "
           "The answer: −1 on F6P, +2 on T3P, zero on the other four. "
           "Consumed is negative, produced is positive — that is a convention "
           "and I say so, because half the room will have picked the other one "
           "at some point.\n "
           "The TWO is the one I actually care about. A student who writes +1 "
           "has written a reaction that destroys three carbons, and S is the "
           "only object in this course that cannot be wrong about that. If "
           "someone writes +1, that is the best thing that happens in this "
           "segment and I use it.\n "
           "Nobody needs more than a minute. If they do, they did not have the "
           "pathway as firmly as the last surface suggested, and I would "
           "rather find that out now than in segment 3.")

    s = d.dark()
    d.header(s, "segment 1", "debrief  ·  what you just wrote")
    d.title(s, "A column is a reaction, counted")
    d.rows(s, [
        ("the column", "−1 on F6P, +2 on T3P, zero everywhere else. Consumed "
                       "negative, produced positive.", CYAN),
        ("the two is not decoration", "it is the carbon balance. Six carbons "
                                      "in, two three-carbon molecules out. "
                                      "Write +1 and you have built a network "
                                      "that destroys matter."),
        ("so what S is", "nine of those columns side by side. Every entry an "
                         "atom count, and the only part of a cell you can "
                         "write down exactly.", CYAN),
    ], label_color=CYAN)
    d.foot(s, "No rate constants anywhere in it. That is what makes it exact, and in two segments it is also what makes it not enough.")
    d.notes(s,
           "LEDGER: a column is a reaction; a row is a metabolite; an entry is "
           "an atom count.\n "
           "I plant the last line deliberately. Exactness and informativeness "
           "are about to trade against each other and I want the trade visible "
           "before it happens.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  the same nine lines, counted")
    d.title(s, "You have met this object before")
    d.image(s, FIG + "s20_network.png", M, 1.70, w=W - 2 * M)
    d.foot(s, "Session 3 built S and integrated with it. Nothing here is new except the question.")
    d.notes(s,
           "This is session 3's matrix and I say so plainly — they built one of "
           "these seven weeks ago and integrated dx/dt = S v.\n "
           "S is not an abstraction layered on the biology. It IS the biology, "
           "counted. "
           "Every column is one reaction, every row one metabolite, every "
           "entry an atom count.\n "
           "And it is the only part of a cell you can write down exactly.")


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
            ("dim = n_rxn − rank(S)",
             "nine reactions, rank six, so three are left over",
             "more reactions than balances is normal"),
            ("nothing picks v",
             "the stoichiometry has run out of things to say",
             "so an objective has to be imported"),
        ],
        board="S v = 0,  dim(null) = n_rxn - rank(S)",
        note="Five lines, and the last one is where the run lands: the "
             "stoichiometry has said everything it can say and it still has "
             "not picked a flux.\n "
             "Linger on step two. S v = 0 contains no rate constant — that is "
             "why it is exact, and it is also why it is not enough. Exactness "
             "and informativeness are trading against each other here.\n "
             "Session 3 wrote dim = n - rank(S) for the LEFT null space, "
             "where n was METABOLITES. This is the right null space and n is "
             "REACTIONS, so the step and the board both say n_rxn. A student "
             "who substitutes session 3's n here gets zero.\n "
             "Three degrees of freedom in a nine-reaction toy. A real "
             "reconstruction has hundreds, which is why nobody does this "
             "without an objective.")


def _program(d):
    s = d.light()
    d.header(s, "segment 3", "frame  ·  choosing, and what the choice costs")
    d.title(s, "Linear constraints, linear objective")
    d.rows(s, [
        ("the problem", "maximise c·v subject to S·v = 0 and "
                        "lo ≤ v ≤ hi. Linear in v throughout, so it is "
                        "a linear program — `scipy.optimize.linprog`, four lines."),
        ("the objective", "we are choosing biomass. That is a HYPOTHESIS about "
                          "what selection did to this organism, not something "
                          "the network tells you."),
        ("what you get", "an optimum at a vertex of the feasible region — "
                         "at least one. The theorem promises that a corner is "
                         "optimal. It does not promise the corner is alone."),
    ], top=2.00)
    d.foot(s, "A linear objective is flat along any tie, so the set of optima can be a whole edge. Segment 5 is what that costs you.")
    d.notes(s,
           "I say why it is linear, because they will assume optimisation is "
           "hard. Everything in sight is linear in v.\n "
           "The objective line is the one that matters for the rest of the "
           "hour. Biomass maximisation is not derived from anything — it is a "
           "guess about selection, and Fong and Palsson is the test of the "
           "guess.\n "
           "Vertex: worth a beat, and be careful with it. The theorem is "
           "that SOME optimum sits at a corner — not that the optimum is a "
           "corner and nothing else. When two arms tie, every blend of them "
           "is just as optimal, and 'sixty percent down this arm' is a "
           "perfectly good answer the solver will never volunteer. An earlier "
           "version of this slide said 'never a graded split'. Segment 5 "
           "builds the counterexample, so do not overclaim here.")

    s = d.light()
    d.header(s, "segment 3", "build  ·  the toy, solved")
    d.title(s, "Ten glucose in, and the answer is an integer")
    d.image(s, FIG + "s20_flux_map.png", M, 1.62, w=W - 2 * M)
    d.foot(s, "Biomass 4 exactly. Knock out the TCA and it is 10/3 — a different corner, not a scaled-down one.")
    d.notes(s,
           "I walk the left panel against the board derivation they just did. "
           "P5P has one producer and one consumer, so zwf equals biomass; G6P "
           "splits ten between pgi and zwf. F6P has one producer and one "
           "consumer, so tpi equals pgi. Then T3P, then the ATP balance, and "
           "b is at most four.\n "
           "ackA is exactly zero on the left and carries everything on the "
           "right. THAT is the vertex, and it is visible rather than asserted.\n "
           "The knockout costs them 17% of growth and it is exact — same six "
           "lines, one bound set to zero.")


def _knockouts(d):
    s = d.light()
    d.header(s, "segment 4", "frame  ·  deleting a reaction is one line of code")
    d.title(s, "A knockout is a bound set to zero")
    d.rows(s, [
        ("in the model", "bounds[reaction] = (0, 0). That is the entire "
                         "intervention — no new equations, no new "
                         "parameters."),
        ("which is the point", "you can ask about a strain nobody has built. "
                               "That is what makes this a design tool rather "
                               "than a description."),
        ("so let us ask", "seven real reactions in this network. Delete each "
                          "one in turn. What happens?"),
    ], top=2.00)
    d.foot(s, "One line of code per strain. Before I run it, you run it.")
    d.notes(s,
           "The one-line point is worth landing hard, because it is the reason "
           "anyone cares about constraint-based modelling at all.\n "
           "Then I hand the question over rather than answering it. They did "
           "the six-line derivation twenty minutes ago and they have "
           "everything they need.")

    s = d.light()
    d.header(s, "segment 4", "release  ·  two minutes, on paper")
    d.title(s, "Which deletions kill it?")
    d.rows(s, [
        ("the question", "of the seven real reactions, which deletions drive "
                         "biomass to exactly zero? Name them, and say what "
                         "they have in common."),
        ("you already did the work", "the same six lines you used to get "
                                     "biomass = 4. Ask what the network has "
                                     "no second route to."),
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
           "one and it is neither — hold it for the debrief.\n "
           "I take answers before the figure. The figure is then a check on "
           "them rather than a reveal.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  and the solver agrees")
    d.title(s, "Four of these are lethal, and exactly so")
    d.image(s, FIG + "s20_knockouts.png", M, 1.62, w=W - 2 * M)
    d.foot(s, "Zero is not a small number here. It is the network saying there is no other way round.")
    d.notes(s,
           "Check their four against the figure, name by name.\n "
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

    s = d.light()
    d.header(s, "segment 4", "debrief  ·  what the network has already decided")
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
           "you look. posb.fba.coupled_pairs returns exactly these two, and "
           "the test names the set so it cannot quietly start returning "
           "everything.\n "
           "Hold the zwf-biomass pair in mind. In two segments I add a second "
           "route to P5P and that coupling disappears, while pgi-tpi survives "
           "untouched. Same move, and it shows what the coupling was resting "
           "on.\n "
           "The consequence is the engineering content: there are quantities "
           "in a cell that regulation cannot touch, and stoichiometry tells "
           "you which ones before you do any experiment.")


def _alternates(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  the limitation built into the shape")
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
           "The second route is a MODELLING DEVICE and I say so out loud: "
           "E. coli has one glucose-6-phosphate dehydrogenase. Duplicated "
           "routes are everywhere in real reconstructions — transhydrogenases, "
           "parallel electron-transport branches — but this particular one is "
           "mine, built to make the point visible in a network they can hold "
           "in their heads.")

    s = d.light()
    d.header(s, "segment 5", "release  ·  ninety seconds, on paper")
    d.title(s, "Find a second answer")
    d.rows(s, [
        ("what the solver returned", "v_zwf = 4, v_zwf2 = 0, biomass = 4. "
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
           "variability analysis, which is the next surface.")

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
           "This is the correction to something I said two segments ago, and "
           "I make the correction out loud rather than hoping nobody "
           "noticed — the earlier surface said a linear program never gives "
           "you a graded split. It does, whenever there is a tie, and here is "
           "the tie.\n "
           "LEDGER: optimum at a vertex, yes. Unique, no. FVA is how you tell.\n "
           "And collect the debt from segment 4. We had TWO coupled pairs: "
           "pgi-tpi and zwf-biomass. Adding this second route gives P5P a "
           "second producer, so zwf-biomass is gone — coupled_pairs returns "
           "one pair now, not two. pgi-tpi is untouched, because nothing I "
           "added touches F6P. The coupling was never about the enzymes; it "
           "was about a row of S with exactly two entries in it, and I just "
           "put a third in one of those rows.\n "
           "Generic, not a quirk of the toy. Real reconstructions are full of "
           "parallel routes, and this is why a published flux map with no "
           "variability analysis beside it is an assertion rather than a "
           "result.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  the ranges, drawn")
    d.title(s, "Two fluxes, completely undetermined")
    d.image(s, FIG + "s20_alternate_optima.png", M, 1.62, w=W - 2 * M)
    d.foot(s, "The exact tie is ours; the limitation is general. The solver returns one point and tells you nothing about the rest.")
    d.notes(s,
           "The objective does not move — still four. But two fluxes are now "
           "undetermined across their whole range, and the solver picked one "
           "without saying so.\n "
           "Point at the two full-width bars. That width is the thing the "
           "single flux map was hiding.")


# ------------------------------------------------------------------- Fong ---
def _fong(d):
    s = d.light()
    d.header(s, "segment 6", "frame  ·  somebody tested the hypothesis")
    d.title(s, "Six deletions, fifty strains, and a prediction each")
    d.rows(s, [
        ("the strains", "in-frame deletions of ackA, frd, pck, ppc, tpi and "
                        "zwf, built by λ-red recombination in E. coli "
                        "K-12 MG1655. Each was evolved on four carbon "
                        "sources, in replicate: 24 cases, fifty evolved "
                        "strains."),
        ("the model", "904 genes, 1,327 reactions. A knockout is simulated by "
                      "deleting that gene's reactions from the list — the same "
                      "one line you just saw."),
        ("the inputs", "the measured substrate and oxygen uptake rates were "
                       "fed in as constraints. Supplementary Table 1 is "
                       "that table."),
        ("the result", "the growth rate was predicted to within 10% for "
                       "39 of 50."),
    ], top=1.95)
    d.notes(s,
           "The third row is the one nobody reads and it changes what the "
           "number means. The model was handed its own boundary conditions — "
           "the uptake rates are measurements, not predictions — and asked for "
           "ONE number out.\n "
           "That is still a real result. It is not 'the genome predicts "
           "growth', and I want them to be able to say the difference.\n "
           "904 genes and 1327 reactions is iJR904, Reed 2003, which is the "
           "reconstruction their own reference 1 points at.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  the word that is doing the work")
    d.title(s, "Evolved")
    d.rows(s, [
        ("what they did", "built the deletion strain, then passaged it "
                          "daily for fifty days before measuring."),
        ("why it matters", "a freshly built knockout is NOT where the model "
                           "says it should be. The agreement appears after "
                           "selection has had time to act."),
        ("so the claim is", "not this is how fast the strain grows — it is "
                            "this is where selection takes the strain. "
                            "Flux balance predicts a destination, not a "
                            "starting point."),
        ("the prior paper", "Ibarra, Edwards & Palsson, Nature 420:186 "
                            "(2002) — a population starting below the line of "
                            "optimality, moving onto it."),
    ], top=1.95)
    d.foot(s, "An optimality assumption is a claim about selection. This is the experiment that tests it.")
    d.notes(s,
           "This is the heart of the session and it is one word in their "
           "abstract.\n "
           "Ibarra 2002 made the point first and is Fong's own reference four. "
           "I mention it and move on.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  the evidence for the word")
    d.title(s, "Growth rate, day by day")
    d.paper_figure(s, "fong2004_sfig1", M + 2.02, 1.75, 5.18, 4.0,
                   "Fong & Palsson 2004, Supplementary Fig. 1",
                   "six genes, thirteen parallel lineages, fifty days",
                   show_caption=True)
    d.notes(s,
           "Six panels, one per gene, thirteen lineages between them. The "
           "x axis is DAYS of evolution, 0 to 50 — the word 'generation' does "
           "not appear anywhere in this paper, and an earlier version of this "
           "slide put it in their mouths.\n "
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
           "or pyruvate; ppc2 would.\n "
           "That divergence is the setup for the next segment, because three "
           "of the eleven failed predictions are single lineages whose "
           "parallel twin was fine.")


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
    d.title(s, "What do the failures have in common?")
    d.rows(s, [
        ("you were asked", "to come with a guess. Hands."),
        ("first, they are not eleven of a kind", "eight involve ppc or "
         "tpi. The other three — pck on α-ketoglutarate, zwf on glucose "
         "and on glycerol — are single replicates, and the authors decline to "
         "diagnose them: \"may be a result of experimental and evolutionary "
         "variability.\""),
        ("second, they do not sort by gene", "both strains miss both ways. "
         "ppc runs 28% slow on glucose and 11–12% slow on α-ketoglutarate. "
         "tpi runs 33% slow on glucose — and on lactate it grew above 0.70 h⁻¹ "
         "when no growth at all was predicted."),
        ("and the model was right where it mattered most", "tpi on malate and "
         "on succinate: no growth predicted, and none observed. Two "
         "correct predictions that are easy to score as failures."),
    ], top=1.90)
    d.foot(s, "Fong & Palsson 2004, p. 1057. Eight of eleven, and the eight do not split by gene.")
    d.notes(s,
           "I take the guesses first and let the wrong ones stand — 'they're "
           "all the same pathway', 'they're all poor carbon sources'. My own "
           "first guess was that tpi was a structural failure and ppc a "
           "quantitative one, and the paper says otherwise in a single "
           "sentence.\n "
           "The row that surprises people is the last one. A no-growth "
           "prediction that comes true is a success, and it looks like a blank "
           "panel in the supplementary figure — the two tpi panels that say No "
           "Growth are the model getting it right.\n "
           "Lactate is the one real structural miss: predicted nothing, got "
           "0.70 per hour. Same gene, same model, three substrates, two right "
           "and one wrong.")

    s = d.light()
    d.header(s, "segment 7", "debrief  ·  what the authors conclude from it")
    d.title(s, "Accurate in half the cases, for both strains")
    d.rows(s, [
        ("their sentence", "\"Predicted growth rates were accurate in half the "
         "cases for both the ppc– and tpi– strains, suggesting that the "
         "reconstructed network may be incomplete.\""),
        ("notice what they do not say", "they do not blame the objective. One "
         "diagnosis, covering both genes: the reaction list is missing "
         "something the cell can do."),
        ("why that follows", "a strain that is predicted correctly on two "
         "substrates and wrongly on two others has not got a wrong objective — "
         "an objective is the same on every substrate. What changes with the "
         "carbon source is which reactions are carrying flux."),
        ("the design consequence", "a failure localises the gap. Which "
         "substrate broke it tells you where in the network to go looking, and "
         "that is what makes a wrong prediction worth more than a right one."),
    ], top=1.90)
    d.foot(s, "A model that fails on some substrates and not others is pointing at a reaction, not at an assumption.")
    d.notes(s,
           "This is the surface the reading was assigned for, and it is a "
           "better lesson than the one I had planned to teach.\n "
           "The argument in row three is worth going slowly on. An objective "
           "is a single assumption applied everywhere; if it were wrong you "
           "would expect to be wrong everywhere, not on half the substrates. "
           "Substrate-dependent error points at the stoichiometry.\n "
           "And it closes the hour's loop. We imported an objective because "
           "the stoichiometry ran out of things to say. The failures say the "
           "stoichiometry was also the thing that was incomplete — so the "
           "fix is more biochemistry, not a better guess about selection.")


def _close(d):
    s = d.dark()
    d.header(s, "close", "where this goes")
    d.title(s, "Known exactly, and still not enough")
    d.rows(s, [
        ("today — session 20",
         "the coupling is written down to the atom. It buys you the "
         "constraints, and it tells you nothing about rates — so an objective "
         "has to be imported, and it is a hypothesis.", CYAN),
        ("Thursday — session 21",
         "a coupling that is not written down anywhere. Worse: the diagram "
         "draws it as an arrow, and an arrow is a lie about the physics."),
        ("and then",
         "once you have met three contexts that break a circuit, the question "
         "stops being how to model each one and becomes how to reject all of "
         "them. That is the week after."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "S is exact because it only counts atoms. That is also why it cannot tell you a rate.")
    d.notes(s,
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
                      "Biotechnol 2014 — a load driver. A different Mishra "
                      "from session 18's: same surname, same senior author, "
                      "nine days apart. Cite both with the year."),
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
