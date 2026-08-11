# Instructor Setup

[← back to README](../README.md) · See also [Lecture Design](lecture-design.md) (the per-session template), [For Instructors](for-instructors.md) (adapting the material), [Design Notes](design-notes.md) (why it is built this way)

A runbook. This page is operational — accounts, commands, checklists. It is
written for three people:

- **The instructor**, setting the course up for a new term
- **A GSI or reader**, being onboarded mid-course
- **You, next year**, having forgotten all of this

Berkeley-specific steps are marked **[Berkeley]** and have generic equivalents
noted.

---

## 1. One-time setup

Roughly 30 minutes. Do this once, ever.

### 1.1 Clone and install

```bash
git clone https://github.com/ArkinLaboratory/posb2026.git
cd posb2026
pip install -r requirements.txt
```

**Do not put the working copy inside Dropbox, iCloud Drive, or OneDrive.** Sync
daemons race with `.git` on loose objects and index locks, and the failure mode
is a repository that looks fine until it suddenly is not.

Verify:

```bash
python -m pytest tests/ -q          # expect 13 passed
python tools/build_notebooks.py --check
python tools/execute_notebooks.py
```

All three must pass before you change anything. If they do not, the problem is
your environment, not the material.

### 1.2 The private repository

Problem-set masters contain solutions and **cannot live in the public repo**.
They go in `private/`, which is gitignored here — meaning it is also outside
your git history and not backed up by anything.

Create a second, private repository for them:

```bash
mkdir -p private/sources
cd private
git init
git remote add origin https://github.com/ArkinLaboratory/posb2026-private.git
git add -A && git commit -m "Problem set masters"
git push -u origin main
```

Private repositories are free and unlimited on GitHub. This is where masters,
exams, and anything with answers in it belongs.

**Do not solve this by making the main repository private.** The Colab badges
throughout the material require public access; private repos force every student
through a GitHub OAuth grant, which defeats the purpose of having a
zero-installation fallback.

### 1.3 Instructor-only tooling

```bash
pip install otter-grader
```

Needed only to build problem sets from masters. Not needed to run any notebook,
and not installed on DataHub by default.

---

## 2. Before each semester

Start **three weeks out**. Two of these have real lead times.

### 2.1 Compute — DataHub **[Berkeley]**

`datahub.berkeley.edu` is free, authenticates through bCourses, and requires no
application. Students already have accounts. But two things need doing early:

**Request a memory increase.** The default is 1 GB per user, which will
OOM-kill kernels once students hold trajectory arrays or run stochastic
ensembles. Open an issue at
`github.com/berkeley-dsep-infra/datahub/issues/new/choose` requesting a group
profile keyed to your **bCourses course ID** with `mem_limit: 4G`,
`mem_guarantee: 2G`.

Requests are auto-approved when `students × GB ≤ 200` for a full semester, so 35
students × 4 GB = 140 is comfortably inside. It is a pull request against their
config repo, so allow **several days**, and the request stalls silently without
a course ID attached.

Verify it landed — from a notebook, *not* with `free -m`, which reports the
Kubernetes node's memory and will read ~64 GB regardless:

```python
print(open("/sys/fs/cgroup/memory.max").read().strip())
# 1073741824 = still 1 GB   |   4294967296 = request landed
```

**Batch any package requests** in the same window; installs take about two
business days.

*Not at Berkeley?* Any JupyterHub works — substitute the hostname in the
nbgitpuller links. If you have no hub, the Colab badges work anywhere and
require only a Google account.

### 2.2 Check the environment versions

The binding constraint is whichever student environment is **oldest**. Run the
PS0 check cell in each supported environment and record the numbers:

| | DataHub | Colab |
|---|---|---|
| Python | 3.11.0 | 3.12.13 |
| NumPy | 2.4.2 | **2.0.2** |
| SciPy | 1.17.0 | **1.16.3** |

*(measured August 2026 — re-measure each year)*

Colab lags. Set `requirements.txt` and the CI pin to the **floor**, not the
newest. Testing against current libraries tells you nothing about whether
students can run the code.

