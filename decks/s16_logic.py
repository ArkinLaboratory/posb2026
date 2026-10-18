"""Session 16 — Combinational and sequential logic.

Tuesday 20 October 2026. The first session of Part II.

WHAT THIS SESSION IS. Session 13 asked what must be true of a gene before you
may call it a gate. This one wires gates together and finds out what a truth
table does NOT promise you, then gives the circuit a memory and asks where the
memory should physically live.

THE ROOM HAS READ NIELSEN. The Cello paper went out at the end of session 14
on 13 October -- `build_readings.py` places it there deliberately so that
nothing is handed out at the end of an exam. So the Cello segment asks them to
USE the paper, not to be shown it.

HOW IT IS BUILT. Four moves per segment -- frame, build, release, debrief --
`docs/lecture-design.md` 5e. Every table on these slides is computed by
`posb.logic` at render time; none of the ticks is typed into a figure.

THE WRONG EXPLANATION IS TAUGHT ALONGSIDE THE RIGHT ONE, per the standing rule
(`posb-teaching-derivations` 6). The obvious reading of the glitch is "unequal
path lengths -- equalise them". The path lengths are real and the diagnosis is
wrong: a perfectly balanced circuit still glitches on a cold start, because a
repressor-based gate is ON before its repressor arrives. That correction is
the session's engineering result, not a footnote.

NO PRINTED TIME RANGES. Settled; minutes are Adam's.

Run:  python tools/build_decks.py s16
"""
from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)
from decks.theme import ROOT

FIG = "figures/build/"
FILENAME = "s16-logic"


def _fig(d, s, name, y, dpi=160):
    """Place a figure at its NATURAL size, centred, and return its bottom.

    figures/style.py saves with bbox="tight", so a PNG is cropped to its ink.
    Placing it at width = pixels/dpi means the deck neither enlarges nor
    shrinks it -- and a point inside the figure is then a point on the slide,
    which is the only way the 20pt type authored in figures/s16_logic.py
    actually arrives at 20pt in Dwinelle. Measured rather than written down,
    so re-rendering a figure at a different size cannot silently rescale its
    text. See posb-slide-legibility.
    """
    from PIL import Image
    w, h = Image.open(ROOT / FIG / f"{name}.png").size
    w, h = w / dpi, h / dpi
    d.image(s, FIG + f"{name}.png", (W - w) / 2, y, w, h)
    return y + h


def build():
    d = Deck("Session 16 — Combinational and sequential logic", session=16)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _reading(d)
    _truth_to_nor(d)
    _classifier(d)
    _glitch(d)
    _wrong_then_right(d)
    _cascade_delay(d)
    _cello(d)
    _latch(d)
    _dna_memory(d)
    _close(d)
    return d


# ---------------------------------------------------------------------------
def _opening(d):
    s = d.dark()
    d.text(s, "Session 16  ·  Part II begins", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "Logic in cells, and what a truth table does not tell you",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "Part I asked what a circuit does. Part II asks whether it "
              "survives being built. We start with a circuit that settles to "
              "the right answer and does damage on the way there.",
           M, 4.45, 8.6, 1.05, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Name the turn: Part I was analysis, Part II is construction. "
               "The exam is behind us, and the paper they read over the "
               "weekend carries the first half of the hour.")


# ---------------------------------------------------------------------------
# Reminder questions first, then what the hour is for. In that order, and
# before any new content, per Adam 18 October: the room has just come off an
# exam and needs to be back in the thread before anything is added to it.
# ---------------------------------------------------------------------------
def _retrieval(d):
    s = d.light()
    d.header(s, "retrieval", "Three minutes  ·  no notes")
    d.title(s, "Three things from before the exam")
    d.rows(s, [
        ("from Thursday's paper", "Loop Q: a cascade with a shortcut and an OR gate. Which END did the shortcut change, switching on or switching off? And why only one?"),
        ("from session 13", "a gate has TWO input thresholds. What is true at each of them?"),
        ("from session 9", "the toggle has two stable states. What decides which one a cell lands in?"),
    ])
    d.foot(s, "All three come back within the hour. The first one comes back in Boolean.")
    d.notes(s, "Take answers aloud. Do not resolve the first one. Loop Q is "
               "the analogue of today's hazard and it pays better if they "
               "meet it again rather than being told now.\n"
               "Third one: which side of the dividing line. Basins, s14.")

    s = d.light()
    d.header(s, "goals", "What the hour is for")
    d.title(s, "Where today goes")
    d.rows(s, [
        ("first, where a gate comes from", "a promoter with operators on it, and the Boolean function that arrangement computes. You derived the occupancy in session 6. Today it becomes a gate."),
        ("then, what a truth table leaves out", "when. A circuit built from repressors gives a wrong answer before it gives the right one, and in the therapy we will look at, that is fatal."),
        ("then, memory", "output that depends on the order the inputs arrived in. You built one in session 9 without being told its name."),
        ("and a number to carry out of here", "both halves of the hour end at the same limit, and it is not the design method."),
    ])
    d.foot(s, "Nielsen 2016 is the spine of the first half. You read it over the weekend; today we use it.")
    d.notes(s, "Say the four in order and leave them up for a beat. The "
               "fourth is withheld on purpose: they should be able to name "
               "it themselves by the close.")


# ---------------------------------------------------------------------------
# SEGMENT 0 — the paper they read, on the screen
#
# Added 18 October after Adam's note that slide 4 of the first build threw the
# room into a truth table with no introduction, no review of the reading and
# no picture of a real circuit. Fig. 1A is the pipeline; the truth table is
# one box inside it, and that is where it should arrive from.
# ---------------------------------------------------------------------------
def _reading(d):
    s = d.light()
    d.header(s, "cello-paper", "The paper you read")
    d.title(s, "Cello: a specification in, DNA out")
    d.paper_figure(s, "nielsen2016_fig1a", 1.42, 1.58, 10.50, 4.41,
                   "Nielsen et al., Science 352:aac7341 (2016), Fig. 1A",
                   "Verilog and a sensor table in; parsing to a truth table; "
                   "synthesis to AND-inverter, then to NOR and NOT; gate "
                   "assignment from the library; DNA out.")
    d.foot(s, "Every box in that diagram is a step somebody automated. We are going to open two of them.")
    d.notes(s, "Walk the top row left to right and name each box out loud, "
               "then drop to the User Constraint File and gate library "
               "underneath it. Ask which box they think is the hard one. "
               "Most say logic synthesis, which is the one that is solved.\n"
               "The two we open today: Verilog parsing, which produces the "
               "truth table, and the NOR/NOT library, which is where the "
               "gates come from. Gate ASSIGNMENT is where the failures are, "
               "and that is the segment after the break.")

    s = d.light()
    d.header(s, "reading-why", "What that buys")
    d.title(s, "The numbers you should have brought with you")
    d.rows(s, [
        ("what Cello did", "60 circuits designed from Verilog and all 60 built with no additional tuning, up to 10 regulators and 55 parts, 880 kb of DNA (p. aac7341-1)."),
        ("how well it worked", "45 of the 60 correct in EVERY output state; 92% of the 412 individual output states as predicted."),
        ("so the question for today", "the compiler ran on all sixty of them. What is the missing quarter made of?"),
    ])
    d.foot(s, "Hold that question. We come back to it once you have built a gate by hand.")
    d.notes(s, "Resist answering. The answer arrives in the Cello segment "
               "with Fig. 5A in front of them, and it is worth more earned "
               "than given.")


