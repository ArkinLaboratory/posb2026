"""Session 19 — Resource sharing and burden: the edge that is not in the diagram.

Thursday 29 October 2026. PS6 is due today; PS7 is posted today.

WHAT THIS SESSION IS. Session 17 showed composition failing because parts change
each other through what they physically share -- a junction encodes a 5'UTR, so
attaching a promoter changes the mRNA stability you were about to call promoter
strength. Its cure was to impose boundaries: fix the junction, insulate,
standardise, and the abstraction becomes true because you made it true.

Today composition fails again and THERE IS NO BOUNDARY TO IMPOSE. Two genes with
no regulatory connection change each other's output because they draw on the
same ribosomes. You can fix a 5'UTR. You cannot give your circuit its own
ribosome pool.

That escalation is the hour, and it is rung one of the ladder the rest of Part II
climbs (docs/course-map.md): the host's economy (19, 20), the module next door
(21), disturbance (22), evolution (23), the community (24), the population (25).
So this session has to establish the axis, not just teach shared resources.

THE MECHANISM THAT RUNS THROUGH THREE SESSIONS, and it is named here:
    s18  a transcription factor sequestered by decoy sites
    s19  a ribosome sequestered by every other mRNA in the cell
    s21  an upstream regulator sequestered by its own downstream sites
One mechanism. A student who leaves with three unrelated topics has missed it.

THE CLOSE. Tan, Marguet & You built a noncooperative positive feedback loop --
which by session 9's analysis cannot be bistable -- and it was. The missing
nonlinearity came from the host: activating the circuit slows growth, slower
growth dilutes less, and the dilution term saturates. So the host does not merely
tax the circuit; it adds a behavior that is not in the diagram. Set the burden
parameter to zero and the bistability disappears, which is the controlled test
and is the paper's own semantics ("If gamma = 0, bacteria always divide at phi").

WHERE THE NUMBERS COME FROM. sessions/s19-resources/NUMBERS.md, every one with
its source and its KIND. Nothing on these slides is a number without a kind.
Three things to keep straight while editing:
  * phi_R^max ~ 0.55 and phi_c ~ 0.48 are DIFFERENT quantities, both stated in
    Scott 2010. An earlier build drew them as rival estimates of one ceiling.
  * The Ceroni capacity percentages exist only as plots -- crop the figure, do
    not transcribe numbers off it.
  * The Tan parameter VALUES are secondhand (Ochab-Marcinek 2012 citing Tan).
    The mechanism is reproduced; the figures are not a replication.

NO PRINTED TIME RANGES. Minutes are Adam's.

Run:  python tools/build_decks.py s19
"""
from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)
from decks.theme import LINE, ROOT, line_cap, scale

FIG = "figures/build/"
FILENAME = "s19-resources"

FOOT_Y = 6.75


# Ported from decks/s18_protein.py, 25 October, with the reason it exists.
# paper_figure() fits an image inside a box, so a box whose shape does not
# match the figure leaves the image small in a large empty slot -- the s19
# build reported three of those. Nothing here is sized by eye: the aspect
# comes from the file and the caller gives a height. theme.text() also maps a
# bare size= up onto the 20pt content floor, so the citation line is measured
# at the size it will actually render at, not the number passed.
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


def _paper(d, s, key, y, h, ref, caption, show_caption=False):
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
    cap_h = (max(0.30, _cell_height(caption, w, 14)) + 0.06
             if (caption and show_caption) else 0.0)
    if y + h + 0.04 + ref_h + cap_h > FOOT_Y - 0.05:
        raise AssertionError(
            f"{key}: {h:.2f}in tall at y={y:.2f}in, and its citation plus "
            f"caption need {ref_h + cap_h:.2f}in in a {w:.2f}in column, "
            f"which reaches {y + h + 0.04 + ref_h + cap_h:.2f}in against a "
            f"foot at {FOOT_Y}. Reduce h, or shorten the ref or caption.")
    d.paper_figure(s, key, (W - w) / 2, y, w, h, ref, caption,
                   show_caption=show_caption)
    return y + h + 0.04 + ref_h + cap_h


def _paper_beside(d, s, key, y, h, ref, rows, label_color=TEAL):
    """A TALL paper figure on the left, with the reading of it on the right.

    `_paper` centres a figure at its own aspect, which is right for a wide
    figure and wrong for a tall one: Scott Fig. 4B,C is 0.56 wide for its
    height, so at a full-height 4.6in it is 2.6in across in an 11.9in column
    and the slide reads as empty. Three figures in this deck are like that
    (aspect under about 1.1), and on the rendered page all three looked like
    postage stamps with a caption.

    The fix is not to stretch the figure. It is to put the annotation in the
    space the figure does not want, which is also better teaching: the student
    sees the panel and what to look for in it at the same time, instead of a
    bare panel under a one-line caption.
    """
    from PIL import Image

    from decks.theme import _resolve_paper_figure
    img = _resolve_paper_figure(key)
    if img.exists():
        iw, ih = Image.open(img).size
        w = h * iw / ih
    else:
        w = h * 0.7                       # a slot, for the public build
    gap = 0.55
    col_x = M + w + gap
    col_w = W - M - col_x
    if col_w < 3.2:
        raise AssertionError(
            f"{key}: at h={h:.2f}in the figure is {w:.2f}in wide, leaving a "
            f"{col_w:.2f}in column for the annotation. Use _paper instead, or "
            f"reduce h.")

    ref_h = max(0.30, _cell_height(ref, w, 14))
    if y + h + 0.04 + ref_h > FOOT_Y - 0.05:
        raise AssertionError(
            f"{key}: {h:.2f}in tall at y={y:.2f}in reaches "
            f"{y + h + 0.04 + ref_h:.2f}in against a foot at {FOOT_Y}.")
    d.paper_figure(s, key, M, y, w, h, ref, "")

    cy = y + 0.04
    for i, row in enumerate(rows):
        label, body = row[0], row[1]
        col = row[2] if len(row) > 2 else label_color
        lh = _cell_height(label, col_w, 16)
        d.text(s, label, col_x, cy, col_w, lh, size=16, bold=True, color=col)
        cy += lh + 0.06
        bh = _cell_height(body, col_w, 16)
        d.text(s, body, col_x, cy, col_w, bh, size=16, color=INK, spacing=1.1)
        cy += bh
        if i < len(rows) - 1:          # no trailing gap under the last row
            cy += 0.30
    if cy > FOOT_Y - 0.05:
        raise AssertionError(
            f"{key}: the annotation column runs to {cy:.2f}in against a foot "
            f"at {FOOT_Y}. Cut a row or shorten one.")
    return max(y + h + 0.04 + ref_h, cy)


def _fig(d, s, name, y, dpi=160):
    """Place a figure at its natural size, centred, and return its bottom."""
    from PIL import Image
    w, h = Image.open(ROOT / FIG / f"{name}.png").size
    w, h = w / dpi, h / dpi
    FOOT_Y = 6.75
    if y + h > FOOT_Y - 0.10:
        raise AssertionError(
            f"{name}: placed at {y:.2f}in, {h:.2f}in tall, so it ends at "
            f"{y + h:.2f}in and runs into the foot at {FOOT_Y}. Shorten the "
            f"figure in figures/s19_resources.py -- cut content, not type.")
    # WIDTH GUARD, 26 October. This checked height against the foot and not
    # width against the slide, so a figure wider than 13.33in was centred at a
    # NEGATIVE x and hung off both edges. Two were: s19_bifurcation at 14.52in
    # (y-axis label gone, tick labels clipped to "0^-2", the three-line
    # construction argument cut mid-word, "OFF state is destroyed" struck
    # through by the curve) and s19_ppgpp_mechanism at 13.46in. tools/
    # slide_fit.py reported "Everything fits" throughout, because it measures
    # PowerPoint text boxes and cannot see inside a PNG. Found by the F4.5
    # review; this is the gate that should have caught it.
    if w > W:
        raise AssertionError(
            f"{name}: {w:.2f}in wide on a {W}in slide, so centring puts it at "
            f"x={(W - w) / 2:.2f}in and it is CUT OFF at both edges. Reduce "
            "figsize in figures/s19_resources.py -- cut content, not type.")
    if w > W - 2 * M:
        print(f"  !! {name} is {w:.2f}in wide and bleeds "
              f"{(w - (W - 2 * M)) / 2:.2f}in into each margin "
              f"(text column is {W - 2 * M:.2f}in). On the slide, but not in "
              "the column.")
    d.image(s, FIG + f"{name}.png", (W - w) / 2, y, w, h)
    return y + h


def build():
    d = Deck("Session 19 — Resource sharing and burden", session=19)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _goals(d)
    _economy(d)
    _instrument(d)
    _derivation(d)
    _hidden_edge(d)
    _isocost(d)
    _burden_loop(d)
    _emergent(d)
    _ledger(d)
    _close(d)
    return d


