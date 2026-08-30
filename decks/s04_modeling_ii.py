"""Session 4 — Modeling Biology II: timescale separation, and where rate laws come from.

Tuesday 8 September. Board work and one short paper block; no laptops. The
computing lives in PS1, which is already out and which this session exists to
make answerable.

    0–8    retrieval (2 from Thursday, 1 interleaved from session 2)
    5–8    goals as questions
    8–14   the small parameter, and what setting it to zero actually claims
    14–26  Michaelis-Menten derived, four named steps
    26–30  the REAL validity condition: Eₜₒₜ << Kₘ + S₀
    30–34  where that group comes from -- two clocks
    34–38  ConcepTest 1 -- double Eₜₒₜ; what happens to Kₘ?
    38–42  the two regimes
    42–46  the error is one ratio, slope 1 over four decades
    46–48  the pause
    48–58  faded set, ITEMS 1 AND 2 ONLY -- ten minutes
    58–62  the answers, and K is not Kd
    62–67  sensitivity, 81^(1/n)
    67–72  two independent sites give n = 1
    72–76  ConcepTest 2 -- a fit gives n = 1.9; how many sites?
    76–80  consolidation, the reading, and the forward link

WHY THE PAPER BLOCK IS TEN MINUTES AND NOT TWENTY-FOUR
Adam, 30 August 2026: too much in-class work causes time diffusion and costly
context switching; sharp easy-ish tasks belong in the room and the rest belongs
on the problem set. Items 3 and 4 of the handout are therefore PS1 Q4b and Q5.
Item 1 is fully worked, so the "nothing is assessed that was not demonstrated"
rule is satisfied by demonstration rather than by completion.

WHAT THIS SESSION OWES PS1
- Q3a wants the validity condition stated as a condition on CONCENTRATIONS.
  That is Eₜₒₜ << Kₘ + S₀, not E << S. Teaching the sloppy version makes the
  question unanswerable, so the condition is on a slide and on a figure.
- Q4a wants the Hill form derived from all-or-none binding: handout item 2.
- Q4b wants the 10-to-90 sensitivity solved analytically: 81^(1/n), slide 14.
- Q5 (247) wants a four-state partition function -- the technique of session 6,
  a week later. Handout item 4 and slide 15 are what keep the coverage rule
  honest on the first problem set.

Coverage matrix: T7, T8, T9.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session04_Modeling_II"


def build():
    d = Deck("Session 4 — Modeling Biology II", session=4)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 4", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Modeling Biology II", M, 2.72, 9.4, 1.3,
           size=40, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Timescale separation, and where a rate law comes from",
           M, 4.15, 9.4, 0.5, size=17, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "No laptops today -- say so at the door, they will have brought "
               "them after Thursday. Handouts go out at the pause, not before: "
               "paper on the desk during a board derivation is paper being read "
               "instead of the board. "
               "PS1 IS DUE THURSDAY. Ask for hands on who has started. Q3 and "
               "Q4 are today's material and Q5 is today's handout item 4, so "
               "anyone who has not started is not behind yet -- say that, "
               "because half of them will assume they are.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 8 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions, and one is not from Thursday")
    for i, (n, src, q, c) in enumerate([
            ("1", "From Thursday",
             "The cascade had γₘ = 0.5 and γₚ = 0.05. Which variable is the fast one, and how do you know without simulating?", TEAL),
            ("2", "From Thursday",
             "Translation is m → m + p. What is the net stoichiometry of m, and why is that a modelling choice rather than a fact?", TEAL),
            ("3", "From session 2",
             "A protein crosses E. coli in ~65 ms; the gene that makes it is transcribed in ~20 s. Which of the two is a variable in this course?", CYAN)]):
        y = 1.9 + i * 1.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.15, fill=c, line=None)
        d.text(s, n, M, y + 0.38, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, src, M + 0.8, y, 3.0, 0.3, size=10.5, bold=True, color=c)
        d.text(s, q, M + 0.8, y + 0.3, 11.7, 0.85, size=15.5, color=BODY)
    d.text(s, "Two minutes in writing. Then I take answers, and I will take the wrong ones first.",
           M, 6.45, W - 2 * M, 0.4, size=15, bold=True, color=INK)
    d.notes(s, "Five minutes and do not shorten it -- this is the spaced "
               "retrieval and it is the cheapest thing in the course. "
               "Q1 is the hinge of the whole session: gamma_m is ten times "
               "gamma_p, so the mRNA relaxes ten times faster, and 'fast' means "
               "'reaches its quasi-equilibrium while the other one is still "
               "moving'. If they can say that, the next forty minutes are a "
               "formalisation of something they already believe. "
               "Q3 is the interleaved one, three sessions back. The answer is "
               "NEITHER -- position is not a variable, because diffusion is "
               "fast compared with everything else, which is the same argument "
               "as Q1 applied to space instead of chemistry. Say that out loud; "
               "it is the connection the retrieval exists to make.")

    # 3 GOALS AS QUESTIONS ----------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By 9:30 you should be able to answer")
    for i, (n, lab) in enumerate([("2", "The substrate"), ("3", "Modeling I"),
                                  ("4", "Modeling II"), ("5", "Expression"),
                                  ("6", "Promoters")]):
        x, here = M + i * 2.42, n == "4"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=12, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "When are you allowed to throw away a differential equation — and how would you know you were wrong?",
            "Michaelis–Menten is on every biochemistry slide you have ever seen. Where does it come from, and what does it assume?",
            "A dose–response curve fits a Hill coefficient of 1.9. How many binding sites does the protein have?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "Three minutes, and questions rather than statements. "
               "Q3 is the one to leave hanging -- it is the last ConcepTest of "
               "the session and the answer is not the one anybody expects. Do "
               "not hint.")

    # 4 THE SMALL PARAMETER ---------------------------------------------------
    s = d.light()
    d.header(s, "8 – 14 min", "At the board  ·  from Thursday's cascade")
    d.title(s, "What you were actually asking on Thursday")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.75, 12.5, 1.35, fill=WASH, line=RULE,
            lw=1)
    for i, (line, why) in enumerate([
            ("dm/dt  =  α  −  γₘ m", "the fast variable: γₘ = 0.5, half-life ~1.4 min"),
            ("dp/dt  =  kₚ m  −  γₚ p", "the slow one: γₚ = 0.05, half-life ~14 min"),
            ("ε  =  γₚ / γₘ  =  0.1", "not a number about enzymes. A number about CLOCKS.")]):
        y = 1.9 + i * 0.42
        d.text(s, line, M + 0.3, y, 6.2, 0.35, size=16, font=TEXT, bold=True,
               color=INK)
        d.text(s, why, M + 6.8, y + 0.03, 5.4, 0.3, size=12, italic=True,
               color=MUTED)
    d.text(s, "Measure time in the protein's units and the mRNA equation acquires an ε in front of its derivative.",
           M, 3.35, 12.5, 0.4, size=18, font=HEAD, bold=True, color=AMBER)
    for i, (k, txt) in enumerate([
            ("Setting ε = 0 is not setting a derivative to zero",
             "It says the fast variable's derivative is small COMPARED WITH THE TERMS IN ITS OWN EQUATION — each of which is order α. dm/dt is not zero; it is ε times something. The equation stops being differential and becomes algebraic."),
            ("Which is why you always get an extra condition",
             "A first-order equation had one initial condition and now has none: m jumps to α/γₘ instantly. That jump is real, it is the first ~1.4 minutes, and it is where the error you cannot remove lives.")]):
        y = 3.95 + i * 1.25
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.05, fill=AMBER, line=None)
        d.text(s, k, M + 0.4, y, 4.3, 0.5, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.9, y + 0.02, 7.3, 1.1, size=13, color=BODY)
    d.notes(s, "Six minutes, at the board, and nondimensionalise in front of "
               "them -- do not show the scaled equation as a fait accompli. "
               "t = tau/gamma_p, m = alpha/gamma_m * mu, and the epsilon "
               "appears. It is the same move as session 3's four-parameters-"
               "become-one, which is the point: they have done this. "
               "THE SENTENCE TO LAND, and it is the one students get wrong for "
               "the rest of the course: 'quasi-steady state' does NOT mean the "
               "fast species stops changing. It means its rate of change is "
               "negligible next to the individually large terms that nearly "
               "cancel to produce it. dm/dt is small because it is a difference "
               "of two big numbers, not because nothing is happening. "
               "The lost initial condition is worth the extra minute. It is a "
               "boundary layer, they will meet the words in a fluids course, "
               "and here it is simply the first minute and a half.")

    # 5 MICHAELIS-MENTEN ------------------------------------------------------
    s = d.light()
    d.header(s, "14 – 26 min", "At the board  ·  every step named")
    d.title(s, "The same move, on the reaction everyone has memorised")
    d.text(s, "E + S  ⇌  ES  →  E + P                    k₁ , k₋₁ , k₂",
           M, 1.7, 12.5, 0.45, size=20, font=TEXT, bold=True, color=INK)
    for i, (step, line, why) in enumerate([
            ("1  ·  QSSA on the complex",
             "k₁[E][S]  =  (k₋₁ + k₂)[ES]",
             "the fast variable is ES, and this is the algebraic equation that replaces its ODE"),
            ("2  ·  Enzyme conservation",
             "[E] + [ES]  =  Eₜₒₜ",
             "nothing is created or destroyed — this is a left null vector, from Thursday"),
            ("3  ·  Eliminate [E]",
             "[ES]  =  Eₜₒₜ [S] / (Kₘ + [S]),    Kₘ ≡ (k₋₁ + k₂)/k₁",
             "Kₘ is a ratio of rate constants. It is not a concentration of anything"),
            ("4  ·  The rate you wanted",
             "v  =  k₂[ES]  =  Vₘₐₓ [S] / (Kₘ + [S]),    Vₘₐₓ ≡ k₂ Eₜₒₜ",
             "one algebraic law, two parameters, and both are things you can measure")]):
        y = 2.3 + i * 1.05
        d.text(s, step, M, y, 3.4, 0.3, size=12.5, font=HEAD, bold=True,
               color=TEAL)
        d.text(s, line, M + 3.6, y - 0.04, 8.9, 0.36, size=15, font=TEXT,
               bold=True, color=INK)
        d.text(s, why, M + 3.6, y + 0.34, 8.9, 0.5, size=11.5, italic=True,
               color=MUTED)
    d.foot(s, "Four steps. Two of them are things you did on Thursday, and one of them is a definition.", 6.6)
    d.notes(s, "Twelve minutes, all of it at the board, and ASK FOR EACH STEP "
               "before you write it. They can do steps 1 and 2 unaided; step 2 "
               "IS a conservation law and calling it that out loud is worth "
               "more than the algebra, because it connects Thursday's left null "
               "space to something they already knew from biochemistry. "
               "Insist on K_M being a ratio of rate constants. Half the room "
               "arrives believing K_M is 'the concentration at half V_max', "
               "which is a consequence, not a definition, and the difference "
               "matters the moment k2 is not small. "
               "If k2 << k_-1 then K_M -> k_-1/k1 = K_d, the true dissociation "
               "constant. Say when that is true and when it is not. The gap "
               "between K_M and K_d is a real experimental headache and thirty "
               "seconds now saves an argument in session 6.")

    # 6 THE CONDITION ---------------------------------------------------------
    s = d.dark()
    d.header(s, "26 – 30 min", "The half of it nobody teaches")
    d.title(s, "'The enzyme is small' is not a condition")
    d.text(s, "A condition is something you can check with the numbers in front of you.",
           M, 2.0, 11.9, 0.4, size=17, italic=True, color=MINT)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 2.6, W - 2 * M, 1.15, fill=None,
            line=CYAN, lw=2)
    d.text(s, "Eₜₒₜ   ≪   Kₘ  +  S₀", M, 2.78, W - 2 * M, 0.6, size=30,
           font=TEXT, bold=True, color=CYAN, align="c")
    d.text(s, "and NOT  E ≪ S,  which is the version in the textbook you had",
           M, 3.35, W - 2 * M, 0.32, size=13, italic=True, color=SILVER,
           align="c")
    for i, (k, txt) in enumerate([
            ("They agree when S₀ ≫ Kₘ",
             "which is the in-vitro assay the textbook was describing: substrate flooded in, enzyme a trace. Fine, and not the situation in a cell."),
            ("They part company when S₀ ≪ Kₘ",
             "then the condition is Eₜₒₜ ≪ Kₘ, and the approximation survives an enzyme concentration comparable with the substrate. Many intracellular enzymes live here."),
            ("The reason is the timescale, not the tidiness",
             "the QSSA needs ES to equilibrate before S has appreciably changed. What sets the ratio of those two times is Eₜₒₜ/(Kₘ + S₀).")]):
        y = 4.05 + i * 0.9
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.72, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.6, 0.4, size=14, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.3, y - 0.02, 6.6, 0.78, size=12.5, color=MINT)
    d.notes(s, "Eight minutes. THIS IS THE SLIDE PS1 Q3a IS ASKING ABOUT -- the "
               "question says explicitly 'not merely that ES is at steady "
               "state, but what must be true of the concentrations', and a "
               "student who only has E << S cannot answer it. "
               "Do NOT derive the perturbation theory. Segel's scaling argument "
               "(Segel 1988; Segel & Slemrod 1989) is a beautiful paper and a "
               "different course. State the condition, motivate it by the "
               "timescale argument in the third box, and then SHOW it holding "
               "numerically on the next two slides. That ordering is the "
               "session's method: assert nothing you are about to be able to "
               "check. "
               "Worth saying plainly: you were taught the special case and "
               "nobody mentioned it was one. That happens a lot, and noticing "
               "it is most of what this course is for.")

    # 6b WHY THAT GROUP -------------------------------------------------------
    # Split out of the condition slide because the build harness flagged eight
    # minutes on one slide -- which is not a short segment, it is an improvised
    # one. The condition and the reason for the condition are two ideas and they
    # get a surface each.
    s = d.light()
    d.header(s, "30 – 34 min", "At the board  ·  where that group comes from")
    d.title(s, "Two clocks, and the QSSA needs one to beat the other")
    for i, (k, expr, why) in enumerate([
            ("τ₁ — how long ES takes to reach quasi-equilibrium",
             "τ₁  ≈  1 / [ k₁ (Kₘ + S₀) ]",
             "the fast clock — and notice it does not contain Eₜₒₜ at all"),
            ("τ₂ — how long S takes to be consumed",
             "τ₂  ≈  (Kₘ + S₀) / Vₘₐₓ  =  (Kₘ + S₀) / (k₂ Eₜₒₜ)",
             "the slow clock — and this one is inversely proportional to Eₜₒₜ"),
            ("The QSSA needs τ₁ ≪ τ₂, so form the ratio",
             "τ₁ / τ₂  =  [ k₂ / k₁(Kₘ + S₀) ] · Eₜₒₜ / (Kₘ + S₀)",
             "and the bracket is at most 1, because k₂/k₁ ≤ Kₘ ≤ Kₘ + S₀")]):
        y = 1.8 + i * 1.25
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.05, fill=TEAL, line=None)
        d.text(s, k, M + 0.4, y, 4.5, 0.5, size=14, font=HEAD, bold=True,
               color=INK)
        d.text(s, expr, M + 5.1, y, 7.1, 0.36, size=15, font=TEXT, bold=True,
               color=INK)
        d.text(s, why, M + 5.1, y + 0.4, 7.1, 0.5, size=11.5, italic=True,
               color=MUTED)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.55, W - 2 * M, 1.0, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "So Eₜₒₜ / (Kₘ + S₀) is an upper bound on the ratio of the two clocks. Make it small and you have made the fast one fast enough — whatever the rate constants are.",
           M + 0.3, 5.72, 11.6, 0.7, size=15, bold=True, color=INK)
    d.notes(s, "Four minutes at the board and derive both clocks rather than "
               "showing them. t_c is the relaxation time of the linearised "
               "complex equation; t_s is substrate over its maximum rate. "
               "Neither needs perturbation theory and both are one line. "
               "THE OBSERVATION THAT MAKES IT CLICK: t_c does not contain "
               "E_tot. The fast clock is set by the chemistry; the slow clock "
               "is set by how much enzyme you added. So the only way to break "
               "the separation is to add enzyme -- which is exactly what the "
               "vote you are about to take is about. "
               "With today's numbers: t_c = 0.48 in both cases, t_s = 21000 at "
               "E_tot = 0.001 and 21 at E_tot = 1. Same enzyme, same substrate, "
               "and the two clocks went from a factor of 44,000 apart to a "
               "factor of 44. Write those four numbers on the board. "
               "Do NOT prove the bound on the bracket; state it and move. The "
               "point is that the group is an upper bound, so checking it is "
               "conservative.")

    # 7 CONCEPTEST 1 ----------------------------------------------------------
    s = d.dark()
    d.header(s, "34 – 38 min", "Vote  ·  argue with your neighbour  ·  vote again")
    d.title(s, "You double the enzyme concentration.")
    d.text(s, "Same enzyme, same substrate, same buffer. Twice as much E. What happens to Kₘ and to Vₘₐₓ?",
           M, 2.0, 12.5, 0.6, size=19, font=HEAD, color=MINT)
    for i, (lab, opt) in enumerate([
            ("A", "Both double — they are both properties of the reaction."),
            ("B", "Vₘₐₓ doubles; Kₘ is unchanged."),
            ("C", "Kₘ doubles; Vₘₐₓ is unchanged."),
            ("D", "Neither changes; Kₘ and Vₘₐₓ are constants of the enzyme.")]):
        y = 2.9 + i * 0.78
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.52, fill=CYAN, line=None)
        d.text(s, lab, M, y + 0.11, 0.55, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.08, 11.6, 0.4, size=16, color=WHITE)
    d.foot(s, "You have both definitions on the board. This is a ten-second question and a two-minute argument.", 6.15)
    d.notes(s, "Four minutes. ANSWER B. V_max = k2 * E_tot doubles; "
               "K_M = (k_-1 + k2)/k1 contains no E at all. "
               "A is the majority first answer and it comes from treating both "
               "symbols as 'enzyme properties' without looking at what they are "
               "made of. That is exactly the habit the derivation was for. "
               "D is the interesting wrong answer and worth naming: K_M IS a "
               "constant of the enzyme, V_max is not -- it is a constant of the "
               "enzyme TIMES how much you put in. A quantity people quote as a "
               "property of a protein turns out to be a property of an "
               "experiment. "
               "THE STING, and only after the revote: doubling E_tot also "
               "doubles E_tot/(K_M + S_0). Ask whether the Michaelis-Menten "
               "curve they just corrected is still valid. It is the bridge to "
               "the next slide and somebody always sees it.")

    # 8 THE TWO REGIMES -------------------------------------------------------
    s = d.light()
    d.header(s, "38 – 42 min", "The same reduction, twice")
    d.title(s, "Nothing about the enzyme changed")
    d.image(s, "figures/build/s04_qssa_regimes.png", M, 1.6, 12.5, 3.9)
    d.text(s, "Left: the condition holds and the two curves are the same curve. Right: Eₜₒₜ/(Kₘ + S₀) ≈ 0.5 and Michaelis–Menten is early by fifteen per cent of the substrate.",
           M, 5.65, 12.5, 0.55, size=15, color=BODY)
    d.foot(s, "Both panels run to twelve turnovers. Compare on the system's own clock or you compare your integration window instead.", 6.4)
    d.notes(s, "Four minutes. Ask which panel is which BEFORE you say -- the "
               "shapes are identical and the only cue is the label, which is "
               "the point. "
               "The shaded band is where PS1's integration window stops. On the "
               "left it is a tenth of one turnover, so the number PS1 prints "
               "for E0 = 0.001 is the error over the first ten per cent of the "
               "reaction, not over the reaction. Both are tiny and the "
               "conclusion is unaffected, but if a student notices, they are "
               "right and should be told so.")

    # 9 THE ERROR IS A RATIO --------------------------------------------------
    s = d.light()
    d.header(s, "42 – 46 min", "Why it is a condition and not a slogan")
    d.title(s, "The error is set by one number, over four decades")
    d.image(s, "figures/build/s04_qssa_error.png", M + 1.6, 1.6, 9.3, 4.3)
    d.text(s, "Slope one. Halve the group, halve the error — which is what lets you decide, before you trust a model, how wrong it is allowed to be.",
           M, 6.05, 12.5, 0.5, size=16, font=HEAD, bold=True, color=AMBER)
    d.notes(s, "Four minutes, and this is the slide that earns the session. "
               "A straight line on log-log across four decades is what turns a "
               "rule of thumb into an engineering tolerance: pick the error you "
               "can live with, read off the ratio, and that is a constraint on "
               "your design. "
               "Ask what the slope being ONE means. Answer: the error is "
               "first-order in the small parameter, which is exactly what the "
               "epsilon argument at the board predicted. The figure is not "
               "decoration; it is the check on the derivation. "
               "PS1 Q3c is this figure, two points of it, and Q3d asks them to "
               "connect those points to the condition. Say so.")

    # 10 PAUSE ----------------------------------------------------------------
    s = d.dark()
    d.header(s, "46 – 48 min", "Two minutes  ·  I will not say anything")
    d.title(s, "Compare notes with the person next to you")
    d.text(s, "One of you writes down what the QSSA assumes. The other writes down what Kₘ is made of. Then swap and argue.",
           M, 2.2, 11.9, 0.8, size=20, color=WHITE, spacing=1.3)
    d.text(s, "This is not a break. It is the only two minutes in the session where you find out what you missed while you were writing.",
           M, 3.4, 11.9, 0.6, size=16, italic=True, color=MINT)
    d.text(s, "Then: handouts.", M, 4.5, 11.9, 0.5, size=22, font=HEAD,
           bold=True, color=CYAN)
    d.foot(s, "The pause procedure — two minutes, three times a lecture — is one of the cheapest interventions with real evidence behind it.", 6.3)
    d.notes(s, "Two minutes and SAY NOTHING. Stand at the back. "
               "Hand the paper out during the second minute so the transition "
               "is already made when you speak again.")

    # 11 THE FADED SET --------------------------------------------------------
    s = d.light()
    d.header(s, "48 – 58 min", "Handout  ·  items 1 and 2  ·  ten minutes")
    d.title(s, "Where a regulation function comes from")
    for i, (n, k, txt, c) in enumerate([
            ("1", "Fully worked — one site",
             "P + X ⇌ PX. Write the equilibrium, form the fraction, cancel what you cannot measure. Read it; do not copy it.", TEAL),
            ("2", "The last step is yours — n sites, all or nothing",
             "The same four steps with n copies of X. You finish it, and you say what K is — because it is not Kd.", CYAN),
            ("3", "On PS1 — what n actually buys you",
             "The fold-change in X from 10% to 90% occupancy, solved algebraically. Q4b.", MUTED),
            ("4", "On PS1 — two INDEPENDENT sites  ·  247",
             "Four states, a partition function, and an answer that is not the one the site count suggests. Q5.", MUTED)]):
        y = 1.85 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.9, fill=c, line=None)
        d.text(s, n, M, y + 0.26, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 4.4, 0.4, size=14.5, font=HEAD, bold=True,
               color=INK if i < 2 else MUTED)
        d.text(s, txt, M + 5.4, y + 0.02, 6.9, 0.9, size=12.5,
               color=BODY if i < 2 else MUTED)
    d.text(s, "Ten minutes, and only the first two. Three and four are the same technique with the scaffolding gone — that is a problem set, not a lecture.",
           M, 6.45, W - 2 * M, 0.45, size=15, bold=True, color=INK)
    d.notes(s, "TEN MINUTES, AND SAY THE NUMBER OUT LOUD when you set them off. "
               "A block this size stays sharp; the twenty-four minute version "
               "diffuses and the switch back costs more than the extra work "
               "buys. "
               "Item 1 is already worked -- tell them to READ it rather than "
               "copy it, and to start at item 2 if the first one is obvious. "
               "Nobody has to announce which. "
               "CIRCULATE. The error to watch for in item 2 is students "
               "writing K = K_d and moving on: the whole point is that "
               "K = K_d^(1/n), and getting it wrong is more useful than getting "
               "it right if you catch it in the room. "
               "Do not work item 3 or 4 even if asked. They are on the set, "
               "they are due Thursday, and the discussion hour exists.")

    # 12 THE ANSWERS ----------------------------------------------------------
    s = d.light()
    d.header(s, "58 – 62 min", "The answers  ·  and the one that is not Kd")
    d.title(s, "Items 1 and 2")
    for i, (n, ans, prompt, c) in enumerate([
            ("1",
             "f = (x/Kd) / (1 + x/Kd) = x / (Kd + x).  A Hill function with n = 1 and K = Kd.",
             "[P] cancelled because it appears in every term of both numerator and denominator — it is the reference state. It would not cancel if the promoter could be in a state that is neither empty nor bound by X, which is exactly what session 6 is about.",
             TEAL),
            ("2",
             "f = xⁿ / (Kd + xⁿ) = xⁿ / (Kⁿ + xⁿ)  with  K = ⁿ√Kd.",
             "K is the concentration at half occupancy; Kd is an equilibrium constant with units of concentration^n. Two promoters with the same K and different Kd differ in n — the same switch point, a different sharpness.",
             CYAN)]):
        y = 1.9 + i * 2.0
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.6, fill=c, line=None)
        d.text(s, n, M, y + 0.6, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, ans, M + 0.8, y, 11.7, 0.5, size=15, font=HEAD, bold=True,
               color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, M + 0.8, y + 0.58, 0.1, 0.95,
                fill=MUTED, line=None)
        d.text(s, prompt, M + 1.15, y + 0.55, 11.35, 1.0, size=12.5, color=BODY)
    d.text(s, "The idealisation in item 2 — empty or full, nothing between — is a lie. The next ten minutes are about what it costs you.",
           M, 6.3, W - 2 * M, 0.45, size=16, font=HEAD, bold=True, color=AMBER)
    d.notes(s, "Four minutes, and take both from the room before showing them. "
               "The K = K_d^(1/n) point is the one to slow down on. Units are "
               "the fastest way in: K_d in item 2 has units of concentration to "
               "the n, so it cannot be a concentration, so it cannot be the "
               "half-point. Dimensional analysis catches it before algebra "
               "does, and that is a habit worth naming. "
               "Land the closing line and move -- it sets up both remaining "
               "slides.")

    # 13 SENSITIVITY ----------------------------------------------------------
    s = d.light()
    d.header(s, "62 – 67 min", "At the board  ·  what n is for")
    d.title(s, "A Hill coefficient is a sensitivity, and that is all it is")
    d.image(s, "figures/build/s04_hill_family.png", M + 1.8, 1.55, 9.0, 4.15)
    d.text(s, "Set f = 0.1 and f = 0.9, solve each for x:   x₁₀ = K (1/9)^(1/n),  x₉₀ = K (9)^(1/n)   ⟹   x₉₀/x₁₀ = 81^(1/n)",
           M, 5.8, 12.5, 0.45, size=17, font=TEXT, bold=True, color=INK)
    d.foot(s, "Independent of K. Every curve above crosses half occupancy in the same place — n is the only thing that differs.", 6.4)
    d.notes(s, "Five minutes and derive it at the board; it is four lines and "
               "it is PS1 Q4b, which asks for it analytically and says no "
               "numerical search. "
               "The number to make them feel: n = 1 needs an EIGHTY-ONE-FOLD "
               "change in the input to go from a tenth on to nine tenths on. "
               "That is not a switch, it is a slope. n = 4 needs three-fold. "
               "This is why cooperativity is worth engineering and why every "
               "toggle in the second half of this course has an n in it -- "
               "session 9's bistability condition is alpha_c = n(n-1)^-(n+1)/n, "
               "which is infinite for n <= 1. No cooperativity, no switch, and "
               "that is not a modelling artifact.")

    # 14 INDEPENDENT SITES ----------------------------------------------------
    s = d.light()
    d.header(s, "67 – 72 min", "At the board  ·  the idealisation, priced")
    d.title(s, "Two sites, no cooperativity, and the answer is n = 1")
    d.image(s, "figures/build/s04_independent_sites.png", M + 1.8, 1.5, 9.0, 4.1)
    for i, (k, txt) in enumerate([
            ("Four states, and the weights write themselves",
             "Z = 1 + 2w + w² = (1 + w)² with w = x/Kd. Occupancy = w(1+w)/(1+w)² = w/(1+w). The square cancels."),
            ("So n counts cooperativity, not sites",
             "n = 2 requires the intermediate states to be unpopulated. n ≤ number of sites always, with equality only in a limit nothing quite reaches.")]):
        y = 5.7 + i * 0.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.1, 0.42, fill=AMBER, line=None)
        d.text(s, k, M + 0.32, y - 0.02, 4.4, 0.4, size=13, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 4.9, y - 0.02, 7.4, 0.45, size=12, color=BODY)
    d.notes(s, "Five minutes, at the board, and write the four states as a "
               "column before you write Z. This is a partition function and it "
               "is session 6 arriving a week early -- say that, because PS1 Q5 "
               "asks 247 for exactly this and it would otherwise be assessing "
               "something untaught. "
               "MAKE THEM SAY WHICH FRACTION. 'Fraction of sites occupied' is "
               "w/(1+w); 'fraction of promoters with at least one site bound' "
               "is 1 - 1/(1+w)^2, which is not a Hill function at all. Same "
               "molecules, same physics, two different curves, and the paper "
               "you are reading may not tell you which it plotted. "
               "The generalisation, one sentence: N independent identical sites "
               "give (1+w)^N, and the occupancy is ALWAYS w/(1+w). "
               "Independence is what makes the sites invisible to the "
               "dose-response.")

    # 15 CONCEPTEST 2 ---------------------------------------------------------
    s = d.dark()
    d.header(s, "72 – 76 min", "Vote  ·  argue  ·  vote again")
    d.title(s, "A dose–response fits a Hill coefficient of 1.9.")
    d.text(s, "Clean data, a good fit, a well-behaved protein. How many binding sites does it have?",
           M, 2.0, 12.5, 0.5, size=19, font=HEAD, color=MINT)
    for i, (lab, opt) in enumerate([
            ("A", "Two."),
            ("B", "At least two."),
            ("C", "Exactly one — 1.9 is within error of a single site."),
            ("D", "You cannot tell anything about the number of sites from n.")]):
        y = 2.8 + i * 0.78
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.52, fill=CYAN, line=None)
        d.text(s, lab, M, y + 0.11, 0.55, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.08, 11.6, 0.4, size=16, color=WHITE)
    d.foot(s, "One of these is right, one is nearly right, and the difference between them is the whole session.", 6.15)
    d.notes(s, "Four minutes. ANSWER B -- AT LEAST two. "
               "n <= number of sites, with equality only for infinite "
               "cooperativity, so a fitted 1.9 puts a FLOOR under the site "
               "count and no ceiling. A protein with six sites and moderate "
               "cooperativity fits 1.9 perfectly well. "
               "A is the majority first answer and it is the misreading this "
               "session exists to prevent -- it is also extremely common in "
               "print, which is worth saying out loud to a room that is about "
               "to start reading primary literature. "
               "D is the interesting wrong answer. It over-corrects: n does "
               "constrain the site count, just from below. Somebody clever "
               "usually argues for D after the first vote and the argument is "
               "worth having. "
               "C misreads the question rather than the biology.")

    # 16 CONSOLIDATION + FORWARD ----------------------------------------------
    s = d.dark()
    d.header(s, "76 – 80 min", "Next")
    d.title(s, "You can reduce a model. Now ask how fast it can change its mind.")
    d.text(s, "Thursday: gene expression dynamics and response time.",
           M, 1.95, 11.6, 0.45, size=22, font=HEAD, bold=True, color=MINT)
    d.text(s, "Today you deleted a variable and priced the deletion. Both rate laws you derived are instantaneous — they have no memory and no clock of their own. Every clock in a circuit is therefore set by the SLOW variables you kept, and there is one you cannot delete and cannot slow down.",
           M, 2.55, 11.6, 1.15, size=16, color=WHITE, spacing=1.35)
    d.text(s, "How quickly can a cell change the concentration of a protein — and what sets the floor?",
           M, 3.85, 11.6, 0.4, size=17, bold=True, color=CYAN)
    bottom = d.assignment(s, y=4.45)
    d.text(s, "PS1 is due Thursday. Q3 and Q4 are today; Q5 is item 4 of your handout.",
           M, bottom + 0.1, 11.6, 0.35, size=15, bold=True, color=SILVER)
    d.notes(s, "Four minutes total, and the last two are the retrieval: notes "
               "closed, one sentence each on the three questions from the goals "
               "slide. Do not skip it to finish the material -- it is the "
               "second retrieval and it is the part with the evidence behind "
               "it. "
               "ASSIGN THE READING OUT LOUD, do not rely on the slide: Andersen "
               "1998, seven pages, and Figure 3A is the one that matters. It is "
               "in Files > Readings on bCourses. Session 5 opens on it. "
               "The forward link is a question, not a statement -- leave it "
               "hanging.")

    return d
