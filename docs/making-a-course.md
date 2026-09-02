# How to make a course

[← back to README](../README.md)

Written for two readers: **you next August**, standing up this course again, and
**a colleague** standing up a different one on the same machinery. It is the
spine — the whole thing in order, with the decisions called out where they are
actually made. Depth lives in the reference pages it links to; nothing here is
repeated there, and nothing there is repeated here.

Everything in it was learned by doing it wrong first. Where a rule looks
fussy, it is because something broke.

---

## 1. Four decisions, made before anything is built

These constrain everything downstream. Making them late is what costs weeks.

### 1.1 Is there a graduate section, and what does it actually do?

A cross-listed 147/247 site is one Canvas course, one Gradescope course, and
**two populations with different work and different denominators.** That single
fact ramifies further than anything else on this page.

Decide, in this order:

1. **Does the graduate section do extra work?** If no, stop; everything below is
   moot and you have one assignment per problem set.
2. **Is that extra work required, extra credit, or both?** Ours is **required
   for 247 and extra credit for 147**. Those are two different totals — 39 and
   34 — which is what forces two assignments per problem set.
3. **Write the answer into the syllabus before the first problem set.** The
   totals become promises. "39 total" is hard to walk back in November.

The implementation, and why the obvious alternatives fail, is §5.4.

### 1.2 Are notebooks the medium?

If students run code, everything else follows: a hub, a distribution link, an
autograder, a submission format. If they do not, most of §3 and §5 disappears.

Half-measures are the expensive option. A course where *some* work is
notebooks pays the whole setup cost for a fraction of the benefit.

### 1.3 Public repository, or not?

Ours is public (CC BY 4.0) with a **second, private repository mounted inside
it**. That split is not tidiness; it is what makes the public half publishable:

- **public** — notebooks, package, docs, deck *sources*, generated figures,
  handout PDFs, syllabus
- **private** — problem-set masters with solutions, figures scanned from
  papers, supplementary movies, assembled decks, as-taught decks

A deck build embeds a paper figure if it is present and draws a labelled
placeholder if it is not, so the public build never carries copyrighted
material and there is never a public deck and a private deck to keep in sync.

If you will not maintain the discipline, make the whole repository private. A
public repository with solutions in its history cannot be un-published.

### 1.4 Who else edits the material, and how?

The tension: **the material is code** — decks are Python, notebooks are built
from Python, figures are generated — and **instructors want to edit documents.**
Both are legitimate and they collide.

Our resolution, in §2.3. Decide it up front, because the failure mode is an
instructor hand-editing a generated file and losing the work at the next build.

---

## 2. The repository

### 2.1 The shape

```
posb2026/                          <- public, CC BY 4.0
├── decks/          deck sources (Python)
├── figures/        figure generators (Python) + build/ (committed PNGs)
├── posb/           the course package
├── tools/          every build and check script
├── sessions/  problem-sets/  handouts/  board-notes/  docs/
└── private/                       <- a SECOND repo, gitignored by the first
    ├── sources/psNN.py            masters, with solutions
    ├── paper-figures/  paper-movies/
    ├── build/decks/               assembled decks
    └── taught/                    as-taught copies. See §2.3.
```

**Two repositories means two pushes.** Committing in the public repo does not
commit anything under `private/`.

Details, including what belongs where and what belongs in neither:
[where-things-live §3](where-things-live.md).

### 2.2 Authored versus generated

The distinction that prevents most confusion. Some files you write. Others are
**produced by a command** and must never be hand-edited, because the next build
destroys the edit silently.

