"""Session 18 — Protein circuits: a parameter is manufactured, not found.

Tuesday 27 October 2026. Part II, third session. Required reading already out:
Mishra et al., Science 2021. Ceroni 2015 is handed out at the close.

WHAT THIS SESSION IS. Session 9 ended on a slide its own notes call "THE slide
of the lecture": cooperativity is the parameter that most determines bistability
and the one you can least control, and Gardner solved it by CHOOSING a repressor
that already dimerizes. Today is the answer to that slide. A covalent
modification cycle reaches an apparent Hill coefficient of 26 from ONE site with
no cooperative binding anywhere in it, and the knob that places the switch is a
ratio of two expression levels -- session 9's EASY axis.

Session 17's thesis was "a part is manufactured, not found". This is the same
sentence about a PARAMETER, which is what makes Part II continuous with Part I
rather than a change of subject.

THE BRIDGE THAT WAS BACKWARDS. s17's DESIGN.md set this up as "so stop using
promoters". The algebra says the opposite: (V1/V2) at half-maximum is a
ratio of (k + 1/2), so as the Michaelis constants shrink -- which is what buys
the sharpness -- the threshold walks to 1 and stops being tunable. The protein
layer buys sharpness the transcriptional layer cannot; the transcriptional layer
still sets the threshold. You need both. Corrected in s17/DESIGN.md, 19 October.

TWO DEBTS THIS SESSION PAYS.
  * s04's note of 8 September promised zero-order ultrasensitivity to session
    13, with a number ("an apparent n above 20 from ONE site"). Session 13
    contains none of it. Discharged here, out loud, in segment 3.
  * s02 asked the room on 1 September why the same circuit behaves differently
    in a bacterium and a human cell, and its notes say "it is why session 18
    exists". Paid on the SPEED axis in segment 5 and on specificity in 6.

THE OBJECT BEFORE THE MODEL. Vocabulary check across every deck s04-s17:
"kinase" 0, "phosphatase" 0, "Michaelis" 9 — eight in s04 (seven weeks
ago) and one in s05. So the session may assume none of it, and the biology gets its own segment
before any algebra. The structural fact to land while drawing it: this is the
FIRST system in the course whose total is conserved. Every circuit so far had
production balanced against dilution. Here nothing is made and nothing is
destroyed, and that is where the sharpness comes from.

FIGURES COME FROM THE PAPERS WHERE THEY EXIST. 24 crops are declared in
decks/paper_figures.yaml. Ours are the ones students reproduce in the notebook,
and they go up AFTER the authors' version of the same picture, never instead.

NOTE ON BASHOR FIG. 4: Science reissued panels B and D on 22 August 2008. The
article page carries the superseded schematics. Use the _corrected keys wherever
the wiring is what is being read.

WHERE THE NUMBERS COME FROM. sessions/s18-protein/NUMBERS.md, every one with a
kind. The two kinds that must never be confused on a surface here: Goldbeter &
Koshland contains NOT ONE MEASUREMENT -- the authors say so on p. 6844 -- and
Bashor's and Dueber's Hill coefficients are measured. 26.08 is derived; 2.84 is
measured. Say which, every time.

NO PRINTED TIME RANGES. Minutes are Adam's.

Run:  python tools/build_decks.py s18
"""
from pptx.enum.shapes import MSO_SHAPE

from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)
from decks.theme import LINE, ROOT, line_cap, scale

FIG = "figures/build/"
FILENAME = "s18-protein"

FOOT_Y = 6.75


def _fig(d, s, name, y, dpi=160):
    """Place a figure at its natural size, centered, and return its bottom."""
    from PIL import Image
    w, h = Image.open(ROOT / FIG / f"{name}.png").size
    w, h = w / dpi, h / dpi
    if y + h > FOOT_Y - 0.10:
        raise AssertionError(
            f"{name}: placed at {y:.2f}in, {h:.2f}in tall, so it ends at "
            f"{y + h:.2f}in and runs into the foot at {FOOT_Y}. Shorten the "
            f"figure in figures/s18_protein.py -- cut content, not type.")
    d.image(s, FIG + f"{name}.png", (W - w) / 2, y, w, h)
    return y + h


def _cell_height(txt, w, size):
    """Height of `txt` in a `w` inch box, wrapped at WORD boundaries.

    theme.text_height divides the character count by the characters that fit,
    which is right on average and wrong per cell: a line that cannot break
    mid-word wraps early, so a cell that the estimate calls two lines renders
    as three. In a row stack the gap absorbs that. In a table it does not --
    the first build of this deck had seven overlapping pairs and every one of
    them was short by exactly one line (0.27in at 16pt). So this wraps greedily
    the way the renderer does.
    """
    # theme.text() maps a bare `size=` up onto the type scale -- size=16 and
    # size=14 both RENDER at the 20pt content floor. Measuring at the number
    # passed rather than the number rendered is a guaranteed underestimate,
    # and it was five of the seven overlaps on the first build. Measure at the
    # size that will actually be set. (theme.paper_figure has the same
    # mismatch internally: it reserves its citation line at TYPE["caption"]
    # and renders it at scale(14). Reported, not changed here -- it touches
    # every deck.)
    size = scale(size)
    cap = line_cap(w, size)
    n = 0
    for para in str(txt).split("\n"):
        words = para.split()
        if not words:
            n += 1
            continue
        lines, cur = 1, 0
        for word in words:
            add = len(word) + (1 if cur else 0)
            if cur and cur + add > cap:
                lines += 1
                cur = len(word)
            else:
                cur += add
        n += lines
    return n * size / 72.0 * LINE


def _paper(d, s, key, y, h, ref, caption):
    """Place a paper figure at ITS OWN aspect ratio, centered, and return the
    bottom of the citation line.

    paper_figure() takes a box and fits the image inside it, so a box whose
    shape does not match the figure's leaves the image small in a large empty
    slot -- nine of them on the first build of this deck, every one reported by
    the build and invisible on the page. Nothing here is sized by eye: the
    aspect comes from the file, the caller gives a height, and the width
    follows. A figure that would be wider than the text column is fitted to the
    column instead.
    """
    from PIL import Image

    from decks.theme import _resolve_paper_figure
    img = _resolve_paper_figure(key)
    if img.exists():
        iw, ih = Image.open(img).size
        w = h * iw / ih
        if w > W - 2 * M:
            w = W - 2 * M
            h = w * ih / iw
    else:
        w = min(W - 2 * M, h * 1.5)      # a slot, for the public build
    # paper_figure() sets the citation line as wide as the IMAGE, so a tall
    # narrow figure gets a narrow column and a long citation wraps into the
    # foot. Measure it rather than reserving a constant.
    ref_h = max(0.30, _cell_height(ref, w, 14))
    if y + h + 0.04 + ref_h > FOOT_Y - 0.05:
        raise AssertionError(
            f"{key}: {h:.2f}in tall at y={y:.2f}in, and its citation needs "
            f"{ref_h:.2f}in in a {w:.2f}in column, which reaches "
            f"{y + h + 0.04 + ref_h:.2f}in against a foot at {FOOT_Y}. "
            f"Reduce h, or shorten the ref.")
    d.paper_figure(s, key, (W - w) / 2, y, w, h, ref, caption)
    return y + h + 0.04 + ref_h


def _grid(d, s, cols, rows, top=2.26, colw=None, size=16, head_color=None,
          gap=0.20):
    """A comparison table. Columns are fixed; row heights are measured.

    theme.rows() pitches one label against one body, which is the wrong shape
    for T45 -- four media against three axes only reads if the columns line up.
    So this measures each cell at the type size it will render at, takes the
    tallest in the row, and stacks. Nothing is pitched by eye. The saved file
    still goes through slide_fit, which is what catches the case this gets
    wrong.
    """
    n = len(cols)
    colw = colw or [(W - 2 * M) / n] * n
    xs, x = [], M
    for cw in colw:
        xs.append(x)
        x += cw
    # The header row is measured like any other. It was assumed to be one
    # line until a four-column table gave a column head that wrapped, and the
    # head landed on the first data row.
    y = top
    head_h = max([_cell_height(c, colw[j] - 0.18, 14)
                  for j, c in enumerate(cols)] + [0.34])
    for j, c in enumerate(cols):
        d.text(s, c, xs[j], y, colw[j] - 0.18, head_h, size=14, bold=True,
               color=head_color or (CYAN if s._posb_dark else TEAL))
    y += head_h + 0.08
    d.shape(s, MSO_SHAPE.RECTANGLE, M, y - 0.08, W - 2 * M, 0.012,
            fill=SILVER if s._posb_dark else MUTED)
    for r in rows:
        cells = r if isinstance(r, (list, tuple)) else (r,)
        hs = [_cell_height(c, colw[j] - 0.18, size)
              for j, c in enumerate(cells)]
        rh = max(max(hs), 0.34)
        for j, c in enumerate(cells):
            d.text(s, str(c), xs[j], y, colw[j] - 0.18, rh, size=size,
                   bold=(j == 0),
                   color=(WHITE if s._posb_dark else INK) if j == 0
                   else (SILVER if s._posb_dark else None))
        y += rh + gap
    if y > FOOT_Y - 0.05:
        raise AssertionError(
            f"_grid: the table ends at {y:.2f}in and the foot is at {FOOT_Y}. "
            f"Cut a row or shorten a cell -- do not shrink the type.")
    return y


