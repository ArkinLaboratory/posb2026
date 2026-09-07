"""Session 8 — The phase plane: nullclines, fixed points, and linear stability.

Tuesday 22 September. **SPINE ONLY, 7 September 2026** — the three derivation
runs and the frame around them, built early and deliberately. This is the test
case named in docs/lecture-design.md §5c: the highest element-interactivity
content in Part I, in the session where the cohort is thinnest, built with
slide-resident derivations to find out whether the format survives it.

Still to add before 22 September: the generation opener, the figures (nullcline
plot, trace-determinant chart, the toggle's three fixed points), the faded
handout and its answer sheet, and the board notes for the ledger.

WHY THIS SESSION IS THE HARD ONE
docs/deck-triage.md §3: across all 962 pages of the 2025 corpus, `nullcline`,
`Jacobian`, `eigenvalue` and `bifurcation` each appear ZERO times. The
vocabulary is absent, not thin. Of 21 onboarding respondents, 5 had ever seen a
phase portrait. Twenty coverage-matrix points are assessed on it.

THE RUNNING EXAMPLE IS THE TOGGLE, ON PURPOSE
    du/dt = a/(1+v^n) - u        dv/dt = a/(1+u^n) - v
Gardner 2000 is read BEFORE this session (assigned in s07, 7 Sep change), so
the algebra lands on a circuit the room has already met. Session 9 takes the
same paper apart as biology.
The symmetric fixed point u = v = x satisfies x + x^(n+1) = a; the Jacobian
there is [[-1,-b],[-b,-1]] with b = n x^(n+1)/a, so the eigenvalues are -1 +/- b
and it loses stability at b = 1. That gives

    x_c = (n-1)^(-1/n)        a_c = n (n-1)^(-(n+1)/n)

VERIFIED NUMERICALLY 7 Sep: b = 1.0000 at n = 2, 3, 4, 8, and x + x^(n+1) = a_c
to four figures in every case. n = 2 gives x_c = 1, a_c = 2.

That is the same alpha_c session 4 quotes as a forward reference and session 9
uses. **This session is where it gets derived**, which is what makes the phase
plane worth eighty minutes rather than a definition slide.

Coverage matrix: T18, T19, T20.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session08_Phase_Plane"


def build():
    d = Deck("Session 8 — The phase plane", session=8)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 8", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "The phase plane", M, 2.72, 9.4, 1.3,
           size=40, font=HEAD, bold=True, color=WHITE)
    d.text(s, "Two equations, no solution, and everything you need anyway",
           M, 4.15, 9.4, 0.5, size=17, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Five of twenty-one said they had seen a phase portrait. Assume "
               "nobody has.\n"
               "The promise to make at the door: by the end of today you will "
               "know whether a two-gene circuit is a switch WITHOUT solving "
               "anything, and you will have done it for the toggle you are "
               "reading about for Thursday.")

    # 2 THE PROBLEM -----------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 6 min", "Retrieval  ·  notes closed")
    d.title(s, "Why you cannot do what you did in session 5")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.8, W - 2 * M, 1.25, fill=WASH,
            line=RULE, lw=1)
    d.text(s, "du/dt  =  a / (1 + v\^{n})  \\u2212  u                    dv/dt  =  a / (1 + u\^{n})  \\u2212  v",
           M + 0.3, 2.05, 12.0, 0.5, size=22, font=TEXT, bold=True, color=INK)
    d.text(s, "Two genes, each repressing the other. This is the toggle from Gardner, Cantor & Collins — the paper you read for today.",
           M + 0.3, 2.58, 12.0, 0.35, size=14, italic=True, color=MUTED)
    for i, (n, q) in enumerate([
            ("1", "In session 5 you solved dp/dt = \\u03b1 \\u2212 (\\u03b3+\\u03bc)p in one line. Try the same move here. Where exactly does it fail?"),
            ("2", "You want to know whether this circuit is a switch. Write down what \\u201cis a switch\\u201d means as a statement about solutions."),
            ("3", "From session 4: a Hill coefficient of n. What did n buy you, in one sentence?")]):
        y = 3.35 + i * 0.95
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.75, fill=TEAL, line=None)
        d.text(s, n, M, y + 0.2, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, q, M + 0.8, y, 11.7, 0.8, size=16, color=BODY)
    d.text(s, "Three minutes in writing. Nobody solves these equations today, including me.",
           M, 6.35, W - 2 * M, 0.4, size=15, bold=True, color=INK)
    d.notes(s, "Q1: the equations are coupled and nonlinear. Separation of "
               "variables fails at the first step because du/dt depends on v. "
               "There is no closed form and there is not going to be one.\n"
               "Q2 is the one to spend time on. 'Is a switch' means: more than "
               "one stable steady state, and which one you end up in depends on "
               "where you started. Get that sentence out of the room before you "
               "give them any machinery, because the whole session is a method "
               "for checking it.\n"
               "Q3: n is a sensitivity - 81^(1/n) from session 4. It will turn "
               "out to be the thing that decides whether this is a switch at "
               "all.\n"
               "LEDGER, left wing, up all period: the two equations above.")

    # 3 GOALS -----------------------------------------------------------------
    s = d.light()
    d.header(s, "6 – 9 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By the end you should be able to answer")
    for i, g in enumerate([
            "Given two coupled equations you cannot solve, how do you find where the system can sit still?",
            "Having found such a point, how do you know whether the system stays there when you nudge it?",
            "The toggle has a Hill coefficient n. For which n is it a switch at all — and can you get the number?"]):
        y = 2.2 + i * 1.25
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.95, size=18, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.9, W - 2 * M, 0.85, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "The third one has an exact answer, you will derive it today, and session 4 quoted it at you three weeks ago without proof.",
           M + 0.3, 6.12, 11.6, 0.5, size=16, bold=True, color=INK)
    d.notes(s, "The third question is the session's spine and the reason it is "
               "worth a whole period.\n"
               "Session 4 slide 13 quoted alpha_c = n(n-1)^(-(n+1)/n) as a "
               "forward reference. Today it gets derived. Say that - a promise "
               "kept three weeks later is worth more than the algebra.")

    # 4 RUN 1 — NULLCLINES ----------------------------------------------------
    d.derivation(
        None, "9 – 19 min", "Built one line at a time",
        "Where can the system sit still?",
        [("Sitting still means both derivatives vanish at once",
          "du/dt = 0   AND   dv/dt = 0",
          "two conditions, two unknowns \u2014 so expect isolated points, not a curve"),
         ("Take them one at a time. Each gives a CURVE, not a point",
          "du/dt = 0   \u21d2   u  =  a / (1 + v^{n})",
          "the u-nullcline: every state on it has u momentarily unchanging"),
         ("And the other one",
          "dv/dt = 0   \u21d2   v  =  a / (1 + u^{n})",
          "the v-nullcline. On it, v is unchanging \u2014 but u need not be"),
         ("A fixed point is where a state satisfies BOTH",
          "fixed points  =  intersections of the two nullclines",
          "which is why you draw them: the intersections are visible before any algebra")],
        closing="Two curves in the (u,v) plane. Their intersections are the states the circuit can rest in.",
        note=("Draw the axes before anything else and keep them: u on the "
              "horizontal, v on the vertical. Everything today lives in this "
              "plane.\n"
              "The move students miss is that a nullcline is a curve, not a "
              "point. On the u-nullcline u is momentarily still and v is "
              "moving. Say that twice.\n"
              "The u-nullcline is decreasing in v and the v-nullcline is "
              "decreasing in u, so the picture is two hyperbola-ish curves that "
              "can cross once or three times. That count is the whole session.\n"
              "LEDGER, left wing: the two nullcline equations, beneath the two "
              "ODEs. Every later step points back at them.\n"
              "Ask: can two decreasing curves cross more than once?"))

    # 5 RHYTHM 1 --------------------------------------------------------------
    s = d.light()
    d.header(s, "19 – 25 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "How many times can those two curves cross?")
    d.text(s, "Both nullclines are smooth and decreasing. Sketch them on paper for n = 1 and for n = 4, then vote.",
           M, 1.95, 12.5, 0.5, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "Exactly once, always \u2014 they are both decreasing."),
            ("B", "Once or three times, depending on n and a."),
            ("C", "Any number, depending on n."),
            ("D", "Twice, by symmetry.")]):
        y = 2.75 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "Four minutes sketching before any vote. A drawing is an argument here, not a decoration.", 6.3)
    d.notes(s, "Answer B. Both curves are decreasing, but their CURVATURE "
               "changes with n: at n = 1 they are gentle and cross once; at "
               "large n they are step-like and can cross three times.\n"
               "A is the majority answer and it is the intuition to break. Two "
               "decreasing curves crossing three times is not obvious until you "
               "have drawn a steep one.\n"
               "D is worth taking seriously out loud: the system IS symmetric "
               "under swapping u and v, and that symmetry is why the "
               "middle crossing always sits on the diagonal. But symmetry does "
               "not force an even count.\n"
               "This is the vote that motivates the next run. Do not resolve "
               "it with algebra - resolve it by asking someone with three "
               "crossings to describe their sketch.\n"
               "Record the distribution.")

    # 6 RUN 2 — FIXED POINTS --------------------------------------------------
    d.derivation(
        None, "25 – 35 min", "Built one line at a time",
        "Getting the crossings without drawing them",
        [("Substitute one nullcline into the other",
          "u  =  a / [ 1 + (a/(1+u^{n}))^{n} ]",
          "one equation, one unknown \u2014 and no longer a system"),
         ("On the diagonal u = v = x it collapses",
          "x  =  a / (1 + x^{n})     \u21d2     x + x^{n+1}  =  a",
          "the symmetric fixed point, and now it is a polynomial you can solve"),
         ("For n = 2 that is a cubic you can do by hand",
          "x + x^{3} = a        a = 2  \u21d2  x = 1",
          "one real root here; the other two crossings are off the diagonal and come in a pair"),
         ("For anything else, hand it to a root finder",
          "brentq(lambda x: x + x**(n+1) - a, lo, hi)",
          "bracket it from the sketch you already drew \u2014 the picture tells the solver where to look")],
        closing="Fixed points are roots of one polynomial. The sketch tells you how many to expect and where to bracket.",
        note=("The substitution is the move: two coupled equations become one "
              "equation in one unknown. It works because each nullcline is "
              "already solved for one variable.\n"
              "The diagonal collapse is worth naming as a use of symmetry "
              "rather than a trick - u <-> v leaves the system unchanged, so a "
              "fixed point on the diagonal is the one you can always find.\n"
              "n = 2, a = 2 gives x = 1 exactly. Do that one on the board; it "
              "is the case they will hand-check on PS3.\n"
              "The bracketing point matters and is the one PS3 marks: an "
              "unbracketed solver finds whichever root it stumbles into, and "
              "the sketch is what tells you there are three.\n"
              "Ask: you now have the points. Which of them will the cell "
              "actually sit in?"))

    # 7 RUN 3 — STABILITY -----------------------------------------------------
    d.derivation(
        None, "35 – 47 min", "Built one line at a time",
        "Nudge it. Does it come back?",
        [("Perturb about a fixed point and keep only the linear term",
          "u = u* + \u03b5_{1} ,   v = v* + \u03b5_{2} ,   \u03b5 small",
          "the same move as session 4: a small parameter, and you drop what it multiplies"),
         ("What is left is linear, and its matrix has a name",
          "d\u03b5/dt  =  J \u03b5 ,      J  =  [[ \u2202f/\u2202u , \u2202f/\u2202v ] , [ \u2202g/\u2202u , \u2202g/\u2202v ]]",
          "the Jacobian, evaluated AT the fixed point \u2014 four numbers, not four functions"),
         ("For the toggle on the diagonal it is symmetric",
          "J  =  [[ \u22121 , \u2212\u03b2 ] , [ \u2212\u03b2 , \u22121 ]] ,      \u03b2 \u2261 n x^{n+1} / a",
          "one number \u03b2 carries the whole coupling. Everything now depends on it alone"),
         ("A linear system decays if its eigenvalues have negative real part",
          "\u03bb  =  \u22121 \u00b1 \u03b2",
          "read straight off a symmetric 2\u00d72 \u2014 no characteristic polynomial needed"),
         ("So the diagonal point is stable exactly when",
          "\u03b2 < 1 ,   i.e.   n x^{n+1} < a",
          "and when \u03b2 crosses 1 it becomes a saddle and two new stable points appear")],
        closing="\u03b2 = 1 is the boundary. Everything left to do is solve \u03b2 = 1 together with x + x^{n+1} = a.",
        note=("The linearisation is session 4's move again and saying so is "
              "worth a minute: small parameter, drop what it multiplies, keep "
              "what survives. They have done this.\n"
              "The Jacobian is FOUR NUMBERS. Students hold it as four "
              "functions and then cannot evaluate anything. Compute one entry "
              "with them and substitute the fixed point immediately.\n"
              "beta = n x^(n+1)/a comes from d/dv of a/(1+v^n) at v = x, using "
              "1 + x^n = a/x to clear the square. Do that step slowly; it is "
              "the only algebra in the run.\n"
              "Eigenvalues of [[-1,-b],[-b,-1]] are -1 +/- b by inspection - "
              "the eigenvectors are (1,1) and (1,-1), which are the symmetric "
              "and antisymmetric perturbations. Name them: the toggle loses "
              "stability to the ANTISYMMETRIC one, which is the two genes "
              "diverging. That is the switch being born.\n"
              "LEDGER: J and lambda = -1 +/- beta.\n"
              "Do not do the trace-determinant classification chart here. It "
              "is the next surface and it is a reference, not a derivation."))


    # 8 THE PAYOFF — alpha_c derived ------------------------------------------
    d.derivation(
        None, "47 – 55 min", "Built one line at a time",
        "The promise session 4 made, kept",
        [("Two equations, two unknowns \u2014 x and a at the boundary",
          "\u03b2 = n x^{n+1} / a = 1        and        x + x^{n+1} = a",
          "the first says the point is marginally stable; the second says it is a fixed point"),
         ("Eliminate a between them",
          "n x^{n+1}  =  x + x^{n+1}     \u21d2     x^{n+1}(n \u2212 1)  =  x",
          "one line of algebra, and every a has gone"),
         ("Solve for x",
          "x^{n}  =  1/(n \u2212 1)     \u21d2     x_{c}  =  (n \u2212 1)^{-1/n}",
          "the concentration at which the switch is born \u2014 and it depends only on n"),
         ("Put it back to get the critical strength",
          "a_{c}  =  x_{c}(1 + x_{c}^{n})  =  n (n \u2212 1)^{-(n+1)/n}",
          "n = 2 gives a_{c} = 2 exactly; n = 3 gives 1.19; n = 4 gives 1.01"),
         ("And read what happens at n = 1",
          "a_{c}  \u2192  \u221e     as     n \u2192 1",
          "no cooperativity, no switch, at any promoter strength whatsoever")],
        closing="a_{c} = n(n\u22121)^{-(n+1)/n}. Session 4 quoted this at you in week 2 without proof. That is the proof.",
        note=("This is the eight minutes the whole session is for. Slow down.\n"
              "Step 2 is the only real algebra and it is one line. Let them do "
              "it.\n"
              "Numbers, verified: n = 2 gives x_c = 1 and a_c = 2 exactly; "
              "n = 3 gives 0.794 and 1.191; n = 4 gives 0.760 and 1.013; n = 8 "
              "gives 0.784 and 0.896.\n"
              "The n -> 1 limit is the sentence to land. (n-1) in the "
              "denominator diverges, so no amount of promoter strength makes a "
              "non-cooperative toggle bistable. That is a HARD design "
              "constraint, derived, not asserted - and it is exactly what "
              "session 4's 81^(1/n) was pointing at.\n"
              "Say it plainly: you were told this in week 2. You have just "
              "proved it. That is what the phase plane buys you."))

    # 9 CLASSIFICATION REFERENCE ----------------------------------------------
    s = d.light()
    d.header(s, "55 – 60 min", "Reference  ·  keep this one")
    d.title(s, "Every 2\u00d72 fixed point, from two numbers")
    d.text(s, "\u03c4 = trace J = \u03bb\u2081 + \u03bb\u2082          \u0394 = det J = \u03bb\u2081\u03bb\u2082          \u03bb = \u00bd [ \u03c4 \u00b1 \u221a(\u03c4\u00b2 \u2212 4\u0394) ]",
           M, 1.85, 12.5, 0.45, size=19, font=TEXT, bold=True, color=INK)
    rows = [("\u0394 < 0", "saddle", "unstable \u2014 one way in, one way out", RED),
            ("\u0394 > 0, \u03c4 < 0, \u03c4\u00b2 > 4\u0394", "stable node", "comes back, no overshoot", TEAL),
            ("\u0394 > 0, \u03c4 < 0, \u03c4\u00b2 < 4\u0394", "stable spiral", "comes back, oscillating \u2014 session 11", TEAL),
            ("\u0394 > 0, \u03c4 > 0", "unstable node or spiral", "leaves", RED),
            ("\u03c4 = 0, \u0394 > 0", "centre (linearly)", "the linear test is not enough here", MUTED)]
    for i, (cond, name, meaning, c) in enumerate(rows):
        y = 2.55 + i * 0.66
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.11, 0.5, fill=c, line=None)
        d.text(s, cond, M + 0.34, y, 4.0, 0.42, size=15, font=TEXT, bold=True,
               color=INK)
        d.text(s, name, M + 4.6, y, 3.2, 0.42, size=15, font=HEAD, bold=True,
               color=c)
        d.text(s, meaning, M + 8.0, y + 0.02, 4.6, 0.42, size=13.5, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.95, W - 2 * M, 0.85, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "The toggle at \u03b2 > 1: \u03c4 = \u22122 < 0 but \u0394 = 1 \u2212 \u03b2\u00b2 < 0. Saddle. Which is why the symmetric state is the one the cell cannot stay in.",
           M + 0.3, 6.15, 11.6, 0.5, size=16, bold=True, color=INK)
    d.notes(s, "This is a reference surface, not a derivation. Do not build it "
               "line by line - hand it to them and use it once.\n"
               "The use is the box: for the toggle, tau = -2 always, and "
               "Delta = 1 - beta^2, so the sign of Delta is the whole story and "
               "it flips exactly at beta = 1. The two criteria agree, which is "
               "worth showing because they will use the tau-Delta version on "
               "PS3 and the eigenvalue version on the midterm.\n"
               "The centre row is the honest caveat: at tau = 0 linearisation "
               "does not decide, and that is where a nonlinear term you dropped "
               "comes back. One sentence, no more - session 11 needs it.")

    # 10 RHYTHM 2 -------------------------------------------------------------
    s = d.light()
    d.header(s, "60 – 68 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "Your toggle has n = 1.8 and a = 5.")
    d.text(s, "You measured both. Is it a switch? Five minutes on paper — you have every formula you need on the board.",
           M, 1.95, 12.5, 0.5, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "Yes \u2014 a = 5 is well above a_{c}."),
            ("B", "No \u2014 n = 1.8 is below 2, so it cannot be."),
            ("C", "Yes, but only just, and a small drop in n would kill it."),
            ("D", "Cannot tell without solving the equations numerically.")]):
        y = 2.75 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "a_{c} = n(n\u22121)^{-(n+1)/n}. Put 1.8 in it. Eyes down to vote.", 6.3)
    d.notes(s, "Answer A. a_c(1.8) = 1.8 * (0.8)^(-2.8/1.8) = 1.8 * "
               "0.8^(-1.556) = 1.8 * 1.415 = 2.55. So a = 5 clears it "
               "comfortably and the circuit IS bistable.\n"
               "B is the majority answer and it is the misconception this "
               "session must kill: n = 2 is not a threshold. The threshold is "
               "on a, and n only sets where it is. Bistability needs n > 1, "
               "not n >= 2.\n"
               "D is the pre-session answer and worth naming as such: you have "
               "just spent an hour learning not to need it.\n"
               "C tests whether they can read the sensitivity - a_c rises "
               "steeply as n approaches 1, so the margin really does vanish. "
               "Have someone compute a_c(1.2) = 1.2 * 0.2^(-1.833) = 21.7, and "
               "then a = 5 is nowhere near enough.\n"
               "Record the distribution.")

    # 11 FORWARD --------------------------------------------------------------
    s = d.dark()
    d.header(s, "68 – 80 min", "Faded set  ·  then next")
    d.title(s, "You just did this to a real circuit")
    d.text(s, "Thursday: bistability, hysteresis, and what Gardner had to build.",
           M, 1.95, 11.6, 0.45, size=22, font=HEAD, bold=True, color=MINT)
    d.text(s, "The system on the board all period is the toggle you read for today. You now have a criterion for whether it switches, you got it without solving anything, and it says the whole design turns on n. Thursday: where in that paper were they fighting for n, and what did it cost them?",
           M, 2.55, 11.6, 1.1, size=16, color=WHITE, spacing=1.35)
    d.assigned_on(M, 3.85, 8.0, s)
    bottom = d.assignment(s, y=4.35)
    d.text(s, "The faded set (68–78) is on your handout: nullclines, fixed points and the Jacobian for a system that is NOT symmetric. PS3 Q1–Q3.",
           M, bottom + 0.15, 11.6, 0.5, size=15, bold=True, color=SILVER)
    d.notes(s, "They read Gardner for TODAY, not for Thursday - moved on "
               "7 September so the algebra lands on a circuit they have met. "
               "Ask early who has read it.\n"
               "SPINE NOTE: the 68-78 faded set is referenced here and not yet "
               "written. It has to break the symmetry - two different Hill "
               "coefficients - because everything derived today used u <-> v "
               "symmetry to get onto the diagonal, and a student who only ever "
               "sees the symmetric case will think the diagonal trick is the "
               "method rather than a convenience.\n"
               "Assign Gardner out loud. The reading question - where are they "
               "fighting for n - is the one that connects today's algebra to a "
               "wet-lab decision, and session 9 opens on it.")

    return d
