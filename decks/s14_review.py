"""Session 14 — Review and worked problems.

Tuesday 13 October 2026, two days before the midterm.

WHAT THIS SESSION IS. Not a summary of eleven sessions. Motions the course
asked students to WATCH rather than DO, plus one idea — basins — that was
taught at the board in session 9 and has never been on paper.

HOW IT IS BUILT, and why it was rebuilt on 11 October. Adam, reading the first
version: every segment "starts in the middle and stops before the end". He was
right, and it was one defect repeated six times. The unit was

    derivation run  →  worked example  →  your turn  →  [cut to a new topic]

so no segment said what object it was about before the algebra started, and
NONE of the five student releases was followed by the answer. The room worked a
problem and then watched a different topic begin. Three further symptoms came
from the same cause: a four-surface run about a Jacobian that never drew a
matrix, a trace with no gene attached to it, and the word "buys" standing in
for the outcome the segment exists to deliver.

So every segment here is four moves, in this order, and none is optional:

    FRAME     the object, drawn, and the question in the shape it gets asked —
              plus what a finished answer looks like. Before any algebra.
    BUILD     the derivation, with the PICTURE advancing beside it
              (`derivation_fig`), not arriving finished underneath it.
    RELEASE   their turn, on a different circuit.
    DEBRIEF   the answer to what they just worked, illustrated, on the item's
              own circuit, immediately.

That rule is now in `docs/lecture-design.md` and is not specific to session 14.

NOTHING FROM THURSDAY'S PAPER IS IN THIS DECK, and that is enforced rather
than asserted: `figures/s14_review.py` refuses to draw an exam circuit, and
`private/midterm/check_s14_firewall.py` reads the exam and every student-facing
file in this session and refuses its parameter sets, its rings, its gate and
its set-ups. Both gates caught real leaks that reading had missed.

    exam                           here
    symmetric mutual repression    mutual ACTIVATION, a = 3
    pure repression rings 3/4/5    mixed-sign loops of three and four
    two AND feedforward loops      a cascade against a C1 loop with an OR gate
    beta/gamma, with gamma moved   beta and the starting level only
    its own gate                   a different gate, levels further apart

NO PRINTED TIME RANGES. Adam, 11 October: drop them. Two adjacent surfaces of
the first build printed "67 – 73 min" and "66 – 71 min", and a restructure of
this size invalidates every one of them. The badge still exists — `pacing()`
uses it to tell one segment from the next — but it is descriptive and is not
drawn. Minutes are Adam's to set.

Run:  python tools/build_decks.py s14
"""
from decks.theme import Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED, WHITE, SILVER, RED

FIG = "figures/build/"
FILENAME = "s14-review"


def build():
    d = Deck("Session 14 — Review and worked problems", session=14)
    d.show_badges = False
    _opening(d)
    _frame(d)
    _motion1(d)
    _basins(d)
    _motion2(d)
    _motion3(d)
    _digital(d)
    _feedforward(d)
    _close(d)
    return d


# ---------------------------------------------------------------------------
def _opening(d):
    s = d.dark()
    d.text(s, "Session 14", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Review, by working five motions", M, 2.72, 8.3, 1.3,
           size=40, font="head", bold=True, color=WHITE)
    d.text(s, "Not a summary of eleven sessions — moves you have watched me make and have not made yourself, and one picture you have seen only on the board",
           M, 4.25, 8.6, 1.5, size=18, color=MINT, spacing=1.25)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Two days before the midterm. Say in the first minute that this "
               "is not a recap: it is five things you have seen done and have "
               "not done with a pencil.")

    s = d.light()
    d.header(s, "open", "What the hour is for")
    d.title(s, "Five motions, and how each one runs")
    d.rows(s, [
        ("every segment runs the same way", "I frame the question on a circuit, we build the method together, you work it on a DIFFERENT circuit, and then I put the answer up. Four moves, every time."),
        ("why these five", "each is something this course demonstrated and never required of you. The exam requires them."),
        ("one of them is new on paper", "basins — which state a circuit ends up in — has been on the board and nowhere else. It is assessed on Thursday."),
        ("what you need in front of you", "the practice sheet. Nothing on it is on Thursday's paper; the point is the motion, not the example."),
    ])
    d.foot(s, "A correct answer with no reason earns half. Everything today is about the reason.")
    d.notes(s, "Hand out s14-review-practice.md now and tell them it stays "
               "face down until the first worked example is up.\n"
               "Say the four moves out loud once. It tells the room when to "
               "listen and when to write, and they will not have to guess "
               "whether an answer is coming — it always is.")


