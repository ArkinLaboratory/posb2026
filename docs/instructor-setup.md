# Instructor Setup

[← back to README](../README.md) · See also [For Instructors](for-instructors.md) (adapting the material) and [Design Notes](design-notes.md) (why it is built this way)

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

Berkeley site-licenses Gradescope; all features are free to instructors.

1. Enable it in bCourses course navigation
2. Link the course and sync the roster
3. Create one **Programming Assignment** per problem set
4. Upload the autograder zip from `private/build/psNN/dist/autograder/`

Grades post back to bCourses. Free-response questions appear in Gradescope's
manual-grading interface.

### 2.4 Distribution links — nbgitpuller

One link per assignment, posted on bCourses. Format:

```
https://datahub.berkeley.edu/hub/user-redirect/git-pull
  ?repo=https://github.com/ArkinLaboratory/posb2026
  &branch=main
  &urlpath=lab/tree/posb2026/problem-sets/ps01-modeling/ps01.ipynb
```

**Set `branch` explicitly.** It defaults to `master`, and students get an
unhelpful failure otherwise.

Add `&backup=true` to make a **reset link** — it renames the student's copy with
a timestamp and re-clones fresh. Post one alongside each assignment; it is the
answer to most "I broke my notebook" emails.

**Test every link in a private window.** In your own browser the repo is already
cloned, so a broken link still appears to work.

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
- [ ] Gradescope linked to bCourses, roster synced
- [ ] Every nbgitpuller link tested in a private window
- [ ] Reset (`backup=true`) links posted
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
| Your fix never reached a student | nbgitpuller keeps their version | Ship a new folder; send a `backup=true` reset link |
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