# ---------------------------------------------------------------------------
# SEGMENT 1 — from a specification to a gate you can clone
# ---------------------------------------------------------------------------
def _truth_to_nor(d):
    s = d.light()
    d.header(s, "spec-frame", "Frame  ·  the first box we are opening")
    d.title(s, "A truth table is a contract, not a circuit")
    d.rows(s, [
        ("where it comes from", "the Verilog parsing box. You write what the circuit must do; the table is that specification in a form a machine can act on."),
        ("what it promises", "for each combination of inputs, what the output must be ONCE EVERYTHING HAS SETTLED."),
        ("what it says about time", "nothing. Not a word. That silence is the whole first half of today."),
        ("what we do with it", "build a circuit from the gates biology actually gives you, then find out what the table failed to specify."),
    ])
    d.foot(s, "Say 'once everything has settled' out loud. We collect on that phrase later in the hour.")
    d.notes(s, "This slide exists because the first build of this session "
               "opened on the contract line to a room that had never been "
               "told where a truth table comes from. It comes out of the "
               "paper they just read, and the previous slide shows it.")

    s = d.light()
    d.header(s, "universal", "Frame  ·  what a gate library has to supply")
    d.title(s, "Two ingredients are enough to build every logic function")
    _fig(d, s, "s16_universal", 2.15)
    d.foot(s, "Every gate has to hand you both at once. The next two slides are two ways of arranging DNA that do it.")
    d.notes(s, "Make them say the two words back: a complement and an "
               "aggregator. Then ask which of the two a promoter with a "
               "repressor sitting on it already gives you, and let them get "
               "to repression IS the complement on their own.\n"
               "If someone asks about XOR: built from these, not extra.")

    d.derivation(
        None, "nor-build", "Built one line at a time",
        "Where a NOR gate comes from",
        [("Two sites, four states",
          "weights   1 ,   r_A ,   r_B ,   r_A\u00b7r_B",
          "r = [repressor] / K, the occupancy ratio from session 6"),
         ("The partition function",
          "Z  =  1 + r_A + r_B + r_A\u00b7r_B  =  (1 + r_A)(1 + r_B)",
          "it factorises because the two sites are independent"),
         ("Only the empty state fires",
          "P_on  =  1 / (1 + r_A)(1 + r_B)",
          "one promoter, so exactly one way to be ON"),
         ("Read the four corners",
          "(0,0) \u2192 1     (1,0) \u2192 0     (0,1) \u2192 0     (1,1) \u2192 0",
          "either repressor on its own is enough to silence it")],
        closing="That is NOR, and nobody chose it. The DNA layout wrote it.",
        note=("This is the slide that earns the rest of the hour. They "
              "derived the two-operator occupancy in session 6 and have "
              "never been told what it IS.\n"
              "Do not let 'NOR is universal' arrive as a fact imported from "
              "digital electronics. It arrives here out of a rate law they "
              "wrote themselves.\n"
              "Next slide draws the same equation over the whole r-plane, so "
              "the five lines above become one picture."))

    s = d.light()
    d.header(s, "arch-nor", "Build  ·  one promoter, two operators")
    d.title(s, "Read the gate off the map")
    _fig(d, s, "s16_arch_nor", 1.62)
    d.foot(s, "The four circled corners ARE the truth table. Nothing was tabulated; the map was read.")
    d.notes(s, "Point at the axes first: both are repressor concentration in "
               "units of that repressor's K, on a log scale, so the corners "
               "are 'far below threshold' and 'far above'.\n"
               "Then let the room read the four corners aloud before you say "
               "the word NOR. The large white region at the lower left is the "
               "only ON state, which is the whole content of the gate.")

    s = d.light()
    d.header(s, "arch-nand", "Build  ·  two promoters, one gene")
    d.title(s, "One operator moves, and the gate flips")
    _fig(d, s, "s16_arch_nand", 1.62)
    d.foot(s, "Same two repressors, same two sites, the opposite gate. Now look at the two half-strength ON corners.")
    d.notes(s, "This is the mechanistic answer to 'why NOR and not NAND', "
               "and the answer is that biology hands you both. The LAYOUT "
               "chooses. Two promoters driving one gene add their outputs, "
               "so the gene is silent only when both are blocked, and the "
               "ON region is now three corners instead of one.\n"
               "Make them look at the SHADE of those three corners. With "
               "both repressors low the output is 1; with one of them high "
               "it is only about a half, because one promoter is still "
               "firing and the other is not. A NAND built this way has a "
               "weak ON state, and that is a noise margin you would lose "
               "points for under the Cello score we meet after the break.\n"
               "Cello's library is NOR/NOT because its gates are "
               "repressor-promoter pairs on a single promoter, not because "
               "NAND is unavailable in cells. The classifier we look at next "
               "uses the two-promoter NAND, and now you can see why it is a "
               "NAND.")

    s = d.light()
    d.header(s, "voigt-nor", "The part Cello's library is made of")
    d.title(s, "A gate whose input and output are both promoters")
    _fig(d, s, "s16_voigt_nor", 1.52)
    d.foot(s, "Same tandem-promoter DNA as the slide before. What changed is which quantity you call the input.")
    d.notes(s, "Say this one slowly, because it is the piece the rest of the "
               "hour leans on and the first build of this session never "
               "showed it.\n"
               "A Cello gate is three things in one part: two input "
               "promoters in tandem, a repressor gene behind them, and an "
               "output promoter carrying that repressor's operator. Either "
               "input promoter firing makes the repressor, and the repressor "
               "shuts the output. NOR.\n"
               "Now the collision with the previous slide, out loud, because "
               "they will feel it: that is the SAME DNA we just called a "
               "NAND. It is. The difference is what you call the input. We "
               "called the inputs the two REPRESSORS binding the promoters, "
               "which inverts each input, and got NAND. Cello calls the "
               "inputs the two PROMOTER ACTIVITIES, and puts the inversion at "
               "the output instead. One architecture, two conventions, and "
               "you have to say which you are using.\n"
               "Then the universality slide pays off: the tandem promoters "
               "are the aggregator and the repressor on the output promoter "
               "is the complement. Both ingredients, one part. That is why a "
               "library of these alone can build anything.\n"
               "Last point, and it is the one that makes the paper make "
               "sense: the gate's input and output are the same KIND of "
               "quantity, a promoter activity in RPU. That is what lets you "
               "plug one gate into the next without a converter, and it is "
               "why the library can be characterised once and reused.")

    s = d.light()
    d.header(s, "nor-library", "The free gate library")
    d.title(s, "One operator is an inverter, two is a NOR, and that is all you need")
    d.rows(s, [
        ("one operator on a promoter", "out = NOT in. The complement, for the price of cloning an operator site."),
        ("two operators on a promoter", "out = NOT (in₁ OR in₂). Complement and aggregator in one piece of DNA, which is why NOR alone is universal."),
        ("compiling any table", "one term per row where the output is 1, then DeMorgan twice: every AND of literals becomes a NOR of their complements."),
        ("what it costs", "depth. Each layer is another gene, and a gene is a delay. Hold that thought."),
    ])
    d.foot(s, "The compilation always succeeds. That is exactly why it is not where the difficulty lives.")
    d.notes(s, "Keep this brisk. The point is that realisability is free and "
               "everything interesting sits downstream of it. AND you would "
               "have to engineer; NOR you can clone.")

    s = d.light()
    d.header(s, "nor-release", "Your turn  ·  groups of 2–3")
    d.title(s, "Compile XNOR")
    d.rows(s, [
        ("the table", "XNOR: output 1 when A and B agree, 0 when they differ."),
        ("build it", "from NOT and NOR only. Write the network as a list of genes and say what represses what."),
        ("then count", "how many genes deep is the longest path from an input to the output? And the shortest?"),
    ])
    d.foot(s, "The two depths are the answer I want. The network is how you get them.")
    d.notes(s, "Circulate. Common stall: trying to be clever and minimise. "
               "Tell them not to. Minimisation is cut from this course, and "
               "the unminimised network is the one that teaches depth.")

    s = d.light()
    d.header(s, "nor-debrief", "Debrief  ·  two of your answers")
    d.title(s, "One truth table, two circuits")
    _fig(d, s, "s16_xnor_two_ways", 1.52)
    d.foot(s, "Both compute XNOR. Neither is wrong. The table did not choose between them.")
    d.notes(s, "Put up whichever networks the room actually produced and "
               "sort them against these two. The left one is what the recipe "
               "gives: one NOR term per agreeing row, then an inverter. The "
               "right one is the smallest there is, and an exhaustive search "
               "over two-input NOR networks says so.\n"
               "Both numbers on each panel are computed from the gate list "
               "by posb.logic at render time, which is how the first version "
               "of this slide was caught claiming depths of 3 and 2.")

    s = d.light()
    d.header(s, "nor-choice", "Debrief  ·  what the choice costs")
    d.title(s, "Choosing between them is the compiler's job, not the table's")
    d.rows(s, [
        ("what you save", "two genes and one stage. In a cell that is two fewer transcription units to clone, two fewer proteins to express, and one less protein lifetime before the output is right."),
        ("why anyone would still ship the long one", "the recipe is mechanical and always works. The search is not: the number of NOR networks grows fast, and for a circuit of any size you stop at a good one rather than the best one."),
        ("where you have seen this", "the Cello pipeline, box three. 'Logic synthesis' is exactly this choice, made by a machine."),
        ("and in both of them", "the paths are not the same length. Longest four and shortest three on the left; three and two on the right."),
    ])
    d.foot(s, "Unequal path lengths, in both circuits, written down before anyone has said why they matter.")
    d.notes(s, "PLANT THE LAST ROW and do not explain it. The hazard segment "
               "collects on it, and the collection is much stronger if they "
               "wrote the numbers down themselves first.\n"
               "If someone asks whether a balanced XNOR exists: yes, pad the "
               "short path, and the second act of this session is that "
               "padding it does not help.")