The full table is in
[where-things-live §2](where-things-live.md#2-authored-versus-generated). The
principle: **if a command can produce it, editing it is a bug.**

Every generated artifact carries a `.deps.json` sidecar recording what it was
built from, with content hashes. `--verify` recomputes them. Content hashes,
not timestamps, because file copies restamp mtimes and on the teaching machine
every source looks newer than the artifact built from it.

### 2.3 The escape hatch, and why it exists

Sometimes the fix happens in the room, or five minutes before it. That copy is
now a **record**, not a build artifact, and it needs to be where no build can
reach it:

```
private/build/decks/PoSB_Session02_Substrate.pptx      generated. Disposable.
private/taught/PoSB_Session02_Substrate_APA.pptx       what was actually shown.
```

The build writes into `build/decks/` unconditionally and never touches
`taught/`. So: **the moment you hand-edit a generated file, save it into
`taught/` under a new name.**

Two consequences worth stating plainly, because this is the point where the
"material is code" discipline meets a human being with a deadline:

- `--verify` does not check `taught/`, deliberately. The file is not what the
  sources produce and is not supposed to be.
- **If an edit matters next year, port it back into the source.** The taught
  copy records what happened in the room; the source is what next year builds
  from. When they disagree, the source is wrong.

This is the honest answer to "can instructors edit documents?" — yes, with a
named place for the result and a rule about what happens to it. It is not
"yes, edit anything", which loses work, and it is not "no", which loses
instructors.

### 2.4 A rule about PDFs, since it cost an afternoon

PowerPoint's own **Export as PDF** produced a PDF with styling and images gone,
from a `.pptx` that was byte-identical to a good one and opened perfectly.
LibreOffice converted the same file correctly. Use
`python tools/build_decks.py --pdf`, or `soffice --headless --convert-to pdf
<file>.pptx` for a deck in `taught/` — and **look at the PDF**. An exporter
failing silently is not something you can reason your way past.

Do not glob. `soffice --convert-to pdf *.pptx` picks up the 165-byte `~$name.pptx`
lock files PowerPoint leaves behind after a crash, reports them as corrupt, and
you conclude your decks are broken. Name the file you mean.

---

## 3. Compute

### 3.1 The hub, and the fallback

**DataHub** is the primary: students click one link, it clones the repository
into their home directory and opens the notebook. Nothing to install, no
accounts to create beyond CalNet.

**Colab is the fallback and it is not optional.** It needs no institutional
anything, which matters for two populations: students on the waitlist who are
not yet enrolled, and everyone on the day the hub is down. Every notebook
carries a Colab badge and a setup cell that clones the repository when it
detects Colab, because Colab opens a notebook *alone*, without the package
beside it.

Memory and version-floor setup: [instructor-setup §2.1–2.2](instructor-setup.md).

### 3.2 The distribution link, and its three traps

Students never clone anything. They click a link that clones for them.

```
https://datahub.berkeley.edu/hub/user-redirect/git-pull
  ?repo=https://github.com/ArkinLaboratory/posb2026
  &branch=main
  &urlpath=lab/tree/posb2026/problem-sets/ps01-modeling/ps01.ipynb
```

Generate them with `python tools/check_links.py`, never by hand and never with
the web generator, and all three of these become impossible:

1. **`urlpath` must include the clone folder** — `lab/tree/posb2026/…`. Get it
   wrong and the pull *succeeds*, then JupyterLab says "Could not find path",
   which students read as *the assignment is missing*.
2. **The Berkeley generator pre-fills `branch=master`** and prefers it to the
   branch it detected. Ours is `main`.
3. **`&backup=true` does nothing.** It is an nbgitpuller 1.3.0 feature and
   DataHub pins 1.2.2, which ignores it silently.

### 3.3 The update path is not the clone path, and it will bite you

nbgitpuller **updates** an existing clone rather than replacing it, and it
preserves files the student has modified. Consequences:

- **A fix you push does not reach a student who already pulled.** If the change
  matters, say so in an announcement and tell them how to force it; if it
  matters a great deal, ship a new folder.
- **You cannot test the clone path from your own account**, because your home
  directory already has the folder. Incognito does not help: same CalNet ID,
  same NFS home. Either `mv ~/posb2026 ~/posb2026-mine` first, or have someone
  else click it.
- **This will bite you before it bites a student.** On 2 September the
  instructor's own tab was showing a version of PS1 from before a fix three days
  earlier, and the review being done from it was a review of nothing.

---

## 4. The course site

bCourses is an **index, not a store**. The only files that live there are the
ones that cannot live anywhere else — lecture PDFs, behind CalNet, which is what
makes ordinary educational use of paper figures fine. Everything a student
*runs* is a link out.

The rule that keeps it usable: **anything a student needs is one click from the
Modules page.** They should never need to know a repository exists.

The structure — a permanent *Start here* module plus one module per week, and
which Canvas item type to use for each kind of thing — is in
**[course-site-runbook](course-site-runbook.md)**, along with every trap: Modules
hidden from student navigation by default, the built-in Syllabus being neither
a Page nor a File, File items named after their filenames, publish state on the
item *and* the module, and Student View being unable to preview an LTI tool.

Two things belong here rather than there, because they are decisions rather
than clicks:

- **A problem set's Canvas description is the problem-set README**, converted,
  not fresh prose. The README already carries the DataHub and Colab links. Write
  the description by hand and you will point at the links instead of carrying
  them — which is exactly what happened to PS1, leaving students a submission
  box and no way to obtain the notebook.
- **Build *Start here* before day one.** In 2026 it went up in week two, so the
  students who most needed it — the ones adding late — had it last.

---

## 5. Grading

### 5.1 Assignment type is forced, and it is not the obvious one

Gradescope's **Homework / Problem Set** type accepts a single PDF or
per-question images. **It will not accept a `.ipynb`.** A notebook course lives
on **Programming Assignments**, whatever the work actually is.

An autograder is not required to use one: leave autograder points at 0, tick
*enable manual grading*, and it is a plain file drop with a gradebook column.
That is the right shape for anything ungraded — an environment check, a survey —
and it costs no Docker build.

### 5.2 Lead time you cannot compress

An assignment that *does* autograde needs its image built on Gradescope's side:
10–25 minutes for an Otter environment, plus a test submission, plus raising the
defaults (§5.3). **Build it days before the assignment posts.**

Test it by uploading the *solved* notebook Otter produces —
`private/build/psNN/dist/autograder/psNN.ipynb` — and confirming it scores full
autograder marks. That single check proves the whole chain: build → zip → image
→ submission → score.

### 5.3 Defaults that are wrong for a computational course

Group submission on, GitHub and Bitbucket submission on, 0.5 CPU / 0.75 GB, a
10-minute timeout, and a point ceiling that silently caps extra credit. All five,
with what to set them to, are in
[course-site-runbook §5.10](course-site-runbook.md).

### 5.4 Two course numbers: two assignments, one per section

From §1.1: different denominators, and one Gradescope assignment has one
outline. So each problem set is **two assignments**, each assigned to one
section's students:

| | assigned to | the extra question |
|---|---|---|
| `PSn (147)` | both 147 sections | **0 points**, positive-scoring rubric worth up to +*e*, **point ceiling off** |
| `PSn (247)` | both 247 sections | **worth *e* points**, total = base + *e* |

Build the second by **duplicating** the first once it is fully configured;
duplication copies the outline, every rubric and the autograder. Each student
submits once and appears in exactly one queue, so you grade N submissions, not
2N. Click-by-click: [course-site-runbook §5.12](course-site-runbook.md).

**The two alternatives both fail, and it is worth knowing why:**

- **One shared assignment plus a small add-on for the graduate section** breaks
  the drop rule. A 247 student would carry eighteen items in the problem-set
  group against a 147 student's nine, so "lowest two dropped" discards two small
  supplements instead of two whole problem sets. Same stated policy, materially
  different relief.
- **One assignment at the higher total, with the extra question auto-credited
  for undergraduates**, inverts the intent: the graduate section must earn
  points the undergraduates are given.

### 5.5 The roster is synced by hand and nothing tells you it is stale

**Gradescope → Roster → Sync.** Not automatic. A student enrolled in the LMS and
absent from the Gradescope roster **cannot submit**, and finds out at 11pm on
the due date.

On 2 September the roster held 25 students. One click took it to 31. Six people
could not have handed in PS1, and nothing anywhere said so.

**Re-sync before every problem set opens**, and do not check by adding up the
Sections page — that counts memberships, not people.

---

## 6. The weekly loop

The canonical version. Other pages describe pieces of it; this is the sequence.

**Before the week**

1. Author or revise the session notebook — edit `tools/sources/sNN.py`, then
   `python tools/build_notebooks.py && python tools/execute_notebooks.py`.
   Never hand-edit a `.ipynb`.
2. Author or revise the deck — edit `decks/sNN_*.py`, then
   `python tools/build_decks.py sNN --pdf`. The build fails on pacing
   violations; that is intentional.
3. `python tools/build_figures.py` if any generator changed.
4. Commit and push **both** repositories.

**The morning of**

5. `python tools/handoff.py --check` — did everything land on this disk?
6. `python tools/build_decks.py --verify` — is the deck you are about to teach
   from the one your sources would produce? `up to date` is the only answer to
   walk into the room on.
7. Print what needs printing: board notes for you, handouts for them.

**After the last class of the week**

8. Convert the deck to PDF and upload it to bCourses Files.
9. Build next week's module: slides as **File** items — then `⋮ → Edit` each to
   give it a real title, because the File dialog has no title box — the reading
   as an **External URL** through the library proxy, the problem set as an
   **Assignment**.
10. The paper discussed in class *N* is assigned at the end of class *N−1*, so
    the reading goes up with the **previous** week's module. `readings.yaml`
    enforces this; `python tools/build_readings.py --check` checks it.
11. Publish the items, then publish the module.
12. **Student View.** Click all of it.
13. Post the announcement: what happened, what to click, what is due.

---

## 7. Verification

Four layers, each catching something the others cannot. All of them build
nothing.

| Command | Question it answers | What it caught |
|---|---|---|
| `handoff.py --check` | Did the files that were handed over actually land on this disk? | Eighteen files written to the wrong directory, every call reporting success |
| `build_decks.py --verify` | Is the artifact on this disk the one these sources would produce? | A deck taught from that was two hours stale, twice |
| `build_figures.py --verify` | Is a committed figure older than the code that generates it? | — |
| `build_readings.py --check` | Is every paper handed out before it is discussed? | — |
| `check_links.py` | Do the distribution links resolve, on the right branch, with the clone folder in the path? | — |
| `check_schedule.py` | Do `course.yaml` and the course map agree? | — |
| `pytest tests/` | Does the package still work? | — |

**And the layer no command reaches.** Canvas Student View cannot preview an LTI
tool — it launches as a Test Student, the tool resolves to your instructor
identity, and you are shown a staff console. So the Gradescope half of a
student's experience can only be checked by **a person with a student account**,
and a TA is not one; a TA sees the staff view too.

Budget for this. The single most valuable ten minutes in the setup is someone
with a student account clicking every link once. In 2026 the two defects that
reached students were both found this way — one by a GSI, one by a student who
sent mail an hour after the assignment posted.

---

## 8. End of term, and next August

**At the end of term**

- Decide, on purpose, whether solutions are published —
  [instructor-setup §6](instructor-setup.md).
- Commit `private/taught/`. Those are the decks you actually gave.
- Write down what broke while you still remember it. Every section of this page
  exists because someone did or did not.

**Next August, in this order**

1. Re-read §1. The four decisions may have changed — enrolment, a co-instructor,
   a new hub version.
2. Turn on Modules in the student navigation **before** building anything.
3. Build *Start here* before day one.
4. Build the autograder images the week before, not the morning of.
5. Sync the roster.
6. Have someone with a student account click every link.

**And the standing hazard:** a policy stated in nine separate files will be
wrong in at least one of them. PS1 shipped in 2026 saying the extra question was
worth "no credit" to undergraduates when it was extra credit, because the
sentence had been typed into a notebook by hand. The fix was not to retype it
correctly — it was `tools/sources/common.py`, which now states the 147/247
policy once and injects it into every problem-set master. Prefer a function to a
convention every time.
