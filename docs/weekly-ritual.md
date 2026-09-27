# The weekly ritual

[← back to README](../README.md) · Companions:
[session-release-checklist](session-release-checklist.md) (per-session detail) ·
[course-site-runbook](course-site-runbook.md) (*why* each click is that way) ·
[instructor-setup](instructor-setup.md) (accounts) ·
[where-things-live](where-things-live.md)

**Everything for a teaching week is finished before that week begins.** Build
Friday, review Saturday, publish Sunday. From Monday morning the only operations
are teaching and uploading what the room produced.

Weekdays are packed and non-operational. Any step still open on Monday is a step
that will be done in a gap between meetings, on the morning it is needed, which
is the condition under which every defect in this document was originally made.

---

## Why this exists

The release checklist is *session*-shaped and gets run twice a week. That was
tolerable until two sessions, a problem set, an autograder, two Gradescope
assignments, two Canvas assignments and a reader brief all landed inside
forty-eight hours. Everything shipped. Everything also shipped **on the day it
was needed**:

- A deck was approved and copied to `private/taught/` at 16:43; the rebuild at
  18:33 gave it the board-cue icon it had been missing. Nobody would have seen
  that on the projector.
- Two Gradescope Docker images were built sixteen minutes apart from the same
  zip. Nothing in either system compares them.
- A Canvas description was written from a template that did not match the one
  actually in use.
- A session's handout, answer sheet and board notes did not exist at 7pm on the
  Monday before the Thursday they were needed.

Scheduling failures, not competence failures. The work was serialised against
the deadline instead of against itself.

---

## The week at a glance

| day | operations | gate |
|---|---|---|
| **Friday** | build both sessions + the problem set; **adversarially review both** | `preflight` exits 0 for both, after the review's fixes |
| **Saturday** | review on paper; approve; port back; rebuild | decks copied to `private/taught/` |
| **Sunday** | Gradescope, bCourses, modules, announcement, reader | final `preflight` exits 0 |
| **Mon–Fri** | teach; upload after class | nothing is built *against a design that is not settled* — see below |

`NN` = Tuesday's session, `MM` = Thursday's, `psPP` = the set released that week.

## Earlier is always allowed

**These are deadlines, not start times.** Adam's rule, 8 September 2026: he will
pull work forward whenever the week gives him room, and this document must not
be read as forbidding that. Friday is the day by which both sessions and the
problem set are *finished*; nothing about it says they may not be finished on
Wednesday.

Two conditions, and they are the whole of it:

1. **A session is built only against a settled design.** The gate is the
   design, not the day. Building from an unsettled plan is how you get a deck
   that has to be rebuilt after the plan changes, which costs more than waiting.
2. **Design never happens on build day.** This is the failure the ritual was
   originally written against, in its other form. Friday assumes a settled plan
   from F1 onward; a Friday that opens by designing a session has already lost
   its gate. Design work belongs *earlier* in the week — it is not a build, and
   the "nothing is built" rule does not reach it.

What does not move: **the Saturday review and the Sunday publish still happen**,
on paper and in that order, however early the build finished. Finishing
Wednesday buys a longer gap between building and reviewing, which is worth
having. It does not buy skipping the review.

Week 4 is the first week run this way — session 6's design was settled on
Sunday, so it was built Tuesday to Wednesday, and session 7 was designed
Thursday and built Friday. See `2026/SESSION-LOG.md`, 8 September.

---

# FRIDAY — build

Nothing here touches a browser. All of it is repeatable.

## Where each step runs

**New, 26 September 2026.** This document was written as if there were one
machine. There is not, and a step run in the wrong place fails in a way that
looks like a broken repository rather than a missing dependency.

| step | runs where | because |
|---|---|---|
| **F1, F7, S7** — all git | **Adam's terminal, always** | Anything else leaves `.git/index.lock` and blocks his own commits. No assistant, no bridge, no script runs git here — including `git status`. |
| **F2, F2b** — figures | **cloud container** | Needs scipy. The device VM does not have it. |
| **F3** — decks | **either** | Pure python-pptx. `--pdf` needs LibreOffice, which the device has. |
| **F4** — handouts | **cloud container** | Needs playwright and Chromium for MathJax rendering. |
| **F5** — problem sets | **cloud container** | Needs otter-grader and a registered `python3` kernel. |
| **F6, status.py** | **either** | Pure stdlib plus PyYAML. |