# ---------------------------------------------------------------------------
# SEGMENT 2 — the classifier
# ---------------------------------------------------------------------------
def _classifier(d):
    s = d.light()
    d.header(s, "clf-frame", "Frame  ·  a real design problem")
    d.title(s, "Detect one cell type, and only that one")
    _fig(d, s, "s16_classifier", 1.58)
    d.foot(s, "R2 is one gene read by two independently repressed promoters \u2014 NAND. In a therapeutic version of this circuit, the output kills the cell.")
    d.notes(s, "Walk the circuit aloud. R2 is the one worth pausing on: ONE "
               "gene, TWO independently repressed promoters, so it is silenced "
               "by either repressor — the sum of two repressions is a NAND, "
               "and the biology picked the gate.\n"
               "Say the actuator line plainly. It is what makes the glitch a "
               "safety result rather than an engineering curiosity.")


# ---------------------------------------------------------------------------
# SEGMENT 3 — the glitch
# ---------------------------------------------------------------------------
def _glitch(d):
    d.derivation_fig(
        "glitch-build", "Built one tick at a time",
        "Put a clock on it and fill the table in",
        [("A cell that has just been made",
          "every gene at 0",
          "no protein exists yet. This is not a steady state"),
         ("One gate delay later",
          "R3  =  NOT R2 ,   and R2 was 0",
          "so R3 switches ON — with A = 0, where the answer is 0"),
         ("Let it settle",
          "R3 :   0 → 1 → 0 → 0",
          "right at the end, wrong on the way: a STATIC-0 hazard")],
        [FIG + "s16_timing_p1.png", FIG + "s16_timing_p2.png",
         FIG + "s16_timing_p3.png"],
        closing="The circuit is correct. Its truth table is correct. It still kills the wrong cell.",
        note=("Fill the first two rows WITH the room, out loud, before "
              "advancing. One gate reads tick t and presents at t+1; that is "
              "the whole model.\n"
              "Every number on these four panels is computed by posb.logic "
              "from the gate list, not typed in. The traces reproduce the "
              "2025 lecture's published table exactly, and a test asserts "
              "it.\n"
              "Collect on 'once everything has settled' here."))

    s = d.light()
    d.header(s, "glitch-survey", "And it is not one unlucky case")
    d.title(s, "Every input combination glitches")
    _fig(d, s, "s16_timing_p4", 1.58)
    d.foot(s, "Three hold 0 and blip to 1. The THIRD panel, A = 1 and B = 0, is the case whose answer IS 1. It goes 0, 1, 0, 1: a dynamic hazard.")
    d.notes(s, "Computed, not tabulated by hand. Ask which case is worst "
               "before saying it: the dynamic one, because an actuator that "
               "fires, stops and fires again is worse than one that fires "
               "once.")

    s = d.light()
    d.header(s, "glitch-name", "The vocabulary")
    d.title(s, "Three ways to be transiently wrong")
    _fig(d, s, "s16_hazard_types", 1.74)
    d.rows(s, [
        ("named by what the output was SUPPOSED to do", "hold 0 and it blipped high — static-0. Hold 1 and it dropped — static-1. Change once and it changed three times — dynamic."),
        ("what they share", "a value the settled circuit never takes."),
    ], top=4.84)
    d.foot(s, "The names are borrowed from electronics. The consequence is not — a transistor that glitches does not kill anything.")
    d.notes(s, "Keep this brief; it is vocabulary, and PS6 asks them to name "
               "a kind. Do not dwell.")

    s = d.light()
    d.header(s, "glitch-release", "Your turn  ·  groups of 2–3")
    d.title(s, "Fill in a different circuit")
    d.rows(s, [
        ("on the sheet", "a two-input circuit with three genes, wired differently from the one above. Every gene starts at zero."),
        ("fill the table", "one row per tick, four ticks, every gene. Then say whether the output glitches — and if it does, which of the three kinds."),
        ("and say WHY", "one sentence. Not 'because it glitches'. What in the wiring let a wrong value out?"),
    ])
    d.foot(s, "The third question is the one on the problem set, and it is the one that is actually hard.")
    d.notes(s, "Circulate and listen for the explanation they reach for. Most "
               "groups will say unequal path lengths. That answer is coming "
               "up next and it is WRONG — do not correct it here, let them "
               "commit to it.")