# ---------------------------------------------------------------- opening ---
def _opening(d):
    s = d.dark()
    d.text(s, "Session 19  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "Your circuit is not alone in there",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "Thursday showed parts changing each other through what they "
              "share. Today they change each other through what they BORROW — "
              "and this time you cannot insulate.",
           M, 4.50, 8.6, 1.2, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.45, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s,
           "PS6 is due tonight at 11:59 and PS7 goes out today. Both in "
           "one line, before anything else.\n "
           "The title is the thesis. Thursday's cure for composition "
           "failure was to impose a boundary — fix the junction, "
           "standardise, and the abstraction becomes true because you made "
           "it true. There is no boundary to impose on a ribosome pool. "
           "That makes today the harder problem, not the easier one, and "
           "the difference is what I want them to leave with.")


def _retrieval(d):
    s = d.light()
    d.header(s, "retrieval", "Three minutes  ·  no notes")
    d.title(s, "Three things you already own")
    d.rows(s, [
        ("from Tuesday",
         "a covalent cycle gets an apparent Hill coefficient of 26 out of one modification site. Where did the sharpness come from, given that nothing binds cooperatively?"),
        ("from session 6",
         "write the occupancy of an operator that two different factors compete for. What is in the denominator, and why?"),
        ("from session 5",
         "the response time of a protein is t½ = ln2/(γ + μ). What is μ, and what did we assume about it?"),
    ])
    d.foot(s, "On the third: you treated μ as a number you were given. It is a property of the cell's state, and your circuit changes it.")
    d.notes(s,
           "Answers, so I am not improvising them at the board.\n "
           "Q1 — saturation of both enzymes. Zero-order. No cooperative "
           "binding anywhere in the cycle, which was Tuesday's whole "
           "surprise. It is a warm-up here, so I keep it to thirty "
           "seconds.\n "
           "Q2 — one weight on top, a sum over every competing "
           "configuration underneath. The denominator is everything else "
           "the operator could be doing. This one goes on the board and "
           "stays there, because I reuse that exact denominator in fifteen "
           "minutes with a different pool in it.\n "
           "Q3 — mu is dilution by growth. Nobody volunteers \"and we "
           "assumed it was constant\". That sentence is mine, and it is "
           "what the last third of the hour cashes.")


def _goals(d):
    s = d.light()
    d.header(s, "goals", "What the hour is for")
    d.title(s, "Three questions you cannot answer yet")
    d.rows(s, [
        ("What sets a cell's composition — how fast it is growing, or what it is eating?", ""),
        ("Two genes, no wire between them. Induce one. What happens to the other, and how would you tell that apart from regulation?", ""),
        ("Your circuit slows the cell down. What does that do to the circuit?", ""),
    ], side=False)
    d.foot(s, "You should be able to answer all three by the end. None of them has a one-word answer.")
    d.notes(s,
           "Questions rather than statements, and I answer none of them "
           "here — objectives as a pretest beat objectives as a "
           "declaration.\n "
           "Q3 is the one that comes back twice: once as the response-time "
           "correction in segment 6, and once as the closing result.")


