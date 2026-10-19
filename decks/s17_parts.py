"""Session 17 — Parts, context, and why composition is not composition.

Thursday 22 October 2026. M2 (Specific Aims and the model) is due today.

WHAT THIS SESSION IS. Session 16 ended on a number: the parts set was the
limit, not the design method. The obvious next question is "so what is a
part?" -- and the answer this session gives, Adam's framing of 18 October, is
that there isn't one. Not physically and not functionally.

    1. No crisp physical boundary. 5'-RACE pins a transcription start and
       nothing else. Strength lives in the flanking DNA, the host, ribosome
       availability. The promoter is not contained in the sequence you
       ordered, and the model for how it shifts with context is not known.
    2. Composition is reciprocal. Joining a promoter to something downstream
       changes that thing AND itself -- the transcript's 5'UTR, which the
       junction encodes, sets RNA stability.
    3. There is no agreed model or measurement set that settles either.

Point 2 is the one that does structural damage, and it is the spine of the
hour. Every abstraction this course has used -- mass action, QSSA, transfer
curves, truth tables, the compositor -- assumes composition leaves the
operands alone and combines their behaviours. It does not. That is not
context bending a model; it is composition failing to be composition.

THE CLOSE IS NOT NIHILISM, and this matters. Cello still got 45 of 60. It got
there by MANUFACTURING parts: insulated gates, one characterisation context,
fixed junctions. A part is manufactured, not discovered. The session's last
move is the catalogue of manufacturing moves and what each one costs.

SCOPE. Narrowed to five segments on Adam's call, 18 October: CRISPRi/a and
bridge RNAs become a closing slide pointing at S18, and enzymatic synthesis,
syn1.0 and syn3A move to S19. The published syllabus promised the first two
on Thursday, so SAY THE NARROWING OUT LOUD rather than letting the room
notice the syllabus and the lecture disagree.

HOW IT IS BUILT. Four moves per segment -- frame, build, release, debrief --
`docs/lecture-design.md` 5e. Every number on these slides comes from
`figures/s17_parts.py`, which recomputes from the papers' own data at render
time; the terminator panel reads `figures/data/s17_cambray_terminators.csv`.

NO PRINTED TIME RANGES. Settled; minutes are Adam's.

Run:  python tools/build_decks.py s17
"""
from decks.theme import (Deck, M, W, TEAL, CYAN, AMBER, MINT, INK, MUTED,
                         WHITE, SILVER, RED, GREEN)
from decks.theme import ROOT

FIG = "figures/build/"
FILENAME = "s17-parts"


def _fig(d, s, name, y, dpi=160):
    """Place a figure at its NATURAL size, centred, and return its bottom.

    Same contract as session 16: width = pixels/dpi, so the deck neither
    enlarges nor shrinks it and a point authored in the figure is a point on
    the slide. figures/s17_parts.py gates every figure against the slide's
    usable width and body height for exactly this reason.
    """
    from PIL import Image
    w, h = Image.open(ROOT / FIG / f"{name}.png").size
    w, h = w / dpi, h / dpi
    # The deck's overlap gate compares TEXT SHAPES, so it cannot see a line of
    # text baked into a PNG landing on the foot. Four figures did exactly that
    # on the first build of this session. foot() defaults to y=6.75.
    FOOT_Y = 6.75
    if y + h > FOOT_Y - 0.10:
        raise AssertionError(
            f"{name}: placed at {y:.2f}in, {h:.2f}in tall, so it ends at "
            f"{y + h:.2f}in and runs into the foot at {FOOT_Y}. Shorten the "
            f"figure in figures/s17_parts.py -- cut content, not type.")
    d.image(s, FIG + f"{name}.png", (W - w) / 2, y, w, h)
    return y + h


def build():
    d = Deck("Session 17 — Parts, context, and composition", session=17)
    d.show_badges = False
    _opening(d)
    _retrieval(d)
    _frame_context(d)
    _no_such_thing(d)
    _how_badly(d)
    _where_it_works(d)
    _manufacture(d)
    _composing(d)
    _close(d)
    return d


def _opening(d):
    s = d.dark()
    d.text(s, "Session 17  ·  Part II", M, 2.25, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "There is no such thing as a promoter",
           M, 2.72, 8.3, 1.6, size=38, font="head", bold=True, color=WHITE)
    d.text(s, "Tuesday ended on a parts set that ran out. Today: what a "
              "part is, and why the question has no clean answer.",
           M, 4.50, 8.6, 0.9, size=18, color=MINT, spacing=1.2)
    d.text(s, d.date_line, M, 6.45, 9.0, 0.4, size=13, color=SILVER)
    d.image(s, "docs/assets/posb-logo-520.png", W - M - 2.9, 2.05, 2.9, 2.9)
    d.notes(s, "The title is deliberately too strong and you will walk it "
               "back to exactly the right strength by the end of segment 1. "
               "Do not soften it here.\n"
               "M2 is due tonight at 11:59. Say that first, in one line, "
               "before anything else.")