# ---------------------------------------------------------------------------
# SEGMENT 4 — the wrong explanation, then the right one
# ---------------------------------------------------------------------------
def _wrong_then_right(d):
    s = d.light()
    d.header(s, "fix-wrong", "Debrief  ·  the obvious answer")
    d.title(s, "\"The two paths are different lengths\"")
    d.rows(s, [
        ("and they are", "A reaches the output in two gates. B reaches it in three, through R1. You wrote down the same thing about XNOR earlier."),
        ("so the fix is obvious", "pad the short path. Equalise them. Insert a gene."),
        ("let us check that", "take a circuit where the paths are already equal, and see whether it glitches."),
    ])
    d.foot(s, "This is the right instinct, it is the one electronics teaches, and on this circuit it is wrong.")
    d.notes(s, "Say explicitly that this is the answer most of the room "
               "reached, that it is reasonable, and that we are about to "
               "test it. The test is the lesson.")

    s = d.light()
    d.header(s, "fix-counterexample", "The test")
    d.title(s, "Balanced, and it glitches anyway")
    _fig(d, s, "s16_cold_start", 1.58)
    d.foot(s, "An empty cell is a cell with every inverter switched ON. The false ON is the gate's resting state, not the wiring.")
    d.notes(s, "Let the counterexample land before explaining it. Ask the "
               "room what NOR(0,0) is, then ask what every inverter is doing "
               "in a cell that has just been transformed.\n"
               "This is the correction, and it is worth more than the "
               "original explanation was.")

    s = d.light()
    d.header(s, "fix-activator", "The first repair, and why it fails")
    d.title(s, "Padding the path moves the glitch by one tick")
    d.rows(s, [
        ("the repair", "insert an activator between R2 and the output. Now both paths are one longer."),
        ("what happens", "the glitch arrives one tick later and is otherwise identical. Adding a stage to the SHARED tail changes both paths equally, so it changes nothing about their difference — and it does not touch the resting state at all."),
        ("the 2025 lecture's own verdict", "\"Hazard is simply delayed, we need a hybrid promoter.\""),
    ])
    d.foot(s, "A repair that treats the symptom you named rather than the cause you found.")
    d.notes(s, "Verified: the delayed circuit's hazard is the same kind, one "
               "tick later. Say that we checked rather than assumed.")

    s = d.light()
    d.header(s, "fix-before", "The repair that works  ·  before")
    d.title(s, "What we have: ON before anything arrives")
    _fig(d, s, "s16_timing_broken", 1.52)
    d.foot(s, "R3 is a NOT gate: with no repressor present it is expressed, and that is the first thing the output does.")
    d.notes(s, "Take the answer from the room before advancing. The answer "
               "is not in the wiring.")

    s = d.light()
    d.header(s, "fix-hybrid", "The repair that works  ·  after")
    d.title(s, "Make the output require an activator")
    _fig(d, s, "s16_timing_fixed", 1.52)
    d.foot(s, "Clean in all four cases. Two things changed at once, and the next slide separates them.")
    d.notes(s, "Both halves of the figure are computed. Point at the top row, "
               "then the bottom, and say the difference out loud: the broken "
               "output is a NOT, which is ON when empty; the fixed one needs "
               "an activator, so it is OFF when empty.")

    s = d.light()
    d.header(s, "fix-separate", "Debrief  ·  what actually changed")
    d.title(s, "Two things changed, so test them one at a time")
    _fig(d, s, "s16_two_conditions", 1.70)
    d.foot(s, "Every cell in that table is computed from the gate list, not asserted. The middle two rows are the counterexamples.")
    d.notes(s, "This slide exists because an earlier build of this session "
               "said 'fix the promoter, not the wiring', which is as wrong "
               "as the path-length diagnosis it was correcting. The hybrid "
               "repair changed BOTH: the output stopped being ON when empty, "
               "AND both legs became two gates deep.\n"
               "Row 2 is the cold-start circuit from earlier: balanced, and "
               "it glitches in three of four cases. Row 3 is the padded "
               "repair: OFF when empty, and it glitches in all four. Each "
               "condition alone is demonstrably not enough.\n"
               "Say plainly what this does and does not establish: the two "
               "together are enough HERE. The model has one gate delay "
               "everywhere, and that is doing work.")

    s = d.light()
    d.header(s, "fix-consequence", "Debrief  ·  what this is actually a rule about")
    d.title(s, "Fail-safe when empty, and arriving together")
    d.rows(s, [
        ("the engineering result", "when the output does something irreversible, two things must hold: the output must be OFF in a cell that has only just been made, and the signals that drive it must arrive at the same depth."),
        ("one is a promoter decision", "OFF when empty means the output needs an activator, not just the absence of a repressor. You cannot wire your way to it."),
        ("the other is a wiring decision", "equal path lengths. Necessary, and on its own worth nothing, which is the cold-start circuit two slides back."),
        ("and the honest limit", "this model gives every gate the same unit delay. Real promoters do not, and nothing in the model tells you which way unequal delays push the answer."),
    ])
    d.foot(s, "A classifier that fires while it is still booting has already killed the cell it was deciding about.")
    d.notes(s, "Land the therapeutic framing here, having set it up on the "
               "classifier slide. This is the surface that earns the segment "
               "and it is the one to protect if the hour runs short.")

    s = d.light()
    d.header(s, "hazard-regimes", "And where the path-length answer IS right")
    d.title(s, "Cello's paper has one of these in it")
    d.rows(s, [
        ("what they saw", "\"0x8E shows a transient incorrect state, known as a 'fault' in electronics, when the inputs are changed from \u2212/\u2212/\u2212 to +/\u2212/+\" (p. aac7341-9)."),
        ("their mechanism", "\"consistent with the last NOR gate transiently receiving ON/OFF inputs until one of the signals transits two layers.\" That is unequal path lengths, and here it is the right diagnosis."),
        ("so why was it wrong for us", "two regimes. Theirs is a settled circuit whose INPUTS changed. Ours is a circuit that has just been made, with nothing in it yet."),
        ("the rule, both halves", "for an input transition, equalise the paths. For a cold start, make the output require an activator. If the output is irreversible, you need both."),
    ])
    d.foot(s, "Same vocabulary, two different causes. Naming which regime you are in is most of the diagnosis.")
    d.notes(s, "This slide is the honest close to the segment. The "
               "electronics hazard taxonomy is defined for a transition in "
               "a settled circuit; we applied it to a power-on transient, "
               "which is a different regime and is why posb.logic's "
               "hazards() takes a `settle` argument at all.\n"
               "They read this paper. Ask whether anyone noticed that "
               "sentence; almost nobody will have, and that is a useful "
               "thing to notice about how one reads a paper.")


