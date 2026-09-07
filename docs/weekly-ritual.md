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
| **Friday** | build both sessions + the problem set | `preflight` exits 0 for both |
| **Saturday** | review on paper; approve; port back; rebuild | decks copied to `private/taught/` |
| **Sunday** | Gradescope, bCourses, modules, announcement, reader | final `preflight` exits 0 |
| **Mon–Fri** | teach; upload after class | nothing is built |

`NN` = Tuesday's session, `MM` = Thursday's, `psPP` = the set released that week.

---

# FRIDAY — build

Nothing here touches a browser. All of it is repeatable.

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

Both preflights exit 0; `check_links` is all PASS; both repos pushed. If any of
those is false, Friday is not finished.

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

Submit `private/build/psPP/psPP.ipynb` — the **solution** notebook. It must
score the full autograded total. **Then delete the submission**, or it pollutes
the queue and the statistics.

### G6 · Duplicate for 247

**Duplicate Assignment** is at the **foot** of the assignments page, beside
*Create Assignment* — not in the `⋮` menu. Rename to `(BioE247)`. Change the
extra-credit question to its point value and set its scoring to match the other
questions on that assignment. It starts its own Docker build. Test and delete
again.

> **The invariant:** both Configure Autograder pages must show the **same zip
> filename**. Nothing compares them. If you ever replace one, replace both in
> the same sitting.

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

Slides and answer sheets are added after each class, not now.

**Publish the items, then publish the module.** Two separate states; published
items inside an unpublished module are invisible with no warning.

## Sunday evening — announcement and reader

### A1 · The announcement

`/discussion_topics/new?is_announcement=true`. Draft lives in
`2026/announcements/`. It covers, in this order: **both** sessions of the coming
week with room and time; the deadline closest; the set that opens; the reading
for the week after; and one thing further out so nobody is surprised.

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

**Nothing is built during the week.** If something must change, it changes on
the following Friday unless it is wrong rather than improvable.

### Morning of each class

```bash
python tools/preflight.py NN --ps PP
```

A different question from Friday's. Friday asked *is it right*; this asks *is
the file I am about to open still the one my sources make* — the built deck and
its PDF against the sources, the `private/taught/` copy against that build, the
print copy against its handout.

Then the two things no script can see:

- **Gradescope → Roster → Sync bCourses Roster.** Not automatic. A student
  enrolled in bCourses and absent here **cannot submit** and finds out at 11pm.
  One sync took the roster from 25 to 31.
- **Student View**, from the course home page.

Close PowerPoint before you leave — it holds a `~$` lock file, and a deck open on
your laptop argues with you at the lectern.

### After each class

Into that week's module: the **deck PDF** from `private/build/decks/`, and the
**answer sheet**, which is the one item that must wait until the room has done
the handout. Attachments have no name field in the Add Item dialog and take the
raw filename — `⋮ → Edit` each to name it. Publish both.

---

## What this replaces

The old rhythm was: write the session in the two days before it, release the set
on the morning it went out, and meet the manual half at 7am. Every session
shipped. Every defect was also found under time pressure, and the ones that were
not found are the ones that reached students.

The gap between Friday's build and Sunday's publish is not slack. It is where
the review happens, and the review is the only step here that cannot be
automated, hurried, or checked by a script.