def _retrieval(d):
    s = d.light()
    d.header(s, "retrieval", "Three minutes  ·  no notes")
    d.title(s, "Three things from Tuesday")
    d.rows(s, [
        ("the number Cello ended on", "45 of 60 circuits worked. What was the limit -- the design method, or something else?"),
        ("the cold-start rule", "a gene is safe if its promoter needs an activator and no repressor it depends on arrives later. Why does an ABSENT repressor cause the glitch?"),
        ("from session 13", "a gate's transfer curve has a gain. What did we have to measure to get one?"),
    ])
    d.foot(s, "The third one is the hinge. You measured a gate in one place. Today: does that number travel?")
    d.notes(s, "Third answer: you measured it -- in one context, one "
               "plasmid, one host. Let that sit. The whole hour is whether "
               "that measurement means anything anywhere else.")

    s = d.light()
    d.header(s, "goals", "What the hour is for")
    d.title(s, "Where today goes")
    d.rows(s, [
        ("first, a definition that fails", "try to say what a promoter IS, physically. Three different ways the object refuses to have edges."),
        ("then, the measurement", "twelve thousand combinations, and how much of the answer the parts actually account for."),
        ("then, what engineers do", "you do not find a part that composes. You build one. Four moves, and what each removes."),
        ("then, putting them together", "overhangs on the bench, compositors in code -- and the honest note about where the compositor's numbers came from."),
    ])
    d.foot(s, "The syllabus also promised CRISPRi/a and bridge RNAs today. They move to Tuesday; you get the idea on one slide at the end.")
    d.notes(s, "SAY THE SYLLABUS CHANGE OUT LOUD, here, in one sentence. "
               "They can read the syllabus. Narrowing it quietly is worse "
               "than narrowing it.")


# ---------------------------------------------------------------------------
# FRAME — what "context" means, before any measurement lands.
#
# Adam, 18 October: Cardinale & Arkin is the paper that lets students
# understand context rather than just meet it. Vocabulary first. Every
# example on these slides is from that paper and is quoted, not recalled.
# ---------------------------------------------------------------------------
def _frame_context(d):
    s = d.light()
    d.header(s, "frame", "Cardinale & Arkin 2012")
    d.title(s, "Three kinds of context, named")
    d.rows(s, [
        ("compositional", "what the neighbours do to you. PHYSICAL: parts on the same DNA, RNA or polypeptide interacting. FUNCTIONAL: two things competing for one shared output — the name for that is retroactivity, and it gets its own session in November."),
        ("host", "what the cell does to you. Parasitic interactions with its own machinery; competition for ribosomes, tRNAs and proteases; and coupling to growth, replication and partitioning."),
        ("environmental", "what the world does to you — directly, and through the host's response to it."),
    ])
    d.foot(s, "Cardinale & Arkin, Biotechnol J 7:856–866 (2012). The categories are theirs; keep the names.")
    d.notes(s, "Give them the three words now and use them for the rest of "
               "the hour. Without the vocabulary, 'context dependence' is a "
               "complaint. With it, it is a diagnosis you can act on -- "
               "different classes have different fixes, which is segment 4.")

    s = d.light()
    d.header(s, "frame", "the same three, with teeth")
    d.title(s, "What each one actually did to someone")
    d.rows(s, [
        ("compositional", "moving the operators on a two-input promoter changed its strength AND its logic. Spacers of 100–1000 bp failed to insulate tandem RNA attenuators; hammerhead ribozymes worked."),
        ("host", "a logic circuit using orthogonal Pseudomonas regulators failed in five of seven E. coli strains while its inputs were engineered E. coli promoters; swapping Plac for the exogenous Plux restored it. Separately: β-galactosidase at 30% of total cell protein halts growth."),
        ("environmental", "the lac promoter is repressed by 1% glucose and leaks in rich medium. Lower the temperature and λ PL gets stronger."),
    ])
    d.foot(s, "All six from Cardinale & Arkin 2012 and its references.")
    d.notes(s, "The spacer line is the one to land hard on: distance does "
               "not insulate. It comes back in segment 4 as the first row of "
               "the manufacturing table, and it is the reason insulators are "
               "DEVICES.\n"
               "The five-of-seven story is the best one on the slide and "
               "it is easy to tell wrong. The REGULATORS were already "
               "orthogonal — imported from Pseudomonas syringae. What broke "
               "it was the one native component left: engineered E. coli "
               "Plac and Pbad as the inputs. Replace Plac with the "
               "exogenous Plux and the circuit works.\n"
               "So orthogonality is not a property you get by importing "
               "most of your parts from elsewhere. One E. coli-derived "
               "element was enough.")