# ---------------------------------------------------------------------------
# SEGMENT 5 — cascade delay
# ---------------------------------------------------------------------------
def _cascade_delay(d):
    s = d.light()
    d.header(s, "delay-frame", "Frame  ·  three cascades you have already met")
    d.title(s, "One gene deep, two, three")
    d.paper_figure(s, "hooshangi2005_fig1", 1.52, 1.56, 10.30, 5.29,
                   "Hooshangi, Thiberge & Weiss, PNAS 102:3581 (2005), Fig. 1",
                   "Circuit 1: aTc relieves TetR and EYFP rises. Circuit 2 "
                   "adds LacI. Circuit 3 adds CI. Same input, same reporter, "
                   "one more repressor each time.")
    d.notes(s, "Session 13's paper, and the circuits are on the screen "
               "rather than described. Walk the three boxes and have the "
               "room count the repressors between aTc and EYFP: one, two, "
               "three.\n"
               "Then ask the question and leave it: if each stage costs the "
               "same, how much later is circuit 3 than circuit 1? We predict "
               "it first, then look at what they measured.")

    s = d.light()
    d.header(s, "delay-ask", "Frame  ·  the quantity")
    d.title(s, "How late is late? Put a number on it")
    d.rows(s, [
        ("the question", "a chain of n genes, each driving the next. A step at the input. How long until the output is halfway there?"),
        ("the convention", "session 10's, unchanged: the time for the output to reach 50% of its final value. We are not inventing a second definition."),
        ("the outcome", "a number, in protein lifetimes, that you can quote for any depth, and then compare against circuits 1, 2 and 3."),
    ])
    d.foot(s, "You measured a delay in session 10 and graded one on PS5. This is the same measurement on a chain.")
    d.notes(s, "Point back at PS5 Q2 explicitly. They own the convention "
               "already; this is a new object, not a new method.")

    s = d.light()
    d.header(s, "delay-build", "Worked")
    d.title(s, "One stage, one lifetime")
    _fig(d, s, "s16_cascade_delay", 1.62)
    d.foot(s, "Half-times of 0.693, 1.678 and 2.674 lifetimes for one, two and three stages. Each extra gene costs very nearly one τ.")
    d.notes(s, "The first number is ln2 and they should recognise it from "
               "session 5. The rest is that result compounded, and the right "
               "panel is the per-stage cost converging on one lifetime.")

    s = d.light()
    d.header(s, "delay-release", "Your turn  ·  thirty seconds")
    d.title(s, "Four stages, and a number")
    d.rows(s, [
        ("the circuit", "a four-gene chain, every protein with the same lifetime τ. A step at the input at t = 0."),
        ("estimate", "the half-time of the output, in units of τ, without computing the sum."),
        ("then say", "how much later that is than the three-gene chain, and whether you would have guessed that before this segment."),
    ])
    d.foot(s, "One number and one difference. Both are in your head already if you have the per-stage cost.")
    d.notes(s, "Answer: (4 − 1/3) τ = 3.667, against the exact 3.672. The "
               "difference from three stages is 0.998 τ, which is the point "
               "of the whole segment: one more gene, one more lifetime.\n"
               "Take the second half aloud. Most people underestimate depth "
               "because the first stage is fast.")

    s = d.light()
    d.header(s, "delay-rule", "Debrief  ·  the number to carry")
    d.title(s, "A cascade costs one protein lifetime per gene")
    d.rows(s, [
        ("the rule of thumb", "t½ ≈ (n − ⅓) τ, within 0.008 τ of the exact half-time from n = 3 on."),
        ("so, three genes", "a half-time of about 2.7 τ, which is about 2.0 τ later than a single stage. For a protein diluted by division rather than degraded, τ is the doubling time, so that is hours."),
        ("say which one you mean", "2.7 is the half-TIME and 2.0 is the DELAY against one stage. Two quantities, one segment, and the paper you are about to see uses a third definition again."),
        ("what to do with it", "a deep circuit is a slow circuit, and depth is set by the network you chose back on the XNOR slide. Two implementations, two delays."),
    ])
    d.foot(s, "This is the floor. Now look at what three real cascades actually did.")
    d.notes(s, "Close the loop to the XNOR comparison out loud: the "
               "six-gene network is one τ slower than the four-gene one, and "
               "that is what the extra stage buys you.\n"
               "The half-time / delay distinction is worth the row. An "
               "earlier build of this slide said 'about two and a half "
               "lifetimes late', which is neither quantity.")

    s = d.light()
    d.header(s, "delay-data", "Debrief  ·  what the three circuits did")
    d.title(s, "One more repressor each time")
    d.paper_figure(s, "hooshangi2005_fig3a", 4.30, 1.52, 4.75, 4.24,
                   "Hooshangi et al. (2005), Fig. 3A",
                   "aTc added at t = 0. Circuit 1 (○) rises and settles; "
                   "circuit 2 (+) falls, being one inversion further on; "
                   "circuit 3 (◆) sits flat for over two hours, then climbs.")
    d.foot(s, "Circuit 1 has settled by about 120 min. Circuit 3 does not settle until about 600 (p. 3583).")
    d.notes(s, "Have them read the three curves before you say anything. "
               "The + curve FALLING is worth a beat: circuit 2 has one more "
               "inversion, so the same input drives the reporter the other "
               "way. That is the complement from the first half of the hour, "
               "in a real measurement.\n"
               "Compare settling with settling, 120 against 600. Circuit 3 "
               "also has not begun to move at 140 min, which is the more "
               "vivid number, but it is a different event and saying so "
               "matters.")

    s = d.light()
    d.header(s, "delay-debrief", "Debrief  ·  against the measurement")
    d.title(s, "The real ones are slower, and the paper says why")
    d.rows(s, [
        ("what we predicted", "about one protein lifetime per stage, so two extra stages cost about two lifetimes."),
        ("what they measured", "circuit 1 settled by about 120 min and circuit 3 by about 600, for two extra stages (p. 3583). Not two lifetimes; many."),
        ("their explanation", "the delay carries \"protein decay, protein production, and repression thresholds\" (p. 3585). Circuit 3 moves only once enough LacI exists to shut off CI AND the CI already there has been diluted away."),
        ("and a third convention", "their half-time is the crossing of the geometric mean on a log scale (p. 3583). Ours is 50% of the final value. Two reasonable definitions, two different numbers."),
    ])
    d.foot(s, "Our model has no threshold in it. It is a floor on the delay, not an estimate of it.")
    d.notes(s, "This is the gap between a clean result and a measurement, "
               "which is the most useful thing in the segment. Do not skip "
               "it.\n"
               "If someone asks for delay against depth: that is Fig. 3C, "
               "and it is the SIMULATED system rather than the measured one. "
               "Say so if you put it up.")


