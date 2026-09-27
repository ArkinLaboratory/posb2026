"""Session 10 — Feedforward loops.

Tuesday 29 September. Continues from session 9: the toggle held a state; a
feedforward loop does something with TIME. Same three-node object, three jobs
-- delay, acceleration, pulse -- and three signs decide which.

Artifact first, the same shape as session 9: Basu's pulse generator (a real
incoherent type-1 FFL, Weiss lab) is the thing on the table; the abstraction
and the eight-type map (Mangan & Alon) come after the room has argued about the
device. Every result is related back to what a designer can turn -- an RBS, a
degradation tag, a promoter.

Two coverage rows are AUTO-graded on PS5, so both are stated as procedures with
their conventions written down:
  * the sign-sensitive DELAY (T24, T25), with the response-time convention on
    the slide, derived one line at a time in derivation_fig.
  * the ADAPTATION ERROR of the incoherent FFL (T26): peak, final, final/peak,
    read numerically off figures/build/s10_iffl_adaptation.png.

Every curve on the slides comes from figures/s10_feedforward.py, i.e. from
posb.core -- the plot on the wall is the plot in the notebook.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session10_Feedforward"
FIG = "figures/build/"


def build():
    d = Deck("Session 10 — Feedforward loops", session=10)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 10", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Feedforward loops", M, 2.72, 9.0, 1.3,
           size=42, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Three genes, three jobs, and the three signs that decide which",
           M, 4.15, 9.4, 0.5, size=18, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Continue from Thursday, as the announcement said. One line: the "
               "toggle held a state after the signal was gone. Today the signal "
               "is still there and the circuit does something with its timing.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions before we start")
    for i, (src, q, c) in enumerate([
            ("From Thursday", "A nullcline crossing is a saddle exactly when ______ .", TEAL),
            ("From Thursday", "The toggle flips low→high in hours but high→low in minutes. What sets that difference — production, or removal?", TEAL),
            ("From session 5", "A gene switched on with a step of inducer reaches half its steady state in about how long, in units of the protein's lifetime?", CYAN)]):
        y = 2.15 + i * 1.25
        d.shape(s, S.OVAL, M, y, 0.42, 0.42, fill=c, line=None)
        d.text(s, str(i + 1), M, y + 0.08, 0.42, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, src.upper(), M + 0.75, y - 0.02, 3.4, 0.28, size=14,
               bold=True, color=MUTED)
        d.text(s, q, M + 0.75, y + 0.26, W - 2 * M - 0.75, 0.6, size=17, color=BODY)
    d.foot(s, "Question 3 is the whole clock for today: response time is one protein lifetime, and everything here is measured against it.")
    d.notes(s, "Q1: g_1 g_2 > 1 (or lambda = -1 + g > 0). Q2: removal — the "
               "toggle's asymmetry was dilution vs active destruction. That is "
               "the fact today's delay is built on. Q3: t_half = ln2 ~ 0.7 "
               "lifetimes, from session 5. Say the number; the delay is measured "
               "against it.")

    # 2b CARRYOVER FROM SESSION 9 — the failure surface ----------------------
    # Session 9 was delivered through its slide 20 (the second half of the
    # faded set), and then its slide 23, the forward link -- Adam confirmed
    # 26 September that he gave the forward link, so d.assignment() fired and
    # Basu and Mangan & Alon went out in the room on schedule. What was NOT
    # reached is slides 21 and 22: the 40-hour failure surface and the
    # parameter window. Both are carried here, so the toggle is finished
    # before the new object starts.
    s = d.dark()
    d.header(s, "carry over", "Thursday, unfinished")
    d.title(s, "The toggle set to green fails after 40 hours")
    d.paper_figure(s, "toggle_longevity_2025deck", M, 1.62, 5.3, 2.38,
                   "pTog dual-reporter toggle · unpublished flow cytometry",
                   "pTog dual-reporter toggle, 2 h / 31 h / 40 h")
    # Attribution unchanged from session 9: unpublished pTog flow cytometry
    # from the 2025 deck, origin not on record. Delivered labelled, no name.
    for i, (t, txt) in enumerate([("2 h", "clean separation"),
                                  ("31 h", "green is broadening"),
                                  ("40 h", "leaked back to red")]):
        y = 1.9 + i * 0.7
        d.text(s, t, 7.1, y, 1.1, 0.45, size=20, font=HEAD, bold=True,
               color=AMBER if i == 2 else WHITE)
        d.text(s, txt, 8.3, y + 0.08, 4.3, 0.4, size=14, color=MINT)
    d.text(s, "Why would it fail? What would you change?", M, 4.95, 11, 0.5,
           size=26, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Two minutes with your neighbor. There are at least four distinct mechanisms and they need different fixes.",
           M, 5.52, 11, 0.4, size=16, color=MINT)
    d.foot(s, "Mutation in a repressor · promoter mutation · plasmid loss · burden selecting against the expressing state")
    d.notes(s, "CARRIED FROM SESSION 9, which ran out at its slide 20. Do not "
               "re-teach the toggle — this is the one surface that was left, "
               "and it is the bridge to today: a circuit can be correct and "
               "still fail, and what fails is TIMING and drift, not logic.\n"
               "PROVENANCE unchanged: these panels are NOT Gardner 2000 (their "
               "longest run is Fig. 4c at about 28 h, showing stability). Unpublished "
               "pTog flow cytometry, almost certainly Weiss-lab or course data. "
               "Still needs a name before it is delivered again.\n"
               "Do not reveal the four mechanisms until they have argued. Key "
               "distinction: a mutation that breaks the CIRCUIT versus selection "
               "that breaks the POPULATION — sequence redundancy versus lowering "
               "burden.")

    # 2c CARRYOVER — the parameter window ------------------------------------
    s = d.light()
    d.header(s, "carry over", "What that generalizes to")
    d.title(s, "Bistability lives in a parameter window")
    d.text(s, "A preview. Session 23 does it properly.",
           M, 1.85, W - 2 * M, 0.3, size=14, italic=True, color=MUTED)
    for i, (k, txt) in enumerate([
            ("The window is finite", "The wedge. Outside it, one state. pTAK117 sits inside — and close to the lower edge."),
            ("Mutation is a random walk in parameter space", "Every generation some cells step. A cell that steps out of the wedge loses the state, permanently."),
            ("Expression costs growth", "The state that expresses more is selected against. Not a circuit failure — the population editing your design."),
            ("Robustness is an objective, not a property", "You can put the operating point in the middle of the wedge instead of the edge. That costs dynamic range.")]):
        y = 2.4 + i * 1.05
        d.text(s, k, M, y, 4.3, 0.85, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, txt, M + 4.6, y + 0.03, 7.3, 0.9, size=14, color=BODY)
    d.text(s, "Today the circuits have three components instead of two, and what they control is not which state you are in — it is when.",
           M, 6.35, W - 2 * M, 0.5, size=16, bold=True, color=INK)
    d.notes(s, "CARRIED FROM SESSION 9. Sixty seconds — a hook for session 23, "
               "not a treatment. The last line is the hinge into today, so say "
               "it rather than clicking past it.")

    # 3 GOALS -----------------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By 9:30 you should be able to answer")
    for i, (n, lab) in enumerate([("8", "Phase plane"), ("9", "Bistability"),
                                  ("10", "Feedforward"), ("11", "Oscillation"),
                                  ("12", "Noise")]):
        x, here = M + i * 2.42, n == "10"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=14, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "One circuit ignores a signal that flickers on and off, but responds the moment the signal is steady. How, and why only in one direction?",
            "Another turns a lasting step of signal into a single pulse — on, then off, while the signal stays on. What makes it let go?",
            "Can a three-gene circuit reach its steady state faster than the one-gene version of the same thing \u2014 without changing a single lifetime?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "Goals as questions they cannot yet answer. All three are the "
               "same object seen three ways; the point of the session is that "
               "the wiring signs decide which one you get.\n"
               "Q1 lands on the derivation at 30\u201342. Q2 lands at 42\u201348. Q3 "
               "lands at 52\u201358, on the acceleration surface \u2014 and it is "
               "graded on PS5, so do not let that one get cut for time.")

    # 4 THE ARTIFACT ----------------------------------------------------------
    s = d.light()
    d.header(s, "8 – 14 min", "The artifact")
    d.title(s, "Basu, Mehreja, Thiberge, Chen & Weiss, PNAS 2004")
    d.text(s, "“Spatiotemporal control of gene expression with pulse-generating networks”",
           M, 1.9, 7.0, 0.4, size=16, font=HEAD, italic=True, color=TEAL)
    for i, (k, v) in enumerate([
            ("Sender", "makes AHL, a small molecule that diffuses to its neighbors."),
            ("Receiver", "LuxR·AHL turns on GFP — and turns on CI, which represses the GFP promoter."),
            ("The output", "GFP rises, then CI catches up and shuts it. A step in gives a pulse out."),
            ("The signature", "the signal drives the output and its own delayed brake. That is the incoherence.")]):
        y = 2.5 + i * 0.86
        d.text(s, k, M, y, 2.0, 0.8, size=14, font=HEAD, bold=True, color=INK)
        d.text(s, v, M + 2.05, y, 4.6, 0.85, size=14, color=BODY)
    d.paper_figure(s, "basu2004_fig1", 7.9, 1.95, 3.9, 3.6,
                   "Basu 2004, Fig. 1", "the sender/receiver pulse circuit")
    d.assigned_on(M, 6.05, 6.6, s)
    d.foot(s, "The whole receiver is three genes: one activator, one repressor it also switches on, one reporter.")
    d.notes(s, "GENERATION PHASE begins on the next slide; here just put the "
               "device on the table. Point at the incoherence physically: the "
               "same input, LuxR-AHL, does two opposite things to GFP — one "
               "direct and fast, one through CI and slow.\n"
               "Fig. 3 is the hook: the pulse height depends on how FAST the AHL "
               "rises, not just how high. Hold that; it comes back as distance "
               "sensing.")

    # 4b WHAT IT DOES — the rate hook ----------------------------------------
    s = d.light()
    d.header(s, "8 – 14 min", "The artifact  ·  what it does")
    d.title(s, "A lasting signal in, a single pulse out")
    d.paper_figure(s, "basu2004_fig3", M, 1.72, 11.9, 3.35,
                   "Basu 2004, Fig. 3",
                   "pulses at different AHL levels (a), and at different rates of rise (b, c)")
    for i, (k, txt) in enumerate([
            ("The AHL stays on", "It never goes away. The circuit lets go by itself."),
            ("Above ~47 nM it stops growing", "More signal, no more output — the repressor rises with it."),
            ("Rate matters, not just level", "A slow ramp gives a smaller, later pulse."),
            ("So a receiver tells near from far", "Distance from the sender IS the rate of rise. Cells 4.5 mm out never respond.")]):
        x = M + (i % 2) * 6.05
        y = 5.48 + (i // 2) * 0.62
        d.text(s, k, x, y, 5.8, 0.3, size=14, font=HEAD, bold=True, color=INK)
        d.text(s, txt, x, y + 0.27, 5.8, 0.32, size=14, color=BODY)
    d.foot(s, "A circuit that responds to how fast something changed, built out of two promoters and a repressor.")
    d.notes(s, "The rate result is the hook for the argue block, so land it "
               "here and do not explain it — question 3 next slide asks them to "
               "explain it.\n"
               "Numbers, if asked: pulses at AHL above 47 nM share the same "
               "initial slope and peak at about 45 min. The five-rate experiment "
               "(Fig. 3b,c) all reach 47-50 nM. On solid medium the positions "
               "are 2.5-4.5 mm from the senders and the farthest shows no "
               "observable response.")

    # 5 ARGUE -----------------------------------------------------------------
    s = d.dark()
    d.header(s, "14 – 24 min", "Argue it out  ·  groups of 3–4")
    d.title(s, "It pulses. Where, in the circuit, is the ‘off’?")
    d.text(s, "You have the three genes and Fig. 3. Point at the physical thing that ends the pulse.",
           M, 1.95, 11.6, 0.4, size=17, color=MINT)
    for i, q in enumerate([
            "Two paths run from AHL to GFP. Which one is fast and which is slow, and what physical step makes the slow one slow?",
            "Swap the two — make CI build faster than GFP. What does the output look like now? Is it still a pulse?",
            "A far-away cell sees AHL rise slowly. Fig. 3 says its pulse is smaller. Argue why a slow rise gives a smaller pulse, not just a later one."]):
        y = 2.75 + i * 1.15
        d.shape(s, S.OVAL, M, y + 0.05, 0.44, 0.44, fill=CYAN, line=None)
        d.text(s, str(i + 1), M, y + 0.13, 0.44, 0.3, size=15, bold=True,
               color=INK, align="c")
        d.text(s, q, M + 0.8, y, 11.2, 0.85, size=18, color=WHITE)
    d.foot(s, "Question 3 is the one that matters: the pulse ends when CI crosses a threshold, and a slow ramp lets CI keep pace with GFP the whole way up.")
    d.notes(s, "Analysis of a real artifact, not invention. Collect answers on "
               "the board BY GROUP; you name them again in ten minutes. Correct "
               "nothing yet.\n"
               "Q1: direct path AHL->GFP is fast; indirect AHL->CI->(repress GFP) "
               "is slow because CI has to be transcribed, translated, and build "
               "up past the operator threshold. That build time IS the delay.\n"
               "Q2: swap and GFP never gets ahead — no pulse, just a lower "
               "steady level. The pulse needs the output fast and the brake "
               "slow.\n"
               "Q3: on a slow ramp, at every instant AHL is lower, so GFP's "
               "drive is lower AND CI has had time to accumulate — it clamps GFP "
               "at a lower level. Rate, not just final value. That is how a cell "
               "reads distance from the sender.")

    # 6 SORTED ----------------------------------------------------------------
    s = d.light()
    d.header(s, "24 – 28 min", "Your answers, sorted")
    d.title(s, "What you just said, in one picture")
    d.image(s, FIG + "s10_pulse_generator.png", M, 1.85, 6.6, 3.0)
    for i, (k, txt, c) in enumerate([
            ("Two paths, one delayed",
             "AHL → GFP directly, and AHL → CI → GFP through a build-up. Every FFL is this.", TEAL),
            ("The delay is the second path's build time",
             "CI has to be made and cross its operator threshold. That is why the brake is late.", CYAN),
            ("Agree or fight decides the job",
             "Here the two paths fight — activate, then repress. That is an incoherent FFL, and fighting paths make a pulse.", AMBER),
            ("⚠ Rate sensing, and an honest gap",
             "Right: a slow ramp gives a SMALLER pulse, not just a later one — 1.21, 1.08, 0.78 as the rise stretches. But look how far it took: 500× in rate for a 35% drop, because our Y and Z share a lifetime. Basu’s GFP reports faster than CI accumulates, so his device separates distances our reduction barely resolves.", RED)]):
        y = 1.88 + i * 1.12
        d.shape(s, S.ROUNDED_RECTANGLE, 7.4, y, 0.16, 0.95, fill=c, line=None)
        d.text(s, k, 7.75, y, 5.0, 0.42, size=15, font=HEAD, bold=True, color=INK)
        d.text(s, txt, 7.75, y + 0.4, 5.0, 0.72, size=13, color=BODY)
    d.foot(s, "Our own simulation of the same circuit — the fast path and the slow brake are the two curves crossing. Dotted, on the right, is the input ramp itself.")
    d.notes(s, "Name real groups. This is the consolidation step and it is the "
               "fidelity condition for the generation phase. The figure is "
               "s10_pulse_generator.png, built from posb \u2014 GFP (fast) overshoots "
               "while CI (slow) is still rising.\n"
               "ROW 3 is the answer to the ten-minute argument and it has to "
               "land: a slow ramp gives a SMALLER pulse, because the brake has "
               "time to arrive before the output gets going. Point at the "
               "three dots.\n"
               "ROW 4 IS THE ONE TO SAY OUT LOUD, and it is uncomfortable on "
               "purpose. The rate sensitivity in our model is weak \u2014 12% "
               "across 0.2 to 10 lifetimes, and you need 500x in rate to get "
               "35%. Basu resolves 2.5 mm from 4.5 mm. Our reduction cannot, "
               "and the reason is that we gave Y and Z the same lifetime. His "
               "GFP is reported as fast as it is translated; his CI has to "
               "dimerize and find an operator first.\n"
               "This is the same lesson as the n = 2 wall on Thursday: the "
               "model answers WHETHER, and the size of the effect belongs to "
               "what you kept. Do not let them leave thinking the 11% is the "
               "biology.")

    # 7 THE MAP ---------------------------------------------------------------
    s = d.light()
    d.header(s, "28 – 30 min", "The whole family, in one line")
    d.title(s, "Three edges, each + or −, gives eight wirings")
    d.paper_figure(s, "mangan2003_coherent_table", M, 1.75, 5.85, 2.48,
                   "Mangan & Alon 2003, Table 1", "the four coherent types")
    d.paper_figure(s, "mangan2003_incoherent_table", 6.75, 1.75, 5.85, 2.90,
                   "Mangan & Alon 2003, Table 2", "the four incoherent types")
    d.text(s, "Coherent: the two paths agree in sign. Incoherent: they disagree. Type 1 of each is by far the most common in E. coli and yeast — and those are the two we build.",
           M, 5.45, W - 2 * M, 0.7, size=16, color=INK)
    d.assigned_on(M, 6.3, 8.0, s, prefix="You read Mangan & Alon for today")
    d.notes(s, "Thirty seconds on the counting: three edges, two signs each, "
               "eight types; split coherent/incoherent by whether the direct "
               "sign matches the product of the indirect two. Do not walk all "
               "eight — the tables are for reference and the reading covered "
               "them. Name the abundance fact: coherent-1 and incoherent-1 "
               "dominate, 28 and 5 in E. coli. Then build those two.")

    # 8 RUN — THE DELAY -------------------------------------------------------
    d.derivation_fig(
        "30 – 42 min", "Built one line at a time",
        "Where the delay comes from  (coherent type 1, AND)",
        [("X switches on; Y builds on its own timescale",
          "Y(t) = Y_{max}(1 - e^{-α_y t})",
          "the direct path to Z is fast; this slow one is the whole story"),
         ("Z needs both X and Y, so it waits for Y",
          "sharp gate:  Z waits until  Y(t) = K_{yz}",
          "AND logic. X is already high, but the gate needs Y as well — and ‘sharp’ is a lie we will collect on in a moment"),
         ("Solve the exponential for that instant",
          "t_{cross} = α_y^{-1} ln[Y_{max}/(Y_{max} − K_{yz})]",
          "solve Y_{max}(1 − e^{−α_y t}) = K_{yz} for t — rearrange, take the log, divide. The only algebra in the session"),
         ("Now compare it to one gene, fairly",
          "FFL: t_{½} = t_{cross} + ln2   one gene: t_{½} = ln2",
          "this is why the steady states must match: the same Z rise happens in BOTH, so it cancels"),
         ("Subtract, and only the wait survives",
          "t_D = t_{cross} ≈ ln 2 ≈ 0.69  at K_{yz} = ½",
          "measured off the curve: 0.75. The gap is the gate leaking — at H = 2 Z is already at 18% when Y crosses. Item 2 asks which way that pushes"),
         ("Turn X off and Z falls at once",
          "off step:  t_D = 0",
          "X is gone, so the gate shuts the instant X drops. The wait was only on the way up"),
         ("It acts on a steady signal, ignores a flicker",
          "short pulse of X  ⇒  Y never reaches K_{yz}",
          "Z reaches only 13% of its full response and decays — a persistence detector, and it filters ON, not OFF")],
        [FIG + "s10_c1_p1.png", FIG + "s10_c1_p2.png", None, FIG + "s10_c1_p3.png",
         FIG + "s10_c1_p3.png", FIG + "s10_c1_p4.png", FIG + "s10_c1_p5.png"],
        closing="Same steady state as one gene — but it makes you wait, and only on the way up.",
        board="t_{D} = ln[Y_{max}/(Y_{max}−K_{yz})] ≈ 0.69 lifetimes at K_{yz} = ½,  and t_{D} = 0 on the off-step",
        note=("SEVEN steps, deliberately, because this is the session\u2019s only "
              "derivation and the room has no common background. One knob at a "
              "time, and do not skip 3 or 4 to save time \u2014 skip step 7 "
              "instead if you must.\n"
              "Step 1: only the slow arm matters. Say the direct arm is fast "
              "and set it aside.\n"
              "Step 2 is the AND gate doing the work: Z is held off not because "
              "it is slow but because its gate is not satisfied until Y "
              "arrives. SAY THE WORD PRETEND out loud. A student watching the "
              "panel can see Z is already climbing when the dotted line is "
              "drawn, and if you assert \u2018Z stays off\u2019 flatly you lose them. "
              "Promise to collect on it in three steps.\n"
              "Step 3 IS THE ALGEBRA and it goes on the board, not just the "
              "screen. Solve Y_max(1 - e^{-t}) = K_yz for t. Rearrange, take "
              "the log, divide by alpha_y. Ask the room to do the rearranging; "
              "it is the one piece of calculus-free algebra everyone here can "
              "do, and doing it is what makes the formula theirs.\n"
              "Step 4 is the fairness step and it is the one people skip. "
              "t_cross is the time the GATE opens; t_D is a difference of "
              "HALF-TIMES. Those are different quantities. They are equal only "
              "because we matched beta_z so that Z\u2019s rise after the gate "
              "opens is the same curve in both designs \u2014 so it appears in "
              "both half-times and subtracts away. Point at the board "
              "convention while you say it.\n"
              "Step 5 is the collection. ln 2 = 0.693, measured 0.754. The gap "
              "is NOT numerical error: at H = 2 the gate leaks, and Z has "
              "reached 18% of its final value at the instant Y crosses K_yz. "
              "Do not resolve which direction that pushes in general \u2014 that "
              "is handout item 2 and PS5 Q2c, and the answer is that it pushes "
              "BOTH ways depending on K_yz.\n"
              "Step 6 is sign sensitivity, and it is the whole reason the "
              "circuit is interesting: the two curves lie on top of each other "
              "going down. The delay has a direction.\n"
              "Step 7: a pulse of X too short to build Y is rejected. Z gets to "
              "13% of full and decays \u2014 quote the number, because \u2018never "
              "fires\u2019 is visibly false on the panel. Persistence detection, "
              "and it is the engineering use.\n"
              "LEDGER: t_D and the convention."))

    # 9 THE INCOHERENT ONE — ADAPTATION --------------------------------------
    s = d.light()
    d.header(s, "42 – 45 min", "The other one  ·  fighting paths")
    d.title(s, "Incoherent type 1: overshoot, then adapt")
    d.image(s, FIG + "s10_iffl_adaptation.png", M, 1.80, 6.2, 4.4)
    d.text(s, "X turns on Z fast, and turns on Z's repressor slowly.",
           7.1, 1.9, 5.5, 0.4, size=17, font=HEAD, bold=True, color=INK)
    for i, (k, txt) in enumerate([
            ("The output runs first", "Z is driven directly by X, and Y is not there yet. Z overshoots."),
            ("The brake arrives", "Y builds, represses Z, and pulls it back down while X is still on."),
            ("It settles above zero", "Y represses by a factor, not absolutely — so Z lands on a new, lower plateau.")]):
        y = 2.5 + i * 1.15
        d.text(s, k, 7.1, y, 5.5, 0.4, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, txt, 7.1, y + 0.38, 5.5, 0.75, size=14, color=BODY)
    d.text(s, "Same wiring as Basu's — the only difference is that Y has a basal level here, so the brake never fully lets go.",
           M, 6.35, W - 2 * M, 0.4, size=15, color=BODY)
    d.notes(s, "The mechanism surface. The NUMBER is the next one — do not do "
               "both here. The distinction from Basu: with no basal Y the pulse "
               "is strong and returns near zero; with basal Y it lands on a "
               "plateau and the circuit is an accelerator rather than a pulser. "
               "Mangan's Table 2 calls those the two regimes of the same type.")

    # 9b THE NUMBER -----------------------------------------------------------
    s = d.light()
    d.header(s, "45 – 48 min", "The number a designer quotes")
    d.title(s, "Adaptation error = final ÷ peak")
    for i, (k, v, txt, c) in enumerate([
            ("peak", "1.10", "the highest value Z reaches, read off the trajectory", AMBER),
            ("final", "0.68", "where Z settles with X still on", RED),
            ("adaptation error", "0.62", "final ÷ peak — how much of the step it failed to forget", TEAL)]):
        y = 2.0 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 3.4, 0.95, fill=CARD, line=c, lw=2)
        d.text(s, k, M + 0.15, y + 0.1, 3.1, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, v, M + 0.15, y + 0.5, 3.1, 0.4, size=20, font=HEAD, bold=True,
               color=c)
        d.text(s, txt, M + 3.8, y + 0.22, 8.2, 0.7, size=15, color=BODY)
    d.text(s, "Near 0: the circuit forgets the step almost completely and reports only change. Near 1: it barely pulsed, and reports level.",
           M, 5.6, W - 2 * M, 0.5, size=16, bold=True, color=INK)
    d.foot(s, "Both numbers are measured off the curve, not solved for. That is the PS5 item, and it is how you will report any adaptation.")
    d.notes(s, "This is T26 and it is AUTO-graded, so the definition has to be "
               "exact and stated: adaptation error = final/peak, both read off "
               "the trajectory numerically "
               "(figures/s10_feedforward.py::iffl_numbers).\n"
               "Do NOT hand them a formula to plug into — the point of the "
               "problem is that they simulate and measure, the way session 5 "
               "measured a response time.\n"
               "Perfect adaptation (error -> 0) is what bacterial chemotaxis "
               "does; that is session 22's target, and worth naming in one line "
               "so the word is not new in November.\n"
               "LEDGER: adaptation error, beside t_D.")

    # 10 THE TWO JOBS, THE WHOLE TABLE ---------------------------------------
    s = d.light()
    d.header(s, "48 – 52 min", "Coherent vs incoherent, in one table")
    d.title(s, "Same object, opposite job")
    rows = [
        ("", "COHERENT type 1", "INCOHERENT type 1"),
        ("paths", "agree: activate, activate", "fight: activate, then repress"),
        ("ON step", "delayed rise (persistence filter)", "overshoot then adapt (a pulse)"),
        ("OFF step", "immediate — sign-sensitive", "immediate — sign-sensitive"),
        ("speed", "\u2014 (it is a delay, by construction)", "6.3\u00d7 faster to the same steady state"),
        ("the job", "reject a flicker, act on a steady signal", "respond to a change, not a level"),
        ("who has it", "CRP, RpoN in E. coli sugar/N systems", "Basu's pulse generator; the gal system in E. coli (CRP → GalS ⊣ galETK)")]
    ws = [2.0, 5.2, 5.3]
    for r, row in enumerate(rows):
        y = 1.86 + r * 0.63
        head = r == 0
        if head:
            d.shape(s, S.RECTANGLE, M, y, sum(ws), 0.6, fill=TEAL, line=None)
        for c_, (cell, wcol) in enumerate(zip(row, ws)):
            xx = M + sum(ws[:c_])
            d.text(s, cell, xx + 0.15, y + (0.14 if head else 0.06), wcol - 0.3, 0.6,
                   size=15 if head else 14,
                   bold=head or c_ == 0,
                   color=WHITE if head else (INK if c_ == 0 else BODY))
    d.text(s, "OR logic at the Z promoter flips the sign sensitivity — delay on the OFF step instead of the ON. Same machine, mirror image.   \u00b7   And read Table 2\u2019s pulse row: type 1 with AND is marked WEAK; the strong pulsers are types 3 and 4. Basu got a tall pulse from a type 1 by driving the Z promoter hard \u2014 pulse height is a parameter, the sign structure is not.",
           M, 6.28, W - 2 * M, 0.62, size=13.5, italic=True, color=MUTED)
    d.notes(s, "This is the T24 classification row, stated as a rule they can "
               "apply: read the three signs, compute coherent/incoherent, and "
               "the job follows. The OR-gate line is one sentence — Mangan's "
               "Table 3 — not a derivation; it is on the handout as a check "
               "item, not lectured.")

    # 10b RESPONSE ACCELERATION -----------------------------------------------
    s = d.light()
    d.header(s, "52 \u2013 58 min", "Design  \u00b7  which of these can you turn?")
    d.title(s, "The same circuit is also six times faster")
    d.image(s, FIG + "s10_iffl_acceleration.png", M, 1.78, 6.35, 4.23)
    for i, (k, txt, c) in enumerate([
            ("The comparison is matched",
             "Same input, same final Z \u2014 \u03b2_z on the one-gene design is set so both land in the same place. The only difference is the repressor arm.",
             TEAL),
            ("0.11 against 0.69 lifetimes",
             "Half-way to steady state 6.3\u00d7 sooner. And it is the SAME circuit, the same parameters, whose adaptation error you measured four minutes ago.",
             TEAL),
            ("Why it is faster",
             "Z is driven at full strength at the start, because Y has not arrived yet. The brake lands only once Z is most of the way up. You overshoot on purpose, then settle back.",
             AMBER),
            ("What it buys you",
             "Simple regulation has ONE response time: ln2/\u03b1, about 0.7 lifetimes, whatever \u03b2 is. The only way to speed it up is to shorten the lifetime \u2014 and that costs you the steady state. The FFL buys speed without touching either.",
             GREEN),
            ("And it was measured",
             "Alon 2007, Fig. 4c: the gal system in E. coli responds about threefold faster than lac, which is simple regulation on the same kind of signal.",
             GREEN)]):
        y = 1.82 + i * 0.94
        d.shape(s, S.ROUNDED_RECTANGLE, 7.35, y, 0.14, 0.86, fill=c, line=None)
        d.text(s, k, 7.65, y, 4.95, 0.4, size=14.5, font=HEAD, bold=True, color=INK)
        d.text(s, txt, 7.65, y + 0.38, 4.95, 0.56, size=13, color=BODY)
    d.foot(s, "One wiring, three jobs: it pulses, it adapts, and it accelerates. Mangan & Alon call the incoherent family sign-sensitive ACCELERATORS \u2014 the mirror of the coherent family\u2019s delay.")
    d.notes(s, "This closes the goals slide\u2019s third question, and it is graded "
               "on PS5, so it has to be DEMONSTRATED here and not just "
               "mentioned.\n"
               "WALK THE FIGURE, slowly, because it is the one place a "
               "biologist and a physicist read the same picture and take away "
               "different things. Grey is one gene driven by X. Teal is the "
               "FFL. The dotted line is the steady state they share BY "
               "CONSTRUCTION \u2014 say that twice, because the comparison is "
               "worthless otherwise, and it is the same matching rule that "
               "made t_D well defined this morning.\n"
               "THE MECHANISM in one sentence, and let them supply it: why is "
               "the FFL off the line so fast? Because for the first fraction "
               "of a lifetime the repressor simply is not there yet. The "
               "circuit is running open-loop, at full beta_z, and beta_z here "
               "is 6.\n"
               "THE UNITS TRAP, and say it out loud because they have the "
               "paper in front of them: we call 1/alpha the lifetime, so "
               "simple regulation takes 0.69 lifetimes to reach half. Mangan "
               "and Alon call ln2/alpha the lifetime, so the SAME fact reads "
               "as \u2018a response time of one lifetime\u2019 in their paper. Same "
               "circuit, same physics, two conventions. Point at the axis.\n"
               "THE HONEST CAVEAT if someone raises it: this acceleration "
               "needs a BASAL level of Y, which this circuit has (B_y = 0.4). "
               "Basu\u2019s pulse generator has none, and it pulses instead. Same "
               "wiring, one parameter apart \u2014 Mangan\u2019s Table 3 splits the "
               "family on exactly that.")

    # 11 ENGINEERABILITY ------------------------------------------------------
    s = d.light()
    d.header(s, "52 – 58 min", "Design  ·  which of these can you turn?")
    d.title(s, "What sets the timing, and what you can change")
    for i, (p, verd, txt, c) in enumerate([
            ("Y's lifetime", "MODERATE", "sets how fast the delayed arm builds — an ssrA tag on Y shortens the delay and the pulse together.", AMBER),
            ("K_yz", "EASY", "the operator/RBS on the Y→Z arm. Raise it and Y must build higher, so the delay grows. The knob Basu turned.", GREEN),
            ("β_z vs the repression", "EASY", "how hard the output runs before the brake — a stronger GFP RBS raises the peak and worsens the adaptation error.", GREEN),
            ("the three signs", "HARD", "the wiring itself. Changing a sign means swapping an activator for a repressor — a different protein, a different job.", RED)]):
        y = 1.9 + i * 1.08
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 2.5, 0.9, fill=CARD, line=c, lw=2)
        d.text(s, p, M, y + 0.12, 2.5, 0.4, size=16, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, verd, M, y + 0.54, 2.5, 0.32, size=14, bold=True, color=c, align="c")
        d.text(s, txt, M + 2.8, y + 0.05, 9.1, 0.9, size=14.5, color=BODY)
    d.text(s, "Basu built a library of pulse circuits by swapping exactly two things — the CI RBS and the operator affinity. Those are K_yz and the repression strength above.",
           M, 6.35, W - 2 * M, 0.5, size=15, bold=True, color=INK)
    d.notes(s, "THE slide that separates this from a math course. Basu Fig. 2 is "
               "a contour of pulse gain over CI-RBS strength and operator "
               "affinity — a two-knob design sweep. Those two knobs are exactly "
               "K_yz and the repression factor here. Tie it back: the same RBS "
               "move that walked the toggle into its wedge last Thursday tunes "
               "the pulse here.")

    # 12 CONCEPTEST -----------------------------------------------------------
    s = d.light()
    d.header(s, "58 – 63 min", "Pose  ·  silent vote  ·  argue  ·  vote again")
    d.title(s, "You want the pulse taller and to peak later")
    for i, (letter, opt) in enumerate([
            ("A", "Strengthen the GFP RBS and weaken the CI RBS"),
            ("B", "Strengthen both RBSs equally"),
            ("C", "Add ssrA tags to both GFP and CI"),
            ("D", "Raise the AHL concentration")]):
        y = 2.2 + i * 0.95
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, W - 2 * M, 0.75, fill=CARD, line=RULE, lw=1)
        d.text(s, letter, M + 0.25, y + 0.2, 0.5, 0.4, size=20, font=HEAD,
               bold=True, color=CYAN)
        d.text(s, opt, M + 0.9, y + 0.22, W - 2 * M - 1.2, 0.4, size=16, color=BODY)
    d.foot(s, "Taller means the output runs further before the brake. Later means the brake arrives later. Which knob does each?")
    d.notes(s, "Answer: A, and every number below is measured on the "
               "Basu-parameter circuit (K_yz = 0.15, beta_z = 8), baseline "
               "peak 1.22 at t = 0.44, adaptation error 0.15.\n"
               "A: stronger GFP RBS AND weaker CI RBS \u2014 output faster, brake "
               "later. Peak 4.19 at t = 0.70. Uniquely taller AND later.\n"
               "B raises both, so the brake keeps pace: peak 1.36 but EARLIER, "
               "t = 0.29. And be careful here \u2014 the adaptation error does not "
               "stay put, it IMPROVES, 0.15 to 0.07. Taller is not the same as "
               "slower, and a better-adapting circuit is not the one asked "
               "for.\n"
               "C speeds removal of both: peak 0.94, earlier, error 0.48. The "
               "opposite on every count. Worth knowing before you pose it: "
               "Basu\u2019s CI and GFP ALREADY carry LVA ssrA tags, so C is really "
               "\u2018tag them harder\u2019. Say so if someone asks what is left to "
               "tag.\n"
               "D saturates: peak 1.22, unchanged to within 0.2%. That is "
               "Basu\u2019s own observation \u2014 above about 47 nM the pulses have "
               "the same rising slope and about the same maximum.\n"
               "FOLLOW-UP worth drawing out: A also worsens the adaptation "
               "error, 0.15 to 0.32. Taller pulse, less complete forgetting. "
               "There is a trade, and it is the same trade the engineerability "
               "slide named.")

    # 13 FADED WORKED SET -----------------------------------------------------
    s = d.light()
    d.header(s, "63 – 71 min", "Worked set  ·  handout  ·  start where you like")
    d.title(s, "Four problems. The scaffolding falls away.")
    for i, (num, k, txt, c) in enumerate([
            ("1", "Fully worked", "classify three FFLs by the sign rule", TEAL),
            ("2", "Last step blank", "fill the delay table, convention stated", GREEN),
            ("3", "Three blanks", "peak, final, adaptation error — all measured", CYAN),
            ("4", "Bare problem", "pick a wiring for a stated job", AMBER)]):
        x = M + i * 3.05
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.1, 2.8, 2.5, fill=CARD, line=c, lw=2)
        d.shape(s, S.OVAL, x + 1.15, 2.35, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 1.15, 2.46, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 0.15, 3.05, 2.5, 0.4, size=16, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, txt, x + 0.15, 3.48, 2.5, 0.95, size=14, color=MUTED, align="c")
    d.text(s, "Start wherever the scaffolding stops helping you. Nobody needs to announce where that is.",
           M, 4.95, W - 2 * M, 0.4, size=18, bold=True, color=INK)
    d.text(s, "The delay table asks you to state your convention before you fill it. That is not bookkeeping — it is what makes two people's tables comparable.",
           M, 5.45, W - 2 * M, 0.5, size=15, color=BODY)
    d.notes(s, "Six minutes, then take the numbers, then the second half. "
               "Circulate. Do NOT work item 1 at the board — that collapses the "
               "fading. Item 2's convention line is the T25 spec; a table with "
               "no convention is not gradeable, and PS5 docks it. You are also "
               "scouting which of the two standard stalls (next surface) you "
               "actually see.")

    # 13b MID-SET -------------------------------------------------------------
    s = d.dark()
    d.header(s, "71 – 73 min", "Two minutes at the front  ·  then back to it")
    d.title(s, "The two places people stall")
    for i, (k, txt) in enumerate([
            ("A delay needs two curves, not one",
             "You cannot report a delay from the FFL alone. Draw the one-gene design with the SAME final level beside it, and measure the gap at half-max. No comparison, no number."),
            ("‘Adaptation error’ is final over peak, both measured",
             "There is no formula to plug into. Simulate, find the highest point, find where it settles, divide. If you are solving for it algebraically you are answering a different question.")]):
        y = 2.3 + i * 1.7
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.45, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.4, 0.85, size=16, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.2, y + 0.02, 7.3, 1.5, size=14, color=MINT)
    d.text(s, "Four more minutes. Reach item 4 — the design one.",
           M, 5.85, 12.5, 0.5, size=18, font=HEAD, bold=True, color=CYAN)
    d.notes(s, "Two minutes, say the two things, take no questions, send them "
               "back. Both are about HOW to proceed and give away no answer — "
               "the line that keeps the fading intact.")

    # 13c SECOND HALF ---------------------------------------------------------
    s = d.light()
    d.header(s, "73 – 78 min", "Worked set  ·  four more minutes  ·  reach item 4")
    d.title(s, "Design one: match the wiring to the job")
    for i, (num, k, txt, c) in enumerate([
            ("3", "Three blanks", "peak, final, adaptation error — all measured", CYAN),
            ("4", "Bare problem", "you need a circuit that fires only if a signal lasts over an hour. Which FFL, which gate, which sign?", AMBER)]):
        x = M + i * 6.35
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.05, 6.15, 2.0, fill=CARD, line=c, lw=2)
        d.shape(s, S.OVAL, x + 0.3, 2.3, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 0.3, 2.41, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 1.0, 2.35, 4.9, 0.4, size=16, font=HEAD, bold=True, color=INK)
        d.text(s, txt, x + 1.0, 2.8, 4.9, 1.0, size=14, color=MUTED)
    d.text(s, "Item 4 is the session run backwards: not ‘what does this circuit do’ but ‘what circuit does this’. You have the sign rule, Mangan’s two tables, and one derived delay. Which of the eight can hold off an ON step and still let go instantly — and is there more than one?",
           M, 4.35, W - 2 * M, 0.7, size=16, bold=True, color=INK)
    d.foot(s, "Nobody is expected to finish item 4 here. What is expected is that you can name the type and the gate before I show the answer.")
    d.notes(s, "Four minutes, stop at 78. Item 4 closes the loop: the delay "
               "derivation was a persistence filter all along. If someone has "
               "it, have them say the argument — the delay on the ON step is "
               "exactly the ‘must last longer than t_D’ condition.")

    # 14 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "78 – 80 min", "Next")
    d.title(s, "A toggle holds. An FFL times one event. What keeps time?")
    d.text(s, "Thursday: three repressors in a ring.",
           M, 2.05, 11, 0.45, size=23, font=HEAD, bold=True, color=MINT)
    d.text(s, "The toggle was two genes repressing each other, and it had two stable states.\n\nPut three repressors in a ring, each shutting off the next, and there is no state the system can rest in — chase the logic around the loop and it never closes.",
           M, 2.72, 11.3, 1.6, size=16, color=WHITE, spacing=1.4)
    d.text(s, "So what does it do instead, and what decides whether it keeps time or merely wobbles? Session 11.",
           M, 4.52, 11.3, 0.34, size=14, italic=True, color=CYAN)
    d.assignment(s, y=5.12)
    d.notes(s, "Pose it as the next constraint, not a summary. The reading for "
               "Thursday (Potvin-Trottier 2016) goes out now — it is the "
               "repressilator with its noise sources removed one at a time, so "
               "it is an argument about which term destroys the period. PS5 "
               "posts Thursday and covers both of this week's sessions.")

    return d
