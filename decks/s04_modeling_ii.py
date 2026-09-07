"""Session 4 — Modeling Biology II: timescale separation, and where rate laws come from.

Tuesday 8 September. Board work and one short paper block; no laptops. The
computing lives in PS1, which is already out and which this session exists to
make answerable.

    0–8    retrieval (2 from Thursday, 1 interleaved from session 2)
    5–8    goals as questions
    8–14   the small parameter, and what setting it to zero actually claims
    14–26  Michaelis-Menten derived, four named steps
    26–30  two clocks, and the group that falls out of their ratio
    30–34  that group named as the validity condition: E_{tot} << K_{M} + S_{0}
    34–38  ConcepTest 1 -- double E_{tot}; what happens to K_{M}?
    38–42  the two regimes
    42–46  the error is one ratio, slope 1 over four decades
    46–48  the pause
    48–58  faded set, ITEMS 1 AND 2 ONLY -- ten minutes
    58–62  the answers to items 1 and 2
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
  That is E_{tot} << K_{M} + S_{0}, not E << S. Teaching the sloppy version makes the
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
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=14, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "No laptops today. Say so at the door.\n"
               "Handouts stay at the front until the pause.\n"
               "PS1 is due Thursday. Q3 and Q4 are today's material; Q5 is "
               "item 4 of today's handout.\n"
               "Ask: hands up who has opened it.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Three questions, notes closed")
    for i, (n, src, q, c) in enumerate([
            ("1", "From Thursday",
             "The cascade had γ_{m} = 0.5 and γ_{p} = 0.05. Which variable is the fast one, and how do you know without simulating?", TEAL),
            ("2", "From Thursday",
             "Translation is m → m + p. What is the net stoichiometry of m, and why is that a modeling choice rather than a fact?", TEAL),
            ("3", "From session 2",
             "A protein crosses E. coli in ~65 ms; the gene that makes it is transcribed in ~20 s. Is either of those a variable in this course?", CYAN)]):
        y = 1.9 + i * 1.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.15, fill=c, line=None)
        d.text(s, n, M, y + 0.38, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, src, M + 0.8, y, 3.0, 0.3, size=13, bold=True, color=c)
        d.text(s, q, M + 0.8, y + 0.3, 11.7, 0.85, size=15.5, color=BODY)
    d.text(s, "Two minutes in writing. Then we take answers — including the ones you are unsure of.",
           M, 6.45, W - 2 * M, 0.4, size=15, bold=True, color=INK)
    d.notes(s, "Q1: gamma_m is ten times gamma_p, so mRNA relaxes ten times "
               "faster. 'Fast' means it reaches quasi-equilibrium while the "
               "other one is still moving.\n"
               "Q2: the net stoichiometry of m is zero. m is a catalyst here, "
               "which is a choice about which timescale we are modeling.\n"
               "Q3: neither. Position is not a variable because diffusion is "
               "fast compared with everything else - Q1's argument applied to "
               "space.\n"
               "Say: 'Two minutes in writing. I will take the wrong answers "
               "first.'")

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
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=13.5, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "When are you allowed to throw away a differential equation — and how would you know you were wrong?",
            "Michaelis–Menten is the standard rate law for enzyme catalysis. Where does it come from, and what does it assume?",
            "A dose–response curve fits a Hill coefficient of 1.9. What can you conclude about the number of binding sites?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "The third question is ConcepTest 2, at 72 min. Leave it "
               "unanswered here.")

    # 4 THE SMALL PARAMETER ---------------------------------------------------
    s = d.light()
    d.header(s, "8 – 14 min", "At the board  ·  from Thursday's cascade")
    d.title(s, "Back to Thursday's cascade")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.75, 12.5, 1.35, fill=WASH, line=RULE,
            lw=1)
    for i, (line, why) in enumerate([
            ("dm/dt  =  α  −  γ_{m} m", "the fast variable: γ_{m} = 0.5, half-life ~1.4 min"),
            ("dp/dt  =  k_{p} m  −  γ_{p} p", "the slow one: γ_{p} = 0.05, half-life ~14 min"),
            ("ε  =  γ_{p} / γ_{m}  =  0.1", "the ratio of two clocks: 0.05 per min against 0.5 per min")]):
        y = 1.9 + i * 0.42
        d.text(s, line, M + 0.3, y, 6.2, 0.35, size=16, font=TEXT, bold=True,
               color=INK)
        d.text(s, why, M + 6.8, y + 0.03, 5.4, 0.3, size=13.5, italic=True,
               color=MUTED)
    d.text(s, "Measure time in the protein's units and the mRNA equation acquires an ε in front of its derivative.",
           M, 3.35, 12.5, 0.4, size=18, font=HEAD, bold=True, color=INK)
    for i, (k, txt) in enumerate([
            ("Setting ε = 0 is not setting a derivative to zero",
             "It says dm/dt is small next to the terms in its own equation, each of which is about the size of α. The equation stops being differential and becomes algebraic."),
            ("Which is why you always get an extra condition",
             "A first-order equation had one initial condition and now has none: m jumps to α/γ_{m} instantly. The real trajectory takes about 1.4 minutes to get there, and the reduced model misses all of it.")]):
        y = 3.95 + i * 1.25
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.05, fill=AMBER, line=None)
        d.text(s, k, M + 0.4, y, 4.3, 0.5, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.9, y + 0.02, 7.3, 1.1, size=14, color=BODY)
    d.notes(s, "Scaling: t = tau/gamma_p, m = (alpha/gamma_m) mu. The epsilon "
               "appears in front of the mRNA derivative.\n"
               "Quasi-steady state does not mean the fast species stops "
               "changing. dm/dt is small because it is a difference of two big "
               "numbers: at alpha = 10 and gamma_m = 0.5, each term is about "
               "10 and the difference is about 1.\n"
               "The algebraic equation has no initial condition left. m jumps "
               "to alpha/gamma_m instantly, and the jump lasts about 1/gamma_m "
               "= 1.4 min. It is a boundary layer.\n"
               "Ask: which is the fast variable, and how do you know without "
               "simulating?")

    # 5 MICHAELIS-MENTEN ------------------------------------------------------
    s = d.light()
    d.header(s, "14 – 26 min", "At the board  ·  every step named")
    d.title(s, "The same move, on enzyme catalysis")
    d.text(s, "E + S  ⇌  ES  →  E + P                    k_{1} , k_{-1} , k_{2}",
           M, 1.7, 12.5, 0.45, size=20, font=TEXT, bold=True, color=INK)
    for i, (step, line, why) in enumerate([
            ("1  ·  Quasi-steady state on ES",
             "k_{1}[E][S]  =  (k_{-1} + k_{2})[ES]",
             "the QSSA: ES changes slowly next to the big terms that make it, so algebra replaces its ODE"),
            ("2  ·  Enzyme conservation",
             "[E] + [ES]  =  E_{tot}",
             "nothing is created or destroyed — a conservation law, and the left null vector from Thursday"),
            ("3  ·  Eliminate [E]",
             "[ES]  =  E_{tot} [S] / (K_{M} + [S]),    K_{M} ≡ (k_{-1} + k_{2})/k_{1}",
             "a ratio of rate constants — it has units of concentration, but it is nobody's concentration"),
            ("4  ·  The rate you wanted",
             "v  =  k_{2}[ES]  =  V_{max} [S] / (K_{M} + [S]),    V_{max} ≡ k_{2} E_{tot}",
             "[S] is FREE substrate. Everything after this slide quietly uses total S — that substitution is the error we are about to price")]):
        y = 2.3 + i * 1.05
        d.text(s, step, M, y, 3.4, 0.3, size=14, font=HEAD, bold=True,
               color=TEAL)
        d.text(s, line, M + 3.6, y - 0.04, 8.9, 0.36, size=15, font=TEXT,
               bold=True, color=INK)
        d.text(s, why, M + 3.6, y + 0.34, 8.9, 0.5, size=13.5, italic=True,
               color=MUTED)
    d.foot(s, "Steps 1 and 2 you did on Thursday. Step 3 is a definition. Step 1 is an assumption, and we have not said when it holds.", 6.6)
    d.notes(s, "Ask for each step before writing it. They can do 1 and 2 "
               "unaided.\n"
               "Step 2 is a conservation law - a left null vector, from "
               "Thursday.\n"
               "K_M = (k_-1 + k_2)/k_1 is a ratio of rate constants with units "
               "of concentration. Half the room arrives believing K_M is 'the "
               "concentration at half V_max', which follows from the "
               "definition and is not it.\n"
               "When k_2 << k_-1, K_M -> k_-1/k_1 = K_d.\n"
               "Move both definitions to the left wing and leave them there. "
               "ConcepTest 1 needs them.")

    # 6 WHAT THE QSSA COSTS ---------------------------------------------------
    # REWRITTEN 7 Sep after an adversarial review. The previous version derived
    # the condition from tau_1 << tau_2, and that argument is wrong: holding
    # E_tot/(K_M+S_0) at 0.5 and driving tau_1/tau_2 down three decades leaves
    # the error pegged at 16%. The deck refuted itself -- slide 9's right panel
    # has tau_1/tau_2 = 0.023, clocks separated 44-fold, and Michaelis-Menten
    # wrong by 15%. Clock separation is NECESSARY (you need a fast variable to
    # eliminate) and nowhere near sufficient. What actually controls the error
    # is substrate bookkeeping: how much S is hiding inside ES. One line, and
    # it lands on the same group.
    s = d.light()
    d.header(s, "26 – 30 min", "At the board  ·  when is step 1 allowed?")
    d.title(s, "Where the substrate goes while you are not looking")
    for i, (k, expr, why) in enumerate([
            ("First, there IS a fast variable",
             "\u03c4_{1}  \u2248  1 / [ k_{1}(E_{tot} + K_{M} + S_{0}) ]        \u03c4_{2}  \u2248  (K_{M} + S_{0}) / (k_{2} E_{tot})",
             "ES relaxes; S is consumed. Necessary — but on its own it buys you almost nothing"),
            ("Second, and this is the one that bites",
             "[ES]  =  E_{tot} S / (K_{M} + S)   \u2264   E_{tot} S_{0} / (K_{M} + S_{0})",
             "the reduced model tracks S alone — every molecule in ES is substrate it cannot see"),
            ("So demand the hidden substrate be negligible",
             "E_{tot} S_{0} / (K_{M} + S_{0})   <<   S_{0}",
             "divide out S_{0} — and the whole condition is one dimensionless group")]):
        y = 1.8 + i * 1.25
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.05, fill=TEAL, line=None)
        d.text(s, k, M + 0.4, y, 4.5, 0.5, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, expr, M + 5.1, y, 7.1, 0.4, size=16, font=TEXT, bold=True,
               color=INK)
        d.text(s, why, M + 5.1, y + 0.44, 7.1, 0.5, size=14, italic=True,
               color=MUTED)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.55, W - 2 * M, 1.0, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "E_{tot} / (K_{M} + S_{0})   is the fraction of the substrate the reduced model cannot see. Make it small and Michaelis–Menten is bookkeeping you can trust.",
           M + 0.3, 5.75, 11.6, 0.6, size=17, bold=True, color=INK)
    d.notes(s, "Two conditions, and only the second one has teeth.\n"
               "Clock separation is necessary: you cannot eliminate a variable "
               "that is not fast. It is nowhere near sufficient. Hold "
               "E_tot/(K_M+S_0) at 0.5 and drive tau_1/tau_2 down a "
               "thousandfold and the error stays at 16%.\n"
               "The condition that bites is substrate bookkeeping. The reduced "
               "model has one variable, S, and no account for the substrate "
               "held in ES. At quasi-steady state that is E_tot S/(K_M+S), "
               "largest at the start, and it has to be small next to S_0.\n"
               "Divide by S_0 and the condition is E_tot/(K_M+S_0) << 1. No "
               "bound, no bracket, one line.\n"
               "The number that makes it concrete, and it is the next figure: "
               "at E_tot = 1, thirty-five percent of all the substrate is "
               "sitting in complex at the peak. That is the 15% error.\n"
               "Ask the room: the reduced model has one equation for S. Where "
               "did the rest of the substrate go?")

    # 6b THE CONDITION --------------------------------------------------------
    s = d.dark()
    d.header(s, "30 – 34 min", "Where the textbook condition comes from")
    d.title(s, "The condition, and the version usually quoted")
    d.text(s, "From the board: the substrate hidden in ES is a fraction E_{tot}/(K_{M} + S_{0}) of the total. Require that to be small, and",
           M, 1.98, 11.9, 0.45, size=16, color=MINT)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 2.52, W - 2 * M, 0.95, fill=None,
            line=CYAN, lw=2)
    d.text(s, "E_{tot}   <<   K_{M}  +  S_{0}", M, 2.63, W - 2 * M, 0.6, size=30,
           font=TEXT, bold=True, color=CYAN, align="c")
    d.text(s, "The condition usually quoted is  E_{tot} << S_{0}.  That is this line in the case S_{0} >> K_{M}.",
           M, 3.60, W - 2 * M, 0.34, size=15, italic=True, color=SILVER,
           align="c")
    for i, (k, txt) in enumerate([
            ("They agree when S_{0} >> K_{M}",
             "a test-tube assay: substrate flooded in, enzyme present in trace amounts. Fine, and not the situation in a cell."),
            ("They part company when S_{0} << K_{M}",
             "the condition becomes E_{tot} << K_{M}, which survives an enzyme concentration comparable with the substrate. Many enzymes inside a cell sit here."),
            ("And \u201c<<\u201d means more than you think",
             "the error is about 0.36 of the group. For 1% you need E_{tot}/(K_{M} + S_{0}) = 0.028 — a factor of forty, not a factor of ten.")]):
        y = 4.15 + i * 0.88
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.72, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.6, 0.4, size=15, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.3, y - 0.02, 6.6, 0.78, size=14, color=MINT)
    d.notes(s, "Nothing new here. The hidden-substrate fraction being small "
               "and E_tot << K_M + S_0 are the same sentence.\n"
               "This is what PS1 Q3a asks for - what must be true of the "
               "concentrations. E << S does not answer it.\n"
               "S_0 >> K_M: the two agree, which is why the short version "
               "survived. That is the test-tube assay.\n"
               "S_0 << K_M: the condition becomes E_tot << K_M.\n"
               "The prefactor is the practical point. Error is about 0.36 "
               "times the group, so 1% needs 0.028 and 5% needs 0.14. Students "
               "read << as a factor of ten and it is closer to forty.\n"
               "Segel 1988 and Segel & Slemrod 1989 are the full treatment.\n"
               "If asked whether the approximation can be repaired rather "
               "than merely avoided: yes. Writing the rate in terms of "
               "TOTAL substrate instead of free gives the total QSSA, "
               "which at E_tot = 1 has 1.3% error where this one has 15%. "
               "Name it, do not derive it.")

    # 7 CONCEPTEST 1 ----------------------------------------------------------
    s = d.dark()
    d.header(s, "34 – 38 min", "Vote  ·  argue with your neighbor  ·  vote again")
    d.title(s, "You double the enzyme concentration.")
    d.text(s, "Same enzyme, same substrate, same buffer. Twice as much E. What happens to K_{M} and to V_{max}?",
           M, 2.0, 12.5, 0.6, size=19, font=HEAD, color=MINT)
    for i, (lab, opt) in enumerate([
            ("A", "Both double — they are both properties of the reaction."),
            ("B", "V_{max} doubles; K_{M} is unchanged."),
            ("C", "K_{M} doubles; V_{max} is unchanged."),
            ("D", "Neither changes. Both are constants of the enzyme.")]):
        y = 2.9 + i * 0.78
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.52, fill=CYAN, line=None)
        d.text(s, lab, M, y + 0.11, 0.55, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.08, 11.6, 0.4, size=16, color=WHITE)
    d.foot(s, "Both definitions are on the board. Vote, argue, vote again — then one more question about the same two numbers.", 6.15)
    d.notes(s, "Answer B. V_max = k_2 E_tot doubles; K_M = (k_-1 + k_2)/k_1 "
               "contains no E.\n"
               "A is the majority first answer: both symbols read as 'enzyme "
               "properties' without looking at what they are made of.\n"
               "D: K_M is a constant of the enzyme; V_max is a constant of the "
               "enzyme times how much you put in.\n"
               "After the revote: doubling E_tot also doubles E_tot/(K_M + "
               "S_0). Ask whether the curve they just corrected is still "
               "valid.")

    # 8 THE TWO REGIMES -------------------------------------------------------
    s = d.light()
    d.header(s, "38 – 42 min", "So how far can you push it?")
    d.title(s, "Nothing about the enzyme changed. Only how much of it.")
    d.image(s, "figures/build/s04_qssa_regimes.png", M, 1.6, 12.5, 3.9)
    d.text(s, "Left: E_{tot}/(K_{M}+S_{0}) = 0.0005, and the two curves are one curve. Right: 0.48 — a third of the substrate is sitting in ES, and Michaelis–Menten puts half-completion at 0.60 τ when the truth is 0.85 τ.",
           M, 5.65, 12.5, 0.55, size=15, color=BODY)
    d.foot(s, "Both panels run for the same number of characteristic times τ = (K_{M}+S_{0})/V_{max}, so the comparison is like for like. A fixed wall-clock window would compare integration windows instead.", 6.4)
    d.notes(s, "Ask which panel is which before saying. The shapes are "
               "identical and the only cue is the label.\n"
               "Both panels run to twelve turnovers. PS1 Q3c runs five "
               "turnovers in every case, so their numbers are these numbers.\n"
               "tau goes inversely with E_tot, so a fixed t_end measures the "
               "approximation in one case and the integration window in the "
               "other. A fixed output grid spread over too long a window "
               "misses the peak error.")

    # 9 THE ERROR IS A RATIO --------------------------------------------------
    s = d.light()
    d.header(s, "42 – 46 min", "Turning a condition into a tolerance")
    d.title(s, "The error is set by one number")
    d.image(s, "figures/build/s04_qssa_error.png", M + 2.4, 1.42, 7.7, 3.22)
    d.text(s, "Slope one below 0.05. Pick your tolerance, read off the enzyme: 1% needs E_{tot}/(K_{M}+S_{0}) = 0.028, here E_{tot} = 0.058.",
           M, 4.74, 12.5, 0.38, size=17, font=HEAD, bold=True, color=INK)
    for i, (k, txt) in enumerate([
            ("You can see it in the data too",
             "fit Michaelis–Menten to progress curves at several E_{tot}. Inside the regime K_{M} comes back constant; outside it drifts — 1.10, 1.23, 3.01 at E_{tot} = 0.001, 0.1, 1.0. A constant of the enzyme that moves with how much you pipetted is the model failing."),
            ("Then the harder question",
             "you have priced the structural error at 1%. Do you know K_{M} to 1%? Reported values for one enzyme differ severalfold between labs — below that, tightening the approximation buys nothing.")]):
        y = 5.32 + i * 0.86
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.11, 0.74, fill=TEAL, line=None)
        d.text(s, k, M + 0.34, y + 0.02, 3.5, 0.6, size=14, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 4.1, y, 8.3, 0.8, size=13, color=BODY)
    d.notes(s, "Slope one across four decades: the error is first-order in the "
               "small parameter, which is what the epsilon argument predicted.\n"
               "Pick the error you can live with, read off the ratio, and that "
               "is a design constraint. 1% at E_tot = 0.058, 5% at E_tot = "
               "0.30 - about sixty times the assay concentration in hand "
               "before 1%, three hundred before 5%.\n"
               "PS1 Q3c is two points of this figure; Q3d connects them to the "
               "condition.\n"
               "The drift is the experimental version of the whole "
               "session, and it redeems option C of the last vote. Fit MM "
               "to progress curves at several E_tot: apparent K_M = 1.10 "
               "at E_tot = 0.001, 1.23 at 0.1, 3.01 at 1.0, against a true "
               "1.10. Apparent V_max drifts too, 0.149 against k_2 E_tot = "
               "0.100. So C was not simply wrong - in the model it is "
               "wrong, and at the bench outside the valid regime K_M "
               "really does climb with enzyme.\n"
               "The point to land: parameters fitted outside the regime "
               "belong to the assay, not the enzyme. That is why anyone "
               "quoting a K_M has to quote the conditions.\n"
               "Then the budget question. 1% structural error is only "
               "worth having if K_M is known better than 1%, and it is "
               "not. Chasing structural error below parameter uncertainty "
               "is wasted work, and that judgement is the engineering.\n"
               "Ask: what does a slope of one mean?")

    # 10 PAUSE ----------------------------------------------------------------
    # Was "compare notes with the person next to you". Adam's read of the room
    # is that open-ended pair-compare falls flat here, and the cohort explains
    # why: biology, chemistry, physics and engineering backgrounds sitting side
    # by side means one partner explains and the other receives, so it becomes
    # tutoring rather than retrieval, and the weaker retrieval is the one that
    # needed the practice. The vote-argue-vote ConcepTests keep peer work,
    # because there the argument has a target - convince someone of an answer.
    # This pause has no target, so it is now individual, written, and collected.
    s = d.dark()
    d.header(s, "46 – 48 min", "Two minutes  ·  written  ·  on your own")
    d.title(s, "Two minutes. On paper, on your own.")
    for i, (n, q) in enumerate([
            ("1", "What does the QSSA assume? Write the condition, not the words."),
            ("2", "What is K_{M} made of?"),
            ("3", "One line on whatever is still murky. This one is for you, not for me.")]):
        y = 2.15 + i * 0.85
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.6, fill=CYAN, line=None)
        d.text(s, n, M, y + 0.14, 0.5, 0.35, size=16, bold=True, color=INK,
               align="c")
        d.text(s, q, M + 0.85, y + 0.1, 11.6, 0.5, size=18, color=WHITE)
    d.text(s, "No conferring. If you cannot answer 1 without looking, that is the answer to 3.",
           M, 4.85, 11.9, 0.5, size=16, italic=True, color=MINT)
    d.text(s, "Keep it. Then: handouts.", M, 5.6, 11.9, 0.5,
           size=22, font=HEAD, bold=True, color=CYAN)
    d.foot(s, "Nothing to hand in. This one is only useful if it is honest.", 6.3)
    d.notes(s, "Their own paper, and it stays with them. Nothing is "
               "collected - lecture-design 5c.\n"
               "Say nothing for the full two minutes. Stand at the back.\n"
               "Question 3 is for them, not for you. The read on the room comes "
               "from the two vote distributions, which is why those get "
               "written down.\n"
               "Hand the paper out during the second minute.")

    # 11 THE FADED SET --------------------------------------------------------
    s = d.light()
    d.header(s, "48 – 58 min", "Handout  ·  items 1 and 2  ·  ten minutes")
    d.title(s, "Where a regulation function comes from")
    for i, (n, k, txt, c) in enumerate([
            ("1", "Fully worked — one site",
             "P + X ⇌ PX. Write the equilibrium, form the fraction, cancel what you cannot measure. Read it; do not copy it.", TEAL),
            ("2", "The last step is yours — n sites, all or nothing",
             "The same four steps with n copies of X. You finish it, and you say what K is — because it is not K_{d}.", CYAN),
            ("3", "We start it at 62 min — what n buys you",
             "The fold-change in X from 10% to 90% occupancy. PS1 Q4b asks you to use it.", MUTED),
            ("4", "We derive it together at 67 min  ·  247",
             "Four states, a partition function, two independent identical sites. PS1 Q5 wants it written up — and what it means for reading a measured n.", MUTED)]):
        y = 1.85 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.9, fill=c, line=None)
        d.text(s, n, M, y + 0.26, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 4.4, 0.4, size=15, font=HEAD, bold=True,
               color=INK if i < 2 else MUTED)
        d.text(s, txt, M + 5.4, y + 0.02, 6.9, 0.9, size=14,
               color=BODY if i < 2 else MUTED)
    d.text(s, "Ten minutes, and only the first two. We start items 3 and 4 together after the break; the problem set is where you finish them.",
           M, 6.45, W - 2 * M, 0.45, size=15, bold=True, color=INK)
    d.notes(s, "Item 1 is worked. They read it, and start at item 2 if the "
               "first is obvious.\n"
               "Items 3 and 4 are PS1, due Thursday. They stay unworked here.\n"
               "While circulating, watch for K = K_d in item 2. It is K = "
               "K_d^(1/n).\n"
               "Say: 'Ten minutes. Items one and two only.'")

    # 12 THE ANSWERS ----------------------------------------------------------
    s = d.light()
    d.header(s, "58 – 62 min", "The answers  ·  items 1 and 2")
    d.title(s, "Both are Hill functions. Only one has an honest K.")
    for i, (n, ans, prompt, c) in enumerate([
            ("1",
             "f = (x/K_{d}) / (1 + x/K_{d}) = x / (K_{d} + x).  A Hill function with n = 1 and K = K_{d}.",
             "[P] cancelled because it appears in every term of both numerator and denominator — it is the reference state. It would not cancel if the promoter could be in a state that is neither empty nor bound by X, which is exactly what session 6 is about.",
             TEAL),
            ("2",
             "f = x^{n} / (K_{d} + x^{n}) = x^{n} / (K^{n} + x^{n})  with  K = K_{d}^{1/n}.",
             "K is the concentration at half occupancy. K_{d} here is an equilibrium constant with units of (concentration)^{n}, so it cannot itself be a half-point. Two promoters with the same K and different K_{d} differ in n: same switch point, different sharpness.",
             CYAN)]):
        y = 1.9 + i * 2.0
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 1.6, fill=c, line=None)
        d.text(s, n, M, y + 0.6, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, ans, M + 0.8, y, 11.7, 0.5, size=15, font=HEAD, bold=True,
               color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, M + 0.8, y + 0.58, 0.1, 0.95,
                fill=MUTED, line=None)
        d.text(s, prompt, M + 1.15, y + 0.55, 11.35, 1.0, size=14, color=BODY)
    d.text(s, "Item 2 assumed empty or full, nothing between. That is an idealization, and the next ten minutes are what it costs you.",
           M, 6.3, W - 2 * M, 0.45, size=16, font=HEAD, bold=True, color=INK)
    d.notes(s, "Take both from the room before showing them.\n"
               "K = K_d^(1/n). K_d in item 2 has units of concentration^n, so "
               "it cannot be a concentration and cannot be the half-point. "
               "Units catch it before algebra does.\n"
               "[P] cancels in item 1 because it appears in every term of "
               "numerator and denominator. It would not cancel if the promoter "
               "could sit in a state that is neither empty nor bound - session "
               "6.")

    # 13 SENSITIVITY ----------------------------------------------------------
    s = d.light()
    d.header(s, "62 – 67 min", "At the board  ·  what n is for")
    d.title(s, "A Hill coefficient measures sensitivity")
    d.image(s, "figures/build/s04_hill_family.png", M + 1.8, 1.55, 9.0, 4.15)
    d.text(s, "Set f = 0.1 and f = 0.9, solve each for x:   x_{10} = K (1/9)^(1/n),  x_{90} = K (9)^(1/n)   ⇒   x_{90}/x_{10} = 81^(1/n)",
           M, 5.8, 12.5, 0.45, size=17, font=TEXT, bold=True, color=INK)
    d.foot(s, "Note which K: this is the HALF-OCCUPANCY constant of the binding curve, not the Michaelis constant K_{M} of an enzyme rate law. Read the table as a spec — a switch that must go 10% → 90% on a three-fold input change needs n ≈ 4.", 6.4)
    d.notes(s, "Four lines at the board. PS1 Q4b asks for it analytically and "
               "forbids a numerical search.\n"
               "x_10 = K(1/9)^(1/n), x_90 = K(9)^(1/n), so x_90/x_10 = "
               "81^(1/n). K cancels.\n"
               "n = 1 needs an eighty-one-fold change in input to go from a "
               "tenth on to nine tenths on. n = 2 needs nine-fold, n = 4 "
               "three-fold.\n"
               "Run it backwards and it is a design spec: the circuit has "
               "to switch on a three-fold change in input, so you need n "
               "of about 4, so you need cooperativity, so you go looking "
               "for a protein that has it. That direction - requirement to "
               "mechanism - is the one they will use in the project.\n"
               "Session 9's bistability condition is alpha_c = "
               "n(n-1)^-((n+1)/n), infinite for n <= 1.\n"
               "Ask: where did K go?")

    # 14 INDEPENDENT SITES ----------------------------------------------------
    s = d.light()
    d.header(s, "67 – 72 min", "At the board  ·  the idealization, priced")
    d.title(s, "Two independent sites give n = 1")
    d.image(s, "figures/build/s04_independent_sites.png", M + 1.8, 1.5, 9.0, 4.1)
    for i, (k, txt) in enumerate([
            ("Four states, and each gets a statistical weight",
             "Z = 1 + 2w + w² = (1 + w)² with w = x/K_{d}. Occupancy = w(1+w)/(1+w)² = w/(1+w). The square cancels."),
            ("So n counts cooperativity, not sites",
             "and the sites must be IDENTICAL too — two independent sites with different K_{d} give n < 1. n ≤ number of sites, with equality only for infinitely strong cooperativity, which no real protein has.")]):
        y = 5.7 + i * 0.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.1, 0.42, fill=AMBER, line=None)
        d.text(s, k, M + 0.32, y - 0.02, 4.4, 0.4, size=14, font=HEAD,
               bold=True, color=INK)
        d.text(s, txt, M + 4.9, y - 0.02, 7.4, 0.45, size=13.5, color=BODY)
    d.notes(s, "Write the four states as a column before writing Z. With w = "
               "x/K_d: Z = 1 + 2w + w^2 = (1+w)^2, and site occupancy is "
               "w/(1+w).\n"
               "This is a partition function, and it is session 6 a week "
               "early. PS1 Q5 asks 247 for it.\n"
               "Make them say which fraction they mean. 'Fraction of sites "
               "occupied' is w/(1+w). 'Fraction of promoters with at least one "
               "site bound' is 1 - 1/(1+w)^2, which is not a Hill function.\n"
               "N independent identical sites give (1+w)^N and site occupancy "
               "w/(1+w), always.\n"
               "Ask: so what does a fitted n of 1.9 tell you?")

    # 15 CONCEPTEST 2 ---------------------------------------------------------
    s = d.dark()
    d.header(s, "72 – 76 min", "Vote  ·  argue  ·  vote again")
    d.title(s, "A dose–response fits a Hill coefficient of 1.9.")
    d.text(s, "Output against input, measured on the circuit you built. Clean data, a good fit, a well-behaved protein.",
           M, 2.0, 12.5, 0.5, size=19, font=HEAD, color=MINT)
    for i, (lab, opt) in enumerate([
            ("A", "Two."),
            ("B", "At least two — n can never exceed the site count."),
            ("C", "Exactly one — 1.9 is within error of a single site."),
            ("D", "Nothing: a dose–response bounds the site count neither above nor below.")]):
        y = 2.8 + i * 0.78
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.52, fill=CYAN, line=None)
        d.text(s, lab, M, y + 0.11, 0.55, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.08, 11.6, 0.4, size=16, color=WHITE)
    d.foot(s, "Careful: what you measured is not the quantity the last slide was about.", 6.15)
    d.notes(s, "ANSWER D, and the reason has two halves. Get both.\n"
               "NO CEILING: n <= number of sites holds for an equilibrium "
               "BINDING curve, which is what the last slide was about. Fine.\n"
               "NO FLOOR, and this is the half nobody expects: a dose-response "
               "is binding plus everything downstream of it, and downstream "
               "steps sharpen. Zero-order ultrasensitivity in a "
               "phosphorylation cycle gives an apparent n above 20 from ONE "
               "site; so does titration by a decoy. Both are session 13. So a "
               "fitted 1.9 does not put a floor under anything.\n"
               "B is the majority answer and it is the one to spend the time "
               "on. It is exactly right for the curve on the previous slide "
               "and wrong for the quantity in this stem, which is the whole "
               "point: WHICH CURVE DID YOU MEASURE?\n"
               "A ignores the last slide entirely.\n"
               "C misreads the question rather than the biology.\n"
               "The transferable habit: before you read anything off a Hill "
               "coefficient, ask whether the y axis is occupancy or output.\n"
               "If someone argues that D is too strong because in practice you "
               "usually know the readout is close to occupancy - that is the "
               "right argument and it is worth two minutes. The answer is that "
               "you have to KNOW that, and it is a claim about your assay, not "
               "about the fit.")

    # 16 CONSOLIDATION + FORWARD ----------------------------------------------
    s = d.dark()
    d.header(s, "76 – 80 min", "Next")
    d.title(s, "Now: how fast can it change its mind?")
    d.text(s, "Thursday: gene expression dynamics and response time.",
           M, 2.05, 11.6, 0.45, size=22, font=HEAD, bold=True, color=MINT)
    d.text(s, "Today you deleted a variable and priced the deletion. Both rate laws you derived are instantaneous — they have no memory and no clock of their own. Every clock in a circuit is therefore set by the SLOW variables you kept, and there is one you cannot delete and cannot slow down.",
           M, 2.55, 11.6, 1.15, size=16, color=WHITE, spacing=1.35)
    d.text(s, "How quickly can a cell change the concentration of a protein — and what sets the floor?",
           M, 3.85, 11.6, 0.4, size=17, bold=True, color=CYAN)
    bottom = d.assignment(s, y=4.45)
    d.text(s, "PS1 is due Thursday. Q3 and Q4 are today's material; Q5 is handout item 4, which we derive at 67 min — its marks are in the interpretation, not the algebra.",
           M, bottom + 0.1, 11.6, 0.35, size=15, bold=True, color=SILVER)
    d.notes(s, "Last two minutes: notes closed, one sentence each on the three "
               "questions from the goals slide.\n"
               "Assign the reading out loud: Andersen 1998, seven pages, "
               "Figure 3A. Files > readings on bCourses, filed as 'Session 05 "
               "- andersen-1998'.\n"
               "Leave the forward question unanswered.")

    return d