# ---------------------------------------------------------------------------
# SEGMENT 6 — Cello
# ---------------------------------------------------------------------------
def _cello(d):
    s = d.light()
    d.header(s, "cello-assign", "The step you have not done")
    d.title(s, "Assignment: which repressor goes in which socket")
    d.paper_figure(s, "nielsen2016_fig2a", 1.90, 1.60, 9.54, 4.30,
                   "Nielsen et al. (2016), Fig. 2A",
                   "Three circuits, each as a NOR/NOT diagram with its gates "
                   "coloured by the repressor assigned to them, and as the "
                   "DNA that assignment produces.")
    d.foot(s, "Recolour the diagram and the logic is unchanged. The DNA is not, and neither is whether it works.")
    d.notes(s, "One sentence: the shapes on the left are the logic, which "
               "you can now derive; the colours are the assignment, which "
               "you cannot, because it depends on measured properties of "
               "real repressors.\n"
               "Point at the purple boxes. A gate used twice in one circuit "
               "is the same repressor twice, and that is a constraint rather "
               "than a convenience.")

    s = d.light()
    d.header(s, "cello-frame", "Back to the question we left open")
    d.title(s, "45 of 60. Where did the missing quarter go?")
    d.rows(s, [
        ("what you have just built by hand", "a gate out of a promoter and two operators, and a network out of those gates. Cello does both steps for you."),
        ("what it does next, which you have not", "picks WHICH repressor goes in each NOR socket, out of a library, and predicts how well that assignment will work."),
        ("so the candidates", "the compiler is wrong, the gate models are wrong, the DNA was built wrong, or the gates interfere with one another."),
    ])
    d.foot(s, "Every one of the sixty was built. Three quarters of them were right in every state.")
    d.notes(s, "Do not re-walk Fig. 1A; it was on the screen at the top of "
               "the hour. Spend the time on the score and on 45/60.")

    s = d.light()
    d.header(s, "cello-score", "Their criterion, in your units")
    d.title(s, "The circuit score is a noise margin written as a ratio")
    d.rows(s, [
        ("their definition", "the score S is \"the ratio of the lowest predicted ON state to the highest predicted OFF state\" (Fig. 2 caption, p. aac7341-3)."),
        ("yours, from session 13", "a margin is the gap between what the sender puts out and what the receiver needs. In logs a difference; in linear units a ratio."),
        ("so it is one quantity under two names", "S > 1 is your margin being positive. S >> 1 is a circuit you would trust in a patient."),
        ("and watch the paper", "Fig. 5 scores the same letter from measured MEDIANS rather than predictions (caption, p. aac7341-9). Same symbol, two definitions."),
    ])
    d.foot(s, "You computed this in session 13 on two of their own gates, out of their Table S4.")
    d.notes(s, "The point is that they already own Cello's scoring rule "
               "under a different name. Ask which session 13 quantity it is "
               "before revealing it.\n"
               "The two definitions are a real feature of the paper. A "
               "predicted score is what the compiler optimises; a measured "
               "one is what you grade it on. Say which you mean each time "
               "you say S.")

    s = d.light()
    d.header(s, "cello-search", "What the compiler spends its time on")
    d.title(s, "Simulated annealing over assignments")
    d.paper_figure(s, "nielsen2016_fig2e", 3.00, 1.58, 7.30, 3.79,
                   "Nielsen et al. (2016), Fig. 2E",
                   "Circuit score against iteration, climbing in steps from "
                   "near zero to about 345 over roughly 11,000 tries. Both "
                   "insets are the SAME topology under different "
                   "assignments.")
    d.foot(s, "The bars beside each inset are the predicted ON and OFF levels: jumbled on the left, separated on the right.")
    d.notes(s, "This is the optimizer. Say what it searches over: not the "
               "logic, which is fixed by now, but which repressor sits in "
               "which socket.\n"
               "The score climbing in steps is simulated annealing accepting "
               "an improvement. About 11,000 iterations for this one, which "
               "is the honest answer to 'why is there a search algorithm "
               "inside a compiler at all'.")

    s = d.light()
    d.header(s, "cello-search-live", "The same search, running")
    d.title(s, "Watch an assignment get better")
    d.paper_movie(s, "der2016_cello_hillclimb", 1.55, 1.42, 10.20, 4.92,
                  "Bryan Der, Voigt lab; from PoSB 2025 Lecture 18",
                  "Hill climbing over assignments for a three-input XOR: "
                  "the repressor database, the circuit, the best score so "
                  "far, and the predicted ON and OFF level of all eight "
                  "states.")
    d.notes(s, "Play it twice. First time, tell them to watch only the "
               "bottom right: eight bars, one per input state, and at the "
               "start they are all at much the same height, which is a "
               "circuit that computes nothing.\n"
               "Second time, watch the circuit. The colours are the "
               "assignment changing, and the database on the left is what "
               "they are being drawn from.\n"
               "Then the score panel: it only ever goes up, because it keeps "
               "the best so far. About 250 iterations here.\n"
               "This is Bryan Der's animation from the Voigt lab, and it is "
               "the same search that produced Fig. 2E on the slide before.")

    s = d.light()
    d.header(s, "cello-release", "Your turn  ·  thirty seconds, no paper")
    d.title(s, "Commit to one of the four")
    d.rows(s, [
        ("pick one", "compiler wrong / gate models wrong / DNA built wrong / gates interfere with one another."),
        ("defend it in a sentence", "you have the paper's own numbers. All 60 were built, and 92% of individual output states were right."),
    ])
    d.foot(s, "There is a defensible answer, the paper's own answer, and an answer about the field. They are not the same answer.")
    d.notes(s, "Take three answers and put them on the board before "
               "advancing. 92% of states right but only 75% of circuits "
               "right is the clue, and someone usually spots that a circuit "
               "needs EVERY state to be right.\n"
               "Be straight about the next two slides: the PAPER's own "
               "failure analysis blames particular parts, and the argument "
               "about the library is mine on top of it.")

    s = d.light()
    d.header(s, "cello-data", "The measurement behind 45 of 60")
    d.title(s, "Failures climb with the size of the repressor set")
    d.paper_figure(s, "nielsen2016_fig5a", 4.17, 1.58, 5.00, 4.27,
                   "Nielsen et al. (2016), Fig. 5A",
                   "Fraction correct against the number of repressors: "
                   "output STATES fall only from about 0.97 to about 0.86, "
                   "while whole CIRCUITS fall from about 1.0 to about 0.4.")
    d.foot(s, "States hold up. Circuits do not, because a circuit is correct only if every one of its states is.")
    d.notes(s, "Read the two curves separately. The upper one says each "
               "individual output state is almost as reliable however big "
               "the circuit is. The lower one is that per-state reliability "
               "raised to the number of states.\n"
               "The paper's own words for it: 'As more gates were included "
               "in a design, there was a higher probability of failure' "
               "(p. aac7341-9).")

    s = d.light()
    d.header(s, "cello-why", "Whose fault, according to the authors")
    d.title(s, "The paper blames particular parts, not the method")
    d.rows(s, [
        ("what they found", "\"most of the circuit failures point to unexpected behavior from the anhydrotetracycline (aTc) sensor (seven circuits) or AmtR gate (two circuits)\", plus two circuits that impaired growth (p. aac7341-9)."),
        ("so, of your four", "the paper's own verdict is closest to 'the gate models are wrong': the parts did not behave in context the way they behaved in isolation."),
        ("what that does NOT say", "nothing in the failure analysis blames crosstalk between repressors. If you picked interference, you picked an argument the paper does not make here."),
        ("the honest shape", "nine of fifteen failures are two named parts. Fix those two and the method looks very good indeed."),
    ])
    d.foot(s, "Which is a better result for Cello than 45 of 60 sounds, and a worse one for anybody wanting a general rule.")
    d.notes(s, "This slide exists because the first build of this segment "
               "taught orthogonality as 'the best answer' to the release, "
               "and the paper says something else. Give them the paper's "
               "answer first and label the next one as mine.")

    s = d.light()
    d.header(s, "cello-matrix", "And the constraint behind all of it")
    d.title(s, "Every gate has to not interfere with every other gate")
    d.paper_figure(s, "nielsen2016_fig2c", 2.55, 1.54, 8.20, 5.30,
                   "Nielsen et al. (2016), Fig. 2C",
                   "For each ordered pair of gates, the fold-change gate A "
                   "leaves for gate B, in position 1 (left) and position 2 "
                   "(right). Black is a pair excluded by roadblocking.")
    d.notes(s, "Read the left panel first: bright is a pair that connects, "
               "dark is a pair that barely does. Then the right panel, which "
               "is the same library in the SECOND position behind another "
               "gate, and most of it is black.\n"
               "This is not the paper's explanation of the 15 failures. It "
               "is the reason the library cannot simply be made bigger, and "
               "it is the bridge to Thursday. Adding a gate adds a row AND a "
               "column, and both have to work.")

    s = d.light()
    d.header(s, "cello-debrief", "Debrief")
    d.title(s, "The architecture is fine. The parts list is the problem.")
    d.rows(s, [
        ("what Cello proves", "you can compile a specification to DNA and have it work most of the time, at a scale nobody reaches by hand: 60 circuits, 880 kb."),
        ("what the paper blames", "two misbehaving parts, an aTc sensor and the AmtR gate, for most of the failures. Part characterisation, not compilation."),
        ("what limits the next circuit", "the size of the library. Each new gate must not interfere with any gate already in the circuit, in either position, and that constraint tightens as the set grows."),
        ("Thursday", "where a usable part actually comes from, and how many candidates die on the way."),
    ])
    d.foot(s, "Hold that. The memory half of today arrives at the same place from the other end.")
    d.notes(s, "This is the hinge of the session. The second half reaches "
               "the identical conclusion from recombinases, and the rhyme is "
               "the point.\n"
               "Keep the two claims separate out loud: the paper's failure "
               "analysis is about particular parts, and the library-size "
               "argument is the field-level claim built on Fig. 2C.")


