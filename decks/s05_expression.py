"""Session 5 — Gene expression dynamics: response time, dilution, and the floor.

Thursday 10 September. **First session built to the revised standard** in
docs/lecture-design.md §5b and §5c: derivations live on slides as step-slide
runs, the board keeps only the ledger, and every student activity is the same
rhythm — pose, work on paper, silent vote, discuss.

    0–5    retrieval (2 from Tuesday, 1 interleaved from session 2)
    5–8    map + goals as questions
    8–18   DERIVATION 1 — the expression equation, its steady state, its clock
    18–24  rhythm 1 — which knob moves the level? which moves the speed?
    24–34  DERIVATION 2 — response time, and why alpha is not in it
    34–40  rhythm 2 — you double the promoter strength. What happens to t_1/2?
    40–48  the floor: dilution you cannot switch off, and Andersen's four tags
    48–50  pause (individual, not collected)
    50–64  faded set, items 1 and 2 — fitting a removal rate from decay data
    64–70  the answers
    70–76  the design trade, priced
    76–80  consolidation, the reading, forward link

WHAT THIS SESSION OWES PS2
- T10 response time, t_1/2 = ln2/(gamma + mu): derivation 2 and the faded set.
- T11 dilution vs degradation, and what a degradation tag does to circuit speed:
  the floor segment, with Andersen's measured half-lives.
- T12 steady-state level from a production/removal balance: derivation 1.

THE NUMBERS, computed and not asserted (E. coli, 30 min doubling, mu = ln2/30):
    tag     t_1/2 degradation   gamma+mu    t_1/2 total   p* relative
    none          --             0.0231        30.0 min      1.00
    ASV          110 min         0.0294        23.6 min      0.79
    AAV           60 min         0.0347        20.0 min      0.67
    LVA/LAA       40 min         0.0404        17.1 min      0.57
The whole session lands on the last two columns: the strongest tag in Andersen
buys 1.75x in speed and costs 43% of the steady-state level, because one knob
moves both. That is session 3's ConcepTest 2 collision with measured numbers on
it, and it is the reason session 7 goes looking for a second knob.

Coverage matrix: T10, T11, T12.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session05_Expression"


def build():
    d = Deck("Session 5 — Gene expression dynamics", session=5)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 5", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Gene expression dynamics", M, 2.72, 9.4, 1.3,
           size=40, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Response time, dilution, and the floor you cannot get under",
           M, 4.15, 9.4, 0.5, size=17, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "PS1 closes tonight at 23:59. PS2 posts today.\n"
               "Andersen 1998 was assigned Tuesday. Ask who has read it before "
               "you need it at 40 min, so you know what you are working with.\n"
               "The two most common answers from Tuesday's slips open the "
               "retrieval.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions, notes closed")
    for i, (n, src, q, c) in enumerate([
            ("1", "From Tuesday",
             "You double the enzyme in an assay. Which of K_{M} and V_{max} moves, and why does the other not?", TEAL),
            ("2", "From Tuesday",
             "State the condition under which Michaelis–Menten is safe — as a condition on concentrations, not in words.", TEAL),
            ("3", "From session 2",
             "An E. coli cell divides every 30 minutes. A protein in it is chemically perfectly stable. How long does it stay around?", CYAN)]):
        y = 1.9 + i * 1.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.15, fill=c, line=None)
        d.text(s, n, M, y + 0.38, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, src, M + 0.8, y, 3.0, 0.3, size=11.5, bold=True, color=c)
        d.text(s, q, M + 0.8, y + 0.3, 11.7, 0.85, size=15.5, color=BODY)
    d.text(s, "Two minutes in writing. Then we take answers — including the ones you are unsure of.",
           M, 6.45, W - 2 * M, 0.4, size=15, bold=True, color=INK)
    d.notes(s, "Q1: V_max = k_2 E_tot moves; K_M = (k_-1+k_2)/k_1 has no E in "
               "it.\n"
               "Q2: E_tot << K_M + S_0. Watch for E << S, which is Tuesday's "
               "whole point and is what PS1 Q3a is marking.\n"
               "Q3 is the interleaved one and it is today's hinge. The answer "
               "is that it halves every 30 minutes anyway, because the cell "
               "divides and the protein is shared out. Chemical stability is "
               "not persistence. If they get this, the next thirty minutes are "
               "a formalization of something they already believe.\n"
               "Say: 'Two minutes in writing.'")

    # 2b WHY THIS SESSION EXISTS ----------------------------------------------
    # TEMPLATE for the sessions 5-8 openers (design-notes, 7 Sep 2026). Three
    # minutes, one artifact, one number, and it must be examinable -- the test
    # from "Choices worth arguing about" applies here too, or it is a seminar.
    # For the other three: pick something that was BUILT, name what it could not
    # do before, and make the fix the thing you are about to derive.
    #
    # The network is drawn in our own notation (figures/s05_expression.py) and
    # the DATA are Elowitz & Leibler's, embedded through paper_figure() so the
    # public build shows a labelled slot and the classroom build shows the real
    # panel. See private/paper-figures/README.md.
    s = d.light()
    d.header(s, "5 – 8 min", "Why anyone needed this")
    d.title(s, "For thirty years you could not watch a gene switch off")
    for i, (k, txt, c) in enumerate([
            ("GFP was too good",
             "Wild-type GFP is chemically stable for days. Induce a promoter and the signal climbs; switch the promoter OFF and it just sits there.",
             TEAL),
            ("So you could measure ON, never OFF",
             "No response time, no recovery, no oscillation. A field that could see steady states and nothing else.",
             CYAN),
            ("Andersen's fix was eleven amino acids",
             "An ssrA tag recruits the ClpXP protease. Four variants, four half-lives, 1998 — and it is today's reading.",
             TEAL)]):
        y = 1.80 + i * 1.22
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.11, 1.02, fill=c, line=None)
        d.text(s, k, M + 0.32, y - 0.02, 5.1, 0.5, size=15, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 0.32, y + 0.40, 5.2, 0.78, size=13.5, color=BODY)

    # Slot geometry is derived from the images, not guessed: the ring PNG is
    # 890x658 (aspect 1.353) and the Elowitz crop 1448x1192 (aspect 1.215).
    # Sized by eye at 3.15x1.78 and 2.91x1.78 they filled 76% and 74% of the
    # space they reserved, which is the "loose slot" the build warns about --
    # and, being height-limited, the Elowitz trace was smaller than the room
    # could read. Common height 2.35in is the largest that still leaves the
    # caption and the closing box their space.
    d.image(s, "figures/build/s05_repressilator_ring.png", 6.35, 1.45, 3.18, 2.35)
    d.paper_figure(s, "elowitz2000_fig2", 9.78, 1.45, 2.86, 2.35,
                   "Elowitz & Leibler, Nature 2000, Fig. 2",
                   "fluorescence oscillations in single cells")
    d.text(s, "Two years after Andersen, Elowitz & Leibler tagged all three repressors the same way. Without fast degradation the only removal is dilution — and the period they measured, about 150 min, is threefold longer than the cells' own division time.",
           6.35, 4.15, 6.28, 1.0, size=14, color=BODY)

    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.62, W - 2 * M, 0.95, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "The number that made all of this necessary, and the one we derive today: an untagged protein in a cell dividing every 30 minutes still has a half-life of 30 minutes.",
           M + 0.3, 5.85, 11.6, 0.6, size=17, bold=True, color=INK)
    d.notes(s, "Three minutes. One artifact, one number, then move.\n"
               "Not history for its own sake: the quantity we are about to "
               "derive - a removal rate - was a hard experimental barrier for a "
               "whole field, and someone removed it with a peptide tag.\n"
               "The ring is drawn in our notation; the oscillation panel is "
               "Elowitz & Leibler's and is cited on the slide.\n"
               "The closing number IS the session: dilution alone gives a "
               "30-minute half-life and no promoter change touches it. That is "
               "retrieval question 3 restated as a design constraint.\n"
               "The repressilator is a forward hook to session 11. Name it, do "
               "not explain it. If pressed: period about 150 min against a "
               "50-70 min division time, both from the paper.\n"
               "Ask: what can you not measure, if you can only watch a signal "
               "go up?")

    # 3 GOALS -----------------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By the end you should be able to answer")
    for i, (n, lab) in enumerate([("3", "Modeling I"), ("4", "Modeling II"),
                                  ("5", "Expression"), ("6", "Promoters"),
                                  ("7", "Autoregulation")]):
        x, here = M + i * 2.42, n == "5"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=13.5, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "Your circuit has to respond in ten minutes. Your host divides every thirty. Is that possible at all?",
            "A degradation tag makes a protein disappear faster. What does it cost you, and can you get the cost back?",
            "Which parameter in an expression model sets the steady-state level, which sets the speed, and why is that the same parameter?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.coming_up(s, y=6.5)
    d.notes(s, "Questions, not statements.\n"
               "The first is the one to leave hanging — it is the design "
               "question the whole session answers, and the honest answer is "
               "'only if you pay for it'.\n"
               "The BUILDING TOWARD line is new. Say it once, out loud: the "
               "next four sessions are the machinery for understanding why "
               "Gardner's toggle works, and you read that paper on 24 "
               "September. Four derivations in a row need a destination.")

    # 4 DERIVATION 1 — the equation and its steady state ----------------------
    # Step-slide run, per lecture-design.md 5b. Five steps, five surfaces, the
    # last carrying the whole argument for anyone reading the PDF afterwards.
    d.derivation(
        None, "8 – 18 min", "Built one line at a time",
        "Where a protein concentration settles, and why",
        [("Write down what makes it and what removes it",
          "dp/dt  =  \u03b1  \u2212  \u03b3 p  \u2212  \u03bc p",
          "\u03b1 is production, \u03b3 degradation, \u03bc growth \u2014 and only one of the three is chemistry"),
         ("Growth removes protein without touching a single molecule",
          "\u03bc  =  ln2 / T_{d}        T_{d} = 30 min  \u2192  \u03bc = 0.023 min\u207b\u00b9",
          "the cell divides and the protein is shared out \u2014 retrieval question 3, written as a rate"),
         ("So the two removal terms are the same kind of term",
          "dp/dt  =  \u03b1  \u2212  (\u03b3 + \u03bc) p",
          "they add: nothing here distinguishes destroying a molecule from diluting it"),
         ("Set the derivative to zero for the steady state",
          "p*  =  \u03b1 / (\u03b3 + \u03bc)",
          "a balance, not an equilibrium \u2014 both processes run the whole time"),
         ("And read what each knob does",
          "\u03b1 \u2191  raises p*        (\u03b3 + \u03bc) \u2191  lowers p*",
          "two knobs for one number. Which one you turn is the whole of today")],
        closing="p* = \u03b1/(\u03b3 + \u03bc). Hold that; the next ten minutes are about how long it takes to get there.",
        board="LEFT WING, and leave it up all period:   p* = \u03b1/(\u03b3+\u03bc)   and   \u03bc = 0.023 min\u207b\u00b9",
        note=("Build it with them; ask for each term before it appears.\n"
              "The move that matters is step 2. Dilution is a removal rate with "
              "units of inverse time, exactly like degradation, and it is there "
              "whether or not the protein is stable. Retrieval Q3 is this.\n"
              "mu = ln2/30 = 0.023 per min. Put it on the ledger; every number "
              "for the rest of the session uses it.\n"
              "Step 4: name it a balance rather than an equilibrium. Nothing "
              "has stopped; production and removal are equal.\n"
              "LEDGER, left wing, stays up all period: "
              "p* = alpha/(gamma+mu) and mu = 0.023/min."))

    # 5 RHYTHM 1 --------------------------------------------------------------
    s = d.light()
    d.header(s, "18 – 24 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "You swap in a promoter twice as strong.")
    d.text(s, "Same protein, same host, same growth rate. Only \u03b1 doubles. Work it on paper before you vote.",
           M, 1.95, 12.5, 0.5, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "p* doubles, and it gets there twice as fast."),
            ("B", "p* doubles, and the time to get there is unchanged."),
            ("C", "p* is unchanged, and it gets there twice as fast."),
            ("D", "Both change, but not by a factor of two.")]):
        y = 2.75 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "Three minutes on paper. Then vote with your eyes down, argue with the person next to you, and vote again.", 6.3)
    d.notes(s, "Answer B. p* = alpha/(gamma+mu) doubles. The approach rate is "
               "(gamma+mu), which contains no alpha at all, so the time to get "
               "there does not move.\n"
               "A is the majority first answer: 'stronger promoter, faster "
               "response' is the intuition every engineer arrives with, and it "
               "is wrong.\n"
               "They cannot fully justify B yet — the solution is the next "
               "derivation. That is deliberate. Take the vote, take the "
               "argument, and do not resolve it; let the derivation resolve it.\n"
               "First vote eyes down. Record the distribution.")

    # 6 DERIVATION 2 — response time ------------------------------------------
    d.derivation(
        None, "24 – 34 min", "Built one line at a time",
        "How long it takes, and what that does not depend on",
        [("Solve it. One line, and it is separable",
          "p(t)  =  p* [ 1 \u2212 e\u207b\u207d\u03b3\u207a\u03bc\u207e\u1d57 ]",
          "from an empty cell. The shape is always this; only the constants differ"),
         ("Ask when it is half way there",
          "p(t\u00bd) = p*/2   \u21d2   e\u207b\u207d\u03b3\u207a\u03bc\u207e\u1d57 = \u00bd",
          "the definition of response time in this course, and the one PS2 uses"),
         ("Take logs",
          "t\u00bd  =  ln2 / (\u03b3 + \u03bc)",
          "no \u03b1 \u2014 the vote is settled: promoter strength is not in this expression"),
         ("Which is the collision session 3 promised you",
          "\u03b1  \u2192  level only        (\u03b3 + \u03bc)  \u2192  level AND speed",
          "one knob is clean, the other is coupled \u2014 and only the coupled one changes the speed")],
        closing="t\u00bd = ln2/(\u03b3 + \u03bc), and it is the same denominator as p*. Speed and level share a knob.",
        board="LEFT WING, under p*:   t\u00bd = ln2/(\u03b3 + \u03bc)",
        note=("Separable, one line, and the exponential shape is worth naming: "
              "everything first-order approaches its steady state this way, and "
              "they will see it again in session 7 and session 11.\n"
              "Step 3 settles the vote. Say so explicitly and point at the "
              "board — alpha is absent, so B was right.\n"
              "Step 4 is the session's argument. It is session 3's ConcepTest 2 "
              "with real parameters: the only knob that changes the speed also "
              "changes the level.\n"
              "LEDGER, left wing, under p*: t_half = ln2/(gamma+mu).\n"
              "Ask: so if you need it faster, what are you allowed to touch?"))


    # 7 RHYTHM 2 --------------------------------------------------------------
    s = d.light()
    d.header(s, "34 – 40 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "Your circuit must respond in ten minutes.")
    d.text(s, "Your host divides every thirty. The protein is chemically stable: \u03b3 = 0. Work out t\u00bd before you vote.",
           M, 1.95, 12.5, 0.5, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "Fine — response time has nothing to do with division."),
            ("B", "t\u00bd = 30 min. Use a stronger promoter to get to ten."),
            ("C", "t\u00bd = 30 min, and no promoter change will fix it."),
            ("D", "t\u00bd = 10 min already, if \u03b1 is large enough.")]):
        y = 2.75 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "Two minutes on paper — you have both formulas on the board. Eyes down to vote.", 6.3)
    d.notes(s, "Answer C. With gamma = 0, t_half = ln2/mu = the doubling time "
               "exactly, 30 min. And alpha is not in t_half, so no promoter "
               "swap touches it.\n"
               "B is the majority answer and it is the same mistake as the "
               "last vote, one derivation later. Worth naming that out loud "
               "rather than just marking it wrong: the intuition survives "
               "being corrected once.\n"
               "D confuses reaching a high level with reaching it quickly.\n"
               "The consequence is the next segment: the ONLY way to get under "
               "the doubling time is to make gamma non-zero. Ask what that "
               "means physically before you show the paper.")

    # 8 THE FLOOR -------------------------------------------------------------
    s = d.light()
    d.header(s, "40 – 44 min", "Andersen 1998, Figure 3A")
    d.title(s, "Dilution is a floor. A tag is how you push against it.")
    d.image(s, "figures/build/s05_response_tags.png", M + 0.2, 1.5, 7.4, 4.4)
    for i, (k, txt) in enumerate([
            ("\u03bc is not optional",
             "it is set by the host and the medium, not by your construct. At 30 min doubling, \u03bc = 0.023 min\u207b\u00b9 and t\u00bd \u2264 30 min no matter what you build."),
            ("\u03b3 is the knob you added",
             "an ssrA tag recruits ClpXP. Andersen measured four of them, and the half-lives are the paper's whole contribution: 40, 40, 60, 110 min."),
            ("Together they set one number",
             "t\u00bd = ln2/(\u03b3 + \u03bc). Adding the strongest tag takes 30 min down to 17.1 \u2014 a factor of 1.75, and that is the best on offer."),
            ("And you paid for it",
             "p* = \u03b1/(\u03b3 + \u03bc) fell by the same factor. Same promoter, 57% of the protein.")]):
        y = 1.6 + i * 1.12
        d.shape(s, S.ROUNDED_RECTANGLE, M + 8.0, y, 0.11, 0.95, fill=TEAL,
                line=None)
        d.text(s, k, M + 8.25, y - 0.02, 4.3, 0.4, size=14, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 8.25, y + 0.36, 4.3, 0.75, size=12.5, color=BODY)
    d.foot(s, "Half-lives from Andersen et al. 1998 Fig 3A, measured after a medium downshift — so they are degradation alone, with dilution switched off.", 6.5)
    d.notes(s, "This is the reading. Ask what Figure 3A actually plots before "
               "you interpret it.\n"
               "The measurement detail matters and it is worth thirty seconds: "
               "the downshift arrests growth, so mu goes to zero and what "
               "Andersen reports is gamma alone. That is why we can add it to "
               "our own mu rather than double-counting.\n"
               "Numbers on the ledger: mu = 0.023, LAA gamma = ln2/40 = 0.017, "
               "sum 0.040, t_half = 17.1 min.\n"
               "The four rows in the table are the four columns of PS2 Q1.\n"
               "Ask: you need ten minutes and the best tag gives you "
               "seventeen. What now? Answers worth having: divide faster "
               "(change mu), or stop asking for a concentration change and "
               "start asking for an activity change - which is session 21.")

    # 9 PAUSE -----------------------------------------------------------------
    s = d.dark()
    d.header(s, "48 – 50 min", "Two minutes  ·  your own notes")
    d.title(s, "Two minutes. Fix your own notes.")
    d.text(s, "Not a break, and nothing to hand in. Find the one line in the last forty minutes you could not reconstruct on your own, and write it out properly.",
           M, 2.2, 11.9, 0.9, size=20, color=WHITE, spacing=1.3)
    d.text(s, "Then: handouts.", M, 3.9, 11.9, 0.5, size=22, font=HEAD,
           bold=True, color=CYAN)
    d.foot(s, "If nothing comes to mind, work out what t\u00bd would be for a protein with a 10-minute degradation half-life in a cell that divides every 20.", 6.3)
    d.notes(s, "Say nothing for the full two minutes. Stand at the back.\n"
               "Nothing is collected. The foot line is there so the students "
               "who think they are done have something real to do.\n"
               "Answer to the foot line: 1/(1/10 + 1/20) = 6.7 min.\n"
               "Hand the paper out during the second minute.")


    # 10 FADED SET ------------------------------------------------------------
    s = d.light()
    d.header(s, "50 – 58 min", "Handout  ·  items 1 and 2  ·  eight minutes")
    d.title(s, "Getting a removal rate out of real decay data")
    for i, (n, k, txt, c) in enumerate([
            ("1", "Fully worked — one variant",
             "Semi-log plot, slope, and the half-life that comes out of it. Read it; do not copy it.", TEAL),
            ("2", "The last steps are yours — a second variant",
             "Same four steps, different numbers, and then: is this \u03b3, or is it \u03b3 + \u03bc? The answer depends on how the experiment was run.", CYAN),
            ("3", "On PS2 — the design question",
             "You need t\u00bd = 12 min in a host that divides every 25. Which tag, and what does it cost you?", MUTED),
            ("4", "On PS2 \u00b7 247",
             "Production is not a step change: \u03b1 ramps. Solve for p(t) and say when the response-time formula stops being the right description.", MUTED)]):
        y = 1.85 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.9, fill=c, line=None)
        d.text(s, n, M, y + 0.26, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 4.4, 0.4, size=14.5, font=HEAD, bold=True,
               color=INK if i < 2 else MUTED)
        d.text(s, txt, M + 5.4, y + 0.02, 6.9, 0.9, size=13, color=BODY if i < 2 else MUTED)
    d.text(s, "Eight minutes, and only the first two. We start item 3 together at 62 min; PS2 is where you finish it.",
           M, 6.45, W - 2 * M, 0.45, size=15, bold=True, color=INK)
    d.notes(s, "Item 1 is worked. They read it and start at item 2 if the "
               "first is obvious.\n"
               "The error to watch for while circulating: reading a slope off "
               "a semi-log plot as a half-life without the ln2. The other one "
               "is quoting a rate with no units.\n"
               "Item 2's real question is whether the measured decay is gamma "
               "or gamma+mu, and the answer is that it depends on whether the "
               "cells were growing. That is Andersen's downshift, and it is "
               "the most common way to misread a stability measurement.\n"
               "Say: 'Eight minutes. Items one and two only.'")

    # 11 THE ANSWERS ----------------------------------------------------------
    s = d.light()
    d.header(s, "58 – 62 min", "The answers  ·  items 1 and 2")
    d.title(s, "A slope is a rate. A rate is not a half-life.")
    for i, (n, ans, prompt, c) in enumerate([
            ("1",
             "slope of ln p against t is \u2212(\u03b3 + \u03bc);  t\u00bd = ln2 / (\u03b3 + \u03bc)",
             "The factor of ln2 is where most of the marks go. A slope of \u22120.04 min\u207b\u00b9 is a rate constant, and the half-life is 17 min, not 25. Units are the check: the slope is per minute, a half-life is minutes.",
             TEAL),
            ("2",
             "growing cells give \u03b3 + \u03bc;  arrested cells give \u03b3 alone",
             "So a number quoted as 'the half-life of this protein' is only \u03b3 if the experiment stopped growth first. Andersen's downshift does exactly that, which is why his numbers can be added to your own \u03bc instead of replacing it.",
             CYAN)]):
        y = 1.9 + i * 2.0
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.6, fill=c, line=None)
        d.text(s, n, M, y + 0.6, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, ans, M + 0.8, y, 11.7, 0.5, size=16, font=HEAD, bold=True,
               color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, M + 0.8, y + 0.58, 0.1, 0.95,
                fill=MUTED, line=None)
        d.text(s, prompt, M + 1.15, y + 0.55, 11.35, 1.0, size=13, color=BODY)
    d.text(s, "Every stability number in the literature is one of these two quantities, and papers do not always say which.",
           M, 6.3, W - 2 * M, 0.45, size=16, font=HEAD, bold=True, color=INK)
    d.notes(s, "Take both from the room before showing them.\n"
               "The ln2 is the mark most will drop. Units catch it: a slope is "
               "per minute, a half-life is minutes.\n"
               "The second one is the transferable habit — when you read a "
               "half-life, ask what was growing.")

    # 12 THE TRADE, PRICED ----------------------------------------------------
    s = d.light()
    d.header(s, "62 – 66 min", "The design question, with numbers on it")
    d.title(s, "Speed and level share one knob")
    d.image(s, "figures/build/s05_speed_level.png", M + 1.9, 1.45, 8.7, 4.0)
    d.text(s, "Every tag moves you left AND down. To get back the level you lost you have to raise \u03b1 — a second knob, and the reason session 7 goes looking for one.",
           M, 5.65, 12.5, 0.5, size=17, font=HEAD, bold=True, color=INK)
    d.foot(s, "Item 3 of your handout is this question with numbers on it. Four minutes on it now.", 6.4)

    # 12b RHYTHM 3 — pose ------------------------------------------------------
    s3 = d.light()
    d.header(s3, "66 – 71 min", "Pose  ·  paper")
    d.title(s3, "t\u00bd = 12 min, in a host that divides every 25.")
    d.text(s3, "Handout item 3. Which of Andersen's tags gets you there, and what level do you end up with? Four minutes, on your own.",
           M, 2.0, 12.5, 0.55, size=20, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "LAA/LVA, and you keep about 90% of the level."),
            ("B", "LAA/LVA, and you keep about 60%."),
            ("C", "None of them gets you to 12 min in that host."),
            ("D", "AAV is enough, and it costs least.")]):
        y = 2.9 + i * 0.8
        d.shape(s3, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s3, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True,
               color=WHITE, align="c")
        d.text(s3, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s3, "Everything you need is the two lines on the left wing and one row of the table. Eyes down to vote.", 6.3)
    d.notes(s3, "Four minutes on paper before any vote. Circulate.\n"
                "The arithmetic: T_d = 25 gives mu = 0.0277. Wanting t_half = "
                "12 needs gamma + mu = ln2/12 = 0.0578, so gamma = 0.0301, a "
                "degradation half-life of 23.1 min.\n"
                "Andersen's best is 40 min. So no tag in that paper reaches it, "
                "and C is correct.\n"
                "Do not signal that. Take the vote first.")

    # 12c RHYTHM 3 — resolve ---------------------------------------------------
    s4 = d.dark()
    d.header(s4, "71 – 76 min", "Vote  ·  argue  ·  vote again")
    d.title(s4, "C. The specification is not purchasable.")
    for i, (k, txt) in enumerate([
            ("What you need",
             "T_{d} = 25 \u2192 \u03bc = 0.0277. t\u00bd = 12 needs \u03b3 + \u03bc = 0.0578, so \u03b3 = 0.0301 \u2014 a degradation half-life of 23.1 min."),
            ("What exists",
             "Andersen's best is 40 min. With LAA you reach ln2/(0.0173 + 0.0277) = 15.4 min, and 62% of the level. Close, and not 12."),
            ("So the honest answer is not a tag",
             "you change the host, you change the specification, or you stop asking for a concentration to move and ask for an activity to move instead \u2014 which is session 21.")]):
        y = 2.1 + i * 1.25
        d.shape(s4, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.05, fill=CYAN, line=None)
        d.text(s4, k, M + 0.4, y, 4.4, 0.5, size=15, font=HEAD, bold=True,
               color=WHITE)
        d.text(s4, txt, M + 5.1, y - 0.02, 7.3, 1.1, size=14, color=MINT)
    d.foot(s4, "Most specifications you will be handed are like this one. Finding out early is the cheapest thing modelling does for you.", 6.3)
    d.notes(s4, "B is the majority answer and it is a good one - it is right "
                "about the tag and wrong about whether it clears the bar.\n"
                "The point is not that they got it wrong. It is that four "
                "minutes of arithmetic told them a specification was "
                "unreachable before anyone cloned anything, and that is what "
                "the whole session has been for.\n"
                "Record the distribution.\n"
                "PS2 Q2 is this question with a different host.")
    d.notes(s, "Start item 3 in the room, do not finish it.\n"
               "The point of the figure is that there is no point on it that is "
               "both fast and high with a single knob. Speed costs level, "
               "one for one, because both are ln2/(gamma+mu) and "
               "alpha/(gamma+mu).\n"
               "Ask: how would you get both? Raise alpha as well. That is two "
               "knobs for two requirements, which is the first time in this "
               "course that a design has needed more than one, and it is what "
               "autoregulation buys you in session 7 without the extra part.")

    # 13 CONSOLIDATION --------------------------------------------------------
    s = d.dark()
    d.header(s, "76 – 80 min", "Next")
    d.title(s, "Now: where does \u03b1 come from?")
    d.text(s, "Tuesday: promoter occupancy from statistical mechanics.",
           M, 2.05, 11.6, 0.45, size=22, font=HEAD, bold=True, color=MINT)
    d.text(s, "Today \u03b1 was a constant you were handed. It is not — it is a rate set by how often RNA polymerase is bound, which is set by how many transcription factors are around. That is the last piece of machinery Part I needs, and it is where the Hill function you derived on Tuesday actually comes from.",
           M, 2.62, 11.6, 1.15, size=16, color=WHITE, spacing=1.35)
    d.text(s, "What determines how much of the time a promoter is occupied?",
           M, 3.95, 11.6, 0.4, size=17, bold=True, color=CYAN)
    bottom = d.assignment(s, y=4.5)
    d.text(s, "PS1 closes tonight. PS2 posts today and is due 17 September.",
           M, bottom + 0.12, 11.6, 0.35, size=15, bold=True, color=SILVER)
    d.notes(s, "Last two minutes: notes closed, one sentence each on the three "
               "questions from the goals slide.\n"
               "Assign the reading out loud: Bintu 2005, Figures 1 and 2, in "
               "Files > readings on bCourses. Skip Figure 3 for now.\n"
               "Leave the forward question unanswered.")

    return d
