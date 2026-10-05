"""Session 12 — Noise and the master equation.

Tuesday 6 October. Session 11 stopped at its slide 18, so this session opens by
finishing it: the sweep step by step (the demonstration PS5 Q5a-b grades, due
Thursday), the n <= 2 wall, and delay (T30, also owed to the midterm).
Potvin-Trottier is the bridge -- a paper about removing noise sources one at a
time from a circuit our deterministic model says is fine.

Then the session proper, artifact first: Elowitz 2002's two colors in one
cell; the master equation for birth-death, derived to the Poisson; bursting;
Gillespie derived and live-coded; and T17 -- negative autoregulation against a
constitutive gene at matched mean, with Becskei & Serrano 2000 as the
measurement.

REBUILT 5 OCTOBER 2026 against Adam's slide-by-slide review of the first
build. His summary was the governing instruction: "this derivation is a bit
opaque for this class. We need to be VERY tutorial here." What changed:

  - the bridge is three surfaces, not one: the two Potvin-Trottier movies
    (original against repaired), the four repairs with the mechanism of each,
    and WHY the fourth one worked -- a relaxation oscillator whose period is a
    decay time, so the clock waits on the last few molecules. That last surface
    is the paper's actual argument and it was missing.
  - the two-colour scatter is now SHOWN, with its two directions unlabelled,
    BEFORE the room is asked which direction their answers move a point in.
  - sigma, eta and Fano get a surface of their own before any of them is used.
  - the decomposition is derived (why the cross term dies) rather than asserted.
  - the master equation is two runs, seven steps and five, with the step from
    J_0 = 0 to the Poisson expanded from one line into four.
  - bursting and Gillespie are runs: where b comes from, and why the waiting
    time is exponential rather than anything else.
  - the linear-noise rule is named, sourced and checked, and "return rate" is
    defined before it is used.
  - Becskei is two surfaces: the four constructs drawn, then the fact that
    their "stability" IS our return rate -- so their twofold is g = 1, which
    predicts sqrt(2) against a measured threefold. The gap is stated, not
    papered over.

Paid for inside 80 minutes by one minute each off the goals, delay and
live-code segments. Student working time is unchanged at 21 minutes.

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
    d.header(s, "5 – 7 min", "Where we are  ·  what you'll be able to answer")
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
    d.header(s, "7 – 12 min", "Finishing Thursday  ·  T29")
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
    d.header(s, "7 – 12 min", "Finishing Thursday  ·  the design space")
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
    d.header(s, "12 – 14 min", "Finishing Thursday  ·  T30")
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

    # 7 BRIDGE A — THE TWO MOVIES ---------------------------------------------
    s = d.light()
    d.header(s, "14 – 17 min", "Thursday’s reading  ·  the bridge to today")
    d.title(s, "The same circuit, before and after")
    # The two clips have different aspect ratios (468x146 and 932x364), and
    # `movie` letterboxes inside the box it is given, so the boxes are sized to
    # put BOTH video bottoms on y = 4.30 and both captions on the same line.
    d.text(s, "BEFORE  —  the original repressilator", M, 1.60, 5.90, 0.32,
           size=17, font=HEAD, bold=True, color=RED, align="c")
    d.text(s, "AFTER  —  four repairs later", 6.75, 1.60, 5.90, 0.32,
           size=17, font=HEAD, bold=True, color=TEAL, align="c")
    d.paper_movie(s, "potvintrottier2016_s2", M, 2.46, 5.90, 1.84,
                  "Nature 2016, Supplementary Movie 2",
                  "NDL332: it oscillates, and it loses the beat")
    d.paper_movie(s, "potvintrottier2016_s6", 6.75, 2.00, 5.90, 2.30,
                  "Nature 2016, Supplementary Movie 6",
                  "LPT117: red → green → blue, generation after generation")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.20, W - 2 * M, 1.12, fill=WASH, line=RED)
    d.text(s, "Same topology. Same three repressors. Same ODE — and our ODE gives one trajectory, run it a thousand times. Everything that separates these two movies is invisible to the model you have.",
           M + 0.18, 5.30, W - 2 * M - 0.36, 0.94, size=16, bold=True, color=INK)
    d.assigned_on(M, 6.78, 9.0, s, key="potvintrottier2016",
                  prefix="Potvin-Trottier — you were to read it for Thursday, and we did not reach it")
    d.notes(s, "Play both, left then right, and say nothing over them. Ten "
               "seconds each is enough: the left one wanders, the right one "
               "keeps a rhythm you can count out loud.\n"
               "The left movie is Elowitz & Leibler's original circuit, which "
               "is session 11's circuit -- the one whose stability boundary the "
               "room swept on Thursday. Our analysis said it oscillates, and it "
               "does. It says nothing at all about the difference on the screen.\n"
               "If the movies are not on this machine: Fig. 1d is on the next "
               "surface and carries the same contrast in traces. The download "
               "URLs and the ffmpeg line are in decks/paper_movies.yaml.\n"
               "The red box is the hand-off, and it is the honest version of "
               "it: this is not a model that is slightly wrong. It is a model "
               "with no variable in which the difference could be expressed.")

    # 8 BRIDGE B — THE FOUR REPAIRS -------------------------------------------
    s = d.light()
    d.header(s, "14 – 17 min", "Thursday’s reading  ·  the bridge to today")
    d.title(s, "Four repairs, and only the fourth fixed the clock")
    d.paper_figure(s, "potvintrottier2016_fig1d", M, 1.68, 4.55, 3.05,
                   "Potvin-Trottier 2016, Fig. 1d",
                   "traces, before and after the reporter repairs")
    d.rows(s, [
        ("Reporter to the low-copy plasmid", "A high-copy ColE1 vector replicates sloppily and its copy number wanders. Scatter 78% → 36%.", TEAL),
        ("Tag off the reporter", "Reporter and repressors shared one protease: it was changing what it measured. Period 2.4 → 5.7 gen.", TEAL),
        ("Tags off the repressors", "They now leave only by dilution. Period ~10 gen — and the period noise barely moved.", AMBER),
        ("The TetR sponge, put back", "Sites that soak up the last few TetR. Period ~14 generations, drift 14% per period.", RED)],
        top=1.70, bottom=6.40, side=False, pad=0.02, gap=0.07,
        left=5.55, right=12.63, label_color=INK, numbered=True)
    d.notes(s, "The detective story, and the shape of it is the lesson: the two "
               "obvious repairs worked on the AMPLITUDE, the third was predicted "
               "to fix the PERIOD and did not, and the fourth came from measuring "
               "where in the cycle the noise actually was.\n"
               "Repairs 1 and 2 are two different mechanisms and the numbers "
               "belong to them separately. 78% -> 36% is the plasmid move, and "
               "its cause is slow copy-number drift of a ColE1 vector (p. 2, "
               "ref. 24). The protease story is the SECOND repair, and its "
               "number is the period going from ~2.4 to ~5.7 generations. "
               "Their own surprise is worth one sentence: competition was "
               "predicted to slow ssrA degradation and instead ACCELERATED it "
               "(Extended Data Fig. 3).\n"
               "Repair 3 is the one that should unsettle the room. Removing "
               "degradation is the textbook move -- it is what makes the protein "
               "half-life long and the circuit slow -- and the period noise did "
               "not care.\n"
               "The sponge is a re-introduction, not an invention: the high-copy "
               "reporter plasmid they removed in repair 1 already carried TetR "
               "sites. Sponges for CI and LacI did almost nothing (Extended Data "
               "Fig. 7d), which is the control that makes the TetR result mean "
               "something. Their abstract's 'not by adding control loops' is "
               "true -- a sponge is not a loop -- but not the whole story.\n"
               "WHY the sponge works is the next surface, and it is the reason "
               "this paper is the bridge rather than an anecdote.")

    # 9 BRIDGE C — WHY THE LAST FEW MOLECULES SET THE CLOCK -------------------
    s = d.light()
    d.header(s, "17 – 20 min", "Thursday’s reading  ·  why the fourth repair worked")
    d.title(s, "The clock is a stopwatch on a decaying protein")
    d.rows(s, [
        ("Not a harmonic oscillator", "In single cells the traces are sawteeth: a build-up, then almost pure dilution (their Box 1)."),
        ("So the period is a decay time", "How long TetR takes to fall from its peak N to the threshold S. About ln(N/S) half-lives."),
        ("Amplitude noise barely matters", "Double N and you add ONE half-life — which is why repairs 1 and 2 left the period alone."),
        ("The last few molecules do", "Near S the count is a handful, and a handful of random departures takes a wildly variable time."),
        ("Raise S, and it stops waiting", "That is all a sponge does. There is an optimal S (Box 1).")],
        top=1.82, bottom=5.96, label_w=3.95, gap=0.07)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.08, W - 2 * M, 0.82, fill=WASH, line=RED)
    d.text(s, "“The last few molecules” is a count, not a concentration. x(t) cannot be a handful. For the next hour, n can.",
           M + 0.18, 6.16, W - 2 * M - 0.36, 0.66, size=17, bold=True, color=INK)
    d.notes(s, "This is the surface Potvin-Trottier is assigned FOR, and the one "
               "that was missing. Without it the paper is a list of four fixes "
               "and the sponge is a trick; with it the paper is an argument about "
               "where variance lives in a first-order decay, which is today's "
               "subject arriving a half-hour early.\n"
               "Row 3 is the one to dwell on, because it explains a NEGATIVE "
               "result. Their Box 1: the decay time depends on ln(N/S), so a "
               "twofold error in the peak costs one half-life out of the ten or "
               "so in a period. Amplitude noise is logarithmically damped. That "
               "is why two successful repairs moved the amplitude scatter from "
               "78% to 36% and the period noise hardly at all.\n"
               "Row 4, if asked for the mechanism now: a first-order decay from "
               "N to S is a sum of waiting times, and the waits get longer as "
               "the count falls, because the departure rate is proportional to "
               "the count. The last few terms are the longest AND the most "
               "variable, so they dominate the variance of the total (Box 1, "
               "SI 4.2.2). Promise the room the tool for that today and move; "
               "the master equation is the honest version of this sentence.\n"
               "Row 5: they measured S from partitioning errors at cell division "
               "and found derepression happening at an extremely low threshold "
               "(SI 3.5). The optimum S_opt minimises the CV of the decay time; "
               "raising N helps only if S is already above it (Extended Data "
               "Fig. 4e). Do not derive this -- name it as a design variable and "
               "say the paper does the calculation.")

    # 10 THE ARTIFACT — ELOWITZ 2002 ------------------------------------------
    s = d.light()
    d.header(s, "20 – 23 min", "The artifact")
    d.title(s, "Elowitz et al., Science 2002 — two colors, one cell")
    d.rows(s, [
        ("The construct", "One promoter, two copies in the chromosome: one drives CFP, one YFP."),
        ("Held equal", "Same cell; loci equidistant from, and on opposite sides of, the origin."),
        ("Measured", "Both colors in every cell. Green CFP and red YFP, merged."),
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

    # 11 ARGUE ----------------------------------------------------------------
    s = d.dark()
    d.header(s, "23 – 29 min", "Argue it out  ·  groups of 3–4")
    d.title(s, "Same promoter, same cell. Why are the colors different?")
    d.image(s, FIG + "s12_scatter_axes.png", 8.05, 1.74, 4.55, 3.95)
    d.text(s, "One point per cell: its CFP across, its YFP up. The dashed line is where the two agree.",
           8.05, 5.78, 4.55, 0.56, size=13, italic=True, color=MINT)
    d.rows(s, [
        ("Name two things that would make BOTH colors brighter in one cell than its neighbour. Then one thing that would make one brighter and not the other.", None),
        ("Which of your answers moves a point along A, and which along B? Then say what A and B deserve to be called.", None),
        ("Repress both promoters until the cells make 3% as much protein. Which spread grows, and why?", None)],
        top=2.00, bottom=6.40, side=False, numbered=True, right=7.75,
        label_role="emphasis", label_color=WHITE)
    d.foot(s, "Question 3 is a prediction. Table 1 has the answer, and we read it in four minutes.")
    d.notes(s, "Q1, both brighter: more polymerase or ribosomes, a bigger cell, a "
               "different point in the cell cycle, more of a shared regulator. "
               "One and not the other: which polymerase happened to arrive, when "
               "an mRNA happened to decay -- events at that gene.\n"
               "Q2: A is the diagonal and it is the SHARED causes; B is across "
               "it and it is the PRIVATE ones. The figure is deliberately "
               "unlabelled -- the room names A and B, and then the paper's own "
               "words arrive two surfaces later and agree with them.\n"
               "Q3: the intrinsic part grows because the counts are smaller. "
               "Most of the room will not have the reason yet; the master "
               "equation gives it fifteen minutes later. Extrinsic also grows, about 5-fold, and the "
               "paper's reason is cell-to-cell variation in LacI (p. 1184).")

    # 12 THE VOCABULARY — σ, η, FANO ------------------------------------------
    s = d.light()
    d.header(s, "29 – 31 min", "Before any of them is used  ·  T33")
    d.title(s, "Three numbers off one histogram")
    d.image(s, FIG + "s12_noise_vocab.png", M, 1.70, 5.30, 3.90)
    d.rows(s, [
        ("σ — the spread", "Units of n: here 6.3. Alone it says nothing — 6 is catastrophic at a mean of 10, invisible at 10,000.", TEAL),
        ("η = σ/⟨n⟩ — the CV", "Dimensionless, here 0.159. What you compare across genes and papers. Becskei calls it V_{c}.", AMBER),
        ("Fano = σ^{2}/⟨n⟩", "A ratio to a standard: pure chance gives exactly 1. Below 1 something controls the count, above 1 something worsens it.", RED),
        ("One relation, not three", "η^{2} = Fano/⟨n⟩. Say which one you mean.", INK)],
        top=1.64, bottom=6.46, side=False, pad=0.02, gap=0.07,
        left=6.15, right=12.63, label_color=INK)
    d.notes(s, "Adam's review of the built deck, 5 October: sigma, eta and Fano "
               "were being used across four surfaces without ever being "
               "separated. This surface exists to separate them, and it comes "
               "BEFORE the first one is used rather than after.\n"
               "The picture is one simulated gene, k = 40, gamma = 1, seed 3: "
               "mean 40.0, sigma 6.3, eta 0.159, Fano 1.01. Check 1/sqrt(40) = "
               "0.158 against the eta on the title out loud -- that is the law "
               "they will derive in eight minutes, already true on the screen.\n"
               "The question that separates them, and it is worth asking: WHICH "
               "ONE tells you whether a gene is well controlled? Fano, because "
               "it has a standard to compare against. Eta tells you whether the "
               "noise matters for the job, which is a different question with a "
               "different answer. A gene with Fano 0.3 and eta 0.5 is tightly "
               "controlled AND far too noisy to use.\n"
               "Fano's units bother careful students and they are right to be "
               "bothered: sigma^2/<n> is a count, not a pure number. It is a "
               "ratio to the Poisson variance, which happens to equal the mean. "
               "Say that rather than waving it away.\n"
               "V_c appears again at the Becskei surface, where it is the only "
               "quantity on their axis.")

    # 13 SORTED ---------------------------------------------------------------
    s = d.light()
    d.header(s, "31 – 33 min", "Your answers, sorted  ·  T34")
    d.title(s, "Across the diagonal: the gene. Along it: the cell.")
    d.paper_figure(s, "elowitz2002_fig3a", M, 1.62, 5.15, 3.30,
                   "Elowitz et al. 2002, Fig. 3A", "M22 (quiet) and D22 (noisy), one point per cell")
    d.rows(s, [
        ("Your B — intrinsic, η_{int}", "How much two copies in ONE cell differ: private events move a point across the diagonal.", TEAL),
        ("Your A — extrinsic, η_{ext}", "How much cells differ in what both share: shared causes slide a point along it.", AMBER),
        ("Both are an η", "Each is a σ over a mean.", INK)],
        top=1.70, bottom=5.02, side=False, pad=0.02, gap=0.08,
        left=6.10, right=12.63, label_color=INK)
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
               "state than at one (p. 1186). M22 is at intensity 1, so it is not "
               "the comparison to make here.\n"
               "The estimators, if asked (Swain et al. 2002): eta_int^2 = "
               "<(c1-c2)^2>/(2<c1><c2>), eta_ext^2 = (<c1 c2> - <c1><c2>)/"
               "(<c1><c2>). They are what produced the numbers on our plot.\n"
               "figures/build/s12_two_color.png is our own version of Fig. 3A "
               "(a simulated M22-like and RP22-like strain, with the Swain "
               "estimators printed on it); it goes in the notebook rather than "
               "on this surface, where it was too small to read.")

    # 14 RUN — WHY THEY ADD AS SQUARES ----------------------------------------
    d.derivation_fig(
        "33 – 35 min", "Built one line at a time",
        "Why do the two add as squares?",
        [("Split one cell’s deviation in two",
          "c_{1} = m(1 + ε + δ_{1}) ,   c_{2} = m(1 + ε + δ_{2})",
          "ε is what the CELL did — both colors feel it. δ_{i} is what happened at copy i, and only copy i"),
         ("The cross term averages away",
          "⟨ε δ_{i}⟩ = 0",
          "fix the cell, and δ_{i} is still as likely up as down: ⟨δ_{i} | ε⟩ = 0. Multiply by ε and average again"),
         ("So the cross term dies",
          "Var(ε + δ) = Var(ε) + Var(δ) + 2⟨εδ⟩",
          "the last term is zero. That — and only that — is why it is squares and not a plain sum"),
         ("Divide by the mean squared",
          "η_{tot}^{2} = η_{ext}^{2} + η_{int}^{2}",
          "M22: 5.5² + 5.4² = 59.4, and √59.4 = 7.7, which is the third column of Table 1")],
        [FIG + "s12_squares_ext.png", FIG + "s12_squares_int.png", None,
         FIG + "s12_squares_both.png"],
        closing="Squares mean the larger one wins. Halve the smaller and almost nothing moves.",
        board="η_{tot}^{2} = η_{int}^{2} + η_{ext}^{2}   ⇐   ⟨εδ⟩ = 0",
        note=("Adam's review, 5 October: the decomposition was asserted. Why "
              "squares, and why does it matter.\n"
              "WHY SQUARES is step 2 and it is the only real content: "
              "independent contributions add in variance, not in standard "
              "deviation, because the cross term vanishes. Everything else is "
              "bookkeeping. If anyone has met error propagation in a lab "
              "course, this is the same theorem and worth saying so.\n"
              "DO NOT SAY the two are independent, because they are not: a cell "
              "running hot has a larger delta in absolute molecules, so the "
              "SIZE of the private deviation depends on the shared one. What is "
              "needed is weaker and is all step 2 claims -- that with the cell "
              "held fixed the private deviation is still as likely up as down. "
              "Uncorrelated is enough to kill the cross term; independence is "
              "not available and is not required. A sharp student will push on "
              "this and should be told they are right.\n"
              "WHY IT MATTERS is the closing line, and it deserves a number. "
              "RP22 reads 25 intrinsic, 33 extrinsic, 41 total. Remove the "
              "intrinsic noise ENTIRELY -- perfect transcription, infinite "
              "copies -- and the total goes 41 -> 33, an 18% improvement for a "
              "biologically impossible intervention. Chasing the smaller term "
              "is the commonest way to waste a year, and the decomposition is "
              "what tells you which term is smaller BEFORE you start.\n"
              "The two left panels are the extreme cases, simulated: shared "
              "cause only puts every point exactly on the diagonal (eta_int "
              "0.000); private cause only gives a round blob (eta_int 0.090 at "
              "mean 120, against 1/sqrt(120) = 0.091). The third panel is both "
              "at once and looks like the paper's.\n"
              "The step-1 notation is Elowitz's, and the estimators that turn "
              "it into the numbers are in Swain, Elowitz & Siggia (PNAS 2002) "
              "rather than in the assigned paper."))

    # 15 THE OBJECT — COUNTS, EVENTS, RATES -----------------------------------
    s = d.light()
    d.header(s, "35 – 37 min", "Before the model  ·  what a count does")
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

    # 16 RUN — THE MASTER EQUATION, BUILT -------------------------------------
    d.derivation_fig(
        "37 – 42 min", "Built one line at a time",
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
          "births arriving INTO n from below, minus deaths leaving back down. Net traffic up across the gap"),
         ("The master equation, rewritten",
          "dP_{n}/dt = J_{n} - J_{n+1}",
          "what flows into rung n from below, minus what flows out of it above. Expand it: step 4, term for term"),
         ("Steady state makes every J equal",
          "dP_{n}/dt = 0  ⇒  J_{n} = J_{n+1} = … = J",
          "one common value for the whole infinite ladder. We do not yet know what J is — but one rung will tell us")],
        [FIG + "s12_bd_traj.png", None, None, None, None, None, None],
        closing="An infinite ladder of equations — and one rung will collapse it.",
        board="dP_{n}/dt = J_{n} − J_{n+1},   J_{n} = k P_{n-1} − γn P_{n}",
        note=("T31, part one of two: BUILDING the equation. Adam's review, "
              "5 October -- the old run put fourteen moves on one surface and "
              "the jump from J_0 = 0 to the Poisson happened in a single line. "
              "It is now two runs with a breath between them, and the break is "
              "deliberate: everything up to here is setting the problem up, and "
              "everything after it is solving it.\n"
              "THE SPINE, if the room loses the thread: an infinite set of "
              "equations is about to be turned into ONE small one, and the thing "
              "that does it is a boundary. Say that before step 5 and again at "
              "the start of part two.\n"
              "Step 6 is worth doing on the board rather than reading: expand "
              "J_n - J_{n+1} and show it reproduces step 4 term for term. The "
              "biologists need to see it is the same equation rewritten, not a "
              "new one. Thirty seconds, and it buys the whole of part two.\n"
              "Step 7 leaves them with an unknown constant J on purpose. Ask "
              "the room what could possibly pin it down before turning the "
              "surface; someone will say 'the end of the ladder'.\n"
              "The left panel is our simulator: one cell's count wandering, "
              "k = 10, gamma = 1. It is the thing the equation is about."))

    # 17 RUN — THE MASTER EQUATION, SOLVED ------------------------------------
    d.derivation_fig(
        "42 – 47 min", "Built one line at a time",
        "Now solve it: climb down the ladder",
        [("The bottom rung carries nothing",
          "J_{0} = k P_{-1} - 0 = 0 ,   so  J = 0",
          "there is no n = -1 to be born from, and no molecule at n = 0 to die. One zero at the bottom zeroes every rung"),
         ("Which leaves one small equation",
          "k P_{n-1} = γ n P_{n}",
          "births up across the gap exactly balance deaths back down, rung by rung. The infinite ladder is now a recursion"),
         ("Walk it down to the bottom",
          "P_{n} = (k/γn) P_{n-1} = P_{0}(k/γ)^{n}/n!",
          "P_{1} = (k/γ)P_{0}; P_{2} = (k/γ)/2 · P_{1}; the n! is the 1, 2, 3, … you divide by on the way"),
         ("Fix P_{0} by making them sum to 1",
          "Σ(k/γ)^{n}/n! = e^{k/γ}  ⇒  P_{0} = e^{-k/γ}",
          "that sum is the series for e. The answer is a Poisson with mean k/γ — T31, solved"),
         ("Read the noise off it",
          "⟨n⟩ = σ^{2} = k/γ  ⇒  Fano = 1 ,  η^{2} = 1/⟨n⟩",
          "a Poisson’s variance equals its mean. The floor for an unregulated gene")],
        [None, None, None, FIG + "s12_bd_hist.png", None],
        closing="Halve the count and η² doubles. Only more molecules, or feedback, fixes that.",
        board="J_{n} = k P_{n-1} − γn P_{n} = 0   ⇒   Poisson,  η^{2} = 1/⟨n⟩",
        note=("T31, twelve steps. Adam's review, 5 October: the old version "
              "went from 'J_0 = 0' straight to the Poisson in one surface, and "
              "that jump is now steps 7 to 11.\n"
              "THE SPINE OF THE ARGUMENT, if the room loses the thread: an "
              "infinite set of equations is turned into ONE small one, and the "
              "thing that does it is a boundary. Steady state makes all the "
              "fluxes equal; the bottom of the ladder says what that common "
              "value is; it is zero. Say it that way before step 5 and again "
              "after step 9.\n"
              "Step 6 is worth doing on the board rather than reading: expand "
              "J_n - J_{n+1} and show it reproduces step 4 term for term. The "
              "biologists need to see it is the same equation rewritten, not a "
              "new one. Thirty seconds, and it buys steps 7 and 8.\n"
              "Step 8: both halves of J_0 vanish for different reasons and it is "
              "worth naming both. There is no state n = -1 to be born from, so "
              "the birth term has nothing to act on; and at n = 0 there is no "
              "molecule to die, so gamma times zero. Either alone is enough.\n"
              "Step 9 is where the room should relax: the infinite ladder is "
              "gone and what is left is a recursion a first-year could solve. "
              "This is also the one line that stops working for almost any other "
              "network, which is why Gillespie exists and is next.\n"
              "Step 10: write P_1, P_2, P_3 out longhand and let the factorial "
              "appear rather than announcing it.\n"
              "IF ASKED where the variance comes from without quoting the "
              "Poisson -- and it is the best question in the hour -- the moment "
              "method answers it. Multiply the master equation by n and sum over "
              "all n: the <n^2> terms cancel between the birth and death sums "
              "and you are left with d<n>/dt = k - gamma<n>, which is the ODE "
              "from session 5, recovered as a statement about an average. Do the "
              "same with n^2 and the <n^3> terms cancel; at steady state "
              "2 gamma <n^2> = 2k<n> + k + gamma<n>, so <n^2> = (k/gamma)^2 + "
              "k/gamma and sigma^2 = k/gamma. That the hierarchy CLOSES is "
              "special to a LINEAR birth-death; for anything nonlinear it does "
              "not, which is the honest reason the feedback result later has to "
              "borrow an approximation. It is on the answer sheet.\n"
              "Step 14 against the reading: Elowitz fit eta_int^2 ~ c1/m + c2 "
              "(Fig. 3B caption). The c1/m term is this 1/<n>. The floor c2 is "
              "not, and that is a fair question to leave open. Their recA result "
              "points at transient copy-number differences (p. 1186); that this "
              "sets c2 is our inference, not their claim. The fit is in the "
              "Fig. 3B caption, p. 1185.\n"
              "The right panel is our simulator, not the formula: mean 9.96, "
              "variance 9.92.\n"
              "LEDGER: eta^2 = 1/<n> for an unregulated gene."))

    # 18 RUN — BURSTING, T35 --------------------------------------------------
    d.derivation_fig(
        "47 – 50 min", "Built one line at a time",
        "Where does the Poisson floor break?",
        [("Proteins do not come from DNA",
          "two stages:  DNA → mRNA → protein",
          "each with its own rate and its own decay: k_{m}, γ_{m}, k_{p}, γ_{p}. The last derivation assumed ONE stage — that is the assumption to break"),
         ("One mRNA delivers a lump",
          "b = k_{p}/γ_{m}  proteins before it dies",
          "it lives about 1/γ_{m} and makes protein at k_{p}. The BURST SIZE — and it is a design parameter, set by the RBS"),
         ("The mean cannot see the lump",
          "⟨p⟩ = (k_{m}/γ_{m})(k_{p}/γ_{p}) = (k_{m}/γ_{p})·b",
          "only the product appears. Halve k_{m} and double b: identical mean, and two different circuits"),
         ("The variance can",
          "Fano ≈ 1 + b",
          "proteins now arrive b at a time. One lump of b moves the count b times as far as one molecule would, and the variance follows the jump"),
         ("Exactly, and checked",
          "Fano = 1 + k_{p}/(γ_{m} + γ_{p})",
          "T35, stated not derived. b = 1 and b = 10 at mean 50: 1.91 and 10.09 exact, 1.86 and 10.32 simulated")],
        [None, FIG + "s12_burst_traj.png", None, None,
         FIG + "s12_burst_hist.png"],
        closing="At a fixed mean, a strong promoter with a weak RBS is quieter.",
        board="b = k_{p}/γ_{m} ,   Fano ≈ 1 + b",
        note=("T35. Adam's review, 5 October: the old single surface produced "
              "four parameters and a formula with nothing between them. The "
              "model is now built before it is used, and where the stated "
              "result sits is marked.\n"
              "Step 1 is the honest framing and it matters: this is not a new "
              "subject, it is the last derivation with its first assumption "
              "removed. Proteins arriving one at a time was never stated as an "
              "assumption, which is exactly why it is worth naming now.\n"
              "Step 2: b is the number of proteins per transcript, and the room "
              "should recognise it as the RBS. Strictly each mRNA emits a "
              "protein with probability k_p/(k_p + gamma_m) at each step and "
              "dies otherwise, so the burst size is geometric with mean "
              "k_p/gamma_m, not a fixed lump. The mean is what step 2 needs; "
              "the geometric tail is what makes the exact answer 1 + b rather "
              "than something smaller.\n"
              "Step 4 is the intuition and step 5 is the provenance. The full "
              "result: for production in Poisson-timed bursts of size B with "
              "first-order decay, Fano = 1 + (<B^2> - <B>)/(2<B>); for B "
              "geometric with mean b that is exactly 1 + b. The two-stage "
              "version with a finite mRNA lifetime gives 1 + k_p/(gamma_m + "
              "gamma_p), which is Thattai & van Oudenaarden 2001 (ref. 17 of "
              "Elowitz). We state it and check it rather than deriving it; "
              "deriving it needs the moment method on a two-species master "
              "equation, which is a problem set, not a surface.\n"
              "The correction is not cosmetic at these parameters: 1 + b would "
              "say 11 and the exact answer is 10.09, because the mRNA does not "
              "die the instant it is made. It is on the answer sheet.\n"
              "Both runs have mean 50: k_m = 50, gamma_m = 10, k_p = 10 against "
              "k_m = 5, gamma_m = 10, k_p = 100, both with gamma_p = 1. The "
              "design rule is why a promoter library and an RBS library that "
              "reach the same expression level are not interchangeable."))

    # 19 RUN — GILLESPIE, THE TWO DRAWS ---------------------------------------
    d.derivation_fig(
        "50 – 54 min", "Built one line at a time",
        "How do you simulate one cell exactly?",
        [("Add up every rate",
          "a_{0} = Σ a_{j} ;   birth–death: a_{0} = k + γn",
          "the chance per unit time that SOMETHING happens. While nothing does, the counts do not change — so a_{0} does not either"),
         ("Chop the wait into slivers",
          "P(nothing in one dt) = 1 - a_{0}dt",
          "and every sliver is the SAME lottery, whatever has gone before. Waiting does not make the next event more likely"),
         ("Multiply the slivers",
          "P(none in τ) = (1 - a_{0}dt)^{τ/dt} → e^{-a_{0}τ}",
          "the same limit as compound interest, and the reason the wait is exponential rather than anything else"),
         ("Turn that into a distribution",
          "P(τ ≤ T) = 1 - e^{-a_{0}T}",
          "if it has not happened by τ with probability e^{-a_{0}τ}, it HAS happened with one minus that. A CDF, rising from 0 to 1"),
         ("Draw a uniform, and invert",
          "u_{1} = 1 - e^{-a_{0}τ}  ⇒  τ = -ln(u_{1})/a_{0}",
          "WHEN. Solve for τ; 1 - u is uniform if u is, so either sign of the name works. Divide by a_{0} — never multiply"),
         ("Then draw which",
          "pick reaction j with probability a_{j}/a_{0}",
          "WHICH. Line up the a_{j} end to end and drop u_{2}·a_{0} on the line"),
         ("Fire it, and go again",
          "t ← t + τ ,   x ← x + stoich_{j}",
          "then recompute every a: the rates changed because the count did")],
        [FIG + "s12_ssa_anatomy_col.png", None, None, None, None, None, None],
        closing="Two random numbers per event, and no approximation anywhere.",
        board="τ = −ln u_{1} / a_{0}   ·   j: a_{j}/a_{0}",
        note=("T32, derived before it is coded. Adam's review, 5 October: the "
              "exponential arrived with no explanation. Steps 2 to 4 are that "
              "explanation.\n"
              "THE SENTENCE THAT CARRIES IT, at step 2: between events nothing "
              "about the system changes, so the chance of an event in the next "
              "instant is the same instant after instant. A process that forgets "
              "how long it has already waited can only have an exponential "
              "waiting time -- that is the whole content, and it is why the "
              "exponential is not a modelling choice here but a consequence. "
              "Anyone who has met radioactive decay has met it; a nucleus does "
              "not age.\n"
              "Step 3 at the board: (1 - a0 dt)^(tau/dt) as dt -> 0. Write it "
              "next to (1 + 1/m)^m -> e and let them see it is one limit.\n"
              "Step 4 is the step that was missing and it is pure bookkeeping: "
              "survival to a CDF. Worth doing because step 5 is meaningless "
              "without it -- you cannot invert something you have not written "
              "as a CDF.\n"
              "Step 5: inverse-transform sampling, and this is the line students "
              "most often get wrong in code. Dividing by a0 versus multiplying "
              "gives a plausible-looking trajectory with every timescale "
              "inverted. The sign convention also confuses: -ln(u)/a0 and "
              "-ln(1-u)/a0 are both correct because u and 1-u are both uniform "
              "on (0,1), and our code uses the first.\n"
              "Step 7: the rates are recomputed every event. That is why it is "
              "exact and why it is slow -- millions of events for a mean of a "
              "few hundred over a long run."))

    # 20 LIVE CODE ------------------------------------------------------------
    s = d.dark()
    d.header(s, "54 – 57 min", "Live code  ·  the editor is the board")
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

    # 21 RUN — T17: NAR AT MATCHED MEAN ---------------------------------------
    d.derivation_fig(
        "57 – 65 min", "Built one line at a time",
        "Does negative feedback make a gene quieter?",
        [("State it so it can be answered",
          "same ⟨x⟩ — which circuit spreads less?",
          "matching the mean is the whole discipline here: otherwise you are comparing a quiet weak gene with a loud strong one"),
         ("Why we have to borrow something",
          "⟨f(x)⟩ ≠ f(⟨x⟩)  for a Hill function",
          "the last derivation closed because birth and death were LINEAR in n. A Hill function is not, and the moment hierarchy never closes"),
         ("Linearise, and borrow a standard result",
          "var = (noise in) / (2 × return rate)",
          "for a count held near x* and kicked about: the Ornstein–Uhlenbeck result, got from van Kampen’s expansion. Imported, not proved"),
         ("What a return rate is",
          "kick it by Δ:  dΔ/dt = -rΔ  ⇒  Δ ~ e^{-rt}",
          "r is that restoring rate. 1/r is how long a fluctuation LASTS before it is pulled back. For a plain gene, r = γ"),
         ("Check the rule where we know the answer",
          "var = 2k/(2γ) = k/γ",
          "constitutive: births and deaths each fire at k per unit time, so noise in = 2k, and r = γ. It returns the Poisson"),
         ("Self-repression: the top line is unchanged",
          "noise in = births + deaths = 2γx",
          "at steady state births = deaths, whatever sets them. Same mean ⇒ same γx ⇒ the SAME event rate. Feedback cannot touch this line"),
         ("What feedback changes is the return",
          "r = γ - f′(x)",
          "f′ < 0: a cell that drifts high makes less, so the pull back is stronger than dilution alone"),
         ("Write it with Thursday’s g",
          "γ - f′ = γ(1 + g),  g = n u^{n}/(1 + u^{n})",
          "g = -x f′/f, using f = γx at steady state; u = x/K. Here n is the cooperativity again, not the count"),
         ("Divide",
          "var = 2γx / 2γ(1+g)  ⇒  Fano = 1/(1+g)",
          "T17. At n = 4, x = K: g = 2, Fano 1/3. At mean 100 the CV falls from 0.100 to 0.058")],
        [FIG + "s12_nar_hist.png", None, None, None, None, None, None, None,
         FIG + "s12_nar_fano.png"],
        closing="Feedback did not remove noise at its source. It shortened each fluctuation.",
        board="Fano = 1/(1 + g),   g = n u^{n}/(1+u^{n})",
        note=("The T17 obligation, recorded in the coverage matrix since 14 "
              "September: a worked comparison at matched mean. This is it. "
              "Adam's review, 5 October: where the rule is borrowed from, what a "
              "return rate is, and why the self-repression step follows. Steps "
              "2 to 6 are those three answers.\n"
              "STEP 2 IS THE ONE THAT EARNS THE BORROWING, and it is worth being "
              "blunt: we did not stop deriving because it got tedious. The "
              "birth-death chain closed because kP_{n-1} and gamma n P_n are "
              "linear in n, so the equation for <n> involved only <n>. Put a "
              "Hill function in and the equation for <x> involves <f(x)>, which "
              "is not f(<x>), and the equation for that involves something "
              "worse. There is no exact answer to read off, for this or for "
              "almost any real circuit.\n"
              "STEP 3's provenance, if asked for a name: the linear noise "
              "approximation, van Kampen's system-size expansion. Expand the "
              "master equation about the deterministic trajectory in powers of "
              "1/sqrt(volume) and the leading term is an Ornstein-Uhlenbeck "
              "process -- a linear restoring force with white noise -- whose "
              "stationary variance is injection over twice the restoring rate. "
              "It is exact for a linear system and an approximation for anything "
              "else, which is why step 5 checks it and the simulation at step 9 "
              "checks it again where it is not exact.\n"
              "STEP 4 is the definition that was missing. Draw it: a fluctuation "
              "is a displacement, the circuit pulls it back, and r is how hard. "
              "1/r is the lifetime of a fluctuation. Two things set the "
              "variance -- how often you are kicked, and how long each kick "
              "survives -- and feedback only touches the second.\n"
              "STEP 5 checks only the constant, not the 1/r dependence, which is "
              "the part feedback actually uses. Say so. The independent test of "
              "the dependence is the Gillespie panel at step 9.\n"
              "STEP 6 is the hinge, and it is where the room usually assumes "
              "something false. The claim is NOT that feedback leaves the event "
              "rate alone in general -- it is that if you retune the promoter so "
              "the two circuits sit at the same mean, then at steady state both "
              "have births = deaths = gamma<x>, so both are being kicked equally "
              "often. The matched mean from step 1 is doing the work. Without "
              "it, the comparison is meaningless.\n"
              "Step 7 connects to retrieval question 3: faster return is "
              "Rosenfeld's faster response. One mechanism, two benefits.\n"
              "The right panel at step 9: Gillespie at x = K for n = 1, 2, 4, 8 "
              "gives 0.666, 0.494, 0.334, 0.204 against 0.667, 0.5, 0.333, 0.2.\n"
              "Limits for the board: protein-only model, no bursts; with bursts "
              "the benefit is smaller (the ConcepTest's numbers). And it is the "
              "INTRINSIC part only. Feedback also buffers slow extrinsic change "
              "in its own rates, and more strongly: from gamma x = f(x), "
              "d ln x*/d ln beta = 1/(1 + g), so a slow wobble in beta reaches x "
              "divided by 1 + g in CV, not by sqrt(1 + g). Elowitz p. 1186: "
              "noise-suppressing mechanisms 'need to respond to both sources'.\n"
              "LEDGER: Fano = 1/(1 + g) at matched mean."))

    # 22 THE MEASUREMENT A — WHAT THEY BUILT ----------------------------------
    s = d.light()
    d.header(s, "65 – 69 min", "The measurement")
    d.title(s, "Becskei & Serrano 2000: one loop, three controls")
    d.image(s, FIG + "s12_becskei_circuits.png", M, 1.62, 6.10, 4.85)
    d.rows(s, [
        ("A is the loop", "TetR–EGFP from a promoter with two tet operators: it represses what makes it.", TEAL),
        ("Three ways to break it", "Repressor off the loop (B). Operator swapped (C). DNA-binding domain crippled (D)."),
        ("Why three", "Each changes one thing. Any one alone could be explained away.", AMBER),
        ("V_{c} = σ / mean", "Their read-out (p. 594): our η, in percent.", RED)],
        top=1.66, bottom=6.46, side=False, pad=0.02, gap=0.07,
        left=6.95, right=12.63, label_color=INK)
    d.notes(s, "Not an assigned reading; it is the measurement T17 asks you to "
               "connect to. Adam's review, 5 October: the circuit was in the "
               "speaker notes and the bar chart's four categories were "
               "undefined on the screen. This surface is the categories.\n"
               "Identities, from their Fig. 3 caption (p. 592): column A the "
               "autoregulatory system; B an EGFP vector under CHROMOSOMAL TetR; "
               "C the operator-replaced system of their Fig. 2c after 1 mM "
               "IPTG -- the tet operator swapped for a lac operator; D the "
               "mutant-repressor system of Fig. 2b, TetR carrying Y42A in the "
               "DNA-binding domain.\n"
               "V_c is worth half a minute because it is the only quantity on "
               "their axis and the room met it twenty minutes ago under another "
               "name. Their Methods: 'V_c is the simple ratio of standard "
               "deviation to mean'. It is eta. They report it as a percentage "
               "and we report it as a fraction, and that is the entire "
               "difference.\n"
               "A fair objection to invite: in B the repressor is still TetR and "
               "still represses the promoter -- what is broken is only the LOOP, "
               "because the repressor's level no longer depends on the "
               "promoter's output. That is the cleanest of the three controls "
               "and it is the one the threefold number comes from.")

    # 23 THE MEASUREMENT B — THEIR STABILITY IS OUR RETURN RATE ---------------
    s = d.light()
    d.header(s, "65 – 69 min", "The measurement")
    d.title(s, "Their “stability” is our return rate")
    d.paper_figure(s, "becskei2000_fig3a", M, 1.66, 4.30, 4.55,
                   "Becskei & Serrano 2000, Fig. 3a",
                   "V_c for A, B, C, D — the four circuits on the last surface")
    d.rows(s, [
        ("Their argument is step 7", "They linearise about the steady state and call it S — the same γ − f′(x). Their S is our return rate r.", TEAL),
        ("“Twofold increase in stability”", "S doubles, so r = 2γ. In step 8, γ(1 + g) = 2γ means g = 1 for their circuit (p. 590).", TEAL),
        ("So we predict √2", "Fano falls by 1 + g = 2, V_{c} by √2 = 1.41. Extrinsic buffering would buy at most 1 + g = 2.", AMBER),
        ("They measured threefold", "V_{c} 6–9% with the loop, about 3× higher at equal mean without it (p. 592). More than our model allows.", RED)],
        top=1.70, bottom=6.48, side=False, pad=0.02, gap=0.07,
        left=5.30, right=12.63, label_color=INK)
    d.notes(s, "THE CROSS-REFERENCE, because it is the point of the surface: "
               "their 'stability' S is not a vague word. Their Methods, p. 590: "
               "'The value of the stability (S) is obtained by the linearization "
               "of the equations around the steady state.' That is the "
               "eigenvalue, which is the return rate, which is step 7 of the "
               "derivation twenty minutes ago. Point at the board line.\n"
               "WHY TWOFOLD IMPLIES TWICE AS FAST: r is defined so a "
               "displacement decays as e^{-rt}. Double r and every fluctuation "
               "-- and every response to a step change -- takes half as long. "
               "Their claim is about the deterministic relaxation; Rosenfeld "
               "2002, which the room read for session 7, measured exactly that "
               "and is the same statement.\n"
               "THE NUMBER THAT FOLLOWS, and it is a correction to an earlier "
               "version of this slide: their twofold is 1 + g = 2, so g = 1, not "
               "2. Our intrinsic result then predicts the CV falling by "
               "sqrt(2) = 1.41, and the extrinsic-buffering bound is 2. The "
               "measured gap is about 3. OUR MODEL DOES NOT ACCOUNT FOR IT, and "
               "that is the honest thing to say rather than reaching for a "
               "factor.\n"
               "What could close it, if asked: bursts (our result assumes "
               "proteins arrive one at a time, and real expression is bursty, "
               "which feedback also damps); plasmid copy number varying between "
               "cells, which feedback compensates -- they measured that "
               "separately, and expression rose only 2.6- and 4.8-fold across a "
               "copy-number range of 3-4, 20-30 and 50-70 (p. 592); and the fact "
               "that their controls are not perfectly matched circuits.\n"
               "Control C was sampled shortly after induction, a transient, so "
               "it is the weaker comparison. Control B is not a transient and is "
               "where the threefold comes from. Their mutant D is not at matched "
               "mean at all -- its relative mean is 38 (Fig. 2b).")

    # 24 CONCEPTEST -----------------------------------------------------------
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

    # 25 FADED SET ------------------------------------------------------------
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

    # 26 FORWARD LINK ---------------------------------------------------------
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