# ---------------------------------------------------------------------------
# SEGMENT 1 — the object refuses to have edges.
#
# Adam's three points, 18 October. The wrong turn is taught alongside the
# right one per the standing rule: the obvious reading is "a part's number
# moves with context, so measure it in more contexts". That is wrong in a
# way that matters -- point 2 says the parts are not separable objects, so
# there is no number belonging to the part to measure in the first place.
# ---------------------------------------------------------------------------
def _no_such_thing(d):
    s = d.light()
    d.header(s, "segment 1", "frame")
    d.title(s, "Draw the boundary")
    d.rows(s, [
        ("on the bench", "you order a promoter. Some number of bases of DNA arrives in a tube. Where does the promoter start and where does it stop?"),
        ("the best answer we have", "5′-RACE sequences the transcript and tells you where transcription STARTED. That is one edge."),
        ("the other edge", "there isn't one. Not operationally, not in the annotation, not in any model."),
    ])
    d.foot(s, "Hold the question open. It does not get answered in this segment; it gets replaced.")
    d.notes(s, "Ask the room to commit to a number of bases before you move "
               "on. Someone will say 'the −35 and −10 plus a bit'. Ask how "
               "much is a bit, and what sets it.")

    s = d.light()
    d.header(s, "segment 1", "build  ·  three failures, not one")
    d.title(s, "Why the object has no edges")
    d.rows(s, [
        ("1 · no boundary", "5′-RACE pins where transcription started. There is no second edge — not operationally, not in the annotation, not in any model."),
        ("2 · it is not contained", "the strength depends on the flanking DNA, on the host, on ribosome availability. Those are not in the tube. And we do not have a model for how they move it."),
        ("3 · joining changes both", "the transcript's 5′UTR is encoded at the junction. The 5′UTR sets RNA stability. So attaching a promoter to a gene changes the mRNA's lifetime — and the RNA level you were about to call 'promoter strength'."),
    ])
    d.foot(s, "Number 3 is the one that breaks something you already rely on. A fourth: there is no agreed measurement set that would settle any of it.")
    d.notes(s, "Same numbering as the handout front page. Spend the time "
               "on 3. Mass action, QSSA, transfer curves, "
               "truth tables, the compositor -- every abstraction in this "
               "course assumes that composing A and B leaves A and B alone "
               "and combines their behaviours.\n"
               "If joining alters the operands, that is not context bending "
               "a model. It is composition failing to be composition.")

    s = d.light()
    d.header(s, "segment 1", "release  ·  two minutes, with a neighbour")
    d.title(s, "You measured a promoter. Now move it.")
    d.rows(s, [
        ("what you did", "measured output from your promoter on a high-copy plasmid, GFP downstream, in DH5α, in LB, at 37 °C."),
        ("what you are about to do", "put the same promoter on the chromosome, in front of a different gene, in a production strain, in minimal medium."),
        ("name four things", "that could move the number — and for each, say which of Cardinale's three classes it is. The handout asks for the same four."),
    ])
    d.foot(s, "Four. Named and classified. Not a list of everything that could go wrong.")
    d.notes(s, "The classification is the work, not the list. Anyone can "
               "name five worries; the skill is knowing that 'different "
               "gene downstream' is COMPOSITIONAL and 'minimal medium' is "
               "ENVIRONMENTAL, because those two have different fixes.")

    s = d.light()
    d.header(s, "segment 1", "debrief")
    d.title(s, "What the room usually says, and which one is special")
    d.rows(s, [
        ("copy number — host", "chromosome versus high-copy. You can model this one: it is a multiplier, and you already have it."),
        ("medium and strain — environmental and host", "you cannot model these, but you can hold them fixed and report them. That is what a characterisation context IS."),
        ("the different gene downstream — compositional", "this one is different in kind. It does not shift the number — it means the number was never a property of the promoter alone."),
    ])
    d.foot(s, "The first two make the measurement harder. The third makes the thing you were measuring not exist.")
    d.notes(s, "Make the distinction explicit, because the obvious response "
               "to this whole session is 'fine, measure in more contexts'. "
               "That answers the first two and not the third.\n"
               "Then: so how bad is the third, actually? Next segment is a "
               "number.")


# ---------------------------------------------------------------------------
# SEGMENT 2 — how badly, measured. Kosuri 2013 and Cambray 2018.
#
# The figure carries its own caveat that these are two decompositions and not
# one measurement; say it aloud too.
# ---------------------------------------------------------------------------
def _how_badly(d):
    s = d.light()
    d.header(s, "segment 2", "frame")
    d.title(s, "How would you find out if parts compose?")
    d.rows(s, [
        ("the claim to test", "protein out = (what the promoter does) × (what the RBS does). Two numbers, multiplied. That is what a parts list promises."),
        ("the experiment that tests it", "take every promoter crossed with every RBS and measure them all. 114 × 111 = 12,654, less one that created an incompatible restriction site."),
        ("what you get to compare", "the prediction from the two numbers alone, against the measurement of the pair."),
    ])
    d.foot(s, "Kosuri, Goodman, Cambray, Mutalik, Gao, Arkin, Endy & Church, PNAS 110:14024–14029 (2013). 12,653 constructs.")
    d.notes(s, "Make them state the multiplicative model before they see "
               "the result. It is the model they have been using all term "
               "without writing it down.")

    s = d.light()
    d.header(s, "segment 2", "the paper  ·  what they built")
    d.title(s, "12,653 constructs, and how you measure that many")
    d.paper_figure(s, "kosuri2013_fig1", 0.9, 1.7, 11.53, 2.52,
                   "Kosuri et al., PNAS 110:14024–14029 (2013), Fig. 1A",
                   "Design all 114 × 111 combinations; synthesise them as an "
                   "oligo library; clone into one vector carrying sfGFP and a "
                   "constitutive mCherry; then DNASeq, RNASeq, and FlowSeq.")
    d.foot(s, "FlowSeq: sort the population into 12 log-spaced bins by sfGFP/mCherry ratio, sequence each bin, reconstruct each construct's level from where its reads landed.")
    d.notes(s, "Three things to say before any result.\n"
               "GOAL: not 'how strong is this promoter' but 'does the pair "
               "behave like the product of its parts'. You can only ask that "
               "if you have every pair.\n"
               "CONSTRUCT: Agilent oligo synthesis, ~50-fold coverage, one "
               "medium-copy vector, sfGFP as the output and **mCherry on the "
               "same plasmid as an internal ratio control**. That control is "
               "there to divide out exactly the context effects we are about "
               "to discuss — the instrument has the same disease as the "
               "thing it measures.\n"
               "MEASUREMENT: FlowSeq. Nobody pipetted 12,653 cultures.")

    s = d.light()
    d.header(s, "segment 2", "build")
    d.title(s, "Where the variance actually lives")
    _fig(d, s, "s17_variance", 1.95)
    d.foot(s, "Kosuri 2013, ANOVA. Cambray, Guimaraes & Arkin, Nat Biotechnol (2018) — 244,000 designed sequences.")
    d.notes(s, "Walk the three bars in order.\n"
               "RNA: the promoter does own the RNA level, 92%. The parts "
               "list works here.\n"
               "Protein: the RBS takes 30% of the variance in a quantity "
               "you attribute to the promoter.\n"
               "Then the third bar, and slow down: DIFFERENT question. Not "
               "'which part' but 'what about the sequence'. 28%. The part "
               "identity predicts; the part sequence does not.")

    s = d.light()
    d.header(s, "segment 2", "release  ·  commit to a number")
    d.title(s, "Predict one, then I'll tell you the tail")
    d.rows(s, [
        ("you have", "promoter P, measured. RBS R, measured. Both characterised alone, carefully, in the same strain and medium."),
        ("predict", "the protein level of P + R. Write down your number and a tolerance you would defend to a collaborator."),
        ("the question", "how often does a twofold tolerance hold? And when it fails, by how much?"),
    ])
    d.foot(s, "Everyone writes a tolerance. Nobody gets to say 'about right'.")
    d.notes(s, "Make them commit to the tolerance, not the number. The "
               "tolerance is the engineering claim.")

    s = d.light()
    d.header(s, "segment 2", "the other paper  ·  what they built")
    d.title(s, "244,000 sequences, designed — not sampled")
    d.paper_figure(s, "cambray2018_fig1", 2.68, 1.7, 7.98, 4.05,
                   "Cambray, Guimaraes & Arkin, Nat Biotechnol (2018), Fig. 1A",
                   "A full factorial over nucleotide, secondary-structure, "
                   "codon and amino-acid properties — 56 replicates of the "
                   "design — read out as transcript abundance and decay, "
                   "polysome profiles, protein, and growth rate.")
    d.foot(s, "The reporter is standardised to the hilt — fixed flanks, a designed 96-nt N-terminal window, His tag, TEV site, linkers into sfGFP — so the designed variation is the only variation.")
    d.notes(s, "GOAL: not 'what is this sequence worth' but 'which sequence "
               "properties cause translation efficiency, disentangled from "
               "each other'. That is why it is a factorial design and not a "
               "library screen — screens confound.\n"
               "CONSTRUCT: again, an instrument built to be insulated. And "
               "note what they measured: not just protein, but transcript "
               "DECAY and polysome profiles, because the mechanism they "
               "expected involves both.\n"
               "Then the result, and it is humbling.")

    s = d.light()
    d.header(s, "segment 2", "debrief")
    d.title(s, "Twofold holds about two-thirds of the time")
    d.rows(s, [
        ("the bulk", "80% of RNA levels and 64% of protein levels land within twofold of the multiplicative prediction. R² 0.92 on RNA, 0.76 on protein."),
        ("the tail", "the largest 5% of protein deviations are off by an average of 13-fold. That is the number that kills a ten-gene design."),
        ("the reciprocity, measured", "a 10-fold change in TRANSLATION efficiency moves RNA abundance about 3-fold. The downstream element reaches back and changes the transcript level."),
        ("and the deeper one", "in 244,000 designed sequences, design properties explain 28% of that library's variance. And sequences those properties score as EQUIVALENT — 1 to 4 mutations apart — differ by 8% of total variance, well above experimental error."),
    ])
    d.foot(s, "Secondary structure around the start codon accounts for 83% of what the design properties do explain.")
    d.notes(s, "The 10×→3× line IS point 2 from segment 1, with a number. "
               "Say that explicitly -- it is the same claim, now measured.\n"
               "Be exact about the 8%. It is NOT three builds of one part. "
               "It is three sequences within a mutational series, 1-4 "
               "mutations apart and >95% identical, which the design "
               "properties score the same. They differ by more than the "
               "instrument's error. So the scoring, not the building, is "
               "what fails -- the properties we use to describe a sequence "
               "do not capture what the cell responds to.")