# ---------------------------------------------------------------------------
# SEGMENT 7 — the latch
# ---------------------------------------------------------------------------
def _latch(d):
    s = d.light()
    d.header(s, "latch-frame", "Frame  ·  the second half")
    d.title(s, "Output that depends on what happened earlier")
    d.rows(s, [
        ("combinational", "inputs in, output out. Everything so far today."),
        ("sequential", "the same inputs can give different outputs, because the circuit remembers. That requires a state, and a state requires something physical to hold it."),
        ("the outcome", "two ways to hold a bit, and an argument about where a bit should live."),
    ])
    d.foot(s, "You have already built one of the two. You were not told what it was called.")
    d.notes(s, "Set up the reveal rather than stepping on it.")

    s = d.light()
    d.header(s, "latch-circuit", "Worked  ·  the circuit, and the two letters")
    d.title(s, "Two NOR genes, each repressing the other")
    _fig(d, s, "s16_sr_circuit", 1.56)
    d.foot(s, "No clock anywhere. The state is held because each gene keeps the other one off.")
    d.notes(s, "Build it at the board before showing the table. Gene Q is a "
               "NOR of R and of the other gene's product; gene ¬Q is a NOR "
               "of S and of Q. That is the whole circuit.\n"
               "Then walk one case: S goes to 1, so ¬Q is repressed and "
               "falls; with ¬Q gone, nothing is repressing Q, so Q rises; "
               "Q now holds ¬Q down even after S goes away. That last "
               "clause is the memory, and it is worth saying twice.\n"
               "S = R = 1 is worth naming as forbidden rather than skipping. "
               "It is the standard answer to 'what if both?' and the reason "
               "real designs gate the inputs.\n"
               "This is session 9's toggle with the inducers renamed. Say so "
               "only AFTER they have agreed it is a memory, so the renaming "
               "lands as a recognition rather than a definition.")

    s = d.light()
    d.header(s, "latch-rename", "Worked  ·  a renaming, not a derivation")
    d.title(s, "Session 9's toggle IS an SR latch")
    _fig(d, s, "s16_latch_state_table", 1.52)
    d.foot(s, "SET and RESET are the inducer pulses you analysed on PS4. Both Q and Q̄ read 0 for one tick mid-switch. Ask whether that is the cell or the clock.")
    d.notes(s, "Say 'you built this five weeks ago' and mean it. This segment "
               "is deliberately cheap, and it is the slack in the hour.\n"
               "Worth pointing at: during SET and RESET both Q and Q-bar are "
               "0 for one tick. Whether a cell ever "
               "does that is a question about the clock: "
               "this model updates both gates in the same "
               "tick, and updating them one at a time "
               "removes the zero. Worth asking the room "
               "which they believe, and saying that the "
               "model does not settle it.")

    s = d.light()
    d.header(s, "latch-scale", "What people have built with it")
    d.title(s, "Latches, registers, and the same attrition again")
    d.rows(s, [
        ("one bit", "an SR latch in cells, measured in RPU — the same units as session 13's transfer curves."),
        ("how many worked", "most of the designed latches were functional, and the ones that were not failed for the same reason Cello's did."),
        ("more than one bit", "parallel latches and resettable registers; a gated D latch that only records when a clock line says to."),
        ("the cost", "every independent bit needs its own orthogonal pair. The same ceiling as Cello, reached from the other side."),
    ])
    d.foot(s, "Different labs, different decades, the same bottleneck: how many parts you have that do not interfere.")
    d.notes(s, "The 31-of-41 figure that used to be on this slide came "
               "off the 2025 deck with no paper named, and nothing in "
               "private/readings supports it. Cut rather than taught "
               "unverified. If you can name the source — Andrews, Roehner "
               "& Voigt, Science 2018 is the likely one — put the number "
               "back, because it is a better slide with it.")


