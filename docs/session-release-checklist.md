# Releasing a session

[← back to README](../README.md) · Companions: [weekly-ritual](weekly-ritual.md)
(*which day* each of these steps happens on) ·
[course-site-runbook](course-site-runbook.md) (*why* bCourses is shaped this
way) · [instructor-setup](instructor-setup.md) (accounts, DataHub, Gradescope) ·
[where-things-live](where-things-live.md)

> This document is **session**-shaped: it is everything one session and its
> problem set need. [weekly-ritual.md](weekly-ritual.md) is **week**-shaped and
> says when to run it — the short version being *build Friday, review over the
> weekend, post Monday*. Running this checklist on the morning it is due is the
> failure mode that document exists to prevent.

The ritual, in order, for every teaching day. It has two halves and the split is
deliberate.

| | owned by | how it fails |
|---|---|---|
| **Mechanical** — does it build, is a PDF stale, is the notebook on `main` | **`tools/preflight.py`** | loudly, on demand |
| **Manual** — clicking in Gradescope and bCourses | **this document** | silently, at 11pm on the due date |

> **If you find yourself adding a check to this document that a script could
> make, add it to `preflight.py` instead.** A hand-maintained list of derivable
> facts is wrong within a fortnight and nothing about it looks wrong.

---

## Phase 0 — the gate

Do not start until **the content is reviewed and you have said so.** Every step
below costs a build cycle to undo, and the Gradescope Docker build costs two.

---

## Phase 1 — build everything

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026

python tools/build_figures.py sNN          # needs scipy — your machine, not the bridge
python tools/build_decks.py --pdf sNN      # needs LibreOffice
python tools/build_handouts.py sNN         # needs playwright; builds handout + answers + board notes
python tools/build_problem_sets.py psNN    # needs otter-grader; only on a set's release day
python tools/build_canvas_description.py psNN   # the README as pasteable HTML
```

Then the copy that actually goes to the printer — it lives outside the repo and
is made by hand, so it silently drifts:

```bash
cp posb2026/handouts/sNN-<name>.pdf \
   2026/handouts-to-print/sNN-<name>-PRINT-THIS.pdf
```

## Phase 2 — preflight

```bash
python tools/preflight.py 5 --ps 2
```

Exit 0 means every mechanical precondition holds: the deck builds with no
missing glyphs and no unembedded paper figures, every handout PDF is newer than
its source, the print copy is newer than the handout, the reading for the *next*
session is declared and handed out here, the student notebook contains **no
solutions**, its README carries both the DataHub and Colab links, the autograder
zip exists, and every committed notebook resolves on `main`.

**Do not proceed past a FAIL.** WARNs are judgement calls (a session with no
handout, a handout with no answer sheet yet).

## Phase 3 — commit and push, public first

Push **before** anything is pasted into bCourses. A DataHub link posted before
the notebook is on `main` pulls successfully and then shows *"Could not find
path"*, which reads to a student as a broken assignment.

```bash
git add decks/ figures/ handouts/ board-notes/ sessions/ docs/ tools/ \
        posb/ problem-sets/ readings.yaml AGENTS.md
git commit -m "Session N: ..."
git push