# ---------------------------------------------------------------------------
# SEGMENT 3 — where prediction DOES work, and what that costs.
#
# This segment exists to stop the session being a complaint. Cambray's
# terminator model is near-exact -- on the class its features were identified
# over. The paper names the three classes it fails on. So predictability is a
# property of how tightly the class is drawn.
# ---------------------------------------------------------------------------
def _where_it_works(d):
    s = d.light()
    d.header(s, "segment 3", "frame")
    d.title(s, "Is any of this predictable from sequence?")
    d.rows(s, [
        ("the honest answer", "yes, sometimes. Cambray fitted a LINEAR model — four sequence features chosen by stepwise selection out of twelve candidates, on 31 curated terminators. The features are biophysically motivated: hairpin stability normalised by length, the U-tail, the closing base pair."),
        ("two groups, same year", "Cambray et al. in NAR and Chen et al. in Nature Methods both published sequence → strength terminator models in 2013, from different data."),
        ("which is itself the third failure", "two models, no agreed measurement set to adjudicate them."),
    ])
    d.foot(s, "Chen et al. measured 582 terminators — 227 annotated, 90 of those also reversed, 265 synthetic — and found 39 strong ones.")
    d.notes(s, "Do not present Chen as 'the catalogue' and Cambray as 'the "
               "model'. Chen built a model too. The point is that there are "
               "two of them.\n"
               "582 to 39 is a 6.7% yield. Park that; it comes back.")

    s = d.light()
    d.header(s, "segment 3", "the paper  ·  what they built")
    d.title(s, "How do you measure a terminator at all?")
    d.paper_figure(s, "cambray2013_device", 0.9, 1.7, 11.53, 4.07,
                   "Cambray et al., NAR 41:5139–5148 (2013), Fig. 1",
                   "A measurement device: green and red fluorescent reporters "
                   "bracketing the terminator test site, with RNase III sites "
                   "flanking it to standardise the ends of the processed "
                   "mRNA.")
    d.foot(s, "Read-through is estimated as the ratio of downstream to upstream fluorescence; termination efficiency is what is left. 100% means every arriving complex was stopped.")
    d.notes(s, "THIS SLIDE IS THE SESSION IN MINIATURE and it is worth the "
               "time.\n"
               "You cannot measure a terminator by measuring one reporter, "
               "because you would be measuring the promoter too. So you "
               "bracket it and take a ratio.\n"
               "But a ratio is still contaminated: mRNA stability differs "
               "either side of the terminator. So they put **RNase III sites "
               "around the test site to standardise the processed ends**. "
               "They tried RNase E too and it was worse -- coefficient of "
               "variation 0.37 against 0.15 -- so the device they kept is "
               "the RNase III one. Even the choice of insulator was "
               "measured.\n"
               "In other words: before they could measure a part, they had "
               "to INSULATE THEIR OWN INSTRUMENT. The measuring device has "
               "the same disease as the thing being measured, and they "
               "solved it the same way we will solve it in segment 4 — by "
               "imposing boundaries.\n"
               "The paper also says, in its introduction, that diverse "
               "characterisation strategies have hindered comparison of "
               "measurements. That is point 3, in their words.")

    s = d.light()
    d.header(s, "segment 3", "build")
    d.title(s, "Good on what it was trained on. Wrong, in named ways, outside.")
    _fig(d, s, "s17_terminator_model", 1.95)
    d.foot(s, "Residuals recomputed from Suppl. Table 1; classes are the paper's. The paper reports r = 0.9 (cross-validated 0.85) on the 31 curated, and r = 0.67 (CV 0.61) across all 54.")
    d.notes(s, "SAY THE TRAINING SET OUT LOUD. The 31 teal points are the "
               "terminators the model was FITTED on, with four features "
               "chosen by stepwise selection from twelve. A tight fit there "
               "is partly just that. The paper is straight about it: r = "
               "0.9, cross-validated 0.85.\n"
               "The other 23 were held out, and they do not fail randomly "
               "— they fail DIRECTIONALLY, and the paper names each one. "
               "Low-efficiency terminators are overestimated by a median "
               "of 44 points. Low-folding ones are overestimated. Extended "
               "terminators are UNDERESTIMATED, by about 8.\n"
               "A model that is wrong unpredictably is useless. A model "
               "that is wrong in three named directions tells you when not "
               "to trust it, which is most of what you want.")

    s = d.light()
    d.header(s, "segment 3", "debrief  ·  the move to take away")
    d.title(s, "Prediction is a property of the definition")
    d.rows(s, [
        ("what the model predicts", "not 'terminators'. Things that are terminators in the model's sense — a hairpin of the right kind, a U-tract of the right kind. The curated set defines the class, and it is also the training set."),
        ("so the boundary is doing the work", "cross-validated inside the curated class, r = 0.85. Outside it, the same model is off by a median of 44 points on the low-efficiency ones — and in a direction the paper can name."),
        ("which answers segment 1", "you cannot find the edges of a part. You can IMPOSE them. The imposition is the engineering."),
    ])
    d.foot(s, "This is the hinge of the hour. Everything after it is imposition.")
    d.notes(s, "Say the last line slowly. The session's title was 'there is "
               "no such thing as a promoter' and this is where it becomes "
               "'...until you build one'.")


