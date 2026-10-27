"""Session 22 — Robustness and control: rejecting the disturbance instead of
modelling it.

Tuesday 10 November 2026. Part II, seventh session. PS8 is out and assesses
this session; Aoki 2019 was assigned at the close of session 21.

WHAT THIS SESSION IS. Rung 4, and the arc's turn. Rungs 1-3 each found a
coupling and dealt with it on its own terms -- measure the burden, compute the
fluxes, insulate the interface -- and every cure was specific to its
disturbance. This session says you can stop doing that:

    AN INTEGRATOR DOES NOT NEED TO KNOW WHAT THE DISTURBANCE IS.

The room should feel it as a release, which is why it comes after three
sessions of patches rather than before them.

THE SENTENCE THE HOUR IS BUILT ON, in the authors' words (Aoki et al., Nature
570:533, 2019): "the steady-state value of the output is determined solely by
the ratio mu/theta. Notably, it does not depend on the topology and parameters
of the circuit of interest." The clause before it is "as long as the
closed dynamics are stable", and it is not decoration.

THE BEAT THAT MAKES IT PART II'S SESSION AND NOT A CONTROL-THEORY LECTURE.
Aoki implement the annihilation Z1 + Z2 -> nothing with a sigma factor and its
anti-sigma factor from B. subtilis, SigW and RsiW, and the paper describes the
mechanism in this course's own word: "In its natural context, RsiW stably
SEQUESTERS and holds SigW inactive."

Session 18 named sequestration. Session 19 found it in the ribosome pool,
session 21 in the downstream operator, and the ladder's invariant has been
that a molecule held by something that is not its target is not available to
do its job. HERE THAT UNAVAILABILITY IS THE MECHANISM OF THE CURE. The same
physics that was the problem on rungs 1-3 is what makes rung 4 work. Say it in
those words at the sequestration debrief.

AND THEY CONTROL GROWTH RATE, not GFP. sfgfp replaced by metE in a delta-metE
host in methionine-free medium, so the cell's own growth rate is the regulated
output. Session 19 opened Part II on growth rate as the thing a circuit
changes; this closes it on growth rate as the thing a circuit regulates.

TWO FAILURES, AND THE DECK MUST NOT BLUR THEM.
  SATURATION  the controller acts only through Z1 >= 0, so it can only push
              UP. Past d = gamma*mu/theta = 2.5 there is NO steady state --
              Z1 hits zero, the annihilation FLUX PINS at mu (it cannot
              exceed it), so Z2 grows at theta*X - mu while X settles at
              d/gamma. No steady state, because Z2 climbs forever.
  THE LEAK    dilution of Z1 and Z2 makes the integrator leak. A steady state,
              in the wrong place, first order in delta.
Saturation is the controller running out of authority. The leak is rung 1
eating the guarantee. PS8 Q4c asks about the first and Q5 about the second.

WHERE THE NUMBERS COME FROM. sessions/s22-control/NUMBERS.md, every one with
its KIND. Ours are COMPUTED from posb.control; Aoki's are MEASURED and are
never mixed with ours -- that was session 21's failure and the KIND column is
how this one avoids it.

THE PS8 CONTRACT. Q4 and Q5 were released on 5 November against this design,
five days before this session is taught. Nothing here may contradict them.

CROSS-DECK VOCABULARY GREP, run 26 October against decks s01-s21. I expected
all ten terms to be new. Four were not, and two of those changed this deck:

  integral feedback  NEW        set point       NEW        closed loop  NEW
  antithetic         NEW        anti-sigma      NEW
  actuator           s16        sigma factor    s06        disturbance  s14,19,20,21
  adaptation         s10, s20   open loop       s07, s10, s13

  * ADAPTATION is s10's word, with a NUMBER attached. The incoherent
    feedforward loop adapts, and PS5 autograded its adaptation error at
    final/peak = 0.62 (T26). So the room has already built a circuit that
    partly forgets a step, and has measured how badly. This deck must say so
    at the derivation, or today's exact zero sounds like a new trick rather
    than the same goal finally met. See _derivation and _close.
  * OPEN LOOP is established (s07, s10, s13) and needs no introduction. s07
    also did negative autoregulation against an open loop, which is why the
    home guide's proportional-control item points back at it instead of
    pretending the comparison is new.
  * "plant", "actuator", "set point", "error" and the open/closed distinction
    are now DEFINED on a surface, on the block diagram at the top of
    segment 2, before any algebra uses them. They were not, in the first
    build, and the docstring claimed they were -- which is how it went
    unnoticed. The error is also written down as a derivation step now
    (e = mu/theta - X), because the hour is about driving it to zero and no
    surface had ever said what it was.

AND THE NAME COLLISION THE GREP TURNED UP. posb/control.py originally exported
`adaptation_error` for X_ss - mu/theta, a DIFFERENCE. Session 10 already uses
"adaptation error" for final/peak, a RATIO, and that one is autograded. Both
make zero mean "good", so nothing would have warned a student. Renamed to
`setpoint_error`, and PS8 Q4c now flags the overload where it is first used.

NO PRINTED TIME RANGES. Minutes are Adam's.

Run:  python tools/build_decks.py s22
"""
from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)

FIG = "figures/build/"
FILENAME = "s22-control"