Also confirm Colab works with an institutional Google account — in a
**private/incognito window**, signed in only as your `@berkeley.edu` address. If
you are signed into several Google accounts, Colab silently uses the default and
you will conclude it works when you tested a personal Gmail.

### 2.3 Grading — Gradescope **[Berkeley]**

Berkeley site-licenses Gradescope — no request form, no eligibility check.
As of January 7 2026 only **LTI 1.3** exists; LTI 1.0 was removed.

**Do this first, in August.** Log in once at
`https://www.gradescope.com/auth/saml/berkeley` with CalNet, *before* touching
bCourses. Then confirm you can see a **Create Course** button. If you cannot,
your account was created as a *student* account and only `help@gradescope.com`
can flip it — a multi-day round trip you do not want in week 1.

**Decide the 147/247 question before publishing the sites.** They meet together,
so use **one merged bCourses site containing both official sections**, linked to
**one** Gradescope course. Berkeley's tool is **Manage Sites** (which now also
contains the old Official Sections tool). Two parallel Gradescope courses means
duplicating every assignment and every autograder Docker build. Merging *after*
students have submitted work is not reliably self-service — email
`bcourseshelp@berkeley.edu` if you are already past that point. If you need to
distinguish 147 from 247, use **sections inside the one course**.

**Enable and link:**

1. bCourses → **Settings** → **Navigation** tab
2. Drag **Gradescope** into the enabled list → **Save** *(easy to miss; nothing
   persists without it)*
3. Click the new **Gradescope** nav item → choose new or existing course →
   **Link Course**
4. Gradescope → **Roster** → **Sync bCourses Roster**

> **Roster sync is manual.** It does not update on add/drop. Re-sync at the end
> of week 1, end of week 2, and after the add/drop deadline. Re-syncing
> overwrites any manually customised section names.

**Create assignments from bCourses**, not from inside Gradescope, or they will
not be linked to the gradebook: **Assignments** → **+ Assignment** → Submission
Type **External Tool** → **Find** → **Gradescope** → create a new Gradescope
assignment → **Link Assignment** → set points → **Save and Publish**.

Then in Gradescope choose **Programming Assignment** and upload the zip from
`private/build/psNN/dist/autograder/`. Take the **default Ubuntu 22.04 base
image** — Otter's `setup.sh` builds its own conda environment, so a
Python-preloaded variant only wastes layers.

> **Build the Docker image days before release.** Otter's setup downloads
> Miniforge and solves a conda environment; expect roughly 10–25 minutes, longer
> if PDF export is enabled. Also raise the defaults on the assignment settings
> page: memory defaults to **768 MB** and timeout to **10 minutes** (max 40),
> both tight for a NumPy/SciPy autograder.

**Grade passback is a manual push**, not automatic: Gradescope → **Review
Grades** → **Post Grades to Canvas**. Only the overall score posts; the
per-question breakdown stays in Gradescope. Two known failure modes — posting
fails if the bCourses course has *concluded* (check the term end date), and
TAs/Readers often cannot sync rosters or post grades due to a Canvas permission
on viewing email addresses. If your reader needs to post, give them
**Instructor** in Gradescope.

Campus contact: `gradescope@berkeley.edu`, ~1 business day.

### 2.4 Distribution links — nbgitpuller

One link per assignment, posted on bCourses. Format:

```
https://datahub.berkeley.edu/hub/user-redirect/git-pull
  ?repo=https://github.com/ArkinLaboratory/posb2026
  &branch=main
  &urlpath=lab/tree/posb2026/problem-sets/ps01-modeling/ps01.ipynb
```

Generate and check them all at once:

```bash
python tools/check_links.py
```

That reproduces nbgitpuller's own logic — `git ls-remote` for the repo and
branch, a raw-content HEAD request for the notebook — and prints paste-ready
links. It catches three of the four real failure modes with no browser.

> **`&backup=true` does not work on DataHub.** It is an nbgitpuller **1.3.0**
> feature and DataHub pins **1.2.2**, which silently ignores the parameter. A
> "reset link" built this way appears to work and does nothing. Re-check after
> DataHub bumps the pin. *(An earlier version of this runbook recommended it.
> It was wrong.)*