# ---------------------------------------------------------------------------
# MOTION 1 — what a wiring diagram tells you
# ---------------------------------------------------------------------------
def _frame(d):
    s = d.light()
    d.header(s, "loops-frame", "Frame  ·  what we are after")
    d.title(s, "Read the wiring, say what the circuit DOES")
    d.image(s, FIG + "s14_loop_outcomes.png", M, 1.78, W - 2 * M, 3.95)
    d.rows(s, [
        ("the outcome", "a diagram in, a verdict out: oscillate, latch, or settle. No numbers, no solving."),
    ], top=5.92)
    d.foot(s, "Three circuits, three verdicts, and the only thing counted was inversions.")
    d.notes(s, "This is the slide that was missing. Say the outcome in those "
               "words before anything else: a diagram in, a verdict out.\n"
               "Do not work any of the three yet — they are the destination, "
               "and the next few surfaces are how you get there.")

    d.derivation(
        None, "loops-build", "Built one line at a time",
        "What a loop does to a disturbance",
        [("Nudge a gene, walk it round",
          "a disturbance returns  FLIPPED  or  UNFLIPPED",
          "each repression inverts; each activation does not"),
         ("It is also scaled on the way",
          "returns  SHRUNK  or  NOT SHRUNK",
          "g  ≡  how steep that one step is at the operating point"),
         ("And each step takes time",
          "a delay, accumulated once per stage",
          "the half that matters for FREQUENCY"),
         ("Flipped? shrunk? late?",
          "FLIPPED ?     SHRUNK ?     LATE enough ?",
          "three independent questions, and a clock needs all three")],
        closing="Unflipped → latch. Shrunk → settles. Flipped+unshrunk: necessary, not enough.",
        note=("The two boxes go on the board and stay there all hour. This is "
              "the one idea worth more on Thursday than anything else today.\n"
              "Do not let anyone collapse the two questions into one."))


def _motion1(d):
    s = d.light()
    d.header(s, "loops-worked-a", "Worked  ·  a mixed ring")
    d.title(s, "Mixed signs: two flips, so it comes back unchanged")
    d.image(s, FIG + "s14_round_trip.png", M, 1.70, W - 2 * M, 2.55)
    d.rows(s, [
        ("count the flips", "two — the activation is an edge but not an inversion. Even, so the sign returns unchanged."),
        ("so what is it", "a latch. It reinforces what began it, and no amount of gain changes that."),
    ], top=4.55)
    d.foot(s, "Count edges and you get three. Count INVERSIONS and you get two. Only the second one matters.")
    d.notes(s, "Walk it with a finger, out loud, twice. Ask after the first "
               "walk whether the strengths matter for THIS question — no, they "
               "decide shrunk, not flipped.")

    s = d.light()
    d.header(s, "loops-worked-b", "Worked  ·  an even loop")
    d.title(s, "Zero flips: it comes back unchanged, and latches")
    d.image(s, FIG + "s14_even_latch.png", M, 1.70, W - 2 * M, 2.70)
    d.rows(s, [
        ("count the flips", "ZERO — and zero is even. X up makes more Y, more Y makes more X. Nothing inverts anywhere."),
        ("so what is it", "positive feedback. It runs away from where it started and stops at an extreme — and there are two extremes."),
    ], top=4.70)
    d.foot(s, "Zero is an even number. The test is parity, not presence — a loop with no bars in it fails the clock test just as surely.")
    d.notes(s, "Make the parity point explicitly: students read 'even number "
               "of inversions' and go looking for inversions to count. Zero "
               "counts.\n"
               "This pair is the bridge into the basin segment: the round trip "
               "explains WHY it has two states, and the next question is which "
               "one you get.")

    s = d.light()
    d.header(s, "loops-release", "Your turn  ·  item 1  ·  groups of 2–3")
    d.title(s, "A loop with mixed signs")
    d.rows(s, [
        ("on the sheet", "a FOUR-gene loop: X ⊣ Y, Y → Z, Z ⊣ W, W ⊣ X. Walk a nudge around it and say what comes back."),
        ("then", "can it be a clock? If it can, say what still has to be true — passing one half of the test is not enough."),
        ("and then change ONE edge", "make Z → W instead. Same four genes, same strengths. Does the verdict change, and why?"),
    ])
    d.foot(s, "I want the walk said out loud in your group, not done in your head. The answer goes up straight afterwards.")
    d.notes(s, "Circulate. The common error is counting edges instead of "
               "inversions — an activation is an edge and not a flip, so this "
               "loop has four arms and three flips.\n"
               "The one-edge change is the point of the item: parity flips, "
               "nothing else moves, and the verdict reverses.")

    s = d.light()
    d.header(s, "loops-debrief", "Debrief  ·  item 1")
    d.title(s, "One edge, and the verdict reverses")
    d.image(s, FIG + "s14_loop_debrief.png", M + 1.7, 1.64, W - 2 * M - 3.4, 3.22)
    d.rows(s, [
        ("what settled it", "how many bars — odd against even. Not the strengths, not which gene."),
        ("what it does NOT settle", "the odd one is not a clock yet: one test of three. Gain and delay still to go."),
    ], top=5.08)
    d.foot(s, "Parity is cheap and it is only the first question. A circuit that fails it is finished; a circuit that passes it has two more to go.")
    d.notes(s, "Take the walk from the room before you reveal it, node by "
               "node. The error to listen for is counting the ARROW as a "
               "flip.\n"
               "Then make the general point once: parity is settled by the "
               "wiring alone, which is why it is the first thing to ask and "
               "the cheapest thing to check.")