**When a build runs off-device, copy the artifact and its stamp together.** A
figure without its `.deps.json`, or a handout PDF without its `.build/*.sha`,
reads as stale on the machine that will open it. Both stamp files hash
*sources*, not the artifact's bytes, so they are valid wherever they were
computed — which is what makes this split safe.

**Verify the copy landed.** The bridge has reported success on writes that did
not take. Grep the destination for the change before believing it.

### F1 · Start from a clean tree

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026
git pull
git status                      # must be clean before you start
cd private && git pull && cd ..
```

A dirty tree on Friday means an edit from a previous week never landed. Resolve
it before building anything on top of it.

### F2 · Figures — both sessions

```bash
python tools/build_figures.py sNN sMM
python tools/build_figures.py --verify
```

**Expect:** "Every committed figure matches the code that made it."

- A new figure module must be added to `MODULES` in `tools/build_figures.py` or
  it is never built and its PNGs get no manifest. This has happened.
- `figures/style.py` is a dependency of *every* figure. If you touched it, run
  `python tools/build_figures.py` with no arguments and expect ~20 rewrites.
- The s02 movie is in `SLOW` and is only built when named:
  `python tools/build_figures.py s02_movie`. Needs ffmpeg. Takes a minute.

### F2b · Deep figure check — re-render and compare pictures

```bash
python tools/build_figures.py sNN sMM --deep
```

**Expect:** "Every committed figure is the picture its generator draws."

`--verify` above asks whether the recorded hashes still hold. It cannot answer
the question that actually bit us on 26 September: **is the committed PNG the
one this generator produces?** The committed `s10_iffl_adaptation.png` was the
*annotated* variant — peak, final and the adaptation error printed on a surface
three slides before those numbers are defined, and the same three numbers a
handout item and a hidden autograder test ask students to produce. The
generator was correct throughout. Only the artifact was wrong, and it carried a
manifest written from its own bad bytes, so `--verify` called it clean.

`--deep` renders every figure into a scratch directory and compares decoded
pixels. Slower. It is the only check that catches a committed figure which is
simply the wrong picture, so run it at least on the week's two sessions.

> **Why the manifest hashes pixels and not bytes.** The bridge that moves files
> between the build machine and the teaching machine re-encodes PNGs. Verified
> on `s11_sweep.png`: 104,847 bytes on one side, 110,617 on the other, byte
> hashes unrelated, **decoded pixels identical to the bit**. A byte comparison
> therefore fired on all eighteen week-6 figures after every transfer, which is
> exactly the cry-wolf failure `tools/manifest.py`'s own docstring says it
> exists to avoid. `manifest.image_digest()` hashes the decoded pixels plus the
> size and mode — the same move `content_digest` already made for zips — so a
> re-encode passes and a resize or a colour-space change still fails.

### F3 · Decks — both sessions

```bash
python tools/build_decks.py --pdf sNN sMM
```

**Expect** per deck: a slide count, "all paper figures embedded", and a pacing
line. **Read the pacing line.** It is the only automated statement about whether
a session is teachable:

- `min/slide` for exposition — over ~6 means you will be improvising.
- `% students working` — the course's own sessions run 28–46%. Below 25% means
  the derivations have eaten the class.
- `min/step` on a derivation run, capped at 3.0.
- Any `!!` under-slided segment, and any student block over 10 minutes.

Also fix, not ignore: `no glyph` (a character Calibri lacks — see the denylist
in `theme.py`), `shown as slots` (a paper figure missing from
`private/paper-figures/`), `loose slot` (an image filling under 75% of the space
reserved for it — size the slot from the image's aspect ratio).

**And the fit report, which is the one that decides whether the deck is
readable.** `tools/slide_fit.py` runs inside the deck build and prints three
kinds of finding:

- `text box(es) overflow` — should be impossible now; `Deck.text()` grows a box
  to its contents. If you see one, something bypassed `text()`.
- `overlapping text pair(s)` — two boxes whose ink lands in the same place. This
  is what a reader sees first and what no other gate has ever caught. **Fix
  every one before Saturday.** The usual cause is a hand-written row pitch; the
  fix is `Deck.rows()`, which pitches itself. See AGENTS.md.
- `shape(s) run off the slide` — a box grew past an edge. Cut the text.

`row stack needs X in a Y band` during the build tells you the shortfall and
roughly how many characters to cut, per slide, before you go looking at a PDF.
The count is part of `--check`. Sessions 1–9 predate the gate and are named in
`GRANDFATHERED` in `build_decks.py`: reported, not counted. Nothing else is
exempt, including a deck you have already taught.

### F4 · Handouts, answer sheets, board notes — both sessions

```bash
python tools/build_handouts.py sNN
python tools/build_handouts.py sMM
```

One command per session produces the handout PDF, the answer-sheet PDF and the
board-notes PDF. Needs playwright, which is instructor-machine only.

Every session with a handout needs a **matching answer sheet** — students get
nothing back otherwise — and every session needs **board notes**, even a short
card, because the deck records what is *projected* and nothing else records what
is *written*.

### F4.5 · Adversarial review — both sessions, before Saturday

**New, 26 September 2026.** Saturday's paper read is one reader, and that
reader designed the session. It catches what paper catches: a figure that dies
at the back of the room, a derivation that is clear step by step and pointless
overall, a handout with nowhere to write. It does not catch a wrong
multiple-choice key, a number quoted from the wrong row of a table, or a claim
about a paper the paper does not make, because those need recomputation and
cross-document comparison rather than reading.

The first time this step was run it returned, on materials that had already
passed every mechanical check: a committed figure that printed three answers
three surfaces before they were defined, and that `--verify` called clean; an
answer sheet whose headline claim was refuted by a circuit the students
classify twenty minutes earlier; a technique on the goals slide, graded on the
problem set, and demonstrated nowhere; a ConcepTest distractor whose stated
rationale was false; an FFL type misidentified against the paper's own prose;
a "find the optimum" question whose optimum is always the left endpoint; and
$Y_{\max}$ defined one way in three documents and another way in two.

Run one agent **per session**, and give each of them:

- `decks/sNN_*.py`, `figures/sNN_*.py`
- `handouts/sNN-*.md` and its answer sheet
- `board-notes/sNN-board-notes.md`
- `sessions/sNN-*/README.md`
- `private/sources/psPP.py`
- `docs/coverage-matrix.md` — the rows this session claims
- `posb/` — the library the figures and the set both call
- the assigned papers, as **PDFs**, in `private/readings/`

Tell it to find defects, not to summarize, and to rank by severity. Name the
classes explicitly, because a general request gets a general answer:

1. **Numerical claims.** Every number on a slide, in a handout, in an answer
   sheet or in a speaker note is checkable. Recompute them from `posb` and
   report disagreements with the computation.
2. **Paper claims.** Quote the PDF and give the page.
3. **Cross-document drift** between deck, handout, answer sheet, board notes,
   plan, coverage matrix and problem set. They are written at different times.
4. **Multiple-choice keys** — more than one correct option, a wrong key, or a
   distractor whose stated rationale is false.
5. **Assessed but never demonstrated.** A speaker note is not a demonstration.
6. **A figure that gives away a later answer**, or that annotates a quantity
   the class has not yet defined.
7. **Questions with no real answer** — an optimum that is always an endpoint, a
   convergence that is not monotone, a bracket that need not bracket.
8. **Legibility** — type below the 14 pt floor, overlapping boxes, aspect-ratio
   mismatches.
9. **Tutorial gaps.** The room spans biology, engineering, chemistry, chemical
   engineering and physics. A result asserted rather than derived, algebra done
   off-screen, notation never defined, or an unlabelled axis is a defect here
   even though it is correct.

**Re-verify every finding before acting on it.** The reports are lead lists,
not patches. Of the two run on 26 September, one put a crossing at 0.72 that is
0.655 and claimed a tolerance inconsistency that does not exist. Recompute
before you change anything, and record in the log where the agent was wrong.

Then triage in two piles. **Mechanical defects** — a wrong number, a
misidentified type, an overlapping box, a spelling — get fixed on the spot.
**Anything that changes what is taught, what is assessed, or student workload**
goes to the instructor as a decision with the evidence and a recommendation,
and waits. The C1-versus-C4 answer to session 10's item 4 was that kind of
finding and it was right to hold it.

Rebuild after fixing, then run F6 again. **Saturday should read a corrected
artifact**, which is the whole point of putting this before it rather than
after.

### F5 · Problem set — release weeks only

```bash
python tools/build_problem_sets.py psPP
python tools/build_canvas_description.py psPP
```

`build_problem_sets` runs the tests against the solutions as it goes; a failure
here is a wrong expected value, not a flaky test. It writes the student
notebook, the autograder zip, and `psPP-SOLUTIONS.html` for the reader.

> ### The `posb/` freeze starts now
> The autograder zip carries its own copy of `posb/`. Once Sunday's Docker image
> is built, the autograder runs against **that snapshot** while the student's
> notebook imports the current one from `main`. Edit `posb/data.py` after the
> build and the data a student fits is not the data the hidden test checks.
> `preflight.py` compares them and fails. **Treat `posb/` as frozen from here
> until the set's deadline passes.**

### F6 · Preflight both sessions

```bash
python tools/preflight.py NN
python tools/preflight.py MM --ps PP
```

**Both must exit 0** before you go further. WARNs are judgement calls — a
session with no handout, a `private/taught/` copy that does not exist yet
because you have not reviewed it. FAILs are not.

### F7 · Push, public first

**Public before anything is pasted into bCourses.** A DataHub link posted before
the notebook is on `main` pulls successfully and then says *"Could not find
path"*, which a student reads as a broken assignment.

```bash
git add decks/ figures/ handouts/ board-notes/ sessions/ docs/ tools/ \
        posb/ problem-sets/ readings.yaml
