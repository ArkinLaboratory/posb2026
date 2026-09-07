# The weekly ritual

[← back to README](../README.md) · Companions:
[session-release-checklist](session-release-checklist.md) (the per-session
mechanics) · [course-site-runbook](course-site-runbook.md) (*why* bCourses and
Gradescope are shaped this way)

This document is the **calendar**. It says what happens on which day and why
that day. The checklist says what to do inside each step; the runbook says why
each click is the way it is. If you are looking for a command, you are in the
wrong file.

---

## Why this exists

The release checklist is *session*-shaped, and it gets run twice a week. That
was fine until the week the two sessions, a problem set, an autograder, two
Gradescope assignments, two Canvas assignments and a reader brief all landed
inside forty-eight hours. Everything got done, and everything got done **on the
day it was needed**, which is the state in which mistakes are cheapest to make
and most expensive to find:

- A deck was approved and copied to `private/taught/` at 16:43; the full rebuild
  at 18:33 gave it the board-cue icon it had been missing. Nobody would have
  noticed on the projector.
- Two Gradescope Docker images were built sixteen minutes apart from the same
  zip, and nothing in either system compares them.
- A problem set's Canvas description was written from a template that turned out
  not to match the one actually in use.
- The session-5 handout, answer sheet and board notes did not exist at 7pm on
  the Monday before the Thursday they were needed.

None of those was a competence failure. They were a **scheduling** failure: the
work was serialised against the deadline instead of against itself.

**The rule this document exists to state:**

> **Build the whole week on Friday. Review it over the weekend. Post it Monday.
> Teach from something you last touched three days ago.**

Everything below follows from that.

---

## The shape of a week

Sessions are Tuesday and Thursday. A problem set is released on one of them and
is due seven days later. So the unit of work is **the week, not the session**,
and the week starts on the Friday *before* it.

| day | what happens | why then |
|---|---|---|
| **Friday** | build everything for next week | the far side of the weekend from the deadline |
| **Sat / Sun** | review, on paper, away from the machine | you cannot review what you just wrote |
| **Monday** | post; the browser half | one day of slack before Tuesday |
| **Tuesday** | teach; upload after class | |
| **Wednesday** | announcement; reader brief if a set is out | |
| **Thursday** | teach; upload after class | |

---

## Friday — build both sessions and the problem set

Nothing here touches a browser. All of it is repeatable, and all of it can be
redone on Saturday if the review says so.

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026

python tools/build_figures.py sNN sMM        # both sessions
python tools/build_decks.py --pdf sNN sMM
python tools/build_handouts.py sNN           # handout + answers + board notes
python tools/build_handouts.py sMM
python tools/build_problem_sets.py psNN      # only in a release week
python tools/build_canvas_description.py psNN
python tools/preflight.py NN
python tools/preflight.py MM --ps NN
```

**Both sessions, not one.** The Thursday session is written on Friday alongside
the Tuesday one, because the two share figures, notation and a reading, and the
inconsistencies between them are visible only when they are built together.

**The problem set is built Friday even though it is released the following
Thursday.** The Gradescope Docker build takes 10–25 minutes and the duplicate
for the second section takes another. Building on Friday means the image is warm
and tested before anyone needs it, and it means a defect found in the notebook
costs a rebuild rather than a crisis.

> **The freeze that starts here.** The autograder zip carries its own copy of
> `posb/`. Once the image is built, editing anything under `posb/` means the
> autograder and the student's notebook are running different code.
> `preflight.py` compares them; the fix is a rebuild and a re-upload of *both*
> section assignments. Treat `posb/` as frozen from Friday's build until the
> set's deadline passes.

## Saturday or Sunday — review, on paper

Print the two decks two-up, the handouts as students will get them, and the
board notes. Read them somewhere that is not your desk.

What only shows up on paper: a figure that is legible on a 27-inch monitor and
not from the back of a room; a derivation whose steps are individually clear and
collectively pointless; a handout with no room to write in.

**Approve explicitly.** Nothing after this point is worth doing to a deck you
have not decided is finished.

```bash
cp private/build/decks/PoSB_SessionNN_*.pptx private/taught/
cp private/build/decks/PoSB_SessionNN_*.pdf  private/taught/
```

> **`private/taught/` is a PowerPoint round-trip, and never `cp` over it a
> second time.** Every deck in there has been opened and saved by PowerPoint —
> `docProps` says so — so it matches the build on neither bytes nor zip members
> nor mtime, and it may carry hand edits that exist nowhere else.
> `preflight.py` compares the two on **slide text and embedded figures**, the
> things a round-trip preserves. If it reports a difference, diff it, port
> whatever you want to keep back into `decks/sNN_*.py`, rebuild, and only then
> copy again.

## Monday — post, and do the browser half

`preflight.py` must exit 0 first. Then commit and push **public before private**,
and public **before** anything is pasted into bCourses — a DataHub link posted
before the notebook is on `main` pulls successfully and then says *"Could not
find path"*, which reads to a student as a broken assignment.

Then the manual half, in this order, because each step depends on the one above
it:

1. **Gradescope**, both sections — [checklist Phase 4](session-release-checklist.md).
   The autograder points come from `preflight.py`, not from arithmetic. Test
   with the solution notebook, confirm the autograded total, delete the test
   submission.
2. **bCourses assignments**, both sections — link each to *its own* Gradescope
   assignment through **Find**, never by typing the tool URL.
3. **The module.** Create it before it is needed, not when the first file wants
   a home. Reading as External URL, both assignments, then publish the items and
   then the module.
4. **The first launch.** Click through to Gradescope from the Canvas assignment
   once. Until something launches, Gradescope does not know it is linked and its
   settings page still shows an editable *Title* — which looks exactly like a
   broken link and is not one. The test submission does this for you.

**Print on Monday**, not Thursday morning:

```bash
cp handouts/sNN-<name>.pdf ../2026/handouts-to-print/sNN-<name>-PRINT-THIS.pdf
```

## Tuesday and Thursday — teach

Morning of:

```bash
python tools/preflight.py NN --ps MM
```

This run asks a different question from Friday's. Friday asked *is it right*;
this asks *is the file I am about to open still the one my sources make*. Then
the two things no script can see: **Gradescope → Roster → Sync bCourses Roster**,
and **Student View**.

Close PowerPoint before you leave. It leaves a `~$` lock file, and a deck that
is open on your laptop is a deck that argues with you at the lectern.

After class, into that week's module: the deck PDF, and the **answer sheet**,
which is the one thing that must wait until after the room has done the handout.

## Wednesday — the announcement, and the reader

Post the announcement Wednesday evening: after Tuesday's class, so it can refer
to what happened, and before Thursday's, so it can prepare for it. It covers the
deadline that is closest, the set that opens next, the reading for the following
week, and one thing further out so nobody is surprised.

In a release week, this is also when the reader gets the brief and the worked
solutions — `private/reader-briefs/psNN.md` and
`private/build/psNN/psNN-SOLUTIONS.html`. Both carry solutions. Neither goes
anywhere public.

---

## What this replaces

The old rhythm was: write the session in the two days before it, release the
problem set on the morning it is due out, and discover the manual half at 7am.
That worked, in the sense that every session shipped. It also meant every defect
was found under time pressure, and the ones that were not found are the ones
that reached students.

The three days between Friday's build and Monday's post are not slack. They are
where the review happens, and the review is the only step in this document that
cannot be automated, hurried, or checked by a script.