# ---------------------------------------------------------------------------
# BASINS — the segment that exists because the board cannot carry it
# ---------------------------------------------------------------------------
def _basins(d):
    s = d.light()
    d.header(s, "basins-frame", "Frame  ·  a question the last segment cannot answer")
    d.title(s, "It has two states. Which one do you GET?")
    d.rows(s, [
        ("take an even loop — the latch", "the two-gene activator pair from earlier, or the right-hand loop a moment ago. Both of them settle into one of TWO stable states and hold it."),
        ("what parity does NOT tell you", "which of the two. A cell has to be in one of them, and something has to decide — and nothing in the last segment says what."),
        ("the question, in the shape it gets asked", "the cell sits in one state. Something gives it a brief push and then STOPS — nothing about the circuit changes. Does it come back, or does it end up in the other state?"),
        ("what a finished answer says", "which SIDE of a dividing line the push left it on. Not how big the push was — 'it depends how big' is true and is not an answer."),
    ])
    d.foot(s, "This has been on the board in this course and nowhere else. It is on Thursday's paper.")
    d.notes(s, "THIS IS THE SEGMENT THE DECK EXISTS FOR. lecture-design 5b "
               "says the board carries nothing that is assessed, and this is "
               "assessed. Do not improvise it away.\n"
               "Read the third row out as written — it is the exact shape of "
               "the question, and students who have only seen the picture "
               "answer a different one.")

    d.derivation_fig(
        "basins-build", "Built one line at a time",
        "Two states is not the whole story",
        [("The circuit, in a plane",
          "X → Y ,    Y → X",
          "a POINT here is one cell, right now"),
         ("Where each gene would sit still",
          "nullclines:   ẋ = 0    and    ẏ = 0",
          "on one, x holds; on the other, y holds"),
         ("They cross three times",
          "both OFF ,    a SADDLE ,    both ON",
          "two you can sit in, one you cannot"),
         ("The way IN divides the plane",
          "one side → both OFF.   other → both ON",
          "not how big the kick was. Only which side")],
        [FIG + "s14_basin_stage1.png", FIG + "s14_basin_stage2.png",
         FIG + "s14_basin_stage3.png", FIG + "s14_basin_stage4.png"],
        closing="That line is a separatrix. You are asked which side — never the word.",
        note=("The picture grows with the argument here, which is the point: "
              "the first build put the phrase 'two states is not the whole "
              "story' in front of a room that had not been shown the circuit, "
              "the axes or the question.\n"
              "The circuit is mutual ACTIVATION, deliberately. Do not redraw "
              "it as a toggle at the board.\n"
              "Do NOT take inducer-threshold questions here — that is session "
              "9's other mechanism, where a parameter moves and a fixed point "
              "is destroyed. One line if it comes up: kick the state, or move "
              "the landscape."))

    s = d.light()
    d.header(s, "basins-worked-a", "Worked  ·  read it off the flow")
    d.title(s, "Two genes that switch each other ON")
    d.image(s, FIG + "s14_basins.png", M + 1.5, 1.60, 5.5, 4.85)
    d.rows(s, [
        ("the circuit", "X → Y and Y → X. Each needs the other."),
        ("two stable states", "filled dots: both off at the origin, both on out at 2.618."),
        ("the saddle", "open dot, on the diagonal at 0.382."),
        ("the red curve", "the divide. It runs INTO the saddle."),
        ("read it", "pick a point. Which side of red? That is where it goes."),
    ], top=1.75, left=7.3, label_w=2.1)
    d.foot(s, "Both off is a stable state here: with neither gene made, neither has anything to switch it on.")
    d.notes(s, "Make them pick a point and say the answer before you do. Two "
               "or three points is enough.\n"
               "If someone asks why both-off is stable: because each promoter "
               "needs the OTHER protein, and there isn't any.")

    s = d.light()
    d.header(s, "basins-worked-b", "Worked  ·  the number that catches everyone")
    d.title(s, "A pulse in X alone does not start on the diagonal")
    d.rows(s, [
        ("the saddle is at 0.382", "so the rule people reach for is: get X past 0.382 and it switches on."),
        ("but a pulse raises X ALONE", "when it ends the cell is at (x, 0) — on the axis, with Y still at zero. Nothing has made any Y yet."),
        ("and the divide is a CURVE", "it passes through (0.382, 0.382), but where it crosses the x-axis it is out at 0.711."),
        ("so the rule is wrong", "a pulse to x = 0.5 is past 0.382 and falls back OFF. One to 0.72 switches on."),
    ])
    d.foot(s, "Which side of the curve — never how far along one axis. Both coordinates are part of the question.")
    d.notes(s, "Slow here. This is the hardest idea in the hour and it is the "
               "one most likely to be asked badly on Thursday.\n"
               "Point at the red curve meeting the axis on the previous slide "
               "while you say 0.711. Then say the reason in one line: Y has to "
               "be made before it can hold X up, and at the moment the pulse "
               "ends there is none.")

    s = d.light()
    d.header(s, "basins-worked-c", "Worked  ·  four pulses, run forward")
    d.title(s, "Two fall back, two switch on — the close pair differ by 0.04")
    d.movie(s, FIG + "s14_basin_runs.mp4", M + 0.6, 1.66, 11.4, 4.45,
            poster=FIG + "s14_basin_trajectories.png",
            caption="click to run them — the still is the finished comparison")
    d.foot(s, "Nothing about the circuit changed between these four. Only where the pulse left the cell.")
    d.notes(s, "Play it once, then stop on the two middle runs and ask what "
               "is different about them. The honest answer is 0.04 in x, and "
               "that is the whole lesson.\n"
               "If the clip does not play, the poster frame already carries "
               "the four finished paths and both traces — teach from it and "
               "say nothing about the video.")

    s = d.light()
    d.header(s, "basins-release", "Your turn  ·  item 4  ·  groups of 2–3")
    d.title(s, "The same question with only ONE variable")
    d.rows(s, [
        ("the circuit", "one gene activating its own promoter, with a small basal rate. One variable, not two."),
        ("the move", "sketch production and removal on the same axes. Three crossings. Which are states, which is the divide?"),
        ("then", "give the NUMBER a pulse has to clear — and say in one line why the two-gene case could not be answered with a number."),
    ])
    d.foot(s, "On a line a divide can only be a point; in a plane it is a curve. That is the whole of it.")
    d.notes(s, "The arrows are the method: production above removal pushes "
               "right, below pushes left. Arrows toward a crossing means a "
               "state, away from it means the divide.\n"
               "Do not give the number. 0.683 is on the answer sheet and on "
               "the debrief slide.")

    s = d.light()
    d.header(s, "basins-debrief", "Debrief  ·  item 4")
    d.title(s, "On a line the divide is a number — and you can read it off")
    d.image(s, FIG + "s14_autoactivator_debrief.png", M, 1.72, W - 2 * M, 3.75)
    d.rows(s, [
        ("the method, in one line", "where production is above removal, x grows. Arrows TOWARD a crossing make it a state; arrows AWAY make it the divide."),
    ], top=5.70)
    d.foot(s, "0.68 falls back; 0.69 climbs. Add a second variable and that number becomes a curve — which is why 0.382 was the wrong answer earlier.")
    d.notes(s, "Take the three crossings from the room first, then the "
               "arrows, then the verdict. Do not shortcut to the number.\n"
               "Close the loop out loud: the 1-D case is the one where 'how "
               "far along x' and 'which side' are the same question, and the "
               "2-D case is where they come apart.")


