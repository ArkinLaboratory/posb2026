# The course site: how bCourses was built, and how to rebuild it

[← back to README](../README.md)

Written the week the site went up, while the details were still fresh. It is a
record of what was actually clicked in Fall 2026 and, more usefully, of the
half-dozen places Canvas quietly does something other than what you expect.
Everything here was hit for real; nothing is anticipated.

Companion pages: [where-things-live](where-things-live.md) is about files and
the boundaries between machines; [instructor-setup](instructor-setup.md) is
about accounts, DataHub and Gradescope. This page is only about the course site.

---

## 1. What the site is for

Three systems, one job each, and the whole design follows from keeping them
apart:

| | holds | who can see it |
|---|---|---|
| **bCourses** | the table of contents, the lecture PDFs, announcements, grades | enrolled students, via CalNet |
| **GitHub** (`posb2026`) | the source of truth for notebooks, figures, docs | the world |
| **DataHub** | where a notebook actually runs | anyone with a CalNet ID |

bCourses is an **index, not a store.** The only files that live there are the
ones that cannot live anywhere else — lecture PDFs, which are behind CalNet
precisely because they may embed figures from published papers. Everything a
student *runs* is a link out to DataHub, which clones from GitHub.

The rule that keeps it usable: **anything a student needs is one click from the
Modules page.** They should never have to know that a repository exists, or
what a branch is, or that there is a private half of the course.

---

## 2. One-time setup, at the start of a term

### 2.1 Turn Modules on. This is the first trap.

A new Canvas site does not show **Modules** in the student navigation. You will
not notice, because the instructor view shows it. You build three modules,
publish everything, and a student sees a course with no content in it.

    Settings → Navigation → drag Modules into the enabled list → Save

While you are there, disable everything you do not intend to maintain. An
enabled-but-empty tab reads to a student as a broken course, and every enabled
tab is a second place they might look for the thing that is in Modules.

### 2.2 Make the home page the Modules page

    Home → Choose Home Page → Modules → Save

So the first thing a student sees on landing is the index, not an empty
activity stream.

### 2.3 Verify as a student before you believe any of it

    Home → Student View  (top right)

Do this now, with an empty site, so you learn what "empty" looks like. Then do
it again after every module you build — see §6.

---

## 3. The shape of the site

Two kinds of module. One permanent, the rest one per week:

```
Start here                                     never gets a date; always first
   Syllabus                        Page
   How this course runs            Page
   Problem Set 0                   External URL  → DataHub

Week 1 — Specification and substrate
   Session 1 slides                File          (PDF, uploaded)
   Session 2 slides                File          (PDF, uploaded)
   Reading: <author year>          External URL  → UC Library proxy
   Problem Set 0                   Assignment    (due date, gradebook column)

Week 2 — Modeling I / II
   ...
```

**Start here** exists so that a student arriving in week 6 — added late, or
lost — has a single place that explains the machinery. It is the only module
that is not chronological, and it is the only one that never changes after
week 1.

Week modules are named for their content, not just their number. `Week 3` tells
a student nothing when they are looking for the deck on stochasticity.

---

## 4. Which item type for which thing

Canvas's **+** button offers Assignment, Quiz, File, Page, Discussion, Text
Header, External URL, External Tool. Only five matter here, and picking the
wrong one is the cause of half the traps in §5.