# ------------------------------------------------------------- 1 · economy ---
def _economy(d):
    s = d.light()
    d.header(s, "segment 1", "frame  ·  the cell as an economy")
    d.title(s, "A surprising fact, from 1958")
    d.rows(s, [
        ("Schaechter, Maaløe & Kjeldgaard",
         "measured cell size and macromolecular composition across media and temperatures, in Salmonella, during balanced growth."),
        ("what they found",
         "mass, RNA, DNA and nuclei per cell are set by THE MEDIUM. Within one medium they barely move — drop the temperature from 37 °C to 25 °C, halve the growth rate, and the cell is the same cell."),
        ("and the later generalisation",
         "Scott 2014 restates it as composition tracking the GROWTH RATE. Read literally that is not what 1958 found — the temperature result halves λ and moves nothing — but across media it holds, and it is what makes λ a budget you can write an equation about."),
    ])
    d.foot(s, "Scott et al. 2014, restating it fifty-six years later: composition is “correlated simply with the growth rate of the culture, largely independent of the specific nutrients”. Hold both sentences.")
    d.notes(s,
           "Salmonella typhimurium, not E. coli. Somebody always asks "
           "and I would rather be the one to say it.\n "
           "The third row is what gets left out when people cite this "
           "paper. Everybody quotes the "
           "growth-rate correlation. Almost nobody quotes Table 2, where "
           "they drop the temperature from 37 to 25, the growth rate falls "
           "by about half, and the cell does not change. Verbatim: \"in all "
           "cases, the growth rate at 25 was about half that at 37; "
           "nevertheless, mass, RNA, DNA and number of nuclei/cell remained "
           "nearly constant for a given medium.\"\n "
           "Why I care: growth rate is not the thing the cell regulates on. "
           "If it were reading its own growth rate, cooling it would have "
           "changed the composition, and it did not. Whatever the sensor "
           "is, it is reading the MEDIUM — and fifteen minutes from now "
           "that sensor turns out to be charged tRNA. This is where I plant "
           "the question.\n "
           "A caution about the later literature, because our own foot used "
           "to carry it. Scott 2014 restates this as composition being "
           "\"largely independent of the specific nutrients\" at a given "
           "growth rate. That is a later and looser generalisation, and read "
           "literally it says the opposite of the temperature result. I "
           "quote the 1958 sentence.\n "
           "One more line from their summary that I use two slides on: "
           "\"per unit of RNA, the number of protein molecules synthesized "
           "per minute is almost independent of the growth rate.\" That is "
           "the constant-elongation assumption, stated in 1958, and it is "
           "what the mass-balance argument leans on.")

    s = d.light()
    d.header(s, "segment 1", "frame  ·  why ribosomes, of all things")
    d.title(s, "The one component that has to make itself")
    d.rows(s, [
        ("what a ribosome is",
         "three RNA chains and 56 proteins in bacteria — and about two thirds of its mass is RNA, not protein. Both halves have to be built, and in step."),
        ("why its share tracks the RATE",
         "the ribosomes have to build that cell's entire protein content in one division. Grow twice as fast and, at the same output each, you need about twice the ribosome mass fraction.", CYAN),
        ("and the machine makes itself",
         "some of what they build is more ribosomes. Scott puts it sharply: if ribosomes are 30% of the proteome, 30% of them are making ribosomes."),
        ("and why the assay works",
         "about 85% of the RNA in E. coli is rRNA folded into ribosomes. So an RNA-to-protein ratio IS a ribosome count, measured with a spectrophotometer."),
    ])
    d.foot(s, "Milo & Phillips, Cell Biology by the Numbers (2015), pp. 87 and 188. The 30%: Scott et al. 2014, p. 8. The 85%: Scott et al. 2010, p. 1099.")
    d.notes(s,
           "This is the slide that makes the hour biology rather than "
           "accounting.\n "
           "Row 2 does the work and I say it rather than read it. A cell "
           "has to double its protein. Ribosomes are what make protein. So "
           "the ribosome mass fraction is set by how much protein, and how "
           "fast.\n "
           "The fixed-rate assumption underneath it is not mine and not "
           "Scott's — it is in the 1958 summary: \"per unit of RNA, the "
           "number of protein molecules synthesized per minute is almost "
           "independent of the growth rate.\" Worth saying, because it "
           "means the argument is as old as the observation.\n "
           "Two caveats, and I give them because somebody will get there. "
           "The argument yields proportionality, and law 1 is affine — "
           "phi_R^min = 0.07, ribosomes that are not translating. And it "
           "assumes every ribosome works at a fixed rate, which is false "
           "at the low end: the Bremer and Dennis table has elongation "
           "rising from 13 to 22 amino acids per second across this range, "
           "so the clean argument holds above roughly 1.5 doublings per "
           "hour. It is the right way to see where the law comes from. It "
           "is not a derivation of it.\n "
           "Row 3 is Scott 2014's own sentence and it is the one that "
           "lands. I ask what makes the ribosomal proteins and wait for "
           "somebody to say \"ribosomes\".\n "
           "Row 4 answers the question the Scott figure always produces — "
           "why measure RNA when the claim is about ribosomes.\n "
           "What I will not argue: ribosomes are autocatalytic, therefore "
           "phi_R scales with lambda. No paper we have makes that "
           "argument, and the mass balance gets there honestly.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  what the cell owns")
    d.title(s, "Ribosomes, as a function of how fast you are going")
    _fig(d, s, "s19_ribosome_budget", 1.72)
    d.foot(s, "Bremer & Dennis, EcoSal Plus 3(1) 2008, Table 3 — E. coli B/r at 37 °C, six growth rates. Their columns are doublings per hour; these axes are per hour, so 3.0 doublings/h is 2.08 h⁻¹.")
    d.notes(s,
           "Fivefold in growth rate, ninefold in ribosomes — eight "
           "thousand per cell to seventy-three thousand. That "
           "disproportion is the reason to think in ribosomes rather than "
           "in anything else, and it is the mass balance from a moment ago "
           "arriving as a measurement.\n "
           "Right panel is 7.7% to 22.7% of total protein. Strictly "
           "r-proteins. This is NOT Scott's phi_R, which includes "
           "affiliates, and I cannot reconcile the two without his "
           "supplementary conversion factor. I will not pretend to.\n "
           "Provenance if anyone asks: Bremer and Dennis, EcoSal Plus "
           "3(1) 2008, Table 3 — E. coli B/r at 37 degrees, six growth "
           "rates. Their columns are doublings per hour and these axes are "
           "per hour, which is a factor of ln2 if somebody checks.")

    s = d.light()
    d.header(s, "segment 1", "the paper  ·  what they measured")
    d.title(s, "Two correlations, and the second one is a surprise")
    _paper(d, s, "scott2010_fig1", 1.66, 3.35,
                   "Scott et al., Science 330:1099 (2010), Fig. 1",
                   "A: change the nutrient and the RNA/protein ratio rises with growth rate. "
                   "B: hold the nutrient, inhibit translation, and it rises as growth FALLS. Ignore B's inset.",
                   show_caption=True)
    d.notes(s,
           "Construct before result. The measurement is the RNA-to-protein "
           "ratio, r.\n "
           "Left panel: change the nutrient and r rises with growth rate. "
           "Right panel: hold the nutrient, inhibit translation, and r "
           "rises as growth FALLS.\n "
           "The second correlation deserves the pause. Their sentence is "
           "\"Surprisingly, these data revealed another linear correlation\" "
           "— the authors did not expect it either. Poison the ribosomes "
           "and the cell makes more of them.\n "
           "Two things I will not say. Not \"two assays\" — the word assay "
           "does not appear in the paper. And I will not attach \"six "
           "nutrient sources\" to this figure; the phrase is theirs but it "
           "belongs to Fig. 2A.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  the two laws")
    d.title(s, "Two straight lines, and they disagree about the sign")
    _fig(d, s, "s19_growth_law", 1.72)
    d.foot(s, "φ_R^min = 0.07, γ₀ = 5.9 h⁻¹, φ_R^max = ρ·r_max ≈ 0.55 — all FITTED or extrapolated, and all three quoted from the Scott et al. 2014 Fig. 2 legend.")
    d.notes(s,
           "Segment 1 turns here, and it is where I lose people "
           "if I move fast.\n "
           "The axes first. phi_R is the fraction of total cell protein "
           "that is ribosomal protein. lambda is growth rate, per hour. "
           "Every point is a steady state of a whole culture — not a time "
           "course, and not one cell.\n "
           "Law 1, the thick teal line: vary the carbon source. Better "
           "food, faster growth, more ribosomes. Nobody argues with this "
           "one.\n "
           "Law 2, the two arms coming off it: take ONE medium — a filled "
           "circle sitting on law 1 — and add increasing chloramphenicol. "
           "Growth falls and the ribosome fraction RISES. Each arm is one "
           "medium, and both head for the ceiling, because at total "
           "inhibition growth is zero and the cell is nothing but "
           "ribosome.\n "
           "Then the question that always comes, and I want it: why would "
           "a cell build more of something that does not work? The answer "
           "is the next surface, so I hold it. Short form — the cell is "
           "not counting its ribosomes. It reads charged tRNA. "
           "Chloramphenicol slows elongation and leaves the amino-acid "
           "supply alone, so tRNA stays charged, ppGpp falls, and rRNA "
           "synthesis is de-repressed. The cell reads \"plenty of amino "
           "acids\" and builds.\n "
           "phi_R^max = 0.55 is FITTED, not measured, and I say so. Same "
           "for phi_R^min = 0.07.\n "
           "The ceiling is the constraint that does all the work twenty "
           "minutes from now: there is a maximum fraction of the proteome "
           "that can be ribosome, so anything else I express comes out of "
           "a finite remainder.")

    s = d.light()
    d.header(s, "segment 1", "frame  ·  the controller behind the second law")
    d.title(s, "Why the second law goes the wrong way")
    # The rows that were here named uncharged tRNA, an alarmone and rRNA
    # synthesis in a causal chain without any of those objects having been
    # drawn — rule 1, and the worst bimodality failure in the deck. The
    # figure IS those rows, with the things in it. Replacing rather than
    # adding, so segment 1 does not grow.
    _fig(d, s, "s19_ppgpp_mechanism", 1.70)
    d.foot(s, "Scott et al. 2014, p. 6 — except the antibiotic chain, which is Scott 2010 p. 1100 and hedged there as “possibly”. Note what this is NOT: nothing in it counts ribosomes.")
    d.notes(s,
           "This is the one place in the hour where the biology explains a "
           "result the mathematics cannot, and it answers the question the "
           "last surface raised.\n "
           "Walk the top chain left to right, then the bottom one, and let "
           "the two ppGpp boxes do the work — same box, opposite arrow.\n "
           "The top chain is one passage of Scott 2014, p. 6, including the "
           "flat bar: rRNA synthesis is repressed by ppGpp, which is made "
           "in response to uncharged tRNA. It is four sentences and the "
           "best short statement of this mechanism I know.\n "
           "The bottom chain is NOT in that passage. The antibiotic "
           "reversal is Scott 2010, p. 1100, and there they write "
           "\"implemented POSSIBLY through the relief of repression\". So "
           "I give it as the leading explanation rather than as settled — "
           "which is more interesting anyway, because it means law 2 is a "
           "better-established observation than its own mechanism.\n "
           "What I say out loud that is not on the figure: this is "
           "FEEDFORWARD, not feedback. The cell is not counting ribosomes "
           "and correcting. It measures an upstream mismatch — amino-acid "
           "supply against the rate translation burns them — and acts "
           "ahead of the consequence. Session 10 spent an hour on why that "
           "architecture exists. The amino-acid end-product inhibition is "
           "the feedback layer and it is a separate arm.\n "
           "One detail I will drop if time is short: ribosomal proteins "
           "with no rRNA to bind turn around and bind their own mRNA, "
           "silencing themselves — so the protein half follows the RNA half "
           "with no second controller. That is the fourth sequestration "
           "instance today, inside the machinery.\n "
           "Trap: Scott 2010's Fig. 3B legend says ppGpp \"up-regulates "
           "ribosome synthesis\", which reads as the opposite of all this. "
           "It is loose wording for the FALL in ppGpp doing the "
           "up-regulating. I quote the 2014 sentence.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  the controller, measured")
    d.title(s, "Nine times down, seventeen times up")
    _fig(d, s, "s19_ppgpp", 1.72)
    d.foot(s, "Bremer & Dennis, EcoSal Plus 2008, Table 3 — same cells and growth rates as the budget figure. ppGpp is directly observed; the initiation rate is derived in-table from the ribosome count.")
    d.notes(s,
           "The last slide was mechanism with no numbers on it. These are "
           "the numbers, and they come from the same table as the ribosome "
           "budget — so it is the same organism at the same growth rates.\n "
           "Left: ppGpp falls about ninefold as the cell speeds up. Right: "
           "the initiation rate at each ribosomal RNA gene rises about "
           "seventeenfold over the same range. A repressor going down "
           "while the thing it represses goes up.\n "
           "I am precise about what kind of numbers these are, because the "
           "table is. Its Observed parameters column marks ppGpp as "
           "directly observed but DERIVES the rRNA initiation rate from "
           "the ribosome count — which is the other figure they just "
           "looked at. These are not two independent measurements and I "
           "will not say they are. The honest sentence: one observed "
           "quantity falls while a quantity computed from the ribosome "
           "budget rises.\n "
           "It does not prove causation either. It is a correlation across "
           "growth rates in a table, and the causal work is in the ppGpp "
           "literature. What it establishes is that the controller is "
           "quantitative rather than a story.\n "
           "If somebody asks why initiation per GENE rather than total: "
           "the cell also carries more rrn genes at high growth rate, 7.9 "
           "to 9.4 per genome in the same table, so the per-gene rate "
           "understates the total rise. That is a second, slower knob on "
           "the same output.")

    s = d.light()
    d.header(s, "segment 1", "release  ·  two minutes, on paper")
    d.title(s, "Spend a tenth of the cell on nothing")
    d.rows(s, [
        ("the question",
         "You express a protein the cell has no use for, at 10% of its total protein. Estimate what happens to the growth rate, and say what you had to assume."),
        ("you have what you need",
         "a ceiling on the proteome, and a cell that must build ribosomes in proportion to how fast it grows."),
    ])
    d.foot(s, "Two minutes, a number and one assumption. Do not finish it — I want the shape of the argument, not the arithmetic.")
    d.notes(s,
           "Sharp and short. Most of the room will say \"it goes down\" — I "
           "push for HOW MUCH and watch them reach for a linear "
           "extrapolation to some ceiling. That instinct is exactly right "
           "and segment 6 confirms it with Scott's Fig. 4B.\n "
           "The assumption I am fishing for: that the useless protein "
           "comes out of the same finite proteome the ribosomes are "
           "competing for, so taking 10% leaves 10% less for everything "
           "else including the ribosomes that set the growth rate.")