# ---------------------------------------------------------------------------
# MOTION 2 — signs of a Jacobian
# ---------------------------------------------------------------------------
def _motion2(d):
    s = d.light()
    d.header(s, "jac-frame", "Frame  ·  a different kind of question")
    d.title(s, "A matrix of SIGNS, read straight off the wiring")
    d.rows(s, [
        ("what you have done all term", "put numbers into a model and get eigenvalues out. That is not this."),
        ("what this is", "the other direction: write the PATTERN of plus, minus and zero in the Jacobian, and say where each entry came from. Nothing is differentiated."),
        ("why anyone cares", "the pattern alone settles real questions — whether a circuit can oscillate at all, whether anything can destabilise it. Cheap, and it works before you have any numbers."),
        ("what a finished answer looks like", "a matrix with every entry filled, and one clause per entry naming the arrow in the diagram that put it there."),
    ])
    d.foot(s, "Thursday asks you to write one of these. So we are going to write one.")
    d.notes(s, "Say the last line plainly. The first build spent four "
               "surfaces on partial-derivative notation and never drew a "
               "matrix, in a segment whose exam item asks for a matrix.")

    d.derivation_fig(
        "jac-build", "Built one line at a time",
        "Filling it in, one rule at a time",
        [("The shape every one of these has",
          "ẋ  =  (production)  −  x",
          "production: other species. Removal: only this one"),
         ("Diagonal: does x act on itself?",
          "∂ ẋ / ∂ x   =   − 1     always",
          "production has no x in it. The step people miss"),
         ("Off-diagonal: j ACTIVATES i?",
          "∂ ẋ_{i} / ∂ x_{j}   >   0",
          "more j, more production of i"),
         ("Off-diagonal: j REPRESSES i?",
          "∂ ẋ_{i} / ∂ x_{j}   <   0",
          "more repressor, less production. That is all of it")],
        [FIG + "s14_jacobian_stage1.png", FIG + "s14_jacobian_stage2.png",
         FIG + "s14_jacobian_stage3.png", FIG + "s14_jacobian_stage4.png"],
        closing="Own removal on the diagonal; who acts on whom off it. Nothing differentiated.",
        note=("The matrix on the left fills in as the rule on the right is "
              "stated — that is the whole reason this is a step run with a "
              "figure rather than four surfaces of notation.\n"
              "The diagonal is the error. Ask explicitly where the production "
              "term went before you write the −1."))

    s = d.light()
    d.header(s, "jac-worked", "Worked  ·  two wirings")
    d.title(s, "Same rule, and what a ZERO entry means")
    d.image(s, FIG + "s14_jacobian_signs.png", M, 1.70, W - 2 * M, 3.45)
    d.rows(s, [
        ("why it matters", "a zero is not a small number — it means the wiring has no arrow there, so that species appears nowhere in the other's equation."),
    ], top=5.35)
    d.foot(s, "You are not asked for the trace–determinant plane. You are asked where each entry came from — zeros included.")
    d.notes(s, "The activator–repressor has one positive off-diagonal; the "
               "cascade has four zeros. Those are the two to work. Do not "
               "write out any OTHER two-gene sign pattern at the board — one "
               "of them is a Thursday item. Do not go into the trace–"
               "determinant plane: it was handed to them once as a reference "
               "and nothing this term was decided with it.")

    s = d.light()
    d.header(s, "jac-release", "Your turn  ·  item 2  ·  groups of 2–3")
    d.title(s, "Nine entries, and several of them are zero")
    d.image(s, FIG + "s14_cascade_release.png", M, 1.64, W - 2 * M, 3.40)
    d.rows(s, [
        ("the part that counts", "why an entry is ZERO rather than small — and what that buys you on the eigenvalues."),
        ("disagree out loud", "about the diagonal, before I put it up."),
    ], top=5.22)
    d.foot(s, "Take the diagonal first; it is where the error lives.")
    d.notes(s, "Take answers on the diagonal first. If the room is quick, "
               "push the triangular question: what does a matrix with zeros "
               "above the diagonal give you for free?")

    s = d.light()
    d.header(s, "jac-debrief", "Debrief  ·  item 2")
    d.title(s, "The zeros ARE the sentence 'nothing feeds back'")
    d.image(s, FIG + "s14_jacobian_debrief.png", M, 1.70, 6.1, 4.60)
    d.rows(s, [
        ("lower triangular", "so the eigenvalues ARE the diagonal."),
        ("λ = −1, −1, −1", "real and negative at EVERY parameter value."),
        ("so it cannot be unstable", "and it cannot oscillate — no imaginary part to oscillate with."),
        ("and the reason is the wiring", "the zeros ARE “nothing feeds back”."),
    ], top=1.84, left=7.0, label_w=2.6)
    d.foot(s, "That is the same sentence as motion 1, from the other side: no loop, so no round trip to pass or fail.")
    d.notes(s, "Make the connection back to the first segment explicitly. It "
               "is the only place in the hour where two motions meet, and it "
               "is worth the thirty seconds.")