# ---------------------------------------------------------------------------
# SEGMENT 4 — manufacture the part. Adam, 18 October: "it is a manufacturing
# lesson -- you can manufacture to make parts more composable and
# predictable."
#
# The rival strategy is in here honestly: Kosuri's own paper concludes you
# should screen libraries rather than predict or standardise. Two papers,
# same year, overlapping authors, opposite prescriptions.
# ---------------------------------------------------------------------------
def _manufacture(d):
    s = d.light()
    d.header(s, "segment 4", "frame")
    d.title(s, "Three things you can do about it")
    d.rows(s, [
        ("model it", "find the sequence features that set the number. Works when the class is tight — segment 3. Does not work for promoters or RBSs."),
        ("build the context away", "change what the part IS so the abstraction becomes true. This is what insulation means."),
        ("give up on prediction and screen", "build the library, measure it, pick the ones that landed where you wanted."),
    ])
    d.foot(s, "All three are in the literature. Two of them are in the same year, from overlapping author lists, recommending opposite things.")
    d.notes(s, "Do not resolve this yet. The room should feel that the "
               "field has not settled it, because it has not.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  what insulation actually is")
    d.title(s, "Not distance. A device.")
    _fig(d, s, "s17_insulators", 1.95)
    d.foot(s, "Cardinale & Arkin 2012; Davis & Sauer, NAR 2011; Qi, Doudna & Arkin, Nat Biotechnol 2012; Lou & Voigt, Nat Biotechnol 2012; Mutalik et al., Nat Methods 2013.")
    d.notes(s, "Start at the top row and let it be a surprise: a kilobase "
               "of spacer does not insulate. Space is not separation.\n"
               "Then the two RNA rows -- same disease, two cures, published "
               "months apart in the same journal and volume. Csy4 cuts the "
               "transcript at a fixed site; RiboJ cleaves itself. Either "
               "way the 5'UTR stops depending on which promoter is "
               "upstream, which is EXACTLY point 2 from segment 1.\n"
               "Last row: the bicistronic design does it by construction -- "
               "every transcription element encodes the same mRNA start.")

    s = d.light()
    d.header(s, "segment 4", "the paper  ·  what they built")
    d.title(s, "An expression operating unit")
    d.paper_figure(s, "mutalik2013_eou", 0.9, 1.7, 11.53, 3.84,
                   "Mutalik et al., Nat Methods (2013), Fig. 1A",
                   "Upstream insulator, transcription element, translation "
                   "initiation element, the gene, 3′UTR, terminator, "
                   "downstream insulator — every boundary named and fixed, "
                   "with a standard +1 promoter:5′UTR junction inside it.")
    d.foot(s, "Their own words: an expression operating unit defined 'to set boundaries and junctions of functional genetic elements'.")
    d.notes(s, "Read their phrase out loud: SET BOUNDARIES AND JUNCTIONS. "
               "Segment 1 said the object has no edges. This is a group "
               "deciding to supply them.\n"
               "The key move is the common +1: every transcription element "
               "emits the same mRNA start, so the promoter can no longer "
               "reach downstream and change the transcript through the "
               "5'UTR it would otherwise encode. That is point 2, designed "
               "out of existence.\n"
               "Then the number.")

    s = d.light()
    d.header(s, "segment 4", "build  ·  what it buys")
    d.title(s, "Predict it: 47%.  Build it: 93%.")
    _fig(d, s, "s17_manufacture", 1.95)
    d.foot(s, "Both numbers from Mutalik et al., Nat Methods (2013) — the same question, the same twofold tolerance, the predictor's figure quoted in their own introduction.")
    d.notes(s, "One metric, measured one way, both numbers from the same "
               "paper: the chance of landing within twofold of a TARGET "
               "expression level. The best computational predictor gets "
               "~47%. Their manufactured elements get ~93%.\n"
               "This is the cleanest statement of the whole session. You "
               "did not get better at predicting. You changed what you were "
               "predicting ABOUT.\n"
               "Do NOT put Kosuri's 64% next to this -- that is prediction "
               "accuracy over a combinatorial library, a different "
               "question, and it already has its own slide in segment 2.")

    s = d.light()
    d.header(s, "segment 4", "the other road  ·  screening, and its price")
    d.title(s, "Or: stop predicting, and pay for it in throughput")
    d.rows(s, [
        ("Kosuri's own conclusion", "rather than relying on prediction or standardisation, build and screen large libraries. From the same paper that measured the 13-fold tail."),
        ("Chen's terminators", "582 measured → 39 strong enough to use, with enough sequence diversity not to recombine. A 6.7% yield."),
        ("Stanton's repressors", "73 TetR-family repressors mined from genomes → 16 that both repress their own promoter, 5- to 207-fold, and leave the others alone. 22%."),
        ("and what 16 buys", "as NOT/NOR gates, more than 10⁵⁴ distinct circuits. The scarcity is in the parts, never in the designs."),
    ])
    d.foot(s, "Chen et al., Nat Methods (2013); Stanton, Nielsen, Tamsir, Clancy, Peterson & Voigt, Nat Chem Biol (2014).")
    d.notes(s, "Tie back to Tuesday: 34 integrases gave 11 orthogonal, and "
               "45 of 60 Cello circuits worked. Four attrition numbers "
               "across two sessions.")

    s = d.light()
    d.header(s, "segment 4", "debrief  ·  the distinction worth having")
    d.title(s, "Two attritions that are not the same thing")
    d.rows(s, [
        ("Chen: attrition on strength", "a property of the part by itself. Measure each one once, keep the strong ones. 582 measurements for 582 parts."),
        ("Stanton: attrition on orthogonality", "a property of the SET. No measurement of one repressor tells you whether it crosstalks. You screen pairs — n², not n."),
        ("why that matters", "better single-part models make the first cheaper and do nothing for the second. Orthogonality is a part's value given everything else in the cell."),
    ])
    d.foot(s, "This is 'a part is not a separable object' at its sharpest — and it is what Cello ran out of first.")
    d.notes(s, "If they take one thing from the segment, take this. It is "
               "also the honest answer to 'why not just measure more': "
               "because the thing you need to know is not a property of the "
               "thing you would be measuring.")


