"""Session 12 — Noise and the master equation.

Tuesday 6 October. Session 11 stopped at its slide 18, so this session opens by
finishing it: the sweep step by step (the demonstration PS5 Q5a-b grades, due
Thursday), the n <= 2 wall, and delay (T30, also owed to the midterm).
Potvin-Trottier is the bridge -- a paper about removing noise sources one at a
time from a circuit our deterministic model says is fine.

Then the session proper, artifact first: Elowitz 2002's two colours in one
cell; the master equation for birth-death, derived to the Poisson; bursting as
one surface; Gillespie derived on the board and live-coded; and T17 -- negative
autoregulation against a constitutive gene at matched mean, with Becskei &
Serrano 2000 as the measurement.

The results, derived in class and verified in tests/test_stochastic.py:

    birth-death:   P_n Poisson, Fano = 1, eta^2 = 1/<n>
    bursting:      Fano = 1 + k_p/(gamma_m + gamma_p) ~ 1 + b   (stated, checked)
    NAR, matched mean:  Fano = 1/(1 + g),  g = n u^n/(1 + u^n)  -- session 11's g

Coverage: T31 (master equation), T32 (Gillespie), T33 (CV and Fano from
trajectories), T34 (intrinsic/extrinsic), T35 (bursting), T17 (NAR variance,
the obligation recorded in docs/coverage-matrix.md). Carried from S11: T29, T30.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks import theme as T
from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session12_Noise"
FIG = "figures/build/"


def build():
    d = Deck("Session 12 — Noise and the master equation", session=12)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 12", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Noise and the master equation", M, 2.72, 9.0, 1.3,
           size=42, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Two identical genes in one cell disagree. How much, why, and what a circuit can do about it",
           M, 4.15, 8.4, 0.8, size=18, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Thursday ended at the first sweep slide. The first four surfaces "
               "finish it, because two of them are graded on PS5, due Thursday.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions before we start")
    d.rows(s, [
        ("FROM THURSDAY", "The ring’s steady state loses stability when g = 2. What is g made of, and why does α drop out of it?", TEAL),
        ("FROM THURSDAY", "Why can a ring of three never settle into ‘LacI high’?", TEAL),
        ("FROM SESSION 7", "Negative autoregulation made a gene reach its steady state faster. Why faster?", CYAN)],
        top=1.95, bottom=6.30, label_w=2.70, numbered=True, label_role="caption")
    d.foot(s, "Hold question 3. By the end of today the same answer explains a second thing it does.")
    d.notes(s, "Q1: g = n x^n/(1 + x^n), the gain of one arm at the operating "
               "point. Substituting alpha = x(1 + x^n) cancels a power of "
               "(1 + x^n) and alpha with it.\n"
               "Q2: chase it: LacI high -> TetR low -> cI high -> LacI low. An odd "
               "ring cannot be consistently colored.\n"
               "Q3: the restoring rate is gamma plus the feedback's slope, so "
               "displacements decay faster (Rosenfeld 2002). Today that same "
               "faster return shrinks the spread: Becskei & Serrano make exactly "
               "this argument, and it is the T17 result.")

    # 3 GOALS -----------------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By 9:30 you should be able to answer")
    for i, (n, lab) in enumerate([("11", "Oscillation"), ("12", "Noise"),
                                  ("13", "Digital"), ("14", "Review"),
                                  ("15", "Midterm")]):
        x, here = M + i * 2.42, n == "12"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=14, bold=here,
               color=WHITE if here else MUTED, align="c")
    d.rows(s, [
        ("?", "Two copies of one gene, same promoter, same cell. Why do they disagree, and how would you tell that from the cell disagreeing with its neighbour?", None),
        ("?", "If you can only count molecules, what does the model look like — and what is the least noise an unregulated gene can have?", None),
        ("?", "You need a quieter reporter at the same mean. What do you change?", None)],
        top=2.95, bottom=6.50, label_w=0.50, label_role="emphasis",
        label_color=CYAN)
    d.notes(s, "The first is the reading. The second is the master equation and "
               "the Gillespie algorithm. The third is the design payoff: RBS "
               "against promoter, and negative feedback.")

    # 4 CARRY — THE SWEEP, STEP BY STEP (S11 9b) ------------------------------
    s = d.light()
    d.header(s, "8 – 14 min", "Finishing Thursday  ·  T29")
    d.title(s, "The sweep, one step at a time — this is PS5 Q5a")
    d.rows(s, [
        ("Fix n. Pick one α.", "One point in design space, one yes/no question: is the symmetric state stable?"),
        ("Find the fixed point.", "Solve  x = α/(1 + x^{n}).  The right side falls as x rises, so there is exactly one root. Bracket on [0, α]."),
        ("Build the Jacobian.", "g = n x^{n}/(1 + x^{n}), then J = -I - gP. Or finite-difference it — that one survives asymmetry."),
        ("Largest REAL part", "max Re λ over the three eigenvalues. Not the largest magnitude."),
        ("Repeat, then bisect.", "Negative at small α, positive at large α. The crossing is the boundary.")],
        top=1.82, bottom=5.82, label_w=3.30, numbered=True, gap=0.09)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.92, W - 2 * M, 0.90, fill=WASH, line=AMBER)
    d.text(s, "Two traps. A same-sign bracket has no root inside: raise an error (PS5 Q5b). At the crossing Im λ = √3, so bisecting on |λ| never finds it.",
           M + 0.18, 5.98, W - 2 * M - 0.36, 0.7, size=16, color=INK)
    d.notes(s, "This is S11's slide 19, unchanged in content. It is the "
               "demonstration of T29 and PS5 Q5a-b is due Thursday, so it is the "
               "one carried surface that cannot be cut.\n"
               "Step 2: why exactly one root -- alpha/(1+x^n) falls, x rises, they "
               "cross once. Contrast the toggle, where the same question had one "
               "or three answers.\n"
               "Step 4: numpy returns eigenvalues in no useful order; abs() and "
               ".real.max() give different answers and only one is stability.\n"
               "The trap box: a bisection handed a non-bracketing interval "
               "converges to an endpoint and reports it as a boundary.")

    # 5 CARRY — THE WALL AT n = 2 (S11 10) ------------------------------------
    s = d.light()
    d.header(s, "8 – 14 min", "Finishing Thursday  ·  the design space")
    d.title(s, "You cannot buy oscillation with strong promoters")
    d.image(s, FIG + "s11_alpha_critical.png", M, 1.90, 5.00, 3.50)
    d.rows(s, [
        ("n ≤ 2: no α works", "In our model the boundary runs to infinity.", RED),
        ("n > 2: α_{c} falls fast", "At n = 3, α ≈ 3.8; at n = 4, exactly 2.", TEAL),
        ("Compare the toggle", "It needed n > 1. The ring needs n > 2: one more gene, a stricter requirement.", AMBER),
        ("n is bought, not tuned", "You choose it by choosing the protein.", AMBER)],
        top=1.80, bottom=6.40, side=False, pad=0.02, gap=0.08,
        left=6.00, right=12.63, label_color=INK)
    d.foot(s, "Circles: the boundary found by sweep. Line: the formula. Elowitz & Leibler’s own n = 2 oscillates because they kept the mRNA step; we folded it away.")
    d.notes(s, "S11 slide 20, plus the one sentence from slide 21 that keeps "
               "this honest: their Fig. 1b curve B is n = 2 and bounds a real "
               "unstable region. Ours is the worst-case limit with mRNA folded "
               "away; keeping mRNA relaxes the requirement to about g > 4/3. The "
               "n > 2 wall is a fact about our model.")

    # 6 CARRY — DELAY, T30 (S11 13) -------------------------------------------
    s = d.light()
    d.header(s, "14 – 17 min", "Finishing Thursday  ·  T30")
    d.title(s, "You do not need three genes. You need a delay.")
    d.rows(s, [
        ("What the ring was doing", "Each stage took time. Three stages of build-up is a delay, dressed up as topology."),
        ("Feedback plus delay oscillates", "One gene repressing itself, with the repression arriving late enough, does the same job."),
        ("Why five stages is slower", "More stages, more delay, longer period — and for an odd ring the gain to beat falls: 2, then 1.24, then 1.11."),
        ("Why real clocks rarely use a ring", "Many circadian clocks run on transcription–translation delay. KaiABC runs on neither, in a test tube.")],
        top=1.92, bottom=6.10, label_w=4.30)
    d.text(s, "A clock needs enough gain and enough delay. The ring gave you the delay by making you walk round it.",
           M, 6.22, W - 2 * M, 0.5, size=16, bold=True, color=INK)
    d.notes(s, "T30, assessed on PS5 Q6 (247-required) and committed to the "
               "midterm on 26 September as an argument about gain and delay, not "
               "a delay-differential calculation. No algebra here: name the "
               "principle and move on.")

    # 7 BRIDGE — POTVIN-TROTTIER ----------------------------------------------
    s = d.light()
    d.header(s, "17 – 21 min", "Thursday’s reading  ·  the bridge to today")
    d.title(s, "It ticks, badly — and our model cannot say why")
    d.paper_figure(s, "potvintrottier2016_fig1d", M, 1.70, 5.2, 2.80,
                   "Potvin-Trottier 2016, Fig. 1d",
                   "one cell loses the reporter plasmid, and starts keeping time")
    d.rows(s, [
        ("Reporter off its plasmid", "Its ssrA tag competed for the repressors’ proteases. Amplitude scatter 78% → 36%.", TEAL),
        ("Tags off the repressors", "Removal by dilution only. Every cell oscillated, but period noise barely moved.", TEAL),
        ("A TetR sponge", "Soaks up the last few molecules. Period 14 generations, drift 14% per period.", AMBER)],
        top=1.70, bottom=5.30, side=False, pad=0.02, gap=0.08,
        left=6.20, right=12.63, label_color=INK)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.48, W - 2 * M, 0.98, fill=WASH, line=RED)
    d.text(s, "The fix that steadied the period acted on the last few TetR molecules. Our ODE has no ‘few’ in it — run it twice, same trajectory forever. Today we build the model that does.",
           M + 0.18, 5.56, W - 2 * M - 0.36, 0.8, size=16, bold=True, color=INK)
    d.assigned_on(M, 6.80, 8.0, s, prefix="Potvin-Trottier was assigned for Thursday")
    d.notes(s, "One surface where Thursday had two. The detective story in one "
               "breath: change 1 was the obvious one and worked; change 2 was "
               "predicted to fix the period noise and did not; change 3 came from "
               "measuring where the noise was, with three colours, and found it "
               "in the interval where TetR was low.\n"
               "The sponge is an addition, and a re-introduction -- the removed "
               "reporter plasmid already carried TetR sites. Their abstract's "
               "'not by adding control loops' is true (a sponge is not a loop) "
               "but not the whole story.\n"
               "The red box is the hand-off: the noise lives where copy numbers "
               "are small, and a continuous concentration cannot see that. Today "
               "is the tool that can.")

    # 8 THE ARTIFACT — ELOWITZ 2002 -------------------------------------------
    s = d.light()
    d.header(s, "21 – 25 min", "The artifact")
    d.title(s, "Elowitz et al., Science 2002 — two colours, one cell")
    d.rows(s, [
        ("The construct", "One promoter, two copies in the chromosome: one drives CFP, one YFP."),
        ("Held equal", "Same cell; loci equidistant from, and on opposite sides of, the origin."),
        ("Measured", "Both colours in every cell. Green CFP and red YFP, merged."),
        ("What you see", "Repressed: red, green and yellow. Induced: almost all yellow.")],
        top=1.90, bottom=6.30, label_w=2.30, right=6.70)
    d.paper_figure(s, "elowitz2002_fig2ab", 6.95, 1.85, 5.65, 3.40,
                   "Elowitz et al. 2002, Fig. 2A–B",
                   "RP22 repressed by LacI, and with 2 mM IPTG")
    d.assigned_on(M, 6.80, 9.0, s, prefix="Read for today, through the library proxy")
    d.notes(s, "You read this for today, through the library proxy -- it is the "
               "one paper this term with no free copy. Some of the room did not "
               "get the assignment slide on Thursday; say what it is.\n"
               "Correction to the reading guide: it pointed at Fig. 2, which is "
               "micrographs. The plot that does the work is Fig. 3A, and the "
               "algebra behind it is in their supplement and in Swain, Elowitz "
               "& Siggia (PNAS 2002), not in this paper. We do it here.\n"
               "The equidistant loci matter: a gene near the origin is copied "
               "before one near the terminus, so for part of the cycle it has "
               "two copies to the other's one. Putting both at the same distance "
               "removes that systematic difference (p. 1184).\n"
               "Do not explain the arrows on the figure yet. That is the next "
               "ten minutes.")

    # 9 ARGUE -----------------------------------------------------------------
    s = d.dark()
    d.header(s, "25 – 31 min", "Argue it out  ·  groups of 3–4")
    d.title(s, "Same promoter, same cell. Why are the colours different?")
    d.rows(s, [
        ("Name two things that would make BOTH colours brighter in one cell than its neighbour. Then one thing that would make one brighter and not the other.", None),
        ("On the plot, which direction does each of your answers move a point — along the diagonal, or across it?", None),
        ("Repress both promoters until the cells make 3% as much protein. Which kind of spread grows, and why?", None)],
        top=2.05, bottom=6.35, side=False, numbered=True,
        label_role="emphasis", label_color=WHITE)
    d.foot(s, "Question 3 is a prediction. Table 1 has the answer, and we read it in four minutes.")
    d.notes(s, "Q1, both brighter: more polymerase or ribosomes, a bigger cell, a "
               "different point in the cell cycle, more of a shared regulator. "
               "One and not the other: which polymerase happened to arrive, when "
               "an mRNA happened to decay -- events at that gene.\n"
               "Q2: shared causes move a point along the diagonal; private "
               "causes across it. That is the whole decomposition.\n"
               "Q3: the intrinsic part grows because the counts are smaller. "
               "Most of the room will not have the reason yet; the master "
               "equation gives it fifteen minutes later. Extrinsic also grows, about 5-fold, and the "
               "paper's reason is cell-to-cell variation in LacI (p. 1184).")

    # 10 SORTED ---------------------------------------------------------------
    s = d.light()
    d.header(s, "31 – 34 min", "Your answers, sorted  ·  T34")
    d.title(s, "Across the diagonal: the gene. Along it: the cell.")
    d.paper_figure(s, "elowitz2002_fig3a", M, 1.62, 5.60, 3.30,
                   "Elowitz et al. 2002, Fig. 3A", "M22 (quiet) and D22 (noisy), one point per cell")
    d.rows(s, [
        ("Intrinsic, η_{int}", "How much two copies in one cell differ. η = σ/mean.", TEAL),
        ("Extrinsic, η_{ext}", "How much cells differ in what both copies share.", AMBER),
        ("They add as squares", "η_{int}^{2} + η_{ext}^{2} = η_{tot}^{2}.  M22: 5.5² + 5.4² = 7.7² (×10^{-2}).", INK)],
        top=1.70, bottom=5.00, side=False, pad=0.02, gap=0.08,
        left=6.55, right=12.63, label_color=INK)
    d.text(s, "Table 1, ×10^{-2}:  constitutive M22  5.5 / 5.4 / 7.7  ·  LacI-repressed RP22  25 / 33 / 41  ·  RP22 + IPTG  6.3 / 9.8 / 11.7  ·  repressilator  12 / 42 / 43",
           M, 5.55, W - 2 * M, 0.7, size=15, color=BODY)
    d.foot(s, "Elowitz et al. 2002, Table 1, p. 1185. Their arrows on Fig. 3A are the answer to your question 2.")
    d.notes(s, "Read the order int / ext / tot off the table row by row. "
               "Repressed 30-fold (intensity 0.030), intrinsic noise goes from "
               "5.5 to 25 -- the room's Q3 prediction. Add IPTG and both come "
               "back down. The repressilator row: extrinsic noise is huge "
               "because the clock moves LacI in every cell. Intrinsic noise is "
               "12 at intensity 0.18, against about 8 that their own Fig. 3B fit "
               "(c1/m + c2) predicts at that mean -- about 1.5x higher, which is "
               "their point that noise is larger on the approach to a steady "
               "state than at one (p. 1186). Do not compare it to M22: M22 is at "
               "intensity 1.\n"
               "The estimators, if asked (Swain et al. 2002): eta_int^2 = "
               "<(c1-c2)^2>/(2<c1><c2>), eta_ext^2 = (<c1 c2> - <c1><c2>)/"
               "(<c1><c2>). They are what produced the numbers on our plot.\n"
               "figures/build/s12_two_color.png is our own version of Fig. 3A "
               "(a simulated M22-like and RP22-like strain, with the Swain "
               "estimators printed on it); it goes in the notebook rather than "
               "on this surface, where it was too small to read.")

    # 11 THE OBJECT — COUNTS, EVENTS, RATES ----------------------------------
    s = d.light()
    d.header(s, "34 – 36 min", "Before the model  ·  what a count does")
    d.title(s, "At tens of molecules, a concentration is the wrong variable")
    d.image(s, FIG + "s12_ssa_anatomy.png", M, 1.62, W - 2 * M, 2.90)
    d.rows(s, [
        ("A count", "n molecules. It changes by one, at an instant.", TEAL),
        ("A rate is a chance", "a birth in the next dt with probability k·dt; a death with γn·dt.", AMBER),
        ("No schedule", "between events the count sits still for a random time τ.", RED)],
        top=4.62, bottom=6.72, label_w=2.60, gap=0.05)
    d.notes(s, "Teach the object before the model. Three sentences, and the "
               "second is the one the biologists need slowly: k is not a number "
               "of molecules per minute that arrive on schedule, it is a chance "
               "per minute. The two tau arrows are two waits of very different "
               "length from almost the same total rate.\n"
               "This picture is twelve events from the simulator we will write "
               "in twenty minutes.")

    # 12 RUN — THE MASTER EQUATION --------------------------------------------
    d.derivation_fig(
        "36 – 46 min", "Built one line at a time",
        "What is the distribution of n?",
        [("Ask for a list, not a number",
          "P_{n}(t) = Prob(n molecules at time t)",
          "one probability for every n = 0, 1, 2, … — the state of our knowledge"),
         ("Two ways into n",
          "k P_{n-1}   +   γ(n+1) P_{n+1}",
          "a birth from n-1; or a death from n+1, which has n+1 molecules to lose"),
         ("Two ways out of n",
          "a birth or a death:  (k + γn) P_{n}",
          "both leave n, so both are losses"),
         ("In minus out: the master equation",
          "dP_{n}/dt = kP_{n-1} + γ(n+1)P_{n+1} - (k+γn)P_{n}",
          "T31. One equation per n — an infinite ladder of them"),
         ("Name the flow across one rung",
          "J_{n} = k P_{n-1} - γn P_{n}",
          "net traffic up from n-1 to n. Then dP_{n}/dt = J_{n} - J_{n+1}: expand it and step 4 comes back"),
         ("The bottom rung carries nothing",
          "steady: all J_{n} equal, and J_{0} = 0",
          "there is no n = -1 to arrive from. One zero at the bottom makes every rung zero"),
         ("Climb the ladder",
          "kP_{n-1} = γnP_{n}  ⇒  P_{n} = P_{0}(k/γ)^{n}/n!",
          "each rung multiplies by (k/γ)/n. Normalise: P_{0} = e^{-k/γ}. That is a Poisson"),
         ("Read off the noise",
          "⟨n⟩ = σ^{2} = k/γ ,   η^{2} = 1/⟨n⟩",
          "η = σ/⟨n⟩, the CV. Fano = σ^{2}/⟨n⟩ = 1: the floor for an unregulated gene, set by the count alone")],
        [FIG + "s12_bd_traj.png", None, None, None, None, None,
         FIG + "s12_bd_hist.png", None],
        closing="Halve the count and η² doubles. Only more molecules, or feedback, fixes that.",
        board="J_{n} = k P_{n-1} − γn P_{n} = 0   ⇒   Poisson,  η^{2} = 1/⟨n⟩",
        note=("T31, eight steps. The one where something disappears is step 6: "
              "the flux at the bottom of the ladder is zero because there is "
              "nowhere below n = 0 to come from, and steady state forces every "
              "flux to equal it. Say that slowly; it is why a birth-death chain "
              "can be solved by hand and most networks cannot.\n"
              "Step 5: expand J_n - J_{n+1} on the board and show it reproduces "
              "step 4 term by term. The biologists need to see it is the same "
              "equation rewritten, not a new one.\n"
              "Step 7: write P_1 = (k/gamma) P_0, P_2 = (k/gamma)/2 P_1, and let "
              "the factorial appear. The normalisation sum is the series for e.\n"
              "Step 8 against the reading: Elowitz fit eta_int^2 ~ c1/m + c2 "
              "(Fig. 3B caption). The c1/m term is this 1/<n>. The floor c2 is "
              "not, and that is a fair question to leave open. Their recA result "
              "points at transient copy-number differences (p. 1186); that this "
              "sets c2 is our inference, not their claim. The fit is in the "
              "Fig. 3B caption, p. 1185.\n"
              "The right panel is our simulator, not the formula: mean 9.96, "
              "variance 9.92.\n"
              "LEDGER: eta^2 = 1/<n> for an unregulated gene."))

    # 13 BURSTING (one surface) -----------------------------------------------
    s = d.light()
    d.header(s, "46 – 49 min", "The same count, made in bursts  ·  T35")
    d.title(s, "Same mean, two designs, five times the variance")
    d.image(s, FIG + "s12_bursting.png", M, 1.62, W - 2 * M, 2.90)
    d.rows(s, [
        ("Bursts", "k_{m} per lifetime, each of b = k_{p}/γ_{m} proteins: mean = (k_{m}/γ_{p})·b.", TEAL),
        ("Fano ≈ 1 + b", "exactly 1 + k_{p}/(γ_{m} + γ_{p}): 1.91 and 10.09 here, simulated 1.9 and 10.3.", AMBER),
        ("Design rule", "at a given mean, strong promoter plus weak RBS is quieter.", RED)],
        top=4.62, bottom=6.72, label_w=2.60, gap=0.05)
    d.notes(s, "T35, and by decision this is one surface. The formula is STATED, "
               "not derived here: it is the stationary result for the two-stage "
               "model (Thattai & van Oudenaarden 2001, ref. 17 of Elowitz). What "
               "the slide does instead is check it: the simulated Fano factors "
               "in the legend are 1.9 and 10.3 against exact 1.91 and 10.09.\n"
               "The intuition to give: the master-equation result assumed "
               "proteins arrive one at a time. If they arrive ten at a time, the "
               "count jumps by ten and the variance per molecule of mean goes up "
               "by about ten.\n"
               "Both runs have mean 50: k_m = 50, b = 1 against k_m = 5, b = 10. "
               "The design rule is the reason a promoter library and an RBS "
               "library are not interchangeable even when they reach the same "
               "mean.")

    # 14 RUN — GILLESPIE, THE TWO DRAWS ---------------------------------------
    d.derivation_fig(
        "49 – 53 min", "Built one line at a time",
        "How do you simulate one cell exactly?",
        [("Add up every rate",
          "a_{0} = Σ a_{j} ;   birth–death: a_{0} = k + γn",
          "the chance per unit time that SOMETHING happens"),
         ("Nothing happens for τ",
          "Prob(no event in τ) = exp(-a_{0}τ)",
          "each short dt survives with probability 1 - a_{0}dt; multiply τ/dt of them"),
         ("So draw the wait",
          "τ = -ln(u_{1})/a_{0} ,   u_{1} uniform on (0, 1)",
          "WHEN. An exponential with rate a_{0}"),
         ("Then draw which",
          "pick reaction j with probability a_{j}/a_{0}",
          "WHICH. Line up the a_{j} end to end and drop u_{2}·a_{0} on the line"),
         ("Fire it, and go again",
          "t ← t + τ ,   x ← x + stoich_{j}",
          "then recompute every a: the rates changed because the count did")],
        [FIG + "s12_ssa_anatomy_col.png", None, None, None, None],
        closing="Two random numbers per event, and no approximation anywhere.",
        board="τ = −ln u_{1} / a_{0}   ·   j: a_{j}/a_{0}",
        note=("T32, derived before it is coded. Step 2 is the one to do at the "
              "board: (1 - a0 dt)^(tau/dt) -> e^{-a0 tau}. Anyone who has met "
              "radioactive decay has met it.\n"
              "Step 3: inverting the exponential's CDF. If u is uniform, "
              "-ln(u)/a0 has the right distribution. Say that this is the one "
              "line students most often get wrong in code: dividing by a0 "
              "versus multiplying.\n"
              "Step 5: the rates are recomputed every event. That is why it is "
              "exact and why it is slow -- millions of events for a mean of a "
              "few hundred over a long run."))

    # 15 LIVE CODE ------------------------------------------------------------
    s = d.dark()
    d.header(s, "53 – 58 min", "Live code  ·  the editor is the board")
    d.title(s, "Twenty lines, written now")
    d.rows(s, [
        ("Set up", "k, γ, n = 0, t = 0, and two lists to record t and n.", None),
        ("Loop", "a = [k, γn];  a0 = sum.  τ from u_{1};  if t + τ > t_{max}, stop.", None),
        ("Choose and fire", "birth if u_{2}·a0 < k, else death. Append t and n.", None),
        ("Check it", "time-weighted mean and variance, both k/γ; then Fano = v/m and CV = √v/m.", None)],
        top=1.95, bottom=5.40, label_w=2.60, label_role="emphasis",
        label_color=CYAN)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.55, W - 2 * M, 0.95, fill=None, line=AMBER)
    d.text(s, "The trap: np.mean(n_list) is wrong. Each state lasted a different τ — weight by how long it was held. Averaging events counts a state held for a nanosecond the same as one held for an hour.",
           M + 0.18, 5.62, W - 2 * M - 0.36, 0.8, size=16, color=WHITE)
    d.notes(s, "The code to type is in board-notes/s12-board-notes.md, "
               "one copy only so the two cannot drift.\n"
               "Expect m and v both near 10 after discarding the first few "
               "lifetimes. Then run ns[keep].mean() and show it comes out near "
               "10.5, not 10: a state with more molecules has a higher total "
               "rate k + gamma n, so it is left sooner and logged more often. "
               "The event-weighted mean is <n(k + gamma n)>/<k + gamma n> = "
               "210/20 = 10.5 exactly. Seed 0, T = 5000: 10.03 time-weighted, "
               "10.53 event-averaged.\n"
               "One cell's long run and many cells at one instant give the same "
               "distribution for a stationary process. That is why a trajectory "
               "CV (T33) and Elowitz's snapshot across cells measure the same "
               "thing -- at steady state, which a repressilator never is.\n"
               "Students write their own in Thursday's notebook before they "
               "import posb.stochastic.gillespie.")

    # 16 RUN — T17: NAR AT MATCHED MEAN ---------------------------------------
    d.derivation_fig(
        "58 – 66 min", "Built one line at a time",
        "Does negative feedback make a gene quieter?",
        [("Borrow a rule, and check it once",
          "variance = noise in / (2 × return rate)",
          "imported from the linear-noise theory, not derived here. Constitutive: 2k/2γ = k/γ, the Poisson"),
         ("Self-repression, same mean",
          "noise in = births + deaths = 2γx",
          "at steady state births = deaths = γx. Matched mean, same event rate: feedback cannot touch this line"),
         ("What feedback changes is the return",
          "return rate = γ - f′(x)",
          "f′ < 0: a cell that drifts high makes less, and comes back faster"),
         ("Write it with Thursday’s g",
          "γ - f′ = γ(1 + g),  g = n u^{n}/(1 + u^{n})",
          "g = -x f′/f, using f = γx at steady state; u = x/K. Here n is the cooperativity again, not the count"),
         ("Divide",
          "var = 2γx / 2γ(1+g)  ⇒  Fano = 1/(1+g)",
          "T17. At n = 4, x = K: g = 2, Fano 1/3. At mean 100 the CV falls from 0.100 to 0.058")],
        [FIG + "s12_nar_hist.png", None, None, None, FIG + "s12_nar_fano.png"],
        closing="Feedback did not remove noise at its source. It shortened each fluctuation.",
        board="Fano = 1/(1 + g),   g = n u^{n}/(1+u^{n})",
        note=("The T17 obligation, recorded in the coverage matrix since 14 "
              "September: a worked comparison at matched mean. This is it.\n"
              "Step 1 is the move to be honest about. The rule is the "
              "linear-noise (Ornstein-Uhlenbeck) result and it is imported, not "
              "proved. Returning the Poisson checks only its constant; it cannot "
              "check the 1/(return rate) dependence, which is the part feedback "
              "uses. The independent test is the Gillespie panel at step 5.\n"
              "Step 3 connects to retrieval question 3: faster return is "
              "Rosenfeld's faster response. One mechanism, two benefits.\n"
              "The right panel at step 5: Gillespie at x = K for n = 1, 2, 4, 8 "
              "gives 0.666, 0.494, 0.334, 0.204 against 0.667, 0.5, 0.333, 0.2.\n"
              "Limits for the board: protein-only model, no bursts; with bursts "
              "the benefit is smaller (the ConcepTest's numbers). And it is the "
              "INTRINSIC part only. Feedback also buffers slow extrinsic change "
              "in its own rates, and more strongly: from gamma x = f(x), "
              "d ln x*/d ln beta = 1/(1 + g), so a slow wobble in beta reaches x "
              "divided by 1 + g in CV, not by sqrt(1 + g). Elowitz p. 1186: "
              "noise-suppressing mechanisms 'need to respond to both sources'.\n"
              "LEDGER: Fano = 1/(1 + g) at matched mean."))

    # 17 THE MEASUREMENT — BECSKEI & SERRANO ----------------------------------
    s = d.light()
    d.header(s, "66 – 69 min", "The measurement")
    d.title(s, "Becskei & Serrano 2000: TetR repressing itself")
    d.paper_figure(s, "becskei2000_fig3a", M, 1.70, 3.90, 4.30,
                   "Becskei & Serrano 2000, Fig. 3a",
                   "Vc, autoregulated (A) against three controls")
    d.rows(s, [
        ("The circuit", "TetR–EGFP from a promoter carrying tet operators: it represses itself. Controls break the loop three ways.", TEAL),
        ("Their argument", "Deterministic: the self-repressed gene relaxes about twice as fast. Today’s step 3.", TEAL),
        ("The number", "Vc 6–9% with feedback; at equal mean, about threefold higher without (p. 592).", AMBER),
        ("⚠ More than our model allows", "Intrinsic noise alone, at g ≈ 2, cuts CV by √3 ≈ 1.7. Buffering slow extrinsic change cuts it by 1 + g.", RED)],
        top=1.70, bottom=6.45, side=False, pad=0.02, gap=0.08,
        left=4.90, right=12.63, label_color=INK)
    d.notes(s, "Not an assigned reading; it is the measurement T17 asks you to "
               "connect to.\n"
               "Their Vc is the CV, sigma/mean. Bars: A autoregulated about 6%; "
               "B EGFP under chromosomal TetR; C operator-replaced, after IPTG; "
               "D the Y42A mutant repressor, about 21-24%.\n"
               "Two equal-mean comparisons on p. 592. Control C (operator "
               "replaced) was sampled 'shortly after induction', a transient. "
               "Control B (EGFP under chromosomal TetR, 3-5 ng/ml atc) is not, "
               "and it shows 'about threefold higher variability'. So the "
               "threefold stands.\n"
               "Our protein-only result is 1/(1 + g) in Fano, 1/sqrt(1 + g) in "
               "CV: at g near 2, 1.7-fold. The measured gap is bigger. The "
               "likeliest reason is that their cells also differ in "
               "polymerase, ribosomes and plasmid copy -- extrinsic -- and "
               "feedback buffers slow changes in its own rates by the full "
               "1 + g in CV (d ln x*/d ln beta = 1/(1 + g)). That last step is "
               "ours, not theirs; say so.\n"
               "Their mutant D is not at matched mean -- its relative mean is 38 "
               "(Fig. 2b).")

    # 18 CONCEPTEST -----------------------------------------------------------
    s = d.light()
    d.header(s, "69 – 74 min", "Pose  ·  silent vote  ·  argue  ·  vote again")
    d.title(s, "Right mean, too noisy. Which changes help?")
    for i, (letter, opt) in enumerate([
            ("A", "Double the promoter, halve the RBS strength"),
            ("B", "Halve the promoter, double the RBS strength"),
            ("C", "Two identical copies in the chromosome, each at half the promoter"),
            ("D", "Make it repress itself, and retune the promoter to restore the mean")]):
        y = 2.0 + i * 1.02
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, W - 2 * M, 0.84, fill=CARD, line=RULE, lw=1)
        d.text(s, letter, M + 0.25, y + 0.2, 0.5, 0.4, size=20, font=HEAD,
               bold=True, color=CYAN)
        d.text(s, opt, M + 0.9, y + 0.2, W - 2 * M - 1.2, 0.4, size=16, color=BODY)
    d.foot(s, "Every option keeps the mean. You start at b = 10, Fano ≈ 10.")
    d.notes(s, "Answer: A and D. Checked by simulation at mean 50, starting from "
               "k_m = 5, b = 10 (Fano 9.7):\n"
               "A: b = 5 -> Fano 5.5.\n"
               "B: b = 20 -> worse, exact Fano 19.2.\n"
               "C is the trap: two independent copies at half rate. The variance "
               "doubles and the mean doubles, so the Fano factor is unchanged -- "
               "simulated 10.0. Copies average away extrinsic nothing and "
               "intrinsic nothing at fixed total mean.\n"
               "D: NAR with n = 2 and K = 50, so u = 1 at the retuned mean of 50 "
               "-> Fano 5.3; with n = 4, 4.0. Feedback and the RBS each buy about a factor of two here, "
               "and they stack.\n"
               "The argument to fish for in C: what matters is the size of each "
               "lump and how fast deviations are corrected, not how many places "
               "the lumps come from.")

    # 19 FADED SET ------------------------------------------------------------
    s = d.light()
    d.header(s, "74 – 79 min", "Worked set  ·  handout  ·  start where you like")
    d.title(s, "Four problems. The scaffolding falls away.")
    for i, (num, k, txt, c) in enumerate([
            ("1", "Fully worked", "birth–death at mean 25: Fano, η", TEAL),
            ("2", "Last step blank", "same mean, b = 4: the spread", GREEN),
            ("3", "Last two blank", "NAR at x = K, n = 3: the Fano", CYAN),
            ("4", "Bare problem", "read Table 1: which strain, which noise, why", AMBER)]):
        x = M + i * 3.05
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.1, 2.8, 2.5, fill=CARD, line=c, lw=2)
        d.shape(s, S.OVAL, x + 1.15, 2.35, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 1.15, 2.46, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 0.15, 3.05, 2.5, 0.4, size=16, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, txt, x + 0.15, 3.5, 2.5, 0.9, size=13.5, color=MUTED, align="c")
    d.text(s, "Item 3 is today’s last derivation with one number changed. Item 4 has no single right answer — say which row, which column, and what moved it.",
           M, 4.92, W - 2 * M, 0.8, size=17, bold=True, color=INK)
    d.notes(s, "Item 1: eta = 1/sqrt(25) = 0.2. Item 2: Fano about "
               "5, eta = sqrt(5/25) = 0.45. Item 3: g = 1.5, Fano 0.4, eta "
               "0.063 against 0.100; n = 3 is deliberately not on the step-5 "
               "figure. Item 4 is "
               "the reading: the strongest answer compares RP22 with and without "
               "IPTG -- same strain, inducer only, intrinsic 25 -> 6.3.\n"
               "Thursday's S11 handout items are still yours and their answer "
               "sheet is posted.")

    # 20 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "79 – 80 min", "Next")
    d.title(s, "A circuit that has to decide cannot afford a wobbly middle.")
    d.text(s, "Thursday: the digital abstraction, and its price.",
           M, 2.05, 11, 0.45, size=23, font=HEAD, bold=True, color=MINT)
    d.text(s, "Weiss’s lab stacked repressors one, two and three deep. The switch sharpened, most of it at the second stage — and the noise you met today grew in the transition region.",
           M, 2.62, 11.3, 1.2, size=16, color=WHITE, spacing=1.25)
    d.assignment(s, y=4.30)
    d.notes(s, "Hooshangi 2005 goes out now, required; Daniel 2013 optional, and "
               "the 247 reading. Hooshangi is free on PMC. Daniel is through the "
               "library proxy.\n"
               "Hooshangi's own simulator is a Gillespie (p. 3582), so Thursday "
               "begins with a tool they now have.")

    return d
