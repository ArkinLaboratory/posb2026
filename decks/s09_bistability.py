"""Session 9 — Bistability and the toggle switch.

Thursday 24 September. **Re-cut 18 September** after session 8 took the
derivations: nullclines, fixed points, the Jacobian, a_c, the scaling from
Box 1 and the bistable wedge of Fig. 2c,d all now happen on Tuesday, and the
first build of this deck repeated every one of them.

What this session does that Tuesday cannot: turn ONE knob on the device that
was actually built and watch a stable state die. IPTG stretches one nullcline;
the low state and the saddle approach, touch and annihilate -- the paper's own
sentence -- and the cell jumps. That is the induction threshold of Fig. 5a, a
saddle-node bifurcation, and the model's own parameters put it at 39 uM, where
the data jump. Remove the IPTG and it does not jump back: hysteresis, memory.

Then: what you can change in the lab, what sets the switching TIME (removal,
Fig. 6), and why the thing fails after 40 hours.

Coverage matrix: T21 (faded set: n = 4 and n = 1), T22 (bifurcation diagram,
hysteresis), T23 (saddle-node; what destroys bistability).

Sign convention: the coupling number is g, as in session 8 (g_1 g_2 > 1 for
the asymmetric case, from Tuesday's handout).
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session09_Bistability"
FIG = "figures/build/"


def build():
    d = Deck("Session 9 — Bistability and the toggle switch", session=9)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 9", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Bistability and the toggle switch", M, 2.72, 9.0, 1.3,
           size=42, font=HEAD, bold=True, color=WHITE)
    d.text(s, "One knob on a real device, and a state that dies",
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
            ("From Tuesday", "Two numbers decide whether a fixed point of the toggle is a saddle. Which two, and what is the test?", TEAL),
            ("From session 4", "When does the quasi-steady-state approximation fail?", CYAN)]):
        y = 2.15 + i * 1.25
        d.shape(s, S.OVAL, M, y, 0.42, 0.42, fill=c, line=None)
        d.text(s, str(i + 1), M, y + 0.08, 0.42, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, src.upper(), M + 0.75, y - 0.02, 3, 0.28, size=14,
               bold=True, color=MUTED)
        d.text(s, q, M + 0.75, y + 0.26, W - 2 * M - 0.75, 0.6, size=17, color=BODY)
    d.foot(s, "Question 3 is deliberately from three sessions back. The spacing is the point.")
    d.notes(s, "Elaborative, not factual. Collect answers; do not lecture them.\n"
               "Q2 wants g_1 g_2 > 1 from the handout, or lambda = -1 +/- g from "
               "the symmetric run. Either is right; the product is the general "
               "form.")

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
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=14, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "Why does the toggle flip all at once at 40 µM IPTG, and not gradually — and why does it not flip back when the IPTG is gone?",
            "Of the parameters that set bistability, which can you change in a lab, and which are you stuck with?",
            "It works. Why does it fail after 40 hours?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "Goals as questions they cannot yet answer. The first one is the "
               "session's spine: Tuesday found the fixed points; today one of "
               "them is destroyed on purpose.")

    # 4 WHY MEMORY ------------------------------------------------------------
    s = d.light()
    d.header(s, "8 – 12 min", "The problem")
    d.title(s, "Every circuit so far forgets")
    for i, (kind, eq, txt, hl) in enumerate([
            ("COMBINATIONAL", "output = f(input)",
             "Remove the inducer and the output returns to where it started. Everything through session 7 behaves this way.", False),
            ("SEQUENTIAL", "output = f(input, state)",
             "Remove the inducer and the output stays. The circuit has to hold something after the signal is gone.", True)]):
        x = M + i * 6.2
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.0, 5.7, 2.0,
                fill=WASH if hl else CARD, line=TEAL if hl else RULE, lw=2 if hl else 1)
        d.text(s, kind, x + 0.3, 2.2, 5, 0.28, size=14, bold=True,
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
            ("One reporter", "GFPmut3, in the cI operon — the state is visible.")]):
        y = 2.45 + i * 0.92
        d.text(s, k, M, y, 2.3, 0.8, size=14, font=HEAD, bold=True, color=INK)
        d.text(s, v, M + 2.4, y, 4.3, 0.85, size=14, color=BODY)
    d.paper_figure(s, "gardner2000_fig1", 7.6, 2.05, 4.9, 1.99,
                   "Gardner 2000, Fig. 1", "the design")
    d.paper_figure(s, "gardner2000_fig3", 8.28, 4.45, 3.54, 1.75,
                   "Gardner 2000, Fig. 3", "the plasmid")
    d.assigned_on(M, 6.05, 6.6, s)
    d.foot(s, "Two promoters, two repressors, one reporter. That is the entire construct.")
    d.notes(s, "The point of this slide is that the thing is SMALL. Students "
               "consistently expect it to be complicated.\n"
               "GFP sits with cI, downstream of Ptrc-2: the HIGH state is cI on, "
               "LacI off. The LOW state is LacI on. Say which is which now; the "
               "whole threshold argument reads GFP as v.")

    # 6 ARGUE -----------------------------------------------------------------
    s = d.dark()
    d.header(s, "16 – 26 min", "Argue it out  ·  groups of 3–4")
    d.title(s, "It works. Where, in the parts, is the reason?")
    d.text(s, "You have Tuesday's criterion and the whole construct. Point at the physical thing.", M, 1.95, 11.6, 0.4,
           size=17, color=MINT)
    for i, q in enumerate([
            "The criterion needs cooperativity on at least one arm. Which repressor supplies it in pTAK, and what about the protein makes it cooperative?",
            "Six toggle variants differ only in the ribosome-binding site in front of lacI. In the language of the wedge, what were they searching for?",
            "Name one change to the construct that would break it, and the parameter it moves."]):
        y = 2.75 + i * 1.15
        d.shape(s, S.OVAL, M, y + 0.05, 0.44, 0.44, fill=CYAN, line=None)
        d.text(s, str(i + 1), M, y + 0.13, 0.44, 0.3, size=15, bold=True,
               color=INK, align="c")
        d.text(s, q, M + 0.8, y, 11.2, 0.85, size=18, color=WHITE)
    d.foot(s, "Question 2 is the one that matters: an RBS moves α, and α is the axis of the wedge you can move along.")
    d.notes(s, "THE GENERATION PHASE, and it is analysis of a real artifact "
               "rather than invention from nothing. Collect answers on the "
               "board BY GROUP — you name them again in ten minutes. Correct "
               "nothing yet.\n"
               "Q1: cI dimerises and binds cooperatively to OR1/OR2 (session 6, "
               "Ackers). The Fig. 5 fit gives beta = 2.5 on the cI arm and "
               "gamma = 1 on the LacI arm. That is the handout from Tuesday.\n"
               "Q2: alpha_1, the LacI arm - RBS1 sits in front of lacI (Fig. 3). "
               "They were walking the point into the wedge along one axis, one "
               "RBS at a time: four pTAK and two pIKE variants, five of the six "
               "inside.\n"
               "Q3: anything. The good answers name the parameter: a weaker "
               "promoter (alpha), a monomeric repressor (beta), a degradation "
               "tag (removal, and therefore alpha in scaled units).")

    # 7 WHAT IT REQUIRES ------------------------------------------------------
    s = d.light()
    d.header(s, "26 – 32 min", "Your answers, sorted")
    d.title(s, "What you just said, sorted")
    for i, (k, sub, txt, c) in enumerate([
            ("Mutual repression", "necessary, not sufficient",
             "Every group had this. It is the easy half.", TEAL),
            ("Cooperativity on one arm", "at least one — the one that matters",
             "cI dimerises; LacI in the paper's own fit has γ = 1, and the switch works anyway. Tuesday's handout is why.", CYAN),
            ("Balanced strengths", "inside the wedge",
             "If one arm overwhelms the other, one state swallows the other. pIKE105 is the variant that fell out.", TEAL),
            ("Slow enough removal", "the state has to outlive the signal",
             "Nobody raised this. Hold onto it — it sets the switching time, and it comes back at 40 hours.", AMBER)]):
        y = 2.0 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.16, 0.95, fill=c, line=None)
        d.text(s, k, M + 0.4, y, 3.6, 0.45, size=17, font=HEAD, bold=True, color=INK)
        d.text(s, sub, M + 0.4, y + 0.45, 3.6, 0.35, size=14, italic=True, color=MUTED)
        d.text(s, txt, M + 4.3, y + 0.05, 7.6, 0.9, size=14, color=BODY)
    d.notes(s, "Name real groups. This is the consolidation step and it is the "
               "fidelity condition for the whole generation phase — skip it and "
               "the previous ten minutes were wasted. The amber row is the one "
               "they will not have said; flag it as a debt paid later.")

    # 8 WHAT TUESDAY GAVE YOU -------------------------------------------------
    s = d.light()
    d.header(s, "32 – 35 min", "Tuesday, in three lines")
    d.title(s, "Nothing today needs a new tool")
    d.paper_figure(s, "gardner2000_box1", M, 1.75, 6.0, 2.86,
                   "Gardner 2000, Box 1", "the model as the paper states it")
    for i, (k, txt) in enumerate([
            ("Fixed points", "are where the two nullclines cross. Count them on the drawing."),
            ("A crossing is a saddle", "exactly when the loop gain g₁g₂ > 1 — the cell cannot sit there."),
            ("Two states exist", "inside a wedge in the (α₂, α₁) plane, and cooperativity opens it.")]):
        y = 1.85 + i * 1.05
        d.text(s, k, 7.1, y, 5.5, 0.4, size=17, font=HEAD, bold=True, color=INK)
        d.text(s, txt, 7.1, y + 0.42, 5.5, 0.6, size=14, color=BODY)
    d.text(s, "Today we hold everything fixed except one thing the experimenter controls — and watch what the picture does.",
           M, 5.0, W - 2 * M, 0.9, size=18, font=HEAD, bold=True, color=INK)
    d.foot(s, "u = LacI, v = cI (and GFP), each in units of its threshold; time in protein lifetimes. α₁ = 156, α₂ = 15.6, β = 2.5, γ = 1 from the Fig. 5 legend.")
    d.notes(s, "Three lines and move on. Every one of them was derived on "
               "Tuesday; do not re-derive. The point of the surface is that the "
               "next ten minutes use only these.\n"
               "Notation, said once: the paper's beta and gamma are the "
               "cooperativities; posb.toggle_model calls them m and n.")

    # 9 RUN — WHERE THE THRESHOLD COMES FROM ---------------------------------
    d.derivation_fig(
        "35 – 45 min", "Built one line at a time",
        "Where the threshold comes from",
        [("IPTG does one thing to the model",
          "u  →  u / (1 + [IPTG]/K)^{η}      in dv/dt only",
          "LacI bound to IPTG does not repress: promoter 2 sees less LacI. Fig. 5's legend, in our notation"),
         ("So one nullcline stretches and the other does not move",
          "v  =  α_{2} / (1 + (u/s)^{γ}) ,      s ≡ (1 + [IPTG]/K)^{η}",
          "s = 1 with no inducer. Raising IPTG raises s, and the v-nullcline slides to the right"),
         ("The low state and the saddle meet, and annihilate",
          "at  s = s_{c}  the two curves are tangent",
          "a saddle-node: the paper says ‘one of the stable steady states is annihilated by the unstable steady state’"),
         ("Past s_{c} there is one state, and the cell must jump",
          "s > s_{c}   ⇒   only the high state remains",
          "from the legend’s own K and η, s_{c} = 5.4 is 39 µM IPTG. Fig. 5a jumps at 40"),
         ("Take the IPTG away, and it does not jump back",
          "s → 1 :   the high state still exists. It stays.",
          "the up-threshold is a saddle-node; there is no down-threshold on this axis. That gap is the memory")],
        [FIG + "s09_fold_p1.png", FIG + "s09_fold_p2.png", FIG + "s09_fold_p3.png",
         FIG + "s09_fold_p4.png", FIG + "s09_hysteresis.png"],
        closing="A threshold is a saddle-node. Memory is a state that outlives its signal.",
        board="s_{c} = 5.4  ⇔  39 µM IPTG,   from K and η in the Fig. 5 legend",
        note=("The whole run is one knob. Say so at the top: nothing about the "
              "circuit changes, only how much of the LacI is able to bind.\n"
              "Step 2 is the picture to dwell on: the u-nullcline is fixed and "
              "the v-nullcline stretches. Students will expect both to move.\n"
              "Step 3 is the word 'annihilate' and it is the paper's. Two "
              "fixed points, one stable and one saddle, meet and cancel. That "
              "is what a saddle-node bifurcation IS; it has no other content.\n"
              "Step 4: 39 micromolar is computed from the legend's K = 2.96e-5 "
              "and eta = 2.0015, by bisection on the number of fixed points "
              "(figures/s09_bistability.py::iptg_threshold). The data in "
              "Fig. 5a jump between points 2 and 3 at 4e-5 M. That agreement "
              "is the payoff of the whole two days; let it land.\n"
              "Step 5: the reason the toggle needs TWO inducers. On the IPTG "
              "axis there is an up-threshold and no down-threshold; to reset "
              "you heat it, which is the other knob. That is hysteresis, and "
              "it is what 'memory' means for this circuit.\n"
              "LEDGER: s_c and the 39 micromolar, beside Tuesday's lines."))

    # 10 THE PAPER'S FIGURE BESIDE OURS --------------------------------------
    s = d.light()
    d.header(s, "45 – 48 min", "The paper  ·  the same curve, drawn by them")
    d.title(s, "Fig. 5a is that picture, with the cells on it")
    d.paper_figure(s, "gardner2000_fig5a", M, 1.7, 6.6, 4.4,
                   "Gardner 2000, Fig. 5a",
                   "normalized GFP against [IPTG]: two stable branches, the unstable one between")
    d.image(s, FIG + "s09_hysteresis.png", 7.5, 1.7, 5.1, 4.6)
    d.foot(s, "Red circles are the toggle; blue triangles are a plain IPTG-inducible control with no memory. Points 3a and 3b are one culture, split in two — the bimodality near a bifurcation.")
    d.notes(s, "Theirs is linear and normalised; ours is log in v*. Same curve. "
               "The bimodal points 3a/3b are the deterministic story meeting "
               "noise: the culture sits close to the fold, so fluctuations "
               "push some cells over and not others. Session 12 has the tool "
               "for that.\n"
               "The blue control is the thing to point at: same inducer, same "
               "reporter, no positive feedback, and the response is a smooth "
               "sigmoid with no memory. The toggle's sharpness and its memory "
               "are the same fact.")

    # 11 ENGINEERABILITY ------------------------------------------------------
    s = d.light()
    d.header(s, "48 – 55 min", "Design  ·  the question that separates this from a math course")
    d.title(s, "Which of these can you change?")
    for i, (p, verd, txt, c) in enumerate([
            ("α₁, α₂", "EASY", "Promoter libraries, RBS swaps, copy number. Gardner built six variants differing in one RBS; five landed inside the wedge.", GREEN),
            ("removal rate", "MODERATE", "ssrA tags shorten a lifetime — and in scaled units that lowers α, so you move the point AND the timescale.", AMBER),
            ("β, γ", "HARD", "Cooperativity is set by the repressor's oligomerisation and the operator architecture. You choose it by choosing a protein.", RED),
            ("symmetry", "EASY, AND FRAGILE", "You can balance the arms — but growth rate, temperature and burden all unbalance them again.", AMBER)]):
        y = 1.88 + i * 1.10
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 2.3, 0.92, fill=CARD, line=c, lw=2)
        d.text(s, p, M, y + 0.1, 2.3, 0.4, size=19, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, verd, M, y + 0.56, 2.3, 0.3, size=14, bold=True, color=c, align="c")
        d.text(s, txt, M + 2.6, y + 0.05, 9.3, 0.9, size=14.5, color=BODY)
    d.text(s, "The parameter that most determines bistability is the one you can least control. That asymmetry is the design problem.",
           M, 6.42, W - 2 * M, 0.45, size=16, bold=True, color=INK)
    d.notes(s, "THE slide of the lecture. The math says cooperativity opens the "
               "wedge; the biology says it is what you can least tune. Gardner "
               "solved it by CHOOSING a repressor that already dimerises, not "
               "by tuning cooperativity — and then tuned alpha, the easy axis, "
               "with RBSs.")

    # 12 CONCEPTEST -----------------------------------------------------------
    s = d.light()
    d.header(s, "55 – 60 min", "Pose  ·  paper  ·  silent vote  ·  argue")
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
    d.foot(s, "Time is measured in protein lifetimes. What sets a lifetime, and which option changes it?")
    d.notes(s, "Answer: B. Switching time is set by the removal rate, not "
               "synthesis. A raises both steady states but not the approach "
               "rate in scaled time. C changes the input, not the circuit. D "
               "changes the mechanism and its own timescale.\n"
               "Follow-up that matters: B also shifts the steady states — a tag "
               "lowers alpha in scaled units — so you buy speed and pay in "
               "wedge width. And tag ONE repressor and Tuesday's tau = -2 is "
               "gone: the two removal rates differ, J is not symmetric, and the "
               "criterion is g_1 g_2 > delta_1 delta_2. That is item 4 of "
               "Tuesday's handout and PS4.")

    # 13 STEADY STATE vs DYNAMICS --------------------------------------------
    s = d.light()
    d.header(s, "60 – 65 min", "Two different questions")
    d.title(s, "Bistable is not the same as useful")
    for i, (kind, q, txt, hl) in enumerate([
            ("STEADY STATE", "Does it hold two states?",
             "Set by α and cooperativity. Answered by counting crossings. Gives the threshold — 39 µM.", False),
            ("DYNAMICS", "How fast does it flip?",
             "Set by the removal rate. In pTAK117 low→high begins at 3–4 h and is complete by 6 h: LacI–IPTG is only diluted by growth. High→low takes 35 min: cI857 is destroyed by heat.", True)]):
        x = M + i * 6.2
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.82, 5.7, 1.92, fill=CARD,
                line=CYAN if hl else RULE, lw=2 if hl else 1)
        d.text(s, kind, x + 0.3, 1.96, 5, 0.28, size=14, bold=True,
               color=CYAN if hl else MUTED)
        d.text(s, q, x + 0.3, 2.24, 5.1, 0.45, size=19, font=HEAD, bold=True, color=INK)
        d.text(s, txt, x + 0.3, 2.74, 5.1, 1.0, size=14, color=BODY)
    d.text(s, "A circuit can be perfectly bistable and still useless, because it takes six hours to commit.",
           M, 3.86, W - 2 * M, 0.34, size=16, bold=True, color=INK)
    d.paper_figure(s, "gardner2000_fig4", M, 4.25, 1.75, 2.72,
                   "Fig. 4", "22 h in both states")
    d.paper_figure(s, "gardner2000_fig6", 2.9, 4.28, 4.3, 2.6,
                   "Gardner 2000, Fig. 6", "switching time: 3–4 h to begin, complete by 6 h")
    for i, (k, txt) in enumerate([
            ("low → high: 3–4 h to begin, done by 6", "LacI bound to IPTG is only diluted by growth"),
            ("high → low: 35 min", "cI857 is destroyed by heat — active removal"),
            ("the ratio is the removal", "nobody designed it; the parts came with it")]):
        y = 4.35 + i * 0.8
        d.text(s, k, 7.6, y, 5.0, 0.35, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, txt, 7.6, y + 0.36, 5.0, 0.4, size=14, color=BODY)
    d.notes(s, "This is where the fourth requirement from the sorted slide — "
               "the one nobody raised — gets paid off. The asymmetry in the two "
               "switching times is the asymmetry in the two removal "
               "mechanisms: dilution against active destruction. The circuit "
               "was not designed to have it; the biology of the parts gave it "
               "to them.")

    # 14 FADED WORKED SET -----------------------------------------------------
    s = d.light()
    d.header(s, "65 – 71 min", "Worked set  ·  handout  ·  start where you like")
    d.title(s, "Four problems. The scaffolding falls away.")
    for i, (num, k, txt, c) in enumerate([
            ("1", "Fully worked", "n = 4, α = 2: every crossing, classified", TEAL),
            ("2", "Last step blank", "the off-diagonal pair: you classify them", GREEN),
            ("3", "Last two blank", "n = 1, α = 2: crossing, Jacobian, verdict", CYAN),
            ("4", "Bare problem", "halve α₁ only. Which state dies, and how?", AMBER)]):
        x = M + i * 3.05
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.1, 2.8, 2.5, fill=CARD, line=c, lw=2)
        d.shape(s, S.OVAL, x + 1.15, 2.35, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 1.15, 2.46, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 0.15, 3.05, 2.5, 0.4, size=16, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, txt, x + 0.15, 3.5, 2.5, 0.9, size=14, color=MUTED, align="c")
    d.text(s, "Start wherever the scaffolding stops helping you. Nobody needs to announce where that is.",
           M, 4.95, W - 2 * M, 0.4, size=18, bold=True, color=INK)
    d.text(s, "At each transition the handout asks: why does that step follow? Answer in writing before you go on.",
           M, 5.45, W - 2 * M, 0.4, size=16, color=BODY)
    d.notes(s, "Six minutes, then the two-minute surface, then four more. "
               "Circulate. Do NOT work item 1 at the board — that removes the "
               "fading and collapses the set into a single demonstration. "
               "You are also scouting: at 71 you say out loud whichever of the "
               "two standard blockers you actually saw.\n"
               "alpha = 2 throughout so the symmetric crossing is x = 1 by "
               "hand at both n = 4 and n = 1. Item 4 is the saddle-node again, "
               "by construction instead of by inducer — it is pIKE105.")

    # 14b MID-SET, TWO MINUTES ------------------------------------------------
    s = d.dark()
    d.header(s, "71 – 73 min", "Two minutes at the front  ·  then back to it")
    d.title(s, "The two places people stall")
    for i, (k, txt) in enumerate([
            ("Setting the nullclines equal is not solving them",
             "You want the intersections of du/dt = 0 and dv/dt = 0. Substitute one into the other and you get a single equation in one variable. Solve that."),
            ("The Jacobian is evaluated AT a fixed point",
             "It is a matrix of numbers, not of symbols. Get the fixed point first, then substitute. Half the algebra disappears the moment the numbers go in before you differentiate.")]):
        y = 2.3 + i * 1.7
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.45, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.2, 0.85, size=16, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.0, y + 0.02, 7.5, 1.5, size=14, color=MINT)
    d.text(s, "Four more minutes. Item 4 is the one to reach — it is today's saddle-node with a different knob.",
           M, 5.85, 12.5, 0.5, size=18, font=HEAD, bold=True, color=CYAN)
    d.notes(s, "Two minutes. Say the two things, take no questions, send them "
               "back. Neither gives away an answer — both are about HOW to "
               "proceed, which is the line that keeps the fading intact.")

    # 14c WORKED SET, SECOND HALF ---------------------------------------------
    s = d.light()
    d.header(s, "73 – 77 min", "Worked set  ·  four more minutes  ·  reach item 4")
    d.title(s, "Keep going from wherever you are")
    for i, (num, k, txt, c) in enumerate([
            ("3", "Last two blank", "n = 1, α = 2: crossing, Jacobian, verdict", CYAN),
            ("4", "Bare problem", "halve α₁ only. Which state dies, and how?", AMBER)]):
        x = M + i * 6.35
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.05, 6.15, 2.0, fill=CARD, line=c,
                lw=2)
        d.shape(s, S.OVAL, x + 0.3, 2.3, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 0.3, 2.41, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 1.0, 2.35, 4.9, 0.4, size=16, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, x + 1.0, 2.8, 4.9, 0.5, size=14, color=MUTED)
        d.text(s, "why does that step follow? — answer in writing before you go on",
               x + 0.3, 3.45, 5.5, 0.5, size=14, italic=True, color=MUTED)
    d.text(s, "Item 4 is the session in one problem: weaken one arm and a stable state is annihilated by the saddle — the same event as 39 µM, built in instead of induced.",
           M, 4.35, W - 2 * M, 0.7, size=16, bold=True, color=INK)
    d.foot(s, "Nobody is expected to finish item 4 here. What is expected is that you have drawn the two curves before I show you the answer.")
    d.notes(s, "Four minutes. Stop at 77 regardless — the failure surface is "
               "the point of the session. If someone has item 4, ask them to "
               "say the argument out loud instead of you saying it.")

    # 15 IT FAILS -------------------------------------------------------------
    s = d.dark()
    d.header(s, "77 – 80 min", "The part the paper does not celebrate")
    d.title(s, "The toggle set to green fails after 40 hours")
    d.paper_figure(s, "toggle_longevity_2025deck", M, 1.62, 5.3, 2.38,
                   "pTog dual-reporter toggle · unpublished flow cytometry",
                   "pTog dual-reporter toggle, 2 h / 31 h / 40 h")
    # Attribution: unpublished pTog flow cytometry from the 2025 deck, origin
    # not on record. Adam's decision, 20 Sep 2026: deliver it labelled as
    # unpublished (the ref line above), no name. See decks/paper_figures.yaml.
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
    d.foot(s, "Mutation in a repressor · promoter mutation · plasmid loss · burden selecting against the expressing state")
    d.notes(s, "PROVENANCE: these panels are NOT from Gardner 2000 (their "
               "longest run is Fig. 4c at 22 h, and it shows stability). The "
               "FCS filenames visible in the original slide — 2h_pTog1,2f,+i.fcs "
               "/ 31h_.. / 40h_.. — show this is unpublished flow cytometry on "
               "a pTog dual-reporter construct (mCherry + GFP, LacI/TetR, "
               "IPTG/aTc). Almost certainly Weiss-lab or course data. Confirm "
               "whose it is and put a name on the slide before delivering.\n"
               "Do not reveal the four mechanisms until they have argued. Key "
               "distinction: a mutation that breaks the CIRCUIT versus "
               "selection that breaks the POPULATION. Different engineering "
               "responses — sequence redundancy versus lowering burden.\n"
               "In the language of today: every one of the four moves the "
               "point in the (alpha_2, alpha_1) plane, and the edge of the "
               "wedge is a saddle-node. Failure is the cell walking out of "
               "the wedge.")

    # 16 ROBUSTNESS -----------------------------------------------------------
    s = d.light()
    d.header(s, "80 min", "What this generalises to")
    d.title(s, "Bistability lives in a parameter window")
    d.text(s, "Everything here is a preview. Session 23 does it properly.",
           M, 1.85, W - 2 * M, 0.3, size=14, italic=True, color=MUTED)
    for i, (k, txt) in enumerate([
            ("The window is finite", "The wedge. Outside it, one state. pTAK117 sits inside — and close to the lower edge."),
            ("Mutation is a random walk in parameter space", "Every generation some cells step. A cell that steps out of the wedge loses the state, permanently."),
            ("Expression costs growth", "The state that expresses more is selected against. Not a circuit failure — the population editing your design."),
            ("Robustness is an objective, not a property", "You can put the operating point in the middle of the wedge instead of the edge. That costs dynamic range.")]):
        y = 2.4 + i * 1.05
        d.text(s, k, M, y, 4.3, 0.85, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, txt, M + 4.6, y + 0.03, 7.3, 0.9, size=14, color=BODY)
    d.notes(s, "Sixty seconds. A hook for session 23, not a treatment.")

    # 17 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "80 min", "Next")
    d.title(s, "A toggle holds a state. What holds a rhythm?")
    d.text(s, "Tuesday: feedforward loops.  Then: three repressors in a ring.",
           M, 2.05, 11, 0.45, size=23, font=HEAD, bold=True, color=MINT)
    d.text(s, "Two mutually repressing genes give you two stable states.\n\nAdd a third repressor and close the loop, and there is no stable state at all — the system never settles.\n\nWhy should an odd number of repressors behave completely differently from an even number?",
           M, 2.72, 11.3, 2.0, size=16, color=WHITE, spacing=1.4)
    d.text(s, "You cannot answer that yet. Session 11 — the other exit from Tuesday's τ–Δ plane.", M, 4.72, 8.5, 0.32,
           size=14, italic=True, color=CYAN)
    d.text(s, "Project description due tonight.", 7.4, 4.72, 5.2, 0.32,
           size=14, bold=True, color=SILVER, align="r")
    d.assignment(s, y=5.12)
    d.notes(s, "Pose it as a constraint on the next problem, not a summary of "
               "this one. PS4 posts tonight: Q4-Q5 are Tuesday's handout items "
               "3-4, and the faded set's item 4 is the warm-up for them.")

    return d
