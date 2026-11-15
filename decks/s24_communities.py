"""Session 24 — The wire is now outside the cell.

Tuesday 17 November 2026. Part II, ninth session. Balagaddé et al., Mol Syst
Biol 4:187 (2008) and Basu et al., Nature 434:1130-1134 (2005) were both
assigned at the close of session 23, under the two-required override Adam
approved.

WHAT THIS SESSION IS. For twenty-three sessions every connection in a circuit
has been a molecule inside one cell, and its transit time was never a design
parameter. The moment the signal leaves, the connection acquires

    A LENGTH SCALE AND A DELAY,

and both belong to the medium rather than to the plasmid. Sessions 19 to 23
were a ladder of contexts that break a circuit, ending in selection, which
cannot be rejected. This session inverts the ladder: the population stops
being what breaks your circuit and becomes what you build with.

FOUR MODELS, FOUR PROVENANCES, AND A SLIDE MUST NEVER RUN THEM TOGETHER.

  * t ~ L^2/2D_A -- session 2's convention, stated before any number, with
    Karig's two ESTIMATED effective cell-to-cell coefficients.
  * ell_A = sqrt(D_A/gamma_A) -- DERIVED on a five-step surface (stop 2,
    "the length scale, derived"): steady state, trial exponential, the
    substitution that forces ell, and the units check. It was asserted as a
    formula until 14 November, which is what deck-bar rule 18 was written
    about; this note said so and was left stale after the fix. What this
    folder still cannot do is source a VALUE for Basu's system, and that is
    T66's lesson. No slide prints 0.32 mm or 0.71 mm: the first is computed from Basu's xi and
    inherits xi's defect, the second combines Karig's 3OC12HSL with Basu's
    gamma_A, a different signal in a different lawn.
  * Basu's printed equations (1)-(4) in the liquid-phase limit the paper
    itself defines, on their printed BD2/BD1/BD3 sets. Nothing fitted.
  * BioModels BIOMD0000000296, curated from Balagaddé 2008 -- NOT "the
    paper's", which prints no equations at all, and NOT "ours", which the
    three-digit agreement with their own Fig. 3C refutes. What IS ours is the
    STRUCTURE the room writes down from Box 1A.

TECHNIQUES CARRIED, all four of them (docs/coverage-matrix.md):
  T64 sender/receiver model construction   -- PS9 and the FINAL
  T65 band-detect analysis                 -- PS9, autograded
  T66 diffusion length scale in a community-- PS9, autograded
  T76 decide whether to split a pathway    -- home GUIDE and the final, HAND

THE FIVE THINGS A LATER PASS MUST NOT UNDO.
 1. 83 um^2/s is an ESTIMATE, an EFFECTIVE CELL-TO-CELL coefficient, and the
    WRONG MOLECULE for Basu's geometry. All three qualifications stay.
 2. Same topology, different consequence. Session 10's pulse came from a slow
    arm; Basu's band comes from two repression coefficients far apart. The
    wiring transfers and the mechanism does not.
 3. High-detect sets the UPPER edge and low-detect the LOWER one, which is
    what the names suggest. The surprise is that a high-detect strain alone
    is an INVERTER.
 4. The hundredfold diffusion ratio is Karig's own NON-STOCHASTIC SIMULATION
    of their own scheme. It is not a classical Turing requirement and there
    is no universal ratio.
 5. Tamsir's wires are 3OC12-HSL and C4-HSL -- Karig's pair, not Basu's
    3OC6HSL. This deck never says "the same AHL" about them.

NO ABSOLUTE AHL POSITION FROM BASU FIG. 2 APPEARS ANYWHERE. Both its panels
have no major ticks to key a digitizer on, and panel d's 10^1 label sits
about 0.16 of a decade off its own even spacing (NUMBERS.md 23.1). Every
number on these slides comes from the printed parameters through
posb.communities, which tests/test_communities.py pins two-sided.

Numbers: sessions/s24-communities/NUMBERS.md, every one tagged with its kind.
Design: sessions/s24-communities/DESIGN.md.

Build:  python tools/build_decks.py s24_communities
"""
from pptx.enum.shapes import MSO_SHAPE as S

from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, BODY, RED, GREEN, WASH, HEAD)

FIG = "figures/build/"
FILENAME = "s24-communities"

# ---------------------------------------------------------------------------
# EVERY NUMBER THIS DECK PRINTS, WITH ITS NUMBERS.md SECTION AND ITS KIND.
# Written out here rather than left in the call sites because the bar's
# section F is a front-to-back check and a reader has to be able to audit the
# arithmetic without opening five files. Each was re-run against
# posb.communities on 8 November before it went on a slide.
#
# sec 19.1  KARIG D: 3OC12HSL 83 um^2/s, C4HSL 1810 um^2/s. modelED from
#           MEASURED -- their word is "estimated", by fitting a fluorescence
#           wave profile. EFFECTIVE CELL-TO-CELL, through a lawn. Measured
#           ratio 21.6 +/- 10; Wilke-Chang predicts about 1.5 in free
#           solution, so most of the ratio is the cells.
# sec 19.2  the ~100 ratio: Karig's NON-STOCHASTIC SIMULATION of their own
#           scheme. modelED and system-specific.
# sec 19.3  half-activations 0.003 uM (3OC12HSL) and 3 uM (C4HSL), MEASURED,
#           each to its OWN cognate signal -- and SI sec 4 measures 3OC12HSL
#           competitively binding RhlR, so the gap buys no orthogonality.
# sec 13.1  BASU_XI = 0.001 mm^2/min, PRINTED, and NOT a diffusion
#           coefficient: eq. (5) is a bare discrete Laplacian so xi is
#           D_A/dx^2 with dx never stated.
# sec 13.3  xi against Basu's own geometry: 10 mm takes 833 h, 7 mm 408 h,
#           6 mm 300 h, against a 36 h experiment. COMPUTED, re-run here.
# sec 7.2   printed BD2 set: beta_L = 0.8 uM, beta_C = 0.008 uM, ratio 100.
# sec 7.3   BD1 is BD2 with rho_R x10; BD3 halves alpha_G, alpha_L2, [LuxR].
#           Liquid-phase simulations omit eq. (5) -- the paper's own limit.
# COMPUTED from those printed parameters by posb.communities, pinned by
#           tests/test_communities.py:
#             BD2 peak 3.973 nM, edges 2.61 and 6.93 nM, 2.65x apart
#             BD1 peak 1.256 nM (exactly sqrt(10) below BD2)
#             BD3 peak 8.934 nM, band 3.39x wide
#             spread BD1 -> BD3 = 0.852 decades
# sec 6.1   30 mm and 22 mm rings, same strain, two experiments: 36 %.
#           MEASURED. Every offered explanation is an environment variable.
# sec 9.2   Fig. 5 is FOUR panels and THREE results -- 5a is a simulation.
# sec 10    gamma_L vs shift begin R^2 = 0.91, CI repression efficiency vs
#           positional shift R^2 = 0.05 (P = 0.0191), everything else
#           R^2 < 0.001 with P > 0.75. ALL modelED: 100 simulations drawn
#           from 2,000 random sets, regressed against their own inputs.
# sec 3.2   10^2-10^4 cells in a 9 nL reactor against >=10^9 macroscale;
#           detection limit ~75 cells per reactor. MEASURED.
# sec 20.1  the deposited parameter set, QUOTED from BIOMD0000000296.
# sec 20.4  oscillatory branch opens D = 0.03673, upper crossing D = 0.16743
#           with period 73.6 h, coexistence lost near 0.176. COMPUTED, and
#           they reproduce the paper's own Fig. 3C to three digits.
# sec 20.5  the five dilution rates the authors ran and the regime they state
#           at each: four disagreements out of five, in opposite directions.
# sec 21.5  Tamsir's plate: 1 uL spots on a 7 mm square grid, 12 h between
#           layers as an EXTERNAL CLOCK. 12 h is stated as SUFFICIENT, not as
#           an arrival time, so no D is computed from it.
# sec 21.3  16 two-input functions from one library, 5-fold (XOR) to
#           335-fold (B gate) induction, no further genetic manipulation.
# sec 21.7  tandem gates add their two promoters' transfer functions; six of
#           seven matched and P_Tet-P_BAD did not -- the same two promoters
#           swapped in order.
# sec 22.2  Zhou version one on glucose: 2 mg/L in 72 h, and ethanol at the
#           highest observed 50 g/L stopped E. coli outright.
# sec 22.3  version two on xylose: 4 mg/L in 72 h, ethanol below the 0.1 g/L
#           detection limit, only ~8 % of taxadiene oxygenated.
# sec 22.4  the rest of the chain to 33 mg/L, and the atpFH knockout; 40:1
#           inoculum settling to 1:2 by 41 h.
# sec 12.2  Tsoi's Fig. 2D: the border moves ~5x with the burden form, and
#           the caption says the parameters were CHOSEN so it orders that way.
# sec 12.1  Fig. 1D's "Relative burden" axis is NOT Eq. 17's burden -- the
#           border at 70 would need mu_max/delta_v ~ 4e4 at n = 2. So no
#           number transfers off that panel, only the DIRECTION.
# COMPUTED by posb.dol_criterion at n = 2, mu_max/delta_v = 10, Hill burden.
# EVERY BURDEN AND BORDER BELOW IS PER ENZYME (B_1 = B_2), which is what
# dol_criterion's two arguments are; the single cell carries B = B_1 + B_2:
#             A: eta 1.0, delta_me 0.001 -> theta_I 1.1656, border 1.135146
#             B: eta 1.0, delta_me 0.5   -> theta_I 1.1156, border 1.355143
#             single-cell yields 0.323 (A) and 0.132 (B): both alive
# ---------------------------------------------------------------------------

# Move 4's eigenvalues are lambda -- session 11's notation, and PS5's.
# Move 2's LENGTH used to be written lambda too; docs/symbols.md moved it to
# ell_A, so lambda in this deck now means exactly one thing and the foot
# below DEFINES it on the slide where it first appears (bar B1) instead of
# disambiguating it, which is what bar B1 rules out.
LAMBDA_NOTE = ("λ is an eigenvalue of the Jacobian, as in session 11. "
               "The held-fixed parameters are printed on the figure.")


# ---------------------------------------------------------------------------
# STANDARD GEOMETRY, derived from theme's own numbers rather than guessed.
# The first build of this deck had 149 fit problems and almost all of them
# came from two mistakes worth writing down.
#
#  1. A TITLE MUST FIT ONE LINE. The title box is W - 2M = 11.93 in at the
#     32 pt title size, which theme's own `line_cap` makes 53 characters. At
#     54 it wraps, the box grows to 1.08 in, and it lands on anything placed
#     at 1.70 -- which is how five titles ended up sitting on a figure. Keep
#     titles under about 50 and the question never arises.
#  2. A TEXT COLUMN BESIDE A CROP IS NOT 6 IN WIDE. At 20 pt a 6 in column
#     holds 43 characters, so four rows of 150 characters is 5.5 in of text
#     in a 4.6 in band. The crop goes LEFT at x = M, the text column starts
#     at 5.60, and `rows` gets 7.03 in -- 50 characters a line, which is
#     about 120 characters a row for four rows in the band below.
#
# The crop goes left for a second reason: when a journal citation wraps,
# theme.paper_figure widens the citation box to 4.6 in and centers it on the
# image. Clamped at x = M that box runs 0.70 to 5.30, which is clear of a
# text column starting at 5.60. Centerd under a right-hand crop it would
# reach back under the text.
TOP = 1.72          # top of the body band
BOT = 6.36          # bottom of it, clear of the foot at 6.75
TXT = 5.60          # left edge of the text column beside a crop


def _crop(d, s, key, ref, cap, x=M, y=TOP, h=3.42, max_w=4.80):
    """A paper crop whose SLOT IS SIZED FROM THE FILE'S OWN ASPECT RATIO.

    theme.paper_figure letterboxes into the box it is handed and then reports
    a "slot much larger than the figure" when the aspects disagree -- eleven
    of this deck's crops did that on the first build, each one rendering
    small and floating in a big empty box. The aspect is a property of the
    file, so it is read from the file rather than guessed in this one.

    Returns the right edge the image occupies.
    """
    from PIL import Image
    from decks.theme import _resolve_paper_figure
    with Image.open(_resolve_paper_figure(key)) as im:
        iw, ih = im.size
    w = min(max_w, h * iw / ih)
    h = w * ih / iw
    d.paper_figure(s, key, x, y, w, h, ref, cap, show_caption=True)
    return x + w