# ---------------------------------------------------------------------------
# SEGMENT 5 — composing anyway. T44 on the bench, T42 in code.
#
# Both assessed on PS7, not PS6: session 17 is taught two days before PS6 is
# due and an item cannot be assessed the week it is first seen. Settled
# 18 October; docs/coverage-matrix.md corrected the same evening.
# ---------------------------------------------------------------------------
def _composing(d):
    s = d.light()
    d.header(s, "segment 5", "frame  ·  T44")
    d.title(s, "Three ways to join two pieces of DNA")
    d.rows(s, [
        ("classic restriction cloning", "the junction is wherever a usable site happens to be, and that site STAYS in the product as a scar. One or two parts at a time, and the site has to be absent everywhere else."),
        ("Gibson assembly", "the junction is a 20–40 bp overlap you design into the ends. Scarless and one pot — but it is long, it is different for every pair, and repeated or similar sequences misassemble."),
        ("Golden Gate / MoClo", "the junction is FOUR BASES YOU CHOOSE. One pot, many parts, in a defined order, and the enzyme site is gone from the product."),
    ])
    d.foot(s, "All three work. Only one gives a SHORT, standardisable junction you can fix across a whole library — which is why it is the one that matters today.")
    d.notes(s, "Do not present this as a techniques slide. The question is "
               "WHICH METHOD GIVES YOU CONTROL OF THE JUNCTION, because "
               "this whole session has been about the junction being the "
               "context.\n"
               "Restriction cloning: the junction is chosen FOR you by "
               "which enzyme you could use.\n"
               "Gibson: the junction is the parts' own ends — fine, but you "
               "cannot standardise it across a library, and 20–40 bp of "
               "overlap is a lot of sequence to put somewhere unexamined.\n"
               "Golden Gate: four bases, chosen. That is why MoClo can fix "
               "a standard set of junctions for a whole community.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  how Golden Gate actually works")
    d.title(s, "The enzyme cuts outside its own site")
    _fig(d, s, "s17_type2s", 1.95)
    d.foot(s, "BsaI recognises GGTCTC and cuts one base downstream, leaving a four-base 5′ overhang whose sequence is whatever you put there.")
    d.notes(s, "This is the mechanism and it takes one minute. A Type IIS "
               "enzyme recognises one sequence and cuts at a fixed OFFSET "
               "from it. Put the recognition site on the scrap side and the "
               "cut lands inside your part's flank — so the site departs "
               "with the scrap and the product carries no site at all. That "
               "is what makes one-pot assembly possible: cut and ligate in "
               "the same tube, and correctly joined products stop being "
               "substrates.\n"
               "Then the right-hand column, which is the point for us. The "
               "freedom and the trap are the same four bases.")

    s = d.light()
    d.header(s, "segment 5", "release  ·  commit to a number, in writing")
    d.title(s, "So how many parts fit in one pot?")
    d.rows(s, [
        ("what you have", "four bases of free choice per junction. A circular assembly of n parts plus a backbone needs n + 1 junctions, and every one must be distinguishable from every other."),
        ("write down two numbers", "how many distinct overhangs you think are usable — and how many JUNCTIONS you could choose at random before two of them became too alike."),
        ("then defend the second one", "to a neighbour, in one sentence. What exactly goes wrong when two junctions are one base apart?"),
    ])
    d.foot(s, "Most rooms put the second number somewhere between twenty and two hundred. Keep in mind that four junctions is a three-part build.")
    d.notes(s, "Make them write both. The gap between the two numbers is "
               "the whole lesson, and it only lands if they have committed "
               "to the wrong one first.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  T44")
    d.title(s, "Fewer than you think")
    _fig(d, s, "s17_overhangs", 1.95)
    d.foot(s, "Counting is exact. The clash curve is a deliberately crude proxy — real assemblies use measured ligation fidelity, not one-base proximity.")
    d.notes(s, "Walk the counting: 256 four-base overhangs, 16 of them "
               "palindromic and so self-ligating, and each remaining one "
               "pairs with its reverse complement — 120 distinct junction "
               "identities, not 256.\n"
               "Then the curve, and say JUNCTIONS not parts -- the x-axis "
               "is junctions, and a circular n-part build needs n+1 of "
               "them. Choose at random and you are at even odds of a clash "
               "by about 4.2 junctions, which is a three-part assembly. "
               "That is why published standards ship a FIXED, designed "
               "overhang set rather than telling you to choose.\n"
               "Flag the toy explicitly. The real work is measured fidelity "
               "data; this is the shape of the problem, not its solution.")

    # ---- the worked example: design one -----------------------------------
    s = d.light()
    d.header(s, "segment 5", "build  ·  T44")
    d.title(s, "Design one: four junctions, none of them free")
    d.rows(s, [
        ("backbone:promoter", "the scar is upstream DNA — and upstream context moves promoter output. That was segment 1."),
        ("promoter:5′UTR", "at or near the transcription start. Whether the scar is transcribed AT ALL depends on where the TSS actually is, and the part definition does not say."),
        ("5′UTR:CDS", "immediately 5′ of the start codon — the window Cambray put 83% of the explained variance in."),
        ("CDS:backbone", "3′ of the stop codon. Transcript 3′ end, terminator context."),
    ])
    d.foot(s, "Three parts in a backbone is four junctions, and every one leaves four chosen bases behind in the product.")
    d.notes(s, "Make them do this on the handout BEFORE you put it up. Draw "
               "the construct on the board, four junctions, and ask what "
               "sequence each scar lands in.\n"
               "Then ask which one they would least like to choose freely. "
               "Expect 5'UTR->CDS, and that is a fine answer.\n"
               "The BETTER answer is promoter->5'UTR, and credit it higher: "
               "you cannot say whether that scar is inside the transcript "
               "without knowing the transcription start. The part definition "
               "does not tell you. 5'-RACE would. That is segment 1 arriving "
               "inside a design decision rather than as a slogan.\n"
               "Do not let 'there is no free junction' stay abstract. Every "
               "row here is a different part of the construct that you are "
               "editing whether you meant to or not.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  T44")
    d.title(s, "The junction you do not choose")
    d.rows(s, [
        ("the problem", "the junction nearest the start codon is the one you would least like to pick four arbitrary bases for."),
        ("the standard's answer", "fix it at AATG. The last three bases ARE the start codon — sequence the biology had already determined. The scar adds nothing that was not going to be there."),
        ("so the move is", "you do not make a junction harmless by choosing well. You make it harmless by putting it where there was no choice."),
    ])
    d.foot(s, "Plant common syntax (Phytobricks). The principle is general; this particular set is not universal.")
    d.notes(s, "This is the session's thesis in one design decision, and it "
               "is worth slowing down for.\n"
               "A part is manufactured, not found -- and so is the standard "
               "that lets parts be joined. The field did not get a safe "
               "junction by searching harder for four good bases. It moved "
               "the junction onto sequence that was already fixed.\n"
               "Good question for the room: where ELSE in a construct is the "
               "sequence already determined? The stop codon is the obvious "
               "second answer. A ribosome binding site is NOT -- which is "
               "why that junction is the hard one.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  T44")
    d.title(s, "Your rule rejects the set the field ships")
    _fig(d, s, "s17_standard", 1.95)
    d.foot(s, "Potapov et al., ACS Synth Biol (2018), 10.1021/acssynbio.8b00333 — all 256 overhangs profiled by single-molecule sequencing.")
    d.notes(s, "They apply the two-base rule on the handout first. Then this.\n"
               "The trap is worth naming out loud: compare TACT and GGTA "
               "directly and all four bases differ, so the pair passes and "
               "you never find it. The reverse complement is the step "
               "everybody skips.\n"
               "Then the assay: 93%. Do NOT let the room conclude the "
               "standard is flawed. The RULE is the approximation. Potapov "
               "profiled all 256 overhangs and concluded it is 'not "
               "necessary to exclude all pairs that have only a single "
               "mismatch' -- mismatch depends on WHICH bases differ and "
               "WHERE, not how many.\n"
               "One guard: the 93% is assemblies that come out correct; the "
               "curve on the last slide was the chance a randomly chosen SET "
               "contains a close pair. Different quantities. Do not let "
               "anyone subtract one from the other.\n"
               "Land it: the binding constraint on a one-pot assembly is a "
               "measurement someone made, not a count you can do at the "
               "board.")

    s = d.light()
    d.header(s, "segment 5", "build  ·  T42")
    d.title(s, "And in code: what a compositor is for")
    _fig(d, s, "s17_compositor", 1.95)
    d.foot(s, "A part as a reaction with named state-variable inputs — the form posb.Model and posb.Reaction already take.")
    d.notes(s, "The left picture is the one they have been using all term "
               "and it is not WRONG, it is just not able to express the "
               "thing segment 1 showed. There is nowhere in p × r to write "
               "down that joining changed p.\n"
               "The right picture can. That is the whole argument for the "
               "abstraction -- not elegance, expressiveness.\n"
               "Then the honest note: the parameters you would put in that "
               "model are the numbers segment 2 showed do not transfer. The "
               "compositor does not fix that. It makes it sayable.")

    s = d.light()
    d.header(s, "segment 5", "debrief")
    d.title(s, "Two kinds of composition, two kinds of constraint")
    d.rows(s, [
        ("physical composition", "a combinatorial constraint the functional design never sees. Nothing about your circuit's logic tells you that two junctions are one base apart."),
        ("functional composition", "a modelling constraint the physical layer never sees. Nothing about your overhang choice tells you the 5′UTR moved."),
        ("and they are not independent", "the junction you choose on the bench IS part of the 5′UTR the model needs. Golden Gate scars are not neutral."),
    ])
    d.foot(s, "T42 and T44 are assessed on PS7, not PS6 — you meet them today and use them in two weeks.")
    d.notes(s, "The third row is worth the time. It is the session's thesis "
               "arriving in the most practical possible place: a four-base "
               "scar you chose for cloning convenience is sequence inside "
               "the transcript, and sequence inside the transcript is what "
               "Cambray's 244,000 said dominates.")