python tools/check_links.py        # must be all PASS now
```

Then the **private** repo, which holds the only copy of every solution:

```bash
cd private
git add sources/ paper-figures/ taught/
git commit -m "PSn master; session N paper figures; taught deck"
git push
```

> `private/` is a single point of failure until this is done. `sources/psNN.py`
> is the only copy of that set's solutions and rubric answers.

---

## Phase 4 — Gradescope

Only on a problem-set release day. **Start this two days early**: the Docker
build is 10–25 minutes and it has to be tested with a real submission.

### 4.1 Create the 147 assignment — `PSn — <Full Title> (BioE147)`

> **Corrected 14 September.** This document used to say the name was
> `PSn (BioE147)`. The convention actually in use on Gradescope is the set's
> full title with the section in parentheses — `PS2 — Expression Dynamics and
> the Cost of Speed (BioE147)`. Match it: the Canvas link dialog lists
> Gradescope assignments **by name alone**, and a set named differently from
> its siblings is the one you mislink at 11pm.

**Programming Assignment.** Not Homework — that type refuses `.ipynb`
([runbook §5.6](course-site-runbook.md)).

| Field | Value | Default is wrong because |
|---|---|---|
| Autograder Points | *the autograded total only* — `preflight.py` prints it | manual points are added by the rubric |
| Manual grading | **enabled** | the written questions |
| Release / Due | the session date / +7 days, 11:59 pm | |
| Group submission | **off** | on by default, with no size limit |
| GitHub / Bitbucket | **off** — upload only | **both are ON by default, and the Create-Assignment wizard never shows them** — they appear only on Settings *after* the assignment exists, so this is a second visit, not a field you can get right the first time |
| Grade by course section | **on** | on by default; leave it — the reader grades one section at a time |
| CPU / RAM | **2.0 / 3.0 GB** | 0.5 / 0.75 GB cannot solve the conda env |
| Timeout | **20 min** | 10 min fails a slow student as `autograder_error` |

Upload the zip from `private/build/psNN/dist/autograder/`. Wait for the build.

**Two things the wizard gets wrong and one it hides.** The create flow collects
only name, autograder points, manual grading, dates and sections. Container
specs (0.5 CPU default), timeout (10 min default) and the submission methods
(GitHub and Bitbucket both **on**) live on **Settings**, which only exists once
the assignment does. So the order is: create → outline → upload zip (starts the
Docker build) → **Settings, fix four things, Save**. The build and the settings
are independent, so fixing settings while the image builds costs nothing.

**Base image** is Ubuntu 22.04 / Base, which is the default and matches every
prior set. Do not change it.

> **Do not edit anything under `posb/` after this upload.** The zip carries its
> own copy of the package, so the built image is frozen against that snapshot
> while the student's notebook imports the current one from `main`. Change
> `posb/data.py` and the data a student fits stops being the data the hidden
> test checks. `preflight.py` compares the two and fails if they have parted;
> the fix is to rebuild the set and re-upload, which costs another Docker build.

### 4.2 Test it before anyone sees it

Submit **`private/build/psNN/dist/autograder/psNN.ipynb`** as a test submission
and confirm it scores full autograder points. Then **delete that submission**,
or it pollutes the queue and the statistics.

> **Corrected 14 September — this step used to name the wrong file.** It said
> `private/build/psNN/psNN.ipynb`. That is the **master** notebook this
> repository writes *before* otter runs, and it carries no
> `metadata.otter.assignment_name`. Submitting it does not fail a test; it
> fails the whole run, with
>
> ```
> OtterRuntimeError: Received submission for assignment 'None'
>                    (this is assignment 'psNN')
> ```
>
> — an *Autograder Error*, 0.0/NN, which looks like a broken image rather than
> a wrong upload. The file you want is the solutions copy **otter itself
> emits**, under `dist/autograder/`: same solutions, plus the metadata the
> grader checks. (`dist/student/psNN.ipynb` also carries the metadata but has
> the solutions stripped, so it scores near zero — right mechanism, wrong
> file.)

### 4.3 The extra-credit question

Every set carries one question that is **required for 247, extra credit for
147**. On the 147 assignment that question is **0 points with rubric items worth
up to +*e*** — and you must **disable the point ceiling on it**. It is on by
default, it caps scores at 0.0, and nobody discovers it by looking; they
discover it when a student asks where their extra credit went.

> **Where the setting lives.** **Create Rubric** (left nav) lists every
> manually graded question with its own **Rubric Settings** link. Open the one
> for the extra-credit question and set:
>
> | | 147 | 247 |
> |---|---|---|
> | Scoring Method | **Positive scoring** (points added to 0) | Negative scoring |
> | Ceiling | **unchecked** | leave checked — *maximum score is e* is correct there |
> | Floor | either; it cannot bind when every item is positive | checked |
> | Rubric item | one, **`Correct +e`** | one, `Correct -0.0` |
>
> **No submission is required.** An earlier version of this note claimed the
> dialog was reachable only from the grading view of a real submission, and that
> the ceiling therefore had to be fixed between the test submission and its
> deletion. That is wrong — it was written from the one route I happened to find
> first. *Create Rubric* works on an assignment with zero submissions, which is
> also why this step can be done the moment the outline is saved, before the
> Docker image has even finished building.
>
> The grading-view route (`Grade Submissions` → the question → *Rubric
> Settings*) does also work, and is the one to use if you are already mid-grade.
> Both edit the same per-question state.

### 4.4 Duplicate for 247

**Duplicate is at the foot of the Assignments page**, beside *Create
Assignment*. It is *not* in the `⋮` menu, which offers only Settings and Delete
— which is why you will conclude the feature does not exist
([runbook §5.12](course-site-runbook.md)).

Name it `PSn (BioE247)` — the same shape as `PSn (BioE147)`, because the
Canvas link dialog lists Gradescope assignments by name alone. Change that one
question to **worth *e* points**, and
assign it to the 247 section. The copy starts **its own** Docker build — another
10–25 minutes, no action needed.

Duplication does **not** carry the LMS link, which is correct: two Gradescope
assignments pointing at one Canvas assignment would fight over grade passback.

> There is **no publish step** in Gradescope. Visibility is the Release Date
> alone. The empty *Published* circle refers to grades and is the correct state
> until you have marked ([runbook §5.11](course-site-runbook.md)).

---

## Phase 5 — bCourses

### 5.1 Lecture slides

**Files → upload the PDF** from `private/build/decks/`. Then **⋮ → Edit** on the
module item and give it a title — the Add Item dialog has no name box for File
items, so it uses the raw filename ([runbook §5.2](course-site-runbook.md)).

Never link to GitHub for a deck: assembled decks are gitignored and may embed
figures from published papers, which is why they live behind CalNet.

### 5.2 The reading

**External URL** to the DOI through the UC Library proxy. Tick **Load in a new
tab**. Do not upload the PDF.

### 5.3 The problem set — two assignments, one per section

Each is an **Assignment → External Tool → Gradescope**, linked to its own
Gradescope assignment, assigned to its own section, with its own point total.

**Use the full Edit page, never quick-edit** — quick-edit silently resets the
submission type to a text box ([runbook §5.12](course-site-runbook.md)).

**The description is the problem set's `README.md`, converted to HTML.** Not
fresh prose. The conversion is done for you —

```bash
open private/build/psNN/canvas-description.html   # or cat it
```

— and it refuses to write a file that lost either link. Select all, then paste
with the **`</>`** button, because the DataHub URL is a query string the
rich-text editor mangles. The embedded Gradescope panel is an upload
box and nothing else — a description without the DataHub and Colab links leaves
a student with somewhere to submit and no way to get the thing they submit.
That happened on PS1 and a student reported it within the hour
([runbook §5.8](course-site-runbook.md)).

Check **Available from** while you are there. PS1 carried a date nobody chose.

### 5.4 Modules

Publish the **items**, then publish the **module**. Both have their own state
and a published set of items inside an unpublished module is invisible to
students with no warning ([runbook §5.3](course-site-runbook.md)).

---

## Phase 6 — the morning of

```bash
python tools/preflight.py N --ps M     # one more time; things drift
```

This run is not the same question as Phase 2's. Phase 2 asked *is it right*;
this one asks *is the file I am about to open still the one my sources make*.
Between the two runs sit a night of edits, and the three things that actually
drift are all hash-checked here: the built `.pptx` and `.pdf` against the deck
source, theme, and every figure they embed; the copy in `private/taught/`
against that build; and the `-PRINT-THIS.pdf` against the handout it came from.
A `FAIL` on any of those means the artifact predates an edit — rebuild and
re-copy, do not present it.

What this run still cannot see is everything on the far side of a browser: the
Gradescope roster, whether the Docker image built, whether the point ceiling
matches the rubric, whether the Canvas module is published. Those are the rest
of this phase, and that is why the split exists.

- **Compare the two rosters — and sync only if Gradescope is short.** Read
  bCourses **People → active students** against the Gradescope **Roster**. The
  failure is one-directional: enrolled in bCourses, absent from Gradescope,
  **cannot submit**, finds out at 11pm. Sync when Gradescope has **fewer**. When
  it has **more** — 31 vs 27 active on 14 September 2026 — do **not** sync; it
  reconciles downward against people who may hold submissions
  ([runbook §5.9](course-site-runbook.md)).
- **Student View**, from the course home page. It does not exercise the
  Gradescope half — have a reader click that once.
- **Check the Late Due Date on the Gradescope receipt.** PS1 came back carrying
  one nobody set, most likely the bCourses *Until* date syncing across. It is a
  policy, not a bug: submissions are accepted and flagged late rather than
  refused.
- **Print**: the handout (one per student), and the board notes (one, for you).
  **Not** the answer sheet.

---

## Phase 7 — after class

1. **Archive the deck you actually taught from** into `private/taught/` under a
   new name. `build_decks.py` overwrites `private/build/decks/` without asking,
   and a taught deck is a record, not a build artifact.
2. **Post the answer sheet** to bCourses. It covers only the items done in the
   room — an item that is also a problem-set question must not have its solution
   in a public repository.
3. **Write down the poll distributions.** They are the only read you get on the
   room between meetings, and they replace anything collected on paper.
4. **Append to `2026/SESSION-LOG.md`**: what changed, why, and where it landed.
   Not what exists — `tools/status.py` derives that. What a directory listing
   cannot tell you.

---

## The whole thing, as commands

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026

python tools/build_figures.py sNN
python tools/build_decks.py --pdf sNN
python tools/build_handouts.py sNN
python tools/build_problem_sets.py psNN
cp handouts/sNN-<name>.pdf ../2026/handouts-to-print/sNN-<name>-PRINT-THIS.pdf

python tools/preflight.py N --ps M          # must exit 0

git add ... && git commit && git push       # public
cd private && git add ... && git commit && git push && cd ..
python tools/check_links.py                 # must be all PASS

#  -> Gradescope  (Phase 4)
#  -> bCourses    (Phase 5)
#  -> morning of  (Phase 6)
```
