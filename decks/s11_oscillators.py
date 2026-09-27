"""Session 11 — Oscillators: the repressilator and the condition for a clock.

Thursday 1 October. The toggle held a state; the feedforward loop timed one
event. This one runs forever, and the session exists to produce the condition
that separates a clock from a circuit that merely wobbles -- which
docs/design-notes.md records as never having been stated at all in prior years.

Artifact first, same shape as sessions 9 and 10: Elowitz & Leibler's
repressilator is the thing on the table, the room argues about why a ring of
three cannot settle, and only then does the algebra arrive. The assigned
reading (Potvin-Trottier 2016) is the other half -- the deterministic criterion
says WHETHER it ticks, and the reading is about how badly it keeps time and
what fixes that.

The result, derived in class and verified in tests/test_analysis.py:

    J = -I - gP at the symmetric fixed point, so the eigenvalues are
    -1 - g*omega_k over the cube roots of unity. The complex pair has real
    part -1 + g/2, so the state loses stability exactly when **g = 2**, giving

        alpha_c = (2/(n-2))^(1/n) * n/(n-2),   infinite for n <= 2

    and at onset the frequency is sqrt(3), i.e. a period of 2*pi/sqrt(3)
    ~ 3.63 protein lifetimes.

Coverage: T27 (construct the model), T28 (state and apply the criterion),
T29 (locate the Hopf boundary numerically by sweep), T30 (delay as a driver).
All four are assessed on PS5.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks import theme as T
from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session11_Oscillators"
FIG = "figures/build/"


def build():
    d = Deck("Session 11 — Oscillators", session=11)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 11", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Oscillators", M, 2.72, 9.0, 1.3,
           size=42, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Three repressors in a ring, and the one number that decides whether it keeps time",
           M, 4.15, 9.6, 0.8, size=18, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Two sessions of circuits that do something once. This one runs "
               "forever — or fails to, and the difference is a single "
               "inequality.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions before we start")
    for i, (src, q, c) in enumerate([
            ("From Tuesday", "Coherent or incoherent — and how do you tell from the three signs?", TEAL),
            ("From Tuesday", "Why does a coherent type-1 FFL reject a short pulse of input?", TEAL),
            ("From session 9", "The toggle needed cooperativity on at least one arm. What went wrong at n = 1?", CYAN)]):
        y = 2.15 + i * 1.25
        d.shape(s, S.OVAL, M, y, 0.42, 0.42, fill=c, line=None)
        d.text(s, str(i + 1), M, y + 0.08, 0.42, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, src.upper(), M + 0.75, y - 0.02, 3.4, 0.28, size=14,
               bold=True, color=MUTED)
        d.text(s, q, M + 0.75, y + 0.26, W - 2 * M - 0.75, 0.6, size=17, color=BODY)
    d.foot(s, "Question 3 is the one today rhymes with: a cooperativity threshold, derived the same way, with a different number.")
    d.notes(s, "Q1: direct sign vs the product of the indirect two. Q2: the AND "
               "gate waits for Y to build, and a short pulse never gets Y there. "
               "Q3: with n = 1 the nullclines cross once however large alpha is "
               "— alpha_c is infinite. Today's answer is the same shape with "
               "n = 2 as the wall instead of n = 1.")

    # 3 GOALS -----------------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By 9:30 you should be able to answer")
    for i, (n, lab) in enumerate([("9", "Bistability"), ("10", "Feedforward"),
                                  ("11", "Oscillation"), ("12", "Noise"),
                                  ("13", "Digital")]):
        x, here = M + i * 2.42, n == "11"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=14, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "Two mutually repressing genes gave two stable states. Why should three in a ring give none at all?",
            "Given a ring, what exactly do you have to check to know whether it will oscillate — and what would you build to make it stop?",
            "The first repressilator kept terrible time. What was destroying the period, and which of the fixes mattered?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "The third goal is the reading, and it is a different kind of "
               "question from the first two — deterministic theory answers "
               "whether it ticks, and has nothing to say about how well. Flag "
               "that now so the last segment does not feel like a change of "
               "subject.")

    # 4 THE ARTIFACT ----------------------------------------------------------
    s = d.light()
    d.header(s, "8 – 13 min", "The artifact")
    d.title(s, "Elowitz & Leibler, Nature 2000 — the repressilator")
    d.rows(s, [
        ("The ring", "Three genes on one plasmid: LacI represses TetR, TetR represses cI, cI represses LacI."),
        ("The reporter", "GFP on a second plasmid. The clock is watched, not measured."),
        ("What it did", "It oscillated — period about 150 min, longer than the cell cycle."),
        ("And badly", "Amplitude and period varied wildly between cells, and peak to peak in one cell.")],
        top=2.00, bottom=6.26, label_w=1.85, right=7.25)
    d.paper_figure(s, "elowitz2000_fig1", 7.90, 1.70, 3.50, 2.10,
                   "Elowitz & Leibler 2000, Fig. 1", "the ring, and the reporter")
    d.paper_figure(s, "elowitz2000_fig2", 8.75, 4.20, 2.15, 1.76,
                   "Elowitz & Leibler 2000, Fig. 2", "single-cell traces")
    d.foot(s, "Their own design rules: strong promoters and efficient RBSs, tight and cooperative repression, comparable protein and mRNA decay. Two of those are α and n; the other two we throw away.")
    d.notes(s, "Same issue of Nature as Gardner's toggle, 20 January 2000 — "
               "worth saying, because it dates the field's founding moment "
               "to a single week.\n"
               "The foot line is THEIR list of what favours oscillation, from "
               "the paper's second paragraph: strong promoters and efficient "
               "RBSs is alpha, cooperative repression is n, low leakiness is "
               "the basal term we dropped. The derivation they are about to "
               "see is why that list reads the way it does.\n"
               "They tagged all three repressors with ssrA to bring protein "
               "lifetimes near the mRNA lifetime. Hold that for the "
               "ConcepTest.\n"
               "This paper is NOT assigned: it is paywalled with no deposit, so "
               "it lives on the slide as the construct. The assigned reading is "
               "Potvin-Trottier, which is about fixing exactly the defect in "
               "the fourth row.")

    # 4b HOW YOU WATCH IT ----------------------------------------------------
    s = d.light()
    d.header(s, "8 – 13 min", "The artifact  ·  and how it was watched")
    d.title(s, "Before you believe a clock, ask how it was watched")
    d.rows(s, [
        ("A flask average is flat", "Every cell ticks, no two in phase. Average over a culture and the oscillation cancels — a straight line from a population of clocks. Every repressilator result is a single-cell result.", TEAL),
        ("Hence time-lapse microscopy", "Elowitz followed single cells on agar and measured peak-to-peak by hand: 160 ± 40 min, n = 63. A few generations was all that platform held.", TEAL),
        ("You are watching a proxy", "GFP on a separate plasmid, driven by one of the three promoters. Between the repressor and the number you plot sit transcription, translation, folding and dilution.", AMBER),
        ("⚠ The platform was the limit", "Run the same circuit in a microfluidic device holding cells for hundreds of generations and EVERY cell oscillates. ‘Only 40%’ was partly a claim about the microscopes of 2000.", RED)],
        top=1.96, bottom=6.42, label_w=2.90)
    d.foot(s, "You cannot debug a clock you cannot watch for long enough. Today’s reading is the group that went back and watched properly.")
    d.notes(s, "Five minutes, and it is the measurement half of the artifact. "
               "Two of the four rows are for the engineers and two for the "
               "biologists, so nobody is bored for the whole slide.\n"
               "ROW 1 is the one to draw in the air: three sine waves at "
               "random phase, and their sum. Ask the room what the average "
               "looks like before you say it. Physics and engineering "
               "students get this instantly; it is worth having them say it "
               "out loud so the biologists hear it from a peer.\n"
               "ROW 3 matters because the whole course keeps conflating the "
               "reporter with the thing reported. Name the chain out loud.\n"
               "ROW 4 is a correction to what we said one slide ago and it "
               "should be said as one. Potvin-Trottier 2016 re-ran the "
               "ORIGINAL circuit in a mother machine and saw clear "
               "oscillations in all cells — their words are that some of the "
               "erratic behavior originally reported was due to the limited "
               "imaging platforms available at the time. That does NOT mean "
               "the irregularity was fake: the remaining irregularity was "
               "real and they tracked down its cause, which is the 54-minute "
               "segment. It means the first number was a claim about an "
               "instrument as much as about a circuit. Do not resolve the "
               "tension here — leave it, and let the reading resolve it.")

    # 5 ARGUE -----------------------------------------------------------------
    s = d.dark()
    d.header(s, "13 – 23 min", "Argue it out  ·  groups of 3–4")
    d.title(s, "Why can a ring of three not just settle down?")
    d.text(s, "You have the toggle from session 9 and this ring. Use the same tools.",
           M, 1.95, 11.6, 0.4, size=17, color=MINT)
    d.rows(s, [
        ("Chase the logic around the loop. Start with LacI high and follow it once around — what comes back to LacI, and why does that not close?", None),
        ("The toggle has two genes and two stable states. Argue what an odd number of repressors does that an even number does not.", None),
        ("Suppose it does settle — every gene at the same middling level. What would have to be true of the repression for that state to hold?", None)],
        top=2.62, bottom=6.40, side=False, numbered=True,
        label_role="emphasis", label_color=WHITE)
    d.foot(s, "Question 3 is the one the algebra answers: a symmetric state always EXISTS. The question is whether the cell can stay in it.")
    d.notes(s, "Collect by group; you name them again in five minutes.\n"
               "Q1: LacI high -> TetR low -> cI high -> LacI low. Contradiction, "
               "so no state with LacI definitely high can persist. Odd loops "
               "cannot be consistently colored.\n"
               "Q2: an even ring of repressors is a toggle generalization — it "
               "CAN be consistently colored (alternate high/low), so it has "
               "stable states. Odd cannot. This is the sign of the loop: an odd "
               "number of inversions is net negative feedback.\n"
               "Q3: the key move, and the bridge to the derivation. The "
               "symmetric state always exists — a middling level that is "
               "self-consistent. Whether the cell STAYS there is a stability "
               "question, and stability questions are Jacobians. That is the "
               "whole session in one sentence; do not say it for them if a "
               "group is close.")

    # 6 SORTED ----------------------------------------------------------------
    s = d.light()
    d.header(s, "23 – 27 min", "Your answers, sorted")
    d.title(s, "Existence is not the question. Stability is.")
    d.image(s, FIG + "s11_ring_dynamics.png", M, 1.9, 7.6, 3.1)
    d.rows(s, [
        ("Odd loop, net negative",
         "Three inversions compose to one. An odd ring cannot be consistently high-and-low.", TEAL),
        ("But a middle state exists",
         "All three at the same middling level solves the equations, for every α and n.", CYAN),
        ("So: does it hold?",
         "Same circuit, two promoter strengths, two different fates. Nothing else differs.", AMBER)],
        top=1.86, bottom=6.42, side=False, pad=0.02, left=8.50, right=12.63,
        label_color=INK)
    d.foot(s, "Left: α below the threshold. Right: α above it. The threshold is what the next ten minutes produces.")
    d.notes(s, "The consolidation step. The figure does the work: identical "
               "circuits, one number changed, and the qualitative behavior "
               "flips. That is a bifurcation and they have seen one before — "
               "session 9's saddle-node. This one is different in kind, and the "
               "difference is that a PAIR of eigenvalues crosses, not one.")

    # 6b THE MODEL, WRITTEN DOWN ---------------------------------------------
    s = d.light()
    d.header(s, "23 – 27 min", "The model  ·  T27")
    d.title(s, "Three genes, one equation, written three times")
    d.text(s, "x_{i} is the concentration of repressor i, in units of the threshold that half-represses the next promoter. Time is in protein lifetimes.",
           M, 1.58, W - 2 * M, 0.5, size=15, color=BODY)
    # One equation per line. Side by side they ran to 95 rendered characters,
    # which is two lines in a 11.9in box at 24pt -- and the wrap fell in the
    # middle of the second gene's equation, which is the one place a reader
    # from biology is counting indices.
    d.text(s, "dx_{1}/dt = α/(1 + x_{3}^{n}) − x_{1}\n"
              "dx_{2}/dt = α/(1 + x_{1}^{n}) − x_{2}\n"
              "dx_{3}/dt = α/(1 + x_{2}^{n}) − x_{3}",
           M + 0.30, 2.37, W - 2 * M, 1.21, size=19, font=HEAD, bold=True,
           color=INK, spacing=1.0)
    d.text(s, "The index wraps: gene 1 is repressed by gene 3 — that wrap is what makes it a ring.",
           M, 3.68, W - 2 * M, 0.34, size=14, italic=True, color=MUTED)
    d.rows(s, [
        ("α  is the only knob", "α = β/(γK): promoter and RBS strength β, removal rate γ, threshold K. One number carries all three — which is why a degradation tag moves α, as it did on the toggle.", TEAL),
        ("n  is the cooperativity", "How sharply the repressor shuts its promoter. You buy it by choosing a protein, not by turning a dial.", CYAN),
        ("What we threw away", "mRNA, and any basal leak. Both are real. We will find out on the last surface what dropping the mRNA step cost us.", AMBER)],
        top=4.10, bottom=6.70, label_w=3.30, bar=0.16)
    d.foot(s, "Everything for the next fifteen minutes comes out of these three lines and nothing else.")
    d.notes(s, "T27 — constructing the model — and until 26 September this "
               "session never put the equations on a projected surface at all. "
               "They were on the board wing and the handout only.\n"
               "Say the scaling out loud: alpha = beta/(gamma K). It is the "
               "line that makes the ConcepTest answerable and it is the line "
               "that connects a degradation tag to a position in the design "
               "space. Session 9 already made that move for the toggle.\n"
               "The index wrap is worth pointing at physically — chase 1 -> 3 "
               "-> 2 -> 1 on the drawing on the board.")

    # 7 RUN — THE CRITERION ---------------------------------------------------
    d.derivation_fig(
        "27 – 40 min", "Built one line at a time",
        "When can the middling state not hold?",
        [("Every gene at the same level solves it",
          "x = α/(1 + x^{n}) ,  so  α = x(1 + x^{n})",
          "one equation, one unknown, always exactly one positive root"),
         ("Differentiate one Hill term",
          "∂/∂x [ α/(1 + x^{n}) ] = -α n x^{n-1}/(1 + x^{n})^{2}",
          "the chain rule on one Hill term, and nothing else. The minus sign is the repression"),
         ("Put α = x(1 + x^{n}) back in — it collapses",
          "-α n x^{n-1}/(1+x^{n})^{2} = -n x^{n}/(1 + x^{n}) ≡ -g",
          "one power of (1+x^{n}) cancels and α disappears. g is a pure number now — the gain of one arm"),
         ("Assemble: -1 diagonal, -g one step behind",
          "J = -I - gP ,   P = the cyclic shift",
          "each gene feels its own removal, and exactly one other gene. That is the whole matrix"),
         ("(1, ω, ω^{2}) is an eigenvector of P",
          "P v = ω v   when   ω^{3} = 1",
          "shifting a list whose entries step by ω returns the same list times ω"),
         ("A shift of P shifts every eigenvalue",
          "λ_k = -1 - g ω_k ,  ω_k = 1, e^{±2πi/3}",
          "all three eigenvalues, with no 3×3 determinant anywhere"),
         ("The real one is safe; the pair is not",
          "Re λ = -1 + g/2   for the complex pair",
          "the -1 is removal, the +g/2 is feedback fighting it. Everything is in this line"),
         ("The state fails when the gain reaches two",
          "g = 2 ,  hence  α_c = (2/(n-2))^{1/n}·n/(n-2)",
          "infinite for n ≤ 2 — in THIS model. Hold that; the next surface but one tests it")],
        [FIG + "s11_crit_p1.png", None, None, None,
         FIG + "s11_crit_p2.png", None,
         FIG + "s11_crit_p3.png", FIG + "s11_crit_p4.png"],
        closing="A clock is a steady state that failed — by a complex pair crossing together.",
        board="g = n x^{n}/(1+x^{n}) = 2   at   α_{c} = (2/(n−2))^{1/n}·n/(n−2)",
        note=("THE derivation of the session, and the one design-notes says was "
              "never stated in prior years. Eight steps, deliberately — this "
              "was five until the review found the Jacobian was being asserted "
              "rather than derived, which is exactly the step this cohort needs "
              "shown.\n"
              "Step 1: the symmetric state always exists — the room's question "
              "3. x(1+x^n) is strictly increasing, so one root, always.\n"
              "Steps 2-3 are the new pair and they are the heart of it. Step 2 "
              "is a chain rule and nothing more; do it slowly and let the "
              "biologists write it down. Step 3 is the PAYOFF — where something "
              "disappears. Substituting alpha = x(1+x^n) cancels one power of "
              "(1+x^n) and kills alpha entirely, leaving a pure number. Say out "
              "loud that g no longer depends on alpha: the gain at the "
              "operating point is set by n and x alone.\n"
              "Step 4: assemble. The only structural fact is that each gene is "
              "repressed by exactly one other, which is what makes J a "
              "circulant — and circulants are why this is doable by hand.\n"
              "Step 5 is the roots-of-unity step and it is NOT optional to "
              "draw. Write v = (1, omega, omega^2) on the board and shift it by "
              "hand: the shift sends it to (omega^2, 1, omega) = omega^2 * v. "
              "Many in this room have never met a complex eigenvector.\n"
              "Step 6 is the spectral shift: if Pv = omega v then "
              "(-I - gP)v = (-1 - g*omega)v. One line, and it is the trick that "
              "replaces the characteristic polynomial.\n"
              "Step 7: take the real part of -1 - g(-1/2 + i sqrt3/2). The -1/2 "
              "flips sign and you get -1 + g/2.\n"
              "Step 8: g = 2, then solve for alpha. At n = 4, alpha_c is "
              "exactly 2 — the same coincidence the toggle had at n = 2. The "
              "comparison worth drawing: toggle needs n > 1, this ring needs "
              "n > 2, so adding a gene made the requirement HARDER.\n"
              "LEDGER: g = 2 and alpha_c.")

    )

    # 8 THE PERIOD ------------------------------------------------------------
    s = d.light()
    d.header(s, "40 – 44 min", "What else that line gave you")
    d.title(s, "The criterion also hands you the period")
    d.text(s, "At the boundary g = 2, so the complex pair is",
           M, 1.9, 7.0, 0.4, size=17, color=BODY)
    d.text(s, "λ = 0 ± i√3", M, 2.35, 7.0, 0.7, size=30, font=HEAD, bold=True,
           color=TEAL)
    d.text(s, "A pure imaginary pair is an oscillation with no growth and no decay. Its frequency is √3, so the period at onset is",
           M, 3.08, 7.0, 0.8, size=16, color=BODY)
    d.text(s, "T = 2π/√3 ≈ 3.63 protein lifetimes", M, 4.15, 7.4, 0.44,
           size=24, font=HEAD, bold=True, color=INK)
    d.rows(s, [
        ("Measured on our own model", "3.64 lifetimes just above the boundary — as predicted."),
        ("Away from onset it drifts", "at 3× α_c the period is 5.2; at 10×, 8.0. Only local."),
        ("Against the real device", "About 150 min, with effective lifetimes of tens of minutes. Same order — all a three-variable model earns."),
        ("And the SHAPE changes too", "near onset a sine; at 10× a slow build-up then a sharp collapse. The reading says the device is the second kind.")],
        top=4.66, bottom=6.95, label_w=3.90, gap=0.08)
    d.image(s, FIG + "s11_period.png", 7.9, 1.72, 4.6, 2.68)
    d.notes(s, "A short surface, and it is the one that makes the criterion "
               "feel like an instrument rather than a yes/no. Linearisation "
               "gives the frequency AT onset; it does not give the period far "
               "from it, and the numbers say by how much it is wrong. Be "
               "explicit that the 150-minute comparison is an order-of-magnitude "
               "check and not a fit — we have thrown away mRNA and delay.\n"
               "THE FIGURE: three traces, each with one peak-to-peak interval "
               "measured off the curve rather than asserted. Say the measured "
               "3.64 against the predicted 3.628 out loud — it is the only "
               "number in the session the linear theory predicted and the "
               "simulation then confirmed without being fitted to it.\n"
               "Point at the y-axes, not only the periods: peak-to-trough is "
               "0.3 at onset and about 28 at ten times alpha_c. That is the "
               "Hopf growing an amplitude out of nothing, which the previous "
               "surface claimed in words.\n"
               "THE SHAPE ROW is a deliberate hook into the reading. The "
               "bottom panel is a relaxation oscillator — build up, then "
               "collapse — and Potvin-Trottier's Box 1 argues that is what "
               "the real repressilator does, which is why their accuracy "
               "argument turns on how far a concentration has to fall rather "
               "than on cooperativity at all.")

    # 9 T29 — FIND IT NUMERICALLY --------------------------------------------
    s = d.light()
    d.header(s, "44 – 50 min", "The same boundary, without the algebra")
    d.title(s, "Sweep one parameter and watch the eigenvalue cross")
    d.image(s, FIG + "s11_sweep.png", M, 1.70, 8.0, 3.40)
    d.rows(s, [
        ("The procedure", "pick α, solve for x, build J, take max Re λ. Bisect."),
        ("What it found", "α_c = 3.7797631 either way, to one part in 10⁹."),
        ("Why you would ever", "the algebra needed symmetry. Sweeping does not, and real circuits are not.")],
        top=1.62, bottom=5.26, side=False, pad=0.02, left=8.85, right=12.63,
        label_color=INK)
    d.text(s, "Right: past the boundary the amplitude grows continuously out of zero — like √(α − α_c) near onset — rather than jumping. A circuit just past the boundary oscillates faintly.",
           M, 5.34, W - 2 * M, 0.5, size=15, color=BODY)
    d.foot(s, "posb.sweep, posb.leading_real_part, posb.hopf_boundary — and you write the loop yourself on PS5 before you import ours.")
    d.notes(s, "T29, and it is the new public surface in posb this week. The "
               "rule holds: they write the sweep on the problem set, and the "
               "library version is for afterwards.\n"
               "The contrast with session 9 is worth one sentence: the toggle's "
               "saddle-node ANNIHILATED a state and the cell jumped. Here "
               "nothing is annihilated — a state goes gently unstable and a "
               "small cycle grows out of it. Different bifurcation, different "
               "engineering consequence: near a Hopf you get a small, fragile "
               "oscillation, which is exactly what Elowitz saw.")

    # 9b THE SWEEP, STEP BY STEP ---------------------------------------------
    s = d.light()
    d.header(s, "44 – 50 min", "The same boundary, without the algebra")
    d.title(s, "The sweep, one step at a time — this is PS5 Q5a")
    d.rows(s, [
        ("Fix n. Pick one α.", "One point in design space. Everything below answers one yes/no question: is the symmetric state stable?"),
        ("Find the fixed point.", "Solve  x = α/(1 + x^{n}).  The right side falls as x rises, so there is exactly one root. Bracket on [0, α]."),
        ("Build the Jacobian.", "g = n x^{n}/(1 + x^{n}), then J = -I - gP. Or finite-difference it — that one survives asymmetry."),
        ("Largest REAL part", "max Re λ over the three eigenvalues. NOT the largest magnitude — confusing the two is the commonest error here."),
        ("Repeat, then bisect.", "Negative at small α, positive at large α. The boundary is the crossing; bisection finds it in forty steps.")],
        top=1.82, bottom=5.86, label_w=3.30, numbered=True, gap=0.09)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.96, W - 2 * M, 0.72, fill=WASH, line=AMBER)
    d.text(s, "Two traps.  A bracket with the same sign at both ends has no answer inside: raise, do not return a number (PS5 Q5b).  And at the crossing Re λ hits zero while Im λ is √3 — bisect on |λ| and you never find it.",
           M + 0.18, 6.04, W - 2 * M - 0.36, 0.5, size=12.5, color=INK)
    d.foot(s, "Nothing in those five steps used symmetry, or three genes, or Hill functions. That is why the method is the part worth keeping and the formula is not.")
    d.notes(s, "THIS IS THE TUTORIAL SURFACE for T29 and it is deliberately "
               "slow. Walk it. They write exactly this on PS5 Q5a–b before "
               "they are allowed to import ours.\n"
               "STEP 2: say why there is exactly one root, because it is the "
               "one place in the session where monotonicity does real work. "
               "alpha/(1+x^n) decreases in x, x increases in x, so the two "
               "curves cross once. Contrast the toggle, where the same "
               "question had one or three answers depending on alpha — that "
               "is why the toggle needed a picture and this does not.\n"
               "STEP 3: offer both routes honestly. The analytic J is faster "
               "and exact; the finite-difference J needs no algebra and works "
               "on a ring of seven with unequal parameters, which is where "
               "they will actually be on PS5 Q5c and Q6.\n"
               "STEP 4: this is the error to name out loud, twice. numpy "
               "returns eigenvalues in no useful order; abs() and .real.max() "
               "give different answers and only one of them is stability.\n"
               "THE TRAP BOX: the ValueError requirement on PS5 is not "
               "pedantry. A bisection handed a non-bracketing interval will "
               "happily converge to an endpoint and report it as a boundary. "
               "Silent wrong answers are the ones that get into papers.")

    # 10 THE WALL AT n = 2 ----------------------------------------------------
    s = d.light()
    d.header(s, "50 – 54 min", "The design space")
    d.title(s, "You cannot buy oscillation with strong promoters")
    d.image(s, FIG + "s11_alpha_critical.png", M, 1.90, 5.00, 3.50)
    d.rows(s, [
        ("n ≤ 2: no α works", "In our model the boundary runs to infinity: however strong the promoters, the ring settles.", RED),
        ("n > 2: α_c falls fast", "At n = 3, α ≈ 3.8; at n = 4, exactly 2.", TEAL),
        ("n = 2 is still cooperative", "A dimer on two operators is n = 2. The toggle's n = 1 wall was weaker; this one is stricter.", AMBER),
        ("Compare the toggle", "It needed n > 1. The ring needs n > 2 — adding a gene made it harder, not easier.", AMBER),
        ("And as in session 9, n is bought, not tuned", None, AMBER)],
        top=1.80, bottom=6.50, side=False, pad=0.02, gap=0.08,
        left=6.00, right=12.63, label_color=INK)
    d.foot(s, "Circles are the boundary located by sweep; the line is the formula. They are the same curve.")
    d.notes(s, "This is the session's design ledger entry and it rhymes "
               "deliberately with session 9's engineerability slide. The "
               "students should feel the repetition — twice now the quantity "
               "that decides whether the circuit works at all is the one you "
               "cannot tune.\n"
               "Elowitz used LacI, TetR and cI, all of which bind cooperatively. "
               "That was not decoration.")

    # 10b THEIR OWN BOUNDARY --------------------------------------------------
    s = d.light()
    d.header(s, "50 – 54 min", "The same picture, drawn in 2000")
    d.title(s, "They drew this boundary too")
    d.paper_figure(s, "elowitz2000_fig1b", M, 1.80, 5.00, 3.40,
                   "Elowitz & Leibler 2000, Fig. 1b",
                   "stable steady state, and the region where it oscillates")
    d.rows(s, [
        ("Same object", "A design space cut in two: settle on one side, oscillate on the other."),
        ("Different axes", "Theirs: protein-to-mRNA lifetime ratio against proteins per cell. Ours: α and n."),
        ("⚠ And their n = 2 oscillates", "Curve B is n = 2 and bounds a real unstable region, with their design point inside."),
        ("The honest difference", "Folding mRNA away is the worst case. Keep it and the requirement relaxes to g > 4/3 — how they designed at n = 2.")],
        top=1.80, bottom=6.50, side=False, pad=0.02, gap=0.08,
        left=6.00, right=12.63, label_color=INK)
    d.foot(s, "Our n > 2 is a fact about our model, not about repressilators. Knowing which is which is the whole skill.")
    d.notes(s, "Sixty seconds, and it is the house pattern — session 8 paired "
               "Gardner's Fig. 2c,d with our own computed bifurcation line, and "
               "this is the same move.\n"
               "The point worth making: they did this in 2000, before the field "
               "existed, and the reason the repressilator worked at all is that "
               "they computed the boundary FIRST and then chose parts to land "
               "inside it. That is the whole argument for the course.\n"
               "The X is the caption's 'typical parameter values', used for "
               "their Fig. 1c simulation — near where they expected to sit, not "
               "a measurement of the built device. Do not overclaim it.\n"
               "⚠ THE IMPORTANT ONE, and do not skip it because it is "
               "uncomfortable: their curve B is n = 2, and it bounds a real "
               "unstable region. Ten minutes ago we said n <= 2 never "
               "oscillates. Both statements are correct — ours is the beta -> 0 "
               "limit of theirs, and that limit is the worst case. Keeping the "
               "mRNA step drops the requirement to about g > 4/3 at beta = 1.\n"
               "This is the most valuable thing in the session and it is worth "
               "being explicit: you did not learn 'rings need n > 2'. You "
               "learned how to compute a boundary, and that the boundary moves "
               "when you change what you keep.")

    # 11 THE READING ----------------------------------------------------------
    s = d.light()
    d.header(s, "54 – 62 min", "The reading  ·  what the criterion cannot tell you")
    d.title(s, "It ticks. It keeps terrible time. Why?")
    d.paper_figure(s, "potvintrottier2016_fig1d", M, 1.62, 5.4, 2.78,
                   "Potvin-Trottier 2016, Fig. 1d",
                   "one cell, before and after it loses the reporter plasmid")
    d.paper_figure(s, "potvintrottier2016_fig3a", 6.55, 1.62, 3.32, 2.78,
                   "Potvin-Trottier 2016, Fig. 3a",
                   "period across temperatures and media, two circuits")
    d.text(s, "Only about 40% of Elowitz's cells were reported to oscillate. These hold phase for hundreds of generations — and two of the three fixes were REMOVALS.",
           M, 5.24, W - 2 * M, 0.5, size=15.5, bold=True, color=INK)
    # The right-hand panel's reading used to be spelled out here too, and the
    # numbers in it are the next surface's third column. Kept once.
    d.text(s, "Left: this cell loses the reporter plasmid mid-run and starts keeping time — the reporter's own ssrA tag was competing with the circuit measuring it.",
           M, 6.01, W - 2 * M, 0.55, size=13, color=BODY)
    d.assigned_on(M, 6.80, 8.0, s)
    d.notes(s, "DISCUSSION SEGMENT — they read this. Open with the goals-slide "
               "question: which change did you expect to matter most, and were "
               "you right?\n"
               "THE SURPRISE, and it is the one to spend time on: the "
               "measurement was corrupting the circuit. Elowitz put GFP on a "
               "separate higher-copy plasmid — which is on our artifact slide — "
               "and the reporter's ssrA-ASV degradation tag was competing for "
               "the same proteases. Fig. 1d is a single cell losing that "
               "plasmid mid-experiment and starting to keep time. Nobody "
               "designs a reporter expecting it to be part of the circuit.\n"
               "THE THESIS, in their own words: they improved it 'not by adding "
               "control loops, but by simply removing existing features'. In a "
               "course that has spent ten sessions adding parts, that is worth "
               "saying twice.\n"
               "THE NUMBERS: only ~40% of the original cells oscillated at all. "
               "The streamlined circuit holds 14 generations across division "
               "times from 27 to 59 min, keeps phase for hundreds of "
               "generations, and whole flasks and colonies oscillate "
               "synchronously with no coupling between cells.\n"
               "THE MOVE TO LAND, and state it carefully: every one of their "
               "changes MOVES alpha, and therefore g — untagging the repressors "
               "raises alpha, the sponge changes the effective K, moving the "
               "reporter changes the protease load. What none of them touches "
               "is alpha_c(n), the CRITERION, which depends on n alone. So the "
               "circuit stays comfortably past onset throughout, and every "
               "improvement they made is invisible to our model: it is a right "
               "tool for 'does it tick' and a wrong tool for 'does it keep "
               "time'. That is the honest hand-off to session 12.\n"
               "If there is appetite, Fig. 3c is the colony image: concentric "
               "fluorescent rings like tree rings, because every cell in the "
               "colony is still in phase.")

    # 11b THREE CHANGES ------------------------------------------------------
    s = d.light()
    d.header(s, "54 – 62 min", "The reading  ·  what the criterion cannot tell you")
    d.title(s, "Three changes, and what each one moved")
    d.text(s, "The change", M, 1.78, 2.9, 0.32, size=12.5, font=HEAD, bold=True, color=MUTED)
    d.text(s, "Why it should help", M + 3.0, 1.78, 4.6, 0.32, size=12.5, font=HEAD, bold=True, color=MUTED)
    d.text(s, "What it actually did", M + 7.7, 1.78, 3.9, 0.32, size=12.5, font=HEAD, bold=True, color=MUTED)
    ROWS = [
            ("Reporter off its own plasmid",
             "The separate reporter sat on a high-copy ColE1 vector whose copy number drifts slowly — and its own ssrA-ASV tag competed for the proteases degrading the repressors. The measurement was inside the circuit.",
             "Amplitude scatter 78% → 36%.  Period 2.4 → 5.6 generations.  Fig. 1d catches one cell losing that plasmid mid-run and starting to keep time.",
             TEAL),
            ("Degradation tags off the repressors",
             "With no ssrA tag a repressor is removed only by dilution as the cell grows. Fewer stochastic removal events, and no shared protease coupling the three genes together.",
             "Oscillated in every cell, period → ~10 generations. But the noise in the period barely moved — and that is the result that told them the problem was somewhere else.",
             TEAL),
            ("A TetR sponge put back",
             "Extra TetR operator sites soak up the last few molecules, lifting the derepression threshold off the floor. Diagnosed with a three-color circuit: the noisiest interval was the one where TetR was low.",
             "Period → 14 generations, drift 14% per period — about 18 periods before half a period is lost. This one is an ADDITION, and the original design already carried these sites.",
             AMBER)]
    ys, hs, _y = [], [], 2.08
    for _k, _why, _did, _c in ROWS:
        h = max(T.text_height(_why, 4.6, T.TYPE["caption"]),
                T.text_height(_did, 3.9, T.TYPE["caption"]), 0.74)
        ys.append(_y); hs.append(h); _y += h + 0.10
    for i, (k, why, did, c) in enumerate(ROWS):
        # Pitch from the tallest cell in the row, not from a fixed 1.48: at
        # caption size a 210-character cell is four lines in a 4.6in column
        # and the row below it started three lines down.
        y = ys[i]
        h = hs[i]
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.14, h, fill=c, line=None)
        d.text(s, k, M + 0.3, y, 2.6, 0.74, size=14, font=HEAD, bold=True, color=INK)
        d.text(s, why, M + 3.0, y, 4.6, h, size=12.5, color=BODY)
        d.text(s, did, M + 7.7, y, 3.9, h, size=12.5, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, ys[-1] + hs[-1] + 0.12,
            W - 2 * M - 0.72, 0.66, fill=WASH, line=RED)
    d.text(s, "Not one of those three changes touches α_c(n) — our boundary depends on n alone. They move α, K and the lifetime: the operating POINT, not the boundary. Every circuit in the paper oscillates, so all sit past g = 2 and our model cannot tell them apart.",
           M + 0.18, ys[-1] + hs[-1] + 0.19, W - 2 * M - 1.08, 0.54, size=12.5,
           bold=True, color=INK)
    d.notes(s, "This is the surface that earns the session its honest ending, "
               "and it is the one to protect if you are running late — cut the "
               "ConcepTest instead.\n"
               "Take the three rows as a DETECTIVE STORY, in order, because "
               "that is how the paper reads. Change 1 was the obvious one and "
               "it worked. Change 2 was predicted to fix the period noise and "
               "it DID NOT — say that plainly, because a negative result "
               "driving the next experiment is the most useful thing in the "
               "paper. Change 3 came from measuring where the noise actually "
               "was, with three colors, and only then fixing it.\n"
               "ROW 3, be careful and be honest: this is an addition, and it "
               "is a re-introduction — the high-copy reporter plasmid they "
               "had just removed was already carrying TetR binding sites. So "
               "the abstract's 'not by adding control loops, but by simply "
               "removing existing features' is true — a sponge is not a "
               "control loop — but it is not the whole story, and a student "
               "who notices that is reading well.\n"
               "NUMBERS, if asked: the body text says the period rose to ~5.7 "
               "generations and the Fig. 1e caption says 5.6 over 8,694 "
               "divisions. Either is fine; the discrepancy is theirs.\n"
               "THE RED BOX is the hand-off to Tuesday and it is worth "
               "reading off the screen word for word. We spent fifty minutes "
               "deriving a criterion, it is correct, and it is blind to "
               "everything this paper is about. That is not a failure of the "
               "criterion — it is what it means for a model to have a scope.")

    # 12 CONCEPTEST -----------------------------------------------------------
    s = d.light()
    d.header(s, "62 – 67 min", "Pose  ·  silent vote  ·  argue  ·  vote again")
    d.title(s, "Your ring oscillates. You want a longer period.")
    for i, (letter, opt) in enumerate([
            ("A", "Raise α on all three promoters"),
            ("B", "Add degradation tags to all three repressors"),
            ("C", "Add two more repressors, making a ring of five"),
            ("D", "Add a fourth repressor, making a ring of four")]):
        y = 2.2 + i * 0.95
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, W - 2 * M, 0.75, fill=CARD, line=RULE, lw=1)
        d.text(s, letter, M + 0.25, y + 0.2, 0.5, 0.4, size=20, font=HEAD,
               bold=True, color=CYAN)
        d.text(s, opt, M + 0.9, y + 0.22, W - 2 * M - 1.2, 0.4, size=16, color=BODY)
    d.foot(s, "Period is measured in protein lifetimes. Which of these changes a lifetime, which changes the number of steps around the loop — and which stops it being a clock?")
    d.notes(s, "Answer: A and C, and the discussion is which and why.\n"
               "A: measured on our own model — the period goes 3.6 -> 5.2 -> "
               "8.0 as alpha rises to 3x and 10x alpha_c, because each "
               "repressor has to be built up and torn down further every "
               "cycle.\n"
               "C: more stages, more delay around the loop, longer period. That "
               "is T30 and the route to session 22. C buys the most.\n"
               "B is the trap and most of the room will pick it. Tags shorten "
               "the lifetime, and the period is measured IN lifetimes, so in "
               "real time the clock speeds up. Worse than that: in our scaling "
               "alpha = beta/(gamma K), so raising the removal rate gamma also "
               "LOWERS alpha, which lowers g and shortens the period again. B "
               "loses twice. If a student says 'tags change alpha', they have "
               "the session-9 result right and should be credited out loud.\n"
               "D is the one to enjoy. A ring of FOUR does not oscillate more "
               "slowly — it does not oscillate at all. Even rings cross on a "
               "REAL eigenvalue (omega = -1), so the state goes unstable into "
               "bistability: you get a toggle, not a slower clock. C and D are "
               "deliberately parallel, five against four, and the difference "
               "between them is the whole odd/even result. That is handout "
               "item 3, and anyone who gets D right has already done it.")

    # 13 DELAY — T30 ----------------------------------------------------------
    s = d.light()
    d.header(s, "67 – 71 min", "The other route to a clock")
    d.title(s, "You do not need three genes. You need a delay.")
    d.rows(s, [
        ("What the ring was really doing", "Each stage took time. Three stages of build-up is a delay, dressed up as topology."),
        ("Negative feedback plus delay oscillates", "One gene repressing itself, with the repression arriving late enough, does the same job."),
        ("Which is why five stages is slower", "More stages, more delay, longer period — and for an ODD ring the gain to beat falls as you add stages: 2, then 1.24, then 1.11."),
        ("And why real clocks rarely use a ring", "Many circadian oscillators run on transcription–translation delay rather than a ring — and KaiABC runs on neither, in a test tube.")],
        top=1.92, bottom=6.20, label_w=4.60)
    d.text(s, "The engineering statement: a clock needs enough gain and enough delay. The ring gave you the delay by making you walk round it.",
           M, 6.35, W - 2 * M, 0.5, size=16, bold=True, color=INK)
    d.notes(s, "T30, and it is a HAND row on PS5 — an argument, not a "
               "computation. Four minutes, no algebra. The point is that the "
               "three-gene ring is one implementation of a more general "
               "principle, so they do not leave thinking clocks require rings.\n"
               "Do not derive the delay-differential criterion. Name it, say it "
               "is the same shape — gain against delay — and move on.")

    # 14 FADED SET ------------------------------------------------------------
    s = d.light()
    d.header(s, "71 – 78 min", "Worked set  ·  handout  ·  start where you like")
    d.title(s, "Four problems. The scaffolding falls away.")
    for i, (num, k, txt, c) in enumerate([
            ("1", "Fully worked", "n = 3: fixed point, g, verdict", TEAL),
            ("2", "Last step blank", "n = 4: find α_c yourself", GREEN),
            ("3", "Last two blank", "a ring of five: redo the eigenvalues", CYAN),
            ("4", "Bare problem", "kill it without touching α", AMBER)]):
        x = M + i * 3.05
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.1, 2.8, 2.5, fill=CARD, line=c, lw=2)
        d.shape(s, S.OVAL, x + 1.15, 2.35, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 1.15, 2.46, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 0.15, 3.05, 2.5, 0.4, size=16, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, txt, x + 0.15, 3.5, 2.5, 0.9, size=13.5, color=MUTED, align="c")
    d.text(s, "Item 3 is today's derivation with one number changed. If you can do it, you did not memorise the answer — you followed the argument.",
           M, 4.92, W - 2 * M, 0.5, size=17, bold=True, color=INK)
    d.text(s, "Item 4 has more than one right answer. Name the parameter and say which way you move it.",
           M, 5.72, W - 2 * M, 0.4, size=15, color=BODY)
    d.notes(s, "Circulate. Item 3 is the fidelity check on the whole "
               "derivation: a ring of five has fifth roots of unity, the "
               "worst-case real part is -1 + g cos(pi/5), and the criterion "
               "becomes g > 1/cos(pi/5) = 1.236. Easier to oscillate, not "
               "harder — more delay around the loop.\n"
               "Do NOT work item 1 at the board.")

    # 15 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "78 – 80 min", "Next")
    d.title(s, "Every run of our model is identical. No cell is.")
    d.text(s, "Tuesday: noise, and the master equation.",
           M, 2.05, 11, 0.45, size=23, font=HEAD, bold=True, color=MINT)
    d.text(s, "Today's model has no randomness in it: start it twice from the same place and you get the same trajectory forever. But the traces you just looked at came from single cells, and no two agreed — a cell holds tens of molecules of a repressor, not micromolar of it.",
           M, 2.62, 11.3, 1.7, size=16, color=WHITE, spacing=1.25)
    d.text(s, "How do you model a circuit when the number of molecules is small enough to count? Session 12.",
           M, 4.44, 11.3, 0.34, size=14, italic=True, color=CYAN)
    d.assignment(s, y=5.02)
    d.notes(s, "The hand-off is earned rather than announced: the reading "
               "established that variability is the real problem, and we have "
               "just admitted our tool cannot see it.\n"
               "Elowitz 2002 goes out now. Say the access route out loud — it "
               "is through the library proxy, and it is the one paper this term "
               "with no free copy anywhere.")

    return d