| The thing | Item type | Why that one |
|---|---|---|
| Lecture slides | **File** | Uploaded PDF, behind CalNet. Never a link to GitHub — assembled decks are gitignored and never published. |
| A notebook students run | **External URL** with the nbgitpuller link, **Load in a new tab** ticked | The link *is* the deliverable. See [where-things-live §5](where-things-live.md#5-how-a-notebook-reaches-a-student). |
| Anything graded | **Assignment** | It is the only type that produces a due date and a gradebook column. Put the nbgitpuller link in the assignment body. |
| A paper | **External URL** to the DOI through the UC Library proxy | Never upload the PDF. You cannot redistribute it, and the proxy makes each student authenticate as themselves. |
| Prose you write for the site | **Page** | Editable in place, versioned by Canvas, and it can be linked to from anywhere. |

Note the doubling on problem sets: PS0 appears **twice** — once in *Start here*
as a plain link, so a lost student can find it, and once in *Week 1* as the
Assignment that carries the deadline. That is deliberate, not a mistake to tidy
up.

---

## 5. The traps, with symptoms

Each of these cost real time. They are ordered by how much.

### 5.1 The Syllabus is neither a Page nor a File

Canvas has a **built-in Syllabus tab** with its own body text, edited from its
own screen. It is a third thing. So when you go to add it to a module:

- *Add item → File* — the syllabus is not in the file list, because you never
  uploaded a file.
- *Add item → Page* — it is not in the page list either, because the built-in
  Syllabus is not a Page. The picker looks empty even though the syllabus is
  plainly sitting there in its tab.

Two ways out, and it is worth deciding on purpose:

1. **Make a Page** and put the syllabus in it. Then the module item is an
   ordinary Page and behaves like everything else. This is the route taken in
   Fall 2026.
2. **Point at the built-in tab** with an External URL to
   `…/courses/<id>/assignments/syllabus`. One less copy to keep in sync, but
   the item is a bare link and the built-in tab has its own layout you do not
   control.

Either way, the durable source is `docs/syllabus.md` in the repository. What is
on Canvas is a copy, and it goes stale the moment the schedule slips. When you
paste it in, use the **`</>` button** in the editor toolbar to work in raw HTML
— the rich-text editor mangles nested lists and anything that looks like code.

### 5.2 A File item shows the raw filename

Symptom: the module reads `PoSB_Session03_Modeling_I.pdf`.

Cause: the *Add Item* dialog has a **Page Name** box for Page and External URL
items, and **no such box for File items**. There is nowhere to type a title, so
Canvas uses the filename.

Fix: add it, then **⋮ → Edit** on the item and give it a title. The file keeps
its name; the item gets a label. Do this immediately — a module full of
`PoSB_Session0*.pdf` is the single ugliest thing on the site.

### 5.3 There are two publish states, and both must be green

Every **item** has a publish state. Every **module** has its own. A fully
published set of items inside an unpublished module is invisible to students,
and the module page gives you no warning, because from the instructor side
everything is legible either way.

Publish the items first, then the module. Then check as a student (§6).

### 5.4 DataHub links must open in a new tab

When you add the External URL, tick **Load in a new tab**. Without it Canvas
renders DataHub inside its own iframe: the CalNet redirect fights the frame,
and even when it survives, JupyterLab in a 700-pixel column is unusable.

### 5.5 The nbgitpuller traps

Three of them, all still live, all documented once in
[where-things-live §5](where-things-live.md#5-how-a-notebook-reaches-a-student):
the `urlpath` must include the clone folder; Berkeley's link generator pre-fills
`branch=master` and ours is `main`; and `&backup=true` is silently ignored by
the nbgitpuller DataHub pins. Generate links with `python tools/check_links.py`
rather than the web generator and none of the three can happen.

**And incognito does not test them.** A private window is the same CalNet ID and
the same NFS home directory, so `~/posb2026` already exists and nbgitpuller
takes the *update* path instead of the clone path. Only a second person's
account exercises what a student actually hits.

### 5.6 A Gradescope Homework/Problem Set will not accept a notebook

This one is not obvious and it is the kind of thing you discover with a student
on the phone. Gradescope's assignment types differ in what students may upload:

| Gradescope type | Students may submit |
|---|---|
| **Homework / Problem Set**, **Exam / Quiz** | a single PDF, or images per question (`.png`, `.jpeg`, `.gif`, `.heic`). **No `.ipynb`.** |
| **Bubble Sheet** | PDF only |
| **Programming Assignment** | *any* file type, several per submission, `.ipynb` included |
| **Online Assignment** | any file type |

So a notebook course lives on **Programming Assignments**, whatever the
assignment actually is. And an autograder is not required to use one: leave the
autograder points at 0 and tick **enable manual grading**, and it becomes a
plain file drop with a gradebook column. That is the right shape for anything
ungraded — PS0, a survey, a reflection — and it costs no Docker build.

The corollary is a lead time you cannot compress. A Programming Assignment that
*does* autograde needs its Docker image built on Gradescope's side, which takes
10–25 minutes for an Otter environment and must be tested with a real
submission before students see it. Build it days before the assignment posts,
not the morning of. See [instructor-setup §2.3](instructor-setup.md).

### 5.7 Two course numbers, two assignments — and the ceiling that eats extra credit

Every problem set carries one extra question: **required for BioE 247, extra
credit for BioE 147.** Those are two different denominators, and one Gradescope
assignment has one outline. So each set is **two assignments, one per section**:

| | assigned to | Question *n* |
|---|---|---|
| `PSn` | 147 section | **0 points**, with rubric items worth up to +*e* |
| `PSn — BioE 247` | 247 section | **worth *e* points**, so the total is base + *e* |

Build the second by **duplicating** the first once it is fully configured —
Gradescope's duplicate copies the outline, the rubric *and* the autograder —
then change the one question's point value and the section it is assigned to.
Each student submits once and appears in exactly one queue, so you grade N
submissions, not 2N.

**Do not** do this as a small add-on assignment alongside a shared main one.
It looks tidier and it breaks the drop rule: a 247 student would carry
eighteen items in the problem-set group against a 147 student's nine, so
"lowest two dropped" could discard two small supplements instead of two whole
problem sets. Same stated policy, materially different relief.

**The trap.** A 0-point question with positive rubric items is Gradescope's
documented way to do extra credit — but the **point ceiling is enabled by
default and prevents scores above 100%**. Leave it on and a 147 student who
earns +5 on a 34-point set is silently capped at 34. Disable the ceiling on
that question when you build it. Nobody discovers this by looking; they
discover it when a student asks where their extra credit went.

The wording students read comes from `tools/sources/common.py` (`grad`), which
is injected into every problem-set master. Do not retype the policy into a
notebook — PS1 shipped saying "students in 147 may attempt this for no credit",
which was the exact opposite, and a student had already pulled it.

### 5.8 The Gradescope frame accepts the notebook. It never provides it.

A problem set's Canvas description must carry **Open in DataHub** and **Open in
Colab** links. The embedded Gradescope panel is an upload box and nothing else,
so a description without links leaves a student with somewhere to submit and no
way to get the thing they submit. This happened on PS1 in Fall 2026 and a
student reported it within the hour.

The rule that prevents it: **the Canvas description for a problem set is the
problem-set README**, converted to HTML, not fresh prose. `problem-sets/psNN-*/README.md`
already opens with both links. PS0's page worked because it was pasted from its
README; PS1's failed because it was composed in the Canvas editor by someone
who knew the README had the links and wrote *"links are in the problem-set
README"* instead of carrying them across.

Paste it with the **`</>`** button. The DataHub URL is a query string full of
`&` and the rich-text editor mangles it.

### 5.9 The Gradescope roster is synced by hand, and nothing tells you it is stale

**Gradescope → Roster → `Sync bCourses Roster`.** It is not automatic. Gradescope's
own guide: *"If students add/drop in Canvas, be sure to re-sync the roster."*
A student who is enrolled in bCourses and absent from the Gradescope roster
**cannot submit**, and finds out at 11pm on the due date. Nothing warns you.

On 2 September 2026 the roster held 25 students. One click of Sync took it to
31. Six people could not have handed in PS1.

**Do not check this by adding up the Sections page.** Sections counts
*memberships*, not people — a student normally holds two, a LEC and a DIS — so
four sections reading 16 / 17 / 16 / 15 is about 31 humans, not 64. The
authoritative count is **People**, filtered to Students. The arithmetic is
worth doing anyway: it is what exposed the gap.

Re-sync after every add/drop, and at minimum before every problem set opens.
Leave the enrolment notification **on** when you sync mid-term — someone being
added now needs to know they can submit.

The sync also brings sections across, so Gradescope's roster shows who is 147
and who is 247. Useful for filtering while grading. It does **not** let you
scope an assignment to a section; that stays on the Canvas side (§5.7).

### 5.10 Gradescope's defaults are wrong for a course like this one

Every one of these is on or set by default and every one needs changing. None
of them announce themselves.

| Default | Why it is wrong here | Set to |
|---|---|---|
| **Group submission: on**, no size limit | Lets any number of students submit one notebook for one grade. Contradicts the COLLABORATORS field and the individual-work policy. | **off** |
| **GitHub and Bitbucket: on** | A student submitting via GitHub sends a repository, not `psNN.ipynb`, and the autograder finds nothing. | **off** — Upload only |
| **0.5 CPU, 0.75 GB RAM** | A conda environment plus SciPy plus an ODE integration. | **2.0 CPU, 3.0 GB** |
| **10 minute timeout** | Your correct code passes easily; a student's runaway loop hits the wall and fails as `autograder_error`, which reads as *your* bug. | **20 minutes** |
| **Point ceiling: on** | Silently caps extra credit. See §5.7. | off, on extra-credit questions only |

### 5.11 "Published" in Gradescope does not mean what it means in Canvas

There is **no publish step for a Gradescope assignment.** Visibility to students
is governed entirely by the **Release Date**. The *Published* column in the
assignment list refers to **grades** being released, which is why a correctly
configured, fully visible assignment shows an empty circle there and a banner
reading "No Published Grades." That is the correct state until you have graded.

Related: check the Canvas assignment's **Available from** date. PS1 carried
"Available after Aug 3" — a leftover nobody chose, three weeks before term.
Harmless here because assignments are exposed early on purpose, but a date
nobody picked is how a "why can't I see this" message happens in November.

### 5.12 Building the second section's assignment, click by click

Everything in this subsection was learned the slow way on 2 September 2026,
building `PS1 (BioE247)` from `PS1 (BioE147)`.

**Duplicate is at the bottom of the Assignments page.** Not in the `⋮` menu
beside an assignment — that offers only *Assignment Settings* and *Delete
Assignment*, which is why you will conclude the feature does not exist. Scroll
to the foot of the list; it sits beside *Create Assignment*. It needs an
institutional licence, which Berkeley has.

**What duplication carries:** settings, the question outline, every question
rubric, and the autograder configuration. The copy then **starts its own Docker
build** from the copied zip — expect `building as of …` on the Configure
Autograder page, 10–25 minutes, and no action needed. That is the copy building
*its own* image, not a link back to the original.

**What it does not carry: the LMS link.** Good, because a second Gradescope
assignment pointing at the same Canvas assignment would fight over grade
passback. Verify rather than assume — the tell is on the assignment's Settings
page:

| | linked to Canvas | not linked |
|---|---|---|
| top field | read-only **BCourses Assignment Name** with a chain icon | editable **Title** |
| footer | Delete · **Unlink from LMS** · Save | Delete · Save |

**Canvas's quick-edit dialog cannot set a submission type.** The inline `+`
form and `⋮ → Edit` expose only Name, Due at and Points. An assignment created
there silently becomes **"a text entry box"**, and it will happily publish that
way. **`More Options`**, or the full **Edit** page from the assignment itself,
is the only route to Submission Type.

**Linking an existing Gradescope assignment:** Submission Type → **External
Tool** → **Find** → **Gradescope** → in the dialog choose **"An existing
Gradescope assignment"**, pick it, **Link Assignment**. The dialog notes that
*"the LMS assignment name will override the Gradescope assignment name"* — so
rename in Canvas only; Gradescope catches up. (It does **not** refresh a name
that changed *after* linking, which is cosmetic and not worth chasing.)

**Assign to: the LEC for that course number.** The site carries four sections —
a LEC and a DIS for each of 147 and 247 — but enrollments come in pairs, so the
LEC alone reaches everyone in that number. Remove *Everyone*, add the one LEC.

Listing both sections also works and is what PS1 shipped with. It is worth
knowing why the shorter form is better: a student in two listed sections has two
applicable due dates the moment you grant a per-section extension, which is the
one occasion you would ever edit this field again.

The check, if you doubt it: sort the People page by Section and look for anyone
in a DIS without its LEC. There were none.

**A new assignment does not appear in a module by itself.** Add it: Modules →
the week's `+` → **Assignment** → pick it. Both section variants can live in the
same week; Canvas hides an assignment from students outside its *Assign to*
list, in Modules as well as in Assignments, so each student sees exactly one.

---

## 6. The settling test: View as Student

Nothing above is finished until this passes. **Home → Student View**, then click
every item in every module.

**It cannot preview an LTI tool, and Gradescope is one.** Canvas launches as its
Test Student, Gradescope has no such person on its roster, and the launch
resolves to your instructor identity — so the embedded frame shows you *Manage
Submissions* and *Configure Autograder*, which no student can ever see. Student
View verifies the Canvas half only: publish state, points, dates, and whether
the description renders. The Gradescope half can only be checked by a second
person with a student account. Budget for that: a GSI or reader who clicks every
link once is the single most valuable ten minutes in the setup.

It catches, in the order it has actually caught them:

- a module you published items in but did not publish
- File items still named after files
- an external link that opens inside the Canvas frame
- an nbgitpuller link that clones and then cannot find the notebook
- the *Start here* module ordered after Week 1, because Canvas appends new
  modules to the bottom

Run it after every week's module goes up. It takes ninety seconds.

---

## 7. Announcements

One announcement per week, posted when the module goes up. Three sentences:
what happened, what to click, what is due. **Link into the module** rather than
describing where it is.

Announcements are the only push channel — students do not poll Modules. If
something changes after an announcement is posted, **edit the announcement**
rather than posting a second one. A second post about the same week trains
people to ignore the first.

Two standing decisions worth writing down because they will come up again:

- **Problem sets are exposed early on purpose.** PS*n* becomes visible as soon
  as it is built, often before it is announced. Say so once, in *How this
  course runs*, and then it needs no announcement of its own each time.
- **Solutions are a separate decision**, made per problem set, and it is
  documented in [instructor-setup §6](instructor-setup.md).

---

## 8. The weekly loop

The week's sequence — build, verify, print, upload, module, publish, Student
View, announce — is in
**[making-a-course §6](making-a-course.md#6-the-weekly-loop)**, which owns it.
Steps 8 to 13 there are the site half. Come back here for the click detail on
any of them.

---

## 9. What to do differently next year

- **Build *Start here* before day one.** In 2026 it went up in week 2, which
  means the students who most needed it — the ones adding late — had it last.
- **Turn Modules on before you build anything**, not after you notice.
- **Upload every lecture PDF into a `lectures/` folder** in Files. The File item
  picker is a flat list and it gets long fast.
- **Name modules for content**, from module one. Renaming later breaks nothing,
  but nobody does it.
- **Give PS0 a trivial autograder.** In 2026 it was a plain file drop, which
  tests that a student can submit but not that *your* autograder pipeline works
  — so the first real exercise of the Docker image, the `otter.export` cell and
  the zip upload was PS1, which is graded. Two Otter tests in PS0 that check
  nothing but `1 + 1` would move that discovery a week earlier and cost
  nothing. It has to be in the notebook from the start: once students have
  pulled PS0 you cannot change it, because nbgitpuller keeps their copy.
- Decide once whether **Files** is in the student navigation. It is not needed —
  they navigate by Modules — and hiding it removes a second place to look.