# ---------------------------------------------------------- 2 · instrument ---
def _instrument(d):
    s = d.light()
    d.header(s, "segment 2", "frame  ·  burden is otherwise a word")
    d.title(s, "Burden is a word until something is measured")
    d.rows(s, [
        ("the problem with “burden”",
         "it sounds like an explanation. Before it can be one, something has to be measured, in units, by an instrument you can describe."),
        ("the usual proxy",
         "growth rate. It is easy, it is cheap, and today you will see why it is the wrong instrument."),
    ])
    d.foot(s, "You read Ceroni et al. for today. The focus line asked you to come able to say what is being measured and in what units.")
    d.notes(s,
           "I take the answer from the room before showing the next "
           "surface. Somebody will have it from the reading: GFP from a "
           "constitutive cassette, as a percentage of an untransformed "
           "cell. If nobody does, that tells me something useful about how "
           "the reading landed and I slow down.\n "
           "What this slide is for is the complaint about the "
           "word. Burden sounds like an explanation. It is not one until "
           "something is measured, in units, by an instrument I can "
           "describe — and growth rate, the obvious instrument, is about "
           "to turn out to be the wrong one.")

    s = d.light()
    d.header(s, "segment 2", "the paper  ·  what they built")
    d.title(s, "A reporter that measures what is left over")
    _paper(d, s, "ceroni2015_fig1a", 1.70, 2.95,
                   "Ceroni et al., Nat Methods 12:415 (2015), Fig. 1a",
                   "Left: capacity, from a constitutive chromosomal GFP cassette. Right: the same cultures' OD. "
                   "Black = no plasmid · blue = plasmid, uninduced · orange and red = Lux induced at the arrows, 0 and 120 min.",
                   show_caption=True)
    d.notes(s,
           "A trace key, because naming them is the job here:\n "
           "grey dashed — DH10B, no GFP at all. The background.\n "
           "black — DH10B-GFP, no plasmid. The ceiling.\n "
           "blue — plasmid present, uninduced.\n "
           "orange — Lux induced at time zero, the first arrow.\n "
           "red — Lux induced at 120 min, the second arrow, and you can "
           "watch it leave the blue curve right there.\n "
           "Left is capacity, thousands of GFP per hour, from a "
           "constitutive cassette at the lambda locus that has nothing to "
           "do with the thing being induced. Right is OD600, same "
           "cultures, same axis out to 270 minutes.\n "
           "One question, which I do not answer: finger on 120 minutes in "
           "each panel — which has separated? Left, ORANGE is a quarter of "
           "black; red is still sitting on blue, because red is the culture "
           "induced AT 120 minutes and has not had time to do anything yet. "
           "Then watch red leave blue over the next thirty minutes on the "
           "left, and not on the right. Right, everything is still on top "
           "of itself.\n "
           "The numbers off the panel, if I need them: at t = 120 the "
           "capacity traces are black 9.3, blue 5.0, red 5.2, orange 1.6, "
           "in thousands of GFP per hour.\n "
           "Wording care: the paper says capacity is \"reduced compared to "
           "that of uninduced cells\". That is a gap between curves, not a "
           "fall — every trace is still rising. Say \"falls\" in front of "
           "rising lines and I lose them while they work out who is "
           "wrong.\n "
           "Absolute units here. The percentage-of-untransformed scale is "
           "Fig. 1d, not this one.")

    s = d.light()
    d.header(s, "segment 2", "debrief  ·  why not weigh the cells")
    d.title(s, "Capacity moves first")
    d.rows(s, [
        ("measured", "within 30 MINUTES of induction, capacity is substantially below what the same cells reach uninduced."),
        ("measured", "the growth change over the same window is smaller and slower."),
        ("and the order matters", "the capacity change PRECEDES the growth change — which is the evidence that losing expression resources is the cause and the slower growth is the consequence."),
    ])
    d.foot(s, "“Decreases in capacity in both strains led to subsequent growth-rate decreases of similar magnitude.” Ceroni et al. 2015.")
    d.notes(s,
           "This is the argument for the instrument and it is better than "
           "any single number in the paper. Growth rate is a lagging, "
           "blunt proxy: by the time it shows on an OD trace, the thing "
           "that caused it happened half an hour ago.\n "
           "It also licenses the rest of the hour. If burden were only "
           "\"the cells grow slower\" there would be nothing to model. "
           "Capacity says what was TAKEN, and taken from a pool, which is "
           "what the next segment derives.\n "
           "The ORDER is what is being claimed — capacity moves first, growth "
           "follows. That is the evidence that losing expression resources "
           "is the cause and slower growth is the consequence, rather than "
           "the other way round.")

    s = d.light()
    d.header(s, "segment 2", "the paper  ·  the result you read")
    d.title(s, "Same output, different price")
    _paper_beside(d, s, "ceroni2015_fig2c", 1.74, 3.90,
        "Ceroni et al. 2015, Fig. 2c",
        [("one protein, built many ways",
          "VioB-mCherry, varied by copy number, promoter, RBS and codon usage. Each point is one design."),
         ("read it horizontally",
          "H3 and M1 deliver output in the same range. H3 leaves the host about three times the capacity that M1 does. Same job, very different price.", RED),
         ("and note the shaded corner",
          "they drew a frontier and called the far side unattainable. Hold that picture — you derive its shape in segment 5.", CYAN)])
    d.notes(s,
           "The protein has no function in these cells. That is "
           "deliberate, and it is the same experiment Scott did with LacZ "
           "— pure load, no benefit.\n "
           "The teaching point is the VERTICAL spread at a fixed output, "
           "and H3 against M1 is the pair to point at. Comparable output; "
           "one of them leaves the host about three times the capacity of "
           "the other. If burden were a function of output alone, every "
           "point would lie on one curve and there would be no spread to "
           "point at.\n "
           "Colour carries most of the story: blue is weak-RBS, red is "
           "strong-RBS, grey is uninduced. The strong-RBS designs are the "
           "expensive ones at any given output.\n "
           "The shaded corner is the thing I flag deliberately. They have "
           "drawn a frontier and called the other side unattainable — from "
           "a flow cytometer, with no model. In segment 5 I derive that "
           "frontier from a partition function and it comes out straight. "
           "I tell them now that we are coming back to this picture.\n "
           "I do not read numbers off the axes out loud. They live in the "
           "plot, not in the text.")