# ---------------------------------------------------------------------------
# SEGMENT 8 — memory in DNA
# ---------------------------------------------------------------------------
def _dna_memory(d):
    s = d.light()
    d.header(s, "dna-frame", "Frame  ·  where should a bit live?")
    d.title(s, "A protein latch dies with the cell")
    d.rows(s, [
        ("what the latch costs to HOLD", "continuous expression of two repressors, for as long as you want to remember. Stop, and the memory evaporates."),
        ("the alternative", "store the bit in the DNA sequence itself — flip a segment over. Nothing has to be expressed to hold it, and it survives the cell."),
        ("the machine", "an invertase: an enzyme that reverses the stretch of DNA between two sites it recognises."),
    ])
    d.foot(s, "Volatile against non-volatile, and in a cell the distinction is not academic.")
    d.notes(s, "Make the energy point: a transcriptional latch is a bit you "
               "pay rent on. DNA orientation is a bit you buy outright.")

    s = d.light()
    d.header(s, "dna-inversion", "What the machine actually does")
    d.title(s, "An inversion, and where you put the sites")
    _fig(d, s, "s16_inversion", 1.58)
    d.notes(s, "Nobody can follow the state graph on the next slide without "
               "this one. Three things to say at the board:\n"
               "One: the two sites of a pair point AT each other. That is "
               "what makes an inversion rather than an excision, and it is "
               "why the flipped segment comes back with its sites still "
               "facing inward, so it can flip again.\n"
               "Two: what inverts is everything between them, including the "
               "direction of the gene. A promoter pointing out of the "
               "segment now points into it. That is the whole mechanism of "
               "the 'readout by action' idea later.\n"
               "Three: with two pairs you have a choice. Nested means one "
               "pair lies entirely inside the other; staggered means they "
               "interleave. Ask for a prediction about which gives more "
               "states before the next slides answer it.")

    s = d.light()
    d.header(s, "dna-ham", "Worked  ·  the first one")
    d.title(s, "Two invertases, and the ORDER of the inputs")
    _fig(d, s, "s16_dirs_states", 1.7)
    d.rows(s, [
        ("why this is sequential logic", "states 3 and 4 use the same two inputs, and differ only in which arrived first. Memory of ORDER, with no protein holding it."),
    ], top=5.85)
    d.foot(s, "Ham, Lee, Keasling & Arkin, PLoS ONE 2008. About 1 kb, and the state is the sequence.")
    d.notes(s, "This is mine, with Tim Ham — say so. It predates the "
               "better-known recombinase memory work by several years.\n"
               "The dashed node is the honest part: state 3 was predicted and "
               "never observed. The fim arm barely inverted, and of 50 "
               "isolates sequenced none carried it. A proof of principle that "
               "says so.")

    s = d.light()
    d.header(s, "dna-theory", "The power, and where it comes from")
    d.title(s, "Staggered sites, not nested ones")
    d.rows(s, [
        ("independent, or NESTED", "n invertases, n bits, 2^{n} states. Two invertases with one pair of sites fully inside the other give \"only four\" (Ham, Fig. 1B). A register, and nothing more."),
        ("STAGGERED sites", "the inversions stop commuting, so the ORDER they fired in becomes part of the state. Two staggered invertases give five, \"and any input sequence results in a different output\" (Fig. 1C)."),
        ("so predict", "nesting looks as though it must create interaction, since one inversion carries the other's sites bodily with it. It buys nothing. Overlap is what matters."),
    ])
    d.foot(s, "Ask for the prediction on nesting before you reveal it. Almost everyone gets it wrong, and it is the useful kind of wrong.")
    d.notes(s, "Draw the two layouts on the board: sites ABba against sites "
               "ABab. Then ask which one gives more states before showing "
               "Ham's answer.")

    s = d.light()
    d.header(s, "dna-count", "How many states, exactly")
    d.title(s, "Count the orders, not the bits")
    d.rows(s, [
        ("what a state records", "which invertases have fired, and in what order. So a state is an ordered sequence drawn from a subset of the n available."),
        ("so count those", "S(n) = Σ k!·C(n,k) over the non-empty subsets, which is Ham's own formula. Two staggered give 4 beyond the start, so five in all: the graph you just saw."),
        ("and it runs away", "15 at three invertases against 8 for a register. At ten, \"nearly 10⁷\" (Fig. 1E) against 1 024."),
        ("what nature does with it", "the R64 shufflon: ONE invertase, Rci, four DNA segments, seven recognition sites. Combinatorial surface variants off a single enzyme."),
    ])
    d.foot(s, "A register pays one orthogonal enzyme per bit. A shufflon pays one enzyme, full stop.")
    d.notes(s, "Derive S(n) at the board rather than quoting it; it is three "
               "lines. Choose a non-empty subset of the invertases that have "
               "fired, C(n,k) ways, then an order for them, k! ways, and sum "
               "over k.\n"
               "Ham's Fig. 1E plots TWO curves and they are different "
               "quantities: the blue one is how many ways the sites can be "
               "ARRANGED, past 10^10 at ten invertases, and the red one is "
               "the state space of one arrangement, nearly 10^7. Do not "
               "quote one for the other.\n"
               "An earlier build of this slide carried our own orbit "
               "enumeration instead, which gives 1 024 at three invertases "
               "against the paper's 15. That model lets an invertase fire "
               "again after another has moved its sites, which Ham's count "
               "does not. It is an open question, not a result, and it is "
               "parked in DESIGN.md 8.5.")

    s = d.light()
    d.header(s, "dna-fork", "Debrief  ·  two roads, and the field took one")
    d.title(s, "A bit you read, or a program you run")
    d.rows(s, [
        ("the register road", "unidirectional integrases, which flip once and stay. 34 found in prophage genomes, 13 chosen to be at most 60% identical and built, 11 of those perfectly orthogonal: 2¹¹ states, 1.375 bytes. Readout by sequencing. This is where the field went."),
        ("the program road", "place promoters, terminators and genes so that each arrangement IS a working transcription unit. Then you do not read the state — you run it, and selection does the reading."),
        ("which is Ham's idea", "the second. And it is the one still open."),
        ("the same ceiling", "11 of the 13 they tested were orthogonal, so the parts were good. The limit is that you need EVERY pair to be orthogonal, which is Cello's constraint arriving from the opposite direction."),
    ])
    d.foot(s, "The compact state space is real, and it was never going to be read. It was going to be selected on.")
    d.notes(s, "Close the rhyme explicitly: both halves of this session end "
               "at the orthogonal parts set.\n"
               "Modern note if there is room: a 2025 toolkit paper found 14 "
               "new shufflon invertases and orthogonal site pairs, aiming at "
               "millions of variants in vivo — for barcoding and selection, "
               "which is the right-hand column.")


# ---------------------------------------------------------------------------
def _close(d):
    s = d.light()
    d.header(s, "close", "Where this leaves us")
    d.title(s, "Both halves ran out of the same thing")
    d.rows(s, [
        ("combinational", "the compiler works, on all 60. The paper's own failures are two misbehaving parts, and the ceiling beyond them is how many gates do not interfere."),
        ("sequential", "DNA memory works. 11 integrases that are orthogonal to each other and to the two host invertases, and every new bit has to be orthogonal to all of them."),
        ("so Thursday", "what a part actually is, where one comes from, and why its number changes when you move it."),
    ])
    d.foot(s, "Neither half of this hour was stopped by the architecture. Both were stopped by the parts list.")
    d.notes(s, "One sentence, then the reading. The two halves rhyme on "
               "parts, not on the design method, and that is the thing to "
               "leave in the room.")

    s = d.light()
    d.header(s, "reading", "For Thursday")
    d.title(s, "The reading for 22 October")
    d.assignment(s, y=2.30, label="For Thursday 22 October")
    d.text(s, "A part is a measurement, not a name. This is the version with a "
              "model underneath it rather than a regression — which is the bar "
              "every reading on this course has to clear.",
           M, 5.30, W - 2 * M, 0.9, size=17, color=MUTED, spacing=1.2)
    d.notes(s, "Say that it is mine, with Mutalik, Carothers and Endy. Chen "
               "2013 and Stanton 2014 are optional and both are worth the "
               "time — the catalogue and the mining.\n"
               "M2 is due Thursday: Specific Aims and the model.")