# ---------------------------------------------------------------------------
# MOTION 3 — draw a curve
# ---------------------------------------------------------------------------
def _motion3(d):
    s = d.light()
    d.header(s, "curve-frame", "Frame  ·  a real protein, on real axes")
    d.title(s, "First: what is actually being simulated")
    d.image(s, FIG + "s14_curve_system.png", M + 1.3, 1.72, 10.4, 4.24)
    d.rows(s, [
        ("the outcome", "given a circuit and a switch, draw the trace."),
    ], top=6.08)
    d.foot(s, "One gene, one promoter, one protein, two rates. Everything today's traces do comes off that one equation.")
    d.notes(s, "Adam, 11 October: draw the system being simulated. The first "
               "build opened on axes with no apparatus attached to them, and "
               "the honest question back was 'a trace of WHAT?'\n"
               "Walk the cartoon left to right once: promoter, gene, protein, "
               "and the two arrows that are the two terms in the equation.")

    s = d.light()
    d.header(s, "curve-anatomy", "Frame  ·  what a trace is made of")
    d.title(s, "Three things make a curve")
    d.image(s, FIG + "s14_curve_anatomy.png", M, 1.68, 6.6, 4.17)
    d.rows(s, [
        ("where it starts", "zero, here — no protein yet."),
        ("how fast it leaves", "β, the promoter's full rate."),
        ("where it ends", "β/γ, where the two arrows balance."),
        ("the clock", "half-way at ln2/γ — about 2 minutes."),
    ], top=1.84, left=7.5, label_w=2.0)
    d.foot(s, "Every number on those axes is one you could have measured. Nobody is marking your draughtsmanship.")
    d.notes(s, "Point back at the cartoon for each of the three: the start is "
               "the empty cell, the departure rate is the β arrow, the end is "
               "where β and γ balance.")

    s = d.light()
    d.header(s, "curve-worked", "Worked  ·  what each knob drags with it")
    d.title(s, "Nothing moves just one of the three")
    d.image(s, FIG + "s14_curve_moves.png", M, 1.80, W - 2 * M, 3.70)
    d.rows(s, [
        ("the habit", "before you draw, ask which of the three the change touches — and what it drags along with it."),
    ], top=5.72)
    d.foot(s, "β sets how fast it leaves and where it ends, together. Where you start changes how fast it leaves, because removal is already running.")
    d.notes(s, "Resist naming which of the three a given regulation changes "
               "in general — that is item 3's work, and the answer depends on "
               "what is being held fixed, which is a question they should "
               "carry into Thursday rather than receive from me.")

    s = d.light()
    d.header(s, "curve-release", "Your turn  ·  item 3  ·  groups of 2–3")
    d.title(s, "Draw two curves on the axes you are given")
    d.rows(s, [
        ("draw", "an unregulated gene, and the SAME gene with negative autoregulation added — same promoter, same removal rate."),
        ("then mark", "each curve's own half-way time on the time axis."),
        ("and say", "which of the three — start, slope, end — the feedback changed, and which it left alone. There is more than one."),
    ])
    d.foot(s, "If you are slow, take the first curve from me and spend your time on the second. The second one is the skill.")
    d.notes(s, "Expect 'the slope is steeper'. It is not, at t = 0: there is "
               "no repressor yet. What changes first is where it ENDS.")

    s = d.light()
    d.header(s, "curve-debrief", "Debrief  ·  item 3")
    d.title(s, "Same promoter, same removal — so what actually moved?")
    d.image(s, FIG + "s14_curve_debrief.png", M + 1.0, 1.70, 6.6, 3.95)
    d.rows(s, [
        ("the start", "unchanged. No protein either way."),
        ("the slope", "unchanged — no repressor at t = 0, so both leave at β."),
        ("the end", "LOWER. Repression on an unchanged promoter drops it."),
        ("'faster'?", "needs a comparison before it means anything."),
    ], top=1.82, left=8.0, label_w=1.6)
    d.foot(s, "Compare at each curve's OWN half-way time. Comparing endpoints answers a different question.")
    d.notes(s, "Leave 'faster' open deliberately — do not supply the "
               "comparison that makes it mean something. Being able to STATE "
               "the comparison is what an A-part item turns on, and handing "
               "it over here would spend it.\n"
               "If someone insists the regulated curve starts steeper, put "
               "t = 0 to them: how much repressor is there?")


