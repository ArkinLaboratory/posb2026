"""Session 1 — What synthetic biology is in 2026; the specification problem.

Eighty minutes: 8:10–9:30. The 8:00–9:29 in the Student Information System is
not the room -- under Berkeley Time instruction begins ten minutes after the
official start, and the ':29' is an SIS workaround. Four things compete for the
time: find out where the room actually is, establish the organising question, be
honest about the answer, and buy twenty minutes to explain why the course is
built the way it is.

The close is NOT a laptops-open DataHub session. The posted syllabus says
students will not usually need a laptop in lecture and moves environment setup
to the Tuesday 1 September discussion hour in Dwinelle 88; the sent announcement
says the same. So the last slide points at where the computing lives and stops.

    0–2    the organising question, and the answer "partially"
    2–10   diagnostic, on paper, ungraded
    10–13  lambda phage: nature did it first
    13–33  three given specifications, argued in groups          [20 min]
    33–37  consolidation: sense, compute, actuate
    37–40  SURVIVE — the one nobody wrote down
    40–43  ConcepTest 1 — vote, argue, revote
    43–46  the same cell, two ways
    46–49  four things that are not true of transistors
    49–52  ConcepTest 2 — vote, argue, revote
    52–55  thirty years of things that were built
    55–57  and four it still cannot do
    57–59  the whole course as one picture
    59–79  why the course is built this way                      [20 min, 6 slides]
    79–80  forward link
    close  where the computing lives, and the only administration

Twenty-two slides. The count is not a target -- docs/lecture-design.md lists
slide-count targets under "[C] Ignore" -- but the ratio behind it is: 46 minutes
of exposition across 17 slides is about 2.7 min/slide, against roughly 2.2 in
the 2025 decks. An earlier draft sat at 4.2, which meant six-to-eight-minute
stretches with nothing on the screen changing. That is not a short lecture, it
is an improvised one.

Three design notes, all corrections to earlier drafts of this deck.

**The 26–48 block was 22 minutes of unbroken instructor talk.** At 8am, on day
one. It is now three segments with a vote at each seam, which is what
docs/lecture-design.md §6 requires and what the earlier version simply omitted.
Both ConcepTests are answerable from first principles by a room that has been
taught nothing yet, and both seed a later session.

**The earlier version had no figures at all.** That was an over-correction. The
seductive-details finding justifies cutting the 2025 deck's pp. 4-9 -- Global
Risks Report, population projections -- because those are tangential decoration.
It says nothing against *explanatory* diagrams, which §5 grades [A]. Three
figures come back from the 2025 deck and one is generated from figures/.

**The twenty-minute format talk sat on four slides.** It is the block with the
least rehearsed material and the highest stakes, and it now has six, including
one that says where the evidence is weak and one on what to do when you are
lost. Overselling the evidence is the failure mode that costs you the room in
week nine; a student who checks the citation and finds a 300-person freshman
physics course will discount everything else you said.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session01_Specification"


def build():
    d = Deck("Session 1 — What synthetic biology is in 2026", session=1)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 1", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "The specification problem", M, 2.72, 9.0, 1.3,
           size=42, font=HEAD, bold=True, color=WHITE)
    d.text(s, "What synthetic biology is in 2026, and what it still cannot do",
           M, 4.15, 9.0, 0.5, size=18, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Do NOT open with administrivia. The syllabus is on bCourses and "
               "reading it aloud teaches nothing and sets the wrong expectation "
               "about what this room is for. Mechanics are the last two minutes. "
               "No laptops today -- the syllabus and the welcome announcement "
               "both said they would not need one, so do not ask for them. "
               "Hand out both paper handouts at the door.")

    # 2 THE QUESTION ----------------------------------------------------------
    s = d.dark()
    d.header(s, "0 – 2 min", "The whole course, in one sentence")
    d.title(s, "One question")
    d.text(s, "Can we specify what we want a biological system to do,\nand then build a cell that does it?",
           M, 2.3, 11.6, 1.6, size=30, font=HEAD, bold=True, color=MINT,
           spacing=1.3)
    d.text(s, "Thirty years in, the answer is", M, 4.4, 5.0, 0.4, size=18,
           color=WHITE)
    d.text(s, "partially.", M + 4.5, 4.32, 4.0, 0.6, size=32, font=HEAD,
           bold=True, color=AMBER)
    d.text(s, "The substance of the field lives in that word. This course is about where the specification-to-implementation pipeline works, where it breaks, and why.",
           M, 5.3, 11.6, 0.8, size=17, color=SILVER)
    d.notes(s, "Ninety seconds. Say the question, say 'partially', and move. "
               "Resist elaborating -- the next seventy-five minutes are the "
               "elaboration, and they will earn it rather than be told it.")

    # 3 DIAGNOSTIC ------------------------------------------------------------
    s = d.light()
    d.header(s, "2 – 10 min", "Diagnostic  ·  ungraded  ·  affects nothing")
    d.title(s, "Before anything else: where is this room?")
    d.text(s, "This cohort reliably spans molecular biology, physics, and EECS. That is not a problem to be managed quietly — it is a fact I need in order to set the pace honestly.",
           M, 1.95, 11.9, 0.8, size=17, color=BODY)
    for i, (n, txt, c) in enumerate([
            ("It is not graded", "It does not enter your grade in any way. Put your name on it anyway — I want to know how the room changes, not just where it starts.", TEAL),
            ("Blanks are data", "If you have never seen something, leave it blank. A blank is more useful to me than a guess, and it costs you nothing.", CYAN),
            ("Eight minutes", "Then we start work. You will get an anonymous summary of where the room is on Tuesday.", GREEN)]):
        y = 3.0 + i * 1.05
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.16, 0.85, fill=c, line=None)
        d.text(s, n, M + 0.4, y, 3.0, 0.4, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, txt, M + 3.7, y + 0.02, 8.2, 0.8, size=14, color=BODY)
    d.foot(s, "handouts/s01-diagnostic.pdf — two pages, duplexed. Four questions, one from each background the room contains.")
    d.notes(s, "Hand out on paper, face down, before you start talking. Eight "
               "minutes hard-stopped; take them in even if unfinished -- an "
               "unfinished sheet is itself a measurement. "
               "You are looking for the SHAPE of the distribution, not who is "
               "strong. Read them tonight; the session 2 pace depends on it, and "
               "PS0's self-report does not arrive until Sept 1. "
               "Question 4 is the one that separates the room hardest. Expect "
               "most biologists to leave it blank and most EECS students to get "
               "it in ten seconds. That asymmetry, said out loud on Tuesday, is "
               "worth more than any reassurance you could offer either group.")

    # 3b NATURE DID IT FIRST --------------------------------------------------
    s = d.light()
    d.header(s, "10 – 13 min", "The existence proof")
    d.title(s, "None of this would be worth trying if biology could not do it")
    d.text(s, "Lambda phage infects E. coli and makes one decision: replicate and burst the cell, or integrate and wait.",
           M, 1.9, 11.9, 0.45, size=17, color=BODY)
    for i, (k, txt, c) in enumerate([
            ("The decision is made once", "Two repressors, cI and Cro, each repressing the other's promoter. The circuit is small enough to draw on a napkin.", TEAL),
            ("And then held for generations", "A lysogen carries the decision through hundreds of divisions without re-deciding. That is memory, in a cell, built from two genes.", CYAN),
            ("And it is reversible on cue", "DNA damage cleaves cI and the switch flips. The state is stable, not frozen — which is a much harder specification.", GREEN)]):
        y = 2.6 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.16, 0.95, fill=c, line=None)
        d.text(s, k, M + 0.4, y, 3.6, 0.5, size=15.5, font=HEAD, bold=True, color=INK)
        d.text(s, txt, M + 4.3, y + 0.03, 7.6, 0.9, size=13.5, color=BODY)
    d.text(s, "So the question in 1999 was not whether a cell can hold a state. It was whether you can build one on purpose, from parts, in a cell that never had one.",
           M, 6.1, W - 2 * M, 0.6, size=16, bold=True, color=INK)
    d.notes(s, "Three minutes, no more, and no molecular detail -- Ptashne's "
               "switch is an existence proof, not today's content. Session 9 "
               "builds the synthetic version and session 7 does the "
               "autoregulation that makes it possible. "
               "The point students should leave with: the hard part was never "
               "'can matter compute'. It was 'can we specify it'. That is the "
               "title of the session.")

    # 4 LAUNCH ----------------------------------------------------------------
    s = d.dark()
    d.header(s, "13 – 33 min", "Groups of 3–4  ·  no answers yet")
    d.title(s, "Three things someone wants built")
    d.text(s, "You have the specification. You do not yet have any of the course.",
           M, 1.9, 11.6, 0.4, size=17, color=MINT)
    for i, (tag, spec, c) in enumerate([
            ("A", "A bacterium that turns visibly red when the well water it is in exceeds 10 µg/L arsenic.", CYAN),
            ("B", "A human T cell that kills a tumour cell and spares a healthy cell of the same tissue.", MINT),
            ("C", "A cereal crop that fixes its own nitrogen and needs no synthetic fertiliser.", AMBER)]):
        y = 2.5 + i * 1.15
        d.shape(s, S.OVAL, M, y + 0.06, 0.5, 0.5, fill=c, line=None)
        d.text(s, tag, M, y + 0.15, 0.5, 0.32, size=17, bold=True, color=INK,
               align="c")
        d.text(s, spec, M + 0.85, y, 11.1, 0.9, size=18, color=WHITE)
    d.text(s, "For each one:   what would you have to KNOW,   and what would you have to BUILD?",
           M, 6.05, 11.9, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Then rank them by difficulty and be ready to defend the ranking. The ranking is what we will argue about.",
           M, 6.5, 11.9, 0.35, size=14, italic=True, color=SILVER)
    d.notes(s, "TWENTY minutes, and it is the best-spent block in the session. "
               "Structure it: five minutes silent and individual first, then "
               "fifteen in groups. Individual-first stops the loudest person in "
               "each group from setting the frame before anyone else has "
               "thought. "
               "Circulate and write down WHO said WHAT. You need names for the "
               "next slide, and naming them is the fidelity condition that makes "
               "generation-before-instruction work at all (Sinha & Kapur). Give "
               "NO feedback during this phase. "
               "The cases are GIVEN, not invented -- contrasting cases are the "
               "active ingredient, and students inventing their own applications "
               "reliably produce three variants of the same easy problem. "
               "Expect the ranking A < B < C. The interesting disagreements are "
               "about WHY: most rank C hardest for the wrong reason (it is a "
               "plant) rather than the right one -- nitrogenase is irreversibly "
               "poisoned by oxygen, the ATP cost is enormous, and the host is a "
               "root-associated community you do not control. "
               "If a group finishes early, ask them which of the three they "
               "would fund, which is a different question and a harder one.")

    # 5 CONSOLIDATION A ------------------------------------------------------
    s = d.light()
    d.header(s, "33 – 37 min", "What you just said  ·  consolidation")
    d.title(s, "Every list in the room had the same three things on it")
    d.paper_figure(s, "l01_2025_sense_compute_actuate", M, 1.85, 7.6, 3.6,
                   "2025 deck, p. 19", "the cell as a designed system")
    for i, (k, txt, c) in enumerate([
            ("SENSE", "With a threshold and a false-positive rate you can state. A said 10 µg/L; what does your strain do at 9?", TEAL),
            ("COMPUTE", "Almost never one input. B needs at least two markers to separate a tumour cell from a healthy one.", TEAL),
            ("ACTUATE", "And strongly enough to matter. C's output is not a colour, it is grams of fixed nitrogen per hectare.", TEAL)]):
        y = 2.0 + i * 1.45
        d.text(s, k, 8.75, y, 2.0, 0.35, size=17, font=HEAD, bold=True, color=c)
        d.text(s, txt, 8.75, y + 0.36, 3.85, 1.0, size=13, color=BODY)
    d.foot(s, "Name the groups. Quote them. This is the ten minutes of argument being paid back.")
    d.notes(s, "NAME THE GROUPS. 'Group 2 said X; group 5 disagreed, and here "
               "is where the disagreement actually lives.' Skipping this makes "
               "the previous twenty minutes a waste -- it is the single "
               "strongest predictor of whether generation-before-instruction "
               "works at all (Sinha & Kapur). "
               "Four minutes. Do not add anything of your own yet; the next "
               "slide is where you add the thing they missed.")

    # 6 CONSOLIDATION B — THE MISSING ONE --------------------------------------
    s = d.dark()
    d.header(s, "37 – 40 min", "And the one that was not on anybody's list")
    d.title(s, "SURVIVE")
    d.text(s, "Keep doing it — in the real environment, for as long as it is needed.",
           M, 2.0, 11.9, 0.45, size=22, font=HEAD, color=MINT)
    for i, (spec, txt) in enumerate([
            ("A", "Six months in a well. Hundreds of generations, no selection keeping your circuit there, and nobody coming to re-inoculate."),
            ("B", "Weeks inside a patient, in a tissue that is actively hostile to the cell you injected."),
            ("C", "A growing season, in soil, in a root community of thousands of species you did not choose.")]):
        y = 2.85 + i * 0.95
        d.shape(s, S.OVAL, M, y + 0.02, 0.44, 0.44, fill=AMBER, line=None)
        d.text(s, spec, M, y + 0.1, 0.44, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, txt, M + 0.8, y, 11.2, 0.8, size=15.5, color=WHITE)
    d.text(s, "Look back at the figure. Nothing in it represents burden, mutation, or an environment that fights back.",
           M, 5.9, 11.9, 0.4, size=16, color=SILVER)
    d.text(s, "That absence is the second half of this course.", M, 6.35, 11.9,
           0.4, size=17, bold=True, color=CYAN)
    d.notes(s, "Three minutes, and it is the most important three in the "
               "consolidation. Almost no room writes this down -- not because "
               "they are careless, but because every diagram of a designed cell "
               "they have ever seen omits it, including the one on the previous "
               "slide. "
               "Do NOT scold. Flag it as a debt and name the sessions that pay "
               "it: 19 burden, 22 control, 23 evolutionary failure, 24 "
               "communities. "
               "If a group DID write it down, say whose it was. It is the single "
               "best thing anyone can have said in the first twenty minutes of "
               "the course.")

    # 6 CONCEPTEST 1 ----------------------------------------------------------
    s = d.dark()
    d.header(s, "40 – 43 min", "Vote  ·  argue with your neighbour  ·  vote again")
    d.title(s, "Your arsenic sensor works perfectly in the lab.")
    d.text(s, "You deploy ten thousand of them in wells and come back in six months. Most have stopped turning red. What is the most likely reason?",
           M, 1.95, 11.9, 0.75, size=18, color=WHITE)
    for i, (k, opt) in enumerate([
            ("A", "The sensor protein no longer binds arsenic."),
            ("B", "The red pigment is chemically degraded by something in the water."),
            ("C", "Cells that make less pigment grew faster than the ones that make more."),
            ("D", "Arsenic damaged the DNA of the construct.")]):
        y = 2.95 + i * 0.78
        d.shape(s, S.OVAL, M, y, 0.46, 0.46, fill=CYAN, line=None)
        d.text(s, k, M, y + 0.08, 0.46, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.04, 11.2, 0.45, size=16, color=WHITE)
    d.foot(s, "Nothing you have been taught yet answers this. Reason it out.", 6.35)
    d.notes(s, "ANSWER: C. Making pigment costs the cell resources it could "
               "spend growing. Over six months -- hundreds of generations -- any "
               "cell that makes less of it outgrows the ones that make more, and "
               "the population edits your design without asking. "
               "Run it properly: silent vote by hand or clicker, then two minutes "
               "of argument, then revote. Do not reveal the answer between "
               "votes. The swing between the two votes is the thing worth having. "
               "Most rooms split A/B on the first vote. Both are reasonable "
               "engineering failures and both are far less likely than selection. "
               "This is the first time they meet the idea that the SUBSTRATE "
               "IS EVOLVING, and it pays off in sessions 19 and 23. "
               "If someone answers C on the first vote, ask them to estimate how "
               "many generations six months is. Roughly a thousand. That number "
               "is the argument.")

    # 7 TWO VIEWS -------------------------------------------------------------
    s = d.light()
    d.header(s, "43 – 46 min", "Why this is not electrical engineering")
    d.title(s, "The same object, two ways")
    d.paper_figure(s, "l01_2025_cell_perspectives", M, 1.75, 8.6, 4.1,
                   "circuit board: courtesy Tim Lu · burrito: after Michael Elowitz",
                   "two views of one cell")
    d.text(s, "Which one\ndid you draw?", 9.6, 2.1, 3.0, 1.0, size=21,
           font=HEAD, bold=True, color=INK, spacing=1.25)
    d.text(s, "During the launch problem, everybody in this room was picturing the left-hand one. Defined parts, clean interfaces, a substrate that does what it is told.",
           9.6, 3.3, 3.0, 1.6, size=13, color=BODY)
    d.text(s, "The right-hand one is closer.", 9.6, 5.1, 3.0, 0.5, size=15,
           bold=True, color=AMBER)
    d.foot(s, "Everything in the right-hand column of the previous slide follows from picking the wrong picture.")
    d.notes(s, "Three minutes. The images ARE the argument -- do not talk over "
               "them at length. Ask the question on the slide out loud and wait "
               "for hands; the room finds it funny and then finds it "
               "uncomfortable, in that order, which is exactly the sequence you "
               "want before the next slide. "
               "Credits stay visible: circuit board courtesy of Tim Lu, burrito "
               "after Michael Elowitz. Both are credited on the 2025 slide.")

    # 8 FOUR CONSEQUENCES ------------------------------------------------------
    s = d.light()
    d.header(s, "46 – 49 min", "What follows from that")
    d.title(s, "Four things that are not true of transistors")
    for i, (k, txt) in enumerate([
            ("The substrate is alive and has its own agenda",
             "The host grows, competes for the ribosomes your circuit needs, and changes its physiology under your load. You are not building ON a chassis; you are building INSIDE a system that is already running."),
            ("Every part is context-dependent",
             "A promoter characterised in one construct does not keep its number in the next. Composition is not free, and session 21 measures exactly what it costs."),
            ("The population edits your design",
             "Mutation plus selection is a design process you did not authorise and cannot switch off. A circuit that costs growth gets deleted, on a timescale you can calculate."),
            ("You are always ignorant of most of it",
             "Not 'unmeasured yet' — thousands of interactions you will never enumerate. Designs have to work despite this, not after it is fixed.")]):
        y = 1.95 + i * 1.2
        d.shape(s, S.OVAL, M, y + 0.06, 0.44, 0.44, fill=TEAL, line=None)
        d.text(s, str(i + 1), M, y + 0.14, 0.44, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, k, M + 0.8, y, 11.2, 0.4, size=17, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 0.8, y + 0.4, 11.2, 0.75, size=13.5, color=BODY)
    d.foot(s, "None of these is a reason not to engineer biology. Each is a reason the engineering looks different.")
    d.notes(s, "Three minutes -- one line each, then move. This is the 2025 "
               "L01 pp. 23-25 content, but it lands AFTER they have argued "
               "about three real specifications, so each item answers an "
               "objection somebody in the room already raised. Asserted first "
               "it is a list; earned, it is a diagnosis. "
               "Item 2 is the one the next ConcepTest tests. Do not signpost "
               "that.")

    # 8 CONCEPTEST 2 ----------------------------------------------------------
    s = d.dark()
    d.header(s, "49 – 52 min", "Vote  ·  argue  ·  vote again")
    d.title(s, "You measure a promoter and get 100 units.")
    d.text(s, "Now you move that identical DNA sequence into a different construct — same cell, same medium, same day. What do you expect to measure?",
           M, 1.95, 11.9, 0.75, size=18, color=WHITE)
    for i, (k, opt) in enumerate([
            ("A", "100 units. It is the same sequence."),
            ("B", "Within about 10% of 100."),
            ("C", "Anywhere from 20 to 500."),
            ("D", "Nothing — a promoter only works in its original context.")]):
        y = 2.95 + i * 0.78
        d.shape(s, S.OVAL, M, y, 0.46, 0.46, fill=CYAN, line=None)
        d.text(s, k, M, y + 0.08, 0.46, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.04, 11.2, 0.45, size=16, color=WHITE)
    d.foot(s, "If B were true, this would be electrical engineering and the course would be shorter.", 6.35)
    d.notes(s, "ANSWER: C. Order-of-magnitude context effects are routine, not "
               "exceptional: neighbouring sequence, copy number, the load of "
               "whatever else is on the plasmid, the growth rate. "
               "A is what the parts-registry framing implicitly promises and it "
               "is the single most consequential wrong belief a student can "
               "leave this course with. D is the opposite over-correction -- "
               "parts do compose, just not for free and not additively. "
               "Sessions 17 and 21 are the whole answer. Say that; do not answer "
               "it today. "
               "Good follow-up if the room lands on C quickly: if it varies by "
               "an order of magnitude, what would you have to measure to design "
               "with it anyway? That is retroactivity, and it is session 21.")

    # 9 WHAT THE FIELD BUILT --------------------------------------------------
    s = d.light()
    d.header(s, "52 – 55 min", "Where the field actually is  ·  the good half")
    d.title(s, "Thirty years of things that were actually built")
    d.paper_figure(s, "l01_2025_prototypes_to_applications", M, 1.75, 8.4, 4.2,
                   "2025 deck, p. 26 — panel sources need resolving",
                   "prototypes → systems → applications")
    for i, (k, txt) in enumerate([
            ("You will build six of these", "Toggle, oscillator, band detector, multi-input logic, metabolic pathway, classifier — sessions 9 through 26."),
            ("Reading and writing DNA is solved", "Sequencing and synthesis are not the bottleneck for anything in this course."),
            ("So is single-protein design", "Binders and enzymes to specification is a working technology now, not a promise.")]):
        y = 2.0 + i * 1.5
        d.text(s, k, 9.4, y, 3.3, 0.7, size=14.5, font=HEAD, bold=True, color=GREEN)
        d.text(s, txt, 9.4, y + 0.62, 3.3, 1.0, size=12, color=BODY)
    d.notes(s, "Three minutes and keep it fast -- this slide is a tour, not a "
               "syllabus. Point at the six the course actually builds; that is "
               "the promise being made. "
               "FIGURE PROVENANCE: 2025 Lecture 01 p. 26, a composite of "
               "published panels whose individual sources are not marked on the "
               "original slide. Resolve before any public release of the deck.")

    # 10 WHAT IT CANNOT DO -----------------------------------------------------
    s = d.dark()
    d.header(s, "55 – 57 min", "Where the field actually is  ·  the other half")
    d.title(s, "And four things it still cannot do")
    for i, (k, txt) in enumerate([
            ("Integration", "Sc2.0 has been building synthetic yeast chromosomes since 2011. There is still no strain carrying all sixteen."),
            ("Prediction in a real host", "Behaviour in a lab strain does not transfer to a gut, a soil, or a tumour. Nobody can compute the difference."),
            ("Durability", "Almost nothing published keeps working for a month of growth without selection holding it in place."),
            ("Specification itself", "There is no language in which you state what you want and get an implementation. English is the state of the art.")]):
        y = 1.95 + i * 1.12
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.85, fill=RED, line=None)
        d.text(s, k, M + 0.4, y, 3.5, 0.4, size=17, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 4.2, y + 0.02, 7.7, 0.85, size=14, color=MINT)
    d.text(s, "Every one of these is a session in the second half of this course.",
           M, 6.5, W - 2 * M, 0.4, size=16, bold=True, color=CYAN)
    d.notes(s, "Two minutes. CHECK BEFORE DELIVERY -- this is the one slide "
               "with a shelf life and it should be re-examined every year. "
               "SC2.0 IS NOT FINISHED. Individual synthetic chromosomes have "
               "been designed, built and debugged for over a decade, the most "
               "recent reported in early 2025 -- but there is no strain "
               "carrying all sixteen. Do not say or imply otherwise. "
               "That is the whole point, and it is worth saying slowly: every "
               "part was verified in isolation, by people who are extremely "
               "good at this, over fifteen years, in a genome that is small, "
               "well characterised and haploid. Consolidation is STILL the hard "
               "part. If integration is unsolved there, nobody should be "
               "surprised when a four-gene circuit misbehaves in a mouse gut. "
               "Ask: why should assembling verified parts be harder than making "
               "them? That question is sessions 17 through 23.")

    # 10 THE ARCHITECTURE -----------------------------------------------------
    s = d.light()
    d.header(s, "57 – 59 min", "The shape of the semester")
    d.title(s, "The whole course, as one picture")
    d.image(s, "figures/build/s01_pipeline.png", M, 1.75, 11.9, 3.7)
    for i, (n, k, txt, c) in enumerate([
            ("SESSIONS 1 – 14", "Design principles",
             "What can a circuit do, and why is it built that way? By session 14 anyone here can take a circuit diagram, write the equations, and determine its behaviour quantitatively.", TEAL),
            ("SESSIONS 16 – 28", "Engineering design",
             "Now build one that survives in a real host. The three red and amber boxes above are the second half of the semester.", GREEN)]):
        x = M + i * 6.2
        d.shape(s, S.ROUNDED_RECTANGLE, x, 5.35, 0.1, 1.25, fill=c, line=None)
        d.text(s, n, x + 0.32, 5.35, 5.3, 0.26, size=10, bold=True, color=c)
        d.text(s, k, x + 0.32, 5.6, 5.3, 0.34, size=16, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, x + 0.32, 5.96, 5.3, 0.7, size=12, color=BODY)
    d.notes(s, "Two minutes. This is the slide to come back to in every session "
               "-- 'we are here' -- and the one to reuse on the last day. "
               "The hinge is session 13, the digital abstraction, followed "
               "immediately by session 16 on why design automation plateaued "
               "anyway. "
               "Both ConcepTests they just voted on live in the two right-hand "
               "boxes. Say so: neither was a detail.")

    # 11 FORMAT I -------------------------------------------------------------
    s = d.dark()
    d.header(s, "59 – 79 min", "Why this course is built the way it is")
    d.title(s, "You are going to feel like you are learning less")
    d.text(s, "This is the most important twenty minutes of the semester, and it is not about synthetic biology.",
           M, 2.05, 11.9, 0.4, size=17, italic=True, color=MINT)
    d.text(s, "Almost every session will ask you to attempt something before I have taught you how to do it, and to argue about it with the people next to you. You did it twice already this morning.",
           M, 2.75, 11.9, 0.9, size=19, color=WHITE, spacing=1.3)
    d.text(s, "That is deliberate, it is uncomfortable, and there is a specific, measured reason for it.",
           M, 3.85, 11.9, 0.5, size=19, bold=True, color=CYAN)
    d.text(s, "I am telling you now because the discomfort is the mechanism, not a defect in the teaching — and because a course that does this and does not explain it gets abandoned.",
           M, 4.7, 11.9, 0.8, size=16, color=SILVER)
    d.notes(s, "Do not rush this and do not apologise for it. Deslauriers et al. "
               "2019 PNAS: the gap between real and perceived learning is the "
               "mechanism by which good redesigns get dropped. Twenty minutes "
               "here is cheaper than the alternative. "
               "Point back at the two votes explicitly -- they have now felt the "
               "thing you are about to describe, which is a much better position "
               "to describe it from than a cold start.")

    # 12 FORMAT II — THE NUMBERS ---------------------------------------------
    s = d.light()
    d.header(s, "59 – 79 min", "The measurement")
    d.title(s, "The same students, measured two ways")
    for i, (n, lab, txt, c) in enumerate([
            ("+0.46 SD", "ACTUAL LEARNING", "Measured by a test of the material, in a controlled comparison against a lecture on the same content by the same instructors.", GREEN),
            ("−0.56 SD", "FEELING OF LEARNING", "The same students, asked how much they felt they had learned. They were confident, and they were wrong.", RED)]):
        x = M + i * 6.2
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.0, 5.7, 2.6, fill=CARD, line=c, lw=2)
        d.text(s, lab, x + 0.3, 2.22, 5, 0.28, size=10, bold=True, color=c)
        d.text(s, n, x + 0.3, 2.55, 5.1, 0.8, size=44, font=HEAD, bold=True,
               color=c)
        d.text(s, txt, x + 0.3, 3.5, 5.1, 1.0, size=14, color=BODY)
    d.text(s, "Deslauriers, McCarty, Miller, Callaghan & Kestin, PNAS 116:19251 (2019). Active learning raises exam performance ~0.47 SD across 225 studies (Freeman et al. 2014).",
           M, 4.85, W - 2 * M, 0.5, size=13, italic=True, color=MUTED)
    d.text(s, "A smooth lecture feels like understanding. Fluency is not learning, and fluency is what your intuition is measuring.",
           M, 5.55, W - 2 * M, 0.6, size=17, bold=True, color=INK)
    d.notes(s, "Put the numbers on the board and leave them there. Students who "
               "have seen the effect size argue with you far less in week eight. "
               "If asked whether it replicates: Freeman is 225 studies. Do NOT "
               "oversell -- say the evidence base is mostly large introductory "
               "courses and this is a 35-person advanced course, so it is an "
               "extrapolation. Being straight about that buys more credibility "
               "than the claim does.")

    # F3 THE HONEST CAVEAT -----------------------------------------------------
    s = d.light()
    d.header(s, "59 – 79 min", "What that evidence does not say")
    d.title(s, "Where I think the argument is weak")
    for i, (k, txt) in enumerate([
            ("The studies are mostly not this course",
             "Large introductory physics and biology courses, hundreds of students, short retention intervals. This is a 35-person advanced course with material of much higher element interactivity. Every number I just showed you is an extrapolation."),
            ("Effect sizes are averages over designs that vary a lot",
             "'Active learning' covers everything from clicker questions to full studio courses. The meta-analytic average does not tell you which parts did the work."),
            ("Some of what I do here is convention, not evidence",
             "Putting retrieval at the start of class, showing a course map, the two-minute pause — these are reasonable and unsupported. They are labelled [C] in the design document, and you can read which is which."),
            ("One famous result in this area failed to replicate",
             "The longhand-beats-laptop finding. I am not going to tell you to close your laptop on that basis. Multitasking harming your NEIGHBOUR is a different and better-supported claim.")]):
        y = 1.88 + i * 1.16
        d.shape(s, S.OVAL, M, y + 0.04, 0.4, 0.4, fill=AMBER, line=None)
        d.text(s, str(i + 1), M, y + 0.11, 0.4, 0.28, size=13, bold=True,
               color=WHITE, align="c")
        d.text(s, k, M + 0.72, y, 11.3, 0.38, size=15.5, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 0.72, y + 0.38, 11.3, 0.8, size=12.5, color=BODY)
    d.foot(s, "I would rather you knew where the argument is soft than discover it yourself in week nine and conclude the whole thing was marketing.", 6.62)
    d.notes(s, "Two to three minutes, and do not skip it to save time. "
               "Overselling the evidence is the failure mode that costs you the "
               "room later: a student who checks the citation and finds it is a "
               "physics course with 300 freshmen will discount everything else "
               "you said. Saying it first is cheap and it is true. "
               "It also models the thing the course is about -- distinguishing "
               "what was demonstrated from what was claimed, which is learning "
               "outcome 9.")

    # 13 FORMAT III — WHAT IT MEANS -------------------------------------------
    s = d.light()
    d.header(s, "59 – 79 min", "What that means for how a session runs")
    d.title(s, "So here is what happens every Tuesday and Thursday")
    for i, (t, k, txt) in enumerate([
            ("0–5", "Retrieval, notes closed", "Two questions from last session, one from three or four back. It will feel like a quiz. It is not graded — retrieving is what makes it stick."),
            ("8–20", "You try it first", "A problem you cannot yet solve, in groups. Getting it wrong is the intended outcome; the attempt is what makes the explanation land."),
            ("20–48", "The concept, in three pieces", "Each ending in a vote, a two-minute argument with your neighbour, and a second vote — exactly like the two you did today."),
            ("50–72", "Faded worked examples", "Four versions of one problem, each with less of my working shown. Start wherever the scaffolding stops helping you — nobody announces where that is."),
            ("72–80", "Close the loop", "Back to the opening questions, in writing, notes closed. Then one slide on why the next session exists.")]):
        y = 1.9 + i * 0.95
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.95, 0.42, fill=TEAL, line=None)
        d.text(s, t, M, y + 0.09, 0.95, 0.3, size=11, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 1.2, y, 3.4, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.75, y + 0.02, 7.15, 0.85, size=12.5, color=BODY)
    d.foot(s, "The full design, with the evidence and its grade, is in docs/lecture-design.md. Read it if you want to argue with it — several choices are convention, and they are labelled as convention.")
    d.notes(s, "Publishing the pedagogy is unusual and worth saying out loud "
               "that you are doing it. It converts 'trust me' into 'here is the "
               "argument, and here is where it is weak'.")

    # F5 WHEN YOU ARE LOST -----------------------------------------------------
    s = d.light()
    d.header(s, "59 – 79 min", "The part nobody tells you")
    d.title(s, "What to do when you are lost — and you will be")
    for i, (k, txt, c) in enumerate([
            ("In the room, mid-derivation", "Put your hand up. Someone else is lost at the same step and has not said so. You are not slowing us down; you are telling me my pace is wrong, which is information I cannot get any other way.", TEAL),
            ("On the faded handout", "Move UP the sheet, not down. Item 1 is fully worked. Starting there is not a confession, it is what the sheet is for — nobody is watching where you start.", CYAN),
            ("On a problem set, at 1am", "Stop. The set is meant to take a few hours, not a weekend. If it is taking longer, that is information about the course, not about you. Post it on the forum — the answer helps ten people.", GREEN),
            ("Three weeks in, generally", "Come to Tuesday's discussion hour. Historically it is the most useful hour in the course for the students who use it, and almost nobody uses it in September.", AMBER)]):
        y = 1.88 + i * 1.18
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.14, 0.95, fill=c, line=None)
        d.text(s, k, M + 0.4, y, 3.5, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.2, y + 0.02, 7.7, 0.95, size=13, color=BODY)
    d.foot(s, "If your background is light on differential equations, weeks 1–4 are the demanding stretch. If it is light on molecular biology, weeks 8–10 are. Both are survivable. Neither is if you wait until the midterm to say something.", 6.62)
    d.notes(s, "Two to three minutes. This is the slide that makes the format "
               "humane rather than merely demanding, and it is the one students "
               "quote back in evaluations. "
               "Say the discussion-hour line and mean it -- Dwinelle 88, "
               "Tuesdays after class. The students who need it most are the "
               "ones who assume it is for people who are already ahead.")

    # 14 FORMAT IV — THE DEAL -------------------------------------------------
    s = d.dark()
    d.header(s, "59 – 79 min", "The deal")
    d.title(s, "What I owe you, and what you owe the room")
    for i, (who, items, c) in enumerate([
            ("I will", ["Never assess a technique I did not demonstrate first — there is a matrix, and it is public.",
                         "Work the mathematics rather than assert the result.",
                         "Publish every notebook, deck, and derivation, free, for anyone.",
                         "Tell you when something is not known, rather than smoothing over it."], CYAN),
            ("You will", ["Read the paper before the session that argues about it. It is assigned the class before, every time.",
                           "Attempt the launch problem badly rather than wait to be told.",
                           "Say the thing you think is wrong out loud. The room learns from the wrong answer.",
                           "Tell me when the pace is wrong — early, not on the evaluation in December."], MINT)]):
        x = M + i * 6.2
        d.text(s, who.upper(), x, 1.9, 5.7, 0.35, size=13, bold=True, color=c)
        for j, it in enumerate(items):
            y = 2.4 + j * 1.02
            d.shape(s, S.ROUNDED_RECTANGLE, x, y, 0.1, 0.8, fill=c, line=None)
            d.text(s, it, x + 0.35, y, 5.35, 0.95, size=13.5, color=WHITE)
    d.foot(s, "Errors in the material are worth reporting and you will be credited by name. Several of last year's corrections are already in the repository.", 6.7)
    d.notes(s, "The reciprocity is the point. Students accept a demanding format "
               "far more readily when the obligations run both ways and the "
               "instructor's half is specific enough to be checked.")

    # 15 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "79 – 80 min", "Next")
    d.title(s, "You listed what you would need to know. Start with the cell.")
    d.text(s, "Tuesday: the cell as a physical substrate.", M, 2.1, 11.6, 0.45,
           size=24, font=HEAD, bold=True, color=MINT)
    d.text(s, "Every specification you wrote today assumes a thing that senses, computes and acts. That thing is about one femtolitre, roughly a fifth protein by weight, and it divides in twenty minutes.\n\nHow many copies of your sensor protein are in there? How long does one of them take to cross the cell? Is 'concentration' even the right variable at that copy number?",
           M, 2.8, 11.6, 2.0, size=17, color=WHITE, spacing=1.4)
    d.text(s, "You cannot design anything until you can answer those in your head, to an order of magnitude.",
           M, 4.95, 11.6, 0.4, size=16, bold=True, color=CYAN)
    d.assignment(s, y=5.5)
    d.text(s, "No reading before Tuesday. PS0 is ten minutes, at home, due Wednesday 2 September.",
           M, 5.6, 11.6, 0.35, size=15, bold=True, color=SILVER)
    d.notes(s, "LEAVE THIS SLIDE UP through the closing slide. The three "
               "questions sit on the projector while they are clicking links, "
               "which is free exposure while they photograph the links. "
               "They are the session 2 retrieval "
               "opener, verbatim.")

    # 16 DATAHUB + MECHANICS --------------------------------------------------
    s = d.light()
    d.header(s, "the last two minutes", "Where the computing lives")
    d.title(s, "Where the computing lives — photograph this slide")
    for i, (n, k, txt) in enumerate([
            ("1", "The link is on bCourses", "CalNet signs you in, clones the repository and opens the notebook. That is the whole setup — there is nothing to install, and nothing to do right now."),
            ("2", "PS0 — ten minutes, ungraded", "Run it at home this week. Due Wednesday 2 September, 11:59pm. If it takes longer than ten minutes, something is wrong and I want to know."),
            ("3", "If it fights you", "Tuesday's discussion hour, straight after class, Dwinelle 88. Bring a laptop to that one and we will fix it together, before PS0 is due."),
            ("4", "Waitlisted, or CalNet not caught up?", "Use the Colab badge today — DataHub needs you enrolled and Colab does not. Then tell me.")]):
        y = 1.85 + i * 0.82
        d.shape(s, S.OVAL, M, y + 0.02, 0.4, 0.4, fill=TEAL, line=None)
        d.text(s, n, M, y + 0.09, 0.4, 0.28, size=12, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.62, y, 3.6, 0.35, size=14, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.4, y + 0.02, 7.5, 0.7, size=12.5, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.25, W - 2 * M, 1.45, fill=WASH,
            line=TEAL, lw=1.5)
    d.text(s, "WHILE THAT SPAWNS — THE ONLY ADMINISTRATION IN THIS COURSE",
           M + 0.3, 5.4, 8.0, 0.28, size=10, bold=True, color=TEAL)
    for i, (k, v) in enumerate([("Problem sets", "30%"), ("Midterm", "15%"),
                                ("Final", "25%"), ("Project", "30%")]):
        x = M + 0.3 + i * 2.45
        d.text(s, v, x, 5.68, 1.2, 0.4, size=20, font=HEAD, bold=True, color=INK)
        d.text(s, k, x, 6.08, 2.3, 0.28, size=11.5, color=BODY)
    d.text(s, "Nine sets, lowest two dropped · Midterm Thu 15 Oct · Project description due session 9 · PS0 ten minutes, ungraded, due Wed 2 Sep",
           M + 0.3, 6.36, 12.0, 0.28, size=11, italic=True, color=MUTED)
    d.notes(s, "TWO MINUTES, NO LAPTOPS. The syllabus and the welcome "
               "announcement both told them they would not need one today, and "
               "the environment session is Tuesday's discussion hour in Dwinelle "
               "88 -- do not contradict that here. Tell them to photograph the "
               "slide. "
               "Say the assessment weights out loud; do not read the syllabus, "
               "it is on bCourses. "
               "The one thing worth pressing: PS0 is due WEDNESDAY 2 September, "
               "the day after the discussion hour, so the help lands before the "
               "deadline and the deadline lands before session 3. "
               "Stay a few minutes after. The students who cannot get in are "
               "exactly the ones who will not email.")

    return d
