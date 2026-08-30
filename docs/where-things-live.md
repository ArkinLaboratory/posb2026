# Where everything lives, and how to check it got there

[← back to README](../README.md)

Written for one person: you, on the Mac, the morning of a lecture. It assumes
nothing and it is meant to be read start to finish once and then used as a
lookup.

There are a lot of moving parts now — two git repositories, a sandbox that
cannot see your disk, a hub, an autograder, a course site, and a deck builder.
Each one is simple. The complexity is entirely in the **boundaries between
them**, so that is what this page is about.

---

## 1. The three places a file can be

| Where | What it is | Can Claude write it? | Can students see it? |
|---|---|---|---|
| **`~/Documents/Claude/Projects/PoSB/posb2026`** on your Mac | the real thing. What you teach from. | only by an explicit copy step | no |
| **`github.com/ArkinLaboratory/posb2026`** | the public copy | only via you | **yes** |
| **`github.com/ArkinLaboratory/posb2026-private`** | masters, paper figures, movies | only via you | no |
| Claude's sandbox | a scratch clone on a different computer | yes | no |

**The one sentence that matters:** the sandbox and your Mac are different
computers with different disks. Nothing moves between them automatically. When
Claude says "I built the deck," that happened *somewhere else*, and the file
only exists on your Mac after a separate copy step. This has gone wrong twice.

### Checking that a handoff actually landed

Claude runs `python tools/handoff.py --emit` in the sandbox, which writes
`docs/handoff.json` — a sha256 for every file, including built decks. That file
comes over with everything else. Then, on your Mac:

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026
python tools/handoff.py --check
```

```
Checked 139 files against docs/handoff.json

   137 OK        byte-identical
     2 MISSING   never arrived here
         decks/s03_modeling_i.py
         figures/build/s03_cascade.png