def build():
    d = Deck("Session 18 — Protein circuits", session=18)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _goals(d)
    _object(d)
    _derivation(d)
    _saturation(d)
    _cost(d)
    _mishra(d)
    _media(d)
    _comparison(d)
    _close(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    s = d.dark()
    d.text(s, "Session 18  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "A parameter is manufactured, not found",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "Thursday: a part is manufactured, not found. Today the same "
              "sentence about a NUMBER — and the number is the one session 9 "
              "told you that you could least control.",
           M, 4.50, 8.6, 1.2, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.45, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "Mishra was the reading. PS6 is due Thursday and PS7 goes out "
               "Thursday; say so at the close, not here.\n"
               "The title is the thesis and it is deliberately Thursday's "
               "sentence with one word changed. Part II is not a change of "
               "subject.")


def _retrieval(d):
    s = d.light()
    d.header(s, "retrieval", "Three minutes  ·  no notes")
    d.title(s, "Three things from Thursday and from session 9")
    d.rows(s, [
        ("from Thursday",
         "you measured a promoter's strength in one construct and it was different in the next. What physically changed, given that the promoter sequence did not?"),
        ("from Thursday",
         "what is the difference between a part's identity and a part's sequence? Give me the junction argument in one sentence."),
        ("from session 9",
         "the toggle needs cooperativity on at least one arm or the wedge closes. Where did Gardner GET his?"),
    ])
    d.foot(s, "The third one is the hinge. He chose a repressor that already dimerized. That is not engineering a parameter — that is shopping for one.")
    d.notes(s, "Q1 and Q2 are warm-ups. The answer to Q1 is the 5'UTR the junction encodes.\n"
               "Q3 is the one this hour exists to answer. Push until somebody "
               "says he picked a protein that already had the property. Then "
               "leave it: 'so cooperativity is something you shop for. Is it?' "
               "and move. Do not resolve it here.")


def _goals(d):
    s = d.light()
    d.header(s, "today", "where we are going")
    d.title(s, "By the end of the hour")
    d.rows(s, [
        ("Draw the object", "a covalent modification cycle, with real enzymes on it, and say what is conserved and what is not."),
        ("Derive the switch", "one quadratic, two exact results. An apparent Hill coefficient of 26 out of a system with no cooperative binding in it."),
        ("Price it", "the sharpness is free and the threshold is not. The constraint is exact and you will meet it again."),
        ("Compare four media", "transcription factor, phosphorylation, CRISPRi, recombinase — on orthogonality, speed and load. With the empty cells left empty."),
    ], label_color=TEAL)
    d.foot(s, "And an answer to a question this class was asked on 1 September: why does the same circuit behave differently in another cell?")
    d.notes(s, "Say the last line slowly. Session 2 posed that as an "
               "objectives-as-pretest question in week one and its notes say "
               "'it is why session 18 exists'. Eight weeks is a long time to "
               "hold a question open, and closing it visibly in front of them "
               "is why the date gets said.")


# ------------------------------------------------------- 1 · the object ---
def _object(d):
    # --- the biology, in the authors' words, before any abstraction --------
    s = d.light()
    d.header(s, "segment 1", "the object")
    d.title(s, "Switched on and off by a pair of enzymes")
    d.rows(s, [
        ("The discovery",
         "Cori & Green, and Krebs & Fischer: glycogen phosphorylase exists in two forms, phosphorylated and dephosphorylated. One protein, two states, and a pair of enzymes that interconvert them."),
        ("What it controls",
         "“carbohydrate metabolism, fat metabolism, sensory systems, muscular contraction, protein synthesis … and malignant transformation” — Goldbeter & Koshland, PNAS 1981, p. 6840."),
        ("The two enzymes",
         "a KINASE puts a phosphate on; a PHOSPHATASE takes it off. Both are running at the same time, in the same compartment, on the same pool of protein. Neither ever stops."),
        ("What is spent",
         "ATP, every cycle. The modified and unmodified protein are both conserved; the phosphate is not. This is a machine that burns to stand still."),
    ], label_color=TEAL)
    d.notes(s, "Say 'kinase' and 'phosphatase' out loud and write them on the "
               "board. The word 'kinase' has not appeared in a single deck "
               "from session 4 to session 17 — this room has done ten weeks "
               "of synthetic biology without it, and it is the most common "
               "regulatory mechanism in a eukaryotic cell.\n"
               "Row 4 is the one to pause on. Both enzymes are always on, so "
               "the cycle hydrolyzes ATP continuously even at steady state "
               "when nothing is changing. That is the cost of the sharpness "
               "we are about to buy, and it is the honest version of 'free'. "
               "Do not put a number on it — we have not sourced one.")

    # --- the frame, from a paper -------------------------------------------
    s = d.light()
    d.header(s, "segment 1", "the four numbers")
    d.title(s, "What you are allowed to ask of a switch")
    _paper(d, s, "dueber2007_fig1b", 1.70, 3.30,
                   "Dueber, Mirsky & Lim, Nat Biotechnol 25:660 (2007), Fig. 1b",
                   "Basal activity, induced activity, K_act, and ultrasensitivity (n_H).")
    d.foot(s, "Four parameters, and every one of them is something you will try to set on purpose. Two of them are the whole of today.")
    d.notes(s, "This is the frame for the hour and it comes from a paper "
               "rather than from me. Walk the four: where it sits with no "
               "input, where it saturates, the input that gets you halfway — "
               "their K_act is our half-maximal V₁/V₂ — and how sharply it turns, their n_H.\n"
               "Today is K_act and n_H. Basal and maximal are session 5's "
               "alpha and they are the easy ones.")

    # --- the object, drawn --------------------------------------------------
    s = d.light()
    d.header(s, "segment 1", "the object")
    d.title(s, "A covalent modification cycle")
    _fig(d, s, "s18_cycle", 1.72)
    d.foot(s, "Nothing is made and nothing is destroyed. W + W* is a constant, which no circuit in this course has had before.")
    d.notes(s, "Draw this on the board as well as showing it, because every "
               "piece of algebra in segment 2 refers back to it.\n"
               "The structure is what makes the "
               "mathematics come out differently. Every circuit in this "
               "course so far had a species produced at some rate and removed "
               "at another, and its steady state balanced production against "
               "dilution. This one has a CONSERVED TOTAL. W plus W-star is a "
               "constant. Ask the room what that buys before telling them — "
               "somebody will get it.")

    # --- the knobs, as a question ------------------------------------------
    s = d.light()
    d.header(s, "segment 1", "two minutes  ·  with a neighbor")
    d.title(s, "What can you change?")
    d.rows(s, [
        ("V₁ and V₂", "the two maximal rates. How would you change one? — and what does that cost you?", GREEN),
        ("K_m1 and K_m2", "the two Michaelis constants. Same question.", AMBER),
        ("W_T", "the size of the pool itself. Same question — and this one has a sting in it.", AMBER),
    ], label_color=TEAL)
    d.foot(s, "Two of these three are expression and one is protein engineering. Which is which — and which one can the cell turn by accident?")
    d.to_board(s, "Keep the three answers up. The ledger in segment 4 is checked against them.")
    d.notes(s, "The split you are fishing for: v1 and v2 are EXPRESSION — "
               "clone it, induce it, swap the RBS. That is session 9's easy "
               "axis. K1 and K2 mean mutating the enzyme or swapping a "
               "domain: session 9's hard axis.\n"
               "The third row is the one to wait for. k1 and k2 are K_m "
               "divided by W_T, so expressing more substrate makes BOTH "
               "enzymes MORE saturated at once — an enzyme is saturated when "
               "its substrate sits well above its K_m, and more substrate is "
               "more saturated. So the size of the pool is a sharpness knob, "
               "and it is a promoter.\n"
               "If nobody gets there, push on the units: what does it mean "
               "for a K_m to be measured in units of the pool? Segment 3 "
               "cashes this and segment 4 charges for it.")


# ---------------------------------------------------- 2 · the derivation ---
def _derivation(d):
    d.derivation(
        None, "segment 2", "the model",
        "Two enzymes, one conserved pool",
        # Asides are ONE SHORT LINE. See the note in s19: derivation() switches
        # asides on at pitch >= 0.70 but draws them from y+0.42 to y+0.86, so
        # any run landing in that window overlaps itself. FOUR steps gives a
        # pitch of 1.25 and is clean. This was one run of five until the F4.5
        # review: the old step 5 did three things at once — substituted the
        # conservation law, divided by W_T, and divided by V₂ — and W_T and V₂
        # BOTH disappear in there. Those are the two moves the hour turns on,
        # so they get their own surfaces and the run is split in two.
        [("Michaelis–Menten, twice",
          "forward = V₁W/(K_m1+W)       back = V₂W*/(K_m2+W*)",
          "Session 4's form, one for each direction."),
         ("Steady state is a standoff",
          "V₁·W / (K_m1 + W)  =  V₂·W* / (K_m2 + W*)",
          "Not zero flux. Equal and opposite flux."),
         ("The total is conserved",
          "W + W*  =  W_T",
          "The new thing. Nothing is made or destroyed."),
         ("So there is only one unknown",
          "W = W_T(1 − w)   and   W* = W_T·w,   where w = W*/W_T",
          "Put the conservation law in and W is gone.")],
        board="Point at the cycle you drew in segment 1.",
        note="Step three is the one that is new and should be said as new: "
             "this is the first conservation law in the course. Every steady "
             "state before today was production against dilution.\n"
             "Step four is the substitution, and the thing to notice is that "
             "the system had two unknowns a moment ago and now has one. "
             "Everything from here is bookkeeping on a single number — the "
             "fraction of the pool that is modified.")

    d.derivation(
        None, "segment 2", "the model",
        "What the pool size turns out to be",
        [("Substitute",
          "V₁W_T(1−w)/(K_m1+W_T(1−w))  =  V₂W_T·w/(K_m2+W_T·w)",
          "W_T is a factor in every numerator."),
         ("Divide through by W_T",
          "V₁(1−w)/(k₁+1−w)  =  V₂w/(k₂+w),    k = K_m/W_T",
          "W_T is gone — and it left k behind."),
         ("Divide both sides by V₂",
          "(V₁/V₂)(1−w) / (k₁ + 1 − w)  =  w / (k₂ + w)",
          "V₂ is gone. Only the RATIO survives."),
         ("Cross-multiply",
          "(V₁/V₂)(1−w)(w + k₂)  =  w(1 − w + k₁)",
          "A quadratic in w. That is the whole model.")],
        note="Two things disappear in this run and each one is a result.\n"
             "W_T leaves in step two, but it does not leave the problem — it "
             "leaves as k = K_m/W_T. That is the line the hour turns on. The "
             "Michaelis constants stop being properties of the enzymes and "
             "become properties of the enzymes RELATIVE TO HOW MUCH "
             "SUBSTRATE THERE IS. So a bigger pool means a smaller k, and a "
             "smaller k means a more saturated enzyme. Ask the room which "
             "way that goes before you say it.\n"
             "V₂ leaves in step three, and what survives is V₁/V₂ — a ratio "
             "of two expression levels, which is session 9's easy axis. "
             "Write it as the ratio and keep writing it as the ratio; it is "
             "the whole design argument and a single letter hides it.\n"
             "Five parameters became three. Do not solve the quadratic on "
             "the board — the next surface shows what the authors did.")

    # --- the check against the paper ---------------------------------------
    s = d.light()
    d.header(s, "segment 2", "the check")
    d.title(s, "They solved it. Read the second line carefully.")
    # Eq. 7 runs across BOTH columns of the printed page, so the column crop
    # this slide first used was 2.8in wide on a 13.3in slide and could not be
    # read from the back of the room. Two wide crops, stacked, at the width
    # the equations were set in.
    y = _paper(d, s, "gk1981_eq7_wide", 1.58, 1.42,
               "Goldbeter & Koshland, PNAS 78:6840 (1981), Eq. 7, as printed",
               "The closed form for the modified fraction.")
    d.text(s, "and rearranged — which is the line you just derived:",
           M, y + 0.22, W - 2 * M, 0.34, size=14, italic=True, color=MUTED,
           align="c")
    _paper(d, s, "gk1981_eq8_wide", y + 0.70, 1.05,
           "Goldbeter & Koshland 1981, Eq. 8",
           "The same relation, solved the other way round.")
    d.foot(s, "Eq. 8 is your line. Eq. 7 above it has a typo in the printed paper — it is in the last term under the square root. Find it.")
    d.notes(s, "Let them find it. It is the LAST term under the square root, "
               "which reads 4K2(V2/V2 - 1)(V1/V2) where V1/V2 - 1 is "
               "required. The leading bracket and the denominator are both "
               "correct, so do not point there.\n"
               "Why it has to be V1/V2: that term is the -4ac of the "
               "quadratic you just derived. With a = 1 - V1/V2 and "
               "c = (V1/V2)k2, -4ac = 4k2(V1/V2)(V1/V2 - 1). As printed the "
               "bracket is identically zero, so the discriminant would collapse "
               "to the squared bracket alone.\n"
               "Verified twice: by rendering "
               "page 6841 at 200 dpi and reading it, and by deriving the "
               "quadratic independently from Eq. 8. It is a typesetting error "
               "in a 1981 journal, not a mistake by the authors.\n"
               "Make the argument out loud: a published equation found "
               "defective by a room that did the algebra first is a better "
               "case for doing the algebra than anything I can say about it.")

    # --- the notation bridge, before any plot of ours goes up -------------
    s = d.light()
    d.header(s, "segment 2", "same quantities, two notations")
    d.title(s, "Their symbols and ours, before we plot anything")
    _grid(d, s,
          ["", "Goldbeter & Koshland write", "we write", "and it means"],
          [["the output",
            "W*  (a mole fraction)", "w",
            "the fraction of the pool that is modified, W*/W_T"],
           ["the stimulus",
            "V₁/V₂", "V₁/V₂",
            "the two enzymes' maximal rates, so an expression ratio"],
           ["the saturation",
            "K₁, K₂  (already divided by W_T)", "k₁, k₂",
            "K_m in units of the pool. Small means saturated."]],
          colw=[2.25, 3.55, 1.65, 4.48], top=2.20, gap=0.20)
    d.foot(s, "Their capital K is already our lowercase k — they divided by W_T on page 6841 and then kept the capital letter. Watch for it when you read the paper.")
    d.notes(s, "Thirty seconds, and it prevents an hour of confusion. The "
               "room is about to see our plots next to their figures, and "
               "the only differences are typographic.\n"
               "The third row is the one that bites. Goldbeter and Koshland "
               "define K₁ = K_m1/W_T and then write it as a capital K for "
               "the rest of the paper, so their 'K₁ = K₂ = 10⁻²' is our "
               "k₁ = k₂ = 0.01 and NOT a Michaelis constant of 10 nanomolar. "
               "Every figure caption in this deck says '(their K₁, K₂)' for "
               "that reason.")

    # --- exact result 1 -----------------------------------------------------
    s = d.light()
    d.header(s, "segment 2", "the first exact result")
    d.title(s, "Where the curves cross never moves")
    d.text(s, "four runs of the same model, each with k₁ = k₂, sweeping V₁/V₂.",
           M, 1.58, W - 2 * M, 0.34, size=14, italic=True, color=MUTED,
           align="c")
    _fig(d, s, "s18_response_crossing", 2.02)
    d.foot(s, "V₁/V₂ = 1 is not chosen for convenience. It is where the w² term drops out, so the answer is exact and the same for every curve.")
    d.notes(s, "Say what is held fixed before anything else, because the "
               "figure does not show it: every curve has k₁ = k₂, the "
               "y-axis is w = W*/W_T from step four of the derivation, and "
               "the x-axis is the stimulus. Four curves, four saturations.\n"
               "Then answer the question they should be asking — why V₁/V₂ "
               "= 1? Not for simplicity. The quadratic's leading "
               "coefficient is (1 − V₁/V₂), so at V₁/V₂ = 1 the w² term "
               "vanishes and what is left is linear in w. That is the only "
               "stimulus where the model collapses to something exact, "
               "which is why it is the first thing to ask of it.\n"
               "Do the algebra on the board — four seconds of chalk, and it "
               "turns the figure from an assertion into a confirmation. At "
               "V₁/V₂ = 1 the quadratic reads "
               "(1−w)(w+k₂) = w(1−w+k₁). Expand: w + k₂ − w² − k₂w on the "
               "left, w − w² + k₁w on the right. The w² cancels on both "
               "sides, the lone w cancels, and you are left with "
               "k₂ = w(k₁+k₂).\n"
               "This is the paper's Eq. 9. Verified against the numerical "
               "root to 3.4e-14. At k₁ = k₂ it is one half, which is why "
               "every curve in the figure crosses at the middle.")

    # --- the result the algebra already contained --------------------------
    s = d.light()
    d.header(s, "segment 2", "and look what cancels")
    d.title(s, "The crossing point does not know how big the pool is")
    d.text(s, "w  =  k₂ / (k₁ + k₂)  =  K_m2 / (K_m1 + K_m2)",
           M, 2.24, W - 2 * M, 0.7, size=32, font="head", bold=True,
           color=TEAL, align="c")
    d.text(s, "every k is a K_m over the same W_T, so it divides out of the top and the bottom",
           M, 3.00, W - 2 * M, 0.4, size=14, italic=True, color=MUTED,
           align="c")
    d.rows(s, [
        ("W_T cancels, exactly", "where the curves cross is set by the RATIO of the two Michaelis constants and nothing else. Change the pool a thousandfold and it does not move."),
        ("Which makes the pool useful", "the pool size turns out to set the SHARPNESS, and it does that without disturbing the crossing. It is not free — segment 4 sends the bill."),
        ("And the pool is a promoter", "W_T is how much substrate you express — session 9's EASY axis, and the one the course said you could not use for this."),
    ], top=3.46, label_color=TEAL)
    d.notes(s, "This result was sitting in the algebra from the moment we "
               "had Eq. 9 and it costs one surface to collect.\n"
               "Verified: with K_m1 = 0.3 and K_m2 = 1.7 and the pool varied "
               "a thousandfold, the crossing stays at 0.850000000000 to "
               "twelve figures while the apparent Hill coefficient goes from "
               "1.5 to 249.\n"
               "Do not give away the sharpness result yet — segment 3 earns "
               "it. What they should leave holding is narrower than it "
               "sounds: the pool size moves WITHOUT MOVING THE CROSSING. It "
               "does move the half-maximal point, hard, and segment 4 is "
               "where that bill arrives. Two parameters, two jobs is the "
               "wrong summary and it is the trap posb/protein.py documents.")

    # --- exact result 2 -----------------------------------------------------
    s = d.light()
    d.header(s, "segment 2", "the second exact result")
    d.title(s, "And the half-way point is a ratio of (k + ½)")
    d.text(s, "(V₁/V₂)₅₀  =  (k₁ + ½) / (k₂ + ½)",
           M, 2.30, W - 2 * M, 0.9, size=34, font="head", bold=True,
           color=TEAL, align="c")
    d.rows(s, [
        ("Set w = ½ in the quadratic", "and solve for the ratio. There is no approximation anywhere in this line — it is exact, checked to 1 × 10⁻⁸."),
        ("Read it as k gets small", "both k's go to zero, and the ratio goes to (½)/(½) = 1. The threshold walks to the point where the two enzymes have equal capacity, and stops being yours."),
        ("Hold that thought", "we have not yet shown that small k is what you want. Segment 3 does that, and then this line becomes the bill."),
    ], top=3.45, label_color=TEAL)
    d.notes(s, "Write the substitution on the board rather than showing it — "
               "it is two lines and they should see it happen.\n"
               "Do not editorialize yet. Let them go on thinking the threshold "
               "is a free parameter until segment 4. The surface where "
               "that collapses lands much harder if nobody has been warned.")


# ------------------------------------------- 3 · what saturation buys ---
def _saturation(d):
    s = d.light()
    d.header(s, "segment 3", "how do you measure steepness?")
    d.title(s, "You need a ruler before you can say “sharp”")
    d.rows(s, [
        ("Their definition", "the V₁/V₂ needed to reach 90% modified, divided by the V₁/V₂ needed to reach 10%. Call it R. It is a question you can ask of any dose–response, measured or modeled."),
        ("A hyperbola scores 81", "work it out for Michaelis–Menten and you get exactly 81, every time, for every K. So 81 is the number to beat, and it is not an arbitrary one."),
        ("Converting to a Hill coefficient", "a Hill curve with coefficient n scores 81^(1/n). So n = ln 81 / ln R, and now a cycle with no cooperativity in it can be quoted on the same scale as hemoglobin."),
    ], label_color=TEAL)
    d.foot(s, "This is their Eq. 10 and Eq. 11. posb.protein.sensitivity_index and apparent_hill are those two lines and nothing else.")
    d.notes(s, "Have somebody derive the 81 on the board: 0.9/0.1 divided by "
               "(0.1/0.9) is 81. Doing it makes the rest of the segment "
               "concrete rather than definitional.\n"
               "The conversion lets one number "
               "compare a mechanism that has cooperativity with a mechanism "
               "that has none, and the comparison is the result of the paper.")

    # --- the authors' own response curves ----------------------------------
    s = d.light()
    d.header(s, "segment 3", "1981")
    d.title(s, "Same model, two saturations")
    _paper(d, s, "gk1981_fig1", 1.70, 3.30,
                   "Goldbeter & Koshland, PNAS 78:6840 (1981), Fig. 1",
                   "W and W* against V₁/V₂, at K₁ = K₂ = 1.0 and at K₁ = K₂ = 10⁻².")
    d.foot(s, "There is one modification site in this model and nothing binds anything cooperatively. The inner pair is a switch anyway.")
    d.notes(s, "Theirs first, ours next, and the notebook has them "
               "reproducing it. Saying 'here is the figure from the paper, "
               "now here is the same figure out of the package you will use "
               "tonight' is worth more than either one alone.\n"
               "Ask what changed between the two pairs. The answer is K, and "
               "K is the enzymes' affinity relative to the pool — so the "
               "sharp pair is the one where both enzymes are SATURATED. They "
               "are working flat out and cannot go faster, which is what "
               "makes small changes in the ratio tip the balance so hard.")

    s = d.light()
    d.header(s, "segment 3", "the same sweep, as motion")
    d.title(s, "Nothing is made. The pool just moves.")
    d.movie(s, "figures/build/s18_cycle_sweep.mp4", 0.87, 1.72, 11.60, 4.10,
            caption="Two cycles under one sweep of V₁/V₂. Disc AREA is the amount in each form, so the two areas sum to a constant on every frame.")
    d.foot(s, "Watch the right-hand pair do nothing, do nothing, and then flip. Same sweep, same conservation, different saturation.")
    d.notes(s, "Play it twice. The first time, let them watch. The second "
               "time, narrate.\n"
               "What to say on the second pass: the two discs always add up "
               "to the same area, because W + W* = W_T and nothing is "
               "synthesised or destroyed anywhere in this picture. That is "
               "the structural thing from segment 1, and it is why the "
               "sharpness is surprising — there is no production term to "
               "make steep, and no cooperative binding anywhere.\n"
               "Then the comparison, and start it where they AGREE. At "
               "V₁/V₂ = 1 both pairs are at exactly one half — that is "
               "the crossing from segment 2, it is in the authors' own "
               "Fig. 1 two surfaces ago, and the whole point is that "
               "saturation did not move it. The difference is how fast "
               "they leave: by V₁/V₂ = 1.98 the saturated pair is at "
               "99.0% and the unsaturated one has only reached 72.9%. "
               "Both end in the same place; one of them does it inside "
               "a factor of two and the other takes more than a "
               "decade.\n"
               "Generated from posb.protein by figures/s18_movie.py, so it "
               "is the same function they call in the notebook.")

    s = d.light()
    d.header(s, "segment 3", "why saturation does this")
    d.title(s, "A saturated enzyme does not care how much substrate there is")
    d.rows(s, [
        ("That is what saturated means", "well above K_m, an enzyme runs at V_max. Add more substrate and the rate does not change. Its rate is ZERO ORDER in substrate — and that is where the name comes from."),
        ("So near the middle, both arms are flat", "the kinase is going flat out and so is the phosphatase. Neither one speeds up or slows down as the pool shifts between the two forms."),
        ("Which makes the balance brittle", "nothing pushes back. Whichever V_max is larger wins the whole pool: at k = 0.01 it takes under a 20% change in V₁/V₂ to go from 10% modified to 90%."),
        ("And far from the middle", "one arm has run out of its substrate and drops below V_max. That ends the sharp region and rounds the curve into the plateaus, which conservation fixes at w = 0 and w = 1."),
    ], label_color=TEAL)
    d.foot(s, "Zero order in substrate. No cooperative binding anywhere — the sharpness comes from two enzymes being unable to go any faster.")
    d.notes(s, "Say the words 'zero order' and write them. This is the first "
               "time they appear today, and the session-4 quotation two "
               "surfaces from now uses them — so they get defined here, "
               "before the room meets them in someone else's sentence.\n"
               "This is the causal link of the whole hour and it is one "
               "sentence: a saturated enzyme's rate is independent of its "
               "substrate concentration, so near the balance point neither "
               "enzyme responds to the pool shifting, so there is nothing to "
               "restore the balance.\n"
               "Contrast it with cooperativity out loud. In session 9 the "
               "sharpness came from molecules binding each other. Here "
               "nothing binds anything. Same curve, different cause.")
    s = d.light()
    d.header(s, "segment 3", "ours")
    d.title(s, "How sharp, as a function of how saturated")
    _fig(d, s, "s18_apparent_hill", 1.72)
    d.foot(s, "Derived, not measured — every point on this line is a property of the quadratic. At k = 0.01 the apparent Hill coefficient is 26.1.")
    d.notes(s, "Kind matters here and should be said: this is a curve "
               "computed from an equation, and there is not one measurement "
               "anywhere in Goldbeter and Koshland. They say so themselves on "
               "page 6844.\n"
               "Below about k = 0.1 the scaling is close to n ~ k^-0.9, so "
               "down there you buy sharpness nearly in proportion to how "
               "saturated you can get the pair. Above it the curve flattens "
               "towards n = 1, which is the hyperbolic limit — and you can "
               "see it flatten on the screen, so do not say \"across the "
               "range\". Over the whole plotted axis the slope averages "
               "-0.57. There is no threshold effect and no magic point: it "
               "is a smooth trade, and every point on the line is "
               "reachable.")

    # --- the promise from session 4, discharged ----------------------------
    s = d.dark()
    d.header(s, "segment 3", "a debt from 8 September")
    d.title(s, "Session 4 promised you this number")
    d.text(s, "“Zero-order ultrasensitivity in a phosphorylation cycle gives an "
              "apparent n above 20 from ONE site.”",
           M, 2.20, W - 2 * M, 1.1, size=24, italic=True, color=MINT)
    d.text(s, "— session 4, 8 September, in a ConcepTest resolution",
           M, 3.32, W - 2 * M, 0.34, size=16, color=SILVER)
    d.rows(s, [
        ("It is true", "26.08 at k₁ = k₂ = 0.01, from their Eq. 10. One modification site. No cooperative binding anywhere in the model."),
        ("It was promised to session 13", "which did not carry it. You are getting it here instead."),
    ], top=4.05, label_color=CYAN, body_role="body")
    d.notes(s, "Say this plainly and briefly. A number was asserted to this "
               "room in week two against a session that turned out not to "
               "contain it, and the right response is to hand over the number "
               "and name the gap rather than let it pass.")

    # --- the conversion chart, and its edge --------------------------------
    s = d.light()
    d.header(s, "segment 3", "the exchange rate")
    d.title(s, "What that is worth in Hill coefficients")
    _paper(d, s, "gk1981_fig2", 1.62, 4.10,
                   "Goldbeter & Koshland 1981, Fig. 2",
                   "Their R against a Hill coefficient (dashed), and R against K for three cases (solid).")
    d.foot(s, "Their own prose says a cycle at K = 10⁻² matches “a Hill coefficient greater than 13”. Their Eq. 10 gives 26.08. Look at where the axis ends.")
    d.notes(s, "Let somebody find it. The n_H axis runs 2 to 12 and stops, "
               "and at K = 10 to the minus 2 the curve bottoms out past the "
               "right-hand edge. Their graph ran out of axis.\n"
               "Be careful how you put it: the axis range is a fact and you "
               "can see it; that it explains their wording is an inference "
               "and the paper does not say so. Offer it as an inference.\n"
               "So: evaluate the closed "
               "form, do not read the value off the figure. Including when "
               "the figure is the authors' own.")

    # --- what has actually been built, BEFORE the ladder tabulates it -----
    s = d.dark()
    d.header(s, "segment 3", "nobody has reached 26")
    d.title(s, "Two ways people have really built one")
    d.rows(s, [
        ("Autoinhibition", "stack repressing domains onto a catalytic one, so the output only switches on when enough of them are displaced at once. Dueber, in a protein called N-WASP."),
        ("Recruitment", "tether a modulator to a scaffold so it acts on the pathway, and let a competitor displace it. Bashor, in the yeast mating pathway."),
        ("Neither is zero-order", "neither one saturates a cycle. They are two more routes to the same destination, and they are the routes with measured numbers on them."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "The next three surfaces are where the ladder's measured rows come from. Then we put all of them on one scale.")
    d.notes(s, "This surface exists because the ladder two slides from now "
               "quotes four measured Hill coefficients, and until today the "
               "room had met none of the constructs they came from.\n"
               "Say plainly that we are leaving zero-order for a moment. "
               "These are different mechanisms — autoinhibition and "
               "recruitment — and the reason to show them is that they are "
               "what people have actually built, against a theory that "
               "permits 26.")

    s = d.light()
    d.header(s, "segment 3", "a different cycle, in a real protein")
    d.title(s, "A switch held OFF by part of itself")
    _paper(d, s, "dueber2003_fig1", 1.68, 1.76,
           "Dueber, Yeh, Chak & Lim, Science 301:1904 (2003), Fig. 1",
           "N-WASP: autoinhibited, then activated when an input displaces the autoinhibition.")
    d.rows(s, [
        ("The natural switch", "its output domain drives actin polymerization on its own. Two of its own domains fold back and hold it off."),
        ("Which makes it a gate", "Cdc42 and PIP₂ each displace one, and they act synergistically — so the authors call it an AND gate."),
        ("And it is reprogrammable", "they swapped the natural autoinhibition for a PDZ domain and its ligand. New input, same output. K_act = 50 µM."),
    ], top=4.06, bottom=6.52, label_color=TEAL)
    d.notes(s, "This is the allosteric cycle, and the word 'allosteric' has "
               "not appeared in a single deck from session 1 to 17 even "
               "though the syllabus promises allosteric switches. Say it "
               "and define it: a molecule binds HERE and changes what "
               "happens THERE.\n"
               "Note the shape of the cycle against the one on the board. "
               "Ours moves a phosphate between two forms of a conserved "
               "pool. This one moves a domain on and off its own output "
               "domain. Different chemistry, same two-state structure, and "
               "both are switches.\n"
               "The AND gate is worth thirty seconds — it is session 16's "
               "material arriving in a protein, and it is a real one rather "
               "than a designed one. The phrase is the authors' own.\n"
               "K_act = 50 µM is their p. 1904, verbatim: "
               "'Half-maximal activation (Kact) required 50 µM "
               "input.' If anyone asks about the ligand affinity, the 8 µM "
               "in the legend is the INPUT peptide; the authors separately "
               "tighten the INTERNAL autoinhibitory ligand to 8 µM on "
               "p. 1906. Different ligand, same number.\n"
               "And the hedge I want them to hear, p. 1906: tightening that "
               "internal ligand gave a well-behaved AND gate in one "
               "architecture (H14) and destroyed the behaviour in another "
               "(C11). The same affinity, two contexts, two outcomes — "
               "which is Thursday's thesis arriving a session early, in a "
               "paper from 2003.\n"
               "Then set up the next slide: panel B is the move. They "
               "REPLACED the natural autoinhibitory module with a "
               "heterologous one, which is what makes the next figure "
               "possible — once the module is a part you choose, you can "
               "choose how many.")

    s = d.light()
    d.header(s, "segment 3", "the first route  ·  autoinhibition")
    d.title(s, "Now add more of them, and the switch gets steeper")
    _paper(d, s, "dueber2007_fig2b", 1.66, 3.30,
           "Dueber, Mirsky & Lim, Nat Biotechnol 25:660 (2007), Fig. 2b",
           "Three synthetic switches built on N-WASP: one, three and five SH3 autoinhibitory modules.")
    d.foot(s, "One module gives n_H = 1.0 — a hyperbola. Three gives 2.7. Five gives 3.9. All measured, from actin polymerization assays.")
    d.notes(s, "The mechanism in one sentence: the catalytic domain is held "
               "off by SH3 modules, and the input has to displace them. With "
               "one module that is a simple competition and the response is "
               "hyperbolic. With five, several have to let go before "
               "anything happens, and that is what bends the curve.\n"
               "So this IS cooperativity — but it is cooperativity between "
               "domains on one chain, engineered by adding modules, not "
               "inherited from a protein that already had it. That is "
               "session 9's hard axis made soft, by a completely different "
               "route from ours.\n"
               "The design trade-off, in their words: interactions too weak "
               "and the basal activity is high; too strong and the switch "
               "cannot be activated at all. Their five-strong construct, "
               "A.5.5a, is dead.")

    s = d.light()
    d.header(s, "segment 3", "the vocabulary for the next surface")
    d.title(s, "Scaffolds, modulators, recruitment")
    d.rows(s, [
        ("A scaffold protein", "a chassis with docking sites on it. It does no catalysis; it holds the enzymes of a pathway next to each other. Ste5 in the yeast mating pathway is the one here."),
        ("A modulator", "an enzyme you tether to a spare site on that chassis — positive if it drives the pathway, negative if it shuts it down."),
        ("Recruitment", "tethering raises the LOCAL concentration enormously. That is the whole mechanism: you have not changed any enzyme, only where it sits."),
        ("And the knob", "which site, and how tightly. Bashor used leucine zippers of three affinities — K_d = 6, 40 and 810 nM — to set how hard a modulator is held."),
    ], label_color=TEAL)
    d.foot(s, "Nothing in this course has used a scaffold before. Thirty seconds here and the next figure reads in half a minute.")
    d.notes(s, "A grep of every deck from session 1 to 17 finds zero uses of "
               "'modulator', zero of 'allosteric', and 'scaffold' only in "
               "the teaching sense of scaffolded practice. The room has no "
               "vocabulary for the next slide, which is the strongest "
               "MEASURED evidence in the hour.\n"
               "Local concentration is the idea to land. Tethering two "
               "molecules to the same chassis is the same as raising their "
               "concentration by orders of magnitude, without expressing "
               "any more of either one.")

    s = d.light()
    d.header(s, "segment 3", "and now, two people who built one")
    d.title(s, "One toolkit, four behaviors")
    # The whole of Fig. 4 is four panels stacked in a journal column: at a
    # 0.72 aspect it renders 3.0in wide here and none of the four time courses
    # can be read. These are the two that carry this session's argument.
    y = _paper(d, s, "bashor2008_fig4cd", 1.55, 3.30,
               "Bashor et al., Science 2008, Fig. 4, panels C and D",
               "Delay, and the ultrasensitive switch. Circuit on the left, measured time course on the right.")
    d.text(s, "The same scaffold also gives a PULSE GENERATOR and an "
              "ACCELERATOR — WT-maximal output in under 20 min against about "
              "75 min for wild type.",
           M, y + 0.20, W - 2 * M, 0.40, size=14, italic=True, color=MUTED,
           align="c")
    d.foot(s, "The gain is set by WHERE a modulator is recruited and with what affinity: K_d = 6, 40 and 810 nM across these circuits.")
    d.notes(s, "Here is the hour's thesis in its strongest measured form. "
               "Four qualitatively different dynamics out of one scaffold "
               "and one set of parts, selected by recruitment.\n"
               "Do not read panel D's wiring off this surface — it is the "
               "superseded version, and the next slide is why.")

    s = d.light()
    d.header(s, "segment 3", "read to the last page")
    d.title(s, "The panel you just saw was corrected in 2008")
    _paper(d, s, "bashor2008_fig4d_corrected", 1.62, 3.05,
           "Science, Corrections & Clarifications, 22 August 2008",
           "The reissued panel D. The positive modulator's zipper is black, and the label now reads high-affinity.")
    d.foot(s, "The switch works by DISPLACEMENT, so the affinity difference is the mechanism — and the published panel drew both zippers the same.")
    d.notes(s, "Worth the minute. Science reissued panels B and D five "
               "months after publication and said exactly what was wrong: "
               "in 4D the positive modulator's leucine zipper should have "
               "been black because it binds more tightly than the negative "
               "modulator's, K_d 6.1 against 41 nM, and the label should "
               "have read high-affinity. In 4B both zippers should have "
               "been grey, because there both modulators carried identical "
               "zippers and the printed label wrongly said high affinity.\n"
               "The teaching point is not that the authors erred. It is "
               "that the uncorrected figure CONTRADICTS the mechanism it "
               "illustrates — if the two zippers bind equally, nothing "
               "displaces anything — and that you only find this by reading "
               "to the last page of the PDF. Tell them the erratum also "
               "amends two sentences of the main text and the supplementary "
               "tables.")

    # --- the ladder ---------------------------------------------------------
    s = d.light()
    d.header(s, "segment 3", "on one scale")
    d.title(s, "Five switches, one ruler, two kinds of number")
    _grid(d, s,
          ["", "apparent n_H", "mechanism", "kind"],
          [["Wild-type yeast mating pathway\nBashor 2008, Fig. 4D", "1.21 ± 0.06",
            "none engineered in", "measured"],
           ["Bashor's enhanced switch\nBashor 2008, Fig. 4D", "2.84 ± 0.19",
            "a modulator on a scaffold", "measured"],
           ["Hemoglobin\nvia Goldbeter & Koshland 1981", "≈ 2.9",
            "cooperative binding, four sites", "measured"],
           ["Dueber's best construct\nDueber 2007", "3.9",
            "five autoinhibitory domains", "measured"],
           ["One covalent cycle at k = 0.01\nGoldbeter & Koshland, Eq. 10", "26.1",
            "saturation. One site. Nothing cooperative.", "DERIVED"]],
          colw=[4.55, 1.95, 3.9, 1.53], top=2.18, gap=0.14)
    d.foot(s, "The last row is a property of an equation; the four above it are properties of molecules. Nobody has built the last row.")
    d.notes(s, "Do not let the 26 look like a win. It is what the equations "
               "permit; the best measured engineered protein switches reach "
               "about 2.8 to 3.9, and that gap is a real open question to "
               "leave the room holding.\n"
               "Reasons the gap exists, and segment 4 supplies two of them: "
               "you need BOTH enzymes saturated, and real enzyme "
               "concentrations are not negligible against the substrate pool. "
               "Invite guesses before you move on.")


# ------------------------------------------------ 4 · what it costs ---
def _cost(d):
    s = d.light()
    d.header(s, "segment 4", "the bill")
    d.title(s, "Now go back and look at the threshold")
    d.text(s, "across: how sharp you want it.    up: every half-maximal V₁/V₂ still reachable.",
           M, 1.56, W - 2 * M, 0.34, size=14, italic=True, color=MUTED,
           align="c")
    _fig(d, s, "s18_threshold_tradeoff", 1.98)
    d.foot(s, "At apparent n = 32 every reachable threshold lies within 3.4% of 1, whatever affinities you choose. The sharper you make it, the less you can place it.")
    d.notes(s, "This is the surface segments 2 and 3 were set up for, "
               "and it should land as a reversal. The half-maximal ratio LOOKS like a free "
               "parameter — it is a ratio of two things you can choose — and "
               "it is not, because it is a ratio of (k + one half) and the "
               "halves dominate as the k's shrink.\n"
               "So: the protein layer buys you sharpness the transcriptional "
               "layer cannot, and the transcriptional layer still has to set "
               "the threshold, because what places the switch is the ratio V1/V2, "
               "which is an EXPRESSION RATIO. You need both layers. If "
               "anybody came in thinking today was an argument for abandoning "
               "promoters, this is where that dies.")

    s = d.light()
    d.header(s, "segment 4", "and it belongs to the pair")
    d.title(s, "Saturate one enzyme and you have almost nothing")
    d.text(s, "three runs, each pinning one enzyme at k₁ and relaxing the other.",
           M, 1.56, W - 2 * M, 0.34, size=14, italic=True, color=MUTED,
           align="c")
    _fig(d, s, "s18_both_saturated", 1.98)
    d.foot(s, "Follow the top curve: k₁ pinned at 0.005, k₂ relaxed from 0.005 to 0.5, and apparent n falls from 50.8 to 3.2. The property is in neither enzyme.")
    d.notes(s, "Thursday's orthogonality lesson in a new place. The sharpness "
               "is a property of the PAIR, so characterizing your kinase "
               "alone tells you nothing, and swapping in a better phosphatase "
               "can destroy a switch that worked.\n"
               "Ask what this means for a parts registry. You cannot put a "
               "number on the kinase in the catalogue, because the number "
               "does not belong to the kinase.")

    s = d.light()
    d.header(s, "segment 4", "the assumption, violated by its own authors")
    d.title(s, "And it needs the enzymes to be scarce")
    d.text(s, "the same cycle at k₁ = k₂ = 10⁻¹, at three enzyme concentrations.",
           M, 1.54, W - 2 * M, 0.34, size=14, italic=True, color=MUTED,
           align="c")
    _paper(d, s, "gk1981_fig3", 1.94, 3.10,
                   "Goldbeter & Koshland 1981, Fig. 3",
                   "The same cycle at K = 10⁻¹, with enzyme at ≪ W_T, at 0.1 W_T, and at W_T.")
    d.foot(s, "The dashed pair is enzyme at the same concentration as substrate: the swing collapses from 0→1 to about 0.12→0.27. Substrate in a complex cannot move.")
    d.notes(s, "They checked their own assumption in the same paper, which "
               "is worth noticing out loud.\n"
               "Read the three pairs with the room. Solid: enzyme much less "
               "than W_T, which is what every line of our derivation "
               "assumed, and the switch is intact. Dash-dot: enzyme at 10% "
               "of W_T, already softening. Dashed: enzyme equal to W_T, and "
               "there is no switch left.\n"
               "The mechanism is SEQUESTRATION, and name it, because it is "
               "about to become a through-line: a molecule held by something "
               "that is not its target is a molecule that is not available. "
               "Here it is substrate bound up in enzyme–substrate complex.")

    # --- the three-session mechanism ---------------------------------------
    s = d.dark()
    d.header(s, "segment 4", "name it once, use it three times")
    d.title(s, "One mechanism, three sessions")
    d.rows(s, [
        ("today", "a transcription factor held by DECOY SITES that are not its promoter — and the enzyme–substrate complex you just saw. Titration."),
        ("Thursday — session 19", "a ribosome held by every other mRNA in the cell. You cannot give your circuit its own ribosomes."),
        ("session 21", "an upstream regulator held by its own downstream targets. Retroactivity: the thing reading your signal loads it."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "In all three the molecule is held by something that is not its target, so it is not available to do its job.")
    d.notes(s, "Decoy titration was promised in the same session-4 note as "
               "zero-order ultrasensitivity and has also been taught nowhere. "
               "This one surface discharges it, because it is "
               "the same sequestration you just met in Fig. 3.\n"
               "Say the three out loud as one sentence, and say that it is one "
               "mechanism, so they carry it as one thing.")

    # --- the ledger ---------------------------------------------------------
    s = d.light()
    d.header(s, "segment 4", "the design ledger")
    d.title(s, "So what do you turn?")
    d.rows(s, [
        ("Where it crosses", "the ratio K_m1 : K_m2. A property of the two proteins, and the pool size cannot move it.", GREEN),
        ("How sharp", "lower k₁ AND k₂ together. A tighter-binding pair, which is hard — or MORE substrate, since k = K_m/W_T. That one is a promoter.", GREEN),
        ("Where it fires", "the expression ratio V₁/V₂. Promoters and RBSs again. You cannot get it from the affinities.", GREEN),
        ("What you cannot have", "sharpness and a free threshold. Driving k down walks V₁/V₂ at half-maximum to 1 and pins it there.", RED),
        ("What you are paying", "ATP, continuously, even at rest. Both enzymes run whether or not anything is changing.", AMBER),
    ], label_color=TEAL)
    d.foot(s, "Two of the three knobs are promoters. The parameter session 9 said you could only shop for is the one you set by expressing more substrate.")
    d.notes(s, "Point at the board. If anybody put the pool size in the "
               "sharpness row back in segment 1, say whose it was.\n"
               "This is the answer to session 9's slide and it should be said "
               "as one. Gardner could not tune cooperativity, so he chose a "
               "protein that already had it. Here you tune the equivalent "
               "parameter with a promoter on the substrate, and the crossing "
               "point does not move while you do it.\n"
               "Then the catch, which is Thursday. Expressing more substrate "
               "is not free, so the cheapest knob on this list is the one "
               "session 19 takes away.")


# --------------------------------------------------- 5 · Mishra 2021 ---
def _mishra(d):
    s = d.dark()
    d.header(s, "segment 5", "from one cycle to a network of them")
    d.title(s, "Now wire two of them against each other")
    d.rows(s, [
        ("What you have", "one covalent cycle. A sharp, fast response, with a sharpness you set by the pool and a threshold you set by expression — and the two are coupled."),
        ("What you do next", "take two cycles and have each one shut the other off. Mutual repression — the move from session 8, in a medium that did not exist for us until this morning."),
        ("And what you get", "a toggle. Same topology, same phase plane, same stability test. The molecules are completely different and the clock runs in seconds."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "That is the paper you read for today.")
    d.notes(s, "This bridge matters because segment 4 ended on a single "
               "cycle and segment 5 opens on an eleven-element network. It "
               "is a real conceptual step, not a change of example, and "
               "without it the room experiences the paper as a new topic.\n"
               "Ask the question before you answer it: you have a sharp "
               "switch — what would you build out of two of them?")

    s = d.light()
    d.header(s, "segment 5", "the reading")
    d.title(s, "A toggle switch with no promoter in it")
    d.rows(s, [
        ("What they built", "“a bistable toggle switch in Saccharomyces cerevisiae with a regulatory network based solely on reversible protein-protein phosphorylation.”"),
        ("Out of what", "11 phospho-in and phospho-out elements: chimeric fusions they made, plus endogenous proteins of the high-osmolarity MAPK pathway."),
        ("The topology", "two branches arranged so that they repress each other. Mutual cross-repression, and two inputs to flip it."),
        ("Why it was hard", "“engineering … protein networks capable of switching state in seconds has not yet been achieved.” Transcriptional toggles run in minutes to hours."),
    ], bottom=6.38, label_color=TEAL)
    # The full author list appears once in this deck and this is the slide for
    # it: the figure slides are narrow and a wrapped citation walks into the
    # foot. Folding it into the assignment line puts the authors, the journal
    # and the date the paper went out on one line.
    d.assigned_on(M, 6.50, W - 2 * M, s,
                  prefix="Mishra, Bepler, Teague, Berger, Broach & Weiss, "
                         "Science 373 (2021) — you read this for today")
    d.notes(s, "Construct before result, as always. Rows 1 and 4 are their "
               "words and the quotation marks are real; rows 2 and 3 are "
               "mine.\n"
               "The topology row is the one to connect: mutual "
               "cross-repression IS Gardner's toggle. Same wiring diagram, "
               "same phase plane, same wedge. Different molecules entirely.")

    s = d.light()
    d.header(s, "segment 5", "the topology")
    d.title(s, "Two arms, each shutting off the other")
    _paper(d, s, "mishra2021_fig3a", 1.70, 3.00,
           "Mishra et al., Science 2021, Fig. 3A",
           "The engineered network as a Boolean logic diagram.")
    d.foot(s, "Same topology as Gardner's Fig. 1, drawn as logic instead of as DNA. Mutual repression, two inputs, two states — and not one promoter in the loop.")
    d.notes(s, "Put this up before the pathway diagram and ask what it is. "
               "Somebody will say toggle switch, and they will be right: it "
               "is the wiring diagram from session 9 with different nouns "
               "on it.\n"
               "Get that recognition BEFORE the next surface, because the "
               "next surface is a real signalling pathway with twenty "
               "protein names on it and the topology disappears into the "
               "biochemistry if they have not seen it first.")

    # ----------------------------------------------------------------
    # The staircase from "here is a logic diagram" to "here is a
    # twenty-protein pathway". Ported from Adam's 2025 Lecture 24
    # (Classes/PoSB/2025/Lectures/2025-12-02-Lecture 24-Protein-Circuits-
    # and-more.pptx, slides 7-11), which built it in exactly this order and
    # which the 2026 deck had skipped -- it went straight from Fig. 3A to
    # Fig. 3B, and the pathway diagram arrives as a wall of protein names
    # with no reason to expect any particular one of them.
    #
    # This is also the specific thing Adam asked for on 25 October: "step
    # through the path to elucidate where it is implementing architectures
    # we have seen before but with different biochemistry."
    # ----------------------------------------------------------------
    s = d.light()
    d.header(s, "segment 5", "frame  ·  why these gates compose at all")
    d.title(s, "Phospho in, phospho out")
    d.rows(s, [
        ("the condition for composing anything",
         "a gate is composable only if what comes OUT of it is the same KIND of thing that goes in. Otherwise every junction needs a translator, and Thursday told you what junctions cost."),
        ("their move, and it is the whole design",
         "make the input and the output both a PHOSPHORYLATION STATE. The output of one gate is already the input to the next, with nothing in between.", CYAN),
        ("which is why this is a circuit and not a cascade",
         "you can chain them without designing an interface each time. A transcriptional part has the same property — protein in, protein out — bought in a different currency and at a different speed."),
    ])
    d.foot(s, "Eleven elements, all phospho-in and phospho-out. That phrase in the abstract is a specification, not a description.")
    d.notes(s, "Ask the room what makes a part composable before you give "
               "this. Somebody will say standard interfaces, which is "
               "Thursday's answer and is right.\n"
               "The point to land is that matching the currency is a DESIGN "
               "DECISION they made, not a property phosphorylation happens "
               "to have. They could have built gates whose output was "
               "localization and whose input was phosphorylation, and then "
               "nothing would chain.")

    s = d.light()
    d.header(s, "segment 5", "frame  ·  how many kinds of gate you need")
    d.title(s, "Two gates are enough, and you already know why")
    d.rows(s, [
        ("session 16 gave you this argument",
         "NOR is universal. Wire enough NOR gates together and you can build any Boolean function at all, which is why Cello needs only one gate type in its library."),
        ("here the complete set is OR and NOT",
         "also functionally complete. So if you can build those two out of phosphorylation, you can build ANY logic out of phosphorylation — a toggle included.", CYAN),
        ("and the engineering question narrows",
         "it stops being “how do I make a toggle out of proteins”, which is open-ended, and becomes “how do I make an OR and a NOT out of phosphorylation”. Two concrete problems."),
    ])
    d.foot(s, "Same completeness argument as session 16, a different complete set, and a completely different physical substrate.")
    d.notes(s, "This is the architecture-transfer beat and it is the reason "
               "the session is positioned here rather than next to session "
               "9.\n"
               "They proved NOR universality for themselves in session 16 "
               "from a DNA layout. The argument does not care what the gate "
               "is MADE of -- that is what being a logical argument means. "
               "Say that out loud. It is the single most transferable idea "
               "in the hour.\n"
               "If somebody asks why OR and NOT rather than NOR: NOT of an "
               "OR is a NOR, so the sets are interconvertible. They chose "
               "the pair that was easiest to build in this chemistry, which "
               "is the right reason to choose.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  the two gates, physically")
    d.title(s, "An OR is a shared substrate. A NOT is a change of address.")
    d.rows(s, [
        ("OR, by pathway convergence",
         "two different upstream kinases phosphorylate the SAME target. Either input alone is enough to switch it. The convergence IS the OR — there is no new part, just a substrate that two pathways both reach.", CYAN),
        ("NOT, by phospho-activated localization",
         "HOG1 moves into the nucleus when it is phosphorylated. Send the output somewhere the next gate cannot reach it and you have inverted the signal. The gate is a change of address, not a change of amount.", RED),
        ("and the inputs are chimeras they built",
         "CRE1-HKRR and the rest — a sensing domain cut from one protein and fused onto a relay the cell already runs. Thursday's part-swapping, in protein, with the same question about whether the join behaves."),
    ])
    d.foot(s, "Neither gate is a new molecule. One is a wiring choice and the other is a trafficking choice — both made out of what the pathway already does.")
    d.notes(s, "This is the surface that makes the next one readable, so do "
               "not rush it.\n"
               "The OR is worth dwelling on because it is almost free. In "
               "transcription, an OR costs you a promoter with two operators "
               "and a lot of characterization. Here, two kinases that happen "
               "to share a substrate ARE an OR, and signalling pathways are "
               "full of shared substrates. That is an argument that protein "
               "circuits might be CHEAPER to build than transcriptional "
               "ones, which is not the direction people expect.\n"
               "The NOT is the clever one and it has no transcriptional "
               "analogue in this course. Nothing is degraded and nothing is "
               "repressed -- the molecule is moved out of reach. Ask them "
               "what the equivalent would be for a transcription factor; "
               "the answer is sequestration, which is Tuesday's session.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  composing the two into a state")
    d.title(s, "Write the toggle as pseudocode first")
    d.rows(s, [
        ("go back to the boxes on Fig. 3A",
         "they were there all along: if IP, set the YPD1 branch HIGH and the PBS2 branch LOW. If sorbitol, the other way round. That is the whole specification."),
        ("which is the machine from session 9",
         "two branches, each suppressing the other, and one inducer per branch. You wrote this specification for LacI and cI, and you drew its phase plane in session 8. Nothing about it is new.", CYAN),
        ("what IS new is the last step",
         "mapping each line of that specification onto a real protein. Every name on the next slide is one line of this, implemented in the cell's own osmotic-stress pathway."),
        ("and the first engineering act was deletion",
         "Δhog1 Δhot1 Δfus3 Δkss1 Δsln1 — five genes removed before anything was built, so that nothing else in the cell answers the inputs.", RED),
    ])
    d.foot(s, "Specification, then completeness, then gates, then mapping. That is the whole method, and it is the same one Cello automates for DNA.")
    d.notes(s, "Put the pseudocode up and ask what it is before you tell "
               "them. You want somebody to say toggle.\n"
               "Then walk the correspondence explicitly, because it is the "
               "payoff of three sessions: two branches are the two genes, "
               "mutual suppression is the mutual repression, IP and sorbitol "
               "are IPTG and heat, and the two stable branch states are the "
               "two stable points of the phase plane.\n"
               "The deletion row is the one students will not anticipate and "
               "it is the honest part of the story. You do not build a "
               "protein circuit in a cell that is already using those "
               "proteins -- you clear the ground first. That is Thursday's "
               "orthogonality problem arriving with a scalpel instead of a "
               "part registry, and it is the cost that does not appear "
               "anywhere in the logic diagram.")

    s = d.light()
    d.header(s, "segment 5", "the object")
    d.title(s, "And this is what it is made of")
    _paper(d, s, "mishra2021_fig3b", 1.62, 4.10,
                   "Mishra et al., Science 2021, Fig. 3B",
                   "Membrane, cytosol and nucleus. Every arrow is a phosphotransfer.")
    d.foot(s, "SHO1, YPD1, SSK1, SSK2, PBS2 — the cell's own osmotic stress pathway. HOG1, HOT1 and SLN1 are DELETED, and come back only inside the chimeras.")
    d.notes(s, "Spend real time here. This is the biology and it is the "
               "reason the session is worth an hour.\n"
               "Two inputs, two branches, and the paper says which drives "
               "which: \"administering IP sets the YPD1 branch high, "
               "administering sorbitol sets the PBS2 branch high.\" Sorbitol "
               "is sensed at SHO1 and runs through CDC42, STE20, STE50 and "
               "STE11 to PBS2. IP acts on the chimera CRE1-HKRR and relays "
               "through YPD1 to SSK1. Each branch represses the other, and "
               "that is the toggle.\n"
               "Then point at the genotype printed on the figure: delta-hog1 "
               "delta-hot1 delta-fus3 delta-kss1 delta-sln1. Five genes "
               "deleted BEFORE anything was built, and three of the names on "
               "this diagram — HOG1, HOT1, SLN1 — are among them; they "
               "re-enter only as domains inside the fusions. Engineering a "
               "protein circuit means deleting the cross-talk first, which is "
               "Thursday's orthogonality problem in a new medium.")

    s = d.light()
    d.header(s, "segment 5", "the result")
    d.title(s, "Thirty seconds of input. The state stays.")
    _paper(d, s, "mishra2021_fig4a", 1.62, 4.10,
                   "Mishra et al., Science 2021, Fig. 4A",
                   "Nuclear fluorescence after a 30-s sorbitol pulse (top) and a 30-s IP pulse (bottom). n = 100 cells.")
    d.foot(s, "Nuclear localization stabilizes by 2 min and holds for 240 min, across cell division. Gardner's toggle needed a six-hour induction — his Fig. 4c.")
    d.notes(s, "Two numbers, and they are the paper's: the input lasted "
               "thirty seconds, and nuclear localization \"stabilized by "
               "2 min, remained constant over 240 min, and was maintained "
               "across cell division.\" That is memory, and it is the two "
               "stable points of session 8's phase plane seen directly.\n"
               "Then the comparison. Same topology, same analysis, timescale "
               "faster by orders of magnitude, and the paper reports "
               "bistability holding across cell divisions. This is the answer "
               "to the question session 2 asked on 1 September: the medium "
               "sets the clock. Transcription is slow because you have to "
               "make a protein; phosphorylation is fast because the protein "
               "is already there and you are only moving a phosphate onto it.")

    s = d.light()
    d.header(s, "segment 5", "the control that earns it")
    d.title(s, "Break the feedback and nothing latches")
    _paper(d, s, "mishra2021_fig4c", 1.62, 4.10,
                   "Mishra et al., Science 2021, Fig. 4C",
                   "Single-cell traces after a 2-s pulse. Above: the toggle with its feedback deleted. Below: the full network.")
    d.foot(s, "Two seconds of input, a permanent state change — and only when the feedback is intact. The top row is why you believe the bottom row.")
    d.notes(s, "Make them read the top row first. The defective toggle never "
               "latches: at the highest dose it rises and decays straight "
               "back. The full network latches at 100 micromolar and holds "
               "flat.\n"
               "Be careful with the word ultrasensitivity here, because the "
               "paper uses it for a different quantity than Goldbeter and "
               "Koshland do. Theirs is STEEPNESS — a Hill coefficient. "
               "Mishra's claim is about THRESHOLD: the toggle responds to "
               "concentrations that 'do not elicit observable responses in "
               "similar networks lacking feedback regulation'. Mishra report "
               "no Hill coefficient at all. Say which one is meant.\n"
               "Ask what the deletion strain is FOR. It is the control that "
               "separates 'the pathway responds' from 'the circuit we built "
               "is bistable', and without it there is no result.")

    s = d.dark()
    d.header(s, "segment 5", "the obvious reading, and why it fails")
    d.title(s, "So did zero-order ultrasensitivity build this switch?")
    d.rows(s, [
        ("The reading you would expect", "Mishra's toggle is sharp because its modification cycles are saturated. That is this morning's mechanism, and it is the one you came in holding."),
        ("What their control says", "break the feedback and nothing latches, at any dose. The bistability needs the LOOP. Saturation of a single cycle does not produce it on its own."),
        ("And the word moves too", "their ultrasensitivity claim is about the lowest concentration that works, not about steepness. They report no Hill coefficient."),
        ("So where does today land", "zero-order is a floor you can build on, not the whole story. One cycle gives you a sharp response; two cycles wired against each other give you a state."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "Two routes to a sharp switch are now in the room — saturation of one cycle, and feedback around a network. They are not the same mechanism.")
    d.notes(s, "This surface exists because the hour's thesis does not quite "
               "close against the evidence, and that is worth teaching "
               "rather than hiding.\n"
               "The honest position: Goldbeter and Koshland prove that one "
               "saturated cycle can manufacture an apparent Hill coefficient "
               "of 26. Mishra build a fast bistable switch out of such "
               "cycles, but what makes it bistable is the cross-repression, "
               "and they never measure a Hill coefficient. Both things are "
               "true and the session should say so.\n"
               "If a 247 student asks whether the zero-order mechanism did "
               "any work in the paper, the answer is that it is what lets "
               "each arm act like a switch rather than a dimmer. That is "
               "necessary for the loop to latch cleanly, and it is not "
               "sufficient.")

    s = d.light()
    d.header(s, "segment 5", "line by line")
    d.title(s, "Gardner's toggle, with the biochemistry swapped out")
    _grid(d, s,
          ["", "session 9 — Gardner", "today — Mishra"],
          [["the two states",
            "concentration of two repressors",
            "phosphorylation state of two branches"],
           ["what represses",
            "LacI binds P_trc; cI binds P_Ls1con",
            "each branch's PHOSPHATASE shuts off the other"],
           ["the nonlinearity",
            "cooperative binding — a dimer on DNA",
            "saturation, and the loop itself"],
           ["what removes it",
            "degradation and dilution, the −u term",
            "the OPPOSING ENZYME — converted, not diluted"],
           ["how long",
            "6 h induction, held 22 h",
            "2 min to stabilize, held 240 min"]],
          colw=[2.55, 4.6, 4.78], top=2.12, gap=0.14)
    d.foot(s, "Row four is the one that is NOT a renaming. The method transfers; the production-against-dilution form does not, and the phosphatase is what replaces it.")
    d.notes(s, "Walk this row by row and do not rush it. This is the "
               "session's reason to exist: the room learned a METHOD in "
               "September, and here is the method surviving a complete "
               "change of molecules.\n"
               "Row four is where to be honest. Segments 1 and 2 spent four "
               "surfaces establishing that a conserved pool is structurally "
               "different from everything before — production balanced "
               "against dilution. So the nullclines, the Jacobian and the "
               "wedge all transfer, and the EQUATIONS do not have the same "
               "form. What plays the role of the dilution term is the "
               "opposing enzyme. Say that, rather than claiming everything "
               "transfers unchanged.\n"
               "Row three is the other honest one, and segment 5's last "
               "surface takes it further.")

    s = d.light()
    d.header(s, "segment 5", "two minutes  ·  with a neighbor")
    d.title(s, "Put it on session 8's axes")
    d.rows(s, [
        ("The axes", "activity of one branch across, activity of the other up — session 8's u and v, with the two branches in their place."),
        ("Draw", "the two nullclines, and mark every intersection."),
        ("Then say", "which intersections are stable, and what the paper's Fig. 4C is showing you about the middle one."),
    ], label_color=TEAL)
    d.foot(s, "The reading asked you to come able to do this. Two minutes.")
    d.notes(s, "Collect this one and walk the room — the reading's focus "
               "line set the task a week ago.\n"
               "The middle intersection is the unstable one, and Fig. 4C is "
               "what happens when you push a cell across it: the defective "
               "toggle falls back, the full network does not. A separatrix, "
               "seen in single cells.")


# ---------------------------------------------- 6 · the other media ---
def _media(d):
    s = d.dark()
    d.header(s, "segment 6", "we are changing the question")
    d.title(s, "The rest of the hour is not about sharpness at all")
    d.rows(s, [
        ("What we have been asking", "how do you MANUFACTURE A PARAMETER — specifically a Hill coefficient — when session 9 said you could only shop for one. That question is now answered three ways: saturation, autoinhibition, recruitment."),
        ("The next two media cannot answer it", "CRISPRi has no cooperativity and no zero-order anything. A recombinase has no dose–response worth the name. Neither will give you a steep switch, and neither is here for that."),
        ("So the question changes", "not “how do I shape a response?” but “what ELSE can I build a circuit out of, and what is each material good for?” Four materials, three axes, one table at the end."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "Say it plainly: a different question, not a continuation. These are two more ways to BUILD and MODIFY a circuit, not two more ways to sharpen one.")
    d.notes(s, "Without this the back half reads as unrelated: the room "
               "has spent the hour on steepness and CRISPRi has none of "
               "it. The pivot has to be explicit and sound deliberate.\n"
               "The honest framing is that segments 1 to 5 answered a "
               "question about a NUMBER and segments 6 and 7 answer a "
               "question about MATERIALS. Both belong in a session called "
               "'protein circuits' because choosing the medium is the first "
               "design decision you make, and it is the one session 2 asked "
               "about in week one.\n"
               "This also sets up T45: the three axes are orthogonality, "
               "speed and load, and each medium wins on a different one.")

    s = d.light()
    d.header(s, "segment 6", "a third medium")
    d.title(s, "Specificity you can type out")
    _paper(d, s, "qi2013_fig1a", 1.80, 2.90,
                   "Qi, Larson, Gilbert, Doudna, Weissman, Arkin & Lim, Cell 152:1173 (2013), Fig. 1A",
                   "20 nt of base pairing, a 42 nt dCas9 handle, a 40 nt terminator.")
    d.foot(s, "A repressor's specificity sits in a protein–DNA interface that evolution built. This one is twenty bases, and you choose them.")
    d.notes(s, "This is the contrast that earns CRISPRi a place on the list. "
               "Thursday showed that recombining protein parts does not "
               "reliably work, because the properties live in interfaces we "
               "did not design. Here the recognition is Watson–Crick, so a "
               "new target is a new oligo.\n"
               "The handle and terminator are fixed. Only the first twenty "
               "bases change, which is why this scales to libraries in a way "
               "that transcription factors never did.")

    s = d.light()
    d.header(s, "segment 6", "the mechanism")
    d.title(s, "Two substitutions turn a nuclease into a roadblock")
    _paper(d, s, "qi2013_fig1b", 1.62, 4.05,
                   "Qi et al. 2013, Fig. 1B",
                   "Wild-type Cas9 binds and cuts. Catalytically dead Cas9 binds and stays there.")
    d.foot(s, "Repression here is physical. The complex sits on the DNA and RNA polymerase cannot get past it.")
    d.notes(s, "Mechanism before model. Once the room has seen that the block "
               "is steric, the repression model they are asked for on PS7 is "
               "an obvious thing rather than a formula.\n"
               "And the chassis point, which is session 2's question again "
               "from the other side. Be precise about what is compared, "
               "because the obvious version of this claim is not what the "
               "paper did: the 1000-fold is TWO sgRNAs combined at about "
               "300-fold each, against mRFP in E. coli; the 46% is a "
               "different guide, eNT2, against EGFP in HEK293. There is no "
               "same-guide comparison across the two hosts anywhere in Qi.\n"
               "What survives is a comparison between MEDIA, and it still "
               "answers session 2: same chemistry of recognition, two orders "
               "of magnitude of difference, because chromatin, nuclear import "
               "and the cell cycle are different.")

    s = d.light()
    d.header(s, "segment 6", "the model  ·  T46")
    d.title(s, "You already wrote this model, in September")
    d.text(s, "F_reg  =  1 / (1 + [dCas9·sgRNA]/K_d)       so       "
              "fold repression  =  1 + [dCas9·sgRNA]/K_d",
           M, 2.22, W - 2 * M, 0.8, size=24, font="head", bold=True,
           color=TEAL, align="c")
    d.text(s, "derived by us from session 6, in the weak-promoter limit. Qi 2013 publishes no model.",
           M, 2.98, W - 2 * M, 0.36, size=14, italic=True, color=MUTED,
           align="c")
    d.rows(s, [
        ("It is session 6's occupancy function", "free or blocked; the denominator sums over whatever can sit on the promoter; the output is the free fraction. Swap the repressor for a dCas9–sgRNA complex and the form is the same."),
        ("What is new is K_d", "specificity comes from 20 nt of base pairing, so K_d is something you design rather than something you inherit from a protein–DNA interface."),
        ("And what is NOT in it", "[dCas9·sgRNA] is not yours to set. Every guide in the cell draws on one dCas9 pool."),
    ], top=3.44, bottom=6.58, label_color=TEAL)
    d.foot(s, "Same equation, third time: operator occupancy in session 6, decoy titration this morning, a shared dCas9 pool on Thursday.")
    d.notes(s, "Write the denominator on the board beside session 6's "
               "1/(1 + [R]/K_m) and "
               "let them see that it is the same object. This is the third "
               "time today that a new medium has turned out to reuse "
               "machinery the course already built, and that repetition is "
               "the argument for having built it.\n"
               "Row three is the one PS7 turns on and it is also Thursday's "
               "hook. The model as written treats the complex concentration "
               "as a free parameter. It is not: Zhang and Voigt measured "
               "the dynamic range collapsing below 10-fold once fifteen "
               "sgRNAs share one dCas9 pool. The term you thought you "
               "controlled is set by what else is in the cell.\n"
               "Two honesty notes. This form is ours, derived from session "
               "6 — Qi publish no model, so do not attribute it to them. "
               "And it is equilibrium occupancy of a PROMOTER, which covers "
               "their ~100-fold promoter-targeting result; their headline "
               "10- to 300-fold comes from an elongation roadblock in the "
               "coding region, which is a different calculation.")

    s = d.light()
    d.header(s, "segment 6", "a fourth medium")
    d.title(s, "Recombinases: memory you cannot un-write")
    d.rows(s, [
        ("The mechanism", "an integrase cuts at two recognition sites and rejoins the DNA inverted or excised. The state is the SEQUENCE now, not a concentration."),
        ("The model", "no differential equation. A finite state machine, with a transition probability per cell per unit time. Session 16's latch, made physical."),
        ("What you get", "memory that survives dilution and the protein being degraded. Nothing has to be maintained."),
        ("What you give up", "reversibility without a second enzyme, and the write is one-way per site. A counter needs a site per count."),
    ], label_color=TEAL)
    d.foot(s, "Four media now. Phosphorylation buys seconds and costs orthogonality; recombinases buy permanence and cost reversibility.")
    d.notes(s, "Keep this brief. The state model is on the next surface and "
               "it is the simplest one in the course.\n"
               "The contrast to draw is with everything else today. A "
               "phospho-toggle holds its state for as long as the ATP lasts "
               "and the enzymes keep running. A recombinase changes the DNA "
               "and then you can kill the enzyme.")

    s = d.light()
    d.header(s, "segment 6", "the model  ·  T47")
    d.title(s, "Session 16's latch, made out of DNA")
    _grid(d, s,
          ["", "session 16 — the SR latch", "today — the recombinase"],
          [["the state",
            "which of two gates is holding",
            "the ORIENTATION of a DNA segment"],
           ["how you write it",
            "a pulse on S or on R",
            "express integrase, or integrase + RDF"],
           ["what holds it",
            "the loop keeps driving itself",
            "nothing. The sequence IS the state."],
           ["what the model is",
            "a state table, not an ODE",
            "a state table, with a rate per cell per hour"],
           ["how fast",
            "as fast as the gates",
            "<2 h (Int8) to 4–6 h (Yang 2014)"]],
          colw=[2.55, 4.6, 4.78], top=2.12, gap=0.14)
    d.foot(s, "No differential equation anywhere. Row three is the difference that matters: one state is maintained, the other is written.")
    d.notes(s, "Put this beside the state table from session 16 if you "
               "still have it up — this is that object with a different "
               "physical realization, and saying so is the whole reason "
               "recombinases are in this session rather than their own.\n"
               "Row three is where to slow down. A latch holds its state by "
               "continuously doing work; kill the power and you lose it. A "
               "recombinase changes the DNA and then you can kill the "
               "enzyme, the cell can divide fifty times, and the state is "
               "still there. One is a standing wave, the other is a scar.\n"
               "Row five, carefully: Yang measured whole-circuit switching "
               "from under 2 hours for the fastest integrase to 4-6 hours "
               "for the slowest. The often-quoted '>90% after 8 h' is the "
               "INDUCTION WINDOW of the assay, not a switching time. Even "
               "so, this is the slowest medium on today's table.")



# ------------------------------------------------ 7 · the comparison ---
def _comparison(d):
    s = d.light()
    d.header(s, "segment 7", "four media")
    d.title(s, "What each one makes easy, and what it charges")
    _grid(d, s,
          ["", "orthogonality", "speed", "load"],
          [["Transcription factor",
            "cross-talk; parts resist recombination",
            "minutes to hours",
            "expression and dilution"],
           ["Protein phosphorylation",
            "poor — Mishra deleted five genes first",
            "seconds",
            "ATP per cycle. No number found."],
           ["CRISPRi",
            "high — 20 nt, designed",
            "set by dCas9 synthesis",
            "shared dCas9 pool: <10× past 15 sgRNAs"],
           ["Recombinase",
            "high — orthogonal site pairs cataloged",
            "<2 h to 4–6 h, once",
            "none once written"]],
          colw=[3.05, 3.55, 2.05, 3.28], top=2.20, gap=0.18)
    d.foot(s, "The phosphorylation load cell says “no number found”, and it means it. Nobody has measured what one of these gates costs its host.")
    d.notes(s, "The CRISPRi load cell is Zhang and Voigt 2018 and it is the "
               "hand-off to Thursday, so say it out loud: 30 orthogonal "
               "sgRNA-promoter pairs are characterized as NOT gates, and once "
               "15 are co-expressed the dynamic range is under 10-fold, "
               "because they all draw on one dCas9 pool. The medium's "
               "headline advantage — programmable orthogonality, roughly "
               "10^7 possible pairs — is destroyed by resource competition. "
               "Thursday's mathematics, arriving a session early as a "
               "measured fact.\n"
               "Do not fill the one empty cell. Nobody has measured the load "
               "of a phosphorylation gate, and a plausible estimate on a "
               "slide is exactly the defect this course keeps catching.")

    s = d.dark()
    d.header(s, "segment 7", "1 September, answered")
    d.title(s, "“Why does the same circuit behave differently in a bacterium and in a human cell?”")
    d.rows(s, [
        ("Speed", "the medium sets the clock. Transcription has to make a protein; phosphorylation moves a phosphate onto one that is already there. Hours against seconds."),
        ("Specificity", "Qi's best single guide gives ~300-fold repression in E. coli, and two combined reach ~1000-fold. A different guide against a different reporter gives 46% in HEK293."),
        ("Size", "diffusion across a cell twenty times wider takes about 400 times longer — 20². Session 2 did that arithmetic in week one."),
        ("And the parts", "Mishra had to delete five genes before the circuit would behave. The chassis is not a blank substrate; it is already running."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "Four reasons, three of them measured. Speed and specificity are the two that will change which medium you reach for.")
    d.notes(s, "Close the loop explicitly and name the date. Students "
               "remember being asked something they could not answer, and "
               "showing that the course was built to come back to it is worth "
               "more than the content of the answer.")


# -------------------------------------------------------------- close ---
def _close(d):
    s = d.dark()
    d.header(s, "close", "where this goes")
    d.title(s, "A parameter is manufactured, not found")
    d.rows(s, [
        ("What you can now do", "produce an apparent Hill coefficient of 26 from one site, with no cooperative binding, by saturating a pair of enzymes. Gardner had to shop for his."),
        ("What it costs", "the threshold, which walks to V₁ = V₂ as the switch sharpens — so you still need the transcriptional layer to place it. Both layers, always."),
        ("Thursday — session 19", "the host's economy. Composition fails again, and this time there is no boundary to impose: your circuit and every other gene draw on the same ribosomes."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "Decoy sites today, ribosomes on Thursday, downstream targets in session 21. One mechanism, three sessions.")
    d.notes(s, "The first row is the answer to session 9's slide and should "
               "be said as one. The second row is why today is not an "
               "argument against promoters.\n"
               "The handoff to Thursday is the pool-size sting from segment 1 "
               "arriving for real: expressing more substrate changed k1 and "
               "k2 by accident. On Thursday the thing you change by accident "
               "is the whole cell.")

    s = d.light()
    d.header(s, "close", "before Thursday")
    d.title(s, "What to read, and what is due")
    d.assignment(s, y=2.10)
    d.notes(s, "PS6 is due Thursday night and PS7 goes out Thursday. Say "
               "both, and say what PS7 covers — sessions 17, 18 and 19.\n"
               "Ceroni is four pages with a capacity monitor inside the cell. "
               "Tell them to come able to say what is being measured and in "
               "what units, because otherwise 'burden' is just a word.")
