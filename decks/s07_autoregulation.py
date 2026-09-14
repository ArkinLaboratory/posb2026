"""Session 7 — Autoregulation: buying speed without paying for it.

Thursday 17 September. Built 12 September to the session 6 lessons: the object
before the model, one mathematical move per surface, and every segment landing
on something a designer can choose.

Revision 2, same day: the first build put 6, 6 and 8 minutes on single surfaces
-- the pacing check called all three "you would be improvising" -- so each is
now a run of short surfaces, and the biology that session 6's review said was
missing (the wiring, drawn, before any curve) opens the session. 34 surfaces.

    0–5    retrieval (2 from Tuesday, 1 interleaved from session 5)
    5–8    map + goals as questions
    8–10   Tuesday's unanswered question — take the vote, do not resolve
    10–12  the WIRING — autoregulation as one edit to session 6's promoter
    12–14  THE OBJECT — production and removal on one pair of axes
    14–16  how to READ that picture: crossing, sign of the gap, steepness
    16–26  DERIVATION 1 — the cost identity, and the vote resolved
    26–32  rhythm 1 — what would NAR have to cost?
    32–44  DERIVATION 2 — negative autoregulation, graphically then exactly
    44–47  Rosenfeld 2002 — the design and the control, before any result
    47–50  Rosenfeld 2002 — the result, and why 5x measured vs 1.8x derived
    50–56  rhythm 2 — which curve is the expensive one?
    56–65  handout, items 1 and 2
    65–69  the answers
    69–71  POSITIVE autoregulation — what the production curve looks like
    71–74  the third crossing, and the geometric condition for it
    74–77  what two stable states buy you, and what they cost
    77–81  variance, and the limit of the model on the board
    81–84  the design ledger
    84–87  consolidation

WHAT THIS SESSION OWES PS3 AND THE MIDTERM
- T15 derive the negative-autoregulation speed-up: derivations 1 and 2.
- T16 positive autoregulation -> graphical bistability condition: 69-77 min.
- T17 variance reduction under NAR: 77-81, stated with its mechanism and with
  the derivation explicitly deferred to session 12. NOT assessed on PS3 -- the
  assessment moved to PS6 on 14 September, after session 12 gives them the
  Gillespie sampler and the CV to measure it with. See the coverage matrix.

THE NUMBERS, all computed in figures/s07_autoregulation.py and none asserted:
    route                      t1/2     steady-state synthesis
    do nothing                 30.0     23.1 protein/min
    LAA tag, alpha raised      17.1     40.4 protein/min   1.75x, forever
    NAR, repression ratio 2    16.8     23.1 protein/min   transient only

Speed-ups: the tag buys 1.75x, NAR at repression ratio 2 buys 1.79x. The
repression ratio matching the tag exactly is 1.94.

The repression ratio of 2 sits just short of the value at which NAR matches the
strongest tag in Andersen 1998, which is 1.94 (solved for, not guessed). At 2
the circuit gives 1.79x against the tag's 1.75x -- the same number to within the
precision of a measured half-life, and NOT to be claimed as a win. The claim
worth making is that NAR matches the best tag WITHOUT moving the removal line.
The slide aside and the answer sheet were both corrected on 14 September; if you
change one, change the other.

Coverage matrix: T15, T16 (assessed PS3); T17 (demonstrated here, assessed PS6).
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session07_Autoregulation"


def build():
    d = Deck("Session 7 — Autoregulation", session=7)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 7", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Autoregulation", M, 2.72, 9.4, 1.3,
           size=40, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Buying speed without paying for it",
           M, 4.15, 9.4, 0.5, size=20, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=14, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "PS2 is due today. PS3 posts today and carries five techniques, "
               "three of them from this session.\\n"
               "Rosenfeld 2002 was handed out on Tuesday. Ask who has read it "
               "before you need it at 44 min.\\n"
               "Tuesday's closing question is the opener. Do not recap the "
               "whole of session 6 first.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions, notes closed")
    for i, (n, src, q, c) in enumerate([
            ("1", "From Tuesday",
             "You measured a fold-change. Name one thing that cancelled out of it and say why that matters for reusing the part.", TEAL),
            ("2", "From Tuesday",
             "A helper operator raises the slope and not the ceiling. Which parameter sets the ceiling?", TEAL),
            ("3", "From session 5",
             "p* = α/(γ+μ) and t½ = ln2/(γ+μ). If I double γ+μ, what happens to each?", CYAN)]):
        y = 1.9 + i * 1.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.15, fill=c, line=None)
        d.text(s, n, M, y + 0.38, 0.5, 0.35, size=20, bold=True, color=WHITE,
               align="c")
        d.text(s, src, M + 0.8, y, 3.0, 0.3, size=13, bold=True, color=c)
        d.text(s, q, M + 0.8, y + 0.3, 11.7, 0.85, size=16, color=BODY)
    d.text(s, "Two minutes in writing. Question 3 stays on the board all period.",
           M, 6.45, W - 2 * M, 0.4, size=16, bold=True, color=INK)
    d.notes(s, "Q1: the core promoter, p. Also N_NS, the polymerase count and "
               "both binding energies. The reuse consequence is the "
               "composability result from Tuesday — the same part on any weak "
               "promoter reports the same fold-change.\\n"
               "Q2: f, the enhancement factor. omega only sharpens.\\n"
               "Q3 is the interleaved one and it is today's hinge. p* halves "
               "and t_half halves. ONE knob moved BOTH, and that is the "
               "problem this session solves.\\n"
               "LEAVE Q3 ON THE BOARD. Derivation 1 points at it at 24 min.\\n"
               "Say: 'Two minutes in writing.'")

    # 3 GOALS -----------------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By the end you should be able to answer")
    for i, (n, lab) in enumerate([("5", "Expression"), ("6", "Promoters"),
                                  ("7", "Autoregulation"), ("8", "Phase plane"),
                                  ("9", "Bistability")]):
        x, here = M + i * 2.42, n == "7"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=14, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "You need a circuit twice as fast, at the same protein level. What does each way of getting it cost you, and for how long?",
            "A protein that activates its own promoter can sit at two different levels in two genetically identical cells. What has to be true for that?",
            "Two cells with the same average have different spreads. Which circuit gives you the tighter one, and can the equation on the board tell you?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.coming_up(s, y=6.5)
    d.notes(s, "Questions, not statements.\\n"
               "The third one has a deliberate sting in the tail — the honest "
               "answer at 77 minutes is no, the equation on the board cannot "
               "tell you, and that is why session 12 exists.")

    # 4 TUESDAY'S QUESTION -----------------------------------------------------
    s = d.light()
    d.header(s, "8 – 10 min", "Pose  ·  silent vote  ·  no resolution yet")
    d.title(s, "The question I left you with on Tuesday")
    d.text(s, "Two cells. One expresses a protein with a degradation tag, one without, and both hold the same steady level.",
           M, 1.90, 12.5, 0.85, size=20, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "The same. The levels are equal, so the spending is equal."),
            ("B", "The tagged cell spends more, and only while it is catching up."),
            ("C", "The tagged cell spends more, and never stops."),
            ("D", "The untagged cell spends more — it has to make up for dilution.")]):
        y = 3.05 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=16, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=18, color=BODY)
    d.foot(s, "Vote now. I am not telling you the answer — you are going to derive it in fifteen minutes, and the derivation is exact.", 6.35)
    d.notes(s, "Take the vote and record the distribution. Do NOT resolve.\n"
               "A is the majority answer. It is the intuition that a steady "
               "state is a state of rest, and it is wrong: a steady state is a "
               "balance between two processes that are both running the whole "
               "time. Session 5 said that once; today it costs money.\n"
               "B is the interesting wrong answer, because it is the right "
               "answer for the OTHER route they meet at 32 min.\n"
               "If someone gets C, ask them for the factor. They will not have "
               "it. That is the derivation.")

    # 5a WHAT AUTOREGULATION IS ----------------------------------------------
    s = d.light()
    d.header(s, "10 – 12 min", "The wiring, before any curve")
    d.title(s, "Autoregulation is one edit to Tuesday's promoter")
    d.image(s, "figures/build/s07_wiring.png", M + 0.65, 1.62, 11.0, 4.25)
    d.foot(s, "Everything you derived on Tuesday still holds. The only new thing is that the protein on the operator is the one this gene makes.", 6.20)
    d.notes(s, "Two minutes, and do not let it become a biology lecture — "
               "they built the promoter on Tuesday and this is one edit to "
               "it.\n"
               "Walk the top row first: constitutive, alpha is a NUMBER, and "
               "that is every model they have written so far.\n"
               "Middle row: the operator is bound by this gene's own product. "
               "Point at the loop. ASK: what does that do to alpha? Answer: "
               "it makes alpha a function of p. That is the whole session in "
               "one sentence and it is worth waiting for.\n"
               "Bottom row: same loop, opposite sign. Say you will come back "
               "to it at 69 min and move on — do not open bistability here.\n"
               "The fold-change they derived Tuesday is exactly what alpha(p) "
               "is built from: alpha(p) = alpha_max * F_reg(p). Say that "
               "sentence out loud; it is the bridge between the two "
               "sessions.")

    # 5b THE OBJECT ------------------------------------------------------------
    s = d.light()
    d.header(s, "12 – 14 min", "The object  ·  built with them, not shown")
    d.title(s, "Production and removal on one pair of axes")
    d.image(s, "figures/build/s07_three_curves.png", M, 1.35, 12.4, 4.4)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.92, W - 2 * M, 0.95, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "Everything today is this picture redrawn. The crossing is the steady state; how steeply the two curves meet is the response time; and a production curve that rises fast enough crosses three times.",
           M + 0.3, 6.06, 11.6, 0.7, size=16, bold=True, color=INK)
    d.notes(s, "Do not rush this. It is the object, and the whole session is "
               "read off it.\n"
               "Build the left panel with them. Production is flat — that is "
               "session 5, where alpha did not depend on p. Removal is a "
               "straight line through the origin, because dilution takes a "
               "FRACTION per minute. They cross once.\n"
               "Middle panel: the protein represses itself, so production "
               "falls as p rises. Same crossing point here BY CONSTRUCTION — "
               "we raised the promoter to put it there. That construction is "
               "the fair comparison and they should see it announced.\n"
               "Right panel: hold it for ten seconds, say three crossings, and "
               "move on. It comes back at 69 min.\n"
               "The board gets the axes and nothing else. They will draw these "
               "four times on the handout.")

    # 5c HOW TO READ IT --------------------------------------------------------
    s = d.light()
    d.header(s, "14 – 16 min", "Three things you read off one picture")
    d.title(s, "What the geometry tells you, before any algebra")
    for i, (n, k, txt, c) in enumerate([
            ("1", "Where they cross is the steady state",
             "production equals removal, so dp/dt = 0. Nothing else on the axes matters for the LEVEL. Production rate, synthesis rate, α — three names for this curve, and I will use all three.", TEAL),
            ("2", "Which side you are on tells you which way p moves",
             "above the crossing, removal wins and p falls; below it, production wins and p rises. That is why this crossing is stable — and it is the only stability argument you need today.", CYAN),
            ("3", "How steeply they meet is the response time",
             "a bigger gap between the curves just off the crossing means a bigger restoring flux, so the system returns faster. Speed is the SLOPE story; level is the CROSSING story, and they are separable.", AMBER)]):
        y = 1.70 + i * 1.42
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.22, fill=c, line=None)
        d.text(s, n, M, y + 0.42, 0.5, 0.35, size=20, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 11.7, 0.42, size=17, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 0.8, y + 0.40, 11.7, 0.85, size=14, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.02, W - 2 * M, 0.80, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "That separation is the engineering result: a design that moves only the production curve's SHAPE changes speed without changing level — which is what you are about to price.",
           M + 0.3, 6.16, 11.6, 0.55, size=15, bold=True, color=INK)
    d.notes(s, "Two minutes, and this is the slide that makes the derivations "
               "readable. Session 6's review said terms get introduced without "
               "being described; the same failure mode for a PICTURE is "
               "showing it and never saying how to read it.\n"
               "Item 2 is the stability argument they will reuse at 69 min on "
               "the middle crossing. Make them say it out loud now, in words, "
               "so it is cheap later.\n"
               "Item 3 is deliberately qualitative. The exact statement is the "
               "slope of (production minus removal) at the crossing, and that "
               "is derivation 2's last step. Do not pre-empt it.\n"
               "ASK before moving on: which of the three panels changed the "
               "crossing? None of them — that is the setup for the vote they "
               "just took.")

    # 6 DERIVATION 1 — the cost identity ---------------------------------------
    d.derivation(
        None, "16 – 26 min", "Built one line at a time",
        "What speed costs, exactly",
        [("Start from Tuesday's board",
          "p* = α / (γ + μ)        t½ = ln2 / (γ + μ)",
          "one denominator, two requirements — session 5's result, still on the board"),
         ("Say what the specification is",
          "hold p* fixed, and make t½ smaller",
          "this is the job. Not 'make it faster' — faster AT THE SAME LEVEL"),
         ("A tag raises the removal rate",
          "γ + μ  →  λ (γ + μ),    λ > 1",
          "Andersen's best tag gives λ = 1.75 in a host dividing every 30 min"),
         ("t½ falls by exactly that factor",
          "t½  →  t½ / λ",
          "which is what you wanted, and it is the easy half"),
         ("So α must rise to hold p* fixed",
          "α  →  λ α",
          "forced, not chosen: p* = α/(γ+μ), and the tag just moved the denominator"),
         ("Now read the cost off",
          "cost factor  =  λ  =  speed-up factor",
          "not approximately. The same λ appears in both because they share the denominator"),
         ("And it never ends",
          "λα is paid every minute, forever — α is a rate, not a stock",
          "answer C, and the factor is 1.75")],
        closing="The energy cost of speed IS the speed-up factor, exactly — as long as speed comes from the removal rate.",
        board="LEFT WING, and leave it up:   speed-up λ  ⇒  cost λ, forever   (when λ comes from γ)",
        note=("Build it with them, and resolve the 8-minute vote at step 7 "
              "rather than before.\n"
              "Step 2 is the one to labour. 'Faster' is not a specification; "
              "'faster at the same level' is. Every real brief they are handed "
              "will hold something fixed, and finding out what it is comes "
              "first.\n"
              "Step 5 is where the room should feel the trap close. They are "
              "not choosing to raise alpha — the algebra forces it.\n"
              "Step 6: the two lambdas are the same symbol because they are "
              "the same number. Point at Tuesday's Q3 on the board.\n"
              "Numbers if wanted: 23.1 protein/min becomes 40.4, and t_half "
              "30.0 becomes 17.1. Both from the figure at 50 min.\n"
              "The last clause of the closing line is doing real work. It is "
              "the escape hatch, and the next twenty minutes walk through it."))

    # 7 RHYTHM 1 --------------------------------------------------------------
    s = d.light()
    d.header(s, "26 – 32 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "Now price the other route.")
    d.text(s, "Negative autoregulation: the protein represses its own promoter. Same host, same p*, and the same speed-up, near enough. What does it cost at steady state?",
           M, 1.90, 12.5, 0.85, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "The same factor again — you cannot get speed for free."),
            ("B", "More than that, because feedback wastes repressor."),
            ("C", "Nothing extra at steady state. Same synthesis as doing nothing."),
            ("D", "Less than doing nothing — repression means less made.")]):
        y = 3.05 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=16, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=18, color=BODY)
    d.foot(s, "Before you vote, write down the one thing you would have to know about NAR to answer this at all. Then answer it.", 6.35)
    d.notes(s, "Answer C. The foot line used to hand them the clue — it does "
               "not any more, because the thing it gave away IS the item: "
               "the question is decided entirely by which of the two rates "
               "the circuit touches. Expect the room to need the full four "
               "minutes now, and expect A to be popular. NAR changes "
               "PRODUCTION, not removal.\n"
               "At steady state the synthesis rate must equal the removal "
               "rate, and the removal rate is (gamma+mu)p*. Neither factor "
               "moved. So the steady-state flux is 23.1/min whatever the "
               "feedback does — identical to doing nothing.\n"
               "A is the majority answer and it is a good instinct ('no free "
               "lunch') applied where it does not hold. Take it seriously: the "
               "lunch is not free, it is prepaid. They will see the bill at "
               "50 min.\n"
               "D is worth a sentence. Repression lowers the production "
               "CURVE, but we raised the promoter to put the crossing back at "
               "p* — so the rate AT the crossing is unchanged.\n"
               "Do not resolve fully. Derivation 2 does it.")

    # 8 DERIVATION 2 — negative autoregulation ---------------------------------
    d.derivation(
        None, "32 – 44 min", "Built one line at a time",
        "Negative autoregulation: graphically, then exactly",
        [("Write what p does to its own promoter",
          "dp/dt  =  α / (1 + p/K)  −  (γ + μ) p",
          "production now depends on p. That is the only change, and it is the whole change"),
         ("Look at the picture before the algebra",
          "production falls as p rises;  removal still a straight line",
          "middle panel of the figure at 10 minutes"),
         ("Why that is faster, in one sentence",
          "below p* the gap between the curves is LARGER than it was",
          "the net rate is the vertical distance between them, so it climbs harder"),
         ("Fix the level: put the crossing back",
          "α  =  α₀ (1 + p*/K)",
          "α/α₀ is the REPRESSION RATIO: how many-fold the promoter is held down at p*"),
         ("Pick a design point",
          "K = p*  ⇒  repression ratio 2,  α = 46.2/min",
          "a modest circuit. Rosenfeld's is far more aggressive, and it shows"),
         ("Now the steady-state cost — the vote",
          "synthesis at p*  =  (γ + μ) p*  =  α₀",
          "unchanged. The removal side never moved, so the balance never moved"),
         ("Prove it settles lower, no algebra",
          "at p = 0 both agree;  NAR slope < 0 < open-loop slope",
          "so the NAR curve is below the flat one everywhere past the origin — no quadratic needed"),
         ("Put a number on the speed",
          "repression ratio 2  ⇒  t½ = 16.8 min against 30.0",
          "1.79× against the best tag's 1.75× — the same, within measurement error"),
         ("So compare the two bills",
          "tag: 40.4/min forever.   NAR: 46.2 at first, → 23.1",
          "the tag takes out a standing charge; autoregulation buys on credit")],
        closing="Same speed-up, and NAR pays only during the transient. That is why it is the most common single-node motif in E. coli.",
        board="LEFT WING, under the first:   NAR — α raised, γ untouched  ⇒  steady-state flux unchanged",
        note=("Step 3 is the graphical heart of the session and it is the part "
              "the whole room can follow. Do it at the figure, not in "
              "symbols: the net rate is the VERTICAL GAP between the two "
              "curves. NAR starts with a bigger gap because we raised the "
              "promoter, and the gap closes faster because production is "
              "falling as removal rises.\n"
              "Step 4: the repression ratio is the design parameter. K = p* is "
              "a two-fold ratio, which is a modest circuit, and it already "
              "matches the best tag.\n"
              "STEP 6 IS THE PROOF and it is worth the time. Two functions "
              "that agree at a point, one with a smaller derivative "
              "everywhere, stay ordered. That is the whole argument and it "
              "avoids solving a quadratic. It is in the 20.405 notes if anyone "
              "wants it written out.\n"
              "Step 8: 46.2 is twice 23.1, and it is the initial rate, when p "
              "is near zero and the repressor is not yet there to repress.\n"
              "If a student says the transient cost is not zero — they are "
              "right, and that is the shaded area on the next figure. Say so."))

    # 9a ROSENFELD — the experiment -------------------------------------------
    s = d.light()
    d.header(s, "44 – 47 min", "Rosenfeld, Elowitz & Alon 2002  ·  the design")
    d.title(s, "Before the result: what did they actually build?")
    d.paper_figure(s, "rosenfeld2002_fig3", M, 1.62, 7.0, 4.0,
                   "Rosenfeld, Elowitz & Alon, J Mol Biol 2002, Fig. 3",
                   "TetR–GFP, with the feedback and with it cut")
    for i, (k, txt) in enumerate([
            ("One construct, one edge",
             "tetR fused to GFP, driven by a promoter carrying its own operator. The protein you measure is the protein doing the repressing."),
            ("The control is the same cells",
             "aTc binds TetR and stops it binding DNA. Same strain, same growth, same everything — the feedback edge is chemically cut and nothing else changes."),
            ("Read the axes out loud",
             "time in CELL CYCLES, not minutes, so dilution is normalised out; fluorescence divided by its own final value.")]):
        y = 1.52 + i * 1.50
        d.shape(s, S.ROUNDED_RECTANGLE, M + 7.4, y, 0.11, 1.30, fill=TEAL,
                line=None)
        d.text(s, k, M + 7.65, y - 0.02, 4.9, 0.42, size=14.5, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 7.65, y + 0.38, 4.9, 1.05, size=13, color=BODY)
    d.foot(s, "Ask first: what is on each axis, and what has been divided out? The normalisation is the experiment.", 6.42)
    d.notes(s, "Three minutes on the DESIGN before any interpretation. This is "
               "the habit the course is trying to build — the axes and the "
               "control first, the claim second.\n"
               "Take the axes from the room. Do not read them out yourself.\n"
               "The aTc control is the thing worth dwelling on: it is as close "
               "to one-edge-different as biology gets, and it is why this "
               "paper counts as a measurement of a design principle rather "
               "than a correlation.\n"
               "ASK: why normalise to the final value? Because otherwise a "
               "faster rise is indistinguishable from a smaller target — "
               "which is exactly the confound the derivation warned about.")

    # 9b ROSENFELD — the result ------------------------------------------------
    s = d.light()
    d.header(s, "47 – 50 min", "Rosenfeld, Elowitz & Alon 2002  ·  the result")
    d.title(s, "The same claim, measured")
    for i, (k, txt, c) in enumerate([
            ("Rise time 0.21 cell cycles against 1.0",
             "with the loop intact the protein reaches its steady level in about a fifth of a generation; with it cut, one full generation — which is exactly the dilution time our removal line predicts.", TEAL),
            ("Both curves land in the same place",
             "the maxima match. So the speed-up is not a smaller target reached sooner, and that is the only way the comparison means anything.", CYAN),
            ("Five-fold measured, 1.8-fold derived — and that is not a discrepancy",
             "our worked example uses a repression ratio of 2, a modest design. They are in the strong-autorepression limit. Same mechanism, different aggression: the repression ratio is the knob, and it is one you set when you choose the operator and the promoter strength.", AMBER)]):
        y = 1.70 + i * 1.48
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.28, fill=c, line=None)
        d.text(s, k, M + 0.45, y, 12.1, 0.44, size=17, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 0.45, y + 0.42, 12.1, 0.95, size=14, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.08, W - 2 * M, 0.80, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "A design principle being measured, not argued — and the design variable is one you can order from a catalogue. PS3 asks you how far it goes: there is a ceiling on this speed-up, and it has no parameters in it.",
           M + 0.3, 6.18, 11.6, 0.62, size=15, bold=True, color=INK)
    d.notes(s, "Three minutes. The honest caveat is item 3 and it must be "
               "said: their speed-up is about fivefold, ours is 1.8. Do not "
               "let that sit as an unexplained gap — it is the repression "
               "ratio, and naming it turns an embarrassment into a knob.\n"
               "If asked why the red curve overshoots and comes back: that is "
               "discussed in their Materials and Methods, and it is not "
               "today's business.\n"
               "Do NOT give away the ceiling. PS3 Q3 has them derive it: in "
               "the strong-repression limit the equation becomes p dp/dt = "
               "alpha_0 p* - mu p^2, so p(t) = p* sqrt(1 - exp(-2 mu t)) — "
               "which is the curve printed on this very figure — and the "
               "half-time is ln(4/3)/(2 ln2) = 0.2075 cell cycles, THEIR 0.21. "
               "The ceiling is 2 ln2/ln(4/3) = 4.82x and it contains no host, "
               "no promoter and no target level. If someone asks in the room, "
               "tell them it is on the problem set and that it is the best "
               "question on it.\n"
               "Engineering landing, and say it explicitly: the repression "
               "ratio is set by operator affinity and by where you put the "
               "operator relative to the core promoter — both of which are "
               "sequence choices they made on Tuesday.")

    # 10 RHYTHM 2 --------------------------------------------------------------
    s = d.light()
    d.header(s, "50 – 56 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "Which of these is the expensive one?")
    d.image(s, "figures/build/s07_cost_in_time.png", M + 0.55, 1.45, 10.6, 4.4)
    d.foot(s, "Same host, same final level, same speed-up for two of them. The vertical axis is what the cell pays per minute.", 6.35)
    d.notes(s, "Four minutes on paper, then vote. The question sounds trivial "
               "with the figure up, and it is not: ask them to say WHEN NAR "
               "stops being the expensive one.\n"
               "The crossing is at about 40 minutes — before that NAR spends "
               "more per minute than the tag, after that it spends less than "
               "either.\n"
               "The shaded area is the entire cost of autoregulation, and it "
               "is finite. The orange line's area grows without bound.\n"
               "The design reading, and this is the one to say out loud: if "
               "your protein is needed once, in a burst, the tag may be "
               "cheaper. If it is needed for the rest of the cell's life, NAR "
               "wins and the margin grows. Cost depends on the DURATION of the "
               "requirement, which is not in any of the equations on the "
               "board.")

    # 11 HANDOUT ---------------------------------------------------------------
    s = d.light()
    d.header(s, "56 – 65 min", "Handout  ·  items 1 and 2  ·  nine minutes")
    d.title(s, "The same two curves, four times")
    for i, (n, k, txt, c) in enumerate([
            ("1", "Fully worked — constitutive",
             "Draw both curves, find the crossing, and show it is stable by asking what happens either side of it.", TEAL),
            ("2", "The last step is yours — NAR",
             "Same axes. Raise α to put the crossing back where it was, then say which of the two curves moved and which did not.", CYAN),
            ("3", "On PS3 — positive autoregulation",
             "Cooperative, with basal. Find every crossing and classify each. Then find the cooperativity at which the middle two appear.", MUTED),
            ("4", "On PS3 · the design item",
             "You are handed a protein that must reach its level in under 15 minutes and stay there for a day. Pick a route, price it, and defend the choice.", MUTED)]):
        y = 1.85 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.9, fill=c, line=None)
        d.text(s, n, M, y + 0.26, 0.5, 0.35, size=20, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 4.6, 0.4, size=16, font=HEAD, bold=True,
               color=INK if i < 2 else MUTED)
        d.text(s, txt, M + 5.6, y + 0.02, 6.7, 0.9, size=14,
               color=BODY if i < 2 else MUTED)
    d.text(s, "Start wherever the scaffolding stops helping you. Nine minutes, and only the first two.",
           M, 6.45, W - 2 * M, 0.45, size=16, bold=True, color=INK)
    d.notes(s, "Item 1 is worked. They read it and start at item 2.\n"
               "Errors to watch for while circulating: drawing removal as a "
               "curve rather than a straight line; forgetting that raising "
               "alpha moves only the production curve; and classifying "
               "stability by which crossing is higher rather than by the sign "
               "of the gap either side.\n"
               "Item 4 is the one that matters for the project and it is on "
               "PS3 because it needs prose. The answer turns on 'stay there "
               "for a day' — duration is what decides between the two routes, "
               "and nothing in the equations says so.\n"
               "Say: 'Nine minutes. Items one and two only.'")

    # 12 THE ANSWERS -----------------------------------------------------------
    s = d.light()
    d.header(s, "65 – 69 min", "The answers  ·  items 1 and 2")
    d.title(s, "Which curve moved, and which did not")
    for i, (n, ans, prompt, c) in enumerate([
            ("1",
             "one crossing, and it is stable because the gap changes sign through it",
             "Above the crossing removal wins and p falls; below it production wins and p rises. That argument never mentions the functional form, which is why it survives into the phase plane on Tuesday.",
             TEAL),
            ("2",
             "production moved down and then up; removal never moved at all",
             "Repression lowers the production curve; raising α to restore p* lifts it again at the crossing. Removal is (γ+μ)p throughout, so the synthesis rate AT the crossing is what it always was. That is the whole cost result, read off a picture.",
             CYAN)]):
        y = 1.9 + i * 2.0
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.6, fill=c, line=None)
        d.text(s, n, M, y + 0.6, 0.5, 0.35, size=20, bold=True, color=WHITE,
               align="c")
        d.text(s, ans, M + 0.8, y, 11.7, 0.5, size=17, font=HEAD, bold=True,
               color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, M + 0.8, y + 0.58, 0.1, 0.95,
                fill=MUTED, line=None)
        d.text(s, prompt, M + 1.15, y + 0.55, 11.35, 1.0, size=14, color=BODY)
    d.text(s, "When a design changes one curve and not the other, look for what is conserved. Here it is the steady-state flux.",
           M, 6.3, W - 2 * M, 0.45, size=17, font=HEAD, bold=True, color=INK)
    d.notes(s, "Take both from the room before showing them.\n"
               "Item 1's stability argument is the one to dwell on: it is "
               "purely about the SIGN of the gap, and that is exactly how "
               "nullclines work on Tuesday. Say that out loud — it is the "
               "bridge to session 8.")

    # 13a PAR — why the curve bends -------------------------------------------
    s = d.light()
    d.header(s, "69 – 71 min", "Positive autoregulation  ·  the production curve")
    d.title(s, "Turn the feedback around and production rises with p")
    for i, (k, txt, c) in enumerate([
            ("Same loop, opposite sign",
             "the bottom row of the wiring you saw at 10 min. The product now helps RNAP instead of excluding it, so \u03b1(p) is INCREASING — and the flat line and the falling curve you have used all session are both gone.", TEAL),
            ("One binding site gives you a saturating rise",
             "\u03b1(p) = \u03b1_basal + \u03b1_max p/(K + p). \u03b1_basal is the LEAK — what the promoter makes with nothing bound, and the only reason a cell at p = 0 ever starts. A curve that rises and flattens crosses a line through the origin exactly once, however you tune it.", CYAN),
            ("Cooperativity makes it S-shaped, and that is the whole difference",
             "p^n/(K^n + p^n) — session 4's Hill function, now with p on both sides of the circuit. Flat at low p, steep in the middle, flat again at high p.", AMBER),
            ("Where n comes from, precisely",
             "n sites is the CEILING, not the value. Tuesday's \u03c9 is what makes the sites act as one: with \u03c9 = 1 the curve is barely sharper than a single site, and the effective exponent approaches n only as \u03c9 grows.", GREEN)]):
        y = 1.56 + i * 1.24
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.08, fill=c, line=None)
        d.text(s, k, M + 0.45, y, 12.1, 0.42, size=16, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 0.45, y + 0.38, 12.1, 0.86, size=13.5, color=BODY)
    d.foot(s, "Removal has not changed. It is still \u03bcp — a straight line through the origin — and it will be in every picture you draw this term.", 6.55)
    d.notes(s, "Two minutes, and it is set-up, not result. The class needs the "
               "SHAPE of alpha(p) in hand before the geometry means "
               "anything.\n"
               "Item 2 is the one they skip: a saturating rise cannot cross a "
               "line through the origin three times, because it is concave "
               "everywhere. Make them see that n = 1 is genuinely "
               "uninteresting before showing the n = 4 picture.\n"
               "Item 3 connects back to Tuesday. SAME KNOB, second use: the "
               "cooperativity they bought for a sharp input-output curve is "
               "the cooperativity that buys memory. Say it in those words.\n"
               "Draw nothing on the board yet. The next slide is the picture.")

    # 13b PAR — the third crossing ---------------------------------------------
    s = d.light()
    d.header(s, "71 – 74 min", "Positive autoregulation  ·  the third crossing")
    d.title(s, "What has to be true for the curves to cross three times")
    d.image(s, "figures/build/s07_bistable_condition.png", M + 0.15, 1.40, 8.0, 4.5)
    for i, (k, txt) in enumerate([
            ("Steeper than the line somewhere, shallower at both ends",
             "that is the entire condition, and it is geometric. No algebra required to see it."),
            ("Two stable states, one unstable between them",
             "an open circle is unstable: push p either way and it leaves. Use item 2 from 14 min — the sign of the gap on each side is the argument."),
            ("Cooperativity creates it; basal decides where the low state sits",
             "n = 1 crosses once however you tune it. With no basal expression the low state is zero, and a cell that starts there never starts at all.")]):
        y = 1.55 + i * 1.52
        d.shape(s, S.ROUNDED_RECTANGLE, M + 8.4, y, 0.11, 1.32, fill=AMBER,
                line=None)
        d.text(s, k, M + 8.65, y - 0.02, 3.9, 0.60, size=13.5, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 8.65, y + 0.56, 3.9, 0.92, size=12.5, color=BODY)
    d.foot(s, "Two genetically identical cells, same medium, can sit at different levels — and stay there.", 6.42)
    d.notes(s, "Three minutes, and the figure carries it.\n"
               "Start by ASKING what has to be true for a curve to cross a "
               "straight line three times. Wait for it. It has to be steeper "
               "than the line somewhere and shallower at both ends.\n"
               "The classification: gap positive to the left and negative to "
               "the right means stable; reverse means unstable. That is item 2 "
               "from the 14-minute slide, reused verbatim. Do NOT introduce "
               "eigenvalues — that is Tuesday.\n"
               "PS3 asks for the cooperativity at which the pair appears. Do "
               "not derive it here. If you name it, name it correctly: this is "
               "a saddle-NODE BIFURCATION, which is session 9, not Tuesday. "
               "Tuesday introduces a SADDLE, a fixed-point class in two "
               "dimensions — a different object, and students who hear the two "
               "words in the same week will weld them together unless you "
               "separate them now. Safest line: 'that event has a name, you "
               "get it in session 9.'")

    # 13c PAR — what it buys you -----------------------------------------------
    s = d.light()
    d.header(s, "74 – 77 min", "Positive autoregulation  ·  what you would use it for")
    d.title(s, "Two stable states is a design goal, not an accident")
    for i, (k, txt, c) in enumerate([
            ("You have built a memory",
             "a transient input that pushes p past the unstable point leaves the cell in the high state after the input is gone. Nothing holds it there but the loop itself.", TEAL),
            ("The knobs are ones you already have",
             "n from oligomerisation and cooperative binding (Tuesday's \u03c9); \u03b1_max from promoter strength; K from operator affinity; the basal rate from how leaky you let the promoter be.", CYAN),
            ("And the costs are real",
             "the high state pays its synthesis flux forever, the switching threshold drifts with growth rate because \u03bc is the line's slope, and noise can flip a cell that sits too near the unstable point.", AMBER)]):
        y = 1.68 + i * 1.50
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.30, fill=c, line=None)
        d.text(s, k, M + 0.45, y, 12.1, 0.44, size=17, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 0.45, y + 0.42, 12.1, 0.98, size=14, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.10, W - 2 * M, 0.78, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "Session 9 builds this deliberately out of two repressors and calls it a toggle. You are eight days from it.",
           M + 0.3, 6.24, 11.6, 0.52, size=15, bold=True, color=INK)
    d.notes(s, "Three minutes, and this is the engineering landing for the "
               "whole second half.\n"
               "Item 1: ask what happens if the input is removed. They will "
               "see it. Memory with no memory element is the surprising "
               "part.\n"
               "Item 3 is the one that keeps them honest. The line's slope IS "
               "the growth rate, so a circuit that switches reliably in rich "
               "medium may not switch in minimal — same construct, different "
               "picture. That is a real failure mode and it has bitten "
               "people.\n"
               "The forward link is real: Gardner's toggle is two of these "
               "wired to repress each other.")

    # 14 VARIANCE, AND THE LIMIT -----------------------------------------------
    s = d.dark()
    d.header(s, "77 – 81 min", "Variance  ·  and what this model cannot tell you")
    d.title(s, "NAR also narrows the spread — not from this equation")
    for i, (k, txt) in enumerate([
            ("The mechanism, which you can see",
             "a cell that drifts high represses itself harder and comes back; one that drifts low represses less. The feedback pulls both toward p*."),
            ("Positive autoregulation does the opposite",
             "a cell that drifts high makes more, and goes higher. The same feedback that stores a bit also amplifies a fluctuation."),
            ("But look at what is on the board",
             "dp/dt = α(p) − (γ+μ)p is deterministic. Two identical cells obeying it have identical trajectories. It has no variance in it at all."),
            ("It is measured, not asserted",
             "Becskei & Serrano, Nature 2000: the same gene with and without its own operator, and the autoregulated one has the narrower distribution at the same mean."),
            ("So the honest answer",
             "it holds where noise is birth-and-death of the protein itself; strong feedback with slow binding can do the opposite. This equation gives you neither. Session 12 builds the master equation.")]):
        y = 1.66 + i * 0.92
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.80, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.6, 0.40, size=14.5, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.3, y - 0.02, 7.1, 0.90, size=13.5, color=MINT)
    d.foot(s, "Knowing which question your model cannot answer is worth more than another decimal place on the ones it can.", 6.52)
    d.notes(s, "Four minutes, and do not fudge it.\n"
               "The mechanism is genuinely intuitive and they should get it "
               "from the picture: restoring force. Use the middle panel of the "
               "10-minute figure — a cell to the right of the crossing is "
               "pushed back harder under NAR than under constitutive "
               "expression, because the production curve is falling as well.\n"
               "Then the limitation, plainly. An ODE has no fluctuations. "
               "Writing down a variance from it would be hand-waving, and this "
               "course does not do that.\n"
               "Alon's summary card says 'NAR decreases variance' as a bullet. "
               "We are deriving the four bullets on that card this session — "
               "three of them today, and this one in session 12. Say that; it "
               "makes the deferral a plan rather than a gap.\n"
               "Do NOT promise a PS3 question on this. There isn't one -- "
               "the assessment sits on PS6, after they can simulate it. What "
               "you are promising here is session 12, and PS6 is where they "
               "pay for it. Saying so out loud is the whole point of the "
               "slide: the deferral is a plan with a date on it.\n"
               "IF YOU ARE RUNNING LATE: this segment is the LAST cut, not "
               "the first. It was the first until 14 September, when T17's "
               "assessment moved to PS6 -- which means nothing between today "
               "and session 12 asks them to think about variance again, and "
               "these four minutes are the only demonstration it gets. Cut "
               "13c at 74 instead; its knob list is on the ledger at 81.")

    # 15 THE DESIGN LEDGER -----------------------------------------------------
    s = d.light()
    d.header(s, "81 – 84 min", "The design ledger")
    d.title(s, "Knobs, constraints, limits")
    for i, (head, items, c) in enumerate([
            ("KNOBS — what you can change",
             ["the topology — whether the protein regulates its own promoter at all",
              "the repression ratio α/α₀ — how hard it represses itself",
              "the cooperativity n — oligomerisation, and Tuesday's ω",
              "basal expression — where the low state sits, or whether there is one"],
             TEAL),
            ("CONSTRAINTS — what you do not set",
             ["μ is the host's, not yours — the floor from session 5 has not moved",
              "a steady state is a balance, so removal always fixes the steady-state flux",
              "feedback needs a repressor and an operator: more parts, more context",
              "and the transient still has to be paid for, up front"],
             CYAN),
            ("LIMITS — where today's answer stops",
             ["the ODE has no variance in it. The spread is real and this cannot give it to you",
              "fast binding assumed throughout — same equilibrium assumption as Tuesday",
              "cost measured as synthesis rate, which is not the same as burden (session 19)",
              "\u03b3 was constant all session. Tagged protein queues for ClpXP, so \u03bb is not a dial you can turn without limit"],
             AMBER)]):
        x = M + i * 4.28
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.75, 4.05, 0.52, fill=c, line=None)
        d.text(s, head, x + 0.18, 1.87, 3.75, 0.32, size=13, bold=True,
               color=WHITE)
        for j, it in enumerate(items):
            y = 2.42 + j * 1.09
            d.shape(s, S.ROUNDED_RECTANGLE, x, y, 0.08, 0.94, fill=c,
                    line=None)
            d.text(s, it, x + 0.28, y - 0.05, 3.75, 1.02, size=16, color=BODY)
    d.foot(s, "Tuesday you asked what you could change in the lab. Today the answer includes the wiring, not just the parts.")
    d.notes(s, "The Knobs column has something new in it and it is worth "
               "naming: TOPOLOGY is a knob. Sessions 5 and 6 gave them "
               "parameters to turn; this is the first time the answer to a "
               "specification is to change the shape of the circuit rather "
               "than the value of something.\n"
               "If you are late: cut a Knob. Never cut a Limit.")

    # 16 CONSOLIDATION ---------------------------------------------------------
    s = d.dark()
    d.header(s, "84 – 87 min", "Next")
    d.title(s, "Two stable states, and nothing to compute them with")
    d.text(s, "You just met a system that sits in one of two places, and the only tool you have for it is a picture.",
           M, 2.05, 11.6, 0.85, size=20, color=WHITE, spacing=1.3)
    d.text(s, "Tuesday: the phase plane.", M, 3.05, 11.6, 0.5, size=26,
           font=HEAD, bold=True, color=CYAN)
    d.text(s, "Two proteins instead of one, nullclines instead of two curves, and a way to classify every crossing without drawing it. Then Gardner's toggle, which is this session's last figure built on purpose.",
           M, 3.70, 11.6, 0.9, size=16, color=MINT)
    d.text(s, "Before you go:  two proteins, each repressing the other. Draw that picture.",
           M, 4.62, 11.6, 0.45, size=19, font=HEAD, bold=True, color=WHITE)
    bottom = d.assignment(s, y=5.28)
    d.text(s, "PS2 is due tonight. PS3 posts today and carries five techniques.",
           M, bottom + 0.12, 11.6, 0.35, size=16, bold=True, color=SILVER)
    d.notes(s, "Last two minutes: notes closed, one sentence each on the three "
               "questions from the goals slide.\n"
               "Assign the reading OUT LOUD.\n"
               "The forward link is the honest one: they can see bistability "
               "and cannot yet compute it. That is what Tuesday is for.\n"
               "Leave the closing question up while they pack. They cannot "
               "draw it — not on one pair of axes — and finding that out for "
               "themselves is the cold open for session 8. Do not explain "
               "why; let them try.")

    return d