```

- **MISSING** — it never arrived. Ask for it again. This is the failure the
  tool exists to catch.
- **DIFFERS** — it is here but not the version sent. Either you edited it, which
  you would know, or an older copy landed on top of a newer one.
- **EXTRA** — here and not in the handoff. Normally your own work. Ignore it.

It compares file *contents*, not timestamps, on purpose: the copy step restamps
every mtime, so on your Mac the sources always look newer than the deck built
from them even when nothing changed.

---

## 2. Authored versus generated

This is the distinction that prevents most of the confusion. Some files you (or
Claude) write by hand. Others are **produced by a command** and must never be
hand-edited, because the next build silently destroys your edit.

| Generated file | Produced by | Edit this instead |
|---|---|---|
| `private/build/decks/*.pptx` and `.pdf` | `tools/build_decks.py` | `decks/s03_modeling_i.py` |
| `figures/build/*.png`, `*.mp4` | `tools/build_figures.py` | `figures/s03_modeling_i.py` |
| `handouts/*.pdf` | `tools/build_handouts.py` | `handouts/*.md` |
| `board-notes/*.pdf` | `tools/build_handouts.py` | `board-notes/*.md` |
| `docs/readings.md` | `tools/build_readings.py` | `readings.yaml` |
| `problem-sets/*/ps01.ipynb` (student version) | `tools/build_problem_sets.py` | `private/sources/ps01.py` |
| `docs/handoff.json` | `tools/handoff.py --emit` | nothing — it is a receipt |

If you open a `.pptx` in PowerPoint, fix a typo and save it, `--verify` will
tell you: it reports **EDITED BY HAND after the build**. That is not a scolding,
it is a warning that the fix is about to be thrown away. Put it in the deck
source.

---

## 3. The two repositories, and what belongs in each

**Public** (`posb2026`) — CC BY 4.0. Everything students and the world can see:
notebooks, the `posb` package, docs, generated figures, **deck sources**,
handout PDFs, the syllabus and coverage matrix.

**Private** (`posb2026-private`) — mounted *inside* the public working copy as
`private/`, and gitignored by it, so the two never collide. Holds problem-set
masters with solutions, figures scanned from papers, supplementary movies, and
built decks.

```
~/Documents/Claude/Projects/PoSB/posb2026/          <- public repo
├── decks/  figures/  posb/  docs/  problem-sets/  sessions/
└── private/                        <- a SECOND repo, ignored by the first
    ├── sources/ps01.py             <- master, with solutions
    ├── paper-figures/*.png
    ├── paper-movies/*.mp4
    └── build/decks/*.pptx
```

Two repositories means **two pushes**. Committing in the public repo does not
commit anything under `private/`:

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026        && git add -A && git commit -m "..." && git push
cd ~/Documents/Claude/Projects/PoSB/posb2026/private && git add -A && git commit -m "..." && git push
```

### What never goes in either repo

Paper PDFs. You cannot redistribute them, not even privately. What the repo
holds is the *declaration* that a paper is assigned — `readings.yaml`, with a
DOI. What goes on bCourses is a **link through the UC Library proxy**, so
students authenticate as themselves.

---

## 4. How a deck reaches a projector, and a PDF reaches bCourses

```
decks/s03_modeling_i.py          you edit this
figures/build/*.png              embedded if present
private/paper-figures/*.png      embedded if present, dashed slot if not
        │
        │   python tools/build_decks.py s03 --pdf
        ▼
private/build/decks/PoSB_Session03_Modeling_I.pptx    <- project this
                                 ...Modeling_I.pdf     <- post this to bCourses
                                 ...pptx.deps.json     <- the receipt
```

The assembled `.pptx` is gitignored because it may embed figures from published
papers and the public repo is CC BY. So it never goes to GitHub. The **PDF goes
to bCourses**, which is behind CalNet — ordinary educational use.

**Before class, always:**

```bash
python tools/build_decks.py --verify
```

It builds nothing. It tells you whether the file you are about to teach from is
the one your current sources would produce. `up to date` is the only answer you
should walk into the room on.

---

## 5. How a notebook reaches a student

Students do not clone anything. They click one link, which clones for them.

```
https://datahub.berkeley.edu/hub/user-redirect/git-pull
  ?repo=https://github.com/ArkinLaboratory/posb2026
  &branch=main
  &urlpath=lab/tree/posb2026/problem-sets/ps01-modeling/ps01.ipynb
```

Generate and pre-flight all of them at once:

```bash
python tools/check_links.py
```

Three traps, all of which have bitten real courses:

1. **`urlpath` must include the clone folder** — `lab/tree/posb2026/…`, not
   `lab/tree/…`. Get it wrong and the pull *succeeds*, then JupyterLab says
   "Could not find path", which students read as *the assignment is missing*.
2. **The Berkeley link generator pre-fills `branch=master`** and prefers it over
   the branch it detected. Our default branch is `main`. Always read the
   `branch=` in a generated URL.
3. **`&backup=true` does nothing.** It is an nbgitpuller 1.3.0 feature and
   DataHub pins 1.2.2, which ignores it silently.

**Testing a link: incognito does not work.** A private window logs you into the
same CalNet ID and the same NFS home directory, where `~/posb2026` already
exists — so nbgitpuller takes the *update* path instead of cloning and tests
nothing. Either:

```bash
# in a DataHub terminal
mv ~/posb2026 ~/posb2026-mine
```

then click the link — or, better, have Hetvi click every link once. Her home
directory genuinely lacks the folder and she is a different identity, which also
catches the Berkeley-specific trap where DataHub's GitHub credential helper
lets *your* server clone private repos and no student's.

The Colab badge at the top of every notebook is the fallback when DataHub is
down. It needs no Berkeley anything.

---

## 6. The commands, in the order you actually use them

```bash
cd ~/Documents/Claude/Projects/PoSB/posb2026

# --- did the handoff land? ------------------------------------------------
python tools/handoff.py --check

# --- rebuild what changed -------------------------------------------------
python tools/build_figures.py            # figures/build/*.png
python tools/build_decks.py --pdf        # private/build/decks/
python tools/build_handouts.py           # handouts/*.pdf

# --- the checks. all of these build nothing -------------------------------
python tools/build_decks.py   --verify   # deck vs its sources, on THIS disk
python tools/build_figures.py --verify   # committed PNGs vs their generators
python tools/check_schedule.py           # course.yaml vs the course map
python tools/build_readings.py --check   # a paper is assigned before discussed
python tools/check_links.py              # nbgitpuller links
python -m pytest tests/ -q               # 48 tests

# --- publish --------------------------------------------------------------
git add -A && git commit -m "..." && git push
cd private && git add -A && git commit -m "..." && git push && cd ..
```

**The morning-of-lecture version** is three lines:

```bash
python tools/handoff.py --check
python tools/build_decks.py --verify
open private/build/decks/PoSB_Session03_Modeling_I.pptx
```

---

## 7. Rules that exist because something broke

- **Never let Claude run `git` in your repositories.** The file bridge cannot
  delete files, so a stranded `.git/index.lock` blocks your next commit and only
  you can clear it. This happened once.
- **A directory is not a deliverable.** Empty directories do not cross the
  bridge; only files do. `private/paper-movies/` "existed" in the sandbox and
  not on your Mac for an hour.
- **`.gitignore` patterns without a leading slash match at every level.** A bare
  `build/` matched `figures/build/` as well as the repo root, so no generated
  figure was ever committed and every figure link in the session READMEs was
  broken on GitHub. It is `/build/` now.
- **Do not commit the raw downloads next to the converted ones.** Four PNAS
  supplementary files went in at 76 MB alongside the 15 MB of converted mp4s the
  build actually reads. Fixed, but only because the repo was three commits old.