# ---------------------------------------------------------------------------
# CLOSE — the certification question, then the forward slide.
#
# Adam, 18 October: point 3 is not "the field is stuck". A standard WAS
# proposed, by this group, in the same year as the BCD paper. It did not
# take. That is a better question to leave a room with than a complaint.
# ---------------------------------------------------------------------------
def _close(d):
    s = d.light()
    d.header(s, "close", "the measurement that would settle it")
    d.title(s, "Somebody did propose a standard")
    d.rows(s, [
        ("the gap", "manufacturing works — Cello is the proof. What is missing is certification: knowing in advance that a part, in a stated context, will hold its number."),
        ("the proposal", "an ANOVA framework for part performance, and a second statistic beside activity — part QUALITY, which tracks how much the activity moves across contexts."),
        ("published", "2013. Same group, same year as the bicistronic design. Thirteen years ago."),
        ("the question to leave with", "it did not take. Why not — and what would a standard have to offer a working lab for it to be worth adopting?"),
    ])
    d.foot(s, "Mutalik, Guimaraes, Cambray, Mai, Christoffersen, Martin, Yu, Lam, Rodriguez, Bennett, Keasling, Endy & Arkin, Nat Methods 2013.")
    d.notes(s, "This is the 247 project prompt hiding in plain sight. Say "
               "so.\n"
               "Do not answer the last question. It is open, and they "
               "should feel that it is open.")

    s = d.light()
    d.header(s, "close", "and the escape — Tuesday")
    d.title(s, "What if specificity were computable?")
    d.rows(s, [
        ("the problem all hour", "you cannot predict a protein–DNA part's function from its sequence, so you screen, and you pay the attrition."),
        ("CRISPRi/a and bridge RNAs", "specificity set by Watson–Crick base pairing instead of by protein–DNA coevolution. Small, and designable on paper."),
        ("why that changes the economics", "orthogonality stops being a property you discover by screening n² pairs and becomes one you write down."),
        ("Tuesday", "protein circuits — the other escape. Ultrasensitivity with no transcription at all, on a timescale of seconds."),
    ])
    d.foot(s, "Qi & Arkin, Nat Rev Microbiol 12:341–354 (2014). The syllabus promised these today; they get their model on Tuesday.")
    d.notes(s, "Close the loop on the scope change you announced at the "
               "start. They met the idea; S18 does the model.\n"
               "Last line out loud: a part is manufactured, not found. "
               "Everything today was about what the manufacturing costs.")

    s = d.light()
    d.header(s, "reading", "For Tuesday")
    d.title(s, "The reading for 27 October")
    d.assignment(s, y=2.30, label="For Tuesday 27 October")
    d.text(s, "A toggle switch with no promoter in it. Session 9's two stable "
              "states, built out of phosphorylation instead of transcription — "
              "and running in seconds rather than cell generations.",
           M, 5.30, W - 2 * M, 0.9, size=17, color=MUTED, spacing=1.2)
    d.notes(s, "This is the other escape from today's limit, and the one "
               "S18 actually takes. Point back at the closing slide: "
               "Watson–Crick specificity was escape one, changing the "
               "physical layer entirely is escape two.")

    s = d.dark()
    d.text(s, "Session 17  ·  what to carry", M, 2.1, 8.6, 0.4, size=16,
           bold=True, color=CYAN)
    d.text(s, "A part is manufactured, not found",
           M, 2.55, 9.0, 1.1, size=34, font="head", bold=True, color=WHITE)
    d.text(s, "The object has no edges, and joining two of them changes "
              "both. So you impose the edges, and the abstraction becomes "
              "true because you made it true.",
           M, 3.95, 8.8, 1.0, size=18, color=MINT, spacing=1.2)
    d.text(s, "Predicted: 47% within twofold.   Manufactured: 93%.",
           M, 5.45, 9.0, 0.45, size=20, color=CYAN, bold=True)
    d.text(s, "M2 is due tonight, 11:59 pm.  ·  Tuesday: protein circuits.",
           M, 6.20, 9.0, 0.4, size=16, color=SILVER)
    d.notes(s, "Hold this one up while they pack. The two numbers are the "
               "thing to leave in the room.")
