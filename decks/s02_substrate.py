"""Session 2 — The cell as a physical substrate.

Eighty-nine minutes. The first working session of the course, and the first
faded worked-example set.

    0–5    retrieval: the three questions session 1 ended on
    5–8    map + goals as questions
    8–11   setting the scale: one femtolitre, and 10^30 of them
    11–15  the one number — 1 nM is 1 molecule
    15–18  ConcepTest 1 — vote, argue, revote
    18–21  what the femtolitre contains
    21–25  crowding: why the box is not a beaker
    25–28  ConcepTest 2 — vote, argue, revote
    28–32  nine orders of magnitude, on one axis
    32–35  which pairs can you treat as instantaneous?
    35–37  nothing outruns division
    37–39  the pause: two minutes, compare notes with a neighbour
    39–63  faded worked-example set                              [24 min]
    63–67  what the numbers force: because things are countable
    67–70  ...because things are slow, and the box has a size
    70–74  how to be wrong by less than ten times
    74–77  item 4: your estimate was wrong, and that is the result
    77–83  consolidation + second retrieval, in writing
    83–86  forward link
    86–89  slack

Twenty slides: 43 minutes of exposition over 13 slides, about 3.3 min/slide,
with 48% of the period given to the students. An earlier draft of this deck did
the same 43 minutes on SEVEN slides -- 6.1 min/slide -- which is not a short
lecture, it is an improvised one. `tools/build_decks.py` now measures this per
segment and flags anything past 4.5, because it is invisible in the source and
obvious in the ratio.

This is a PROCEDURE day, so per docs/lecture-design.md §2 it gets a faded
worked-example set and no launch problem: "generation for concepts, faded worked
examples for procedures." Estimating a copy number is a procedure. Inventing it
is not a productive failure, it is a wasted twenty minutes.

Coverage matrix: demonstrates T1 (molecule counts from concentration and
volume), T2 (diffusion timescale), T3 (comparing process timescales). All three
are assessed in PS1, which is out on Sept 3 — so this session is the first place
the "nothing is assessed that was not demonstrated" rule has to hold.

Every number on these slides is in figures/s02_substrate.py with its source.
The one worth knowing by heart, and the whole session in one line:

    1 nM is about 1 molecule per E. coli.
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, TEAL, GREEN, MINT, CYAN, SILVER, INK, BODY,
                         MUTED, AMBER, RED, WHITE, CARD, RULE, WASH,
                         HEAD, TEXT, W, M)

FILENAME = "PoSB_Session02_Substrate"


def build():
    d = Deck("Session 2 — The cell as a physical substrate", session=2)

    # 1 TITLE -----------------------------------------------------------------
    s = d.dark()
    d.text(s, "Session 2", M, 2.25, 8.6, 0.4, size=16, bold=True, color=CYAN)
    d.text(s, "The cell as a physical substrate", M, 2.72, 9.4, 1.3,
           size=40, font=HEAD, bold=True, color=WHITE)
    d.text(s, "One femtolitre, a fifth protein by weight, and it divides in twenty minutes",
           M, 4.15, 9.4, 0.5, size=17, italic=True, color=MINT)
    d.text(s, d.date_line, M, 6.35, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "PS0 is due today. Ask for hands: who got a plot? Anyone who "
               "did not, see them after -- do not debug in the room now, you "
               "did that on Thursday. "
               "Also: report the diagnostic. Two minutes, anonymous, shape of "
               "the distribution only. 'Half of you have solved an ODE by hand "
               "and half have run a PCR, and almost nobody has done both' is "
               "exactly the right thing for this room to hear out loud.")

    # 2 RETRIEVAL -------------------------------------------------------------
    s = d.light()
    d.header(s, "0 – 5 min", "Retrieval  ·  notes closed")
    d.title(s, "The three questions I left you with")
    for i, (src, q, c) in enumerate([
            ("From Thursday", "How many copies of your sensor protein are in one cell?", TEAL),
            ("From Thursday", "How long does one of them take to cross the cell?", TEAL),
            ("From Thursday", "Is “concentration” even the right variable at that copy number?", CYAN)]):
        y = 2.15 + i * 1.25
        d.shape(s, S.OVAL, M, y, 0.42, 0.42, fill=c, line=None)
        d.text(s, str(i + 1), M, y + 0.08, 0.42, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, src.upper(), M + 0.75, y - 0.02, 3, 0.28, size=9.5,
               bold=True, color=MUTED)
        d.text(s, q, M + 0.75, y + 0.26, W - 2 * M - 0.75, 0.6, size=17,
               color=BODY)
    d.foot(s, "Nobody can answer these yet. That is the point — write down a guess, and we will come back to it at 9:20.")
    d.notes(s, "Five minutes and it is not a quiz. These are the SAME three "
               "questions that closed session 1, deliberately: they are the "
               "prequestion and the retrieval cue at once. "
               "Take guesses out loud. Write the numbers on the board and LEAVE "
               "them there -- at minute 77 the room compares its guesses with "
               "what it now knows, and the gap is the measurement of the "
               "session. "
               "Expect wild answers on Q1, orders of magnitude apart. Do not "
               "correct anybody.")

    # 3 MAP + GOALS -----------------------------------------------------------
    s = d.light()
    d.header(s, "5 – 8 min", "Where we are  ·  what you'll be able to answer")
    d.title(s, "By 9:30 you should be able to answer")
    for i, (n, lab) in enumerate([("1", "Specification"), ("2", "The substrate"),
                                  ("3", "Modeling I"), ("4", "Modeling II"),
                                  ("5", "Expression")]):
        x, here = M + i * 2.42, n == "2"
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.95, 2.15, 0.62,
                fill=TEAL if here else WASH, line=TEAL if here else RULE, lw=1)
        d.text(s, f"{n}  {lab}", x, 2.13, 2.15, 0.3, size=12, bold=here,
               color=WHITE if here else MUTED, align="c")
    for i, g in enumerate([
            "At what concentration does a molecule stop being a concentration and start being a countable object?",
            "Which is faster in a bacterium — a protein crossing the cell, or the gene that makes it being transcribed?",
            "Why does the same circuit behave differently in a bacterium and in a human cell, before you change anything?"]):
        y = 3.25 + i * 1.0
        d.text(s, "?", M, y, 0.4, 0.5, size=26, font=HEAD, bold=True,
               color=CYAN, align="c")
        d.text(s, g, M + 0.6, y, W - 2 * M - 0.6, 0.8, size=17, color=BODY)
    d.notes(s, "Three minutes. Questions, not statements -- objectives-as-"
               "pretest beat objectives-as-declaration (Sana et al. 2020). "
               "Q3 is the one that pays off furthest away: it is why session 18 "
               "exists and why nothing from E. coli transfers for free.")

    # 4a HOW BIG IS A CELL ----------------------------------------------------
    s = d.light()
    d.header(s, "8 – 11 min", "Setting the scale")
    d.title(s, "One femtolitre")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.9, 5.9, 2.35, fill=WASH, line=TEAL, lw=2.5)
    d.text(s, "1 fL  =  10⁻¹⁵ L", M + 0.35, 2.15, 5.2, 0.6, size=28,
           font=HEAD, bold=True, color=INK)
    d.text(s, "A rod about 1 µm across and 2 µm long. If you inflated it to the size of this room, an average protein would be a grapefruit.",
           M + 0.35, 2.9, 5.2, 1.1, size=14, color=BODY)
    for i, (k, v) in enumerate([
            ("~3 × 10⁶", "protein molecules in it"),
            ("~20%", "of its wet mass is protein"),
            ("~70%", "is water — and that is the crowded case"),
            ("20–30 min", "and there are two of them")]):
        y = 4.5 + i * 0.58
        d.text(s, k, M, y, 2.0, 0.35, size=17, font=HEAD, bold=True, color=TEAL)
        d.text(s, v, M + 2.2, y + 0.04, 4.2, 0.35, size=13.5, color=BODY)
    d.text(s, "And there are a lot of them", 7.1, 1.95, 5.5, 0.4, size=17,
           font=HEAD, bold=True, color=INK)
    for i, (k, v) in enumerate([
            ("10⁶", "microorganisms per gram of soil"),
            ("10⁹", "per millilitre of rich medium"),
            ("10³⁰", "on Earth — more than stars in the observable universe"),
            ("100–200", "plasmids per cell, if you put them there")]):
        y = 2.5 + i * 0.82
        d.text(s, k, 7.1, y, 1.5, 0.4, size=19, font=HEAD, bold=True, color=CYAN)
        d.text(s, v, 8.75, y + 0.06, 3.9, 0.72, size=13, color=BODY)
    d.text(s, "So: what is the computational capacity of one of these, and how would you program it?",
           7.1, 5.95, 5.5, 0.75, size=14, bold=True, color=INK)
    d.notes(s, "Three minutes and keep it moving -- this is scale-setting, not "
               "content. The two columns do different jobs: the left says the "
               "cell is SMALL, the right says there are ASTONISHINGLY MANY. "
               "Both matter, and the second is the one students have never "
               "thought about. "
               "The question at the bottom right is from the 2025 deck and it "
               "is the right question. Do not answer it -- it is session 13, "
               "and arguably the whole course.")

    # 4b THE ONE NUMBER --------------------------------------------------------
    s = d.light()
    d.header(s, "11 – 15 min", "The one number to know by heart")
    d.title(s, "One nanomolar is one molecule")
    d.image(s, "figures/build/s02_copy_number.png", M, 1.8, 7.0, 4.1)
    d.shape(s, S.ROUNDED_RECTANGLE, 8.1, 1.9, 4.5, 1.5, fill=WASH,
            line=TEAL, lw=2.5)
    d.text(s, "1 nM  ≈  1 molecule\nper E. coli", 8.4, 2.12, 4.0, 1.1,
           size=23, font=HEAD, bold=True, color=INK, spacing=1.25)
    for i, (k, v) in enumerate([
            ("concentration", "10⁻⁹ mol / L"),
            ("× volume", "× 10⁻¹⁵ L"),
            ("× Avogadro", "× 6 × 10²³ /mol"),
            ("= a count", "≈ 0.6 molecules")]):
        y = 3.65 + i * 0.55
        d.text(s, k, 8.15, y, 2.0, 0.3, size=13, font=HEAD, bold=True,
               color=TEAL if i < 3 else INK)
        d.text(s, v, 10.35, y, 2.3, 0.3, size=13, color=BODY)
    d.text(s, "Two constants and one multiplication. Do it on the board — slowly, once — and then never look it up again.",
           8.1, 6.0, 4.5, 0.8, size=13, italic=True, color=MUTED)
    d.notes(s, "Four minutes, and do the arithmetic ON THE BOARD rather than "
               "showing it done. This is the first calculation of the course "
               "and it sets the expectation that numbers get worked, not "
               "asserted. "
               "Drill the rule of thumb: 1 nM ~ 1 molecule, 1 uM ~ 600. Ask who "
               "already knew it -- typically a couple of physicists, and saying "
               "so out loud is a cheap way to make the bimodality of the room "
               "visible and unembarrassing. "
               "The important consequence is on the LEFT of the plot, not the "
               "right: a repressor at 100 pM is not 'a low concentration', it "
               "is most cells having zero copies. That is the next slide.")

    # 5 CONCEPTEST 1 ----------------------------------------------------------
    s = d.dark()
    d.header(s, "15 – 18 min", "Vote  ·  argue with your neighbour  ·  vote again")
    d.title(s, "A transcription factor is present at 100 pM.")
    d.text(s, "You have a flask of E. coli. What is actually true of the individual cells in it?",
           M, 1.95, 11.9, 0.45, size=18, color=WHITE)
    for i, (k, opt) in enumerate([
            ("A", "Every cell has about a tenth of a molecule."),
            ("B", "Most cells have none, and a few have one."),
            ("C", "Every cell has one, they are just hard to detect."),
            ("D", "The question is malformed — concentration does not apply below 1 nM.")]):
        y = 2.9 + i * 0.8
        d.shape(s, S.OVAL, M, y, 0.46, 0.46, fill=CYAN, line=None)
        d.text(s, k, M, y + 0.08, 0.46, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.04, 11.2, 0.45, size=16, color=WHITE)
    d.foot(s, "You have everything you need. It is one line of arithmetic and one sentence of interpretation.", 6.35)
    d.notes(s, "ANSWER: B. 100 pM in 1 fL is 0.06 molecules -- which cannot be "
               "what any single cell contains, because molecules are integers. "
               "What it means is that roughly one cell in seventeen has one "
               "copy and the rest have none. "
               "A is the trap and most rooms pick it: it treats a population "
               "average as a property of an individual, which is the single "
               "most common modelling error in this field. "
               "D is defensible and worth taking seriously out loud -- "
               "concentration is still a perfectly good variable, it has just "
               "stopped being a description of any particular cell. Give credit "
               "for that argument, then land on B. "
               "This is the seed of session 12 (noise) and of every "
               "single-cell measurement in the course.")

    # 6a CROWDING --------------------------------------------------------------
    s = d.light()
    d.header(s, "18 – 22 min", "Why the box is not a beaker")
    d.title(s, "There is almost no water in the way you are picturing")
    d.paper_figure(s, "l02_2025_crowding", M, 1.8, 6.2, 3.0,
                   "2025 deck, p. 11 — panel source needs resolving",
                   "1 fL, and a 100 nm box inside it")
    d.paper_movie(s, "valverde2025_s4", 7.2, 1.8, 5.4, 3.0,
                  "Valverde-Mendez et al., PNAS 122(4) 2025 — Movie S4",
                  "the same packing, simulated and moving")
    for i, (k, txt, c) in enumerate([
            ("70% water, 20% protein", "By wet mass — and the second number is your competition. Every ribosome your circuit uses is one the host was already using.", TEAL),
            ("GFP diffuses 11× slower", "7.7 µm²/s in the cytoplasm against ~87 in water. The factor of eleven IS the crowding, and it was measured, not assumed.", AMBER)]):
        x = M + i * 6.2
        d.text(s, k, x, 5.35, 5.7, 0.4, size=15, font=HEAD, bold=True, color=c)
        d.text(s, txt, x, 5.75, 5.7, 0.9, size=12.5, color=BODY)
    d.sources(s, [
        ("the number, D = 7.7 µm²/s",
         "Elowitz, Surette, Wolf, Stock & Leibler, J. Bacteriol. 181:197–203 (1999)"),
        ("the movie",
         "Valverde-Mendez et al., PNAS 122(4) e2406340121 (2025), Movie S4 · CC BY-NC-ND")],
        y=6.72)
    d.notes(s, "Four minutes. Left picture, then PLAY THE MOVIE -- thirty "
               "seconds is enough. The still says the cytoplasm is packed; the "
               "movie is the same packing MOVING, which is the difference "
               "between crowded as an adjective and crowded as a mechanism. "
               "Magenta is the nucleoid, grey and white are charged crowders, "
               "yellow are ribosomes and polysomes, the single green one is the "
               "tracked particle -- all at physiological density. "
               "It is a simulation, and say so: it is the model that produces "
               "the result two slides from now, which is why showing it here "
               "pays for itself. "
               "IF THE ROOM ASKS how any of this is measured, Movie S2 in "
               "private/paper-movies is the clean one -- a segmented cell with "
               "a star tracking the particle. Movie S3 is the 3D "
               "reconstruction and makes a lovely separate point about "
               "projections throwing information away. Neither is on a slide "
               "because neither is what this slide claims. "
               "Do not over-teach crowding theory. The operational point is "
               "that D is measured and it is ~11x lower than the beaker value. "
               "Tie it back to Thursday: this is the burrito, quantified. "
               "The composition table is private/paper-figures/"
               "l02_2025_composition.png if the room wants the breakdown -- "
               "deliberately not on a slide, because two numbers carry it. "
               "PROVENANCE: the 100 nm box is a Goodsell-tradition rendering, "
               "uncredited on the 2025 slide. The movie is CC BY-NC-ND -- fine "
               "to project unmodified, not to redistribute.")

    # 6b THE 2025 MEASUREMENT --------------------------------------------------
    s = d.light()
    d.header(s, "22 – 25 min", "What one diffusion coefficient hides")
    d.title(s, "Two things that number will not tell you")
    d.image(s, "figures/build/s02_size_dependence.png", M, 1.72, 6.4, 2.4)
    d.movie(s, "figures/build/s02_confinement.mp4", M, 4.18, 6.4, 2.35,
            caption="ours — a random walk and a wall, nothing else")
    for i, (k, txt, c) in enumerate([
            ("There is no single viscosity",
             "A ribosome-sized particle sees ~100 cP where GFP sees ~12. Four times bigger, but thirty-five times slower to cross the cell. The medium depends on the probe.", AMBER),
            ("And it looks anomalous when it is not",
             "Tracked motion gives sub-diffusive exponents, α ≈ 0.75. A plain random walk in a box gives the same 0.75 — with ordinary diffusion at every step. The apparent anomaly is the nucleoid and the cell wall.", CYAN),
            ("So use L²/2D, and say so",
             "It is the right first estimate and we will use it all term. Just know which direction it is wrong in: for anything large, optimistic by more than an order of magnitude.", TEAL)]):
        y = 1.9 + i * 1.6
        d.shape(s, S.ROUNDED_RECTANGLE, 7.4, y, 0.12, 1.25, fill=c, line=None)
        d.text(s, k, 7.75, y, 4.85, 0.62, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, 7.75, y + 0.6, 4.85, 1.05, size=12.5, color=BODY)
    d.sources(s, [
        ("~100 cP for a ribosome-sized probe, and α ≈ 0.75",
         "Valverde-Mendez et al., PNAS 122(4) e2406340121 (2025)"),
        ("the confined walk, and both panels reproduced",
         "ours — demos/d02-crowding and figures/s02_movie.py")],
        y=6.78)
    d.notes(s, "Three minutes, and RUN DEMO 2 here rather than talking over "
               "these plots -- demos/d02-crowding. Take a prediction before "
               "each cell: 'a ribosome is four times bigger, so how much "
               "slower?' The room says four. It is thirty-five. "
               "Then the second half: 'this is a plain random walk, ordinary "
               "diffusion at every step -- what exponent will it show once I "
               "put a wall on it?' The room says one. It is 0.75, which is what "
               "the paper measures. "
               "The methodological point is deliberately NOT laboured here -- "
               "item 4 of the faded set carries that, and saying it twice in "
               "eighty-nine minutes makes it a slogan. Here the paper's job is "
               "to make the crowding claim visual and quantitative. "
               "One sentence worth saying: nobody needed anomalous-diffusion "
               "theory to explain an anomalous-looking exponent. When a "
               "measurement looks exotic, check whether something boring and "
               "geometric produces the same signature first.")

    # 7 CONCEPTEST 2 ----------------------------------------------------------
    s = d.dark()
    d.header(s, "25 – 28 min", "Vote  ·  argue  ·  vote again")
    d.title(s, "The same protein, in a human cell instead.")
    d.text(s, "A HeLa cell is about 20 µm across; E. coli is about 1 µm. Roughly how much longer does the protein take to cross it?",
           M, 1.95, 11.9, 0.75, size=18, color=WHITE)
    for i, (k, opt) in enumerate([
            ("A", "About 20 times longer."),
            ("B", "About 400 times longer."),
            ("C", "About the same — diffusion is fast either way."),
            ("D", "It never gets across; it would be degraded first.")]):
        y = 2.95 + i * 0.78
        d.shape(s, S.OVAL, M, y, 0.46, 0.46, fill=CYAN, line=None)
        d.text(s, k, M, y + 0.08, 0.46, 0.3, size=15, bold=True, color=INK,
               align="c")
        d.text(s, opt, M + 0.85, y + 0.04, 11.2, 0.45, size=16, color=WHITE)
    d.foot(s, "The exponent is the whole answer. Everything else on this slide is a distractor.", 6.35)
    d.notes(s, "ANSWER: B. Diffusion time goes as L SQUARED, so 20x the "
               "distance is 400x the time: ~65 ms across E. coli becomes ~26 s "
               "across a HeLa cell -- and that is an underestimate, because a "
               "eukaryotic cytoplasm is more crowded and compartmentalised. "
               "A is the majority answer on the first vote and it is the whole "
               "reason this question exists. Linear intuition about diffusion "
               "is wrong and it is wrong in the direction that matters. "
               "The design consequence, which is worth stating explicitly: a "
               "circuit that relies on something diffusing across the cell "
               "faster than it decays works in a bacterium and may simply not "
               "work in a mammalian cell. Nothing about the DNA changed. That "
               "is session 18. "
               "D is a real effect and worth a sentence -- for some proteins it "
               "IS true, which is why localisation exists.")

    # 8a NINE ORDERS ----------------------------------------------------------
    s = d.light()
    d.header(s, "28 – 32 min", "Everything, on one axis")
    d.title(s, "Nine orders of magnitude")
    d.image(s, "figures/build/s02_timescales.png", M, 1.7, 11.9, 4.5)
    d.text(s, "Print this. It is the only slide in the course you will want on the wall — every model you write for the next fourteen weeks is a claim about where two of these sit relative to each other.",
           M, 6.3, W - 2 * M, 0.6, size=14, color=INK)
    d.notes(s, "Four minutes. Walk it left to right ONCE, naming each point, "
               "and resist commentary -- the next slide is the commentary. "
               "The red point on the right is session 9's toggle failure. Note "
               "out loud that it is five orders of magnitude slower than "
               "anything the circuit itself does, which is exactly why it was "
               "invisible to the people who built the circuit.")

    # 8b WHICH PAIRS ----------------------------------------------------------
    s = d.light()
    d.header(s, "32 – 35 min", "The only question this axis is for")
    d.title(s, "Which of these can you treat as instantaneous?")
    for i, (fast, slow, ratio, verdict, c) in enumerate([
            ("a protein crossing the cell", "the gene being transcribed", "~300×",
             "Yes. Position inside the cell is not a variable in this course, and this is why.", TEAL),
            ("mRNA appearing and decaying", "protein accumulating", "~10×",
             "Usually. This is the approximation that turns a four-variable model into a two-variable one — session 4 does it properly.", TEAL),
            ("a protein being made", "the cell dividing", "~100×",
             "Yes, and it is why a steady state exists at all within one generation.", TEAL),
            ("everything above", "the circuit being lost to mutation", "~10⁴×",
             "Yes — and that is precisely why nobody notices until 40 hours in.", AMBER)]):
        y = 1.9 + i * 1.2
        d.text(s, fast, M, y, 3.6, 0.4, size=13.5, font=HEAD, bold=True,
               color=INK)
        d.text(s, "vs", M + 3.7, y + 0.03, 0.5, 0.3, size=11, italic=True,
               color=MUTED)
        d.text(s, slow, M + 4.3, y, 3.4, 0.4, size=13.5, font=HEAD, bold=True,
               color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, M + 7.9, y - 0.02, 0.95, 0.36,
                fill=c, line=None)
        d.text(s, ratio, M + 7.9, y + 0.04, 0.95, 0.3, size=11.5, bold=True,
               color=WHITE, align="c")
        d.text(s, verdict, M, y + 0.42, 11.9, 0.7, size=12.5, color=BODY)
    d.foot(s, "Separated timescales are a gift. They are the reason a four-variable model of a real cell is defensible rather than a fantasy.")
    d.notes(s, "Three minutes. THIS is the slide that does the work -- the "
               "previous one is just the data. "
               "Ask the room for each pair before you reveal the verdict; they "
               "can read the ratio off the axis. What they are doing is the "
               "quasi-steady-state approximation, informally, two sessions "
               "before they meet it as algebra. Meeting it here as an "
               "observation about a picture is worth more than meeting it as a "
               "manoeuvre. "
               "Row 2 is the one with a real caveat: the 10x separation is "
               "marginal, and session 4 shows exactly when it breaks. Flag it "
               "as the interesting case.")

    # 8c NOTHING OUTRUNS DIVISION ---------------------------------------------
    #
    # This was three bullets on a dark slide and no picture, which is a bad
    # trade for the most useful consequence in the session. The claim is
    # quantitative -- there is a ceiling, and the ceiling moves with the medium
    # -- so it wants an axis, not an adjective. It does NOT want a live demo:
    # nothing here is emergent, both curves are single exponentials, and the
    # session already spends a demo on crowding at minute 22.
    s = d.light()
    d.header(s, "35 – 37 min", "The clock you cannot switch off")
    d.title(s, "Nothing outruns division")
    d.text(s, "Switch the promoter off and a perfectly stable protein still disappears — because the cell keeps making more cells to divide it between.",
           M, 1.72, 11.9, 0.45, size=16, color=BODY)
    d.image(s, "figures/build/s02_dilution.png", M, 2.25, 11.9, 3.55)
    # Removal rates add. Written this way it is the parallel-resistor formula,
    # which is the form students will recognise and the form session 5 uses.
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.92, 11.9, 0.62, fill=WASH, line=TEAL,
            lw=1)
    # No underscores in the equation: PowerPoint renders "T_d" as literally
    # T-underscore-d, which reads as a typo on a slide about being exact.
    d.text(s, "µ + γ  is the removal rate. With doubling time  T  and the half-life  τ  you engineer:   "
              "you get   Tτ / (T + τ)  ≤  T.   Half-lives combine like resistors in parallel, and  T  is the one you cannot remove.",
           M + 0.2, 6.03, 11.5, 0.45, size=13.5, color=INK)
    d.foot(s, "Session 9's toggle takes hours to switch. That is not a detail about the toggle — it is this constraint, in a circuit.", 6.68)
    d.notes(s, "Two minutes, and it is now a picture rather than three claims. "
               "LEFT PANEL: point at the teal curve. Nothing degrades it. It "
               "halves in one doubling time anyway. Say the correction out "
               "loud, because the sloppy version of this sentence is wrong: it "
               "is the CONCENTRATION that halves, and only once synthesis has "
               "stopped. The number of molecules in a given cell does not fall "
               "-- they get shared out. "
               "RIGHT PANEL: this is the one to spend the time on. The x axis "
               "is a design knob -- how hard you tag the protein -- and the y "
               "axis is what you actually get. Every curve saturates. The "
               "ceiling is the doubling time, and it MOVES WITH THE MEDIUM, so "
               "the slowest dynamics your circuit can express is set by what "
               "you feed the cells and not by anything you designed. "
               "Do not assert a single ssrA number: reported tag half-lives "
               "scatter from a few minutes to an hour depending on tag, "
               "protease load and medium (Andersen et al. 1998 get ~40 min for "
               "LVA and LAA, but after a shift to minimal medium, which is not "
               "a clean degradation rate). The shaded band is honest; a point "
               "estimate would not be. "
               "Comes back in session 5 as gamma + mu, in session 9 as the "
               "switching time, in session 19 as the reason burden matters.")

    # 9 THE PAUSE -------------------------------------------------------------
    s = d.dark()
    d.header(s, "37 – 39 min", "Two minutes  ·  I will not say anything")
    d.title(s, "Compare notes with the person next to you")
    d.text(s, "Fill in each other's gaps. Find one thing you wrote down differently.",
           M, 2.4, 11.9, 0.5, size=22, font=HEAD, color=MINT)
    d.text(s, "This is not a break. It is the only two minutes in the session where you find out what you missed while you were writing.",
           M, 3.3, 11.9, 0.7, size=17, color=WHITE)
    d.text(s, "Then: handouts.", M, 4.6, 11.9, 0.5, size=20, font=HEAD,
           bold=True, color=CYAN)
    d.foot(s, "The pause procedure — two minutes, three times a lecture — is one of the cheapest interventions with real evidence behind it. [B]", 6.4)
    d.notes(s, "SAY NOTHING FOR TWO MINUTES. That is harder than it sounds and "
               "it is the whole intervention; if you talk over it, it does not "
               "work. Stand at the back so the room stops looking at you. "
               "Hand the faded sets out during the pause so no time is lost.")

    # 10 FADED SET ------------------------------------------------------------
    s = d.light()
    d.header(s, "39 – 63 min", "Worked set  ·  handout  ·  start where you like")
    d.title(s, "Four estimates, with less of my working each time")
    for i, (n, k, txt, c) in enumerate([
            ("1", "Fully worked", "Copy number of a repressor at 10 nM. Every step written out, each one labelled with what it accomplishes.", TEAL),
            ("2", "Last step removed", "How long a protein takes to cross E. coli. The setup is given; you finish it.", TEAL),
            ("3", "Last two removed", "The same protein in a HeLa cell, and the ratio. You are given the convention and nothing else.", CYAN),
            ("4", "Bare problem", "A repressor has to find one operator site in 4.6 Mb of genome. Estimate the search time and compare it to the cell cycle.", AMBER)]):
        y = 1.9 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.5, 0.9, fill=c, line=None)
        d.text(s, n, M, y + 0.26, 0.5, 0.35, size=17, bold=True, color=WHITE,
               align="c")
        d.text(s, k, M + 0.8, y, 3.2, 0.4, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.2, y + 0.02, 7.7, 0.9, size=13, color=BODY)
    d.text(s, "Start wherever the scaffolding stops helping you. Nobody needs to announce where that is.",
           M, 6.5, W - 2 * M, 0.4, size=16, bold=True, color=INK)
    d.notes(s, "Twenty-four minutes. CIRCULATE. Do NOT work item 1 at the "
               "board -- that removes the fading and collapses the whole set "
               "into a single demonstration, which is precisely the "
               "intervention this replaces. "
               "The handout carries subgoal labels ('convert to a count', "
               "'state the convention') and a self-explanation prompt at each "
               "transition. Both have independent evidence; neither works if "
               "the students skip the writing, so say once that the prompts are "
               "the point. "
               "Item 4 is genuinely hard and is meant to be. If nobody gets it, "
               "that is fine -- it is the setup for the last twenty minutes, "
               "and the answer (~minutes, by 1-D sliding along the DNA rather "
               "than 3-D search) is one of the loveliest results in molecular "
               "biophysics. Do not give it away before 63 minutes.")

    # 11a WHAT IT FORCES — COUNTING -------------------------------------------
    s = d.light()
    d.header(s, "63 – 67 min", "What the numbers force on you  ·  1 of 2")
    d.title(s, "Because things are countable")
    for i, (k, txt, fwd) in enumerate([
            ("Low copy number means noise, unavoidably",
             "A regulator present at a few copies per cell has fractional fluctuations of order one. Not bad engineering — counting statistics. No amount of care removes it, and a design that needs it removed is not a design.",
             "session 12"),
            ("A population average is not a cell",
             "Half your intuitions about concentration were built on beakers containing 10²⁰ molecules. In a cell with six, the average describes nobody. Every single-cell measurement in this course exists because of that gap.",
             "sessions 12, 13")]):
        y = 1.85 + i * 1.9
        d.shape(s, S.OVAL, M, y + 0.06, 0.46, 0.46, fill=TEAL, line=None)
        d.text(s, str(i + 1), M, y + 0.14, 0.46, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, k, M + 0.85, y, 9.3, 0.45, size=19, font=HEAD, bold=True,
               color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, 10.4, y + 0.02, 2.2, 0.36,
                fill=WASH, line=TEAL, lw=1)
        d.text(s, fwd, 10.4, y + 0.09, 2.2, 0.3, size=11, bold=True,
               color=TEAL, align="c")
        d.text(s, txt, M + 0.85, y + 0.5, 11.05, 1.25, size=14, color=BODY)
    # Forty seconds, one exponent, and it buys the forward links to 12 and 25.
    # It is here rather than on its own slide because the arithmetic is the
    # same arithmetic as item 1 -- counting -- and a separate slide would imply
    # a separate mechanism.
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.5, 12.5, 0.95, fill=WASH,
            line=AMBER, lw=1)
    d.text(s, "And division does the same arithmetic.", M + 0.2, 5.58, 3.5,
           0.3, size=13.5, font=HEAD, bold=True, color=AMBER)
    d.text(s, "A plasmid at 5 copies splits binomially: P(one daughter gets none) = 2·(½)⁵ ≈ 6%. "
              "Not asymmetry — counting again, and why low-copy plasmids carry partition systems.   → sessions 12, 25",
           M + 0.2, 5.9, 12.1, 0.5, size=13, color=BODY)
    d.notes(s, "Four minutes, two items and a coda; say the forward references "
               "out loud -- students who can see where a fact gets used "
               "remember it. "
               "Item 2 is the deeper one and worth the extra minute: the "
               "beaker intuition is not merely imprecise here, it is about a "
               "different object. "
               "THE CODA IS FORTY SECONDS. Ask for the exponent before you show "
               "it; five copies, fair coin, they can do it. Then be precise "
               "about the word: this is RANDOM partitioning, which is "
               "symmetric in expectation and noisy at low copy number. It is "
               "not asymmetric division -- systematically biased inheritance, "
               "like damaged-protein aggregates going to the old pole -- which "
               "is a different mechanism and is not in this course. Conflating "
               "them teaches a wrong cause for a right observation. "
               "Session 25 does the full binomial calculation for a genome; "
               "this is the one-line version that makes them want it.")

    # 11b WHAT IT FORCES — GEOMETRY AND GROWTH ---------------------------------
    s = d.light()
    d.header(s, "67 – 70 min", "What the numbers force on you  ·  2 of 2")
    d.title(s, "Because things are slow, and the box has a size")
    for i, (k, txt, fwd) in enumerate([
            ("Growth is a rate you cannot switch off",
             "Dilution sets the floor on every protein's lifetime. Design a circuit slower than division and the cell erases it while you watch.",
             "sessions 5, 19"),
            ("Geometry changes the answer, not just the number",
             "Twenty times bigger is four hundred times slower. A design that works in a bacterium can fail in a mammalian cell with no change to the DNA at all.",
             "session 18")]):
        y = 2.0 + i * 2.0
        d.shape(s, S.OVAL, M, y + 0.06, 0.46, 0.46, fill=AMBER, line=None)
        d.text(s, str(i + 3), M, y + 0.14, 0.46, 0.3, size=14, bold=True,
               color=WHITE, align="c")
        d.text(s, k, M + 0.85, y, 9.3, 0.45, size=19, font=HEAD, bold=True,
               color=INK)
        d.shape(s, S.ROUNDED_RECTANGLE, 10.4, y + 0.02, 2.2, 0.36,
                fill=WASH, line=AMBER, lw=1)
        d.text(s, fwd, 10.4, y + 0.09, 2.2, 0.3, size=11, bold=True,
               color=AMBER, align="c")
        d.text(s, txt, M + 0.85, y + 0.5, 11.05, 1.3, size=14, color=BODY)
    d.text(s, "Four design consequences. Three numbers and a square.",
           M, 6.15, W - 2 * M, 0.45, size=17, bold=True, color=INK)
    d.notes(s, "Three minutes. Item 4 is the one that surprises people who "
               "have only worked in bacteria, and it is the whole reason "
               "session 18 exists as a separate session rather than an aside. "
               "Land the closing line and pause on it -- it is the argument of "
               "the session.")

    # 12a THE HABIT ------------------------------------------------------------
    s = d.dark()
    d.header(s, "70 – 74 min", "The habit this course wants")
    d.title(s, "How to be wrong by less than ten times")
    for i, (k, txt) in enumerate([
            ("State the convention before the number", "L²/2D or L²/6D? Say which. A factor of three is nothing; an unstated convention is an argument you cannot settle afterwards."),
            ("One significant figure, and no more", "Writing 64.9 ms implies you know something you do not. 'Tens of milliseconds' says exactly what you know."),
            ("Ask what would make it wrong by 10×", "Not 'is this right'. An estimate you cannot break is an estimate you have not understood."),
            ("Predict before you compute", "Every worked example in this course asks for the expected answer first. A simulation you cannot check independently is not evidence of anything.")]):
        y = 1.95 + i * 1.15
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.12, 0.9, fill=CYAN, line=None)
        d.text(s, k, M + 0.4, y, 4.6, 0.42, size=15.5, font=HEAD, bold=True,
               color=WHITE)
        d.text(s, txt, M + 5.3, y + 0.02, 6.6, 0.9, size=13, color=MINT)
    d.foot(s, "Item 4 is the one I will hold you to all term. It is also the one that catches your own errors before I do.", 6.6)
    d.notes(s, "Four minutes, and this is the transferable part of the "
               "session. Most of these students will never again compute a "
               "diffusion time; all of them will need to judge whether a number "
               "someone hands them is plausible.")

    # 12b THE SEARCH-TIME ANSWER -----------------------------------------------
    s = d.light()
    d.header(s, "74 – 77 min", "Item 4  ·  your estimate was wrong")
    d.title(s, "And being wrong is the result")
    for i, (k, txt, c) in enumerate([
            ("What you estimated", "A repressor bouncing around 1 fL of cytoplasm until it happens to hit one 20-base-pair target in 4.6 million. Diffusion-limited, three-dimensional, and slow — of order an hour.", MUTED),
            ("What is measured", "Association in minutes. Fast enough that a cell can respond to a change in its environment within a fraction of a generation, which it manifestly does.", TEAL),
            ("So the model is wrong, not the arithmetic", "The protein does not only search in three dimensions. It binds DNA non-specifically and slides along it, converting a hopeless 3-D search into a series of short 1-D ones.", CYAN)]):
        y = 1.95 + i * 1.32
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.14, 1.05, fill=c, line=None)
        d.text(s, k, M + 0.4, y, 3.7, 0.42, size=15, font=HEAD, bold=True,
               color=INK)
        d.text(s, txt, M + 4.4, y + 0.02, 7.5, 1.05, size=13, color=BODY)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 6.0, W - 2 * M, 0.85, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "An estimate that disagrees with a measurement is not a failure. It is the most reliable way anyone has ever found a mechanism they were not looking for.",
           M + 0.3, 6.2, 11.5, 0.6, size=15, bold=True, color=INK)
    d.notes(s, "Three minutes, and this is the note to end the teaching on. "
               "Do NOT derive facilitated diffusion -- Berg and von Hippel, "
               "1981, and it is a beautiful piece of work that belongs in a "
               "different course. The point here is entirely methodological: "
               "the estimate was off by a factor of tens, that discrepancy was "
               "not noise, and chasing it produced a mechanism. "
               "If a group got close to this during the faded set, name them. "
               "It is the best thing anyone can have done today.")

    # 13 CONSOLIDATION --------------------------------------------------------
    s = d.light()
    d.header(s, "77 – 83 min", "Notes closed  ·  in writing")
    d.title(s, "The three questions again — now answer them")
    for i, (q, hint) in enumerate([
            ("How many copies of your sensor protein are in one cell?",
             "at 10 nM, in 1 fL"),
            ("How long does one of them take to cross the cell?",
             "state your convention"),
            ("Is “concentration” the right variable at that copy number?",
             "one sentence, and say when it stops being right")]):
        y = 2.05 + i * 1.15
        d.shape(s, S.OVAL, M, y + 0.02, 0.42, 0.42, fill=TEAL, line=None)
        d.text(s, str(i + 1), M, y + 0.09, 0.42, 0.3, size=13, bold=True,
               color=WHITE, align="c")
        d.text(s, q, M + 0.78, y, 11.3, 0.45, size=17, color=BODY)
        d.text(s, hint, M + 0.78, y + 0.45, 11.3, 0.3, size=12, italic=True,
               color=MUTED)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.6, W - 2 * M, 1.0, fill=WASH,
            line=TEAL, lw=1.5)
    d.text(s, "Now look at the board.", M + 0.3, 5.78, 5.0, 0.32, size=14,
           font=HEAD, bold=True, color=INK)
    d.text(s, "Those are the guesses this room made ninety minutes ago. How far off were you, and in which direction?",
           M + 0.3, 6.1, 11.5, 0.4, size=13.5, color=BODY)
    d.notes(s, "Six minutes: three writing, three comparing. Notes CLOSED for "
               "the writing -- this is the second retrieval and it is where the "
               "session actually gets consolidated. "
               "Then reveal the opening guesses still on the board. The gap "
               "between the 8:05 guess and the 9:20 answer is the most "
               "persuasive thing that happens today, and it costs nothing "
               "because you already wrote them down. "
               "Most rooms are two to three orders of magnitude high on Q1. "
               "Say so cheerfully; being wrong by 1000x at 8am and right by "
               "9:20 is the format working.")

    # 14 FORWARD LINK ---------------------------------------------------------
    s = d.dark()
    d.header(s, "83 – 86 min", "Next")
    d.title(s, "You can count the molecules. Now make them react.")
    d.text(s, "Thursday: Modeling I — mass action and the stoichiometric matrix.",
           M, 2.15, 11.9, 0.45, size=23, font=HEAD, bold=True, color=MINT)
    d.text(s, "Today you established that a cell contains a countable number of things, moving on timescales you can compare. Thursday those things start reacting, and one equation covers every network in this course:",
           M, 2.85, 11.9, 1.0, size=16, color=WHITE, spacing=1.35)
    d.text(s, "dx/dt  =  S · v(x)", M, 4.0, 6.0, 0.7, size=32, font=HEAD,
           bold=True, color=CYAN)
    d.text(s, "We will solve the same three-reaction network three ways — by hand, as a matrix, and with the package — and assert that all three agree to 10⁻⁹. If they do not, you will find out why before you trust any of it.",
           M, 4.85, 11.9, 0.9, size=15, color=SILVER)
    bottom = d.assignment(s, y=5.9)
    d.text(s, "Bring a laptop. PS1 goes out Thursday and it starts here.",
           M, 6.0, 11.9, 0.35, size=15, bold=True, color=SILVER)
    d.notes(s, "Three minutes. Session 3 is the Python onboarding as well as "
               "the modelling session, so the laptop line is not optional. "
               "PS1 assesses T1, T2 and T3 -- everything from today -- plus "
               "session 3 and 4 material. Today is the first test of the "
               "'nothing assessed that was not demonstrated' rule, and it "
               "passes: the faded set IS the PS1 technique.")

    return d
