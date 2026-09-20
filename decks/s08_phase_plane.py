"""Session 8 — The phase plane: nullclines, fixed points, and linear stability.

Tuesday 22 September. Spine built 7 September; **rebuilt on the split surface
18 September** after Adam named the cause of the ten minutes he loses per
class: the proofs on the slides are not clear enough, so the explaining
happens at the board. The first build had twenty-five surfaces of symbols
about a plane that was never drawn, in a room where 5 of 21 had seen a phase
portrait. Every derivation run now advances a picture alongside the algebra
(`Deck.derivation_fig`, `figures/s08_phase_plane.py`), and the picture is the
one students can regenerate from `posb`.

WHY THIS SESSION IS THE HARD ONE
docs/deck-triage.md §3: across all 962 pages of the 2025 corpus, `nullcline`,
`Jacobian`, `eigenvalue` and `bifurcation` each appear ZERO times. The
vocabulary is absent, not thin. Twenty coverage-matrix points are assessed on it.

THE RUNNING EXAMPLE IS THE TOGGLE, ON PURPOSE
    du/dt = a/(1+v^n) - u        dv/dt = a/(1+u^n) - v
Gardner 2000 is read BEFORE this session, so the algebra lands on a circuit
the room has already met. Session 9 takes the same paper apart as biology.
Worked at n = 2, a = 3 throughout -- NOT a = 2, which is a_c exactly and has
one crossing. At a = 3 the symmetric point is x = 1.2134, the pair is
(0.382, 2.618), and g = n x^(n+1)/a = 1.19 > 1: a saddle.

THE COUPLING NUMBER IS CALLED g, NOT beta (18 September). The 7 September
build called it beta, which is Gardner's name for a cooperativity -- and the
scaling run and the handout both use Gardner's beta and gamma on the same
day. g is positive, g = n x^(n+1)/a, J = [[-1,-g],[-g,-1]], lambda = -1 +/- g.
Session 9 already writes g. If this is reversed, it is one substitution.

The symmetric fixed point u = v = x satisfies x + x^(n+1) = a; the Jacobian
there is [[-1,-g],[-g,-1]], so it loses stability at g = 1, which gives

    x_c = (n-1)^(-1/n)        a_c = n (n-1)^(-(n+1)/n)

VERIFIED NUMERICALLY 7 Sep: g = 1.0000 at n = 2, 3, 4, 8, and x + x^(n+1) = a_c
to four figures in every case. n = 2 gives x_c = 1, a_c = 2. a_c(1.2) = 22.94,
a_c(1.8) = 2.547 (the session README's table).

Coverage matrix: T18, T19, T20.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session08_Phase_Plane"
FIG = "figures/build/"


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
               "anything, and you will have done it for the toggle you read "
               "about.")

    # 2 THE PROBLEM -----------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 6 min", "Retrieval  ·  notes closed")
    d.title(s, "Why you cannot do what you did in session 5")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.8, W - 2 * M, 1.25, fill=WASH,
            line=RULE, lw=1)
    d.text(s, "du/dt  =  a / (1 + v^{n})  −  u                    dv/dt  =  a / (1 + u^{n})  −  v",
           M + 0.3, 2.05, 12.0, 0.5, size=22, font=TEXT, bold=True, color=INK)
    d.text(s, "Two genes, each repressing the other. This is the toggle from Gardner, Cantor & Collins — the paper you read for today.",
           M + 0.3, 2.58, 12.0, 0.35, size=14, italic=True, color=MUTED)
    for i, (n, q) in enumerate([
            ("1", "In session 5 you solved dp/dt = α − (γ+μ)p in one line. Try the same move here. Where exactly does it fail?"),
            ("2", "You want to know whether this circuit is a switch. Write down what “is a switch” means as a statement about solutions."),
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
    d.header(s, "6 – 8 min", "Where we are  ·  what you'll be able to answer")
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

    # 4 RUN 0 — WHERE a AND n COME FROM (Gardner, Box 1) ----------------------
    d.derivation(
        None, "8 – 12 min", "Built one line at a time",
        "Where a and n come from",
        [("The equations as the cell has them",
          "dU/dt  =  α_{1} / (1 + (V/K_{2})^{n})  −  (γ+μ) U",
          "session 7's form: synthesis repressed by the other protein, removal by degradation and dilution. Twice over"),
         ("Measure each repressor in units of its threshold",
          "u ≡ U / K_{1} ,      v ≡ V / K_{2}",
          "K is where the other promoter is half shut — session 4's K; n is session 4's Hill coefficient"),
         ("Measure time in units of the protein lifetime",
          "t′ ≡ (γ+μ) t",
          "ONE lifetime for both proteins. That is an assumption, and Thursday breaks it"),
         ("What survives",
          "du/dt′  =  a_{1} / (1 + v^{n})  −  u ,      a_{1} ≡ α_{1} / [(γ+μ) K_{1}]",
          "a lumps what Box 1 lists: RNAP binding, open complex, elongation, ribosome binding. n: multimerisation and operator binding")],
        closing="Two knobs survive: a = synthesis ÷ (removal × threshold), and the cooperativity n. Gardner writes n as β on one arm and γ on the other.",
        note=("Without this surface every engineerable parameter is invisible "
              "for the whole period: the room sees a and n as given and never "
              "learns what a wet-lab change does to them. This is Gardner's "
              "Box 1 in our notation.\n"
              "a is a ratio: synthesis over removal times threshold. Raise the "
              "promoter, raise a. Tag the protein for degradation, LOWER a. "
              "Change the operator so the repressor binds tighter (smaller K), "
              "raise a. Those are the three knobs, and they all enter through "
              "one number.\n"
              "Symbol collision, say it once and keep them apart on the board: "
              "on this surface gamma+mu is removal, as in session 5, and the "
              "Hill coefficient is n, as in session 4. Gardner's paper calls "
              "the two Hill coefficients beta and gamma. From the next surface "
              "on, nothing today is called gamma except in the handout, where "
              "it is Gardner's, and there is no removal rate in sight.\n"
              "The one-lifetime assumption is what makes the Jacobian symmetric "
              "later. Session 9's ConcepTest tags one repressor with ssrA and "
              "not the other, and then it is not.\n"
              "LEDGER, left wing: a = alpha / ((gamma+mu) K)."))

    # 5 RUN 1 — NULLCLINES ----------------------------------------------------
    d.derivation_fig(
        "12 – 21 min", "Built one line at a time",
        "Where can the system sit still?",
        [("A state is a point. Sitting still means no arrow",
          "du/dt = 0     AND     dv/dt = 0",
          "two conditions, two unknowns — so expect isolated points, not a curve"),
         ("Take the first condition alone. It gives a curve",
          "du/dt = 0   ⇒   u  =  a / (1 + v^{n})",
          "the u-nullcline. On it u is momentarily still — and v is not"),
         ("And the second",
          "dv/dt = 0   ⇒   v  =  a / (1 + u^{n})",
          "the v-nullcline. On it v is still and u is moving"),
         ("A fixed point satisfies both at once",
          "fixed points  =  where the two curves cross",
          "three crossings here. Count them on the drawing before any algebra"),
         ("Everywhere else, the state moves",
          "sign of du/dt, sign of dv/dt   ⇒   the arrow",
          "the flow drains into two of the three crossings. Which two is Run 3")],
        [FIG + "s08_plane_p1.png", FIG + "s08_plane_p2.png",
         FIG + "s08_plane_p3.png", FIG + "s08_plane_p4.png",
         FIG + "s08_plane_p5.png"],
        closing="Two curves. Where they cross, the circuit can rest. Everywhere else it moves.",
        note=("Axes first and keep them: u across, v up. Everything today "
              "lives in this plane.\n"
              "The move students miss is that a nullcline is a curve, not a "
              "point. On the u-nullcline u is momentarily still and v is "
              "moving - the arrow on the drawing is vertical. Say that twice.\n"
              "Both curves are decreasing: more of the other repressor, less "
              "of you. Whether two decreasing curves can cross more than once "
              "is the vote that comes next; do not resolve it here.\n"
              "The last panel is the flow field. Do not explain it yet - it is "
              "there so the room sees that the plane has arrows everywhere and "
              "the fixed points are where the arrows vanish. Run 3 reads it.\n"
              "LEDGER, left wing: the two nullcline equations, beneath the two "
              "ODEs. Every later step points back at them."))

    # 6 RHYTHM 1 --------------------------------------------------------------
    s = d.light()
    d.header(s, "21 – 27 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "How many times can those two curves cross?")
    d.text(s, "Both nullclines are smooth and decreasing. Sketch them on paper for n = 1 and for n = 4, then vote.",
           M, 1.95, 12.5, 0.5, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "Exactly once, always — they are both decreasing."),
            ("B", "Once or three times, depending on n and a."),
            ("C", "Any number, depending on n."),
            ("D", "Twice, by symmetry.")]):
        y = 2.75 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "A drawing is an argument here, not a decoration. Four minutes sketching before any vote.")
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
               "Resolve it by asking someone with three crossings to describe "
               "their sketch, then show the next surface.\n"
               "Record the distribution.")

    # 7 RHYTHM 1 RESOLVED -----------------------------------------------------
    s = d.light()
    d.header(s, "21 – 27 min", "Resolution")
    d.title(s, "Steepness is what n buys you")
    d.image(s, FIG + "s08_crossings.png", M, 1.75, W - 2 * M, 4.85)
    d.foot(s, "Same a = 3 on both. At n = 1 the curves are gentle and meet once; at n = 4 they are step-like and meet three times.")
    d.notes(s, "The picture the vote was about. The open circle in the middle "
               "of the right panel is the crossing the cell will not sit in - "
               "that is the claim of Run 3, so name it now and prove it "
               "later.\n"
               "Steepness is the sensitivity from session 4: 81^(1/n). A Hill "
               "coefficient bends a curve, and a bent curve can cross a "
               "decreasing partner three times.")

    # 8 RUN 2 — FIXED POINTS --------------------------------------------------
    d.derivation_fig(
        "27 – 36 min", "Built one line at a time",
        "Getting the crossings without drawing them",
        [("Substitute one curve into the other",
          "u  =  a / [ 1 + (a/(1+u^{n}))^{n} ]",
          "one equation, one unknown — no longer a system"),
         ("Use the symmetry: one crossing sits on u = v",
          "u = v = x     ⇒     x + x^{n+1}  =  a",
          "swapping u and v leaves the system unchanged, so the diagonal always carries a fixed point"),
         ("For n = 2 it is a cubic. At a = 3:",
          "x + x^{3}  =  3     ⇒     x  =  1.213",
          "the other two crossings are the mirror pair (0.38, 2.62) and (2.62, 0.38)"),
         ("For anything else, hand it to a root finder",
          "brentq(lambda x: x + x**(n+1) - a, lo, hi)",
          "bracket it from the drawing — the picture tells the solver where to look")],
        [FIG + "s08_plane_p4.png", FIG + "s08_diagonal.png", None, None],
        closing="Fixed points are roots of one equation. The drawing says how many, and where.",
        note=("The substitution is the move: two coupled equations become one "
              "equation in one unknown. It works because each nullcline is "
              "already solved for one variable.\n"
              "The diagonal collapse is a use of symmetry, not a trick: "
              "u <-> v leaves the system unchanged, so a fixed point on the "
              "diagonal is the one you can always find. The handout breaks "
              "this symmetry on purpose.\n"
              "a = 3, not 2: at n = 2, a = 2 is EXACTLY the critical value the "
              "session derives in Run 4, and the three crossings collapse to "
              "one. Do not use it as the worked example.\n"
              "The bracketing point is the one PS4 marks: an unbracketed "
              "solver finds whichever root it stumbles into, and the sketch is "
              "what tells you there are three.\n"
              "Ask: you now have the points. Which of them will the cell "
              "actually sit in?"))

    # 9 RUN 3a — LINEARISE ----------------------------------------------------
    d.derivation_fig(
        "36 – 43 min", "Built one line at a time",
        "Nudge it. Does it come back?",
        [("Nudge the fixed point",
          "u = u* + ε_{1} ,     v = v* + ε_{2} ,     ε small",
          "session 4's move: a small parameter, keep what multiplies ε, drop ε²"),
         ("Expand each rate to first order",
          "f(u*+ε_{1}, v*+ε_{2})  ≈  f* + (∂f/∂u) ε_{1} + (∂f/∂v) ε_{2}",
          "and f* = 0 — that is what being a fixed point means"),
         ("What is left is linear, and its matrix has a name",
          "dε/dt = Jε,   J = [[∂f/∂u, ∂f/∂v],[∂g/∂u, ∂g/∂v]]",
          "the Jacobian, evaluated AT the fixed point: four numbers, not four functions"),
         ("Linear means: directions the matrix cannot mix",
          "J e  =  λ e     ⇒     ε along e grows as e^{λt}",
          "an eigenvector is a direction J only stretches. λ says how fast; its sign says which way")],
        [FIG + "s08_perturb_p1.png", None, None, FIG + "s08_perturb_p2.png"],
        closing="Stable means every λ has a negative real part: every direction comes back.",
        note=("The linearisation is session 4's move again and saying so is "
              "worth a minute: small parameter, drop what it multiplies, keep "
              "what survives. They have done this.\n"
              "The Jacobian is FOUR NUMBERS. Students hold it as four "
              "functions and then cannot evaluate anything. The next run "
              "computes the entries for the toggle one at a time.\n"
              "The eigenvector sentence is the one to land: a direction the "
              "matrix only stretches. Along it the linear system is "
              "one-dimensional and session 5 solved it - exponential in, "
              "exponential out. That is why eigenvalues decide everything."))

    # 10 RUN 3b — THE TOGGLE'S JACOBIAN --------------------------------------
    d.derivation_fig(
        "43 – 50 min", "Built one line at a time",
        "The toggle's Jacobian, one entry at a time",
        [("The diagonal entries are easy",
          "∂f/∂u  =  ∂g/∂v  =  −1",
          "each protein removes itself at rate 1 — that is the lifetime we scaled by"),
         ("The off-diagonal one is the only real algebra",
          "∂f/∂v  =  − a n v^{n−1} / (1 + v^{n})^{2}",
          "differentiate a/(1+v^{n}) once, quotient rule"),
         ("Evaluate it at u = v = x, using 1 + x^{n} = a/x",
          "∂f/∂v  =  − a n x^{n−1} · x^{2}/a^{2}  =  − n x^{n+1}/a  ≡  −g",
          "the fixed-point equation clears the square. One number g carries the whole coupling"),
         ("Equal entries on each diagonal: eigenvectors (1,1), (1,−1)",
          "J  =  [[ −1 , −g ] , [ −g , −1 ]] ,     λ  =  −1 ± g",
          "(1,1): both genes up together, λ = −1−g. (1,−1): one up, one down, λ = −1+g"),
         ("Stable exactly when",
          "g < 1 ,     i.e.     n x^{n+1} < a",
          "past g = 1 the antisymmetric direction grows: the two genes diverge, and the switch is born")],
        [FIG + "s08_perturb_p1.png", None, None, FIG + "s08_perturb_p2.png",
         FIG + "s08_perturb_p3.png"],
        closing="g = 1 is the boundary. What is left: solve g = 1 together with x + x^{n+1} = a.",
        board="J = [[−1, −g], [−g, −1]]   and   λ = −1 ± g",
        note=("Step 3 is the only algebra in the run and it deserves the "
              "time: the fixed-point equation 1 + x^n = a/x is what turns "
              "(1+x^n)^2 into a^2/x^2, and everything cancels down to one "
              "number. Say what g is in words: how much a nudge in v shows up "
              "in the rate of u, at the fixed point. It is a loop gain.\n"
              "The eigenvectors are the physics. (1,1) is both repressors "
              "rising together - that is damped by both removals and dies "
              "fastest. (1,-1) is one rising while the other falls, which is "
              "what a switch DOES. The toggle loses stability to the "
              "antisymmetric direction: the two genes diverging is the switch "
              "being born. That sentence is on the surface now; it used to "
              "live only in these notes.\n"
              "g > 1 reads as: loop gain above one. Session 7's positive "
              "autoregulation had the same condition with a slope.\n"
              "Caution that belongs here or Thursday: tau = -2 only because "
              "both removal rates were scaled to 1. Tag one repressor with "
              "ssrA and the diagonal entries differ, J is not symmetric, and "
              "lambda = -1 +/- g is false."))

    # 11 RUN 4 — THE PAYOFF ---------------------------------------------------
    d.derivation_fig(
        "50 – 58 min", "Built one line at a time",
        "The promise session 4 made, kept",
        [("Two equations, two unknowns — x and a at the boundary",
          "n x^{n+1} / a  =  1        and        x + x^{n+1}  =  a",
          "marginally stable, and a fixed point. Two equations, two unknowns"),
         ("Eliminate a",
          "n x^{n+1}  =  x + x^{n+1}     ⇒     x^{n+1} (n − 1)  =  x",
          "one line, and every a has gone"),
         ("Solve for x",
          "x^{n}  =  1/(n − 1)     ⇒     x_{c}  =  (n − 1)^{−1/n}",
          "the concentration at which the switch is born depends only on n. n = 2 gives x_{c} = 1"),
         ("Put it back for the critical strength",
          "a_{c}  =  x_{c} (1 + x_{c}^{n})  =  n (n − 1)^{−(n+1)/n}",
          "n = 2 gives a_{c} = 2 exactly; n = 3 gives 1.19; n = 4 gives 1.01"),
         ("And read what happens at n = 1",
          "a_{c}  →  ∞     as     n → 1",
          "no cooperativity, no switch, at any promoter strength whatsoever")],
        [FIG + "s08_tangent.png", None, None, FIG + "s08_ac_curve_p1.png",
         FIG + "s08_ac_curve_p2.png"],
        closing="a_{c} = n(n−1)^{−(n+1)/n}. Quoted at you in week 2 without proof. That was the proof.",
        board="a_{c} = n (n − 1)^{−(n+1)/n}",
        note=("This is the eight minutes the whole session is for.\n"
              "Step 2 is the only real algebra and it is one line. Let them do "
              "it.\n"
              "The picture on the first three steps: at a = 2 the two curves "
              "touch at (1,1). Say why that is the same statement as g = 1: "
              "the slope of the u-nullcline there is -1/g_1 and of the "
              "v-nullcline -g_2 (in the same axes), so tangency is g_1 g_2 = 1. "
              "Below a_c they cross once, above it three times.\n"
              "Numbers, verified: n = 2 gives x_c = 1 and a_c = 2 exactly; "
              "n = 3 gives 0.794 and 1.191; n = 4 gives 0.760 and 1.013; n = 8 "
              "gives 0.784 and 0.896.\n"
              "The n -> 1 limit is the sentence to land. (n-1) in the "
              "denominator diverges, so no amount of promoter strength makes a "
              "non-cooperative SYMMETRIC toggle bistable. That is a hard design "
              "constraint, derived, not asserted - and it is exactly what "
              "session 4's 81^(1/n) was pointing at.\n"
              "Say 'symmetric' out loud. The handout is Gardner's own device, "
              "which has gamma = 1 on one arm and switches anyway. The "
              "criterion says at least ONE arm needs cooperativity, not both - "
              "and the room will generalise to both unless stopped.\n"
              "Say it plainly: you were told this in week 2. You have just "
              "proved it. That is what the phase plane buys you."))

    # 12 THE SAME PICTURE, IN THE PAPER ---------------------------------------
    s = d.light()
    d.header(s, "58 – 61 min", "The paper  ·  what you just derived, as they drew it")
    d.title(s, "Gardner drew the same region — for two different arms")
    d.paper_figure(s, "gardner2000_fig2cd", M, 1.7, 6.0, 4.6,
                   "Gardner, Cantor & Collins 2000, Fig. 2c,d",
                   "the bistable region in log α₁ vs log α₂; bifurcation lines for β = γ = 1.1, 2, 3")
    d.image(s, FIG + "s08_design_space.png", 7.0, 1.7, 5.6, 4.6)
    d.foot(s, "Inside a wedge, two states. Their axes are our a_{1}, a_{2}; their β, γ are our n, one per arm. The red point is the device they built.")
    d.notes(s, "Left is the paper; right is the same computation from posb, "
               "same axes. The wedge is the bistable region and its edges are "
               "where the curves touch - the tangency condition of Run 4, done "
               "for two different cooperativities.\n"
               "Read the slopes: at large alpha the upper edge has slope beta "
               "and the lower has slope 1/gamma. Cooperativity opens the "
               "wedge. At beta = gamma = 1.1 it is a sliver that needs alpha "
               "near 100 - the n -> 1 wall from the previous surface, seen from "
               "above.\n"
               "The red point is pTAK117: alpha_1 = 156, alpha_2 = 15.6, "
               "beta = 2.5, gamma = 1 (Fig. 5 legend). One arm has NO "
               "cooperativity and it switches. It sits close to the lower "
               "edge, which is why Fig. 5c shows a bimodal population near the "
               "bifurcation. That is Thursday, and the handout.\n"
               "Design reading: to move a point into the wedge you raise "
               "alpha - promoter, RBS, degradation tag - and Gardner did it by "
               "swapping RBS sequences. Six variants, five bistable.")

    # 13 CLASSIFICATION — THE tau-Delta PLANE ---------------------------------
    s = d.light()
    d.header(s, "61 – 65 min", "Reference  ·  keep this one")
    d.title(s, "Every 2×2 fixed point, from two numbers")
    d.image(s, FIG + "s08_tau_delta.png", M, 1.62, W - 2 * M, 4.95)
    d.foot(s, "τ = trace J = λ₁+λ₂,   Δ = det J = λ₁λ₂.   The toggle: τ = −2 always, Δ = 1 − g², and Δ flips sign at g = 1.")
    d.notes(s, "This is a reference surface, not a derivation. Hand it to "
               "them and use it once.\n"
               "The rows, for the record: Delta < 0 is a saddle; Delta > 0 "
               "with tau < 0 is stable, node below the parabola tau^2 = 4 Delta "
               "and spiral above it; tau > 0 leaves; tau = 0 with Delta > 0 is "
               "a centre and the linear test does not decide.\n"
               "The use is the toggle's track: tau = -2 always, Delta = 1 - g^2, "
               "so the sign of Delta is the whole story and it flips exactly at "
               "g = 1. The two criteria agree. They will use the tau-Delta "
               "version on PS4 and the eigenvalue version on the midterm.\n"
               "Two exits from the stable region, and the course visits both: "
               "down through Delta = 0 is the switch (today and Thursday); "
               "across through tau = 0 with Delta > 0 is the oscillator, "
               "session 11. In our scaling tau is set by removal and Delta by "
               "the coupling - both are engineerable.\n"
               "The centre row is the honest caveat: at tau = 0 linearisation "
               "does not decide, and that is where a nonlinear term you dropped "
               "comes back. One sentence, no more - session 11 needs it.")

    # 14 RHYTHM 2 -------------------------------------------------------------
    s = d.light()
    d.header(s, "65 – 72 min", "Pose  ·  paper  ·  silent vote  ·  argue")
    d.title(s, "Your toggle has n = 1.8 and a = 5.")
    d.text(s, "You measured both. Is it a switch? Five minutes on paper — you have every formula you need on the board.",
           M, 1.95, 12.5, 0.5, size=19, font=HEAD, color=INK)
    for i, (lab, opt) in enumerate([
            ("A", "Yes — a = 5 is well above a_{c}."),
            ("B", "No — n = 1.8 is below 2, so it cannot be."),
            ("C", "Yes, but only just, and a small drop in n would kill it."),
            ("D", "Cannot tell without solving the equations numerically.")]):
        y = 2.75 + i * 0.8
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.54, fill=TEAL, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=WHITE,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.09, 11.6, 0.4, size=17, color=BODY)
    d.foot(s, "a_{c} = n(n−1)^{−(n+1)/n}. Put 1.8 in it. Eyes down to vote.")
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
               "Have someone compute a_c(1.2) = 1.2 * 0.2^(-2.2/1.2) = "
               "1.2 * 0.2^(-1.833) = 1.2 * 19.1 = 22.9, and then a = 5 is "
               "nowhere near enough. (The earlier note said 21.7; 22.94 is "
               "right and is the session README's table.)\n"
               "Record the distribution, then show the next surface.")

    # 15 RHYTHM 2 RESOLVED ----------------------------------------------------
    s = d.light()
    d.header(s, "65 – 72 min", "Resolution")
    d.title(s, "n = 2 is not a threshold. a_{c} is.")
    d.image(s, FIG + "s08_ac_curve_p2.png", M, 1.62, 5.6, 4.95)
    d.text(s, "a_{c}(1.8) = 2.55, so a = 5 is a switch with room to spare.\n\n"
              "a_{c}(1.2) = 22.9. The same a = 5 is nowhere near.\n\n"
              "The wall is at n = 1, not n = 2. Bistability needs n > 1 in the symmetric toggle; how much a you need is what n sets.",
           6.7, 1.9, 5.9, 4.4, size=18, color=BODY, spacing=1.3)
    d.foot(s, "Thursday's ConcepTest asks what sets τ, and the handout asks what happens when only one arm has cooperativity.")
    d.notes(s, "The dot is the vote. Read a_c off the curve at 1.8 and at 1.2 "
               "and the two answers are the two ends of C: the margin is "
               "comfortable at 1.8 and gone at 1.2.\n"
               "Design reading: measured n comes from the repressor's "
               "multimerisation and the number of operators - session 6. A "
               "monomeric repressor on a single operator has n near 1 and no "
               "promoter will rescue it.")

    # 16 FORWARD --------------------------------------------------------------
    s = d.dark()
    d.header(s, "72 – 80 min", "Handout  ·  then next")
    d.title(s, "You just did this to a real circuit")
    d.text(s, "Thursday: bistability, hysteresis, and what Gardner had to build.",
           M, 1.95, 11.6, 0.45, size=22, font=HEAD, bold=True, color=MINT)
    d.text(s, "The system on the board all period is the toggle you read for today. You now have a criterion for whether it switches, you got it without solving anything, and it says the design turns on n and a. Thursday: where in that paper were they fighting for a, and what did it cost them?",
           M, 2.55, 11.6, 1.1, size=16, color=WHITE, spacing=1.35)
    d.assigned_on(M, 3.85, 8.0, s)
    bottom = d.assignment(s, y=4.35)
    d.text(s, "The handout on your desk: Gardner's working toggle has γ = 1 on one arm. Your criterion says n ≤ 1 cannot switch. Reconcile. PS4 Q4–Q5 continue it.",
           M, bottom + 0.15, 11.6, 0.5, size=15, bold=True, color=SILVER)
    d.notes(s, "They read Gardner for TODAY. Ask early who has read it.\n"
               "The handout breaks the symmetry: two different Hill "
               "coefficients, because everything derived today used u <-> v "
               "symmetry to get onto the diagonal, and a student who only ever "
               "sees the symmetric case will think the diagonal trick is the "
               "method rather than a convenience. Gardner's own device has "
               "beta = 2.5 and gamma = 1 and it switches - the criterion is "
               "'at least one arm', which Box 1 states and the symmetric "
               "derivation cannot show.\n"
               "The reading question for Thursday - where are they fighting "
               "for a - is the one that connects today's algebra to a wet-lab "
               "decision, and session 9 opens on it.")

    return d