def build():
    d = Deck("Session 22 — Robustness and control", session=22)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _goals(d)
    _frame(d)
    _vocabulary(d)
    _derivation(d)
    _instantiate(d)
    _motif(d)
    _sequestration(d)
    _aoki(d)
    _evidence(d)
    _leak(d)
    _close(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    s = d.dark()
    d.text(s, "Session 22  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "You do not have to know what hit you",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "Three sessions of cures, each built for its own disease. "
              "Today: one device that rejects a disturbance nobody told it "
              "about — and it works because of the thing that has been going "
              "wrong all term.",
           M, 4.42, 8.6, 1.70, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.45, 9.0, 0.4, size=13, color=SILVER)
    d.notes(s,
           "This is the arc's turn and I say so in the first minute. Three "
           "patches, each tailored, and today we stop patching.\n "
           "The sting in the opening line is deliberate — the mechanism that "
           "makes the cure work is sequestration, which has been the problem "
           "since session 18. I do not explain that yet. Segment 6 is where "
           "it lands.")


def _retrieval(d):
    s = d.light()
    d.header(s, "open", "retrieval — sessions 10, 19 and 21")
    d.title(s, "Before we start")
    d.rows(s, [
        ("1", "Session 19: your circuit expresses something useless at 10% of "
              "the proteome. Which way does the growth rate move, and which "
              "way does a protein's response time move?"),
        ("2", "Session 21: a downstream module reads your regulator. What did "
              "the load cost you, and what could you NOT do about it?"),
        ("3", "Both of those were cures aimed at one disturbance. Name the "
              "disturbance each one was aimed at."),
        ("4", "Session 10: the incoherent feedforward loop. It took a step "
              "and came back down. How far back? What did we call that "
              "number, and what did it depend on?"),
    ], top=2.05, label_w=0.7)
    d.notes(s,
           "One and two are retrieval. Three is the frame for the hour and it "
           "is the one I wait for.\n "
           "Answers: growth rate falls, so gamma falls, so the response time "
           "goes UP for everything in the cell. The load cost speed and — if "
           "the complex dilutes — level, and you could not lower it, because "
           "the bill is the site count.\n "
           "Three: burden was aimed at competition for ribosomes; the load "
           "driver at one interface. Each cure needs you to have NAMED the "
           "disturbance first. That is the thing today removes.\n "
           "FOUR IS THE ONE THAT SETS UP THE HOUR. Adaptation error = final / "
           "peak = 0.62, which they computed on PS5. It came back 38 per cent "
           "of the way and no further, and that number depended on every rate "
           "constant in the motif. So they have already built a circuit that "
           "partly forgets a step. Today's question is not whether adaptation "
           "is possible — it is whether it can be EXACT, and free of the "
           "parameters.")


def _goals(d):
    s = d.light()
    d.header(s, "open", "what you should be able to do by the end")
    d.title(s, "Three questions")
    d.rows(s, [
        ("the guarantee", "A controller holds its output at a set point. What "
                          "is the set point allowed to depend on — and what "
                          "is it not?"),
        ("the device", "Two molecules that destroy each other. Why is that an "
                       "integrator, and why does the circuit being controlled "
                       "not get a vote?"),
        ("the limit", "The guarantee is exact on paper. Name the ways a "
                      "real cell breaks it — there are more than two."),
    ], top=2.05)
    d.notes(s,
           "The third one is the hour's honesty and it has TWO answers, which "
           "I say now so nobody leaves with one: the controller can run out "
           "of authority, and the controller can leak. Different failures, "
           "different fixes, and PS8 asks about both.")


# ------------------------------------------------------------------ frame ---
def _frame(d):
    s = d.dark()
    d.header(s, "segment 1", "frame  ·  three cures, each built for its disease")
    d.title(s, "What would it take to stop patching?")
    d.rows(s, [
        ("19", "the host's machinery. You measured the burden and budgeted "
               "against it — and the budget is specific to that burden."),
        ("20", "the host's metabolism. You computed the fluxes exactly, and "
               "had to import an objective to do it."),
        ("21", "the module next door. You derived the load and built a stage "
               "fast enough to outrun it — that stage insulates against THAT "
               "interface and nothing else.", CYAN),
        ("the pattern", "every cure so far needs you to name the disturbance "
                        "first. Miss one and the cure does not cover it.",
         AMBER),
        ("and note", "f is unknown, so a CHANGE in f is covered too — a "
                     "different rate constant, a different temperature, a "
                     "protease you did not plan for. Not only a term added "
                     "on the end."),
    ], label_color=CYAN)
    d.foot(s, "Three disturbances, three devices. The question is whether there is a device that does not need the list.")
    d.notes(s,
           "I walk the three deliberately, because the release only lands if "
           "the pattern is explicit first.\n "
           "The fourth row is the hinge: every one of those cures is a "
           "FEEDFORWARD argument. You model the disturbance, then you build "
           "against your model. If the model is wrong or the list is "
           "incomplete, so is the cure.\n "
           "Then the question, and I leave it hanging into the derivation.")


# ------------------------------------------------------------- derivation ---
def _vocabulary(d):
    s = d.light()
    d.header(s, "segment 2", "frame  ·  five words, before any algebra")
    d.title(s, "The words this hour is made of")
    d.image(s, FIG + "s22_block_diagram.png", M, 1.60, w=W - 2 * M, h=5.05)
    d.foot(s, "\"Plant\" is the control engineer's word for whatever you are controlling. It is not a metaphor and it has nothing to do with botany.")
    d.notes(s,
           "Half this room has never met any of these words and the other "
           "half has used them for years, so I spend the time and I say why: "
           "every one of them turns up in the next four surfaces.\n "
           "PLANT is the one to be explicit about. It is the thing being "
           "controlled — your circuit, the cell, whatever sits downstream of "
           "the actuator — and in a synthetic biology course the wrong "
           "reading is sitting right there. I say the botany line out loud; "
           "it gets a laugh and it fixes the word.\n "
           "ERROR is the one that matters most, because the whole derivation "
           "is about driving it to zero and we have never written it down: "
           "e = mu/theta − X. Set point minus output. That is all.\n "
           "ACTUATOR is what the controller pushes with. Today it will be a "
           "molecule, and the fact that a molecule cannot go below zero is "
           "the entire second half of the hour.\n "
           "CLOSED and OPEN: the loop is closed when the sensor reports back. "
           "Aoki's control strain is this diagram with that one arrow cut, "
           "which is worth pointing at now so it is familiar later.")


def _derivation(d):
    d.derivation(
        None, "segment 2", "build  ·  integral feedback, on no particular plant",
        "Zero error is the only place it can rest",
        [
            ("a plant, any plant",
             "dX/dt = f(X, u) + d",
             "f unknown, d unknown and constant"),
            ("the error, written down",
             "e = mu/theta - X",
             "set point minus output"),
            ("the controller integrates it",
             "du/dt = theta·e = mu - theta·X",
             "u is the running total of e"),
            ("at steady state du/dt = 0",
             "mu - theta·X = 0",
             "whatever f was doing"),
            ("so the output is",
             "X = mu / theta",
             "two constants, and no f anywhere"),
        ],
        board="e = mu/theta - X;  du/dt = theta·e   =>   X_ss = mu/theta",
        note="AT THE BOX, SAY IT AGAINST SESSION 10. Their feedforward loop "
             "adapted too, and its adaptation error was 0.62 — final over "
             "peak — and it moved whenever any rate constant moved. This one "
             "is ZERO, and there is no rate constant in it to move. Same "
             "goal, and the difference between a motif that fights the step "
             "and a motif that integrates it.\n "
             "Four lines, on a plant I deliberately refuse to specify. The "
             "generality IS the result and specifying the plant would throw it "
             "away.\n "
             "Step two is new and it is the one the room has been missing: "
             "e = mu/theta − X, set point minus output, and du/dt = theta·e "
             "says u is the RUNNING TOTAL of the error. That is what the word "
             "integral is doing in the name of this thing.\n "
             "Step four. du/dt = 0 is forced at ANY steady state — "
             "it is what steady state means — so the error has to be zero. "
             "Not small. Zero.\n "
             "LEDGER, left wing: X_ss = mu/theta, and f is not in it.\n "
             "Aoki's own sentence is worth reading out here: the steady state "
             "is determined solely by the ratio mu/theta, and it does not "
             "depend on the topology and parameters of the circuit of "
             "interest — as long as the closed dynamics are stable, which is "
             "the clause everyone drops and I do not. That is what we just "
             "derived, and the next surface makes them check it.\n "
             "AND THE CONSEQUENCE, which is the reason to care: you do not "
             "have to characterise your plant. Change host, change promoter, "
             "change chassis — the controller ports without re-tuning, "
             "because none of those appear in the answer. That is what this "
             "device buys you and it is worth saying here, not fifteen "
             "surfaces later on the ledger.")


def _instantiate(d):
    s = d.light()
    d.header(s, "segment 3", "release  ·  on paper")
    d.title(s, "Put a plant under it")
    d.rows(s, [
        ("the plant", "session 5's protein, driven by the controller: "
                      "dX/dt = k·u − γX + d, where u is whatever the "
                      "controller pushes with."),
        ("your turn", "write down where the output settles. Then say which of "
                      "k, γ, d and the controller's own constants it is "
                      "allowed to depend on."),
    ])
    d.foot(s, "Two minutes. You do not need to solve the dynamics — you need the steady state, and you proved it on the last surface.")
    d.notes(s,
           "Short, and almost everyone gets it, which is the point: the "
           "answer does not require the plant at all.\n "
           "X = mu/theta. It depends on the two CONTROLLER constants and on "
           "nothing else — not k, not gamma, not d.\n "
           "The one to push on: 'but k and gamma must do something.' They do. "
           "They set how it gets there and how long it takes. They do not set "
           "where it ends up, and that distinction is the hour.")

    s = d.dark()
    d.header(s, "segment 3", "debrief  ·  where it settles")
    d.title(s, "X = μ / θ")
    d.rows(s, [
        ("what is in it", "two controller constants. μ, the rate Z₁ is made "
                          "at. θ, the strength of the sensing.", CYAN),
        ("what is not", "k. γ. d. Not one of them survives into the answer, "
                        "and you did not need to know any of them."),
        ("what k and γ do", "they set the ride — how fast it gets there, how "
                            "much it rings on the way. They do not set the "
                            "destination."),
    ], label_color=CYAN)
    d.foot(s, "Everything for the rest of the hour is this box, or a reason it fails.")
    d.notes(s,
           "The answer goes UP, not just around the room, because the eight "
           "people who did not speak need it too.\n "
           "The push-back I want: 'but k and gamma must do something.' They "
           "do, and the next two surfaces are exactly that — the ride against "
           "the destination.\n "
           "A student will ask whether d really drops out. It does, and the "
           "step figure is next.")

    s = d.light()
    d.header(s, "segment 3", "build  ·  send a disturbance in")
    d.title(s, "Same plant, same disturbance, one difference")
    d.image(s, FIG + "s22_step.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "The open loop takes the hit and keeps it. The closed loop takes the hit and gives it back.")
    d.notes(s,
           "This is the first thing to show, before any claim about "
           "generality: a step disturbance arrives and the two circuits do "
           "different things with it.\n "
           "The open loop steps up and stays up — its new level is the old "
           "one plus d/gamma, which is exactly session 5's answer, because "
           "without feedback that is all this is.\n "
           "The closed loop moves, then comes back. All the way back, not "
           "most of the way. Point at the tail and say that the gap is zero, "
           "not small, and that is what the derivation bought us.\n "
           "Ideal controller, no dilution. Segment 6 takes that away.")

    s = d.light()
    d.header(s, "segment 3", "debrief  ·  and the computer agrees")
    d.title(s, "Four different plants, one set point")
    d.image(s, FIG + "s22_plant_does_not_matter.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "Plant gain quadrupled, removal rate cut fivefold, annihilation ten times faster. The destination does not move.")
    d.notes(s,
           "I change a plant parameter and we watch the answer not move. Four "
           "runs, and the steady state is 5.0000000000 in every one of them.\n "
           "The orange curve is the one to point at: slower removal means it "
           "rings for a long time and overshoots badly. It still lands on "
           "five. A worse plant is a worse RIDE, not a worse destination.\n "
           "This is the ideal controller, no dilution. I say that every time "
           "I show it, because the leak segment takes it away.")


# ------------------------------------------------------------------ motif ---
def _motif(d):
    s = d.light()
    d.header(s, "segment 4", "frame  ·  that integral has to be a molecule")
    d.title(s, "Nothing in a cell computes an integral")
    d.rows(s, [
        ("what we assumed", "du/dt = μ − θX. Something in the cell has to "
                            "accumulate the error and remember it."),
        ("what a cell has", "production, degradation, binding. No memory, no "
                            "arithmetic, no stored running total."),
        ("so the question is", "which arrangement of molecules has a quantity "
                               "that rises and falls exactly as the error "
                               "does, and forgets nothing?", CYAN),
    ], top=2.00, label_color=CYAN)
    d.notes(s,
           "This is the step that makes it synthetic biology rather than "
           "control theory, and skipping it is how this hour would go wrong.\n "
           "An integrator needs a quantity with no leak — anything that "
           "decays forgets, and a controller that forgets is not an "
           "integrator. I leave that open; the leak segment comes back "
           "for it.")

    s = d.light()
    d.header(s, "segment 4", "frame  ·  the arrangement, before the algebra")
    d.title(s, "Two molecules that destroy each other")
    d.image(s, FIG + "s22_motif_topology.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "Z₁ is made at a constant rate and drives the output. Z₂ is made in proportion to the output. They destroy each other.")
    d.notes(s,
           "The picture first, and the algebra after. The first build of this "
           "deck put the two rate equations up cold and the release that "
           "follows asked the room to subtract them — which works for anyone "
           "who already thinks in rate equations and leaves everyone else "
           "trying to work out what Z1 and Z2 ARE.\n "
           "Three strokes: Z1 at a constant rate mu, Z2 at theta times the "
           "output, and the two annihilate. The plant is a box marked ANY "
           "TOPOLOGY, ANY PARAMETERS because that is the whole claim.\n "
           "Note the arrows on the annihilation converge — both species are "
           "consumed. That is not the same as reversible binding, and the "
           "home guide asks them to pin the difference down.\n "
           "Then the two rate equations on the board, and stop.")

    s = d.light()
    d.header(s, "segment 4", "release  ·  two lines of algebra")
    d.title(s, "Subtract them")
    d.rows(s, [
        ("on the board", "dZ₁/dt = μ − η·Z₁Z₂      dZ₂/dt = θ·X − η·Z₁Z₂"),
        ("your turn", "subtract the second from the first."),
        ("then vote", "which quantity in this circuit is the integral of the "
                      "error?    Z₁    ·    Z₂    ·    X    ·    Z₁ − Z₂",
         AMBER),
    ], top=2.05)
    d.foot(s, "You are looking for something you derived twenty minutes ago.")
    d.notes(s,
           "THE KEY RELEASE OF THE HOUR. Do not do this for them — it is two "
           "lines of algebra and the whole mechanism is inside it.\n "
           "The annihilation term is IDENTICAL in both equations, so it "
           "cancels, and what is left is d(Z1 − Z2)/dt = mu − theta X. That "
           "is the controller we derived, with u = Z1 − Z2.\n "
           "The thing to say once they have it: nothing here MEASURES "
           "anything. There is no comparator and no subtraction step. The "
           "subtraction is done by the chemistry, for free, because one "
           "reaction consumes both species at the same rate.\n "
           "LEDGER: Z1 − Z2 integrates the error; the annihilation cancels.\n "
           "AND THE DISTINCTION THE REST OF THE HOUR RUNS ON. u = Z1 − Z2 is "
           "what INTEGRATES. The plant is driven by Z1 ALONE — Z1 is the "
           "actuator, which is Aoki's own word for it. Those are two "
           "different quantities, and I write both on the board:\n "
           "   dX/dt = k·Z1 − gamma·X + d        the plant sees Z1\n "
           "   d(Z1 − Z2)/dt = mu − theta·X      the controller integrates\n "
           "The set point does not care which, because the integral is what "
           "forces the error to zero. The actuator bound cares completely, "
           "because Z1 ≥ 0 and Z1 − Z2 has no sign restriction at all. If I "
           "leave the plant written in terms of u, the leak segment's bound "
           "is a bound on nothing.\n "
           "I take the vote before anyone explains, hands up, and I count. "
           "Z1 and Z2 both draw votes, which is the useful part: either one "
           "alone still has the annihilation term in it and so is not a clean "
           "running total of anything. Only the DIFFERENCE cancels it.\n "
           "The eta question will come: eta does not appear in the result at "
           "all. Faster annihilation is a faster ride, not a different "
           "destination — which is the orange curve on the four-plants figure.")


    s = d.light()
    d.header(s, "segment 4", "debrief  ·  what you just derived, drawn")
    d.title(s, "The antithetic motif")
    d.image(s, FIG + "s22_motif.png", M, 1.66, w=W - 2 * M, h=4.95)
    d.foot(s, "The banner is your two lines. Nothing in the picture measures anything — the chemistry does the subtraction.")
    d.notes(s,
           "UP ONLY AFTER THE RELEASE. The banner across the top is the line "
           "they just derived, and putting it on the wall before they do the "
           "algebra kills the release — which is what the first cut of this "
           "deck did.\n "
           "Walk the picture once: Z1 made at a constant rate, Z2 made in "
           "proportion to the output, the two destroy each other, and the "
           "plant is a box labelled ANY TOPOLOGY, ANY PARAMETERS because that "
           "is the whole claim.")

def _sequestration(d):
    s = d.dark()
    d.header(s, "segment 4", "debrief  ·  the reaction underneath it")
    d.title(s, "You have seen this reaction all term")
    d.rows(s, [
        ("18", "a factor held by decoy sites. You named it: sequestration."),
        ("19", "a ribosome held by every other mRNA in the cell."),
        ("21", "a regulator held by its own downstream targets — and the "
               "holding was the cost."),
        ("22", "Z₁ held by Z₂. Aoki built it from a σ factor and its anti-σ "
               "factor, and the paper's own words are: RsiW stably "
               "SEQUESTERS and holds SigW inactive.", CYAN),
    ], label_color=CYAN)
    d.foot(s, "Four sessions, one reaction. On three of them it was the disease. Here it is the cure.")
    d.notes(s,
           "THIS IS THE BEAT OF PART II AND I DO NOT RUSH IT.\n "
           "Every rung of the ladder has been the same sentence: a molecule "
           "held by something that is not its target is not available to do "
           "its job. On rungs one to three that unavailability was the "
           "problem — burden, coupling, retroactivity.\n "
           "Here the unavailability IS the mechanism. The whole reason Z1 and "
           "Z2 annihilate cleanly enough to integrate is that each one takes "
           "the other out of circulation, completely, with no leftover.\n "
           "Same physics, opposite sign. If they take one thing from Part II, "
           "this is it.\n "
           "LEDGER: sequestration — the disease on rungs 1-3, the cure on "
           "rung 4.")


# ------------------------------------------------------------------- Aoki ---
def _aoki(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  somebody built it, out of parts you know")
    d.title(s, "σ and anti-σ")
    d.rows(s, [
        ("σ factor", "the subunit that tells RNA polymerase which promoters "
                     "to read. SigW switches on P_sigW — more SigW, harder "
                     "that promoter fires. Z₁ is the ACTUATOR.", CYAN),
        ("anti-σ factor", "binds a σ one-to-one and holds it off the "
                          "polymerase. RsiW comes from P_BAD, which AraC "
                          "drives, and AraC sits downstream of the output. "
                          "Z₂ is the SENSOR.", AMBER),
        ("why that is an annihilation", "a σ held by its anti-σ does nothing, "
                                        "and the two leave circulation "
                                        "together — one for one, which is "
                                        "exactly what made the subtraction "
                                        "cancel."),
    ], top=1.95, label_color=CYAN)
    d.foot(s, "Both from B. subtilis, moved into E. coli. The annihilation is not engineered — it is what these two proteins already do.")
    d.notes(s,
           "Session 6 is the last time they saw a sigma factor and anti-sigma "
           "has never come up, so I draw the mechanism rather than naming "
           "it.\n "
           "The mapping is the part that is easy to leave implicit and must "
           "not be: SigW is Z1 because it ACTUATES — it turns the output "
           "promoter on. RsiW is Z2 because its expression is driven by AraC, "
           "which is downstream of the output, so its production rate tracks "
           "the output. That is the theta*X term, built out of a two-step "
           "chain the paper draws in Fig. 2a.\n "
           "Then why it is an annihilation and not just inhibition: the "
           "complex takes both out together, one for one. A pair that binds "
           "reversibly would not do this, which is the home guide's item 2.")

    s = d.light()
    d.header(s, "segment 5", "frame  ·  and what they regulate with it")
    d.title(s, "They control the growth rate")
    d.rows(s, [
        ("the output", "not GFP. They replace sfgfp with metE, the last step "
                       "of cobalamin-independent methionine biosynthesis, in "
                       "a ΔmetE host in methionine-free medium — so the "
                       "controlled output is the cell's GROWTH RATE.", CYAN),
        ("the control", "the open-loop strain is the same circuit with the "
                        "anti-σ module (P_BAD–rsiW) deleted: the sensor arrow "
                        "cut, everything else the same. It also carries less "
                        "protein, which is session 19's confound and worth "
                        "naming."),
    ], top=2.05, label_color=CYAN)
    d.foot(s, "Session 19 opened Part II on growth rate as the thing your circuit changes. This closes it on growth rate as the thing a circuit regulates.")
    d.notes(s,
           "The growth-rate choice is worth a beat and it is not decoration — "
           "it is the arc closing on the same variable it opened on.\n "
           "The open-loop control is the cleanest I have shown all term and I "
           "say why: they delete ONE module, the anti-sigma. Same promoters, "
           "same host, same medium, same everything. The only difference is "
           "whether the loop closes. That is what a control should be.")


def _evidence(d):
    s = d.light()
    d.header(s, "segment 5", "release  ·  read their two p-values")
    d.title(s, "Is that adaptation?")
    d.rows(s, [
        ("what they did", "perturbed the temperature, 37 °C against 30 °C, "
                          "and measured each circuit's growth rate relative "
                          "to its own 37 °C rate. n = 3."),
        ("what they got", "closed loop P = 0.2261. Open loop "
                          "P = 7.769 × 10⁻⁵."),
        ("your turn", "what does each of those two numbers license you to "
                      "say?"),
    ], top=2.00)
    d.foot(s, "Ninety seconds. Two p-values, and they are not two of the same thing.")
    d.notes(s,
           "The small P is easy and they will get it: the open loop's growth "
           "rate moved, decisively.\n "
           "The large one is the question. P = 0.2261 is a FAILURE TO DETECT "
           "a difference at n = 3. It is not a demonstration that there is "
           "none, and with three replicates the test could not have detected "
           "a modest one.\n "
           "They met this exact distinction five days ago on PS8, with "
           "Mishra 2014's 432 against 396 at n = 3 and p = 0.10. Say so, in "
           "the same words. Twice in a fortnight is how it sticks.\n "
           "What would settle it: an equivalence test, or more replicates, or "
           "a stated effect size they can rule out.")

    s = d.dark()
    d.header(s, "segment 5", "debrief  ·  what each number licenses")
    d.title(s, "Two P values, and they are not two of a kind")
    d.rows(s, [
        ("P = 7.769 × 10⁻⁵", "the open loop's growth rate moved with "
                             "temperature. Reject the null. Say it plainly.",
         CYAN),
        ("P = 0.2261", "we FAILED TO DETECT a difference at n = 3. That is "
                       "not the same as showing there is none, and with three "
                       "replicates a modest change would have looked like "
                       "this too.", AMBER),
        ("what would settle it", "a bound on the difference rather than a "
                                 "failure to reject — which needs a stated "
                                 "effect size, and more replicates than "
                                 "three."),
    ], top=2.00, label_color=CYAN)
    d.foot(s, "A large P is the absence of evidence. It is not evidence of absence, and at n = 3 it is barely even the first one.")
    d.notes(s,
           "This is the half of the room with no statistics course, so the "
           "answer goes on the wall.\n "
           "They meet the same distinction on PS8 Q3d, with Mishra's 432 "
           "against 396 at n = 3 and p = 0.10. Same words both times.\n "
           "What I am NOT saying: that Aoki are wrong. The circuit very "
           "probably does reject the perturbation. The claim that outruns the "
           "data is 'perfectly', and nothing at n = 3 could establish it.")

    s = d.light()
    d.header(s, "segment 5", "debrief  ·  their figure")
    d.title(s, "Closed loop against open loop, across seven degrees")
    d.paper_figure(s, "aoki2019_fig3d", M, 1.72, W - 2 * M, 3.95,
                   "Aoki et al. 2019, Fig. 3d",
                   "growth rate normalised to each circuit's own 37 °C rate, n = 3; "
                   "two-tailed unpaired Welch t-test",
                   show_caption=True)
    d.notes(s,
           "Start on the LEFT half, not the bars: the control system wraps "
           "around araC/metE and the arrow coming out of it is cell growth. "
           "The loop closes through the growth rate. That is the picture for "
           "everything said on the last surface.\n "
           "Then the two bars and the two p-values. The closed loop's "
           "normalised growth rate is statistically indistinguishable across "
           "the temperature change; the open loop's is not, by three and a half "
           "magnitude.\n "
           "Then say the honest version: this is good evidence that the "
           "controller rejects the perturbation, and it is not proof of "
           "perfect adaptation. Nothing at n = 3 could be.")


# ------------------------------------------------------------------- leak ---
def _leak(d):
    s = d.light()
    d.header(s, "segment 6", "frame  ·  what the derivation assumed")
    d.title(s, "An integrator is not allowed to forget")
    d.rows(s, [
        ("we assumed", "Z₁ and Z₂ are lost ONLY by annihilating each other. "
                       "That is what makes Z₁ − Z₂ a perfect running total."),
        ("the paper says", "the ideal analysis assumed negligible degradation "
                           "of the controller proteins — and that in living "
                           "cells this fails, in the case of fast-growing "
                           "cells, by dilution."),
        ("so", "the cell grows. Z₁ and Z₂ are diluted along with everything "
               "else, the running total leaks away, and the guarantee stops "
               "being exact.", AMBER),
    ], top=2.00, label_color=TEAL)
    d.foot(s, "The integrator forgets at exactly the rate the cell divides.")
    d.notes(s,
           "I come back to the motif frame's aside here: anything "
           "that decays forgets, and a controller that forgets is not an "
           "integrator.\n "
           "Then the subtraction again, with the dilution term in it: "
           "mu − theta X = delta (Z1 − Z2). The error is no longer zero; it "
           "is proportional to delta.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  how much does it cost")
    d.title(s, "First order in the growth rate")
    d.image(s, FIG + "s22_leak.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "Slope one on log-log. Halve the growth rate and you halve the error — there is no threshold and no safe region.")
    d.notes(s,
           "Straight line, slope one, over two and a half decades. The error "
           "is first order in delta and PS8 Q5 asks them to get that exponent "
           "out of the algebra rather than off this plot.\n "
           "The sign matters and I say it: the output UNDERSHOOTS. The leak "
           "does not add noise around the set point, it moves the set point "
           "down.\n "
           "LEDGER: X_ss − mu/theta = −(delta/theta)(Z1 − Z2). First order in "
           "delta, and NEGATIVE — the minus is easy to drop and then the "
           "formula says overshoot while the plot says undershoot.\n "
           "And the arc: in session 19 the growth rate was the thing your "
           "circuit changed. Here it is the thing that degrades your "
           "circuit's guarantee. Rung 1 eating rung 4.")

    s = d.light()
    d.header(s, "segment 6", "release  ·  find the bound")
    d.title(s, "Where does it run out?")
    d.rows(s, [
        ("the constraint", "Z₁ is a molecule, so Z₁ ≥ 0. The controller can "
                           "only push the output UP."),
        ("your turn", "the disturbance is positive — something is making X "
                      "on its own. How large can d get before the controller "
                      "cannot hold the set point at all? Give it in terms of "
                      "γ, μ and θ."),
    ], top=2.05)
    d.foot(s, "At the set point, what does the plant still need from the controller — and what is the least the controller can supply?")
    d.notes(s,
           "Harder than the subtraction and worth the three minutes, because "
           "this is PS8 Q4c and they have had the set for five days.\n "
           "At the set point the plant needs k·Z1 = gamma·mu/theta − d, and "
           "Z1 cannot go below zero, so d <= gamma·mu/theta. With our numbers "
           "that is 2.5.\n "
           "The other sign is worth a sentence if it comes up: a disturbance "
           "REMOVING X is one the controller simply makes more Z1 against, "
           "and on that side there is no bound at all. The controller pushes "
           "one way, so only the direction it cannot push is limited.\n "
           "Then show them what happens past it, because this is the trap: "
           "Z1 goes to zero, the annihilation STOPS, and Z2 grows without "
           "bound. X itself SETTLES, at d/gamma, stably and in the wrong place — "
           "the runaway is Z2 alone, which is why Q4c watches Z2 and not "
           "X. There is no steady state. A "
           "simulation that stops at one horizon reports one anyway.\n "
           "LEDGER: d <= gamma·mu/theta — the actuator bound.")

    s = d.dark()
    d.header(s, "segment 6", "debrief  ·  four ways it breaks, not one")
    d.title(s, "Running out is not the same as leaking")
    d.rows(s, [
        ("the leak", "dilution. There IS a steady state and it is in the "
                     "wrong place, by an amount first order in the growth "
                     "rate.", CYAN),
        ("saturation", "the bound you just derived. Past d = γ·μ/θ there is "
                       "no steady state AT ALL — Z₁ hits zero, the "
                       "annihilation flux pins at μ, and Z₂ climbs for ever "
                       "at θX − μ.", AMBER),
        ("why those two matter", "they look alike in a simulation that stops "
                                 "too early. One is fixed by diluting less; "
                                 "the other by a bigger actuator, and nothing "
                                 "else will do."),
        ("two more, theirs", "STABILITY — a loop that oscillates has no "
                             "steady state to be exact about. VARIANCE — they "
                             "report the closed loop MORE variable cell to "
                             "cell. The mean is pinned; the spread is not."),
    ], label_color=CYAN)
    d.foot(s, "Integral feedback rejects any disturbance it has the authority to reject. That sentence needs both halves.")
    d.notes(s,
           "I put the overstatement on the board and then break it: 'integral "
           "feedback rejects any disturbance' is what they will remember "
           "unless I stop them.\n "
           "The saturation case is the one that looks convergent and is not. "
           "Z2 climbs linearly forever while X drifts toward d/gamma, so a "
           "simulation that stops at one horizon reports a steady state that "
           "does not exist. PS8 Q4c makes them check two horizons for exactly "
           "this reason.\n "
           "LEDGER: leak = wrong place. Saturation = no place.")


# ------------------------------------------------------------------ close ---
def _close(d):
    s = d.dark()
    d.header(s, "close", "the design ledger")
    d.title(s, "What you can now do, and what it costs")
    d.rows(s, [
        ("knobs", "μ — Aoki turn it with HSL, onto the sigW promoter. θ — "
                  "with arabinose, onto rsiW. The set point is the RATIO, so "
                  "anything hitting both equally is rejected too.", CYAN),
        ("constraints", "δ is the growth rate and belongs to the host, not "
                        "to you. k and γ belong to the plant. η belongs to "
                        "the protein pair you picked. None of them is a dial."),
        ("guarantee", "exact adaptation to any constant disturbance, whatever "
                      "the plant — while the loop is stable and the "
                      "controller is lost only to itself."),
        ("limits, and the tell", "actuator: Z₁ pins at zero. Dilution: the "
                                "error tracks the growth rate. Stability: it "
                                "rings and never settles.", AMBER),
    ], top=1.88, label_color=CYAN)
    d.foot(s, "Aoki's own design rule for the leak: pick controller species whose only loss channel IS dilution. σ factors are stable; RNA is not.")
    d.notes(s,
           "The surface I want photographed, and it is four columns now "
           "because the constraints row is the one this session can fill "
           "better than any other in Part II.\n "
           "KNOBS have to be physical or they are not knobs. HSL and "
           "arabinose, both in their Fig. 2c, and the set point is mu/theta "
           "so what matters is the ratio — which is also why a global insult "
           "that scales both is rejected without anyone designing for it.\n "
           "The foot line is the engineering answer to the leak, and it is "
           "the paper's own: the high native stability of these sigma and "
           "anti-sigma factors is what makes integral action practical in "
           "fast-growing cells, in contrast to RNA-based controllers where "
           "instability is a major limitation. So the fix is not 'dilute "
           "less', which they cannot do. It is a PART CHOICE.\n "
           "LIMITS each come with the observable, because a limit you cannot "
           "see from the bench is not a limit you can design around.")

    s = d.light()
    d.header(s, "close", "two threads, both ending here")
    d.title(s, "Part II ends here")
    d.rows(s, [
        ("19 → 22", "burden, stoichiometry, retroactivity, control. One "
                    "mechanism underneath three of them, and the fourth is "
                    "built out of it.", CYAN),
        ("10 → 22", "the older thread. A feedforward loop that forgot 38% of "
                    "a step, against a feedback loop that forgets all of it. "
                    "Approximate adaptation needs the right parameters. Exact "
                    "adaptation needs the right topology."),
    ], top=2.05)
    d.foot(s, "Session 10 asked whether a circuit can ignore a step. This answer is exact, and holds only while the controller species are lost to each other and the actuator has range left.")
    d.notes(s,
           "I close Part II explicitly, and on two threads rather than one.\n "
           "The rungs are the thread they expect. The s10 one is the thread "
           "that has been open since the middle of Part I, and 0.62 against "
           "zero is the whole distance between a motif that fights a step and "
           "a motif that integrates it.\n "
           "Say the last line slowly. Topology, not parameters. That is the "
           "difference between the two devices and it is the sentence Part III "
           "opens on.")

    s = d.light()
    d.header(s, "close", "notes down — the three from the start")
    d.title(s, "Can you answer these now?")
    d.rows(s, [
        ("the guarantee", "what is the set point allowed to depend on, and "
                          "what is it not?"),
        ("the device", "two molecules that destroy each other. Why is that an "
                       "integrator, and why does the circuit being controlled "
                       "not get a vote?"),
        ("the limit", "name the ways a real cell breaks it. There were four."),
    ], top=2.05)
    d.foot(s, "If the third one is hard, that is the honest state of this material and not a gap in your notes.")
    d.notes(s,
           "Notes closed, and I take these from the room rather than reading "
           "them out. Three minutes, and it is the only measurement I get of "
           "whether the hour landed.\n "
           "One: μ and θ, and nothing else — not k, not γ, not d.\n "
           "Two: because Z1 − Z2 is the running total of the error and a "
           "steady state forces that total to stop changing, which forces the "
           "error to zero. The plant never enters.\n "
           "Three: actuator range, dilution, stability, variance. If they get "
           "two I am content; if they get the first two I am content, because "
           "those are the two PS8 asks about.")

    s = d.light()
    d.header(s, "close", "where this goes")
    d.title(s, "Before Thursday")
    d.rows(s, [
        ("Thursday", "Part III opens. Design at a scale where the thing you "
                     "build is supposed to spread."),
        ("PS8", "due 19 November. Q4 and Q5 are this session — and Q4c is the "
                "saturation trap we just took apart."),
    ], top=2.05)
    d.assignment(s, y=4.20)
    d.notes(s,
           "Point at PS8 Q4c. They have had the set for five days and that "
           "question has been sitting there looking like a bug in their "
           "integrator. Now they know it is not a bug.\n "
           "Q5 is the leak, and the set calls it the SET-POINT error, not the "
           "adaptation error — because session 10 already owns that name for "
           "final over peak. The note is in the question. Say it out loud "
           "anyway.")