git commit -m "Week of <date>: sessions NN and MM; PSPP"
git push

python tools/check_links.py      # every committed notebook resolves on main
```

Never `git add -A`. Add explicit paths.

Then the private repo, which holds the only copy of every solution:

```bash
cd private
git add sources/ paper-figures/ reader-briefs/
git commit -m "PSPP master and reader brief"
git push
cd ..
```

### Friday gate

Both preflights exit 0; `--deep` is clean; **F4.5 has been run on both sessions
and its mechanical findings are fixed**; `check_links` is all PASS; both repos
pushed. If any of those is false, Friday is not finished.

Findings held for the instructor do not block the gate — they go to him with
the Saturday print, so he decides on paper alongside everything else.

---

# SATURDAY — review, on paper

The only step here that matters is the one that cannot be automated.

### S1 · Print

- both decks, two-up
- both handouts, exactly as students will receive them
- both answer sheets
- both sets of board notes

### S2 · Read them somewhere that is not your desk

What only shows up on paper: a figure legible on a 27-inch monitor and not from
the back of a room; a derivation whose steps are individually clear and
collectively pointless; a handout with no room to write in; an answer sheet that
answers a different question than the one asked.

### S3 · Approve, then copy

```bash
cp private/build/decks/PoSB_SessionNN_*.pptx private/taught/
cp private/build/decks/PoSB_SessionNN_*.pdf  private/taught/
```

> ### Never `cp` over `private/taught/` a second time
> Every deck in there has been opened and saved by PowerPoint — `docProps` says
> `Application="Microsoft Macintosh PowerPoint"` — so it matches the build on
> neither bytes, nor zip members, nor mtime, and it may carry hand edits that
> exist nowhere else. `preflight.py` compares the two on **slide text and
> embedded figures**, which is what a round-trip preserves.

### S4 · If preflight says the taught copy differs

It is telling you that you edited the deck in PowerPoint. Find what changed:

```bash
python - <<'PY'
import re, zipfile, difflib
def slides(p):
    z = zipfile.ZipFile(p)
    n = sorted((x for x in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", x)),
               key=lambda x: int(re.search(r"(\d+)", x.split("/")[-1]).group(1)))
    return [re.sub(r"\s+", " ", " ".join(
        re.findall(r"<a:t>(.*?)</a:t>", z.read(x).decode(), re.S))).strip() for x in n]
a = slides("private/build/decks/PoSB_SessionNN_....pptx")
b = slides("private/taught/PoSB_SessionNN_....pptx")
for i, (x, y) in enumerate(zip(a, b), 1):
    if x != y:
        print(f"--- slide {i}")
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
                None, x.split(), y.split(), autojunk=False).get_opcodes():
            if tag == "equal": continue
            print(f"  BUILD : {' '.join(x.split()[i1:i2])[:200]!r}")
            print(f"  TAUGHT: {' '.join(y.split()[j1:j2])[:200]!r}")
