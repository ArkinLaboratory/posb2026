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
    d.foot(s, "All three come back within the hour. The first one comes back in Boolean, about fifteen minutes from now.")
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
        ("what Cello did", "60 circuits designed from Verilog and all 60 built with no additional tuning, up to 10 regulators and 55 parts, 880 kb of DNA (p. 1)."),
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
    d.foot(s, "Say 'once everything has settled' out loud. We collect on that phrase in twenty minutes.")
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
    d.header(s, "nor-library", "The free gate library")
    d.title(s, "One operator is an inverter, two is a NOR, and that is all you need")
    d.rows(s, [
        ("one operator on a promoter", "out = NOT in. The complement, for the price of cloning an operator site."),
        ("two operators on a promoter", "out = NOT (in₁ OR in₂). Complement and aggregator in one piece of DNA, which is why NOR alone is universal."),
        ("compiling any table", "one term per row where the output is 1, then DeMorgan twice: every AND of literals becomes a NOR of their complements."),
        ("what it costs", "depth. Each layer is another gene, and a gene is a delay. Hold that thought for fifteen minutes."),
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
    d.header(s, "nor-debrief", "Debrief")
    d.title(s, "Three genes on one path, two on the other")
    d.rows(s, [
        ("the network", "¬A and ¬B as inverters; NOR(A, B) and NOR(¬A, ¬B) as the two agreement terms; then a NOR of those two, then an inverter."),
        ("the depths", "three gates on the longest path from an input to the output, two on the shortest."),
        ("write that down", "the paths are not the same length. In twenty minutes that stops being a curiosity."),
    ])
    d.foot(s, "Unequal path lengths, on the board before anyone has said why they matter.")
    d.notes(s, "PLANT THIS and do not explain it. The hazard segment collects "
               "on this line, and the collection is much stronger if they "
               "wrote the two numbers down themselves first.")


# ---------------------------------------------------------------------------
# SEGMENT 2 — the classifier
# ---------------------------------------------------------------------------
def _classifier(d):
    s = d.light()
    d.header(s, "clf-frame", "Frame  ·  a real design problem")
    d.title(s, "Detect one cell type, and only that one")
    _fig(d, s, "s16_classifier", 1.58)
    d.foot(s, "R2 is one gene read by two independently repressed promoters \u2014 NAND. In the therapy this is cloned from, the output kills the cell.")
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
    d.foot(s, "Three hold 0 and blip to 1. The fourth \u2014 the case whose answer IS 1 \u2014 goes 0, 1, 0, 1: a dynamic hazard.")
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
        ("and they are", "A reaches the output in two gates. B reaches it in three, through R1. You wrote down the same thing about XNOR twenty minutes ago."),
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
    d.foot(s, "Clean in all four cases, and not because the wiring changed. Because the resting state did.")
    d.notes(s, "Both halves of the figure are computed. Point at the top row, "
               "then the bottom, and say the difference out loud: the broken "
               "output is a NOT, which is ON when empty; the fixed one needs "
               "an activator, so it is OFF when empty.")

    s = d.light()
    d.header(s, "fix-consequence", "Debrief  ·  what this is actually a rule about")
    d.title(s, "The fail-safe state must be the empty state")
    d.rows(s, [
        ("the engineering result", "when the output does something irreversible, design it so the circuit cannot assert it while it is still filling. That is a promoter architecture decision, not a wiring decision."),
        ("what would still break it", "if activation and repression have different dynamics, the hybrid promoter is only as good as the matching. Faster activation than repression and the glitch returns."),
        ("and the honest limit", "this model gives every gate the same unit delay. Real promoters do not. Unequal delays make it worse, never better."),
    ])
    d.foot(s, "A classifier that fires while it is still booting has already killed the cell it was deciding about.")
    d.notes(s, "Land the therapeutic framing here, having set it up on the "
               "classifier slide. This is the surface that earns the segment "
               "and it is the one to protect if the hour runs short.")


# ---------------------------------------------------------------------------
# SEGMENT 5 — cascade delay
# ---------------------------------------------------------------------------
def _cascade_delay(d):
    s = d.light()
    d.header(s, "delay-frame", "Frame")
    d.title(s, "How late is late? Put a number on it")
    d.rows(s, [
        ("the question", "a chain of n genes, each driving the next. A step at the input. How long until the output is halfway there?"),
        ("the convention", "session 10's, unchanged — the time for the output to reach 50% of its final value. We are not inventing a second definition."),
        ("the outcome", "a number, in protein lifetimes, that you can quote for any depth."),
    ])
    d.foot(s, "You measured a delay in session 10 and graded one on PS5. This is the same measurement on a chain.")
    d.notes(s, "Point back at PS5 Q2 explicitly. They own the convention "
               "already; this is a new object, not a new method.")

    s = d.light()
    d.header(s, "delay-build", "Worked")
    d.title(s, "One stage, one lifetime")
    _fig(d, s, "s16_cascade_delay", 1.7)
    d.rows(s, [
        ("the numbers", "0.693, 1.678, 2.674 lifetimes for one, two, three stages — nearly one lifetime each."),
        ("the rule of thumb", "t½ ≈ (n − ⅓) τ, good to 0.008 by n = 3."),
    ], top=5.06)
    d.foot(s, "A three-gene cascade is about two and a half lifetimes late. For a protein diluted by division, that is hours.")
    d.notes(s, "The first number is ln2 and they should recognise it from "
               "session 5. The rest is that result compounded.")

    s = d.light()
    d.header(s, "delay-debrief", "Debrief  ·  against the measurement")
    d.title(s, "The real cascades are slower than that, and the paper says why")
    d.rows(s, [
        ("what we predicted", "about one lifetime per stage."),
        ("what Hooshangi measured", "circuit 1 settles by about 120 min; circuit 3 — two stages deeper — does not START until about 140. Much more than two lifetimes of difference."),
        ("their explanation", "the delay also carries \"protein decay, protein production, and repression thresholds\" (p. 3585). A repressor has to clear a THRESHOLD before the next stage moves at all, and our model has no threshold in it."),
        ("and a convention trap", "their half-time is the geometric mean on a log scale (p. 3583), not ours. Two reasonable definitions, different numbers."),
    ])
    d.foot(s, "The model is the floor, not the estimate. Everything real adds to it.")
    d.notes(s, "This is a debrief about the gap between a clean result and a "
               "measurement, which is the most useful thing in the segment. "
               "Do not skip it to save time.")


# ---------------------------------------------------------------------------
# SEGMENT 6 — Cello
# ---------------------------------------------------------------------------
def _cello(d):
    s = d.light()
    d.header(s, "cello-frame", "Back to the question we left open")
    d.title(s, "45 of 60. Whose fault is the missing quarter?")
    d.rows(s, [
        ("what you have just built by hand", "a gate out of a promoter and two operators, and a network out of those gates. Cello does both steps for you."),
        ("what it does next, which you have not", "picks WHICH repressor goes in each NOR socket, out of a library, and predicts how well that assignment will work."),
        ("so the candidates", "the compiler is wrong, the gate models are wrong, the DNA was built wrong, or the gates are not orthogonal enough."),
    ])
    d.foot(s, "Every one of the sixty was built. Three quarters of them were right in every state. Where did the quarter go?")
    d.notes(s, "Do not re-walk Fig. 1A; it was on the screen at the top of "
               "the hour. Spend the time on the score and on 45/60.")

    s = d.light()
    d.header(s, "cello-score", "Their criterion, in your units")
    d.title(s, "The circuit score is a noise margin written as a ratio")
    d.rows(s, [
        ("their definition", "the score S is “the ratio of the lowest predicted ON state to the highest predicted OFF state” (Fig. 2 caption, p. 4)."),
        ("yours, from session 13", "a margin is the gap between what the sender puts out and what the receiver needs. In logs a difference; in linear units a ratio."),
        ("so it is one quantity under two names", "S > 1 is your margin being positive. S >> 1 is a circuit you would trust in a patient."),
        ("watch the paper here", "Fig. 5 scores the SAME letter from measured medians, not predictions (caption, p. 10). Quote whichever matches the context and say which."),
    ])
    d.foot(s, "You computed this in session 13 on two of their own gates, out of their Table S4.")
    d.notes(s, "The point is that they already own Cello's scoring rule under "
               "a different name. Ask which session 13 quantity it is before "
               "revealing it.\n"
               "The two definitions are a real feature of the paper, not a "
               "typo. Worth one sentence: a predicted score is what the "
               "compiler optimises, a measured one is what you grade it on.")

    s = d.light()
    d.header(s, "cello-release", "Your turn  ·  thirty seconds, no paper")
    d.title(s, "Commit to one of the four")
    d.rows(s, [
        ("pick one", "compiler wrong / gate models wrong / DNA built wrong / gates not orthogonal enough."),
        ("defend it in a sentence", "you have the paper's own numbers. All 60 were built, and 92% of individual output states were right."),
    ])
    d.foot(s, "There is a defensible answer and there is a best answer. The next slide is the data.")
    d.notes(s, "Take three answers and write them on the board before "
               "advancing. 92% of states right but only 75% of circuits "
               "right is the clue, and someone usually spots that a circuit "
               "needs EVERY state to be right.")

    s = d.light()
    d.header(s, "cello-data", "The measurement behind 45 of 60")
    d.title(s, "Failures climb with the size of the repressor set")
    d.paper_figure(s, "nielsen2016_fig5a", 4.17, 1.58, 5.00, 4.27,
                   "Nielsen et al. (2016), Fig. 5A",
                   "Fraction correct against the number of repressors: "
                   "output STATES stay near 0.85, whole CIRCUITS fall from "
                   "1.0 to about 0.4 by seven repressors.")
    d.foot(s, "States hold up. Circuits do not, because a circuit is correct only if every one of its states is.")
    d.notes(s, "Read the two curves separately. The flat one says each "
               "individual gate is roughly as reliable however big the "
               "circuit is. The falling one is the product of those "
               "probabilities over more and more states.\n"
               "So the answer to the release is orthogonality: every gate "
               "added has to not interfere with every gate already there. "
               "Thursday's reading is where the library comes from.")

    s = d.light()
    d.header(s, "cello-debrief", "Debrief")
    d.title(s, "The architecture is fine. The parts list runs out.")
    d.rows(s, [
        ("what Cello proves", "you can compile a specification to DNA and have it work most of the time, at a scale nobody reaches by hand: 60 circuits, 880 kb."),
        ("what limits it", "the number of mutually orthogonal repressors. Each new gate must not interfere with any gate already there, and that constraint tightens quadratically."),
        ("why design automation plateaued", "not because the compiler stopped improving. Because the library stopped growing."),
        ("Thursday", "where a usable part actually comes from, and how many candidates die on the way."),
    ])
    d.foot(s, "Hold that sentence. The memory half of today arrives at it again, from the other end.")
    d.notes(s, "This is the hinge of the session. Say the sentence slowly. "
               "The second half reaches the identical conclusion from "
               "recombinases, and the rhyme is the point.")


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
    d.header(s, "latch-rename", "Worked  ·  a renaming, not a derivation")
    d.title(s, "Session 9's toggle IS an SR latch")
    _fig(d, s, "s16_latch_state_table", 1.52)
    d.foot(s, "SET and RESET are the inducer pulses you analysed on PS4. Both Q and Q̄ are briefly 0 mid-switch \u2014 that is real.")
    d.notes(s, "Say 'you built this five weeks ago' and mean it. This segment "
               "is deliberately cheap, and it is the slack in the hour.\n"
               "Worth pointing at: during SET and RESET both Q and Q-bar are "
               "briefly 0. That is real, not an artifact of the model.")

    s = d.light()
    d.header(s, "latch-scale", "What people have built with it")
    d.title(s, "Latches, registers, and the same attrition again")
    d.rows(s, [
        ("one bit", "an SR latch in cells, measured in RPU — the same units as session 13's transfer curves."),
        ("how many worked", "31 of 41 designed latches were functional."),
        ("more than one bit", "parallel latches and resettable registers; a gated D latch that only records when a clock line says to."),
        ("the cost", "every independent bit needs its own orthogonal pair. The same ceiling as Cello, reached from the other side."),
    ])
    d.foot(s, "31 of 41, and 45 of 60. Different labs, different decades, same bottleneck.")
    d.notes(s, "[unverified: the 31/41 figure is read off the 2025 deck and "
               "its source paper is not named on the slide — check before "
               "this is taught, or cut the number and keep the shape.]")


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
    d.title(s, "Overlapping sites, not nested ones")
    d.rows(s, [
        ("independent segments", "n invertases, n bits, 2^{n} states. A register, and nothing more."),
        ("NESTED segments", "also exactly 2^{n}. It looks as though one inversion carrying another's sites should create interaction. It does not."),
        ("OVERLAPPING segments", "the inversions stop commuting, so the order they fire in is part of the answer — and the count explodes: 1 024 states from three invertases against 8, and nearly a million from six against 64."),
        ("what nature does", "the R64 shufflon: ONE invertase, Rci, four DNA segments, seven recognition sites — combinatorial surface variants off a single enzyme."),
    ])
    d.foot(s, "A register pays one orthogonal enzyme per bit. A shufflon pays one enzyme, full stop.")
    d.notes(s, "The nested result is the surprise and it is worth asking for "
               "a prediction before revealing.\n"
               "These counts are OUR enumeration, written for this session — "
               "Ham's paper states nearly 10^7 for a ten-input device under "
               "its own definition of a state. Present them as a model, not "
               "as the paper's numbers.")

    s = d.light()
    d.header(s, "dna-fork", "Debrief  ·  two roads, and the field took one")
    d.title(s, "A bit you read, or a program you run")
    d.rows(s, [
        ("the register road", "unidirectional integrases, which flip once and stay. 34 screened, 13 built, 11 mutually orthogonal, 1.375 bytes. Readout by sequencing. This is where the field went."),
        ("the program road", "place promoters, terminators and genes so that each arrangement IS a working transcription unit. Then you do not read the state — you run it, and selection does the reading."),
        ("which is Ham's idea", "the second. And it is the one still open."),
        ("34 to 11", "the same one-in-three attrition as Cello's gate library, arriving from the opposite direction."),
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
        ("combinational", "the compiler works. 45 of 60, and the missing quarter is orthogonality."),
        ("sequential", "DNA memory works. 11 orthogonal integrases out of 34 screened."),
        ("so Thursday", "what a part actually is, where one comes from, and why its number changes when you move it."),
    ])
    d.foot(s, "The architecture has not been the limit in either half of this hour.")
    d.notes(s, "One sentence, then the reading.")

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
