"""Session 6 — Promoter occupancy from statistical thermodynamics.

Tuesday 15 September. Built to sessions/s06-promoter-occupancy/README.md,
which was settled before any of this existed and is not re-opened here.

    0–5    retrieval (2 from Thursday, 1 interleaved from session 4)
    5–8    map + goals as questions
    8–10   THE HINGE — try the session-4 method on an activator; watch it fail
    10–22  DERIVATION 1 — states, weights, p_bound, the weak-promoter limit
    22–28  rhythm 1 — do you need to know N_NS to read a fold-change?
    28–36  DERIVATION 2 — simple activation, lac + CRP2*: the parameters K_A and f
    36–42  rhythm 2 — a specification that needs s = 1.66
    42–46  lambda P_RM: cooperativity buys sharpness, not amplitude
    46–48  pause (individual, not collected)
    48–58  handout, items 1 and 2 — one derivation, twice
    58–62  the answers
    62–66  lambda O_R as a solved design problem — Ackers, Johnson & Shea 1982
    66–72  rhythm 3 — which arrows in your network diagrams are safe?
    72–76  the design ledger
    76–80  consolidation, Rosenfeld handed out, the unanswered cost question

WHAT THIS SESSION OWES PS3 AND THE MIDTERM
- T13 promoter occupancy from a partition function: derivation 1, handout 1.
- T14 activator, repressor and AND-like regulation functions: derivation 2,
  handout items 2-4. Items 3 and 4 finish on PS3.

THE NUMBERS, and where each one is READ OFF rather than recalled:
    N_NS = 5e6                      Bintu models, Fig. 1 legend
    f = 11 (lambda P_RM)            Bintu applications, Fig. 2 legend
    omega = 80 (Bintu round to 100) Koblan & Ackers 1992 Table II, 37 C
    omega = 25.2 (superseded)       Ackers 1982 Table 3, dG_12 = -1.99 kcal/mol
    K_R2/K_R1 = 25                  Bintu applications, text
    s = 0.54 one site, 0.93 helper  Bintu applications, text and Fig. 2 legend

Both sensitivities are REPRODUCED by figures/s06_promoter_occupancy.py from
regulation factors derived here rather than copied -- Bintu's Table 1 is an
image in the PDF and cannot be read as text. Two independent numbers from two
architectures agreeing to two decimal places is the check that the algebra on
these slides is the algebra in the paper.

Coverage matrix: T13, T14.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session06_PromoterOccupancy"


def build():
    d = Deck("Session 6 — Promoter occupancy", session=6)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 6", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Promoter occupancy", M, 2.72, 9.4, 1.3,
           size=40, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Where α comes from — and why one calculation does all of it",
           M, 4.15, 9.4, 0.5, size=17, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "PS2 is due Thursday. PS3 posts Thursday and carries five "
               "techniques, two of them from today.\n"
               "Bintu 2005 (models) was assigned Thursday — Figures 1 and 2. "
               "Ask who has read it before you need it at 10 min.\n"
               "Rosenfeld 2002 goes out at the end of today for Thursday.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions, notes closed")
    for i, (n, src, q, c) in enumerate([
            ("1", "From Thursday",
             "t½ = ln2/(γ + μ). Promoter strength α is nowhere in it. Say why, in one sentence.", TEAL),
            ("2", "From Thursday",
             "Andersen's strongest tag buys a factor of 1.75 in speed. What does it cost, and why is the cost exactly that factor?", TEAL),
            ("3", "From session 4",
             "A repressor binds one site. Write the fraction of time the site is occupied. You have done this; do it again from scratch.", CYAN)]):
        y = 1.9 + i * 1.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.15, fill=c, line=None)
        d.text(s, n, M, y + 0.38, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, src, M + 0.8, y, 3.0, 0.3, size=11.5, bold=True, color=c)
        d.text(s, q, M + 0.8, y + 0.3, 11.7, 0.85, size=15.5, color=BODY)
    d.text(s, "Two minutes in writing. Question 3 stays on the board — we are about to break it.",
           M, 6.45, W - 2 * M, 0.4, size=15, bold=True, color=INK)
    d.notes(s, "Q1: alpha sets the LEVEL the exponential climbs to; the rate "
               "of climb is the removal rate, and alpha is not a removal "
               "rate.\n"
               "Q2: 43% of the steady-state level, and it is the same factor "
               "because p* = alpha/(gamma+mu) and t_half = ln2/(gamma+mu) "
               "have the identical denominator. One knob, two requirements.\n"
               "Q3 is the interleaved one and it is today's hinge. Expect "
               "x/(K_d + x) from the binding equilibrium. Get it on the board "
               "and LEAVE IT THERE — the next slide asks them to do the same "
               "thing for an activator, and it is going to fail.\n"
               "Say: 'Two minutes in writing.'")

    # 3 GOALS -----------------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By the end you should be able to answer")
    for i, (n, lab) in enumerate([("4", "Modeling II"), ("5", "Expression"),
                                  ("6", "Promoters"), ("7", "Autoregulation"),
                                  ("8", "Phase plane")]):
        x, here = M + i * 2.42, n == "6"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=13.5, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "Where does a Hill function actually come from, and what is it the special case of?",
            "Your specification says the output must swing ten-fold while the input moves four-fold. Can any single promoter do that?",
            "Every network diagram you have drawn puts a + or a − on each edge. When is that label wrong?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.coming_up(s, y=6.5)
    d.notes(s, "Questions, not statements.\n"
               "The third one is the session's sting and they will not believe "
               "it until 66 minutes in. Leave it hanging.\n"
               "BUILDING TOWARD: this is the last piece of machinery Part I "
               "needs. After Thursday you have everything Gardner's toggle "
               "requires, and you read that paper on 24 September.")


    # 3b THE OBJECT ------------------------------------------------------------
    # Added 11 September. Adam's review: the session named operator, core
    # promoter, recruitment and the closed-to-open transition without ever
    # drawing one, and sessions 1-5 never draw them either -- "closed complex"
    # and "-35" appear ZERO times in decks 1 through 5. Three tutorial surfaces
    # now come before any counting. They are paid for by cutting the Ackers
    # segment and ConcepTest 3; see the module docstring.
    s = d.light()
    d.header(s, "8 – 12 min", "The object, before the model")
    d.title(s, "What a promoter actually is")
    d.image(s, "figures/build/s06_promoter_anatomy.png", M, 1.35, 12.4, 4.6)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.02, W - 2 * M, 0.86, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "You have this promoter in your hands. What can you actually change — and what would you have to DO to change each one?",
           M + 0.3, 6.14, 11.6, 0.56, size=16.5, bold=True, color=INK)
    d.notes(s, "Do not rush this — it is the first time in "
               "the course that a promoter is a piece of DNA rather than a "
               "symbol, and half the room has never seen it.\n"
               "ASK before you show the operator boxes: where would you put a "
               "site for a protein that BLOCKS transcription? Expect 'on top "
               "of the promoter', which is right and is item 1 of the "
               "handout.\n"
               "Then ask where you would put one for a protein that HELPS. "
               "Beside it, so the two can touch. That is the whole logic of "
               "the next slide and it is better if they say it.\n"
               "Promoter strength = how close the two hexamers are to "
               "consensus. Say it once; it is the Knob they will otherwise "
               "think means 'copy number'.\n"
               "Do NOT go into sigma factors. Not today.\n"
               "Take four or five answers to the closing question onto the "
               "right wing and leave them there; the "
               "ledger at 75 min is where the list comes back. What you want "
               "on the board:\n"
               "  mutate the operator sequence -> changes K. Cloning.\n"
               "  move the site, change the spacing -> changes whether the "
               "two proteins can touch at all. Cloning.\n"
               "  swap the core promoter -> changes p. Cloning.\n"
               "  mutate the protein surface -> changes omega or f. Cloning, "
               "and much harder.\n"
               "  add inducer -> changes [A] at the bench, today, reversibly.\n"
               "The split that matters and that they will not volunteer: the "
               "first four are things you BUILD ONCE and inherit; the last is "
               "the only one you turn during an experiment. Say it once here "
               "and the Knobs/Constraints distinction has already been made "
               "by the room.")

    # 3c WHERE THE POLYMERASE IS ----------------------------------------------
    s = d.light()
    d.header(s, "12 – 16 min", "Where the polymerase actually is")
    d.title(s, "Almost every polymerase in the cell is stuck to DNA")
    d.paper_figure(s, "bintu2005_models_fig1a", M, 1.40, 5.9, 2.5,
                   "Bintu et al. 2005 (models), Fig. 1a",
                   "RNAP bound all over the genome; two free")
    d.paper_figure(s, "bintu2005_models_fig1c", M + 6.4, 1.40, 6.0, 3.9,
                   "Bintu et al. 2005 (models), Fig. 1c",
                   "p_{bound} for two real promoters")
    for i, (k, txt) in enumerate([
            ("You proved this in session 2",
             "a repressor finds one site in 4.6 Mb by sticking to the backbone non-specifically and sliding. Same physics, other consequence: the DNA is a reservoir."),
            ("So N_{NS} counts places to stick",
             "about 5 × 10⁶ of them — the genome itself. It is not a parameter you set, and in twelve minutes it will cancel.")]):
        y = 4.15 + i * 1.05
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.11, 0.9, fill=TEAL, line=None)
        d.text(s, k, M + 0.3, y - 0.02, 5.6, 0.36, size=13.5, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 0.3, y + 0.33, 5.7, 0.64, size=12, color=BODY)
    d.foot(s, "And read the right-hand panel: lac sits near 10⁻³. A promoter that is occupied a thousandth of the time is what ‘weak promoter’ will mean.", 6.42)
    d.notes(s, "This slide exists so that N_NS is a fact about cells before it "
               "is a symbol in an equation.\n"
               "Start from session 2. They did the search-time estimate; they "
               "already believe proteins stick to DNA non-specifically. All "
               "that is new is the consequence for counting.\n"
               "The right panel is the one to dwell on. lacP1 is bound about "
               "three times in a thousand; T7 A1 about four times in ten. Ask "
               "which of those two is a 'weak promoter' and why it might "
               "matter — then let it go. The condition p << 1 arrives with a "
               "measurement behind it at minute 30.\n"
               "IF ASKED where 5e6 comes from: it is roughly the number of "
               "base pairs. Do not defend the second figure.")

    # 3d TWO MECHANISMS --------------------------------------------------------
    s = d.light()
    d.header(s, "16 – 20 min", "Two levers, and only two")
    d.title(s, "There are exactly two ways to change transcription")
    d.image(s, "figures/build/s06_two_mechanisms.png", M, 1.35, 12.4, 4.5)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.02, W - 2 * M, 0.82, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "Today's model charges for the first and holds the second fixed. Remember that it does — at 72 minutes it is the entry in the Limits column.",
           M + 0.3, 6.20, 11.6, 0.5, size=16, bold=True, color=INK)
    d.foot(s, "Which lever a part uses decides whether it travels. Hold that question until minute 46 — the algebra answers it.", 6.95)
    d.notes(s, "This is the slide the session rests "
               "on.\n"
               "Left: the activator touches polymerase and holds it at the "
               "promoter more of the time. Occupancy up, firing rate "
               "unchanged. That contact energy is the f you are about to "
               "derive.\n"
               "Right: polymerase is already there, sitting in the closed "
               "complex. It has to melt the DNA to start — that is the "
               "open complex — and a protein can change how often that "
               "happens without changing how often RNAP is present at all.\n"
               "ASK: which of these two would a fold-change measurement see? "
               "Both. That is the problem, and it is why the arrow on a "
               "network diagram is ambiguous.\n"
               "Say plainly that today we model ONLY the left one. The room "
               "should know it is a choice while it is being made, not be told "
               "afterwards.")

    # 4 THE HINGE -------------------------------------------------------------
    s = d.light()
    d.header(s, "20 – 22 min", "On your own  ·  ninety seconds")
    d.title(s, "Now do question 3 for an activator.")
    d.text(s, "Same method, same two minutes. A protein binds one site and transcription goes UP. Write the regulation function.",
           M, 1.85, 12.5, 0.55, size=19, font=HEAD, color=INK)
    for i, (k, txt, c) in enumerate([
            ("What the method gives you",
             "the fraction of time the site is occupied — a number between 0 and 1, of the form [A]/(K_{d} + [A]). Nothing more.",
             TEAL),
            ("What activation actually is",
             "either the bound protein RECRUITS polymerase — a protein–protein contact — or it speeds the closed-to-open transition. Two different mechanisms.",
             CYAN),
            ("So the question the method cannot answer",
             "occupied by an activator, at what RATE does the promoter fire? There is no dissociation constant for ‘makes transcription more likely’.",
             AMBER)]):
        y = 2.7 + i * 1.22
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.11, 1.02, fill=c, line=None)
        d.text(s, k, M + 0.34, y - 0.02, 5.0, 0.5, size=15, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 5.5, y - 0.02, 6.9, 1.05, size=13.5, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.15, W - 2 * M, 0.82, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "Session 4 counted molecules on a site. Today we count STATES of the promoter, and give each one a weight and a firing rate.",
           M + 0.3, 6.33, 11.6, 0.5, size=16.5, bold=True, color=INK)
    d.notes(s, "Let them try it, then take the failure from the room rather "
               "than announcing it.\n"
               "Be precise about what fails, because a sharp student will say "
               "'just multiply the occupancy by a bigger rate constant' — and "
               "that is RIGHT, and it is exactly the move we are about to "
               "formalise. The honest statement is not that session 4's method "
               "is wrong; it is that it cannot TELL you that rate, cannot say "
               "how two sites combine, and cannot say why the answer does not "
               "depend on the size of the genome. Assuming a productive bound "
               "state is not deriving one.\n"
               "Leave question 3 on the board. Derivation 2 reproduces it as a "
               "special case at 36 min, and that is the payoff.")

    # 5 DERIVATION 1 — the machinery -------------------------------------------
    # Expanded 12 September. Adam: the class will not get this off one line per
    # move. The old step 4 did the multinomial, the P << N_NS limit and the
    # definition of p at once, which is where a biologist loses the thread and
    # a physicist stops watching. Eight steps now, and the two that matter --
    # counting the arrangements, and what survives the division -- each get
    # their own surface.
    d.derivation(
        None, "22 – 34 min", "Built one line at a time",
        "Count the states. Weight them. Divide by the sum.",
        [("Ask where the polymerase actually is",
          "P molecules,  N_{NS} = 5 × 10⁶ non-specific sites,  one promoter",
          "the genome is the reservoir — you saw the picture at 12 minutes"),
         ("Count the ways to put P of them on N_{NS} sites",
          "W(P)  =  N_{NS}! / [ P! (N_{NS} − P)! ]   ≈   N_{NS}^{P} / P!",
          "balls in boxes. N_{NS} is five million and P a few thousand, so the falling factorial is just N_{NS}^{P}"),
         ("State 1 — promoter empty, all P stuck non-specifically",
          "Z_{1}  =  (N_{NS}^{P} / P!) · e^{−P ε_NS / k_BT}",
          "every one of those arrangements has the same energy, so they share one Boltzmann factor"),
         ("State 2 — one polymerase on the promoter, P−1 elsewhere",
          "Z_{2}  =  (N_{NS}^{P−1} / (P−1)!) · e^{−(P−1) ε_NS / k_BT} · e^{−ε_P / k_BT}",
          "one fewer molecule in the reservoir, and one sitting on the site we care about"),
         ("Divide. Watch what fails to survive",
          "Z_{2} / Z_{1}  =  (P / N_{NS}) · e^{−(ε_P − ε_NS) / k_BT}   ≡   p",
          "P!/(P−1)! = P, one factor of N_{NS} is left over, and only the energy DIFFERENCE survives"),
         ("So the promoter is occupied some fraction of the time",
          "p_{bound}  =  Z_{2} / (Z_{1} + Z_{2})  =  p / (1 + p)",
          "two states, so the sum has two terms. That is the whole of the statistical mechanics"),
         ("A regulator does not change the method. It changes the list",
          "p_{bound}  =  p F_{reg} / (1 + p F_{reg})",
          "every promoter in this course is this equation. Only F_{reg} changes"),
         ("And take the weak-promoter limit: p << 1",
          "fold-change  =  p_{bound}(A) / p_{bound}(0)  =  F_{reg}",
          "p cancels — and with it N_{NS}, the polymerase count, and both energies")],
        closing="fold-change = F_{reg}. Everything you cannot measure has cancelled — which is why a part is characterised in fold-change and not in molecules.",
        board="LEFT WING, and leave it up all period:   p_{bound} = p F_{reg}/(1 + p F_{reg})   and   fold-change = F_{reg}  (weak promoter)",
        note=("Build it with them. Ask for the state list before you write "
              "it.\n"
              "Step 2 is where a biologist will stall, so do the count out "
              "loud: how many ways to put 3 balls in 5 boxes, then generalise. "
              "The approximation is worth ten seconds — N_NS is 5e6 and P is a "
              "few thousand, so (N_NS − P) is still 5e6.\n"
              "Step 3: say why all those arrangements share one Boltzmann "
              "factor. They are the same energy. That is the only reason the "
              "count and the weight separate.\n"
              "STEP 5 IS THE ONE. Do the division on the board beside the "
              "slide if you have to. Three things happen: the factorials leave "
              "a single P, the powers of N_NS leave a single N_NS "
              "downstairs, and the absolute energies cancel to a difference. "
              "That last one is why nobody ever has to measure an absolute "
              "binding energy.\n"
              "Ask after step 6: what have we NOT needed to know? The number "
              "of polymerases, the size of the genome, and every energy in the "
              "problem. Three things, and none of them measurable.\n"
              "LEDGER, left wing: p_bound = pF/(1+pF), fold-change = F_reg."))

    # 6 RHYTHM 1 --------------------------------------------------------------
    s = d.light()
    d.header(s, "34 – 38 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "Your collaborator wants the genome size.")
    d.text(s, "She says your fold-change measurement cannot be interpreted without knowing N_{NS} and the RNAP copy number. Work it before you vote.",
           M, 1.95, 12.5, 0.55, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "She is right — both appear in p, and p is in the model."),
            ("B", "She is wrong — they cancel in the ratio, always."),
            ("C", "She is wrong for a weak promoter, right for a strong one."),
            ("D", "She is right, but only the ratio P/N_{NS} matters.")]):
        y = 2.85 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "Three minutes on paper. Eyes down to vote, argue with your neighbour, vote again.", 6.3)
    d.notes(s, "Answer C, and B is the trap — it is the right instinct with "
               "the condition filed off.\n"
               "Work it: p_bound = pF/(1+pF). The ratio to the unregulated "
               "case is F(1+p)/(1+pF). For p << 1 that is F and everything "
               "cancels. For p of order 1 or larger it is not, and the "
               "measured fold-change depends on how strong the promoter "
               "already was.\n"
               "The same regulatory architecture on a strong promoter reports "
               "a SMALLER fold-change. That is a property of the assay, not of "
               "the regulation.\n"
               "A is wrong but honest. D is true and irrelevant — the ratio is "
               "what p contains, and it still cancels.\n"
               "THE ENGINEERING POINT, and do not leave it out: p is the core "
               "promoter. It cancelled. So the fold-change of a regulatory "
               "part is the SAME whichever weak promoter you bolt it onto — "
               "characterise it once, reuse it anywhere. That is why parts "
               "registries quote fold-change, and it is the first orthogonality "
               "result in this course.\n"
               "And C is the failure condition for exactly that reuse. On a "
               "strong promoter the two knobs stop being independent and your "
               "characterisation stops transferring. Modularity is not a "
               "property of the part; it is a property of the regime.\n"
               "Record the distribution. Say out loud: every limit in this "
               "course is a condition you have to know you are standing in.")


    # 6b RHYTHM 1 — resolve. Added 11 September: this vote had no resolution
    # surface, so the composability result it contains reached the room only if
    # the instructor happened to say it. It is the session's first engineering
    # payoff and it was living in a speaker note.
    s = d.dark()
    d.header(s, "38 – 40 min", "Vote  ·  argue  ·  vote again")
    d.title(s, "C — and you just proved parts are reusable.")
    for i, (k, txt) in enumerate([
            ("The algebra, in one line",
             "p_{bound}(A)/p_{bound}(0) = [pF/(1+pF)] · [(1+p)/p] = F_{reg}(1+p)/(1+pF_{reg}). For p << 1 that is F_{reg}."),
            ("p is the core promoter",
             "and it cancelled. So the same regulatory part, bolted onto any WEAK promoter, gives the same fold-change. Characterise it once, reuse it anywhere."),
            ("Which is why datasheets quote fold-change",
             "not molecules. The number transfers between hosts and constructs; an absolute occupancy does not."),
            ("And C is that reuse breaking",
             "on a strong promoter the two knobs stop being independent and your characterisation stops transferring. Modularity is a property of the REGIME, not of the part.")]):
        y = 1.85 + i * 1.12
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.94, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.6, 0.45, size=14, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.3, y - 0.02, 7.1, 0.95, size=13, color=MINT)
    d.foot(s, "Session 17 calls this composability and spends a whole period on when it fails. You have just derived the condition.", 6.4)
    d.notes(s, "B is the majority answer and it is right about the cancelling "
               "and wrong about the condition.\n"
               "Do not rush the third box. Every part registry in synthetic "
               "biology quotes fold-change, and most students have never asked "
               "why. It is because that is the number that survives being "
               "moved.\n"
               "The fourth box is the one that will matter to them in the "
               "project: a characterisation taken on a weak promoter does not "
               "transfer to a strong one, and nothing about the part changed.")

    # 7 DERIVATION 2 — simple activation --------------------------------------
    d.derivation(
        None, "40 – 49 min", "Built one line at a time",
        "Simple activation: lac and CRP, with measured parameters",
        [("Write the state list for one activator site plus the promoter",
          "empty · A bound · RNAP bound · both bound",
          "four states, and choosing them is the modelling decision"),
         ("Weight them the same way you just did",
          "1  ·  a  ·  p  ·  a p f,      a = [A]/K_{A},   f = e^{−ε_ap/k_BT}",
          "a and p are each a concentration over a reference — exactly the p you built"),
         ("Charge f only where the two proteins are actually touching",
          "ε_ap < 0 means they like being adjacent, so f > 1",
          "this is the recruitment lever from minute 16, and it is the only new object today"),
         ("Only the states with RNAP on the promoter transcribe",
          "p_{bound}  ∝  (p + a p f) / (1 + a + p + a p f)",
          "the activator-bound one fires f times as often, so it is counted f times"),
         ("Weak promoter again: drop p and apf from the denominator",
          "p_{bound}  ≈  p (1 + a f) / (1 + a)",
          "p is small, so any term carrying it is small next to 1 and a"),
         ("Divide by the promoter with no activator, a = 0",
          "F_{reg}  =  (1 + f a) / (1 + a)",
          "two parameters. Not four, not six — and both of them are visible"),
         ("Read them off a log–log plot instead of measuring energies",
          "plateau = f      midpoint = K_{A}      s = (√f − 1)/(√f + 1)",
          "dF/da = (f−1)/(1+a)², so s = a(f−1)/[(1+a)² F], and at a = 1/√f that collapses")],
        closing="F_{reg} = (1 + fa)/(1 + a). Set f = 0 and the repressor from session 4 falls out — same equation, one state deleted.",
        board="LEFT WING, under the first two:   F_{reg} = (1 + fa)/(1 + a),   a = [A]/K_{A}",
        note=("Slow down on step 3. f is a protein-protein interaction energy, "
              "which means it is a surface, which means it is engineerable. It "
              "is the left-hand panel of the minute-16 figure with a number on "
              "it.\n"
              "Step 5 is the same move as step 8 of the last run. Say so — "
              "they have done this once already and it should feel cheap the "
              "second time.\n"
              "STEP 7 IS THE OTHER HARD ONE. The aside carries the "
              "differentiation; do it on the board if the room wants it. What "
              "matters is where the midpoint is: in a log-log plot the middle "
              "is F = sqrt(f), not F = f/2, and that is a = 1/sqrt(f). Put "
              "f = 11 in and you get 0.54, which is the number printed in "
              "Bintu's Figure 2 legend.\n"
              "The ceiling is the design consequence: s < 1 for every finite "
              "f. One site cannot be made sharp. That is the next vote.\n"
              "The closing line is the hinge closing. Point at question 3, "
              "still on the board: set f = 0 and you get session 4's answer "
              "back. The old method was the special case."))

    # 8 RHYTHM 2 --------------------------------------------------------------
    s = d.light()
    d.header(s, "49 – 55 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "Ten-fold out, four-fold in.")
    d.text(s, "The specification: output rises ten-fold while the input rises only four-fold. Your activator has f = 11 at one site. Work out the slope you need.",
           M, 1.95, 12.5, 0.55, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "Use a stronger core promoter — more output per bound RNAP."),
            ("B", "Improve the activator–RNAP contact: raise f at the one site."),
            ("C", "Add a second, tighter operator for the same protein, with cooperativity."),
            ("D", "No promoter built from these parts reaches it.")]):
        y = 2.85 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "You need one number before you can answer: the log–log slope the specification is asking for. Three minutes.", 6.3)
    d.notes(s, "The slope required is log10/log4 = 1.66.\n"
               "A does nothing: the core promoter is in p, and p cancelled.\n"
               "B cannot work. s = (sqrt(f)-1)/(sqrt(f)+1) is below 1 for "
               "every finite f, so no contact energy gets a single site past "
               "1, let alone 1.66.\n"
               "C is the right DIRECTION — two sites with cooperativity can in "
               "principle approach s = 2 — and it is still not enough here. "
               "With f = 11 and lambda's own omega = 100 the best this "
               "architecture reaches is 0.98, and lambda O_R itself sits at "
               "0.93. Getting to 1.66 needs f in the hundreds AND a large "
               "omega.\n"
               "So the answer is D, and C is the answer most rooms give. Do "
               "not treat C as wrong: it is the correct architecture and an "
               "insufficient one, which is a different and more useful lesson "
               "than a wrong answer.\n"
               "This is session 5's move again — four minutes of arithmetic "
               "kills a specification before anyone clones anything.\n"
               "Take the vote first. The next slide has the real numbers.")

    # 9 LAMBDA P_RM -----------------------------------------------------------
    s = d.light()
    d.header(s, "55 – 59 min", "λ P_{RM}  ·  Bintu applications, Fig. 2")
    d.title(s, "Cooperativity buys sharpness, not amplitude.")
    d.image(s, "figures/build/s06_cooperativity.png", M + 0.05, 1.48, 7.05, 4.05)
    d.paper_figure(s, "bintu2005_app_fig2", 8.6, 1.45, 3.45, 2.5,
                   "Bintu et al., Curr Opin Genet Dev 2005, Fig. 2",
                   "λ P_{RM} — the same result, their axes")
    for i, (k, txt) in enumerate([
            ("cI₂ at O_{R}2 activates",
             "that is the site with the contact. Its enhancement factor is f ≈ 11."),
            ("cI₂ at O_{R}1 only helps",
             "it does not touch polymerase. It recruits the OTHER dimer, through ω."),
            ("So full activation is unchanged",
             "both curves saturate at f. The helper cannot raise the ceiling because it is not what fires the promoter.")]):
        y = 4.15 + i * 0.80
        d.shape(s, S.ROUNDED_RECTANGLE, 7.95, y, 0.11, 0.66, fill=TEAL,
                line=None)
        d.text(s, k, 8.20, y - 0.02, 4.4, 0.35, size=13.5, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, 8.20, y + 0.30, 4.4, 0.48, size=12, color=BODY)
    d.foot(s, "s = 0.54 with O_{R}1 deleted, 0.93 with it. Same plateau, nearly double the slope — and 0.93 is still under the 1.66 you were asked for.", 6.42)
    d.notes(s, "Resolve the vote here, with their own numbers on the screen.\n"
               "The two curves have the SAME plateau. Make them look at it "
               "before you say it.\n"
               "Where the numbers come from, and say this: f = 11 and omega = "
               "100 are in the legend of Bintu's Figure 2, from in vitro "
               "studies. Our left-hand curve is not traced from theirs — it is "
               "computed from the regulation factor we derived at 28 minutes, "
               "and it returns their 0.54 and their 0.93. That agreement is "
               "the reason to trust the algebra you just watched.\n"
               "The dashed curve uses omega = 25, from Ackers' 1982 table, "
               "and it is SUPERSEDED. Koblan & Ackers 1992 remeasured it at "
               "the same temperature with a better method: dG_12 = -2.7 +/- "
               "0.3, so omega = 80 with a range of 49 to 130. Bintu's 100 sits "
               "inside that; the 1982 value does not. One lab revising its own "
               "number.\n"
               "Mention it even if nobody asks. The answer sheet pushes each "
               "temperature's measured pair through the expression they just "
               "derived and finds s barely moves — 0.92, 0.93, 0.91, 0.86, "
               "0.76 from 37 C down to 5 C — while both inputs swing by a "
               "factor of four. The design is robust to exactly the parameters "
               "that are worst known, and you can only find that out by "
               "pushing them through a model you built.\n"
               "Ask: you have two requirements now, amplitude and sharpness. "
               "Do they share a knob? No. Hold that until the ledger.")

    # 10 PAUSE ----------------------------------------------------------------
    s = d.dark()
    d.header(s, "59 – 61 min", "Two minutes  ·  your own notes")
    d.title(s, "Two minutes. Fix your own notes.")
    d.text(s, "Find the one line in the last forty minutes you could not reconstruct on your own and write it out properly.",
           M, 2.2, 11.9, 0.9, size=20, color=WHITE, spacing=1.3)
    d.text(s, "Then: handouts.", M, 3.9, 11.9, 0.5, size=22, font=HEAD,
           bold=True, color=CYAN)
    d.foot(s, "If nothing comes to mind: write the state list for a promoter with TWO repressor sites that cannot both be occupied at once.", 6.3)
    d.notes(s, "Say nothing for the full two minutes. Stand at the back.\n"
               "Nothing is collected.\n"
               "The foot line is the mutually-exclusive-states case and it is "
               "handout item 1's structure. Answer: three states, not four — "
               "the doubly-bound one is simply absent from the sum, which is "
               "the whole trick.\n"
               "Hand the paper out during the second minute.")

    # 11 HANDOUT --------------------------------------------------------------
    s = d.light()
    d.header(s, "61 – 70 min", "Handout  ·  items 1 and 2  ·  nine minutes")
    d.title(s, "The same calculation, four times, with less of my working each time")
    for i, (n, k, txt, c) in enumerate([
            ("1", "Fully worked — simple repression",
             "lacUV5 truncated to one operator, LacI₄ at O_{m}. Every step labelled. Read it; do not copy it.", TEAL),
            ("2", "The last step is yours — λ P_{RM}",
             "cI₂ at O_{R}2 and O_{R}1, with ω. Four states, then the sum. Check that ω → 1 gives you two independent sites.", CYAN),
            ("3", "On PS3 — two different proteins",
             "melAB: MelR₂* activates at O2, CRP₂* helps at O1 and does not itself activate. Whose f appears in the answer?", MUTED),
            ("4", "On PS3 · the design item",
             "Build a promoter whose fold-change is AND-like. Give the truth table, and say which knob you turned to get it.", MUTED)]):
        y = 1.85 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.9, fill=c, line=None)
        d.text(s, n, M, y + 0.26, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 4.6, 0.4, size=14.5, font=HEAD, bold=True,
               color=INK if i < 2 else MUTED)
        d.text(s, txt, M + 5.6, y + 0.02, 6.7, 0.9, size=13,
               color=BODY if i < 2 else MUTED)
    d.text(s, "Start wherever the scaffolding stops helping you. Ten minutes, and only the first two.",
           M, 6.45, W - 2 * M, 0.45, size=15, bold=True, color=INK)
    d.notes(s, "Item 1 is worked. They read it and start at item 2 if the "
               "first is obvious. Do not announce who should start where.\n"
               "Errors to watch for while circulating: (a) forgetting the "
               "empty state in the denominator, which is the single most "
               "common one; (b) including a state the architecture forbids — "
               "in item 1 LacI and RNAP cannot both be bound; (c) putting f on "
               "the helper in item 2.\n"
               "Item 2's real question is whether omega multiplies a state or "
               "a site. It multiplies the STATE in which both are bound, and "
               "nothing else.\n"
               "Say: 'Ten minutes. Items one and two only.'")

    # 12 THE ANSWERS ----------------------------------------------------------
    s = d.light()
    d.header(s, "70 – 74 min", "The answers  ·  items 1 and 2")
    d.title(s, "The denominator is the whole answer.")
    for i, (n, ans, prompt, c) in enumerate([
            ("1",
             "three states, not four:  F_{reg} = 1/(1 + [R]/K_{m})",
             "LacI on O_{m} and RNAP on the promoter overlap, so the doubly-occupied state does not exist and is simply absent from the sum. Repression has no f in it — there is no contact to charge for. This is session 4's answer, reached by counting instead of by cancelling [P].",
             TEAL),
            ("2",
             "four states:  F_{reg} = (1 + fa + h + fωah)/(1 + a + h + ωah)",
             "ω multiplies only the state with both dimers bound. Set ω = 1 and the sites are independent; set h = 0 and you are back to one site and s = 0.54. Every architecture in this course is this expression with states added or deleted.",
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
    d.text(s, "Two checks that catch nearly everything: is the empty state in the denominator, and does every state you wrote physically exist?",
           M, 6.3, W - 2 * M, 0.45, size=16, font=HEAD, bold=True, color=INK)
    d.notes(s, "Take both from the room before showing them.\n"
               "Item 1 closes the hinge for the second time: the session-4 "
               "result, derived by counting. Say so.\n"
               "The two checks at the bottom are the transferable habit and "
               "they are what the midterm will reward.")

    # 13 LAMBDA O_R — restored 12 September ------------------------------------
    # Cut on the 11th to pay for the biology block, restored on Adam's call:
    # sessions have been running 5-12 minutes short, and this is the session's
    # only worked engineering case study. Badges now sum to 84 against an
    # 80-minute room, which is inside the OBSERVED slack but not inside the
    # planned budget -- so this segment is marked first-to-cut in the board
    # notes, and it is placed where dropping it costs nothing downstream.
    #
    # ConcepTest 3 (Gedeon) stays cut. It is a Limits entry with the paper
    # cited, and the two-levers slide at 16 min now teaches the mechanism it
    # rested on.
    s = d.light()
    d.header(s, "74 – 78 min", "Ackers, Johnson & Shea 1982")
    d.title(s, "One operator, two promoters, opposite requirements")
    d.paper_figure(s, "ackers1982_fig2", M, 1.45, 6.1, 4.3,
                   "Ackers, Johnson & Shea, PNAS 79:1129 (1982), Fig. 2",
                   "predicted repression at P_{R} and P_{RM}")
    for i, (k, txt) in enumerate([
            ("The specification",
             "at ONE repressor concentration: turn P_{R} nearly all the way off, and keep P_{RM} active. Two outputs, opposite requirements, one input, one operator region."),
            ("The knobs they had",
             "three site affinities and two cooperativities. Nothing else — and every one of them is on your board from minute 12."),
            ("The parameters are measured, not fitted to the answer",
             "ΔG₁ = −11.69, ΔG₂ = −10.10, ΔG₃ = −10.09, ΔG₁₂ = −1.99 kcal/mol. DNase protection, 37 °C, 0.2 M KCl. Then the model predicts both curves with no further adjustment."),
            ("Which is the job you will be given",
             "a specification with more outputs than inputs, and a parts list. Evolution solved this one; Gardner solves it deliberately in session 9.")]):
        y = 1.55 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M + 6.5, y, 0.11, 0.98, fill=TEAL,
                line=None)
        d.text(s, k, M + 6.75, y - 0.02, 5.8, 0.4, size=14, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 6.75, y + 0.34, 5.8, 0.78, size=12.5, color=BODY)
    d.foot(s, "An engineering document written eighteen years before anyone could build one. Read its Table 3 as a parts list with measured values.", 6.42)
    d.notes(s, "Teach the shape of the achievement, not the phage "
               "biology.\n"
               "Say the arithmetic out loud once: omega = exp(1.99/RT) at 37 C "
               "is 25. A measured free energy in a 1982 table is the "
               "cooperativity parameter from your own derivation.\n"
               "The second box is the one that ties the session together — "
               "point at the right wing. Their list of what you can change in "
               "the lab IS the list Ackers had.\n"
               "IF ASKED about the two values of omega: Koblan & Ackers 1992 "
               "revised this to -2.7, the same lab with a better method. The "
               "answer sheet works it through.\n"
               "IF YOU ARE LATE, THIS IS THE SEGMENT TO DROP. Put up Table 3, "
               "say that these five measured numbers are the switch, and go "
               "straight to the ledger.")

    # 16 THE DESIGN LEDGER ----------------------------------------------------
    s = d.light()
    d.header(s, "78 – 81 min", "The design ledger")
    d.title(s, "Knobs, constraints, limits")
    for i, (head, items, c) in enumerate([
            ("KNOBS — what a sequence change can move",
             ["operator affinity K — it is a binding site, so it is a sequence",
              "number and spacing of sites — add a helper operator",
              "the interaction energy ω — protein surfaces and linkers. Ackers measured λ's at −1.99 kcal/mol in 1982, and that one number holds lysogeny stable",
              "the enhancement factor f — which mechanism you recruit through"],
             TEAL),
            ("CONSTRAINTS — what you do not set",
             ["N_{NS} is the genome. That is WHY fold-change, not occupancy, is the observable",
              "RNAP is a shared pool, set by growth rate and every other promoter",
              "k_{B}T is not adjustable — which is why 2–3 k_{B}T is a large effect and 0.1 is nothing",
              "and synthesis flux is a currency you have not been charged for yet"],
             CYAN),
            ("LIMITS — where today's answer stops being true",
             ["the weak-promoter limit: strong promoters break fold-change = F_{reg}",
              "equilibrium: binding must settle fast against transcription. Fine in bacteria, shakier in eukaryotes",
              "the monotone arrow. Restore the second lever — each state has its own firing rate — and an activator can repress (Gedeon 2008). Every + and − you have drawn is the one-lever special case"],
             AMBER)]):
        x = M + i * 4.28
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.75, 4.05, 0.52, fill=c, line=None)
        d.text(s, head, x + 0.18, 1.87, 3.75, 0.32, size=12.5, bold=True,
               color=WHITE)
        for j, it in enumerate(items):
            y = 2.48 + j * 1.02
            d.shape(s, S.ROUNDED_RECTANGLE, x, y, 0.08, 0.86, fill=c,
                    line=None)
            d.text(s, it, x + 0.28, y - 0.04, 3.75, 0.95, size=12, color=BODY)
    d.foot(s, "Check this against the list on the right wing — the one you made at minute 12, before any of the mathematics.", 6.35)
    d.notes(s, "Read the comparison box out loud. It is the strongest single "
               "thing in the session and it only exists because Thursday came "
               "first.\n"
               "The Limits column is the one not to skip. If you are late, cut "
               "a Knob, never a Limit.\n"
               "The last Constraint is deliberately unpaid. It is the "
               "forward link, and the next slide asks for it.")


    # 16b THE COMPARISON — the session's actual argument, on its own surface
    s = d.dark()
    d.header(s, "81 – 83 min", "Two sessions, side by side")
    d.title(s, "Do your requirements share a knob?")
    for i, (when, eqn, verdict, c) in enumerate([
            ("THURSDAY", "p* = α/(γ+μ)      t½ = ln2/(γ+μ)",
             "One knob, two requirements. Speed costs level, one for one, and no tag escapes it.", MINT),
            ("TODAY", "ceiling = f      slope set by ω",
             "Two knobs, two requirements. Sharpness and amplitude move independently.", CYAN)]):
        y = 2.05 + i * 1.55
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.3, fill=c, line=None)
        d.text(s, when, M + 0.4, y, 2.2, 0.4, size=15, font=HEAD, bold=True,
               color=c)
        d.text(s, eqn, M + 2.8, y - 0.02, 9.5, 0.45, size=19, font=TEXT,
               bold=True, color=WHITE)
        d.text(s, verdict, M + 2.8, y + 0.52, 9.5, 0.75, size=14, color=MINT)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.25, W - 2 * M, 0.95, fill=None,
            line=CYAN, lw=2)
    d.text(s, "Which case you are in is a property of the mechanism, not of how hard you push. Finding out is the first thing a designer does.",
           M + 0.3, 5.48, 11.6, 0.6, size=17, bold=True, color=WHITE)
    d.notes(s, "This is the strongest thing in the session and it only exists "
               "because Thursday came first. Say it slowly.\n"
               "The two equations are on the left wing. Point at them.\n"
               "It is also the argument for deriving rather than quoting: you "
               "cannot tell which case you are in from a Hill function "
               "somebody handed you. You can tell immediately from the state "
               "list, because sharing a knob means sharing a denominator.")

    # 17 CONSOLIDATION --------------------------------------------------------
    s = d.dark()
    d.header(s, "83 – 87 min", "Next")
    d.title(s, "One question, and I am not answering it today.")
    d.text(s, "Two cells. One expresses a protein with a degradation tag, one without, and both hold the same steady level.",
           M, 2.05, 11.6, 0.85, size=20, color=WHITE, spacing=1.3)
    d.text(s, "Which cell is spending more?", M, 3.1, 11.6, 0.5, size=26,
           font=HEAD, bold=True, color=CYAN)
    d.text(s, "Fifteen seconds. Do not write anything down. Thursday opens on it, and the answer is why the most common single-gene circuit in E. coli looks the way it does.",
           M, 3.75, 11.6, 0.75, size=15, color=MINT)
    bottom = d.assignment(s, y=4.7)
    d.text(s, "PS2 is due Thursday. PS3 posts Thursday and carries today's two techniques.",
           M, bottom + 0.12, 11.6, 0.35, size=15, bold=True, color=SILVER)
    d.notes(s, "No arithmetic, and no resolution.\n"
               "Most of the room will say 'the same' — the levels are equal, "
               "so what is there to spend? It is wrong and they cannot yet see "
               "why, which is the same deliberate non-resolution as session "
               "5's ConcepTest 1.\n"
               "It also does real work today: the Constraints column says RNAP "
               "is a shared pool, and this calculation treated that pool as "
               "infinite. This question is the first crack in it, and session "
               "19 is where it becomes the whole subject.\n"
               "Assign the reading OUT LOUD: Rosenfeld et al. 2002, in Files > "
               "readings on bCourses. It is four pages and they should read "
               "all of it.\n"
               "Do not answer the question.")

    return d
