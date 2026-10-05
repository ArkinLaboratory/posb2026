"""Session 13 — The digital abstraction, and its price.

Thursday 8 October, the last content session before the review and the midterm.

Shape: a measured artifact first (Hooshangi et al. 2005, cascades one to three
repressors deep), then the abstraction derived from a single transfer curve
(gain as a log slope, the two unity-gain thresholds, noise margins), then
signal matching between two real gates (Nielsen et al. 2016, Fig. 2B, with the
fitted parameters from their Table S4), and finally the alternative to the
abstraction (Daniel et al. 2013) with a worked example on how wide a logarithm
a Hill curve can be.

Verified in tests/test_digital.py and figures/s13_digital.py:
    |G| = g (y - y_min)/y with g = n u^n/(1 + u^n)
    n = 2, 100-fold leak ratio, K = 1: x_IL = 1.02, x_IH = 9.80
    same gate driving itself at y_max = 10: NM_L +0.70, NM_H -0.30 decades
    PhlF P1 -> BetI E1 (Table S4): +1.44 / +0.08 ; reverse: -0.73 / +1.10
    Hill log-linear range, slope within 75% of peak: 9^(1/n)-fold

Coverage: T36, T37, T38 (PS6; recognition-only on the midterm).
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks import theme as T
from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session13_Digital"
FIG = "figures/build/"


def build():
    d = Deck("Session 13 — The digital abstraction and its price", session=13)
    _opening(d)
    _artifact(d)
    _abstraction(d)
    _matching(d)
    _price(d)
    _analog(d)
    _close(d)
    return d


def _opening(d):
    s = d.dark()
    d.text(s, "Session 13", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "The digital abstraction, and its price", M, 2.72, 8.3, 1.3,
           size=40, font=HEAD, bold=True, color=WHITE)
    d.text(s, "When a gene may be treated as a switch, when two switches can be wired together, and what that costs",
           M, 4.15, 8.4, 0.8, size=18, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Last content session before Tuesday's review. On the midterm "
               "this session is recognition only; PS6 assesses it with numbers.")

    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions before we start")
    d.rows(s, [
        ("FROM TUESDAY", "An unregulated gene averages 25 molecules. What is η, and what would halve it?", TEAL),
        ("FROM TUESDAY", "Self-repression made a gene quieter at the same mean. What did it change, and what not?", TEAL),
        ("FROM SESSION 9", "The toggle needed cooperativity. What failed at n = 1?", CYAN)],
        top=1.95, bottom=6.30, label_w=2.70, numbered=True, label_role="caption")
    d.foot(s, "Question 3 returns in twenty minutes, with a third job for the same condition.")
    d.notes(s, "Q1: eta = 1/sqrt(25) = 0.2. Halving it takes four times the "
               "molecules, or feedback.\n"
               "Q2: the event rate is gamma x either way. The return rate became "
               "gamma(1 + g).\n"
               "Q3: at n = 1 the nullclines cross once at every alpha. Today the "
               "same n > 1 decides whether a gate can restore a weakened signal.")

    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By 9:30 you should be able to answer")
    for i, (n, lab) in enumerate([("12", "Noise"), ("13", "Digital"),
                                  ("14", "Review"), ("15", "Midterm"),
                                  ("16", "Logic")]):
        x, here = M + i * 2.42, n == "13"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=14, bold=here,
               color=WHITE if here else MUTED, align="c")
    d.rows(s, [
        ("?", "Given a measured transfer curve, what must be true before you may call the gene a switch?", None),
        ("?", "Gate A feeds gate B. How do you decide, with numbers, whether B reads A correctly — and what do you change if not?", None),
        ("?", "What does treating a gene as a switch discard, and when is that the wrong trade?", None)],
        top=2.95, bottom=6.50, label_w=0.50, label_role="emphasis",
        label_color=CYAN)
    d.notes(s, "First question: T36 and T37. Second: T38. Third: Daniel.")


def _artifact(d):
    s = d.light()
    d.header(s, "8 – 12 min", "The artifact")
    d.title(s, "Hooshangi, Thiberge & Weiss, PNAS 2005")
    d.paper_figure(s, "hooshangi2005_fig1", M, 1.62, 6.60, 3.40,
                   "Hooshangi et al. 2005, Fig. 1", "one, two and three repressors deep")
    d.rows(s, [
        ("Input", "aTc binds TetR and takes it off the promoter.", TEAL),
        ("Circuit 1", "TetR ⊣ EYFP", TEAL),
        ("Circuit 2", "TetR ⊣ LacI ⊣ EYFP", TEAL),
        ("Circuit 3", "TetR ⊣ LacI ⊣ CI ⊣ EYFP", TEAL),
        ("Measured", "one plasmid each, 30–50 aTc levels.", AMBER)],
        top=1.70, bottom=5.85, side=False, pad=0.02, gap=0.06,
        left=7.45, right=12.63, label_color=INK)
    d.assigned_on(M, 6.80, 9.0, s)
    d.notes(s, "Free on PMC, assigned Tuesday. Each circuit sits on a single "
               "p15A plasmid so every gene in it has the same copy number "
               "(Methods, p. 3581) -- Elowitz's copy-number worry again.\n"
               "Ron Weiss's lab. He co-taught this course for fifteen years.")

    s = d.light()
    d.header(s, "12 – 15 min", "The artifact  ·  what they measured")
    d.title(s, "Each stage sharpened the switch — the third, barely")
    d.paper_figure(s, "hooshangi2005_fig2a", M, 1.62, 5.30, 4.40,
                   "Hooshangi et al. 2005, Fig. 2A", "mean EYFP against aTc")
    d.rows(s, [
        ("Hill coefficient", "2.3, 7.0, 7.5 for one, two, three stages.", TEAL),
        ("Transition width", "1.75, 0.36, 0.21 µM aTc, low to high.", TEAL),
        ("Simulated", "2.8, 7.5, 11, 29 at depth 1, 2, 3, 7.", MUTED),
        ("Circuit 2 falls", "Circuits 1 and 3 rise with aTc; 2 inverts once more.", AMBER)],
        top=1.70, bottom=5.70, side=False, pad=0.02, gap=0.07,
        left=5.90, right=12.63, label_color=INK)
    d.foot(s, "Numbers from p. 3583. Stage two bought a factor of three in sharpness; stage three bought seven percent.")
    d.notes(s, "The three fitted Hill coefficients, then the diminishing "
               "return. The paper's own candidates for it are on p. 3585: "
               "noise may ultimately limit the gain from adding elements, and "
               "LacI is expressed far above what full repression of cI needs. "
               "Our model adds a third -- gains multiply only where two stages "
               "overlap -- and the next surface shows that on our own gate, not "
               "on theirs.\n"
               "Circuit 2 has one inversion fewer between aTc and EYFP, so its "
               "EYFP falls as aTc rises.")

    s = d.dark()
    d.header(s, "15 – 23 min", "Argue it out  ·  groups of 3–4")
    d.title(s, "Why should stacking repressors sharpen anything?")
    d.rows(s, [
        ("Stage one’s output swings over roughly two decades as aTc rises, and stage two sees that swing as its own input. Argue what stage two does to it, and why that is not simply ‘more of the same’.", None),
        ("Draw the curve you would expect for a fourth and a fifth stage. Where does your drawing stop improving, and what sets that point?", None),
        ("Stage three added almost nothing here. Name a property of stage three’s promoter that would explain it.", None)],
        top=2.05, bottom=6.35, side=False, numbered=True,
        label_role="emphasis", label_color=WHITE)
    d.foot(s, "You have everything you need: a Hill function, and the chain rule.")
    d.notes(s, "Q1: the steep part of stage two sits on the swing of stage one, "
               "so a fractional change in aTc is multiplied twice. Fish for "
               "'multiply', not 'add'.\n"
               "Q2: it stops improving when a stage's steep region no longer "
               "overlaps the previous stage's output range -- the matching "
               "question, two segments early. Also when leak sets the floor.\n"
               "Q3: the honest answers are its threshold sitting off the "
               "previous stage's swing, or its leak. Evidence that leak can "
               "ruin a stage, though about a circuit they discarded rather than "
               "the one they shipped: their FIRST three-stage build used a "
               "mutant lambda promoter whose elevated low output gave an "
               "undesirable transfer curve, so the final design went back to "
               "the original OR1 (p. 3585). For the shipped circuit 3 the paper "
               "offers noise and excess LacI, same page.")

    s = d.light()
    d.header(s, "23 – 26 min", "Your answers, sorted")
    d.title(s, "Gains multiply — where the stages overlap")
    d.image(s, FIG + "s13_cascade.png", M, 1.66, W - 2 * M, 3.00)
    d.rows(s, [
        ("Aligned", "stage two’s steep part sits on stage one’s swing: peak 1.64 → 2.35.", TEAL),
        ("Misaligned", "push stage two’s K up 30-fold: 0.06, flatter than one stage alone.", RED),
        ("So", "not how many stages, but whether each output lands where the next is steep.", AMBER)],
        top=4.80, bottom=6.80, label_w=1.85, gap=0.06)
    d.notes(s, "Our own two-stage model, same gate twice, n = 2. The left panel "
               "is the chain rule made visible: AT EACH INPUT the composite log "
               "slope is the product of the two log slopes.\n"
               "Do not multiply the two PEAK gains. 1.64 x 1.64 = 2.69, and the "
               "measured composite peak is 2.35, because the two peaks sit at "
               "different inputs -- which is the slide's own point about "
               "overlap, in numbers.\n"
               "The right panel is the whole of signal matching in one picture, "
               "and it is the same failure Hooshangi describes on p. 3585.\n"
               "Peak gains are measured off the curves, not asserted.")


def _abstraction(d):
    d.derivation_fig(
        "26 – 38 min", "Built one line at a time",
        "When may you call a gene a switch?",
        [("Write the curve you measured",
          "y = y_{min} + (y_{max} − y_{min})/(1 + (x/K)^{n})",
          "one promoter, one repressor. y_{min} is the leak: no promoter is ever fully off"),
         ("‘Slope’ needs units. Use the log slope",
          "G = d ln y / d ln x",
          "x and y are different molecules, so dy/dx depends on your units. A fractional change does not"),
         ("Differentiate, leak first set to zero",
          "|G| = n u^{n}/(1 + u^{n}) ≡ g ,   u = x/K",
          "Thursday's loop gain, again — and it is below n, approaching it only far past K"),
         ("Can |G| ever exceed 1?",
          "g < 1 everywhere when n ≤ 1",
          "at n = 1, g = u/(1+u) < 1. A non-cooperative gate cannot restore a signal"),
         ("Now put the leak back",
          "|G| = g · (y − y_{min})/y",
          "the leak discounts the gain, and the discount bites hardest where y is near y_{min}"),
         ("If the peak clears 1, it crosses twice",
          "peak |G| > 1  ⇒  x_{IL} and x_{IH} exist",
          "n > 1 is necessary, not sufficient: a big enough leak holds the peak under 1 and there is no switch at all"),
         ("Those two inputs name the levels",
          "y_{OH} = y(x_{IL}) ,   y_{OL} = y(x_{IH})",
          "worst-case outputs. Everything below x_{IL} is LOW, everything above x_{IH} is HIGH"),
         ("A switch, with numbers",
          "n = 2, y_{max}/y_{min} = 100 :  peak |G| = 1.64",
          "x_{IL} = 1.02K, x_{IH} = 9.80K, y_{OH} = 4.95, y_{OL} = 0.20. The gate's whole datasheet")],
        [FIG + "s13_gain_p1.png", None, FIG + "s13_gain_p2.png", FIG + "s13_gain_p3.png",
         FIG + "s13_gain_p2.png", None, FIG + "s13_gain_p4.png", None],
        closing="Four numbers per gate: two input thresholds and two output levels.",
        board="|G| = g·(y − y_{min})/y  ,   peak |G| > 1 ?",
        note=("T36 and T37. Eight steps; the one where something disappears is "
              "step 3, where the Hill algebra collapses to Thursday's g.\n"
              "STEP 2 is a choice and it needs defending. In "
              "electronics gain is dV_out/dV_in and both sides are volts. Here "
              "they are different molecules, so a linear slope changes when you "
              "change units; d ln y/d ln x does not. Daniel et al. call the same "
              "quantity sensitivity (p. 623). For a chain of identical gates in "
              "the same units the two agree about where the restoring region is.\n"
              "STEP 4 is the callback to retrieval question 3. The toggle needed "
              "n > 1 to have two states; the ring needed n > 2 to tick; a gate "
              "needs n > 1 to clean up its input. Three sessions, one condition.\n"
              "STEP 6 has two halves and both matter. The leak is what brings "
              "the gain back down, so an upper threshold exists at all -- ask "
              "why a leak is welcome before saying it. But the leak can also go "
              "too far: at this gate's hundredfold swing the peak clears 1 only "
              "for n above about 1.3, and at n = 2 a tenfold swing has peak "
              "|G| = 1.04 while a fivefold swing has 0.76 and no switch. "
              "posb.digital.thresholds raises rather than returning numbers for "
              "such a gate, and two of Cello's twenty gates are in that class "
              "(next surface but three).\n"
              "LEDGER: x_IL, x_IH, y_OL, y_OH.")
    )


def _matching(d):
    s = d.light()
    d.header(s, "38 – 44 min", "Signal matching  ·  T38")
    d.title(s, "Does gate B read what gate A emits?")
    d.image(s, FIG + "s13_self_match.png", M, 1.60, W - 2 * M, 3.40)
    d.rows(s, [
        ("The test", "NM_{L} = log(x_{IL}/y_{OL}), NM_{H} = log(y_{OH}/x_{IH}).", TEAL),
        ("It fails", "y_{OH} = 4.95 is below x_{IH} = 9.80 K.", RED),
        ("One knob", "a stronger RBS moves both outputs, neither threshold.", GREEN),
        ("⚠ Here", "the output’s RBS is separate from the repressor’s. In Nielsen’s gates it is one RBS, and their thresholds moved with it.", AMBER)],
        top=5.06, bottom=6.95, label_w=1.70, gap=0.04)
    d.notes(s, "T38, and the first half of the worked example. Same gate driving "
               "an identical copy, n = 2, hundred-fold leak ratio.\n"
               "Say the asymmetry plainly: the low side has 0.70 decades to "
               "spare and the high side is 0.30 decades short, so this pair "
               "fails even though both gates are fine on their own. A gate is "
               "not good or bad; a PAIR is matched or not.\n"
               "The RBS argument is the one worth slowing down for. Scaling the "
               "output multiplies y_min and y_max by the same factor, so "
               "(y - y_min)/y is unchanged at every x, so G is unchanged, so "
               "both thresholds are unchanged. Promoter strength and RBS "
               "strength are not interchangeable knobs -- that was Tuesday's "
               "bursting result, and it is a different reason for the same "
               "conclusion.\n"
               "THE WARNING ROW is not a hedge, it is the architecture. Our y is "
               "a reporter with its own RBS, so scaling it cannot touch the "
               "gate's reading. In a repressor chain the output protein IS the "
               "next gate's repressor, so one RBS sets both. Nielsen's "
               "supplement, section I.C: the RBS controlling repressor "
               "expression is one determinant of the threshold of a gate, and "
               "changing it shifted thresholds or eliminated the response "
               "entirely. That is why their library carries several RBS "
               "variants of each repressor rather than one.")

    s = d.light()
    d.header(s, "38 – 44 min", "Signal matching  ·  how much RBS")
    d.title(s, "The window, and what sets its width")
    d.image(s, FIG + "s13_rbs_window.png", M, 1.70, 6.10, 4.40)
    d.rows(s, [
        ("Raise it", "NM_{H} rises, NM_{L} falls.", TEAL),
        ("n = 2", "both positive, ×2.0 to ×5.1: a 2.6-fold window.", TEAL),
        ("n = 4", "×0.55 to ×5.7, 10.3-fold. Sharper matches easier.", CYAN),
        ("n ≤ 1", "no window: no restoring region, nothing to match.", RED),
        ("The move", "take the middle.", AMBER)],
        top=1.62, bottom=6.45, side=False, pad=0.02, gap=0.07,
        left=6.60, right=12.63, label_color=INK)
    d.foot(s, "Equal margins at ×3.16: both +0.20 decades, the most noise this pair survives.")
    d.notes(s, "The geometric middle of the window is where the two margins are "
               "equal, which is the most tolerant choice -- same logic as "
               "centering a trip point.\n"
               "The n comparison is the session's design ledger entry: "
               "cooperativity buys matching tolerance, and Daniel charges for "
               "exactly that at 56.")

    s = d.light()
    d.header(s, "44 – 50 min", "Signal matching  ·  two real gates")
    d.title(s, "Nielsen et al. 2016: PhlF drives BetI, but not the reverse")
    d.paper_figure(s, "nielsen2016_fig2b", M, 1.70, 9.40, 3.35,
                   "Nielsen et al. 2016, Fig. 2B", "the same two gates, in each order")
    d.text(s, "Their caption: the orange gate (PhlF) has a large dynamic range that spans the threshold of the purple gate (BetI). In the reverse order, the gates do not functionally connect.",
           M, 5.52, W - 2 * M, 0.8, size=17, color=BODY)
    d.text(s, "Which side fails — the low or the high — and by how much?",
           M, 6.48, W - 2 * M, 0.5, size=20, bold=True, color=INK)
    d.notes(s, "The artifact for T38. Cello is a design-automation tool that "
               "assigns repressors to the gates of a circuit, and this figure is "
               "why the assignment matters: the same two gates connect in one "
               "order and not the other.\n"
               "The question stays on the screen. The next surface is "
               "their own fitted parameters, and the margins we compute from "
               "them.")

    s = d.light()
    d.header(s, "44 – 50 min", "Signal matching  ·  two real gates")
    d.title(s, "Their four numbers per gate, our arithmetic")
    d.rows(s, [
        ("PhlF → BetI", "+1.44 and +0.08 decades. It connects, and the high side is tight.", GREEN),
        ("BetI → PhlF", "−0.73 on the low side. BetI’s worst-case LOW is 0.12 RPU; PhlF reads LOW below 0.023.", RED),
        ("The repair", "cut BetI’s output 5- to 12-fold, or put a different gate downstream.", AMBER)],
        top=1.95, bottom=4.90, label_w=2.30, gap=0.08)
    d.sources(s, [("PhlF P1:  y_min, y_max, K in RPU — 0.01, 3.9, 0.03 — and n = 4.0",
                   "Nielsen et al. 2016, Table S4"),
                  ("BetI E1:  0.07, 3.8, 0.41 RPU, and n = 2.4",
                   "Nielsen et al. 2016, Table S4")], y=5.15)
    d.foot(s, "Same four numbers per gate as our own example. Their rule is not ours — they ask that the sender’s range span the receiver’s threshold — but on this pair the two agree.")
    d.notes(s, "The numbers are theirs, not ours: "
               "Table S4 of the supplement gives every insulated gate's fitted "
               "y_min, y_max, K and n in RPU. Our own margin arithmetic, run on "
               "their four numbers per gate, agrees with the tick and the cross "
               "in their figure.\n"
               "Their caption says the orange gate has a dynamic range that "
               "spans the purple gate's threshold, and not the reverse. We can "
               "now say WHICH side fails and BY HOW MUCH, which is what a "
               "designer needs.\n"
               "Cello searches assignments of repressors to gates with simulated "
               "annealing, because choosing which gate goes where is NP-complete "
               "(p. aac7341-2). Session 16 is that paper; today is why the "
               "search is necessary at all.\n"
               "WHERE OUR CRITERION IS STRICTER THAN THEIRS, and say it if "
               "anyone pushes: their rule is that the sender's output range "
               "spans the receiver's threshold, which is one threshold and a "
               "range. Ours is two unity-gain points and worst-case levels. On "
               "their twenty gates, TWO -- AmeR F1 and IcaRA I1, both n = 1.4 "
               "with a large leak -- never reach |G| = 1 at all, so our "
               "criterion says they cannot restore a signal, and Cello uses "
               "them in working circuits. A circuit can work without every "
               "stage restoring; what it cannot do is work with every stage "
               "losing. That is the honest scope of today's test.")


def _price(d):
    s = d.light()
    d.header(s, "50 – 56 min", "The price  ·  what the abstraction discards")
    d.title(s, "Three bills, and the paper paid all of them")
    d.paper_figure(s, "hooshangi2005_fig2b", M, 1.68, 4.45, 3.90,
                   "Hooshangi et al. 2005, Fig. 2B", "CV against mean output, circuits 1–3")
    d.rows(s, [
        ("Quiet at both ends", "Far from the transition the CV is the same for all three circuits.", TEAL),
        ("Loud in the middle", "In the transition region it rises with depth: about 0.9, 1.6, 2.7.", RED),
        ("Why", "Their reason, p. 3585: the increasing slope, plus the noise each stage adds.", RED),
        ("Which is to say", "slope is gain. A gate with gain 7 turns a 10 % wobble into 70 %.", AMBER)],
        top=1.70, bottom=6.10, side=False, pad=0.02, gap=0.07,
        left=6.90, right=12.63, label_color=INK)
    d.foot(s, "A gate is only digital at its two ends. In between it is an amplifier, and what it amplifies includes Tuesday’s noise.")
    d.notes(s, "The first of two cost surfaces, and the bridge back to Tuesday. "
               "Read the three peak CVs off the figure rather than asserting "
               "them -- about 0.9, 1.6 and 2.7 for one, two and three stages.\n"
               "The last row is the sentence to land: the sharpening and the "
               "noise amplification are the same number. You cannot buy one "
               "without the other, and that is not a flaw in their build.\n"
               "Their Fig. 2C makes the same point in simulation out to seven "
               "stages, if anyone asks whether it keeps going.")

    s = d.light()
    d.header(s, "50 – 56 min", "The price  ·  what the abstraction discards")
    d.title(s, "And it is slow, and the cells stop agreeing")
    d.paper_figure(s, "hooshangi2005_fig3a", M, 1.68, 4.45, 3.90,
                   "Hooshangi et al. 2005, Fig. 3A", "response after aTc is added")
    d.rows(s, [
        ("Delay", "Circuit 1 settles by 120 min; circuit 3 starts at 140 and settles near 600.", RED),
        ("Why", "each repressor must dilute away before the next stage answers.", RED),
        ("Synchrony", "every stage adds scatter to the switching time.", RED),
        ("Paid back", "circuit 3 ignores aTc pulses under 15 min: a low-pass filter.", GREEN)],
        top=1.70, bottom=6.26, side=False, pad=0.02, gap=0.07,
        left=6.60, right=12.63, label_color=INK)
    d.foot(s, "Fig. 3A, p. 3583; the pulse result p. 3584. Cost or feature, depending on what you are building.")
    d.notes(s, "DELAY: the figure has it. Circuit 1 rises immediately; "
               "circuit 3 is flat for 140 minutes. The cell cycle here is about "
               "45 minutes, so three stages cost roughly three divisions.\n"
               "SYNCHRONY: their Fig. 3B and 3E show the CV spiking DURING a "
               "transition and settling afterwards -- cells cross at different "
               "times. That is fatal for anything developmental, which is their "
               "own conclusion on p. 3585.\n"
               "THE LAST ROW is the honest one and it is why this is not simply "
               "a list of complaints. The same dilution delay that makes the "
               "cascade slow makes it ignore short transients. A filter you did "
               "not design and may well want.")


def _analog(d):
    s = d.light()
    d.header(s, "56 – 60 min", "The alternative")
    d.title(s, "What if you did not want a switch?")
    d.rows(s, [
        ("A switch throws away the middle", "Between x_{IL} and x_{IH} we declared the output meaningless. For a sensor, that region is the measurement.", TEAL),
        ("Hill curves are logarithms — briefly", "On a log axis a Hill function is a straight line, and the straight stretch is narrow.", TEAL),
        ("How narrow?", "Within 75 % of its steepest slope, a Hill function spans 9^{1/n}-fold input: ninefold at n = 1, threefold at n = 2, 1.7-fold at n = 4.", AMBER),
        ("Which is the bill from the last slide, inverted", "The cooperativity that bought you matching tolerance is what costs you measuring range.", RED)],
        top=1.95, bottom=5.95, label_w=4.30, gap=0.08)
    d.foot(s, "The next five surfaces are one answer: Daniel et al. 2013, a circuit built to stay logarithmic where a Hill curve cannot.")
    d.notes(s, "The hinge of the session, and it is one sentence: the same n "
               "appears in both bills with opposite signs.\n"
               "The derivation is on the answer sheet. On a log "
               "axis the slope of u^n/(1+u^n) is n y (1 - y), peaking at y = 1/2; "
               "staying within 75% of that peak means y between 1/4 and 3/4, and "
               "the input ratio between those is 9^(1/n).\n"
               "The small figure is the full version of the two panels the next "
               "run uses, kept here so the claim is visible while it is made.")

    d.derivation_fig(
        "60 – 68 min", "Built one line at a time",
        "How do you widen a logarithm?",
        [("The problem, in one line",
          "log-linear over 9^{1/n}-fold, and no more",
          "saturation at both ends is what ends it: the repressor runs out of inducer, or the DNA runs out of sites"),
         ("Daniel's first move: feed the output back",
          "more AraC made as arabinose rises",
          "positive feedback. The transcription factor rises with the input, so the inducer never saturates it"),
         ("Second move: add a sink for the factor",
          "a high-copy plasmid of sites: the shunt",
          "it holds the free factor down, so the DNA sites never saturate either"),
         ("Together, the curve straightens",
          "output ∝ ln(1 + x) ,  not x/(1 + x)",
          "their fit, Fig. 1d: more than three decades, against a narrow range for the open loop on the same axes"),
         ("The same circuit, made digital again",
          "raise the feedback plasmid's copy number",
          "Fig. 2e: at high copy the curve fits a Hill function over about two decades instead")],
        [FIG + "s13_loglin_p1.png", None, None, FIG + "s13_loglin_p2.png", None],
        closing="One circuit. Analog or digital, set by a plasmid copy number.",
        board="Hill: 9^{1/n}-fold   ·   ln(1+x): three to four decades",
        note=("The analog half as a worked example, per the 4 October decision. "
              "Daniel et al. 2013 is optional reading for 147 and required for "
              "247.\n"
              "STEP 1 is the result from the previous surface, restated as a "
              "design problem: a sensor that must read four decades of inducer "
              "cannot be built from one Hill curve.\n"
              "STEPS 2-3 are the two halves of their PFS motif, and the "
              "mechanism is the same both times: something was saturating, so "
              "they added a process that empties it. Ask the room which "
              "saturation each move removes before saying it.\n"
              "STEP 4: their Fig. 1d is the comparison -- the open-loop control "
              "on the same axes, fitted by x/(1+x), against the PFS circuit "
              "fitted by ln(1+x) over more than three decades. Their LuxR "
              "version reaches nearly four decades at low copy (Fig. 2e).\n"
              "STEP 5 is the one to end on. The same circuit, same parts, "
              "behaves analog or digital-like depending on the copy number of "
              "one plasmid. Digital is not a property of biology; it is a "
              "regime you choose to operate in, and today we paid for it twice.\n"
              "Do not claim they compute with three transcription factors in "
              "general -- the abstract says the adders and ratiometers need no "
              "more than three (Fig. 3). The log circuit itself uses one.")
    )


def _close(d):
    s = d.light()
    d.header(s, "68 – 73 min", "Pose  ·  silent vote  ·  argue  ·  vote again")
    d.title(s, "Gate A feeds gate B. NM_L is +0.70, NM_H is −0.30.")
    for i, (letter, opt) in enumerate([
            ("A", "Strengthen A’s RBS, so A emits more of everything"),
            ("B", "Strengthen B’s RBS"),
            ("C", "Swap B for a gate with the same K but n = 4"),
            ("D", "Put a third, identical gate between them")]):
        y = 2.0 + i * 1.02
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, W - 2 * M, 0.84, fill=CARD, line=RULE, lw=1)
        d.text(s, letter, M + 0.25, y + 0.2, 0.5, 0.4, size=20, font=HEAD,
               bold=True, color=CYAN)
        d.text(s, opt, M + 0.9, y + 0.2, W - 2 * M - 1.2, 0.4, size=16, color=BODY)
    d.foot(s, "Which of these moves an output level, which moves a threshold, and which moves neither?")
    d.notes(s, "Answer: A and C. Computed with posb.digital on the session's "
               "own gate, n = 2, hundred-fold leak ratio.\n"
               "A: ×3 on the sender gives +0.23 and +0.18. Both positive, so it "
               "works -- the sender's levels rise, the receiver's thresholds do "
               "not move.\n"
               "B is the trap, and it is the point of the question. An RBS on "
               "the RECEIVER scales the receiver's own outputs; it does not "
               "touch the receiver's input thresholds, because G is unchanged. "
               "The margins are identical: +0.70 and -0.30. Expect this to "
               "split the room, and let them argue it rather than ruling.\n"
               "C: a sharper receiver has thresholds 0.76 and 4.14 instead of "
               "1.02 and 9.80, so the high side clears: +0.58 and +0.08.\n"
               "D: an identical gate in the middle inherits the same mismatch "
               "and inverts the logic as well. Two wrongs.")

    s = d.light()
    d.header(s, "73 – 79 min", "Worked set  ·  handout  ·  start where you like")
    d.title(s, "Four problems. The scaffolding falls away.")
    for i, (num, k, txt, c) in enumerate([
            ("1", "Fully worked", "n = 2 gate: thresholds and levels", TEAL),
            ("2", "Last step blank", "n = 3: find x_{IL} and x_{IH}", GREEN),
            ("3", "Last two blank", "two gates: the margins, then the RBS", CYAN),
            ("4", "Bare problem", "a four-decade sensor: say why not", AMBER)]):
        x = M + i * 3.05
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.1, 2.8, 2.5, fill=CARD, line=c, lw=2)
        d.shape(s, S.OVAL, x + 1.15, 2.35, 0.5, 0.5, fill=c, line=None)
        d.text(s, num, x + 1.15, 2.46, 0.5, 0.35, size=18, font=HEAD, bold=True,
               color=WHITE, align="c")
        d.text(s, k, x + 0.15, 3.05, 2.5, 0.4, size=16, font=HEAD, bold=True,
               color=INK, align="c")
        d.text(s, txt, x + 0.15, 3.5, 2.5, 0.9, size=13.5, color=MUTED, align="c")
    d.text(s, "Item 4 has no single right answer. Name the quantity that stops you, and say what you would build instead.",
           M, 4.92, W - 2 * M, 0.7, size=17, bold=True, color=INK)
    d.notes(s, "Item 1 is today's gate, worked. Item 2 changes n to 3: "
               "x_IL = 0.80 K, x_IH = 5.80 K, y_OH = 6.65 K, y_OL = 0.15 K. "
               "Item 3 is the two-gate test and the RBS window. Item 4 asks for "
               "the 9^(1/n) argument in words, and the strongest answer names "
               "feedback plus a sink, which is Daniel's circuit.")

    s = d.dark()
    d.header(s, "79 – 80 min", "Next")
    d.title(s, "Thirteen sessions of circuits, one at a time.")
    d.text(s, "Tuesday: review and worked problems. Thursday: the midterm.",
           M, 2.05, 11, 0.45, size=23, font=HEAD, bold=True, color=MINT)
    d.text(s, "Sessions 12 and 13 are examinable by recognition only — what a transfer curve is, what a noise margin buys, why a cascade sharpens and what it costs. No simulation and no signal-matching arithmetic under exam conditions.",
           M, 2.62, 11.3, 1.3, size=16, color=WHITE, spacing=1.25)
    d.text(s, "PS5 is due tonight. M1 is due tonight. PS6 opens 20 October and is where today gets assessed with numbers.",
           M, 4.10, 11.3, 0.5, size=14, italic=True, color=CYAN)
    d.notes(s, "No reading for Tuesday: it is the review. The scope handout "
               "goes out with it.\n"
               "PS5 and M1 are both due tonight at 11:59, with the usual Friday "
               "grace.")