> **The `branch` default is not `master`.** nbgitpuller's own docs say it is,
> and that has been false since 1.1.0 — it now resolves the repo's default HEAD.
> So omitting `branch` works. But the **Berkeley link-generator extension
> pre-fills the field with `master`** and uses it in preference to the branch it
> detected, which produces a link that fails for every student on a `main`-only
> repo. Always read the `branch=` in the generated URL.

**The urlpath must include the clone folder name** — `lab/tree/posb2026/…`, not
`lab/tree/…`. This is the single most common mistake, and its symptom is
deceptive: the pull *succeeds*, then JupyterLab says "Could not find path",
which students read as "the assignment is missing."

### Testing a link — incognito does not work

Your DataHub home directory is persistent NFS keyed to your CalNet ID. Once
`~/posb2026` exists, nbgitpuller takes the *update* path — `git fetch` against
the folder's own configured remote — instead of cloning. **A private window logs
you in as the same CalNet ID, into the same home directory, so it tests
nothing.**

The correct test, in a DataHub terminal:

```bash
mv ~/posb2026 ~/posb2026-mine    # or rm -rf if you have no local edits
```

Then click the link. With the folder absent, nbgitpuller runs the true
first-time path and exercises every failure mode a student would hit.

Non-destructive alternative: add `&targetPath=linktest` and point `urlpath` at
`linktest/…` instead. Cleaner, but it does not test the exact string you ship.

Best of all: have your reader or a colleague click every link once. Their home
directory genuinely lacks the folder, and they are a different identity.

> **A Berkeley-specific false positive.** DataHub mounts a GitHub App
> credential helper (`berkeley-datahub-git-access`). If you have ever authorised
> it, your DataHub server can clone your *private* repos transparently and your
> students' cannot — so a private-repo link works perfectly for you, even after
> deleting the folder, and fails for all 35 of them. `check_links.py` guards
> against this by testing unauthenticated; run it with no GitHub credentials in
> the environment.

> ### ⚠ The nbgitpuller trap
>
> On a conflicting line, **the student's version always wins.**
>
> A student who has *executed* a notebook has changed `execution_count` and
> `outputs` on nearly every cell. So if you fix a bug in one of those cells and
> push, **the fix silently never reaches anyone who already ran it.** They keep
> working from the broken version and you find out when they submit.
>
> Two rules follow. Ship each assignment as a **new folder** — never patch a
> notebook students have run. And keep reusable logic in `.py` modules, which
> students rarely edit, so merges stay clean.

### 2.5 Pre-flight checklist

- [ ] Tests, build-check, and notebook execution all pass on a clean clone
- [ ] DataHub memory increase confirmed via `/sys/fs/cgroup/memory.max`
- [ ] Colab verified with an institutional account, in a private window
- [ ] Version floor recorded; `requirements.txt` and CI pinned to it
- [ ] 147/247 merged into one bCourses site; Gradescope linked; roster synced
- [ ] Autograder Docker image built and **Test Autograder** run; memory and timeout raised
- [ ] `python tools/check_links.py` passes, and one link clicked after `mv ~/posb2026 ~/posb2026-mine`
- [ ] Gradescope: CalNet SAML login done, **Create Course** button visible
- [ ] `private/` pushed to the private repo
- [ ] Dates in `docs/course-map.md` and the syllabus match the registrar

---

## 3. The weekly loop

### 3.1 Authoring a session notebook

Notebooks are **build artifacts**. The Python modules in `tools/sources/` are the
source of truth.

```bash
# edit tools/sources/sNN.py, then:
python tools/build_notebooks.py
python tools/execute_notebooks.py
git add -A && git commit -m "Session NN" && git push
```

**Never hand-edit a `.ipynb`.** Executed notebooks churn `execution_count` and
`outputs` on every cell, which makes diffs useless and — much worse — guarantees
the nbgitpuller conflict above.

