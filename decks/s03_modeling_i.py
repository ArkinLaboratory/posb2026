"""Session 3 — Modeling Biology I: mass action, stoichiometry, S·v.

Eighty-nine minutes, Thursday 3 September. The first laptops day, and the
session where the course's Python setup arrives. PS1 goes out at the end.

    0–5    retrieval: what session 2 left on the board
    5–8    map + goals as questions
    8–13   mass action, derived from counting collisions          [board]
    13–17  where mass action fails, with the numbers from session 2 [board]
    17–21  the long way: three derivatives, and the redundancy      [board]
    21–26  S and v, assembled entry by entry                        [board]
    26–33  BOTH null spaces — what is conserved, what can flow      [board]
    33–37  ConcepTest 1 — the catalyst, which is the error everyone makes
    37–39  the pause: write S for the cascade, with the trap fresh
    39–48  laptops: three ways to the same answer                   [9 min]
    48–51  debrief at the front — the two things people are stuck on
    51–59  laptops: the cascade, predicting first                   [8 min]
    59–63  the steady state you can get without a computer          [board]
    63–67  the cascade integrated exactly, by integrating factor    [board]
    67–70  what the numbers look like: two clocks
    70–74  nondimensionalise — four parameters become one           [board]
    74–77  the QSSA error, which is what session 4 is about
    77–80  ConcepTest 2 — the knob that moves level and speed together
    80–84  one matrix, three questions
    84–87  PS1, and the forward link
    87–89  close

Twenty-three slides. 21 min of exposition over 8 slides (2.6 min/slide),
31 min of student work in blocks of 4, 2, 9 and 8, and 37 min at a board — for
which board-notes/s03-board-notes.pdf is the script.

ConcepTest 1 sits at 33–37, immediately before the pause, and that placement is
deliberate. It asks for the net stoichiometry of the mRNA in m → m + p; the
pause then asks the room to write S for the cascade, in which that reaction is
the third column. Trap, then use it thirty seconds later, with nothing in
between. An earlier draft put the ConcepTest between the worked example and the
assembly of S, which interrupted the A + B ⇌ C thread to ask about a different
system and then went back.

A FIRST DRAFT OF THIS DECK WAS TOO THIN. It had the reaction list, the matrix,
one conservation law and a qualitative "look, two timescales" -- about
forty-five minutes of content spread over eighty-nine by leaning on the
notebook block. What it was missing was the mathematics that makes any of it
load-bearing, and all four additions are things this room can do:

  * mass action's validity conditions computed, not asserted -- a Damkohler
    number from session 2's diffusion constant, and the copy-number limit,
    which come out disagreeing with each other in an interesting way;
  * the RIGHT null space as well as the left, so "structure versus kinetics"
    has two theorems behind it rather than one;
  * the cascade integrated exactly, so session 4's approximation has something
    to be an approximation TO;
  * nondimensionalisation, which turns four parameters into one and hands
    session 4 its small parameter already defined.

This is a PROCEDURE day but not a faded-set day: the procedure is being built
for the first time, and the fading happens across PS1 rather than within the
period.

The deck and sessions/s03-modeling-i/s03_modeling_i.ipynb are deliberately not
the same thing. The deck carries the derivations — mass action from collisions,
the assembly of S, the null-space argument — because those are the parts worth
doing at a board with everyone watching the same line appear. The notebook
carries the execution. Do not project the notebook and read it out: they have
it open.

Coverage matrix: demonstrates T4 (mass-action rate laws from a reaction list),
T5 (construct S; assemble dx/dt = S·v), T6 (numerical integration with
solve_ivp). All three are assessed on PS1, which is released today. The null
spaces, the exact solution and the nondimensionalisation are ABOVE the matrix's
requirement for this session -- they are demonstrated here and assessed in
session 4's terms, and the 247 half of the room should be told which parts
those are.

Figures come from figures/s03_modeling_i.py, which imports posb and runs the
same code the students run, so a slide cannot drift from what is on their
screens.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session03_Modeling_I"


def build():
    d = Deck("Session 3 — Modeling Biology I", session=3)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 3", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "Modeling Biology I", M, 2.72, 9.4, 1.3, size=40, font=HEAD,
           bold=True, color=WHITE)
    d.text(s, "Mass action, stoichiometry, and  dx/dt = S v",
           M, 4.15, 9.4, 0.5, size=19, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Laptops open from the start today. Say so in the first ten "
               "seconds, because half the room will not have brought one "
               "otherwise and the middle twenty-four minutes need it. "
               "PS1 goes out at the end of this session and is due Thursday "
               "10 September. Everything on it is demonstrated today or in "
               "session 4 -- say that out loud; it is the contract. "
               "If DataHub is down, the Colab badge in the notebook works "
               "from any browser and is the fallback. Check both before class.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "Two numbers from Tuesday, without looking")
    for i, (q, hint, c) in enumerate([
            ("How many molecules is 1 nM in an E. coli?",
             "The one number from session 2.", TEAL),
            ("A protein crossing the cell, or the gene being transcribed — which is faster, and by how much?",
             "You put this on an axis.", TEAL),
            ("Why does a perfectly stable protein still disappear?",
             "Nothing outruns it.", CYAN)]):
        y = 2.15 + i * 1.3
        d.shape(s, S.OVAL, M, y, 0.42, 0.42, fill=c, line=None)
        d.text(s, str(i + 1), M, y + 0.08, 0.42, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, q, M + 0.75, y - 0.02, W - 2 * M - 0.75, 0.6, size=17,
               color=BODY)
        d.text(s, hint, M + 0.75, y + 0.62, 8.0, 0.3, size=11.5, italic=True,
               color=MUTED)
    d.foot(s, "Two minutes in writing, then say them out loud. Spaced retrieval is the cheapest thing in this course and it only works if it is uncomfortable.")
    d.notes(s, "Five minutes. Answers: (1) about one molecule per cell -- "
               "0.6, and the point is that it is order one. (2) The protein, "
               "by roughly 300x. (3) Dilution by growth; the doubling time is "
               "a ceiling on any protein's half-life. "
               "Do NOT let this run long. If two people know each answer, "
               "move. The retrieval effect is in the attempt, not in the "
               "discussion.")

    # 3 MAP + GOALS -----------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to do")
    d.title(s, "By 9:30 you should be able to")
    for i, (n, lab) in enumerate([("1", "Specification"), ("2", "The substrate"),
                                  ("3", "Modeling I"), ("4", "Modeling II"),
                                  ("5", "Expression")]):
        x, here = M + i * 2.42, n == "3"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=12, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "Given a list of reactions and nothing else, write down the differential equations — every time, without thinking about it.",
            "Say what part of a model is structure and what part is kinetics, and why anyone would care about the difference.",
            "Find a quantity your model must conserve, and use it to catch the mistake you just made."]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "Three minutes, and questions rather than statements -- "
               "objectives-as-pretest beat objectives-as-declaration (Sana et "
               "al. 2020). "
               "Goal 2 is the one they will not see the value of today and "
               "will in session 20, when the same S gets a completely "
               "different question asked of it. Plant it now, name it then.")

    # 4 MASS ACTION, DERIVED --------------------------------------------------
    s = d.light()
    d.header(s, "8 – 13 min", "At the board  ·  derived, not asserted")
    d.title(s, "Where mass action comes from")
    for i, (step, txt) in enumerate([
            ("The rate is a collision rate",
             "A and B react only when they meet. In a well-mixed volume the number of A–B encounters per second is proportional to how many A there are times how many B there are — double either and you double the encounters."),
            ("So  v = k [A][B]",
             "Everything else — how often an encounter has enough energy, the right orientation, a catalyst present — is lumped into k. That lumping is the whole content of the assumption."),
            ("A coefficient becomes an exponent",
             "If two molecules of P must meet, the encounter rate goes as [P]², not 2[P]. The stoichiometric coefficient enters the flux as a power and the balance as a multiplier. These are different roles for the same number and confusing them is exercise E4.")]):
        y = 1.85 + i * 1.5
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.2, fill=TEAL, line=None)
        d.text(s, step, M + 0.4, y, 3.9, 0.7, size=16, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.6, y + 0.02, 7.6, 1.2, size=13.5, color=BODY)
    d.text(s, "Well mixed, dilute, many molecules. Session 2 spent ninety minutes on a cell that is none of those things — so the next slide puts numbers on all three.",
           M, 6.35, W - 2 * M, 0.4, size=14, bold=True, color=RED)
    d.notes(s, "Seven minutes and do it at the board, not off the slide. "
               "Draw the box, draw two A and three B, count the pairs -- six. "
               "Add one A: nine. The proportionality falls out of counting "
               "pairs and it is worth the ninety seconds. "
               "THE RED LINE IS THE POINT OF THE SLIDE. They have just spent a "
               "session on crowding, on copy numbers of order one, on a "
               "cytoplasm that is 20% protein by weight. Mass action assumes "
               "the opposite of all of it. Say plainly: we use it anyway, it "
               "works remarkably well, and sessions 12 and 21 are where each "
               "assumption gets paid for -- copy number in 12, the "
               "well-mixed-and-unloaded assumption in 21. "
               "A student who asks 'then why are we doing this?' has asked the "
               "right question. The answer is that a model whose assumptions "
               "you can name is a tool; one whose assumptions you cannot is a "
               "guess.")

    # 4b WHERE IT FAILS, WITH NUMBERS -----------------------------------------
    s = d.light()
    d.header(s, "13 – 17 min", "At the board  ·  three assumptions, three numbers")
    d.title(s, "Is mass action allowed in an E. coli?")
    for i, (name, test, num, verdict, c) in enumerate([
            ("Well mixed",
             "Diffusion must beat reaction. Damköhler number Da = τ_mix / τ_rxn, with τ_mix ≈ L²/2D and τ_rxn ≈ 1/(k_on·C).",
             "L = 1 µm, D = 7.7 µm²/s  →  τ_mix ≈ 0.065 s.\nk_on = 10⁸ M⁻¹s⁻¹ at C = 1 nM  →  τ_rxn ≈ 10 s.\nDa ≈ 0.007.",
             "PASSES, by three orders of magnitude. A molecule crosses the cell hundreds of times before it reacts, so there is no spatial gradient to speak of.", TEAL),
            ("Dilute",
             "Activity must be proportional to concentration. Crowding makes that false: excluded volume raises the activity of a large complex above its concentration.",
             "20% protein by weight. Association constants shift\nby up to an order of magnitude for large complexes.",
             "BENDS. k absorbs it, which is fine as long as you never transplant a k measured in vitro into a model of a cell without saying so.", AMBER),
            ("Many molecules",
             "The ODE is the N → ∞ limit. Fractional fluctuations go as 1/√N.",
             "1 nM ≈ 1 molecule per cell.  N = 1.\n1/√N = 1.",
             "FAILS OUTRIGHT. Not approximately — the quantity the ODE integrates does not describe any single cell. Session 12.", RED)]):
        y = 1.72 + i * 1.58
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.35, fill=c, line=None)
        d.text(s, name, M + 0.35, y, 1.75, 0.35, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, test, M + 0.35, y + 0.36, 4.4, 0.95, size=11.5, color=BODY)
        d.text(s, num, M + 5.0, y + 0.02, 3.9, 1.3, size=11, font=TEXT,
               color=INK)
        d.text(s, verdict, M + 9.1, y + 0.02, 3.5, 1.3, size=11.5, bold=True,
               color=c)
    d.foot(s, "Two of the three survive. The one that does not is the one about counting — which is exactly what session 2 said would be the problem.", 6.52)
    d.notes(s, "Six minutes at the board, and it is the slide that makes the "
               "rest of the session honest. Do the Damkohler estimate live; it "
               "is two divisions and they have both numbers from Tuesday. "
               "THE PAYOFF IS THAT THE THREE ANSWERS DISAGREE. Students expect "
               "'is this model valid' to have one answer. It has three, and "
               "the one that fails is not the one anybody guesses -- the "
               "spatial assumption, the one that feels shakiest in a crowded "
               "cell, is the one that passes most comfortably. "
               "So the honest statement of what we are doing for the next ten "
               "weeks: we are integrating the MEAN of a process whose "
               "fluctuations are of order one, and it works because we mostly "
               "ask questions about populations and about whether a design can "
               "work at all. Session 12 is where the mean stops being enough, "
               "and session 21 is where the well-mixed-and-unloaded assumption "
               "goes. "
               "k_on = 10^8 /M/s is diffusion-limited; a typical "
               "protein-protein association is 10^5 to 10^6, which makes "
               "tau_rxn LONGER and Da even smaller, so the conclusion is "
               "robust. Say that if someone challenges the number. "
               "The crowding row is the one with a shelf life -- the size "
               "dependence is real (Valverde-Mendez 2025) but 'up to an order "
               "of magnitude' is a range, not a measurement. Mark it as such.")

    # 5 THE LONG WAY ----------------------------------------------------------
    s = d.light()
    d.header(s, "17 – 21 min", "At the board  ·  every term written out")
    d.title(s, "A + B ⇌ C, and nothing clever")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.75, 12.5, 1.5, fill=WASH, line=RULE,
            lw=1)
    for i, (eq, why) in enumerate([
            ("d[A]/dt  =  − kf[A][B]  +  kr[C]", "consumed forward, made in reverse"),
            ("d[B]/dt  =  − kf[A][B]  +  kr[C]", "identical to A's — same events"),
            ("d[C]/dt  =  + kf[A][B]  −  kr[C]", "the same two terms, opposite signs")]):
        y = 1.88 + i * 0.42
        d.text(s, eq, M + 0.3, y, 6.4, 0.35, size=16, font=TEXT, bold=True,
               color=INK)
        d.text(s, why, M + 7.0, y + 0.03, 5.2, 0.3, size=12, italic=True,
               color=MUTED)
    d.text(s, "Two fluxes. Six terms. Every one of them is one of those two fluxes with a sign in front.",
           M, 3.45, 12.5, 0.4, size=18, font=HEAD, bold=True, color=AMBER)
    for i, (k, txt) in enumerate([
            ("The redundancy is the signal",
             "Three equations that contain no information the reaction list did not already have. Anything you write out by hand three times is something a matrix should be writing for you."),
            ("It gets worse fast",
             "Thirty species and forty reactions is where this course is by November. That is 1200 potential terms, hand-typed, each an opportunity for a sign error you will not find.")]):
        y = 4.05 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.95, fill=AMBER, line=None)
        d.text(s, k, M + 0.4, y, 3.9, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.6, y + 0.02, 7.6, 1.0, size=13, color=BODY)
    d.notes(s, "Six minutes. WRITE THESE THREE LINES ON THE BOARD as you say "
               "them, do not just show the slide. The whole rhetorical move of "
               "the next twenty minutes depends on the room having felt the "
               "repetition, and reading it off a slide is not feeling it. "
               "Ask before you write the third line: 'what is d[C]/dt?' They "
               "will get it. That is the point -- they already know the "
               "content, and what is coming is only bookkeeping.")

    # 6 THE ASSEMBLY ----------------------------------------------------------
    s = d.light()
    d.header(s, "21 – 26 min", "At the board  ·  build it term by term")
    d.title(s, "Two fluxes, one matrix")
    d.text(s, "v₁ = kf[A][B]        v₂ = kr[C]", M, 1.72, 6.0, 0.4,
           size=17, font=TEXT, bold=True, color=INK)
    # The matrix, as a table -- built on the board, revealed here.
    d.shape(s, S.ROUNDED_RECTANGLE, M, 2.25, 4.6, 2.0, fill=WASH, line=TEAL,
            lw=1.5)
    for j, lab in enumerate(["", "v₁  forward", "v₂  reverse"]):
        d.text(s, lab, M + 0.25 + j * 1.5, 2.35, 1.5, 0.3, size=12, bold=True,
               color=MUTED, align="c" if j else "l")
    for i, (sp, row) in enumerate([("A", ("−1", "+1")), ("B", ("−1", "+1")),
                                   ("C", ("+1", "−1"))]):
        y = 2.72 + i * 0.44
        d.text(s, sp, M + 0.25, y, 0.6, 0.3, size=15, font=TEXT, bold=True,
               color=INK)
        for j, val in enumerate(row):
            d.text(s, val, M + 0.25 + (j + 1) * 1.5, y, 1.5, 0.3, size=15,
                   font=TEXT, bold=True,
                   color=TEAL if val.startswith("+") else AMBER, align="c")
    d.text(s, "Sᵢⱼ  =  net molecules of species i made by reaction j",
           M, 4.4, 6.0, 0.3, size=12, italic=True, color=MUTED)
    d.text(s, "dx/dt  =  S v(x)", M + 5.4, 2.5, 7.0, 0.7, size=32, font=HEAD,
           bold=True, color=INK)
    for i, (k, txt, c) in enumerate([
            ("S is structure",
             "A constant integer matrix. It comes straight off the reaction list and does not know about rate constants, concentrations, or time.", TEAL),
            ("v is kinetics",
             "Every parameter and all of the biology. This is the part you argue about, measure, and get wrong.", AMBER)]):
        y = 3.45 + i * 1.05
        d.shape(s, S.ROUNDED_RECTANGLE, M + 5.4, y, 0.12, 0.9, fill=c, line=None)
        d.text(s, k, M + 5.8, y, 2.1, 0.35, size=14, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 7.9, y + 0.02, 4.5, 0.95, size=12, color=BODY)
    d.foot(s, "Session 20 keeps this exact matrix, throws away v entirely, and asks which flux distributions are consistent with steady state. That is flux balance analysis.")
    d.notes(s, "Eight minutes, and build the matrix at the board with the room "
               "calling out entries. Ask for the A row first, then B -- they "
               "will notice it is identical and that is worth naming. Then C. "
               "Then multiply S by v out loud, one row at a time, and watch "
               "the three equations from the previous slide reappear. That "
               "moment is the session. "
               "Say explicitly that this is not notation. The separation is "
               "structural: you can ask questions of S alone (what is "
               "conserved? what fluxes are feasible?) with no kinetics at all, "
               "and that is a whole field.")

    # 7 CONSERVATION ----------------------------------------------------------
    s = d.light()
    d.header(s, "26 – 33 min", "At the board  ·  both null spaces")
    d.title(s, "Two null spaces, and what each one is for")
    for i, (side, algebra, means, dim, c) in enumerate([
            ("LEFT null space",
             "wᵀS = 0   ⟹   d(wᵀx)/dt = wᵀS v = 0,  whatever v is",
             "conserved quantities", "dim  =  n − rank S", TEAL),
            ("RIGHT null space",
             "S v = 0   with v ≠ 0",
             "flux patterns that hold steady state", "dim  =  r − rank S", AMBER)]):
        x = M + i * 6.35
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.72, 6.15, 1.32, fill=WASH,
                line=c, lw=1.5)
        d.text(s, side, x + 0.2, 1.8, 3.0, 0.3, size=12, font=HEAD, bold=True,
               color=c)
        d.text(s, dim, x + 3.4, 1.8, 2.6, 0.3, size=11, font=TEXT, color=MUTED,
               align="r")
        d.text(s, algebra, x + 0.2, 2.16, 5.8, 0.35, size=13.5, font=TEXT,
               bold=True, color=INK)
        d.text(s, means, x + 0.2, 2.60, 5.8, 0.3, size=12.5, italic=True,
               color=BODY)
    d.text(s, "A + B ⇌ C:  S is 3×2 with rank 1, so two conservation laws and one flux mode.        The cascade:  2×4, rank 2 — no conservation laws at all, and two flux modes.",
           M, 3.15, 12.5, 0.35, size=12.5, color=MUTED)
    d.image(s, "figures/build/s03_conservation.png", M, 3.55, 12.5, 2.55)
    d.foot(s, "Two extra lines of code. It has caught more of my modelling errors than every other check combined.", 6.2)
    d.notes(s, "Eight minutes and it is the linear algebra of the session, so "
               "do it on the board. LEFT first: it is three symbols. For "
               "A + B <-> C, w = (1,0,1) and (0,1,1) both kill S, giving "
               "[A]+[C] and [B]+[C]. Ask the room to find them before showing "
               "them. Note rank S = 1 because the two columns are negatives of "
               "each other -- forward and reverse are not independent "
               "reactions, which is worth saying out loud. "
               "RIGHT next, and this is the half that is new to almost "
               "everyone. S v = 0 asks: which patterns of reaction rates leave "
               "every concentration unchanged? For A + B <-> C the answer is "
               "v1 = v2, the obvious one. For the cascade the rank is 2 and "
               "the right null space is 2-dimensional: transcription balancing "
               "mRNA decay, and translation balancing protein decay -- the two "
               "independent balances, read off the matrix without solving "
               "anything. "
               "Then the sentence that makes session 20 make sense: FBA is "
               "the right null space plus bounds plus an objective. Nothing "
               "else. They have now seen the object itself. "
               "The cascade having NO conservation laws is the interesting "
               "case, not a defect -- it is an open system with synthesis and "
               "degradation, so nothing is conserved and rank S = n. Ask what "
               "that means physically before you say it. "
               "THE FIGURE IS THE DIMER, NOT THE BINDING EXAMPLE, on purpose. "
               "P + P <-> P2 with the stoichiometric 2 dropped from the P "
               "equation. Every concentration stays positive, both species "
               "settle, the equilibrium ratio is right -- and [P] + 2[P2] "
               "walks away from its initial value. A first draft of this "
               "figure used a flipped sign instead and the flipped sign sent a "
               "concentration negative, which would have made the caption "
               "false. Worth telling them that, because 'the check that only "
               "catches errors you would have noticed anyway' is a real "
               "failure mode of checking. "
               "This is exercise E4 in the notebook. Do not solve it here.")

    # 8b CONCEPTEST 1 — moved here on purpose ----------------------------------------------------------
    s = d.dark()
    d.header(s, "33 – 37 min", "ConcepTest  ·  vote  ·  argue  ·  vote again")
    d.title(s, "Translation:  m → m + p")
    d.text(s, "What is the net stoichiometry of the mRNA in that reaction?",
           M, 2.0, 12.5, 0.5, size=21, font=HEAD, color=MINT)
    for i, (lab, txt) in enumerate([
            ("A", "−1 — the mRNA is used up making the protein"),
            ("B", "0 — it appears on both sides"),
            ("C", "+1 — a protein appeared, so something was made"),
            ("D", "It depends on whether the ribosome falls off")]):
        y = 2.75 + i * 0.72
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.52, fill=CYAN, line=None)
        d.text(s, lab, M, y + 0.11, 0.55, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, txt, M + 0.85, y + 0.08, 11.6, 0.4, size=16, color=WHITE)
    d.foot(s, "Vote. Then find someone who voted differently and make them change their mind. Then vote again.", 6.05)
    d.notes(s, "Four minutes, and it is the single most useful four minutes "
               "in the session. "
               "Answer B. The notebook calls this 'the single most common "
               "modeling error in the first two weeks' and that is not "
               "rhetoric -- it is the error that shows up on PS1 every year in "
               "some form. "
               "A is the majority answer on the first vote and it comes from a "
               "real intuition: translation does consume something. It "
               "consumes amino acids and GTP, which are not in this model. "
               "That is worth saying, because it makes B a modelling choice "
               "rather than a fact, and modelling choices are what this course "
               "is about. "
               "D is the interesting wrong answer -- if the ribosome DID "
               "destroy the message, the stoichiometry would be -1, and there "
               "are real systems where a message is translated a countable "
               "number of times. Ask what that would change. It changes the "
               "steady state from alpha*k_p/(gamma_m*gamma_p) to something "
               "with no mRNA pool at all. "
               "Do not resolve it before the second vote. "
               "AND DO NOT OVER-RESOLVE IT AFTER. The next two minutes are the "
               "pause, and the pause asks them to write S for the cascade -- in "
               "which m -> m + p is the third column and the answer to this "
               "vote is the entry they are about to write. That adjacency is "
               "the whole reason this sits here rather than twenty minutes "
               "earlier. Land B, say 'you are about to need that', and stop "
               "talking.")

    # 9 THE PAUSE -------------------------------------------------------------
    s = d.dark()
    d.header(s, "37 – 39 min", "Two minutes  ·  I will not say anything")
    d.title(s, "Compare notes with the person next to you")
    d.text(s, "Between you, write down S for the cascade — four reactions, two species — before you open a laptop.",
           M, 2.4, 12.5, 0.9, size=21, font=HEAD, color=MINT)
    d.text(s, "∅ → m        m → ∅        m → m + p        p → ∅",
           M, 3.6, 12.5, 0.5, size=20, font=TEXT, bold=True, color=WHITE)
    d.text(s, "Then: laptops open.", M, 4.7, 12.5, 0.5, size=20, font=HEAD,
           bold=True, color=CYAN)
    d.foot(s, "You will check this against posb in ten minutes. Getting it wrong now is cheaper than getting it wrong on PS1.", 6.4)
    d.notes(s, "SAY NOTHING FOR TWO MINUTES. Stand at the back. "
               "This one has a task attached rather than being open-ended, "
               "because the task is exercise E3 and doing it before the "
               "machine does it is the entire 'nothing in posb is abstracted "
               "away before it has been built by hand' rule. "
               "Walk the room and look for the mRNA column under translation. "
               "A zero there means they got the ConcepTest.")

    # 10 THE NOTEBOOK ---------------------------------------------------------
    s = d.light()
    d.header(s, "39 – 48 min", "Laptops  ·  nine minutes  ·  I circulate")
    d.title(s, "Three ways to the same answer")
    for i, (n, k, txt, c) in enumerate([
            ("1", "The long way", "Type the three derivatives out. Integrate with solve_ivp. This is the version you can defend to anyone.", TEAL),
            ("2", "S and v, by hand", "Build the 3×2 array yourself. Same integration. Check the two agree to 1e-9 — the notebook asserts it.", TEAL),
            ("3", "posb.Model", "Give it the reaction list. Read _build_S; it is nine lines and it does exactly what you just did.", CYAN)]):
        y = 1.9 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.9, fill=c, line=None)
        d.text(s, n, M, y + 0.26, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 3.4, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.4, y + 0.02, 7.9, 0.9, size=13, color=BODY)
    d.text(s, "Nine minutes, and it stops whether or not you are finished — I will give away step 2 at the front before we move on.",
           M, 5.5, W - 2 * M, 0.4, size=16, bold=True, color=INK)
    d.text(s, "If DataHub is slow, use the Colab badge in the notebook. Do not spend this period fighting an environment.",
           M, 6.0, W - 2 * M, 0.4, size=13, italic=True, color=MUTED)
    d.notes(s, "NINE MINUTES, AND STOP ON TIME. This used to be one "
               "twenty-minute block and it should not be: past about ten "
               "minutes the fast half has finished and disengaged and the slow "
               "half has stalled on something you could have said in a "
               "sentence, and neither is being taught. Two short blocks with "
               "three minutes of teaching between them beat one long one. "
               "CIRCULATE -- do not work the notebook at the front. They have "
               "it open; reading it aloud is the one way to waste the period. "
               "Expected trouble, in the order it arrives: (1) people who "
               "cannot get the environment up -- pair them with a neighbour "
               "immediately, do not debug at the front; (2) row order of S not "
               "matching the species order, which is why the notebook passes "
               "species= explicitly; (3) the catalyst zero, again, even after "
               "the ConcepTest. "
               "Note who is stuck. You are about to spend three minutes on "
               "exactly that at the front, so the walk around the room is "
               "reconnaissance, not just help.")

    # 10b DEBRIEF -------------------------------------------------------------
    s = d.dark()
    d.header(s, "48 – 51 min", "Three minutes at the front  ·  then back to it")
    d.title(s, "The two things half the room is stuck on")
    for i, (k, txt) in enumerate([
            ("Row order is not automatic",
             "S has one row per species, and 'per species' means whatever order the constructor chose. That is why the notebook passes species=[\"A\",\"B\",\"C\"] explicitly — so the matrix you built by hand and the matrix posb built can be compared at all. If your np.array_equal fails, check this before you check your signs."),
            ("The zero you keep not writing",
             "Translation is m → m + p. The mRNA row under that column is 0, not −1. We voted on this before the break and it is still the most common error in the room, which is exactly why it is worth saying twice.")]):
        y = 2.2 + i * 1.6
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.35, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.0, 0.8, size=17, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 4.8, y + 0.02, 7.7, 1.4, size=13.5, color=MINT)
    d.text(s, "Now the cascade — eight minutes, and predict before you simulate.",
           M, 5.6, 12.5, 0.5, size=19, font=HEAD, bold=True, color=CYAN)
    d.notes(s, "Three minutes, and the CONTENT OF THIS SLIDE IS NOT FIXED -- "
               "it is written for the two problems that show up every year, "
               "but you have just walked the room and you know what is actually "
               "wrong. Say that instead if it differs. The point of the slide "
               "is that the block gets interrupted by teaching, not that these "
               "particular two things get said. "
               "Do NOT work step 2 at the board. Give the row-order fact and "
               "the catalyst zero, which are facts, and leave the assembly to "
               "them.")

    # 10c LAPTOPS, SECOND BLOCK -----------------------------------------------
    s = d.light()
    d.header(s, "51 – 59 min", "Laptops  ·  eight minutes  ·  the cascade")
    d.title(s, "Four reactions, two species, one prediction first")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.75, 12.5, 0.95, fill=WASH, line=TEAL,
            lw=1.5)
    d.text(s, "∅ →(α) m        m →(γₘ) ∅        m →(kₚ) m + p        p →(γₚ) ∅",
           M + 0.3, 2.0, 11.9, 0.45, size=18, font=TEXT, bold=True, color=INK)
    for i, (n, k, txt, c) in enumerate([
            ("1", "On paper, before anything runs",
             "Set both derivatives to zero and get m* and p* in symbols, then in numbers. Write them down where you can see them.", TEAL),
            ("2", "Then simulate",
             "Build the model, integrate, and compare. If the two disagree, one of them is wrong and you now have thirty seconds of work to find out which.", CYAN),
            ("3", "Then E1",
             "Change α to 20 and predict before running. Then γₚ to 0.1. One sentence: which parameters set the level, and which set the speed?", AMBER)]):
        y = 3.0 + i * 1.05
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.85, fill=c, line=None)
        d.text(s, n, M, y + 0.24, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 3.9, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.9, y + 0.02, 7.6, 0.85, size=13, color=BODY)
    d.text(s, "E2–E4 are for after class. E4 — the dimer and the factor of two — is set for 247, and it is the one worth doing whichever number you are enrolled in.",
           M, 6.3, W - 2 * M, 0.4, size=13.5, italic=True, color=MUTED)
    d.notes(s, "Eight minutes. Again: stop on time. "
               "Item 1 is the one that matters and it is the one they will "
               "want to skip -- circulate looking for people who have opened "
               "the simulation without writing m* down, and make them write it "
               "down. Predicting after the fact is not predicting. "
               "If the room is fast, point the quick finishers at E4 rather "
               "than letting them idle; it is the dimer and the factor of two, "
               "and it is the best exercise in the notebook. The notebook sets "
               "it for 247, but say out loud that any 147 student who wants it "
               "should take it -- a 247-only label reads as 'not for you' to "
               "exactly the undergraduates who would most benefit. "
               "At 59 minutes stop regardless. The next twenty minutes are the "
               "mathematics this block exists to motivate, and they are worth "
               "more than the last two exercises.")

    # 11 THE CASCADE, ON PAPER ------------------------------------------------
    s = d.light()
    d.header(s, "59 – 63 min", "At the board  ·  prediction before plot")
    d.title(s, "The steady state you can get without a computer")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.75, 12.5, 1.72, fill=WASH, line=TEAL,
            lw=1.5)
    for i, (line, why) in enumerate([
            ("dm/dt  =  α − γₘ m  =  0        ⟹        m*  =  α / γₘ",
             "the mRNA does not know the protein exists"),
            ("dp/dt  =  kₚ m* − γₚ p  =  0    ⟹        p*  =  kₚ α / (γₘ γₚ)",
             "so the cascade solves top-down, one line at a time")]):
        y = 1.92 + i * 0.72
        d.text(s, line, M + 0.3, y, 8.4, 0.4, size=15.5, font=TEXT, bold=True,
               color=INK)
        d.text(s, why, M + 0.35, y + 0.36, 8.0, 0.3, size=11.5, italic=True,
               color=MUTED)
    d.shape(s, S.ROUNDED_RECTANGLE, M + 8.9, 1.92, 3.6, 1.42, fill=CARD,
            line=TEAL, lw=1)
    d.text(s, "α = 10   γₘ = 0.5   kₚ = 4   γₚ = 0.05",
           M + 9.05, 2.02, 3.4, 0.3, size=11.5, font=TEXT, color=MUTED)
    d.text(s, "m* = 20        p* = 1600", M + 9.05, 2.44, 3.4, 0.45, size=17,
           font=TEXT, bold=True, color=TEAL)
    d.text(s, "before you ran anything", M + 9.05, 2.94, 3.4, 0.3, size=11,
           italic=True, color=MUTED)
    for i, (k, txt) in enumerate([
            ("All four set the level.  One sets the speed.",
             "Every parameter appears in p*, so all four move it. But the protein approaches p* exponentially with time constant 1/γₚ, and γₚ is the only one in that expression — which means the one knob that changes the speed also changes the level. ConcepTest 2 is about that collision."),
            ("A simulation you cannot check is not evidence",
             "You had both numbers before you ran anything. If the plot had disagreed, one of the two was wrong and you would have known within a minute which — that is the entire reason for predicting first.")]):
        y = 3.75 + i * 1.25
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.05, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.3, 0.7, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 5.0, y + 0.02, 7.2, 1.1, size=13, color=BODY)
    d.notes(s, "Five minutes, at the board, and take it from the room. "
               "The move worth naming is that a cascade solves top-down: m* "
               "does not contain p, so you solve for it alone and substitute. "
               "That is the first appearance of a structure they will use "
               "constantly, and in session 4 it becomes the quasi-steady-state "
               "approximation applied on purpose rather than noticed by luck. "
               "If someone points out that p* has no dependence on the initial "
               "conditions at all, that is the right observation and it is "
               "session 8's territory -- one globally stable fixed point. Say "
               "the phrase and move on.")

    # 11b THE EXACT SOLUTION --------------------------------------------------
    s = d.light()
    d.header(s, "63 – 67 min", "At the board  ·  it is linear, so solve it")
    d.title(s, "The cascade, integrated exactly")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.7, 12.5, 2.55, fill=WASH, line=TEAL,
            lw=1.5)
    for i, (line, why) in enumerate([
            ("m(t)  =  m* (1 − e^(−γₘ t))",
             "first-order linear, one variable — integrate it directly"),
            ("dp/dt + γₚ p  =  kₚ m(t)",
             "now p is forced by a known function of time"),
            ("multiply by e^(γₚ t):     d/dt [ p e^(γₚ t) ]  =  kₚ m(t) e^(γₚ t)",
             "the integrating factor — the whole trick, and it is the same trick every time"),
            ("p(t)  =  p* [ 1  −  ( γₘ e^(−γₚ t) − γₚ e^(−γₘ t) ) / (γₘ − γₚ) ]",
             "check it: zero at t = 0, and p* as t → ∞")]):
        y = 1.85 + i * 0.6
        d.text(s, line, M + 0.3, y, 11.8, 0.35, size=15, font=TEXT, bold=True,
               color=INK)
        d.text(s, why, M + 0.35, y + 0.32, 11.6, 0.28, size=11, italic=True,
               color=MUTED)
    d.text(s, "Two exponentials, not one. The protein does not simply relax at rate γₚ — it also carries the mRNA's rise, and the difference between those two facts is what session 4 is about.",
           M, 4.45, 12.5, 0.5, size=16, font=HEAD, bold=True, color=AMBER)
    for i, (k, txt) in enumerate([
            ("Why bother, when the computer will do it",
             "Because in twenty minutes we are going to approximate this, and an approximation with nothing to compare against is a hope. You cannot compute the error of a method if you do not have the answer."),
            ("And because it degenerates",
             "Put γₘ = γₚ and the expression divides by zero. The limit exists — it is p*(1 − (1 + γt)e^(−γt)) — and the fact that the algebra flinches exactly where the two timescales coincide is not a coincidence.")]):
        y = 5.08 + i * 0.72
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.6, fill=CYAN, line=None)
        d.text(s, k, M + 0.35, y, 4.0, 0.55, size=12.5, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.6, y - 0.02, 8.0, 0.65, size=11.5, color=BODY)
    d.notes(s, "Four minutes and do every line at the board. This is the only "
               "closed-form integration in the course and it is worth doing "
               "once properly, because the integrating factor is the move that "
               "reappears in session 5 for response time and in session 11 for "
               "the delayed oscillator. "
               "Sanity checks out loud, both of them: at t = 0 the bracket is "
               "(gm - gp)/(gm - gp) = 1, so p = 0. As t grows both exponentials "
               "die and p -> p*. Ten seconds each and they are the habit worth "
               "building. "
               "The degeneracy at gm = gp is worth thirty seconds. Somebody "
               "always asks. The answer is that it is a removable singularity, "
               "the limit is the (1 + gamma t) form, and physically it is the "
               "critically damped case -- the two relaxation modes have "
               "collided. If nobody asks, say it anyway; it comes back as "
               "repeated eigenvalues in session 8.")

    # 12 THE TWO TIMESCALES ---------------------------------------------------
    s = d.light()
    d.header(s, "67 – 70 min", "What the numbers look like")
    d.title(s, "Same system, two clocks")
    d.image(s, "figures/build/s03_cascade.png", M, 1.62, 12.5, 3.45)
    d.text(s, "You now have this curve exactly. So: what would you have lost by deleting the mRNA equation and writing m = α/γₘ?",
           M, 5.22, 12.5, 0.62, size=18, font=HEAD, bold=True, color=AMBER)
    d.text(s, "Guess a percentage before the next slide. Write it down — you will be able to check it.",
           M, 5.86, 12.5, 0.4, size=14, italic=True, color=MUTED)
    d.foot(s, "Two axes with different scales: the curves cross where they do because of the plot, not the biology. The 20 and the 1600 are the real comparison.", 6.35)
    d.notes(s, "Three minutes. TAKE A NUMBER FROM THE ROOM before moving on -- "
               "a prediction they have committed to is worth far more than the "
               "same figure shown cold two slides later, and this one is cheap "
               "because they only have to say a percentage. Expect guesses "
               "clustered at 1% and at 50%; the answer is 8%. "
               "Point out the twin axis explicitly -- mRNA on the left, "
               "protein on the right, and their crossing point is an artefact "
               "of the scaling. Students read crossings as meaningful. That "
               "the numbers are 20 and 1600 is itself worth a sentence: one "
               "message makes eighty proteins here, which is the "
               "amplification step and comes back in session 13 as gain. "
               "Tenfold separation is the generic bacterial case, not a choice "
               "of convenient parameters -- mRNA half-lives are minutes and "
               "proteins are removed mostly by dilution.")

    # 12b NONDIMENSIONALISE ---------------------------------------------------
    s = d.light()
    d.header(s, "70 – 74 min", "At the board  ·  four parameters become one")
    d.title(s, "Measure time in the units the system cares about")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.7, 5.9, 1.5, fill=WASH, line=TEAL,
            lw=1.5)
    d.text(s, "Scale everything by the answer:", M + 0.25, 1.8, 5.4, 0.3,
           size=12, italic=True, color=MUTED)
    d.text(s, "τ = γₚ t         μ = m / m*         π = p / p*",
           M + 0.25, 2.14, 5.4, 0.4, size=15, font=TEXT, bold=True, color=INK)
    d.text(s, "no units left anywhere — τ counts protein lifetimes",
           M + 0.25, 2.62, 5.4, 0.3, size=11, italic=True, color=MUTED)
    d.shape(s, S.ROUNDED_RECTANGLE, M + 6.35, 1.7, 6.15, 1.5, fill=CARD,
            line=AMBER, lw=1.5)
    d.text(s, "dμ/dτ  =  (1/ε)(1 − μ)", M + 6.6, 1.86, 5.6, 0.4, size=16,
           font=TEXT, bold=True, color=INK)
    d.text(s, "dπ/dτ  =  μ − π", M + 6.6, 2.30, 5.6, 0.4, size=16, font=TEXT,
           bold=True, color=INK)
    d.text(s, "ε  =  γₚ / γₘ   —   the only parameter left",
           M + 6.6, 2.76, 5.6, 0.3, size=12, bold=True, color=AMBER)
    for i, (k, txt) in enumerate([
            ("α, kₚ, γₘ, γₚ  →  ε",
             "Four numbers you would have to measure become one ratio. Every cascade with the same ε has the same shape; the other three parameters only set the axes. That is not tidying up — it is a statement about which experiments could distinguish two systems."),
            ("ε is small when the mRNA is fast",
             "Our cascade: γₚ/γₘ = 0.05/0.5 = 0.1. Bacterial mRNAs turn over in minutes and proteins are removed by dilution, so ε ≈ 0.05–0.2 is the normal situation and not a special case."),
            ("Setting ε = 0 is the approximation",
             "Put ε = 0 in the first equation and it says μ = 1 instantly — the mRNA is always at steady state. That is the quasi-steady-state approximation, and it now has a small parameter attached to it rather than a hand wave.")]):
        y = 3.42 + i * 1.05
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.9, fill=TEAL, line=None)
        d.text(s, k, M + 0.35, y, 3.5, 0.6, size=13.5, font=TEXT, bold=True,
               color=INK)
        d.text(s, txt, M + 4.1, y - 0.02, 8.5, 0.95, size=12.5, color=BODY)
    d.notes(s, "Four minutes, at the board, and derive both equations rather "
               "than displaying them -- each is two lines. "
               "dm/dt = alpha - gamma_m m, divide through by m* = "
               "alpha/gamma_m, and you get gamma_m(1 - mu). Then change the "
               "time variable to tau = gamma_p t and the chain rule puts "
               "gamma_m/gamma_p = 1/eps in front. Same for pi. "
               "THE POINT IS THE PARAMETER COUNT. Say it plainly: you started "
               "with four parameters and a two-dimensional system, and you now "
               "have one parameter. Two cascades with wildly different rate "
               "constants and the same eps produce the same curve after "
               "rescaling, which means no experiment measuring the shape alone "
               "can tell them apart. That is a real and slightly unwelcome "
               "result and the 247 students should sit with it. "
               "This is Buckingham Pi without the ceremony. If someone knows "
               "the name, say so; if not, do not introduce it.")

    # 12c THE ERROR OF THE APPROXIMATION --------------------------------------
    s = d.light()
    d.header(s, "74 – 77 min", "What Tuesday is actually about")
    d.title(s, "The approximation comes with an error bar")
    d.image(s, "figures/build/s03_qssa_error.png", M, 1.68, 12.5, 3.5)
    d.text(s, "The largest error in p/p* is ε itself. Not 'small when the separation is large' — ε, the number you already have.",
           M, 5.28, 12.5, 0.45, size=17, font=HEAD, bold=True, color=AMBER)
    d.text(s, "So for our cascade, deleting the mRNA equation costs you 8% of p* at worst, and only during the first few minutes. Whether that is acceptable is a question about what you are using the model for — which is the only kind of answer this question has.",
           M, 5.78, 12.5, 0.55, size=13, color=BODY)
    d.foot(s, "Tuesday: why it is ε and not ε², what happens near ε = 1, and the systems where this approximation quietly destroys the behaviour you cared about.", 6.5)
    d.notes(s, "Three minutes. This slide is the reason session 4 is a "
               "derivation rather than a recipe, so do not rush it. "
               "LEFT PANEL: all four parameters gone. Every cascade in the "
               "universe is one of these curves. The dashed line is the "
               "approximation and the coloured lines are the truth at three "
               "separations. "
               "RIGHT PANEL: the max error against eps, on log-log, computed "
               "rather than argued -- and it lies on the line error = eps. Ask "
               "them to read the slope. It is 1. "
               "Say what that buys: you can now decide whether to use QSSA "
               "BEFORE using it, from a number you can estimate in your head. "
               "That is the difference between a method and a habit. "
               "The one honest caveat: this is the error in the TRAJECTORY of "
               "a linear cascade. For a nonlinear system, or when the "
               "approximation is inside a feedback loop, small trajectory "
               "error does not imply small error in the behaviour -- a QSSA "
               "that is 5% wrong can move a bifurcation and delete an "
               "oscillation entirely. Session 11. Do not oversell this slide.")

    # 13 CONCEPTEST 2 ---------------------------------------------------------
    s = d.dark()
    d.header(s, "77 – 80 min", "ConcepTest  ·  vote  ·  argue  ·  vote again")
    d.title(s, "You double γₚ. What happens?")
    for i, (lab, txt) in enumerate([
            ("A", "p* halves, and it gets there twice as fast"),
            ("B", "p* halves, and the time to reach it is unchanged"),
            ("C", "p* is unchanged, and it gets there twice as fast"),
            ("D", "p* halves, and it takes twice as long")]):
        y = 2.5 + i * 0.78
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.55, 0.55, fill=CYAN, line=None)
        d.text(s, lab, M, y + 0.12, 0.55, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, txt, M + 0.85, y + 0.1, 11.6, 0.4, size=16, color=WHITE)
    d.foot(s, "You have the algebra for this. Use it rather than your intuition — and notice which one you reached for first.", 6.05)
    d.notes(s, "Four minutes. Answer A, and it is the answer that surprises "
               "people, which is why it is worth a vote rather than a "
               "sentence. "
               "p* = k_p*alpha/(gamma_m*gamma_p), so doubling gamma_p halves "
               "it. And the approach is exponential with time constant "
               "1/gamma_p, so it also halves the settling time. ONE parameter "
               "moves both. "
               "That coupling is a real design constraint and not a curiosity: "
               "in this model you cannot make a protein respond faster without "
               "also making less of it. Session 5 is where they get the two "
               "apart -- raise alpha to put the level back -- and session 7 is "
               "where negative autoregulation buys speed without paying in "
               "level, which is the actual answer and one of the nicer results "
               "in the field. "
               "C is the tempting wrong answer for anyone thinking about "
               "half-life alone.")

    # 14a THE SAME MATRIX, WITHOUT KINETICS -----------------------------------
    s = d.light()
    d.header(s, "80 – 82 min", "Consolidation  ·  1 of 2")
    d.title(s, "Two questions you can ask of S alone")
    for i, (q, when, txt, c) in enumerate([
            ("What is conserved?", "today",
             "The left null space of S. No kinetics, no parameters, no simulation — it falls out of the reaction list and nothing else.", TEAL),
            ("Which flux distributions are possible at steady state?", "session 20",
             "S v = 0, with v unknown and bounded. Throw the rate laws away entirely and it becomes a linear program. That is flux balance analysis, and it is how metabolic engineering is actually done.", CYAN)]):
        y = 2.0 + i * 2.0
        d.shape(s, S.OVAL, M, y + 0.04, 0.46, 0.46, fill=c, line=None)
        d.text(s, str(i + 1), M, y + 0.12, 0.46, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, q, M + 0.85, y - 0.02, 8.6, 0.45, size=19, font=HEAD,
               bold=True, color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, 10.4, y, 2.2, 0.36, fill=WASH,
                line=c, lw=1)
        d.text(s, when, 10.4, y + 0.07, 2.2, 0.3, size=11, bold=True, color=c,
               align="c")
        d.text(s, txt, M + 0.85, y + 0.5, 11.05, 1.2, size=14, color=BODY)
    d.foot(s, "Neither of these needs a single rate constant. That is what the separation buys you.")
    d.notes(s, "Three minutes. Row 2 lands hardest with the engineers and it "
               "is worth being concrete: the same S they built for four "
               "reactions today is what a genome-scale E. coli model has with "
               "about 2500 rows and 3000 columns -- and nobody writes those "
               "ODEs, because nobody has the rate constants. The structure is "
               "knowable when the kinetics are not, and that asymmetry is the "
               "entire reason FBA exists.")

    # 14b ...AND ONE THAT NEEDS A DERIVATIVE ----------------------------------
    s = d.light()
    d.header(s, "82 – 84 min", "Consolidation  ·  2 of 2")
    d.title(s, "And one that costs you a derivative")
    d.shape(s, S.OVAL, M, 1.94, 0.46, 0.46, fill=AMBER, line=None)
    d.text(s, "3", M, 2.02, 0.46, 0.3, size=14, bold=True, color=WHITE,
           align="c")
    d.text(s, "Is this steady state stable?", M + 0.85, 1.88, 8.6, 0.45,
           size=19, font=HEAD, bold=True, color=INK)
    d.shape(s, S.ROUNDED_RECTANGLE, 10.4, 1.9, 2.2, 0.36, fill=WASH,
            line=AMBER, lw=1)
    d.text(s, "sessions 8–9", 10.4, 1.97, 2.2, 0.3, size=11, bold=True,
           color=AMBER, align="c")
    d.text(s, "Differentiate S v(x) with respect to x. That gives you the Jacobian, and its eigenvalues decide whether a small push comes back or runs away. Today's cascade has exactly one steady state and every trajectory reaches it, which is why nothing interesting happened. Session 9's toggle has three, and two of them are the memory.",
           M + 0.85, 2.4, 11.05, 1.3, size=14, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 3.95, 12.5, 1.5, fill=WASH, line=TEAL,
            lw=1.5)
    d.text(s, "You wrote down a reaction list.",
           M + 0.35, 4.12, 11.8, 0.45, size=20, font=HEAD, bold=True,
           color=INK)
    d.text(s, "Three different fields ask three different questions of it — what is conserved, what is feasible, what is stable — and none of them need you to write another differential equation by hand for the rest of the course.",
           M + 0.35, 4.62, 11.8, 0.75, size=15, color=BODY)
    d.foot(s, "That is the whole argument for spending a session on bookkeeping.")
    d.notes(s, "Three minutes. Say 'eigenvalues' out loud now so that session "
               "8 is not the first time they hear the word in a lecture about "
               "stability -- naming a thing early costs nothing and removes "
               "most of the shock. "
               "The line about today's cascade being boring is deliberate: one "
               "globally stable fixed point is the uninteresting case, and "
               "they should leave knowing that the interesting cases exist and "
               "have a name.")

    # 15 PS1 AND FORWARD ------------------------------------------------------
    s = d.dark()
    d.header(s, "84 – 87 min", "PS1  ·  and Tuesday")
    d.title(s, "Out today, due Thursday 10 September")
    for i, (k, txt) in enumerate([
            ("Everything on PS1 was demonstrated",
             "Mass-action rate laws, building S, integrating — today. Michaelis–Menten and Hill — Tuesday, before you need them. If you find a question that was not demonstrated first, tell me: that is a defect in the course, not in you."),
            ("Start it this weekend, not Wednesday",
             "The environment problems are the slow part and they are the part I cannot fix at 11 pm. Office hours are Tuesday after class, Dwinelle 88.")]):
        y = 2.15 + i * 1.35
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 1.15, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.3, 0.75, size=16, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.0, y + 0.02, 7.4, 1.2, size=13.5, color=MINT)
    bottom = d.assignment(s, 4.95)
    d.text(s, "Tuesday:  Modeling II — quasi-steady state, and where Michaelis–Menten actually comes from.",
           M, max(bottom + 0.12, 5.3), 12.5, 0.5, size=17, font=HEAD,
           bold=True, color=CYAN)
    d.notes(s, "Four minutes. Say the 'nothing is assessed that was not "
               "demonstrated' promise out loud and mean it -- it is in the "
               "syllabus, the coverage matrix is the audit behind it, and "
               "inviting them to catch you breaking it is most of what makes "
               "it credible. "
               "If readings.yaml declares a paper for session 4, the box above "
               "renders it and you must say it out loud as well; the slide is "
               "the record, your voice is what makes anyone read it.")

    # 16 THE LAST SLIDE -------------------------------------------------------
    s = d.dark()
    d.header(s, "87 – 89 min", "Close")
    d.title(s, "Three things to take away")
    for i, t in enumerate([
            "Every deterministic model in this course is dx/dt = S v(x). Structure and kinetics separate, and that separation is worth more than the brevity.",
            "A species on both sides of a reaction has zero net stoichiometry. Translation is catalytic in the message.",
            "Find the conserved quantity and check it. It is two lines and it is the cheapest test you will ever write."]):
        y = 2.15 + i * 1.15
        d.shape(s, S.OVAL, M, y + 0.04, 0.44, 0.44, fill=CYAN, line=None)
        d.text(s, str(i + 1), M, y + 0.11, 0.44, 0.3, size=14, bold=True,
               color=INK, align="c")
        d.text(s, t, M + 0.8, y, 11.7, 1.0, size=17, color=MINT)
    d.foot(s, "Notebook, problem set and office hours are all on bCourses. The notebook is yours to keep — reopen it in November when you have forgotten what S was.", 6.4)
    d.notes(s, "Three minutes of genuine slack. If you are running early, the "
               "best use of it is E4 -- the dimer, and why the 2 appears in "
               "the conservation law but the flux uses [P] squared. If you are "
               "running late, cut this slide entirely and let them go; the "
               "three points are in the notebook's 'What to take away'.")

    return d