# ---------------------------------------------------------------------------
# The log convention — the hardest arithmetic they are asked to recognise
# ---------------------------------------------------------------------------
def _digital(d):
    s = d.light()
    d.header(s, "margins-frame", "Frame  ·  what a margin is for")
    d.title(s, "How much noise can the next gate take?")
    d.image(s, FIG + "s14_margins_frame.png", M, 1.80, W - 2 * M, 3.55)
    d.rows(s, [
        ("what a margin is", "how much dirt a level can pick up and still be read as the digit it was meant to be."),
    ], top=5.55)
    d.foot(s, "Positive at both ends and the gate cleans its own noise. Negative at either end and it does not.")
    d.notes(s, "Session 13, recognition only — no numeric signal matching "
               "under exam conditions. What they need is that gain is a log "
               "slope and a margin is a distance.")

    d.derivation(
        None, "margins-build", "Built one line at a time",
        "Gain and margin, in the convention we actually used",
        [("Gain is a LOG slope",
          "G  ≡  d ln(out) / d ln(in)",
          "fractional out per fractional in. Session 13"),
         ("A threshold: |G| = 1",
          "| G |  =  1",
          "under 1 it squashes noise, over 1 it amplifies"),
         ("Two inputs, two outputs",
          "x_{IL} → y_{OH} ,        x_{IH} → y_{OL}",
          "off the curve: the output AT each threshold"),
         ("A margin: output vs input",
          "NM_{L} = log ( x_{IL}/y_{OL} ) ,  NM_{H} = log ( y_{OH}/x_{IH} )",
          "carry it onto the input axis — a ratio becomes a gap")],
        closing="Positive both ends: it cleans its own noise. Negative either end: it does not.",
        note=("The carry across out = in is the step people skip, and it is "
              "the only step that makes a margin a distance rather than a "
              "subtraction of two numbers off different axes."))

    s = d.light()
    d.header(s, "margins-worked", "Worked  ·  one construction, four moves")
    d.title(s, "Carry the output across, then measure what is left")
    d.image(s, FIG + "s14_margins_steps.png", M, 1.95, W - 2 * M, 3.30)
    d.foot(s, "The carry across out = in is the step people skip, and it is the only step that makes a margin a distance.")
    d.notes(s, "Do all four panels at the board speed of the clicker. The "
               "gate here is not the one from session 13's handout — the "
               "levels are further apart so both gaps are visible from the "
               "back.")

    s = d.light()
    d.header(s, "margins-debrief", "Debrief  ·  back to the question")
    d.title(s, "So: how much noise can it take?")
    d.rows(s, [
        ("the answer, for this gate", "two gaps, one at each end, both positive — so a level can drift by that much and still be read correctly at the join."),
        ("what makes them gaps and not numbers", "the carry across out = in. Without that diagonal a margin is two numbers off two different axes, and the subtraction means nothing."),
        ("how you would be asked", "shown a curve: mark the thresholds, carry the outputs across, and say whether the gate can drive a copy of itself."),
        ("the recognition test", "if your two margins come out on the SAME axis, as a distance, you did it right. If you subtracted an output from an input, you did not."),
    ])
    d.foot(s, "A gate that cannot drive a copy of itself cannot be used in a chain — which is the only reason any of this matters.")
    d.notes(s, "Short segment, no release — this one is recognition. Close it "
               "by answering the frame's question in one sentence so it does "
               "not end mid-air the way the first build did.")