Add each new notebook to the `NOTEBOOKS` list in `tools/build_notebooks.py`.

### 3.2 Authoring a problem set

```bash
# edit private/sources/psNN.py, then:
python tools/build_problem_sets.py psNN
```

That one command produces three artifacts, going three places:

| Artifact | Location | Audience |
|---|---|---|
| `psNN.ipynb` (blanks) | `problem-sets/` — **committed** | students, publicly |
| `*-autograder.zip` | `private/build/` | Gradescope only |
| `psNN-SOLUTIONS.html` | `private/build/` | you and your reader |

It also **executes the solution notebook and requires every `grader.check` to
pass**. A green build means your reference answers actually satisfy every test,
visible and hidden, in the namespace students will have.

Then:

```bash
git add -A && git commit -m "PSNN" && git push
cd private && git add -A && git commit -m "PSNN master" && git push
```

Upload the zip to Gradescope. Post the nbgitpuller link on bCourses.

### 3.3 Writing tests — the rule that matters

**Visible tests are embedded verbatim in the student notebook. Hidden tests are
not.** Verified on real output:

```
public test text in student notebook : True
hidden test text in student notebook : False
```

So:

- **Visible tests check *properties*** — shapes, conservation laws, scaling
  relations, monotonicity, consistency between the student's own functions.
- **Hidden tests check *values*.**

A visible test asserting `molecules(1.0, 1.0) == 0.6022` hands over the answer;
a student can return the constant and pass. A visible test asserting that
doubling the concentration doubles the count catches a broken function without
revealing the formula.

Tell students this explicitly. A green visible check means *not obviously
broken*, not *correct*.

### 3.4 Otter Assign format — traps, verified empirically

These cost hours to establish. Two of them fail **silently**.