# ---------------------------------------------------------- 3 · derivation ---
def _derivation(d):
    # The two objects the run needs, defined BEFORE it starts. Folding them in
    # as steps took the run to seven, and at seven the band forces a choice
    # between the closing box and the asides -- both renderings were checked
    # and both were bad. Five steps, each a move where something changes, is
    # the shape `posb-teaching-derivations` asks for anyway.
    s = d.light()
    d.header(s, "segment 3", "frame  ·  from measuring it to deriving it")
    d.title(s, "What a ribosome is doing, and how hard a gene pulls")
    d.rows(s, [
        ("the binding step",
         "R + m_{i} ⇌ C_{i}  —  a ribosome binds an mRNA and is released when it finishes. Same shape as an enzyme and a substrate, which is why session 4's move will work on it."),
        ("the demand of gene i",
         "d_{i} = m_{i} / K_{i}  —  how hard gene i pulls on the pool. More message, or tighter binding, is more demand. One number per gene."),
        ("and K_{i} is a sequence you can order",
         "it is set by the ribosome-binding site. Demand is a thing you clone, not a parameter you fit.", CYAN),
    ])
    d.foot(s, "Ceroni measured the coupling. Nobody has said WHY two unconnected genes should interact at all — that is the next five lines, and these two definitions are all they need.")
    d.notes(s,
           "Two definitions, named, so the run itself is uninterrupted. "
           "This is not a segment and I do not let it become one.\n "
           "The demand is worth a beat: it folds message abundance and "
           "binding strength into one quantity, which is why the answer "
           "comes out in terms of it rather than in terms of five "
           "parameters.\n "
           "And K_i is the row that makes this a biology slide rather than "
           "a notation slide. It is set by the ribosome-binding site — how "
           "well the bases upstream of the start codon pair with the "
           "ribosome's own 16S rRNA. Demand is a thing you clone. It is "
           "the same knob Ceroni varied across his library and the same "
           "one Gyorgy weakens in the figure coming up.")

    d.derivation(
        None, "segment 3", "the model",
        "Two genes, one ribosome pool",
        # Asides are ONE SHORT LINE each. At this pitch a two-line aside runs
        # into the next row -- eleven overlaps, found by rendering. The
        # fuller version of each lives in the speaker notes.
        [("Quasi-steady state",
          "C_{i}  =  R · d_{i}",
          "Session 4's move, on a ribosome."),
         ("Ribosomes are conserved",
          "R_{T}  =  R  +  Σ_{j} C_{j}",
          "Free or busy. Nothing else."),
         ("Substitute",
          "R_{T}  =  R  +  R · Σ_{j} d_{j}",
          "Each bound one is proportional to R."),
         ("So the free pool factors out",
          "R_{T}  =  R · ( 1 + Σ_{j} d_{j} )",
          "One division finishes it."),
         ("Solve",
          "R  =  R_{T} / ( 1 + Σ_{j} d_{j} )",
          "One number, multiplying every gene at once.")],
        # NO closing box, and the reason is arithmetic rather than taste.
        # `derivation` places an aside from y+0.42 to y+0.86 but switches
        # asides on whenever the pitch is >= 0.70, so ANY run whose pitch
        # lands between 0.70 and 0.86 overlaps itself. A closing box drops the
        # band to 3.90in, which at five steps is a pitch of 0.78 -- inside
        # that window, and the build reported ten overlapping pairs that the
        # rendered page did not obviously show. Without the box the band is
        # 4.98in, the pitch is 1.00, and the run is clean. The punchline then
        # gets its own surface, which is where it belongs anyway.
        # Reported to Adam as a theme.py threshold to fix (0.70 -> 0.86).
        board="the session-6 occupancy, still on the board",
        note="The payoff is step four: the free pool factors out of the "
             "conservation law. Everything after it is one "
             "division.\n"
             "The closing line is the one to land. In session 6 the sum ran "
             "over binding configurations of an operator; here it runs over "
             "the genes in the cell. Nothing new had to be invented, and that "
             "is the argument for having derived it the hard way in "
             "September. Point at the board.")

    s = d.light()
    d.header(s, "segment 3", "debrief  ·  what you have just written down")
    d.title(s, "You have seen this denominator before")
    d.rows(s, [
        ("one more line, and it is the one you will use",
         "gene i's output follows the ribosomes sitting on its message:  p_{i} ∝ C_{i} = R · d_{i}.  Put back the R you just solved for."),
        ("which gives",
         "p_{i}  ∝  d_{i} / ( 1 + Σ_{j} d_{j} )   —  gene i's own demand, over what every gene in the cell is asking for.", CYAN),
        ("session 6, September 15",
         "the occupancy of an operator: one weight on top, and a sum over every competing configuration underneath."),
        ("same form, different pool",
         "there the sum ran over ways of occupying one piece of DNA. Here it runs over the genes competing for one set of ribosomes. Nothing new had to be invented.", CYAN),
    ])
    d.foot(s, "Which is what five weeks of deriving things the hard way buys you — the second time, it is five minutes.")
    d.notes(s,
           "This is the transferable thing in the whole session and it is "
           "worth its own surface.\n "
           "I point at the board where the session-6 expression still is. "
           "If it is not still there, I write it again before I start.\n "
           "What they should take: it is not the ribosome model that "
           "transfers, it is the recognition. A conserved pool with "
           "competing demands always gives a partition function — one "
           "weight on top, a sum over everything competing underneath — "
           "and they already know how to read one. In September it ran "
           "over binding configurations of one operator. Here it runs over "
           "the genes in the cell. Nothing new had to be invented, and "
           "that is what five weeks of deriving things the hard way "
           "bought.")


# -------------------------------------------------------- 4 · hidden edge ---
def _hidden_edge(d):
    s = d.light()
    d.header(s, "segment 4", "frame")
    d.title(s, "An edge with no arrow")
    d.rows(s, [
        ("what you just derived",
         "p₁ depends on d₂. Gene 1's output depends on how hard gene 2 is pulling, for every gene 2 in the cell."),
        ("what a circuit diagram records",
         "nothing. There is no arrow to draw. The two genes are not connected in any sense the schematic knows about."),
    ])
    d.foot(s, "So: induce one gene, and an unrelated one moves. How much, and could you tell it from repression?")
    d.notes(s,
           "I do not call this crosstalk, and I say why. Crosstalk is a "
           "part being unspecific — a repressor binding an operator it "
           "should not. This is two perfectly specific parts interacting "
           "through a resource neither of them is misusing. The "
           "distinction matters because the fixes are completely "
           "different: for crosstalk you re-engineer the part, and here "
           "there is no part to re-engineer.\n "
           "The sentence I want in their heads: there is no arrow to draw. "
           "The schematic is not wrong, it is incomplete in a way no "
           "schematic of this kind can fix.")

    s = d.light()
    d.header(s, "segment 4", "release  ·  commit to a number")
    d.title(s, "Gene 2 pulls four times as hard. What happens to gene 1?")
    d.rows(s, [
        ("gene 1 is running at demand 1",
         "You now induce gene 2 to demand 4 — four times gene 1's pull on the pool."),
        ("predict",
         "By what percentage does gene 1's output fall? Write a number down before we go on."),
    ])
    d.foot(s, "Thirty seconds and a number. You have the expression; this is arithmetic, not insight.")
    d.notes(s,
           "They commit in writing before anything goes up. The answer is "
           "67% and most people guess far too low, because a "
           "factor-of-four demand from a gene they are not even thinking "
           "about sounds like a nuisance rather than two thirds of their "
           "output.\n "
           "The arithmetic, so it is on the tip of my tongue: p1 goes as "
           "d1/(1+d1+d2). With d1 = 1 and d2 = 0 that is one half. With d2 "
           "= 4 it is one sixth. One sixth over one half is a third, so "
           "two thirds of the output is gone.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  the edge, and how to catch it")
    d.title(s, "It looks exactly like repression")
    bot = _fig(d, s, "s19_hidden_edge", 1.70)
    d.foot(s, "p₁/p₁(d₂=0) = 1/(1 + d₂/(1+d₁)) — a Hill function in d₂, n = 1, K_app = 1 + d₁. Both panels normalised the same way: to the output with the competitor absent.")
    d.notes(s,
           "Left panel first, against the numbers they just wrote down.\n "
           "Where the curve comes from, because this is the slide that "
           "connects the algebra to the picture. Take what we derived, p1 "
           "proportional to d1/(1+d1+d2), and divide by its value when "
           "gene 2 is absent, which is d1/(1+d1). Everything cancels "
           "except 1/(1 + d2/(1+d1)). That is algebraically a Hill "
           "function in d2 with exponent one, and its half-point is K_app "
           "= 1 + d1. It IS a repression curve. Nothing is repressing "
           "anything.\n "
           "So the left panel does not resemble a dose-response. It "
           "is one, exactly, and that is why the mistake is so easy to "
           "make from real data.\n "
           "The right panel is the engineering payoff and it is a "
           "diagnostic a student can design. Three curves, three values of "
           "d1 — the demand of the gene being apparently repressed. The "
           "fitted K moves with it: 1.2, 2 and 6 for d1 of 0.2, 1 and 5, "
           "which is 1 + d1 each time.\n "
           "Why that is a test: a real repressor's K is a property of a "
           "protein binding a piece of DNA. It does not care how hard the "
           "reporter is being expressed. So measure the apparent K at two "
           "expression levels of your own reporter. If it moves, you are "
           "looking at the pool. No cloning required, and they could run "
           "it this semester.")