def build():
    d = Deck("Session 24 — Working with more than one cell", session=24,
             subtitle="A signal that leaves the cell turns position into an "
                      "input. Splitting the work across cells puts each "
                      "half’s burden in a different cell.")
    # Printed time ranges are off, as in session 23. The badges are
    # structural -- pacing() tells one segment from the next by them -- and
    # carry no minutes, so nothing on screen claims a running order.
    d.show_badges = False
    # Adam, 8 Nov: the new aside standard applies going forward. Week 13
    # opts in; the taught decks keep what is posted.
    d.aside_standard = True

    _opening(d)
    _retrieval(d)
    _goals(d)
    _where(d)

    # STOP 1 -- Basu 2005: position becomes an input. Rebuilt
    # 14 November 2026 to the five-part shape: the paper
    # introduced, their logic and results, the design features,
    # the analysis, then one sentence on its own slide.
    _b1_paper(d)
    _s1_frame_object(d)
    _s1_frame_synthase(d)
    _s1_density(d)
    _s1_model(d)
    _s3_frame(d)
    _s3_close(d)
    _s3_far(d)
    _s3_between(d)
    _s3_betas(d)
    _s3_model(d)
    _s3_edges(d)
    _s3_band(d)
    _s3_variants(d)
    _s3_measured(d)
    _s3_bullseyes(d)
    _s3_senders(d)
    _s3_release(d)
    _s3_debrief(d)
    _b1_learning(d)

    # STOP 2 -- Karig 2018: what sets the reach. Rebuilt 14 November.
    # The length scale is now DERIVED (the substitution step forces
    # the square root); Karig is introduced before its numbers are
    # used; Wilke-Chang is explained rather than cited; and the reach
    # is bounded three ways against Basu's own 10 mm ring.
    _k2_paper(d)
    _k2_result(d)
    _s1_thresholds(d)
    _k2_wilkechang(d)
    _s2_lambda(d)
    _s2_xi(d)
    _k2_bound(d)
    _s2_release(d)
    _s2_debrief_ratio(d)
    _s2_debrief_universal(d)
    _k2_learning(d)

    # STOP 3 -- Tamsir 2011: placement becomes the program. Built
    # 14 November. Four slides, no graded technique. The paper, their
    # XOR (Fig. 3), their library (Fig. 4), one sentence.
    _t3_paper(d)
    _t3_xor(d)
    _t3_sixteen(d)
    _t3_learning(d)

    # STOPS 3 AND 4 ARE NOT REBUILT YET. What follows is the old
    # move 4 and move 5 material, left in running order so the deck
    # builds. DESIGN-v2-PLAN.md has what replaces it.
    _s5_declare(d)
    _z4_paper(d)
    _s5_zhou_glucose(d)
    _s5_zhou_xylose(d)
    _s5_criterion(d)
    _s5_dol_fig(d)
    _s5_caveat(d)
    _s5_release(d)
    _s5_debrief(d)
    _s5_debrief2(d)
    _z4_learning(d)

    _ledger_knobs(d)
    _ledger_constraints(d)
    _ledger_limits(d)
    _reading(d)

    # APPENDIX -- kept in the deck, not taught.
    _appendix_divider(d)
    _appendix_contents_1(d)
    _appendix_contents_2(d)
    _s1_steady(d)
    _s3_parts(d)
    _s2_ratio(d)
    _s2_frame(d)
    _s2_coefficients(d)
    _s2_lambda_fig(d)
    _s2_ledger(d)
    _s3_inverter(d)
    _s3_regression(d)
    _appendix_contents_3(d)
    _s4_frame(d)
    _s4_arms(d)
    _s4_build(d)
    _s4_qssa_reminder(d)
    _s4_reduce(d)
    _s4_jacobian(d)
    _s4_phase(d)
    _s4_qss_fig(d)
    _s4_restore(d)
    _s4_putback(d)
    _s4_hopf(d)
    _s4_box1b(d)
    _s4_fig2c(d)
    _s4_mismatch(d)
    _s4_faithful(d)
    _s4_release(d)
    _s4_debrief(d)
    _s4_poll(d)
    _s4_data(d)
    _s1_release(d)
    _s1_debrief(d)
    _s3_ffl(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    """Title and claim. The subtitle states what the hour teaches."""
    s = d.dark()
    d.text(s, "Session 24  \u00b7  Part II", M, 2.15, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "Working with more than one cell",
           M, 2.60, 9.4, 1.10, size=38, font=HEAD, bold=True, color=WHITE)
    d.text(s, "A signal that leaves the cell turns position into an input.",
           M, 3.90, 9.0, 0.50, size=20, color=MINT, spacing=1.2)
    d.text(s, "Splitting the work across cells puts each half\u2019s burden "
              "in a different cell.",
           M, 4.55, 9.0, 0.50, size=20, color=MINT, spacing=1.2)
    d.notes(s,
            "Two things today, and the subtitle is both of them.\n "
            "One. Put the signal outside the cell and it crosses a distance "
            "and decays while it crosses. A receiver at a given distance "
            "therefore reads a particular concentration, so position is an "
            "input. Basu built that and we solve it.\n "
            "Two. Cut a pathway in half and put each half in a different "
            "cell. Each cell carries less burden, and the price is that the "
            "intermediate has to leave one cell and get into the other. "
            "Tsoi\u2019s criterion decides when that trade is worth taking.\n "
            "Burden is session 19\u2019s number and selection is session "
            "23\u2019s. Today they are design variables rather than "
            "problems.")


def _retrieval(d):
    """Three retrievals and a pivot.

    All three reach back further than one session, which is the spacing
    argument in lecture-design 3. They are also the three things this hour
    needs in hand: session 2's convention is move 2's frame, session 10's
    saturation is the collision move 3 has to disarm, and session 19's
    burden number is what move 5's criterion is written in.
    """
    s = d.light()
    d.header(s, "open", "retrieval — sessions 2, 10 and 19")
    d.title(s, "Before we start")
    d.rows(s, [
        ("1", "Session 2: you have used t ≈ L²/2D_{A} three times. State the "
              "convention before the number — why does the course write 2 in "
              "that denominator rather than 6, and does the choice matter?"),
        ("2", "Session 10: a receiver's output stops growing above about "
              "47 nM AHL — more signal, no more output. Today's circuit "
              "does something different: its output goes LOW again when the "
              "signal gets large. Name the difference."),
        ("3", "Session 19: your circuit takes a tenth of the proteome. By "
              "Scott's linear laws, what does that cost you in growth rate?"),
        ("4", "All three of those are one cell. What changes when the thing "
              "making the signal is a different cell, a centimetre away?",
         AMBER),
    ], top=2.00, label_w=0.7)
    d.foot(s, "Session 2 wrote the diffusion coefficient D. In this hour a "
              "bare D is the reactor's DILUTION rate, so the signal's "
              "coefficient is D_{A} throughout.")
    d.notes(s,
            "ONE. L²/2D_{A}. The 2 is there because crossing a gap is a "
            "one-dimensional question: mean square displacement is 2Dt in "
            "one dimension, 6Dt in three. Does the choice matter — no. A "
            "factor of three is nothing against squaring the distance. Say "
            "which one you mean and move on. One micron in E. coli "
            "cytoplasm: about 65 ms.\n "
            "Say once, here: the coefficient is D_{A} today. A bare D in "
            "this hour is the reactor's dilution rate. Both are in the "
            "ledger at the end.\n "
            "TWO. Saturation is more input, no more output — the curve goes "
            "flat and stays flat. A band goes flat and then comes back "
            "DOWN. Different mechanism: saturation is one route running out "
            "of room, the band is a second route switching on. They will "
            "see the second one in ten minutes.\n "
            "THREE. About 2% of growth rate per 1% of proteome diverted, so "
            "a tenth of the proteome is roughly 20%. That number is what "
            "the last stop's design decision turns on.\n "
            "FOUR is the pivot. Take answers. Steer to: the signal has to "
            "get there, and it can be gone before it does.")


def _goals(d):
    s = d.light()
    d.header(s, "open", "what you should be able to do by the end")
    d.title(s, "Three questions")
    d.rows(s, [
        ("the reach", "A signal leaves the cell and decays while it travels. "
                      "What sets how far it gets, and which part of that is "
                      "yours to set?"),
        ("the window", "One circuit, one input, and an output that is on only "
                       "in the middle of the input range. What makes a "
                       "response do that, and what moves the window?"),
        ("the second strain", "When is a second strain worth building — and "
                              "what do you then have to engineer that you "
                              "never had to engineer inside one cell?"),
    ], top=2.05)
    d.notes(s,
            "I read the three out and say where each gets answered. I do "
            "NOT answer them here — the reach has a derivation behind it in "
            "the second stop and handing over the result first would waste "
            "it.\n "
            "THE REACH — second stop, Karig. It comes out of a balance "
            "between diffusion in and decay out, and the answer names which "
            "of the two is mine to set.\n "
            "THE WINDOW — first stop, Basu, and it is the next thing we do. "
            "Their own circuit, their own numbers.\n "
            "THE SECOND STRAIN — last stop, and it is the one the home "
            "guide grades.\n "
            "Worth saying out loud: all three have a quantitative answer "
            "today, not a qualitative one.")


def _where(d):
    s = d.light()
    d.header(s, "frame", "where this sits")
    d.title(s, "Other cells stop being the problem")
    d.rows(s, [
        ("sessions 19 to 22", "sharing was the problem. Your genes and the "
                              "host\u2019s draw on one ribosome pool, so "
                              "expressing anything costs growth rate. A "
                              "downstream module binds your regulator and "
                              "takes it out of circulation."),
        ("session 23", "the population removed your circuit on a schedule "
                       "you could compute, and no controller helped, because "
                       "the controller was inside the thing being removed."),
        ("today", "other cells are the device. A signal between them makes "
                  "position an input, and splitting a pathway between them "
                  "splits the burden.", AMBER),
        ("session 25", "the population is the carrier."),
    ], top=2.00, label_w=3.4)
    d.notes(s,
            "Five sessions have treated other cells and other modules as "
            "the thing that breaks a circuit, and the last one ended with "
            "the worst version of it: selection, which cannot be "
            "rejected.\n "
            "Today the same object changes sign, and in the two ways the "
            "subtitle names. A signal that leaves one cell and arrives at "
            "another makes distance an input. Cutting a pathway across two "
            "cells puts each half\u2019s burden in a different cell.\n "
            "Burden is session 19\u2019s number \u2014 one ribosome pool, "
            "shared. What it costs you over time is session 23\u2019s. "
            "Today both are quantities I set on purpose rather than "
            "problems I work around.")


# ================================================= MOVE 1 · it leaves ======
# FRAME on the paper's own object rather than a redraw. Basu Fig. 1a already
# draws the gradient, the three AHL levels and the receiver response at three
# distances -- bar D3: a mechanism figure is either publication-grade or
# taken from the paper, and this one is in the paper the room read.
def _s1_frame_object(d):
    s = d.light()
    d.header(s, "stop 1", "what they put on the plate")
    d.title(s, "What Basu put on the plate")
    _crop(d, s, "basu2005_fig1a",
          "Basu et al., Nature 434:1130–1134 (2005), Fig. 1a",
          "Fig. 1a: circuit, gradient, response.", h=3.95)
    d.rows(s, [
        ("sender", "a cell that MAKES the signal. Basu's sit on a paper disk "
                   "at the center of the plate."),
        ("receiver", "a cell that RESPONDS to it. The lawn is receivers, "
                     "spread flat on the agar."),
        ("AHL", "acyl-homoserine lactone, the signal. Basu's is 3OC6HSL; "
                "it crosses the membrane unaided."),
        ("what to look at", "output HIGH in the middle of the AHL range, "
                            "LOW at both ends. That is the band.", AMBER),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.assigned_on(TXT, 6.46, 7.0, s, prefix="You read this for today",
                  key="basu2005")
    d.notes(s,
            "I start on their picture rather than one of mine, because they "
            "drew exactly the thing the hour is about.\n "
            "Bottom left is the gradient — their caption calls it an "
            "approximation of the AHL gradient as a function of distance "
            "from the senders. Top left is the circuit at high, medium and "
            "low AHL. Right is what a receiver does at three distances.\n "
            "Sender and receiver are the two words for the hour and I define "
            "them here. We met them once in session 10 and that is a long "
            "time ago.\n "
            "Before any mathematics: the response is not "
            "monotone. Bright in the middle, dark at both ends. Hold that — "
            "it is the second half of the first hour.")


def _s1_frame_synthase(d):
    """The synthase, which Fig. 1a does not carry.

    DESIGN sec 2 is explicit that the enzyme making the signal is the one
    object that cannot be words: session 10's slide said a sender "makes
    AHL" and never named or drew the enzyme. luxI is drawn in the SENDER
    PLASMID MAP and nowhere else, so that panel is a frame slide of its own.
    """
    s = d.light()
    d.header(s, "stop 1", "the object, from the paper you read")
    d.title(s, "The enzyme that makes the signal")
    _crop(d, s, "basu2005_fig1b",
          "Basu et al., Nature 2005, Fig. 1b — the sender plasmid",
          "pSND: luxI behind P_{LTet-O1}.", h=3.95)
    d.rows(s, [
        ("LuxI", "the synthase. One gene, and that is the whole sender. "
                 "Nothing in the panel names an enzyme — their own caption "
                 "calls the senders constitutive."),
        ("the promoter's name lies",
         "P_{LTet-O1} is TetR-REPRESSED, and the strain DH5α carries no "
         "TetR. So nothing represses it and luxI runs flat out."),
        ("so a sender has one knob",
         "how much LuxI each sender makes. A promoter choice, and the only "
         "thing about a sender you set.", AMBER),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "Session 10 told this room that a sender makes AHL and never "
            "named the enzyme or showed it. Here it is: one gene, luxI, and "
            "the sender is that gene behind a promoter.\n "
            "The promoter name is worth thirty seconds because it is a trap. "
            "P-L-tet-O-1 is repressed by TetR. There is no TetR in DH5 "
            "alpha. So the promoter is not being regulated by anything and "
            "the senders express constitutively, which is what their own "
            "caption says. If anyone has read the name as a TetR-driven "
            "sender, this is where to fix it.\n "
            "And it gives me the one sender knob: how much synthase. "
            "Everything else about the gradient belongs to the agar.")


def _s1_density(d):
    """What a receiver reads is cell number per volume. An identity, not a
    measurement -- so it needs no number the course cannot source."""
    s = d.light()
    d.header(s, "stop 1", "what a molecule outside the cell reports")
    d.title(s, "A receiver reads how many senders share its volume")
    d.rows(s, [
        ("one cell does make a concentration",
         "it is just far below what any receiver here responds to. Basu\u2019s "
         "lower band edge is 2.61 nM, and one cell\u2019s synthase cannot hold "
         "the medium around it anywhere near that."),
        ("what sets the number the receiver sees",
         "molecules made per cell, times how many cells share the volume, "
         "divided by that volume. The receiver reads cells per volume. "
         "Nothing counted anything."),
        ("so the volume is part of the circuit",
         "the same cells with the same synthase give a different reading in "
         "a droplet and in a flask. Change the vessel and you have changed "
         "the input.", AMBER),
    ], top=1.95, label_w=3.9, bottom=6.10)
    d.foot(s, "This is QUORUM SENSING: a cell makes a small molecule that "
              "others read as a measure of how many of them there are. "
              "2.61 nM is solved later this segment from Basu\u2019s own "
              "printed parameters.")
    d.notes(s,
            "First thing a molecule outside the cell buys, and it is free.\n "
            "I am precise about the one-cell case. A single cell makes a "
            "concentration. It cannot make one this receiver responds to, "
            "because the lower edge of the band is single-digit nanomolar "
            "and one cell\u2019s output into an open volume is far under it.\n "
            "The second row is an identity and I write it as one: "
            "concentration is output per cell times cell number over "
            "volume. No cell measures anything. The volume does the "
            "arithmetic.\n "
            "The design consequence is the third row. The vessel is a "
            "circuit parameter. That is new to them and it comes back at "
            "the ledger.")


def _s1_thresholds(d):
    """Two measured half-activations, and the crosstalk in the same paper.

    Bar F5 -- the measurement before the statistic. "Half-activation" is
    defined in words and the comparison it came from is named BEFORE the two
    numbers, because 0.003 against 3 is meaningless until the room knows
    each was measured against its OWN cognate signal.
    """
    s = d.light()
    d.header(s, "segment 1", "what a molecule outside the cell can report")
    d.title(s, "A sensitivity gap that buys no orthogonality")
    _crop(d, s, "karig2018_fig1",
          "Karig et al., PNAS 115:6572–6577 (2018), Fig. 1A",
          "Their two-signal circuit.", h=3.95)
    d.rows(s, [
        ("what they measured", "receivers were given a dose series and their "
                               "reporter read. HALF-ACTIVATION is the "
                               "concentration giving half the maximum."),
        ("two homologous systems",
         "3OC12HSL on its own receptor: 0.003 µM. C4HSL on its own: 3 µM. "
         "Each to its OWN cognate signal."),
        ("and the gap buys nothing",
         "the same paper measures 3OC12HSL competitively binding RhlR, the "
         "C4HSL receptor. Specificity came from the promoter.", RED),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.foot(s, "ORTHOGONAL here means two signal/receptor pairs that do "
              "not talk to each other. Not the geometric sense.")
    d.notes(s,
            "Karig is one of the optional papers and it is where the only "
            "sourced numbers in the first half of this hour come from.\n "
            "I say what was measured before I say the numbers. They gave "
            "cells a dose series and read a reporter; half-activation is "
            "where the reporter gets to half of its own maximum. Three "
            "nanomolar for one signal, three micromolar for the other — a "
            "factor of a thousand between two systems that are close "
            "relatives.\n "
            "Then the correction, and it is the teaching point. A "
            "thousandfold difference in sensitivity does not make two "
            "signals independent. Their own supplement has a section "
            "titled signal specificity and competitive inhibition, and it "
            "measures the long signal competitively binding the short "
            "signal's receptor. Specificity came from the promoter.\n "
            "If anyone leaves here thinking a sensitivity gap is an "
            "orthogonality argument, somebody will build a circuit on it.")


def _s1_model(d):
    """T64, and it is on PS9 AND the final.

    A plain step run rather than derivation_fig: DESIGN sec 7 assigns
    derivation_fig to moves 2, 3 and 4, and move 1's object is already drawn
    -- it is Basu's Fig. 1a and 1b, two slides of frame. FOUR steps and no
    closing box, deliberately: five steps or a closing box pushes the pitch
    under 0.86 in, and below that theme suppresses the asides on every step
    but the live one. The asides are where every symbol in this model is
    defined, so losing them would cost the deck bar section B.
    """
    d.derivation(
        None, "stop 1", "build  ·  a sender and a receiver, from scratch",
        "The smallest model of a sender and a receiver",
        [
            ("the sender makes it",
             "dA/dt = k_{I} S",
             "A the signal in the agar · S the sender density · "
             "k_{I} per sender"),
            ("it decays where it sits",
             "dA/dt = k_{I} S − γ_{A} A",
             "γ_{A} is first-order decay, and it belongs to the medium"),
            ("a reactor dilutes too",
             "dA/dt = k_{I} S − γ_{A} A − D A",
             "D is the vessel's dilution rate. On a plate D is zero."),
            ("the receiver reads it",
             "output = α A^{n} / (θ_{A}^{n} + A^{n})",
             "α the maximum · θ_{A} the half-output concentration · "
             "n the sharpness"),
        ],
        note="Two equations, and between them they are the whole of a "
             "sender-receiver link. I write them with the room rather than "
             "showing them.\n "
             "The sender term has no concentration in it, only a density. "
             "That is the density-reporting line from a moment ago, in "
             "symbols: the signal made per unit volume goes up with how "
             "many senders are in the volume.\n "
             "The decay term is where the medium enters. Basu say so on "
             "their last page — the AHL decay rate sets the steepness of "
             "the gradient, and it is pH-sensitive.\n "
             "The dilution term is zero on a plate and nonzero in a "
             "reactor, and it is the same D that runs all of the second half "
             "of this hour.\n "
             "The receiver is a Hill function and they have had that since "
             "session 6. Theta-A is the half-output concentration and n is how "
             "sharp the turn-on is.")


def _s1_steady(d):
    """T64's result, composed, and the figures module draws the composition.

    `fig_sender_receiver` arrived in figures/s24_communities.py while this
    deck was being written and it is the right object for this slide: two
    rules on one axis, the SAME senders behind two different promoters, so
    the claim that k_I is the knob is made graphically rather than asserted
    (bar C4).
    """
    s = d.light()
    d.header(s, "stop 1", "build  ·  what the pair says")
    d.title(s, "The output is a report on sender density")
    d.text(s, "Set dA/dt = 0:      A* = k_{I} S / (γ_{A} + D)",
           M, 1.66, W - 2 * M, 0.52, role="emphasis", font=HEAD, bold=True,
           color=INK)
    d.image_centered(s, FIG + "s24_sender_receiver.png", top=2.26, band=4.44)
    d.foot(s, "k_{I} is ours — neither paper prints a sender rate, so the "
              "session supplies it, and it is a promoter choice. No position "
              "appears in either equation: one well-mixed volume, one "
              "number.")
    d.notes(s,
            "Setting the derivative to zero gives the one line the whole "
            "move was for: the signal is sender density over total removal. "
            "Through the Hill function, the receiver's output is a readout "
            "of how many senders are nearby.\n "
            "Both rules on this figure are the SAME senders. The only "
            "difference is the promoter driving the synthase — a fourfold "
            "change — and the same population is then read at ten percent "
            "of the receiver's range or at sixty-four. So k sub I is not a "
            "nuisance parameter; it is where you set the detection point.\n "
            "I am explicit that the number is mine. Neither paper prints it. "
            "Basu's model has no sender in it at all — equations one to four "
            "take AHL as an input, and the senders were tuned until the ring "
            "landed at seven millimetres, with the value never printed. "
            "Balagaddé's equations are in a supplement we do not hold. So "
            "what I am really choosing when I choose it is a promoter.\n "
            "And the limitation, so nobody carries the wrong thing into the "
            "next half: there is no x in either equation. This is one "
            "volume. The gradient has to be built.")


def _s1_release(d):
    """RELEASE on a different object from the build: an antidote, not a
    reporter. And it is Balagaddé's predator, which move 4 opens on -- so
    the release does work twice.
    """
    s = d.light()
    d.header(s, "segment 1", "pose  ·  on your own paper  ·  vote, then argue")
    d.title(s, "Your turn: a receiver that survives")
    d.rows(s, [
        ("the circuit", "a cell makes a toxin constitutively, and the toxin "
                        "kills it. The arriving signal switches on an "
                        "ANTIDOTE that neutralises the toxin. Nothing else "
                        "changes."),
        ("write", "the antidote's equation, in the symbols of the model we "
                  "just built, with one new symbol for the antidote itself.",
         AMBER),
        ("then answer", "the cell lives or dies as a function of WHAT? Name "
                        "the quantity, and say where it is set.", AMBER),
    ], top=2.05, label_w=2.6, bottom=5.60)
    d.text(s, "You need one decision before you can answer the second "
              "question: which symbol in the model is set outside the dying "
              "cell.",
           M, 5.80, W - 2 * M, 0.62, role="body", bold=True, color=TEAL,
           spacing=1.12)
    d.notes(s,
            "This is a different object from the one we just built. The "
            "receiver's output was a reporter; now it is the thing that "
            "keeps the cell alive, and the structure of the model does not "
            "change at all.\n "
            "What I want them to reach is that survival is a function of "
            "sender density — of how many OTHER cells are nearby — and that "
            "the quantity is set outside the cell that is dying.\n "
            "The second question is the one worth the time. People write the "
            "equation quickly and then have to decide what it is a function "
            "of, and the answer is the hour's thesis.")


def _s1_debrief(d):
    s = d.light()
    d.header(s, "segment 1", "debrief  ·  the answer, on its own object")
    d.title(s, "A cell whose survival is set by its neighbors")
    d.text(s, "dX/dt = α A^{n} / (θ_{A}^{n} + A^{n})  −  γ_{X} X",
           M, 1.82, W - 2 * M, 0.56, role="emphasis", font=HEAD, bold=True,
           color=INK)
    d.text(s, "X is the antidote and γ_{X} its decay. Nothing else is new.",
           M, 2.44, W - 2 * M, 0.40, role="body", color=MUTED)
    d.rows(s, [
        ("the sender is unaffected",
         "the sender does not care what the receiver does with the signal. "
         "A* = k_{I}S/(γ_{A}+D), exactly as before."),
        ("so survival tracks S",
         "X rises with A, and A rises with sender density S. The cell lives "
         "while X stays ahead of the toxin — and S is set by how many "
         "senders share the volume.", AMBER),
        ("this is not hypothetical",
         "it is Balagaddé's predator. CcdB is the toxin, made whether the "
         "predator likes it or not; CcdA is the antidote, switched on by the "
         "prey's signal."),
    ], top=2.96, label_w=3.1, bottom=6.00)
    d.sources(s, [("CcdA rescuing against CcdB, and the promoter it runs from",
                   "Balagaddé et al., Mol Syst Biol 2008, Box 1A and p. 3")],
              y=6.24)
    d.notes(s,
            "Here is the answer. One new variable, one Hill term, one decay "
            "term, and the sender's equation untouched — which is the part "
            "people get wrong, because it feels like the receiver should "
            "feed back.\n "
            "Survival goes as sender density. A cell carrying this circuit "
            "is alive because of a quantity set by other cells, and that is "
            "a kind of coupling no single-cell circuit in this course has "
            "had.\n "
            "And they have already read the paper that built it. "
            "Balagaddé's predator makes CcdB constitutively and is rescued "
            "by CcdA, which the prey's signal turns on. We come back to that "
            "circuit in full later in the hour. For now the point is that "
            "the release they just did is a real device.")


# ============================================ MOVE 2 · how far it gets =====
def _s2_frame(d):
    """FRAME: session 2's own formula, restated on this slide.

    Bar F1 -- a system the slide argues about is drawn on that slide. The
    thing this move leans on is a FORMULA and a CONVENTION, so restating it
    in full, with the number session 3 used it to reach, is the redraw. The
    room is not asked to carry it from twenty-two sessions ago.
    """
    s = d.light()
    d.header(s, "stop 2",
             "frame  ·  their ring sits at 10 mm — what sets that?")
    d.title(s, "The same estimate over four more decades")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.78, W - 2 * M, 1.06, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "t  ≈  L² / 2D_{A}",
           M + 0.35, 1.92, 4.2, 0.50, size=32, font=HEAD, bold=True,
           color=INK)
    d.text(s, "L the distance · D_{A} the coefficient · t the time"
              "\nConvention: 2D_{A}, not 6D_{A} — say which first.",
           M + 4.8, 1.94, 7.3, 0.76, role="body", color=BODY, spacing=1.12)
    d.rows(s, [
        ("sessions 2 and 3",
         "one micron of E. coli cytoplasm, at 7.7 µm²/s for GFP, is "
         "about 65 ms. That is what session 3 used to argue there is no "
         "gradient inside one cell."),
        ("what changed today",
         "nothing in the formula. L went from a micron to a centimetre — "
         "four orders of magnitude — and t goes as L², so the estimate moves "
         "by eight.", AMBER),
        ("so the inequality flips",
         "inside one cell diffusion is fast enough that position is not a "
         "variable. Across a plate it is slow enough that position is the "
         "only variable."),
    ], top=3.06, label_w=3.4, bottom=6.34)
    d.notes(s,
            "I put session 2's formula back on the slide rather than asking "
            "anyone to remember it. L is the distance, D-sub-A the "
            "coefficient of whatever is moving, and the convention is two "
            "D — session 2's first habit is to say "
            "which denominator you mean, because an unstated convention is "
            "an argument you cannot settle afterwards.\n "
            "Sixty-five milliseconds for a micron. That is the number that "
            "let session 3 say there is no gradient inside a bacterium, and "
            "it was the right conclusion.\n "
            "Now change nothing but L. A centimetre is ten thousand microns, "
            "and the time goes as the square, so the estimate moves by a "
            "factor of a hundred million. The same formula that abolished "
            "position inside the cell makes position the whole story "
            "outside it.")


def _s2_ledger(d):
    s = d.light()
    d.header(s, "segment 2", "build  ·  four decades of distance")
    d.title(s, "Four decades of distance is eight of time")
    d.image_centered(s, FIG + "s24_diffusion_ledger.png", top=1.76,
                     band=4.60)
    d.foot(s, "Session 2 also measured which way this estimate is wrong: for "
              "anything large it is OPTIMISTIC, by more than an order of "
              "magnitude, because the effective viscosity depends on the "
              "size of the probe.")
    d.notes(s,
            "Two lines, slope two, four decades of distance and eight of "
            "time. A signal that crosses one cell in milliseconds takes days "
            "to cross a hundred millimetres of plate, and nothing on the "
            "plasmid changes that number.\n "
            "The only thing on this figure a designer picks is WHICH LINE — "
            "which of the two signals the circuit uses. Karig measured that "
            "the choice is worth about twentyfold, and Karig's own "
            "decomposition of it is in this segment's debrief.\n "
            "The foot is the honest boundary and I say it out loud. This "
            "estimate is not conservative. Session 2 found it optimistic by "
            "more than ten times for anything the size of a protein or "
            "bigger, because viscosity is not a single number — it depends "
            "on what is moving through it.")


def _s2_coefficients(d):
    """The four numbers, and the comparison version 1 of the design got wrong.

    83 um^2/s and 87 um^2/s are not comparable quantities: one is an
    EFFECTIVE CELL-TO-CELL coefficient fitted to a wave through a lawn, the
    other a free-solution value for a protein. The near-coincidence is not a
    result, and the slide says so where the two numbers sit.
    """
    s = d.light()
    d.header(s, "stop 2", "build  ·  the numbers, and what each one is")
    d.title(s, "Only two of these four are signals")
    rows = [("3OC12HSL", "83 µm²/s", "Karig 2018 — ESTIMATED, by fitting a "
                                     "fluorescence wave profile. Effective "
                                     "CELL-TO-CELL, through a bacterial "
                                     "lawn.", TEAL),
            ("C4HSL", "1,810 µm²/s", "Karig 2018 — the same measurement, the "
                                      "other signal.", CYAN),
            ("GFP in E. coli", "7.7 µm²/s", "session 2 — a protein in "
                                            "cytoplasm.", MUTED),
            ("GFP in water", "87 µm²/s", "session 2 — a protein in free "
                                         "solution.", MUTED)]
    y = 1.86
    for k, val, why, col in rows:
        d.shape(s, S.ROUNDED_RECTANGLE, M, y, 0.14, 0.74, fill=col, line=None)
        d.text(s, k, M + 0.34, y, 2.5, 0.34, role="body", font=HEAD,
               bold=True, color=INK)
        d.text(s, val, M + 2.95, y, 1.9, 0.34, role="emphasis", font=HEAD,
               bold=True, color=col if col != MUTED else INK)
        d.text(s, why, M + 5.05, y, 7.0, 0.70, role="caption", color=BODY)
        y += 0.88
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.50, W - 2 * M, 1.02, fill=None,
            line=RED, lw=2)
    d.text(s, "83 and 87 are not the same kind of number, and the near-match "
              "is not a result.\nOne is a signal fitted to a wave through "
              "cells; the other is a protein in water. Do not put them side "
              "by side and call it a speed.",
           M + 0.3, 5.62, W - 2 * M - 0.6, 0.80, role="body", color=RED,
           spacing=1.12)
    d.notes(s,
            "Two of these four are signals and two are the protein the room "
            "already has a number for. The two signals are the only sourced "
            "diffusion coefficients anywhere in this session's folder.\n "
            "The word on both of Karig's numbers is theirs: ESTIMATED. They "
            "did not put a molecule in an instrument — they fitted the "
            "profile of a fluorescence wave moving across a lawn and "
            "inferred the coefficient. And what comes out of that is an "
            "EFFECTIVE cell-to-cell coefficient, which is a property of the "
            "lawn as much as of the molecule.\n "
            "The red box is a trap I want closed. Eighty-three and "
            "eighty-seven look like the same number and they are not the "
            "same quantity, so the coincidence means nothing. One is a small "
            "signal crawling through packed cells; the other is a protein in "
            "water.\n "
            "And the one that matters for the rest of the hour: "
            "eighty-three is 3OC12HSL. Basu's signal is 3OC6HSL. Neither of "
            "Karig's molecules is Basu's, so neither number can be carried "
            "onto Basu's plate.")


def _s2_ratio(d):
    """What kind of knob a diffusion coefficient is: not one.

    DESIGN sec 4's ledger and this slide have to agree, and they do: the
    PAIR is the choice, the coefficients are inherited. "Turing instability"
    is defined here, before it carries an argument (bar B3), and the
    condition travels with it (bar F3) -- the critical ratio comes out of
    the kinetics, so no number is stated here. The ~100 belongs to the
    debrief, after they have been asked.
    """
    s = d.light()
    d.header(s, "stop 2", "build  ·  which of these is a design variable")
    d.title(s, "A diffusion coefficient is not a dial")
    d.rows(s, [
        ("you cannot set D_{A}", "you pick a signal and inherit its coefficient "
                             "in the medium you have. Nothing you can do to "
                             "the molecule makes it diffuse much faster."),
        ("what you do set", "WHICH PAIR of signals the circuit uses, out of "
                            "a short menu of quorum systems. That fixes the "
                            "ratio you start from.", AMBER),
        ("why a ratio at all",
         "a TURING INSTABILITY is a uniform state going unstable to a "
         "pattern because the two species spread at different rates. How "
         "much faster comes out of the Jacobian of your own KINETICS."),
        ("Karig's pair, measured",
         "the ratio of their two coefficients, as the circuit meets it: "
         "21.6 ± 10. Their word for it is measured.", TEAL),
    ], top=1.88, label_w=3.4, bottom=6.08)
    d.sources(s, [("the two coefficients and their ratio",
                   "Karig et al., PNAS 2018, main text p. 6573 and SI")],
              y=6.24)
    d.notes(s,
            "This is the slide that says what kind of quantity we are "
            "dealing with, and the answer is: not a knob. I cannot make a "
            "molecule diffuse faster. I choose a molecule and I inherit "
            "whatever it does in the medium I have.\n "
            "What I do choose is the pair. There are a handful of quorum "
            "systems with usable receptors, and choosing two of them fixes "
            "the ratio I start from.\n "
            "Turing instability is a new term for this room and I define it "
            "here. A uniform state goes unstable to a pattern because one "
            "species outruns the other. For an activator and an inhibitor "
            "the inhibitor is the one that has to outrun — and the amount "
            "is not a universal constant. It comes out of the Jacobian of "
            "whatever kinetics you wrote down, so you cannot quote it "
            "without naming a scheme. I am deliberately not giving a number "
            "here.\n "
            "Twenty-one point six, plus or minus ten, is what Karig's "
            "circuit experienced. Where that number came from is "
            "the thing I am about to ask them.")


def _s2_lambda(d):
    """BUILD with the picture advancing: ell_A = sqrt(D_A/gamma_A).

    The length is ell_A, not lambda: lambda is an eigenvalue in move 4 and
    in sessions 8, 11 and 14, and T29 is autograded on PS5 (docs/symbols.md).
    The figure function and PNG names are still the historical lambda ones.

    Four steps, two pictures. The figure column is 5.4 x 4.95 in and the
    text column holds about 42 rendered characters, which is why the step
    labels are short -- a line that does not fit is a step doing more than
    one move.
    """
    d.derivation_fig(
        "stop 2", "build  ·  the length scale, derived",
        "How far a signal gets once it decays",
        [
            ("a source at x = 0",
             "A(x) = ?",
             "one dimension, and let it settle"),
            ("diffusion in, decay out",
             "0 = D_{A} d²A/dx² − γ_{A} A",
             "at steady state the two have to balance"),
            ("try a decaying exponential",
             "A = A_{0} e^{−x/ℓ}  ⇒  d²A/dx² = A / ℓ²",
             "differentiating twice returns the same shape"),
            ("substitute, and ℓ is forced",
             "0 = A (D_{A}/ℓ² − γ_{A})  ⇒  ℓ² = D_{A}/γ_{A}",
             "the bracket must vanish, so only one ℓ solves it"),
            ("so the length is a square root",
             "ℓ_{A} = √(D_{A} / γ_{A})",
             "D_{A} is length²/time, γ_{A} is 1/time"),
        ],
        [FIG + "s24_lambda_step_1.png", None, None,
         FIG + "s24_lambda_step_2.png", None],
        closing="γ_{A} is the knob — Basu say it sets the steepness.",
        note="This is the replacement for the estimate we opened the "
             "segment with. L squared over 2D answers how long a signal "
             "takes to get somewhere. It says nothing about whether any of "
             "the signal is still there when it arrives.\n "
             "So: a source at the origin, let it settle, and balance what "
             "diffuses in against what decays away. One line of algebra and "
             "the answer is an exponential with a single length in it.\n "
             "Ell-A is the distance over which the signal falls by a "
             "factor of e. Check the units out loud — D-sub-A is length squared "
             "over time, the decay rate is one over time, so the square "
             "root of their ratio is a length. That check is most of why to "
             "trust the formula.\n "
             "And the knob is the decay rate, not the coefficient. Basu "
             "hand that over on their last page: the AHL decay rate sets "
             "the steepness of the gradient and it is pH-sensitive. So I "
             "change the reach of my signal by changing the medium.")


def _s2_lambda_fig(d):
    s = d.light()
    d.header(s, "stop 2", "build  ·  what the square root costs")
    d.title(s, "Doubling the reach costs four times the lifetime")
    d.image_centered(s, FIG + "s24_lambda_scaling.png", top=1.76, band=4.60)
    d.foot(s, "Both curves are Karig's signals in Karig's own lawn. Neither "
              "molecule is Basu's 3OC6HSL, so there is no ℓ_{A} here for Basu's "
              "band — and this folder cannot source one.")
    d.notes(s,
            "The square root is the whole economics of the formula. To "
            "double how far the signal reaches I have to make it last four "
            "times as long, and lifetime is bought in the medium — "
            "buffering, pH, whatever is degrading it.\n "
            "The foot is the part of this slide I most want said out loud, "
            "and it is the honest answer to the obvious question. There is "
            "no ell-A on here for Basu's band. Both curves are Karig's "
            "molecules measured through Karig's lawn, and Basu's signal is a "
            "different molecule in a different lawn. If I combined Karig's "
            "coefficient with Basu's decay rate I would get a number, and "
            "it would be a number about nothing.\n "
            "What it would take to get a real one: a measured coefficient "
            "for 3OC6HSL in agar, with the medium stated. Nobody in this "
            "folder has published one, so we teach the formula and say so.")


def _s2_xi(d):
    """T66's engineering lesson, and it is better than any number.

    The arithmetic is reproducible from printed numbers alone and it reaches
    a correct engineering conclusion: the paper's own parameter cannot be a
    diffusion coefficient. NUMBERS.md 13.3, re-run by posb.diffusion_time.

    The three rows this slide carried are now one line and a foot: a figure
    in a 3.90 in band leaves room for two lines of text under it, and three
    rows of prose need three times that.
    """
    s = d.light()
    d.header(s, "stop 2", "build  ·  a parameter that fails its own paper")
    d.title(s, "A published coefficient that is not one")
    d.image_centered(s, FIG + "s24_xi_check.png", top=1.70, band=3.90)
    d.text(s, "Their equation (5) is a bare discrete Laplacian with no grid "
              "spacing Δx, so the coefficient in it has to be D_{A}/Δx² — "
              "and Δx is never printed. The units are D_{A}'s; the quantity "
              "is not.",
           M, 5.78, W - 2 * M, 0.46, role="body", bold=True, color=INK)
    d.foot(s, "ξ = 0.001 mm²/min is printed in their parameter table as AHL "
              "intercellular diffusion. It puts their own 10 mm ring 833 h "
              "out. Their run was 36 h and the ring was stable by 32 h.")
    d.notes(s,
            "This is the one I want them to take away from the length-scale "
            "half of the hour, and it is a method rather than a number.\n "
            "Basu print one diffusion number. Put it into the course's own "
            "estimate with the paper's own ring position and the ring "
            "arrives thirty-four days after the experiment finished. Every "
            "length in their own figures fails the same way, by one to two "
            "orders of magnitude.\n "
            "The resolution is in their equation five. It is a discrete "
            "Laplacian — the sum of six neighbors minus six times the "
            "center — with no lattice spacing anywhere in it. For that "
            "equation to balance, the coefficient must be D-sub-A over delta x "
            "squared, and delta x is never stated. So the printed units are "
            "the units of a diffusion coefficient and the printed quantity "
            "is not one.\n "
            "The lesson: check a published coefficient against that paper's "
            "own geometry and its own duration before you use it. It takes "
            "two lines and it would have caught this.")


def _s2_release(d):
    s = d.light()
    d.header(s, "stop 2", "pose  ·  on your own paper  ·  vote, then argue")
    d.title(s, "Your turn: a pair only a factor of three apart")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.84, W - 2 * M, 1.62, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "You have two signals whose FREE-SOLUTION diffusion "
              "coefficients differ by a factor of 3, and you want a pattern.",
           M + 0.32, 1.98, W - 2 * M - 0.64, 0.80, role="emphasis",
           color=INK, spacing=1.12)
    d.text(s, "Your circuit needs the two to spread at different enough "
              "rates for the uniform state to go unstable.",
           M + 0.32, 2.90, W - 2 * M - 0.64, 0.44, role="body", color=BODY)
    d.rows(s, [
        ("a", "name TWO things you could change to widen the ratio the "
              "circuit really sees.", AMBER),
        ("b", "name ONE reason you might get a pattern without widening it "
              "at all.", AMBER),
    ], top=3.70, label_w=0.5, bottom=5.20)
    d.text(s, "Neither answer is a change to either molecule's chemistry. "
              "That is the constraint to reason inside.",
           M, 5.50, W - 2 * M, 0.46, role="body", bold=True, color=TEAL)
    d.notes(s,
            "I ask for two of one thing and one of another because the "
            "question has two halves and students will otherwise answer only "
            "the first.\n "
            "Part a: the honest answers are the signal's interaction with "
            "the cells and the lawn itself. Not the molecules — the "
            "free-solution ratio is close to fixed by molecular size.\n "
            "Part b: because the critical ratio is not universal, and "
            "because noise in a small population does work that the "
            "deterministic analysis leaves out.\n "
            "The line at the bottom is there to stop the answer I do not "
            "want, which is engineer the molecule. If they say that, I ask "
            "what they would change about an acyl chain to double a "
            "diffusion coefficient.")


def _s2_debrief_ratio(d):
    s = d.light()
    d.header(s, "stop 2", "debrief  ·  part a, where a ratio comes from")
    d.title(s, "Karig's ratio was mostly the lawn")
    d.rows(s, [
        ("free solution", "the Wilke–Chang correlation predicts a "
                          "free-solution coefficient from molecular size. "
                          "For Karig's pair it gives about 1.5."),
        ("through a lawn", "they measured 21.6 ± 10 — the ratio the circuit "
                           "experienced.", TEAL),
        ("so about fourteen of that is cells",
         "which answers part a. The two things you change are how the signal "
         "interacts with the cells, and the lawn itself. The number you can "
         "move is the EFFECTIVE coefficient, never the molecule's.", AMBER),
        ("their mechanism, hedged",
         "they attribute the slow signal to 3OC12HSL partitioning into the "
         "membrane — and write likely due to in the main text, one possible "
         "explanation in the supplement."),
    ], top=1.88, label_w=3.6, bottom=6.30)
    d.notes(s,
            "The decomposition is the answer. Molecular size predicts a "
            "ratio of about one and a half for these two molecules. The "
            "circuit saw twenty-one point six. So about fourteen of the "
            "twenty-one came from somewhere other than the molecules, and "
            "the only other thing in the experiment is the cells.\n "
            "That is what makes part a answerable. You cannot change the "
            "free-solution ratio in any useful way. You can change what the "
            "signal does when it meets a membrane, and you can change the "
            "lawn — how dense it is, what it is made of.\n "
            "Their proposed mechanism is partitioning into the membrane, "
            "and I quote their hedge rather than theirs as a result. The "
            "main text says likely due to. The supplement says one possible "
            "explanation. That is an honest paper and I read it honestly.")


def _s2_debrief_universal(d):
    """Their own figure makes the stochastic argument; rows cannot."""
    s = d.light()
    d.header(s, "stop 2", "debrief  \u00b7  part b")
    d.title(s, "Noise beats the deterministic requirement")
    _crop(d, s, "karig2018_fig3dg",
          "Karig et al., PNAS 115:6572\u20136577 (2018), Fig. 3D\u2013G",
          "Their models, same circuit, two diffusion ratios.", h=3.42)
    d.rows(s, [
        ("D", "the deterministic model, handed a ratio of 100. It patterns."),
        ("F, upper", "the same deterministic model at the MEASURED 21.6. "
                     "Flat in both channels. No pattern."),
        ("F, lower", "the stochastic model at that same 21.6. It patterns.",
         AMBER),
        ("so the ratio is not the whole condition",
         "small populations make noise part of the dynamics, not a "
         "correction to it \u2014 session 12, in space."),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.foot(s, "Their abstract: the stochastic treatment puts no severe "
              "requirement on the ratio. The factor of 100 is their own "
              "non-stochastic simulation, not a classical law.")
    d.notes(s,
            "This is the figure that makes the point, so I put it up rather "
            "than describe it.\n "
            "Top left, D: give the deterministic model a hundredfold "
            "difference and it makes spots. That is the textbook Turing "
            "result.\n "
            "Bottom left, F: two rows. The upper pair is the SAME "
            "deterministic model run at the ratio they actually measured, "
            "twenty-one point six, and both channels are flat. The lower "
            "pair is the stochastic model at that same ratio, and the "
            "pattern is back.\n "
            "So the hundredfold is a property of the smooth analysis. Their "
            "populations are small enough that fluctuations are part of the "
            "dynamics, which is session 12 moved into space.\n "
            "What I want carried out of here: a critical ratio belongs to "
            "your kinetics and your population size. It is never a number "
            "you look up.")


def _k2_result(d):
    """Karig's experimental result, shown rather than cited."""
    s = d.light()
    d.header(s, "stop 2", "the result")
    d.title(s, "Spots in one channel, voids in the other")
    _crop(d, s, "karig2018_fig2a",
          "Karig et al., PNAS 115:6572\u20136577 (2018), Fig. 2A",
          "One lawn, two channels. Scale bar 100 \u00b5m.", h=2.30)
    d.rows(s, [
        ("what it is", "a lawn that started uniform and isogenic, with no "
                       "IPTG. Every cell carries the same circuit."),
        ("the pattern", "red spots, and voids in the green channel at the "
                        "same places.", TEAL),
        ("why it is here", "the coefficient we are about to use was fitted "
                           "from a wave crossing this lawn, so the number "
                           "inherits this system."),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "I show their result before I use their number.\n "
            "The lawn is isogenic and starts uniform. No gradient is "
            "imposed, nobody spots senders anywhere. The pattern is "
            "emergent, which is the claim in their title.\n "
            "Red spots, green voids, same places. Two reporters reading one "
            "underlying pattern.\n "
            "And the reason it belongs in this stop: the eighty-three "
            "microns squared per second we are about to use was fitted from "
            "a wave moving through this lawn. The number inherits this "
            "system.")


# ===================================== MOVE 3 · a motif on a new input =====
def _s3_frame(d):
    """FRAME on the printed truth table: non-monotonicity as a LOGICAL fact.

    The table is typeset on the slide as well as being inside the crop,
    because the printed one is small and the whole frame is that the room
    can read three rows and see that the middle one is different before any
    kinetics exist.
    """
    s = d.light()
    d.header(s, "stop 1", "frame  ·  their truth table, before any model")
    d.title(s, "The output is off, on, off across AHL")
    _crop(d, s, "basu2005_fig1a", "Basu et al., Nature 2005, Fig. 1a",
          "The same panel, read for its logic.", h=3.95)
    hdr = ("AHL", "CI", "LacI_{M1}", "LacI", "GFP")
    body = [("high", "++", "++", "−", "OFF"),
            ("middle", "+", "+", "−", "ON"),
            ("low", "−", "−", "++", "OFF")]
    xs = (TXT, TXT + 1.50, TXT + 2.60, TXT + 4.20, TXT + 5.30)
    d.shape(s, S.ROUNDED_RECTANGLE, TXT - 0.10, TOP + 0.04, 6.90, 0.46,
            fill=TEAL, line=None)
    for x, h in zip(xs, hdr):
        d.text(s, h, x, TOP + 0.12, 1.5, 0.32, role="body", font=HEAD,
               bold=True, color=WHITE)
    for r, row in enumerate(body):
        y = 2.42 + r * 0.60
        on = row[4] == "ON"
        if on:
            d.shape(s, S.ROUNDED_RECTANGLE, TXT - 0.10, y - 0.06, 6.90, 0.54,
                    fill=WASH, line=AMBER, lw=2)
        for x, cell in zip(xs, row):
            d.text(s, cell, x, y, 1.5, 0.34, role="body", font=HEAD,
                   bold=on, color=AMBER if on else INK)
    d.rows(s, [
        ("read the GFP column", "off, on, off — NON-MONOTONE in its input."),
        ("logic, not kinetics", "nothing here is a rate. No kinetics yet.",
         AMBER),
    ], top=4.46, bottom=6.30, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "Their own truth table, typeset large enough to read. Three "
            "rows, and the only thing to do is read the last column top to "
            "bottom: off, on, off.\n "
            "That is what non-monotone means. Session 10 ended with a "
            "saturation — more "
            "signal, no more output — and this is a different animal. Here "
            "more signal takes the output back DOWN.\n "
            "And I want it established before any rate appears. There is no "
            "kinetics on this slide. Four protein levels and one output, and "
            "the middle row is already the band.\n "
            "The four proteins are CI, the lambda repressor; LacI sub M1, a "
            "codon-modified LacI; wild-type LacI; and GFP. Which plasmid "
            "carries which is the next thing.")


def _s3_parts(d):
    """Which plasmid sets which edge, in the paper's own words.

    DESIGN sec 6 point 3: the high/low names are CORRECT and a later pass
    must not reverse them. p.1130, QUOTED: the high-detect component
    determines the AHL threshold above which GFP is muted; the low-detect
    component determines the lowest AHL that elicits a GFP response.
    """
    s = d.light()
    d.header(s, "stop 1", "frame  ·  two plasmids, two edges")
    d.title(s, "The names say which edge each half sets")
    d.rows(s, [
        ("pHD, high-detect",
         "luxR from P_{lux(L)} · lacI_{M1} from P_{lux(R)} · gfp from "
         "P_{lac}. It sets the AHL level ABOVE which GFP is muted — the "
         "band's UPPER edge.", TEAL),
        ("pLD, low-detect",
         "cI, a destabilized λ repressor, from P_{lux(R)} · wild-type lacI "
         "from λP_{(R-O12)}. It sets the LOWEST AHL that gives any GFP.",
         CYAN),
        ("the names are right",
         "high-detect, upper edge. Low-detect, lower edge. That is what the "
         "words suggest and what the paper says.", AMBER),
        ("and one free detail",
         "lacI_{M1} is codon-modified, and the paper says why: to stop it "
         "recombining with the wild-type lacI on the other plasmid. Session "
         "23's failure mode, designed around in 2005."),
    ], top=1.92, label_w=3.6, bottom=6.08)
    d.sources(s, [("which component sets which threshold",
                   "Basu et al., Nature 2005, p. 1130"),
                  ("the codon-modified lacI_{M1}",
                   "Basu et al., Nature 2005, p. 1133")], y=6.24)
    d.notes(s,
            "Two plasmids. The high-detect one carries the receptor, the "
            "mutant LacI and the reporter; the low-detect one carries CI and "
            "wild-type LacI.\n "
            "I say the edge assignment carefully because it has misled "
            "people. High-detect sets the upper edge — the level above which "
            "GFP goes out. Low-detect sets the lower edge — the lowest level "
            "that gets any GFP at all. Both are quoted from their page "
            "eleven-thirty. The names are not backwards.\n "
            "The last row is free and it is a nice one. They modified the "
            "codons of the mutant lacI specifically so it would not "
            "recombine with the wild-type copy on the other plasmid. That is "
            "the repeat-recombination failure mode from last session, "
            "designed around, twenty-one years ago.")


def _s3_close(d):
    s = d.light()
    d.header(s, "stop 1", "build  ·  close to the senders")
    d.title(s, "High AHL: the mutant LacI shuts the reporter")
    d.text(s, "AHL high  →  LuxR·AHL high  →  P_{lux(R)} on  →  "
              "LacI_{M1} HIGH  →  P_{lac} repressed  →  GFP off",
           M, 1.90, W - 2 * M, 0.82, role="emphasis", font=HEAD, bold=True,
           color=INK, spacing=1.15)
    d.rows(s, [
        ("what is on", "both CI and LacI_{M1}, because they share "
                       "P_{lux(R)} and both respond to LuxR·AHL."),
        ("what decides it", "LacI_{M1} is now high enough to repress "
                            "P_{lac}, so the reporter is off whatever else "
                            "is happening.", AMBER),
        ("the truth table row", "AHL ++, CI ++, LacI_{M1} ++, LacI −, "
                                "GFP −. It is the top row."),
    ], top=3.05, label_w=3.0, bottom=6.20)
    d.foot(s, "LuxR is a protein in every receiver: it binds AHL, and the "
              "LuxR·AHL pair switches a promoter. A REPRESSOR is a protein "
              "that sits on DNA at a promoter — the OPERATOR — and blocks "
              "production.")
    d.notes(s,
            "Case one, nearest the senders. Lots of signal, so lots of "
            "LuxR-AHL, so both genes behind that promoter are on.\n "
            "The one that matters is the mutant LacI, which is now high "
            "enough to shut the reporter promoter. GFP off.\n "
            "Note what is NOT happening: wild-type LacI is low here, "
            "because CI is high and CI represses it. So the reporter is dark "
            "even though one of its two repressors is absent. That is the "
            "thing to hold on to — there are two routes to dark.")


def _s3_far(d):
    s = d.light()
    d.header(s, "stop 1", "build  ·  far from the senders")
    d.title(s, "Low AHL: wild-type LacI shuts the reporter")
    d.text(s, "AHL low  →  no LuxR·AHL  →  no CI  →  λP_{(R-O12)} runs  →  "
              "wild-type LacI HIGH  →  GFP off",
           M, 1.90, W - 2 * M, 0.82, role="emphasis", font=HEAD, bold=True,
           color=INK, spacing=1.15)
    d.rows(s, [
        ("the enabling step", "CI is what represses λP_{(R-O12)}. With no "
                              "signal there is no CI, so that promoter runs "
                              "and wild-type LacI accumulates."),
        ("what decides it", "wild-type LacI represses P_{lac}. Different "
                            "repressor, different promoter, same dark "
                            "reporter.", AMBER),
        ("the truth table row", "AHL −, CI −, LacI_{M1} −, LacI ++, GFP −. "
                                "It is the bottom row."),
        ("so dark has two causes",
         "too much signal mutes GFP through LacI_{M1}; too little lets "
         "wild-type LacI mute it instead. The band is the gap between them."),
    ], top=3.00, label_w=3.0, bottom=6.26)
    d.notes(s,
            "Case two, far away. No signal, so no CI — and CI was the only "
            "thing holding wild-type LacI down. So wild-type LacI goes up "
            "and shuts the reporter.\n "
            "This is the half people find counterintuitive, because "
            "removing the input turns something ON. The low-detect plasmid "
            "is wired so that silence is a positive instruction.\n "
            "And now the shape is forced. Dark at the top because of one "
            "repressor, dark at the bottom because of a different one. "
            "Whatever happens in between is the band, and it exists because "
            "the two causes of dark do not overlap.")


def _s3_between(d):
    s = d.light()
    d.header(s, "stop 1", "build  ·  the window")
    d.title(s, "The window: neither repressor is doing its job")
    d.text(s, "AHL middle  →  CI present  →  wild-type LacI OFF, "
              "while LacI_{M1} is still too low to repress  →  GFP ON",
           M, 1.90, W - 2 * M, 0.82, role="emphasis", font=HEAD, bold=True,
           color=AMBER, spacing=1.15)
    d.rows(s, [
        ("CI arrives first", "enough signal to make CI, which shuts off "
                             "wild-type LacI."),
        ("LacI_{M1} lags", "the same signal is making it, but not yet to the "
                           "level that represses P_{lac}.", AMBER),
        ("so GFP is on", "both of its repressors are out of the way at once, "
                         "and only in this range of AHL."),
        ("the authors' reason",
         "the repression efficiency of CI is significantly higher than that "
         "of LacI_{M1}. One protein acts at a much lower concentration than "
         "the other."),
    ], top=3.00, label_w=3.5, bottom=6.08)
    d.sources(s, [("the repression efficiency of CI is significantly higher "
                   "than that of LacI_{M1}",
                   "Basu et al., Nature 2005, p. 1130")], y=6.24)
    d.notes(s,
            "Case three, and it is the result. At intermediate signal CI is "
            "already present and the mutant LacI is not yet effective, so "
            "both routes to dark are open at once and the reporter lights "
            "up.\n "
            "Their explanation is one sentence and I read it verbatim: the "
            "repression efficiency of CI is significantly higher than that "
            "of the mutant LacI. In plain terms, CI works at a much lower "
            "concentration.\n "
            "That asymmetry is the whole band. If both repressors worked at "
            "the same concentration the two dark regions would meet and "
            "there would be no window. In the model it is two numbers, and "
            "they go up once I have redrawn the circuit.")


def _s3_ffl(d):
    """Bar F1: session 10's feed-forward loop, REDRAWN here.

    The room met feed-forward loops fourteen sessions ago. Asking it to
    carry a topology that far is an assumption, not a reference, so both
    wirings are drawn side by side on this slide -- which also makes the
    comparison GRAPHICAL (bar C4) instead of a sentence claiming two things
    are alike.

    AND THE SLIDE DOES NOT CLAIM A NODE COUNT. It used to -- title and
    eyebrow both said "the same three nodes" -- while the right-hand column
    prints five species against the left's three. What actually transfers is
    the two-arms-in-opposition MOTIF, so that is what both now say (bar F7).

    Arrow chains rather than a box-and-arrow drawing: `TetR ⊣ LacI ⊣ EYFP`
    is this course's own notation for a topology (session 13 used it on
    three circuits) and it cannot land under the type floor, which a
    half-width reuse of session 10's own PNG would. Both chains are
    NUMBERS.md 5.3, written out there verbatim.
    """
    s = d.light()
    d.header(s, "segment 3", "build  ·  the same two fighting arms, twice")
    d.title(s, "The same two fighting arms, a band not a pulse")
    for x, (head, paths, mech, col) in zip(
            (M, 6.95),
            [("session 10  ·  the pulse generator",
              [("AHL  →  GFP", "direct"),
               ("AHL  →  CI  ⊣  GFP", "through a build-up")],
              "Two paths that FIGHT, one of them LATE: CI takes time to "
              "build up. An overshoot that adapts — a pulse in TIME.",
              TEAL),
             ("Basu 2005  ·  the band detector",
              [("AHL  →  CI  ⊣  LacI  ⊣  GFP", "two inversions: GFP on"),
               ("AHL  →  LacI_{M1}  ⊣  GFP", "one inversion: GFP off")],
              "Two paths that FIGHT, and neither is late. CI acts at a far "
              "lower concentration than LacI_{M1}. A window in the DOSE.",
              AMBER)]):
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.80, 5.68, 3.74, fill=WASH,
                line=col, lw=2)
        d.text(s, head, x + 0.26, 1.92, 5.16, 0.34, role="body", font=HEAD,
               bold=True, color=col)
        yy = 2.38
        for chain, why in paths:
            d.text(s, chain, x + 0.26, yy, 5.16, 0.36, role="body",
                   font=HEAD, bold=True, color=INK)
            d.text(s, why, x + 0.26, yy + 0.36, 5.16, 0.30, role="caption",
                   italic=True, color=MUTED)
            yy += 0.78
        d.text(s, mech, x + 0.26, 4.00, 5.16, 1.38, role="body", color=BODY,
               spacing=1.12)
    d.text(s, "Their own words: a feed-forward loop that begins with LuxR "
              "and culminates in GFP.",
           M, 5.68, W - 2 * M, 0.40, role="body", italic=True, color=MUTED)
    d.text(s, "The wiring transfers, the mechanism does not: a kinetic "
              "delay producing a transient against a non-monotone "
              "STEADY-STATE dose response.",
           M, 6.14, W - 2 * M, 0.70, role="body", bold=True, color=INK,
           spacing=1.12)
    d.notes(s,
            "I draw session 10's circuit again rather than ask anyone to "
            "remember it, because that was fourteen sessions ago.\n "
            "Left is the pulse generator — the same laboratory, and they "
            "read it in session 10. Two routes from the signal to the "
            "reporter, one direct and one through CI, and they pull against "
            "each other. The reason it pulses is that CI takes time to build "
            "up, so for a while the fast route is unopposed.\n "
            "Right is today's circuit, and the wiring is the same shape. Two "
            "routes from the signal to the reporter, pulling against each "
            "other. But nothing is late here. Both routes respond to the "
            "same signal at the same time.\n "
            "So what makes this one non-monotone is not a delay, it is that "
            "the two repressors work at wildly different concentrations. "
            "Same topology, different reason, different kind of answer — a "
            "pulse in time against a window in dose. If anyone says the ring "
            "is the pulse drawn in space, this is the slide that says no.")


def _s3_betas(d):
    """beta_L and beta_C, defined where they first appear and before the
    figure that prints them. And the failure boundary with them (bar F4):
    the hundredfold is BD2's VALUE, not a requirement -- the same paper
    forms rings at 28.6 and at 3.3.

    Page references are inline rather than in a sources() block: five rows
    plus the lumping sentence fill the band, and sources() placed under them
    runs off the bottom of the slide.
    """
    s = d.light()
    d.header(s, "stop 1", "build  ·  the asymmetry, as two numbers")
    d.title(s, "The asymmetry is two numbers, not two proteins")
    d.rows(s, [
        ("β_{L}", "the repression coefficient of LacI on GFP — the LacI "
                  "concentration at which GFP is half shut off. Printed "
                  "0.8 µM (p. 1134).", TEAL),
        ("β_{C}", "the repression coefficient of CI on LacI, same meaning. "
                  "Printed 0.008 µM.", CYAN),
        ("the ratio", "β_{L}/β_{C} = 100 on the printed BD2 set. CI acts at "
                      "a hundredth of the concentration LacI needs.", AMBER),
        ("what matters", "β_{C} much smaller than β_{L}. That INEQUALITY is "
                         "what makes the response non-monotone.", AMBER),
        ("not a rule", "their own Figs. 4b and 4c form rings at ratios of "
                       "28.6 and 3.3. A hundred is one parameter set's "
                       "value.", RED),
    ], top=1.88, label_w=2.3, bottom=5.86)
    d.text(s, "The model has five species, so both LacIs are ONE variable "
              "with one β_{L}. It cannot say CI is the better repressor — "
              "only that β_{C} is much smaller than β_{L}.",
           M, 5.98, W - 2 * M, 0.70, role="body", color=BODY, spacing=1.12)
    d.notes(s,
            "Two symbols, both defined here, both printed in their "
            "parameter table. A repression coefficient is the concentration "
            "of the repressor at which the thing it represses is half shut "
            "off — so a SMALL beta means a STRONG repressor, which is the "
            "part people invert.\n "
            "Nought point eight micromolar for LacI on GFP, eight "
            "nanomolar for CI on LacI. A factor of a hundred, and that is "
            "the quantitative form of the sentence I just read out.\n "
            "Then the boundary, because a hundredfold number invites being "
            "treated as a requirement. It is not. Their own figures four b "
            "and four c have that ratio at twenty-eight and at three point "
            "three, and both of those form rings. What the band needs is the "
            "inequality, not the number.\n "
            "And the modeling honesty: there are five species in their "
            "model, so both LacIs are one variable. The model cannot "
            "represent two repressors with different strengths at all. It "
            "represents the asymmetry as two beta values, which is a "
            "different claim from the one the prose makes.")


def _s3_model(d):
    """G(A), written down. Added 14 November 2026.

    The gauntlet's sharpest finding: slides that ask the room to find where
    dG/dA = 0 and to root-find both edges, on a function the deck never
    wrote. The only receiver model in the hour was the generic Hill on
    _s1_model, which is MONOTONE and cannot make this curve -- and no slide
    said those were different objects. T65 is autograded on PS9.

    These are Basu's own eqs (1)-(4) at steady state (NUMBERS sec 7.1).
    Equation (5), the lattice AHL term, is dropped: that IS the liquid-phase
    limit _s3_band already names.
    """
    d.derivation(
        None, "stop 1", "build  ·  the response, written down",
        "The band detector, as one function of AHL",
        [
            ("AHL makes the complex",
             "R = ρ_{R} [LuxR]² A² / γ_{R}",
             "eq. (4) at steady state. R rises as A SQUARED"),
            ("the complex drives two genes",
             "f(R) = R / (θ_{R} + R)",
             "eqs. (2) and (3) both use it"),
            ("LacI falls and rises",
             "γ_{L} L = α_{L1}/(1 + (C/β_{C})²)  +  α_{L2} f(R)",
             "eq. (2), with γ_{C}C = α_{C}f(R). One term falls, one rises"),
            ("GFP is what LacI leaves",
             "G(A) = α_{G} / [ γ_{G} (1 + (L/β_{L})²) ]",
             "eq. (1). G falls monotonically in L"),
        ],
        closing="L has a minimum, so G has a maximum. That is the band.",
        note="This is the function the next four slides differentiate, so "
             "I write it rather than point at a curve.\n "
             "Four lines, and each is one of their equations with the time "
             "derivative set to zero. AHL squared makes the complex. The "
             "complex drives CI and the mutant LacI off the same "
             "activation.\n "
             "The third line is the whole mechanism in symbols. Lumped "
             "LacI is a sum of two terms: one that CI shuts down as signal "
             "rises, and one that the signal itself turns up. A falling "
             "term plus a rising term has a minimum.\n "
             "And GFP only ever falls in LacI. So the hump in the output "
             "is not a property of the reporter — it is the dip in LacI, "
             "read upside down.\n "
             "One honesty note: their five-species model lumps wild-type "
             "LacI and the mutant into one L with one β_{L}. The two "
             "routes are in the two production terms, not in two "
             "proteins.")


def _s3_edges(d):
    """T65, autograded on PS9, and solved rather than read off a plot."""
    d.derivation_fig(
        "stop 1", "build  ·  the two edges, solved",
        "Where the window starts and stops",
        [
            ("the response we have",
             "G(A): GFP out, AHL in",
             "not monotone — dark at both ends"),
            ("find the peak",
             "A_{peak} where dG/dA = 0",
             "one interior maximum, not a plateau"),
            ("an edge needs a definition",
             "G(A) = ½ G_{peak}",
             "Basu's own criterion: half the maximum"),
            ("solve for both roots",
             "A_{lo} and A_{hi}",
             "rooted in log A, not read off the plot"),
        ],
        [FIG + "s24_band_step_1.png", None,
         FIG + "s24_band_step_2.png", FIG + "s24_band_step_3.png"],
        closing="On the printed BD2 set: 2.61 and 6.93 nM, 2.65× apart.",
        note="This is the technique PS9 autogrades, so I do it properly "
             "rather than pointing at a curve.\n "
             "G is the GFP output and A is the AHL input. The peak first — "
             "there is exactly one interior maximum, and a coarse grid will "
             "straddle it and tell you the response is still rising, which "
             "is a mistake worth mentioning because the autograder will "
             "catch it.\n "
             "Then an edge needs a definition, and we take the paper's own: "
             "half of the maximum steady-state fluorescence is how Basu "
             "locate a ring. So the edges are where the response crosses "
             "half its own peak.\n "
             "And then it is a root-find in log A, twice, on the printed "
             "parameters. Two point six one and six point nine three "
             "nanomolar, a factor of two point six five apart. Those are "
             "properties of the printed parameter set in the liquid-phase "
             "limit the paper itself defines — not of the measured strains, "
             "and not read off anybody's panel.")


def _s3_band(d):
    """The solved response, with the limit it was solved in on the slide.

    Bar F4 -- a result carries its failure boundary where it is stated. The
    liquid-phase limit is the paper's OWN limit (they define it by dropping
    equation 5), and the observable that tells you you have left it is on
    this slide rather than waiting for the closing ledger.
    """
    s = d.light()
    d.header(s, "stop 1", "build  ·  the response, from their parameters")
    d.title(s, "Both edges solved from the printed parameters")
    d.image_centered(s, FIG + "s24_band_response.png", top=1.70, band=4.40)
    d.foot(s, "The edges are solved in the LIQUID-PHASE limit, which the "
              "paper defines by dropping its own equation (5). You have left "
              "it when the answer becomes a position rather than a dose.")
    d.notes(s,
            "That is the curve, from their printed parameters, with the "
            "peak and both half-maximum edges on it. The band is narrow — a "
            "factor of two and a half between the two edges.\n "
            "What I want on this slide along with the result is the limit it "
            "holds in, because this is a spatial paper and we have just "
            "solved a non-spatial problem. Dropping equation five is the "
            "paper's own move for its liquid-phase simulations: AHL stops "
            "being a field with a position and becomes a dose you impose.\n "
            "And the test for whether you are still in that limit is "
            "something you can see down a microscope. If the fluorescence "
            "depends on where you look, there is no single AHL in the "
            "culture, and then these two numbers are not a dose window — "
            "they are the two radii of a ring.")


def _s3_inverter(d):
    s = d.light()
    d.header(s, "segment 3", "build  ·  one half of the circuit, alone")
    d.title(s, "A high-detect strain on its own runs backwards")
    _crop(d, s, "basu2005_fig2b",
          "Basu et al., Nature 2005, Fig. 2b — MEASURED",
          "Three high-detect strains.", h=3.95)
    d.rows(s, [
        ("what the panel shows", "all three high-detect strains run "
                                 "INVERSELY with AHL: bright at low signal, "
                                 "dark at high.", AMBER),
        ("so it is an inverter", "on its own this half is not a detector of "
                                 "anything high — it goes out when the "
                                 "signal arrives."),
        ("and that makes the band", "two inverted responses overlapped: one "
                                    "off going up, one off going down. "
                                    "Neither half is a band."),
        ("the names are not the trick", "high-detect really does set the "
                                        "upper edge. The surprise is the "
                                        "inverting."),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "This is the panel that catches people, and it is measured "
            "rather than simulated.\n "
            "Every one of the three high-detect strains goes DOWN as you add "
            "AHL. So the thing called high-detect is, on its own, an "
            "inverter. It is bright in the dark and dark in the light.\n "
            "Which is how the band is made. Overlap a response that goes out "
            "as the signal rises with one that goes out as the signal falls, "
            "and the only place anything is lit is between them.\n "
            "I say explicitly that the names are not the trick. High-detect "
            "sets the high edge. The counterintuitive part is the inverting, "
            "not the labeling.")


def _s3_variants(d):
    """The knob DESIGN sec 4's ledger rests on: a detection threshold is set.

    Our three curves stand in for their Fig. 2c, which is their SIMULATION
    of the same printed model -- so the slide loses nothing and is exact
    where a crop would be approximate.
    """
    s = d.light()
    d.header(s, "stop 1", "build  ·  three strains, three thresholds")
    d.title(s, "A detection threshold is something you set")
    d.image_centered(s, FIG + "s24_band_variants.png", top=1.70, band=4.40)
    d.text(s, "AHL enters the model only as ρ_{R}[LuxR]²A², so ten times "
              "ρ_{R} is exactly √10 lower IN AHL — the curve slides sideways "
              "and nothing else changes.",
           M, 5.98, W - 2 * M, 0.42, role="body", bold=True, color=INK)
    d.foot(s, "BD1 is BD2 with the LuxR dimerization constant ρ_{R} ten "
              "times higher — their LuxR-G2F mutant. BD3 halves the copy "
              "number, and with it [LuxR] and the GFP and LacI_{M1} "
              "synthesis rates α_{G}, α_{L2}.")
    d.notes(s,
            "Three curves from their printed parameters, and these are "
            "exact: the module is their model, so our three curves are what "
            "their own simulated panel draws.\n "
            "The point is that they did not take one band and describe it. "
            "They built three receivers that band in three different places "
            "and the model says exactly what they changed.\n "
            "BD1 is a point mutation in the receptor, represented as a "
            "tenfold dimerization constant. AHL only ever enters the model "
            "as rho times LuxR squared times A squared, so raising rho "
            "tenfold is identical to lowering the AHL axis by root ten — the "
            "curve slides sideways and nothing else happens. The tests pin "
            "that to nine digits and it is the cleanest check in the file.\n "
            "BD3 is a copy number, and it is messier, because halving the "
            "copy number halves three different parameters. So BD3's band "
            "moves AND gets wider. Two routes to the same knob, with "
            "different side effects.\n "
            "So: a receiver's detection threshold is set by a point mutation "
            "in a receptor, or by a plasmid copy number. That is a design "
            "knob with a mechanism behind it.")


def _s3_measured(d):
    s = d.light()
    d.header(s, "segment 3", "build  ·  and the strains agree")
    d.title(s, "The order and the spread survive in the data")
    _crop(d, s, "basu2005_fig2d",
          "Basu et al., Nature 2005, Fig. 2d — MEASURED",
          "The same three, measured.", h=3.95)
    d.rows(s, [
        ("what this slide claims",
         "the ORDERING — BD1 lowest, then BD2, then BD3 — and the SPREAD, "
         "about 0.85 decades computed against roughly a decade measured.",
         AMBER),
        ("what it does not claim",
         "any absolute AHL position off this panel. Every number here comes "
         "from their printed parameters through code the tests pin."),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "Their measured triple, next to what the printed model gave for "
            "the same three strains. Same order, and about the same "
            "total spread — a little under a decade computed, roughly a "
            "decade measured.\n "
            "That is the claim and I keep it to that. The ordering and the "
            "spread are what this comparison supports.\n "
            "I do not read an absolute AHL number off this panel and neither "
            "should anyone else. Every number I have given this hour comes "
            "from their printed parameter set through our own code, which is "
            "pinned by tests, and that is a different and better kind of "
            "number than a position measured off a published axis.")


def _s3_bullseyes(d):
    """Both panels on one slide, which is the only way the 36 % is visible.

    NUMBERS.md 23.5: these two crops are 220 ppi embedded raster and must
    not be scaled past about half a slide. At 3.0 in they are well inside
    that, and the two citations stay narrow enough that theme does not
    widen them to 4.6 in -- which, with two crops side by side, would make
    the two citation boxes overlap each other.

    Two plain lines rather than a rows() stack: a two-row stack costs
    0.46 in of pad and gap before any text, and there is 1.37 in under the
    captions.
    """
    s = d.light()
    d.header(s, "segment 3", "build  ·  the same circuit, on a plate")
    d.title(s, "The most sensitive strain makes the OUTER ring")
    _crop(d, s, "basu2005_fig3b", "Basu et al., Nature 2005, Fig. 3b",
          "Lawn BD2-Red + BD3.", x=3.45, h=3.00)
    _crop(d, s, "basu2005_fig3c", "Basu et al., Nature 2005, Fig. 3c",
          "Lawn BD1 + BD2-Red.", x=6.95, h=3.00)
    d.text(s, "AHL is highest AT the sender, so the strain needing least "
              "is satisfied farthest out.",
           M, 5.92, W - 2 * M, 0.40, role="body", bold=True, color=AMBER)
    d.text(s, "BD2-Red: 30 mm once, 22 mm another — 36 %, and every cause "
              "they offer is the plate.",
           M, 6.34, W - 2 * M, 0.40, role="body", bold=True, color=RED)
    d.foot(s, "3b: inner green ring BD3, outer red BD2-Red. 3c: inner red "
              "BD2-Red, outer green BD1.")
    d.notes(s,
            "Two plates, each with a mixed lawn of two band detectors and a "
            "disk of senders in the middle. Each strain lights up in a ring "
            "at its own radius.\n "
            "The inversion is worth ten seconds of thought out loud. The "
            "signal is strongest at the disk. A strain that needs very "
            "little signal is therefore satisfied a long way out, where "
            "everybody else has gone dark. So the most sensitive strain "
            "makes the OUTERMOST ring, which is the opposite of what the "
            "word sensitive makes people expect. In 3b the inner green ring "
            "is BD3 and the outer red one is BD2-Red; in 3c the inner red "
            "one is BD2-Red and the outer green one is BD1.\n "
            "And then the number I want them to leave with. The same strain, "
            "with the same threshold, made a thirty millimetre ring on one "
            "plate and a twenty-two millimetre ring on another. Thirty-six "
            "percent. Every explanation the authors offer is something about "
            "the plate rather than something about the circuit — growth "
            "rates, population densities, nutrients, agar. If your readout "
            "is a position, the environment is a circuit parameter whether "
            "you like it or not.")


def _s3_senders(d):
    s = d.light()
    d.header(s, "segment 3", "build  ·  the lawn stays the same")
    d.title(s, "The senders are the program")
    for key, x, cap in (("basu2005_fig5b", 2.74, "two disks — ellipse"),
                        ("basu2005_fig5c", 5.58, "three — heart"),
                        ("basu2005_fig5d", 8.39, "four — clover")):
        _crop(d, s, key, "Basu et al., Nature 2005, Fig. 5", cap, x=x,
              h=2.40)
    d.text(s, "The knobs: the NUMBER of sender disks, their DISTANCE "
              "apart, and their DENSITY.",
           M, 5.76, W - 2 * M, 0.40, role="body", bold=True, color=AMBER)
    d.text(s, "Nothing genetic changes. Fig. 5 is four panels and three "
              "experiments — panel a is their SIMULATION, so it is not here.",
           M, 6.24, W - 2 * M, 0.40, role="body", bold=True, color=INK)
    d.notes(s,
            "Same lawn, same genetics, three different patterns, and the "
            "only thing that changed is where the senders were put.\n "
            "That is as cheap a demonstration as this field has of a "
            "pattern living in the boundary conditions rather than in the "
            "DNA. Two disks give an ellipse, three give a heart, four give a "
            "clover, and the receivers never knew.\n "
            "The knobs are a pipette: how many disks, how far apart, and how "
            "concentrated. Density is the one people drop, and it is in both "
            "their caption and their text, so it belongs in the ledger with "
            "the other two.\n "
            "And the counting point, which is about reading figures. Panel a "
            "of that figure is a simulation of the ellipse. If I put all "
            "four up here, this slide would be showing one simulation among "
            "three experiments with nothing saying so. Three results.")


def _s3_regression(d):
    """Bar F5: the measurement comes before the statistic.

    Every quantity is defined in words and the comparison is named BEFORE
    any R^2 appears -- which is the whole point, because what the comparison
    turns out to be is the lesson.
    """
    s = d.light()
    d.header(s, "segment 3", "build  ·  a sentence in a Nature abstract")
    d.title(s, "Which kinetic parameters affect ring development")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.80, W - 2 * M, 0.80, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "“Experimental and theoretical analyses reveal which kinetic "
              "parameters most significantly affect ring development over "
              "time.”    — their abstract",
           M + 0.30, 1.94, W - 2 * M - 0.60, 0.56, role="body", italic=True,
           color=INK, spacing=1.12)
    d.rows(s, [
        ("what was regressed",
         "2,000 random parameter sets around BD2; the first 100 that banded "
         "were run as SIMULATIONS, and each rate constant regressed against "
         "its own simulated timings."),
        ("the quantities, in words",
         "γ_{L} is the LacI decay rate, a model INPUT. SHIFT BEGIN is when "
         "and where the ring first passes half its final maximum."),
        ("then the numbers",
         "γ_{L} against shift begin: R² = 0.91. CI repression efficiency "
         "against shift: R² = 0.05, which they call weak. Everything else "
         "below 0.001."),
        ("so — what was measured?",
         "one BD2 time course, compared by eye.", AMBER),
    ], top=2.80, label_w=4.0, bottom=6.50)
    d.notes(s,
            "I read their sentence out, then take it apart in the order "
            "that makes it answerable: what was compared with what, then "
            "what the quantities are, then the numbers.\n "
            "The design is a hundred simulations drawn from two thousand "
            "random parameter sets, with each simulation's own input "
            "regressed against its own output. No experiment enters the "
            "regression at any point. The experimental contribution to that "
            "sentence is a single BD2 time course compared to a single "
            "simulation by eye — their words are accounts for the "
            "similarity.\n "
            "So the answer to what was measured is: nothing in the "
            "regression. And the R squared of nought point nine one is "
            "real, it is just a statement about their model, not about their "
            "circuit.\n "
            "I take answers before I say that. Somebody usually spots it "
            "from the phrase random parameter sets.\n "
            "And the nought point oh five is worth a sentence of its own. "
            "Five percent of the variance over a hundred points, with a P "
            "value of nought point oh one nine that only says five percent "
            "is unlikely to be exactly zero. They call it weak and they are "
            "right. It is not a design lever.")


def _s3_release(d):
    s = d.light()
    d.header(s, "stop 1", "pose  ·  on your own paper  ·  vote, then argue")
    d.title(s, "Your turn: build the band out of activators")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.84, W - 2 * M, 1.90, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "Basu's band is two repression routes of opposite parity. "
              "Replace both repressors with ACTIVATORS.",
           M + 0.32, 1.98, W - 2 * M - 0.64, 0.80, role="emphasis",
           color=INK, spacing=1.12)
    d.text(s, "The signal activates X, which activates GFP. The signal also "
              "activates Y, which activates GFP. Nothing represses anything, "
              "and every arm is monotone.",
           M + 0.32, 2.90, W - 2 * M - 0.64, 0.76, role="body", color=BODY,
           spacing=1.12)
    d.rows(s, [
        ("a", "can this circuit band? Argue it from the signs, not from a "
              "simulation.", AMBER),
        ("b", "if your answer is no — what is the smallest change that "
              "would let two activators band?", AMBER),
    ], top=3.96, label_w=0.5, bottom=5.40)
    d.text(s, "Part a has a one-line answer and the line is about "
              "derivatives.",
           M, 5.68, W - 2 * M, 0.44, role="body", bold=True, color=TEAL)
    d.notes(s,
            "A different object from the one we built, and it is answerable "
            "without any arithmetic, which is why I want it argued from "
            "signs.\n "
            "Part a: no. If the output rises with X, rises with Y, and both "
            "X and Y rise with the signal, then the output's derivative with "
            "respect to the signal is a sum of positive terms and cannot "
            "change sign. A band needs that derivative to change sign.\n "
            "Part b: make the two arms interact. One activator has to be "
            "able to UNDO the other's effect — competing for the same "
            "operator, or sequestering the first activator — so that the "
            "second arm's contribution is effectively negative at high "
            "signal.\n "
            "I point out that they have already seen the biology for part b "
            "today: Karig measured one signal competitively binding the "
            "other's receptor. Competitive binding at one site is exactly "
            "the mechanism that turns a second activator into an opponent.")


def _s3_debrief(d):
    s = d.light()
    d.header(s, "stop 1", "debrief  ·  the answer, from the signs")
    d.title(s, "A band needs one arm to oppose the other")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.82, W - 2 * M, 1.44, fill=WASH,
            line=AMBER, lw=2)
    d.text(s, "If  ∂G/∂X > 0,  ∂G/∂Y > 0,  dX/dA > 0  and  dY/dA > 0,  then "
              "dG/dA > 0 everywhere.",
           M + 0.32, 1.94, W - 2 * M - 0.64, 0.82, role="emphasis",
           font=HEAD, bold=True, color=INK)
    d.text(s, "A sum of positive terms cannot change sign. Part a is no.",
           M + 0.32, 2.84, W - 2 * M - 0.64, 0.40, role="body", color=BODY)
    d.rows(s, [
        ("what a band requires",
         "dG/dA has to CHANGE SIGN. Two monotone arms of the same parity "
         "cannot do that, whatever the thresholds."),
        ("the smallest change",
         "the two arms must stop being independent — an activator that "
         "COMPETES for the same operator.", AMBER),
        ("you will see it today",
         "the next stop’s paper measures 3OC12HSL competitively binding "
         "RhlR, the C4HSL receptor — the mechanism."),
        ("why repression is easier",
         "it gives the opposing sign free. They only had to separate the "
         "two thresholds."),
    ], top=3.32, label_w=4.3, bottom=6.40)
    d.notes(s,
            "The answer is one line of calculus and I want it said as one "
            "line. Positive times positive plus positive times positive is "
            "positive. The derivative cannot turn over, so the response "
            "cannot come back down.\n "
            "That reframes what the band detector is. It is not a circuit "
            "with two thresholds — it is a circuit with two OPPOSING arms "
            "whose thresholds happen to be separated. Opposing comes first.\n "
            "For part b the honest answer is that two activators can band if "
            "they are not independent. Competition at a shared operator "
            "does it, because displacing a strong activator with a weak one "
            "lowers the output. Sequestration does it too.\n "
            "And then the callback, which is theirs rather than mine: Karig "
            "measured exactly that competition between the same two signals "
            "we read the diffusion coefficients off. The mechanism part b "
            "needs is in one of today's papers.")


# ======================================== MOVE 4 · two populations =========
def _s4_frame(d):
    """FRAME on Box 1A -- and it is BOX 1A, not Figure 1.

    NUMBERS.md 23.3: the paper numbers Figures 1-3 separately and does have
    a Figure 1 (the liquid-culture growth controls). Calling the circuit
    schematic "Fig. 1" would name the wrong object.
    """
    s = d.light()
    d.header(s, "segment 4", "frame  ·  the object, from the paper you read")
    d.title(s, "Each strain holds the other's life in its hands")
    _crop(d, s, "balagadde2008_box1a",
          "Balagaddé et al., Mol Syst Biol 4:187 (2008), Box 1A",
          "Two cells, two signals, a toxin and an antidote. Their Figure 1 "
          "is a different thing — the liquid-culture controls.", h=2.70)
    d.rows(s, [
        ("the predator", "makes its toxin only with IPTG, then dies of it "
                         "unless the prey's signal switches on its "
                         "antidote."),
        ("the prey", "grows fine alone, and is killed by the predator's "
                     "signal. It has no antidote."),
        ("IPTG is the knob", "a small molecule you add to the medium: it "
                             "induces the predator's toxin and the prey's "
                             "synthase.", AMBER),
        ("this is the release you did",
         "the antidote receiver is this cell. CcdB is the toxin, CcdA the "
         "antidote.", AMBER),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.assigned_on(TXT, 6.46, 7.0, s, prefix="You read this for today",
                  key="balagadde2008")
    d.notes(s,
            "Two engineered strains in one reactor, and each one controls "
            "whether the other lives.\n "
            "The predator is the interesting cell, and the detail that "
            "matters is WHEN it makes its poison. The toxin gene sits under "
            "an IPTG-inducible promoter, so with IPTG in the medium the "
            "predator is dying and the prey's signal is the only thing "
            "keeping it alive. With no IPTG it survives perfectly well "
            "alone, which is exactly what their four uninduced reactors "
            "show. What IS constitutive in this cell is the luxR-lasI "
            "operon, not the toxin.\n "
            "The prey is simpler: it grows, and the predator's signal kills "
            "it. No antidote on that side.\n "
            "IPTG gets one sentence here because the next twenty slides run "
            "on it. It is a small molecule we add to the medium; it induces "
            "the predator's toxin gene and the prey's synthase, and those "
            "are the only two things in the circuit it touches.\n "
            "I point out that they wrote this circuit already. The antidote "
            "receiver from the first part of the hour is the predator, and "
            "now it has names on it — CcdB the toxin, CcdA the antidote. "
            "One difference worth naming: the toxin you were given was "
            "constitutive, and theirs is induced.\n "
            "One citation point: this is Box 1A. The paper has a real Figure "
            "1 and it is something else.")


def _s4_arms(d):
    s = d.light()
    d.header(s, "segment 4", "frame  ·  the two arms, traced")
    d.title(s, "Both arms end on the same promoter")
    for x, (head, chain, who, col) in zip(
            (M, 6.95),
            [("prey → predator  ·  RESCUE",
              "LuxI  →  3OC6HSL  →  LuxR  →  P_{luxI}  →  CcdA  →  "
              "CcdB neutralised",
              "The predator lives.", GREEN),
             ("predator → prey  ·  KILLING",
              "LasI  →  3OC12HSL  →  LasR  →  P_{luxI}  →  CcdB",
              "The prey dies.", RED)]):
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.82, 5.68, 2.04, fill=WASH,
                line=col, lw=2)
        d.text(s, head, x + 0.26, 1.92, 5.16, 0.34, role="body", font=HEAD,
               bold=True, color=col)
        d.text(s, chain, x + 0.26, 2.34, 5.16, 1.00, role="body", font=HEAD,
               bold=True, color=INK, spacing=1.18)
        d.text(s, who, x + 0.26, 3.44, 5.16, 0.34, role="body", italic=True,
               color=col)
    d.rows(s, [
        ("one promoter, used twice",
         "active LuxR and active LasR both initiate at P_{luxI}. Two cells, "
         "opposite outcomes.", AMBER),
        ("and the orthogonality leaks",
         "their Fig. 1 controls show the prey retarded by IPTG alone, and "
         "they settle nothing."),
    ], top=4.02, bottom=6.08, side=False, pad=0.04)
    d.sources(s, [("both LuxR and LasR initiate at P_{luxI}",
                   "Balagaddé et al., Mol Syst Biol 2008, p. 3"),
                  ("the crosstalk admission",
                   "Balagaddé et al., Mol Syst Biol 2008, Fig. 1")], y=6.24)
    d.notes(s,
            "Each arm in one line, and I trace them out loud.\n "
            "The prey's synthase makes 3OC6HSL. It leaves the prey, crosses "
            "to the predator, binds LuxR, and the complex fires the "
            "promoter that makes the antidote. The predator survives.\n "
            "The predator's synthase makes 3OC12HSL. It crosses to the prey, "
            "binds LasR, and fires the SAME promoter — which in that cell is "
            "wired to the toxin. The prey dies.\n "
            "That is a lovely piece of part reuse and it is also the "
            "orthogonality problem. Both receptors initiate at P-lux-I, so "
            "the specificity is entirely in which gene is downstream in "
            "which cell.\n "
            "And they are honest that it leaks. In their liquid-culture "
            "controls the prey is slowed by IPTG alone, and one of the two "
            "explanations they offer is basal toxin from the prey's own "
            "signal hitting LasR. They settle neither.")


def _s4_build(d):
    """Run one of two: the four-state model, written from Box 1A.

    T64's construction half, and the STRUCTURE is the session's own work --
    the room writes it from the wiring diagram. The equations and every
    constant are the BioModels deposit's, which is a different provenance
    and the next slides say so.

    Two runs of four rather than one of eight, for the reason session 23
    recorded: eight steps in one derivation_fig column makes the stack drop
    its finished equations to fit, and the finished equations are the record
    a revising student reads.
    """
    d.derivation_fig(
        "segment 4", "build  ·  the model, from their wiring diagram",
        "Write it down: four states",
        [
            ("two populations, one capacity",
             "dC_{1}/dt = k_{c1}C_{1}(1 − T/C_{m}) − m_{1}C_{1}\n"
             "dC_{2}/dt = k_{c2}C_{2}(1 − T/C_{m}) − m_{2}C_{2}",
             "T = C_{1}+C_{2}; k_{c1}, k_{c2} the two growth rates; C_{m} "
             "the SHARED carrying capacity; m_{1}, m_{2} the death rates"),
            ("the OTHER's signal sets m_{1}",
             "m_{1} = D + d_{1}K_{1}/(K_{1} + A_{2}²)",
             "A_{2} is the prey's signal — it RESCUES. d_{1} is the "
             "IPTG-set toxin death rate, K_{1} the A_{2} that halves it"),
            ("and the prey has no antidote",
             "m_{2} = D + d_{2}A_{1}²/(K_{2} + A_{1}²)",
             "A_{1} is the predator's signal — it KILLS. d_{2} and K_{2} "
             "are the prey's pair of those same two constants"),
            ("the signals are states too",
             "dA_{1}/dt = k_{A1}C_{1} − (d_{AA1} + D)A_{1}\n"
             "dA_{2}/dt = k_{A2}C_{2} − (d_{AA2} + D)A_{2}",
             "k_{A1}, k_{A2} are made per cell; d_{AA1}, d_{AA2} are the "
             "abiotic decays; and both signals also leave with D"),
        ],
        [FIG + "s24_pp_step_1.png", None, None, None],
        closing="D appears four times: once per population, once per signal.",
        note="The structure is theirs and ours — they drew the wiring and we "
             "write the equations from it, which is exactly the "
             "model-construction technique PS9 and the final both ask for.\n "
             "The growth terms are logistic with ONE shared capacity, so "
             "both strains are assumed to be drawing on one pooled "
             "resource.\n "
             "The death terms are the circuit. The predator's death rate "
             "goes DOWN as the prey's signal rises — that is the antidote, "
             "and it is why K over K plus A squared rather than A squared "
             "over K plus A squared. The prey's goes UP with the predator's "
             "signal. Opposite signs, and that is the whole ecology.\n "
             "Both populations go up in the first step, because the prey's "
             "line is the mirror image and costs nothing to read — same "
             "logistic term, same shared capacity, the other death rate. "
             "Every constant in the model is named in the asides as it "
             "arrives.\n "
             "Then the fourth move, which is the one that matters later: the "
             "signals get their own equations. Each is made in proportion to "
             "the population that makes it and removed by decay AND by "
             "washout.\n "
             "The closing line is worth pausing on. Writing the signals "
             "down doubled the number of places the dilution rate appears, "
             "from two to four. It leaves with each population and it leaves "
             "with each signal.")


def _s4_qssa_reminder(d):
    """Bar F1: session 4's QSSA, redrawn on the slide that uses it.

    And bar F3: the approximation carries its CONDITION here, because the
    condition is what the segment later goes back and checks. Session 4's
    own words are on the slide -- setting epsilon to zero is not setting a
    derivative to zero -- because that distinction is what makes the check
    checkable.

    U+21CC is in theme.MISSING_GLYPHS (it reached a session 21 slide and
    came out of the PDF as a question mark), so the equilibrium is written
    <=>. The equilibrium line is set at 32 pt, where a 5.0 in box holds 22
    characters, so it gets its own band rather than sharing one.
    """
    s = d.light()
    d.header(s, "segment 4", "build  ·  an approximation you already own")
    d.title(s, "An approximation you have used since session 4")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.78, W - 2 * M, 1.54, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "E + S  <=>  ES  →  E + P",
           M + 0.32, 1.90, 5.6, 0.54, size=32, font=HEAD, bold=True,
           color=INK)
    d.text(s, "[ES] changes slowly next to the big terms that make it, so "
              "ALGEBRA REPLACES ITS ODE:  [ES] = E_{tot}[S]/(K_{M}+[S]), and "
              "then v = V_{max}[S]/(K_{M}+[S]).",
           M + 0.32, 2.52, W - 2 * M - 0.64, 0.72, role="body", color=BODY,
           spacing=1.12)
    d.rows(s, [
        ("what session 4 insisted on",
         "setting ε = 0 is NOT setting a derivative to zero. It says the "
         "derivative is small next to the terms in its own equation."),
        ("and ε is a ratio of two clocks",
         "in session 4 it was γ_{p}/γ_{m} = 0.1 — the fast species relaxed "
         "ten times faster than the slow one. That is a condition you "
         "check.", AMBER),
        ("the fast species here",
         "small molecules against populations that grow over hours. So put "
         "A_{1} and A_{2} at quasi-steady state."),
    ], top=3.50, label_w=4.3, bottom=6.50)
    d.notes(s,
            "I put Michaelis-Menten back on the slide rather than say the "
            "word QSSA, because this room met it twenty sessions ago and the "
            "whole of the next five minutes turns on it.\n "
            "The move is: one species is fast, so its own equation stops "
            "being differential and becomes algebraic, and you substitute.\n "
            "Session 4 was careful about one thing and I repeat it. Setting "
            "epsilon to zero does not mean the fast species stops changing. "
            "It means its rate of change is small next to the individual "
            "terms in its own equation, each of which is large.\n "
            "And epsilon is a ratio of two clocks, which makes it checkable. "
            "In session 4 it was nought point one. Keep that in mind, "
            "because we are going to come back and check it, and the answer "
            "is going to be interesting.\n "
            "The reason anyone would reach for this here: the signals look "
            "fast. They are small molecules; the populations take hours. So "
            "eliminate them.")


def _s4_reduce(d):
    d.derivation_fig(
        "segment 4", "build  ·  eliminate the signals",
        "Put the signals at quasi-steady state",
        [
            ("balance synthesis against removal",
             "A_{1} = k_{A1}C_{1}/(d_{AA1} + D)",
             "the same form as a sender on a plate"),
            ("substitute, and it is 2×2",
             "dC_{1}/dt = k_{c1}C_{1}(1−T/C_{m}) − m_{1}(C_{2})C_{1}",
             "m_{1} now depends on C_{2} directly"),
        ],
        [FIG + "s24_pp_step_2.png", None],
        closing="Two states. Every interaction is now population to "
                "population.",
        note="Balancing what makes each signal against what removes it "
             "gives the signal as its maker's density over its own total "
             "removal — which is exactly "
             "the sender steady state we wrote in the first segment, with "
             "the population in place of the sender density. Same algebra, "
             "new letters.\n "
             "Substitute, and the two death rates become functions of the "
             "two populations directly. The signals are gone as variables "
             "and the community is two states in C one and C two.\n "
             "And that feels like progress. It is a two-dimensional system, "
             "they have nullclines, a Jacobian and eigenvalues, and all of "
             "that machinery is sitting ready. So let us use it.")


def _s4_jacobian(d):
    """The matrix, DRAWN. lecture-design 5e, on the session 14 rebuild: a
    four-slide run about a Jacobian never drew a matrix, in a segment whose
    exam item asks the student to write one.

    And then the two lines that collapse its diagonal, which is the whole
    shock of the move. Verified against posb.pp_jacobian. The trace line is
    32 pt and needs 8.0 in to stay on one line: at 6.2 in it wrapped onto
    the sentence under it.
    """
    s = d.light()
    d.header(s, "segment 4", "build  ·  the matrix, and then the trace")
    d.title(s, "The diagonal collapses at every interior point")
    d.text(s, "L ≡ 1 − T/C_{m},   the shared logistic factor",
           M, 1.74, 6.0, 0.36, role="body", italic=True, color=MUTED)
    # The matrix. Two thin rectangles stand in for the brackets: a drawn
    # bracket cannot go missing the way a bracket GLYPH can.
    d.text(s, "J  =", M, 2.46, 0.9, 0.44, size=32, font=HEAD, bold=True,
           color=INK)
    bx, by, bw, bh = M + 0.95, 2.16, 10.40, 1.42
    d.shape(s, S.RECTANGLE, bx, by, 0.045, bh, fill=INK, line=None)
    d.shape(s, S.RECTANGLE, bx + bw, by, 0.045, bh, fill=INK, line=None)
    cells = [("k_{c1}L − k_{c1}C_{1}/C_{m} − m_{1}",
              "−k_{c1}C_{1}/C_{m} − C_{1} ∂m_{1}/∂C_{2}"),
             ("−k_{c2}C_{2}/C_{m} − C_{2} ∂m_{2}/∂C_{1}",
              "k_{c2}L − k_{c2}C_{2}/C_{m} − m_{2}")]
    for r, row in enumerate(cells):
        for c, cell in enumerate(row):
            d.text(s, cell, bx + 0.25 + c * 4.80, by + 0.16 + r * 0.66,
                   4.70, 0.40, role="body", font=HEAD, bold=True, color=INK)
    d.rows(s, [
        ("the off-diagonal signs are the ecology",
         "∂m_{1}/∂C_{2} is NEGATIVE (rescue); ∂m_{2}/∂C_{1} is POSITIVE "
         "(killing)."),
        ("now use the fixed point",
         "each per-capita rate is zero there, so k_{c1}L = m_{1} and "
         "k_{c2}L = m_{2}.", AMBER),
    ], top=3.84, bottom=5.52, side=False, pad=0.04)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.62, W - 2 * M, 1.14, fill=WASH,
            line=RED, lw=2)
    d.text(s, "tr J  =  − (k_{c1}C_{1} + k_{c2}C_{2}) / C_{m}",
           M + 0.32, 5.72, 8.0, 0.54, size=32, font=HEAD, bold=True,
           color=RED)
    d.text(s, "Strictly NEGATIVE in this 2-STATE reduction: every interior "
              "point, any parameter.",
           M + 0.32, 6.30, W - 2 * M - 0.64, 0.40, role="body", color=INK)
    d.notes(s,
            "Here is the matrix, written out, because writing one is the "
            "thing they get asked to do.\n "
            "The off-diagonals carry the biology and I point at the signs. "
            "More prey means less predator death, so that entry is "
            "negative. More predator means more prey death, so that one is "
            "positive. Opposite signs off the diagonal is the signature of a "
            "predator-prey pair, and it is what makes the determinant "
            "positive and the eigenvalues complex.\n "
            "Then the move that does the damage. At an interior fixed point "
            "both per-capita rates are zero, which says k c one times L "
            "equals m one, and the same for the prey. Put those into the "
            "diagonal and the growth term cancels the death term in both "
            "entries.\n "
            "What is left is minus k c one C one plus k c two C two, over "
            "the carrying capacity. Every single quantity in that "
            "expression is positive. So the trace is negative — not usually, "
            "not at these parameters, but always.\n "
            "I say the qualifier every time, and it is on the slide: this is "
            "a claim about the TWO-STATE reduction. It is not a proof that a "
            "predator-prey community cannot oscillate, and anyone who "
            "copies it down without those three words has written down "
            "something false — which the next ten minutes then has to "
            "undo.")


def _s4_phase(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  the plane, and the eigenvalues")
    d.title(s, "The one coexistence state is a stable spiral")
    d.image_centered(s, FIG + "s24_pp_phase_plane.png", top=1.70, band=4.40)
    d.foot(s, LAMBDA_NOTE)
    d.notes(s,
            "Left is the plane they already know how to read: two "
            "nullclines, and where they cross is a fixed point. There is "
            "exactly one interior crossing.\n "
            "Right is why it is stable. Both eigenvalues have negative real "
            "part and a nonzero imaginary part, so the trajectory spirals "
            "in. That is what the trace just told us had to happen.\n "
            "I name these as eigenvalues out loud: it is session 11's "
            "notation and problem set five's.\n "
            "The held-fixed parameters are on the figure. An eigenvalue plot "
            "without them is a picture rather than evidence, because you "
            "cannot tell what was varied.")


def _s4_qss_fig(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  not at these parameters — at any")
    d.title(s, "A strictly negative trace rules out a Hopf")
    d.image_centered(s, FIG + "s24_qss_no_hopf.png", top=1.70, band=4.40)
    d.text(s, "The left panel's low cluster is a 2nd fixed point, at "
              "other parameters.",
           M, 6.14, W - 2 * M, 0.42, role="body", color=BODY)
    d.foot(s, "A 2×2 Hopf needs tr J = 0 with det J > 0. Strictly negative "
              "at every interior point and every parameter value — no Hopf "
              "anywhere; and on the left panel’s sweep, not close: "
              "−0.10/h at the nearest D.")
    d.notes(s,
            "I want the algebra backed by a picture, because a proof that "
            "something is impossible is the kind of claim people want to see "
            "tested.\n "
            "Left: the trace at the interior fixed point across every "
            "dilution rate that has one, with the closed form drawn "
            "underneath it. They lie on top of each other.\n "
            "Right: random parameter sets across IPTG, the dilution rate and "
            "seven rate constants. Every point on the diagonal, every point "
            "negative.\n "
            "One label on that panel needs a word, because it reads against "
            "the slide before this one. The low cluster is a SECOND "
            "interior fixed point. It turns up at other parameter values, "
            "the dilution rate among them; at the nought point one one two "
            "five we have been working at there is exactly the one crossing "
            "we just looked at.\n "
            "And the condition is worth stating properly. For a "
            "two-by-two, a Hopf needs the trace to pass through zero with a "
            "positive determinant. Strictly negative is a proof of absence, "
            "and that part holds at every interior point and every "
            "parameter value.\n "
            "How far from zero is a separate question, and the two panels "
            "answer it differently. On the left, at the deposit’s values, "
            "the closest the trace comes to zero across the whole dilution "
            "sweep is minus nought point one per hour — a sixth of that "
            "panel.\n "
            "The cloud on the right gets much closer — about minus nought "
            "point zero zero seven. If anyone asks, that is not a near "
            "Hopf. The trace goes to zero as an interior fixed point runs "
            "out of cells: at that one the predator sits at nought point "
            "six against a carrying capacity of four hundred and "
            "thirty-five. It is the populations in the numerator going to "
            "zero, not the parameters doing anything interesting.\n "
            "Which is why I state the proof and not the margin. It is "
            "strictly negative everywhere, and the size of the gap is not "
            "what the argument rests on.\n "
            "So the system we just built by a perfectly standard reduction "
            "cannot do the thing the paper's title is about. Something has "
            "gone wrong, and it is not the paper.")


def _s4_restore(d):
    """Step 8, and the diagnosis -- which is to go back and check the
    condition the QSSA slide put on the slide.

    THE ARITHMETIC IS DERIVED FROM THE DEPOSIT'S QUOTED CONSTANTS
    (NUMBERS.md 20.1): signal relaxation is dAA + D, so 0.017 + 0.1125 =
    0.1295 /h for the predator's signal against kc1 = 0.8 /h, a factor of
    6.2 the WRONG WAY; and 0.11 + 0.1125 = 0.2225 against kc2 = 0.4, a
    factor of 1.8 the wrong way. Re-run on 8 November against pp_params().

    And bar F1 again: session 11's Hopf is redrawn here, as the ring of
    three and the sweep they were graded on, because this slide leans on it.
    """
    s = d.light()
    d.header(s, "segment 4", "build  ·  check the condition you assumed")
    d.title(s, "The signals were never the fast variables")
    d.rows(s, [
        ("the condition, checked",
         "d_{AA1} + D = 0.017 + 0.1125 = 0.13/h against k_{c1} = 0.8/h, so "
         "ε = 0.8/0.13 = 6.2.", RED),
        ("and the other one too",
         "the prey's: 0.11 + 0.1125 = 0.22/h against k_{c2} = 0.4/h, so "
         "ε = 0.4/0.22 = 1.8.", RED),
        ("never licensed",
         "ε = k_{c}/(d_{AA}+D) had to be << 1 — session 4's was 0.1. These "
         "are 6.2 and 1.8.", AMBER),
        ("put them back",
         "a population's signal LAGS its maker, and a delay around a loop is "
         "what oscillates.", AMBER),
    ], top=1.86, label_w=3.4, bottom=5.74)
    d.shape(s, S.ROUNDED_RECTANGLE, M, 5.86, W - 2 * M, 1.22, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "Session 11: X ⊣ Y ⊣ Z ⊣ X, swept α for the crossing — "
              "posb.hopf_boundary, PS5.",
           M + 0.30, 6.00, W - 2 * M - 0.60, 0.36, role="body", color=INK)
    d.text(s, "Here it is a ring of FOUR: predator, signal, prey, signal.",
           M + 0.30, 6.48, W - 2 * M - 0.60, 0.36, role="body", bold=True,
           color=TEAL)
    d.notes(s,
            "This is the slide the dead end was for, and the diagnosis is "
            "one division.\n "
            "Go back and check epsilon, and I write the ratio the same way "
            "up as session 4 did: the SLOW rate over the rate of the "
            "species we eliminated. In session 4 that was gamma-p over "
            "gamma-m, nought point nought five over nought point five, "
            "equals nought point one.\n "
            "Here the predator's signal is removed at its decay rate plus "
            "the dilution rate — nought point zero one seven plus nought "
            "point one one two five, about nought point one three per hour. "
            "The predator grows at nought point eight. So epsilon is nought "
            "point eight over nought point one three, which is six point "
            "two: the signal is six times SLOWER than the thing it was "
            "supposed to be fast compared to.\n "
            "Same for the prey's signal, one point eight. Both the wrong "
            "way, and both bigger than one when the whole move needed them "
            "much smaller.\n "
            "So the reduction was algebra done correctly on a premise that "
            "is false. Nothing we derived is wrong; it is a statement about "
            "a different system.\n "
            "And naming what we threw away tells us what the oscillation "
            "is. A population's signal lags the population. Put the signals "
            "back and the loop is longer — predator, its signal, prey, its "
            "signal, back to the predator. A ring of four.\n "
            "They have done this already. Session 11 was a ring of three "
            "repressors, they swept alpha, they watched the leading real "
            "part cross zero, and they wrote that sweep themselves on "
            "problem set five. Same machinery. What is new is that this time "
            "the algebra told us in advance that the two-state version could "
            "not do it.")


def _s4_putback(d):
    """Step 8: restore the two equations the QSSA deleted.

    This run exists because `s24_pp_step_3` was built and placed nowhere --
    figure_fit reported it as the deck's only unreadable placement, and the
    figures module's own docstring says stage 3 is the LAG. A stage drawn
    for a derivation and never shown is a build artifact, so it gets the
    step it was drawn for.

    THE TWO LAG TIMES ARE DERIVED FROM THE DEPOSIT'S QUOTED CONSTANTS
    (NUMBERS.md 20.1): a signal removed at d_AA + D relaxes with time
    constant 1/(d_AA + D), so 1/0.1295 = 7.7 h for the predator's signal and
    1/0.2225 = 4.5 h for the prey's. The figure prints the same two numbers.
    """
    d.derivation_fig(
        "segment 4", "build  ·  the two equations we deleted",
        "Put the signals back and the loop gets longer",
        [
            ("restore the two states",
             "C_{1}, C_{2}, A_{1}, A_{2} — four again",
             "the loop regains the nodes the QSSA deleted"),
            ("and that is a lag",
             "each signal lags its own maker",
             "1/(d_{AA1}+D) = 7.7 h,  1/(d_{AA2}+D) = 4.5 h"),
        ],
        [FIG + "s24_pp_step_3.png", None],
        closing="A delay around a loop is what oscillates.",
        note="The two amber nodes are the ones we deleted, and putting them "
             "back is the whole of this step.\n "
             "A signal removed at its decay rate plus the dilution rate "
             "relaxes with a time constant of one over that sum. For the "
             "predator's signal that is about seven and a half hours; for "
             "the prey's, about four and a half. Those are real lags on the "
             "scale of a population that doubles in an hour.\n "
             "So the loop is predator, signal, prey, signal, back to the "
             "predator — four nodes and two lags in it, where the reduced "
             "version had two nodes and none.\n "
             "And that is session 11's result arriving in a new substrate. "
             "What makes a loop oscillate is the delay around it. The "
             "repressilator's delay was three transcription steps; this "
             "one's is two molecules waiting to accumulate outside the "
             "cells that make them.")


def _s4_hopf(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  the crossing, located")
    d.title(s, "Put the signals back and the real part crosses zero")
    d.image_centered(s, FIG + "s24_hopf_D.png", top=1.70, band=4.40)
    d.foot(s, "Two crossings: D = 0.0367 and D = 0.1674 /h, period 73.6 h at "
              "the upper one. Box 1B's caption calls these Hopf bifurcation "
              "points — the word is theirs.")
    d.notes(s,
            "Four states, same coexistence point, and now the leading real "
            "part does cross — twice. The oscillatory region in dilution "
            "rate is bounded on both sides.\n "
            "Nought point zero three seven at the bottom, nought point one "
            "six seven at the top, with a period of about seventy-four hours "
            "at the upper crossing. Both located by the same kind of sweep "
            "they wrote on problem set five, not read off this curve.\n "
            "Between them the coexistence focus is unstable and the "
            "community oscillates; outside them it spirals in; and a little "
            "above the upper crossing coexistence is lost altogether.\n "
            "And it has a name, which is theirs rather than mine: Box 1B's "
            "caption says a line connecting Hopf bifurcation points "
            "demarcates three regions.\n "
            "So the shape of the whole move: an approximation they trusted "
            "removed the phenomenon, the algebra proved it had to, the "
            "validity check said why, and restoring the two equations we "
            "deleted brought it back.")


def _s4_box1b(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  their own regime diagram")
    d.title(s, "A curve separates the three regimes")
    _crop(d, s, "balagadde2008_box1b",
          "Balagaddé et al., Mol Syst Biol 2008, Box 1B",
          "Death rate against growth rate, both the predator's.", h=3.95)
    d.rows(s, [
        ("the axes", "death rate on y, growth rate on x — both the "
                     "predator's, both per hour, both strain properties."),
        ("three points on one line",
         "growth rates 0.2, 0.8 and 1.2 /h: prey, oscillation, predator. "
         "All modelED, not measured."),
        ("and this is where the LOCUS is",
         "their caption: a line connecting HOPF BIFURCATION points "
         "demarcates three regions.", AMBER),
        ("two cautions",
         "the caption sets both constants EQUAL; Box 1B's OTHER panel is "
         "cells per µl, a CONCENTRATION.", RED),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "Their bifurcation analysis, in a plane spanned by two strain "
            "parameters: death rate up the side, growth rate along the "
            "bottom. And it is a MODEL result, not an experiment — worth "
            "saying two slides from a model-versus-experiment slide.\n "
            "Three operating points along one horizontal line, and the "
            "panel I have not put up beside this one carries the three time "
            "courses that go with them. Prey wins, they oscillate, predator "
            "wins.\n "
            "This is the slide where they draw the whole LOCUS. Their "
            "caption says a line connecting Hopf bifurcation points "
            "demarcates three regions — so what separates the regimes is a "
            "curve in a plane, not a number, and Fig. 2C in a moment is a "
            "single crossing of that curve.\n "
            "And it matters for the design conclusion: those are both STRAIN "
            "parameters. Which regime you are in depends on what you built. "
            "The dilution rate is the thing you can still change after the "
            "strains exist.\n "
            "Two reading cautions. The caption sets both species' constants "
            "equal while the axes are labeled for the predator, and the "
            "caption wins. And the population axis on Box 1B's OTHER panel "
            "— the one with the time courses, which is not on this slide — "
            "is ten cubed cells per microlitre, a concentration, where the "
            "rest of the paper counts cells per reactor. Never put the two "
            "on one axis.")


def _s4_fig2c(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  the knob they could turn")
    d.title(s, "IPTG is the knob they could cross it with")
    _crop(d, s, "balagadde2008_fig2c",
          "Balagaddé et al., Mol Syst Biol 2008, Fig. 2C",
          "Predator density against IPTG, with a period inset.", h=2.50)
    d.rows(s, [
        ("read it from its axes",
         "a solid stable branch, a dashed unstable one, and the branch point "
         "labeled Hopf on the panel — but not in the Fig. 2 caption."),
        ("why IPTG is their knob",
         "in the deposited model IPTG enters in exactly TWO places: the "
         "prey's signal synthesis and the predator's death rate.", AMBER),
        ("two things not to reproduce",
         "the inset's axis is printed IPTG (M) and the units are µM. And the "
         "three traces along the bottom print in one ink."),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "This is their version of the curve we just computed, against "
            "the knob they had in the lab.\n "
            "I describe it from its axes rather than its caption. Solid "
            "branch stable, dashed branch unstable, and a green dot where "
            "they meet, with the word Hopf set in bold just below and left "
            "of it. The word IS on this panel. What it is not in is the "
            "Fig. 2 caption, which says only bifurcation diagram — and the "
            "distinction is worth making because a caption is what people "
            "quote. It is also in Box 1B's caption and three times in their "
            "results text. So this is the slide where they CROSS the "
            "bifurcation; Box 1B is where they draw the whole LOCUS of "
            "them.\n "
            "Why IPTG and not dilution? Because of how it enters. In the "
            "deposited model IPTG appears in exactly two rules — the prey's "
            "signal synthesis and the predator's death rate — and nowhere "
            "else. It moves both strain parameters at once, which is also "
            "why it is not a clean single-parameter knob, and they say so.\n "
            "Two reading cautions. The inset's axis says molar and means "
            "micromolar. And the bottom row of simulated traces comes out in "
            "one ink, so the color legend beside it does not apply there — "
            "do not ask anyone to tell predator from prey in that row.")


def _s4_data(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  one reactor, and then all twelve")
    d.title(s, "The clean trace is one reactor out of twelve")
    _crop(d, s, "balagadde2008_fig2a",
          "Balagaddé et al., Mol Syst Biol 2008, Fig. 2A",
          "IPTG = 5 µM, D = 0.1125 /h, period ~180 h.", x=2.88, h=2.50)
    _crop(d, s, "balagadde2008_fig2b",
          "Balagaddé et al., Mol Syst Biol 2008, Fig. 2B",
          "Twelve reactors, six IPTG levels, 0–200 h.", x=6.70, h=2.50)
    d.rows(s, [
        ("the hedge is the right panel's",
         "several reactors is the Fig. 2B caption, not 2A's. 2A is one trace "
         "pair."),
        ("and some induced reactors did something else",
         "prey high, predator flat for 200 h — domination, not oscillation.",
         AMBER),
    ], top=5.78, bottom=7.32, side=False, pad=0.04)
    d.notes(s,
            "Left is the headline result and it is genuinely clean: a "
            "hundred and eighty hour period, prey and predator out of phase, "
            "running for most of a month.\n "
            "Right is the honest companion, and it is in the same figure. "
            "Twelve reactors, and six different IPTG levels across them — "
            "four columns, but not four levels. Some of the induced ones "
            "show the prey going up and staying up with the predator flat "
            "for two hundred hours — that is not an oscillation, it is prey "
            "domination. The four uninduced reactors wash the prey out, "
            "which is what they intended.\n "
            "I am careful about whose hedge is whose. The phrase several "
            "reactors is in the caption of the twelve-panel figure, not of "
            "the single trace. The single trace is a selected reactor and "
            "the figure next to it is how you know.\n "
            "And then the thing I admire about the paper. The chip holds "
            "fourteen reactors and this figure shows twelve of them, so "
            "both numbers are right and I say which is which. The "
            "throughput was sold as a feature, and it is also the "
            "instrument that shows the variability. They published both.")


def _s4_mismatch(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  the model against the experiment")
    d.title(s, "Four disagreements out of five")
    d.image_centered(s, FIG + "s24_model_vs_experiment.png", top=1.70,
                     band=4.40)
    d.text(s, "The model's cycle at D = 0.11 is 168 h — 3.4× the reactor's "
              "slowest ring.",
           M, 6.16, W - 2 * M, 0.42, role="body", bold=True, color=RED)
    d.foot(s, "Steady where the model oscillates (D = 0.11, 0.15); "
              "oscillating where the model has lost coexistence (0.20, "
              "0.23); agreed at 0.31. Those are MEASURED limit-cycle "
              "periods, not a linearised 2π/|Im λ|.")
    d.notes(s,
            "Five dilution rates, the five the authors ran. The "
            "model's row is computed; the experiment's row is the regime "
            "they state in their own text at each one. No panel is "
            "digitized for this.\n "
            "Four of the five disagree, and the thing that makes it "
            "interesting is that they disagree in OPPOSITE directions. At "
            "low dilution the experiment is steady and the model is "
            "oscillating. At high dilution the experiment is oscillating and "
            "the model has already lost the coexistence state.\n "
            "And it is not only the PLACE that is wrong, it is the "
            "timescale. At nought point one one the model settles into a "
            "limit cycle of a hundred and sixty-eight hours, and at nought "
            "point one five, a hundred and twenty-two. The slowest thing "
            "the reactor ever did was ring at about fifty. So the model's "
            "slowest cycle is three and a half times the slowest "
            "oscillation they ever saw, and nothing it does at any dilution "
            "rate resembles the experiment.\n "
            "One methodological point, because it is also how to read the "
            "number I gave a few slides ago. Linearise at the unstable "
            "fixed point, take two pi over the imaginary part, and you get "
            "about fifty hours — and that is NOT a cycle period. It is the "
            "period of the infinitesimal spiral at a point the system "
            "leaves, and setting it beside a measured period compares "
            "unlike quantities. The numbers I just gave are integrated "
            "limit cycles, measured peak to peak. The one place a "
            "linearised period IS the right quantity is at a Hopf, where "
            "the emerging cycle has that period by construction — which is "
            "why the seventy-three point six hours on the crossing slide "
            "is sound.\n "
            "Before anyone concludes we typed it in wrong, the next slide "
            "closes that door.")


def _s4_faithful(d):
    s = d.light()
    d.header(s, "segment 4", "build  ·  and it is not a transcription error")
    d.title(s, "The same model reproduces their own Fig. 3C")
    # The MAIN-PANEL sub-crop, not the full one: this slide asks the room to
    # read the panel from its axes, and the three time courses below the main
    # axes are never used here. Strict sub-region of balagadde2008_fig3c
    # (NUMBERS.md 23.0); the panel letter C is inside it, so the ref stays
    # Fig. 3C.
    #
    # MEASURED, AND IT DOES NOT BUY MAGNIFICATION AT THIS CALL SITE. Both
    # crops are WIDTH-bound against _crop's max_w = 4.80 -- the full crop
    # wants 4.87 in at h=3.40 and is capped, the sub-crop wants 8.02 and is
    # capped -- so the main panel renders 4.80 x 2.04 in either way and the
    # x-label projects at the same size. The 1.6x needs an image about 7.9 in
    # wide, and the four rows beside it already need 4.49 in of a 4.64 in
    # band, so there is no width to give it without cutting taught text.
    # What the swap does deliver is 1.32 in of vertical space and no unused
    # ink. Reported upward rather than decided here.
    #
    # DECIDED by Adam, 8 November: keep the crop, do not chase the
    # magnification. So "read it from its axes" stays in the row below even
    # though the axis type projects at about 6.6 pt -- the caption-vs-axes
    # catch is the move, and he will say the axes out loud. Reaching the
    # 20 pt floor would have meant ~9.5 in of image width, i.e. giving the
    # panel its own slide and moving these four rows to the next one. He
    # declined that trade. **Do not re-open this**; the measurement is
    # above, the decision is here.
    _crop(d, s, "balagadde2008_fig3c_main",
          "Balagaddé et al., Mol Syst Biol 2008, Fig. 3C",
          "Predator density against D, with a period inset.", h=3.40)
    d.rows(s, [
        ("three independent agreements",
         "D = 0.0367 against their 0.035–0.04; 0.1674 against ~0.168; "
         "0.176 against washout above 0.18.", TEAL),
        ("so the model is faithfully theirs",
         "the BioModels deposit, curated from this paper. Not a "
         "reconstruction, not a typo."),
        ("their phrase for all of this",
         "the model QUALITATIVELY ACCOUNTS FOR the observations.", AMBER),
        ("read it from its axes",
         "the caption says PERIOD against D; the main y-axis is predator "
         "cells. Only the inset is period."),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "This is the door-closing slide. Three numbers, all computed "
            "from the deposited constants, all landing on what their own "
            "figure prints.\n "
            "The oscillatory branch opens where theirs opens. The upper "
            "crossing is at the same dilution rate with the same period. And "
            "coexistence is lost near nought point one seven six, against "
            "their washout above nought point one eight — I say both halves "
            "of that one out loud, because a number with no comparator "
            "beside it is not an agreement.\n "
            "So this is their model. Not a reconstruction, not a typo. And "
            "it disagrees with their reactor at four of five settings.\n "
            "Which puts a lot of weight on one phrase, and it is theirs: "
            "qualitatively accounts for. I want the room to notice what that "
            "phrase is doing, because this is the honest standing of most "
            "models in this course — the shape is right and the numbers are "
            "wrong.\n "
            "One reading caution on the panel itself. The caption calls it a "
            "diagram of period against dilution rate; the main axes are "
            "predator cells. It is the inset that is period. Describe a "
            "panel from its axes.")


def _s4_release(d):
    s = d.light()
    d.header(s, "segment 4", "pose  ·  on your own paper  ·  vote, then argue")
    d.title(s, "Your turn: double the dilution rate")
    d.shape(s, S.ROUNDED_RECTANGLE, M, 1.84, W - 2 * M, 1.50, fill=WASH,
            line=TEAL, lw=2)
    d.text(s, "The reactor is running at D = 0.1125 per hour with both "
              "populations coexisting. You double it to D = 0.225.",
           M + 0.32, 1.96, W - 2 * M - 0.64, 0.80, role="emphasis",
           color=INK, spacing=1.12)
    d.text(s, "Work it off the four equations you wrote, not off the "
              "figures. What does raising D do to every term it appears in?",
           M + 0.32, 2.86, W - 2 * M - 0.64, 0.40, role="body", color=BODY)
    d.rows(s, [
        ("a", "what happens to the PREDATOR, and why — argue it from the "
              "two death-rate terms.", AMBER),
        ("b", "name the quantity that decides it, and say whether it belongs "
              "to the strains or to the reactor.", AMBER),
    ], top=3.54, label_w=0.5, bottom=5.10)
    d.text(s, "D appears in four places. Any answer that moves only one of "
              "them is incomplete.",
           M, 5.40, W - 2 * M, 0.44, role="body", bold=True, color=TEAL)
    d.notes(s,
            "I want this argued from the equations rather than looked up, "
            "because writing and reading that model is the thing they are "
            "being assessed on.\n "
            "The answer: the predator goes. Raising D adds equally to both "
            "death rates AND speeds the removal of both signals, so the "
            "predator loses its rescue twice over — its own antidote signal "
            "is washing out faster, and the prey that makes it is being "
            "diluted too. The interior crossing of the two nullclines moves "
            "and then stops existing. In the deposited model coexistence is "
            "lost a little above nought point one seven six, and nought "
            "point two two five is past that.\n "
            "Part b: the dilution rate, and it belongs to the REACTOR. The "
            "regime diagram we just looked "
            "at is spanned by two strain parameters, so most of this system "
            "is fixed once you have built the strains. D is what is left.\n "
            "The line at the bottom is there to catch the common wrong "
            "answer, which moves the death rates and forgets the signals.")


def _s4_debrief(d):
    s = d.light()
    d.header(s, "segment 4", "debrief  ·  the answer, off the equations")
    d.title(s, "The predator loses its rescue twice over")
    d.rows(s, [
        ("D in the death rates", "m_{1} and m_{2} both carry a bare +D, so "
                                 "both populations die faster. That is the "
                                 "half everybody gets."),
        ("D in the signal removals",
         "A_{1} = k_{A1}C_{1}/(d_{AA1}+D), and the same for A_{2}. Raising D "
         "LOWERS the standing signal, so the antidote is weaker at the same "
         "prey density. That SCALING survives; what the "
         "QSSA could not do is ELIMINATE the variable.", AMBER),
        ("the rescue fails twice",
         "less prey making signal, and faster removal of what they make. "
         "Coexistence is lost a little above D = 0.176, and 0.225 is past "
         "it.", AMBER),
        ("and it is the reactor's",
         "the dilution rate. Box 1B's plane is spanned by two STRAIN "
         "parameters, so once the strains are built that plane is fixed. D "
         "is what is left.", TEAL),
    ], top=1.88, label_w=3.9, bottom=6.36)
    d.notes(s,
            "Both halves, and the second one is the half the question was "
            "for.\n "
            "D sits in both death rates, so raising it kills both "
            "populations faster. Everyone gets that.\n "
            "D also sits in both signal removals, and that is the one people "
            "miss. The standing concentration of each signal is its maker's "
            "density over decay plus dilution. Raise dilution and the same "
            "number of prey produce a smaller signal. So the predator's "
            "antidote gets weaker even before the prey has thinned out.\n "
            "Put the two together and the rescue arm fails from both ends. "
            "The interior crossing walks off and coexistence goes with it. "
            "In this model that happens a little above nought point one "
            "seven six, and we doubled to nought point two two five.\n "
            "And the design reading: the thing that decided it is the "
            "reactor's parameter, not the strains'. Which is the useful half "
            "of today, because the strains are expensive and the pump is "
            "not.")


def _s4_poll(d):
    """The two-part poll, both stems and all options printed.

    DESIGN splits the stem deliberately: asking what the MODEL says and what
    the EXPERIMENT did as two separate votes makes the mismatch the subject
    rather than a footnote. Version 1's single stem had three defensible
    options, which is a broken poll.

    Each card's text column is 5.16 in, which at the 20 pt floor is 37
    characters, so every stem and every option is written to fit one line.
    """
    s = d.light()
    d.header(s, "segment 4", "vote  ·  silently, then argue, then vote again")
    d.title(s, "Two votes at the same dilution rate")
    for x, (head, stem, opts, col) in zip(
            (M, 6.95),
            [("vote 1  ·  the MODEL",
              "At D = 0.23 /h, the model says:",
              ["A   sustained oscillation, ~30 h",
               "B   a stable coexistence state",
               "C   no coexistence state at all",
               "D   prey out, predator persists"], AMBER),
             ("vote 2  ·  the EXPERIMENT",
              "At D = 0.23 /h, they observed:",
              ["A   sustained oscillation",
               "B   damped oscillation, ~30 h",
               "C   the predator washed out",
               "D   the prey washed out"], TEAL)]):
        d.shape(s, S.ROUNDED_RECTANGLE, x, 1.82, 5.68, 3.48, fill=WASH,
                line=col, lw=2)
        d.text(s, head, x + 0.26, 1.94, 5.16, 0.34, role="body", font=HEAD,
               bold=True, color=col)
        d.text(s, stem, x + 0.26, 2.38, 5.16, 0.36, role="body", color=INK)
        for i, o in enumerate(opts):
            d.text(s, o, x + 0.26, 2.92 + i * 0.56, 5.16, 0.40, role="body",
                   color=BODY)
    d.text(s, "Both votes are about the same reactor at the same setting. "
              "That is why they are asked separately.",
           M, 5.52, W - 2 * M, 0.44, role="body", bold=True, color=TEAL)
    d.notes(s,
            "Two separate votes, deliberately, because asking them together "
            "lets the mismatch slide past as a detail.\n "
            "Vote one is C. At nought point two three the deposited model "
            "has no interior fixed point — coexistence is gone a little "
            "above nought point one seven six.\n "
            "Vote two is B. At nought point two three they saw a damped "
            "oscillation with a period of about thirty hours, and then at "
            "nought point three one the predator washed out.\n "
            "So the model says nothing can live there and the reactor "
            "contained two living populations ringing at thirty hours. I "
            "record the distribution on both votes and then I let them "
            "argue, because the interesting disagreement in the room is "
            "usually about whether that makes the model useless.\n "
            "My answer to that, if it comes up: it gets the shape of the "
            "dependence right and the locations wrong, which is enough to "
            "design an experiment with and not enough to set a pump by.")


# ===================================== MOVE 5 · is a second strain worth it =
# T76 -- decide whether to split a pathway across strains. Assessed by the
# session 24 HOME GUIDE and on the FINAL, hand-graded, and NOT on PS9. The
# release and debrief below are the technique's only demonstration anywhere
# in the course, which is why the release names two pathways rather than two
# kinds of pathway and prints every number it needs.

# Neither theta in this hour is written bare: move 1's receiver half-output
# concentration is theta_A and Tsoi's inefficiency factor is theta_I, so the
# subscripts carry the distinction and no slide needs a foot to explain it
# (docs/symbols.md; bar B1 rules out defining a symbol in a note). The old
# THETA_NOTE foot on _s5_criterion is gone with it.


def _z4_paper(d):
    """Two papers, introduced together, before either is used.

    They are a pair on purpose: Zhou alone is an anecdote, Tsoi alone is a
    criterion with nothing under it.
    """
    s = d.light()
    d.header(s, "stop 4", "the papers")
    d.title(s, "One demonstration and one piece of arithmetic")
    d.rows(s, [
        ("the demonstration", "Zhou, Qiao, Edgar & Stephanopoulos. "
                              "Distributing a metabolic pathway among a "
                              "microbial consortium enhances production of "
                              "natural products. Nat Biotechnol 33, "
                              "377–383 (2015)."),
        ("what they built", "A taxane pathway cut in two across E. coli and yeast — neither "
                            "makes the product alone. They build the SAME split twice, and "
                            "what changes between them is the ecology.",
         TEAL),
        ("the arithmetic", "Tsoi, Wu, Zhang, Bewick, Karig & You. Metabolic "
                           "division of labor in microbial systems. PNAS "
                           "115, 2526–2531 (2018). A criterion for when "
                           "splitting helps at all."),
        ("why both", "Zhou on its own is an anecdote. Tsoi on its own is a "
                     "criterion with nothing under it. Together they are a "
                     "design decision you can make.", AMBER),
    ], top=1.90, label_w=3.4, bottom=6.36)
    d.notes(s,
            "Two papers for one stop, and they do different jobs.\n "
            "Zhou is the existence proof. A real pathway, really cut in "
            "two, across two species — and the interesting part is that "
            "they built the same split twice and only the ecology changed "
            "between them.\n "
            "Tsoi is the arithmetic. One inequality that says when the "
            "split is worth doing. It is what the home guide and the final "
            "ask you to use.\n "
            "I say out loud why there are two. A demonstration without a "
            "criterion is a story, and a criterion with no demonstration "
            "under it is a formula nobody has any reason to trust.")


def _z4_learning(d):
    """One sentence, on its own slide, closing stop 4 and the hour."""
    s = d.light()
    d.header(s, "stop 4", "what this establishes")
    d.title(s, "Split when the burden removed beats the transit paid")
    d.rows(s, [
        ("the result", "Two cells each carrying one enzyme grow better than one "
                       "carrying both — but on a HALVED capacity, so splitting starts "
                       "a factor of two behind. The crossing is the decision."),
        ("what you set", "One strain or two, where the cut goes, and how "
                         "much enzyme each half expresses — each enzyme's "
                         "burden is proportional to its expression.", AMBER),
        ("what you inherit", "The intermediate. η is how fast it crosses, "
                             "δ_{me} how fast it turns over outside, and "
                             "ε_{T} = δ_{me}/η is what you pay. The leakier "
                             "it is, the more burden it takes to justify "
                             "the split."),
        ("burden is PER ENZYME", "take B as the pathway total and "
                                           "the verdict on one of the two "
                                           "pathways you just did reverses.",
         RED),
    ], top=1.98, label_w=3.5, bottom=6.40)
    d.notes(s,
            "The sentence for the whole hour, not just this stop: splitting "
            "pays when the burden you take out of each cell beats the "
            "intermediate you lose getting it between them.\n "
            "The factor of two is the part worth saying twice. At zero "
            "burden, division of labor LOSES — two populations sharing one "
            "capacity. It does not start level and win; it starts behind "
            "and catches up, and where it catches up is the whole question."
            "\n "
            "What they inherit is the intermediate, and it is two numbers "
            "rather than one. Their ratio is the penalty, but the criterion "
            "needs both.\n "
            "The last row is the one that costs marks. Per enzyme, not per "
            "pathway. They just saw it flip an answer.\n "
            "Then the ledger, and the hour is three columns: what you set, "
            "what is set for you, where it stops being true.")


def _s5_declare(d):
    s = d.light()
    d.header(s, "stop 4", "frame  ·  the question changes")
    d.title(s, "Everything so far assumed you wanted a community")
    d.rows(s, [
        ("what we have been doing", "taking a job that needs more than one "
                                    "cell and building it — a gradient, a "
                                    "band, a four-colony logic circuit."),
        ("the question now", "you have a job that one cell CAN do. Should "
                             "you split it across two strains anyway?",
         AMBER),
        ("division of labor", "one pathway, cut in two, with each half in a "
                               "different strain and the intermediate "
                               "crossing between them. That is the object "
                               "for the rest of the hour."),
        ("and the last stop gave the reason",
         "re-using a part in another cell buys program size. Tamsir did it "
         "for computation. The question now is whether it buys anything "
         "for a pathway.", TEAL),
    ], top=1.92, label_w=3.6, bottom=6.30)
    d.notes(s,
            "I say out loud that the question is changing, because the first "
            "four moves all assumed the answer.\n "
            "Everything so far took a job that genuinely needs more than one "
            "cell. A gradient needs a sender and a receiver. An XOR on a "
            "plate needs four colonies. Fine.\n "
            "Now: a pathway that one cell can run. Three enzymes, one "
            "chassis, it works. Should you cut it in half and put the halves "
            "in two strains? That is a design decision with a real answer, "
            "and it is what the home guide will ask you.\n "
            "The reason anyone would is in Voigt's introduction rather than "
            "his abstract, and it is the best sentence in that paper for "
            "this course: you can build a bigger program out of fewer "
            "orthogonal parts if you re-use the same parts in different "
            "cells. Session 17 was an hour on how short that list of "
            "orthogonal parts is. This is the move that makes the list go "
            "further.")


def _s5_zhou_glucose(d):
    s = d.light()
    d.header(s, "stop 4", "build  ·  the same split, built twice")
    d.title(s, "Version one: the ethanol the yeast makes")
    _crop(d, s, "zhou2015_fig1",
          "Zhou, Qiao, Edgar & Stephanopoulos, Nat Biotechnol 33:377–383 "
          "(2015), Fig. 1", "The glucose co-culture.", h=3.20)
    d.rows(s, [
        ("the split", "E. coli makes taxadiene; yeast oxygenates it. NEITHER "
                      "makes the product alone."),
        ("the chemistry works", "taxadiene does cross and does get "
                                "oxygenated. A yeast-only control makes "
                                "none."),
        ("the culture does not", "density and titer both fall. 2 mg/L in "
                                 "72 h.", RED),
        ("and the agent is the ETHANOL",
         "on glucose the yeast makes ethanol, and at 50 g/L it stopped "
         "E. coli outright. The fix removes the ethanol, not the yeast.",
         AMBER),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "A pathway genuinely cut in two, across two SPECIES. E. coli "
            "makes the terpene, yeast oxygenates it with a P450, and neither "
            "organism can make the product by itself.\n "
            "The chemistry is fine. The intermediate crosses, the P450 does "
            "its job, and a yeast-only control makes nothing — so the "
            "transfer is real.\n "
            "The culture is not fine. Put the yeast in and the E. coli "
            "density drops and the total taxane output drops with it. Two "
            "milligrams per liter in three days.\n "
            "And I am careful about the causal statement, because it is the "
            "whole value of the paper for us. It is not that the yeast "
            "inhibits the E. coli. On glucose the yeast ferments and makes "
            "ethanol, and ethanol at the highest concentration they observed "
            "stopped the E. coli dead. The agent is a metabolite. That is "
            "what the second design goes after.")


def _s5_zhou_xylose(d):
    s = d.light()
    d.header(s, "stop 4", "build  ·  the same split, built twice")
    d.title(s, "Version two: each removes the other's problem")
    _crop(d, s, "zhou2015_fig2", "Zhou et al., Nat Biotechnol 2015, Fig. 2",
          "On xylose the two become mutually dependent.", h=3.20)
    d.rows(s, [
        ("one change: the carbon source",
         "E. coli on xylose excretes acetate. Yeast eats acetate, not "
         "xylose, and makes no ethanol."),
        ("so the dependency runs both ways",
         "yeast grows only with E. coli; E. coli's inhibitor is removed. "
         "Ethanol below the 0.1 g/L limit.", AMBER),
        ("and the honest number",
         "2 → 4 mg/L in 72 h. STABILITY, not titer.", RED),
        ("the headline took three more steps",
         "more yeast and feeding, a stronger promoter, then deleting "
         "ATP synthase subunits (atpFH) so the ONLY route to ATP was "
         "making acetate. 33 mg/L.", TEAL),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "One change, and it is not genetic. Swap glucose for xylose.\n "
            "On xylose the E. coli excretes acetate and poisons itself a "
            "little. The yeast cannot touch xylose, so it has nothing to eat "
            "except the acetate — and eating acetate it does not ferment, so "
            "no ethanol. Each organism removes the other's problem, and "
            "neither of them was engineered to do it. The paper designed "
            "that and calls it a mutualistic relationship.\n "
            "Then the number that keeps me honest. Two milligrams to four. "
            "Eight percent of the taxadiene oxygenated. What version two "
            "bought was a culture that holds, not a yield.\n "
            "The thirty-three milligram headline is three further pieces of "
            "work, and the last one is the one to carry out of here: they "
            "knocked out ATP synthase subunits so that the only way E. coli "
            "could make ATP was to make acetate. Their word is enforce. They "
            "stopped hoping for cooperation and made it the only option.\n "
            "And then the species ratio regulated itself — inoculated at "
            "about forty to one yeast to E. coli, it settles to one to two "
            "by forty-one hours, because yeast growth is limited by the "
            "acetate the E. coli makes.")


def _s5_criterion(d):
    """Tsoi's criterion, STATED rather than derived, with the assumptions on
    the slide that states it (bar F3). Every symbol defined here.
    """
    s = d.light()
    d.header(s, "stop 4", "build  ·  the criterion, stated")
    d.title(s, "Biomass you gain against intermediate you lose")
    _crop(d, s, "tsoi2018_fig1c",
          "Tsoi, Wu, Zhang, Bewick, Karig & You, PNAS 2018, Fig. 1C",
          "Their two sides, drawn.", h=3.40)
    d.rows(s, [
        ("split it when", "biomass gained beats per-cell productivity "
                          "lost."),
        ("the gain side", "each enzyme's B_{1}, B_{2}. One cell carries the "
                          "SUM; split, each carries one on HALF the "
                          "capacity."),
        ("the loss side", "η its transport rate, δ_{me} its turnover outside, ε_{T} = "
                          "δ_{me}/η. θ_{I} needs BOTH, not the ratio.",
         AMBER),
        ("all five assumptions travel",
         "passive diffusion · the two populations DO NOT COMPETE · each "
         "on half the capacity · well mixed · substrate in excess.", RED),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.foot(s, "θ_{I} = (k + η υ_{2})/(k + η υ), with "
              "k = δ_{me}(1 + η/α_{2}e_{2}) and α_{2}e_{2} = 1 here. "
              "υ is steady-state biomass; ῡ_{DOL} = √(υ_{1}υ_{2}). "
              "The panel’s bare ε is ε_{T}.")
    d.notes(s,
            "The criterion is stated, not derived — it is their equation and "
            "the derivation is in a supplement we do not hold.\n "
            "Split when the biomass you gain beats the productivity you "
            "lose. One side each.\n "
            "The gain is real and it has a mechanism: a single cell "
            "expressing both enzymes carries the sum of both burdens, and "
            "burden enters growth rate, so splitting always helps growth. "
            "What it costs is capacity — the two populations share one "
            "halved carrying capacity, so at zero burden division of labor "
            "starts a factor of two behind and has to earn its way out.\n "
            "The loss side is transport. The intermediate has to get out, "
            "survive, and get in. Eta is how fast it crosses, delta-m-e is "
            "how fast it decays outside, and their ratio is the transport "
            "inefficiency epsilon-T — subscript T for transport, and the "
            "bare epsilon they print is this one.\n "
            "I read the printed inequality out symbol by symbol, because "
            "it is on the slide and it decides the rest of the hour. Two "
            "reading cautions on the panel first: their upsilon is set in "
            "an italic that looks like a Latin v, and the epsilon they "
            "print bare is the one we are calling epsilon-T, because this "
            "hour already spent a bare epsilon on the predator-prey "
            "reduction. We do not alter a published panel, so the slide "
            "says it instead.\n "
            "Upsilon is a population's steady-state biomass. Upsilon-bar-"
            "D-O-L is the geometric mean of the two split populations'. "
            "Theta-I is the inefficiency factor the biomass gain has to "
            "beat, and I flag that it depends on the two transport numbers "
            "separately rather than only on their ratio. That matters for "
            "the question in a minute.\n "
            "And the assumptions are on the slide because the criterion is "
            "worth nothing without them. They also assume well-mixed "
            "conditions, excess substrate and enzymes at steady state. The "
            "one that will bite is that the two populations are assumed not "
            "to compete. Two E. coli strains in one flask eating the same "
            "sugar are competing.")


def _s5_dol_fig(d):
    s = d.light()
    d.header(s, "stop 4", "build  ·  the two sides, computed")
    d.title(s, "Splitting trades capacity for growth")
    d.image_centered(s, FIG + "s24_dol.png", top=1.70, band=4.44)
    d.text(s, "μ_{max} is the host's top growth rate, δ_{υ} its turnover, "
              "ρ its capacity.",
           M, 6.22, W - 2 * M, 0.42, role="body", color=BODY)
    d.foot(s, "Both axes are the TOTAL B = B_{1}+B_{2} — Tsoi’s "
              "βe_{1}+γe_{2} — so the crossing here is a total. The borders "
              "in a moment are PER ENZYME, half this scale. Never read one "
              "against the other.")
    d.notes(s,
            "Left: the single cell carries the sum of both burdens, so its "
            "density collapses first. The split pair each carry one term and "
            "keep growing — but they are sharing a halved capacity, so at "
            "zero burden they start behind. The crossing is where the gain "
            "catches up with the halving.\n "
            "Right: where that crossing sits depends on what you ASSUMED "
            "about burden, which is the next slide.\n "
            "Three parameters are printed along the top of the figure and "
            "they are not ours to choose, so I name them here rather than "
            "at the ledger. Mu-max is the host's "
            "fastest growth rate, delta-upsilon is how fast the population "
            "turns over, and rho is its carrying capacity. The RATIO "
            "mu-max over delta-upsilon is the one you need in a few "
            "minutes: it is how much burden the host can carry before it "
            "stops growing, and the release prints it as ten.\n "
            "One thing to say out loud about the axis, because it is the "
            "mistake I most expect. This axis is the TOTAL burden, B-one "
            "plus B-two, and the crossing on it is a total. The two "
            "borders I put up in a few minutes are per enzyme, which is "
            "half this scale. Read one against the other and you are out "
            "by a factor of two, and that is enough to flip the verdict.")


def _s5_caveat(d):
    s = d.light()
    d.header(s, "stop 4", "build  ·  the border moves with your modeling")
    d.title(s, "The burden form you assume moves the border")
    _crop(d, s, "tsoi2018_fig2d", "Tsoi et al., PNAS 2018, Fig. 2D",
          "Linear, exponential and Hill burden.", h=3.20)
    d.rows(s, [
        ("the border moves about fivefold",
         "across the three forms on the same axes, with everything else "
         "held. Only how burden was written down changed.", AMBER),
        ("the DIRECTION is a fact about the functions",
         "at n = 2, 1/(1+B²) ≥ e^{−B} ≥ 1 − B for every B ≥ 0. So Hill puts "
         "the border highest and linear lowest. That ordering is not a "
         "choice.", TEAL),
        ("the SIZE is a chosen example",
         "their own caption: in this example, parameters are chosen such "
         "that Hill-type burden reduces growth the least and linear the "
         "most.", RED),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "This is the modeling-choice slide and it is the honest limit "
            "on everything we are about to compute.\n "
            "Three ways of writing the same idea — that enzyme makes the "
            "host grow slower — and the border between split and do-not-"
            "split moves by a factor of about five between them. The biology "
            "did not move. The algebra did.\n "
            "I separate two things there, because they have different "
            "standing. The ORDER is a fact: the Hill form is always above "
            "the exponential which is always above the linear one, at every "
            "burden, and you can check that in one line. So Hill always puts "
            "the border highest.\n "
            "The SIZE of the gap is not a fact. Their own caption says the "
            "parameters were chosen so the three forms order that way. So "
            "fivefold is this example's number.\n "
            "Which is why the comparison I am about to make holds the "
            "burden form fixed. Two pathways under the same assumption can "
            "be compared. Neither border position means anything on its own.")


def _s5_release(d):
    """T76's demonstration, and the stem is the specification in DESIGN 7.4.

    THREE THINGS THIS STEM HAS TO GET RIGHT, each of which has gone wrong
    once in this folder:
      * PER ENZYME. Read as a pathway total, A's two enzymes carry 0.6 each,
        far below its border, and the criterion then says LEAVE A -- the
        opposite verdict, reached by correct reasoning from an ambiguous
        stem.
      * eta AND delta_me, never their ratio. epsilon_T does not pin the
        border: sweeping eta from 0.2 to 10 with delta_me held at 0.5 eta --
        every pair giving epsilon_T = 0.5 -- moves the border by about 0.03.
      * the two pathways PULL OPPOSITE WAYS, which is what forces both
        halves of the inequality to be used.
    """
    s = d.light()
    d.header(s, "stop 4", "pose  ·  on your own paper  ·  vote, then argue")
    d.title(s, "Your turn: split one of these two pathways")
    # ONE LINE, and it has to stay one line: the box tops are at 2.34 and a
    # second line runs underneath them, which `slide_fit` cannot see (it
    # compares text with text, never text with a drawn shape). The wrapped
    # version hid μ_{max}/δ_{υ} = 10, without which the criterion cannot be
    # applied at all. Keep this under about 75 characters.
    d.text(s, "Both pathways: TWO ENZYMES, ONE HOST.  Hill burden, n = 2.  "
              "μ_{max}/δ_{υ} = 10.",
           M, 1.78, W - 2 * M, 0.46, role="body", bold=True, color=INK)
    for x, (name, lines, col) in zip(
            (M, 6.95),
            [("A  ·  the intermediate crosses freely",
              ["transport rate   η = 1.0",
               "turnover outside   δ_{me} = 0.001",
               "burden   B_{1} = B_{2} = 1.2  PER ENZYME"], TEAL),
             ("B  ·  charged, and lost fast once outside",
              ["transport rate   η = 1.0",
               "turnover outside   δ_{me} = 0.5",
               "burden   B_{1} = B_{2} = 1.3  PER ENZYME"], CYAN)]):
        d.shape(s, S.ROUNDED_RECTANGLE, x, 2.34, 5.68, 2.30, fill=WASH,
                line=col, lw=2)
        d.text(s, name, x + 0.26, 2.46, 5.16, 0.62, role="body", font=HEAD,
               bold=True, color=TEAL, spacing=1.12)
        for i, ln in enumerate(lines):
            d.text(s, ln, x + 0.26, 3.16 + i * 0.44, 5.16, 0.40,
                   role="body", color=INK)
    d.rows(s, [
        ("a", "split ONE of them across two strains. Which, and why — name "
              "the term that decided it.", AMBER),
        ("b", "what would you MEASURE before building either version?",
         AMBER),
    ], top=4.84, label_w=0.5, bottom=6.30)
    d.text(s, "Those are PER ENZYME. Read as a pathway total they halve, "
              "and the answer changes.",
           M, 6.54, W - 2 * M, 0.44, role="body", bold=True, color=RED)
    d.notes(s,
            "Every number they need is printed, because none of them can be "
            "read off a figure.\n "
            "The two pathways pull opposite ways on purpose. B carries the "
            "higher burden, which argues for splitting it. B's intermediate "
            "also moves slowly, which argues against. So neither half of the "
            "inequality can be skipped.\n "
            "The answer is split A, leave B — and I want them to feel why "
            "that is surprising before I show it.\n "
            "The red line is load-bearing. B-one and B-two are per enzyme. "
            "If anyone "
            "reads it as a pathway total they will halve it, get nought "
            "point six for A, find it far below A's border, and correctly "
            "conclude leave A alone. That is a right answer to a different "
            "question and I do not want to be marking it.\n "
            "Part b is the half students skip if it is not asked separately, "
            "and it is the half a hand-graded item is really for.")


def _s5_debrief(d):
    """The verdicts, computed by posb.dol_criterion.

    Borders found by rooting the yield margin in the PER-ENZYME burden
    B_1 = B_2 at the pathway's own (eta, delta_me): A 1.135146, B 1.355143.
    Both re-verified against `dol_criterion` on 8 November. Single-cell
    yields 0.323 and
    0.132, so both populations are alive in both cases -- this is the part
    of the plane where the criterion is deciding something.

    The three caveats DESIGN requires on the debrief get the slide after
    this one rather than a footnote: at this column width they are 700
    characters, which is four times what fits under the table.
    """
    s = d.light()
    d.header(s, "stop 4", "debrief  ·  the answer, computed")
    d.title(s, "The higher-burden pathway is the one you leave")
    hdr = ("", "η, δ_{me}", "ε_{T}", "θ_{I}", "B_{1}=B_{2}", "its border",
           "split it?")
    rows = [("A", "1.0, 0.001", "0.001", "1.166", "1.2", "1.135",
             "YES", TEAL),
            ("B", "1.0, 0.5", "0.500", "1.116", "1.3", "1.355",
             "no", TEAL)]
    xs = (M, M + 0.75, M + 3.15, M + 4.25, M + 5.45, M + 6.55, M + 8.95)
    d.shape(s, S.ROUNDED_RECTANGLE, M - 0.08, 1.76, 11.0, 0.46, fill=TEAL,
            line=None)
    for x, h in zip(xs, hdr):
        d.text(s, h, x, 1.84, 2.3, 0.32, role="body", font=HEAD, bold=True,
               color=WHITE)
    for r, row in enumerate(rows):
        y = 2.34 + r * 0.56
        for x, cell in zip(xs, row[:7]):
            d.text(s, cell, x, y, 2.3, 0.34, role="body", font=HEAD,
                   bold=True, color=row[7] if x == M else INK)
    d.text(s, "Burden and border are PER ENZYME. Both single cells are "
              "still alive — biomass 0.32 and 0.22 — so the criterion is "
              "deciding something here.",
           M, 3.60, W - 2 * M, 0.44, role="body", color=BODY)
    d.rows(s, [
        ("why the higher burden is the one you leave alone",
         "fast loss outside pushes the border UP. B's border is above "
         "its burden; A's is below. So “more burden, so split it” is the "
         "wrong rule on its own.",
         AMBER),
        ("what you would measure",
         "B_{1} and B_{2}, per enzyme; the host's μ_{max}/δ_{υ}; and η "
         "against δ_{me}. "
         "Zhou is the case of the last: their intermediate crossed freely, "
         "and what they engineered was the ecology."),
    ], top=4.44, bottom=7.30, side=False, pad=0.04)
    d.notes(s,
            "Split A, leave B, and the reason is the opposite of the rule "
            "most people would guess.\n "
            "B carries more burden. B is also the one whose intermediate "
            "turns over fast once it is outside the cell, and that pushes "
            "B's border up above its burden. A's border sits below A's "
            "burden. So the pathway you split is the one that is cheaper to "
            "split, not the one that hurts most.\n "
            "I check out loud that both single cells are alive — yields of "
            "nought point three two and nought point one three. That matters "
            "because above a burden of about one point five the single cell "
            "dies of its own enzymes and the criterion stops deciding "
            "anything.\n "
            "Part b, the measurement half: the burden per enzyme times "
            "expression, the host's resilience, and the two transport "
            "numbers. Zhou is the case study for the last one, and the twist "
            "is that their intermediate crossed freely and the thing they "
            "had to engineer was the ecology.")



def _s5_debrief2(d):
    """The second half of the debrief: the three caveats DESIGN requires on
    the slide rather than in a footnote. They are 700 characters at this
    width, so they get their own slide rather than being cut to fit under
    the table on the one before.
    """
    s = d.light()
    d.header(s, "stop 4", "debrief  ·  what the verdict does not settle")
    d.title(s, "Three caveats on the number you just computed")
    d.rows(s, [
        ("the burden values are ours",
         "1.2 and 1.3 are values this session picked, evaluated with their "
         "criterion at the printed n = 2 and μ_{max}/δ_{υ} = 10. They are "
         "NOT points on Fig. 1D's axis: that axis is not the burden the "
         "criterion is written in, and putting its border back through their "
         "own inequality needs a host 10^{4} times more resilient than "
         "anything they state.", AMBER),
        ("no border position transfers",
         "the border moves about fivefold on TSOI's burden axis. The "
         "COMPARISON between A and B survives, because both were evaluated "
         "under the same form; neither border position survives on its own.",
         RED),
        ("and Tsoi contains no experiment anywhere",
         "their own best natural examples — nitrification and syringate "
         "metabolism — exist in BOTH single-cell and divided form, and they "
         "write that what constrained the difference remains an open "
         "question. A computed verdict here is an argument, not a decision "
         "procedure, which is exactly why this one is hand-graded.", RED),
    ], top=1.88, bottom=7.00, side=False, pad=0.04)
    d.notes(s,
            "The caveats are not decoration, and I say all three.\n "
            "Those two burden numbers are mine. I picked them, and I "
            "evaluated them with their criterion at the parameters printed "
            "on the release. They are not points on their figure's axis, and "
            "that is a real finding rather than caution: put their drawn "
            "border back through their own inequality and you need a host "
            "with a resilience of order ten thousand, which the paper "
            "nowhere supports. So the axis is not the quantity the criterion "
            "is written in, and no number transfers off it. The direction "
            "the border moves does.\n "
            "Second, on their own axis the border moves about fivefold with how you "
            "write burden down. So no single border position means much. "
            "What survives is the comparison, because both pathways used the "
            "same form.\n "
            "Third, the paper has no experiment in it at all. Its own best "
            "natural examples exist both ways and the authors say the "
            "question is open.\n "
            "Which is why this technique is hand-graded. What earns credit "
            "is naming the term that decided it, not reaching a particular "
            "verdict.")

# ================================================== CLOSE · the ledger =====
# lecture-design 5d, and the house pattern is session 22's: a derivation()
# run rather than four separate rows() slides, because rows() re-spreads its
# leftover band every click and the earlier lines slide up the wall. Here
# each run is one column of the ledger shown a line at a time, and pacing()
# already counts a step run as one slide's worth of material.
#
# NO ASIDES ON ANY OF THESE RUNS, and the Limits observables are inside the
# body rather than in an aside. An aside is placed below the equation and
# clamped to a ceiling; with a two-line equation at the 1.125in pitch it
# lands 0.013in clear of the row below, which is not a margin. Three lines
# of 20 pt body fit the same pitch with 0.117in spare, which is what session
# 22's ledger established.
# The four ledger slides were written with d.derivation(), which renders
# ONE SLIDE PER STEP on purpose: an argument must not show its endpoint
# before the room has had step one. A ledger has no endpoint to withhold --
# every row restates something the hour already established -- so the
# reveal bought nothing and cost 17 slides. Converted to d.rows() on
# 14 November 2026, at Adam's instruction: 17 slides -> 4. Do not put the
# reveal back.


def _ledger_knobs(d):
    s = d.dark()
    d.header(s, "close", "the design ledger  ·  knobs")
    d.title(s, "What you can set")
    d.rows(s, [("the sender",
          "k_{I}, the synthase expression — a promoter choice, and the one "
          "number neither paper gives you."),
         ("the medium",
          "γ_{A}, set by the medium and its pH, which moves ℓ_{A} = √(D_{A}/γ_{A}). "
          "And WHICH PAIR of signals you use."),
         ("the receiver",
          "β_{L} and β_{C} — a repressor and operator choice. The threshold "
          "itself: a receptor mutation, or copy number."),
         ("the placement",
          "where the senders sit — their NUMBER, SPACING and "
          "DENSITY — and which gate strain goes where. Basu set "
          "it, Tamsir set it, and it costs no cloning either "
          "time."),
         ("the architecture",
          "one strain or two — and with it how much enzyme you express, "
          "which each enzyme’s own burden B_{1} or B_{2} is proportional "
          "to."),
    ], top=1.74, bottom=6.34, label_w=3.0)
    d.foot(s, "Check these against the three questions you were given at the "
              "start of the hour.")
    d.notes(s,
            "Knobs have to be physical or they are not knobs, so every row "
            "here names the thing you would change.\n "
            "The sender's knob is a promoter, and it is the one number "
            "neither paper gave us.\n "
            "The medium is two knobs in one row. The decay rate, which you "
            "move with pH and buffering and which sets the reach. And which "
            "pair of signals you picked, which fixes the ratio you start "
            "from — because you cannot dial a diffusion coefficient.\n "
            "The receiver's knobs are a choice of repressor and operator for "
            "the two coefficients, and then the threshold itself, which Basu "
            "moved two different ways: a point mutation in LuxR, and halving "
            "the plasmid copy number.\n "
            "The last row is today's closing technique, and how much enzyme "
            "you express goes with it, because what the criterion sees is "
            "burden per unit of enzyme times the amount expressed. I keep "
            "that per-enzyme: B-one and B-two are each one enzyme's, and "
            "the single cell is the one carrying their sum.")


def _ledger_constraints(d):
    s = d.dark()
    d.header(s, "close", "the design ledger  ·  constraints")
    d.title(s, "What is set for you")
    d.rows(s, [("the coefficient",
          "D_{A} itself: pick a signal and inherit it. The LAWN supplied most of "
          "Karig's ratio — 1.5 free, 21.6 through cells."),
         ("the sensitivity gap",
          "0.003 µM against 3 µM across two quorum systems. It comes with "
          "the receptor pair and buys NO orthogonality."),
         ("the population's own limits",
          "the carrying capacity, the two growth rates, and the cell's own "
          "export of the signal."),
         ("the host and the enzyme",
          "the burden per unit of enzyme, and μ_{max}/δ_{υ}, the host's "
          "resilience to carrying it. Neither is yours."),
         ("the intermediate",
          "δ_{me}, how fast it turns over once outside, which with η sets "
          "the transport penalty ε_{T} you pay for splitting."),
    ], top=1.74, bottom=6.34, label_w=3.0)
    d.notes(s,
            "The first row is the one that changes how you think about "
            "diffusion. You do not set D-sub-A. You pick a molecule and you "
            "inherit what it does in the medium you have — and most of the "
            "ratio Karig ended up with came from the cells rather than from "
            "the molecules.\n "
            "The sensitivity gap is inherited with the receptor pair, and I "
            "say again that it buys no orthogonality, because that is the "
            "most tempting wrong inference in the hour.\n "
            "Carrying capacity, growth rates and the cell's own export are "
            "the population's, not yours.\n "
            "The last two rows are the closing technique's constraints. The "
            "burden per unit of enzyme belongs to the enzyme. The host's "
            "resilience belongs to the host. And how fast the intermediate "
            "turns over outside the cell belongs to the molecule and the "
            "medium. You choose whether to split; you do not choose any of "
            "the numbers that decide whether splitting pays.")


def _ledger_limits(d):
    s = d.dark()
    d.header(s, "close", "the design ledger  ·  limits")
    d.title(s, "Where today's results stop being true")
    d.rows(s, [("the first estimate",
          "t ≈ L²/2D_{A} at first; once decay matters the length is "
          "√(D_{A}/γ_{A}).  OBSERVABLE: the front stops and the band sits "
          "still."),
         ("a published coefficient",
          "Basu's ξ is really D_{A}/Δx² with Δx never printed, so it is not a "
          "diffusion coefficient.  OBSERVABLE: their own 10 mm ring needs "
          "833 h against a 36 h run whose ring was stable by 32 h."),
         ("the diffusion ratio",
          "The hundredfold is Karig's own non-stochastic simulation. There "
          "is no universal ratio.  OBSERVABLE: a pattern appears at a ratio "
          "your own analysis forbids."),
         ("the band edges",
          "Solved in the LIQUID-PHASE limit, by dropping equation (5). "
          "OBSERVABLE: the answer becomes a position, not a dose."),
         ("Tsoi's criterion",
          "It assumes the two split populations do not compete, each on "
          "half the capacity.  OBSERVABLE: the pair's combined density "
          "falls below the sum of the monocultures'."),
    ], top=1.70, bottom=6.52, label_w=2.9)
    d.notes(s,
            "The limits column is the one that must not be skipped, and "
            "every row names something you could see from a bench.\n "
            "The estimate we opened on is a first estimate and it is the "
            "wrong tool as soon as the signal decays. You can tell which "
            "regime you are in by whether the front is still moving: a band "
            "that sits still is a steady profile, not a spreading one, and "
            "Basu saw no positional shift over thirty-six hours.\n "
            "A published coefficient may not be a coefficient. The test is "
            "two lines of arithmetic against the paper's own geometry.\n "
            "The hundredfold belongs to one simulation of one scheme. You "
            "know you have left that limit when you get a pattern the "
            "deterministic analysis of your own kinetics forbids — which is "
            "what they saw.\n "
            "And the two edges we solved are a dose window only while a "
            "single AHL number describes the culture. The moment "
            "fluorescence depends on where you look, the same two numbers "
            "are the radii of a ring.\n "
            "The last row is the limit on the thing I am about to assess "
            "them on. Tsoi's criterion assumes the two populations eat "
            "different things and do not compete. Two E. coli strains in "
            "one flask on the same sugar ARE competing, and then the "
            "biomass gain on the left-hand side is not there. Testable by "
            "adding up biomass.")


def _reading(d):
    s = d.light()
    d.header(s, "close", "what to read before Thursday")
    d.title(s, "The reading for next time")
    d.assignment(s, y=2.00, row_h=0.84)
    d.text(s, "Today's home guide is on bCourses. One item is the "
              "split-or-not decision again, on a different pathway.",
           M, 1.48, W - 2 * M, 0.40, role="body", color=INK)
    d.notes(s,
            "Point at the home guide before the reading, because one of its "
            "items is the only other place in the course you will be asked "
            "to make the split-or-not call. It is hand-graded, the answers "
            "go up alongside it, and what earns full credit is naming the "
            "term that decided it rather than reaching a particular "
            "verdict.\n "
            "One warning for anyone who tries to find the border "
            "numerically: above a burden per enzyme of three both split "
            "populations die of their own burden, so the yield margin is "
            "identically zero up there and a bisection over any bracket "
            "containing three will hand you back three. That is not the "
            "border.\n "
            "Then the reading. Weinberger is the required one and it is a "
            "different kind of object again — the population becomes the "
            "carrier rather than the device.")











# --------------------------------------------------------------- appendix ---
def _appendix_contents_3(d):
    """The predator-prey run, annotated. Cut from the hour 14 November.

    It was twenty-three slides on Balagadde's two-strain reactor -- a
    Jacobian, a trace argument, a Hopf located twice, and their regime
    diagram against their own experiment. Nothing in the hour cites it any
    more: the two ledger rows that did were removed with it, and the one
    that survived is Tsoi's, which stop 4 establishes on its own. It comes
    out because the hour's thesis is division of labor and spatial
    placement, and a predator-prey oscillator is neither -- and because
    session 25 reaches a Hopf three ways with its own papers, and session 11
    already carries the oscillation criterion.
    """
    s = d.light()
    d.header(s, "appendix", "the predator-prey run, cut from the hour")
    d.title(s, "Balagadde's two-strain reactor, worked through")
    d.rows(s, [
        ("what it builds", "Two strains, each holding the other's survival: "
                           "one arm kills, the other rescues, and both end "
                           "on the same promoter. Four states, written down "
                           "with the room."),
        ("where it goes", "Quasi-steady state on the signals, then the Jacobian. The "
                          "trace is strictly negative, which RULES OUT a Hopf — until the "
                          "signals go back in and the longer loop crosses zero.", AMBER),
        ("the honest ending", "The model reproduces their own Fig. 3C to "
                              "three digits and still misses their "
                              "experiment at four of five dilution rates. "
                              "Shape right, numbers wrong.", RED),
        ("why it is here and not in the hour",
         "Session 11 already carries the oscillation criterion and "
         "session 25 reaches a Hopf three ways. This hour is about "
         "division of labor and placement, and this is neither."),
    ], top=1.92, label_w=3.1, bottom=6.40)
    d.notes(s,
            "I do not teach this. It is here because it is good and because "
            "the home guide's reactor question points at the same paper.\n "
            "If a question lands on whether a two-strain community can "
            "oscillate, the slide to put up is the trace one: a strictly "
            "negative trace is a no at ANY parameters, and that is a "
            "stronger statement than checking a few.\n "
            "And if anyone asks why we trust the criterion but not the "
            "model, the answer is on the third row.")


def _appendix_divider(d):
    s = d.dark()
    d.text(s, "Appendix", M, 2.55, 8.6, 1.10, size=40, font="head",
           bold=True, color=WHITE)
    d.text(s, "Thirty-seven slides that came out of the hour. Nothing in "
              "the hour depends on them.",
           M, 3.95, 8.6, 1.20, size=20, color=MINT, spacing=1.2)
    d.notes(s,
            "I do not teach from here. These are in the deck so the students "
            "have them when they read it afterwards, and so I can put one up "
            "if a question lands on it.\n "
            "Every one was checked for whether anything still in the hour "
            "cites it. Nothing does.")


def _appendix_contents_1(d):
    s = d.light()
    d.header(s, "appendix", "the ones most likely to come up")
    d.title(s, "The gradient, and reading Basu's data")
    d.rows(s, [
        ("Four decades of distance", "The scaling figure for the sender "
                                     "estimate. The hour states the result "
                                     "in words."),
        ("Running backwards", "Basu Fig. 2b. A high-detect strain on its "
                              "own, inverted."),
        ("Order and spread", "Basu Fig. 2d against the printed model. Same "
                             "order, about a decade of spread."),
        ("The outer ring", "Basu Fig. 3b and 3c — and the 36% the same "
                           "strain gave twice. That number is nowhere else "
                           "in the deck.", AMBER),
    ], top=1.92, label_w=3.1, bottom=6.40)
    d.notes(s,
            "Four slides from the first three segments. The band edges are "
            "solved in the hour; these check that answer against Basu's own "
            "pictures.\n "
            "The one in amber is the only place the ring irreproducibility "
            "appears — the same strain measured 30 mm once and 22 mm "
            "another time, and every cause they offer is the plate. If I "
            "want that in the hour it has to come back.")


def _appendix_contents_2(d):
    s = d.light()
    d.header(s, "appendix", "the ones most likely to come up")
    d.title(s, "The senders, the regression, and one reactor")
    d.rows(s, [
        ("The senders are the program", "Basu Fig. 5. Number, spacing and "
                                        "density make the shape. The ledger "
                                        "no longer claims this as a knob."),
        ("Which parameters matter", "Basu's regression on their own "
                                    "simulations. Nothing in it was "
                                    "measured."),
        ("One reactor out of twelve", "Balagadde Fig. 2a and 2b. Home guide "
                                      "item 3 asks which reactor earned "
                                      "which claim.", AMBER),
    ], top=1.92, label_w=3.1, bottom=6.40)
    d.notes(s,
            "The senders slide came out together with the ledger row that "
            "rested on it, so the hour no longer offers a knob it never "
            "showed.\n "
            "The regression is the one worth knowing about: an R-squared of "
            "nought point nine one, on a hundred simulations drawn from two "
            "thousand random parameter sets, with no experiment anywhere in "
            "it. It is a statement about their model.\n "
            "The reactor slide is home guide item 3, so the students read "
            "that evidence themselves with the answers alongside."
            )


# ---------------------------------------------- stop 1 \u00b7 Basu 2005 ---
def _b1_paper(d):
    """The paper introduced before any of its content is used."""
    s = d.light()
    d.header(s, "stop 1", "the paper")
    d.title(s, "Basu 2005: a lawn that lights in a ring")
    d.rows(s, [
        ("the paper", "Basu, Gerchman, Collins, Arnold & Weiss. A synthetic "
                      "multicellular system for programmed pattern "
                      "formation. Nature 434, 1130\u20131134 (2005). Your "
                      "required reading."),
        ("what they built", "Sender colonies that synthesize AHL, and a lawn "
                            "of receiver cells carrying a circuit whose "
                            "output is on only over a middle range of AHL."),
        ("what they found", "The lawn lights in a ring at a distance from the "
                            "senders. Receivers with different detection "
                            "thresholds ring at different radii, and where "
                            "the senders sit sets the shape.", TEAL),
        ("what we take from it", "How a circuit turns a distance into an "
                                 "input, and how to solve where the ring\u2019s "
                                 "two edges fall from their printed "
                                 "parameters."),
    ], top=1.92, label_w=3.4, bottom=6.40)
    d.notes(s,
            "They have read this one, so I spend the time on why it is the "
            "paper for today rather than on summarizing it.\n "
            "It is the only paper on the list where the design variable is "
            "where you put the cells. Everything else sets a part or a "
            "parameter; this sets a position.\n "
            "The circuit is a band detector \u2014 on in the middle of the "
            "AHL range, off at both ends. That is why a ring appears and "
            "not a disk, and it is the thing to hold on to through the "
            "whole stop.\n "
            "Three things they set, and each comes back: the two repression "
            "coefficients, the receiver\u2019s detection threshold, and "
            "sender placement.")


def _b1_learning(d):
    """One sentence, on its own slide, closing stop 1."""
    s = d.light()
    d.header(s, "stop 1", "what this establishes")
    d.title(s, "A band is what makes a distance readable")
    d.rows(s, [
        ("the mechanism", "Two routes to dark, and they are different "
                          "proteins. Close to the senders the MUTANT LacI "
                          "is high enough to shut the reporter. Far away "
                          "there is no CI, so WILD-TYPE LacI shuts it. In "
                          "between, CI has removed wild-type LacI and the "
                          "mutant is not yet effective — so the reporter "
                          "lights."),
        ("the condition", "The window exists only because CI acts on LacI at "
                          "a far lower concentration than LacI acts on GFP "
                          "\u2014 \u03b2_{C} = 8 nM against "
                          "\u03b2_{L} = 0.8 \u00b5M. Bring the two "
                          "together and the two dark regions meet, leaving "
                          "no band.", AMBER),
        ("what you set", "Both edges move with the repressor and operator "
                         "choice, and with the receiver\u2019s detection "
                         "threshold \u2014 a receptor point mutation, or "
                         "plasmid copy number."),
    ], top=1.95, label_w=3.2, bottom=6.30)
    d.notes(s,
            "This is the sentence I want them to say back to me.\n "
            "A switch gives a half-plane. A band gives a ring, and the ring "
            "has a radius I can move.\n "
            "Say the two routes carefully, because they are two different "
            "proteins and it is easy to run them together. Near the "
            "senders: mutant LacI, high enough to repress. Far away: no CI, "
            "so wild-type LacI is up. CI never touches the reporter — its "
            "target is wild-type LacI.\n "
            "The condition is the part that gets lost: bring the two "
            "coefficients together and there is no window. The data cannot "
            "tell us CI is the better repressor, only that its coefficient "
            "is much the smaller of the two.\n "
            "Next stop is what sets the radius, which nothing so far has "
            "said.")


# ------------------------------------------- stop 2 · Karig 2018, new ---
def _k2_paper(d):
    """Karig introduced before any of its numbers are used."""
    s = d.light()
    d.header(s, "stop 2", "the paper")
    d.title(s, "Karig 2018: diffusion measured through cells")
    d.rows(s, [
        ("the paper", "Karig, Martini, Lu, DeLateur, Goldenfeld & Weiss. "
                      "Stochastic Turing patterns in a synthetic bacterial "
                      "population. PNAS 115, 6572–6577 (2018)."),
        ("what they built", "Two AHL signals in one engineered lawn, wired "
                            "so the pattern mechanism needs the two to move "
                            "at different rates."),
        ("what they measured",
         "They fitted a fluorescence wave spreading through the lawn, so "
         "the number is an EFFECTIVE cell-to-cell coefficient: 3OC12HSL "
         "83 µm²/s, C4HSL 1810 µm²/s.", TEAL),
        ("why this paper", "It is the only source here for what moving "
                           "through cells costs a signal. Basu's ring needs "
                           "a coefficient and Basu do not have one."),
    ], top=1.92, label_w=3.8, bottom=6.40)
    d.notes(s,
            "I introduce this one properly because it is optional reading "
            "and some of them will not have it.\n "
            "What matters is how they got the number. They did not put AHL "
            "in a cuvette. They watched a fluorescence front move across a "
            "lawn of cells and fitted a coefficient to the profile. So what "
            "they report is what the signal does in the presence of cells, "
            "which is the quantity a circuit designer needs.\n "
            "Two numbers, and the pair matters more than either: eighty-three "
            "and eighteen hundred square microns per second. We come back to "
            "why they differ by so much.")


def _k2_wilkechang(d):
    s = d.light()
    d.header(s, "stop 2", "build  ·  what free solution would predict")
    d.title(s, "Size alone predicts a factor of about 1.5")
    d.rows(s, [
        ("the correlation", "Wilke–Chang estimates a small molecule's "
                            "diffusion coefficient in a solvent from three "
                            "things: temperature, the solvent's viscosity, "
                            "and the molecule's own molar volume."),
        ("how it scales", "D rises with temperature, falls with viscosity, "
                          "and falls as roughly the molar volume to the 0.6 "
                          "power. That exponent is weak — doubling the size "
                          "costs about a third of the coefficient."),
        ("so for Karig's pair", "they differ only in acyl chain length — "
                                "3OC12HSL about 297 Da against C4HSL's 171. "
                                "Free solution predicts a ratio near 1.5.",
         TEAL),
        ("they measured 21.6", "through the lawn. The molecules account for "
                               "about 1.5 of it, so roughly fourteen of that "
                               "factor is the cells.", AMBER),
    ], top=1.90, label_w=3.5, bottom=6.30)
    d.notes(s,
            "They need to know what the correlation is before the comparison "
            "means anything, so I spend a line on it.\n "
            "Wilke–Chang is the standard estimate for a small solute in a "
            "liquid. Temperature over viscosity on top, molar volume to the "
            "six tenths underneath. Nothing about the molecule's chemistry "
            "enters except its size.\n "
            "The exponent being weak is the whole point here. These two "
            "signals are the same molecule with a longer tail on one of "
            "them, so size can only buy a factor of one and a half.\n "
            "They measured twenty-one point six. That gap is the result, and "
            "it is a result about the lawn rather than about AHL.")


def _k2_bound(d):
    s = d.light()
    d.header(s, "stop 2", "build  ·  what the reach comes out as")
    d.title(s, "The reach comes out under a millimeter")
    d.rows(s, [
        ("from Basu's own set", "ξ = 0.001 mm²/min with γ_{A} = 0.01 min⁻¹ "
                                "gives ℓ_{A} = 0.32 mm. Their ring is at "
                                "10 mm — thirty-two e-foldings out."),
        ("borrowing Karig's", "83 µm²/s with the same decay rate gives "
                              "0.71 mm. Still fourteen times short — and it "
                              "is the wrong signal in a different lawn, so "
                              "it bounds the answer rather than giving it.",
         AMBER),
        ("what the ring requires", "run session 2's estimate backwards: a "
                                   "front at 10 mm by 32 h needs D ≈ 0.026 "
                                   "mm²/min, which is 433 µm²/s."),
        ("and that is a sane number", "session 2 had GFP in water at "
                                      "87 µm²/s. A 213-dalton lactone is "
                                      "roughly five times smaller in radius, "
                                      "so scaling gives about 450 µm²/s.",
         TEAL),
    ], top=1.88, label_w=3.6, bottom=6.24)
    d.foot(s, "The last scaling is mine: Stokes–Einstein gives D ∝ 1/radius, "
              "and radius ∝ mass^{1/3}, so D ∝ mass^{−1/3}. It settles an "
              "order of magnitude, not a number.")
    d.notes(s,
            "Three numbers for the same length and they do not agree, which "
            "is the honest state of this.\n "
            "Basu's own parameter gives a third of a millimeter. Thirty-two "
            "e-foldings to their ring is a concentration ratio around ten to "
            "the thirteenth, and no synthesis rate makes that a device.\n "
            "Borrowing Karig's coefficient triples the reach and leaves it "
            "fourteen times short. I say out loud that this is the wrong "
            "signal in a different lawn — it is a bound, not a value.\n "
            "Then backwards. A front at ten millimeters in thirty-two hours "
            "needs about four hundred square microns per second. Scale "
            "session 2's GFP-in-water number by size and a small lactone "
            "lands near four fifty.\n "
            "So the ring is consistent with a small molecule diffusing "
            "nearly freely, and inconsistent with both coefficients we hold. "
            "The difference between them is how much cell the signal has to "
            "cross.")


def _k2_learning(d):
    s = d.light()
    d.header(s, "stop 2", "what this establishes")
    d.title(s, "You set the decay rate and nothing else")
    d.rows(s, [
        ("the result", "ℓ_{A} = √(D_{A}/γ_{A}). Doubling the reach costs "
                       "four times the lifetime."),
        ("what you inherit", "D_{A} — and through a lawn it is mostly the "
                             "lawn, not the molecule. About fourteen of "
                             "Karig's factor of twenty-one."),
        ("what you set", "γ_{A}. The lactone ring hydrolyzes faster as pH "
                         "rises, and Basu say the decay rate sets the band's "
                         "steepness.", AMBER),
        ("what you check", "a published coefficient against that paper's own "
                           "geometry and duration. Two lines of arithmetic "
                           "caught one here."),
    ], top=1.95, label_w=3.4, bottom=6.30)
    d.notes(s,
            "Four things out of this stop.\n "
            "The length scale, derived rather than handed over, and the "
            "square root is the design fact: reach is cheap to lose and "
            "expensive to buy.\n "
            "The coefficient is not mine. Worse, in a lawn it is mostly the "
            "lawn, so the number I want depends on the cell density I am "
            "going to use.\n "
            "The decay rate is the knob, and it is a medium knob — pH and "
            "buffering. That is the one line of this stop that is a design "
            "action.\n "
            "And the habit: check a coefficient against the figure it "
            "generated before using it.")


# ------------------------------------------ stop 3 · Tamsir 2011, new ---
# Built 14 November 2026. Four slides: the paper, their XOR, their library,
# one sentence. This stop carries NO graded technique, which is why it is
# four slides and not twenty, and the two crops carry the results rather
# than a row of prose describing them. The gate and the wires are folded
# into the XOR slide -- the figure is already on screen there, and the gate
# only matters because it explains why the colonies compose at all.


def _t3_paper(d):
    """Tamsir introduced before the plate is used for anything."""
    s = d.light()
    d.header(s, "stop 3", "the paper")
    d.title(s, "Tamsir 2011: the arrangement is the circuit")
    d.rows(s, [
        ("the paper", "Tamsir, Tabor & Voigt. Robust multicellular computing "
                      "using genetically encoded NOR gates and chemical "
                      "“wires”. Nature 469, 212–215 (2011)."),
        ("what they built", "One logic gate per strain, with AHL carrying "
                            "the signal between colonies. Four strains "
                            "spotted in the right places on an agar plate "
                            "perform an XOR."),
        ("what they found", "A small library of those strains covers all "
                            "sixteen two-input functions with no further "
                            "genetic manipulation. Between one function and "
                            "the next, only the layout changes.", TEAL),
        ("why this paper", "Session 17 was an hour on how short the list of orthogonal "
                           "parts is. This is what you do about it — build a program from "
                           "fewer parts by “re-using them in multiple cells”."),
    ], top=1.92, label_w=3.5, bottom=6.30)
    d.sources(s, [("re-using parts in multiple cells",
                   "Tamsir, Tabor & Voigt, Nature 469:212–215 (2011), "
                   "introduction")])
    d.notes(s,
            "This is optional reading, so some of them will not have it. I "
            "introduce it properly and then move fast, because there is no "
            "derivation in this stop.\n "
            "One gate per strain. The gate's inputs are promoters and its "
            "output is a promoter, and the AHL is what carries a signal from "
            "one colony to the next.\n "
            "The result is the thing to hold: sixteen different circuits out "
            "of one set of strains, and the only difference between them is "
            "where the spots go. No cloning between functions.\n "
            "Why it is here: session 17 counted the orthogonal parts and the "
            "number was small. That hour ended on a problem. This is the "
            "answer — the same part, used again in a different cell.")


def _t3_xor(d):
    """Their XOR, shown. The gate and the wires ride along with the figure."""
    s = d.light()
    d.header(s, "stop 3", "their logic  ·  four colonies, one function")
    d.title(s, "An XOR is three NOR gates and a buffer")
    _crop(d, s, "tamsir2011_fig3",
          "Tamsir, Tabor & Voigt, Nature 469:212–215 (2011), Fig. 3",
          "The XOR, spotted in the arrangement that performs it.", h=3.20)
    d.rows(s, [
        ("the gate", "two tandem promoters in, a repressor out. Both input and "
                     "output are promoters, so gates layer."),
        ("NOR and buffer", "a NOR's output is on only when NEITHER input is. "
                           "A buffer's is on only when its input is."),
        ("one gate per strain", "three NOR gates and one buffer, four "
                                "strains, spotted in the arrangement the "
                                "function needs.", AMBER),
        ("the wires", "3OC12-HSL from LasI and C4-HSL from RhlI — KARIG's "
                      "two molecules, NOT Basu's 3OC6HSL.", TEAL),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "Four colonies on an agar plate, computing exclusive-or.\n "
            "The gate is worth thirty seconds because it is why any of this "
            "composes. Both the inputs and the output are promoters. So a "
            "gate's output can be another gate's input with no translation "
            "layer, and the AHL is what carries it between cells.\n "
            "NOR means output on when neither input is on. The buffer is the "
            "output stage, on when its input is on. Three NORs and a buffer "
            "make an XOR, and each one lives in its own strain.\n "
            "In the figure: the first colony takes arabinose and aTc and "
            "sends the long AHL to the two middle colonies. Each of those "
            "takes the long AHL and one of the inducers, and both send the "
            "short AHL to the output colony.\n "
            "The wires matter for this session specifically. Those are the "
            "same two molecules Karig measured — the ones a factor of twenty "
            "apart. They are NOT Basu's signal, so the honest callback is to "
            "the diffusion numbers rather than to the band detector.")


def _t3_sixteen(d):
    """Their library, shown. The plate's one length and one time with it."""
    s = d.light()
    d.header(s, "stop 3", "their result  ·  the same library, rearranged")
    d.title(s, "Sixteen two-input functions from one library")
    _crop(d, s, "tamsir2011_fig4", "Tamsir, Tabor & Voigt, Nature 2011, Fig. 4",
          "One small library, sixteen circuits.", h=3.95)
    d.rows(s, [
        ("every two-input function",
         "all sixteen, from one small library, with no further genetic "
         "manipulation.", AMBER),
        ("a length and a time",
         "1 µL spots on a 7 mm grid, 12 h between layers — an EXTERNAL "
         "CLOCK, so no transient wrong answer."),
        ("not a coefficient",
         "12 h is stated as SUFFICIENT, not as an arrival time. A "
         "coefficient needs a front position.", RED),
        ("one composition failure",
         "tandem gates ADD their promoters’ transfer functions — six of "
         "seven. Seventh: the pair reversed."),
    ], top=TOP, bottom=BOT, left=TXT, side=False, pad=0.04)
    d.notes(s,
            "Sixteen circuits out of one library of strains, and the only "
            "thing that changes between them is where the colonies sit. No "
            "cloning. The induction range across the set runs from five-fold "
            "for the XOR to three hundred and thirty-five-fold for the B "
            "gate.\n "
            "The plate has two numbers on it and they are the cheapest line "
            "in the stop: seven millimeters between spots, twelve hours "
            "between layers. They call the delay an external clock, and the "
            "reason is a good one — genetic computing is asynchronous, so if "
            "one path through the circuit is slower than another you get a "
            "transient wrong answer, a hazard. Spotting the layers in order "
            "with a delay removes the race.\n "
            "I say firmly that seven millimeters over twelve hours is not a "
            "diffusion coefficient. Twelve hours is stated as enough. A "
            "coefficient needs the front's position at a known time, and "
            "they never give one. This is the habit from the last stop, "
            "arriving one paper later.\n "
            "The last row is session 17 as a measurement. A tandem promoter "
            "adds its two inputs' transfer functions, and that prediction "
            "worked six times out of seven. The failure is the same two "
            "promoters in the other order — they offer DNA looping, binding- "
            "site occlusion or mRNA stability and settle none of them. A "
            "part that composes one way round and not the other is exactly "
            "what session 17 was about.")


def _t3_learning(d):
    """One sentence, on its own slide, closing stop 3."""
    s = d.light()
    d.header(s, "stop 3", "what this establishes")
    d.title(s, "Re-using a part in another cell buys program size")
    d.rows(s, [
        ("the result", "Sixteen functions out of one library. Each one is a "
                       "layout, not a new part — the one move that makes a "
                       "short list of orthogonal parts go further."),
        ("what you set", "Which gate strain goes where, and the order the "
                         "layers are spotted in. That is the whole program.",
         AMBER),
        ("what you inherit", "The wire carries no address. Every gate on "
                             "C4-HSL hears every colony sending it — Tamsir "
                             "use that on purpose, with two colonies "
                             "reporting to one output, and it is also why "
                             "the library needs two signals rather than one."),
        ("what still breaks", "Composition inside a cell. The addition rule "
                              "for tandem promoters held six times out of "
                              "seven, and the one failure was the same pair "
                              "in the other order.", RED),
    ], top=1.95, label_w=3.4, bottom=6.30)
    d.notes(s,
            "The sentence I want back from them: a part re-used in another "
            "cell buys program size, and adding parts does not, because "
            "there are not many parts to add.\n "
            "What they set is a position. That is the second time this hour "
            "— Basu set where the senders go, Tamsir sets where the gates "
            "go. Different purposes, same design variable.\n "
            "The limit is worth a line because it is the reason this does "
            "not scale forever. An AHL is a broadcast, not a wire to a named "
            "destination. Every gate that reads C4-HSL hears every gate that "
            "makes it. They exploit that here, deliberately, but it means "
            "the number of independent connections is the number of "
            "orthogonal signals — and that list is short too.\n "
            "And the honest caveat: putting gates in separate cells fixed "
            "composition between cells and did nothing for composition "
            "inside one.\n "
            "So more cells bought computation. Next: what else does a second "
            "cell buy?")