1. **Solutions must sit between `# BEGIN SOLUTION` / `# END SOLUTION` *block*
   cells** (fenced ```` ```otter ```` markdown cells), like `# BEGIN TESTS`.
   Inline `# BEGIN SOLUTION` comments **alone strip nothing**. Get this wrong
   and `otter assign` exits 0 while writing a "student" notebook containing
   every answer. **No warning.**
2. **The two mechanisms compose.** A block-tagged code cell with inline markers
   keeps the signature and docstring and replaces only the marked body.
3. **Every cell object must be distinct.** Cells are mutable dicts; a helper
   returning a shared `# END QUESTION` cell aliases it across the notebook,
   and Otter then strips only the first solution block. The builder fails the
   build on aliased cells rather than letting this through.
4. **Question points must equal the sum of that question's test points.**
5. **Otter assigns random cell ids to the student notebook on every build.**
   The builder normalises them to `c000`, `c001`, … before committing, so an
   unchanged rebuild is a true no-op. Without that, every rebuild rewrites
   ~19 ids — noisy diffs, and every affected cell looks changed, which is
   exactly the state that makes nbgitpuller conflict with students' executed
   copies. If you fork this pipeline, keep that normalisation step.

**Always run the leak check before publishing a set** — parse both notebooks and
confirm no solution fragment appears in the student version. Do not rely on
reading the file.

---

## 4. Onboarding a reader or GSI

Most of this is deliberately *not* needed.

**What they need:**

1. **Gradescope access** — add them as a Course Staff / Grader on the Gradescope
   course. This is where all grading happens.
2. **The solutions document** — `private/build/psNN/psNN-SOLUTIONS.html`, the
   executed solution notebook with derivations, plots and printed values. Send
   it directly; it must not go in the public repo.
3. **A rubric** per free-response question, in Gradescope.

**What they do not need:** the repository, git, Python, Otter, or DataHub.
Autograded questions are scored without human involvement; free-response
grading happens entirely in Gradescope's interface.

**Only if they will write or edit problems:** add them as a collaborator on the
private repo, and point them at [For Instructors](for-instructors.md) plus §3.3
and §3.4 above.

### Load, so you can staff it honestly

Roughly half the assessed techniques in this course are autogradable; the rest
are derivations needing a human. The load is **front-weighted** — Part I is
derivation-heavy, Part II computation-heavy — so reader hours peak around PS2–PS3.

That is also where the course's value is concentrated, so it is the wrong place
to economise. Resist making every problem numerically checkable to reduce
grading: that reintroduces exactly the defect this course was rebuilt to fix.

---

## 5. During the term

### Day one

Ten minutes, with laptops:

1. Project one short URL → the PS0 nbgitpuller link
2. Everyone opens it → bCourses SSO → JupyterLab opens the notebook. Expect
   1–3 minutes for the first simultaneous spawn
3. Run the environment check cell. **If the plot renders, they are done**
4. Two named failure modes, two fixed answers:
   - *bCourses login fails* → not enrolled yet → use the Colab badge today
   - *spawn hangs > 5 min* → reload once, then Colab
5. State the submission rule aloud: **Restart Kernel and Run All Cells**, then
   submit to Gradescope
6. Mention the 30-minute idle timeout so nobody is surprised
7. Show the reset link once

### Things that will come up

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'posb'` in Colab | Setup cell skipped | Run it. Colab opens the notebook alone, without the package |
| Kernel dies on a large simulation | 1 GB default memory | The §2.1 request; check `/sys/fs/cgroup/memory.max` |
| Work lost after a break | 30-minute idle cull | Save intermediate results to disk; files persist, memory does not |
| Student's notebook "won't run" | Cells run out of order | Restart Kernel and Run All Cells |
| Your fix never reached a student | nbgitpuller keeps their version | Ship a new folder. `backup=true` does not work on DataHub 1.2.2 |
| Link works for you, fails for students | Private repo + DataHub's GitHub App credential | `python tools/check_links.py` with no GitHub credentials |
| "Could not find path" after a successful pull | urlpath missing the clone folder name | `lab/tree/posb2026/…` |
| Gradescope grade posting fails | Course concluded, or TA permissions | Check term dates; post as Instructor |
| Notebook works locally, not on DataHub | Version drift | Check against the floor in §2.2 |
| `FileNotFoundError: 'otter'` | Instructor dependency missing | `pip install otter-grader` |

### End of term

- [ ] Post worked solutions to bCourses (**not** the repository — see below)
- [ ] Export Gradescope grades to bCourses
- [ ] Remind students to **download their work**; DataHub home directories are
      not backed up and access ends ~9 months after graduation
- [ ] Push `private/` — masters, exams, and any new problems
- [ ] Update `docs/course-map.md` status marks
- [ ] Re-measure environment versions for next year

---

## 6. Publishing solutions: decide on purpose

This course distributes worked solutions to enrolled students through
**bCourses** and does **not** publish them in the repository.

The trade cuts both ways. Published solutions are far more useful to people
working through the material independently — which is much of the point of
putting a course online. But once answers are indexed, every problem must be
rewritten each year. Berkeley's Data 8 does not publish solutions for exactly
this reason.

The compromise here: problems stay reusable, and the **worked examples** in the
session notebooks are public and demonstrate every technique the problem sets
assess. Someone self-studying has a worked reference for each method without an
answer key.

If you decide differently, change it in three places — `problem-sets/README.md`,
the problem-set README, and the closing cell of the master source — and keep them
consistent. They drifted apart once already.

---

## 7. The discipline that holds this together

One artifact does more work than any tool here: the **coverage matrix**. Four
columns — *technique*, *the session that demonstrates it*, *the instrument that
assesses it*, *whether a machine can grade it*. This course has 74 rows, and one
rule:

> Nothing is assessed that was not demonstrated first.

Check every problem against it before release. When it was first built for the
previous version of this course it found a 20-point problem on retroactivity
supported by two occurrences of the phrase "impedance matching" in nineteen
lecture decks, both in bullet lists — and the criterion for oscillation assessed
but never once stated.

Then, rebuilt against the *corrected* calendar, it caught the same class of
failure recurring: stochastic simulation scheduled for October 6, examined
October 15, with no graded practice in between. Caught in August instead of by
thirty students in October.

Keep it current. It is the cheapest quality control in the course.
