"""Session 9 — Bistability and the toggle switch.

The exemplar deck. Structure follows docs/lecture-design.md, with one
deliberate departure argued there: the generation phase is **analysis of a real
working artifact**, not invention from nothing. Students get the Gardner paper
and its construct, argue about why it works, and only then meet the model.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session09_Bistability"


def build():
    d = Deck("Session 9 — Bistability and the toggle switch", session=9)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 9", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Bistability and the toggle switch", M, 2.72, 9.0, 1.3,
           size=42, font=HEAD, bold=True, color=WHITE)
    d.text(s, "One paper, one construct, and everything it demands of you",
           M, 4.15, 9.0, 0.5, size=18, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Project description is due today — say so now, not at the end.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions before we start")
    for i, (src, q, c) in enumerate([
            ("From Tuesday", "A nullcline is the set of points where ______ .", TEAL),
            ("From Tuesday", "How do you tell a stable fixed point from an unstable one?", TEAL),
            ("From session 4", "When does the quasi-steady-state approximation fail?", CYAN)]):
        y = 2.15 + i * 1.25
        d.shape(s, S.OVAL, M, y, 0.42, 0.42, fill=c, line=None)
        d.text(s, str(i + 1), M, y + 0.08, 0.42, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, src.upper(), M + 0.75, y - 0.02, 3, 0.28, size=9.5,
               bold=True, color=MUTED)
        d.text(s, q, M + 0.75, y + 0.26, W - 2 * M - 0.75, 0.6, size=17, color=BODY)
    d.foot(s, "Question 3 is deliberately from three sessions back. The spacing is the point.")
    d.notes(s, "Elaborative, not factual. Collect answers; do not lecture them.")

    # 3 MAP + GOALS -----------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By 9:30 you should be able to answer")
    for i, (n, lab) in enumerate([("3", "Modeling"), ("8", "Phase plane"),
                                  ("9", "Bistability"), ("10", "Feedforward"),
                                  ("11", "Oscillation")]):
        x, here = M + i * 2.42, n == "9"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=12, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "Why does mutual repression need cooperativity to hold two states?",
            "Of the parameters that set bistability, which can you actually change in a lab — and which are you stuck with?",
            "The toggle works. Why does it fail after 40 hours?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "Goals as questions they cannot yet answer, not as statements.")

    # 4 WHY MEMORY ------------------------------------------------------------
    s = d.light()
    d.header(s, "8 – 12 min", "The problem")
    d.title(s, "Every circuit so far forgets")
    for i, (kind, eq, txt, hl) in enumerate([
            ("COMBINATIONAL", "output = f(input)",
             "Remove the inducer and the output returns to where it started. Everything through session 8 behaves this way.", False),
            ("SEQUENTIAL", "output = f(input, state)",
             "Remove the inducer and the output stays. The circuit has to hold something after the signal is gone.", True)]):
        x = M + i * 6.2
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.0, 5.7, 2.0,
                fill=WASH if hl else CARD, line=TEAL if hl else RULE, lw=2 if hl else 1)
        d.text(s, kind, x + 0.3, 2.2, 5, 0.28, size=10, bold=True,
               color=TEAL if hl else MUTED)
        d.text(s, eq, x + 0.3, 2.52, 5.1, 0.45, size=22, font=HEAD, bold=True, color=INK)
        d.text(s, txt, x + 0.3, 3.05, 5.1, 0.85, size=14, color=BODY)
    d.text(s, "Nature solved this first: the λ phage lysis–lysogeny decision is a bistable switch that holds for generations.",
           M, 4.45, W - 2 * M, 0.5, size=16, color=INK)
    d.text(s, "The question in 1999 was whether you could build one on purpose, from parts, in a cell that had never had one.",
           M, 5.0, W - 2 * M, 0.5, size=16, bold=True, color=INK)
    d.notes(s, "Ptashne's lambda switch is worth 60 seconds — it establishes the phenomenon is real before we ask whether it is engineerable.")

    # 5 THE PAPER + CONSTRUCT -------------------------------------------------
    s = d.light()
    d.header(s, "12 – 16 min", "The artifact")
    d.title(s, "Gardner, Cantor & Collins, Nature 2000")
    d.text(s, "“Construction of a genetic toggle switch in Escherichia coli”",
           M, 1.9, 6.6, 0.4, size=17, font=HEAD, italic=True, color=TEAL)
    for i, (k, v) in enumerate([
            ("Two plasmids", "pTAK — lacI ⇄ cI857\npIKE — lacI ⇄ tetR"),
            ("Mutual repression", "Each repressor's promoter is repressed by the other. Nothing else."),
            ("Two inducers", "IPTG relieves LacI. Heat (42 °C) inactivates cI857; aTc relieves TetR."),
            ("One reporter", "GFPmut3 — the state is visible.")]):
        y = 2.45 + i * 0.92
        d.text(s, k, M, y, 2.3, 0.8, size=14, font=HEAD, bold=True, color=INK)
        d.text(s, v, M + 2.4, y, 4.3, 0.85, size=12.5, color=BODY)
    d.paper_figure(s, "gardner2000_fig1", 7.6, 2.05, 4.9, 1.99,
                   "Gardner 2000, Fig. 1", "the design")
    d.paper_figure(s, "gardner2000_fig3", 8.28, 4.45, 3.54, 1.75,
                   "Gardner 2000, Fig. 3", "the plasmid")
    d.assigned_on(M, 6.05, 6.6, s)
    d.foot(s, "Two promoters, two repressors, one reporter. That is the entire construct.")
    d.notes(s, "The point of this slide is that the thing is SMALL. Students consistently expect it to be complicated.")

    # 6 ARGUE -----------------------------------------------------------------
    s = d.dark()
    d.header(s, "16 – 26 min", "Argue it out  ·  groups of 3–4")
    d.title(s, "It works. Why?")
    d.text(s, "You have the whole construct. No equations yet.", M, 1.95, 11, 0.4,
           size=17, color=MINT)
    for i, q in enumerate([
            "Why does mutual repression hold a state at all, once the inducer is removed?",
            "What has to be true of the two repressors for this to work? Be specific — name a property.",
            "What could you change that would break it?"]):
        y = 2.75 + i * 1.15
        d.shape(s, S.OVAL, M, y + 0.05, 0.44, 0.44, fill=CYAN, line=None)
        d.text(s, str(i + 1), M, y + 0.13, 0.44, 0.3, size=15, bold=True,
               color=INK, align="c")
        d.text(s, q, M + 0.8, y, 11.2, 0.85, size=18, color=WHITE)
    d.foot(s, "Question 2 is the one that matters. Most groups get there by arguing about what happens when the two repressors are equally strong.", 6.25)
    d.notes(s, "THE GENERATION PHASE, and it is analysis of a real artifact rather than invention from nothing. Collect answers on the board BY GROUP — you name them again in 12 minutes. Correct nothing yet.")

    # 7 WHAT IT REQUIRES ------------------------------------------------------
    s = d.light()
    d.header(s, "26 – 32 min", "Your answers, sorted")
    d.title(s, "What you just derived")
    for i, (k, sub, txt, c) in enumerate([
            ("Mutual repression", "necessary, not sufficient",
             "Every group had this. It is the easy half.", TEAL),
            ("Cooperativity", "the one that matters",
             "Without it the nullclines cross once, and there is only one state. Groups 2 and 5 got here by arguing about symmetry.", CYAN),
            ("Balanced strengths", "sets how wide the window is",
             "If one arm overwhelms the other, one state swallows the other.", TEAL),
            ("Slow enough removal", "the state has to outlive the signal",
             "Nobody raised this. Hold onto it — it comes back at 40 hours.", AMBER)]):
        y = 2.0 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.16, 0.95, fill=c, line=None)
        d.text(s, k, M + 0.4, y, 3.1, 0.45, size=17, font=HEAD, bold=True, color=INK)
        d.text(s, sub, M + 0.4, y + 0.45, 3.1, 0.35, size=12, italic=True, color=MUTED)
        d.text(s, txt, M + 3.8, y + 0.05, 8.1, 0.9, size=14, color=BODY)
    d.notes(s, "Name real groups. This is the consolidation step and it is the fidelity condition for the whole generation phase — skip it and the previous ten minutes were wasted. The amber row is the one they will not have said; flag it as a debt paid later.")

    # 8 THE MODEL -------------------------------------------------------------
    s = d.light()
    d.header(s, "32 – 40 min", "Abstraction")
    d.title(s, "Now write it down")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.9, 6.0, 1.75, fill=CARD, line=TEAL, lw=2)
    d.text(s, "du/dt  =  α₁ / (1 + v^β)  −  u\ndv/dt  =  α₂ / (1 + u^γ)  −  v",
           M + 0.35, 2.15, 5.4, 1.25, size=21, font=HEAD, bold=True, color=INK,
           spacing=1.5)
    for i, (sym, txt) in enumerate([
            ("u, v", "the two repressor concentrations"),
            ("α₁, α₂", "effective synthesis rates — promoter strength, RBS, copy number"),
            ("β, γ", "cooperativity of each repression"),
            ("−u, −v", "removal: degradation plus dilution by growth")]):
        y = 1.95 + i * 0.88
        d.text(s, sym, 7.15, y, 1.5, 0.4, size=17, font=HEAD, bold=True, color=CYAN)
        d.text(s, txt, 8.5, y + 0.03, 4.1, 0.75, size=13.5, color=BODY)
    d.text(s, "This is Box 1 of the paper, verbatim. Time is in units of protein lifetime, concentration in units of the repression threshold — four parameters left, and every one is something you argued about ten minutes ago.",
           7.15, 5.5, 5.45, 1.4, size=14, color=INK)
    # aspect 2.10 -- a wide, short strip. The box is sized to it.
    d.paper_figure(s, "gardner2000_box1", M, 3.85, 6.0, 2.86,
                   "Gardner 2000, Box 1", "the model as the paper states it")
    d.notes(s, "Derive the scaling on the board — two minutes, and it is where the four parameters come from. Note the notation: the paper uses beta and gamma for the cooperativities; posb.toggle_model calls them m and n. Say so once so nobody is confused reading the paper.")

    # 9 NULLCLINES ------------------------------------------------------------
    s = d.light()
    d.header(s, "40 – 45 min", "Concept")
    d.title(s, "Cooperativity is what bends the nullcline")
    d.image(s, "figures/build/s09_nullclines.png", M, 1.9, 6.6, 3.1)
    d.text(s, "generated from posb — the same call you make in the notebook",
           M, 5.05, 6.6, 0.3, size=11, italic=True, color=MUTED, align="c")
    # aspect 0.91 -- taller than wide, so it gets a tall slot on the right and
    # the three read-off lines move under the left figure.
    d.paper_figure(s, "gardner2000_fig2", 8.35, 1.9, 4.26, 4.7,
                   "Gardner 2000, Fig. 2", "their version of this same picture")
    for i, (k, txt, c) in enumerate([
            ("n = 1", "crosses once. One state, always.", MUTED),
            ("n > 1", "can cross three times: two stable, one saddle.", TEAL),
            ("the saddle", "its stable manifold is the separatrix.", CYAN)]):
        y = 5.28 + i * 0.37
        d.text(s, k, M, y, 1.45, 0.35, size=13.5, font=HEAD, bold=True, color=c)
        d.text(s, txt, M + 1.5, y + 0.02, 5.1, 0.35, size=12.5, color=BODY)
    d.foot(s, "Put them side by side and say it: a 2000 Nature result you can now regenerate in four lines.")
    d.notes(s, "The pairing is the point — their figure and yours, same picture, 26 years apart.")

    # 10 ENGINEERABILITY ------------------------------------------------------
    s = d.light()
    d.header(s, "45 – 52 min", "Design  ·  the question that separates this from a math course")
    d.title(s, "Which of these can you actually change?")
    for i, (p, verd, txt, c) in enumerate([
            ("α₁, α₂", "EASY", "Promoter libraries, RBS calculators, copy number. Continuously tunable over orders of magnitude.", GREEN),
            ("removal rate", "MODERATE", "ssrA/protease tags shorten lifetime — but they move the timescale AND the steady state together.", AMBER),
            ("β, γ", "HARD", "Cooperativity is set by the repressor's oligomerisation and operator architecture. You choose it by choosing a protein, not by tuning a knob.", RED),
            ("symmetry", "EASY, AND FRAGILE", "You can balance the arms — but growth rate, temperature and burden all unbalance them again.", AMBER)]):
        y = 1.88 + i * 1.10
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 2.3, 0.92, fill=CARD, line=c, lw=2)
        d.text(s, p, M, y + 0.1, 2.3, 0.4, size=19, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, verd, M, y + 0.56, 2.3, 0.3, size=10, bold=True, color=c, align="c")
        d.text(s, txt, M + 2.6, y + 0.05, 9.3, 0.9, size=14.5, color=BODY)
    d.text(s, "The parameter that most determines bistability is the one you can least control. That asymmetry is the design problem.",
           M, 6.42, W - 2 * M, 0.45, size=14, bold=True, color=INK)
    d.notes(s, "THE slide of the lecture. The math says n matters most; the biology says it is what you can least tune. Gardner solved it by CHOOSING repressors that already dimerise, not by tuning cooperativity.")

    # 11 CONCEPTEST -----------------------------------------------------------
    s = d.light()
    d.header(s, "≈ 3 min", "Vote  →  discuss  →  vote again")
    d.title(s, "You want this circuit to switch faster")
    for i, (letter, opt) in enumerate([
            ("A", "Use stronger promoters and RBSs"),
            ("B", "Attach protease recognition tags to both repressors"),
            ("C", "Increase the IPTG import rate"),
            ("D", "Replace the protein repressors with CRISPRi")]):
        y = 2.2 + i * 0.95
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, W - 2 * M, 0.75, fill=CARD, line=RULE, lw=1)
        d.text(s, letter, M + 0.25, y + 0.2, 0.5, 0.4, size=20, font=HEAD,
               bold=True, color=CYAN)
        d.text(s, opt, M + 0.9, y + 0.22, W - 2 * M - 1.2, 0.4, size=16, color=BODY)
    d.foot(s, "Vote alone. Then convince your neighbour. Then vote again.")
    d.notes(s, "Answer: B. Switching time is set by the removal rate, not synthesis. A raises both steady states but not the approach rate in scaled time. C changes the input, not the circuit. D changes the mechanism and its own timescale. Useful follow-up: B also shifts the steady states, so you buy speed and pay in bistable window width.")

    # 12 STEADY STATE vs DYNAMICS --------------------------------------------
    s = d.light()
    d.header(s, "52 – 60 min", "Two different questions")
    d.title(s, "Bistable is not the same as useful")
    for i, (kind, q, txt, hl) in enumerate([
            ("STEADY STATE", "Does it hold two states?",
             "Set by α and n. Answered by counting nullcline intersections. Gives the induction threshold.", False),
            ("DYNAMICS", "How fast does it flip?",
             "Set by the removal rate. In Gardner's construct that is hours: stable repressors, 30-minute doubling.", True)]):
        x = M + i * 6.2
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.82, 5.7, 1.92, fill=CARD,
                line=CYAN if hl else RULE, lw=2 if hl else 1)
        d.text(s, kind, x + 0.3, 1.96, 5, 0.28, size=10, bold=True,
               color=CYAN if hl else MUTED)
        d.text(s, q, x + 0.3, 2.24, 5.1, 0.45, size=19, font=HEAD, bold=True, color=INK)
        d.text(s, txt, x + 0.3, 2.74, 5.1, 1.0, size=13.5, color=BODY)
    d.text(s, "A circuit can be perfectly bistable and still useless, because it takes six hours to commit.",
           M, 3.86, W - 2 * M, 0.34, size=15, bold=True, color=INK)
    # fig5 is tall (0.74) and fig6 wide (1.65); both get the full remaining
    # height and centre themselves in it rather than being squeezed into a strip.
    d.paper_figure(s, "gardner2000_fig5a", M + 0.55, 4.28, 4.6, 2.6,
                   "Gardner 2000, Fig. 5a", "induction threshold, with hysteresis")
    d.paper_figure(s, "gardner2000_fig6", 7.60, 4.28, 4.29, 2.6,
                   "Gardner 2000, Fig. 6", "switching time")
    d.notes(s, "This is where the fourth requirement from slide 7 — the one nobody raised — gets paid off.")

    # 13 THE DERIVATION -------------------------------------------------------
    s = d.light()
    d.header(s, "the worked example", "Ten lines, and cooperativity stops being a slogan")
    d.title(s, "Where the requirement comes from")
    d.text(s, "At a symmetric fixed point  u = v = x :", M, 1.85, 6.2, 0.3,
           size=14, color=BODY)
    d.text(s, "x = α / (1 + xⁿ)        so        α = x + xⁿ⁺¹", M, 2.18, 6.2, 0.4,
           size=17, font=HEAD, bold=True, color=INK)
    d.text(s, "The Jacobian there is  [[−1, g], [g, −1]] , so the eigenvalues are −1 ± |g| .\nUsing (1 + xⁿ) = α/x this collapses to",
           M, 2.68, 6.2, 0.7, size=14, color=BODY)
    d.text(s, "|g| = n xⁿ⁺¹ / α", M, 3.42, 6.2, 0.4, size=17, font=HEAD,
           bold=True, color=INK)
    d.text(s, "It becomes a saddle exactly when |g| > 1 :", M, 3.9, 6.2, 0.3,
           size=14, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 4.28, 6.2, 1.6, fill=WASH, line=TEAL, lw=2)
    d.text(s, "n xⁿ⁺¹  >  x + xⁿ⁺¹\n(n − 1) xⁿ  >  1\nx  >  (n − 1)^(−1/n)",
           M + 0.35, 4.45, 5.6, 1.3, size=16, font=HEAD, bold=True, color=INK,
           spacing=1.35)
    d.shape(s, S.ROUNDED_RECTANGLE, 7.25, 1.85, 5.35, 2.2, fill=CARD, line=RED, lw=2)
    d.text(s, "Impossible for n ≤ 1", 7.55, 2.05, 4.8, 0.45, size=20, font=HEAD,
           bold=True, color=RED)
    d.text(s, "(n − 1)^(−1/n) is undefined. There is no x, and therefore no α however large, that gives two states.\n\nCooperativity is not an optimisation. It is a necessary condition.",
           7.55, 2.52, 4.8, 1.4, size=13.5, color=BODY)
    d.text(s, "Substituting back into  α = x(1 + xⁿ) :", 7.25, 4.2, 5.35, 0.3,
           size=13.5, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, 7.25, 4.58, 5.35, 1.0, fill=TEAL, line=TEAL)
    d.text(s, "critical α  =  n (n − 1)^−(n+1)/n", 7.25, 4.92, 5.35, 0.4, size=19,
           font=HEAD, bold=True, color=WHITE, align="c")
    d.foot(s, "Writing β = γ = n for the symmetric case. n = 2 gives critical α = 2 exactly — a theorem, not an observation.")
    d.notes(s, "DO THIS ON THE BOARD. Ten lines, and it converts 'you need cooperativity' from asserted to proved. Elowitz/Bois derive the analogous single-gene autoactivation condition; this is the two-gene version. posb.toggle_alpha_critical carries the same derivation, and tests/test_analysis.py checks it against numerics at n = 1.5, 2, 3, 4.")

    # 14 THE BOUNDARY, CHECKED ------------------------------------------------
    s = d.light()
    d.header(s, "≈ 2 min", "Analytic vs numerical")
    d.title(s, "And it is true")
    d.image(s, "figures/build/s09_bifurcation.png", 3.4, 1.8, 6.6, 4.4)
    d.foot(s, "Line: the formula we just derived. Points: the smallest α at which a numerical search finds two stable states. Same axes, no fitting.")
    d.notes(s, "Regenerated by tools/build_figures.py on every build, so the agreement is a live check rather than a claim.")

    # 15 FADED WORKED SET -----------------------------------------------------
    s = d.light()
    d.header(s, "60 – 66 min", "Worked set  ·  six minutes  ·  start where you like")
    d.title(s, "Four problems. The scaffolding falls away.")
    for i, (num, k, txt, c) in enumerate([
            ("1", "Fully worked", "fixed points for α = 3, n = 2", TEAL),
            ("2", "Last step blank", "you classify them", GREEN),
            ("3", "Last two blank", "you build the Jacobian too", CYAN),
            ("4", "Bare problem", "n = 1. Prove only one state exists.", CYAN)]):
        x = M + i * 3.05
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.1, 2.8, 2.5, fill=CARD, line=c, lw=2)
        d.shape(s, S.OVAL, x + 1.15, 2.35, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 1.15, 2.46, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 0.15, 3.05, 2.5, 0.4, size=15, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, txt, x + 0.15, 3.5, 2.5, 0.9, size=12, color=MUTED, align="c")
    d.text(s, "Start wherever the scaffolding stops helping you. Nobody needs to announce where that is.",
           M, 4.95, W - 2 * M, 0.4, size=16, bold=True, color=INK)
    d.text(s, "At each transition the handout asks: why does that step follow? Answer in writing before you go on.",
           M, 5.45, W - 2 * M, 0.4, size=14, color=BODY)
    d.notes(s, "SIX MINUTES, then stop. This was one twelve-minute block; no "
               "block of student work in this course runs past ten, because "
               "past that the fast half has finished and the slow half has "
               "stalled and neither is being taught. "
               "Circulate. Do NOT work item 1 at the board -- that removes the "
               "fading and collapses the set into a single demonstration. "
               "You are also scouting: at 66 you say out loud whichever of the "
               "two standard blockers you actually saw.")

    # 15b MID-SET, TWO MINUTES ------------------------------------------------
    s = d.dark()
    d.header(s, "66 – 68 min", "Two minutes at the front  ·  then back to it")
    d.title(s, "The two places people stall")
    for i, (k, txt) in enumerate([
            ("Setting the nullclines equal is not solving them",
             "You want the intersections of du/dt = 0 and dv/dt = 0. Substitute one into the other and you get a single equation in one variable — a polynomial. Solve that. Do not try to solve the pair simultaneously by inspection."),
            ("The Jacobian is evaluated AT a fixed point",
             "It is a matrix of numbers, not of symbols. Get the fixed point first, then substitute. Half the algebra people get stuck in disappears the moment they put the numbers in before differentiating rather than after.")]):
        y = 2.3 + i * 1.7
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.45, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.2, 0.85, size=16, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.0, y + 0.02, 7.5, 1.5, size=13, color=MINT)
    d.text(s, "Four more minutes. Item 4 is the one to reach — n = 1 is where the switch stops being a switch.",
           M, 5.85, 12.5, 0.5, size=18, font=HEAD, bold=True, color=CYAN)
    d.notes(s, "Two minutes and not a second more. Say the two things, take no "
               "questions, send them back. "
               "Neither of these gives away any answer -- both are about HOW to "
               "proceed, not what the result is, which is the line that keeps "
               "the fading intact.")

    # 15c WORKED SET, SECOND HALF ---------------------------------------------
    s = d.light()
    d.header(s, "68 – 72 min", "Worked set  ·  four more minutes  ·  reach item 4")
    d.title(s, "Keep going from wherever you are")
    for i, (num, k, txt, c) in enumerate([
            ("3", "Last two blank", "you build the Jacobian too", CYAN),
            ("4", "Bare problem", "n = 1. Prove only one state exists.", AMBER)]):
        x = M + i * 6.35
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.05, 6.15, 2.0, fill=CARD, line=c,
                lw=2)
        d.shape(s, S.OVAL, x + 0.3, 2.3, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 0.3, 2.41, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 1.0, 2.35, 4.9, 0.4, size=16, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, x + 1.0, 2.8, 4.9, 0.5, size=13, color=MUTED)
        d.text(s, "why does that step follow? — answer in writing before you go on",
               x + 0.3, 3.45, 5.5, 0.5, size=11.5, italic=True, color=MUTED)
    d.text(s, "Item 4 is the whole session in one problem: cooperativity is not decoration, and at n = 1 the bistability is simply gone.",
           M, 4.35, W - 2 * M, 0.5, size=16, bold=True, color=INK)
    d.foot(s, "Nobody is expected to finish item 4 here. What is expected is that you have tried it before I show you the answer.", 5.05)
    d.notes(s, "Four minutes. Stop at 72 regardless -- the failure slide is "
               "the point of the session and it needs its five minutes. "
               "Item 4 is the one that matters. If someone has it, ask them to "
               "say the argument out loud at 72 instead of you saying it.")

    # 16 IT FAILS -------------------------------------------------------------
    s = d.dark()
    d.header(s, "72 – 77 min", "The part the paper does not celebrate")
    d.title(s, "The toggle set to green fails after 40 hours")
    d.paper_figure(s, "toggle_longevity_2025deck", M, 1.62, 5.3, 2.38,
                   "pTog dual-reporter toggle · unpublished flow cytometry",
                   "pTog dual-reporter toggle, 2 h / 31 h / 40 h")
    d.unattributed(s, M, 4.32, 5.9,
                   "whose pTog data is this? Weiss lab / course / other")
    for i, (t, txt) in enumerate([("2 h", "clean separation"),
                                  ("31 h", "green is broadening"),
                                  ("40 h", "leaked back to red")]):
        y = 1.9 + i * 0.7
        d.text(s, t, 7.1, y, 1.1, 0.45, size=20, font=HEAD, bold=True,
               color=AMBER if i == 2 else WHITE)
        d.text(s, txt, 8.3, y + 0.08, 4.3, 0.4, size=14, color=MINT)
    d.text(s, "Why would it fail? What would you change?", M, 4.95, 11, 0.5,
           size=26, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Two minutes with your neighbour. There are at least four distinct mechanisms and they need different fixes.",
           M, 5.52, 11, 0.4, size=16, color=MINT)
    d.foot(s, "Mutation in a repressor · promoter mutation · plasmid loss · burden selecting against the expressing state", 6.3)
    d.notes(s, "PROVENANCE: these panels are NOT from Gardner 2000 (their longest run is Fig. 4c at ~28 h, and it shows stability). The FCS filenames visible in the original slide — 2h_pTog1,2f,+i.fcs / 31h_.. / 40h_.. — show this is unpublished flow cytometry on a pTog dual-reporter construct (mCherry + GFP, LacI/TetR, IPTG/aTc). Almost certainly Weiss-lab or course data. Confirm whose it is and put a name on the slide before delivering. Note also the middle panel is 31 h, not 30 h as the old caption said. Do not reveal the four mechanisms until they have argued. Key distinction: a mutation that breaks the CIRCUIT versus selection that breaks the POPULATION. Different engineering responses — sequence redundancy versus lowering burden.")

    # 17 ROBUSTNESS -----------------------------------------------------------
    s = d.light()
    d.header(s, "77 – 78 min", "What this generalises to")
    d.title(s, "Bistability lives in a parameter window")
    d.text(s, "Everything here is a preview. Session 23 does it properly.",
           M, 1.85, W - 2 * M, 0.3, size=13, italic=True, color=MUTED)
    for i, (k, txt) in enumerate([
            ("The window is finite", "There is a region of (α, n) where two states exist. Outside it, one. The toggle sits inside by design."),
            ("Mutation is a random walk in parameter space", "Every generation some cells step. A cell that steps outside loses the state, permanently."),
            ("Expression costs growth", "The state that expresses more is selected against. Not a circuit failure — the population editing your design."),
            ("Robustness is an objective, not a property", "You can put the operating point in the middle of the window instead of the edge. That costs dynamic range.")]):
        y = 2.4 + i * 1.05
        d.text(s, k, M, y, 4.3, 0.85, size=15.5, font=HEAD, bold=True, color=INK)
        d.text(s, txt, M + 4.6, y + 0.03, 7.3, 0.9, size=14, color=BODY)
    d.notes(s, "Sixty seconds. A hook for session 23, not a treatment.")

    # 18 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "78 – 80 min", "Next")
    d.title(s, "A toggle holds a state. What holds a rhythm?")
    d.text(s, "Tuesday: feedforward loops.  Then: three repressors in a ring.",
           M, 2.05, 11, 0.45, size=23, font=HEAD, bold=True, color=MINT)
    d.text(s, "Two mutually repressing genes give you two stable states.\n\nAdd a third repressor and close the loop, and there is no stable state at all — the system never settles.\n\nWhy should an odd number of repressors behave completely differently from an even number?",
           M, 2.72, 11.3, 2.0, size=16, color=WHITE, spacing=1.4)
    d.text(s, "You cannot answer that yet. Session 11.", M, 4.72, 6.5, 0.32,
           size=14, italic=True, color=CYAN)
    d.text(s, "Project description due tonight.", 7.4, 4.72, 5.2, 0.32,
           size=13, bold=True, color=SILVER, align="r")
    d.assignment(s, y=5.12)
    d.notes(s, "Pose it as a constraint on the next problem, not a summary of this one.")

    return d
