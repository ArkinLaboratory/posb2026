"""Session 22 — Robustness and control: rejecting the disturbance instead of
modeling it.

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

AND "ANY PLANT" IS NOT WHAT THEY CLAIM. Aoki's Box 1 does not hand the result
to an arbitrary network; it hands it to an arbitrary network WIRED A
PARTICULAR WAY. The controller reaches the network through actuation
reactions -- Fig. 1c: "Z1 works as an actuator by affecting processes that
lead to the increase in the production of the output of interest" -- and the
network reaches the controller through a sensing reaction "which is catalysed
by the output species of interest XL". Then stability. A plant whose output
the actuator cannot move has no integral action to speak of, however many
question-marked nodes are drawn inside it: Z1 - Z2 runs away instead of
resting, so there is no stable closed loop for the clause to be true of.

SO THE DECK SAYS, IN THE ROOM'S OWN WORDS, ANY PLANT THE CONTROLLER CAN MOVE
AND CAN SEE. "Actuator" and "sensor" are both defined on the five-words
surface, where the loop diagram names them on the arrow and the box that are
those things, so the condition costs no new vocabulary. State-space words --
reachable, controllable, observable -- are deliberately NOT used: linear
algebra is this cohort's weak axis, and a term introduced to carry a
condition has to be defined where it first appears, which would cost a
surface the hour does not have.

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
    are now DEFINED on a slide, on the block diagram at the top of
    segment 2, before any algebra uses them. They were not, in the first
    build, and the docstring claimed they were -- which is how it went
    unnoticed. The error is also written down as a derivation step now
    (e = r - X), because the hour is about driving it to zero and no slide
    had ever said what it was. The run is written in r and a gain G
    throughout: mu and theta are the MOTIF's two rate constants, they are
    produced by the subtraction, and nothing before that subtraction is
    allowed to spend them.

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
    d.text(s, "The controller sets the output level and holds it",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    # THE CLAIM, WITH ITS CONDITION, FROM THE FIRST SURFACE. This read "the
    # circuit being controlled cannot move it", which is false of a circuit
    # the controller cannot act on: there the level is not held at all, so
    # nothing is being claimed about where it sits. The condition is two
    # plain verbs and needs no vocabulary the room has not got -- the words
    # "actuator" and "sensor" arrive on the five-words surface and the
    # ledger uses them there.
    d.text(s, "Two rate constants in the controller fix that level. A "
              "circuit the controller can move and can see gets no vote on "
              "it, and neither does a disturbance nobody told you about.",
           M, 4.42, 8.6, 1.70, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.45, 9.0, 0.4, size=13, color=SILVER)
    d.notes(s,
           "Sessions 19, 20 and 21 each cured one named disturbance. "
           "Today's device does not need the name."
           "\n The set point depends on two numbers in the controller, "
           "and on nothing in the circuit being controlled — in any "
           "circuit the controller can move and can see. The condition "
           "goes with the claim every time I say it, starting here."
           "\n It works by sequestration — the disease since session 18. "
           "I do not say that yet. It lands on the sequestration slide.")


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
        ("3", "Each of those sessions built a defense, and you had to name "
              "the disturbance before you could build it. What was the "
              "disturbance in each case?"),
        ("4", "Session 10: step the input to an incoherent feedforward "
              "loop and the output spikes, then falls back part of the way. "
              "What did we call the number that says how far it came back, "
              "and what did that number depend on?"),
    ], top=2.05, label_w=0.7)
    d.notes(s,
           "One and two are retrieval. Three and four set up the hour."
           "\n One: growth rate falls, gamma falls, response time goes "
           "up for everything in the cell. gamma is session 5's removal "
           "rate, dilution plus degradation."
           "\n Two: the load cost speed, and level too if the complex "
           "dilutes. They could not lower it; the bill is the number of "
           "binding sites."
           "\n Three: burden was competition for ribosomes, the load "
           "driver one interface. Every cure so far needs the "
           "disturbance named first."
           "\n Four: adaptation error = final / peak = 0.6193. They saw "
           "it in session 10 and computed it on PS5 Q3a."
           "\n Peak 1.0989, final 0.6806 — so the loop gave back 38 per "
           "cent of its peak and kept the rest. Change the motif's "
           "parameters and that number changes with them: K_yz from 0.25 "
           "to 1 takes it from 0.50 to 0.83. Not every constant — beta_z "
           "cancels out of final over peak and moves it not at all."
           "\n So they have built a circuit that partly forgets a step. "
           "Today: can adaptation be exact, and free of the parameters.")


def _goals(d):
    s = d.light()
    d.header(s, "open", "what you should be able to do by the end")
    d.title(s, "Three questions")
    d.rows(s, [
        ("what the set point can depend on",
         "A controller holds the output of the circuit it controls at a "
         "fixed level. What is that level allowed to depend on, and what is "
         "it not allowed to depend on?"),
        ("why two molecules are enough",
         "Two molecules that destroy each other on meeting. Why does that "
         "arrangement keep a running total of how far off the output is, "
         "and why does the circuit being controlled not get a vote?"),
        ("what breaks it in a real cell",
         "On paper the output sits exactly on the set point. Name the ways "
         "a living cell misses it. There are more than two."),
    ], top=2.05)
    d.notes(s,
           "I answer all three now, briefly."
           "\n Guarantee: the set point depends on two constants inside "
           "the controller — the rate it makes its own molecule at, and "
           "how hard it senses the output. Nothing from the plant. The "
           "symbols for those two arrive in the derivation."
           "\n Device: two molecules that destroy each other, so the "
           "difference between them is the running total of the error."
           "\n Limit: four answers — actuator range, dilution, "
           "stability, variance. PS8 asks about the first two.")


# ------------------------------------------------------------------ frame ---
def _frame(d):
    s = d.light()
    d.header(s, "segment 1", "frame  ·  three patches, and what each one needed")
    d.title(s, "What would it take to stop patching?")
    d.text(s, "Patching means naming what will go wrong, then building a "
              "fix for that one thing.",
           M, 1.56, W - 2 * M, 0.40, size=20, color=INK)
    d.image(s, FIG + "s22_patch_vs_feedback.png", M, 2.02, w=W - 2 * M,
            h=4.60)
    d.foot(s, "Feedback needs no list of disturbances. Its own costs are the last third of today.")
    d.notes(s,
           "I walk the three lanes one at a time, then the empty one.\n "
           "Rungs 1 to 3 are sessions 19, 20 and 21. Today is rung 4.\n "
           "All three are feedforward: model the disturbance, then build "
           "against the model. Wrong model or short list, wrong cure.\n "
           "Session 20 is the sharp one. The flux calculation was exact, and "
           "it still made you supply an objective from outside. Being exact "
           "did not save you from having to name something.\n "
           "The fourth lane: no session behind it, no device in the slot, and "
           "it reaches the circuit anyway.\n "
           "f is the plant's own dynamics and it is unknown, so a CHANGE in f "
           "is a disturbance too — a different rate constant, a different "
           "temperature, a protease nobody planned for. That is why a longer "
           "list is not the answer.\n "
           "The answer to the title question, which I hold until the "
           "derivation: a controller that integrates the error. It never "
           "needs the list.")


# ------------------------------------------------------------- derivation ---
def _vocabulary(d):
    s = d.light()
    d.header(s, "segment 2", "frame  ·  five words, before any algebra")
    d.title(s, "The words this hour is made of")
    d.image(s, FIG + "s22_block_diagram.png", M, 1.60, w=W - 2 * M, h=5.05)
    d.foot(s, "\"Plant\" is the control engineer's word for whatever you are controlling. It is not a metaphor and it has nothing to do with botany.")
    d.notes(s,
           "All five words get defined here, before any algebra uses "
           "them."
           "\n PLANT: the thing being controlled — your circuit, the "
           "cell, whatever sits downstream of the actuator."
           "\n The sentence I say: plant is the control engineer's word "
           "for whatever you are controlling. It is not a metaphor and "
           "it has nothing to do with botany."
           "\n ERROR: e = r − X. r is the set point coming in, X the "
           "measured output. The sensor in this diagram is unity gain, "
           "so the subtraction is honest as written."
           "\n The hour drives e to zero, and no slide has written the "
           "error down before now. What sets r in our own circuit comes "
           "out of the derivation."
           "\n ACTUATOR: what the controller pushes with. Here a "
           "molecule — and a molecule cannot go below zero, which is the "
           "second half of the hour."
           "\n CLOSED and OPEN: closed when the sensor reports back. "
           "Aoki's control strain is this diagram with that arrow cut. I "
           "point at the arrow now.")


def _derivation(d):
    d.derivation(
        None, "segment 2", "build  ·  integral feedback, on no particular plant",
        "Zero error is the only place the loop can rest",
        # GENERIC SYMBOLS, BECAUSE THIS IS THE GENERIC RESULT. The set point
        # is r -- the same r the block diagram one click earlier defines and
        # glosses -- and the controller's gain on the error is G, defined on
        # the step that first writes it. Nothing in this run is specific to
        # the molecules, because the molecules are twelve slides away and the
        # run's whole claim is that it does not need to know what they are.
        #
        # MU AND THETA ARE NOT HERE, and that is the point of this rebuild.
        # They are the antithetic motif's own two rate constants; they are
        # PRODUCED by subtracting its two rate laws, and until that happens
        # they have no origin a student can point at. Writing them here spent
        # them fifteen slides early and made the set point look like a given
        # rather than a result.
        #
        # EVERY SYMBOL IS DEFINED WHERE IT FIRST APPEARS, in the run and not
        # in the note: f, X, u and d on step one, e and the set point r on
        # step two, the gain G on step three.
        # "f unknown" said what f's STATUS was and never what f IS, and a
        # student who cannot say what f is cannot follow a derivation whose
        # whole point is that f drops out.
        #
        # AND EACH LINE SAYS WHERE IT LIVES ON THE LOOP DIAGRAM. The step
        # labels are the names of the things the room looked at one click
        # earlier -- the plant box, the summing junction, the controller box,
        # the output arrow -- so the algebra and the picture are visibly the
        # same object. Step two carries the sentence the review found missing
        # outright: the X being subtracted is the plant's own output coming
        # back through the unity-gain sensor, not a second quantity that
        # happens to share a letter.
        #
        # The three columns are capped by the theme's own arithmetic: 28
        # characters for a label, 56 for an equation, 56 for an aside, all at
        # the 20 pt floor. Five steps with no closing box is the one geometry
        # that keeps an aside on EVERY step of the last slide -- pitch 0.90
        # against the 0.86 the asides need -- and the last slide is the
        # artifact a revising student reads.
        [
            ("the plant box, unopened",
             "dX/dt = f(X, u) + d,   d constant",
             "f the plant's chemistry, X out, u in, d disturbance"),
            ("the error, at the junction",
             "e = r − X   ·   r is the set point",
             "this X is the plant's output, back through the sensor"),
            ("the controller box",
             "du/dt = G·e   ·   G > 0 is the gain on the error",
             "u is the running total of e — that is the integral"),
            ("at steady state, du/dt = 0",
             "G·e = 0,  and G > 0,  so e = 0",
             "zero, not small — whatever f was doing"),
            ("the output arrow, at rest",
             "X = r, as long as the loop is stable",
             "session 10 adapted partly: 0.62. this one exactly: 0"),
        ],
        board="e = r - X;  du/dt = G·e   =>   X_{ss} = r",
        note="Five lines, on a plant I refuse to specify. The generality "
             "is the result."
             "\n Session 10 for contrast: their feedforward loop adapted "
             "too, adaptation error final over peak = 0.6193 — they saw "
             "it in session 10 and computed it on PS5 Q3a — and it moves "
             "when the motif's parameters move."
             "\n This one is zero, and there is no rate constant in it "
             "to move."
             "\n Step two: e = r − X, the same error the block diagram "
             "defines. r is the set point the controller carries in, X "
             "the output coming back."
             "\n Step three: du/dt = G·e makes u the running total of "
             "the error — that is the integral in the name. G is the "
             "controller's gain on the error, and all the result asks of "
             "it is that it be positive."
             "\n Step four: du/dt = 0 at any steady state — that is what "
             "steady state means — so G·e = 0, and G is not zero, so "
             "the error has to be zero. Not small. Zero."
             "\n X_ss = r, and f is nowhere in it."
             "\n If someone asks what sets r: hold them. It is two rate "
             "constants of the controller, and they do not exist yet — "
             "they come out of the molecules when we build them. I do not "
             "name them here."
             "\n The consequence: you never characterize your plant. "
             "Change host, promoter, chassis — the controller ports "
             "without re-tuning, because none of them is in the answer.")

    # THE COMPARISON THE HOUR IS FOR, ON A SLIDE. The retrieval slide at the
    # top of the hour asks the room for session 10's adaptation error and
    # until now the answer lived only in a speaker note, so the question was
    # posed and never answered on screen. By this deck's own standard that
    # means it was not in the deck.
    #
    # It lands here, on the click after X = r, because the contrast is what
    # makes the result mean anything: the room has already built a circuit
    # that partly forgets a step and has measured how badly. The number and
    # the reason are both drawn -- move a rate constant of the feedforward
    # motif and 0.6193 moves with it; there is no plant constant in X = r
    # for the plant to move.
    #
    # AND THE FEEDFORWARD LOOP IS DRAWN ON IT. The review: "Slide 11 comes
    # from nowhere. What is the system?" The panel plotted session 10's
    # incoherent feedforward loop against today's flat zero and never showed
    # the loop, so the subject of half the figure was twelve sessions back
    # and invisible. The topology is now on the same surface, named by role
    # -- input, repressor, output -- so the comparison can be read by
    # somebody who has forgotten session 10 entirely.
    s = d.light()
    d.header(s, "segment 2", "debrief  ·  the number from the top of the hour")
    d.title(s, "Session 10 kept 0.62 of the step. This keeps none.")
    d.image(s, FIG + "s22_partial_vs_exact.png", M, 1.62, w=W - 2 * M, h=4.95)
    d.foot(s, "Zero is what the ideal analysis gives. The last third of the hour is the ways a real cell misses it.")
    d.notes(s,
           "This answers question four from the start of the hour."
           "\n Adaptation error, final over peak, 0.6193. Peak 1.0989, "
           "final 0.6806. They computed it on PS5 Q3a."
           "\n The orange and red lines are the same feedforward motif "
           "with K_yz scaled and with B_y scaled. The number slides from "
           "about 0.50 to about 0.83. It is a property of the motif's "
           "rate constants, so it moves when they move."
           "\n The flat line is today's controller with the plant's gain "
           "and removal rate scaled over the same range. Zero at every "
           "point, because X = r has no plant constant in it."
           "\n One honest caveat, and I say it here rather than later: "
           "that zero is the ideal analysis. Nothing dilutes, and the "
           "controller has as much room to push as it needs. Both of "
           "those fail in a cell, and that is the last third of the "
           "hour."
           "\n If someone asks why the two lines are not the same "
           "quantity: they are both the fraction of the step still "
           "there at the end, and session 10's final over peak is that "
           "fraction because the output starts at zero.")


def _instantiate(d):
    s = d.light()
    d.header(s, "segment 3", "release  ·  on paper")
    # THE TITLE. "Put a plant under it" is the wording the review struck
    # outright, and it survived this run because a different builder fixed a
    # different slide carrying the same phrase. A title makes one claim; this
    # slide's claim is the question the room is being asked, so that is what
    # it says now.
    #
    # AND THE PLANT IS WRITTEN DOWN, not cited. It used to read "session 5's
    # protein", seventeen sessions back, with no picture of it anywhere on
    # the surface -- so the exercise's first move was a memory test the
    # exercise does not care about. Every constant in the model is now
    # glossed on the slide in the order it appears, and no session number is
    # needed to read it.
    d.title(s, "Where does this one settle?")
    d.rows(s, [
        ("the plant", "one protein, and nothing clever. The controller makes "
                      "it at rate k per unit of u, it is removed at rate γ, "
                      "and a disturbance d adds to its production:"),
        ("the model", "dX/dt = k·u − γX + d", CYAN),
        ("your turn", "write down where the output settles. Then say which of "
                      "k, γ, d, r and G it is allowed to depend on."),
    ])
    # "on the last slide" was a slide referred to by position, which the bar
    # does not allow anywhere. The derivation has a name; use it.
    d.foot(s, "Two minutes. You need the steady state, not the dynamics — the derivation already gave it to you.")
    d.notes(s,
           "Short, because the answer does not need the plant at all."
           "\n X = r. The set point and nothing else — not k, not "
           "gamma, not d."
           "\n Push-back to expect: 'k and gamma must do something.' "
           "They do — how fast it gets there and how long it rings. Not "
           "where it ends up.")

    s = d.dark()
    d.header(s, "segment 3", "debrief  ·  where it settles")
    d.title(s, "X = r")
    d.rows(s, [
        ("what is in it", "the set point, and nothing else. r is a number "
                          "the controller carries; the plant never sees it.",
         CYAN),
        ("what is not", "k. γ. d. Not one of them survives into the answer, "
                        "and you did not need to know any of them."),
        ("what k and γ do", "they set the ride — how fast it gets there, how "
                            "much it rings on the way. They do not set the "
                            "destination."),
    ], label_color=CYAN)
    d.foot(s, "Everything for the rest of the hour is this box, or a reason it fails.")
    d.notes(s,
           "The answer: X = r. The set point, and nothing else."
           "\n Dropped out: k, gamma, d. They never needed to know any "
           "of them."
           "\n What r is made of is still open, and I say so: it is two "
           "rate constants of the controller and we have not built the "
           "controller yet."
           "\n k and gamma set the ride — how fast, how much it rings. "
           "Not the destination. That is what the next run shows."
           "\n If someone asks whether d really drops out: it does, and "
           "the step figure is next.")

    # TWO MOVES, NOT ONE. Note 13: "complex slide with no build. It is ok but
    # the text makes the figure hard to take in and the fonts are all small."
    # The open loop takes the step alone; only then does the closed loop
    # arrive, on the same axes with the same limits, so the frame does not
    # jump and the only thing that changes under the click is the curve the
    # room is being asked to look at.
    #
    # THE TEXT he could not take in was the figure's own two-line claim block
    # -- which was this slide's foot, repeated word for word INSIDE the axes.
    # Prose on a slide beside the same prose spoken is verbal redundancy;
    # prose laid over a figure collapses the signaling benefit to g = 0.06
    # (docs/lecture-design.md 5). Both copies cannot be right and the one
    # that goes is the one sitting in the data. The figure now carries four
    # direct labels and no key.
    #
    # THE FONTS followed from geometry, not from authoring. Nothing was below
    # the floor: the old PNG saved 4.80in tall and d.image(h=5.05) placed it
    # at 1.052, so 20pt authored landed at 21 -- at the floor and not a point
    # over it. These save at 4.40in and place at 1.148, so body type lands at
    # 23 and the two labels that have to carry to row 8 land at 27.5. Those
    # are measured off the saved PNGs, not off figure_fit's bbox, which
    # excludes savefig's 0.1in pad per side and runs about 2% optimistic.
    #
    # The note goes on the LAST slide of the run only -- Deck.derivation's
    # own rule, because a note on an intermediate step is read out before the
    # thing it describes is on the wall.
    for png, foot in (
            ("s22_step_1.png",
             "The step arrives at t = 40 and the output goes up by d/γ. "
             "Nothing in an open loop brings it back."),
            ("s22_step.png",
             "Same plant, same step. The open loop keeps the hit; the closed "
             "loop gives it back, and the gap at the tail is zero."),
    ):
        s = d.light()
        d.header(s, "segment 3", "build  ·  send a disturbance in")
        d.title(s, "Closing the loop gives the disturbance back")
        d.image(s, FIG + png, M, 1.62, w=W - 2 * M, h=5.05)
        d.foot(s, foot)
    d.notes(s,
           "A step disturbance arrives and the two circuits do different "
           "things with it."
           "\n Open loop: steps up and stays up, at the old level plus "
           "d/gamma. Session 5's answer, because without feedback that "
           "is all this is."
           "\n Closed loop: moves, then comes all the way back. I point "
           "at the tail — the gap is zero, not small."
           "\n Ideal controller, no dilution. The leak segment takes "
           "that away.")

    # FOUR MOVES, ONE CHANGED CONSTANT EACH. Note 14: "too many curves linked
    # to too many parameters. We need to step through these slowly and with
    # explanation", and bar rule C3 -- a comparison of several curves to
    # several parameters is taken one at a time. The reference run is
    # established first and stays on every frame; each click adds exactly one
    # changed constant, names it beside a sample of its own curve, and
    # restates the steady state computed for that run underneath. The
    # headline changes four times. The number under it does not, and that is
    # the claim.
    #
    # WHOSE CONSTANT IT IS, now said out loud. k and gamma are the plant's;
    # eta is the controller's. "Four different plants" filed all three under
    # the plant, which is a second and different claim made without saying
    # so, and the deck's own design ledger already separates them -- "k and
    # gamma belong to the plant. eta belongs to the protein pair you picked."
    # eta also makes its first appearance in this deck HERE, before the motif
    # segment builds the molecules it belongs to, so the last foot defines it
    # rather than leaving the room to meet a symbol it has not been given.
    #
    # THE THREE MULTIPLIERS the old foot carried -- gain quadrupled, removal
    # cut fivefold, annihilation ten times faster -- are each correct, against
    # NUMBERS.md section 2 and against posb.control. They are now printed as
    # before-and-after values on the figure, one per click, because a ratio
    # read out after the fact is exactly the thing the room could not follow.
    for png, foot in (
            ("s22_plant_does_not_matter_1.png",
             "The reference plant, and the level the controller holds it at. "
             "Each change from here moves one constant and nothing else."),
            ("s22_plant_does_not_matter_2.png",
             "Four times the plant gain. A different ride to the same place."),
            ("s22_plant_does_not_matter_3.png",
             "A fifth of the removal rate. It overshoots, it is still ringing "
             "at the right-hand edge, and it still lands on five."),
            ("s22_plant_does_not_matter.png",
             "η is a rate constant inside the controller, not in the plant — "
             "and it is not in the answer either."),
    ):
        s = d.light()
        d.header(s, "segment 3", "debrief  ·  and the computer agrees")
        d.title(s, "The ride changes and the destination does not")
        d.image(s, FIG + png, M, 1.62, w=W - 2 * M, h=5.05)
        d.foot(s, foot)
    d.notes(s,
           "One constant at a time, and the answer does not move. Four "
           "runs, steady state 5.0000000000 in every one. k and gamma "
           "are the plant's; eta is the controller's."
           "\n Orange is slower removal, gamma from 0.5 down to 0.1. It "
           "rings a long time and overshoots badly, and still lands on "
           "five."
           "\n A worse plant is a worse ride, not a worse destination."
           "\n Ideal controller, no dilution. I say that every time this "
           "plot goes up.")

    # THE CONSEQUENCE, which the demonstration above has never stated. Four
    # runs show changed constants and a destination that does not move, and
    # then the segment used to stop. What it MEANS is what keeps the turn of
    # the hour standing: the plant term f is never written down, so what is
    # covered is not only an unknown f but a CHANGED one.
    #
    # Without that, the obvious reply to the whole session is "then write a
    # longer list" -- and that reply is a good one. If an uncovered
    # disturbance were only something you forgot to enumerate, better
    # enumeration really would be the honest remedy. It stops being the
    # remedy at the point where the disturbance could not have been on any
    # list, because it did not exist when the list was written.
    #
    # This is the right surface for it because the figures above have just
    # changed plant constants in front of the room, so the student watches it
    # happen instead of being asked to accept it.
    #
    # STATED WITH ITS CONDITIONS OR NOT AT ALL. Aoki's sentence carries "as
    # long as the closed dynamics are stable", the derivation assumed d
    # constant, and the actuator has finite range. A change in f large enough
    # to destabilize the loop is emphatically not covered by anything here --
    # the last third of the session is those failures. The design ledger at
    # the close already says this in these terms; this slide must not claim
    # more than that one does.
    s = d.dark()
    d.header(s, "segment 3", "debrief  ·  what was never written down")
    d.title(s, "A change in the plant is a disturbance too")
    d.rows(s, [
        ("what moved", "k and γ are the plant's own constants: together they "
                       "are f. η is the controller's. Three constants moved, "
                       "one at a time, and the destination moved in none of "
                       "them.", CYAN),
        ("so f may change", "f is not merely unknown, it is free to move. A "
                            "different temperature, a different host, a "
                            "protease nobody planned for. The controller was "
                            "never told what f is."),
        ("the obvious reply", "\"then write a longer list.\" That is the "
                              "honest fix for a disturbance you forgot. A "
                              "disturbance that did not exist when you "
                              "designed the circuit was on no list, however "
                              "long."),
        # NO AUTHOR NAMED HERE. The clause is theirs and it must survive, but
        # the deck has not introduced the paper yet -- bar rule B4, and note
        # 19 in person. So the condition is stated and the paper is credited
        # where it is introduced, which is where a citation means something.
        ("what is not covered", "a plant the controller cannot move or "
                                "cannot see. And a change in f big enough to "
                                "make the loop unstable, or to run the "
                                "actuator out of range. The result carries a "
                                "clause: it holds only while the closed "
                                "dynamics are stable.",
         AMBER),
    ], top=1.88, label_color=CYAN)
    d.foot(s, "Feedback needs no list of disturbances. It does need a plant the controller can move and can see, a stable loop, an actuator with range left, and the constant d the derivation assumed.")
    d.notes(s,
           "This is the slide that answers 'then just write a longer "
           "list'."
           "\n f is the plant's own dynamics and it was never written "
           "down. So the controller does not care that f is unknown, and "
           "it does not care that f CHANGES."
           "\n A different temperature. A different host. A protease "
           "nobody planned for. They just watched three constants move "
           "and the answer sit still."
           "\n That is the part a longer list cannot buy. A disturbance "
           "that did not exist when you designed the circuit was on "
           "nobody's list, however long the list was."
           "\n And the condition, in the same breath, every time: this "
           "holds in a plant the controller can MOVE and can SEE, while "
           "the loop is stable and while Z1 has range left. The four "
           "runs on the wall are all plants it can move, so the run is "
           "honest and it is not the whole condition. "
           "Aoki's own sentence carries 'as long as the closed dynamics "
           "are stable' and I read it with the clause."
           "\n Also: d is constant in every line we have written. A "
           "disturbance that moves is a different question."
           "\n Both failures are the last third of today, so nobody "
           "leaves thinking this is free.")


# ------------------------------------------------------------------ motif ---
def _motif(d):
    s = d.light()
    d.header(s, "segment 4", "frame  ·  that integral has to be a molecule")
    d.title(s, "Nothing in a cell computes an integral")
    d.rows(s, [
        ("what we assumed", "du/dt = G·e, with e = r − X. Something in the "
                            "cell has to accumulate the error and remember "
                            "it."),
        ("what a cell has", "production, degradation, binding. No memory, no "
                            "arithmetic, no stored running total."),
        ("so the question is", "which arrangement of molecules has a quantity "
                               "that rises and falls exactly as the error "
                               "does, and forgets nothing?", CYAN),
    ], top=2.00, label_color=CYAN)
    d.notes(s,
           "du/dt = G·e needs something in the cell that accumulates "
           "the error and remembers it."
           "\n A cell has production, degradation and binding. No "
           "memory, no arithmetic. So the integral has to be an "
           "arrangement of molecules."
           "\n An integrator needs a quantity with no leak — anything "
           "that decays forgets, and a controller that forgets is not an "
           "integrator. I leave that half open; the leak segment comes "
           "back for it."
           "\n The answer to the question on the slide is two species "
           "that annihilate each other, and the difference between them "
           "is the running total. That is the next slide.")

    s = d.light()
    d.header(s, "segment 4", "frame  ·  the arrangement, before the algebra")
    d.title(s, "Two molecules that destroy each other")
    d.image(s, FIG + "s22_motif_topology.png", M, 1.62, w=W - 2 * M, h=5.05)
    # WHERE MU AND THETA FIRST APPEAR IN THE HOUR. The topology drawing
    # labels the two production arrows with them, so the foot glosses both in
    # words on the same surface: mu is a rate, theta is a rate per unit of
    # output, and the difference between those two kinds of number is what
    # makes their ratio a concentration.
    d.foot(s, "Z_{1} is made at the constant rate μ and drives the output. Z_{2} is made at rate θ per unit of output. They destroy each other.")
    d.notes(s,
           "Picture first, algebra after. The room has to see what Z1 "
           "and Z2 are before being asked to subtract rate equations."
           "\n Three strokes: Z1 made at the constant rate mu, Z2 made "
           "at theta times the output, the two annihilate at rate eta."
           "\n The plant is a box marked ANY TOPOLOGY, IF Z1 CAN MOVE "
           "X. I point at the arrows inside the box: five of them run "
           "from where Z1 arrives to the output node, and the sensor "
           "leg leaves from that same node. The nodes are unknown; the "
           "PATH is not, and the path is the condition."
           "\n The two arrows converge: one Z1 and one Z2 go in "
           "together. That symmetry is the whole trick, and it is worth "
           "saying why — because the term is then IDENTICAL in both rate "
           "equations, so it cancels the moment you subtract them. The "
           "home guide's item 2 is where they work out what that does "
           "and does not require of the chemistry."
           "\n The rate equations come on the next slide.")

    s = d.light()
    d.header(s, "segment 4", "release  ·  two lines of algebra")
    d.title(s, "Subtract them")
    d.rows(s, [
        ("on the board", "dZ_{1}/dt = μ − η·Z_{1}Z_{2}      dZ_{2}/dt = θ·X − η·Z_{1}Z_{2}"),
        ("the two rates", "μ is the rate Z_{1} is made at. θ is the rate per "
                          "unit of output that Z_{2} is made at. Both belong to "
                          "the controller."),
        ("your turn", "subtract the second from the first."),
        ("then vote", "which quantity in this circuit is the integral of the "
                      "error?    Z_{1}    ·    Z_{2}    ·    X    ·    Z_{1} − Z_{2}",
         AMBER),
    ], top=2.05)
    d.foot(s, "You are looking for something you derived twenty minutes ago.")
    d.notes(s,
           "I do not do this for them. Two lines of algebra."
           "\n The annihilation term is identical in both equations, so "
           "it cancels: d(Z1 − Z2)/dt = mu − theta·X. The controller we "
           "derived, with u = Z1 − Z2."
           "\n Nothing here measures anything. No comparator, no "
           "subtraction step. The chemistry subtracts for free, because "
           "one reaction consumes both species at the same rate."
           "\n Two quantities, kept apart. u = Z1 − Z2 INTEGRATES. The "
           "plant is driven by Z1 ALONE, and Z1 is the actuator — Aoki's "
           "own word."
           "\n    dX/dt = k·Z1 − gamma·X + d        the plant sees Z1"
           "\n    d(Z1 − Z2)/dt = mu − theta·X      the controller "
           "integrates"
           "\n The set point does not care which, because the integral "
           "is what forces the error to zero."
           "\n The actuator bound cares completely: Z1 ≥ 0, while Z1 − "
           "Z2 has no sign restriction at all. Written in u, the leak "
           "segment's bound is a bound on nothing."
           "\n The vote comes before anyone explains, and I record the "
           "split."
           "\n Z1 and Z2 both draw votes. Either one alone still carries "
           "the annihilation term, so neither is a clean running total. "
           "Only the difference cancels it."
           "\n The eta question: eta is not in the result at all. Its "
           "trace lies on the reference, and tenfold — 50 to 500 — moves "
           "the overshoot by two per cent and the peak itself by two "
           "tenths of one per cent. That is the answer."
           "\n What eta sets is how much controller protein you carry: "
           "Z2 at steady state is mu/(eta·Z1).")

    # WHERE THE SET POINT COMES FROM, AND IT IS HERE. The derivation ran on a
    # set point called r and a gain called G, and left both of them open on
    # purpose: a controller has to have them, and nothing about the generic
    # result says what they are made of. The subtraction the room has just
    # done answers it. The annihilation term is identical in the two rate
    # laws, so it cancels; what is left is mu - theta*X, which is theta
    # times (mu/theta - X); so r IS mu/theta and G IS theta, and both of them
    # are rate constants of the controller.
    #
    # THAT IDENTIFICATION IS THE PAYOFF OF THE HOUR, so it gets a surface of
    # its own rather than a clause in a foot. The review: "Slide 23 -- first
    # place with mu and theta", which is right, and the reason it is right is
    # that this is the first place either of them is PRODUCED by anything.
    # Before the subtraction they would be two symbols handed down.
    #
    # It mirrors the generic debrief: release, then a dark slide carrying the
    # answer. There the answer was X = r. Here it is what r was all along.
    s = d.dark()
    d.header(s, "segment 4", "debrief  ·  what the subtraction produced")
    d.title(s, "The set point is the ratio μ / θ")
    d.rows(s, [
        ("what cancels", "η·Z_{1}Z_{2} is the same term in both lines, so it "
                           "goes: d(Z_{1} − Z_{2})/dt = μ − θX. Nothing measured "
                           "anything — the chemistry subtracted.", CYAN),
        ("so u = Z_{1} − Z_{2}", "the difference between the two species is the "
                            "running total of the error. That is the "
                            "integrator the derivation assumed."),
        ("and r = μ / θ", "μ − θX is θ·(μ/θ − X), which is θ·e. So the "
                          "set point the derivation called r is μ/θ, and "
                          "the gain it called G is θ."),
        ("why the plant gets no vote", "μ and θ are both rate constants of "
                                       "the controller. There is nothing in "
                                       "the set point for the circuit being "
                                       "controlled to reach.", AMBER),
    ], top=1.92, label_color=CYAN)
    d.foot(s, "Two rate constants you chose, and a ratio. The result still carries its clause: it holds while the closed dynamics are stable.")
    d.notes(s,
           "This is the answer to the question I held back at the "
           "derivation: what sets r."
           "\n The annihilation term is identical in both lines, so it "
           "cancels. d(Z1 − Z2)/dt = mu − theta·X. That is du/dt = G·e "
           "with u = Z1 − Z2."
           "\n Factor theta out: mu − theta·X = theta·(mu/theta − X). So "
           "r = mu/theta and G = theta. Both of them fell out of the "
           "chemistry; neither was handed to them."
           "\n mu is the rate Z1 is made at. theta is the rate per unit "
           "of output that Z2 is made at. One is a rate, the other is a "
           "rate per concentration, so the ratio is a concentration — "
           "which is what a set point has to be."
           "\n Now the sentence the hour is built on, read out with its "
           "clause: the steady-state value of the output is determined "
           "solely by the ratio mu/theta, and does not depend on the "
           "topology and parameters of the circuit of interest — as long "
           "as the closed dynamics are stable. I keep that clause every "
           "time."
           "\n And the consequence: you never characterize your plant. "
           "Change host, promoter, chassis. The two numbers that set the "
           "level are yours."
           "\n If someone asks why G does not matter: it has to be "
           "positive and that is all the derivation asked. Here it is "
           "theta, which is positive because it is a production rate.")

    s = d.light()
    d.header(s, "segment 4", "debrief  ·  what you just derived, drawn")
    d.title(s, "The antithetic motif")
    # 4.60, not 4.95, to buy the line underneath: the PNG saves at
    # 9.74 x 4.43in, so placement is height-limited and the scale is 1.038.
    d.image(s, FIG + "s22_motif.png", M, 1.66, w=W - 2 * M, h=4.60)
    # The constraint, at the moment the result lands. No bound and no number:
    # those are the actuator segment's work, a third of an hour later.
    d.text(s, "It holds while Z\u2081 has room to push. What happens when "
              "Z\u2081 runs out is still to come.",
           M, 6.30, W - 2 * M, 0.38, size=20, color=INK)
    d.foot(s, "The banner is your two lines. Nothing in the picture measures anything — the chemistry does the subtraction.")
    d.notes(s,
           "This goes up only after they have the result. The banner is "
           "the line they just derived."
           "\n I walk the picture once: Z1 at a constant rate, Z2 in "
           "proportion to the output, the two destroy each other, and "
           "the plant a box labeled ANY TOPOLOGY, IF Z1 CAN MOVE X."
           "\n Then the line under it, and I do not derive it here: the "
           "result holds while Z1 has room to push. Z1 is a count of "
           "molecules and the plant is driven by Z1 alone, so when Z1 "
           "runs down to nothing the controller has nothing left to "
           "push with and the output leaves the set point.")

def _sequestration(d):
    s = d.dark()
    d.header(s, "segment 4", "debrief  ·  the reaction underneath it")
    d.title(s, "You have seen this reaction all term")
    d.rows(s, [
        ("18", "a factor held by decoy sites. You named it: sequestration."),
        ("19", "a ribosome held by every other mRNA in the cell."),
        ("21", "a regulator held by its own downstream targets — and the "
               "holding was the cost."),
        ("22", "Z_{1} held by Z_{2}. Aoki built it from a σ factor and its anti-σ "
               "factor, and the paper's own words are: RsiW stably "
               "SEQUESTERS and holds SigW inactive.", CYAN),
    ], label_color=CYAN)
    d.foot(s, "Four sessions, one reaction. On three of them it was the disease. Here it is the cure.")
    d.notes(s,
           "One sentence under all four rungs: a molecule held by "
           "something that is not its target is not available to do its "
           "job."
           "\n On rungs 1 to 3 — sessions 19, 20, 21 — that "
           "unavailability was the problem. Burden, coupling, "
           "retroactivity."
           "\n Here it is the mechanism. Z1 and Z2 annihilate cleanly "
           "enough to integrate because each takes the other out of "
           "circulation completely, with nothing left over."
           "\n Same physics, opposite sign."
           "\n Sequestration: the disease on rungs 1 to 3, the cure on "
           "rung 4.")


# ------------------------------------------------------------------- Aoki ---
def _aoki(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  somebody built it, out of parts you know")
    d.title(s, "σ and anti-σ")
    d.rows(s, [
        ("σ factor", "the subunit that tells RNA polymerase which promoters "
                     "to read. SigW switches on P_{sigW} — more SigW, harder "
                     "that promoter fires. Z_{1} is the ACTUATOR.", CYAN),
        ("anti-σ factor", "binds a σ one-to-one and holds it off the "
                          "polymerase. RsiW comes from P_{BAD}, and AraC "
                          "drives P_{BAD}. AraC IS the controlled output — "
                          "sfGFP is only the reporter that tracks it. "
                          "Z_{2} is the SENSOR.", AMBER),
        ("why that is an annihilation", "a σ held by its anti-σ does nothing, "
                                        "and the two leave circulation "
                                        "together — one for one, which is "
                                        "exactly what made the subtraction "
                                        "cancel."),
    ], top=1.95, label_color=CYAN)
    d.foot(s, "Both from B. subtilis, moved into E. coli. The annihilation is not engineered — it is what these two proteins already do.")
    d.notes(s,
           "Session 6 is the last sigma factor they saw, and anti-sigma "
           "has never come up, so I draw the mechanism."
           "\n The biology is this room's strong axis, on the survey, so "
           "I move briskly through the protein story and spend the time "
           "on the control story instead."
           "\n SigW is Z1 because it ACTUATES — it turns the output "
           "promoter on."
           "\n RsiW is Z2 because AraC drives its expression. AraC is "
           "not downstream of the output — AraC IS it. Their words: "
           "P_sigW drives araC and sfgfp together, AraC closes the loop "
           "by regulating P_BAD-driven rsiW, and sfGFP is proportional "
           "to AraC. So RsiW is made in proportion to X directly. That "
           "is the theta·X term, and sfGFP is how they read X off."
           "\n Sequestration, not inhibition: the complex takes one "
           "SigW and one RsiW out together, one for one.\n "
           "And if somebody asks whether a REVERSIBLE pair still "
           "integrates — it does, and I want to be exact about this "
           "because it is easy to get backwards. Release returns one of "
           "each, so the release term is identical in both equations and "
           "cancels on subtraction just as the binding term does. I "
           "checked it: with the complex cleared, the output sits on "
           "mu/theta to nine figures at k_off of 0, 1, 10, 100 and "
           "1000.\n "
           "What sequestration DOES need is that the complex be cleared. "
           "Leave a reversible pool that nothing removes and there is no "
           "steady state at all — the output sits off the set point and "
           "Z1 minus Z2 drifts for ever. Aoki's own caption hedges "
           "\"annihilate (or sequester)\" and the hedge is right. That "
           "is the home guide's item 2.")

    # THE PAPER ARRIVES HERE, NAMED, AND AS A PICTURE. Note 19: "we haven't
    # cited Aoki directly before this", and bar rule B4 -- a paper is
    # introduced before its results are quoted. Two slides later the room is
    # asked to read two P values off this experiment, and until now the deck
    # had never shown the experiment. s21's Mishra segment learned the same
    # lesson on 1 November and fixed it the same way: the device goes up
    # before anything is claimed about it.
    #
    # THE PANELS ARE THE ONES THE READING GUIDE POINTS AT. readings.yaml s22
    # says "Fig. 3a-b for the closed and open loop" -- so the slide shows what
    # the students were told to study, and the open-loop control stops being a
    # sentence and becomes a picture with a module missing from it.
    s = d.light()
    d.header(s, "segment 5", "frame  ·  the circuit, before any claim about it")
    d.title(s, "The open loop is this circuit minus one module")
    # A FULL-WIDTH, SHORT BAND, because the two panels sit side by side on the
    # page: measured off the held PDF they are about 3.4 wide to 1 tall, so a
    # squarer slot would leave the image small inside a big empty box and trip
    # the loose-slot report. 11.93 x 3.55 is 3.36, which fills from about
    # 2.5:1 to 4:1.
    d.paper_figure(s, "aoki2019_fig3ab", M, 1.78, W - 2 * M, 3.55,
                   "Aoki et al. 2019, Fig. 3a, b",
                   "left, the closed loop; right, the same circuit with "
                   "P_{BAD}–rsiW deleted",
                   show_caption=True)
    d.foot(s, "Aoki, Lillacci, Gupta, Baumschlager, Schweingruber and Khammash, Nature 570:533, 2019 — the paper assigned for today.")
    d.notes(s,
           "Their circuit, before anything is claimed about it. This is "
           "the paper they read for today."
           "\n The beige box is the controller they just derived. P_BAD "
           "makes RsiW, the yellow circle. P_LUX makes SigW, the gray "
           "one. The phi where the two meet is the annihilation — both "
           "of them to nothing."
           "\n The gray box is the plant — Aoki's own name for it is the "
           "circuit of interest. One promoter, P_sigW, driving araC and "
           "metE together, two tandem copies."
           "\n The blue box is the biology that turns MetE into growth: "
           "a methyl group onto homocysteine makes methionine, "
           "methionine makes biomass."
           "\n Right panel is the control. P_BAD-rsiW is gone. One "
           "module, and everything else identical."
           "\n I make them find the feedback path before I point at it. "
           "It leaves the gray box and climbs to P_BAD.")

    # NOTE 20, VERBATIM: "'Under it'? Poor phrasing. Be exact." The old title
    # was "They put a growth rate under it" and the old rows named the output
    # and the control and nothing else -- not the plant, not what was
    # perturbed, not how. All four are here now, and the title makes the one
    # claim the hour turns on: the disturbance is a temperature, and nobody
    # wrote a model of it. Every term here was defined in segment 2 -- plant,
    # output, sensor, open and closed -- except "circuit of interest", which
    # is Aoki's and is glossed where it appears.
    s = d.light()
    d.header(s, "segment 5", "frame  ·  what they changed, and what they compared")
    d.title(s, "The only thing they changed was the temperature")
    d.rows(s, [
        ("the plant", "two P_{sigW}–araC–metE modules — Aoki's circuit of "
                      "interest. SigW drives them, AraC carries the output "
                      "to the sensor, MetE makes methionine.", CYAN),
        ("the output", "sfgfp — superfolder GFP, the reporter — swapped for "
                       "metE, in a host whose own metE is deleted, in "
                       "methionine-free medium. The cell grows only as fast "
                       "as MetE lets it."),
        ("the perturbation", "incubation temperature: 37 °C, then 30 °C, held "
                             "constant. Nobody wrote a model of what the cold "
                             "does to the plant or to the controller.", AMBER),
        ("the comparison", "the same strain with the anti-σ module "
                           "P_{BAD}–rsiW deleted — sensor gone, loop open. "
                           "Same promoters, host, medium, inducers, and one "
                           "protein fewer, which is session 19's confound."),
    ], top=2.00, label_color=CYAN)
    d.foot(s, "Session 19 opened Part II on growth rate as the thing your circuit changes. This closes it on growth rate as the thing a circuit regulates.")
    d.notes(s,
           "The regulated output is the cell's own growth rate, not a "
           "fluorescent protein."
           "\n sfgfp replaced by metE in a delta-metE host, methionine "
           "out of the medium, so the cell grows only as fast as MetE "
           "lets it."
           "\n Session 19 opened Part II on growth rate as the thing a "
           "circuit changes. This closes it on growth rate as the thing "
           "a circuit regulates."
           "\n The open-loop control is the cleanest I have shown all "
           "term: they delete one module, the anti-sigma. Same "
           "promoters, host and medium. The only difference is whether "
           "the loop closes."
           "\n It does carry less protein than the closed-loop strain — "
           "session 19's confound.")


def _evidence(d):
    # NOTE 23, VERBATIM: "This introduction of P comes out of nowhere. The
    # next slide 'explains' but we are expecting the class to quote a figure."
    # Two P values were released to the room with no definition of P, no
    # statement of what was compared with what, and no effect sizes -- the
    # differences the two numbers were computed ON sat only in the speaker
    # note and in handouts/s22-control.md. NUMBERS.md 6 says so in terms.
    #
    # So the slide now carries, in order: the comparison, the difference, and
    # only then P, defined where it first appears (bar rule B1). "The null"
    # is named here too, because the debrief slide says "reject the null" and
    # until now nothing had told the room what the null was.
    #
    # THE NUMBERS. 1.00 -> 1.03 and 1.00 -> 0.33 are MEASURED, NUMBERS.md 6.
    # They are not redrawn: figures/s22_control.py's docstring refuses to
    # invent the points behind Aoki's bars, and quoting them as theirs is the
    # whole of the session-21 lesson.
    # THE DATA BEFORE THE STATISTICS. This figure used to come after the
    # room had been asked to interpret two P values, so they read the
    # numbers first and saw what the numbers were computed on two
    # surfaces later. The instructor: "they have no idea of the test or
    # the measurement before" that slide. Now the bars go up, then the
    # question. The title no longer presupposes the P values either.
    s = d.light()
    d.header(s, "segment 5", "frame  ·  their figure, before the numbers")
    # "Closed against open across seven degrees" described a sweep. There is
    # no sweep: two circuits, two temperatures, four bars. The replacement
    # names provenance rather than result, because the note has him read the
    # LEFT panel first -- a title announcing which way the bars go would pull
    # the room straight to them and cost the figure-reading lesson.
    d.title(s, "What they measured: two circuits, two temperatures")
    # American spelling, and the test named the way the paper names it. The
    # caption read "Welch t-test", which is the same test but is not a phrase
    # that appears anywhere in Aoki or in NUMBERS.md, so a student checking
    # the caption against the paper would have found nothing.
    d.paper_figure(s, "aoki2019_fig3d", M, 1.72, W - 2 * M, 3.95,
                   "Aoki et al. 2019, Fig. 3d",
                   "growth rate normalized to the 37 °C rate for each circuit, "
                   "n = 3; two-tailed unpaired unequal-variance t-test",
                   show_caption=True)
    d.notes(s,
           "The left half first, not the bars. The obvious reading is "
           "wrong."
           "\n The black feedback path leaves the araC/metE box and "
           "returns to the control system. The blue arrow marked cell "
           "growth leaves and never comes back."
           "\n So the loop closes through AraC — their words: AraC "
           "closes the loop by regulating PBAD-driven rsiW expression."
           "\n Growth rate rides on MetE downstream. It is not the "
           "sensed variable."
           "\n Their figure is titled Growth-rate control, which is the "
           "looser framing. The gap between a figure's title and its "
           "mechanism is what they should catch, and the home guide asks "
           "them about it."
           "\n Then the bars. The closed loop's normalized growth rate "
           "is statistically indistinguishable across the temperature "
           "change; the open loop's is not, by three and a half orders "
           "of magnitude."
           "\n Then the honest version: good evidence that the "
           "controller rejects the perturbation, not proof of perfect "
           "adaptation. Nothing at n = 3 could be.")
    s = d.light()
    d.header(s, "segment 5", "release  ·  read their two P values")
    d.title(s, "Is that adaptation?")
    d.rows(s, [
        ("what was compared", "each circuit against itself: its steady-state "
                              "growth rate at 30 °C against its own rate at "
                              "37 °C. n = 3 biological replicates, two-tailed "
                              "unpaired unequal-variance t-test."),
        ("what moved", "closed loop 1.00 → 1.03.      open loop 1.00 → 0.33.",
         CYAN),
        ("P", "how often a gap at least this large would turn up if "
              "temperature changed the growth rate not at all — that \"not at "
              "all\" is the null. Closed loop P = 0.2261. Open loop "
              "P = 7.769 × 10⁻⁵.", AMBER),
        ("your turn", "what does each of those two numbers license you to "
                      "say?"),
    ], top=2.00)
    d.foot(s, "Same test, same three replicates, both circuits. Whatever differs between the two numbers is in the data, not in the method.")
    d.notes(s,
           "The small P first: the open loop's growth rate moved, "
           "decisively. Normalized, 1.00 down to 0.33."
           "\n The large one is the question. Closed loop, normalized, "
           "1.00 to 1.03, and P = 0.2261."
           "\n P = 0.2261 is a failure to detect a difference at n = 3. "
           "Not a demonstration that there is none — three replicates "
           "could not have detected a modest one."
           "\n They met this five days ago on PS8 Q3d, with Mishra "
           "2014's 432 against 396 at n = 3, p = 0.10."
           "\n The sentence I used there and use again: a large p is a "
           "failure to detect a difference, not a demonstration that "
           "there is none."
           "\n What would settle it: an equivalence test, more "
           "replicates, or a stated effect size they can rule out.")

    s = d.dark()
    d.header(s, "segment 5", "debrief  ·  what each number licenses")
    d.title(s, "Two P values that do not mean the same thing")
    d.rows(s, [
        ("P = 7.769 × 10⁻⁵", "1.00 down to 0.33. The open loop's growth rate "
                             "moved with temperature. Reject the null. Say it "
                             "plainly.",
         CYAN),
        ("P = 0.2261", "1.00 to 1.03, and we FAILED TO DETECT a difference at "
                       "n = 3. That is not the same as showing there is none, "
                       "and with three replicates a modest change would have "
                       "looked like this too.", AMBER),
        ("what would settle it", "a bound on the difference rather than a "
                                 "failure to reject — which needs a stated "
                                 "effect size, and more replicates than "
                                 "three."),
    ], top=2.00, label_color=CYAN)
    d.foot(s, "A large P is the absence of evidence. It is not evidence of absence, and at n = 3 it is barely even the first one.")
    d.notes(s,
           "This is the debrief, so the answer goes up on the slide "
           "rather than only into the air."
           "\n P = 7.769 × 10⁻⁵: the open loop's growth rate moved with "
           "temperature. Reject the null."
           "\n P = 0.2261: failure to detect a difference at n = 3. Not "
           "the same as showing there is none — a modest change would "
           "have looked like this too."
           "\n Same distinction as PS8 Q3d: Mishra's 432 against 396, n "
           "= 3, p = 0.10. The sentence is the same one — a large p is a "
           "failure to detect a difference, not a demonstration that "
           "there is none."
           "\n The effect sizes behind these two numbers: closed loop "
           "1.00 to 1.03, open loop 1.00 to 0.33, normalized to each "
           "circuit's own 37 °C rate."
           "\n What I am NOT saying is that Aoki are wrong. The circuit "
           "very probably does reject the perturbation. The word that "
           "outruns the data is 'perfectly', and nothing at n = 3 could "
           "establish it.")



# ------------------------------------------------------------------- leak ---
def _leak(d):
    s = d.light()
    d.header(s, "segment 6", "frame  ·  what the derivation assumed")
    d.title(s, "An integrator is not allowed to forget")
    d.rows(s, [
        ("we assumed", "Z_{1} and Z_{2} are lost ONLY by annihilating each other. "
                       "That is what makes Z_{1} − Z_{2} a perfect running total."),
        ("the paper says", "the ideal analysis assumed negligible degradation "
                           "of the controller proteins — and that in living "
                           "cells this fails, in the case of fast-growing "
                           "cells, by dilution."),
        # delta IS DEFINED HERE, which is where it first appears and where
        # the rest of this segment starts arguing with it -- on the figure
        # axis one surface later, and on the comparison at the close. It had
        # been defined only in the speaker note, and a symbol defined in a
        # note is not defined (bar B1).
        ("the cell grows", "so Z_{1} and Z_{2} are diluted along with everything "
                           "else in it, at a rate δ. δ is the growth rate, "
                           "and it belongs to the host.", AMBER),
        ("the total leaks", "a running total that is itself being removed is "
                            "no longer a running total.", AMBER),
        ("so", "the output no longer settles exactly on the set point.",
         AMBER),
    ], top=2.00, label_color=TEAL)
    d.foot(s, "The integrator forgets at exactly the rate the cell divides.")
    d.notes(s,
           "Back to the aside in the motif frame: anything that decays "
           "forgets, and a controller that forgets is not an integrator."
           "\n delta is the dilution rate set by growth. The cell "
           "divides, so Z1 and Z2 go with everything else."
           "\n The subtraction again, with dilution in it: mu − theta·X "
           "= delta·(Z1 − Z2). The error is no longer zero. It is "
           "proportional to delta.")

    s = d.light()
    d.header(s, "segment 6", "build  ·  how much does it cost")
    d.title(s, "First order in the growth rate")
    d.image(s, FIG + "s22_leak.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "Slope one on log-log. Halve the growth rate and you halve the error — there is no threshold and no safe region.")
    d.notes(s,
           "Straight line across the whole sweep, delta from 4e-4 to "
           "0.2. Fitted slope 0.998 — first order in delta."
           "\n X_ss − mu/theta = −(delta/theta)(Z1 − Z2). The minus sign "
           "is easy to drop, and dropping it flips a claim that is "
           "already conditional."
           "\n PS8 Q5 asks them to get that exponent out of the algebra "
           "rather than off this plot."
           "\n The sign is not fixed, so the leak MOVES the set point "
           "rather than lowering it. At the d = 1 this figure uses the "
           "output undershoots; past d = 2.05 — still inside the "
           "actuator bound of 2.5 — it overshoots."
           "\n The arc: in session 19 growth rate was what your circuit "
           "changed. Here it is what degrades your circuit's guarantee. "
           "Rung 1 eating rung 4.")

    s = d.light()
    d.header(s, "segment 6", "release  ·  find the bound")
    d.title(s, "Where does it run out?")
    d.rows(s, [
        ("what you have", "dX/dt = k·Z_{1} − γX + d, and the set point is "
                          "X = μ/θ."),
        ("the constraint", "Z_{1} is a molecule, so Z_{1} ≥ 0. The controller can "
                           "only push the output UP."),
        ("your turn", "the disturbance is positive — something is making X "
                      "on its own. How large can d get before the controller "
                      "cannot hold the set point at all? Give it in terms of "
                      "γ, μ and θ."),
    ], top=2.05)
    d.foot(s, "At the set point, what does the plant still need from the controller — and what is the least the controller can supply?")
    d.notes(s,
           "Harder than the subtraction. This is PS8 Q4c, five days in "
           "their hands."
           "\n At the set point the plant needs k·Z1 = gamma·mu/theta − "
           "d, and Z1 cannot go below zero, so d ≤ gamma·mu/theta. With "
           "mu = 10, theta = 2, gamma = 0.5, the bound is 2.5."
           "\n The other sign, if it comes up: a disturbance REMOVING X "
           "is one the controller makes more Z1 against, and there is no "
           "bound on that side. Only the direction it cannot push is "
           "limited."
           "\n Past the bound, the trap. Z1 goes to zero but the "
           "annihilation does NOT stop — it PINS at mu. dZ1/dt = mu − "
           "eta·Z1·Z2, and Z1 cannot go negative, so the flux sits at "
           "mu."
           "\n So Z2 climbs at theta·X − mu = 10, not at theta·X = 20. I "
           "say PINS, never 'stops' — a room told it stops predicts "
           "twice the slope they will measure in Q4c."
           "\n Z1 has no single value past the bound: it decays like "
           "1/t. At d = 5 it is 2.5e-6 at t = 8000, the horizon Q4c "
           "uses, and half that at 16000."
           "\n The flux is mu to within a part in a million at both "
           "horizons, and that is the part that does not move."
           "\n Z2 is what runs: about 80,000 at t = 8000 and 160,000 at "
           "16000. Doubling the horizon doubles it, which is the linear "
           "climb at 10."
           "\n X itself SETTLES, at d/gamma, stably and in the wrong "
           "place. The runaway is Z2 alone, which is why Q4c watches Z2. "
           "There is no steady state, and a simulation that stops at one "
           "horizon reports one anyway.")

    # THE ANSWER, STEPPED (bar C2: if the room is asked to solve something,
    # the deck steps through it with them -- not "solve this" followed by the
    # answer). The release above asks for the bound and the surface that
    # followed it opened with "the bound you just derived", which is the
    # failure note 27 names. Four lines, one move each, and the only one with
    # any content is the second.
    #
    # FOUR STEPS AND A CLOSING BOX IS THE GEOMETRY THAT KEEPS THE ASIDES.
    # derivation() reserves the band 1.62-5.52 when there is a closing line,
    # so four steps run at pitch 0.975 and five at 0.78 -- and below 0.86 the
    # asides survive on the live step only. The asides are where the sign
    # argument lives, so four it is.
    d.derivation(
        None, "segment 6", "debrief  ·  the bound, with them",
        "The controller can only push one way",
        [
            ("a steady state holds X still",
             "0 = k·Z_{1} − γX + d",
             "dX/dt = 0. That is all a steady state means."),
            ("put X on the set point",
             "k·Z_{1} = γ·(μ/θ) − d",
             "what the plant still needs from the controller"),
            ("Z_{1} is a count of molecules",
             "Z_{1} ≥ 0,  so  γ·(μ/θ) − d ≥ 0",
             "the controller can ADD X. It has no way to remove any."),
            ("the bound, with numbers in",
             "d ≤ γ·μ/θ = 0.5 × 5 = 2.5",
             "γ = 0.5 and μ/θ = 5. Note what is absent: k."),
        ],
        closing="A bigger k buys no extra range. k is not in the bound.",
        note="Take the bound from the room first, then step these four."
             "\n Step one is the definition of steady state and nothing "
             "more."
             "\n Step two is the only line with content: at X = mu/theta "
             "the plant still needs k·Z1 = gamma·mu/theta − d from the "
             "controller."
             "\n Step three is the constraint they are least likely to "
             "reach for. Z1 is a molecule count, so it cannot go below "
             "zero."
             "\n So d <= gamma·mu/theta = 2.5. This is PS8 Q4c, five "
             "days in their hands."
             "\n The closing line is worth saying twice. I swept k from "
             "0.25 to 20: the last d that settles is 2.4 and the first "
             "that does not is 2.6, at every k. A stronger actuator buys "
             "nothing, because what is limited is the DIRECTION it "
             "cannot push, not the force it can."
             "\n The other sign, if it comes up: a disturbance REMOVING "
             "X is one the controller answers with more Z1, and nothing "
             "bounds that side."
             "\n If someone offers mu/theta as the knob: raising the set "
             "point does raise the bound, and it also moves the thing you "
             "are controlling. gamma is the honest knob.")

    s = d.light()
    d.header(s, "segment 6", "debrief  ·  and what happens past it")
    d.title(s, "Past the bound the annihilation pins at μ")
    d.image(s, FIG + "s22_past_the_bound.png", M, 1.62, w=W - 2 * M, h=5.05)
    d.foot(s, "Said as 'the annihilation stops', this predicts twice the slope they will measure. It pins at μ, which is the most it can ever be.")
    d.notes(s,
           "Left panel first, and it is a ledger rather than a "
           "trajectory. Two books on Z2, in the same units: theta·X is "
           "what Z2 gains, eta·Z1·Z2 is what it loses."
           "\n X has settled at d/gamma = 10, so theta·X = 20 and stays "
           "there."
           "\n Z1 is down to 2.5e-6 by t = 8000 — the actuator is empty "
           "— and the annihilation flux is still 10 to a part in a "
           "million."
           "\n Why it cannot be anything else: dZ1/dt = mu − eta·Z1·Z2, "
           "and Z1 cannot go negative, so the flux cannot sit above mu "
           "and cannot sit below it either. It PINS."
           "\n The shaded gap IS dZ2/dt: 20 − 10 = 10."
           "\n Right panel: the dashed line is what 'it stops' predicts, "
           "slope theta·X = 20. Twice the truth, and the error is "
           "invisible in the algebra."
           "\n Z2 reaches 79,979 at t = 8000 and 159,979 at 16,000. "
           "Twice the horizon, twice Z2, which is why Q4c makes them run "
           "two."
           "\n X itself settles, stably, at d/gamma = 10. The runaway is "
           "Z2 alone.")

    # LIGHT, AND IT WAS DARK. Nothing in the course places a matplotlib
    # figure on a dark slide -- every figure is authored on the light slide
    # ground "#F8FAF9", so a dark surface would have carried a bright white
    # card. The comparison has to be a figure (a two-column grid is a
    # geometry, and rows() makes one column), so the surface follows the
    # figure rather than the figure following the surface.
    s = d.light()
    d.header(s, "segment 6", "debrief  ·  four ways it breaks, not one")
    d.title(s, "Running out is not the same as leaking")
    # The same four questions asked of both failures in the same order, so
    # the eye crosses a row instead of reading down two paragraphs. This was
    # four rows of sentences, which is note 28's "wall of text" -- and the
    # row that separates the two failures, whether there is a steady state
    # at all, was the one the prose buried.
    d.image(s, FIG + "s22_two_failures.png", M, 1.52, w=W - 2 * M, h=3.80)
    # No color bars on these two. AMBER and TEAL are the figure's two
    # columns, and a bar in either would read as "this limit belongs to that
    # failure", which neither of them does.
    d.rows(s, [
        ("stability", "a loop that oscillates has no steady state to be "
                      "exact about."),
        ("variance", "their closed loop tended to be more variable cell to "
                     "cell, and less so on perturbation. The mean is pinned, "
                     "not the spread."),
    ], top=5.44, bottom=6.62, label_w=1.55, label_color=TEAL)
    d.foot(s, "Integral feedback rejects any disturbance it has the authority to reject. That sentence needs both halves.")
    d.notes(s,
           "The runaway is a delta = 0 statement and I keep the "
           "condition on it."
           "\n With any dilution there IS a steady state past the bound: "
           "Z2 caps at (theta·X − mu)/delta. At delta = 0.01 and d = 5 "
           "that is Z2 = 1000, identical at t = 8000 and 16000."
           "\n So what separates the two failures is how BIG Z2 gets, "
           "not whether it converges."
           "\n The overstatement I break: 'integral feedback rejects any "
           "disturbance.' It rejects any disturbance it has the "
           "authority to reject."
           "\n Stability is the limit I name and do not derive. Deciding "
           "it means linearizing the closed loop, and on the survey that "
           "is the thing most of them have not done, even where the "
           "eigenvalue mechanics are there."
           "\n So I state the condition and leave the derivation to Part "
           "III."
           "\n Saturation looks convergent and is not. Z2 climbs "
           "linearly for ever while X drifts to d/gamma."
           "\n So a simulation that stops at one horizon reports a "
           "steady state that does not exist. PS8 Q4c makes them check "
           "two horizons."
           "\n Leak: wrong place. Saturation: no place.")

    # THE PAPER'S OWN TREATMENT OF THE SAME TWO (note 28: "without backup
    # from paper figures"). Both failures are one sentence of Aoki's text --
    # limited production capacity, and dilution in fast-growing cells -- and
    # Extended Data Fig. 1 is the figure that sentence points at: panels b
    # and c are dilution alone, panel d adds actuator saturation. It is also
    # the counterweight the segment owes them. Three surfaces on how the
    # guarantee breaks, and their own finding is that with realistic
    # parameters it does not break enough to matter.
    s = d.light()
    d.header(s, "segment 6", "debrief  ·  theirs, not ours")
    d.title(s, "They model both failures and map the error")
    # 3.70, not 4.20: the slot and a real image do not sit the same way --
    # the dashed slot carried its own ref and caption, an embedded image
    # puts them below itself, which pushed the caption onto the foot.
    d.paper_figure(s, "aoki2019_edfig1", M, 1.80, 6.65, 3.70,
                   "Aoki et al. 2019, Extended Data Fig. 1d",
                   # 41 characters, not 51: the caption box is the IMAGE's
                   # drawn width, not the 6.65in slot, so theme's line_cap
                   # over-estimates it and the longer version wrapped with
                   # "once" alone on line two.
                   "dilution, disturbance, saturation at once",
                   show_caption=True)
    d.rows(s, [
        ("what they assumed away", "unlimited production, and no loss of Z_{1} "
                                   "and Z_{2} except to each other."),
        ("what they did about it", "simulated it at realistic E. coli "
                                   "numbers, and mapped where the "
                                   "steady-state error stays under 5%."),
        # ONE LINE SHORTER AND NO LONGER PRESENTED AS A QUOTATION. The row
        # had their sentence verbatim under a label that said so, which ran
        # five lines deep and put the stack 0.15in past the band. It is
        # their finding either way, and the hedge is the whole reason the
        # row is here, so the hedge is what the paraphrase keeps.
        ("their conclusion", "at realistic parameters the error is small "
                             "enough, they suggest, to count as perfect "
                             "adaptation in growing cells.", TEAL),
    # left=7.70, not 7.90: the colored bar on the last row pushes the body
    # column 0.20in right, which cost a character a line and a line a row.
    ], top=1.86, bottom=6.40, left=7.70, right=W - M, side=False, pad=0.04)
    d.foot(s, "A leak you can put somewhere it does not matter is a design problem, not a dead end.")
    d.notes(s,
           "Their Extended Data Fig. 1, and it is the figure attached to "
           "the sentence behind the frame's second row."
           "\n That sentence names both of our failures in one breath, and "
           "it is theirs, not mine: production capacity is limited, and in "
           "fast-growing cells the dilution of the controller proteins has "
           "to be in the dynamics."
           "\n Panels b and c are dilution with a negative disturbance. "
           "Panel d adds actuator saturation."
           "\n The shadings are where the relative steady-state error "
           "stays under 5% — green bacteria, blue yeast, yellow "
           "mammalian, by dilution rate."
           "\n Their conclusion, and I read the hedge out loud with it. "
           "They do not claim perfect adaptation outright. They say the "
           "errors at realistic parameters are small enough to SUGGEST it, "
           "for all practical purposes."
           "\n So the honest summary is not that it leaks and that is "
           "that. It leaks, first order, and a designer can put the leak "
           "where it does not matter. That is what a map of parameter "
           "space is for."
           "\n One caution if anyone reads the axes closely: their "
           "disturbance is NEGATIVE and ours is positive, so their "
           "saturation boundary is not our d <= gamma·mu/theta. Same two "
           "mechanisms, opposite sign convention.")


# ------------------------------------------------------------------ close ---
def _close(d):
    # THE LEDGER AS A BUILD, which is bar rule C1 and note 29 ("wall of
    # text. This could be stepped through"). All four columns survive, and
    # the constant-ownership sentence survives word for word, because
    # _instantiate quotes it as this deck's authority on whose constant is
    # whose. What changed is the RATE.
    #
    # derivation() is the course's own step-slide mechanism (lecture-design
    # 5b) and it is the only one here that holds the pitch FIXED: it sizes
    # the run from len(steps) and draws steps[:i], so a line that is on the
    # slide at click 2 has not moved by click 4. pacing() already counts a
    # step run as one slide's worth of material, which is what 5d means by
    # "a slide, not a lecture" -- this is one ledger shown in four moments,
    # not four ledger slides.
    #
    # WHY NOT AN ACCUMULATING rows() STACK. rows() spreads its leftover band
    # between the rows it is handed, so the same four rows revealed one at a
    # time put row 2 at 3.66 for three clicks and then at 3.42, and row 3 at
    # 5.11 and then 4.62. A build whose earlier lines slide up the wall on
    # the last click is worse than the wall it replaced.
    #
    # label_steps=True, AGAINST THE DEFAULT, and on purpose. The step
    # counter is the better choice for a fifteen-step derivation, which is
    # what it was added for. Here the header is not a segment label being
    # repeated -- it is the name of a recurring ritual that every session
    # ends on, and a student should recognize the surface on click one.
    #
    # THE ONE COST, said out loud rather than discovered: every rhs here is
    # longer than the 56 rendered characters derivation() warns at, so the
    # build prints four "step equation wraps onto its aside" lines. They are
    # false on this run -- the warning is about an equation wrapping into
    # its own aside, and these steps carry no asides, which is also why
    # three lines of 20 pt body fit inside the 1.125in pitch with 0.117in
    # spare. The alternative was demoting the ledger's load-bearing
    # sentences into a 14 pt italic aside, which is where this slide's
    # content is least likely to be read.
    s = d.derivation(
        None, "close", "the design ledger",
        "You set two constants. The plant sets none.",
        [("knobs",
          "μ and θ. Aoki turn μ with AHL onto P_{LUX} driving sigW, θ with "
          "arabinose onto rsiW. The set point is the RATIO: anything hitting "
          "both equally is rejected too.", None),
         ("constraints",
          "δ is the growth rate and belongs to the host, not to you. k and γ "
          "belong to the plant. η belongs to the protein pair you picked. "
          "None of them is a dial.", None),
         # "WHATEVER THE PLANT" WAS THE OVERCLAIM'S LAST STANDING COPY, and
         # this row is the deck's own authority -- _instantiate's "what is
         # not covered" row says it must not claim more than this one does.
         # The three conditions that were here are kept and a fourth is
         # named first, because it is the one that decides whether the word
         # "plant" applies at all. The row has to stay inside three rendered
         # lines: the pitch is 1.125in for four steps and 56 characters a
         # line at the 20 pt floor, so 168 characters is the ceiling and
         # this is 162. "any constant d" rather than "any constant
         # disturbance" buys ten of them, and d is defined on the
         # five-words surface and used on every surface since.
         ("guarantee",
          "exact adaptation to any constant d, in any plant the controller "
          "can move and can see — while the loop is stable, it is lost only "
          "to itself, and Z_{1} has range left.", None),
         # The note promises that each limit carries its observable. Two of
         # the three did; the actuator's said only that Z1 pins at zero,
         # which is a mechanism and not something you can see from a bench.
         # X settling at d/gamma is the thing you can see, it is in
         # NUMBERS.md section 4, and it is what makes the runaway findable
         # from a trace rather than only from the algebra.
         ("limits",
          "actuator: Z_{1} pins at zero and X settles at d/γ. Dilution: the "
          "error tracks the growth rate. Stability: it rings and never "
          "settles.", None)],
        dark=True, label_steps=True)
    d.foot(s, "Aoki's own design rule for the leak: pick controller species whose only loss channel IS dilution. σ factors are stable; RNA is not.")
    d.notes(s,
           "Knobs have to be physical or they are not knobs. AHL onto "
           "P_LUX for mu, arabinose onto P_BAD for theta, both in Aoki's "
           "Fig. 2c."
           "\n The set point is the RATIO mu/theta, so a global insult "
           "that scales both is rejected without anyone designing for "
           "it."
           "\n Constraints: delta is the host's growth rate, k and gamma "
           "belong to the plant, eta to the protein pair they picked. "
           "None is a dial."
           "\n The foot line is the paper's own fix for the leak: the "
           "native stability of these sigma and anti-sigma factors is "
           "what makes integral action practical in fast-growing cells, "
           "in contrast to RNA-based controllers where instability is a "
           "major limitation."
           "\n So the fix is not 'dilute less', which they cannot do. It "
           "is a PART CHOICE."
           "\n Each limit carries its observable, because a limit you "
           "cannot see from the bench is not one you can design around.")

    # NOTE 30, AND THE OLDEST UNFIXED ITEM IN THE REVIEW. This slide was
    # titled "Four rungs up the ladder" and no slide in this course has ever
    # said what a rung is. The metaphor GOES rather than gets a definition,
    # for three reasons and in this order:
    #
    #   * THE WORDS ARE ALREADY SPENT, ON SCREEN. Session 12 teaches "an
    #     infinite ladder" of master equations, one rung per molecule number
    #     -- in a derivation run, in a step label ("Name the flow across one
    #     rung") and in its closing box. The room has met "rung" exactly
    #     once and it meant an equation. A second on-screen meaning for the
    #     same two words is worse than no metaphor at all.
    #   * THE COURSE ALREADY HAS AN ON-SCREEN CONVENTION FOR THIS ARC, and
    #     it is not the metaphor. s19's close slide and s21's _ladder both
    #     put these same sessions on a slide, and both NAME them -- s21's
    #     row labels are "session 18 / session 19 / today". Neither prints
    #     the word. This surface now matches them.
    #   * A TERM INTRODUCED AT THE CLOSE CARRIES NO ARGUMENT. B3 exists so
    #     that a word is defined before it does work. Introduced here it
    #     does none, so a definition would be decode cost at minute 76 and
    #     nothing else.
    #
    # "Rung" and "the ladder" stay in the module docstring and in DESIGN.md,
    # which are instructor-facing and where the metaphor earns its keep as
    # an index into the arc.
    #
    # AND NOTE 30'S OTHER HALF -- the comparison, made visual. Not the
    # comparison that is already drawn twice: see fig_defenses_traded's
    # docstring for what the hinge figure carries (you need no list, costs
    # deferred) and what fig_partial_vs_exact carries (0.6193 moves, zero
    # does not), and for why the EXCHANGE is the one claim neither of them
    # makes.
    #
    # THE 10 -> 22 THREAD KEEPS ITS PLACE, in the two sentences under the
    # figure and in the foot's number, because the note's "I say the last
    # line slowly" points at those sentences and Part III opens on them.
    # They are the last line on the slide, which is where the note needs
    # them. The conditions the old foot carried are now inside the figure,
    # so the foot stops saying them twice.
    s = d.light()
    d.header(s, "close", "two threads, both ending here")
    d.title(s, "Only the fourth defense needed no list")
    d.image(s, FIG + "s22_defenses_traded.png", M, 1.62, w=W - 2 * M, h=3.90)
    d.text(s, "Approximate adaptation needs the right parameters. Exact "
              "adaptation needs the right topology.",
           M, 5.66, W - 2 * M, 0.42, role="emphasis", bold=True, color=INK)
    d.foot(s, "Session 10 asked whether a circuit can ignore a step. You computed 0.6193 of it still there on PS5; today the answer is zero.")
    d.notes(s,
           "Part II closes on two threads, not one."
           "\n The rungs are the thread they expect: burden, "
           "stoichiometry, retroactivity, control — sessions 19 through "
           "22."
           "\n The session 10 thread has been open since the middle of "
           "Part I. 0.6193 against zero is the distance between a motif "
           "that fights a step and a motif that integrates it."
           "\n I say the last line slowly. Approximate adaptation needs "
           "the right parameters; exact adaptation needs the right "
           "topology. Part III opens on that sentence.")

    s = d.light()
    d.header(s, "close", "notes down — the three from the start")
    d.title(s, "Can you answer these now?")
    d.rows(s, [
        # THE LABELS ARE HIS and are the bookend to the goals slide. The
        # bodies needed two repairs.
        #
        # ONE: "that level" had no antecedent. The goals slide opens the row
        # with "A controller holds the output of the circuit it controls at
        # a fixed level", and this row was that row with the first sentence
        # cut off, so it pointed at a level the slide never named.
        #
        # TWO: "destroy each other" is right at the top of the hour and
        # wrong here. The motif segment spends a slide on the fact that
        # RsiW does not destroy SigW -- it holds it, one for one, and the
        # cancelation needs only that the two leave together. Asking the
        # question back in the word the hour retired undoes the correction.
        # "One for one" is fig_motif's own hand-off phrase.
        ("what the set point can depend on",
         "what is the set point allowed to depend on, and what is it not "
         "allowed to depend on?"),
        ("why two molecules are enough",
         "two molecules that take each other out of circulation, one for "
         "one. Why does that keep a running total of how far off the output "
         "is, and why does the circuit being controlled not get a vote?"),
        ("what breaks it in a real cell",
         "name the ways a living cell misses it. There were four."),
    ], top=2.05)
    # NO FOOT. It read "The third one has four answers: actuator range,
    # dilution, stability, variance" -- the answer to the question the slide
    # asks, printed on the slide, on a notes-closed retrieval surface whose
    # own note says "I take these from the room rather than reading them
    # out". All three answers are in the note, which is where E4 puts them.
    d.notes(s,
           "Notes closed, and I take these from the room rather than "
           "reading them out."
           "\n One: mu and theta, nothing else — not k, not gamma, not "
           "d."
           "\n Two: Z1 − Z2 is the running total of the error, and a "
           "steady state forces that total to stop changing, which "
           "forces the error to zero. The plant never enters."
           "\n Three: actuator range, dilution, stability, variance. PS8 "
           "asks about the first two.")

    s = d.light()
    d.header(s, "close", "where this goes")
    d.title(s, "Before Thursday")
    d.rows(s, [
        ("Thursday", "session 23. The same circuit, two hundred generations "
                     "later, and what the population does to it."),
        ("PS8", "due 19 November. Q4 and Q5 are this session — and Q4c is the "
                "saturation trap we just took apart."),
    ], top=2.05)
    # The forward link the template asks for (lecture-design section 6:
    # today's result as a constraint on next session's problem). The title,
    # the rows and the note are unchanged; this is the one line that was
    # missing. It is today's result -- both constants in X = mu/theta sit in
    # the controller and none in the plant -- used against Thursday, whose
    # own frame slide says feedback cannot help because the controller is
    # encoded in the thing being removed.
    d.foot(s, "Both constants in today's answer live in the controller, and nothing today said the controller stays as you built it.")
    d.assignment(s, y=4.20)
    d.notes(s,
           "PS8 Q4c is the saturation trap we just took apart. It has "
           "been in their set for five days looking like a bug in their "
           "integrator."
           "\n Q5 is the leak. The set calls it the SET-POINT error, not "
           "the adaptation error, because session 10 owns that name for "
           "final over peak. The note is in the question and I say it "
           "out loud too.")
