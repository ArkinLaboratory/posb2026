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
  * NOT YET TRUE, and recorded here rather than asserted away: "plant",
    "actuator", "set point", "error" and "integral feedback" are used on
    surfaces without ever being defined on one. That is the next rebuild.

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
        ("the limit", "The guarantee is exact. Name the two different ways a "
                      "real cell breaks it."),
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
def _derivation(d):
    d.derivation(
        None, "segment 2", "build  ·  integral feedback, on no particular plant",
        "Zero error is the only place it can rest",
        [
            ("a plant, any plant",
             "dX/dt = f(X, u) + d",
             "f unknown, d unknown and constant"),
            ("the controller integrates",
             "du/dt = mu - theta·X",
             "and nothing else"),
            ("at steady state du/dt = 0",
             "mu - theta·X = 0",
             "whatever f was doing"),
            ("so the output is",
             "X = mu / theta",
             "two constants, and no f anywhere"),
        ],
        board="du/dt = mu - theta X   =>   X_ss = mu/theta",
        note="AT THE BOX, SAY IT AGAINST SESSION 10. Their feedforward loop "
             "adapted too, and its adaptation error was 0.62 — final over "
             "peak — and it moved whenever any rate constant moved. This one "
             "is ZERO, and there is no rate constant in it to move. Same "
             "goal, and the difference between a motif that fights the step "
             "and a motif that integrates it.\n "
             "Four lines, on a plant I deliberately refuse to specify. The "
             "generality IS the result and specifying the plant would throw it "
             "away.\n "
             "Linger on step three. du/dt = 0 is forced at ANY steady state — "
             "it is what steady state means — so the error has to be zero. "
             "Not small. Zero.\n "
             "LEDGER, left wing: X_ss = mu/theta, and f is not in it.\n "
             "Aoki's own sentence is worth reading out here: the steady state "
             "is determined solely by the ratio mu/theta, and it does not "
             "depend on the topology and parameters of the controlled "
             "network. That is what we just derived, and the next surface "
             "makes them check it.")


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
    d.header(s, "segment 4", "release  ·  two lines of algebra")
    d.title(s, "Subtract them")
    d.rows(s, [
        ("on the board", "dZ₁/dt = μ − η·Z₁Z₂      dZ₂/dt = θ·X − η·Z₁Z₂"),
        ("your turn", "subtract the second from the first. Then look at what "
                      "you have and say which quantity in this circuit is the "
                      "integral of the error."),
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
    d.header(s, "segment 5", "frame  ·  somebody built it")
    d.title(s, "And controlled the one thing Part II opened on")
    d.rows(s, [
        ("the controller", "SigW and RsiW — a σ factor and its anti-σ factor "
                           "from B. subtilis, moved into E. coli. The "
                           "annihilation is their natural interaction."),
        ("the output", "not GFP. They replace sfgfp with metE, the last "
                       "step of cobalamin-independent methionine biosynthesis, in "
                       "a ΔmetE host in "
                       "methionine-free medium — so the controlled output is "
                       "the cell's GROWTH RATE."),
        ("the control", "the open-loop strain is the same circuit with the "
                        "anti-σ module deleted. One module out, feedback "
                        "gone, everything else identical.", CYAN),
    ], top=1.95, label_color=CYAN)
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
    d.header(s, "segment 6", "debrief  ·  two failures, not one")
    d.title(s, "Running out of authority is not the same as leaking")
    d.rows(s, [
        ("the leak", "dilution. There IS a steady state and it is in the "
                     "wrong place, by an amount first order in the growth "
                     "rate.", CYAN),
        ("saturation", "the bound you just derived. Past d = γ·μ/θ there is "
                       "no steady state AT ALL — Z₁ hits zero, the annihilation "
                       "stops, and Z₂ grows without bound.", AMBER),
        ("why it matters", "they look alike in a simulation that stops too "
                           "early. One is fixed by diluting less; the other "
                           "is fixed by a bigger actuator, and nothing else "
                           "will do."),
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
        ("the knobs", "μ and θ, and that is the whole list. The set point is "
                      "a ratio of two rate constants you choose.", CYAN),
        ("the guarantee", "exact adaptation to any constant disturbance, "
                          "whatever the plant is — provided the controller "
                          "species are lost only to each other."),
        ("the limits", "the actuator's range; a stable closed loop, which "
                       "is Aoki's own proviso; and dilution. The last is not "
                       "avoidable in a growing cell.", AMBER),
        ("the pattern", "every cure in Part II has cost something on a "
                        "different axis from the damage. This one costs you "
                        "the assumption that your controller does not "
                        "dilute."),
    ], label_color=CYAN)
    d.foot(s, "Four rungs, four couplings, and the last device is made of the first problem.")
    d.notes(s,
           "This is the ledger surface and it is the one I want "
           "photographed.\n "
           "The limits row is the one that must not be skipped — "
           "lecture-design says so and this is the session with the most "
           "seductive guarantee in the course.\n "
           "The last row is Part II's whole shape: session 17 said a "
           "parameter is manufactured, 21 said the load is the price of the "
           "regulation, and today says the guarantee is the price of not "
           "diluting. Nothing is free and the bill always arrives somewhere "
           "you were not looking.")

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