# ---------------------------------------------------------------------------
# MOTION 5 — a shortcut changes one end, and the gate decides which
# ---------------------------------------------------------------------------
def _feedforward(d):
    s = d.light()
    d.header(s, "ffl-frame", "Frame  ·  two circuits, one wire apart")
    d.title(s, "When the input switches, which end of the output moves?")
    d.image(s, FIG + "s14_ffl_frame.png", M + 0.5, 1.72, W - 2 * M - 1.0, 3.60)
    d.rows(s, [
        ("the outcome", "given the wiring and which arm is slow, say which END of the output's trace is delayed — and say WHY, from what the output is waiting for."),
    ], top=5.58)
    d.foot(s, "Both circuits see the same input. One has an extra wire and a gate. That is the whole difference.")
    d.notes(s, "Set the regime out loud before any algebra: Y is slow and "
               "sets the clock, Z follows its own promoter quickly. Without "
               "that the question has no answer.")

    d.derivation(
        None, "ffl-build", "Built one line at a time",
        "What a shortcut does to a trace",
        [("Two routes, one slow",
          "X → Y → Z   (slow)        X → Z   (prompt)",
          "Y sets the clock; Z follows its own promoter quickly"),
         ("What Z waits for, going UP",
          "OR: either route will do → Z does NOT wait for Y",
          "the shortcut is already there the moment X arrives"),
         ("And coming DOWN",
          "OR: X is gone, but Y alone still satisfies the gate",
          "so Z cannot fall until the SLOW arm has decayed"),
         ("So one end only is late",
          "prompt ON,   late OFF        — a sign-sensitive delay",
          "and with AND instead of OR, both answers swap over")],
        closing="A shortcut speeds the end where it is the ONLY thing needed. The gate picks it.",
        note=("Do not let them leave with 'coherent loops delay the ON step'. "
              "The SAME wiring gives the opposite answer under the other "
              "gate, which is why the question is always what the output is "
              "waiting for.\n"
              "The cascade, for contrast, is late at both ends — no shortcut "
              "exists, so there is nothing to be asymmetric about."))

    s = d.light()
    d.header(s, "ffl-worked", "Worked  ·  the two traces, measured")
    d.title(s, "Late at both ends, against prompt up and late down")
    d.image(s, FIG + "s14_ffl_worked.png", M + 2.05, 1.66, 9.1, 5.18)
    d.foot(s, "The numbers are computed from the model, not sketched. The cascade's two delays are nearly equal; the OR loop's are not.")
    d.notes(s, "Point at the two ON numbers first — 0.7 against 0.1 — and "
               "then at the two OFF numbers, which are the same. That pair of "
               "comparisons IS the sign-sensitivity.")

    s = d.light()
    d.header(s, "ffl-release", "Your turn  ·  item 5  ·  groups of 2–3")
    d.title(s, "Draw both traces, then say which end moved")
    d.image(s, FIG + "s14_ffl_axes.png", M, 1.66, 7.0, 4.71)
    d.rows(s, [
        ("you are given", "the wiring, the input X and the slow arm Y, for BOTH loops. Only Z is empty."),
        ("draw", "the cascade's Z, then the OR loop's."),
        ("say", "which end the shortcut changed, in terms of what Z is waiting for."),
        ("then", "what an AND gate would do. Reason it; do not guess."),
    ], top=1.78, left=7.5, label_w=1.6, bottom=6.30)
    d.foot(s, "The reasoning in the last question is the whole item.")
    d.notes(s, "Take the AND answer last and take it from the room. If nobody "
               "has it, walk the two ends again rather than telling them.")

    s = d.light()
    d.header(s, "ffl-debrief", "Debrief  ·  item 5")
    d.title(s, "Ask what the output is waiting for")
    d.image(s, FIG + "s14_ffl_debrief.png", M, 1.70, 6.3, 4.55)
    d.rows(s, [
        ("OR, going up", "either arm will do, and X is here NOW  →  PROMPT"),
        ("OR, coming down", "both arms must go, and Y is still high  →  LATE"),
        ("AND, going up", "needs both, so it waits for slow Y  →  LATE"),
        ("AND, coming down", "either arm going breaks it, and X goes at once  →  PROMPT"),
    ], top=1.96, left=7.2, label_w=2.4)
    d.foot(s, "Recall a slogan and you have a one-in-two chance. Work the ends and you cannot get it wrong.")
    d.notes(s, "Take the AND rows from the room before revealing them — they "
               "have just reasoned it.\n"
               "No AND-gated trace is drawn here on purpose: Thursday asks "
               "them to sketch two of those, and the table gives the "
               "reasoning without handing over the curve.")