PY
```

Port the edit into `decks/sNN_*.py`, rebuild, then copy again. An edit left only
in the pptx is destroyed by the next build and nothing reports it.

### S5 · Rebuild and re-check

```bash
python tools/build_decks.py --pdf sNN sMM
python tools/preflight.py NN
python tools/preflight.py MM --ps PP
```

### S6 · Stage the print copies

```bash
cp handouts/sNN-<name>.pdf ../2026/handouts-to-print/sNN-<name>-PRINT-THIS.pdf
cp handouts/sMM-<name>.pdf ../2026/handouts-to-print/sMM-<name>-PRINT-THIS.pdf
```

`preflight` compares each print copy against the handout it came from. It has
caught a copy a week stale.

### S7 · Commit the approved decks and any ported edits

```bash
git add decks/                      # only if S4 ported something
git commit -m "Session NN: <what the edit was>" && git push

cd private
git add taught/PoSB_SessionNN_*.pptx taught/PoSB_SessionMM_*.pptx
git commit -m "Sessions NN and MM as taught"
git push
cd ..
```

`taught/*.pdf` is gitignored — it is a render of the pptx beside it.

### Saturday gate

Both decks in `private/taught/`, both preflights exit 0, print copies staged.

---

# SUNDAY — publish

Everything here is a browser and none of it can be scripted. Do it in this
order; each step depends on the one above.

## Gradescope — release weeks only · `gradescope.com/courses/1347910/assignments`

### G1 · Create the 147 assignment

**Create Assignment → Programming Assignment.** Not Homework — that type refuses
`.ipynb`.

| field | value |
|---|---|
| Name | `PSPP — <full title> (BioE147)` — must match what Canvas will link by |
| **Autograder Points** | the number `preflight` printed. Only on the creation form; afterwards it is outline question 1 |
| Manual grading | **on** |
| Release Date | the Thursday, **12:00 AM** — not the form's default of *now*, or an 8:10am class cannot open it |
| Due Date | +7 days, 11:59 PM |
| Create your Rubric | **Before student submission** |

Save, then on **Settings**:

| field | value |
|---|---|
| Grade by course section | **on** |
| Allow late submissions | **on** → +1 day, 11:59 PM |
| Group submission | off |
| Submission Methods | **Upload** only — untick GitHub and Bitbucket |
| Container Specifications | **2.0 CPU / 3.0 GB** — the default cannot solve the conda env |
| Autograder Timeout | **20 minutes** — 10 fails a slow student as `autograder_error` |

### G2 · Outline

**Edit Outline.** Question 1 is `Autograder` at the autograded total; then one
row per manually graded question. The header total must equal the 147 total.

**Build the rows with `+ New Question` in this editor and nowhere else.** The
button creates a `FreeResponseQuestion`, which is what every working problem set
uses. A row created any other way can come out a **`QuestionGroup`** — a
container that sums children and has no rubric of its own, so G4 below fails
with a 500 and a modal that says only *"Unexpected Error"*. The type is invisible
in the UI. To see it, on any outline or rubric page:

```js
JSON.parse(document.querySelector('[data-react-props]')
  .getAttribute('data-react-props')).outline.map(q => q.type + ' ' + q.title)
```

All four PS5 rows were `QuestionGroup` on 26 September and the extra credit could
not be configured at all until they were rebuilt.

> **The `Autograder` row exists only because of the creation form.** It is made
> once, from **Autograder Points** in G1. Re-uploading the zip does not recreate
> it; neither does a submission — the submission's own results page then 500s.
> Lose it and the assignment must be rebuilt from scratch. Deleting *other* rows
> in this editor is safe and leaves it alone.

### G3 · Autograder — start the build

**Configure Autograder** → leave **Zip file upload** selected → upload from
`private/build/psPP/dist/autograder/` → set **Base Image** (Ubuntu 22.04 Base;
it greys out after the first successful build) → **Update Autograder**.

Watch **Docker Image Status** for *built as of …*. 10–25 minutes.

### G4 · The extra-credit question, while it builds

**Create Rubric** → the extra-credit question → **Rubric Settings**:

- 147: **Positive scoring**, **ceiling OFF**. It reads *"maximum score is 0.0"* —
  tick it and the extra credit is silently clamped to zero.
- Items are optional. A brief for the reader is a legitimate substitute and is
  usually the better use of the evening.

### G5 · Test

Submit **`private/build/psPP/psPP-solved.ipynb`**. It must score the full
autograded total. **Then delete the submission**, or it pollutes the queue and
the statistics. *Student Name* is optional — leave it blank and the submission
belongs to nobody.

> **Not `psPP.ipynb`.** That is the master: it has the answers but no
> `metadata.otter`, so otter rejects it before running a single test —
> *"Received submission for assignment 'None' (this is assignment 'psPP')"* —
> which reads like a broken autograder and is not one. The student notebook has
> the identity and no answers. `psPP-solved.ipynb` is built for exactly this by
> `build_problem_sets.write_solved()` and `preflight` asserts it is current.

### G5b · Diff the structure against the set that worked

Before trusting any of the above, put the new assignment beside the previous
release and compare field by field. The previous working instance is the
specification; *"it looks right"* is not a check.

```js
// paste on any Gradescope page, with the two assignment ids
for (const [lbl, aid] of [['new', NEW_ID], ['prev', PREV_ID]]) {
  const h = await (await fetch(`/courses/1347910/assignments/${aid}/rubric/edit`,
                               {cache:'no-store'})).text();
  const p = JSON.parse(new DOMParser().parseFromString(h,'text/html')
              .querySelector('[data-react-props]').getAttribute('data-react-props'));
  console.log(lbl, p.questions.map(q =>
    `${q.title} w=${q.weight} ${q.scoring_type} ceil=${q.ceiling}`));
}
```

Expect the extra-credit row to read `w=0.0 positive ceil=false` on 147. Anything
else and G4 did not take.

**Verify from a fresh page load, never from a response code.** A 200 that
changes nothing is routine here: the server accepts and ignores fields it does
not permit, and the rubric modal reports success on saves that never left the
browser.

### G6 · Duplicate for 247

**Duplicate Assignment** is at the **foot** of the assignments page, beside
*Create Assignment* — not in the `⋮` menu. Rename to `(BioE247)`. Change the
extra-credit question to its point value and set its scoring to match the other
questions on that assignment. It starts its own Docker build. Test and delete
again.

> **The invariant:** both Configure Autograder pages must show the **same zip
> filename**. Nothing compares them. If you ever replace one, replace both in
> the same sitting.

> **Never send a write to Gradescope to find out how its API works.** On 26
> September one "no-op" `PATCH` — the current outline posted back unchanged,
> purely to learn the route — returned **200** and silently deleted every
> question on a live assignment, `Autograder` row included, which then had to be
> rebuilt from nothing. Use the UI, or a payload you have watched the page
> itself send. And capture the current state before any change you cannot
> trivially undo.

> **A stalled Docker build is not a bad zip.** One cold build sat frozen at an
> identical log length for 45 minutes and then finished in minutes once
> restarted from the Gradescope page. Give it 25 minutes, then restart it before
> suspecting the autograder.

## bCourses · `bcourses.berkeley.edu/courses/1557313`

### B1 · Two assignments

`/assignments` → **+ Assignment** → **the full edit page**. The inline `+` form
and `⋮ → Edit` cannot set a submission type and will silently leave it as a text
box.

| field | value |
|---|---|
| Name | identical to the Gradescope assignment |
| Description | bespoke prose — **not** the README. See `2026/bcourses/psPP-assignment-description.md` |
| Points | the section total |
| Submission Type | **External Tool → Find → Gradescope → *an existing Gradescope assignment* → pick → Link Assignment**. Typing the tool URL links the *tool*, not the assignment |
| Load This Tool In A New Tab | **checked** |
| Assign To | that number's **LEC + DIS**, *Everyone* removed. Must match the previous problem set |
| Due | the following Thursday 11:59 PM |
| Available from | blank |
| Until | +1 day, 11:59 PM — this is where the late deadline lives on the Canvas side |

**The description carries the DataHub and Colab links as links on bold text.**
Build them with the link button; do not type a query string into the editor. A
description without them leaves a student with somewhere to submit and no way to
get the thing they are submitting. That has happened.

### B2 · Verify the link — the counter-intuitive one

Do **not** expect Gradescope's settings page to show *BCourses Assignment Name*
yet. Gradescope only learns about the binding when the tool is first **launched**,
so a correctly linked assignment looks unlinked until someone clicks through.
The authoritative check is Canvas's own record:

```
bcourses.berkeley.edu/api/v1/courses/1557313/assignments?per_page=20
```

Each assignment's `external_tool_tag_attributes.custom_params` must carry
`custom_gradescope_resource_id: assignment-<the Gradescope id>`, and the two must
not be crossed.

### B3 · The module

`/modules` → **+ Module** → `Week N · <dates> — <the two session titles>`.
Create it before it is needed, not when the first file wants a home.

Add, in order:

1. the reading for the *following* week — **External URL**, ✅ *Load in a new
   tab*, named `Read before Session X — <author>, "<title>"`
2. both problem-set assignments — type **Assignment**
3. **both deck PDFs**, from `private/taught/` — never from
   `private/build/decks/`, which is not the file you will teach from
4. **both handout PDFs**

**What goes up now and what waits.** Adam's rule, 26 September 2026: *slides,
handouts and problem sets go up early; answer sheets go up after each class.*
Students prepare against the deck and the handout, so withholding them buys
nothing and costs the students who read ahead. An answer sheet released before
the room has worked the handout destroys the exercise, so it is the one item
that waits.

> **Upload the taught copy, not the build.** S3 copies the approved deck into
> `private/taught/`, and that is the file that gets hand-edited in PowerPoint.
> A module built from `private/build/decks/` is correct on Sunday and wrong the
> moment you fix a typo at the lectern, with nothing to say so. This was done
> the wrong way round in week 6.

**Re-check every module file by HASH, not by size.** A file that changed after
it was uploaded is the normal case here — decks get re-cut, handouts get
rebuilt — and the module gives no sign of it. On 26 September six of the eight
week 6 files were stale; five were caught by size, and `s11-oscillators.pdf`
was **the same 166,113 bytes with different content** and was missed until it
was hashed. Paste this on any bCourses page and compare against
`sha256sum` in the repo:

```js
const r = await fetch('/api/v1/courses/1557313/modules/<MODULE_ID>/items?per_page=50',
                      {credentials:'include', headers:{'Accept':'application/json'}});
for (const i of JSON.parse((await r.text()).replace(/^while\(1\);/,''))
                   .filter(x => x.type === 'File')) {
  const j = JSON.parse((await (await fetch(
    `/api/v1/courses/1557313/files/${i.content_id}`,
    {credentials:'include', headers:{'Accept':'application/json'}})).text())
    .replace(/^while\(1\);/,''));
  const b = await (await fetch(j.url)).arrayBuffer();
  console.log([...new Uint8Array(await crypto.subtle.digest('SHA-256', b))]
    .map(x => x.toString(16).padStart(2,'0')).join('').slice(0,16), j.display_name);
}
```

Uploading with `on_duplicate:'overwrite'` mints a **new file id**, and Canvas
repoints the module items to it by itself — so the items do not need editing,
but they do need re-reading to confirm it happened.

**Publish the items, then publish the module.** Two separate states; published
items inside an unpublished module are invisible with no warning.

## Sunday evening — announcement and reader

### A1 · The announcement

Draft lives in `private/announcements/YYYY-MM-DD-weekN.md`, with everything below
the `**Subject:**` line being the posted text and everything above it being the
record. A weekly one covers, in this order: **both** sessions of the coming week
with room and time; the deadline closest; the set that opens; the reading for the
week after; and one thing further out so nobody is surprised.

**Post it from the file, not by retyping it.** Generate HTML from the markdown
below the Subject line, base64 it, and POST from a logged-in bCourses tab:

```js
POST /api/v1/courses/1557313/discussion_topics
{title: <the Subject line>, message: <html>, is_announcement: true, published: true}
```

CSRF from the `_csrf_token` cookie, header `X-CSRF-Token`, as in S-section uploads.
The response's `message` length should equal what was sent.

**Then verify, because "looks right" has been wrong here before.** Re-fetch
`/api/v1/courses/1557313/discussion_topics/<id>` and SHA-256 its `message`
against the locally generated HTML. Comparing lengths alone is what let a stale
file through on 26 September — two files of identical size with different
content. Check `published: true`, `delayed_post_at: null`, and
`is_section_specific: false` unless the post is meant for one cohort. Record the
topic id and the hash in the draft's header, and change its subtitle to
**As posted**.

An off-cycle announcement (a policy or staging change, not a week) gets its own
dated file and the same treatment. Do not fold it into the weekly post if the
weekly post has already gone out — a changed rule buried in a week-six roundup
is a rule nobody read.

### A2 · The reader — release weeks only

Send `private/reader-briefs/psPP.md` and
`private/build/psPP/psPP-SOLUTIONS.html`. Both carry solutions; neither goes
anywhere public. The brief says what each written question tests, what earns the
marks, and the mistake that looks like a right answer.

### Sunday gate

```bash
python tools/preflight.py MM --ps PP        # exits 0
```

Plus, by eye: both Gradescope assignments show *built as of*, both Canvas
assignments carry the right `custom_gradescope_resource_id`, the module is
published, the announcement is posted.

---

# MONDAY TO FRIDAY — teach only

**Nothing is built during the week for the week being taught.** If something
must change in a session about to be taught, it changes on the following Friday
unless it is wrong rather than improvable — you do not rebuild a deck the night
before the room sees it.

That is not a prohibition on working ahead. Building *next* week's sessions
early, from settled designs, is encouraged; see **Earlier is always allowed**
above. The rule protects the taught copy, not the calendar.

### Morning of each class

```bash
python tools/preflight.py NN --ps PP
```

A different question from Friday's. Friday asked *is it right*; this asks *is
the file I am about to open still the one my sources make* — the built deck and
its PDF against the sources, the `private/taught/` copy against that build, the
print copy against its handout.

Then the two things no script can see:

- **Compare the two rosters — and sync only if Gradescope is short.** The
  failure this guards against is one-directional: a student enrolled in
  bCourses and absent from Gradescope **cannot submit** and finds out at 11pm.
  So read both counts first — bCourses **People → active students**, Gradescope
  **Roster**. Sync when Gradescope has **fewer**. When Gradescope has **more**,
  as on 14 September 2026 (31 vs 27 active), do **not** sync: it reconciles
  downward against people who may already hold submissions. Sync is manual and
  does not follow add/drop in either direction.
- **Student View**, from the course home page.

Close PowerPoint before you leave — it holds a `~$` lock file, and a deck open on
your laptop argues with you at the lectern.

### After each class

Into that week's module: the **answer sheet**, which is the one item that waits
until the room has done the handout. The deck and the handout went up on Sunday
(B3). Attachments have no name field in the Add Item dialog and take the raw
filename — `⋮ → Edit` to name it. Publish it.

**If you hand-edited the deck in PowerPoint**, port the edit into
`decks/sNN_*.py` (S4), rebuild, re-copy to `private/taught/`, and **replace the
deck PDF in the module**. The copy students have is otherwise the one from
before the edit.

---

## What this replaces

The old rhythm was: write the session in the two days before it, release the set
on the morning it went out, and meet the manual half at 7am. Every session
shipped. Every defect was also found under time pressure, and the ones that were
not found are the ones that reached students.

The gap between Friday's build and Sunday's publish is not slack. It is where
the review happens, and the review is the only step here that cannot be
automated, hurried, or checked by a script.
