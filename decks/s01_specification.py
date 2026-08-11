"""Session 1 — What synthetic biology is in 2026; the specification problem.

The first day, and it has to do four things that compete for the same eighty
minutes: find out where the room actually is, establish the organising question,
be honest about the answer, and buy twenty minutes to explain why the course is
built the way it is.

The twenty minutes are not optional. Active formats raise learning ~0.46 SD and
lower *perceived* learning ~0.56 SD (Deslauriers et al. 2019), and that gap is
the mechanism by which good redesigns get abandoned. See docs/lecture-design.md
§7. Everything else on this day was budgeted around it.

What was cut from the 2025 L01, and why: pages 4-9, six slides of Global Risks
Report / population-projection / "the age of biology is here" framing. It is
2016-era advocacy, it is the seductive-details pattern the slide-design evidence
says measurably costs comprehension, and none of it survives the only question
this session actually asks -- what would you have to know to build one?
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
               "about what this room is for. Mechanics are at minute 70, after "
               "they have already done something.")

    # 2 THE QUESTION ----------------------------------------------------------
    s = d.dark()
    d.header(s, "0 – 3 min", "The whole course, in one sentence")
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
               "Resist elaborating -- the next seventy minutes are the "
               "elaboration, and they will earn it rather than be told it.")

    # 3 DIAGNOSTIC ------------------------------------------------------------
    s = d.light()
    d.header(s, "3 – 11 min", "Diagnostic  ·  ungraded  ·  affects nothing")
    d.title(s, "Before anything else: where is this room?")
    d.text(s, "This cohort reliably spans molecular biology, physics, and EECS. That is not a problem to be managed quietly — it is a fact I need in order to set the pace honestly.",
           M, 1.95, 11.9, 0.8, size=17, color=BODY)
    for i, (n, txt, c) in enumerate([
            ("It is not graded", "It does not enter your grade in any way. Put your name on it anyway — I want to know how the room changes, not just where it starts.", TEAL),
            ("Blanks are data", "If you have never seen something, leave it blank. A blank is more useful to me than a guess, and it costs you nothing.", CYAN),
            ("Eight minutes", "Then we start work. You will not get it back; you will get an anonymous summary of the room in session 2.", GREEN)]):
        y = 3.0 + i * 1.05
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.16, 0.85, fill=c, line=None)
        d.text(s, n, M + 0.4, y, 3.0, 0.4, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, txt, M + 3.7, y + 0.02, 8.2, 0.8, size=14, color=BODY)
    d.foot(s, "Handout: handouts/s01-diagnostic — four questions, one from each background the room contains.")
    d.notes(s, "Hand out on paper, face down, before you start talking. Eight "
               "minutes hard-stopped. The point is calibration, not assessment: "
               "you are looking for the SHAPE of the distribution, not who is "
               "strong. Read them tonight; the S2 pace depends on it. "
               "PS0's questionnaire is self-report and arrives Sept 1 -- too "
               "late to affect session 2, which is why this one is on paper.")

    # 4 LAUNCH ----------------------------------------------------------------
    s = d.dark()
    d.header(s, "11 – 26 min", "Groups of 3–4  ·  no answers yet")
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
    d.text(s, "Then rank them by difficulty and be ready to defend the ranking.",
           M, 6.5, 11.9, 0.35, size=14, italic=True, color=SILVER)
    d.notes(s, "Fifteen minutes. Circulate, write down WHO said WHAT -- you need "
               "names for the consolidation slide and that is the fidelity "
               "condition that makes generation-before-instruction work at all "
               "(Sinha & Kapur). Give NO feedback in this phase. "
               "The cases are given, not invented: contrasting cases are the "
               "active ingredient, and students inventing their own applications "
               "produces three variants of the same easy problem. "
               "Expect the ranking A < B < C. The interesting disagreements are "
               "about WHY: most rank C hardest for the wrong reason (it is a "
               "plant) rather than the right one (nitrogenase is oxygen-"
               "sensitive, the energy cost is enormous, and the host is a "
               "community you do not control).")

    # 5 CONSOLIDATION I -------------------------------------------------------
    s = d.light()
    d.header(s, "26 – 34 min", "What you just said  ·  consolidation")
    d.title(s, "Every list you wrote had the same four things on it")
    for i, (k, txt, ex) in enumerate([
            ("SENSE", "Detect the condition, with a threshold and a false-positive rate you can state.",
             "A: 10 µg/L is the WHO limit. What is your detection limit, and what does the strain do at 9?"),
            ("COMPUTE", "Combine evidence. Almost never one input — B needs at least two markers to separate tumour from healthy.",
             "B: one antigen is not enough. This is why session 13 is about logic and session 26 about classifiers."),
            ("ACTUATE", "Do the thing. Colour, killing, catalysis — and it has to be strong enough to matter.",
             "C: nitrogenase is not a reporter. The output is grams of fixed nitrogen per hectare."),
            ("SURVIVE", "Keep doing it, in the real environment, for as long as it is needed.",
             "Nobody wrote this down. It is where most of these fail, and it is half of this course.")]):
        y = 1.95 + i * 1.18
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 1.9, 0.95,
                fill=WASH if i < 3 else AMBER, line=TEAL if i < 3 else AMBER, lw=1.5)
        d.text(s, k, M, y + 0.3, 1.9, 0.35, size=14, font=HEAD, bold=True,
               color=INK if i < 3 else WHITE, align="c")
        d.text(s, txt, M + 2.15, y + 0.02, 9.75, 0.5, size=15, color=BODY)
        d.text(s, ex, M + 2.15, y + 0.52, 9.75, 0.42, size=12.5, italic=True,
               color=MUTED)
    d.notes(s, "NAME THE GROUPS. 'Group 2 said X; group 5 disagreed and here is "
               "where the disagreement actually lives.' Skipping this makes the "
               "previous fifteen minutes a waste -- it is the single strongest "
               "predictor of whether the technique works. "
               "The amber row is almost always absent from their lists. Do not "
               "scold; flag it as a debt, and pay it in sessions 19-23.")

    # 6 WHAT IS DIFFERENT -----------------------------------------------------
    s = d.light()
    d.header(s, "34 – 42 min", "Why this is not electrical engineering")
    d.title(s, "Four things that are not true of transistors")
    for i, (k, txt) in enumerate([
            ("The substrate is alive and has its own agenda",
             "The host grows, competes for the ribosomes your circuit needs, and its physiology changes under your load. You are not building ON a chassis; you are building INSIDE a system that is already running."),
            ("Every part is context-dependent",
             "A promoter characterised in one construct does not keep its number in the next. Composition is not free, and session 21 is about measuring exactly what it costs."),
            ("The population edits your design",
             "Mutation plus selection is a design process you did not authorise and cannot switch off. A circuit that costs growth will be deleted, on a timescale you can calculate."),
            ("You are always ignorant of most of it",
             "Not 'we haven't measured it yet' — the host has thousands of interactions you will never enumerate. Designs have to work despite this, not after it is fixed.")]):
        y = 1.9 + i * 1.2
        d.shape(s, S.OVAL, M, y + 0.08, 0.42, 0.42, fill=TEAL, line=None)
        d.text(s, str(i + 1), M, y + 0.16, 0.42, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, k, M + 0.75, y, 11.2, 0.4, size=17, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 0.75, y + 0.4, 11.2, 0.75, size=13.5, color=BODY)
    d.notes(s, "This is the 2025 L01 pp. 23-25 content, but it now lands AFTER "
               "they have argued about three real specs, so each item answers "
               "an objection somebody in the room already raised. Asserted "
               "first, it is a list; earned, it is a diagnosis.")

    # 7 THE 2026 SCORECARD ----------------------------------------------------
    s = d.light()
    d.header(s, "42 – 48 min", "Where the field actually is")
    d.title(s, "What 2026 can and cannot do")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.9, 6.0, 4.3, fill=CARD, line=GREEN, lw=2)
    d.text(s, "LARGELY SOLVED", M + 0.3, 2.05, 5.4, 0.3, size=11, bold=True,
           color=GREEN)
    for i, t in enumerate([
            "Reading and writing DNA. Sequencing and synthesis are no longer the bottleneck for anything in this course.",
            "Single-protein design. Binders and enzymes to specification is a working technology, not a promise.",
            "Megabase-scale DNA construction. Individual synthetic yeast chromosomes approaching 1 Mb are designed, built and debugged.",
            "Small circuits in a lab strain. Toggles, oscillators, logic gates — the objects of sessions 9–13."]):
        d.text(s, "▪", M + 0.3, 2.45 + i * 0.95, 0.25, 0.3, size=13, color=GREEN)
        d.text(s, t, M + 0.62, 2.45 + i * 0.95, 5.1, 0.9, size=12.5, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M + 6.3, 1.9, 6.0, 4.3, fill=CARD,
            line=RED, lw=2)
    d.text(s, "NOT SOLVED", M + 6.6, 2.05, 5.4, 0.3, size=11, bold=True, color=RED)
    for i, t in enumerate([
            "Integration. Sc2.0 has been building synthetic yeast chromosomes since 2011 and there is still no strain carrying all sixteen.",
            "Prediction in a real host. Circuit behaviour in a lab strain does not transfer to a gut, a soil, or a tumour.",
            "Durability. Almost nothing published keeps working for a month of growth without selection to hold it there.",
            "Specification itself. There is no language in which you can state what you want and get an implementation."]):
        d.text(s, "▪", M + 6.6, 2.45 + i * 0.95, 0.25, 0.3, size=13, color=RED)
        d.text(s, t, M + 6.92, 2.45 + i * 0.95, 5.1, 0.9, size=12.5, color=BODY)
    d.text(s, "The left column is why the field is worth joining. The right column is what this course is for.",
           M, 6.3, W - 2 * M, 0.35, size=15, bold=True, color=INK)
    d.text(s, "Note what the two columns have in common: making the parts is the solved problem. Putting them together is not — at every scale, from four genes to sixteen chromosomes.",
           M, 6.7, W - 2 * M, 0.35, size=13, italic=True, color=MUTED)
    d.notes(s, "CHECK BEFORE DELIVERY -- this is the one slide in the course "
               "with a shelf life and it should be re-examined every year. "
               "Sc2.0 is the anchor for the right-hand column and it is worth "
               "two minutes on its own. Individual synthetic chromosomes have "
               "been designed, built and debugged for over a decade; the most "
               "recent, synXVI, was reported in early 2025. The project is NOT "
               "fully built: there is no strain carrying all sixteen. "
               "Do not say or imply otherwise. "
               "That is the whole point. Every part was verified in isolation "
               "by people who are extremely good at this, over fifteen years, "
               "with a genome that is small, well characterised and haploid -- "
               "and consolidation is still the hard part. If integration is "
               "unsolved THERE, nobody should be surprised that a four-gene "
               "circuit behaves differently in a mouse gut. "
               "Ask the room: why should assembling verified parts be harder "
               "than making them? That question is sessions 17 through 23.")

    # 8 THE ARCHITECTURE ------------------------------------------------------
    s = d.light()
    d.header(s, "48 – 50 min", "The shape of the semester")
    d.title(s, "Two halves that do different work")
    for i, (n, k, txt, c) in enumerate([
            ("1 – 14", "Design principles",
             "What can a circuit do, and why is it built that way? By session 14 anyone here — from any background — can take a circuit diagram, write the equations, and determine its behaviour quantitatively.", TEAL),
            ("16 – 28", "Engineering design",
             "Now build one that survives in a real host. Burden, retroactivity, control, evolution, communities, delivery, and what the field cannot yet specify.", GREEN)]):
        x = M + i * 6.2
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.1, 5.7, 2.5, fill=CARD, line=c, lw=2)
        d.text(s, f"SESSIONS {n}", x + 0.3, 2.32, 5, 0.28, size=10, bold=True,
               color=c)
        d.text(s, k, x + 0.3, 2.62, 5.1, 0.5, size=22, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, x + 0.3, 3.22, 5.1, 1.2, size=13.5, color=BODY)
    d.text(s, "The hinge is session 13 — the digital abstraction — followed immediately by session 16, which is about why design automation plateaued anyway.",
           M, 4.95, W - 2 * M, 0.5, size=15, color=INK)
    d.text(s, "The right-hand column of the previous slide is the second half of this one.",
           M, 5.55, W - 2 * M, 0.4, size=15, bold=True, color=INK)
    d.notes(s, "Two minutes. This is signalling, not content -- students should "
               "be able to locate themselves in the architecture on any day.")

    # 9 FORMAT I --------------------------------------------------------------
    s = d.dark()
    d.header(s, "50 – 70 min", "Why this course is built the way it is")
    d.title(s, "You are going to feel like you are learning less")
    d.text(s, "This is the most important twenty minutes of the semester, and it is not about synthetic biology.",
           M, 2.05, 11.9, 0.4, size=17, italic=True, color=MINT)
    d.text(s, "Almost every session here will ask you to attempt something before I have taught you how to do it, and to argue about it with the people next to you.",
           M, 2.75, 11.9, 0.8, size=19, color=WHITE, spacing=1.3)
    d.text(s, "That is deliberate, it is uncomfortable, and there is a specific, measured reason for it.",
           M, 3.75, 11.9, 0.5, size=19, bold=True, color=CYAN)
    d.text(s, "I am telling you now because the discomfort is the mechanism, not a defect in the teaching — and because a course that does this and does not explain it gets abandoned.",
           M, 4.6, 11.9, 0.8, size=16, color=SILVER)
    d.notes(s, "Do not rush this and do not apologise for it. Deslauriers et al. "
               "2019 PNAS: the gap between real and perceived learning is the "
               "mechanism by which good redesigns get dropped. Twenty minutes "
               "spent here is cheaper than the alternative.")

    # 10 FORMAT II — THE NUMBERS ---------------------------------------------
    s = d.light()
    d.header(s, "50 – 70 min", "The measurement")
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
    d.text(s, "A smooth lecture feels like understanding. Fluency is not learning, and it is the thing your intuition is measuring.",
           M, 5.55, W - 2 * M, 0.6, size=17, bold=True, color=INK)
    d.notes(s, "Put the numbers on the board and leave them there. Students who "
               "have seen the effect size argue with you far less in week eight. "
               "If someone asks whether it replicates: Freeman is 225 studies, "
               "and the perceived-learning gap has held up in several settings. "
               "Do not oversell it -- say the evidence base is mostly large "
               "intro courses, and that this room is a 35-person advanced "
               "course, so it is an extrapolation. Being straight about that "
               "buys more credibility than the claim does.")

    # 11 FORMAT III — WHAT IT MEANS -------------------------------------------
    s = d.light()
    d.header(s, "50 – 70 min", "What that means for how a session runs")
    d.title(s, "So here is what happens every Tuesday and Thursday")
    for i, (t, k, txt) in enumerate([
            ("0–5", "Retrieval, notes closed", "Two questions from last session, one from three or four back. It will feel like a quiz. It is not graded — retrieving is what makes it stick."),
            ("8–20", "You try it first", "A problem you cannot yet solve, in groups. Getting it wrong is the intended outcome; the attempt is what makes the explanation land."),
            ("20–48", "The concept, in three pieces", "Each ending in a vote, a two-minute argument with your neighbour, and a second vote. I will quote your solutions back by name."),
            ("50–72", "Faded worked examples", "Four versions of one problem, each with less of my working shown. Start wherever the scaffolding stops helping you — nobody announces where that is."),
            ("72–80", "Close the loop", "Back to the opening questions, in writing, notes closed. Then one slide on why the next session exists.")]):
        y = 1.9 + i * 0.95
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.95, 0.42, fill=TEAL, line=None)
        d.text(s, t, M, y + 0.09, 0.95, 0.3, size=11, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 1.2, y, 3.4, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.75, y + 0.02, 7.15, 0.85, size=12.5, color=BODY)
    d.foot(s, "The full design, with the evidence and its grade, is in docs/lecture-design.md. Read it if you want to argue with it — several of the choices are convention, and they are labelled as convention.")
    d.notes(s, "Publishing the pedagogy is unusual and it is worth saying out "
               "loud that you are doing it. It converts 'trust me' into "
               "'here is the argument, and here is where it is weak'.")

    # 12 FORMAT IV — THE DEAL -------------------------------------------------
    s = d.dark()
    d.header(s, "50 – 70 min", "The deal")
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

    # 13 MECHANICS ------------------------------------------------------------
    s = d.light()
    d.header(s, "70 – 76 min", "Mechanics  ·  details on bCourses")
    d.title(s, "How the course is run")
    for i, (k, v, note) in enumerate([
            ("Problem sets", "30%", "Nine sets, lowest two dropped. Notebooks, autograded where the answer is a number, read by a human where it is an argument."),
            ("Midterm", "15%", "Thursday 15 October, sessions 1–13. Scope published two weeks out, in writing."),
            ("Final", "25%", "Cumulative, weighted to the second half."),
            ("Project", "30%", "Design a system, in a team. Description due session 9; you will be given the specification format.")]):
        y = 1.95 + i * 0.92
        d.text(s, k, M, y, 2.4, 0.4, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, v, M + 2.5, y - 0.04, 1.0, 0.45, size=22, font=HEAD,
               bold=True, color=TEAL)
        d.text(s, note, M + 3.8, y + 0.02, 8.1, 0.8, size=13, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.7, W - 2 * M, 1.0, fill=WASH,
            line=TEAL, lw=1.5)
    d.text(s, "TONIGHT", M + 0.3, 5.85, 1.5, 0.28, size=10, bold=True, color=TEAL)
    d.text(s, "PS0 — ten minutes, ungraded, due Tuesday. It proves your computing environment works so that nothing about the tooling is a surprise in week 3. Link on bCourses; sign in to DataHub with CalNet, or use the Colab badge.",
           M + 0.3, 6.15, 12.0, 0.5, size=13.5, color=BODY)
    d.notes(s, "Six minutes, and no more. Everything here is in the syllabus; "
               "the reason to say it aloud is that the assessment weights change "
               "what students do, and PS0 has a deadline. "
               "247 students: mention the additional project requirement here, "
               "not on a slide -- it is four people.")

    # 14 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "76 – 80 min", "Next")
    d.title(s, "You listed what you would need to know. Start with the cell.")
    d.text(s, "Tuesday: the cell as a physical substrate.", M, 2.15, 11.6, 0.45,
           size=24, font=HEAD, bold=True, color=MINT)
    d.text(s, "Every specification you wrote today assumes a thing that senses, computes and acts. That thing is about one femtolitre, roughly a fifth protein by weight, and it divides in twenty minutes.\n\nHow many copies of your sensor protein are in there? How long does one of them take to cross the cell? Is 'concentration' even the right variable at that copy number?",
           M, 2.85, 11.6, 2.0, size=17, color=WHITE, spacing=1.4)
    d.text(s, "You cannot design anything until you can answer those in your head, to an order of magnitude.",
           M, 5.0, 11.6, 0.4, size=16, bold=True, color=CYAN)
    bottom = d.assignment(s, y=5.55)
    d.text(s, "No reading before Tuesday. Do PS0.", M, 5.65, 11.6, 0.35,
           size=15, bold=True, color=SILVER)
    d.notes(s, "Pose it as a constraint on Tuesday's problem, not a summary of "
               "today. The three questions on this slide are the S2 retrieval "
               "opener, verbatim -- that is deliberate.")

    return d