# ---------------------------------------------------------------------------
def _close(d):
    s = d.light()
    d.header(s, "close", "If you take one thing from each")
    d.title(s, "Five sentences")
    d.rows(s, [
        ("the round trip", "count the flips first. An even number cannot be rescued by any gain — and flipped plus unshrunk is still only NECESSARY, never enough on its own."),
        ("basins", "which SIDE, not how far. On a line the divide is a number; in a plane it is a curve, and reading a curve as a number on one axis is how this gets lost."),
        ("Jacobian signs", "own removal on the diagonal; who acts on whom off it. A zero is a missing arrow, not a small number."),
        ("a time course", "a start, a slope and an end — and nothing moves just one of them."),
        ("a shortcut", "changes one end only, and which end is decided by the gate — never by a remembered rule."),
    ])
    d.foot(s, "A correct answer with no reason earns half. The reason is where you spend your time.")
    d.notes(s, "Close on the half-credit rule — it is on the scope sheet and "
               "it is the single biggest avoidable loss.")

    s = d.light()
    d.header(s, "after", "After Thursday")
    d.title(s, "The reading for 20 October")
    d.text(s, "Nothing to read before the midterm. This is for the Monday after it — do not open it this week.",
           M, 1.70, W - 2 * M, 0.6, size=17, italic=True, color=MUTED)
    d.assignment(s, y=2.45, label="For 20 October, after the midterm")
    d.notes(s, "Say explicitly that there is no reading before Thursday. The "
               "Cello paper is for session 16 and the obligation lands on "
               "this deck only because the midterm sits between.")

    s = d.dark()
    d.header(s, "thursday", "Thursday")
    d.title(s, "The midterm — Thursday 15 October, in class")
    d.text(s, "100 points · the full period · Dwinelle 219",
           M, 2.05, 11, 0.45, size=23, font="head", bold=True, color=MINT)
    d.text(s, "One page of notes, both sides, prepared by you. No calculator — one significant figure, and a bracketing argument is a complete answer. You write on the paper itself, in the box under each item; scratch paper is handed out, and anything on it needs your name, SID and the item label.",
           M, 2.62, 11.3, 1.6, size=16, color=WHITE, spacing=1.25)
    d.text(s, "Three items ask you to draw on a figure as well as write in the box — leave time for them.",
           M, 4.30, 11.3, 0.62, size=16, color=CYAN, spacing=1.2)
    d.text(s, "I will be proctoring remotely. Hetvi is in the room — ask her, and she can reach me.",
           M, 5.22, 11.3, 0.62, size=17, bold=True, color=AMBER, spacing=1.2)
    d.notes(s, "Say the proctoring arrangement out loud as well as showing "
               "it, and say it again at the door. Hetvi is in the room and "
               "can reach me the whole period.\n"
               "Answers to today's sheet go up after class.")


if __name__ == "__main__":
    build()