# -------------------------------------------------------------- 5 · isocost --
def _isocost(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  a different question")
    d.title(s, "Stop asking who loses. Ask what the budget is.")
    bot = _fig(d, s, "s19_isocost", 1.70)
    d.foot(s, "Until now: who loses when you induce. Now: how much is there to go round at all? Each line is one total demand, spent every possible way — and the sum depends on the total, not the split.")
    d.notes(s,
           "I derive the sum out loud and I keep the qualifier, because "
           "the identity is false without it. Normalise each output by "
           "what it would reach alone AT UNLIMITED DEMAND — which is one — "
           "not by what it reaches alone at its own demand. Then p1 + p2 = "
           "(sum of d)/(1 + sum of d), which contains no d1 or d2 "
           "separately.\n "
           "So at a fixed total demand the achievable outputs lie on a "
           "straight line, and raising the total walks that line outward "
           "toward a bound it never reaches.\n "
           "The name is theirs, from economics: an isocost line is the set "
           "of input combinations that cost the same. Each solid line here "
           "is one budget, spent every possible way between two genes.")

    s = d.light()
    d.header(s, "segment 5", "the paper  ·  measured")
    d.title(s, "The same straight line, out of a cytometer")
    _paper_beside(d, s, "gyorgy2015_fig3b", 1.74, 3.70,
        "Gyorgy et al. 2015, Fig. 3B",
        [("the four lines",
          "one plasmid in four versions, differing only in the RFP ribosome-binding site — 1.0 down to 0.006. Along a line you turn AHL up."),
         ("each point",
          "a population mean at one dose, by flow cytometry. No wire between the two genes."),
         ("we drew this line from a partition function",
          "they got it from a cytometer. Straight, as predicted — and steeper as the RBS weakens, which ribosomes alone cannot give you.", CYAN)])
    d.notes(s,
           "Where we are, and it is a "
           "shift that deserves naming. We derived the isocost line on "
           "the board, from a partition function, with no data anywhere "
           "near it. The question now is whether a cell does "
           "that. This is the first time today we check ourselves against "
           "a measurement.\n "
           "What is on the axes: mean RFP on x, mean GFP on y, both "
           "arbitrary units. Each point is a population mean at one AHL "
           "dose, read by flow cytometry — not single cells.\n "
           "The four lines are four versions of the same plasmid, "
           "differing only in the strength of the ribosome-binding site in "
           "front of RFP. MBP-1.0 is the full-strength RBS; 0.3, 0.02 and "
           "0.006 are progressively weaker, and the number is the relative "
           "RBS strength. Walking along any one line means turning AHL up "
           "and making more RFP.\n "
           "Two things to see. Each one is straight, which is our isocost "
           "line out of a cytometer. And the slope steepens as the RBS "
           "weakens — which ribosomes alone cannot predict. Their "
           "sentence: it \"cannot be predicted unless RNAP is limiting\". "
           "Two shared resources, not one. One sentence on that, not five.\n "
           "If anyone is reading closely: the intercept also rises for "
           "weaker RBSs, which is in the paper and which I am not going to "
           "explain today.")

    s = d.light()
    d.header(s, "segment 5", "the paper  ·  both reporters on the plasmid")
    d.title(s, "Induce one gene, and an unconnected one falls")
    _paper(d, s, "gyorgy2015_fig1a", 1.74, 3.30,
           "Gyorgy et al. 2015, Fig. 1A",
           "RFP and GFP on one plasmid, RFP driven by LuxR and AHL. Bars are the AHL series. Watch the GFP axis — it is INVERTED, 0 at the top.",
           show_caption=True)
    d.foot(s, "Our model says one pool, so where a gene sits should not matter. That is testable in the most direct way there is, and this is half of the test.")
    d.notes(s,
           "Read the two bar charts against each other. More AHL, more RFP "
           "going up; GFP going the other way. The GFP axis is upside "
           "down, 0 at the top, which nobody expects and which I say "
           "before anybody squints at it.\n "
           "Nothing connects these two genes. Different promoters, "
           "different regulators, no shared operator. The only thing they "
           "share is the machinery that reads them.\n "
           "What I set up here and resolve next: our model, taken "
           "literally, says the pool is the whole cell. If that is right, "
           "moving the GFP gene somewhere else cannot change anything.")

    s = d.light()
    d.header(s, "segment 5", "the paper  ·  now move one of them")
    d.title(s, "Same induction, same series. One thing changed.")
    _paper(d, s, "gyorgy2015_fig1b", 1.74, 3.30,
           "Gyorgy et al. 2015, Fig. 1B",
           "A DIFFERENT construct: the same circuit, with GFP integrated in the chromosome instead of sitting on the plasmid.",
           show_caption=True)
    d.foot(s, "The chromosome's GFP does not move. If there were one pool, this could not happen.")
    d.notes(s,
           "Why this experiment exists, and I lead with it, because "
           "without the motivation it is two bar charts.\n "
           "Our model says one pool. Taken literally that means everything "
           "in the cell couples to everything, and it should not matter "
           "WHERE a gene sits. That is a strong claim and it is testable "
           "in the most direct way available: put the same reporter in two "
           "places and induce exactly the same way.\n "
           "Panel A: GFP and RFP both on the plasmid. Induce with AHL and "
           "the plasmid's GFP falls.\n "
           "Panel B: a DIFFERENT construct — built so the GFP is "
           "integrated in the chromosome instead. Same inducer, same AHL "
           "series, same everything else. The chromosome's GFP does not "
           "move.\n "
           "I say out loud what is identical and what is not, because that "
           "is the entire argument: one thing differs, and it is where the "
           "gene sits.\n "
           "And the control, which is what makes this a result rather than "
           "a null: they built a separate strain, with TetR on a plasmid "
           "and the GFP still chromosomal, specifically to show that a "
           "reduction in the chromosomal GFP WOULD have been detectable if "
           "it were there. It is not an absence of evidence.\n "
           "I do not give the conclusion here. The debrief is next and "
           "what they should be holding is the puzzle: if there were one "
           "pool, moving the gene could not matter.")

    s = d.light()
    d.header(s, "segment 5", "debrief  ·  where is the pool, exactly?")
    d.title(s, "The pool has an edge, and it is not where the model put it")
    d.rows(s, [
        ("the obvious reading of our model",
         "one pool, so everything couples to everything. Induce anything, and every other gene moves."),
        ("what they measured",
         "two reporters on one plasmid interfere — up to 60%. Move one to the CHROMOSOME and the same induction leaves it alone. And it scales: 64 plasmid copies gives 60%, 18 gives 48%, 4 gives 29%.", RED),
        ("and the null is controlled",
         "they built a strain specifically to show that a chromosomal reduction would have been detectable. It was not an absence of evidence."),
        ("so", "the shared pool has a boundary, and it is not where the model's one-pool reading puts it. Where it falls is an experimental question."),
    ])
    d.foot(s, "“The pools of RNAP and ribosomes available to the genes on the plasmid are essentially separated from those available to the chromosomal genes.” — Gyorgy et al. 2015, Discussion.")
    d.notes(s,
           "This is the wrong turn and the correction, and it is better "
           "teaching than the clean version would be. The one-pool model "
           "is right about the mechanism and wrong about the extent, and "
           "only a measurement settles which.\n "
           "Each number comes from a different place. The up-to-60% "
           "drop is Fig. 1C, the GapA version of the circuit. The "
           "chromosome-unchanged result is Fig. 1B, a different construct. "
           "The paper does not put a percentage on the same-plasmid drop "
           "in the chromosomal experiment, so I do not quote one as though "
           "it were a matched pair.\n "
           "The copy-number series is the other half of it, and it is the "
           "designer's lever: 64 copies gives 60%, 18 gives 48%, 4 gives "
           "29%. Lowering copy number genuinely lowers coupling.\n "
           "A caveat that keeps the three papers honest. Gyorgy saw almost "
           "NO growth-rate change on induction. Their coupling and "
           "Ceroni's burden are not the same measurement. If somebody asks "
           "how that squares with the growth law, the answer is that this "
           "construct is cheap enough to move reporters around without "
           "moving lambda.\n "
           "And the tie back to Thursday, explicitly. Session 17: a part "
           "has no boundary until you manufacture one. Today: a resource "
           "pool has a boundary and you have to go and FIND it. Same "
           "lesson, opposite direction.")


# --------------------------------------------------------- 6 · burden loop ---
def _burden_loop(d):
    s = d.light()
    d.header(s, "segment 6", "build  ·  the price, in growth")
    d.title(s, "Linear, all the way to a stop")
    _fig(d, s, "s19_burden_cost", 1.72)
    d.foot(s, "φ_c = 0.48 is NOT the φ_R^max = 0.55 from segment 1 — that was the ribosome ceiling, this is where growth hits zero. Different quantities, both from Scott 2010.")
    d.notes(s,
           "A biologist in the room should object here, and the objection "
           "is right: surely a useless protein also costs amino acids, ATP "
           "for every peptide bond, and chaperone capacity to fold it. "
           "Scott's model charges for NONE of that. It charges proteome "
           "fraction and nothing else.\n "
           "I say that, and then I say that it fits anyway — which is the "
           "interesting part, and tells you the proteome channel dominates "
           "in this regime. I do not let the simplification pass unmarked.\n "
           "The form and the intercept are both theirs. phi_c = 0.48 is "
           "stated in the paper and computed there from r_max. The "
           "per-percent figure is one division of it and it is ours — "
           "about two percent of growth rate for every one percent of the "
           "proteome you take.\n "
           "Then the intercept itself: growth extrapolates to zero at 48%. "
           "That is a hard ceiling on how much of a cell you can spend on "
           "something it does not need.")

    s = d.light()
    d.header(s, "segment 6", "the paper  ·  the law, tested")
    d.title(s, "The lines were drawn before the data")
    _paper_beside(d, s, "scott2010_fig4b", 1.74, 4.30,
        "Scott et al. 2010, Fig. 4B",
        [("what is plotted",
          "growth rate against the percentage of total protein given to β-galactosidase the cell has no use for, in three media."),
         ("the three lines are predictions",
          "from Eq. 6, with the 48% intercept computed from an r_max fitted to a DIFFERENT experiment. The slope was not fitted to these points."),
         ("why that is the stronger claim",
          "a regression would only tell you these points lie on a line. This says the line was known before the points were.", CYAN)])
    d.notes(s,
           "The predictions-not-fits point, made accurately, because I "
           "have overstated it before.\n "
           "Each line IS anchored at that medium's own zero-induction "
           "growth rate, so it is not true that nothing was taken from "
           "this data. What is true, and is the strong claim, is that the "
           "SLOPE was fixed in advance by an r_max fitted to a different "
           "experiment. The intercept was computed, the lines were drawn, "
           "and then the data fell on them.\n "
           "So I say \"the slope was known before the points were\", not \"no "
           "adjustable parameters\" — even though the paper itself says the "
           "latter.\n "
           "That is a much stronger claim than a regression, and noticing "
           "the difference is one of the things this course is for.")

    s = d.light()
    d.header(s, "segment 6", "the paper  ·  and it does not matter which protein")
    d.title(s, "Three proteins, four systems, one curve")
    _paper_beside(d, s, "scott2010_fig4c", 1.74, 3.65,
        "Scott et al. 2010, Fig. 4C",
        [("three proteins, four expression systems",
          "β-galactosidase twice, from two promoters in two papers, plus β-lactamase and a truncated EF-Tu."),
         ("and they all fall together",
          "no lines drawn here, and none needed. The defect tracks how MUCH of the proteome you took — not what you took it for, nor how you expressed it."),
         ("which is the model's real claim",
          "the cell charges you for the space — not the amino acids, not the ATP, not the folding. A strong and falsifiable claim, and this is where it survives.", CYAN)])
    d.notes(s,
           "Thirty seconds, and it is the strongest evidence in the paper for "
           "the modelling choice I flagged two surfaces back.\n "
           "Three proteins across four expression systems — and two of the "
           "four series are the SAME protein, beta-galactosidase, driven "
           "from different promoters on different plasmids in different "
           "papers. That pair is its own control: same protein, different "
           "way of making it, same cost.\n "
           "If the cost were really about amino acids or folding, these "
           "would not land together. A beta-lactamase is exported to the "
           "periplasm. A truncated EF-Tu is a misfolding hazard. They cost "
           "the same as LacZ per percent of proteome. That is what "
           "licenses the one-channel model.\n "
           "The honest limit, out loud: one organism, one growth regime, a "
           "handful of proteins. Not a law of nature — a good "
           "approximation with evidence behind it.")

    s = d.light()
    d.header(s, "segment 6", "debrief  ·  the loop closes")
    d.title(s, "What this does to your circuit's own dynamics")
    d.rows(s, [
        ("session 5 gave you", "t½ = ln2 / (γ + μ), and μ is dilution by growth."),
        ("you treated μ as given", "a number from the medium. PS2 used it that way."),
        ("but μ is a property of the cell's state", "and your circuit just changed it. Induce the circuit, divert ribosomes, growth slows, μ falls.", RED),
        ("so every protein in the cell", "gets a longer effective lifetime when you switch your circuit on — including the circuit's own. The response time you computed is not the response time you get."),
    ])
    d.foot(s, "Nothing about the DNA changed. That closes the tax — everything so far has been the host charging you, in numbers. Next: something the host does that your diagram cannot do at all.")
    d.notes(s,
           "This is the payoff of the third retrieval question and it "
           "should land hard. I go back to the board where mu is written "
           "and change it in front of them.\n "
           "The caveat: the direction is unambiguous, the magnitude "
           "depends on the construct and the medium, and "
           "posb.resources.dilution_coupled_steady_state asks THEM for the "
           "penalty rather than assuming one — because a coefficient "
           "travels with its citation or it means nothing.\n "
           "And this closes segment 6, so I say what has just finished. "
           "Everything so far today has been the host charging them: less "
           "output, slower growth, longer lifetimes. All of it "
           "quantitative. Every one of those is a number attached to a "
           "mechanism they can already draw.\n "
           "The next segment asks a different question, and I announce it "
           "rather than letting them discover it: does the host do "
           "something your diagram cannot do AT ALL?")


# ------------------------------------------------------------ 7 · emergent ---
def _emergent(d):
    s = d.light()
    d.header(s, "segment 7", "frame  ·  one more thing the host does")
    d.title(s, "Session 9 says this circuit cannot do what it does")
    d.rows(s, [
        ("so far today", "the host taxes you. Less output, slower growth, longer lifetimes. All of it quantitative, none of it qualitative."),
        ("now a circuit", "a mutant T7 RNA polymerase that activates its own expression. One gene, positive feedback, and the activation is NONCOOPERATIVE."),
        ("session 9 says", "no cooperativity, no bistability. The wedge needs n > 1 on at least one arm. You proved this and PS4 made you find that n = 1 fails."),
    ])
    d.foot(s, "Tan, Marguet & You, Nat Chem Biol 5:842 (2009). Hold your prediction until you have seen the circuit.")
    d.notes(s,
           "This surface sets the contradiction up and deliberately does "
           "not resolve it. Three rows, then I move — the vote happens on "
           "the next surface, once they can see the loop.\n "
           "The row that matters is the third one. They derived this "
           "themselves in session 9 and PS4 made them find the case where "
           "n = 1 fails, so it is not a fact they are being told. The "
           "wedge needs cooperativity on at least one arm, and here there "
           "is no exponent anywhere.\n "
           "Where this is going, which I say in one sentence: the last "
           "three things the host did were taxes. This one is not a tax. "
           "The host is about to supply a nonlinearity the circuit does "
           "not contain, and that is a different kind of claim.")

    s = d.light()
    d.header(s, "segment 7", "the paper  ·  the circuit")
    d.title(s, "One gene, activating its own promoter")
    _paper(d, s, "tan2009_fig1a", 1.70, 3.30,
           "Tan, Marguet & You, Nat Chem Biol 5:842 (2009), Fig. 1a",
           "T7 RNAP* drives its own promoter. CFP is the readout; IPTG relieves LacI.")
    d.foot(s, "No cooperativity anywhere in that loop. Hands up: one stable state, or two?")
    d.notes(s,
           "The vote happens here, out loud, hands up, before anybody "
           "turns the page. One stable state or two.\n "
           "Session 9's analysis is unambiguous and the room should say "
           "one — the wedge needs n greater than one on an arm and there "
           "is no n in this loop at all. They are about to be wrong, and "
           "being wrong out loud first is what makes the next surface "
           "work.\n "
           "The circuit, in case it is asked: a mutant T7 RNA polymerase "
           "driving its own promoter, P_T7 carrying a lac operator so LacI "
           "represses it, IPTG relieving the repression, and CFP "
           "co-expressed as the readout. One gene, positive feedback on "
           "itself.")

    s = d.light()
    d.header(s, "segment 7", "the paper  ·  what happened")
    d.title(s, "Two populations, from a circuit that cannot have two")
    _paper_beside(d, s, "tan2009_fig1c", 1.74, 4.20,
        "Tan et al. 2009, Fig. 1c",
        [("what is plotted",
          "CFP across a whole population of single cells — not a population average. Two modes, not one broad peak."),
         ("the measurement is not an assumption",
          "their Fig. S6 puts a Hill coefficient of about 0.99 on CFP against EYFP. Noncooperative, measured — not merely absent from the diagram."),
         ("and that is the result",
          "a third of cells ON before dilution, a third ON eight hours after. The two modes are a steady state, not a transient on the way to one.")])
    d.foot(s, "Session 9's wedge needs cooperativity on at least one arm. There is none anywhere in this loop. So where did the second state come from?")
    d.notes(s,
           "Two populations, from a circuit whose regulation contains no "
           "cooperativity anywhere. I let that sit before explaining it.\n "
           "The noncooperativity is MEASURED, not assumed — their Fig. S6 "
           "gives a Hill coefficient of about 0.99 for CFP against EYFP. "
           "That is a stronger statement than \"no cooperative step appears "
           "in the diagram\" and it closes off the obvious objection before "
           "anyone raises it.\n "
           "They checked it was a steady state rather than a transient: "
           "diluted into fresh medium, grew eight more hours, same "
           "fraction of ON cells. The panel is labelled 30% ON before and "
           "32% ON after; the Fig. 1c legend rounds both to about 31%. Say "
           "\"about a third, and it did not move\" — the two-point "
           "difference is a rounding, not a drift, and the room can read "
           "both numbers off the screen.\n "
           "If anyone asks where the legend's 31% comes from: it is the "
           "rounding of the panel's own 30 and 32, not a third "
           "measurement.")

    s = d.light()
    d.header(s, "segment 7", "build  ·  where the nonlinearity was hiding")
    d.title(s, "Not in the regulation — in the dilution")
    bot = _fig(d, s, "s19_rate_balance", 1.70)
    d.foot(s, "x is T7 RNAP*.  δ its leak, α its synthesis rate, which IPTG turns up.  φ the unburdened growth rate, and the +x is degradation.  γ is the burden — how hard x slows the cell.")
    d.notes(s,
           "The axes first, because \"rate\" on its own means nothing. Both "
           "curves are rates of change of the SAME quantity — T7 RNAP* "
           "made per unit time, and T7 RNAP* removed per unit time — "
           "plotted against how much of it is already there. Log-log, "
           "because the three steady states at alpha = 14 sit at 0.0015, "
           "0.06 and 11, and on a linear axis the two low ones land in the "
           "same pixel.\n "
           "Expression is Hill-1 in x. No exponent anywhere, which is the "
           "whole point.\n "
           "Removal is dilution plus degradation, and dilution SATURATES — "
           "expressing more polymerase slows growth, and a cell that grows "
           "more slowly dilutes less. A saturating removal curve crossing "
           "a saturating production curve can cross three times.\n "
           "Then the part the figure now states and I used to skip. A "
           "crossing is a steady state, nothing more. Whether it HOLDS is "
           "the slopes. Where removal is steeper, a nudge upward is "
           "over-removed and the system comes back — stable, filled. Where "
           "expression is steeper, a nudge upward makes more than it "
           "removes and it runs — unstable, open. The crossing is not the "
           "evidence; the slopes are.\n "
           "Right panel is the controlled test and it is the paper's own "
           "semantics: \"If gamma = 0, bacteria always divide at phi.\" Take "
           "the burden away and the third crossing is gone. The "
           "nonlinearity was never in the circuit.")

    s = d.light()
    d.header(s, "segment 7", "debrief  ·  and it has a wedge")
    d.title(s, "Two saddle-nodes, and they fail differently")
    _fig(d, s, "s19_bifurcation", 1.70)
    d.foot(s, "α increases with IPTG, so this axis is a knob you turn. The two edges fail differently — and the right-hand one is the dangerous direction.")
    d.notes(s,
           "Where this curve comes from, because without it the S is an "
           "assertion.\n "
           "Fix alpha. Draw the made-against-removed picture from the last "
           "surface. Mark every crossing. That column of crossings is one "
           "vertical slice of this plot. Now sweep alpha and collect them "
           "all. That is the whole construction, and it is worth saying "
           "slowly because the two figures look unrelated otherwise.\n "
           "Then what a saddle-node IS, which is not \"the curve bends\". At "
           "the dashed lines two crossings MERGE and disappear. In the "
           "previous picture that is the moment the production and removal "
           "curves stop intersecting and become TANGENT. A tangency, not a "
           "crossing — the stable and unstable states annihilate each "
           "other.\n "
           "Session 8 and 9's machinery, applied to a one-species system. "
           "Same S-curve, same two saddle-nodes, same wedge, and they did "
           "it for two species in September.\n "
           "The asymmetry is the design consequence and it is the thing to "
           "leave them with. At the left edge the ON state is born. At the "
           "right edge the OFF state is DESTROYED — push the synthesis "
           "rate too hard and the low state and the unstable state "
           "annihilate, leaving only ON. You lose the ability to switch "
           "the circuit off, and you lose it by turning a knob that looks "
           "like it should only make the signal stronger.\n "
           "Provenance, once: the mechanism is Tan's, the parameter values "
           "reach us through a later paper quoting them, and these two "
           "panels are our reproduction of the published model rather than "
           "a replication of their figures.")


# -------------------------------------------------------------- 8 · ledger ---
def _ledger(d):
    s = d.light()
    d.header(s, "segment 8", "the design ledger")
    d.title(s, "You cannot insulate. So what can you do?")
    d.rows(s, [
        ("Lower the demand", "weaker RBS, lower copy number, shorter coding sequence — Gyorgy's 60% to 29%, from segment 5.", GREEN),
        ("Spend it better", "two designs with the same output can cost the host different amounts. Measure capacity, not output alone.", GREEN),
        ("Close a loop on burden itself", "the cell already senses burden: a few heat-shock (σ32) promoters fire hard when you overexpress. Ceroni 2018 put an sgRNA under one of them and let dCas9 throttle the construct.", AMBER),
        ("Characterize in place", "and stop expecting the number to travel — Thursday's lesson, now with the host in it.", AMBER),
        ("What you cannot do", "give your circuit its own ribosomes. There is no junction to fix and no insulator to drop in.", RED),
    ])
    d.foot(s, "Before you look: what would YOU change first, and what would it cost you?")
    d.notes(s,
           "The sigma-32 row needs care, because the obvious story is not "
           "one the paper tells. Ceroni 2018 screened promoters, found "
           "nearly all the responders were sigma-32 dependent — ibpAB, "
           "dnaKJ, htpG — and says plainly that \"the precise mechanisms "
           "behind their activation are not fully understood\". The sensor "
           "is established. The mechanism is open.\n "
           "If a student offers the chaperone-titration story — misfolded "
           "protein pulls DnaK off sigma-32 and frees it — I say that is "
           "the textbook picture and that this paper does not claim it. "
           "Ceroni's own discussion suggests chaperones may be an "
           "additional KIND of burden rather than the sensing step.\n "
           "Thirty seconds of history that I like: Dong, Nilsson and "
           "Kurland in 1995 already saw DnaK and GroEL rise under "
           "gratuitous overexpression, by roughly 90 and 27 percent. Seen "
           "in 1995, mapped transcriptome-wide in 2018, mechanism still "
           "open. That is a fair picture of how much of this field works.\n "
           "The numbers exactly: promoter activity rose up to 50-fold in "
           "DH10B and 10-fold in MG1655. The controller runs off htpG1 "
           "specifically, and the dCas9 is CONSTITUTIVE — it is the sgRNA "
           "that is burden-driven. I do not say \"a dCas9 driven by "
           "sigma-32 promoters\".\n "
           "The last row is what distinguishes today from Thursday and I "
           "say it plainly. Session 17's problem had an engineering "
           "answer: manufacture the boundary. This one does not, at least "
           "not yet. Orthogonal ribosomes exist in the literature and are "
           "worth naming as the attempt, but they do not remove the "
           "constraint.")


def _close(d):
    s = d.dark()
    d.header(s, "close", "where this goes")
    d.title(s, "The same mechanism, three times")
    d.rows(s, [
        ("Tuesday just gone — session 18",
         "a transcription factor held by its decoy sites. You called that ultrasensitivity, and the holding is what made it sharp."),
        ("TODAY — session 19",
         "a ribosome held by every other mRNA in the cell. The same holding — and this time there is no boundary you can put around it.", CYAN),
        ("Thursday — session 21",
         "a regulator held by its own downstream targets. Retroactivity: a module loaded by the thing that is reading it."),
        ("and next Tuesday widens the axis",
         "session 20 runs the same conservation argument over metabolites, with the S matrix from session 3. Then the module next door, disturbance, evolution, the community."),
    ], label_color=CYAN, body_role="body")
    d.foot(s, "One mechanism, three sessions. Leave with burden, retroactivity and decoy titration as three unrelated topics and you have missed what connects them.")
    d.notes(s,
           "This is the surface the hour exists for, and session 18 ended "
           "on the same one. Same shape, second instance — if they "
           "recognise that, the ladder is built.\n "
           "The middle row is today and it carries the weight. "
           "Sequestration is not an analogy between the three: it is "
           "literally the same move each time — something that should be "
           "free is held by something that binds it, and the holding is "
           "what produces the behaviour. On Tuesday the holding made a "
           "response sharp. Today it coupled two genes with no wire "
           "between them. On Thursday it will make a module's output "
           "depend on who is listening.\n "
           "The fourth row is a DIFFERENT axis and I say so, because these "
           "two were blurred on this surface before. Session 20 is not a "
           "fourth rung of the sequestration ladder — it is the host's "
           "economy again at the level of metabolites, and it opens the "
           "run of contexts that fills the rest of Part II.\n "
           "If they leave with burden, retroactivity and decoy titration "
           "as three unrelated topics, the rest of Part II will not cohere "
           "and I will be re-explaining it in session 24.")

    # The assignment gets its own surface. Putting it under the ladder rows
    # collided with the foot -- assignment() starts at y=5.55 and the foot
    # sits at 6.75.
    s = d.light()
    d.header(s, "close", "before Tuesday")
    d.title(s, "What to read, and what is due")
    d.rows(s, [
        ("tonight, 11:59", "PS6 is due."),
        ("today", "PS7 goes out. It covers Thursday, Tuesday and today — parts and context, the covalent cycle, and shared resources."),
    ], top=2.05)
    d.assignment(s, y=3.60)
    d.notes(s,
           "PS7 is posted today and PS6 is due tonight. Both, and what PS7 "
           "covers.\n "
           "Fong and Palsson is three pages in which a model predicts a "
           "growth rate, somebody builds the strain, evolves it, and "
           "checks. They should come with a guess about what the failures "
           "have in common.")
